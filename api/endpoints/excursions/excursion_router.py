from pytest import Session
from schemas.excursions import *
from fastapi import Depends, status, APIRouter
from api.deps.get_db import get_db
from services.excursions import create_excursion, delete_excursion, get_all_excursions, get_excursion_by_id, update_excursion


excursion_router = APIRouter(prefix="/excursions", tags=["Excursions"])

@excursion_router.post("/create", response_model=ExcursionsCreate, status_code=status.HTTP_201_CREATED)
async def create_excursion_endpoint(excursion:ExcursionsCreate, db:Session = Depends(get_db)):
    return await create_excursion(db,excursion)

@excursion_router.get("/list", response_model=list[ExcursionsWithTouristPlaceAndAgency], status_code=status.HTTP_200_OK)
async def get_all_excursions_endpoint(db:Session = Depends(get_db)):
    return await get_all_excursions(db)

@excursion_router.get("/list/{excursion_id}", response_model=ExcursionWithGanancias, status_code=status.HTTP_200_OK)
async def get_excursion_by_id_endpoint(excursion_id:int, db:Session = Depends(get_db)):
    return await get_excursion_by_id(db,excursion_id)

@excursion_router.put("/update/{excursion_id}", response_model=ExcursionsUpdate, status_code=status.HTTP_200_OK)
async def update_excursion_endpoint(excursion_id:int, new_excursion:ExcursionsUpdate, db:Session = Depends(get_db)):
    return await update_excursion(db,excursion_id,new_excursion)

@excursion_router.delete("/delete/{excursion_id}", status_code=status.HTTP_200_OK)
async def delete_excursion_endpoint(excursion_id:int, db:Session = Depends(get_db)):
    return await delete_excursion(db,excursion_id)

