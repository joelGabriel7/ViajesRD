from typing import List
from services.users import *
from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.get_db import get_db
from sqlalchemy.orm import Session
from schemas.users import *




router = APIRouter(prefix='/users', tags=['Users'])

@router.post("/create", response_model=UserCreate, status_code=status.HTTP_201_CREATED)
async def create_agency_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(db, user) 

@router.get("/all-users/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_all_users_endpoint(db: Session = Depends(get_db)):
    return await get_all_users(db)  

@router.get('/all-users/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_id_endpoint(user_id:int, db: Session = Depends(get_db)):
    return await get_user_by_id(db, user_id)

@router.put('/update/{user_id}', response_model=User, status_code=status.HTTP_200_OK)
async def update_user_endpoint(user_id:int, user: UserUpdate, db: Session = Depends(get_db)):
    return await update_user(db, user_id, user)

@router.put('/{user_id}/deactive', response_model=UserResponse,status_code = status.HTTP_200_OK)
async def deactive_user_endpoint(user_id:int, db:Session = Depends(get_db)):
    try:
        user = await deactive_user(db, user_id)
        return {'message': 'User deactivated', 'user': user}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

