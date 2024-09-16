from sqlalchemy import create_engine, Column, Integer, String,Float, ForeignKey,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
import os 
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# initializing the database 
DATABASE_URL=os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# creating tables for the movie application to store and retrive the information from the database

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="User")
    is_active = Column(Boolean, default=False)
    verification_token = Column(String, nullable=True)
    reviews = relationship("Review", back_populates="user")
    
    


class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    director = Column(String, index=True)
    genre = Column(String, index=True)
    showtimes = relationship("Showtime", back_populates="movie")  # Add showtimes
    reviews = relationship('Review',  back_populates="movie")



class Showtime(Base):
    __tablename__ = "showtimes"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    start_time = Column(String, index=True)
    movie = relationship("Movie", back_populates="showtimes")
    



class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, index=True)
    seat_number = Column(String, index=True)
    user_name = Column(String, index=True)
    showtime_id = Column(Integer, ForeignKey('showtimes.id'))  # Add showtime ID

class Review(Base):
    __tablename__ ="reviews"
    id=Column(Integer,primary_key=True,index=True)
    movie_id=Column(Integer,ForeignKey("movies.id"))
    user_id=Column(Integer,ForeignKey("users.id"))
    rating=Column(Float)
    review_text=Column(String)
    movie=relationship("Movie",back_populates="reviews")
    user=relationship("User",back_populates="reviews")



Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

