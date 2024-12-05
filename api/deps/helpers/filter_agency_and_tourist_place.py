from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from services.tourist_place import get_tourist_place_by_id
from services.agency import get_agency_by_id
from schemas.excursions import *

async def validate_tourist_place_exites(db:Session, excursion:ExcursionsCreate):
    tourist_place = await get_tourist_place_by_id(db,excursion.tourist_place_id)
    if not tourist_place:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found")
async def validate_agency_exites(db:Session, excursion:ExcursionsCreate):
    agency = await get_agency_by_id(db,excursion.agency_id)
    if not agency:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Agency not found")
