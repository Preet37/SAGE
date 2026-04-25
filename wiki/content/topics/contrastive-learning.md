---
title: "Contrastive Learning"
subject: "Multimodal AI"
date: 2025-01-01
tags:
  - "subject/multimodal-ai"
  - "level/intermediate"
  - "level/advanced"
  - "educator/yannic-kilcher"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Yannic Kilcher"
  - "Lilian Weng"
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

# Contrastive Learning

## Video (best)
- **Yannic Kilcher** — "CLIP: Connecting Text and Images (Paper Explained)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=OZF1t_Hieq8)
- Why: Kilcher walks through the original CLIP paper with exceptional clarity, explaining the dual-encoder architecture, InfoNCE loss, and zero-shot classification in a single cohesive narrative. His paper-explanation style is ideal for learners who want to understand *why* design choices were made, not just *what* they are.
- Level: intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "Contrastive Representation Learning"
- **Link:** [https://lilianweng.github.io/posts/2021-05-31-contrastive/](https://lilianweng.github.io/posts/2021-05-31-contrastive/)
- Why: Weng's post is the canonical written reference for contrastive learning — it covers the theoretical motivation, loss functions (InfoNCE, NT-Xent, triplet loss), and major methods (SimCLR, MoCo, CLIP) with clean math and diagrams. It bridges self-supervised vision methods and multimodal contrastive learning in one place, making it ideal for the full conceptual arc of this topic.
- Level: intermediate/advanced

## Deep dive
- **Author** — OpenAI CLIP model card + Hugging Face CLIP docs combined with Sebastian Raschka's "Understanding Contrastive Learning"
- url: https://sebastianraschka.com/blog/2022/understanding-contrastive-learning.html [NOT VERIFIED]
- Why: Raschka's treatment is unusually rigorous about the mathematical underpinnings of InfoNCE loss and why contrastive objectives work as representation learners. He connects theory to implementation more carefully than most blog posts, making it the best resource for learners who want to go from intuition to derivation to code.
- Level: advanced

## Original paper
- **Radford et al. (OpenAI)** — "Learning Transferable Visual Models From Natural Language Supervision" (CLIP)
- **Link:** [https://arxiv.org/abs/2103.00020](https://arxiv.org/abs/2103.00020)
- Why: This is the seminal paper that crystallized contrastive learning for multimodal settings and introduced the dual-encoder + InfoNCE framework at scale. It is unusually readable for an OpenAI paper — the motivation, method, and zero-shot evaluation protocol are explained with enough detail to be self-contained. SigLIP and OpenCLIP are direct descendants, so understanding this paper unlocks the whole family.
- Level: intermediate/advanced

## Code walkthrough
- **Hugging Face / @merveenoyan** — CLIP fine-tuning notebook on Hugging Face
- url: https://huggingface.co/blog/fine_tune_clip_fashion [NOT VERIFIED]
- Why: This notebook demonstrates the full contrastive training loop end-to-end — projection layers, InfoNCE loss computation, dual-encoder forward pass, and evaluation — using real data and the `transformers` library. It is more pedagogically complete than most standalone scripts because it explains each component inline, and it maps directly to the OpenCLIP/SigLIP ecosystem learners will encounter in practice.
- Level: intermediate

## Coverage notes
- **Strong:** The CLIP paper itself is exceptionally clear; Lilian Weng's blog post is one of the best technical explainers in the entire ML blogosphere for this topic; Hugging Face ecosystem has strong practical coverage.
- **Weak:** SigLIP-specific content (sigmoid loss vs. softmax InfoNCE) has very limited dedicated tutorial coverage. Projection layer design choices are rarely explained in depth outside of paper appendices.
- **Gap:** No excellent standalone beginner-friendly video exists that covers *contrastive learning as a general framework* (not just CLIP specifically) with visual intuition — something in the 3Blue1Brown or StatQuest style. Kilcher's video is the best available but assumes paper-reading familiarity. OpenCLIP and SigLIP also lack dedicated video explainers as of early 2025.

---

## Additional Resources for Tutor Depth

> **6 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 CLIP objective (symmetric InfoNCE over batch)
**Paper** · [source](https://arxiv.org/abs/2103.00020)

*Primary-source CLIP objective: symmetric cross-entropy over full batch similarity matrix; temperature/logit_scale parameterization; encoder→linear projection→L2-normalized shared embedding space.*

<details>
<summary>Key content</summary>

- **Training task (Section 2; Fig. 1):** Given a batch of **N (image, text) pairs**, predict which caption matches which image among **N×N** possible pairings (N positives on diagonal, **N²−N** negatives off-diagonal).
- **Encoders + projections (Fig. 3 pseudocode):**  
  - Image features: \(I_f = f_\text{img}(I)\in\mathbb{R}^{N\times d_i}\)  
  - Text features: \(T_f = f_\text{text}(T)\in\mathbb{R}^{N\times d_t}\)  
  - Linear projections to shared embedding dim \(d_e\): \(W_i\in\mathbb{R}^{d_i\times d_e}, W_t\in\mathbb{R}^{d_t\times d_e}\)  
  - Normalize: \(I_e=\mathrm{L2Norm}(I_f W_i)\), \(T_e=\mathrm{L2Norm}(T_f W_t)\)
- **Similarity logits + temperature (Fig. 3):**  
  \[
  \text{logits} = I_e T_e^\top \cdot \exp(t)
  \]
  where \(t\) is a **learned log-temperature** (so scale = \(\exp(t)\)); cosine similarity due to L2 norm.
- **Loss = symmetric cross-entropy (Fig. 3):** with labels \(y_i=i\) for \(i\in\{0,\dots,N-1\}\):  
  \[
  \mathcal{L}_\text{img}=\mathrm{CE}(\text{logits}, y;\text{axis}=0),\quad
  \mathcal{L}_\text{text}=\mathrm{CE}(\text{logits}, y;\text{axis}=1),\quad
  \mathcal{L}=\tfrac{1}{2}(\mathcal{L}_\text{img}+\mathcal{L}_\text{text})
  \]
- **Design rationale:** remove **non-linear projection head**; use **only linear projection** (simplifies training; overfitting “not a major concern”). Objective is multi-class **N-pair loss** (Sohn, 2016).
- **Defaults/params:** temperature initialized to equivalent of **0.07** (Wu et al., 2018) and **clipped** so logit scaling ≤ **100**.
- **Empirical anchors:** Best CLIP zero-shot **ImageNet top-1 76.2%**, **top-5 95%**; matches original ResNet-50 without using ImageNet labels. Dataset scale: **400M** image-text pairs.

</details>

### 📄 CLIP zero-shot pipeline + mutual-knowledge (MI) analysis
**Paper** · [source](https://arxiv.org/html/2410.13016v1)

*Mechanistic breakdown of CLIP zero-shot classification + concept-based interpretation via mutual information dynamics across 13 CLIP models.*

<details>
<summary>Key content</summary>

- **CLIP zero-shot classification (Section 3):** Treat classification as retrieval. Encode fixed prompts for each class (e.g., “an image of a {class}”) with text encoder; encode image with vision encoder; pick class with highest similarity in shared embedding space. Encoders each have **separate projection layers** fed by **[CLS]**.
- **Descriptor pool (Section 3):** Use an LLM to generate class-agnostic textual descriptors (“textual concepts”). For ImageNet: **4,229** unique descriptors after deduplication.
- **Visual concept extraction (Section 3.1):**
  - Extract patch features \(F=\{f_i\}_{i=1}^{N}\). Build affinity matrix \(A\) from patchwise feature correlations.
  - Spectral graph cut: eigendecompose \(A\); use **Fiedler eigenvector** (2nd largest non-zero). Sign gives binary mask; positive group = **prominent patches**. Interpolate to pixels with **CRF**.
  - Derive **visual concepts** by **PCA or K-means** on prominent patches across images.
- **Map visual concepts → text (Section 3.1, Eq. 2):** Encode each concept region using **visual prompt engineering** (red circle / blur outside region). Compute similarities to all descriptors; then enforce diversity via **Optimal Transport** (Sinkhorn-Knopp) to get a permutation-like assignment. OT increases descriptor diversity entropy: **1.70 → 2.33 (PCA)** and **1.70 → 2.34 (K-means)**.
- **Text-side concepts (Section 3.2):** For predicted class text embedding, retrieve **top-\(k\)** nearest descriptors in language embedding space.
- **Mutual information (Section 3, Eq. 1):**
  \[
  I(V;L)=H(V)+H(L)-H(V,L)
  \]
  where \(V\)=discrete textual concepts from vision side, \(L\)=discrete textual concepts near predicted class; compute via contingency table after mapping concepts to integers.
- **MI dynamics/AUC (Section 3.3):** Sort vision concepts by importance; ablate sequentially; recompute MI curve; **AUC** summarizes “shared knowledge strength” (slower MI drop ⇒ higher AUC).
- **Key empirical results (Section 4):**
  - Adding discovered descriptors improves ImageNet zero-shot accuracy vs base prompts: **RN50 59.54→61.85 (+2.31)**; **RN50x16 68.47→72.22 (+3.75)**; **ViT-B/16 67.93→70.28 (+2.35)**; **ViT-L/14@336 75.49→77.64 (+2.15)**.
  - Across 13 models, **AUC correlates with top-1 accuracy within an architecture**; ViTs show stronger shared knowledge than CNNs. Example (Table 3): **ViT-B/16-dfn** top-1 **76.24%**, MI **8.19**, AUC **4.62** (PCA).

</details>

### 📄 LiT/CLIP Zero-shot Robustness via Self-Consistency + WordNet Hierarchy
**Paper** · [source](https://arxiv.org/pdf/2212.01758.pdf)

*Concrete zero-shot ImageNet(+shift) numbers for CLIP/LiT; post-hoc confidence via self-consistency; hierarchy-based label augmentation procedure.*

<details>
<summary>Key content</summary>

- **Zero-shot logit (cosine sim):**  
  \(z_m=f_{\text{image}}(x)\), \(z_c=f_{\text{text}}(c)\).  
  \(\text{logit}(x,c)=\cos(z_m,z_c)\); predict \(\hat c(x,\emptyset)=\arg\max_{c\in C}\text{logit}(x,c)\). (Sec. 4.1)
- **Prompt self-consistency confidence (Eq. 1):** for prompt set \(T\),  
  \(S_T(x)=\frac{1}{|T|}\sum_{t\in T}\mathbf{1}\{\hat c(x,t)=\hat c(x,\emptyset)\}\), where \(\hat c(x,t)=\arg\max_{c\in C}\text{logit}(x,t(c))\).
- **Image-perturbation self-consistency (Eq. 2):** for transforms \(B\),  
  \(S_B(x)=\frac{1}{|B|}\sum_{b\in B}\mathbf{1}\{\hat c(x,b)=\hat c(x,\emptyset)\}\), where \(\hat c(x,b)=\arg\max_{c}\text{logit}(b(x),c)\). Best single perturbation: **left-right flip**.
- **Low-confidence set construction:** union \(O=O_T\cup O_B\). For ImageNet, split CLIP’s **80 prompts** into \(T_1\) (first 40), \(T_2\) (last 40), \(T_3\) (all 80), \(T_4=\emptyset\); mark low-confidence if top-1 predictions disagree across sets.
- **Hierarchy label augmentation (Sec. 4.2, Alg. 2):** rerank only **top-5** predicted classes using WordNet parent \(p(c)\) and children \(c_1..c_r\). Combined score (Eq. 3):  
  \(\text{logit}(x,c)=\max\{\text{logit}(x,[c;p(c)]), \text{logit}(x,[c_1;p(c)]),...,\text{logit}(x,[c_r;p(c)])\}\). Natural-language template used: “**{child} which is a kind of {parent}**”. Prune overly abstract/rare WordNet terms; rarity estimated via **variance of text-embedding norms across prompts**.
- **Empirical results (Table 1):**  
  - **CLIP ViT-B/16** ImageNet top-1: low-conf **21.58→38.71%** (+17.13); full **64.18→67.78%** (+3.60).  
  - **LiT ViT-B/32** ImageNet top-1: low-conf **31.18→37.25%**; full **68.26→69.41%**.  
  - Shifted sets (CLIP full): ImageNet-v2 **58.06→61.07**, IN-R **56.88→59.46**, IN-A **26.12→29.23**, IN-Sketch **44.71→47.28**.
- **Confidence estimator quality (Fig. 3):** AUROC vs max-logit baseline: **CLIP 0.84 vs 0.67**, **LiT 0.81 vs 0.70**; better selective prediction at all abstention rates.

</details>

### 📄 SigLIP pairwise sigmoid loss (vs CLIP/InfoNCE softmax)
**Paper** · [source](https://arxiv.org/abs/2303.15343)

*Defines SigLIP’s pairwise sigmoid loss for image–text dual-encoder training; explains removal of batch-wise softmax normalization, efficient distributed “chunked” implementation, and scaling/stability/training-recipe implications.*

<details>
<summary>Key content</summary>

- **Setup (dual encoder):** image encoder \(f(\cdot)\), text encoder \(g(\cdot)\); embeddings \(z_{\text{img}}, z_{\text{txt}}\). Similarity/logit matrix (Alg. 1):  
  \[
  \text{logits} = z_{\text{img}} z_{\text{txt}}^\top \cdot t + b
  \]
  where **temperature** \(t=\exp(t')\) is learnable; **bias** \(b\) is learnable.
- **Pairwise sigmoid loss (Section 3.2, Alg. 1):** define label matrix  
  \[
  \text{labels} = 2I_n - \mathbf{1}_{n\times n}
  \]
  (diagonal \(+1\) for matched pairs, off-diagonal \(-1\) for mismatches). Loss:
  \[
  \mathcal{L} = -\frac{1}{n}\sum_{i,j}\log \sigma(\text{labels}_{ij}\cdot \text{logits}_{ij})
  \]
  Key property: **no global softmax normalization across the batch**; symmetric; single pass; typically **less memory** than softmax/InfoNCE.
- **Initialization rationale (Section 3.2):** many negatives dominate early; add bias \(b\) to avoid huge initial correction. Initialize \(t'\approx \log 10\) (paper also notes “10” in some text) and \(b=-10\).
- **Efficient distributed “chunked” loss (Section 3.3, Fig. 1):** avoid materializing \(|B|\times|B|\) similarities; compute local positives + subset of negatives; **permute embeddings across devices** to stream negatives; sum per-device losses.
- **Empirical batch-size findings (Fig. 2):**
  - Sigmoid **outperforms softmax when batch size < 16k**; gap closes at larger BS.
  - Benefits of scaling BS **saturate ~32k**; pushing to **1,000,000** BS shows diminishing returns; very large BS (e.g., **307k**) can hurt.
- **Training stability at large batch (Section 4.7, Fig. 5):** gradient spikes increase with BS; setting optimizer **\(\beta_2=0.95\)** (vs 0.999) stabilizes.
- **Recipe detail (Section 4.2):** WebLI English; ViT-B/16 image + B-sized text transformer; images 224×224; SentencePiece vocab 32k; keep **max 16 text tokens**.
- **Fine-tuning recipe (Fig. 4):** when using a **pre-trained vision backbone**, **disable weight decay on pre-trained encoder weights**; apply WD only to randomly initialized parts → more stable and better transfer.
- **Concrete results (Table 1 / text):**
  - **SigLiT** (LiT + sigmoid; frozen public ViT-AugReg): **79.7%** ImageNet zero-shot in **1 day on 4 TPUv4** (B/8); **84.5%** with g/14 in **2 days on 4 TPUv4**.
  - **SigLIP** from-scratch: **73.4%** ImageNet zero-shot at **32k batch**, **32 TPUv4**, **5 days**; fine-tune setup reaches **~71%** 0-shot at **16k batch** (reported in Fig. 4 text).

</details>

### 📊 SigLIP/SigLiT — Pairwise Sigmoid Loss vs Softmax (InfoNCE) + Batch-Size Effects
**Benchmark** · [source](https://arxiv.org/pdf/2303.15343v3.pdf)

*Tables/ablations with ImageNet zero-shot accuracy vs batch size; shows sigmoid loss benefits (esp. small BS) and saturation ~32k; includes 84.5% claim (large LiT + SigLIP/SigLiT).*

<details>
<summary>Key content</summary>

- **Softmax (InfoNCE) loss (Sec. 3.1):** for batch \(B\), normalized embeddings \(x_i=\frac{f(I_i)}{\|f(I_i)\|_2}\), \(y_i=\frac{g(T_i)}{\|g(T_i)\|_2}\), temperature \(t=\exp(t')\):  
  \[
  \mathcal{L}_{softmax}=-\frac{1}{2|B|}\sum_{i=1}^{|B|}\Big(\log\frac{e^{t x_i\cdot y_i}}{\sum_j e^{t x_i\cdot y_j}}+\log\frac{e^{t x_i\cdot y_i}}{\sum_j e^{t x_j\cdot y_i}}\Big)
  \]
- **Pairwise sigmoid loss (Sec. 3.2, Alg. 1):** logits \(s_{ij}=t\,x_i\!\cdot\! y_j + b\); labels \(z_{ij}=+1\) if matched else \(-1\):  
  \[
  \mathcal{L}_{sigmoid}=-\frac{1}{|B|}\sum_i\sum_j \log \sigma(z_{ij}\, s_{ij})
  \]
  **Defaults:** initialize \(t'=\log 10\) (so \(t=10\)), **bias** \(b=-10\) to prevent early over-correction from huge neg:pos imbalance.
- **Efficient “chunked” distributed implementation (Sec. 3.3, Fig. 1):** avoid all-gathers; compute loss on local \(b\times b\) blocks while permuting text (or image) embeddings across devices; reduces memory from \(|B|^2\) to \(b^2\).
- **Key ImageNet zero-shot results (Table 1):**
  - **SigLiT** (frozen public ViT-g/14 vision; LiT dataset): **BS 20k**, **4 TPUv4**, **2 days** → **84.5%**
  - SigLiT (frozen public B/8; BS 32k; 4 TPUv4; 1 day) → **79.7%**
  - SigLIP (from scratch, WebLI): B/16, BS 32k, 32 TPUv4, 5 days → **73.4%**
- **Batch-size ablations (Fig. 2; Tables 4–5):**
  - Sigmoid **outperforms softmax strongly when BS < 16k**; gap closes at large BS.
  - Performance **saturates around 32k**; very large BS (e.g., 307k) can hurt.
  - **SigLIP 9B examples (Table 4):** sigmoid peak **73.4% @32k** vs softmax peak **73.2% @98k**; at **307k**: sigmoid **71.6%**, softmax **72.6%**.
- **Stabilizing large-batch training (Sec. 4.6):** reduce Adam/AdaFactor \(\beta_2\) from **0.999 → 0.95** to mitigate gradient spikes.
- **Bias ablation (Table 3, BS 8k, 900M examples):** with bias \(b=-10\): ImageNet **63.0%** vs **62.0%** without bias.

</details>

### 📋 OpenCLIP quick API + training knobs (README)
**Code** · [source](https://github.com/mlfoundations/open_clip/blob/main/README.md)

*Factory entry points for loading CLIP/OpenCLIP models + standard zero-shot workflow; training CLI defaults/flags; notes on activations & distributed loss scaling.*

<details>
<summary>Key content</summary>

- **Load model + preprocess (factory):**
  - `model, _, preprocess = open_clip.create_model_and_transforms(model_name, pretrained=...)`
  - `tokenizer = open_clip.get_tokenizer(model_name)`
  - Set `model.eval()` (README notes model defaults to train mode; affects models w/ BatchNorm or stochastic depth).
- **Zero-shot inference procedure (cosine + temperature):**
  - Encode: `image_features = model.encode_image(image)`; `text_features = model.encode_text(text)`
  - L2 normalize: `x /= ||x||` along last dim.
  - Similarity logits: `logits = 100.0 * image_features @ text_features.T`
  - Probabilities: `softmax(logits, dim=-1)`
  - Variables: `image_features ∈ R^{B×D}`, `text_features ∈ R^{T×D}`.
- **Pretrained discovery:** `open_clip.list_pretrained()`. `pretrained` can be a key or local path (e.g., `/path/to/my/b32.pt`), including HF-downloaded `open_clip_pytorch_model.bin`.
- **Activation rationale / default:** Many checkpoints use **QuickGELU**; OpenCLIP model defs now default to `nn.GELU`. Use `-quickgelu` model variants to match QuickGELU weights; otherwise accuracy drop (fine-tuning may recover).
- **Distributed training memory rationale:** naive all-gather logit matrix is **O(n²)** space; use `--gather-with-grad` + `--local-loss` for effectively linear scaling with **numerically identical** results.
- **Training CLI example (key hyperparams):** `--batch-size=128 --lr=1e-3 --wd=0.1 --epochs=30 --warmup 10000 --workers=8 --model RN50`.
- **Empirical zero-shot ImageNet-1k examples (from table):**
  - ConvNext-Large LAION-2B 320px: **76.9%**
  - ViT-L-14 DataComp-1B 224px: **79.2%**
  - ViT-bigG-14 LAION-2B 224px: **80.1%**

</details>

---

## Related Topics

- [[topics/multimodal-fundamentals|Multimodal Fundamentals]]
- [[topics/vision-language-models|Vision Language Models]]
- [[topics/word-embeddings|Word Embeddings]]
