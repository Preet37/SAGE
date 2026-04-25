# Card: LoCoMo — Very Long-Term Conversational Memory Benchmark
**Source:** https://aclanthology.org/2024.acl-long.747.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** LoCoMo construction (multi-session, ~600 turns) + tasks/metrics for evaluating very long-term conversational memory (QA, event summarization, multimodal dialog gen)

## Key Content
- **Dataset scale (Table 1 / Conclusion):** LoCoMo has **10 conversations**, each **~588 turns** and **~16,618 tokens** on average, spanning **~27.2 sessions** (up to **32 sessions**) over **a few months**; **multimodal** (image sharing). Compared to MSC: **16×** longer in tokens, **10×** more turns, **5×** more sessions.
- **Generation pipeline (Section 3):**
  - **Persona (Sec 3.1):** start from MSC persona seed (**4–5 sentences**) → expand with **gpt-3.5-turbo**.
  - **Temporal event graph (Sec 3.2):** per speaker graph **G** with up to **25 events** over **6–12 months**; iterative generation in batches **k=3**; includes causal links **l=(e_i,e_j)** and event times **t_i**.
  - **Agent memory (Sec 3.3):** after each session *k*, produce summary **w_k** conditioned on session history **h_k** and prior summary **w_{k−1}**; store turn-level **observations o_{k,j}** in long-term memory; responses conditioned on persona **p**, current session history, retrieved observations, and events between sessions **{e ∈ G | t_s^k < t_e < t_s^{k+1}}**. Image captions also stored as memory.
  - **Human editing (Sec 3.4):** annotators edited **~15%** of turns; removed/substituted **~19%** images.
- **Evaluation tasks (Section 4):**
  - **QA (Sec 4.1):** 5 types: single-hop, multi-hop, temporal, open-domain knowledge, adversarial (unanswerable). Metric: **token-level F1** after normalization; answers drawn directly from dialogue; QA annotated with **turn IDs**; for RAG report **retrieval recall@k**.
  - **Event summarization (Sec 4.2):** summarize events in timeframe; compare to event graph **G** using **FactScore** (atomic facts) → **precision/recall/F1**.
  - **Multimodal dialog gen (Sec 4.3):** evaluate alignment with ground-truth using **MMRelevance** (+ standard NLG metrics).
- **Key empirical results (Tables 2–4):**
  - **Human QA overall F1:** **87.9** (single-hop **95.1**, temporal **92.6**).
  - **Best long-context QA:** **gpt-4-turbo 128K overall 51.6** (single-hop **72.3**, multi-hop **51.5**, temporal **51.4**, adversarial **15.7**).
  - **Long-context hallucination vulnerability:** adversarial drops sharply (e.g., **claude-3-sonnet adversarial 2.5**, **gemini-1.0-pro 5.2**).
  - **Event summarization best:** **gpt-4-turbo FactScore F1 48.9** (precision **51.9**, recall **46.5**).
  - **RAG finding (Sec 6.1/Table 3):** storing history as **observations (assertions)** improves QA vs raw dialog; too many retrieved items hurts (signal-to-noise).

## When to surface
Use when students ask how to **evaluate** or **benchmark** long-term conversational memory across many sessions, or how **summaries/observations/RAG vs long context windows** perform empirically on recall, temporal reasoning, and hallucination resistance.