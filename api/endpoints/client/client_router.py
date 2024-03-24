from typing import Annotated
from schemas.clients import *
from sqlalchemy.orm import Session
from fastapi import status,APIRouter, Depends
from api.deps.get_db import get_db
from schemas.users import User
from services.auth.autentication import get_current_user
from services.clients import *
router = APIRouter(prefix='/clients', tags=['Clients'])
user_dependecies = Annotated[User, Depends(get_current_user)]
@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ClientCreate)
async def create_client_endpoint(client:ClientCreate, user:user_dependecies,db:Session=Depends(get_db)):
    if user.role != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to create a client')
    return await create_client(db, client)

@router.get('/list', response_model=list[Client],status_code=status.HTTP_200_OK)
async def get_all_client(db:Session=Depends(get_db)):
    return await get_clients(db)

@router.get('/list/{client_id}', response_model=Client, status_code=status.HTTP_200_OK)
async def get_client_by_id_endpoint(client_id:int, db:Session=Depends(get_db)):
    return await get_client_by_id(db, client_id)

@router.put('/update/{client_id}', response_model=Client, status_code=status.HTTP_200_OK)
async def update_client_endpoint(client_id:int, user:user_dependecies,client:ClientUpdated, db:Session=Depends(get_db)):
    if user.role != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to update a client')
    return await update_client(db, client_id, client)

@router.delete('/delete/{client_id}', status_code=status.HTTP_200_OK)
async def delete_client_endpoint(client_id:int,user:user_dependecies, db:Session=Depends(get_db)):
    if user.role != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to delete a client')
    return await delete_client(db, client_id)


