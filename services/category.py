from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.models  import Categories
from schemas.category import CategoryCreate, CategoryUpdate


async def create_category(db: Session, category: CategoryCreate):
    category_exist = db.query(Categories).filter(Categories.code_category == category.code_category).first()
    if category_exist:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists with this code")
    new_category = Categories(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

async def get_all_categories(db:Session):
    categories = db.query(Categories).order_by(Categories.id).all()
    if categories is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Do not have any category")
    return  categories

async def get_categories_by_id(db:Session, category_id: int):
    category = db.query(Categories).filter(Categories.id == category_id).first()
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category

async def update_category(db:Session, category_id: int, category: CategoryUpdate):
    category_exist = db.query(Categories).filter(Categories.id == category_id).first()
    if category_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    category_exist.name = category.name
    category_exist.description = category.description
    db.commit()
    db.refresh(category_exist)
    return category_exist

async def delete_category(db:Session, category_id: int):
    category_exist = db.query(Categories).filter(Categories.id == category_id).first()
    if category_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(category_exist)
    db.commit()
    return category_exist

