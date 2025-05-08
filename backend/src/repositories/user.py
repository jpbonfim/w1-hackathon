import logging

from src.domain.entities.user import User
from src.domain.exceptions.repository import DataNotFound, FailToPersist
from src.infrastructures import get_config
from src.infrastructures.mongo import MongoDBInfrastructure


class UserRepository(MongoDBInfrastructure):
    collection = None

    @classmethod
    def _get_collection(cls):
        if cls.collection is None:
            database = get_config("MONGO_DATABASE")
            collection = get_config("MONGO_COLLECTION_USERS")
            cls.collection = cls._instance_collection(database, collection)
        return cls.collection

    @classmethod
    async def get_user(cls, user_id: str) -> User:
        return await cls._get_user_by_query({"user_id": user_id})

    @classmethod
    async def get_user_by_cpf(cls, cpf: str) -> User:
        return await cls._get_user_by_query({"cpf": cpf})

    @classmethod
    async def _get_user_by_query(cls, query: dict) -> User:
        collection = cls._get_collection()
        user = await collection.find_one(query)
        if user is None:
            raise DataNotFound("User not found")
        return User(**user)

    @classmethod
    async def update_user(cls, user_id: str, user_data: dict):
        user_filter = {"user_id": user_id}
        try:
            collection = cls._get_collection()
            update = await collection.update_one(user_filter, {"$set": user_data})
        except Exception as error:
            message = f"Failed to update user {user_id}. Error: {error}"
            logging.error(message)
            raise FailToPersist(message)
        if not update.matched_count == 1:
            message = f"Failed to update user {user_id}."
            logging.error(message)
            raise FailToPersist(message)
