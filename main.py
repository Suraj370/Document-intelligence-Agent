from agents.chunk_embedder import ChunkEmbedderAgent
from agents.hybrid_retreiver import HybridRetriever
from agents.neo4j_ingestor import Neo4jIngestionAgent
from agents.parser import DocumentParserAgent
from dotenv import load_dotenv

load_dotenv()


def main():
    print("Hello from doc-intelligence-agent!")
    parser = DocumentParserAgent("sample_pdf.pdf")
    result = parser.run()
    embedder = ChunkEmbedderAgent(source_id=result["metadata"]["source"])
    chunked_embeddings = embedder.run(result["text"])

    neo4j_agent = Neo4jIngestionAgent()
    neo4j_agent.ingest_chunks(chunked_embeddings)
    neo4j_agent.link_sequential_chunks(chunked_embeddings)
    
    retriever = HybridRetriever(embedder=embedder, neo4j_driver=neo4j_agent)
    results = retriever.retrieve("What is the context of the document?", chunked_embeddings)

    # Step 5: Print results
    print("\nTop Retrieved Chunks:")
    for r in results:
        print(f"{r['chunk_id']}: {r['text']}")
    


if __name__ == "__main__":
    main()
