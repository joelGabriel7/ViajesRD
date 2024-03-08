from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext 
from api.deps.get_db import get_db
from models.models import Users
from schemas.auth import TokenData   
from typing import Annotated, Union

SECRET_KEY = "1ffd17bc3bd1b6a1f08cefe1300fa6de273124cb0fe7bf22f1c8e8228160fcba"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRATION = timedelta(minutes=30)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


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

def create_access_token(data:dict, expires_delta: Union[timedelta,None] = None):
        to_encode = data.copy()
        if expires_delta:
             expire = datetime.now(timezone.utc) + expires_delta
        else:
            to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
        return encoded_jwt


async def get_current_user(token:Annotated[str, Depends(oauth2_scheme)]):
    credential_exception = HTTPException(
        status_code=401,
        detail= 'No se puedo validar las credenciales',
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username  = payload.get('username')
        user_role = payload.get('role')
        if username or user_role is None:
            raise  credential_exception
        token_data = TokenData(username=username,role=user_role)
    except JWTError:
        raise credential_exception  
    user = get_user(Session=Depends(get_db), username=token_data.username)
    if user is None:
        raise credential_exception
    return user 



