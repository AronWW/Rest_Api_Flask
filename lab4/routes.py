from flask import Blueprint, request, jsonify
from models import db, Book
from schemas import book_schema, books_schema
from marshmallow import ValidationError

book_bp = Blueprint("books", __name__)

@book_bp.route("/", methods=["GET"])
def get_books():
    limit = request.args.get('limit', 10, type=int)
    cursor = request.args.get('cursor', type=int)  
    direction = request.args.get('direction', 'next')  
    
    limit = min(limit, 100)
    
    query = Book.query
    
    if cursor:
        if direction == 'next':
            query = query.filter(Book.id > cursor).order_by(Book.id.asc())
        elif direction == 'prev':
            query = query.filter(Book.id < cursor).order_by(Book.id.desc())
        else:
            return jsonify({"error": "Invalid direction. Use 'next' or 'prev'"}), 400
    else:
        query = query.order_by(Book.id.asc())

    books = query.limit(limit + 1).all()

    has_more = len(books) > limit
    if has_more:
        books = books[:limit]  

    if cursor and direction == 'prev':
        books = books[::-1]

    next_cursor = books[-1].id if books and has_more else None
    prev_cursor = books[0].id if books and cursor else None
    
    response_data = {
        'books': books_schema.dump(books),
        'pagination': {
            'has_more': has_more,
            'next_cursor': next_cursor,
            'prev_cursor': prev_cursor,
            'limit': limit
        }
    }
    
    return jsonify(response_data), 200

@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        return jsonify(book_schema.dump(book)), 200
    return jsonify({"error": "Book not found"}), 404

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

@book_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    
    return jsonify({"message": f"Book {book_id} deleted"}), 200