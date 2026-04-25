# Source: https://www.abhik.ai/concepts/attention/masked-attention
# Author: Abhik Sarkar
# Author Slug: abhik-sarkar
# Title: Masked and Causal Attention - Abhik Sarkar
# Fetched via: trafilatura
# Date: 2026-04-11

[Masked and Causal Attention: Preserving Causality in Generation](#masked-and-causal-attention-preserving-causality-in-generation)
Masked attention is the key mechanism that allows transformers to generate sequences one token at a time, ensuring models only attend to past tokens and maintaining the autoregressive property essential for generation tasks.
[Interactive Masked Attention Visualization](#interactive-masked-attention-visualization)
Explore how masking patterns control information flow in attention:
[Why Masked Attention?](#why-masked-attention)
[The Information Leakage Problem](#the-information-leakage-problem)
In standard self-attention, every position can attend to every other position:
- During training: Model can "cheat" by looking at future tokens
- During inference: Future tokens don't exist yet
Solution: Apply masks to prevent attending to future positions
[Types of Masking](#types-of-masking)
- Causal Mask: For autoregressive generation (GPT-style)
- Padding Mask: For variable-length sequences
- Custom Masks: For specific attention patterns
- Combined Masks: Multiple masks applied together
[How Causal Masking Works](#how-causal-masking-works)
[The Causal Mask](#the-causal-mask)
For a sequence of length n, the causal mask is a lower triangular matrix:
This ensures position i can only attend to positions 0 through i.
[Applying the Mask](#applying-the-mask)
Mask Application Process:
- Compute attention scores: Q × K^T / √d_k
- Apply mask: Replace masked positions with -∞
- Apply softmax: -∞ becomes 0, preventing attention flow
- Result: Clean attention weights with no information leakage
Key Insight: Softmax(-∞) = 0, completely blocking attention to masked positions
[Implementation](#implementation)
[Creating Causal Masks](#creating-causal-masks)
Standard Approach:
- Create lower triangular matrix where position i can attend to positions 0...i
- Use torch.tril() for efficient generation
- Shape: [seq_len, seq_len]
Memory-Efficient Approach:
- Generate mask on-the-fly using broadcasting with row/column indices
- Compare row_indices >= col_indices
- No memory allocation for full matrix
[Masked Self-Attention](#masked-self-attention)
Key Components:
- Projections: Standard Q, K, V linear layers
- Causal Mask Buffer: Pre-computed lower triangular matrix registered as buffer
- Mask Application: Scores masked before softmax
- Optional Padding Mask: Can combine causal + padding masks
Forward Pass Steps:
- Project input to Q, K, V and reshape for multi-head attention
- Compute attention scores: Q × K^T / √d_k
- Slice pre-computed causal mask to current sequence length
- Apply mask: scores.masked_fill(mask == 0, -∞)
- Apply softmax and dropout
- Apply attention to values
- Reshape and project output
[Training vs Inference](#training-vs-inference)
[Training: Parallel Processing](#training-parallel-processing)
Efficient Batch Training:
- Process entire sequence at once with causal mask applied
- Compute logits for all positions in parallel
- Calculate loss across all positions simultaneously (teacher forcing)
- GPU can parallelize across sequence dimension
Benefit: Extremely fast training compared to sequential generation
[Inference: Sequential Generation](#inference-sequential-generation)
Autoregressive Token Generation:
- Start with prompt tokens
- Run forward pass to get logits for all positions
- Use only last position's logits to predict next token
- Sample next token (greedy, top-k, or nucleus sampling)
- Append to sequence and repeat
- Stop at max length or end-of-sequence token
Key Difference: Training is parallel, inference is sequential
[KV Cache Optimization](#kv-cache-optimization)
Efficient Generation with KV Cache:
The Problem: Recomputing K,V for all previous tokens at each step is wasteful
The Solution:
- Store computed K,V pairs in cache
- For each new token, compute only new K,V
- Concatenate with cached K,V from previous tokens
- Compute Q only for current token
- Massive speedup for long sequences
Cache Management:
- Initialize empty cache
- For each generated token:
- Compute K,V for new token only
- Concatenate with cached K,V
- Update cache with full K,V
- Compute attention with full context
- Reuse cache across generation steps
[Types of Attention Masks](#types-of-attention-masks)
[1. Standard Causal Mask](#1-standard-causal-mask)
Purpose: Autoregressive generation (GPT-style) Pattern: Lower triangular matrix Use Case: Language modeling, text generation
[2. Padding Mask](#2-padding-mask)
Purpose: Handle variable-length sequences in batches Pattern: Mask positions beyond actual sequence length Implementation: Create binary mask based on sequence lengths Use Case: Efficient batching with different length inputs
[3. Prefix LM Mask](#3-prefix-lm-mask)
Purpose: Bidirectional attention for prefix, causal for generation Pattern: Full attention within prefix, then causal Use Case: Given context (bidirectional), generate completion (causal) Example: T5, UL2 models
[4. Block-Sparse Mask](#4-block-sparse-mask)
Purpose: Reduce computation for long sequences Pattern: Local attention within blocks + global attention to special tokens Use Case: Long-context models (Longformer, BigBird) Benefit: O(n) complexity instead of O(n²)
[Attention Patterns with Masking](#attention-patterns-with-masking)
[Visualization of Different Masks](#visualization-of-different-masks)
Interactive Visualization: Use the interactive component above to explore different mask patterns
Common Patterns:
- Causal: Lower triangular (each position attends to itself and previous)
- Padding: Block pattern (mask padding tokens)
- Prefix LM: Hybrid pattern (bidirectional prefix + causal suffix)
- Block-Sparse: Diagonal blocks + vertical/horizontal stripes for global tokens
[Special Considerations](#special-considerations)
[1. Numerical Stability](#1-numerical-stability)
Mask Value Selection:
- Use -1e9 instead of -∞ for better numerical stability
- Or use torch.finfo(dtype).min for dtype-specific minimum
- Prevents NaN issues in some implementations
[2. Efficient Masking](#2-efficient-masking)
Pre-computation Strategy:
- Register causal mask as buffer in module initialization
- Pre-compute for maximum sequence length
- Slice to actual sequence length during forward pass
- Avoids repeated mask creation overhead
Benefits:
- No repeated tensor allocations
- Mask moves with model to correct device
- Included in state_dict for checkpointing
[3. Flash Attention with Causal Mask](#3-flash-attention-with-causal-mask)
Modern Optimization (PyTorch 2.0+):
- Use F.scaled_dot_product_attention() with is_causal=True
- Automatically applies causal masking with fused kernels
- 2-4× speedup over manual implementation
- Reduces memory usage (no explicit mask materialization)
[Common Applications](#common-applications)
[Language Modeling (GPT)](#language-modeling-gpt)
Architecture:
- Stack of transformer decoder blocks
- Each block contains masked self-attention
- Layer normalization before attention (pre-norm)
- Residual connections around attention and feedforward
Forward Pass:
- Apply layer norm
- Masked self-attention with causal mask
- Add residual connection
- Apply layer norm
- Feedforward network
- Add residual connection
[Decoder in Seq2Seq](#decoder-in-seq2seq)
Architecture:
- Masked self-attention on decoder inputs (causal)
- Cross-attention to encoder outputs (no mask)
- Feedforward network
Key Differences:
- Self-attention uses causal mask (can't see future)
- Cross-attention has no mask (can see all encoder outputs)
- Used in translation, summarization models (T5, BART)
[Performance Implications](#performance-implications)
[Memory Usage](#memory-usage)
- Standard: O(seq_len²) for mask storage
- Optimized: O(1) with on-the-fly generation
- Flash Attention: Fused kernels eliminate mask materialization
[Computational Cost](#computational-cost)
- Masking itself: O(seq_len²) comparisons
- Can be fused with attention computation
- Negligible overhead with proper implementation
[Best Practices](#best-practices)
- Pre-compute masks when sequence length is known
- Use buffers for fixed masks to avoid re-allocation
- Leverage built-in functions like
is_causal
in PyTorch 2.0+ - Combine masks efficiently using logical operations
- Profile memory usage for long sequences
[Common Pitfalls](#common-pitfalls)
[Pitfall 1: Wrong Mask Shape](#pitfall-1-wrong-mask-shape)
Problem: Mask shape [seq_len, seq_len] doesn't broadcast with scores [batch, heads, seq_len, seq_len]
Solution: Reshape mask to broadcast-compatible shape [1, 1, seq_len, seq_len]
Why: PyTorch broadcasting rules require compatible dimensions
[Pitfall 2: Forgetting to Mask During Inference](#pitfall-2-forgetting-to-mask-during-inference)
Problem: Not applying causal mask during generation leads to incorrect behavior
Solution: Always apply causal mask, even during inference
Impact: Without mask, model sees "future" tokens that don't exist yet
[Pitfall 3: Mask Value Too Small](#pitfall-3-mask-value-too-small)
Problem: Using small negative values (like -1) doesn't effectively block attention
Solution: Use large negative value (-1e9 or -∞)
Reason: Softmax needs very negative values to produce near-zero outputs
[Related Concepts](#related-concepts)
[Self-Attention](/concepts/attention/self-attention)[Scaled Dot-Product Attention](/concepts/attention/scaled-dot-product)[KV Cache](/concepts/llms/kv-cache)[GPT Architecture](/concepts/llms/tokenization)- Transformer Decoder