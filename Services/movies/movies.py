from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,HTTPException
import logging


from models import MovieResponse,MovieCreate
from db_handler import Movies,Base,engine,get_db

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title = "Movie Service",lifespan=lifespan)

@app.get("/movies",status_code=status.HTTP_200_OK)
def get_movies(db: Session = Depends(get_db)):
    movies = db.query(Movies).all()
    return movies

@app.post("/",status_code=status.HTTP_201_CREATED,response_model=MovieResponse)
def create_movie(movie: MovieCreate ,db: Session = Depends(get_db)):
    new_movie = Movies(**movie.model_dump())
    try:
        db.add(new_movie)
        db.commit()
        db.refresh(new_movie)

        logging.info("new movie created")

        return new_movie
    except Exception as e:
        db.rollback()
        logging.debug(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Unable to create movie")

@app.get("/movies/{movie_id}",status_code=status.HTTP_200_OK,response_model=MovieResponse)
def get_movie(movie_id:int,db: Session = Depends(get_db)):
    movie = db.query(Movies).filter(Movies.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="movie not found")
    
    return movie
