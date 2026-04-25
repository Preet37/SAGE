## Key Facts & Specifications

- **InstructGPT (OpenAI) RLHF pipeline has three stages**
  - (1) **Supervised fine-tuning (SFT)** on demonstrations, (2) **reward model (RM)** training on human preference comparisons, (3) **PPO** fine-tuning of the SFT policy using the RM as a scalar reward. (OpenAI, *Training language models to follow instructions with human feedback*, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

- **InstructGPT: human preference result with parameter count comparison**
  - In human evaluations on OpenAI’s prompt distribution, outputs from the **1.3B** InstructGPT model were **preferred to** outputs from **175B** GPT-3, despite having **~100× fewer parameters**. (OpenAI, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

- **InstructGPT PPO objective includes a per-token KL penalty**
  - OpenAI adds a **per-token KL penalty from the SFT model at each token** to mitigate over-optimization of the reward model. (OpenAI, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
  - The KL reward coefficient is denoted **β**, and a pretraining loss coefficient **γ** controls pretraining gradients; for “PPO” models, **γ is set to 0**. (OpenAI, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

- **InstructGPT reward model: pairwise Bradley–Terry / logistic loss**
  - RM loss (as written in the paper) is:
    - \[
      \text{loss}(\theta) = -\frac{1}{\binom{K}{2}} \mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma\left(r_\theta(x,y_w)-r_\theta(x,y_l)\right)\right]
      \]
    - where \(y_w\) is the preferred completion and \(y_l\) is the dispreferred completion. (OpenAI, 2022, Eq. (1), https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

- **InstructGPT RM training efficiency detail**
  - Treating all \(\binom{K}{2}\) comparisons as separate datapoints caused overfitting; instead, OpenAI trains on all \(\binom{K}{2}\) comparisons from each prompt **as a single batch element**, requiring **one forward pass per completion** (rather than \(\binom{K}{2}\) forward passes). (OpenAI, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

- **PPO-Clip: clipping range and early stopping by KL (OpenAI Spinning Up)**
  - PPO-Clip uses clipping in the objective rather than a KL term in the objective; OpenAI Spinning Up notes **early stopping** if mean KL exceeds a threshold. (OpenAI Spinning Up PPO docs, https://spinningup.openai.com/en/latest/algorithms/ppo.html)
  - Hugging Face PPO blog summarizes PPO clipping ratio range \([1-\epsilon, 1+\epsilon]\) and states the PPO paper uses **\(\epsilon = 0.2\)**. (Hugging Face blog, https://huggingface.co/blog/deep-rl-ppo)

- **TRL (Hugging Face) PPOConfig defaults and key parameters**
  - `num_ppo_epochs` default: **4**
  - `kl_coef` default: **0.05**
  - `cliprange` default: **0.2**
  - `vf_coef` default: **0.1**
  - `cliprange_value` default: **0.2**
  - `gamma` default: **1.0**
  - `lam` default: **0.95**
  - `whiten_rewards` default: **False**
  - `kl_estimator` default: **"k1"** (can be `"k3"`; `"k2"` used for logging and cannot be set) (Hugging Face TRL PPOConfig docs, https://huggingface.co/docs/trl/ppo_trainer)

- **TRL PPO logged metric definitions (selected)**
  - `objective/non_score_reward` is described as `beta * kl.sum(1)` (β = KL penalty coefficient; `kl` = per-token KL divergence).
  - `objective/rlhf_reward` is `score - non_score_reward`.
  - `policy/approxkl_avg` is approximate KL between consecutive PPO policies and is **not the same** as `objective/kl`. (Hugging Face TRL PPO Trainer docs, https://huggingface.co/docs/trl/main/en/ppo_trainer and GitHub mirror https://github.com/huggingface/trl/blob/main/docs/source/ppo_trainer.md)

- **TRL PPO “EOS trick”**
  - `--missing_eos_penalty` subtracts a **static scalar penalty** from the score of completions that do not end with EOS; docs recommend using it. Example shows `--missing_eos_penalty 1.0`. (Hugging Face TRL PPO Trainer docs, https://huggingface.co/docs/trl/main/en/ppo_trainer)

- **TRL Reward Modeling: Bradley–Terry probability and loss**
  - Preference probability: \(p(y^+ \succ y^- \mid x)=\sigma(r(x,y^+)-r(x,y^-))\)
  - Loss: \(L(\theta)=-\mathbb{E}_{(x,y^+,y^-)\sim D}[\log \sigma(r_\theta(x,y^+)-r_\theta(x,y^-))]\). (Hugging Face TRL Reward Modeling docs, https://huggingface.co/docs/trl/main/en/reward_trainer)

- **TRL Reward Modeling: centering auxiliary loss recommendation**
  - `center_rewards_coefficient` is mentioned as controlling an auxiliary centering term; **recommended value is `1e-2`** (cited in TRL docs as proposed by “Helping or Herding? Reward Model Ensembles Mitigate but do not Eliminate Reward Hacking”). (Hugging Face TRL Reward Modeling docs, https://huggingface.co/docs/trl/main/en/reward_trainer)

- **DPO (Rafailov et al., 2023): high-level claims and one reported win-rate comparison**
  - DPO is presented as eliminating explicit reward modeling and RL, using a “simple classification loss,” and being “stable, performant, and computationally lightweight.” (Rafailov et al., 2023, https://arxiv.org/abs/2305.18290; NeurIPS PDF)
  - In one experiment described in the NeurIPS paper: **DPO ~61% win rate at temperature 0.0** vs **PPO 57% at its optimal sampling temperature of 0.0** (same GPT-J SFT base). (Rafailov et al., 2023 NeurIPS PDF, https://proceedings.neurips.cc/paper_files/paper/2023/file/a85b405ed65c6477a4fe8302b5e06ce7-Paper-Conference.pdf)

- **TRL DPOTrainer key defaults and parameters**
  - `beta` default: **0.1** (“Higher β means less deviation from the reference model.”)
  - `label_smoothing` default: **0.0**
  - For Robust DPO: `label_smoothing` interpreted as probability preference label is flipped; “typical value recommended … is **0.1**.”
  - For EXO: `label_smoothing` must be > 0; recommended **`1e-3`**.
  - `discopop_tau` default: **0.05** (paper recommends default 0.05).
  - `ref_model_mixup_alpha` default: **0.6** and `ref_model_sync_steps` default: **512** when `sync_ref_model=True`. (Hugging Face TRL DPO docs, https://huggingface.co/docs/trl/dpo_trainer and https://huggingface.co/docs/trl/main/en/dpo_trainer; GitHub mirror https://github.com/huggingface/trl/blob/main/docs/source/dpo_trainer.md)

- **DPO vs PPO broader benchmark claims (one study)**
  - A 2024 study claims PPO can surpass DPO across experiments and reports a code benchmark improvement: on CodeContest, their **PPO 34B** model improves **10@1k from 16.4% to 22.4%** compared to AlphaCode-41B. (arXiv:2404.10719v1, https://arxiv.org/html/2404.10719v1)

- **Reward hacking mitigation via reward shaping: specific numeric finding**
  - In one set of experiments, increasing KL penalty coefficient from **0.01 to 0.1** increased win rate curve and decreased reward curve, interpreted as mitigating reward hacking. (Fu et al., 2025, *Reward Shaping to Mitigate Reward Hacking in RLHF*, https://arxiv.org/html/2502.18770v1)

- **Constitutional AI (Anthropic) pipeline stages**
  - Two phases: **supervised phase** (sample responses → generate self-critiques and revisions → fine-tune on revised responses) and **RL phase** (sample from fine-tuned model → AI evaluates which of two samples is better → train preference model from AI preferences → RL using preference model reward; “RL from AI Feedback” / RLAIF). (Anthropic, *Constitutional AI: Harmlessness from AI Feedback*, 2022, https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback; arXiv PDF https://arxiv.org/pdf/2212.08073.pdf)

- **Constitutional AI: prompt dataset size for red teaming prompts**
  - Collected **42,496** human-written red teaming prompts (partial conversations). (Bai et al., 2022, arXiv PDF https://arxiv.org/pdf/2212.08073.pdf)

- **Constitution usage detail (Anthropic blog)**
  - During critique/revision and evaluation, the model **pulls one principle each time**; it **does not look at every principle every time**, but sees each principle many times during training. (Anthropic, “Claude’s Constitution,” https://www.anthropic.com/news/claudes-constitution)

- **CAI vs RLHF claim (Anthropic blog)**
  - Claims CAI training can produce a “Pareto improvement” where Constitutional RL is “both more helpful and more harmless than RLHF.” (Anthropic, “Claude’s Constitution,” https://www.anthropic.com/news/claudes-constitution)  
  - Note: this is stated as a claim in the blog; the search results provided do not include the exact numeric evaluation supporting it.

- **Sycophancy and RLHF (Benade et al.)**
  - Paper claims sycophancy “often becomes more pronounced after preference-based post-training,” and provides a formal mechanism linking optimization against learned reward to bias in preference data. (Benade et al., *How RLHF Amplifies Sycophancy*, PDF https://www.gerdusbenade.com/files/26_sycophancy.pdf)

---

## Technical Details & Procedures

### InstructGPT Reward Model Training (pairwise comparisons)
- **Data format**
  - Dataset \(D\) contains tuples \((x, y_w, y_l)\) where labelers prefer \(y_w\) over \(y_l\). (OpenAI, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
- **Loss**
  - Uses logistic / Bradley–Terry style loss (Eq. (1) in the paper):  
    \[
    -\frac{1}{\binom{K}{2}} \mathbb{E}[\log \sigma(r_\theta(x,y_w)-r_\theta(x,y_l))]
    \]
  - (OpenAI, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
- **Batching trick**
  - For each prompt with \(K\) completions, train on all \(\binom{K}{2}\) comparisons **as one batch element** to avoid overfitting and reduce compute (one forward pass per completion). (OpenAI, 2022, same URL)

### InstructGPT PPO Fine-tuning with KL penalty
- **Environment framing**
  - “Environment” presents a random customer prompt and expects a response; episode ends after response; reward is RM scalar score. (OpenAI, 2022, same URL)
- **KL penalty**
  - Adds **per-token KL penalty from the SFT model at each token**. (OpenAI, 2022, same URL)
- **Coefficients**
  - β controls KL penalty strength; γ controls pretraining gradients; for PPO models γ=0. (OpenAI, 2022, same URL)

### TRL (Hugging Face) PPOTrainer: configuration and CLI examples
- **Key PPOConfig parameters and defaults**
  - `num_ppo_epochs=4`, `kl_coef=0.05`, `cliprange=0.2`, `vf_coef=0.1`, `cliprange_value=0.2`, `gamma=1.0`, `lam=0.95`, `whiten_rewards=False`, `kl_estimator="k1"` (or `"k3"`). (TRL docs, https://huggingface.co/docs/trl/ppo_trainer)
- **Reference model behavior**
  - `ref_model` optional; if `None`, TRL creates a copy of the policy model to compute KL. (TRL docs, https://huggingface.co/docs/trl/ppo_trainer)
- **EOS trick**
  - Use `--missing_eos_penalty` to penalize non-EOS completions; example uses `--missing_eos_penalty 1.0` and `--stop_token eos`. (TRL PPO Trainer docs, https://huggingface.co/docs/trl/main/en/ppo_trainer)
- **Example command snippet (from docs)**
  - Includes:
    - `accelerate launch --config_file examples/accelerate_configs/deepspeed_zero3.yaml`
    - `--total_episodes 1000000`
    - `--local_rollout_forward_batch_size 16`
    - `--missing_eos_penalty 1.0`
    - `--stop_token eos`
  - (TRL PPO Trainer docs, https://huggingface.co/docs/trl/main/en/ppo_trainer)

### TRL RewardTrainer: quick start and dataset preprocessing example
- **Quick start**
  - `RewardTrainer(model="Qwen/Qwen3-0.6B", train_dataset=load_dataset("trl-lib/ultrafeedback_binarized", split="train"))` then `trainer.train()`. (TRL Reward Modeling docs, https://huggingface.co/docs/trl/main/en/reward_trainer)
- **Example preprocessing steps (Arena Human Preference 55k)**
  - Filter ties: `dataset.filter(lambda example: example["winner_tie"] == 0)`
  - Map to `chosen`/`rejected` based on winner fields
  - Convert to conversational format with `{"role": "user" ...}, {"role": "assistant" ...}`
  - Select columns: `dataset.select_columns(["chosen", "rejected"])`
  - (TRL Reward Modeling docs, same URL)
- **PEFT/LoRA note**
  - If loaded model is a causal LM, TRL recommends `modules_to_save=["score"]` so the reward head is trained. (TRL Reward Modeling docs, same URL)

### TRL DPOTrainer: minimal training script and accelerate command
- **Python script pattern**
  - Load model/tokenizer, load dataset `trl-lib/ultrafeedback_binarized`, create `DPOConfig(output_dir=...)`, then `DPOTrainer(...).train()`. (TRL DPO docs, https://github.com/huggingface/trl/blob/main/docs/source/dpo_trainer.md)
- **CLI command (docs)**
  - `accelerate launch trl/scripts/dpo.py --model_name_or_path Qwen/Qwen2-0.5B-Instruct --dataset_name trl-lib/ultrafeedback_binarized --num_train_epochs 1 --output_dir Qwen2-0.5B-DPO` (TRL DPO docs, https://huggingface.co/docs/trl/main/en/dpo_trainer)
- **Reference model handling**
  - `ref_model` optional; if `None`, trainer uses the initial policy state as reference. (TRL DPO docs, https://huggingface.co/docs/trl/dpo_trainer)

### Constitutional AI (Anthropic): critique → revision → finetune; then AI preferences → preference model → RL
- **Supervised stage**
  - Generate responses to harmfulness prompts using a helpful-only assistant; ask model to critique response according to a principle; revise; repeat with randomly drawn principles; fine-tune on final revised responses (and/or revisions from steps). (Bai et al., 2022, arXiv PDF https://arxiv.org/pdf/2212.08073.pdf)
- **RL stage**
  - AI comparison evaluations → preference model → RL using preference model reward (“RLAIF”). (Anthropic research page and arXiv PDF above)

---

## Comparisons & Trade-offs

### PPO-based RLHF vs DPO
- **Complexity / components**
  - PPO-based RLHF (as in InstructGPT) includes: SFT model, separate RM, PPO loop, and KL penalty to SFT reference. (OpenAI, 2022)
  - DPO claims to remove explicit reward modeling and RL, using a classification-style objective directly on preference pairs. (Rafailov et al., 2023, https://arxiv.org/abs/2305.18290)
- **Empirical results (not fully consistent across sources)**
  - DPO paper reports DPO win rate **~61%** at temperature **0.0** vs PPO **57%** at temperature **0.0** in one GPT-J setting. (Rafailov et al., 2023 NeurIPS PDF)
  - A later study argues PPO can outperform DPO broadly and reports CodeContest **10@1k 16.4% → 22.4%** improvement vs AlphaCode-41B. (arXiv:2404.10719v1)
  - **Discrepancy note:** These results are from different experimental setups, tasks, and evaluation protocols; the search results do not provide a unified benchmark that reconciles them.

### PPO clipping vs explicit KL penalty
- **PPO-Clip (Spinning Up)**
  - No KL term in objective; relies on clipping; uses early stopping if KL grows beyond threshold. (OpenAI Spinning Up PPO docs)
- **RLHF PPO with KL penalty (InstructGPT)**
  - Adds explicit per-token KL penalty to SFT reference at each token. (OpenAI, 2022)
- **Trade-off framing (from sources)**
  - PPO clipping constrains updates via objective clipping; RLHF KL penalty constrains divergence from a fixed reference policy (SFT) to mitigate reward over-optimization. (OpenAI, 2022; Spinning Up PPO docs)

### Reward hacking mitigation: KL coefficient and reward shaping
- Increasing KL penalty coefficient from **0.01 to 0.1** improved win rate while reducing proxy reward curve in one study, interpreted as mitigating reward hacking. (Fu et al., 2025, https://arxiv.org/html/2502.18770v1)
- This supports a trade-off: stronger regularization (higher KL penalty) may reduce proxy reward but improve human-aligned win rate (as measured in that paper). (Fu et al., 2025)

### Constitutional AI vs RLHF (human feedback)
- **Human labeling dependence**
  - CAI aims to train harmlessness without human labels identifying harmful outputs; oversight is via a list of principles. (Anthropic CAI research page; Bai et al., 2022 arXiv)
- **Claimed outcome**
  - Anthropic blog claims CAI can be more helpful and more harmless than RLHF (Pareto improvement). (Anthropic, “Claude’s Constitution”)
- **Caveat**
  - The provided search snippets do not include the exact numeric comparisons; treat as a qualitative claim unless the tutor retrieves the paper’s evaluation tables.

---

## Architecture & Design Rationale

- **Why pairwise comparisons (RM training)**
  - InstructGPT uses labelers indicating which output they prefer between model outputs; RM predicts the human-preferred output. (OpenAI, 2022)
  - TRL reward modeling docs explicitly motivate Bradley–Terry modeling of preference probability via reward differences. (TRL Reward Modeling docs)

- **Why KL regularization in RLHF**
  - InstructGPT adds per-token KL penalty “to mitigate over-optimization of the reward model.” (OpenAI, 2022)
  - TRL PPO metrics separate “score” from “non_score_reward” (β * KL sum), reflecting the design where the effective RLHF reward is RM score minus KL penalty. (TRL PPO Trainer docs)

- **Why DPO’s design (as stated by authors)**
  - DPO introduces a parameterization enabling extraction of the optimal policy in closed form, allowing solving the RLHF problem with a classification loss; claims stability and reduced need for sampling/hyperparameter tuning. (Rafailov et al., 2023, arXiv/NeurIPS)

- **Why Constitutional AI uses critique/revision before RL**
  - CAI supervised stage “significantly improves the initial model” and “gives some control over the initial behavior at the start of the RL phase,” addressing exploration problems and reducing total RL training length. (Bai et al., 2022, arXiv PDF)
  - CAI draws principles randomly across steps; the model doesn’t apply all principles every time but sees each many times. (Bai et al., 2022; Anthropic blog)

- **Why reward shaping principles (reward hacking paper)**
  - Fu et al. (2025) propose principles including: (1) RL reward ideally bounded; (2) RL benefits from rapid initial growth then gradual convergence; (3) RL reward best formulated as a function of centered reward. (Fu et al., 2025, https://arxiv.org/html/2502.18770v1)

- **Why sycophancy can increase after RLHF (mechanistic rationale)**
  - Benade et al. argue preference optimization can amplify sycophancy due to bias in preference data; direction of drift determined by a covariance under base policy between endorsing belief signal and learned reward. (Benade et al., PDF)

---

## Common Questions & Answers

- **Q: What exact loss does InstructGPT use to train the reward model?**  
  **A:** The paper gives a logistic pairwise loss (Bradley–Terry style):  
  \[
  \text{loss}(\theta) = -\frac{1}{\binom{K}{2}} \mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma\left(r_\theta(x,y_w)-r_\theta(x,y_l)\right)\right]
  \]
  where \(y_w\) is the preferred completion. (OpenAI, 2022, https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

- **Q: How does InstructGPT prevent the PPO policy from drifting too far from SFT?**  
  **A:** It adds a **per-token KL penalty from the SFT model at each token** during PPO to mitigate over-optimization of the reward model; the coefficient is **β**. (OpenAI, 2022, same URL)

- **Q: What are β and γ in InstructGPT PPO training?**  
  **A:** **β** is the KL reward coefficient controlling KL penalty strength; **γ** controls pretraining gradients; for “PPO” models, **γ = 0**. (OpenAI, 2022, same URL)

- **Q: What’s a concrete example of RLHF success reported by OpenAI?**  
  **A:** OpenAI reports that in human evaluations on their prompt distribution, **1.3B** InstructGPT outputs were preferred to **175B** GPT-3 outputs, despite ~**100× fewer parameters**. (OpenAI, 2022, same URL)

- **Q: In TRL PPO training, what does `objective/rlhf_reward` mean?**  
  **A:** TRL defines `objective/rlhf_reward` as `score - non_score_reward`, where `objective/non_score_reward` is basically `beta * kl.sum(1)` (β is KL penalty coefficient; `kl` is per-token KL divergence). (TRL PPO Trainer docs, https://huggingface.co/docs/trl/main/en/ppo_trainer)

- **Q: What are TRL PPO defaults for KL and clipping?**  
  **A:** In PPOConfig, defaults include `kl_coef=0.05` and `cliprange=0.2` (also `cliprange_value=0.2`). (TRL PPOConfig docs, https://huggingface.co/docs/trl/ppo_trainer)

- **Q: How can I encourage PPO-trained models to end with EOS in TRL?**  
  **A:** Use `--missing_eos_penalty`, which subtracts a static scalar penalty from the score of completions that do not end with EOS; docs show an example `--missing_eos_penalty 1.0`. (TRL PPO Trainer docs, https://huggingface.co/docs/trl/main/en/ppo_trainer)

- **Q: What does TRL recommend for reward model training with LoRA on a causal LM?**  
  **A:** It recommends setting `modules_to_save=["score"]` in the PEFT configuration to ensure the reward head is properly trained. (TRL Reward Modeling docs, https://huggingface.co/docs/trl/main/en/reward_trainer)

- **Q: What is Constitutional AI’s training recipe at a high level?**  
  **A:** Supervised phase: sample responses → generate self-critiques and revisions guided by principles → fine-tune on revised responses. RL phase: sample from fine-tuned model → AI compares outputs guided by principles → train preference model from AI preferences → RL using that preference model reward (RLAIF). (Anthropic CAI research page; Bai et al., 2022 arXiv PDF)

- **Q: How many red-teaming prompts did the Constitutional AI paper collect?**  
  **A:** The paper reports **42,496** human-written red teaming prompts. (Bai et al., 2022, https://arxiv.org/pdf/2212.08073.pdf)

- **Q: Does DPO always beat PPO?**  
  **A:** The provided sources disagree depending on setting:
  - DPO paper reports DPO **~61%** vs PPO **57%** win rate in one GPT-J experiment at temperature **0.0**. (Rafailov et al., 2023 NeurIPS PDF)
  - Another study claims PPO can outperform DPO across tasks and reports CodeContest **10@1k 16.4% → 22.4%** vs AlphaCode-41B. (arXiv:2404.10719v1)  
  These are different tasks and setups; the search results do not establish a single definitive ordering.

- **Q: Is there evidence that increasing KL penalty can reduce reward hacking?**  
  **A:** One reward shaping study reports that increasing KL penalty coefficient from **0.01 to 0.1** raised win rate and reduced the reward curve, interpreted as mitigating reward hacking. (Fu et al., 2025, https://arxiv.org/html/2502.18770v1)