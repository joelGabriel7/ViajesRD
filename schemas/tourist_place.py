from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional



class TouristPlaceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    image: Optional[str] = None
    location: str= Field(min_length=1)
    category_id: int

class TouristPlaceCreate(TouristPlaceBase):
    pass


class CategoryName(BaseModel):
    name: str
    code_category: str

class TouristPlaceWithCategory(TouristPlaceBase):
    id:int
    category: CategoryName

class TouristPlace(TouristPlaceBase):   
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

class TouristPlaceUpdate(TouristPlaceBase):
    pass