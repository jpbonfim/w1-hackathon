import logging
from typing import Annotated

from fastapi import APIRouter
from fastapi import Header

from src.domain.contract_models.patrimony import (
    GetPatrimonyResponse,
    UpdatePatrimonyResponse,
    UpdatePatrimonyRequest, EvolutionResponse, HoldingResponse,
)
from src.domain.entities.patrymony import Patrimony
from src.domain.exceptions.service import EntityNotFound
from src.services.auth import AuthService
from src.services.patrimony import PatrimonyService


class PatrimonyRouter:
    __patrimony_router = APIRouter(
        prefix="/patrimony", tags=["User patrimony management"]
    )

    @staticmethod
    def get_routes():
        return PatrimonyRouter.__patrimony_router

    @staticmethod
    @__patrimony_router.get("/", response_model=GetPatrimonyResponse)
    async def get_user_patrimony(auth: Annotated[str, Header()]):
        token_data = AuthService.validate_token(auth)
        user_id = token_data.user_id

        try:
            patrimony = await PatrimonyService.get_patrimony(user_id)
            return GetPatrimonyResponse(success=True, patrimony=patrimony)
        except EntityNotFound:
            empty_patrimony_data = Patrimony()

            created_patrimony = await PatrimonyService.create_patrimony(
                user_id, empty_patrimony_data
            )
            return GetPatrimonyResponse(success=True, patrimony=created_patrimony)
        except Exception as e:
            logging.error("Failed to update patrimony: %s", str(e))
            raise

    @staticmethod
    @__patrimony_router.put(
        "/update",
        response_model=UpdatePatrimonyResponse,
    )
    async def update_user_patrimony(
        auth: Annotated[str, Header()], request: UpdatePatrimonyRequest
    ):
        token_data = AuthService.validate_token(auth)
        user_id = token_data.user_id

        try:
            update_data = request.patrimony

            try:
                updated_patrimony = await PatrimonyService.update_patrimony(
                    user_id, update_data
                )
                return UpdatePatrimonyResponse(
                    success=True, patrimony=updated_patrimony
                )
            except EntityNotFound:
                patrimony_data = update_data
                created_patrimony = await PatrimonyService.create_patrimony(
                    user_id, patrimony_data
                )
                return UpdatePatrimonyResponse(
                    success=True, patrimony=created_patrimony
                )

        except Exception as e:
            logging.error("Failed to update patrimony: %s", str(e))
            raise

    @staticmethod
    @__patrimony_router.get("/patrimony-history", response_model=EvolutionResponse)
    async def get_patrimony_history(auth: Annotated[str, Header()]):
        token_data = AuthService.validate_token(auth)
        history = await PatrimonyService.get_user_patrimony_history(user_id=token_data.user_id)
        response = EvolutionResponse(success=True, evolution=history)
        return response

    @staticmethod
    @__patrimony_router.get("/economy-history", response_model=EvolutionResponse)
    async def get_economy_history(auth: Annotated[str, Header()]):
        token_data = AuthService.validate_token(auth)
        history = await PatrimonyService.get_user_economy_history(user_id=token_data.user_id)
        response = EvolutionResponse(success=True, evolution=history)
        return response

    @staticmethod
    @__patrimony_router.get("/get-holding", response_model=HoldingResponse)
    async def get_user_holding(auth: Annotated[str, Header()]):
        token_data = AuthService.validate_token(auth)
        holding = await PatrimonyService.get_user_holding(user_id=token_data.user_id)
        response = HoldingResponse(success=True, holding=holding)
        return response

