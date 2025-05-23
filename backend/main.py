import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from src.router.base import BaseRouter
from src.infrastructures import get_config

app = BaseRouter.register_routers()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(get_config("W1_BACKEND_PORT")),
        log_level="info",
        # root_path=get_config("W1_BACKEND_ROOT_PATH"),
    )


