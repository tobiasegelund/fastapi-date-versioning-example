"""Example to show how to use date versioning in FastAPI.

POST requests: payload should be a JSON object with a "version" key.
GET requests: query parameter "v"/"version" should be provided, e.g. ?v=20200630
"""

import datetime
import typing as t
from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI
from fastapi import HTTPException, Request
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

from fastapi_date_versioning.schemas import RequestInput, ResponseOutput
from fastapi_date_versioning.api import HOME_API_VERSIONS
from fastapi_date_versioning.logger import logger

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run at startup
    Initialize the Client and add it to request.state
    """
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    app.state.model = model
    yield


app = fastapi.FastAPI(title="FastAPI Date Versioning", lifespan=lifespan)


def get_fn_version(
    version: datetime.date, versions: dict[datetime.date, t.Callable]
) -> t.Callable:
    """Get the function version based on the date.

    It will traverse through dates in descending order and return the first version. If no version
    is found (date specified prior to first version), it will raise an HTTPException.

    Args:
        version (datetime.date): The version date.
        versions (dict[datetime.date, t.Callable]): The API versions.
    """
    for date in sorted(versions.keys(), reverse=True):
        if version >= date:
            logger.info(f"Using version {date}")
            return versions[date]

    raise HTTPException(status_code=500, detail=f"Version {version} is not supported")


@app.post("/", response_model=ResponseOutput)
async def home(inp: RequestInput, req: Request) -> ResponseOutput:
    logger.info(f"endpoint=/ {inp}")

    model = req.app.state.model
    fn = get_fn_version(inp.version, HOME_API_VERSIONS)

    embedding = model.encode([inp.input])
    resp = await fn(inp, embedding)
    return resp
