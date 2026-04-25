# Source: https://reference.langchain.com/python/langgraph/types/
# Title: Types | LangChain Reference (LangGraph)
# Fetched via: search
# Date: 2026-04-10

# Types

##

types



|FUNCTION|DESCRIPTION|
|--|--|
|`interrupt`|Interrupt the graph with a resumable exception from within a node.|
###

All

`module-attribute`



```

All = Literal['*']

```

Special value to indicate that graph should interrupt on all nodes.

###

Checkpointer

`module-attribute`



```

Checkpointer = None | bool | BaseCheckpointSaver

```

Type of the checkpointer to use for a subgraph.

`True`enables persistent checkpointing for this subgraph.

`False`disables checkpointing, even if the parent graph has a checkpointer.

`None`inherits checkpointer from the parent graph.

###

StreamMode

`module-attribute`



```

StreamMode = Literal[

"values", "updates", "checkpoints", "tasks", "debug", "messages", "custom"



```

How the stream method should emit outputs.

`"values"`: Emit all values in the state after each step, including interrupts. When used with functional API, values are emitted once at the end of the workflow.
`"updates"`: Emit only the node or task names and updates returned by the nodes or tasks after each step. If multiple updates are made in the same step (e.g. multiple nodes are run) then those updates are emitted separately.

`"custom"`: Emit custom data using from inside nodes or tasks using
`StreamWriter`.

`"messages"`: Emit LLM messages token-by-token together with metadata for any LLM invocations inside nodes or tasks.

`"checkpoints"`: Emit an event when a checkpoint is created, in the same format as returned by

`get_state()`.

`"tasks"`: Emit events when tasks start and finish, including their results and errors.

`"debug"`: Emit

`"checkpoints"`and

`"tasks"`events for debugging purposes.

###

StreamWriter

`module-attribute`



```

StreamWriter = Callable[[Any], None]

```

`Callable` that accepts a single argument and writes it to the output stream.

Always injected into nodes if requested as a keyword argument, but it's a no-op

when not using

`stream_mode="custom"`.

###

RetryPolicy



Bases:

`NamedTuple`

Configuration for retrying nodes.

Added in version 0.2.24

####

initial_interval

`class-attribute`

`instance-attribute`



```

initial_interval: float = 0.5

```

Amount of time that must elapse before the first retry occurs. In seconds.

####

backoff_factor

`class-attribute`

`instance-attribute`



```

backoff_factor: float = 2.0

```

Multiplier by which the interval increases after each retry.

####

max_interval

`class-attribute`

`instance-attribute`



```

max_interval: float = 128.0

```

Maximum amount of time that may elapse between retries. In seconds.

####

max_attempts

`class-attribute`

`instance-attribute`



```

max_attempts: int = 3

```

Maximum number of attempts to make before giving up, including the first.

####

jitter

`class-attribute`

`instance-attribute`



```

jitter: bool = True

```

Whether to add random jitter to the interval between retries.

###

CachePolicy

`dataclass`



Bases:

`Generic[KeyFuncT]`

Configuration for caching nodes.

####

key_func

`class-attribute`

`instance-attribute`



```

key_func: KeyFuncT = default_cache_key

```

Function to generate a cache key from the node's input. Defaults to hashing the input with pickle.

###

Interrupt

`dataclass`



Information about an interrupt that occurred in a node.

Added in version 0.2.24

Changed in version v0.4.0

`interrupt_id`was introduced as a property

Changed in version v0.6.0

The following attributes have been removed:

`ns`

`when`

`resumable`

`interrupt_id`, deprecated in favor of

`id`

###

PregelTask



Bases:

`NamedTuple`

A Pregel task.

###

StateSnapshot



Bases:

`NamedTuple`

Snapshot of the state of the graph at the beginning of a step.

####

next

`instance-attribute`



```

next: tuple[str, ...]

```

The name of the node to execute in each task for this step.

####

config

`instance-attribute`



```

config: RunnableConfig

```

Config used to fetch this snapshot.

####

metadata

`instance-attribute`



```

metadata: CheckpointMetadata | None

```

Metadata associated with this snapshot.

####

parent_config

`instance-attribute`



```

parent_config: RunnableConfig | None

```

Config used to fetch the parent snapshot, if any.

####

tasks

`instance-attribute`



```

tasks: tuple[PregelTask, ...]

```

Tasks to execute in this step. If already attempted, may contain an error.

###

Send



A message or packet to send to a specific node in the graph.

The

`Send` class is used within a

`StateGraph`'s conditional edges to

dynamically invoke a node with a custom state at the next step.

Importantly, the sent state can differ from the core graph's state, allowing for flexible and dynamic workflow management.
One such example is a "map-reduce" workflow where your graph invokes the same node multiple times in parallel with different states, before aggregating the results back into the main graph's state.

|ATTRIBUTE|DESCRIPTION|
|--|--|
|`node`|The name of the target node to send the message to.|
|`arg`|The state or message to send to the target node.|
Example
```

from typing import Annotated

from langgraph.types import Send

from langgraph.graph import END, START

from langgraph.graph import StateGraph

import operator

class OverallState(TypedDict):

subjects: list[str]

jokes: Annotated[list[str], operator.add]

def continue_to_jokes(state: OverallState):
return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]

builder = StateGraph(OverallState)

builder.add_node("generate_joke", lambda state: {"jokes": [f"Joke about {state['subject']}"]})

builder.add_conditional_edges(START, continue_to_jokes)
builder.add_edge("generate_joke", END)

graph = builder.compile()

# Invoking with two subjects results in a generated joke for each

graph.invoke({"subjects": ["cats", "dogs"]})

# {'subjects': ['cats', 'dogs'], 'jokes': ['Joke about cats', 'Joke about dogs']}

```

|METHOD|DESCRIPTION|
|--|--|
|`__init__`|Initialize a new instance of the|

###

Command

`dataclass`



Bases:

`Generic[N]`,

`ToolOutputMixin`

One or more commands to update the graph's state and send messages to nodes.

|PARAMETER|DESCRIPTION|
|--|--|
|`graph`|Graph to send the command to. Supported values are:|
|`update`|Update to apply to the graph's state.|
|`resume`|Value to resume execution with. To be used together with|
|`goto`|Can be one of the following:|

###

Overwrite

`dataclass`



Bypass a reducer and write the wrapped value directly to a

`BinaryOperatorAggregate` channel.

Receiving multiple

`Overwrite` values for the same channel in a single super-step

will raise an

`InvalidUpdateError`.

Example
```

from typing import Annotated

import operator

from langgraph.graph import StateGraph

from langgraph.types import Overwrite

class State(TypedDict):

messages: Annotated[list, operator.add]

def node_a(state: TypedDict):

# Normal update: uses the reducer (operator.add)

return {"messages": ["a"]}
def node_b(state: State):

# Overwrite: bypasses the reducer and replaces the entire value

return {"messages": Overwrite(value=["b"])}

builder = StateGraph(State)

builder.add_node("node_a", node_a)

builder.add_node("node_b", node_b)

builder.set_entry_point("node_a")
builder.add_edge("node_a", "node_b")

graph = builder.compile()

# Without Overwrite in node_b, messages would be ["START", "a", "b"]

# With Overwrite, messages is just ["b"]

result = graph.invoke({"messages": ["START"]})

assert result == {"messages": ["b"]}
```

###

interrupt



```

interrupt(value: Any) -> Any

```

Interrupt the graph with a resumable exception from within a node.

The

`interrupt` function enables human-in-the-loop workflows by pausing graph

execution and surfacing a value to the client. This value can communicate context

or request input required to resume execution.
In a given node, the first invocation of this function raises a

`GraphInterrupt`

exception, halting execution. The provided

`value` is included with the exception

and sent to the client executing the graph.

A client resuming the graph must use the

`Command`

primitive to specify a value for the interrupt and continue execution.
The graph resumes from the start of the node,

**re-executing** all logic.

If a node contains multiple

`interrupt` calls, LangGraph matches resume values

to interrupts based on their order in the node. This list of resume values

is scoped to the specific task executing the node and is not shared across tasks.
To use an

`interrupt`, you must enable a checkpointer, as the feature relies

on persisting the graph state.

Example
```

import uuid

from typing import Optional

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import InMemorySaver

from langgraph.constants import START

from langgraph.graph import StateGraph

from langgraph.types import interrupt, Command

class State(TypedDict):

"""The graph state."""

foo: str
human_value: Optional[str]

"""Human value will be updated using an interrupt."""

def node(state: State):

answer = interrupt(

# This value will be sent to the client

# as part of the interrupt information.

"what is your age?"



print(f"> Received an input from the interrupt: {answer}")
return {"human_value": answer}

builder = StateGraph(State)

builder.add_node("node", node)

builder.add_edge(START, "node")

# A checkpointer must be enabled for interrupts to work!

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)

config = {

"configurable": {
"thread_id": uuid.uuid4(),



for chunk in graph.stream({"foo": "abc"}, config):

print(chunk)

# > {'__interrupt__': (Interrupt(value='what is your age?', id='45fda8478b2ef754419799e10992af06'),)}

command = Command(resume="some input from a human!!!")
for chunk in graph.stream(Command(resume="some input from a human!!!"), config):

print(chunk)

# > Received an input from the interrupt: some input from a human!!!

# > {'node': {'human_value': 'some input from a human!!!'}}

```

|PARAMETER|DESCRIPTION|
|--|--|
|`value`|The value to surface to the client when the graph is interrupted.|
|RETURNS|DESCRIPTION|
|--|--|
|`Any`|On subsequent invocations within the same node (same task to be precise), returns the value provided during the first invocation|
|RAISES|DESCRIPTION|
|--|--|
|`GraphInterrupt`|On the first invocation within the node, halts execution and surfaces the provided value to the client.|

# LangGraph reference
Welcome to the LangGraph reference docs!
These pages detail the core interfaces you will use when building with LangGraph.
Each section covers a different part of the ecosystem.
##
`langgraph`¶
The core APIs for the LangGraph open source library.
- Graphs: Main graph abstraction and usage.
- Functional API: Functional programming interface for graphs.
- Pregel: Pregel-inspired computation model.
- Checkpointing: Saving and restoring graph state.
- Storage: Storage backends and options.
- Caching: Caching mechanisms for performance.
- Types: Type definitions for graph components.
- Runtime: Runtime configuration and options.
- Config: Configuration options.
- Errors: Error types and handling.
- Constants: Global constants.
- Channels: Message passing and channels.
Model Context Protocol (MCP) support
To use MCP tools in your LangGraph application, check out
`langchain-mcp-adapters`.

Welcome to the LangGraph reference docs!
These pages detail the core interfaces you will use when building with LangGraph.
Each section covers a different part of the ecosystem.
Tip
If you are just getting started, see LangGraph basics for an introduction to the main concepts and usage patterns.
## LangGraph¶
The core APIs for the LangGraph open source library.
- Graphs: Main graph abstraction and usage.
- Functional API: Functional programming interface for graphs.
- Pregel: Pregel-inspired computation model.
- Checkpointing: Saving and restoring graph state.
- Storage: Storage backends and options.
- Caching: Caching mechanisms for performance.
- Types: Type definitions for graph components.
- Config: Configuration options.
- Errors: Error types and handling.
- Constants: Global constants.
- Channels: Message passing and channels.
…
## LangGraph Platform¶

Course
Imagine you're building a complex, multi-agent large language model (LLM) application.
...
This is where LangGraph can help.
LangGraph is a library within the LangChain ecosystem designed to tackle these challenges head-on.
LangGraph provides a framework for defining, coordinating, and executing multiple LLM agents (or chains) in a structured manner.
It simplifies the development process by enabling the creation of cyclical graphs, which are essential for developing agent runtimes.
With LangGraph, we can easily build robust, scalable, and flexible multi-agent systems.
If you want to learn more about the LangChain ecosystem, I recommend this introduction to LangChain.
...
LangGraph enables us to create stateful, multi-actor applications utilizing LLMs as easily as possible.
It extends the capabilities of LangChain, introducing the ability to create and manage cyclical graphs, which are pivotal for developing sophisticated agent runtimes.
The core concepts of LangGraph include: graph structure, state management, and coordination.
### Graph structure
Imagine your application as a directed graph.
In LangGraph, each node represents an LLM agent, and the edges are the communication channels between these agents.
This structure allows for clear and manageable workflows, where each agent performs specific tasks and passes information to other agents as needed.
### State management
One of LangGraph's standout features is its automatic state management.
This feature enables us to track and persist information across multiple interactions.
As agents perform their tasks, the state is dynamically updated, ensuring the system maintains context and responds appropriately to new inputs.
…
### Basic Concepts
Nodes: Nodes represent units of work within your LangGraph.
They are typically Python functions that perform a specific task, such as:
- Interacting with an LLM
- Calling a tool or API
- Performing some data manipulation
- Receiving user input
- Executing business logic
In LangGraph, you can add nodes using the
…
syntax.
Edges: Edges are communication channels between nodes.
They define the flow of information and the order of execution.
You can add edges using the
…
syntax.
State: The state is a central object updated over time by the nodes in the graph.
It manages the internal state of your application and can be overridden or added to, depending on the application's requirements.
This state can hold things such as:
- Conversation history: A list of messages between the agent and the user.
- Contextual data: Information relevant to the current task or interaction.
- Internal variables: Flags, counters, or other variables to track the agent's progress and behavior.
…
is a class object defined with a single key
…
```
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
class State(TypedDict):
# messages have the type "list".
# The add_messages function appends messages to the list, rather than overwriting them
messages: Annotated[list, add_messages]
graph_builder = StateGraph(State)
```
### Step 2: Initialize an LLM and add it as a Chatbot node
Here, we initialize the AzureChatOpenAI model and create a simple chatbot function that takes in the state messages as input and generates a message response (which is subsequently appended to the state).
This chatbot function is added as a node named “chatbot” to the graph.
```
from langchain_openai import AzureChatOpenAI
llm = AzureChatOpenAI(
openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
def chatbot(state: State):
return {"messages": [llm.invoke(state["messages"])]}
‘’’The first argument is the unique node name
# The second argument is the function or object that will be called whenever the node is used.’’’
graph_builder.add_node("chatbot", chatbot)
```
…
```
# Set entry and finish points
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
```
Step 4: Compile and Visualize the Graph
Compile the graph to create a CompiledGraph object, and optionally, we can visualize the graph structure using the code below:
…
### Step 5: Run the chatbot
Finally, we implement a loop to continuously prompt the user for input, process it through the graph, and print the assistant's response.
The loop exits when the user types
…
```
# Run the chatbot
while True:
user_input = input("User: ")
if user_input.lower() in ["quit", "exit", "q"]:
print("Goodbye!")
 break
for event in graph.stream({"messages": [("user", user_input)]}):
for value in event.values():
print("Assistant:", value["messages"][-1].content)
```
…
### Custom node types
LangGraph allows you to create custom node types to implement complex agent logic.
This provides flexibility and control over your application's behavior.
```
from typing import Annotated
from langchain_anthropic import ChatAnthropic
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
class MyCustomNode:
def __init__(self, llm):
self.llm = llm
def __call__(self, state):
# Implement your custom logic here
# Access the state and perform actions
messages = state["messages"]
response = self.llm.invoke(messages)
return {"messages": [response]}
graph_builder = StateGraph(State)
llm = ChatAnthropic(model="claude-3-haiku-20240307")
custom_node = MyCustomNode(llm)
graph_builder.add_node("custom_node", custom_node)
```
…
that encapsulates custom logic and interacts with the LLM.
This provides a more structured and maintainable way to implement complex node behaviors.
### Edge types
LangGraph supports different edge types to handle various communication patterns between nodes.
One useful type is the conditional edge, which allows for decision-making based on a node's output.
To create a conditional edge, you need three components:
1. The upstream node: The node's output decides the next step.
2. A function: This function evaluates the upstream node's output and determines the next node to execute, returning a string that represents the decision.
3. A mapping: This mapping links the possible outcomes of the function to the corresponding nodes to be executed.
Here's an example in pseudocode:
…
Here, after the “model” node is called, we can either exit the graph (”end”) and return to the user, or we can continue (”continue”) and call a tool—depending on what the user decides!
...
### Error handling
LangGraph also provides mechanisms for error handling:
- Exceptions: Node functions can raise exceptions to signal errors during execution.
You can catch and handle these exceptions to prevent your graph from crashing.
- Retry mechanisms: You can implement retry logic within your nodes to handle transient errors, such as network issues or API timeouts.
- Logging: Use logging to record errors and track the execution of your graph.

LangGraph is a Python library built on top of LangChain for creating complex conversational AI workflows using a graph-based approach.

### I. Core LangGraph Elements and Structure

|Element|Description|
|--|--|
|Graph|The overarching structure that maps how different tasks (nodes) are connected and executed, representing the workflow.|
|State|A shared data structure that holds the current information or context of the entire application (the application’s memory). Nodes access and modify it. The State is typically defined using a `TypedDict`.|
|Node|An individual Python function or operation that performs a specific task. It receives the current State as input and returns the updated State as output.|
|Edge|The connection between nodes that determines the flow of execution, specifying which node executes next.|
|Conditional Edge|A specialized connection that routes execution based on a specific condition or logic applied to the current State. Used for decision-making.|
|Start/End Point|Virtual entry and conclusion points for the workflow execution.|
|Tool|Specialized functions or utilities that nodes can utilize to perform specific tasks, enhancing capabilities (e.g., fetching data from an API).|
|Tool Node|A special type of node whose main job is to run a Tool and connect the tool’s output back into the State.|
|State Graph|The framework ( `StateGraph` class) used to build and compile the graph structure, managing the nodes, edges, and overall state flow.|
|Reducer Function|A rule that defines how updates from nodes are combined with the existing state. `add_messages` is a reducer function used to append new data without overwriting the state.|

### II. Essential Python Type Annotations

These concepts are used extensively for defining the State and handling complex data flow:
|Annotation|Purpose|Usage Note|
|--|--|--|
|TypedDict|Defines the structure of the State as a class, explicitly setting the expected data type for each key (e.g., `name: str`).|Crucial for type safety, reducing runtime errors.|
|Union|Specifies that a value can be one of several defined data types (e.g., `int` or `float`).|Used extensively in LangGraph/LangChain.|
|Optional|Specifies that a parameter can be a defined data type or a `None` value.|
|Lambda|A shortcut for writing small, anonymous functions.|Often used as a pass-through function ( `lambda state: state`) in nodes that only return an edge or perform comparison without state assignment.|
|Annotated|Provides additional context (metadata) to a type without changing its data type (e.g., specifying a `str` must be a “valid email format”).|
|Sequence|Helps automatically handle state updates for sequential data structures, like chat history, avoiding manual list manipulation.|

…

|Message Type|Purpose|
|--|--|
|Human Message|Represents the input from a user (prompt).|
|AI Message|Represents responses generated by AI models.|
|System Message|Used to provide fixed instructions or context to the model (e.g., persona definition).|
|Tool Message|Contains data passed back to the LLM after a tool call (specific to tool usage).|
|Base Message|The foundational parent class for all message types in LangGraph.|

### IV. Basic Graph Implementation Patterns

#### A. Hello World Graph (Single Node, Sequential Flow)

This template shows how to define the state, create a node, and compile the simplest graph structure:

**1. Define the Agent State (Schema)**

```

from typing import TypedDict

from langgraph.graph import StateGraph, START, END

class AgentState(TypedDict):

message: str

# The state needs to be in the form of a TypedDict.

```
**2. Define the Node Function (Action)**

Nodes receive the State and return the updated State. Docstrings are important as they inform LLMs what the function does.

```

def greeting_node(state: AgentState) -> AgentState:

"""Simple node that adds a greeting message to the state""" #

# Access and update the state key

state["message"] = "Hey " + state["message"] + " how is your day going"

return state # Must return the updated state

```
**3. Build and Compile the Graph**

The graph is initialized using

`StateGraph` and the defined state schema.

```

graph = StateGraph(AgentState) # Pass the state schema

node_name = "greeter"

# Add the node (name and function/action)

graph.add_node(node_name, greeting_node)

# Set the entry and finish points to the single node

graph.set_entry_point(node_name)

graph.set_finish_point(node_name)

app = graph.compile() # Compile the graph

```

…

#### B. Sequential Graph (Multiple Nodes)

Nodes are connected using

`graph.add_edge()`.

```

# Assuming 'first_node' and 'second_node' are defined

graph.add_node("first_node", first_node)

graph.add_node("second_node", second_node)

graph.set_entry_point("first_node")

# Use add_edge to connect the flow directionally

graph.add_edge("first_node", "second_node")

graph.set_finish_point("second_node")

app = graph.compile()

```

#### C. Conditional Graph (Routing)

This pattern uses a routing function to determine the next path, defining branches with

`add_conditional_edges`.

**1. Define the Router Function**

The router function inspects the state (e.g.,

`operation` attribute) and returns the name of the edge to take.

…

**3. Define Conditional Edges**

The

`path_map` links the returned edge name (e.g., “addition_operation”) to the target node name (e.g., “add_node”).
```

graph.add_edge(START, "router") # Connect start to router

graph.add_conditional_edges(

source="router",

path=decide_next_node, # The routing function

path_map={

"addition_operation": "add_node",

"subtraction_operation": "subtract_node"



# Edges from operations back to the END point

graph.add_edge("add_node", END)

graph.add_edge("subtract_node", END)

app = graph.compile()

```

#### D. Looping Graph

Looping logic is handled by a conditional edge routing back to a prior node, typically controlled by a counter variable in the state.

**1. Define the Continuation Logic**

The function checks a state attribute (

`counter`) to decide whether to continue the loop or exit.

```

def should_continue(state: AgentState):

# Assuming AgentState has a 'counter: int' attribute

if state["counter"] < 5:

print(f"Counter: {state['counter']}") #

return "loop"

else:

return "exit"

```
**2. Implement the Conditional Loop Edge**

If the result is “loop”, execution routes back to the source node (

`random_node`). If “exit”, it routes to

`END`.

```

# Define the conditional edge starting from the random node

graph.add_conditional_edges(

source="random_node",

path=should_continue,

path_map={

"loop": "random_node", # Loop back to itself

"exit": END # End the graph



```

…

```

from langchain_core.tools import tool

from langchain_openai import ChatOpenAI

@tool

def add(a: int, b: int) -> int:

"""This is an addition function that adds two numbers together.""" # Necessary docstring

return a + b

tools = [add]

model = ChatOpenAI(model="gpt-4o")

# Bind tools to the LLM so the model knows they exist

llm_with_tools = model.bind_tools(tools)

```

…

### RAG Example

```

from dotenv import load_dotenv

import os

from langgraph.graph import StateGraph, END

from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, ToolMessage

from operator import add as add_messages

from langchain_openai import ChatOpenAI

from langchain_openai import OpenAIEmbeddings

from langchain_community.document_loaders import PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_chroma import Chroma

from langchain_core.tools import tool

load_dotenv()

llm = ChatOpenAI(

model="gpt-4o", temperature = 0) # I want to minimize hallucination - temperature = 0 makes the model output more deterministic

# Our Embedding Model - has to also be compatible with the LLM

embeddings = OpenAIEmbeddings(

model="text-embedding-3-small",



pdf_path = "Stock_Market_Performance_2024.pdf"

# Safety measure I have put for debugging purposes :)

if not os.path.exists(pdf_path):

raise FileNotFoundError(f"PDF file not found: {pdf_path}")

pdf_loader = PyPDFLoader(pdf_path) # This loads the PDF

# Checks if the PDF is there

try:

pages = pdf_loader.load()

print(f"PDF has been loaded and has {len(pages)} pages")

except Exception as e:

print(f"Error loading PDF: {e}")

raise

# Chunking Process

text_splitter = RecursiveCharacterTextSplitter(

chunk_size=1000,

chunk_overlap=200



pages_split = text_splitter.split_documents(pages) # We now apply this to our pages

persist_directory = r"C:\Vaibhav\LangGraph_Book\LangGraphCourse\Agents"

collection_name = "stock_market"

# If our collection does not exist in the directory, we create using the os command

if not os.path.exists(persist_directory):

os.makedirs(persist_directory)

try:

# Here, we actually create the chroma database using our embeddigns model

vectorstore = Chroma.from_documents(

documents=pages_split,

embedding=embeddings,

persist_directory=persist_directory,

collection_name=collection_name



print(f"Created ChromaDB vector store!")

except Exception as e:

print(f"Error setting up ChromaDB: {str(e)}")

raise

# Now we create our retriever

retriever = vectorstore.as_retriever(

search_type="similarity",

search_kwargs={"k": 5} # K is the amount of chunks to return



@tool

def retriever_tool(query: str) -> str:

"""

This tool searches and returns the information from the Stock Market Performance 2024 document.

"""

docs = retriever.invoke(query)

if not docs:

return "I found no relevant information in the Stock Market Performance 2024 document."

results = []

for i, doc in enumerate(docs):

results.append(f"Document {i+1}:\n{doc.page_content}")

return "\n\n".join(results)

tools = [retriever_tool]

llm = llm.bind_tools(tools)

class AgentState(TypedDict):

messages: Annotated[Sequence[BaseMessage], add_messages]

def should_continue(state: AgentState):

"""Check if the last message contains tool calls."""

result = state['messages'][-1]

return hasattr(result, 'tool_calls') and len(result.tool_calls) > 0

system_prompt = """

You are an intelligent AI assistant who answers questions about Stock Market Performance in 2024 based on the PDF document loaded into your knowledge base.

Use the retriever tool available to answer questions about the stock market performance data. You can make multiple calls if needed.

If you need to look up some information before asking a follow up question, you are allowed to do that!

Please always cite the specific parts of the documents you use in your answers.

"""

tools_dict = {our_tool.name: our_tool for our_tool in tools} # Creating a dictionary of our tools

# LLM Agent

def call_llm(state: AgentState) -> AgentState:

"""Function to call the LLM with the current state."""

messages = list(state['messages'])

messages = [SystemMessage(content=system_prompt)] + messages

message = llm.invoke(messages)

return {'messages': [message]}

# Retriever Agent

def take_action(state: AgentState) -> AgentState:

"""Execute tool calls from the LLM's response."""

tool_calls = state['messages'][-1].tool_calls

results = []

for t in tool_calls:

print(f"Calling Tool: {t['name']} with query: {t['args'].get('query', 'No query provided')}")

if not t['name'] in tools_dict: # Checks if a valid tool is present

print(f"\nTool: {t['name']} does not exist.")

result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."

else:

result = tools_dict[t['name']].invoke(t['args'].get('query', ''))

print(f"Result length: {len(str(result))}")

# Appends the Tool Message

results.append(ToolMessage(tool_call_id=t['id'], name=t['name'], content=str(result)))

print("Tools Execution Complete. Back to the model!")

return {'messages': results}

graph = StateGraph(AgentState)

graph.add_node("llm", call_llm)

graph.add_node("retriever_agent", take_action)

graph.add_conditional_edges(

"llm",

should_continue,

{True: "retriever_agent", False: END}



graph.add_edge("retriever_agent", "llm")

graph.set_entry_point("llm")

rag_agent = graph.compile()

def running_agent():

print("\n=== RAG AGENT===")

while True:

user_input = input("\nWhat is your question: ")

if user_input.lower() in ['exit', 'quit']:

break

messages = [HumanMessage(content=user_input)] # converts back to a HumanMessage type

result = rag_agent.invoke({"messages": messages})

print("\n=== ANSWER ===")

print(result['messages'][-1].content)

running_agent()

```

## Enjoy Reading This Article?

Here are some more articles you might like to read next: