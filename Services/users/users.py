from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,HTTPException
import logging
import requests
import json

from models import UserResponse
from db_handler import User,Base,engine,get_db

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title = "User Service",lifespan=lifespan)

@app.get("/users",status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    students = db.query(User).all()
    return students

@app.get("/users/{user_name}",status_code=status.HTTP_200_OK,response_model=UserResponse)
def get_user(user_name:str,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    
    return user

@app.get("/users/{user_name}/bookings",status_code=status.HTTP_200_OK)
def get_user_bookings(user_name: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.name == user_name).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="user not found")
    
    try:
        users_bookings = requests.get(f"http://bookings-service:4004/bookings/{user_name}",verify=False)
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="The Bookings service is unavailable.")

    if users_bookings.status_code == 404:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"No bookings were found for {user_name}")
    
    users_bookings = users_bookings.json()
    

    for booking in users_bookings:
        movies = booking["movies"]
        result = []
       
        for movieId in movies:
            try: 
                movie = requests.get(f"http://movies-service:4001/movies/{movieId}",verify=False)
            except requests.exceptions.ConnectionError:
                raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,detail="The movies service is unavailable.")
            
            movie = movie.json()
            result.append({
                "title": movie["title"],
                "director": movie["director"],
                "rating": movie["rating"]})

        booking["movies"] = result
    

    return users_bookings
