from pydantic import BaseModel,Field


class MovieResponse(BaseModel):
    id: int
    title: str
    rating: float
    director: str


    class Config:
        from_attributes = True
   

class MovieCreate(BaseModel):
    title: str = Field(...)
    rating: float = Field(...)
    director: str = Field(...)

