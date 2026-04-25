# Card: SELF-REFINE (Generate → Feedback → Refine loop)
**Source:** https://arxiv.org/pdf/2303.17651.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Self-Refine algorithm loop + equations + stopping criterion + prompt roles

## Key Content
- **Core idea (Sec. 1–2):** Use a *single* LLM \(M\) as generator, feedback provider, and refiner; no supervised training, no RL, no extra models.
- **Algorithm 1 (SELF-REFINE loop):**
  1) **Initial generation (Eq. 1):**  
     \[
     y_0 = M(p_{\text{gen}} \parallel x)
     \]
  2) For iterations \(t=0,1,\dots\):  
     **Feedback (Eq. 2):**  
     \[
     fb_t = M(p_{\text{fb}} \parallel x \parallel y_t)
     \]
     **Stop check:** break if \(stop(fb_t, t)\) is true (either max-iteration \(t\) or a stop indicator/score extracted from feedback; Sec. 2).  
     **Refine (Eq. 3 / instantiated as Eq. 4 with history):**  
     \[
     y_{t+1} = M(p_{\text{refine}} \parallel x \parallel y_t \parallel fb_t)
     \]
     \[
     y_{t+1} = M(p_{\text{refine}} \parallel x \parallel y_0 \parallel fb_0 \parallel \dots \parallel y_t \parallel fb_t)
     \]
  - **Notation:** \(x\)=input; \(y_t\)=draft at iteration \(t\); \(fb_t\)=feedback; \(\parallel\)=concatenation; prompts \(p_{\text{gen}}, p_{\text{fb}}, p_{\text{refine}}\) are task-specific few-shot templates.
- **Feedback design rationale (Sec. 2, Sec. 4):** Prompt feedback to be **actionable** (concrete improvement action) and **specific** (points to concrete phrases/issues). Generic/no feedback reduces performance (Table 2).
- **Defaults/parameters (Sec. 3.1):** Iterate until criterion met, **max 4 iterations**; greedy decoding with **temperature 0.7**.
- **Key empirical results (Table 1):** SELF-REFINE improves base LLMs across tasks (absolute gains shown):
  - Dialogue Response (GPT-4): **25.4 → 74.6** (**+49.2**)
  - Constrained Generation (ChatGPT): **44.0 → 67.0** (**+23.0**)
  - Code Optimization (GPT-4): **27.3 → 36.0** (**+8.7**)
  - Sentiment Reversal (ChatGPT): **11.4 → 43.2** (**+31.8**)
- **Iteration gains (Fig. 4):** Example average scores improve with iterations (diminishing returns): Constrained Gen **29.0 (y0) → 49.7 (y3)**.

## When to surface
Use when students ask how to implement an **agentic self-correction loop** (reflection/self-critique) with **explicit equations**, **stop conditions**, and **prompt roles** for iterative refinement.