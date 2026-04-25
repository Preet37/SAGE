# Curation Report: Multi-Head Attention
**Topic:** `multi-head-attention` | **Date:** 2026-04-09 16:23
**Library:** 9 existing → 16 sources (7 added, 6 downloaded)
**Candidates evaluated:** 50
**Reviewer verdict:** good

## Added (7)
- **[reference_doc]** [MultiheadAttention — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)
  Gives authoritative, citable API semantics and defaults for multi-head attention in PyTorch, including masking conventions and shape contracts that students routinely get wrong.
- **[paper]** [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)
  Primary-source mathematical formulation and rationale for RoPE, with enough detail to derive and implement rotary embeddings correctly in multi-head attention.
- **[paper]** [Train Short, Test Long: Attention with Linear Biases Enables Input Length Extrapolation](https://arxiv.org/abs/2108.12409)
  Provides the canonical definition of ALiBi and the design rationale for length extrapolation, enabling precise explanation of how positional bias integrates into attention.
- **[benchmark]** [[PDF] Are Sixteen Heads Really Better than One? - NIPS](https://proceedings.neurips.cc/paper_files/paper/2019/file/2c601ad9d2ff9bc8b282670cdd54f69f-Paper.pdf)
  Directly supports teaching about head redundancy, pruning, and the accuracy/efficiency tradeoff with empirical evidence and a reproducible pruning method.
- **[paper]** [[PDF] FlashAttention: Fast and Memory-Efficient Exact Attention with IO ...](https://arxiv.org/pdf/2205.14135.pdf)
  A widely cited deployment-relevant optimization paper with concrete performance metrics and system-level rationale useful for explaining real-world latency/memory constraints.
- **[reference_doc]** [tf.keras.layers.MultiHeadAttention | TensorFlow](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention)
  Even if “thin,” this is an authoritative spec for a widely used MHA API and complements PyTorch by clarifying mask conventions and tensor shape expectations in another major framework.
- **[reference_doc]** [tf.keras.layers.MultiHeadAttention | TensorFlow](https://www.tensorflow.org/api_docs/python/tf/keras/layers/MultiHeadAttention) *(promoted by reviewer)*
  Even if “thin,” this is an authoritative spec for a widely used MHA API and complements PyTorch by clarifying mask conventions and tensor shape expectations in another major framework.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **FlashAttention-3: Fast and Accurate Attention with Asynchron** — [FlashAttention-3: Fast and Accurate Attention with Asynchrony and ...](https://arxiv.org/html/2407.08608v1)
  _Skipped because:_ Strong for cutting-edge kernels, but FlashAttention (v1) is the more established baseline reference for teaching core IO-aware attention ideas and commonly cited deployment metrics.
- **Fourier Position Embedding:Enhancing Attention's Periodic Ex** — [Fourier Position Embedding:Enhancing Attention's Periodic Extension for Length Generalization](https://arxiv.org/pdf/2412.17739.pdf)
  _Skipped because:_ Likely contains useful comparisons, but it is not a clearly established, canonical benchmark source for sinusoidal vs learned vs RoPE vs ALiBi long-context generalization relative to more standard evaluations.
- **Discrepancy Between key_padding_mask and attn_mask ...** — [Discrepancy Between key_padding_mask and attn_mask ...](https://discuss.pytorch.org/t/discrepancy-between-key-padding_mask-and_attn_mask-in-multiheadattention-layer/203322)
  _Skipped because:_ Helpful clarifications, but it is forum content rather than authoritative API specification; the official docs are the better citable reference.

## Reasoning
**Curator:** Selections prioritize authoritative primary sources and official docs that provide (1) exact equations for positional methods and (2) concrete empirical/production-relevant evidence for head redundancy and attention optimization, while avoiding non-authoritative or less canonical candidates.
**Reviewer:** The curator’s additions are strong and on-target; among the provided near-misses/candidates, only the official TensorFlow MultiHeadAttention API doc clearly adds durable, citable reference value beyond what’s already included.
