import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

from src.domain.exceptions.infrastructure import (
    DatabaseStructureException,
    ConnectionException,
)
from src.infrastructures import get_config


class MongoDBInfrastructure:
    client = None

    @classmethod
    def _get_client(cls):
        if cls.client is None:
            mongo_connection_url = get_config("MONGO_CONNECTION_URL")
            try:
                cls.client = AsyncIOMotorClient(mongo_connection_url)
            except Exception as error:
                logging.error(
                    f"Error connecting to MongoDB. URL: {mongo_connection_url}\n"
                    f"Error: {error}"
                )
                raise ConnectionException()
        return cls.client

    @classmethod
    def _instance_collection(
        cls, database: str, collection: str
    ) -> AsyncIOMotorCollection:
        connection = cls._get_client()
        try:
            database = connection[database]  # pylint: disable=E1136
            collection = database[collection]
            return collection
        except Exception as error:
            logging.error(
                f"Error getting MongoDB collection."
                f"database: {database}, collection: {collection} \n"
                f"Error: {error}"
            )
            raise DatabaseStructureException()
