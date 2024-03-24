from typing import Annotated, List
from services.auth.autentication import get_current_user
from services.users import *
from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.get_db import get_db
from sqlalchemy.orm import Session
from schemas.users import *




router = APIRouter(prefix='/users', tags=['Users'])
user_dependecies = Annotated[User, Depends(get_current_user)]

@router.post("/create", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def create_agency_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(db, user) 

@router.get("/me", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_me_endpoint(user_loggued: user_dependecies, db: Session = Depends(get_db)):
    if user_loggued is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized to get user')
    user = db.query(users_model).filter(users_model.id == user_loggued.id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/all-users/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users_endpoint(db: Session = Depends(get_db)):
    return await get_all_users(db)  

@router.get('/all-users/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_id_endpoint(user_id:int, db: Session = Depends(get_db)):
    return await get_user_by_id(db, user_id)

@router.put('/update/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def update_user_endpoint(user_id:int, user: UserUpdate, user_loggued:user_dependecies,db: Session = Depends(get_db)):
    if user_loggued is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not Authorized to update user')
    return await update_user(db, user_id, user)

@router.put('/{user_id}/deactive', response_model=UserResponse,status_code = status.HTTP_200_OK)
async def deactive_user_endpoint(user_id:int, user_loggued:user_dependecies,db:Session = Depends(get_db)):
    if user_loggued.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to deactivate a user')
    try:
        user = await deactive_user(db, user_id)
        return {'message': 'User deactivated', 'user': user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

