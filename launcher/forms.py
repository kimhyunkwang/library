from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Regexp, EqualTo
import email_validator

class RegisterForm(FlaskForm):

    name_reg = r"(^[a-zA-Z]+$)|(^[ㄱ-ㅣ가-힣]+$)"
    email_reg = r"(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[!@#$%^&*])"

    fullname = StringField('fullname', 
                            validators=[DataRequired('이름을 입력해주세요.'),
                                        Regexp(name_reg, message='이름은 한글 또는 영문으로만 입력해주세요.')])
    email = StringField('email', 
                        validators=[DataRequired('이메일을 입력해주세요.'), 
                                    Email('이메일 형식으로 입력해주세요.')])
    password = PasswordField('password', 
                            validators=[DataRequired('비밀번호를 입력해주세요.'), 
                                        Length(min=8, max=30, message='비밀번호는 8자 이상 입력해주세요.'),
                                        Regexp(email_reg, message='비밀번호는 영문, 숫자, 특수문자를 각 하나 이상 포함하여야 합니다.')])
    repeat_password = PasswordField('repeat_password', 
                                    validators=[DataRequired('비밀번호를 다시 한 번 입력해주세요.'),
                                                EqualTo('password', message='비밀번호가 일치하지 않습니다.')])


class LoginForm(FlaskForm):
    email = StringField('email', 
                        validators=[DataRequired('이메일을 입력해주세요.'), 
                                    Email('이메일 형식으로 입력해주세요.')])
    password = PasswordField('password', 
                            validators=[DataRequired('비밀번호를 입력해주세요.'), 
                                        Length(min=8, max=30, message='비밀번호는 8자 이상 입력해주세요.')])
