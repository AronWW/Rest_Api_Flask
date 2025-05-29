from typing import List, Dict, Optional
from bson import ObjectId
from schemas import Book, BookCreate
from database import books_collection


async def get_all_books() -> List[Dict]:
    books = await books_collection.find().to_list(length=100)
    return books


async def get_book_by_id(book_id: str) -> Optional[Dict]:
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    return book


async def add_book(book_data: BookCreate) -> Dict:
    book_dict = book_data.model_dump()
    result = await books_collection.insert_one(book_dict)
    new_book = await books_collection.find_one({"_id": result.inserted_id})
    return new_book


async def delete_book(book_id: str) -> Optional[Dict]:
    book = await books_collection.find_one({"_id": ObjectId(book_id)})
    if book:
        await books_collection.delete_one({"_id": ObjectId(book_id)})
        return book
    return None