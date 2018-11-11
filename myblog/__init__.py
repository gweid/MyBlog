"""使用工厂函数创建程序实例"""
import os

import click
from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFError
from flask_login import current_user

from myblog.settings import config
from myblog.views.blog import blog_bp
from myblog.views.auth import auth_bp
from myblog.views.admin import admin_bp
from myblog.models import Admin, Category, Link, Comment, Post
from myblog.extensions import bootstrap, db, mail, ckeditor, moment, csrf, login_manager


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('myblog')
    app.config.from_object(config[config_name])

    register_logging(app)  # 注册日志处理函数
    register_extensions(app)  # 注册扩展（扩展初始化）
    register_blueprints(app)  # 注册蓝本
    register_shell_context(app)  # 注册shell上下文处理函数
    register_template_context(app)  # 注册模板上下文处理函数
    register_errors(app)  # 注册错误处理函数
    register_commands(app)  # 注册自定义shell命令

    return app


def register_logging(app):
    pass


def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()  # order_by排序规则
        links = Link.query.order_by(Link.name).all()
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, links=links, unread_comments=unread_comments)


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help="删除数据库后新建")
    def initdb(drop):
        if drop:
            click.confirm('此操作将删除数据库，是否继续？', abort=True)
            db.drop_all()
            click.echo('删除表...')
        db.create_all()
        click.echo('初始化数据库...')

    # 用于创建一个管理员
    @app.cli.command()
    @click.option('--username', prompt=True, help="用于登录的用户名")
    # hide_input输入密码是隐藏状态的，confirmation_prompt二次输入密码确认
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help="用于登录的密码")
    def init(username, password):
        click.echo('初始化数据库...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:  # 如果管理员已经存在就更新用户名和密码
            click.echo('管理员已经存在，正在更新...')
            admin.username = username
            admin.set_password(password)
        else:  # 否则，创建新管理员
            click.echo('创建临时管理员帐户...')
            admin = Admin(
                username="admin",
                blog_title="维度's Blog",
                blog_sub_title="快乐生活，快乐编程！",
                name="Gweid",
                about="我，Gweid，一个小小的程序员..."
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('创建默认分类...')
            category = Category(name='默认')
            db.session.add(category)

        db.session.commit()
        click.echo('完成')

    @app.cli.command()
    @click.option('--category', default=10, help='类别数量，默认为10')
    @click.option('--post', default=50, help='文章数量，默认为50')
    @click.option('--comment', default=500, help='评论数量，默认为500')
    def forge(category, post, comment):
        """生成虚假数据。"""
        from myblog.fakes import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('生成管理员...')
        fake_admin()

        click.echo('生成 %d 个分类...' % category)
        fake_categories(category)  # 这里的category代表数量，下同

        click.echo('生成 %d 篇文章...' % post)
        fake_posts(post)

        click.echo('生成 %d 条评论...' % comment)
        fake_comments(comment)

        click.echo('生成分享链接...')
        fake_links()

        click.echo('完成')
