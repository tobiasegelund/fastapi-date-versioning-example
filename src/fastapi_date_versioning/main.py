import datetime
import typing as t

import fastapi
from fastapi import HTTPException
from dotenv import load_dotenv

from fastapi_date_versioning.schemas import RequestInput, ResponseOutput
from fastapi_date_versioning.api.home import API_VERSIONS as home_versions
from fastapi_date_versioning.logger import logger

load_dotenv()


app = fastapi.FastAPI(
    title="FastAPI Date Versioning",
)


def get_fn_version(
    version: datetime.date, API_VERSIONS: dict[datetime.date, t.Callable]
) -> t.Callable:
    for date in sorted(API_VERSIONS.keys(), reverse=True):
        if version >= date:
            logger.info(f"Using version {date}")
            return API_VERSIONS[date]

    raise HTTPException(status_code=500, detail=f"Version {version} is not supported")


# For GET requests: ?v=20200630
@app.post("/", response_model=ResponseOutput)
async def home(request: RequestInput) -> ResponseOutput:
    fn = get_fn_version(request.version, home_versions)
    return fn(request)
