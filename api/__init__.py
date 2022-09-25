from fastapi import APIRouter

from api.analytics.v1.analytics import analytics_router as analytics_v1_router

router = APIRouter()
router.include_router(analytics_v1_router, prefix="/api/v1/analytics", tags=["Analytics"])

__all__ = ["router"]
