#encoding:utf-8
from wtforms import Form, StringField, IntegerField, PasswordField, ValidationError
from wtforms.validators import Length, NumberRange, DataRequired, Email

from app.models.user import User


class RegisterForm(Form):
  email = StringField(
      validators=[DataRequired(),
            Length(8, 64),
            Email(message='Email Not Validate')])
  password = PasswordField(
      validators=[DataRequired(message='Password Not Blank'),
            Length(6, 32)])
  nickname = StringField(
      validators=[DataRequired(),
            Length(2, 10, message='Nickname need gt 2 charsets')])

#业务校验
  def validate_email(self, field):
    if User.query.filter_by(email=field.data).first():
      raise ValidationError('电子邮件已被注册') #异常信息存贮在form.error 里

class LoginForm(Form):
  email = StringField(
      validators=[DataRequired(),
          Length(8, 64),
          Email(message='电子邮件不符合规范')])
  password = PasswordField(
      validators=[DataRequired(message='请输入密码'),
          Length(6, 32)])

class EmailForm(Form):
  email = StringField(validators=[DataRequired(), Length(8,64), Email(message='电子邮件不符合规范')])