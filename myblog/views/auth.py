"""用户认证"""
from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user

from myblog.forms import LoginForm
from myblog.models import Admin
from myblog.utils import redirect_back

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # 如果当前用户已登陆，则重定向回博客主页
    if current_user.is_authenticated:
        return redirect(url_for('blog.html'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            # 验证用户名和密码
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('欢迎回来！', 'success')
                return redirect_back()
            flash('用户名或密码无效', 'warning')
        else:
            flash('该账户不存在', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功', 'info')
    return redirect_back()
