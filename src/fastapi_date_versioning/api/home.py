import datetime
import typing as t

from fastapi_date_versioning.schemas import RequestInput, ResponseOutput
from fastapi_date_versioning.core.search import store
from fastapi_date_versioning.logger import logger


async def hello_version_v1(request: RequestInput) -> ResponseOutput:
    logger.info(f"{request}")
    subset_df = store.search(query=request.input, k=request.top_k)
    response = subset_df.to_dict("records")
    return ResponseOutput(output=response)


# def hello_version_v2(request: RequestInput) -> ResponseOutput:
#     return ResponseOutput(message=f"Hello, {request.input}! (v2)")


API_VERSIONS: dict[datetime.date, t.Callable] = {
    datetime.date(2023, 6, 1): hello_version_v1,
    # datetime.date(2024, 6, 1): hello_version_v2,
}
