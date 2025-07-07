# 🛒 Mini Store QA Demo with Ollama + Chroma + FastAPI

This is a simple proof-of-concept app that demonstrates how to build a question-answering system for a product catalog using:

✅ **Ollama** (local LLM server)  
✅ **ChromaDB** (vector database)  
✅ **FastAPI** (REST API)  
✅ **Docker Compose** (orchestration)

## 🚀 What does it do?

- Loads a JSON file with ~50 sample products (clothing, accessories, etc.).
- Indexes product information as embeddings in Chroma.
- Exposes a FastAPI endpoint to receive user questions about the products.
- On each question:
  1. Chroma filters products related to the query.
  2. Context of top results is passed to Ollama.
  3. Ollama generates a natural language answer.

All wrapped in a containerized environment so you can spin it up easily.

## 📂 Project structure

```
app/
  ├── chroma_utils.py      # Functions for indexing and searching products in Chroma
  ├── main.py              # FastAPI server with endpoints
  ├── ollama_utils.py      # Code to send prompts to Ollama and handle responses
  └── schemas.py           # Pydantic schemas for FastAPI

docker-compose.yml         # Docker orchestration for Ollama + FastAPI
Dockerfile                 # Build FastAPI app container
requirements.txt           # Python dependencies
products.json             # Product dataset (JSON with 50 products)
```

## 🐳 How to run it

1. Clone the repo:
   ```bash
   git clone https://github.com/guduchango/mini-store-qa-demo.git
   cd mini-store-qa-demo
   ```

2. Build and start the services:
   ```bash
   docker compose up --build
   ```

3. Download ia in the ollama container:
   ```bash
   docker exec -it ollama-chroma-v1-ollama-1 /bin/sh
   ollama pull deepseek-llm
   ollama pull llama-2-7b-chat
   ```

4. Once the containers are up, FastAPI will be accessible on:
   ```
   http://localhost:8001
   ```

5. Check health endpoint to confirm everything is running:
   ```bash
   curl http://localhost:8001/health
   ```

6. Test the `/query` endpoint (example with curl):
   ```bash
   curl -X POST -H "Content-Type: application/json"    -d '{"ask": "I need comfortable clothes for lounging at home, what do you suggest?"}'    http://localhost:8001/query
   ```

## 📝 Requirements

The Python environment (inside the Docker container) uses:
```
chromadb
sentence-transformers
requests
fastapi
uvicorn
```

## 🪵 Logs

You can see detailed logs for the app and Ollama directly in your terminal when you run:
```bash
docker compose up
```

Logs include:
- Product indexing info.
- Incoming queries.
- Chroma search results.
- Prompts sent to Ollama.
- Responses generated.

## ✨ Notes

- Ollama is installed as a service in Docker; it serves your local LLM (e.g., TinyLlama).
- Chroma stores vectors in a persistent volume (`app_chroma_data`) so you don’t need to re-index products each time.

---
