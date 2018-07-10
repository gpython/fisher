#encoding:utf-8
from threading import Thread

from app import mail
from flask_mail import Message
from flask import current_app, render_template



def send_async_email(app, msg):
  with app.app_context():
    try:
      mail.send(msg)
    except Exception as e:
      print('Mail Exception %s' %e)
      pass

#to 邮件要发送给谁
#subject 标题
#template 模板
def send_mail(to, subject, template, **kwargs):
  msg = Message('[Fasher]' + subject,
                sender=current_app.config['MAIL_USERNAME'],
                body=template,
                recipients=[to])
  msg.html = render_template(template, **kwargs)
  app = current_app._get_current_object()
  thr = Thread(target=send_async_email, args=[app, msg])
  thr.start()
  pass
