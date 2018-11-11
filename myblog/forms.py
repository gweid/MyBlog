from flask_wtf import FlaskForm
from flask_ckeditor import CKEditorField
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, HiddenField, \
    ValidationError
from wtforms.validators import DataRequired, Length, Email, URL, Optional

from myblog.models import Category


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住')
    submit = SubmitField('登陆')


class SettingForm(FlaskForm):
    """设置表单"""
    name = StringField('博客名', validators=[DataRequired(), Length(1, 20)])
    blog_title = StringField('博客标题', validators=[DataRequired(), Length(1, 60)])
    blog_sub_title = StringField('博客副标题', validators=[DataRequired(), Length(1, 100)])
    about = CKEditorField('关于', validators=[DataRequired()])
    submit = SubmitField('确定')


class PostForm(FlaskForm):
    """文章表单"""
    title = StringField('标题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int, default=1)  # 发表文章时的类别选择
    body = CKEditorField('正文', validators=[DataRequired()])
    submit = SubmitField('确定')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(cate.id, cate.name) for cate in Category.query.order_by(Category.name).all()]


class CategoryForm(FlaskForm):
    """分类名表单"""
    name = StringField('类名', validators=[DataRequired()])
    submit = SubmitField('确定')

    # 验证类名是否重复
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('类名已存在')


class CommentForm(FlaskForm):
    """评论表单"""
    author = StringField('名字', validators=[DataRequired(), Length(1, 30)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 254)])
    # Optional()使字段可以为空,URL()检验是URL否有效
    site = StringField('站点', validators=[Optional(), URL(), Length(0, 255)])
    body = TextAreaField('评论', validators=[DataRequired()])
    submit = SubmitField('确定')


class AdminCommentForm(CommentForm):
    """管理员评论表单,把管理员评论的author,email,site选项隐藏"""
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()


class LinkForm(FlaskForm):
    """分享链接表单"""
    name = StringField('名字', validators=[DataRequired(), Length(1, 30)])
    url = StringField('站点', validators=[DataRequired(), URL(), Length(0, 255)])
    submit = SubmitField('确定')
