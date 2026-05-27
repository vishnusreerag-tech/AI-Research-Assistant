# 🧠 AI Research Assistant

An advanced AI-powered Research Assistant built using RAG (Retrieval-Augmented Generation), ChromaDB, Gemini, and Streamlit.

The system allows users to upload multiple PDFs, perform semantic document search, and generate intelligent context-aware answers using modern LLM architecture.

---

#  Features

 Multi-PDF Upload Support  
 Semantic Search using Embeddings  
 ChromaDB Vector Database Integration  
 Retrieval-Augmented Generation (RAG)  
 Context-Aware Question Answering  
 Source Citation Support  
 Persistent Vector Storage  
 Modern Streamlit UI  
 Modular AI Architecture  
 Gemini/OpenAI LLM Integration  

---

#  RAG Pipeline

```text
PDF Upload
↓
Text Extraction
↓
Chunking
↓
Embeddings Generation
↓
Store in ChromaDB
↓
Semantic Retrieval
↓
Gemini Response Generation
↓
Answer + Source Citations
```

---

#  Tech Stack

- Python
- Streamlit
- ChromaDB
- LangChain Text Splitters
- Sentence Transformers
- Gemini API / OpenAI API
- NLP
- RAG Architecture

---

#  Project Structure

```bash
AI-Research-Assistant/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env
│
├── utils/
│   ├── pdf_loader.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   └── generator.py
│
├── chroma_db/
├── screenshots/
│
└── data/
```

---

#  Installation

## Clone Repository

```bash
git clone https://github.com/vishnusreerag-tech/AI-Research-Assistant.git
```

---

## Move Into Project Folder

```bash
cd AI-Research-Assistant
```

---

## Create Virtual Environment

### Linux / Mac

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\\Scripts\\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

#  Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

---

#  Run Application

```bash
streamlit run app.py
```

---

#  Upcoming Features

### Conversational Memory
- Context-aware conversations
- Chat history support

### Streaming Responses
- Real-time AI response generation

### Advanced Retrieval
- Hybrid search
- Reranking
- Metadata filtering

### AI Research Features
- Research summarization
- Flashcard generation
- Quiz generation
- Notes generation

### UI Improvements
- Chat-based interface
- Dark/Light themes
- Animated loading effects

### Multi-Format Support
- TXT
- DOCX
- Markdown
- Website ingestion

---

#  Concepts Used

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Embeddings
- Vector Databases
- NLP Pipelines
- Large Language Models (LLMs)

---

#  Status

Currently under active development with continuous feature additions and improvements.

---

#  Author

Vishnu Sreerag  
MSc Computer Science (Data Science)
