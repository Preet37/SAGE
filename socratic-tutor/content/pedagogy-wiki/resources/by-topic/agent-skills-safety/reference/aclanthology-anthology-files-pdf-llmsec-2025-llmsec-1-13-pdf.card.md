# Card: CAPTURE benchmark + robustness scoring for prompt-injection guardrails
**Source:** https://aclanthology.org/anthology-files/pdf/llmsec/2025.llmsec-1.13.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Full evaluation protocol (context-aware test generation + scoring) and published FNR/FPR results

## Key Content
- **Attack construction (Section 2):** Context-aware prompt injection uses 3-part structure from Liu et al. (2023): **Framework (F)** = normal in-domain request; **Separator (S)** = context-breaking cue to override F; **Disruptor (D)** = malicious instruction. CAPTURE systematically varies **F, S, D**.
- **Two generation modes (Figure 1):**
  - **MALICIOUS-GEN:** GPT-4o decomposes existing attacks into **S and D** (Fig. 3), then rewrites **S → S′** to be more evasive (Fig. 4), then embeds **S′ + D** into in-domain **F**. Output sizes: **1274 train**, **641 test/val** adversarial prompts.
  - **SAFE-GEN (over-defense test):** Uses trigger words from **NotInject** inside **S**, with **safe D** (Fig. 2). Output sizes: **339 train**, **171 test/val** benign prompts.
- **Domains (Section 2.1):** 6 domains: Shopping, Covid, Movies, Stock, Travel, Python Code. Base split per domain: **30 train / 15 test / 15 val**, expanded via GPT-4o to **100 examples per domain per split**.
- **Metrics (Tables 2–3):** Report **False Negative Rate (FNR%)** on MALICIOUS-GEN and **False Positive Rate (FPR%)** on SAFE-GEN.
- **Key empirical results (Tables 2–3):**
  - **PromptGuard:** **FNR 0%** across domains, but **FPR ~100%** (e.g., Stock/Movies/Travel/Covid/Shopping all **100%**, Python **24.12%**).
  - **InjecGuard:** extremely high **FNR** (e.g., Movies **100%**, Stock **99.84%**) and **FPR ~99%** (Python **0.88%** exception).
  - **Fmops:** **FNR 100%** across domains; **FPR 0%** (misleading due to total miss).
  - **GPT-4o baseline:** low FNR (**7.33–16.38%**) and low FPR (**2.64–13.15%**).
  - **CaptureGuard (trained on CAPTURE data):** near-zero on tested domains—**FNR 0.00–0.15%**, **FPR 0.00–2.05%** (Stock/Movies/Python).
- **CaptureGuard training defaults (Section 2.4, Table 5):** DeBERTaV3-base; **batch 32**, **LR 2e-5**, **max seq len 64**, **Adam**, **1 epoch**, **threshold 0.5**. Trained per-domain (Python/Movies/Stocks) on CAPTURE + InjecGuard’s **14 benign + 12 malicious** datasets.
- **External benchmark accuracies (Table 6):** CaptureGuard: **NotInject(avg) 79.04%**, **WildGuard 75.00%**, **BIPIA(Injection) 54.77%** (vs InjecGuard **87.31/76.11/68.34**, GPT-4o **86.62/84.24/66.00**).

## When to surface
Use when students ask how to **generate realistic context-aware prompt-injection tests**, how to **score guardrails (FNR/FPR)**, or want **published comparisons** showing over-defense vs missed attacks and the effect of **training on CAPTURE-generated data**.