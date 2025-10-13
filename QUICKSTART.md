# Quick Start Guide

## 1. Install Dependencies

```powershell
pip install -r requirements.txt
```

## 2. Set OpenAI API Key

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

## 3. Add Your PDF

Place your geospatial PDF at: `data/geospatial_book.pdf`

## 4. Run the Application

```powershell
python app.py
```

Or with auto-reload:
```powershell
uvicorn app:app --reload
```

## 5. Access the Application

Open your browser and go to: http://localhost:8000

## 6. Test the API (Optional)

```powershell
python test_api.py
```

## API Usage Examples

### Using cURL:

**Health Check:**
```powershell
curl http://localhost:8000/health
```

**Ask a Question:**
```powershell
curl -X POST http://localhost:8000/ask `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"What is remote sensing?\"}'
```

### Using Python:

```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:8000/ask",
    json={"question": "What is remote sensing?"}
)

print(response.json())
```

### Using JavaScript:

```javascript
// Ask a question
fetch('http://localhost:8000/ask', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        question: 'What is remote sensing?'
    })
})
.then(response => response.json())
.then(data => console.log(data.answer));
```

## Troubleshooting

### Port Already in Use?

```powershell
uvicorn app:app --port 8080
```

### API Key Not Found?

Make sure to set it in the same terminal session:
```powershell
$env:OPENAI_API_KEY="sk-..."
python app.py
```

### PDF Not Found?

Check the path:
```powershell
ls data/geospatial_book.pdf
```
