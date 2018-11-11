"""用来存储扩展实例化"""
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_ckeditor import CKEditor
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect

bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
ckeditor = CKEditor()
moment = Moment()
login_manager = LoginManager()
csrf = CSRFProtect()


@login_manager.user_loader
def load_user(user_id):
    from myblog.models import Admin
    user = Admin.query.get(int(user_id))
    return user


# 设置登陆视图端点值
login_manager.login_view = 'auth.login'
# 如果没有登陆就访问设置界面的url显示提示
login_manager.login_message_category = '请先登录'
