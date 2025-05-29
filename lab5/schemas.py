from pydantic import BaseModel, Field
from pydantic_mongo import ObjectIdField
from bson import ObjectId
from typing import Optional


class BookBase(BaseModel):
    title: str
    author: str
    year: int
    isbn: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    id: ObjectIdField = Field(default_factory=ObjectId, alias="_id")

    class Config:
        populate_by_name = True
        json_encoders = {ObjectId: str}