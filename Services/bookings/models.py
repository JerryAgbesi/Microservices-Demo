from typing import Optional
from pydantic import BaseModel,Field


class BookingResponse(BaseModel):
    id: int
    patron: str
    movies: list


    class Config:
        from_attributes = True
   

class BookingCreate(BaseModel):
    patron: str = Field(...)
    movies: list = Field(...)

