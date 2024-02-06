from pydantic import BaseModel,Field, EmailStr, Enum,validator
from datetime import datetime

class Gender(str, Enum):
    M = 'M'
    F = 'F'

class ClientBase(BaseModel):
    first_name : str =  Field(max_length=50)
    last_name : str =Field(max_length=75)
    birth_date : str
    gender : Gender
    phone : str = Field(max_length=12)
    email : EmailStr
    address : str = Field(max_length=255)

    @validator('birth_date')
    def parse_birth_date(cls, v):
        return datetime.strptime(v, '%d-%m-%Y').date() 


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ClientUpdated(ClientBase):
    pass    