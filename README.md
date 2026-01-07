# 📄 Chatbot for PDF – RAG-based Document Q&A using LLaMA & Groq

This is a lightweight Retrieval-Augmented Generation (RAG) agent that takes a PDF document, breaks it into chunks, indexes the chunks using FAISS, and answers user queries based on the document context using the LLaMA3 model deployed via Groq API.

---

## 🚀 Features

- ✅ Extracts text from PDF documents
- ✅ Splits text into meaningful chunks
- ✅ Builds a FAISS vector index for fast similarity search
- ✅ Uses Groq API with LLaMA3 to generate answers
- ✅ CLI-based (no FastAPI or web frontend)

---

## 🛠️ Setup Instructions

1. **Clone the repo**

   ```bash
   git clone https://github.com/tibdewalchahak/Chatbot_for_PDF.git
   cd Chatbot_for_PDF
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set your Groq API key:**
   Create a .env file in the root directory:
   ```bash
   GROQ_API_KEY=your_groq_api_key_here
   ```
4. **Run the RAG agent**
   ```bash
   python main.py
   ```
   You'll be prompted to enter a PDF file path and then a query.

## 📁 Project Structure
```bash
Chatbot_for_PDF/
├── main.py               # Entry point for the agent
├── .gitignore
├── rag_utils.py           # FAISS index, search, and LLaMA3 answer generation
├── pdf_utils.py           # PDF text extraction and chunking
├── requirements.txt       # Python dependencies
├── .env                   # (not included) Groq API key
└── README.md
```

## 📌 Example
```bash
Enter the path to your PDF file: ./docs/sample_resume.pdf
Ask a question: What technologies does the candidate know?
```
