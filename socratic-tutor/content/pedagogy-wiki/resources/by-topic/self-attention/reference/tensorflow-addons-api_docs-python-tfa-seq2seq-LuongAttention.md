# Source: https://www.tensorflow.org/addons/api_docs/python/tfa/seq2seq/LuongAttention
# Title: tfa.seq2seq.LuongAttention - Addons
# Fetched via: trafilatura
# Date: 2026-04-09

tf.keras.layers.Attention
Stay organized with collections
Save and categorize content based on your preferences.
Dot-product attention layer, a.k.a. Luong-style attention.
Inherits From: Layer
, Operation
tf.keras.layers.Attention(
use_scale=False,
score_mode='dot',
dropout=0.0,
seed=None,
**kwargs
)
Inputs are a list with 2 or 3 elements:
- A
query
tensor of shape (batch_size, Tq, dim)
.
- A
value
tensor of shape (batch_size, Tv, dim)
.
- A optional
key
tensor of shape (batch_size, Tv, dim)
. If none
supplied, value
will be used as a key
.
The calculation follows the steps:
- Calculate attention scores using
query
and key
with shape
(batch_size, Tq, Tv)
.
- Use scores to calculate a softmax distribution with shape
(batch_size, Tq, Tv)
.
- Use the softmax distribution to create a linear combination of
value
with shape (batch_size, Tq, dim)
.
Args |
use_scale
|
If True , will create a scalar variable to scale the
attention scores.
|
dropout
|
Float between 0 and 1. Fraction of the units to drop for the
attention scores. Defaults to 0.0 .
|
seed
|
A Python integer to use as random seed incase of dropout .
|
score_mode
|
Function to use to compute attention scores, one of
{"dot", "concat"} . "dot" refers to the dot product between the
query and key vectors. "concat" refers to the hyperbolic tangent
of the concatenation of the query and key vectors.
|
Call Args |
inputs
|
List of the following tensors:
query : Query tensor of shape (batch_size, Tq, dim) .
value : Value tensor of shape (batch_size, Tv, dim) .
key : Optional key tensor of shape (batch_size, Tv, dim) . If
not given, will use value for both key and value , which is
the most common case.
|
mask
|
List of the following tensors:
query_mask : A boolean mask tensor of shape (batch_size, Tq) .
If given, the output will be zero at the positions where
mask==False .
value_mask : A boolean mask tensor of shape (batch_size, Tv) .
If given, will apply the mask such that values at positions
where mask==False do not contribute to the result.
|
return_attention_scores
|
bool, it True , returns the attention scores
(after masking and softmax) as an additional output argument.
|
training
|
Python boolean indicating whether the layer should behave in
training mode (adding dropout) or in inference mode (no dropout).
|
use_causal_mask
|
Boolean. Set to True for decoder self-attention. Adds
a mask such that position i cannot attend to positions j > i .
This prevents the flow of information from the future towards the
past. Defaults to False .
|
Output |
Attention outputs of shape (batch_size, Tq, dim) .
(Optional) Attention scores after masking and softmax with shape
(batch_size, Tq, Tv) .
|
Attributes |
input
|
Retrieves the input tensor(s) of a symbolic operation.
Only returns the tensor(s) corresponding to the first time
the operation was called.
|
output
|
Retrieves the output tensor(s) of a layer.
Only returns the tensor(s) corresponding to the first time
the operation was called.
|
Methods
from_config
[View source](https://github.com/keras-team/keras/tree/v3.3.3/keras/src/ops/operation.py#L191-L213)
@classmethod
from_config(
config
)
Creates a layer from its config.
This method is the reverse of get_config
,
capable of instantiating the same layer from the config
dictionary. It does not handle layer connectivity
(handled by Network), nor weights (handled by set_weights
).
| Args |
config
|
A Python dictionary, typically the
output of get_config.
|
| Returns |
|
A layer instance.
|
symbolic_call
[View source](https://github.com/keras-team/keras/tree/v3.3.3/keras/src/ops/operation.py#L58-L70)
symbolic_call(
*args, **kwargs
)
Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates. Some content is licensed under the [numpy license](https://numpy.org/doc/stable/license.html).
Last updated 2024-06-07 UTC.
[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Missing the information I need","missingTheInformationINeed","thumb-down"],["Too complicated / too many steps","tooComplicatedTooManySteps","thumb-down"],["Out of date","outOfDate","thumb-down"],["Samples / code issue","samplesCodeIssue","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2024-06-07 UTC."],[],[]]