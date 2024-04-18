from schemas.payments import PaymentMethod, PaymentStatus
from schemas.reservations import *
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.models import Excursions, Payments, Reservations
from sqlalchemy.exc import SQLAlchemyError


async def get_excursion_by_id(db: Session, excursion_id: int):
    excursion = db.query(Excursions).filter(Excursions.id == excursion_id).first()
    if excursion == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    return excursion

async def create_reservation(db: Session, request: ReservationCreate):
    excursion = db.query(Excursions).filter(Excursions.id == request.excursion_id).first()
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")

    if request.number_of_places < 1:
        raise HTTPException(status_code=400, detail="The number of places must be greater than 0")

    if excursion.available_places < request.number_of_places:
        raise HTTPException(status_code=400, detail="Not enough available places")

    try:
        # Create and save the reservation
        new_reservation = Reservations(
            date_reservation=request.date_reservation,
            number_of_places=request.number_of_places,
            status='pending',  # Make sure your enum accepts this string directly
            client_id=request.client_id,
            excursion_id=request.excursion_id
        )
        db.add(new_reservation)
        excursion.available_places -= request.number_of_places
        db.commit()
        db.refresh(new_reservation)

        # Create payment
        new_payment = Payments(
            amount=request.number_of_places * excursion.price,
            status='pending',
            reservation_id=new_reservation.id
        )
        db.add(new_payment)
        db.commit()
        db.refresh(new_payment)
        print(f'New reservation: {new_reservation.excursion}')
        return new_reservation
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


async def get_all_reservations(db: Session):
    return db.query(Reservations).all()

async def get_reservation_by_id(db: Session, reservation_id: int):
    reservation = db.query(Reservations).filter(Reservations.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return reservation 

async def get_reservations_by_excursion_id(db: Session, excursion_id: int):
    reservations = db.query(Reservations).filter(Reservations.excursion_id == excursion_id).all()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservations not found")
    return reservations

async def get_reservations_by_limit(db: Session, skip:int = 0, limit: int=10):
    reservations = db.query(Reservations).offset(skip).limit(limit).all()
    if not reservations:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservations not found")
    return reservations

async def update_reservations (db:Session,reservation_id:int,  reservationUpdate:ReservationUpdate):
    reservation = await get_reservation_by_id(db,reservation_id)
    for key, value in vars(reservationUpdate).items(): 
        if value:
            setattr(reservation, key, value)
        else:
            return None
    db.commit()
    db.refresh(reservation)
    return reservation

async def delete_reservation(db:Session, reservation_id:int):
    reservation = await get_reservation_by_id(db,reservation_id)
    db.delete(reservation)
    db.commit()
    return {'Reservation deleted':reservation}


async def confirm_reservation_and_initiate_payment(reservation_id:int, db:Session):
    reservation = await get_reservation_by_id(db,reservation_id)
    amount = reservation.number_of_places * reservation.excursion.price
    x = reservation.excursion.tourist_place.name
    print(x)
    
    new_payment = Payments(
            amount=amount, 
            reservation_id=reservation_id,
            status = 'pending'
          )
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment
