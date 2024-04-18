from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime

from schemas.tourist_place import CategoryName, TouristPlaceImage


class ExcusionsBase(BaseModel):
    agency_id: int = Field(title="Agency ID", description="ID de la agencia que ofrece la excursión") 
    tourist_place_id: int
    date_excursion: Optional[date] = date(2000,1,1)
    duration_excursion: int = Field(title="Duration", description="Duración de la excursión en minutos")
    price: float = Field(title="Price", description="Precio de la excursión")
    description: str = Field(title="Description", description="Descripción de la excursión")
    available_places: int = Field(title="Available places", description="Número de plazas disponibles")

class ExcursionsCreate(ExcusionsBase):
    pass

class AgencyName(BaseModel):
    name: str
    email: EmailStr
 
class TouristPlaceForExcursion(BaseModel):
    name: str
    location: str
    images: Optional[list[TouristPlaceImage]] = []
    
class ExcursionWithGanancias(ExcusionsBase):
    total_ganancias: float
    agency: AgencyName
    tourist_place: TouristPlaceForExcursion

    class Config:
        # orm_mode = True
        from_attributes = True

class ExcursionsWithTouristPlaceAndAgency(ExcusionsBase):
    id: int
    agency: AgencyName
    tourist_place: TouristPlaceForExcursion
    
class Excursions(ExcusionsBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True

class ExcursionsUpdate(ExcusionsBase):
     class Config:
        # orm_mode = True
        from_attributes = True