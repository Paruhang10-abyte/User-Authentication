from fastapi import FastAPI,HTTPException
from pydantic import BaseModel, field_validator
from model import User
from db import SessionLocal

app = FastAPI()

class UserRegister(BaseModel):
    id: int
    username: str
    email: str
    password: str
    
    @field_validator("email")
    def check_email(cls,v):
        if not v.endswith("@gmail.com"):
            raise ValueError("Email must be @gmail.com")
        return v
       
    @field_validator("password")
    def check_password(cls,v):
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v