import logging
from typing import Any, List, Optional, Dict

import asyncpg
from asyncpg.pool import Pool

from src.domain.exceptions.infrastructure import (
    ConnectionException,
    QueryExecutionException,
    CommandExecutionException,
    RecordAlreadyExistsException,
)
from src.infrastructures import get_config


class PostgreSQLInfrastructure:
    _pool: Optional[Pool] = None

    @classmethod
    async def _get_connection_pool(cls) -> Pool:
        if cls._pool is None:
            try:
                connection_url = get_config("POSTGRES_CONNECTION_URL")
                cls._pool = await asyncpg.create_pool(
                    dsn=connection_url, min_size=1, max_size=10
                )
            except Exception as error:
                logging.error(f"Failed to create PostgreSQL connection pool: {error}")
                raise ConnectionException()
        return cls._pool

    @classmethod
    async def execute_query(
        cls, query: str, params: Optional[List[Any]] = None
    ) -> List[Dict[str, Any]]:
        pool = await cls._get_connection_pool()
        async with pool.acquire() as connection:
            try:
                statement = await connection.prepare(query)
                if params:
                    rows = await statement.fetch(*params)
                else:
                    rows = await statement.fetch()
                return [dict(row) for row in rows]
            except Exception as error:
                logging.error(f"Failed to execute query: {error}")
                raise QueryExecutionException()

    @classmethod
    async def execute_command(
        cls, command: str, params: Optional[List[Any]] = None
    ) -> str:
        pool = await cls._get_connection_pool()
        async with pool.acquire() as connection:
            try:
                if params:
                    await connection.execute(command, *params)
                else:
                    await connection.execute(command)
                return "SUCCESS"
            except asyncpg.exceptions.UniqueViolationError:
                logging.error("Unique constraint violation")
                raise RecordAlreadyExistsException()
            except Exception as error:
                logging.error(f"Failed to execute command: {error}")
                raise CommandExecutionException()
