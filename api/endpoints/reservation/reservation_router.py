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

@router.get('/', response_model=list[Reservation], status_code = status.HTTP_200_OK)
async def get_reservations_by_limit_endpoint(skip:int = 0, limit: int=10, db:Session = Depends(get_db)):
    return await get_reservations_by_limit(db,skip,limit)

@router.put('/{reservation_id}', response_model=ReservationUpdate, status_code = status.HTTP_200_OK)
async def update_reservation_endpoint(reservation_id:int, reservationUpdate:ReservationUpdate, db:Session = Depends(get_db)):
    return await update_reservations(db,reservation_id, reservationUpdate)

@router.delete('/{reservation_id}', status_code = status.HTTP_200_OK)
async def delete_reservation_endpoint(reservation_id:int,db:Session = Depends(get_db)):
    return await delete_reservation(db,reservation_id)


@router.post("/{reservation_id}/confirm", status_code = status.HTTP_200_OK)
async def confirm_reservation_endpoint(reservation_id:int, db:Session = Depends(get_db)):
    return await confirm_reservation_and_initiate_payment(reservation_id,db)