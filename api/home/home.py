from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.analytics.schemas import ResponseBaseModel

from core.fastapi.dependencies import PermissionDependency, AllowAll

home_router = APIRouter()


@home_router.get("/health-check", response_model=ResponseBaseModel, dependencies=[Depends(PermissionDependency([AllowAll]))])
async def health_check():
    return JSONResponse({"success": True, "message": "OK"}, status_code=200)
