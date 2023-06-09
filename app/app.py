
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Book , Genre , Author , User , Loan
from generate_books import generate_seed_data


# Set up database using SQLAlchemy ORM
Base = declarative_base()
engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()



# Define CLI application functions
def add_book(title, author_name, genre_name):
    author = session.query(Author).filter_by(name=author_name).first()
    if not author:
        author = Author(name=author_name)
        session.add(author)
        session.commit()

    genre = session.query(Genre).filter_by(name=genre_name).first()
    if not genre:
        genre = Genre(name=genre_name)
        session.add(genre)
        session.commit()
    book = session.query(Book).filter_by(title=title).first()
    if book:
        return "Book already in this database"
    else:
        book = Book(title=title, author=author, genre=genre)
        session.add(book)
        session.commit()
        print("Your book has been added to the database.")
def update_book(book_title, new_title=None, new_author_name=None, new_genre_name=None):
    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        return "Book not found in library"

    if new_title:
        book.title = new_title

    if new_author_name:
        author = session.query(Author).filter_by(name=new_author_name).first()
        if not author:
            author = Author(name=new_author_name)
            session.add(author)
            session.commit()

        book.author = author

    if new_genre_name:
        genre = session.query(Genre).filter_by(name=new_genre_name).first()
        if not genre:
            genre = Genre(name=new_genre_name)
            session.add(genre)
            session.commit()

        book.genre = genre

    session.commit()
    print("Your book has been updated in the database.")
def add_user(name):
    user = session.query(User).filter_by(name=name).first()
    if not user:
        user = User(name=name)
        session.add(user)
        session.commit()
        print("The User has been added to the database.")
    else:
        print("User already exists.")

def remove_user(name):
    user = session.query(User).filter_by(name=name).first()
    if not user:
        print("No user by that name in this database.")
    if user:
        session.delete(user)
        session.commit()
        print("The User has been removed.")
    else:
        print("User not found.")

def delete_book(book_title):
    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        return "Book not found in library"

    session.delete(book)
    session.commit()
    print("Your book has beeen deleted from the database.")

def loan_book(user_name, book_title):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        user = User(name=user_name)
        session.add(user)
        session.commit()

    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        return "Book not found in library"

    loan = Loan(user=user, book=book)
    session.add(loan)
    session.commit()

def return_book(user_name, book_title):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        return "User not found in library"

    book = session.query(Book).filter_by(title=book_title).first()
    if not book:
        return "Book not found in library"

    loan = session.query(Loan).filter_by(user=user, book=book).first()

    session.delete(loan)
    session.commit()

def view_books():
    books = session.query(Book).all()
    for book in books:
        print(f"{book.title} by {book.author.name}")

def view_loans():
    loans = session.query(Loan).all()
    for loan in loans:
        print(f"{loan.user.name} has borrowed {loan.book.title}")

def view_books_by_author(author_name):
    books = session.query(Book).join(Author).filter(Author.name == author_name).all()
    for book in books:
        print(book.title)

def report_books_by_user(user_name):
    loans = session.query(Loan).join(User).filter(User.name == user_name).all()
    for loan in loans:
        print(loan.book.title)

def report_favorite_author(user_name):
    loans = session.query(Loan).join(User).filter(User.name == user_name).all()
    author_count = {}
    for loan in loans:
        author_name = loan.book.author.name
        if author_name in author_count:
            author_count[author_name] += 1
        else:
            author_count[author_name] = 1

    favorite_author = max(author_count, key=author_count.get)
    print(favorite_author)

def report_books_by_author(author_name):
    books = session.query(Book).join(Author).filter(Author.name == author_name).all()
    num_books = len(books)
    print(f"{author_name} has written {num_books} books")

def find_most_popular_genre():
    loans = session.query(Loan).all()
    genre_count = {}

    for loan in loans:
        genre = loan.book.genre
        if genre in genre_count:
            genre_count[genre] += 1
        else:
            genre_count[genre] = 1

    popular_genre = max(genre_count.items(), key=lambda x: x[1], default=(None, 0))

    if popular_genre[0] is not None:
        print(f"The most popular genre loaned is '{popular_genre[0].name}' with {popular_genre[1]} loans.")
    else:
        print("No loans found in the library.")


def display_table_data(command):
    if command == "9":
        view_books()
    elif command == "10":
        view_loans()
    elif command == "11":
        author_name = input("Enter author name: ")
        view_books_by_author(author_name)
    elif command == "12":
        user_name = input("Enter user name: ")
        report_books_by_user(user_name)
    elif command == "13":
        user_name = input("Enter user name: ")
        report_favorite_author(user_name)
    elif command == "14":
        find_most_popular_genre()


# def view_books():
#     books = session.query(Book).all()
#     for book in books:
#         print(f"{book.title} by {book.author.name}")

def view_users():
    users = session.query(User).all()
    for user in users:
        print(user.name)



def books_borrowed_by_user(user_name):
    user = session.query(User).filter_by(name=user_name).first()
    if not user:
        print("User not found in library.")
        return

    loans = session.query(Loan).filter_by(user=user).all()
    if not loans:
        print("No books borrowed by the user.")
        return

    for loan in loans:
        print(f"Book: {loan.book.title}")
        print(f"Author: {loan.book.author.name}")
        print("---")

while True:
    print("----------Library Management System----------")
    print("Menu:")
    print("1. Add book")
    print("2. Update book")
    print("3. View Users")
    print("4. Add User")
    print("5. Remove User")
    print("6. Delete book")
    print("7. Loan book")
    print("8. Return book")
    print("9. View books")
    print("10. View loans")
    print("11. View books by author")
    print("12. Report books by user")
    print("13. Report favorite author")
    print("14. Find most popular genre")
    print("15. Exit")
    command = input("Enter command(1-14): ")

    if command not in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]:
        print("Invalid command.")
        continue

    # Execute command
    if command == "1":
        #view_books()
        title = input("Enter book title: ")
        author_name = input("Enter author name: ")
        genre_name = input("Enter genre name: ")
        add_book(title, author_name, genre_name)
    elif command == "2":
        #view_books()
        book_title = input("Enter book title: ")
        new_title = input("Enter new title: ")
        new_author_name = input("Enter new author name: ")
        new_genre_name = input("Enter new genre name: ")
        update_book(book_title, new_title, new_author_name, new_genre_name)
    elif command == "3":
        view_users()
    elif command == "4":
        view_users()
        user_name = input("Enter user name: ")
        add_user(user_name)
        view_users()
    elif command == "5":
        view_users()
        user_name = input("Enter user name: ")
        remove_user(user_name)
        view_users()
    elif command == "6":
        #view_books()
        book_title = input("Enter book title: ")
        delete_book(book_title)
    elif command == "7":
        view_users()
        user_name = input("Enter user name: ")
        books_borrowed_by_user(user_name)
        book_title = input("Enter book title: ")
        loan_book(user_name, book_title)
        books_borrowed_by_user(user_name)
    elif command == "8":
        view_users()
        user_name = input("Enter user name: ")
        books_borrowed_by_user(user_name)
        book_title = input("Enter book title: ")
        return_book(user_name, book_title)
        books_borrowed_by_user(user_name)
    elif command == "9" or command == "10" or command == "11" or command == "12" or command == "13" or command == "14":
        display_table_data(command)
    elif command == "15":
        print("Goodbye")
        break

if __name__ == '__main__':
    engine = create_engine('sqlite:///library.db')
    Base.metadata.create_all(engine)
    generate_seed_data()
    
