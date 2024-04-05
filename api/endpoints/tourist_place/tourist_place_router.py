from datetime import datetime
from typing import Annotated, List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.deps.get_db import get_db
from schemas.tourist_place import TouristPlaceCreate,TouristPlaceUpdate, TouristPlace, TouristPlaceWithCategory, TouristPlaceImage as image_schema
from schemas.users import User
from services.auth.autentication import get_current_user
from services.tourist_place import create_tourist_place, get_all_tourist_place, get_tourist_place_by_categories, get_tourist_place_by_id, rate_tourist_place,  update_tourist_place, delete_tourist_place
import os

from models.models import TouristPlaceImage

router = APIRouter(prefix='/tourist_place', tags=['Tourist Place']) 
user_dependecies = Annotated[User, Depends(get_current_user)]

@router.post('/create', response_model=TouristPlace, status_code=status.HTTP_201_CREATED)
async def create_tourist_place_endpoint(tourist_place:TouristPlaceCreate, user:user_dependecies,db:Session = Depends(get_db)):
    if user.role != 'agency':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to create a tourist place')
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
async def update_tourist_place_endpoint(tourist_place_id:int, tourist_place_to_update:TouristPlaceUpdate,user:user_dependecies, db:Session=Depends(get_db)):
    if user.role != 'agency':   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to update a tourist place')
    return await update_tourist_place(db,tourist_place_to_update, tourist_place_id)

@router.delete('/delete/{tourist_place_id}',status_code=status.HTTP_200_OK)
async def delete_tourist_place_endpoint(tourist_place_id:int, user:user_dependecies,db:Session=Depends(get_db)):
    if user.role != 'agency':   
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to delete a tourist place')
    return await delete_tourist_place(db, tourist_place_id)


# Upload Images

@router.post("/{tourist_place_id}/images/")
async def upload_images(tourist_place_id: int,user:user_dependecies, files: List[UploadFile] = File(...), db: Session = Depends(get_db)):
    if user.role != 'agency':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to upload a image')
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

@router.delete("/images/{image_id}/")
async def delete_image(image_id: int, user:user_dependecies,db: Session = Depends(get_db)):
    if user.role != 'agency':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You do not have permission to delete a image')
    image_to_delete = db.query(TouristPlaceImage).filter(TouristPlaceImage.id == image_id).first()
    if not image_to_delete:
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        if os.path.exists(image_to_delete.image_url):
            os.remove(image_to_delete.image_url)

        db.delete(image_to_delete)
        db.commit()
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post('/rate/{tourist_place_id}/{rating}', status_code=status.HTTP_201_CREATED)
async def rate_tourist_place_endpoint(tourist_place_id:int, rating:int, user:user_dependecies, db:Session = Depends(get_db)):
    return await rate_tourist_place(db, tourist_place_id, rating, user.id)

    
    
    
