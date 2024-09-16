from fastapi import Depends, status,HTTPException
from typing import Optional
import secrets
from passlib.context import CryptContext
from database import User,get_db
from datetime import datetime, timedelta,timezone
from jose import jwt,JWTError
from dotenv import load_dotenv
import os
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
#create verification token 

load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




def generate_verification_token():
    return secrets.token_urlsafe(16)





def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)
#Ensure that only users with verified emails can log in

def authenticate_user(db, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.is_active:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# def authenticate_user(db, username: str, password: str):
#     user = db.query(User).filter(User.username == username).first()
#     if not user:
#         return False
#     if not verify_password(password, user.hashed_password):
#         return False
#     return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt



async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user





async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.role != "User":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "Admin":
        raise HTTPException(status_code=400, detail="Inactive admin")
    return current_user
