# Curation Report: Neural Networks
**Topic:** `neural-networks` | **Date:** 2026-04-09 16:25
**Library:** 11 existing → 23 sources (12 added, 9 downloaded)
**Candidates evaluated:** 35
**Reviewer verdict:** needs_additions

## Added (12)
- **[reference_doc]** [BatchNorm2d — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.BatchNorm2d.html)
  Gives citable, framework-accurate parameter defaults and the precise training/eval behavior students often ask about when debugging normalization and deployment discrepancies.
- **[explainer]** [Taming the tail utilization of ads inference at Meta scale](https://engineering.fb.com/2024/07/10/production-engineering/tail-utilization-ads-inference-meta/)
  Provides real-world serving constraints and measurable outcomes (latency/throughput/reliability) that connect neural network design to production inference behavior and failure modes.
- **[benchmark]** [[PDF] Understanding the difficulty of training deep feedforward neural networks](https://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf)
  Supplies both the conceptual explanation and experimental support for why deep nets were hard to train pre-2010 and how initialization/activation choices affect gradient flow.
- **[benchmark]** [Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification](https://arxiv.org/abs/1502.01852)
  Adds authoritative numbers and a widely-used initialization rule that directly addresses exploding/vanishing behavior in deep rectifier networks.
- **[paper]** [Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift](https://proceedings.mlr.press/v37/ioffe15.html)
  Seminal, equation-complete reference for normalization mechanics and why it stabilizes/accelerates training—useful for both precise formulas and conceptual explanation.
- **[paper]** [[1607.06450] Layer Normalization](https://arxiv.org/abs/1607.06450)
  Provides the canonical mathematical formulation and rationale for LayerNorm, enabling clear explanations of when/why it replaces BatchNorm (e.g., RNNs/Transformers, small batch sizes).
- **[paper]** [Understanding the difficulty of training deep feedforward neural networks](https://proceedings.mlr.press/v9/glorot10a.html)
  The curator already added a PDF version, but the PMLR proceedings page is a canonical, stable citation with the official metadata and is often preferred in reference libraries.
- **[reference_doc]** [tf.keras.optimizers.AdamW | TensorFlow v2.16.1](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW)
  Directly fills the unfilled need about weight decay semantics (decoupled vs L2 penalty) with authoritative defaults—thin API docs are exactly what students need when debugging optimizer behavior.
- **[reference_doc]** [tf.keras.optimizers.Adam | TensorFlow v2.16.1](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam)
  The library lacks any official optimizer reference; this provides citable defaults/semantics that frequently differ across frameworks and versions.
- **[paper]** [Understanding the difficulty of training deep feedforward neural networks](https://proceedings.mlr.press/v9/glorot10a.html) *(promoted by reviewer)*
  The curator already added a PDF version, but the PMLR proceedings page is a canonical, stable citation with the official metadata and is often preferred in reference libraries.
- **[reference_doc]** [tf.keras.optimizers.AdamW | TensorFlow v2.16.1](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW) *(promoted by reviewer)*
  Directly fills the unfilled need about weight decay semantics (decoupled vs L2 penalty) with authoritative defaults—thin API docs are exactly what students need when debugging optimizer behavior.
- **[reference_doc]** [tf.keras.optimizers.Adam | TensorFlow v2.16.1](https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam) *(promoted by reviewer)*
  The library lacks any official optimizer reference; this provides citable defaults/semantics that frequently differ across frameworks and versions.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Batch Normalization: Accelerating Deep Network Training by .** — [Batch Normalization: Accelerating Deep Network Training by ... - arXiv](https://arxiv.org/abs/1502.03167)
  _Skipped because:_ Same paper as the PMLR version; kept only one canonical link to avoid duplication.
- **Batch Normalization: Accelerating Deep Network Training by .** — [Batch Normalization: Accelerating Deep Network Training by ... - ar5iv](https://ar5iv.labs.arxiv.org/html/1502.03167)
  _Skipped because:_ Helpful HTML rendering, but redundant once the official proceedings version is included.
- **Batch normalization | Proceedings of the 32nd International ** — [Batch normalization | Proceedings of the 32nd International Conference on International Conference on Machine Learning - Volume 37](https://dl.acm.org/doi/10.5555/3045118.3045167)
  _Skipped because:_ Another venue landing page for the same BN paper; not needed alongside the PMLR page.
- **How does one use the mean and std from training in Batch Nor** — [How does one use the mean and std from training in Batch Norm?](https://discuss.pytorch.org/t/how-does-one-use-the-mean-and-std-from-training-in-batch-norm/136029)
  _Skipped because:_ Useful troubleshooting discussion, but less authoritative and less complete than the official PyTorch API reference for defaults/semantics.

## Reasoning
**Curator:** Selections prioritize authoritative, citable sources that directly supply missing equations/defaults (BatchNorm/LayerNorm + PyTorch API) and empirical grounding for gradient/initialization issues (Glorot+Bengio; He et al.), plus one production-scale inference case study with concrete metrics.
**Reviewer:** The curator’s additions are strong for normalization/initialization, but the library still needs at least one official optimizer/weight-decay API reference (and the canonical Glorot/Bengio proceedings link is worth including alongside the PDF).
