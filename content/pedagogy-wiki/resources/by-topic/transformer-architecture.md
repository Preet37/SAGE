# Transformer Architecture

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- youtube_id: kCc8FmEb1nY
- Why: Karpathy builds a transformer from scratch in ~2 hours, covering every architectural component (attention, FFN, residual connections, layer norm) with live coding. The ground-up construction forces genuine understanding rather than hand-waving. Uniquely bridges conceptual and implementation levels in a single session.
- Level: intermediate

> **Note on existing curation:** The 3Blue1Brown video (`wjZofJX0v4M`) is excellent for visual intuition and is correctly curated — it is the best *purely visual/conceptual* intro. Karpathy's video is recommended here as the single best overall because it covers more of the related concepts (residual connections, layer norm, the full transformer block) at implementation depth. Both are worth including; the 3B1B video appears to be duplicated 6× in the existing list — **deduplication is needed.**

---

## Blog / Written explainer (best)
- **Jay Alammar** — "The Illustrated Transformer"
- url: https://jalammar.github.io/illustrated-transformer/
- Why: The definitive visual walkthrough of the transformer architecture. Alammar's step-by-step diagrams of multi-head attention, positional encoding, and the encoder-decoder stack are unmatched for building correct mental models. Widely used as a first reading in university ML courses. Covers most related concepts (positional encoding, FFN, residual connections, layer norm) in one coherent narrative.
- Level: beginner–intermediate

---

## Deep dive
- **Lilian Weng** — "Attention? Attention!"
- url: https://lilianweng.github.io/posts/2018-06-24-attention/
- Why: Weng's post situates the transformer within the broader history of attention mechanisms, covers the mathematical formulation rigorously, and connects to related variants. Her writing is precise and densely referenced, making it the best single technical reference for understanding *why* each design choice was made. Complements Alammar's visual approach with mathematical depth.
- Level: intermediate–advanced

---

## Original paper
- **Vaswani et al., 2017** — "Attention Is All You Need"
- url: https://arxiv.org/abs/1706.03762
- Why: The seminal paper introducing the transformer architecture. Unusually readable for a foundational ML paper — the architecture section is concise, the diagrams are clear, and the ablations justify design choices (number of heads, model depth, positional encoding). Essential primary source for all related concepts in this topic.
- Level: intermediate–advanced

---

## Code walkthrough
- **Andrej Karpathy** — "nanoGPT" (repository)
- url: https://github.com/karpathy/nanoGPT
- Why: The cleanest, most pedagogically intentional transformer implementation available. The `model.py` file is ~300 lines and implements a full GPT-style transformer (transformer block, multi-head attention, FFN, layer norm, residual connections, positional encoding) with no unnecessary abstraction. Directly paired with the video above. Widely used in courses and bootcamps as the reference implementation.
- Level: intermediate

---

## Coverage notes
- **Strong:** Core transformer block, multi-head attention, residual connections, layer normalization, sinusoidal positional encoding, feed-forward network — all covered excellently by the resources above.
- **Weak:** RoPE (RoPE), ALiBi, RMSNorm, SwiGLU — these are post-2020 architectural refinements not covered in the classic resources. The Karpathy video touches on some but not all.
- **Gap:** No single excellent beginner-friendly video exists specifically for **RoPE vs. ALiBi vs. sinusoidal encoding** as a comparative topic. No excellent standalone explainer for **Mixture of Experts** at the transformer-architecture level (MoE deserves its own curated resource). **Diffusion Transformers (DiT)** are not covered by any of the above — a separate resource (e.g., the DiT paper or a multimodal-focused video) should be curated under `intro-to-multimodal`. **SwiGLU** has no dedicated high-quality explainer video; the best available is the original PaLM/GLU Variants paper.

---

## Cross-validation
This topic appears in **3 courses**: `intro-to-llms`, `intro-to-multimodal`, `ml-engineering-foundations`

| Resource | intro-to-llms | intro-to-multimodal | ml-engineering-foundations |
|---|---|---|---|
| Karpathy video | ✅ core | ⚠️ partial (no DiT) | ✅ core |
| Illustrated Transformer | ✅ core | ✅ background | ✅ core |
| Weng deep dive | ✅ advanced | ✅ advanced | ✅ core |
| Attention Is All You Need | ✅ primary source | ✅ background | ✅ reference |
| nanoGPT | ✅ core | ⚠️ partial | ✅ core |

**Recommendation:** `intro-to-multimodal` needs an additional resource specifically covering **Diffusion Transformers** (DiT — Peebles & Xie, 2023, arxiv.org/abs/2212.09748). `ml-engineering-foundations` may benefit from a systems-level resource covering efficient transformer implementations (e.g., Flash Attention).

---

## Deduplication alert
The existing curation contains `youtube_id=wjZofJX0v4M` listed **6 times** for the same lesson (`intro-to-llms/transformer-block`). This should be reduced to a single entry.

---


> **[Structural note]** "Positional Information: Sinusoidal and Learned Embeddings" appears to have sub-concepts:
> positional encoding, sequence order
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*


> **[Structural note]** "Scaled Dot-Product Self-Attention: Math and Shapes" appears to have sub-concepts:
> tensor shapes, softmax stability, attention matrix
> *Discovered during enrichment for course "Attention Mechanisms (pipeline test)" | 2026-04-08*

## Last Verified
2026-04-06