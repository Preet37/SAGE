# Long Context

## Video (best)
- **Andrej Karpathy** — "Let's build GPT: from scratch, in code, spelled out."
- youtube_id: kCc8FmEb1nY
- Why: Clear, practical explanation of Transformer attention and why context length matters; good foundation before diving into long-context extensions.
- Level: Beginner → Intermediate

## Blog / Written explainer (best)
- **Lil'Log (Lilian Weng)** — "Attention? Attention!"
- url: https://lilianweng.github.io/posts/2018-06-24-attention/
- Why: Strong conceptual grounding in attention mechanisms; useful for understanding efficient attention and context utilization issues.
- Level: Beginner → Intermediate

## Deep dive
- **Jay Alammar** — "The Illustrated Transformer"
- url: https://jalammar.github.io/illustrated-transformer/
- Why: Visual, intuitive walkthrough of self-attention and positional information; helpful context for rope scaling, interpolation, and long-context behavior.
- Level: Beginner → Intermediate
- **Lilian Weng** — "Transformer Family"
- url: https://lilianweng.github.io/posts/2020-04-07-the-transformer-family/
- Why: Surveys Transformer variants, including efficiency-oriented ideas that connect to long-context evaluation and efficient attention.
- Level: Intermediate

## Original paper
- **Su et al.** — "RoFormer: Enhanced Transformer with Rotary Position Embedding"
- url: https://arxiv.org/abs/2104.09864
- Why: Primary reference for RoPE (rotary position embeddings), a key building block behind many modern long-context extension techniques (and later rope scaling variants).
- Level: Intermediate → Advanced
- **Beltagy, Peters, Cohan** — "Longformer: The Long-Document Transformer"
- url: https://arxiv.org/abs/2004.05150
- Why: Canonical efficient-attention approach (sparse attention) for longer sequences; useful contrast vs “just increase context”.
- Level: Intermediate → Advanced
- **Dao et al.** — "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness"
- url: https://arxiv.org/abs/2205.14135
- Why: Widely used exact-attention implementation enabling longer contexts in practice by reducing memory/compute overhead.
- Level: Advanced

## Code walkthrough
- **Andrej Karpathy** — "nanoGPT"
- url: https://github.com/karpathy/nanoGPT
- Why: Readable reference implementation of GPT-style training/inference; good base for experimenting with context length, attention cost, and positional embeddings.
- Level: Intermediate

## Coverage notes
- Strong: Transformer attention fundamentals; positional embeddings (incl. RoPE); efficient attention (Longformer) and practical attention optimization (FlashAttention).
- Weak: Direct, practitioner-focused guides on **rope scaling**, **yarn**, and **position interpolation** as used in modern long-context LLMs (few stable, canonical explainers).
- Gap: A single authoritative explainer that cleanly compares **retrieval vs long context**, addresses **lost-in-the-middle** and **context utilization**, and ties them to **needle-in-a-haystack** evaluation and **context compression** techniques.

## Last Verified
2026-04-09