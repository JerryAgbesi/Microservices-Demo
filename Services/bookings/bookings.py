from contextlib import asynccontextmanager
from prometheus_client import start_http_server,Counter,Histogram
from sqlalchemy.orm import Session
from fastapi import FastAPI,Depends,status,HTTPException
import logging


from db_handler import Booking,Base,engine,get_db

logging.basicConfig(format='%(asctime)s %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

REQUEST_COUNT = Counter("request_count","App request count")
REQUEST_LATENCY = Histogram("request_latency","Time taken for request to complete")

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title = "Booking Service",lifespan=lifespan)

start_http_server(6000)

@app.get("/bookings",status_code=status.HTTP_200_OK)
def get_bookings(db: Session = Depends(get_db)):
    bookings = db.query(Booking).all()
    return bookings

@REQUEST_LATENCY.time()
@app.get("/bookings/{patron}", status_code=status.HTTP_200_OK)
def get_booking(patron: str, db: Session = Depends(get_db)):
    REQUEST_COUNT.inc()
    bookings = db.query(Booking).filter(Booking.patron == patron).all()
    if not bookings:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="booking not found")
    
    return bookings
