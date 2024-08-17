from sqlalchemy import create_engine,Column,Float,Integer,String,ForeignKey,TIMESTAMP,JSON,UUID,Uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create table for movies

class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer,primary_key=True,index=True)
    title = Column(String,nullable=False)
    rating = Column(Float,unique=True)
    director = Column(String,nullable=False)
