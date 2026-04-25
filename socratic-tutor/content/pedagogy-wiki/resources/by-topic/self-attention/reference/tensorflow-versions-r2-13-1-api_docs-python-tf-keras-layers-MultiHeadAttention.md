# Source: https://www.tensorflow.org/versions/r2.13.1/api_docs/python/tf/keras/layers/MultiHeadAttention
# Author: Keras Team
# Author Slug: keras-team
# Title: tf.keras.layers.MultiHeadAttention (TensorFlow v2.13.1 API docs)
# Fetched via: search
# Date: 2026-04-11

# tf.keras.layers.MultiHeadAttention
View source on GitHub
MultiHeadAttention layer.
Inherits From: `Layer`, `Operation`
```
tf.keras.layers.MultiHeadAttention(
num_heads,
key_dim,
value_dim=None,
dropout=0.0,
use_bias=True,
output_shape=None,
attention_axes=None,
kernel_initializer='glorot_uniform',
bias_initializer='zeros',
kernel_regularizer=None,
bias_regularizer=None,
activity_regularizer=None,
kernel_constraint=None,
bias_constraint=None,
**kwargs
)
```
### Used in the notebooks
...
This is an implementation of multi-headed attention as described in the
paper "Attention is all you Need"
Vaswani et al., 2017.
If `query`, `key,` `value` are the same, then
this is self-attention.
Each timestep in `query` attends to the
corresponding sequence in `key`, and returns a fixed-width vector.
This layer first projects `query`, `key` and `value`.
These are
(effectively) a list of tensors of length `num_attention_heads`, where the
corresponding shapes are `(batch_size, <query dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, value_dim)`.
Then, the query and key tensors are dot-producted and scaled.
These are
softmaxed to obtain attention probabilities.
The value tensors are then
interpolated by these probabilities, then concatenated back to a single
tensor.
Finally, the result tensor with the last dimension as `value_dim` can take
a linear projection and return.
|## Args|## Args|
|--|--|
|`num_heads`|Number of attention heads.|
|`key_dim`|Size of each attention head for query and key.|
|`value_dim`|Size of each attention head for value.|
|`dropout`|Dropout probability.|
|`use_bias`|Boolean, whether the dense layers use bias vectors/matrices.|
|`output_shape`|The expected shape of an output tensor, besides the batch and sequence dims.
If not specified, projects back to the query feature dim (the query input's last dimension).|
|`attention_axes`|axes over which the attention is applied.
`None` means attention over all axes, but batch, heads, and features.|
|`kernel_initializer`|Initializer for dense layer kernels.|
|`bias_initializer`|Initializer for dense layer biases.|
|`kernel_regularizer`|Regularizer for dense layer kernels.|
|`bias_regularizer`|Regularizer for dense layer biases.|
|`activity_regularizer`|Regularizer for dense layer activity.|
|`kernel_constraint`|Constraint for dense layer kernels.|
|`bias_constraint`|Constraint for dense layer kernels.|
|## Call arguments|## Call arguments|
|--|--|
|`query`|Query tensor of shape `(B, T, dim)`, where `B` is the batch size, `T` is the target sequence length, and dim is the feature dimension.|
|`value`|Value tensor of shape `(B, S, dim)`, where `B` is the batch size, `S` is the source sequence length, and dim is the feature dimension.|
|`key`|Optional key tensor of shape `(B, S, dim)`.
If not given, will use `value` for both `key` and `value`, which is the most common case.|
|`attention_mask`|a boolean mask of shape `(B, T, S)`, that prevents attention to certain positions.
The boolean mask specifies which query elements can attend to which key elements, 1 indicates attention and 0 indicates no attention.
Broadcasting can happen for the missing batch dimensions and the head dimension.|
|`return_attention_scores`|A boolean to indicate whether the output should be `(attention_output, attention_scores)` if `True`, or `attention_output` if `False`.
Defaults to `False`.|
|`training`|Python boolean indicating whether the layer should behave in training mode (adding dropout) or in inference mode (no dropout).
Will go with either using the training mode of the parent layer/model, or `False` (inference) if there is no parent layer.|
|`use_causal_mask`|A boolean to indicate whether to apply a causal mask to prevent tokens from attending to future tokens (e.g., used in a decoder Transformer).|
|## Returns|## Returns|
|--|--|
|`attention_output`|The result of the computation, of shape `(B, T, E)`, where `T` is for target sequence shapes and `E` is the query input last dimension if `output_shape` is `None`.
Otherwise, the multi-head outputs are projected to the shape specified by `output_shape`.|
|`attention_scores`|(Optional) multi-head attention coefficients over attention axes.|
|## Attributes|## Attributes|
|--|--|
|`attention_axes`| |
|`dropout`| |
|`input`|Retrieves the input tensor(s) of a symbolic operation.
Only returns the tensor(s) corresponding to the *first time* the operation was called.|
|`key_dense`| |
|`key_dim`| |
|`num_heads`| |
|`output`|Retrieves the output tensor(s) of a layer.
Only returns the tensor(s) corresponding to the *first time* the operation was called.|
|`output_dense`| |
|`output_shape`| |
|`query_dense`| |
|`use_bias`| |
...
@classmethod
from_config(
config
)
```
Creates a layer from its config.
This method is the reverse of `get_config`,
capable of instantiating the same layer from the config
dictionary.
It does not handle layer connectivity
(handled by Network), nor weights (handled by `set_weights`).
|Args|Args|
|--|--|
|`config`|A Python dictionary, typically the output of get_config.|
|Returns|Returns|
|--|--|
|A layer instance.|A layer instance.|
### symbolic_call
View source
```
symbolic_call(
*args, **kwargs
)
```
Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License.

None
► Keras 3 API documentation / Layers API / Attention layers / MultiHeadAttention layer
…
### MultiHeadAttention class
```
keras.layers.MultiHeadAttention(
num_heads,
key_dim,
value_dim=None,
dropout=0.0,
use_bias=True,
output_shape=None,
attention_axes=None,
flash_attention=None,
kernel_initializer="glorot_uniform",
bias_initializer="zeros",
kernel_regularizer=None,
bias_regularizer=None,
activity_regularizer=None,
kernel_constraint=None,
bias_constraint=None,
use_gate=False,
seed=None,
**kwargs
)
```
MultiHeadAttention layer.
This is an implementation of multi-headed attention as described in the
paper "Attention is all you Need"
Vaswani et al., 2017.
If `query`, `key,` `value` are the same, then
this is self-attention.
Each timestep in `query` attends to the
corresponding sequence in `key`, and returns a fixed-width vector.
This layer first projects `query`, `key` and `value`.
These are
(effectively) a list of tensors of length `num_attention_heads`, where the
corresponding shapes are `(batch_size, <query dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, value_dim)`.
Then, the query and key tensors are dot-producted and scaled.
These are
softmaxed to obtain attention probabilities.
The value tensors are then
interpolated by these probabilities, then concatenated back to a single
tensor.
Finally, the result tensor with the last dimension as `value_dim` can take
a linear projection and return.
…
- **num_heads**: Number of attention heads.
- **key_dim**: Size of each attention head for query and key.
- **value_dim**: Size of each attention head for value.
- **dropout**: Dropout probability.
- **use_bias**: Boolean, whether the dense layers use bias vectors/matrices.
- **output_shape**: The expected shape of an output tensor, besides the batch and sequence dims.
If not specified, projects back to the query feature dim (the query input's last dimension).
- **attention_axes**: axes over which the attention is applied.
`None` means
attention over all axes, but batch, heads, and features.
- **flash_attention**: If `None`, the layer attempts to use flash
attention for faster and more memory-efficient attention
computations when possible.
This behavior can be configured using
`keras.config.enable_flash_attention()` or
`keras.config.disable_flash_attention()`.
- **kernel_initializer**: Initializer for dense layer kernels.
- **bias_initializer**: Initializer for dense layer biases.
- **kernel_regularizer**: Regularizer for dense layer kernels.
- **bias_regularizer**: Regularizer for dense layer biases.
- **activity_regularizer**: Regularizer for dense layer activity.
- **kernel_constraint**: Constraint for dense layer kernels.
- **bias_constraint**: Constraint for dense layer kernels.
- **use_gate**: Boolean, whether to apply a gated attention mechanism.
When True, an additional gating branch is added based on the (Gated Attention for Large Language Models)[https://arxiv.org/abs/2505.06708].
It applies a sigmoid-activated linear projection to the query which then gates the attention output.
This helps improve training stability and eliminates "attention sinks".
- **seed**: Optional integer to seed the dropout layer.
**Call arguments**
- **query**: Query tensor of shape `(B, T, dim)`, where `B` is the batch size,
`T` is the target sequence length, and dim is the feature dimension.
- **value**: Value tensor of shape `(B, S, dim)`, where `B` is the batch size,
`S` is the source sequence length, and dim is the feature dimension.
- **key**: Optional key tensor of shape `(B, S, dim)`.
If not given, will
use `value` for both `key` and `value`, which is the most common
case.
- **attention_mask**: a boolean mask of shape `(B, T, S)`, that prevents
attention to certain positions.
The boolean mask specifies which
query elements can attend to which key elements, 1 indicates
attention and 0 indicates no attention.
Broadcasting can happen for
the missing batch dimensions and the head dimension.
- **return_attention_scores**: A boolean to indicate whether the output should be `(attention_output, attention_scores)` if `True`, or
`attention_output` if `False`.
Defaults to `False`.
- **training**: Python boolean indicating whether the layer should behave in training mode (adding dropout) or in inference mode (no dropout).
Will go with either using the training mode of the parent layer/model, or `False` (inference) if there is no parent layer.
- **use_causal_mask**: A boolean to indicate whether to apply a causal mask to prevent tokens from attending to future tokens (e.g., used in a decoder Transformer).
**Returns**
- **attention_output**: The result of the computation, of shape `(B, T, E)`,
where `T` is for target sequence shapes and `E` is the query input
last dimension if `output_shape` is `None`.
Otherwise, the
multi-head outputs are projected to the shape specified by
`output_shape`.
- **attention_scores**: (Optional) multi-head attention coefficients over attention axes.
**Guides and examples using `MultiHeadAttention`**
- Named Entity Recognition using Transformers

# layer_multi_head_attention
## MultiHeadAttention layer
## Description
This is an implementation of multi-headed attention based on “Attention is all you Need”.
If query, key, value are the same, then this is self-attention.
Each timestep in query attends to the corresponding sequence in key, and returns a fixed-width vector.
## Usage
```
layer_multi_head_attention(
inputs,
num_heads,
key_dim, value_dim = NULL,
dropout = 0,
use_bias = TRUE,
output_shape = NULL,
attention_axes = NULL,
kernel_initializer = "glorot_uniform",
bias_initializer = "zeros",
kernel_regularizer = NULL,
bias_regularizer = NULL,
activity_regularizer = NULL,
kernel_constraint = NULL,
bias_constraint = NULL,
...
)
```
## Arguments
|Arguments|Description|
|--|--|
|inputs|a list of inputs first should be the query tensor, the second the value tensor|
|num_heads|Number of attention heads.|
|key_dim|Size of each attention head for query and key.|
|value_dim|Size of each attention head for value.|
|dropout|Dropout probability.|
|use_bias|Boolean, whether the dense layers use bias vectors/matrices.|
|output_shape|The expected shape of an output tensor, besides the batch and sequence dims.
If not specified, projects back to the key feature dim.|
|attention_axes|axes over which the attention is applied.
None means attention over all axes, but batch, heads, and features.|
|kernel_initializer|Initializer for dense layer kernels.|
|bias_initializer|Initializer for dense layer biases.|
|kernel_regularizer|Regularizer for dense layer kernels.|
|bias_regularizer|Regularizer for dense layer biases.|
|activity_regularizer|Regularizer for dense layer activity.|
|kernel_constraint|Constraint for dense layer kernels.|
|bias_constraint|Constraint for dense layer kernels.|
|…|Other arguments passed to the layer.
Eg, `name`, `training`.|
## Details
This layer first projects query, key and value.
These are (effectively) a list of tensors of length num_attention_heads, where the corresponding shapes are
`[batch_size, , key_dim]`,
`[batch_size, , key_dim]`,
`[batch_size, , value_dim]`.
Then, the query and key tensors are dot-producted and scaled.
These are softmaxed to obtain attention probabilities.
The value tensors are then interpolated by these probabilities, then concatenated back to a single tensor.
Finally, the result tensor with the last dimension as value_dim can take an linear projection and return.
## Section
## Call arguments
query: Query Tensor of shape
`[B, T, dim]`.
value: Value Tensor of shape
`[B, S, dim]`.
key: Optional key Tensor of shape
`[B, S, dim]`.
If not given, will use value for both key and value, which is the most common case.
attention_mask: a boolean mask of shape
`[B, T, S]`, that prevents attention to certain positions.
return_attention_scores: A boolean to indicate whether the output should be attention output if TRUE, or (attention_output, attention_scores) if FALSE.
Defaults to FALSE.
training: Python boolean indicating whether the layer should behave in training mode (adding dropout) or in inference mode (no dropout).
Defaults to either using the training mode of the parent layer/model, or FALSE (inference) if there is no parent layer.
## Value
attention_output: The result of the computation, of shape
`[B, T, E]`, where T is for target sequence shapes and E is the query input last dimension if output_shape is None.
Otherwise, the multi-head outputs are project to the shape specified by output_shape.
attention_scores: (Optional) multi-head attention coeffients over attention axes.

# tf.keras.layers.MultiHeadAttention
View source on GitHub
MultiHeadAttention layer.
Inherits From: `Layer`, `Operation`
```
tf.keras.layers.MultiHeadAttention(
num_heads,
key_dim,
value_dim=None,
dropout=0.0,
use_bias=True,
output_shape=None,
attention_axes=None,
kernel_initializer='glorot_uniform',
bias_initializer='zeros',
kernel_regularizer=None,
bias_regularizer=None,
activity_regularizer=None,
kernel_constraint=None,
bias_constraint=None,
**kwargs
)
```
### Used in the notebooks
...
This is an implementation of multi-headed attention as described in the
paper "Attention is all you Need"
Vaswani et al., 2017.
If `query`, `key,` `value` are the same, then
this is self-attention.
Each timestep in `query` attends to the
corresponding sequence in `key`, and returns a fixed-width vector.
This layer first projects `query`, `key` and `value`.
These are
(effectively) a list of tensors of length `num_attention_heads`, where the
corresponding shapes are `(batch_size, <query dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, value_dim)`.
Then, the query and key tensors are dot-producted and scaled.
These are
softmaxed to obtain attention probabilities.
The value tensors are then
interpolated by these probabilities, then concatenated back to a single
tensor.
Finally, the result tensor with the last dimension as `value_dim` can take
a linear projection and return.
|## Args|## Args|
|--|--|
|`num_heads`|Number of attention heads.|
|`key_dim`|Size of each attention head for query and key.|
|`value_dim`|Size of each attention head for value.|
|`dropout`|Dropout probability.|
|`use_bias`|Boolean, whether the dense layers use bias vectors/matrices.|
|`output_shape`|The expected shape of an output tensor, besides the batch and sequence dims.
If not specified, projects back to the query feature dim (the query input's last dimension).|
|`attention_axes`|axes over which the attention is applied.
`None` means attention over all axes, but batch, heads, and features.|
|`kernel_initializer`|Initializer for dense layer kernels.|
|`bias_initializer`|Initializer for dense layer biases.|
|`kernel_regularizer`|Regularizer for dense layer kernels.|
|`bias_regularizer`|Regularizer for dense layer biases.|
|`activity_regularizer`|Regularizer for dense layer activity.|
|`kernel_constraint`|Constraint for dense layer kernels.|
|`bias_constraint`|Constraint for dense layer kernels.|
|## Call arguments|## Call arguments|
|--|--|
|`query`|Query tensor of shape `(B, T, dim)`, where `B` is the batch size, `T` is the target sequence length, and dim is the feature dimension.|
|`value`|Value tensor of shape `(B, S, dim)`, where `B` is the batch size, `S` is the source sequence length, and dim is the feature dimension.|
|`key`|Optional key tensor of shape `(B, S, dim)`.
If not given, will use `value` for both `key` and `value`, which is the most common case.|
|`attention_mask`|a boolean mask of shape `(B, T, S)`, that prevents attention to certain positions.
The boolean mask specifies which query elements can attend to which key elements, 1 indicates attention and 0 indicates no attention.
Broadcasting can happen for the missing batch dimensions and the head dimension.|
|`return_attention_scores`|A boolean to indicate whether the output should be `(attention_output, attention_scores)` if `True`, or `attention_output` if `False`.
Defaults to `False`.|
|`training`|Python boolean indicating whether the layer should behave in training mode (adding dropout) or in inference mode (no dropout).
Will go with either using the training mode of the parent layer/model, or `False` (inference) if there is no parent layer.|
|`use_causal_mask`|A boolean to indicate whether to apply a causal mask to prevent tokens from attending to future tokens (e.g., used in a decoder Transformer).|
|## Returns|## Returns|
|--|--|
|`attention_output`|The result of the computation, of shape `(B, T, E)`, where `T` is for target sequence shapes and `E` is the query input last dimension if `output_shape` is `None`.
Otherwise, the multi-head outputs are projected to the shape specified by `output_shape`.|
|`attention_scores`|(Optional) multi-head attention coefficients over attention axes.|
|## Attributes|## Attributes|
|--|--|
|`attention_axes`| |
|`dropout`| |
|`input`|Retrieves the input tensor(s) of a symbolic operation.
Only returns the tensor(s) corresponding to the *first time* the operation was called.|
|`key_dense`| |
|`key_dim`| |
|`num_heads`| |
|`output`|Retrieves the output tensor(s) of a layer.
Only returns the tensor(s) corresponding to the *first time* the operation was called.|
|`output_dense`| |
|`output_shape`| |
|`query_dense`| |
|`use_bias`| |
...
@classmethod
from_config(
config
)
```
Creates a layer from its config.
This method is the reverse of `get_config`,
capable of instantiating the same layer from the config
dictionary.
It does not handle layer connectivity
(handled by Network), nor weights (handled by `set_weights`).
|Args|Args|
|--|--|
|`config`|A Python dictionary, typically the output of get_config.|
|Returns|Returns|
|--|--|
|A layer instance.|A layer instance.|
### symbolic_call
View source
```
symbolic_call(
*args, **kwargs
)
```
Except as otherwise noted, the content of this page is licensed under the Creative Commons Attribution 4.0 License, and code samples are licensed under the Apache 2.0 License.

None
► Keras 2 API documentation / Layers API / Attention layers / MultiHeadAttention layer
…
### MultiHeadAttention class
```
tf_keras.layers.MultiHeadAttention(
num_heads,
key_dim,
value_dim=None,
dropout=0.0,
use_bias=True,
output_shape=None,
attention_axes=None,
kernel_initializer="glorot_uniform",
bias_initializer="zeros",
kernel_regularizer=None,
bias_regularizer=None,
activity_regularizer=None,
kernel_constraint=None,
bias_constraint=None,
**kwargs
)
```
MultiHeadAttention layer.
This is an implementation of multi-headed attention as described in the
paper "Attention is all you Need" (Vaswani et al., 2017).
If `query`, `key,` `value` are the same, then
this is self-attention.
Each timestep in `query` attends to the
corresponding sequence in `key`, and returns a fixed-width vector.
This layer first projects `query`, `key` and `value`.
These are
(effectively) a list of tensors of length `num_attention_heads`, where the
corresponding shapes are `(batch_size, <query dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, key_dim)`,
`(batch_size, <key/value dimensions>, value_dim)`.
Then, the query and key tensors are dot-producted and scaled.
These are
softmaxed to obtain attention probabilities.
The value tensors are then
interpolated by these probabilities, then concatenated back to a single
tensor.
Finally, the result tensor with the last dimension as value_dim can take an
linear projection and return.
When using `MultiHeadAttention` inside a custom layer, the custom layer must
implement its own `build()` method and call `MultiHeadAttention`'s
`_build_from_signature()` there.
This enables weights to be restored correctly when the model is loaded.
**Examples**
Performs 1D cross-attention over two sequence inputs with an attention mask.
Returns the additional attention weights over heads.
```
>>> layer = MultiHeadAttention(num_heads=2, key_dim=2)
>>> target = tf.keras.Input(shape=[8, 16])
>>> source = tf.keras.Input(shape=[4, 16])
>>> output_tensor, weights = layer(target, source,
...
return_attention_scores=True)
>>> print(output_tensor.shape)
(None, 8, 16)
>>> print(weights.shape)
(None, 2, 8, 4)
```
Performs 2D self-attention over a 5D input tensor on axes 2 and 3.
```
>>> layer = MultiHeadAttention(
...
num_heads=2, key_dim=2, attention_axes=(2, 3))
>>> input_tensor = tf.keras.Input(shape=[5, 3, 4, 16])
>>> output_tensor = layer(input_tensor, input_tensor)
>>> print(output_tensor.shape)
(None, 5, 3, 4, 16)
```
…
- **num_heads**: Number of attention heads.
- **key_dim**: Size of each attention head for query and key.
- **value_dim**: Size of each attention head for value.
- **dropout**: Dropout probability.
- **use_bias**: Boolean, whether the dense layers use bias vectors/matrices.
- **output_shape**: The expected shape of an output tensor, besides the batch and sequence dims.
If not specified, projects back to the query feature dim (the query input's last dimension).
- **attention_axes**: axes over which the attention is applied.
`None` means
attention over all axes, but batch, heads, and features.
- **kernel_initializer**: Initializer for dense layer kernels.
- **bias_initializer**: Initializer for dense layer biases.
- **kernel_regularizer**: Regularizer for dense layer kernels.
- **bias_regularizer**: Regularizer for dense layer biases.
- **activity_regularizer**: Regularizer for dense layer activity.
- **kernel_constraint**: Constraint for dense layer kernels.
- **bias_constraint**: Constraint for dense layer kernels.
**Call arguments**
- **query**: Query `Tensor` of shape `(B, T, dim)`.
- **value**: Value `Tensor` of shape `(B, S, dim)`.
- **key**: Optional key `Tensor` of shape `(B, S, dim)`.
If not given, will
use `value` for both `key` and `value`, which is the most common
case.
- **attention_mask**: a boolean mask of shape `(B, T, S)`, that prevents
attention to certain positions.
The boolean mask specifies which
query elements can attend to which key elements, 1 indicates
attention and 0 indicates no attention.
Broadcasting can happen for
the missing batch dimensions and the head dimension.
- **return_attention_scores**: A boolean to indicate whether the output should be `(attention_output, attention_scores)` if `True`, or
`attention_output` if `False`.
Defaults to `False`.
- **training**: Python boolean indicating whether the layer should behave in training mode (adding dropout) or in inference mode (no dropout).
Will go with either using the training mode of the parent layer/model, or False (inference) if there is no parent layer.
- **use_causal_mask**: A boolean to indicate whether to apply a causal mask to prevent tokens from attending to future tokens (e.g., used in a decoder Transformer).
**Returns**
- **attention_output**: The result of the computation, of shape `(B, T, E)`,
where `T` is for target sequence shapes and `E` is the query input
last dimension if `output_shape` is `None`.
Otherwise, the
multi-head outputs are projected to the shape specified by
`output_shape`.
- **attention_scores**: [Optional] multi-head attention coefficients over attention axes.