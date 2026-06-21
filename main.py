from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from db import engine,get_db
from model import User
from schemas import UserRegister

app = FastAPI()  

#Create tables
User.metadata.create_all(bind = engine) 
      
@app.post("/register")
def user_post_register(user:UserRegister, db:Session = Depends(get_db)):
    
    #Check duplicate email
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code= 400,detail= "Email already exist")
    
    # Save user
    new_user = User(
        username = user.username,
        email = user.email,
        password = user.password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "Register successfully",
        "data": new_user
    }
    
    

