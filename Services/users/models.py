from typing import Optional
from pydantic import BaseModel,Field
from uuid import UUID

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str


    class Config:
        from_attributes = True
   

class UserCreate(BaseModel):
    name: str = Field(...)
    email: str = Field(...)


