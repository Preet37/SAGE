# Source: https://machinelearningmastery.com/a-gentle-introduction-to-attention-masking-in-transformer-models/
# Author: Machine Learning Mastery
# Author Slug: machine-learning-mastery
# Title: A Gentle Introduction to Attention Masking in Transformer Models
# Fetched via: trafilatura
# Date: 2026-04-07

Attention mechanisms in transformer models need to handle various constraints that prevent the model from attending to certain positions. This post explores how attention masking enables these constraints and their implementations in modern language models.
Kick-start your project with my book [Building Transformer Models From Scratch with PyTorch](https://machinelearningmastery.com//building-transformer-models-from-scratch/). It provides self-study tutorials with working code.
Let’s get started.
Overview
This post is divided into four parts; they are:
- Why Attention Masking is Needed
- Implementation of Attention Masks
- Mask Creation
- Using PyTorch’s Built-in Attention
Why Attention Masking is Needed
In the [previous post](https://machinelearningmastery.com/a-gentle-introduction-to-multi-head-attention-and-grouped-query-attention/), you learned how attention mechanisms allow models to focus on relevant parts of sequences. However, there are several scenarios where you want to prevent the model from attending to certain positions:
- Causal Masking: In language modeling and text generation, the model should only attend to previous tokens, not future ones. Causal masks prevent information leakage from the future during training.
- Padding Masking: When processing batches of sequences with different lengths, shorter sequences are padded with special tokens. The model should ignore these padding tokens. This is the most common use of masking during inference.
- Custom Masking: In some applications, we might want to prevent attention to specific tokens or positions based on domain-specific rules.
Consider the sentence “The cat sat on the mat” being learned by a language model. When training the model to predict the word “sat”, it should only consider “The cat” and not “on the mat” to avoid cheating by looking at the future.
For causal masking, if you train a model with “The cat sat on the mat” as input, you would use the following mask:
$$
\begin{bmatrix}
1 & 0 & 0 & 0 & 0 & 0 \\
1 & 1 & 0 & 0 & 0 & 0 \\
1 & 1 & 1 & 0 & 0 & 0 \\
1 & 1 & 1 & 1 & 0 & 0 \\
1 & 1 & 1 & 1 & 1 & 0 \\
1 & 1 & 1 & 1 & 1 & 1
\end{bmatrix}
$$
This mask is a lower triangular matrix of all 1’s. The element $(i,j)$ is 1 means query token $i$ can attend to key token $j$. The lower triangular structure ensures that the key sequence never exceeds the query sequence length, even when a full sequence is fed to the model during training.
Some models like BERT are “bidirectional” and predict masked tokens rather than the next token. These models are trained with masks containing 0’s at random positions.
During inference, you might pass a batch of sequences to the model:
|
1 2 |
[["The", "cat", "sat", "on", "the", "mat"], ["Once", "upon", "a", "time"]] |
This batch contains two sequences of unequal length. After preprocessing and padding:
|
1 2 3 |
[["The", "cat", "sat", "on", "the", "mat"], ["In", "the", "beginning", "<PAD>", "<PAD>", "<PAD>"], ["Once", "upon", "a", "time", "<PAD>", "<PAD>"]] |
To ensure the model ignores padding tokens, you create a padding mask like this:
$$
\begin{bmatrix}
1 & 1 & 1 & 1 & 1 & 1 \\
1 & 1 & 1 & 0 & 0 & 0 \\
1 & 1 & 1 & 1 & 0 & 0
\end{bmatrix}
$$
Here, positions corresponding to padding tokens are set to 0, while all other positions are set to 1.
Implementation of Attention Masks
Building on the attention module from the [previous post](https://machinelearningmastery.com/a-gentle-introduction-to-multi-head-attention-and-grouped-query-attention/), you can modify it to support masking:
|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 |
import torch import torch.nn as nn import torch.nn.functional as F import math class MultiHeadAttention(nn.Module): def __init__(self, d_model, num_heads, dropout_prob=0): super().__init__() self.d_model = d_model self.num_heads = num_heads self.head_dim = d_model // num_heads self.dropout_prob = dropout_prob self.q_proj = nn.Linear(d_model, d_model) self.k_proj = nn.Linear(d_model, d_model) self.v_proj = nn.Linear(d_model, d_model) self.out_proj = nn.Linear(d_model, d_model) def forward(self, x, mask=None): batch_size = x.size(0) seq_length = x.size(1) # Project queries, keys, and values q = self.q_proj(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2) k = self.k_proj(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2) v = self.v_proj(x).view(batch_size, seq_length, self.num_heads, self.head_dim).transpose(1, 2) # Compute attention scores scores = torch.matmul(q, k.transpose(2, 3)) / math.sqrt(self.head_dim) # Apply mask to attention scores if mask is not None: scores = scores.masked_fill(mask == 0, float("-inf")) # Apply softmax to compute the attention weights attn_weights = F.softmax(scores, dim=-1) # Apply dropout if self.dropout_prob: attn_weights = F.dropout(attn_weights, p=self.dropout_prob) # Apply attention weights to values context = torch.matmul(attn_weights, v).transpose(1, 2).contiguous() context = context.view(batch_size, seq_length, self.d_model) return self.out_proj(context) |
This is the standard implementation of multi-head attention with masking and dropout. The mask is applied to attention scores before softmax. In mathematical terms, the mask is a matrix $M$ such that:
$$
\text{Attention}(Q, K, V, M) = \text{softmax}\left(\frac{QK^\top}{\sqrt{d}} + M\right)V
$$
The mask must be added before softmax because softmax operates across entire rows. You don’t want softmax to consider masked elements. Since softmax computes:
$$
\text{softmax}(x_i) = \frac{\exp(x_i)}{\sum_{j=1}^n \exp(x_j)}
$$
To make masked elements contribute 0 to the softmax, you add $-\infty$ to those positions. This is what the masked_fill()
function accomplishes.
Given this implementation, you can also use a mask directly if it is a matrix of $-\infty$ and 0 values:
|
1 2 3 |
... if mask is not None: scores = scores + mask |
The next section will show you how to create masks for different use cases.
Mask Creation
Since masks are essential and widely used, it’s valuable to create dedicated functions for mask generation:
|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 |
import torch def create_causal_mask(seq_len): """ Create a causal mask for autoregressive attention. Args: seq_len: Length of the sequence Returns: Causal mask of shape (seq_len, seq_len) """ mask = torch.triu(torch.full((seq_len, seq_len), float('-inf')), diagonal=1) return mask def create_padding_mask(batch, padding_token_id): """ Create a padding mask for a batch of sequences. Args: batch: Batch of sequences, shape (batch_size, seq_len) padding_token_id: ID of the padding token Returns: Padding mask of shape (batch_size, seq_len, seq_len) """ batch_size, seq_len = batch.shape padded = torch.zeros_like(batch).float().masked_fill(batch == padding_token_id, float('-inf')) mask = torch.zeros(batch_size, seq_len, seq_len) + padded[:,:,None] + padded[:,None,:] return mask[:, None, :, :] print(create_causal_mask(5)) batch = torch.tensor([ [1, 2, 3, 4, 5, 6], [1, 2, 3, 0, 0, 0], [1, 2, 3, 4, 0, 0] ]) print(create_padding_mask(batch, 0)) |
These are the two most common mask types. You can extend these for other use cases. In create_causal_mask()
, you create an upper triangular matrix of $-\infty$ values above the diagonal. Positions with 0 allow attention.
In create_padding_mask()
, you first identify padding tokens in the batch with the padded
tensor, which has the same shape as batch
. The output mask has shape (batch_size, seq_len, seq_len)
, initialized with all 0’s, then modified by adding the padded
tensor twice: once for rows and once for columns.
Running this code produces:
|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 |
tensor([[0., -inf, -inf, -inf, -inf], [0., 0., -inf, -inf, -inf], [0., 0., 0., -inf, -inf], [0., 0., 0., 0., -inf], [0., 0., 0., 0., 0.]]) tensor([[[[0., 0., 0., 0., 0., 0.], [0., 0., 0., 0., 0., 0.], [0., 0., 0., 0., 0., 0.], [0., 0., 0., 0., 0., 0.], [0., 0., 0., 0., 0., 0.], [0., 0., 0., 0., 0., 0.]]], [[[0., 0., 0., -inf, -inf, -inf], [0., 0., 0., -inf, -inf, -inf], [0., 0., 0., -inf, -inf, -inf], [-inf, -inf, -inf, -inf, -inf, -inf], [-inf, -inf, -inf, -inf, -inf, -inf], [-inf, -inf, -inf, -inf, -inf, -inf]]], [[[0., 0., 0., 0., -inf, -inf], [0., 0., 0., 0., -inf, -inf], [0., 0., 0., 0., -inf, -inf], [0., 0., 0., 0., -inf, -inf], [-inf, -inf, -inf, -inf, -inf, -inf], [-inf, -inf, -inf, -inf, -inf, -inf]]]]) |
These masks can be used directly as the mask
argument in the forward()
method of the MultiHeadAttention
class above.
Using PyTorch’s Built-in Attention with Masks
The matrix multiplication and softmax operations in the forward()
method above can be replaced with PyTorch’s built-in SDPA function:
|
1 2 |
... context = F.scaled_dot_product_attention(q, k, v, attn_mask=mask, dropout_p=self.dropout_prob) |
All other parts of the code remain the same, including the projection matrices and mask creation functions.
Alternatively, you can use PyTorch’s built-in MultiheadAttention
class. Using it with masks is straightforward:
|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 |
import torch dim = 16 num_heads = 4 attn_layer = torch.nn.MultiheadAttention(dim, num_heads, dropout=0.1, batch_first=True) # Input tensor: 0 = padding batch = torch.tensor([ [1, 2, 3, 4, 5, 6], [1, 2, 3, 0, 0, 0], [1, 2, 3, 4, 0, 0] ]) batch_size, seq_len = batch.shape x = torch.randn(batch_size, seq_len, dim) padding_mask = (batch == 0) y = attn_layer(x, x, x, key_padding_mask=padding_mask, attn_mask=None) |
You only need to specify the dimension size and number of heads when creating the attention layer. The class handles all projection matrices and dropout internally. Note that you should set batch_first=True
to use input tensors with shape (batch_size, seq_len, dim)
.
The code above demonstrates using MultiheadAttention
for self-attention, where the same tensor x
serves as query, key, and value. If your input tensor contains padding tokens, you can use key_padding_mask
to indicate where attention should be masked.
For more precise control over attention masking, you can use the attn_mask
argument:
|
1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 |
import torch def create_mask(query, key, padding_token_id): """ Create a padding mask for a batch of sequences. Args: query: Batch of sequences for query, shape (batch_size, query_len) key: Batch of sequences for key, shape (batch_size, key_len) padding_token_id: ID of the padding token Returns: Padding mask of shape (batch_size, query_len, key_len) """ batch_size, query_len = query.shape _, key_len = key.shape q_padded = torch.zeros_like(query).float().masked_fill(query == padding_token_id, float('-inf')) k_padded = torch.zeros_like(key).float().masked_fill(key == padding_token_id, float('-inf')) mask = torch.zeros(batch_size, query_len, key_len) + q_padded[:,:,None] + k_padded[:,None,:] return mask dim = 16 num_heads = 4 attn_layer = torch.nn.MultiheadAttention(dim, num_heads, dropout=0.1, batch_first=True) # Input tensor: 0 = padding batch = torch.tensor([ [1, 2, 3, 4, 5, 6], [1, 2, 3, 0, 0, 0], [1, 2, 3, 4, 0, 0] ]) batch_size, seq_len = batch.shape x = torch.randn(batch_size, seq_len, dim) attn_mask = create_mask(batch, batch, 0) attn_mask = attn_mask.repeat(1, num_heads, 1, 1).view(-1, seq_len, seq_len) y = attn_layer(x, x, x, key_padding_mask=None, attn_mask=attn_mask) |
Using attn_mask
requires more setup because it expects a 3D mask of shape (batch_size * num_heads, query_len, key_len)
. The create_mask()
function creates a 3D mask of shape (batch_size, query_len, key_len)
indicating padding token positions in the query-key matrix. You then use repeat()
to duplicate the mask for each attention head. This is the format expected by the built-in MultiHeadAttention
class.
Further Readings
Below are some resources that you may find useful:
[Attention Is All You Need](https://arxiv.org/abs/1706.03762)[PyTorch MultiheadAttention API doc](https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html)[PyTorch Scaled Dot Product Attention API doc](https://pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html)[Muilti-Headed Attention (MHA)](https://nn.labml.ai/transformers/mha.html)
Summary
In this post, you learned about attention masking in transformer models. Specifically, you learned about:
- Why attention masking is necessary for preventing information leakage and handling variable-length sequences
- Different types of masks and their applications
- How to implement attention masking in both custom and PyTorch’s built-in attention mechanisms
No comments yet.