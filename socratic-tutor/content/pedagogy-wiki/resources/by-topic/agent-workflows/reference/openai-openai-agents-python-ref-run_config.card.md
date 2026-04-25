# Card: OpenAI Agents SDK (Python) — RunConfig & RunOptions
**Source:** https://openai.github.io/openai-agents-python/ref/run_config/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact `RunConfig` fields + runtime hooks/tracing/session/handoff controls; `RunOptions` chaining + error handlers.

## Key Content
- **RunConfig (dataclass): config for an entire agent run**
  - **Model selection**
    - `model: str | Model | None = None` — if set, **overrides every agent’s model**; `model_provider` must resolve string names.
    - `model_provider: ModelProvider = MultiProvider()` — default provider (docs: “Defaults to OpenAI”).
    - `model_settings: ModelSettings | None` — **non-null values override agent-specific** model settings.
  - **Handoffs**
    - `handoff_input_filter: HandoffInputFilter | None` — global filter for all handoffs; **per-handoff filter takes precedence**.
    - `nest_handoff_history` — **default disabled**; when `True`, wraps prior run history into **one assistant message** before handoff if no custom filter.
    - `handoff_history_mapper: HandoffHistoryMapper | None` — runs **only when** `nest_handoff_history=True`; maps normalized transcript → history passed to next agent. If `None`, runner collapses transcript into one assistant message.
  - **Guardrails**
    - `input_guardrails: list[InputGuardrail] | None` — run on **initial** run input.
    - `output_guardrails: list[OutputGuardrail] | None` — run on **final** run output.
  - **Tracing/telemetry knobs**
    - `tracing_disabled` — disables tracing entirely.
    - `tracing: TracingConfig | None`
    - `trace_include_sensitive_data` — if `False`, spans exist but **tool/LLM inputs/outputs omitted**.
    - `workflow_name`, `trace_id` (custom), `group_id` (link traces), `trace_metadata` (dict).
  - **Session/memory**
    - `session_input_callback: SessionInputCallback | None` — default: **append new input** to session history; custom callback can merge history+input.
    - `session_settings: SessionSettings | None` — non-null overrides session defaults (e.g., retrieval item count).
  - **Pre-model/tool hooks**
    - `call_model_input_filter(agent, context, ModelInputData) -> ModelInputData` — invoked **immediately before** model call; can edit instructions/items (e.g., token limits, add system prompt).
    - `tool_error_formatter(ToolErrorFormatterArgs) -> str | None` — format tool errors; `None` uses SDK default.
  - **Reasoning item IDs**
    - `reasoning_item_id_policy: None/"preserve"|"omit"` — preserve IDs or strip them from next-turn model input.

- **RunOptions (TypedDict): arguments for AgentRunner methods**
  - `previous_response_id`, `auto_previous_response_id` (auto chaining first turn), `conversation_id`
  - `error_handlers: RunErrorHandlers | None` keyed by error kind; currently supports **`max_turns`**.

## When to surface
Use when students ask how OpenAI Agents SDK controls runtime behavior (model override, handoff transcript shaping, tracing privacy, session history handling, pre-model hooks, or response chaining/error handling like `max_turns`).