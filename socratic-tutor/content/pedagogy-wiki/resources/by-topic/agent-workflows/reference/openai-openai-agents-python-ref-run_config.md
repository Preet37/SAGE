# Source: https://openai.github.io/openai-agents-python/ref/run_config/
# Author: OpenAI
# Author Slug: openai
# Title: Run Config - OpenAI Agents SDK (Python)
# Fetched via: trafilatura
# Date: 2026-04-10

Run Config
ModelInputData
dataclass
CallModelData
dataclass
Bases: Generic[TContext]
Data passed to RunConfig.call_model_input_filter
prior to model call.
Source code in src/agents/run_config.py
ToolErrorFormatterArgs
dataclass
Bases: Generic[TContext]
Data passed to RunConfig.tool_error_formatter
callbacks.
Source code in src/agents/run_config.py
kind
instance-attribute
The category of tool error being formatted.
tool_type
instance-attribute
The tool runtime that produced the error.
default_message
instance-attribute
The SDK default message for this error kind.
run_context
instance-attribute
run_context: [RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[TContext]
The active run context for the current execution.
RunConfig
dataclass
Configures settings for the entire agent run.
Source code in src/agents/run_config.py
|
|
model
class-attribute
instance-attribute
model: str | [Model](../models/interface/#agents.models.interface.Model) | None = None
The model to use for the entire agent run. If set, will override the model set on every agent. The model_provider passed in below must be able to resolve this model name.
model_provider
class-attribute
instance-attribute
model_provider: [ModelProvider](../models/interface/#agents.models.interface.ModelProvider) = field(
default_factory=[MultiProvider](../models/multi_provider/#agents.models.multi_provider.MultiProvider)
)
The model provider to use when looking up string model names. Defaults to OpenAI.
model_settings
class-attribute
instance-attribute
model_settings: [ModelSettings](../model_settings/#agents.model_settings.ModelSettings) | None = None
Configure global model settings. Any non-null values will override the agent-specific model settings.
handoff_input_filter
class-attribute
instance-attribute
handoff_input_filter: [HandoffInputFilter](../handoffs/#agents.handoffs.HandoffInputFilter) | None = None
A global input filter to apply to all handoffs. If Handoff.input_filter
is set, then that
will take precedence. The input filter allows you to edit the inputs that are sent to the new
agent. See the documentation in Handoff.input_filter
for more details.
nest_handoff_history
class-attribute
instance-attribute
Opt-in beta: wrap prior run history in a single assistant message before handing off when no custom input filter is set. This is disabled by default while we stabilize nested handoffs; set to True to enable the collapsed transcript behavior.
handoff_history_mapper
class-attribute
instance-attribute
handoff_history_mapper: [HandoffHistoryMapper](../handoffs/#agents.handoffs.HandoffHistoryMapper) | None = None
Optional function that receives the normalized transcript (history + handoff items) and
returns the input history that should be passed to the next agent. When left as None
, the
runner collapses the transcript into a single assistant message. This function only runs when
nest_handoff_history
is True.
input_guardrails
class-attribute
instance-attribute
input_guardrails: list[[InputGuardrail](../guardrail/#agents.guardrail.InputGuardrail)[Any]] | None = None
A list of input guardrails to run on the initial run input.
output_guardrails
class-attribute
instance-attribute
output_guardrails: list[[OutputGuardrail](../guardrail/#agents.guardrail.OutputGuardrail)[Any]] | None = None
A list of output guardrails to run on the final output of the run.
tracing_disabled
class-attribute
instance-attribute
Whether tracing is disabled for the agent run. If disabled, we will not trace the agent run.
tracing
class-attribute
instance-attribute
tracing: [TracingConfig](../tracing/#agents.tracing.TracingConfig) | None = None
Tracing configuration for this run.
trace_include_sensitive_data
class-attribute
instance-attribute
Whether we include potentially sensitive data (for example: inputs/outputs of tool calls or LLM generations) in traces. If False, we'll still create spans for these events, but the sensitive data will not be included.
workflow_name
class-attribute
instance-attribute
The name of the run, used for tracing. Should be a logical name for the run, like "Code generation workflow" or "Customer support agent".
trace_id
class-attribute
instance-attribute
A custom trace ID to use for tracing. If not provided, we will generate a new trace ID.
group_id
class-attribute
instance-attribute
A grouping identifier to use for tracing, to link multiple traces from the same conversation or process. For example, you might use a chat thread ID.
trace_metadata
class-attribute
instance-attribute
An optional dictionary of additional metadata to include with the trace.
session_input_callback
class-attribute
instance-attribute
session_input_callback: [SessionInputCallback](../memory/util/#agents.memory.util.SessionInputCallback) | None = None
Defines how to handle session history when new input is provided.
- None
(default): The new input is appended to the session history.
- SessionInputCallback
: A custom function that receives the history and new input, and
returns the desired combined list of items.
call_model_input_filter
class-attribute
instance-attribute
Optional callback that is invoked immediately before calling the model. It receives the current
agent, context and the model input (instructions and input items), and must return a possibly
modified ModelInputData
to use for the model call.
This allows you to edit the input sent to the model e.g. to stay within a token limit. For example, you can use this to add a system prompt to the input.
tool_error_formatter
class-attribute
instance-attribute
Optional callback that formats tool error messages returned to the model.
Returning None
falls back to the SDK default message.
session_settings
class-attribute
instance-attribute
session_settings: [SessionSettings](../memory/session_settings/#agents.memory.session_settings.SessionSettings) | None = None
Configure session settings. Any non-null values will override the session's default settings. Used to control session behavior like the number of items to retrieve.
reasoning_item_id_policy
class-attribute
instance-attribute
Controls how reasoning items are converted to next-turn model input.
None
/"preserve"
keeps reasoning item IDs as-is."omit"
strips reasoning item IDs from model input built by the runner.
RunOptions
Bases: TypedDict
, Generic[TContext]
Arguments for AgentRunner
methods.
Source code in src/agents/run_config.py
previous_response_id
instance-attribute
The ID of the previous response, if any.
auto_previous_response_id
instance-attribute
Enable automatic response chaining for the first turn.
conversation_id
instance-attribute
The ID of the stored conversation, if any.
error_handlers
instance-attribute
error_handlers: NotRequired[
[RunErrorHandlers](../run_error_handlers/#agents.run_error_handlers.RunErrorHandlers)[TContext] | None
]
Error handlers keyed by error kind. Currently supports max_turns.