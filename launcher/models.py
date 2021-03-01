from launcher import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(64), nullable=False)
    publisher = db.Column(db.String(64), nullable=False) 
    author = db.Column(db.String(64), nullable=False) 
    publication_date = db.Column(db.Date(), nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    image_path = db.Column(db.String(128), nullable=False)

    def __init__(self, book_name, publisher, author, publication_date, pages, isbn, description, link, stock, rating, image_path):
        self.book_name = book_name
        self.publisher = publisher
        self.author = author
        self.publication_date = publication_date
        self.pages = pages
        self.isbn = isbn
        self.description = description
        self.link = link
        self.stock = stock
        self.rating = rating
        self.image_path = image_path

class BookRental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship('Book')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('book_rental_set'))
    rental_date = db.Column(db.Date(), nullable=False)
    return_date = db.Column(db.Date(), nullable=True)

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), nullable=False)
    book = db.relationship('Book', backref=db.backref('comment_set'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User')
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    rating = db.Column(db.Integer, nullable=False)