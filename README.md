

## Overview  
Smart Ruby Surge is an AI-powered document retrieval and response generation system. It processes and indexes various file formats, enabling efficient retrieval and AI-assisted question answering. The project implements **two approaches**:  
1. **LangChain-based approach** – Optimized for structured retrieval workloads, providing efficient and lightweight processing.  
2. **Non-LangChain approach** – Offers greater flexibility, allowing custom vector search and document handling.  

## Features and Implementation  

### **Document Processing and Transcription**  
- Extracts text from **PDF, DOCX, and images** using `PyMuPDF`, `python-docx`, and `Pytesseract OCR`.  
- **Videos** are transcribed by extracting audio, chunking it, and converting speech to text using `SpeechRecognition`.  
- The processed text is converted into a **PDF** using `ReportLab` for consistency.  

### **Vector Storage and Retrieval**  
- Converts processed text into embeddings using a simulated embedding function.  
- Stores embeddings in a **FAISS vector database**, optimized for similarity search.  
- Query documents are dynamically uploaded, embedded, and searched against stored vectors.  

### **AI-Powered Response Generation**  
- Retrieves relevant document chunks based on vector similarity search.  
- Uses **LLaMA 3.2 (via Ollama)** to generate human-like responses.  
- Maintains **conversation history** for contextual understanding.  

### **Interactive Chat System**  
- Provides a **command-line interface** for document uploads, text extraction, and AI interaction.  
- Dynamically updates the vector store with newly processed documents for future queries.  

### **AI-Generated Response Playback**  
- Uses **JavaScript** to read aloud AI-generated responses.  
- Converts text responses into speech for better accessibility.  
- Enhances the user experience by enabling voice-based output.  

## Project Structure  
```
📂 Smart-Ruby-Surge  
│── 📂 db                # FAISS vector database  
│── 📂 langchain         # Implementation using LangChain  
│── 📂 source_documents  # Source files for processing  
│── 📂 transcript        # Transcribed text from videos  
│── 📂 without_langchain # Implementation without LangChain  
│── 📄 requirements.txt  # Dependencies  
```

## **Tech Stack**  
- **Python** – Core programming language  
- **LangChain** – Efficient structured retrieval (used in one approach)  
- **FAISS** – Vector database for similarity search  
- **Ollama (LLaMA 3.2)** – AI-powered response generation  
- **SpeechRecognition** – Converts speech to text for video transcription  
- **Tesseract OCR** – Extracts text from images(Make sure to download Tesseract from the given link before running - https://github.com/UB-Mannheim/tesseract/wiki)
- **PyMuPDF & python-docx** – Parses PDFs and DOCX files  
- **JavaScript** – Reads aloud AI-generated responses  

## **Setup Instructions**  

### **1. Clone the Repository**  
```bash
git clone https://github.com/your-username/Smart-Ruby-Surge.git  
cd Smart-Ruby-Surge
```

### **2. Install Dependencies**  
```bash
pip install -r requirements.txt
```

### **3. Run the Application**  
#### **LangChain-based Approach**  
```bash
cd langchain  
python app.py  
```

#### **Non-LangChain Approach**  
```bash
cd without_langchain  
streamlit run frontendollama.py 
```

## **Inference**  
After implementing and testing both methods:  
- The **LangChain-based approach** is **more accurate, lightweight, and efficient**. It optimizes embedding retrieval, ensuring **faster and more relevant** results with minimal computational overhead. Ideal for **real-time AI applications** like chatbots and enterprise search.  
- The **Non-LangChain approach** allows **greater flexibility** in document processing and vector search, making it suitable for **research projects** or cases requiring **customized AI retrieval pipelines**.  
![Screenshot 2025-03-25 112432](https://github.com/user-attachments/assets/b1613b71-3acb-48c2-9e7d-a3b9d875c2c2)



  
