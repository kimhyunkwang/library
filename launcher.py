import pymysql
from flask import Flask, jsonify, request, session
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

# session을 위한 secret_key 설정
app.config.from_mapping(SECRET_KEY='dev')

parser = reqparse.RequestParser()
parser.add_argument('id')
parser.add_argument('email')
parser.add_argument('fullname')
parser.add_argument('password')


@app.route("/")
def home():
    if session['user_id']:
        return render_template('loggedin.html')
    else:
        return render_template('index.html') 


@app.route('/user/register', methods=('GET', 'POST'))
def register():
    args = parser.parse_args()
    if request.method == 'POST':
        sql = "INSERT INTO `user` (`fullname`, `email`, `password`) VALUES (%s, %s, %s)"
        cursor.execute(sql, (args['fullname'], args['email'], generate_password_hash(args['password'])))
        db.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')


@app.route('/user/login', methods=('GET', 'POST'))
def login():
    args = parser.parse_args()
    if request.method == 'POST':
        sql = "SELECT password FROM `user` WHERE `email` = %s"
        cursor.execute(sql, (args["email"], ))
        user_info = cursor.fetchone()
        if user_info:
            if check_password_hash(user_info[0], args["password"]):
                session.clear()
                session['user_id'] = args["email"]
	
                return redirect(url_for('home'))
            else:
                return "비밀번호를 확인해주세요."
        else:
            return "존재하지 않는 계정입니다."
    else:
        return render_template('login.html')


@app.route('/user/logout')
def logout():
    session.clear()
    return render_template('index.html')


if __name__ == '__main__':
    app.run('localhost', port=5000)