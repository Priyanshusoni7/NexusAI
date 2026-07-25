# NexusAI — Self-Hosted AI Knowledge Assistant

A full-stack RAG (Retrieval-Augmented Generation) platform that turns your local documents and GitHub repositories into a queryable AI knowledge base.

Built with **FastAPI · LangGraph · ChromaDB · BM25 · Next.js**

---

## How It Works

```
User Query
    │
    ├── ChromaDB (semantic vector search)
    └── BM25 (keyword search)
            │
         RRF Fusion (Reciprocal Rank Fusion)
            │
         Top-K Chunks → Gemini LLM → Answer + Citations
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 14, React, Tailwind CSS |
| Backend API | Python 3.11+, FastAPI, Uvicorn |
| AI Orchestration | LangGraph, LangChain |
| Vector Search | ChromaDB |
| Keyword Search | BM25 (rank-bm25) |
| LLM | Google Gemini (via API) |
| Database | SQLite (WAL mode) |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- Google Gemini API key → [Get one free](https://aistudio.google.com/)

### 1. Clone the repo
```bash
git clone https://github.com/Priyanshusoni7/NexusAI.git
cd NexusAI
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate        # Windows
# source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt

cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 3. Frontend setup
```bash
cd ../frontend
npm install
cp .env.example .env
```

### 4. Run the project

**Terminal 1 — Backend:**
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

Open **http://localhost:3000** in your browser.

---

## Features

- **Upload documents** — PDF, Markdown, plain text
- **Index GitHub repos** — point to any public repo URL
- **Hybrid search** — semantic + keyword merged with RRF
- **Persistent chat sessions** — conversation history stored in SQLite
- **Source citations** — every answer links back to its source chunks

---

## Environment Variables

### `backend/.env`
```env
GOOGLE_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.0-flash
HOST=127.0.0.1
PORT=8000
DATABASE_PATH=./nexus.db
CHROMA_DB_DIR=./chroma_db
```

### `frontend/.env`
```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

---

## License

MIT
