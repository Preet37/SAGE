# Card: CAPTURE context-aware prompt-injection testing + robustness results
**Source:** https://aclanthology.org/2025.llmsec-1.13.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Context-aware prompt-injection testing procedure (generation + evaluation) with empirical FNR/FPR results for guardrails and a trained improved detector (CaptureGuard).

## Key Content
- **Attack structure (Section 2):** prompts decomposed into **Framework (F)** = normal in-domain request; **Separator (S / refined S′)** = context-break to redirect; **Disruptor (D)** = injected instruction (malicious or safe). Final prompt = embed **S′ + D** inside domain **F**.
- **Dataset generation pipeline (Fig. 1, Sec. 2):**
  - **Contextual domain data (Sec. 2.1):** 6 domains (Shopping, Covid, Movies, Stock, Travel, Python Code). Start with **30 train / 15 test / 15 val** questions per domain, expanded via **GPT-4o** to **100 examples per domain per split**.
  - **MALICIOUS-GEN (Sec. 2.2):** GPT-4o decomposes existing attacks into **S and D**; augment **D** with strategies (Table 7); refine **S → S′** to evade trigger-word detection; yields **1274 train** and **641 test/val** attacks.
  - **SAFE-GEN (Sec. 2.3):** build benign prompts to test over-defense: **S** uses trigger words from **NotInject**; **D** is safe in-domain instruction; yields **339 train** and **171 test/val** benign samples.
- **Evaluation metrics (Sec. 3):** **FNR** on MALICIOUS-GEN (missed attacks) and **FPR** on SAFE-GEN (benign flagged).
- **Empirical results (Tables 2–3):**
  - **PromptGuard:** **FNR 0%** across domains but **FPR ~100%** (e.g., Stock/Movies **100%**, Python **24.12%**).
  - **InjecGuard:** extremely high **FNR** (Stock **99.84%**, Movies **100%**, Python **35.65%**) and **FPR** (Stock/Movies **99.12%**, Python **0.88%**).
  - **Fmops:** **FNR 100%** with **FPR 0%** (fails by missing all attacks).
  - **GPT-4o detector baseline:** low FNR/FPR (e.g., Stock **16.38/5.81**, Movies **7.48/9.35**, Python **13.72/2.64**).
  - **CaptureGuard (trained on CAPTURE + InjecGuard datasets):** near-zero errors: **FNR 0.00–0.15%**, **FPR 0.00–2.05%** (Table 2).
- **CaptureGuard training defaults (Table 5):** DeBERTaV3-base; batch **32**; LR **2e-5**; max length **64**; Adam; **1 epoch**; threshold **0.5**.

## When to surface
Use when students ask how to *systematically test* prompt-injection defenses in realistic app contexts, or want *concrete FNR/FPR comparisons* showing over-defense vs missed attacks and how context-aware data improves robustness.