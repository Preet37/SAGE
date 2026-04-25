# Source: https://docs.langchain.com/oss/python/langchain/human-in-the-loop
# Title: Human-in-the-loop - Docs by LangChain
# Fetched via: trafilatura
# Date: 2026-04-10

[middleware](/oss/python/langchain/middleware/built-in#human-in-the-loop)lets you add human oversight to agent tool calls. When a model proposes an action that might require review—for example, writing to a file or executing SQL—the middleware can pause execution and wait for a decision. It does this by checking each tool call against a configurable policy. If intervention is needed, the middleware issues an
[interrupt](https://reference.langchain.com/python/langgraph/types/interrupt)that halts execution. The graph state is saved using LangGraph’s
[persistence layer](/oss/python/langgraph/persistence), so execution can pause safely and resume later. A human decision then determines what happens next: the action can be approved as-is (
approve
), modified before running (edit
), or rejected with feedback (reject
).
Interrupt decision types
The[middleware](/oss/python/langchain/middleware/built-in#human-in-the-loop)defines three built-in ways a human can respond to an interrupt:
| Decision Type | Description | Example Use Case |
|---|---|---|
✅ approve | The action is approved as-is and executed without changes. | Send an email draft exactly as written |
✏️ edit | The tool call is executed with modifications. | Change the recipient before sending an email |
❌ reject | The tool call is rejected, with an explanation added to the conversation. | Reject an email draft and explain how to rewrite it |
interrupt_on
.
When multiple tool calls are paused at the same time, each action requires a separate decision.
Decisions must be provided in the same order as the actions appear in the interrupt request.
Configuring interrupts
To use HITL, add the[middleware](/oss/python/langchain/middleware/built-in#human-in-the-loop)to the agent’s
middleware
list when creating the agent.
You configure it with a mapping of tool actions to the decision types that are allowed for each action. The middleware will interrupt execution when a tool call matches an action in the mapping.
You must configure a checkpointer to persist the graph state across interrupts.
In production, use a persistent checkpointer like
[. For testing or prototyping, use](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.postgres.aio.AsyncPostgresSaver)AsyncPostgresSaver
[.When invoking the agent, pass a](https://reference.langchain.com/python/langgraph/checkpoints/#langgraph.checkpoint.memory.InMemorySaver)InMemorySaver
config
that includes the thread ID to associate execution with a conversation thread.
See the [LangGraph interrupts documentation](/oss/python/langgraph/interrupts)for details.Configuration options
Configuration options
Mapping of tool names to approval configs. Values can be
True
(interrupt with default config), False
(auto-approve), or an InterruptOnConfig
object.Prefix for action request descriptions
InterruptOnConfig
options:List of allowed decisions:
'approve'
, 'edit'
, or 'reject'
Static string or callable function for custom description
Responding to interrupts
When you invoke the agent, it runs until it either completes or an interrupt is raised. An interrupt is triggered when a tool call matches the policy you configured ininterrupt_on
. With version="v2"
, the result is a GraphOutput
with an interrupts
attribute containing the actions that require review. You can then present those actions to a reviewer and resume execution once decisions are provided.
Decision types
- ✅ approve
- ✏️ edit
- ❌ reject
Use
approve
to approve the tool call as-is and execute it without changes.Streaming with human-in-the-loop
You can usestream()
instead of invoke()
to get real-time updates while the agent runs and handles interrupts. Use stream_mode=['updates', 'messages']
with version="v2"
to stream both agent progress and LLM tokens in the unified v2 format.
[Streaming](/oss/python/langchain/streaming)guide for more details on stream modes.
Execution lifecycle
The middleware defines anafter_model
hook that runs after the model generates a response but before any tool calls are executed:
- The agent invokes the model to generate a response.
- The middleware inspects the response for tool calls.
- If any calls require human input, the middleware builds a
HITLRequest
withaction_requests
andreview_configs
and calls[interrupt](https://reference.langchain.com/python/langgraph/types/interrupt). - The agent waits for human decisions.
- Based on the
HITLResponse
decisions, the middleware executes approved or edited calls, synthesizes[ToolMessage](https://reference.langchain.com/python/langchain-core/messages/tool/ToolMessage)’s for rejected calls, and resumes execution.
Custom HITL logic
For more specialized workflows, you can build custom HITL logic directly using the[interrupt](https://reference.langchain.com/python/langgraph/types/interrupt)primitive and
[middleware](/oss/python/langchain/middleware)abstraction. Review the
[execution lifecycle](#execution-lifecycle)above to understand how to integrate interrupts into the agent’s operation.
[Connect these docs](/use-these-docs)to Claude, VSCode, and more via MCP for real-time answers.