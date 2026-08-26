from datetime import datetime

from fastapi import APIRouter, status

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    summary="Kiểm tra trạng thái API",
    description="Kiểm tra API có đang hoạt động hay không.",
    response_model=dict,
    status_code=status.HTTP_200_OK,
)
def health_check():
    return {
        "statusCode": 200,
        "message": "API is healthy",
        "data": {
            "status": "ok",
            "timestamp": datetime.utcnow(),
        },
        "error": None,
    }
