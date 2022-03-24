from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flaskalchemy import Book, Base

app = Flask(__name__)

# Connection to database and making a session
engine = create_engine("sqlite:///books-collection.db", connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Page where all books will be shown
# This page will be only for read
@app.route('/')
@app.route('/books')
def show_books():
    books = session.query(Book).all()
    return render_template("books.html", books=books)


# This function lets to create new book and save it in db
@app.route('/books/new', methods=['GET', 'POST'])
def new_books():
    if request.method == 'POST':
        new_book = Book(title=request.form['name'], author=request.form['author'], genre=request.form['genre'])
        session.add(new_book)
        session.commit()
        return redirect(url_for('show_books'))
    else:
        return render_template('new_books.html')


# This function allows updating info and save it in db
@app.route('/books/<int:book_id>/edit', methods=['GET', 'POST'])
def edit_book(book_id):
    edited_book = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        edited_book.title = request.form['name']
        return redirect(url_for('show_books'))
    else:
        return render_template('edit_book.html', book=edited_book)


# This function allows deleting book from db
@app.route('/books/<int:book_id>/delete', methods=['GET', 'POST'])
def delete_book(book_id):
    del_book = session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        session.delete(del_book)
        session.commit()
        return redirect(url_for('show_books'))
    else:
        return render_template('delete_book.html', book=del_book)


if __name__ == '__main__':
    app.debug = True
    app.run(port=4996)
