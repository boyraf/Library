from sqlalchemy import  String, Column, Integer , create_engine, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
# Define tables using SQLAlchemy ORM
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author_id = Column(Integer, ForeignKey('authors.id'))
    genre_id = Column(Integer, ForeignKey('genres.id'))
    author = relationship('Author', back_populates='books')
    genre = relationship('Genre', back_populates='books')

    def __repr__(self):
        return f"<Book(title='{self.title}', author='{self.author.name}', genre='{self.genre.name}')>"

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='author')

    def __repr__(self):
        return f"<Author(name='{self.name}')>"

class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    books = relationship('Book', back_populates='genre')

    def __repr__(self):
        return f"<Genre(name='{self.name}')>"

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return f"<User(name='{self.name}')>"

class Loan(Base):
    __tablename__ = 'loans'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    book_id = Column(Integer, ForeignKey('books.id'))
    user = relationship('User')
    book = relationship('Book')

    def __repr__(self):
        return f"<Loan(user='{self.user.name}', book='{self.book.title}')>"

# Create database tables
Base.metadata.create_all(engine)