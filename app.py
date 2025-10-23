"""
Geospatial Information Chatbot
A FastAPI application that answers questions from a fixed geospatial PDF using LangChain and FAISS.
Uses HuggingFace models (FREE - no API key required for basic usage!)
"""

import os
from functools import lru_cache
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
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

# Mount the built frontend folder to serve static files
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

# Global variable to store the QA chain
qa_chain = None


class QuestionRequest(BaseModel):
    """Request model for asking questions"""
    question: str


class AnswerResponse(BaseModel):
    """Response model for answers"""
    answer: str
    status: str


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


@app.get("/")
async def root():
    """
    Serve the main HTML page from the frontend dist folder.
    """
    return FileResponse("frontend/dist/index.html")


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
            detail="System not ready. Please check if PDF is loaded."
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
