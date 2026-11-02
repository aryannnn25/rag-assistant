# Domain Specific Conversational Assistant with Memory and Source Grounding

A local, terminal-based conversational AI assistant designed for domain-specific knowledge bases (PDF collections). Powered by Ollama, it combines multi-turn conversation memory with hybrid retrieval (semantic vector search + BM25 keyword matching) and strict source grounding to provide accurate, citation-backed technical answers.

The included corpus focuses on AI research papers, but the assistant can index any text-based PDFs placed in `docs/`.

## Key Pillars

- **Domain-Specific Knowledge Base:** Ingests local domain PDFs, preserving page numbers, chunk boundaries, and document metadata.
- **Conversational Memory:** Preserves multi-turn dialogue context across the session for coherent follow-up questions.
- **Strict Source Grounding:** Employs autonomous function-calling/tool use to query domain documents prior to answering, grounding responses directly with document names, chunk IDs, and page ranges while mitigating hallucination.

## Features

- Local PDF text extraction with PyMuPDF
- Overlapping, page-aware text chunks
- Local embeddings through Ollama's `nomic-embed-text` model
- Hybrid retrieval: cosine-similarity vector search plus BM25-style keyword search
- Reciprocal Rank Fusion (RRF) to combine both rankings
- Neighboring-chunk expansion for surrounding context
- Tool-calling terminal chat assistant with streamed answers
- Source filename, page range, and chunk metadata included in retrieved context

## Project layout

```text
rag-assistant-main/
├── assistant.py       # Interactive chat assistant and tool-calling loop
├── embed.py           # PDF ingestion and embedding-index generation
├── rag.py             # Hybrid search and context construction
├── requirements.txt   # Python dependencies
├── docs/              # Source PDF corpus
└── index.json         # Generated local index (not committed)
```

## Requirements

- Python 3.10 or newer
- [Ollama](https://ollama.com/) installed and running locally
- An Ollama embedding model and a chat model that supports tool calling

The default models are:

```text
Embedding: nomic-embed-text
Chat:      lfm3-omni:2b
```

Pull them before building or running the assistant:

```bash
ollama pull nomic-embed-text
ollama pull lfm3-omni:2b
```

You may use another compatible chat model by changing `MODEL` in `assistant.py`.

## Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate              # macOS / Linux
# venv\\Scripts\\activate               # Windows PowerShell
```

Install dependencies:

```bash
python3 -m pip install -r requirements.txt
```

Add PDFs to `docs/`, then build the index:

```bash
python3 embed.py
```

This creates `index.json` in the project root. Rebuild the index whenever you add, remove, or replace source PDFs, or change the embedding model.

## Usage

Start the assistant:

```bash
python3 assistant.py
```

Example session:

```text
Assistant ready: lfm3-omni:2b
Type 'exit' to quit.

You: How does grouped-query attention differ from multi-query attention?
```

Use `exit` or `quit` to end the session.

## How it works

### 1. Ingestion and indexing

`embed.py` reads each `*.pdf` in `docs/` with PyMuPDF. Extracted text is cleaned, combined into a word stream, and split into overlapping chunks. Each chunk preserves the first and last PDF page it spans.

By default, chunks contain 650 words with 100 words of overlap. Each chunk is embedded through Ollama and stored in `index.json` with this information:

```json
{
  "doc": "example.pdf",
  "chunk": 0,
  "page_start": 1,
  "page_end": 2,
  "text": "Extracted chunk text...",
  "vec": ["embedding values..."]
}
```

### 2. Retrieval

For a query, `rag.py` performs two searches over the generated index:

1. **Vector search** embeds the query and ranks chunks by cosine similarity.
2. **Keyword search** applies BM25-style lexical scoring.

The candidate lists are merged using Reciprocal Rank Fusion. The highest ranked chunks are expanded with their immediately adjacent chunks from the same PDF, giving the chat model additional local context. The assembled context is limited to 24,000 characters.

### 3. Answer generation

`assistant.py` exposes retrieval to the chat model as a `search_knowledge` tool. Its system prompt instructs the model to search the corpus before answering technical questions and to cite document names and pages in the answer.

The assistant keeps conversation history for the current terminal session only; it is not persisted after the process exits.

## Configuration

The main tuning constants are kept at the top of the source files.

| File | Setting | Default | Purpose |
| --- | --- | --- | --- |
| `embed.py` | `EMBED_MODEL` | `nomic-embed-text` | Ollama embedding model |
| `embed.py` | `CHUNK_SIZE` | `650` | Words per source chunk |
| `embed.py` | `CHUNK_OVERLAP` | `100` | Overlap between chunks |
| `rag.py` | `VECTOR_CANDIDATES` | `30` | Vector-search candidates |
| `rag.py` | `KEYWORD_CANDIDATES` | `30` | Keyword-search candidates |
| `rag.py` | `FINAL_CHUNKS` | `8` | Top fused hits before expansion |
| `rag.py` | `RRF_K` | `60` | RRF smoothing constant |
| `rag.py` | `CONTEXT_CHAR_LIMIT` | `24000` | Maximum supplied context |
| `assistant.py` | `MODEL` | `lfm3-omni:2b` | Ollama chat model |
| `assistant.py` | `DEFAULT_K` | `8` | Default retrieval result count |
| `assistant.py` | `MAX_TOOL_ROUNDS` | `5` | Maximum tool-calling rounds |

## Limitations

- This is designed for small local corpora. Search is implemented with Python loops and scans the entire JSON index for every query.
- PDF text extraction works best for digitally generated, text-based PDFs. Scanned documents need OCR before they can be indexed well.
- Retrieval quality depends on the source material, chunking settings, chosen embedding model, and chat model.
- The model is instructed to cite retrieved passages, but citations should be verified when accuracy is important.
- The application does not currently enforce a score threshold for declaring that no relevant source material was found.

## Troubleshooting

### `index.json not found`

Run the indexer first:

```bash
python3 embed.py
```

### Ollama connection or model errors

Confirm Ollama is running and the configured models are installed:

```bash
ollama list
ollama pull nomic-embed-text
ollama pull lfm3-omni:2b
```

### PDFs produce little or no useful text

The PDF may be scanned, protected, or have an unusual layout. Use an OCR'd, text-searchable version where possible.

### You changed the embedding model

Run `python3 embed.py` again. Query and document vectors must use the same embedding model.

## Development notes

Generated files are intentionally ignored by Git:

```text
venv/
models/
index.json
__pycache__/
```

No data leaves the machine when using a local Ollama server. The commented remote Ollama-client configuration in `assistant.py` is an alternative setup; using it changes that privacy property.
