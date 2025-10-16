from agents.chunk_embedder import ChunkEmbedderAgent
from agents.parser import DocumentParserAgent
from dotenv import load_dotenv

load_dotenv()


def main():
    print("Hello from doc-intelligence-agent!")
    parser = DocumentParserAgent("sample_pdf.pdf")
    result = parser.run()
    embedder = ChunkEmbedderAgent(source_id=result["metadata"]["source"])
    chunked_embeddings = embedder.run(result["text"])

    print(chunked_embeddings[0])
    


if __name__ == "__main__":
    main()
