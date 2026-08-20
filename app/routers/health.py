from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check():
    return {
        "statusCode": 200,
        "message": "API is healthy",
        "data": {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
        },
        "error": None,
    }
