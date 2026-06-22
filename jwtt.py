from fastapi import FastAPI, HTTPException, Depends
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "random_secret_string"

ALGORITHM = "HS256"

ACCESS_TOKEN_MINUTES = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl= "login")      #extract token from request
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone # Imported timezone

SECRET_KEY = "random_secret_string"
ALGORITHM = "HS256"
ACCESS_TOKEN_MINUTES = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):
    to_encode = data.copy()
    # FIX 1: Use explicit, timezone-aware UTC time
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # FIX 2: Return None here instead of crashing with an HTTPException
        return None

def get_current_user(token: str = Depends(oauth2_schema)):
    payload = verify_token(token)
    
    # FIX 2 (Cont.): Handle the HTTP error directly at the dependency layer
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return {
        "user_id": payload.get("user_id"),
        "email": payload.get("email")
    }

def create_access_token(data:dict):   #to_encode is the final payload data that will be packed into the JWT token, not request validation data
    
    to_encode = data.copy()    # data that will go inside the token
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_MINUTES)
    
    token = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail= "Invalid or expired token")


# Create dependency function
def get_current_user(token:str = Depends(oauth2_schema)):       #get_current_user() is the bridge between FastAPI routes and JWT
    payload = verify_token(token)           #internally uses verify_token() to validate the token
    return {
    "user_id": payload.get("user_id"),
    "email": payload.get("email")
    }
    
    
    
    

    
        

