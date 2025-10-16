import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict

def similarity_search(query_vec: List[float], chunk_embeddings: List[List[float]], chunks: List[Dict], top_k: int = 5) -> List[Dict]:
    scores = cosine_similarity([query_vec], chunk_embeddings)[0]
    top_indices = np.argsort(scores)[-top_k:][::-1]
    return [chunks[i] for i in top_indices]

class HybridRetriever:
    def __init__(self, embedder, neo4j_driver):
        self.embedder = embedder
        self.neo4j = neo4j_driver

    def retrieve(self, query: str, chunks: List[Dict]) -> List[Dict]:
        query_vec = self.embedder.embed_query(query)
        chunk_vecs = [c["embedding"] for c in chunks]
        top_chunks = similarity_search(query_vec, chunk_vecs, chunks)
        expanded = self.neo4j.expand_chunks([c["chunk_id"] for c in top_chunks])
        return expanded or top_chunks
