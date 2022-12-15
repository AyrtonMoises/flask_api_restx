from models.book import BookModel


def test_create_book():
    """ Test create book """
    book = BookModel(
        title='Meu livro',
        pages=150
    )

    assert book.title == 'Meu livro'
    assert book.pages == 150
