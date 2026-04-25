# Source: https://docs.langchain.com/oss/python/langgraph/interrupts
# Title: Interrupts - Docs by LangChain (LangGraph)
# Fetched via: trafilatura
# Date: 2026-04-10

[persistence](/oss/python/langgraph/persistence)layer and waits indefinitely until you resume execution. Interrupts work by calling the
interrupt()
function at any point in your graph nodes. The function accepts any JSON-serializable value which is surfaced to the caller. When you’re ready to continue, you resume execution by re-invoking the graph using Command
, which then becomes the return value of the interrupt()
call from inside the node.
Unlike static breakpoints (which pause before or after specific nodes), interrupts are dynamic: they can be placed anywhere in your code and can be conditional based on your application logic.
- Checkpointing keeps your place: the checkpointer writes the exact graph state so you can resume later, even when in an error state.
thread_id
is your pointer: setconfig={"configurable": {"thread_id": ...}}
to tell the checkpointer which state to load.- Interrupt payloads surface via
chunk["interrupts"]
: when streaming withversion="v2"
, the values you pass tointerrupt()
appear in theinterrupts
field ofvalues
stream parts so you know what the graph is waiting on.
thread_id
you choose is effectively your persistent cursor. Reusing it resumes the same checkpoint; using a new value starts a brand-new thread with an empty state.
Pause using interrupt
The [function pauses graph execution and returns a value to the caller. When you call](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
[within a node, LangGraph saves the current graph state and waits for you to resume execution with input. To use](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
[, you need:](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
- A checkpointer to persist the graph state (use a durable checkpointer in production)
- A thread ID in your config so the runtime knows which state to resume from
- To call
interrupt()
where you want to pause (payload must be JSON-serializable)
[, here’s what happens:](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
- Graph execution gets suspended at the exact point where
is calledinterrupt
- State is saved using the checkpointer so execution can be resumed later, In production, this should be a persistent checkpointer (e.g. backed by a database)
- Value is returned to the caller under
__interrupt__
; it can be any JSON-serializable value (string, object, array, etc.) - Graph waits indefinitely until you resume execution with a response
- Response is passed back into the node when you resume, becoming the return value of the
interrupt()
call
Resuming interrupts
After an interrupt pauses execution, you resume the graph by invoking it again with aCommand
that contains the resume value. The resume value is passed back to the interrupt
call, allowing the node to continue execution with the external input.
- v2 (LangGraph >= 1.1)
- v1 (default)
- You must use the same thread ID when resuming that was used when the interrupt occurred
- The value passed to
Command(resume=...)
becomes the return value of thecallinterrupt
- The node restarts from the beginning of the node where the
was called when resumed, so any code before theinterrupt
runs againinterrupt
- You can pass any JSON-serializable value as the resume value
Common patterns
The key thing that interrupts unlock is the ability to pause execution and wait for external input. This is useful for a variety of use cases, including:-
[Approval workflows](#approve-or-reject): Pause before executing critical actions (API calls, database changes, financial transactions) -
[Handling multiple interrupts](#handling-multiple-interrupts): Pair interrupt IDs with resume values when resuming multiple interrupts in a single invocation -
[Review and edit](#review-and-edit-state): Let humans review and modify LLM outputs or tool calls before continuing -
[Interrupting tool calls](#interrupts-in-tools): Pause before executing tool calls to review and edit the tool call before execution -
[Validating human input](#validating-human-input): Pause before proceeding to the next step to validate human input
Stream with human-in-the-loop (HITL) interrupts
When building interactive agents with human-in-the-loop workflows, you can stream both message chunks and node updates simultaneously to provide real-time feedback while handling interrupts. Use multiple stream modes ("messages"
and "updates"
) with subgraphs=True
(if subgraphs are present) to:
- Stream AI responses in real-time as they’re generated
- Detect when the graph encounters an interrupt
- Handle user input and resume execution seamlessly
-
version="v2"
: All chunks areStreamPart
dicts withtype
,ns
, anddata
keys -
chunk["type"]
: Narrow on the stream mode ("messages"
,"updates"
, etc.) for type inference -
chunk["ns"]
: Identifies the source graph (empty tuple for root, populated for subgraphs) -
subgraphs=True
: Required for interrupt detection in nested graphs -
Command(resume=...)
: Resumes graph execution with user-provided data
Handling multiple interrupts
When parallel branches interrupt simultaneously (for example, fan-out to multiple nodes that each callinterrupt()
), you may need to resume multiple interrupts in a single invocation.
When resuming multiple interrupts with a single invocation, map each interrupt ID to its resume value.
This ensures each response is paired with the correct interrupt at runtime.
Approve or reject
One of the most common uses of interrupts is to pause before a critical action and ask for approval. For example, you might want to ask a human to approve an API call, a database change, or any other important decision.True
to approve or False
to reject:
Full example
Full example
Review and edit state
Sometimes you want to let a human review and edit part of the graph state before continuing. This is useful for correcting LLMs, adding missing information, or making adjustments.Full example
Full example
Interrupts in tools
You can also place interrupts directly inside tool functions. This makes the tool itself pause for approval whenever it’s called, and allows for human review and editing of the tool call before it is executed. First, define a tool that uses[:](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
Full example
Full example
Validating human input
Sometimes you need to validate input from humans and ask again if it’s invalid. You can do this using multiple[calls in a loop.](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
Full example
Full example
Rules of interrupts
When you call[within a node, LangGraph suspends execution by raising an exception that signals the runtime to pause. This exception propagates up through the call stack and is caught by the runtime, which notifies the graph to save the current state and wait for external input. When execution resumes (after you provide the requested input), the runtime restarts the entire node from the beginning—it does not resume from the exact line where](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
[was called. This means any code that ran before the](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
[will execute again. Because of this, there’s a few important rules to follow when working with interrupts to ensure they behave as expected.](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
Do not wrap interrupt
calls in try/except
The way that [pauses execution at the point of the call is by throwing a special exception. If you wrap the](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
[call in a try/except block, you will catch this exception and the interrupt will not be passed back to the graph.](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
- ✅ Separate
calls from error-prone codeinterrupt
- ✅ Use specific exception types in try/except blocks
- 🔴 Do not wrap
calls in bare try/except blocksinterrupt
Do not reorder interrupt
calls within a node
It’s common to use multiple interrupts in a single node, however this can lead to unexpected behavior if not handled carefully.
When a node contains multiple interrupt calls, LangGraph keeps a list of resume values specific to the task executing the node. Whenever execution resumes, it starts at the beginning of the node. For each interrupt encountered, LangGraph checks if a matching value exists in the task’s resume list. Matching is strictly index-based, so the order of interrupt calls within the node is important.
- ✅ Keep
calls consistent across node executionsinterrupt
- 🔴 Do not conditionally skip
calls within a nodeinterrupt
- 🔴 Do not loop
calls using logic that isn’t deterministic across executionsinterrupt
Do not return complex values in interrupt
calls
Depending on which checkpointer is used, complex values may not be serializable (e.g. you can’t serialize a function). To make your graphs adaptable to any deployment, it’s best practice to only use values that can be reasonably serialized.
- ✅ Pass simple, JSON-serializable types to
interrupt
- ✅ Pass dictionaries/objects with simple values
- 🔴 Do not pass functions, class instances, or other complex objects to
interrupt
Side effects called before interrupt
must be idempotent
Because interrupts work by re-running the nodes they were called from, side effects called before [should (ideally) be idempotent. For context, idempotency means that the same operation can be applied multiple times without changing the result beyond the initial execution. As an example, you might have an API call to update a record inside of a node. If](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
[is called after that call is made, it will be re-run multiple times when the node is resumed, potentially overwriting the initial update or creating duplicate records.](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
- ✅ Use idempotent operations before
interrupt
- ✅ Place side effects after
callsinterrupt
- ✅ Separate side effects into separate nodes when possible
- 🔴 Do not perform non-idempotent operations before
interrupt
- 🔴 Do not create new records without checking if they exist
Using with subgraphs called as functions
When invoking a subgraph within a node, the parent graph will resume execution from the beginning of the node where the subgraph was invoked and the[was triggered. Similarly, the subgraph will also resume from the beginning of the node where](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
[was called.](https://reference.langchain.com/python/langgraph/types/interrupt)
interrupt
Debugging with interrupts
To debug and test a graph, you can use static interrupts as breakpoints to step through the graph execution one node at a time. Static interrupts are triggered at defined points either before or after a node executes. You can set these by specifyinginterrupt_before
and interrupt_after
when compiling the graph.
Static interrupts are not recommended for human-in-the-loop workflows. Use the
[function instead.](https://reference.langchain.com/python/langgraph/types/interrupt)interrupt
- At compile time
- At run time
- The breakpoints are set during
compile
time. interrupt_before
specifies the nodes where execution should pause before the node is executed.interrupt_after
specifies the nodes where execution should pause after the node is executed.- A checkpointer is required to enable breakpoints.
- The graph is run until the first breakpoint is hit.
- The graph is resumed by passing in
None
for the input. This will run the graph until the next breakpoint is hit.
Using LangSmith Studio
You can use[LangSmith Studio](/langsmith/studio)to set static interrupts in your graph in the UI before running the graph. You can also use the UI to inspect the graph state at any point in the execution.
[Connect these docs](/use-these-docs)to Claude, VSCode, and more via MCP for real-time answers.