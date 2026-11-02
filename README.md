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

- **Web GUI & Terminal Interfaces:** Choose between a modern browser-based Streamlit dashboard or an interactive CLI.
- **Document Explorer & Text Inspector:** Real-time GUI panel to view indexed PDFs, inspect page counts, file sizes, and review extracted text page-by-page.
- **Page-Aware PDF Extraction:** Text extraction with PyMuPDF that automatically repairs hyphenated line wraps.
- **Sliding-Window Chunking:** Word-based chunking (650 words with 100-word overlap) tracking exact start and end page numbers.
- **Hybrid Search Engine:** Combines dense cosine-similarity embeddings (`nomic-embed-text`) with sparse BM25 keyword scoring.
- **Reciprocal Rank Fusion (RRF):** Fuses dense and sparse rankings robustly ($k=60$) without requiring score normalization.
- **Neighboring Chunk Expansion:** Automatically retrieves adjacent chunks ($n-1, n, n+1$) to ensure complete context without mid-sentence truncations.
- **Presentation Deck Included:** Comes with a built-in PowerPoint presentation (`Domain_Specific_Conversational_Assistant.pptx`) for project reviews and evaluations.

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

## 🛠️ Prerequisites & Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running locally
- Default local models:
  - **Embedding:** `nomic-embed-text`
  - **Chat Model:** `lfm3-omni:2b`

Pull the models before running:

```bash
ollama pull nomic-embed-text
ollama pull lfm3-omni:2b
```

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/aryannnn25/rag-assistant.git
   cd rag-assistant
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate              # macOS / Linux
   # venv\Scripts\activate               # Windows
   ```

3. **Install dependencies:**
   ```bash
   python3 -m pip install -r requirements.txt
   ```

4. **Add PDFs and build the Knowledge Base:**
   Place your domain PDF documents inside the `docs/` folder, then run:
   ```bash
   python3 embed.py
   ```
   *This parses the PDFs and saves chunks, page numbers, and embeddings into `index.json`.*

---

## 🖥️ Running the Application

### Option 1: Web GUI Dashboard (Recommended)
Launch the Streamlit web interface with the interactive Question Panel and Document Explorer:

```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

**GUI Highlights:**
- **💬 Question Panel:** Chat interface with streaming responses, conversational memory, and expandable source grounding citations.
- **📂 Document Explorer:** Dropdown to inspect any PDF in `docs/`, see its metadata, and read any page's text via a slider.
- **📊 Knowledge Base Sidebar:** Live metrics on indexed chunk count, PDF sizes, and Ollama connectivity.

---

### Option 2: Terminal Interactive CLI
To run the assistant directly in your terminal:

```bash
python3 assistant.py
```

Type your questions at the prompt; type `exit` or `quit` to leave.

---

## 📊 Presentation Deck & Guide

- **PowerPoint Presentation:** Ready-to-present 16:9 widescreen presentation saved at `Domain_Specific_Conversational_Assistant.pptx`.
- **Regenerate Presentation:** You can customize and regenerate the slides anytime by running:
  ```bash
  python3 generate_presentation.py
  ```

---

## ⚙️ Configuration Reference

Key constants can be configured directly at the top of each file:

| File | Setting | Default | Purpose |
| :--- | :--- | :--- | :--- |
| `embed.py` | `EMBED_MODEL` | `nomic-embed-text` | Ollama embedding model |
| `embed.py` | `CHUNK_SIZE` | `650` | Words per text chunk |
| `embed.py` | `CHUNK_OVERLAP` | `100` | Overlapping words across chunks |
| `rag.py` | `VECTOR_CANDIDATES` | `30` | Vector search top candidate limit |
| `rag.py` | `KEYWORD_CANDIDATES` | `30` | BM25 keyword search candidate limit |
| `rag.py` | `FINAL_CHUNKS` | `8` | Top fused hits before neighbor expansion |
| `rag.py` | `RRF_K` | `60` | Reciprocal Rank Fusion smoothing factor |
| `rag.py` | `CONTEXT_CHAR_LIMIT`| `24000` | Character ceiling for model context |
| `assistant.py`| `MODEL` | `lfm3-omni:2b` | Default Ollama LLM |
| `assistant.py`| `MAX_TOOL_ROUNDS` | `5` | Maximum autonomous search rounds |

---

## 🤝 Contributing & License

Feel free to fork, open pull requests, and contribute to extending multi-session memory, multimodal PDF parsing, or web endpoints!
