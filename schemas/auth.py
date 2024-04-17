from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    

class TokenData(BaseModel):
    id: int
    username: str
    role: str  
    agency_id: int
    client_id: int
	