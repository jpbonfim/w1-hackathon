from fastapi import APIRouter

from src.domain.contract_models.auth import (
    RegisterResponse,
    RegisterRequest,
    LoginRequest,
    LoginResponse,
)
from src.domain.exceptions.router import Unauthorized
from src.repositories.user import UserRepository
from src.services.auth import AuthService
from src.services.user import UserService


class AuthRouter:
    __router = APIRouter(prefix="/auth", tags=["Auth"])

    @staticmethod
    def get_routes():
        return AuthRouter.__router

    @staticmethod
    @__router.post("/register", response_model=RegisterResponse)
    async def register_user(user_create: RegisterRequest):
        hashed_password = AuthService.get_password_hash(user_create.password)

        user_data = user_create.model_dump()
        user_data.pop("password")
        user_id = await UserService.create_user(user_data=user_data)
        await UserRepository.register_password(user_id, hashed_password)

        return RegisterResponse(success=True, user_id=user_id)

    @staticmethod
    @__router.post("/login", response_model=LoginResponse)
    async def login_for_access_token(request: LoginRequest):
        user = await AuthService.authenticate_user(request.email, request.password)
        if not user:
            raise Unauthorized()

        access_token = AuthService.create_access_token(data={"user_id": user.user_id})

        return LoginResponse(
            success=True,
            user_id=user.user_id,
            access_token=access_token,
            token_type="bearer",
        )
