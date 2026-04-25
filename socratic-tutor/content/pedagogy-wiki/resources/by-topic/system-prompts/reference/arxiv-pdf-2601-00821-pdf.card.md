# Card: CogCanvas (verbatim-grounded artifacts for long conversations)
**Source:** https://www.arxiv.org/pdf/2601.00821.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** Concrete architecture pattern for long-conversation management: extract *verbatim-grounded* artifacts (avoid summary drift), store in a temporal-aware graph, retrieve/inject adaptively; includes empirical comparisons vs truncation/summarization/RAG/GraphRAG.

## Key Content
- **Problem & rationale (Intro):** Summarization is *lossy* and causes “recursive information decay” (iterative abstraction drops nuance). Example constraint: “use type hints **everywhere**” becomes “prefers type hints.” Controlled benchmark exact match: **Summarization 19.0% vs verbatim-grounded retrieval 93.0%**.
- **Artifact data structure (Section 3.1, Eq. 1):** `CanvasObject = (type, content, grounding_quote, source, embedding, turn_index, confidence)` where `type ∈ {Decision, Todo, KeyFact, Reminder, Insight}`; **grounding_quote is verbatim** for traceability/hallucination tolerance.
- **Extraction workflow (Section 3.2, Eq. 2):** Per turn `t`, call an extraction LLM using prior objects to avoid duplicates. **Two-pass “gleaning”**: 2nd pass targets pronouns/omitted subjects/implicit causality/temporal expressions; merge+dedupe.
- **Graph construction (Section 3.2, Eq. 3–4):** Embed each object with sentence encoder; create edges via cosine similarity plus **keyword overlap + temporal heuristics** (reference edges; causal edges for type pairs with similarity+temporal constraints; extra temporal-heuristic causal edges for recent KeyFacts/Reminders influencing later Decisions).
- **Adaptive injection (Section 3.3, Eq. 5):** Hybrid retrieval = semantic + lexical keyword score; **adaptive top‑k by query complexity** (multi-hop/temporal get larger k). Two-stage retrieval: coarse top‑20 → **BGE reranker** → greedy pack into token budget.
- **Empirical results:**
  - Controlled (Table 2): **CogCanvas Recall 97.5%, Exact 93.0%**; RAG(k=10) 93.5/89.5; GraphRAG 83.5/70.0; Summarization 19.0/14.0; Truncation (recent 5 turns) poor.
  - Multi-hop benchmark (Table 3): **CogCanvas Pass 81.0%, KW 90.2%, Causal 87.5%, Impact 92.6%**; RAG Pass 55.5%; GraphRAG 40.0%; Summarization 0.0%.
  - LoCoMo real-world (Table 4): **CogCanvas 32.4% overall vs RAG 24.6% (+7.8pp)**; **Temporal 32.7% vs 12.1% (+20.6pp)**; Multi-hop 41.7% vs 40.6 (+1.1pp); 1-hop 26.6 vs 24.6 (+2.0pp).
- **Ablation (Table 5):** Biggest contributor **reranking** (remove → **32.4%→20.9%, −11.5pp**). Remove graph expansion: 32.4→25.8 (−6.6pp). Remove gleaning: 32.4→30.7 (−1.7pp).
- **Defaults/hyperparams (Appendix A/B):** Extraction model **GPT‑4o‑mini**, embeddings **text-embedding-3-small**; retrieval **Top‑15**, max **2000 tokens**; temperatures **0.1 (extract)**, **0.0 (generate)**. Token cost per query (Appendix B): **CogCanvas ~1,250 tokens** vs RAG(top‑5) 1,500; Summ 2,000; GraphRAG 3,000; Full context 10,000.

## When to surface
Use when students ask how to manage long chat history (trimming vs summarization vs retrieval), how to prevent summary drift, or how to design a deployable memory pipeline with measurable gains (especially temporal/multi-hop questions).