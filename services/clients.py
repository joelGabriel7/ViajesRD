from fastapi import HTTPException, status
from schemas.clients import *
from models.models import Clients
from sqlalchemy.orm import Session

from schemas.users import UserCreate
from .users import create_user


async def create_client(db:Session, client:ClientCreate):
    client_exists = db.query(Clients).filter(Clients.email == client.email).first()
    if client_exists is  None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    new_client= Clients(**client.model_dump())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client

async def get_clients(db:Session):
    clients = db.query(Clients).all()
    if clients is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No clients found")
    return clients

async def get_client_by_id(db:Session, client_id:int):
    client  = db.query(Clients).filter(Clients.id == client_id).first()
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client

async def update_client(db:Session, client_id:int, client:ClientUpdated):
    client_update = await get_client_by_id(db, client_id)    
    for key, value in vars(client).items(): 
        if value:
            setattr(client_update, key, value)
        else:
             return None
    db.commit()
    db.refresh(client_update)
    return client_update

async def delete_client(db:Session,  client_id):
    client = await get_client_by_id(db, client_id)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    db.delete(client)
    db.commit()
    return {"message":"Client deleted successfully"}

