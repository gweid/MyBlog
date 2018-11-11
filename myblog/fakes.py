"""创建的虚拟博客管理员信息、文章、分类和评论"""
import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from myblog.models import Admin, Category, Post, Comment, Link
from myblog.extensions import db

fake = Faker('zh_CN')


def fake_admin():
    """虚拟管理员信息"""
    admin = Admin(
        username="super",
        blog_title="维度's Blog",
        blog_sub_title="快乐生活，快乐编程！",
        name="Gweid",
        about="我，Gweid，一个小小的程序员..."
    )
    admin.set_password('123456')
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    """生成虚拟分类"""
    category = Category(name='默认')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    """生成虚拟文章"""
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            timestamp=fake.date_time_this_year(),
            # 每一篇文章指定一个随机分类，主键值为1到所有分类数量之间的随机值
            category=Category.query.get(random.randint(1, Category.query.count()))
        )
        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    """生成虚拟评论"""
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)  # 未审核评论、管理员评论和回复都是50条

    # 未审核评论
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 管理员评论
        comment = Comment(
            author="Gweid",
            email="Gweid@example.com",
            site="example.com",
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    """分享链接"""
    micro_blog = Link(name='微博', url='#')
    wechat_circle = Link(name='朋友圈', url='#')
    qq_zone = Link(name='知乎', url='#')
    linkedin = Link(name='豆瓣', url='#')
    db.session.add_all([micro_blog, wechat_circle, qq_zone, linkedin])
    db.session.commit()
