from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional,List
from.category import Category, CategoryBase


class TouristPlaceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    image: Optional[str] = None
    location: str= Field(min_length=1)
    category_id: int
    # category: Optional[Category] = None




class TouristPlaceCreate(TouristPlaceBase):
    pass



class TouristPlaceWithCategory(TouristPlaceBase):
    category: CategoryBase

class TouristPlace(TouristPlaceBase):   
    id: int
    created: datetime
    updated: datetime


 

    class Config:
        from_attributes = True

class TouristPlaceUpdate(TouristPlaceBase):
    pass