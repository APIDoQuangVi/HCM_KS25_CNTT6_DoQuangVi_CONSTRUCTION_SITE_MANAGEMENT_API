from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.database import Base, engine
from app.models import user, site, site_member, work_item
from app.routers.health import router as health_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
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
async def not_found_exception_handler(request: Request, exc):
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
async def bad_request_exception_handler(request: Request, exc):
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
async def forbidden_exception_handler(request: Request, exc):
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
