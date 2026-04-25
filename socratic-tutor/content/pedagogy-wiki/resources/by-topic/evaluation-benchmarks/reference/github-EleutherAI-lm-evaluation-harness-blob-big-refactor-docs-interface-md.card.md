# Card: lm-eval Harness Interface (CLI + Python API)
**Source:** https://github.com/EleutherAI/lm-evaluation-harness/blob/big-refactor/docs/interface.md  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** CLI argument surface + equivalent `simple_evaluate()` kwargs for standardized eval runs

## Key Content
- **Primary invocation:** run via `python -m lm_eval` or `lm-eval` CLI entrypoint; flags viewable with `-h/--help`.
- **Model selection**
  - `--model <string>`: model type/provider name (must match enabled names list in main README).
  - `--model_args "arg1=val1,arg2=val2,..."`: comma-separated kwargs passed to model constructor (example: `pretrained=EleutherAI/pythia-160m,dtype=float32`).
- **Task selection & prompting**
  - `--tasks "t1,t2,group1,..."`: comma-separated task and/or task-group names (must be valid).
  - `--num_fewshot <int>`: number of few-shot examples inserted into context.
- **Generation controls**
  - `--gen_kwargs "k=v,..."`: kwargs passed to `generate_until` tasks (e.g., `temperature`, `top_p`, `top_k`); applies to **all** `generate_until` tasks in the run (no per-task overrides via CLI; per-task control via task YAML).
- **Batching & device**
  - `--batch_size <int|auto|auto:N>`: fixed batch size or auto-fit; `auto:N` re-finds max batch size **N times** during eval (helps because docs are sorted by descending context length).
  - `--max_batch_size <int>`: cap when using `--batch_size auto`.
  - `--device <string>`: e.g., `cuda` (default), `cuda:0`, `cpu`, `mps`.
- **Outputs & observability**
  - `--output_path dir/file.jsonl|dir/`: save high-level results; if `--log_samples`, also saves per-document outputs/metrics into directory.
  - `--log_samples`: requires `--output_path`; logs model inputs/outputs per document.
- **Debugging/repro**
  - `--limit <int|float 0.0–1.0>`: evaluate first X docs or first X% per task.
  - `--use_cache /path/to/sqlite_cache_`: creates per-process caches `/path/to/sqlite_cache_rank{i}.db`.
  - `--check_integrity`: run task tests.
  - `--write_out`: print prompt + gold target for first doc of each task.
  - `--show_config`: print full `TaskConfig` (incl. non-default YAML settings).
  - `--include_path <folder>`: add external YAML task configs to registry.
- **Python API workflow**
  1. Implement an `lm_eval.api.model.LM` subclass (`loglikelihood`, `loglikelihood_rolling`, `generate_until`).
  2. Register tasks: `lm_eval.tasks.initialize_tasks()` or `include_path(...)`.
  3. Call `lm_eval.simple_evaluate(model=lm_obj, tasks=[...], num_fewshot=..., ...)` (kwargs mirror CLI flags).
  - `lm_eval.evaluate()` provides core functionality with less abstraction than `simple_evaluate()`.

## When to surface
Use when students ask how to run standardized benchmark evaluations (CLI flags, batching, logging, caching, task selection) or how to reproduce the same settings via `simple_evaluate()` in code.