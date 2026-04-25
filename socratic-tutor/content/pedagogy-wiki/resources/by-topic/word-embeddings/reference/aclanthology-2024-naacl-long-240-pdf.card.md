# Card: Contextual Embeddings for Lexical Semantic Change (LSC) — Controlled Comparison
**Source:** https://aclanthology.org/2024.naacl-long.240.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** Controlled, multi-language comparison of contextual embedding choices + concrete evaluation protocols and reported numbers.

## Key Content
- **LSC framework (i–iii)** (Intro/§2): (i) semantic proximity judgments for usage pairs; (ii) induce senses by clustering a Diachronic Word Usage Graph (DWUG); (iii) quantify change from time-specific sense distributions.
- **Embeddings setup** (§3): For each target word, collect contextual embeddings for all usages in two periods:  
  Φ₁ = {a₁…aₙ} (time t₁), Φ₂ = {b₁…bₘ} (time t₂). Default: **no extra fine-tuning**, use **last layer (12th)** embeddings; average subword embeddings when token splits.
- **GCD (Graded Change Detection) metrics**: evaluate by **Spearman correlation** between predicted change scores and gold rankings (§2, §4).
- **Form-based change scores** (§4.1):  
  - **PRT** (Eq.1): PRT(Φ₁,Φ₂)= 1 − cosine(μ₁, μ₂), where μ₁, μ₂ are mean (prototype) embeddings in each period.  
  - **APD** (Eq.2): APD(Φ₁,Φ₂)= (1/(|Φ₁||Φ₂|)) Σ_{a∈Φ₁,b∈Φ₂} d(a,b), with d = cosine distance.
- **Sense-based** (§4.2): **AP+JSD** (cluster Φ₁∪Φ₂ with Affinity Propagation; compute JSD between cluster distributions p₁,p₂; Eq.3). **WiDiD**: cluster Φ₁ and Φ₂ separately with APP; compute **APDP = APD(Ψ₁,Ψ₂)** over sense prototypes (Eq.4; uses **Canberra distance** per footnote).
- **Key empirical results (Table 1/2)**:  
  - Best overall GCD: **XL-LEXEME + APD weighted avg Spearman = .751** (8 languages). Leaderboard: **APD > PRT > WiDiD > AP+JSD**.  
  - Computational annotators (Table 2): WiC avg Spearman **BERT .358, mBERT .301, XLM-R .272, XL-LEXEME .568**; EN WiC: **XL-LEXEME .626 vs GPT-4 .606**, human agreement (Krippendorff α) **.633**.  
  - GCD as annotators avg Spearman: **BERT .422, mBERT .357, XLM-R .324, XL-LEXEME .754**; EN GCD: **XL-LEXEME .801, GPT-4 .818**.
- **Layer choice finding** (§4.3): earlier/middle layers often better; best results typically **layers 8–10**; **no consistent gain** from aggregating last 4 layers.

## When to surface
Use when students ask how to *measure semantic change with contextual embeddings*, compare **APD vs prototype vs clustering**, or want **controlled benchmark numbers** (XL-LEXEME, BERT/mBERT/XLM-R, GPT-4) and **evaluation protocol details** (WiC/WSI/GCD).