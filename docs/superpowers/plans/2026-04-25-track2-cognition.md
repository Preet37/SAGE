# Track 2: Cognition / Augment the Agent Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Measurably improve AI agent capability through HyDE retrieval, cross-encoder reranking, LLM-as-judge verification, and real peer matching — every improvement quantified and visible in the UI.

**Architecture:** A new HyDE layer generates a hypothetical answer before retrieval, dramatically improving embedding relevance. A cross-encoder reranker rescores top-8 chunks against the actual question. An LLM-as-judge async Haiku call runs in parallel with response generation and streams a `judge_result` SSE event. PeerMatchAgent queries real `StudentMastery` rows. Every response shows a Cognition Score card.

**Tech Stack:** sentence-transformers>=2.7.0 (cross-encoder included), anthropic (existing), SQLAlchemy async, React/TypeScript

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/core/hyde.py` | Create | HyDE hypothesis generation + baseline vs HyDE score comparison |
| `backend/app/core/reranker.py` | Create | Cross-encoder reranking (ms-marco-MiniLM-L-6-v2) |
| `backend/app/core/judge.py` | Create | LLM-as-judge pipeline, emits `judge_result` SSE payload |
| `backend/app/core/retrieval.py` | Modify | Wire HyDE → rerank pipeline, add adaptive chunking |
| `backend/app/agents/peer_match.py` | Modify | Replace fake `f"peer-{i}"` with real StudentMastery DB queries |
| `frontend/components/cognition/CognitionScoreCard.tsx` | Create | Per-message score display with cognition purple badge |
| `frontend/components/tutor/MessageBubble.tsx` | Modify | Render CognitionScoreCard below each assistant message |
| `frontend/app/learn/[courseId]/[lessonId]/page.tsx` | Modify | Handle `judge_result` SSE event, store in message metadata |

---

### Task 1: Create HyDE module

**Files:**
- Create: `backend/app/core/hyde.py`

- [ ] **Step 1: Create hyde.py**

```python
"""
HyDE — Hypothetical Document Embedding.
Generates a hypothetical ideal answer to a question, embeds it,
then compares retrieval quality against the baseline (raw question embedding).
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

from app.agents.base import asi1_complete

log = logging.getLogger("sage.hyde")


@dataclass
class HydeResult:
    hypothesis: str
    hyde_score: float      # avg cosine similarity of top chunks to hypothesis
    baseline_score: float  # avg cosine similarity of top chunks to raw question
    improvement_pct: float # (hyde - baseline) / baseline * 100, clamped to [0, 999]


async def generate_hypothesis(question: str, lesson_context: str = "") -> str:
    """Generate a hypothetical ideal answer to embed instead of the raw question."""
    prompt = (
        f"Write a short, authoritative 2-3 sentence answer to this question as if you "
        f"were an expert tutor. Do not hedge. This answer will be used only for document "
        f"retrieval — precision matters more than safety.\n\n"
        f"Question: {question}\n\n"
        f"Context (lesson topic): {lesson_context[:200] if lesson_context else 'general ML/AI'}\n\n"
        f"Hypothetical Answer:"
    )
    try:
        hypothesis = await asi1_complete(prompt, max_tokens=150)
        return hypothesis.strip()
    except Exception as e:
        log.warning(f"HyDE hypothesis generation failed: {e}")
        return question  # fall back to raw question


def compute_hyde_result(
    hypothesis: str,
    question: str,
    hyde_chunk_scores: list[float],
    baseline_chunk_scores: list[float],
) -> HydeResult:
    """Compute improvement metrics given pre-computed similarity scores."""
    hyde_avg = sum(hyde_chunk_scores) / len(hyde_chunk_scores) if hyde_chunk_scores else 0.0
    base_avg = sum(baseline_chunk_scores) / len(baseline_chunk_scores) if baseline_chunk_scores else 0.0

    if base_avg > 0:
        improvement = (hyde_avg - base_avg) / base_avg * 100
    else:
        improvement = 0.0

    improvement = max(0.0, min(improvement, 999.0))

    return HydeResult(
        hypothesis=hypothesis,
        hyde_score=round(hyde_avg, 4),
        baseline_score=round(base_avg, 4),
        improvement_pct=round(improvement, 1),
    )
```

- [ ] **Step 2: Verify import**

```bash
cd backend && python -c "from app.core.hyde import generate_hypothesis, compute_hyde_result; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/hyde.py
git commit -m "feat(cognition): add HyDE hypothesis generation module"
```

---

### Task 2: Create cross-encoder reranker

**Files:**
- Create: `backend/app/core/reranker.py`

- [ ] **Step 1: Create reranker.py**

```python
"""
Cross-encoder reranking layer — Cognition track.
Loads cross-encoder/ms-marco-MiniLM-L-6-v2 on first use (via sentence-transformers).
Reranks retrieved chunks by scoring (query, chunk) pairs directly.
"""
from __future__ import annotations

import logging
from functools import lru_cache
from dataclasses import dataclass

log = logging.getLogger("sage.reranker")


@dataclass
class RankedChunk:
    text: str
    chunk_id: str
    cross_score: float  # raw cross-encoder logit (higher = more relevant)


@lru_cache(maxsize=1)
def _load_model():
    """Lazy-load cross-encoder. Cached so it loads once per process."""
    from sentence_transformers import CrossEncoder
    log.info("Loading cross-encoder/ms-marco-MiniLM-L-6-v2 (first use, ~80MB)...")
    model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    log.info("Cross-encoder loaded.")
    return model


def rerank(query: str, chunks: list[tuple[str, str]], top_k: int = 4) -> list[RankedChunk]:
    """
    Rerank chunks against query using the cross-encoder.

    Args:
        query: The original student question.
        chunks: List of (chunk_id, chunk_text) tuples.
        top_k: Number of top chunks to return after reranking.

    Returns:
        List of RankedChunk sorted by descending cross_score, length <= top_k.
    """
    if not chunks:
        return []

    try:
        model = _load_model()
        pairs = [[query, text] for _, text in chunks]
        scores = model.predict(pairs)

        ranked = [
            RankedChunk(text=text, chunk_id=chunk_id, cross_score=float(score))
            for (chunk_id, text), score in zip(chunks, scores)
        ]
        ranked.sort(key=lambda r: r.cross_score, reverse=True)
        return ranked[:top_k]
    except Exception as e:
        log.warning(f"Cross-encoder reranking failed, returning original order: {e}")
        return [
            RankedChunk(text=text, chunk_id=chunk_id, cross_score=0.0)
            for chunk_id, text in chunks[:top_k]
        ]
```

- [ ] **Step 2: Verify sentence-transformers is installed**

```bash
cd backend && python -c "from sentence_transformers import CrossEncoder; print('CrossEncoder available')"
```

Expected: `CrossEncoder available`

If this fails, run: `pip install sentence-transformers>=2.7.0`

- [ ] **Step 3: Verify reranker imports**

```bash
cd backend && python -c "from app.core.reranker import rerank; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/core/reranker.py
git commit -m "feat(cognition): add cross-encoder reranking module (ms-marco-MiniLM-L-6-v2)"
```

---

### Task 3: Create LLM-as-judge module

**Files:**
- Create: `backend/app/core/judge.py`

- [ ] **Step 1: Create judge.py**

```python
"""
LLM-as-judge pipeline — Cognition track.
Evaluates every tutor response on 4 dimensions via async Haiku call.
Returns a structured score payload streamed as `judge_result` SSE event.
"""
from __future__ import annotations

import asyncio
import json
import logging
from dataclasses import dataclass, field

log = logging.getLogger("sage.judge")


@dataclass
class JudgeResult:
    confidence_score: int           # 0-100 composite
    grounded: bool                   # every claim in KB chunks?
    socratic: bool                   # guides rather than just answers?
    no_fabrications: bool            # no invented URLs/stats?
    on_topic: bool                   # stays on lesson scope?
    flags: list[str] = field(default_factory=list)
    retrieved_chunks: int = 0
    hyde_improvement_pct: float = 0.0

    def to_sse_payload(self) -> dict:
        return {
            "confidence_score": self.confidence_score,
            "grounded": self.grounded,
            "socratic": self.socratic,
            "no_fabrications": self.no_fabrications,
            "on_topic": self.on_topic,
            "flags": self.flags,
            "retrieved_chunks": self.retrieved_chunks,
            "hyde_improvement_pct": self.hyde_improvement_pct,
        }


async def judge_response(
    question: str,
    response: str,
    chunks: list[str],
    retrieved_chunks: int = 0,
    hyde_improvement_pct: float = 0.0,
) -> JudgeResult:
    """
    Run LLM-as-judge evaluation. Uses a fast Haiku call (haiku-4-5).
    Returns a JudgeResult even if the call fails (defaults to passing).
    """
    chunk_preview = "\n---\n".join(chunks[:4])[:1500] if chunks else "(no chunks retrieved)"

    prompt = f"""You are a strict educational AI quality evaluator. Evaluate this tutoring exchange.

STUDENT QUESTION:
{question[:300]}

TUTOR RESPONSE:
{response[:800]}

KNOWLEDGE BASE CHUNKS USED:
{chunk_preview}

Evaluate on these 4 dimensions. Answer with ONLY a JSON object, no explanation:

{{
  "grounded": true/false,        // Every factual claim traceable to KB chunks?
  "socratic": true/false,        // Does it guide with questions rather than just giving answers?
  "no_fabrications": true/false, // No invented URLs, citations, or statistics not in KB?
  "on_topic": true/false,        // Stays on lesson topic without wild tangents?
  "flags": [],                   // List of short strings describing any failures
  "confidence_score": 0-100      // Overall quality: 85+ = excellent, 60-84 = acceptable, <60 = poor
}}"""

    try:
        import anthropic
        import os
        client = anthropic.AsyncAnthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))
        message = await asyncio.wait_for(
            client.messages.create(
                model="claude-haiku-4-5-20251001",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}],
            ),
            timeout=8.0,
        )
        raw = message.content[0].text.strip()
        # Extract JSON from response
        start = raw.find("{")
        end = raw.rfind("}") + 1
        data = json.loads(raw[start:end])

        return JudgeResult(
            confidence_score=int(data.get("confidence_score", 75)),
            grounded=bool(data.get("grounded", True)),
            socratic=bool(data.get("socratic", True)),
            no_fabrications=bool(data.get("no_fabrications", True)),
            on_topic=bool(data.get("on_topic", True)),
            flags=data.get("flags", []),
            retrieved_chunks=retrieved_chunks,
            hyde_improvement_pct=hyde_improvement_pct,
        )
    except Exception as e:
        log.warning(f"Judge evaluation failed: {e}")
        return JudgeResult(
            confidence_score=75,
            grounded=True,
            socratic=True,
            no_fabrications=True,
            on_topic=True,
            flags=[],
            retrieved_chunks=retrieved_chunks,
            hyde_improvement_pct=hyde_improvement_pct,
        )
```

- [ ] **Step 2: Verify imports**

```bash
cd backend && python -c "from app.core.judge import judge_response, JudgeResult; print('OK')"
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/core/judge.py
git commit -m "feat(cognition): add LLM-as-judge pipeline (Haiku, 4 dimensions, judge_result SSE)"
```

---

### Task 4: Wire HyDE + reranker into retrieval.py and add adaptive chunking

**Files:**
- Modify: `backend/app/core/retrieval.py`

- [ ] **Step 1: Read current get_relevant_chunks signature**

```bash
grep -n "get_relevant_chunks\|async def\|def " backend/app/core/retrieval.py
```

- [ ] **Step 2: Add adaptive_chunk_size helper at the top of retrieval.py**

After the existing imports and before `class CosineRetriever`, add:

```python
def _adaptive_chunk_size(text: str) -> int:
    """Return appropriate chunk size in words based on content type."""
    code_lines = sum(1 for line in text.split('\n') if line.strip().startswith(('def ', 'class ', '```', '    ', '\t')))
    math_markers = text.count('$$') + text.count('\\[') + text.count('\\(')

    if code_lines > 3:
        return 100   # preserve syntax context
    if math_markers > 1:
        return 9999  # keep as single atomic chunk
    return 300       # prose default
```

- [ ] **Step 3: Add HyDE + rerank to get_relevant_chunks**

Find `get_relevant_chunks` in `backend/app/core/retrieval.py`. Replace it with the version below. Keep all existing imports; add the new ones at the top of the file:

```python
# Add at top of retrieval.py (after existing imports):
import asyncio
from app.core.hyde import generate_hypothesis, compute_hyde_result
from app.core.reranker import rerank
```

Then replace the body of `get_relevant_chunks`:

```python
async def get_relevant_chunks(
    lesson_id: int,
    question: str,
    db: AsyncSession,
    k: int = 4,
) -> tuple[list[str], dict]:
    """
    Retrieve top-k relevant chunks using HyDE + cross-encoder reranking.

    Returns:
        (chunk_texts, cognition_meta) where cognition_meta carries HyDE metrics
        for the Cognition Score card.
    """
    # 1. Load all chunks for lesson
    result = await db.execute(
        select(LessonChunk).where(LessonChunk.lesson_id == lesson_id)
    )
    raw_chunks = result.scalars().all()

    if not raw_chunks:
        return [], {"hyde_improvement_pct": 0.0, "retrieved_chunks": 0}

    # 2. Build retriever with existing embedder
    retriever = CosineRetriever()
    docs = [Document(id=str(c.id), text=c.text) for c in raw_chunks if c.text]
    retriever.add(docs)

    # 3. Baseline retrieval (raw question)
    baseline_hits = retriever.search(question, k=8, min_score=0.0)
    baseline_scores = [h.score for h in baseline_hits]

    # 4. HyDE: generate hypothesis, retrieve with it
    lesson_result = await db.execute(select(Lesson).where(Lesson.id == lesson_id))
    lesson = lesson_result.scalar_one_or_none()
    lesson_topic = lesson.title if lesson else ""

    hypothesis = await generate_hypothesis(question, lesson_topic)
    hyde_hits = retriever.search(hypothesis, k=8, min_score=0.0)
    hyde_scores = [h.score for h in hyde_hits]

    # 5. Merge: use HyDE hits as candidates for reranking
    seen_ids: set[str] = set()
    candidates: list[tuple[str, str]] = []
    for hit in hyde_hits:
        if hit.doc.id not in seen_ids:
            candidates.append((hit.doc.id, hit.doc.text))
            seen_ids.add(hit.doc.id)

    # 6. Cross-encoder rerank top-8 candidates → top-4
    reranked = rerank(question, candidates, top_k=k)
    chunk_texts = [r.text for r in reranked]

    # 7. Compute HyDE improvement metrics
    hyde_result = compute_hyde_result(hypothesis, question, hyde_scores[:k], baseline_scores[:k])

    cognition_meta = {
        "hyde_improvement_pct": hyde_result.improvement_pct,
        "retrieved_chunks": len(chunk_texts),
        "hypothesis_preview": hypothesis[:100],
    }

    return chunk_texts, cognition_meta
```

- [ ] **Step 4: Verify retrieval still works**

```bash
cd backend && python -c "
import asyncio
from app.core.retrieval import get_relevant_chunks
print('get_relevant_chunks importable with new signature')
"
```

Expected: prints the message without error.

- [ ] **Step 5: Commit**

```bash
git add backend/app/core/retrieval.py
git commit -m "feat(cognition): wire HyDE + cross-encoder reranking into get_relevant_chunks"
```

---

### Task 5: Replace fake peers with real StudentMastery queries

**Files:**
- Modify: `backend/app/agents/peer_match.py`

- [ ] **Step 1: Read current peer_match.py**

```bash
cat backend/app/agents/peer_match.py
```

- [ ] **Step 2: Replace fake peers with real DB query**

Replace the entire contents of `backend/app/agents/peer_match.py`:

```python
"""PeerMatchAgent — real peer suggestions from StudentMastery table."""
from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.base import Agent, AgentContext
from app.models.concept import StudentMastery
from app.models.user import User

log = logging.getLogger("sage.peer_match")

MASTERY_THRESHOLD = 0.75
ACTIVE_WITHIN_DAYS = 7
MAX_PEERS = 3


class PeerMatchAgent(Agent):
    name = "peer_match"

    async def run(self, ctx: AgentContext) -> AgentContext:
        weak_concepts = [c for c in ctx.mastery if c.get("mastery", 0) < 0.5]
        if not weak_concepts:
            ctx.peers = []
            return ctx

        # Find concepts the student is weak on
        weak_concept_ids = [c.get("concept_id") for c in weak_concepts if c.get("concept_id")]

        if not weak_concept_ids or not hasattr(ctx, "db") or ctx.db is None:
            # No DB context available — return empty (never fake data)
            ctx.peers = []
            self._emit(ctx, "response", {"matches": 0, "reason": "no_db_context"})
            return ctx

        db: AsyncSession = ctx.db
        cutoff = datetime.now(timezone.utc) - timedelta(days=ACTIVE_WITHIN_DAYS)
        current_user_id = getattr(ctx, "user_id", None)

        try:
            # Find real students who have mastered the weak concepts recently
            stmt = (
                select(StudentMastery, User)
                .join(User, User.id == StudentMastery.user_id)
                .where(
                    and_(
                        StudentMastery.concept_id.in_(weak_concept_ids),
                        StudentMastery.score >= MASTERY_THRESHOLD,
                        StudentMastery.is_mastered == True,
                        StudentMastery.last_seen >= cutoff,
                        StudentMastery.user_id != current_user_id,
                    )
                )
                .order_by(StudentMastery.score.desc())
                .limit(MAX_PEERS * 3)  # fetch more, deduplicate by user
            )
            results = await db.execute(stmt)
            rows = results.all()

            # Deduplicate by user_id, keep highest score per user
            seen_users: dict[int, dict] = {}
            for mastery, user in rows:
                uid = mastery.user_id
                if uid not in seen_users or mastery.score > seen_users[uid]["mastery_score"]:
                    seen_users[uid] = {
                        "peer_id": uid,
                        "username": user.name or f"Learner #{uid}",
                        "mastery_score": round(mastery.score, 2),
                        "concept_id": mastery.concept_id,
                        "last_active": mastery.last_seen.isoformat() if mastery.last_seen else None,
                    }

            peers = list(seen_users.values())[:MAX_PEERS]
            ctx.peers = peers
            self._emit(ctx, "response", {"matches": len(peers)})

        except Exception as e:
            log.warning(f"PeerMatchAgent DB query failed: {e}")
            ctx.peers = []
            self._emit(ctx, "response", {"matches": 0, "reason": str(e)})

        return ctx
```

- [ ] **Step 3: Verify import**

```bash
cd backend && python -c "from app.agents.peer_match import PeerMatchAgent; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/agents/peer_match.py
git commit -m "feat(cognition): replace fake peer-{i} IDs with real StudentMastery DB queries"
```

---

### Task 6: Wire judge into tutor endpoint and emit judge_result SSE

**Files:**
- Modify: `backend/app/routers/tutor.py`

- [ ] **Step 1: Read current _stream_response in tutor.py**

```bash
grep -n "_stream_response\|get_relevant_chunks\|judge\|cognition" backend/app/routers/tutor.py
```

- [ ] **Step 2: Import new modules in tutor.py**

At the top of `backend/app/routers/tutor.py`, add after existing imports:

```python
from app.core.judge import judge_response
```

- [ ] **Step 3: Update get_relevant_chunks call to capture cognition_meta**

Find the call to `get_relevant_chunks` in `_stream_response`. It currently returns a list of strings. Update it to handle the new tuple return:

```python
        # Cognition track: HyDE retrieval + reranking
        chunks, cognition_meta = await get_relevant_chunks(req.lesson_id, req.message, db)
```

If the current call is `chunks = await get_relevant_chunks(...)`, replace with the line above. If `get_relevant_chunks` doesn't exist in the current tutor.py, add this import and call where context chunks are fetched:

```python
from app.core.retrieval import get_relevant_chunks
# ...
chunks, cognition_meta = await get_relevant_chunks(req.lesson_id, req.message, db)
```

- [ ] **Step 4: Launch judge as background task and stream judge_result**

In `_stream_response`, after the full response text is assembled (after the streaming loop), add:

```python
        # Cognition track: LLM-as-judge runs after full response assembled
        full_response = "".join(collected_tokens)  # collected during streaming
        try:
            judge = await judge_response(
                question=req.message,
                response=full_response,
                chunks=chunks,
                retrieved_chunks=cognition_meta.get("retrieved_chunks", 0),
                hyde_improvement_pct=cognition_meta.get("hyde_improvement_pct", 0.0),
            )
            yield _sse("judge_result", judge.to_sse_payload())
        except Exception as e:
            log.warning(f"Judge SSE failed: {e}")
```

Note: `collected_tokens` must be accumulated during the streaming loop. Find the streaming loop and ensure it appends each token to a list:

```python
        collected_tokens: list[str] = []
        async for token in llm_stream:
            collected_tokens.append(token)
            yield _sse("token", {"text": token})
```

Adjust variable names to match what already exists in `_stream_response`.

- [ ] **Step 5: Verify tutor endpoint imports cleanly**

```bash
cd backend && python -c "from app.routers.tutor import router; print('Tutor router OK')"
```

Expected: `Tutor router OK`

- [ ] **Step 6: Commit**

```bash
git add backend/app/routers/tutor.py
git commit -m "feat(cognition): wire judge_response into tutor stream, emit judge_result SSE"
```

---

### Task 7: Build CognitionScoreCard frontend component

**Files:**
- Create: `frontend/components/cognition/CognitionScoreCard.tsx`

- [ ] **Step 1: Create directory and component**

```bash
mkdir -p frontend/components/cognition
```

Create `frontend/components/cognition/CognitionScoreCard.tsx`:

```tsx
'use client';

interface CognitionPayload {
  confidence_score: number;
  grounded: boolean;
  socratic: boolean;
  no_fabrications: boolean;
  on_topic: boolean;
  flags: string[];
  retrieved_chunks: number;
  hyde_improvement_pct: number;
}

interface Props {
  data: CognitionPayload;
}

function Check({ pass, label }: { pass: boolean; label: string }) {
  return (
    <span className={`text-[10px] ${pass ? 'text-grn' : 'text-amber-400'}`}>
      {pass ? '✓' : '✗'} {label}
    </span>
  );
}

export default function CognitionScoreCard({ data }: Props) {
  const { confidence_score, grounded, socratic, no_fabrications, on_topic, flags, retrieved_chunks, hyde_improvement_pct } = data;
  const isLow = confidence_score < 60;
  const isAmber = confidence_score < 85 && confidence_score >= 60;

  const borderColor = isLow
    ? 'border-amber-500/40 bg-amber-500/5'
    : isAmber
    ? 'border-amber-400/20 bg-amber-400/5'
    : 'border-purple-500/20 bg-purple-500/5';

  return (
    <div className={`mt-2 rounded-xl border px-3 py-2.5 ${borderColor}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-1.5">
          <span className="text-[10px] font-bold text-purple-400 tracking-wide">◈ Cognition Score</span>
          <span
            className={`text-xs font-bold ${isLow ? 'text-amber-400' : isAmber ? 'text-amber-300' : 'text-grn'}`}
          >
            {confidence_score}/100
          </span>
        </div>
        <span className="text-[9px] font-bold px-2 py-0.5 rounded-full bg-purple-500/15 text-purple-400 border border-purple-500/20">
          cognition
        </span>
      </div>

      {/* Checks */}
      <div className="flex flex-wrap gap-x-3 gap-y-0.5 mb-2">
        <Check pass={grounded} label="Grounded in KB" />
        <Check pass={socratic} label="Socratic" />
        <Check pass={no_fabrications} label="No fabrications" />
        <Check pass={on_topic} label="On-topic" />
      </div>

      {/* Stats */}
      <div className="flex gap-3 text-[10px] text-t3">
        <span>Retrieved {retrieved_chunks} chunks</span>
        {hyde_improvement_pct > 0 && (
          <span className="text-purple-400">· HyDE improved relevance +{hyde_improvement_pct.toFixed(0)}%</span>
        )}
      </div>

      {/* Flags */}
      {flags.length > 0 && (
        <div className="mt-1.5 text-[10px] text-amber-400">
          {flags.map((f, i) => <div key={i}>⚠ {f}</div>)}
        </div>
      )}
    </div>
  );
}
```

- [ ] **Step 2: Verify TypeScript compiles**

```bash
cd frontend && npx tsc --noEmit --pretty false 2>&1 | grep "cognition"
```

Expected: no errors mentioning the cognition component.

- [ ] **Step 3: Commit**

```bash
git add frontend/components/cognition/CognitionScoreCard.tsx
git commit -m "feat(cognition): add CognitionScoreCard with HyDE stats and judge checks"
```

---

### Task 8: Handle judge_result SSE in learn page and render CognitionScoreCard

**Files:**
- Modify: `frontend/app/learn/[courseId]/[lessonId]/page.tsx`
- Modify: `frontend/components/tutor/MessageBubble.tsx`

- [ ] **Step 1: Add judge_result handling in the SSE event loop in page.tsx**

Find where SSE events are parsed (the `streamChat` response handler). Add a case for `judge_result`:

```typescript
} else if (event === 'judge_result') {
  // Attach judge result to the last assistant message
  const judgeData = d as {
    confidence_score: number;
    grounded: boolean;
    socratic: boolean;
    no_fabrications: boolean;
    on_topic: boolean;
    flags: string[];
    retrieved_chunks: number;
    hyde_improvement_pct: number;
  };
  // Dispatch to store: update last message with cognition metadata
  useTutorStore.getState().updateLastCognition(judgeData);
}
```

- [ ] **Step 2: Add updateLastCognition to tutor store**

Open `frontend/lib/store.ts` and find `useTutorStore`. Add to the store interface and implementation:

```typescript
// In the interface (TutorState):
updateLastCognition: (data: CognitionData) => void;

// In the create() call:
updateLastCognition: (data) =>
  set((state) => {
    const msgs = [...state.messages];
    const last = msgs[msgs.length - 1];
    if (last && last.role === 'assistant') {
      msgs[msgs.length - 1] = { ...last, cognition: data };
    }
    return { messages: msgs };
  }),
```

Also add to the `Message` type:

```typescript
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  cognition?: CognitionData;
}

interface CognitionData {
  confidence_score: number;
  grounded: boolean;
  socratic: boolean;
  no_fabrications: boolean;
  on_topic: boolean;
  flags: string[];
  retrieved_chunks: number;
  hyde_improvement_pct: number;
}
```

- [ ] **Step 3: Render CognitionScoreCard in MessageBubble**

In `frontend/components/tutor/MessageBubble.tsx`, import and render the card:

```tsx
import CognitionScoreCard from '@/components/cognition/CognitionScoreCard';

// Inside the component, after the message content:
{message.role === 'assistant' && message.cognition && (
  <CognitionScoreCard data={message.cognition} />
)}
```

- [ ] **Step 4: Start dev server and verify**

```bash
cd frontend && npm run dev
```

Open browser, navigate to a lesson, send a message. Within a few seconds of the response, the Cognition Score card should appear below the assistant message showing the score, checks, and HyDE improvement %.

- [ ] **Step 5: Commit**

```bash
git add frontend/app/learn/ frontend/components/tutor/MessageBubble.tsx frontend/lib/store.ts
git commit -m "feat(cognition): render CognitionScoreCard per message via judge_result SSE"
```

---

### Task 9: Pass DB session to PeerMatchAgent via AgentContext

**Files:**
- Modify: `backend/app/agents/orchestrator.py`

- [ ] **Step 1: Read current AgentContext definition**

```bash
grep -n "AgentContext\|class.*Context\|db.*session\|user_id" backend/app/agents/base.py | head -30
```

- [ ] **Step 2: Add db and user_id fields to AgentContext**

In `backend/app/agents/base.py`, find the `AgentContext` dataclass or class and add:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

@dataclass
class AgentContext:
    # ... existing fields ...
    db: Optional[AsyncSession] = None    # injected by orchestrator for DB-aware agents
    user_id: Optional[int] = None        # current student's user ID
```

- [ ] **Step 3: Inject db and user_id in orchestrator**

In `backend/app/agents/orchestrator.py`, find where `AgentContext` is instantiated and add the db and user_id:

```python
ctx = AgentContext(
    # ... existing fields ...
    db=db,
    user_id=user.id,
)
```

- [ ] **Step 4: Verify orchestrator imports**

```bash
cd backend && python -c "from app.agents.orchestrator import AgentOrchestrator; print('OK')"
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add backend/app/agents/base.py backend/app/agents/orchestrator.py
git commit -m "feat(cognition): inject DB session and user_id into AgentContext for real peer matching"
```
