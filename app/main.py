import os
from fastapi import FastAPI
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load variables from .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="BuildAI API")

# Create a SQLAlchemy engine once, reused across requests
engine = create_engine(DATABASE_URL, pool_pre_ping=True) if DATABASE_URL else None


@app.get("/")
def root():
    return {"status": "BuildAI is running"}


@app.get("/health/db")
def check_db():
    if not engine:
        return {"status": "error", "detail": "DATABASE_URL not set in .env"}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "detail": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


@app.post("/api/v1/estimate")
def estimate(payload: dict):
    return {"message": "Hello, BuildAI is alive", "input": payload}