## Core Definitions

**Vision Transformer (ViT).** A Vision Transformer processes an image by splitting it into fixed-size patches, linearly projecting each patch into a token embedding, adding positional embeddings, and then applying standard Transformer self-attention over the resulting token sequence; a special learned **class token** is appended and its final representation is used for classification. (DeiT/ViT tokenization description in Touvron et al., 2020: https://arxiv.org/pdf/2012.12877.pdf)

**Patch embeddings.** Patch embeddings are the per-patch token vectors produced by (1) flattening each image patch (e.g., a 16×16 RGB patch has 3·16·16 = 768 raw values) and (2) applying a learned linear projection into the Transformer embedding dimension \(D\); these patch tokens form the input sequence to the Transformer (along with class/distillation tokens). (Touvron et al., 2020: https://arxiv.org/pdf/2012.12877.pdf)

**Mel spectrogram.** A mel spectrogram is a time–frequency representation of audio where the frequency axis is mapped onto the mel scale; it is commonly used as an “image-like” input to audio models because it converts a 1D waveform into a 2D array (time × frequency) suitable for convolution/transformer-style encoders. (This lesson’s summary references mel spectrograms as the audio-side representation; no additional mel-specific formula is provided in the curated sources.)

**Shared embedding space.** A shared embedding space is a vector space where representations from different modalities (e.g., images and text) are mapped into the same dimensionality and compared directly (typically via cosine similarity after L2 normalization) so that matched pairs are close and mismatched pairs are far. In CLIP, image and text encoders each feed a **linear projection** into a shared embedding dimension, followed by L2 normalization; similarity is computed by dot product (cosine due to normalization) scaled by a learned temperature. (Radford et al., 2021: https://arxiv.org/abs/2103.00020)

**Projection layers.** Projection layers are learned mappings (often linear) applied to encoder outputs to convert modality-specific hidden states into a common embedding dimension for cross-modal comparison or fusion. CLIP explicitly uses separate linear projections \(W_i\) and \(W_t\) for image and text features before L2 normalization and similarity computation. (Radford et al., 2021: https://arxiv.org/abs/2103.00020; CLIP pipeline breakdown also notes separate projection layers fed by [CLS] in https://arxiv.org/html/2410.13016v1)

**SigLIP.** SigLIP is a CLIP-like dual-encoder trained with a **pairwise sigmoid loss** over all image–text pairs in a batch, replacing CLIP’s batch-softmax (InfoNCE) normalization; it uses a learnable temperature and bias in the similarity logits and supports an efficient distributed “chunked” implementation. (Zhai et al., 2023: https://arxiv.org/abs/2303.15343)

**DINOv2.** DINOv2 is a family of self-supervised ViT backbones trained on a large curated dataset (LVD-142M) using a combination of DINO (image-level) and iBOT (patch-level masked token) objectives plus centering (Sinkhorn-Knopp) and a feature-spreading regularizer (KoLeo), producing strong “as-is” visual features for linear probing, k-NN, and downstream tasks. (Oquab et al., 2023: http://arxiv.org/pdf/2304.07193.pdf; usage notes: https://github.com/facebookresearch/dinov2/blob/main/README.md)

---

## Key Formulas & Empirical Results

### CLIP: projections, normalization, similarity, loss
**Encoders + projections (Radford et al.).**
- Image features: \(I_f = f_\text{img}(I)\in\mathbb{R}^{N\times d_i}\)  
- Text features: \(T_f = f_\text{text}(T)\in\mathbb{R}^{N\times d_t}\)  
- Linear projections to shared dim \(d_e\): \(W_i\in\mathbb{R}^{d_i\times d_e}, W_t\in\mathbb{R}^{d_t\times d_e}\)  
- Shared embeddings: \(I_e=\mathrm{L2Norm}(I_f W_i)\), \(T_e=\mathrm{L2Norm}(T_f W_t)\)  
- Similarity logits: \(\text{logits} = I_e T_e^\top \cdot \exp(t)\) where \(t\) is learned log-temperature.  
**Supports claim:** “projection layers bridge modality-specific encoders into a shared embedding space.”  
Source: https://arxiv.org/abs/2103.00020

**CLIP symmetric cross-entropy over batch (Radford et al.).**
\[
\mathcal{L}=\tfrac{1}{2}(\mathcal{L}_\text{img}+\mathcal{L}_\text{text})
\]
with \(\mathcal{L}_\text{img}=\mathrm{CE}(\text{logits}, y;\text{axis}=0)\), \(\mathcal{L}_\text{text}=\mathrm{CE}(\text{logits}, y;\text{axis}=1)\), and labels \(y_i=i\).  
**Supports claim:** CLIP trains by matching within-batch image–text pairs among \(N\times N\) candidates.  
Source: https://arxiv.org/abs/2103.00020

**CLIP temperature default.** Temperature initialized to equivalent of **0.07** and logit scaling clipped so scale ≤ **100**.  
Source: https://arxiv.org/abs/2103.00020

### SigLIP: pairwise sigmoid loss + defaults
**SigLIP logits (Zhai et al.).**
\[
\text{logits} = z_{\text{img}} z_{\text{txt}}^\top \cdot t + b
\]
with learnable temperature \(t=\exp(t')\) and learnable bias \(b\).  
Source: https://arxiv.org/abs/2303.15343

**Pairwise sigmoid loss (Zhai et al.).**
- Label matrix: \(\text{labels} = 2I_n - \mathbf{1}_{n\times n}\) (diagonal +1, off-diagonal −1)  
- Loss:
\[
\mathcal{L} = -\frac{1}{n}\sum_{i,j}\log \sigma(\text{labels}_{ij}\cdot \text{logits}_{ij})
\]
**Supports claim:** removes batch-softmax normalization; treats each pair independently with sigmoid.  
Source: https://arxiv.org/abs/2303.15343 (also mirrored with more tables in https://arxiv.org/pdf/2303.15343v3.pdf)

**Initialization defaults (SigLIP).** Initialize \(t'\approx \log 10\) (so \(t\approx 10\)) and \(b=-10\) to avoid early domination by many negatives.  
Source: https://arxiv.org/abs/2303.15343; https://arxiv.org/pdf/2303.15343v3.pdf

**Batch-size findings (SigLIP).**
- Sigmoid outperforms softmax when batch size < **16k**; benefits saturate around **32k**; very large batch (e.g., **307k**) can hurt.  
Source: https://arxiv.org/abs/2303.15343; https://arxiv.org/pdf/2303.15343v3.pdf

**Concrete ImageNet zero-shot results (SigLIP/SigLiT).**
- SigLiT (frozen public ViT-g/14 vision): **84.5%** ImageNet zero-shot (BS 20k, 4 TPUv4, 2 days).  
- SigLIP from scratch (ViT-B/16, BS 32k): **73.4%** ImageNet zero-shot.  
Source: https://arxiv.org/pdf/2303.15343v3.pdf

### ViT tokenization facts (DeiT)
- 224×224 image with 16×16 patches → \(N=14\times 14\) patches.  
- Each patch flattened dimension: \(3\cdot16\cdot16=768\), then projected to embedding dim \(D\).  
- Positional embeddings added before Transformer blocks; class token appended (sequence length \(N+1\)).  
Source: https://arxiv.org/pdf/2012.12877.pdf

### DINOv2: dataset + evaluation numbers
**ImageNet linear eval (frozen trunk).**
- DINOv2 ViT-B/14: **84.5%** top-1  
- ViT-L/14: **86.3%**  
- ViT-g/14: **86.5%**  
Source: http://arxiv.org/pdf/2304.07193.pdf

**Data curation scale.**
- LVD-142M curated from **1.2B** unique web images after filtering/dedup; curated set size **142M**.  
Source: http://arxiv.org/pdf/2304.07193.pdf

### CLIP zero-shot as retrieval (mechanistic pipeline)
**Zero-shot classification = retrieval.** Encode prompts like “an image of a {class}” with text encoder; encode image with vision encoder; choose class with highest similarity in shared embedding space. Notes separate projection layers fed by [CLS].  
Source: https://arxiv.org/html/2410.13016v1

---

## How It Works

### A. Modality-specific encoders → shared embedding space (CLIP-style)
1. **Encode each modality with a specialized encoder.**
   - Image: vision encoder (often a ViT) outputs image feature vector \(I_f\).
   - Text: text transformer outputs text feature vector \(T_f\).  
   (Radford et al.: https://arxiv.org/abs/2103.00020)

2. **Project into a common dimension with separate projection layers.**
   - \(I_f W_i \rightarrow\) image embedding (pre-norm)
   - \(T_f W_t \rightarrow\) text embedding (pre-norm)  
   (Radford et al.: https://arxiv.org/abs/2103.00020)

3. **Normalize to make dot product = cosine similarity.**
   - \(I_e=\mathrm{L2Norm}(I_f W_i)\)
   - \(T_e=\mathrm{L2Norm}(T_f W_t)\)  
   (Radford et al.)

4. **Compute similarity matrix for a batch.**
   - \(\text{logits} = I_e T_e^\top \cdot \exp(t)\)  
   (Radford et al.)

5. **Train with a contrastive objective.**
   - CLIP: symmetric cross-entropy over the batch similarity matrix (image→text and text→image).  
   (Radford et al.)
   - SigLIP: pairwise sigmoid loss over all pairs (no batch-softmax normalization).  
   (Zhai et al.: https://arxiv.org/abs/2303.15343)

### B. ViT image encoding (patch embeddings → tokens)
1. **Split image into patches** (e.g., 16×16). For 224×224, get 14×14 = 196 patches.
2. **Flatten each patch** (RGB → 768 values for 16×16).
3. **Linear projection** of each patch to embedding dim \(D\) → patch tokens.
4. **Append class token** (learned vector) → sequence length 197.
5. **Add positional embeddings** to tokens.
6. **Transformer blocks** (self-attention + MLP) process the sequence.
7. **Use final class token** as global image representation for heads/projections.  
Source: https://arxiv.org/pdf/2012.12877.pdf

### C. CLIP zero-shot classification (as retrieval)
1. **Create a text prompt per class** (e.g., “an image of a {class}”).
2. **Encode each prompt** with the text encoder → text embeddings (class prototypes).
3. **Encode the input image** with the vision encoder → image embedding.
4. **Compute similarities** image↔each class prompt embedding in the shared space.
5. **Predict the argmax similarity** class.  
Source: https://arxiv.org/html/2410.13016v1

---

## Teaching Approaches

### Intuitive (no math)
- “Each modality speaks a different ‘raw language’ (pixels vs. words vs. audio). You first use a specialist translator (encoder) for each modality. Then you map both translations into the same ‘meeting room’ (shared embedding space) so you can compare them directly. The projection layers are the final adapters that ensure both end up in the same coordinate system.”

### Technical (with math)
- Use CLIP’s exact pipeline: \(I_e=\mathrm{L2Norm}(f_\text{img}(I)W_i)\), \(T_e=\mathrm{L2Norm}(f_\text{text}(T)W_t)\), logits \(= I_eT_e^\top\exp(t)\). Emphasize: **separate** \(W_i, W_t\) are required because \(d_i\neq d_t\) and because the encoders’ feature geometries differ. (Radford et al.: https://arxiv.org/abs/2103.00020)

### Analogy-based
- **Power adapters:** Different countries have different plug shapes (modalities). Encoders are the appliances’ internal power supplies; projection layers are the plug adapters that let everything connect to the same outlet standard (shared embedding space). Similarity is “does this plug fit / does this meaning match?”

---

## Common Misconceptions

1. **“If both modalities end up as vectors, we don’t need separate projection layers.”**  
   - **Why wrong:** The image encoder output dimension \(d_i\) and text encoder output dimension \(d_t\) can differ, and even if equal, their feature spaces are not automatically aligned. CLIP explicitly uses **two different linear projections** \(W_i\) and \(W_t\) before normalization.  
   - **Correct model:** Encoders produce modality-specific features; **projection layers are the learned alignment step** into a shared embedding dimension \(d_e\). (Radford et al.: https://arxiv.org/abs/2103.00020)

2. **“CLIP zero-shot classification is a normal classifier head with 1000 logits.”**  
   - **Why wrong:** CLIP zero-shot is framed as **retrieval**: compare the image embedding to **text prompt embeddings** for each class and pick the highest similarity.  
   - **Correct model:** The “classifier weights” are effectively the text embeddings of prompts; prediction is nearest neighbor in the shared space. (CLIP pipeline: https://arxiv.org/html/2410.13016v1)

3. **“SigLIP is just CLIP with a different temperature.”**  
   - **Why wrong:** SigLIP changes the **loss normalization structure**: it uses a **pairwise sigmoid loss** over all pairs rather than CLIP’s batch-softmax (InfoNCE) cross-entropy. It also introduces a learnable **bias** \(b\) and emphasizes distributed “chunked” computation.  
   - **Correct model:** SigLIP modifies the contrastive objective to avoid global batch normalization effects and improve behavior at smaller batch sizes. (Zhai et al.: https://arxiv.org/abs/2303.15343)

4. **“ViT ‘patch embeddings’ are just convolution features.”**  
   - **Why wrong:** In DeiT/ViT tokenization, each patch is **flattened and linearly projected** into \(D\); the model then uses Transformer self-attention over tokens. While patchification can be implemented with a conv-like operation, the defining representation is a **token sequence** with positional embeddings and (often) a class token.  
   - **Correct model:** Patch embeddings are the tokenization step that converts an image into a sequence for a Transformer. (Touvron et al.: https://arxiv.org/pdf/2012.12877.pdf)

5. **“DINOv2 is a vision-language model like CLIP.”**  
   - **Why wrong:** DINOv2 is **self-supervised vision-only** pretraining (DINO + iBOT, etc.) producing strong visual features; it does not define a text encoder or a shared image–text embedding objective in the cited sources.  
   - **Correct model:** DINOv2 is a strong **visual backbone** you might later connect to language via a projector/adapter, but its pretraining is unimodal. (Oquab et al.: http://arxiv.org/pdf/2304.07193.pdf)

---

## Worked Examples

### 1) CLIP-style zero-shot classification (minimal NumPy-like pseudocode)
Goal: show the *mechanics* of “classification as retrieval” in a shared embedding space.

```python
# Given:
# - image_encoder: I -> I_f (shape [d_i])
# - text_encoder:  prompt -> T_f (shape [d_t])
# - Wi: [d_i, d_e], Wt: [d_t, d_e]
# - logit_scale = exp(t)

def l2norm(x, eps=1e-12):
    return x / ( (x**2).sum()**0.5 + eps )

classes = ["cat", "dog", "airplane"]
prompts = [f"an image of a {c}" for c in classes]

# Encode text prompts (class prototypes)
text_embs = []
for p in prompts:
    Tf = text_encoder(p)          # R^{d_t}
    Te = l2norm(Tf @ Wt)          # R^{d_e}
    text_embs.append(Te)

# Encode image
If = image_encoder(image)         # R^{d_i}
Ie = l2norm(If @ Wi)              # R^{d_e}

# Similarities (cosine due to normalization), scaled by exp(t)
logits = [ (Ie @ Te) * logit_scale for Te in text_embs ]
pred = classes[argmax(logits)]
```

**Tutor notes (what to emphasize verbally):**
- The “classifier” is not a learned 3-way head here; it’s the set of **text embeddings** for prompts. (https://arxiv.org/html/2410.13016v1)
- The projection matrices \(W_i, W_t\) are what make dot products meaningful across modalities. (https://arxiv.org/abs/2103.00020)

### 2) ViT patch token counting sanity check (DeiT numbers)
Student often asks “how many tokens does ViT see?”

- Image: 224×224, patch: 16×16 → 14×14 = **196** patches.  
- Add class token → **197** tokens total.  
- Each patch raw dimension: 3·16·16 = **768**, then projected to embedding dim \(D\).  
Source: https://arxiv.org/pdf/2012.12877.pdf

---

## Comparisons & Trade-offs

| Choice | What changes | Pros | Cons | When to choose | Source |
|---|---|---|---|---|---|
| **CLIP (InfoNCE / batch-softmax)** | Symmetric cross-entropy over batch similarity matrix | Strong standard baseline; clean probabilistic “match among N” framing | Depends on batch-softmax normalization; batch size can matter | When you can afford large batches and want canonical CLIP setup | https://arxiv.org/abs/2103.00020 |
| **SigLIP (pairwise sigmoid)** | Pairwise sigmoid loss over all pairs; no global softmax | Better at smaller batch sizes (<16k); efficient distributed “chunked” loss; includes bias \(b\) | Different calibration dynamics; still needs many negatives | When batch size is constrained or distributed efficiency is key | https://arxiv.org/abs/2303.15343 |
| **CLIP-style shared embedding (dual encoder)** | Compare modalities via similarity in shared space | Fast retrieval; enables zero-shot classification as retrieval | Limited cross-modal reasoning vs deep fusion (not covered here) | When you need scalable retrieval/zero-shot classification | https://arxiv.org/html/2410.13016v1 |
| **DINOv2 (vision-only SSL)** | Self-supervised visual pretraining (DINO+iBOT+KoLeo) | Very strong frozen visual features (linear probe/k-NN) | Not aligned to text by default | When you need a robust vision backbone before adding a projector/adapter | http://arxiv.org/pdf/2304.07193.pdf |

---

## Prerequisite Connections

- **Transformer self-attention basics.** Needed to understand how ViT processes patch tokens and why a class token can aggregate information. (DeiT provides the attention equation and token pipeline: https://arxiv.org/pdf/2012.12877.pdf)
- **Cosine similarity + L2 normalization.** Needed to interpret “shared embedding space” comparisons and why dot product becomes cosine in CLIP. (CLIP uses L2Norm then dot product: https://arxiv.org/abs/2103.00020)
- **Contrastive learning objective intuition.** Needed to understand why matched pairs are pulled together and mismatches pushed apart (CLIP InfoNCE vs SigLIP sigmoid). (CLIP: https://arxiv.org/abs/2103.00020; SigLIP: https://arxiv.org/abs/2303.15343)

---

## Socratic Question Bank

1. **If I remove \(W_i\) and \(W_t\) and compare encoder outputs directly, what assumption am I making?**  
   *Good answer:* That both encoders already output aligned vectors in the same dimension/geometry; CLIP does not assume this and learns separate projections.

2. **Why does CLIP zero-shot classification need prompts at all—why not just class names?**  
   *Good answer:* Because the “class prototype” is a text embedding; prompts shape that embedding and CLIP’s pipeline is retrieval over those embeddings.

3. **What does L2 normalization buy you in CLIP’s similarity computation?**  
   *Good answer:* Dot product becomes cosine similarity; magnitude no longer dominates; temperature controls scale.

4. **In ViT-B/16 at 224×224, how many tokens go into self-attention, and what token is used for classification?**  
   *Good answer:* 196 patch tokens + 1 class token = 197; class token output is used.

5. **What is the key structural difference between CLIP’s loss and SigLIP’s loss?**  
   *Good answer:* CLIP uses batch-softmax cross-entropy (InfoNCE) over rows/cols; SigLIP uses independent pairwise sigmoid terms for all pairs (no global normalization).

6. **Why might SigLIP help more at smaller batch sizes?**  
   *Good answer:* Per the paper’s findings, sigmoid outperforms softmax when BS < 16k; removing batch-softmax normalization changes dependence on batch size.

7. **If you have a strong vision-only backbone (DINOv2), what extra component do you still need to do CLIP-like retrieval with text?**  
   *Good answer:* A text encoder and a learned projection/alignment into a shared embedding space (projection layers).

8. **What does it mean to say “classification is retrieval” in CLIP?**  
   *Good answer:* You retrieve the nearest text prompt embedding to the image embedding; the nearest prompt determines the class.

---

## Likely Student Questions

**Q: What is the exact CLIP similarity logit formula?**  
→ **A:** \(\text{logits} = I_e T_e^\top \cdot \exp(t)\), where \(I_e=\mathrm{L2Norm}(I_f W_i)\), \(T_e=\mathrm{L2Norm}(T_f W_t)\), and \(t\) is a learned log-temperature. (Radford et al., https://arxiv.org/abs/2103.00020)

**Q: What loss does CLIP use?**  
→ **A:** A symmetric cross-entropy over the batch similarity matrix: \(\mathcal{L}=\tfrac12(\mathrm{CE}(\text{logits},y;\text{axis}=0)+\mathrm{CE}(\text{logits},y;\text{axis}=1))\) with labels \(y_i=i\). (Radford et al., https://arxiv.org/abs/2103.00020)

**Q: How does SigLIP’s loss differ from CLIP’s InfoNCE?**  
→ **A:** SigLIP uses a pairwise sigmoid loss \(-\frac{1}{n}\sum_{i,j}\log\sigma(z_{ij}s_{ij})\) with \(z_{ij}=+1\) for matched pairs and \(-1\) otherwise, and logits \(s_{ij}=t\,x_i\cdot y_j + b\); it removes the batch-softmax normalization used in InfoNCE. (Zhai et al., https://arxiv.org/abs/2303.15343)

**Q: What are SigLIP’s key initialization defaults?**  
→ **A:** Initialize temperature parameter \(t'=\log 10\) (so \(t\approx 10\)) and bias \(b=-10\) to avoid early over-correction due to many negatives. (Zhai et al., https://arxiv.org/abs/2303.15343)

**Q: How many tokens does a ViT see for a 224×224 image with 16×16 patches?**  
→ **A:** \(14\times14=196\) patch tokens, plus a class token → 197 tokens. Each patch is flattened (3·16·16=768) then linearly projected to embedding dim \(D\). (Touvron et al., https://arxiv.org/pdf/2012.12877.pdf)

**Q: How does CLIP do zero-shot ImageNet classification mechanically?**  
→ **A:** It encodes a prompt per class (e.g., “an image of a {class}”) with the text encoder, encodes the image with the vision encoder, and picks the class whose text embedding has the highest similarity to the image embedding in the shared space. (Mechanistic pipeline: https://arxiv.org/html/2410.13016v1)

**Q: What are representative DINOv2 ImageNet linear-probe numbers?**  
→ **A:** Frozen linear eval top-1: ViT-B/14 **84.5%**, ViT-L/14 **86.3%**, ViT-g/14 **86.5%**. (Oquab et al., http://arxiv.org/pdf/2304.07193.pdf)

**Q: How do I load a DINOv2 backbone quickly in PyTorch?**  
→ **A:** Example from the official README:  
```python
import torch
dinov2_vitb14 = torch.hub.load('facebookresearch/dinov2','dinov2_vitb14')
```  
(https://github.com/facebookresearch/dinov2/blob/main/README.md)

---

## Available Resources

### Videos
- [CLIP: Connecting Text and Images (Paper Explained)](https://youtube.com/watch?v=OZF1t_Hieq8) — Surface when: student asks for an end-to-end narrative of CLIP’s dual-encoder training and zero-shot retrieval framing.

### Articles & Tutorials
- [Lilian Weng — Contrastive Representation Learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/) — Surface when: student is confused about contrastive objectives broadly (InfoNCE family, negatives, batch effects) and needs a wider map beyond CLIP/SigLIP.

---

## Visual Aids

![CLIP enables zero-shot image classification via shared text-image embeddings. (Huyen Chip)](/api/wiki-images/vision-language-models/images/huyenchip-2023-10-10-multimodal-html_004.png)  
**Show when:** student asks “what does ‘shared embedding space’ buy us?” or “how can CLIP classify without training a classifier head?”

---

## Key Sources

- [Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020) — Defines the dual-encoder + projection + L2-normalized shared embedding space and the symmetric batch contrastive loss.
- [SigLIP: Pairwise Sigmoid Loss for Image-Text Pretraining](https://arxiv.org/abs/2303.15343) — Primary source for the sigmoid loss, temperature/bias defaults, and batch-size behavior.
- [DeiT: Training Data-efficient Image Transformers](https://arxiv.org/pdf/2012.12877.pdf) — Precise ViT patch/token pipeline (patch embeddings, class token, positional embeddings).
- [DINOv2](http://arxiv.org/pdf/2304.07193.pdf) — Authoritative details on self-supervised ViT training recipe, dataset curation, and strong linear-probe results.
- [CLIP zero-shot pipeline + mechanistic breakdown](https://arxiv.org/html/2410.13016v1) — Clear statement of “zero-shot classification as retrieval” and notes on separate projection layers fed by [CLS].