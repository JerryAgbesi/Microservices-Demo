from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,HTTPException
import logging

from models import BookingResponse
from db_handler import Booking,Base,engine,get_db

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title = "Booking Service",lifespan=lifespan)

@app.get("/bookings",status_code=status.HTTP_200_OK)
def get_bookings(db: Session = Depends(get_db)):
    students = db.query(Booking).all()
    return students

@app.get("/bookings/{student_name}",status_code=status.HTTP_200_OK,response_model=BookingResponse)
def get_booking(user_name:int,db: Session = Depends(get_db)):
    booking = db.query(Booking).filter(Booking.user == user_name).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="booking not found")
    
    return booking
