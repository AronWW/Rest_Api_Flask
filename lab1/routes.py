from flask import Blueprint, request, jsonify
from models import books
from schemas import book_schema, books_schema
from marshmallow import ValidationError

book_bp = Blueprint("books", __name__)

def find_book(book_id):
    return next((book for book in books if book["id"] == book_id), None)

# GET /books/
@book_bp.route("/", methods=["GET"])
def get_books():
    return jsonify(books_schema.dump(books)), 200

# GET /books/<id>
@book_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = find_book(book_id)
    if book:
        return jsonify(book_schema.dump(book)), 200
    return jsonify({"error": "Book not found"}), 404

# POST /books/
@book_bp.route("/", methods=["POST"])
def add_book():
    try:
        new_book_data = book_schema.load(request.json)  # клієнт не передає id
    except ValidationError as err:
        return jsonify(err.messages), 400

    max_id = max(book["id"] for book in books) if books else 0
    new_book = {"id": max_id + 1, **new_book_data}

    books.append(new_book)
    return jsonify(book_schema.dump(new_book)), 201

# DELETE /books/<id>
@book_bp.route("/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    books.remove(book)
    return jsonify({"message": f"Book {book_id} deleted"}), 200
