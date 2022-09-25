from typing import List

from fastapi import FastAPI, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi_utils.tasks import repeat_every
import requests, json

import os
from dotenv import load_dotenv

load_dotenv()

from hubspot import HubSpot

from api import router
from api.home.home import home_router
from core.config import config
from core.exceptions import CustomException
from core.fastapi.dependencies import Logging
from core.fastapi.middlewares import (
    AuthenticationMiddleware,
    AuthBackend,
    SQLAlchemyMiddleware,
)
from core.helpers.cache import Cache, RedisBackend, CustomKeyMaker


def init_routers(app_: FastAPI) -> None:
    app_.include_router(home_router)
    app_.include_router(router)


def init_listeners(app_: FastAPI) -> None:
    # Exception handler
    @app_.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        return JSONResponse(
            status_code=exc.code,
            content={"error_code": exc.error_code, "message": exc.message},
        )


def on_auth_error(request: Request, exc: Exception):
    status_code, error_code, message = 401, None, str(exc)
    if isinstance(exc, CustomException):
        status_code = int(exc.code)
        error_code = exc.error_code
        message = exc.message

    return JSONResponse(
        status_code=status_code,
        content={"error_code": error_code, "message": message},
    )


def make_middleware() -> List[Middleware]:
    middleware = [
        Middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        ),
        Middleware(
            AuthenticationMiddleware,
            backend=AuthBackend(),
            on_error=on_auth_error,
        ),
        Middleware(SQLAlchemyMiddleware),
    ]
    return middleware


def init_cache() -> None:
    Cache.init(backend=RedisBackend(), key_maker=CustomKeyMaker())


def create_app() -> FastAPI:
    app_ = FastAPI(
        title="Hide",
        description="Hide API",
        version="1.0.0",
        docs_url=None if config.ENV == "production" else "/docs",
        redoc_url=None if config.ENV == "production" else "/redoc",
        dependencies=[Depends(Logging)],
        middleware=make_middleware(),
    )
    init_routers(app_=app_)
    init_listeners(app_=app_)
    init_cache()
    return app_


app = create_app()

@app.on_event("startup")
@repeat_every(seconds=60*60)  # 1 hour
def fetch_updated_analytics() -> None:
    print("Updating Analytics")
    company_list = os.getenv("FAKE_API_DATA_SEED").split(", ")
    comp_analytics = []
    for comp in company_list:
        req = requests.get(f"{os.getenv('PYNE_BACKEND')}/{comp}")
        comp_analytics.append(req.json())
    
    comp_analytics = [item for sublist in comp_analytics for item in sublist]

    api_client = HubSpot(access_token=os.getenv("HS_API_KEY"))
    try:
        all_contacts = api_client.crm.contacts.get_all()
        all_companies = api_client.crm.companies.get_all()
        companies = []
        contacts = []
        for company in all_companies:
            companies.append(jsonable_encoder(company.to_dict()))

        for contact in all_contacts:
            contacts.append(jsonable_encoder(contact.to_dict()))

        with open('hs_company_data.json', 'w') as outfile:
            json.dump(companies, outfile)
        
        with open('hs_contact_data.json', 'w') as outfile:
            json.dump(contacts, outfile)

    except Exception as e:
        print("Exception when requesting contact by id: %s\n" % e)

    with open('analytics_data.json', 'w') as outfile:
        json.dump(comp_analytics, outfile)
