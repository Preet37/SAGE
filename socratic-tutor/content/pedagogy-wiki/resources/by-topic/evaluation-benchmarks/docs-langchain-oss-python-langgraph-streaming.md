# Source: https://docs.langchain.com/oss/python/langgraph/streaming
# Title: Streaming - Docs by LangChain
# Fetched via: browser
# Date: 2026-04-10

LangGraph implements a streaming system to surface real-time updates. Streaming is crucial for enhancing the responsiveness of applications built on LLMs. By displaying output progressively, even before a complete response is ready, streaming significantly improves user experience (UX), particularly when dealing with the latency of LLMs.
​
Get started
​
Basic usage
LangGraph graphs expose the stream (sync) and astream (async) methods to yield streamed outputs as iterators. Pass one or more stream modes to control what data you receive.
for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode=["updates", "custom"],
    version="v2",
):
    if chunk["type"] == "updates":
        for node_name, state in chunk["data"].items():
            print(f"Node {node_name} updated: {state}")
    elif chunk["type"] == "custom":
        print(f"Status: {chunk['data']['status']}")

Output
Status: thinking of a joke...
Node generate_joke updated: {'joke': 'Why did the ice cream go to school? To get a sundae education!'}


Full example

​
Stream output format (v2)
Requires LangGraph >= 1.1. All examples on this page use version="v2".
Pass version="v2" to stream() or astream() to get a unified output format. Every chunk is a StreamPart dict with a consistent shape — regardless of stream mode, number of modes, or subgraph settings:
{
    "type": "values" | "updates" | "messages" | "custom" | "checkpoints" | "tasks" | "debug",
    "ns": (),           # namespace tuple, populated for subgraph events
    "data": ...,        # the actual payload (type varies by stream mode)
}

Each stream mode has a corresponding TypedDict containing ValuesStreamPart, UpdatesStreamPart, MessagesStreamPart, CustomStreamPart, CheckpointStreamPart, TasksStreamPart, DebugStreamPart. You can import these types from langgraph.types. The union type StreamPart is a disjoing union on part["type"], enabling full type narrowing in editors and type checkers.
With v1 (default), the output format changes based on your streaming options (single mode returns raw data, multiple modes return (mode, data) tuples, subgraphs return (namespace, data) tuples). With v2, the format is always the same:
v2 (new)
v1 (current default)
for chunk in graph.stream(inputs, stream_mode="updates", version="v2"):
    print(chunk["type"])  # "updates"
    print(chunk["ns"])    # ()
    print(chunk["data"])  # {"node_name": {"key": "value"}}

The v2 format also enables type narrowing, which means you can filter chunks by chunk["type"] and get the correct payload type. Each branch narrows part["data"] to the specific type for that mode:
for part in graph.stream(
    {"topic": "ice cream"},
    stream_mode=["values", "updates", "messages", "custom"],
    version="v2",
):
    if part["type"] == "values":
        # ValuesStreamPart — full state snapshot after each step
        print(f"State: topic={part['data']['topic']}")
    elif part["type"] == "updates":
        # UpdatesStreamPart — only the changed keys from each node
        for node_name, state in part["data"].items():
            print(f"Node `{node_name}` updated: {state}")
    elif part["type"] == "messages":
        # MessagesStreamPart — (message_chunk, metadata) from LLM calls
        msg, metadata = part["data"]
        print(msg.content, end="", flush=True)
    elif part["type"] == "custom":
        # CustomStreamPart — arbitrary data from get_stream_writer()
        print(f"Progress: {part['data']['progress']}%")

​
Stream modes
Pass one or more of the following stream modes as a list to the stream or astream methods:
Mode	Type	Description
values	ValuesStreamPart	Full state after each step.
updates	UpdatesStreamPart	State updates after each step. Multiple updates in the same step are streamed separately.
messages	MessagesStreamPart	2-tuples of (LLM token, metadata) from LLM calls.
custom	CustomStreamPart	Custom data emitted from nodes via get_stream_writer.
checkpoints	CheckpointStreamPart	Checkpoint events (same format as get_state()). Requires a checkpointer.
tasks	TasksStreamPart	Task start/finish events with results and errors. Requires a checkpointer.
debug	DebugStreamPart	All available info — combines checkpoints and tasks with extra metadata.
​
Graph state
Use the stream modes updates and values to stream the state of the graph as it executes.
updates streams the updates to the state after each step of the graph.
values streams the full value of the state after each step of the graph.
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
  topic: str
  joke: str


def refine_topic(state: State):
    return {"topic": state["topic"] + " and cats"}


def generate_joke(state: State):
    return {"joke": f"This is a joke about {state['topic']}"}

graph = (
  StateGraph(State)
  .add_node(refine_topic)
  .add_node(generate_joke)
  .add_edge(START, "refine_topic")
  .add_edge("refine_topic", "generate_joke")
  .add_edge("generate_joke", END)
  .compile()
)

updates
values
Use this to stream only the state updates returned by the nodes after each step. The streamed outputs include the name of the node as well as the update.
for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode="updates",
    version="v2",
):
    if chunk["type"] == "updates":
        for node_name, state in chunk["data"].items():
            print(f"Node `{node_name}` updated: {state}")

Output
Node `refine_topic` updated: {'topic': 'ice cream and cats'}
Node `generate_joke` updated: {'joke': 'This is a joke about ice cream and cats'}

​
LLM tokens
Use the messages streaming mode to stream Large Language Model (LLM) outputs token by token from any part of your graph, including nodes, tools, subgraphs, or tasks.
The streamed output from messages mode is a tuple (message_chunk, metadata) where:
message_chunk: the token or message segment from the LLM.
metadata: a dictionary containing details about the graph node and LLM invocation.
If your LLM is not available as a LangChain integration, you can stream its outputs using custom mode instead. See use with any LLM for details.
Manual config required for async in Python < 3.11 When using Python < 3.11 with async code, you must explicitly pass RunnableConfig to ainvoke() to enable proper streaming. See Async with Python < 3.11 for details or upgrade to Python 3.11+.
from dataclasses import dataclass

from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START


@dataclass
class MyState:
    topic: str
    joke: str = ""


model = init_chat_model(model="gpt-4.1-mini")

def call_model(state: MyState):
    """Call the LLM to generate a joke about a topic"""
    # Note that message events are emitted even when the LLM is run using .invoke rather than .stream
    model_response = model.invoke(
        [
            {"role": "user", "content": f"Generate a joke about {state.topic}"}
        ]
    )
    return {"joke": model_response.content}

graph = (
    StateGraph(MyState)
    .add_node(call_model)
    .add_edge(START, "call_model")
    .compile()
)

# The "messages" stream mode streams LLM tokens with metadata
# Use version="v2" for a unified StreamPart format
for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        message_chunk, metadata = chunk["data"]
        if message_chunk.content:
            print(message_chunk.content, end="|", flush=True)

​
Filter by LLM invocation
You can associate tags with LLM invocations to filter the streamed tokens by LLM invocation.
from langchain.chat_models import init_chat_model

# model_1 is tagged with "joke"
model_1 = init_chat_model(model="gpt-4.1-mini", tags=['joke'])
# model_2 is tagged with "poem"
model_2 = init_chat_model(model="gpt-4.1-mini", tags=['poem'])

graph = ... # define a graph that uses these LLMs

# The stream_mode is set to "messages" to stream LLM tokens
# The metadata contains information about the LLM invocation, including the tags
async for chunk in graph.astream(
    {"topic": "cats"},
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        msg, metadata = chunk["data"]
        # Filter the streamed tokens by the tags field in the metadata to only include
        # the tokens from the LLM invocation with the "joke" tag
        if metadata["tags"] == ["joke"]:
            print(msg.content, end="|", flush=True)


Extended example: filtering by tags

​
Omit messages from the stream
Use the nostream tag to exclude LLM output from the stream entirely. Invocations tagged with nostream still run and produce output; their tokens are simply not emitted in messages mode.
This is useful when:
You need LLM output for internal processing (for example structured output) but do not want to stream it to the client
You stream the same content through a different channel (for example custom UI messages) and want to avoid duplicate output in the messages stream
from typing import Any, TypedDict

from langchain_anthropic import ChatAnthropic
from langgraph.graph import START, StateGraph

stream_model = ChatAnthropic(model_name="claude-3-haiku-20240307")
internal_model = ChatAnthropic(model_name="claude-3-haiku-20240307").with_config(
    {"tags": ["nostream"]}
)


class State(TypedDict):
    topic: str
    answer: str
    notes: str


def answer(state: State) -> dict[str, Any]:
    r = stream_model.invoke(
        [{"role": "user", "content": f"Reply briefly about {state['topic']}"}]
    )
    return {"answer": r.content}


def internal_notes(state: State) -> dict[str, Any]:
    # Tokens from this model are omitted from stream_mode="messages" because of nostream
    r = internal_model.invoke(
        [{"role": "user", "content": f"Private notes on {state['topic']}"}]
    )
    return {"notes": r.content}


graph = (
    StateGraph(State)
    .add_node("write_answer", answer)
    .add_node("internal_notes", internal_notes)
    .add_edge(START, "write_answer")
    .add_edge("write_answer", "internal_notes")
    .compile()
)

initial_state: State = {"topic": "AI", "answer": "", "notes": ""}
stream = graph.stream(initial_state, stream_mode="messages")

​
Filter by node
To stream tokens only from specific nodes, use stream_mode="messages" and filter the outputs by the langgraph_node field in the streamed metadata:
# The "messages" stream mode streams LLM tokens with metadata
# Use version="v2" for a unified StreamPart format
for chunk in graph.stream(
    inputs,
    stream_mode="messages",
    version="v2",
):
    if chunk["type"] == "messages":
        msg, metadata = chunk["data"]
        # Filter the streamed tokens by the langgraph_node field in the metadata
        # to only include the tokens from the specified node
        if msg.content and metadata["langgraph_node"] == "some_node_name":
            ...


Extended example: streaming LLM tokens from specific nodes

​
Custom data
To send custom user-defined data from inside a LangGraph node or tool, follow these steps:
Use get_stream_writer to access the stream writer and emit custom data.
Set stream_mode="custom" when calling .stream() or .astream() to get the custom data in the stream. You can combine multiple modes (e.g., ["updates", "custom"]), but at least one must be "custom".
No get_stream_writer in async for Python < 3.11 In async code running on Python < 3.11, get_stream_writer will not work. Instead, add a writer parameter to your node or tool and pass it manually. See Async with Python < 3.11 for usage examples.
node
tool
from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START

class State(TypedDict):
    query: str
    answer: str

def node(state: State):
    # Get the stream writer to send custom data
    writer = get_stream_writer()
    # Emit a custom key-value pair (e.g., progress update)
    writer({"custom_key": "Generating custom data inside node"})
    return {"answer": "some data"}

graph = (
    StateGraph(State)
    .add_node(node)
    .add_edge(START, "node")
    .compile()
)

inputs = {"query": "example"}

# Set stream_mode="custom" to receive the custom data in the stream
for chunk in graph.stream(inputs, stream_mode="custom", version="v2"):
    if chunk["type"] == "custom":
        print(f"Custom event: {chunk['data']['custom_key']}")

​
Subgraph outputs
To include outputs from subgraphs in the streamed outputs, you can set subgraphs=True in the .stream() method of the parent graph. This will stream outputs from both the parent graph and any subgraphs.
The outputs will be streamed as tuples (namespace, data), where namespace is a tuple with the path to the node where a subgraph is invoked, e.g. ("parent_node:<task_id>", "child_node:<task_id>").
v2 (LangGraph >= 1.1)
v1 (default)
With version="v2", subgraph events use the same StreamPart format. The ns field identifies the source:
for chunk in graph.stream(
    {"foo": "foo"},
    subgraphs=True,
    stream_mode="updates",
    version="v2",
):
    print(chunk["type"])  # "updates"
    print(chunk["ns"])    # () for root, ("node_name:<task_id>",) for subgraph
    print(chunk["data"])  # {"node_name": {"key": "value"}}


Extended example: streaming from subgraphs

​
Checkpoints
Use the checkpoints streaming mode to receive checkpoint events as the graph executes. Each checkpoint event has the same format as the output of get_state(). Requires a checkpointer.
from langgraph.checkpoint.memory import MemorySaver

graph = (
    StateGraph(State)
    .add_node(refine_topic)
    .add_node(generate_joke)
    .add_edge(START, "refine_topic")
    .add_edge("refine_topic", "generate_joke")
    .add_edge("generate_joke", END)
    .compile(checkpointer=MemorySaver())
)

config = {"configurable": {"thread_id": "1"}}

for chunk in graph.stream(
    {"topic": "ice cream"},
    config=config,
    stream_mode="checkpoints",
    version="v2",
):
    if chunk["type"] == "checkpoints":
        print(chunk["data"])

​
Tasks
Use the tasks streaming mode to receive task start and finish events as the graph executes. Task events include information about which node is running, its results, and any errors. Requires a checkpointer.
from langgraph.checkpoint.memory import MemorySaver

graph = (
    StateGraph(State)
    .add_node(refine_topic)
    .add_node(generate_joke)
    .add_edge(START, "refine_topic")
    .add_edge("refine_topic", "generate_joke")
    .add_edge("generate_joke", END)
    .compile(checkpointer=MemorySaver())
)

config = {"configurable": {"thread_id": "1"}}

for chunk in graph.stream(
    {"topic": "ice cream"},
    config=config,
    stream_mode="tasks",
    version="v2",
):
    if chunk["type"] == "tasks":
        print(chunk["data"])

​
Debug
Use the debug streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.
for chunk in graph.stream(
    {"topic": "ice cream"},
    stream_mode="debug",
    version="v2",
):
    if chunk["type"] == "debug":
        print(chunk["data"])

The debug mode combines checkpoints and tasks events with additional metadata. Use checkpoints or tasks directly if you only need a subset of the debug information.
​
Multiple modes at once
You can pass a list as the stream_mode parameter to stream multiple modes at once.
With version="v2", every chunk is a StreamPart dict. Use chunk["type"] to distinguish between modes:
v2
v1
for chunk in graph.stream(inputs, stream_mode=["updates", "custom"], version="v2"):
    if chunk["type"] == "updates":
        for node_name, state in chunk["data"].items():
            print(f"Node `{node_name}` updated: {state}")
    elif chunk["type"] == "custom":
        print(f"Custom event: {chunk['data']}")

​
Advanced
​
Use with any LLM
You can use stream_mode="custom" to stream data from any LLM API—even if that API does not implement the LangChain chat model interface.
This lets you integrate raw LLM clients or external services that provide their own streaming interfaces, making LangGraph highly flexible for custom setups.
from langgraph.config import get_stream_writer

def call_arbitrary_model(state):
    """Example node that calls an arbitrary model and streams the output"""
    # Get the stream writer to send custom data
    writer = get_stream_writer()
    # Assume you have a streaming client that yields chunks
    # Generate LLM tokens using your custom streaming client
    for chunk in your_custom_streaming_client(state["topic"]):
        # Use the writer to send custom data to the stream
        writer({"custom_llm_chunk": chunk})
    return {"result": "completed"}

graph = (
    StateGraph(State)
    .add_node(call_arbitrary_model)
    # Add other nodes and edges as needed
    .compile()
)
# Set stream_mode="custom" to receive the custom data in the stream
for chunk in graph.stream(
    {"topic": "cats"},
    stream_mode="custom",
    version="v2",
):
    if chunk["type"] == "custom":
        # The chunk data will contain the custom data streamed from the llm
        print(chunk["data"])


Extended example: streaming arbitrary chat model

​
Disable streaming for specific chat models
If your application mixes models that support streaming with those that do not, you may need to explicitly disable streaming for models that do not support it.
Set streaming=False when initializing the model.
init_chat_model
Chat model interface
from langchain.chat_models import init_chat_model

model = init_chat_model(
    "claude-sonnet-4-6",
    # Set streaming=False to disable streaming for the chat model
    streaming=False
)

Not all chat model integrations support the streaming parameter. If your model doesn’t support it, use disable_streaming=True instead. This parameter is available on all chat models via the base class.
​
Migrate to v2
The v2 streaming format (used throughout this page) provides a unified output format. Here’s a summary of the key differences and how to migrate:
Scenario	v1 (default)	v2 (version="v2")
Single stream mode	Raw data (dict)	StreamPart dict with type, ns, data
Multiple stream modes	(mode, data) tuples	Same StreamPart dict, filter on chunk["type"]
Subgraph streaming	(namespace, data) tuples	Same StreamPart dict, check chunk["ns"]
Multiple modes + subgraphs	(namespace, mode, data) triples	Same StreamPart dict
invoke() return type	Plain dict (state)	GraphOutput with .value and .interrupts
Interrupt location (stream)	__interrupt__ key in state dict	interrupts field on values stream parts
Interrupt location (invoke)	__interrupt__ key in result dict	.interrupts attribute on GraphOutput
Pydantic/dataclass output	Returns plain dict	Coerces to model/dataclass instance
​
v2 invoke format
When you pass version="v2" to invoke() or ainvoke(), it returns a GraphOutput object with .value and .interrupts attributes:
from langgraph.types import GraphOutput

result = graph.invoke(inputs, version="v2")

assert isinstance(result, GraphOutput)
result.value       # your output — dict, Pydantic model, or dataclass
result.interrupts  # tuple[Interrupt, ...], empty if none occurred

With any stream mode other than the default "values", invoke(..., stream_mode="updates", version="v2") returns list[StreamPart] instead of list[tuple].
Dict-style access on GraphOutput (result["key"], "key" in result, result["__interrupt__"]) still works for backwards compatibility but is deprecated and will be removed in a future version. Migrate to result.value and result.interrupts.
This separates state from interrupt metadata. With v1, interrupts are embedded in the returned dict under __interrupt__:
v2 (new)
v1 (current default)
config = {"configurable": {"thread_id": "thread-1"}}
result = graph.invoke(inputs, config=config, version="v2")

if result.interrupts:
    print(result.interrupts[0].value)
    graph.invoke(Command(resume=True), config=config, version="v2")

​
Pydantic and dataclass state coercion
When your graph state is a Pydantic model or dataclass, v2 values mode automatically coerces output to the correct type:
from pydantic import BaseModel
from typing import Annotated
import operator

class MyState(BaseModel):
    value: str
    items: Annotated[list[str], operator.add]

# With version="v2", chunk["data"] is a MyState instance
for chunk in graph.stream(
    {"value": "x", "items": []}, stream_mode="values", version="v2"
):
    print(type(chunk["data"]))  # <class 'MyState'>

​
Async with Python < 3.11
In Python versions < 3.11, asyncio tasks do not support the context parameter. This limits LangGraph ability to automatically propagate context, and affects LangGraph’s streaming mechanisms in two key ways:
You must explicitly pass RunnableConfig into async LLM calls (e.g., ainvoke()), as callbacks are not automatically propagated.
You cannot use get_stream_writer in async nodes or tools—you must pass a writer argument directly.

Extended example: async LLM call with manual config

Extended example: async custom streaming with stream writer

Edit this page on GitHub or file an issue.
Connect these docs to Claude, VSCode, and more via MCP for real-time answers.