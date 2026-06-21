from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from utils import pwd_context

from db import engine,get_db
from model import User
from schemas import UserRegister, UserLogin

app = FastAPI()  

#Create tables
User.metadata.create_all(bind = engine) 
      
@app.post("/register")
def user_post_register(user:UserRegister, db:Session = Depends(get_db)):
    
    #Check duplicate email
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code= 400,detail= "Email already exist")
    
    hashed_password = pwd_context.hash(user.password)
    
    # Save user
    new_user = User(
        username = user.username,
        email = user.email,
        password = hashed_password
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
        "message": "Register successfully",
        "data": new_user
    }
    
    
@app.post("/login")
def user_post_login(user:UserLogin, db:Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(status_code= 400, detail= "Email not found")
    
    is_valid = pwd_context.verify(user.password, db_user.password)
    if not is_valid:
        raise HTTPException(status_code= 400, detail= "Incorrect Password")
  
    
    return{
        "message": "Login Successfully"
    #     "data": db_user
    }
    
    
    
   
    
    
    
    
    

