# Card: tf.keras.optimizers.AdamW (TensorFlow/Keras v2.16.1)
**Source:** https://www.tensorflow.org/api_docs/python/tf/keras/optimizers/AdamW  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact defaults + parameter semantics for AdamW (decoupled weight decay), incl. clipping, EMA, loss scaling, gradient accumulation, and excluding vars from weight decay.

## Key Content
- **Constructor + defaults (API signature):**  
  `tf.keras.optimizers.AdamW(learning_rate=0.001, weight_decay=0.004, beta_1=0.9, beta_2=0.999, epsilon=1e-07, amsgrad=False, clipnorm=None, clipvalue=None, global_clipnorm=None, use_ema=False, ema_momentum=0.99, ema_overwrite_frequency=None, loss_scale_factor=None, gradient_accumulation_steps=None, name='adamw', **kwargs)`
- **Algorithm identity / rationale:** AdamW = Adam (adaptive first/second moment estimates) **plus decoupled weight decay** per *Decoupled Weight Decay Regularization* (Loshchilov & Hutter et al., 2019). Adam described as computationally efficient, low memory, invariant to diagonal rescaling of gradients, suited to large data/parameter problems (Kingma et al., 2014).
- **EMA procedure (when `use_ema=True`):** maintains moving average of model weights:  
  **Eq. (EMA-1)** `new_average = ema_momentum * old_average + (1 - ema_momentum) * current_variable_value`  
  Defaults: `ema_momentum=0.99`.  
  `ema_overwrite_frequency`: every N steps overwrite model vars with moving average; if `None`, no mid-training overwrite; call `optimizer.finalize_variable_values()` at end (built-in `fit()` does this automatically after last epoch).
- **Gradient accumulation (`gradient_accumulation_steps=int`):** update model/optimizer variables every N steps using the **average** gradient since last update.
- **Mixed precision support (`loss_scale_factor`):** if float, multiply loss by factor before gradients; multiply gradients by inverse factor before updating.
- **Weight decay exclusions:** call `exclude_from_weight_decay(var_list=None, var_names=None)` **before** optimizer `build()`. `var_names` matches substrings (e.g., `['bias']` excludes all bias variables).
- **AMSGrad toggle:** `amsgrad=False` by default (Reddi et al., 2018 reference).

## When to surface
Use when students ask for **AdamW defaults**, how **decoupled weight decay** is configured in Keras, or how to use **EMA, clipping, loss scaling, gradient accumulation, or excluding biases/norm params from weight decay**.