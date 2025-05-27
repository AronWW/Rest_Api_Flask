from pydantic import BaseModel, Field, validator
from typing import Optional

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Назва книги")
    author: str = Field(..., min_length=1, max_length=100, description="Автор книги")
    year: int = Field(..., ge=0, le=2100, description="Рік публікації")

    @validator("title")
    def title_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("Назва книги не може бути порожньою")
        return value

    @validator("author")
    def author_must_not_be_blank(cls, value):
        if not value.strip():
            raise ValueError("Ім'я автора не може бути порожнім")
        return value

class Book(BookCreate):
    id: int = Field(..., ge=1, description="ID книги")