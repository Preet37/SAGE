# Source: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/streamMode
# Title: streamMode | @langchain/langgraph (CompiledStateGraph.streamMode)
# Fetched via: search
# Date: 2026-04-10

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
Use the stream modes `updates` and `values` to stream the state of the graph as it executes.
- `updates` streams the **updates** to the state after each step of the graph.
- `values` streams the **full value** of the state after each step of the graph.
…
- updates
- values
Use this to stream only the **state updates** returned by the nodes after each step.
The streamed outputs include the name of the node as well as the update.
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
from typing import TypedDict
...
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
...
# Set stream_mode="custom" to receive the custom data in the stream
for chunk in graph.stream(inputs, stream_mode="custom", version="v2"):
if chunk["type"] == "custom":
print(f"Custom event: {chunk['data']['custom_key']}")
```
…
```
...
# Set subgraphs=True to stream outputs from subgraphs
subgraphs=True,
version="v2",
):
if chunk["type"] == "updates":
if chunk["ns"]:
print(f"Subgraph {chunk['ns']}: {chunk['data']}")
...
print(f"Root: {chunk['data']}")
...
for chunk in graph.stream(inputs, stream_mode=["updates", "custom"], version="v2"):
...
for node_name, state in chunk["data"].items():
print(f"Node `{node_name}` updated: {state}")
elif chunk["type"] == "custom":
print(f"Custom event: {chunk['data']}")

## ​ Stream modes
Pass one or more of the following stream modes as a list to the `stream` method: |Mode|Description|
|--|--|
|values|Full state after each step.|
|updates|State updates after each step. Multiple updates in the same step are streamed separately.|
|messages|2-tuples of (LLM token, metadata) from LLM calls.|
|custom|Custom data emitted from nodes via the `writer` config parameter.|
|tools|Tool-call lifecycle events (`on_tool_start`, `on_tool_event`, `on_tool_end`, `on_tool_error`).|
|debug|All available info throughout graph execution.|

### ​ Graph state
Use the stream modes `updates` and `values` to stream the state of the graph as it executes. - `updates` streams the **updates** to the state after each step of the graph.
- `values` streams the **full value** of the state after each step of the graph.
```
import { StateGraph, StateSchema, START, END } from "@langchain/langgraph";
import { z } from "zod/v4";

const State = new StateSchema({
 topic: z.string(),
 joke: z.string(),
});

const graph = new StateGraph(State)
 .addNode("refineTopic", (state) => {
 return { topic: state.topic + " and cats" };
 })
 .addNode("generateJoke", (state) => {
 return { joke: `This is a joke about ${state.topic}` };
 })
 .addEdge(START, "refineTopic")
 .addEdge("refineTopic", "generateJoke")
 .addEdge("generateJoke", END)
 .compile();

```
- updates
- values
Use this to stream only the **state updates** returned by the nodes after each step. The streamed outputs include the name of the node as well as the update.
```
for await (const chunk of await graph.stream(
 { topic: "ice cream" },
 { streamMode: "updates" }
)) {
 for (const [nodeName, state] of Object.entries(chunk)) {
 console.log(`Node ${nodeName} updated:`, state);
 }
}

```

…

```
import { ChatOpenAI } from "@langchain/openai";
import { StateGraph, StateSchema, GraphNode, START } from "@langchain/langgraph";
import * as z from "zod";

const MyState = new StateSchema({
 topic: z.string(),
 joke: z.string().default(""),
});

const model = new ChatOpenAI({ model: "gpt-4.1-mini" });

const callModel: GraphNode<typeof MyState> = async (state) => {
 // Call the LLM to generate a joke about a topic
 // Note that message events are emitted even when the LLM is run using .invoke rather than .stream
 const modelResponse = await model.invoke([
 { role: "user", content: `Generate a joke about ${state.topic}` },
 ]);
 return { joke: modelResponse.content };
};

const graph = new StateGraph(MyState)
 .addNode("callModel", callModel)
 .addEdge(START, "callModel")
 .compile();

// The "messages" stream mode returns an iterator of tuples [messageChunk, metadata]
// where messageChunk is the token streamed by the LLM and metadata is a dictionary
// with information about the graph node where the LLM was called and other information
for await (const [messageChunk, metadata] of await graph.stream(
 { topic: "ice cream" },
 { streamMode: "messages" }
)) {
 if (messageChunk.content) {
 console.log(messageChunk.content + "|");
 }
}

```

…

```
import { ChatAnthropic } from "@langchain/anthropic";
import { StateGraph, StateSchema, START } from "@langchain/langgraph";
import * as z from "zod";

const streamModel = new ChatAnthropic({ model: "claude-3-haiku-20240307" });
const internalModel = new ChatAnthropic({
 model: "claude-3-haiku-20240307",
}).withConfig({
 tags: ["nostream"],
});

const State = new StateSchema({
 topic: z.string(),
 answer: z.string().optional(),
 notes: z.string().optional(),
});

const writeAnswer = async (state: typeof State.State) => {
 const r = await streamModel.invoke([
 { role: "user", content: `Reply briefly about ${state.topic}` },
 ]);
 return { answer: r.content };
};

const internalNotes = async (state: typeof State.State) => {
 // Tokens from this model are omitted from streamMode: "messages" because of nostream
 const r = await internalModel.invoke([
 { role: "user", content: `Private notes on ${state.topic}` },
 ]);
 return { notes: r.content };
};

const graph = new StateGraph(State)
 .addNode("writeAnswer", writeAnswer)
 .addNode("internal_notes", internalNotes)
 .addEdge(START, "writeAnswer")
 .addEdge("writeAnswer", "internal_notes")
 .compile();

const stream = await graph.stream({ topic: "AI" }, { streamMode: "messages" });

```

…

```
import { ChatOpenAI } from "@langchain/openai";
import { StateGraph, StateSchema, GraphNode, START } from "@langchain/langgraph";
import * as z from "zod";

const model = new ChatOpenAI({ model: "gpt-4.1-mini" });

const State = new StateSchema({
 topic: z.string(),
 joke: z.string(),
 poem: z.string(),
});

const writeJoke: GraphNode<typeof State> = async (state) => {
 const topic = state.topic;
 const jokeResponse = await model.invoke([
 { role: "user", content: `Write a joke about ${topic}` }
 ]);
 return { joke: jokeResponse.content };
};

const writePoem: GraphNode<typeof State> = async (state) => {
 const topic = state.topic;
 const poemResponse = await model.invoke([
 { role: "user", content: `Write a short poem about ${topic}` }
 ]);
 return { poem: poemResponse.content };
};

const graph = new StateGraph(State)
 .addNode("writeJoke", writeJoke)
 .addNode("writePoem", writePoem)
 // write both the joke and the poem concurrently
 .addEdge(START, "writeJoke")
 .addEdge(START, "writePoem")
 .compile();

// The "messages" stream mode returns a tuple of [messageChunk, metadata]
// where messageChunk is the token streamed by the LLM and metadata is a dictionary
// with information about the graph node where the LLM was called and other information
for await (const [msg, metadata] of await graph.stream(
 { topic: "cats" },
 { streamMode: "messages" }
)) {
 // Filter the streamed tokens by the langgraph_node field in the metadata
 // to only include the tokens from the writePoem node
 if (msg.content && metadata.langgraph_node === "writePoem") {
 console.log(msg.content + "|");
 }
}

```

…

```
import { StateGraph, StateSchema, GraphNode, START, LangGraphRunnableConfig } from "@langchain/langgraph";
import * as z from "zod";

const State = new StateSchema({
 query: z.string(),
 answer: z.string(),
});

const node: GraphNode<typeof State> = async (state, config) => {
 // Use the writer to emit a custom key-value pair (e.g., progress update)
 config.writer({ custom_key: "Generating custom data inside node" });
 return { answer: "some data" };
};

const graph = new StateGraph(State)
 .addNode("node", node)
 .addEdge(START, "node")
 .compile();

const inputs = { query: "example" };

// Set streamMode: "custom" to receive the custom data in the stream
for await (const chunk of await graph.stream(inputs, { streamMode: "custom" })) {
 console.log(chunk);
}

```

…

```
import { StateGraph, StateSchema, START } from "@langchain/langgraph";
import { z } from "zod/v4";

// Define subgraph
const SubgraphState = new StateSchema({
 foo: z.string(), // note that this key is shared with the parent graph state
 bar: z.string(),
});

const subgraphBuilder = new StateGraph(SubgraphState)
 .addNode("subgraphNode1", (state) => {
 return { bar: "bar" };
 })
 .addNode("subgraphNode2", (state) => {
 return { foo: state.foo + state.bar };
 })
 .addEdge(START, "subgraphNode1")
 .addEdge("subgraphNode1", "subgraphNode2");
const subgraph = subgraphBuilder.compile();

// Define parent graph
const ParentState = new StateSchema({
 foo: z.string(),
});

const builder = new StateGraph(ParentState)
 .addNode("node1", (state) => {
 return { foo: "hi! " + state.foo };
 })
 .addNode("node2", subgraph)
 .addEdge(START, "node1")
 .addEdge("node1", "node2");
const graph = builder.compile();

for await (const chunk of await graph.stream(
 { foo: "foo" },
 {
 streamMode: "updates",
 // Set subgraphs: true to stream outputs from subgraphs
 subgraphs: true,
 }
)) {
 console.log(chunk);
}

```

…

### ​ Debug
Use the `debug` streaming mode to stream as much information as possible throughout the execution of the graph. The streamed outputs include the name of the node as well as the full state.

…

### ​ Multiple modes at once
You can pass an array as the `streamMode` parameter to stream multiple modes at once. The streamed outputs will be tuples of `[mode, chunk]` where `mode` is the name of the stream mode and `chunk` is the data streamed by that mode.

…

```
import { StateGraph, GraphNode, StateSchema } from "@langchain/langgraph";
import * as z from "zod";

const State = new StateSchema({ result: z.string() });

const callArbitraryModel: GraphNode<typeof State> = async (state, config) => {
 // Example node that calls an arbitrary model and streams the output
 // Assume you have a streaming client that yields chunks
 // Generate LLM tokens using your custom streaming client
 for await (const chunk of yourCustomStreamingClient(state.topic)) {
 // Use the writer to send custom data to the stream
 config.writer({ custom_llm_chunk: chunk });
 }
 return { result: "completed" };
};

const graph = new StateGraph(State)
 .addNode("callArbitraryModel", callArbitraryModel)
 // Add other nodes and edges as needed
 .compile();

// Set streamMode: "custom" to receive the custom data in the stream
for await (const chunk of await graph.stream(
 { topic: "cats" },
 { streamMode: "custom" }
)) {
 // The chunk will contain the custom data streamed from the llm
 console.log(chunk);
}

```

### Properties

~NodeReturnType ~NodeType ~RunInput ~RunOutput autoValidate builder cache? channels checkpointer? config? debug description? inputChannels interruptAfter? interruptBefore? lc_kwargs lc_runnable lc_serializable name? nodes outputChannels retryPolicy? stepTimeout? store? streamChannels? streamMode

…

### Methods

_batchWithConfig _callWithConfig _getOptionsList _separateRunnableConfigFromCallOptions _streamLog _transformStreamWithConfig assign asTool attachBranch attachEdge attachNode batch clearCache getGraphAsync getName getState getStateHistory getSubgraphsAsync invoke isInterrupted pick pipe stream streamEvents streamLog toJSON toJSONNotImplemented transform updateState validate withConfig withFallbacks withListeners withRetry isRunnable

…

### stream Mode

streamMode: StreamMode[]

The streaming modes enabled for this graph. Defaults to ["values"].
Supported modes:

- "values": Streams the full state after each step
- "updates": Streams state updates after each step
- "messages": Streams messages from within nodes
- "custom": Streams custom events from within nodes
- "debug": Streams events related to the execution of the graph - useful for tracing & debugging graph execution

…

undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  >,
  >[],
  runManagers?: (undefined | CallbackManagerForChainRun)[],
  batchOptions?: RunnableBatchOptions,
  ) => Promise<(Error | StateType<ToStateDefinition<O>>)[]>,
inputs: T[],
  options?:
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  > & { runType?: string },
  >
| Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

  #### Parameters
  - func: (
  inputs: T[],
  options?: Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

- inputs: T[]
  - `Optional`options:
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
> & { runType?: string },
  >
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  >,
  >,
  runManager?: CallbackManagerForChainRun,
  ) => Promise<StateType<ToStateDefinition<O>>>
  ),
input: T,
  options?: Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],

…

>,
  >,
  runManager?: CallbackManagerForChainRun,
  ) => Promise<StateType<ToStateDefinition<O>>>
  )
  - input: T
  - `Optional`options: Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

  #### Type Parameters
  - O extends PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  > & { runType?: string }

…

>,
  >,
  ): [
  RunnableConfig<Record<string, any>>,
  Omit<
  Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  >,
  >,
  keyof RunnableConfig<Record<string, any>>,
  >,
  ]
  #### Parameters
  - `Optional`options: Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  >,
  >
  #### Returns [ RunnableConfig < Record < string , any > > , Omit < Partial < PregelOptions < Record < "__start__" | N , PregelNode < S , U > > , Record < string | N , BaseChannel < unknown , unknown , unknown > > , StateType < ToStateDefinition < C > > & Record < string , any > , undefined | StreamMode | StreamMode [] , boolean , undefined | "text/event-stream" , > , > , keyof RunnableConfig < Record < string , any > > , > , ]

### Protected _ stream Log
- _streamLog(
  input:
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >,
  logStreamCallbackHandler: LogStreamCallbackHandler,
  config: Partial<CallOptions>,
  ): AsyncGenerator<RunLogPatch>

…

  #### Returns AsyncGenerator < RunLogPatch >

### Protected _ transform Stream With Config
- _transformStreamWithConfig<
  I extends
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,

…

Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  >,
  >,
  ) => AsyncGenerator<O>,
  options?: Partial<
PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  >,
  > & { runType?: string },
  ): AsyncGenerator<O>

…

  #### Parameters
  - inputGenerator: AsyncGenerator<I>
  - transformer: (
  generator: AsyncGenerator<I>,
  runManager?: CallbackManagerForChainRun,
  options?: Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
>,
  >,
  ) => AsyncGenerator<O>
  - `Optional`options: Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

)[],
  options?:
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
>,
  >
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

  #### Parameters
  - inputs: (
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >
  )[]

   Array of inputs to each batch call.
- `Optional`options:
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
>,
  >
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

)[],
  options?:
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
>,
  >
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

  #### Parameters
  - inputs: (
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >
  )[]

   Array of inputs to each batch call.
- `Optional`options:
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
>,
  >
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

…

)[],
  options?:
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
>,
  >
  | Partial<
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",

## What’s possible with LangGraph streaming
**Stream graph state**— get state updates / values with
`updates`and
`values`modes.
**Stream subgraph outputs**— include outputs from both the parent graph and any nested subgraphs.
**Stream LLM tokens**— capture token streams from anywhere: inside nodes, subgraphs, or tools.
**Stream custom data**— send custom updates or progress signals directly from tool functions.
**Use multiple streaming modes**— choose from
…
|Mode|Description|
|--|--|
|`values`|Streams the full value of the state after each step of the graph.|
|`updates`|Streams the updates to the state after each step of the graph.
If multiple updates are made in the same step (e.g., multiple nodes are run), those updates are streamed separately.|
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
…
Use this to stream only the
**state updates**returned by the nodes after each step.
The streamed outputs include the name of the node as well as the update.
```
for await (const chunk of await graph.stream(
{ topic: "ice cream" },
{ streamMode: "updates" }
)) {
console.log(chunk);
```
…
## Use with any LLMYou can use
`streamMode: "custom"` to stream data from
**any LLM API**— even if that API does
**not**implement the LangChain chat model interface.
This lets you integrate raw LLM clients or external services that provide their own streaming interfaces, making LangGraph highly flexible for custom setups.
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
...
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
...
import { z } from "zod/v4";
import OpenAI from "openai";
...
const getItems = tool(
async (input, config: LangGraphRunnableConfig) => {
let response = "";
for await (const msgChunk of streamTokens(
...
content: `Can you tell me what kind of items i might find in the following place: '${input.place}'.
List at least 3 such items separating them by a comma.
And include a brief description of each item.`,
...
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
...
return { messages: [toolMessage] };
...
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
...
for await (const chunk of await graph.stream(
inputs,
{ streamMode: "custom" }
...
console.log(chunk.content + "|");
```
## Disable streaming for specific chat modelsIf your application mixes models that support streaming with those that do not, you may need to explicitly disable streaming for models that do not support it.
Set
`streaming: false` when initializing the model.
```
import { ChatOpenAI } from "@langchain/openai";
const model = new ChatOpenAI({
model: "o1-preview",
streaming: false, // (1)!
});
```

## 여러 모드 스트리밍
`streamMode` 매개변수에 배열을 전달하여 여러 모드를 동시에 스트리밍할 수 있습니다.
스트리밍되는 출력은
`[mode, chunk]` 튜플이 되며, 여기서
`mode`는 스트림 모드의 이름이고
`chunk`는 해당 모드에서 스트리밍된 데이터입니다.
```
for await (const [mode, chunk] of await graph.stream(inputs, {
streamMode: ["updates", "custom"],
})) {
console.log(chunk);
```
…
## 커스텀 데이터 스트리밍LangGraph 노드 또는 도구 내부에서
**커스텀 사용자 정의 데이터**를 전송하려면 다음 단계를 따르세요:
`LangGraphRunnableConfig`의
`writer`매개변수를 사용하여 커스텀 데이터를 발생시킵니다.
`.stream()`을 호출할 때
`streamMode: "custom"`으로 설정하여 스트림에서 커스텀 데이터를 가져옵니다.
여러 모드를 결합할 수 있지만 (예:
`["updates", "custom"]`), 적어도 하나는
`"custom"`이어야 합니다.
```
import { StateGraph, START, LangGraphRunnableConfig } from "@langchain/langgraph";
import * as z from "zod";
const State = z.object({
query: z.string(),
answer: z.string(),
...
const graph = new StateGraph(State)
.addNode("node", async (state, config) => {
// 커스텀 키-값 쌍을 발생시키기 위해 writer를 사용합니다 (예: 진행 상황 업데이트)
config.writer({ custom_key: "Generating custom data inside node" });
return { answer: "some data" };
})
.addEdge(START, "node")
.compile();
const inputs = { query: "example" };
// 스트림에서 커스텀 데이터를 받으려면 streamMode: "custom"으로 설정합니다
for await (const chunk of await graph.stream(inputs, { streamMode: "custom" })) {
console.log(chunk);
```
## 모든 LLM과 함께 사용
`streamMode: "custom"`을 사용하여
**모든 LLM API**에서 데이터를 스트리밍할 수 있습니다 — 해당 API가 LangChain 채팅 모델 인터페이스를 구현하지
**않더라도**말입니다.
이를 통해 자체 스트리밍 인터페이스를 제공하는 원시 LLM 클라이언트 또는 외부 서비스를 통합할 수 있어, LangGraph를 커스텀 설정에 매우 유연하게 사용할 수 있습니다.
```
import { LangGraphRunnableConfig } from "@langchain/langgraph";
const callArbitraryModel = async (
state: any,
config: LangGraphRunnableConfig
...
// 커스텀 스트리밍 클라이언트를 사용하여 LLM 토큰을 생성합니다
for await (const chunk of yourCustomStreamingClient(state.topic)) {
// writer를 사용하여 스트림에 커스텀 데이터를 전송합니다
config.writer({ custom_llm_chunk: chunk });
return { result: "completed" };
};
const graph = new StateGraph(State)
.addNode("callArbitraryModel", callArbitraryModel)
// 필요에 따라 다른 노드와 엣지를 추가합니다
.compile();
// 스트림에서 커스텀 데이터를 받으려면 streamMode: "custom"으로 설정합니다
for await (const chunk of await graph.stream(
{ topic: "cats" },
{ streamMode: "custom" }
)) {
// 청크에는 LLM에서 스트리밍된 커스텀 데이터가 포함됩니다
console.log(chunk);
```
확장 예제: 임의의 채팅 모델 스트리밍
...
async function* streamTokens(modelName: string, messages: any[]) {
const response = await openaiClient.chat.completions.create({
messages,
model: modelName,
stream: true,
...
let role: string | null = null;
for await (const chunk of response) {
const delta = chunk.choices[0]?.delta;
if (delta?.role) {
role = delta.role;
if (delta?.content) {
yield { role, content: delta.content };
// 이것은 우리의 도구입니다
const getItems = tool(
async (input, config: LangGraphRunnableConfig) => {
let response = "";
for await (const msgChunk of streamTokens(
...
content: `Can you tell me what kind of items i might find in the following place: '${input.place}'.
List at least 3 such items separating them by a comma.
And include a brief description of each item.`,
...
},
...
messages: z
.array(z.custom<BaseMessage>())
...
const graph = new StateGraph(State)
// 이것은 도구 호출 그래프 노드입니다
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
...
## 특정 채팅 모델에 대한 스트리밍 비활성화애플리케이션에서 스트리밍을 지원하는 모델과 지원하지 않는 모델을 혼합하여 사용하는 경우, 스트리밍을 지원하지 않는 모델에 대해 명시적으로 스트리밍을 비활성화해야 할 수 있습니다.
모델을 초기화할 때
`streaming: false`로 설정합니다.
```
import { ChatOpenAI } from "@langchain/openai";
const model = new ChatOpenAI({
model: "o1-preview",
// 채팅 모델에 대한 스트리밍을 비활성화하려면 streaming: false로 설정합니다
streaming: false,
});
```