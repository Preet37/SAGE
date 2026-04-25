# Card: Dagster op retry policies (RetryPolicy & RetryRequested)
**Source:** https://docs.dagster.io/guides/build/ops/op-retries  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Dagster op retry policy configuration (max_retries, delay/backoff/jitter) and retry behavior at the op boundary during job execution

## Key Content
- **Core behavior (Overview):** When an exception occurs during **op execution**, Dagster can **retry that op within the same job run** (retry happens at the **op boundary**, not by rerunning the whole job).
- **Two mechanisms (Relevant APIs / Using op retries):**
  - **Declarative:** attach `dagster.RetryPolicy` to an op (or job / invocation) so retries are requested automatically on exception.
  - **Manual:** raise `dagster.RetryRequested` from inside the op body to conditionally request a retry.
- **RetryPolicy parameters (Section “RetryPolicy”):**
  - `max_retries` = maximum retry attempts (example: `max_retries=3`)
  - `delay` = base delay between retries in seconds (example: `delay=0.2` → 200ms)
  - `backoff` modifies delay by attempt number (example enum: `Backoff.EXPONENTIAL`)
  - `jitter` adds randomness to delay (example enum: `Jitter.PLUS_MINUS`)
  - **Delay formula (Eq. 1, conceptual):** `wait_time(attempt) = f(delay, backoff, jitter, attempt_number)` where `backoff` scales with attempt and `jitter` perturbs the result.
- **Where to set policy (Section “RetryPolicy”):**
  1. On op definition: `@op(retry_policy=RetryPolicy(...))`
  2. On a specific invocation: `problematic.with_retry_policy(flakey_op_policy)()`
  3. On a job for all contained ops: `@job(op_retry_policy=default_policy)`
  - Example job-level defaults/overrides: `default_policy = RetryPolicy(max_retries=1)`, override op with `RetryPolicy(max_retries=10)`.
- **RetryRequested usage (Section “RetryRequested”):**
  - Pattern: `try/except` → `if should_retry(e): raise RetryRequested(max_retries=1, seconds_to_wait=1) from e`
  - `raise ... from e` preserves original exception info in Dagster.
- **Applies to asset jobs too:** `define_asset_job(..., op_retry_policy=RetryPolicy(max_retries=3))`.

## When to surface
Use when students ask how to configure retries in Dagster (per-op vs per-job), how to control retry count and timing (delay/backoff/jitter), or how to conditionally retry based on exception type using `RetryRequested`.