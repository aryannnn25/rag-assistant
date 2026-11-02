import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Theme colors
    PRIMARY = RGBColor(26, 37, 48)       # Deep slate blue
    SECONDARY = RGBColor(41, 128, 185)   # Tech blue
    ACCENT = RGBColor(39, 174, 96)       # Emerald green
    DARK_TEXT = RGBColor(44, 62, 80)     # Charcoal
    LIGHT_BG = RGBColor(248, 249, 250)   # Off white
    CARD_BG = RGBColor(255, 255, 255)
    MUTED_TEXT = RGBColor(127, 140, 141)

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category_text="PROJECT PRESENTATION"):
        # Category label
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(11)
        p_cat.font.bold = True
        p_cat.font.color.rgb = SECONDARY

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.85), Inches(11.5), Inches(0.8))
        tf_t = t_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = PRIMARY

    def set_slide_background(slide, color):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = color
        bg.line.fill.background()
        return bg

    # ==================== SLIDE 1: TITLE ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, PRIMARY)

    # Accent decorative bar
    bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(1.8), Inches(0.8), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()

    # Title box
    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(2.1), Inches(11.0), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Domain Specific Conversational Assistant"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = RGBColor(255, 255, 255)

    p2 = tf.add_paragraph()
    p2.text = "with Memory and Source Grounding"
    p2.font.size = Pt(32)
    p2.font.bold = True
    p2.font.color.rgb = SECONDARY

    # Subtitle box
    sbox = s1.shapes.add_textbox(Inches(1.2), Inches(4.5), Inches(10.5), Inches(1.5))
    stf = sbox.text_frame
    stf.word_wrap = True
    sp1 = stf.paragraphs[0]
    sp1.text = "Offline, Local Hybrid RAG Architecture Powered by Ollama"
    sp1.font.size = Pt(18)
    sp1.font.color.rgb = RGBColor(200, 214, 229)

    sp2 = stf.add_paragraph()
    sp2.text = "PyMuPDF  |  nomic-embed-text  |  Reciprocal Rank Fusion (RRF)  |  Tool-Calling Loop"
    sp2.font.size = Pt(14)
    sp2.font.color.rgb = RGBColor(160, 175, 195)

    # ==================== SLIDE 2: PROBLEM STATEMENT ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Problem Statement: Challenges with Modern LLMs in Domains")

    # 3 Cards
    cards_data_s2 = [
        ("LLM Hallucinations", "Generic LLMs confidently generate fabricated answers and unverifiable citations when asked about specialized research or private documents.", RGBColor(231, 76, 60)),
        ("Privacy & Cloud Costs", "Sending proprietary enterprise or research PDFs to public third-party APIs risks data exposure and creates recurring operational expenses.", RGBColor(230, 126, 34)),
        ("Lack of Source Traceability", "Traditional chatbots lack exact page-level citations, making it difficult for technical practitioners to verify factual authenticity.", RGBColor(52, 152, 219))
    ]

    for idx, (head, desc, color) in enumerate(cards_data_s2):
        left = Inches(0.8 + idx * 3.95)
        top = Inches(2.0)
        card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(3.7), Inches(4.6))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(220, 224, 230)

        # Top indicator tag
        tag = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, left + Inches(0.3), top + Inches(0.4), Inches(0.8), Inches(0.08))
        tag.fill.solid()
        tag.fill.fore_color.rgb = color
        tag.line.fill.background()

        tb = s2.shapes.add_textbox(left + Inches(0.3), top + Inches(0.6), Inches(3.1), Inches(3.5))
        c_tf = tb.text_frame
        c_tf.word_wrap = True
        cp1 = c_tf.paragraphs[0]
        cp1.text = head
        cp1.font.size = Pt(18)
        cp1.font.bold = True
        cp1.font.color.rgb = PRIMARY

        cp2 = c_tf.add_paragraph()
        cp2.space_before = Pt(14)
        cp2.text = desc
        cp2.font.size = Pt(14)
        cp2.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 3: PROPOSED SOLUTION ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "The Solution: Four Pillars of our System")

    pillars = [
        ("1. Domain Knowledge", "Processes local domain PDF collections via PyMuPDF with clean hyphen-wrap removal and exact page numbering.", SECONDARY),
        ("2. Hybrid Retrieval (RRF)", "Combines semantic vector search (nomic-embed-text) with keyword BM25 scoring fused via Reciprocal Rank Fusion.", ACCENT),
        ("3. Conversational Memory", "Maintains chronological multi-turn dialogue context, resolving follow-ups and conversational references.", PRIMARY),
        ("4. Strict Source Grounding", "Autonomous agent tool loop enforces retrieval prior to answering, providing document and page citations.", RGBColor(142, 68, 173))
    ]

    for idx, (title, desc, color) in enumerate(pillars):
        row = idx // 2
        col = idx % 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(2.0 + row * 2.45)
        card = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.1))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(220, 224, 230)

        # Left bar accent
        lbar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, Inches(0.12), Inches(2.1))
        lbar.fill.solid()
        lbar.fill.fore_color.rgb = color
        lbar.line.fill.background()

        tb = s3.shapes.add_textbox(left + Inches(0.35), top + Inches(0.25), Inches(5.1), Inches(1.6))
        ptf = tb.text_frame
        ptf.word_wrap = True
        p1 = ptf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY

        p2 = ptf.add_paragraph()
        p2.space_before = Pt(8)
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 4: ARCHITECTURE FLOW ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "End-to-End System Workflow")

    steps = [
        ("PDF Corpus", "Local files in docs/ folder", PRIMARY),
        ("Text Ingestion", "PyMuPDF + 650/100 word chunks", SECONDARY),
        ("Embedding", "nomic-embed-text to index.json", SECONDARY),
        ("Hybrid Retrieval", "Cosine Vector + BM25 with RRF", ACCENT),
        ("Tool-Calling Agent", "Ollama LLM (search_knowledge)", PRIMARY),
        ("Grounded Answer", "Grounded text + Page/Doc citations", ACCENT)
    ]

    for idx, (stitle, ssub, scolor) in enumerate(steps):
        left = Inches(0.6 + idx * 2.05)
        top = Inches(2.6)
        scard = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(1.9), Inches(2.4))
        scard.fill.solid()
        scard.fill.fore_color.rgb = CARD_BG
        scard.line.color.rgb = scolor
        scard.line.width = Pt(1.5)

        num_box = s4.shapes.add_textbox(left, top + Inches(0.15), Inches(1.9), Inches(0.4))
        np = num_box.text_frame.paragraphs[0]
        np.alignment = PP_ALIGN.CENTER
        np.text = f"Step {idx+1}"
        np.font.size = Pt(12)
        np.font.bold = True
        np.font.color.rgb = scolor

        tb = s4.shapes.add_textbox(left + Inches(0.1), top + Inches(0.6), Inches(1.7), Inches(1.6))
        stf = tb.text_frame
        stf.word_wrap = True
        sp1 = stf.paragraphs[0]
        sp1.alignment = PP_ALIGN.CENTER
        sp1.text = stitle
        sp1.font.size = Pt(14)
        sp1.font.bold = True
        sp1.font.color.rgb = PRIMARY

        sp2 = stf.add_paragraph()
        sp2.space_before = Pt(6)
        sp2.alignment = PP_ALIGN.CENTER
        sp2.text = ssub
        sp2.font.size = Pt(11)
        sp2.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 5: INGESTION & INDEXING ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Ingestion & Indexing Pipeline (embed.py)", "TECHNICAL IMPLEMENTATION")

    features_s5 = [
        ("Text Normalization & Hyphen Cleaning", "Extracts PDF text using PyMuPDF while automatically cleaning hyphenated line wraps (e.g., 'trans- \nformer' -> 'transformer') and excess whitespace."),
        ("Sliding Window Chunking", "Chunks by word counts (CHUNK_SIZE = 650 words, CHUNK_OVERLAP = 100 words), tracking page_start and page_end for every chunk to guarantee source accountability."),
        ("Local Embedding Generation", "Invokes Ollama's local nomic-embed-text model with 8192 token context window, avoiding external API calls or token charges."),
        ("Zero-Dependency Local Index", "Stores chunks, vectors, and page metadata into a portable, lightweight index.json, eliminating the operational overhead of heavy vector databases.")
    ]

    for idx, (title, desc) in enumerate(features_s5):
        top = Inches(1.8 + idx * 1.3)
        c = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.1))
        c.fill.solid()
        c.fill.fore_color.rgb = CARD_BG
        c.line.color.rgb = RGBColor(220, 224, 230)

        tb = s5.shapes.add_textbox(Inches(1.1), top + Inches(0.12), Inches(11.2), Inches(0.9))
        ctf = tb.text_frame
        ctf.word_wrap = True
        p1 = ctf.paragraphs[0]
        p1.text = f"•  {title}"
        p1.font.size = Pt(15)
        p1.font.bold = True
        p1.font.color.rgb = SECONDARY

        p2 = ctf.add_paragraph()
        p2.space_before = Pt(3)
        p2.text = f"    {desc}"
        p2.font.size = Pt(12)
        p2.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 6: HYBRID SEARCH & RRF ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Hybrid Retrieval & Reciprocal Rank Fusion (rag.py)", "CORE ALGORITHM")

    # Card 1: Vector Search
    c1 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(3.7), Inches(4.7))
    c1.fill.solid()
    c1.fill.fore_color.rgb = CARD_BG
    c1.line.color.rgb = SECONDARY
    tb1 = s6.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(3.3), Inches(4.3))
    t1 = tb1.text_frame
    t1.word_wrap = True
    p = t1.paragraphs[0]
    p.text = "1. Dense Vector Search"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p_sub = t1.add_paragraph()
    p_sub.space_before = Pt(8)
    p_sub.text = "• Cosine similarity over normalized vectors\n• Captures high-level semantic meaning and concepts\n• Retrieves Top-30 candidate chunks"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = DARK_TEXT

    # Card 2: BM25
    c2 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.8), Inches(1.9), Inches(3.7), Inches(4.7))
    c2.fill.solid()
    c2.fill.fore_color.rgb = CARD_BG
    c2.line.color.rgb = ACCENT
    tb2 = s6.shapes.add_textbox(Inches(5.0), Inches(2.1), Inches(3.3), Inches(4.3))
    t2 = tb2.text_frame
    t2.word_wrap = True
    p = t2.paragraphs[0]
    p.text = "2. Sparse BM25 Search"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p_sub = t2.add_paragraph()
    p_sub.space_before = Pt(8)
    p_sub.text = "• Pure Python BM25 implementation (k1=1.5, b=0.75)\n• Captures exact domain keywords, acronyms, and codes\n• Retrieves Top-30 candidate chunks"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = DARK_TEXT

    # Card 3: RRF & Context Window
    c3 = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.8), Inches(1.9), Inches(3.7), Inches(4.7))
    c3.fill.solid()
    c3.fill.fore_color.rgb = CARD_BG
    c3.line.color.rgb = RGBColor(142, 68, 173)
    tb3 = s6.shapes.add_textbox(Inches(9.0), Inches(2.1), Inches(3.3), Inches(4.3))
    t3 = tb3.text_frame
    t3.word_wrap = True
    p = t3.paragraphs[0]
    p.text = "3. RRF & Expansion"
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = PRIMARY
    p_sub = t3.add_paragraph()
    p_sub.space_before = Pt(8)
    p_sub.text = "• Reciprocal Rank Fusion: 1 / (60 + rank)\n• Fuses scores without manual tuning\n• Window Expansion: Automatically appends neighboring chunks (chunk ± 1)\n• 24k character context limiter"
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 7: AGENTIC ASSISTANT ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "Source Grounding & Autonomous Tool Loop (assistant.py)", "AGENTIC BEHAVIOR")

    left_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.9), Inches(5.6), Inches(4.7))
    left_card.fill.solid()
    left_card.fill.fore_color.rgb = CARD_BG
    left_card.line.color.rgb = RGBColor(220, 224, 230)

    ltb = s7.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(5.2), Inches(4.3))
    ltf = ltb.text_frame
    ltf.word_wrap = True
    lp1 = ltf.paragraphs[0]
    lp1.text = "Strict Anti-Hallucination Directives"
    lp1.font.size = Pt(18)
    lp1.font.bold = True
    lp1.font.color.rgb = PRIMARY

    bullets_left = [
        "Mandatory Search: LLM is strictly prohibited from answering technical questions from memory without tool use.",
        "Iterative Refinement: Can run up to 5 tool-calling exploration rounds if first search is insufficient.",
        "Forced Verification: If facts are not present in retrieved context, model must state it does not know.",
        "Verifiable Citation: Must explicitly state source document filename and page numbers."
    ]
    for b in bullets_left:
        p = ltf.add_paragraph()
        p.space_before = Pt(8)
        p.text = f"• {b}"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_TEXT

    right_card = s7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.8), Inches(1.9), Inches(5.7), Inches(4.7))
    right_card.fill.solid()
    right_card.fill.fore_color.rgb = PRIMARY
    right_card.line.fill.background()

    rtb = s7.shapes.add_textbox(Inches(7.1), Inches(2.1), Inches(5.2), Inches(4.3))
    rtf = rtb.text_frame
    rtf.word_wrap = True
    rp1 = rtf.paragraphs[0]
    rp1.text = "search_knowledge Tool Definition"
    rp1.font.size = Pt(18)
    rp1.font.bold = True
    rp1.font.color.rgb = SECONDARY

    code_snippet = (
        '{\n'
        '  "name": "search_knowledge",\n'
        '  "description": "Search local PDF knowledge base",\n'
        '  "parameters": {\n'
        '    "query": "technical search terms",\n'
        '    "k": 8\n'
        '  }\n'
        '}\n\n'
        'Output Context Provided to Model:\n'
        '[Source: attention.pdf | Pages: 3-4 | Chunk: 12]\n'
        '"Multi-head attention allows the model to..."'
    )
    rp2 = rtf.add_paragraph()
    rp2.space_before = Pt(10)
    rp2.text = code_snippet
    rp2.font.size = Pt(12)
    rp2.font.color.rgb = RGBColor(230, 240, 250)

    # ==================== SLIDE 8: MEMORY ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Conversational Memory & Multi-Turn Context", "STATEFUL INTERACTION")

    memory_points = [
        ("Multi-Turn Context Preservation", "Maintains chronological message history across user inputs, tool calls, tool responses, and assistant answers in-memory.", SECONDARY),
        ("Co-Reference Resolution", "Enables ambiguous conversational follow-ups such as 'Can you explain the second formula from the paper you just cited?' without re-specifying the document.", ACCENT),
        ("Real-Time Streaming Output", "Uses Ollama's non-blocking token streaming for natural terminal output while preserving the full response in history.", PRIMARY)
    ]

    for idx, (title, desc, color) in enumerate(memory_points):
        top = Inches(2.0 + idx * 1.6)
        card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), top, Inches(11.7), Inches(1.35))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(220, 224, 230)

        bar = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), top, Inches(0.12), Inches(1.35))
        bar.fill.solid()
        bar.fill.fore_color.rgb = color
        bar.line.fill.background()

        tb = s8.shapes.add_textbox(Inches(1.2), top + Inches(0.15), Inches(11.0), Inches(1.1))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY

        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 9: KEY COMPARISON ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Technical Comparison & Project Advantages", "COMPETITIVE EVALUATION")

    rows = [
        ("Feature / Capability", "Standard Cloud RAG", "Our Domain-Specific Assistant"),
        ("Deployment & Cost", "Cloud APIs ($/token, OpenAI/Pinecone)", "100% Local & Free (Ollama + local JSON)"),
        ("Data Privacy & Security", "Data sent to external servers", "Air-gapped / Local (zero external egress)"),
        ("Retrieval Strategy", "Vector-only or basic keyword", "Hybrid (Cosine Vector + BM25) with RRF"),
        ("Context Continuity", "Isolated chunks (fragmented)", "Neighboring chunk expansion (chunk ± 1)"),
        ("Citation Precision", "Loose paragraph match", "Exact Document, Chunk ID, & Page Range"),
        ("Agentic Tool Loop", "One-shot RAG prompt", "Multi-turn autonomous tool-calling (up to 5 rounds)")
    ]

    top_start = Inches(1.8)
    table_shape = s9.shapes.add_table(len(rows), 3, Inches(0.8), top_start, Inches(11.7), Inches(4.9))
    table = table_shape.table
    table.columns[0].width = Inches(3.2)
    table.columns[1].width = Inches(4.2)
    table.columns[2].width = Inches(4.3)

    for r_idx, (c0, c1, c2) in enumerate(rows):
        row = table.rows[r_idx]
        for c_idx, text in enumerate((c0, c1, c2)):
            cell = row.cells[c_idx]
            cell.text = text
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(12)
            if r_idx == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = PRIMARY
                p.font.bold = True
                p.font.color.rgb = RGBColor(255, 255, 255)
            else:
                cell.fill.solid()
                if c_idx == 2:
                    cell.fill.fore_color.rgb = RGBColor(235, 245, 255)
                    p.font.bold = True
                    p.font.color.rgb = SECONDARY
                else:
                    cell.fill.fore_color.rgb = CARD_BG
                    p.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 10: FUTURE SCOPE ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, LIGHT_BG)
    add_header(s10, "Future Enhancements & Scalability Roadmap", "LOOKING FORWARD")

    future_cards = [
        ("Persistent Multi-Session Memory", "Adding SQLite or local vector session storage so user conversational history persists across terminal sessions and reboots.", SECONDARY),
        ("Cross-Encoder Reranker", "Incorporating a local cross-encoder model (e.g., bge-reranker-large) to score candidate chunks following RRF retrieval for pinpoint precision.", ACCENT),
        ("Web & Mobile UI", "Packaging backend endpoints into a lightweight FastAPI service with a modern React or Streamlit front-end.", PRIMARY),
        ("Multimodal PDF Parsing", "Adding OCR and vision-language model support to extract diagrams, tables, and formulas from research papers.", RGBColor(142, 68, 173))
    ]

    for idx, (title, desc, color) in enumerate(future_cards):
        col = idx % 2
        row = idx // 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(2.0 + row * 2.5)

        card = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.7), Inches(2.2))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = RGBColor(220, 224, 230)

        dot = s10.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.4), top + Inches(0.4), Inches(0.25), Inches(0.25))
        dot.fill.solid()
        dot.fill.fore_color.rgb = color
        dot.line.fill.background()

        tb = s10.shapes.add_textbox(left + Inches(0.8), top + Inches(0.3), Inches(4.6), Inches(1.7))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = title
        p1.font.size = Pt(17)
        p1.font.bold = True
        p1.font.color.rgb = PRIMARY

        p2 = tf.add_paragraph()
        p2.space_before = Pt(8)
        p2.text = desc
        p2.font.size = Pt(13)
        p2.font.color.rgb = DARK_TEXT

    # ==================== SLIDE 11: CONCLUSION & QA ====================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11, PRIMARY)

    # Accent decorative bar
    bar = s11.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(2.0), Inches(0.8), Inches(0.1))
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()

    tb = s11.shapes.add_textbox(Inches(1.2), Inches(2.3), Inches(11.0), Inches(3.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "Thank You!"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)

    p2 = tf.add_paragraph()
    p2.space_before = Pt(16)
    p2.text = "Domain Specific Conversational Assistant with Memory and Source Grounding"
    p2.font.size = Pt(22)
    p2.font.color.rgb = SECONDARY

    p3 = tf.add_paragraph()
    p3.space_before = Pt(12)
    p3.text = "Questions & Answers"
    p3.font.size = Pt(18)
    p3.font.color.rgb = RGBColor(200, 214, 229)

    output_path = "/Users/aryan/Desktop/rag-assistant-main/Domain_Specific_Conversational_Assistant.pptx"
    prs.save(output_path)
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()
