import smtplib
from email.mime.text import MIMEText
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from database import get_db,User
from  models import UserCreate,UserResponse
from  utils import get_password_hash ,generate_verification_token

router=APIRouter()

async def send_verification_email(email: str, token: str):
    # message = EmailMessage()
    # message["From"] = "noreply@yourdomain.com"
    # message["To"] = email
    # message["Subject"] = "Verify Your Email"
    verification_link = f"http://localhost:8000/verify-email?token={token}"
    # message.set_content(f"Please verify your email by clicking the following link: {verification_link}")
   
   
   
    msgcontent=f"Please verify your email by clicking the following link: {verification_link}"
    msg = MIMEText(msgcontent)
    msg["Subject"] = "Verify Your Email"
    msg["From"] = "vishnumaheshwaram1997@gmail.com"
    msg["To"] = email
 
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("vishnumaheshwaram1997@gmail.com", "bsppxslgwiwdtqcn")
            response=server.send_message(msg)
            print("SMTP server response:",response)
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")


#Create an Email Verification Endpoint
@router.get("/verify-email")
async def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")

    user.is_active = True
    user.verification_token = None
    db.commit()
    return {"message": "Email verified successfully"}


#Modify User Registration to Include Email Verification

# @router.post("/users/", response_model=UserResponse)
# async def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = db.query(User).filter(User.username == user.username).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already registered")
#     # db_email = db.query(User).filter(User.email == user.email).first()
#     # if db_email:
#     #     raise HTTPException(status_code=400, detail="Email already registered")

#     hashed_password = get_password_hash(user.password)
#     verification_token = generate_verification_token()
    
#     db_user = User(
#         username=user.username,
#         hashed_password=hashed_password,
#         email=user.email,
#         role=user.role,
#         verification_token=verification_token
#     )
#     print(db_user)
#     print(hashed_password)
#     print(verification_token)
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
     
#     # asyncio.run(send_verification_email(user.email, verification_token))
#    # await send_verification_email(user.email, verification_token)

#     return db_user


# Send Verification Email
# async def send_verification_email(email: str, token: str):
#     # message = EmailMessage()
#     # message["From"] = "noreply@yourdomain.com"
#     # message["To"] = email
#     # message["Subject"] = "Verify Your Email"
#     verification_link = f"http://localhost:8000/verify-email?token={token}"
#     # message.set_content(f"Please verify your email by clicking the following link: {verification_link}")
    
    
    
#     msgcontent=f"Please verify your email by clicking the following link: {verification_link}"
#     msg = MIMEText(msgcontent)
#     msg["Subject"] = "Verify Your Email"
#     msg["From"] = "vishnumaheshwaram1997@gmail.com"
#     msg["To"] = email

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login("vishnumaheshwaram1997@gmail.com", "bsppxslgwiwdtqcn")
#             server.send_message(msg)
#         print("Email sent successfully")
#     except Exception as e:
#         print(f"Failed to send email: {e}")
#     # try:
#     #     await aiosmtplib.send(
#     #         message,
#     #         hostname="smtp.gmail.com",
#     #         port=587,
#     #         username="vishnumaheshwaram1997@gmail.com",
#     #         password="bsppxslgwiwdtqcn",  # Use an App Password
#     #         start_tls=True,  # Ensure TLS is started after connecting
#     #     )
#     #     print("Email sent successfully")
#     # except Exception as e:
#     #     print(f"Failed to send email: {e}")




