from typing import Optional
from pydantic import BaseModel, Field
from datetime import date, datetime
from enum import Enum

class PaymentStatus(str, Enum):
    pending = 'pending'
    confirmed = 'confirmed'
    cancelled = 'cancelled'

class PaymentMethod(str, Enum):
    cash = 'cash'
    credit_card = 'credit'
    debit_card = 'debit'


class PaymentBase(BaseModel):
    amount: float
    status: int
    payment_method: PaymentMethod = PaymentMethod.cash
    payment_date: Optional[date] = date(2000,1,1)
    reservation_id: int

class Payment(PaymentBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_atributtes = True