# Curation Report: Transformer Architecture
**Topic:** `transformer-architecture` | **Date:** 2026-04-09 16:38
**Library:** 6 existing → 20 sources (14 added, 9 downloaded)
**Candidates evaluated:** 36
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467)
  Gives citable, precise math for RMSNorm vs LayerNorm and the design rationale (dropping re-centering) that tutors can quote and derive from.
- **[paper]** [[2002.05202] GLU Variants Improve Transformer](https://arxiv.org/abs/2002.05202)
  Provides the canonical equations and experimentally motivated design choices behind SwiGLU/GLU MLP variants used in modern Transformer blocks.
- **[paper]** [Scaling to Trillion Parameter Models with Simple and Efficient Sparsity](https://jmlr.org/papers/volume23/21-0998/21-0998.pdf)
  This is the authoritative, detailed algorithmic description of MoE Transformers (routing + stability tricks) that a tutor can walk through procedurally.
- **[reference_doc]** [TransformerEncoderLayer — PyTorch 2.11 documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html)
  Provides citable API defaults and parameter meanings for a widely used Transformer block implementation, useful for answering 'what are the defaults?' precisely.
- **[paper]** [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity (JMLR 2022)](https://arxiv.org/pdf/2101.03961.pdf)
  This is the finalized journal version of the exact MoE method the curator wants to teach; it’s more citable and complete than relying on secondary summaries or snippets.
- **[paper]** [GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding](https://arxiv.org/pdf/2006.16668v1.pdf)
  Even if Switch is cleaner for routing, GShard is the key architecture/systems reference for how MoE Transformers are actually scaled and trained, which a Socratic tutor will get asked about.
- **[reference_doc]** [torch.nn.TransformerEncoderLayer — PyTorch 2.9 documentation](https://docs.pytorch.org/docs/2.9/generated/torch.nn.TransformerEncoderLayer.html)
  Versioned API docs are valuable for reproducibility and answering “what were the defaults in version X?”; including one stable+one versioned page avoids ambiguity.
- **[reference_doc]** [torch.nn.TransformerEncoderLayer — PyTorch 2.8 documentation](https://docs.pytorch.org/docs/2.8/generated/torch.nn.TransformerEncoderLayer.html)
  Thin docs are exactly what’s needed for precise parameter/default questions; keeping a second pinned version helps when learners’ environments differ.
- **[paper]** [Peri-LN: Revisiting Layer Normalization in the Transformer](https://arxiv.org/html/2502.02732v1)
  The current library lacks numeric ablations around normalization choices; this directly supplies empirical tables/plots and mechanistic rationale a tutor can cite.
- **[paper]** [Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity (JMLR 2022)](https://arxiv.org/pdf/2101.03961.pdf) *(promoted by reviewer)*
  This is the finalized journal version of the exact MoE method the curator wants to teach; it’s more citable and complete than relying on secondary summaries or snippets.
- **[paper]** [GShard: Scaling Giant Models with Conditional Computation and Automatic Sharding](https://arxiv.org/pdf/2006.16668v1.pdf) *(promoted by reviewer)*
  Even if Switch is cleaner for routing, GShard is the key architecture/systems reference for how MoE Transformers are actually scaled and trained, which a Socratic tutor will get asked about.
- **[reference_doc]** [torch.nn.TransformerEncoderLayer — PyTorch 2.9 documentation](https://docs.pytorch.org/docs/2.9/generated/torch.nn.TransformerEncoderLayer.html) *(promoted by reviewer)*
  Versioned API docs are valuable for reproducibility and answering “what were the defaults in version X?”; including one stable+one versioned page avoids ambiguity.
- **[reference_doc]** [torch.nn.TransformerEncoderLayer — PyTorch 2.8 documentation](https://docs.pytorch.org/docs/2.8/generated/torch.nn.TransformerEncoderLayer.html) *(promoted by reviewer)*
  Thin docs are exactly what’s needed for precise parameter/default questions; keeping a second pinned version helps when learners’ environments differ.
- **[paper]** [Peri-LN: Revisiting Layer Normalization in the Transformer](https://arxiv.org/html/2502.02732v1) *(promoted by reviewer)*
  The current library lacks numeric ablations around normalization choices; this directly supplies empirical tables/plots and mechanistic rationale a tutor can cite.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] GShard: Scaling Giant Models with Conditional Computat** — [[PDF] GShard: Scaling Giant Models with Conditional Computation ... - arXiv](https://arxiv.org/pdf/2006.16668.pdf)
  _Skipped because:_ Strong MoE systems paper, but Switch Transformers is the cleaner, more directly teachable step-by-step routing reference for core MoE mechanics.
- **Understanding the RoPE Extensions of Long-Context LLMs - arX** — [Understanding the RoPE Extensions of Long-Context LLMs - arXiv](https://arxiv.org/html/2406.13282v1)
  _Skipped because:_ Relevant to RoPE scaling/extrapolation, but the stated need also requires baseline RoPE/ALiBi definitions and benchmark comparisons, which aren’t adequately covered by the provided candidate set.

## Reasoning
**Curator:** Selections prioritize authoritative, citable sources that directly provide equations (RMSNorm, GLU/SwiGLU), a step-by-step MoE routing algorithm (Switch), and official API defaults (PyTorch). Positional-encoding formulas and broad comparative benchmark tables were not adequately covered by the provided candidates, so they are left unfilled with targeted search hints.
**Reviewer:** The core Transformer basics are well covered, but the library should add the finalized Switch paper, a scaling/systems MoE reference (GShard), version-pinned PyTorch API docs, and at least one empirical normalization study to better meet the stated unfilled needs.
