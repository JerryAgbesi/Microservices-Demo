from typing import Optional
from pydantic import BaseModel,Field


class UserResponse(BaseModel):
    id: int
    name: str
    email: str


    class Config:
        from_attributes = True
   

class UserCreate(BaseModel):
    name: str = Field(...)
    email: str = Field(...)


