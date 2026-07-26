<div align="center">

# NexusAI

### Self-Hosted AI Knowledge Assistant & Research Engine

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat-square&logo=fastapi&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-14-000000?style=flat-square&logo=next.js&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-latest-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-vector--store-FF6B35?style=flat-square)

**Ingest local documents and GitHub repositories. Query them with a Gemini-powered AI assistant that always cites its sources.**

[Features](#features) · [Architecture](#architecture) · [Getting Started](#getting-started) · [API Reference](#api-reference) · [Configuration](#configuration)

</div>

---

## Overview

NexusAI is a full-stack Retrieval-Augmented Generation (RAG) platform built for engineering teams and developers. It addresses a key weakness of standard RAG systems — poor performance on technical codebases — by combining **semantic vector search** with **keyword-based BM25 search**, merged through **Reciprocal Rank Fusion (RRF)**.

The result is a knowledge assistant that excels at both conceptual questions ("how does this service work?") and precise technical lookups ("find all usages of `auth_middleware`").

---

## Features

- **Hybrid Retrieval** — ChromaDB vector search + BM25 keyword search fused via RRF for superior accuracy on technical content
- **Document Ingestion** — Upload PDFs, Markdown, and plain text files
- **GitHub Indexing** — Point to any public repository URL to index its codebase
- **Persistent Sessions** — Multi-turn conversation history stored in SQLite (WAL mode)
- **Source Citations** — Every AI response links back to the exact source chunks it used
- **Stateful Workflow** — LangGraph orchestrates a multi-step Query → Retrieve → Generate → Persist pipeline
- **Self-Hosted** — All data stays local; no external vector DB required

---

## Architecture

```
                        ┌─────────────────────────────────────────┐
                        │               User Query                 │
                        └──────────────────┬──────────────────────┘
                                           │
                          ┌────────────────┴────────────────┐
                          ▼                                  ▼
               ┌──────────────────┐              ┌──────────────────┐
               │  ChromaDB Vector │              │   BM25 Keyword   │
               │  Search          │              │   Search         │
               │  (semantic)      │              │   (lexical)      │
               └────────┬─────────┘              └────────┬─────────┘
                        │                                  │
                        └────────────────┬─────────────────┘
                                         ▼
                              ┌──────────────────┐
                              │  Reciprocal Rank  │
                              │  Fusion (RRF)     │
                              └────────┬──────────┘
                                       ▼
                              ┌──────────────────┐
                              │   Top-K Chunks   │
                              └────────┬──────────┘
                                       ▼
                              ┌──────────────────┐
                              │   Gemini LLM     │
                              └────────┬──────────┘
                                       ▼
                              ┌──────────────────┐
                              │  Answer + Sources │
                              └──────────────────┘
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Next.js 14, React 18, Tailwind CSS | Responsive chat UI with citation badges and ingestion drawer |
| **Backend API** | Python 3.11, FastAPI, Uvicorn | Async REST endpoints for chat, uploads, and repo indexing |
| **AI Orchestration** | LangGraph, LangChain | Stateful multi-step execution graph |
| **Vector Store** | ChromaDB | Dense semantic embeddings and similarity search |
| **Keyword Search** | rank-bm25 | Sparse lexical search for exact code symbols and terms |
| **Score Fusion** | Reciprocal Rank Fusion | Unified ranking from both retrieval strategies |
| **Persistence** | SQLite (WAL mode) | High-concurrency session and message history storage |
| **LLM** | Google Gemini | Answer generation with source-grounded prompting |

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- A free Google Gemini API key from [Google AI Studio](https://aistudio.google.com/)

### 1. Clone the Repository

```bash
git clone https://github.com/Priyanshusoni7/NexusAI.git
cd NexusAI
```

### 2. Backend Setup

```bash
cd backend

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # macOS / Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
```

Open `.env` and add your Gemini API key:
```env
GOOGLE_API_KEY=your_actual_api_key_here
```

### 3. Frontend Setup

```bash
cd ../frontend
npm install
cp .env.example .env
```

### 4. Run the Application

Open two terminal windows:

**Terminal 1 — Backend API:**
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd frontend
npm run dev
```

Open **[http://localhost:3000](http://localhost:3000)** in your browser.

---

## API Reference

| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/chat` | Send a message and receive an AI response with citations |
| `GET` | `/sessions` | List all chat sessions |
| `GET` | `/sessions/{id}/messages` | Retrieve message history for a session |
| `POST` | `/upload` | Upload a PDF, Markdown, or text file for indexing |
| `POST` | `/ingest/github` | Index a public GitHub repository by URL |
| `GET` | `/documents` | List all ingested documents |
| `DELETE` | `/documents/{name}` | Remove a document and its indexed chunks |

Interactive API docs available at **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)** when the backend is running.

---

## Configuration

### `backend/.env`

```env
# Required — get a free key at https://aistudio.google.com/
GOOGLE_API_KEY=your_gemini_api_key

# Model selection
GEMINI_MODEL=gemini-2.0-flash

# Server
HOST=127.0.0.1
PORT=8000

# Storage (auto-created on first run)
DATABASE_PATH=./nexus.db
CHROMA_DB_DIR=./chroma_db
```

### `frontend/.env`

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

---

## Project Structure

```
NexusAI/
├── backend/
│   ├── api/
│   │   └── routes.py          # FastAPI route definitions
│   ├── db/
│   │   └── database.py        # SQLite schema and query helpers
│   ├── graph/
│   │   └── workflow.py        # LangGraph RAG pipeline
│   ├── services/
│   │   ├── hybrid_retriever.py  # ChromaDB + BM25 + RRF fusion
│   │   └── ingestion.py         # Document and GitHub indexing
│   ├── config.py              # Settings loaded from .env
│   ├── main.py                # FastAPI app entry point
│   └── requirements.txt
└── frontend/
    └── app/
        ├── page.js            # Main chat interface
        ├── layout.js          # Root layout
        └── globals.css        # Global styles
```

---

