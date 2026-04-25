## Core Definitions

**Context window** — The model’s finite token budget for *all* text it can attend to in a single forward pass: system/developer instructions, conversation history, tool outputs, and the current user input. When inputs exceed this limit, the application must either trim/compress history or the request fails, depending on API settings. In the OpenAI Responses API, `truncation: "auto"` will “drop items from the beginning of the conversation to fit,” while `truncation: "disabled"` causes a **400 error** if the input would exceed the context window. (OpenAI Responses API streaming/truncation reference)

**Conversation history** — The accumulated sequence of prior user/assistant/tool messages that an application may prepend to the current turn to preserve continuity. In the Responses API, a `conversation` can be used so that items are prepended to `input_items`, and after completion “input and output items are automatically added to the conversation.” (OpenAI Responses API list + streaming references)

**Summarization (as dialogue memory / context compression)** — A lossy compression strategy that replaces long dialogue history with a shorter representation intended to preserve salient facts/preferences/goals. LLM-Rsum formalizes this as producing a memory \(M\) from history \(H\), then generating the next response conditioned on \(M\) and current context \(x\). Summarization can suffer from “recursive information decay” and drift when repeatedly re-summarized. (LLM-Rsum; CogCanvas)

**Sliding window** — A context management strategy that keeps only the most recent \(N\) turns (or a token budget’s worth) of conversation in the prompt, dropping older turns. The memory taxonomy paper lists sliding window as a form of “context compression,” and the OpenAI Responses API’s `truncation: "auto"` implements a specific sliding-window-like behavior by dropping earliest conversation items first. (Agent Memory Taxonomy; OpenAI Responses API streaming/truncation reference)

**Message trimming** — Any policy that removes parts of the conversation history to fit within the context window (e.g., drop oldest turns, drop low-priority tool logs, keep pinned instructions). In the Responses API, trimming can be automatic (`truncation: "auto"`) or enforced by the developer by constructing shorter `input_items` / conversation state. (OpenAI Responses API streaming/truncation reference)

**System prompt / system instructions** — High-priority instructions inserted into the model’s context that steer behavior. In the Responses API, `instructions: string` is “a system (or developer) message inserted into the model’s context,” and developer/system instructions take precedence over user instructions. A key operational detail: when using `previous_response_id`, “instructions from the previous response are not carried over” to the next response. (OpenAI Responses API list + streaming references)

---

## Key Formulas & Empirical Results

### LLM-Rsum: factorization + memory update equations (dialogue summarization as memory)
**Factorization (Eq. 1):**
\[
p(y \mid H, x) = p(M \mid H)\; p(y \mid M, x)
\]
- \(H\): past sessions (multi-session dialogue history)  
- \(x\): current session context at step \(t\)  
- \(M\): available memory after a session  
- \(y\): response  
**Claim supported:** treat “memory creation” and “response generation” as two stages; memory \(M\) is the compressed substitute for long history \(H\). (LLM-Rsum)

**Memory iteration (Eq. 2):**
\[
M_s = \text{LLM}(P_m;\; M_{s-1}, S_s)
\]
- \(S_s\): full dialogue of session \(s\)  
- \(P_m\): memory-iteration prompt  
- \(M_{s-1}\): prior memory (initially `"none"`)  
**Claim supported:** recursive summarization across sessions. (LLM-Rsum)

**Response generation (Eq. 3):**
\[
y = \text{LLM}(P_g;\; M, x)
\]
- \(P_g\): generation prompt  
**Claim supported:** generate using memory \(M\) as primary reference. (LLM-Rsum)

**Implementation defaults reported:** temperature **0**; retriever top‑k **3 or 5**; datasets input lengths ≤ **4k** tokens. (LLM-Rsum)

### Empirical results: summarization vs retrieval vs long-context baselines
**LLM-Rsum (ChatGPT backbone):**
- MSC: ChatGPT‑Rsum F1 **20.48** vs ChatGPT **19.41**; human Consistency **1.45** vs **1.32**.  
- Carecall: ChatGPT‑Rsum F1 **14.02** vs ChatGPT **13.69**; Consistency **1.70** vs **1.43**.  
- Retrieval can hurt (Carecall): BM25(k=3) F1 **12.64**, DPR(k=3) F1 **12.21** (both below vanilla ChatGPT).  
**Claim supported:** recursive summarization can improve long-term consistency; naive retrieval is not guaranteed to help. (LLM-Rsum)

**CogCanvas (verbatim-grounded artifacts) controlled benchmark:**
- Exact match: **Summarization 19.0%** vs verbatim-grounded retrieval **93.0%** (example: “use type hints everywhere” decays to “prefers type hints”).  
- Controlled Table 2: CogCanvas Recall **97.5%**, Exact **93.0%**; Summarization Recall **19.0%**, Exact **14.0%**.  
**Claim supported:** iterative summarization can drift/lose constraints; verbatim grounding preserves fidelity. (CogCanvas)

**CogCanvas multi-hop benchmark (Table 3):**
- CogCanvas Pass **81.0%** vs RAG Pass **55.5%** vs GraphRAG **40.0%** vs Summarization **0.0%**.  
**Claim supported:** summarization can fail badly on multi-hop/temporal reasoning; structured retrieval helps. (CogCanvas)

**Agent Memory Taxonomy: “long context isn’t enough”**
- MemoryArena: long-context-only baseline completion drops from **>80% to ~45%** vs active memory agent.  
**Claim supported:** simply increasing context length doesn’t guarantee effective recall/use. (Agent Memory Taxonomy)

### OpenAI Responses API: operational parameters that affect context/memory
- `truncation: "auto"` drops items from the **beginning** to fit context; `truncation: "disabled"` fails with **400** if too long. (Responses streaming/truncation reference)
- `max_output_tokens` bounds generated tokens “including visible output + reasoning tokens.” (Responses streaming/truncation reference)
- `instructions` are **not carried over** when using `previous_response_id`. (Responses streaming/truncation reference)

---

## How It Works

### A. Sliding window / trimming (pure in-context short-term memory)
1. **Maintain a running conversation list** of message “items” (user/assistant/tool).
2. **Before each model call**, compute (or estimate) token usage for:
   - system/developer instructions
   - selected conversation items
   - current user input
   - expected output budget (`max_output_tokens`)
3. **If over budget**, apply a trimming policy:
   - simplest: drop oldest turns first (sliding window)
   - better: drop low-value items first (e.g., verbose tool logs), keep pinned constraints
4. **Send the remaining items** to the model.
5. **Risk profile:** older constraints/preferences may disappear; model may contradict earlier decisions because they are no longer in-context. (Agent Memory Taxonomy; OpenAI truncation behavior)

**API hook (Responses API):** set `truncation: "auto"` to have the platform drop earliest conversation items automatically; set `"disabled"` to force explicit app-side management (400 on overflow). (Responses streaming/truncation reference)

### B. Recursive summarization (LLM-Rsum style)
Per session \(s\):
1. **Collect full session transcript** \(S_s\).
2. **Update memory** using the LLM with a memory prompt \(P_m\):  
   \(M_s = \text{LLM}(P_m; M_{s-1}, S_s)\). (LLM-Rsum)
3. **At inference time for a new turn**, generate response using memory \(M\) and current context \(x\):  
   \(y = \text{LLM}(P_g; M, x)\). (LLM-Rsum)
4. **Risk profile:** memory is lossy; repeated summarization can cause drift (“recursive information decay”). (CogCanvas)

### C. Verbatim-grounded artifact memory (CogCanvas pattern)
Per turn \(t\):
1. **Extract “CanvasObjects”** from the new turn (and optionally prior objects to dedupe):  
   `CanvasObject = (type, content, grounding_quote, source, embedding, turn_index, confidence)`  
   where `type ∈ {Decision, Todo, KeyFact, Reminder, Insight}` and `grounding_quote` is verbatim. (CogCanvas)
2. **Two-pass gleaning:** second pass targets pronouns/implicit causality/temporal expressions; merge + dedupe. (CogCanvas)
3. **Build a temporal-aware graph**:
   - embed objects
   - connect edges using cosine similarity + keyword overlap + temporal heuristics (including causal edges with constraints). (CogCanvas)
4. **Retrieve for the current query**:
   - hybrid semantic + lexical scoring
   - adaptive top‑k by query complexity
   - rerank (BGE reranker in the paper)
   - greedy pack into a token budget (e.g., max 2000 tokens reported). (CogCanvas)
5. **Inject retrieved objects** into the model context for response generation.
6. **Risk profile:** more engineering complexity; but higher faithfulness due to grounding quotes. (CogCanvas)

### D. “Memory loop” framing (Agent Memory Taxonomy)
At step \(t\):
1. agent receives input \(x_t\)
2. consults memory \(M_t\) to choose action \(a_t\)
3. updates memory via **write–manage–read** operations (summarize, dedup, score priority, resolve contradictions, delete).  
**Key idea:** memory behaves like a belief state in a POMDP; storing everything increases utility but harms efficiency/governance. (Agent Memory Taxonomy)

---

## Teaching Approaches

### Intuitive (no math)
- **You have a backpack with limited space (context window).** Every turn you decide what to keep: the last few messages (sliding window), a “trip journal” summary (summarization), or a set of labeled sticky notes with exact quotes (verbatim artifacts). If you keep only recent stuff, you forget old constraints; if you summarize too aggressively, you may rewrite history incorrectly.

### Technical (with math)
- Use LLM-Rsum’s decomposition: generate a compact memory \(M\) from history \(H\), then generate response \(y\) from \(M\) and current context \(x\):  
  \(p(y|H,x)=p(M|H)p(y|M,x)\).  
- Then contrast with CogCanvas: instead of compressing into \(M\), store *verbatim-grounded objects* and retrieve/inject them, reducing summarization drift (controlled exact match 93% vs summarization 19%). (LLM-Rsum; CogCanvas)

### Analogy-based
- **RAM vs disk vs notes:** the context window is RAM (fast, limited). Summaries are like compressing files (smaller but lossy). CogCanvas-style artifacts are like a notebook of signed quotes you can cite later (slower to search, but reliable). The agent memory taxonomy explicitly discusses multi-tier memory (e.g., MemGPT “virtual context” RAM/disk/cold storage) as a design pattern. (Agent Memory Taxonomy)

---

## Common Misconceptions

1. **“If I use `previous_response_id`, the model will remember my system prompt automatically.”**  
   - **Why wrong:** The Responses API states that when using `previous_response_id`, “instructions from the previous response are not carried over.”  
   - **Correct model:** You must resend/replace `instructions` each turn if you rely on them; conversation state can persist, but system instructions do not automatically persist under `previous_response_id`. (Responses streaming/truncation reference)

2. **“Setting `truncation: "auto"` is the same as summarization.”**  
   - **Why wrong:** `truncation: "auto"` drops items from the beginning to fit—this is trimming/sliding window, not compression.  
   - **Correct model:** Truncation removes content; summarization transforms content into a shorter representation (lossy but potentially keeps older facts). (Responses streaming/truncation reference; Agent Memory Taxonomy)

3. **“Bigger context windows solve memory; you don’t need memory mechanisms.”**  
   - **Why wrong:** The memory taxonomy paper reports MemoryArena where a long-context-only baseline drops completion from **>80% to ~45%** compared to an active memory agent. Also, LLM-Rsum notes “lost in the middle” where models fail to use distant context effectively.  
   - **Correct model:** Long context increases capacity but doesn’t guarantee *effective retrieval/use*; you still need prioritization, retrieval, or structured memory. (Agent Memory Taxonomy; LLM-Rsum)

4. **“Summaries are always safer than retrieval because they’re shorter.”**  
   - **Why wrong:** CogCanvas shows summarization can catastrophically lose exact constraints (controlled exact 14% for summarization vs 93% for verbatim-grounded retrieval). LLM-Rsum also shows retrieval can hurt in some settings (Carecall BM25/DPR below vanilla), so neither is universally safe.  
   - **Correct model:** Choose based on *faithfulness needs* and query type; for exact constraints, prefer verbatim grounding; for broad persona/preferences, summaries may work. (CogCanvas; LLM-Rsum)

5. **“If the model contradicts earlier info, it must be ‘hallucinating’—not a memory issue.”**  
   - **Why wrong:** If earlier constraints were trimmed or drifted in summaries, the model may be consistent with what it currently sees. The taxonomy emphasizes faithfulness/staleness/contradiction as memory quality metrics; stale or incorrect recall can be worse than none.  
   - **Correct model:** Diagnose whether the relevant info is still in-context, summarized accurately, or retrievable; contradictions can be a *memory pipeline* failure, not just generation. (Agent Memory Taxonomy)

---

## Worked Examples

### Example 1 — Responses API: automatic trimming vs hard failure
**Goal:** demonstrate how `truncation` changes behavior when conversation grows.

```python
from openai import OpenAI
client = OpenAI()

# (A) Hard fail if too long
resp = client.responses.create(
    model="gpt-4.1-mini",
    instructions="You are a tutor. Always ask one Socratic question.",
    input="Continue the conversation...",
    truncation="disabled",          # if context too long -> 400
    max_output_tokens=200
)

# (B) Auto-drop oldest conversation items to fit
resp2 = client.responses.create(
    model="gpt-4.1-mini",
    instructions="You are a tutor. Always ask one Socratic question.",
    conversation="conv_123",        # server-managed conversation state
    input="Continue the conversation...",
    truncation="auto",              # drops earliest items first
    max_output_tokens=200
)
```

**Tutor notes (what to emphasize mid-conversation):**
- `truncation="auto"` implements “drop from the beginning” behavior (sliding-window-like).  
- `truncation="disabled"` is useful in debugging to force you to notice overflow rather than silently forgetting. (Responses streaming/truncation reference)

### Example 2 — LLM-Rsum style: recursive session memory update (conceptual skeleton)
**Goal:** show the two-stage pattern: update memory \(M\), then answer using \(M\).

Pseudo-steps aligned to equations:
1. Start with `M = "none"`.
2. After session `S_s` ends, call the model with a memory prompt `P_m`:
   - input: `M_{s-1}` and `S_s`
   - output: `M_s`
3. For the next session/turn, call the model with generation prompt `P_g`:
   - input: `M` and current context `x`
   - output: response `y`

**Tutor notes:**
- Cite the factorization \(p(y|H,x)=p(M|H)p(y|M,x)\) when a student asks “why separate memory from response?” (LLM-Rsum)

### Example 3 — CogCanvas object: what “verbatim-grounded” means in practice
Given a user says: “In this codebase, use type hints everywhere—no exceptions.”

A stored object would include:
- `type`: Decision (or KeyFact depending on schema)
- `content`: “Use type hints everywhere in the codebase.”
- `grounding_quote`: exact quote: “use type hints everywhere—no exceptions”
- `turn_index`: where it occurred

**Tutor notes:**
- This is designed to prevent the drift example CogCanvas highlights (“use type hints everywhere” → “prefers type hints”). (CogCanvas)

---

## Comparisons & Trade-offs

| Strategy | What you keep in-context | Strengths | Failure modes | When to choose (per sources) |
|---|---|---|---|---|
| Sliding window / trimming | Recent turns only; older dropped | Simple; efficient | Forgets older constraints; “lost” preferences | When recency dominates and you can tolerate forgetting; aligns with `truncation:"auto"` dropping earliest items (OpenAI API) |
| Recursive summarization (LLM-Rsum) | A compact memory \(M\) + current context | Improves consistency vs no memory in reported datasets (small gains) | Summarization drift/decay; lossy | When you need lightweight long-term continuity and can accept lossy compression (LLM-Rsum) |
| Retrieval of stored items (RAG-like) | Retrieved snippets injected per query | Can outperform naive long-context; but not guaranteed | Bad retrieval hurts (Carecall BM25/DPR < vanilla) | When you can build reliable retrieval and evaluation; beware retrieval quality (LLM-Rsum) |
| Verbatim-grounded artifacts + graph (CogCanvas) | Retrieved objects with grounding quotes | High fidelity; strong exact match vs summarization | More system complexity; needs extraction + rerank | When exact constraints/temporal multi-hop matter; summarization shown to fail badly (CogCanvas) |

**Selection heuristic grounded in sources:**  
- If you need **faithfulness to exact constraints**, CogCanvas reports large gains over summarization (Exact 93% vs 14%).  
- If you need **simple continuity** and can accept lossy memory, LLM-Rsum shows modest improvements over vanilla.  
- If you rely on **automatic trimming**, understand it is deletion, not compression (`truncation:"auto"` drops earliest items). (CogCanvas; LLM-Rsum; OpenAI Responses API)

---

## Prerequisite Connections

- **Tokenization & token budgets** — Context windows are measured in tokens; trimming/summarization decisions are token-budget decisions. (Implied by OpenAI truncation + max token budgeting fields)
- **Role hierarchy in chat inputs** — Developer/system instructions take precedence over user instructions; crucial for understanding system prompts. (Responses API list reference)
- **Information retrieval basics (top‑k, reranking)** — CogCanvas’s gains depend heavily on reranking (ablation shows large drop without it). (CogCanvas)
- **Evaluation thinking (precision/recall, contradiction/staleness)** — Memory taxonomy frames memory quality beyond task success. (Agent Memory Taxonomy)

---

## Socratic Question Bank

1. **If your conversation exceeds the context window, what are two fundamentally different things you can do besides “buy a bigger model”?**  
   *Good answer:* trimming/sliding window vs compression (summarization) vs external memory/retrieval.

2. **What’s the difference between “the model forgot” and “the app didn’t send it”? How would you test which happened?**  
   *Good answer:* inspect prompt construction / truncation settings; use `truncation:"disabled"` to force overflow errors.

3. **Why might retrieval make performance worse than doing nothing (as in Carecall BM25/DPR)?**  
   *Good answer:* irrelevant/incorrect retrieved items distract; retrieval quality matters.

4. **In LLM-Rsum’s factorization, what does \(M\) represent, and what trade-off does it introduce?**  
   *Good answer:* compressed memory; improves capacity but is lossy and can drift.

5. **Why does CogCanvas store a `grounding_quote` instead of only a paraphrase?**  
   *Good answer:* to prevent summarization drift and enable traceability/faithfulness.

6. **If you use `previous_response_id`, what must you remember about `instructions`?**  
   *Good answer:* they are not carried over; must resend if needed.

7. **When would you prefer `truncation:"disabled"` in development?**  
   *Good answer:* to catch overflow early rather than silently dropping history.

8. **What metrics beyond “task success” would you track for memory quality?**  
   *Good answer:* precision/recall of recalled facts, contradiction rate, staleness, coverage; plus efficiency/governance (taxonomy).

---

## Likely Student Questions

**Q: What exactly happens when I set `truncation: "auto"` in the Responses API?**  
→ **A:** If the input exceeds the model’s context window, the API “drops items from the beginning of the conversation to fit.” It’s deletion of earliest conversation items, not summarization. (https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl)

**Q: If I use `previous_response_id`, do my system instructions persist?**  
→ **A:** No. The Responses API states: when using `previous_response_id`, “instructions from the previous response are not carried over to the next response.” (https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl)

**Q: What’s the formal model behind “summarize then answer”?**  
→ **A:** LLM-Rsum factorizes response generation as \(p(y|H,x)=p(M|H)p(y|M,x)\), where \(M\) is the memory produced from history \(H\), and the response \(y\) is generated from \(M\) and current context \(x\). (https://arxiv.org/html/2308.15022v3)

**Q: Does summarization actually help, empirically?**  
→ **A:** In LLM-Rsum’s reported results (ChatGPT backbone), MSC F1 improves from **19.41** to **20.48** and human consistency from **1.32** to **1.45**; Carecall consistency improves **1.43 → 1.70**. (https://arxiv.org/html/2308.15022v3)

**Q: Can retrieval be worse than not using memory at all?**  
→ **A:** Yes. LLM-Rsum reports on Carecall that ChatGPT‑BM25(k=3) F1 **12.64** and ChatGPT‑DPR(k=3) F1 **12.21**, both below vanilla ChatGPT F1 **13.69**. (https://arxiv.org/html/2308.15022v3)

**Q: Why do people say summarization “drifts”? Is there evidence?**  
→ **A:** CogCanvas argues summarization is lossy and causes “recursive information decay,” giving an example where “use type hints everywhere” becomes “prefers type hints.” In a controlled benchmark, summarization exact match is **14.0%** vs CogCanvas **93.0%**. (https://www.arxiv.org/pdf/2601.00821.pdf)

**Q: Isn’t a long context window enough for agent tasks?**  
→ **A:** The Agent Memory Taxonomy paper reports MemoryArena where a long-context-only baseline completion drops from **>80% to ~45%** compared to an active memory agent, highlighting a recall→utility gap. (https://arxiv.org/html/2603.07670v1)

**Q: What memory metrics should I track besides “did it answer correctly”?**  
→ **A:** The taxonomy proposes a stack: (1) task effectiveness; (2) memory quality (precision/recall, contradiction rate, staleness, coverage); (3) efficiency (latency, prompt tokens, retrieval calls, storage growth); (4) governance (privacy leakage, deletion compliance, access violations). (https://arxiv.org/html/2603.07670v1)

---

## Available Resources

### Videos
- [Let’s build the GPT Tokenizer (Andrej Karpathy)](https://youtube.com/watch?v=zduSFxRajkE) — **Surface when:** a student is stuck on what “tokens” are and why context windows are measured in tokens (prerequisite for trimming/summarization decisions).

### Articles & Tutorials
- [Prompt Engineering (Lilian Weng)](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — **Surface when:** a student asks how role-based prompts (system/developer/user) affect behavior and why prompt design is empirical.
- [Building LLM applications for production (Chip Huyen)](https://huyenchip.com/2023/04/11/llm-engineering.html) — **Surface when:** a student asks for production strategies around context management, reliability, and engineering trade-offs.
- [How to format inputs to ChatGPT models (OpenAI Cookbook)](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb) — **Surface when:** a student needs concrete message formatting patterns (roles/content) and API call structure.

---

## Visual Aids

![Same prompt, different outputs: LLMs produce inconsistent results by default. (Chip Huyen)](/api/wiki-images/system-prompts/images/huyenchip-2023-04-11-llm-engineering-html_001.png)  
**Show when:** the student assumes “the model will behave consistently” and you need to motivate deterministic settings and careful context construction (before discussing memory/trimming).

![Temperature=0 enforces consistency but doesn't guarantee trustworthy LLM outputs. (Chip Huyen)](/api/wiki-images/system-prompts/images/huyenchip-2023-04-11-llm-engineering-html_002.png)  
**Show when:** the student proposes “just set temperature=0” as a complete reliability/memory solution; use to separate determinism from faithfulness/recall.

---

## Key Sources

- [Responses API — streaming + system instructions + truncation](https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl) — authoritative for how `instructions`, `previous_response_id`, and `truncation` actually behave in production.
- [Recursive Summarization for Long-Term Dialogue Memory (LLM-Rsum)](https://arxiv.org/html/2308.15022v3) — provides the core memory-via-summarization equations and empirical comparisons (including cases where retrieval hurts).
- [CogCanvas (verbatim-grounded artifacts for long conversations)](https://www.arxiv.org/pdf/2601.00821.pdf) — concrete deployable pattern to reduce summarization drift; strong benchmark evidence and ablations (reranking impact).
- [Agent Memory Taxonomy + Benchmarks + Metrics](https://arxiv.org/html/2603.07670v1) — structured taxonomy, design objectives (utility/efficiency/faithfulness/governance), and benchmark/metric framing for evaluating memory systems.