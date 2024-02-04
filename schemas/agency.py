
from pydantic import BaseModel, EmailStr,Optional,Field
from datetime import datetime

class AgencyBase(BaseModel):
    name: Field(str, min_length=0, max_length=20)
    address: Optional[str] = None
    phone: str
    email: EmailStr
    logo: Optional[str] = None
    certications: str
    legal_registration_number: Field(str, min_length=0, max_length=255)
    insurance_number: Field(str, min_length=0, max_length=255)
    insurance_provider: str
    legal_contact_name: str

    
class AgencyCreate(AgencyBase):
        pass

class Agency(AgencyBase):
    id: int
    license_expiration_date: datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class AgencyUpdate(AgencyBase):
    pass


