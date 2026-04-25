# Card: Transformers `generate()` — decoding controls & semantics
**Source:** https://huggingface.co/docs/transformers/main_classes/text_generation  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact parameter names/semantics for generation controls (length, beams, sampling, penalties) + strategy selection rules

## Key Content
- **Generation entry point:** `model.generate(inputs=None, generation_config=None, **kwargs)`; `kwargs` that match `GenerationConfig` fields override config.
- **Config loading priority:** if `generation_config` not passed: (1) `generation_config.json` in model repo (if exists) → (2) model config; remaining `None` fields filled by internal defaults during generation loop.
- **Length controls**
  - `max_new_tokens` (recommended): max tokens generated **ignoring prompt length**.
  - `max_length` (backward compat): total sequence length cap.
  - `min_new_tokens`: min tokens generated ignoring prompt length.
  - `min_length`: min total length; corresponds to `input_length + min_new_tokens`; overridden by `min_new_tokens` if set.
  - `stop_strings`: string or list of strings that terminate generation if output.
  - `max_time` (seconds): generation finishes current pass after time exceeded.
- **Strategy selection (procedural rules)**
  - Greedy: `num_beams=1` and `do_sample=False`
  - Multinomial sampling: `num_beams=1` and `do_sample=True`
  - Beam search: `num_beams>1` and `do_sample=False`
  - Beam + sampling: `num_beams>1` and `do_sample=True`
  - Assisted decoding: pass `assistant_model` or `prompt_lookup_num_tokens` to `.generate()`
- **Beam stopping:** `early_stopping=True` stops when `num_beams` complete candidates; `False` uses heuristic; `"never"` = canonical beam search (stop only when no better candidates possible).
- **Logits / decoding parameters (with documented defaults if unset in `generation_config.json`)**
  - `temperature` default **1.0**; scales next-token probabilities.
  - `top_k` default **50**; keep k highest-prob tokens.
  - `top_p` default **1.0**; keep smallest set with cumulative prob ≥ `top_p`.
  - `repetition_penalty`: **1.0 = no penalty**.
  - `length_penalty` (beam-based): score divided by `output_length ** length_penalty`; `>0` promotes longer, `<0` shorter.
- **Scoring reconstruction formula (beam example):**  
  **Eq. 1:** `sequence_score = sum(transition_scores) / (output_length ** length_penalty)`  
  where `transition_scores` are per-generated-token log-probs; `output_length` excludes input length.

## When to surface
Use when students ask how `max_length` differs from `max_new_tokens`, how to choose greedy vs sampling vs beam search, or what parameters like `top_k/top_p/temperature/length_penalty/early_stopping/repetition_penalty` *mean and default to* in Hugging Face Transformers.