## Core Definitions

**Foundation model (robotics)**  
A robot foundation model is a large-capacity model pretrained on broad, heterogeneous robot experience (many tasks, objects, scenes, and often multiple robot embodiments) so that it can *generalize* and be *adapted* (e.g., via finetuning) to new tasks/domains with relatively little additional data. In the RT‑X framing, this is enabled by aggregating many robot datasets into a standardized format (Open X‑Embodiment) and training a single policy across them, aiming for transfer across tasks and embodiments rather than per-robot specialization. (Open X‑Embodiment + RT‑X: https://arxiv.org/abs/2310.08864)

**Pre-training (for robot policies)**  
Pre-training is the initial large-scale training phase on a broad mixture of robot trajectories (often multi-dataset, multi-embodiment) to learn reusable representations and action-generation behavior before any task- or robot-specific adaptation. Octo, for example, is pretrained on ~800k robot trajectories from a 25-dataset subset of Open X‑Embodiment, then finetuned on ~100 trajectories for a target task/robot. (Octo paper: https://octo-models.github.io/paper.pdf)

**Generalization (robot foundation models)**  
Generalization is the ability of a pretrained policy to succeed outside its training distribution—e.g., new objects, new scenes, new tasks, or even new robots—either *zero-shot* (no additional training) or with small-data finetuning. RT‑X reports “emergent skills” improvements when co-finetuning a large VLA model with robot data (RT‑2‑X), and Octo reports higher average zero-shot success than RT‑1‑X across tested robots. (RT‑X: https://arxiv.org/abs/2310.08864; Octo: https://octo-models.github.io/paper.pdf)

**Cross-embodiment transfer**  
Cross-embodiment transfer is when a policy trained on data from multiple robot bodies (different kinematics, sensors, controllers) can transfer knowledge to a new embodiment. Open X‑Embodiment explicitly aggregates trajectories across embodiments, but notes key non-alignments: camera poses and coordinate frames vary, and the same canonical 7D end-effector action vector can produce different motions across robots due to differing control conventions and frames. (RT‑X / OXE: https://arxiv.org/abs/2310.08864)

**Open X‑Embodiment (OXE)**  
Open X‑Embodiment is a dataset and standardization effort that aggregates 60 existing robot datasets into 1M+ real robot trajectories across multiple embodiments, converted into RLDS format (serialized TFRecord) to support heterogeneous modalities and efficient loading. (RT‑X / OXE: https://arxiv.org/abs/2310.08864)

**RT‑X (RT‑1‑X / RT‑2‑X)**  
RT‑X is a family of multi-robot policies trained on Open X‑Embodiment-style mixtures using either (a) RT‑1-style discrete action token prediction (RT‑1‑X) or (b) a vision-language-action model that casts actions as text tokens and is co-finetuned with web VLM data (RT‑2‑X). (RT‑X: https://arxiv.org/abs/2310.08864)

**Octo**  
Octo is a “Transformer-first” diffusion generalist robot policy pretrained on large-scale multi-robot trajectories (Open X‑Embodiment subset). It tokenizes language and images into a unified transformer sequence, uses masked attention and readout tokens for modular I/O, and decodes continuous actions via a diffusion head with a DDPM objective. (Octo: https://octo-models.github.io/paper.pdf)

**NVIDIA GR00T**  
Not defined in the provided sources; do not quote specifics beyond the lesson summary’s high-level statement that it is a robot foundation model.

---

## Key Formulas & Empirical Results

### Octo: scale, architecture numbers, and training/finetuning defaults
- **Pretraining scale:** pretrained on **~800k robot trajectories** from **25 datasets** (Open X‑Embodiment subset). Released checkpoints include **Octo-Small (27M params)** and **Octo-Base (~86–93M params)**. (https://octo-models.github.io/paper.pdf)
- **Tokenization counts (one common configuration):**
  - Language: **T5-base (111M)** encoder → **16 language embedding tokens**.
  - Images: shallow CNN → patches → tokens; e.g. **256 tokens** for **256×256** 3rd-person (16×16 patches), **64 tokens** for **128×128** wrist. (https://octo-models.github.io/paper.pdf)
- **Diffusion decoding update (Eq. 1):** sample \(x_K\sim\mathcal N(0,I)\), then iteratively denoise with
  \[
  x_{k-1}=\alpha\big(x_k-\gamma\,\epsilon_\theta(x_k,e,k)+\mathcal N(0,\sigma^2 I)\big)
  \]
  where \(\epsilon_\theta\) predicts noise conditioned on transformer embedding \(e\) and diffusion step \(k\). Uses **DDPM objective** and **cosine noise schedule**; **20 diffusion steps** train/infer; **one transformer forward pass** per action (denoising in a small head). (https://octo-models.github.io/paper.pdf)
- **Pretraining hyperparameters (App. D / Sec. 3):** AdamW, **LR 3e-4**, **warmup 2000**, **inverse-sqrt LR decay**, **weight decay 0.1**, **grad clip 1.0**, **batch 2048**. ViT-B-sized model trained **300k steps** on **TPU v4-128** in **~14 hours**. (https://octo-models.github.io/paper.pdf)
- **Finetuning recipe:** about **100 trajectories**, **50k steps**, cosine LR decay + linear warmup; **update full model** (better than head-only). Reported **~5 hours** on **single NVIDIA A5000 24GB**. (https://octo-models.github.io/paper.pdf)

### Octo: reported performance numbers (useful for “does it work?” questions)
- **Zero-shot:** Octo averages **33% higher success** than **RT‑1‑X (35M)** across tested robots; on WidowX, **goal-image conditioning** gave **+25%** success vs language. (https://octo-models.github.io/paper.pdf)
- **Finetuning success (Table 1):** scratch ResNet+Transformer **avg 20%**; VC‑1 **avg 9%**; **Octo avg 64%** across listed tasks (e.g., Stanford Coffee **75%**, Berkeley Peg Insert **70%** with new force-torque obs, Berkeley Pick-up **60%** with new joint-position action space). (https://octo-models.github.io/paper.pdf)

### RT‑X / OXE: standardization + action tokenization
- **OXE scale:** **60 datasets**, **1M+ real robot trajectories**, multiple embodiments; standardized into **RLDS** (TFRecord). (https://arxiv.org/abs/2310.08864)
- **Canonical action representation:** **7D end-effector action** \((x,y,z,\text{roll},\text{pitch},\text{yaw},\text{gripper})\) (or rates). Actions are **normalized per-dataset** before discretization; at inference, outputs are **de-normalized per embodiment**. (https://arxiv.org/abs/2310.08864)
- **Action tokenization (RT‑1‑style):** discretize into **256 bins** along **8 dimensions** = **7 action dims + 1 terminate-episode dim**. (https://arxiv.org/abs/2310.08864)
- **RT‑1 architecture size:** **35M params**; EfficientNet vision encoder; language via USE embedding; FiLM fusion producing **81 vision-language tokens**; decoder-only transformer outputs discrete action tokens. (https://arxiv.org/abs/2310.08864)
- **RT‑2 action-as-text example:** action tokens rendered as text like `"1 128 91 241 5 101 127"`. (https://arxiv.org/abs/2310.08864)

### RT‑X: empirical transfer signal
- **Emergent skills (Google Robot; skills from Bridge/WidowX):** **RT‑2‑X 75.8% vs RT‑2 62%** success (Table II). Removing Bridge data significantly reduces emergent-skill performance. (https://arxiv.org/abs/2310.08864)

---

## How It Works

### A. “Multi-robot foundation policy” pipeline (RT‑X / OXE style)
1. **Aggregate datasets across robots** into a common container format (OXE uses **RLDS/TFRecord**) with consistent field names and modality handling. (https://arxiv.org/abs/2310.08864)
2. **Choose a canonical observation interface** (often: one resized RGB view per dataset + short image history + language instruction). (https://arxiv.org/abs/2310.08864)
3. **Choose a canonical action interface** (RT‑X uses **7D end-effector + gripper**, plus terminate). Note: this is *not* a true physical alignment—frames and controllers differ across robots. (https://arxiv.org/abs/2310.08864)
4. **Normalize actions per dataset**, then discretize (RT‑1‑X) or map to text tokens (RT‑2‑X). (https://arxiv.org/abs/2310.08864)
5. **Mixture training across datasets**:
   - RT‑1‑X: train on robotics mixture only.
   - RT‑2‑X: **co-finetune** with ~**1:1** split between original VLM data and robotics mixture. (https://arxiv.org/abs/2310.08864)
6. **Inference**: output tokens at **~3–10 Hz**; de-normalize actions per embodiment before execution. (https://arxiv.org/abs/2310.08864)

### B. Octo’s “Transformer-first diffusion policy” pipeline (mechanical view)
1. **Inputs → tokens** (Sec. 2.1):
   - Language instruction → tokenize → **T5-base** encoder → **16 tokens**.
   - One or more images (obs, optional goal image) → shallow CNN → patch tokens (e.g., 256 or 64 tokens depending on resolution/camera).
   - Assemble a single sequence with **learnable positional embeddings**; supports multi-camera, history, and either language or goal image. (https://octo-models.github.io/paper.pdf)
2. **Backbone transformer with modular masking**:
   - Uses **block-wise masked attention** so observation tokens attend causally to same/earlier timesteps + task tokens.
   - Missing modalities are **fully masked** (enables training/inference with variable sensors).
   - **Readout tokens** attend to prior tokens but are not attended to (lets you add/remove I/O modules cleanly). (https://octo-models.github.io/paper.pdf)
3. **Action decoding via diffusion head**:
   - Run **one transformer forward pass** to get conditioning embedding \(e\).
   - Run **20-step diffusion** in a small head to sample a continuous action, using Eq. 1 update and DDPM objective. (https://octo-models.github.io/paper.pdf)
4. **Pretraining data conditioning tricks** (practical knobs):
   - Drop datasets without images or without delta end-effector control.
   - Zero-pad missing cameras.
   - Align gripper convention to **+1=open, 0=closed**.
   - Use **hindsight goal relabeling** (random future observation as goal).
   - Randomly drop language or goal per example; if no language, use goal images. (https://octo-models.github.io/paper.pdf)
5. **Finetuning**:
   - Collect ~**100 trajectories** for the target task/robot.
   - Finetune **full model** for **~50k steps** (reported better than head-only). (https://octo-models.github.io/paper.pdf)

---

## Teaching Approaches

### Intuitive (no math)
- **“One brain, many bodies.”** Pretraining mixes experience from many robots and tasks so the model learns reusable visual-language-to-action patterns (e.g., what “pick up the mug” looks like), then you adapt it to a specific robot with a small amount of data.
- Emphasize that **standardization is approximate**: we can store actions in a common 7D format, but different robots interpret that differently due to frames/controllers.

### Technical (with math)
- Use Octo’s diffusion equation as the concrete “how actions are produced” anchor: transformer produces conditioning \(e\), then diffusion iteratively denoises \(x_K\to x_0\) using Eq. 1. (https://octo-models.github.io/paper.pdf)
- Use RT‑X’s discretization as the concrete “how actions become tokens” anchor: 7 action dims + terminate dim, each discretized into 256 bins; trained with categorical cross-entropy over tokens. (https://arxiv.org/abs/2310.08864)

### Analogy-based
- **Robotics mixture pretraining ≈ multilingual pretraining.** Different robots are like different “languages/dialects” for acting: same intent, different execution details. The model learns shared structure, but you still need per-embodiment calibration (de-normalization, controller conventions). (RT‑X notes non-aligned frames and differing effects of the same 7D action.) (https://arxiv.org/abs/2310.08864)

---

## Common Misconceptions

1. **“If actions are standardized to a 7D vector, then the policy is automatically cross-robot compatible.”**  
   - **Why wrong:** RT‑X explicitly notes camera poses/properties vary, **coordinate frames are not aligned**, and actions may be absolute vs relative positions/velocities—so the *same* 7D vector can cause different motions across robots. (https://arxiv.org/abs/2310.08864)  
   - **Correct model:** Standardization is a *training interface*, not a guarantee of physical equivalence. Cross-embodiment transfer relies on learning invariances and robust mappings despite imperfect alignment.

2. **“Octo is just a transformer that outputs actions directly.”**  
   - **Why wrong:** Octo uses a transformer to produce a conditioning embedding, then a **diffusion head** samples continuous actions via **20 denoising steps** (DDPM objective), with only **one transformer forward pass** per action. (https://octo-models.github.io/paper.pdf)  
   - **Correct model:** Transformer = multimodal encoder/backbone; diffusion = stochastic continuous action generator.

3. **“More datasets always improves performance; mixture training can’t hurt.”**  
   - **Why wrong:** RT‑X reports RT‑1‑X can **underfit** large-scale domains and not beat embodiment-specific RT‑1; higher capacity (RT‑2‑X) is needed for better transfer. (https://arxiv.org/abs/2310.08864)  
   - **Correct model:** Mixture training increases diversity *and* difficulty; capacity, optimization, and representation choices determine whether transfer is positive.

4. **“Language is always the best conditioning signal for robot policies.”**  
   - **Why wrong:** Octo reports on WidowX that **goal-image conditioning** improved success by **+25%** compared to language. (https://octo-models.github.io/paper.pdf)  
   - **Correct model:** Conditioning choice depends on task ambiguity and dataset quality; goal images can be a stronger, less ambiguous target specification.

5. **“Finetuning only the head is the safe/standard approach.”**  
   - **Why wrong:** Octo reports **updating the full model** during finetuning works better than head-only finetuning (and gives a concrete recipe: ~100 trajectories, 50k steps). (https://octo-models.github.io/paper.pdf)  
   - **Correct model:** For these policies, the backbone representations often need to adapt to new sensors/action spaces; full-model finetuning can be necessary.

---

## Worked Examples

### Example 1: Compute RT‑1‑X action token IDs from continuous 7D action (conceptual, matches RT‑X discretization)
**Goal:** show the tutor a concrete way to walk from “continuous action” → “256-bin tokens per dimension” as described in RT‑X. (https://arxiv.org/abs/2310.08864)

```python
import numpy as np

def discretize_action_8d(action7, terminate, mins, maxs, n_bins=256):
    """
    action7: shape (7,) continuous (x,y,z,roll,pitch,yaw,gripper)
    terminate: scalar in [0,1] or {0,1}
    mins/maxs: per-dataset normalization bounds for the 7 dims (RT-X normalizes per-dataset)
    returns: 8 integer tokens in [0, 255]
    """
    action7 = np.asarray(action7, dtype=np.float32)
    mins = np.asarray(mins, dtype=np.float32)
    maxs = np.asarray(maxs, dtype=np.float32)

    # 1) normalize per-dataset (RT-X: normalize before discretization)
    norm = (action7 - mins) / (maxs - mins + 1e-8)
    norm = np.clip(norm, 0.0, 1.0)

    # 2) discretize each dim into 256 bins
    tokens7 = np.floor(norm * (n_bins - 1) + 1e-6).astype(np.int32)

    # 3) terminate dim as its own tokenized dimension (RT-X: 7 dims + terminate dim)
    term = int(np.clip(terminate, 0, 1) * (n_bins - 1))

    return np.concatenate([tokens7, np.array([term], dtype=np.int32)])

# Demo numbers (mins/maxs are dataset-specific; RT-X de-normalizes per embodiment at inference)
action7 = [0.02, -0.01, 0.10, 0.0, 0.1, -0.1, 1.0]  # example
mins    = [-0.05, -0.05, 0.00, -0.5, -0.5, -0.5, 0.0]
maxs    = [ 0.05,  0.05, 0.20,  0.5,  0.5,  0.5, 1.0]
print(discretize_action_8d(action7, terminate=0, mins=mins, maxs=maxs))
```

**Tutor prompts while using this:**
- “Where do `mins/maxs` come from?” → RT‑X: **normalized per-dataset before discretization**; then **de-normalized per embodiment** at inference. (https://arxiv.org/abs/2310.08864)
- “Why does this not guarantee cross-robot equivalence?” → RT‑X: frames/controllers differ; same 7D vector can move robots differently. (https://arxiv.org/abs/2310.08864)

### Example 2: Octo forward pass vs diffusion sampling (whiteboard pseudocode)
Use this when a student asks “why is it still fast if it uses diffusion?”

```text
# Octo inference (conceptual)
tokens = tokenize(language, images, goals, history)
e = Transformer(tokens)              # ONE transformer forward pass
x = Normal(0, I)                     # x_K
for k in K..1:                       # K = 20 steps (train/infer)
    eps = diffusion_head(x, e, k)    # small head, not full transformer
    x = alpha * (x - gamma*eps + Normal(0, sigma^2 I))
action = x_0
```

Key facts to quote:
- **20 diffusion steps** train/infer.
- **Only one transformer forward pass per action**; denoising is in a small head. (https://octo-models.github.io/paper.pdf)

---

## Comparisons & Trade-offs

| Model / Approach | Action representation | Core architecture | Strengths (per sources) | Common failure mode / cost | When to choose |
|---|---|---|---|---|---|
| **RT‑1‑X** (RT‑X) | Discrete tokens: **256 bins × 8 dims** (7 action + terminate) | EfficientNet + FiLM + decoder-only transformer (**35M**) | Works across mixture; beats “Original Method” on 4/5 small-scale datasets (per RT‑X) | Can **underfit** large-scale domains; may not beat embodiment-specific training | When you want a relatively small, tokenized policy trained on robot mixture data (https://arxiv.org/abs/2310.08864) |
| **RT‑2‑X** (RT‑X) | Actions as **text tokens** | Large VLA (e.g., RT‑2‑PaLI‑X) co-finetuned with web+robot data | Better transfer/emergent skills: **75.8% vs 62%** (RT‑2‑X vs RT‑2) | Higher capacity/infra; cloud inference noted for RT‑2 | When you can afford large VLA capacity and want web pretraining benefits (https://arxiv.org/abs/2310.08864) |
| **Octo** | Continuous actions via **diffusion** | Transformer-first + diffusion head | Strong zero-shot and finetuning: **+33%** vs RT‑1‑X zero-shot; finetune avg **64%** | Diffusion sampling adds iterative steps (though head-only) | When you want modular multimodal inputs and continuous action generation with strong finetuning recipe (https://octo-models.github.io/paper.pdf) |

---

## Prerequisite Connections

- **Transformers / attention basics:** Octo and RT‑X policies use transformer backbones or decoder-only transformers; students need to know tokens, attention, and causal masking at a high level. (Octo: https://octo-models.github.io/paper.pdf; RT‑X: https://arxiv.org/abs/2310.08864)
- **Behavior cloning / supervised sequence prediction:** RT‑1‑X trains with categorical cross-entropy over discretized action tokens; Octo trains a diffusion objective conditioned on transformer embeddings. (RT‑X: https://arxiv.org/abs/2310.08864; Octo: https://octo-models.github.io/paper.pdf)
- **Dataset standardization & distribution shift:** OXE mixes heterogeneous robots and sensors; students must understand why “same field name” ≠ “same semantics.” (https://arxiv.org/abs/2310.08864)

---

## Socratic Question Bank

1. **If two robots both use a 7D end-effector action vector, what are two reasons the *same* vector might produce different physical motions?**  
   *Good answer:* coordinate frames not aligned; actions may be absolute vs relative/velocity; controller differences; camera pose differences (RT‑X notes these non-alignments). (https://arxiv.org/abs/2310.08864)

2. **What’s the practical difference between “tokenizing actions” (RT‑1‑X) and “diffusion decoding” (Octo) in terms of what the model outputs and how it’s trained?**  
   *Good answer:* RT‑1‑X predicts discrete bins with cross-entropy; Octo samples continuous actions via iterative denoising with DDPM objective. (https://arxiv.org/abs/2310.08864, https://octo-models.github.io/paper.pdf)

3. **Why might mixture training across many datasets require *more* model capacity to see gains?**  
   *Good answer:* RT‑X reports RT‑1‑X underfitting in large-scale domains; RT‑2‑X (higher capacity + web pretraining) improves. (https://arxiv.org/abs/2310.08864)

4. **Octo uses “readout tokens” that attend to prior tokens but are not attended to—what modularity problem does that solve?**  
   *Good answer:* lets you add/remove I/O modules without other tokens depending on them; supports missing modalities via masking. (https://octo-models.github.io/paper.pdf)

5. **If you had no reliable language labels for a dataset, what conditioning alternative does Octo explicitly support, and what result suggests it can help?**  
   *Good answer:* goal-image conditioning; WidowX +25% success vs language. (https://octo-models.github.io/paper.pdf)

6. **What does “one transformer forward pass per action” mean in Octo, given it uses 20 diffusion steps?**  
   *Good answer:* transformer produces conditioning embedding once; diffusion steps run in a small head. (https://octo-models.github.io/paper.pdf)

7. **What is the terminate dimension in RT‑X tokenization, and why might it be included?**  
   *Good answer:* an extra 8th discretized dimension indicating episode termination; allows policy to signal completion. (https://arxiv.org/abs/2310.08864)

8. **When finetuning Octo to a new task, what evidence suggests you should update the full model rather than only the head?**  
   *Good answer:* Octo reports full-model finetuning works better; provides recipe (~100 trajectories, 50k steps). (https://octo-models.github.io/paper.pdf)

---

## Likely Student Questions

**Q: How big is Octo and what data scale does it use?** → **A:** Octo is pretrained on **~800k robot trajectories** from **25 datasets** (Open X‑Embodiment subset). Released checkpoints include **Octo-Small (27M params)** and **Octo-Base (~86–93M params)**. (https://octo-models.github.io/paper.pdf)

**Q: What exactly is the RT‑X “canonical action space”?** → **A:** RT‑X uses a **7D end-effector action** \((x,y,z,\text{roll},\text{pitch},\text{yaw},\text{gripper})\) (or rates), normalized per-dataset and later de-normalized per embodiment; plus an additional terminate dimension when tokenized. (https://arxiv.org/abs/2310.08864)

**Q: How does RT‑1‑X tokenize actions?** → **A:** It discretizes actions into **256 bins** along **8 dimensions**: **7 action dims + 1 terminate-episode dim**. (https://arxiv.org/abs/2310.08864)

**Q: Why doesn’t a standardized 7D action vector guarantee cross-robot transfer?** → **A:** RT‑X notes camera poses/properties vary, **coordinate frames are not aligned**, and actions can be absolute/relative/velocity; thus the same 7D vector can cause different motions across robots. (https://arxiv.org/abs/2310.08864)

**Q: What’s Octo’s action generation equation and what do the symbols mean?** → **A:** Octo samples \(x_K\sim\mathcal N(0,I)\) and iteratively denoises via  
\(x_{k-1}=\alpha(x_k-\gamma\epsilon_\theta(x_k,e,k)+\mathcal N(0,\sigma^2 I))\),  
where \(\epsilon_\theta\) predicts noise conditioned on transformer embedding \(e\) and diffusion step \(k\). It uses **DDPM** with a **cosine noise schedule** and **20 diffusion steps**. (https://octo-models.github.io/paper.pdf)

**Q: What are Octo’s concrete pretraining hyperparameters?** → **A:** AdamW, **LR 3e-4**, **warmup 2000**, **inverse-sqrt LR decay**, **weight decay 0.1**, **grad clip 1.0**, **batch 2048**; trained **300k steps** on **TPU v4-128** in **~14 hours** (ViT-B-sized). (https://octo-models.github.io/paper.pdf)

**Q: How much data/time does Octo finetuning take?** → **A:** Reported finetuning uses **~100 trajectories** for **~50k steps**, updating the full model; **~5 hours** on a **single NVIDIA A5000 24GB**. (https://octo-models.github.io/paper.pdf)

**Q: Is there evidence that web pretraining helps robot generalization in RT‑X?** → **A:** RT‑2‑X co-finetunes with ~**1:1** web VLM data and robot mixture; it reports **75.8% vs 62%** success (RT‑2‑X vs RT‑2) on emergent skills, and removing Bridge data significantly reduces performance. (https://arxiv.org/abs/2310.08864)

---

## Available Resources

### Videos
- [Let’s build GPT: from scratch, in code, spelled out.](https://youtube.com/watch?v=kCc8FmEb1nY) — **Surface when:** the student is missing transformer fundamentals (tokens, causal attention) needed to understand RT‑X/Octo architectures.

### Articles & Tutorials
- [Lilian Weng — Domain Randomization for Sim-to-Real Transfer](https://lilianweng.github.io/posts/2019-05-05-domain-randomization/) — **Surface when:** the student conflates robot foundation models with sim-to-real; use to clarify domain randomization vs multi-robot pretraining.
- [Lilian Weng — Meta-Learning: Learning to Learn Fast](https://lilianweng.github.io/posts/2018-11-30-meta-learning/) — **Surface when:** the student asks whether “foundation models” are the same as meta-learning/few-shot learning; use to contrast adaptation mechanisms.
- [Tobin et al. (2017) — Domain Randomization](https://arxiv.org/abs/1703.06907) — **Surface when:** the student asks for the classic “randomize sim until real looks like a variation” statement and early sim-only-to-real results.
- [OpenAI — Learning Dexterity](https://openai.com/index/learning-dexterity/) — **Surface when:** the student wants a canonical large-scale sim-to-real case study (domain randomization/system ID), distinct from RT‑X/Octo-style multi-robot pretraining.
- [Yannic Kilcher — Domain Adaptation / Transfer Learning overview (arXiv link)](https://arxiv.org/abs/2010.03978) — **Surface when:** the student asks for a broader transfer/domain adaptation framing to situate cross-embodiment transfer.

---

## Visual Aids

(Available images are meta-learning diagrams; use only when the conversation detours into “few-shot adaptation” as a conceptual cousin of finetuning.)

![4-shot 2-class image classification: support set and query example.](/api/wiki-images/domain-adaptation/images/lilianweng-posts-2018-11-30-meta-learning_001.png)  
**Show when:** the student asks “is finetuning on ~100 trajectories basically few-shot learning?” Use to separate *task-as-sample* meta-learning framing from standard pretrain→finetune.

---

## Key Sources

- [Octo — Transformer-first Diffusion Generalist Robot Policy](https://octo-models.github.io/paper.pdf) — Most concrete architecture/training pipeline details (tokenization, masked attention/readouts, diffusion decoding) plus finetuning recipe and success numbers.
- [Open X‑Embodiment + RT‑X (RT‑1‑X / RT‑2‑X)](https://arxiv.org/abs/2310.08864) — Authoritative on multi-dataset standardization (RLDS), canonical action tokenization, and empirical evidence for/limits of cross-embodiment transfer.