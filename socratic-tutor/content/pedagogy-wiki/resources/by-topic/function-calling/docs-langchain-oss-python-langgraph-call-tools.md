# Source: https://docs.langchain.com/oss/python/langgraph/call-tools
# Title: Call tools - Docs by LangChain
# Fetched via: search
# Date: 2026-04-10

This quickstart demonstrates how to build a calculator agent using the LangGraph Graph API or the Functional API.
- Use the Graph API if you prefer to define your agent as a graph of nodes and edges.
- Use the Functional API if you prefer to define your agent as a single function.
For conceptual information, see Graph API overview and Functional API overview.
For this example, you will need to set up a Claude (Anthropic) account and get an API key.
Then, set the `ANTHROPIC_API_KEY` environment variable in your terminal.
- Use the Graph API
- Use the Functional API
## ​ 1.
Define tools and model
In this example, we’ll use the Claude Sonnet 4.5 model and define tools for addition, multiplication, and division.
```
from langchain.tools import tool
from langchain.chat_models import init_chat_model
model = init_chat_model(
"claude-sonnet-4-6",
temperature=0
)
# Define tools
@tool
def multiply(a: int, b: int) -> int:
"""Multiply `a` and `b`.
Args:
a: First int
b: Second int
"""
return a * b
@tool
def add(a: int, b: int) -> int:
"""Adds `a` and `b`.
Args:
a: First int
b: Second int
"""
return a + b
@tool
def divide(a: int, b: int) -> float:
"""Divide `a` and `b`.
Args:
a: First int
b: Second int
"""
return a / b
# Augment the LLM with tools
tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)
```
## ​ 2.
Define state
The graph’s state is used to store the messages and the number of LLM calls.
```
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
class MessagesState(TypedDict):
messages: Annotated[list[AnyMessage], operator.add]
llm_calls: int
```
## ​ 3.
Define model node
The model node is used to call the LLM and decide whether to call a tool or not.
```
from langchain.messages import SystemMessage
def llm_call(state: dict):
"""LLM decides whether to call a tool or not"""
return {
"messages": [
model_with_tools.invoke(
[
SystemMessage(
content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)
]
+ state["messages"]
)
],
"llm_calls": state.get('llm_calls', 0) + 1
}
```
## ​ 4.
Define tool node
The tool node is used to call the tools and return the results.
```
from langchain.messages import ToolMessage
def tool_node(state: dict):
"""Performs the tool call"""
result = []
for tool_call in state["messages"][-1].tool_calls:
tool = tools_by_name[tool_call["name"]]
observation = tool.invoke(tool_call["args"])
result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
return {"messages": result}
```
## ​ 5.
Define end logic
The conditional edge function is used to route to the tool node or end based upon whether the LLM made a tool call.
```
from typing import Literal
from langgraph.graph import StateGraph, START, END
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
"""Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
messages = state["messages"]
last_message = messages[-1]
# If the LLM makes a tool call, then perform an action
if last_message.tool_calls:
return "tool_node"
# Otherwise, we stop (reply to the user)
return END
```
## ​ 6.
Build and compile the agent
The agent is built using the `StateGraph` class and compiled using the `compile` method.
```
# Build workflow
agent_builder = StateGraph(MessagesState)
# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
"llm_call",
should_continue,
["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")
# Compile the agent
agent = agent_builder.compile()
# Show the agent
from IPython.display import Image, display
display(Image(agent.get_graph(xray=True).draw_mermaid_png()))
# Invoke
from langchain.messages import HumanMessage
messages = [HumanMessage(content="Add 3 and 4.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
m.pretty_print()
```
Congratulations!
You’ve built your first agent using the LangGraph Graph API.
Full code example
```
# Step 1: Define tools and model
from langchain.tools import tool
from langchain.chat_models import init_chat_model
model = init_chat_model(
"claude-sonnet-4-6",
temperature=0
)
# Define tools
@tool
def multiply(a: int, b: int) -> int:
"""Multiply `a` and `b`.
Args:
a: First int
b: Second int
"""
return a * b
@tool
def add(a: int, b: int) -> int:
"""Adds `a` and `b`.
Args:
a: First int
b: Second int
"""
return a + b
@tool
def divide(a: int, b: int) -> float:
"""Divide `a` and `b`.
Args:
a: First int
b: Second int
"""
return a / b
# Augment the LLM with tools
tools = [add, multiply, divide]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)
# Step 2: Define state
from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator
class MessagesState(TypedDict):
messages: Annotated[list[AnyMessage], operator.add]
llm_calls: int
# Step 3: Define model node
from langchain.messages import SystemMessage
def llm_call(state: dict):
"""LLM decides whether to call a tool or not"""
return {
"messages": [
model_with_tools.invoke(
[
SystemMessage(
content="You are a helpful assistant tasked with performing arithmetic on a set of inputs."
)
]
+ state["messages"]
)
],
"llm_calls": state.get('llm_calls', 0) + 1
}
# Step 4: Define tool node
from langchain.messages import ToolMessage
def tool_node(state: dict):
"""Performs the tool call"""
result = []
for tool_call in state["messages"][-1].tool_calls:
tool = tools_by_name[tool_call["name"]]
observation = tool.invoke(tool_call["args"])
result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
return {"messages": result}
# Step 5: Define logic to determine whether to end
from typing import Literal
from langgraph.graph import StateGraph, START, END
# Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
"""Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""
messages = state["messages"]
last_message = messages[-1]
# If the LLM makes a tool call, then perform an action
if last_message.tool_calls:
return "tool_node"
# Otherwise, we stop (reply to the user)
return END
# Step 6: Build agent
# Build workflow
agent_builder = StateGraph(MessagesState)
# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
"llm_call",
should_continue,
["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")
# Compile the agent
agent = agent_builder.compile()
from IPython.display import Image, display
# Show the agent
display(Image(agent.get_graph(xray=True).draw_mermaid_png()))
# Invoke
from langchain.messages import HumanMessage
messages = [HumanMessage(content="Add 3 and 4.")]
messages = agent.invoke({"messages": messages})
for m in messages["messages"]:
m.pretty_print()
```

Tools extend what agents can do—letting them fetch real-time data, execute code, query external databases, and take actions in the world. Under the hood, tools are callable functions with well-defined inputs and outputs that get passed to a chat model. The model decides when to invoke a tool based on the conversation context, and what input arguments to provide.

## ​ Create tools

### ​ Basic tool definition
The simplest way to create a tool is with the `@tool` decorator. By default, the function’s docstring becomes the tool’s description that helps the model understand when to use it:
```
from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
 """Search the customer database for records matching the query.

 Args:
 query: Search terms to look for
 limit: Maximum number of results to return
 """
 return f"Found {limit} results for '{query}'"

```
Type hints are **required** as they define the tool’s input schema. The docstring should be informative and concise to help the model understand the tool’s purpose.

**Server-side tool use:** Some chat models feature built-in tools (web search, code interpreters) that are executed server-side. See Server-side tool use for details.

### ​ Customize tool properties

#### ​ Custom tool name
By default, the tool name comes from the function name. Override it when you need something more descriptive:
```
@tool("web_search") # Custom name
def search(query: str) -> str:
 """Search the web for information."""
 return f"Results for: {query}"

print(search.name) # web_search

```

…

```
from pydantic import BaseModel, Field
from typing import Literal

class WeatherInput(BaseModel):
 """Input for weather queries."""
 location: str = Field(description="City name or coordinates")
 units: Literal["celsius", "fahrenheit"] = Field(
 default="celsius",
 description="Temperature unit preference"
 )
 include_forecast: bool = Field(
 default=False,
 description="Include 5-day forecast"
 )

@tool(args_schema=WeatherInput)
def get_weather(location: str, units: str = "celsius", include_forecast: bool = False) -> str:
 """Get current weather and optional forecast."""
 temp = 22 if units == "celsius" else 72
 result = f"Current weather in {location}: {temp} degrees {units[0].upper()}"
 if include_forecast:
 result += "\nNext 5 days: Sunny"
 return result

```

…

## ​ Access context
Tools are most powerful when they can access runtime information like conversation history, user data, and persistent memory. This section covers how to access and update this information from within your tools. Tools can access runtime information through the `ToolRuntime` parameter, which provides: |Component|Description|Use case|
|--|--|--|
|**State**|Short-term memory - mutable data that exists for the current conversation (messages, counters, custom fields)|Access conversation history, track tool call counts|
|**Context**|Immutable configuration passed at invocation time (user IDs, session info)|Personalize responses based on user identity|
|**Store**|Long-term memory - persistent data that survives across conversations|Save user preferences, maintain knowledge base|
|**Stream Writer**|Emit real-time updates during tool execution|Show progress for long-running operations|
|**Execution Info**|Identity and retry information for the current execution (thread ID, run ID, attempt number)|Access thread/run IDs, adjust behavior based on retry state|
|**Server Info**|Server-specific metadata when running on LangGraph Server (assistant ID, graph ID, authenticated user)|Access assistant ID, graph ID, or authenticated user info|
|**Config**|`RunnableConfig` for the execution|Access callbacks, tags, and metadata|
|**Tool Call ID**|Unique identifier for the current tool invocation|Correlate tool calls for logs and model invocations|

### ​ Short-term memory (State)
State represents short-term memory that exists for the duration of a conversation. It includes the message history and any custom fields you define in your graph state.

Add `runtime: ToolRuntime` to your tool signature to access state. This parameter is automatically injected and hidden from the LLM - it won’t appear in the tool’s schema.

…

```
from langgraph.types import Command
from langchain.tools import tool

@tool
def set_user_name(new_name: str) -> Command:
 """Set the user's name in the conversation state."""
 return Command(update={"user_name": new_name})

```

…

```
from dataclasses import dataclass
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.tools import tool, ToolRuntime

USER_DATABASE = {
 "user123": {
 "name": "Alice Johnson",
 "account_type": "Premium",
 "balance": 5000,
 "email": "alice@example.com"
 },
 "user456": {
 "name": "Bob Smith",
 "account_type": "Standard",
 "balance": 1200,
 "email": "bob@example.com"
 }
}

@dataclass
class UserContext:
 user_id: str

@tool
def get_account_info(runtime: ToolRuntime[UserContext]) -> str:
 """Get the current user's account information."""
 user_id = runtime.context.user_id

 if user_id in USER_DATABASE:
 user = USER_DATABASE[user_id]
 return f"Account holder: {user['name']}\nType: {user['account_type']}\nBalance: ${user['balance']}"
 return "User not found"

model = ChatOpenAI(model="gpt-4.1")
agent = create_agent(
 model,
 tools=[get_account_info],
 context_schema=UserContext,
 system_prompt="You are a financial assistant."
)

result = agent.invoke(
 {"messages": [{"role": "user", "content": "What's my current balance?"}]},
 context=UserContext(user_id="user123")
)

```

…

```
from langchain.tools import tool, ToolRuntime

@tool
def get_assistant_scoped_data(runtime: ToolRuntime) -> str:
 """Fetch data scoped to the current assistant."""
 server = runtime.server_info
 if server is not None:
 print(f"Assistant: {server.assistant_id}, Graph: {server.graph_id}")
 if server.user is not None:
 print(f"User: {server.user.identity}")
 return "done"

```

…

## ​ ToolNode
`ToolNode` is a prebuilt node that executes tools in LangGraph workflows. It handles parallel tool execution, error handling, and state injection automatically.

For custom workflows where you need fine-grained control over tool execution patterns, use `ToolNode` instead of `create_agent`. It’s the building block that powers agent tool execution.

### ​ Basic usage

```
from langchain.tools import tool
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, MessagesState, START, END

@tool
def search(query: str) -> str:
 """Search for information."""
 return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
 """Evaluate a math expression."""
 return str(eval(expression))

# Create the ToolNode with your tools
tool_node = ToolNode([search, calculator])

# Use in a graph
builder = StateGraph(MessagesState)
builder.add_node("tools", tool_node)
# ... add other nodes and edges

```

…

#### ​ Return a Command
Return a `Command` when the tool needs to update graph state (for example, setting user preferences or app state). You can return a `Command` with or without including a `ToolMessage`.
If the model needs to see that the tool succeeded (for example, to confirm a preference change), include a `ToolMessage` in the update, using `runtime.tool_call_id` for the `tool_call_id` parameter.
```
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime, tool
from langgraph.types import Command

@tool
def set_language(language: str, runtime: ToolRuntime) -> Command:
 """Set the preferred response language."""
 return Command(
 update={
 "preferred_language": language,
 "messages": [
 ToolMessage(
 content=f"Language set to {language}.",
 tool_call_id=runtime.tool_call_id,
 )
 ],
 }
 )

```

…

```
from langgraph.prebuilt import ToolNode

# Default: catch invocation errors, re-raise execution errors
tool_node = ToolNode(tools)

# Catch all errors and return error message to LLM
tool_node = ToolNode(tools, handle_tool_errors=True)

# Custom error message
tool_node = ToolNode(tools, handle_tool_errors="Something went wrong, please try again.")

# Custom error handler
def handle_error(e: ValueError) -> str:
 return f"Invalid input: {e}"

tool_node = ToolNode(tools, handle_tool_errors=handle_error)

# Only catch specific exception types
tool_node = ToolNode(tools, handle_tool_errors=(ValueError, TypeError))

```

…

```
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, MessagesState, START, END

builder = StateGraph(MessagesState)
builder.add_node("llm", call_llm)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "llm")
builder.add_conditional_edges("llm", tools_condition) # Routes to "tools" or END
builder.add_edge("tools", "llm")

graph = builder.compile()

```

…

```
from langchain.tools import tool, ToolRuntime
from langgraph.prebuilt import ToolNode

@tool
def get_message_count(runtime: ToolRuntime) -> str:
 """Get the number of messages in the conversation."""
 messages = runtime.state["messages"]
 return f"There are {len(messages)} messages."

tool_node = ToolNode([get_message_count])

```

The main use is for adding

**cycles** to your LLM application.

Crucially, this is NOT a **DAG** framework.

If you want to build a DAG, you should just use LangChain Expression Language.

Cycles are important for agent-like behaviors, where you call an LLM in a loop, asking it what action to take next.

…

## Quick Start

Here we will go over an example of creating a simple agent that uses chat models and function calling. This agent will represent all its state as a list of messages.

We will need to install some LangChain packages, as well as Tavily to use as an example tool.

…

We can now wrap these tools in a simple LangGraph

`ToolExecutor`.

This is a simple class that receives

`ToolInvocation` objects, calls that tool, and returns the output.

`ToolInvocation` is any class with

`tool` and

`tool_input` attributes.

…

### Set up the model

Now we need to load the chat model we want to use. Importantly, this should satisfy two criteria:

- It should work with lists of messages. We will represent all agent state in the form of messages, so it needs to be able to work well with them.

- It should work with the OpenAI function calling interface. This means it should either be an OpenAI model or a model that exposes a similar interface.

…

After we've done this, we should make sure the model knows that it has these tools available to call. We can do this by converting the LangChain tools into the format for OpenAI function calling, and then bind them to the model class.

…

### Define the nodes

We now need to define a few different nodes in our graph.

In

`langgraph`, a node can be either a function or a runnable.

There are two main nodes we need for this:

- The agent: responsible for deciding what (if any) actions to take.

- A function to invoke tools: if the agent decides to take an action, this node will then execute that action.

…

```

from langgraph.prebuilt import ToolInvocation

import json

from langchain_core.messages import FunctionMessage

# Define the function that determines whether to continue or not

def should_continue(state):

messages = state['messages']

last_message = messages[-1]

# If there is no function call, then we finish

if "function_call" not in last_message.additional_kwargs:

return "end"

# Otherwise if there is, we continue

else:

return "continue"

# Define the function that calls the model

def call_model(state):

messages = state['messages']

response = model.invoke(messages)

# We return a list, because this will get added to the existing list

return {"messages": [response]}

# Define the function to execute tools

def call_tool(state):

messages = state['messages']

# Based on the continue condition

# we know the last message involves a function call

last_message = messages[-1]

# We construct an ToolInvocation from the function_call

action = ToolInvocation(

tool=last_message.additional_kwargs["function_call"]["name"],

tool_input=json.loads(last_message.additional_kwargs["function_call"]["arguments"]),



# We call the tool_executor and get back a response

response = tool_executor.invoke(action)

# We use the response to create a FunctionMessage

function_message = FunctionMessage(content=str(response), name=action.tool)

# We return a list, because this will get added to the existing list

return {"messages": [function_message]}

```

…

```

from langgraph.graph import StateGraph, END

# Define a new graph

workflow = StateGraph(AgentState)

# Define the two nodes we will cycle between

workflow.add_node("agent", call_model)

workflow.add_node("action", call_tool)

# Set the entrypoint as `agent`

# This means that this node is the first one called

workflow.set_entry_point("agent")

# We now add a conditional edge

workflow.add_conditional_edges(

# First, we define the start node. We use `agent`.

# This means these are the edges taken after the `agent` node is called.

"agent",

# Next, we pass in the function that will determine which node is called next.

should_continue,

# Finally we pass in a mapping.

# The keys are strings, and the values are other nodes.

# END is a special node marking that the graph should finish.

# What will happen is we will call `should_continue`, and then the output of that

# will be matched against the keys in this mapping.

# Based on which one it matches, that node will then be called.



# If `tools`, then we call the tool node.

"continue": "action",

# Otherwise we finish.

"end": END



# We now add a normal edge from `tools` to `agent`.

# This means that after `tools` is called, `agent` node is called next.

workflow.add_edge('action', 'agent')

# Finally, we compile it!

# This compiles it into a LangChain Runnable,

# meaning you can use it as you would any other runnable

app = workflow.compile()

```

…

```

inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}

for output in app.stream(inputs):

# stream() yields dictionaries with output keyed by node name

for key, value in output.items():

print(f"Output from node '{key}':")

print("---")

print(value)

print("\n---\n")

```
```

Output from node 'agent':

---

{'messages': [AIMessage(content='', additional_kwargs={'function_call': {'arguments': '{\n "query": "weather in San Francisco"\n}', 'name': 'tavily_search_results_json'}})]}

---

Output from node 'action':

---

{'messages': [FunctionMessage(content="[{'url': 'https://weatherspark.com/h/m/557/2024/1/Historical-Weather-in-January-2024-in-San-Francisco-California-United-States', 'content': 'January 2024 Weather History in San Francisco California, United States Daily Precipitation in January 2024 in San Francisco Observed Weather in January 2024 in San Francisco San Francisco Temperature History January 2024 Hourly Temperature in January 2024 in San Francisco Hours of Daylight and Twilight in January 2024 in San FranciscoThis report shows the past weather for San Francisco, providing a weather history for January 2024. It features all historical weather data series we have available, including the San Francisco temperature history for January 2024. You can drill down from year to month and even day level reports by clicking on the graphs.'}]", name='tavily_search_results_json')]}

---

Output from node 'agent':

---

{'messages': [AIMessage(content="I couldn't find the current weather in San Francisco. However, you can visit [WeatherSpark](https://weatherspark.com/h/m/557/2024/1/Historical-Weather-in-January-2024-in-San-Francisco-California-United-States) to check the historical weather data for January 2024 in San Francisco.")]}

---

Output from node '__end__':

---

{'messages': [HumanMessage(content='what is the weather in sf'), AIMessage(content='', additional_kwargs={'function_call': {'arguments': '{\n "query": "weather in San Francisco"\n}', 'name': 'tavily_search_results_json'}}), FunctionMessage(content="[{'url': 'https://weatherspark.com/h/m/557/2024/1/Historical-Weather-in-January-2024-in-San-Francisco-California-United-States', 'content': 'January 2024 Weather History in San Francisco California, United States Daily Precipitation in January 2024 in San Francisco Observed Weather in January 2024 in San Francisco San Francisco Temperature History January 2024 Hourly Temperature in January 2024 in San Francisco Hours of Daylight and Twilight in January 2024 in San FranciscoThis report shows the past weather for San Francisco, providing a weather history for January 2024. It features all historical weather data series we have available, including the San Francisco temperature history for January 2024. You can drill down from year to month and even day level reports by clicking on the graphs.'}]", name='tavily_search_results_json'), AIMessage(content="I couldn't find the current weather in San Francisco. However, you can visit [WeatherSpark](https://weatherspark.com/h/m/557/2024/1/Historical-Weather-in-January-2024-in-San-Francisco-California-United-States) to check the historical weather data for January 2024 in San Francisco.")]}

---

```

…

```

inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}

async for output in app.astream_log(inputs, include_types=["llm"]):

# astream_log() yields the requested logs (here LLMs) in JSONPatch format

for op in output.ops:

if op["path"] == "/streamed_output/-":

# this is the output from .stream()

...

elif op["path"].startswith("/logs/") and op["path"].endswith(

"/streamed_output/-"

):

# because we chose to only include LLMs, these are LLM tokens

print(op["value"])

```
```

content='' additional_kwargs={'function_call': {'arguments': '', 'name': 'tavily_search_results_json'}}

content='' additional_kwargs={'function_call': {'arguments': '{\n', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': ' ', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': ' "', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': 'query', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': '":', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': ' "', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': 'weather', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': ' in', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': ' San', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': ' Francisco', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': '"\n', 'name': ''}}

content='' additional_kwargs={'function_call': {'arguments': '}', 'name': ''}}

content=''

content=''

content='I'

content="'m"

content=' sorry'

content=','

content=' but'

content=' I'

content=' couldn'

content="'t"

content=' find'

content=' the'

content=' current'

content=' weather'

content=' in'

content=' San'

content=' Francisco'

content='.'

content=' However'

content=','

content=' you'

content=' can'

content=' check'

content=' the'

content=' historical'

content=' weather'

content=' data'

content=' for'

content=' January'

content=' '

content='202'

content='4'

content=' in'

content=' San'

content=' Francisco'

content=' ['

content='here'

content=']('

content='https'

content='://'

content='we'

content='athers'

content='park'

content='.com'

content='/h'

content='/m'

content='/'

content='557'

content='/'

content='202'

content='4'

content='/'

content='1'

content='/H'

content='istorical'

content='-'

content='Weather'

content='-in'

content='-Jan'

content='uary'

content='-'

content='202'

content='4'

content='-in'

content='-S'

content='an'

content='-F'

content='r'

content='anc'

content='isco'

content='-Cal'

content='ifornia'

content='-'

content='United'

content='-'

content='States'

content=').'

content=''

```

…

## Examples

### ChatAgentExecutor: with function calling

This agent executor takes a list of messages as input and outputs a list of messages. All agent state is represented as a list of messages. This specifically uses OpenAI function calling. This is recommended agent executor for newer chat based models that support function calling.

- Getting Started Notebook: Walks through creating this type of executor from scratch

- High Level Entrypoint: Walks through how to use the high level entrypoint for the chat agent executor.

…

- Human-in-the-loop: How to add a human-in-the-loop component

- Force calling a tool first: How to always call a specific tool first

- Respond in a specific format: How to force the agent to respond in a specific format

- Dynamically returning tool output directly: How to dynamically let the agent choose whether to return the result of a tool directly to the user

…

- Human-in-the-loop: How to add a human-in-the-loop component

- Force calling a tool first: How to always call a specific tool first

- Managing agent steps: How to more explicitly manage intermediate steps that an agent takes

…

It then exposes a runnable interface. It can be used to call tools: you can pass in an AgentAction and it will look up the relevant tool and call it with the appropriate input.

…

This is a helper function for creating a graph that works with a chat model that utilizes function calling. Can be created by passing in a model and a list of tools. The model must be one that supports OpenAI function calling.
```

from langchain_openai import ChatOpenAI

from langchain_community.tools.tavily_search import TavilySearchResults

from langgraph.prebuilt import chat_agent_executor

from langchain_core.messages import HumanMessage

tools = [TavilySearchResults(max_results=1)]

model = ChatOpenAI()

app = chat_agent_executor.create_function_calling_executor(model, tools)

inputs = {"messages": [HumanMessage(content="what is the weather in sf")]}

for s in app.stream(inputs):

print(list(s.values())[0])

print("----")

```

…

```

from langgraph.prebuilt import create_agent_executor

from langchain_openai import ChatOpenAI

from langchain import hub

from langchain.agents import create_openai_functions_agent

from langchain_community.tools.tavily_search import TavilySearchResults

tools = [TavilySearchResults(max_results=1)]

# Get the prompt to use - you can modify this!

prompt = hub.pull("hwchase17/openai-functions-agent")

# Choose the LLM that will drive the agent

llm = ChatOpenAI(model="gpt-3.5-turbo-1106")

# Construct the OpenAI Functions agent

agent_runnable = create_openai_functions_agent(llm, tools, prompt)

app = create_agent_executor(agent_runnable, tools)

inputs = {"input": "what is the weather in sf", "chat_history": []}

for s in app.stream(inputs):

print(list(s.values())[0])

print("----")

```

### Transcript
{ts:0} I built an AI research assistant to draft out scientific research papers on
{ts:5} any topic you want and in this video I'm going to show you how I built that using Lang graph I actually already talked
{ts:11} about this system in a previous video but in this one I'm going deeper into the Lang graph implementation at a lower

…

{ts:34} want to stress that the results are not the point of this point was to demonstrate how to use Lang graph with a
{ts:40} practical use case and honestly the results were cool enough that I was excited to share what I've built with
{ts:48} everybody and it could be a starting point of something a lot better so before I show you the code I want to
{ts:52} quickly demonstrate the tool and I you can get this code on GitHub there's a link in the description go on into this
{ts:58} folder AI scientific research agent and you'll see my library right here so we're going to run python
{ts:65} DMS research agent and I've got my virtual environment installed and activated already this is what our agent

…

{ts:239} that P PDF after generating it uh there's been another HTTP request to Claude so basically the agent is going
{ts:246} ahead and doing all of this work um without us needing to prompt it explicitly because I've given it access
{ts:252} to these tools so it went ahead and drafted a paper and then render that as a PDF and then it just sort of tells me

…

{ts:330} talked through this workflow a lot more detail in the last video so here I'm just going to show you just for a few
{ts:337} seconds how this works we're using this open AI model actually I lied when I said Claude we're using um open AI for
{ts:344} this and but I could simply use Claud just by commenting that line in uh but in any case so then if I come down we
{ts:352} are creating a react agent so this stands for uh reason and then act and they sort of have this pre-built for us
{ts:360} and I talked about this again in the first video in more detail so you can check that out if you're interested in
{ts:364} seeing this and looking at a bit of the source for that some of the source code but with this one line we create our
{ts:369} whole graph and then I'm just simply calling that so if I come down I have an initial prompt that I sort of put as the
{ts:376} initial condition and then we start our chatbot which iterates in this like infinite Loop of talking with it uh and
{ts:382} the interface for that is graph. stream and the last thing I'll show you is the initial prompt so here it is and this is
{ts:388} kind of the brains of the agent this is what I've written that sort of tells it how to act and I have no other like
{ts:394} baked in instruction for it um the reason it's using all these tools is cuz I've told it about the tools so we
{ts:400} provide the tools down here to the react agent that's it so what we're going to do now is switch to workflow number two

…

{ts:502} it's going to have something like uh role right and the role is like the user or the assistant and then
{ts:510} uh where is it it'll be content right like up here message. content and the content will be you know
{ts:518} um the the the stuff coming out right okay so uh the reason I'm showing you this is because we should have this kind

…

{ts:543} and these are coming from other libraries I talked about these in the first video I will talk about these
{ts:548} later but we we have these tools and then we are creating our own tool node this is different than the first
{ts:554} workflow we we just sort of pass these tools into this create react agent pre-built function but now we're
{ts:559} building the graph ourself and so I'm creating an explicit tool node in our graph for that again we're defining our
{ts:567} model now just for fun I want to use a different model so I'm going to use anthropic we're going to get that in
{ts:573} comment out a a that one okay so now we're using Sonet and check this out on the very right we are binding tools so

…

{ts:619} model and call model is a node right here so it is our agent it is our agent node this is um we're going to be like
{ts:627} we're we're invoking our model so we're this means like we're making a I I think of invoke as making a call to the API
{ts:636} the model that we're talking to of course it could be like a locally hosted model like I've got an oama line we we

…

{ts:715} graph message and it affects this object of State in such a way that we are allowed to where is it down here we we
{ts:725} don't need to append the response to the previous messages when we return this it's going to do some magic in order to
{ts:733} um add this response as a message onto our messages in our state yeah pretty crazy stuff right all

…

{ts:756} down and we just Define these nodes and now I have to connect these things and I do that with edges so we're going to
{ts:762} start with the agent again start again just we we import that where is it oh that's not it this is it so we're
{ts:769} importing start end and state graph um of course do I have end okay end is sort of in this continue okay let's come down
{ts:776} so we we come to our agent here then have a conditional note and this defines like okay what do we do we want to call
{ts:785} a tool or do we want to um just like basically restart the chat loop with our agent um if we do call a tool we always

…

{ts:814} at the uh messages we look at the the latest message so this would be something that we've just received from
{ts:821} like um let's say from anthropic and then we're going to say is that a tool call so if the last message has tool
{ts:829} calls because Claude will say something like oh uh you want the weather well I have a tool that gets me the live
{ts:836} weather so let's make a tool call to that weather API so that I can get the weather then I then I'll know the
{ts:842} weather and I can tell the user that so if if um we're getting a tool called in the message then we return the tools
{ts:850} node which points to this tools node right here and we call the tool um and that's how our that's how everything was

…

{ts:913} ready to go so I can just go ahead and run it up here and we're going to see some logs coming down below so uh we can
{ts:919} see the graph looks the same this is what we expected but this really is the visual that we've been just talking
{ts:924} through there's this dotted line to tools so we might call tools um but and if we do we will always call back to the

…

{ts:1145} sure did I not save I didn't save it okay um okay let's go back so this graph is is working that's pretty cool um
{ts:1153} we've gone ahead and sent off a human message to grock uh and you'll notice that this this um grock that I'm using
{ts:1160} it has tool calling available so okay so check it out now we're making HTTP requests to Local Host and this is where

…

{ts:1313} graph so here's an example from the documentation we're going to import this tool decorator and that will let us
{ts:1319} Define a tool and here's a tool from the docs about getting uh weather and so it's just called search but um I might
{ts:1327} want to say something like get weather and then the query let's um call it the city the city name and for the city name

…

{ts:1465} model for example using this bind tools that's exactly what we're doing um if I look for bind tools do you see down here
{ts:1473} we are binding these tools to some sort of model right and so when we do that um it's it becomes available in the prompt
{ts:1481} context through something called prompt augmentation so um the the Lang graph is going to create a prompt that has

…

{ts:1510} access to this tool um and then we say something like when a user asks for weather information you call this tool
{ts:1517} with the appropriate City we know the arguments that it requires um yeah uh and so this will work with any type of
{ts:1524} tool and we'll sort of just list them out in the prompt and so you might might be wondering does this get repeated for

…

{ts:1549} context window in order to get the next output the response so now what's happening is we have information like
{ts:1556} this this exact thing we were just looking at and this gets included it's like going to be at the start of the
{ts:1561} conversation included as context for every for every question throughout this interaction now this is is not literally

# Tools¶
Tools are a way to encapsulate a function and its input schema in a way that can be passed to a chat model that supports tool calling.
This allows the model to request the execution of this function with specific inputs.
You can either define your own tools or use prebuilt integrations that LangChain provides.
## Define simple tools¶
You can pass a vanilla function to
`create_react_agent` to use as a tool:
*API Reference: create_react_agent*
```
from langgraph.prebuilt import create_react_agent
def multiply(a: int, b: int) -> int:
"""Multiply two numbers."""
return a * b
create_react_agent(
model="anthropic:claude-3-7-sonnet",
tools=[multiply]
```
`create_react_agent` automatically converts vanilla functions to LangChain tools.
…
```
from langgraph.prebuilt import InjectedState
from langgraph.prebuilt.chat_agent_executor import AgentState
from langchain_core.runnables import RunnableConfig
def my_tool(
# This will be populated by an LLM
tool_arg: str,
# access information that's dynamically updated inside the agent
state: Annotated[AgentState, InjectedState],
# access static data that is passed at agent invocation
config: RunnableConfig,
) -> str:
"""My tool."""
do_something_with_state(state["messages"])
do_something_with_config(config)
...
```
## Disable parallel tool calling¶
Some model providers support executing multiple tools in parallel, but allow users to disable this feature.
For supported providers, you can disable parallel tool calling by setting
`parallel_tool_calls=False` via the
`model.bind_tools()` method:
*API Reference: init_chat_model*
```
from langchain.chat_models import init_chat_model
def add(a: int, b: int) -> int:
"""Add two numbers"""
return a + b
def multiply(a: int, b: int) -> int:
"""Multiply two numbers."""
return a * b
model = init_chat_model("anthropic:claude-3-5-sonnet-latest", temperature=0)
tools = [add, multiply]
agent = create_react_agent(
# disable parallel tool calls
model=model.bind_tools(tools, parallel_tool_calls=False),
tools=tools
agent.invoke(
{"messages": [{"role": "user", "content": "what's 3 + 5 and 4 * 7?"}]}
```
…
```
from langchain_core.tools import tool
@tool(return_direct=True)
def add(a: int, b: int) -> int:
"""Add two numbers"""
return a + b
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[add]
agent.invoke(
{"messages": [{"role": "user", "content": "what's 3 + 5?"}]}
```
## Force tool use¶
To force the agent to use specific tools, you can set the
`tool_choice` option in
`model.bind_tools()`:
*API Reference: tool*
```
from langchain_core.tools import tool
@tool(return_direct=True)
def greet(user_name: str) -> int:
"""Greet user."""
return f"Hello {user_name}!"
tools = [greet]
agent = create_react_agent(
model=model.bind_tools(tools, tool_choice={"type": "tool", "name": "greet"}),
tools=tools
agent.invoke(
{"messages": [{"role": "user", "content": "Hi, I am Bob"}]}
```
...
## Handle tool errors¶
By default, the agent will catch all exceptions raised during tool calls and will pass those as tool messages to the LLM.
To control how the errors are handled, you can use the prebuilt
`ToolNode` — the node that executes tools inside
`create_react_agent` — via its
`handle_tool_errors` parameter:
…
## Prebuilt tools¶
You can use prebuilt tools from model providers by passing a dictionary with tool specs to the
`tools` parameter of
`create_react_agent`.
For example, to use the
`web_search_preview` tool from OpenAI:
*API Reference: create_react_agent*
…
**Search**: Bing, SerpAPI, Tavily **Code interpreters**: Python REPL, Node.js REPL **Databases**: SQL, MongoDB, Redis **Web data**: Web scraping and browsing **APIs**: OpenWeatherMap, NewsAPI, and others
These integrations can be configured and added to your agents using the same