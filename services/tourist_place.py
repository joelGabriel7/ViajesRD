from schemas.tourist_place import TouristPlaceCreate, TouristPlaceUpdate,TouristPlaceSchema
from models.models import Categories, TouristPlace, TouristPlaceImage, TouristPlaceRating
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
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return new_tourist_place

async def get_all_tourist_place(db:Session):
    tourist_place = db.query(TouristPlace).options(
        joinedload(TouristPlace.category),
        joinedload(TouristPlace.images),
        joinedload(TouristPlace.ratings)
    
    ).order_by(TouristPlace.id).all()  
    return  tourist_place

async def get_tourist_place_by_id(db:Session, tourist_place_id:int):
    place_id = db.query(TouristPlace).options(joinedload(TouristPlace.category)).filter(TouristPlace.id == tourist_place_id).first()
    if place_id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found")
    return place_id

async def get_tourist_place_by_categories(db:Session, categories:int):
    category= db.query(TouristPlace).filter(TouristPlace.category_id == categories).all()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found with category")
    return category



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
    

    images_to_delete = db.query(TouristPlaceImage).filter(TouristPlaceImage.tourist_place_id == tourist_place).all()
    for image in images_to_delete:
        db.delete(image)
        
    db.delete(tourist_place_to_delete)
    db.commit()
    return {"message":"Tourist place deleted successfully"}



async def rate_tourist_place(db:Session, tourist_place_id:int, rating:int, user_id:int):
    tourist_place = await get_tourist_place_by_id(db, tourist_place_id)
    if tourist_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found")
    try:
        new_rating = TouristPlaceRating(rating=rating, tourist_place_id=tourist_place_id, user_id=user_id)
        db.add(new_rating)
        db.commit()
        db.refresh(new_rating)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return new_rating.rating


async def search_tourist_place_and_category(db:Session, search:str):
    tourist_place = db.query(TouristPlace).join(TouristPlace.category).filter((TouristPlace.name.ilike(f'%{search}%')) |(TouristPlace.location.ilike(f'%{search}%')) | (Categories.name.ilike(f'%{search}%'))).all()
    if tourist_place is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tourist place not found")
    
    return tourist_place
