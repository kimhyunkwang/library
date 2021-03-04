from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
import email_validator

class RegisterForm(FlaskForm):
    fullname = StringField('fullname', validators=[DataRequired('이름을 입력해주세요.')])
    email = StringField('email', validators=[DataRequired('이메일을 입력해주세요.'), Email('이메일 형식으로 입력해주세요.')])
    password = PasswordField('password', validators=[DataRequired('비밀번호를 입력해주세요.')])
    repeat_password = PasswordField('repeat_password', validators=[DataRequired('비밀번호를 다시 한 번 입력해주세요.')])

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired('이메일을 입력해주세요.'), Email('이메일 형식으로 입력해주세요.')])
    password = PasswordField('password', validators=[DataRequired('비밀번호를 입력해주세요.')])