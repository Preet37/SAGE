# Card: tf.keras.optimizers.Adam (TensorFlow/Keras v2.16.1)
**Source:** https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/Adam  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact Adam constructor parameters + defaults (lr, betas, epsilon, amsgrad, weight_decay, clipping, EMA, loss scaling, grad accumulation)

## Key Content
- **What Adam is (per Kingma et al., 2014):** SGD method using adaptive estimates of **1st and 2nd moments**; described as computationally efficient, low memory, invariant to diagonal rescaling of gradients, suited to large data/parameter problems.
- **Constructor + defaults (TensorFlow 2.16.1):**  
  `tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, weight_decay=None, clipnorm=None, clipvalue=None, global_clipnorm=None, use_ema=False, ema_momentum=0.99, ema_overwrite_frequency=None, loss_scale_factor=None, gradient_accumulation_steps=None, name='adam', **kwargs)`
- **EMA procedure (when `use_ema=True`):**  
  **Eq. 1 (EMA update):** `new_average = ema_momentum * old_average + (1 - ema_momentum) * current_variable_value`  
  - `ema_overwrite_frequency`: every N steps, overwrite model variables with moving average.  
  - If `None`: no mid-training overwrite; call `optimizer.finalize_variable_values()` at end (built-in `fit()` does this automatically after last epoch).
- **Gradient accumulation (when `gradient_accumulation_steps=int`):** update model/optimizer variables **every N steps** using the **average gradient** since last update (reduces gradient noise for very small batch sizes).
- **Loss scaling (mixed precision):** if `loss_scale_factor` is float: multiply loss by factor before gradients; multiply gradients by inverse factor before applying updates.

## When to surface
Use when students ask for **Adam hyperparameter defaults**, how to configure **epsilon/betas/amsgrad**, or how Keras Adam handles **EMA, gradient clipping, weight decay, loss scaling, or gradient accumulation**.