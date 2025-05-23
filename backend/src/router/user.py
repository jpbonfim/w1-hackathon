from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi import Header

from src.domain.contract_models.user import (
    CreateUserResponse,
    CreateUserRequest,
    GetUserResponse,
    GetUserRequest,
    MeResponse,
    UpdateUserRequest,
    UpdateUserResponse,
)
from src.services.auth import AuthService
from src.services.user import UserService


class AccountRouter:
    __user_router = APIRouter(prefix="/account", tags=["User account management"])

    @staticmethod
    def get_routes():
        return AccountRouter.__user_router

    # @staticmethod
    # @__user_router.post(
    #     "/create",
    #     response_model=CreateUserResponse,
    # )
    # async def create_user(request: CreateUserRequest):
    #     user_data = request.model_dump()
    #     user_id = await UserService.create_user(user_data=user_data)
    #     response = CreateUserResponse(success=True, user_id=user_id)
    #     return response
    #
    # @staticmethod
    # @__user_router.get(
    #     "/get",
    #     response_model=GetUserResponse,
    # )
    # async def get_user(request: GetUserRequest = Depends(GetUserRequest)):
    #     user = await UserService.get_user(user_id=request.user_id)
    #     response = GetUserResponse(success=True, user=user)
    #     return response

    @staticmethod
    @__user_router.get("/me", response_model=MeResponse)
    async def get_current_user(auth: Annotated[str, Header()]):
        token_data = AuthService.validate_token(auth)
        user = await UserService.get_user(user_id=token_data.user_id)
        response = MeResponse(success=True, user_data=user)
        return response

    @staticmethod
    @__user_router.put(
        "/update",
        response_model=UpdateUserResponse,
    )
    async def update_user(auth: Annotated[str, Header()], request: UpdateUserRequest):
        token_data = AuthService.validate_token(auth)
        user_data = {k: v for k, v in request.model_dump().items() if v is not None}
        if user_data:
            await UserService.update_user(user_id=token_data.user_id, update_data=user_data)
        response = UpdateUserResponse(success=True)
        return response
