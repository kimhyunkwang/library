from flask import Blueprint, request, session, url_for, render_template, redirect, flash
from launcher import db
from launcher.models import Book, BookRental, Comment
import datetime

bp = Blueprint('book', __name__, template_folder='templates', static_folder='static')

@bp.route('/books/<int:book_id>', methods=('GET', 'POST'))
def book_info(book_id):
    if request.method == 'POST':
        user_id = session['user_id']

        book_rental = BookRental.query.filter(BookRental.book_id == book_id, BookRental.user_id == user_id).first()
        comment = Comment.query.filter(Comment.book_id == book_id, Comment.user_id == user_id).first()

        if book_rental and not comment:

            content = request.form['content']
            rating = request.form['rating']
            create_date = datetime.datetime.now()

            new_comment = Comment(book_id = book_id, 
                                user_id = user_id, 
                                content = content, 
                                rating = rating, 
                                create_date = create_date)
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
            return redirect(url_for('.book_info', book_id = book_id))
        
        else:
            flash("댓글을 작성할 수 없습니다.")

    book = Book.query.get(book_id)
    comments = Comment.query.filter(Comment.book_id == book_id).all()
    return render_template('book_info.html', book = book, comments = comments)
