from fastapi import FastAPI
from routes import router

app = FastAPI(title="Library API")

app.include_router(router, prefix="/books", tags=["Books"])
