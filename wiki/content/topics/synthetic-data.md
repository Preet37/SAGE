---
title: "Synthetic Data & Self-Improvement"
subject: "Large Language Models"
date: 2026-04-09
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Synthetic Data

## Video (best)
- **Andrej Karpathy** — "State of GPT"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=bZQun8Y4L2A)
- Why: Clear, practitioner-oriented overview of how modern LLM training pipelines use curated data mixtures (including synthetic data) and why data quality matters.
- Level: Intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "Constitutional AI: Harmlessness from AI Feedback"
- Why: Strong written explanation of Constitutional AI, including how synthetic preference/critique data can be generated and used to steer model behavior.
- Level: Intermediate
- **Link:** [https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)
## Deep dive
- **Stanford CRFM** — "Self-Instruct: Aligning Language Models with Self-Generated Instructions"
- Why: Canonical deep dive into *self-instruct* style synthetic instruction generation, filtering, and iterative bootstrapping.
- Level: Intermediate–Advanced
- **Link:** [https://arxiv.org/abs/2212.10560](https://arxiv.org/abs/2212.10560)
- **Google DeepMind** — "Evol-Instruct: Evolutionary Prompting for Instruction-Tuning Data"
- Why: Representative of *evol-instruct* approaches (mutating/expanding instructions to increase diversity/complexity).
- Level: Advanced
- url: https://arxiv.org/abs/2304.12244 [VERIFY]
- **OpenAI** — "RLAIF: Reinforcement Learning from AI Feedback"
- Why: Core reference for generating synthetic preference labels/feedback from models (relevant to constitutional AI data and self-play-like feedback loops).
- Level: Advanced
- **Link:** [https://arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073)
## Original paper
- **Wang et al.** — "Self-Instruct: Aligning Language Models with Self-Generated Instructions"
- Why: Foundational synthetic instruction data generation + filtering pipeline that influenced many later instruction-tuning datasets.
- Level: Intermediate–Advanced
- **Link:** [https://arxiv.org/abs/2212.10560](https://arxiv.org/abs/2212.10560)
## Code walkthrough
- **tatsu-lab** — "stanford_alpaca" (Self-Instruct-style synthetic instruction data + instruction tuning recipe)
- Why: Widely used, concrete codebase showing how synthetic instruction-following data is produced/used (and how distillation-style instruction tuning is run in practice).
- Level: Intermediate
- **Link:** [https://github.com/tatsu-lab/stanford_alpaca](https://github.com/tatsu-lab/stanford_alpaca)
## Coverage notes
- Strong: self-instruct; synthetic instruction generation; constitutional AI data (written explainer); distillation-style instruction tuning via Alpaca-like pipelines.
- Weak: self-play as a general synthetic-data engine outside of preference modeling; RLVR specifically (term varies by source and is not consistently standardized in public references).
- Gap: high-quality, widely-cited single resource focused specifically on *data quality filtering* and *decontamination* for synthetic datasets (beyond scattered best practices in papers/tooling).

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Auto Evol-Instruct (Automatic Instruction Evolving)
**Paper** · [source](https://aclanthology.org/2024.emnlp-main.397.pdf)

*Empirical comparison/ablation of instruction-evolving strategies (auto-designed evolution rules + selection by failure rate) with downstream benchmark gains.*

<details>
<summary>Key content</summary>

- **Goal / optimization objective (Eq. 1):** find evolving method \(e^*\) maximizing post-SFT performance on evolved data:  
  \[
  e^*=\arg\max_e Q(X_e)
  \]
  where \(X=\{x_i\}\) is seed instruction-response data, \(X_e\) is evolved dataset under method \(e\), \(Q(\cdot)\) is downstream benchmark score after instruction tuning.
- **Core workflow (Sec. 3; Fig. 1):**
  1) Start with **universal initial evolving method** prompt (Fig. 2): Step1 list methods to increase complexity; Step2 plan; Step3 rewrite adding **10–20 words**; Step4 review for reasonableness.  
  2) Iteratively optimize evolving method using **optimizer LLM** via: **Evol Trajectory Analysis** (prompt Fig. 7) → **Evolving Method Optimization** (Fig. 8).  
  3) **Multiple optimizations (self-consistency):** run optimizer \(m\) times; select method with **lowest evolution failure rate** on dev set \(D\).
- **Failure-rate selection (Eq. 2):**
  \[
  \lambda_{R^{e_i^t}}=\frac{\sum_{r\in R^{e_i^t}}F(r)}{|D|}
  \]
  \(R^{e_i^t}\): responses when answering evolved dev instructions; \(F(r)\in\{0,1\}\) flags evolution failure (Appendix A rules: e.g., “Understood/Thank you … ?”, “Sure … ?”, contains “please provide”).
- **Defaults / setup (Table 1):** seed data sizes: ShareGPT **10K**, GSM8K-train **7K**, Code Alpaca **20K**. Evol+optimizer LLM often **GPT-4**; subset ~**2,000** samples used to optimize method (footnote Sec. 3).
- **Main empirical results (Table 2; large models):**
  - Mixtral-8x7B + **10K evolved ShareGPT**: **MT-Bench 8.09**, **AlpacaEval 91.37** (vs seed 7.65/87.98; Evol-Instruct 7.76/89.50).
  - Mixtral-8x7B + **7K evolved GSM8K**: **GSM8K 82.49** (vs seed 70.60; Evol-Instruct 79.15).
  - DeepSeek-Coder-Base-33B + **20K evolved Code Alpaca**: **HumanEval 77.40** (vs seed 72.00; Evol-Instruct 73.20).
- **Ablations:**
  - Initial evolving method alone improves vs Evol-Instruct (Fig. 3): MT-Bench **6.31→6.60**, HumanEval **61.0→62.2**; Auto Evol-Instruct further to MT-Bench **6.71**, HumanEval **64.0**, GSM8K **64.4**.
  - **#optimizations \(m\)** (Fig. 5a, GSM8K): \(m=1\) → **62.7**, \(m=9\) → **65.0**.
  - **Optimization steps** (Fig. 5b): performance rises early, then **drops after ~12 steps** (over-optimization).
  - **Evol LLM strength** (Table 3, GSM8K): Auto Evol-Instruct with evol LLM **GPT-3.5: 64.4**; with **GPT-4: 70.7**.
- **Contamination check (Sec. 5.6):** GSM8K evolved 7K; only **10** samples show any **13-gram** match.

</details>

### 📄 Auto Evol-Instruct (Evol-Instruct automation)
**Paper** · [source](https://aclanthology.org/anthology-files/pdf/emnlp/2024.emnlp-main.397.pdf)

*End-to-end evol-style synthetic instruction refinement (mutations/operators via prompts, trajectory analysis, selection by failure rate) + benchmark gains from iterative refinement.*

<details>
<summary>Key content</summary>

- **Goal / optimization objective (Eq. 1):** find evolving method \(e^*\) maximizing post-SFT performance on evolved data:  
  \[
  e^*=\arg\max_e Q(X_e)
  \]
  where \(X=\{x_i\}\) is seed instruction-response data, \(e\) is an evolving method (prompt/rules), \(X_e\) is evolved dataset, \(Q(\cdot)\) is benchmark score after instruction tuning.
- **Core workflow (Section 3, Fig. 1):**
  1) Start with **universal initial evolving method** \(e_0\) (Fig. 2: Step1 list methods to increase complexity; Step2 plan; Step3 rewrite adding **10–20 words**; Step4 review for reasonableness; no language change).  
  2) For step \(t\): sample minibatch from \(X\); evol LLM evolves each instruction **\(l\) rounds** → trajectory \(S_t=\{X_t, X_t^{(1)},...,X_t^{(l)}\}\).  
  3) **Optimizer LLM** does **trajectory analysis** (Fig. 7 prompt) → feedback \(f_t\).  
  4) **Method optimization** updates \(e_{t-1}\to e_t\) using \(f_t\).  
  5) Run **m parallel optimizations** (sampling decoding); select \(e_t\) with lowest failure rate on dev set \(D\).
- **Selection metric (Eq. 2):** evolution failure rate  
  \[
  \lambda_{R^{e_t}}=\frac{\sum_{r\in R^{e_t}}F(r)}{|D|}
  \]
  where \(R^{e_t}\) are responses for evolved dev instructions; \(F(r)\in\{0,1\}\) flags failures (Appendix A: “Understood/Thank you…?” stagnant complexity; “Sure…?” insufficient qualification; contains “please provide” loss of key info).
- **Key results (Table 2):**  
  - **Large models:** Seed→Auto: MT-Bench **7.65→8.09 (+0.44)**; AlpacaEval **87.98→91.37 (+3.39)**; GSM8K **70.60→82.49 (+11.89)**; HumanEval **72.00→77.40 (+5.4)**.  
  - **Small models:** Seed→Auto: MT-Bench **6.88→7.51 (+0.63)**; GSM8K **56.90→70.74 (+13.84)**; HumanEval **57.90→65.85 (+7.95)**.
- **Defaults/params (Table 1):** seed sizes: ShareGPT **10K**, GSM8K-train **7K**, Code Alpaca **20K**; method-optimization uses ~**2,000** sampled entries; evol/optimizer often **GPT-4** (paper also tests GPT-3.5 vs GPT-4; Table 3: Auto with GPT-4 evol LLM on GSM8K **70.7** vs GPT-3.5 **64.4**).

</details>

### 📄 Cost-effective synthetic data strategies (BR rule)
**Paper** · [source](https://arxiv.org/html/2409.19759v2)

*Cost-effectiveness trade-offs: generating new *responses* vs new *instructions*, plus ablations on verification and model choices.*

<details>
<summary>Key content</summary>

- **Three SFT synthetic data strategies (Section 3.1):**
  - **Answer Augmentation:** keep seed instructions; sample multiple teacher responses (CoT + temperature sampling).
  - **Question Rephrasing:** augmenter rewrites seed instruction to same meaning/same answer; then teacher answers.
  - **New Question Evolution:** augmenter creates *new* instruction conditioned on seed but with different final answer; includes self-verification to ensure answerable/format-correct; then teacher answers.
- **Cost metric (Section 4.2):** **Budget Ratio (BR)**  
  - **BR = Q / |S|**, where **Q** = teacher query budget (#queries), **|S|** = seed instruction set size.
- **Main empirical rule (Section 5.2, Fig. 3):**
  - **Low BR:** **Answer Augmentation** most cost-effective.
  - **High BR:** generating **new prompts** (Question Rephrase / New Question) becomes optimal.
  - **Shift point depends on seed size:**  
    - **|S|=100:** shift at **BR ≈ 27–51** (≈ **3k–5k** samples).  
    - **|S|=1,000:** average shift **BR = 17.6**.  
    - **Largest seed:** average shift **BR = 16.4**.
  - **New Question Evolution** generally beats **Question Rephrase** in cost + scalability.
- **Ablations (Section 5.3):**
  - **Augmenter model choice:** Rephrasing is robust to weaker augmenters; **New Question** depends strongly on augmenter capability. Using **Llama 2 7B** as augmenter drops New Question accuracy by **~15%** vs stronger augmenters at **10k** synthetic samples (GSM8k, |S|=1,000).
  - **Verification w/ ground truth (Spider):** filtering to verified-correct responses yields **no significant improvement** vs simply scaling dataset size (Figs. 5–6); teacher wrong on **~10%** instructions (filtered out reduces diversity).
  - **Different student:** BR trend holds for **Mistral 7B**; transition around **BR ≈ 12** (Fig. 7).
- **Defaults/params (Appendix F):** SFT **3 epochs**, peak LR **4e-5** (Mistral **1e-5**), cosine decay, **3% warmup**, batch **128**, max seq **1536**. Generation: greedy decoding, **temperature 0.7**. Teacher/augmenter often **Llama 3.1 70B Instruct**; student **Llama 2 7B Chat**.

</details>

### 📄 FineWeb2 multilingual web-data curation pipeline (LID → dedup → adaptive filters → rehydration)
**Paper** · [source](https://arxiv.org/html/2506.20920v1)

*Step-by-step CommonCrawl pipeline with concrete dedup + filtering stages and key hyperparameters.*

<details>
<summary>Key content</summary>

- **Pipeline overview (Section 4):**
  1) Download ~**96** CommonCrawl snapshots (2013–Apr 2024); URL blocklist for adult content; HTML→text via **trafilatura**.  
  2) **Language ID (LID)** with **GlotLID** (supports **1880** language-script labels; includes “noise/script” labels).  
  3) **Global per-language dedup** using **MinHash** (Broder 1997) **before filtering** to isolate filter effects.  
  4) **Adaptive heuristic filtering** (FineWeb/Gopher-style) with language-specific thresholds derived from metric distributions.  
  5) **Rehydration**: duplication-aware upsampling using dedup cluster-size metadata + filter removal rates.
- **LID threshold formula (Section 4.2):** per-language confidence cutoff set to  
  **τ = clip(median(s) − std(s), [0.2, 0.9])**, where **s** are GlotLID confidence scores for that language’s docs.
- **Dedup defaults (Section 4.3):** MinHash with **14 buckets**, **bucket size 8**, **word 5-grams**; uses language-specific word tokenizers; keep **1 doc/cluster** and record **cluster size**.
- **Stopword filter (Section 4.4.1):** build stopwords from high-frequency words (frequency-thresholded, not fixed count); require **≥2 stopwords** present per document (per Gopher filters).
- **Filter threshold selection methods tested (Section 4.4.2):** English-fixed, MeanStd, Quantile, **10Tail (remove 10%)**, MedianRatio; best choices: **10Tail + Quantile on Wikipedia** (or GlotLID-corpus if no Wikipedia) for quality filters; **MeanStd on CommonCrawl** for repetition filters.
- **Low-resource precision filter (Section 4.4.3):** high-affinity wordlists; contamination = fraction of docs with **none** of these words; apply when contamination **>10%**; URL-based exceptions (language code/name/TLD). Manual audit: **~30% precision** gain for some languages.
- **Rehydration weighting rule (Section 4.5):** assign weight **10** to cluster-size bin with **lowest filter removal rate**; weight **1** to bins with removal rate **above global removal rate**; interpolate between.
- **Scale/resulting dataset (Section 5):** FineWeb2 = **20 TB**, **5B documents**, **1,868** language-script pairs (1,226 with >100 docs; 474 >1k; 203 ≥10k). FineWeb2 excludes English; pair with FineWeb for full coverage.

</details>

### 📄 Process-based Self-Rewarding (Stepwise Self-Judging + DPO)
**Paper** · [source](https://aclanthology.org/2025.findings-acl.930.pdf)

*Procedure + equations for process-level (stepwise) self-rewarding/judging and iterative step-wise preference optimization.*

<details>
<summary>Key content</summary>

- **Core pipeline (Fig. 1; §3.2–3.5):**
  1) Build **IFT** (step-by-step reasoning) by logically segmenting CoT solutions into steps (“Step n: …”) using GPT-o1; 28,889 NuminaMath samples.  
  2) Build **EFT** (step-wise LLM-as-a-Judge) via: train a **PRM** on PRM800k to label each step “+/-”; run **MCTS** on a policy model; pick best/worst step at same depth; GPT-o1 writes pairwise judgment + explanation; keep pairs consistent with PRM and consistent under swapped order (double-eval). Final EFT: 4,679 (train 4,167 / test 500).  
  3) Initialize **M1** by SFT on **EFT+IFT**.  
  4) Iteratively generate step-wise preference pairs with the model as judge, then train with **step-wise DPO** to get M2…Mn.
- **Step candidate scoring (Eq. 1–5; §3.3):** For step index \(l\), sample width \(w\) candidates  
  \(S_l=\{s_{l,1},...,s_{l,w}\}\) (Eq.1).  
  Pairwise win indicator \(O(s_{l,i},s_{l,j}\mid x,s_{1:l-1})\in\{0,1\}\).  
  \(Score_{l,i}=\sum_{j\neq i} O(s_{l,i},s_{l,j}\mid x,s_{1:l-1})\) (Eq.2).  
  Choose \(s^{best}_l=\arg\max Score_l\), \(s^{worst}_l=\arg\min Score_l\) (Eq.3–4); set next step \(s_l=s^{best}_l\) (Eq.5). If \(\max=\min\), **rollback** one step and discard that pair.
- **Step-wise DPO loss (Eq. 6–8; §3.4):**  
  \(A=\beta\log\frac{\pi_\theta(s^b_l\mid x,s_{1:l-1})}{\pi_{ref}(s^b_l\mid x,s_{1:l-1})}\),  
  \(B=\beta\log\frac{\pi_\theta(s^w_l\mid x,s_{1:l-1})}{\pi_{ref}(s^w_l\mid x,s_{1:l-1})}\).  
  \(L(\pi_\theta;\pi_{ref})=-\mathbb{E}_{D}\left[\log\sigma(A-B)\right]\).
- **Design rationale:** Step-wise **pairwise comparison** is more consistent than scoring whole solutions (Table 6: consistency 0.84 vs 0.72; agreement 0.88 vs 0.32). Fine-grained step rewards help long-chain math reasoning.
- **Key empirical results (Table 1–2):**  
  72B PSRLM improves avg to **60.6** at M4 (vs base 48.6). From M1→M4 (Table 2): **+10.0 AIME2024**, **+12.5 AMC2023**.  
  7B PSRLM M4 avg **55.7** (vs base 36.1); M1→M4 gains include **+10.0 AMC2023**, **+6.6 AIME2024**.
- **Defaults/params (§4):** generation temp 0.5, top_p 0.95; search width \(w=6\); max step iterations 20. PRM/MCTS prefilter: simulation_depth 3, num_iterations 100, temp 0.7, top_p 0.95. Step-wise DPO: 1 epoch, lr 5e-7, batch 32; M2/M3/M4 use 400/800/1200 questions for preference generation.

</details>

### 📄 RLVR under noisy verification (RLVεR phase transition)
**Paper** · [source](https://arxiv.org/abs/2601.04411)

*RLVR/GRPO update rule with noisy binary verifier; how FP/FN noise changes learning direction (“rate vs fate”).*

<details>
<summary>Key content</summary>

- **RLVR/GRPO loop (Section 2):** (1) sample a *group* of completions per prompt from current policy; (2) score each completion with verifier reward; (3) **group-normalize** rewards to advantages via z-score: \(A_i=(r_i-\bar r)/s_r\) (Eq. 23); (4) policy-gradient update reinforcing high-advantage samples (core update Eq. 3).
- **Noise model (Eq. 1):** binary observed reward \(r\in\{0,1\}\) is a flipped version of latent correctness with **false negative** rate \(\mathrm{FNR}\) and **false positive** rate \(\mathrm{FPR}\).
- **Verifier quality scalar (Eq. 2):** **Youden’s index**
  \[
  J = 1-\mathrm{FNR}-\mathrm{FPR}.
  \]
  Interpretation: \(J=1\) perfect; \(J=0\) chance-level; \(J<0\) anti-informative.
- **Key theoretical result (Sections 2.2–3):** Under group normalization, the **advantage gap** between good vs bad modes is proportional to \(J\) (Eq. 5), yielding a **phase transition** in bad-mass dynamics (Eq. 6):  
  - \(J>0\): bad mass driven to extinction (learning).  
  - \(J=0\): neutral drift (no directional learning).  
  - \(J<0\): bad modes amplify (anti-learning/collapse).
- **“Rate, not fate” (Eq. 9):** for \(J>0\), noise mainly **rescales time** (more steps/rollouts compensate).
- **Empirics (Section 7, Qwen2.5-3B, Python unit-test verifier, 2 epochs = 1,410 steps, KL=0):** pass@1 improvement vs base under synthetic noise:  
  - (FPR=0.60, FNR=0.50) \(J=-0.10\): **−12.6%**  
  - (0.50, 0.50) \(J=0\): **+0.6%**  
  - (0.00, 0.70) \(J=0.30\): **+3.2%**  
  - (0.70, 0.00) \(J=0.30\): **+1.8%**  
  - (0.20, 0.10) \(J=0.70\): pass@1 **18.6%**, **+5.8%**  
  - (0.00, 0.00) \(J=1\): pass@1 **20.8%**, **+8.0%**
- **Design rationale:** group normalization makes dynamics analyzable as **replicator flow** on probability simplex; outcome depends primarily on verifier discriminative power \(J\), not on PPO clipping/importance sampling at leading order (Section 6).

</details>

### 📄 Self-Rewarding LMs via Iterative DPO (LLM-as-a-Judge)
**Paper** · [source](https://arxiv.org/abs/2401.10020)

*Iterative DPO self-improvement loop using self-generated preference pairs scored by the same LLM (LLM-as-a-Judge).*

<details>
<summary>Key content</summary>

- **Overall iterative pipeline (Sec. 2.4):**
  - Start with base pretrained LM \( \pi_0 \).
  - Train \( \pi_1 \) with **SFT** on seed **IFT+EFT** data.
  - For iteration \(t\ge 1\): create **AIFT(\(\pi_t\))** via self-instruction creation, then train \( \pi_{t+1} \) from \( \pi_t \) using **DPO** on AIFT(\(\pi_t\)).
- **Self-Instruction Creation (Sec. 2.2):**
  1) Generate new prompts (few-shot; in main exp prompt-gen uses fixed Llama 2-Chat 70B).  
  2) Sample diverse candidate responses from current model.  
  3) **Evaluate** candidates with the *same model* as judge; scores are averaged over **3 sampled evaluations**.
- **Preference pair construction (Sec. 2.3):** For each prompt, take **highest-scoring** response as **winner** and **lowest-scoring** as **loser**; **discard** if scores tie. Dataset format: \((x, y^+, y^-)\).
- **Judge prompt design (Sec. 2.1, A.2):** additive 5-criterion scoring (relevance, coverage, usefulness, clarity, expertise) with justification + final score (out of 5). This prompt greatly outperformed a multiple-choice style prompt: **pairwise accuracy 65.1% vs 26.6%** (Table 5).
- **Key empirical results:**
  - **Instruction following (AlpacaEval 2.0 win rate vs GPT-4 Turbo):** Iter1 **9.94%**, Iter2 **15.38%**, Iter3 **20.44%** (Table 1).
  - **Head-to-head:** Iter2 beats Iter1 **55.5% vs 11.7%**; Iter3 beats Iter2 **47.7% vs 12.5%**.
  - **Reward modeling (Table 4, pairwise acc vs human rankings):** SFT baseline **65.1%** → Iter1 **78.7%** → Iter2 **80.4%** → Iter3 **81.7%**.
- **Defaults/hyperparams (Sec. 3.1.3):**
  - DPO: \(\beta=0.1\); early stopping via pairwise eval every **200 steps**.
  - Data sizes: IFT seed **3,200**; EFT train **1,630** (eval **541**). AIFT pairs: **3,964** for AIFT(\(\pi_1\)), **6,942** for AIFT(\(\pi_2\)).

</details>

### 📄 Superfiltering (Weak-to-Strong Instruction-Data Filtering via IFD)
**Paper** · [source](https://aclanthology.org/2024.acl-long.769.pdf)

*Ablation results + threshold/budget trade-offs for weak-to-strong instruction-data filtering and downstream benchmark impacts.*

<details>
<summary>Key content</summary>

- **Perplexity (Eq. 1):**  
  \[
  \mathrm{PPL}(y_i|x_i)=\exp\left(-\frac{1}{N}\sum_{j=1}^{N}\log p(y_{i,j}\mid x_i,y_{i,1..j-1})\right)
  \]  
  *Defs:* \(x_i\)=instruction (incl. optional input), \(y_i\)=response, \(N\)=#tokens in \(y_i\).
- **Instruction-Following Difficulty (IFD) (Eq. 2):**  
  \[
  \mathrm{IFD}(y_i|x_i)=\frac{\mathrm{PPL}(y_i|x_i)}{\mathrm{PPL}(y_i)}
  \]  
  Higher IFD ⇒ instruction provides less help ⇒ “harder” sample.
- **Procedure (Section 3.3):** Use a *weak* pretrained LM (GPT-2 124M) **without extra training** to compute IFD for each sample; select **top k% with highest IFD under 1**; finetune *strong* student (LLaMA2-7B/13B).
- **Weak-to-strong consistency (Table 1):** Spearman rank correlation vs LLaMA2-7B is high even for GPT-2. Example (Alpaca): ρ(PPL)=0.726, ρ(IFD)=0.679. Wizard70k: ρ(IFD)=0.802 (GPT-2). Overlap of selected sets increases with budget (e.g., Alpaca GPT-2 overlap: 5%→0.28, 10%→0.41, 15%→0.49).
- **Downstream gains with small budgets (Table 2):**  
  Alpaca + LLaMA2-7B: **5%** data (2,600) Pairwise Winning Score **1.133** vs 100%; AlpacaEval win rate **33.04** vs **27.75**.  
  Alpaca-GPT4 + LLaMA2-13B: **10%** data (5,200) Avg **63.65** vs **60.81** (100%).
- **Ablation—strategy & filter model (Table 3, Alpaca→LLaMA2-7B):**  
  Random (5%): **0.936**; Diversity (5%): **0.927**; **Perplexity-based** (5%): **0.261** (bad).  
  IFD filters: GPT-2 (Superfilter) **1.133**; GPT-NEO **1.096**; LLaMA2-7B filter **1.303** (best).
- **Cost/latency (Table 4):** Filtering time: Superfiltering **8 min** vs ChatGPT-score **120 min**, reward-model **1400 min**, IFD using LLaMA2-7B **161 min**; Superfiltering reported **~20× faster** than filtering with LLaMA2-7B.
- **Training defaults (Section 4.2):** Adam; LR **2e-5** (LLaMA2-7B), **1e-5** (13B); batch **128**; **3 epochs**; max length **2048**; warmup **0.03**.

</details>

### 📄 Why Self-Rewarding Works (Iterative SRLM Guarantees)
**Paper** · [source](https://arxiv.org/pdf/2601.22513.pdf)

*Formal assumptions + convergence/guarantee statements for iterative self-rewarding/DPO; when self-judging improves and when single-step can fail.*

<details>
<summary>Key content</summary>

- **Setup (Section 3):** Policy is a conditional distribution \(\pi(y\mid x)\) over responses \(y\in\mathcal V^L\) given prompt \(x\sim\mathcal D\). Iterations \(t=0,1,\dots,T\): \(\pi_0\to \pi_1\to\cdots\to \pi_T\).
- **Self-reward (Eq. 1):** \(r_{\pi_t}(x,y)=\log \pi_t(y\mid x)\). Data per round: sample \(x\), generate two responses \(y^+,y^-\), define preference by reward difference \(\Delta r = r_{\pi_t}(x,y^+)-r_{\pi_t}(x,y^-)\).
- **KL-regularized improvement objective (Eq. 2):** choose \(\pi_{t+1}\) maximizing expected reward while staying close to reference \(\pi_t\) via KL regularization.
- **DPO-style loss (Eq. 3):** minimize logistic regression on pairwise preferences with reference \(\pi_t\):  
  \[
  \mathcal L_t(\pi)=\mathbb E\Big[\log\big(1+\exp(-\beta(\log\pi(y^+\!\mid x)-\log\pi(y^-\!\mid x)-(\log\pi_t(y^+\!\mid x)-\log\pi_t(y^-\!\mid x))))\big)\Big]
  \]
  Update operator (Eq. 4): \(\pi_{t+1}=\mathcal T(\pi_t)=\arg\min_{\pi\in\Pi}\mathcal L_t(\pi)\).
- **Policy condition number (Eq. 5, Section 4):**  
  \[
  \kappa(\pi)=\mathbb E_{x\sim\mathcal D}\Big[\frac{1}{\max_y \pi(y\mid x)}\Big]
  \]
  Large \(\kappa\) = diffuse/low-confidence policy → unstable self-rewarding.
- **Single-step limitation (Theorem 4.1):** For any one-step self-rewarding algorithm with sample budget \(n\), there exists a hard instance where failure probability is lower-bounded as a function of \(\kappa(\pi_0)\) (Eq. 6; \(\tilde\Omega(\cdot)\) hides logs). Near-uniform or low top-1 autoregressive policies make \(\kappa(\pi_0)\) scale like response-space size or \(\alpha^{-L}\), yielding constant failure when \(n\) is comparable.
- **Inference consequence (Proposition 4.3):** If the unique optimal sequence has probability \(\le 1/2\), greedy decoding can be guaranteed to miss it.
- **Iterative guarantees (Section 5):**
  - **Assumption 5.1 (Realizability):** optimal KL-regularized policy \(\pi^\star\in\Pi\).
  - **Stability constants (Def. 5.2):** minimum confidence \(\mu=\min_{t,x}\max_y \pi_t(y\mid x)\); margin \(\gamma=\min_{t,x}\big(\log\pi_t(y^\star\mid x)-\max_{y\ne y^\star}\log\pi_t(y\mid x)\big)\).
  - **Finite-sample bound (Theorem 5.3 + Remark 5.4):** failure probability after \(T\) rounds scales like a **statistical term** \(\tilde O(1/\sqrt n)\) times \((\text{stable floor depending on }\mu)+(\text{transient term depending on }\kappa(\pi_0)\text{ decaying exponentially in }T)\). For large \(T\), simplifies (up to logs/constants) to \(\tilde O(1/\sqrt n)\); initialization influence vanishes exponentially.
  - **Mechanism (Remark 5.5):** early iterations induce a **contraction mapping on \(\kappa(\pi_t)\)**: \(\kappa(\pi_t)\to \kappa_\infty\) with geometric decay of the initialization component.
  - **Iterations needed (Cor. 5.7):** \(T\) only needs to grow **logarithmically in \(\kappa(\pi_0)\)** to make initialization effects negligible; larger per-round \(n\) reduces required \(T\).

</details>

### 📊 HumanEval + pass@k (Codex) evaluation & leakage-aware benchmark design
**Benchmark** · [source](https://arxiv.org/abs/2107.03374)

*Exact benchmark construction + evaluation protocol (pass@k) and overlap/contamination rationale for code LMs*

<details>
<summary>Key content</summary>

- **Why functional correctness (Section 2.1):** Match-based metrics (exact match/BLEU) fail for code because many programs are functionally equivalent; evaluate by **unit tests** instead.
- **pass@k unbiased estimator (Eq. 1):** Generate **n ≥ k** samples per problem, let **c** = #samples passing tests.  
  \[
  \text{pass@k} := \mathbb{E}_{\text{Problems}}\left[1-\frac{\binom{n-c}{k}}{\binom{n}{k}}\right]
  \]
  **Defaults used:** **n = 200**, **k ≤ 100**. (They note estimating via \(1-(1-\hat p)^k\) with \(\hat p=\) pass@1 is **biased**.)
- **HumanEval benchmark construction (Section 2.2):**
  - **164 hand-written** Python function-synthesis problems (signature + docstring + unit tests).
  - Avg **7.7 unit tests/problem**.
  - **Rationale:** tasks must be hand-written because training data includes large fractions of GitHub; GitHub contains many public solution repos (e.g., Codeforces solutions), risking overlap with scraped benchmarks.
- **Sampling/eval procedure (Section 3):**
  - Prompt = header + signature + docstring.
  - Stop sequences: `\nclass`, `\ndef`, `\n#`, `\nif`, `\nprint`.
  - Sampling: nucleus **top-p = 0.95**; temperature tuned per k (e.g., for 679M: **T*=0.2** for pass@1, **T*=0.8** for pass@100).
- **Key results (Abstract/Section 3):**
  - HumanEval pass@1: **Codex-12B 28.8%**, **GPT-3 ~0%**, **GPT-J 11.4%**.
  - With **100 samples/problem**: solves **70.2%** (Codex); **Codex-S** (supervised FT) **77.5%**.
  - Selecting sample by **highest mean log-probability** passes **44.5%**.
- **Training hyperparams (Section 3.2):** 100B tokens; Adam **β1=0.9, β2=0.95, ε=1e-8**, weight decay **0.1**; LR schedule: **175-step warmup + cosine decay**.

</details>

---

## Related Topics

- [[topics/pre-training|Pre-Training]]
- [[topics/rlhf-alignment|RLHF & Alignment]]
- [[topics/reasoning-models|Reasoning Models]]
- [[topics/lora-peft|LoRA & PEFT]]
