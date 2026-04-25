# Source: https://reference.langchain.com/python/langgraph/agents/
# Title: Agents (LangGraph) | LangChain Reference
# Fetched via: search
# Date: 2026-04-10

Agents combine language models with tools to create systems that can reason about tasks, decide which tools to use, and iteratively work towards solutions. `create_agent` provides a production-ready agent implementation. An LLM Agent runs tools in a loop to achieve a goal. An agent runs until a stop condition is met - i.e., when the model emits a final output or an iteration limit is reached.
`create_agent` builds a **graph**-based agent runtime using LangGraph. A graph consists of nodes (steps) and edges (connections) that define how your agent processes information. The agent moves through this graph, executing nodes like the model node (which calls the model), the tools node (which executes tools), or middleware.Learn more about the Graph API.

## ​ Core components

### ​ Model
The model is the reasoning engine of your agent. It can be specified in multiple ways, supporting both static and dynamic model selection.

#### ​ Static model
Static models are configured once when creating the agent and remain unchanged throughout execution. This is the most common and straightforward approach. To initialize a static model from a :
```
from langchain.agents import create_agent

agent = create_agent("openai:gpt-5", tools=tools)

```
For more control over the model configuration, initialize a model instance directly using the provider package. In this example, we use `ChatOpenAI`. See Chat models for other available chat model classes.
```
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

model = ChatOpenAI(
 model="gpt-5",
 temperature=0.1,
 max_tokens=1000,
 timeout=30
 # ... (other params)
)
agent = create_agent(model, tools=tools)

```
Model instances give you complete control over configuration. Use them when you need to set specific parameters like `temperature`, `max_tokens`, `timeouts`, `base_url`, and other provider-specific settings. Refer to the reference to see available params and methods on your model.

#### ​ Dynamic model
Dynamic models are selected at based on the current and context. This enables sophisticated routing logic and cost optimization. To use a dynamic model, create middleware using the `@wrap_model_call` decorator that modifies the model in the request:
```
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse

basic_model = ChatOpenAI(model="gpt-4.1-mini")
advanced_model = ChatOpenAI(model="gpt-4.1")

@wrap_model_call
def dynamic_model_selection(request: ModelRequest, handler) -> ModelResponse:
 """Choose model based on conversation complexity."""
 message_count = len(request.state["messages"])

 if message_count > 10:
 # Use an advanced model for longer conversations
 model = advanced_model
 else:
 model = basic_model

 return handler(request.override(model=model))

agent = create_agent(
 model=basic_model, # Default model
 tools=tools,
 middleware=[dynamic_model_selection]
)

```

### ​ Tools
Tools give agents the ability to take actions. Agents go beyond simple model-only tool binding by facilitating: - Multiple tool calls in sequence (triggered by a single prompt)
- Parallel tool calls when appropriate
- Dynamic tool selection based on previous results
- Tool retry logic and error handling
- State persistence across tool calls
For more information, see Tools.

#### ​ Static tools
Static tools are defined when creating the agent and remain unchanged throughout execution. This is the most common and straightforward approach. To define an agent with static tools, pass a list of the tools to the agent.
```
from langchain.tools import tool
from langchain.agents import create_agent

@tool
def search(query: str) -> str:
 """Search for information."""
 return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
 """Get weather information for a location."""
 return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(model, tools=[search, get_weather])

```

…

#### ​ Dynamic tools
With dynamic tools, the set of tools available to the agent is modified at runtime rather than defined all upfront. Not every tool is appropriate for every situation. Too many tools may overwhelm the model (overload context) and increase errors; too few limit capabilities. Dynamic tool selection enables adapting the available toolset based on authentication state, user permissions, feature flags, or conversation stage. There are two approaches depending on whether tools are known ahead of time: - Filtering pre-registered tools
- Runtime tool registration
When all possible tools are known at agent creation time, you can pre-register them and dynamically filter which ones are exposed to the model based on state, permissions, or context.
- State
- Store
- Runtime Context

Enable advanced tools only after certain conversation milestones:
```
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_model_call, ModelRequest, ModelResponse
from typing import Callable

@wrap_model_call
def state_based_tools(
 request: ModelRequest,
 handler: Callable[[ModelRequest], ModelResponse]
) -> ModelResponse:
 """Filter tools based on conversation State."""
 # Read from State: check if user has authenticated
 state = request.state
 is_authenticated = state.get("authenticated", False)
 message_count = len(state["messages"])

 # Only enable sensitive tools after authentication
 if not is_authenticated:
 tools = [t for t in request.tools if t.name.startswith("public_")]
 request = request.override(tools=tools)
 elif message_count < 5:
 # Limit tools early in conversation
 tools = [t for t in request.tools if t.name != "advanced_search"]
 request = request.override(tools=tools)

 return handler(request)

agent = create_agent(
 model="gpt-4.1",
 tools=[public_search, private_search, advanced_search],
 middleware=[state_based_tools]
)

```

…

#### ​ Tool use in the ReAct loop
Agents follow the ReAct (“Reasoning + Acting”) pattern, alternating between brief reasoning steps with targeted tool calls and feeding the resulting observations into subsequent decisions until they can deliver a final answer.

Example of ReAct loop

**Prompt:** Identify the current most popular wireless headphones and verify availability.

…

### ​ System prompt
You can shape how your agent approaches tasks by providing a prompt. The `system_prompt` parameter can be provided as a string:
```
agent = create_agent(
 model,
 tools,
 system_prompt="You are a helpful assistant. Be concise and accurate."
)

```
When no `system_prompt` is provided, the agent will infer its task from the messages directly. The `system_prompt` parameter accepts either a `str` or a `SystemMessage`. Using a `SystemMessage` gives you more control over the prompt structure, which is useful for provider-specific features like Anthropic’s prompt caching:
```
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage

literary_agent = create_agent(
 model="anthropic:claude-sonnet-4-5",
 system_prompt=SystemMessage(
 content=[
 {
 "type": "text",
 "text": "You are an AI assistant tasked with analyzing literary works.",
 },
 {
 "type": "text",
 "text": "<the entire contents of 'Pride and Prejudice'>",
 "cache_control": {"type": "ephemeral"}
 }
 ]
 )
)

result = literary_agent.invoke(
 {"messages": [HumanMessage("Analyze the major themes in 'Pride and Prejudice'.")]}
)

```

…

```
from typing import TypedDict

from langchain.agents import create_agent
from langchain.agents.middleware import dynamic_prompt, ModelRequest

class Context(TypedDict):
 user_role: str

@dynamic_prompt
def user_role_prompt(request: ModelRequest) -> str:
 """Generate system prompt based on user role."""
 user_role = request.runtime.context.get("user_role", "user")
 base_prompt = "You are a helpful assistant."

 if user_role == "expert":
 return f"{base_prompt} Provide detailed technical responses."
 elif user_role == "beginner":
 return f"{base_prompt} Explain concepts simply and avoid jargon."

 return base_prompt

agent = create_agent(
 model="gpt-4.1",
 tools=[web_search],
 middleware=[user_role_prompt],
 context_schema=Context
)

# The system prompt will be set dynamically based on context
result = agent.invoke(
 {"messages": [{"role": "user", "content": "Explain machine learning"}]},
 context={"user_role": "expert"}
)

```

### ​ Name
Set an optional `name` for the agent. This is used as the node identifier when adding the agent as a subgraph in multi-agent systems:
```
agent = create_agent(
 model,
 tools,
 name="research_assistant"
)

```

…

For streaming steps and / or tokens from the agent, refer to the streaming guide. Otherwise, the agent follows the LangGraph Graph API and supports all associated methods, such as `stream` and `invoke`.

…

```
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class ContactInfo(BaseModel):
 name: str
 email: str
 phone: str

agent = create_agent(
 model="gpt-4.1-mini",
 tools=[search_tool],
 response_format=ToolStrategy(ContactInfo)
)

result = agent.invoke({
 "messages": [{"role": "user", "content": "Extract contact info from: John Doe, john@example.com, (555) 123-4567"}]
})

result["structured_response"]
# ContactInfo(name='John Doe', email='john@example.com', phone='(555) 123-4567')

```

…

### ​ Memory
Agents maintain conversation history automatically through the message state. You can also configure the agent to use a custom state schema to remember additional information during the conversation. Information stored in the state can be thought of as the short-term memory of the agent: Custom state schemas must extend `AgentState` as a `TypedDict`. There are two ways to define custom state: 1. Via middleware (preferred)
2. Via `state_schema` on `create_agent`

…

```
from langchain.agents import AgentState
from langchain.agents.middleware import AgentMiddleware
from typing import Any

class CustomState(AgentState):
 user_preferences: dict

class CustomMiddleware(AgentMiddleware):
 state_schema = CustomState
 tools = [tool1, tool2]

 def before_model(self, state: CustomState, runtime) -> dict[str, Any] | None:
 ...

agent = create_agent(
 model,
 tools=tools,
 middleware=[CustomMiddleware()]
)

# The agent can now track additional state beyond messages
result = agent.invoke({
 "messages": [{"role": "user", "content": "I prefer technical explanations"}],
 "user_preferences": {"style": "technical", "verbosity": "detailed"},
})

```

…

```
from langchain.agents import AgentState

class CustomState(AgentState):
 user_preferences: dict

agent = create_agent(
 model,
 tools=[tool1, tool2],
 state_schema=CustomState
)
# The agent can now track additional state beyond messages
result = agent.invoke({
 "messages": [{"role": "user", "content": "I prefer technical explanations"}],
 "user_preferences": {"style": "technical", "verbosity": "detailed"},
})

```

…

```
from langchain.messages import AIMessage, HumanMessage

for chunk in agent.stream({
 "messages": [{"role": "user", "content": "Search for AI news and summarize the findings"}]
}, stream_mode="values"):
 # Each chunk contains the full state at that point
 latest_message = chunk["messages"][-1]
 if latest_message.content:
 if isinstance(latest_message, HumanMessage):
 print(f"User: {latest_message.content}")
 elif isinstance(latest_message, AIMessage):
 print(f"Agent: {latest_message.content}")
 elif latest_message.tool_calls:
 print(f"Calling tools: {[tc['name'] for tc in latest_message.tool_calls]}")

```

### ​ Middleware
Middleware provides powerful extensibility for customizing agent behavior at different stages of execution. You can use middleware to: - Process state before the model is called (e.g., message trimming, context injection)
- Modify or validate the model’s response (e.g., guardrails, content filtering)
- Handle tool execution errors with custom logic
- Implement dynamic model selection based on state or context
- Add custom logging, monitoring, or analytics
Middleware integrates seamlessly into the agent’s execution, allowing you to intercept and modify data flow at key points without changing the core agent logic.

## Overview
In this tutorial we will build a retrieval agent using LangGraph.
LangChain offers built-in agent implementations, implemented using LangGraph primitives.
If deeper customization is required, agents can be implemented directly in LangGraph.
This guide demonstrates an example implementation of a retrieval agent.
Retrieval agents are useful when you want an LLM to make a decision about whether to retrieve context from a vectorstore or respond to the user directly.
By the end of the tutorial we will have done the following:1.
Fetch and preprocess documents that will be used for retrieval.
2. Index those documents for semantic search and create a retriever tool for the agent.
3. Build an agentic RAG system that can decide when to use the retriever tool.
### Concepts
We will cover the following concepts:- Retrieval using document loaders, text splitters, embeddings, and vector stores
- The LangGraph Graph API, including state, nodes, edges, and conditional edges.
## Setup
Let’s download the required packages and set our API keys:
…
## 1.
Preprocess documents
1. Fetch documents to use in our RAG system.
We will use three of the most recent pages from Lilian Weng’s excellent blog.
We’ll start by fetching the content of the pages using
…
```
from langchain_community.document_loaders import WebBaseLoader
urls = [
"https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
"https://lilianweng.github.io/posts/2024-07-07-hallucination/",
"https://lilianweng.github.io/posts/2024-04-12-diffusion-video/",
docs = [WebBaseLoader(url).load() for url in urls]
```
…
## 3.
Generate query
Now we will start building components (nodes and edges) for our agentic RAG graph.
Note that the components will operate on the
…
key with a list of chat messages.
1. Build a
…
node.
It will call an LLM to generate a response based on the current graph state (list of messages).
Given the input messages, it will decide to retrieve using the retriever tool, or respond directly to the user.
Note that we’re giving the chat model access to the
…
```
from langgraph.graph import MessagesState
from langchain.chat_models import init_chat_model
response_model = init_chat_model("gpt-4.1", temperature=0)
def generate_query_or_respond(state: MessagesState):
"""Call the model to generate a response based on the current state.
Given
the question, it will decide to retrieve using the retriever tool, or simply respond to the user.
"""
response = (
response_model
.bind_tools([retriever_tool]).invoke(state["messages"])
)
return {"messages": [response]}
```
…
```
input = {"messages": [{"role": "user", "content": "hello!"}]}
generate_query_or_respond(input)["messages"][-1].pretty_print()
```
…
```
from langchain.messages import HumanMessage
REWRITE_PROMPT = (
"Look at the input and try to reason about the underlying semantic intent / meaning.\n"
"Here is the initial question:"
"\n ------- \n"
"{question}"
"\n ------- \n"
"Formulate an improved question:"
def rewrite_question(state: MessagesState):
"""Rewrite the original user question."""
messages = state["messages"]
question = messages[0].content
prompt = REWRITE_PROMPT.format(question=question)
response = response_model.invoke([{"role": "user", "content": prompt}])
return {"messages": [HumanMessage(content=response.content)]}
```
…
```
GENERATE_PROMPT = (
"You are an assistant for question-answering tasks.
"
"Use the following pieces of retrieved context to answer the question.
"
"If you don't know the answer, just say that you don't know.
"
"Use three sentences maximum and keep the answer concise.\n"
"Question: {question} \n"
"Context: {context}"
def generate_answer(state: MessagesState):
"""Generate an answer."""
question = state["messages"][0].content
context = state["messages"][-1].content
prompt = GENERATE_PROMPT.format(question=question, context=context)
response = response_model.invoke([{"role": "user", "content": prompt}])
return {"messages": [response]}
```
…
## 7.
Assemble the graph
Now we’ll assemble all the nodes and edges into a complete graph:- Start with a
…
to retrieve context
- Otherwise, respond directly to the user
- If
- Grade retrieved document content for relevance to the question (
…
```
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
workflow = StateGraph(MessagesState)
# Define the nodes we will cycle between
workflow.add_node(generate_query_or_respond)
workflow.add_node("retrieve", ToolNode([retriever_tool]))
workflow.add_node(rewrite_question)
workflow.add_node(generate_answer)
workflow.add_edge(START, "generate_query_or_respond")
# Decide whether to retrieve
workflow.add_conditional_edges(
"generate_query_or_respond",
# Assess LLM decision (call `retriever_tool` tool or respond to the user)
tools_condition,
{
# Translate the condition outputs to nodes in our graph
"tools": "retrieve",
END: END,
},
# Edges taken after the `action` node is called.
workflow.add_conditional_edges(
"retrieve",
# Assess agent decision
grade_documents,
workflow.add_edge("generate_answer", END)
workflow.add_edge("rewrite_question", "generate_query_or_respond")
# Compile
graph = workflow.compile()
```
…
```
for chunk in graph.stream(
{
"messages": [
{
"role": "user",
"content": "What does Lilian Weng say about types of reward hacking?",
}
]
}
):
for node, update in chunk.items():
print("Update from node", node)
update["messages"][-1].pretty_print()
print("\n\n")
```

# LangGraph quickstart¶
This guide shows you how to set up and use LangGraph's
**prebuilt**, **reusable** components, which are designed to help you construct agentic systems quickly and reliably.
…
## 2.
Create an agent¶
To create an agent, use
`create_react_agent`:
*API Reference: create_react_agent*
```
from langgraph.prebuilt import create_react_agent
def get_weather(city: str) -> str: # (1)!
"""Get weather for a given city."""
return f"It's always sunny in {city}!"
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest", # (2)!
tools=[get_weather], # (3)!
prompt="You are a helpful assistant" # (4)!
# Run the agent
agent.invoke(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]}
```
- Define a tool for the agent to use.
Tools can be defined as vanilla Python functions.
For more advanced tool usage and customization, check the tools page.
- Provide a language model for the agent to use.
To learn more about configuring language models for the agents, check the models page.
- Provide a list of tools for the model to use.
- Provide a system prompt (instructions) to the language model used by the agent.
…
```
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import create_react_agent
model = init_chat_model(
"anthropic:claude-3-7-sonnet-latest",
temperature=0
agent = create_react_agent(
model=model,
tools=[get_weather],
```
…
## 4.
Add a custom prompt¶
Prompts instruct the LLM how to behave.
Add one of the following types of prompts:
**Static**: A string is interpreted as a **system message**.
**Dynamic**: A list of messages generated at **runtime**, based on input or configuration.
Define a fixed prompt string or list of messages:
```
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
# A static prompt that never changes
prompt="Never answer questions about the weather."
agent.invoke(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]}
```
Define a function that returns a message list based on the agent's state and configuration:
```
from langchain_core.messages import AnyMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.chat_agent_executor import AgentState
from langgraph.prebuilt import create_react_agent
def prompt(state: AgentState, config: RunnableConfig) -> list[AnyMessage]: # (1)!
user_name = config["configurable"].get("user_name")
system_msg = f"You are a helpful assistant.
Address the user as {user_name}."
return [{"role": "system", "content": system_msg}] + state["messages"]
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
prompt=prompt
agent.invoke(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]},
config={"configurable": {"user_name": "John Smith"}}
```
…
`state`and
`config`and return a list of messages to send to the LLM.
- Information passed at runtime, like a
For more information, see Context.
…
```
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
checkpointer=checkpointer # (1)!
# Run the agent
config = {"configurable": {"thread_id": "1"}}
sf_response = agent.invoke(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]},
config # (2)!
ny_response = agent.invoke(
{"messages": [{"role": "user", "content": "what about new york?"}]},
config
```
`checkpointer`allows the agent to store its state at every step in the tool calling loop.
This enables short-term memory and human-in-the-loop capabilities.
- Pass configuration with
`thread_id`to be able to resume the same conversation on future agent invocations.
When you enable the checkpointer, it stores agent state at every step in the provided checkpointer database (or in memory, if using
…
## 6.
Configure structured output¶
To produce structured responses conforming to a schema, use the
`response_format` parameter.
The schema can be defined with a
`Pydantic` model or
`TypedDict`.
The result will be accessible via the
`structured_response` field.
*API Reference: create_react_agent*
```
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent
class WeatherResponse(BaseModel):
conditions: str
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
response_format=WeatherResponse # (1)!
response = agent.invoke(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]}
response["structured_response"]
```
- When
`response_format`is provided, a separate step is added at the end of the agent loop: agent message history is passed to an LLM with structured output to generate a structured response.
`To provide a system prompt to this LLM, use a tuple `(prompt, schema)`, e.g., `response_format=(prompt, WeatherResponse)`.`

The idea behind the agent in LangChain is to use an LLM and a sequence of actions; the agent then uses a reasoning engine to decide which action to take. LangChain was useful for simple agents with straightforward chains and retrieval flows, but building more complex agentic systems was overly complicated-memory management, persistence, and human-in-the-loop components were implemented manually, rendering chains and agents less flexible.
This is where LangGraph comes into play. LangGraph is an orchestration framework built by LangChain. LangGraph allows you to develop agentic LLM applications using a graph structure, which can be used with or without LangChain.

This article focuses on building agents with LangGraph rather than LangChain. It provides a tutorial for building LangGraph agents, beginning with a discussion of LangGraph and its components. These concepts are reinforced by building a LangGraph agent from scratch and managing conversation memory with LangGraph agents. Finally, we use Zep's long-term memory for egents to create an agent that remembers previous conversations and user facts.

…

|Concept|Description|
|--|--|
|What is LangGraph?|LangGraph is an AI agent framework that implements agent interactions as stateful graphs. Nodes represent functions or computational steps that are connected via edges. LangGraph maintains an agent state shared among all the nodes and edges. Unlike LangChain, LangGraph supports the implementation of more complex agentic workflows. Key features include built-in persistence, support for human intervention, and the ability to handle complex workflows with cycles and branches.|
|Building a LangGraph agent|Creating a LangGraph agent is the best way to understand the core concepts of nodes, edges, and state. The LangGraph Python libraries are modular and provide the functionality to build a stateful graph by incrementally adding nodes and edges. Incorporating tools enables an agent to perform specific tasks and access external information. For example, the **ArXiv** tool wrapper can return content from research papers. LangGraph offers a prebuilt reason and act (ReACT) agent that can help you get started.|

…

## What is LangGraph?

LangGraph is an AI agent framework built on LangChain that allows developers to create more sophisticated and flexible agent workflows. Unlike traditional LangChain chains and agents, LangGraph implements agent interactions as cyclic graphs with multiple-step processing involving branching and loops. This eliminates the need to implement custom logic to control the flow of information between multiple agents in the workflow.

### How LangGraph works

As the name suggests, LangGraph is a graph workflow consisting of nodes and edges. The nodes implement functionality within the workflow while the edges control its direction.

The following diagram best explains how LangGraph works at a high level.

A high-level overview of a LangGraph agent and its components

A LangGraph agent receives input, which can be a user input or input from another LangGraph agent. Typically, an LLM agent processes the input and decides whether it needs to call one or more tools, but it can directly generate a response and proceed to the next stage in the graph.
If the agent decides to call one or more tools, the tool processes the agent output and returns the response to the agent. The agent then generates its response based on the tool output. Once an agent finalizes its response, you can further add an optional "human-in-the-loop" step to refine the agent response before returning the final output.

…

### Persistence

One key LangGraph feature that distinguishes it from traditional LangChain agents is its built-in persistence mechanism. LangGraph introduces the concept of an agent state shared among all the nodes and edges in a workflow. This allows automatic error recovery, enabling the workflow to resume where it left off.

In addition to the agent state memory, LangGraph supports persisting conversation histories using short-term and long-term memories, which are covered in detail later in the article.

### Cycles

LangGraph introduces cycling graphs, allowing agents to communicate with tools in a cyclic manner. For example, an agent may call a tool, retrieve information from the tool, and then call the same or another tool to retrieve follow-up information. Similarly, tools may call each other multiple times to share and refine information before passing it back to an agent. This differentiates it from DAG-based solutions.

### Human-in-the-loop capability

LangGraph supports human intervention in agent workflows, which interrupts graph execution at specific points, allowing humans to review, approve, or edit the agent's proposed response. The workflow resumes after receiving human input.

This feature fosters greater control and oversight in critical decision-making processes in an agent's workflow.

…

### Understanding nodes, edges, and state

If you are new to LangGraph, you must understand a few terms before creating an agent: nodes, edges, and state.

A simple graph in LangGraph showing nodes, edges, and states (source)

**Nodes**

Nodes are the building blocks of your agents and represent a discrete computation unit within your agent's workflow. A node can be as simple as a small Python function or as complex as an independent agent that calls external tools.
**Edges**

Edges connect nodes and define how your agent progresses from one step to the next. Edges can be of two types: direct and conditional. A direct edge simply connects two nodes without any condition, whereas a conditional node is similar to an if-else statement and connects two nodes based on a condition.

**State**
A state is LangGraph's most underrated yet most essential component. It contains all the data and context available to different entities, such as nodes and edges. Simply put, the state shares data and context among all nodes and edges in a graph.

## Building a LangGraph agent

Enough with the theory-in this section, you will see all the building blocks of LangGraph agents in action. You will learn how to:

- Create a LangGraph agent from scratch
- Incorporate tools into LangGraph agents
- Stream agent responses
- Use built-in agents

…

```
[object Object] langchain_openai [object Object] ChatOpenAI
[object Object] langchain_core.messages [object Object] AnyMessage, SystemMessage, HumanMessage, ToolMessage, AIMessage, trim_messages
[object Object] langchain_core.tools [object Object] tool, ToolException, InjectedToolArg
[object Object] langchain_core.runnables [object Object] RunnableConfig
[object Object] langchain_community.utilities [object Object] ArxivAPIWrapper
[object Object] langchain_community.tools [object Object] ArxivQueryRun, HumanInputRun
[object Object] langgraph.graph [object Object] StateGraph,START,END, add_messages, MessagesState
[object Object] langgraph.prebuilt [object Object] create_react_agent, ToolNode
[object Object] langgraph.checkpoint.memory [object Object] MemorySaver
[object Object] langgraph.store.base [object Object] BaseStore
[object Object] langgraph.store.memory [object Object] InMemoryStore
[object Object] typing [object Object] Annotated, [object Object]
[object Object] typing_extensions [object Object] TypedDict
[object Object] pydantic [object Object] BaseModel, Field
[object Object] wikipedia
[object Object] uuid
[object Object] operator
[object Object] IPython.display [object Object] Image, display
[object Object] os
[object Object] google.colab [object Object] userdata

```

…

This defines a simple state that stores a list of any type of LangChain message, such as ToolMessage, AIMessage, HumanMessage, etc. The **operator.add** operator will add new messages to the list instead of overwriting existing ones.

Next, we will define a simple Python function to add a node in our LangGraph agent.

…

The **run_llm()** function accepts an object of the **State** class that we defined before. When we add the **run_llm()** function to a LangGraph node, LangGraph will automatically pass the agent's state to the **run_llm()** function.

Let's now create our graph.

…

To create a graph, we will create a **StateGraph** object and define the state type in the **StateGraph** constructor. Subsequently, we will add a node titled **llm** and add the **run_llm()** function to the node.

We add two edges that define the start and end of the agent execution. Our agent has a single node, so we start with the **llm** node and end the agent execution once we receive the response from the **llm** node.

…

```
messages = [HumanMessage(content=[object Object])]
result = graph.invoke({[object Object]: messages})
[object Object](result[[object Object]][-[object Object]].content)

```

…

```
[object Object] [object Object]([object Object]):
    tool_calls = state[[object Object]][-[object Object]].tool_calls
    results = []
    [object Object] t [object Object] tool_calls:

      [object Object] [object Object] t[[object Object]] [object Object] tools_names:
        result = [object Object]
      [object Object]:
        result = tools_names[t[[object Object]]].invoke(t[[object Object]])

        results.append(
          ToolMessage(
            tool_call_id=t[[object Object]],
            name=t[[object Object]],
            content=[object Object](result)
          )
        )

    [object Object] {[object Object]: results}

```
The **execute_tools** function above will be added to a LangGraph agent's node, automatically receiving the agent's current state. We will only call the **execute_tools()** function if the agent decides to use one or more tools.

Inside the **execute_tools** function, we will iteratively call the tools and pass the arguments from the LLM's last response to them. Finally, we will append the tool response to the **results[]** list and add the list to the model state using the state's **messages** list.

…

We will use this function to create a conditional edge, which decides whether to go to the **execute_tools()** function or the END node and returns the agent's final response.

Now let's create a LangGraph agent that uses the tool we created. The following script defines the agent's state and the **run_llm()** function as before.

…

```
graph_builder=StateGraph(State)
graph_builder.add_node([object Object], run_llm)
graph_builder.add_node([object Object], execute_tools)
graph_builder.add_conditional_edges(
    [object Object],
     tool_exists,
    {[object Object]: [object Object], [object Object]: END}
    )

graph_builder.add_edge([object Object], [object Object])

graph_builder.set_entry_point([object Object])

graph=graph_builder.[object Object]()

display(Image(graph.get_graph().draw_mermaid_png()))

```
Here is how the graph looks:

We have two nodes in the graph: the **llm**, which runs the **run_llm()** function, and the **tools** node, which runs the **execute_tools()** function. The conditional node connects the **llm** node with the **tool** or the END node depending upon the output of the **llm** node. We also add an edge back from the **tools** to the **llm** node because we want the **llm** node to generate the final response with or without the help of the tool.

…

### Streaming agent responses

You can also stream the individual responses from all nodes and edges in your LangGraph agent. Streaming messages allows users to receive responses in real-time. To do so, you can call the **stream()** function instead of the **invoke()** method.

Let's define a function that receives streaming agent response and displays it on the console.
```
[object Object] [object Object]([object Object]):
    [object Object] s [object Object] stream:
        message = s[[object Object]][-[object Object]]
        [object Object] [object Object](message, [object Object]):
            [object Object](message)
        [object Object]:
            message.pretty_print()

```
Next, call **graph().stream()** and pass it the input messages. Also set the attribute **stream_mode** to **values**, which displays the values of the streaming agent responses.
```
messages = [HumanMessage(content=[object Object])]
print_stream(graph.stream({[object Object]: messages}, stream_mode= [object Object]))

```
You will see real-time responses from each graph node printed on the console. For example, in the output above, you can see the human message followed by the AI response, which contains tool calls to the **wikipedia_search** tool. The tool returns the response to the user query; this is again passed to the AI node, which generates the final response.

…

### Putting it all together: a LangGraph agent with Zep

Now that you know how Zep's long-term memory works, let's look at how to develop an agent using LangGraph agents that employ Zep's long-term memory to store user facts. The agent responses will be based on the user facts from Zep's memory.

We will define a graph state that stores messages originating from different nodes, user names, and thread IDs. Next, we will create the **search_facts** tool, which uses the Zep client's **graph.search()** method to find user facts relevant to the query.

This page shows you how to develop an agent by using the framework-specific
LangGraph template (the `LanggraphAgent` class in the Vertex AI SDK for Python). The agent returns the exchange rate between two currencies on a specified date. Here are the steps:

1. Define and configure a model
2. Define and use a tool
3. (Optional) Store checkpoints
4. (Optional) Customize the prompt template
5. (Optional) Customize the orchestration

…

```
model_kwargs = {
# temperature (float): The sampling temperature controls the degree of
# randomness in token selection.
"temperature": 0.28,
# max_output_tokens (int): The token limit determines the maximum amount of
# text output from one prompt.
"max_output_tokens": 1000,
# top_p (float): Tokens are selected from most probable to least until
# the sum of their probabilities equals the top-p value.
"top_p": 0.95,
# top_k (int): The next token is selected from among the top-k most
# probable tokens. This is not supported by all model versions. See
# https://cloud.google.com/vertex-ai/generative-ai/docs/multimodal/image-understanding#valid_parameter_values
# for details.
"top_k": None,
# safety_settings (Dict[HarmCategory, HarmBlockThreshold]): The safety
# settings to use for generating content.
# (you must create your safety settings using the previous step first).
"safety_settings": safety_settings,
}

```

…

```
{
'messages': [{
'id': ['langchain', 'schema', 'messages', 'HumanMessage'],
'kwargs': {
'content': 'What is the exchange rate from US dollars to Swedish currency?',
'id': '5473dd25-d796-42ad-a690-45bc49a64bec',
'type': 'human',
},
'lc': 1,
'type': 'constructor',
}, {
'id': ['langchain', 'schema', 'messages', 'AIMessage'],
'kwargs': {
'content': """
 I do not have access to real-time information, including currency exchange rates.

 To get the most up-to-date exchange rate from US dollars to Swedish currency (SEK),
 I recommend checking a reliable online currency converter like: ...

 These websites will provide you with the current exchange rate and allow you to
 convert specific amounts.""",
'id': 'run-c42f9940-8ba8-42f1-a625-3aa0780c9e87-0',
...
'usage_metadata': {
'input_tokens': 12,
'output_tokens': 145,
'total_tokens': 157,
},
},
'lc': 1,
'type': 'constructor',
}],
}

```

### (Optional) Advanced customization

The `LanggraphAgent` template uses `ChatVertexAI` by default, because it provides access to all foundational models available in Google Cloud. To use a model that is not available through `ChatVertexAI`, you can specify the `model_builder=` argument,
with a Python function of the following signature:

…

For a list of the chat models supported in LangChain and their capabilities, see
Chat Models. The set of supported values for `model=` and `model_kwargs=` are specific to
each chat model, so you have to refer to their corresponding documentation for
details.

…

```
def model_builder(*, model_name: str, model_kwargs = None, **kwargs):
from langchain_anthropic import ChatAnthropic
return ChatAnthropic(model_name=model_name, **model_kwargs)

```

…

```
from vertexai import agent_engines

agent = agent_engines.LanggraphAgent(
model="claude-3-opus-20240229", # Required.
model_builder=model_builder, # Required.
model_kwargs={
"api_key": "ANTHROPIC_API_KEY", # Required.
"temperature": 0.28, # Optional.
"max_tokens": 1000, # Optional.
},
)

```

…

## Step 2. Define and use a tool

After you define your model, the next step is to define the tools that your
model uses for reasoning. A tool can be a
LangChain tool or a Python function. You can also convert a defined Python function to a LangChain Tool.

When you define your function, it's important to include comments that fully and
clearly describe the function's parameters, what the function does, and what the
function returns. This information is used by the model to determine which
function to use. You must also test your function locally to confirm that it
works.

…

```
from vertexai import agent_engines

agent = agent_engines.LanggraphAgent(
model=model,
tools=[generate_and_execute_code],
)
response = agent.query(input={"messages": [("user", """
 Using the data below, construct a bar chart that includes only the height values with different colors for the bars:

 tree_heights_prices = {
 \"Pine\": {\"height\": 100, \"price\": 100},
 \"Oak\": {\"height\": 65, \"price\": 135},
 \"Birch\": {\"height\": 45, \"price\": 80},
 \"Redwood\": {\"height\": 200, \"price\": 200},
 \"Fir\": {\"height\": 180, \"price\": 162},
 }
""")]})

print(response)

```

…

from vertexai import agent_engines

agent = agent_engines.LanggraphAgent(
model=model,
tools=[
get_exchange_rate, # Optional (Python function)
grounded_search_tool, # Optional (Grounding Tool)
movie_search_tool, # Optional (Langchain Tool)
generate_and_execute_code, # Optional (Vertex Extension)
],
)

…

```

For details, visit Tool Configuration.

## Step 3. Store checkpoints

To track chat messages and append them to a database, define a
`checkpointer_builder` function and pass it in when you create the agent.

### Set up a database

First, install and use the relevant package to set up a database of your choice (e.g. AlloyDB for PostgreSQL, or Cloud SQL for PostgreSQL):

- AlloyDB for PostgreSQL
- Cloud SQL for PostgreSQL

Next, define a `checkpointer_builder` function as follows:

### Cloud SQL for PostgreSQL

```

…

```

## Step 4. Customize the prompt template

Prompt templates help to translate user input into instructions for a model, and
are used to guide a model's response, helping it understand the context and
generate relevant and coherent language-based output. For details, visit
ChatPromptTemplates.

The default prompt template is organized sequentially into sections.

|Section|Description|
|--|--|
|(Optional) System instruction|Instructions for the agent to be applied across all queries.|
|(Optional) Chat history|Messages corresponding to the chat history from a past session.|
|User input|The query from the user for the agent to respond to.|
|Agent Scratchpad|Messages created by the agent (e.g. with function calling) as it performs uses its tools and performs reasoning to formulate a response to the user.|

The default prompt template is generated if you create the agent without
specifying your own prompt template, and will look like the following in full:

```

…

```

## Step 5. Customize the orchestration

All LangChain components implement the Runnable interface, which provide input and output schemas for orchestration. The `LanggraphAgent` class requires a runnable to be built for it to respond to queries. By default, `LanggraphAgent` will build such a runnable by using the prebuilt react agent implementation from langgraph.

You might want to customize the orchestration if you intend to (i) implement an
agent that performs a deterministic set of steps (rather than to perform
open-ended reasoning), or (ii) prompt the Agent in a ReAct-like fashion to
annotate each step with thoughts for why it performed that step. To do so, you
have to override the default runnable when creating `LanggraphAgent` by specifying the `runnable_builder=` argument with a Python function of the
following signature:

```

…

```

where

- `model` corresponds to the chat model being returned from the `model_builder`
  (see Define and configure a model),
- `tools` corresponds to the tools and configurations to be used (see
  Define and use a tool),
- `checkpointer` corresponds to the database for storing checkpoints (see
  Store checkpoints),
- `system_instruction` and `prompt` corresponds to the prompt configuration (see
  Customize the prompt template),
- `runnable_kwargs` are the keyword arguments you can use for customizing the
  runnable to be built.

This gives different options for customizing the orchestration logic.

### ChatModel

In the simplest case, to create an agent without orchestration, you can
override the `runnable_builder` for `LanggraphAgent` to return the `model`
directly.

```

…

agent = create_react_agent(model, tools, prompt)
return AgentExecutor(agent=agent, tools=tools, **agent_executor_kwargs)

agent = agent_engines.LanggraphAgent(
model=model,
tools=[get_exchange_rate],
prompt=hub.pull("hwchase17/react"),
agent_executor_kwargs={"verbose": True}, # Optional. For illustration.
runnable_builder=react_builder,
)

…

from vertexai import agent_engines

def langgraph_builder(*, model, **kwargs):
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, MessageGraph

output_parser = StrOutputParser()

planner = ChatPromptTemplate.from_template(
"Generate an argument about: {input}"
) | model | output_parser

…

builder = MessageGraph()
builder.add_node("planner", planner)
builder.add_node("pros", pros)
builder.add_node("cons", cons)
builder.add_node("summary", summary)

builder.add_edge("planner", "pros")
builder.add_edge("planner", "cons")
builder.add_edge("pros", "summary")
builder.add_edge("cons", "summary")
builder.add_edge("summary", END)
builder.set_entry_point("planner")
return builder.compile()