# Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.MultiheadAttention.html
# Title: MultiheadAttention — PyTorch 2.11 documentation
# Fetched via: trafilatura
# Date: 2026-04-09

MultiheadAttention[#](#multiheadattention)
-
class torch.nn.MultiheadAttention(embed_dim, num_heads, dropout=0.0, bias=True, add_bias_kv=False, add_zero_attn=False, kdim=None, vdim=None, batch_first=False, device=None, dtype=None)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/nn/modules/activation.py#L1089)[#](#torch.nn.MultiheadAttention) Allows the model to jointly attend to information from different representation subspaces.
This MultiheadAttention layer implements the original architecture described in the
[Attention Is All You Need](https://arxiv.org/abs/1706.03762)paper. The intent of this layer is as a reference implementation for foundational understanding and thus it contains only limited features relative to newer architectures. Given the fast pace of innovation in transformer-like architectures, we recommend exploring this[tutorial](https://pytorch.org/tutorials/intermediate/transformer_building_blocks.html)to build efficient layers from building blocks in core or using higher level libraries from the[PyTorch Ecosystem](https://landscape.pytorch.org/).Multi-Head Attention is defined as:
where .
nn.MultiheadAttention
will use the optimized implementations ofscaled_dot_product_attention()
when possible.In addition to support for the new
scaled_dot_product_attention()
function, for speeding up Inference, MHA will use fastpath inference with support for Nested Tensors, iff:self attention is being computed (i.e.,
query
,key
, andvalue
are the same tensor).inputs are batched (3D) with
batch_first==True
Either autograd is disabled (using
torch.inference_mode
ortorch.no_grad
) or no tensor argumentrequires_grad
training is disabled (using
.eval()
)add_bias_kv
isFalse
add_zero_attn
isFalse
kdim
andvdim
are equal toembed_dim
if a
[NestedTensor](https://pytorch.org/docs/stable/nested.html)is passed, neitherkey_padding_mask
norattn_mask
is passedautocast is disabled
If the optimized inference fastpath implementation is in use, a
[NestedTensor](https://pytorch.org/docs/stable/nested.html)can be passed forquery
/key
/value
to represent padding more efficiently than using a padding mask. In this case, a[NestedTensor](https://pytorch.org/docs/stable/nested.html)will be returned, and an additional speedup proportional to the fraction of the input that is padding can be expected.- Parameters:
embed_dim – Total dimension of the model.
num_heads – Number of parallel attention heads. Note that
embed_dim
will be split acrossnum_heads
(i.e. each head will have dimensionembed_dim // num_heads
).dropout – Dropout probability on
attn_output_weights
. Default:0.0
(no dropout).bias – If specified, adds bias to input / output projection layers. Default:
True
.add_bias_kv – If specified, adds bias to the key and value sequences at dim=0. Default:
False
.add_zero_attn – If specified, adds a new batch of zeros to the key and value sequences at dim=1. Default:
False
.kdim – Total number of features for keys. Default:
None
(useskdim=embed_dim
).vdim – Total number of features for values. Default:
None
(usesvdim=embed_dim
).batch_first – If
True
, then the input and output tensors are provided as (batch, seq, feature). Default:False
(seq, batch, feature).
Examples:
>>> multihead_attn = nn.MultiheadAttention(embed_dim, num_heads) >>> attn_output, attn_output_weights = multihead_attn(query, key, value)
-
forward(query, key, value, key_padding_mask=None, need_weights=True, attn_mask=None, average_attn_weights=True, is_causal=False)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/nn/modules/activation.py#L1255)[#](#torch.nn.MultiheadAttention.forward) Compute attention outputs using query, key, and value embeddings.
Supports optional parameters for padding, masks and attention weights.
- Parameters:
query (
[Tensor](../tensors.html#torch.Tensor)) – Query embeddings of shape for unbatched input, whenbatch_first=False
or whenbatch_first=True
, where is the target sequence length, is the batch size, and is the query embedding dimensionembed_dim
. Queries are compared against key-value pairs to produce the output. See “Attention Is All You Need” for more details.key (
[Tensor](../tensors.html#torch.Tensor)) – Key embeddings of shape for unbatched input, whenbatch_first=False
or whenbatch_first=True
, where is the source sequence length, is the batch size, and is the key embedding dimensionkdim
. See “Attention Is All You Need” for more details.value (
[Tensor](../tensors.html#torch.Tensor)) – Value embeddings of shape for unbatched input, whenbatch_first=False
or whenbatch_first=True
, where is the source sequence length, is the batch size, and is the value embedding dimensionvdim
. See “Attention Is All You Need” for more details.key_padding_mask (
[Tensor](../tensors.html#torch.Tensor)| None) – If specified, a mask of shape indicating which elements withinkey
to ignore for the purpose of attention (i.e. treat as “padding”). For unbatched query, shape should be . Binary and float masks are supported. For a binary mask, aTrue
value indicates that the correspondingkey
value will be ignored for the purpose of attention. For a float mask, it will be directly added to the correspondingkey
value.need_weights (
[bool](https://docs.python.org/3/library/functions.html#bool)) – If specified, returnsattn_output_weights
in addition toattn_outputs
. Setneed_weights=False
to use the optimizedscaled_dot_product_attention
and achieve the best performance for MHA. Default:True
.attn_mask (
[Tensor](../tensors.html#torch.Tensor)| None) – If specified, a 2D or 3D mask preventing attention to certain positions. Must be of shape or , where is the batch size, is the target sequence length, and is the source sequence length. A 2D mask will be broadcasted across the batch while a 3D mask allows for a different mask for each entry in the batch. Binary and float masks are supported. For a binary mask, aTrue
value indicates that the corresponding position is not allowed to attend. For a float mask, the mask values will be added to the attention weight. If both attn_mask and key_padding_mask are supplied, their types should match.average_attn_weights (
[bool](https://docs.python.org/3/library/functions.html#bool)) – If true, indicates that the returnedattn_weights
should be averaged across heads. Otherwise,attn_weights
are provided separately per head. Note that this flag only has an effect whenneed_weights=True
. Default:True
(i.e. average weights across heads)is_causal (
[bool](https://docs.python.org/3/library/functions.html#bool)) – If specified, applies a causal mask as attention mask. Default:False
. Warning:is_causal
provides a hint thatattn_mask
is the causal mask. Providing incorrect hints can result in incorrect execution, including forward and backward compatibility.
- Return type:
- Outputs:
attn_output - Attention outputs of shape when input is unbatched, when
batch_first=False
or whenbatch_first=True
, where is the target sequence length, is the batch size, and is the embedding dimensionembed_dim
.attn_output_weights - Only returned when
need_weights=True
. Ifaverage_attn_weights=True
, returns attention weights averaged across heads of shape when input is unbatched or , where is the batch size, is the target sequence length, and is the source sequence length. Ifaverage_attn_weights=False
, returns attention weights per head of shape when input is unbatched or .
Note
batch_first argument is ignored for unbatched inputs.
-
merge_masks(attn_mask, key_padding_mask, query)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/nn/modules/activation.py#L1518)[#](#torch.nn.MultiheadAttention.merge_masks) Determine mask type and combine masks if necessary.
If only one mask is provided, that mask and the corresponding mask type will be returned. If both masks are provided, they will be both expanded to shape
(batch_size, num_heads, seq_len, seq_len)
, combined with logicalor
and mask type 2 will be returned :param attn_mask: attention mask of shape(seq_len, seq_len)
, mask type 0 :param key_padding_mask: padding mask of shape(batch_size, seq_len)
, mask type 1 :param query: query embeddings of shape(batch_size, seq_len, embed_dim)
- Returns:
merged mask mask_type: merged mask type (0, 1, or 2)
- Return type:
merged_mask