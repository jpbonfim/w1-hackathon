import json
import logging
import time

from fastapi import FastAPI, Request, Response
from starlette import status

from src.domain.exceptions.infrastructure import EnvironmentException
from src.domain.exceptions.router import (
    BadRequestError,
    NotFoundError,
    EntityNotFound,
)

from src.router.user import UserRouter


class BaseRouter:
    app = FastAPI(
        title="Stock Exchange Assets Information",
        description="Dados gerais da bolsa de valores",
    )

    @staticmethod
    def register_routers():
        user_router = UserRouter.get_routes()
        BaseRouter.app.include_router(user_router)
        return BaseRouter.app

    @staticmethod
    @app.middleware("http")
    async def middleware_response(request: Request, call_next):
        try:
            start_time = time.perf_counter()
            response = await call_next(request)
            process_time = time.perf_counter() - start_time
            response.headers["X-Process-Time"] = str(process_time)
            return response

        except BadRequestError as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=json.dumps(
                    {"success": False}
                ),
            )

        except NotFoundError as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=json.dumps(
                    {"success": False}
                ),
            )

        except EntityNotFound as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_404_NOT_FOUND,
                content=json.dumps(
                    {"success": False}
                ),
            )

        except EnvironmentException as err:
            logging.error(f"ENVIRONMENT ERROR!!! ->{err}")
            raise err

        except Exception as err:
            logging.error(f"{err}")
            return Response(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content=json.dumps(
                    {"success": False}
                ),
            )
