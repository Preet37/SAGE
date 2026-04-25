# Source: https://reference.langchain.com/python/langgraph/graph/state/StateGraph
# Title: StateGraph | langgraph - LangChain Reference Docs
# Fetched via: browser
# Date: 2026-04-10

Class
v1.1.6 (latest)
●
Since v0.1
StateGraph

A graph whose nodes communicate by reading and writing to a shared state.

The signature of each node is State -> Partial<State>.

Each state key can optionally be annotated with a reducer function that will be used to aggregate the values of that key received from multiple nodes. The signature of a reducer function is (Value, Value) -> Value.

Warning

StateGraph is a builder class and cannot be used directly for execution. You must first call .compile() to create an executable graph that supports methods like invoke(), stream(), astream(), and ainvoke(). See the CompiledStateGraph documentation for more details.

Copy
StateGraph(
  self,
  context_schema: type[ContextT] | None = None,
  *,
  input_schema: type[InputT] | None = None,
  output_schema: type[OutputT] | None = None,
  **kwargs: Unpack[DeprecatedKwargs] = {}
)
BASES
Generic[StateT, ContextT, InputT, OutputT]

The config_schema parameter is deprecated in v0.6.0 and support will be removed in v2.0.0. Please use context_schema instead to specify the schema for run-scoped context.

Example:

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
Copy
USED IN DOCS
A2A endpoint in Agent Server
Build a custom RAG agent with LangGraph
Build a custom SQL agent
Build a multi-source knowledge base with routing
Choosing between Graph and Functional APIs
+15 more
(18 more not shown)
Parameters
Name	Type	Description

The schema class that defines the state.


context_schema	type[ContextT] | None	
Default:
None

The schema class that defines the runtime context.

Use this to expose immutable context data to your nodes, like user_id, db_conn, etc.


input_schema	type[InputT] | None	
Default:
None

The schema class that defines the input to the graph.


output_schema	type[OutputT] | None	
Default:
None

The schema class that defines the output from the graph.

Constructors
constructor
__init__
Name	Type
context_schema	type[ContextT] | None
input_schema	type[InputT] | None
output_schema	type[OutputT] | None
Attributes
attribute
edges
: set[tuple[str, str]]
attribute
nodes
: dict[str, StateNodeSpec[Any, ContextT]]
attribute
branches
: defaultdict[str, dict[str, BranchSpec]]
attribute
channels
: dict[str, BaseChannel]
attribute
managed
: dict[str, ManagedValueSpec]
attribute
schemas
: dict[type[Any], dict[str, BaseChannel | ManagedValueSpec]]
attribute
waiting_edges
: set[tuple[tuple[str, ...], str]]
attribute
compiled
: bool
attribute
: type[StateT]
attribute
context_schema
: type[ContextT] | None
attribute
input_schema
: type[InputT]
attribute
output_schema
: type[OutputT]
Methods
method
add_node

Add a new node to the StateGraph.

method
add_edge

Add a directed edge from the start node (or list of start nodes) to the end node.

When a single start node is provided, the graph will wait for that node to complete before executing the end node. When multiple start nodes are provided, the graph will wait for ALL of the start nodes to complete before executing the end node.

method
add_conditional_edges

Add a conditional edge from the starting node to any number of destination nodes.

method
add_sequence

Add a sequence of nodes that will be executed in the provided order.

method
set_entry_point

Specifies the first node to be called in the graph.

Equivalent to calling add_edge(START, key).

method
set_conditional_entry_point

Sets a conditional entry point in the graph.

method
set_finish_point

Marks a node as a finish point of the graph.

If the graph reaches this node, it will cease execution.

method
validate
method
compile

Compiles the StateGraph into a CompiledStateGraph object.

The compiled graph implements the Runnable interface and can be invoked, streamed, batched, and run asynchronously.

View source on GitHub
Version History