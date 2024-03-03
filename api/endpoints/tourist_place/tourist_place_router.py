from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.deps.get_db import get_db
from schemas.tourist_place import TouristPlaceCreate,TouristPlaceUpdate, TouristPlace, TouristPlaceWithCategory, TouristPlaceImage as image_schema
from services.tourist_place import create_tourist_place, get_all_tourist_place, get_tourist_place_by_categories, get_tourist_place_by_id,  update_tourist_place, delete_tourist_place
import os

from models.models import TouristPlaceImage

router = APIRouter(prefix='/tourist_place', tags=['Tourist Place']) 


@router.post('/create', response_model=TouristPlace, status_code=status.HTTP_201_CREATED)
async def create_tourist_place_endpoint(tourist_place:TouristPlaceCreate, db:Session = Depends(get_db)):
    return await create_tourist_place(db, tourist_place)

@router.get('/list', response_model=list[TouristPlaceWithCategory], status_code=status.HTTP_200_OK)
async def tourist_place_list_endpoint(db:Session = Depends(get_db)):
    return await  get_all_tourist_place(db)

@router.get('/{tourist_place_id}', response_model=TouristPlaceWithCategory,status_code=status.HTTP_200_OK)
async def get_tourist_place_by_id_endpoint(tourist_place_id:int, db:Session = Depends(get_db)):
    return await get_tourist_place_by_id(db,tourist_place_id)

@router.get('/{categories}/tourist_places', response_model=list[TouristPlaceWithCategory],status_code=status.HTTP_200_OK)
async def get_tourist_place_by_category_endpoint(categories:int, db:Session = Depends(get_db)):
    return await get_tourist_place_by_categories(db,categories)

@router.put('/update/{tourist_place_id}', response_model=TouristPlaceUpdate,status_code=status.HTTP_202_ACCEPTED)
async def update_tourist_place_endpoint(tourist_place_id:int, tourist_place_to_update:TouristPlaceUpdate, db:Session=Depends(get_db)):
    return await update_tourist_place(db,tourist_place_to_update, tourist_place_id)

@router.delete('/delete/{tourist_place_id}',status_code=status.HTTP_200_OK)
async def delete_tourist_place_endpoint(tourist_place_id:int, db:Session=Depends(get_db)):
    return await delete_tourist_place(db, tourist_place_id)


# Upload Images

@router.post("/tourist-places/{tourist_place_id}/images/")
async def upload_images(tourist_place_id: int, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    files_urls = []
    for file in files:
        try:
            os.makedirs('static', exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            filename = f"{timestamp}_{file.filename}"

            file_path = f'static/{filename}'


            with open(file_path, "wb") as file_object:
                file_object.write(file.file.read())
                await file.close()
            files_urls.append(file_path)

        except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))  

    new_images = []
    for url in files_urls:
        new_image = TouristPlaceImage(image_url = url, tourist_place_id = tourist_place_id)
        db.add(new_image)
        new_images.append(new_image)
    db.commit()
    images_data = [image_schema.from_orm(image).model_dump() for image in new_images]
    return {"images": images_data}

    
    
