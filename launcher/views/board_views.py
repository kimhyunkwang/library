from flask import Blueprint, request, session, url_for, render_template, redirect
from launcher import db
from launcher.models import Article
import datetime

bp = Blueprint('board', __name__, template_folder='templates', static_folder='static')

@bp.route('/board', methods=('GET', 'POST'))
def board():
    if request.method == 'POST':
        user_id = session['user_id']
        author = request.form['author']
        book_name = request.form['book_name']
        create_date = datetime.datetime.now()

        new_article = Article(user_id = user_id, 
                            author = author,
                            book_name = book_name,
                            create_date = create_date,
                            check = False)
        db.session.add(new_article)
        db.session.commit()

        return redirect(url_for('.board'))

    articles = Article.query.all()
    return render_template('board.html', articles = articles)
