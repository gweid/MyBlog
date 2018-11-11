"""数据库"""
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from myblog.extensions import db


class Admin(db.Model, UserMixin):
    """管理员模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    blog_sub_title = db.Column(db.String(100))
    name = db.Column(db.String(30))
    about = db.Column(db.Text)

    # 设置管理员密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 登录时验证密码是否正确
    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 分类与文章建立双向一对多关系
class Category(db.Model):
    """存储文章分类的模型"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)  # 分类名称不允许重复，所以unique(唯一性)设置为True

    posts = db.relationship('Post', back_populates='category')

    def delete(self):
        default_category = Category.query.get(1)
        posts = self.posts[:]
        for post in posts:
            post.category = default_category
        db.session.delete(self)
        db.session.commit()


class Post(db.Model):
    """存储文章模型"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    can_comment = db.Column(db.Boolean, default=True)  # 是否允许评论

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    # 通过cascade设置级联删除，即文章删除则该文章所有的评论也会删除
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')


# 文章与评论也是双向一对多关系
class Comment(db.Model):
    """存储评论的模型"""
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))  # 站点
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)  # 用来判断是否是管理员的评论
    reviewed = db.Column(db.Boolean, default=False)  # 用来判断是否通过审核
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    # 在同一模型内建立一对多关系将评论与回复内容联系起来
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))  # 设置一个外键指向本身
    replies = db.relationship('Comment', back_populates='replied', cascade='all, delete-orphan')
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])


# 链接
class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
