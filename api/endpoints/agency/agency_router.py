from typing import Annotated
from fastapi import APIRouter,Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.users import User
from services.agency import create_agency, delete_agency, get_agencie_by_rnc, get_all_agencies, get_agency_by_id, get_ten_agencies, update_agency
from data.db import *
from schemas.agency import AgencyUpdate,AgencyCreate, Agency
from api.deps.get_db import get_db
from services.auth.autentication import get_current_user


router = APIRouter(prefix='/agencies',tags=["Agency"])
user_dependecies = Annotated[User, Depends(get_current_user)]

@router.post("/create", response_model=AgencyCreate, status_code=201)
async def create_agency_endpoint(agency: AgencyCreate,db: Session = Depends(get_db)):
    return await create_agency(db, agency)

@router.get("/list", response_model=list[Agency], status_code=200)
async def get_all_agencies_endpoint(db: Session = Depends(get_db)):
    return await get_all_agencies(db)

@router.get("/list/ten", response_model=list[Agency], status_code=200)
async def get_ten_agencies_endpoint(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return await get_ten_agencies(db, skip, limit)

@router.get("/{agency_id}", response_model=Agency, status_code=200)
async def get_agency_by_id_endpoint(agency_id: int, db: Session = Depends(get_db)):
    return await get_agency_by_id(db, agency_id)

@router.get("/rnc/{rnc}", response_model=Agency, status_code=200)
async def get_agencie_by_rnc_endpoint(rnc:str, db:Session = Depends(get_db)):
    return await get_agencie_by_rnc(db, rnc)

@router.put("/{agency_id}", response_model=AgencyUpdate, status_code=200)
async def update_agency_endpoint(agency_id: int, agency: AgencyUpdate, user:user_dependecies,db: Session = Depends(get_db)):
    if user.role != 'agency':
        raise HTTPException(status_code=401, detail='You do not have permission to update an agency')
    return await update_agency(db, agency_id, agency)

@router.delete("/{agency_id}", status_code=200)
async def delete_agency_endpoint(agency_id: int, user:user_dependecies,db: Session = Depends(get_db)):
    if user.role != 'agency':
        raise HTTPException(status_code=401, detail='You do not have permission to delete an agency')
    return await delete_agency(db, agency_id)
