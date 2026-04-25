# Source: https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam
# Author: Keras Team
# Author Slug: keras-team
# Title: tf.keras.optimizers.Adam | TensorFlow v2.16.1
# Fetched via: trafilatura
# Date: 2026-04-09

|
|
Optimizer that implements the Adam algorithm.
Inherits From: Optimizer
tf.keras.optimizers.Adam(
learning_rate=0.001,
beta_1=0.9,
beta_2=0.999,
epsilon=1e-07,
amsgrad=False,
weight_decay=None,
clipnorm=None,
clipvalue=None,
global_clipnorm=None,
use_ema=False,
ema_momentum=0.99,
ema_overwrite_frequency=None,
loss_scale_factor=None,
gradient_accumulation_steps=None,
name='adam',
**kwargs
)
Used in the notebooks
| Used in the guide | Used in the tutorials |
|---|---|
Adam optimization is a stochastic gradient descent method that is based on adaptive estimation of first-order and second-order moments.
According to
[Kingma et al., 2014](http://arxiv.org/abs/1412.6980),
the method is "computationally
efficient, has little memory requirement, invariant to diagonal rescaling of
gradients, and is well suited for problems that are large in terms of
data/parameters".
Args | |
|---|---|
learning_rate
|
A float, a
keras.optimizers.schedules.LearningRateSchedule |
0.001
.
beta_1
0.9
.
beta_2
0.999
.
epsilon
1e-7
.
amsgrad
False
.
name
weight_decay
clipnorm
clipvalue
global_clipnorm
use_ema
False
.
If True
, exponential moving average
(EMA) is applied. EMA consists of computing an exponential moving
average of the weights of the model (as the weight values change
after each training batch), and periodically overwriting the
weights with their moving average.
ema_momentum
use_ema=True
.
This is the momentum to use when computing
the EMA of the model's weights:
new_average = ema_momentum * old_average + (1 - ema_momentum) *
current_variable_value
.
ema_overwrite_frequency
use_ema=True
. Every ema_overwrite_frequency
steps of iterations,
we overwrite the model variable by its moving average.
If None, the optimizer
does not overwrite model variables in the middle of training,
and you need to explicitly overwrite the variables
at the end of training by calling
optimizer.finalize_variable_values()
(which updates the model
variables in-place). When using the built-in fit()
training loop,
this happens automatically after the last epoch,
and you don't need to do anything.
loss_scale_factor
None
. If a float, the scale factor will
be multiplied the loss before computing gradients, and the inverse
of the scale factor will be multiplied by the gradients before
updating variables. Useful for preventing underflow during
mixed precision training. Alternately,
[will automatically set a loss scale factor.](https://www.tensorflow.org/api_docs/python/tf/keras/mixed_precision/LossScaleOptimizer)keras.optimizers.LossScaleOptimizer
gradient_accumulation_steps
None
. If an int, model & optimizer
variables will not be updated at every step; instead they will be
updated every gradient_accumulation_steps
steps, using the average
value of the gradients since the last update. This is known as
"gradient accumulation". This can be useful
when your batch size is very small, in order to reduce gradient
noise at each update step.
Attributes | |
|---|---|
learning_rate
|
|
variables
|
Methods
add_variable
add_variable(
shape,
initializer='zeros',
dtype=None,
aggregation='mean',
name=None
)
add_variable_from_reference
add_variable_from_reference(
reference_variable, name=None, initializer='zeros'
)
Add an all-zeros variable with the shape and dtype of a reference variable.
apply
apply(
grads, trainable_variables=None
)
Update traininable variables according to provided gradient values.
grads
should be a list of gradient tensors
with 1:1 mapping to the list of variables the optimizer was built with.
trainable_variables
can be provided
on the first call to build the optimizer.
apply_gradients
apply_gradients(
grads_and_vars
)
assign
assign(
variable, value
)
Assign a value to a variable.
This should be used in optimizers instead of variable.assign(value)
to
support backend specific optimizations.
Note that the variable can be a model variable or an optimizer variable;
it can be a backend native variable or a Keras variable.
| Args | |
|---|---|
variable
|
The variable to update. |
value
|
The value to add to the variable. |
assign_add
assign_add(
variable, value
)
Add a value to a variable.
This should be used in optimizers instead of
variable.assign_add(value)
to support backend specific optimizations.
Note that the variable can be a model variable or an optimizer variable;
it can be a backend native variable or a Keras variable.
| Args | |
|---|---|
variable
|
The variable to update. |
value
|
The value to add to the variable. |
assign_sub
assign_sub(
variable, value
)
Subtract a value from a variable.
This should be used in optimizers instead of
variable.assign_sub(value)
to support backend specific optimizations.
Note that the variable can be a model variable or an optimizer variable;
it can be a backend native variable or a Keras variable.
| Args | |
|---|---|
variable
|
The variable to update. |
value
|
The value to add to the variable. |
build
build(
var_list
)
Initialize optimizer variables.
Adam optimizer has 3 types of variables: momentums, velocities and velocity_hat (only set when amsgrad is applied),
| Args | |
|---|---|
var_list
|
list of model variables to build Adam variables on. |
exclude_from_weight_decay
exclude_from_weight_decay(
var_list=None, var_names=None
)
Exclude variables from weight decay.
This method must be called before the optimizer's build
method is
called. You can set specific variables to exclude out, or set a list of
strings as the anchor words, if any of which appear in a variable's
name, then the variable is excluded.
| Args | |
|---|---|
var_list
|
A list of Variable s to exclude from weight decay.
|
var_names
|
A list of strings. If any string in var_names appear
in the model variable's name, then this model variable is
excluded from weight decay. For example, var_names=['bias']
excludes all bias variables from weight decay.
|
finalize_variable_values
finalize_variable_values(
var_list
)
Set the final value of model's trainable variables.
Sometimes there are some extra steps before ending the variable updates, such as overriding the model variables with its average value.
| Args | |
|---|---|
var_list
|
list of model variables. |
from_config
@classmethod
from_config( config, custom_objects=None )
Creates an optimizer from its config.
This method is the reverse of get_config
, capable of instantiating the
same optimizer from the config dictionary.
| Args | |
|---|---|
config
|
A Python dictionary, typically the output of get_config. |
custom_objects
|
A Python dictionary mapping names to additional user-defined Python objects needed to recreate this optimizer. |
| Returns | |
|---|---|
| An optimizer instance. |
get_config
get_config()
Returns the config of the optimizer.
An optimizer config is a Python dictionary (serializable) containing the configuration of an optimizer. The same optimizer can be reinstantiated later (without any saved state) from this configuration.
Subclass optimizer should override this method to include other hyperparameters.
| Returns | |
|---|---|
| Python dictionary. |
load_own_variables
load_own_variables(
store
)
Set the state of this optimizer object.
save_own_variables
save_own_variables(
store
)
Get the state of this optimizer object.
scale_loss
scale_loss(
loss
)
Scale the loss before computing gradients.
Scales the loss before gradients are computed in a train_step
. This
is primarily useful during mixed precision training to prevent numeric
underflow.
set_weights
set_weights(
weights
)
Set the weights of the optimizer.
optimizer_variables, grads, trainable_variables
)
update_step
update_step(
gradient, variable, learning_rate
)
Update step given gradient and the associated model variable.