---
title: "RLHF & Alignment"
subject: "Large Language Models"
date: 2025-01-01
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/yannic-kilcher"
  - "educator/lilian-weng"
  - "educator/chip-huyen"
  - "educator/hugging-face"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Yannic Kilcher"
  - "Lilian Weng"
  - "Chip Huyen"
  - "Hugging Face"
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

# Rlhf Alignment

## Video (best)
- **Andrej Karpathy** — "Let's build the GPT Tokenizer" — *Note: For RLHF specifically, the best available is from Karpathy's broader LLM series, but the most focused RLHF explainer comes from a Stanford lecture*
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zduSFxRajkE)
- **Łukasz Kaiser / Stanford CS224N** — "Reinforcement Learning from Human Feedback" (CS224N 2023 Guest Lecture)
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zjrM-MW-0y0)
- Why: Stanford CS224N guest lectures on RLHF provide rigorous technical grounding covering reward modeling, PPO fine-tuning, and alignment objectives in a structured academic format. Karpathy's own content does not have a dedicated RLHF standalone video as of this writing.
- Level: intermediate/advanced

> ⚠️ **Coverage note**: No single canonical YouTube explainer from the preferred educators (3B1B, Karpathy, Yannic Kilcher) is dedicated solely to RLHF alignment as a standalone video. Yannic Kilcher has covered the InstructGPT paper, which is the closest match.

**Better-confidence alternative:**
- **Yannic Kilcher** — "InstructGPT: Training language models to follow instructions with human feedback (Paper Explained)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=VIARnQFSeHk)
- Why: Kilcher's paper walkthroughs are pedagogically strong — he reads the paper live, explains motivation, critiques methodology, and connects RLHF mechanics (reward model training, PPO loop) to the broader alignment goal. This is the most direct video treatment of RLHF from a trusted educator.
- Level: intermediate

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Reinforcement Learning from Human Feedback (RLHF)"
- **Link:** [https://lilianweng.github.io/posts/2024-11-28-reward-hacking/](https://lilianweng.github.io/posts/2024-11-28-reward-hacking/)
- Why: Weng's post is the gold standard written explainer for RLHF. It systematically covers the three-stage pipeline (SFT → reward model → RL fine-tuning), connects to InstructGPT and ChatGPT, discusses reward hacking and alignment failure modes, and includes clean diagrams. It is comprehensive yet accessible, making it ideal for learners moving from beginner to intermediate.
- Level: intermediate

---

## Deep dive
- **Chip Huyen** — "RLHF: Reinforcement Learning from Human Feedback" (from *Designing Machine Learning Systems* blog / huyenchip.com)
- **Link:** [https://huyenchip.com/2023/05/02/rlhf.html](https://huyenchip.com/2023/05/02/rlhf.html)
- Why: Huyen's deep dive extends beyond mechanics into practical system design considerations — data collection pipelines, labeler disagreement, reward model overfitting, and the transition toward Constitutional AI and DPO. It bridges research and production, which is essential for learners in agentic and LLM application courses. Well-structured with clear sections for progressive reading.
- Level: advanced

---

## Original paper
- **Ouyang et al. (OpenAI)** — "Training language models to follow instructions with human feedback" (InstructGPT)
- **Link:** [https://arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155)
- Why: This is the seminal, most-cited, and most readable paper establishing the RLHF pipeline as applied to large language models. It clearly describes all three stages (SFT, reward model, PPO), includes human evaluation methodology, and directly motivated ChatGPT. The writing is unusually accessible for an OpenAI technical paper, with strong ablations that illuminate each component's contribution.
- Level: intermediate/advanced

---

## Code walkthrough
- **Hugging Face** — "Illustrating Reinforcement Learning from Human Feedback (RLHF)" + TRL library tutorial
- **Link:** [https://huggingface.co/blog/rlhf](https://huggingface.co/blog/rlhf)
- Why: The Hugging Face RLHF blog post combines conceptual explanation with direct pointers to their `trl` library (PPOTrainer, RewardTrainer), making it the most actionable hands-on resource. Learners can go from reading to running code with a real reward model and PPO loop on a small LLM within the same session. The `trl` library is now the de facto open-source implementation standard.
- Level: intermediate

**Supplementary code resource:**
- **Hugging Face TRL documentation / examples**
- **Link:** [https://github.com/huggingface/trl](https://github.com/huggingface/trl)
- Why: Contains runnable scripts for SFT, reward modeling, PPO, and DPO — covering the full RLHF pipeline with modern best practices.
- Level: intermediate/advanced

---

## Coverage notes
- **Strong**: The reward model training stage, PPO-based RLHF loop, and InstructGPT-style alignment are extremely well covered across all resource types. Lilian Weng and Chip Huyen together provide near-complete written coverage.
- **Weak**: **Constitutional AI (CAI)** and **DPO (Direct Preference Optimization)** as alternatives to RLHF are underrepresented in video format from top educators. Most videos focus on the original PPO-based pipeline.
- **Weak**: **Goal drift** and **reward hacking** as failure modes are discussed in blogs but rarely given dedicated video treatment.
- **Gap**: No excellent standalone video from the preferred educator list (3B1B, Karpathy, StatQuest, Serrano) exists specifically for RLHF alignment. Karpathy's "State of GPT" (youtube_id: bZQun8Y4L2A) touches on RLHF briefly and is worth supplementing but is not a dedicated explainer.
- **Gap**: Multimodal RLHF (relevant to `intro-to-multimodal`) has very limited dedicated tutorial coverage outside of research papers (e.g., InstructBLIP, LLaVA RLHF).

---

## Cross-validation
This topic appears in **3 courses**: `intro-to-agentic-ai`, `intro-to-llms`, `intro-to-multimodal`

| Course | Most relevant resources |
|---|---|
| `intro-to-llms` | InstructGPT paper, Lilian Weng blog, Yannic Kilcher video |
| `intro-to-agentic-ai` | Chip Huyen deep dive (reward hacking, goal drift), TRL code walkthrough |
| `intro-to-multimodal` | Gap — no strong multimodal-RLHF specific resource identified; InstructGPT paper + HF blog provide foundations |

Related concepts well-served by these resources:
- ✅ `rlhf`, `reward model`, `supervised fine-tuning` — fully covered
- ✅ `alignment`, `hallucination` — covered in Weng + Huyen
- ⚠️ `dpo` — partially covered (HF TRL has DPO examples; dedicated explainer: https://arxiv.org/abs/2305.18290)
- ⚠️ `constitutional ai` — Anthropic blog post is the primary source (https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback)
- ⚠️ `red teaming` — covered tangentially; dedicated resource would be Perez et al. arxiv paper

---

---

## Additional Resources for Tutor Depth

> **37 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Constitutional AI (CAI) pipeline: critique→revision + RLAIF
**Paper** · [source](https://arxiv.org/pdf/2212.08073.pdf)

*Step-by-step critique→revision supervised phase and the RLAIF preference-data generation + RL phase (how constitutional principles are applied; how preference models are trained/used)*

<details>
<summary>Key content</summary>

- **Overall goal:** Train a *helpful, harmless, non-evasive* assistant **without human harmfulness labels**; human input is a short natural-language **“constitution”** (≈ **16 principles** used in experiments).
- **Stage 1 (Supervised / SL-CAI; Section 3): Critique → Revision → SFT**
  - For each red-teaming prompt, sample an initial response from a helpful RLHF model.
  - Append a **critique request** tied to a sampled constitutional principle; sample critique.
  - Append a **revision request**; sample revised response. Repeat multiple times with **randomly sampled principles each step** (e.g., up to **4 revisions per prompt**).
  - **Training data:** red-team prompts **42,496 human-written + 140,335 model-generated = 182,831**; sample **4 critique-revision pairs per prompt**. Helpfulness prompts: **135,296**; sample **2 responses per prompt**.
  - **SFT hyperparams:** **1 epoch**, constant LR **0.5× pretraining LR**, batch size **1024 sequences**, sampling temperature **T=1**.
  - **Empirical:** revisions improve harmlessness monotonically by human-trained PM scores (Fig. 5); critiques help vs direct revision especially for smaller models (Fig. 7).
- **Stage 2 (RL / RL-CAI; Section 4): AI comparisons → Preference Model (PM) → RL (RLAIF)**
  - Generate **pairs of responses** from SL-CAI policy for harmful prompts.
  - A separate **feedback model** answers a **multiple-choice**: choose (A) vs (B) per a sampled principle; label uses **normalized log-probabilities** as **soft targets** (better than hard 0/1).
  - Train a **PM** on mixed data: **135,296 human helpfulness comparisons + 182,831 AI-labeled harmlessness comparisons**; then do RL using PM as reward (standard RLHF pipeline).
  - **CoT labeling variant:** prompt “Let’s think step-by-step”; CoT makes probabilities extreme → **clamp to 40–60%** (best reported) to reduce brittleness/overreaction.
  - **Design choices:** ensembling over **16 principles** improves robustness; SL stage reduces RL exploration problems; penalize evasiveness by instructing evaluators to prefer *thoughtful non-evasive* harmless answers.
- **Key results (crowdworker Elo):** RL-CAI models become **significantly more harmless** than RLHF/SL-CAI with small helpfulness cost (Figs. 2–3, 8). Label calibration shown as “reasonably well-calibrated” (Fig. 9). Overtraining can cause **Goodharting** (boilerplate “you are valued…”).

</details>

### 📄 Constitutional AI (CAI) training pipeline (SL + RLAIF)
**Paper** · [source](https://arxiv.org/abs/2212.08073)

*Detailed critique→revision supervised phase and RLAIF phase using a preference model trained from AI-generated comparisons guided by a constitution (principles list).*

<details>
<summary>Key content</summary>

- **Goal:** Train a *harmless but non-evasive* assistant **without human labels identifying harmful outputs**; only human input is a **list of principles (“constitution”)** (Abstract).
- **Two-phase training workflow (Abstract):**
  1. **Supervised (SL) self-improvement**
     - Sample prompts and responses from an **initial model**.
     - Generate **self-critiques** of the sampled responses using constitutional principles.
     - Produce **revisions** based on the critiques.
     - **Fine-tune** the original model on the **revised responses** (critique→revision SFT).
  2. **Reinforcement learning via AI feedback (RLAIF)**
     - Sample **two candidate responses** from the **SL-finetuned model**.
     - Use an AI judge guided by the **constitution** to decide **which response is better** (pairwise preference).
     - Train a **preference model (reward model)** on these AI-generated comparisons.
     - Run **RL** using the preference model as the **reward signal** (“RL from AI Feedback”, RLAIF).
- **Design rationale (Abstract + highlights):**
  - **Scalability:** reduces need for large volumes of human preference labels; avoids exposing crowdworkers to harmful content.
  - **Helpfulness–harmlessness trade-off:** CAI aims to reduce “evasive refusals” encouraged by standard RLHF; models **engage** but explain objections to unsafe requests.
  - **Transparency:** principles are in **natural language**; chain-of-thought-style reasoning can improve judged performance and transparency.
- **Example constitutional principle (policy highlight excerpt):** choose the response “a wise, ethical, polite and friendly person would more likely say.”

</details>

### 📄 DPO derivation from KL-regularized RLHF + key pitfalls
**Paper** · [source](https://arxiv.org/html/2410.15595v2)

*Consolidated derivations/variants around DPO and its relationship to KL-regularized RLHF objectives*

<details>
<summary>Key content</summary>

- **RLHF pipeline (Section 2.1):** (1) **SFT** on high-quality responses → initial policy \(\pi_{\text{sft}}\). (2) Collect **pairwise preferences** \((y_w,y_l)\) for prompt \(x\) and train reward model \(r_\phi(x,y)\) via Bradley–Terry. (3) **RL optimization** (e.g., PPO) to maximize reward while staying close to reference \(\pi_{\text{ref}}\) via KL penalty.
- **Bradley–Terry preference likelihood (Eq. 1 / Eq. 2):**  
  \[
  P(y_w \succ y_l \mid x)=\sigma\!\big(r_\phi(x,y_w)-r_\phi(x,y_l)\big)
  \]
  Reward-model MLE loss:
  \[
  \mathcal{L}_{\text{RM}}(\phi)= -\mathbb{E}_{(x,y_w,y_l)}\left[\log \sigma\!\big(r_\phi(x,y_w)-r_\phi(x,y_l)\big)\right]
  \]
  where \(\sigma\) is sigmoid.
- **KL-regularized RLHF objective (Eq. 3):**  
  \[
  \max_\pi\; \mathbb{E}_{x,y\sim \pi(\cdot|x)}[r(x,y)]-\beta\,\mathrm{KL}\!\left(\pi(\cdot|x)\,\|\,\pi_{\text{ref}}(\cdot|x)\right)
  \]
  \(\beta\): KL penalty coefficient.
- **DPO closed-form link policy↔reward (Eq. 4–6):** optimal policy has Boltzmann form  
  \[
  \pi^*(y|x)=\frac{1}{Z(x)}\pi_{\text{ref}}(y|x)\exp\!\left(\tfrac{1}{\beta}r(x,y)\right)
  \]
  Rearranged implicit reward:
  \[
  r(x,y)=\beta\left(\log \pi^*(y|x)-\log \pi_{\text{ref}}(y|x)\right)+\beta\log Z(x)
  \]
- **DPO training loss (Eq. 7–8):** partition function cancels in reward differences; maximize BT likelihood with implicit reward:
  \[
  \mathcal{L}_{\text{DPO}}(\theta)= -\mathbb{E}_{(x,y_w,y_l)}\left[\log \sigma\!\Big(\beta\big(\log\tfrac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)}-\log\tfrac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\big)\Big)\right]
  \]
- **Empirical OOD generalization note (RQ1):** Lin et al. (2024b) reported implicit reward modeling in DPO generalizes worse than explicit RM: **avg accuracy drop 3%**, **max drop 7%** across **5 OOD settings**.
- **Reward hacking/length bias (RQ5):** win-rate correlates with verbosity: Wang et al. (2023b) reported **corr = 0.96** between win rates and **avg # unique tokens**; motivates length-regularized DPO variants.

</details>

### 📄 DPO derivations → closed-form logistic loss
**Paper** · [source](https://arxiv.org/html/2305.18290v3)

*Appendix derivations: (i) KL-constrained reward maximization optimum and (ii) DPO objective under Bradley–Terry/Plackett–Luce → closed-form logistic loss with reference-policy terms and temperature β.*

<details>
<summary>Key content</summary>

- **RLHF objective (Eq. 3, Section 3):**  
  \[
  \max_{\pi}\ \mathbb{E}_{x\sim\mathcal{D},\,y\sim\pi(\cdot|x)}[r(x,y)]-\beta\,\mathbb{D}_{\mathrm{KL}}(\pi(\cdot|x)\,\|\,\pi_{\text{ref}}(\cdot|x))
  \]
  where \(\pi_{\text{ref}}\) is the reference/SFT policy; \(\beta\) controls deviation (KL penalty strength).
- **Optimal policy for KL-constrained reward maximization (Eq. 4; App. A.1):**  
  \[
  \pi^*(y|x)=\frac{1}{Z(x)}\,\pi_{\text{ref}}(y|x)\exp\!\left(\frac{1}{\beta}r(x,y)\right)
  \]
  with partition function \(Z(x)\).
- **Reward reparameterization (Eq. 5):**  
  \[
  r(x,y)=\beta\Big(\log \pi^*(y|x)-\log \pi_{\text{ref}}(y|x)\Big)+\beta\log Z(x)
  \]
  Key trick: in **pairwise differences**, \(\log Z(x)\) cancels.
- **Bradley–Terry preference model (Eq. 1):**  
  \[
  \Pr(y_w \succ y_l|x)=\sigma\big(r(x,y_w)-r(x,y_l)\big)
  \]
- **DPO preference probability (Eq. 6; App. A.2):**  
  \[
  \Pr(y_w \succ y_l|x)=\sigma\!\left(\beta\Big[\Delta_\theta-\Delta_{\text{ref}}\Big]\right)
  \]
  where \(\Delta_\theta=\log\pi_\theta(y_w|x)-\log\pi_\theta(y_l|x)\), \(\Delta_{\text{ref}}=\log\pi_{\text{ref}}(y_w|x)-\log\pi_{\text{ref}}(y_l|x)\).
- **DPO training loss (Eq. 7):** maximize log-likelihood of preferences (binary cross-entropy):  
  \[
  \mathcal{L}_{\text{DPO}}(\theta)= -\mathbb{E}_{(x,y_w,y_l)}\Big[\log \sigma(\beta(\Delta_\theta-\Delta_{\text{ref}}))\Big]
  \]
- **Procedure (Section 4):** (1) collect offline preference pairs \((x,y_w,y_l)\); (2) minimize \(\mathcal{L}_{\text{DPO}}\) (no RL sampling loop).
- **Empirical numbers:** TL;DR summarization win rate vs reference: **DPO ~61% (temp 0.0)** vs **PPO ~57% (temp 0.0)** (Section 6.2). OOD CNN/DM win rate vs ground-truth summaries: **DPO 0.36/0.31** vs **PPO 0.26/0.23** (Table 1; temps 0/0.25).

</details>

### 📄 DPO objective (closed-form log-ratio loss from KL-RLHF)
**Paper** · [source](https://arxiv.org/abs/2305.18290)

*Derivation of the DPO objective from KL-regularized RLHF + practical closed-form log-ratio loss*

<details>
<summary>Key content</summary>

- **RLHF KL-regularized objective (Eq. 3):**  
  \[
  \max_{\pi}\; \mathbb{E}_{x\sim\mathcal{D},\, y\sim \pi(\cdot|x)}\big[r(x,y)\big]\;-\;\beta\,\mathbb{E}_{x}\big[\mathrm{KL}(\pi(\cdot|x)\,\|\,\pi_{\text{ref}}(\cdot|x))\big]
  \]  
  - \(x\)=prompt, \(y\)=completion, \(r(x,y)\)=reward, \(\pi_{\text{ref}}\)=reference/SFT policy, \(\beta\)=KL strength.
- **Closed-form optimal policy under Eq. 3 (Eq. 4):**  
  \[
  \pi^*(y|x)=\frac{1}{Z(x)}\,\pi_{\text{ref}}(y|x)\exp\!\left(\frac{1}{\beta}r(x,y)\right)
  \]
  \(Z(x)\)=partition function.
- **Reward reparameterization via policy log-ratio (Eq. 5):**  
  \[
  r(x,y)=\beta\log\frac{\pi^*(y|x)}{\pi_{\text{ref}}(y|x)}+\beta\log Z(x)
  \]
- **Bradley–Terry preference model (Eq. 1):**  
  \[
  P(y_w \succ y_l \mid x)=\sigma\!\big(r(x,y_w)-r(x,y_l)\big)
  \]
  \(\sigma\)=logistic; \(y_w\)=preferred, \(y_l\)=dispreferred.
- **DPO preference probability (Eq. 6):** partition cancels, yielding  
  \[
  P(y_w \succ y_l \mid x)=\sigma\!\left(\beta\log\frac{\pi(y_w|x)}{\pi_{\text{ref}}(y_w|x)}-\beta\log\frac{\pi(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)
  \]
- **DPO training loss (Eq. 7):** maximize likelihood / minimize BCE over preference pairs \((x,y_w,y_l)\):  
  \[
  \mathcal{L}_{\text{DPO}}(\pi)= -\mathbb{E}\left[\log \sigma\!\left(\beta\log\frac{\pi(y_w|x)}{\pi_{\text{ref}}(y_w|x)}-\beta\log\frac{\pi(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\right)\right]
  \]
- **Procedure (Section 4):** (1) collect offline preference pairs; (2) optimize \(\pi\) with \(\mathcal{L}_{\text{DPO}}\). Often initialize \(\pi\leftarrow \pi_{\text{ref}}\) (SFT); if \(\pi_{\text{ref}}\) unavailable, initialize by MLE on preferred completions.
- **Empirical numbers:** TL;DR summarization: DPO win rate ≈ **61%** (temp 0.0) vs PPO **57%** (temp 0.0). Human eval: DPO (temp 0.25) preferred **58%** over PPO (temp 0). OOD (CNN/DM) GPT-4 win rate: DPO **0.36/0.31** vs PPO **0.26/0.23** (two temps).

</details>

### 📄 Direct Preference Optimization (DPO) objective & link to KL-RLHF
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf)

*Closed-form DPO objective/derivation (logistic loss on preference pairs), explicit connection to KL-regularized RL and the role of the reference policy π_ref.*

<details>
<summary>Key content</summary>

- **Preference model (Bradley–Terry)** (Eq. 1):  
  \(p^*(y_1 \succ y_2 \mid x)=\frac{\exp(r^*(x,y_1))}{\exp(r^*(x,y_1))+\exp(r^*(x,y_2))}=\sigma(r^*(x,y_1)-r^*(x,y_2))\).  
  Dataset \(D=\{(x^{(i)},y_w^{(i)},y_l^{(i)})\}_{i=1}^N\).
- **Reward-model loss** (Eq. 2):  
  \(L_R(r_\phi,D)=-\mathbb{E}_{(x,y_w,y_l)\sim D}\big[\log \sigma(r_\phi(x,y_w)-r_\phi(x,y_l))\big]\).
- **KL-regularized RLHF objective** (Eq. 3):  
  \(\max_{\pi_\theta}\ \mathbb{E}_{x\sim D,\,y\sim\pi_\theta(\cdot|x)}[r_\phi(x,y)]-\beta\,D_{KL}(\pi_\theta(\cdot|x)\|\pi_{ref}(\cdot|x))\).  
  Typically \(\pi_{ref}=\pi_{SFT}\); \(\beta\) controls deviation.
- **Optimal policy under KL constraint** (Eq. 4):  
  \(\pi_r(y|x)=\frac{1}{Z(x)}\pi_{ref}(y|x)\exp(\tfrac{1}{\beta}r(x,y))\).
- **Reward–policy reparameterization** (Eq. 5):  
  \(r(x,y)=\beta\log\frac{\pi_r(y|x)}{\pi_{ref}(y|x)}+\beta\log Z(x)\).  
  In BT differences, \(\log Z(x)\) cancels → preferences depend only on log-ratios.
- **DPO loss (closed form)** (Eq. 7):  
  \(L_{DPO}(\pi_\theta;\pi_{ref})=-\mathbb{E}_{(x,y_w,y_l)\sim D}\Big[\log \sigma\big(\beta\log\frac{\pi_\theta(y_w|x)}{\pi_{ref}(y_w|x)}-\beta\log\frac{\pi_\theta(y_l|x)}{\pi_{ref}(y_l|x)}\big)\Big]\).  
  Implicit reward: \(\hat r_\theta(x,y)=\beta\log\frac{\pi_\theta(y|x)}{\pi_{ref}(y|x)}\).
- **Procedure** (Section 4): (1) sample pairs from \(\pi_{ref}\), label preferences → \(D\); (2) optimize \(\pi_\theta\) by minimizing \(L_{DPO}\). If no SFT: set \(\pi_{ref}=\arg\max_\pi \mathbb{E}_{(x,y_w)\sim D}[\log \pi(y_w|x)]\).
- **Empirical numbers:** TL;DR summarization win rate vs reference summaries: **DPO ~61% (temp 0.0)** vs **PPO ~57% (temp 0.0)**; DPO more robust to sampling temperature. OOD CNN/DailyMail win vs ground-truth summaries (Table 1): **DPO 0.36 (temp 0)** vs **PPO 0.26 (temp 0)**.
- **Hyperparameter sweeps reported:** DPO \(\beta\in\{0.05,0.1,1,5\}\); PPO target KL \(\in\{3,6,9,12\}\).

</details>

### 📄 InstructGPT RLHF objectives (RM loss + PPO-ptx)
**Paper** · [source](https://arxiv.org/abs/2203.02155)

*Explicit PPO objective with KL penalty/constraint (PPO-ptx) + Bradley–Terry/logistic RM loss for pairwise preferences*

<details>
<summary>Key content</summary>

- **3-step RLHF pipeline (Fig. 2; Sec. 3):**
  1) **SFT:** fine-tune GPT-3 on **labeler demonstrations** (≈ **13k** training prompts). Trained **16 epochs**, **cosine LR decay**, **residual dropout 0.2**.  
  2) **Reward Model (RM):** train on **rankings** of model outputs (≈ **33k** training prompts). Labelers rank **K = 4 to 9** responses; train on all \(\binom{K}{2}\) comparisons per prompt as one batch element (efficiency + less overfitting).  
  3) **RL (PPO):** bandit environment: sample prompt \(x\), generate completion \(y\), reward = RM score; add **per-token KL penalty** vs SFT to prevent reward hacking. **Value function initialized from RM**.
- **RM preference loss (Eq. 1; Bradley–Terry/logistic):**  
  \[
  \text{loss}(\theta)= -\frac{1}{\binom{K}{2}}\; \mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma\left(r_\theta(x,y_w)-r_\theta(x,y_l)\right)\right]
  \]
  where \(r_\theta(x,y)\) is scalar reward; \(y_w\) preferred over \(y_l\); \(D\) comparison dataset; \(\sigma\) logistic sigmoid.
- **PPO-ptx combined objective (Eq. 2):**  
  \[
  \text{objective}(\phi)=\mathbb{E}_{(x,y)\sim D_{\pi^{RL}_\phi}}\!\left[r_\theta(x,y)-\beta \log\frac{\pi^{RL}_\phi(y|x)}{\pi^{SFT}(y|x)}\right]+\gamma \mathbb{E}_{x\sim D_{pretrain}}\left[\log \pi^{RL}_\phi(x)\right]
  \]
  \(\beta\)=KL coefficient; \(\gamma\)=pretraining-mix coefficient (**PPO:** \(\gamma=0\); **PPO-ptx:** \(\gamma>0\)).
- **Key empirical results (Abstract/Results):**
  - **1.3B InstructGPT preferred over 175B GPT-3** (human evals).  
  - **175B InstructGPT preferred** to **175B GPT-3: 85 ± 3%**, and to **few-shot prompted 175B GPT-3: 71 ± 4%**.  
  - **Closed-domain hallucination:** **21%** (InstructGPT) vs **41%** (GPT-3).  
  - **Toxicity:** about **25% fewer** toxic outputs vs GPT-3 (RealToxicityPrompts, when prompted to be respectful).

</details>

### 📄 InstructGPT RLHF pipeline (SFT → RM → PPO w/ KL + pretraining mix)
**Paper** · [source](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

*Operational RLHF details (labelers, data, RM, PPO+KL, PPO-ptx) + deployment-relevant outcomes*

<details>
<summary>Key content</summary>

- **3-step RLHF workflow (Sec. 3.1):**  
  1) **SFT** on labeler demonstrations; 2) **Reward Model (RM)** trained on labeler rankings; 3) **PPO** to optimize RM reward, with **per-token KL penalty** to SFT policy; iterate steps 2–3 with new comparisons.
- **Human data ops (Sec. 3.4):** ~**40 contractors** (Upwork/ScaleAI) selected via **screening test**; onboarding + detailed instructions + shared chat. Inter-annotator agreement: **72.6±1.5%** (training labelers) vs **77.3±1.3%** (held-out).
- **Prompt sourcing & filtering (Sec. 3.2):** prompts mainly from **API Playground** (not production); **dedupe** by long common prefix; **≤200 prompts/user**; splits by **user ID**; **PII filtered** from training prompts. Dataset sizes: **SFT 13k**, **RM 33k**, **PPO 31k** prompts.
- **RM loss (Eq. 1):** for prompt \(x\), preferred completion \(y_w\), less-preferred \(y_l\):  
  \[
  \text{loss}(\theta)= -\frac{1}{\binom{K}{2}}\;\mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma(r_\theta(x,y_w)-r_\theta(x,y_l))\right]
  \]
  with **K=4..9** ranked responses; train all \(\binom{K}{2}\) comparisons **as one batch element** to reduce overfitting; RM rewards **normalized** so demonstrations have mean **0** pre-RL.
- **PPO-ptx objective (Eq. 2):**  
  \[
  \mathbb{E}_{(x,y)\sim D_{\pi^\phi_{RL}}}\!\left[r_\theta(x,y)-\beta\log\frac{\pi^\phi_{RL}(y|x)}{\pi_{SFT}(y|x)}\right]+\gamma\,\mathbb{E}_{x\sim D_{pretrain}}[\log \pi^\phi_{RL}(x)]
  \]
  \(\beta\)=KL coef; \(\gamma\)=pretraining-mix coef (**PPO:** \(\gamma=0\)).
- **SFT defaults (Sec. 3.5):** **16 epochs**, cosine LR decay, **residual dropout 0.2**; select checkpoint by **RM score**.
- **Key empirical outcomes (Sec. 4.1):** On held-out API prompts, **1.3B InstructGPT preferred over 175B GPT-3**; **175B InstructGPT preferred over 175B GPT-3 85±3%**, and over **few-shot prompted GPT-3 71±4%**. **Held-out labelers** show similar preferences.
- **Alignment tax mitigation (Sec. 1, 4.2):** PPO can regress on SQuAD/DROP/HellaSwag/WMT; **PPO-ptx** (pretraining mix) greatly reduces regressions **without hurting preference**.

</details>

### 📄 InstructGPT RLHF pipeline (SFT → RM → PPO w/ KL)
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2022/file/b1efde53be364a73914f58805a001731-Paper-Conference.pdf)

*Step-by-step InstructGPT pipeline + RM loss (ranked comparisons) + PPO w/ KL penalty + selection/early-stopping details*

<details>
<summary>Key content</summary>

- **3-step RLHF pipeline (Fig. 2; Sec. 3.1):**
  1) **SFT:** collect **labeler demonstrations** on prompts; supervised fine-tune GPT-3.  
  2) **RM:** collect **labeler rankings** of multiple model outputs per prompt; train reward model to predict preferences.  
  3) **PPO:** optimize SFT policy against RM reward using **PPO** in a **bandit** setup; add **per-token KL penalty from SFT** to prevent reward over-optimization; value function initialized from RM. Steps 2–3 can be iterated with new data.
- **Reward model loss (Eq. 1; Sec. 3.4 RM):** labelers rank **K = 4 to 9** responses; train on all \(\binom{K}{2}\) pairs.  
  \[
  \text{loss}(\theta)= -\frac{1}{\binom{K}{2}}\;\mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma\left(r_\theta(x,y_w)-r_\theta(x,y_l)\right)\right]
  \]
  - \(x\)=prompt, \(y_w\)=preferred completion, \(y_l\)=less-preferred, \(D\)=comparison dataset, \(r_\theta(x,y)\)=scalar RM output, \(\sigma\)=sigmoid.
- **Data + labelers (Sec. 3.2–3.3):** ~**40 contractors**; prompts mostly API + some labeler-written; **>96% English**; PII filtered; train sizes: **SFT 13k prompts**, **RM 33k**, **PPO 31k** (API-only).
- **SFT hyperparams + selection (Sec. 3.4):** **16 epochs**, **cosine LR decay**, **residual dropout 0.2**; select final SFT checkpoint by **RM score on validation** (not val loss).
- **RM choice rationale (Sec. 3.4):** use **6B RM** (compute savings; **175B RM training unstable**, also less suitable as value fn).
- **PPO-ptx rationale (Sec. 4.2):** mix **pretraining-distribution (ptx) gradients** into PPO to reduce regressions on public NLP tasks; performs better than simply increasing KL coefficient.
- **Key empirical results (Abstract; Sec. 4.1):**
  - **1.3B InstructGPT preferred over 175B GPT-3** on their prompt distribution.  
  - **175B InstructGPT preferred to 175B GPT-3: 85 ± 3%**; preferred to **175B GPT-3 few-shot prompted: 71 ± 4%**.
  - Closed-domain hallucination rate: **21% (InstructGPT) vs 41% (GPT-3)**.
  - Inter-annotator agreement: training labelers **72.6 ± 1.5%**; held-out labelers **77.3 ± 1.3%**.

</details>

### 📄 PPO clipped objective & KL-penalty (trust-region-like stability)
**Paper** · [source](https://arxiv.org/pdf/1707.06347.pdf)

*Primary-source definition of PPO clipped surrogate objective + KL-penalty variant; motivation vs TRPO; empirical stability comparisons*

<details>
<summary>Key content</summary>

- **Vanilla policy gradient objective (Eq. 2):**  
  \(L^{PG}(\theta)=\hat{\mathbb E}_t[\log \pi_\theta(a_t|s_t)\,\hat A_t]\). Multiple epochs on \(L^{PG}\) often cause destructively large updates (Sec. 2.1).
- **TRPO surrogate + KL constraint (Eq. 3–4):**  
  Maximize \(\hat{\mathbb E}_t\!\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\hat A_t\right]\)  
  s.t. \(\hat{\mathbb E}_t[KL(\pi_{\theta_{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t))]\le \delta\).
- **KL-penalty form (Eq. 5, 8):**  
  \(L^{KLPEN}(\theta)=\hat{\mathbb E}_t\!\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\hat A_t-\beta\, KL(\pi_{\theta_{old}}(\cdot|s_t),\pi_\theta(\cdot|s_t))\right]\).  
  **Adaptive \(\beta\)** (Sec. 4): compute \(d=\hat{\mathbb E}_t[KL(\cdot)]\); if \(d<d_{targ}/1.5\), \(\beta\leftarrow\beta/2\); if \(d>d_{targ}\times1.5\), \(\beta\leftarrow 2\beta\).
- **Probability ratio (Sec. 3):** \(r_t(\theta)=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{old}}(a_t|s_t)}\), so \(r_t(\theta_{old})=1\).
- **Clipped surrogate objective (Eq. 7):**  
  \(L^{CLIP}(\theta)=\hat{\mathbb E}_t\left[\min\left(r_t(\theta)\hat A_t,\; \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\right)\right]\).  
  Rationale: clipping removes incentive to push \(r_t\) outside \([1-\epsilon,1+\epsilon]\); min makes a pessimistic (lower-bound) surrogate; behaves like TRPO-style trust region while using first-order SGD/Adam.
- **Combined objective (Eq. 9):**  
  \(\hat{\mathbb E}_t[L^{CLIP}_t(\theta)-c_1 L^{VF}_t(\theta)+c_2 S[\pi_\theta](s_t)]\), with \(L^{VF}_t=(V_\theta(s_t)-V^{targ}_t)^2\).
- **PPO training loop (Alg. 1):** collect \(N\) actors × \(T\) steps with \(\pi_{\theta_{old}}\); compute advantages \(\hat A_t\); optimize surrogate for \(K\) epochs with minibatches \(M\le NT\); set \(\theta_{old}\leftarrow\theta\).
- **Empirical stability (Table 1, 7 MuJoCo tasks, 1M steps):** avg normalized score  
  - No clipping/penalty: **-0.39**  
  - Clipping \(\epsilon=0.2\): **0.82** (best among shown)  
  - Clipping \(\epsilon=0.1\): 0.76; \(\epsilon=0.3\): 0.70  
  - Adaptive KL \(d_{targ}=0.01\): 0.74 (worse than clip 0.2)
- **Default hyperparams (Table 3, MuJoCo):** \(T=2048\), Adam lr \(3\times10^{-4}\), epochs 10, minibatch 64, \(\gamma=0.99\), GAE \(\lambda=0.95\).  
  **Atari (Table 5):** \(T=128\), epochs 3, \(\gamma=0.99\), \(\lambda=0.95\), actors 8, \(\epsilon=0.1\times\alpha\), entropy \(c_2=0.01\), VF \(c_1=1\), lr \(2.5\times10^{-4}\times\alpha\) with \(\alpha\) annealed 1→0.

</details>

### 📄 PPO clipped surrogate objective (PPO-Clip)
**Paper** · [source](https://arxiv.org/abs/1707.06347)

*PPO clipped surrogate objective \(L^{\text{CLIP}}(\theta)\) + KL constraint/penalty context (basis for PPO-style RLHF updates)*

<details>
<summary>Key content</summary>

- **Vanilla policy gradient estimator (Eq. 1) / objective (Eq. 2):**  
  \[
  \hat g=\hat{\mathbb E}_t\left[\nabla_\theta \log \pi_\theta(a_t|s_t)\,\hat A_t\right],\quad
  L^{PG}(\theta)=\hat{\mathbb E}_t\left[\log \pi_\theta(a_t|s_t)\,\hat A_t\right]
  \]
  \(\pi_\theta\): stochastic policy; \(\hat A_t\): advantage estimate; \(\hat{\mathbb E}_t\): empirical average over batch.
- **TRPO surrogate + KL constraint (Eq. 3–4):**  
  \[
  \max_\theta \hat{\mathbb E}_t\left[\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}\hat A_t\right]
  \ \text{s.t.}\ 
  \hat{\mathbb E}_t\left[KL(\pi_{\theta_{\text{old}}}(\cdot|s_t),\pi_\theta(\cdot|s_t))\right]\le \delta
  \]
- **KL-penalized variant (Eq. 5):**  
  \[
  \max_\theta \hat{\mathbb E}_t\left[r_t(\theta)\hat A_t-\beta\, KL(\pi_{\theta_{\text{old}}}(\cdot|s_t),\pi_\theta(\cdot|s_t))\right]
  \]
  \(\beta\) hard to tune across tasks/training.
- **PPO ratio + clipped surrogate (Section 3, Eq. 6 + main objective):**  
  \[
  r_t(\theta)=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)},\quad
  L^{CPI}(\theta)=\hat{\mathbb E}_t[r_t(\theta)\hat A_t]
  \]
  \[
  L^{CLIP}(\theta)=\hat{\mathbb E}_t\left[\min\left(r_t(\theta)\hat A_t,\ \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\right)\right]
  \]
  Rationale: clipping removes incentive to push \(r_t\) outside \([1-\epsilon,1+\epsilon]\); min makes a **pessimistic/lower-bound** surrogate; equals \(L^{CPI}\) to first order near \(\theta_{\text{old}}\).
- **Combined training loss (Eq. 9):**  
  \[
  L^{CLIP+VF+S}_t(\theta)=\hat{\mathbb E}_t\left[L^{CLIP}_t(\theta)-c_1 L^{VF}_t(\theta)+c_2 S[\pi_\theta](s_t)\right]
  \]
  \(L^{VF}_t=(V_\theta(s_t)-V^{targ}_t)^2\); \(S\): entropy bonus.
- **Procedure (Section 5):** collect on-policy rollouts with \(N\) actors for \(T\) steps; compute \(\hat A_t\) (e.g., GAE); optimize surrogate with **multiple epochs of minibatch SGD/Adam** per batch.
- **Empirical specifics:** clipping typically uses \(\epsilon=0.2\) (continuous control experiments). Example interpolation plot: updated policy at **KL \(\approx 0.02\)** where \(L^{CLIP}\) maximal (Hopper-v1, first update). Table snippet: **Fixed KL penalty \(\beta=10\)** yields avg normalized score **0.69** (continuous control benchmark).

</details>

### 📄 PPO clipping ≠ trust region; rollback + KL-trigger variants
**Paper** · [source](http://proceedings.mlr.press/v115/wang20b/wang20b-supp.pdf)

*When/why PPO clipping fails to be a trust-region method; theory + empirical evidence; KL-trigger + rollback improves stability/sample efficiency.*

<details>
<summary>Key content</summary>

- **Policy-gradient surrogate (Eq. 1):**  
  \(L_{\pi_{\text{old}}}(\pi)=\mathbb{E}_{s,a}[r_\pi(s,a)A_{\pi_{\text{old}}}(s,a)]+\eta(\pi_{\text{old}})\), where \(r_\pi=\pi(a|s)/\pi_{\text{old}}(a|s)\).
- **TRPO trust-region bound (Thm 1, Eq. 2–3):**  
  \(\eta(\pi)\ge M_{\pi_{\text{old}}}(\pi)=L_{\pi_{\text{old}}}(\pi)-C\max_s D^{s}_{KL}(\pi_{\text{old}},\pi)\), with \(C=\max_{s,a}|A_{\pi_{\text{old}}}(s,a)|\frac{4\gamma}{(1-\gamma)^2}\). TRPO constrains \(\max_s D^{s}_{KL}\le \delta\).
- **PPO clipped objective (Eq. 4–7):**  
  \(L^{CLIP}_t(\theta)=\min(r_tA_t,\;F_{CLIP}(r_t,\epsilon)A_t)\), \(F_{CLIP}=\text{clip}(r_t,1-\epsilon,1+\epsilon)\). Clipping condition: \(r_t\ge 1+\epsilon \land A_t>0\) or \(r_t\le 1-\epsilon \land A_t<0\) ⇒ zero gradient for that sample.
- **Why ratios can still blow up (Thm 2):** even if clipped, overall gradient can push \(r_t\) further out when \(\langle\nabla L^{CLIP}(\theta_0),\nabla r_t(\theta_0)\rangle A_t>0\). Empirically this condition occurs **25%–45%** of samples (1M-sample stats).
- **Clipping does NOT enforce KL trust region (Thm 3):** even with \(1-\epsilon\le r_t\le 1+\epsilon\), \(\sup_{\theta\in\Theta} D^{s_t}_{KL}(\theta_{old},\theta)=\infty\) (discrete \(|A|\ge 3\) and Gaussian continuous).
- **Rollback PPO (Eq. 11):** replace clip with  
  \(F_{RB}(r_t,\epsilon,\alpha)= -\alpha r_t+(1+\alpha)(1\pm\epsilon)\) when out of range; else \(r_t\). Reverses slope (negative incentive). Default **\(\alpha=0.3\)** (Humanoid **0.1**). Improves ratio control (Thm 4).
- **KL-trigger PPO (TR-PPO, Eq. 13–15):** clip when \(D^{s_t}_{KL}(\theta_{old},\theta)\ge \delta\): set \(F_{TR}=r_t(\theta_{old})=1\). Must keep **min(·,·)**; “TR-PPO-simple” (no min) performs extremely badly. Defaults: **\(\delta=0.025\)** (Humanoid/HalfCheetah **0.03**).
- **Combine (TR-PPO-RB, Eq. 16):** if \(D_{KL}\ge\delta\), use \(-\alpha r_t\) (negative incentive). Defaults: **\(\delta=0.03,\alpha=0.05\)** (Humanoid/HalfCheetah \(\alpha=0.1\)).
- **Empirics:** PPO ratios often exceed clip; max ratio **>3** on all tested tasks (with \(\epsilon=0.2\)); some tasks can reach **~40** (noted). PPO KL max grows over training. New methods reduce out-of-range ratios/KL and improve learning.
- **Sample-efficiency (Table 1a, timesteps×10³ to threshold):**  
  Hopper(3000): PPO **273**, PPO-RB **179**, TR-PPO **153**, TR-PPO-RB **130**.  
  Walker2d(3000): PPO **528**, PPO-RB **305**, TR-PPO **345**, TR-PPO-RB **320**.  
  HalfCheetah(2100): PPO **374**, PPO-RB **227**, TR-PPO **266**, TR-PPO-RB **39**.  
  Humanoid(5000, 20M steps): PPO **8410**, TR-PPO **7580**, TR-PPO-RB **6422**.
- **Performance (Table 1b, avg top-10 returns):** Walker2d: PPO **4036**, PPO-RB **4992**, TR-PPO-RB **5011**. HalfCheetah: PPO **1623**, TR-PPO **4672**, TR-PPO-RB **4048**.
- **Training pipeline (“epoch”):** (1) sample \((s_t,a_t)\sim \rho_{\pi_{\theta_{old}}},\pi_{\theta_{old}}\); (2) optimize surrogate to get new \(\theta\); measure ratios/KL per epoch.

</details>

### 📄 RL from Human Preferences (Pairwise Comparisons → Reward Model)
**Paper** · [source](https://arxiv.org/abs/1706.03741)

*Primary-source reward-model training from pairwise comparisons (Bradley–Terry/logistic likelihood over trajectory segment preferences) + full preference-learning loop*

<details>
<summary>Key content</summary>

- **Setup (Section 2):** Human provides preferences over **trajectory segments**  
  \(\sigma=((o_0,a_0),\dots,(o_{k-1},a_{k-1}))\in(\mathcal O\times\mathcal A)^k\). Preference \(\sigma_1\succ\sigma_2\).
- **Training loop (Section 2.2, Fig. 1):** Maintain policy \(\pi(o)\) and reward predictor \(\hat r(o,a)\) (both neural nets), updated asynchronously:  
  1) Roll out \(\pi\) to collect trajectories \(\{\tau^i\}\). Optimize \(\pi\) with standard RL (TRPO/A2C) to maximize \(\sum_t \hat r(o_t,a_t)\).  
  2) Sample segment pairs \((\sigma_1,\sigma_2)\) from trajectories; human labels preference (better / equal / incomparable). Store as triples \((\sigma_1,\sigma_2,\mu)\) where \(\mu\) is a distribution over \(\{1,2\}\) (equal ⇒ uniform; incomparable ⇒ drop).  
  3) Supervised-fit \(\hat r\) to preference data.
- **Preference likelihood (Eq. 1, Bradley–Terry):** Let \(\hat R(\sigma)=\sum_{t=0}^{k-1}\hat r(o_t,a_t)\).  
  \[
  \hat P[\sigma_1\succ\sigma_2]=\frac{\exp(\hat R(\sigma_1))}{\exp(\hat R(\sigma_1))+\exp(\hat R(\sigma_2))}
  \]
  Loss (cross-entropy over dataset \(D\)):  
  \[
  \text{loss}(\hat r)=-\sum_{(\sigma_1,\sigma_2,\mu)\in D}\mu(1)\log \hat P[\sigma_1\succ\sigma_2]+\mu(2)\log \hat P[\sigma_2\succ\sigma_1]
  \]
- **Defaults/mods (Section 2.2.3–2.2.4):** ensemble of predictors (bootstrap resample \(|D|\)); hold out **\(1/e\)** for validation; tune \(\ell_2\) reg so val loss is **1.1–1.5×** train; assume **10%** random-label noise; normalize predicted rewards to **zero mean, fixed std**; query selection via **ensemble disagreement** (variance).
- **Empirical numbers (Abstract/Results):** feedback on **<1%** of interactions; **~700** human comparisons nearly match true-reward RL on MuJoCo tasks; **~900** queries (<1 hour) learn Hopper **backflips**; Atari uses thousands of synthetic comparisons (e.g., **3,300** mentioned for BeamRider/Pong).

</details>

### 📄 RLHF (SFT→RM→PPO) Implementation Details for TL;DR
**Paper** · [source](https://arxiv.org/html/2403.17031v1)

*Step-by-step, reproducibility-oriented RLHF w/ PPO (dataset/tokenization, RM training, PPO tricks, key hyperparams + results)*

<details>
<summary>Key content</summary>

- **RLHF pipeline (Section 2):**
  - **Step 1 SFT:** next-token prediction on human demos (TL;DR reference summaries).
  - **Step 2 RM from preferences:** initialize RM from SFT + linear scalar head; train on pairwise prefs.
    - **RM loss (Eq. 1/2):** for prompt \(x\), chosen \(y^+\), rejected \(y^-\):  
      \[
      \mathcal{L}_{RM}=-\mathbb{E}_{(x,y^+,y^-)\sim D}\left[\log \sigma(r_\theta(x,y^+)-r_\theta(x,y^-))\right]
      \]
      where \(\sigma\) is sigmoid, \(r_\theta\) scalar reward.
  - **Step 3 PPO vs RM:** reward includes RM score + KL penalty (Eq. 3):  
    \[
    R(x,y)=r_\theta(x,y)-\beta\,\mathrm{KL}(\pi_\phi(\cdot|x)\,\|\,\pi_{ref}(\cdot|x))
    \]
    \(\beta\)=KL coeff, \(\pi_\phi\)=policy, \(\pi_{ref}\)=SFT/reference.
- **DPO (Eq. 4/5):** DPO loss uses preference pairs; implicit reward can be extracted from logprob differences (paper notes DPO validation accuracy regresses vs explicit RM).
- **Dataset/tokenization “gotchas” (Section 3):**
  - Query template: `SUBREDDIT… TITLE… POST… TL;DR:`; **no trailing space** after `TL;DR:`.
  - **Truncate by removing last paragraph** if >512 tokens (find last `\n`), not hard token truncation.
  - **Completion processing:** prepend leading space; append EOS `<|endoftext|>`; use distinct `[PAD]` (don’t set pad=eos) to ensure model learns to stop.
  - Padding: **right-pad** query+response for SFT/RM; **left-pad** queries for PPO generation.
- **Critical PPO/RM implementation details:**
  - **Disable dropout** (Detail 7) so PPO ratios/KL are reproducible.
  - **RM reward extracted at EOS token** (Detail 12); non-EOS logits mostly negative/non-valid (Detail 13).
  - **Reward normalization:** shift RM outputs so reference summaries have mean 0 (Detail 15).
  - **“EOS trick” (Detail 23):** sample fixed length (48 tokens; 53 in reproduction), then truncate at EOS; if no EOS, assign constant **-1 reward** → ensures defined reward + encourages concise outputs.
- **Default hyperparameters:**
  - **SFT (Detail 9):** 1 epoch (116,722 episodes), AdamW, cosine LR schedule, batch 128.
  - **RM (Detail 10):** 1 epoch (92,858 episodes), AdamW, cosine, batch 64.
  - **PPO (Detail 20):** 1,000,000 episodes (~8.56 epochs), AdamW, linear schedule, batch 512, \(\beta=0.05\), \(\gamma=1.0\), GAE \(\lambda=0.95\), minibatches=1, PPO epochs=4, clip=0.2, value clip=0.2, vf coef=0.1, temp=0.7.
- **Empirical results (Table 5 + Section 7.1):**
  - RM overall validation accuracy: **1B 0.628±0.002**, **2.8B 0.669±0.003**, **6.9B 0.689±0.004**; CNN/DM OOD accuracy overall: **1B 0.627±0.013**, **2.8B 0.665±0.010**, **6.9B 0.686±0.003**.
  - PPO scaling: GPT judge prefers best **6.9B ~80%** vs reference summaries; 1B can **over-optimize** (high KL ~50–85) with degraded judged preference.

</details>

### 📄 RLHF for Summarization (Reward Model + PPO w/ KL)
**Paper** · [source](https://proceedings.neurips.cc/paper/2020/file/1f89885d556929e98d3ef9b86448f951-Paper.pdf)

*Pairwise preference reward-model likelihood (Bradley–Terry/logistic) + KL-regularized PPO fine-tuning setup end-to-end.*

<details>
<summary>Key content</summary>

- **Pipeline (Section 3.1; Fig. 2):**
  1) Start from **SFT policy** on TL;DR.  
  2) **Collect human comparisons**: for each post *x*, sample summaries from multiple sources (current policy, initial policy, reference, baselines); humans choose better of a pair.  
  3) **Train reward model (RM)** on comparisons.  
  4) **RL fine-tune policy** with PPO to maximize RM reward; repeat iteratively.
- **RM objective = pairwise preference logistic (Section 3.4; Fig. 2):**  
  For comparison data \((x, y^0, y^1, i)\sim D\) where human prefers \(y^i\):  
  **(Eq. RM-loss)** \[
  \text{loss}(r_\theta)=\mathbb{E}\big[\log \sigma(r_\theta(x,y^i)-r_\theta(x,y^{1-i}))\big]
  \]
  - \(r_\theta(x,y)\): scalar RM score (logit); \(\sigma\): logistic sigmoid; \(D\): human judgments dataset.  
  - RM outputs **normalized** so dataset reference summaries have **mean score 0**.
- **RL reward with KL penalty (Section 3.4):**  
  **(Eq. PPO-reward)** \[
  R(x,y)=r_\theta(x,y)-\beta \log\frac{\pi^{RL}_\phi(y|x)}{\pi^{SFT}(y|x)}
  \]
  - \(\pi^{RL}_\phi\): learned policy; \(\pi^{SFT}\): original supervised model; \(\beta\): KL coefficient.  
  - Rationale: KL term (i) encourages exploration / prevents mode collapse, (ii) keeps policy near RM training distribution.
- **RL setup defaults (Section 3.4):** reward only at end of summary; episode ends at EOS; **discount \(\gamma=1\)**; PPO time step = **BPE token**. Separate **value network** (Transformer) to avoid damaging pretrained policy; value net initialized from RM parameters.
- **Key empirical numbers (Section 4.1):**
  - On TL;DR, **1.3B RLHF** preferred over reference **61%** vs **6.7B SFT 43%** (raw preference vs reference).  
  - Length-control reduces RLHF-vs-reference preference by **~5%**, but **6.7B RLHF still ~65%** preferred vs reference.
- **Over-optimization finding (Section 4.3; Fig. 5):** increasing optimization strength (via KL coefficient/penalty) initially improves human preference, then degrades; RM predictions can become **anti-correlated** with human preferences.
- **Data scale (Section 4.3; Fig. 6):** doubling RM training data → **~+1.1%** validation accuracy; doubling model size → **~+1.8%**.
- **Human data quality (Section 3.3):** labeler–researcher agreement **77% ± 2%**; researcher–researcher **73% ± 4%**.
- **Compute cost (Section 5):** 6.7B RL fine-tuning ≈ **320 GPU-days**.

</details>

### 📄 RLHF pipeline for Helpful & Harmless assistant (Anthropic, 2022)
**Paper** · [source](https://arxiv.org/abs/2204.05862)

*Primary-source RLHF pipeline details + robustness finding (reward vs KL) + online iteration cadence*

<details>
<summary>Key content</summary>

- **Overall training pipeline (RLHF):**  
  1) **Supervised Fine-Tuning (SFT):** fine-tune a pretrained LM on human-written assistant demonstrations to get an initial instruction-following policy.  
  2) **Preference / Reward Model (RM):** collect human preference comparisons between candidate assistant responses; train a model to predict which response is preferred (used as a scalar reward).  
  3) **RL optimization with KL regularization:** optimize the policy to maximize RM reward while penalizing divergence from the SFT initialization (keeps behavior close to the starting policy; improves stability/harmlessness).
- **Iterated online RLHF (weekly cadence):** preference models and RL policies are **updated weekly** using **fresh human feedback**, improving datasets/models over time (online data collection → RM update → RL update loop).
- **Robustness / scaling relation (empirical):** identifies a **roughly linear relationship** between **RL reward** and **√(KL divergence)** between the RL policy and its initialization (i.e., reward increases approximately linearly with the square root of KL from the starting policy).
- **Compatibility claim (empirical, broad):** alignment training **improves performance on almost all NLP evaluations** and is **compatible with specialized skills** training (e.g., **Python coding** and **summarization**).
- **Additional analyses mentioned:** calibration, competing objectives, OOD detection, comparisons with human writers, and prompt-based samples (useful for evaluation discussion).

</details>

### 📄 RLHF recipe for summarization (Stiennon et al. 2020)
**Paper** · [source](https://arxiv.org/abs/2009.01325)

*Concrete RLHF pipeline: reward model from pairwise comparisons + PPO policy optimization with KL-to-SFT; human preference results + transfer.*

<details>
<summary>Key content</summary>

- **Motivation (Intro/Abstract):** ROUGE and MLE-on-references are weak proxies for “summary quality”; optimize **human preferences** directly.
- **Pipeline (Section 3; Fig. 2):**
  1. **SFT baseline**: fine-tune pretrained GPT-3 model on TL;DR reference summaries (used to initialize policy + RM; also used to sample candidates for comparisons). Final eval sampling uses **temperature T=0**.
  2. **Collect human comparisons**: for each post \(x\), humans choose preferred summary among two candidates \(y_0,y_1\).
  3. **Train reward model (RM)**: start from SFT model + linear scalar head \(r_\theta(x,y)\).
  4. **Optimize policy with RL (PPO)** against RM reward, iterating data collection if desired.
- **RM loss (pairwise Bradley–Terry style; Section 3):** if human prefers \(y_i\),
  \[
  \text{loss}(r_\theta)= -\mathbb{E}_{(x,y_0,y_1,i)\sim D}\left[\log \sigma\big(r_\theta(x,y_i)-r_\theta(x,y_{1-i})\big)\right]
  \]
  where \(\sigma\) is logistic sigmoid; \(D\) is comparison dataset. RM outputs normalized so **reference summaries have mean score 0**.
- **RL objective with KL penalty (Section 3):**
  \[
  R(x,y)= r_\theta(x,y) - \beta \log\frac{\pi^{RL}_\phi(y|x)}{\pi^{SFT}(y|x)}
  \]
  where \(\beta\) controls KL-to-reference (SFT) regularization.
- **Key empirical results (TL;DR):**
  - Human-feedback **1.3B** policy beats supervised model **10× larger**: **61% vs 43%** raw preference vs reference summaries.
  - Controlling for length reduces preference vs references by **~5%** (length explains ~⅓ of gap at 6.7B).
  - Human-feedback models preferred **over the human demonstrations** in the dataset.
- **Generalization/transfer (CNN/DM):** Reddit-trained RLHF summaries transfer to CNN/DM **without news-specific fine-tuning**, nearly matching human references on Likert quality axes.
- **RM generalization numbers:** RM agrees with labelers on CNN/DM **62.4% (1.3B)**, **66.5% (6.7B)**; inter-labeler agreement **66.9%**. Minimal-edit preference: **79.4% (1.3B)**, **82.8% (6.7B)**; role-reversal perturbations: **92.9% / 97.2%**.
- **Scaling trends:** doubling RM data → **~+1.1%** val accuracy; doubling RM size → **~+1.8%**.
- **Failure mode (over-optimization; Sec. 4.3):** with too much optimization, RM prediction and true human preference diverge; can become **anti-correlated**.
- **Cost (Limitations):** RL fine-tuning **6.7B** required **~320 GPU-days**.
- **Dataset released:** **64,832** TL;DR comparison pairs.

</details>

### 📄 Reference policy in DPO (what π_ref does + how β matters)
**Paper** · [source](https://arxiv.org/html/2407.13709v2)

*Formal treatment of the reference policy in DPO (π_ref meaning, implied reward/regularization, and effects of β)*

<details>
<summary>Key content</summary>

- **KL-constrained RL objective (Eq. 1–2):**  
  Maximize over policy \( \pi_\theta(y|x)\):  
  \[
  \mathbb{E}_{y\sim \pi_\theta(\cdot|x)}[r(x,y)]-\beta\,\mathrm{KL}(\pi_\theta(\cdot|x)\,\|\,\pi_{\text{ref}}(\cdot|x))
  \]
  where \(\pi_{\text{ref}}\) is the **reference policy** (typically the SFT model) and \(\beta\) controls KL penalty strength.
- **DPO objective (Eq. 5) via Bradley–Terry (Eq. 3–4):** preference likelihood with sigmoid \(\sigma\).  
  Implicit reward parameterization (Eq. 6):  
  \[
  r_\theta(x,y)=\beta\big(\log \pi_\theta(y|x)-\log \pi_{\text{ref}}(y|x)\big)
  \]
- **Dense/token reward view (Eq. 7–8):** token-level credit proportional to log-prob gap; statistic  
  \(\Delta_t=\log \pi_\theta(y_t|x,y_{<t})-\log \pi_{\text{ref}}(y_t|x,y_{<t})\). Smaller \(\beta\) → more extreme token shifts; EOS heavily downweighted → longer outputs.
- **Empirical β sensitivity (Table 1, AlpacaEval2 length-controlled):**  
  - mistral-7b SFT: **7.57**; DPO best at **β=0.01 → 16.25**, β=0.02 → 16.06; too small β=0.005 → **12.36**.  
  - tulu-2-7b SFT: **8.50**; DPO best at **β=0.02 → 10.46**; β=0.005 **degenerate**.
- **Ranking accuracy trend (Table 2):** smaller β improves policy ranking accuracy but risks degeneration (e.g., mistral-7b policy acc rises from **0.495 (β=0.1)** to **0.704 (β=0.005)**).
- **Training pipeline (Section 3):** UltraFeedback-binarized (64K instruction + pos/neg pair, GPT-4 scored); DPO for **3 epochs**, batch **32**, linear LR schedule with **10% warmup**; checkpoint by **validation loss** (interval **500 steps**).  
- **Stronger reference policies (Section 6):** can help only if “compatible”; optimal β becomes larger (often **β≈1.0** with suitable strong refs vs **0.01–0.02** when self/SFT ref).

</details>

### 📊 DPO vs PPO best practices (Ivison et al. 2024/2026)
**Benchmark** · [source](https://arxiv.org/html/2406.09279v2)

*Tabulated ablations isolating preference data, algorithm (DPO vs PPO), reward model scale/data, and policy prompts; downstream eval deltas.*

<details>
<summary>Key content</summary>

- **PPO pipeline (Sec. 2.1):** (1) Train **reward model** on preference pairs \((x, y_w, y_l)\). (2) During policy training, sample \(y \sim \pi_\theta(\cdot|x)\), score with RM to get scalar reward \(r_\phi(x,y)\). (3) Optimize PPO objective with **KL penalty** to reference policy \(\pi_{\text{ref}}\) (usually SFT init): maximize \( \mathbb{E}[r_\phi(x,y)] - \beta\,\mathrm{KL}(\pi_\theta||\pi_{\text{ref}})\). Authors note **tuning KL coefficient \(\beta\)** is important.
- **DPO (Sec. 2.1, Eq. 3):** Offline optimization directly on preference pairs; increases margin between \(\log \pi_\theta(y_w|x)\) and \(\log \pi_\theta(y_l|x)\) while staying close to reference (implicit KL via reference model).
- **Preference data matters most (Sec. 3.1, Table 1):** Best dataset **Synthetic UltraFeedback (fine-grained per-aspect)** average **61.0** vs Tülu2 SFT **56.8**; instruction following **52.8** vs **44.2**, truthfulness **69.3** vs **56.6** (≈ **+8–13** category gains). Chatbot Arena data harms safety (e.g., 2024 safety **58.1**).
- **PPO vs DPO (Sec. 3.2, Table 2):** Using same labeled data (subsampled to **60,908**): UltraFeedback(FG) **PPO avg 62.2** vs **DPO 61.0**. Average PPO–DPO deltas: **Reasoning +1.3**, **Coding +2.9**, **Safety +2.3**, **Truthfulness −2.5**, **Overall +0.7**.
- **Reward model scaling (Sec. 3.3, Table 3):** Better RM ≠ much better policy. 70B UltraF RM improves PPO GSM **58.0** vs 13B UltraF RM **53.0**; overall avg **62.8** vs **62.2** (small). Direct RM eval: RewardBench **79.8** (13B Mix RM) vs **61.0** (13B UltraF RM).
- **Policy prompts (Sec. 3.4):** Targeted prompts help **only** when aligned to target task + strong RM; GSM-train prompts + 70B RM yields ~**46%→62%** GSM (≈ **+16**). Mixed prompts for generalist setting often **drops** overall (Table 4).

</details>

### 📊 PPO vs DPO for RLHF—limitations, tuning, and benchmarks
**Benchmark** · [source](https://arxiv.org/abs/2404.10719)

*Head-to-head PPO-RLHF vs DPO/DPO-Iter comparisons + PPO ablations (stability/hyperparameter sensitivity) on dialogue + code tasks.*

<details>
<summary>Key content</summary>

- **RLHF objective (Eq. 2, Sec. 3):** maximize  
  \[
  \mathbb{E}_{x\sim D,\; y\sim \pi_\theta(\cdot|x)}[r(x,y)]-\beta\,\mathrm{KL}(\pi_\theta(\cdot|x)\,\|\,\pi_{\text{ref}}(\cdot|x))
  \]
  where \(x\)=prompt, \(y\)=response, \(r\)=reward (or learned RM), \(\pi_{\text{ref}}\)=reference/SFT model, \(\beta\)=KL weight.
- **Reward model training (Eq. 3–4):** Bradley–Terry preference likelihood  
  \[
  P(y_w \succ y_l|x)=\sigma(r_\phi(x,y_w)-r_\phi(x,y_l))
  \]
  Train \(r_\phi\) by NLL over preference pairs \((x,y_w,y_l)\).
- **DPO link to RLHF optimum (Eq. 5–7):** optimal policy form  
  \[
  \pi^*(y|x)\propto \pi_{\text{ref}}(y|x)\exp(r(x,y)/\beta)
  \]
  and DPO directly optimizes policy on preference pairs via log-ratio objective (Eq. 7).
- **Key theoretical claim (Thm 4.1):** policies reachable by PPO (with RM trained on data) are a **proper subset** of DPO minimizers; DPO can admit **biased/OOD-exploiting** solutions when preference data has narrow coverage.
- **Empirical: SafeRLHF (Table 2):**  
  - SFT(Alpaca): Help −2.62, Harm +1.50, Safety rate 41.6%  
  - **PPO:** Help +1.69, Harm −12.08, SR 99.5%  
  - **DPO:** Help −4.19, Harm −0.97, SR 55.4%  
  - DPO improves with distribution-shift mitigation: +SFT(Safe) SR 71.8%; filtering dual-safe yields SR 95.8% but hurts helpfulness (Help −2.86).
  - **DPO-Iter** SR rises to 99.9% by Iter.3–4 but helpfulness stays low (≈ −3).
- **PPO ablations (Table 3):** baseline PPO on APPS degrades vs SFT; adding **Advantage Normalization**, **Large Batch**, then **Reference EMA** improves: CodeContest pass@1k **7.7% → 15.4% → 19.6% → 21.4%**; APPS Intro pass@5 **18.0% → 38.1% → 42.3% → 44.4%**.
- **Benchmarks (Sec. 6):**
  - **CodeContest:** CodeLlama-34B SFT test 10@1k 15.2%; **DPO 0.0%**, DPO-Iter 3.2%; **PPO 22.4%** (beats AlphaCode-41B 16.4% test 10@1k).
  - **HH-RLHF (Table 4–5):** PPO reward 0.718 vs DPO 0.611; GPT-4 pairwise: PPO vs DPO = **42 win / 28 tie / 30 lose**.

</details>

### 📊 PPO vs DPO in Preference Learning (NeurIPS 2024)
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2024/file/404df2480b6eef0486a1679e371894b0-Paper-Conference.pdf)

*Head-to-head PPO vs DPO results + ablations (data quality, RM scaling, prompts) + explicit KL-regularized objective*

<details>
<summary>Key content</summary>

- **PPO objective (Eq. 2, KL-regularized):**  
  \[
  \max_{\pi_\theta}\ \mathbb{E}_{x\sim D_\pi,\ y\sim \pi_\theta(\cdot|x)}[R_\psi(x,y)]\ -\ \beta\, D_{KL}(\pi_\theta\ \|\ \pi_{ref})
  \]  
  - \(D_\pi\): policy-training prompts (unlabeled); \(R_\psi\): reward model; \(\pi_{ref}\): reference policy (usually SFT init); \(\beta\): KL penalty coefficient (tuned; important).
- **Reward model training loss (Eq. 1):**  
  \[
  L_R(\psi)=-\mathbb{E}_{(x,y_c,y_r)\sim D_R}\big[\log \sigma(R_\psi(x,y_c)-R_\psi(x,y_r))\big]
  \]  
  - \(D_R\): preference pairs; \(y_c\) chosen, \(y_r\) rejected.
- **DPO loss (Eq. 3):**  
  \[
  L_{DPO}(\theta)=-\mathbb{E}\Big[\log \sigma\big(\beta\log\frac{\pi_\theta(y_c|x)}{\pi_{ref}(y_c|x)}-\beta\log\frac{\pi_\theta(y_r|x)}{\pi_{ref}(y_r|x)}\big)\Big]
  \]
- **Empirical: PPO > DPO (Table 2, 13B; same data, subsampled to 60,908 ex; p<0.05).** Avg ∆ (PPO−DPO): **Reasoning +1.3**, **Coding +2.9**, **Safety +2.3**, **Truthfulness −2.5**, **Overall +0.7**.  
  UltraFeedback(FG): **DPO avg 61.0 vs PPO avg 62.2**.
- **Preference data quality dominates (Sec. 3.1/Table 1):** UltraFeedback fine-grained **avg 61.0** vs SFT **56.8**; biggest gains in **instruction following & truthfulness (up to +8 pts)**; factuality ~flat (~1 pt spread).
- **Reward model scaling (Table 3):** 70B UltraF RM boosts **GSM 58.0 vs 53.0** (13B UltraF RM) and **avg 62.8 vs 62.2** (small overall gain); RM improvements on RewardBench/BoN often **don’t translate** broadly downstream.
- **Policy prompts (Sec. 3.4/Fig. 3/Table 4):** In-domain GSM prompts + strong (70B) RM can raise GSM **46%→62%** (+16); “mixed” prompt remix **does not improve** generalist overall performance.

</details>

### 📖 Accelerate essentials for distributed training knobs
**Reference Doc** · [source](https://huggingface.co/docs/accelerate/index)

*Distributed training configuration knobs (mixed precision, gradient accumulation, FSDP/DeepSpeed integration points)*

<details>
<summary>Key content</summary>

- **Minimal integration pattern (core workflow)**
  1) `from accelerate import Accelerator`  
  2) `accelerator = Accelerator(...)` (auto-detects hardware/distributed setup)  
  3) Wrap objects: `model, optimizer, train_dl, eval_dl = accelerator.prepare(model, optimizer, train_dl, eval_dl)`  
  4) Replace backprop: `accelerator.backward(loss)` (instead of `loss.backward()`)  
  5) Launch: `accelerate launch script.py`
- **Key configuration knobs (constructor / config file)**
  - `mixed_precision`: supports `fp16`, `bf16`, `fp8` (hardware-dependent; fp8 noted for Hopper/H100-class GPUs).
  - `gradient_accumulation_steps`: increases effective batch size without increasing per-device batch.
  - Distributed strategy selectable via config: DDP / DP, **FSDP** (parameter/grad/optimizer-state sharding), **DeepSpeed** (ZeRO stages, accumulation, mixed precision).
- **Design rationale**
  - Reduces PyTorch DDP boilerplate (process group init, device placement, distributed samplers, DDP wrapping) while keeping the *same* user-defined training loop structure.
  - `prepare()` centralizes: device placement, wrapping model with backend (e.g., DDP/FSDP), enabling mixed precision, and sharding dataloaders per process.
- **Distributed data sharding rule (BatchSamplerShard)**
  - Each process yields batches where: **(Eq. 1)** `idx % num_processes == process_index`  
    - `idx`: batch index from original sampler; `num_processes`: world size; `process_index`: rank.
  - `split_batches` (bool) controls whether batches are split across processes vs. each process taking whole batches.

</details>

### 📖 DeepSpeed config knobs that change memory/throughput
**Reference Doc** · [source](https://www.deepspeed.ai/docs/config-json/)

*Concrete config fields (batch sizing, ZeRO stages/offload, fp16/bf16, gradient clipping)*

<details>
<summary>Key content</summary>

- **Batch size identity (Eq. 1):**  
  `train_batch_size = train_micro_batch_size_per_gpu * gradient_accumulation_steps * num_gpus`  
  - `train_batch_size`: effective batch per optimizer update  
  - `train_micro_batch_size_per_gpu`: per-GPU batch per fwd/bwd  
  - `gradient_accumulation_steps`: steps to accumulate before update (default **1**)  
  DeepSpeed can infer the 3rd value if you set any 2.
- **Gradient clipping:** `gradient_clipping` (float), default **1.0**.
- **Mixed precision modes (mutual exclusivity):**
  - `fp16` dict (cannot combine with `amp`): defaults include `enabled:false`, `loss_scale:0.0` (dynamic), `initial_scale_power:16` (scale=2^16), `loss_scale_window:1000`, `hysteresis:2`, `min_loss_scale:1`.
  - `bf16` dict (cannot combine with `fp16` or `amp`): `enabled:false`; options `bf16_master_weights_and_grads`, `bf16_optimizer_states`.
  - `amp` not compatible with **ZeRO** (per doc).
  - `torch_autocast`: `enabled:false`, `dtype:"bfloat16"`, `lower_precision_safe_modules` default includes Linear/Conv*.
- **ZeRO optimization (`zero_optimization.stage`):**  
  Stage **0/1/2/3** = disabled / partition optimizer states / partition optimizer+gradients / partition optimizer+gradients+parameters.  
  Common defaults: `allgather_bucket_size:5e8`, `reduce_bucket_size:5e8`, `overlap_comm:false`, `reduce_scatter:true`, `contiguous_gradients:true`.
- **Offload constraints:**
  - `offload_param` (params to **cpu|nvme**) is **stage 3 only**; defaults: `device:"cpu"`, `nvme_path:"/local_nvme"`, `buffer_count:5`, `buffer_size:1e8`, `max_in_cpu:1e9`, `pin_memory:false`.
  - `offload_optimizer` valid for **stage 1/2/3**; NVMe only with **stage 3**; defaults: `device:"cpu"`, `ratio:1`, `buffer_count:4`, `pin_memory:false`.
  - `cpu_offload` is **deprecated** (use `offload_optimizer`).

</details>

### 📖 GPT-4 System Card — Deployment safety & eval methodology
**Reference Doc** · [source](https://cdn.openai.com/papers/gpt-4-system-card.pdf)

*Operational safety/deployment practices + evaluation framing (risk areas, mitigations, monitoring, red teaming)*

<details>
<summary>Key content</summary>

- **Training pipeline (2-stage):** (1) Pre-train on large internet text to predict next token; (2) fine-tune with **RLHF** to produce outputs preferred by human labelers (Intro).
- **Model variants compared:** **GPT-4-early** (instruction-following, minimal mitigations) vs **GPT-4-launch** (fine-tuned for increased helpfulness/harmlessness; reflects mitigations) (Sec. 1.1).
- **Risk areas explicitly evaluated (list):** hallucinations; harmful content; representation/allocation/QoS harms; disinformation/influence ops; weapons proliferation; privacy; cybersecurity; risky emergent behaviors; interactions with other systems; economic impacts; acceleration; overreliance (Sec. 2).
- **Qualitative eval procedure:** iterative “red teaming” (stress/boundary/adversarial testing) starting Aug 2022; **>50 external experts** across domains (fairness, mis/disinfo, chemistry/biorisk, cybersecurity, nuclear, econ, HCI, law, education, healthcare, etc.); iterative rounds as mitigations added (Sec. 2.1.1).
- **Quantitative eval procedure:** internal automated evals for policy categories (e.g., hate, self-harm advice, illicit advice). Prompts designed to elicit each category; outputs labeled via **classifiers + human analysis**; used to compare checkpoints/models (Sec. 2.1.2).
- **Empirical results (hallucinations):** GPT-4-launch scored **+19 percentage points** vs latest GPT-3.5 at avoiding **open-domain** hallucinations; **+29 pp** at avoiding **closed-domain** hallucinations (Sec. 2.2).
- **Mitigation levers used:** reduce policy-violating content in pretraining data; fine-tune to **refuse** illicit instructions; reduce hallucinations using prior usage data; reduce jailbreak surface using prior exploit data; train new risk-vector classifiers integrated into monitoring/enforcement (Sec. 1.1).
- **Emergent/agentic risk eval:** ARC tested autonomous replication/resource acquisition with tool loop; preliminary finding: GPT-4 versions tested **ineffective** at autonomous replication “in the wild” (Sec. 2.9).

</details>

### 📖 OpenAI Safety Evaluations Hub (public eval categories + metrics)
**Reference Doc** · [source](https://openai.com/safety/evaluations-hub/)

*Publicly described safety evaluation categories + downloadable evaluation data (disallowed content, jailbreaks, hallucinations/factuality, instruction hierarchy)*

<details>
<summary>Key content</summary>

- **Purpose & usage:** OpenAI runs evaluations to measure model **safety and performance**, publishes results **ongoing** (not just at launch). Results are used **internally** as *one input* to safety/deployment decisions and are also included in **system cards**.
- **Scope (text-based) evaluation categories (4):**
  1. **Disallowed content:** checks model **does not comply** with requests violating policy (e.g., hateful content, illicit advice).
  2. **Jailbreaks:** adversarial prompts intended to **circumvent safety training** and induce harmful output.
  3. **Hallucinations:** measures **factual errors**.
  4. **Instruction hierarchy:** measures adherence to instruction priority: **system > developer > user**.
- **Disallowed content / overrefusal scoring (autograder):**
  - **Metric 1: `not_unsafe`** = output is not unsafe per OpenAI policy/model spec.
  - **Metric 2: `not_overrefuse`** = model does not refuse a benign/good request.
  - Includes **disaggregated sub-metrics** for higher-severity categories; has **Standard** and harder **“Challenge”** test sets.
- **Jailbreak evaluation sets:** includes **StrongReject** (academic jailbreak benchmark) + **human-sourced jailbreaks** (from human red teaming).
- **Empirical ranges reported (hub summary article):**
  - Disallowed content refusal effectiveness near **0.99** for many models; benign-handling (`not_overrefuse`) top around **0.80**, others **0.65–0.79**.
  - StrongReject robustness **0.23–0.85**; human jailbreak robustness **0.90–1.00**.
  - Hallucination benchmarks: **SimpleQA accuracy 0.09–0.59**, hallucination rate **0.41–0.86**; **PersonQA accuracy 0.17–0.70**, hallucination rate **0.13–0.52**.
  - Instruction hierarchy: system-vs-user **0.50–0.85**; developer-vs-user **0.15–0.77**; system-vs-developer **0.55–0.93**.
- **Design rationale:** evaluation methods are updated as older tests **saturate** (stop differentiating models) and to address **new modalities/emerging risks**.

</details>

### 📖 PPO-Clip objective + KL early stopping (Spinning Up)
**Reference Doc** · [source](https://spinningup.openai.com/en/latest/algorithms/ppo.html)

*Side-by-side PPO-Clip vs PPO-Penalty framing; explicit PPO-Clip surrogate objective + intuition; practical KL target / early stopping; implementation hyperparameters.*

<details>
<summary>Key content</summary>

- **Motivation (Background):** Take the largest improvement step using current on-policy data **without** moving policy so far that performance collapses. PPO is a simpler first-order alternative to TRPO.
- **Two PPO variants:**
  - **PPO-Penalty:** adds a **KL-divergence penalty** to approximate a KL-constrained update; **automatically adjusts** penalty coefficient during training.
  - **PPO-Clip (focus; “primary variant used at OpenAI”):** **no KL term / no hard constraint**; uses **clipping** to remove incentives to move far from old policy.
- **PPO-Clip surrogate objective (Eq. 1, simplified form):**  
  Let \(r_t(\theta)=\frac{\pi_\theta(a_t|s_t)}{\pi_{\theta_{\text{old}}}(a_t|s_t)}\), advantage \(\hat A_t\), clip \(\epsilon\).  
  \[
  L^{\text{CLIP}}(\theta)=\mathbb{E}_t\Big[\min\big(r_t(\theta)\hat A_t,\ \text{clip}(r_t(\theta),1-\epsilon,1+\epsilon)\hat A_t\big)\Big].
  \]
  **Intuition:**  
  - If \(\hat A_t>0\): objective increases with \(r_t\) until \(r_t>1+\epsilon\), then capped at \((1+\epsilon)\hat A_t\).  
  - If \(\hat A_t<0\): objective increases as \(r_t\) decreases until \(r_t<1-\epsilon\), then capped at \((1-\epsilon)\hat A_t\).
- **Procedure detail (“You Should Know”):** Despite clipping, policy can drift; Spinning Up uses **early stopping**: stop policy gradient steps if **mean KL(new‖old)** exceeds a threshold.
- **Defaults / key hyperparameters (PyTorch/TF docs):**
  - `clip_ratio` \(\epsilon\): **0.1–0.3 typical**, default **0.2**
  - `target_kl`: **0.01 or 0.05 typical**, default **0.01** (used for early stopping)
  - `steps_per_epoch` **4000**, `epochs` **50**, `gamma` **0.99**, `lam` **0.97**
  - `train_pi_iters` **80** (max; may stop early), `train_v_iters` **80**
  - `pi_lr` **3e-4**, `vf_lr` **1e-3**, `max_ep_len` **1000**
- **Implementation note:** PPO does **multiple minibatch SGD steps** per epoch to maximize \(L^{CLIP}\); on-policy sampling from current stochastic policy.

</details>

### 📖 TRL DPO/ORPO dataset schema (prompt/chosen/rejected)
**Reference Doc** · [source](https://discuss.huggingface.co/t/orpo-dpo-dataset-clarification/103637/2)

*Exact dataset schema expectations for DPO/ORPO in TRL; how to derive `(prompt, chosen, rejected)` from chat-style preference data.*

<details>
<summary>Key content</summary>

- **TRL `DPOTrainer` expected dataset format:** a **triple** of columns/fields  
  **(prompt, chosen, rejected)**  
  - `prompt`: the input context shown to the model  
  - `chosen`: the preferred continuation/response (given the prompt)  
  - `rejected`: the less-preferred continuation/response (given the prompt)
- **Common real-world preference dataset situation:** many datasets provide only **chosen/rejected** as **full chat transcripts** (often including roles like `user`/`assistant`) where the user prompt appears repeated inside both `chosen` and `rejected`.
- **Procedure to convert chat transcripts → TRL triple:**
  1. **Select the first message** in the transcript as the **`prompt`**.
  2. Put the remaining **N−1 messages** (the continuation after the first message) into **`chosen`** and **`rejected`** respectively.  
     - This matches the pattern: prompt = initial user turn; chosen/rejected = rest of conversation/assistant continuation.
  3. Reference implementation is pointed to in the Alignment Handbook code (`alignment-handbook/src/alignment/data.py`, lines ~73–90 in the linked commit).
- **Design rationale / note:** TRL currently requires the explicit triple, but maintainers suggest it could be simplified in the future to accept just chosen/rejected (would require refactoring).

</details>

### 📖 TRL DPOTrainer (API + dataset schema + key knobs)
**Reference Doc** · [source](https://huggingface.co/docs/trl/en/dpo_trainer)

*Authoritative DPOTrainer configuration (β/temperature, reference model handling, loss variants) and expected dataset schema for preference pairs*

<details>
<summary>Key content</summary>

- **DPO objective (core idea):** train on preference pairs (prompt *x*, preferred completion *y_w*, dispreferred *y_l*) to increase the **log-likelihood margin** of *y_w* vs *y_l* **relative to a reference model** π_ref, without an explicit reward model. Uses a **classification-style loss** with sigmoid; **β** controls preference strength / deviation from reference.  
  - Implicit rewards logged:  
    - `rewards/chosen = β * (log πθ(y_w|x) − log πref(y_w|x))`  
    - `rewards/rejected = β * (log πθ(y_l|x) − log πref(y_l|x))`  
    - `rewards/margins = rewards/chosen − rewards/rejected`
- **Expected dataset (preference format):** must contain `chosen` and `rejected`, optionally `prompt` (recommended).  
  - Standard explicit: `{"prompt": "...", "chosen": "...", "rejected": "..."}`  
  - Standard implicit: `{"chosen": "...", "rejected": "..."}`  
  - Conversational explicit: `prompt/chosen/rejected` are lists of `{role, content}`; chat template auto-applied.
- **Reference model handling (DPOTrainer `ref_model`):**
  - If `ref_model` provided: used directly for reference log-probs.
  - If `None`: reference is the **initial policy** (model state before DPO starts).
- **Key config defaults (DPOConfig):** `beta=0.1`, `loss_type=["sigmoid"]`, `max_length=1024`, `truncation_mode="keep_start"`, `learning_rate=1e-6`, `gradient_checkpointing=True`, `disable_dropout=True`, `precompute_ref_log_probs=False`, `sync_ref_model=False`.
- **Loss variants (`loss_type`):** `"sigmoid"` (default), `"hinge"` (β is reciprocal margin), `"ipo"` (β is τ), `"exo_pair"` (requires `label_smoothing>0`, rec. `1e-3`), `"robust"` (`label_smoothing` in `[0,0.5)`), `"aot"`/`"aot_unpaired"`, `"apo_zero"`/`"apo_down"`, `"discopop"` (temperature `discopop_tau=0.05`), `"bco_pair"`, `"sppo_hard"`, `"sft"`. Supports **multi-loss** lists + `loss_weights` (e.g., MPO: `["sigmoid","bco_pair","sft"]` with `[0.8,0.2,1.0]`).
- **Constraints:** `sync_ref_model=True` incompatible with `precompute_ref_log_probs=True`; `precompute_ref_log_probs` not supported with `IterableDataset`; `use_weighting=True` not supported with AOT losses.

</details>

### 📖 TRL DPOTrainer / DPOConfig API (losses, β, reference model)
**Reference Doc** · [source](https://huggingface.co/docs/trl/main/en/dpo_trainer)

*Authoritative parameter names/semantics for `DPOTrainer`/`DPOConfig` in TRL (β/temperature, reference model handling, loss variants)*

<details>
<summary>Key content</summary>

- **DPO objective (core loss):** For prompt \(x\), preferred completion \(y_w\) (chosen), dispreferred \(y_l\) (rejected), policy \(\pi_\theta\), reference \(\pi_{\text{ref}}\), sigmoid \(\sigma\), and hyperparameter \(\beta\):  
  \[
  \mathcal{L}_{\text{DPO}} = -\log \sigma\Big(\beta\big[(\log \pi_\theta(y_w|x)-\log \pi_\theta(y_l|x))-(\log \pi_{\text{ref}}(y_w|x)-\log \pi_{\text{ref}}(y_l|x))\big]\Big)
  \]
  (Doc “Computing the loss”). **Rationale:** aligns to preferences without an explicit reward model; typically suppresses rejected likelihood.
- **Dataset format (preference pairs):** examples must contain `prompt` + `chosen` + `rejected` (standard text or conversational messages). Conversational datasets auto-apply chat template.
- **Reference model handling (`DPOTrainer(ref_model=...)`):**
  - If `ref_model` provided: used directly for reference log-probs.
  - If `None`: reference is the **initial policy** (model state before DPO training).
- **Key `DPOConfig` defaults:** `loss_type=["sigmoid"]`, `beta=0.1`, `max_length=1024`, `truncation_mode="keep_start"`, `disable_dropout=True`, `learning_rate=1e-6`, `logging_steps=10`, `gradient_checkpointing=True`, `precompute_ref_log_probs=False`, `sync_ref_model=False`.
- **Loss variants (`loss_type`):** `"sigmoid"`, `"hinge"`, `"ipo"`, `"exo_pair"` (requires `label_smoothing>0`, rec. `1e-3`), `"nca_pair"`, `"robust"` (`label_smoothing` in \([0,0.5)\)), `"bco_pair"`, `"sppo_hard"`, `"aot"`, `"aot_unpaired"`, `"apo_zero"`, `"apo_down"`, `"discopop"` (uses `discopop_tau`, default `0.05`), `"sft"`.
- **Multi-loss (MPO-style):** `loss_type=[...]` + `loss_weights=[...]` (example: `["sigmoid","bco_pair","sft"]` with `[0.8,0.2,1.0]`).
- **Constraints:** `sync_ref_model=True` incompatible with `precompute_ref_log_probs=True`; `precompute_ref_log_probs` not supported with `IterableDataset`; `use_weighting=True` not supported with AOT losses.
- **Logged metrics:** `rewards/chosen = logπθ - logπref`, `rewards/rejected`, `rewards/margins`, `rewards/accuracies`, plus `logps/*`, `logits/*`, `entropy`, `mean_token_accuracy`, etc.
- **VLM note:** set `DPOConfig(max_length=None)` to avoid truncating image tokens.

</details>

### 📖 TRL PPOTrainer (API + key PPO knobs)
**Reference Doc** · [source](https://huggingface.co/docs/trl/en/ppo_trainer)

*Authoritative parameter names/semantics for `trl.experimental.ppo.PPOTrainer` + `PPOConfig` defaults; logged metrics meanings; rollout/generation controls.*

<details>
<summary>Key content</summary>

- **Core objective components (logged):**
  - **Non-score reward (Eq. 1):** `objective/non_score_reward = beta * kl.sum(1)`  
    - `beta` = KL penalty coefficient (`PPOConfig.kl_coef`)  
    - `kl` = per-token KL divergence between policy and reference.
  - **RLHF reward (Eq. 2):** `objective/rlhf_reward = score - non_score_reward`  
    - `score` = reward model output (`objective/scores`).
- **Debugging heuristics (procedural):**
  - `objective/rlhf_reward` should increase if PPO training is working.
  - `val/ratio` should hover near **1.0**; it is clipped by `--cliprange 0.2`. Ratios like **2.0**, **1000.0**, or **0.1** indicate overly drastic updates.
- **EOS trick (design rationale):** `missing_eos_penalty` subtracts a **positive** scalar penalty from the score when no EOS is generated; encourages coherent/shorter completions (shorter than `max_new_tokens`).
- **Empirical result (TL;DR benchmark):** Judge eval (GPT-4o mini) win rate: **SFT 33.00%** vs **PPO 64.70%** preferred.
- **Key classes / signatures:**
  - `PPOTrainer(args: PPOConfig, processing_class, model, ref_model=None, reward_model, train_dataset, value_model, ...)`
  - If `ref_model=None`, a **copy of the policy model** is created for KL computation.
- **`PPOConfig` PPO-specific defaults (selected):**
  - `learning_rate=3e-6`, `gradient_checkpointing=True`, `logging_steps=10`
  - PPO: `num_ppo_epochs=4`, `num_mini_batches=1`, `kl_coef=0.05`, `kl_estimator='k1'|'k3' (default 'k1')`, `cliprange=0.2`, `vf_coef=0.1`, `cliprange_value=0.2`, `gamma=1.0`, `lam=0.95`, `whiten_rewards=False`
  - Generation/rollout: `response_length=53`, `temperature=0.7`, `num_sample_generations=10`, `local_rollout_forward_batch_size=64`, `stop_token` mutually exclusive with `stop_token_id`
  - ZeRO-3: `ds3_gather_for_generation=True` (faster gen; disable to fit larger-than-single-GPU models).

</details>

### 📖 TRL PPOTrainer (API + key metrics)
**Reference Doc** · [source](https://huggingface.co/docs/trl/main/en/ppo_trainer)

*Authoritative parameter names/semantics for `trl.experimental.ppo.PPOTrainer` + `PPOConfig` (KL control, clipping, batching, reward shaping, logging)*

<details>
<summary>Key content</summary>

- **Core reward decomposition (Eq. 1):**  
  - `objective/non_score_reward = beta * kl.sum(1)` where `beta = kl_coef` and `kl` is **per-token KL** between policy and reference.  
  - `objective/rlhf_reward = score - non_score_reward` where `score = objective/scores` (reward model output).
- **Key logged PPO diagnostics (definitions):**
  - `objective/kl`: mean KL(current policy || reference policy).  
  - `policy/approxkl_avg`: approx KL between consecutive PPO policies (not same as `objective/kl`).  
  - `val/ratio`: mean prob ratio (new/old); should hover ~1.0; clipped by `--cliprange 0.2`.  
  - `policy/clipfrac_avg`, `val/clipfrac_avg`: fraction of updates clipped (policy/value).  
  - `objective/entropy`, `policy/entropy_avg`: action randomness.
- **Training workflow (scripted):** run `examples/scripts/ppo/ppo.py` with SFT model path + reward model path; recommends **“EOS trick”**: `missing_eos_penalty` subtracts a positive scalar from `score` if completion lacks EOS to encourage coherent/shorter completions.
- **Empirical benchmark (TL;DR, 1B model):** GPT-4o mini judge win-rate: **SFT 33.00%** vs **PPO 64.70%** preferred.
- **PPOTrainer constructor (API):** `PPOTrainer(args: PPOConfig, processing_class, model, ref_model=None, reward_model, train_dataset, value_model, ...)`. If `ref_model=None`, **copies policy model** for KL reference.
- **Key PPOConfig defaults (selected):** `learning_rate=3e-6`, `num_ppo_epochs=4`, `num_mini_batches=1`, `local_rollout_forward_batch_size=64`, `response_length=53`, `temperature=0.7`, `kl_coef=0.05`, `kl_estimator='k1'` (or `'k3'` lower variance), `cliprange=0.2`, `cliprange_value=0.2`, `vf_coef=0.1`, `gamma=1.0`, `lam=0.95`, `num_sample_generations=10`, `gradient_checkpointing=True`.

</details>

### 📋 # Source: https://discuss.huggingface.co/t/negative-kl-values-during-ppo-training-trl-library/84143
**Source** · 

### 📋 # Source: https://discuss.huggingface.co/t/new-version-of-ppotrainer/118316
**Source** · 

### 📋 # Source: https://github.com/huggingface/trl
**Source** · 

### 📋 # Source: https://www.anthropic.com/news/constitutional-ai-harmlessness-from-ai-feedback
**Source** · 

### 🔍 InstructGPT instruction-following via RLHF (key results & pipeline)
**Explainer** · [source](https://openai.com/index/instruction-following/)

*Human-evaluation preference results + comparisons across SFT vs RLHF variants (InstructGPT vs GPT‑3; safety metrics; alignment-tax mitigation)*

<details>
<summary>Key content</summary>

- **Core empirical preference result:** Human labelers **prefer outputs from the 1.3B InstructGPT model over outputs from 175B GPT‑3**, despite **>100× fewer parameters** (API prompt distribution).
- **Preference robustness:** InstructGPT is **significantly preferred** over GPT‑3 on prompts submitted to **both** InstructGPT and GPT‑3 models on the API; holds even when GPT‑3 prompts are prefixed to induce an “instruction-following mode.”
- **Safety/quality metrics (directional, named benchmarks):**
  - **Fewer imitative falsehoods** vs GPT‑3 on **TruthfulQA**.
  - **Less toxic** vs GPT‑3 on **RealToxicityPrompts**.
  - Human eval on API prompts: **hallucinates less often** and produces **more appropriate outputs**.
  - Other harms on API distribution (sexual/violent content, denigrating protected class, encouraging abuse): **no significant improvement**; incidence **equally low** for both.
- **Comparative generalization:** On customer prompt distribution, InstructGPT outputs are **preferred over FLAN and T0**, suggesting academic instruction datasets aren’t fully representative of deployed use.
- **Training pipeline (RLHF, PPO):**
  1) Collect **human-written demonstrations** on API prompts → **supervised fine-tuning (SFT) baseline**.  
  2) Collect **human rankings** of multiple model outputs on more API prompts.  
  3) Train a **reward model (RM)** to predict labeler preference.  
  4) **RL fine-tune** the policy to maximize RM reward using **PPO**.
- **Design rationale / compute note:** Fine-tuning uses **<2%** of pretraining compute+data; mainly **elicits/unlocks** pretrained capabilities rather than teaching many new ones.
- **Alignment tax mitigation:** During RL fine-tuning, **mix a small fraction of original GPT‑3 pretraining data** and train with **log-likelihood maximization**; found **more effective than increasing the KL coefficient**; maintains safety/preferences while reducing academic-task regressions.

</details>

### 📋 PPO policy training w/ KL control (lm-human-preferences)
**Code** · [source](https://github.com/openai/lm-human-preferences/blob/cbfd210bb8b08f6bc5c26878c10984b90f516c66/lm_human_preferences/train_policy.py)

*Reference implementation of policy optimization from human preferences: PPO loop + reward shaping with KL penalty (fixed/adaptive), batching across MPI ranks, and default hyperparameters.*

<details>
<summary>Key content</summary>

- **Training objective (reward shaping) (Eq. 1):**  
  - Per-token KL term: `kl = logprobs - ref_logprobs` (same shape as tokens).  
  - Non-score reward: `r_kl = - kl_coef * kl`.  
  - Final per-token reward: `rewards = r_kl; rewards[:, -1] += scores` (scalar preference score added only to last token).  
  - Returns `(rewards, non_score_reward, kl_coef)` from `compute_rewards(...)`.
- **KL controllers:**
  - **FixedKLController:** `kl_coef` constant (`update` is no-op).
  - **AdaptiveKLController update (Eq. 2):**  
    - `proportional_error = clip(current/target - 1, -0.2, 0.2)`  
    - `mult = 1 + proportional_error * n_steps / horizon`  
    - `kl_coef *= mult`  
    - Defaults: `target=None` (must be set if used), `horizon=10000` episodes.
- **Default PPO hyperparameters (PpoHParams):**  
  `total_episodes=2_000_000`, `batch_size=64`, `nminibatches=1`, `noptepochs=4`, `lr=5e-6`, `vf_coef=0.1`, `cliprange=0.2`, `cliprange_value=0.2`, `gamma=1`, `lam=0.95`, `whiten_rewards=True`.
- **Batching across MPI ranks:**  
  - `per_rank_rollout_batch_size = batch_size / comm_size`  
  - `per_rank_minibatch_size = per_rank_rollout_batch_size / nminibatches`  
  - Whitening constraint: minibatch size ≥ 8 (also enforced per-rank).
- **Training loop procedure:** initialize vars → `sync_models()` (broadcast/sync score model + ref_policy + policy params) → repeat until `global_step < ceil(total_episodes/batch_size)`: `ppo_trainer.step()` → `global_step += 1` → periodic checkpoint save (`save_interval`).

</details>

---

## Related Topics

- [[topics/pre-training|Pre-Training]]
- [[topics/reinforcement-learning|Reinforcement Learning]]
- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/reasoning-models|Reasoning Models]]
- [[topics/synthetic-data|Synthetic Data & Self-Improvement]]
