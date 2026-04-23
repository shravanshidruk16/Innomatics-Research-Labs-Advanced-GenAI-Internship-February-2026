# 🤖 NovaTech RAG-Based Customer Support Assistant

## 📌 Overview

This project is an AI-powered **Customer Support Assistant** built using **Retrieval-Augmented Generation (RAG)** and **LangGraph**.

It answers user queries based on a predefined **knowledge base PDF** and intelligently decides whether to:

* ✅ Respond using AI
* ⚠️ Escalate to a human (HITL - Human-in-the-Loop)

---

## 🚀 Features

* 📄 PDF-based knowledge ingestion
* 🔍 Semantic search using embeddings (ChromaDB)
* 🧠 Context-aware response generation (LLM)
* 🔁 LangGraph workflow (stateful execution)
* ⚖️ Intelligent routing (Respond / Escalate)
* 👨‍💻 Human-in-the-loop (HITL) support
* 💬 CLI-based interactive chatbot

---

## 🏗️ Project Architecture (HLD)

High-Level Flow:

User Query
↓
RAG Pipeline (Retrieve + Generate)
↓
LangGraph Workflow
↓
Decision Node
↓
[Respond] OR [Escalate to Human]

### Components:

* **Ingestion Layer** → Loads and processes PDF
* **Embedding Layer** → Converts text into vectors
* **Vector Store** → Stores embeddings (ChromaDB)
* **Retriever** → Fetches relevant chunks
* **LLM Layer** → Generates answers
* **Graph Layer (LangGraph)** → Controls workflow
* **Routing Layer** → Decides response or escalation
* **HITL Module** → Handles human intervention

---

## 🧩 Low-Level Design (LLD)

### 📁 Folder Structure

```
rag-support-bot/
│
├── app/
│   ├── ingestion/      # PDF loading & chunking
│   ├── retrieval/      # vector DB & retriever
│   ├── llm/            # LLM configuration
│   ├── graph/          # LangGraph workflow
│   ├── routing/        # decision logic
│   ├── hitl/           # human escalation
│   └── main.py         # entry point
│
├── data/               # knowledge base PDF
├── vectorstore/        # embeddings database
├── docs/               # HLD, LLD, Technical Docs
├── requirements.txt
└── README.md
```

---

## ⚙️ Tech Stack

* **Python**
* **LangChain**
* **LangGraph**
* **ChromaDB**
* **Ollama / Groq (LLM)**
* **Sentence Transformers (Embeddings)**

---

## 🔄 Workflow Explanation

1. User enters a query
2. System retrieves relevant chunks from vector DB
3. LLM generates answer using retrieved context
4. LangGraph processes the state
5. Router decides:

   * Respond → return answer
   * Escalate → trigger human input

---

## 🧠 Routing Logic

* Respond when answer is relevant and complete
* Escalate when:

  * Answer is weak or missing
  * Query is out of scope
  * Sensitive cases (e.g., security issues)

---

## 👨‍💻 HITL (Human-in-the-Loop)

When escalation is triggered:

* System asks for human input via CLI
* Human response is returned to the user
* Ensures reliability for complex queries

---

## 🛠️ Setup Instructions

### 1. Clone Repository

```
git clone <your-repo-link>
cd rag-support-bot
```

### 2. Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create `.env` file:

```
GROQ_API_KEY=your_api_key_here
```

---

## ▶️ Run the Project

```
python app/main.py
```

---

## 💬 Example Queries

* How do I cancel my subscription?
* My payment failed what should I do?
* Files are not syncing
* What is refund policy?
* My account is hacked

---

## 📊 Technical Design Decisions

* **RAG over Fine-tuning** → Better flexibility and real-time updates
* **Chunking Strategy** → Optimized for structured documents
* **ChromaDB** → Lightweight and efficient vector storage
* **LangGraph** → Enables stateful and modular workflows
* **HITL Integration** → Improves reliability and real-world usability

---

## ⚠️ Limitations

* Depends on knowledge base quality
* Basic routing logic (can be improved with confidence scoring)
* CLI-based interface (can be extended to web UI)

---

## 📈 Future Improvements

* Web-based UI (React / Streamlit)
* LLM-based routing with confidence score
* Multi-document support
* Chat history & memory
* API deployment

---

## 📄 Documentation

Detailed documents are available in the `/docs` folder:

* HLD (High-Level Design)
* LLD (Low-Level Design)
* Technical Documentation

---

## 🧠 Key Concepts Used

* RAG (Retrieval-Augmented Generation)
* Embeddings & Vector Search
* LangGraph (Stateful AI workflows)
* HITL (Human-in-the-Loop)
* Prompt Engineering

---

## 🙌 Conclusion

This project demonstrates how to build a **real-world AI customer support system** that combines:

* Retrieval
* Generation
* Decision-making
* Human intervention

---

## ⭐ If you like this project, consider giving it a star!
