from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from api.deps.get_db import get_db
from schemas.tourist_place import TouristPlaceCreate, TouristPlaceUpdate, TouristPlace, TouristPlaceWithCategory
from services.tourist_place import create_tourist_place, get_all_toruist_place, get_all_toruist_place_with_category, get_tourist_place_by_id, get_tourist_place_by_id_with_category, update_tourist_place, delete_tourist_place


router = APIRouter(prefix='/tourist_place', tags=['Tourist Place']) 


@router.post('/create', response_model=TouristPlace, status_code=status.HTTP_201_CREATED)
async def create_tourist_place_endpoint(tourist_place:TouristPlaceCreate, db:Session = Depends(get_db)):
    return await create_tourist_place(db, tourist_place)


@router.get('/list', response_model=list[TouristPlace], status_code=status.HTTP_200_OK)
async def tourist_place_list_endpoint(db:Session = Depends(get_db)):
    return await get_all_toruist_place(db)


@router.get('/{tourist_place_id}', response_model=TouristPlace,status_code=status.HTTP_200_OK)
async def get_tourist_place_by_id_endpoint(tourist_place_id:int, db:Session = Depends(get_db)):
    return await get_tourist_place_by_id(db,tourist_place_id)

@router.get('/places/category', response_model=list[TouristPlaceWithCategory], status_code=status.HTTP_200_OK)
async def tourist_place_list_with_category_endpoint(db:Session = Depends(get_db)):
    return await get_all_toruist_place_with_category(db)

@router.get('/places/category/{category_id}', response_model=TouristPlaceWithCategory, status_code=status.HTTP_200_OK)
async def tourist_place_list_by_category_endpoint(category_id:int, db:Session = Depends(get_db)):
    return await get_tourist_place_by_id_with_category(db, category_id)

@router.put('/update/{tourist_place_id}', response_model=TouristPlaceUpdate,status_code=status.HTTP_202_ACCEPTED)
async def update_tourist_place_endpoint(tourist_place_id:int, tourist_place_to_update:TouristPlaceUpdate, db:Session=Depends(get_db)):
    return await update_tourist_place(db,tourist_place_to_update, tourist_place_id)

@router.delete('/delete/{tourist_place_id}',status_code=status.HTTP_200_OK)
async def delete_tourist_place_endpoint(tourist_place_id:int, db:Session=Depends(get_db)):
    return await delete_tourist_place(db, tourist_place_id)