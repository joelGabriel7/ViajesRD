from schemas.clients import *
from models.models import Clients
from sqlalchemy.orm import Session
from fastapi import HTTPException, status,APIRouter, Depends
from api.deps.get_db import get_db
from services.clients import *
router = APIRouter(prefix='/clients', tags=['Clients'])

@router.post('/create', status_code=status.HTTP_201_CREATED, response_model=ClientCreate)
async def create_client_endpoint(client:ClientCreate, db:Session=Depends(get_db)):
    return await create_client(db, client)

@router.get('/list', response_model=list[Client],status_code=status.HTTP_200_OK)
async def get_all_client(skip:int=0, limit:int=10, db:Session=Depends(get_db)):
    return await get_clients(db, skip, limit)
