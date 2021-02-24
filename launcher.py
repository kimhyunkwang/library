import pymysql
from flask import Flask, request, session, render_template, url_for, redirect
from flask_restful import reqparse, abort, Api, Resource
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

app = Flask(__name__)
api = Api(app)

db = pymysql.connect(
    user='root',
    host='127.0.0.1',
    port=3306,
    db='library',
    charset='utf8',
)

cursor = db.cursor()

app.config.from_mapping(SECRET_KEY='dev')

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
        
        if not fullname:
            error = 'Fullname이 유효하지 않습니다.'
        if not email:
            error = 'Email이 유효하지 않습니다.'
        elif not password:
            error = 'Password가 유효하지 않습니다.'
        elif not repeat_password:
            error = 'Repeat Password가 유효하지 않습니다.'

        sql = 'SELECT id FROM user WHERE email = %s'
        cursor.execute(sql, (email,))
        result = cursor.fetchone()
        if result is not None:
            error = '{} 은 이미 등록된 계정입니다.'.format(email)

        if password != repeat_password:
            error = 'Password와 Repeat Password가 다릅니다.'

        if error is None:
            sql = "INSERT INTO `user` (`email`, `fullname`, `password`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (email, fullname, generate_password_hash(password)))
            db.commit()
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
        
        sql = 'SELECT email, password FROM user WHERE email = %s'
        cursor.execute(sql, (email,))
        user = cursor.fetchone()
        
        if user is None:
            error = '등록되지 않은 계정입니다.'
        
        if not (user == None or check_password_hash(user[1], password)):
            error = '비밀번호가 틀렸습니다.'

        if error is None:
            session.clear()
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error=error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session['logged_in'] = False
    return render_template('index.html')


if __name__ == '__main__':
    app.debug = True
    app.run('localhost', port=5000)