# Card: Durable Human-in-the-Loop with Temporal (Signals, Waits, Queries)
**Source:** https://learn.temporal.io/tutorials/ai/building-durable-ai-applications/human-in-the-loop/  
**Role:** explainer | **Need:** COMPARISON_DATA  
**Anchor:** Step-by-step mechanics for durable approval gates (signals + wait_condition + query) with retry-safe state persistence.

## Key Content
- **Core rationale (durability for HITL):**
  - Human decisions are **durably stored in Workflow history**; after crashes/timeouts, the Workflow **resumes without re-asking** for approval.
  - `workflow.wait_condition(...)` pauses without consuming CPU; Temporal records the “waiting” checkpoint and resumes only when condition becomes true.

- **Signal data model (Step 1):**
  - `UserDecision = {KEEP, EDIT, WAIT}` (enum).
  - `UserDecisionSignal(decision: UserDecision, additional_prompt: str="")` (dataclass).

- **Workflow state persistence (Step 2):**
  - Instance vars persist across execution/replay:
    - `_current_prompt: str`
    - `_user_decision: UserDecisionSignal = UserDecisionSignal(decision=WAIT)`
    - (for queries) `_research_result: str = ""`

- **Signal handler (Step 3):**
  - `@workflow.signal async def user_decision_signal(decision_data): self._user_decision = decision_data`

- **Approval/edit loop (Step 4 + waiting):**
  - Loop:
    1) `research_facts = execute_activity(llm_call, start_to_close_timeout=30s)`
    2) Store for query: `_research_result = research_facts["choices"][0]["message"]["content"]`
    3) **Gate:** `await workflow.wait_condition(lambda: _user_decision.decision != WAIT)`
    4) If `KEEP`: exit loop → `create_pdf` activity (`start_to_close_timeout=20s`)
    5) If `EDIT`: append `additional_prompt` to `_current_prompt`, set `llm_call_input.prompt`, then **reset** `_user_decision = WAIT` and repeat.

- **Query support:**
  - `@workflow.query def get_research_result(self)->str: return _research_result`
  - Queries are synchronous read-only; **do not create history events**; can query during/after completion.

- **Client interactions:**
  - `handle = client.get_workflow_handle(workflow_id)`
  - Send signal: `await handle.signal("user_decision_signal", UserDecisionSignal(decision=KEEP|EDIT,...))`
  - Query: `await handle.query(GenerateReportWorkflow.get_research_result)`

## When to surface
Use when students ask how to implement **durable human approval/feedback gates**, **pause/resume** agent workflows safely, or compare Temporal Signals/Queries + wait conditions to interrupt/resume patterns (e.g., LangGraph).