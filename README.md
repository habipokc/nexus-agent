# 🤖 Nexus-Agent

> **Fully Local, Autonomous AI Agent with RAG & Self-Reflection Capabilities.**

![Python](https://img.shields.io/badge/Python-3.12%2B-blue)
![Orchestration](https://img.shields.io/badge/Orchestration-LangGraph-orange)
![Model](https://img.shields.io/badge/Model-Llama_3.2-green)
![Backend](https://img.shields.io/badge/Backend-FastAPI-teal)
![Frontend](https://img.shields.io/badge/Frontend-Streamlit-red)


**Nexus-Agent** is an intelligent conversational assistant designed to run **100% locally** on Ubuntu Linux. It leverages the lightweight **Llama 3.2 3B** model via Ollama and orchestrates a multi-agent workflow using **LangGraph**. The system features a hybrid router, local RAG (Retrieval-Augmented Generation) for technical knowledge, Wikipedia integration for general queries, and a self-correction mechanism to ensure response quality.

---

## 🏗️ Architecture

The system operates on a **Stateful Multi-Agent** architecture:

1.  **Router:** A hybrid (keyword-based) router classifies user intent into `Technical`, `General`, or `Greeting`.
2.  **Specialized Agents:**
    *   **🛠️ Technical Agent:** Uses **ChromaDB** (Local Vector Store) to answer project-specific questions.
    *   **🌍 General Agent:** Uses **Wikipedia** to answer general knowledge questions.
    *   **👋 Greeting Agent:** Handles small talk without invoking external tools.
3.  **⚖️ Grader (Self-Reflection):** Evaluates the generated answer. If the answer is hallucinated or irrelevant, it rejects it (or flags it).
4.  **💾 Memory:** Utilizes `LangGraph Checkpointer` to maintain conversation context across turn-based interactions.

---

## 📂 Project Structure

```text
nexus-agent/
├── nexus_agent/
│   ├── api/            # FastAPI Backend (REST API & Pydantic Models)
│   ├── ui/             # Streamlit Frontend (Chat Interface)
│   ├── agents/         # Node Definitions (Tech, General, Grader)
│   ├── core/           # Core Logic (Router, State Management)
│   ├── agent.py        # LangGraph Orchestration & Workflow Definition
│   ├── rag.py          # ChromaDB Ingestion & Retrieval Logic
│   └── tools.py        # Tool Definitions (Safe Wikipedia Wrapper)
├── data/               # Source documents for RAG
├── chroma_db/          # Local Vector Database (Persisted)
├── pyproject.toml      # Poetry Dependency Management
└── README.md           # Documentation

```

---

## 🚀 Getting Started

### Prerequisites

*   **OS:** Ubuntu Linux (Developed and tested on Ubuntu).
*   **Python:** Version 3.12+
*   **Package Manager:** [Poetry](https://python-poetry.org/)
*   **LLM Runtime:** [Ollama](https://ollama.com/)

### 1. Installation

Clone the repository and install dependencies using Poetry:

```bash
git clone https://github.com/habip-okc/nexus-agent.git
cd nexus-agent

# Install dependencies
poetry install
```

### 2. Model Setup

Pull the Llama 3.2 model using Ollama:

```bash
ollama pull llama3.2
```

### 3. Database Initialization (RAG)

Before running the agent, ingest your local data (inside `data/` folder) into the vector database:

```bash
poetry run python nexus_agent/rag.py
```
*You should see a success message indicating chunks have been embedded.*

---

## 💻 Usage

Nexus-Agent follows a Client-Server architecture. You will need **two terminal windows**.

### Terminal 1: Backend (API)
Start the FastAPI server. This exposes the LangGraph logic via a REST API.

```bash
poetry run uvicorn nexus_agent.api.main:app --reload
```
*Server runs at: `http://127.0.0.1:8000`*
*Swagger Docs: `http://127.0.0.1:8000/docs`*

### Terminal 2: Frontend (UI)
Start the Streamlit interface to chat with the agent.

```bash
poetry run streamlit run nexus_agent/ui/app.py
```
*UI opens at: `http://localhost:8501`*

---

## 🧪 Development & Testing

We strictly follow **Clean Code** principles. The project includes a CI pipeline setup for formatting and testing.

```bash
# Run Linter (Ruff)
poetry run ruff check .

# Run Unit Tests
poetry run pytest