import logging
from decimal import Decimal
from typing import Optional, Dict, Any

from src.domain.entities.patrymony import (
    PatrimonyInDB,
    PatrimonyCreate,
    PatrimonyUpdate,
    Patrimony,
)
from src.domain.exceptions.repository import DataNotFound, FailToPersist
from src.domain.exceptions.service import EntityNotFound
from src.repositories.patrimony import PatrimonyRepository


class PatrimonyService:
    @classmethod
    async def create_patrimony(
        cls, user_id: str, patrimony_data: Patrimony
    ) -> PatrimonyInDB:
        try:
            existing_patrimony = await PatrimonyRepository.get_patrimony_by_user_id(
                user_id
            )

            if existing_patrimony:
                return existing_patrimony

            patrimony_dict = patrimony_data.model_dump()
            await PatrimonyRepository.create_patrimony(user_id, patrimony_dict)

            created_patrimony = await PatrimonyRepository.get_patrimony_by_user_id(
                user_id
            )

            if not created_patrimony:
                message = f"Failed to retrieve created patrimony for user {user_id}"
                logging.error(message)
                raise FailToPersist(message)

            return created_patrimony

        except Exception as error:
            message = f"Failed to create patrimony: {error}"
            logging.error(message)
            raise

    @classmethod
    async def update_patrimony(
        cls, user_id: str, patrimony: Patrimony
    ) -> PatrimonyInDB:
        current_patrimony = await PatrimonyRepository.get_patrimony_by_user_id(user_id)

        if not current_patrimony:
            message = f"Patrimony not found for user {user_id}"
            logging.error(message)
            raise EntityNotFound(message)

        update_data = patrimony.model_dump()
        await PatrimonyRepository.update_patrimony(user_id, update_data)
        updated_patrimony = await PatrimonyRepository.get_patrimony_by_user_id(user_id)
        return updated_patrimony

    @classmethod
    async def get_patrimony(cls, user_id: str) -> PatrimonyInDB:
        patrimony = await PatrimonyRepository.get_patrimony_by_user_id(user_id)

        if not patrimony:
            message = f"Patrimony not found for user {user_id}"
            logging.error(message)
            raise EntityNotFound(message)

        return patrimony

    @classmethod
    async def get_user_patrimony_history(cls, user_id: str) -> list[dict]:
        history = await PatrimonyRepository.get_patrimony_history(user_id)

        if not history:
            patrimony = await cls.get_patrimony(user_id)
            values = patrimony.model_dump()
            values.pop("id")
            values.pop("user_id")
            values.pop("created_at")
            values.pop("updated_at")
            total_patrimony = 0

            for key, value in values.items():
                total_patrimony += value

            return [{"month": "Mai", "value": total_patrimony}]

        return history

    @classmethod
    async def get_user_economy_history(cls, user_id: str) -> list[dict]:
        history = await PatrimonyRepository.get_economy_history(user_id)

        if not history:
            return [{"month": "Mai", "value": 0}]

        return history
