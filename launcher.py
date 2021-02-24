import pymysql
from flask import Flask, request, session, render_template, url_for, redirect
from flask_restful import reqparse, abort, Api, Resource
from flask_migrate import Migrate
import config
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
# from models import db
# from models import User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://root:@localhost:3306/library?charset=utf8")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'
# app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)


class User(db.Model):
    # __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.set_password(password)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)


@app.route("/")
def home():
    if session.get('logged_in'):
        return render_template('loggedin.html')
    else:
        return render_template('index.html') 


@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']
        repeat_password = request.form['repeat-password']
        
        error = None

        if not(fullname and email and password and repeat_password):
            error = "입력되지 않은 정보가 있습니다."
        elif password != repeat_password:
            error = '비밀번호가 일치하지 않습니다.'
        else:
            data = User.query.filter(User.email == email).first()
            if data is not None:
                error = f'{email} 은 이미 등록된 계정입니다.'

        if error is None:
            new_user = User(fullname, email, password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error=error)
        
    return render_template('register.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        error = None
        
        data = User.query.filter(User.email == email).first()
        
        if data is None:
            error = '등록되지 않은 계정입니다.'
        
        if not (data == None or check_password_hash(data.password, password)):
            error = '비밀번호가 틀렸습니다.'

        if error is None:
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('index.html')


@app.route('/all')
def select_all():
    users = User.query.all()
    return render_template('db.html', users = users)


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run('localhost', port=5000)