# Source: https://reference.langchain.com/python/langgraph/graphs/
# Title: Graphs | LangChain Reference
# Fetched via: search
# Date: 2026-04-10

# Graphs

##

StateGraph



Bases:

`Generic[StateT, ContextT, InputT, OutputT]`

A graph whose nodes communicate by reading and writing to a shared state.

The signature of each node is

`State -> Partial<State>`.

Each state key can optionally be annotated with a reducer function that

will be used to aggregate the values of that key received from multiple nodes.

…

`ainvoke()`. See the

`CompiledStateGraph` documentation for more details.

|PARAMETER|DESCRIPTION|
|--|--|
|`state_schema`|The schema class that defines the state.|
|`context_schema`|The schema class that defines the runtime context. Use this to expose immutable context data to your nodes, like|
|`input_schema`|The schema class that defines the input to the graph.|
|`output_schema`|The schema class that defines the output from the graph.|
`config_schema` Deprecated

…

return a + [b]

return a

class State(TypedDict):

x: Annotated[list, reducer]

class Context(TypedDict):

r: float

graph = StateGraph(state_schema=State, context_schema=Context)

def node(state: State, runtime: Runtime[Context]) -> dict:

r = runtime.context.get("r", 1.0)
x = state["x"][-1]

next_value = x * r * (1 - x)

return {"x": next_value}

graph.add_node("A", node)

graph.set_entry_point("A")

graph.set_finish_point("A")

compiled = graph.compile()

step1 = compiled.invoke({"x": 0.5}, context={"r": 3.0})

# {'x': [0.5, 0.75]}

```
|METHOD|DESCRIPTION|
|--|--|
|`add_node`|Add a new node to the|
|`add_edge`|Add a directed edge from the start node (or list of start nodes) to the end node.|
|`add_conditional_edges`|Add a conditional edge from the starting node to any number of destination nodes.|
|`add_sequence`|Add a sequence of nodes that will be executed in the provided order.|
|`compile`|Compiles the|

###

add_node

```

add_node(

node: str | StateNode[NodeInputT, ContextT],

action: StateNode[NodeInputT, ContextT] | None = None,

*,

defer: bool = False,

metadata: dict[str, Any] | None = None,

input_schema: type[NodeInputT] | None = None,

retry_policy: RetryPolicy | Sequence[RetryPolicy] | None = None,

cache_policy: CachePolicy | None = None,

destinations: dict[str, str] | tuple[str, ...] | None = None,

**kwargs: Unpack[DeprecatedKwargs],

) -> Self
```

Add a new node to the

`StateGraph`.

|PARAMETER|DESCRIPTION|
|--|--|
|`node`|The function or runnable this node will run. If a string is provided, it will be used as the node name, and action will be used as the function or runnable.|
|`action`|The action associated with the node. Will be used as the node function or runnable if|
|`defer`|Whether to defer the execution of the node until the run is about to end.|
|`metadata`|The metadata associated with the node.|
|`input_schema`|The input schema for the node. (Default: the graph's state schema)|
|`retry_policy`|The retry policy for the node. If a sequence is provided, the first matching policy will be applied.|

…

## Example

```

from typing_extensions import TypedDict

from langchain_core.runnables import RunnableConfig

from langgraph.graph import START, StateGraph

class State(TypedDict):

x: int

def my_node(state: State, config: RunnableConfig) -> State:

return {"x": state["x"] + 1}

builder = StateGraph(State)

builder.add_node(my_node) # node name will be 'my_node'

builder.add_edge(START, "my_node")

graph = builder.compile()

graph.invoke({"x": 1})

# {'x': 2}

```

## Customize the name:

```

builder = StateGraph(State)

builder.add_node("my_fair_node", my_node)

builder.add_edge(START, "my_fair_node")

graph = builder.compile()

graph.invoke({"x": 1})

# {'x': 2}

```

|RETURNS|DESCRIPTION|
|--|--|
|`Self`|The instance of the|

###

add_edge



```

add_edge(start_key: str | list[str], end_key: str) -> Self

```

Add a directed edge from the start node (or list of start nodes) to the end node.

When a single start node is provided, the graph will wait for that node to complete before executing the end node. When multiple start nodes are provided, the graph will wait for ALL of the start nodes to complete before executing the end node.
|PARAMETER|DESCRIPTION|
|--|--|
|`start_key`|The key(s) of the start node(s) of the edge.|
|`end_key`|The key of the end node of the edge.|
|RAISES|DESCRIPTION|
|--|--|
|`ValueError`|If the start key is|
|RETURNS|DESCRIPTION|
|--|--|
|`Self`|The instance of the|

…

Add a conditional edge from the starting node to any number of destination nodes.

|PARAMETER|DESCRIPTION|
|--|--|
|`source`|The starting node. This conditional edge will run when exiting this node.|
|`path`|The callable that determines the next node or nodes. If not specifying If it returns|
|`path_map`|Optional mapping of paths to node names. If omitted the paths returned by|
|RETURNS|DESCRIPTION|
|--|--|
|`Self`|The instance of the graph, allowing for method chaining.|
Warning

…

|PARAMETER|DESCRIPTION|
|--|--|
|`nodes`|A sequence of If no names are provided, the name will be inferred from the node object (e.g. a Each node will be executed in the order provided.|
|RAISES|DESCRIPTION|
|--|--|
|`ValueError`|If the sequence is empty.|
|`ValueError`|If the sequence contains duplicate node names.|
|RETURNS|DESCRIPTION|
|--|--|
|`Self`|The instance of the|

###

compile



```

compile(

checkpointer: Checkpointer = None,

*,

cache: BaseCache | None = None,

store: BaseStore | None = None,

interrupt_before: All | list[str] | None = None,

interrupt_after: All | list[str] | None = None,

debug: bool = False,

name: str | None = None,

) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]

```
Compiles the

`StateGraph` into a

`CompiledStateGraph` object.

The compiled graph implements the

`Runnable` interface and can be invoked,

streamed, batched, and run asynchronously.

…

##

CompiledStateGraph



Bases:

`Pregel[StateT, ContextT, InputT, OutputT]`,

`Generic[StateT, ContextT, InputT, OutputT]`
|METHOD|DESCRIPTION|
|--|--|
|`stream`|Stream graph steps for a single input.|
|`astream`|Asynchronously stream graph steps for a single input.|
|`invoke`|Run the graph with a single input and config.|
|`ainvoke`|Asynchronously run the graph with a single input and config.|
|`get_state`|Get the current state of the graph.|
|`aget_state`|Get the current state of the graph.|
|`get_state_history`|Get the history of the state of the graph.|
|`aget_state_history`|Asynchronously get the history of the state of the graph.|
|`update_state`|Update the state of the graph with the given values, as if they came from|
|`aupdate_state`|Asynchronously update the state of the graph with the given values, as if they came from|
|`bulk_update_state`|Apply updates to the graph state in bulk. Requires a checkpointer to be set.|
|`abulk_update_state`|Asynchronously apply updates to the graph state in bulk. Requires a checkpointer to be set.|
|`get_graph`|Return a drawable representation of the computation graph.|
|`aget_graph`|Return a drawable representation of the computation graph.|
|`get_subgraphs`|Get the subgraphs of the graph.|
|`aget_subgraphs`|Get the subgraphs of the graph.|
|`with_config`|Create a copy of the Pregel object with an updated config.|

…

interrupt_before: All | Sequence[str] | None = None,

interrupt_after: All | Sequence[str] | None = None,

durability: Durability | None = None,

subgraphs: bool = False,

debug: bool | None = None,

**kwargs: Unpack[DeprecatedKwargs],

) -> Iterator[dict[str, Any] | Any]

```
Stream graph steps for a single input.

|PARAMETER|DESCRIPTION|
|--|--|
|`input`|The input to the graph.|
|`config`|The configuration to use for the run.|
|`context`|The static context to use for the run. Added in version 0.6.0|
|`stream_mode`|The mode to stream output, defaults to Options are: You can pass a list as the See LangGraph streaming guide for more details.|
|`print_mode`|Accepts the same values as Does not affect the output of the graph in any way.|
|`output_keys`|The keys to stream, defaults to all non-context channels.|
|`interrupt_before`|Nodes to interrupt before, defaults to all nodes in the graph.|
|`interrupt_after`|Nodes to interrupt after, defaults to all nodes in the graph.|
|`durability`|The durability mode for the graph execution, defaults to Options are:|
|`subgraphs`|Whether to stream events from inside subgraphs, defaults to If See LangGraph streaming guide for more details.|
|YIELDS|DESCRIPTION|
|--|--|
|`dict[str, Any] | Any`|The output of each step in the graph. The output shape depends on the|

…

interrupt_before: All | Sequence[str] | None = None,

interrupt_after: All | Sequence[str] | None = None,

durability: Durability | None = None,

subgraphs: bool = False,

debug: bool | None = None,

**kwargs: Unpack[DeprecatedKwargs],

) -> AsyncIterator[dict[str, Any] | Any]

```
Asynchronously stream graph steps for a single input.

|PARAMETER|DESCRIPTION|
|--|--|
|`input`|The input to the graph.|
|`config`|The configuration to use for the run.|
|`context`|The static context to use for the run. Added in version 0.6.0|
|`stream_mode`|The mode to stream output, defaults to Options are: You can pass a list as the See LangGraph streaming guide for more details.|
|`print_mode`|Accepts the same values as Does not affect the output of the graph in any way.|
|`output_keys`|The keys to stream, defaults to all non-context channels.|
|`interrupt_before`|Nodes to interrupt before, defaults to all nodes in the graph.|
|`interrupt_after`|Nodes to interrupt after, defaults to all nodes in the graph.|
|`durability`|The durability mode for the graph execution, defaults to Options are:|
|`subgraphs`|Whether to stream events from inside subgraphs, defaults to If See LangGraph streaming guide for more details.|
|YIELDS|DESCRIPTION|
|--|--|
|`AsyncIterator[dict[str, Any] | Any]`|The output of each step in the graph. The output shape depends on the|

###

invoke



```

invoke(

input: InputT | Command | None,

config: RunnableConfig | None = None,

*,

context: ContextT | None = None,

stream_mode: StreamMode = "values",

print_mode: StreamMode | Sequence[StreamMode] = (),

output_keys: str | Sequence[str] | None = None,

interrupt_before: All | Sequence[str] | None = None,

interrupt_after: All | Sequence[str] | None = None,

durability: Durability | None = None,

**kwargs: Any,

) -> dict[str, Any] | Any

```
Run the graph with a single input and config.

|PARAMETER|DESCRIPTION|
|--|--|
|`input`|The input data for the graph. It can be a dictionary or any other type.|
|`config`|The configuration for the graph run.|
|`context`|The static context to use for the run. Added in version 0.6.0|
|`stream_mode`|The stream mode for the graph run.|
|`print_mode`|Accepts the same values as Does not affect the output of the graph in any way.|
|`output_keys`|The output keys to retrieve from the graph run.|
|`interrupt_before`|The nodes to interrupt the graph run before.|
|`interrupt_after`|The nodes to interrupt the graph run after.|
|`durability`|The durability mode for the graph execution, defaults to Options are:|
|`**kwargs`|Additional keyword arguments to pass to the graph run.|
|RETURNS|DESCRIPTION|
|--|--|
|`dict[str, Any] | Any`|The output of the graph run. If|
|`dict[str, Any] | Any`|If|

###

ainvoke

`async`

```

ainvoke(

input: InputT | Command | None,

config: RunnableConfig | None = None,

*,

context: ContextT | None = None,

stream_mode: StreamMode = "values",

print_mode: StreamMode | Sequence[StreamMode] = (),

output_keys: str | Sequence[str] | None = None,

interrupt_before: All | Sequence[str] | None = None,

interrupt_after: All | Sequence[str] | None = None,

durability: Durability | None = None,

**kwargs: Any,

) -> dict[str, Any] | Any

```
Asynchronously run the graph with a single input and config.

|PARAMETER|DESCRIPTION|
|--|--|
|`input`|The input data for the graph. It can be a dictionary or any other type.|
|`config`|The configuration for the graph run.|
|`context`|The static context to use for the run. Added in version 0.6.0|
|`stream_mode`|The stream mode for the graph run.|
|`print_mode`|Accepts the same values as Does not affect the output of the graph in any way.|
|`output_keys`|The output keys to retrieve from the graph run.|
|`interrupt_before`|The nodes to interrupt the graph run before.|
|`interrupt_after`|The nodes to interrupt the graph run after.|
|`durability`|The durability mode for the graph execution, defaults to Options are:|
|`**kwargs`|Additional keyword arguments to pass to the graph run.|
|RETURNS|DESCRIPTION|
|--|--|
|`dict[str, Any] | Any`|The output of the graph run. If|
|`dict[str, Any] | Any`|If|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to apply the updates to.|
|`supersteps`|A list of supersteps, each including a list of updates to apply sequentially to a graph state. Each update is a tuple of the form|
|RAISES|DESCRIPTION|
|--|--|
|`ValueError`|If no checkpointer is set or no updates are provided.|
|`InvalidUpdateError`|If an invalid update is provided.|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|The updated config.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to apply the updates to.|
|`supersteps`|A list of supersteps, each including a list of updates to apply sequentially to a graph state. Each update is a tuple of the form|
|RAISES|DESCRIPTION|
|--|--|
|`ValueError`|If no checkpointer is set or no updates are provided.|
|`InvalidUpdateError`|If an invalid update is provided.|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|The updated config.|

…

###

get_subgraphs



```

get_subgraphs(

*, namespace: str | None = None, recurse: bool = False

) -> Iterator[tuple[str, PregelProtocol]]

```

Get the subgraphs of the graph.

|PARAMETER|DESCRIPTION|
|--|--|
|`namespace`|The namespace to filter the subgraphs by.|
|`recurse`|Whether to recurse into the subgraphs. If|
|RETURNS|DESCRIPTION|
|--|--|
|`Iterator[tuple[str, PregelProtocol]]`|An iterator of the|

###

aget_subgraphs

`async`



```

aget_subgraphs(

*, namespace: str | None = None, recurse: bool = False

) -> AsyncIterator[tuple[str, PregelProtocol]]

```

Get the subgraphs of the graph.

|PARAMETER|DESCRIPTION|
|--|--|
|`namespace`|The namespace to filter the subgraphs by.|
|`recurse`|Whether to recurse into the subgraphs. If|
|RETURNS|DESCRIPTION|
|--|--|
|`AsyncIterator[tuple[str, PregelProtocol]]`|An iterator of the|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`left`|The base list of|
|`right`|The list of|
|`format`|The format to return messages in. If Requirement Must have|
|RETURNS|DESCRIPTION|
|--|--|
|`Messages`|A new list of messages with the messages from|
|`Messages`|If a message in|

## Basic usage

```

from langchain_core.messages import AIMessage, HumanMessage

msgs1 = [HumanMessage(content="Hello", id="1")]

msgs2 = [AIMessage(content="Hi there!", id="2")]

add_messages(msgs1, msgs2)

# [HumanMessage(content='Hello', id='1'), AIMessage(content='Hi there!', id='2')]

```

…

],

},



builder = StateGraph(State)

builder.add_node("chatbot", chatbot_node)

builder.set_entry_point("chatbot")

builder.set_finish_point("chatbot")

graph = builder.compile()

graph.invoke({"messages": []})

# {

# 'messages': [

# HumanMessage(

# content=[

# {"type": "text", "text": "Here's an image:"},

# LangGraph reference
Welcome to the LangGraph reference docs!
These pages detail the core interfaces you will use when building with LangGraph.
Each section covers a different part of the ecosystem.
##
`langgraph`¶
The core APIs for the LangGraph open source library.
- Graphs: Main graph abstraction and usage.
- Functional API: Functional programming interface for graphs.
- Pregel: Pregel-inspired computation model.
- Checkpointing: Saving and restoring graph state.
- Storage: Storage backends and options.
- Caching: Caching mechanisms for performance.
- Types: Type definitions for graph components.
- Runtime: Runtime configuration and options.
- Config: Configuration options.
- Errors: Error types and handling.
- Constants: Global constants.
- Channels: Message passing and channels.
Model Context Protocol (MCP) support
To use MCP tools in your LangGraph application, check out
`langchain-mcp-adapters`.
## Prebuilt components¶
Higher-level abstractions for common workflows, agents, and other patterns.
- Agents: Built-in agent patterns.
- Supervisor: Orchestration and delegation.
- Swarm: Multi-agent collaboration.

# Graph Definitions ¶

## StateGraph ¶

Bases: `Generic[StateT, ContextT, InputT, OutputT]`

A graph whose nodes communicate by reading and writing to a shared state.
The signature of each node is State -> Partial.

Each state key can optionally be annotated with a reducer function that
will be used to aggregate the values of that key received from multiple nodes.
The signature of a reducer function is (Value, Value) -> Value.

…

|Name|Type|Description|Default|
|--|--|--|--|
|`state_schema`|`type[StateT]`|The schema class that defines the state.|*required*|
|`context_schema`|`type[ContextT] | None`|The schema class that defines the runtime context. Use this to expose immutable context data to your nodes, like user_id, db_conn, etc.|`None`|
|`input_schema`|`type[InputT] | None`|The schema class that defines the input to the graph.|`None`|

…

```
from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated, TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import StateGraph
from langgraph.runtime import Runtime

def reducer(a: list, b: int | None) -> list:
 if b is not None:
 return a + [b]
 return a

class State(TypedDict):
 x: Annotated[list, reducer]

class Context(TypedDict):
 r: float

graph = StateGraph(state_schema=State, context_schema=Context)

def node(state: State, runtime: Runtime[Context]) -> dict:
 r = runtime.context.get("r", 1.0)
 x = state["x"][-1]
 next_value = x * r * (1 - x)
 return {"x": next_value}

graph.add_node("A", node)
graph.set_entry_point("A")
graph.set_finish_point("A")
compiled = graph.compile()

step1 = compiled.invoke({"x": 0.5}, context={"r": 3.0})
# {'x': [0.5, 0.75]}

```

…

|Name|Description|
|--|--|
|`add_node`|Add a new node to the state graph.|
|`add_edge`|Add a directed edge from the start node (or list of start nodes) to the end node.|
|`add_conditional_edges`|Add a conditional edge from the starting node to any number of destination nodes.|
|`add_sequence`|Add a sequence of nodes that will be executed in the provided order.|
|`compile`|Compiles the state graph into a `CompiledStateGraph` object.|

### add_node ¶

```
add_node(
 node: str | StateNode[NodeInputT, ContextT],
 action: StateNode[NodeInputT, ContextT] | None = None,
 *,
 defer: bool = False,
 metadata: dict[str, Any] | None = None,
 input_schema: type[NodeInputT] | None = None,
 retry_policy: (
 RetryPolicy | Sequence[RetryPolicy] | None
 ) = None,
 cache_policy: CachePolicy | None = None,
 destinations: (
 dict[str, str] | tuple[str, ...] | None
 ) = None,
 **kwargs: Unpack[DeprecatedKwargs]
) -> Self

```

…

|Name|Type|Description|Default|
|--|--|--|--|
|`node`|`str | StateNode[NodeInputT, ContextT]`|The function or runnable this node will run. If a string is provided, it will be used as the node name, and action will be used as the function or runnable.|*required*|
|`action`|`StateNode[NodeInputT, ContextT] | None`|The action associated with the node. (default: None) Will be used as the node function or runnable if `node` is a string (node name).|`None`|

…

|`destinations`|`dict[str, str] | tuple[str, ...] | None`|Destinations that indicate where a node can route to. This is useful for edgeless graphs with nodes that return `Command` objects. If a dict is provided, the keys will be used as the target node names and the values will be used as the labels for the edges. If a tuple is provided, the values will be used as the target node names. NOTE: this is only used for graph rendering and doesn't have any effect on the graph execution.|`None`|

…

```
from typing_extensions import TypedDict

from langchain_core.runnables import RunnableConfig
from langgraph.graph import START, StateGraph

class State(TypedDict):
 x: int

def my_node(state: State, config: RunnableConfig) -> State:
 return {"x": state["x"] + 1}

builder = StateGraph(State)
builder.add_node(my_node) # node name will be 'my_node'
builder.add_edge(START, "my_node")
graph = builder.compile()
graph.invoke({"x": 1})
# {'x': 2}

```

…

|Name|Type|Description|Default|
|--|--|--|--|
|`source`|`str`|The starting node. This conditional edge will run when exiting this node.|*required*|
|`path`|`Callable[..., Hashable | Sequence[Hashable]] | Callable[..., Awaitable[Hashable | Sequence[Hashable]]] | Runnable[Any, Hashable | Sequence[Hashable]]`|The callable that determines the next node or nodes. If not specifying `path_map` it should return one or more nodes. If it returns END, the graph will stop execution.|*required*|

…

|Name|Type|Description|Default|
|--|--|--|--|
|`nodes`|`Sequence[StateNode[NodeInputT, ContextT] | tuple[str, StateNode[NodeInputT, ContextT]]]`|A sequence of StateNodes (callables that accept a state arg) or (name, StateNode) tuples. If no names are provided, the name will be inferred from the node object (e.g. a runnable or a callable name). Each node will be executed in the order provided.|*required*|

…

### compile ¶

```
compile(
 checkpointer: Checkpointer = None,
 *,
 cache: BaseCache | None = None,
 store: BaseStore | None = None,
 interrupt_before: All | list[str] | None = None,
 interrupt_after: All | list[str] | None = None,
 debug: bool = False,
 name: str | None = None
) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]

```

…

|Name|Type|Description|Default|
|--|--|--|--|
|`checkpointer`|`Checkpointer`|A checkpoint saver object or flag. If provided, this Checkpointer serves as a fully versioned "short-term memory" for the graph, allowing it to be paused, resumed, and replayed from any point. If None, it may inherit the parent graph's checkpointer when used as a subgraph. If False, it will not use or inherit any checkpointer.|`None`|
|`interrupt_before`|`All | list[str] | None`|An optional list of node names to interrupt before.|`None`|

…

## CompiledStateGraph ¶

Bases: `Pregel[StateT, ContextT, InputT, OutputT]`, `Generic[StateT, ContextT, InputT, OutputT]`

Methods:
|Name|Description|
|--|--|
|`stream`|Stream graph steps for a single input.|
|`astream`|Asynchronously stream graph steps for a single input.|
|`invoke`|Run the graph with a single input and config.|
|`ainvoke`|Asynchronously invoke the graph on a single input.|
|`get_state`|Get the current state of the graph.|
|`aget_state`|Get the current state of the graph.|
|`get_state_history`|Get the history of the state of the graph.|
|`aget_state_history`|Asynchronously get the history of the state of the graph.|
|`update_state`|Update the state of the graph with the given values, as if they came from|
|`aupdate_state`|Asynchronously update the state of the graph with the given values, as if they came from|
|`bulk_update_state`|Apply updates to the graph state in bulk. Requires a checkpointer to be set.|
|`abulk_update_state`|Asynchronously apply updates to the graph state in bulk. Requires a checkpointer to be set.|
|`get_graph`|Return a drawable representation of the computation graph.|

…

### stream ¶

```
stream(
 input: InputT | Command | None,
 config: RunnableConfig | None = None,
 *,
 context: ContextT | None = None,
 stream_mode: (
 StreamMode | Sequence[StreamMode] | None
 ) = None,
 print_mode: StreamMode | Sequence[StreamMode] = (),
 output_keys: str | Sequence[str] | None = None,
 interrupt_before: All | Sequence[str] | None = None,
 interrupt_after: All | Sequence[str] | None = None,
 durability: Durability | None = None,
 subgraphs: bool = False,
 debug: bool | None = None,
 **kwargs: Unpack[DeprecatedKwargs]
) -> Iterator[dict[str, Any] | Any]

```

…

|Name|Type|Description|Default|
|--|--|--|--|
|`stream_mode`|`StreamMode | Sequence[StreamMode] | None`|The mode to stream output, defaults to `self.stream_mode`. Options are:- `"values"`: Emit all values in the state after each step, including interrupts. When used with functional API, values are emitted once at the end of the workflow. - `"updates"`: Emit only the node or task names and updates returned by the nodes or tasks after each step. If multiple updates are made in the same step (e.g. multiple nodes are run) then those updates are emitted separately. - `"custom"`: Emit custom data from inside nodes or tasks using `StreamWriter`. - `"messages"`: Emit LLM messages token-by-token together with metadata for any LLM invocations inside nodes or tasks. Will be emitted as 2-tuples `(LLM token, metadata)`. - `"checkpoints"`: Emit an event when a checkpoint is created, in the same format as returned by get_state(). - `"tasks"`: Emit events when tasks start and finish, including their results and errors. You can pass a list as the `stream_mode` parameter to stream multiple modes at once. The streamed outputs will be tuples of `(mode, data)`.See LangGraph streaming guide for more details.|`None`|
|`print_mode`|`StreamMode | Sequence[StreamMode]`|Accepts the same values as `stream_mode`, but only prints the output to the console, for debugging purposes. Does not affect the output of the graph in any way.|`()`|
|`output_keys`|`str | Sequence[str] | None`|The keys to stream, defaults to all non-context channels.|`None`|
|`interrupt_before`|`All | Sequence[str] | None`|Nodes to interrupt before, defaults to all nodes in the graph.|`None`|
|`interrupt_after`|`All | Sequence[str] | None`|Nodes to interrupt after, defaults to all nodes in the graph.|`None`|
|`durability`|`Durability | None`|The durability mode for the graph execution, defaults to "async". Options are: - `"sync"`: Changes are persisted synchronously before the next step starts. - `"async"`: Changes are persisted asynchronously while the next step executes. - `"exit"`: Changes are persisted only when the graph exits.|`None`|

…

### astream async ¶

```
astream(
 input: InputT | Command | None,
 config: RunnableConfig | None = None,
 *,
 context: ContextT | None = None,
 stream_mode: (
 StreamMode | Sequence[StreamMode] | None
 ) = None,
 print_mode: StreamMode | Sequence[StreamMode] = (),
 output_keys: str | Sequence[str] | None = None,
 interrupt_before: All | Sequence[str] | None = None,
 interrupt_after: All | Sequence[str] | None = None,
 durability: Durability | None = None,
 subgraphs: bool = False,
 debug: bool | None = None,
 **kwargs: Unpack[DeprecatedKwargs]
) -> AsyncIterator[dict[str, Any] | Any]

```

…

|Name|Type|Description|Default|
|--|--|--|--|
|`stream_mode`|`StreamMode | Sequence[StreamMode] | None`|The mode to stream output, defaults to `self.stream_mode`. Options are:- `"values"`: Emit all values in the state after each step, including interrupts. When used with functional API, values are emitted once at the end of the workflow. - `"updates"`: Emit only the node or task names and updates returned by the nodes or tasks after each step. If multiple updates are made in the same step (e.g. multiple nodes are run) then those updates are emitted separately. - `"custom"`: Emit custom data from inside nodes or tasks using `StreamWriter`. - `"messages"`: Emit LLM messages token-by-token together with metadata for any LLM invocations inside nodes or tasks. Will be emitted as 2-tuples `(LLM token, metadata)`. - `"debug"`: Emit debug events with as much information as possible for each step. You can pass a list as the `stream_mode` parameter to stream multiple modes at once. The streamed outputs will be tuples of `(mode, data)`.See LangGraph streaming guide for more details.|`None`|
|`print_mode`|`StreamMode | Sequence[StreamMode]`|Accepts the same values as `stream_mode`, but only prints the output to the console, for debugging purposes. Does not affect the output of the graph in any way.|`()`|
|`output_keys`|`str | Sequence[str] | None`|The keys to stream, defaults to all non-context channels.|`None`|
|`interrupt_before`|`All | Sequence[str] | None`|Nodes to interrupt before, defaults to all nodes in the graph.|`None`|
|`interrupt_after`|`All | Sequence[str] | None`|Nodes to interrupt after, defaults to all nodes in the graph.|`None`|
|`durability`|`Durability | None`|The durability mode for the graph execution, defaults to "async". Options are: - `"sync"`: Changes are persisted synchronously before the next step starts. - `"async"`: Changes are persisted asynchronously while the next step executes. - `"exit"`: Changes are persisted only when the graph exits.|`None`|

…

### invoke ¶

```
invoke(
 input: InputT | Command | None,
 config: RunnableConfig | None = None,
 *,
 context: ContextT | None = None,
 stream_mode: StreamMode = "values",
 print_mode: StreamMode | Sequence[StreamMode] = (),
 output_keys: str | Sequence[str] | None = None,
 interrupt_before: All | Sequence[str] | None = None,
 interrupt_after: All | Sequence[str] | None = None,
 durability: Durability | None = None,
 **kwargs: Any
) -> dict[str, Any] | Any

```

…

|Name|Type|Description|Default|
|--|--|--|--|
|`input`|`InputT | Command | None`|The input data for the graph. It can be a dictionary or any other type.|*required*|
|`config`|`RunnableConfig | None`|Optional. The configuration for the graph run.|`None`|
|`context`|`ContextT | None`|The static context to use for the run. Added in version 0.6.0.|`None`|

…

|`interrupt_before`|`All | Sequence[str] | None`|Optional. The nodes to interrupt the graph run before.|`None`|
|`interrupt_after`|`All | Sequence[str] | None`|Optional. The nodes to interrupt the graph run after.|`None`|
|`durability`|`Durability | None`|The durability mode for the graph execution, defaults to "async". Options are: - `"sync"`: Changes are persisted synchronously before the next step starts. - `"async"`: Changes are persisted asynchronously while the next step executes. - `"exit"`: Changes are persisted only when the graph exits.|`None`|

…

|Name|Type|Description|Default|
|--|--|--|--|
|`print_mode`|`StreamMode | Sequence[StreamMode]`|Accepts the same values as `stream_mode`, but only prints the output to the console, for debugging purposes. Does not affect the output of the graph in any way.|`()`|
|`output_keys`|`str | Sequence[str] | None`|Optional. The output keys to include in the result. Default is None.|`None`|
|`interrupt_before`|`All | Sequence[str] | None`|Optional. The nodes to interrupt before. Default is None.|`None`|
|`interrupt_after`|`All | Sequence[str] | None`|Optional. The nodes to interrupt after. Default is None.|`None`|
|`durability`|`Durability | None`|The durability mode for the graph execution, defaults to "async". Options are: - `"sync"`: Changes are persisted synchronously before the next step starts. - `"async"`: Changes are persisted asynchronously while the next step executes. - `"exit"`: Changes are persisted only when the graph exits.|`None`|
|`**kwargs`|`Any`|Additional keyword arguments.|`{}`|

# Reference¶
Welcome to the LangGraph reference docs!
These pages detail the core interfaces you will use when building with LangGraph.
Each section covers a different part of the ecosystem.
Tip
If you are just getting started, see LangGraph basics for an introduction to the main concepts and usage patterns.
## LangGraph¶
The core APIs for the LangGraph open source library.
- Graphs: Main graph abstraction and usage.
- Functional API: Functional programming interface for graphs.
- Pregel: Pregel-inspired computation model.
- Checkpointing: Saving and restoring graph state.
- Storage: Storage backends and options.
- Caching: Caching mechanisms for performance.
- Types: Type definitions for graph components.
- Config: Configuration options.
- Errors: Error types and handling.
- Constants: Global constants.
- Channels: Message passing and channels.

This is a part of LangChain Open Tutorial
## Overview
In this tutorial, you will learn how to use
`LangGraph` to create foundational graph structures.
You will learn the following:
The steps to define a graph
How to use conditional edges and different flow variations
Re-search graph structure
Multi-LLM graph structure
Query rewrite graph structure
SQL RAG graph structure
### Table of Contents
...
%%capture --no-stderr
%pip install langchain-opentutorial
```
```
# Install required packages
from langchain_opentutorial import package
package.install(
"langsmith",
"langchain_core",
"langgraph",
"typing",
"IPython",
],
verbose=False,
upgrade=False,
```
…
## Steps for Defining a Graph
To define a graph with
`LangGraph`, you need to define
**State** , **Node** , and **Graph** , and then compile them.
If necessary, you can flexibly adjust the graph flow by adding conditional edges to nodes using
`add_conditional_edges()`.
### Define State
**State** defines the shared state between the nodes in the graph.
It uses the
`TypedDict` format and adds metadata to type hints using
`Annotated` to provide detailed information.
…
### Define Node
Define the nodes that process each step.
These are usually implemented as Python functions, with
**State** as both input and output.
```
def retrieve(state: GraphState) -> GraphState:
# retrieve: search
documents = "searched documents"
return {"context": documents}
def rewrite_query(state: GraphState) -> GraphState:
# Query Transform: rewrite query
documents = "searched documents"
return GraphState(context=documents)
def llm_gpt_execute(state: GraphState) -> GraphState:
…
# Search on Web
documents = state["context"] = "existing documents"
searched_documents = "searched documents"
documents += searched_documents
return GraphState(context=documents)
def get_table_info(state: GraphState) -> GraphState:
# Get Table Info
table_info = "table information"
return GraphState(context=table_info)
…
def validate_sql_query(state: GraphState) -> GraphState:
# Validate SQL Query
binary_score = "SQL query validation result"
return GraphState(binary_score=binary_score)
def handle_error(state: GraphState) -> GraphState:
# Error Handling
error = "error occurred"
return GraphState(context=error)
def decision(state: GraphState) -> GraphState:
# Decision Making
decision = "decision"
# Additional logic can be added here.
if state["binary_score"] == "yes":
return "exit"
else:
return "re_search"
```
### Define Graph
Connect nodes with
**Edge** .
Using conditional edges, you can determine the next
**Node** to execute based on the current **State** .
```
from IPython.display import Image, display
from langgraph.graph import END, StateGraph
from langgraph.checkpoint.memory import MemorySaver
# Import StateGraph and END from langgraph.graph.
workflow = StateGraph(GraphState)
# Add nodes.
workflow.add_node("retrieve", retrieve)
workflow.add_node("GPT_request", llm_gpt_execute)
…
# Set the entry point.
workflow.set_entry_point("retrieve")
# Set up memory storage for recording.
memory = MemorySaver()
# Compile the graph.
app = workflow.compile(checkpointer=memory)
# Visualize the graph
display(Image(app.get_graph().draw_mermaid_png()))
```
## Various Graph Structures
In this section, you will learn about different graph structures using conditional edges.
The graph structures you will learn are as follows:
Re-search graph structure
Multi-LLM graph structure
Query rewrite graph structure
SQL RAG graph structure
### Re-search Graph Structure
The Re-search Graph inspects the output from the GPT model and selects either
`re_search` or
`exit`.
This allows you to obtain more relevant results for the query.
The execution flow is as follows:
A conditional edge is added to the
`Aggregation_results`node.
…
```
# Import StateGraph and END from langgraph.graph.
workflow = StateGraph(GraphState)
# Add nodes.
workflow.add_node("retrieve", retrieve)
workflow.add_node("GPT_request", llm_gpt_execute)
workflow.add_node("GPT_relevance_check", relevance_check)
workflow.add_node("Aggregation_results", sum_up)
…
decision,
"re_search": "retrieve", # If the relevance check result is ambiguous, generate the answer again.
"exit": END, # If relevant, exit.
},
# Set the entry point.
workflow.set_entry_point("retrieve")
# Set up memory storage for recording.
memory = MemorySaver()
# Compile the graph.
app = workflow.compile(checkpointer=memory)
# Visualize the graph
display(Image(app.get_graph().draw_mermaid_png()))
...
The Multi-LLM graph uses various LLM models to generate results.
This allows for obtaining a variety of answers.
```
# Import StateGraph and END from langgraph.graph.
workflow = StateGraph(GraphState)
# Add nodes.
workflow.add_node("retrieve", retrieve)
workflow.add_node("GPT_request", llm_gpt_execute)
workflow.add_node("GPT_relevance_check", relevance_check)
# add a new node for Claude
workflow.add_node("Claude_request", llm_claude_execute)
…
# Set the entry point.
workflow.set_entry_point("retrieve")
# Set up memory storage for recording.
memory = MemorySaver()
# Compile the graph.
app = workflow.compile(checkpointer=memory)
# Visualize the graph
...
The Query Rewrite Graph is a structure that adds the
`rewrite_query` node to the Re-search Graph structure.
The rewrite node for the query rewrites the question to obtain more refined results.
```
# Import StateGraph and END from langgraph.graph.
workflow = StateGraph(GraphState)
# Add nodes.
workflow.add_node("retrieve", retrieve)
# add a new node for rewriting the query
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_node("GPT_request", llm_gpt_execute)
workflow.add_node("Claude_request", llm_claude_execute)
…
"Aggregation_results", # Pass the result from the relevance check node to the decision function.
decision,
"re_search": "rewrite_query", # If the relevance check result is ambiguous, generate the answer again.
"exit": END, # If relevant, exit.
},
# Set the entry point.
workflow.set_entry_point("retrieve")
# Set up memory storage for recording.
memory = MemorySaver()
# Compile the graph.
app = workflow.compile(checkpointer=memory)
# Visualize the graph
...
The SQL RAG Graph is a structure that combines Conventional RAG with SQL RAG.
It uses rewrite nodes for the question and query to generate precise results based on the requirements.
```
# Import StateGraph and END from langgraph.graph
workflow = StateGraph(GraphState)
# Add nodes.
workflow.add_node("retrieve", retrieve)
workflow.add_node("rewrite_query", rewrite_query)
workflow.add_node("rewrite_question", rewrite_query)
workflow.add_node("GPT_request", llm_gpt_execute)
workflow.add_node("GPT_relevance_check", relevance_check)
…
"PASS": "GPT_request",
},
workflow.add_edge("rewrite_query", "execute_sql_query")
workflow.add_edge("rewrite_question", "rewrite_query")
workflow.add_edge("GPT_request", "GPT_relevance_check")
workflow.add_edge("GPT_relevance_check", "Aggregation_results")
workflow.add_edge("Aggregation_results", END)
# Set the entry point.
workflow.set_entry_point("retrieve")
# Set up memory storage for recording.
memory = MemorySaver()
# Compile the graph.
app = workflow.compile(checkpointer=memory)
# Visualize the graph
display(Image(app.get_graph().draw_mermaid_png()))
```