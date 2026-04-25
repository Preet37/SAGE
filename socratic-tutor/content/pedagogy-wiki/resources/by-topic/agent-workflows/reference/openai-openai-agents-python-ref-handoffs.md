# Source: https://openai.github.io/openai-agents-python/ref/handoffs/
# Author: OpenAI
# Author Slug: openai
# Title: Handoffs - OpenAI Agents SDK
# Fetched via: trafilatura
# Date: 2026-04-10

Handoffs
HandoffInputFilter
module-attribute
HandoffInputFilter: TypeAlias = Callable[
[[HandoffInputData](#agents.handoffs.HandoffInputData)], MaybeAwaitable[[HandoffInputData](#agents.handoffs.HandoffInputData)]
]
A function that filters the input data passed to the next agent.
HandoffHistoryMapper
module-attribute
HandoffHistoryMapper: TypeAlias = Callable[
[list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]], list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]
]
A function that maps the previous transcript to the nested summary payload.
HandoffInputData
dataclass
Source code in src/agents/handoffs/__init__.py
input_history
instance-attribute
input_history: str | tuple[[TResponseInputItem](../items/#agents.items.TResponseInputItem), ...]
The input history before Runner.run()
was called.
pre_handoff_items
instance-attribute
pre_handoff_items: tuple[[RunItem](../items/#agents.items.RunItem), ...]
The items generated before the agent turn where the handoff was invoked.
new_items
instance-attribute
new_items: tuple[[RunItem](../items/#agents.items.RunItem), ...]
The new items generated during the current agent turn, including the item that triggered the handoff and the tool output message representing the response from the handoff output.
run_context
class-attribute
instance-attribute
run_context: [RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[Any] | None = None
The run context at the time the handoff was invoked. Note that, since this property was added later on, it is optional for backwards compatibility.
input_items
class-attribute
instance-attribute
input_items: tuple[[RunItem](../items/#agents.items.RunItem), ...] | None = None
Items to include in the next agent's input. When set, these items are used instead of new_items for building the input to the next agent. This allows filtering duplicates from agent input while preserving all items in new_items for session history.
clone
clone(**kwargs: Any) -> [HandoffInputData](#agents.handoffs.HandoffInputData)
Make a copy of the handoff input data, with the given arguments changed. For example, you could do:
Source code in src/agents/handoffs/__init__.py
Handoff
dataclass
Bases: Generic[TContext, TAgent]
A handoff is when an agent delegates a task to another agent.
For example, in a customer support scenario you might have a "triage agent" that determines which agent should handle the user's request, and sub-agents that specialize in different areas like billing, account management, etc.
Source code in src/agents/handoffs/__init__.py
|
|
tool_description
instance-attribute
The description of the tool that represents the handoff.
input_json_schema
instance-attribute
The JSON schema for the handoff tool-call arguments.
This schema is exposed to the model as the handoff tool's parameters
. It only describes the
structured payload passed to on_invoke_handoff
and does not replace the next agent's main
input.
on_invoke_handoff
instance-attribute
on_invoke_handoff: Callable[
[[RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[Any], str], Awaitable[TAgent]
]
The function that invokes the handoff.
The parameters passed are: (1) the handoff run context, (2) the arguments from the LLM as a
JSON string (or an empty string if input_json_schema
is empty). Must return an agent.
input_filter
class-attribute
instance-attribute
input_filter: [HandoffInputFilter](#agents.handoffs.HandoffInputFilter) | None = None
A function that filters the inputs that are passed to the next agent.
By default, the new agent sees the entire conversation history. In some cases, you may want to
filter inputs (for example, to remove older inputs or remove tools from existing inputs). The
function receives the entire conversation history so far, including the input item that
triggered the handoff and a tool call output item representing the handoff tool's output. You
are free to modify the input history or new items as you see fit. The next agent receives the
input history plus input_items
when provided, otherwise it receives new_items
. Use
input_items
to filter model input while keeping new_items
intact for session history.
IMPORTANT: in streaming mode, we will not stream anything as a result of this function. The
items generated before will already have been streamed.
nest_handoff_history
class-attribute
instance-attribute
Override the run-level nest_handoff_history
behavior for this handoff only.
strict_json_schema
class-attribute
instance-attribute
Whether the input JSON schema is in strict mode. We strongly recommend setting this to True because it increases the likelihood of correct JSON input.
is_enabled
class-attribute
instance-attribute
is_enabled: (
bool
| Callable[
[[RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[Any], [AgentBase](../agent/#agents.agent.AgentBase)[Any]],
MaybeAwaitable[bool],
]
) = True
Whether the handoff is enabled.
Either a bool or a callable that takes the run context and agent and returns whether the handoff is enabled. You can use this to dynamically enable or disable a handoff based on your context or state.
default_handoff_history_mapper
default_handoff_history_mapper(
transcript: list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)],
) -> list[[TResponseInputItem](../items/#agents.items.TResponseInputItem)]
Return a single assistant message summarizing the transcript.
Source code in src/agents/handoffs/history.py
get_conversation_history_wrappers
Return the current start/end markers used for the nested conversation summary.
nest_handoff_history
nest_handoff_history(
handoff_input_data: [HandoffInputData](#agents.handoffs.HandoffInputData),
*,
history_mapper: [HandoffHistoryMapper](#agents.handoffs.HandoffHistoryMapper) | None = None,
) -> [HandoffInputData](#agents.handoffs.HandoffInputData)
Summarize the previous transcript for the next agent.
Source code in src/agents/handoffs/history.py
reset_conversation_history_wrappers
Restore the default <CONVERSATION HISTORY>
markers.
Source code in src/agents/handoffs/history.py
set_conversation_history_wrappers
Override the markers that wrap the generated conversation summary.
Pass None
to leave either side unchanged.
Source code in src/agents/handoffs/history.py
handoff
handoff(
agent: [Agent](../agent/#agents.agent.Agent)[TContext],
*,
tool_name_override: str | None = None,
tool_description_override: str | None = None,
input_filter: Callable[
[[HandoffInputData](#agents.handoffs.HandoffInputData)], [HandoffInputData](#agents.handoffs.HandoffInputData)
]
| None = None,
nest_handoff_history: bool | None = None,
is_enabled: bool
| Callable[
[[RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[Any], [Agent](../agent/#agents.agent.Agent)[Any]],
MaybeAwaitable[bool],
] = True,
) -> [Handoff](#agents.handoffs.Handoff)[TContext, [Agent](../agent/#agents.agent.Agent)[TContext]]
handoff(
agent: [Agent](../agent/#agents.agent.Agent)[TContext],
*,
on_handoff: OnHandoffWithInput[THandoffInput],
input_type: type[THandoffInput],
tool_description_override: str | None = None,
tool_name_override: str | None = None,
input_filter: Callable[
[[HandoffInputData](#agents.handoffs.HandoffInputData)], [HandoffInputData](#agents.handoffs.HandoffInputData)
]
| None = None,
nest_handoff_history: bool | None = None,
is_enabled: bool
| Callable[
[[RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[Any], [Agent](../agent/#agents.agent.Agent)[Any]],
MaybeAwaitable[bool],
] = True,
) -> [Handoff](#agents.handoffs.Handoff)[TContext, [Agent](../agent/#agents.agent.Agent)[TContext]]
handoff(
agent: [Agent](../agent/#agents.agent.Agent)[TContext],
*,
on_handoff: OnHandoffWithoutInput,
tool_description_override: str | None = None,
tool_name_override: str | None = None,
input_filter: Callable[
[[HandoffInputData](#agents.handoffs.HandoffInputData)], [HandoffInputData](#agents.handoffs.HandoffInputData)
]
| None = None,
nest_handoff_history: bool | None = None,
is_enabled: bool
| Callable[
[[RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[Any], [Agent](../agent/#agents.agent.Agent)[Any]],
MaybeAwaitable[bool],
] = True,
) -> [Handoff](#agents.handoffs.Handoff)[TContext, [Agent](../agent/#agents.agent.Agent)[TContext]]
handoff(
agent: [Agent](../agent/#agents.agent.Agent)[TContext],
tool_name_override: str | None = None,
tool_description_override: str | None = None,
on_handoff: OnHandoffWithInput[THandoffInput]
| OnHandoffWithoutInput
| None = None,
input_type: type[THandoffInput] | None = None,
input_filter: Callable[
[[HandoffInputData](#agents.handoffs.HandoffInputData)], [HandoffInputData](#agents.handoffs.HandoffInputData)
]
| None = None,
nest_handoff_history: bool | None = None,
is_enabled: bool
| Callable[
[[RunContextWrapper](../run_context/#agents.run_context.RunContextWrapper)[Any], [Agent](../agent/#agents.agent.Agent)[TContext]],
MaybeAwaitable[bool],
] = True,
) -> [Handoff](#agents.handoffs.Handoff)[TContext, [Agent](../agent/#agents.agent.Agent)[TContext]]
Create a handoff from an agent.
Parameters:
| Name | Type | Description | Default |
|---|---|---|---|
agent
|
|
The agent to handoff to. |
required |
tool_name_override
|
str | None
|
Optional override for the name of the tool that represents the handoff. |
None
|
tool_description_override
|
str | None
|
Optional override for the description of the tool that represents the handoff. |
None
|
on_handoff
|
OnHandoffWithInput[THandoffInput] | OnHandoffWithoutInput | None
|
A function that runs when the handoff is invoked. The |
None
|
input_type
|
type[THandoffInput] | None
|
The type of the handoff tool-call arguments. If provided, the model-generated
JSON arguments are validated against this type and the parsed value is passed to
|
None
|
input_filter
|
Callable[[
|
A function that filters the inputs that are passed to the next agent. |
None
|
nest_handoff_history
|
bool | None
|
Optional override for the RunConfig-level |
None
|
is_enabled
|
bool | Callable[[
|
Whether the handoff is enabled. Can be a bool or a callable that takes the run context and agent and returns whether the handoff is enabled. Disabled handoffs are hidden from the LLM at runtime. |
True
|
Source code in src/agents/handoffs/__init__.py
|
|