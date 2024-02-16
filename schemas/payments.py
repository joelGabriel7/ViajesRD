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
    status: PaymentStatus = PaymentStatus.pending
    payment_method: PaymentMethod = PaymentMethod.cash
    date_payment: Optional[date] = None
    reservation_id: int

class Payment(PaymentBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_atributtes = True