# Source: https://www.langgraphcn.org/reference/graphs/
# Title: 图定义 / Graphs reference (LangGraphCN) — StateGraph signature and reducers
# Fetched via: search
# Date: 2026-04-10

# 图定义¶
##

StateGraph



Bases:

`Generic[StateT, InputT, OutputT]`

A graph whose nodes communicate by reading and writing to a shared state.

The signature of each node is State -> Partial

Each state key can optionally be annotated with a reducer function that will be used to aggregate the values of that key received from multiple nodes. The signature of a reducer function is (Value, Value) -> Value.
Parameters:

|Name|Type|Description|Default|
|--|--|--|--|
|`state_schema`|`type[StateT]`|The schema class that defines the state.|required|
|`config_schema`|`type[Any] | None`|The schema class that defines the configuration. Use this to expose configurable parameters in your API.|`None`|

## Example
```
from langchain_core.runnables import RunnableConfig

from typing_extensions import Annotated, TypedDict

from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph

def reducer(a: list, b: int | None) -> list:

if b is not None:

return a + [b]
return a

class State(TypedDict):

x: Annotated[list, reducer]

class ConfigSchema(TypedDict):

r: float

graph = StateGraph(State, config_schema=ConfigSchema)

def node(state: State, config: RunnableConfig) -> dict:

r = config["configurable"].get("r", 1.0)
x = state["x"][-1]

next_value = x * r * (1 - x)

return {"x": next_value}

graph.add_node("A", node)

graph.set_entry_point("A")

graph.set_finish_point("A")

compiled = graph.compile()

print(compiled.config_specs)

# [ConfigurableFieldSpec(id='r', annotation=<class 'float'>, name=None, description=None, default=None, is_shared=False, dependencies=None)]

…

|Name|Description|
|--|--|
|`add_node`|Add a new node to the state graph.|
|`add_edge`|Add a directed edge from the start node (or list of start nodes) to the end node.|
|`add_conditional_edges`|Add a conditional edge from the starting node to any number of destination nodes.|
|`add_sequence`|Add a sequence of nodes that will be executed in the provided order.|
|`compile`|Compiles the state graph into a|

###

add_node
```

add_node(

node: str | StateNode[StateT],

action: StateNode[StateT] | None = None,

*,

defer: bool = False,

metadata: dict[str, Any] | None = None,

input_schema: type[Any] | None = None,

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
Add a new node to the state graph.

Parameters:
|Name|Type|Description|Default|
|--|--|--|--|
|`node`|`str | StateNode[StateT]`|The function or runnable this node will run. If a string is provided, it will be used as the node name, and action will be used as the function or runnable.|required|

…

|`metadata`|`dict[str, Any] | None`|The metadata associated with the node. (default: None)|`None`|
|`input_schema`|`type[Any] | None`|The input schema for the node. (default: the graph's state schema)|`None`|
|`retry_policy`|`RetryPolicy | Sequence[RetryPolicy] | None`|The retry policy for the node. (default: None) If a sequence is provided, the first matching policy will be applied.|`None`|
|`cache_policy`|`CachePolicy | None`|The cache policy for the node. (default: None)|`None`|
|`destinations`|`dict[str, str] | tuple[str, ...] | None`|Destinations that indicate where a node can route to. This is useful for edgeless graphs with nodes that return|`None`|

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

Returns:

|Name|Type|Description|
|--|--|--|
|`Self`|`Self`|The instance of the state graph, allowing for method chaining.|

###

add_edge



```

add_edge(start_key: str | list[str], end_key: str) -> Self

```

Add a directed edge from the start node (or list of start nodes) to the end node.

When a single start node is provided, the graph will wait for that node to complete before executing the end node. When multiple start nodes are provided, the graph will wait for ALL of the start nodes to complete before executing the end node.
Parameters:

|Name|Type|Description|Default|
|--|--|--|--|
|`start_key`|`str | list[str]`|The key(s) of the start node(s) of the edge.|required|
|`end_key`|`str`|The key of the end node of the edge.|required|
Raises:
|Type|Description|
|--|--|
|`ValueError`|If the start key is 'END' or if the start key or end key is not present in the graph.|
Returns:

|Name|Type|Description|
|--|--|--|
|`Self`|`Self`|The instance of the state graph, allowing for method chaining.|

…

Add a conditional edge from the starting node to any number of destination nodes.

Parameters:
|Name|Type|Description|Default|
|--|--|--|--|
|`source`|`str`|The starting node. This conditional edge will run when exiting this node.|required|
|`path`|`Callable[..., Hashable | list[Hashable]] | Callable[..., Awaitable[Hashable | list[Hashable]]] | Runnable[Any, Hashable | list[Hashable]]`|The callable that determines the next node or nodes. If not specifying|required|
|`path_map`|`dict[Hashable, str] | list[str] | None`|Optional mapping of paths to node names. If omitted the paths returned by|`None`|
Returns:

|Name|Type|Description|
|--|--|--|
|`Self`|`Self`|The instance of the graph, allowing for method chaining.|

…

|Name|Type|Description|Default|
|--|--|--|--|
|`nodes`|`Sequence[StateNode[StateT] | tuple[str, StateNode[StateT]]]`|A sequence of StateNodes (callables that accept a state arg) or (name, StateNode) tuples. If no names are provided, the name will be inferred from the node object (e.g. a runnable or a callable name). Each node will be executed in the order provided.|required|
Raises:

|Type|Description|
|--|--|
|`ValueError`|if the sequence is empty.|
|`ValueError`|if the sequence contains duplicate node names.|
Returns:

|Name|Type|Description|
|--|--|--|
|`Self`|`Self`|The instance of the state graph, allowing for method chaining.|

…

Compiles the state graph into a

`CompiledStateGraph` object.

The compiled graph implements the

`Runnable` interface and can be invoked,

streamed, batched, and run asynchronously.

Parameters:

…

|`interrupt_before`|`All | list[str] | None`|An optional list of node names to interrupt before.|`None`|
|`interrupt_after`|`All | list[str] | None`|An optional list of node names to interrupt after.|`None`|
|`debug`|`bool`|A flag indicating whether to enable debug mode.|`False`|
|`name`|`str | None`|The name to use for the compiled graph.|`None`|
Returns:

|Name|Type|Description|
|--|--|--|
|`CompiledStateGraph`|`CompiledStateGraph[StateT, InputT]`|The compiled state graph.|

##

CompiledStateGraph



Bases:

`Pregel[StateT, InputT, OutputT]`,

`Generic[StateT, InputT, OutputT]`

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
|`aget_graph`|Return a drawable representation of the computation graph.|
|`get_subgraphs`|Get the subgraphs of the graph.|
|`aget_subgraphs`|Get the subgraphs of the graph.|
|`with_config`|Create a copy of the Pregel object with an updated config.|

…

Stream graph steps for a single input.

Parameters:
|Name|Type|Description|Default|
|--|--|--|--|
|`input`|`InputT`|The input to the graph.|required|
|`config`|`RunnableConfig | None`|The configuration to use for the run.|`None`|
|`stream_mode`|`StreamMode | list[StreamMode] | None`|The mode to stream output, defaults to You can pass a list as the See LangGraph streaming guide for more details.|`None`|
|`output_keys`|`str | Sequence[str] | None`|The keys to stream, defaults to all non-context channels.|`None`|
|`interrupt_before`|`All | Sequence[str] | None`|Nodes to interrupt before, defaults to all nodes in the graph.|`None`|
|`interrupt_after`|`All | Sequence[str] | None`|Nodes to interrupt after, defaults to all nodes in the graph.|`None`|
|`checkpoint_during`|`bool | None`|Whether to checkpoint intermediate steps, defaults to False. If False, only the final checkpoint is saved.|`None`|
|`debug`|`bool | None`|Whether to print debug information during execution, defaults to False.|`None`|
|`subgraphs`|`bool`|Whether to stream events from inside subgraphs, defaults to False. If True, the events will be emitted as tuples See LangGraph streaming guide for more details.|`False`|
Yields:

|Type|Description|
|--|--|
|`dict[str, Any] | Any`|The output of each step in the graph. The output shape depends on the stream_mode.|

…

Asynchronously stream graph steps for a single input.

Parameters:
|Name|Type|Description|Default|
|--|--|--|--|
|`input`|`InputT`|The input to the graph.|required|
|`config`|`RunnableConfig | None`|The configuration to use for the run.|`None`|
|`stream_mode`|`StreamMode | list[StreamMode] | None`|The mode to stream output, defaults to You can pass a list as the See LangGraph streaming guide for more details.|`None`|
|`output_keys`|`str | Sequence[str] | None`|The keys to stream, defaults to all non-context channels.|`None`|
|`interrupt_before`|`All | Sequence[str] | None`|Nodes to interrupt before, defaults to all nodes in the graph.|`None`|
|`interrupt_after`|`All | Sequence[str] | None`|Nodes to interrupt after, defaults to all nodes in the graph.|`None`|
|`checkpoint_during`|`bool | None`|Whether to checkpoint intermediate steps, defaults to False. If False, only the final checkpoint is saved.|`None`|
|`debug`|`bool | None`|Whether to print debug information during execution, defaults to False.|`None`|
|`subgraphs`|`bool`|Whether to stream events from inside subgraphs, defaults to False. If True, the events will be emitted as tuples See LangGraph streaming guide for more details.|`False`|
Yields:

|Type|Description|
|--|--|
|`AsyncIterator[dict[str, Any] | Any]`|The output of each step in the graph. The output shape depends on the stream_mode.|

…

Run the graph with a single input and config.

Parameters:
|Name|Type|Description|Default|
|--|--|--|--|
|`input`|`InputT`|The input data for the graph. It can be a dictionary or any other type.|required|
|`config`|`RunnableConfig | None`|Optional. The configuration for the graph run.|`None`|
|`stream_mode`|`StreamMode`|Optional[str]. The stream mode for the graph run. Default is "values".|`'values'`|
|`output_keys`|`str | Sequence[str] | None`|Optional. The output keys to retrieve from the graph run.|`None`|
|`interrupt_before`|`All | Sequence[str] | None`|Optional. The nodes to interrupt the graph run before.|`None`|
|`interrupt_after`|`All | Sequence[str] | None`|Optional. The nodes to interrupt the graph run after.|`None`|
|`debug`|`bool | None`|Optional. Enable debug mode for the graph run.|`None`|
|`**kwargs`|`Any`|Additional keyword arguments to pass to the graph run.|`{}`|
Returns:

|Type|Description|
|--|--|
|`dict[str, Any] | Any`|The output of the graph run. If stream_mode is "values", it returns the latest output.|
|`dict[str, Any] | Any`|If stream_mode is not "values", it returns a list of output chunks.|

…

Asynchronously invoke the graph on a single input.

Parameters:
|Name|Type|Description|Default|
|--|--|--|--|
|`input`|`InputT`|The input data for the computation. It can be a dictionary or any other type.|required|
|`config`|`RunnableConfig | None`|Optional. The configuration for the computation.|`None`|
|`stream_mode`|`StreamMode`|Optional. The stream mode for the computation. Default is "values".|`'values'`|
|`output_keys`|`str | Sequence[str] | None`|Optional. The output keys to include in the result. Default is None.|`None`|

…

|`debug`|`bool | None`|Optional. Whether to enable debug mode. Default is None.|`None`|
|`**kwargs`|`Any`|Additional keyword arguments.|`{}`|
Returns:

|Type|Description|
|--|--|
|`dict[str, Any] | Any`|The result of the computation. If stream_mode is "values", it returns the latest value.|
|`dict[str, Any] | Any`|If stream_mode is "chunks", it returns a list of chunks.|

…

|Name|Type|Description|Default|
|--|--|--|--|
|`config`|`RunnableConfig`|The config to apply the updates to.|required|
|`supersteps`|`Sequence[Sequence[StateUpdate]]`|A list of supersteps, each including a list of updates to apply sequentially to a graph state. Each update is a tuple of the form|required|

…

|Name|Type|Description|Default|
|--|--|--|--|
|`config`|`RunnableConfig`|The config to apply the updates to.|required|
|`supersteps`|`Sequence[Sequence[StateUpdate]]`|A list of supersteps, each including a list of updates to apply sequentially to a graph state. Each update is a tuple of the form|required|

…

###

get_subgraphs



```

get_subgraphs(

*, namespace: str | None = None, recurse: bool = False

) -> Iterator[tuple[str, PregelProtocol]]

```

Get the subgraphs of the graph.

Parameters:

|Name|Type|Description|Default|
|--|--|--|--|
|`namespace`|`str | None`|The namespace to filter the subgraphs by.|`None`|
|`recurse`|`bool`|Whether to recurse into the subgraphs. If False, only the immediate subgraphs will be returned.|`False`|
Returns:

…

|Name|Type|Description|Default|
|--|--|--|--|
|`namespace`|`str | None`|The namespace to filter the subgraphs by.|`None`|
|`recurse`|`bool`|Whether to recurse into the subgraphs. If False, only the immediate subgraphs will be returned.|`False`|
Returns:

|Type|Description|
|--|--|
|`AsyncIterator[tuple[str, PregelProtocol]]`|AsyncIterator[tuple[str, PregelProtocol]]: An iterator of the (namespace, subgraph) pairs.|

Course
Imagine you're building a complex, multi-agent large language model (LLM) application.
...
This is where LangGraph can help.
LangGraph is a library within the LangChain ecosystem designed to tackle these challenges head-on.
LangGraph provides a framework for defining, coordinating, and executing multiple LLM agents (or chains) in a structured manner.
It simplifies the development process by enabling the creation of cyclical graphs, which are essential for developing agent runtimes.
With LangGraph, we can easily build robust, scalable, and flexible multi-agent systems.
If you want to learn more about the LangChain ecosystem, I recommend this introduction to LangChain.
...
LangGraph enables us to create stateful, multi-actor applications utilizing LLMs as easily as possible.
It extends the capabilities of LangChain, introducing the ability to create and manage cyclical graphs, which are pivotal for developing sophisticated agent runtimes.
The core concepts of LangGraph include: graph structure, state management, and coordination.
### Graph structure
Imagine your application as a directed graph.
In LangGraph, each node represents an LLM agent, and the edges are the communication channels between these agents.
This structure allows for clear and manageable workflows, where each agent performs specific tasks and passes information to other agents as needed.
### State management
One of LangGraph's standout features is its automatic state management.
This feature enables us to track and persist information across multiple interactions.
As agents perform their tasks, the state is dynamically updated, ensuring the system maintains context and responds appropriately to new inputs.
### Coordination
LangGraph ensures agents execute in the correct order and that necessary information is exchanged seamlessly.
This coordination is vital for complex applications where multiple agents need to work together to achieve a common goal.
By managing the flow of data and the sequence of operations, LangGraph allows developers to focus on the high-level logic of their applications rather than the intricacies of agent coordination.
## Why LangGraph?
...
This means developers can define their workflows and logic without worrying about the underlying mechanisms that ensure data consistency and proper execution order.
...
Its robust architecture can handle a high volume of interactions and complex workflows, enabling the development of scalable systems that can grow with your needs.
...
Nodes: Nodes represent units of work within your LangGraph.
They are typically Python functions that perform a specific task, such as:
- Interacting with an LLM
- Calling a tool or API
- Performing some data manipulation
- Receiving user input
- Executing business logic
In LangGraph, you can add nodes using the
```
graph.add_node(name, value)
```
syntax.
Edges: Edges are communication channels between nodes.
They define the flow of information and the order of execution.
You can add edges using the
```
graph.add_edge(node1, node2)
```
syntax.
State: The state is a central object updated over time by the nodes in the graph.
It manages the internal state of your application and can be overridden or added to, depending on the application's requirements.
This state can hold things such as:
- Conversation history: A list of messages between the agent and the user.
- Contextual data: Information relevant to the current task or interaction.
- Internal variables: Flags, counters, or other variables to track the agent's progress and behavior.
…
### Step 1: Define the StateGraph
Define a
…
```
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
class State(TypedDict):
# messages have the type "list".
# The add_messages function appends messages to the list, rather than overwriting them
messages: Annotated[list, add_messages]
graph_builder = StateGraph(State)
```
…
node as both the entry and finish points of the graph to indicate where to start and end the process.
```
# Set entry and finish points
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
```
Step 4: Compile and Visualize the Graph
Compile the graph to create a CompiledGraph object, and optionally, we can visualize the graph structure using the code below:
…
### Custom node types
LangGraph allows you to create custom node types to implement complex agent logic.
This provides flexibility and control over your application's behavior.
```
from typing import Annotated
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
class MyCustomNode:
def __init__(self, llm):
self.llm = llm
def __call__(self, state):
# Implement your custom logic here
# Access the state and perform actions
messages = state["messages"]
response = self.llm.invoke(messages)
return {"messages": [response]}
graph_builder = StateGraph(State)
llm = ChatAnthropic(model="claude-3-haiku-20240307")
custom_node = MyCustomNode(llm)
graph_builder.add_node("custom_node", custom_node)
```
…
that encapsulates custom logic and interacts with the LLM.
This provides a more structured and maintainable way to implement complex node behaviors.
...
One useful type is the conditional edge, which allows for decision-making based on a node's output.
To create a conditional edge, you need three components:
1. The upstream node: The node's output decides the next step.
2. A function: This function evaluates the upstream node's output and determines the next node to execute, returning a string that represents the decision.
3. A mapping: This mapping links the possible outcomes of the function to the corresponding nodes to be executed.
Here's an example in pseudocode:
…
### Error handling
...
- Exceptions: Node functions can raise exceptions to signal errors during execution.
You can catch and handle these exceptions to prevent your graph from crashing.
- Retry mechanisms: You can implement retry logic within your nodes to handle transient errors, such as network issues or API timeouts.
- Logging: Use logging to record errors and track the execution of your graph.

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
…
## LangGraph Platform¶
Tools for deploying and connecting to the LangGraph Platform.
- SDK (Python): Python SDK for interacting with instances of the LangGraph Server.
- SDK (JS/TS): JavaScript/TypeScript SDK for interacting with instances of the LangGraph Server.
- RemoteGraph:
`Pregel`abstraction for connecting to LangGraph Server instances.

# Types¶

Classes:



**–**

`RetryPolicy`

Configuration for retrying nodes.



**–**

`CachePolicy`

Configuration for caching nodes.



**–**

`Interrupt`

Information about an interrupt that occurred in a node.



**–**

`PregelTask`

A Pregel task.



**–**

`StateSnapshot`
Snapshot of the state of the graph at the beginning of a step.



**–**

`Send`

A message or packet to send to a specific node in the graph.



**–**

`Command`

One or more commands to update the graph's state and send messages to nodes.

Functions:



**–**

`interrupt`
Interrupt the graph with a resumable exception from within a node.

Attributes:



**–**

`All`

Special value to indicate that graph should interrupt on all nodes.



**–**

`StreamMode`

How the stream method should emit outputs.



**–**

`StreamWriter`

Callable that accepts a single argument and writes it to the output stream.

##

All

`module-attribute`



```

All = Literal['*']

```

Special value to indicate that graph should interrupt on all nodes.

##

StreamMode

`module-attribute`



```

StreamMode = Literal[

"values", "updates", "debug", "messages", "custom"



```

How the stream method should emit outputs.

`"values"`: Emit all values in the state after each step, including interrupts. When used with functional API, values are emitted once at the end of the workflow.
`"updates"`: Emit only the node or task names and updates returned by the nodes or tasks after each step. If multiple updates are made in the same step (e.g. multiple nodes are run) then those updates are emitted separately.

`"custom"`: Emit custom data using from inside nodes or tasks using

`StreamWriter`.

`"messages"`: Emit LLM messages token-by-token together with metadata for any LLM invocations inside nodes or tasks.

`"debug"`: Emit debug events with as much information as possible for each step.

…

###

initial_interval

`class-attribute`

`instance-attribute`



```

initial_interval: float = 0.5

```

Amount of time that must elapse before the first retry occurs. In seconds.

###

backoff_factor

`class-attribute`

`instance-attribute`



```

backoff_factor: float = 2.0

```

Multiplier by which the interval increases after each retry.

…

##

CachePolicy



Bases:

`NamedTuple`

Configuration for caching nodes.

Added in version 0.2.24.

##

Interrupt

`dataclass`



Information about an interrupt that occurred in a node.

Added in version 0.2.24.

Attributes:



**(**

`interrupt_id`

`str`) –

Generate a unique ID for the interrupt based on its namespace.

##

PregelTask



Bases:

`NamedTuple`

A Pregel task.
##

StateSnapshot



Bases:

`NamedTuple`

Snapshot of the state of the graph at the beginning of a step.

Attributes:



**(**

`values`

`Union[dict[str, Any], Any]`) –

Current values of channels.



**(**

`next`

`tuple[str, ...]`) –

The name of the node to execute in each task for this step.
**(**

`config`

`RunnableConfig`) –

Config used to fetch this snapshot.



**(**

`metadata`

`Optional[CheckpointMetadata]`) –

Metadata associated with this snapshot.



**(**

`created_at`

`Optional[str]`) –

Timestamp of snapshot creation.



**(**

`parent_config`

`Optional[RunnableConfig]`) –

…

###

next

`instance-attribute`



```

next: tuple[str, ...]

```

The name of the node to execute in each task for this step.

###

config

`instance-attribute`



```

config: RunnableConfig

```

Config used to fetch this snapshot.

###

metadata

`instance-attribute`



```

metadata: Optional[CheckpointMetadata]

```

Metadata associated with this snapshot.

…

##

Send



A message or packet to send to a specific node in the graph.

The

`Send` class is used within a

`StateGraph`'s conditional edges to

dynamically invoke a node with a custom state at the next step.

Importantly, the sent state can differ from the core graph's state, allowing for flexible and dynamic workflow management.
One such example is a "map-reduce" workflow where your graph invokes the same node multiple times in parallel with different states, before aggregating the results back into the main graph's state.

Attributes:



**(**

`node`

`str`) –

The name of the target node to send the message to.



**(**
`arg`

`Any`) –

The state or message to send to the target node.

Examples:
```
>>> from typing import Annotated

>>> import operator

>>> class OverallState(TypedDict):

... subjects: list[str]

... jokes: Annotated[list[str], operator.add]

...

>>> from langgraph.types import Send

>>> from langgraph.graph import END, START

>>> def continue_to_jokes(state: OverallState):
... return [Send("generate_joke", {"subject": s}) for s in state['subjects']]

...

>>> from langgraph.graph import StateGraph

>>> builder = StateGraph(OverallState)

>>> builder.add_node("generate_joke", lambda state: {"jokes": [f"Joke about {state['subject']}"]})
>>> builder.add_conditional_edges(START, continue_to_jokes)

>>> builder.add_edge("generate_joke", END)

>>> graph = builder.compile()

>>>

>>> # Invoking with two subjects results in a generated joke for each

>>> graph.invoke({"subjects": ["cats", "dogs"]})

{'subjects': ['cats', 'dogs'], 'jokes': ['Joke about cats', 'Joke about dogs']}

```
Methods:



**–**

`__init__`

Initialize a new instance of the Send class.
##

Command

`dataclass`



Bases:

`Generic[N]`,

`ToolOutputMixin`

One or more commands to update the graph's state and send messages to nodes.

Added in version 0.2.24.

Parameters:



**(**

`graph`

`Optional[str]`, default:

`None`) –
graph to send the command to. Supported values are:

- None: the current graph (default)

- Command.PARENT: closest parent graph



**(**

`update`

`Optional[Any]`, default:

`None`) –

update to apply to the graph's state.



**(**

`resume`

`Optional[Union[dict[str, Any], Any]]`, default:

…

`()`) –

can be one of the following:

- name of the node to navigate to next (any node that belongs to the specified

`graph`)

- sequence of node names to navigate to next

`Send`object (to execute a node with the input provided)

- sequence of

`Send`objects

- name of the node to navigate to next (any node that belongs to the specified

##

interrupt



```

interrupt(value: Any) -> Any

```

Interrupt the graph with a resumable exception from within a node.

The

`interrupt` function enables human-in-the-loop workflows by pausing graph

execution and surfacing a value to the client. This value can communicate context

or request input required to resume execution.
In a given node, the first invocation of this function raises a

`GraphInterrupt`

exception, halting execution. The provided

`value` is included with the exception

and sent to the client executing the graph.

A client resuming the graph must use the

`Command`

primitive to specify a value for the interrupt and continue execution.
The graph resumes from the start of the node,

**re-executing** all logic.

If a node contains multiple

`interrupt` calls, LangGraph matches resume values

to interrupts based on their order in the node. This list of resume values

is scoped to the specific task executing the node and is not shared across tasks.

To use an

`interrupt`, you must enable a checkpointer, as the feature relies

on persisting the graph state.

## Example
```
import uuid

from typing import Optional

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver

from langgraph.constants import START

from langgraph.graph import StateGraph

from langgraph.types import interrupt

class State(TypedDict):

"""The graph state."""

foo: str

human_value: Optional[str]
"""Human value will be updated using an interrupt."""

def node(state: State):

answer = interrupt(

# This value will be sent to the client

# as part of the interrupt information.

"what is your age?"



print(f"> Received an input from the interrupt: {answer}")

return {"human_value": answer}

…

```

{'__interrupt__': (Interrupt(value='what is your age?', resumable=True, ns=['node:62e598fa-8653-9d6d-2046-a70203020e37'], when='during'),)}

```

```

command = Command(resume="some input from a human!!!")

for chunk in graph.stream(Command(resume="some input from a human!!!"), config):

print(chunk)

```
```

Received an input from the interrupt: some input from a human!!!

{'node': {'human_value': 'some input from a human!!!'}}

```

Parameters:



**(**

`value`

`Any`) –

The value to surface to the client when the graph is interrupted.

Returns:



**(**

`Any`
`Any`) –

On subsequent invocations within the same node (same task to be precise), returns the value provided during the first invocation

Raises:



`GraphInterrupt`–

On the first invocation within the node, halts execution and surfaces the provided value to the client.

# LangGraph

## Tutorials

[Learn the basics](https://langchain-ai.github.io/langgraph/tutorials/introduction/): LLM should read this page when needing to build a LangGraph chatbot or when learning about chat agents with memory, human-in-the-loop functionality, and state management. This page provides a comprehensive LangGraph quickstart tutorial covering building a support chatbot with web search capability, conversation memory, human review routing, custom state management, and time travel functionality to explore alternative conversation paths.

…

[Workflows and Agents](https://langchain-ai.github.io/langgraph/tutorials/workflows/): LLM should read this page when implementing agent systems, designing workflow architectures, or troubleshooting LLM orchestration strategies. The page covers patterns for LLM system design, comparing workflows (predefined paths) vs agents (dynamic control), with implementations of prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer, and agent patterns using both graph and functional APIs in LangGraph.

## Concepts 

[Concepts](https://langchain-ai.github.io/langgraph/concepts/): LLM should read this page when needing to understand LangGraph's key concepts or when planning to deploy LangGraph applications. Comprehensive guide covering LangGraph fundamentals (graph primitives, agents, multi-agent systems, breakpoints, persistence), features (time travel, memory, streaming), and LangGraph Platform deployment options (self-hosted, cloud, enterprise).
[Agent architectures](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/): LLM should read this page when designing agent architectures, implementing control flows for LLM applications, or customizing agent behavior patterns. This page covers different LLM agent architectures including routers, tool calling agents (ReAct), structured outputs, memory systems, planning capabilities, and advanced customization options like human-in-the-loop, parallelization, subgraphs, and reflection mechanisms.
[Application Structure](https://langchain-ai.github.io/langgraph/concepts/application_structure/): LLM should read this page when needing to understand LangGraph application structure, preparing to deploy a LangGraph application, or troubleshooting configuration issues. This page details the structure of LangGraph applications, including required components (graphs, langgraph.json config file, dependency files, optional .env), file organization patterns for Python/JavaScript projects, configuration file format with all supported fields, and how to specify dependencies, graphs, and environment variables.
[Assistants](https://langchain-ai.github.io/langgraph/concepts/assistants/): LLM should read this page when looking for information about LangGraph assistants, understanding assistant configuration in LangGraph Platform, or learning about versioning agent configurations. This page explains LangGraph assistants, which allow developers to modify agent configurations (prompts, models, etc.) without changing graph logic, supports versioning for tracking changes, and is available only in LangGraph Platform (not open source).

…

[Functional API](https://langchain-ai.github.io/langgraph/concepts/functional_api/): LLM should read this page when implementing workflows with persistent state, adding human-in-the-loop features, or converting existing code to use LangGraph. The page documents LangGraph's Functional API, which allows adding persistence, memory, and human-in-the-loop capabilities with minimal code changes using @entrypoint and @task decorators, handling serialization requirements, state management, and common patterns for parallel execution and error handling.
[Why LangGraph?](https://langchain-ai.github.io/langgraph/concepts/high_level/): LLM should read this page when understanding LangGraph's core capabilities, exploring LLM application infrastructure, or evaluating agent/workflow persistence options. LangGraph provides infrastructure for LLM applications with three key benefits: persistence for memory and human-in-the-loop capabilities, streaming of workflow events and LLM outputs, and tools for debugging and deployment via LangGraph Platform.
[Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/): LLM should read this page when implementing human-in-the-loop workflows in LangGraph, designing approval systems with LLMs, or creating interactive multi-turn conversation agents. This page explains human-in-the-loop patterns in LangGraph using the interrupt function, showing how to pause graph execution for human review/input and resume with Command. Includes design patterns for approval workflows, state editing, tool call reviews, and multi-turn conversations, with code examples and warnings about execution flow and common pitfalls.

…

[LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/): LLM should read this page when seeking information about LangGraph Platform's components or evaluating production deployment options for agentic applications. The page details the LangGraph Platform, a commercial solution for deploying agentic applications, including its components (Server, Studio, CLI, SDK, Remote Graph) and key benefits like streaming support, background runs, long run handling, burstiness management, and human-in-the-loop capabilities.
[LangGraph Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/): LLM should read this page when developing applications with LangGraph Server, deploying agent-based applications, or integrating persistent state management in agent workflows. LangGraph Server provides an API for creating and managing agent applications with key features like streaming endpoints, background runs, task queues, persistence, webhooks, cron jobs, and monitoring capabilities through a structured system of assistants, threads, runs, and stores.

…

[LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/): LLM should read this page when needing to understand LangGraph terminology, implementing agent workflows as graphs, or developing modular multi-step AI systems. The page covers core LangGraph concepts including StateGraph, nodes, edges, state management, messaging, persistence, configuration, human-in-the-loop features, subgraphs, and visualization capabilities.

…

[LangGraph's Runtime (Pregel)](https://langchain-ai.github.io/langgraph/concepts/pregel/): LLM should read this page when learning about LangGraph's runtime, implementing applications with Pregel directly, or understanding how LangGraph executes graph applications. Explains LangGraph's Pregel runtime which manages graph application execution through a three-phase process (Plan, Execution, Update), describes different channel types (LastValue, Topic, Context, BinaryOperatorAggregate), provides direct implementation examples, and contrasts the StateGraph API with the Functional API.

…

## How Tos

[How-to Guides](https://langchain-ai.github.io/langgraph/how-tos/): LLM should read this page when looking for specific implementation techniques in LangGraph or when trying to deploy LangGraph applications to production environments. This page contains an extensive collection of how-to guides for LangGraph, covering graph fundamentals, persistence, memory management, human-in-the-loop features, tool calling, multi-agent systems, streaming, and deployment options through LangGraph Platform.

…

[How to run a graph asynchronously](https://langchain-ai.github.io/langgraph/how-tos/async/): LLM should read this page when needing to implement asynchronous graph execution in LangGraph or when optimizing IO-bound LLM applications. This page explains how to convert synchronous graphs to asynchronous in LangGraph, including updating node definitions with async/await, using StateGraph with TypedDict, implementing conditional edges, and streaming results.

…

[How to define input/output schema for your graph](https://langchain-ai.github.io/langgraph/how-tos/input_output_schema/): LLM should read this page when needing to define separate input/output schemas for LangGraph, implementing schema-based data filtering, or understanding schema definitions in StateGraph. This page explains how to define distinct input and output schemas for a StateGraph, showing how input schema validates the provided data structure while output schema filters internal data to return only relevant information, with code examples demonstrating implementation.

…

[How to create and control loops](https://langchain-ai.github.io/langgraph/how-tos/recursion-limit/): LLM should read this page when building loops in computational graphs, needing to implement termination conditions, or handling recursion limits in LangGraph. The page explains how to create graphs with loops using conditional edges for termination, set recursion limits, handle GraphRecursionError, and implement complex loops with branches.

…

[How to create a sequence of steps](https://langchain-ai.github.io/langgraph/how-tos/sequence/): LLM should read this page when implementing sequential workflows in LangGraph, creating multi-step processes in applications, or learning about state management in graph-based systems. This page explains how to create sequences in LangGraph, covering methods for building sequential graphs using .add_node/.add_edge or the shorthand .add_sequence, defining state with TypedDict, creating nodes as functions that update state, and compiling/invoking graphs with examples.

…

[How to use subgraphs](https://langchain-ai.github.io/langgraph/how-tos/subgraph/): LLM should read this page when building complex systems with subgraphs, implementing multi-agent systems, or needing to share state between parent graphs and subgraphs. The page explains two methods for using subgraphs: adding compiled subgraphs when schemas share keys, and invoking subgraphs via node functions when schemas differ, with code examples for both approaches.

…

[How to transform inputs and outputs of a subgraph](https://langchain-ai.github.io/langgraph/how-tos/subgraph-transform-state/): LLM should read this page when needing to work with nested subgraphs, transforming state between parent and child graphs, or integrating independent state components in LangGraph. This page demonstrates how to transform inputs and outputs between parent graphs and subgraphs with different state structures, showing implementation of three nested graphs (parent, child, grandchild) with separate state dictionaries and transformation functions.

…

[How to visualize your graph](https://langchain-ai.github.io/langgraph/how-tos/visualization): LLM should read this page when needing to visualize LangGraph graphs, looking for graph visualization methods, or working with graph visualization in Python. Comprehensive guide for visualizing graphs in LangGraph with multiple methods: Mermaid syntax, Mermaid.ink API for PNG rendering, Pyppeteer-based visualization, and Graphviz, with customization options for colors, styles, and layout.