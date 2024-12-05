
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class AgencyBase(BaseModel):
    name: str = Field(min_length=0, max_length=20)
    address: Optional[str] = None
    phone: str
    email: EmailStr
    logo: Optional[str] = None
    rnc:str= Field( min_length=0, max_length=255)

    
class AgencyCreate(AgencyBase):
        pass

class Agency(AgencyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class AgencyUpdate(AgencyBase):
    pass


