# Source: https://github.com/langchain-ai/langgraph/discussions/938
# Author: LangChain
# Author Slug: langchain
# Title: langgraph/how-tos/human_in_the_loop/edit-graph-state (discussion #938)
# Fetched via: search
# Date: 2026-04-10

Trusted by companies shaping the future of agents— including Klarna, Uber, J.P. Morgan, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.
LangGraph is very low-level, and focused entirely on agent **orchestration**.
Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with models and tools.
We will commonly use LangChain components throughout the documentation to integrate models and tools, but you don’t need to use LangChain to use LangGraph.
If you are just getting started with agents or want a higher-level abstraction, we recommend you use LangChain’s agents that provide prebuilt architectures for common LLM and tool-calling loops.
LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.
…
```
from langgraph.graph import StateGraph, MessagesState, START, END
def mock_llm(state: MessagesState):
return {"messages": [{"role": "ai", "content": "hello world"}]}
graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()
graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```
## ​ Core benefits
LangGraph provides low-level supporting infrastructure for *any* long-running, stateful workflow or agent.
LangGraph does not abstract prompts or architecture, and provides the following central benefits: - Durable execution: Build agents that persist through failures and can run for extended periods, resuming from where they left off.
- Human-in-the-loop: Incorporate human oversight by inspecting and modifying agent state at any point.
- Comprehensive memory: Create stateful agents with both short-term working memory for ongoing reasoning and long-term memory across sessions.
- Debugging with LangSmith: Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.

## ​ Graphs
At its core, LangGraph models agent workflows as graphs. You define the behavior of your agents using three key components: 1. `State`: A shared data structure that represents the current snapshot of your application. It can be any data type, but is typically defined using a shared state schema.
2. `Nodes`: Functions that encode the logic of your agents.
They receive the current state as input, perform some computation or side-effect, and return an updated state.
3. `Edges`: Functions that determine which `Node` to execute next based on the current state. They can be conditional branches or fixed transitions.
By composing `Nodes` and `Edges`, you can create complex, looping workflows that evolve the state over time.
The real power, though, comes from how LangGraph manages that state. To emphasize: `Nodes` and `Edges` are nothing more than functions—they can contain an LLM or just good ol’ code. In short: *nodes do the work, edges tell what to do next*. LangGraph’s underlying graph algorithm uses message passing to define a general program.
When a Node completes its operation, it sends messages along one or more edges to other node(s). These recipient nodes then execute their functions, pass the resulting messages to the next set of nodes, and the process continues. Inspired by Google’s Pregel system, the program proceeds in discrete “super-steps.” A super-step can be considered a single iteration over the graph nodes.
Nodes that run in parallel are part of the same super-step, while nodes that run sequentially belong to separate super-steps. At the start of graph execution, all nodes begin in an `inactive` state. A node becomes `active` when it receives a new message (state) on any of its incoming edges (or “channels”).
The active node then runs its function and responds with updates. At the end of each super-step, nodes with no incoming messages vote to `halt` by marking themselves as `inactive`. The graph execution terminates when all nodes are `inactive` and no messages are in transit.

…

### ​ Compiling your graph
To build your graph, you first define the state, you then add nodes and edges, and then you compile it. What exactly is compiling your graph and why is it needed? Compiling is a pretty simple step. It provides a few basic checks on the structure of your graph (no orphaned nodes, etc). It is also where you can specify runtime args like checkpointers and breakpoints. You compile your graph by just calling the `.compile` method:

…

## ​ State
The first thing you do when you define a graph is define the `State` of the graph. The `State` consists of the schema of the graph as well as `reducer` functions which specify how to apply updates to the state. The schema of the `State` will be the input schema to all `Nodes` and `Edges` in the graph, and can be either a `TypedDict` or a `Pydantic` model. All `Nodes` will emit updates to the `State` which are then applied using the specified `reducer` function.

### ​ Schema
The main documented way to specify the schema of a graph is by using a `TypedDict`. If you want to provide default values in your state, use a `dataclass`. We also support using a Pydantic `BaseModel` as your graph state if you want recursive data validation (though note that Pydantic is less performant than a `TypedDict` or `dataclass`).

…

We may also want to use different input / output schemas for the graph. The output might, for example, only contain a single relevant output key.
It is possible to have nodes write to private state channels inside the graph for internal node communication. We can simply define a private schema, `PrivateState`. It is also possible to define explicit input and output schemas for a graph.
In these cases, we define an “internal” schema that contains *all* keys relevant to graph operations. But, we also define `input` and `output` schemas that are sub-sets of the “internal” schema to constrain the input and output of the graph. See Define input and output schemas for more detail.

…

```
class InputState(TypedDict):
 user_input: str

class OutputState(TypedDict):
 graph_output: str

class OverallState(TypedDict):
 foo: str
 user_input: str
 graph_output: str

class PrivateState(TypedDict):
 bar: str

def node_1(state: InputState) -> OverallState:
 # Write to OverallState
 return {"foo": state["user_input"] + " name"}

def node_2(state: OverallState) -> PrivateState:
 # Read from OverallState, write to PrivateState
 return {"bar": state["foo"] + " is"}

def node_3(state: PrivateState) -> OutputState:
 # Read from PrivateState, write to OutputState
 return {"graph_output": state["bar"] + " Lance"}

builder = StateGraph(OverallState,input_schema=InputState,output_schema=OutputState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", node_2)
builder.add_node("node_3", node_3)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
builder.add_edge("node_2", "node_3")
builder.add_edge("node_3", END)

graph = builder.compile()
graph.invoke({"user_input":"My"})
# {'graph_output': 'My name is Lance'}

```
There are two subtle and important points to note here: 1. We pass `state: InputState` as the input schema to `node_1`. But, we write out to `foo`, a channel in `OverallState`. How can we write out to a state channel that is not included in the input schema? This is because a node *can write to any state channel in the graph state.* The graph state is the union of the state channels defined at initialization, which includes `OverallState` and the filters `InputState` and `OutputState`.
2. We initialize the graph with:

…

### ​ Reducers
Reducers are key to understanding how updates from nodes are applied to the `State`. Each key in the `State` has its own independent reducer function. If no reducer function is explicitly specified then it is assumed that all updates to that key should override it. There are a few different types of reducers, starting with the default type of reducer:

…

#### ​ Overwrite

### ​ Working with messages in graph state

#### ​ Why use messages?
Most modern LLM providers have a chat model interface that accepts a list of messages as input. LangChain’s chat model interface in particular accepts a list of message objects as inputs. These messages come in a variety of forms such as `HumanMessage` (user input) or `AIMessage` (LLM response). To read more about what message objects are, please refer to the Messages conceptual guide.

#### ​ Using messages in your graph
In many cases, it is helpful to store prior conversation history as a list of messages in your graph state. To do so, we can add a key (channel) to the graph state that stores a list of `Message` objects and annotate it with a reducer function (see `messages` key in the example below).

…

#### ​ Serialization
In addition to keeping track of message IDs, the `add_messages` function will also try to deserialize messages into LangChain `Message` objects whenever a state update is received on the `messages` channel. For more information, see LangChain serialization/deserialization. This allows sending graph inputs / state updates in the following format:

…

#### ​ MessagesState
Since having a list of messages in your state is so common, there exists a prebuilt state called `MessagesState` which makes it easy to use messages. `MessagesState` is defined with a single `messages` key which is a list of `AnyMessage` objects and uses the `add_messages` reducer. Typically, there is more state to track than just messages, so we see people subclass this state and add more fields, like:

…

## ​ Nodes
In LangGraph, nodes are Python functions (either synchronous or asynchronous) that accept the following arguments: 1. `state`—The state of the graph
2. `config`—A `RunnableConfig` object that contains configuration information like `thread_id` and tracing information like `tags`
3. `runtime`—A `Runtime` object that contains runtime `context` and other information like `store`, `stream_writer`, `execution_info`, and `server_info`
Similar to `NetworkX`, you add these nodes to a graph using the `add_node` method:

…

### ​ Node caching
LangGraph supports caching of tasks/nodes based on the input to the node. To use caching: - Specify a cache when compiling a graph (or specifying an entrypoint)
- Specify a cache policy for nodes. Each cache policy supports:
  - `key_func` used to generate a cache key based on the input to a node, which defaults to a `hash` of the input with pickle.
  - `ttl`, the time to live for the cache in seconds. If not specified, the cache will never expire.
For example:
```
import time
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy

class State(TypedDict):
 x: int
 result: int

builder = StateGraph(State)

def expensive_node(state: State) -> dict[str, int]:
 # expensive computation
 time.sleep(2)
 return {"result": state["x"] * 2}

builder.add_node("expensive_node", expensive_node, cache_policy=CachePolicy(ttl=3))
builder.set_entry_point("expensive_node")
builder.set_finish_point("expensive_node")

graph = builder.compile(cache=InMemoryCache())

print(graph.invoke({"x": 5}, stream_mode='updates'))
# [{'expensive_node': {'result': 10}}]
print(graph.invoke({"x": 5}, stream_mode='updates'))
# [{'expensive_node': {'result': 10}, '__metadata__': {'cached': True}}]

```

…

## ​ Edges
Edges define how the logic is routed and how the graph decides to stop. This is a big part of how your agents work and how different nodes communicate with each other. There are a few key types of edges: - Normal Edges: Go directly from one node to the next.
- Conditional Edges: Call a function to determine which node(s) to go to next.
- Entry Point: Which node to call first when user input arrives.
- Conditional Entry Point: Call a function to determine which node(s) to call first when user input arrives.
A node can have multiple outgoing edges. If a node has multiple outgoing edges, **all** of those destination nodes will be executed in parallel as a part of the next superstep.

…

Similar to nodes, the `routing_function` accepts the current `state` of the graph and returns a value. By default, the return value `routing_function` is used as the name of the node (or list of nodes) to send the state to next. All those nodes will be run in parallel as a part of the next superstep. You can optionally provide a dictionary that maps the `routing_function`’s output to the name of the next node.

…

```
from langgraph.types import Command, interrupt

def human_review(state: State):
 # Pauses the graph and waits for a value
 answer = interrupt("Do you approve?")
 return {"messages": [{"role": "user", "content": answer}]}

# First invocation - hits the interrupt and pauses
result = graph.invoke({"messages": [...]}, config)

# Resume with a value - the interrupt() call returns "yes"
result = graph.invoke(Command(resume="yes"), config)

```

…

## ​ Graph migrations
LangGraph can easily handle migrations of graph definitions (nodes, edges, and state) even when using a checkpointer to track state. - For threads at the end of the graph (i.e. not interrupted) you can change the entire topology of the graph (i.e. all nodes and edges, remove, add, rename, etc)

…

```
from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.managed import RemainingSteps

class State(TypedDict):
 messages: Annotated[list, lambda x, y: x + y]
 remaining_steps: RemainingSteps # Managed value - tracks steps until limit

def reasoning_node(state: State) -> dict:
 # RemainingSteps is automatically populated by LangGraph
 remaining = state["remaining_steps"]

 # Check if we're running low on steps
 if remaining <= 2:
 return {"messages": ["Approaching limit, wrapping up..."]}

 # Normal processing
 return {"messages": ["thinking..."]}

def route_decision(state: State) -> Literal["reasoning_node", "fallback_node"]:
 """Route based on remaining steps"""
 if state["remaining_steps"] <= 2:
 return "fallback_node"
 return "reasoning_node"

def fallback_node(state: State) -> dict:
 """Handle cases where recursion limit is approaching"""
 return {"messages": ["Reached complexity limit, providing best effort answer"]}

# Build graph
builder = StateGraph(State)
builder.add_node("reasoning_node", reasoning_node)
builder.add_node("fallback_node", fallback_node)
builder.add_edge(START, "reasoning_node")
builder.add_conditional_edges("reasoning_node", route_decision)
builder.add_edge("fallback_node", END)

graph = builder.compile()

# RemainingSteps works with any recursion_limit
result = graph.invoke({"messages": []}, {"recursion_limit": 10})

```

…

```
from typing import Annotated, Literal, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.managed import RemainingSteps
from langgraph.errors import GraphRecursionError

class State(TypedDict):
 messages: Annotated[list, lambda x, y: x + y]
 remaining_steps: RemainingSteps

# Proactive Approach (recommended) - using RemainingSteps
def agent_with_monitoring(state: State) -> dict:
 """Proactively monitor and handle recursion within the graph"""
 remaining = state["remaining_steps"]

 # Early detection - route to internal handling
 if remaining <= 2:
 return {
 "messages": ["Approaching limit, returning partial result"]
 }

 # Normal processing
 return {"messages": [f"Processing... ({remaining} steps remaining)"]}

def route_decision(state: State) -> Literal["agent", END]:
 if state["remaining_steps"] <= 2:
 return END
 return "agent"

# Build graph
builder = StateGraph(State)
builder.add_node("agent", agent_with_monitoring)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", route_decision)
graph = builder.compile()

# Proactive: Graph completes gracefully
result = graph.invoke({"messages": []}, {"recursion_limit": 10})

# Reactive Approach (fallback) - catching error externally
try:
 result = graph.invoke({"messages": []}, {"recursion_limit": 10})
except GraphRecursionError as e:
 # Handle externally after graph execution fails
 result = {"messages": ["Fallback: recursion limit exceeded"]}

```

### Community links
...
- docs.langchain.com/oss/python/langgraph
…

# 🚀 LangGraph Quickstart¶

In this tutorial, we will build a support chatbot in LangGraph that can:

**Answer common questions** by searching the web

**Maintain conversation state** across calls

**Route complex queries** to a human for review

**Use custom state** to control its behavior

**Rewind and explore** alternative conversation paths

…

## Part 1: Build a Basic Chatbot¶

We'll first create a simple chatbot using LangGraph. This chatbot will respond directly to user messages. Though simple, it will illustrate the core concepts of building with LangGraph. By the end of this section, you will have a built rudimentary chatbot.

Start by creating a

`StateGraph`. A

`StateGraph` object defines the structure of our chatbot as a "state machine". We'll add
`nodes` to represent the llm and functions our chatbot can call and

`edges` to specify how the bot should transition between these functions.

*API Reference: StateGraph | START | END | add_messages*

…

Our graph can now handle two key tasks:

- Each

`node`can receive the current

`State`as input and output an update to the state.

- Updates to

`messages`will be appended to the existing list rather than overwriting it, thanks to the prebuilt

`add_messages`function used with the
`Annotated`syntax.

Concept

When defining a graph, the first step is to define its

`State`. The

`State` includes the graph's schema and reducer functions that handle state updates. In our example,

`State` is a

`TypedDict` with one key:

`messages`. The

`add_messages` reducer function is used to append new messages to the list instead of overwriting it. Keys without a reducer annotation will overwrite previous values. Learn more about state, reducers, and related concepts in this guide.

…

```

from langchain.chat_models import init_chat_model

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

def chatbot(state: State):

return {"messages": [llm.invoke(state["messages"])]}

# The first argument is the unique node name

# The second argument is the function or object that will be called whenever

# the node is used.

graph_builder.add_node("chatbot", chatbot)

```
**Notice** how the

`chatbot` node function takes the current

`State` as input and returns a dictionary containing an updated

`messages` list under the key "messages". This is the basic pattern for all LangGraph node functions.

The

`add_messages` function in our

`State` will append the llm's response messages to whatever messages are already in the state.

…

("anthropic:claude-3-5-sonnet-latest") def chatbot(state: State): return {"messages": [llm.invoke(state["messages"])]} # The first argument is the unique node name # The second argument is the function or object that will be called whenever # the node is used. graph_builder.add_node("chatbot", chatbot) graph_builder.set_entry_point("chatbot") graph_builder.set_finish_point("chatbot") graph = graph_builder.compile()`

…

```

{'query': "What's a 'node' in LangGraph?",

'follow_up_questions': None,

'answer': None,

'images': [],

'results': [{'title': "Introduction to LangGraph: A Beginner's Guide - Medium",

'url': 'https://medium.com/@cplog/introduction-to-langgraph-a-beginners-guide-14f9be027141',

'content': 'Stateful Graph: LangGraph revolves around the concept of a stateful graph, where each node in the graph represents a step in your computation, and the graph maintains a state that is passed around and updated as the computation progresses. LangGraph supports conditional edges, allowing you to dynamically determine the next node to execute based on the current state of the graph. We define nodes for classifying the input, handling greetings, and handling search queries. def classify_input_node(state): LangGraph is a versatile tool for building complex, stateful applications with LLMs. By understanding its core concepts and working through simple examples, beginners can start to leverage its power for their projects. Remember to pay attention to state management, conditional edges, and ensuring there are no dead-end nodes in your graph.',

'score': 0.7065353,

'raw_content': None},

{'title': 'LangGraph Tutorial: What Is LangGraph and How to Use It?',

'url': 'https://www.datacamp.com/tutorial/langgraph-tutorial',

'content': 'LangGraph is a library within the LangChain ecosystem that provides a framework for defining, coordinating, and executing multiple LLM agents (or chains) in a structured and efficient manner. By managing the flow of data and the sequence of operations, LangGraph allows developers to focus on the high-level logic of their applications rather than the intricacies of agent coordination. Whether you need a chatbot that can handle various types of user requests or a multi-agent system that performs complex tasks, LangGraph provides the tools to build exactly what you need. LangGraph significantly simplifies the development of complex LLM applications by providing a structured framework for managing state and coordinating agent interactions.',

'score': 0.5008063,

'raw_content': None}],

'response_time': 1.38}

```
The results are page summaries our chat bot can use to answer questions.

Next, we'll start defining our graph. The following is all

**the same as in Part 1**, except we have added

`bind_tools` on our LLM. This lets the LLM know the correct JSON format to use if it wants to use our search engine.

…

```

from typing import Annotated

from langchain.chat_models import init_chat_model

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages

class State(TypedDict):

messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

# Modification: tell the LLM which tools it can call

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):

return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

```

…

```

def route_tools(

state: State,

):

"""

Use in the conditional_edge to route to the ToolNode if the last message

has tool calls. Otherwise, route to the end.

"""

if isinstance(state, list):

ai_message = state[-1]

elif messages := state.get("messages", []):

ai_message = messages[-1]

else:

raise ValueError(f"No messages found in input state to tool_edge: {state}")

if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:

return "tools"

return END

# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if

# it is fine directly responding. This conditional routing defines the main agent loop.

graph_builder.add_conditional_edges(

"chatbot",

route_tools,

# The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node

# It defaults to the identity function, but if you

# want to use a node named something else apart from "tools",

# You can update the value of the dictionary to something else

# e.g., "tools": "my_tools"

{"tools": "tools", END: END},



# Any time a tool is called, we return to the chatbot to decide the next step

graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

```

…

```

Assistant: [{'text': "To provide you with accurate and up-to-date information about LangGraph, I'll need to search for the latest details. Let me do that for you.", 'type': 'text'}, {'id': 'toolu_01Q588CszHaSvvP2MxRq9zRD', 'input': {'query': 'LangGraph AI tool information'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]

Assistant: [{"url": "https://www.langchain.com/langgraph", "content": "LangGraph sets the foundation for how we can build and scale AI workloads \u2014 from conversational agents, complex task automation, to custom LLM-backed experiences that 'just work'. The next chapter in building complex production-ready features with LLMs is agentic, and with LangGraph and LangSmith, LangChain delivers an out-of-the-box solution ..."}, {"url": "https://github.com/langchain-ai/langgraph", "content": "Overview. LangGraph is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. Compared to other LLM frameworks, it offers these core benefits: cycles, controllability, and persistence. LangGraph allows you to define flows that involve cycles, essential for most agentic architectures ..."}]

Assistant: Based on the search results, I can provide you with information about LangGraph:

1. Purpose:

LangGraph is a library designed for building stateful, multi-actor applications with Large Language Models (LLMs). It's particularly useful for creating agent and multi-agent workflows.

2. Developer:

LangGraph is developed by LangChain, a company known for its tools and frameworks in the AI and LLM space.

3. Key Features:

- Cycles: LangGraph allows the definition of flows that involve cycles, which is essential for most agentic architectures.

- Controllability: It offers enhanced control over the application flow.

- Persistence: The library provides ways to maintain state and persistence in LLM-based applications.

4. Use Cases:

LangGraph can be used for various applications, including:

- Conversational agents

- Complex task automation

- Custom LLM-backed experiences

5. Integration:

LangGraph works in conjunction with LangSmith, another tool by LangChain, to provide an out-of-the-box solution for building complex, production-ready features with LLMs.

6. Significance:

LangGraph is described as setting the foundation for building and scaling AI workloads. It's positioned as a key tool in the next chapter of LLM-based application development, particularly in the realm of agentic AI.

7. Availability:

LangGraph is open-source and available on GitHub, which suggests that developers can access and contribute to its codebase.

8. Comparison to Other Frameworks:

LangGraph is noted to offer unique benefits compared to other LLM frameworks, particularly in its ability to handle cycles, provide controllability, and maintain persistence.

LangGraph appears to be a significant tool in the evolving landscape of LLM-based application development, offering developers new ways to create more complex, stateful, and interactive AI systems.

Goodbye!

```

…

(tools) def chatbot(state: State): return {"messages": [llm_with_tools.invoke(state["messages"])]} graph_builder.add_node("chatbot", chatbot) tool_node = ToolNode(tools=[tool]) graph_builder.add_node("tools", tool_node) graph_builder.add_conditional_edges( "chatbot", tools_condition, ) # Any time a tool is called, we return to the chatbot to decide the next step graph_builder.add_edge("tools", "chatbot") graph_builder.set_entry_point("chatbot") graph = graph_builder.compile()`

…

`thread_id`, the graph loads its saved state, allowing the chatbot to pick up where it left off.

We will see later that

**checkpointing** is *much* more powerful than simple chat memory - it lets you save and resume complex state at any time for error recovery, human-in-the-loop workflows, time travel interactions, and more. But before we get too ahead of ourselves, let's add checkpointing to enable multi-turn conversations.

…

```

StateSnapshot(values={'messages': [HumanMessage(content='Hi there! My name is Will.', additional_kwargs={}, response_metadata={}, id='8c1ca919-c553-4ebf-95d4-b59a2d61e078'), AIMessage(content="Hello Will! It's nice to meet you. How can I assist you today? Is there anything specific you'd like to know or discuss?", additional_kwargs={}, response_metadata={'id': 'msg_01WTQebPhNwmMrmmWojJ9KXJ', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 405, 'output_tokens': 32}}, id='run-58587b77-8c82-41e6-8a90-d62c444a261d-0', usage_metadata={'input_tokens': 405, 'output_tokens': 32, 'total_tokens': 437}), HumanMessage(content='Remember my name?', additional_kwargs={}, response_metadata={}, id='daba7df6-ad75-4d6b-8057-745881cea1ca'), AIMessage(content="Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.", additional_kwargs={}, response_metadata={'id': 'msg_01E41KitY74HpENRgXx94vag', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 444, 'output_tokens': 58}}, id='run-ffeaae5c-4d2d-4ddb-bd59-5d5cbf2a5af8-0', usage_metadata={'input_tokens': 444, 'output_tokens': 58, 'total_tokens': 502})]}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef7d06e-93e0-6acc-8004-f2ac846575d2'}}, metadata={'source': 'loop', 'writes': {'chatbot': {'messages': [AIMessage(content="Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.", additional_kwargs={}, response_metadata={'id': 'msg_01E41KitY74HpENRgXx94vag', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 444, 'output_tokens': 58}}, id='run-ffeaae5c-4d2d-4ddb-bd59-5d5cbf2a5af8-0', usage_metadata={'input_tokens': 444, 'output_tokens': 58, 'total_tokens': 502})]}}, 'step': 4, 'parents': {}}, created_at='2024-09-27T19:30:10.820758+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef7d06e-859f-6206-8003-e1bd3c264b8f'}}, tasks=())

```

…

The snapshot above contains the current state values, corresponding config, and the

`next` node to process. In our case, the graph has reached an

`END` state, so

`next` is empty.

**Congratulations!** Your chatbot can now maintain conversation state across sessions thanks to LangGraph's checkpointing system. This opens up exciting possibilities for more natural, contextual interactions. LangGraph's checkpointing even handles **arbitrarily complex graph states**, which is much more expressive and powerful than simple chat memory.

…

```

from typing import Annotated

from langchain.chat_models import init_chat_model

from langchain_tavily import TavilySearch

from langchain_core.tools import tool

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.types import Command, interrupt

class State(TypedDict):

messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool

def human_assistance(query: str) -> str:

"""Request assistance from a human."""

human_response = interrupt({"query": query})

return human_response["data"]

tool = TavilySearch(max_results=2)

tools = [tool, human_assistance]

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):

message = llm_with_tools.invoke(state["messages"])

# Because we will be interrupting during tool execution,

# we disable parallel tool calling to avoid repeating any

# tool invocations when we resume.

assert len(message.tool_calls) <= 1

return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)

graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(

"chatbot",

tools_condition,



graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge(START, "chatbot")

```

…

**Congrats!** You've used an

`interrupt` to add human-in-the-loop execution to your chatbot, allowing for human oversight and intervention when needed. This opens up the potential UIs you can create with your AI systems. Since we have already added a

**checkpointer**, as long as the underlying persistence layer is running, the graph can be paused **indefinitely** and resumed at any time as if nothing had happened.

…

= interrupt({"query": query}) return human_response["data"] tool = TavilySearch(max_results=2) tools = [tool, human_assistance] llm = init_chat_model("anthropic:claude-3-5-sonnet-latest") llm_with_tools = llm.bind_tools(tools
) def chatbot(state: State): message = llm_with_tools.invoke(state["messages"]) assert(len(message.tool_calls) <= 1) return {"messages": [message]} graph_builder.add_node("chatbot", chatbot) tool_node = ToolNode(tools=tools) graph_builder.add_node("tools", tool_node) graph_builder.add_conditional_edges( "chatbot", tools_condition, ) graph_builder.add_edge("tools", "chatbot") graph_builder.add_edge(START, "chatbot") memory = MemorySaver() graph = graph_builder.compile(checkpointer=memory)`

## Part 5: Customizing State¶

So far, we've relied on a simple state with one entry-- a list of messages. You can go far with this simple state, but if you want to define complex behavior without relying on the message list, you can add additional fields to the state. Here we will demonstrate a new scenario, in which the chatbot is using its search tool to find specific information, and forwarding them to a human for review. Let's have the chatbot research the birthday of an entity. We will add

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
[Memory](https://langchain-ai.github.io/langgraph/concepts/memory/): LLM should read this page when implementing memory systems for AI agents, managing conversation context across sessions, or designing systems that require both short-term and long-term information retention. This page explains memory systems in LangGraph, covering short-term (thread-scoped) memory for managing conversation history and long-term memory across threads, with techniques for handling long conversations, summarizing past interactions, and organizing persistent memories in namespaces.

…

[Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/): LLM should read this page when needing to understand LangGraph persistence mechanisms, implementing stateful workflows, or managing conversation history across interactions. This page covers LangGraph's persistence features including checkpointers, threads, state snapshots, replay functionality, forking state, cross-thread memory via InMemoryStore, and semantic search capabilities for stored memories.

…

[LangGraph Platform Architecture](https://langchain-ai.github.io/langgraph/concepts/platform_architecture/): LLM should read this page when needing to understand LangGraph Platform's technical architecture or troubleshooting deployment issues. The page details how LangGraph Platform uses Postgres for persistent storage of user/run data and Redis for worker communication (run cancellation, output streaming) and ephemeral metadata storage (retry attempts).
[LangGraph's Runtime (Pregel)](https://langchain-ai.github.io/langgraph/concepts/pregel/): LLM should read this page when learning about LangGraph's runtime, implementing applications with Pregel directly, or understanding how LangGraph executes graph applications. Explains LangGraph's Pregel runtime which manages graph application execution through a three-phase process (Plan, Execution, Update), describes different channel types (LastValue, Topic, Context, BinaryOperatorAggregate), provides direct implementation examples, and contrasts the StateGraph API with the Functional API.

…

## How Tos

[How-to Guides](https://langchain-ai.github.io/langgraph/how-tos/): LLM should read this page when looking for specific implementation techniques in LangGraph or when trying to deploy LangGraph applications to production environments. This page contains an extensive collection of how-to guides for LangGraph, covering graph fundamentals, persistence, memory management, human-in-the-loop features, tool calling, multi-agent systems, streaming, and deployment options through LangGraph Platform.

…

[How to integrate LangGraph with AutoGen, CrewAI, and other frameworks](https://langchain-ai.github.io/langgraph/how-tos/autogen-integration/): LLM should read this page when integrating LangGraph with other agent frameworks, building multi-agent systems, or adding persistence features to agents. The page demonstrates how to combine LangGraph with AutoGen by calling AutoGen agents inside LangGraph nodes, showing code examples for setting up the integration with memory and conversation persistence.

…

[How to define input/output schema for your graph](https://langchain-ai.github.io/langgraph/how-tos/input_output_schema/): LLM should read this page when needing to define separate input/output schemas for LangGraph, implementing schema-based data filtering, or understanding schema definitions in StateGraph. This page explains how to define distinct input and output schemas for a StateGraph, showing how input schema validates the provided data structure while output schema filters internal data to return only relevant information, with code examples demonstrating implementation.

…

[How to add summary of the conversation history](https://langchain-ai.github.io/langgraph/how-tos/memory/add-summary-conversation-history/): LLM should read this page when implementing conversation summarization, managing context windows, or building chatbots with memory management. This page demonstrates how to add summary functionality to conversation history using LangGraph, including checking conversation length, creating summaries, and removing old messages while maintaining context.

…

[How to create a sequence of steps](https://langchain-ai.github.io/langgraph/how-tos/sequence/): LLM should read this page when implementing sequential workflows in LangGraph, creating multi-step processes in applications, or learning about state management in graph-based systems. This page explains how to create sequences in LangGraph, covering methods for building sequential graphs using .add_node/.add_edge or the shorthand .add_sequence, defining state with TypedDict, creating nodes as functions that update state, and compiling/invoking graphs with examples.