# Card: API-Bank benchmark (tool-augmented LLM eval + results)
**Source:** https://aclanthology.org/anthology-files/pdf/emnlp/2023.emnlp-main.187.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** API-Bank benchmark design (Call / Retrieve+Call / Plan+Retrieve+Call), executable evaluation protocol, and quantitative success rates across models.

## Key Content
- **Ability grading (Sec. 2.1):** derived from 2 axes: *(Few vs Many APIs in pool)* and *(Single vs Several API calls per turn)* → merged into 3 evaluated abilities:  
  1) **Call** (APIs known)  
  2) **Retrieve+Call** (APIs unknown; retrieve then call single API)  
  3) **Plan+Retrieve+Call** (APIs unknown; iterative plan/retrieve/call multiple APIs)
- **Evaluation system (Sec. 3):** **73 runnable APIs**; evaluation set **314 dialogues**, **753 API calls** (discarded **21.5%** of 400 annotated). Multi-turn allowed; multi-call supported.
- **API Search / ToolSearcher (Sec. 3.1):** required before every other API call in retrieval settings. Model condenses demand → **keywords**; system embeds keywords + API metadata, uses **cosine similarity**, returns top-matching API metadata.
- **Metrics (Sec. 3.3):**
  - **API-call correctness (Accuracy):** correct if predicted call yields **same DB query/modification and same returned results** as annotated call.
  - **Response quality:** **ROUGE-L** after tool execution.
- **Main results (Table 3, zero-shot unless noted):** API-call correctness (Total / Call / Retrieve+Call / Plan+Retrieve+Call)
  - **GPT-4:** **60.24% / 63.66% / 37.04% / 70.00%**
  - **GPT-3.5-turbo:** **47.16% / 59.40% / 38.52% / 22.00%**
  - **Lynx-7B (fine-tuned):** **39.58% / 49.87% / 30.37% / 20.00%**
  - **Alpaca-7B:** **15.19% / 24.06% / 5.19% / 0.00%**
  - **GPT-3 Davinci:** **0.57% / 0.50% / 1.48% / 0.00%**
- **Fine-tuning defaults (Sec. 7):** Lynx initialized from Alpaca/LLaMA-7B; **3 epochs**, **batch size 256**, **lr 2e-5**. Multi-agent data gen cost **$0.1/dialogue** vs **$8** manual (~**98%** savings).

## When to surface
Use when students ask how to *evaluate* tool-calling agents (ReAct/LangGraph), what metrics to track (call accuracy vs response ROUGE), or want concrete baseline success rates for tool use across models and difficulty tiers.