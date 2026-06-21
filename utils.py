from fastapi import FastAPI
from passlib.context import CryptContext

# password manager object -----> use bcrypt for hashing
pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")   #helps manage old password hashes safely when upgrading security methods