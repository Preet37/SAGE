# Card: Runner.run & RunConfig (OpenAI Agents SDK, Python)
**Source:** https://openai.github.io/openai-agents-python/ref/run/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Canonical runner signatures, accepted input types, and multi-turn lifecycle semantics

## Key Content
- **Canonical async runner signature (Runner.run):**  
  `await Runner.run(starting_agent, input, *, context=None, max_turns=DEFAULT_MAX_TURNS, hooks=None, run_config=None, error_handlers=None, previous_response_id=None, auto_previous_response_id=False, conversation_id=None, session=None) -> RunResult`
  - **Input types:** `input ∈ { str | list[TResponseInputItem] | RunState[TContext] }`
  - **starting_agent:** `Agent[TContext]` (required)

- **Lifecycle loop (workflow semantics):**  
  1) Invoke agent with given input  
  2) **Stop condition:** if agent produces **final output** of type `agent.output_type`  
  3) If **handoff** occurs: repeat loop with the new agent  
  4) Else: execute **tool calls** (if any), then re-run loop

- **Turn definition / limit:**  
  `max_turns` counts **one AI invocation per turn**, **including tool calls**.

- **Exceptions (unless handled):**  
  - `MaxTurnsExceeded` when `max_turns` exceeded  
  - `GuardrailTripwireTriggered` when a guardrail tripwire triggers  
  - **Guardrail note:** *Only the first agent’s input guardrails are run.*

- **Multi-turn / state parameters:**  
  - `previous_response_id`: Responses API optimization to avoid resending prior-turn input  
  - `conversation_id`: uses Responses API conversation state; runner reads/writes items; recommended only if exclusively using OpenAI models (other providers won’t write to Conversation)  
  - `session`: automatic conversation history management

- **Sync + streaming variants:**  
  - `Runner.run_sync(...)`: wraps `run`; won’t work inside an existing event loop (e.g., Jupyter/async frameworks).  
  - `Runner.run_streamed(...) -> RunResultStreaming`: provides method to stream semantic events.

- **RunConfig key overrides (global):**  
  - `model`: overrides every agent’s model  
  - `model_provider`: resolves string model names (default: OpenAI via `MultiProvider`)  
  - `model_settings`: non-null values override agent-specific settings  
  - `input_guardrails` (initial input), `output_guardrails` (final output)  
  - `handoff_input_filter` (global; per-handoff filter takes precedence)  
  - `nest_handoff_history` (beta, default False) + `handoff_history_mapper` (used when nesting True)  
  - `call_model_input_filter` (edit model input pre-call), `tool_error_formatter`  
  - tracing controls: `tracing_disabled`, `tracing`, `workflow_name`, `trace_id`, `group_id`, `trace_metadata`, `trace_include_sensitive_data`  
  - `reasoning_item_id_policy`: `None/"preserve"` keeps IDs; `"omit"` strips IDs

## When to surface
Use when students ask how OpenAI Agents SDK runs multi-turn workflows (handoffs/tools), what `Runner.run` accepts/returns, or how to manage conversation state (`conversation_id`, `session`, `previous_response_id`) and global run overrides via `RunConfig`.