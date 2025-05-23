import logging
from decimal import Decimal
from typing import Optional

from src.domain.entities.patrymony import PatrimonyInDB
from src.domain.exceptions.repository import DataNotFound, FailToPersist
from src.infrastructures.postgresql import PostgreSQLInfrastructure


class PatrimonyRepository(PostgreSQLInfrastructure):
    @classmethod
    async def get_patrimony_by_user_id(cls, user_id: str) -> Optional[PatrimonyInDB]:
        query = "SELECT * FROM patrimony WHERE user_id = $1"
        try:
            results = await cls.execute_query(query, [user_id])
            if not results:
                return None
            return PatrimonyInDB(**results[0])
        except Exception as error:
            message = f"Failed to get patrimony for user_id: {user_id}. Error: {error}"
            logging.error(message)
            raise

    @classmethod
    async def create_patrimony(cls, user_id: str, patrimony_data: dict) -> None:
        try:
            patrimony_data["user_id"] = user_id
            fields = ", ".join(patrimony_data.keys())
            placeholders = ", ".join(f"${i + 1}" for i in range(len(patrimony_data)))
            values = list(patrimony_data.values())

            command = f"INSERT INTO patrimony ({fields}) VALUES ({placeholders})"
            result = await cls.execute_command(command, values)

            if result != "SUCCESS":
                message = f"Failed to create patrimony for user_id: {patrimony_data.get('user_id')}"
                logging.error(message)
                raise FailToPersist(message)
        except Exception as error:
            message = f"Failed to create patrimony for user_id: {patrimony_data.get('user_id')}. Error: {error}"
            logging.error(message)
            raise FailToPersist(message)

    @classmethod
    async def update_patrimony(cls, user_id: str, update_data: dict) -> None:
        try:
            set_clause = ", ".join(
                f"{key} = ${i + 2}" for i, key in enumerate(update_data.keys())
            )
            values = list(update_data.values())
            values.insert(0, user_id)

            command = f"UPDATE patrimony SET {set_clause} WHERE user_id = $1"

            result = await cls.execute_command(command, values)
            if result != "SUCCESS":
                message = f"Failed to update patrimony for user {user_id}."
                logging.error(message)
                raise FailToPersist(message)

        except Exception as error:
            message = f"Failed to update patrimony for user {user_id}. Error: {error}"
            logging.error(message)
            raise FailToPersist(message)

    @classmethod
    async def delete_patrimony(cls, user_id: str) -> None:
        try:
            command = "DELETE FROM patrimony WHERE user_id = $1"
            result = await cls.execute_command(command, [user_id])

            if result != "SUCCESS":
                message = f"Failed to delete patrimony for user {user_id}."
                logging.error(message)
                raise FailToPersist(message)
        except Exception as error:
            message = f"Failed to delete patrimony for user {user_id}. Error: {error}"
            logging.error(message)
            raise FailToPersist(message)
