from typing import Optional
from pydantic import BaseModel,Field


class BookingResponse(BaseModel):
    id: int
    name: str
    booked_dates: str


    class Config:
        from_attributes = True
   

class BookingCreate(BaseModel):
    name: str = Field(...)
    booked_dates: str = Field(...)

