from datetime import timedelta

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi_jwt import JwtAuthorizationCredentials, JwtAccessBearer, JwtRefreshBearer
from starlette import status

from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import or_

from models import User
from schemas import SignUpModel, LoginModel
from database import SessionLocal
from werkzeug.security import generate_password_hash, check_password_hash

SECRET_KEY = "58597a77ef066bb037ecaa7bc0d6e30a5b1bc6203a6b7321f5883f5084192c7a"

access_security = JwtAccessBearer(
    secret_key=SECRET_KEY,
    auto_error=True,
    access_expires_delta=timedelta(hours=1)  # Token expires in 1 hour
)

refresh_security = JwtRefreshBearer(
    secret_key=SECRET_KEY,
    auto_error=True,
    refresh_expires_delta=timedelta(days=30)  # Refresh token expires in 30 days
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



auth_router = APIRouter(
    prefix="/auth",
)

# session = session(bind=engine)

@auth_router.get("/")
async def root(credentials: JwtAuthorizationCredentials = Depends(access_security)):
    current_user = credentials.subject["username"]
    return {
        "message": f"Welcome back, {current_user}!",
        "user": current_user
    }
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED )
async def signup(user: SignUpModel, db: Session = Depends(get_db)):
    db_email = db.query(User).filter_by(email=user.email).scalar()
    if db_email is not None:
        return {"message": "Email already registered"}

    db_username = db.query(User).filter(User.username == user.username).first()
    if db_username is not None:
        return {"message": "Username already registered"}

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password, method="pbkdf2:sha256"),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created"}


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(or_(User.username == user.username_or_email, User.email == user.username_or_email)).first()

    subject = {'username': db_user.username}

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = access_security.create_access_token(subject=subject)
        refresh_token = refresh_security.create_refresh_token(subject=subject)
        response= {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
        return jsonable_encoder(response)

    return {"message": "Invalid credentials"}


@auth_router.post("/login/refresh", status_code=status.HTTP_200_OK)
async def refresh_token(credentials: JwtAuthorizationCredentials = Depends(refresh_security), db: Session = Depends(get_db)):
    current_user = credentials.subject["username"]
    db_user = db.query(User).filter(User.username == current_user).first()

    if db_user is None:
        return {"message": "User not found"}

    new_access_token = access_security.create_access_token(subject={"username": db_user.username})

    return {
        "access_token": new_access_token,
        "message": "Successfully refreshed access token"
    }

