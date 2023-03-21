""" M04 Lab - Case Study: Python APIs
    SDEV 220
    Paul R. Thompson
    Set up an API for Book
"""

from flask import Flask, request

from flask_sqlalchemy   import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(50), unique=True, nullable=False)
    author = db.Column(db.String(30))
    publisher = db.Column(db.String(50))

    def __repr__(self):
        return f'{self.book_name} - {self.author} - {self.publisher}'
    
@app.route('/')
def index():
    return 'Hello. The book API is here!'

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'name': book.book_name, 'Author': book.author, 'Publisher': book.publisher}
        output.append(book_data)
    return {'Books': output}

@app.route('/books/id')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'Name': book.book_name, 'Author': book.author, 'Publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name=request.json['book_name'], author=request.json['author'], publisher=reuest.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {'Error': 'Not Found'}
    db.session.delete(book)
    db.session.commit()
    return {'message': 'all gone'}