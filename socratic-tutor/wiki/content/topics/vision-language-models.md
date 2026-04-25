---
title: "Vision Language Models"
subject: "Multimodal AI"
date: 2025-01-01
tags:
  - "subject/multimodal-ai"
  - "level/intermediate"
  - "level/advanced"
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

# Vision Language Models

## Video (best)
- **Yannic Kilcher** — "Flamingo: a Visual Language Model for Few-Shot Learning (Paper Explained)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=EhlnhGBZZAo)
- Why: Yannic Kilcher's paper walkthroughs are uniquely strong for VLMs because he dissects the architectural decisions (cross-attention fusion, perceiver resampler) with clear diagrams and critical commentary. Flamingo is the most pedagogically central paper for understanding modern VLM design patterns, making this the best entry point for the fusion architecture concepts that underpin BLIP-2, LLaVA, and GPT-4V.
- Level: intermediate/advanced

> ⚠️ **Coverage note on video:** No single video comprehensively covers the full VLM landscape (Flamingo → BLIP-2 → LLaVA → GPT-4V progression). The Kilcher video is the best single anchor, but instructors should supplement.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Large Multimodal Models"
- **Link:** [https://lilianweng.github.io/posts/2022-06-09-vlm/](https://lilianweng.github.io/posts/2022-06-09-vlm/)
- Why: Lilian Weng's posts are the gold standard for systematic, well-cited ML surveys. This post traces VLMs from contrastive pretraining (CLIP) through generative fusion architectures, covering visual tokens, patch embeddings, and Q-Former with consistent notation. Her writing bridges intuition and technical rigor better than any other single written resource for this topic.
- Level: intermediate

---

## Deep dive
- **Chip Huyen** — "Multimodal and Large Language Models" (CS329A course notes / blog)
- **Link:** [https://huyenchip.com/2023/10/10/multimodal.html](https://huyenchip.com/2023/10/10/multimodal.html)
- Why: Chip Huyen's multimodal deep dive is the most comprehensive *practical* technical reference covering the full pipeline: how visual tokens are constructed, how patch embeddings are projected into language model space, the tradeoffs between different fusion architectures (early vs. late fusion, cross-attention vs. prefix), and dynamic resolution strategies. It connects architecture to deployment concerns in a way that pure academic surveys do not.
- Level: advanced

---

## Original paper
- **Alayrac et al. (DeepMind)** — "Flamingo: a Visual Language Model for Few-Shot Learning"
- **Link:** [https://arxiv.org/abs/2204.14198](https://arxiv.org/abs/2204.14198)
- Why: Flamingo is the clearest seminal paper for the generative VLM paradigm. It introduces the Perceiver Resampler, cross-attention fusion layers interleaved with a frozen LLM, and visual token compression — concepts that directly influenced BLIP-2's Q-Former, LLaVA's projection head, and Gemini's architecture. The paper is unusually well-written with strong ablations, making it the most readable entry point into the design space.
- Level: advanced

---

## Code walkthrough
- **Hugging Face** — "BLIP-2 with Transformers — practical walkthrough"
- **Link:** [https://huggingface.co/docs/transformers/model_doc/blip-2](https://huggingface.co/docs/transformers/model_doc/blip-2)
- Why: The HuggingFace BLIP-2 documentation and associated notebooks provide the most hands-on, runnable implementation of the core VLM concepts: Q-Former architecture, visual token extraction via patch embeddings, and conditional text generation. BLIP-2 is architecturally richer than LLaVA for teaching purposes (it makes the vision-language bridge explicit via Q-Former) while remaining accessible. The HF ecosystem means learners can run inference and fine-tuning without custom infrastructure.
- Level: intermediate

---

## Coverage notes
- **Strong:** Flamingo architecture, Q-Former / BLIP-2, fusion architecture concepts, patch embeddings, visual tokens — all well covered across the resources above.
- **Weak:** Dynamic resolution (as used in LLaVA-HD, InternVL, Gemini) has no dedicated high-quality explainer; it appears only as a subsection in survey posts.
- **Weak:** GPT-4V and Gemini are closed models — no authoritative architectural walkthrough exists; only the technical reports (which are incomplete).
- **Gap:** No excellent standalone video exists that surveys the *full* VLM landscape from CLIP → Flamingo → BLIP-2 → LLaVA → GPT-4V in a single coherent narrative. This is a genuine pedagogical gap in the ecosystem as of early 2024.
- **Gap:** No distill.pub-style interactive explainer exists for visual token compression (Perceiver / Q-Former) — a concept that benefits greatly from visualization.

---

---

## Additional Resources for Tutor Depth

> **10 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 BLIP-2 two-stage objectives + Q-Former querying
**Paper** · [source](https://proceedings.mlr.press/v202/li23q/li23q.pdf)

*Stage-1/Stage-2 BLIP-2 training objectives for Q-Former + query-token cross-attention bottleneck*

<details>
<summary>Key content</summary>

- **Architecture (Sec. 3.1, Fig. 2):** Q-Former bridges a **frozen image encoder** and **frozen LLM** using **learnable query tokens**. Queries use **self-attention** among themselves and **cross-attention to frozen image features** (cross-attn layers inserted **every other transformer block**). Queries can also interact with text tokens via shared self-attn layers; interaction controlled by **attention masks** per objective.
- **Bottleneck sizing:** typically **32 queries**, each **768-d**; output query reps **Z ∈ R^{32×768}**. Example frozen ViT features: **257×1024 (ViT-L/14)**. Q-Former initialized from **BERT-base**; cross-attn layers random init; Q-Former ~**188M params** (queries count as parameters).
- **Stage-1 (Sec. 3.2): joint loss = ITC + ITM + ITG**
  - **ITC (Image-Text Contrastive):** align image rep from queries **Z** with text rep **t** (the **[CLS]** embedding). Similarity: compute sim(q_i, t) for each query output, take **max_i** as image-text similarity; uses **unimodal mask** (queries/text cannot attend each other); uses **in-batch negatives**.
  - **ITG (Image-grounded Text Generation):** LM-style generation conditioned on queries; **multimodal causal mask**: queries attend queries only; each text token attends **all queries + previous text tokens**; replace [CLS] with **[DEC]** token.
  - **ITM (Image-Text Matching):** binary matched/unmatched with **bidirectional mask** (full query-text attention). For each query output, compute 2-class logit; **average logits across queries** for match score; uses **hard negative mining**.
- **Stage-2 (Sec. 3.3, Fig. 3): vision→language generative bootstrapping**
  - Project queries via **FC layer** to LLM embedding dim; **prepend projected queries** as **soft visual prompts** to LLM input.
  - **Decoder-only LLM (e.g., OPT):** train with **language modeling loss** to generate text conditioned on visual prompts.
  - **Encoder–decoder LLM (e.g., FlanT5):** **prefix LM loss**: split text into **prefix** (encoder input with visual prompts) and **suffix** (decoder target).
- **Key results (Tables 1–2):**
  - Zero-shot **VQAv2 test-dev:** **BLIP-2 65.0** vs **Flamingo80B 56.3** (BLIP-2 uses **54× fewer trainable params**).
  - Example configs: **BLIP-2 ViT-g + FlanT5-XXL:** **VQAv2 test-dev 65.0**, **OK-VQA 45.9**, **GQA 44.7** (Table 2).
- **Pretraining defaults (Sec. 3.4):** Stage-1 **250k steps**, Stage-2 **80k steps**; image size **224×224**; optimizer **AdamW**, β1=0.9, β2=0.98, weight decay 0.05; cosine LR, peak **1e-4**, warmup **2k** steps; Stage-2 min LR **5e-5**.

</details>

### 📄 Flamingo architecture—Perceiver Resampler + gated cross-attn for interleaved vision/text
**Paper** · [source](https://ar5iv.labs.arxiv.org/html/2204.14198)

*Copyable architectural definitions (Perceiver Resampler; gated cross-attention insertion; masking for interleaved inputs)*

<details>
<summary>Key content</summary>

- **Autoregressive objective (Eq. 1):** Flamingo models next-token likelihood conditioned on prior text and preceding visuals in an interleaved sequence:  
  \[
  p(y_t \mid y_{<t}, x_{\le t})
  \]
  where \(y_t\) is the \(t\)-th language token, \(y_{<t}\) preceding tokens, and \(x_{\le t}\) the set of images/videos preceding token \(t\) in the interleaved prompt (Section 2).
- **Perceiver Resampler (Section 2.1):** Takes variable-length vision features (flattened spatial grid for images; spatio-temporal grid for videos with learned temporal embeddings; frames sampled at **1 FPS**) and outputs a **fixed 64 visual tokens** per image/video to reduce cross-attention cost.
- **Conditioning a frozen LM (Section 2.2):** Insert **gated cross-attention dense blocks** between frozen pretrained LM layers; train only inserted modules + resampler (vision encoder and LM blocks frozen).  
  **Rationale:** preserve pretrained knowledge; avoid catastrophic forgetting (Section 3.3 row viii).
- **0-init gating for stability (Section 2.2, ablation 3.3 row iii):** output of each new layer is multiplied by a learnable scalar gate (tanh/ReZero-style), **initialized to 0**, so initial behavior matches the original LM; improves stability/performance.
- **Per-image/video attention masking (Section 2.3):** At each text token, cross-attend only to the **most recent** image’s visual tokens (not all previous images); enables generalization to **any number** of visuals. Trained with up to **5 images/sequence**, evaluated benefiting up to **32 shots**.
- **Training loss (Eq. 2):** weighted sum of per-dataset expected NLLs over a mixture of datasets (interleaved webpages + image-text pairs + video-text pairs); gradient accumulation across datasets beats round-robin (Section 2.4, 3.3 row ii).
- **Key few-shot results (Table 1, Flamingo-80B, 32-shot):** OKVQA **57.8**, VQAv2 **67.6**, COCO CIDEr **113.8**, MSVDQA **52.3**, VATEX CIDEr **65.1**, VizWiz **49.8**, TextVQA **37.9**, HatefulMemes **70.0**.
- **Ablations (Table 3, Flamingo-3B, 4-shot):** removing **M3W** drops COCO CIDEr **86.5→54.1**; removing tanh gating drops overall score (**70.7→66.5**); Perceiver Resampler beats MLP/Transformer resamplers.

</details>

### 📄 Flamingo — Perceiver Resampler & Gated Cross-Attention (XATTN-DENSE)
**Paper** · [source](https://storage.googleapis.com/deepmind-media/DeepMind.com/Blog/tackling-multiple-tasks-with-a-single-visual-language-model/flamingo.pdf)

*Exact definitions of the Perceiver Resampler and the Flamingo gated cross-attention block (gating + insertion in LM stack)*

<details>
<summary>Key content</summary>

- **Interleaved conditional LM objective (Eq. 1, Section 3):**  
  \[
  p(y\mid x)=\prod_{\ell=1}^{L} p\big(y_\ell \mid y_{<\ell}, x_{\le \ell}\big)
  \]
  where \(y_\ell\) is the \(\ell\)-th text token, \(y_{<\ell}\) preceding tokens, and \(x_{\le \ell}=\{x_i\mid i\le \phi(\ell)\}\) are images/videos preceding token \(\ell\) in the interleaved sequence.
- **Per-image/video attention indexing (Section 3.1.3):** define \(\phi:[1,L]\to[0,N]\) = index of the **last** image/video before token position \(\ell\) (0 if none). Cross-attn is masked so token \(\ell\) attends only to visual tokens of image/video \(x_{\phi(\ell)}\) (Fig. 6). Authors report this works better than attending to all previous images directly.
- **Perceiver Resampler algorithm (Fig. 4, Section 3.1.1):** input visual features \(x_f\in\mathbb{R}^{[T,S,d]}\) (time, space, dim), learned latents \(x\in\mathbb{R}^{[R,d]}\). Add learned **time** embeddings, flatten \([T,S,d]\to[T\!\cdot\!S,d]\). For each layer \(i\):  
  \(x \leftarrow x + \text{attn}_i(q=x,\ kv=\text{concat}([x_f,x]))\); then \(x \leftarrow x + \text{ffw}_i(x)\). Output is fixed \(R\) visual tokens (in practice **64**).
- **Gated XATTN-DENSE block (Fig. 5, Section 3.1.2):** inserted **between frozen pretrained LM layers**. For language features \(y\), visual tokens \(x\):  
  1) \(y \leftarrow y + \tanh(\alpha_{\text{xattn}})\cdot \text{attn}(q=y, kv=x)\)  
  2) \(y \leftarrow y + \tanh(\alpha_{\text{dense}})\cdot \text{ffw}(y)\)  
  with learnable scalars \(\alpha_{\text{xattn}},\alpha_{\text{dense}}\) **initialized at 0** so the model initially matches the frozen LM; improves stability/performance.
- **Defaults/data pipeline snippets:** M3W training subsequence \(L=256\) tokens, up to \(N=5\) images; images resized \(320\times320\). Video frames sampled at **1 FPS**; paired-video uses \(T=8\) frames. Special token **<EOC>** added; literal “`<image>`” tag inserted in text.

</details>

### 📄 Joint Adaptive Representations (efficient image–language fusion)
**Paper** · [source](https://arxiv.org/pdf/2305.19924.pdf)

*Quantitative compute/accuracy tradeoffs from reducing/reshaping visual tokens; efficient fusion vs concatenation/cross-attn/Perceiver/co-tokenization.*

<details>
<summary>Key content</summary>

- **Problem/rationale (Sec. 2, Fig. 2–3):**
  - Concatenation increases sequence length by **H·W** visual tokens → attention cost grows quadratically; scales poorly with image/model size.
  - Standard cross-attention “squeezes” many visual tokens (e.g., **14×14=196** at 224²) into few text tokens (e.g., **~10** in VQA) → information bottleneck.
  - Goal: **reduce tokens first**, then **iteratively fuse** with low FLOPs; expensive tokenization over full inputs done **once** (unlike Perceiver/co-tokenization).

- **Core equations (Sec. 2):**
  - **Eq. 1 (visual projection):** \(P(X_{im}) = W_1 X_{im}\), where \(X_{im}\in\mathbb{R}^{H\times W\times C}\), \(P(X_{im})\in\mathbb{R}^{H\!*\!W\times D}\).
  - **Eq. 2 (latent token resampling, DETR-style learnable tokens):** learn \(X_N\in\mathbb{R}^{N\times D}\); \(f_N = W_2\,\Phi(X_N, P(X_{im}))\). Similarly produce \(t_N\) from \(X_{text}\in\mathbb{R}^{L\times D}\). \(N\) is **not tied** to text length.
  - **Eq. 3 (gated fusion):**
    - \(P_{cr}(t_N,f_N)=Ln(t_N)+\tanh(\alpha)\Phi(Ln(t_N),Ln(f_N))\)
    - \(F(t_N,f_N)=P_{cr}+\tanh(\beta)MLP(P_{cr})\)
  - **Eq. 4 (iterative refinement):** replace \(t_N\) with \(F_i+t_N\); compute \(F_{i+1}\) via Eq. 3 then transformer layer \(T(\cdot)\).

- **Key empirical results (Tables 1–4):**
  - **Concat baseline vs Ours (Table 3):** **58.4→38.9 GFLOPs** (~**33%** less; **1.5× fewer FLOPs**) and **GQA 78.9→79.1**, **SNLI-VE 77.4→77.9**. Memory **15GB→9GB** (~40% reduction).
  - **Vs Perceiver/CoTokenization (Table 2, base):** Perceiver **40.3 GF** (GQA **78.2**), CoToken **43.8 GF** (GQA **78.5**), **Ours 38.9 GF** (GQA **79.1**, SNLI-VE **77.9**).
  - **Ablations (Table 4):**
    - Iterations: **1/2/4/8** → **34.2/35.5/38.9/42.5 GF**, GQA **78.3/78.8/79.1/79.2** (diminishing returns).
    - Tokens \(N\): **16/32/64/128** → **18.5/28.4/38.9/72.9 GF**, GQA **76.5/78.3/79.1/79.2**.
    - Resampling: **Latent** better than **Spatial** (GQA **79.1 vs 78.9**, **38.9 vs 42.5 GF**).
    - Iterative combination: **Weighted** best (GQA **79.1**) vs **Residual 78.7**, **None 78.1** at same **38.9 GF**.
    - Fusion module layers: **32 layers** best among shown (**38.9 GF**, GQA **79.1**) vs **16 layers 30.5 GF, 78.3**; very deep (**822.4 GF**) hurts (**76.7**).

</details>

### 📄 MobileVLM (VLM training + efficient projector; contrasts Q-Former/MLP)
**Paper** · [source](https://arxiv.org/pdf/2312.16886.pdf)

*Concrete equations for VLM token projection + 2-step VLM training (freeze/train projector then tune), plus empirical token-count/speed comparisons and Q-Former vs MLP rationale.*

<details>
<summary>Key content</summary>

- **Architecture (Sec. 3.1):** Vision encoder → visual embeddings \(Z\in\mathbb{R}^{N\times D_v}\) (N patches, \(D_v\) hidden). Projector maps to LLM embedding space to form **image tokens** + **text tokens** for autoregressive decoding.
- **Eq. (1) (Sec. 3.1):** Projector converts vision features into word-embedding space: \(H_v = \Phi(Z)\) (projector \(\Phi\)); output dimension matches LLM embedding size \(D\). (Text tokens \(H_t\in\mathbb{R}^{T\times D}\); image tokens \(H_v\in\mathbb{R}^{M\times D}\).)
- **Eq. (2) (Sec. 3.1):** Autoregressive response conditioned on multimodal tokens: \(p(y\,|\,H_v,H_t)=\prod_{i=1}^{L} p(y_i\,|\,y_{<i},H_v,H_t)\).
- **Projector rationale (Sec. 3.4):**
  - **Q-Former:** controls #visual tokens via queries but “loses spatial positional information,” “slow convergence,” and is inefficient on edge.
  - **MLP projector:** retains spatial info but injects many (often background) tokens → slows inference.
  - **LDP (Lightweight Downsample Projector):** uses depth-wise conv (PEG-like) + stride-2 downsampling to keep spatial info while reducing tokens; <20M params; reduces tokens by **75%**.
- **Token-count result (Sec. 5.1):** LDP reduces visual tokens **576 → 144** (−75%) with **equivalent or sometimes better** benchmark performance.
- **Resolution vs token reduction (Sec. 5.3, Table 11):** With 144 tokens, **LDP beats reducing input resolution (RIR)**:  
  - LDP: GQA **56.1**, SQA **54.7**, VQA **41.5**, POPE **84.5**, MME **1196.2**, MMB **53.2**  
  - RIR: GQA **53.9**, SQA **53.1**, VQA **37.1**, POPE **81.5**, MME **1072.5**, MMB **46.7**
- **VLM training pipeline (Sec. 4.1):** 2-step: (1) **freeze vision encoder + LLM**, train projector only (pretrain on **CC-595K**, 1 epoch, batch **256**); (2) fine-tune **projector + LLM** (instruction tuning on **LLaVA-Instruct-158K**, 1 epoch, batch **128**). AdamW, cosine LR, warmup ratio **3%**, no weight decay.
- **Latency formula (Eq. 4, Sec. 4.5):** Total inference time decomposed into load + prompt processing + generation terms using measured tokens/s; key point: fewer visual tokens reduces prompt-processing time.

</details>

### 📄 Perceiver-VL efficiency via iterative latent attention
**Paper** · [source](https://openaccess.thecvf.com/content/WACV2023/papers/Tang_Perceiver-VL_Efficient_Vision-and-Language_Modeling_With_Iterative_Latent_Attention_WACV_2023_paper.pdf)

*Perceiver-style iterative latent cross-attention as a visual token bottleneck; concrete FLOPs/latency vs accuracy tradeoffs + LayerDrop/mixed-stream retrieval.*

<details>
<summary>Key content</summary>

- **Core idea (Sec. 3.2):** Map input array length **M** (concat visual+text embeddings) to latent array length **N** via **iterative cross-attention**, then self-attend only over latents.
- **Complexity formulas (Sec. 3.2):**
  - Perceiver-VL encoder with **k** blocks, each: 1 cross-attn + **l** latent self-attns  
    **O(kMN + klN²)**  
  - Standard transformer encoder with same # self-attns over inputs: **O(klM²)**  
  - Example input length: video 8 frames, 224², patch 16 ⇒ **M=(224/16)²·8=1568**, typical **N=128**.
- **Embeddings (Sec. 3.1):** input embedding = modality + temporal (video only) + positional + patch/token embedding; treat image as 1-frame video.
- **LayerDrop on cross-attn (Sec. 3.3, Table 3):** drop cross-attn layers during training with prob **pLD** (not first cross-attn). Enables inference-time depth reduction.
  - With LD during finetuning: inference time **72.0→58.0 ms** (−19.4%) with **R@1 27.1→26.3** on MSRVTT retrieval.
- **Mixed-stream retrieval (Sec. 3.5, Fig. 6):** accuracy/latency tradeoff on MSRVTT val:  
  - single-stream **R@1 27.2** (slowest), multi-stream **26.0** (fastest), **mixed-stream 26.8** (near single-stream, faster).
- **Key efficiency/accuracy comparisons (Tables 1–2):**
  - MSRVTT retrieval: **Perceiver-VL N=128 mixed**: **R@1 32.6**, **43.2 GFLOPs**, **72.0 ms** vs Frozen-in-Time: **R@1 31.0**, **89.0 GFLOPs**, **260 ms**.
  - VQAv2: **Perceiver-VL N=128**: **70.91 acc**, **30.5 GFLOPs**, **18 ms** vs ViLT-B/32: **71.26**, **55.9 GFLOPs**, **32 ms**.
- **Defaults (Sec. 4.1):** hidden 768, 12 heads; **k=3**, **l=3** (3 cross-attn, 12 self-attn); decoder: 1 cross-attn; image/frame size **384**, patch **32**; **pLD=0.5**.
- **Pretraining (Sec. 4.3):** CC (3M) + WebVid (2.5M); Adam lr **1e-5**, wd **0.001**, **200k steps**, batch **4096** (grad accum), 4×RTX2080Ti ~14 days.

</details>

### 📊 Flamingo supplement — few-shot benchmarks & ablations
**Benchmark** · [source](https://proceedings.neurips.cc/paper_files/paper/2022/file/960a172bc7fbf0177ccccbb411a7d800-Supplemental-Conference.pdf)

*Supplemental benchmark tables + ablations for Flamingo (few-shot across tasks/scales; design choices like Perceiver Resampler, gated cross-attn, data mixture)*

<details>
<summary>Key content</summary>

- **Autoregressive objective (Eq. 1):**  
  \(p(y|x)=\prod_{\ell=1}^{L} p(y_\ell \mid y_{<\ell}, x_{\le \ell})\)  
  where \(y_\ell\)=\(\ell\)-th text token; \(x_{\le \ell}\)=images/videos occurring before token \(\ell\) in the interleaved sequence.
- **Training loss (Eq. 2):** weighted multi-dataset NLL  
  \(\sum_{m=1}^{M}\lambda_m \, \mathbb{E}_{(x,y)\sim \mathcal{D}_m}\left[-\sum_{\ell=1}^{L}\log p(y_\ell|y_{<\ell},x_{\le \ell})\right]\).  
  Uses **gradient accumulation across datasets** (better than round-robin; Table 3 row (ii)).
- **Architecture defaults (Sec. 2):**
  - Frozen **NFNet-F6** vision encoder; frames at **1 FPS** for video.
  - **Perceiver Resampler** outputs **64 visual tokens** per image/video (Sec. 2.1).
  - Frozen pretrained LM (Chinchilla 1.4B/7B/70B → **Flamingo-3B/9B/80B**); insert **GATED XATTN-DENSE** blocks with **tanh gating** scalars \(\alpha\) init **0** (Fig. 4) for stability.
  - **Per-image causal masking**: each text token cross-attends only to the **most recent** image’s tokens (Sec. 2.3); enables >5 images at inference though trained with ≤5.
- **Data mixture (Sec. 2.4):** M3W interleaved webpages (**~43M** pages; sample **L=256** tokens, keep **N=5** images), plus ALIGN **1.8B** image-text, LTIP **312M** image-text, VTP **27M** video-text.
- **Key few-shot results (Table 1, 32 shots, Flamingo-80B):** OKVQA **57.8**, VQAv2 **67.6**, COCO **113.8** (CIDEr), VATEX **65.1** (CIDEr), VizWiz **49.8**, TextVQA **55.6**, HatefulMemes **37.9**, VisDial **86.8**, YouCook2 **45.3**, MSRVTTQA **75.4**.
- **Ablations (Table 3, Flamingo-3B, 4-shot DEV):**
  - Remove **M3W**: Overall **70.7 → 53.4** (largest drop).
  - No tanh gating: **70.7 → 66.5**.
  - Cross-attn frequency: every layer best; **every 4th** gives **70.7 → 68.8** with faster step time (**1.74s → 1.02s**).
  - Resampler: **Perceiver** best vs MLP/Transformer (Overall **70.7** vs **66.6/66.7**).
  - Vision encoder: NFNet-F6 beats CLIP ViT-L/14 (Overall **70.7 vs 64.9**).
  - Unfreezing LM hurts (catastrophic forgetting): fine-tune pretrained LM **70.7 → 62.7**; train from scratch **→ 57.8**.

</details>

### 📖 OpenAI Images API (Generate/Edit/Variations) — schema & params
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/images)

*Exact parameter names, request/response schema, and documented defaults/constraints for image endpoints*

<details>
<summary>Key content</summary>

- **Endpoints (Images):**
  - **Generate an Image**: `POST /v1/images/generations`
  - **Edit an Image**: `POST /v1/images/edits`
  - **Create Variation**: `POST /v1/images/variations`
  - Also documented: **streaming events** for image generation/edit (see “Image generation streaming events”, “Image edit streaming events” in the Images section).
- **Core request fields (by operation):**
  - **Generate**: `model`, `prompt`, optional controls such as `n`, `size`, `response_format`, `user` (exact availability/allowed values are specified per endpoint in the reference).
  - **Edit**: multipart form with `image` (input image), optional `mask`, plus `prompt`, `model`, and other optional controls (e.g., `n`, `size`, `response_format`, `user`) as listed in the endpoint schema.
  - **Variation**: multipart form with `image` (input image), plus `model` and optional controls (`n`, `size`, `response_format`, `user`) per schema.
- **Response schema (common pattern):**
  - Returns an object containing a `data` array of generated items; each item includes image output payload (commonly `url` or base64 content depending on `response_format`, per endpoint docs).
- **Procedure/workflow (implementation):**
  1. Choose operation (generate/edit/variation) and **model**.
  2. Provide required inputs (`prompt` for generate/edit; `image` for edit/variation; optional `mask` for edit).
  3. Set output controls (`n`, `size`, `response_format`) as needed.
  4. Parse `data[]` in the response; handle streaming events if using streaming.

</details>

### 📖 OpenAI Vision Inputs (Schemas, Detail Levels, Token Cost)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/images-vision)

*Official request/response patterns for sending images to vision-capable models (URL/base64/file_id), `detail` behavior, and image tokenization constraints.*

<details>
<summary>Key content</summary>

- **Send images to models (3 methods):**
  - **URL**: provide fully qualified image URL.
  - **Base64 data URL**: `data:image/jpeg;base64,{BASE64}`.
  - **File ID**: upload via Files API with `purpose:"vision"`, then reference `file_id`.
- **Chat Completions schema (image input):** message `content` array with parts:
  - `{ "type":"text", "text":"..." }`
  - `{ "type":"image_url", "image_url": { "url":"...", "detail":"auto|low|high|original" } }`
- **Responses API schema (image input):** `input` array of items; user `content` parts:
  - `{ "type":"input_text", "text":"..." }`
  - `{ "type":"input_image", "image_url":"..." , "detail":"..." }` or `{ "type":"input_image", "file_id":"..." }`
- **Image input requirements:**
  - Types: PNG, JPEG/JPG, WEBP, **non-animated** GIF
  - Limits: **512 MB total payload/request**, **1500 images/request**
  - Other: no watermarks/logos, no NSFW, must be human-legible
- **`detail` parameter (default = `auto`):**
  - `low`: model gets **512×512** low-res (fast/cheap)
  - `high`: standard high-fidelity understanding
  - `original`: for large/dense/spatially sensitive/computer-use images; available on **gpt-5.4+**
- **Model resizing/patch budgets (32×32 patch-based families):**
  - `gpt-5.4`+: `high` ≤ **2,500 patches** or **2048px max dim**; `original` ≤ **10,000 patches** or **6000px max dim**
  - `gpt-5-mini/nano`, `o4-mini`, `gpt-4.1-mini/nano (2025-04-14)` : `high` ≤ **1,536 patches** or **2048px max dim**
- **Patch token cost formula (Section: Patch-based tokenization):**
  - **Eq.1** `original_patch_count = ceil(width/32) * ceil(height/32)`
  - If over budget, scale down:  
    **Eq.2** `shrink_factor = sqrt((32^2 * patch_budget)/(width*height))`  
    **Eq.3** `adjusted_shrink_factor = shrink_factor * min( floor(width*shrink_factor/32)/(width*shrink_factor/32), floor(height*shrink_factor/32)/(height*shrink_factor/32) )`
  - **Eq.4** `resized_patch_count = ceil(resized_width/32) * ceil(resized_height/32)` (capped by budget)
  - **Eq.5 billed_tokens = resized_patch_count * multiplier**
    - Multipliers: `gpt-5.4-mini` **1.62**, `gpt-5.4-nano` **2.46**, `gpt-5-mini` **1.62**, `gpt-5-nano` **2.46**, `gpt-4.1-mini*` **1.62**, `gpt-4.1-nano*` **2.46**, `o4-mini` **1.72**
- **Worked examples (1,536 patch budget):**
  - 1024×1024 → patch count **1024** (no resize)
  - 1800×2400 → resized to **1056×1408**, patch count **1452**

</details>

### 📖 Vision fine-tuning — dataset format + constraints
**Reference Doc** · [source](https://platform.openai.com/docs/guides/vision-fine-tuning)

*End-to-end procedure for vision fine-tuning: dataset format expectations, training workflow, and operational constraints*

<details>
<summary>Key content</summary>

- **What it is / model:** Vision fine-tuning = **supervised fine-tuning (SFT)** with **image inputs** to improve image understanding; best for **image classification** and **fixing instruction-following failures on complex prompts**. Use with **`gpt-4o-2024-08-06`**.
- **Training data format (JSONL):** Each line is a JSON object with `"messages"` (chat-style). Image inputs appear in a user message as a **content array** containing objects like:  
  - `{ "type": "image_url", "image_url": { "url": "<http(s) URL or data URL base64>" } }`  
  - Images may be **HTTP URLs** or **data URLs (Base64)**.  
  - **Constraint:** You **cannot** include images in messages with the **`assistant`** role (images are inputs only).
- **Image data requirements (hard limits):**
  - Max **50,000** examples that contain images (text-only examples not counted).
  - Max **10 images per example**.
  - Max **10 MB per image**.
  - Formats: **JPEG, PNG, WEBP** only.
  - Color mode: **RGB or RGBA**.
- **Content moderation filtering (pre-training scan):** Images containing **people, faces, children, CAPTCHAs** are **excluded** (and may add latency during validation).
  - Common skip reasons + fixes: inaccessible URL → make public; too large → meet size limits; invalid format → meet format rules; contains restricted entities → remove image.
- **Cost/quality control via `detail` parameter (per image):**
  - `detail: "low"` → image resized to **512×512** and represented by **85 tokens** regardless of original size (reduces training cost).
  - `detail` can be **`low` / `high` / `auto`**; affects fidelity + token count + cost.
- **Post-training safety gate:** Completed fine-tuned models are evaluated across **13 safety categories**; each has a pass threshold; failing categories can **block deployment**. Debug via fine-tuning **events** endpoint; look for event type **`moderation_checks`**.

</details>

---

## Related Topics

- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/contrastive-learning|Contrastive Learning]]
- [[topics/transformer-architecture|Transformer Architecture]]
- [[topics/video-understanding|Video Understanding]]
- [[topics/document-understanding|Document Understanding]]
