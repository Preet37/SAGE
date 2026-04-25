# Source: https://openai.github.io/openai-agents-js/guides/handoffs/
# Author: OpenAI
# Author Slug: openai
# Title: Handoffs | OpenAI Agents SDK (JavaScript)
# Fetched via: trafilatura
# Date: 2026-04-10

Handoffs
Handoffs let an agent delegate part of a conversation to another agent. This is useful when different agents specialise in specific areas. In a customer support app for example, you might have agents that handle bookings, refunds or FAQs.
Handoffs are represented as tools to the LLM. If you hand off to an agent called Refund Agent
, the tool name would be transfer_to_refund_agent
.
Read this page after
[Agents]once you know the specialist should take over the conversation. If the specialist should stay behind the original agent, use[agents as tools]instead.
Creating a handoff
[Section titled “Creating a handoff”](#creating-a-handoff)
Every agent accepts a handoffs
option. It can contain other Agent
instances or Handoff
objects returned by the handoff()
helper.
If you pass plain Agent
instances, their handoffDescription
(if provided) is appended to the default tool description. Use it to clarify when the model should pick that handoff.
Basic usage
[Section titled “Basic usage”](#basic-usage)
Customising handoffs via handoff()
[Section titled “Customising handoffs via handoff()”](#customising-handoffs-via-handoff)
The handoff()
function lets you tweak the generated tool.
agent
– the agent to hand off to.toolNameOverride
– override the defaulttransfer_to_<agent_name>
tool name.toolDescriptionOverride
– override the default tool description.onHandoff
– callback when the handoff occurs. Receives aRunContext
and, wheninputType
is configured, the parsed handoff payload.inputType
– schema for the handoff tool-call arguments.inputFilter
– filter the history passed to the next agent.isEnabled
– boolean or predicate that exposes the handoff only for matching runs.
The handoff()
helper always transfers control to the specific agent
you passed in. If you have multiple possible destinations, register one handoff per destination and let the model choose among them. Use a custom Handoff
when your own handoff code must decide which agent to return at invocation time.
Handoff inputs
[Section titled “Handoff inputs”](#handoff-inputs)
Sometimes you want the model to attach a small structured payload when it chooses a handoff. Define inputType
and onHandoff
together for that case.
inputType
describes the arguments for the handoff tool call itself. The SDK exposes that schema to the model as the handoff tool’s parameters
, parses the returned arguments locally, and passes the parsed value to onHandoff
.
It does not replace the next agent’s main input, and it does not choose a different destination. The handoff()
helper still transfers to the specific agent you wrapped, and the receiving agent still sees the conversation history unless you change it with an inputFilter
.
inputType
is also separate from RunContext
. Use it for metadata the model decides at handoff time, not for application state or dependencies you already have locally.
When to use inputType
[Section titled “When to use inputType”](#when-to-use-inputtype)
Use inputType
when the handoff needs a small piece of model-generated routing metadata such as reason
, language
, priority
, or summary
. For example, a triage agent can hand off to a refund agent with { reason: 'duplicate_charge', priority: 'high' }
, and onHandoff
can log or persist that metadata before the refund agent takes over.
Choose a different mechanism when the goal is different:
- Put existing application state in
RunContext
. - Use
inputFilter
if you want to change what history the receiving agent sees. - Register one handoff per destination if there are multiple possible specialists.
inputType
can add metadata to the chosen handoff, but it does not dispatch between destinations. - Prefer a Zod schema when you want the SDK to validate the parsed payload before
onHandoff
runs; a raw JSON Schema only defines the tool contract sent to the model.
Input filters
[Section titled “Input filters”](#input-filters)
By default a handoff receives the entire conversation history. To modify what gets passed to the next agent, provide an inputFilter
. Common helpers live in @openai/agents-core/extensions
.
An inputFilter
receives and returns a HandoffInputData
object:
inputHistory
– the input history before the run started.preHandoffItems
– items generated before the turn where the handoff happened.newItems
– items generated during the current turn, including the handoff call/output items.runContext
– the active run context.
If you also configure handoffInputFilter
on the Runner
, the per-handoff inputFilter
takes precedence for that specific handoff.
Recommended prompts
[Section titled “Recommended prompts”](#recommended-prompts)
LLMs respond more reliably when your prompts mention handoffs. The SDK exposes a recommended prefix via RECOMMENDED_PROMPT_PREFIX
.
Related guides
[Section titled “Related guides”](#related-guides)
[Agents](/openai-agents-js/guides/agents#composition-patterns)for choosing between managers and handoffs.[Agent orchestration](/openai-agents-js/guides/multi-agent)for the broader workflow tradeoffs.[Tools](/openai-agents-js/guides/tools#4-agents-as-tools)for the manager-style alternative usingagent.asTool()
.[Running agents](/openai-agents-js/guides/running-agents)for how handoffs behave at run time.[Results](/openai-agents-js/guides/results#final-output)for typedfinalOutput
across handoff graphs.