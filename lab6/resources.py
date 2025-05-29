from flask_restful import Resource, reqparse
from flask import request
from models import db, Book
from schemas import book_schema, books_schema
from marshmallow import ValidationError
from flasgger import swag_from

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Books API",
        "description": "API for managing books",
        "version": "1.0"
    },
    "definitions": {
        "Book": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "readOnly": True},
                "title": {"type": "string"},
                "author": {"type": "string"},
                "year": {"type": "integer"}
            },
            "required": ["title", "author", "year"]
        }
    }
}

class BookListResource(Resource):
    @swag_from({
        'tags': ['books'],
        'description': 'Get a paginated list of books',
        'parameters': [
            {
                'name': 'page',
                'in': 'query',
                'type': 'integer',
                'default': 1,
                'description': 'Page number'
            },
            {
                'name': 'per_page',
                'in': 'query',
                'type': 'integer',
                'default': 10,
                'description': 'Items per page'
            }
        ],
        'responses': {
            200: {
                'description': 'List of books',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'books': {
                            'type': 'array',
                            'items': {'$ref': '#/definitions/Book'}
                        },
                        'total': {'type': 'integer'},
                        'pages': {'type': 'integer'},
                        'current_page': {'type': 'integer'}
                    }
                }
            }
        }
    })
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)
        return {
            'books': books_schema.dump(pagination.items),
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page
        }

    @swag_from({
        'tags': ['books'],
        'description': 'Create a new book',
        'parameters': [
            {
                'in': 'body',
                'name': 'body',
                'required': True,
                'schema': {
                    '$ref': '#/definitions/Book'
                }
            }
        ],
        'responses': {
            201: {
                'description': 'Book created',
                'schema': {'$ref': '#/definitions/Book'}
            },
            400: {
                'description': 'Validation error',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def post(self):
        try:
            new_book_data = book_schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        new_book = Book(**new_book_data)
        db.session.add(new_book)
        db.session.commit()
        return book_schema.dump(new_book), 201


class BookResource(Resource):
    @swag_from({
        'tags': ['books'],
        'description': 'Get a single book by ID',
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'Book ID'
            }
        ],
        'responses': {
            200: {
                'description': 'Book found',
                'schema': {'$ref': '#/definitions/Book'}
            },
            404: {
                'description': 'Book not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def get(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        return book_schema.dump(book), 200

    @swag_from({
        'tags': ['books'],
        'description': 'Delete a book by ID',
        'parameters': [
            {
                'name': 'book_id',
                'in': 'path',
                'type': 'integer',
                'required': True,
                'description': 'Book ID'
            }
        ],
        'responses': {
            200: {
                'description': 'Book deleted',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'}
                    }
                }
            },
            404: {
                'description': 'Book not found',
                'schema': {
                    'type': 'object',
                    'properties': {
                        'error': {'type': 'string'}
                    }
                }
            }
        }
    })
    def delete(self, book_id):
        book = Book.query.get(book_id)
        if not book:
            return {"error": "Book not found"}, 404
        db.session.delete(book)
        db.session.commit()
        return {"message": f"Book {book_id} deleted"}, 200