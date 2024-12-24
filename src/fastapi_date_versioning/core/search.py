import faiss
import numpy as np


class Search:
    def __init__(self, index_path: str):
        self.index = faiss.read_index(index_path)

    def search(self, query: np.ndarray, k: int) -> list[int]:
        # distance, indices
        _, indices = self.index.search(query, k)
        return indices[0]
