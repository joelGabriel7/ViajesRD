from sqlalchemy.orm import Session
from models.models  import Agencies
from fastapi import HTTPException, status
from schemas.users import *
from schemas.agency import AgencyCreate, AgencyUpdate


async def create_agency(db:Session ,agency: AgencyCreate):
    agency_exist=db.query(Agencies).filter(Agencies.rnc==agency.rnc).first()
    if agency_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Agency already exist with this legal registration number")
    new_agency= Agencies(**agency.model_dump())
    db.add(new_agency)
    db.commit()
    db.refresh(new_agency)
    return new_agency    

async def get_all_agencies(db:Session):
    agencies = db.query(Agencies).all()
    if agencies is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Do not have any agency")
    return  agencies 

async def get_ten_agencies(db:Session , skip: int = 0, limit: int = 10):
    agencies =  db.query(Agencies).offset(skip).limit(limit).all()
    if agencies is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Do not have any agency")
    return agencies 

async def get_agency_by_id(db:Session, agency_id:int):
    agency =  db.query(Agencies).filter(Agencies.id==agency_id).first()
    if agency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    return agency

async def update_agency(db:Session, agency_id:int, agency: AgencyUpdate):
    agency_to_update = await get_agency_by_id(db, agency_id)
    if agency_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    for var, value in vars(agency).items():
       setattr(agency_to_update, var, value) if value else None
    db.commit()
    db.refresh(agency_to_update)
    return agency_to_update

async def delete_agency(db:Session, agency_id:int):
    agency_to_delete = await get_agency_by_id(db, agency_id)
    if agency_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
    db.delete(agency_to_delete)
    db.commit()
    return {"message":"Agency deleted successfully"}


