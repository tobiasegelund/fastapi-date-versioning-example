import faiss
import numpy as np
import pandas as pd

from fastapi_date_versioning.constants import (
    PATH_TO_ANSWERS_INDEX,
    PATH_TO_QUESTIONS_INDEX,
    PATH_TO_DATA,
)
from fastapi_date_versioning.logger import logger


class VectorStore:
    def __init__(self):
        self.questions_index = faiss.read_index(PATH_TO_QUESTIONS_INDEX)
        self.answers_index = faiss.read_index(PATH_TO_ANSWERS_INDEX)

        self.df = pd.read_parquet(PATH_TO_DATA)

    def search(self, vec: np.ndarray, k: int) -> pd.DataFrame:
        # distance, indices
        _, indices = self.questions_index.search(vec, k)
        logger.info(f"Indices: {indices}")
        return self.df.iloc[indices[0]]


store = VectorStore()
