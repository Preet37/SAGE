# Card: CMMLU (Chinese MMLU-style benchmark) — construction + eval protocol + results
**Source:** https://aclanthology.org/2024.findings-acl.671.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark construction + leaderboard-style results/ablations (splits, protocol, numbers)

## Key Content
- **Benchmark design (Section 3):**
  - **67 subjects**, **4-choice single-answer MCQ** format.
  - **Total questions:** reported as **11,528** (text) / **11,582 test-set** (Table 1).  
  - **Per-subject split:** **5-question few-shot dev** + **>100-question test**; each subject **min 105** questions (Table 1).
  - **Supercategories:** **17 STEM (2,531 Q)**, **13 Humanities (2,489 Q)**, **22 Social Science (3,652 Q)**, **15 Other (2,910 Q)**; **China-specific:** **15 tasks (2,572 Q)** (Table 1).
  - **Data collection:** 4 annotators; **50 CNY/hour**; ~**250 hours**; **>80% from PDFs (OCR)** to reduce training contamination; estimated **~2% label noise**.
  - **Overlap check vs CEval/M3KE:** exact-string match after sorting choices + punctuation removal → **74 overlaps with CEval**, **158 with M3KE** (~**1%** of CMMLU).

- **Evaluation protocol (Section 4):**
  - **Closed models:** *free generation* + regex extract option.
  - **Open models:** *next-token prediction* over tokens **{A,B,C,D}** using next-token logits (preferred vs perplexity; Appendix G).
  - **Prompt:** “以下是关于[主题]的单项选择题，请直接给出正确答案的选项…答案是：”; **0-shot** and **up to 5-shot**; if context too long, **drop longest examples** by sub-token count.

- **Main 5-shot results (Table 3; macro-average over subjects):**
  - **GPT-4:** **70.95%** overall (STEM **65.23**, Humanities **72.11**, Social **72.06**, Other **74.79**, China-spec **66.12**).
  - **ChatGPT:** **55.51%** overall.
  - Best open multilingual: **LLaMA2-70B 53.21%**; best Chinese: **Baichuan2-13B 61.92%** (beats ChatGPT).

- **Ablations (Section 4.2):**
  - **Chain-of-thought prompt often doesn’t help**; e.g., **Baichuan2-13B-Chat overall 58.77 (DA) → 52.82 (COT)** (Table 4).
  - **Negation words:** ~**10.7%** of data; most models worse with negation (Table 5).
  - **Sub-options:** ~**10.8%** of data; accuracy drops **~10–20 points**; **GPT-4 5-shot: 71.72 (no sub-options) vs 53.41 (with)** (~**−18.3**) (Table 6).

## When to surface
Use when students ask how to **build/evaluate a Chinese MMLU-style benchmark**, compare **Chinese vs multilingual LLM accuracy**, or discuss **prompting/eval choices** (next-token vs free-gen, few-shot, CoT, negation/sub-option difficulty, contamination/overlap checks).