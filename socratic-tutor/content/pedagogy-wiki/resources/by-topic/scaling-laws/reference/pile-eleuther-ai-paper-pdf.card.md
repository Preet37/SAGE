# Card: The Pile — mixture composition + preprocessing/eval metrics
**Source:** https://pile.eleuther.ai/paper.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Dataset construction pipeline details: component datasets/mixture, preprocessing/normalization, filtering/dedup

## Key Content
- **Dataset goal/size:** The Pile is an **825.18 GiB** English-focused corpus built from **22** component datasets to improve cross-domain generalization vs Common Crawl-only training (Intro, Sec. 2).
- **Mixture weighting (“epochs”):** Higher-quality components are upsampled; a “full epoch over the Pile” may include multiple passes over some components (Sec. 2, Table 1). Examples (raw → epochs → effective):
  - **Pile-CC:** 227.12 GiB, **1.0×**, effective 227.12 GiB (**18.11%** weight)
  - **PubMed Central:** 90.27 GiB, **2.0×**, effective 180.55 GiB (**14.40%**)
  - **Books3:** 100.96 GiB, **1.5×**, effective 151.44 GiB (**12.07%**)
  - **Wikipedia (en):** 6.38 GiB, **3.0×**, effective 19.13 GiB (**1.53%**)
  - Total **effective size:** **1254.20 GiB**; mean doc size **5.91 KiB**.
- **Common Crawl pipeline (Pile-CC):** Extract from **raw HTTP/HTML (WARC)** using **jusText** (not WET text) for higher-quality extraction (Sec. 2.1).
- **Splits:** Validation and test are **0.1% each**, sampled uniformly at random; dedup efforts exist but duplicates across splits may remain (Sec. 3.1).
- **Metric (BPB) (Sec. 3.1):**  
  **BPB = (L_T / L_B) · log₂(e^ℓ) = (L_T / L_B) · ℓ / ln(2)**  
  where **ℓ** = NLL loss, **L_T** = token length, **L_B** = UTF-8 byte length. For GPT-2 tokenizer on Pile: **L_T/L_B = 0.29335 tokens/byte**.
- **Scaling law fit (GPT-3 family on Pile, Sec. 3.2):** best-fit line coefficient **−0.1674**, intercept **2.5516** (perplexity/BPB scaling vs model size).
- **Size-controlled training comparison (Sec. 4.1–4.2, Table 3):** decontaminate eval sets via **13-gram overlap filtering** (Brown et al. 2020) and **downsample to ~40GB**. Results: Pile beats CC-100 and Raw CC on Pile BPB and WikiText PPL (e.g., **Pile test BPB 0.9433** vs **CC-100 1.3293** vs **Raw CC 1.1275**).

## When to surface
Use when students ask how large LM pretraining datasets are *constructed/weighted*, how Common Crawl is *extracted/filtered*, or how to compare models with *tokenizer-invariant* metrics (BPB) and scaling-law fits.