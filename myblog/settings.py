import os
import sys

if sys.platform.startswith('win'):
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


class BaseConfig(object):
    SECRET_KEY = os.getenv("SECRET_KEY", "secret string")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465

    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Myblog Admin', MAIL_USERNAME)

    MYBLOG_EMAIL = os.getenv('MYBLOG_EMAIL')
    MYBLOG_POST_PRE_PAGE = 10  # 文章列表页每页显示的数量
    MYBLOG_COMMENT_PER_PAGE = 15  # 每篇文章下是的评论数
    MYBLOG_MANAGE_POST_PER_PAGE = 15  # 管理文章列表显示的文章标题数

    MYBLOG_THEMES = {'charming': '迷你绿', 'vibrant_sea': '海景蓝', 'black_swan': '天鹅黑'}  # 主题选择


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class ProductionConFig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'production': ProductionConFig,
}
