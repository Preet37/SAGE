---
title: "Evaluation Benchmarks"
subject: "Agents & Reasoning"
date: 2025-01-01
tags:
  - "subject/agents-and-reasoning"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/chip-huyen"
  - "educator/hugging-face"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Chip Huyen"
  - "Hugging Face"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Evaluation Benchmarks

## Video (best)
- **Andrej Karpathy** — "State of GPT" (Microsoft Build 2023)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=bZQun8Y4L2A)
- Why: Karpathy dedicates a substantial segment to how LLMs are evaluated, covering benchmark design philosophy, contamination risks, and the limitations of static benchmarks — directly relevant to this topic and highly accessible.
- Level: beginner/intermediate

---

## Blog / Written explainer (best)
- **Eugene Yan** — "Patterns for Building LLM-based Systems & Products"
- **Link:** [https://eugeneyan.com/writing/llm-patterns/](https://eugeneyan.com/writing/llm-patterns/)
- Why: Widely cited in the ML community, covers evaluation patterns including LLM-as-judge, human eval, and benchmark contamination with concrete examples and practical framing. Bridges research and production concerns.
- Level: intermediate

**Supplementary:**
- **Chip Huyen** — "Open Challenges in LLM Research" (evaluation section)
- **Link:** [https://huyenchip.com/2023/08/16/llm-research-open-challenges.html](https://huyenchip.com/2023/08/16/llm-research-open-challenges.html)
- Why: Covers hallucination measurement, benchmark limitations, and production evaluation challenges from a practitioner perspective.
- Level: intermediate

---

## Deep dive
- **EleutherAI** — Open LLM Leaderboard documentation + evaluation harness docs
- **Link:** [https://github.com/EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)
- Why: The `lm-evaluation-harness` repository is the de facto standard implementation for running MMLU, HellaSwag, HumanEval, and dozens of other benchmarks. Its README and task implementations serve as the most comprehensive technical reference for *how* benchmarks actually work in practice — covering prompt formatting, few-shot setup, metric computation, and contamination concerns.
- Level: advanced

---

## Original paper
- **Hendrycks et al.** — "Measuring Massive Multitask Language Understanding" (MMLU, 2020)
- **Link:** [https://arxiv.org/abs/2009.03300](https://arxiv.org/abs/2009.03300)
- Why: MMLU is the single most referenced LLM benchmark and this paper established the paradigm of broad, multi-domain academic evaluation. It is readable, well-structured, and directly motivates discussions of contamination, task diversity, and benchmark saturation that define the field. HumanEval (Chen et al., 2021, arxiv 2107.03374) is the complementary seminal paper for code evaluation.
- Level: intermediate

**Honorable mention:**
- **Zheng et al.** — "Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena" (2023)
- **Link:** [https://arxiv.org/abs/2306.05685](https://arxiv.org/abs/2306.05685)
- Why: Foundational paper for the LLM-as-judge paradigm and Chatbot Arena (LMSYS), directly covering two of the related concepts in this topic.
- Level: intermediate/advanced

---

## Code walkthrough
- **EleutherAI** — `lm-evaluation-harness` — running MMLU and HumanEval end-to-end
- **Link:** [https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks](https://github.com/EleutherAI/lm-evaluation-harness/tree/main/lm_eval/tasks)
- Why: Walking through actual task implementations (e.g., `mmlu/`, `humaneval/`) shows learners exactly how prompts are constructed, how metrics are computed, and where contamination can enter — far more instructive than any tutorial video. Pairs naturally with the deep dive above.
- Level: advanced

**Supplementary notebook-style walkthrough:**
- **Hugging Face** — "Evaluate" library documentation with worked examples
- **Link:** [https://huggingface.co/docs/evaluate/index](https://huggingface.co/docs/evaluate/index)
- Why: More beginner-friendly entry point with runnable code for common metrics (accuracy, BLEU, ROUGE, exact match) before tackling full benchmark harnesses.
- Level: beginner/intermediate

---

## Coverage notes
- **Strong:** Static benchmark evaluation (MMLU, HumanEval), LLM-as-judge / Chatbot Arena, contamination concerns, VQA evaluation — all have solid papers and written resources
- **Weak:** Agent evaluation and trajectory analysis — emerging area with limited consolidated pedagogical resources; most material is in recent papers (GAIA, AgentBench, τ-bench) rather than polished explainers
- **Weak:** Observability and task completion rate in production settings — covered in MLOps literature but rarely connected explicitly to benchmark framing
- **Gap:** No single high-quality YouTube video cleanly covers the *full* evaluation benchmarks landscape (static + arena + agent + multimodal) in one explainer. Most videos focus on a single benchmark or paper.
- **Gap:** VQA evaluation specifically (as distinct from general multimodal) lacks a strong standalone explainer video outside of original paper presentations.

---

## Cross-validation
This topic appears in **3 courses**: `intro-to-agentic-ai`, `intro-to-llms`, `intro-to-multimodal`

| Concept | intro-to-llms | intro-to-agentic-ai | intro-to-multimodal |
|---|---|---|---|
| MMLU / HumanEval | ✅ Core | ➖ Reference | ➖ Reference |
| Chatbot Arena / LLM-as-judge | ✅ Core | ✅ Relevant | ➖ Peripheral |
| Agent eval / trajectory analysis | ➖ Peripheral | ✅ Core | ➖ Peripheral |
| VQA evaluation | ➖ Not covered | ➖ Peripheral | ✅ Core |
| Contamination | ✅ Core | ✅ Relevant | ✅ Relevant |
| Observability / task completion | ➖ Peripheral | ✅ Core | ➖ Peripheral |

---

---

## Additional Resources for Tutor Depth

> **54 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Agentic LLM Reliability—KAMI v0.1 trace analysis + eval setup
**Paper** · [source](https://arxiv.org/html/2512.07497v2)

*Empirical reliability evidence in agentic tool-use + evaluation configuration (KAMI v0.1); failure archetypes that motivate reliability metrics beyond aggregate scores*

<details>
<summary>Key content</summary>

- **Dataset / method:** 900 manually reviewed execution traces = **3 models × 10 scenarios × 30 trials** (random sample, **12.5%** of ~240 trials/model/scenario). Emergent coding over full traces (tool calls + tool outputs + outcomes). (Section 2.4)
- **Models + pooled KAMI v0.1 accuracy (Table 1):**
  - **Granite 4 Small (32B, dense): 58.5%** (95% t-CI **57.5–59.3**)
  - **Llama 4 Maverick (400B total / 17B active, MoE): 74.6%** (CI **73.8–75.3**)
  - **DeepSeek V3.1 (671B total / 37B active, MoE): 92.2%** (CI **91.2–93.2**)
  - **DeepSeek V3: 59.4%** (CI **59.0–59.7**) → same architecture as V3.1; improvement attributed to **post-training RL** (Sections 1, 4; Table 1).
- **Recurring failure archetypes (Section 1.2):** (1) premature action without grounding (schema guessing), (2) over-helpfulness substituting missing entities, (3) distractor-induced context pollution, (4) fragile execution under load (malformed tool calls, loops, inconsistent recovery).
- **Benchmark configuration defaults (Section 2.3):** max **20 rounds**; **single tool call per round**; **temperature 0.4**; context window **32K** (non-thinking) / **128K** (thinking); max output **8K tokens/round** (non-thinking); all analyzed models run **non-thinking**.
- **Design rationale:** randomized task parameters to probe stochasticity + reduce memorization; aggregate scores hide *how* failures occur—trace-level analysis needed for enterprise reliability engineering. (Sections 1.2, 2.3)

</details>

### 📄 CMMLU (Chinese MMLU-style benchmark) — construction + eval protocol + results
**Paper** · [source](https://aclanthology.org/2024.findings-acl.671.pdf)

*Benchmark construction + leaderboard-style results/ablations (splits, protocol, numbers)*

<details>
<summary>Key content</summary>

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

</details>

### 📄 DPR dual-encoder objective + in-batch negatives
**Paper** · [source](https://aclanthology.org/2020.emnlp-main.550.pdf)

*Dual-encoder DPR training objective (in-batch negatives / contrastive log-likelihood), dot-product scoring, end-to-end retriever→reader procedure + key hyperparams/results*

<details>
<summary>Key content</summary>

- **Retrieval scoring (Eq. 1, Sec. 3.1):**  
  \[
  \text{sim}(q,p)=E_Q(q)^\top E_P(p)
  \]
  where \(E_Q, E_P\) are question/passage encoders; vectors are \(d\)-dim (BERT-base [CLS], \(d=768\)). Retrieve top-\(k\) passages by maximum inner product search (FAISS).
- **Training loss (Eq. 2, Sec. 3.2):** for instance \(\langle q_i,p_i^+,p_{i,1}^-,...,p_{i,n}^-\rangle\),
  \[
  L=-\log \frac{e^{\text{sim}(q_i,p_i^+)}}{e^{\text{sim}(q_i,p_i^+)}+\sum_{j=1}^n e^{\text{sim}(q_i,p_{i,j}^-)}}
  \]
- **In-batch negatives (Sec. 3.2):** batch size \(B\). Build \(Q,P\in\mathbb{R}^{B\times d}\); \(S=QP^\top\in\mathbb{R}^{B\times B}\). Positive pairs are diagonal \(i=j\); negatives are other batch passages (\(B-1\) per question), yielding \(B^2\) pairs/batch.
- **Negatives used (Sec. 3.2, 5.2):** best model uses **gold in-batch negatives + 1 BM25 hard negative per question** (BM25 passage that doesn’t contain answer). Adding 1 BM25 negative helps; adding 2 doesn’t.
- **Key retrieval results (Table 2):** Top-20 accuracy (answer in retrieved passages):  
  - NQ: **DPR 78.4 vs BM25 59.1**  
  - TriviaQA: **79.4 vs 66.9**  
  - WQ: **73.2 vs 55.0**  
  - TREC: **79.8 vs 70.9**
- **Training hyperparams (Sec. 5):** batch size **128**; epochs **40** (large datasets) / **100** (small); LR **1e-5** Adam + linear warmup; dropout **0.1**.
- **Indexing/runtime (Sec. 5.4):** Wikipedia split into **21,015,324** passages of **100 words** (+ title + [SEP]). FAISS retrieval ~**995 Q/s** (top-100). Dense embedding compute ~**8.8h on 8 GPUs**; FAISS index build **8.5h**; Lucene index build **~30 min**.

</details>

### 📄 MMLU-CF (contamination-free MMLU) — methodology + results
**Paper** · [source](https://aclanthology.org/2025.acl-long.656.pdf)

*Contamination-detection methodology + contamination-free evaluation results (tables) incl. sampling/settings*

<details>
<summary>Key content</summary>

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

</details>

### 📄 Maximal Marginal Relevance (MMR) selection criterion
**Paper** · [source](https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf)

*Original MMR equation balancing query relevance vs novelty/diversity via λ*

<details>
<summary>Key content</summary>

- **MMR selection criterion (Eq. 1 / Section 2):** incrementally select the next item \(D_i\) from retrieved set \(R\) given already-selected set \(S\):  
  \[
  \mathrm{MMR} \triangleq \arg\max_{D_i \in R \setminus S}\Big[\lambda\, \mathrm{Sim}_1(D_i,Q)\;-\;(1-\lambda)\max_{D_j \in S}\mathrm{Sim}_2(D_i,D_j)\Big]
  \]
  **Variables:**  
  - \(C\): document collection/stream; \(Q\): query/user profile  
  - \(R = IR(C,Q,\theta)\): retrieved/ranked list from an IR system with threshold \(\theta\) (match degree or top-N cutoff)  
  - \(S\subset R\): already selected docs/passages; \(R\setminus S\): unselected candidates  
  - \(\mathrm{Sim}_1\): similarity for relevance (doc/passages ↔ query)  
  - \(\mathrm{Sim}_2\): similarity for redundancy (candidate ↔ selected); may equal \(\mathrm{Sim}_1\) or differ  
  - \(\lambda\in[0,1]\): tradeoff; \(\lambda=1\) ⇒ pure relevance ranking; \(\lambda=0\) ⇒ maximal diversity among \(R\)
- **Procedure (reranking / summarization):** segment document into passages (sentences), compute cosine similarity, apply MMR to rerank passages for a query; output top passages in original document order (Section 4).
- **Suggested λ strategy (Section 2):** start broad with \(\lambda\approx 0.3\), then refocus with reformulated query and \(\lambda\approx 0.7\).
- **Empirical results:**  
  - User study (Section 3): 80% (4/5) chose MMR method for a search task.  
  - SUMMAC’98 (Section 4): MMR summarizer achieved **F-score 0.73** for query-relevant summaries; **70% accuracy** on “informative summaries.”  
  - Sentence precision (Table 1): compression 10%: \(\lambda=1\) **0.78/0.83**, \(\lambda=.7\) **0.76/0.83**, \(\lambda=.3\) **0.74/0.79**; Lead sentences **0.74/0.83**. Compression 25%: \(\lambda=1\) **0.74/0.76**, \(\lambda=.7\) **0.73/0.74**, \(\lambda=.3\) **0.74/0.76**; Lead sentences **0.60/0.65**.

</details>

### 📄 Measuring Position Bias in LLM-as-a-Judge
**Paper** · [source](https://arxiv.org/abs/2406.07791)

*Operational definitions + measurement protocol for position bias (RS/PC/PF), factors, and analysis workflow (pairwise + list-wise)*

<details>
<summary>Key content</summary>

- **Evaluation protocol (Section 2.1):**
  - **Pairwise:** judge sees *original prompt* (A then B) and *swapped prompt* (B then A) → a **judgment pair**. Double-blind (candidate identities hidden).
  - **Option modes:** **Two-option** {A,B}; **Three-option** {A,B,C} where **C=tie** (explicit in system prompt).
  - **List-wise:** choose **best** among ≥3 candidates (not full ranking). Use **all order permutations** so each candidate appears in each position exactly once (for *n* candidates → *n!* permutations). Tie option allowed.
- **Metrics (Section 2.2):**
  - **Repetition Stability RS (Eq. 1):** reliability under identical repeated queries.  
    \[
    RS=\frac{1}{N}\sum_{i=1}^{N}\frac{\max_{c\in C}\text{count}_i(c)}{T}
    \]
    *C*: choice set; *T*: repeats per query; *N*: #queries.
  - **Position Consistency PC (Eq. 2):** fraction of prompt-series where the **same winning solution** is chosen across permutations:  
    \[
    PC=\frac{\#\text{consistent series}}{\#\text{valid series}}
    \]
  - **Preference Fairness PF (Eq. 3):** single min–max scaled score centered at 0; sign indicates **primacy** (favor first) vs **recency** (favor later). Extended to list-wise via **“one-vs-all”** (first=primacy, others=recency).
- **Defaults/parameters (Section 3.1):**
  - Temperature **=1** for all judges.
  - RS computed with **3 repeats**; sample: **3 questions/task** and **4 candidate models**, paired with baseline.
  - Pairwise datasets: **MTBench** (baseline **vicuna-13b-v1.3**, **Two-option**, 30 candidates, 8 tasks, 10 Q/task) and **DevBench** (baseline **human**, **Three-option**, 10 candidates, 14 tasks, 8 Q/task).
  - Scale: **4,800** (MTBench) and **2,240** (DevBench) instances for PC/PF; **>100k** total evaluations.
- **Key empirical results (Table 2 + Findings):**
  - Capable judges show **RS > 0.95** (e.g., Claude-3.5-Sonnet, GPT-4, Llama-3.3-70B), supporting bias is **not random**.
  - Bias varies by **judge & task**; **PC and PF can diverge** (high PC ≠ fair).
  - **Answer quality gap** strongly affects PC (larger gap → higher PC); **length effects weak** (only output length minimally significant).
  - Agreement analysis: **>50%** of instances have **≥80%** judge agreement; **<2%** are extreme disagreement (hard-to-judge).
- **Factor analysis workflow (Section 3.1, Appendix E):** bidirectional **stepwise regression with AIC** predicting PC/PF using: judge identity/series, candidate identity, task category, lengths (input/output/prompt), and **answer quality gap**.

</details>

### 📄 Neural Network Calibration Metrics & Temperature Scaling (Guo et al., 2017)
**Paper** · [source](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf)

*Definitions of calibration metrics (ECE/MCE), reliability diagrams, temperature scaling procedure*

<details>
<summary>Key content</summary>

- **Perfect calibration definition (Eq. 1):**  
  \[
  \mathbb{P}(\hat Y = Y \mid \hat P = p)=p,\ \forall p\in[0,1]
  \]  
  where \(\hat Y\) is predicted label, \(Y\) true label, \(\hat P\) confidence (probability assigned to \(\hat Y\)).
- **Reliability diagram binning (Section 2):** Partition predictions into \(M\) confidence bins \(I_m=(\frac{m-1}{M},\frac{m}{M}]\). Let \(B_m=\{i:\hat p_i\in I_m\}\).  
  \[
  \text{acc}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\mathbf{1}(\hat y_i=y_i),\quad
  \text{conf}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\hat p_i
  \]
- **Expected Calibration Error (ECE) (Eq. 3):**  
  \[
  \mathrm{ECE}=\sum_{m=1}^M \frac{|B_m|}{n}\,|\text{acc}(B_m)-\text{conf}(B_m)|
  \]
- **Maximum Calibration Error (MCE) (Eq. 5):**  
  \[
  \mathrm{MCE}=\max_{m\in\{1,\dots,M\}}|\text{acc}(B_m)-\text{conf}(B_m)|
  \]
- **Negative Log Likelihood (NLL) (Eq. 6):** \(L=-\sum_{i=1}^n \log \hat\pi(y_i|x_i)\).
- **Temperature scaling (multiclass) (Eq. 9, Section 4.2):** with logits \(z_i\), temperature \(T>0\):  
  \[
  \hat q_i=\max_k \mathrm{softmax}(z_i/T)_k
  \]
  Optimize \(T\) on a **held-out validation set** by minimizing **NLL**; **predicted class unchanged** (argmax invariant), so **accuracy unchanged**. \(T>1\) softens; \(T\to\infty\Rightarrow 1/K\); \(T\to 0\Rightarrow 1\).
- **Empirical defaults/results:** ECE reported with **\(M=15\) bins** (Table 1). Example: **CIFAR-100 ResNet-110 (SD)** ECE **12.67% → 0.96%** with temperature scaling (Figure 4/Table 1). **CIFAR-10 ResNet-110** ECE **4.6% → 0.83%**. Temperature scaling often best on vision tasks.
- **Compute/implementation note:** temperature scaling is **1D convex optimization**; reported ~**10 iterations** with conjugate gradient; implement by inserting a scalar multiply \(1/T\) between logits and softmax.

</details>

### 📄 Unbiased pass@k for code functional correctness (HumanEval/Codex)
**Paper** · [source](https://arxiv.org/pdf/2107.03374.pdf)

*Primary-source definition + unbiased estimator + sampling protocol for pass@k (HumanEval-style)*

<details>
<summary>Key content</summary>

- **Why pass@k (functional correctness) vs BLEU/match metrics (Sec. 2.1):** Many programs are functionally equivalent but text-different; unit-test passing matches how developers judge code. BLEU can overlap heavily between correct/incorrect solutions (Fig. 8), so BLEU improvements may not imply correctness.
- **pass@k definition + unbiased estimator (Eq. 1, Sec. 2.1):** For each task, generate **n ≥ k** samples, run unit tests, count **c** correct samples (c ≤ n). Unbiased estimator:
  \[
  \text{pass@}k := \mathbb{E}_{\text{problems}}\left[1 - \frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
  \]
  where \(n\)=#samples, \(c\)=#passing samples, \(k\)=budget. Authors use **n=200**, **k≤100** to reduce variance vs naive “any of k” computation.
- **Numerically stable computation (Fig. 3):**
  - If \(n-c<k\): return 1.0  
  - Else: \(1 - \prod_{i=n-c+1}^{n}\left(1-\frac{k}{i}\right)\)
  - (Given as a stable numpy implementation.)
- **Bias warning:** Estimating pass@k as \(1-(1-\hat p)^k\) with \(\hat p=\) empirical pass@1 is **biased** (Appendix A).
- **HumanEval dataset (Sec. 2.2):** **164** hand-written Python function tasks; avg **7.7** unit tests/problem.
- **Key empirical pass rates (Table 1, HumanEval):** Codex-12B **pass@1 28.81%**, **pass@100 72.31%**; GPT-J 6B **11.62% / 27.74%**; GPT-Neo 2.7B **6.41% / 21.37%**; TabNine **2.58% / 7.59%**.
- **Sampling defaults:** nucleus sampling **top-p=0.95**; stop sequences include `\nclass`, `\ndef`, `\n#`, `\nif`, `\nprint`. Temperature tuned by k (e.g., optimal for 679M: **T*=0.2** for pass@1, **T*=0.8** for pass@100).

</details>

### 📄 pass@k functional correctness eval (Codex / HumanEval)
**Paper** · [source](https://arxiv.org/abs/2107.03374)

*Formal definition + unbiased estimator for pass@k; offline evaluation protocol for code generation (HumanEval), plus key reporting conventions.*

<details>
<summary>Key content</summary>

- **Why functional correctness (Sec. 2.1):** Match-based metrics (exact match/BLEU) fail to capture the large space of functionally equivalent programs; instead evaluate **correctness by unit tests**.
- **pass@k definition (Sec. 2.1):** Generate **k samples per problem**; a problem is “solved” if **any** sample passes unit tests; report fraction solved across problems.
- **Unbiased pass@k estimator (Eq. 1):** For each task, generate **n ≥ k** samples, let **c** be #samples that pass tests. Estimate  
  \[
  \text{pass@k} := \mathbb{E}_{\text{Problems}}\left[1-\frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
  \]
  - Variables: **n** total samples, **c** correct samples, **k** budgeted draws.
  - Paper uses **n = 200**, **k ≤ 100**.
  - Notes: direct computation can be numerically unstable; paper provides a stable NumPy product-form implementation. Avoid biased shortcut \(1-(1-\hat p)^k\) (biased; App. A).
- **HumanEval dataset (Sec. 2.2):** **164** hand-written Python function-synthesis problems; each includes signature/docstring/body + unit tests; avg **7.7 tests/problem**.
- **Sampling/eval defaults (Sec. 3):** Nucleus sampling **top-p = 0.95**; stop sequences: `\nclass`, `\ndef`, `\n#`, `\nif`, `\nprint`.
- **Temperature tuning (Sec. 3.3):** Optimize temperature per k; higher T for larger k (diversity helps). Example (679M): **T*=0.2 for pass@1**, **T*=0.8 for pass@100**.
- **Key results (Abstract/Fig. 1):** On HumanEval: Codex-12B **pass@1 = 28.8%**; GPT-3 ~**0%**; GPT-J-6B **11.4%**. With **100 samples**, Codex reaches **70.2%**; Codex-S **pass@1 = 37.7%**, and **77.5% within 100 samples**. Best-of-100 by **highest mean log-prob** yields **44.5%**.

</details>

### 📊 AgentArch enterprise agent-architecture benchmark (18 configs)
**Benchmark** · [source](https://arxiv.org/html/2509.10769v1)

*Benchmark design + quantitative comparisons across orchestration, prompting (ReAct vs function calling), memory, thinking tools*

<details>
<summary>Key content</summary>

- **Benchmark setup (Section 3.1):** 2 enterprise workflows, each **60 user utterances** with **deterministic tool outputs** and **messy/long enterprise-realistic data** (KB articles thousands of words; tool outputs complex JSON with metadata/error codes).
  - **Requesting Time Off (TO):** simpler; **8 tools**, **3 agents**; challenges include date calculations, leave balance/policy compliance.
  - **Customer Request Routing (CR):** complex; **31 tools**, **9 agents**; challenges include escalation decisions, context preservation, ambiguous requests, routing logic.
- **Architectural dimensions tested (18 configurations):**
  - **Orchestration:** (1) orchestrator-led **isolated** agents, (2) orchestrator-led **open** agent network, (3) **single agent** (all tools, no collaboration).
  - **Agent style:** **Function calling** vs **ReAct** (reasoning-action format).
  - **Memory:** **complete** (all prior tool calls/params/responses) vs **summarized** (final summaries only).
  - **Thinking tools:** enabled/disabled (e.g., **math**, **synthesize_collected_information**).
- **Primary metric (Section 3.2): Acceptable Score** = % records satisfying **all**: correct **tool choice**, correct **tool arguments**, correct **final decision**.
  - Tool choice scoring: **Lenient Acceptable** (allows extra read-only tools; penalizes extraneous writes) vs **Strict Acceptable** (exact tools, correct order, no extras/hallucinations). Main reporting uses **lenient**.
  - Reliability: **pass@1** (primary) and **pass^K** = probability **all K trials succeed**.
- **Key empirical results (Section 4.1):**
  - Peak performance: **TO max 70.8%** (GPT-4.1); **CR max 35.3%** (Sonnet 4).
  - **Thinking tools** help on TO for non-reasoning models: GPT-4.1 **48.5% → 70.8%** (single-agent function calling, summarized memory). Minimal benefit for o3-mini **55.8% → 56.7%**.
  - **Function calling generally > ReAct**; **multi-agent ReAct consistently underperforms**.
  - **Hallucinations** occur **exclusively under ReAct** for all models except GPT-4o; Sonnet 4 shows **36–36% hallucination** in multi-agent ReAct vs **0%** elsewhere.
  - Reliability gap: best **pass^k peaks at 0.0634** (only **6.34%** chance of perfect success across **8 trials**).

</details>

### 📊 AgentBench — LLMs as Interactive Agents (8 Environments)
**Benchmark** · [source](https://arxiv.org/abs/2308.03688)

*End-to-end agent task success rates across multiple environments + trajectory/round limits + common failure causes (TLE/IF/IA/CLE)*

<details>
<summary>Key content</summary>

- **Formalization (Section 2):** Interactive evaluation of an LLM agent is modeled as a **POMDP** with components: state space \(S\), action space \(A\), transition \(T\), reward \(R\), task-instruction space \(I\), observation space \(O\). Agent denoted \(M\).
- **Prompting/eval procedure (Section 4.1):**
  - Two-role dialogue: **user** (instruction + environment feedback) and **agent** alternating; trajectory stored as conversation history.
  - Input truncation: choose minimal \(k\) such that token count of history \(\le 3500\); omit earlier messages and append `"[NOTICE] messages are omitted."`
  - Output format includes **Thought + Action in one round** (CoT-style); **temperature = 0** (greedy) for reproducibility.
  - Non-chat models: prepend `USER:` / `AGENT:` per turn; end with `AGENT:` to elicit completion.
- **Finish reason taxonomy (Section 2):**
  - **CLE** (context limit exceeded), **IF** (invalid format), **IA** (invalid action), **TLE** (task limit exceeded / repetitive generations), **Complete**.
- **Benchmark composition (Section 3):** 8 environments across **code-grounded** (OS bash SR; DB SQL SR; KG QA F1), **game-grounded** (DCG win rate; LTP game progress; HH/ALFWorld SR), **web-grounded** (WS reward; WB step SR). Estimated solving rounds per problem: **5–50**.
- **Dataset sizes (Table 2):** total **Dev 269**, **Test 1,014**; ~**3k** and **11k** inference calls (≈ MMLU call volume).
- **Key empirical results (Table 3 / Section 4.2):**
  - **gpt-4 (0613)** overall score **4.01**; notable SRs: **House Holding 78.0%**, **Web Shopping 74.5%**, **OS 42.4%**, **DB 32.0%**, **KG F1 58.8**, **WB step SR 61.1**.
  - **gpt-3.5-turbo (0613)** overall **2.32**; **OS 32.6%**, **HH 64.1%**, **WS 33.7%**.
  - **OSS vs API gap:** average OSS overall **0.51** vs API **2.32**; best OSS reported **codellama-34b overall 0.96**.
- **Failure outcome proportions (Table 4; per-environment):** TLE dominates in several tasks (e.g., **KG TLE 67.9%**, **LTP TLE 82.5%**); **DB IF 53.3%**; **HH IA 64.1%**; **OS Complete 75.0%** with **TLE 23.9%**.

</details>

### 📊 Chatbot Arena Elo Leaderboard (Anonymous Pairwise Human Votes)
**Benchmark** · [source](https://www.lmsys.org/blog/2023-05-03-arena/)

*Elo-based leaderboard methodology for Chatbot Arena (anonymous randomized battles, Elo computation framing, initial results)*

<details>
<summary>Key content</summary>

- **Benchmark setup (workflow):**
  - Users chat with **two anonymous models side-by-side** and **vote** for the better answer; **model names revealed only after voting**.
  - Platform **logs interactions**; analysis uses **only votes where names were hidden** (anonymous votes).
  - Initial launch collected **4.7k valid anonymous votes** in ~1 week.
  - Pairing policy: initially **non-uniform** (biased toward “strong pairings” based on prior ranking), later switched to **uniform sampling** for better coverage; introduced **fastchat-t5-3b** late → non-uniform model frequency.
  - Prompts are “in the wild”; language distribution: **mostly English** (top-15 languages plotted).
- **Elo model (Eq. 1–2):**
  - **Win probability (logistic, base 10):**  
    **Eq. 1:** \(E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}\)  
    where \(R_A, R_B\) are Elo ratings; \(E_A\) is expected score/probability A wins.
  - **Rating update:**  
    **Eq. 2:** \(R'_A = R_A + K(S_A - E_A)\)  
    where \(S_A\) is actual score (win=1, tie=0.5, loss=0); \(K\) is update factor.
- **Empirical results (initial leaderboard):**
  - **Timeframe:** **Apr 24 – May 1, 2023**; **9 models** listed; ratings computed from the **4.7k votes** (notebook linked in post).
  - Pairwise win-rate heatmap shown; **Elo-predicted win rates match observed win rates “relatively well.”**
- **Design rationale:** Pairwise human preference handles **open-ended** assistant quality; Elo provides **scalability**, **incrementality** (new model needs fewer trials), and a **unique ordering** across many models.

</details>

### 📊 SpecTool tool-use error taxonomy + metrics
**Benchmark** · [source](https://ar5iv.labs.arxiv.org/html/2411.13547)

*Quantitative taxonomy + measurement of tool-use failure modes (schema/argument/format vs planning/selection), with model breakdowns and feedback-based evaluation.*

<details>
<summary>Key content</summary>

- **SpecTool dataset (Section 4):** 150 human-annotated tool-use queries across **10 environments** (Tools, Movies, Travel, Sports, Entertainment, Data, Social, Media, Weather, Video Images; table also lists Patent, Spaceflight). Overall averages: **6.8 interactions/query**, **6.2 APIs/query**. Example env stats: Movies **30 queries**, **11 avg interactions**, **11.5 avg APIs**; Patent **20**, **6**, **7.2**; Spaceflight **25**, **9**, **10**.
- **7 error patterns (Section 3):**
  - **IAC** Insufficient API Calls (too few calls to complete task)
  - **IAV** Incorrect Argument Value (incl. missing required args)
  - **IAN** Incorrect Argument Name (hallucinated arg names)
  - **IAT** Incorrect Argument Type
  - **RAC** Repeated API Calls (exact repeats)
  - **IFN** Incorrect Function Name (hallucinated tool)
  - **IFE** Invalid Format Error (violates required parseable format)
- **Evaluation workflow (Section 5):** deterministic environments; agent gets instructions + tool list + format requirements. A **constructive feedback mechanism** checks: (1) parse/format, (2) action in allowed action space (else list valid actions), (3) argument validity (else list valid args + descriptions), (4) argument types (else specify correct types). Only then execute tool and feed observation back.
- **Metrics (Section 6):** Let **N** = max steps; **GT** = labeled ground-truth trajectories.
  - For **IFN/IAN/IAT/IFE/RAC**: error accuracy = **1 − (# API calls exhibiting that error / N)**.
  - For **IAC/IAV**: computed vs each labeled trajectory **g**: **1 − (# API calls with errors w.r.t. GT trajectory g / N)**.
  - Higher metric = fewer errors; aligned with success rate.
- **Key empirical results (Table 3):** Success rates: **GPT-4-0125-preview 0.71** (best), **xLAM-8x22b 0.68**, **xLAM-7b 0.64**, **Code-Llama-13b 0.54**, **GPT-3.5-turbo-1106 0.53**, **Meta-Llama3-8b 0.27**, **Vicuna-13b-16k 0.16**, **Mixtral-8x7b 0.10**. Example error metrics for GPT-4-0125: **RAC 1.00, IFE 1.00, IAC 0.84, IAV 0.94, IAN 0.94, IFN 0.94**.
- **Design rationale (Sections 1–2, 6–7):** prior benchmarks mostly report success-only; SpecTool adds **diagnostic error breakdown**, **multiple valid GT trajectories**, and **feedback** to expose brittle tool-call failures (schema/format/selection) that propagate downstream.

</details>

### 📊 WebArena benchmark (realistic, reproducible web-agent eval)
**Benchmark** · [source](https://arxiv.org/abs/2307.13854)

*End-to-end web task benchmark with baseline agent implementations and success-rate results in a reproducible, realistic browser environment.*

<details>
<summary>Key content</summary>

- **Environment design (Sec. 2):** Standalone, self-hosted web apps (Docker + gym-style APIs) to ensure **reproducibility** (avoids CAPTCHAs, content drift, config changes) while preserving **realism** via open-source stacks + imported real-world data.
- **Domains/sites:** 4 fully functional websites: **e-commerce**, **social forum**, **collaborative development (GitLab-based)**, **CMS**. Plus utility tools: **map, calculator, scratchpad**; knowledge resources: **English Wikipedia + site manuals**.
- **Formal agent interaction (Sec. 2.1):** Given intent \(I\), agent chooses action \(a_t\) from current observation \(o_t\), action history, observation history; deterministic transition yields new state/observation. Reward checks whether state transitions satisfy intent (e.g., order placed; answer correctness).
- **Observation space (Sec. 2.3):** Mimics browser: **URL + open tabs + focused tab content**; supports **multi-tab** tasks. Render modes: **DOM/HTML**, **screenshot**, **accessibility tree** (compact structured subset of DOM). Optional **viewport-limited** observations for context constraints.
- **Action space (Sec. 2.4):** Compound mouse/keyboard + tab + navigation actions: click/hover/type/press/scroll; tab_focus/new_tab/tab_close; go_back/go_forward/goto(URL). Elements selectable by **coordinates** or **unique element IDs** (turns selection into \(N\)-way classification; e.g., `click [1582]`).
- **Benchmark (Sec. 3):** **812** long-horizon tasks from **241 templates** (avg **3.3** instantiations/template). Categories: **information-seeking**, **site navigation**, **content/config**. Includes **unachievable tasks** labeled **“N/A”** to test non-hallucination.
- **Evaluation (Sec. 3.2):** Functional correctness via programmatic checks of intermediate states/DB/page content. Text answers scored by **exact_match**, **must_include**, or **fuzzy_match** (LM-based; uses **gpt-4-0613**).
- **Baseline procedure (Sec. 4):** Few-shot ICL with **2 in-context examples**; two prompting strategies: **direct action** vs **CoT then action**; uses **accessibility tree + element IDs**. Optional **Unachievable (UA) hint** instructs stopping if impossible.
- **Key empirical results (Table 2 / Sec. 5):**
  - **Human:** **78.24%** success (unachievable detection **100%**).
  - **GPT-4 + CoT + UA hint:** **11.70%** success.
  - **GPT-4 + CoT (no UA hint):** **14.41%** success; unachievable detection **44.44%**.
  - **GPT-3.5 + CoT + UA hint:** **8.75%**; **text-bison-001 + CoT + UA hint:** **5.05%**.
  - UA hint causes **early stopping**: GPT-4 marks **54.9%** of feasible tasks as impossible (Sec. 5.1).

</details>

### 📖 AWS Step Functions Retry/Catch Semantics (Error Handling)
**Reference Doc** · [source](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)

*Retry fields (IntervalSeconds, MaxAttempts, BackoffRate) and Catch behavior; error names and propagation rules*

<details>
<summary>Key content</summary>

- **Default behavior:** When a state reports an error, Step Functions **fails the entire execution** unless handled via **Retry/Catch**.
- **Where Catch/Retry apply:** Available on **Task, Parallel, Map** states (not for **top-level execution failures**). For anticipated execution-level failures: handle in caller, **nest child workflows**, or listen for **TIMED_OUT** events (Standard) via EventBridge.
- **Error names (case-sensitive strings):**
  - Built-ins start with `States.`; custom errors **cannot** start with `States.`.
  - Wildcards:  
    - `States.ALL` matches any known error name but **must appear alone** and **last** in `ErrorEquals`; **cannot catch** `States.DataLimitExceeded` or `States.Runtime`.  
    - `States.TaskFailed` matches any known error **except** `States.Timeout`.
  - Notable errors:  
    - `States.Timeout`: task timeout or heartbeat missed; if nested SM throws `States.Timeout`, parent receives `States.TaskFailed`. Also emitted when execution exceeds `TimeoutSeconds`.  
    - `States.Runtime`: non-retriable; **always fails**; not caught by `Retry/Catch` on `States.ALL`.  
    - `States.DataLimitExceeded`: terminal; not caught by `States.ALL`.
- **Retry algorithm (ordered scan):** On error, Step Functions scans `Retry[]` in order; first retrier whose `ErrorEquals` contains the error governs retries. If retries exhausted, normal error handling continues.
- **Retry timing formula (Eq. 1):** delay before attempt *k* (1-indexed)  
  `Delay_k = IntervalSeconds * (BackoffRate)^(k-1)` capped by `MaxDelaySeconds` if set; with `JitterStrategy=FULL`, delay is randomized in `[0, Delay_k]`.
- **Retry defaults/limits:** `IntervalSeconds=1` (max `99999999`), `MaxAttempts=3` (0 = never retry; max `99999999`), `BackoffRate=2.0`, `JitterStrategy=NONE`, `MaxDelaySeconds` optional (0 < value < `31622401`).
- **Catch algorithm (ordered scan):** If no Retry or retries fail, scan `Catch[]` in order; first matching catcher transitions to `Next`. `ResultPath` controls whether error output overwrites input (`$` default) or is merged.
- **Billing note:** Retries count as **state transitions**.

</details>

### 📖 AWS Step Functions — Quotas & Limits (numeric feasibility)
**Reference Doc** · [source](https://docs.aws.amazon.com/step-functions/latest/dg/limits.html)

*Concrete numeric limits for Step Functions (payloads, timeouts, throttles, history size, retention)*

<details>
<summary>Key content</summary>

- **Name constraints (General):** State machine / execution / activity task names **≤ 80 chars**, unique per account+Region; must not include whitespace, wildcards `? *`, brackets `< > { } [ ]`, many special chars (`" # % \ ^ | ~ \` $ & , ; : /`), or control chars (`\u0000-\u001f`, `\u007f-\u009f`). Non-ASCII allowed but can break CloudWatch logging (recommend ASCII).
- **Account quotas (selected):**
  - Registered state machines: **100,000** (increase to **150,000**).
  - Registered activities: **100,000** (increase to **150,000**).
  - State machine definition size: **1 MB (hard)**.
  - Step Functions API **max request size:** **1 MB per request (hard)** (includes headers + all request data).
  - **Open executions (Standard):** **1,000,000 per account per Region** (exceed → `ExecutionLimitExceeded`); **doesn’t apply to Express**.
  - Distributed Map: **open Map Runs max 1000 (hard)**; **parallel Map Run child executions max 10,000 (hard)**.
- **Execution/task hard limits (Standard vs Express):**
  - **Max execution time:** Standard **1 year**; Express **5 minutes**.
  - **Max execution history size:** Standard **25,000 events** (hit → execution fails).
  - **Max idle time:** Standard **1 year**; Express **5 minutes**.
  - **Execution history retention after close:** Standard **90 days** (can request reduction to **30 days**); Express **14 days**.
  - **Max input/output size (task/state/execution):** **256 KiB UTF-8 string** (both).
- **HTTP Task:** duration (request+response) **60 seconds (hard)**.
- **API throttling (token bucket; per account per Region; soft/increasable):**
  - `StartExecution` (Standard): bucket/refill **1300/300** (us-east-1, us-west-2, eu-west-1); **800/150** (other Regions).
  - `StartExecution` (Express): **6000/6000** (all Regions).
  - `RedriveExecution` (Standard): **1300/300** (key Regions); **800/150** (others).
  - `StopExecution` (Standard): **1000/200** (key Regions); **500/25** (others).
  - `GetActivityTask` (Standard): **3000/500** (key Regions); **1500/300** (others).
- **Versions/aliases:** published versions **1000 per state machine**; aliases **100 per state machine**.
- **Tagging (hard):** **50 tags/resource**; key **128** chars; value **256** chars; reserved prefix `aws:`.

</details>

### 📖 Amazon States Language (ASL) — State machine definition skeleton + example
**Reference Doc** · [source](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html)

*Authoritative ASL workflow definition structure; example showing `Task`, `Choice`, `Fail` and transitions*

<details>
<summary>Key content</summary>

- **ASL definition (what it is):** A **JSON-based structured language** to define a Step Functions **state machine** (a collection of states) that can:
  - do work with **`Task`** states,
  - branch with **`Choice`** states,
  - stop with error using **`Fail`** states, etc.
- **File naming requirement (outside console):** Save definitions with extension **`.asl.json`**.
- **Top-level required structure (example):**
  - `Comment`: free-text description.
  - `QueryLanguage`: example sets **`"JSONata"`**.
  - `StartAt`: name of first state (example: **`"FirstState"`**).
  - `States`: object mapping state names → state definitions.
- **State transition fields (example):**
  - `Next`: name of next state (used by `Task`, `Choice` branches).
  - `End: true`: marks terminal state (example: `NextState`).
  - `Default`: fallback transition for `Choice` (example: **`"DefaultState"`**).
- **`Task` state fields (example):**
  - `Type: "Task"`
  - `Resource`: ARN (example Lambda ARN format: `arn:aws:lambda:region:123456789012:function:FUNCTION_NAME`)
  - Optional `Assign` (JSONata) to set variables (example assigns `foo` from `$states.input.foo_input`).
- **`Choice` state fields (example):**
  - `Type: "Choice"`
  - `Choices`: array of rules, each with `Condition` (JSONata) and `Next`.
- **`Fail` state fields (example):**
  - `Type: "Fail"`, plus `Error` and `Cause` strings.

</details>

### 📖 Anthropic Messages SSE Streaming Event Semantics
**Reference Doc** · [source](https://docs.anthropic.com/en/api/messages-streaming?debug_url=1&debug=1&debug=true)

*SSE streaming message event structure, incremental delivery, tool/thinking deltas, and recovery patterns*

<details>
<summary>Key content</summary>

- **Enable streaming:** set `"stream": true` on a Messages create request; responses arrive via **Server-Sent Events (SSE)**.
- **Event flow (canonical order):**  
  1) `message_start` → contains a **Message** object with empty `content: []`  
  2) For each content block `i` in final `message.content[i]`:  
     `content_block_start(index=i)` → 1+ `content_block_delta(index=i)` → `content_block_stop(index=i)`  
  3) 1+ `message_delta` (top-level Message changes)  
  4) `message_stop` (final)
- **Usage accounting:** token counts in `message_delta.usage` are **cumulative** (e.g., `{"output_tokens": 15}`).
- **Ping events:** arbitrary number of `ping` events may appear anywhere in the stream.
- **Error events in-stream:** SSE `event: error` with JSON like  
  `{"type":"error","error":{"type":"overloaded_error","message":"Overloaded"}}` (maps to HTTP **529** in non-streaming).
- **Forward compatibility:** new event types may be added; clients should **ignore/handle unknown event types** gracefully.
- **Delta types (content_block_delta.delta.type):**
  - `text_delta`: incremental text, e.g. `"text":"Hello"`.
  - `input_json_delta`: for `tool_use` blocks; provides **partial JSON string** chunks in `partial_json`. Accumulate chunks; parse to an object at `content_block_stop`. (Current models emit **one complete key/value at a time**, so gaps between chunks can occur.)
  - `thinking_delta` + `signature_delta` (extended thinking): thinking streams as deltas; a **signature_delta arrives just before** `content_block_stop`. If `thinking.display: "omitted"`, no thinking deltas—only signature then stop.
- **SDK accumulation pattern:** stream events but return final Message via `.get_final_message()` (Python) / `.finalMessage()` (TS); Go uses `message.Accumulate(event)`; Java `MessageAccumulator.create().accumulate(event)`; Ruby `.accumulated_message`.
- **Recovery:**  
  - Claude **4.5 and earlier**: resume by sending partial assistant content and continue.  
  - Claude **4.6**: add a **user** message: “Your previous response was interrupted and ended with [previous_response]. Continue…”

</details>

### 📖 Azure Durable Functions — Stateful serverless workflows (overview)
**Reference Doc** · [source](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)

*Deterministic replay model context + orchestrator/activity/entity concepts; pointers to orchestrator constraints, storage providers, and monitoring.*

<details>
<summary>Key content</summary>

- **What Durable Functions is (definition):** An extension of **Azure Functions** for building **stateful workflows** in a **serverless** environment by writing **orchestrator**, **activity**, and **entity** functions in code. Runtime manages **state**, **checkpoints**, **retries**, and **recovery** so workflows can run reliably for **long periods**.
- **Core workflow structure (conceptual procedure):**
  - Orchestrator function coordinates execution.
  - Activity functions perform work steps.
  - Entity functions model stateful entities (for durable state patterns).
- **Getting started procedure (numbered steps from doc):**
  1. Create a new Azure Functions app using a language quickstart.
  2. Add an **orchestrator** function and **one or more activity** functions.
  3. Choose/configure a backend via **Durable Functions storage providers**; **recommended:** **Durable Task Scheduler**.
  4. Run/test locally with **Azure Functions Core Tools**.
  5. Deploy to Azure and **monitor orchestration instances**.
- **Supported languages (table facts):** Durable Functions support listed as **Supported** for **.NET (C#), JavaScript, TypeScript, Python, PowerShell, Java** (each has a “Create your first durable function” quickstart link).
- **Design rationale (explicit):** Runtime-managed state/checkpointing/retries/recovery enables **reliable long-running** workflows without manual state management.
- **Key follow-up topics to consult next (links):** **Task hubs**, **HTTP features**, and **orchestrator code constraints** (deterministic/replay constraints are referenced via link).

</details>

### 📖 Durable Functions External Events (Wait/Raise) API + Semantics
**Reference Doc** · [source](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-external-events)

*API surface for `WaitForExternalEvent` / `RaiseEvent` and correlation semantics*

<details>
<summary>Key content</summary>

- **Purpose/use case:** Orchestrator functions can **wait for external events**—commonly for **human interaction** or other external triggers (human-in-the-loop signaling).
- **One-way async constraint:** External events are **one-way asynchronous**; **not suitable** when the sender needs a **synchronous response** from the orchestrator.
- **Wait API (orchestrator side):**
  - Isolated worker: `await context.WaitForExternalEventAsync<T>("EventName")`
  - In-process: `await context.WaitForExternalEvent<T>("EventName")`
  - Orchestrator declares **event name** and expected **payload type `T`**.
  - **Type conversion rule (.NET):** if payload can’t be converted to `T`, an **exception is thrown**.
- **Concurrency patterns:**
  - **Wait for any:** create multiple `WaitForExternalEvent*` tasks and `await Task.WhenAny(...)`.
  - **Wait for all:** `await Task.WhenAll(gate1, gate2, gate3)` before proceeding.
- **Indefinite wait + lifecycle/billing:**
  - Waits **indefinitely**; app/worker can be **stopped/unloaded** while waiting; instance is **awakened automatically** when event arrives.
  - **Consumption Plan:** **no billing charges** while an orchestrator is awaiting an external event task (regardless of duration).
- **Raise API (client side):**
  - `await client.RaiseEventAsync(instanceId, eventName, eventData)`
  - Event parameters: **`instanceId`**, **`eventName`**, **`eventData`** (must be **JSON-serializable**).
  - **Correlation:** `eventName` must **match** between sender and receiver.
  - **Delivery mechanics:** message is enqueued; if instance isn’t currently waiting on that `eventName`, it’s buffered (in-memory) until it starts listening.
  - **If no instance with `instanceId`:** event is **discarded**.
- **Reliability + dedup:**
  - External events have **at-least-once delivery** ⇒ duplicates possible (restarts/scaling/crashes).
  - Best practice: include a **unique ID** in events for **manual dedup** in orchestrators.
  - Storage note: **MSSQL provider** updates state transactionally ⇒ **no duplicate risk** vs **Azure Storage provider**, but unique IDs/names still recommended for portability.
- **HTTP raise-event example:**  
  `POST /runtime/webhooks/durabletask/instances/MyInstanceId/raiseEvent/Approval&code=XXX` with JSON body `"true"`.

</details>

### 📖 Durable Functions — Durable Timers (sleep/wait) semantics
**Reference Doc** · [source](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-timers)

*Durable timer API usage + semantics for long waits/timeouts (incl. human-approval wait patterns)*

<details>
<summary>Key content</summary>

- **Use durable timers in orchestrators (not language `sleep`/`delay`)** to implement delays and timeouts in Durable Functions/Durable Task orchestrations.
- **Timer creation (Eq. 1: due-time form)**  
  - `dueTime = context.CurrentUtcDateTime + Δ` (e.g., `AddHours(72)`)  
  - `await context.CreateTimer(dueTime, cancellationToken)`  
  - Variables: `context.CurrentUtcDateTime` = orchestrator’s deterministic “now”; `Δ` = desired delay; `cancellationToken` controls cancellation.
- **Timer creation (Eq. 2: duration form)**  
  - `await context.CreateTimer(TimeSpan.FromHours(72), cancellationToken)`
- **Semantics:** awaiting the timer “sleeps” the orchestrator until expiration **while the orchestration can still process other incoming events** during the wait.
- **Underlying behavior:** creating a timer for time *T* enqueues a message that becomes visible at *T* (e.g., 4:30 PM UTC). If the app scales to zero, the visible timer message triggers reactivation on an appropriate VM.
- **Long-timer limits / behavior (numbers):**
  - **JavaScript, Python, PowerShell:** durable timers limited to **6 days**; workaround: loop with multiple timers to simulate longer delays.
  - **.NET and Java (up-to-date):** support **arbitrarily long** timers.
  - Some SDK/storage-provider combos may implement **≥6-day** waits as **multiple shorter timers** (e.g., **3-day** chunks); visible in logs/history but not orchestration behavior.
- **Time calculation rule:** don’t use built-in date/time APIs; always use orchestration context time (`context.CurrentUtcDateTime`, `ctx.current_utc_datetime`, `context.CurrentUtcDateTime` in JS).
- **Timeout pattern (procedure):**  
  1) Start activity task `activityTask = CallActivityAsync(...)`  
  2) Start timer `timeoutTask = CreateTimer(deadline, cts.Token)`  
  3) `winner = await Task.WhenAny(activityTask, timeoutTask)`  
  4) If activity wins: `cts.Cancel()` (cancels timer) else timeout.
- **Cancellation requirement:** if you create timers you won’t await, **cancel them**; orchestration won’t reach **“Completed”** until all outstanding tasks (incl. timers) are completed or canceled.
- **Consumption plan default:** abandoned activities still run/bill; default function timeout **5 minutes** (configurable).

</details>

### 📖 Evals API — Monitoring stored completions for regressions
**Reference Doc** · [source](https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)

*Production-ish workflow: log stored completions, create eval + runs, detect prompt regressions, iterate across prompt/model versions.*

<details>
<summary>Key content</summary>

- **Logging for later evals (production observability)**
  - Set `store=True` on `client.chat.completions.create(...)` to log requests/responses for later evaluation.
  - Alternative: enable org-wide logging “on by default” in admin data controls: `platform.openai.com/settings/organization/data-controls/data-retention`.
  - Use **metadata** to segment use-cases and versions, e.g. `metadata={"prompt_version": "v1", "usecase": "push_notifications_summarizer"}`.

- **Evals structure (configuration vs execution)**
  - **Eval** = shared configuration: `data_source_config` + `testing_criteria`.
  - **Run** = an execution of an Eval over a specific data source slice (e.g., prompt version), producing a report URL.

- **Data source config (stored completions)**
  - `data_source_config = {"type":"stored_completions","metadata":{"usecase":"push_notifications_summarizer"}}`
  - Variables exposed to graders:
    - `{{item.input}}` = messages sent to the completion call
    - `{{sample.output_text}}` = assistant response text

- **Testing criteria (LLM-as-judge label grader)**
  - Grader type: `"type": "label_model"`, model: `"o3-mini"`.
  - Labels: `["correct","incorrect"]`; passing: `["correct"]`.
  - Grader prompt judges whether summary is “concise and snappy”.

- **Run creation patterns (regression detection)**
  - Compare prompt versions by filtering stored completions:
    - Run v1: `metadata={"prompt_version":"v1"}`
    - Run v2: `metadata={"prompt_version":"v2"}`
  - Generate **new** completions for a different model using stored inputs:
    - `input_messages={"type":"item_reference","item_reference":"item.input"}`
    - `model="gpt-4o"` (vs stored `gpt-4o-mini`)

</details>

### 📖 FastAPI wiring for LangChain/LangGraph event streaming (index)
**Reference Doc** · [source](https://github.com/langchain-ai/langchain/discussions/17240)

*Community discussion hub pointing to FastAPI + “events stream API” plumbing patterns and related official how-to guides (stream runnables, debug apps, inspect runnables, stream events from tools), plus LangSmith for tracing/observability.*

<details>
<summary>Key content</summary>

- **Primary use:** A navigation/index-style discussion page for *streaming + observability* topics across LangChain/LangGraph/LangSmith.
- **Relevant procedures (as linked how-to areas):**
  - **Streaming runnables (LCEL/Runnable protocol):** guidance on streaming outputs back to clients (token streaming) and runtime configuration of runnable behavior.
  - **Inspecting/debugging:** “How to: inspect runnables” and “How to: debug your LLM apps” (intermediate state inspection / debugging workflow).
  - **Tool event streaming:** “How to: stream events from a tool” (step/event streaming hooks).
  - **Async/callback environments:** “How to: use callbacks in async environments” and “dispatch custom callback events” (observability/event emission patterns).
- **Observability rationale:** Recommends **LangSmith** as the platform to *trace, monitor, evaluate, and deploy* agents; emphasizes tracing as vital for diagnosing issues and inspecting step-level execution.
- **No equations / no numeric benchmarks / no explicit default hyperparameters** are provided in the captured text; it functions as a pointer to the concrete implementations elsewhere.

</details>

### 📖 LangGraph streaming + runtime config + persistence (thread_id)
**Reference Doc** · [source](https://github.com/langchain-ai/langgraph/discussions/702)

*Concrete config placement patterns + `stream_mode="events"` usage context; thread-level persistence/checkpointing patterns*

<details>
<summary>Key content</summary>

- **Minimal StateGraph compile/invoke pattern (hello world):**
  ```py
  from langgraph.graph import StateGraph, MessagesState, START, END

  def mock_llm(state: MessagesState):
      return {"messages": [{"role": "ai", "content": "hello world"}]}

  graph = StateGraph(MessagesState)
  graph.add_node(mock_llm)
  graph.add_edge(START, "mock_llm")
  graph.add_edge("mock_llm", END)
  graph = graph.compile()

  graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
  ```
  - **Procedure:** define node(s) → connect edges `START → node → END` → `compile()` → `invoke(input_state)`.
- **Prebuilt agent invocation pattern (ReAct-style):**
  ```py
  from langgraph.prebuilt import create_react_agent

  def get_weather(city: str) -> str:
      return f"It's always sunny in {city}!"

  agent = create_react_agent(
      model="anthropic:claude-3-7-sonnet-latest",
      tools=[get_weather],
      prompt="You are a helpful assistant",
  )

  agent.invoke({"messages": [{"role": "user", "content": "what is the weather in sf"}]})
  ```
  - **Defaults/parameters shown:** `model="anthropic:claude-3-7-sonnet-latest"`, `tools=[...]`, `prompt=...`.
- **State update rule for message history (`add_messages` reducer):**
  - Merges `left` (existing messages) and `right` (new messages).
  - **If IDs match:** message in `right` **replaces** the one in `left`.
  - **Else:** messages from `right` are **appended** (append-only history).
- **Design rationale (observability/streaming):** LangGraph emphasizes durable execution + streaming + debugging/observability (LangSmith) for tracing execution paths and state transitions.

</details>

### 📖 LangSmith Datasets — Versioning, Splits, Filtering, Eval Inputs
**Reference Doc** · [source](https://docs.langchain.com/langsmith/datasets)

*Dataset creation/versioning primitives + identifiers (versions/tags/splits/examples) used as inputs to eval automation.*

<details>
<summary>Key content</summary>

- **Core objects**
  - **Dataset** = collection of **examples** for repeatable evaluation.
  - **Example structure:**  
    - `inputs: dict` (passed to app)  
    - `reference_outputs: dict` *(optional; used for evaluation, not passed to app)*  
    - `metadata: dict` *(optional; enables filtered views)*
- **Dataset versioning (default = timestamp)**
  - Any **add/update/delete** of examples ⇒ **new dataset version** created automatically.
  - UI: **Examples** tab shows **latest** by default; selecting a past version (by timestamp) shows dataset state then; **examples are read-only** in past versions.
  - **Tests** tab shows experiments across versions (latest shown in Examples; experiments from all versions shown in Tests).
- **Tagging versions (human-readable milestones)**
  - UI: **+ Tag this version** (Examples tab).
  - SDK (Python): `client.update_dataset_tag(dataset_name=..., as_of=<timestamp>, tag="prod")`
  - Rationale: stable named versions (e.g., `"prod"`) for CI / regression testing.
- **Evaluate on a specific version / view**
  - Fetch examples for a version via `list_examples(dataset_name=..., as_of="latest" | <tag> | <timestamp>)`, then pass iterable to `evaluate/aevaluate(data=...)`.
- **Evaluate on filtered/split subsets**
  - Filter by metadata: `list_examples(dataset_name=..., metadata={"desired_key":"desired_value"})`
  - Evaluate on splits: `list_examples(dataset_name=..., splits=["test","training"])`
- **UI workflows to build datasets**
  - Add traces → dataset: from **Tracing Projects**, multi-select runs → **Add to Dataset**, or open run → **Add to → Dataset**.
  - Annotation queue: review/edit run → **Add to Dataset** (hotkey `D`); edits + run metadata carry over.
  - Playground: **Set up Evaluation** → select/create dataset → **+Row**; note: inline creation doesn’t support **nested keys**.

</details>

### 📖 LangSmith REST API — Run evals (API-only)
**Reference Doc** · [source](https://docs.langchain.com/langsmith/run-evals-api-only)

*LangSmith REST API endpoints + request/response patterns to run experiments/evals without SDKs (auth headers, dataset/session/run/feedback schema)*

<details>
<summary>Key content</summary>

- **Auth (all requests):** HTTP header `x-api-key: $LANGSMITH_API_KEY`.
- **Core workflow (single experiment/session):**
  1. **Fetch dataset examples** (filter by dataset id):  
     `GET https://api.smith.langchain.com/api/v1/examples` with query `dataset=<dataset_id>`.
  2. **Create experiment = tracer session** (ties runs to dataset):  
     `POST /api/v1/sessions` JSON:  
     - `start_time` (ISO8601 UTC), `reference_dataset_id` (string)  
     - optional: `name`, `description`, `extra.metadata`  
     Response includes `id` = `experiment_id`.
  3. **Create runs for each example** (you must do parent/child + linking):  
     `POST /api/v1/runs` JSON fields:  
     - `id` (uuid hex), `name`, `run_type` (e.g., `"chain"`, `"llm"`)  
     - `inputs` (object), `start_time` (ISO8601 UTC)  
     - **Required for experiments:** `reference_example_id` (example id), `session_id` (experiment id)  
     - optional: `parent_run_id` (to form hierarchy).
  4. **Update/close runs with outputs:**  
     `PATCH /api/v1/runs/{run_id}` JSON: `outputs` (object), `end_time` (ISO8601 UTC).
  5. **Close experiment/session:**  
     `PATCH /api/v1/sessions/{session_id}` JSON: `end_time` (ISO8601 UTC).
- **Add evaluation feedback (scoring):**
  - Query root runs: `POST /api/v1/runs/query` JSON:  
    `session: [experiment_id]`, `is_root: true`, `select: ["id","reference_example_id","outputs"]`.
  - Create feedback: `POST /api/v1/feedback` JSON:  
    `run_id`, `key` (e.g., `"correctness"`), `score` (e.g., `1.0`/`0.0`), optional `comment`.
- **Pairwise/comparative experiments:**
  - Create: `POST /api/v1/datasets/comparative` JSON:  
    `experiment_ids` (list), `reference_dataset_id`, `name`, optional `description`, `extra.metadata`.
  - Fetch: `GET /api/v1/datasets/{dataset_id}/comparative` with `id=<comparative_experiment_id>`.
  - Rank via feedback: `POST /api/v1/feedback` with `key:"ranked_preference"`, `score` (1 preferred else 0), plus `feedback_group_id` and `comparative_experiment_id`.

</details>

### 📖 LangSmith/LangGraph Streaming API (runs + threads)
**Reference Doc** · [source](https://docs.langchain.com/langsmith/streaming)

*Official streaming primitives/modes and how streamed outputs map to runs/threads for tracing & observability*

<details>
<summary>Key content</summary>

- **Core workflow (run streaming):**
  1) `client = get_client(url=<DEPLOYMENT_URL>, api_key=<API_KEY>)`  
  2) (Stateful) `thread = await client.threads.create()` → `thread_id = thread["thread_id"]`  
  3) Stream a run:  
     `async for chunk in client.runs.stream(thread_id, assistant_id, input=inputs, stream_mode="updates"): print(chunk.data)`
- **Stateless run:** pass `None` instead of `thread_id` to avoid persisting outputs in the checkpointer DB:  
  `client.runs.stream(None, assistant_id, input=inputs, stream_mode="updates")`
- **Stream modes (run streaming):**
  - `values`: full graph state after each **super-step** (`.stream()`/`.astream()` with `stream_mode="values"`)
  - `updates`: state **updates** after each step; if multiple updates in same step (e.g., multiple nodes), streamed separately
  - `messages-tuple`: **token-by-token** LLM output + metadata (for chat UIs)
  - `debug`: “as much information as possible” incl. node name + full state
  - `custom`: user-defined streamed data from inside graph
  - `events`: all events (incl. state); mainly for migrating large LCEL apps (`.astream_events()`)
- **Multi-mode streaming:** `stream_mode=["updates","custom"]` → outputs are tuples `(mode, chunk)`.
- **Subgraph streaming:** set `stream_subgraphs=True` to include parent + subgraph outputs.
- **Token streaming shape (`messages-tuple`):** `chunk.data == (message_chunk, metadata)`; example filters `chunk.event != "messages"`. Print `message_chunk["content"]`. Metadata includes node/LLM invocation details (e.g., `langgraph_node`).
- **Join existing run:** `client.runs.join_stream(thread_id, run_id)`; **outputs not buffered** (miss earlier output).
- **Thread streaming vs run streaming (comparison table):**
  - Methods: `client.threads.join_stream()` vs `client.runs.stream()`
  - REST: `GET /threads/{thread_id}/stream` vs `POST /threads/{thread_id}/runs/stream`
  - Scope: all runs on thread vs single run; lifetime: indefinite vs closes on completion; creates run: no vs yes.
- **Thread stream modes:** `run_modes` (default; equivalent to run stream output), `lifecycle` (only run start/end). Example: `stream_mode=["lifecycle","state_update"]`.
- **Resumability (thread streams):** use `Last-Event-ID` / `last_event_id="<LAST_EVENT_ID>"`; pass `"-"` to replay from beginning.

</details>

### 📖 OTel Tracing SDK essentials (sampling + processors/exporters)
**Reference Doc** · [source](https://opentelemetry.io/docs/specs/otel/trace/sdk/)

*Canonical SDK semantics for span recording vs sampling, parent-based sampling, span processors/exporters, defaults.*

<details>
<summary>Key content</summary>

- **Two gating signals for data flow**
  - `Span.IsRecording` (bool): if `false`, span discards attributes/events/status; **SpanProcessors MUST receive only spans with `IsRecording=true`**.
  - `SpanContext.TraceFlags.Sampled` (bool): propagated to children; indicates span will be exported; **SpanExporters MUST receive spans only when `Sampled=true`**.
  - **Forbidden combo:** `Sampled=true` & `IsRecording=false` **MUST NOT be allowed** (would create trace gaps).
- **Recording/Sampled reaction table**
  - `IsRecording=true, Sampled=true` → Processor: yes; Exporter: yes  
  - `IsRecording=true, Sampled=false` → Processor: yes; Exporter: no  
  - `IsRecording=false, Sampled=false` → Processor: no; Exporter: no
- **SDK span creation procedure (ordered)**
  1) Use parent trace ID if valid else generate new trace ID (**before** sampling).  
  2) Call `Sampler.ShouldSample(...)`.  
  3) Generate new span ID **regardless** of sampling decision.  
  4) Create recording/non-recording span per decision (`DROP`, `RECORD_ONLY`, `RECORD_AND_SAMPLE`).
- **Sampler API**
  - `ShouldSample(parentContext, traceId, name, kind, attributes, links) -> SamplingResult`
  - Decisions: `DROP` (IsRecording=false), `RECORD_ONLY` (IsRecording=true, Sampled=false), `RECORD_AND_SAMPLE` (IsRecording=true, Sampled=true).
- **Built-in sampler defaults**
  - **Default sampler:** `ParentBased(root=AlwaysOn)`.
  - `ParentBased` routing (defaults): remote/local parent sampled→`AlwaysOn`; not sampled→`AlwaysOff`.
- **BatchSpanProcessor defaults**
  - `maxQueueSize=2048`, `scheduledDelayMillis=5000`, `exportTimeoutMillis=30000`, `maxExportBatchSize=512` (≤ queue).
- **Span limits defaults**
  - `EventCountLimit=128`, `LinkCountLimit=128`, `AttributePerEventCountLimit=128`, `AttributePerLinkCountLimit=128`.

</details>

### 📖 Okapi BM25 (Probabilistic Relevance Framework)
**Reference Doc** · [source](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf)

*BM25 scoring formula + parameter meanings (k1, b), IDF term, length normalization*

<details>
<summary>Key content</summary>

- **BM25 ranking score (Eq. BM25):**  
  \[
  RSV_{BM25}(d,q)=\sum_{i\in q} \log\frac{N}{df_i}\cdot \frac{(k_1+1)\,tf_i}{k_1\left((1-b)+b\frac{dl}{avdl}\right)+tf_i}
  \]
  - \(N\): number of documents in collection  
  - \(df_i\): document frequency of term \(i\)  
  - \(tf_i\): term frequency of term \(i\) in document \(d\)  
  - \(dl\): document length (often \(dl=\sum_{i\in V} tf_i\))  
  - \(avdl\): average document length in collection  
  - \(k_1\): term-frequency saturation control  
  - \(b\in[0,1]\): length normalization strength
- **Length normalization component (Eq. B):**  
  \[
  B=(1-b)+b\frac{dl}{avdl}
  \]
  and normalized term frequency \(t'_f=tf/B\).
- **Parameter interpretations + defaults:**  
  - \(k_1=0\) → binary model; large \(k_1\) → approaches raw \(tf\).  
  - \(b=0\) → no length norm; \(b=1\) → full relative-frequency scaling.  
  - Typical settings: \(k_1\approx 1.2\text{–}2\), \(b\approx 0.75\).
- **Design rationale:** BM25 approximates a probabilistic “2-Poisson/eliteness” view with a **saturating tf curve** (bounded contribution vs unbounded tf-idf), plus **partial** length normalization to balance verbosity vs scope.
- **Empirical comparison (machine learning query example, \(k_1=2\)):**  
  - doc1: learning=1024, machine=1 → BM25: \(7\cdot3 + 10\cdot1 = 31\)  
  - doc2: learning=16, machine=8 → BM25: \(7\cdot2.67 + 10\cdot2.4 = 42.7\)  
  (tf-idf ranks doc1 higher: 87 vs 75)

</details>

### 📖 OpenAI API Streaming (Responses + Events)
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/streaming)

*Parameter-level reference for enabling streaming + event framing/lifecycle*

<details>
<summary>Key content</summary>

- **Default behavior:** API returns the model’s **entire output in one HTTP response** (non-streaming). Streaming reduces perceived latency by sending partial output as it’s generated.
- **Enable streaming (Responses endpoint):** set **`stream: true`** (JS) / **`stream=True`** (Python) in `client.responses.create(...)`.  
  **Procedure:**  
  1) Call `responses.create(..., stream=true)`  
  2) Iterate events (`for await (const event of stream)` / `for event in stream`)  
  3) Route by `event.type` (SDK events are typed; `type` property identifies schema).
- **Streaming model:** Responses API streams **semantic, typed events** (type-safe). Example union includes:  
  `response.created`, `response.in_progress`, `response.failed`, `response.completed`,  
  `response.output_text.delta`, `response.text.done`, `error`, plus tool-related deltas (e.g., `response.function_call_arguments.delta/done`, file search and code interpreter progress events).
- **Common text-stream events to listen for:**  
  - `response.created` (once)  
  - `response.output_text.delta` (many; incremental text)  
  - `response.completed` (once; end-of-stream)  
  - `error`
- **Chat Completions streaming:** also supports `stream=True`, returning **data-only SSE chunks**; iterate chunks and read `chunk.choices[0].delta`.
- **Design rationale:** OpenAI recommends **Responses API for streaming** because it’s “designed with streaming in mind” and uses semantic, type-safe events.
- **Production constraint:** **Moderation risk**—streaming partial output is harder to moderate; partial completions may be difficult to evaluate.

</details>

### 📖 Reliable streaming + efficient state management (LangGraph)
**Reference Doc** · [source](https://changelog.langchain.com/announcements/reliable-streaming-and-efficient-state-management-in-langgraph)

*Release-level guarantees/behavior changes for “reliable streaming” + “efficient state management”; recommended streaming/state patterns.*

<details>
<summary>Key content</summary>

- **Release guarantees / behavior changes (LangGraph API/Cloud):**
  - Streaming runs now use the **same job queue as background runs** → **greater reliability** while keeping **low-latency real-time output**.
  - New streaming endpoint: `GET /threads/{thread_id}/runs/{run_id}/stream` and SDK: `client.runs.join_stream()` → stream output from **any run**, including **background runs** (supports UX where user leaves/returns and streaming continues).
  - Final state retrieval now reliable: `GET /threads/{thread_id}/runs/{run_id}/join` and SDK: `client.runs.join()` → **reliably returns final state values** whether run is ongoing or finished.
  - Thread status expanded: `GET /threads/{id}` / `client.threads.get()` now includes **`error`** and **`interrupted`** (in addition to existing **`idle`**, **`busy`**).
  - Streamlined state retrieval: `GET /threads/{id}` and `GET /threads` now include **latest state values** (fewer API calls; no separate “get state”).
  - Advanced search: `POST /threads/search` / `client.threads.search()` can filter by **thread state values** + status (enables “agent inbox” UIs).
- **Streaming procedures (graph runtime):**
  - Use `graph.stream(...)` / `graph.astream(...)` with `stream_mode` and **`version="v2"`** for unified StreamPart format.
  - Stream modes (table):  
    - `values`: full state snapshot after each step  
    - `updates`: only changed keys; **multiple updates in same step streamed separately**  
    - `messages`: `(message_chunk, metadata)` from LLM calls (**emitted even if model invoked via `.invoke`**)  
    - `custom`: arbitrary events via `get_stream_writer()` / injected `writer` arg  
    - `checkpoints`: checkpoint events (same format as `get_state()`; **requires checkpointer**)  
    - `debug`: “as much info as possible” incl. node name + full state
  - Subgraph streaming: pass `subgraphs=True`; streamed parts include `ns` namespace to distinguish root vs subgraph.

</details>

### 📖 Responses API SSE Streaming Events (event types + payload fields)
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/responses-streaming)

*Exact streaming (SSE/WebSocket) event names + object fields for incremental output, tool-call deltas, and lifecycle/error events in the Responses API.*

<details>
<summary>Key content</summary>

- **Streaming model:** server emits a sequence of **ResponseStreamEvent** objects (also called **ResponsesServerEvent** for WebSocket). Each event includes:
  - `type` (event name discriminator)
  - often `sequence_number`
  - often `output_index`, `item_id`, and sometimes `content_index` for locating the delta within the response.
- **Lifecycle/status events (ResponseStatus):** `queued`, `in_progress`, `completed`, `failed`, `cancelled`, `incomplete`.
  - `response.created`: **ResponseCreatedEvent** `{ type, sequence_number, response }`
  - `response.queued`: **ResponseQueuedEvent** `{ type, sequence_number, response }`
  - `response.in_progress`: **ResponseInProgressEvent** `{ type, sequence_number, response }`
  - `response.completed`: **ResponseCompletedEvent** `{ type, sequence_number, response }`
  - `response.failed`: **ResponseFailedEvent** `{ type, sequence_number, response }`
  - `response.incomplete`: **ResponseIncompleteEvent** `{ type, sequence_number, response }`
  - `response.error`: **ResponseErrorEvent** `{ type, code, message, param, … }`
- **Incremental text output:**
  - `response.output_text.delta`: **ResponseTextDeltaEvent** `{ type, sequence_number, output_index, item_id, content_index, delta }`
  - `response.output_text.done`: **ResponseTextDoneEvent** `{ type, sequence_number, output_index, item_id, content_index, logprobs, … }`
  - Content-part boundaries: **ResponseContentPartAddedEvent**, **ResponseContentPartDoneEvent** (include `output_index`, `item_id`, `content_index`, …).
  - Output-item boundaries: **ResponseOutputItemAddedEvent**, **ResponseOutputItemDoneEvent** `{ type, sequence_number, output_index, item }`.
- **Tool-call streaming (arguments/code/input deltas + done):**
  - Function calls: **ResponseFunctionCallArgumentsDeltaEvent** `{ delta, item_id, output_index, … }`; **…DoneEvent** `{ arguments, name, item_id, output_index, … }`
  - Custom tool input: **ResponseCustomToolCallInputDeltaEvent** / **…DoneEvent** (`delta` → final `input`)
  - MCP tool args: **ResponseMcpCallArgumentsDeltaEvent** / **…DoneEvent** (`delta` → final `arguments`)
  - Code interpreter code: **ResponseCodeInterpreterCallCodeDeltaEvent** / **…DoneEvent** (`delta` → final `code`) plus state events: **…InProgress**, **…Interpreting**, **…Completed**
  - Search tools: web/file search state events **…InProgress**, **…Searching**, **…Completed**
  - Image generation: **…InProgress**, **…Generating**, **…PartialImage** (`partial_image_b64`), **…Completed**
- **Audio streaming:** **ResponseAudioDeltaEvent** (`delta`), **ResponseAudioDoneEvent**; transcript: **ResponseAudioTranscriptDeltaEvent** (`delta`), **…DoneEvent**.
- **Refusals & reasoning summaries:** refusal delta/done (**ResponseRefusalDeltaEvent**, **ResponseRefusalDoneEvent**); reasoning summary part/text delta/done events.
- **Include extra data via `include[]` (ResponseIncludable):**
  - `web_search_call.action.sources`, `web_search_call.results`, `file_search_call.results`,
  - `code_interpreter_call.outputs`, `computer_call_output.output.image_url`,
  - `message.input_image.image_url`, `message.output_text.logprobs`,
  - `reasoning.encrypted_content`.
- **Text output formatting defaults:** `ResponseTextConfig.format` default is `{ "type": "text" }`. Structured Outputs via `{ "type": "json_schema" }` (preferred over `{ "type": "json_object" }` for newer models).

</details>

### 📖 Stream only the final node’s output (LangGraph `streamEvents`)
**Reference Doc** · [source](https://github.com/langchain-ai/langgraphjs/issues/320)

*Event filtering/selection patterns (node-level filtering) for streaming/debugging*

<details>
<summary>Key content</summary>

- **Problem:** In a multi-node LangGraph (e.g., RAG graph with a query-rewrite node then a generation node), the user wants to **stream tokens only from the last/generation node**, not earlier nodes.
- **Baseline streaming loop (JS):**
  - Create event stream:  
    `const eventStream = await graph.streamEvents(inputs, config);`
  - Consume events:  
    `for await (const { event, data } of eventStream) { ... }`
  - Token streaming event type used in example:  
    `event === "on_chat_model_stream"`
  - Accumulate streamed text when chunk content is a string:  
    `if (typeof data.chunk.content === "string") result += data.chunk.content;`
- **Key filtering mechanism (design rationale):**
  - **Events include metadata** that can identify **which node** produced the event (“metadata containing information about the node that it's within”).
  - A common practice is to use **tagging** to **narrow which events are published/handled**, instead of maintaining a manual `currentNode` state variable.
- **Canonical procedure reference:** Maintainer points to an official how-to demonstrating **streaming outputs from the final node** (Python example):  
  https://langchain-ai.github.io/langgraph/how-tos/streaming-from-final-node/#stream-outputs-from-the-final-node  
  (Use this for the concrete pattern; this issue establishes that node metadata/tags are the intended approach.)

</details>

### 📖 Structured outputs / JSON mode (doc index only)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/structured-outputs/json-mode)

*Enforcing JSON outputs via `response_format` / JSON mode; schema/format constraints; failure modes & guardrails.*

<details>
<summary>Key content</summary>

- **This fetch contains no structured-output guidance.** The target URL returns **HTTP 404: Not Found** and displays a “Page not found” screen.
- **Available actionable items are navigation pointers** to the current docs locations:
  - “Structured output” guide: `https://platform.openai.com/api/docs/guides/structured-outputs`
  - “Function calling” guide: `https://platform.openai.com/api/docs/guides/function-calling`
  - “Responses API” migration guide: `https://platform.openai.com/api/docs/guides/migrate-to-responses`
  - “Using tools” guide: `https://platform.openai.com/api/docs/guides/tools`
- **No equations, parameters, schemas, or step-by-step procedures** for `response_format` / JSON mode appear in the provided text (only site navigation and doc section listings).
- **Design rationale / defaults / failure modes:** not present in this excerpt; consult the linked “Structured output” guide above for the authoritative details.

</details>

### 📖 Temporal Activity Operations (Pause/Unpause/Reset/Update Options)
**Reference Doc** · [source](https://docs.temporal.io/activity-operations)

*Operational controls for Activity Executions + effects on retries/timeouts/heartbeats + observability limits*

<details>
<summary>Key content</summary>

- **Scope/availability**
  - Applies to **Activity Executions** (not lifecycle behaviors). **Not for Local or Standalone Activities**.
  - **Public Preview**; available in **Server v1.28.0+**; self-hosted UI requires **v2.47.0+**.
  - **Not available as SDK client methods**; use **CLI/UI/gRPC**.
- **Pause (`temporal activity pause`)**
  - **Stops server-side scheduling of new retries**; parent Workflow keeps running (Signals/Queries/Updates unaffected).
  - **Heartbeat semantics:** with Heartbeat → interrupted on next Heartbeat (SDK raises pause-specific error); without Heartbeat → continues to completion; if it fails, **no retry scheduled**.
  - **Does not stop/extend Schedule-To-Close timeout**; may still time out → use **update-options** to adjust.
  - **Idempotent**; pausing completed Activity errors.
- **Unpause (`temporal activity unpause`)**
  - Reschedules **immediately**; **discard remaining retry backoff**.
  - **Attempts + Heartbeat data preserved by default**; optional `--reset-attempts`, `--reset-heartbeats`.
  - Doesn’t override **Workflow Pause**; both must be unpaused.
- **Reset (`temporal activity reset`)**
  - Clears retry state: **attempt resets to 1**, **backoff discarded**, rescheduled immediately.
  - If paused, Reset **also unpauses** unless `--keep-paused`.
  - Heartbeat: with Heartbeat → interrupted on next Heartbeat (reset-specific error); without Heartbeat → no interruption/concurrent run; if attempt>1, service **rejects current result** due to attempt mismatch; new execution after **Start-To-Close** expires.
  - `--restore-original-options` reverts timeouts/Retry Policy/Task Queue to original.
- **Update Options (`temporal activity update-options`)**
  - Change **timeouts** (Schedule-To-Close, Start-To-Close, Schedule-To-Start, Heartbeat), **Retry Policy** (initial interval, max interval, backoff coefficient, max attempts), **Task Queue**.
  - If waiting to retry → takes effect immediately (retry timer regenerated). If running → stored for **next execution**. If paused → stored; applies on unpause.
  - `--restore-original-options` works **only with `--query`** (batch); ignored in single-workflow mode.
- **Observability/audit**
  - Operations **do not create Workflow Event History events**; Workflow code/replay/tools reading history can’t detect them.
  - Check state via `temporal workflow describe` (paused flag, attempt, last failure) or UI (who/when/why). No namespace-wide query for paused activities; must know Workflow Id.

</details>

### 📖 Temporal Activity Retries — RetryPolicy defaults & backoff
**Reference Doc** · [source](https://docs.temporal.io/activities#activity-retries)

*Exact RetryPolicy fields + default retry behavior (Activities vs Workflows)*

<details>
<summary>Key content</summary>

- **Default retry behavior**
  - **Activities retry automatically by default** with exponential backoff until **success or cancellation**.
  - **Workflow Executions do not retry by default** (no default Retry Policy attached).
  - **Retry Policies do not apply to Workflow Task Executions**; Workflow Tasks retry until Workflow Execution Timeout (unlimited by default) with exponential backoff and **max interval 10 minutes**.
- **RetryPolicy fields (exact names)**
  - `initialInterval`, `backoffCoefficient`, `maximumInterval`, `maximumAttempts`, `nonRetryableErrorTypes`.
- **Default RetryPolicy values (Properties → Default values)**
  - `initialInterval` = **1s**
  - `backoffCoefficient` = **2.0**
  - `maximumInterval` = **100 × initialInterval** (=> **100s** with defaults)
  - `maximumAttempts` = **∞** (unlimited); **0 also means unlimited**, **1 means no retries**, negative => error
  - `nonRetryableErrorTypes` = **[]** (none)
- **Retry interval formula (Retry interval section, Eq. 1)**
  - `retryInterval = min( initialInterval * (backoffCoefficient ^ retries), maximumInterval )`
  - where `retries` = number of retries already attempted (0 for first retry delay).
- **Procedure: what happens on Activity retry**
  1. Activity fails → service evaluates Retry Policy (attempt count, error type) and computes backoff.
  2. If retryable: schedules a new Activity Task after backoff (new Activity Task Execution).
  3. If not retryable / attempts exceeded: Activity fails and error is returned.
- **Override mechanism**
  - An **Application Failure** can set a **“next Retry delay”** that overrides the computed interval, but still respects `maximumAttempts` and overall timeouts (Activity **Schedule-to-Close**, Workflow **Execution Timeout**).
- **Design rationale**
  - Prefer retrying **failed Activities** (failure-prone external ops) vs retrying whole Workflows (deterministic replay; retrying often repeats same failure and wastes resources).

</details>

### 📖 Temporal Workflow History Event Types (Authoritative)
**Reference Doc** · [source](https://docs.temporal.io/reference/events)

*Exact Temporal event type names + meanings/fields for Workflow Execution Event History (debugging/auditing/determinism)*

<details>
<summary>Key content</summary>

- **Event history basics:** Events are created by the **Temporal Service** in response to (a) external occurrences and (b) **Commands** generated by a Workflow Execution.
- **Workflow lifecycle (terminal + key):**
  - `WorkflowExecutionStarted` (**always first event**). Key fields: `workflow_type`, `task_queue`, `input`, timeouts (`workflow_execution_timeout`, `workflow_run_timeout`, `workflow_task_timeout`), `retry_policy`, `attempt`, `cron_schedule`, `continued_execution_run_id`, `identity`, `memo`, `search_attributes`.
  - Terminal outcomes: `WorkflowExecutionCompleted` (`result`), `WorkflowExecutionFailed` (`failure`, `retry_state`), `WorkflowExecutionTimedOut` (`retry_state`), `WorkflowExecutionCanceled` (`details`), `WorkflowExecutionTerminated` (`reason`, `details`).
  - Control-flow: `WorkflowExecutionCancelRequested` (`cause`, `identity`), `WorkflowExecutionSignaled` (`signal_name`, `input`, `identity`), `WorkflowExecutionContinuedAsNew` (`new_execution_run_id`, `input`, `backoff_start_interval`, timeouts), `WorkflowExecutionOptionsUpdated` (versioning override, attached request id, completion callbacks).
- **Workflow Task (WFT) progression:** `WorkflowTaskScheduled` → `WorkflowTaskStarted` → `WorkflowTaskCompleted`; failure modes: `WorkflowTaskTimedOut` (`timeout_type`), `WorkflowTaskFailed` (often **non-determinism**; also used by **reset** with `base_run_id`, `new_run_id`, `fork_event_version`).
- **Activity progression:** `ActivityTaskScheduled` (timeouts: `schedule_to_close_timeout`, `schedule_to_start_timeout`, `start_to_close_timeout`, `heartbeat_timeout`, plus `retry_policy`) → `ActivityTaskStarted` (written to history only when terminal event occurs) → terminal: `ActivityTaskCompleted`/`ActivityTaskFailed` (`retry_state`)/`ActivityTaskTimedOut` (`timeout_type`) / cancel: `ActivityTaskCancelRequested` → `ActivityTaskCanceled`.
- **Other primitives:** Timers (`TimerStarted`/`TimerFired`/`TimerCanceled`), markers (`MarkerRecorded` is server-transparent), child workflows (initiate/start/complete/fail/cancel/timeout/terminate), external cancel/signal initiation + failure events, search attribute upserts (`UpsertWorkflowSearchAttributes`), Updates (`WorkflowExecutionUpdateAcceptedEvent`, `WorkflowExecutionUpdateCompletedEvent`), Nexus ops (`NexusOperationScheduled/Started/Completed/Failed/TimedOut/CancelRequested/Canceled`).

</details>

### 📖 Temporal Workflow timeouts (Execution/Run/Task) — definitions, defaults, API params
**Reference Doc** · [source](https://docs.temporal.io/workflows#workflow-timeouts)

*Workflow-level timeout semantics + parameter names; contrast with Activity timeouts*

<details>
<summary>Key content</summary>

- **General guidance (design rationale):**
  - Temporal **generally does not recommend setting Workflow Timeouts** because Workflows are **long-running/resilient**; timeouts can **limit ability to handle delays**.
  - For “do something after X time” **inside** a Workflow, prefer a **Timer** (durable sleep managed by Temporal service), not Workflow timeouts.

- **Where configured (procedure/API):**
  - Set at Workflow start via `client.start_workflow()` or `client.execute_workflow()`.
  - Timeout parameter names: `execution_timeout`, `run_timeout`, `task_timeout`.
  - Example (Python):  
    `await client.execute_workflow(..., execution_timeout=timedelta(seconds=2), run_timeout=..., task_timeout=...)`

- **Workflow timeout types (definitions + defaults):**
  - **Workflow Execution Timeout**: max time a Workflow Execution can be **Open**, **including retries and Continue-As-New**.  
    - **Default:** `∞` (infinite).  
    - On reach: Execution becomes **Timed Out**.  
    - Common use: limit total duration of a **Temporal Cron Job** over time.
  - **Workflow Run Timeout**: max duration of a **single Run** (one Run ID) within an Execution; **excludes retries/Continue-As-New**.  
    - **Default:** same as **Execution Timeout**.  
    - On reach: Execution becomes **Timed Out**.  
    - Constraint: **cannot be greater than** Execution Timeout.
  - **Workflow Task Timeout**: max time a Worker may execute a **Workflow Task** after pulling from Task Queue (detect Worker down / recovery).  
    - **Default:** **10s**; **max:** **120s**.  
    - Increase only if large history load needs >10s; not recommended beyond default.

- **Observability/troubleshooting:**
  - Use Search Attribute **`TemporalReportedProblems`** to find Workflows with **failed Workflow Tasks**; a failed Workflow Task **does not fail** the Workflow but can prevent completion if unhandled.

</details>

### 📖 `stream_mode="updates"` can miss tool messages when tools return `Command`
**Reference Doc** · [source](https://github.com/langchain-ai/langgraph/issues/2831)

*Edge-case semantics for `stream_mode="updates"` with multi-tool calls + tools returning `Command(update=...)`*

<details>
<summary>Key content</summary>

- **Repro setup (LangGraph ReAct agent):**
  - Build tools `add` and `sub`; create agent via `create_react_agent(model, tools=tools, checkpointer=MemorySaver())`.
  - Stream with:
    - `agent.stream(input={"messages":[("user","add(1,1), add(1,2), add(1,3) at once")]}, config={"configurable":{"thread_id":"1"}}, stream_mode="updates")`
- **Tool return patterns compared:**
  - `add` tool returns a **Command**:
    - **Eq. 1 (Command update):**  
      `Command(update={"messages":[ToolMessage(f"add result: {result}", tool_call_id=tool_call_id)]})`  
      where `result = a + b`, and `tool_call_id` is injected via `Annotated[str, InjectedToolCallId]`.
  - `sub` tool returns a **plain string**: `return f"sub result: {result}"` (note: code shows `result = a + b` even though tool is named `sub`).
- **Observed streaming behavior (empirical):**
  - When the LLM issues **multiple tool calls at once** (3 `add` calls), `stream_mode="updates"` emits:
    - an `agent` update containing **3 tool_calls**,
    - then a `tools` update containing **only 1 ToolMessage**: `add result: 4` (the last call’s message),
    - then final `agent` response.
  - For `sub` (string return), the `tools` update contains **all 3 ToolMessages** in one chunk: `sub result: 2`, `sub result: 3`, `sub result: 4`.
- **State vs stream discrepancy:**
  - `agent.get_state(config).values["messages"]` shows **all ToolMessages** for `add` (2, 3, 4) even though streaming only showed the last one.

</details>

### 📖 lm-eval Harness Interface (CLI + Python API)
**Reference Doc** · [source](https://github.com/EleutherAI/lm-evaluation-harness/blob/big-refactor/docs/interface.md)

*CLI argument surface + equivalent `simple_evaluate()` kwargs for standardized eval runs*

<details>
<summary>Key content</summary>

- **Primary invocation:** run via `python -m lm_eval` or `lm-eval` CLI entrypoint; flags viewable with `-h/--help`.
- **Model selection**
  - `--model <string>`: model type/provider name (must match enabled names list in main README).
  - `--model_args "arg1=val1,arg2=val2,..."`: comma-separated kwargs passed to model constructor (example: `pretrained=EleutherAI/pythia-160m,dtype=float32`).
- **Task selection & prompting**
  - `--tasks "t1,t2,group1,..."`: comma-separated task and/or task-group names (must be valid).
  - `--num_fewshot <int>`: number of few-shot examples inserted into context.
- **Generation controls**
  - `--gen_kwargs "k=v,..."`: kwargs passed to `generate_until` tasks (e.g., `temperature`, `top_p`, `top_k`); applies to **all** `generate_until` tasks in the run (no per-task overrides via CLI; per-task control via task YAML).
- **Batching & device**
  - `--batch_size <int|auto|auto:N>`: fixed batch size or auto-fit; `auto:N` re-finds max batch size **N times** during eval (helps because docs are sorted by descending context length).
  - `--max_batch_size <int>`: cap when using `--batch_size auto`.
  - `--device <string>`: e.g., `cuda` (default), `cuda:0`, `cpu`, `mps`.
- **Outputs & observability**
  - `--output_path dir/file.jsonl|dir/`: save high-level results; if `--log_samples`, also saves per-document outputs/metrics into directory.
  - `--log_samples`: requires `--output_path`; logs model inputs/outputs per document.
- **Debugging/repro**
  - `--limit <int|float 0.0–1.0>`: evaluate first X docs or first X% per task.
  - `--use_cache /path/to/sqlite_cache_`: creates per-process caches `/path/to/sqlite_cache_rank{i}.db`.
  - `--check_integrity`: run task tests.
  - `--write_out`: print prompt + gold target for first doc of each task.
  - `--show_config`: print full `TaskConfig` (incl. non-default YAML settings).
  - `--include_path <folder>`: add external YAML task configs to registry.
- **Python API workflow**
  1. Implement an `lm_eval.api.model.LM` subclass (`loglikelihood`, `loglikelihood_rolling`, `generate_until`).
  2. Register tasks: `lm_eval.tasks.initialize_tasks()` or `include_path(...)`.
  3. Call `lm_eval.simple_evaluate(model=lm_obj, tasks=[...], num_fewshot=..., ...)` (kwargs mirror CLI flags).
  - `lm_eval.evaluate()` provides core functionality with less abstraction than `simple_evaluate()`.

</details>

### 📋 # Source: https://arize.com/docs/phoenix/resources/frequently-asked-questions/open-source-langsmith-alternative-arize-phoenix-vs.-langsmith
**Source** · 

### 📋 # Source: https://docs.anthropic.com/ja/docs/agents-and-tools/tool-use/fine-grained-tool-streaming
**Source** · 

### 📋 # Source: https://docs.langchain.com/langsmith/evaluation
**Source** · 

### 📋 # Source: https://docs.langchain.com/langsmith/trace-with-api
**Source** · 

### 📋 # Source: https://docs.temporal.io/ai-cookbook/human-in-the-loop-python
**Source** · 

### 📋 # Source: https://docs.temporal.io/encyclopedia/event-history/event-history-python
**Source** · 

### 📋 # Source: https://github.com/langchain-ai/langgraphjs/issues/1482
**Source** · 

### 📋 # Source: https://github.com/langchain-ai/langgraphjs/issues/318
**Source** · 

### 📋 LangGraph Agent Streaming via FastAPI WebSocket (Repo Scaffold)
**Code** · [source](https://github.com/sheikhhanif/LangGraph_Streaming)

*Runnable FastAPI server scaffold showing LangGraph Agent + real-time streaming “tokens” (words) over WebSocket; practical place to add redaction/sanitization and observability hooks.*

<details>
<summary>Key content</summary>

- **End-to-end architecture (repo intent):**
  - **LangGraph Agent** used to build a **stateful, multi-actor** LLM application; coordinates and checkpoints multiple chains/actors across **cyclic computational steps** using regular Python functions.
  - **FastAPI** provides the HTTP server framework (high-performance, auto API docs).
  - **WebSocket** used for **real-time, bidirectional** low-latency streaming to a web UI.
- **Streaming behavior (important implementation detail):**
  - “Streaming Tokens” feature is **ChatGPT-like word streaming**: **not raw token streaming**; **tokens are converted to words before displaying in the web UI**.
- **Tooling/agent extensibility:**
  - Agent is created with LangGraph and **has access to one tool** by default in this example; design explicitly supports integrating **many tools**.
- **Design rationale (as stated):**
  - WebSocket chosen to ensure **low-latency data exchange** and interactive UX.
  - LangGraph chosen for **coordination + checkpointing** across iterative/cyclic steps (Pregel/Apache Beam-inspired; NetworkX-like interface).
- **Repo structure (for quick navigation):**
  - Key files: `main.py` (FastAPI entry), `assistant.py` (agent logic), plus `static/` (web UI assets), `docs/`, `README.md`.
- **Empirical/config values:** none stated in the provided excerpt (no hyperparameters, ports, or numeric benchmarks).

</details>

### 🔍 LangGraph runtime + streaming modes (Pregel/BSP)
**Explainer** · [source](https://blog.langchain.com/building-langgraph/)

*Design rationale for LangGraph’s runtime (graph execution model + why streaming exists) and concrete `graph.stream`/`graph.astream` pattern via `stream_mode` values.*

<details>
<summary>Key content</summary>

- **Production needs driving design (6 features):** Parallelization (reduce *actual* latency), Streaming (reduce *perceived* latency), Task queue (reliable retries), Checkpointing (cheap retries), Human-in-the-loop (interrupt/resume), Tracing (visibility into agent loops).
- **Why streaming exists (latency rationale):** LLM agents run in **seconds/minutes/hours**; when you can’t reduce true latency without harming quality, stream useful intermediate info (progress/actions) up to **token-by-token** output.
- **Runtime architecture choice (Section “Execution algorithm”):** Uses **BSP/Pregel** to support **cycles/loops** and **deterministic concurrency** (avoid data races).
- **Execution model (algorithm steps):**
  - **Channels**: named data containers with **monotonically increasing version strings**.
  - **Nodes**: functions subscribing to channels; run when subscribed channel versions change.
  - **Loop per iteration:**  
    1) Select runnable nodes by comparing channel versions vs last-seen versions.  
    2) Execute selected nodes **in parallel** with **independent state copies**.  
    3) Apply node updates to channels in a **deterministic order**, bump versions.  
    4) Halt when no nodes runnable or **max iteration steps** reached (developer-set constant).
- **Streaming implementation + modes:** Engine emits stream output **inside nodes while running** and **at step boundaries** without custom developer code. Provides **6 stream modes**: `values`, `updates`, `messages`, `tasks`, `checkpoints`, `custom`. Example guidance: chatbots → `messages`; long-running agents → `updates`.
- **Checkpoint contents (for resume-anywhere):** serialized channel values (**MsgPack by default**, optionally encrypted), version strings, and record of last-seen channel versions per node.
- **Empirical scaling table (Big-O):**
  - **Planning a step:** nodes **O(1)**, edges **O(1)**, channels **O(n)**, active nodes **O(n)**, history **O(1)**, threads **O(1)**.
  - **History length is O(1)** across start/plan/run/finish (fetch latest checkpoint; no replay).

</details>

### 📋 LangGraph streaming + state inspection patterns (SSE/WebSocket-adaptable)
**Code** · [source](https://github.com/langchain-ai/langgraph/discussions/2028)

*Concrete end-to-end patterns for streaming agent execution + inspecting intermediate state (checkpoint snapshots), suitable for adapting to SSE/WebSocket event streams.*

<details>
<summary>Key content</summary>

- **Graph “hello world” (JS/TS) procedure**
  - Define state schema with `messages: MessagesValue`.
  - Node returns state update: `return { messages: [{ role: "ai", content: "hello world" }] };`
  - Build graph: `new StateGraph(State).addNode("mock_llm", mockLlm).addEdge(START,"mock_llm").addEdge("mock_llm",END).compile();`
  - Invoke: `await graph.invoke({ messages: [{ role:"user", content:"hi!" }] });`
- **Tool-calling loop (Python) procedure**
  - State: `messages: Annotated[list, add_messages]` (reducer appends, not overwrites).
  - Bind tools: `llm_with_tools = llm.bind_tools(tools)`
  - Nodes:
    - `chatbot(state) -> {"messages":[llm_with_tools.invoke(state["messages"])]}`
    - `ToolNode(tools=[...])`
  - Control flow:
    - `add_conditional_edges("chatbot", tools_condition)` routes to tools when tool calls exist.
    - `add_edge("tools","chatbot")` returns to LLM after tool execution.
    - `add_edge(START,"chatbot")`
- **Checkpointing + intermediate state inspection**
  - Compile with checkpointer: `graph.compile(checkpointer=MemorySaver())`
  - Provide `thread_id` in `configurable` to persist/restore across calls.
  - Inspect via `StateSnapshot(...)` containing:
    - `values` (full state, incl. message history)
    - `next` (empty when at `END`)
    - `config.configurable.thread_id`, `checkpoint_id`, `checkpoint_ns`
    - `metadata.step` (example shows `step: 4`)
- **Human-in-the-loop (HIL) interrupt rationale + default constraint**
  - Tool uses `interrupt({"query": query})` and returns `human_response["data"]`.
  - **Rationale:** disable parallel tool calling to avoid repeated tool invocations on resume.
  - Enforced by: `assert len(message.tool_calls) <= 1`.

</details>

### 🔍 Predictable background coding agents via verification loops
**Explainer** · [source](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)

*Concrete production pattern: iterative verification/feedback loops (agent unaware of verifier details) to improve PR success predictability.*

<details>
<summary>Key content</summary>

- **Primary failure modes (production agent at scale):**
  1) Agent fails to produce a PR (minor; manual fallback).  
  2) PR produced but **fails CI** (frustrating; leaves half-broken code).  
  3) PR **passes CI but is functionally incorrect** (most serious; erodes trust; hard to spot across thousands of components).
- **Core procedure: “verification loop” (inner loop)**
  - Implement **strong verification loops** so the agent can **incrementally confirm** it’s on track **before committing/opening a PR**.
  - **Design principle:** agent **doesn’t know** what verification does/how; it only knows it can/must call a verification tool.
  - Loop consists of **one or more independent verifiers** that **auto-activate** based on repo contents (e.g., **Maven verifier** triggers if `pom.xml` exists at repo root).
  - Verifiers are exposed via an abstraction layer (e.g., **MCP tool definition**); **individual verifiers are not exposed directly** to the agent.
  - Verifiers run formatting/build/test and **parse noisy outputs** (often via **regex**) to return **short, relevant error messages** or a short success message.
  - System runs **all relevant verifiers before opening a PR**; in Claude Code implemented via a **stop hook**. If any verifier fails → **PR not opened**; user gets error.
- **Additional safeguard: LLM “Judge” (post-verifier)**
  - Inputs: **diff of proposed change + original prompt**; evaluated by an LLM.
  - Purpose: prevent “ambitious” out-of-scope changes (refactors, disabling flaky tests).
  - Empirics: across **thousands of agent sessions**, judge **vetoes ~25%**; when vetoed, agent **course-corrects ~50%** of the time.
- **Design rationale for predictability/security**
  - Keep agent narrowly scoped: see codebase, edit files, run verifiers only.
  - Surrounding infra handles pushing code, Slack interaction, prompt authoring.
  - Run agent **highly sandboxed** (container, limited permissions, few binaries, minimal system access).

</details>

### 🔍 Spotify “Honk” Background Coding Agent (Part 1) — Deployment Pattern
**Explainer** · [source](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)

*System-level architecture narrative for a background coding agent: how work is scoped/queued, PRs produced, and operational constraints (human review, reliability, cost).*

<details>
<summary>Key content</summary>

- **Baseline platform (Fleet Management):** Runs **source-to-source transformations as jobs** in a **containerized environment**, then **automatically opens PRs** against target repos. Historically strong for:
  - Dependency bumps (e.g., Maven **pom.xml**)
  - Config updates (deployment manifests)
  - Simple refactors (replace deprecated calls)
- **Scale/impact metrics:**
  - Since **mid-2024**, **~50% of Spotify PRs** have been automated by Fleet Management.
  - AI agents have generated **1,500+ PRs merged** into production.
  - Reported **60–90% total time savings** vs writing changes by hand (for complex migrations).
- **Why agents (design rationale):**
  - Deterministic transformation scripts become extremely complex (example: Maven dependency updater grew to **20,000+ LOC** to handle corner cases).
  - Goal: let engineers define fleet-wide changes in **natural language**, lowering expertise barrier.
- **Architecture choice:** Replace only the **transformation declaration** with an agent; keep surrounding infra unchanged (**repo targeting → PR opening → review → merge**).
- **Internal CLI (pluggable agent runner):**
  - Delegates prompt execution to an agent
  - Runs formatting/linting via **local MCP (Model Context Protocol)**
  - Uses **LLMs-as-judge** to evaluate diffs
  - Uploads logs to **GCP**
  - Captures traces in **MLflow**
  - Rationale: enables **swapping agents/LLMs** without changing user workflow.
- **Background agent workflow (Slack/GitHub):**
  1. User interacts with an **interactive agent** to gather task info
  2. Interaction produces a **prompt**
  3. Prompt handed to coding agent → **PR produced**
  - Used for ADR drafting from Slack threads; PM-proposed simple changes.
- **Operational constraints called out:** long runtimes, unpredictable outputs → need validation/quality control; plus safety, sandboxing, and cost/LLM quota management.

</details>

### 🔍 Two-layer agent architecture (LangGraph logic + Temporal durability)
**Explainer** · [source](https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics)

*Pattern: keep agent logic in LangGraph-style graphs, but use Temporal for durable execution (state persistence, retries, recovery, scaling).*

<details>
<summary>Key content</summary>

- **Use case:** “Deep research agent” for a Fortune 500 manufacturer with **100+ plants**; searches internal DBs/shared drives/repos, then expands to web if needed; **labels internal vs open-web sources** and cites sources.
- **Observed LangGraph-in-prod pain points (why migrate):**
  - Needed **robust error handling + retries** → built **custom retry/error-handling** especially for **human-in-the-loop waits**, requiring **manual state maintenance**; led to **inconsistent workflow state** and hard recovery/debugging.
  - **Redis-based state**: had to manage **lifecycle/expiration**; bugs around **expired state** were time-consuming to reproduce; caching updates could wipe common requests.
  - Scaling/exactly-once: to ensure each request processed **exactly once**, they used **Apache Kafka** + executor pool; still hit **race conditions, stale state, stuck agents**.
- **Temporal design rationale (what changed):**
  - **State becomes part of the workflow** (durably persisted in Temporal event history), not an external “baton” (Redis key). Workflow passes a **serializable state object** into each Activity; Activities return updated state.
  - **Declarative retries via `RetryPolicy`** attached to Activity execution (delete “thousands of lines” of try/catch + retry loops).
    - Example defaults shown: `initial_interval=1s`, `backoff_coefficient=2.0`, `maximum_interval=60s`, `maximum_attempts=4`; another policy `initial_interval=5s`, `backoff_coefficient=1.0`, `maximum_interval=15s`, `maximum_attempts=3`; `non_retryable_error_types` includes `ValueError` (and `TypeError` in second).
- **Scaling procedure:** run **multiple identical stateless Temporal Worker replicas** on Kubernetes polling the same task queue; Temporal handles load balancing/distribution.
- **Architectural decoupling step:** convert each LangGraph node into a **self-contained Temporal Activity** with **explicit serializable inputs/outputs**; move shared client init into Activities; optimize via **client pooling/lazy init**.

</details>

---

## Related Topics

- [[topics/scaling-laws|Scaling Laws]]
- [[topics/rlhf-alignment|RLHF & Alignment]]
- [[topics/reasoning-models|Reasoning Models]]
