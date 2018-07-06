#encoding:utf-8
from app import mail
from flask_mail import Message
from flask import current_app, render_template


#to 邮件要发送给谁
#subject 标题
#template 模板
def send_mail(to, subject, template, **kwargs):
  #recipients = [收件人用户列表]
  # msg = Message('Test', sender='artup_a@163.com',
  #               body='Test_content',
  #               recipients=['artup_a@163.com'])

  msg = Message('[Fasher]' + subject,
                sender=current_app.config['MAIL_USERNAME'],
                body=template,
                recipients=[to])
  msg.html = render_template(template, **kwargs)
  mail.send(msg)
  pass
