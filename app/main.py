from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.encoders import jsonable_encoder
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
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=422,
        content={
            "statusCode": 422,
            "message": "Dữ liệu đầu vào không hợp lệ",
            "data": None,
            "error": jsonable_encoder(exc.errors()),
            "path": str(request.url.path),
        },
    )



@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        headers=exc.headers,
        content={
            "statusCode": exc.status_code,
            "message": str(exc.detail),
            "data": None,
            "error": str(exc.detail),
            "path": str(request.url.path),
        },
    )



app.include_router(health_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(site.router)
app.include_router(site_member.router)
app.include_router(work_item.router)