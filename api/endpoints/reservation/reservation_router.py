from typing import Annotated
from fastapi import APIRouter, Depends, status
from api.deps.get_db import get_db
from sqlalchemy.orm import Session
from schemas.users import User
from services.auth.autentication import get_current_user
from services.reservations import *

router = APIRouter(prefix='/reservations', tags=['Reservations'])
user_dependecies = Annotated[User, Depends(get_current_user)]

@router.post('/create', response_model=ReservationBase,status_code = status.HTTP_200_OK)
async def create_reservation_endpoint(reservation: ReservationBase,db: Session = Depends(get_db)):
    return await create_reservation(db, reservation)

@router.get('/all',response_model=List[ReservationSchema], status_code = status.HTTP_200_OK)
async def get_all_reservations_endpoint(db:Session = Depends(get_db)):
    reservations =  get_all_reservations(db)
    if not reservations:
        raise HTTPException(status_code=404, detail="No reservations found")
    return reservations

@router.get('/{reservation_id}', response_model=ReservationSchema, status_code = status.HTTP_200_OK)
async def get_reservation_by_id_endpoint(reservation_id:int, db:Session = Depends(get_db)):
    return await get_reservation_by_id(db,reservation_id)

