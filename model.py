from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Boolean
from db import Base,engine

#Table (Model)
class User(Base):
    __tablename__ ="Users"
    id = Column(Integer, primary_key= True, index= True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    
# Create Table (Outside Class)
Base.metadata.create_all(bind = engine)




    
    