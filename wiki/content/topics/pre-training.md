---
title: "Pre-Training"
subject: "Large Language Models"
date: 2025-04-06
tags:
  - "subject/large-language-models"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/lilian-weng"
  - "educator/sebastian-raschka"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Lilian Weng"
  - "Sebastian Raschka"
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

# PRE-TRAINING

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- Why: Karpathy provides an exceptionally clear mental model of pre-training as the foundational "compression of the internet" step — covering next-token prediction, autoregressive generation, and the intuition behind perplexity in a way that is accessible yet technically honest. Already validated in the existing curated list.
- Level: beginner/intermediate

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Large Language Model Pre-training"
- **Link:** [https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/)
- Why: Lilian Weng's blog posts are the gold standard for structured, citation-backed written explainers in ML. Her coverage of training objectives, data curation (including LAION-5B context), and architectural choices bridges theory and practice better than most written resources. The exact post slug should be verified.
- Level: intermediate/advanced

---

## Deep dive
- **Sebastian Raschka** — "Pre-Training LLMs from Scratch" (Magazine/Substack series)
- url: https://magazine.sebastianraschka.com/p/new-llm-pre-training-and-post-training [VERIFY — Raschka's Substack at magazine.sebastianraschka.com is confirmed real; exact slug needs verification]
- Why: Raschka's writing uniquely combines rigorous mathematical grounding with practical implementation notes. His pre-training coverage explicitly addresses data pipelines, tokenization, training stability, and evaluation via perplexity — making it the most complete written deep dive for practitioners building intuition before touching code.
- Level: advanced

---

## Original paper
- **Brown et al. (2020)** — "Language Models are Few-Shot Learners" (GPT-3)
- **Link:** [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
- Why: This is the most widely cited and pedagogically readable paper establishing the modern pre-training paradigm at scale. It clearly articulates the next-token prediction objective, training data composition, and emergent capabilities — making it the canonical reference for what "pre-training" means in the LLM era. For multi-modal pre-training specifically, the CLIP paper (arxiv.org/abs/2103.00020) is the contrastive pre-training counterpart. [NOT VERIFIED]
- Level: intermediate/advanced

---

## Code walkthrough
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- Why: This is arguably the best hands-on pre-training walkthrough in existence. Karpathy implements autoregressive language model pre-training from scratch in ~2 hours, covering the training loop, next-token prediction loss, and perplexity evaluation with minimal abstraction. The associated GitHub repo (github.com/karpathy/ng-video-lecture) provides runnable code.
- Level: intermediate

---

## Coverage notes
- **Strong:** Unimodal LLM pre-training (next-token prediction, autoregressive generation, perplexity, scale) — Karpathy's video and code walkthrough cover this exceptionally well.
- **Weak:** Multi-modal pre-training specifics (interleaved training, natively multi-modal architectures, LAION-5B data curation) — no single curated video covers this with the same depth as the LLM-only case.
- **Gap:** No excellent standalone YouTube video exists specifically for **contrastive pre-training** (CLIP-style) or **interleaved multi-modal pre-training** (Flamingo/Gemini-style) at a beginner-friendly level. The intro-to-multimodal course will need supplementary resources for these sub-topics. Consider Yannic Kilcher's CLIP paper walkthrough (youtube_id: `T9XSU0pKX2E`) [NOT VERIFIED] as a candidate for contrastive pre-training.

---

## Cross-validation
This topic appears in **2 courses**: `intro-to-llms`, `intro-to-multimodal`
- The Karpathy video (`zjkBMFhNj_g`) is already curated 4× for `intro-to-llms/how-language-models-work` — **deduplication recommended** in the platform's content index.
- The `intro-to-multimodal` course will require additional resources specifically addressing LAION-5B, contrastive pre-training, and natively multi-modal objectives not covered by the LLM-focused resources above.

---

---

## Additional Resources for Tutor Depth

> **7 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Chinchilla compute-optimal scaling (tokens vs parameters)
**Paper** · [source](https://arxiv.org/abs/2203.15556)

*Chinchilla compute-optimal rule-of-thumb: train smaller models on more tokens; explicit token/parameter tradeoff under fixed FLOPs.*

<details>
<summary>Key content</summary>

- **Objective (Eq. 1):** choose parameters **N** and training tokens **D** to minimize final pre-training loss **L(N,D)** under a fixed compute budget **C**:  
  \[
  (N_{\text{opt}}(C),D_{\text{opt}}(C))=\arg\min_{N,D:\ \text{FLOPs}(N,D)=C} L(N,D)
  \]
  - **N** = number of model parameters; **D** = number of seen training tokens; **C** = total training FLOPs.
- **Empirical dataset:** >400 transformer LMs, **70M–16B parameters**, trained on **5B–500B tokens**.
- **Main scaling result (Section 3; Table 2 exponents):** compute-optimal scaling is approximately **equal** in parameters and tokens:  
  - Approach 1: \(N_{\text{opt}}\propto C^{0.50}\), \(D_{\text{opt}}\propto C^{0.50}\)  
  - Approach 2 (IsoFLOP): \(a=0.49,\ b=0.51\)  
  - Approach 3 (parametric fit): \(a=0.46,\ b=0.54\)  
  **Rule-of-thumb:** *for every doubling of model size, double training tokens*.
- **Parametric loss model (Eq. 2):**  
  \[
  \hat L(N,D)=E+\frac{A}{N^{\alpha}}+\frac{B}{D^{\beta}}
  \]
- **Training-procedure detail (Section 3.1/3.2):** best final loss when **cosine LR schedule length matches token horizon**; they **decay LR by 10× over ~D tokens**.
- **Key comparison (Abstract/Fig. 1):** **Chinchilla 70B** trained with **same compute as Gopher** (**5.76×10^{23} FLOPs**) but **4× more data**, and **outperforms** Gopher (280B), GPT‑3 (175B), Jurassic‑1 (178B), MT‑NLG (530B).  
  - **MMLU:** **67.5%** average accuracy, **>7%** absolute improvement over Gopher.

</details>

### 📄 Cross-entropy ↔ Perplexity (next-token prediction)
**Paper** · [source](https://arxiv.org/html/2212.11281v2)

*Explicit definition of perplexity from cross-entropy loss; next-token prediction evaluation details + human-vs-LM numbers.*

<details>
<summary>Key content</summary>

- **Per-token cross-entropy loss (human or model) and perplexity (Section 4.1.1, Eq. 1):**  
  Let \(p(\cdot\mid c)\) be the predictor’s distribution over next tokens given context \(c\), and \(t\) the true next token. The (expected) loss is  
  \[
  \mathcal{L} \;=\; \mathbb{E}_{(c,t)}\big[-\log p(t\mid c)\big]
  \]
  **Perplexity** is defined by exponentiating this cross-entropy:  
  \[
  \mathrm{PPL} \;=\; \exp(\mathcal{L})
  \]
  (If \(\log\) is base-2, loss is in bits and \(\mathrm{PPL}=2^{\mathcal{L}}\); base \(e\) gives nats and \(\exp(\mathcal{L})\).)
- **Top-1 accuracy definition (Intro):** fraction of positions where the predictor’s **highest-probability** token equals the true next token.
- **Human vs LM top-1 accuracy on OpenWebText (Section 3.2):**
  - Humans: mean **29%** top-1 accuracy (38 participants with ≥50 answers: **30%**).  
  - GPT-3: **56%** top-1 accuracy on same dataset.  
  - Even GPT-Neo-125M exceeded all human players in their sample.
- **Human perplexity estimation procedure (Section 4):**
  - Humans can’t provide full \(p(\cdot\mid c)\) over ~50k tokens, so authors elicit **relative likelihoods** between two candidate tokens (true token vs a token sampled from a generator LM).
  - **Importance sampling** with generator \(q\) (GPT-2-small, 117M) to approximate sums over vocabulary (Eq. 3–5).
  - **Bias control:** scoring uses a weighted binary cross-entropy reward so optimal reporting matches the human’s true belief (Eq. 7–9).
- **Defaults/parameters:** OpenWebText validation prompts up to **120 tokens**; response options restricted to **11 ratios** (99%, 90%, …, 1%); 60 participants (top-1 game), 54 participants (perplexity game).

</details>

### 📄 Kaplan et al. 2020 — LLM Scaling Laws & Compute-Optimal Training
**Paper** · [source](https://arxiv.org/abs/2001.08361)

*Power-law fits for cross-entropy loss vs parameters/data/compute; compute-optimal allocation equations + fitted exponents/constants.*

<details>
<summary>Key content</summary>

- **Metric/setting:** Autoregressive Transformer LM; optimize next-token cross-entropy **loss L (nats)** over **1024-token context** on **WebText2**; BPE vocab **50,257**. (Sec. 2)
- **Power-law scaling (when not bottlenecked by other factors):**
  - **Params-limited, trained to convergence:**  
    **Eq. (1.1)** \(L(N)=\left(\frac{N_c}{N}\right)^{\alpha_N}\), with \(\alpha_N\approx 0.076\), \(N_c\approx 8.8\times10^{13}\) **non-embedding params**.
  - **Data-limited, early-stopped:**  
    **Eq. (1.2)** \(L(D)=\left(\frac{D_c}{D}\right)^{\alpha_D}\), with \(\alpha_D\approx 0.095\), \(D_c\approx 5.4\times10^{13}\) **tokens**.
  - **Compute-limited, compute-optimal:**  
    **Eq. (1.3)** \(L(C_{\min})=\left(\frac{C^{\min}_c}{C_{\min}}\right)^{\alpha^{\min}_C}\), with \(\alpha^{\min}_C\approx 0.050\), \(C^{\min}_c\approx 3.1\times10^{8}\) **PF-days**.
- **Joint overfitting law:**  
  **Eq. (1.5)/(4.1)** \(L(N,D)=\Big[\left(\frac{N_c}{N}\right)^{\alpha_N/\alpha_D}+\frac{D_c}{D}\Big]^{\alpha_D}\). Implies **data scaling** \(D\propto N^{\alpha_N/\alpha_D}\approx N^{0.74}\).
  - Practical rule to avoid overfitting near seed-noise \(\sim0.02\): **Eq. (4.4)** \(D\gtrsim (5\times10^3)\,N^{0.74}\) (tokens).
- **Training compute estimate:** \(C\approx 6NBS\) (forward+backward factor 6), with batch **B** and steps **S**. (Sec. 3.3)
- **Learning curve fit (infinite-data limit):**  
  **Eq. (1.6)** \(L(N,S)=\left(\frac{N_c}{N}\right)^{\alpha_N}+\left(\frac{S_c}{S_{\min}(S)}\right)^{\alpha_S}\), with \(S_c\approx 2.1\times10^3\), \(\alpha_S\approx 0.76\). (Sec. 5)
- **Critical batch size (depends on loss, not model size):**  
  **Eq. (1.4)/(5.3)** \(B_{\text{crit}}(L)=B_*\,L^{1/\alpha_B}\), with \(B_*\approx 2\times10^8\) tokens, \(\alpha_B\approx 0.21\). (Sec. 5.1)
- **Compute-optimal allocation (key empirical exponents):** \(N\propto C_{\min}^{0.73}\), \(B\propto C_{\min}^{0.24}\), \(S\propto C_{\min}^{0.03}\) ⇒ spend extra compute mostly on **bigger models**, **stop far before convergence**. (Sec. 6; Eq. 1.8)
- **Defaults:** 10% dropout; LR schedule **3000-step warmup + cosine decay to 0**; early stop when test loss stops decreasing. (Sec. 4.2, App. D.6)

</details>

### 📄 LAION-5B dataset creation & filtering (CLIP-based)
**Paper** · [source](https://arxiv.org/abs/2210.08402)

*Web-scale image–text dataset creation pipeline (CLIP filtering, language split, safety tags) + dataset stats*

<details>
<summary>Key content</summary>

- **Dataset scale & composition (Abstract; Section 4):**
  - **LAION-5B = 5.85B** CLIP-filtered image–text pairs.
  - Subsets derived from Common Crawl:
    - **2.32B English** image–text pairs (LAION-2B-en / LAION-2B).
    - **2.26B multilingual** pairs.
    - **1.27B language-unspecific/unknown** (e.g., places/products).
- **Core filtering equation/criterion (Section 3.1):**
  - Compute **CLIP cosine similarity** between image embedding and text embedding:  
    - \( s = \cos(\mathbf{e}_{img}, \mathbf{e}_{txt}) \)  
    - Keep pair if \( s \ge \tau \).
  - Thresholds used:
    - **English:** remove if **\(s < 0.28\)**.
    - **Non-English:** remove if **\(s < 0.26\)**.
  - Effect: starting from **~50B** candidate images, this CLIP-threshold step removed **~90%**, leaving **just short of 6B** examples.
- **Models used for filtering (Section 3.1):**
  - **English:** OpenAI **CLIP ViT-B/32**.
  - **Other languages:** **multilingual CLIP ViT-B/32** (Carlsson et al.).
  - Rationale: larger CLIP variants existed later, but authors used **ViT-B/32 consistently** across the dataset for timing/consistency.
- **Safety/metadata provided (Abstract):**
  - Released **detection scores** for **watermark**, **NSFW**, and **toxic content**; plus tooling for exploration/subset generation (e.g., nearest-neighbor indices).

</details>

### 📖 Trainer LR scheduler knobs (cosine, restarts, custom)
**Reference Doc** · [source](https://discuss.huggingface.co/t/using-cosine-lr-scheduler-via-trainingarguments-in-trainer/14783/8)

*Exact `Trainer`/`TrainingArguments` knobs for scheduler selection + how to override with a custom scheduler*

<details>
<summary>Key content</summary>

- **Built-in scheduler selection via `TrainingArguments`:**
  - Set `lr_scheduler_type = "cosine_with_restarts"` to use cosine annealing with restarts.
  - Pass scheduler-specific parameters via `lr_scheduler_kwargs`, e.g.  
    - `lr_scheduler_kwargs = {"num_cycles": 5}` (controls number of cosine restart cycles).
- **Custom scheduler when built-ins don’t fit (e.g., don’t decay to 0):**
  - HF core maintainer guidance: *“You can pass your own learning rate scheduler to the `Trainer`.”* (used when you want a different final LR such as 50% of peak).
- **Manual cosine-with-warmup scheduler wiring (procedure):**
  1. Create optimizer (example shown: `PagedAdamW_32bit(model.parameters())`).
  2. Create `Trainer(..., optimizers=(optimizer, None))`.
  3. Build scheduler with Transformers helper:  
     - `scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=training_args.warmup_steps, num_training_steps=...)`
  4. Attach it: `trainer.lr_scheduler = scheduler` **or** pass directly: `Trainer(..., optimizers=(optimizer, lr_scheduler))`.
- **Training step count used in examples:**
  - `num_warmup_steps = int(max_steps * warmup_ratio)`
  - `num_training_steps = max_steps` (explicitly set in `TrainingArguments(max_steps=...)`).

</details>

### 📖 Transformers v3.0.2 Optimization (AdamW + LR Schedules)
**Reference Doc** · [source](https://www.huggingface.co/transformers/v3.0.2/main_classes/optimizer_schedules.html)

*Exact `transformers.AdamW` defaults + official LR scheduler APIs (PyTorch/TensorFlow)*

<details>
<summary>Key content</summary>

- **AdamW (PyTorch) API + defaults** (Section “AdamW (PyTorch)”):  
  `transformers.AdamW(params, lr=0.001, betas=(0.9, 0.999), eps=1e-6, weight_decay=0.0, correct_bias=True)`  
  - `lr`: learning rate (default **1e-3**)  
  - `betas=(b1,b2)`: Adam momentum coefficients (default **(0.9, 0.999)**)  
  - `eps`: numerical stability (default **1e-6**)  
  - `weight_decay`: **decoupled** weight decay (default **0.0**)  
  - `correct_bias`: bias correction toggle (default **True**; BERT TF repo uses **False**)  
  - **Rationale:** “weight decay fix” per *Decoupled Weight Decay Regularization* (decay does not interact with Adam’s m/v states).

- **AdamWeightDecay (TensorFlow) defaults**:  
  `learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7, amsgrad=False, weight_decay_rate=0.0`  
  - **Rationale:** adding L2 penalty to loss is *not* correct for Adam; use decoupled decay (equivalent to L2 with plain SGD).

- **TF helper: `create_optimizer` workflow**: warmup → linear decay schedule.  
  `create_optimizer(init_lr, num_train_steps, num_warmup_steps, min_lr_ratio=0.0, adam_epsilon=1e-8, weight_decay_rate=0.0, include_in_weight_decay=None)`  
  - Final LR at end: **init_lr * min_lr_ratio**.

- **PyTorch LR schedulers (return `torch.optim.lr_scheduler.LambdaLR`)**:  
  - `get_constant_schedule(optimizer, last_epoch=-1)`  
  - `get_constant_schedule_with_warmup(optimizer, num_warmup_steps, last_epoch=-1)` (linear warmup 0 → base lr)  
  - `get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, last_epoch=-1)` (warmup then linear decay to 0)  
  - `get_cosine_schedule_with_warmup(..., num_cycles=0.5)` (half-cosine to 0)  
  - `get_cosine_with_hard_restarts_schedule_with_warmup(..., num_cycles=1)` (cosine with hard restarts)

</details>

### 📋 # Source: https://discuss.huggingface.co/t/how-can-i-use-evaluates-perplexity-metric-on-a-model-thats-already-loaded/48564
**Source** ·

---

## Related Topics

- [[topics/transformer-architecture|Transformer Architecture]]
- [[topics/tokenization|Tokenization]]
- [[topics/scaling-laws|Scaling Laws]]
- [[topics/lora-peft|LoRA & PEFT]]
- [[topics/rlhf-alignment|RLHF & Alignment]]
- [[topics/synthetic-data|Synthetic Data & Self-Improvement]]
