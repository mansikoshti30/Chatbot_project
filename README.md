# Geospatial Information Chatbot 🌍

> **New here? Start with [START_HERE.md](START_HERE.md) or [QUICKSTART.md](QUICKSTART.md)** ⚡

A FastAPI-based chatbot application that answers questions **ONLY** from a fixed geospatial PDF stored locally. The app uses LangChain, OpenAI embeddings, and FAISS vector database for intelligent question answering.

## Features

- 📄 Loads and processes a local geospatial PDF
- 🔍 Extracts text using PyMuPDF
- 📊 Creates embeddings using OpenAI
- 🗄️ Stores embeddings in FAISS vector database
- 🤖 Answers questions using GPT-3.5-turbo/GPT-4
- ⚡ Caching to avoid reprocessing
- 🎨 Clean, modern web interface
- 🚀 Fast REST API with FastAPI

## Prerequisites

- Python 3.8 or higher
- OpenAI API key

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd Chatbot_project
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set OPENAI_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

4. Create a `data` directory and place your PDF file:
```bash
mkdir data
# Copy your geospatial_book.pdf to the data directory
```

## Usage

Run the FastAPI server:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload
```

The app will:
1. Start the server on http://localhost:8000
2. Load and process the PDF at startup (cached for performance)
3. Create embeddings and build the FAISS vector store
4. Serve a web interface to ask questions
5. Answer questions based **ONLY** on the PDF content

Open your browser and navigate to:
- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## Project Structure

```
Chatbot_project/
├── app.py              # Main FastAPI application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── QUICKSTART.md      # Quick start guide
├── test_api.py        # API testing script
├── .gitignore         # Git ignore rules
└── data/
    └── geospatial_book.pdf  # Your PDF file (not included)
```

## API Endpoints

### GET `/`
Serves the web interface

### GET `/health`
Check system status
- Returns `{"status": "ready"}` when system is initialized
- Returns `{"status": "not_ready"}` if still loading

### POST `/ask`
Answer a question
- **Request Body**: `{"question": "your question here"}`
- **Response**: `{"answer": "the answer", "status": "success"}`

## How It Works

1. **PDF Loading**: Uses PyMuPDF to extract all text from the PDF at startup
2. **Text Chunking**: Splits text into 1000-character chunks with 200-character overlap
3. **Embeddings**: Creates embeddings using OpenAI's embedding model
4. **Vector Store**: Stores embeddings in FAISS for fast similarity search
5. **Question Answering**: Uses RetrievalQA chain to answer questions based on retrieved context
6. **Response Filtering**: Ensures answers come only from the PDF content
7. **REST API**: FastAPI serves both the web interface and API endpoints

## Configuration

You can modify the following parameters in `app.py`:

- **PDF Path**: Change `PDF_PATH` to point to your PDF file
- **Chunk Size**: Modify `chunk_size` in `create_text_chunks()` (default: 1000)
- **Chunk Overlap**: Modify `chunk_overlap` in `create_text_chunks()` (default: 200)
- **Model**: Change `model_name` in `get_qa_chain()` (default: "gpt-3.5-turbo")
- **Retrieval Count**: Modify `k` in `as_retriever()` (default: 3 chunks)

## Notes

- The app caches the vector store to avoid reprocessing the PDF on every run
- If the PDF doesn't contain relevant information, the bot responds with: "No relevant answer found in the document."
- The app uses `gpt-3.5-turbo` by default. You can switch to `gpt-4` for better answers (higher cost)

## Troubleshooting

**Error: "OPENAI_API_KEY environment variable is not set"**
- Make sure you've set the environment variable before running the app
- The server will start but won't be able to answer questions

**Error: "PDF file not found"**
- Ensure your PDF file is in the `data/` directory
- Check that the filename matches `PDF_PATH` in `app.py`
- The server will start but system status will be "not_ready"

**Poor answer quality**
- Try increasing the number of retrieved chunks (modify `k` parameter in `get_qa_chain()`)
- Consider using GPT-4 instead of GPT-3.5-turbo
- Adjust chunk size and overlap for better context

**Server won't start**
- Check if port 8000 is already in use
- Try a different port: `uvicorn app:app --port 8080`

## 📚 Additional Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick setup guide with examples
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Detailed system architecture and data flow
- **[SUMMARY.md](SUMMARY.md)** - Complete project summary and features
- **[test_api.py](test_api.py)** - API testing examples
- **[run.ps1](run.ps1)** - PowerShell script to run the app

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## License

MIT License
