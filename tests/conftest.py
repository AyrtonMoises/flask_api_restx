import pytest

from db import db
from models.book import BookModel
from app import app as app_


@pytest.fixture(scope="session")
def app():
    app = app_

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
    app.config["DEBUG"] = True
    app.config["TESTING"] = True
    db.init_app(app)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="module")
def books_fixture(app):
    with app.app_context():
        data = [
            BookModel(title="Meu livro 1", pages=150),
            BookModel(title="Meu livro 2", pages=150),
            BookModel(title="Meu livro 3", pages=150),
        ]
    db.session.bulk_save_objects(data)
    db.session.commit()
    return BookModel.query.all()
