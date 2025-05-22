from datetime import timedelta

from fastapi import APIRouter, Depends

from src.domain.contract_models.auth import RegisterResponse, RegisterRequest, LoginRequest, LoginResponse
from src.domain.entities.user import User
from src.domain.exceptions.router import Unauthorized
from src.services.auth import AuthService
from src.services.user import UserService


class AuthRouter:
    __router = APIRouter(prefix="/auth", tags=["Auth"])

    @staticmethod
    def get_routes():
        return AuthRouter.__router

    @staticmethod
    @__router.post("/register", response_model=RegisterResponse)
    async def register_user(user_create: RegisterRequest = Depends(RegisterRequest)):
        hashed_password = AuthService.get_password_hash(user_create.password)

        user_data = user_create.model_dump()
        user_data.pop("password")
        user_data["password"] = hashed_password

        user_id = await UserService.create_user(user_data=user_data)
        return RegisterResponse(success=True, user_id=user_id)


    @staticmethod
    @__router.post("/login", response_model=LoginResponse)
    async def login_for_access_token(form_data: LoginRequest = Depends(LoginRequest)):
        user = await AuthService.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise Unauthorized()
        
        access_token_expires = timedelta(minutes=AuthService.get_token_expiration_time())
        access_token = AuthService.create_access_token(
            data={"sub": user.user_id}, expires_delta=access_token_expires
        )
        
        return LoginResponse(
            success=True,
            user_id=user.user_id,
            access_token=access_token,
            token_type="bearer"
        )

    # @staticmethod
    # @__router.get("/me")
    # async def get_current_user():
    #     """Get current logged in user information"""
    #     return