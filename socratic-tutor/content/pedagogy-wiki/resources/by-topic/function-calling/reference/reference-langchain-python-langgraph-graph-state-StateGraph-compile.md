# Source: https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile
# Title: compile | langgraph - LangChain Reference Docs
# Fetched via: search
# Date: 2026-04-10

# StateGraph
...
📖 [View in docs](https://reference.langchain.com/python/langgraph/graph/state/StateGraph)
A graph whose nodes communicate by reading and writing to a shared state.
The signature of each node is `State -> Partial<State>`.
Each state key can optionally be annotated with a reducer function that
will be used to aggregate the values of that key received from multiple nodes.
The signature of a reducer function is `(Value, Value) -> Value`.
!!! warning
`StateGraph` is a builder class and cannot be used directly for execution.
You must first call `.compile()` to create an executable graph that supports
methods like `invoke()`, `stream()`, `astream()`, and `ainvoke()`.
See the
`CompiledStateGraph` documentation for more details.
## Signature
```python
StateGraph(
self,
state_schema: type[StateT],
context_schema: type[ContextT] | None = None,
...
input_schema: type[InputT] | None = None,
output_schema: type[OutputT] | None = None,
**kwargs: Unpack[DeprecatedKwargs] = {},
...
Please use `context_schema` instead to specify the schema for run-scoped context.
**Example:**
```python
from langchain_core.runnables import RunnableConfig
from typing_extensions import Annotated, TypedDict
...
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
## Parameters
| Name | Type | Required | Description |
...
| `state_schema` | `type[StateT]` | Yes | The schema class that defines the state.
|
| `context_schema` | `type[ContextT] \| None` | No | The schema class that defines the runtime context.
Use this to expose immutable context data to your nodes, like `user_id`, `db_conn`, etc.
(default: `None`) |
| `input_schema` | `type[InputT] \| None` | No | The schema class that defines the input to the graph.
(default: `None`) |
| `output_schema` | `type[OutputT] \| None` | No | The schema class that defines the output from the graph.
...
- `managed`
- `schemas`
- `waiting_edges`
- `compiled`
- `state_schema`
- `context_schema`
- `input_schema`
- `output_schema`
## Methods
- [`add_node()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_node)
- [`add_edge()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_edge)
- [`add_conditional_edges()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_conditional_edges)
- [`add_sequence()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_sequence)
- [`set_entry_point()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/set_entry_point)
- [`set_conditional_entry_point()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/set_conditional_entry_point)
- [`set_finish_point()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/set_finish_point)
- [`validate()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/validate)
- [`compile()`](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

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
The signature of a reducer function is

`(Value, Value) -> Value`.

Warning

`StateGraph` is a builder class and cannot be used directly for execution.

You must first call

`.compile()` to create an executable graph that supports

methods like

`invoke()`,

`stream()`,

`astream()`, and
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

## Example

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

###

add_sequence



```

add_sequence(

nodes: Sequence[

StateNode[NodeInputT, ContextT] | tuple[str, StateNode[NodeInputT, ContextT]]

],

) -> Self

```

Add a sequence of nodes that will be executed in the provided order.
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

|`debug`|A flag indicating whether to enable debug mode.|
|`name`|The name to use for the compiled graph.|
|RETURNS|DESCRIPTION|
|--|--|
|`CompiledStateGraph`|The compiled|

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

###

stream

```

stream(

input: InputT | Command | None,

config: RunnableConfig | None = None,

*,

context: ContextT | None = None,

stream_mode: StreamMode | Sequence[StreamMode] | None = None,

print_mode: StreamMode | Sequence[StreamMode] = (),

output_keys: str | Sequence[str] | None = None,

…

Stream graph steps for a single input.

|PARAMETER|DESCRIPTION|
|--|--|
|`input`|The input to the graph.|
|`config`|The configuration to use for the run.|
|`context`|The static context to use for the run. Added in version 0.6.0|
|`stream_mode`|The mode to stream output, defaults to Options are: You can pass a list as the See LangGraph streaming guide for more details.|

…

|`durability`|The durability mode for the graph execution, defaults to Options are:|
|`subgraphs`|Whether to stream events from inside subgraphs, defaults to If See LangGraph streaming guide for more details.|
|YIELDS|DESCRIPTION|
|--|--|
|`dict[str, Any] | Any`|The output of each step in the graph. The output shape depends on the|

…

Asynchronously stream graph steps for a single input.

|PARAMETER|DESCRIPTION|
|--|--|
|`input`|The input to the graph.|
|`config`|The configuration to use for the run.|
|`context`|The static context to use for the run. Added in version 0.6.0|
|`stream_mode`|The mode to stream output, defaults to Options are: You can pass a list as the See LangGraph streaming guide for more details.|

…

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

…

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

…

###

get_state



```

get_state(config: RunnableConfig, *, subgraphs: bool = False) -> StateSnapshot

```

Get the current state of the graph.

###

aget_state

`async`



```

aget_state(config: RunnableConfig, *, subgraphs: bool = False) -> StateSnapshot

```

Get the current state of the graph.

###

get_state_history



```

get_state_history(

config: RunnableConfig,

*,

filter: dict[str, Any] | None = None,

before: RunnableConfig | None = None,

limit: int | None = None,

) -> Iterator[StateSnapshot]

```

Get the history of the state of the graph.

###

aget_state_history

`async`



```

aget_state_history(

config: RunnableConfig,

*,

filter: dict[str, Any] | None = None,

before: RunnableConfig | None = None,

limit: int | None = None,

) -> AsyncIterator[StateSnapshot]

```

Asynchronously get the history of the state of the graph.

###

update_state



```

update_state(

config: RunnableConfig,

values: dict[str, Any] | Any | None,

as_node: str | None = None,

task_id: str | None = None,

) -> RunnableConfig

```

Update the state of the graph with the given values, as if they came from

node

`as_node`. If

`as_node` is not provided, it will be set to the last node

that updated the state, if not ambiguous.

###

aupdate_state

`async`



```

aupdate_state(

config: RunnableConfig,

values: dict[str, Any] | Any,

as_node: str | None = None,

task_id: str | None = None,

) -> RunnableConfig

```

Asynchronously update the state of the graph with the given values, as if they came from

node

`as_node`. If

`as_node` is not provided, it will be set to the last node

that updated the state, if not ambiguous.

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

## Use in a StateGraph

```

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph

class State(TypedDict):

messages: Annotated[list, add_messages]

builder = StateGraph(State)

builder.add_node("chatbot", lambda state: {"messages": [("assistant", "Hello")]})

builder.set_entry_point("chatbot")

builder.set_finish_point("chatbot")

graph = builder.compile()

graph.invoke({})

# {'messages': [AIMessage(content='Hello', id=...)]}

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

# Class StateGraph<SD, S, U, N, I, O, C, NodeReturnType, InterruptType, WriterType>

A graph whose nodes communicate by reading and writing to a shared state.
Each node takes a defined `State` as input and returns a `Partial<State>`.

Each state key can optionally be annotated with a reducer function that
will be used to aggregate the values of that key received from multiple nodes.
The signature of a reducer function is (left: Value, right: UpdateValue) => Value.
See Annotation for more on defining state.

After adding nodes and edges to your graph, you must call `.compile()` on it before
you can use it.

#### Example

```
import {
 type BaseMessage,
 AIMessage,
 HumanMessage,
} from "@langchain/core/messages";
import { StateGraph, Annotation } from "@langchain/langgraph";

// Define a state with a single key named "messages" that will
// combine a returned BaseMessage or arrays of BaseMessages
const StateAnnotation = Annotation.Root({
 sentiment: Annotation<string>,
 messages: Annotation<BaseMessage[]>({
 reducer: (left: BaseMessage[], right: BaseMessage | BaseMessage[]) => {
 if (Array.isArray(right)) {
 return left.concat(right);
 }
 return left.concat([right]);
 },
 default: () => [],
 }),
});

const graphBuilder = new StateGraph(StateAnnotation);

// A node in the graph that returns an object with a "messages" key
// will update the state by combining the existing value with the returned one.
const myNode = (state: typeof StateAnnotation.State) => {
 return {
 messages: [new AIMessage("Some new response")],
 sentiment: "positive",
 };
};

const graph = graphBuilder
 .addNode("myNode", myNode)
 .addEdge("__start__", "myNode")
 .addEdge("myNode", "__end__")
 .compile();

await graph.invoke({ messages: [new HumanMessage("how are you?")] });

// {
// messages: [HumanMessage("how are you?"), AIMessage("Some new response")],
// sentiment: "positive",
// }

```

#### Type Parameters
- SD extends SDZod | unknown
- S = SD extends SDZod ? StateType<ToStateDefinition<SD>> : SD
- U = SD extends SDZod ? UpdateType<ToStateDefinition<SD>> : Partial<S>
- N extends string = typeof START
- I extends SDZod = SD extends SDZod ? ToStateDefinition<SD> : StateDefinition
- O extends SDZod = SD extends SDZod ? ToStateDefinition<SD> : StateDefinition
- C extends SDZod = StateDefinition
- NodeReturnType = unknown
- InterruptType = unknown
- WriterType = unknown

…

### Methods

_addSchema addConditionalEdges addEdge addNode addSequence compile validate warnIfCompiled

…

new StateGraph<
  SD extends unknown,
  S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD,
  U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>,
  N extends string = "__start__",

…

>(
  state: SD extends StateDefinition ? AnnotationRoot<SD<SD>> : never,
  options?: {
  context?: C | AnnotationRoot<ToStateDefinition<C>>;
  input?: I | AnnotationRoot<ToStateDefinition<I>>;
  interrupt?: InterruptType;
  nodes?: N[];
  output?: O | AnnotationRoot<ToStateDefinition<O>>;
  writer?: WriterType;
  },
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

- S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD
  - U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>
  - N extends string = "__start__"
  - I extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition
- O extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition
  - C extends SDZod = StateDefinition
  - NodeReturnType = unknown
  - InterruptType = unknown
  - WriterType = unknown
  #### Parameters
  - state: SD extends StateDefinition ? AnnotationRoot<SD<SD>> : never
  - `Optional`options: {
  context?: C | AnnotationRoot<ToStateDefinition<C>>;
  input?: I | AnnotationRoot<ToStateDefinition<I>>;
  interrupt?: InterruptType;
  nodes?: N[];
  output?: O | AnnotationRoot<ToStateDefinition<O>>;
  writer?: WriterType;
  }

…

new StateGraph<
  SD extends unknown,
  S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD,
  U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>,
  N extends string = "__start__",
I extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  O extends
  SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition,
  C extends SDZod = StateDefinition,
  NodeReturnType = unknown,
  InterruptType = unknown,
  WriterType = unknown,
>(
  state: SD extends InteropZodObject ? SD<SD> : never,
  options?: {
  context?: C | AnnotationRoot<ToStateDefinition<C>>;
  input?: I | AnnotationRoot<ToStateDefinition<I>>;
  interrupt?: InterruptType;
  nodes?: N[];
  output?: O | AnnotationRoot<ToStateDefinition<O>>;
  writer?: WriterType;
  },
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

- S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD
  - U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>
  - N extends string = "__start__"
  - I extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition

…

new StateGraph<
  SD extends unknown,
  S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD,
  U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>,
  N extends string = "__start__",

…

>(
  fields: SD extends StateDefinition
  ? StateGraphArgsWithInputOutputSchemas<SD<SD>, ToStateDefinition<O>>
  : never,
  contextSchema?: C | AnnotationRoot<ToStateDefinition<C>>,
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

- S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD
  - U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>
  - N extends string = "__start__"
  - I extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition

…

>(
  fields: SD extends StateDefinition
  ? | AnnotationRoot<SD<SD>>
  | StateGraphArgsWithStateSchema<
  SD<SD>,
  ToStateDefinition<I>,
  ToStateDefinition<O>,
  >
  : never,
  contextSchema?: C | AnnotationRoot<ToStateDefinition<C>>,
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,

…

- S = SD extends SDZod ? StateType<ToStateDefinition<SD<SD>>> : SD
  - U = SD extends SDZod ? UpdateType<ToStateDefinition<SD<SD>>> : Partial<S>
  - N extends string = "__start__"
  - I extends SDZod = SD extends SDZod ? ToStateDefinition<SD<SD>> : StateDefinition

…

  #### Parameters
  - fields: SD extends StateDefinition
  ? | AnnotationRoot<SD<SD>>
  | StateGraphArgsWithStateSchema<
  SD<SD>,
  ToStateDefinition<I>,
  ToStateDefinition<O>,
  >
  : never
  - `Optional`contextSchema: C | AnnotationRoot<ToStateDefinition<C>>

…

>(
  fields: SD extends StateDefinition
  ? SD<SD>
  | StateGraphArgs<S>
  : StateGraphArgs<S>,
  contextSchema?: C | AnnotationRoot<ToStateDefinition<C>>,
  ): StateGraph<
  SD,
  S,
  U,
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,
  >

…

  #### Returns void

### add Conditional Edges
- addConditionalEdges(
  source: BranchOptions<
  S,
  N,
  LangGraphRunnableConfig<StateType<ToStateDefinition<C>>>,
  >,
  ): this

…

  #### Parameters
  - source: N
  - path: RunnableLike$1<
  S,
  BranchPathReturnValue,
  LangGraphRunnableConfig<StateType<ToStateDefinition<C>>>,
  >
  - `Optional`pathMap: Record<string, "__end__" | N> | ("__end__" | N)[]

…

  #### Returns this

### add Node
- addNode<
  K extends string,
  NodeMap extends Record<K, NodeAction<S, U, C, InterruptType, WriterType>>,
  >(
  nodes: NodeMap,
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<
  NodeReturnType,
  {
  [key in string
  | number
  | symbol]: NodeMap[key] extends NodeAction<
  S,
  U,
  C,
  InterruptType,
  WriterType,
  >

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string | number | symbol ] : NodeMap [ key ] extends NodeAction < S , U , C , InterruptType , WriterType , > ? U : never } , > , >
- addNode<K extends string, NodeInput = S, NodeOutput = U>(
  nodes: [
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ][],
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<NodeReturnType, { [key in string]: NodeOutput }>,
  >

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string ] : NodeOutput } > , >
- addNode<K extends string, NodeInput = S, NodeOutput = U>(
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<NodeReturnType, { [key in string]: NodeOutput }>,
  >

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string ] : NodeOutput } > , >
- addNode<K extends string, NodeInput = S>(
  key: K,
  action: NodeAction<NodeInput, U, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ): StateGraph<SD, S, U, N | K, I, O, C, NodeReturnType>

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , NodeReturnType >

### add Sequence
- addSequence<K extends string, NodeInput = S, NodeOutput = U>(
  nodes: [
  key: K,
  action: NodeAction<NodeInput, NodeOutput, C, InterruptType, WriterType>,
  options?: StateGraphAddNodeOptions<string>,
  ][],
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<NodeReturnType, { [key in string]: NodeOutput }>,
  >

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string ] : NodeOutput } > , >
- addSequence<
  K extends string,
  NodeMap extends Record<K, NodeAction<S, U, C, InterruptType, WriterType>>,
  >(
  nodes: NodeMap,
  ): StateGraph<
  SD,
  S,
  U,
  N
  | K,
  I,
  O,
  C,
  MergeReturnType<
  NodeReturnType,
  {
  [key in string
  | number
  | symbol]: NodeMap[key] extends NodeAction<
  S,
  U,
  C,
  InterruptType,
  WriterType,
  >

…

  #### Returns StateGraph < SD , S , U , N | K , I , O , C , MergeReturnType < NodeReturnType , { [ key in string | number | symbol ] : NodeMap [ key ] extends NodeAction < S , U , C , InterruptType , WriterType , > ? U : never } , > , >

### compile
- compile(
  __namedParameters?: {
  cache?: BaseCache<unknown>;
  checkpointer?: boolean | BaseCheckpointSaver<number>;
  description?: string;
  interruptAfter?: "*" | N[];
  interruptBefore?: "*" | N[];
  name?: string;
  store?: BaseStore;
  },
  ): CompiledStateGraph<
  { [K in string
  | number
  | symbol]: S[K] },
  { [K in string | number | symbol]: U[K] },
  N,
  I,
  O,
  C,
  NodeReturnType,
  InterruptType,
  WriterType,

…

  #### Parameters
  - `Optional`__namedParameters: {
  cache?: BaseCache<unknown>;
  checkpointer?: boolean | BaseCheckpointSaver<number>;
  description?: string;
  interruptAfter?: "*" | N[];
  interruptBefore?: "*" | N[];
  name?: string;
  store?: BaseStore;
  }
  #### Returns CompiledStateGraph < { [ K in string | number | symbol ] : S [ K ] } , { [ K in string | number | symbol ] : U [ K ] } , N , I , O , C , NodeReturnType , InterruptType , WriterType , >

### validate
- validate(interrupt?: string[]): void

# ​ Quickstart
This guide will get you up and running with LangGraph in under 5 minutes.
You’ll create a simple stateful workflow that demonstrates the core concepts of graphs, nodes, edges, and state.
…
## ​ Your First LangGraph Application
Let’s build a simple workflow that processes text through multiple nodes.
1
Define Your State
2
First, define the state schema using a TypedDict.
The state represents the data that flows through your graph:
3
…
4
Create Node Functions
5
Nodes are the building blocks of your graph.
Each node is a function that receives the current state and returns an update:
6
```
def node_a(state: State) -> dict:
return {"text": state["text"] + "a"}
def node_b(state: State) -> dict:
return {"text": state["text"] + "b"}
```
7
Node functions can return a partial state update.
LangGraph automatically merges the update with the existing state.
8
Build the Graph
9
Now create a StateGraph and add your nodes and edges:
10
```
from langgraph.graph import START, StateGraph
graph = StateGraph(State)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
```
11
Here’s what’s happening:
12
`StateGraph(State)` creates a graph with your state schema`add_node()` registers functions as nodes in the graph`add_edge()` defines the execution flow between nodes`START` is a special constant representing the entry point
13
Compile and Run
14
Compile the graph and execute it with initial state:
…
```
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict
class State(TypedDict):
text: str
def node_a(state: State) -> dict:
return {"text": state["text"] + "a"}
def node_b(state: State) -> dict:
return {"text": state["text"] + "b"}
graph = StateGraph(State)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
app = graph.compile()
print(app.invoke({"text": ""}))
# Output: {'text': 'ab'}
```
…
## ​ Understanding the Flow
1
State Initialization
2
The graph begins with the initial state you provide: `{"text": ""}`
3
Node Execution
4
Each node receives the current state and returns updates.
LangGraph automatically merges these updates.
5
Sequential Processing
6
Edges determine execution order.
In this example, `node_a` always runs before `node_b`.
…
```
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
class State(TypedDict):
text: str
count: int
def increment(state: State) -> dict:
return {"count": state["count"] + 1}
def should_continue(state: State) -> str:
if state["count"] < 3:
return "increment"
return END
graph = StateGraph(State)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_conditional_edges("increment", should_continue)
app = graph.compile()
result = app.invoke({"text": "hello", "count": 0})
print(result)
# Output: {'text': 'hello', 'count': 3}
```

# ​ Quickstart
This guide will get you up and running with LangGraph in under 5 minutes.
You’ll create a simple stateful workflow that demonstrates the core concepts of graphs, nodes, edges, and state.
…
## ​ Your First LangGraph Application
Let’s build a simple workflow that processes text through multiple nodes.
1
Define Your State
2
First, define the state schema using a TypedDict.
The state represents the data that flows through your graph:
3
…
4
Create Node Functions
5
Nodes are the building blocks of your graph.
Each node is a function that receives the current state and returns an update:
6
```
def node_a(state: State) -> dict:
return {"text": state["text"] + "a"}
def node_b(state: State) -> dict:
return {"text": state["text"] + "b"}
```
7
Node functions can return a partial state update.
LangGraph automatically merges the update with the existing state.
8
Build the Graph
9
Now create a StateGraph and add your nodes and edges:
10
```
from langgraph.graph import START, StateGraph
graph = StateGraph(State)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
```
11
Here’s what’s happening:
12
`StateGraph(State)` creates a graph with your state schema`add_node()` registers functions as nodes in the graph`add_edge()` defines the execution flow between nodes`START` is a special constant representing the entry point
13
Compile and Run
14
Compile the graph and execute it with initial state:
…
```
from langgraph.graph import START, StateGraph
from typing_extensions import TypedDict
class State(TypedDict):
text: str
def node_a(state: State) -> dict:
return {"text": state["text"] + "a"}
def node_b(state: State) -> dict:
return {"text": state["text"] + "b"}
graph = StateGraph(State)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_edge(START, "node_a")
graph.add_edge("node_a", "node_b")
app = graph.compile()
print(app.invoke({"text": ""}))
# Output: {'text': 'ab'}
```
…
## ​ Understanding the Flow
1
State Initialization
2
The graph begins with the initial state you provide: `{"text": ""}`
3
Node Execution
4
Each node receives the current state and returns updates.
LangGraph automatically merges these updates.
5
Sequential Processing
6
Edges determine execution order.
In this example, `node_a` always runs before `node_b`.
…
```
from langgraph.graph import START, END, StateGraph
from typing_extensions import TypedDict
class State(TypedDict):
text: str
count: int
def increment(state: State) -> dict:
return {"count": state["count"] + 1}
def should_continue(state: State) -> str:
if state["count"] < 3:
return "increment"
return END
graph = StateGraph(State)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_conditional_edges("increment", should_continue)
app = graph.compile()
result = app.invoke({"text": "hello", "count": 0})
print(result)
# Output: {'text': 'hello', 'count': 3}
```