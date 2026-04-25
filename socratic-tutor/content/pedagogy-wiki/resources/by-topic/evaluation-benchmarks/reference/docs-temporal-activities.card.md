# Card: Temporal Activity Retries — RetryPolicy defaults & backoff
**Source:** https://docs.temporal.io/activities#activity-retries  
**Role:** reference_doc | **Need:** [COMPARISON_DATA] / [API_REFERENCE]  
**Anchor:** Exact RetryPolicy fields + default retry behavior (Activities vs Workflows)

## Key Content
- **Default retry behavior**
  - **Activities retry automatically by default** with exponential backoff until **success or cancellation**.
  - **Workflow Executions do not retry by default** (no default Retry Policy attached).
  - **Retry Policies do not apply to Workflow Task Executions**; Workflow Tasks retry until Workflow Execution Timeout (unlimited by default) with exponential backoff and **max interval 10 minutes**.
- **RetryPolicy fields (exact names)**
  - `initialInterval`, `backoffCoefficient`, `maximumInterval`, `maximumAttempts`, `nonRetryableErrorTypes`.
- **Default RetryPolicy values (Properties → Default values)**
  - `initialInterval` = **1s**
  - `backoffCoefficient` = **2.0**
  - `maximumInterval` = **100 × initialInterval** (=> **100s** with defaults)
  - `maximumAttempts` = **∞** (unlimited); **0 also means unlimited**, **1 means no retries**, negative => error
  - `nonRetryableErrorTypes` = **[]** (none)
- **Retry interval formula (Retry interval section, Eq. 1)**
  - `retryInterval = min( initialInterval * (backoffCoefficient ^ retries), maximumInterval )`
  - where `retries` = number of retries already attempted (0 for first retry delay).
- **Procedure: what happens on Activity retry**
  1. Activity fails → service evaluates Retry Policy (attempt count, error type) and computes backoff.
  2. If retryable: schedules a new Activity Task after backoff (new Activity Task Execution).
  3. If not retryable / attempts exceeded: Activity fails and error is returned.
- **Override mechanism**
  - An **Application Failure** can set a **“next Retry delay”** that overrides the computed interval, but still respects `maximumAttempts` and overall timeouts (Activity **Schedule-to-Close**, Workflow **Execution Timeout**).
- **Design rationale**
  - Prefer retrying **failed Activities** (failure-prone external ops) vs retrying whole Workflows (deterministic replay; retrying often repeats same failure and wastes resources).

## When to surface
Use when students ask how Temporal retries Activities, what the default backoff/limits are, what each RetryPolicy parameter means, or why Workflows don’t retry by default.