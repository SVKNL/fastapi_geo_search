import logging
import sys

from fastapi import FastAPI

from app.middleware.logging import logging_middleware
from app.routers.buildings import router as buildings_router
from app.routers.health import router as health_router
from app.routers.organizations import router as organizations_router


app = FastAPI(title="Organization Directory API")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
app.middleware("http")(logging_middleware)
app.include_router(health_router)
app.include_router(buildings_router)
app.include_router(organizations_router)
