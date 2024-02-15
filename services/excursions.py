from pydantic import ValidationError
from sqlalchemy import func
import sqlalchemy
from schemas.excursions import *
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from models.models import Excursions as excursions_model, Payments, Reservations
from api.deps.helpers.filter_agency_and_tourist_place import validate_agency_exites, validate_tourist_place_exites


def calculate_total_ganancias_for_excursion(db: Session, excursion_id: int) -> float:
    total_ganancias = db.query(func.sum(Payments.amount)).join(Reservations, Payments.reservation_id == Reservations.id).filter(Reservations.excursion_id == excursion_id).scalar() or 0.0
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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_excursion


async def get_all_excursions(db:Session):
    excursions =  db.query(excursions_model).options(joinedload(excursions_model.tourist_place), joinedload(excursions_model.agency)).all()
    if excursions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No excursions found")
    return excursions

async def get_excursion(db:Session,excursion_id:int):
    excursion = db.query(excursions_model).filter(excursions_model.id == excursion_id).options(joinedload(excursions_model.tourist_place), joinedload(excursions_model.agency)).first()
    if not excursion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Excursion not found")
    return excursion


async def get_excursion_by_id(db: Session, excursion_id: int):

    excursion = await get_excursion(db,excursion_id)
    agency = excursion.agency


    # Calcula el total de ganancias para esta excursión
    total_ganancias = calculate_total_ganancias_for_excursion(db, excursion_id)
    agency_dict = {c.key: getattr(agency, c.key) for c in sqlalchemy.inspect(agency).mapper.column_attrs}

    # Crea una instancia de AgencyName con los datos de la agencia
    agency_name = AgencyName(**agency_dict)

    excursion_data = create_excursion_data(excursion, total_ganancias, agency=agency_name)

    return excursion_data

def create_excursion_data(excursion: excursions_model, total_ganancias: float, agency:AgencyName) -> ExcursionWithGanancias:
    try:
        # Asegúrate de incluir manualmente total_ganancias en el dictado para la creación del modelo Pydantic
        excursion_dict = excursion.__dict__
        excursion_dict.update({"total_ganancias": total_ganancias, "agency": agency})
        excursion_data = ExcursionWithGanancias(**excursion_dict)
    except ValidationError as e:
        # Manejar posibles errores de validación
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return excursion_data


async def update_excursion(db: Session, excursion_id: int, excursion_data: ExcursionsUpdate):
    # Obtener el objeto de excursión directamente como un objeto ORM
    excursion = db.query(excursions_model).filter(excursions_model.id == excursion_id).first()
    if not excursion:
        raise HTTPException(status_code=404, detail="Excursion not found")

    # Actualizar los campos con los datos proporcionados
    update_data = excursion_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(excursion, key, value)

    db.commit()
    db.refresh(excursion)

    # Si necesitas devolver un modelo Pydantic actualizado aquí, debes hacerlo después de actualizar el ORM
    return ExcursionsUpdate.from_orm(excursion)


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