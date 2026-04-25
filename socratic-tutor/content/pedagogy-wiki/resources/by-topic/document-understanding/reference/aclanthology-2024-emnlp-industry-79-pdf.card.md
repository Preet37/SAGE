# Card: LOFI pipeline (Language/OCR/Form Independent) for SER in LRL documents
**Source:** https://aclanthology.org/2024.emnlp-industry.79.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Industry-oriented experimental results + practical evaluation for KIE/SER generalization (Korean/Japanese), robustness, and deployment constraints

## Key Content
- **Problem framing (Intro/§3):** Industrial SER on visually rich documents faces 3 dependencies: **Language** (LRL data/model scarcity), **OCR** (word/line/char-level box granularity varies by language/OCR), **Form** (reading order unreliable under rotation/distortion).
- **LOFI pipeline steps (§3):**
  1) **OCR & text alignment:** OCR → (text, boxes); sort boxes **Top-Left→Bottom-Right** (Algorithm 1; row grouping by height tolerance ϵ, then left-to-right).  
  2) **Token-level box split:** convert any OCR box granularity to **token-level boxes** (Algorithm 2): tokenize text; classify characters (number/symbol/upper/lower etc.); apply **predefined size ratios** per char type to proportionally split/adjust original OCR box into token boxes.  
  3) **Model inference:** (token, token-box) → **LiLT** encoder; **SPADE decoder** outputs **ITC** (initial token entity type) + **STC** (token-to-token connectivity) to recover entities despite wrong reading order.  
  4) Combine outputs → final SER.
- **Design rationale:**  
  - **LiLT** chosen because layout encoder is relatively **language-independent**; swap **text encoder PLM** per language (Korean/Japanese) without extra pretraining (§2.1/§3).  
  - **SPADE** used to reduce reliance on correct 1D reading order under distortions (§2.3/§3).
- **Key empirical results (entity-level F1, §5):**
  - **Korean medical bills:** LayoutXLM 95.58%; **LOFI-ko 95.64%** with **116M params** vs LayoutXLM **369M** (~68.6% fewer).  
  - **Japanese receipts:** LayoutXLM 94.35%; **LOFI-mul† (InfoXLM+lilt-only-base) 94.60%** (284M, no image embedding); LOFI-ja 93.78%.
  - **Open datasets (§5.2):** FUNSD—BROS 83.05% (best), LOFI-en 78.99%; CORD—LayoutLMv3 96.80% (best), LOFI-en 96.39%.
- **Ablations (§6):**
  - **Training data need:** “Satisfactory” SER typically needs **~300–400 docs**; **<200 docs → ≥5% F1 drop** vs full set.  
  - **Pretrained layout encoder helps:** Pretrained vs initialized layout encoder F1: **0.9564 vs 0.9259** (Ko), **0.9290 vs 0.9035** (Ja).
- **Defaults/hyperparams (Appendix Table 5):** max length **512**; epochs **50** (Ko bills), **100** (Ja receipts/FUNSD/CORD); LR **1e-5** (Ko), **5e-5** (Ja/FUNSD/CORD); batch **24** (Ko), **32** (Ja), **4** (FUNSD), **16** (CORD). Base arch: hidden **768**, heads **12**, FFN **3072**, layers **12**.

## When to surface
Use for questions about **evaluating SER/KIE pipelines under OCR variability, LRL transfer, reading-order robustness**, and for **concrete F1/parameter tradeoffs** between LiLT+SPADE (text+layout only) vs multimodal LayoutXLM/LayoutLM variants.