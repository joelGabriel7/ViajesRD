from schemas.tourist_place import TouristPlaceCreate, TouristPlaceUpdate,TouristPlace
from models.models import TouristPlace
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import class_mapper

def asdict(obj):
    return {c.key: getattr(obj, c.key)
            for c in class_mapper(obj.__class__).columns}


async def create_tourist_place(db:Session, tourist_place:TouristPlaceCreate):
    exitisting_tourist_place = db.query(TouristPlace).filter(
        TouristPlace.name == tourist_place.name,
        TouristPlace.category_id == tourist_place.category_id
        ).first()
    if exitisting_tourist_place:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Tourist place already exists in this category')
    try:
        new_tourist_place = TouristPlace(**tourist_place.model_dump())
        db.add(new_tourist_place)
        db.commit()
        db.refresh(new_tourist_place)
        db.commit()
        # new_tourist_place = db.query(TouristPlace).options(joinedload(TouristPlace.category)).filter(TouristPlace.id == new_tourist_place.id).first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return new_tourist_place

async def get_all_toruist_place(db:Session):
    return db.query(TouristPlace).options(joinedload(TouristPlace.category)).all()

async def get_tourist_place_by_id(db:Session, tourist_place_id:int):
    place_id = db.query(TouristPlace).options(joinedload(TouristPlace.category)).filter(TouristPlace.id == tourist_place_id).first()
    if place_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found")
    return place_id

async def update_tourist_place(db:Session,  tourist_place: TouristPlaceUpdate, tourist_place_id:int):
    tourist_place_to_update = await get_tourist_place_by_id(db, tourist_place_id)
    if tourist_place_to_update is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found")
    for var, value in vars(tourist_place).items():
        setattr(tourist_place_to_update, var, value) if value else None
    db.commit()
    db.refresh(tourist_place_to_update)
    return  asdict(tourist_place_to_update)


async def delete_tourist_place(db:Session, tourist_place:int):
    tourist_place_to_delete = await get_tourist_place_by_id(db, tourist_place)
    if tourist_place_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Tourist place not found')
    db.delete(tourist_place_to_delete)
    db.commit()
    return {"message":"Tourist place deleted successfully"}


async def get_all_toruist_place_with_category(db:Session):
    return db.query(TouristPlace).options(joinedload(TouristPlace.category)).all()

async def get_tourist_place_by_id_with_category(db:Session, tourist_place_id:int):
    place_id = db.query(TouristPlace).options(joinedload(TouristPlace.category)).filter(TouristPlace.id == tourist_place_id).first()
    if place_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found")
    return place_id

