from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.store.db import init_db
from app.api import courses, flashcards, life_balance, sessions
import uvicorn
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(title="StudySync AI", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router Endpoints
app.include_router(courses.router)
app.include_router(flashcards.router)
app.include_router(life_balance.router)
app.include_router(sessions.router)

@app.get("/health")
def health_check():
    return {"status": "StudySync Core API is Running"}

# Mount Frontend Directory
frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../frontend"))
app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

