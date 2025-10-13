# Architecture Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Web Browser (http://localhost:8000)                     │  │
│  │  - Beautiful gradient UI                                 │  │
│  │  - Question input box                                    │  │
│  │  - Get Answer button                                     │  │
│  │  - Real-time status indicator                            │  │
│  │  - Answer display area                                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ HTTP Requests
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI SERVER (Port 8000)                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Endpoints:                                              │  │
│  │  • GET  /         → Serve HTML interface                │  │
│  │  • GET  /health   → System status check                 │  │
│  │  • POST /ask      → Answer questions                     │  │
│  │  • GET  /docs     → API documentation                    │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LANGCHAIN QA PIPELINE                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  RetrievalQA Chain                                       │  │
│  │  ┌────────────┐    ┌──────────┐    ┌───────────────┐   │  │
│  │  │  Question  │ ─→ │ Retriever│ ─→ │ GPT-3.5-turbo │   │  │
│  │  │  Input     │    │(FAISS)   │    │ (OpenAI)      │   │  │
│  │  └────────────┘    └──────────┘    └───────────────┘   │  │
│  │                           │                │             │  │
│  │                           ▼                ▼             │  │
│  │                    Top 3 Chunks    Generate Answer      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    VECTOR DATABASE (FAISS)                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Cached in Memory (@lru_cache)                          │  │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐       │  │
│  │  │Chunk 1 │  │Chunk 2 │  │Chunk 3 │  │Chunk N │  ...  │  │
│  │  │+Vector │  │+Vector │  │+Vector │  │+Vector │       │  │
│  │  └────────┘  └────────┘  └────────┘  └────────┘       │  │
│  │  Fast similarity search using embeddings                │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                             │ Built from
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    PDF PROCESSING PIPELINE                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │  Startup Sequence (Runs Once)                           │  │
│  │                                                           │  │
│  │  1. Load PDF (PyMuPDF/fitz)                             │  │
│  │     data/geospatial_book.pdf → Raw Text                 │  │
│  │                                                           │  │
│  │  2. Text Chunking                                        │  │
│  │     Raw Text → 1000-char chunks (200 overlap)           │  │
│  │                                                           │  │
│  │  3. Create Embeddings (OpenAI)                          │  │
│  │     Text Chunks → Vector Embeddings                      │  │
│  │                                                           │  │
│  │  4. Build FAISS Index                                    │  │
│  │     Vector Embeddings → Searchable Database             │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Question to Answer

```
User Question
     │
     ▼
"What is remote sensing?"
     │
     ▼
┌─────────────────────┐
│  Enhanced Question  │  ← Add instruction to answer from PDF only
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Create Embedding   │  ← OpenAI Embeddings API
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  FAISS Search       │  ← Find top 3 similar chunks
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Retrieved Chunks   │  ← Context from PDF
│  • Chunk 47: "..."  │
│  • Chunk 128: "..." │
│  • Chunk 93: "..."  │
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  GPT-3.5-turbo      │  ← Generate answer from context
└─────────────────────┘
     │
     ▼
┌─────────────────────┐
│  Final Answer       │  ← "Remote sensing is..."
└─────────────────────┘
     │
     ▼
Display to User
```

---

## Component Details

### 1. Frontend (Embedded HTML)
- Pure HTML/CSS/JavaScript
- No external dependencies
- Embedded in FastAPI response
- Beautiful gradient design
- Responsive layout

### 2. FastAPI Server
- Async/await support
- Auto-generated OpenAPI docs
- Pydantic data validation
- Error handling middleware
- CORS ready (if needed)

### 3. LangChain Integration
- RetrievalQA chain
- Customizable prompts
- Source tracking (optional)
- Multiple retrievers support
- Chain of thought reasoning

### 4. FAISS Vector Store
- In-memory storage
- Fast cosine similarity
- Efficient indexing
- CPU-optimized
- Scalable to millions of vectors

### 5. OpenAI APIs
- Embeddings: text-embedding-ada-002
- LLM: gpt-3.5-turbo (or gpt-4)
- Temperature: 0 (deterministic)
- Max tokens: default
- Streaming: not enabled

### 6. PDF Processing
- PyMuPDF (fitz) library
- Page-by-page extraction
- Text cleaning
- Metadata preservation
- Error handling

---

## Performance Characteristics

### Startup Time
- PDF loading: ~1-3 seconds
- Text chunking: ~0.5-1 second
- Embedding creation: ~10-30 seconds (depends on PDF size)
- FAISS indexing: ~1-2 seconds
- **Total: ~15-40 seconds**

### Query Time
- Embedding creation: ~0.5 seconds
- FAISS search: ~0.01 seconds
- LLM generation: ~2-5 seconds
- **Total: ~3-6 seconds per query**

### Memory Usage
- Base application: ~100-200 MB
- FAISS index: ~10-50 MB (depends on PDF size)
- LangChain overhead: ~50-100 MB
- **Total: ~200-400 MB**

---

## Scalability Considerations

### Current Setup (Single Server)
- ✅ Good for: 1-100 concurrent users
- ✅ PDF size: Up to ~100 MB
- ✅ Queries: ~10-20 per second

### To Scale Further:
1. **Load Balancer** - Multiple FastAPI instances
2. **Redis Cache** - Cache common questions
3. **Persistent FAISS** - Save index to disk
4. **Async Processing** - Background job queue
5. **CDN** - Serve static content
6. **Database** - Store Q&A history
7. **Monitoring** - Prometheus + Grafana

---

## Security Layers

### API Key Management
- Environment variables (not hardcoded)
- Never exposed to client
- Server-side only

### Input Validation
- Pydantic models
- Type checking
- Length limits
- Sanitization

### Error Handling
- Try-catch blocks
- User-friendly messages
- No stack traces to client
- Logging for debugging

### Future Enhancements
- Rate limiting
- Authentication/Authorization
- HTTPS/TLS
- CORS configuration
- Input sanitization
- SQL injection prevention (if adding DB)

---

## Technology Stack

```
┌──────────────────────────────────────┐
│  Frontend                             │
│  • HTML5                              │
│  • CSS3 (Flexbox, Gradients)         │
│  • Vanilla JavaScript (ES6+)         │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Backend Framework                    │
│  • FastAPI 0.109.0                   │
│  • Uvicorn 0.27.0 (ASGI Server)      │
│  • Pydantic 2.5.3 (Validation)       │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  AI/ML Layer                         │
│  • LangChain 0.1.9                   │
│  • LangChain-OpenAI 0.0.5            │
│  • LangChain-Community 0.0.20        │
│  • OpenAI 1.12.0                     │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Vector Database                      │
│  • FAISS-CPU 1.7.4                   │
│  • NumPy (dependency)                │
└──────────────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────┐
│  Document Processing                  │
│  • PyMuPDF 1.23.26                   │
│  • Tiktoken 0.5.2 (tokenization)     │
└──────────────────────────────────────┘
```

---

This architecture provides a robust, scalable, and maintainable solution for PDF-based question answering!
