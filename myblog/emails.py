from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from myblog.extensions import mail


# 异步发送
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


# 通用发信函数(异步)
def send_mail(subject, to, html):
    app = current_app._get_current_object()  # 获取被代理的程序实例
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


# 新评论提醒邮件
def send_new_comment_email(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    send_mail(subject='新评论', to=current_app.config['MYBLOG_EMAIL'],
              html='<p>文章<i>%s</i>有新评论，点击下面的链接检查：</p>'
                   '<p><a href="%s"></a>%s</p>'
                   '<p><small style="color: #868e96">不要回复这封邮件。</small></p>'
                   % (post.title, post_url, post_url))


# 新回复提醒邮件
def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_mail(subject='新回复', to=comment.email,
              html='<p>你在帖子<i>%s</i>中的留言有新回复，点击下面的链接检查：</p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">不要回复这封邮件。</small></p>'
                   % (comment.post.title, post_url, post_url))
