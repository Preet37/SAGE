# Card: AWS Step Functions — Quotas & Limits (numeric feasibility)
**Source:** https://docs.aws.amazon.com/step-functions/latest/dg/limits.html  
**Role:** reference_doc | **Need:** API_REFERENCE / COMPARISON_DATA  
**Anchor:** Concrete numeric limits for Step Functions (payloads, timeouts, throttles, history size, retention)

## Key Content
- **Name constraints (General):** State machine / execution / activity task names **≤ 80 chars**, unique per account+Region; must not include whitespace, wildcards `? *`, brackets `< > { } [ ]`, many special chars (`" # % \ ^ | ~ \` $ & , ; : /`), or control chars (`\u0000-\u001f`, `\u007f-\u009f`). Non-ASCII allowed but can break CloudWatch logging (recommend ASCII).
- **Account quotas (selected):**
  - Registered state machines: **100,000** (increase to **150,000**).
  - Registered activities: **100,000** (increase to **150,000**).
  - State machine definition size: **1 MB (hard)**.
  - Step Functions API **max request size:** **1 MB per request (hard)** (includes headers + all request data).
  - **Open executions (Standard):** **1,000,000 per account per Region** (exceed → `ExecutionLimitExceeded`); **doesn’t apply to Express**.
  - Distributed Map: **open Map Runs max 1000 (hard)**; **parallel Map Run child executions max 10,000 (hard)**.
- **Execution/task hard limits (Standard vs Express):**
  - **Max execution time:** Standard **1 year**; Express **5 minutes**.
  - **Max execution history size:** Standard **25,000 events** (hit → execution fails).
  - **Max idle time:** Standard **1 year**; Express **5 minutes**.
  - **Execution history retention after close:** Standard **90 days** (can request reduction to **30 days**); Express **14 days**.
  - **Max input/output size (task/state/execution):** **256 KiB UTF-8 string** (both).
- **HTTP Task:** duration (request+response) **60 seconds (hard)**.
- **API throttling (token bucket; per account per Region; soft/increasable):**
  - `StartExecution` (Standard): bucket/refill **1300/300** (us-east-1, us-west-2, eu-west-1); **800/150** (other Regions).
  - `StartExecution` (Express): **6000/6000** (all Regions).
  - `RedriveExecution` (Standard): **1300/300** (key Regions); **800/150** (others).
  - `StopExecution` (Standard): **1000/200** (key Regions); **500/25** (others).
  - `GetActivityTask` (Standard): **3000/500** (key Regions); **1500/300** (others).
- **Versions/aliases:** published versions **1000 per state machine**; aliases **100 per state machine**.
- **Tagging (hard):** **50 tags/resource**; key **128** chars; value **256** chars; reserved prefix `aws:`.

## When to surface
Use when students ask whether Step Functions can handle a workload (throughput, payload size, long-running jobs, history growth, retention/compliance) or when comparing orchestration tools under concrete scaling/deployment constraints.