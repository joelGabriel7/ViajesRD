from enum import Enum
from typing import Optional,List
from pydantic import BaseModel, EmailStr,Field
from datetime import date, datetime



class ReservationDetailsSchema(BaseModel):
    excursion_id: int
    quantity: int

    class Config:
        from_attributes = True
    

class ReservationBase(BaseModel):
    date_reservation: Optional[date] = date(2000,1,1)
    client_id: int
    reservations_details: list[ReservationDetailsSchema]

    class Config:
        from_attributes = True

class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True
class ReservationUpdate(ReservationBase):
    pass


class ReservationDetailSchema(BaseModel):
    excursion_id: int
    quantity: int
    price: float

    class Config:
        from_attributes = True

class ReservationSchema(BaseModel):
    id: int
    date_reservation: datetime
    total_amount: float
    reservation_details: List[ReservationDetailSchema]

    class Config:
        from_attributes = True

