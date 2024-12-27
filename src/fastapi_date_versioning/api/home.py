import numpy as np

from fastapi_date_versioning.schemas import RequestInput, ResponseOutput
from fastapi_date_versioning.core.search import store


async def hello_version_v1(
    request: RequestInput, embedding: np.ndarray
) -> ResponseOutput:
    subset_df = store.search(vec=embedding, k=request.top_k)
    response = subset_df.to_dict("records")
    return ResponseOutput(output=response)


async def hello_version_v2(
    request: RequestInput, embedding: np.ndarray
) -> ResponseOutput:
    _ = store.search(vec=embedding, k=request.top_k)
    return ResponseOutput(output=[{"question": "one two", "answer": "three four"}])
