# Card: MMLU-CF (contamination-free MMLU) — methodology + results
**Source:** https://aclanthology.org/2025.acl-long.656.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Contamination-detection methodology + contamination-free evaluation results (tables) incl. sampling/settings

## Key Content
- **Problem framing:** contamination in public MCQ benchmarks (MMLU) can be **unintentional** (train-data overlap) or **deliberate** (benchmark added to training; models regurgitate exact choices). Example shown where models output **identical MMLU choices** from question-only prompt (Fig. 1).
- **Dataset scale & split (Sec. 3):** MMLU-CF = **20,000 MCQs** across **14 fields**, sourced from **200+ billion webpages**; final split **10k closed-source test** + **10k open-source validation** to deter deliberate contamination while enabling transparency.
- **Construction pipeline (Fig. 3):**
  1) **MCQ collection:** extract **2.7M** MCQs from **3000+ domains**.  
  2) **Cleaning:** length 10–512 chars; require ≥4 choices; normalize labels to **A/B/C/D**; English-only; dedup → **1.66M**.  
  3) **Difficulty sampling:** GPT-4o rates difficulty **0–9** (prompt Table 7); sample ~normal centered at **6**; keep balanced disciplines → **50k**.  
  4) **LLM checking:** GPT-4o/Gemini/Claude rate quality (1–5); keep avg **>4**; safety filters (hate/sex/self-harm/violence); redundancy detection inspired by Decontaminator.  
  5) **Contamination-free processing (Sec. 3.2, Fig. 5):**  
     - Rule 1 **Rephrase question** (GPT-4o)  
     - Rule 2 **Shuffle choices** (special-case “All/None of the above”)  
     - Rule 3 **50%**: replace one choice with **“None of the other choices”** (skip if last choice is All/None above)
- **Evaluation defaults (Sec. 4, Appx A.6, Table 5):** 0-shot & **5-shot**, **no CoT** (except marked). Prompt: “Answer by replying A, B, C or D” (Table 6). Temperatures/max tokens: GPT-4o **0.7/2048**, GPT-3.5 **0.7/2048**, DeepSeek-R1 **0.6/32768**, DeepSeek-V3 **0.7/8192**, Qwen2.5 **0.7/4096**, others **0.7/1024**.
- **Key empirical results (5-shot test, Table 1):** large drops vs MMLU and rank reshuffles. Examples:  
  - **OpenAI o1:** 92.3 → **80.3** (−12.0)  
  - **GPT-4o:** 88.0 → **73.4** (−14.6)  
  - **Qwen2-72B-instruct:** 82.3 → **63.7** (−18.6), rank ↓7  
- **Rule ablation (Table 2, 5-shot):** applying all 3 rules drops accuracy:  
  - On **MMLU:** GPT-4o 88.0 → **79.8** (−8.2)  
  - On **MMLU-CF:** GPT-4o 79.8 → **73.4** (−6.4)  
  Larger drop on MMLU ⇒ more contamination.
- **Contamination detection metric (Sec. 4.5, Fig. 6):** “match rate” of model outputs to original MMLU choices on 1k samples/40 models: ~**10%** of models show **1–5%** match on MMLU; with decontam rules **97.5%** of models <1% match; on **MMLU-CF 100%** of models **<0.2%** match.
- **Validation–test gap as contamination monitor (Appx A.3, Table 4):** define **Δ = |score_val − score_test|**; before validation release: ~**60%** of Δ <0.5 and **96%** <1.0 (5-shot), suggesting similar difficulty; future Δ growth indicates validation contamination.

## When to surface
Use when students ask how to **detect/mitigate benchmark contamination**, why **closed test sets** matter, or how **MMLU scores/rankings change** under decontamination and controlled evaluation settings.