"""博客前台视图函数"""
from flask import render_template, Blueprint, request, current_app, url_for, flash, redirect, abort, make_response
from flask_login import current_user

from myblog.models import Post, Category, Comment
from myblog.forms import AdminCommentForm, CommentForm
from myblog.extensions import db
from myblog.emails import send_new_comment_email, send_new_reply_email
from myblog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PRE_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/index.html', pagination=pagination, posts=posts)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_POST_PRE_PAGE']
    # with_parent(category)表示当前类别下的所有文章
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['MYBLOG_MANAGE_POST_PER_PAGE']
    # with_parent(post)表示当前文章下的所有评论,filter_by(reviewed=True)表示通过审核的评论
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.desc()).paginate(
        page, per_page)
    comments = pagination.items

    if current_user.is_authenticated:  # 如果当前用户已登陆，使用管理员表单
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['MYBLOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:  # 否则使用普通表单
        form = CommentForm()
        from_admin = False
        reviewed = False

    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed)
        replied_id = request.args.get('reply')
        if replied_id:  # 若果存在参数reply，表示是回复
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        if current_user.is_authenticated:  # send message based on authentication status
            flash('回复成功', 'success')
        else:
            flash('谢谢，您的评论将在审核后发表', 'info')
            send_new_comment_email(post)  # send notification email to admin
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, pagination=pagination, form=form, comments=comments)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('评论功能已关闭.', 'warning')
        return redirect(url_for('blog.show_post', post_id=comment.post.id))
    return redirect(
        url_for('blog.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')


@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['MYBLOG_THEMES'].keys():
        abort(404)

    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30 * 24 * 60 * 60)  # max_arg是设置cookies的有效期为30天
    return response
