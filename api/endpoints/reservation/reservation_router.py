from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.deps.get_db import get_db
from sqlalchemy.orm import Session
from schemas.users import User
from services.auth.autentication import get_current_user
from services.reservations import *
from models.models import Excursions

router = APIRouter(prefix='/reservations', tags=['Reservations'])
user_dependecies = Annotated[User, Depends(get_current_user)]

@router.post('/create', response_model=ReservationCreate,status_code = status.HTTP_200_OK)
async def create_reservation_endpoint(reservation: ReservationBase,db: Session = Depends(get_db)):
    return await create_reservation(db, reservation)

@router.get('/all', response_model=list[Reservation], status_code = status.HTTP_200_OK)
async def get_all_reservations_endpoint(db:Session = Depends(get_db)):
    return await get_all_reservations(db)

@router.get('/{reservation_id}', response_model=ReservationWithClient, status_code = status.HTTP_200_OK)
async def get_reservation_by_id_endpoint(reservation_id:int, db:Session = Depends(get_db)):
    return await get_reservation_by_id(db,reservation_id)

@router.get('/excursion/{excursion_id}', response_model=list[ReservationWithClient], status_code = status.HTTP_200_OK)
async def get_reservations_by_excursion_id_endpoint(excursion_id:int, db:Session = Depends(get_db)):
    return await get_reservations_by_excursion_id(db,excursion_id)

@router.get('/', response_model=list[Reservation], status_code = status.HTTP_200_OK)
async def get_reservations_by_limit_endpoint(skip:int = 0, limit: int=10, db:Session = Depends(get_db)):
    return await get_reservations_by_limit(db,skip,limit)

@router.put('/{reservation_id}', response_model=ReservationUpdate, status_code = status.HTTP_200_OK)
async def update_reservation_endpoint(reservation_id:int, reservationUpdate:ReservationUpdate, user:user_dependecies,db:Session = Depends(get_db)):
    if user.role != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to update a reservation')
    return await update_reservations(db,reservation_id, reservationUpdate)

@router.delete('/{reservation_id}', status_code = status.HTTP_200_OK)
async def delete_reservation_endpoint(reservation_id:int,user:user_dependecies,db:Session = Depends(get_db)):
    if user.role != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to delete a reservation')
    return await delete_reservation(db,reservation_id)


@router.post("/{reservation_id}/confirm", status_code = status.HTTP_200_OK)
async def confirm_reservation_endpoint(reservation_id:int, user:user_dependecies,db:Session = Depends(get_db)):
    if user.role != 'client':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to confirm a reservation')
    return await confirm_reservation_and_initiate_payment(reservation_id,db)