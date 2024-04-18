from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr,Field
from datetime import date, datetime


class ReservationsEnum(str,Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    cancelled = 'cancelled'



class ClientName(BaseModel):
    first_name: str
    last_name: str
    email:EmailStr   

class ReservationBase(BaseModel):
    date_reservation: Optional[date] = date(2000,1,1)
    number_of_places: int
    status: ReservationsEnum =  ReservationsEnum.pending
    client_id: int
    excursion_id: int

class ReservationWithClient(ReservationBase):
    client:ClientName


class ReservationCreate(ReservationBase):
    pass

class Reservation(ReservationBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_atributtes = True

class ReservationUpdate(ReservationBase):
    pass

