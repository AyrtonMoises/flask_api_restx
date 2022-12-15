def test_get_book(client, books_fixture):
    """ List books """
    response = client.get("/api/books/1")
    assert response.status_code == 200
    assert response.json ==  {
            "title": "Meu livro 1",
            "pages": 150
        }

def test_get_books(client, books_fixture):
    """ List books """
    response = client.get("/api/books")
    assert response.status_code == 200
    assert response.json == [
        {
            "title": "Meu livro 1",
            "pages": 150
        },
        {
            "title": "Meu livro 2",
            "pages": 150
        },
        {
            "title": "Meu livro 3",
            "pages": 150
        },
    ]
    

def test_post_book(client):
    """" Create book """
    data = {
        "title": "Meu livro 4",
        "pages": 50
    }
    response = client.post("/api/books", json=data)
    assert response.status_code == 201
    response_json = response.json
    assert response_json == data


def test_update_book(client):
    """" Update book """
    data = {
        "title": "Meu livro editado",
        "pages": 100
    }
    response = client.put("/api/books/1", json=data)
    assert response.status_code == 200

    book_edit = response.json
    assert book_edit['title'] == data['title']
    assert book_edit['pages'] == data['pages']


def test_delete_book(client):
    """" Delete book """
    response = client.delete("/api/books/1")
    assert response.status_code == 204

    response_book_delete = client.get("/api/books/1")
    assert response_book_delete.status_code == 404
