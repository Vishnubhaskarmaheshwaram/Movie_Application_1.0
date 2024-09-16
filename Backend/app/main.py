from fastapi import FastAPI, Depends, HTTPException, status,Request,Form
from fastapi.responses import HTMLResponse,JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

from jose import JWTError, jwt
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from authlib.integrations.starlette_client import OAuth, OAuthError
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
import os
import asyncio
from fastapi.middleware.cors import CORSMiddleware

import aiosmtplib
from email.message import EmailMessage
from sqlalchemy import inspect
import verify_mail

from utils import create_access_token,get_password_hash,get_current_active_admin,get_current_active_user,verify_password,generate_verification_token
from database import  get_db, User,Movie,Ticket,Showtime,Session,Review
import smtplib
from email.mime.text import MIMEText
load_dotenv()
import logging
import models 
from fastapi.templating import Jinja2Templates

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


# DATABASE_URL=os.getenv("DATABASE_URL")
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


app = FastAPI()

app.include_router(verify_mail.router)

# Mount the frontend directory to serve static files
#app.mount("/", StaticFiles(directory="../Frontend", html=True), name="static")
# 


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your specific needs
    allow_credentials=True,
    allow_methods=["*"],

    allow_headers=["*"],
)


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)


# load environment variables from .env file 


logging.basicConfig(level=logging.DEBUG)





#-------------------------------------------------------------

#  api endpoints for movie application

# Mount the static files directory to serve the frontend
app.mount("/static", StaticFiles(directory="../Frontend/static"), name="static")
# app.mount("/static", StaticFiles(directory="C:/Users/vishnu.bhaskar/python_Programs/movie_application_2.0/Backend/Frontend"), name="static")

# Route to serve the registration page
# @app.get("/", include_in_schema=False)
# async def redirect_to_registration():
#     return RedirectResponse(url="/templates/register.html")

# # Other routes
# @app.get("/login", include_in_schema=False)
# async def login_page():
#     return FileResponse("../Frontend/templates/index.html")

# @app.get("/", include_in_schema=False)
# async def redirect_to_registration():
#     return RedirectResponse(url="/register")
# @app.get("/", include_in_schema=False)
# async def redirect_to_registration():
#     try:
#         return RedirectResponse(url="/register")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
# @app.get("/register", include_in_schema=False)
# async def register_page():
#     return FileResponse("../Frontend/templates/register.html")

# @app.get("/login", include_in_schema=False)
# async def login_page():
#     return FileResponse("../Frontend/templates/index.html")

# templates = Jinja2Templates(directory="Frontend/templates")
BASE_DIR = os.path.dirname(os.path.abspath("C:/Users/vishnu.bhaskar/python_Programs/movie_application_2.0/Backend/Frontend"))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, 'Frontend', 'templates'))
@app.get("/")
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/register")
async def get_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.get("/user")
async def get_user_page(request: Request):
    return templates.TemplateResponse("user.html", {"request": request})

@app.get("/admin")
async def get_admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


# @app.get("/users/", response_model=List[models.UserResponse])
# async def get_all_users(db: Session = Depends(get_db)):
#     users = db.query(User).all()
#     return users





@app.post("/users/", response_model=models.UserResponse)
async def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Username already registered")

        hashed_password = get_password_hash(user.password)
        verification_token = generate_verification_token()

        db_user = User(
            username=user.username,
            hashed_password=hashed_password,
            email=user.email,
            role=user.role,
            verification_token=verification_token
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        return JSONResponse(content={
            "message": "User registered successfully",
            "role": db_user.role
        })
        #return db_user
    except HTTPException as e:
        # Handling HTTP exceptions
        raise e
    except Exception as e:
        logging.error(f"Error during user registration: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")




@app.post("/token", response_model=models.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role},  # Include role in the token data
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "user_id": user.id, "role": user.role}  # Return role


# @app.post("/users/", response_model=models.UserResponse)
# async def create_user(user: models.UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")

#     hashed_password = get_password_hash(user.password)
#     verification_token = generate_verification_token()
    
#     db_user = User(
#         username=user.username,
#         hashed_password=hashed_password,
#         email=user.email,
#         role=user.role,
#         verification_token=verification_token
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
    
#     return JSONResponse(content={
#         "message": "User registered successfully",
#         "role": db_user.role
#     })



@app.get("/allmovies/", response_model=List[models.MovieResponse])
async def list_movies(db: Session = Depends(get_db)):
    movies = db.query(Movie).all()
    return movies



@app.post("/movies/", response_model=models.MovieCreate)
async def create_movie(movie: models.MovieCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_admin)):
    db_movie = Movie(title=movie.title, director=movie.director, genre=movie.genre)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie




@app.post("/showtimes/", response_model=models.ShowtimeCreate)
async def create_showtime(showtime: models.ShowtimeCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_admin)):
    db_showtime = Showtime(movie_id=showtime.movie_id, start_time=showtime.start_time)
    db.add(db_showtime)
    db.commit()
    db.refresh(db_showtime)
    return db_showtime




@app.post("/tickets/", response_model=models.TicketResponse)
async def create_ticket(ticket: models.TicketCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    db_ticket = Ticket(movie_id=ticket.movie_id, seat_number=ticket.seat_number, user_name=ticket.user_name, showtime_id=ticket.showtime_id)
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket



@app.delete("/users/{user_id}", response_model=bool)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Delete a user by user_id from the database.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
   
 
    db.delete(user)
    db.commit()
    return True



@app.post("/reviews/",response_model=models.ReviewCreate)
async def create_review(review:models.ReviewCreate,db:Session=Depends(get_db)):
    db_review=Review(movie_id=review.movie_id,user_id=review.user_id,rating=review.rating,review_text=review.review_text)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review 



@app.get("/movies/{movie_id}/reviews",response_model=list[models.ReviewCreate])
async def user_reviews(movie_id:int,db:Session=Depends(get_db)):
    db_reviews=db.query(Review).filter(Review.movie_id==movie_id).all()
    if not db_reviews:
        raise HTTPException(status_code=404,detail="no reviews registered")
    return db_reviews




# @app.post("/token", response_model=models.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return {"access_token": access_token, "token_type": "bearer"}



# @app.post("/token", response_model=models.Token)
# async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.username == form_data.username).first()
#     if not user or not verify_password(form_data.password, user.hashed_password):
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
#     access_token = create_access_token(
#         data={"sub": user.username}, expires_delta=access_token_expires
#     )
#     return JSONResponse(content={
#         "access_token": access_token,
#         "token_type": "bearer",
#         "role": user.role
#     })




@app.get("/movies/{movie_id}/showtimes", response_model=List[models.ShowtimeResponse])
async def get_showtimes(movie_id: int, db: Session = Depends(get_db)):
    showtimes = db.query(Showtime).filter(Showtime.movie_id == movie_id).all()
    if not showtimes:
        raise HTTPException(status_code=404, detail="No showtimes available for this movie.")
    return showtimes




# DATABASE_URL = os.getenv("DATABASE_URL")
# print("Database URL:", DATABASE_URL)



# inspector = inspect(engine)
# print(inspector.get_columns('users'))

#------------------------------------------------------------------


# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)