# Domain Specific Conversational Assistant with Memory and Source Grounding

A local, privacy-first conversational AI research assistant built specifically for domain knowledge bases (PDF collections). Powered by Ollama and pure-Python algorithms, it integrates multi-turn conversational memory, hybrid retrieval (semantic vector search + BM25 keyword matching), Reciprocal Rank Fusion (RRF), neighboring chunk expansion, and strict source grounding to deliver verifiable, citation-backed answers.

---

## 🌟 Key Pillars

- **Domain-Specific Knowledge Base:** Ingests local domain PDFs, preserving exact page numbers, chunk boundaries, and document metadata.
- **Conversational Memory:** Preserves multi-turn dialogue context across interactions for natural follow-up questions and co-reference resolution.
- **Strict Source Grounding:** An autonomous agent tool loop requires the model to query documents before answering, eliminating guesswork and citing exact document names, chunk IDs, and page ranges.
- **100% Offline & Private:** Zero cloud dependencies, zero recurring API token costs, and zero data leakage.

---

## ✨ Features

- **Dual Interfaces (Web GUI & Terminal CLI):** Choose between a modern browser-based Streamlit dashboard or an interactive terminal CLI.
- **Document Explorer & Text Inspector:** Real-time GUI panel to view indexed PDFs, inspect page counts, file sizes, and review extracted text page-by-page.
- **Page-Aware PDF Extraction:** Text extraction with PyMuPDF that automatically repairs hyphenated line wraps.
- **Sliding-Window Chunking:** Word-based chunking (650 words with 100-word overlap) tracking exact start and end page numbers.
- **Hybrid Search Engine:** Combines dense cosine-similarity embeddings (`nomic-embed-text`) with sparse BM25 keyword scoring.
- **Reciprocal Rank Fusion (RRF):** Fuses dense and sparse rankings robustly ($k=60$) without requiring score normalization.
- **Neighboring Chunk Expansion:** Automatically retrieves adjacent chunks ($n-1, n, n+1$) to ensure complete context without mid-sentence truncations.
- **Presentation Deck Included:** Comes with an 11-slide PowerPoint presentation (`Domain_Specific_Conversational_Assistant.pptx`) for project reviews and evaluations.

---

## 📁 Project Layout

```text
rag-assistant-main/
├── app.py                                   # Streamlit Web GUI (Question Panel & Document Explorer)
├── assistant.py                             # Interactive CLI assistant with tool-calling loop
├── embed.py                                 # PDF ingestion and embedding-index generator
├── rag.py                                   # Hybrid search, BM25, RRF, and context construction
├── requirements.txt                         # Python dependencies
├── generate_presentation.py                 # Automated PPTX presentation generator script
├── Domain_Specific_Conversational_Assistant.pptx # 11-slide presentation deck
├── docs/                                    # Source PDF corpus (AI research papers)
└── index.json                               # Generated local index (git-ignored)
```

---

## 🛠️ Step-by-Step Implementation Guide

Follow these sequential steps to set up and run the project from scratch:

### Step 1: Install & Launch Ollama
Ensure [Ollama](https://ollama.com/) is installed and running on your system.

Pull the required embedding and language models:
```bash
# 1. Pull the 8192-context embedding model
ollama pull nomic-embed-text

# 2. Pull the default conversational LLM
ollama pull lfm3-omni:2b
```
*(Optional: If Ollama isn't already running in the background, start it with `ollama serve`)*

---

### Step 2: Clone the Repository & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/aryannnn25/rag-assistant.git
cd rag-assistant

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # On macOS / Linux
# venv\Scripts\activate        # On Windows
```

---

### Step 3: Install Required Python Dependencies
```bash
python3 -m pip install -r requirements.txt
```
*Dependencies installed include `ollama`, `pymupdf` (PyMuPDF), `streamlit`, and `python-pptx`.*

---

### Step 4: Populate Domain Documents & Build Knowledge Index
1. Place any domain PDF files inside the `docs/` folder (the repository includes 8 research papers by default).
2. Run the ingestion and embedding script to generate the local vector and keyword index:
```bash
python3 embed.py
```
> **What this does:** `embed.py` reads every PDF in `docs/` with PyMuPDF, cleans hyphens/whitespace, divides the text into page-aware 650-word chunks (with 100-word overlap), computes dense vector embeddings using `nomic-embed-text`, and saves the knowledge base to `index.json`.

---

### Step 5: Run the Conversational Assistant

You have two ways to interact with the assistant:

#### Option A: Web GUI Dashboard (Recommended)
Launch the interactive Streamlit interface:
```bash
python3 -m streamlit run app.py
```
Then open your web browser at **`http://localhost:8501`**.
- **💬 Question Panel:** Multi-turn dialogue, real-time streamed responses, and expandable verifiable source citations.
- **📂 Document Explorer:** Inspect repository documents, page metrics, file sizes, and view extracted text page-by-page.
- **📊 Sidebar Metrics:** Real-time visibility into Ollama connectivity, indexed chunk counts, and chat history controls.

#### Option B: Terminal Interactive CLI
To chat directly from your terminal session:
```bash
python3 assistant.py
```
- Type your questions at the prompt; type `exit` or `quit` to end the session.

---

## 📊 Presentation Deck & Documentation

- **PowerPoint Presentation Deck:** An 11-slide presentation file is located at `Domain_Specific_Conversational_Assistant.pptx`.
- **Regenerate / Modify Presentation:** You can modify slide content and re-generate the presentation deck anytime:
  ```bash
  python3 generate_presentation.py
  ```

---

## ⚙️ Configuration Reference

Tuning parameters are accessible at the top of the respective Python files:

| File | Setting | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `embed.py` | `EMBED_MODEL` | `nomic-embed-text` | Ollama embedding model |
| `embed.py` | `CHUNK_SIZE` | `650` | Number of words per chunk |
| `embed.py` | `CHUNK_OVERLAP` | `100` | Overlapping words across adjacent chunks |
| `rag.py` | `VECTOR_CANDIDATES` | `30` | Number of top candidates from vector search |
| `rag.py` | `KEYWORD_CANDIDATES` | `30` | Number of top candidates from BM25 search |
| `rag.py` | `FINAL_CHUNKS` | `8` | Top fused hits before neighboring chunk expansion |
| `rag.py` | `RRF_K` | `60` | Reciprocal Rank Fusion smoothing parameter |
| `rag.py` | `CONTEXT_CHAR_LIMIT`| `24000` | Maximum context character budget fed to the LLM |
| `assistant.py`| `MODEL` | `lfm3-omni:2b` | Default Ollama chat model |
| `assistant.py`| `MAX_TOOL_ROUNDS` | `5` | Maximum autonomous tool-calling iterations |

---

## 🔍 How the System Works (Under the Hood)

1. **Document Ingestion (`embed.py`):** Extracts text from `docs/*.pdf`, cleans hyphenated line wraps, creates overlapping chunks tracking exact start and end page numbers, and creates dense vector embeddings stored in `index.json`.
2. **Hybrid Retrieval (`rag.py`):** For each query, runs **Cosine Vector Search** + **BM25 Lexical Search**, merges candidates via **Reciprocal Rank Fusion (RRF)**, and performs **Neighboring Chunk Expansion** ($n-1, n, n+1$) to ensure unbroken context.
3. **Agentic Tool Loop (`assistant.py` / `app.py`):** An LLM system prompt strictly forbids answering technical questions from memory. The model executes `search_knowledge`, inspects retrieved context, and produces grounded responses citing document names, chunk IDs, and page ranges.
