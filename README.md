# DeepRead RAG Service

### [Non-local version]

___
Async RAG (Retrieval-Augmented Generation) service built with
FastAPI, PostgreSQL, Redis, Qdrant. Designed to work with OpenRouter-compatible models.
---

## Features

The service allows users to:

- Create and manage users;
- Create document collections;
- Upload and process text documents:
    - split text into semantic chunks;
    - generate embeddings;
    - store vectors and metadata in Qdrant;
- Vector and metadata storage with Qdrant;
- Context retrieval for RAG workflows;
- Question answering over uploaded documents.

With default settings, the service works fully non-locally using OpenRouter models.

---

## Stack

- Python 3.12
- FastAPI
- Pydantic
- PostgreSQL
- SQLAlchemy Async
- Alembic
- Redis
- Qdrant
- LangChain
- Docker Compose
- Black
- Ruff
- MyPy
- Pre-commit

---

## Getting Started

To run project locally:

1. Clone repository:
```shell
git clone https://github.com/AlexandrSmolyachkovGH/deep_read_rag_outer.git
```
2. Create .env file:

```shell
cp .env_example .env
```

3. Configure OpenRouter API key:
  - Create an OpenRouter account;
  - Generate an API key;
  - Set this key as `OPENROUTER_API_KEY` in the `.env` file;

4. Start infrastructure services:
```shell
docker compose up -d
```

5. Run the application locally:
```shell
uvicorn app.main:app --reload
```


