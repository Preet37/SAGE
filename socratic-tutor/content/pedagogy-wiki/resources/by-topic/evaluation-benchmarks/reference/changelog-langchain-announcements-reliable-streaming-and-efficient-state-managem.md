# Source: https://changelog.langchain.com/announcements/reliable-streaming-and-efficient-state-management-in-langgraph
# Title: Reliable streaming and efficient state management in LangGraph
# Fetched via: search
# Date: 2026-04-10

LangGraph implements a streaming system to surface real-time updates. Streaming is crucial for enhancing the responsiveness of applications built on LLMs. By displaying output progressively, even before a complete response is ready, streaming significantly improves user experience (UX), particularly when dealing with the latency of LLMs.

## ​ Get started

### ​ Basic usage
LangGraph graphs expose the `stream` (sync) and `astream` (async) methods to yield streamed outputs as iterators. Pass one or more stream modes to control what data you receive.
```
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

```

…

```
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.config import get_stream_writer

class State(TypedDict):
 topic: str
 joke: str

def generate_joke(state: State):
 writer = get_stream_writer()
 writer({"status": "thinking of a joke..."})
 return {"joke": f"Why did the {state['topic']} go to school? To get a sundae education!"}

graph = (
 StateGraph(State)
 .add_node(generate_joke)
 .add_edge(START, "generate_joke")
 .add_edge("generate_joke", END)
 .compile()
)

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

```

…

```
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

```

## ​ Stream modes
Pass one or more of the following stream modes as a list to the `stream` or `astream` methods: |Mode|Type|Description|
|--|--|--|
|values|`ValuesStreamPart`|Full state after each step.|
|updates|`UpdatesStreamPart`|State updates after each step.
Multiple updates in the same step are streamed separately.|
|messages|`MessagesStreamPart`|2-tuples of (LLM token, metadata) from LLM calls.|
|custom|`CustomStreamPart`|Custom data emitted from nodes via `get_stream_writer`.|
|checkpoints|`CheckpointStreamPart`|Checkpoint events (same format as `get_state()`).

…

### ​ Graph state
Use the stream modes `updates` and `values` to stream the state of the graph as it executes. - `updates` streams the **updates** to the state after each step of the graph.
- `values` streams the **full value** of the state after each step of the graph.
```
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

```
- updates
- values
Use this to stream only the **state updates** returned by the nodes after each step. The streamed outputs include the name of the node as well as the update.
```
for chunk in graph.stream(
 {"topic": "ice cream"},
 stream_mode="updates",
 version="v2",
):
 if chunk["type"] == "updates":
 for node_name, state in chunk["data"].items():
 print(f"Node `{node_name}` updated: {state}")

```

…

```
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

```

…

```
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

```

…

```
from typing import TypedDict
from langgraph.graph import START, StateGraph
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4.1-mini")

class State(TypedDict):
 topic: str
 joke: str
 poem: str

def write_joke(state: State):
 topic = state["topic"]
 joke_response = model.invoke(
 [{"role": "user", "content": f"Write a joke about {topic}"}]
 )
 return {"joke": joke_response.content}

def write_poem(state: State):
 topic = state["topic"]
 poem_response = model.invoke(
 [{"role": "user", "content": f"Write a short poem about {topic}"}]
 )
 return {"poem": poem_response.content}

graph = (
 StateGraph(State)
 .add_node(write_joke)
 .add_node(write_poem)
 # write both the joke and the poem concurrently
 .add_edge(START, "write_joke")
 .add_edge(START, "write_poem")
 .compile()
)

# The "messages" stream mode streams LLM tokens with metadata
# Use version="v2" for a unified StreamPart format
for chunk in graph.stream(
 {"topic": "cats"},
 stream_mode="messages",
 version="v2",
):
 if chunk["type"] == "messages":
 msg, metadata = chunk["data"]
 # Filter the streamed tokens by the langgraph_node field in the metadata
 # to only include the tokens from the write_poem node
 if msg.content and metadata["langgraph_node"] == "write_poem":
 print(msg.content, end="|", flush=True)

```

### ​ Custom data
To send **custom user-defined data** from inside a LangGraph node or tool, follow these steps: 1. Use `get_stream_writer` to access the stream writer and emit custom data.
2. Set `stream_mode="custom"` when calling `.stream()` or `.astream()` to get the custom data in the stream. You can combine multiple modes (e.g., `["updates", "custom"]`), but at least one must be `"custom"`.

…

```
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

```

…

```
from langgraph.graph import START, StateGraph
from typing import TypedDict

# Define subgraph
class SubgraphState(TypedDict):
 foo: str # note that this key is shared with the parent graph state
 bar: str

def subgraph_node_1(state: SubgraphState):
 return {"bar": "bar"}

def subgraph_node_2(state: SubgraphState):
 return {"foo": state["foo"] + state["bar"]}

subgraph_builder = StateGraph(SubgraphState)
subgraph_builder.add_node(subgraph_node_1)
subgraph_builder.add_node(subgraph_node_2)
subgraph_builder.add_edge(START, "subgraph_node_1")
subgraph_builder.add_edge("subgraph_node_1", "subgraph_node_2")
subgraph = subgraph_builder.compile()

# Define parent graph
class ParentState(TypedDict):
 foo: str

def node_1(state: ParentState):
 return {"foo": "hi! " + state["foo"]}

builder = StateGraph(ParentState)
builder.add_node("node_1", node_1)
builder.add_node("node_2", subgraph)
builder.add_edge(START, "node_1")
builder.add_edge("node_1", "node_2")
graph = builder.compile()

for chunk in graph.stream(
 {"foo": "foo"},
 stream_mode="updates",
 # Set subgraphs=True to stream outputs from subgraphs
 subgraphs=True,
 version="v2",
):
 if chunk["type"] == "updates":
 if chunk["ns"]:
 print(f"Subgraph {chunk['ns']}: {chunk['data']}")
 else:
 print(f"Root: {chunk['data']}")

```

…

### ​ Checkpoints
Use the `checkpoints` streaming mode to receive checkpoint events as the graph executes. Each checkpoint event has the same format as the output of `get_state()`. Requires a checkpointer.
```
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

```

### ​ Tasks
Use the `tasks` streaming mode to receive task start and finish events as the graph executes. Task events include information about which node is running, its results, and any errors. Requires a checkpointer.

…

### ​ Debug
Use the `debug` streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.

…

```
for chunk in graph.stream(inputs, stream_mode=["updates", "custom"], version="v2"):
 if chunk["type"] == "updates":
 for node_name, state in chunk["data"].items():
 print(f"Node `{node_name}` updated: {state}")
 elif chunk["type"] == "custom":
 print(f"Custom event: {chunk['data']}")

```

…

```
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

```

…

```
import operator
import json

from typing import TypedDict
from typing_extensions import Annotated
from langgraph.graph import StateGraph, START

from openai import AsyncOpenAI

openai_client = AsyncOpenAI()
model_name = "gpt-4.1-mini"

async def stream_tokens(model_name: str, messages: list[dict]):
 response = await openai_client.chat.completions.create(
 messages=messages, model=model_name, stream=True
 )
 role = None
 async for chunk in response:
 delta = chunk.choices[0].delta

 if delta.role is not None:
 role = delta.role

 if delta.content:
 yield {"role": role, "content": delta.content}

# this is our tool
async def get_items(place: str) -> str:
 """Use this tool to list items one might find in a place you're asked about."""
 writer = get_stream_writer()
 response = ""
 async for msg_chunk in stream_tokens(
 model_name,
 [
 {
 "role": "user",
 "content": (
 "Can you tell me what kind of items "
 f"i might find in the following place: '{place}'. "
 "List at least 3 such items separating them by a comma. "
 "And include a brief description of each item."
 ),
 }
 ],
 ):
 response += msg_chunk["content"]
 writer(msg_chunk)

 return response

class State(TypedDict):
 messages: Annotated[list[dict], operator.add]

# this is the tool-calling graph node
async def call_tool(state: State):
 ai_message = state["messages"][-1]
 tool_call = ai_message["tool_calls"][-1]

 function_name = tool_call["function"]["name"]
 if function_name != "get_items":
 raise ValueError(f"Tool {function_name} not supported")

 function_arguments = tool_call["function"]["arguments"]
 arguments = json.loads(function_arguments)

 function_response = await get_items(**arguments)
 tool_message = {
 "tool_call_id": tool_call["id"],
 "role": "tool",
 "name": function_name,
 "content": function_response,
 }
 return {"messages": [tool_message]}

graph = (
 StateGraph(State)
 .add_node(call_tool)
 .add_edge(START, "call_tool")
 .compile()
)

```

…

```
from typing import TypedDict
from langgraph.graph import START, StateGraph
from langchain.chat_models import init_chat_model

model = init_chat_model(model="gpt-4.1-mini")

class State(TypedDict):
 topic: str
 joke: str

# Accept config as an argument in the async node function
async def call_model(state, config):
 topic = state["topic"]
 print("Generating joke...")
 # Pass config to model.ainvoke() to ensure proper context propagation
 joke_response = await model.ainvoke(
 [{"role": "user", "content": f"Write a joke about {topic}"}],
 config,
 )
 return {"joke": joke_response.content}

graph = (
 StateGraph(State)
 .add_node(call_model)
 .add_edge(START, "call_model")
 .compile()
)

# Set stream_mode="messages" to stream LLM tokens
async for chunk in graph.astream(
 {"topic": "ice cream"},
 stream_mode="messages",
 version="v2",
):
 if chunk["type"] == "messages":
 message_chunk, metadata = chunk["data"]
 if message_chunk.content:
 print(message_chunk.content, end="|", flush=True)

```

…

```
from typing import TypedDict
from langgraph.types import StreamWriter

class State(TypedDict):
 topic: str
 joke: str

# Add writer as an argument in the function signature of the async node or tool
# LangGraph will automatically pass the stream writer to the function
async def generate_joke(state: State, writer: StreamWriter):
 writer({"custom_key": "Streaming custom data while generating a joke"})
 return {"joke": f"This is a joke about {state['topic']}"}

graph = (
 StateGraph(State)
 .add_node(generate_joke)
 .add_edge(START, "generate_joke")
 .compile()
)

# Set stream_mode="custom" to receive the custom data in the stream #
async for chunk in graph.astream(
 {"topic": "ice cream"},
 stream_mode="custom",
 version="v2",
):
 if chunk["type"] == "custom":
 print(chunk["data"])

```

# 🤖 Reliable streaming and efficient state management in LangGraph
**DATE:**
**AUTHOR:** The LangChain Team
We're excited to roll out several key updates that enhance the LangGraph API/Cloud experience.
These includeL
1. **Streaming runs are now powered by the job queue used for background runs.**
This ensures greater reliability for your streaming runs without losing low-latency, real-time output.
Whether you're streaming chat messages token-by-token or running other processes, you'll experience consistent performance.
2. **New Streaming Endpoint & SDK Method**:
We've introduced the GET
```
/threads/{thread_id}/runs/{run_id}/stream
```
endpoint and the
```
client.runs.join_stream()
```
SDK method.
This enables real-time streaming output from any run, including background runs.
With this, you can create new UXs, such as a chatbot that continues streaming even when users navigate away and return to the page.
3. **Enhanced Final State Retrieval**:
The updated GET
```
/threads/{thread_id}/runs/{run_id}/join
```
endpoint and
```
client.runs.join()
```
SDK method now reliably return the final state values after a run completes, ensuring consistent results whether the run is ongoing or finished—essential for workflows requiring dependable state retrieval.
4. **Expanded Thread Status Values**:
The GET
```
/threads/{id}
```
and
```
client.threads.get()
```
now support two new status values:
```
error
```
and
```
interrupted
```
.
 These status indicators help you manage and troubleshoot your threads by knowing when something goes wrong or a process is interrupted.
The existing
```
idle
```
and
```
busy
```
statuses are still supported.
5. **Streamlined State Retrieval**:
Endpoints GET
```
/threads/{id}
```
and GET
```
/threads
```
now include the latest state values of each thread.
This removes the need for separate "get state" calls, reducing the number of API requests needed to retrieve thread states.
6. **Advanced Thread Search**:
The POST
```
/threads/search
```
and
```
client.threads.search
```
```
()
```
can now be filtered by thread state values.
Combined with status filtering, this filtering allows you to build highly specific UIs - such as agent inboxes - where you can easily list threads in precise states.
These updates collectively enhance the reliability, efficiency, and flexibility of LangGraph, enabling you to build more robust and user-friendly applications.

# How to stream full state of your graph¶
LangGraph supports multiple streaming modes.
The main ones are:
`values`: This streaming mode streams back values of the graph.
This is the
**full state of the graph**after each node is called.
`updates`: This streaming mode streams back updates to the graph.
This is the
**update to the state of the graph**after each node is called.
This guide covers
`streamMode="values"`.
```
// process.env.OPENAI_API_KEY = "sk-...";
```
## Define the state¶
The state is the interface for all of the nodes in our graph.
```
import { Annotation } from "@langchain/langgraph";
import { BaseMessage } from "@langchain/core/messages";
const StateAnnotation = Annotation.Root({
messages: Annotation<BaseMessage[]>({
reducer: (x, y) => x.concat(y),
}),
});
```
## Set up the tools¶
We will first define the tools we want to use.
For this simple example, we will use create a placeholder search engine.
However, it is really easy to create your own tools - see documentation here on how to do that.
```
import { tool } from "@langchain/core/tools";
import { z } from "zod";
const searchTool = tool(async ({ query: _query }: { query: string }) => {
// This is a placeholder for the actual implementation
return "Cold, with a low of 3℃";
}, {
name: "search",
description:
"Use to surf the web, fetch current information, check the weather, and retrieve other information.",
schema: z.object({
query: z.string().describe("The query to use in your search."),
}),
});
await searchTool.invoke({ query: "What's the weather like?" });
const tools = [searchTool];
```
We can now wrap these tools in a simple ToolNode.
This object will actually run the tools (functions) whenever they are invoked by our LLM.
```
import { ToolNode } from "@langchain/langgraph/prebuilt";
const toolNode = new ToolNode(tools);
```
## Set up the model¶
Now we will load the chat model.
- It should work with messages.
We will represent all agent state in the form of messages, so it needs to be able to work well with them.
- It should work with tool calling, meaning it can return function arguments in its response.
Note
These model requirements are not general requirements for using LangGraph - they are just requirements for this one example.
```
import { ChatOpenAI } from "@langchain/openai";
const model = new ChatOpenAI({ model: "gpt-4o" });
```
After we've done this, we should make sure the model knows that it has these tools available to call.
We can do this by calling bindTools.
```
const boundModel = model.bindTools(tools);
```
## Define the graph¶
We can now put it all together.
```
import { END, START, StateGraph } from "@langchain/langgraph";
import { AIMessage } from "@langchain/core/messages";
const routeMessage = (state: typeof StateAnnotation.State) => {
const { messages } = state;
const lastMessage = messages[messages.length - 1] as AIMessage;
// If no tools are called, we can finish (respond to the user)
if (!lastMessage?.tool_calls?.length) {
return END;
// Otherwise if there is, we continue and call the tools
return "tools";
};
const callModel = async (
state: typeof StateAnnotation.State,
) => {
// For versions of @langchain/core < 0.2.3, you must call `.stream()`
// and aggregate the message from chunks instead of calling `.invoke()`.
const { messages } = state;
const responseMessage = await boundModel.invoke(messages);
return { messages: [responseMessage] };
};
const workflow = new StateGraph(StateAnnotation)
.addNode("agent", callModel)
.addNode("tools", toolNode)
.addEdge(START, "agent")
.addConditionalEdges("agent", routeMessage)
.addEdge("tools", "agent");
const graph = workflow.compile();
```
## Stream values¶
We can now interact with the agent.
Between interactions you can get and update state.
```
let inputs = { messages: [{ role: "user", content: "what's the weather in sf" }] };
for await (
const chunk of await graph.stream(inputs, {
streamMode: "values",
})
) {
console.log(chunk["messages"]);
console.log("\n====\n");
```
```
[ [ 'user', "what's the weather in sf" ] ]
====
[ 'user', "what's the weather in sf" ],

# How to stream state updates of your graph¶
LangGraph supports multiple streaming modes.
The main ones are:
`values`: This streaming mode streams back values of the graph.
This is the
**full state of the graph**after each node is called.
`updates`: This streaming mode streams back updates to the graph.
This is the
**update to the state of the graph**after each node is called.
This guide covers
`streamMode="updates"`.
```
// process.env.OPENAI_API_KEY = "sk-...";
```
## Define the state¶
The state is the interface for all of the nodes in our graph.
```
import { Annotation } from "@langchain/langgraph";
import { BaseMessage } from "@langchain/core/messages";
const StateAnnotation = Annotation.Root({
messages: Annotation<BaseMessage[]>({
reducer: (x, y) => x.concat(y),
}),
});
```
## Set up the tools¶
We will first define the tools we want to use.
For this simple example, we will use create a placeholder search engine.
However, it is really easy to create your own tools - see documentation here on how to do that.
```
import { tool } from "@langchain/core/tools";
import { z } from "zod";
const searchTool = tool(async ({ query: _query }: { query: string }) => {
// This is a placeholder for the actual implementation
return "Cold, with a low of 3℃";
}, {
name: "search",
description:
"Use to surf the web, fetch current information, check the weather, and retrieve other information.",
schema: z.object({
query: z.string().describe("The query to use in your search."),
}),
});
await searchTool.invoke({ query: "What's the weather like?" });
const tools = [searchTool];
```
We can now wrap these tools in a simple ToolNode.
This object will actually run the tools (functions) whenever they are invoked by our LLM.
```
import { ToolNode } from "@langchain/langgraph/prebuilt";
const toolNode = new ToolNode(tools);
```
## Set up the model¶
Now we will load the chat model.
- It should work with messages.
We will represent all agent state in the form of messages, so it needs to be able to work well with them.
- It should work with tool calling, meaning it can return function arguments in its response.
Note
These model requirements are not general requirements for using LangGraph - they are just requirements for this one example.
```
import { ChatOpenAI } from "@langchain/openai";
const model = new ChatOpenAI({ model: "gpt-4o" });
```
After we've done this, we should make sure the model knows that it has these tools available to call.
We can do this by calling bindTools.
```
const boundModel = model.bindTools(tools);
```
## Define the graph¶
We can now put it all together.
```
import { END, START, StateGraph } from "@langchain/langgraph";
import { AIMessage } from "@langchain/core/messages";
const routeMessage = (state: typeof StateAnnotation.State) => {
const { messages } = state;
const lastMessage = messages[messages.length - 1] as AIMessage;
// If no tools are called, we can finish (respond to the user)
if (!lastMessage?.tool_calls?.length) {
return END;
// Otherwise if there is, we continue and call the tools
return "tools";
};
const callModel = async (
state: typeof StateAnnotation.State,
) => {
const { messages } = state;
const responseMessage = await boundModel.invoke(messages);
return { messages: [responseMessage] };
};
const workflow = new StateGraph(StateAnnotation)
.addNode("agent", callModel)
.addNode("tools", toolNode)
.addEdge(START, "agent")
.addConditionalEdges("agent", routeMessage)
.addEdge("tools", "agent");
const graph = workflow.compile();
```
## Stream updates¶
We can now interact with the agent.
```
let inputs = { messages: [{ role: "user", content: "what's the weather in sf" }] };
for await (
const chunk of await graph.stream(inputs, {
streamMode: "updates",
})
) {
for (const [node, values] of Object.entries(chunk)) {
console.log(`Receiving update from node: ${node}`);
console.log(values);
console.log("\n====\n");
```
```
Receiving update from node: agent
messages: [
AIMessage {
"id": "chatcmpl-9y654VypbD3kE1xM8v4xaAHzZEOXa",
"content": "",
"additional_kwargs": {
"tool_calls": [
"id": "call_OxlOhnROermwae2LPs9SanmD",
"type": "function",
"function": "[Object]"
...
"response_metadata": {
"tokenUsage": {
...
Receiving update from node: agent

**Alpha Notice:**These docs cover the

**v1-alpha**release. Content is incomplete and subject to change.For the latest stable version, see the current LangGraph Python or LangGraph JavaScript docs.

## OverviewLangGraph implements a streaming system to surface real-time updates. This is essential for applications that use LLMs due to the inherent latency involved in model calls. Streaming allows for a more responsive user experience.

## What’s possible with LangGraph streaming

**Stream graph state**— get state updates / values with

`updates`and

`values`modes.

**Stream subgraph outputs**— include outputs from both the parent graph and any nested subgraphs. **Stream LLM tokens**— capture token streams from anywhere: inside nodes, subgraphs, or tools. **Stream custom data**— send custom updates or progress signals directly from tool functions. **Use multiple streaming modes**— choose from

…

|Mode|Description|
|--|--|
|`values`|Streams the full value of the state after each step of the graph.|
|`updates`|Streams the updates to the state after each step of the graph. If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately.|
|`custom`|Streams custom data from inside your graph nodes.|
|`messages`|Streams 2-tuples (LLM token, metadata) from any graph nodes where an LLM is invoked.|
|`debug`|Streams as much information as possible throughout the execution of the graph.|

## Basic usage exampleLangGraph graphs expose the

`.stream()` method to yield streamed outputs as iterators.

```

for await (const chunk of await graph.stream(inputs, {

streamMode: "updates",

})) {

console.log(chunk);



```

Extended example: streaming updates

Extended example: streaming updates
```
import { StateGraph, START, END } from "@langchain/langgraph";

import { z } from "zod/v4";

const State = z.object({

topic: z.string(),

joke: z.string(),

});

const graph = new StateGraph(State)

.addNode("refineTopic", (state) => {

…

## Stream multiple modesYou can pass an array as the

`streamMode` parameter to stream multiple modes at once.

The streamed outputs will be tuples of

`[mode, chunk]` where

`mode` is the name of the stream mode and

`chunk` is the data streamed by that mode.

```

for await (const [mode, chunk] of await graph.stream(inputs, {

streamMode: ["updates", "custom"],

})) {

console.log(chunk);



```

## Stream graph stateUse the stream modes

`updates` and

`values` to stream the state of the graph as it executes.

`updates`streams the

**updates**to the state after each step of the graph.

`values`streams the

**full value**of the state after each step of the graph.
```
import { StateGraph, START, END } from "@langchain/langgraph";

import { z } from "zod/v4";

const State = z.object({

topic: z.string(),

joke: z.string(),

});

const graph = new StateGraph(State)

.addNode("refineTopic", (state) => {

…

Use this to stream only the

**state updates**returned by the nodes after each step. The streamed outputs include the name of the node as well as the update.

```

for await (const chunk of await graph.stream(

{ topic: "ice cream" },

{ streamMode: "updates" }

)) {

console.log(chunk);



```

…

```
import { StateGraph, START } from "@langchain/langgraph";

import { z } from "zod/v4";

// Define subgraph

const SubgraphState = z.object({

foo: z.string(), // note that this key is shared with the parent graph state

bar: z.string(),

});

const subgraphBuilder = new StateGraph(SubgraphState)

…

**Note**that we are receiving not just the node updates, but we also the namespaces which tell us what graph (or subgraph) we are streaming from.

### DebuggingUse the

`debug` streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.

```

for await (const chunk of await graph.stream(

{ topic: "ice cream" },

{ streamMode: "debug" }

)) {

console.log(chunk);



```

…

};

const graph = new StateGraph(MyState)

.addNode("callModel", callModel)

.addEdge(START, "callModel")

.compile();

for await (const [messageChunk, metadata] of await graph.stream(

// (2)!

{ topic: "ice cream" },

{ streamMode: "messages" }

)) {

if (messageChunk.content) {

console.log(messageChunk.content + "|");



```

…

```
import { StateGraph, START, LangGraphRunnableConfig } from "@langchain/langgraph";

import { z } from "zod/v4";

const State = z.object({

query: z.string(),

answer: z.string(),

});

const graph = new StateGraph(State)

.addNode("node", async (state, config) => {

…

## Use with any LLMYou can use

`streamMode: "custom"` to stream data from

**any LLM API**— even if that API does

**not**implement the LangChain chat model interface. This lets you integrate raw LLM clients or external services that provide their own streaming interfaces, making LangGraph highly flexible for custom setups.

```

import { LangGraphRunnableConfig } from "@langchain/langgraph";

const callArbitraryModel = async (

state: any,

config: LangGraphRunnableConfig

) => {

// Example node that calls an arbitrary model and streams the output

// Assume you have a streaming client that yields chunks

for await (const chunk of yourCustomStreamingClient(state.topic)) {

// (1)!

config.writer({ custom_llm_chunk: chunk }); // (2)!



return { result: "completed" };

};

const graph = new StateGraph(State)

.addNode("callArbitraryModel", callArbitraryModel)

// Add other nodes and edges as needed

.compile();

for await (const chunk of await graph.stream(

{ topic: "cats" },

{ streamMode: "custom" } // (3)!

)) {

// The chunk will contain the custom data streamed from the llm

console.log(chunk);



```

- Generate LLM tokens using your custom streaming client.

- Use the writer to send custom data to the stream.

- Set

`streamMode: "custom"`to receive the custom data in the stream.

Extended example: streaming arbitrary chat model

Extended example: streaming arbitrary chat model

Let’s invoke the graph with an AI message that includes a tool call:

```

import { StateGraph, START, MessagesZodMeta, LangGraphRunnableConfig } from "@langchain/langgraph";

import { BaseMessage } from "@langchain/core/messages";

import { registry } from "@langchain/langgraph/zod";

import { z } from "zod/v4";

import OpenAI from "openai";

const openaiClient = new OpenAI();

const modelName = "gpt-4o-mini";

async function* streamTokens(modelName: string, messages: any[]) {

const response = await openaiClient.chat.completions.create({

messages,

model: modelName,

stream: true,

});

let role: string | null = null;

for await (const chunk of response) {

const delta = chunk.choices[0]?.delta;

if (delta?.role) {

role = delta.role;



if (delta?.content) {

yield { role, content: delta.content };



// this is our tool

const getItems = tool(

async (input, config: LangGraphRunnableConfig) => {

let response = "";

for await (const msgChunk of streamTokens(

modelName,



role: "user",

content: `Can you tell me what kind of items i might find in the following place: '${input.place}'. List at least 3 such items separating them by a comma. And include a brief description of each item.`,

},



)) {

response += msgChunk.content;

config.writer?.(msgChunk);



return response;

},



name: "get_items",

description: "Use this tool to list items one might find in a place you're asked about.",

schema: z.object({

place: z.string().describe("The place to look up items for."),

}),



);

const State = z.object({

messages: z

.array(z.custom<BaseMessage>())

.register(registry, MessagesZodMeta),

});

const graph = new StateGraph(State)

// this is the tool-calling graph node

.addNode("callTool", async (state) => {

const aiMessage = state.messages.at(-1);

const toolCall = aiMessage.tool_calls?.at(-1);

const functionName = toolCall?.function?.name;

if (functionName !== "get_items") {

throw new Error(`Tool ${functionName} not supported`);



const functionArguments = toolCall?.function?.arguments;

const args = JSON.parse(functionArguments);

const functionResponse = await getItems.invoke(args);

const toolMessage = {

tool_call_id: toolCall.id,

role: "tool",

name: functionName,

content: functionResponse,

};

return { messages: [toolMessage] };

})

.addEdge(START, "callTool")

.compile();

```

```

const inputs = {

messages: [



content: null,

role: "assistant",

tool_calls: [



id: "1",

function: {

arguments: '{"place":"bedroom"}',

name: "get_items",

},

type: "function",



],



};

for await (const chunk of await graph.stream(

inputs,

{ streamMode: "custom" }

)) {

console.log(chunk.content + "|");



```

## Disable streaming for specific chat modelsIf your application mixes models that support streaming with those that do not, you may need to explicitly disable streaming for models that do not support it. Set

`streaming: false` when initializing the model.

```

import { ChatOpenAI } from "@langchain/openai";

const model = new ChatOpenAI({

model: "o1-preview",

streaming: false, // (1)!

});

```