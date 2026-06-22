from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from utils import pwd_context
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jwtt import get_current_user, create_access_token
from fastapi.middleware.cors import CORSMiddleware

from db import engine,get_db
from model import User
from schemas import UserRegister, UserLogin, UserUpdate, UserEmailUpdate, UserPasswordUpdate, UserDelete

app = FastAPI()  

#Create tables
User.metadata.create_all(bind = engine) 


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Add CORS middleware here
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins (you can restrict later)
    allow_credentials=True,
    allow_methods=["*"],        # allow all HTTP methods
    allow_headers=["*"],        # allow all headers
)
     
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
    }
    
    
@app.post("/login")
def user_post_login(from_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    
    db_user = db.query(User).filter(User.email == from_data.username).first()
    
    if not db_user:
        raise HTTPException(status_code= 400, detail= "Email not found")
    
    try:
        is_valid = pwd_context.verify(from_data.password, db_user.password)
    except Exception:
        # Fallback: if the stored password is plain text (legacy)
        is_valid = from_data.password == db_user.password
        if not is_valid:
            raise HTTPException(status_code= 400, detail= "Incorrect Password")
    
    token = create_access_token({
        "user_id": db_user.id,
        "email": db_user.email
    })
    
    return{
        "message": "Login Successfully",
        "access_token": token,
        "token_type": "bearer"
    #     "data": db_user
    }
    
@app.get("/profile")
def profile(current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    user = db.query(User).filter(User.id == current_user["user_id"]).first()  #Take the value of user_id from the decoded token payload

    if not user:
        raise HTTPException(status_code= 404, detail = "User not found")
    
    return{
        "username": user.username,
        "email": user.email,
        "id": user.id
    }
    
@app.patch("/update-username")
def update_profile(update_data: UserUpdate, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    # Fetch the actual user from the DB using the ID from the token
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if not db_user:
        raise HTTPException(status_code= 404, detail= "user Not Found")
    
    # Only check and update the username
    if update_data.username is not None:
        db_user.username = update_data.username
        
    db.commit()
    db.refresh(db_user)
    
    return{
        "message": "Update User Profile Successfully",
        "user":{
            "id": db_user.id,
            "user_name": db_user.username,
            "email": db_user.email
        }
        
    }
 
@app.patch("/user-email")   
def update_email(update_email:UserEmailUpdate, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    # Fetch the actual user from the DB using the ID from the token
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if not db_user:
        raise HTTPException(status_code = 404, detail = "Email Not Found")
    
    if update_email.email is not None:
        db_user.email = update_email.email
        
    db.commit()
    db.refresh(db_user)
    
    return{
        "message": "Update User Email Successfully",
        "user":{
            "id": db_user.id,
            "user_name": db_user.username,
            "email": db_user.email
        }
        
    }
    

@app.patch("/Update-password")
def update_user_pasword(update_password:UserPasswordUpdate, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    
    # Fetch the actual user from the DB using the ID from the token
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if not db_user:
        raise HTTPException(status_code = 404, detail = "Email Not Found")
    
    # Check if the old password provided matches the stored hashed password
    if not pwd_context.verify(update_password.old_password, db_user.password):
        raise HTTPException(status_code= 400, detail= "Incorrect old password")
    
     # Hash and update new password
    db_user.password = pwd_context.hash(update_password.new_password)
    
    db.commit()
    db.refresh(db_user)
     
    return{
        "message": "Update User Password Successfully"
    }

@app.delete("/Delete")
def delete_user(current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    
    # Fetch the actual user from the DB using the ID from the token
    db_user = db.query(User).filter(User.id == current_user["user_id"]).first()
    
    if not db_user:
        raise HTTPException(status_code = 404, detail = "user Not Found")
    
    db.delete(db_user)
    db.commit()
    
    return{
        "message": "User deleted successfully"
    }
    

    
        
    
    
     
       
    
   
    
    
    
    
    

