## Core Definitions

**Retrieval-Augmented Generation (RAG)**  
Retrieval-Augmented Generation is a generation setup that *retrieves relevant document chunks from an external knowledge store at inference time and conditions the language model on them*, improving factuality, transparency/provenance, and allowing knowledge updates without retraining. Lewis et al. (2020/2021) motivate RAG as combining **parametric memory** (the seq2seq model weights) with **non-parametric memory** (a dense vector index, e.g., Wikipedia) accessed by a neural retriever. (https://arxiv.org/abs/2005.11401; also survey: https://arxiv.org/html/2312.10997v5)

**Vector search (Approximate Nearest Neighbor / ANN search)**  
Vector search retrieves items by nearest-neighbor similarity in an embedding space (rather than keyword overlap), typically using ANN indexes for speed at scale. DPR describes the practical pipeline: precompute passage embeddings, build an ANN index (FAISS), embed the query at runtime, and retrieve top‑k by similarity. (https://aclanthology.org/2020.emnlp-main.550.pdf; FAISS overview: https://arxiv.org/html/2401.08281v2)

**Embedding-based retrieval (dense retrieval / dual-encoder retrieval)**  
Embedding-based retrieval encodes queries and candidate passages into vectors in the same space and scores them with a similarity function (e.g., dot product or cosine). DPR (Dense Passage Retrieval) is a canonical dual-encoder: a question encoder \(E_Q\) and passage encoder \(E_P\) produce vectors; similarity is computed efficiently because passage vectors are precomputed. (https://aclanthology.org/2020.emnlp-main.550.pdf)

**Document chunking**  
Document chunking is the segmentation of source documents into retrievable units (“chunks”) prior to embedding and indexing; chunking choices strongly affect dense retrieval effectiveness and efficiency. A large-scale chunking study benchmarks 36 segmentation methods and finds content-aware chunking can substantially outperform naive fixed-length splitting (e.g., paragraph grouping best overall in their study). (https://arxiv.org/html/2603.06976)

**Context injection (augmentation)**  
Context injection is the act of placing retrieved evidence (and sometimes just-in-time instructions) into the model’s input context so generation is conditioned on that material. Shopify describes “Just-in-Time (JIT) instructions” as returning relevant instructions alongside tool data only when needed—aiming for “perfect context… not a token less, not a token more.” (https://shopify.engineering/building-production-ready-agentic-systems)

**Grounded generation (evidence-attributed generation)**  
Grounded generation is generation that is supported by retrieved evidence, often evaluated by requiring correct provenance. KILT operationalizes this by awarding downstream points only if retrieval places a complete provenance set at the top (R-precision = 1), highlighting the gap between task accuracy and evidence-grounded accuracy. (https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)

**Agentic workflows (tool-using agent loop)**  
An agentic workflow is a loop where an LLM decides actions (often tool calls), executes them, observes results, and iterates until completion. OpenAI’s practical guide defines agents as systems that “independently accomplish tasks on your behalf,” characterized by the LLM controlling workflow execution and using tools to gather context/take actions within guardrails. (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Long-term memory retrieval (for agents)**  
Long-term memory retrieval is an agent memory mechanism where past information is stored outside the context window (often in a vector store) and retrieved on demand to inform current decisions. The agent memory taxonomy paper frames memory as a write–manage–read loop and lists vector stores (ANN/FAISS) as a common substrate for long-term recall. (https://arxiv.org/html/2603.07670v1)

---

## Key Formulas & Empirical Results

### DPR dual-encoder scoring + training (Dense Passage Retrieval)
**Similarity (dot product; DPR Eq. 1):**  
\[
\mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)
\]  
- \(E_Q(q)\in\mathbb{R}^d\): question embedding  
- \(E_P(p)\in\mathbb{R}^d\): passage embedding  
**Claim supported:** dot product is decomposable so passage embeddings can be precomputed; DPR reports it works well vs L2/cosine in ablations. (https://aclanthology.org/2020.emnlp-main.550.pdf)

**Training objective (softmax over positives+negatives; DPR Eq. 2):**  
\[
\mathcal{L}=-\log \frac{e^{\mathrm{sim}(q_i,p_i^+)}}{e^{\mathrm{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\mathrm{sim}(q_i,p_{i,j}^-)}}
\]  
- \(p_i^+\): positive passage for question \(q_i\)  
- \(p_{i,j}^-\): negatives  
**Claim supported:** contrastive learning for retrieval; enables in-batch negatives. (same source)

**In-batch negatives (DPR Sec. 3.2):** batch size \(B\), similarity matrix \(S=QP^\top\in\mathbb{R}^{B\times B}\); diagonal pairs are positives, off-diagonals are negatives → \(B-1\) negatives per question, effectively \(B^2\) pairs/batch. (same source)

**Implementation defaults / scale (DPR):**
- Two independent BERT-base encoders; use \([CLS]\); \(d=768\).  
- Passage units: fixed **100-word blocks**.  
- Wikipedia snapshot: **21,015,324** passages.  
- FAISS retrieval throughput: ~**995 questions/sec** (top‑100).  
- Index build: embed 21M passages ~**8.8h on 8 GPUs**; build FAISS index ~**8.5h**. (same source)

**Top‑20 retrieval accuracy examples (DPR Table 2):**
- NQ: **78.4** (DPR) vs **59.1** (BM25)  
- TriviaQA: **79.4** vs **66.9**  
- WQ: **73.2** vs **55.0**  
- TREC: **79.8** vs **70.9**  
- SQuAD exception: DPR **63.2** vs BM25 **68.8**  
BM25+DPR can improve (e.g., TREC **85.2** Top‑20). (same source)

### KILT: retrieval metrics + “only-if-evidence” scoring
**R-precision (KILT Sec. 5):** \(R\) = #pages in a provenance set, \(r\) = #relevant pages in top‑\(R\) retrieved; report max over provenance sets per input. (https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)

**Recall@k (KILT Sec. 5):** \(n\) = #distinct provenance sets, \(w\) = #complete provenance sets found in top‑k; Recall@k = \(w/n\). (same source)

**KILT scoring rule:** KILT-EM/F1/etc. award downstream points **only if R-precision = 1** (complete provenance set ranked at the top). (same source)

**Illustrative gap (KILT Tables 3–5):**
- RAG NQ: EM **44.39** but KILT‑EM **32.69**  
- RAG Hotpot: EM **26.97** but KILT‑EM **3.21**  
**Claim supported:** downstream correctness can hide missing/incorrect evidence attribution. (same source)

### Chunking strategy empirical results (dense retrieval sensitivity)
A chunking study reports content-aware chunking improves retrieval over naive fixed-size splitting; their top strategy “Paragraph Group Chunking” achieves mean **nDCG@5 0.459**, with **Precision@1 24%**, **Hit@5 59%**, while fixed-size character chunking baselines have **nDCG@5 < 0.244** and **Precision@1 2–3%**. (https://arxiv.org/html/2603.06976)

---

## How It Works

### A. “Naive” RAG inside an agent loop (single retrieval call)
1. **Ingest documents**
   - Collect corpus (private docs, policies, manuals, etc.).
2. **Chunk**
   - Split documents into retrievable units (chunking strategy matters; see chunking study). (https://arxiv.org/html/2603.06976)
3. **Embed chunks**
   - Compute embedding vector per chunk using an embedding model.
4. **Index**
   - Store vectors + metadata in a vector index (ANN). DPR uses FAISS; production systems may use vector DBs/ANN services. (https://aclanthology.org/2020.emnlp-main.550.pdf; https://arxiv.org/html/2401.08281v2)
5. **At query time**
   - Embed the user query (or agent sub-question) into a query vector.
6. **Retrieve top‑k**
   - ANN search returns top‑k chunks by similarity (dot product in DPR). (DPR Eq. 1)
7. **Context injection**
   - Insert retrieved chunks into the model input (often with formatting + citations).
8. **Generate**
   - LLM produces an answer conditioned on the injected evidence.

### B. Agentic RAG (retrieval as a tool the planner can call repeatedly)
In an agentic workflow, retrieval is not a one-shot pre-step; it’s a callable tool inside the loop.

**Loop sketch (aligned with “agent loop” descriptions in Shopify/OpenAI guides):**
1. **User request arrives**
2. **LLM decides next action**
   - Could be: retrieve, ask a clarifying question, call another tool, or answer.
3. **If retrieval needed: call retrieval tool**
   - Often multiple times:
     - broaden query → retrieve
     - refine query → retrieve again
     - retrieve for each sub-question (multi-hop)
4. **Inject results + JIT instructions**
   - Shopify pattern: return relevant instructions alongside tool data only when needed (“perfect context…”). (https://shopify.engineering/building-production-ready-agentic-systems)
5. **Generate grounded output**
6. **Stop condition**
   - OpenAI guide: loop ends when a final-output tool is invoked or the model returns without tool calls. (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

### C. Concrete retrieval mechanics (DPR-style dense retrieval)
**Offline**
1. Chunk Wikipedia into fixed 100-word blocks (DPR default).
2. Compute passage vectors \(v_p = E_P(p)\).
3. Build FAISS ANN index over all \(v_p\). (https://aclanthology.org/2020.emnlp-main.550.pdf)

**Online**
1. Compute query vector \(v_q = E_Q(q)\).
2. Retrieve top‑k by maximum inner product search using \(v_q^\top v_p\).
3. Return passages for context injection. (same source)

### D. Evidence-grounded evaluation (KILT-style)
1. Each example includes **provenance**: spans/pages sufficient to justify the output.
2. Retrieval is scored with R-precision / Recall@k.
3. Downstream score is only counted if evidence is correctly retrieved at the top (R-precision = 1). (https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)

---

## Teaching Approaches

### Intuitive (no math)
- **RAG = “open-book mode.”** The model doesn’t rely only on what it memorized during training; it looks up relevant pages from your knowledge base and then answers using those pages.
- **Inside agents:** retrieval becomes a *repeatable action*—the agent can look things up multiple times as it decomposes the task.

### Technical (with math)
- Dense retrieval uses two encoders \(E_Q, E_P\) mapping text to \(\mathbb{R}^d\). DPR scores with dot product \(E_Q(q)^\top E_P(p)\) and trains with a softmax contrastive loss over positives and negatives (including in-batch negatives). (https://aclanthology.org/2020.emnlp-main.550.pdf)
- Grounding can be evaluated separately from task accuracy using provenance-aware metrics like R-precision and “only-if-evidence” scoring (KILT). (https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)

### Analogy-based
- **Vector index = “semantic library catalog.”** Instead of searching by exact words (card catalog), you search by meaning (embedding similarity).
- **Agentic RAG = “research assistant.”** The assistant can decide when it needs to consult the library again, not just once at the start.

---

## Common Misconceptions

1. **“If I add RAG, the model can’t hallucinate anymore.”**  
   - **Why wrong:** Retrieval can fail (wrong chunks, missing evidence, poor chunking), and generation can still ignore or misinterpret evidence. KILT shows downstream EM can be much higher than evidence-grounded KILT-EM, meaning answers can be “right” without correct provenance.  
   - **Correct model:** RAG *reduces* hallucination risk by providing evidence, but you must evaluate retrieval + grounding (e.g., R-precision, KILT-style “only-if-evidence”). (KILT: https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)

2. **“Chunking is just an implementation detail; embeddings will handle it.”**  
   - **Why wrong:** The chunking study finds naive fixed-size chunking can perform very poorly (Precision@1 2–3%) compared to content-aware chunking (Precision@1 24%).  
   - **Correct model:** Chunking is a primary lever for retrieval quality; embedding model improvements and chunking improvements are complementary. (https://arxiv.org/html/2603.06976)

3. **“Vector search is always cosine similarity.”**  
   - **Why wrong:** DPR explicitly uses dot product \(E_Q(q)^\top E_P(p)\) for maximum inner product search; the choice is tied to precomputability and performance.  
   - **Correct model:** Similarity depends on retriever design; dot product and cosine are both common, and the index/search method must match the similarity metric. (DPR: https://aclanthology.org/2020.emnlp-main.550.pdf)

4. **“Agent memory is just keeping the whole chat history in the context window.”**  
   - **Why wrong:** The memory taxonomy distinguishes working memory (context window) from longer-term substrates like vector stores; long-term memory requires write–manage–read operations and governance/efficiency tradeoffs.  
   - **Correct model:** Long-term memory retrieval is typically externalized (e.g., vector store) and selectively recalled into context. (https://arxiv.org/html/2603.07670v1)

5. **“If retrieval returns top‑k, the model will automatically use the best evidence.”**  
   - **Why wrong:** Retrieval ranking quality matters; KILT’s R-precision requirement (must rank a complete provenance set at the top) shows that “some relevant chunk in top‑k” is not enough for grounded scoring.  
   - **Correct model:** Treat retrieval as a component with its own metrics; consider reranking/verification and provenance requirements. (KILT source above)

---

## Worked Examples

### Example 1: Minimal DPR-style dense retrieval + context injection (toy, runnable)
This is a *didactic* mini-version of the DPR pipeline (encode → dot product → top‑k → inject). It does **not** train DPR; it just demonstrates the mechanics.

```python
import numpy as np

# --- Toy "embeddings" (pretend these came from E_Q and E_P) ---
# 3 passages, 1 query, d=4
P = np.array([
    [0.2, 0.1, 0.0, 0.7],  # passage 0
    [0.9, 0.1, 0.0, 0.0],  # passage 1
    [0.1, 0.2, 0.6, 0.1],  # passage 2
], dtype=float)

q = np.array([0.8, 0.1, 0.0, 0.1], dtype=float)

# DPR similarity is dot product: sim(q,p) = q^T p
scores = P @ q  # shape (3,)
topk = scores.argsort()[::-1][:2]

passages = [
    "Passage 0: Company refund policy: refunds within 30 days...",
    "Passage 1: Shipping times: standard 3-5 business days...",
    "Passage 2: Privacy policy: we retain logs for 90 days...",
]

retrieved = [(i, float(scores[i]), passages[i]) for i in topk]
retrieved
```

**Tutor notes (tie to sources):**
- The scoring line `scores = P @ q` is the DPR Eq. 1 dot product similarity. (https://aclanthology.org/2020.emnlp-main.550.pdf)
- In a real system, \(P\) is precomputed and indexed (FAISS), and `topk` is ANN search rather than brute force.

**Context injection template (what you actually send to the LLM):**
```text
You are an assistant. Use the provided sources to answer. Cite which passage you used.

[SOURCES]
(1) Passage 1: Shipping times: standard 3-5 business days...
(0) Passage 0: Company refund policy: refunds within 30 days...

[USER QUESTION]
Can I get a refund if I bought this 45 days ago?

[INSTRUCTIONS]
Answer using only the sources. If not in sources, say you don't know.
```

### Example 2: Agentic RAG pattern (multi-retrieval) as a tool loop (pseudo-code)
```python
def agent_loop(user_request):
    state = {"question": user_request, "notes": []}

    while True:
        action = llm_decide_next_action(state)  # "retrieve", "ask_user", "answer", etc.

        if action.type == "retrieve":
            chunks = vector_search(action.query, k=5)
            # JIT: attach only relevant instructions with tool data (Shopify pattern)
            state["notes"].append({"retrieved": chunks, "jit_instructions": action.jit})
            continue

        if action.type == "answer":
            return llm_generate_answer(state)

        if action.type == "ask_user":
            return action.question_to_user
```

**Tutor notes:**
- This matches the “agentic loop” framing in Shopify (LLM decides actions → tools → feedback → loop). (https://shopify.engineering/building-production-ready-agentic-systems)
- Stop conditions align with OpenAI’s agent loop description (end when final output tool invoked or no tool calls). (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

---

## Comparisons & Trade-offs

| Choice | What you gain | What you risk / pay | Source anchors |
|---|---|---|---|
| **Sparse retrieval (BM25)** vs **Dense retrieval (DPR)** | BM25: strong lexical match, simple infra; DPR: semantic match, big gains on many QA sets (e.g., NQ Top‑20 78.4 vs 59.1) | DPR needs embedding compute + ANN infra; BM25 can beat DPR on some datasets (SQuAD Top‑20 68.8 vs 63.2) | DPR results table (https://aclanthology.org/2020.emnlp-main.550.pdf) |
| **Dot product** vs **Cosine similarity** | Dot product works with DPR’s MIPS setup and precomputed passage vectors; cosine common in other deployed dense retrieval systems | Must align index/search with metric; normalization differences matter | DPR Eq.1 dot product; Spotify uses cosine in deployed system (https://engineering.atspotify.com/2022/03/introducing-natural-language-search-for-podcast-episodes) |
| **Naive fixed-size chunking** vs **Content-aware chunking** | Content-aware chunking can greatly improve retrieval (Precision@1 24% vs 2–3% in study) | More complex preprocessing; can increase chunk count/index size/latency | Chunking study (https://arxiv.org/html/2603.06976) |
| **One-shot RAG** vs **Agentic (iterative) RAG** | Agent can refine queries, do multi-hop retrieval, and inject JIT instructions only when needed | More tool calls → more latency/cost; needs observability/evals | Shopify JIT + agent loop (https://shopify.engineering/building-production-ready-agentic-systems); OpenAI agent architecture guide (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) |
| **Task accuracy** vs **Grounded/provenance accuracy** (KILT) | Provenance scoring increases auditability and discourages unsupported answers | Scores can drop sharply (e.g., Hotpot EM 26.97 vs KILT‑EM 3.21) | KILT (https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf) |

---

## Prerequisite Connections

- **Embeddings & similarity metrics:** Needed to understand why vector search works and what dot product/cosine mean in retrieval (DPR Eq. 1).  
- **Approximate nearest neighbor indexing (ANN/FAISS):** Needed to understand how retrieval scales to millions of chunks and why precomputing passage vectors matters. (DPR; FAISS paper)  
- **Context windows / prompting:** Needed to understand context injection limits and why “perfect context” (JIT) matters. (Shopify JIT)  
- **Tool-using agent loops:** Needed to understand how retrieval becomes a callable tool rather than a fixed pipeline step. (OpenAI practical guide; Shopify loop)

---

## Socratic Question Bank

1. **If retrieval returns irrelevant chunks, what failure mode do you expect in the final answer—and how would you detect whether the failure was retrieval vs generation?**  
   *Good answer:* separate retrieval metrics (e.g., R-precision/Recall@k) from downstream metrics; mention provenance-based evaluation (KILT).

2. **Why does DPR prefer a decomposable similarity like dot product for its pipeline? What does that enable operationally?**  
   *Good answer:* precompute passage embeddings; ANN/MIPS search; fast runtime retrieval.

3. **Suppose you increase chunk size a lot. What are two opposing effects on retrieval quality and context injection?**  
   *Good answer:* fewer chunks (smaller index) but diluted semantics; harder to fit in context; chunking study shows segmentation affects effectiveness.

4. **In an agentic workflow, when would you retrieve again instead of answering with the current evidence?**  
   *Good answer:* missing evidence, multi-hop decomposition, ambiguity; retrieval as iterative tool.

5. **What does KILT’s “only score if R-precision=1” rule force you to optimize that plain EM/F1 might not?**  
   *Good answer:* correct evidence ranking/provenance, not just plausible answers.

6. **How do in-batch negatives change the number of negative examples per question in DPR training?**  
   *Good answer:* \(B-1\) negatives per question from the batch; effectively \(B^2\) pairs.

7. **If you had to justify an answer to an auditor, what artifacts would you log from a RAG agent run?**  
   *Good answer:* retrieved chunk IDs/text, similarity scores/ranks, prompts with injected context, tool call traces; connect to provenance idea.

---

## Likely Student Questions

**Q: What’s the exact similarity function in DPR dense retrieval?**  
→ **A:** DPR uses dot product similarity: \(\mathrm{sim}(q,p)=E_Q(q)^\top E_P(p)\). This supports maximum inner product search with precomputed passage embeddings. (https://aclanthology.org/2020.emnlp-main.550.pdf)

**Q: What loss does DPR train with?**  
→ **A:** A softmax contrastive loss over one positive passage and multiple negatives:  
\(\mathcal{L}=-\log \frac{e^{\mathrm{sim}(q_i,p_i^+)}}{e^{\mathrm{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\mathrm{sim}(q_i,p_{i,j}^-)}}\). (same DPR source)

**Q: What are “in-batch negatives” and why do they help?**  
→ **A:** In DPR, for batch size \(B\), each question treats the other \(B-1\) passages in the batch as negatives; compute a \(B\times B\) similarity matrix \(S=QP^\top\) once, with diagonal positives and off-diagonal negatives. (https://aclanthology.org/2020.emnlp-main.550.pdf)

**Q: How big was DPR’s passage index and what chunk size did they use?**  
→ **A:** DPR chunks Wikipedia into fixed **100-word blocks**, yielding **21,015,324** passages (Dec 20, 2018 snapshot). (same source)

**Q: How fast is FAISS retrieval in DPR?**  
→ **A:** DPR reports FAISS retrieval around **995 questions/sec** for top‑100 retrieval. (https://aclanthology.org/2020.emnlp-main.550.pdf)

**Q: How does KILT evaluate “grounded” generation differently from normal task metrics?**  
→ **A:** KILT ties outputs to provenance and only awards downstream points if retrieval is perfect at the top: KILT scores count only when **R-precision = 1** (a complete provenance set is ranked at the top). (https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf)

**Q: Do chunking choices really matter for dense retrieval? Any numbers?**  
→ **A:** Yes—one large study reports “Paragraph Group Chunking” mean **nDCG@5 0.459**, **Precision@1 24%**, **Hit@5 59%**, while fixed-size character chunking baselines have **nDCG@5 < 0.244** and **Precision@1 2–3%**. (https://arxiv.org/html/2603.06976)

**Q: What does “Just-in-Time instructions/context injection” mean in production agents?**  
→ **A:** Shopify describes returning relevant instructions alongside tool data only when needed, aiming for “perfect context… not a token less, not a token more,” to avoid bloated prompts and improve modularity/cache efficiency. (https://shopify.engineering/building-production-ready-agentic-systems)

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — **Surface when:** student needs a systems-level mental model of LLMs as the “cognitive core” that can be augmented with tools/memory (useful before diving into agentic RAG).
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — **Surface when:** student confuses “retrieval” with “tool calling” and needs to see how tools are invoked/returned in practice.
- [Word Embedding and Word2Vec, Clearly Explained!!!](https://youtube.com/watch?v=viZrOnJclY0) — **Surface when:** student is shaky on what embeddings are and why similarity search works.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — **Surface when:** student asks where retrieval fits among planning/memory/tool use in an agent architecture.
- [LangGraph Conceptual Docs — Agentic Concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — **Surface when:** student asks how to implement an agent loop that repeatedly calls retrieval/tools.
- [OpenAI Agents SDK (Python) docs](https://openai.github.io/openai-agents-python/) — **Surface when:** student asks about practical run loops/stop conditions and how memory/tools are wired in OpenAI’s agent framework.
- [RAG original paper (Lewis et al.)](https://arxiv.org/abs/2005.11401) — **Surface when:** student wants the canonical definition of RAG and the parametric vs non-parametric memory framing.

---

## Visual Aids

![Common ways to augment an LLM: tools, retrieval, memory (LangChain).](/api/wiki-images/agent-memory/images/langchain-ai-langgraph-concepts-tools_002.png)  
**Show when:** student asks “Should I use RAG, tools, or memory?” or confuses retrieval with other augmentation methods.

![Extended LLM search pipeline for context-aware product recommendations. (Huyenchip.com)](/api/wiki-images/system-prompts/images/huyenchip-2023-04-11-llm-engineering-html_010.png)  
**Show when:** student asks how retrieval fits into a larger production pipeline (retrieve → rank/filter → generate).

![Self-Ask: LLM decomposes questions and queries external search. (Press et al. 2022)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-03-15-prompt-engineering_001.png)  
**Show when:** introducing *iterative* retrieval (agent asks sub-questions) vs one-shot RAG.

---

## Key Sources

- [Dense Passage Retrieval (DPR) — Karpukhin et al., 2020](https://aclanthology.org/2020.emnlp-main.550.pdf) — Core formulas (dot product scoring, contrastive loss), in-batch negatives, and concrete scale/throughput defaults for dense retrieval.
- [KILT — A Benchmark for Knowledge Intensive Language Tasks (provenance)](https://discovery.ucl.ac.uk/id/eprint/10129948/1/Rockta%CC%88schel_2021.naacl-main.200.pdf) — Canonical provenance-aware evaluation; retrieval metrics and “only-if-evidence” scoring.
- [Document Chunking Strategies for Dense Retrieval (systematic study)](https://arxiv.org/html/2603.06976) — Empirical evidence that chunking is a major lever; concrete nDCG/Precision@1 comparisons.
- [Shopify: Building production-ready agentic systems](https://shopify.engineering/building-production-ready-agentic-systems) — Practical agent loop + JIT context injection rationale to prevent prompt bloat/tool overload.
- [OpenAI — A practical guide to building agents (PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Operational definition of agents, tool taxonomy, and loop/exit-condition framing used in production.