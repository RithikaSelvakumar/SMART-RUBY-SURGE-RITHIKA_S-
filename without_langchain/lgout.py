import os
import sys
import pytesseract
from PIL import Image
import faiss
import numpy as np
import subprocess
import fitz  # PyMuPDF
from docx import Document
from sentence_transformers import SentenceTransformer

# -------------------- Configuration -------------------- #

# Set the path to the Tesseract executable
tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
if not os.path.exists(tesseract_path):
    print(f"Error: Tesseract is not installed at {tesseract_path}.")
    sys.exit(1)

pytesseract.pytesseract.tesseract_cmd = tesseract_path

# -------------------- FAISS Vector Store Initialization -------------------- #

class FAISSVectorStore:
    def __init__(self):
        self.index = None  # FAISS index
        self.documents = []  # Store document chunks

    def add_documents(self, texts):
        chunked_texts = []
        for text in texts:
            chunked_texts.extend(chunk_text(text))  # Split each document into chunks

        vectors = embed_documents(chunked_texts)  # Embed chunked texts
        if self.index is None:
            self.index = faiss.IndexFlatL2(vectors.shape[1])
        self.index.add(vectors)
        self.documents.extend(chunked_texts)  # Store chunked texts

    def search(self, query, k=5):
        if not self.documents:
            print("Error: No documents found.")
            return []

        query_vector = embed_documents([query])
        distances, indices = self.index.search(query_vector, k)

        return [self.documents[i] for i in indices[0] if i < len(self.documents)]

vector_store = FAISSVectorStore()

# -------------------- Text Chunking -------------------- #

def chunk_text(text, chunk_size=300, overlap=50):
    """ Splits text into overlapping chunks. """
    words = text.split()  # Tokenize by words
    chunks = []
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    
    return chunks

# -------------------- Embedding and Query Functions -------------------- #

def embed_documents(documents):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return np.array(model.encode(documents, convert_to_numpy=True))

conversation_history = []  # Store chat history

def generate_answer(query):
    try:
        retrieved_docs = vector_store.search(query)
        if not retrieved_docs:
            return "I couldn't find anything relevant. Try rephrasing?"

        context = "\n".join(retrieved_docs)[:600]  # Limit to 600 characters

        conversation_history.append(f"User: {query}")  # Store query

        prompt = """
            You are a helpful AI assistant.
            Maintain a conversational tone and use context from previous chats.

            Past Conversation:
            {}
            
            Context: {}

            Answer the following in a friendly and engaging way:
            {}
        """.format("\n".join(conversation_history[-5:]), context, query)

        response = run_llama(prompt)
        conversation_history.append(f"AI: {response}")  # Store response
        return response if response else "Something went wrong."
    
    except Exception as e:
        print(f"Error generating answer: {e}")
        return "I'm having trouble understanding. Could you rephrase?"

# -------------------- Llama Model Function -------------------- #

def run_llama(query, model="llama3.2"):
    result = subprocess.run(
        ["ollama", "run", model],
        input=query,
        text=True,
        capture_output=True
    )
    
    return result.stdout.strip() if result.returncode == 0 else None

# -------------------- Text Extraction Functions -------------------- #

def extract_text_from_image(image_path):
    try:
        return pytesseract.image_to_string(Image.open(image_path)).strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

def extract_text_from_pdf(pdf_path):
    text = ""
    try:
        doc = fitz.open(pdf_path)
        for page in doc:
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def extract_text_from_docx(docx_path):
    try:
        doc = Document(docx_path)
        return "\n".join([p.text for p in doc.paragraphs]).strip()
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        return None

# -------------------- Main Interactive Loop -------------------- #

def main():
    print("Welcome to the AI Document Query System!")

    while True:
        print("\nPlease choose an option:")
        print("1. Extract text from an image")
        print("2. Extract text from a PDF")
        print("3. Extract text from a DOCX")
        print("4. Chat with the AI")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ").strip()

        if choice in ['1', '2', '3']:
            file_path = input("Enter the file path: ").strip()
            extracted_text = None

            if choice == '1':
                extracted_text = extract_text_from_image(file_path)
            elif choice == '2':
                extracted_text = extract_text_from_pdf(file_path)
            elif choice == '3':
                extracted_text = extract_text_from_docx(file_path)

            if extracted_text:
                vector_store.add_documents([extracted_text])
                print("Text extracted and stored for retrieval.")

        elif choice == '4':
            print("\nStart chatting! (Type 'exit' to go back)\n")
            while True:
                query = input("You: ").strip()
                if query.lower() == 'exit':
                    break
                answer = generate_answer(query)
                print(f"\nAI: {answer}")

        elif choice == '5':
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
