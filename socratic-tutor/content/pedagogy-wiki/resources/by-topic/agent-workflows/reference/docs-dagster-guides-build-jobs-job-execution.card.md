# Card: Dagster job execution + per-run concurrency controls
**Source:** https://docs.dagster.io/guides/build/jobs/job-execution  
**Role:** reference_doc | **Need:** API_REFERENCE (concurrency/executor controls for workflow steps)  
**Anchor:** Run executor configuration knobs (e.g., `max_concurrent`, `tag_concurrency_limits`) and how steps are scheduled within a run

## Key Content
- **Default execution behavior**
  - By default, Dagster runs jobs with **`multiprocess_executor`**: each step runs in its **own process**, and **independent steps can run in parallel**.
- **Execution entry points (procedures)**
  - **UI:** Launchpad → **Launch Run**; includes config editor for runtime config.
  - **CLI:** `dg launch --jobs my_job` (launches asynchronously via the instance run launcher).
  - **Python:** `JobDefinition.execute_in_process()` returns `ExecuteInProcessResult`.
- **Executor configuration (per-run)**
  - Each `JobDefinition` has an `executor_def` (an `ExecutorDefinition`) controlling isolation/parallelism (in-process ↔ multiprocess ↔ k8s pods, etc.).
  - **Toggle to in-process via run config YAML:**
    ```yaml
    execution:
      config:
        in_process:
    ```
- **Multiprocess knobs (defaults/parameters)**
  - `max_concurrent`: limits **max concurrent subprocesses** within a run.
    - Example sets **`max_concurrent: 4`**.
  - `start_method`: controls subprocess spawn method; example uses **`forkserver`** to reduce per-process overhead.
- **Op-level concurrency limits (per-run)**
  - `tag_concurrency_limits`: caps concurrent ops matching a **tag key** or **key-value**; if launching an op would exceed a limit, it **stays queued**.
  - Example: overall **`max_concurrent: 4`**, plus at most **2** ops with tag `database=redshift`:
    ```yaml
    tag_concurrency_limits:
      - key: database
        value: redshift
        limit: 2
    ```
  - Applies **per-run only**; cross-run limits via `celery_executor` / `celery_k8s_job_executor`.

## When to surface
Use when students ask how Dagster schedules steps within a run, how to cap parallelism (`max_concurrent`), or how to throttle specific classes of ops via tag-based concurrency limits.