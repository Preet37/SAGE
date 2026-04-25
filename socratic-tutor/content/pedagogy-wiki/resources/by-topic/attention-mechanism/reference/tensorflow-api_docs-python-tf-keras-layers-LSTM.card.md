# Source: https://www.tensorflow.org/api_docs/python/tf/keras/layers/LSTM
# Author: Keras Team
# Author Slug: keras-team
# Title: tf.keras.layers.LSTM — TensorFlow API docs (current)
# Fetched via: trafilatura
# Date: 2026-04-11

|
|
Long Short-Term Memory layer - Hochreiter 1997.
Inherits From: [ RNN](https://www.tensorflow.org/api_docs/python/tf/keras/layers/RNN),
[,](https://www.tensorflow.org/api_docs/python/tf/keras/Layer)
Layer
Operation
tf.keras.layers.LSTM(
units,
activation='tanh',
recurrent_activation='sigmoid',
use_bias=True,
kernel_initializer='glorot_uniform',
recurrent_initializer='orthogonal',
bias_initializer='zeros',
unit_forget_bias=True,
kernel_regularizer=None,
recurrent_regularizer=None,
bias_regularizer=None,
activity_regularizer=None,
kernel_constraint=None,
recurrent_constraint=None,
bias_constraint=None,
dropout=0.0,
recurrent_dropout=0.0,
seed=None,
return_sequences=False,
return_state=False,
go_backwards=False,
unroll=False,
use_cudnn='auto',
**kwargs
)
Used in the notebooks
| Used in the guide | Used in the tutorials |
|---|---|
Based on available runtime hardware and constraints, this layer will choose different implementations (cuDNN-based or backend-native) to maximize the performance. If a GPU is available and all the arguments to the layer meet the requirement of the cuDNN kernel (see below for details), the layer will use a fast cuDNN implementation when using the TensorFlow backend. The requirements to use the cuDNN implementation are:
activation
==tanh
recurrent_activation
==sigmoid
dropout
== 0 andrecurrent_dropout
== 0unroll
isFalse
use_bias
isTrue
- Inputs, if use masking, are strictly right-padded.
- Eager execution is enabled in the outermost context.
For example:
inputs = np.random.random((32, 10, 8))
lstm = keras.layers.LSTM(4)
output = lstm(inputs)
output.shape
(32, 4)
lstm = keras.layers.LSTM(
4, return_sequences=True, return_state=True)
whole_seq_output, final_memory_state, final_carry_state = lstm(inputs)
whole_seq_output.shape
(32, 10, 4)
final_memory_state.shape
(32, 4)
final_carry_state.shape
(32, 4)
Args | |
|---|---|
units
|
Positive integer, dimensionality of the output space. |
activation
|
Activation function to use.
Default: hyperbolic tangent (tanh ).
If you pass None , no activation is applied
(ie. "linear" activation: a(x) = x ).
|
recurrent_activation
|
Activation function to use
for the recurrent step.
Default: sigmoid (sigmoid ).
If you pass None , no activation is applied
(ie. "linear" activation: a(x) = x ).
|
use_bias
|
Boolean, (default True ), whether the layer
should use a bias vector.
|
kernel_initializer
|
Initializer for the kernel weights matrix,
used for the linear transformation of the inputs. Default:
"glorot_uniform" .
|
recurrent_initializer
|
Initializer for the recurrent_kernel
weights matrix, used for the linear transformation of the recurrent
|
bias_initializer
|
Initializer for the bias vector. Default: "zeros" .
|
unit_forget_bias
|
Boolean (default True ). If True ,
add 1 to the bias of the forget gate at initialization.
Setting it to True will also force bias_initializer="zeros" .
This is recommended in
|
kernel_regularizer
|
Regularizer function applied to the kernel weights
matrix. Default: None .
|
recurrent_regularizer
|
Regularizer function applied to the
recurrent_kernel weights matrix. Default: None .
|
bias_regularizer
|
Regularizer function applied to the bias vector.
Default: None .
|
activity_regularizer
|
Regularizer function applied to the output of the
layer (its "activation"). Default: None .
|
kernel_constraint
|
Constraint function applied to the kernel weights
matrix. Default: None .
|
recurrent_constraint
|
Constraint function applied to the
recurrent_kernel weights matrix. Default: None .
|
bias_constraint
|
Constraint function applied to the bias vector.
Default: None .
|
dropout
|
Float between 0 and 1. Fraction of the units to drop for the linear transformation of the inputs. Default: 0. |
recurrent_dropout
|
Float between 0 and 1. Fraction of the units to drop for the linear transformation of the recurrent state. Default: 0. |
seed
|
Random seed for dropout. |
return_sequences
|
Boolean. Whether to return the last output
in the output sequence, or the full sequence. Default: False .
|
return_state
|
Boolean. Whether to return the last state in addition
to the output. Default: False .
|
go_backwards
|
Boolean (default: False ).
If True , process the input sequence backwards and return the
reversed sequence.
|
|
Boolean (default: False ). If True , the last state
for each sample at index i in a batch will be used as initial
|
unroll
|
Boolean (default False).
If True , the network will be unrolled,
else a symbolic loop will be used.
Unrolling can speed-up a RNN,
although it tends to be more memory-intensive.
Unrolling is only suitable for short sequences.
|
use_cudnn
|
Whether to use a cuDNN-backed implementation. "auto" will
attempt to use cuDNN when feasible, and will fallback to the
default implementation if not.
|
Methods
from_config
@classmethod
from_config( config )
Creates a layer from its config.
This method is the reverse of get_config
,
capable of instantiating the same layer from the config
dictionary. It does not handle layer connectivity
(handled by Network), nor weights (handled by set_weights
).
| Args | |
|---|---|
config
|
A Python dictionary, typically the output of get_config. |
| Returns | |
|---|---|
| A layer instance. |
get_initial_state
get_initial_state(
batch_size
)
inner_loop
inner_loop(
sequences, initial_state, mask, training=False
)
reset_state
reset_state()
reset_states
reset_states()
symbolic_call
symbolic_call(
*args, **kwargs
)