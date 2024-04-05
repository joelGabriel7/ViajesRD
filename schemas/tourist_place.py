from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional



class TouristPlaceImage(BaseModel):
    id: int
    image_url: str

    class Config:
        from_attributes = True


class TouristPlaceBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    location: str= Field(min_length=1)
    category_id: int

class TouristPlaceCreate(TouristPlaceBase):
    pass


class CategoryName(BaseModel):
    name: str
    code_category: str

class TouristPlaceRating(BaseModel):
    rating: float



class TouristPlaceWithCategory(TouristPlaceBase):
    id:int
    category: CategoryName
    images: Optional[list[TouristPlaceImage]] = []
    ratings: Optional[List[TouristPlaceRating]] = None

    @property
    def average_rating(self) -> float:
        if self.ratings:
            return sum(rating.rating for rating in self.ratings) / len(self.ratings)
        else:
            return 0.0

class TouristPlace(TouristPlaceBase):   
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

class TouristPlaceUpdate(TouristPlaceBase):
    pass