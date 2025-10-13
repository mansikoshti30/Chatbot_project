"""
Example script to test the FastAPI chatbot API programmatically.
"""

import requests
import json

# Base URL of the API
BASE_URL = "http://localhost:8000"


def check_health():
    """Check if the API is ready"""
    response = requests.get(f"{BASE_URL}/health")
    data = response.json()
    print("Health Check:")
    print(json.dumps(data, indent=2))
    print()
    return data["status"] == "ready"


def ask_question(question: str):
    """Ask a question to the chatbot"""
    response = requests.post(
        f"{BASE_URL}/ask",
        json={"question": question}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"Question: {question}")
        print(f"Answer: {data['answer']}")
        print()
        return data["answer"]
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        print()
        return None


def main():
    """Main function to test the API"""
    print("=" * 60)
    print("Testing Geospatial Information Chatbot API")
    print("=" * 60)
    print()
    
    # Check health
    if not check_health():
        print("API is not ready. Please check the server.")
        return
    
    # Example questions
    questions = [
        "What is remote sensing?",
        "What are the main types of satellite imagery?",
        "How does GPS work?",
    ]
    
    for question in questions:
        ask_question(question)
        print("-" * 60)
        print()


if __name__ == "__main__":
    main()
