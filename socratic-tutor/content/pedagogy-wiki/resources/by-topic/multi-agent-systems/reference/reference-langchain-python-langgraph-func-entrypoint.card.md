# Card: LangGraph Functional API `@entrypoint`
**Source:** https://reference.langchain.com/python/langgraph/func/entrypoint  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact decorator/function signature + runtime semantics (inputs/config binding, execution, persistence)

## Key Content
- **Purpose:** `entrypoint` decorator defines a LangGraph workflow in *functional style* (sync or async).
- **Decorator signature (v1.1.6):**  
  `entrypoint(self, checkpointer: BaseCheckpointSaver | None = None, store: BaseStore | None = None, cache: BaseCache | None = None, context_schema: type[ContextT] | None = None, cache_policy: CachePolicy | None = None, retry_policy: RetryPolicy | Sequence[RetryPolicy] | None = None, **kwargs: Unpack[DeprecatedKwargs] = {})`
- **Decorated function signature rule:** must accept **one positional input parameter** (any type). To pass multiple inputs, use a **dict**.
- **Injectable runtime parameters (auto-injected at run time):**
  - `config`: `RunnableConfig` (run-time configuration values)
  - `previous`: previous return value for the same **thread id** (only if `checkpointer` provided)
  - `runtime`: `Runtime` (run info incl. context, store, writer)
- **State management / persistence:**
  - `previous` is available only when a checkpointer is enabled and the same `config["configurable"]["thread_id"]` is used across invocations.
  - To **return one value but checkpoint another**, return `entrypoint.final[value_type, save_type](value=..., save=...)`. Next run’s `previous` receives the **saved** value.
- **Execution patterns:**
  - `.invoke(input, config)` runs once.
  - `.stream(input_or_Command, config)` streams results; can resume after `interrupt(...)` using `Command(resume=...)`.
- **Deprecation:** `config_schema` deprecated since v0.6.0; use `context_schema` (removal in v2.0.0).

## When to surface
Use when students ask how to define/run a functional LangGraph workflow, how `config`/`thread_id` affects persistence, how to access `previous`, or how to resume after `interrupt` and checkpoint different state via `entrypoint.final`.