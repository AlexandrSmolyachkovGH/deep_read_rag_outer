"""Main app file."""

import uvicorn
from fastapi import FastAPI

from app.routers.health import router as health_router
from app.routers.root import router as root_router

app = FastAPI()

app.include_router(root_router)
app.include_router(health_router)

if __name__ == "__main__":
    uvicorn.run(
        app=app,
        host="127.0.0.1",
        port=8000,
    )
