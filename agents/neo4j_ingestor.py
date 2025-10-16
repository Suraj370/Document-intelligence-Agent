from neo4j import GraphDatabase
from typing import List, Dict
import os

class Neo4jIngestionAgent:
    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def ingest_chunks(self, chunks: List[Dict]):
        with self.driver.session() as session:
            for chunk in chunks:
                session.run(
                    """
                    MERGE (c:Chunk {chunk_id: $chunk_id})
                    SET c.text = $text,
                        c.source_id = $source_id,
                        c.position = $position,
                        c.embedding = $embedding
                    """,
                    chunk
                )

    def link_sequential_chunks(self, chunks: List[Dict]):
        with self.driver.session() as session:
            for i in range(len(chunks) - 1):
                session.run(
                    """
                    MATCH (a:Chunk {chunk_id: $from_id})
                    MATCH (b:Chunk {chunk_id: $to_id})
                    MERGE (a)-[:NEXT]->(b)
                    """,
                    {
                        "from_id": chunks[i]["chunk_id"],
                        "to_id": chunks[i + 1]["chunk_id"]
                    }
                )

    def expand_chunks(self, chunk_ids: List[str]) -> List[Dict]:
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (c:Chunk)-[:NEXT]->(n:Chunk)
                WHERE c.chunk_id IN $ids
                RETURN n.chunk_id AS chunk_id,
                       n.text AS text,
                       n.source_id AS source_id,
                       n.position AS position,
                       n.embedding AS embedding
                """,
                {"ids": chunk_ids}
            )
            return [record.data() for record in result]
