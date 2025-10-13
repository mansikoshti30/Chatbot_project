# 🚀 Getting Started - Complete Guide

Welcome! This guide will help you get your Geospatial Information Chatbot up and running in **under 5 minutes**.

---

## ⚡ Quick Start (TL;DR)

```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set API key
$env:OPENAI_API_KEY="sk-your-key-here"

# 3. Add your PDF to data/geospatial_book.pdf

# 4. Run the app
python app.py

# 5. Open browser to http://localhost:8000
```

Done! 🎉

---

## 📋 Detailed Step-by-Step Guide

### Step 1: Prerequisites Check

**Check Python Version:**
```powershell
python --version
# Should be Python 3.8 or higher
```

**Check pip:**
```powershell
pip --version
```

**Get OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Sign in or create account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

---

### Step 2: Clone or Download Project

**Option A: Using Git**
```powershell
git clone https://github.com/mansikoshti30/Chatbot_project.git
cd Chatbot_project
```

**Option B: Already Have Files**
```powershell
cd C:\Users\pradi\OneDrive\Documents\GitHub\Chatbot_project
```

---

### Step 3: Create Virtual Environment (Recommended)

**Create virtual environment:**
```powershell
python -m venv venv
```

**Activate it:**
```powershell
.\venv\Scripts\Activate.ps1
```

You should see `(venv)` in your prompt.

**If you get execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- FastAPI (web framework)
- Uvicorn (server)
- PyMuPDF (PDF processing)
- LangChain (AI orchestration)
- OpenAI (GPT models)
- FAISS (vector database)
- And more...

**Installation takes ~2-5 minutes**

**Verify installation:**
```powershell
python -c "import fastapi, uvicorn, fitz, langchain; print('All packages installed!')"
```

---

### Step 5: Set OpenAI API Key

**Option A: Environment Variable (Temporary - This Session Only)**
```powershell
$env:OPENAI_API_KEY="sk-your-actual-key-here"
```

**Option B: Create .env File (Permanent)**
```powershell
# Copy the example file
Copy-Item .env.example .env

# Edit .env and add your key
notepad .env
```

In `.env` file:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Then install python-dotenv:
```powershell
pip install python-dotenv
```

And add to `app.py` (at the top):
```python
from dotenv import load_dotenv
load_dotenv()
```

**Verify API Key:**
```powershell
echo $env:OPENAI_API_KEY
# Should show your key
```

---

### Step 6: Add Your PDF

**Copy your PDF to the data folder:**
```powershell
# Create data folder if it doesn't exist
New-Item -ItemType Directory -Force -Path data

# Copy your PDF (replace with your actual path)
Copy-Item "C:\path\to\your\geospatial_book.pdf" -Destination "data\geospatial_book.pdf"
```

**Verify PDF exists:**
```powershell
Test-Path data\geospatial_book.pdf
# Should return: True
```

**Check PDF size:**
```powershell
Get-Item data\geospatial_book.pdf | Select-Object Name, Length
```

---

### Step 7: Run the Application

**Option A: Using Python Directly**
```powershell
python app.py
```

**Option B: Using Uvicorn with Auto-Reload**
```powershell
uvicorn app:app --reload
```

**Option C: Using the PowerShell Script**
```powershell
.\run.ps1
```

**You should see:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
Loading PDF...
Processing text chunks...
Building vector database...
Vector store built successfully!
Application initialized successfully!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Startup takes ~15-40 seconds** (one-time processing)

---

### Step 8: Access the Application

**Open your browser and navigate to:**

🌐 **Main Interface**: http://localhost:8000

📚 **API Documentation**: http://localhost:8000/docs

📊 **Alternative Docs**: http://localhost:8000/redoc

💚 **Health Check**: http://localhost:8000/health

---

### Step 9: Test the Chatbot

**In the Web Interface:**
1. Type a question: "What is remote sensing?"
2. Click "Get Answer"
3. Wait 3-5 seconds
4. See the answer!

**Example Questions to Try:**
- "What is GIS?"
- "Explain satellite imagery"
- "What are the types of map projections?"
- "How does GPS work?"
- "What is spatial analysis?"

---

### Step 10: Test the API (Optional)

**Open a new terminal** and try:

**Health Check:**
```powershell
curl http://localhost:8000/health
```

**Ask a Question:**
```powershell
curl -X POST http://localhost:8000/ask `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What is GIS?\"}'
```

**Or use the test script:**
```powershell
python test_api.py
```

---

## 🎯 Common Issues & Solutions

### Issue 1: "OPENAI_API_KEY not set"

**Solution:**
```powershell
$env:OPENAI_API_KEY="your-key-here"
python app.py
```

---

### Issue 2: "PDF file not found"

**Check if file exists:**
```powershell
ls data\
```

**If missing, add it:**
```powershell
Copy-Item "C:\path\to\your\pdf.pdf" -Destination "data\geospatial_book.pdf"
```

---

### Issue 3: "Import errors"

**Reinstall dependencies:**
```powershell
pip uninstall -y -r requirements.txt
pip install -r requirements.txt
```

---

### Issue 4: "Port 8000 already in use"

**Option A: Use different port:**
```powershell
uvicorn app:app --port 8080
```

**Option B: Kill existing process:**
```powershell
# Find process using port 8000
Get-NetTCPConnection -LocalPort 8000

# Kill it (replace PID with actual process ID)
Stop-Process -Id <PID> -Force
```

---

### Issue 5: "Slow responses"

**Possible causes:**
1. **Large PDF** - Try smaller PDF first
2. **Slow internet** - OpenAI API requires internet
3. **Low memory** - Close other applications
4. **Free tier rate limits** - Upgrade OpenAI plan

**Check OpenAI status:**
https://status.openai.com/

---

### Issue 6: "Virtual environment activation error"

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

---

## 📱 Next Steps

### 1. Customize the Application

**Change PDF path** (in `app.py`):
```python
PDF_PATH = "data/your_custom_pdf.pdf"
```

**Change model** (in `app.py`, `get_qa_chain()` function):
```python
model_name="gpt-4"  # Better quality, higher cost
```

**Change chunk size** (in `app.py`, `create_text_chunks()` function):
```python
chunk_size=500     # Smaller chunks
chunk_overlap=100  # Less overlap
```

### 2. Explore API Documentation

Visit http://localhost:8000/docs to see:
- All available endpoints
- Request/response schemas
- Try endpoints interactively

### 3. Integrate with Other Apps

**Example: Call from Python**
```python
import requests

response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is remote sensing?"}
)
print(response.json()["answer"])
```

**Example: Call from JavaScript**
```javascript
fetch('http://localhost:8000/ask', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({question: 'What is GIS?'})
})
.then(r => r.json())
.then(data => console.log(data.answer));
```

### 4. Deploy to Production

See deployment guides:
- **Heroku**: https://devcenter.heroku.com/articles/python-gunicorn
- **AWS**: https://aws.amazon.com/getting-started/hands-on/deploy-python-application/
- **Azure**: https://docs.microsoft.com/azure/app-service/quickstart-python
- **Docker**: See DEPLOYMENT.md (coming soon)

### 5. Add Features

Ideas:
- ✨ User authentication
- 💾 Save conversation history
- 🔍 Search history
- 📊 Analytics dashboard
- 🌐 Multiple language support
- 📤 Upload PDF via web interface

---

## 🎓 Learning Resources

### FastAPI
- Official Docs: https://fastapi.tiangolo.com/
- Tutorial: https://fastapi.tiangolo.com/tutorial/

### LangChain
- Docs: https://python.langchain.com/
- QA Tutorial: https://python.langchain.com/docs/use_cases/question_answering/

### OpenAI
- API Docs: https://platform.openai.com/docs
- Embeddings: https://platform.openai.com/docs/guides/embeddings

### FAISS
- GitHub: https://github.com/facebookresearch/faiss
- Tutorial: https://www.pinecone.io/learn/faiss-tutorial/

---

## 💡 Tips & Best Practices

### Performance
- ✅ Use smaller PDFs for faster startup
- ✅ Cache common questions
- ✅ Use gpt-3.5-turbo for speed
- ✅ Use gpt-4 for quality

### Cost Optimization
- 💰 Monitor OpenAI usage: https://platform.openai.com/usage
- 💰 Set billing limits
- 💰 Cache responses
- 💰 Use text-embedding-ada-002 (cheaper)

### Security
- 🔒 Never commit .env file
- 🔒 Use environment variables
- 🔒 Add rate limiting (production)
- 🔒 Enable HTTPS (production)

### Development
- 🔧 Use `--reload` during development
- 🔧 Check `/health` endpoint regularly
- 🔧 Monitor logs for errors
- 🔧 Test with sample questions first

---

## 📞 Getting Help

### Check These First:
1. **README.md** - Project overview
2. **QUICKSTART.md** - Quick reference
3. **ARCHITECTURE.md** - How it works
4. **COMPARISON.md** - Why FastAPI?

### Still Stuck?
1. Check the logs (terminal output)
2. Test with a simple question
3. Verify API key is valid
4. Try with a different PDF
5. Check OpenAI status page

### Error Logs Location:
- Terminal output (stdout/stderr)
- Check console in browser (F12)

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] Python 3.8+ installed
- [ ] All dependencies installed
- [ ] OpenAI API key set correctly
- [ ] PDF file exists in `data/` folder
- [ ] Port 8000 is available
- [ ] Internet connection working
- [ ] OpenAI API has credits
- [ ] No firewall blocking

---

## 🎉 Success!

If you see the web interface and can ask questions, **congratulations!** 

You now have a fully functional AI-powered chatbot that answers questions from your PDF.

**Share your success:**
- ⭐ Star this repository
- 🐦 Tweet about it
- 👥 Share with colleagues

---

## 📚 File Guide

| File | Purpose |
|------|---------|
| `app.py` | Main application code |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |
| `QUICKSTART.md` | Quick reference |
| `ARCHITECTURE.md` | System design |
| `COMPARISON.md` | Streamlit vs FastAPI |
| `SUMMARY.md` | Project summary |
| `test_api.py` | API testing |
| `run.ps1` | PowerShell runner |
| `.env.example` | Environment template |
| `.gitignore` | Git ignore rules |

---

**Happy Coding! 🚀**

Have questions? Check the documentation or create an issue on GitHub.
