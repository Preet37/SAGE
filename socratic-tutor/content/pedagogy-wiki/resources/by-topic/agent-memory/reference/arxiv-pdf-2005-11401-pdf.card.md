# Card: RAG = retrieval + generation with top‑K document marginalization
**Source:** https://arxiv.org/pdf/2005.11401.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** RAG marginalization over retrieved docs (top‑k), joint retriever+generator likelihood objective, rationale for retrieval-then-generate

## Key Content
- **Model components (Sec. 2):**  
  - Retriever \(p_\eta(z\mid x)\): returns a (top‑\(K\) truncated) distribution over passages \(z\) given input/query \(x\) (initialized from DPR).  
  - Generator \(p_\theta(y\mid x,z)\): seq2seq (BART-large, ~400M params) generating output \(y\) conditioned on \(x\) and retrieved passage \(z\) (implemented by concatenating \(x\) and \(z\)).
- **Latent-document marginalization (Sec. 2.1):** retrieved passage \(z\) is a latent variable; approximate marginalization with top‑\(K\) docs.
  - **RAG-Sequence (same doc for whole output):**  
    \[
    p(y\mid x)\approx \sum_{z\in \text{top-}K} p_\eta(z\mid x)\; p_\theta(y\mid x,z)
    \]
  - **RAG-Token (doc may vary per token):**  
    \[
    p(y\mid x)=\prod_{i} \sum_{z\in \text{top-}K} p_\eta(z\mid x)\; p_\theta(y_i\mid x,z,y_{<i})
    \]
- **Training objective (Sec. 2.4):** minimize **negative marginal log-likelihood** over paired data \((x,y)\): \(-\log p(y\mid x)\). Jointly learn retriever + generator **without retrieval supervision**; keep **document encoder/index fixed**, fine-tune **query encoder + BART**.
- **Retriever details (Sec. 2.2–3):** DPR bi-encoder with inner product scoring; retrieval via MIPS (FAISS). Wikipedia index: **Dec 2018 dump**, split into **100-word chunks**, ~**21M** documents.
- **Defaults/parameters (Sec. 3):** retrieve **top \(K=5\)** during training; **\(K=10\)** at test (chosen on dev). Retrieving more docs: monotonic gains for RAG-Seq; RAG-Tok peaks around **10**.
- **Empirical results (Tables 2/6):**  
  - Jeopardy QGen Q-BLEU-1: **BART 19.7**, **RAG-Token 22.2**, **RAG-Seq 21.4**.  
  - FEVER label accuracy: **BART 64.0/81.1** (3-way/2-way), **RAG-Token 72.5/89.5**.  
  - Human eval Jeopardy factuality: **RAG better 42.7%** vs **BART better 7.1%**.
- **Design rationale (Intro/Results):** retrieval augments parametric memory to reduce hallucinations, improve factuality/specificity, provide inspectable evidence, and enable **knowledge updates by swapping the index** (no retraining).

## When to surface
Use when students ask how retrieval-augmented “long-term memory” is formalized (latent docs, top‑\(K\) marginalization), how retriever+generator are trained jointly, or why retrieval enables updating/grounding beyond in-context (short-term) memory.