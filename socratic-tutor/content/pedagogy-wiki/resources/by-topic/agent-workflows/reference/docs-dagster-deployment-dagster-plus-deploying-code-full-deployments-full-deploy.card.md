# Card: Dagster+ run-level retries (full deployment settings)
**Source:** https://docs.dagster.io/deployment/dagster-plus/deploying-code/full-deployments/full-deployment-settings-reference  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Run-level retry configuration in Dagster+ deployment settings; boundary vs op/asset-level retries

## Key Content
- **Where configured:** Full deployment settings are **YAML**. Run retries live under `run_retries:` (Section “Run retries”).
- **Core parameter (Eq. 1 — Run retry cap):**  
  `max_run_retry_attempts = run_retries.max_retries`  
  - **Definition:** Maximum number of times Dagster+ will attempt to retry a **failed run**.  
  - **Default:** `0` (no run retries).  
  - **Behavior:** If `run_retries.max_retries` is **undefined**, Dagster+ uses its default.
- **Failure-scope toggle (boundary vs op/asset retries):** `run_retries.retry_on_asset_or_op_failure`  
  - **Meaning:** Whether to retry runs that failed because **assets or ops** in the run failed.  
  - **Rationale:** Set to `false` to **only** retry failures due to the **run worker crashing/unexpectedly terminating**, and rely on **op/asset-level retry policies** for op/asset failures (explicit separation of concerns: run-level vs op/asset-level).  
  - **Version gate:** Setting this to `false` changes behavior only on **Dagster version ≥ 1.6.7**.
- **Example snippet:**  
  ```yaml
  run_retries:
    max_retries: 0
  ```
- **Related operational defaults (often confused with retries):** `run_monitoring.start_timeout_seconds: 1200`, `cancel_timeout_seconds: 1200`, `max_runtime_seconds: 7200` (timeouts affect run state transitions, not retry count).

## When to surface
Use when students ask how to configure **automatic retries of entire Dagster runs** in Dagster+ deployments, or how run-level retries differ from **op/asset retry policies** and worker-crash retry behavior.