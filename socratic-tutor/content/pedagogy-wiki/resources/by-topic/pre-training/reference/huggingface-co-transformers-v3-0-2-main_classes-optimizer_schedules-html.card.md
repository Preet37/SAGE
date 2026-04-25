# Card: Transformers v3.0.2 Optimization (AdamW + LR Schedules)
**Source:** https://www.huggingface.co/transformers/v3.0.2/main_classes/optimizer_schedules.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact `transformers.AdamW` defaults + official LR scheduler APIs (PyTorch/TensorFlow)

## Key Content
- **AdamW (PyTorch) API + defaults** (Section “AdamW (PyTorch)”):  
  `transformers.AdamW(params, lr=0.001, betas=(0.9, 0.999), eps=1e-6, weight_decay=0.0, correct_bias=True)`  
  - `lr`: learning rate (default **1e-3**)  
  - `betas=(b1,b2)`: Adam momentum coefficients (default **(0.9, 0.999)**)  
  - `eps`: numerical stability (default **1e-6**)  
  - `weight_decay`: **decoupled** weight decay (default **0.0**)  
  - `correct_bias`: bias correction toggle (default **True**; BERT TF repo uses **False**)  
  - **Rationale:** “weight decay fix” per *Decoupled Weight Decay Regularization* (decay does not interact with Adam’s m/v states).

- **AdamWeightDecay (TensorFlow) defaults**:  
  `learning_rate=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-7, amsgrad=False, weight_decay_rate=0.0`  
  - **Rationale:** adding L2 penalty to loss is *not* correct for Adam; use decoupled decay (equivalent to L2 with plain SGD).

- **TF helper: `create_optimizer` workflow**: warmup → linear decay schedule.  
  `create_optimizer(init_lr, num_train_steps, num_warmup_steps, min_lr_ratio=0.0, adam_epsilon=1e-8, weight_decay_rate=0.0, include_in_weight_decay=None)`  
  - Final LR at end: **init_lr * min_lr_ratio**.

- **PyTorch LR schedulers (return `torch.optim.lr_scheduler.LambdaLR`)**:  
  - `get_constant_schedule(optimizer, last_epoch=-1)`  
  - `get_constant_schedule_with_warmup(optimizer, num_warmup_steps, last_epoch=-1)` (linear warmup 0 → base lr)  
  - `get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, last_epoch=-1)` (warmup then linear decay to 0)  
  - `get_cosine_schedule_with_warmup(..., num_cycles=0.5)` (half-cosine to 0)  
  - `get_cosine_with_hard_restarts_schedule_with_warmup(..., num_cycles=1)` (cosine with hard restarts)

## When to surface
Use when students ask for **exact AdamW defaults**, **why decoupled weight decay**, or **which Hugging Face scheduler function** matches “warmup + linear/cosine decay” in PyTorch/TensorFlow.