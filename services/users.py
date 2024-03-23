from sqlite3 import IntegrityError
from schemas.agency import AgencyCreate
from schemas.users import *
from sqlalchemy.orm import Session
from models.models import Users as users_model
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(pwd:str):
    return pwd_context.hash(pwd)

def verify_password(plain_text: str, pwd:str):
    return pwd_context.verify(plain_text, pwd)

def get_users_by_email(db:Session, email:str):
    return db.query(users_model).filter(users_model.email == email).first()

def get_user_by_username(db:Session, username:str):
    return db.query(users_model).filter(users_model.username == username).first()

async def create_user(db: Session, user: UserCreate):
    try:
        password = hash_password(user.password)
        user_exist = get_users_by_email(db, user.email)
        username_exits = get_user_by_username(db, user.username)
        if username_exits:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" username already registered")
        elif user_exist:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=" email already registered")
        user_dict = user.model_dump(exclude={'password'})
        user_dict['hashed_password'] = password 
        db_user = users_model(**user_dict)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    except IntegrityError as e:
        db.rollback()  
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Database integrity error. {e}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return user


async def get_all_users(db: Session):
    user = db.query(users_model).all()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Do not have any user")
    return user

async def get_user_by_id(db:Session, user_id:int):
    current_user =  db.query(users_model).filter(users_model.id == user_id).first()
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return current_user

async def update_user(db:Session, user_id:int, user: UserUpdate):
    user_to_update = await get_user_by_id(db, user_id)
    if user_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for var, value in vars(user).items():
       setattr(user_to_update, var, value) if value else None
    db.commit()
    db.refresh(user_to_update)
    return user_to_update

async def deactive_user(db:Session, user_id:int):
    user = db.query(users_model).filter(users_model.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User not found')
    user.status = 'inactive'
    db.commit()
    db.refresh(user)
    return user	