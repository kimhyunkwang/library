import pymysql
from flask import Flask, request, session, url_for, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # app.config.from_object(config)
    app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://root:@localhost:3306/library?charset=utf8")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'dev'

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)

    from launcher.models import User

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
                new_user = User(fullname, email, generate_password_hash(password))
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

    return app

if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.run('localhost', port=5000)