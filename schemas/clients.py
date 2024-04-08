from enum import Enum
import random
import string
from typing import Optional
from pydantic import BaseModel,Field, EmailStr, validator
from datetime import date, datetime

class Gender(str, Enum):
    M = 'M'
    F = 'F'

class ClientBase(BaseModel):
    first_name : str =  Field(max_length=50)
    last_name : str =Field(max_length=75)
    birth_date : Optional[date] = date(2000,1,1)
    gender : Gender
    phone : str = Field(max_length=12)
    email : EmailStr
    address : str = Field(max_length=255)
    client_code:str
    


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):   
    id: int
    created: datetime
    updated: datetime

    class Config:
        from_atributtes = True

 


class ClientUpdated(ClientBase):
    pass    