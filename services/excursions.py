from schemas.excursions import *
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from models.models import Excursions as excursions_model
from api.deps.helpers.filter_agency_and_tourist_place import validate_agency_exites, validate_tourist_place_exites
from api.deps.helpers.show_agency_and_Tplace import get_excursion_by_id_with_agency_and_tourist_place



async def create_excursion(db:Session, excursion:ExcursionsCreate):

    try:
        await validate_tourist_place_exites(db,excursion)
        await validate_agency_exites(db,excursion)    
        new_excursion = excursions_model(**excursion.model_dump())
        db.add(new_excursion)
        db.commit()
        db.refresh(new_excursion)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_excursion


async def get_all_excursions(db:Session):
    excursions =  db.query(excursions_model).all()
    if excursions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No excursions found")
    return excursions

async def get_excursion_by_id(db:Session, excursion_id:int):
    excursion =  db.query(excursions_model).filter(excursions_model.id == excursion_id).first()
    if excursion is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No excursions found")
    return excursion

async def update_excursion(db:Session, excursion_id:int, new_excursion:ExcursionsUpdate):
    try:
        excursion_update = await get_excursion_by_id(db,excursion_id) 
        for var, value in vars(new_excursion).items():
                setattr(excursion_update, var, value) if value else None

        db.commit()
        db.refresh(excursion_update)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return excursion_update

async def delete_excursion(db:Session, excursion_id:int):
    try:
        excursion_delete = await get_excursion_by_id(db,excursion_id)
        db.delete(excursion_delete)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"detail": "Excursion deleted successfully"}

async def get_excursion_by_id_with_agency_and_tourist_place(db:Session, excursion_id:int):
    return await get_excursion_by_id_with_agency_and_tourist_place(db,excursion_id)