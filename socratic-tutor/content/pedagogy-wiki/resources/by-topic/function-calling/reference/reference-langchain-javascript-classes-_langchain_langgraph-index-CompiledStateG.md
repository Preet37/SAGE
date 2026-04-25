# Source: https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html
# Title: CompiledStateGraph (LangGraph JS API Reference)
# Fetched via: browser
# Date: 2026-04-10

Class
v1.2.8 (latest)
●
Since v0.3
CompiledStateGraph

Final result from building and compiling a StateGraph. Should not be instantiated directly, only using the StateGraph .compile() instance method.

Copy
class CompiledStateGraph
BASES
CompiledGraph<N, S, U, ExtractStateType<C>, ExtractUpdateType<I, ExtractStateType<I>>, ExtractStateType<O>, NodeReturnType, CommandInstance<InferInterruptResumeType<InterruptType>, Prettify<U>, N>, InferWriterType<WriterType>>
Constructors
constructor
constructor
Properties
property
~NodeReturnType
: NodeReturnType
property
~NodeType
: N
property
~RunInput
: U
property
~RunOutput
: S
property
autoValidate
: boolean

Whether to automatically validate the graph structure when it is compiled. Defaults to true.

property
builder
: StateGraph<unknown, S, U, N, I, O, C, NodeReturnType>
property
cache
: BaseCache<unknown>

Optional cache for the graph, useful for caching tasks.

property
channels
: Channels

The channels in the graph, mapping channel names to their BaseChannel or ManagedValueSpec instances

property
checkpointer
: boolean | BaseCheckpointSaver<number>

Optional checkpointer for persisting graph state. When provided, saves a checkpoint of the graph state at every superstep. When false or undefined, checkpointing is disabled, and the graph will not be able to save or restore state.

property
config
: LangGraphRunnableConfig<Record<string, any>>

The default configuration for graph execution, can be overridden on a per-invocation basis

property
debug
: boolean

Whether to enable debug logging. Defaults to false.

property
description
: string

The description of the compiled graph. This is used by the supervisor agent to describe the handoff to the agent.

property
inputChannels
: string | N | string | N[]

The input channels for the graph. These channels receive the initial input when the graph is invoked. Can be a single channel key or an array of channel keys.

property
interruptAfter
: "*" | "__start__" | N[]

Optional array of node names or "all" to interrupt after executing these nodes. Used for implementing human-in-the-loop workflows.

property
interruptBefore
: "*" | "__start__" | N[]

Optional array of node names or "all" to interrupt before executing these nodes. Used for implementing human-in-the-loop workflows.

property
lc_kwargs
: SerializedFields
property
lc_runnable
: boolean
property
lc_serializable
: boolean
property
name
: string

The name of the task, analogous to the node name in StateGraph.

property
nodes
: Nodes

The nodes in the graph, mapping node names to their PregelNode instances

property
outputChannels
: string | N | string | N[]

The output channels for the graph. These channels contain the final output when the graph completes. Can be a single channel key or an array of channel keys.

property
retryPolicy
: RetryPolicy

Optional retry policy for handling failures in node execution

property
stepTimeout
: number

Optional timeout in milliseconds for the execution of each superstep

property
store
: BaseStore

Optional long-term memory store for the graph, allows for persistence & retrieval of data across threads

property
streamChannels
: string | N | string | N[]

Optional channels to stream. If not specified, all channels will be streamed. Can be a single channel key or an array of channel keys.

property
streamMode
: StreamMode[]

The streaming modes enabled for this graph. Defaults to ["values"]. Supported modes:

"values": Streams the full state after each step
"updates": Streams state updates after each step
"messages": Streams messages from within nodes
"custom": Streams custom events from within nodes
"tools": Streams tool-call lifecycle events (on_tool_start, on_tool_event, on_tool_end, on_tool_error) from LLM tool execution
"debug": Streams events related to the execution of the graph - useful for tracing & debugging graph execution
property
lc_aliases
property
lc_attributes
property
lc_id
property
lc_secrets
property
lc_serializable_keys
property
streamChannelsAsIs
: keyof Channels | keyof Channels[]
property
streamChannelsList
: keyof Channels[]
Methods
method
_batchWithConfig
method
_callWithConfig
method
_getOptionsList
method
_separateRunnableConfigFromCallOptions
method
_streamLog
method
_transformStreamWithConfig
method
assign
method
asTool
method
attachBranch
method
attachEdge
method
attachNode
method
batch
→ Promise<OperationResults<Op>>

Execute multiple operations in a single batch. This is more efficient than executing operations individually.

method
clearCache
→ Promise<void>
method
getGraphAsync
→ Promise<Graph>

Returns a drawable representation of the computation graph.

method
getName
method
getState
→ Promise<StateSnapshot>

Gets the current state of the graph. Requires a checkpointer to be configured.

method
getStateHistory
→ AsyncIterableIterator<StateSnapshot>

Gets the history of graph states. Requires a checkpointer to be configured. Useful for:

Debugging execution history
Implementing time travel
Analyzing graph behavior
method
getSubgraphsAsync
→ AsyncGenerator<[string, Pregel<any, any, StrRecord<string, any>, any, any, any, any, unknown, CommandInstance<unknown, Record<string, unknown>, string>, any>]>

Gets all subgraphs within this graph asynchronously. A subgraph is a Pregel instance that is nested within a node of this graph.

method
invoke
→ Promise<ExtractStateType<O, O>>

Run the graph with a single input and config.

method
isInterrupted
→ input is __type
method
pick
method
pipe
→ PregelNode<RunInput, Exclude<NewRunOutput, Error>>

Create a new runnable sequence that runs each individual runnable in series, piping the output of one runnable into another runnable or runnable-like.

method
stream
→ Promise<IterableReadableStream<StreamOutputMap<TStreamMode, TSubgraphs, ExtractUpdateType<I, ExtractStateType<I, I>>, ExtractStateType<O, O>, "__start__" | N, NodeReturnType, InferWriterType<WriterType>, TEncoding>>>

Streams the execution of the graph, emitting state updates as they occur. This is the primary method for observing graph execution in real-time.

Stream modes:

"values": Emits complete state after each step
"updates": Emits only state changes after each step
"debug": Emits detailed debug information
"messages": Emits messages from within nodes
"custom": Emits custom events from within nodes
"checkpoints": Emits checkpoints from within nodes
"tasks": Emits tasks from within nodes
method
streamEvents
→ IterableReadableStream<StreamEvent>
method
streamLog
method
toJSON
→ __type
method
toJSONNotImplemented
method
transform
method
updateState
→ Promise<RunnableConfig<Record<string, any>>>

Updates the state of the graph with new values. Requires a checkpointer to be configured.

This method can be used for:

Implementing human-in-the-loop workflows
Modifying graph state during breakpoints
Integrating external inputs into the graph
method
validate
→ this

Validates the graph structure to ensure it is well-formed. Checks for:

No orphaned nodes
Valid input/output channel configurations
Valid interrupt configurations
method
withConfig
→ CompiledStateGraph<S, U, N, I, O, C, NodeReturnType, InterruptType, WriterType>

Creates a new instance of the Pregel graph with updated configuration. This method follows the immutable pattern - instead of modifying the current instance, it returns a new instance with the merged configuration.

method
withFallbacks
method
withListeners
method
withRetry
method
isRunnable
deprecated
method
getGraph
→ Graph

Returns a drawable representation of the computation graph.

deprecated
method
getSubgraphs
→ Generator<[string, Pregel<any, any, StrRecord<string, any>, any, any, any, any, unknown, CommandInstance<unknown, Record<string, unknown>, string>, any>]>

Gets all subgraphs within this graph. A subgraph is a Pregel instance that is nested within a node of this graph.

Inherited from
CompiledGraph
PROPERTIES
P
~NodeReturnType
: NodeReturnType
P
~NodeType
: N
P
~RunInput
: U
P
~RunOutput
: S
P
autoValidate
: boolean
—

Whether to automatically validate the graph structure when it is compiled. Defaults to true.

P
builder
: StateGraph<unknown, S, U, N, I, O, C, NodeReturnType>
P
cache
: BaseCache<unknown>
—

Optional cache for the graph, useful for caching tasks.

P
channels
: Channels
—

The channels in the graph, mapping channel names to their BaseChannel or ManagedValueSpec instances

P
checkpointer
: boolean | BaseCheckpointSaver<number>
—

Optional checkpointer for persisting graph state.

P
config
: LangGraphRunnableConfig<Record<string, any>>
—

The default configuration for graph execution, can be overridden on a per-invocation basis

P
debug
: boolean
—

Whether to enable debug logging. Defaults to false.

P
inputChannels
: string | N | string | N[]
—

The input channels for the graph. These channels receive the initial input when the graph is invoked.

P
interruptAfter
: "*" | "__start__" | N[]
—

Optional array of node names or "all" to interrupt after executing these nodes.

P
interruptBefore
: "*" | "__start__" | N[]
—

Optional array of node names or "all" to interrupt before executing these nodes.

P
lc_kwargs
P
lc_runnable
P
lc_serializable
P
name
: string
—

The name of the task, analogous to the node name in StateGraph.

P
nodes
: Nodes
—

The nodes in the graph, mapping node names to their PregelNode instances

P
outputChannels
: string | N | string | N[]
—

The output channels for the graph. These channels contain the final output when the graph completes.

P
retryPolicy
: RetryPolicy
—

Optional retry policy for handling failures in node execution

P
stepTimeout
: number
—

Optional timeout in milliseconds for the execution of each superstep

P
store
: BaseStore
—

Optional long-term memory store for the graph, allows for persistence & retrieval of data across threads

P
streamChannels
: string | N | string | N[]
—

Optional channels to stream. If not specified, all channels will be streamed.

P
streamMode
: StreamMode[]
—

The streaming modes enabled for this graph. Defaults to ["values"].

P
lc_aliases
P
lc_attributes
P
lc_id
P
lc_secrets
P
lc_serializable_keys
P
streamChannelsAsIs
: keyof Channels | keyof Channels[]
P
streamChannelsList
: keyof Channels[]
METHODS
M
_batchWithConfig
M
_callWithConfig
M
_getOptionsList
M
_separateRunnableConfigFromCallOptions
M
_streamLog
M
_transformStreamWithConfig
M
assign
M
asTool
M
attachBranch
M
attachEdge
M
attachNode
M
batch
→ Promise<OperationResults<Op>>
—

Execute multiple operations in a single batch.

M
clearCache
→ Promise<void>
M
getGraph
→ Graph
—

Returns a drawable representation of the computation graph.

M
getGraphAsync
→ Promise<Graph>
—

Returns a drawable representation of the computation graph.

M
getName
M
getState
→ Promise<StateSnapshot>
—

Gets the current state of the graph.

M
getStateHistory
→ AsyncIterableIterator<StateSnapshot>
—

Gets the history of graph states.

M
getSubgraphs
→ Generator<[string, Pregel<any, any, StrRecord<string, any>, any, any, any, any, unknown, CommandInstance<unknown, Record<string, unknown>, string>, any>]>
—

Gets all subgraphs within this graph.

M
getSubgraphsAsync
→ AsyncGenerator<[string, Pregel<any, any, StrRecord<string, any>, any, any, any, any, unknown, CommandInstance<unknown, Record<string, unknown>, string>, any>]>
—

Gets all subgraphs within this graph asynchronously.

M
invoke
→ Promise<ExtractStateType<O, O>>
—

Run the graph with a single input and config.

M
pick
M
pipe
→ PregelNode<RunInput, Exclude<NewRunOutput, Error>>
—

Create a new runnable sequence that runs each individual runnable in series,

M
stream
→ Promise<IterableReadableStream<StreamOutputMap<TStreamMode, TSubgraphs, ExtractUpdateType<I, ExtractStateType<I, I>>, ExtractStateType<O, O>, "__start__" | N, NodeReturnType, InferWriterType<WriterType>, TEncoding>>>
—

Streams the execution of the graph, emitting state updates as they occur.

M
streamEvents
→ IterableReadableStream<StreamEvent>
M
streamLog
M
toJSON
→ __type
M
toJSONNotImplemented
M
transform
M
updateState
→ Promise<RunnableConfig<Record<string, any>>>
—

Updates the state of the graph with new values.

M
validate
→ this
—

Validates the graph structure to ensure it is well-formed.

M
withConfig
→ CompiledStateGraph<S, U, N, I, O, C, NodeReturnType, InterruptType, WriterType>
—

Creates a new instance of the Pregel graph with updated configuration.

M
withFallbacks
M
withListeners
M
withRetry
Inherited from
Pregel
PROPERTIES
P
autoValidate
: boolean
—

Whether to automatically validate the graph structure when it is compiled. Defaults to true.

P
cache
: BaseCache<unknown>
—

Optional cache for the graph, useful for caching tasks.

P
channels
: Channels
—

The channels in the graph, mapping channel names to their BaseChannel or ManagedValueSpec instances

P
checkpointer
: boolean | BaseCheckpointSaver<number>
—

Optional checkpointer for persisting graph state.

P
config
: LangGraphRunnableConfig<Record<string, any>>
—

The default configuration for graph execution, can be overridden on a per-invocation basis

P
debug
: boolean
—

Whether to enable debug logging. Defaults to false.

P
inputChannels
: string | N | string | N[]
—

The input channels for the graph. These channels receive the initial input when the graph is invoked.

P
interruptAfter
: "*" | "__start__" | N[]
—

Optional array of node names or "all" to interrupt after executing these nodes.

P
interruptBefore
: "*" | "__start__" | N[]
—

Optional array of node names or "all" to interrupt before executing these nodes.

P
lc_kwargs
P
lc_runnable
P
lc_serializable
P
name
: string
—

The name of the task, analogous to the node name in StateGraph.

P
nodes
: Nodes
—

The nodes in the graph, mapping node names to their PregelNode instances

P
outputChannels
: string | N | string | N[]
—

The output channels for the graph. These channels contain the final output when the graph completes.

P
retryPolicy
: RetryPolicy
—

Optional retry policy for handling failures in node execution

P
stepTimeout
: number
—

Optional timeout in milliseconds for the execution of each superstep

P
store
: BaseStore
—

Optional long-term memory store for the graph, allows for persistence & retrieval of data across threads

P
streamChannels
: string | N | string | N[]
—

Optional channels to stream. If not specified, all channels will be streamed.

P
streamMode
: StreamMode[]
—

The streaming modes enabled for this graph. Defaults to ["values"].

P
lc_aliases
P
lc_attributes
P
lc_id
P
lc_secrets
P
lc_serializable_keys
P
streamChannelsAsIs
: keyof Channels | keyof Channels[]
P
streamChannelsList
: keyof Channels[]
METHODS
M
_batchWithConfig
M
_callWithConfig
M
_getOptionsList
M
_separateRunnableConfigFromCallOptions
M
_streamLog
M
_transformStreamWithConfig
M
assign
M
asTool
M
batch
→ Promise<OperationResults<Op>>
—

Execute multiple operations in a single batch.

M
clearCache
→ Promise<void>
M
getGraph
→ Graph
—

Returns a drawable representation of the computation graph.

M
getGraphAsync
→ Promise<Graph>
—

Returns a drawable representation of the computation graph.

M
getName
M
getState
→ Promise<StateSnapshot>
—

Gets the current state of the graph.

M
getStateHistory
→ AsyncIterableIterator<StateSnapshot>
—

Gets the history of graph states.

M
getSubgraphs
→ Generator<[string, Pregel<any, any, StrRecord<string, any>, any, any, any, any, unknown, CommandInstance<unknown, Record<string, unknown>, string>, any>]>
—

Gets all subgraphs within this graph.

M
getSubgraphsAsync
→ AsyncGenerator<[string, Pregel<any, any, StrRecord<string, any>, any, any, any, any, unknown, CommandInstance<unknown, Record<string, unknown>, string>, any>]>
—

Gets all subgraphs within this graph asynchronously.

M
invoke
→ Promise<ExtractStateType<O, O>>
—

Run the graph with a single input and config.

M
pick
M
pipe
→ PregelNode<RunInput, Exclude<NewRunOutput, Error>>
—

Create a new runnable sequence that runs each individual runnable in series,

M
stream
→ Promise<IterableReadableStream<StreamOutputMap<TStreamMode, TSubgraphs, ExtractUpdateType<I, ExtractStateType<I, I>>, ExtractStateType<O, O>, "__start__" | N, NodeReturnType, InferWriterType<WriterType>, TEncoding>>>
—

Streams the execution of the graph, emitting state updates as they occur.

M
streamEvents
→ IterableReadableStream<StreamEvent>
M
streamLog
M
toJSON
→ __type
M
toJSONNotImplemented
M
transform
M
updateState
→ Promise<RunnableConfig<Record<string, any>>>
—

Updates the state of the graph with new values.

M
validate
→ this
—

Validates the graph structure to ensure it is well-formed.

M
withConfig
→ CompiledStateGraph<S, U, N, I, O, C, NodeReturnType, InterruptType, WriterType>
—

Creates a new instance of the Pregel graph with updated configuration.

M
withFallbacks
M
withListeners
M
withRetry
M
isRunnable
View source on GitHub
Version History