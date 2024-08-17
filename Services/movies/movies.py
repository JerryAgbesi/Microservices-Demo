from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,HTTPException
import logging


from models import MovieResponse
from db_handler import Movie,Base,engine,get_db

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title = "Movie Service",lifespan=lifespan)

@app.get("/movies",status_code=status.HTTP_200_OK)
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return movies

@app.get("/movies/{movie_id}",status_code=status.HTTP_200_OK,response_model=MovieResponse)
def get_movie(movie_id:int,db: Session = Depends(get_db)):
    movie = db.query(Movie).filter(Movie.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="movie not found")
    
    return movie
