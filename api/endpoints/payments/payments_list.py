from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.get_db import get_db
from sqlalchemy.orm import Session
from schemas.payments import PaymentBase, Payment
from models.models import Payments

router = APIRouter(prefix="/payments", tags=["Payments"])


@router.get("/", response_model=list[PaymentBase], status_code=status.HTTP_200_OK)
async def get_payments_list(db: Session = Depends(get_db)):
    payments = db.query(Payments).all()
    if not payments:
        raise HTTPException(status_code=404, detail="Payments do not exist")
    return payments




