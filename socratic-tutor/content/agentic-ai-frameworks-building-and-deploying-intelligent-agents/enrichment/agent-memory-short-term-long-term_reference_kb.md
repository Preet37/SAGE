## Core Definitions

**Short-term memory (thread-scoped / session-scoped memory).**  
As LangGraph’s memory concepts guide defines it, short-term memory “tracks the ongoing conversation by maintaining message history within a session,” and LangGraph “manages short-term memory as a part of your agent’s state,” persisted via a checkpointer so a conversation thread “can be resumed at any time.” This state can include not only messages but also other session artifacts like “uploaded files, retrieved documents, or generated artifacts.” Source: https://langchain-ai.github.io/langgraph/concepts/memory/

**In-context memory (a.k.a. working memory inside the model’s context window).**  
As Weng explains, short-term memory for LLM agents can be viewed as “all the in-context learning” the model performs from the prompt/context it is given at inference time; it is limited by the model’s context window and disappears when not included in the next call. Source: https://lilianweng.github.io/posts/2023-06-23-agent/

**Conversation history (message list used as context).**  
LangGraph describes conversation history as “the most common form of short-term memory,” typically represented as a growing list of alternating human and model messages. Long histories can exceed context windows (causing errors) and can degrade model performance by distracting it with stale content while increasing latency and cost. Source: https://langchain-ai.github.io/langgraph/concepts/memory/

**Long-term memory (persistent, cross-session memory).**  
LangGraph defines long-term memory as storage that “retains information across different conversations or sessions,” is “shared across conversational threads,” and can be recalled “at any time and in any thread.” It is not limited to a single thread ID; memories are “scoped to any custom namespace.” Source: https://langchain-ai.github.io/langgraph/concepts/memory/

**Persistent storage (external memory substrate).**  
In agent systems, long-term memory is commonly implemented using external stores (e.g., vector stores for semantic retrieval). Weng characterizes long-term memory as enabling retention and recall of “(infinite) information over extended periods,” “often by leveraging an external vector store and fast retrieval.” Source: https://lilianweng.github.io/posts/2023-06-23-agent/

**Memory retrieval (retrieve-on-demand rather than carry everything).**  
In RAG-style systems, retrieval is a separate step that selects a small set of relevant items (e.g., top‑K passages) from a large external corpus/index, which are then provided to the generator. This is the core “retrieve then generate” pattern formalized in RAG. Source: https://arxiv.org/pdf/2005.11401.pdf

**Stateful agents.**  
LangGraph Platform (renamed “LangSmith Deployment” as of Oct 2025) frames “stateful” agents as those that require persistence/checkpointing, can manage complex state beyond message lists (including short/long-term memory), and may need human-in-the-loop pauses and resume (“time travel”). Source: https://blog.langchain.dev/why-langgraph-platform/

---

## Key Formulas & Empirical Results

### Retrieval scoring & objectives (long-term memory as vector search)

**DPR similarity (dot product).**  
From DPR (Karpukhin et al., 2020), question and passage are embedded into the same \(d\)-dimensional space and scored by inner product:  
\[
\mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)
\]  
- \(E_Q(\cdot)\): question encoder; \(E_P(\cdot)\): passage encoder; both output vectors in \(\mathbb{R}^d\).  
Supports: implementing long-term memory retrieval via precomputed passage embeddings + ANN (FAISS).  
Source: https://aclanthology.org/2020.emnlp-main.550.pdf

**DPR training loss (in-batch negatives softmax).**  
\[
\mathcal{L}=-\log \frac{e^{\mathrm{sim}(q_i,p_i^+)}}{e^{\mathrm{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\mathrm{sim}(q_i,p_{i,j}^-)}}
\]  
Supports: why dense retrievers can be trained to make relevant memories retrievable.  
Source: https://aclanthology.org/2020.emnlp-main.550.pdf

**RAG top‑K marginalization (retrieval-augmented “memory”).**  
RAG treats retrieved passage \(z\) as a latent variable and approximates marginalization with top‑K docs:  
- RAG‑Sequence:  
\[
p(y\mid x)\approx \sum_{z\in \text{top-}K} p_\eta(z\mid x)\; p_\theta(y\mid x,z)
\]
- RAG‑Token:  
\[
p(y\mid x)=\prod_{i} \sum_{z\in \text{top-}K} p_\eta(z\mid x)\; p_\theta(y_i\mid x,z,y_{<i})
\]  
Supports: formal view of “retrieve a little, generate with it” rather than stuffing all history into context.  
Defaults reported: retrieve top \(K=5\) during training; \(K=10\) at test.  
Source: https://arxiv.org/pdf/2005.11401.pdf

### Empirical results: long-term conversational memory is hard; retrieval/representation choices matter

**LoCoMo benchmark scale (very long-term conversational memory).**  
LoCoMo: 10 conversations, each ~588 turns and ~16,618 tokens on average, spanning ~27.2 sessions (up to 32) over months; multimodal.  
Supports: why short-term context alone becomes impractical.  
Source: https://aclanthology.org/2024.acl-long.747.pdf

**LoCoMo QA performance (long-context baseline struggles).**  
Best long-context QA reported: “gpt-4-turbo 128K overall 51.6” token-level F1 (single-hop 72.3; multi-hop 51.5; temporal 51.4; adversarial 15.7). Human QA overall F1: 87.9.  
Supports: “just use a huge context window” is not sufficient for robust long-term memory.  
Source: https://aclanthology.org/2024.acl-long.747.pdf

**Procedural memory retrieval generalization cliff; summaries help.**  
Procedural Memory Retrieval Benchmark (ALFWorld): under seen→unseen context shift, “Combined embeddings MAP 0.844→0.592 (−29.9%)” while “Summary embeddings 0.754→0.671 (−11.0%)” and become best on unseen.  
Supports: abstraction (summaries) can improve retrieval robustness vs raw embedding of detailed trajectories.  
Source: https://arxiv.org/pdf/2511.21730.pdf

### Production sizing / operational numbers (state persistence)

**Checkpoint write rate sizing (LangGraph production math).**  
\[
\text{writes/sec} = \text{steps\_per\_request} \times \text{requests/sec}
\]  
Example: 12 steps/request and 2,000 req/s ⇒ 24,000 writes/s.  
Supports: why persistence/checkpointing has real infra implications for stateful agents.  
Source: https://aerospike.com/blog/langgraph-production-latency-replay-scale

### API constraints that force memory management

**Context budgeting constraint (Completions API).**  
OpenAI Completions reference states:  
**tokens(prompt) + max_tokens ≤ model_context_length**  
Supports: why you must trim/summarize/retrieve rather than keep everything in prompt.  
Source: https://platform.openai.com/docs/api-reference/completions/create

**Responses API truncation behavior.**  
`truncation: "auto"` drops earlier conversation items to fit; `"disabled"` fails with 400 if input exceeds context window.  
Supports: concrete behavior when short-term memory grows too large.  
Source: https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl

---

## How It Works

### A. Short-term memory (in-thread coherence) in a stateful agent

1. **Represent short-term memory as agent state.**  
   In LangGraph, short-term memory is part of the graph state (often a `messages` list plus other fields). Source: https://langchain-ai.github.io/langgraph/concepts/memory/

2. **Persist state via checkpoints keyed by thread.**  
   A checkpointer saves a snapshot at each super-step boundary; threads are keyed by `thread_id`. This enables resume, human-in-the-loop, and “time travel” replay. Source: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer

3. **On each invocation/step, read state → run node(s) → write updates.**  
   LangGraph’s tracing/how-to shows the pattern of accumulating messages with `add_messages` so new messages append rather than overwrite. Source: https://docs.langchain.com/oss/python/langgraph/how-tos/trace-langgraph-applications/

4. **If you don’t persist, you don’t actually have short-term memory across runs.**  
   A common failure mode: without a checkpointer, each run restarts and the message list appears to “replace” rather than accumulate across turns. This is explicitly called out in LangGraph issue #1568: “Insert a checkpoint, Otherwise, your graph will restart after each run.” Source: https://github.com/langchain-ai/langgraph/issues/1568

5. **Manage context window pressure.**  
   Long message histories can exceed context windows or degrade performance; LangGraph recommends removing/forgetting stale info and points to “Add and manage memory” techniques. Source: https://langchain-ai.github.io/langgraph/concepts/memory/

### B. Long-term memory (cross-session consistency) with retrieve-on-demand

A practical “store a lot, retrieve a little” loop consistent with the sources:

1. **Write:** store durable items outside the prompt.  
   Examples: user preferences, stable facts, summaries/observations. LangGraph long-term memory is stored in namespaces and can be shared across threads. Source: https://langchain-ai.github.io/langgraph/concepts/memory/

2. **Index:** represent items for retrieval.  
   Commonly via embeddings + ANN index (FAISS/Chroma/Vespa). DPR/RAG describe precomputing passage vectors and building ANN indexes. Sources:  
   - DPR: https://aclanthology.org/2020.emnlp-main.550.pdf  
   - RAG: https://arxiv.org/pdf/2005.11401.pdf  
   - Spotify deployment case (dense retrieval + ANN in Vespa): https://engineering.atspotify.com/2022/03/introducing-natural-language-search-for-podcast-episodes

3. **Retrieve:** at runtime, embed the query and fetch top‑K.  
   DPR: embed question \(v_q\), retrieve top‑k by dot product similarity. Source: https://aclanthology.org/2020.emnlp-main.550.pdf

4. **Inject:** include only retrieved items (plus current turn + minimal recent history) in the model context.  
   RAG implements this by concatenating \(x\) and retrieved \(z\) for generation. Source: https://arxiv.org/pdf/2005.11401.pdf

5. **Govern:** avoid over-retrieval.  
   LoCoMo reports that “too many retrieved items hurts (signal-to-noise).” Source: https://aclanthology.org/2024.acl-long.747.pdf

### C. API-level conversation carryover vs explicit memory

**OpenAI Responses API (built-in multi-turn state):**
- Use `previous_response_id` to continue a conversation state, but note: **instructions are not carried over** when using `previous_response_id` (you can swap system/developer instructions per turn). Source: https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl
- Alternatively use `conversation` objects; items are prepended to new input items and auto-appended after completion. Source: https://platform.openai.com/docs/api-reference/responses/list?lang=python

**Critical constraint:** neither approach automatically performs “good memory management”; you still must manage context length (truncation, trimming, summarization, retrieval). Source: OpenAI Agents SDK cookbook on session memory + trimming/compression: https://cookbook.openai.com/examples/agents_sdk/session_memory

---

## Teaching Approaches

### Intuitive (no math)
- **Two buckets:** “What we can fit in the model’s head right now” (context window) vs “what we keep in a notebook” (database/vector store).  
- Short-term memory = coherence within a thread; long-term memory = preferences/facts that survive new threads.  
Grounding: LangGraph explicitly separates thread-scoped memory (state + checkpoints) from cross-thread memory (namespaces/stores). Source: https://langchain-ai.github.io/langgraph/concepts/memory/

### Technical (with math)
- Treat long-term memory as a retrieval model: embed query and memory items; score by dot product (DPR) and retrieve top‑K; then generate conditioned on retrieved items (RAG marginalization).  
- Use RAG equations to explain why you don’t need to include the whole corpus/history in context—only top‑K approximates the marginal. Sources:  
  - DPR: https://aclanthology.org/2020.emnlp-main.550.pdf  
  - RAG: https://arxiv.org/pdf/2005.11401.pdf

### Analogy-based
- **RAM vs disk:** short-term memory is RAM (fast, limited, cleared when power off unless checkpointed); long-term memory is disk (persistent, searchable).  
- LangGraph’s persistence/checkpointer model makes the “RAM snapshot” idea literal: checkpoints at super-step boundaries enable resume/time travel. Source: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer

---

## Common Misconceptions

1. **“If I annotate `messages` with `add_messages`, the agent will remember across turns automatically.”**  
   - Why wrong: without a checkpointer, the graph restarts each run; state isn’t persisted across turns.  
   - Correct model: `add_messages` controls how state updates *within a run/thread*, but persistence across turns requires checkpointing + consistent `thread_id`.  
   - Source: LangGraph issue #1568 (fix: compile with a checkpointer and pass `thread_id`): https://github.com/langchain-ai/langgraph/issues/1568

2. **“Long-term memory means the model weights changed / the model learned permanently.”**  
   - Why wrong: sources describe long-term memory as external storage (often vector store) retrieved at runtime; it’s not weight updates.  
   - Correct model: long-term memory is a separate substrate (store/index) + retrieval step; generation is conditioned on retrieved items (RAG).  
   - Sources: Weng on external vector store retrieval: https://lilianweng.github.io/posts/2023-06-23-agent/ ; RAG formalization: https://arxiv.org/pdf/2005.11401.pdf

3. **“If the model has a 128K+ context window, I can just dump the entire conversation history and be done.”**  
   - Why wrong: LangGraph notes long contexts can still perform poorly (“distracted” by stale content) and cost/latency rise; LoCoMo shows long-context QA F1 remains far below human and is vulnerable on adversarial/unanswerable questions.  
   - Correct model: context windows reduce hard failures but don’t solve relevance, distraction, or hallucination; retrieval + curated summaries/observations can outperform raw long context.  
   - Sources: LangGraph memory guide: https://langchain-ai.github.io/langgraph/concepts/memory/ ; LoCoMo results: https://aclanthology.org/2024.acl-long.747.pdf

4. **“Retrieving more memories is always better.”**  
   - Why wrong: LoCoMo reports “too many retrieved items hurts (signal-to-noise).”  
   - Correct model: retrieval is a precision/recall trade; top‑K should be tuned and memory representations should be curated (e.g., observations/summaries).  
   - Source: https://aclanthology.org/2024.acl-long.747.pdf

5. **“Memory is just storing raw chat logs.”**  
   - Why wrong: benchmarks show representation matters; procedural benchmark finds LLM procedural summaries embedded are more robust under vocabulary shift than raw/action-only embeddings.  
   - Correct model: long-term memory often stores *processed* artifacts (summaries, observations, structured facts) optimized for retrieval and robustness.  
   - Source: https://arxiv.org/pdf/2511.21730.pdf

---

## Worked Examples

### 1) LangGraph short-term memory across turns (why checkpointing matters)

**Goal:** demonstrate that message accumulation across user turns requires a checkpointer + `thread_id`.

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver  # per issue #1568

# State schema: messages append rather than overwrite
class State(TypedDict):
    messages: Annotated[list, add_messages]

def mock_llm(state: State):
    # In real use, call an LLM with state["messages"]
    last_user = state["messages"][-1]
    return {"messages": [{"role": "ai", "content": f"Echo: {last_user.content if hasattr(last_user,'content') else last_user}"}]}

builder = StateGraph(State)
builder.add_node("chatbot", mock_llm)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

graph = builder.compile(checkpointer=MemorySaver())

thread_config = {"configurable": {"thread_id": "user-123"}}

# Turn 1
for event in graph.stream({"messages": ("user", "Hi")}, thread_config):
    pass

# Turn 2 (same thread_id => prior messages are present)
for event in graph.stream({"messages": ("user", "What did I just say?")}, thread_config):
    pass
```

**Tutor notes (what to point out mid-conversation):**
- Without `checkpointer=MemorySaver()` and a stable `thread_id`, the second call won’t see the first turn (graph restarts).  
- This exact confusion is documented in issue #1568; the suggested fix is adding a checkpointer and passing `thread_id`. Source: https://github.com/langchain-ai/langgraph/issues/1568  
- Conceptual backing: checkpointers save state snapshots per super-step and organize them into threads. Source: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer

### 2) Minimal long-term memory retrieval loop (DPR-style)

**Goal:** show the mechanical steps: embed → ANN search → inject top‑K.

Pseudo-steps aligned to DPR/RAG:

1. Offline: embed each memory item \(p\) with \(E_P(p)\) and build ANN index (FAISS).  
2. Online: embed query \(q\) with \(E_Q(q)\).  
3. Score by dot product \(E_Q(q)^\top E_P(p)\) and retrieve top‑K.  
4. Provide retrieved items to generator (concatenate \(x\) and \(z\) as in RAG).  

Sources: DPR retrieval pipeline + dot product scoring: https://aclanthology.org/2020.emnlp-main.550.pdf ; RAG conditioning on retrieved docs: https://arxiv.org/pdf/2005.11401.pdf

---

## Comparisons & Trade-offs

| Choice | What it is | Strengths | Weaknesses / failure modes | When to choose | Sources |
|---|---|---|---|---|---|
| **Long context only** | Put lots of history directly in prompt | Simple; no retrieval infra | Can exceed context; can distract model; adversarial/unanswerable vulnerability; cost/latency | Small/short threads; prototyping | LangGraph memory guide; LoCoMo results |
| **Short-term state + checkpointing** | Persist thread state via checkpointer | Resume, HITL, time travel; coherent within thread | Still grows; needs trimming/summarization | Any stateful agent; long-running workflows | LangGraph memory + checkpointer refs |
| **Long-term memory via vector retrieval (RAG/DPR)** | Store many items externally; retrieve top‑K | Keeps prompts small; update knowledge by swapping index; inspect evidence | Retrieval errors; over-retrieval noise; distribution shift | Cross-session prefs/knowledge; large corpora | DPR; RAG; LoCoMo “too many hurts” |
| **Summary/observation-based memory** | Store abstractions (summaries, assertions) | More robust retrieval; less noise | Summarization drift; may omit details | When raw logs are too noisy; cross-context generalization | LoCoMo observations; procedural benchmark summaries |

Key supporting notes:
- LoCoMo: storing history as “observations (assertions)” improves QA vs raw dialog; too many retrieved items hurts. Source: https://aclanthology.org/2024.acl-long.747.pdf  
- Procedural benchmark: summary embeddings generalize better under vocabulary shift (smaller generalization gap). Source: https://arxiv.org/pdf/2511.21730.pdf  
- RAG rationale: retrieval reduces hallucinations and allows knowledge updates by swapping the index. Source: https://arxiv.org/pdf/2005.11401.pdf

---

## Prerequisite Connections

- **LLM context window & token budgeting.** Needed to understand why short-term memory can’t grow unbounded (e.g., tokens(prompt)+max_tokens ≤ context length). Source: https://platform.openai.com/docs/api-reference/completions/create  
- **Embeddings + nearest-neighbor search.** Needed to understand long-term memory retrieval (DPR dot product; ANN/FAISS). Source: https://aclanthology.org/2020.emnlp-main.550.pdf  
- **RAG pipeline concept.** Needed to connect retrieval outputs to generation (top‑K marginalization). Source: https://arxiv.org/pdf/2005.11401.pdf  
- **Persistence/checkpointing concept.** Needed to understand stateful agents and resume/time travel. Source: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer

---

## Socratic Question Bank

1. **If you remove the checkpointer from a LangGraph app, what exactly changes about “memory” across user turns?**  
   *Good answer:* state won’t persist across runs; each invocation restarts unless checkpoints keyed by `thread_id` exist.

2. **What information belongs in short-term state vs long-term memory for a customer support agent? Why?**  
   *Good answer:* short-term: current ticket context, recent tool outputs; long-term: user preferences, prior tickets summary.

3. **Why might retrieving 50 memories make answers worse than retrieving 5?**  
   *Good answer:* signal-to-noise; LoCoMo notes too many retrieved items hurts.

4. **In DPR, why is dot product similarity operationally convenient?**  
   *Good answer:* decomposable; passage embeddings can be precomputed; ANN search over vectors.

5. **What does RAG’s top‑K marginalization say about how many documents you need in context?**  
   *Good answer:* approximate marginal over latent docs using only top‑K; you don’t include everything.

6. **If a model has a huge context window, what problems remain unsolved for long-term memory?**  
   *Good answer:* distraction, cost/latency, hallucination on adversarial/unanswerable; LoCoMo shows performance still limited.

7. **What’s the difference between “conversation state” in an API (previous_response_id/conversation) and “long-term memory”?**  
   *Good answer:* conversation state is chained context items; long-term memory is separate persistent store retrieved selectively.

8. **How would you detect that your memory system is causing “context poisoning”? What would you change?**  
   *Good answer:* stale/wrong facts repeated; reduce carried context, use summaries/clean-room compression (Agents SDK cookbook framing).

---

## Likely Student Questions

**Q: Why doesn’t my LangGraph bot remember the previous user message even though I used `add_messages`?**  
→ **A:** Without a checkpointer, the graph restarts each run; you need to compile with a checkpointer (e.g., `MemorySaver()`) and pass a stable `thread_id` so state is persisted and reloaded. Source: https://github.com/langchain-ai/langgraph/issues/1568 and checkpointer concept: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer

**Q: What’s the exact difference between short-term and long-term memory in LangGraph?**  
→ **A:** Short-term memory is thread-scoped state (often message history) persisted via thread checkpoints; long-term memory is cross-thread storage in namespaces that can be recalled in any thread. Source: https://langchain-ai.github.io/langgraph/concepts/memory/

**Q: How do I implement long-term memory retrieval mathematically?**  
→ **A:** A standard approach is DPR: embed query and memory items into \(\mathbb{R}^d\) and score with dot product \(\mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)\), retrieving top‑K via ANN (FAISS). Source: https://aclanthology.org/2020.emnlp-main.550.pdf

**Q: What is RAG actually computing with top‑K documents?**  
→ **A:** RAG approximates \(p(y\mid x)\) by marginalizing over retrieved docs \(z\) truncated to top‑K: \(p(y\mid x)\approx \sum_{z\in topK} p_\eta(z\mid x)p_\theta(y\mid x,z)\) (sequence form). Source: https://arxiv.org/pdf/2005.11401.pdf

**Q: Is “just use a 128K context window” competitive with memory retrieval?**  
→ **A:** LoCoMo reports best long-context QA (gpt-4-turbo 128K) overall F1 51.6 vs human 87.9, and adversarial/unanswerable is especially low (15.7), indicating long context alone is not sufficient. Source: https://aclanthology.org/2024.acl-long.747.pdf

**Q: How does the OpenAI Responses API handle too-long conversations?**  
→ **A:** With `truncation="auto"`, it drops earlier conversation items to fit; with `truncation="disabled"` (default), the request fails with 400 if it would exceed the context window. Source: https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl

**Q: What’s a concrete production sizing rule for checkpoint storage?**  
→ **A:** LangGraph production guidance gives: writes/sec = steps_per_request × requests/sec; example 12 steps/request and 2,000 req/s ⇒ 24,000 writes/s. Source: https://aerospike.com/blog/langgraph-production-latency-replay-scale

**Q: Why do summary-based memories sometimes retrieve better than raw logs?**  
→ **A:** In the procedural retrieval benchmark, summary embeddings had a much smaller seen→unseen MAP drop (0.754→0.671, −11.0%) than combined/raw embedding variants (e.g., 0.844→0.592, −29.9%), suggesting abstraction reduces vocabulary-specific noise. Source: https://arxiv.org/pdf/2511.21730.pdf

---

## Available Resources

### Videos
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: the student asks how “stateful agents” are orchestrated in practice (threads, state, tool loops), or how memory fits into multi-agent workflows.
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: the student is missing fundamentals about what an LLM is (weights + runtime) before discussing context windows and memory limits.
- [Let's build the GPT Tokenizer](https://youtube.com/watch?v=zduSFxRajkE) — Surface when: the student’s confusion is really about tokens/context length budgeting rather than memory architecture.

### Articles & Tutorials
- [Memory in LangGraph](https://langchain-ai.github.io/langgraph/concepts/memory/) — Surface when: the student asks for precise definitions of thread-scoped vs cross-thread memory, or how LangGraph implements memory.
- [LLM Powered Autonomous Agents (Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: the student wants a conceptual architecture view (planning/memory/tools) and the short-term vs long-term framing.
- [RAG paper (Lewis et al., 2020)](https://arxiv.org/pdf/2005.11401.pdf) — Surface when: the student asks for the formal probabilistic view of retrieval-augmented “memory.”
- [OpenAI Agents SDK: session memory + trimming/compression](https://cookbook.openai.com/examples/agents_sdk/session_memory) — Surface when: the student asks “how do I manage context in practice?” (trimming vs compression; session object).
- [mem0 repository](https://github.com/mem0ai/mem0) — Surface when: the student asks for a concrete library pattern for “retrieve memories → inject into system prompt → add new memories.”

---

## Visual Aids

![Human memory taxonomy mapped to LLM agent memory components. (Weng, 2023)](/api/wiki-images/agent-memory/images/lilianweng-posts-2023-06-23-agent_008.png)  
**Show when:** the student is mixing up “context window” vs “short-term state” vs “long-term memory,” and you want a taxonomy anchor before implementation details.

![Generative agent architecture: memory stream, reflection, and planning enable human-like behavior. (Park et al. 2023)](/api/wiki-images/agent-memory/images/lilianweng-posts-2023-06-23-agent_012.png)  
**Show when:** the student asks how memory interacts with planning/reflection loops (why memory isn’t just storage, but part of an agent architecture).

![LLM-powered autonomous agent system overview. (Weng, 2023)](/api/wiki-images/agent-memory/images/lilianweng-posts-2023-06-23-agent_001.png)  
**Show when:** the student needs the “big picture” of agent components (planning, memory, tools) before drilling into short-term vs long-term memory.

---

## Key Sources

- [Memory in LangGraph](https://langchain-ai.github.io/langgraph/concepts/memory/) — Most direct, implementation-grounded definitions of short-term (thread) vs long-term (namespace) memory and why context management is necessary.
- [LLM Powered Autonomous Agents (Weng, 2023)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Clear conceptual framing: in-context learning as short-term memory; external vector store retrieval as long-term memory.
- [Retrieval-Augmented Generation (RAG) (Lewis et al., 2020)](https://arxiv.org/pdf/2005.11401.pdf) — Formalizes retrieval + generation with top‑K marginalization; key for “retrieve a little” mental model.
- [DPR (Karpukhin et al., 2020)](https://aclanthology.org/2020.emnlp-main.550.pdf) — Concrete retrieval mechanics (dot product scoring, in-batch negatives, ANN/FAISS pipeline) for implementing long-term memory retrieval.
- [LoCoMo benchmark (2024)](https://aclanthology.org/2024.acl-long.747.pdf) — Empirical evidence that long-context alone underperforms and that retrieval representation/quantity affects outcomes (signal-to-noise).