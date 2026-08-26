from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.config import settings
from app.db.database import Base, engine
from app.models import user, site, site_member, work_item

from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers import site
from app.routers import site_member
from app.routers import work_item
from app.core.exceptions import (
    validation_exception_handler,
    http_exception_handler,
)


# Import model trước khi create_all
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title=settings.APP_NAME
)

app.add_exception_handler(
    RequestValidationError,
    validation_exception_handler,
)
app.add_exception_handler(
    StarletteHTTPException,
    http_exception_handler,
)


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(site.router)
app.include_router(site_member.router)
app.include_router(work_item.router)
