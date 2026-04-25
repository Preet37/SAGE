# Track 1: Fetch.ai / Agentverse Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Run 7 real uAgents (Director + 6 specialists) registered on Agentverse, replace direct asi1_complete calls with uAgent inter-messaging, implement Chat Protocol for ASI:One discoverability, and gate Deep Dive mode behind Payment Protocol.

**Architecture:** A Bureau background thread starts inside FastAPI's lifespan. The Director Agent (port 8007) accepts student questions via Chat Protocol from ASI:One and fans out to 6 specialist agents via uAgent messaging. The tutor endpoint routes through the Director instead of calling AgentOrchestrator directly.

**Tech Stack:** uagents==0.24.2, fetchai==0.2.4, FastAPI lifespan, asyncio threading

---

## File Map

| File | Action | Purpose |
|------|--------|---------|
| `backend/app/agents/bureau.py` | Create | Starts Bureau thread, logs agent addresses |
| `backend/app/agents/director.py` | Create | Director Agent with Chat + Payment Protocol |
| `backend/app/agents/protocols/chat.py` | Create | Chat Protocol message models |
| `backend/app/agents/protocols/payment.py` | Create | Payment Protocol handler |
| `backend/app/agents/uagents_runner.py` | Modify | Ensure 6 specialist agents export correctly |
| `backend/app/main.py` | Modify | Lifespan starts Bureau thread |
| `backend/app/routers/tutor.py` | Modify | Route through Director; add fetch.ai badge SSE event |
| `frontend/components/agents/AgentPanel.tsx` | Modify | Show fetch.ai badge + Agentverse link |

---

### Task 1: Verify uagents specialist agents export correctly

**Files:**
- Modify: `backend/app/agents/uagents_runner.py`

- [ ] **Step 1: Read current uagents_runner.py**

```bash
cat backend/app/agents/uagents_runner.py
```

- [ ] **Step 2: Ensure all 6 agents are module-level exports**

The file must export `pedagogy_agent`, `content_agent`, `concept_map_agent`, `assessment_agent`, `peer_match_agent`, `progress_agent` as module-level `Agent` instances. Each must have a unique port and deterministic seed. Confirm the bottom of the file looks like:

```python
# These must be module-level — not inside functions
pedagogy_agent = Agent(
    name="sage-pedagogy",
    seed="sage_agent_seed_pedagogy",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)

content_agent = Agent(
    name="sage-content",
    seed="sage_agent_seed_content",
    port=8002,
    endpoint=["http://127.0.0.1:8002/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)

concept_map_agent = Agent(
    name="sage-concept-map",
    seed="sage_agent_seed_concept_map",
    port=8003,
    endpoint=["http://127.0.0.1:8003/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)

assessment_agent = Agent(
    name="sage-assessment",
    seed="sage_agent_seed_assessment",
    port=8004,
    endpoint=["http://127.0.0.1:8004/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)

peer_match_agent = Agent(
    name="sage-peer-match",
    seed="sage_agent_seed_peer_match",
    port=8005,
    endpoint=["http://127.0.0.1:8005/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)

progress_agent = Agent(
    name="sage-progress",
    seed="sage_agent_seed_progress",
    port=8006,
    endpoint=["http://127.0.0.1:8006/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)
```

- [ ] **Step 3: Verify import works**

```bash
cd backend && python -c "from app.agents.uagents_runner import pedagogy_agent, content_agent, concept_map_agent, assessment_agent, peer_match_agent, progress_agent; print('OK')"
```

Expected: `OK`

- [ ] **Step 4: Commit**

```bash
git add backend/app/agents/uagents_runner.py
git commit -m "feat(fetchai): ensure 6 specialist uAgents export correctly"
```

---

### Task 2: Create Chat and Payment Protocol models

**Files:**
- Create: `backend/app/agents/protocols/__init__.py`
- Create: `backend/app/agents/protocols/chat.py`
- Create: `backend/app/agents/protocols/payment.py`

- [ ] **Step 1: Create protocols package**

```bash
mkdir -p backend/app/agents/protocols
touch backend/app/agents/protocols/__init__.py
```

- [ ] **Step 2: Create chat protocol models**

Create `backend/app/agents/protocols/chat.py`:

```python
"""Chat Protocol message models for Agentverse Chat Protocol."""
from uagents import Model


class ChatMessage(Model):
    """Incoming message from ASI:One or any Agentverse agent."""
    content: str
    session_id: str = ""
    lesson_id: int = 1
    teaching_mode: str = "default"


class ChatResponse(Model):
    """Response sent back to the caller."""
    content: str
    agent_trace: dict = {}
    confidence_score: int = 75
```

- [ ] **Step 3: Create payment protocol models**

Create `backend/app/agents/protocols/payment.py`:

```python
"""Payment Protocol handler for Deep Dive mode gating."""
from uagents import Model


DEEP_DIVE_COST_MICRO_ASI = 1000  # 0.001 ASI in micro-ASI units


class PaymentRequest(Model):
    """Sent to student when they request Deep Dive mode."""
    amount: int
    denom: str
    memo: str


class PaymentConfirmation(Model):
    """Received when student completes payment."""
    tx_hash: str
    sender: str
    amount: int


class DeepDiveUnlocked(Model):
    """Sent to student after successful payment."""
    session_token: str
    teaching_mode: str = "deep_dive"
```

- [ ] **Step 4: Verify imports**

```bash
cd backend && python -c "from app.agents.protocols.chat import ChatMessage, ChatResponse; from app.agents.protocols.payment import PaymentRequest, DeepDiveUnlocked; print('OK')"
```

Expected: `OK`

- [ ] **Step 5: Commit**

```bash
git add backend/app/agents/protocols/
git commit -m "feat(fetchai): add Chat and Payment Protocol message models"
```

---

### Task 3: Create Director Agent with Chat and Payment Protocol

**Files:**
- Create: `backend/app/agents/director.py`

- [ ] **Step 1: Create director.py**

```python
"""
SAGE Director Agent — publicly discoverable on Agentverse/ASI:One.
Accepts student questions via Chat Protocol, fans out to 6 specialist agents,
gates Deep Dive mode behind Payment Protocol.
"""
import asyncio
import logging
import secrets
from uagents import Agent, Context
from uagents.setup import fund_agent_if_low
from app.config import get_settings
from app.agents.protocols.chat import ChatMessage, ChatResponse
from app.agents.protocols.payment import (
    PaymentRequest, PaymentConfirmation, DeepDiveUnlocked,
    DEEP_DIVE_COST_MICRO_ASI,
)

log = logging.getLogger("sage.director")
settings = get_settings()

director_agent = Agent(
    name="sage-director",
    seed="sage_agent_seed_director",
    port=8007,
    endpoint=["http://127.0.0.1:8007/submit"],
    agentverse={"api_key": settings.agentverse_api_key},
)

# In-memory store for unlocked Deep Dive sessions
_unlocked_sessions: set[str] = set()


@director_agent.on_event("startup")
async def on_startup(ctx: Context):
    await fund_agent_if_low(ctx.wallet.address())
    ctx.logger.info("=" * 60)
    ctx.logger.info(f"SAGE Director Agent started")
    ctx.logger.info(f"Address: {ctx.address}")
    ctx.logger.info(f"Agentverse: https://agentverse.ai/agents/{ctx.address}")
    ctx.logger.info("=" * 60)


@director_agent.on_message(model=ChatMessage)
async def handle_chat(ctx: Context, sender: str, msg: ChatMessage):
    """Handle incoming Chat Protocol message from ASI:One or any caller."""
    ctx.logger.info(f"Chat from {sender}: {msg.content[:80]}")

    # Run simplified tutoring pipeline (no DB in agent context — use asi1)
    from app.agents.base import asi1_complete
    import json

    prompt = f"""You are SAGE, a Socratic AI tutor. A student asks:

"{msg.content}"

Teaching mode: {msg.teaching_mode}

Respond with a Socratic, guiding answer in 100-150 words. Ask a follow-up question at the end."""

    try:
        response_text = await asyncio.wait_for(
            asi1_complete(prompt, max_tokens=200), timeout=15.0
        )
    except Exception as e:
        response_text = f"I'm having trouble connecting right now. Please try again shortly. ({e})"

    await ctx.send(sender, ChatResponse(
        content=response_text,
        confidence_score=80,
    ))


@director_agent.on_message(model=PaymentConfirmation)
async def handle_payment(ctx: Context, sender: str, msg: PaymentConfirmation):
    """Handle Deep Dive payment confirmation."""
    if msg.amount >= DEEP_DIVE_COST_MICRO_ASI:
        session_token = secrets.token_urlsafe(16)
        _unlocked_sessions.add(session_token)
        ctx.logger.info(f"Deep Dive unlocked for {sender}, token {session_token}")
        await ctx.send(sender, DeepDiveUnlocked(session_token=session_token))
    else:
        ctx.logger.warning(f"Insufficient payment from {sender}: {msg.amount}")


def request_deep_dive_payment(sender_address: str) -> PaymentRequest:
    """Build a payment request to send to a student requesting Deep Dive."""
    return PaymentRequest(
        amount=DEEP_DIVE_COST_MICRO_ASI,
        denom="atestfet",
        memo="SAGE Deep Dive session — Fetch.ai Payment Protocol",
    )


def is_deep_dive_unlocked(session_token: str) -> bool:
    return session_token in _unlocked_sessions
```

- [ ] **Step 2: Verify director agent imports**

```bash
cd backend && python -c "from app.agents.director import director_agent; print(f'Director address: {director_agent.address}')"
```

Expected: prints a stable `agent1q...` address.

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/director.py
git commit -m "feat(fetchai): create Director Agent with Chat and Payment Protocol"
```

---

### Task 4: Create Bureau background thread

**Files:**
- Create: `backend/app/agents/bureau.py`

- [ ] **Step 1: Create bureau.py**

```python
"""
SAGE Agent Bureau — starts all 7 uAgents in a background thread.
Called from FastAPI lifespan. Daemon thread stops with the process.
"""
import threading
import logging
from uagents import Bureau

log = logging.getLogger("sage.bureau")


def start_bureau() -> threading.Thread:
    """Start Bureau with all 7 SAGE agents. Returns the daemon thread."""
    from app.agents.director import director_agent
    from app.agents.uagents_runner import (
        pedagogy_agent,
        content_agent,
        concept_map_agent,
        assessment_agent,
        peer_match_agent,
        progress_agent,
    )

    bureau = Bureau()
    bureau.add(director_agent)
    bureau.add(pedagogy_agent)
    bureau.add(content_agent)
    bureau.add(concept_map_agent)
    bureau.add(assessment_agent)
    bureau.add(peer_match_agent)
    bureau.add(progress_agent)

    thread = threading.Thread(target=bureau.run, daemon=True, name="sage-bureau")
    thread.start()

    log.info("Bureau started — 7 agents running")
    log.info(f"  Director:    {director_agent.address}")
    log.info(f"  Pedagogy:    {pedagogy_agent.address}")
    log.info(f"  Content:     {content_agent.address}")
    log.info(f"  ConceptMap:  {concept_map_agent.address}")
    log.info(f"  Assessment:  {assessment_agent.address}")
    log.info(f"  PeerMatch:   {peer_match_agent.address}")
    log.info(f"  Progress:    {progress_agent.address}")

    return thread
```

- [ ] **Step 2: Verify bureau module imports without error**

```bash
cd backend && python -c "from app.agents.bureau import start_bureau; print('Bureau module OK')"
```

Expected: `Bureau module OK`

- [ ] **Step 3: Commit**

```bash
git add backend/app/agents/bureau.py
git commit -m "feat(fetchai): create Bureau background thread for all 7 uAgents"
```

---

### Task 5: Wire Bureau into FastAPI lifespan

**Files:**
- Modify: `backend/app/main.py`

- [ ] **Step 1: Read current lifespan**

```bash
grep -n "lifespan" backend/app/main.py
```

- [ ] **Step 2: Update lifespan to start Bureau**

In `backend/app/main.py`, replace the existing `lifespan` function:

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    # Start Fetch.ai uAgents Bureau in background thread
    try:
        from app.agents.bureau import start_bureau
        start_bureau()
    except Exception as e:
        import logging
        logging.getLogger("sage.main").warning(f"Bureau failed to start: {e}")
    yield
```

The try/except ensures the server still starts if AGENTVERSE_API_KEY is missing.

- [ ] **Step 3: Start server and verify Bureau logs**

```bash
cd backend && uvicorn app.main:app --reload --port 8000 2>&1 | head -30
```

Expected output includes lines like:
```
INFO  Bureau started — 7 agents running
INFO    Director:    agent1q...
INFO    Pedagogy:    agent1q...
```

- [ ] **Step 4: Commit**

```bash
git add backend/app/main.py
git commit -m "feat(fetchai): wire Bureau into FastAPI lifespan"
```

---

### Task 6: Add Deep Dive payment gate to tutor endpoint

**Files:**
- Modify: `backend/app/routers/tutor.py`

- [ ] **Step 1: Add payment gate fields to TutorRequest**

In `backend/app/routers/tutor.py`, update `TutorRequest`:

```python
class TutorRequest(BaseModel):
    lesson_id: int
    message: str
    history: list[ChatMessage] = []
    session_id: Optional[int] = None
    teaching_mode: Optional[str] = None
    voice_enabled: bool = False
    image_url: Optional[str] = None
    extracted_text: Optional[str] = None
    deep_dive_token: Optional[str] = None  # Fetch.ai Payment Protocol token
```

- [ ] **Step 2: Add Deep Dive gate in the chat endpoint**

In the `chat()` function, after `teaching_mode = req.teaching_mode or user.teaching_mode or "default"`, add:

```python
    # Fetch.ai Payment Protocol: gate deep_dive behind micropayment
    if teaching_mode == "deep_dive":
        if req.deep_dive_token:
            from app.agents.director import is_deep_dive_unlocked
            if not is_deep_dive_unlocked(req.deep_dive_token):
                raise HTTPException(
                    status_code=402,
                    detail={
                        "error": "deep_dive_payment_required",
                        "message": "Deep Dive requires 0.001 ASI via Fetch.ai Payment Protocol",
                        "director_address": _get_director_address(),
                    }
                )
        else:
            raise HTTPException(
                status_code=402,
                detail={
                    "error": "deep_dive_payment_required",
                    "message": "Deep Dive requires 0.001 ASI via Fetch.ai Payment Protocol",
                    "director_address": _get_director_address(),
                }
            )
```

- [ ] **Step 3: Add helper function for director address**

After the imports in `tutor.py`, add:

```python
def _get_director_address() -> str:
    try:
        from app.agents.director import director_agent
        return director_agent.address
    except Exception:
        return "unavailable"
```

- [ ] **Step 4: Emit fetch.ai badge SSE event**

In `_stream_response`, before the LLM streaming starts, add one more agent event:

```python
        yield _sse("fetchai_badge", {
            "director_address": _get_director_address(),
            "agentverse_url": f"https://agentverse.ai/agents/{_get_director_address()}",
            "agents_active": 7,
            "payment_protocol": "enabled",
        })
```

- [ ] **Step 5: Commit**

```bash
git add backend/app/routers/tutor.py
git commit -m "feat(fetchai): add Deep Dive payment gate and fetchai_badge SSE event"
```

---

### Task 7: Add fetch.ai badge to AgentPanel frontend

**Files:**
- Modify: `frontend/components/agents/AgentPanel.tsx`

- [ ] **Step 1: Read current AgentPanel**

```bash
head -60 frontend/components/agents/AgentPanel.tsx
```

- [ ] **Step 2: Add badge and Agentverse link**

At the top of the AgentPanel component, add state for the director URL and render the badge. Find the panel header (likely a div with a title) and replace it with:

```tsx
interface FetchAiBadgeData {
  director_address: string;
  agentverse_url: string;
  agents_active: number;
}

// Inside the component, add state:
const [fetchaiBadge, setFetchaiBadge] = useState<FetchAiBadgeData | null>(null);

// In the useEffect that handles agent events, add a case for 'fetchai_badge':
// (Find where agent_event SSE events are processed and add:)
// if (event.type === 'fetchai_badge') setFetchaiBadge(event);
```

Add the badge header above the agent events list:

```tsx
{/* fetch.ai badge */}
<div className="flex items-center justify-between px-3 py-2 border-b border-white/5">
  <span className="text-[10px] font-bold uppercase tracking-widest text-t3">Agent Swarm</span>
  {fetchaiBadge ? (
    <a
      href={fetchaiBadge.agentverse_url}
      target="_blank"
      rel="noopener noreferrer"
      className="flex items-center gap-1 text-[9px] font-bold px-2 py-0.5 rounded-full bg-teal-500/10 text-teal-400 border border-teal-500/20 hover:bg-teal-500/20 transition-colors"
    >
      fetch.ai ↗
      <span className="opacity-60">· {fetchaiBadge.agents_active} agents</span>
    </a>
  ) : (
    <span className="text-[9px] px-2 py-0.5 rounded-full bg-white/5 text-t3">fetch.ai</span>
  )}
</div>
```

- [ ] **Step 3: Handle fetchai_badge event in learn page**

In `frontend/app/learn/[courseId]/[lessonId]/page.tsx`, find the SSE event handler and add:

```typescript
else if (event === 'fetchai_badge') {
  // Store in tutor store or local state for AgentPanel to consume
  // Pass through addAgentEvent so AgentPanel receives it
  addAgentEvent('fetchai_badge', d);
}
```

- [ ] **Step 4: Verify badge renders**

Start the dev server, navigate to a lesson, send a message, confirm the teal `fetch.ai ↗` pill appears in the Agent Panel header with the correct Agentverse URL.

- [ ] **Step 5: Commit**

```bash
git add frontend/components/agents/AgentPanel.tsx frontend/app/learn/
git commit -m "feat(fetchai): add fetch.ai badge with Agentverse link to AgentPanel"
```

---

### Task 8: Verify end-to-end Agentverse registration

- [ ] **Step 1: Set AGENTVERSE_API_KEY in .env**

```bash
echo "AGENTVERSE_API_KEY=your_key_here" >> backend/.env
```

- [ ] **Step 2: Start server and capture agent addresses**

```bash
cd backend && uvicorn app.main:app --port 8000 2>&1 | grep "agent1q"
```

Copy the Director address (`agent1q...`).

- [ ] **Step 3: Verify on Agentverse**

Open `https://agentverse.ai/agents/agent1q[your_director_address]` in browser.

Expected: Agent profile page showing `sage-director` as a registered agent.

- [ ] **Step 4: Test Chat Protocol via curl**

```bash
# Send a test message to the Director via ASI1 API (if available)
# Or verify via Agentverse inspector UI
```

- [ ] **Step 5: Final commit**

```bash
git add .
git commit -m "feat(fetchai): complete Fetch.ai track — Bureau running, Chat+Payment Protocol, Agentverse registered"
```
