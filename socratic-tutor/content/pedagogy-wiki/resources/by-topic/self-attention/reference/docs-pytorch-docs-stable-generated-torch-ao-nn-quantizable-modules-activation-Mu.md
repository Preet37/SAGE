# Source: https://docs.pytorch.org/docs/stable/generated/torch.ao.nn.quantizable.modules.activation.MultiheadAttention.html
# Title: MultiheadAttention — PyTorch 2.11 documentation
# Fetched via: trafilatura
# Date: 2026-04-11

MultiheadAttention[#](#multiheadattention)
-
class torch.ao.nn.quantizable.modules.activation.MultiheadAttention(embed_dim, num_heads, dropout=0.0, bias=True, add_bias_kv=False, add_zero_attn=False, kdim=None, vdim=None, batch_first=False, device=None, dtype=None)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/ao/nn/quantizable/modules/activation.py#L13)[#](#torch.ao.nn.quantizable.modules.activation.MultiheadAttention) -
dequantize()
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/ao/nn/quantizable/modules/activation.py#L198)[#](#torch.ao.nn.quantizable.modules.activation.MultiheadAttention.dequantize) Utility to convert the quantized MHA back to float.
The motivation for this is that it is not trivial to convert the weights from the format that is used in the quantized version back to the float.
-
forward(query, key, value, key_padding_mask=None, need_weights=True, attn_mask=None, average_attn_weights=True, is_causal=False)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/ao/nn/quantizable/modules/activation.py#L297)[#](#torch.ao.nn.quantizable.modules.activation.MultiheadAttention.forward) - Note::
Please, refer to
for more informationforward()
- Parameters:
query (
[Tensor](../tensors.html#torch.Tensor)) – map a query and a set of key-value pairs to an output. See “Attention Is All You Need” for more details.key (
[Tensor](../tensors.html#torch.Tensor)) – map a query and a set of key-value pairs to an output. See “Attention Is All You Need” for more details.value (
[Tensor](../tensors.html#torch.Tensor)) – map a query and a set of key-value pairs to an output. See “Attention Is All You Need” for more details.key_padding_mask (
[Tensor](../tensors.html#torch.Tensor)| None) – if provided, specified padding elements in the key will be ignored by the attention. When given a binary mask and a value is True, the corresponding value on the attention layer will be ignored.need_weights (
[bool](https://docs.python.org/3/library/functions.html#bool)) – output attn_output_weights.attn_mask (
[Tensor](../tensors.html#torch.Tensor)| None) – 2D or 3D mask that prevents attention to certain positions. A 2D mask will be broadcasted for all the batches while a 3D mask allows to specify a different mask for the entries of each batch.
- Return type:
- Shape:
Inputs:
query: where L is the target sequence length, N is the batch size, E is the embedding dimension. if
batch_first
isTrue
.key: , where S is the source sequence length, N is the batch size, E is the embedding dimension. if
batch_first
isTrue
.value: where S is the source sequence length, N is the batch size, E is the embedding dimension. if
batch_first
isTrue
.key_padding_mask: where N is the batch size, S is the source sequence length. If a BoolTensor is provided, the positions with the value of
True
will be ignored while the position with the value ofFalse
will be unchanged.attn_mask: 2D mask where L is the target sequence length, S is the source sequence length. 3D mask where N is the batch size, L is the target sequence length, S is the source sequence length. attn_mask ensure that position i is allowed to attend the unmasked positions. If a BoolTensor is provided, positions with
True
is not allowed to attend whileFalse
values will be unchanged. If a FloatTensor is provided, it will be added to the attention weight.is_causal: If specified, applies a causal mask as attention mask. Mutually exclusive with providing attn_mask. Default:
False
.average_attn_weights: If true, indicates that the returned
attn_weights
should be averaged across heads. Otherwise,attn_weights
are provided separately per head. Note that this flag only has an effect whenneed_weights=True.
. Default: True (i.e. average weights across heads)Outputs:
attn_output: where L is the target sequence length, N is the batch size, E is the embedding dimension. if
batch_first
isTrue
.attn_output_weights: If
average_attn_weights=True
, returns attention weights averaged across heads of shape , where N is the batch size, L is the target sequence length, S is the source sequence length. Ifaverage_attn_weights=False
, returns attention weights per head of shape .
-
dequantize()