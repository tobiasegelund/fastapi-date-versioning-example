import sys
import datetime
import typing as t
import logging

import fastapi
from fastapi import HTTPException

from fastapi_date_versioning.schemas import RequestInput, ResponseOutput


def _create_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create a StreamHandler to output to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)

    # Create a formatter and set it for the handler
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


logger = _create_logger()

app = fastapi.FastAPI(
    title="FastAPI Date Versioning",
)


def hello_version_v1(request: RequestInput) -> ResponseOutput:
    return ResponseOutput(message=f"Hello {request.input}")


def hello_version_v2(request: RequestInput) -> ResponseOutput:
    return ResponseOutput(
        message=f"Hello {request.input}: You reached me at this date {request.version}"
    )


API_VERSION: dict[datetime.date, t.Callable] = {
    datetime.date(2023, 1, 1): hello_version_v1,
    datetime.date(2023, 6, 1): hello_version_v1,
    datetime.date(2024, 1, 1): hello_version_v2,
    datetime.date(2024, 6, 1): hello_version_v2,
}


def get_hello_fn(version: datetime.date) -> t.Callable:
    for date in sorted(API_VERSION.keys(), reverse=True):
        if version >= date:
            logger.info(f"Using version {date}")
            return API_VERSION[date]

    raise HTTPException(status_code=500, detail=f"Version {version} is not supported")


# For GET requests: ?v=20200630


@app.post("/", response_model=ResponseOutput)
async def home(request: RequestInput) -> ResponseOutput:
    version = request.version
    fn = get_hello_fn(version)
    return fn(request)
