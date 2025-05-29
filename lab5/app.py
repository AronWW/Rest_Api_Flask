from fastapi import FastAPI
from routes import router
import uvicorn
from database import init_db

app = FastAPI(
    title="Book API", description="API для бібліотеки", version="1.0.0"
)

app.include_router(router)


@app.on_event("startup")
async def startup_db_client():
    await init_db()


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)