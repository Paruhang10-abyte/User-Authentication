from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Boolean, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,Session,declarative_base
from pydantic import BaseModel


app = FastAPI()

DATABASE_URL = "postgresql://postgres:12345@localhost:5432/User_Registration"

# Engine create( DB Connection)

engine = create_engine(
    DATABASE_URL,
)

# Session (DB for operation)
SessionLocal = sessionmaker(bind = engine)

# Base (for model)
Base = declarative_base() 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()