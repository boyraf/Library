# Import necessary libraries
import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

# Set up virtual environment using Pipenv
# pipenv.install()  # Removed Pipenv installation step

# Set up database using SQLAlchemy ORM
Base = declarative_base()
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()

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

# Define CLI application functions
def add_book(title, author_name, genre_name):
    # Check if author exists in database
    author = session.query(Author).filter_by(name=author_name).first()
    if not author:
        # If author does not exist, create new author
        author = Author(name=author_name)
        session.add(author)
        session.commit()

    # Check if genre exists in database
    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        # If genre does not exist, create new genre
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()

    # Create new book with given title and author
    book = Book(title=title, author=author, genre=genre)
    session.add(book)
    session.commit()

def update_book(book_title, new_title=None, new_author_name=None, new_genre_name=None):
    # Check if book exists in database
    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        # If book does not exist, return error message
        return "Book not found in library"

    # Update book title if new_title is given
    if new_title:
        book.title = new_title

    # Update book author if new_author_name is given
    if new_author_name:
        # Check if author exists in database
        author = session.query(Author).filter_by(name=new_author_name).first()
        if not author:
            # If author does not exist, create new author
            author = Author(name=new_author_name)
            session.add(author)
            session.commit()

        # Update book author
        book.author = author

    # Update book genre if new_genre_name is given
    if new_genre_name:
        # Check if genre exists in database
        genre = session.query(Genre).filter_by(name=new_genre_name).first()
        if not genre:
            # If genre does not exist, create new genre
            genre = Genre(name=new_genre_name)
            session.add(genre)
            session.commit()

        # Update book genre
        book.genre = genre

    # Commit changes to database
    session.commit()

def delete_book(book_title):
    # Check if book exists in database
    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        # If book does not exist, return error message
        return "Book not found in library"

    # Delete book from database
    session.delete(book)
    session.commit()

def loan_book(user_name, book_title):
    # Check if user exists in database
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        # If user does not exist, create new user
        user = User(name=user_name)
        session.add(user)
        session.commit()

    # Check if book exists in database
    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        # If book does not exist, return error message
        return "Book not found in library"

    # Create new loan with given user and book
    loan = Loan(user=user, book=book)
    session.add(loan)
    session.commit()

def return_book(user_name, book_title):
    # Check if user exists in database
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        # If user does not exist, return error message
        return "User not found in library"

    # Check if book exists in database
    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        # If book does not exist, return error message
        return "Book not found in library"

    # Find loan with given user and book
    loan = session.query(Loan).filter_by(user=user, book=book).first()

    # Delete loan from database to indicate that the book has been returned
    session.delete(loan)
    session.commit()

def view_books():
    # Query all books from database and print their titles and authors
    books = session.query(Book).all()
    for book in books:
        print(f"{book.title} by {book.author.name}")

def view_loans():
    # Query all loans from database and print the user and book for each loan
    loans = session.query(Loan).all()
    for loan in loans:
        print(f"{loan.user.name} has borrowed {loan.book.title}")

def view_books_by_author(author_name):
    # Query all books by given author from database and print their titles
    books = session.query(Book).join(Author).filter(Author.name == author_name).all()
    for book in books:
        print(book.title)

def report_books_by_user(user_name):
    # Query all loans by given user from database and print the titles of the borrowed books
    loans = session.query(Loan).join(User).filter(User.name == user_name).all()
    for loan in loans:
        print(loan.book.title)

def report_favorite_author(user_name):
    # Query all loans by given user from database and count the number of loans for each author
    loans = session.query(Loan).join(User).filter(User.name == user_name).all()
    author_count = {}
    for loan in loans:
        author_name = loan.book.author.name
        if author_name in author_count:
            author_count[author_name] += 1
        else:
            author_count[author_name] = 1

    # Find the author with the most loans and print their name
    favorite_author = max(author_count, key=author_count.get)
    print(favorite_author)

def report_books_by_author(author_name):
    # Query all books by given author from database and count the number of books
    books = session.query(Book).join(Author).filter(Author.name == author_name).all()
    num_books = len(books)
    print(f"{author_name} has written {num_books} books")

# Define CLI interface using while loop and input() function
while True:
    print("Menu:")
    print("1. Add book")
    print("2. Update book")
    print("3. Delete book")
    print("4. Loan book")
    print("5. Return book")
    print("6. View books")
    print("7. View loans")
    print("8. View books by author")
    print("9. Report books by user")
    print("10. Report favorite author")
    command = input("Enter command: ")

    # Validate user input
    if command not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]:
        print("Invalid command.")
        continue

    # Execute command
    if command == "1":
        # Get book title
        title = input("Enter book title: ")
        # Get author name
        author_name = input("Enter author name: ")
        # Get genre name
        genre_name = input("Enter genre name: ")
        add_book(title, author_name, genre_name)
    elif command == "2":
        # Get book title
        book_title = input("Enter book title: ")
        # Get new title
        new_title = input("Enter new title: ")
        # Get new author name
        new_author_name = input("Enter new author name: ")
        # Get new genre name
        new_genre_name = input("Enter new genre name: ")
        update_book(book_title, new_title, new_author_name, new_genre_name)
    elif command == "3":
        # Get book title
        book_title = input("Enter book title: ")
        delete_book(book_title)
    elif command == "4":
        # Get user name
        user_name = input("Enter user name: ")
        # Get book title
        book_title = input("Enter book title: ")
        loan_book(user_name, book_title)
    elif command == "5":
        # Get user name
        user_name = input("Enter user name: ")
        # Get book title
        book_title = input("Enter book title: ")
        return_book(user_name, book_title)
    elif command == "6":
        view_books()
    elif command == "7":
        view_loans()
    elif command == "8":
        # Get author name
        author_name = input("Enter author name: ")
        view_books_by_author(author_name)
    elif command == "9":
        # Get user name
        user_name = input("Enter user name: ")
        report_books_by_user(user_name)
    elif command == "10":
        # Get user name
        user_name = input("Enter user name: ")
        report_favorite_author(user_name)
