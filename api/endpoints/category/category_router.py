from services.category import * 
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from api.deps.get_db import get_db
from schemas.category import CategoryCreate, CategoryUpdate, Category

router = APIRouter(prefix="/category", tags=["Category"])

@router.post("/create", response_model=CategoryCreate, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(cateogry:CategoryCreate, db:Session=Depends(get_db)):
    return await create_category(db, cateogry)
    

@router.get("/list", response_model=list[Category], status_code=status.HTTP_200_OK)
async def get_all_categories_endpoint(db:Session = Depends(get_db)):
    return await get_all_categories(db)


@router.get("/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
async def get_Category_by_id_endpoint(category_id: int, db:Session = Depends(get_db)):
    return await get_categories_by_id(db, category_id)

@router.put("/{category_id}", response_model=CategoryUpdate, status_code=status.HTTP_200_OK)
async def update_category_endpoint(category_id: int, category: CategoryUpdate, db:Session = Depends(get_db)):
    return await update_category(db, category_id, category)

@router.delete("/{category_id}", status_code=status.HTTP_200_OK)       
async def delete_category_endpoint(category_id: int, db:Session = Depends(get_db)): 
    return await delete_category(db, category_id)
