import json
import os
from pathlib import Path
import streamlit as st
import fitz  # PyMuPDF

# Page configuration
st.set_page_config(
    page_title="Domain Conversational Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "docs"
INDEX_FILE = BASE_DIR / "index.json"

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 8px;
        padding: 12px 16px;
        border: 1px solid #E2E8F0;
    }
    .source-tag {
        display: inline-block;
        background-color: #EFF6FF;
        color: #1D4ED8;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ----------------- SESSION STATE -----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello! I am your domain-specific research assistant. Ask me questions about the documents in your knowledge base."
        }
    ]

# ----------------- SIDEBAR: DOCUMENTS & STATUS -----------------
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/books.png", width=50)
    st.title("Knowledge Base")
    st.caption("Active Domain Documents")

    # List documents
    DOCS_DIR.mkdir(exist_ok=True)
    pdf_files = sorted(DOCS_DIR.glob("*.pdf"))

    st.subheader(f"Repository Documents ({len(pdf_files)})")
    
    if not pdf_files:
        st.warning("No PDF documents found in `docs/`.")
    else:
        for idx, pdf in enumerate(pdf_files, 1):
            file_size_mb = pdf.stat().st_size / (1024 * 1024)
            with st.expander(f"📄 {pdf.name}", expanded=False):
                st.write(f"**Size:** {file_size_mb:.2f} MB")
                try:
                    doc = fitz.open(pdf)
                    st.write(f"**Pages:** {len(doc)}")
                    doc.close()
                except Exception:
                    st.write("**Pages:** Unable to read")

    st.divider()

    # Index Status
    st.subheader("Index Status")
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, "r", encoding="utf-8") as f:
                index_data = json.load(f)
            st.success(f"Index Active: {len(index_data)} chunks indexed")
        except Exception:
            st.info("Index file present")
    else:
        st.warning("⚠️ `index.json` not generated yet.\nRun `python3 embed.py` to index.")

    st.divider()

    # System Status
    st.subheader("System Status")
    try:
        import ollama
        client = ollama.Client(host="http://localhost:11434")
        models = client.list()
        model_names = [m.model for m in models.models]
        st.success("Ollama Engine Connected")
        with st.expander("Available Models", expanded=False):
            for m in model_names:
                st.write(f"- `{m}`")
    except Exception as e:
        st.warning("Ollama not running on localhost:11434.\nStart it with `ollama serve`.")

    if st.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversation history cleared. What would you like to explore?"
            }
        ]
        st.rerun()

# ----------------- MAIN PANEL -----------------
st.markdown('<div class="main-header">Domain Specific Conversational Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-turn Memory with Hybrid RAG & Verifiable Source Grounding</div>', unsafe_allow_html=True)

# Tabs: Ask Questions vs Document Viewer
tab_chat, tab_docs = st.tabs(["💬 Question Panel", "📂 Document Explorer"])

with tab_chat:
    # Display message history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if "sources" in msg and msg["sources"]:
                with st.expander("🔍 View Retrieved Sources & Citations"):
                    for s in msg["sources"]:
                        st.markdown(f"**Doc:** `{s['document']}` | **Pages:** `{s['pages']}` | **Chunk:** `{s['chunk']}`")
                        if "text" in s:
                            st.caption(s["text"][:300] + "...")

    # Chat input
    if prompt := st.chat_input("Ask a question about the indexed papers..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Assistant generation
        with st.chat_message("assistant"):
            try:
                import ollama
                from rag import rag_search, build_context
                
                # Check if index exists
                if not INDEX_FILE.exists():
                    ans = "⚠️ `index.json` not found. Please run `python3 embed.py` first to generate embeddings for your documents."
                    st.error(ans)
                    st.session_state.messages.append({"role": "assistant", "content": ans})
                else:
                    with st.spinner("Searching domain documents and reasoning..."):
                        # Retrieve relevant passages
                        results = rag_search(prompt, k=6)
                        context = build_context(results)

                        # Prepare sources metadata
                        sources_meta = [
                            {
                                "document": item["doc"],
                                "pages": f"{item.get('page_start', '?')}-{item.get('page_end', '?')}",
                                "chunk": item["chunk"],
                                "text": item.get("text", "")
                            }
                            for item in results
                        ]

                        # Prompt with grounded context and memory
                        system_msg = (
                            "You are a technical research assistant connected to a PDF knowledge base.\n"
                            "RULES:\n"
                            "- Base your answer ONLY on the retrieved document context below.\n"
                            "- Cite document names and page numbers in your response.\n"
                            "- If the context does not contain the answer, state that clearly.\n"
                            "- Explain technical concepts thoroughly.\n\n"
                            f"CONTEXT FROM DOCUMENTS:\n{context}"
                        )

                        # Build message array for Ollama
                        llm_messages = [{"role": "system", "content": system_msg}]
                        for m in st.session_state.messages[-6:]:  # last 6 turns for conversational memory
                            if m["role"] in ("user", "assistant"):
                                llm_messages.append({"role": m["role"], "content": m["content"]})

                        # Model inference
                        MODEL_NAME = "lfm3-omni:2b"
                        client = ollama.Client(host="http://localhost:11434")
                        
                        response_placeholder = st.empty()
                        full_response = ""

                        # Stream output
                        stream = client.chat(
                            model=MODEL_NAME,
                            messages=llm_messages,
                            stream=True
                        )

                        for chunk in stream:
                            if chunk.message.content:
                                full_response += chunk.message.content
                                response_placeholder.markdown(full_response + "▌")
                        
                        response_placeholder.markdown(full_response)

                        # Display citations expander
                        if sources_meta:
                            with st.expander("🔍 Verified Grounding Sources"):
                                for s in sources_meta:
                                    st.markdown(f"• **{s['document']}** (Pages {s['pages']}) - Chunk #{s['chunk']}")

                        # Save to history
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": full_response,
                            "sources": sources_meta
                        })

            except Exception as e:
                err_msg = f"Error during query execution: {e}\n\nPlease verify that Ollama is running (`ollama serve`)."
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})

with tab_docs:
    st.subheader("Document Viewer & Text Inspection")
    if not pdf_files:
        st.info("No documents found in `docs/` folder.")
    else:
        selected_pdf_name = st.selectbox(
            "Select a document to inspect:",
            options=[pdf.name for pdf in pdf_files]
        )
        selected_path = DOCS_DIR / selected_pdf_name

        try:
            doc = fitz.open(selected_path)
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Total Pages", len(doc))
            with col_info2:
                st.metric("File Size", f"{selected_path.stat().st_size / (1024*1024):.2f} MB")
            with col_info3:
                st.metric("Format", "PDF Document")

            # Page selector
            page_num = st.slider("Select Page to View Text", min_value=1, max_value=len(doc), value=1)
            page_text = doc[page_num - 1].get_text("text")

            st.markdown(f"#### Page {page_num} Content:")
            st.text_area("Extracted Text", value=page_text, height=450, disabled=True)
            doc.close()
        except Exception as e:
            st.error(f"Failed to read PDF: {e}")
