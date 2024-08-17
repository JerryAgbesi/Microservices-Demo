from sqlalchemy import create_engine,Column,Float,Integer,String,ForeignKey,TIMESTAMP,JSON,UUID,Uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import uuid
import datetime


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

# Create table for users

class User(Base):
    __tablename__ = "users"
    # id = Column(Integer,primary_key=True,index=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False)
    created_at = Column(TIMESTAMP,default=datetime.now())