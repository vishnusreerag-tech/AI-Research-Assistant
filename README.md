# AI Research Assistant

AI-powered Research Assistant built using RAG (Retrieval-Augmented Generation), LangChain, ChromaDB, and Streamlit.

The application allows users to upload research documents and ask questions using semantic search and Large Language Models.

---

# Features

* PDF document upload
* Semantic search using embeddings
* ChromaDB vector database integration
* Context-aware question answering
* Streamlit interactive UI
* Modular RAG pipeline
* Gemini/OpenAI LLM integration

---

# Tech Stack

* Python
* Streamlit
* LangChain
* ChromaDB
* HuggingFace Embeddings
* Gemini API / OpenAI API

---

# Project Structure

```bash
AI-Research-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│
├── utils/
│   ├── pdf_loader.py
│   ├── text_splitter.py
│   ├── embeddings.py
│   ├── retriever.py
│   └── generator.py
│
└── chroma_db/
```

---

# Installation

```bash
git clone https://github.com/vishnusreerag-tech/AI-Research-Assistant.git

cd AI-Research-Assistant

pip install -r requirements.txt

streamlit run app.py
```

---

# Upcoming Features & Roadmap

### Source Citations

* Retrieved document chunks
* Page numbers
* Source references

### Multiple PDF Support

* Multiple document uploads
* Cross-document retrieval

### ChromaDB Persistence

* Persistent vector database storage

### Conversational Chat Memory

* Context-aware conversations

### Advanced Retrieval

* Hybrid search
* Reranking
* Metadata filtering

### AI Research Features

* Research summarization
* Flashcard generation
* Quiz generation
* Citation generation

### Modern UI Improvements

* Dark/light themes
* Chat-based layout
* Animated loading effects

### Multi-Format Support

* TXT
* DOCX
* Markdown
* Website ingestion

---

# Status

Currently under active development with continuous feature additions and improvements.
