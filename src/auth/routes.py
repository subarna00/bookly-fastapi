from fastapi import status, APIRouter, Depends
from src.db import get_session
from .schemas import UserCreateModel, UserModel, UserModel, UserLoginModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import AuthService
from fastapi.exceptions import HTTPException
from .utils import create_access_token, decode_token, verify_password
from datetime import timedelta
from src.config import Config
from fastapi.responses import JSONResponse


auth_router = APIRouter()
auth_service = AuthService()

@auth_router.post("/signup", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreateModel, session: AsyncSession = Depends(get_session))-> UserModel:
    email = user_data.email
    if await auth_service.user_exists(email, session):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists")
    new_user = await auth_service.create_user(user_data, session)
    return new_user

@auth_router.post("/login")
async def login(user_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email
    password = user_data.password

    user = await auth_service.get_user_by_email(email,session)
    if user is not None:
        if verify_password(password, user.password_hash):

            access_token = create_access_token(data={"user_id": str(user.id), "email": user.email})
            refresh_token = create_access_token(data={"user_id": str(user.id), "email": user.email}, expires_delta=timedelta(seconds=Config.REFRESH_TOKEN_EXPIRY), refresh=True)

            return JSONResponse(
                content={
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "bearer",
                    "user":{
                        "id": str(user.id),
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name
                    }
                }
            )   
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid email or password")
