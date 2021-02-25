from launcher import db

class User(db.Model):
    # __tablename__ = 'user_table'

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password

# class Book(db.model):
#     id = db.Column(db.Integer, primary_key=True)
#     bookname = db.Column(db.String(64), nullable=False)
#     publisher = db.Column(db.String(64), nullable=False) 
#     author = db.Column(db.String(64), nullable=False) 
#     publication_date = db.Column(db.Date(), nullable=False)
#     pages = db.Column(db.Integer, nullable=False)
#     isbn = db.Column(db.String(64), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     link = db.Column(db.String(128), nullable=False)

#     def __init__(self, )