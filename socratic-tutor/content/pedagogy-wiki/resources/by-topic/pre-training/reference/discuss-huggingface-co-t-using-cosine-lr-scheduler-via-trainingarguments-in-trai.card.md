# Card: Trainer LR scheduler knobs (cosine, restarts, custom)
**Source:** https://discuss.huggingface.co/t/using-cosine-lr-scheduler-via-trainingarguments-in-trainer/14783/8  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact `Trainer`/`TrainingArguments` knobs for scheduler selection + how to override with a custom scheduler

## Key Content
- **Built-in scheduler selection via `TrainingArguments`:**
  - Set `lr_scheduler_type = "cosine_with_restarts"` to use cosine annealing with restarts.
  - Pass scheduler-specific parameters via `lr_scheduler_kwargs`, e.g.  
    - `lr_scheduler_kwargs = {"num_cycles": 5}` (controls number of cosine restart cycles).
- **Custom scheduler when built-ins don’t fit (e.g., don’t decay to 0):**
  - HF core maintainer guidance: *“You can pass your own learning rate scheduler to the `Trainer`.”* (used when you want a different final LR such as 50% of peak).
- **Manual cosine-with-warmup scheduler wiring (procedure):**
  1. Create optimizer (example shown: `PagedAdamW_32bit(model.parameters())`).
  2. Create `Trainer(..., optimizers=(optimizer, None))`.
  3. Build scheduler with Transformers helper:  
     - `scheduler = get_cosine_schedule_with_warmup(optimizer, num_warmup_steps=training_args.warmup_steps, num_training_steps=...)`
  4. Attach it: `trainer.lr_scheduler = scheduler` **or** pass directly: `Trainer(..., optimizers=(optimizer, lr_scheduler))`.
- **Training step count used in examples:**
  - `num_warmup_steps = int(max_steps * warmup_ratio)`
  - `num_training_steps = max_steps` (explicitly set in `TrainingArguments(max_steps=...)`).

## When to surface
Use when a student asks how to enable cosine (or cosine-with-restarts) LR scheduling in `Trainer`, how to pass `num_cycles`, or how to override the scheduler (e.g., avoid decaying LR to 0).