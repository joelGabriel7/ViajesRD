from fastapi import APIRouter, Depends, status
from api.deps.get_db import get_db
from sqlalchemy.orm import Session
from services.reservations import *
from models.models import Excursions

router = APIRouter(prefix='/reservations', tags=['Reservations'])

@router.post('/create', response_model=ReservationCreate,status_code = status.HTTP_200_OK)
async def create_reservation_endpoint(reservation: ReservationBase, db: Session = Depends(get_db)):
    return await create_reservation(db, reservation, Excursions)

@router.get('/all', response_model=list[ReservationBase], status_code = status.HTTP_200_OK)
async def get_all_reservations_endpoint(db:Session = Depends(get_db)):
    return await get_all_reservations(db)

@router.get('/{reservation_id}', response_model=ReservationWithClient, status_code = status.HTTP_200_OK)
async def get_reservation_by_id_endpoint(reservation_id:int, db:Session = Depends(get_db)):
    return await get_reservation_by_id(db,reservation_id)

@router.get('/client/{client_id}', response_model=list[ReservationWithClient], status_code = status.HTTP_200_OK)
async def get_reservations_by_client_id_endpoint(client_id:int, db:Session = Depends(get_db)):
    return await get_reservations_by_client_id(db,client_id)

@router.get('/', response_model=list[ReservationBase], status_code = status.HTTP_200_OK)
async def get_reservations_by_limit_endpoint(skip:int = 0, limit: int=10, db:Session = Depends(get_db)):
    return await get_reservations_by_limit(db,skip,limit)