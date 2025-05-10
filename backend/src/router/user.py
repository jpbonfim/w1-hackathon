from fastapi import APIRouter, Depends

from src.domain.contract_models.user import (
    CreateUserResponse,
    CreateUserRequest,
    GetUserResponse,
    GetUserRequest,
)
from src.services.user import UserService


class UserRouter:
    __user_router = APIRouter(prefix="/users", tags=["Users"])

    @staticmethod
    def get_routes():
        return UserRouter.__user_router

    @staticmethod
    @__user_router.post(
        "/create",
        response_model=CreateUserResponse,
    )
    async def create_user(request: CreateUserRequest = Depends(CreateUserRequest)):
        user_data = request.model_dump()
        user_id = await UserService.create_user(user_data=user_data)
        response = CreateUserResponse(success=True, user_id=user_id)
        return response

    @staticmethod
    @__user_router.get(
        "/",
        response_model=GetUserResponse,
    )
    async def get_user(request: GetUserRequest = Depends(GetUserRequest)):
        user = await UserService.get_user(user_id=request.user_id)
        response = GetUserResponse(success=True, user=user)
        return response
