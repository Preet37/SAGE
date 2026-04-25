## Core Definitions

**Multi-modal fine-tuning (vision-language models / VLMs).** Fine-tuning a multi-modal model means adapting a model that consumes *both* images and text (e.g., image + question → answer) to a specialized domain by updating some subset of parameters using domain-specific image–text supervision (e.g., VQA, captioning, instruction-following). In common VLM stacks, the model is composed of a **vision encoder**, a **projector** that maps vision features into the LLM embedding space, and a **language model** that generates text conditioned on both modalities (MobileVLM, Sec. 3–4) https://arxiv.org/pdf/2312.16886.pdf.

**LoRA for VLMs (Low-Rank Adaptation).** LoRA is a parameter-efficient fine-tuning method that keeps pretrained weights frozen and learns a low-rank update to selected linear layers. For a linear projection \(Y=XW\), LoRA adds a low-rank term \(sXL_1L_2\) (Dettmers et al., QLoRA paper Eq. 3) https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf. In PEFT taxonomy terms, LoRA is **reparametrization-based**: it learns \(\Delta W = BA\) (rank \(r\)) and uses \(W' = W + \alpha/r \cdot BA\) while training only \(A,B\) (PEFT taxonomy, Sec. 9.2) https://arxiv.org/html/2303.15647v2.

**QLoRA.** QLoRA is LoRA fine-tuning where the *base model weights are stored in 4-bit quantized form* (NF4) and kept frozen, while gradients update only the LoRA parameters; computation is performed in higher precision (e.g., BF16). QLoRA’s core innovations are **NF4**, **double quantization** (quantizing quantization constants), and **paged optimizers** to manage memory spikes (Dettmers et al., Sec. 3) https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf.

**Domain adaptation (in the context of VLM fine-tuning).** Domain adaptation is transferring a model trained on one distribution (source) to perform well on a different but related distribution (target). Classic theory decomposes target error into (i) source error, (ii) a domain discrepancy term (e.g., \(\mathcal H\)-divergence / A-distance), and (iii) a labeling-function disagreement term \(\lambda\) (Ben-David et al., Thm. 1) https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf. A key caution: forcing domain-invariant representations can fail when label marginals/conditionals differ (Zhao et al., counterexample + lower bounds) http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf.

**VQA evaluation (as a practical evaluation target for VLM adaptation).** VQA evaluation measures whether a VLM can answer questions about images; in practice, VLM papers often report multiple benchmarks (e.g., VQA, GQA, SQA) and use these as proxies for multi-modal capability and domain transfer. MobileVLM reports benchmark scores (e.g., GQA/SQA/VQA) and shows token-reduction strategies can preserve quality (MobileVLM, Table 11) https://arxiv.org/pdf/2312.16886.pdf.

**Multi-modal deployment (adapter-based).** Adapter-based deployment serves a shared frozen base model while swapping/activating lightweight adapters (e.g., LoRA) per tenant/task. Systems like **S-LoRA** avoid merging adapters into base weights and instead compute \(xW\) (shared) plus \(xBA\) (per-adapter) on-the-fly, enabling batching across many adapters and managing KV cache + adapter memory via unified paging (S-LoRA, Sec. 4–6) https://arxiv.org/pdf/2311.03285.pdf.

---

## Key Formulas & Empirical Results

### LoRA / QLoRA math (quotable)

- **LoRA forward (Dettmers et al., Eq. 3):**
  \[
  Y = XW + s X L_1 L_2
  \]
  - \(X\in\mathbb{R}^{b\times h}\): activations (batch \(b\), hidden \(h\))
  - \(W\in\mathbb{R}^{h\times o}\): frozen pretrained weight
  - \(L_1\in\mathbb{R}^{h\times r}, L_2\in\mathbb{R}^{r\times o}\): trainable low-rank factors (rank \(r\))
  - \(s\): scalar (often related to \(\alpha/r\))
  **Claim supported:** you can adapt behavior by training only low-rank matrices while keeping \(W\) fixed.  
  Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

- **PEFT LoRA update form (taxonomy, Sec. 9.2):**
  \[
  \Delta W = BA,\quad W' = W + \alpha/r \cdot BA
  \]
  **Claim supported:** LoRA is a reparameterization of a dense update via low-rank factors; can be merged after training.  
  Source: https://arxiv.org/html/2303.15647v2

- **QLoRA forward (Dettmers et al., Eq. 5–6, frozen 4-bit base + BF16 compute):**
  \[
  Y_{\text{BF16}} = X_{\text{BF16}}\;\text{doubleDequant}(\cdot, W_{k\text{-bit}}) + X_{\text{BF16}}L^{(1)}_{\text{BF16}}L^{(2)}_{\text{BF16}}
  \]
  **Claim supported:** gradients flow only into LoRA params; base weights remain quantized/frozen.  
  Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

### QLoRA quantization specifics (numbers students ask for)

- **NF4 rationale:** weights are approximately normal; NF4 uses normal quantiles and includes exact zero (Dettmers et al., Sec. 3).  
  Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

- **Double quantization defaults (Dettmers et al., Sec. 3):**
  - First-level blocksize for \(W\): **64**
  - Quantize quantization constants using **FP8**, blocksize **256**
  - Memory for constants drops from **0.5 bits/param** to **0.127 bits/param**, saving **0.373 bits/param (~3GB for 65B)**  
  Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

- **Paged optimizers:** use NVIDIA Unified Memory paging to avoid OOM spikes during checkpointing; reported same speed as regular optimizers for **65B, batch size 16** (Dettmers et al., Sec. 3).  
  Source: same as above.

### Empirical comparisons (quality vs memory)

- **Quantization quality (Dettmers et al.):**
  - Pile Common Crawl perplexity: **NF4+DQ 27.41** vs Int4 **34.34** (better is lower)  
  - MMLU 5-shot mean: **NF4+DQ 53.1** vs BF16 **53.0** (matches)  
  Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

- **Chatbot benchmark + memory (Dettmers et al., Table 4):**
  - Guanaco **65B 4-bit 41GB: 99.3% ±4.4** (vs ChatGPT reference in that benchmark framing)  
  Source: same as above.

### VLM-specific insertion points + numbers (MobileVLM)

- **VLM stack definition:** vision encoder + LLM + projector mapping \(Z\in\mathbb{R}^{N\times D_v}\to V\in\mathbb{R}^{M\times D_t}\) (MobileVLM Eq. 1).  
  Source: https://arxiv.org/pdf/2312.16886.pdf

- **Token reduction result:** LDP reduces visual tokens **576 → 144 (−75%)** with comparable or better benchmark performance (MobileVLM Sec. 5.1).  
  Source: https://arxiv.org/pdf/2312.16886.pdf

- **LoRA config + trainable fraction (MobileVLM Sec. 4.4):**
  - LoRA: **r=128**, **α=256**
  - Trainable params during LoRA instruction tuning: **8.87% (1.4B)** and **7.41% (2.7B)** of full LLM (as reported for their settings)  
  Source: https://arxiv.org/pdf/2312.16886.pdf

### Domain adaptation bound (useful to correct “invariance guarantees transfer”)

- **Target risk bound (Ben-David et al., Thm. 1):**
  \[
  \epsilon_T(h)\le \hat\epsilon_S(h)+\text{(gen term)}+d_{\mathcal H}(\tilde D_S,\tilde D_T)+\lambda
  \]
  where \(\lambda=\inf_{h\in\mathcal H}(\epsilon_S(h)+\epsilon_T(h))\) captures labeling-function disagreement.  
  Source: https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf

- **Failure mode for invariant representations (Zhao et al.):** there exist cases where a representation makes source/target features perfectly invariant but forces **joint error = 1** (Sec. 4.1 counterexample).  
  Source: http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf

---

## How It Works

### A. Fine-tuning a VLM with LoRA (mechanical sequence)

1. **Identify the VLM components** (MobileVLM):
   - Vision encoder (often frozen)
   - Projector (aligns/compresses vision tokens into LLM embedding space; Eq. 1)
   - LLM (decoder-only LM generating text conditioned on image tokens + text tokens; Eq. 2)  
   Source: https://arxiv.org/pdf/2312.16886.pdf

2. **Choose what to train**
   - Common pipeline: train projector first with vision+LLM frozen, then instruction-tune projector + LLM (MobileVLM Sec. 4.1).
   - LoRA option: freeze LLM weights and train only LoRA modules inserted into LLM linear layers (MobileVLM Sec. 4.4).

3. **Insert LoRA modules into target linear layers**
   - For each chosen linear layer \(W\), replace forward with \(XW + sXL_1L_2\) (Dettmers Eq. 3).
   - Decide target modules (often attention projections; PEFT taxonomy notes best performance when applied broadly, citing Dettmers et al. 2023) https://arxiv.org/html/2303.15647v2.

4. **Train on domain data**
   - Use domain-specific image–text pairs (e.g., medical images + reports/questions).
   - Optimize standard LM loss (not specified in provided sources; keep tutor language: “autoregressive next-token loss per MobileVLM Eq. 2 framing”).

5. **Export**
   - Save LoRA weights separately (adapter checkpoint).
   - Optionally merge \(\Delta W\) into \(W\) for single-adapter deployment (PEFT taxonomy), but avoid merging if you need multi-tenant serving (S-LoRA rationale).

### B. QLoRA for multi-modal models (what changes vs LoRA)

1. **Quantize base model weights to 4-bit**
   - Use NF4 (normally-distributed weights) and optionally double quantization (Dettmers Sec. 3).
2. **Keep base weights frozen**
   - Only LoRA parameters receive gradients (Dettmers Eq. 5–6).
3. **Compute in BF16**
   - Dequantize blocks on-the-fly into BF16 for matmuls; add LoRA term in BF16.
4. **Use paged optimizers if needed**
   - To avoid memory spikes (Dettmers Sec. 3).

### C. Serving many LoRA adapters (deployment mechanics: S-LoRA)

1. **Do not merge adapters into base weights** when serving many tenants; merging implies duplication or swapping that breaks batching (S-LoRA Sec. 4; LMSYS blog).
2. **Compute base-model matmuls once per batch** and add per-request LoRA contributions \(xBA\) (S-LoRA Eq. 1–2).
3. **Unified paging memory pool**
   - One paged pool manages **KV cache + adapter weights** to reduce fragmentation; page size is hidden size \(h\) (S-LoRA Sec. 5.1; LMSYS blog).
4. **Custom kernels**
   - Prefill uses matrix–matrix; decode uses matrix–vector kernels that can gather non-contiguous adapter pages and handle heterogeneous ranks (S-LoRA Sec. 5.3).

---

## Teaching Approaches

### Intuitive (no math)
- **LoRA:** “Instead of rewriting the whole model, we attach small ‘correction knobs’ to some layers. Training only turns those knobs.”
- **QLoRA:** “Same knobs, but the big frozen model is stored in a compressed 4-bit form so it fits on a smaller GPU; we still compute in higher precision when needed.”
- **VLM-specific:** “You can adapt either the *bridge* (projector) that turns images into language tokens, or the *language brain* (LLM) via LoRA—or both.”

### Technical (with math)
- Quote Dettmers Eq. 3: \(Y=XW+sXL_1L_2\). Emphasize \(W\) frozen, \(L_1,L_2\) trained.
- For QLoRA, emphasize: base \(W\) stored in 4-bit NF4; forward uses dequant-to-BF16 + LoRA BF16 term (Dettmers Eq. 5–6).
- For domain adaptation caution, use Ben-David bound: target error includes discrepancy \(d_{\mathcal H}\) and \(\lambda\); invariance alone doesn’t remove \(\lambda\).

### Analogy-based
- **LoRA as “patch notes”:** base model is the game; LoRA is a small patch file that changes behavior without reinstalling the whole game.
- **QLoRA as “zipped base + patch”:** base game is zipped (4-bit) on disk/GPU; patch is small and editable; runtime unzips only what’s needed for computation.
- **Projector vs LLM tuning:** projector is the “translator” from vision to language; LLM is the “writer.” You can retrain the translator, the writer, or both.

---

## Common Misconceptions

1. **“QLoRA trains the 4-bit weights directly.”**  
   - **Why wrong:** In QLoRA, the base weights are **frozen**; only LoRA parameters get gradients (Dettmers Eq. 5–6).  
   - **Correct model:** QLoRA *backpropagates through* quantized weights to update *adapters*, not the quantized weights themselves.

2. **“LoRA is only for Q and V matrices; that’s the standard/best practice.”**  
   - **Why wrong:** The PEFT taxonomy notes LoRA is often applied to attention projections, but also states best performance when applied to **all weight matrices** (citing Dettmers et al. 2023) https://arxiv.org/html/2303.15647v2.  
   - **Correct model:** Target modules are a design choice; restricting to Q/V is a compute-saving heuristic, not a guarantee of best quality.

3. **“If I make features domain-invariant, target performance is guaranteed.”**  
   - **Why wrong:** Zhao et al. give counterexamples where perfect invariance forces high joint error (Sec. 4.1), and Ben-David’s bound includes \(\lambda\) (labeling disagreement) which invariance does not remove.  
   - **Correct model:** Transfer depends on both distribution alignment and whether the labeling function is compatible across domains.

4. **“For VLMs, you only ever need to tune the projector; the LLM doesn’t matter.”**  
   - **Why wrong:** MobileVLM uses a two-step pipeline: projector-only pretrain, then instruction tuning that updates projector + LLM (Sec. 4.1), and also reports LoRA-on-LLM as a viable alternative (Sec. 4.4).  
   - **Correct model:** Projector tuning aligns modalities; LLM tuning (full or LoRA) adapts reasoning/style/task behavior.

5. **“Merging LoRA into the base weights is always better for deployment.”**  
   - **Why wrong:** S-LoRA shows merging is fine for a single adapter, but breaks batching and causes duplication/swapping overhead when serving many adapters (Sec. 4).  
   - **Correct model:** Merge for single-tenant simplicity; keep separate for multi-tenant/high-throughput serving.

---

## Worked Examples

### Worked Example 1 — QLoRA setup (Transformers + PEFT) for a (text) base model (pattern extends to VLM LLM-backbone)

> Purpose: give the tutor a concrete snippet to reference when a student asks “what are the exact knobs for NF4 + double quant + BF16 compute?”

```python
import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model

# HF PEFT quantization guide defaults (NF4 + double quant + BF16 compute)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

model = AutoModelForCausalLM.from_pretrained(
    "mistralai/Mistral-7B-v0.1",
    quantization_config=bnb_config,
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    r=16,
    lora_alpha=8,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
```

**What to point out (sourced):**
- NF4 + double quant + BF16 compute are the standard QLoRA recipe (Dettmers; HF PEFT quantization guide)  
  https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf  
  https://huggingface.co/docs/peft/main/en/developer_guides/quantization
- Only LoRA params train; base is frozen (Dettmers Eq. 5–6).

### Worked Example 2 — VLM training “what gets trained when” (MobileVLM recipe)

Use this as a *procedural* worked example (no code in source, but concrete steps + hyperparams are in the paper):

1. **Pre-train alignment (projector-only):** freeze vision encoder + LLM; train projector on **CC-595K**, **1 epoch**, lr **2e-3**, batch **256** (MobileVLM Sec. 4.1).  
2. **Instruction tuning:** fine-tune projector + LLM on **LLaVA-Instruct-158K**, **1 epoch**, lr **2e-5**, batch **128**, AdamW, cosine LR, **3% warmup**, **no weight decay** (MobileVLM Sec. 4.1).  
3. **LoRA alternative:** during instruction tuning, freeze LLM except LoRA; LoRA config **r=128**, **α=256**; reported comparable performance to full fine-tuning on 6 benchmarks (MobileVLM Sec. 4.4).  
Source: https://arxiv.org/pdf/2312.16886.pdf

---

## Comparisons & Trade-offs

| Choice | What you train | Memory/compute | When to choose | Key source |
|---|---|---|---|---|
| Full fine-tuning | All weights | Highest optimizer/grad memory | Max quality when you can afford compute and want deep behavior change | PEFT taxonomy memory rationale (Adam overhead) https://arxiv.org/html/2303.15647v2 |
| LoRA | Low-rank adapters on selected layers | Low trainable params (often 0.01–0.5% per taxonomy) | Domain/task adaptation with limited compute; easy to swap adapters | PEFT taxonomy https://arxiv.org/html/2303.15647v2 |
| QLoRA | LoRA + frozen 4-bit base (NF4) | Much lower VRAM; extra quant/dequant overhead | When base model doesn’t fit in VRAM otherwise; want near-BF16 quality | Dettmers et al. https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf |
| Merge LoRA for serving | Merge \(\Delta W\) into \(W\) | Fast for single adapter; bad for many adapters | Single-tenant deployment | S-LoRA rationale https://arxiv.org/pdf/2311.03285.pdf |
| Keep adapters separate (multi-tenant) | Base + per-request LoRA | Enables batching across many adapters | SaaS / many domain variants | S-LoRA https://arxiv.org/pdf/2311.03285.pdf |

**Deployment note:** S-LoRA reports serving **2,000 adapters** simultaneously and large throughput gains vs naive approaches (paper + LMSYS blog) https://arxiv.org/pdf/2311.03285.pdf, https://lmsys.org/blog/2023-11-15-slora/.

---

## Prerequisite Connections

- **Transformer linear projections (Q/K/V/O, FFN).** Needed to understand *where* LoRA is inserted (LoRA modifies linear layers).
- **Quantization basics (blockwise quant/dequant).** Needed to understand QLoRA’s “frozen 4-bit weights, BF16 compute” pipeline (Dettmers Eq. 1–2, 5–6).
- **VLM architecture decomposition (vision encoder + projector + LLM).** Needed to decide whether to tune projector, LLM, or both (MobileVLM Sec. 3–4).
- **Domain adaptation fundamentals (source vs target, discrepancy, labeling shift).** Needed to reason about when fine-tuning helps vs fails under shift (Ben-David; Zhao).

---

## Socratic Question Bank

1. **If your target domain differs mainly in visual appearance (e.g., medical modality), which component would you try tuning first: projector, LLM via LoRA, or both? Why?**  
   *Good answer:* references VLM decomposition (MobileVLM) and argues alignment vs reasoning/style.

2. **In QLoRA, what parameters receive gradients, and what stays frozen? How can gradients “flow through” frozen quantized weights?**  
   *Good answer:* “only LoRA params get gradients; base weights frozen; forward dequantizes for compute” (Dettmers Eq. 5–6).

3. **What does the \(\lambda\) term represent in the domain adaptation bound, and why can’t domain invariance alone eliminate it?**  
   *Good answer:* labeling-function disagreement; invariance doesn’t fix conditional/label shift (Ben-David; Zhao).

4. **Why might merging LoRA weights into the base model hurt throughput when serving many adapters?**  
   *Good answer:* merging causes duplication or swapping; breaks batching; S-LoRA separates base compute from per-adapter compute.

5. **NF4 vs “standard FP4”: what assumption makes NF4 a good fit for pretrained weights?**  
   *Good answer:* weights approximately normal; NF4 uses normal quantiles (Dettmers; bitsandbytes docs).

6. **If you reduce visual tokens (e.g., 576→144), what trade-off are you making, and what evidence suggests it can work?**  
   *Good answer:* fewer tokens → faster; MobileVLM reports comparable/better benchmark scores with LDP.

7. **Suppose your model does great on source but fails on target. Which term(s) in the Ben-David bound could explain it?**  
   *Good answer:* large discrepancy \(d_{\mathcal H}\) and/or large \(\lambda\).

---

## Likely Student Questions

**Q: What’s the exact LoRA equation I should remember?** → **A:** Dettmers et al. write LoRA for a linear layer \(Y=XW\) as  
\[
Y = XW + sXL_1L_2
\]
with \(W\) frozen and \(L_1,L_2\) trainable low-rank factors (Eq. 3).  
Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

**Q: In QLoRA, are the 4-bit weights updated during training?** → **A:** No—QLoRA keeps the base weights frozen in 4-bit (NF4) and updates only LoRA parameters; forward pass dequantizes to BF16 for compute (Eq. 5–6).  
Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

**Q: What are the key QLoRA memory tricks and their default block sizes?** → **A:** NF4 4-bit weights + **double quantization** of quantization constants. Reported defaults: blocksize **64** for weights; constants quantized with **FP8** blocksize **256**, reducing constant overhead from **0.5** to **0.127 bits/param** (~**3GB** saved for 65B).  
Source: https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf

**Q: Where can LoRA be inserted in a VLM?** → **A:** In a typical VLM stack (vision encoder + projector + LLM), LoRA is commonly applied to **LLM linear layers** during instruction tuning while keeping other parts frozen or partially trained; MobileVLM reports LoRA during visual instruction tuning with **r=128, α=256** (Sec. 4.4).  
Source: https://arxiv.org/pdf/2312.16886.pdf

**Q: What’s a concrete VLM training schedule that uses freezing then tuning?** → **A:** MobileVLM: (1) projector-only pretrain on **CC-595K** for **1 epoch**, lr **2e-3**, batch **256**; (2) instruction tuning on **LLaVA-Instruct-158K** for **1 epoch**, lr **2e-5**, batch **128**, AdamW, cosine LR, **3% warmup**, no weight decay (Sec. 4.1).  
Source: https://arxiv.org/pdf/2312.16886.pdf

**Q: Why doesn’t “domain-invariant features” guarantee good target accuracy?** → **A:** Domain adaptation bounds include a labeling-disagreement term \(\lambda\) (Ben-David Thm. 1), and Zhao et al. give counterexamples where perfect invariance forces high joint error (Sec. 4.1).  
Sources: https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf and http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf

**Q: How do systems serve thousands of LoRA adapters without OOM or swapping?** → **A:** S-LoRA computes \(xW\) once and adds per-request \(xBA\), and uses **Unified Paging** to store **KV cache + adapter weights** in one paged GPU pool; reports serving **2,000 adapters** with stable throughput (Sec. 5–7).  
Source: https://arxiv.org/pdf/2311.03285.pdf (plus operational explainer: https://lmsys.org/blog/2023-11-15-slora/)

---

## Available Resources

### Videos
- [State of GPT (covers fine-tuning landscape incl. LoRA/PEFT)](https://www.youtube.com/watch?v=CRFON_RPa_E) — Surface when: student wants a broad, practical walkthrough of LoRA/QLoRA concepts and terminology.
- [AI Agents: Safety, Security, and Trust](https://youtube.com/watch?v=kJLiOGle3Lw) — Surface when: student pivots to deployment risk/guardrails for tool-using systems (adjacent to deployment discussions).

### Articles & Tutorials
- [Making LLMs even more accessible with bitsandbytes, 4-bit quantization and QLoRA (Hugging Face)](https://huggingface.co/blog/4bit-transformers-bitsandbytes) — Surface when: student asks “how do I actually load 4-bit and fine-tune adapters?”
- [PEFT Quantization Developer Guide (Hugging Face)](https://huggingface.co/docs/peft/main/en/developer_guides/quantization) — Surface when: student needs exact `BitsAndBytesConfig`/`prepare_model_for_kbit_training()` steps.
- [Practical Tips for Finetuning LLMs Using LoRA (Raschka)](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms) — Surface when: student asks about practical knobs (rank/alpha, overfitting, layer coverage) beyond the core papers.

---

## Visual Aids

![QLoRA combines 4-bit quantization with LoRA adapters to reduce fine-tuning memory. (Source: Dettmers et al.)](/api/wiki-images/evaluation-benchmarks/images/eugeneyan-writing-llm-patterns_022.webp)  
Show when: student asks “what is QLoRA at a high level?” or “why does 4-bit help memory?”

![LoRA adapters enable fine-tuning of frozen 4-bit quantized base models. (HuggingFace Blog)](/api/wiki-images/lora-peft/images/huggingface-co-blog-4bit-transformers-bitsandbytes_002.gif)  
Show when: student is confused about “how can you train if weights are quantized/frozen?”

---

## Key Sources

- [QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., NeurIPS 2023)](https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf) — definitive equations + NF4/DQ/paged optimizer details + benchmark numbers.
- [PEFT taxonomy + method comparisons](https://arxiv.org/html/2303.15647v2) — clean conceptual map of PEFT methods, parameter ranges, and where LoRA fits.
- [MobileVLM (training pipeline + LoRA in VLM stacks)](https://arxiv.org/pdf/2312.16886.pdf) — concrete VLM componentization, training schedule, and LoRA hyperparams in a multimodal setting.
- [S-LoRA (multi-tenant LoRA serving)](https://arxiv.org/pdf/2311.03285.pdf) — deployment mechanics for serving many adapters (paging, kernels, batching).
- [A theory of learning from different domains (Ben-David et al., 2006)](https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf) — target-risk bound separating source error, discrepancy, and labeling disagreement (\(\lambda\)).