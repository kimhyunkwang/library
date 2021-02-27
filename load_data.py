import csv
from datetime import date, datetime

from launcher import db, create_app
from launcher.models import Book

session = db.session
app = create_app()

with app.app_context():
    with open('data/books.csv', 'r', encoding='UTF8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            publication_date = datetime.strptime(
                            row['publication_date'], '%Y-%m-%d').date()
            image_path = f"/static/image/{row['id']}"
            try:
                open(f'launcher/{image_path}.png')
                image_path += '.png'
            except:
                image_path += '.jpg'

            book = Book(
                # id = int(row['id']), 
                book_name = row['book_name'], 
                publisher = row['publisher'],
                author = row['author'], 
                publication_date = publication_date, 
                pages = int(row['pages']),
                isbn = row['isbn'], 
                description = row['description'],
                link = row['link'],
                image_path=image_path,
                stock=5,
                rating=0,
            )
            db.session.add(book)

        db.session.commit()