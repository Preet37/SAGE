# Future Ideas — Learner Memory, Personalization & User-Uploaded Content

From demo feedback, April 2026.

---

## Idea 1: Learner Memory — Cross-Course Continuity & Personalization

### The Problem

Today, every tutor conversation starts from zero. The tutor has no memory of:
- What the learner already knows (from prior lessons or courses)
- Misconceptions they've struggled with before
- Their preferred learning style (analogies vs code vs math)
- Connections between what they learned in Course A and what they're studying in Course B

A learner who mastered attention mechanisms in "Intro to LLMs" shouldn't get the same "let me explain attention from scratch" treatment when they encounter multi-head attention in "Agentic AI Frameworks." The tutor should say: "You already understand how attention computes weighted averages — multi-head attention just runs that process N times in parallel with different learned projections."

### What to Store

**Three layers of learner memory, each with different granularity and cost:**

#### Layer 1: Structured Progress Profile (cheap, always available)

A compact JSON document per user, updated after each session. The tutor system prompt includes this profile as context.

```
{
  "user_id": "abc123",
  "concepts_mastered": [
    {"concept": "self-attention", "confidence": 0.9, "last_seen": "2026-04-10", "course": "intro-to-llms"},
    {"concept": "backpropagation", "confidence": 0.7, "last_seen": "2026-04-08", "course": "ml-foundations"}
  ],
  "concepts_struggling": [
    {"concept": "kl-divergence", "attempts": 3, "last_misconception": "confused KL divergence with JS divergence"}
  ],
  "learning_preferences": {
    "preferred_modality": "visual",     // inferred from what they engage with
    "preferred_depth": "intermediate",  // inferred from question complexity
    "responds_well_to": ["analogies", "code_examples"],
    "responds_poorly_to": ["formal_math_notation"]
  },
  "courses_completed": ["intro-to-llms"],
  "courses_active": ["agentic-ai-frameworks"],
  "total_sessions": 47,
  "total_questions_asked": 182
}
```

**How it gets built:** After each tutor session, a lightweight LLM call (fast model) reviews the conversation and extracts:
- New concepts the learner demonstrated understanding of
- Concepts they struggled with + the specific misconception
- Style signals (did they ask for code? did they ask to simplify?)

This is append-and-merge — new entries update existing ones, confidence decays over time (spaced repetition signal).

**DB model:**

```python
class LearnerProfile(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", unique=True, index=True)
    profile_data: str  # JSON blob — the structured profile above
    updated_at: datetime
```

**Cost:** One fast-model LLM call per session (~$0.001). Profile stays small (< 2KB for most learners). Always fits in the tutor system prompt.

#### Layer 2: Conversation Summaries (medium cost, searchable)

Full chat transcripts are already stored in `ChatMessage` and `ExplorationMessage`. But raw messages are too large to include in future prompts. Instead, generate a summary per session:

```python
class SessionSummary(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    session_id: str  # TutorSession.id or ExplorationSession.id
    session_type: str  # "lesson" | "exploration"
    lesson_id: Optional[str] = None
    course_slug: Optional[str] = None
    summary: str  # 100-200 word summary of what was discussed/learned
    concepts_touched: str  # JSON list of concept slugs
    key_moments: str  # JSON: breakthroughs, confusions, "aha" moments
    created_at: datetime
```

**How summaries get used:**
- When the tutor starts a new session, retrieve the 3-5 most relevant past summaries (by concept overlap with the current lesson) and inject into the system prompt as a "LEARNER HISTORY" section.
- "Last time you worked on LoRA, you were confused about rank selection. Let's see if that clicks today."

**How summaries get built:** End-of-session LLM call with a focused prompt: "Summarize this tutoring session in 150 words. What did the learner understand? What did they struggle with? Any breakthrough moments?"

**Cost:** One fast-model call per session. Summaries are small. Retrieval is a simple SQL query + concept-matching (no vector DB needed for this scale).

#### Layer 3: Full Chat Archive + Vector Search (higher cost, optional)

For learners who want to search their own history ("When did I learn about attention?"), store embeddings of chat messages and enable semantic search.

```python
class MessageEmbedding(SQLModel, table=True):
    id: str = Field(primary_key=True)
    message_id: str  # ChatMessage.id or ExplorationMessage.id
    user_id: str = Field(foreign_key="user.id", index=True)
    embedding: bytes  # or use pgvector if on Postgres
    created_at: datetime
```

**When to build this:** Only after Layers 1 and 2 are proven useful. Most of the personalization value comes from the structured profile + summaries. Full vector search is a "nice to have" for power users.

### How the Tutor Uses Memory

**System prompt injection (minimal change to existing architecture):**

The current system prompt in `system_prompt_v2.py` already has sections for lesson context, reference KB, and available images. Add a new `LEARNER CONTEXT` section:

```
## LEARNER CONTEXT

### What This Learner Already Knows
- Self-attention (high confidence, learned in Intro to LLMs, April 10)
- Backpropagation (moderate confidence, ML Foundations, April 8)

### Known Struggles
- KL divergence: previously confused it with JS divergence (3 attempts)

### Learning Style
- Prefers: visual explanations, analogies, code examples
- Avoid: heavy formal math notation unless they ask

### Recent Sessions (this course)
- Apr 11: Explored LoRA fine-tuning. Understood rank as "compression." Struggled with when to use LoRA vs full fine-tuning.
- Apr 10: Covered self-attention. Breakthrough: understood Q/K/V as "question/key/value in a database lookup."

### Cross-Course Connections
- From ML Foundations: already understands gradient descent, loss functions, regularization
- From Intro to LLMs: solid on tokenization, embeddings, transformer architecture
```

The tutor then naturally weaves in references: "Remember how you thought of Q/K/V as a database lookup? Multi-head attention is like running multiple such lookups in parallel, each one looking for different kinds of relationships."

### Cross-Course Weaving — The "Connect the Dots" Feature

This was already listed as a future idea in the handoff summary under "AI-First Lesson Layout." With learner memory, it becomes much more powerful:

- **Without memory:** "How does attention relate to LoRA?" — generic answer from the KB
- **With memory:** "You understood attention as weighted averages. LoRA modifies the weight matrices that *produce* those attention weights. So when you fine-tune with LoRA, you're changing *what the model pays attention to* without rewriting the entire attention mechanism."

The tutor can proactively make connections: "This is similar to what you learned about regularization in ML Foundations — LoRA's low rank is a form of regularization on the weight updates."

### Implementation Plan

**Phase 1 — Structured Profile (1-2 days)**
1. Add `LearnerProfile` model
2. Add post-session profile updater (fast LLM call after session ends)
3. Inject profile into tutor system prompt
4. Test: does the tutor reference prior knowledge?

**Phase 2 — Session Summaries (1-2 days)**
1. Add `SessionSummary` model
2. Add end-of-session summarizer
3. Retrieve relevant summaries by concept overlap at session start
4. Inject summaries into system prompt

**Phase 3 — Learner Dashboard (2-3 days)**
1. Frontend "My Progress" page showing concepts mastered/struggling
2. Timeline of sessions with summaries
3. Cross-course concept map visualization (which concepts from Course A connect to Course B)
4. Confidence decay visualization (concepts fading without review → nudge to revisit)

**Phase 4 — Full Archive Search (later, if needed)**
1. Embed messages with a fast embedding model
2. Semantic search endpoint for "find when I discussed X"
3. Learner-facing search UI

---

## Idea 1b: Personal Learning Wiki — "Obsidian for Learners"

### The Vision

Every learner gets a personal wiki that grows as they learn. Think Obsidian's graph view, but auto-populated by the AI tutor.

**What goes in the personal wiki:**
- **Concept nodes** — one page per concept the learner has encountered, auto-generated from their conversations. Each page has:
  - The learner's own understanding (extracted from their chat messages — "I think of attention as a spotlight")
  - The tutor's explanation (the best explanation that resonated with this learner)
  - Connected concepts (bidirectional links)
  - Resources they found helpful
  - Questions they still have
- **Session logs** — linked to concept pages, providing the "source" for each understanding
- **Custom notes** — learner can add their own notes, corrections, annotations
- **Graph view** — interactive concept map showing what they know, how concepts connect, and where gaps exist

### How It Differs from Generic Note-Taking

Obsidian is bottom-up: you create notes and link them yourself. The learner wiki is top-down: the AI creates the structure from your learning activity, and you refine it.

**Auto-population flow:**
1. Learner has a tutoring session about "self-attention"
2. Post-session, the system creates/updates the learner's "Self-Attention" concept page:
   - Adds the learner's understanding ("I think of Q/K/V as a database lookup")
   - Links to related concepts (attention, embeddings, transformers)
   - Marks confidence level
   - Links to the session transcript
3. When the learner later studies "multi-head attention," the tutor checks their wiki and says "Your database lookup analogy for attention is a great foundation. Multi-head attention is like running 8 different database lookups in parallel..."

### Data Model

```python
class LearnerWikiPage(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    concept_slug: str  # maps to the platform's concept taxonomy
    title: str
    content: str  # markdown — auto-generated + user-edited
    understanding_level: str  # "intuitive" | "working" | "deep"
    auto_summary: str  # LLM-generated summary of learner's understanding
    linked_concepts: str  # JSON list of related concept slugs
    source_sessions: str  # JSON list of session IDs that contributed
    user_notes: Optional[str]  # learner's own additions
    created_at: datetime
    updated_at: datetime

class LearnerWikiLink(SQLModel, table=True):
    """Bidirectional concept links in a learner's personal wiki."""
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    from_concept: str
    to_concept: str
    link_type: str  # "prerequisite" | "related" | "extends" | "contrasts"
    auto_generated: bool = True
```

### Why This Is Powerful

1. **Spaced repetition signals** — concepts with declining confidence get surfaced: "You haven't revisited KL divergence in 2 weeks. Want a quick refresher?"
2. **Gap detection** — the graph shows disconnected clusters. "You understand attention and LoRA separately, but haven't connected them. Want to explore how LoRA modifies attention weights?"
3. **Portfolio/proof of learning** — shareable. "Here's everything I've learned about transformers, with my own understanding in my own words."
4. **Onboarding for new courses** — when a learner starts a new course, the system checks their wiki and skips/accelerates concepts they already own.

### Implementation Considerations

- The wiki should be **read-heavy, write-light**. Updates happen post-session (background), not during. The tutor reads from it at session start.
- Start with a simple flat list of concept pages before building the graph view. The graph is a visualization layer on top of `LearnerWikiLink` data.
- The concept slugs should map to the platform's existing concept taxonomy (517 concepts in `concept-map.md`), but learners can also create custom concepts outside the taxonomy.

---

## Idea 2: User-Uploaded Content — "Teach Me From My Book"

### The Problem

Learners often have specific materials they want to study from:
- A textbook chapter assigned by their professor
- Their own class notes
- A paper they need to understand for a journal club
- Slides from a conference talk
- A code repository they need to learn

Currently, the tutor can only teach from its curated wiki. If a learner wants to study from Goodfellow's Deep Learning Chapter 10, the tutor has to rely on its general knowledge rather than the specific content of that chapter.

### How It Should Work

**Upload flow:**
1. Learner uploads a file (PDF, markdown, text, images of notes, code files)
2. System processes the file → extracted text, cleaned, chunked
3. Learner says "Teach me this" or asks questions about the uploaded content
4. Tutor uses the uploaded content as its primary knowledge source, supplemented by its wiki

**Two modes of using uploaded content:**

#### Mode A: "Teach Me This" (content-first)

The learner uploads a textbook chapter and says "Help me understand this." The tutor:
1. Reads the content, identifies key concepts and their dependencies
2. Creates a learning plan (which concepts to cover in what order)
3. Teaches Socratically, using the uploaded content as the source of truth
4. Cross-references with its wiki for additional explanations, analogies, and misconceptions

This is different from "summarize this document." The tutor doesn't just explain — it teaches, asks questions, checks understanding, and adapts.

#### Mode B: "Help Me Study From My Notes" (revision mode)

The learner uploads their own notes and says "Quiz me on this" or "What am I missing?" The tutor:
1. Reads the notes, identifies what the learner has captured
2. Identifies gaps or misconceptions in the notes
3. Generates targeted questions to test understanding
4. Points out what's missing: "Your notes cover attention weights but don't mention the softmax normalization step — that's crucial because..."

### Technical Design

#### File Processing Pipeline

```
Upload → Extract Text → Clean → Chunk → Summarize → Concept-Map → Ready
```

**Extraction by file type:**
- **PDF**: `pymupdf` for text + images, OCR fallback for scanned pages
- **Markdown/text**: direct use
- **Images of notes**: vision LLM to extract text + structure (handwritten OCR + layout understanding)
- **Code files**: syntax-aware chunking (by function/class), docstring extraction
- **Slides (PPTX)**: `python-pptx` for text + images per slide

**Processing outputs stored per upload:**

```python
class UserUpload(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    filename: str
    file_type: str  # "pdf" | "markdown" | "text" | "image" | "code" | "slides"
    file_size_bytes: int
    extracted_text: str  # full cleaned text
    summary: str  # LLM-generated summary (500-1000 words)
    concept_map: str  # JSON: extracted concepts + dependencies
    chunk_count: int
    processing_status: str  # "processing" | "ready" | "failed"
    created_at: datetime

class UploadChunk(SQLModel, table=True):
    id: str = Field(primary_key=True)
    upload_id: str = Field(foreign_key="userupload.id", index=True)
    chunk_index: int
    content: str
    concepts: str  # JSON list of concepts in this chunk
    embedding: Optional[bytes] = None  # for semantic retrieval within the document
```

#### How the Tutor Uses Uploaded Content

**Option A: Full context injection (small uploads < 15K words)**

For a single chapter or set of notes, just include the full text in the system prompt alongside the reference KB. The tutor sees both the learner's material and its own wiki knowledge.

System prompt addition:
```
## LEARNER'S UPLOADED MATERIAL

The learner uploaded: "Chapter 10 - Sequence Modeling from Goodfellow Deep Learning textbook"

<uploaded_content>
{full text of the chapter}
</uploaded_content>

TEACHING RULES FOR UPLOADED CONTENT:
- Use this material as the primary source. The learner wants to learn THIS content.
- When the learner asks about a concept, ground your explanation in how the uploaded material presents it.
- Supplement with your reference KB for additional context, analogies, and common misconceptions.
- If the uploaded material contains errors or outdated information, note this gently.
- Do NOT just summarize the material. Teach it Socratically — ask questions, check understanding, build incrementally.
```

**Option B: RAG over uploaded content (large uploads > 15K words)**

For full textbooks or large codebases, chunk and embed the content. At each turn, retrieve the most relevant chunks based on the current conversation topic and inject them.

This is one of the few cases where RAG makes sense — the content is a single authoritative source (the learner's book), not a scattered knowledge base. Retrieval quality is higher because the document is cohesive.

**Option C: Hybrid — summary + targeted retrieval**

Include the LLM-generated summary (always fits in context) plus the most relevant chunks for the current question. Best of both worlds.

#### Integration with Existing Architecture

The tutor's tool system already supports dynamic context injection. Add a new tool:

```python
{
    "name": "search_uploaded_content",
    "description": "Search the learner's uploaded materials for relevant content. Use when the learner asks about something covered in their uploaded files.",
    "parameters": {
        "query": "what to search for in the uploaded content",
        "upload_id": "optional — specific upload to search, or search all"
    }
}
```

This fits cleanly into the existing agent loop — the model decides when to consult the uploaded content, just like it decides when to search the web or look up images.

### Notes Upload Specifically — Study Companion Mode

When a learner uploads their own notes, the system can do something unique: **compare the learner's understanding against the wiki's ground truth.**

```
LEARNER'S NOTES on "Self-Attention":
"Attention is when the model looks at all other words to decide how important each one is. 
It uses Q and K matrices to compute scores, then multiplies by V to get the output."

WIKI GROUND TRUTH (from reference KB):
- Self-attention computes compatibility between all positions in a sequence
- Q, K, V are linear projections of the input (not separate matrices — same input, different projections)
- Scores are scaled by sqrt(d_k) to prevent softmax saturation
- Output is a weighted sum of values, where weights come from softmax of scaled dot-product scores
```

The tutor can then say: "Your notes capture the high-level idea well! Two things to refine: Q, K, and V aren't separate matrices — they're three different linear projections of the *same* input. And there's a scaling step (divide by sqrt(d_k)) before the softmax that your notes don't mention — without it, for large dimensions the dot products get so large that softmax saturates and gradients vanish."

### Implementation Plan

**Phase 1 — Single File Upload + Full Context (2-3 days)**
1. Add `UserUpload` model + file upload endpoint
2. Text extraction pipeline (PDF via pymupdf, markdown direct, images via vision LLM)
3. Inject full text into tutor system prompt for small files
4. Frontend: upload button in chat, "Teaching from: [filename]" indicator

**Phase 2 — Notes Comparison Mode (1-2 days)**
1. When uploaded content is identified as "notes" (short, informal, personal), switch to comparison mode
2. Cross-reference against wiki ground truth for the relevant concepts
3. Tutor proactively identifies gaps and misconceptions in the notes

**Phase 3 — Large File RAG (2-3 days)**
1. Chunk large uploads, embed with fast embedding model
2. `search_uploaded_content` tool for the agent
3. Hybrid retrieval: summary always in context + relevant chunks per turn

**Phase 4 — Persistent Library (later)**
1. Learners can save uploads to their library
2. Re-use uploaded materials across sessions
3. Share uploaded materials with study groups

---

## Idea 3: Learning Progress Visualization — "How Far I've Come"

### The Problem

Learners have no visibility into their own growth. They can't see:
- Which concepts they've mastered across all courses
- How their understanding has deepened over time
- Where their knowledge gaps are
- How much they've engaged with the platform

### What to Show

**Progress Dashboard (new page, linked from AppHeader):**

1. **Concept Mastery Map** — visual graph of all concepts encountered, colored by confidence level (green = mastered, yellow = working, red = struggling, gray = not yet encountered). Clicking a concept shows when it was learned, which sessions covered it, and the learner's own understanding.

2. **Learning Timeline** — chronological view of sessions, showing what was covered, breakthroughs, and struggles. Like a Git commit history for learning.

3. **Course Progress** — per-course completion bars, but enriched with concept mastery (not just "lessons completed"). A lesson isn't truly "done" when you click through it — it's done when you've demonstrated understanding of its key concepts.

4. **Streak & Engagement** — daily/weekly learning streaks, total time, questions asked, concepts mastered. Gamification lite — enough to motivate, not enough to distract.

5. **Knowledge Connections** — cross-course concept map showing how learnings from different courses connect. "Your understanding of embeddings (from Intro to LLMs) is the foundation for your current study of RAG (in Agentic AI)."

### Data Sources

All of this can be derived from data we already store or will store with Idea 1:
- `UserLessonProgress` — lesson completion
- `ChatMessage` / `ExplorationMessage` — engagement metrics
- `TutorSession` / `ExplorationSession` — session frequency and duration
- `LearnerProfile` (new, from Idea 1) — concept mastery and preferences
- `SessionSummary` (new, from Idea 1) — session highlights and breakthroughs

No new data collection infrastructure — just new views on existing data.

---

## Priority & Dependencies

| Idea | Effort | Impact | Dependencies |
|------|--------|--------|--------------|
| 1 Phase 1 (Structured Profile) | 1-2 days | High — immediate personalization | None |
| 1 Phase 2 (Session Summaries) | 1-2 days | High — cross-session continuity | Phase 1 |
| 2 Phase 1 (Single File Upload) | 2-3 days | High — unlocks "teach from my book" | None |
| 3 (Progress Dashboard) | 2-3 days | Medium — learner motivation | Idea 1 Phase 1 |
| 1 Phase 3 (Learner Dashboard) | 2-3 days | Medium — visibility into own learning | Phase 2 |
| 2 Phase 2 (Notes Comparison) | 1-2 days | Medium — unique differentiation | Phase 1 |
| 1b (Personal Wiki) | 3-5 days | High but later — needs concepts working first | Idea 1 Phase 1-2 |
| 2 Phase 3 (Large File RAG) | 2-3 days | Medium — needed only for textbook-length uploads | Phase 1 |

**Recommended order:** Idea 1 Phase 1 → Idea 2 Phase 1 → Idea 1 Phase 2 → Idea 3 → then iterate.

Start with the structured profile (cheapest, most impactful) and single file upload (highest user demand). Session summaries and the progress dashboard follow naturally. The personal wiki is the ambitious long-term play but needs the foundation of learner profiles and summaries to be meaningful.

---

## Key Design Principles

1. **Append-only, summarize-up.** Raw chats are already stored. Layer summaries and profiles on top. Never reprocess raw messages at runtime — do it post-session in the background.

2. **Inject into existing architecture.** The tutor already reads a system prompt with sections for lesson context, reference KB, and images. Learner memory is just another section. No new agent architecture needed.

3. **The learner owns their data.** Personal wiki pages, uploaded content, session summaries — all exportable, all visible. The platform doesn't just use this data for personalization; it shows it back to the learner.

4. **Graceful degradation.** If the profile is empty (new user), the tutor works exactly as it does today. Memory is additive, not required.

5. **Fast model for metadata extraction.** Profile updates and session summaries use the fast model (GPT-4.1-mini). The cost per session is negligible. Don't gate personalization behind expensive model calls.
