from typing import Annotated
from fastapi import Depends, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import Token
from services.auth.autentication import *
from api.deps.get_db import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix='/auth',tags=["Authentication"])
    

@router.post('/token')
async def login_for_access_token( form_data:OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)   ):
    user = authenticate_user(form_data.username,  form_data.password,db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Usuario o contraseña', headers={'WWW-Authenticate':'Bearer'})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRATION)
    access_token = create_access_token(data={'username':user.username, 'role': user.role,'id':user.id,'exp':  (datetime.now() + access_token_expires).timestamp() }, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type='bearer')