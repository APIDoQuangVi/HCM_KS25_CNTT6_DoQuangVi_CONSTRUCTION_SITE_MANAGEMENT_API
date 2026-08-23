from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.db.database import Base, engine
from app.models import user, site, site_member, work_item
from app.routers.health import router as health_router
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers import site
from app.routers import site_member
from app.routers import work_item
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME
)

@app.exception_handler(RequestValidationError)
def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "message": "Validation error",
            "data": None,
            "error": exc.errors(),
            "path": str(request.url.path),
        },
    )


@app.exception_handler(404)
def not_found_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "statusCode": 404,
            "message": "Resource not found",
            "data": None,
            "error": str(exc),
            "path": str(request.url.path),
        },
    )


@app.exception_handler(400)
def bad_request_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "statusCode": 400,
            "message": "Bad request",
            "data": None,
            "error": str(exc),
            "path": str(request.url.path),
        },
    )


@app.exception_handler(403)
def forbidden_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=403,
        content={
            "statusCode": 403,
            "message": "Forbidden",
            "data": None,
            "error": str(exc),
            "path": str(request.url.path),
        },
    )


app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(site.router)
app.include_router(site_member.router)
from app.routers import work_item