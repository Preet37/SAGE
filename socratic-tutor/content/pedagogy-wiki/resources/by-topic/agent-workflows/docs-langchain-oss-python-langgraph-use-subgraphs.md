# Source: https://docs.langchain.com/oss/python/langgraph/use-subgraphs
# Title: Subgraphs - Docs by LangChain
# Fetched via: browser
# Date: 2026-04-10

This guide explains the mechanics of using subgraphs. A subgraph is a graph that is used as a node in another graph.
Subgraphs are useful for:
Building multi-agent systems
Reusing a set of nodes in multiple graphs
Distributing development: when you want different teams to work on different parts of the graph independently, you can define each part as a subgraph, and as long as the subgraph interface (the input and output schemas) is respected, the parent graph can be built without knowing any details of the subgraph
​
Setup
pip
uv
pip install -U langgraph

Set up LangSmith for LangGraph development Sign up for LangSmith to quickly spot issues and improve the performance of your LangGraph projects. LangSmith lets you use trace data to debug, test, and monitor your LLM apps built with LangGraph—read more about how to get started with LangSmith.
​
Define subgraph communication
When adding subgraphs, you need to define how the parent graph and the subgraph communicate:
Pattern	When to use	State schemas
Call a subgraph inside a node	Parent and subgraph have different state schemas (no shared keys), or you need to transform state between them	You write a wrapper function that maps parent state to subgraph input and subgraph output back to parent state
Add a subgraph as a node	Parent and subgraph share state keys—the subgraph reads from and writes to the same channels as the parent	You pass the compiled subgraph directly to add_node—no wrapper function needed
​
Call a subgraph inside a node
When the parent graph and subgraph have different state schemas (no shared keys), invoke the subgraph inside a node function. This is common when you want to keep a private message history for each agent in a multi-agent system.
The node function transforms the parent state to the subgraph state before invoking the subgraph, and transforms the results back to the parent state before returning.
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

class SubgraphState(TypedDict):
    bar: str

# Subgraph

def subgraph_node_1(state: SubgraphState):
    return {"bar": "hi! " + state["bar"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# Parent graph

class State(TypedDict):
    foo: str

def call_subgraph(state: State):
    # Transform the state to the subgraph state
    subgraph_output = subgraph.invoke({"bar": state["foo"]})
    # Transform response back to the parent state
    return {"foo": subgraph_output["bar"]}

builder = StateGraph(State)
builder.add_node("node_1", call_subgraph)
builder.add_edge(START, "node_1")
graph = builder.compile()


Full example: different state schemas

Full example: different state schemas (two levels of subgraphs)

​
Add a subgraph as a node
When the parent graph and subgraph share state keys, you can pass a compiled subgraph directly to add_node. No wrapper function is needed—the subgraph reads from and writes to the parent’s state channels automatically. For example, in multi-agent systems, the agents often communicate over a shared messages key.
If your subgraph shares state keys with the parent graph, you can follow these steps to add it to your graph:
Define the subgraph workflow (subgraph_builder in the example below) and compile it
Pass compiled subgraph to the add_node method when defining the parent graph workflow
from typing_extensions import TypedDict
from langgraph.graph.state import StateGraph, START

class State(TypedDict):
    foo: str

# Subgraph

def subgraph_node_1(state: State):
    return {"foo": "hi! " + state["foo"]}

subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()

# Parent graph

builder = StateGraph(State)
builder.add_node("node_1", subgraph)
builder.add_edge(START, "node_1")
graph = builder.compile()


Full example: shared state schemas

​
Subgraph persistence
When you use a subgraph, you need to decide what happens to its internal data between calls. Consider a customer support bot that delegates to specialist subagents: should the “billing expert” subagent remember the customer’s earlier questions, or start fresh each time it’s called?
The checkpointer parameter on .compile() controls subgraph persistence:
Mode	checkpointer=	Behavior
Per-invocation	None (default)	Each call starts fresh and inherits the parent’s checkpointer to support interrupts and durable execution within a single call.
Per-thread	True	State accumulates across calls on the same thread. Each call picks up where the last one left off.
Stateless	False	No checkpointing at all—runs like a plain function call. No interrupts or durable execution.
Per-invocation is the right choice for most applications, including multi-agent systems where subagents handle independent requests. Use per-thread when a subagent needs multi-turn conversation memory (for example, a research assistant that builds context over several exchanges).
The parent graph must be compiled with a checkpointer for subgraph persistence features (interrupts, state inspection, per-thread memory) to work. See persistence.
The examples below use LangChain’s create_agent, which is a common way to build agents. create_agent produces a LangGraph graph under the hood, so all subgraph persistence concepts apply directly. If you’re building with raw LangGraph StateGraph, the same patterns and configuration options apply—see the Graph API for details.
​
Stateful
Stateful subgraphs inherit the parent graph’s checkpointer, which enables interrupts, durable execution, and state inspection. The two stateful modes differ in how long state is retained.
​
Per-invocation (default)
This is the recommended mode for most applications, including multi-agent systems where subagents are invoked as tools. It supports interrupts, durable execution, and parallel calls while keeping each invocation isolated.
Use per-invocation persistence when each call to the subgraph is independent and the subagent doesn’t need to remember anything from previous calls. This is the most common pattern, especially for multi-agent systems where subagents handle one-off requests like “look up this customer’s order” or “summarize this document.”
Omit checkpointer or set it to None. Each call starts fresh, but within a single call the subgraph inherits the parent’s checkpointer and can use interrupt() to pause and resume.
The following examples use two subagents (fruit expert, veggie expert) wrapped as tools for an outer agent:
from langchain.agents import create_agent
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt

@tool
def fruit_info(fruit_name: str) -> str:
    """Look up fruit info."""
    return f"Info about {fruit_name}"

@tool
def veggie_info(veggie_name: str) -> str:
    """Look up veggie info."""
    return f"Info about {veggie_name}"

# Subagents - no checkpointer setting (inherits parent)
fruit_agent = create_agent(
    model="gpt-4.1-mini",
    tools=[fruit_info],
    prompt="You are a fruit expert. Use the fruit_info tool. Respond in one sentence.",
)

veggie_agent = create_agent(
    model="gpt-4.1-mini",
    tools=[veggie_info],
    prompt="You are a veggie expert. Use the veggie_info tool. Respond in one sentence.",
)

# Wrap subagents as tools for the outer agent
@tool
def ask_fruit_expert(question: str) -> str:
    """Ask the fruit expert. Use for ALL fruit questions."""
    response = fruit_agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
    )
    return response["messages"][-1].content

@tool
def ask_veggie_expert(question: str) -> str:
    """Ask the veggie expert. Use for ALL veggie questions."""
    response = veggie_agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
    )
    return response["messages"][-1].content

# Outer agent with checkpointer
agent = create_agent(
    model="gpt-4.1-mini",
    tools=[ask_fruit_expert, ask_veggie_expert],
    prompt=(
        "You have two experts: ask_fruit_expert and ask_veggie_expert. "
        "ALWAYS delegate questions to the appropriate expert."
    ),
    checkpointer=MemorySaver(),
)

Interrupts
Multi-turn
Multiple subgraph calls
Each invocation can use interrupt() to pause and resume. Add interrupt() to a tool function to require user approval before proceeding:
@tool
def fruit_info(fruit_name: str) -> str:
    """Look up fruit info."""
    interrupt("continue?")
    return f"Info about {fruit_name}"

config = {"configurable": {"thread_id": "1"}}

# Invoke - the subagent's tool calls interrupt()
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Tell me about apples"}]},
    config=config,
)
# response contains __interrupt__

# Resume - approve the interrupt
response = agent.invoke(Command(resume=True), config=config)
# Subagent message count: 4

​
Per-thread
Use per-thread persistence when a subagent needs to remember previous interactions. For example, a research assistant that builds up context over several exchanges, or a coding assistant that tracks what files it has already edited. The subagent’s conversation history and data accumulate across calls on the same thread. Each call picks up where the last one left off.
Compile with checkpointer=True to enable this behavior.
Per-thread subgraphs do not support parallel tool calls. When an LLM has access to a per-thread subagent as a tool, it may try to call that tool multiple times in parallel (for example, asking the fruit expert about apples and bananas simultaneously). This causes checkpoint conflicts because both calls write to the same namespace.
The examples below use LangChain’s ToolCallLimitMiddleware to prevent this. If you’re building with pure LangGraph StateGraph, you need to prevent parallel tool calls yourself—for example, by configuring your model to disable parallel tool calling or by adding logic to ensure the same subgraph is not invoked multiple times in parallel.
The following examples use a fruit expert subagent compiled with checkpointer=True:
from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command, interrupt

@tool
def fruit_info(fruit_name: str) -> str:
    """Look up fruit info."""
    return f"Info about {fruit_name}"

# Subagent with checkpointer=True for persistent state
fruit_agent = create_agent(
    model="gpt-4.1-mini",
    tools=[fruit_info],
    prompt="You are a fruit expert. Use the fruit_info tool. Respond in one sentence.",
    checkpointer=True,
)

# Wrap subagent as a tool for the outer agent
@tool
def ask_fruit_expert(question: str) -> str:
    """Ask the fruit expert. Use for ALL fruit questions."""
    response = fruit_agent.invoke(
        {"messages": [{"role": "user", "content": question}]},
    )
    return response["messages"][-1].content

# Outer agent with checkpointer
# Use ToolCallLimitMiddleware to prevent parallel calls to per-thread subagents,
# which would cause checkpoint conflicts.
agent = create_agent(
    model="gpt-4.1-mini",
    tools=[ask_fruit_expert],
    prompt="You have a fruit expert. ALWAYS delegate fruit questions to ask_fruit_expert.",
    middleware=[
        ToolCallLimitMiddleware(tool_name="ask_fruit_expert", run_limit=1),
    ],
    checkpointer=MemorySaver(),
)

Interrupts
Multi-turn
Multiple subgraph calls
Per-thread subagents support interrupt() just like per-invocation. Add interrupt() to a tool function to require user approval:
@tool
def fruit_info(fruit_name: str) -> str:
    """Look up fruit info."""
    interrupt("continue?")
    return f"Info about {fruit_name}"

config = {"configurable": {"thread_id": "1"}}

# Invoke - the subagent's tool calls interrupt()
response = agent.invoke(
    {"messages": [{"role": "user", "content": "Tell me about apples"}]},
    config=config,
)
# response contains __interrupt__

# Resume - approve the interrupt
response = agent.invoke(Command(resume=True), config=config)
# Subagent message count: 4

​
Stateless
Use this when you want to run a subagent like a plain function call with no checkpointing overhead. The subgraph cannot pause/resume and does not benefit from durable execution. Compile with checkpointer=False.
Without checkpointing, the subgraph has no durable execution. If the process crashes mid-run, the subgraph cannot recover and must be re-run from the beginning.
subgraph_builder = StateGraph(...)
subgraph = subgraph_builder.compile(checkpointer=False)

​
Checkpointer reference
Control subgraph persistence with the checkpointer parameter on .compile():
subgraph = builder.compile(checkpointer=False)  # or True / None

Feature	Per-invocation (default)	Per-thread	Stateless
checkpointer=	None	True	False
Interrupts (HITL)	✅	✅	❌
Multi-turn memory	❌	✅	❌
Multiple calls (different subgraphs)	✅	⚠️	✅
Multiple calls (same subgraph)	✅	❌	✅
State inspection	⚠️	✅	❌
Interrupts (HITL): The subgraph can use interrupt() to pause execution and wait for user input, then resume where it left off.
Multi-turn memory: The subgraph retains its state across multiple invocations within the same thread. Each call picks up where the last one left off rather than starting fresh.
Multiple calls (different subgraphs): Multiple different subgraph instances can be invoked within a single node without checkpoint namespace conflicts.
Multiple calls (same subgraph): The same subgraph instance can be invoked multiple times within a single node. With stateful persistence, these calls write to the same checkpoint namespace and conflict—use per-invocation persistence instead.
State inspection: The subgraph’s state is available via get_state(config, subgraphs=True) for debugging and monitoring.
​
View subgraph state
When you enable persistence, you can inspect the subgraph state using the subgraphs option. With stateless checkpointing (checkpointer=False), no subgraph checkpoints are saved, so subgraph state is not available.
Viewing subgraph state requires that LangGraph can statically discover the subgraph—i.e., it is added as a node or called inside a node. It does not work when a subgraph is called inside a tool function or other indirection (e.g., the subagents pattern). Interrupts still propagate to the top-level graph regardless of nesting.
Per-invocation
Per-thread
Returns subgraph state for the current invocation only. Each invocation starts fresh.
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import interrupt, Command
from typing_extensions import TypedDict

class State(TypedDict):
    foo: str

# Subgraph
def subgraph_node_1(state: State):
    value = interrupt("Provide value:")
    return {"foo": state["foo"] + value}

subgraph_builder = StateGraph(State)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph = subgraph_builder.compile()  # inherits parent checkpointer

# Parent graph
builder = StateGraph(State)
builder.add_node("node_1", subgraph)
builder.add_edge(START, "node_1")

checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}

graph.invoke({"foo": ""}, config)

# View subgraph state for the current invocation
subgraph_state = graph.get_state(config, subgraphs=True).tasks[0].state  

# Resume the subgraph
graph.invoke(Command(resume="bar"), config)

​
Stream subgraph outputs
To include outputs from subgraphs in the streamed outputs, you can set the subgraphs option in the stream method of the parent graph. This will stream outputs from both the parent graph and any subgraphs.
v2 (LangGraph >= 1.1)
v1 (default)
With version="v2", subgraph events use the same StreamPart format. The ns field identifies the source graph:
for chunk in graph.stream(
    {"foo": "foo"},
    subgraphs=True,
    stream_mode="updates",
    version="v2",
):
    print(chunk["type"])  # "updates"
    print(chunk["ns"])    # () for root, ("node_2:<task_id>",) for subgraph
    print(chunk["data"])  # {"node_name": {"key": "value"}}


Stream from subgraphs

Edit this page on GitHub or file an issue.
Connect these docs to Claude, VSCode, and more via MCP for real-time answers.