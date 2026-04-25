# Card: Lost-in-the-Middle (Long-Context Utilization Curves)
**Source:** https://cs.stanford.edu/~nfliu/papers/lost-in-the-middle.arxiv2023.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Canonical “lost-in-the-middle” U-shaped accuracy curves vs. position of relevant evidence in long contexts; setups for multi-doc QA + synthetic key–value retrieval.

## Key Content
- **Core finding (Fig. 1, Fig. 5, Fig. 7):** Accuracy is **highest when relevant info is at the beginning (primacy) or end (recency)** of the context and **drops in the middle** (U-shaped “lost-in-the-middle” curve), even for explicitly long-context models.
- **Multi-document QA task (Sec. 2.1):**
  - Input: question + **k documents**, with **exactly 1 answer-containing doc** and **k−1 distractors**.
  - Data: **NaturalQuestions-Open**, **2655** queries where long answer is a paragraph.
  - Docs: Wikipedia chunks **≤100 tokens**. Distractors retrieved by **Contriever (MS-MARCO fine-tuned)**; presented in **decreasing relevance**.
  - Controls: vary **context length** by changing total docs (**10/20/30**; ~**2K/4K/6K tokens**), and vary **answer-doc position** by reordering docs.
  - Metric: **accuracy** = any gold answer string appears in output.
- **Closed-book vs oracle baselines (Table 1, multi-doc QA accuracy):**
  - LongChat-13B (16K): **35.0%** closed-book, **83.4%** oracle
  - MPT-30B-Instruct: **31.5%**, **81.9%**
  - GPT-3.5-Turbo: **56.1%**, **88.3%**
  - GPT-3.5-Turbo (16K): **56.0%**, **88.6%**
  - Claude-1.3: **48.3%**, **76.1%**
  - Claude-1.3 (100K): **48.2%**, **76.4%**
  - Notable comparison (Sec. 2.3): GPT-3.5-Turbo **worst-case (middle)** in 20/30-doc settings can be **< closed-book 56.1%**.
- **Extended context ≠ better utilization (Sec. 2.3):** When prompts fit both windows, **GPT-3.5 (4K) vs GPT-3.5 (16K)** curves are **nearly identical** (Fig. 5); similarly **Claude-1.3 vs Claude-1.3-100K**.
- **Synthetic key–value retrieval (Sec. 3):**
  - Input: JSON with **k UUID→UUID pairs** + query key; output associated value (Fig. 6).
  - k tested: **75/140/300 pairs** (~**4K/8K/16K tokens**), **500 examples each**.
  - Result: some models (notably **Claude-1.3 / 100K**) near-perfect; others show **middle-position degradation** (Fig. 7).
- **Query-aware contextualization (Sec. 4.2):**
  - Put query **before and after** data.
  - Effect: **dramatically improves key–value retrieval** (e.g., GPT-3.5-Turbo-16K becomes **perfect** at **300 pairs**; without it, **worst-case 45.6%**), but **minimal improvement** for multi-doc QA (Fig. 9).
- **Architecture effect (Sec. 4.1):** Encoder–decoder (Flan-UL2, Flan-T5-XXL) is **robust within training-time lengths** (Flan-UL2: **1.9%** best–worst gap within **2048 tokens**), but shows U-shape **beyond** training lengths (Fig. 8).
- **More retrieved docs saturate (Sec. 5, Fig. 11):** In open-domain QA, reader accuracy saturates well before retriever recall; using **50 vs 20 docs** yields only **~+1.5% (GPT-3.5)** and **~+1% (Claude-1.3)**.

## When to surface
Use when students ask whether “long context windows” guarantee using all tokens, why models miss evidence in the middle, or how retrieval depth / document ordering affects QA accuracy.