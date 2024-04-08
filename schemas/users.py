from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field,  EmailStr
from datetime import datetime



class UserStatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

class UserRole(str, Enum):
    agency= "agency"
    client = "client"    



class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr 
    status: UserStatusEnum = UserStatusEnum.active
    role: UserRole = UserRole.agency
    agency_id: Optional[int] = None
    client_id: Optional[int] = None

class UserPassword(BaseModel):    
    password: str = Field(min_length=1)

class UserCreate(UserBase, UserPassword):
    pass    

class User(UserBase):
    id: int
    hashed_password: str
    created: datetime
    updated: datetime

    class Config:
        from_atributtes = True

class UserUpdate(UserBase):
    pass   


class UserResponse(BaseModel):
    message: str
    user: User

