from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flaskalchemy import Base, Book


engine = create_engine("sqlite:///books-collection.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

bookOne = Book(title='Clear Python', author='Дэн Бейде', genre='computer literature')
session.add(bookOne)
session.commit()

book_del = session.query(Book).filter_by(id=1).one()
session.delete(book_del)
session.commit()
