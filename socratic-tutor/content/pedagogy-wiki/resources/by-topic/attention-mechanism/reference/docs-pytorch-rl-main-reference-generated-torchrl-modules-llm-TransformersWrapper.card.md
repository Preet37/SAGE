# Card: TorchRL `TransformersWrapper` decoding & generation knobs
**Source:** https://docs.pytorch.org/rl/main/reference/generated/torchrl.modules.llm.TransformersWrapper.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact generation/inference parameter semantics for decoding knobs (standardized args + conflict rules)

## Key Content
- **What it is:** `torchrl.modules.llm.TransformersWrapper` wraps Hugging Face `AutoModelForCausalLM` models to provide a consistent interface for **text generation** and **log-probability computation**.
- **Packing vs Padding (design rationale):**
  - **Packing** (`pad_model_input=False`): more memory efficient for variable-length sequences; requires custom attention masks/position ids; not all HF models support it; **only usable when `generate=False`**.
  - **Padding** (`pad_model_input=True`, default): universally supported; wastes memory for short sequences; simplest/most compatible.
- **Core toggles:**
  - `generate` (bool, default **True**): if True, calls model generation; if False, computes log-probs only.
  - `return_log_probs` (bool, default **False**): include log-prob outputs.
  - `generate_kwargs` (dict): forwarded to HF `.generate()`.
- **Standardized (cross-backend) generation parameters (semantics):**
  - `max_new_tokens` (int): max number of **new** tokens to generate.
  - `num_return_sequences` (int): number of sequences returned.
  - `temperature` (float): sampling temperature (**0.0 = deterministic**, higher = more random).
  - `top_p` (float): nucleus sampling in **[0.0, 1.0]**.
  - `top_k` (int): top-k sampling.
  - `repetition_penalty` (float): penalize repeating tokens.
  - `do_sample` (bool): sampling vs greedy decoding.
  - `num_beams` (int): beam search beams.
  - `length_penalty` (float): length penalty in beam search.
  - `early_stopping` (bool): stop early in beam search.
  - `stop_sequences` (list): stop strings (custom stopping criteria).
  - `skip_special_tokens` (bool): omit special tokens in decoded output.
  - `logprobs` (bool): return log-probs (maps to `output_scores`); **discouraged** because it may conflict with class `generate`.
- **Legacy mapping + conflict rule:**
  - `max_tokens` → `max_new_tokens`; `n` → `num_return_sequences`.
  - If both legacy and standardized names are provided (e.g., `max_tokens` and `max_new_tokens`), **raises `ValueError`**.
- **Sampling count constraint:** `num_samples` (int|None) can also be set via `generate_kwargs["num_return_sequences"]`; **requires** `generate_kwargs["do_sample"]=True`.

## When to surface
Use when students ask what decoding parameters mean (e.g., `top_p`, `temperature`, `num_beams`, `max_new_tokens`), how TorchRL standardizes them across backends, or why generation settings may error due to legacy/standard name conflicts.