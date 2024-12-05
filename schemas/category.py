from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(min_length=0, max_length=20)
    description: Optional[str] = None
    code_category: str = Field(min_length=0, max_length=20)

class CategoryCreate(CategoryBase):
    pass

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CategoryUpdate(CategoryBase):
    pass

