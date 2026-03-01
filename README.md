<div align="center">

# 🤖 AI-Powered Portfolio

<img src="docs/assets/demo.gif" alt="Demo GIF" width="100%" style="border-radius: 8px;" />

> _A portfolio that talks back — RAG-powered AI chat assistant built on FastAPI + React, answering real questions about my experience, skills, and projects._

---

### 🚀 [Live Demo](https://your-demo-url.com) &nbsp;·&nbsp; 📖 [API Docs](http://localhost:8000/docs) &nbsp;·&nbsp; 🐛 [Report Bug](https://github.com/rushikeshxdev/AI-Powered-Portfolio/issues)

---

![Visitors](https://api.visitorbadge.io/api/visitors?path=rushikeshxdev%2FAI-Powered-Portfolio&label=VISITORS&labelColor=%235B2D8E&countColor=%23FF6B6B&style=flat-square)
[![GitHub Stars](https://img.shields.io/github/stars/rushikeshxdev/AI-Powered-Portfolio?style=flat-square&logo=github&labelColor=1a1a2e&color=FFD93D)](https://github.com/rushikeshxdev/AI-Powered-Portfolio/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/rushikeshxdev/AI-Powered-Portfolio?style=flat-square&logo=github&labelColor=1a1a2e&color=6BCB77)](https://github.com/rushikeshxdev/AI-Powered-Portfolio/network/members)
[![GitHub Issues](https://img.shields.io/github/issues/rushikeshxdev/AI-Powered-Portfolio?style=flat-square&labelColor=1a1a2e&color=FF6B6B)](https://github.com/rushikeshxdev/AI-Powered-Portfolio/issues)
[![License: MIT](https://img.shields.io/badge/License-MIT-4D96FF?style=flat-square&labelColor=1a1a2e)](https://opensource.org/licenses/MIT)

![Python](https://img.shields.io/badge/Python_3.11+-3776AB?style=flat-square&logo=python&logoColor=FFD43B)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React_19-61DAFB?style=flat-square&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)

</div>

---

## 📽️ Demo

> **📌 Placeholder** — Replace `docs/assets/demo.gif` with a screen recording of your portfolio in action.
> 
> Recommended tools: [Loom](https://loom.com), [Kap](https://getkap.co/) (macOS), or [ScreenToGif](https://www.screentogif.com/) (Windows)
> 
> Ideal flow to record: open chat → type a question → show streaming response → scroll through portfolio

---

## ✨ What Makes This Different

| Feature | Detail |
|---|---|
| 🧠 **RAG Architecture** | ChromaDB vector store + Sentence Transformers for context-aware answers |
| ⚡ **Real-Time Streaming** | Token-by-token responses via Server-Sent Events |
| 🗄️ **Persistent Sessions** | Full chat history stored in PostgreSQL |
| 🔒 **Production-Ready** | CORS, rate limiting, input validation, HTTPS |
| 📊 **High Performance** | Async FastAPI — handles 100+ concurrent users |

---

## 🏗️ Architecture

```mermaid
graph TB
    A([👤 User]) --> B[⚛️ React Frontend\nTypeScript + Vite]
    B -->|HTTP POST| C[🚀 FastAPI Backend\nAsync Python]
    
    C --> D[🔤 Sentence Transformer\n384-dim Embeddings]
    D --> E[🗄️ ChromaDB\nVector Store]
    E -->|Top-K Context| F[🤖 OpenRouter LLM\nLLaMA 3.1 8B]
    F -->|SSE Stream| B
    
    C --> G[(🐘 PostgreSQL\nChat History)]

    style A fill:#5B2D8E,stroke:#9B59B6,color:#fff
    style B fill:#1a6b8a,stroke:#61DAFB,color:#fff
    style C fill:#00695c,stroke:#009688,color:#fff
    style D fill:#6a1b9a,stroke:#AB47BC,color:#fff
    style E fill:#e65100,stroke:#FF9800,color:#fff
    style F fill:#b71c1c,stroke:#FF6B6B,color:#fff
    style G fill:#1565c0,stroke:#4D96FF,color:#fff
```

### RAG Pipeline — Step by Step

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant FE as ⚛️ Frontend
    participant API as 🚀 FastAPI
    participant DB as 🗄️ ChromaDB
    participant LLM as 🤖 LLM

    U->>FE: Type question
    FE->>API: POST /api/chat
    API->>DB: Embed query → vector search
    DB-->>API: Return top-K context chunks
    API->>LLM: Prompt + context
    LLM-->>FE: Stream tokens (SSE)
    FE-->>U: Real-time response ✨
```

---

## 🛠️ Tech Stack

```
Frontend   →  React 19 · TypeScript 5.9 · Vite 7.3
Backend    →  Python 3.11 · FastAPI 0.109 · SQLAlchemy 2.0
Database   →  PostgreSQL 14+ · Alembic 1.13
AI / ML    →  OpenRouter (LLaMA 3.1 8B) · ChromaDB 0.4 · Sentence Transformers 2.3
DevOps     →  Vercel · Railway · Docker · Pytest
```

---

## ⚡ Quick Start

### Prerequisites
- Node.js 18+ · Python 3.11+ · PostgreSQL 14+
- [OpenRouter API Key](https://openrouter.ai/)

### Backend

```bash
cd backend
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # Add your DATABASE_URL and OPENROUTER_API_KEY

python scripts/init_db.py
uvicorn src.main:app --reload --port 8000
# → API live at http://localhost:8000
# → Swagger docs at http://localhost:8000/docs
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env   # Set VITE_API_URL=http://localhost:8000
npm run dev
# → App live at http://localhost:5173
```

### Environment Variables

<details>
<summary>📋 Click to expand</summary>

**`backend/.env`**
```env
DATABASE_URL=postgresql://user:password@localhost:5432/portfolio
OPENROUTER_API_KEY=your_key_here
CORS_ORIGINS=http://localhost:5173
LOG_LEVEL=INFO
```

**`frontend/.env`**
```env
VITE_API_URL=http://localhost:8000
```
</details>

---

## 📡 API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Health check |
| `POST` | `/api/chat` | Send message → streaming response |
| `GET` | `/api/chat/history/{session_id}` | Fetch session history |

```bash
# Example
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are your Python skills?", "session_id": "abc-123"}'
```

---

## 📊 Performance

```
┌─────────────────────────────────┐
│  API Response Time   < 100ms   │
│  Vector Search       < 50ms    │
│  Concurrent Users    100+      │
│  Test Coverage       85%+      │
│  LLM Streaming       2 – 5s    │
└─────────────────────────────────┘
```

---

## 🧪 Testing

```bash
cd backend && pytest --cov          # Backend — 85%+ coverage
cd frontend && npm run test:coverage # Frontend
```

---

## 📁 Structure

```
AI-Powered-Portfolio/
├── frontend/src/
│   ├── components/    # UI components
│   ├── pages/         # Route pages
│   ├── hooks/         # Custom React hooks
│   └── utils/
├── backend/src/
│   ├── models/        # DB models
│   ├── services/      # RAG + LLM logic
│   ├── repositories/  # Data layer
│   └── main.py
└── docs/assets/       # Screenshots, GIF, diagrams
```

---

## 🚢 Deploy

**Frontend → Vercel**
```bash
cd frontend && vercel --prod
```

**Backend → Railway**
1. Connect repo on [Railway](https://railway.app)
2. Add PostgreSQL plugin
3. Set environment variables
4. Auto-deploys on push ✅

---

<div align="center">

### 📬 Connect

[![Email](https://img.shields.io/badge/rushirandive31@gmail.com-FF6B6B?style=flat-square&logo=gmail&logoColor=white)](mailto:rushirandive31@gmail.com)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat-square&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/rushikeshrandive12/)
[![GitHub](https://img.shields.io/badge/@rushikeshxdev-FFD93D?style=flat-square&logo=github&logoColor=black)](https://github.com/rushikeshxdev)

---

_If this project helped you, drop a ⭐ — it keeps the commits coming._

</div>
