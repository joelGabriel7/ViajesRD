from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import date, datetime
from schemas.agency import AgencyBase, AgencyCreate

from schemas.tourist_place import TouristPlaceBase, TouristPlaceCreate


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
    legal_registration_number:str= Field( min_length=0, max_length=255)
    license_number: str = Field(min_length=0, max_length=255)

class TouristPlaceName(BaseModel):
    name: str
    code_category: str
    

class ExcursionsWithTouristPlaceAndAgency(ExcusionsBase):
    agency: AgencyName
    tourist_place: TouristPlaceName
    
class Excursions(ExcusionsBase):
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_attributes = True


class ExcursionsUpdate(ExcusionsBase):
    pass