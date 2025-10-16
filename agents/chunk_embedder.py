import uuid
import os
from typing import List, Dict
from langchain.text_splitter import RecursiveCharacterTextSplitter
from mistralai import Mistral


class ChunkEmbedderAgent:
    def __init__(self, source_id: str, chunk_size: int = 500, chunk_overlap: int = 50):
        self.source_id = source_id
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize chunk splitter
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )

        # Initialize Mistral client
        self.client = Mistral(api_key=os.getenv("MISTRAL_API_KEY"))

    def chunk_text(self, text: str) -> List[str]:
        return self.splitter.split_text(text)

    def embed_chunks(self, chunks: List[str]) -> List[Dict]:
        # Call Mistral embedding API
        response = self.client.embeddings.create(
            model="mistral-embed",
            inputs=chunks
        )

        return [
            {
                "chunk_id": str(uuid.uuid4()),
                "source_id": self.source_id,
                "position": i,
                "text": chunk,
                "embedding": item.embedding
            }
            for i, (chunk, item) in enumerate(zip(chunks, response.data))
        ]

    def run(self, text: str) -> List[Dict]:
        chunks = self.chunk_text(text)
        return self.embed_chunks(chunks)
