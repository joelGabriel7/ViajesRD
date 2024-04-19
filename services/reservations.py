from schemas.payments import PaymentMethod, PaymentStatus
from schemas.reservations import *
from fastapi import HTTPException, status
from sqlalchemy.orm import Session,joinedload
from models.models import Excursions, Payments, ReservationDetails, Reservations
from sqlalchemy.exc import SQLAlchemyError


async def get_excursion_by_id(db: Session, excursion_id: int):
    excursion = db.query(Excursions).filter(Excursions.id == excursion_id).first()
    if excursion == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    return excursion

async def create_reservation(db: Session, request: ReservationCreate):
    excursion_ids = [detail.excursion_id for detail in request.reservations_details]
    excursions = db.query(Excursions).filter(Excursions.id.in_(excursion_ids)).all()

    if len(excursions) != len(set(excursion_ids)):
        raise HTTPException(status_code=404, detail="One or more excursions not found")

    try:
        new_reservation = Reservations(
            client_id=request.client_id,
            date_reservation=request.date_reservation,
            total_amount=0.0
        )
        db.add(new_reservation)
        db.flush()

        total_amount = 0.0
        formatted_details = []
        for detail in request.reservations_details:
            excursion = next((exc for exc in excursions if exc.id == detail.excursion_id), None)
            if not excursion or excursion.available_places < detail.quantity:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Insufficient places for excursion ID {detail.excursion_id}")

            excursion.available_places -= detail.quantity
            total_amount += detail.quantity * excursion.price

            new_detail = ReservationDetails(
                reservation_id=new_reservation.id,
                excursion_id=detail.excursion_id,
                quantity=detail.quantity,
                price=excursion.price
            )
            db.add(new_detail)
            formatted_details.append({
                "excursion_id": detail.excursion_id,
                "quantity": detail.quantity
            })

        new_reservation.total_amount = total_amount
        db.add(new_reservation)

        payments = Payments(
            reservation_id=new_reservation.id,
            amount=total_amount,
            payment_method='cash',
            status=1
        )
        db.add(payments)
        db.commit()

        reservation_order_data = {
            "date_reservation": new_reservation.date_reservation.isoformat(),   
            "client_id": new_reservation.client_id,
            "total_amount": total_amount,
            "reservations_details": formatted_details
        }
        return ReservationBase.parse_obj(reservation_order_data)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

def get_all_reservations(db: Session) -> List[ReservationSchema]:
    reservations = db.query(Reservations).options(
        joinedload(Reservations.reservation_details)  
    ).all()
    return [ReservationSchema.from_orm(res) for res in reservations]

async def get_reservation_by_id(db: Session, reservation_id: int):
    reservation = db.query(Reservations).filter(Reservations.id == reservation_id).first()
    if not reservation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reservation not found")
    return reservation 
