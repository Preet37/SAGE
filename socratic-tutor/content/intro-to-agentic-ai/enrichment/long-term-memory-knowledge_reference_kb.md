## Core Definitions

**Long-term memory (for LLM agents).** As Weng explains in the context of LLM-powered agents, *long-term memory* is an external mechanism that gives an agent the capability to “retain and recall (infinite) information over extended periods,” often implemented with an external vector store and retrieval, because the model’s in-context “short-term memory” is limited by the context window and degrades over long inputs (Weng, 2023: https://lilianweng.github.io/posts/2023-06-23-agent/). LangGraph similarly defines long-term memory as storing user-specific or application-level data *across sessions* and *across conversational threads*, recallable at any time (LangGraph Memory Concepts: https://langchain-ai.github.io/langgraph/concepts/memory/).

**Vector store (embedding index for retrieval).** In agent memory architectures, a *vector store* is an external database that stores text (or other artifacts) alongside their embedding vectors so the system can retrieve relevant past items by similarity search and inject them into the model’s context at inference time—supporting long-term memory beyond the context window (Weng, 2023: https://lilianweng.github.io/posts/2023-06-23-agent/).

**Episodic memory.** In the “cognitive architectures for language agents” framing (agentic-memory repo), *episodic memory* is historical experiences and their takeaways—i.e., records of what happened in prior interactions that can be recalled later to guide behavior (ALucek agentic-memory: https://github.com/ALucek/agentic-memory/tree/main). In LoCoMo’s benchmark construction, this corresponds closely to storing turn-level “observations” from prior sessions in long-term memory for later retrieval (LoCoMo: https://aclanthology.org/2024.acl-long.747.pdf).

**Semantic memory.** In the same cognitive-architecture framing, *semantic memory* is knowledge context and factual grounding—stable facts and concepts that are not tied to a single episode (ALucek agentic-memory: https://github.com/ALucek/agentic-memory/tree/main). In practice, semantic memory is often implemented via curated knowledge sources (documents, databases, KGs) and retrieval, rather than raw chat logs.

**Knowledge graph (KG).** A KG is “a graph of data consisting of semantically described entities and relations of different types that are integrated from different sources,” where entities have unique identifiers and semantics can be described by an ontology (KG pipeline explainer: https://arxiv.org/html/2302.11509). RDF formalizes this as sets of subject–predicate–object triples (RDF 1.1 Concepts: https://www.w3.org/TR/rdf11-concepts/).

**Mem0.** Mem0 (“mem-zero”) is a production-oriented “intelligent memory layer” for AI assistants/agents that supports multi-level memory (User, Session, Agent state) and provides APIs/SDKs to add and search memories; the repository claims +26% accuracy vs OpenAI Memory on the LoCoMo benchmark, 91% faster responses than full-context, and 90% fewer tokens (Mem0 repo: https://github.com/mem0ai/mem0).

**Personalization.** In Mem0’s framing, personalization is the system’s ability to remember user preferences and adapt responses over time (e.g., “Prefers dark mode and vim keybindings”), by storing and retrieving user-scoped memories across sessions (Mem0 repo: https://github.com/mem0ai/mem0). LangGraph similarly motivates long-term memory as enabling systems to “learn from feedback, and adapt to user preferences” across interactions (LangGraph Memory Concepts: https://langchain-ai.github.io/langgraph/concepts/memory/).

---

## Key Formulas & Empirical Results

### Long-term conversational memory evaluation: LoCoMo (benchmark scale + results)
**Dataset scale (LoCoMo Table 1 / Conclusion).** LoCoMo contains **10 conversations**, each **~588 turns** and **~16,618 tokens** on average, spanning **~27.2 sessions** (up to **32 sessions**) over **a few months**, and includes **multimodal** image sharing. Compared to MSC, LoCoMo is **16×** longer in tokens, **10×** more turns, and **5×** more sessions (LoCoMo: https://aclanthology.org/2024.acl-long.747.pdf).  
**Supports claim:** long-term memory must handle *multi-session* recall at much larger scales than typical chat datasets.

**QA task metric + best long-context baseline.**
- QA metric: **token-level F1** after normalization; answers drawn directly from dialogue; QA annotated with **turn IDs**; for RAG systems report **retrieval recall@k** (LoCoMo Sec. 4.1).
- Best long-context QA reported: **gpt-4-turbo 128K overall F1 51.6** (single-hop **72.3**, multi-hop **51.5**, temporal **51.4**, adversarial **15.7**) (LoCoMo Tables 2–4).  
**Supports claim:** even very large context windows struggle on very long-term multi-session recall, especially adversarial/unanswerable queries.

**RAG finding (signal-to-noise).** LoCoMo reports that storing history as **observations (assertions)** improves QA vs raw dialog, and retrieving too many items can hurt due to signal-to-noise (LoCoMo Sec. 6.1/Table 3).  
**Supports claim:** memory representation and retrieval size matter, not just “more context.”

### Recursive summarization memory update loop (LLM-Rsum)
**Two-stage decomposition (conceptual Eq. 1).** The paper frames response generation as memory update then response generation:  
\(p(y \mid \text{history}, x_t) = p(M \mid \text{history}) \cdot p(y \mid M, x_t)\) (LLM-Rsum: https://arxiv.org/html/2308.15022v3).  
**Supports claim:** treat memory as an explicit intermediate state.

**Memory update equation (Eq. 2).**  
\(M_t = \text{LLM}(P_m,\; M_{t-1},\; S_t)\)  
- \(M_t\): updated memory summary after session \(t\)  
- \(M_{t-1}\): previous memory  
- \(S_t\): dialogue session \(t\)  
- \(P_m\): memory-iteration prompt  
Initialize \(M_0=\) `"none"` (LLM-Rsum Sec. 4.1).  
**Supports claim:** long-term memory can be compressed incrementally with a Markov-style update.

**Response generation with memory (Eq. 3).**  
\(y_t = \text{LLM}(P_g,\; M_t,\; x_t)\)  
- \(x_t\): current session context  
- \(P_g\): response prompt emphasizing consistency with memory (LLM-Rsum Sec. 4.2).

**Implementation defaults.** Temperature **0**; retriever baselines use **BM25/DPR**, top-**k=3 or 5** utterances (LLM-Rsum implementation notes).

**Empirical deltas (selected).** On MSC session 5 (ChatGPT backbone): ChatGPT-Rsum **F1 20.48** vs vanilla ChatGPT **F1 19.41**; ablation “W/O Memory” **F1 18.94** (LLM-Rsum Table 3 & Table 5).  
**Supports claim:** explicit memory update improves long-horizon consistency modestly; retrieval + memory can be complementary (Table 8 shows BM25(k=5) **F1 20.91 → 21.81** with the framework).

### Long-context benchmark baselines: LongBench
**Formalization.** Given **(I, C)** → output **A**, where **I** and **A** are short, **C** is long (thousands of tokens) (LongBench Sec. 3.1: https://aclanthology.org/2024.acl-long.172.pdf).  
**Supports claim:** long-context handling is a distinct evaluation setting.

**Baseline overall scores (Overall-All).** GPT-3.5-Turbo-16k **44.7**; ChatGLM2-6B-32k **41.4**; Vicuna-16k **30.5**; LongChat-32k **31.6**; Llama2-4k **26.8** (LongBench Tables 2–3).  
**Supports claim:** longer context helps but does not solve long-context tasks; model choice matters.

**Truncation rule (when L > M).** Truncate from the middle: keep beginning and end  
\(S_{1:L} \to [S_{1:\lfloor M/2\rfloor};\; S_{L-\lfloor M/2\rfloor-1:L}]\) (LongBench Sec. 4.1).  
**Supports claim:** naive truncation strategies can systematically drop relevant middle content.

### MMR reranking (diverse memory retrieval)
**MMR objective (Carbonell & Goldstein, 1998).**  
\[
\arg\max_{D_i \in R \setminus S}\Big[\lambda\,\mathrm{Sim}_1(D_i,Q)\;-\;(1-\lambda)\max_{D_j\in S}\mathrm{Sim}_2(D_i,D_j)\Big]
\]
- \(Q\): query; \(R\): retrieved candidate set; \(S\): already-selected items  
- \(\mathrm{Sim}_1\): relevance similarity; \(\mathrm{Sim}_2\): redundancy similarity  
- \(\lambda \in [0,1]\): relevance–diversity tradeoff (MMR paper: https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf).  
**Supports claim:** you can reduce redundant retrieved memories while staying relevant.

### BM25 sparse retrieval (common memory retriever baseline)
**BM25 scoring (Lucene-style).**  
\[
R(q,d)=\sum_{t\in q} idf(t)\cdot \frac{tf_{t,d}}{k_1\left((1-b)+b\frac{l_d}{avl_d}\right)+tf_{t,d}}
\]
with  
\[
idf(t)=\log\frac{N-df(t)+0.5}{df(t)+0.5}
\]
Defaults: \(k_1\approx 2\), \(b\approx 0.75\) (BM25 paper: https://arxiv.org/pdf/0911.5046.pdf).  
**Supports claim:** sparse retrieval is a principled baseline for memory search; parameters control tf saturation and length normalization.

### OpenAI Responses API: truncation + output budgeting (production knobs)
- `truncation: "auto" | "disabled"` default **"disabled"**; `"auto"` drops input items **in the middle** to fit context; `"disabled"` causes a **400** if it would exceed the context window (Responses API ref: https://platform.openai.com/docs/api-reference/responses/list?lang=python).  
- `max_output_tokens`: caps generated tokens **including visible output + reasoning tokens** (same source).  
**Supports claim:** production systems must explicitly manage context overflow and output budgets.

---

## How It Works

### A. Canonical long-term memory loop (retrieve → generate → write-back)
1. **Ingest interaction artifacts**
   - Store raw turns (or structured “observations/assertions” as in LoCoMo) and optionally images/captions (LoCoMo Sec. 3.3).
2. **Index for recall**
   - Put items into a vector store (embedding index) for similarity search (Weng, 2023).
   - Optionally also index in sparse form (BM25) for lexical matching (BM25 sources above).
3. **Retrieve at query time**
   - Given the user’s new message, retrieve top-*k* relevant memories.
   - Optionally apply **MMR** to reduce redundancy among retrieved items (MMR paper).
4. **Assemble model context**
   - Combine: system instructions + current thread context (short-term) + retrieved long-term memories.
   - If using OpenAI Responses API, decide truncation behavior (`auto` vs `disabled`) and set `max_output_tokens` (Responses API ref).
5. **Generate response**
   - Condition the response on retrieved memories (LoCoMo’s agent conditions on retrieved observations; LLM-Rsum conditions on memory summary \(M_t\)).
6. **Write-back / update memory**
   - Add new memories extracted from the latest exchange (Mem0’s `memory.add(messages, user_id=...)` pattern).
   - Optionally update a compressed summary state \(M_t\) at session boundaries (LLM-Rsum Eq. 2).

### B. Recursive summarization (LLM-Rsum) as memory compression
Use when you can’t (or don’t want to) store/retrieve many raw turns.
1. Initialize \(M_0 =\) `"none"` (LLM-Rsum).
2. For each session \(t\):
   1) **Update memory**: \(M_t = \text{LLM}(P_m, M_{t-1}, S_t)\)  
   2) **Respond**: \(y_t = \text{LLM}(P_g, M_t, x_t)\)
3. Optionally combine with retrieval (LLM-Rsum Table 8 shows retrieval + framework improves).

### C. LoCoMo-style “observations” memory representation (benchmark construction)
1. After each session, produce a running summary \(w_k\) conditioned on session history \(h_k\) and prior summary \(w_{k-1}\) (LoCoMo Sec. 3.3).
2. Store turn-level **observations** \(o_{k,j}\) in long-term memory (assertion-like units).
3. Generate responses conditioned on persona \(p\), current session history, retrieved observations, and between-session events from an event graph \(G\) (LoCoMo Sec. 3.2–3.3).
4. Empirical note: observations help vs raw dialog; too many retrieved items hurts (LoCoMo Sec. 6.1).

---

## Teaching Approaches

### Intuitive (no math)
- **“Sticky notes vs diary vs encyclopedia.”** Short-term memory is what’s on the desk right now (current messages). Long-term memory is the filing cabinet: you don’t dump the whole cabinet onto the desk; you pull a few relevant notes (retrieval) or keep a running “executive summary” (recursive summarization). Knowledge graphs are the encyclopedia with explicit links (entities/relations) rather than piles of notes.

### Technical (with math)
- **Memory as an explicit latent state.** Use LLM-Rsum’s decomposition: update a memory state \(M_t\) from \((M_{t-1}, S_t)\), then generate \(y_t\) from \((M_t, x_t)\) (LLM-Rsum Eq. 2–3). Retrieval is a separate operator that selects a subset of stored items; MMR formalizes selection to trade off relevance and redundancy via \(\lambda\) (MMR Eq. 1).

### Analogy-based
- **Database query planner analogy.** The model is like an application server with limited RAM (context window). Vector store / BM25 are indexes. Retrieval is a query plan: fetch top-*k* rows, maybe rerank for diversity (MMR), then render a response. If you exceed RAM, the system either errors or truncates (Responses API `truncation` behavior).

---

## Common Misconceptions

1. **“If the model has a 128K context window, we don’t need long-term memory.”**  
   **Why wrong:** LoCoMo shows even the best long-context baseline (gpt-4-turbo 128K) achieves only **51.6** overall QA F1 and collapses on adversarial questions (**15.7**) (LoCoMo Tables 2–4). Long contexts can also add noise.  
   **Correct model:** Long context is not the same as *selective recall*. Long-term memory systems use retrieval/representation (e.g., observations) to improve signal-to-noise (LoCoMo Sec. 6.1).

2. **“Long-term memory is just saving the entire chat log.”**  
   **Why wrong:** Raw logs are hard to retrieve from and can overwhelm the model; LoCoMo reports better QA when storing history as **observations/assertions** rather than raw dialog, and retrieving too many items hurts (LoCoMo Sec. 6.1).  
   **Correct model:** Long-term memory is *stored + indexed + selectively retrieved* information, often transformed into more queryable units (observations, summaries).

3. **“Summarization memory is always safer than retrieval because it’s shorter.”**  
   **Why wrong:** LLM-Rsum reports memory summaries can contain errors (fabricated facts **2.7%**, incorrect relationships **3.2%**, missing details **3.9%** in sampled summaries) (LLM-Rsum Table 6).  
   **Correct model:** Summaries are compression with potential information loss/error; retrieval can complement summarization (LLM-Rsum Table 8).

4. **“Truncation is a harmless implementation detail.”**  
   **Why wrong:** LongBench specifies a concrete truncation rule (drop the middle) when inputs exceed max length (LongBench Sec. 4.1). Dropping the middle can systematically remove the needed evidence. Responses API `truncation="auto"` also drops items in the middle (Responses API ref).  
   **Correct model:** Truncation policy is part of the algorithm; it changes what evidence is available and can change correctness.

5. **“Personalization just means adding a ‘persona prompt’.”**  
   **Why wrong:** Mem0’s personalization is implemented by storing and retrieving user-scoped memories across sessions (e.g., “Prefers dark mode and vim keybindings”) and updating over time (Mem0 repo). A static persona prompt doesn’t update from interaction.  
   **Correct model:** Personalization is *persistent, user-scoped state* with write-back and later recall.

---

## Worked Examples

### 1) Minimal Mem0-style personalization loop (retrieve → respond → add)
From the Mem0 repository pattern (Python) (Mem0: https://github.com/mem0ai/mem0):

```python
from openai import OpenAI
from mem0 import Memory

openai_client = OpenAI()
memory = Memory()

def chat_with_memories(message: str, user_id: str = "default_user") -> str:
    # 1) Retrieve relevant memories
    relevant = memory.search(query=message, user_id=user_id, limit=3)
    memories_str = "\n".join(f"- {e['memory']}" for e in relevant["results"])

    # 2) Inject into system prompt
    system_prompt = (
        "You are a helpful AI. Answer the question based on query and memories.\n"
        f"User Memories:\n{memories_str}"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    # 3) Generate
    resp = openai_client.chat.completions.create(
        model="gpt-4.1-nano-2025-04-14",
        messages=messages
    )
    assistant = resp.choices[0].message.content

    # 4) Write-back: add the new exchange to memory
    messages.append({"role": "assistant", "content": assistant})
    memory.add(messages, user_id=user_id)

    return assistant
```

**Tutor notes (what to emphasize mid-conversation):**
- The *mechanism* of personalization is the `user_id`-scoped store + retrieval + write-back (Mem0 repo).
- `limit=3` is a concrete example of controlling retrieval size to avoid noise (connect to LoCoMo’s “too many retrieved items hurts”).

### 2) Recursive summarization memory (LLM-Rsum) skeleton
Directly mirrors Eq. 2–3 (LLM-Rsum: https://arxiv.org/html/2308.15022v3):

```python
M = "none"  # M_0

for session in sessions:  # each S_t
    # Update memory summary at session end
    M = LLM(prompt=P_m, inputs=[M, session.transcript])

    # During next session, respond using memory + current context x_t
    y = LLM(prompt=P_g, inputs=[M, session.current_context])
```

**Tutor notes:**
- This is a *compression* strategy; discuss error modes using the paper’s sampled summary error rates (LLM-Rsum Table 6).
- Mention complementarity: retrieval + framework improved BM25(k=5) F1 **20.91 → 21.81** (LLM-Rsum Table 8).

---

## Comparisons & Trade-offs

| Approach | What is stored | How recall works | Strengths (per sources) | Weaknesses / risks (per sources) | Choose when |
|---|---|---|---|---|---|
| **Full long-context (no external memory)** | Entire conversation in context window | None (model attends over all tokens) | Simple; no infra | LoCoMo: even 128K context has limited QA F1 (**51.6**) and poor adversarial (**15.7**) (LoCoMo) | Prototyping; very short histories |
| **Retrieval over stored items (vector store / BM25)** | Many discrete items (turns, observations, docs) | Similarity search; top-*k* injection; optionally MMR | Selective recall; can reduce token usage vs full context (motivated by Weng; Mem0 claims efficiency) | Too many retrieved items hurts (LoCoMo Sec. 6.1); retrieval misses if indexing/representation is poor | Multi-session assistants; scalable memory |
| **Observation/assertion memory** (LoCoMo-style) | Turn-level “observations” (assertions) | Retrieve observations relevant to query | Improves QA vs raw dialog (LoCoMo Sec. 6.1) | Requires extraction/structuring step; still needs retrieval tuning | When raw logs are noisy |
| **Recursive summarization (LLM-Rsum)** | A rolling summary \(M_t\) | Always include \(M_t\) | Fits tight context budgets; modest gains vs no memory (LLM-Rsum) | Summary errors (fabrication/incorrect/missing) (LLM-Rsum Table 6); may omit details | When you need compact persistent state |
| **Knowledge graph memory** | Entities/relations with IDs (triples) | Graph queries / structured retrieval | Explicit semantics + integration across sources (KG definition) | Requires extraction/integration/maintenance pipeline (KG pipeline explainer) | When facts/relations must be canonical and queryable |

---

## Prerequisite Connections

- **Context windows & token budgeting.** Needed to understand why long conversations break and why APIs expose truncation/output caps (Responses API `truncation`, `max_output_tokens`).
- **Retrieval basics (sparse vs dense).** Needed to reason about vector stores vs BM25 and why retrieval can miss or return noise (BM25 formula sources; Weng’s vector-store framing).
- **Summarization as compression.** Needed to understand recursive memory updates and their error modes (LLM-Rsum).
- **Graph data modeling (triples/entities/relations).** Needed to understand what a knowledge graph stores and why it differs from text memories (KG pipeline explainer; RDF 1.1 Concepts).

---

## Socratic Question Bank

1. **If you could only retrieve 3 memories for a user query, what criteria would you use to choose them—and what failure happens if you retrieve 30?**  
   *Good answer:* discusses relevance vs noise; references LoCoMo’s “too many retrieved items hurts” signal-to-noise issue.

2. **What’s the difference between “episodic” and “semantic” memory in an agent—can you give one example of each from a chat assistant?**  
   *Good answer:* episodic = past interaction event; semantic = stable fact/knowledge; aligns with agentic-memory definitions.

3. **Why might a rolling summary \(M_t\) drift over time, and how would you detect or mitigate that?**  
   *Good answer:* mentions summary error types (fabrication/incorrect/missing) from LLM-Rsum; suggests cross-checking with retrieval or source grounding.

4. **Suppose the key evidence is in the middle of a long document/chat. What happens under “truncate from the middle” policies?**  
   *Good answer:* explains LongBench truncation rule and why it can delete needed evidence; connects to Responses API `truncation="auto"`.

5. **How would you evaluate whether your long-term memory system is working across months of sessions?**  
   *Good answer:* proposes LoCoMo-style multi-session QA/event summarization; mentions token-level F1 and retrieval recall@k.

6. **When would you prefer a knowledge graph over a vector store for long-term memory?**  
   *Good answer:* KG for canonical entities/relations and integrated sources; vector store for fuzzy semantic recall; references KG definition/pipeline.

7. **What does the MMR \(\lambda\) trade off, and what behavior do you expect at \(\lambda=1\) vs \(\lambda=0\)?**  
   *Good answer:* \(\lambda=1\) pure relevance; \(\lambda=0\) pure diversity (MMR paper).

8. **If a user says “remember I prefer vim keybindings,” where should that live: short-term state, episodic memory, or user long-term memory? Why?**  
   *Good answer:* user long-term memory/personalization; references Mem0’s example.

---

## Likely Student Questions

**Q: How do we *measure* long-term conversational memory across many sessions?**  
→ **A:** LoCoMo evaluates very long-term memory with multi-session conversations (~**588 turns**, ~**27.2 sessions**, multimodal) and tasks including QA (token-level **F1**), event summarization (FactScore precision/recall/F1), and multimodal dialog generation (MMRelevance). QA answers are drawn from the dialogue and annotated with turn IDs; RAG systems also report retrieval **recall@k** (LoCoMo: https://aclanthology.org/2024.acl-long.747.pdf).

**Q: Do huge context windows solve long-term memory? What do benchmarks show?**  
→ **A:** On LoCoMo QA, the best reported long-context baseline is **gpt-4-turbo 128K** with overall F1 **51.6**, and adversarial F1 **15.7** (LoCoMo Tables 2–4), far below human QA F1 **87.9**. This indicates long context alone is insufficient for robust long-term recall.

**Q: What’s the concrete algorithm for recursive summarization memory?**  
→ **A:** LLM-Rsum updates memory each session via \(M_t=\text{LLM}(P_m, M_{t-1}, S_t)\) (initialize \(M_0=\)"none"), then generates responses via \(y_t=\text{LLM}(P_g, M_t, x_t)\) (LLM-Rsum: https://arxiv.org/html/2308.15022v3).

**Q: How accurate are summary memories—do they hallucinate?**  
→ **A:** LLM-Rsum reports sampled summary error rates: fabricated facts **2.7%**, incorrect relationships **3.2%**, missing details **3.9%** (LLM-Rsum Table 6), indicating summaries can drift and should be monitored/grounded.

**Q: Why not just retrieve *more* memories to be safe?**  
→ **A:** LoCoMo reports that retrieving too many items can hurt due to signal-to-noise; representing history as “observations/assertions” helps QA vs raw dialog, but over-retrieval still degrades performance (LoCoMo Sec. 6.1/Table 3).

**Q: What is MMR and how does it help memory retrieval?**  
→ **A:** MMR selects items to maximize \(\lambda\)·relevance to the query minus (1−\(\lambda\))·redundancy with already-selected items:  
\(\arg\max_{D_i\in R\setminus S}[\lambda Sim_1(D_i,Q)-(1-\lambda)\max_{D_j\in S}Sim_2(D_i,D_j)]\). \(\lambda=1\) gives pure relevance ranking; \(\lambda=0\) gives maximal diversity (MMR paper: https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf).

**Q: What happens if my conversation exceeds the model context window in production?**  
→ **A:** In the OpenAI Responses API, `truncation` defaults to `"disabled"` (request fails with **400** if it would exceed the window). If set to `"auto"`, the API drops input items **in the middle** to fit. You can also cap output with `max_output_tokens` (Responses API ref: https://platform.openai.com/docs/api-reference/responses/list?lang=python).

**Q: What’s a knowledge graph, precisely (not just “nodes and edges”)?**  
→ **A:** A KG is “a graph of data consisting of semantically described entities and relations of different types that are integrated from different sources,” with unique identifiers for entities and often an ontology describing semantics (https://arxiv.org/html/2302.11509). In RDF, it is a set of subject–predicate–object triples (https://www.w3.org/TR/rdf11-concepts/).

---

## Available Resources

### Articles & Tutorials
- [LLM Powered Autonomous Agents (Lilian Weng, 2023)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student asks “why do agents need long-term memory?” or “how do vector stores fit into agent architecture?”
- [LangGraph Memory Concepts](https://langchain-ai.github.io/langgraph/concepts/memory/) — Surface when: student asks about thread-scoped vs cross-thread memory, namespaces, or production persistence patterns.
- [Generative Agents: Interactive Simulacra of Human Behavior (Park et al., 2023)](https://arxiv.org/abs/2304.03442) — Surface when: student asks for a canonical agent architecture combining memory stream + reflection + planning.
- [mem0ai/mem0 GitHub repository](https://github.com/mem0ai/mem0) — Surface when: student asks for a concrete memory SDK/API pattern (add/search) or multi-level memory (User/Session/Agent).
- [End-to-end KG Construction Pipeline & Requirements](https://arxiv.org/html/2302.11509) — Surface when: student asks “how do you build/maintain a KG?” or RDF vs property graph tradeoffs.
- [RDF 1.1 Concepts and Abstract Syntax (W3C)](https://www.w3.org/TR/rdf11-concepts/) — Surface when: student needs authoritative definitions of RDF graphs, triples, datasets, IRIs.

---

## Visual Aids

![Human memory taxonomy mapped to LLM agent memory components. (Weng, 2023)](/api/wiki-images/agent-memory/images/lilianweng-posts-2023-06-23-agent_008.png)  
**Show when:** student confuses short-term vs long-term vs episodic/semantic/procedural memory; use to anchor terminology before implementation details.

![Generative agent architecture: memory stream, reflection, and planning enable human-like behavior. (Park et al. 2023)](/api/wiki-images/agent-memory/images/lilianweng-posts-2023-06-23-agent_012.png)  
**Show when:** student asks “what does an agent memory system look like end-to-end?” or how memory connects to planning/reflection.

![LLM-powered autonomous agent system overview. (Weng, 2023)](/api/wiki-images/agent-memory/images/lilianweng-posts-2023-06-23-agent_001.png)  
**Show when:** student needs the big-picture map (planning + memory + tools) before diving into long-term memory mechanics.

---

## Key Sources

- [LoCoMo — Very Long-Term Conversational Memory Benchmark](https://aclanthology.org/2024.acl-long.747.pdf) — Most direct empirical evidence on multi-session conversational memory limits and RAG/observation design effects.
- [Recursive Summarization for Long-Term Dialogue Memory (LLM-Rsum)](https://arxiv.org/html/2308.15022v3) — Concrete memory-update equations and deployment-style loop for summary-based long-term memory.
- [LangGraph Memory Concepts](https://langchain-ai.github.io/langgraph/concepts/memory/) — Practical, production-oriented distinctions: thread-scoped vs cross-thread long-term memory and persistence.
- [LLM Powered Autonomous Agents (Lilian Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Clear conceptual framing of memory in agent architectures and why external memory is needed.
- [End-to-end KG Construction Pipeline & Requirements](https://arxiv.org/html/2302.11509) — Authoritative definition of KGs plus pipeline components (extraction → integration → QA → maintenance) relevant to “semantic memory” implementations.