# Source: https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list
# Title: BaseCheckpointSaver.list | @langchain/langgraph-checkpoint (JavaScript reference)
# Fetched via: search
# Date: 2026-04-10

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
configurable: {
thread_id: "1"
};
const checkpointer = new MemorySaver();
const checkpoint = {
v: 1,
ts: "2024-07-31T20:14:19.804150+00:00",
id: "1ef4f797-8335-6428-8001-8a1503f9b875",
channel_values: {
my_key: "meow",
node: "node"
},
channel_versions: {
__start__: 2,
my_key: 3,
"start:node": 3,
node: 3
},
versions_seen: {
__input__: {},
__start__: {
__start__: 1
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

####

from_pycryptodome_aes

`classmethod`



```

from_pycryptodome_aes(

serde: SerializerProtocol = JsonPlusSerializer(), **kwargs: Any

) -> EncryptedSerializer

```

Create an

`EncryptedSerializer` using AES encryption.

##

memory



###

InMemorySaver



Bases:

`BaseCheckpointSaver[str]`,

`AbstractContextManager`,

`AbstractAsyncContextManager`

An in-memory checkpoint saver.

This checkpoint saver stores checkpoints in memory using a

`defaultdict`.

## Note

Only use

`InMemorySaver` for debugging or testing purposes.

For production use cases we recommend installing langgraph-checkpoint-postgres and using

`PostgresSaver` /

`AsyncPostgresSaver`.

If you are using LangSmith Deployment, no checkpointer needs to be specified. The correct managed checkpointer will be used automatically.

|PARAMETER|DESCRIPTION|
|--|--|
|`serde`|The serializer to use for serializing and deserializing checkpoints.|

## Example

```

import asyncio

from langgraph.checkpoint.memory import InMemorySaver

from langgraph.graph import StateGraph

builder = StateGraph(int)

builder.add_node("add_one", lambda x: x + 1)

builder.set_entry_point("add_one")

builder.set_finish_point("add_one")

memory = InMemorySaver()

graph = builder.compile(checkpointer=memory)

coro = graph.ainvoke(1, {"configurable": {"thread_id": "thread-1"}})

asyncio.run(coro) # Output: 2

```
|METHOD|DESCRIPTION|
|--|--|
|`get_tuple`|Get a checkpoint tuple from the in-memory storage.|
|`list`|List checkpoints from the in-memory storage.|
|`put`|Save a checkpoint to the in-memory storage.|
|`put_writes`|Save a list of writes to the in-memory storage.|

…

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

## Note

This class is meant for lightweight, synchronous use cases

(demos and small projects) and does not

scale to multiple threads.

For a similar sqlite saver with

`async` support,

consider using AsyncSqliteSaver.

|PARAMETER|DESCRIPTION|
|--|--|
|`conn`|The SQLite database connection.|
|`serde`|The serializer to use for serializing and deserializing checkpoints. Defaults to JsonPlusSerializerCompat.|
Examples:

…

>>> # Create a new SqliteSaver instance

>>> # Note: check_same_thread=False is OK as the implementation uses a lock

>>> # to ensure thread safety.

>>> conn = sqlite3.connect("checkpoints.sqlite", check_same_thread=False)

>>> memory = SqliteSaver(conn)

>>> graph = builder.compile(checkpointer=memory)

…

|METHOD|DESCRIPTION|
|--|--|
|`from_conn_string`|Create a new SqliteSaver instance from a connection string.|
|`setup`|Set up the checkpoint database.|
|`cursor`|Get a cursor for the SQLite database.|
|`get_tuple`|Get a checkpoint tuple from the database.|
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

…

```

In memory:

with SqliteSaver.from_conn_string(":memory:") as memory:

...

To disk:

with SqliteSaver.from_conn_string("checkpoints.sqlite") as memory:

...

```

####

setup



```

setup() -> None

```

Set up the checkpoint database.

This method creates the necessary tables in the SQLite database if they don't already exist. It is called automatically when needed and should not be called directly by the user.

…

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
```

>>> config = {"configurable": {"thread_id": "1"}}

>>> before = {"configurable": {"checkpoint_id": "1ef4f797-8335-6428-8001-8a1503f9b875"}}

>>> with SqliteSaver.from_conn_string(":memory:") as memory:

... # Run a graph, then list the checkpoints

>>> checkpoints = list(memory.list(config, before=before))

>>> print(checkpoints)

[CheckpointTuple(...), ...]

```

…

|PARAMETER|DESCRIPTION|
|--|--|
|`config`|Configuration of the related checkpoint.|
|`writes`|List of writes to store, each as (channel, value) pair.|
|`task_id`|Identifier for the task creating the writes.|
|`task_path`|Path of the task creating the writes.|

…

## Note

This async method is not supported by the SqliteSaver class. Use list() instead, or consider using AsyncSqliteSaver.

####

aput

`async`



```

aput(

config: RunnableConfig,

checkpoint: Checkpoint,

metadata: CheckpointMetadata,

new_versions: ChannelVersions,

) -> RunnableConfig

```

Save a checkpoint to the database asynchronously.

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

##

aio



###

AsyncSqliteSaver



Bases:

`BaseCheckpointSaver[str]`

An asynchronous checkpoint saver that stores checkpoints in a SQLite database.

This class provides an asynchronous interface for saving and retrieving checkpoints using a SQLite database. It's designed for use in asynchronous environments and offers better performance for I/O-bound operations compared to synchronous alternatives.

|ATTRIBUTE|DESCRIPTION|
|--|--|
|`conn`|The asynchronous SQLite database connection.|
|`serde`|The serializer used for encoding/decoding checkpoints.|

…

```

async with AsyncSqliteSaver.from_conn_string("checkpoints.sqlite") as saver:

# Your code here

graph = builder.compile(checkpointer=saver)

config = {"configurable": {"thread_id": "thread-1"}}

async for event in graph.astream_events(..., config, version="v1"):

print(event)

```

…

... checkpoint = {"ts": "2023-05-03T10:00:00Z", "data": {"key": "value"}, "id": "0c62ca34-ac19-445d-bbb0-5b4984975b2a"}

... saved_config = await saver.aput(config, checkpoint, {}, {})

... print(saved_config)

>>> asyncio.run(main())

{'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '0c62ca34-ac19-445d-bbb0-5b4984975b2a'}}

```
|METHOD|DESCRIPTION|
|--|--|
|`from_conn_string`|Create a new AsyncSqliteSaver instance from a connection string.|
|`get_tuple`|Get a checkpoint tuple from the database.|
|`list`|List checkpoints from the database asynchronously.|
|`put`|Save a checkpoint to the database.|
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

# @langchain/langgraph-checkpoint
This library defines the base interface for LangGraph.js checkpointers.
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
When using a checkpointer, you must specify a `thread_id` and optionally `checkpoint_id` when running the graph.
- `thread_id` is simply the ID of a thread.
This is always required
- `checkpoint_id` can optionally be passed.
This identifier refers to a specific checkpoint within a thread.
This can be used to kick of a run of a graph from some point halfway through a thread.
You must pass these when invoking the graph as part of the configurable part of the config, e.g.
```
{ configurable: { thread_id: "1" } } // valid config
{ configurable: { thread_id: "1", checkpoint_id: "0c62ca34-ac19-445d-bbb0-5b4984975b2a" } } // also valid config
```
### Serde
`@langchain/langgraph-checkpoint` also defines protocol for serialization/deserialization (serde) and provides an default implementation that handles a range of types.
### Pending writes
When a graph node fails mid-execution at a given superstep, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that superstep, so that whenever we resume graph execution from that superstep we don't re-run the successful nodes.
## Interface
Each checkpointer should conform to `BaseCheckpointSaver` interface and must implement the following methods:
- `.put` - Store a checkpoint with its configuration and metadata.
- `.putWrites` - Store intermediate writes linked to a checkpoint (i.e. pending writes).
- `.getTuple` - Fetch a checkpoint tuple using for a given configuration (`thread_id` and `thread_ts`).
- `.list` - List checkpoints that match a given configuration and filter criteria.
## Usage
```
import { MemorySaver } from "@langchain/langgraph-checkpoint";
const writeConfig = {
configurable: {
thread_id: "1",
checkpoint_ns: ""
}
};
const readConfig = {
configurable: {
thread_id: "1"
}
};
const checkpointer = new MemorySaver();
const checkpoint = {
v: 1,
ts: "2024-07-31T20:14:19.804150+00:00",
id: "1ef4f797-8335-6428-8001-8a1503f9b875",
channel_values: {
my_key: "meow",
node: "node"
},
channel_versions: {
__start__: 2,
my_key: 3,
"start:node": 3,
node: 3
},
versions_seen: {
__input__: {},
__start__: {
__start__: 1
},
node: {
"start:node": 2
}
},
pending_sends: [],
}
// store checkpoint
await checkpointer.put(writeConfig, checkpoint, {}, {})
// load checkpoint
await checkpointer.get(readConfig)
// list checkpoints
for await (const checkpoint of checkpointer.list(readConfig)) {
console.log(checkpoint);
}
```

# @langchain/langgraph-checkpoint
This library defines the base interface for LangGraph.js checkpointers.
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
When using a checkpointer, you must specify a `thread_id` and optionally `checkpoint_id` when running the graph.
- `thread_id` is simply the ID of a thread.
This is always required
- `checkpoint_id` can optionally be passed.
This identifier refers to a specific checkpoint within a thread.
This can be used to kick of a run of a graph from some point halfway through a thread.
You must pass these when invoking the graph as part of the configurable part of the config, e.g.
```
{ configurable: { thread_id: "1" } } // valid config
{ configurable: { thread_id: "1", checkpoint_id: "0c62ca34-ac19-445d-bbb0-5b4984975b2a" } } // also valid config
```
### Serde
`@langchain/langgraph-checkpoint` also defines protocol for serialization/deserialization (serde) and provides an default implementation that handles a range of types.
### Pending writes
When a graph node fails mid-execution at a given superstep, LangGraph stores pending checkpoint writes from any other nodes that completed successfully at that superstep, so that whenever we resume graph execution from that superstep we don't re-run the successful nodes.
## Interface
Each checkpointer should conform to `BaseCheckpointSaver` interface and must implement the following methods:
- `.put` - Store a checkpoint with its configuration and metadata.
- `.putWrites` - Store intermediate writes linked to a checkpoint (i.e. pending writes).
- `.getTuple` - Fetch a checkpoint tuple using for a given configuration (`thread_id` and `thread_ts`).
- `.list` - List checkpoints that match a given configuration and filter criteria.
## Usage
```
import { MemorySaver } from "@langchain/langgraph-checkpoint";
const writeConfig = {
configurable: {
thread_id: "1",
checkpoint_ns: ""
}
};
const readConfig = {
configurable: {
thread_id: "1"
}
};
const checkpointer = new MemorySaver();
const checkpoint = {
v: 1,
ts: "2024-07-31T20:14:19.804150+00:00",
id: "1ef4f797-8335-6428-8001-8a1503f9b875",
channel_values: {
my_key: "meow",
node: "node"
},
channel_versions: {
__start__: 2,
my_key: 3,
"start:node": 3,
node: 3
},
versions_seen: {
__input__: {},
__start__: {
__start__: 1
},
node: {
"start:node": 2
}
},
pending_sends: [],
}
// store checkpoint
await checkpointer.put(writeConfig, checkpoint, {}, {})
// load checkpoint
await checkpointer.get(readConfig)
// list checkpoints
for await (const checkpoint of checkpointer.list(readConfig)) {
console.log(checkpoint);
}
```

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
…
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
configurable: {
thread_id: "1"
};
const checkpointer = new MemorySaver();
const checkpoint = {
v: 1,
ts: "2024-07-31T20:14:19.804150+00:00",
id: "1ef4f797-8335-6428-8001-8a1503f9b875",
channel_values: {
my_key: "meow",
node: "node"
},
channel_versions: {
__start__: 2,
my_key: 3,
"start:node": 3,
node: 3
},
versions_seen: {
__input__: {},
__start__: {
__start__: 1
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