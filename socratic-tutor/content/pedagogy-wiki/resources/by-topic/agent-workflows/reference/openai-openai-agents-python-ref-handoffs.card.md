# Card: Typed Handoffs (Supervisor → Sub-agent) in OpenAI Agents SDK
**Source:** https://openai.github.io/openai-agents-python/ref/handoffs/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Precise, typed handoff interfaces for transferring context/state to a delegated agent (filters, history nesting, schemas, enable/disable).

## Key Content
- **Core type aliases**
  - **HandoffInputFilter (Eq. 1):**  
    `Callable[[HandoffInputData], MaybeAwaitable[HandoffInputData]]`  
    Filters/edits the data passed to the next agent.
  - **HandoffHistoryMapper (Eq. 2):**  
    `Callable[[list[TResponseInputItem]], list[TResponseInputItem]]`  
    Maps prior transcript → nested summary payload.

- **HandoffInputData (dataclass) fields**
  - `input_history: str | tuple[TResponseInputItem, ...]` — history before `Runner.run()`.
  - `pre_handoff_items: tuple[RunItem, ...]` — items generated before the turn where handoff invoked.
  - `new_items: tuple[RunItem, ...]` — items generated during current turn **including** the triggering item and the tool output message representing the handoff output.
  - `run_context: RunContextWrapper[Any] | None = None` — optional (backwards compatibility).
  - `input_items: tuple[RunItem, ...] | None = None` — if set, used **instead of** `new_items` to build next agent input (lets you filter duplicates for model input while keeping full `new_items` in session history).
  - `clone(**kwargs) -> HandoffInputData` — copy with modifications.

- **Handoff (dataclass) behavior/params**
  - `input_json_schema` — schema exposed to model as tool parameters; describes structured payload passed to `on_invoke_handoff` and **does not replace** next agent’s main input.
  - `on_invoke_handoff: Callable[[RunContextWrapper[Any], str], Awaitable[TAgent]]` — receives (1) handoff run context, (2) LLM JSON args string (or `""` if schema empty); must return an agent.
  - `input_filter: HandoffInputFilter | None` — default: next agent sees entire conversation history; can remove older inputs/tools, etc. **Streaming note:** results of this function are not streamed; earlier items already streamed.
  - `strict_json_schema` — recommended `True` to increase correct JSON input.
  - `is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = True` — disabled handoffs hidden from LLM at runtime.
  - `nest_handoff_history` — per-handoff override of run-level nesting behavior.

- **History nesting utilities**
  - `default_handoff_history_mapper(transcript)` → **single assistant message** summarizing transcript.
  - `nest_handoff_history(handoff_input_data, history_mapper=None)` → summarizes previous transcript for next agent.
  - Wrapper markers: `get_conversation_history_wrappers()`, `set_conversation_history_wrappers(...)`, `reset_conversation_history_wrappers()`.

- **Factory: `handoff(...) -> Handoff`**
  - Key args: `agent` (required), `tool_name_override`, `tool_description_override`, `on_handoff` (+ optional `input_type` for validation/parsing), `input_filter`, `nest_handoff_history`, `is_enabled`.

## When to surface
Use when students ask how a supervisor delegates to sub-agents, how to filter/shape context passed across agents, how to validate typed tool-call inputs via JSON schema, or how to nest/summarize prior conversation for subgraph composition.