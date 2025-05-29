import motor.motor_asyncio
from bson import ObjectId

client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb://mongo_admin:password@mongodb:27017"
)
db = client.book_library
books_collection = db.books


async def init_db():
    count = await books_collection.count_documents({})
    if count == 0:
        await books_collection.insert_many(
            [
                {
                    "title": "1984",
                    "author": "George Orwell",
                    "year": 1949,
                    "isbn": "978-966-01-0585-5",
                },
                {
                    "title": "Brave New World",
                    "author": "Aldous Huxley",
                    "year": 1932,
                    "isbn": "978-966-10-4104-0",
                },
            ]
        )