from schemas.clients import *
from sqlalchemy.orm import Session
from fastapi import status,APIRouter, Depends
from api.deps.get_db import get_db
from services.clients import *
router = APIRouter(prefix='/clients', tags=['Clients'])

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ClientCreate)
async def create_client_endpoint(client:ClientCreate, db:Session=Depends(get_db)):
    return await create_client(db, client)

@router.get('/list', response_model=list[Client],status_code=status.HTTP_200_OK)
async def get_all_client(db:Session=Depends(get_db)):
    return await get_clients(db)

@router.get('/list/{client_id}', response_model=Client, status_code=status.HTTP_200_OK)
async def get_client_by_id_endpoint(client_id:int, db:Session=Depends(get_db)):
    return await get_client_by_id(db, client_id)

@router.put('/update/{client_id}', response_model=Client, status_code=status.HTTP_200_OK)
async def update_client_endpoint(client_id:int, client:ClientUpdated, db:Session=Depends(get_db)):
    return await update_client(db, client_id, client)

@router.delete('/delete/{client_id}', status_code=status.HTTP_200_OK)
async def delete_client_endpoint(client_id:int, db:Session=Depends(get_db)):
    return await delete_client(db, client_id)


