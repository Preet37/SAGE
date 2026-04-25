---
title: "Multimodal Fundamentals"
subject: "Multimodal AI"
date: 2025-01-01
tags:
  - "subject/multimodal-ai"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/lilian-weng"
  - "educator/hugging-face"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Lilian Weng"
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

# Multimodal Fundamentals

## Video (best)
- **Andrej Karpathy / Stanford CS231n** — "Lecture on Multimodal Learning and Visual-Language Models"
- **Link:** [https://cs231n.stanford.edu/](https://cs231n.stanford.edu/)
- **Alternative: Yannic Kilcher** — Various CLIP/multimodal paper walkthroughs exist but no single canonical "multimodal fundamentals" explainer
- Why: No single YouTube video cleanly covers the full scope of multimodal fundamentals (modalities, fusion strategies, cross-attention, grounding) at an introductory level from the preferred educators. Karpathy's CS231n lectures touch on this but are fragmented across sessions.
- Level: N/A

> ⚠️ **Coverage gap noted here** — see Coverage Notes below.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Generalized Visual Language Models"
- **Link:** [https://lilianweng.github.io/posts/2022-06-09-vlm/](https://lilianweng.github.io/posts/2022-06-09-vlm/)
- Why: Weng's post is the most comprehensive written introduction to multimodal learning from a trusted author. It systematically covers how vision and language are fused, contrastive learning (CLIP), generative approaches, and grounding — directly mapping to the related concepts in this topic. Her structured writing style makes dense material accessible while remaining technically rigorous.
- Level: intermediate

---

## Deep dive
- **Lilian Weng** — "Large Multimodal Models"
- **Link:** [https://lilianweng.github.io/posts/2022-06-09-vlm/](https://lilianweng.github.io/posts/2022-06-09-vlm/)
- Why: This later post extends the VLM post into the era of instruction-tuned multimodal models (LLaVA-style), covering early vs. late fusion, cross-attention fusion architectures (Flamingo), and visual grounding in depth. Together with the VLM post above, it forms the most complete written technical reference available outside of survey papers.
- Level: advanced

---

## Original paper
- **Radford et al. (OpenAI), 2021** — "Learning Transferable Visual Models From Natural Language Supervision" (CLIP)
- **Link:** [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
- Why: CLIP is the most readable and pedagogically important seminal paper for multimodal fundamentals. It clearly motivates *why* we want to align modalities, introduces contrastive cross-modal training, and is written accessibly enough for learners new to the field. It anchors concepts like visual grounding and cross-modal fusion in a concrete, reproducible system. While not the first multimodal paper, it is the clearest entry point.
- Level: intermediate

---

## Code walkthrough
- **Hugging Face** — "Multimodal Models with Transformers" (official documentation + notebooks)
- url: https://huggingface.co/docs/transformers/index (navigate to vision-language models section)
- Why: Hugging Face's ecosystem provides the most hands-on, runnable code for multimodal fundamentals — covering CLIP, LLaVA, and vision-language pipelines with minimal setup. The notebooks demonstrate early fusion vs. late fusion concretely through real model APIs, making abstract architectural concepts tangible.
- Level: beginner–intermediate

> **More specific alternative:** The `openai/CLIP` GitHub repository includes a clean Jupyter notebook demonstrating zero-shot image classification and embedding alignment:
> url: https://github.com/openai/CLIP/blob/main/notebooks/Interacting_with_CLIP.ipynb

---

## Coverage notes
- **Strong:** Written explainers (Lilian Weng's posts are excellent), seminal papers (CLIP is ideal), and code (HuggingFace + CLIP repo)
- **Weak:** Fusion strategies (early vs. late vs. cross-attention) are rarely the *primary* focus of any single resource — they appear as subsections
- **Gap:** No high-quality YouTube video from preferred educators (3B1B, Karpathy, Kilcher, StatQuest, Serrano) cleanly covers *multimodal fundamentals as a unified topic* at beginner level. Kilcher has CLIP and Flamingo walkthroughs but they are paper-specific, not pedagogical overviews. A dedicated "What is Multimodal Learning?" explainer from a top educator does not appear to exist.
- **Gap:** GUI agents and computer use as multimodal applications are very new (2024–2025); no mature educational resource covers these in a fundamentals context yet.

---

---

## Additional Resources for Tutor Depth

> **8 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 LXMERT cross-attention + multimodal pretraining objectives
**Paper** · [source](https://aclanthology.org/D19-1514.pdf)

*Cross-modality encoder cross-attention equations + explicit pretraining objectives*

<details>
<summary>Key content</summary>

- **Inputs/embeddings (Sec. 2.1, Eq. 1):**
  - Words: \(\hat w_i=\text{WordEmbed}(w_i)\), \(\hat u_i=\text{IdxEmbed}(i)\), \(h_i=\text{LayerNorm}(\hat w_i+\hat u_i)\).
  - Objects: each object \(o_j\) has RoI feature \(f_j\in\mathbb{R}^{2048}\) and box coords \(p_j\).  
    \(\hat f_j=\text{LayerNorm}(W_F f_j+b_F)\), \(\hat p_j=\text{LayerNorm}(W_P p_j+b_P)\),  
    \(v_j=(\hat f_j+\hat p_j)/2\). (Eq. 1; position needed for masked object prediction.)
- **Attention definition (Sec. 2.2):** for query \(x\), contexts \(\{y_j\}\):  
  \(a_j=\text{score}(x,y_j)\), \(\alpha_j=\exp(a_j)/\sum_k\exp(a_k)\), output \(=\sum_j \alpha_j y_j\). Uses **multi-head attention** (Transformer).
- **Cross-modality encoder (Sec. 2.2):** per layer \(k\), bidirectional cross-attn then self-attn:
  - \(\hat h_i^k=\text{CrossAtt}_{L\to R}(h_i^{k-1},\{v_1^{k-1}\dots v_m^{k-1}\})\)  
    \(\hat v_j^k=\text{CrossAtt}_{R\to L}(v_j^{k-1},\{h_1^{k-1}\dots h_n^{k-1}\})\)
  - \(\tilde h_i^k=\text{SelfAtt}_{L\to L}(\hat h_i^k,\{\hat h_1^k\dots \hat h_n^k\})\),  
    \(\tilde v_j^k=\text{SelfAtt}_{R\to R}(\hat v_j^k,\{\hat v_1^k\dots \hat v_m^k\})\)  
  - Residual + LayerNorm after each sub-layer; [CLS] token’s final language vector is cross-modal output (Sec. 2.3).
- **Pretraining tasks (Sec. 3.1; mask prob 0.15):**
  1) Masked cross-modality LM (predict masked words using text + vision).  
  2) Masked object prediction: (a) RoI-feature regression (L2 on \(f_j\)); (b) detected-label classification (cross-entropy on Faster R-CNN labels).  
  3) Cross-modality matching: replace sentence w.p. 0.5; classify match vs mismatch.  
  4) Image QA: predict answer (9500-way answer table) when image-question matched.
- **Data/compute defaults (Sec. 3.2–3.3):** 9.18M image-sentence pairs, 180K images; ~100M words, 6.5M objects. Keep **36 objects/image** (avoid padding). Layers: \(N_L=9\), \(N_X=5\), \(N_R=5\); hidden size 768. Pretrain 20 epochs (~670K steps), batch 256, Adam, peak LR \(1e{-4}\), linear decay; QA loss only last 10 epochs; equal-weight sum of losses. Fine-tune 4 epochs, batch 32, LR \(1e{-5}\) or \(5e{-5}\).
- **Key results (Table 2):** LXMERT test: VQA Acc 72.5 (Binary 88.2 / Number 54.2 / Other 63.1); GQA Acc 60.3 (Binary 77.8 / Open 45.0); NLVR2 Acc 76.2, Consistency 42.1 (prior SotA 53.5 / 12.0).
- **Ablations (Tables 4–5):** adding QA pretrain improves NLVR2 72.4→74.9; vision tasks matter: no-vision-tasks gives NLVR2 50.9 vs feat+label 74.9.

</details>

### 📄 UGround + SeeAct-V (Vision-only GUI grounding & eval)
**Paper** · [source](https://arxiv.org/html/2410.05243v2)

*End-to-end GUI grounding + offline/online evaluation protocols and error analysis (procedures/metrics)*

<details>
<summary>Key content</summary>

- **Core setup (SeeAct-V, §1.1):** Modular 2-stage agent: (1) planner MLLM generates a textual plan + **element description (referring expression, RE)**; (2) separate **visual grounding model** outputs **pixel coordinates** on the screenshot for action. Eliminates HTML/a11y-tree/SoM candidate lists.
- **Training data pipeline (Web-Hybrid, §1.2):** Synthesize (screenshot, RE, target) triplets from webpages using HTML↔rendered bbox correspondences; target is **element center-point coordinate**. RE types:  
  1) **Visual** (text/icon/type/color/shape), 2) **Positional** (absolute/relative/contextual), 3) **Functional** (“Go to My Cart”), plus composites.  
  Hybrid generation: rules + LLMs (LLaVA-NeXT-13B to draft REs from element crop+attrs; Llama-3-8B-Instruct to compress).
- **Dataset scale (Table 1):** Web-Hybrid **9M elements / 773K screenshots**; Web-Direct **408K/408K**; total compiled **10M elements / 1.3M screenshots** (web+Android).
- **Model I/O ( §1.3):** Prompt: *“In the screenshot, what are the pixel element coordinates corresponding to {Description}?”* Output as **natural-language numeric coordinate** e.g., **“(1344, 1344)”** (no normalization).
- **Resolution/architecture defaults (§1.3):** LLaVA-NeXT backbone; AnyRes-style slicing; **CLIP@224px** vision encoder; max supported resolution **(landscape) 1344×896** and **(portrait) 896×1344**; **Vicuna-1.5-7B-16k** with **16K context**; **omit low-res fusion module** (224px global too uninformative for GUIs).
- **Evaluation protocols & metrics (§2):**
  - **Grounding:** ScreenSpot; **standard** (human functional REs) vs **agent setting** (planner generates diverse REs). Report accuracy vs bbox target.
  - **Offline agents (§2.2):** Multimodal-Mind2Web (cached pages): **element accuracy**. AndroidControl (cached): **step-wise accuracy** (action+element+args all correct). OmniACT: **action score** (sequence accuracy penalizing argument errors).
  - **Online agents (§2.3):** Mind2Web-Live: **micro completion rate** (key nodes) + **task success rate**. AndroidWorld: **task success rate** (final device state).
- **Key empirical results:** On ScreenSpot, UGround improves **~+20% absolute (standard)** and **~+29% (agent setting)** average over prior models; strong **desktop** performance despite **no desktop training** (§2.1). Scaling: with **~10K screenshots (~100K elements)**, UGround surpasses SeeClick trained on **~4M elements / ~200K screenshots** (§2.5).
- **Error analysis (§2.4):** Failures mostly **planning errors** (wrong/vague/hallucinated element descriptions). Grounding errors notable on mobile/desktop **long-tail icon semantics**.

</details>

### 📄 ViLBERT two-stream co-attention + pretraining tasks
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2019/file/c74d97b01eae257e44aa9d5bade97baf-Paper.pdf)

*Two-stream co-attentional Transformer layer (cross-modal key/value exchange) + masked multimodal modeling & image-text alignment pretraining*

<details>
<summary>Key content</summary>

- **Two-stream architecture (Sec. 2.2, Fig. 1):** separate visual stream over region features \(v_1,\dots,v_T\) and linguistic stream over tokens \(w_0,\dots,w_T\); interact via **Co-TRM** layers.
- **Co-attentional Transformer (Sec. 2.2, Fig. 2b):** like standard multi-head attention but **swap key/value across modalities**:  
  - Visual update uses \(Q_v\) from \(H_V\) and \(K_w,V_w\) from \(H_W\) → “vision attends to language”.  
  - Linguistic update uses \(Q_w\) from \(H_W\) and \(K_v,V_v\) from \(H_V\) → “language attends to vision”.  
  Residual + FFN as in Transformer encoder blocks.
- **Image representation (Sec. 2.2):** Faster R-CNN regions (10–36 boxes, confidence-thresholded). Add **5-d spatial encoding** \((x_1,y_1,x_2,y_2,\text{area frac})\) projected and summed with region feature. Special **IMG** token = mean-pooled region features + full-image spatial encoding.
- **Pretraining tasks (Sec. 2.2, Fig. 3):**
  - **Masked multimodal modeling:** mask ~15% of words + regions. Text masking as BERT; region features zeroed 90% / unchanged 10%. Predict **region semantic class distribution**; loss = **KL divergence** to detector’s class distribution. Word loss = cross-entropy over vocab.
  - **Multimodal alignment:** input \(\{\text{IMG}, v_{1:T}, \text{CLS}, w_{1:T}, \text{SEP}\}\). Use holistic reps \(h_{\text{IMG}}, h_{\text{CLS}}\); combine by **element-wise product** \(h_{\text{IMG}}\odot h_{\text{CLS}}\) → linear layer → aligned/not (binary CE). Negatives by random image or caption replacement.
- **Defaults/hyperparams (Sec. 3.1):** Conceptual Captions ~3.1M pairs used; batch 512 on 8 TitanX; 10 epochs; Adam LR \(1\mathrm{e}{-4}\) with warmup + linear decay; task losses equally weighted. Linguistic init: **BERT-BASE** (12 layers, 12 heads, hidden 768). Visual stream: hidden 1024, 8 heads.
- **Key transfer results (Table 1):** ViLBERT (pretrained) vs ViLBERT† (no pretrain):  
  - **VQA test-dev:** 70.55 vs 68.93  
  - **VCR Q→AR:** 54.04 vs 49.48  
  - **RefCOCO+ testA/testB:** 78.52/62.61 vs 75.97/58.44  
  - **Image retrieval R@1:** 58.20 vs 45.50  
  - **Zero-shot retrieval R@1:** 31.86 (no fine-tune)
- **Depth ablation (Table 2):** retrieval improves with depth; e.g., ZS R@1: 26.14 (2-layer) → 31.86 (6-layer) → 32.80 (8-layer).

</details>

### 📊 Flexible VLP via detachable parallel fusion (FOD)
**Benchmark** · [source](https://aclanthology.org/2023.findings-acl.316.pdf)

*Ablation comparisons of fusion strategies (concatenation/cascading/parallel) + benchmark results on retrieval & VL understanding*

<details>
<summary>Key content</summary>

- **Architecture (Section 3, Eq. 4–5):** Dual-encoder (ViT image encoder + BERT-like text encoder) with **detachable cross-modal fusion** placed on text side.  
  - **Fusion-free text layer (Eq. 4):**  
    \(T_l^s=\text{MSA}(T_{l-1},T_{l-1},T_{l-1});\ \hat T_l=\text{LN}(T_l^s+T_{l-1});\ T_l=\text{LN}(\text{MLP}(\hat T_l)+\hat T_l)\). Output \(T=T_L\).
  - **Fusion-based (parallel) text layer (Eq. 5):**  
    \(M_l^s=\text{MSA}(M_{l-1},M_{l-1},M_{l-1});\ M_l^c=\text{MCA}(M_{l-1},V,V);\ \tilde M_l=\tfrac12(M_l^s+M_l^c)\) then LN+MLP as above. Output \(M=M_L\). **Parallel** makes fusion easy to remove at inference.
- **Training objectives (Section 4):**
  - **ITC contrastive (Eq. 6–8):** similarities \(s_{i2t}, s_{t2i}\) via projected, L2-normalized CLS embeddings; softmax with temperature \(\sigma\); loss \(L_{itc}=\tfrac12[H(y_{i2t},p_{i2t})+H(y_{t2i},p_{t2i})]\). Uses MoCo-style queues of size \(K\).
  - **ITM (Eq. 9):** binary match classifier on \(M_{cls}\); hard negatives sampled by similarity.
  - **Cross-modal knowledge transfer CKT (Eq. 11):** force unimodal CLS to approximate multimodal CLS:  
    \(L_{I2M}=\text{MSE}(f_v(V_{cls}), f_t(M_{cls}))\), \(L_{T2M}=\text{MSE}(f_t(T_{cls}), f_t(M_{cls}))\).
- **Fusion ablation (Table 4, 50K pretrain steps):** Parallel best.  
  - MSCOCO TR@1/IR@1: Concatenation 72.5/54.2; Cascading 73.0/54.5; **Parallel 73.5/55.4**.  
  - Flickr30k TR@1/IR@1: 92.6/80.5; 91.7/81.2; **93.1/81.6**.
- **CKT ablation (Table 5):** I2M helps text-retrieval; T2M helps image-retrieval; both best overall. With both: MSCOCO avg retrieval 87.2 (vs 86.3 baseline), VQAv2 test-dev 77.57, NLVR2 test-P 83.37.
- **Placing fusions on both sides hurts (Fig. 4):** FOD-both drops vs FOD on VQA/NLVR and Flickr30k TR/IR (authors attribute to harder self-supervision on vision side vs MLM on text).
- **Key downstream results:**  
  - **VQAv2 test-std 78.91; NLVR2 test-P 85.29** (Table 3; pretrain 3M).  
  - Retrieval fine-tuned (Table 1, Dual): MSCOCO TR R@1 **77.3**, IR R@1 **58.9**; Flickr30k TR R@1 **94.6**, IR R@1 **83.5**.
- **Defaults (Section 5.1.2):** Pretrain on 3.4M images (“3M”); ViT-Base init BEiT; text init uncased BERT-base; image res 256², patch 16²; AdamW wd 1e-2; lr 1e-4 warmup 1k; 300K steps on 32×A100, batch 2048.

</details>

### 📖 Images & Vision API (schema + image handling + costs)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/images-vision?api-mode=chat)

*Exact request/response schema variants, image input handling (URL/base64/file_id), detail levels, resizing + token cost rules, constraints/limits*

<details>
<summary>Key content</summary>

- **Endpoints & use cases**
  - **Responses API:** analyze images as input and/or generate images as output (via tools).
  - **Chat Completions API:** analyze images → generate text/audio.
  - **Images API:** generate images (optionally with image inputs).
- **Image input methods (Responses/Chat):** provide **(1)** fully-qualified **URL**, **(2)** **Base64 data URL**, or **(3)** **file_id** (Files API). Multiple images allowed; **images count as tokens**.
- **Responses API schema (vision input):** `input=[{"role":"user","content":[{"type":"input_text","text":...},{"type":"input_image","image_url":...,"detail":...}]}]`
- **Image requirements/limits**
  - Types: **PNG, JPEG/JPG, WEBP, non-animated GIF**
  - Limits: **≤512 MB total payload/request**, **≤1500 images/request**
  - Other: **no watermarks/logos**, **no NSFW**, must be **human-legible**; **CAPTCHAs blocked**
- **Detail parameter (default = auto):** `"low" | "high" | "original"(gpt-5.4+) | "auto"`
  - **low:** 512×512 proxy; faster/cheaper
  - **original:** for dense/spatial/computer-use; recommended for click-accuracy on **gpt-5.4+**
- **Patch-based tokenization (Eq.1–4)**
  - **Eq.1:** `original_patch_count = ceil(w/32)*ceil(h/32)`
  - If over **patch_budget**, shrink:  
    **Eq.2:** `shrink_factor = sqrt((32^2*patch_budget)/(w*h))`  
    **Eq.3:** `adjusted_shrink_factor = shrink_factor * min(floor(w*shrink/32)/(w*shrink/32), floor(h*shrink/32)/(h*shrink/32))`
  - **Eq.4:** `resized_patch_count = ceil(w’/32)*ceil(h’/32)`; billed tokens = `resized_patch_count * multiplier`
  - Multipliers: **gpt-5.4-mini 1.62; gpt-5.4-nano 2.46; gpt-5-mini 1.62; gpt-5-nano 2.46; gpt-4.1-mini(2025-04-14) 1.62; gpt-4.1-nano(2025-04-14) 2.46; o4-mini 1.72**
  - Patch budgets/resizing: **high** up to **1536 patches or 2048px max dim** (many minis); **gpt-5.4+ original** up to **10,000 patches or 6000px max dim**
- **Tile-based tokenization (GPT-4o/4.1/4o-mini/o1/o3/computer-use-preview)**
  - For `"high"`: scale to fit **2048×2048**, then shortest side **768px**, count **512px tiles**, add base tokens.
  - Base/tile tokens: **gpt-5: 70/140; 4o/4.1/4.5: 85/170; 4o-mini: 2833/5667; o1/o1-pro/o3: 75/150; computer-use-preview: 65/129**
  - **GPT Image 1:** like tile-based but shortest side **512px**; low fidelity base **65** + tile **129**; high fidelity adds **+4160** (square) or **+6240** (portrait/landscape-ish).

</details>

### 📖 Vision inputs & image token costs (Node/Responses API)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/vision?lang=node)

*Copy-pastable patterns + concrete limits/cost formulas for image+text requests and image sizing/tokenization*

<details>
<summary>Key content</summary>

- **Send image + text (Responses API pattern):** `input` is an array of messages; each message `content` can mix:
  - `{type:"input_text", text:"..."}` and `{type:"input_image", image_url:"https://..."}`.
- **Image input methods:** (1) fully-qualified URL, (2) Base64 data URL, (3) `file_id` (via Files API). Multiple images allowed; **images count as tokens**.
- **Image requirements:** types **PNG/JPEG/WEBP/non-animated GIF**; **≤512 MB total payload/request**; **≤1500 images/request**; **no watermarks/logos**, **no NSFW**, must be human-legible.
- **Detail parameter (default = `auto`):** `low | high | original | auto`.
  - `low`: model sees **512×512** version (fast/cheap).
  - `high`: standard high-fidelity.
  - `original`: for **large/dense/spatial/computer-use** images; recommended for click-accuracy on **gpt-5.4+**.
- **Patch-based tokenization (32×32 patches) (Eq.1–4):**
  - **Eq.1** `original_patch_count = ceil(w/32) * ceil(h/32)`
  - If over patch budget, shrink: **Eq.2** `shrink_factor = sqrt((32^2 * patch_budget)/(w*h))`
  - **Eq.3** `adjusted_shrink_factor = shrink_factor * min(floor(w*shrink/32)/(w*shrink/32), floor(h*shrink/32)/(h*shrink/32))`
  - **Eq.4** `resized_patch_count = ceil(w’/32) * ceil(h’/32)`; then **tokens = resized_patch_count * multiplier** (capped by budget).
  - Multipliers: **1.62** (gpt-5.4-mini, gpt-5-mini, gpt-4.1-mini snapshot), **2.46** (…-nano), **1.72** (o4-mini).
  - Example (budget 1536): **1024×1024 → 1024 patches**; **1800×2400 → resized 1056×1408 → 1452 patches**.
- **Tile-based tokenization (GPT-4o/4.1/4o-mini/o1/o3/computer-use-preview):**
  - `detail:"low"` = fixed base tokens (model-specific).
  - `detail:"high"`: scale to fit **2048×2048**, then shortest side **768px**, count **512px tiles**; **total = base + tiles*tile_tokens**.
  - Table rows: **4o/4.1/4.5 base 85, tile 170**; **o1/o1-pro/o3 base 75, tile 150**; **computer-use-preview base 65, tile 129**; **gpt-5 base 70, tile 140**; **4o-mini base 2833, tile 5667**.
- **GPT Image 1 input cost:** like tile-based but shortest side **512px**; low fidelity **base 65, tile 129**; high fidelity adds **+4160** (square) or **+6240** (portrait/landscape-ish).

</details>

### 🔍 Multimodal Alignment & Fusion — core equations + fusion taxonomy
**Explainer** · [source](https://arxiv.org/html/2411.17040v1)

*Comparative discussion of fusion configurations (early/late/hybrid; encoder-decoder; attention-based) and where performance gains come from; includes key alignment/attention equations and a few concrete improvement numbers.*

<details>
<summary>Key content</summary>

- **Alignment vs. Fusion (Section 3):**
  - *Alignment* = establish semantic relationships across modalities (often via shared/common space); *Fusion* = combine aligned information into unified predictions. Many methods struggle to fuse well **without** alignment first.
- **Explicit alignment via CCA (Section 4.1, Eq. 1):**
  - CCA projects two modalities into a common space with linear transforms to **maximize correlation**.
  - Variables (as described):  
    - \(X, Y\): data matrices from two modalities/spaces  
    - \(w_x, w_y\): linear transformation (canonical) vectors  
    - \(\rho\): correlation coefficient between projected variables  
  - Goal: choose \(w_x, w_y\) to maximize \(\rho(X w_x,\; Y w_y)\).  
  - Limitation: linear only → motivates KCCA/DCCA for nonlinear alignment.
- **Attention-based fusion (Section 5.4, Eq. 2):**
  - Scaled dot-product attention: \(\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V\)  
    - \(Q\)=queries, \(K\)=keys, \(V\)=values, \(d_k\)=key dimension (scaling).
  - Rationale: dynamically weight modality features; helps with multimodal noise/uncertainty but increases compute and data needs.
- **Fusion taxonomy & rationale (Section 5, 5.1):**
  - **Early fusion** (feature-level) captures inter-modal interactions earlier; **late fusion** combines decisions and is robust to missing modalities; **hybrid** mixes both.
  - Encoder–decoder fusion forms: **data-level** (concat raw inputs → shared encoder), **feature-level** (extract per-modality features → combine → decoder; stated as “often most effective”), **model-level** (combine model outputs).
- **Concrete empirical numbers (Section 5.1.1):**
  - A YOLO-style **raw camera+LiDAR data-level fusion** reported **~5% improvement** in vehicle detection vs **decision-level (late) fusion**.
  - A quality-control/predictive-maintenance **model-level fusion** approach reported **30% reduction in prediction variance** and **45% accuracy increase** vs traditional methods.

</details>

### 🔍 Vision-only GUI grounding (SeeAct‑V + UGround)
**Explainer** · [source](https://arxiv.org/html/2410.05243v3)

*End-to-end GUI agent grounding pipeline: screenshot-only perception, referring-expression→coordinate grounding, data synthesis, evaluation, error analysis*

<details>
<summary>Key content</summary>

- **Problem & rationale (Intro):** Prior GUI agents rely on HTML/a11y trees → **noise/incompleteness** and **latency/cost**. HTML can take **up to 10× more tokens** than visual encoding (Zheng et al., 2024). Visual renderings are “information-complete” for users.
- **Framework (Sec. 2.1): SeeAct‑V**
  - Observation: **screenshots only**.
  - Planning: MLLM generates a **textual plan / element description**.
  - Grounding: separate **visual grounding model outputs pixel coordinates** directly (no candidate list from HTML/SoM).
- **Training data (Sec. 2.2): triplets** *(screenshot, referring expression, target coordinate)* with **target = element center point (x, y)**.
  - Webpages used for synthesis (HTML ↔ rendered pixels ↔ element bounding boxes).
  - **Referring expression (RE) types:**  
    1) **Visual** (text/icon/type/color/shape), 2) **Positional** (absolute/relative/contextual like “input labeled Birthday”), 3) **Functional** (“Go to My Cart”); composites common.
  - **Hybrid synthesis pipeline:**  
    (i) **Primary descriptors** from HTML attrs (inner-text, alt, aria-label) + **LLaVA‑NeXT‑13B** to generate diverse REs; **Llama‑3‑8B‑Instruct** to shorten.  
    (ii) **Positional/context rules** from element geometry + neighbors + DOM structure.
  - **Scale:** Web-Hybrid **9M elements / 773K screenshots**; plus Web-Direct **408K** (GPT‑4o) + Android datasets.
- **Model design (Sec. 2.3):** LLaVA‑NeXT backbone; prompt: *“what are the pixel element coordinates corresponding to {Description}?”* Output as text **“(x, y)”** (unnormalized). AnyRes-style slicing; **CLIP@224** encoder; max supported resolution **≈2016×1344 (landscape)** / **≈1344×2016 (portrait)**; **Vicuna‑1.5‑7B‑16k** (16K context). Remove low-res fusion module (336px too small for GUI global context).
- **Empirical results (Sec. 3.1):** On ScreenSpot, UGround improves over prior models by **~+20% absolute (standard)** and **~+29% (agent setting)** on average; strong on **icons/widgets**; notable **desktop performance despite no desktop training**.
- **Error analysis (Sec. 3.4):** Failures mostly **planning errors** (wrong/vague/hallucinated element descriptions). Grounding errors often from **long-tail, idiosyncratic icon semantics** (esp. mobile/desktop).

</details>

---

## Related Topics

- [[topics/vision-language-models|Vision Language Models]]
- [[topics/contrastive-learning|Contrastive Learning]]
- [[topics/cnns|CNNs]]
- [[topics/tokenization|Tokenization]]
- [[topics/audio-speech-models|Audio & Speech Models]]
- [[topics/document-understanding|Document Understanding]]
