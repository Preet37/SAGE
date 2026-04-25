# Source: https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer
# Title: checkpointer | @langchain/langgraph (JavaScript reference)
# Fetched via: search
# Date: 2026-04-10

LangGraph has a built-in persistence layer that saves graph state as checkpoints. When you compile a graph with a checkpointer, a snapshot of the graph state is saved at every step of execution, organized into threads. This enables human-in-the-loop workflows, conversational memory, time travel debugging, and fault-tolerant execution.

…

## ​ Why use persistence
Persistence is required for the following features: - **Human-in-the-loop**: Checkpointers facilitate human-in-the-loop workflows by allowing humans to inspect, interrupt, and approve graph steps. Checkpointers are needed for these workflows as the person has to be able to view the state of a graph at any point in time, and the graph has to be able to resume execution after the person has made any updates to the state. See Interrupts for examples.

…

- **Time travel**: Checkpointers allow for “time travel”, allowing users to replay prior graph executions to review and / or debug specific graph steps. In addition, checkpointers make it possible to fork the graph state at arbitrary checkpoints to explore alternative trajectories.
- **Fault-tolerance**: Checkpointing provides fault-tolerance and error recovery: if one or more nodes fail at a given superstep, you can restart your graph from the last successful step.

…

## ​ Core concepts

### ​ Threads
A thread is a unique ID or thread identifier assigned to each checkpoint saved by a checkpointer. It contains the accumulated state of a sequence of runs. When a run is executed, the state of the underlying graph of the assistant will be persisted to the thread. When invoking a graph with a checkpointer, you **must** specify a `thread_id` as part of the `configurable` portion of the config:

…

A thread’s current and historical state can be retrieved. To persist state, a thread must be created prior to executing a run. The LangSmith API provides several endpoints for creating and managing threads and thread state. See the API reference for more details. The checkpointer uses `thread_id` as the primary key for storing and retrieving checkpoints. Without it, the checkpointer cannot save state or resume execution after an interrupt, since the checkpointer uses `thread_id` to load the saved state.

### ​ Checkpoints
The state of a thread at a particular point in time is called a checkpoint. A checkpoint is a snapshot of the graph state saved at each super-step and is represented by a `StateSnapshot` object (see StateSnapshot fields for the full field reference).

#### ​ Super-steps
LangGraph created a checkpoint at each **super-step** boundary. A super-step is a single “tick” of the graph where all nodes scheduled for that step execute (potentially in parallel). For a sequential graph like `START -> A -> B -> END`, there are separate super-steps for the input, node A, and node B — producing a checkpoint after each one.
Understanding super-step boundaries is important for time travel, because you can only resume execution from a checkpoint (i.e., a super-step boundary). Checkpoints are persisted and can be used to restore the state of a thread at a later time. Let’s see what checkpoints are saved when a simple graph is invoked as follows:
```
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
 foo: str
 bar: Annotated[list[str], add]

def node_a(state: State):
 return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
 return {"foo": "b", "bar": ["b"]}

workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
graph.invoke({"foo": "", "bar":[]}, config)

```

…

- Checkpoint with the user input `{'foo': '', 'bar': []}` and `node_a` as the next node to be executed
- Checkpoint with the outputs of `node_a` `{'foo': 'a', 'bar': ['a']}` and `node_b` as the next node to be executed
- Checkpoint with the outputs of `node_b` `{'foo': 'b', 'bar': ['a', 'b']}` and no next nodes to be executed
Note that we `bar` channel values contain outputs from both nodes as we have a reducer for `bar` channel.

#### ​ Checkpoint namespace
Each checkpoint has a `checkpoint_ns` (checkpoint namespace) field that identifies which graph or subgraph it belongs to: - **`""`** (empty string): The checkpoint belongs to the parent (root) graph.
- **`"node_name:uuid"`**: The checkpoint belongs to a subgraph invoked as the given node. For nested subgraphs, namespaces are joined with `|` separators (e.g., `"outer_node:uuid|inner_node:uuid"`).
You can access the checkpoint namespace from within a node via the config:
```
from langchain_core.runnables import RunnableConfig

def my_node(state: State, config: RunnableConfig):
 checkpoint_ns = config["configurable"]["checkpoint_ns"]
 # "" for the parent graph, "node_name:uuid" for a subgraph

```

…

## ​ Get and update state

### ​ Get state
When interacting with the saved graph state, you **must** specify a thread identifier. You can view the *latest* state of the graph by calling `graph.get_state(config)`. This will return a `StateSnapshot` object that corresponds to the latest checkpoint associated with the thread ID provided in the config or a checkpoint associated with a checkpoint ID for the thread, if provided.
```
# get the latest state snapshot
config = {"configurable": {"thread_id": "1"}}
graph.get_state(config)

# get a state snapshot for a specific checkpoint_id
config = {"configurable": {"thread_id": "1", "checkpoint_id": "1ef663ba-28fe-6528-8002-5a559208592c"}}
graph.get_state(config)

```

…

```
StateSnapshot(
 values={'foo': 'b', 'bar': ['a', 'b']},
 next=(),
 config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28fe-6528-8002-5a559208592c'}},
 metadata={'source': 'loop', 'writes': {'node_b': {'foo': 'b', 'bar': ['b']}}, 'step': 2},
 created_at='2024-08-29T19:19:38.821749+00:00',
 parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}}, tasks=()
)

```

#### ​ StateSnapshot fields
|Field|Type|Description|
|--|--|--|
|`values`|`dict`|State channel values at this checkpoint.|
|`next`|`tuple[str, ...]`|Node names to execute next. Empty `()` means the graph is complete.|
|`config`|`dict`|Contains `thread_id`, `checkpoint_ns`, and `checkpoint_id`.|
|`metadata`|`dict`|Execution metadata. Contains `source` (`"input"`, `"loop"`, or `"update"`), `writes` (node outputs), and `step` (super-step counter).|
|`created_at`|`str`|ISO 8601 timestamp of when this checkpoint was created.|
|`parent_config`|`dict | None`|Config of the previous checkpoint. `None` for the first checkpoint.|
|`tasks`|`tuple[PregelTask, ...]`|Tasks to execute at this step. Each task has `id`, `name`, `error`, `interrupts`, and optionally `state` (subgraph snapshot, when using `subgraphs=True`).|

### ​ Get state history
You can get the full history of the graph execution for a given thread by calling `graph.get_state_history(config)`. This will return a list of `StateSnapshot` objects associated with the thread ID provided in the config. Importantly, the checkpoints will be ordered chronologically with the most recent checkpoint / `StateSnapshot` being the first in the list.

…

```
[
 StateSnapshot(
 values={'foo': 'b', 'bar': ['a', 'b']},
 next=(),
 config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28fe-6528-8002-5a559208592c'}},
 metadata={'source': 'loop', 'writes': {'node_b': {'foo': 'b', 'bar': ['b']}}, 'step': 2},
 created_at='2024-08-29T19:19:38.821749+00:00',
 parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}},
 tasks=(),
 ),
 StateSnapshot(
 values={'foo': 'a', 'bar': ['a']},
 next=('node_b',),
 config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f9-6ec4-8001-31981c2c39f8'}},
 metadata={'source': 'loop', 'writes': {'node_a': {'foo': 'a', 'bar': ['a']}}, 'step': 1},
 created_at='2024-08-29T19:19:38.819946+00:00',
 parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f4-6b4a-8000-ca575a13d36a'}},
 tasks=(PregelTask(id='6fb7314f-f114-5413-a1f3-d37dfe98ff44', name='node_b', error=None, interrupts=()),),
 ),
 StateSnapshot(
 values={'foo': '', 'bar': []},
 next=('node_a',),
 config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f4-6b4a-8000-ca575a13d36a'}},
 metadata={'source': 'loop', 'writes': None, 'step': 0},
 created_at='2024-08-29T19:19:38.817813+00:00',
 parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f0-6c66-bfff-6723431e8481'}},
 tasks=(PregelTask(id='f1b14528-5ee5-579c-949b-23ef9bfbed58', name='node_a', error=None, interrupts=()),),
 ),
 StateSnapshot(
 values={'bar': []},
 next=('__start__',),
 config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef663ba-28f0-6c66-bfff-6723431e8481'}},
 metadata={'source': 'input', 'writes': {'foo': ''}, 'step': -1},
 created_at='2024-08-29T19:19:38.816205+00:00',
 parent_config=None,
 tasks=(PregelTask(id='6d27aa2e-d72b-5504-a36f-8620e54a76dd', name='__start__', error=None, interrupts=()),),
 )
]

```

#### ​ Find a specific checkpoint
You can filter the state history to find checkpoints matching specific criteria:
```
history = list(graph.get_state_history(config))

# Find the checkpoint before a specific node executed
before_node_b = next(s for s in history if s.next == ("node_b",))

# Find a checkpoint by step number
step_2 = next(s for s in history if s.metadata["step"] == 2)

# Find checkpoints created by update_state
forks = [s for s in history if s.metadata["source"] == "update"]

# Find the checkpoint where an interrupt occurred
interrupted = next(
 s for s in history
 if s.tasks and any(t.interrupts for t in s.tasks)
)

```

### ​ Replay
Replay re-executes steps from a prior checkpoint. Invoke the graph with a prior `checkpoint_id` to re-run nodes after that checkpoint. Nodes before the checkpoint are skipped (their results are already saved). Nodes after the checkpoint re-execute, including any LLM calls, API requests, or interrupts — which are always re-triggered during replay. See Time travel for full details and code examples on replaying past executions.

### ​ Update state
You can edit the graph state using `update_state`. This creates a new checkpoint with the updated values — it does not modify the original checkpoint. The update is treated the same as a node update: values are passed through reducer functions when defined, so channels with reducers *accumulate* values rather than overwrite them. You can optionally specify `as_node` to control which node the update is treated as coming from, which affects which node executes next. See Time travel: `as_node` for details.

## ​ Memory store
A state schema specifies a set of keys that are populated as a graph is executed. As discussed above, state can be written by a checkpointer to a thread at each graph step, enabling state persistence. What if we want to retain some information *across threads*? Consider the case of a chatbot where we want to retain specific information about the user across *all* chat conversations (e.g., threads) with that user!

…

### ​ Using in LangGraph
With this all in place, we use the store in LangGraph. The store works hand-in-hand with the checkpointer: the checkpointer saves state to threads, as discussed above, and the store allows us to store arbitrary information for access *across* threads. We compile the graph with both the checkpointer and the store as follows.
```
from dataclasses import dataclass
from langgraph.checkpoint.memory import InMemorySaver

@dataclass
class Context:
 user_id: str

# We need this because we want to enable threads (conversations)
checkpointer = InMemorySaver()

# ... Define the graph ...

# Compile the graph with the checkpointer and store
builder = StateGraph(MessagesState, context_schema=Context)
# ... add nodes and edges ...
graph = builder.compile(checkpointer=checkpointer, store=store)

```

…

## ​ Checkpointer libraries
Under the hood, checkpointing is powered by checkpointer objects that conform to `BaseCheckpointSaver` interface. LangGraph provides several checkpointer implementations, all implemented via standalone, installable libraries.

See checkpointer integrations for available providers. - `langgraph-checkpoint`: The base interface for checkpointer savers (`BaseCheckpointSaver`) and serialization/deserialization interface (`SerializerProtocol`). Includes in-memory checkpointer implementation (`InMemorySaver`) for experimentation. LangGraph comes with `langgraph-checkpoint` included.

…

- `.put_writes` - Store intermediate writes linked to a checkpoint (i.e. pending writes).
- `.get_tuple` - Fetch a checkpoint tuple using for a given configuration (`thread_id` and `checkpoint_id`). This is used to populate `StateSnapshot` in `graph.get_state()`.
- `.list` - List checkpoints that match a given configuration and filter criteria. This is used to populate state history in `graph.get_state_history()`
If the checkpointer is used with asynchronous graph execution (i.e. executing the graph via `.ainvoke`, `.astream`, `.abatch`), asynchronous versions of the above methods will be used (`.aput`, `.aput_writes`, `.aget_tuple`, `.alist`).

…

### ​ Serializer
When checkpointers save the graph state, they need to serialize the channel values in the state. This is done using serializer objects. `langgraph_checkpoint` defines protocol for implementing serializers provides a default implementation (`JsonPlusSerializer`) that handles a wide variety of types, including LangChain and LangGraph primitives, datetimes, enums and more.

The full state type representing the complete shape of your graph's state after all reducers have been applied.
...
The type of values that can be passed when resuming from an interrupt.
...
Whether to automatically validate the graph structure when it is compiled.
Defaults to true.
`Optional`cache
Optional cache for the graph, useful for caching tasks.
The channels in the graph, mapping channel names to their BaseChannel or ManagedValueSpec instances
`Optional`checkpointer
Optional checkpointer for persisting graph state.
When provided, saves a checkpoint of the graph state at every superstep.
When false or undefined, checkpointing is disabled, and the graph will not be able to save or restore state.
`Optional`config
The default configuration for graph execution, can be overridden on a per-invocation basis
Whether to enable debug logging.
Defaults to false.
`Optional`description
...
Gets the current state of the graph.
Requires a checkpointer to be configured.
Configuration for retrieving the state
`Optional`options: GetStateOptions
...
Gets the history of graph states.
Requires a checkpointer to be configured.
Useful for:
Configuration for retrieving the history
...
Updates the state of the graph with new values.
Requires a checkpointer to be configured.
This method can be used for:
Configuration for the update
...
Final result from building and compiling a StateGraph.
Should not be instantiated directly, only using the StateGraph
`.compile()`instance method.

This library defines the base interface for LangGraph.js checkpointers.
Checkpointers provide persistence layer for LangGraph.
They allow you to interact with and manage the graph's state.
When you use a graph with a checkpointer, the checkpointer saves a
*checkpoint* of the graph state at every superstep, enabling several powerful capabilities like human-in-the-loop, "memory" between interactions and more.
Checkpoint is a snapshot of the graph state at a given point in time.
Checkpoint tuple refers to an object containing checkpoint and the associated config, metadata and pending writes.
Threads enable the checkpointing of multiple different runs, making them essential for multi-tenant chat applications and other scenarios where maintaining separate states is necessary.
A thread is a unique ID assigned to a series of checkpoints saved by a checkpointer.
When using a checkpointer, you must specify a
`thread_id` and optionally
`checkpoint_id` when running the graph.
`thread_id` is simply the ID of a thread.
This is always required
`checkpoint_id` can optionally be passed.
This identifier refers to a specific checkpoint within a thread.
This can be used to kick of a run of a graph from some point halfway through a thread.
You must pass these when invoking the graph as part of the configurable part of the config, e.g.
`{ configurable: { thread_id: "1" } } // valid config`
{ configurable: { thread_id: "1", checkpoint_id: "0c62ca34-ac19-445d-bbb0-5b4984975b2a" } } // also valid config
`@langchain/langgraph-checkpoint` also defines protocol for serialization/deserialization (serde) and provides an default implementation that handles a range of types.
When a graph node fails mid-execution at a given superstep, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that superstep, so that whenever we resume graph execution from that superstep we don't re-run the successful nodes.
Each checkpointer should conform to
`BaseCheckpointSaver` interface and must implement the following methods:
`.put` - Store a checkpoint with its configuration and metadata.
`.putWrites` - Store intermediate writes linked to a checkpoint (i.e. pending writes).
`.getTuple` - Fetch a checkpoint tuple using for a given configuration (
`thread_id` and
`thread_ts`).
`.list` - List checkpoints that match a given configuration and filter criteria.
`import { MemorySaver } from "@langchain/langgraph-checkpoint";`
const writeConfig = {
configurable: {
thread_id: "1",
checkpoint_ns: ""
};
const readConfig = {
…
},
node: {
"start:node": 2
},
pending_sends: [],
// store checkpoint
await checkpointer.put(writeConfig, checkpoint, {}, {})
// load checkpoint
await checkpointer.get(readConfig)
// list checkpoints
for await (const checkpoint of checkpointer.list(readConfig)) {
console.log(checkpoint);

# Class CompiledStateGraph<S, U, N, I, O, C, NodeReturnType, InterruptType, WriterType>

Final result from building and compiling a StateGraph. Should not be instantiated directly, only using the StateGraph `.compile()`
instance method.

#### Type Parameters
- S
- U
- N extends string = typeof START
- I extends SDZod = StateDefinition
- O extends SDZod = StateDefinition
- C extends SDZod = StateDefinition
- NodeReturnType = unknown
- InterruptType = unknown
- WriterType = unknown

#### Hierarchy ( View Summary )
- CompiledGraph<
  N,
  S,
  U,
  StateType<ToStateDefinition<C>>,
  UpdateType<ToStateDefinition<I>>,
  StateType<ToStateDefinition<O>>,
  NodeReturnType,
  CommandInstance<InferInterruptResumeType<InterruptType>, Prettify<U>, N>,
  InferWriterType<WriterType>,
  > - CompiledStateGraph

…

### Properties

~NodeReturnType ~NodeType ~RunInput ~RunOutput autoValidate builder cache? channels checkpointer? config? debug description? inputChannels interruptAfter? interruptBefore? lc_kwargs lc_runnable lc_serializable name? nodes outputChannels retryPolicy? stepTimeout? store? streamChannels? streamMode

…

### Methods

_batchWithConfig _callWithConfig _getOptionsList _separateRunnableConfigFromCallOptions _streamLog _transformStreamWithConfig assign asTool attachBranch attachEdge attachNode batch clearCache getGraphAsync getName getState getStateHistory getSubgraphsAsync invoke isInterrupted pick pipe stream streamEvents streamLog toJSON toJSONNotImplemented transform updateState validate withConfig withFallbacks withListeners withRetry isRunnable

…

## Constructors

### constructor
- new CompiledStateGraph<
  S,
  U,
  N extends string = "__start__",
  I extends SDZod = StateDefinition,
  O extends SDZod = StateDefinition,
  C extends SDZod = StateDefinition,
  NodeReturnType = unknown,
  InterruptType = unknown,
  WriterType = unknown,

…

### auto Validate

autoValidate: boolean

Whether to automatically validate the graph structure when it is compiled. Defaults to true.

…

### channels

channels: Channels

The channels in the graph, mapping channel names to their BaseChannel or ManagedValueSpec instances

### Optional checkpointer

checkpointer?: boolean | BaseCheckpointSaver<number>

Optional checkpointer for persisting graph state.
When provided, saves a checkpoint of the graph state at every superstep.
When false or undefined, checkpointing is disabled, and the graph will not be able to save or restore state.

…

### Optional description

description?: string

The description of the compiled graph.
This is used by the supervisor agent to describe the handoff to the agent.

### input Channels

inputChannels: string | N | (string | N)[]

The input channels for the graph. These channels receive the initial input when the graph is invoked.
Can be a single channel key or an array of channel keys.

### Optional interrupt After

interruptAfter?: "*" | ("__start__" | N)[]

Optional array of node names or "all" to interrupt after executing these nodes.
Used for implementing human-in-the-loop workflows.

### Optional interrupt Before

interruptBefore?: "*" | ("__start__" | N)[]

Optional array of node names or "all" to interrupt before executing these nodes.
Used for implementing human-in-the-loop workflows.

…

### output Channels

outputChannels: string | N | (string | N)[]

The output channels for the graph. These channels contain the final output when the graph completes.
Can be a single channel key or an array of channel keys.

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

  #### Returns string []

### lc_ secrets
- get lc_secrets(): undefined | { [key: string]: string }

  A map of secrets, which will be omitted from serialization.
  Keys are paths to the secret in constructor args, e.g. "foo.bar.baz".
  Values are the secret ids, which will be used when deserializing.

…

  #### Returns keyof Channels | ( keyof Channels ) []

  Channel keys to stream, either as a single key or array

### stream Channels List
- get streamChannelsList(): (keyof Channels)[]

  Gets a list of all channels that should be streamed.
  If streamChannels is specified, returns those channels.
  Otherwise, returns all channels in the graph.

…

## Methods

### _ batch With Config
- _batchWithConfig<
  T extends
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,

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

>,
  >[],
  runManagers?: (undefined | CallbackManagerForChainRun)[],
  batchOptions?: RunnableBatchOptions,
  ) => Promise<(Error | StateType<ToStateDefinition<O>>)[]>

   The function to be executed for each input value.
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

…

### Protected _ call With Config
- _callWithConfig<
  T extends
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,

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

…

  #### Type Parameters
  - T extends
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >

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

  #### Returns Promise < StateType < ToStateDefinition < O > > >

### Protected _ get Options List
- _getOptionsList<
  O extends
  PregelOptions<
  Record<"__start__" | N, PregelNode<S, U>>,
  Record<string | N, BaseChannel<unknown, unknown, unknown>>,
  StateType<ToStateDefinition<C>> & Record<string, any>,
  undefined | StreamMode | StreamMode[],
  boolean,
  undefined | "text/event-stream",
  > & { runType?: string },
  >(
  options: Partial<O> | Partial<O>[],
  length?: number,
  ): Partial<O>[]

…

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
  #### Parameters
  - input:
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >
  - logStreamCallbackHandler: LogStreamCallbackHandler
  - config: Partial<CallOptions>
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

  #### Type Parameters
  - I extends
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >
  - O extends StateType<ToStateDefinition<O>>
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

…

  #### Returns AsyncGenerator < O >

### assign
- assign(
  mapping: RunnableMapLike<
  Record<string, unknown>,
  Record<string, unknown>,
  >,
  ): Runnable

  Assigns new fields to the dict output of this runnable. Returns a new runnable.

…

  #### Returns Runnable

### as Tool
- asTool<
  T extends
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
> =
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >,
  >(
  fields: {
  description?: string;
  name?: string;
  schema: InteropZodType<T>;
  },
  ): RunnableToolLike<
  InteropZodType<ToolCall<string, Record<string, any>> | T>,
  StateType<ToStateDefinition<O>>,
  >

…

  #### Type Parameters
  - T extends
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  > =
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >
  #### Parameters
  - fields: { description?: string; name?: string; schema: InteropZodType<T> } - ##### Optional description ?: string

   The description of the tool. Falls back to the description on the Zod schema if not provided, or undefined if neither are provided.

…

  #### Returns void

### batch
- batch(
  inputs: (
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >
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

  #### Returns Promise < StateType < ToStateDefinition < O > > [] >

  An array of RunOutputs, or mixed RunOutputs and errors if batchOptions.returnExceptions is set
- batch(
  inputs: (
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >
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

  #### Returns Promise < ( Error | StateType < ToStateDefinition < O > > ) [] >

  An array of RunOutputs, or mixed RunOutputs and errors if batchOptions.returnExceptions is set
- batch(
  inputs: (
  | null
  | UpdateType<ToStateDefinition<I>>
  | CommandInstance<
  InferInterruptResumeType<InterruptType, false>,
  { [K in string | number | symbol]: U[K] },
  N,
  >

…

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

## Project description
# LangGraph Checkpoint
This library defines the base interface for LangGraph checkpointers.
Checkpointers provide persistence layer for LangGraph.
They allow you to interact with and manage the graph's state.
When you use a graph with a checkpointer, the checkpointer saves a *checkpoint* of the graph state at every superstep, enabling several powerful capabilities like human-in-the-loop, "memory" between interactions and more.
## Key concepts
### Checkpoint
Checkpoint is a snapshot of the graph state at a given point in time.
Checkpoint tuple refers to an object containing checkpoint and the associated config, metadata and pending writes.
### Thread
Threads enable the checkpointing of multiple different runs, making them essential for multi-tenant chat applications and other scenarios where maintaining separate states is necessary.
A thread is a unique ID assigned to a series of checkpoints saved by a checkpointer.
When using a checkpointer, you must specify a
…
can optionally be passed.
This identifier refers to a specific checkpoint within a thread.
This can be used to kick of a run of a graph from some point halfway through a thread.
You must pass these when invoking the graph as part of the configurable part of the config, e.g.
…
### Pending writes
When a graph node fails mid-execution at a given superstep, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that superstep, so that whenever we resume graph execution from that superstep we don't re-run the successful nodes.
…
- List checkpoints that match a given configuration and filter criteria.
If the checkpointer will be used with asynchronous graph execution (i.e. executing the graph via
…
## Usage
```
from langgraph.checkpoint.memory import MemorySaver
write_config = {"configurable": {"thread_id": "1", "checkpoint_ns": ""}}
read_config = {"configurable": {"thread_id": "1"}}
checkpointer = MemorySaver()
checkpoint = {
"v": 1,
"ts": "2024-07-31T20:14:19.804150+00:00",
"id": "1ef4f797-8335-6428-8001-8a1503f9b875",
"channel_values": {
"my_key": "meow",
"node": "node"
},
"channel_versions": {
"__start__": 2,
"my_key": 3,
"start:node": 3,
"node": 3
},
"versions_seen": {
"__input__": {},
"__start__": {
"__start__": 1
},
"node": {
"start:node": 2
}
},
"pending_sends": [],
# store checkpoint
checkpointer.put(write_config, checkpoint, {}, {})
# load checkpoint
checkpointer.get(read_config)
# list checkpoints
list(checkpointer.list(read_config))
```