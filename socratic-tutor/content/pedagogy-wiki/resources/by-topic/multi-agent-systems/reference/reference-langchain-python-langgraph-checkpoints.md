# Source: https://reference.langchain.com/python/langgraph/checkpoints/
# Title: Checkpointing | LangChain Reference
# Fetched via: search
# Date: 2026-04-10

# Checkpointing

##

base



|FUNCTION|DESCRIPTION|
|--|--|
|`create_checkpoint`|Create a checkpoint for the given channels.|

###

CheckpointMetadata



Bases:

`TypedDict`

Metadata associated with a checkpoint.

####

source

`instance-attribute`



```

source: Literal['input', 'loop', 'update', 'fork']

```

The source of the checkpoint.

`"input"`: The checkpoint was created from an input to invoke/stream/batch.

`"loop"`: The checkpoint was created from inside the pregel loop.

`"update"`: The checkpoint was created from a manual state update.

`"fork"`: The checkpoint was created as a copy of another checkpoint.

####

step

`instance-attribute`



```

step: int

```

The step number of the checkpoint.

`-1` for the first

`"input"` checkpoint.

`0` for the first

`"loop"` checkpoint.

`...` for the

`nth` checkpoint afterwards.

###

Checkpoint



Bases:

`TypedDict`

State snapshot at a given point in time.

####

id

`instance-attribute`



```

id: str

```

The ID of the checkpoint.

This is both unique and monotonically increasing, so can be used for sorting checkpoints from first to last.

####

channel_values

`instance-attribute`



```

channel_values: dict[str, Any]

```

The values of the channels at the time of the checkpoint.

Mapping from channel name to deserialized channel snapshot value.

####

channel_versions

`instance-attribute`



```

channel_versions: ChannelVersions

```

The versions of the channels at the time of the checkpoint.

The keys are channel names and the values are monotonically increasing version strings for each channel.

####

versions_seen

`instance-attribute`



```

versions_seen: dict[str, ChannelVersions]

```

Map from node ID to map from channel name to version seen.

This keeps track of the versions of the channels that each node has seen. Used to determine which nodes to execute next.

###

BaseCheckpointSaver



Bases:

`Generic[V]`

Base class for creating a graph checkpointer.

Checkpointers allow LangGraph agents to persist their state within and across multiple interactions.

When a checkpointer is configured, you should pass a

`thread_id` in the config when

invoking the graph:
```

config = {"configurable": {"thread_id": "my-thread"}}

graph.invoke(inputs, config)

```

The

`thread_id` is the primary key used to store and retrieve checkpoints. Without

it, the checkpointer cannot save state, resume from interrupts, or enable

time-travel debugging.

…

|METHOD|DESCRIPTION|
|--|--|
|`get`|Fetch a checkpoint using the given configuration.|
|`get_tuple`|Fetch a checkpoint tuple using the given configuration.|
|`list`|List checkpoints that match the given criteria.|
|`put`|Store a checkpoint with its configuration and metadata.|
|`put_writes`|Store intermediate writes linked to a checkpoint.|
|`delete_thread`|Delete all checkpoints and writes associated with a specific thread ID.|
|`aget`|Asynchronously fetch a checkpoint using the given configuration.|
|`aget_tuple`|Asynchronously fetch a checkpoint tuple using the given configuration.|
|`alist`|Asynchronously list checkpoints that match the given criteria.|
|`aput`|Asynchronously store a checkpoint with its configuration and metadata.|
|`aput_writes`|Asynchronously store intermediate writes linked to a checkpoint.|
|`adelete_thread`|Delete all checkpoints and writes associated with a specific thread ID.|
|`get_next_version`|Generate the next version ID for a channel.|

####

config_specs

`property`



```

config_specs: list

```

Define the configuration options for the checkpoint saver.

|RETURNS|DESCRIPTION|
|--|--|
|`list`|List of configuration field specs.|
####

get



```

get(config: RunnableConfig) -> Checkpoint | None

```

Fetch a checkpoint using the given configuration.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration specifying which checkpoint to retrieve.|
|RETURNS|DESCRIPTION|
|--|--|
|`Checkpoint | None`|The requested checkpoint, or|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Base configuration for filtering checkpoints.|
|`filter`|Additional filtering criteria.|
|`before`|List checkpoints created before this configuration.|
|`limit`|Maximum number of checkpoints to return.|
|RETURNS|DESCRIPTION|
|--|--|
|`Iterator[CheckpointTuple]`|Iterator of matching checkpoint tuples.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration for the checkpoint.|
|`checkpoint`|The checkpoint to store.|
|`metadata`|Additional metadata for the checkpoint.|
|`new_versions`|New channel versions as of this write.|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|Updated configuration after storing the checkpoint.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration of the related checkpoint.|
|`writes`|List of writes to store.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Base configuration for filtering checkpoints.|
|`filter`|Additional filtering criteria for metadata.|
|`before`|List checkpoints created before this configuration.|
|`limit`|Maximum number of checkpoints to return.|
|RETURNS|DESCRIPTION|
|--|--|
|`AsyncIterator[CheckpointTuple]`|Async iterator of matching checkpoint tuples.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration for the checkpoint.|
|`checkpoint`|The checkpoint to store.|
|`metadata`|Additional metadata for the checkpoint.|
|`new_versions`|New channel versions as of this write.|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|Updated configuration after storing the checkpoint.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration of the related checkpoint.|
|`writes`|List of writes to store.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

`float` versions, as long as they are monotonically increasing.

|PARAMETER|DESCRIPTION|
|--|--|
|`current`|The current version identifier (|
|`channel`|Deprecated argument, kept for backwards compatibility.|
|RETURNS|DESCRIPTION|
|--|--|
|`V`|The next version identifier, which must be increasing.|

###

create_checkpoint



```

create_checkpoint(

checkpoint: Checkpoint,

channels: Mapping[str, ChannelProtocol] | None,

step: int,

*,

id: str | None = None,

) -> Checkpoint

```

Create a checkpoint for the given channels.

…

###

CipherProtocol



Bases:

`Protocol`

Protocol for encryption and decryption of data.

`encrypt`: Encrypt plaintext.

`decrypt`: Decrypt ciphertext.

|METHOD|DESCRIPTION|
|--|--|
|`encrypt`|Encrypt plaintext. Returns a tuple|
|`decrypt`|Decrypt ciphertext. Returns the plaintext.|

…

|METHOD|DESCRIPTION|
|--|--|
|`get_tuple`|Get a checkpoint tuple from the in-memory storage.|
|`list`|List checkpoints from the in-memory storage.|
|`put`|Save a checkpoint to the in-memory storage.|
|`put_writes`|Save a list of writes to the in-memory storage.|
|`delete_thread`|Delete all checkpoints and writes associated with a thread ID.|
|`aget_tuple`|Asynchronous version of|
|`alist`|Asynchronous version of|
|`aput`|Asynchronous version of|
|`aput_writes`|Asynchronous version of|
|`adelete_thread`|Delete all checkpoints and writes associated with a thread ID.|
|`get_next_version`|Generate the next version ID for a channel.|
|`get`|Fetch a checkpoint using the given configuration.|
|`aget`|Asynchronously fetch a checkpoint using the given configuration.|

…

the matching thread ID and timestamp is retrieved. Otherwise, the latest checkpoint

for the given thread ID is retrieved.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to use for retrieving the checkpoint.|
|RETURNS|DESCRIPTION|
|--|--|
|`CheckpointTuple | None`|The retrieved checkpoint tuple, or None if no matching checkpoint was found.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Base configuration for filtering checkpoints.|
|`filter`|Additional filtering criteria for metadata.|
|`before`|List checkpoints created before this configuration.|
|`limit`|Maximum number of checkpoints to return.|
|YIELDS|DESCRIPTION|
|--|--|
|`CheckpointTuple`|An iterator of matching checkpoint tuples.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to associate with the checkpoint.|
|`checkpoint`|The checkpoint to save.|
|`metadata`|Additional metadata to save with the checkpoint.|
|`new_versions`|New versions as of this write|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|The updated config containing the saved checkpoint's timestamp.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to associate with the writes.|
|`writes`|The writes to save.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|The updated config containing the saved writes' timestamp.|

…

`list`.

This method is an asynchronous wrapper around

`list` that runs the synchronous

method in a separate thread using asyncio.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to use for listing the checkpoints.|
|YIELDS|DESCRIPTION|
|--|--|
|`AsyncIterator[CheckpointTuple]`|An asynchronous iterator of checkpoint tuples.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to associate with the checkpoint.|
|`checkpoint`|The checkpoint to save.|
|`metadata`|Additional metadata to save with the checkpoint.|
|`new_versions`|New versions as of this write|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|The updated config containing the saved checkpoint's timestamp.|

…

`put_writes` that runs the synchronous

method in a separate thread using asyncio.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to associate with the writes.|
|`writes`|The writes to save, each as a (channel, value) pair.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|
|RETURNS|DESCRIPTION|
|--|--|
|`None`|None|

…

`float` versions, as long as they are monotonically increasing.

|PARAMETER|DESCRIPTION|
|--|--|
|`current`|The current version identifier (|
|`channel`|Deprecated argument, kept for backwards compatibility.|
|RETURNS|DESCRIPTION|
|--|--|
|`V`|The next version identifier, which must be increasing.|

####

get



```

get(config: RunnableConfig) -> Checkpoint | None

```

Fetch a checkpoint using the given configuration.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration specifying which checkpoint to retrieve.|
|RETURNS|DESCRIPTION|
|--|--|
|`Checkpoint | None`|The requested checkpoint, or|

…

|`list`|List checkpoints from the database.|
|`put`|Save a checkpoint to the database.|
|`put_writes`|Store intermediate writes linked to a checkpoint.|
|`delete_thread`|Delete all checkpoints and writes associated with a thread ID.|
|`aget_tuple`|Get a checkpoint tuple from the database asynchronously.|
|`alist`|List checkpoints from the database asynchronously.|
|`aput`|Save a checkpoint to the database asynchronously.|
|`get_next_version`|Generate the next version ID for a channel.|
|`get`|Fetch a checkpoint using the given configuration.|
|`aget`|Asynchronously fetch a checkpoint using the given configuration.|
|`aput_writes`|Asynchronously store intermediate writes linked to a checkpoint.|
|`adelete_thread`|Delete all checkpoints and writes associated with a specific thread ID.|

…

for the given thread ID is retrieved.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to use for retrieving the checkpoint.|
|RETURNS|DESCRIPTION|
|--|--|
|`CheckpointTuple | None`|The retrieved checkpoint tuple, or None if no matching checkpoint was found.|
Examples:

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to use for listing the checkpoints.|
|`filter`|Additional filtering criteria for metadata.|
|`before`|If provided, only checkpoints before the specified checkpoint ID are returned.|
|`limit`|The maximum number of checkpoints to return.|
|YIELDS|DESCRIPTION|
|--|--|
|`CheckpointTuple`|An iterator of checkpoint tuples.|
Examples:

```

>>> from langgraph.checkpoint.sqlite import SqliteSaver

>>> with SqliteSaver.from_conn_string(":memory:") as memory:

... # Run a graph, then list the checkpoints

>>> config = {"configurable": {"thread_id": "1"}}

>>> checkpoints = list(memory.list(config, limit=2))

>>> print(checkpoints)

[CheckpointTuple(...), CheckpointTuple(...)]

```

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to associate with the checkpoint.|
|`checkpoint`|The checkpoint to save.|
|`metadata`|Additional metadata to save with the checkpoint.|
|`new_versions`|New channel versions as of this write.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration of the related checkpoint.|
|`writes`|List of writes to store, each as (channel, value) pair.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|

…

####

get



```

get(config: RunnableConfig) -> Checkpoint | None

```

Fetch a checkpoint using the given configuration.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration specifying which checkpoint to retrieve.|
|RETURNS|DESCRIPTION|
|--|--|
|`Checkpoint | None`|The requested checkpoint, or|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration of the related checkpoint.|
|`writes`|List of writes to store.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

|`put_writes`|Store intermediate writes linked to a checkpoint.|
|`delete_thread`|Delete all checkpoints and writes associated with a thread ID.|
|`setup`|Set up the checkpoint database asynchronously.|
|`aget_tuple`|Get a checkpoint tuple from the database asynchronously.|
|`alist`|List checkpoints from the database asynchronously.|
|`aput`|Save a checkpoint to the database asynchronously.|
|`aput_writes`|Store intermediate writes linked to a checkpoint asynchronously.|
|`adelete_thread`|Delete all checkpoints and writes associated with a thread ID.|
|`get_next_version`|Generate the next version ID for a channel.|
|`get`|Fetch a checkpoint using the given configuration.|
|`aget`|Asynchronously fetch a checkpoint using the given configuration.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Base configuration for filtering checkpoints.|
|`filter`|Additional filtering criteria for metadata.|
|`before`|If provided, only checkpoints before the specified checkpoint ID are returned.|
|`limit`|Maximum number of checkpoints to return.|
|YIELDS|DESCRIPTION|
|--|--|
|`CheckpointTuple`|An iterator of matching checkpoint tuples.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to associate with the checkpoint.|
|`checkpoint`|The checkpoint to save.|
|`metadata`|Additional metadata to save with the checkpoint.|
|`new_versions`|New channel versions as of this write.|
|RETURNS|DESCRIPTION|
|--|--|
|`RunnableConfig`|Updated configuration after storing the checkpoint.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration of the related checkpoint.|
|`writes`|List of writes to store.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|
|RAISES|DESCRIPTION|
|--|--|
|`NotImplementedError`|Implement this method in your custom checkpoint saver.|

…

the matching thread ID and checkpoint ID is retrieved. Otherwise, the latest checkpoint

for the given thread ID is retrieved.

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|The config to use for retrieving the checkpoint.|
|RETURNS|DESCRIPTION|
|--|--|
|`CheckpointTuple | None`|The retrieved checkpoint tuple, or None if no matching checkpoint was found.|

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Base configuration for filtering checkpoints.|
|`filter`|Additional filtering criteria for metadata.|
|`before`|If provided, only checkpoints before the specified checkpoint ID are returned.|
|`limit`|Maximum number of checkpoints to return.|

LangGraph has a built-in persistence layer that saves graph state as checkpoints. When you compile a graph with a checkpointer, a snapshot of the graph state is saved at every step of execution, organized into threads. This enables human-in-the-loop workflows, conversational memory, time travel debugging, and fault-tolerant execution.
**Agent Server handles checkpointing automatically** When using the Agent Server, you don’t need to implement or configure checkpointers manually. The server handles all persistence infrastructure for you behind the scenes.

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
After we run the graph, we expect to see exactly 4 checkpoints: - Empty checkpoint with `START` as the next node to be executed
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

…

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

- `.list` - List checkpoints that match a given configuration and filter criteria. This is used to populate state history in `graph.get_state_history()`
If the checkpointer is used with asynchronous graph execution (i.e. executing the graph via `.ainvoke`, `.astream`, `.abatch`), asynchronous versions of the above methods will be used (`.aput`, `.aput_writes`, `.aget_tuple`, `.alist`).

```
import { MCPClient } from 'langgraph-mcp';
const client = new MCPClient({ endpoint: 'https://mcp.langgraph.com' });
client.connect()
.then(() => client.callTool('tool_name', { param: 'value' }))
.then(response => console.log(response))
.catch(error => console.error(error));
```
…
## Objectives of the Article
The primary goal of this article is to provide a comprehensive guide on implementing LangGraph checkpointing using the latest practices as of 2025.
We will cover:
- **Code snippets** for setting up LangGraph checkpointing.
- Architectural diagrams illustrating checkpoint integration.
- Examples of integrating vector databases like Pinecone and Weaviate.
- Working implementations of the MCP protocol and tool calling patterns.
- Memory management and multi-turn conversation handling in AI applications.
…
## Architecture Diagram
The architecture of a LangGraph application with checkpointing typically involves a workflow engine, a durable database backend for checkpoint storage, and interfaces for monitoring and debugging.
The diagram (not included here) shows how these components interact to provide a seamless developer experience.
…
### Analysis Process
To evaluate LangGraph checkpointing, we implemented various use-cases using LangChain, AutoGen, and CrewAI frameworks.
We focused on the integration of vector databases such as Pinecone and Weaviate to enhance data retrieval and management capabilities.
Critical attention was given to the implementation of MCP protocols and memory management techniques.
The analysis included constructing multi-turn conversation handling and agent orchestration patterns using real-world scenarios.
…
...
Our architecture diagrams illustrate the flow of data and control within the LangGraph checkpointing system.
These include components such as the vector database integration layer, MCP protocol handlers, and tool calling orchestrators, ensuring clear visualization of the comprehensive system setup.
This HTML code provides a detailed methodology section with practical examples, focusing on the technical aspects of implementing LangGraph checkpointing for developers.
It includes code snippets, architectural explanations, and evaluation criteria, aligning with the current best practices.
## Implementation of LangGraph Checkpointing
This section provides a step-by-step guide to implementing LangGraph checkpointing, with sample code and architectures.
It highlights common pitfalls and offers troubleshooting tips to ensure a smooth integration into your application.
### Step-by-Step Guide to Implementing LangGraph Checkpointing
Follow these steps to integrate LangGraph checkpointing into your development workflow:
1. **Set Up Your Environment:** Ensure your Python environment is set up with the required libraries, including `langgraph-checkpoint-postgres` and `psycopg_pool` for Postgres integration.
2. **Initialize PostgresSaver:** Use the `PostgresSaver` class to create a durable checkpointing backend.
3. **Integrate with LangGraph:** Connect your LangGraph processes to the Postgres backend to manage state persistence.
…
### Tools for Monitoring and Evaluation
LangChain, AutoGen, CrewAI, and LangGraph provide integrated tools for monitoring and evaluating checkpointing implementations.
Using these frameworks, developers can track checkpoint creation, validate data integrity, and observe performance impacts.
For instance, developers can employ the following code to manage memory and facilitate multi-turn conversation handling:

1 Two Basic Streaming Response Techniques of LangGraph 2 Advanced Features of LangGraph: Summary and Considerations ...
5 more parts...
3 Building Complex AI Workflows with LangGraph: A Detailed Explanation of Subgraph Architecture 4 Checkpoints and Human-Computer Interaction in LangGraph 5 Advanced Techniques in LangGraph: Tips for Using Message Deletion in Graph Structure Applications 6 Advanced LangGraph: Building Intelligent Agents with ReACT Architecture 7 Advanced LangGraph: Implementing Conditional Edges and Tool-Calling Agents 8 Introduction to LangGraph: Core Concepts and Basic Components 9 Analysis of Limitations of LCEL and AgentExecutor
## I.
Checkpoint Mechanism in LangGraph
The checkpoint mechanism is a powerful feature in LangGraph that allows us to pause processing at specific points in the graph execution, save the state, and resume when needed.
### 1.1 Basic Concept of Checkpoints
A checkpoint is essentially a snapshot during the graph execution process that contains the current state information.
This is particularly useful for long-running tasks, processes requiring human intervention, or applications needing resumable execution.
### 1.2 Creating Checkpoints
In LangGraph, we can use the `create_checkpoint` function to create checkpoints:
```
from langgraph.checkpoint import create_checkpoint
def process_with_checkpoint(state):
# Processing logic
# ...
# Create a checkpoint
checkpoint = create_checkpoint(state)
return {"checkpoint": checkpoint, "state": state}
graph.add_node("process", process_with_checkpoint)
```
### 1.3 Restoring Checkpoints
Use the `load_checkpoint` function to restore previously saved checkpoints:
```
from langgraph.checkpoint import load_checkpoint
def resume_from_checkpoint(checkpoint):
state = load_checkpoint(checkpoint)
# Continue processing
# ...
return state
graph.add_node("resume", resume_from_checkpoint)
```
…
```
from langgraph.prebuilt import ToolMessage, HumanMessage
from langgraph.checkpoint import create_checkpoint, load_checkpoint
def process_query(state):
# Process user query
# ...
state['confidence'] = calculate_confidence(state)
return state
def human_intervention(state):
print("Current conversation:", state['messages'])
human_response = input("Please provide assistance: ")
state['messages'].append(HumanMessage(content=human_response))
return state
def summarize_and_prune(state):
# Summarize conversation
summary = summarize_conversation(state['messages'])
# Retain latest messages and summary
new_messages = state['messages'][-5:]
new_messages.append(ToolMessage(content=summary))
state['messages'] = new_messages
# Create checkpoint
checkpoint = create_checkpoint(state)
state['checkpoint'] = checkpoint
return state
graph = Graph()
graph.add_node("process_query", process_query)
graph.add_node("human_intervention", human_intervention)
graph.add_node("summarize_and_prune", summarize_and_prune)
graph.add_conditional_edges("process_query", {
"human_intervention": lambda s: s['confidence'] < 0.8,
"summarize_and_prune": lambda s: s['confidence'] >= 0.8
})
graph.add_edge("human_intervention", "summarize_and_prune")
graph.add_edge("summarize_and_prune", "process_query")
```
…
## Summary
The checkpoint mechanism and human-computer interaction features of LangGraph provide powerful tools for building complex and reliable AI systems.
By using these features wisely, we can create more intelligent, flexible, and controllable applications.
Checkpoints allow us to save and restore states in long-running tasks, while human interaction introduces human judgment and expertise into the AI decision-making process.
In practical applications, the combination of these features can significantly enhance system performance and reliability.
## LangGraph Advanced Tutorial (9 Part Series)

# Persistence

LangGraph has a built-in persistence layer, implemented through checkpointers. When you compile a graph with a checkpointer, the checkpointer saves a `checkpoint` of the graph state at every super-step. Those checkpoints are saved to a `thread`, which can be accessed after graph execution. Because `threads` allow access to graph's state after execution, several powerful capabilities including human-in-the-loop, memory, time travel, and fault-tolerance are all possible. Below, we'll discuss each of these concepts in more detail.

…

## Checkpoints

The state of a thread at a particular point in time is called a checkpoint. Checkpoint is a snapshot of the graph state saved at each super-step and is represented by `StateSnapshot` object with the following key properties:
- `config`: Config associated with this checkpoint.
- `metadata`: Metadata associated with this checkpoint.
- `values`: Values of the state channels at this point in time.
- `next` A tuple of the node names to execute next in the graph.
- `tasks`: A tuple of `PregelTask` objects that contain information about next tasks to be executed. If the step was previously attempted, it will include error information. If a graph was interrupted dynamically from within a node, tasks will contain additional data associated with interrupts.
Checkpoints are persisted and can be used to restore the state of a thread at a later time.

Let's see what checkpoints are saved when a simple graph is invoked as follows:
```
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
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

config = {"configurable": {"thread_id": "1"}}
graph.invoke({"foo": ""}, config)
```

…

- empty checkpoint with `START` as the next node to be executed
- checkpoint with the user input `{'foo': '', 'bar': []}` and `node_a` as the next node to be executed
- checkpoint with the outputs of `node_a` `{'foo': 'a', 'bar': ['a']}` and `node_b` as the next node to be executed
- checkpoint with the outputs of `node_b` `{'foo': 'b', 'bar': ['a', 'b']}` and no next nodes to be executed

Note that the `bar` channel values contain outputs from both nodes as we have a reducer for `bar` channel.

…

In our example, the output of `get_state` will look like this:
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

### Get state history

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
        values={'foo': 'a', 'bar': ['a']}, next=('node_b',),
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

…

Importantly, LangGraph knows whether a particular step has been executed previously. If it has, LangGraph simply *re-plays* that particular step in the graph and does not re-execute the step, but only for the steps *before* the provided `checkpoint_id`. All of the steps *after* `checkpoint_id` will be executed (i.e., a new fork), even if they have been executed previously. See this how to guide on time-travel to learn more about replaying .

…

## Checkpointer libraries

Under the hood, checkpointing is powered by checkpointer objects that conform to [BaseCheckpointSaver][langgraph.checkpoint.base.BaseCheckpointSaver] interface. LangGraph provides several checkpointer implementations, all implemented via standalone, installable libraries:

…

- `.put` - Store a checkpoint with its configuration and metadata.
- `.put_writes` - Store intermediate writes linked to a checkpoint (i.e. pending writes ).
- `.get_tuple` - Fetch a checkpoint tuple using for a given configuration (`thread_id` and `checkpoint_id`). This is used to populate `StateSnapshot` in `graph.get_state()`.
- `.list` - List checkpoints that match a given configuration and filter criteria. This is used to populate state history in `graph.get_state_history()`

If the checkpointer is used with asynchronous graph execution (i.e. executing the graph via `.ainvoke`, `.astream`, `.abatch`), asynchronous versions of the above methods will be used (`.aput`, `.aput_writes`, `.aget_tuple`, `.alist`).

…

## Capabilities

### Human-in-the-loop

First, checkpointers facilitate human-in-the-loop workflows workflows by allowing humans to inspect, interrupt, and approve graph steps. Checkpointers are needed for these workflows as the human has to be able to view the state of a graph at any point in time, and the graph has to be to resume execution after the human has made any updates to the state. See the how-to guides for examples.

…

### Time Travel

Third, checkpointers allow for "time travel" , allowing users to replay prior graph executions to review and / or debug specific graph steps. In addition, checkpointers make it possible to fork the graph state at arbitrary checkpoints to explore alternative trajectories.

### Fault-tolerance

Lastly, checkpointing also provides fault-tolerance and error recovery: if one or more nodes fail at a given superstep, you can restart your graph from the last successful step. Additionally, when a graph node fails mid-execution at a given superstep, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that superstep, so that whenever we resume graph execution from that superstep we don't re-run the successful nodes.