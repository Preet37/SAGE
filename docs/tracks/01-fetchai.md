# Track 1 — Fetch.ai (Agentverse + ASI:One)

> **Challenge:** Build on Agentverse, discoverable via ASI:One. Develop a single
> or multi-agent orchestration that demonstrates reasoning, tool execution,
> and solves a real-world problem. Use any agentic framework.
> Register your agents with Agentverse and implement the **Chat Protocol
> (mandatory)** & **Payment Protocol (optional)** to support direct ASI:One
> interactions and built-in monetization.

## What we built

SAGE's full Socratic tutor is now exposed as **two cooperating uAgents** on
the Fetch.ai network. Any ASI:One user can discover and chat with our
tutor agent, ask any technical question on our 74-lesson curriculum, and
receive a grounded, verified answer streamed back through the Chat
Protocol. When the user asks for a quiz, the tutor agent **delegates** to
a sibling quiz agent (multi-agent orchestration) which runs the same loop
in `quiz` mode and routes the formatted quiz back through the chat
session.

A Payment Protocol handler is wired in as a stub so the agent can accept
FET payments for premium content (e.g. annotated lesson videos), with a
clean extension point for the production escrow contract.

### Real-world problem solved

Online learners hop between tools — ChatGPT for explanations, Khan
Academy/YouTube for fundamentals, Quizlet for self-test, papers for
depth. SAGE on Agentverse collapses that to a single conversational
endpoint discoverable via ASI:One: ask a question, get a grounded
answer, ask for a quiz, get one. The agent reasons across an indexed
74-lesson curriculum, executes tools (KB lookup, transcript fetch, web
search), and verifies its own outputs before responding.

## Where it lives

```
backend/app/agents/
├── __init__.py
├── sage_uagent.py    ← Tutor uAgent: Chat Protocol + Payment + delegation
└── quiz_uagent.py    ← Quiz uAgent: multi-agent target

backend/app/routers/
└── fetchai_bridge.py ← /fetchai/info + /fetchai/chat (web demo path)

backend/scripts/
└── register_uagents.py ← Agentverse registration helper

backend/settings.yaml ← features.fetchai_agent flag, agent name/seed
```

### Key code paths

| Concern | File / function |
|---|---|
| uAgent instantiation | `sage_uagent.py:19` (port 8101) |
| **Chat Protocol** handler (mandatory) | `sage_uagent.py:107` `chat_proto.on_message(ChatMessage)` |
| Acknowledgement of every inbound message | `sage_uagent.py:113-116` |
| Routing inbound text → tutor agent loop | `sage_uagent.py:151-158` (uses real `TutorContext`) |
| Verification surfacing in chat | `sage_uagent.py:96-103` (low-confidence claims annotated in the reply) |
| **Payment Protocol** | `sage_uagent.py:48-77` `payment_proto.on_message(PaymentRequest)` |
| **Multi-agent orchestration** — quiz delegation | `sage_uagent.py:128-136` → sends typed `QuizRequest` |
| Quiz agent receiving delegations | `quiz_uagent.py:88-129` |
| Quiz reply relayed back via Chat Protocol | `sage_uagent.py:174-184` |
| Address persistence file | `sage_uagent.py:194-198` (`/tmp/sage_uagent_address`) |
| Web bridge proxy for demo | `routers/fetchai_bridge.py` |

## Why this is 10/10

### ✅ "Discoverable via ASI:One"
- Agent registers on Agentverse with full metadata (`scripts/register_uagents.py`).
- `chat_protocol_spec.version = 0.3.0` published as part of the manifest, which is exactly what ASI:One needs to surface us in agent search.

### ✅ "Single or multi-agent orchestration"
We did **multi-agent**. The tutor doesn't just have a "quiz tool" — it
has a **typed conversation** with another autonomous uAgent:

```
ASI:One user → SAGE Tutor uAgent → typed QuizRequest → Quiz uAgent
                  ← QuizResponse ←
SAGE Tutor → ChatMessage(quiz text) → user
```

Each agent has its own address, its own keypair, its own port, and its
own protocol manifest. The tutor agent only knows the quiz agent's
*address* (`SAGE_QUIZ_AGENT_ADDRESS` env var) — they're independently
deployable processes. That's real orchestration, not a single agent
calling sub-functions.

### ✅ "Demonstrates reasoning, tool execution, real-world problem"
The tutor uAgent doesn't reimplement reasoning — it routes to SAGE's
existing **ReAct-style agent loop** (`backend/app/agent/agent_loop.py`)
which already has 7 tools (`search_web`, `get_lesson_context`,
`get_lesson_transcript`, `get_lesson_reference_kb`,
`get_curated_resources`, `get_relevant_images`, `get_user_progress`),
plus our Cognition-track verifier and semantic memory. So an Agentverse
user gets:

- Multi-step reasoning (max 5 ReAct steps)
- Tool execution against the lesson KB
- Cross-session memory (TF-IDF recall — see Track 2)
- Self-verification before reply

### ✅ "Chat Protocol (MANDATORY)"
Implemented to spec using `uagents_core.contrib.protocols.chat`:
- Receives `ChatMessage`, sends `ChatAcknowledgement` immediately (`sage_uagent.py:113`)
- Replies with `ChatMessage(content=[TextContent(...)])` (`sage_uagent.py:172`)
- Cleanly closes the session with `EndSessionContent` (`sage_uagent.py:175`)
- Logs every inbound and ack for observability (`sage_uagent.py:111`, `:188`)

### ✅ "Payment Protocol (OPTIONAL)"
We did the optional one. `PaymentRequest{sku, amount, currency}` →
`PaymentReceipt{paid, tx_hash, note}` (`sage_uagent.py:33-46`). The web
bridge surfaces concrete SKUs for the demo:

```json
[
  {"sku": "premium_course:lora-deep-dive", "price": 1.0, "currency": "FET"},
  {"sku": "annotated_video:attention",     "price": 0.5, "currency": "FET"}
]
```

The handler is intentionally a stub (`sage_uagent.py:67-77`) with a
`# Wire to Fetch.ai escrow for production billing` note pointing exactly
where to add on-chain verification. That's the right level for a hackathon —
real protocol shape, demo-fast handler.

### ✅ "Use any agentic framework"
We use **uagents** (Fetch.ai's own framework) directly — not LangGraph,
not CrewAI, not OpenAI Agents. The tutor's reasoning runs on Groq's
Llama 3.3 70B for cost/speed. So the agent stack is:

- **uagents 0.24.2** — agent runtime, Chat Protocol
- **agentverse-client 0.1.14** — registration helper
- **Groq llama-3.3-70b-versatile** — reasoning
- **fastapi** — bridge for the demo path

### Beyond the spec

These weren't required, but make this submission stand out:

1. **The agent reuses production infrastructure.** The Chat Protocol
   handler doesn't simulate a tutor — it instantiates the same
   `TutorContext` and runs the same agent loop that powers
   `/tutor/chat`. Whatever judges see in the web app, ASI:One users get
   too.

2. **Verification surfaces in chat.** When the tutor's response scores
   "unverified" (Track 2's groundedness judge), the uAgent annotates the
   reply with a `_(verification: 42%; treat with care)_` footer
   (`sage_uagent.py:96-103`). ASI:One users get the same trust signals
   as web users.

3. **Address persistence.** The tutor writes its address to
   `/tmp/sage_uagent_address` on startup, so the web bridge and the
   registration script can both read it without a hardcoded value
   (`sage_uagent.py:194-198`).

4. **Web bridge for judges.** `/fetchai/info` returns the live agent
   address + Agentverse register link. `/fetchai/chat` proxies a Chat
   Protocol message to the local agent so judges can see the round-trip
   without installing Agentverse Studio (`routers/fetchai_bridge.py`).

## Demo flow

```bash
# 1. Set a stable seed so the agent's address persists across restarts.
export FETCHAI_AGENT_SEED="$(python -c 'import secrets; print(secrets.token_urlsafe(48))')"

# 2. Boot both agents (separate terminals).
cd backend
python -m app.agents.sage_uagent
# ... INFO sage.uagent SAGE Tutor uAgent ready — address: agent1q0mrcaf...

python -m app.agents.quiz_uagent
# ... INFO sage.quiz_uagent SAGE Quiz uAgent ready — address: agent1q0qwcjs...

# 3. Hand the quiz address to the tutor for delegation.
export SAGE_QUIZ_AGENT_ADDRESS=agent1q0qwcjst...

# 4. Register on Agentverse.
export AGENTVERSE_API_KEY=<your key>
python scripts/register_uagents.py

# 5. (Optional) talk to the agent through the web bridge.
curl -s -X POST http://localhost:8000/fetchai/chat \
  -H "Authorization: Bearer $JWT" \
  -d '{"message": "Quiz me on LoRA"}'
# → text round-trip, target_address, elapsed_ms
```

For ASI:One users, after registration:
- Search "SAGE" in ASI:One → "sage-tutor" appears
- Chat: "explain LoRA" → grounded reply with verification footer
- Chat: "now quiz me on attention mechanisms" → tutor delegates to quiz
  agent → user receives a 3-question Socratic quiz
