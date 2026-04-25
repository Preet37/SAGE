# Reference KB Eval Report
*Generated 2026-04-13 03:16*

Comparing **old stored KB (A)** vs **new prompt KB (B)** for 3 lesson(s).

---

## Comparing Agentic Frameworks: LangGraph, AutoGen, CrewAI, and OpenAI Assistants
*Slug: `comparing-agentic-frameworks-langgraph-autogen-crewai-openai`*

**Sources:** 32 pedagogy, 42 reference — *Blended (reference + pedagogy)*

| Dimension | Old (A) | New (B) |
|---|---|---|
| Definition Precision | 4/5 | 5/5 ▲+1 |
| Explanation Diversity | 2/5 | 3/5 ▲+1 |
| Misconception Coverage | 1/5 | 2/5 ▲+1 |
| Teaching Utility | 1/5 | 2/5 ▲+1 |
| Resource Inventory | 2/5 | 2/5 |
| **TOTAL** | **10/25** | **14/25 (▲+4)** |

**Verdict: New wins** — Document B is more precise and instructionally actionable (clearer control-flow framing, better LangGraph semantics, and added formulas/results), even though both are weak on explicit tutoring scaffolds and curated resource guidance.

- Old strengths: Provides many concrete, mostly quotable definitions of LangGraph concepts (state/reducers/super-steps/checkpoints) with citations.
- Old weaknesses: Lacks misconception corrections, teaching scaffolds (questions/examples), and a curated resource catalog with guidance on when to use it.
- New strengths: More cohesive and operationally precise (especially around reducers, super-steps, durable execution, and interrupt/resume) and adds formulas/results that support explanation and sizing.
- New weaknesses: Still provides little explicit Socratic questioning/worked examples and does not curate resources into a 'what to show when' inventory.

<details><summary>New KB (B) — click to expand</summary>

```markdown
## Core Definitions

**Control flow (in agent frameworks)**  
Control flow is the framework’s *default* way of deciding “what runs next” (and under what conditions), including how loops, branching, parallelism, and termination are represented. In LangGraph, this is explicit nodes/edges over shared state; in AutoGen it is multi-agent message exchange with turn/termination rules; in CrewAI it is Flow steps that trigger Crews/Tasks; in OpenAI’s Agents framing it is a managed tool-call loop that runs until a stop condition is met (e.g., no tool calls). (LangGraph execution model: GitHub discussions #2290, #938; AutoGen reference; OpenAI production guide PDF)

**LangGraph (explicit graphs as control flow)**  
LangGraph is a low-level orchestration framework where you define a graph of **nodes** (functions) and **edges** (routing), operating over a shared **State** snapshot. Nodes return partial state updates that are merged via per-key **reducers**; execution proceeds in discrete **super-steps** (Pregel/BSP-inspired) and can checkpoint state at each step for durability and human-in-the-loop. (LangGraph repo README; discussions #4730, #2290, #938; LangGraph persistence docs)

**State (LangGraph)**  
State is a shared snapshot passed to nodes, defined by a schema (e.g., `TypedDict`/Pydantic) where each key/channel can have a reducer that specifies how updates merge into prior values. Keys without reducers overwrite by default; keys with reducers (e.g., `add_messages`) aggregate updates (often append/merge). (Discussions #4730, #938, #3459, #3810; `StateGraph.compile` reference)

**Reducer (LangGraph)**  
A reducer is a per-state-key merge function: `new_value = reducer(old_value, update_value)`. If no reducer is specified, updates replace the prior value. Reducers are central to correctness under parallel steps, retries, and replay (e.g., append reducers can duplicate on re-execution unless designed to be idempotent). (Discussions #4730, #3459, #3810; `StateGraph.compile` reference)

**Super-step (LangGraph)**  
A super-step is a single “tick” of execution where all runnable nodes for that step execute (potentially in parallel), then their updates are applied deterministically; LangGraph checkpoints at super-step boundaries when persistence is enabled. You can only resume/replay from a checkpoint (i.e., a super-step boundary). (Discussions #2290, #938; LangGraph persistence docs; JS `CompiledStateGraph` reference)

**Durable execution (LangGraph)**  
Durable execution means saving progress at key points so a workflow can pause and later resume from the last recorded state, enabling long-running tasks, fault recovery, and human-in-the-loop. LangGraph provides this via its persistence layer (checkpointers) that save a checkpoint at each super-step; guidance emphasizes determinism/idempotency and isolating side effects in tasks/nodes to avoid duplication on replay. (LangGraph durable execution docs; persistence docs; discussions #2290; Aerospike blog)

**Checkpoint / Thread (LangGraph persistence)**  
A **thread** is the primary key (`thread_id`) grouping a sequence of checkpoints for an execution history; a **checkpoint** is a snapshot of graph state at a super-step. Checkpoints enable memory across turns, time travel/forking, and fault tolerance; without `thread_id`, the checkpointer cannot save or resume state. (LangGraph persistence docs; Python checkpoints reference; JS checkpointer reference; AWS DynamoDBSaver blog)

**Interrupt / resume (LangGraph human-in-the-loop)**  
An interrupt is a dynamic pause triggered by calling `interrupt(value)` inside a node. The first call raises a `GraphInterrupt` and surfaces the payload to the caller; later, the graph resumes when re-invoked with `Command(resume=...)`, and the resume value becomes the return value of `interrupt()` inside the node. Interrupts require checkpointing. (LangGraph HITL/interrupts docs; Python `langgraph.types` reference; discussions #938, #2290)

**Multi-agent orchestr [truncated...]
```
</details>

---

## Retrieval-Augmented Generation (RAG) Inside Agents
*Slug: `retrieval-augmented-generation-inside-agents`*

**Sources:** 7 pedagogy, 11 reference — *Blended (reference + pedagogy)*

| Dimension | Old (A) | New (B) |
|---|---|---|
| Definition Precision | 4/5 | 5/5 ▲+1 |
| Explanation Diversity | 2/5 | 2/5 |
| Misconception Coverage | 1/5 | 2/5 ▲+1 |
| Teaching Utility | 2/5 | 2/5 |
| Resource Inventory | 2/5 | 2/5 |
| **TOTAL** | **11/25** | **13/25 (▲+2)** |

**Verdict: New wins** — Document B is more quotable and slightly broader in empirical coverage (adds Spotify and clearer attributions), while both are similarly weak on misconceptions, teaching scaffolds, and curated resource guidance.

- Old strengths: Has fairly precise, source-linked definitions plus several concrete DPR implementation details and metrics that are directly quotable.
- Old weaknesses: Lacks explicit misconceptions, Socratic prompts/worked examples, and any curated resource guidance beyond raw citations (and it is truncated/incomplete at the end).
- New strengths: Provides more consistently quotable definitions with clearer attribution and adds an additional real-world dense-retrieval example (Spotify) that broadens empirical grounding.
- New weaknesses: Still offers minimal teaching scaffolding (no Socratic questions or worked examples), little explicit misconception correction, and the resource list is not organized by 'when to show' (also truncated at the end).

<details><summary>New KB (B) — click to expand</summary>

```markdown
## Core Definitions

**Retrieval-Augmented Generation (RAG).** Lewis et al. define RAG as a model family that “combine[s] pre-trained parametric and non-parametric memory for language generation,” where the non-parametric memory is “a dense vector index of Wikipedia, accessed with a pre-trained neural retriever” and retrieved passages are used to condition generation at inference time. Source: https://arxiv.org/abs/2005.11401

**Embedding-based retrieval (dense retrieval).** Dense retrieval represents queries and documents/passages as vectors in a shared space and retrieves nearest neighbors by a similarity function (e.g., dot product or cosine). DPR operationalizes this as separate encoders for questions and passages, retrieving top‑k passages by maximum inner product search over a prebuilt ANN index. Source: https://aclanthology.org/2020.emnlp-main.550.pdf

**Vector search / Approximate Nearest Neighbor (ANN) search.** Vector search finds nearest vectors to a query embedding under a similarity/distance metric; ANN methods trade exactness for speed/scale. DPR explicitly uses FAISS to index ~21M passage vectors and retrieve top‑k efficiently at runtime. Sources: https://aclanthology.org/2020.emnlp-main.550.pdf, https://arxiv.org/html/2401.08281v2

**Document chunking.** Chunking is the segmentation of documents into retrievable units prior to embedding and indexing; it governs semantic coherence of embeddings and affects retrieval effectiveness and efficiency. A large-scale study of 36 segmentation methods finds content-aware chunking can substantially outperform naive fixed-length splitting. Source: https://arxiv.org/html/2603.06976

**Context injection (augmentation).** In agentic systems, “Just-in-Time (JIT) instructions” are a context injection pattern: return relevant instructions alongside tool data only when needed—aiming for “perfect context… not a token less, not a token more.” This is used to avoid bloated prompts (“Death by a Thousand Instructions”). Source: https://shopify.engineering/building-production-ready-agentic-systems

**Grounded generation / provenance.** KILT formalizes grounding by requiring outputs to be justified by retrieved Wikipedia provenance (spans/pages). KILT scores award downstream credit only if retrieval ranks a complete provenance set at the top (R‑precision = 1). Source: https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf

**Agentic workflows (plan–act loop with tools).** Shopify describes an agentic loop as: human input → LLM decides actions → actions executed via tools/environment → feedback collected → loop continues until task completion. In production guidance, OpenAI’s agent definition emphasizes that the LLM controls workflow execution and uses tools to gather context/take actions within guardrails. Sources: https://shopify.engineering/building-production-ready-agentic-systems, https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

**Long-term memory retrieval (agent memory via retrieval).** Agent memory can be implemented as retrieval over stored artifacts (e.g., vector stores/ANN indexes) that are read during the agent loop; a memory taxonomy frames memory as a write–manage–read loop with objectives including utility, efficiency, and faithfulness (stale/hallucinated recall can be worse than none). Source: https://arxiv.org/html/2603.07670v1


## Key Formulas & Empirical Results

### Dense retrieval scoring + training (DPR)
- **Similarity (dot product; DPR Eq. 1):**
  \[
  \mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)
  \]
  - \(E_Q(\cdot)\): question encoder; \(E_P(\cdot)\): passage encoder; both output \(\mathbb{R}^d\).
  - Supports **precomputing passage embeddings** and doing **maximum inner product search** at runtime.  
  Source: https://aclanthology.org/2020.emnlp-main.550.pdf

- **Training objective (softmax over positives + negatives; DPR Eq. 2):**
  \[
  \mathcal{L}=-\log \frac{e^{\mathrm{sim}(q_i,p_i^+) [truncated...]
```
</details>

---

## LoRA & Parameter-Efficient Methods
*Slug: `lora-parameter-efficient`*

> **Error:** New KB generation returned empty — likely no wiki downloads for this lesson's concepts.

## Summary
- New wins: **2**
- Old wins: **0**
- Ties: **0**