import pymysql
from flask import Flask, request, session, url_for, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import config
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import datetime
from launcher.forms import LoginForm, RegisterForm

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://root:1234@localhost:3306/library?charset=utf8")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'dev'

    db.init_app(app)
    migrate.init_app(app, db)

    from launcher.models import User, Book, BookRental, Comment

    @app.route("/")
    def home():
        if session.get('logged_in'):
            return redirect(url_for('main'))
        else:
            return render_template('index.html')


    @app.route('/register', methods=('GET', 'POST'))
    def register():
        form = RegisterForm()
 
        if request.method == 'POST' and form.validate_on_submit():

            fullname = form.fullname
            email = form.email
            password = form.password
            repeat_password = form.repeat_password

            user = User.query.filter(User.email == email.data).first()
            
            # 이름은 영어 또는 한국어 검사 추가
            if user is not None:
                email.errors.append(f'{email.data}은 이미 등록된 계정입니다.')
            # 비밀번호 3종류 8자리, 2종류 10자리 검사 추가
            elif password.data != repeat_password.data:
                repeat_password.errors.append('비밀번호가 일치하지 않습니다.')
            else:
                new_user = User(fullname = fullname.data, email = email.data, password = generate_password_hash(password.data))
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))

        return render_template('register.html', form=form)


    @app.route('/login', methods=('GET', 'POST'))
    def login():
        form = LoginForm() 
        
        if request.method == 'POST' and form.validate_on_submit():  
            user = User.query.filter(User.email == form.email.data).first()
            
            if user is None:
                form.email.errors.append('등록되지 않은 계정입니다.')
            elif not check_password_hash(user.password, form.password.data):
                form.password.errors.append('비밀번호가 올바르지 않습니다.')
            else:           
                session['logged_in'] = True
                session['user_id'] = user.id
                return redirect(url_for('home'))

        return render_template('login.html', form=form)


    @app.route('/logout')
    def logout():
        session['logged_in'] = False
        session.pop('user_id', None)
        return render_template('index.html')


    @app.route('/main', methods=('GET', 'POST'))
    def main():
        if request.method == 'POST':
            book_id = request.form["book-id"]
            user_id = session['user_id']

            book = Book.query.filter(Book.id == book_id).first()

            # 재고가 있는 경우
            if book.stock > 0:
                book_rental = BookRental.query.filter(BookRental.book_id == book_id, BookRental.user_id == user_id, BookRental.return_date == None).first()
                
                # 대여해서 반납하지 않은 경우 -> 대여 불가
                if book_rental:
                    flash("고객님께서 대여 중인 책입니다.")
                    books = Book.query.all()
                    return render_template('main.html', books=books)

                # 대여한 적이 없는 경우와 대여한 적 있지만 반납 완료한 경우 -> 대여 가능
                now = datetime.datetime.now()
                nowDate = now.strftime('%Y-%m-%d')

                book.stock -= 1
                book_rental = BookRental(book_id = book_id, user_id = user_id, rental_date = nowDate)
                db.session.add(book_rental)
                db.session.commit()
                    
                flash(book.book_name + "을(를) 대여했습니다.")
                return redirect(url_for('main'))

            # 재고가 없는 경우
            else:
                flash("모든 책이 대출 중입니다.")
                books = Book.query.all()
                return render_template('main.html', books=books)

        else:
            page = request.args.get('page', type=int, default=1)

            book_list = Book.query.order_by(Book.id)
            book_list = book_list.paginate(page, per_page=8)

            return render_template('main.html', book_list=book_list)


    @app.route('/rental')
    def rental():
        book_rentals = BookRental.query.filter(BookRental.user_id == session['user_id']).all()
        return render_template('rental.html', book_rentals=book_rentals)


    @app.route('/return', methods=('GET', 'POST'))
    def return_book():
        if request.method == 'POST':
            book_id = request.form["book-id"]
            user_id = session['user_id']

            book = Book.query.filter(Book.id == book_id).first()
            book.stock += 1

            now = datetime.datetime.now()
            nowDate = now.strftime('%Y-%m-%d')
            book_rental = BookRental.query.filter(BookRental.book_id == book_id, BookRental.user_id == user_id, BookRental.return_date == None).first()
            book_rental.return_date = nowDate
                
            db.session.commit()
                
            flash(book.book_name + "을(를) 반납했습니다.")
            return redirect(url_for('return_book'))

        else:
            book_rentals = BookRental.query.filter(BookRental.user_id == session['user_id']).all()
            return render_template('return.html', book_rentals=book_rentals)


    @app.route('/books/<int:book_id>', methods=('GET', 'POST'))
    def book_info(book_id):
        if request.method == 'POST':
            content = request.form['content']
            rating = request.form['rating']
            user_id = session['user_id']
            create_date = datetime.datetime.now()

            new_comment = Comment(book_id = book_id, user_id = user_id, content = content, rating = rating, create_date = create_date)
            db.session.add(new_comment)
            db.session.commit()

            ratings = db.session.query(Comment.rating).filter(Comment.book_id == book_id).all()
            total = 0
            for rating in ratings:
                total += rating[0]
            rating_avg = round( total / len(ratings) )
            book = Book.query.get(book_id)
            book.rating = rating_avg
            db.session.commit()
            return redirect(url_for('book_info', book_id = book_id))

        else:
            book = Book.query.get(book_id)
            comments = Comment.query.filter(Comment.book_id == book_id).all()
            return render_template('book_info.html', book = book, comments = comments)
        

    return app

if __name__ == '__main__':
    db.create_all()
    app.run('localhost', port=5000, debug=True)