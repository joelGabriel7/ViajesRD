from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext 
from api.deps.get_db import get_db
from models.models import Users   
from schemas.users import UserCreate, UserUpdate

SECRET_KEY = "1ffd17bc3bd1b6a1f08cefe1300fa6de273124cb0fe7bf22f1c8e8228160fcba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = timedelta(minutes=30)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    return db.query(Users).filter(Users.username == username).first()

def authenticate_user( username: str,password:str, db: Session = Depends(get_db)):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


