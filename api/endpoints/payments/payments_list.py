from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from api.deps.get_db import get_db
from sqlalchemy.orm import Session
from schemas.payments import PaymentBase, Payment
from models.models import Payments
from schemas.users import User
from services.auth.autentication import get_current_user

router = APIRouter(prefix="/payments", tags=["Payments"])


user_dependecies = Annotated[User, Depends(get_current_user)]
@router.get("/", response_model=list[PaymentBase], status_code=status.HTTP_200_OK)
async def get_payments_list(user:user_dependecies,db: Session = Depends(get_db)):
    if user.role != 'agency':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to get a payments list')
    payments = db.query(Payments).all()
    if not payments:
        raise HTTPException(status_code=404, detail="Payments do not exist")
    return payments




