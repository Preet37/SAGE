# Source: https://apxml.com/courses/how-to-build-a-large-language-model/chapter-23-analyzing-model-behavior/attention-map-visualization
# Author: APXML
# Author Slug: apxml
# Title: Attention Map Visualization
# Fetched via: trafilatura
# Date: 2026-04-07

One of the most direct ways to understand the inner workings of a Transformer model is by examining its attention mechanisms. Self-attention, a primary component of the Transformer architecture, allows the model to weigh the importance of different tokens in the input sequence when computing the representation for a specific token. These attention weights, calculated for each head in each layer, form maps that show how information is routed through the model. Visualizing these maps can provide clues about the relationships the model has learned between tokens.
The core idea of self-attention involves computing scores between a token's query vector () and the key vectors () of all tokens in the sequence (including itself). These scores are scaled, normalized using softmax, and then used to compute a weighted sum of the value vectors (). The attention weights are the result of the scaled dot-product followed by the softmax:
Here, is the dimension of the key vectors. These weights represent the distribution of attention from each query token to all key tokens. A higher weight indicates that the model views the corresponding key token as more significant when generating the representation for the query token.
Most modern deep learning frameworks, including PyTorch, provide mechanisms to access these attention weights during a forward pass. When using PyTorch's nn.MultiheadAttention
layer, you can specify need_weights=True
during the forward call. This argument instructs the layer to return the average attention weights across all heads, in addition to the layer's output. For more granular, head-specific weights, you might need to slightly modify the layer's implementation or use hooks to capture the weights before they are averaged.
Here's a simplified example illustrating how to get attention weights from a nn.MultiheadAttention
layer in PyTorch:
import torch
import torch.nn as nn
# Example setup
seq_len = 5
embed_dim = 8
num_heads = 2
batch_size = 1
# Ensure embed_dim is divisible by num_heads
assert embed_dim % num_heads == 0
mha_layer = nn.MultiheadAttention(embed_dim, num_heads, batch_first=True)
# Dummy input (batch_size, seq_len, embed_dim)
query = torch.randn(batch_size, seq_len, embed_dim)
key = torch.randn(batch_size, seq_len, embed_dim)
value = torch.randn(batch_size, seq_len, embed_dim)
# Forward pass requesting attention weights
# attn_output: (batch_size, seq_len, embed_dim)
# attn_output_weights: (batch_size, seq_len, seq_len) -> Average over heads
attn_output, attn_output_weights = mha_layer(
query, value,
need_weights=True,
average_attn_weights=True
) # Set False for per-head weights (if layer supports/modified)
print("Shape of averaged attention weights:", attn_output_weights.shape)
# If average_attn_weights=False (and layer modified/hooked):
# Shape would be (batch_size, num_heads, seq_len, seq_len)
# Example: Access weights for the first batch item
first_batch_weights = attn_output_weights[0] # Shape: (seq_len, seq_len)
# first_batch_weights[i, j] is the attention from query token i to token j
# To get per-head weights (requires modification or hooks usually)
# _, attn_output_weights_per_head = mha_layer(
# query, value,
# need_weights=True,
# average_attn_weights=False
# )
# print("Shape of per-head attention weights:",
# attn_output_weights_per_head.shape)
# first_batch_head_0_weights = attn_output_weights_per_head[0, 0] # Head 0
Note that the standard nn.MultiheadAttention
returns weights averaged across heads if average_attn_weights
is True
(the default if need_weights
is True
). Accessing individual head weights typically requires either modifying the forward method or, more cleanly, registering a forward hook on the attention mechanism's internal softmax or matrix multiplication operations to capture the weights before averaging.
Once extracted, attention weights, typically matrices of size (sequence_length, sequence_length)
for each head/layer, can be visualized in several ways:
- Heatmaps: This is the most common method. A heatmap displays the attention matrix where rows represent the query tokens (output positions) and columns represent the key tokens (input positions). The color intensity of cell
(i, j)
indicates the attention weight from tokeni
to tokenj
. Lighter colors often signify higher attention. Analyzing these heatmaps can reveal patterns, such as strong diagonal lines (tokens attending to themselves), attention to preceding tokens, or specific tokens (like punctuation or special tokens) acting as information sinks or sources.
Attention weights for a single head. Notice the strong diagonal indicating self-attention, and how "sat" attends strongly to "cat". The special token
[CLS]
attends mostly to itself, while[SEP]
also shows high self-attention.
-
Multi-Head Visualization: Since each layer contains multiple attention heads, visualizing them all is important. Common techniques include:
- Small Multiples: Displaying a grid of heatmaps, one for each head. This allows direct comparison of patterns learned by different heads.
- Averaged Heatmap: Showing a single heatmap representing the average weights across all heads in a layer. This gives a summary view but can obscure head-specific behaviors.
-
Graph-Based Visualization: Attention weights can be represented as a directed graph where tokens are nodes and a directed edge from token
i
to tokenj
exists if the attention weight exceeds a certain threshold. Edge thickness or color can represent the weight's magnitude. This can be effective for visualizing connections in shorter sequences or highlighting specific strong relationships.
Simplified graph showing strong attention links. "sat" strongly attends to "cat", while "cat" attends significantly to "the".
Analyzing attention patterns can sometimes reveal linguistically plausible behaviors:
- Syntactic Dependencies: Heads might learn to attend to syntactically related words, like verbs attending to their subjects or objects, or adjectives to the nouns they modify.
- Coreference Resolution: Attention might link pronouns to the nouns they refer to earlier in the text.
- Positional Information: Some heads often focus heavily on attending to the immediately preceding or succeeding token, or to relative positional offsets.
- Special Tokens: Tokens like
[CLS]
or[SEP]
might aggregate information from the entire sequence, indicated by broad attention patterns originating from or targeting them. - Layer Progression: Attention patterns often differ across layers. Early layers might focus on local, syntactic relationships, while deeper layers may capture more complex, long-range, or semantic connections.
While attention visualization is a valuable tool, it's important to be aware of its limitations:
- Attention is Not Explanation: High attention weights do not necessarily mean that a token was the primary cause for a particular output. Attention indicates which tokens' representations were weighted highly in constructing the next layer's representation, but the complex transformations within the feed-forward networks and across layers obscure direct causality. Research has shown that attention weights might not always correlate strongly with other feature importance metrics like gradient-based measures.
- Averaging Issues: Averaging weights across heads (as done by default in some framework implementations) can hide diverse or even contradictory patterns learned by individual heads. Some heads might learn specialized functions while others appear noisy or redundant.
- Softmax Saturation/Diffusion: The softmax function forces weights to sum to 1. If no single token is clearly important, the attention might be diffused across many tokens, making interpretation difficult. Conversely, if one token is highly relevant, its weight might be close to 1, suppressing the visible weights of other potentially relevant tokens.
- Complexity in Deep Models: In very deep Transformers, the representations passed between layers become increasingly abstract. Attention patterns in later layers operate on these complex representations, making their direct mapping back to the original input tokens less straightforward to interpret.
Attention map visualization provides a window, albeit a foggy one sometimes, into the flow of information within a Transformer. It's a useful diagnostic technique for hypothesis generation about model behavior and identifying potential areas of interest, but conclusions should be drawn cautiously and ideally corroborated with other analysis methods discussed later in this chapter, such as probing internal representations or analyzing neuron activations.
Was this section helpful?
[Attention Is All You Need](https://arxiv.org/abs/1706.03762), Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, Illia Polosukhin, 2017 Advances in Neural Information Processing Systems (NIPS) 30[DOI: 10.48550/arXiv.1706.03762](https://doi.org/10.48550/arXiv.1706.03762)- This foundational paper introduces the Transformer architecture and the self-attention mechanism, which is the core subject of the section.[torch.nn.MultiheadAttention](https://pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html), PyTorch Documentation, 2024 (PyTorch Foundation) - Official documentation for the PyTorch layer used in the code example for extracting attention weights.[Speech and Language Processing (3rd ed. draft)](https://web.stanford.edu/~jurafsky/slp3/), Daniel Jurafsky, James H. Martin, 2025 (Stanford University) - A widely recognized textbook that offers a detailed account of Transformers, attention mechanisms, and their analysis in NLP, covering theory and practical aspects.
© 2026 ApX Machine Learning[AI Ethics & Transparency](/transparency)[•](/sustainability)