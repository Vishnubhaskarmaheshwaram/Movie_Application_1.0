from pydantic import BaseModel,EmailStr
from typing  import Optional,List
from datetime import datetime 



#User Registration Model
class UserCreate(BaseModel):
    username: str
    password: str
    email:str
    # email: EmailStr
    role: Optional[str] = "Admin"
# class UserCreate(BaseModel):
#     username: str
#     password: str

class UserResponse(BaseModel):
    id: int
    username: str

    role: str

    class Config:
        orm_mode = True

class MovieCreate(BaseModel):
    title: str
    director: str
    genre: str

class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    genre: str
    showtimes: List['ShowtimeResponse']

    class Config:
        orm_mode = True

class ShowtimeCreate(BaseModel):
    movie_id: int
    start_time: str

class ShowtimeResponse(BaseModel):
    id: int
    movie_id: int
    start_time: datetime
    
    class Config:
        orm_mode = True

class TicketCreate(BaseModel):
    movie_id: int
    seat_number: str
    user_name: str
    showtime_id: int

class TicketResponse(BaseModel):
    id: int
    movie_id: int
    seat_number: str
    user_name: str
    showtime_id: int

    class Config:
        orm_mode = True

class ReviewResponse(BaseModel):
    id: int
    movie_id: int
    movie_title: str  # Add this field
    user_id: int
    rating: int
    review_text: str
    # other fields...

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id:int 
    role:str

class TokenData(BaseModel):
    username: Optional[str] = None
#---------------------------------------------
class ReviewCreate(BaseModel):
    movie_id:int 
    user_id:int 
    rating:float
    review_text:str 

class MovieResponce(BaseModel):
    id:int 
    title:int 
    director:str 
    genre:str 
    average_rating:float 
    reviews:List[ReviewCreate]
    class Config:
        orm_mode=True 
#--------------------------------------------------------------------------           
