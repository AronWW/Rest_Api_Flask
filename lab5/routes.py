from fastapi import APIRouter, HTTPException, status
from typing import List

import models
from schemas import Book, BookCreate

router = APIRouter(tags=["books"])


@router.get("/books", response_model=List[Book], status_code=status.HTTP_200_OK)
async def get_books():
    return await models.get_all_books()


@router.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book(book_id: str):
    book = await models.get_book_by_id(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено"
        )
    return book


@router.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def add_book(book: BookCreate):
    return await models.add_book(book)


@router.delete("/books/{book_id}", status_code=status.HTTP_200_OK)
async def delete_book(book_id: str):
    book = await models.delete_book(book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Книгу не знайдено"
        )
    return {"message": f"Книгу '{book['title']}' успішно видалено"}