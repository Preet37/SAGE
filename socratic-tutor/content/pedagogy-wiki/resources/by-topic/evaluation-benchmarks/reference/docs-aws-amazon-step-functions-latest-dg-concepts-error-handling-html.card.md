# Card: AWS Step Functions Retry/Catch Semantics (Error Handling)
**Source:** https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Retry fields (IntervalSeconds, MaxAttempts, BackoffRate) and Catch behavior; error names and propagation rules

## Key Content
- **Default behavior:** When a state reports an error, Step Functions **fails the entire execution** unless handled via **Retry/Catch**.
- **Where Catch/Retry apply:** Available on **Task, Parallel, Map** states (not for **top-level execution failures**). For anticipated execution-level failures: handle in caller, **nest child workflows**, or listen for **TIMED_OUT** events (Standard) via EventBridge.
- **Error names (case-sensitive strings):**
  - Built-ins start with `States.`; custom errors **cannot** start with `States.`.
  - Wildcards:  
    - `States.ALL` matches any known error name but **must appear alone** and **last** in `ErrorEquals`; **cannot catch** `States.DataLimitExceeded` or `States.Runtime`.  
    - `States.TaskFailed` matches any known error **except** `States.Timeout`.
  - Notable errors:  
    - `States.Timeout`: task timeout or heartbeat missed; if nested SM throws `States.Timeout`, parent receives `States.TaskFailed`. Also emitted when execution exceeds `TimeoutSeconds`.  
    - `States.Runtime`: non-retriable; **always fails**; not caught by `Retry/Catch` on `States.ALL`.  
    - `States.DataLimitExceeded`: terminal; not caught by `States.ALL`.
- **Retry algorithm (ordered scan):** On error, Step Functions scans `Retry[]` in order; first retrier whose `ErrorEquals` contains the error governs retries. If retries exhausted, normal error handling continues.
- **Retry timing formula (Eq. 1):** delay before attempt *k* (1-indexed)  
  `Delay_k = IntervalSeconds * (BackoffRate)^(k-1)` capped by `MaxDelaySeconds` if set; with `JitterStrategy=FULL`, delay is randomized in `[0, Delay_k]`.
- **Retry defaults/limits:** `IntervalSeconds=1` (max `99999999`), `MaxAttempts=3` (0 = never retry; max `99999999`), `BackoffRate=2.0`, `JitterStrategy=NONE`, `MaxDelaySeconds` optional (0 < value < `31622401`).
- **Catch algorithm (ordered scan):** If no Retry or retries fail, scan `Catch[]` in order; first matching catcher transitions to `Next`. `ResultPath` controls whether error output overwrites input (`$` default) or is merged.
- **Billing note:** Retries count as **state transitions**.

## When to surface
Use when students ask how Step Functions decides **which retry/catch runs**, how **timeouts/runtime/data-limit** errors propagate, or how to compute **exponential backoff/jitter** and defaults.