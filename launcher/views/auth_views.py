from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from launcher import db
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from launcher.models import User
from launcher.forms import LoginForm, RegisterForm

bp = Blueprint('auth', __name__, template_folder='templates', static_folder='static')

@bp.route("/")
def home():
    if session.get('logged_in'):
        return redirect(url_for('main.main'))
    else:
        return render_template('index.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        
        if user is not None:
            flash( f"{user.email}은 이미 등록된 계정입니다.", category="email_error" )
        else:
            new_user = User(fullname = form.fullname.data, 
                            email = form.email.data, 
                            password = generate_password_hash(form.password.data))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('.login'))

    return render_template('register.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm() 
    
    if request.method == 'POST' and form.validate_on_submit():  
        user = User.query.filter(User.email == form.email.data).first()
        
        if user is None:
            flash("등록되지 않은 계정입니다.", category="email_error")
        elif not check_password_hash(user.password, form.password.data):
            flash("비밀번호가 올바르지 않습니다.", category="pw_error")
        else:           
            session['logged_in'] = True
            session['user_id'] = user.id
            return redirect(url_for('.home'))

    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    session['logged_in'] = False
    session.pop('user_id', None)
    return render_template('index.html')
