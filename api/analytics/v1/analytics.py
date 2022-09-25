from datetime import datetime

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from app.analytics.schemas import GetCompanyListResponseSchema, GetCompanyUserListResponseSchema
from app.user.schemas import (
    ExceptionResponseSchema,
)
from app.analytics.services import AnalyticsService

analytics_router = APIRouter()


# /api/v1/analytics/company
@analytics_router.get(
    "/company",
    response_model=GetCompanyListResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_company_list(
):
    result = await AnalyticsService().get_company_list()
    return JSONResponse({"success": True, "message": jsonable_encoder(result)}, status_code=200)

# /api/v1/analytics/company/users
@analytics_router.get(
    "/company/users",
    response_model=GetCompanyUserListResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_company_user_list(
):
    result = await AnalyticsService().get_company_user_list()
    return JSONResponse({"success": True, "message": jsonable_encoder(result)}, status_code=200)

# /api/v1/analytics/company/users/time/{fromDateTime}
@analytics_router.get(
    "/company/users/time",
    response_model=GetCompanyUserListResponseSchema,
    responses={"400": {"model": ExceptionResponseSchema}},
)
async def get_company_user_from_list(
	from_ts: datetime
):
	# TODO - Return with error if timestamp invalid or in the future
    result = await AnalyticsService().get_company_user_from_list(from_ts=from_ts)
    return JSONResponse({"success": True, "message": jsonable_encoder(result)}, status_code=200)
