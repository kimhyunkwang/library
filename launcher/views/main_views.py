from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from launcher import db
from launcher.models import Book, BookRental
import datetime

bp = Blueprint('main', __name__, template_folder='templates', static_folder='static')

@bp.route('/main', methods=('GET', 'POST'))
def main():
    if request.method == 'POST':
        book_id = request.form["book-id"]
        user_id = session['user_id']

        book = Book.query.filter(Book.id == book_id).first()

        # 재고가 있는 경우
        if book.has_stock():
            book_rental = BookRental.query.filter(BookRental.book_id == book_id, 
                                                BookRental.user_id == user_id, 
                                                BookRental.return_date == None).first()
            
            # 대여해서 반납하지 않은 경우 -> 대여 불가
            if book_rental:
                flash("고객님께서 대여 중인 책입니다.")
                return redirect(url_for('.main'))

            # 대여한 적이 없는 경우와 대여한 적 있지만 반납 완료한 경우 -> 대여 가능
            now = datetime.datetime.now()
            nowDate = now.strftime('%Y-%m-%d')

            book.reduce_stock()
            book_rental = BookRental(book_id = book_id, user_id = user_id, rental_date = nowDate)
            db.session.add(book_rental)
            db.session.commit()
                
            flash(book.book_name + "을(를) 대여했습니다.")
            return redirect(url_for('.main'))

        # 재고가 없는 경우
        else:
            flash("모든 책이 대출 중입니다.")

    page = request.args.get('page', type=int, default=1)

    book_list = Book.query.order_by(Book.id)
    book_list = book_list.paginate(page, per_page=8)

    return render_template('main.html', book_list=book_list)


@bp.route('/rental')
def rental():
    book_rentals = BookRental.query.filter(BookRental.user_id == session['user_id']).all()
    return render_template('rental.html', book_rentals=book_rentals)


@bp.route('/return', methods=('GET', 'POST'))
def return_book():
    if request.method == 'POST':
        book_id = request.form["book-id"]
        user_id = session['user_id']

        book = Book.query.filter(Book.id == book_id).first()
        book.add_stock()

        now = datetime.datetime.now()
        nowDate = now.strftime('%Y-%m-%d')
        book_rental = BookRental.query.filter(BookRental.book_id == book_id, 
                                            BookRental.user_id == user_id, 
                                            BookRental.return_date == None).first()
        book_rental.return_date = nowDate
            
        db.session.commit()
            
        flash(book.book_name + "을(를) 반납했습니다.")
        return redirect(url_for('.return_book'))

    else:
        book_rentals = BookRental.query.filter(BookRental.user_id == session['user_id']).all()
        return render_template('return.html', book_rentals=book_rentals)
