## Core Definitions

**Vision-Language Model (VLM)**  
A vision-language model is a generative multimodal model that takes **image + text** inputs and produces **text** outputs, enabling tasks like visual question answering, captioning, and document understanding; Hugging Face characterizes VLMs as models that “learn simultaneously from images and texts” and are typically used as generative models with image+text inputs and text outputs. (Source: https://huggingface.co/blog/vlms)

**Visual tokens**  
“Visual tokens” are the sequence elements derived from an image (often patch/grid features from a vision encoder) that are fed into a language model either by concatenation with text tokens or via cross-attention/prefix mechanisms; the key operational idea is that an image becomes a **token sequence** analogous to text tokens, which then participates in Transformer attention. (Source: https://lilianweng.github.io/posts/2022-06-09-vlm/)

**LLaVA-style VLM (frozen vision encoder + projector + LLM)**  
A common open VLM pattern (explicitly described in MobileVLM) has three parts: **(1) a vision encoder**, **(2) an LLM**, and **(3) a projector** that aligns/compresses vision features into the LLM embedding space; training often proceeds in two steps: first train the projector with both backbone models frozen, then instruction-tune the projector + LLM. (Source: https://arxiv.org/pdf/2312.16886.pdf)

**Projection layer / multimodal projector**  
A projector is a learned mapping that converts vision-encoder hidden states (dimension \(D_v\)) into the LLM token embedding dimension (\(D_t\)), producing “image tokens” that can be consumed by the LLM. MobileVLM formalizes this as mapping \(Z\in\mathbb{R}^{N\times D_v}\) to \(V\in\mathbb{R}^{M\times D_t}\). (Source: https://arxiv.org/pdf/2312.16886.pdf)

**Visual instruction tuning**  
Visual instruction tuning is supervised fine-tuning (SFT) of a VLM on **instruction-following** multimodal data (image + instruction → response) so the model can follow open-ended prompts grounded in images; MobileVLM describes an “instruction tuning” stage that fine-tunes **projector + LLM** on an instruction dataset after an initial projector-alignment pretrain stage. (Source: https://arxiv.org/pdf/2312.16886.pdf)

**Dynamic resolution / patch-budget resizing (API-side)**  
In OpenAI’s vision-capable models, images are tokenized into 32×32 patches and may be **downscaled** to fit a model-specific **patch budget**; the docs define a patch-count formula and a shrink-factor procedure to resize images when the original patch count exceeds the budget. (Source: https://platform.openai.com/docs/guides/images-vision)

**GPT-4V (as an LMM example)**  
Chip Huyen frames GPT-4V as part of the push to incorporate additional modalities (like images) into LLMs, noting OpenAI’s system card statement that adding modalities is viewed by some as a key frontier; in tutoring, this is useful as a reference point for “closed” frontier multimodal systems vs open-source VLM recipes (Flamingo/BLIP-2/LLaVA-style). (Source: https://huyenchip.com/2023/10/10/multimodal.html)

---

## Key Formulas & Empirical Results

### LLaVA-style projector mapping (MobileVLM)
**Projector shape alignment (Eq. 1)** (supports: “why a projector exists; what dimensions must match”)  
- Input visual tokens: \(Z \in \mathbb{R}^{N \times D_v}\)  
- Output image tokens: \(V \in \mathbb{R}^{M \times D_t}\)  
Where \(D_v\) is the vision encoder hidden size and \(D_t\) is the LLM embedding size; \(M\) may be smaller than \(N\) if the projector compresses tokens.  
(Source: https://arxiv.org/pdf/2312.16886.pdf)

**Autoregressive conditioning (Eq. 2)** (supports: “VLMs still do next-token prediction”)  
MobileVLM describes autoregressive generation conditioned on multimodal tokens (image tokens + text tokens) to produce an output of length \(L\).  
(Source: https://arxiv.org/pdf/2312.16886.pdf)

### Token reduction result (MobileVLM, LDP projector)
**Token reduction with quality retention** (supports: “why compress visual tokens instead of lowering resolution”)  
- LDP reduces visual tokens **576 → 144 (−75%)** with equivalent or sometimes better benchmark performance.  
(Source: https://arxiv.org/pdf/2312.16886.pdf)

**Resolution vs token strategy (Table 11)** (supports: “keep resolution, reduce tokens”)  
Keeping 144 tokens via LDP beats reducing input resolution (RIR):  
- **LDP:** GQA 56.1, SQA 54.7, VQA 41.5, POPE 84.5, MME 1196.2, MMB 53.2  
- **RIR:** GQA 53.9, SQA 53.1, VQA 37.1, POPE 81.5, MME 1072.5, MMB 46.7  
(Source: https://arxiv.org/pdf/2312.16886.pdf)

### Two-step VLM training defaults (MobileVLM)
(supports: “what exactly is trained when?”)
1) **Pre-train (projector-only):** freeze vision encoder + LLM; train projector on **CC-595K** for **1 epoch**, lr **2e-3**, batch **256**.  
2) **Instruction tuning:** fine-tune **projector + LLM** on **LLaVA-Instruct-158K** for **1 epoch**, lr **2e-5**, batch **128**.  
Optimizer AdamW, **no weight decay**, cosine LR, **3% warmup**.  
(Source: https://arxiv.org/pdf/2312.16886.pdf)

### PEFT during visual instruction tuning (MobileVLM LoRA)
(supports: “how much do we train if we LoRA the LLM?”)
- Trainable params during instruction tuning when freezing all LLM params except LoRA: **8.87% (1.4B)** and **7.41% (2.7B)** of full LLM (as reported).  
- LoRA config: **r=128**, **α=256**; performance comparable to full finetuning on 6 benchmarks.  
(Source: https://arxiv.org/pdf/2312.16886.pdf)

### Flamingo: fixed visual-token interface + gated cross-attn
**Interleaved autoregressive objective (Eq. 1)** (supports: “how few-shot prompting works with interleaved images/text”)  
\[
p(y\mid x)=\prod_{\ell=1}^{L} p\big(y_\ell \mid y_{<\ell}, x_{\le \ell}\big)
\]
where \(x_{\le \ell}\) are images/videos preceding token \(\ell\) in the interleaved sequence.  
(Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)

**Perceiver Resampler output size** (supports: “why 64 visual tokens”)  
Perceiver Resampler outputs a **fixed 64 visual tokens** per image/video to reduce cross-attention cost.  
(Source: https://ar5iv.labs.arxiv.org/html/2204.14198)

**Gated XATTN-DENSE block (fusion definition)** (supports: “how to condition a frozen LM stably”)  
Inserted between frozen LM layers; for language features \(y\) and visual tokens \(x\):  
1) \(y \leftarrow y + \tanh(\alpha_{\text{xattn}})\cdot \text{attn}(q=y, kv=x)\)  
2) \(y \leftarrow y + \tanh(\alpha_{\text{dense}})\cdot \text{ffw}(y)\)  
with \(\alpha\) scalars initialized at **0** so initial behavior matches the frozen LM.  
(Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)

### BLIP-2: query-token bottleneck + two-stage objectives
**Bottleneck sizing** (supports: “fixed number of learned queries”)  
Typically **32 query tokens**, each **768-d**, producing \(Z\in\mathbb{R}^{32\times 768}\); example frozen ViT features: **257×1024** (ViT-L/14).  
(Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf)

**Stage-1 objectives** (supports: “what losses are used to align vision-language”)  
Stage-1 joint loss = **ITC + ITM + ITG**, with distinct attention masks (unimodal / bidirectional / multimodal causal).  
(Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf)

### OpenAI vision patch-budget resizing + token billing
(supports: “dynamic resolution in practice for API models”)
- Patch count: `ceil(width/32) * ceil(height/32)`  
- If over budget, compute shrink factor: \(\sqrt{(32^2 \cdot \text{patch_budget})/(width\cdot height)}\) and resize accordingly; billed tokens = resized_patch_count × multiplier (model-specific).  
(Source: https://platform.openai.com/docs/guides/images-vision)

### OpenAI vision fine-tuning constraints (dataset-side)
(supports: “what you can/can’t do in vision SFT with OpenAI”)
- JSONL chat format; images only in **user** messages (not assistant).  
- Max **50,000** image-containing examples; max **10 images/example**; max **10 MB/image**; formats **JPEG/PNG/WEBP**; RGB/RGBA.  
- `detail:"low"` resizes to **512×512** and uses **85 tokens** per image (cost control).  
(Source: https://platform.openai.com/docs/guides/vision-fine-tuning)

---

## How It Works

### A. LLaVA-style “projector + LLM” visual instruction tuning (MobileVLM recipe)
1) **Image → vision encoder features**  
   - Run a pretrained vision encoder on the image to get patch/token embeddings \(Z\in\mathbb{R}^{N\times D_v}\). (MobileVLM)

2) **Projector aligns/compresses vision tokens**  
   - Apply a learned projector to map \(Z\) into the LLM embedding dimension \(D_t\), producing image tokens \(V\in\mathbb{R}^{M\times D_t}\). (Eq. 1, MobileVLM)  
   - If using LDP, the projector uses depthwise conv + stride-2 downsampling to reduce token count while preserving spatial structure. (MobileVLM Sec. 3.4)

3) **Concatenate multimodal sequence for the LLM**  
   - Form an input sequence that includes image tokens \(V\) and text tokens (prompt/instruction).  
   - The LLM performs standard autoregressive next-token prediction conditioned on this multimodal prefix. (MobileVLM Eq. 2)

4) **Two-step training**  
   - **Step 1 (alignment pretrain):** freeze vision encoder + LLM; train projector only on image-text data (MobileVLM uses CC-595K, 1 epoch).  
   - **Step 2 (visual instruction tuning):** fine-tune projector + LLM on instruction data (MobileVLM uses LLaVA-Instruct-158K, 1 epoch).  
   - Optional: use LoRA to update only a small subset of LLM parameters during step 2. (MobileVLM Sec. 4.4)

### B. Alternative fusion patterns (for contrast during tutoring)
**Flamingo (cross-attention injection into frozen LM)**  
1) Encode image/video with a frozen vision encoder.  
2) Perceiver Resampler converts variable-length visual features into **64** tokens.  
3) Insert gated cross-attention blocks between frozen LM layers; gates init at 0 for stability.  
4) Train only inserted modules + resampler (LM and vision encoder frozen).  
(Source: Flamingo paper/blog PDF)

**BLIP-2 (query-token bottleneck + two-stage bootstrapping)**  
1) Frozen image encoder produces image features.  
2) Q-Former uses **learned query tokens** that cross-attend to image features to extract a fixed-size representation.  
3) Stage-1 trains Q-Former with ITC/ITM/ITG; Stage-2 projects queries to LLM embedding dim and trains with LM-style generation while LLM remains frozen.  
(Source: BLIP-2 paper)

---

## Teaching Approaches

### Intuitive (no math): “Translator + conversation”
- The vision encoder “speaks vision,” the LLM “speaks text.”  
- The **projector** is the translator that turns vision features into something the LLM can treat like extra “words” (visual tokens).  
- **Visual instruction tuning** is teaching the combined system to follow human-style instructions about images (not just caption them).

### Technical (with math): “Match dimensions, then do next-token prediction”
- Vision encoder outputs \(Z\in\mathbb{R}^{N\times D_v}\).  
- Projector maps to \(V\in\mathbb{R}^{M\times D_t}\) so the LLM can consume it (MobileVLM Eq. 1).  
- The LLM then models \(p(\hat{y})=\prod_i p(\hat{y}_i\mid \hat{y}_{<i}, V, \text{text})\) (MobileVLM Eq. 2 is the same idea: autoregressive generation conditioned on multimodal tokens).  
- Two-step training: first learn the mapping (projector-only), then learn instruction-following (projector+LLM, optionally via LoRA).

### Analogy-based: “Image becomes a short ‘visual paragraph’”
- Patch embeddings are like many raw sentences about pixels.  
- The projector compresses them into a shorter paragraph (e.g., 576→144 tokens in MobileVLM) that still preserves the important details.  
- Instruction tuning teaches the LLM how to “quote” that paragraph correctly when answering questions.

---

## Common Misconceptions (required)

1) **“Visual instruction tuning means training the vision encoder from scratch.”**  
   - Why wrong: MobileVLM’s described pipeline explicitly freezes the vision encoder during projector pretraining, and the key alignment happens via the projector (and later LLM tuning).  
   - Correct model: Visual instruction tuning is typically **SFT on multimodal instruction data**, often with a **frozen** vision encoder and a trainable projector/LLM (or PEFT on the LLM). (Source: https://arxiv.org/pdf/2312.16886.pdf)

2) **“The projector is just a shape fix; it doesn’t affect quality much.”**  
   - Why wrong: MobileVLM motivates projector design choices (Q-Former bottleneck vs MLP background tokens) and shows large token-reduction (576→144) with competitive performance; Table 11 shows LDP beats reducing input resolution.  
   - Correct model: The projector is both a **dimension aligner** and often a **token compressor / information filter** that strongly impacts speed and accuracy. (Source: https://arxiv.org/pdf/2312.16886.pdf)

3) **“To make VLMs faster, you should always lower image resolution.”**  
   - Why wrong: MobileVLM reports that keeping 144 tokens via LDP outperforms reducing input resolution (RIR) across multiple benchmarks (Table 11).  
   - Correct model: You can often keep resolution (retain details) but reduce **token count** via smarter projection/compression. (Source: https://arxiv.org/pdf/2312.16886.pdf)

4) **“Flamingo and LLaVA do the same fusion: they just concatenate image tokens.”**  
   - Why wrong: Flamingo conditions a frozen LM by inserting **gated cross-attention blocks** and uses a **Perceiver Resampler** to output a fixed 64 tokens; this is not the same as simple concatenation into the LM input.  
   - Correct model: Fusion can be done by **prefix/concatenation** (LLaVA-style) or by **cross-attention injection** (Flamingo), with different training stability and compute tradeoffs. (Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)

5) **“Dynamic resolution is a training trick inside the model.”**  
   - Why wrong: In the OpenAI API docs, “dynamic resolution” behavior is described as **patch-budget tokenization and resizing** at input processing time (compute/cost control), not as a learned training-time mechanism.  
   - Correct model: For patch-based API models, images are resized to fit a **patch budget** using explicit formulas; this affects token cost and sometimes fidelity. (Source: https://platform.openai.com/docs/guides/images-vision)

---

## Worked Examples

### 1) Minimal “LLaVA-style” forward-shape walkthrough (PyTorch-like pseudocode)
Goal: give the tutor a concrete step-by-step to debug “dimension mismatch” questions using MobileVLM’s Eq. (1) shapes.

```python
# Given:
# vision_encoder(image) -> Z: (N, Dv)
# projector(Z) -> V: (M, Dt)
# llm.embed_tokens(text_ids) -> T: (L, Dt)

Z = vision_encoder(image)          # Z: [N, Dv]
V = projector(Z)                   # V: [M, Dt]  (MobileVLM Eq. 1)
T = llm.embed_tokens(text_ids)     # T: [L, Dt]

# Multimodal prefix: concatenate along sequence dimension
X = concat([V, T], dim=0)          # X: [M+L, Dt]

# Decoder-only LLM does autoregressive next-token prediction conditioned on X
logits = llm(inputs_embeds=X)      # predicts next tokens (MobileVLM Eq. 2 idea)
```

Tutor notes (what to check live):
- If the student’s LLM embedding dim is \(D_t\), the projector output must be \(D_t\). (MobileVLM Eq. 1)
- Token count \(M\) is a design choice; MobileVLM shows compressing tokens (e.g., 576→144) can preserve quality. (MobileVLM Sec. 5.1)

### 2) Compute OpenAI patch count + resizing trigger (from Images/Vision docs)
Use when a student asks “why did my large image get resized / cost so many tokens?”

```python
import math

def patch_count(w, h, patch=32):
    return math.ceil(w/patch) * math.ceil(h/patch)

w, h = 1800, 2400
original = patch_count(w, h)  # Eq.1 in docs
original
```

- For 1800×2400: `ceil(1800/32)=57`, `ceil(2400/32)=75`, patches = **4275**.  
- If model budget is **1536 patches** (docs example family), it must shrink.  
Docs’ worked example says 1800×2400 is resized to **1056×1408** with patch count **1452**.  
(Source: https://platform.openai.com/docs/guides/images-vision)

### 3) OpenAI vision fine-tuning JSONL example (format constraints)
Use when a student asks “what does a valid training example look like?”

```jsonl
{"messages":[
  {"role":"user","content":[
    {"type":"text","text":"What is the object on the table? Answer briefly."},
    {"type":"image_url","image_url":{"url":"https://example.com/image.jpg","detail":"low"}}
  ]},
  {"role":"assistant","content":"A mug."}
]}
```

Tutor notes:
- Images must be in **user** messages; you **cannot** put images in assistant messages.  
- `detail:"low"` forces 512×512 and **85 tokens** per image (cost control).  
(Source: https://platform.openai.com/docs/guides/vision-fine-tuning)

---

## Comparisons & Trade-offs

| Design choice | Mechanism | Compute/token implications | When to choose | Sources |
|---|---|---|---|---|
| **Concatenate visual tokens into LM input (LLaVA-style)** | Project vision features into \(D_t\), treat as prefix tokens | Sequence length increases by \(M\); attention cost grows with length | Simple, effective; common for open VLMs; pairs well with projector compression | MobileVLM (projector Eq.1, token reduction) https://arxiv.org/pdf/2312.16886.pdf |
| **Cross-attention injection (Flamingo)** | Insert gated cross-attn blocks between frozen LM layers; resample to fixed 64 tokens | Cross-attn cost controlled by fixed token count; stable via 0-init gates | Interleaved multimodal prompting; few-shot; keep LM frozen | Flamingo gated block + resampler https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf |
| **Query-token bottleneck (BLIP-2)** | Learned queries cross-attend to image features; fixed query count (e.g., 32) | Fixed-size interface independent of image token grid | Efficient bootstrapping with frozen encoders/LLM; strong zero-shot | BLIP-2 https://proceedings.mlr.press/v202/li23q/li23q.pdf |
| **Reduce resolution vs reduce tokens** | Downscale image vs compress token sequence | Downscaling may lose details; token compression can preserve details | Prefer token compression when detail matters; MobileVLM shows LDP > RIR | MobileVLM Table 11 https://arxiv.org/pdf/2312.16886.pdf |
| **Full instruction tuning vs LoRA PEFT (on LLM)** | Update all LLM weights vs low-rank adapters | LoRA reduces trainable params; can match full FT in MobileVLM report | Use LoRA when compute/memory constrained | MobileVLM LoRA r=128 α=256 https://arxiv.org/pdf/2312.16886.pdf |

---

## Prerequisite Connections

- **Transformer attention basics (self-attention, token sequences):** Visual tokens only make sense if the student understands that Transformers operate over sequences and attention cost depends on sequence length. (Source for attention formula context: PEFT A2Z attention Eq.2 https://arxiv.org/html/2504.14117)
- **Autoregressive language modeling:** VLMs like MobileVLM and Flamingo still optimize/generate via next-token prediction conditioned on multimodal context. (MobileVLM Eq.2; Flamingo Eq.1)
- **Embedding dimension alignment:** The projector exists because vision encoder hidden size \(D_v\) typically differs from LLM embedding size \(D_t\). (MobileVLM Eq.1)
- **Supervised fine-tuning (SFT) format:** Visual instruction tuning is operationally SFT on (image, instruction → response) examples; OpenAI vision fine-tuning docs provide concrete constraints and JSONL format. (https://platform.openai.com/docs/guides/vision-fine-tuning)

---

## Socratic Question Bank

1) **If your vision encoder outputs \(Z\in\mathbb{R}^{N\times D_v}\) and your LLM expects embeddings in \(\mathbb{R}^{D_t}\), what must the projector guarantee?**  
   - Good answer: output tokens must be \(V\in\mathbb{R}^{M\times D_t}\); it aligns dimensions (MobileVLM Eq.1).

2) **Why might reducing visual tokens (e.g., 576→144) be preferable to lowering image resolution? What failure mode does resolution reduction introduce?**  
   - Good answer: downscaling can remove small text/details; MobileVLM Table 11 shows token reduction via LDP outperforms RIR.

3) **In a two-step training recipe, what problem is step 1 solving that step 2 cannot solve as easily from scratch?**  
   - Good answer: step 1 aligns vision features to the LLM embedding space by training projector while backbones are frozen; step 2 teaches instruction-following once alignment exists (MobileVLM Sec. 4.1).

4) **How does Flamingo keep a frozen LM stable when adding new multimodal capacity?**  
   - Good answer: gated cross-attn blocks with gates initialized to 0 so initial behavior matches the frozen LM (Flamingo gated block).

5) **What does it mean that BLIP-2 uses “32 query tokens”? What stays constant and what can vary?**  
   - Good answer: number of query tokens is fixed; image feature grid can vary but queries extract a fixed-size representation (BLIP-2 bottleneck sizing).

6) **If an API model has a patch budget and your image exceeds it, what happens and why does that affect cost?**  
   - Good answer: image is resized to fit patch budget; billed tokens depend on resized patch count (OpenAI images-vision patch formulas).

7) **When using LoRA during visual instruction tuning, what is the conceptual difference between “training the LLM” and “training adapters on the LLM”?**  
   - Good answer: base weights frozen; only low-rank adapter params updated; MobileVLM reports comparable performance with LoRA (r=128, α=256).

---

## Likely Student Questions

**Q: What exactly is the projector doing in LLaVA-style models?**  
→ **A:** It maps vision encoder tokens \(Z\in\mathbb{R}^{N\times D_v}\) into the LLM embedding dimension, producing image tokens \(V\in\mathbb{R}^{M\times D_t}\) so the LLM can consume them as part of its token sequence. (MobileVLM Eq. 1: https://arxiv.org/pdf/2312.16886.pdf)

**Q: What’s the standard two-stage training schedule for a LLaVA-like model (numbers)?**  
→ **A:** MobileVLM reports: (1) projector-only pretrain with vision encoder + LLM frozen on CC-595K for 1 epoch, lr 2e-3, batch 256; (2) instruction tuning fine-tuning projector + LLM on LLaVA-Instruct-158K for 1 epoch, lr 2e-5, batch 128; AdamW, no weight decay, cosine LR, 3% warmup. (https://arxiv.org/pdf/2312.16886.pdf)

**Q: Is it better to reduce image resolution or reduce visual tokens for efficiency?**  
→ **A:** MobileVLM’s Table 11 shows token reduction via LDP (keeping 144 tokens) outperforms reducing input resolution (RIR) across benchmarks (e.g., VQA 41.5 vs 37.1; MME 1196.2 vs 1072.5). (https://arxiv.org/pdf/2312.16886.pdf)

**Q: How does Flamingo fuse vision into a frozen language model?**  
→ **A:** It uses a Perceiver Resampler to output a fixed **64** visual tokens, then inserts **gated cross-attention** blocks between frozen LM layers: \(y \leftarrow y + \tanh(\alpha)\cdot \text{attn}(q=y,kv=x)\) (plus a gated FFN), with gates initialized to 0 for stability. (https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)

**Q: What are BLIP-2’s training objectives in stage 1?**  
→ **A:** Stage 1 uses a joint loss of **ITC (contrastive)**, **ITM (matching)**, and **ITG (image-grounded text generation)**, with different attention masks (unimodal, bidirectional, multimodal causal). (https://proceedings.mlr.press/v202/li23q/li23q.pdf)

**Q: In OpenAI’s vision API, what does `detail: low` do?**  
→ **A:** For vision fine-tuning, `detail:"low"` resizes the image to **512×512** and represents it with **85 tokens** regardless of original size (reducing cost). (https://platform.openai.com/docs/guides/vision-fine-tuning)

**Q: Why did my image get resized when sending it to a vision model?**  
→ **A:** Patch-based models have a patch budget; patch count is `ceil(w/32)*ceil(h/32)`. If over budget, the system computes a shrink factor and resizes to fit; billed tokens depend on resized patch count and a model-specific multiplier. (https://platform.openai.com/docs/guides/images-vision)

**Q: Can I include images in the assistant messages in OpenAI vision fine-tuning JSONL?**  
→ **A:** No—OpenAI’s vision fine-tuning guide states you **cannot** include images in messages with the **assistant** role; images are inputs in user messages only. (https://platform.openai.com/docs/guides/vision-fine-tuning)

---

## Available Resources

### Videos
- [State of GPT (fine-tuning landscape incl. LoRA/PEFT)](https://youtube.com/watch?v=CRFON_RPa_E) — Surface when: student asks “where does LoRA fit in modern fine-tuning workflows?” or needs high-level framing of PEFT.
- [Flamingo: a Visual Language Model for Few-Shot Learning (Paper Explained)](https://youtube.com/watch?v=EhlnhGBZZAo) — Surface when: student is confused about Flamingo’s resampler + gated cross-attention vs token concatenation.

### Articles & Tutorials
- [Practical Tips for Finetuning LLMs Using LoRA (Raschka)](https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms) — Surface when: student asks for practical LoRA hyperparameter heuristics and training pitfalls (overfitting, rank/alpha choices).
- [The Transformer Family v2 (Weng)](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/) — Surface when: student needs a refresher on attention/Transformer internals to understand token fusion costs.
- [LoRA: Low-Rank Adaptation of Large Language Models (Hu et al. 2021)](https://arxiv.org/abs/2106.09685) — Surface when: student wants the original LoRA motivation and formalism.
- [Hugging Face PEFT library](https://github.com/huggingface/peft) — Surface when: student asks “how do I implement LoRA/adapters in practice?”
- [Large Multimodal Models (Weng)](https://lilianweng.github.io/posts/2022-06-09/vlm/) — Surface when: student asks for a taxonomy of VLM fusion strategies (tokens vs prefix vs cross-attn).

---

## Visual Aids

![VLMs handle diverse tasks from captioning to document understanding. (HuggingFace Blog)](/api/wiki-images/vision-language-models/images/huggingface-co-blog-vlms_001.jpg)  
Show when: opening motivation—“what do VLMs do beyond VQA?”

![Projector aligns image features with text embeddings for the language decoder. (HuggingFace Blog)](/api/wiki-images/vision-language-models/images/huggingface-co-blog-vlms_005.jpg)  
Show when: student asks “what is the projector and why do we need it?”

![GPT-4V use cases illustrating multimodal reasoning and interaction. (Huyen Chip)](/api/wiki-images/vision-language-models/images/huyenchip-2023-10-10-multimodal-html_002.png)  
Show when: student asks “what kinds of tasks does GPT-4V-style multimodality enable?”

![CLIP vs. Flamingo: contrasting architectures, objectives, and capabilities in vision-language AI.](/api/wiki-images/vision-language-models/images/huyenchip-2023-10-10-multimodal-html_019.png)  
Show when: comparing discriminative (CLIP) vs generative few-shot (Flamingo) and transitioning to instruction-tuned VLMs.

![Adapter architectures for LMMs reduce trainable parameters while preserving pretrained knowledge.](/api/wiki-images/vision-language-models/images/huyenchip-2023-10-10-multimodal-html_022.png)  
Show when: student asks “how do we train multimodal models efficiently without full finetuning?”

---

## Key Sources

- [MobileVLM](https://arxiv.org/pdf/2312.16886.pdf) — Concrete LLaVA-style pipeline, projector equation/shapes, two-step training defaults, and token-reduction vs resolution empirical results.
- [Flamingo (DeepMind blog PDF)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf) — Precise gated cross-attention block definition, Perceiver Resampler algorithm, and interleaved objective.
- [BLIP-2](https://proceedings.mlr.press/v202/li23q/li23q.pdf) — Two-stage bootstrapping, query-token bottleneck sizing, and explicit ITC/ITM/ITG objectives with masking.
- [OpenAI Images & Vision guide](https://platform.openai.com/docs/guides/images-vision) — Patch-budget resizing formulas, `detail` behavior, and token-cost mechanics for dynamic resolution in practice.
- [OpenAI Vision fine-tuning guide](https://platform.openai.com/docs/guides/vision-fine-tuning) — Authoritative dataset JSONL format and hard constraints (image counts/sizes/formats; `detail:"low"` = 85 tokens).