"""
Geospatial Information Chatbot
A FastAPI application that answers questions from a fixed geospatial PDF using LangChain and FAISS.
Uses HuggingFace models (FREE - no API key required for basic usage!)
"""

import os
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import fitz  # PyMuPDF
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.schema import Document
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline


# Path to the PDF file
PDF_PATH = "data/geospatial_book.pdf"

# HuggingFace Configuration
# Optional: Set HUGGINGFACEHUB_API_TOKEN for higher rate limits (free to create)
# If not set, will use public models with lower rate limits
HF_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN", None)

# Initialize FastAPI app
app = FastAPI(title="Geospatial Information Chatbot")

# Global variable to store the QA chain
qa_chain = None


class QuestionRequest(BaseModel):
    """Request model for asking questions"""
    question: str


class AnswerResponse(BaseModel):
    """Response model for answers"""
    answer: str
    status: str


def load_pdf_text(pdf_path: str) -> str:
    """
    Load and extract all text from the PDF file using PyMuPDF.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a single string
    """
    try:
        # Open the PDF
        doc = fitz.open(pdf_path)
        text = ""
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
        
        doc.close()
        
        return text
    except Exception as e:
        raise Exception(f"Error loading PDF: {str(e)}")


def create_text_chunks(text: str) -> list:
    """
    Split the text into overlapping chunks for better context retrieval.
    
    Args:
        text: The full text to be chunked
        
    Returns:
        List of Document objects containing text chunks
    """
    # Create text splitter with 1000 character chunks and 200 character overlap
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
    )
    
    # Split the text
    chunks = text_splitter.split_text(text)
    
    # Convert chunks to Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    
    return documents


@lru_cache(maxsize=1)
def build_vector_store(pdf_path: str):
    """
    Build the FAISS vector store from the PDF content.
    This function is cached to avoid reprocessing the PDF on every request.
    Uses HuggingFace embeddings (FREE - runs locally, no API needed!)
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        FAISS vector store object
    """
    print("Loading PDF...")
    text = load_pdf_text(pdf_path)
    
    if not text:
        raise Exception("Failed to load PDF content.")
    
    print("Processing text chunks...")
    documents = create_text_chunks(text)
    
    print("Building vector database with HuggingFace embeddings...")
    print("(First run will download the model - may take a few minutes)")
    
    # Use sentence-transformers model (runs locally, completely free!)
    # Check if CUDA GPU is available
    import torch
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device for embeddings: {device}")
    
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': device},  # Use GPU if available
        encode_kwargs={'normalize_embeddings': True}
    )
    
    vector_store = FAISS.from_documents(documents, embeddings)
    
    print("Vector store built successfully!")
    return vector_store


def get_qa_chain(vector_store):
    """
    Create a RetrievalQA chain for answering questions.
    Uses HuggingFace Hub models (FREE with API token, or limited without)
    
    Args:
        vector_store: FAISS vector store object
        
    Returns:
        RetrievalQA chain object
    """
    # Initialize the language model using local HuggingFace pipeline (NO API KEY NEEDED!)
    # Using Google's FLAN-T5 model (free, runs locally)
    # Options: "google/flan-t5-base" (faster), "google/flan-t5-large" (more detailed but slower)
    
    # Check GPU availability
    import torch
    device = 0 if torch.cuda.is_available() else -1  # 0 = GPU, -1 = CPU
    device_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"
    print(f"🎮 Using device for model: {device_name}")
    
    model_name = "google/flan-t5-large"  # Large model for BEST quality and most detailed responses
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # Move model to GPU if available
    if torch.cuda.is_available():
        model = model.to('cuda')
        print(" Model loaded on GPU - expect 10-20x faster responses!")
    else:
        print(" GPU not available, using CPU")
    
    # Create pipeline
    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        device=device,    # Use GPU (0) or CPU (-1)
        max_length=1024,  # Maximum length for very detailed, comprehensive answers
        min_length=10,   # Minimum length to ensure thorough responses
        temperature=0.3,  # Slightly higher for more varied responses
        do_sample=True,   # Enable sampling for more natural text
        top_p=0.95,       # Nucleus sampling for better quality
        repetition_penalty=1.2  # Reduce repetition in longer text
    )
    
    llm = HuggingFacePipeline(pipeline=pipe)
    
    # Create the RetrievalQA chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_store.as_retriever(search_kwargs={"k": 5}),  # Increased from 3 to 5 for more context
        return_source_documents=False,
        verbose=False,
    )
    
    return qa_chain


def answer_question(question: str, qa_chain) -> str:
    """
    Answer a question using the QA chain.
    
    Args:
        question: User's question
        qa_chain: RetrievalQA chain object
        
    Returns:
        Answer string
    """
    try:
        # Add instruction to answer only from the document with detailed explanation
        enhanced_question = f"""Based on the provided document content, provide a comprehensive and detailed answer to the following question. 

    Instructions:
    - Give a thorough explanation with multiple paragraphs if needed
    - Include relevant examples, definitions, and context from the document
    - Explain concepts clearly and in detail
    - If applicable, break down the answer into key points
    - Use complete sentences and proper formatting

    If the information is not in the document, respond with: "No relevant answer found in the document."

Question: {question}

Detailed Answer:"""
        
        # Get the answer
        result = qa_chain.invoke({"query": enhanced_question})
        answer = result.get("result", "No relevant answer found in the document.")
        
        return answer
    except Exception as e:
        return f"Error processing question: {str(e)}"


@app.on_event("startup")
async def startup_event():
    """
    Initialize the QA chain when the application starts.
    Using HuggingFace models - FREE!
    """
    global qa_chain
    
    # Check if HuggingFace token is set (optional but recommended)
    if not HF_API_TOKEN:
        print("INFO: HUGGINGFACEHUB_API_TOKEN not set - using limited rate limits")
        print("To get unlimited access: Get free token at https://huggingface.co/settings/tokens")
    else:
        print("INFO: Using HuggingFace API token")
    
    # Check if PDF exists
    if not os.path.exists(PDF_PATH):
        print(f"WARNING: PDF file not found at: {PDF_PATH}")
        return
    
    try:
        # Build vector store and QA chain
        print("Initializing with HuggingFace models (FREE)...")
        vector_store = build_vector_store(PDF_PATH)
        qa_chain = get_qa_chain(vector_store)
        print("Application initialized successfully!")
        print("Ready to answer questions! 🚀")
    except Exception as e:
        print(f"Error during initialization: {str(e)}")


@app.get("/", response_class=HTMLResponse)
async def root():
    """
    Serve the main HTML page with the chatbot interface.
    """
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Geospatial Information Chatbot</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 800px;
                width: 100%;
                padding: 40px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            
            .header h1 {
                color: #333;
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            
            .header .emoji {
                font-size: 3em;
                margin-bottom: 10px;
            }
            
            .header p {
                color: #666;
                font-size: 1.1em;
            }
            
            .divider {
                height: 2px;
                background: linear-gradient(90deg, transparent, #667eea, transparent);
                margin: 30px 0;
            }
            
            .question-section {
                margin-bottom: 30px;
            }
            
            .question-section label {
                display: block;
                color: #333;
                font-weight: 600;
                margin-bottom: 10px;
                font-size: 1.1em;
            }
            
            .input-group {
                display: flex;
                gap: 10px;
            }
            
            #questionInput {
                flex: 1;
                padding: 15px;
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            
            #questionInput:focus {
                outline: none;
                border-color: #667eea;
            }
            
            #askButton {
                padding: 15px 30px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            
            #askButton:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
            }
            
            #askButton:active {
                transform: translateY(0);
            }
            
            #askButton:disabled {
                background: #ccc;
                cursor: not-allowed;
                transform: none;
            }
            
            .answer-section {
                display: none;
                background: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
            }
            
            .answer-section.show {
                display: block;
            }
            
            .answer-section h2 {
                color: #333;
                margin-bottom: 15px;
                font-size: 1.3em;
            }
            
            .answer-content {
                color: #555;
                line-height: 1.8;
                font-size: 1.05em;
            }
            
            .loading {
                display: none;
                text-align: center;
                padding: 20px;
                color: #667eea;
            }
            
            .loading.show {
                display: block;
            }
            
            .spinner {
                border: 3px solid #f3f3f3;
                border-top: 3px solid #667eea;
                border-radius: 50%;
                width: 40px;
                height: 40px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .footer {
                text-align: center;
                color: #999;
                font-size: 0.9em;
                margin-top: 30px;
            }
            
            .status-indicator {
                display: inline-block;
                padding: 8px 16px;
                border-radius: 20px;
                font-size: 0.9em;
                margin-bottom: 20px;
            }
            
            .status-success {
                background: #d4edda;
                color: #155724;
            }
            
            .status-error {
                background: #f8d7da;
                color: #721c24;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="emoji">🌍</div>
                <h1>Geospatial Information Chatbot</h1>
                <p>Ask questions about geospatial information from the loaded PDF document</p>
            </div>
            
            <div class="divider"></div>
            
            <div id="statusContainer"></div>
            
            <div class="question-section">
                <label for="questionInput">Ask your question:</label>
                <div class="input-group">
                    <input 
                        type="text" 
                        id="questionInput" 
                        placeholder="e.g., What is remote sensing?"
                        onkeypress="handleKeyPress(event)"
                    >
                    <button id="askButton" onclick="askQuestion()">Get Answer</button>
                </div>
            </div>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p id="loadingText">🤖 Analyzing your question with AI...</p>
                <p style="font-size: 0.85em; color: #888; margin-top: 10px;">
                    Using FLAN-T5-Large (783M parameters) with GPU acceleration 🎮<br>
                    Expected time: 2-5 seconds for detailed, comprehensive answers
                </p>
                <div style="margin-top: 15px; font-size: 0.8em; color: #999;">
                    <span id="timer">0</span> seconds elapsed...
                </div>
            </div>
            
            <div class="answer-section" id="answerSection">
                <h2>📝 Answer:</h2>
                <div class="answer-content" id="answerContent"></div>
            </div>
            
            <div class="divider"></div>
            
            <div class="footer">
                Powered by LangChain, HuggingFace 🤗, and FAISS (100% Free & Open Source!)
            </div>
        </div>
        
        <script>
            // Check health status on load
            window.onload = function() {
                checkHealth();
            };
            
            async function checkHealth() {
                try {
                    const response = await fetch('/health');
                    const data = await response.json();
                    const statusContainer = document.getElementById('statusContainer');
                    
                    if (data.status === 'ready') {
                        statusContainer.innerHTML = '<div class="status-indicator status-success">✅ System Ready</div>';
                    } else {
                        statusContainer.innerHTML = '<div class="status-indicator status-error">⚠️ ' + data.message + '</div>';
                    }
                } catch (error) {
                    console.error('Error checking health:', error);
                }
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    askQuestion();
                }
            }
            
            let timerInterval;
            
            async function askQuestion() {
                const questionInput = document.getElementById('questionInput');
                const question = questionInput.value.trim();
                
                if (!question) {
                    alert('Please enter a question.');
                    return;
                }
                
                // Show loading, hide answer
                document.getElementById('loading').classList.add('show');
                document.getElementById('answerSection').classList.remove('show');
                document.getElementById('askButton').disabled = true;
                
                // Start timer and dynamic messages
                let seconds = 0;
                const timerElement = document.getElementById('timer');
                const loadingText = document.getElementById('loadingText');
                const messages = [
                    '🤖 Analyzing your question with AI...',
                    '📚 Searching through document chunks...',
                    '🧠 Generating comprehensive answer...',
                    '✨ Crafting detailed response...',
                    '⚡ Almost done, perfecting the answer...'
                ];
                let messageIndex = 0;
                
                timerInterval = setInterval(() => {
                    seconds++;
                    timerElement.textContent = seconds;
                    
                    // Change message every 5 seconds
                    if (seconds % 5 === 0 && messageIndex < messages.length - 1) {
                        messageIndex++;
                        loadingText.textContent = messages[messageIndex];
                    }
                }, 1000);
                
                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ question: question })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        document.getElementById('answerContent').textContent = data.answer;
                        document.getElementById('answerSection').classList.add('show');
                    } else {
                        alert('Error: ' + (data.detail || 'Unknown error'));
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                } finally {
                    clearInterval(timerInterval);
                    document.getElementById('loading').classList.remove('show');
                    document.getElementById('askButton').disabled = false;
                }
            }
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


@app.get("/health")
async def health_check():
    """
    Check if the application is ready to answer questions.
    """
    if qa_chain is None:
        return {
            "status": "not_ready",
            "message": "System is initializing or PDF not loaded"
        }
    
    return {
        "status": "ready",
        "message": "System is ready to answer questions"
    }


@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: QuestionRequest):
    """
    Answer a question based on the PDF content.
    """
    if qa_chain is None:
        raise HTTPException(
            status_code=503,
            detail="System not ready. Please check if PDF is loaded and OpenAI API key is set."
        )
    
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    
    try:
        answer = answer_question(request.question, qa_chain)
        return AnswerResponse(answer=answer, status="success")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
