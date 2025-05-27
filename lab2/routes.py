from fastapi import APIRouter, HTTPException
from typing import List
from models import books
from schemas import Book, BookCreate

router = APIRouter()

def find_book(book_id: int):
    return next((book for book in books if book["id"] == book_id), None)

def get_next_id():
    if not books:
        return 1
    return max(book["id"] for book in books) + 1

@router.get("/", response_model=List[Book])
async def get_books():
    return books

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("/", response_model=Book, status_code=201)
async def add_book(book_data: BookCreate):
    new_id = get_next_id()
    new_book = {
        "id": new_id,
        "title": book_data.title,
        "author": book_data.author,
        "year": book_data.year
    }
    books.append(new_book)
    return new_book

@router.delete("/{book_id}")
async def delete_book(book_id: int):
    book = find_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    books.remove(book)
    return {"message": f"Book {book_id} deleted"}