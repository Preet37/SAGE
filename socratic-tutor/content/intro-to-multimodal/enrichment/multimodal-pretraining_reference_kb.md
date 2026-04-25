## Core Definitions

**Multi-modal pre-training** — Training a model on paired or interleaved data from multiple modalities (e.g., images + text, video + text) so it learns cross-modal representations and/or can generate one modality conditioned on another. In modern VLMs this is often done either (a) with **contrastive** objectives that align image and text embeddings (CLIP-style), or (b) with **autoregressive next-token prediction** over text conditioned on visual inputs (Flamingo-style). (Chip Huyen survey frames these as foundational multimodal training patterns; Flamingo defines the interleaved conditional LM objective explicitly.) Sources: https://huyenchip.com/2023/10/10/multimodal.html , https://ar5iv.labs.arxiv.org/html/2204.14198

**Interleaved training (interleaved vision/text sequences)** — A pre-training setup where the model is trained on sequences that contain multiple images/videos and text in arbitrary order (like webpages), and the model predicts the next text token conditioned on the preceding text and the relevant preceding visuals. Flamingo formalizes this as conditioning on the set of images/videos that occur before each token position and uses masking so each token attends to the most recent image. Sources: https://ar5iv.labs.arxiv.org/html/2204.14198 , https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

**Contrastive pre-training (image–text contrastive learning)** — A multi-modal objective that learns a shared embedding space for images and text by making matched image–text pairs have higher similarity than mismatched pairs (often using in-batch negatives). BLIP-2’s Stage-1 includes an **Image-Text Contrastive (ITC)** loss that aligns an image representation (from query tokens) with a text representation (the [CLS] embedding), using in-batch negatives. Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

**Natively multi-modal** — In this lesson’s usage: a model trained so that multi-modal inputs are part of its core training distribution/objective (e.g., interleaved image+text next-token prediction), rather than only being added later as a thin adapter on top of a text-only model. Flamingo is trained on interleaved multimodal sequences with an autoregressive objective conditioned on visuals; BLIP-2 bootstraps multimodality via a learned bridge (Q-Former) between frozen vision and frozen LLM. Sources: https://ar5iv.labs.arxiv.org/html/2204.14198 , https://proceedings.mlr.press/v202/li23q/li23q.pdf

**Flamingo** — A family of visual language models that (i) bridges a pretrained vision encoder and a pretrained language model, (ii) handles arbitrarily interleaved visual and textual inputs, and (iii) is trained with an autoregressive next-token objective conditioned on preceding visuals. Key mechanisms: **Perceiver Resampler** (fixed number of visual tokens) and **gated cross-attention blocks** inserted into a frozen LM with gates initialized to 0 for stability. Sources: https://ar5iv.labs.arxiv.org/html/2204.14198 , https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

**BLIP-2** — A two-stage pre-training strategy that bootstraps vision-language learning using a frozen image encoder and a frozen LLM, connected by a lightweight **Q-Former** with learnable query tokens that cross-attend to image features. Stage-1 trains Q-Former with ITC/ITM/ITG; Stage-2 trains a projection + LM objective to generate text conditioned on the visual prompts. Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf (HF overview echoes this framing: https://huggingface.co/docs/transformers/model_doc/blip-2)

**LAION-5B** — A web-scale dataset of **5.85B** image–text pairs filtered from Common Crawl using CLIP cosine similarity thresholds (e.g., keep if similarity ≥ τ; English threshold 0.28, non-English 0.26). Includes metadata such as watermark/NSFW/toxic scores. Source: https://arxiv.org/abs/2210.08402

---

## Key Formulas & Empirical Results

### Flamingo: interleaved conditional LM objective + masking
**Autoregressive objective (Flamingo Eq. 1):**
\[
p(y\mid x)=\prod_{\ell=1}^{L} p\big(y_\ell \mid y_{<\ell}, x_{\le \ell}\big)
\]
- \(y_\ell\): \(\ell\)-th text token; \(y_{<\ell}\): previous text tokens.
- \(x_{\le \ell}\): the set of images/videos that occur before token position \(\ell\) in the interleaved sequence.  
Supports claim: Flamingo is trained as a next-token predictor over text, conditioned on interleaved visuals.  
Sources: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf , https://ar5iv.labs.arxiv.org/html/2204.14198

**Per-token “most recent image” indexing (masking):** define \(\phi(\ell)\) = index of the last image/video before token \(\ell\). Cross-attention is masked so token \(\ell\) attends only to visual tokens of \(x_{\phi(\ell)}\).  
Supports claim: interleaving can scale to many images because each token only attends to one image’s tokens.  
Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

### Flamingo: Perceiver Resampler + gated cross-attention block
**Perceiver Resampler (fixed visual token bottleneck):**
- Input visual features \(x_f\in\mathbb{R}^{[T,S,d]}\) (time, space, dim), flattened to \([T\cdot S, d]\) with learned time embeddings.
- Learned latents \(x\in\mathbb{R}^{[R,d]}\); iterate attention+FFW updates; output is fixed \(R\) tokens (in practice **64**).  
Supports claim: converts variable-size vision features into a fixed token budget.  
Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

**Gated XATTN-DENSE block (inserted between frozen LM layers):**
1) \(y \leftarrow y + \tanh(\alpha_{\text{xattn}})\cdot \text{attn}(q=y, kv=x)\)  
2) \(y \leftarrow y + \tanh(\alpha_{\text{dense}})\cdot \text{ffw}(y)\)  
with learnable scalars \(\alpha_{\text{xattn}},\alpha_{\text{dense}}\) initialized at **0**.  
Supports claim: stable conditioning of a frozen LM; initial behavior matches the original LM.  
Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

### Flamingo: multi-dataset training loss
**Weighted mixture NLL (Flamingo Eq. 2):**
\[
\sum_{m=1}^{M}\lambda_m \, \mathbb{E}_{(x,y)\sim \mathcal{D}_m}\left[-\sum_{\ell=1}^{L}\log p(y_\ell|y_{<\ell},x_{\le \ell})\right]
\]
Supports claim: trained on a mixture of datasets (interleaved webpages + image-text + video-text).  
Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf

### Flamingo: key empirical results + ablations (few-shot)
**32-shot Flamingo-80B (Table 1):** OKVQA **57.8**, VQAv2 **67.6**, COCO CIDEr **113.8**, VATEX CIDEr **65.1**, VizWiz **49.8** (plus others in supplement).  
Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf

**Ablations (Flamingo-3B, 4-shot DEV, Table 3):**
- Remove M3W interleaved webpages: overall **70.7 → 53.4** (largest drop).
- No tanh gating: **70.7 → 66.5**.
- Unfreezing LM hurts: **70.7 → 62.7** (catastrophic forgetting).  
Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf

### BLIP-2: Stage-1 objectives + Stage-2 bootstrapping
**Q-Former bottleneck sizing (example):**
- Learnable query tokens: typically **32 queries**, each **768-d**; output \(Z\in\mathbb{R}^{32\times 768}\).
- Example frozen ViT features: **257×1024** (ViT-L/14).  
Supports claim: fixed-size visual interface independent of image resolution.  
Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

**Stage-1 joint loss:** ITC + ITM + ITG (with different attention masks).  
Supports claim: BLIP-2 learns alignment + matching + grounded generation before connecting to the LLM.  
Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

**Stage-2:** project queries to LLM embedding dim; prepend as soft visual prompts; train with LM loss (decoder-only) or prefix LM loss (encoder–decoder).  
Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

**Result highlight:** BLIP-2 zero-shot VQAv2 test-dev **65.0** vs Flamingo80B **56.3** (BLIP-2 uses **54× fewer trainable params**).  
Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

### LAION-5B: filtering criterion + dataset scale
**CLIP filtering criterion:**
- Compute \(s=\cos(\mathbf{e}_{img},\mathbf{e}_{txt})\); keep if \(s\ge\tau\).
- Thresholds: English remove if \(s<0.28\); non-English remove if \(s<0.26\).
- From ~50B candidates, removes ~90%, leaving just under 6B (LAION-5B = **5.85B**).  
Source: https://arxiv.org/abs/2210.08402

---

## How It Works

### A. Contrastive multi-modal pre-training (BLIP-2 Stage-1 ITC as a concrete template)
1) **Encode image** with a *frozen* vision encoder → patch/grid features.
2) **Query bottleneck (Q-Former):** feed learnable query tokens that cross-attend to frozen image features to produce a fixed set of query outputs \(Z\).
3) **Encode text** with Q-Former text side to get a text representation (e.g., [CLS]).
4) **Compute similarity** between image and text representations (BLIP-2: compute sim(query_i, text_cls) and take max over queries).
5) **Contrastive loss with in-batch negatives:** push matched pairs together, mismatched pairs apart.
6) Optionally add:
   - **ITM (matching):** binary classifier for matched/unmatched pairs with hard negatives.
   - **ITG (grounded generation):** LM-style generation conditioned on queries with a multimodal causal mask.  
Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

### B. Interleaved multi-modal next-token pre-training (Flamingo)
1) **Prepare interleaved sequences** like: text with `<image>` tags and multiple images/videos (webpage-like). (Flamingo mentions literal `<image>` tag and `<EOC>` token in its pipeline.)  
Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf
2) **Encode each image/video** with a vision encoder (frozen in Flamingo) → spatio-temporal features.
3) **Resample to fixed visual tokens** using Perceiver Resampler → 64 tokens per image/video.
4) **Condition a frozen LM** by inserting gated cross-attention blocks between LM layers; train only the inserted modules + resampler (LM and vision encoder frozen).
5) **Apply per-token masking:** for each text token position \(\ell\), allow cross-attention only to the most recent image/video \(x_{\phi(\ell)}\).
6) **Train with autoregressive NLL** over text tokens using the interleaved conditional objective \(p(y_\ell|y_{<\ell},x_{\le \ell})\), often over a mixture of datasets with weights \(\lambda_m\).  
Sources: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf , https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf

### C. “Bridge a frozen vision encoder to a frozen LLM” (BLIP-2 full pipeline)
1) **Stage-1 (learn cross-modal representation in the bridge):**
   - Train Q-Former with ITC/ITM/ITG while keeping the image encoder frozen.
2) **Stage-2 (teach the LLM to use visual prompts):**
   - Project Q-Former query outputs to the LLM embedding dimension.
   - Prepend projected queries as soft prompts to the LLM input.
   - Train with LM loss (decoder-only) or prefix LM loss (encoder–decoder).  
Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

---

## Teaching Approaches

### Intuitive (no math)
- **Two big families of objectives:**
  1) **“Match”**: learn that an image and its caption belong together (contrastive alignment; BLIP-2 ITC).
  2) **“Continue the story”**: given text so far and the images you’ve seen, predict the next word (Flamingo interleaved next-token prediction).
- **Interleaving matters** because real documents mix images and text; training on that format teaches the model to use images as context during generation.

### Technical (with math)
- Contrastive alignment uses a similarity score (BLIP-2: max over query-to-text similarities) and in-batch negatives to separate matched vs mismatched pairs. (BLIP-2 Stage-1 ITC.)  
Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf
- Interleaved generative training optimizes:
  \[
  \prod_{\ell} p(y_\ell \mid y_{<\ell}, x_{\le \ell})
  \]
  with masking via \(\phi(\ell)\) so each token attends to the most recent image’s 64 resampled tokens.  
Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

### Analogy-based
- **Contrastive**: like learning a bilingual dictionary between “image language” and “text language”—matched pairs are synonyms, mismatched pairs are not.
- **Interleaved next-token**: like reading a comic book; when you’re on a speech bubble, you mostly look at the most recent panel (Flamingo’s “most recent image” masking).

---

## Common Misconceptions

1) **“Multi-modal pre-training just means concatenating image tokens and text tokens and training like a normal LM.”**  
   - Why wrong: Many successful systems *don’t* simply concatenate raw patch tokens into the LM context; they introduce **bottlenecks** (Perceiver Resampler: 64 tokens; Q-Former: ~32 queries) and/or **cross-attention adapters** to control compute and preserve pretrained LM behavior.  
   - Correct model: Multi-modal pre-training often hinges on *how* vision is injected (resampling + gated cross-attn in Flamingo; query bottleneck + staged objectives in BLIP-2).  
   Sources: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf , https://proceedings.mlr.press/v202/li23q/li23q.pdf

2) **“Flamingo attends to all previous images for every token, so it must blow up compute as you add images.”**  
   - Why wrong: Flamingo explicitly masks cross-attention so each token attends only to the **most recent** image/video \(x_{\phi(\ell)}\), not all previous ones.  
   - Correct model: Compute per token is bounded by the fixed visual token count (64) for one image at a time; this is part of how it generalizes to many-shot prompting.  
   Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

3) **“If you have a strong pretrained LM, you should unfreeze it during multimodal training to get the best results.”**  
   - Why wrong: Flamingo’s ablations show **unfreezing the LM hurts** (catastrophic forgetting): fine-tuning pretrained LM drops overall score **70.7 → 62.7** (Flamingo-3B, 4-shot DEV).  
   - Correct model: Keep LM frozen and train small inserted modules (gated cross-attn blocks) to preserve language knowledge while adding visual conditioning.  
   Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf

4) **“LAION-5B is just ‘5B random image-caption pairs’; there’s no quality control.”**  
   - Why wrong: LAION-5B is explicitly **CLIP-filtered** using cosine similarity thresholds (e.g., English keep if \(s\ge 0.28\)), removing ~90% of candidates from ~50B.  
   - Correct model: It’s web-scale, but with a specific automated filtering pipeline and released safety/metadata scores (watermark/NSFW/toxic).  
   Source: https://arxiv.org/abs/2210.08402

5) **“BLIP-2 is basically Flamingo with a different name.”**  
   - Why wrong: Flamingo conditions a frozen LM via **gated cross-attention blocks** and trains on **interleaved sequences** with an autoregressive objective. BLIP-2 uses a **Q-Former query bottleneck** and a **two-stage** training scheme (Stage-1 ITC/ITM/ITG; Stage-2 generative bootstrapping into the LLM via soft prompts).  
   - Correct model: Both bridge vision and language efficiently, but the *interface* (cross-attn adapters vs query tokens + projection) and *objectives* differ.  
   Sources: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf , https://proceedings.mlr.press/v202/li23q/li23q.pdf

---

## Worked Examples

### Worked example 1: Write down Flamingo’s training probability for a tiny interleaved prompt
**Prompt structure (conceptual):**
- Sequence contains: text tokens, then an image, then more text tokens.
- Let the text tokens be \(y_1, y_2, \dots, y_L\).
- Let there be one image \(x_1\) that appears before token positions \(\ell \ge k\).

**Using Flamingo Eq. 1:**
\[
p(y\mid x)=\prod_{\ell=1}^{L} p(y_\ell \mid y_{<\ell}, x_{\le \ell})
\]

- For \(\ell < k\): \(x_{\le \ell}\) is empty (no image yet), so the model is effectively a text-only LM at those positions.
- For \(\ell \ge k\): \(x_{\le \ell}=\{x_1\}\), so each next-token distribution is conditioned on the image (via cross-attention to the resampled 64 visual tokens).

**Masking detail (most recent image):**
- \(\phi(\ell)=0\) for \(\ell<k\), \(\phi(\ell)=1\) for \(\ell\ge k\).
- Cross-attention for token \(\ell\) is allowed only to tokens of \(x_{\phi(\ell)}\) (so to \(x_1\) once it appears).  
Sources: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

### Worked example 2: LAION-5B filtering decision for one pair
Given an image embedding \(\mathbf{e}_{img}\) and text embedding \(\mathbf{e}_{txt}\) from CLIP:
1) Compute cosine similarity:
\[
s=\cos(\mathbf{e}_{img},\mathbf{e}_{txt})
\]
2) Keep the pair if \(s\ge\tau\).
- If English: \(\tau=0.28\).
- If non-English: \(\tau=0.26\).  
Source: https://arxiv.org/abs/2210.08402

---

## Comparisons & Trade-offs

| Design choice | What it is | Pros | Cons | Choose when | Sources |
|---|---|---|---|---|---|
| Contrastive pre-training (ITC / CLIP-style) | Align image/text embeddings using similarity + negatives | Strong retrieval/alignment signal; efficient supervision from pairs | Doesn’t directly train long-form generation unless combined with generative losses | You want shared embedding space + robust alignment; can be Stage-1 for bridging | BLIP-2 Stage-1 ITC: https://proceedings.mlr.press/v202/li23q/li23q.pdf |
| Interleaved next-token pre-training | Autoregressive LM over text conditioned on interleaved visuals | Directly trains generation conditioned on visuals; supports in-context few-shot prompting | Requires interleaved corpora + careful masking; heavier training | You want a “multimodal LM” behavior (dialogue, few-shot) | Flamingo Eq.1 + masking: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf |
| Q-Former query bottleneck (BLIP-2) | Learnable queries cross-attend to frozen image features; fixed-size output | Efficient interface; can keep vision encoder + LLM frozen; staged training | Requires extra bridge training stages/objectives | You want to cheaply connect frozen vision + frozen LLM | https://proceedings.mlr.press/v202/li23q/li23q.pdf |
| Perceiver Resampler + gated cross-attn (Flamingo) | Resample to 64 tokens; insert gated cross-attn blocks into frozen LM | Stable adaptation (0-init gates); handles many interleaved images | More architectural surgery into LM stack than “prefix only” | You want interleaved prompting and strong few-shot behavior | https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf |

**Tutor note:** A common “why” is *compute + stability*: both Flamingo and BLIP-2 introduce a **fixed-size visual bottleneck** (64 resampled tokens; ~32 queries) to keep attention costs manageable and to avoid destabilizing a pretrained LM.

---

## Prerequisite Connections

- **Autoregressive language modeling / next-token prediction** — Needed to understand Flamingo’s objective \(p(y_\ell|y_{<\ell},x_{\le \ell})\) and why interleaving is trained as conditional LM. (Flamingo Eq. 1)
- **Attention (self-attention vs cross-attention)** — Needed to parse “queries attend to image features” (BLIP-2 Q-Former) and “LM tokens cross-attend to visual tokens” (Flamingo gated cross-attn). (Flamingo block formula; BLIP-2 architecture description)
- **Contrastive learning basics** — Needed to understand ITC and CLIP-style filtering/alignment (LAION filtering uses CLIP cosine similarity; BLIP-2 Stage-1 includes ITC).  
Sources: https://proceedings.mlr.press/v202/li23q/li23q.pdf , https://arxiv.org/abs/2210.08402 , https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

---

## Socratic Question Bank

1) **If you trained only contrastive alignment (ITC) on image–caption pairs, what capability might still be weak compared to interleaved next-token training?**  
Good answer: long-form conditional generation / multi-turn dialogue conditioned on visuals; contrastive aligns embeddings but doesn’t directly optimize next-token generation.

2) **In Flamingo, why define \(\phi(\ell)\) and mask cross-attention to only the most recent image? What breaks if you attend to all previous images?**  
Good answer: compute and scaling with many images; masking keeps per-token visual context bounded and matches “local” grounding in interleaved documents.

3) **What is the purpose of initializing Flamingo’s gating scalars to 0?**  
Good answer: initial behavior matches the frozen LM (stability), then gates learn to incorporate visual info gradually.

4) **BLIP-2 uses 32 query tokens; Flamingo uses 64 resampled tokens. What is the shared design principle?**  
Good answer: fixed-size bottleneck between vision and language to control compute and standardize interface.

5) **LAION-5B uses CLIP similarity thresholds (0.28/0.26). What kind of errors does this filtering reduce, and what might it still not fix?**  
Good answer: reduces mismatched/noisy captions; may not fully remove bias, harmful content (though metadata scores exist), or subtle miscaptioning.

6) **Why might unfreezing the LM during multimodal training hurt, according to Flamingo ablations?**  
Good answer: catastrophic forgetting; the LM loses pretrained language competence; ablation shows performance drop.

7) **Given Flamingo’s Eq. 1, what changes in the conditional distribution before vs after the first image appears in the sequence?**  
Good answer: before image, conditioning set \(x_{\le \ell}\) empty; after, includes image tokens, so next-token distribution can depend on visual context.

---

## Likely Student Questions

**Q: What is Flamingo’s exact training objective?**  
→ **A:** Flamingo trains an autoregressive conditional LM over text tokens with interleaved visuals:
\[
p(y\mid x)=\prod_{\ell=1}^{L} p(y_\ell \mid y_{<\ell}, x_{\le \ell})
\]
where \(x_{\le \ell}\) are images/videos occurring before token \(\ell\). Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

**Q: How does Flamingo handle multiple images without attention cost exploding?**  
→ **A:** It masks cross-attention so each token \(\ell\) attends only to the **most recent** image/video \(x_{\phi(\ell)}\), and each image/video is resampled to a fixed **64** visual tokens. Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

**Q: What is the gated cross-attention formula in Flamingo, and why are gates initialized to 0?**  
→ **A:** Inserted block:
1) \(y \leftarrow y + \tanh(\alpha_{\text{xattn}})\cdot \text{attn}(q=y, kv=x)\)  
2) \(y \leftarrow y + \tanh(\alpha_{\text{dense}})\cdot \text{ffw}(y)\)  
with \(\alpha\) initialized at **0** so the model initially behaves like the frozen LM (stability). Source: https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf

**Q: What are BLIP-2’s Stage-1 objectives (names + purpose)?**  
→ **A:** Stage-1 trains Q-Former with **ITC** (image-text contrastive alignment using in-batch negatives), **ITM** (image-text matching classifier with hard negatives), and **ITG** (image-grounded text generation with a multimodal causal mask). Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

**Q: What is the “query token bottleneck” in BLIP-2 (typical size)?**  
→ **A:** BLIP-2 uses learnable query tokens (typically **32 queries**, **768-d**) that cross-attend to frozen image features; outputs \(Z\in\mathbb{R}^{32\times 768}\). Source: https://proceedings.mlr.press/v202/li23q/li23q.pdf

**Q: How was LAION-5B filtered and what thresholds were used?**  
→ **A:** Compute CLIP cosine similarity \(s=\cos(\mathbf{e}_{img},\mathbf{e}_{txt})\) and keep if \(s\ge\tau\). Thresholds: English \(\tau=0.28\), non-English \(\tau=0.26\). LAION-5B totals **5.85B** pairs. Source: https://arxiv.org/abs/2210.08402

**Q: What evidence suggests interleaved webpage data matters for multimodal few-shot ability?**  
→ **A:** Flamingo ablation: removing M3W interleaved webpages drops overall 4-shot DEV score **70.7 → 53.4** (Flamingo-3B). Source: https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student needs a refresher on next-token prediction as the base objective that Flamingo extends to multimodal conditioning.
- [Let's build GPT: from scratch, in code, spelled out](https://youtube.com/watch?v=kCc8FmEb1nY) — Surface when: student asks “what does next-token training look like in code?” before mapping that idea to interleaved multimodal sequences.
- [Flamingo: a Visual Language Model for Few-Shot Learning (Paper Explained)](https://youtube.com/watch?v=EhlnhGBZZAo) — Surface when: student is confused about Perceiver Resampler, gated cross-attn insertion, or why interleaving enables few-shot prompting.

### Articles & Tutorials
- [Lilian Weng — The Transformer Family v2](https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/) — Surface when: student needs attention/transformer mechanics to understand cross-attention adapters and masking.
- [Sebastian Raschka — New LLM Pre-training and Post-training Paradigms](https://magazine.sebastianraschka.com/p/new-llm-pre-training-and-post-training) — Surface when: student asks how pretraining objectives relate to evaluation (loss/perplexity) and modern training pipelines.
- [Brown et al. (2020) — Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — Surface when: student asks where “few-shot prompting” comes from in language-only pretraining, before extending to multimodal few-shot (Flamingo).
- [Lilian Weng — Vision-Language Models](https://lilianweng.github.io/posts/2022-06-09-vlm/) — Surface when: student asks for a taxonomy of VLM fusion strategies (prefix, cross-attn, joint tokens) and where Flamingo/BLIP-2 fit.
- [Chip Huyen — Multimodality and Large Multimodal Models](https://huyenchip.com/2023/10/10/multimodal.html) — Surface when: student wants a practical overview connecting CLIP-style contrastive learning to Flamingo/BLIP-2 style generative multimodal models.

---

## Visual Aids

![CLIP's dual-encoder architecture maps images and text to a shared space. (Huyen Chip)](/api/wiki-images/vision-language-models/images/huyenchip-2023-10-10-multimodal-html_005.png)  
Show when: student asks “what does contrastive image–text pretraining look like architecturally?” before discussing ITC/LAION filtering.

![Flamingo engages in multi-turn visual conversations using few-shot prompting. (Alayrac et al.)](/api/wiki-images/vision-language-models/images/huyenchip-2023-10-10-multimodal-html_013.png)  
Show when: student asks “what does interleaved multimodal prompting enable?” or needs motivation for why Flamingo’s architecture exists.

---

## Key Sources

- [Flamingo: a Visual Language Model for Few-Shot Learning (PDF)](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf) — Authoritative formulas for interleaved objective, \(\phi(\ell)\) masking, Perceiver Resampler, and gated cross-attention block.
- [Flamingo paper (ar5iv HTML)](https://ar5iv.labs.arxiv.org/html/2204.14198) — Clear restatement of Eq. 1 and architectural rationale; useful for quick lookup during tutoring.
- [Flamingo NeurIPS 2022 Supplement](https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf) — Benchmark numbers + ablations (data mixture importance, gating, freezing).
- [BLIP-2: Bootstrapping Language-Image Pre-training (PMLR)](https://proceedings.mlr.press/v202/li23q/li23q.pdf) — Precise Stage-1/Stage-2 objectives, masking regimes, and query-token bottleneck details.
- [LAION-5B dataset paper](https://arxiv.org/abs/2210.08402) — Concrete dataset scale and CLIP-based filtering thresholds used to build a major image–text pretraining corpus.