import logging
from typing import Dict, Any, Optional

from src.domain.entities.user import User
from src.domain.exceptions.repository import DataNotFound, FailToPersist
from src.infrastructures import get_config
from src.infrastructures.postgresql import PostgreSQLInfrastructure


class UserRepository(PostgreSQLInfrastructure):
    @classmethod
    async def get_user(cls, user_id: str) -> User:
        return await cls._get_user_by_query("user_id", user_id)

    @classmethod
    async def get_user_by_cpf(cls, cpf: str) -> User:
        return await cls._get_user_by_query("cpf", cpf)

    @classmethod
    async def _get_user_by_query(cls, field: str, value: str) -> User:
        query = f"SELECT * FROM users WHERE {field} = $1"
        try:
            results = await cls.execute_query(query, [value])
            if not results:
                raise DataNotFound("User not found")
            return User(**results[0])
        except DataNotFound:
            raise
        except Exception as error:
            message = f"Failed to get user with {field}: {value}. Error: {error}"
            logging.error(message)
            raise

    @classmethod
    async def create_user(cls, user: User) -> None:
        try:
            user_data = user.model_dump()
            fields = ", ".join(user_data.keys())
            placeholders = ", ".join(f"${i + 1}" for i in range(len(user_data)))
            values = list(user_data.values())

            command = f"INSERT INTO users ({fields}) VALUES ({placeholders})"
            await cls.execute_command(command, values)
        except Exception as error:
            message = f"Failed to create user CPF: {user.cpf}. Error: {error}"
            logging.error(message)
            raise FailToPersist(message)

    @classmethod
    async def update_user(cls, user_id: str, update_data: dict) -> None:
        try:
            set_clause = ", ".join(f"{key} = ${i + 2}" for i, key in enumerate(update_data.keys()))
            values = list(update_data.values())
            values.insert(0, user_id)

            command = f"UPDATE users SET {set_clause} WHERE user_id = $1"

            result = await cls.execute_command(command, values)
            if result != "SUCCESS":
                message = f"Failed to update user {user_id}."
                logging.error(message)
                raise FailToPersist(message)
        except Exception as error:
            message = f"Failed to update user {user_id}. Error: {error}"
            logging.error(message)
            raise FailToPersist(message)