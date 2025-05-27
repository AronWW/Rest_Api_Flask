from flask import Blueprint, request, jsonify
from models import db, Book
from schemas import book_schema, books_schema
from marshmallow import ValidationError

book_bp = Blueprint("books", __name__)

# GET /books/ with pagination
@book_bp.route("/", methods=["GET"])
def get_books():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    books_pagination = Book.query.paginate(page=page, per_page=per_page, error_out=False)
    books = books_pagination.items
    
    return jsonify({
        'books': books_schema.dump(books),
        'total': books_pagination.total,
        'pages': books_pagination.pages,
        'current_page': books_pagination.page
    }), 200

# GET /books/<id>
@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(book_schema.dump(book)), 200
    return jsonify({"error": "Book not found"}), 404

# POST /books/
@book_bp.route("/", methods=["POST"])
def add_book():
    try:
        new_book_data = book_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400

    new_book = Book(**new_book_data)
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify(book_schema.dump(new_book)), 201

# DELETE /books/<id>
@book_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    
    return jsonify({"message": f"Book {book_id} deleted"}), 200