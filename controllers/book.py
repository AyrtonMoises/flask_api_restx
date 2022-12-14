from flask import request
from flask_restx import Resource, fields

from marshmallow import ValidationError

from models.book import BookModel
from schemas.books import BookSchema
from server.instance import server


book_ns = server.api.namespace('books', description='Books related operations')

book_schema = BookSchema()
book_list_schema = BookSchema(many=True)

ITEM_NOT_FOUND = 'Book not found'

item = book_ns.model('Book', {
    'title': fields.String(description='Book title'),
    'pages': fields.Integer(default=0)
})

item_out = book_ns.model('Book', {
    'id': fields.Integer,
    'title': fields.String(description='Book title'),
    'pages': fields.Integer(default=0)
})

@book_ns.route('/<int:id>')
@book_ns.response(404, 'Book not found')
@book_ns.param('id', 'The book identifier')
class Book(Resource):

    @book_ns.doc('get_book')
    @book_ns.marshal_with(item)
    def get(self, id):
        '''Get book'''
        book_data = BookModel.find_by_id(id)
        if book_data:
            return book_schema.dump(book_data)
        return {'message': ITEM_NOT_FOUND}, 404

    @book_ns.expect(item)
    @book_ns.marshal_with(item)
    def put(self, id):
        '''Update book'''
        book_data = BookModel.find_by_id(id)
        book_json = request.get_json()

        book_data.pages = book_json['pages']
        book_data.title = book_json['title']

        book_data.save_to_db()
        return book_schema.dump(book_data), 200

    @book_ns.doc('delete_book')
    @book_ns.response(204, 'Book deleted')
    def delete(self, id):
        '''Delete book'''
        book_data = BookModel.find_by_id(id)
        if book_data:
            book_data.delete_from_db()
            return '', 204
        return {'message': ITEM_NOT_FOUND}


@book_ns.route('/')
class BookList(Resource):

    @book_ns.doc('list_books')
    @book_ns.marshal_list_with(item_out)
    def get(self):
        '''List all books'''
        return book_list_schema.dump(BookModel.find_all()), 200

    @book_ns.doc('create_book')
    @book_ns.expect(item)
    @book_ns.marshal_with(item, code=201)
    def post(self):
        '''Create a book'''
        book_json = request.get_json()
        try:                                                                         
            book_data = book_schema.load(book_json)
        except ValidationError as err:
            return err.messages, 422
        
        book_data.save_to_db()
        return book_schema.dump(book_data), 201