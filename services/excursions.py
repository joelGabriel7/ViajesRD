from pydantic import ValidationError
from sqlalchemy import func
import sqlalchemy
from schemas.excursions import *
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models.models import Excursions as excursions_model, Payments, Reservations,ReservationDetails
from api.deps.helpers.filter_agency_and_tourist_place import validate_agency_exites, validate_tourist_place_exites


def calculate_total_ganancias_for_excursion(db: Session, excursion_id: int) -> float:
    total_ganancias = db.query(func.sum(Payments.amount)).join(ReservationDetails, Payments.reservation_id == ReservationDetails.id).filter(ReservationDetails.excursion_id == excursion_id).scalar() or 0.0
    return total_ganancias

async def create_excursion(db:Session, excursion:ExcursionsCreate):

    try:
        await validate_tourist_place_exites(db,excursion)
        await validate_agency_exites(db,excursion)    
        new_excursion = excursions_model(**excursion.model_dump())
        db.add(new_excursion)
        db.commit()
        db.refresh(new_excursion)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_excursion


async def get_all_excursions(db:Session):
    excursions =  db.query(excursions_model).options(joinedload(excursions_model.tourist_place), joinedload(excursions_model.agency)).all()
    if excursions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No excursions found")
    return excursions

async def get_excursion_to_delete(db:Session,excursion_id:int):
    excursion = db.query(excursions_model).filter(excursions_model.id == excursion_id).options(joinedload(excursions_model.tourist_place), joinedload(excursions_model.agency)).first()
    if not excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    return excursion

async def get_excursion_by_id(db: Session, excursion_id: int):
    excursion = db.query(excursions_model).filter(excursions_model.id == excursion_id).options(joinedload(excursions_model.tourist_place), joinedload(excursions_model.agency)).first()
    if not excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    agency = excursion.agency
    total_ganancias = calculate_total_ganancias_for_excursion(db, excursion_id)
    places = excursion.tourist_place
    data_tourist_place = {
        "name": places.name,
        "location": places.location,
        "images": places.images
    }
    tourist_place_instance = TouristPlaceForExcursion(**data_tourist_place)
    agency_dict = {c.key: getattr(agency, c.key) for c in sqlalchemy.inspect(agency).mapper.column_attrs}
    agency_instance = AgencyName(**agency_dict)
    excursion_data = ExcursionWithGanancias(
        **{**excursion.__dict__, "total_ganancias": total_ganancias, "agency": agency_instance, "tourist_place": tourist_place_instance}
    )
    return excursion_data

async def update_excursion(db: Session, excursion_id: int, excursion_data: ExcursionsUpdate):
    
    excursion = db.query(excursions_model).filter(excursions_model.id == excursion_id).first() 
    if not excursion or validate_tourist_place_exites(db,excursion_data):
        raise HTTPException(status_code=404, detail="Excursion not found or Tourist place not found")

    update_data = excursion_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(excursion, key, value)

    db.commit()
    db.refresh(excursion)

    # Si necesitas devolver un modelo Pydantic actualizado aquí, debes hacerlo después de actualizar el ORM
    return ExcursionsUpdate.from_orm(excursion)


async def delete_excursion(db:Session, excursion_id:int):
    try:
        excursion_delete = await get_excursion_to_delete(db,excursion_id)
        db.delete(excursion_delete)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return {"detail": "Excursion deleted successfully"}
