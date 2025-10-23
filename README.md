# Geospatial Information Chatbot 🌍

A FastAPI-based chatbot that answers questions from a PDF document using LangChain, HuggingFace models, and FAISS vector database.

## Features

- 📄 Loads and processes PDF documents locally
- 🔍 Uses HuggingFace models (FREE - no API keys required)
- 🗄️ FAISS vector database for fast retrieval
- 🤖 FLAN-T5 model for question answering
- 💻 Works offline after initial model download
- ⚡ GPU acceleration support (optional)
- 🎨 Clean web interface

## Quick Start

### Option 1: Automated Setup (Recommended)

**For CPU:**
```powershell
.\setup.ps1
.\start_chatbot.bat
```

**For GPU (NVIDIA only):**
```powershell
.\setup.ps1 -GPU
.\start_chatbot.bat
```

### Option 2: Manual Setup

1. **Install Python 3.11** (recommended)

2. **Create virtual environment:**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. **Install dependencies:**
```powershell
pip install -r requirements.txt
```

4. **For GPU support (optional):**
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

7. **Open your browser:** http://localhost:8000

---

## 📁 Project Structure

```
Chatbot_project/
├── app.py                 # Main application
├── requirements.txt       # Dependencies (CPU)
├── requirements-gpu.txt   # GPU-specific packages
├── setup.ps1             # Automated setup script
├── start_chatbot.bat     # Start script
├── README.md             # This file
└── data/
    └── geospatial_book.pdf  # Your PDF file
```

---

## 🔧 System Requirements

**Minimum (CPU Mode):**
- Python 3.11 or 3.12
- 8GB RAM (16GB recommended)
- 5GB free disk space
- Internet (first-time model download only)

**Recommended (GPU Mode):**
- NVIDIA GPU with 6GB+ VRAM
- CUDA 12.1 or higher
- 16GB RAM

---

## 🌐 Usage

After starting the chatbot:
- **Web Interface:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

### API Endpoints

**POST /ask** - Ask a question
```json
{
  "question": "What is geospatial data?"
}
```

**GET /health** - Check server status

---

## ⚙️ Configuration

Edit `app.py` to customize:
- **PDF Path:** Change `PDF_PATH` variable
- **Model:** Switch between `flan-t5-base` and `flan-t5-large`
- **Chunk Size:** Modify in `create_text_chunks()`
- **GPU Usage:** Automatically detected

---

## 🐛 Troubleshooting

**"Python not found"**
- Install Python 3.11 from python.org
- Make sure "Add to PATH" is checked

**"PDF file not found"**
- Place your PDF in `data/geospatial_book.pdf`
- Create the `data` folder if it doesn't exist

**"Port 8000 already in use"**
- Close other applications using port 8000
- Or change port in app.py: `uvicorn.run(app, port=8080)`

**Slow responses (CPU mode)**
- Use GPU mode for 5-10x faster: `.\setup.ps1 -GPU`
- Or switch to smaller model: `flan-t5-base`

---

## 📝 Notes

- First run downloads models (~3GB for flan-t5-large)
- Models are cached locally for offline use
- GPU acceleration is automatic if NVIDIA GPU detected
- Answers are generated only from your PDF content
- No API keys or external services required

---

## 🚀 Performance

**CPU Mode:**
- Startup: 10-30 seconds
- Per answer: 5-15 seconds

**GPU Mode (RTX 3060+):**
- Startup: 10-30 seconds
- Per answer: 1-3 seconds
- Submit pull requests

## License

MIT License
