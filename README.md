# 🧠 Agentic Document Intelligence System

A modular, agentic platform for intelligent document understanding. It parses documents, embeds chunks using Mistral, stores them in a Neo4j graph, and retrieves context using hybrid semantic + graph traversal. Designed for recruiter visibility, demoability, and real-world utility.

---

## 🧠 Architecture Diagram

```
────────────────────────────┐
│ sample_pdf.pdf │
└────────────┬───────────────┘
             │
 ┌──────────▼──────────┐
│ DocumentParserAgent │
└──────────┬──────────┘
            │
 ┌──────────▼──────────┐
│ ChunkEmbedderAgent│
← Mistral Embeddings ]
└──────────┬──────────┘
            │
 ┌──────────▼──────────┐
│ Neo4jIngestionAgent │
← Stores chunks as nodes
 └──────────┬──────────┘
│ ┌──────────▼──────────┐
│ HybridRetriever       │
← Cosine + Graph traversal
 └──────────┬──────────┘ │
 ┌──────────▼──────────┐
│ ResponseAgent        │
   ← Mistral Chat (citations)
└─────────────────────┘
````


---

## 🧩 Agents Breakdown

| Agent                | Purpose                                                                 |
|---------------------|-------------------------------------------------------------------------|
| `DocumentParserAgent` | Parses PDF and extracts clean text chunks                              |
| `ChunkEmbedderAgent`  | Embeds chunks using Mistral embedding API                              |
| `Neo4jIngestionAgent` | Stores chunks as nodes and links them sequentially in Neo4j            |
| `HybridRetriever`     | Retrieves relevant chunks using cosine similarity + graph expansion    |
| `ResponseAgent`       | Formats chunks and prompts Mistral chat for citation-aware answers     |

---

## 🛠️ Setup

1. **Install dependencies**

```bash
uv init
uv add
```
Set environment variables

Create a .env file:
```bash

NEO4J_URI=neo4j+s://your-neo4j-uri
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-password
MISTRAL_API_KEY=your-mistral-key

```
