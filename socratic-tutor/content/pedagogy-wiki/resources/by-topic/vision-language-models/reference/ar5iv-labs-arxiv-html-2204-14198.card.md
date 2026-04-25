# Card: Flamingo architecture—Perceiver Resampler + gated cross-attn for interleaved vision/text
**Source:** https://ar5iv.labs.arxiv.org/html/2204.14198  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Copyable architectural definitions (Perceiver Resampler; gated cross-attention insertion; masking for interleaved inputs)

## Key Content
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

## When to surface
Use for questions about Flamingo’s exact conditioning mechanism (gated cross-attn insertion + 0-init gating), Perceiver Resampler fixed-token interface (64 tokens), and how interleaved image/text prompts are handled via attention masking and Eq. 1/Eq. 2 training.