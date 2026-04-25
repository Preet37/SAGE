# Source: https://openai.github.io/openai-agents-python/ref/run/
# Author: OpenAI
# Author Slug: openai
# Title: RunConfig / Runner.run - OpenAI Agents SDK (Python) Reference
# Fetched via: trafilatura
# Date: 2026-04-10

Runner
Runner
Source code in src/agents/run.py
|
|
run
async
classmethod
run(
starting_agent: [Agent](../agent/#agents.agent.Agent)[TContext],
input: str
| list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]
| [RunState](../run_state/#agents.run_state.RunState)[TContext],
*,
context: TContext | None = None,
max_turns: int = DEFAULT_MAX_TURNS,
hooks: [RunHooks](../lifecycle/#agents.lifecycle.RunHooks)[TContext] | None = None,
run_config: [RunConfig](../run_config/#agents.run_config.RunConfig) | None = None,
error_handlers: [RunErrorHandlers](../run_error_handlers/#agents.run_error_handlers.RunErrorHandlers)[TContext]
| None = None,
previous_response_id: str | None = None,
auto_previous_response_id: bool = False,
conversation_id: str | None = None,
session: [Session](../memory/#agents.memory.Session) | None = None,
) -> [RunResult](../result/#agents.result.RunResult)
Run a workflow starting at the given agent.
The agent will run in a loop until a final output is generated. The loop runs like so:
- The agent is invoked with the given input.
- If there is a final output (i.e. the agent produces something of type
agent.output_type
), the loop terminates. - If there's a handoff, we run the loop again, with the new agent.
- Else, we run tool calls (if any), and re-run the loop.
In two cases, the agent may raise an exception:
- If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.
- If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.
Note
Only the first agent's input guardrails are run.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
starting_agent
|
|
The starting agent to run. |
required |
input
|
str | list[
|
The initial input to the agent. You can pass a single string for a user message, or a list of input items. |
required |
context
|
TContext | None
|
The context to run the agent with. |
None
|
max_turns
|
int
|
The maximum number of turns to run the agent for. A turn is defined as one AI invocation (including any tool calls that might occur). |
DEFAULT_MAX_TURNS
|
hooks
|
|
An object that receives callbacks on various lifecycle events. |
None
|
run_config
|
|
Global settings for the entire agent run. |
None
|
error_handlers
|
|
Error handlers keyed by error kind. Currently supports max_turns. |
None
|
previous_response_id
|
str | None
|
The ID of the previous response. If using OpenAI models via the Responses API, this allows you to skip passing in input from the previous turn. |
None
|
conversation_id
|
str | None
|
The conversation ID (https://platform.openai.com/docs/guides/conversation-state?api-mode=responses). If provided, the conversation will be used to read and write items. Every agent will have access to the conversation history so far, and its output items will be written to the conversation. We recommend only using this if you are exclusively using OpenAI models; other model providers don't write to the Conversation object, so you'll end up having partial conversations stored. |
None
|
session
|
|
A session for automatic conversation history management. |
None
|
Returns:
| Type | Description |
|---|---|
|
A run result containing all the inputs, guardrail results and the output of |
|
the last agent. Agents may perform handoffs, so we don't know the specific |
|
type of the output. |
Source code in src/agents/run.py
|
|
run_sync
classmethod
run_sync(
starting_agent: [Agent](../agent/#agents.agent.Agent)[TContext],
input: str
| list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]
| [RunState](../run_state/#agents.run_state.RunState)[TContext],
*,
context: TContext | None = None,
max_turns: int = DEFAULT_MAX_TURNS,
hooks: [RunHooks](../lifecycle/#agents.lifecycle.RunHooks)[TContext] | None = None,
run_config: [RunConfig](../run_config/#agents.run_config.RunConfig) | None = None,
error_handlers: [RunErrorHandlers](../run_error_handlers/#agents.run_error_handlers.RunErrorHandlers)[TContext]
| None = None,
previous_response_id: str | None = None,
auto_previous_response_id: bool = False,
conversation_id: str | None = None,
session: [Session](../memory/#agents.memory.Session) | None = None,
) -> [RunResult](../result/#agents.result.RunResult)
Run a workflow synchronously, starting at the given agent.
Note
This just wraps the run
method, so it will not work if there's already an
event loop (e.g. inside an async function, or in a Jupyter notebook or async
context like FastAPI). For those cases, use the run
method instead.
The agent will run in a loop until a final output is generated. The loop runs:
- The agent is invoked with the given input.
- If there is a final output (i.e. the agent produces something of type
agent.output_type
), the loop terminates. - If there's a handoff, we run the loop again, with the new agent.
- Else, we run tool calls (if any), and re-run the loop.
In two cases, the agent may raise an exception:
- If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.
- If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.
Note
Only the first agent's input guardrails are run.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
starting_agent
|
|
The starting agent to run. |
required |
input
|
str | list[
|
The initial input to the agent. You can pass a single string for a user message, or a list of input items. |
required |
context
|
TContext | None
|
The context to run the agent with. |
None
|
max_turns
|
int
|
The maximum number of turns to run the agent for. A turn is defined as one AI invocation (including any tool calls that might occur). |
DEFAULT_MAX_TURNS
|
hooks
|
|
An object that receives callbacks on various lifecycle events. |
None
|
run_config
|
|
Global settings for the entire agent run. |
None
|
error_handlers
|
|
Error handlers keyed by error kind. Currently supports max_turns. |
None
|
previous_response_id
|
str | None
|
The ID of the previous response, if using OpenAI models via the Responses API, this allows you to skip passing in input from the previous turn. |
None
|
conversation_id
|
str | None
|
The ID of the stored conversation, if any. |
None
|
session
|
|
A session for automatic conversation history management. |
None
|
Returns:
| Type | Description |
|---|---|
|
A run result containing all the inputs, guardrail results and the output of |
|
the last agent. Agents may perform handoffs, so we don't know the specific |
|
type of the output. |
Source code in src/agents/run.py
|
|
run_streamed
classmethod
run_streamed(
starting_agent: [Agent](../agent/#agents.agent.Agent)[TContext],
input: str
| list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]
| [RunState](../run_state/#agents.run_state.RunState)[TContext],
context: TContext | None = None,
max_turns: int = DEFAULT_MAX_TURNS,
hooks: [RunHooks](../lifecycle/#agents.lifecycle.RunHooks)[TContext] | None = None,
run_config: [RunConfig](../run_config/#agents.run_config.RunConfig) | None = None,
previous_response_id: str | None = None,
auto_previous_response_id: bool = False,
conversation_id: str | None = None,
session: [Session](../memory/#agents.memory.Session) | None = None,
*,
error_handlers: [RunErrorHandlers](../run_error_handlers/#agents.run_error_handlers.RunErrorHandlers)[TContext]
| None = None,
) -> [RunResultStreaming](../result/#agents.result.RunResultStreaming)
Run a workflow starting at the given agent in streaming mode.
The returned result object contains a method you can use to stream semantic events as they are generated.
The agent will run in a loop until a final output is generated. The loop runs like so:
- The agent is invoked with the given input.
- If there is a final output (i.e. the agent produces something of type
agent.output_type
), the loop terminates. - If there's a handoff, we run the loop again, with the new agent.
- Else, we run tool calls (if any), and re-run the loop.
In two cases, the agent may raise an exception:
- If the max_turns is exceeded, a MaxTurnsExceeded exception is raised unless handled.
- If a guardrail tripwire is triggered, a GuardrailTripwireTriggered exception is raised.
Note
Only the first agent's input guardrails are run.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
starting_agent
|
|
The starting agent to run. |
required |
input
|
str | list[
|
The initial input to the agent. You can pass a single string for a user message, or a list of input items. |
required |
context
|
TContext | None
|
The context to run the agent with. |
None
|
max_turns
|
int
|
The maximum number of turns to run the agent for. A turn is defined as one AI invocation (including any tool calls that might occur). |
DEFAULT_MAX_TURNS
|
hooks
|
|
An object that receives callbacks on various lifecycle events. |
None
|
run_config
|
|
Global settings for the entire agent run. |
None
|
error_handlers
|
|
Error handlers keyed by error kind. Currently supports max_turns. |
None
|
previous_response_id
|
str | None
|
The ID of the previous response, if using OpenAI models via the Responses API, this allows you to skip passing in input from the previous turn. |
None
|
conversation_id
|
str | None
|
The ID of the stored conversation, if any. |
None
|
session
|
|
A session for automatic conversation history management. |
None
|
Returns:
| Type | Description |
|---|---|
|
A result object that contains data about the run, as well as a method to |
|
stream events. |
Source code in src/agents/run.py
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