from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
from models import Book, Genre, Author, User, Loan, engine

# Define your models and engine here

Session = sessionmaker(bind=engine)
session = Session()

def generate_seed_data():
    fake = Faker()
    for _ in range(10):
        title = fake.catch_phrase()
        author_name = fake.name()
        genre_name = fake.word()

        author = session.query(Author).filter_by(name=author_name).first()
        if not author:
            author = Author(name=author_name)
            session.add(author)

        genre = session.query(Genre).filter_by(name=genre_name).first()
        if not genre:
            genre = Genre(name=genre_name)
            session.add(genre)

        book = Book(title=title, author=author, genre=genre)
        session.add(book)

    session.commit()

generate_seed_data()
