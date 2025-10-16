from typing import List

from mistralai import Dict


class ResponseAgent:
    def __init__(self, chat_model):
        self.chat_model = chat_model

    def format_chunks(self, chunks: List[Dict]) -> str:
        return "\n\n".join([f"[{c['chunk_id']}] {c['text']}" for c in chunks])

    def generate_answer(self, query: str, chunks: List[Dict]) -> str:
        context = self.format_chunks(chunks)
        prompt = f"""You are a helpful assistant. Use the following chunks to answer the question. Cite sources using [chunk_id].

Question: {query}

Chunks:
{context}
"""
        return self.chat_model.chat(prompt)
