from schemas.reservations import *
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.models import Excursions, Reservations


async def get_excursion_by_id(db: Session, excursion_id: int):
    excursion = db.query(Excursions).filter(Excursions.id == excursion_id).first()
    if excursion == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    return excursion



async def create_reservation(db: Session, request: ReservationCreate, excursion: Excursions):
    excursion= await get_excursion_by_id(db, request.excursion_id)
    
    if request.number_of_places < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The number of places must be greater than 0")
    
    if excursion.available_places < request.number_of_places:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not enough available places in the excursion")
    
    new_reservation = Reservations(**request.model_dump())
    excursion.available_places -= request.number_of_places
    
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    db.commit()
    return new_reservation


async def get_all_reservations(db: Session):
    return db.query(Reservations).all()

async def get_reservation_by_id(db: Session, reservation_id: int):
    reservation = db.query(Reservations).filter(Reservations.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return reservation 

async def get_reservations_by_client_id(db: Session, client_id: int):
    reservations = db.query(Reservations).filter(Reservations.client_id == client_id).all()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservations not found")
    return reservations

async def get_reservations_by_limit(db: Session, skip:int = 0, limit: int=10):
    reservations = db.query(Reservations).offset(skip).limit(limit).all()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservations not found")
    return reservations