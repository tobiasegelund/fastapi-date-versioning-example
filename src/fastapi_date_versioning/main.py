"""Example to show how to use date versioning in FastAPI.

POST requests: payload should be a JSON object with a "version" key.
GET requests: query parameter "v"/"version" should be provided, e.g. ?v=20200630
"""

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
    """Get the function version based on the date.

    It will traverse through dates in descending order and return the first version. If no version
    is found (date specified prior to first version), it will raise an HTTPException.

    Args:
        version (datetime.date): The version date.
        API_VERSIONS (dict[datetime.date, t.Callable]): The API versions.
    """
    for date in sorted(API_VERSIONS.keys(), reverse=True):
        if version >= date:
            logger.info(f"Using version {date}")
            return API_VERSIONS[date]

    raise HTTPException(status_code=500, detail=f"Version {version} is not supported")


@app.post("/", response_model=ResponseOutput)
async def home(request: RequestInput) -> ResponseOutput:
    fn = get_fn_version(request.version, home_versions)
    return fn(request)
