# Source: https://github.com/langchain-ai/langgraph/discussions/3346
# Author: LangChain
# Author Slug: langchain
# Title: Dynamic Workflow Mode Implementation for Conditional Edges (langgraph discussion #3346)
# Fetched via: search
# Date: 2026-04-10

Trusted by companies shaping the future of agents— including Klarna, Uber, J.P. Morgan, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.
LangGraph is very low-level, and focused entirely on agent **orchestration**.
Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with models and tools.
We will commonly use LangChain components throughout the documentation to integrate models and tools, but you don’t need to use LangChain to use LangGraph.
If you are just getting started with agents or want a higher-level abstraction, we recommend you use LangChain’s agents that provide prebuilt architectures for common LLM and tool-calling loops.
LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.
…
Then, create a simple hello world example:
```
from langgraph.graph import StateGraph, MessagesState, START, END
def mock_llm(state: MessagesState):
return {"messages": [{"role": "ai", "content": "hello world"}]}
graph = StateGraph(MessagesState)
graph.add_node(mock_llm)
graph.add_edge(START, "mock_llm")
graph.add_edge("mock_llm", END)
graph = graph.compile()
graph.invoke({"messages": [{"role": "user", "content": "hi!"}]})
```
## ​ Core benefits
LangGraph provides low-level supporting infrastructure for *any* long-running, stateful workflow or agent.
LangGraph does not abstract prompts or architecture, and provides the following central benefits: - Durable execution: Build agents that persist through failures and can run for extended periods, resuming from where they left off.
- Human-in-the-loop: Incorporate human oversight by inspecting and modifying agent state at any point.
- Comprehensive memory: Create stateful agents with both short-term working memory for ongoing reasoning and long-term memory across sessions.
- Debugging with LangSmith: Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
…
## ​ LangGraph ecosystem
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents.
To improve your LLM application development, pair LangGraph with:
## LangSmith Observability
Trace requests, evaluate outputs, and monitor deployments in one place.
Prototype locally with LangGraph, then move to production with integrated observability and evaluation to build more reliable agent systems.
...
Deploy and scale agents effortlessly with a purpose-built deployment platform for long running, stateful workflows.
Discover, reuse, configure, and share agents across teams — and iterate quickly with visual prototyping in Studio.
...
Provides integrations and composable components to streamline LLM application development.
Contains agent abstractions built on top of LangGraph.
## ​ Acknowledgements
LangGraph is inspired by Pregel and Apache Beam.
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.
Edit this page on GitHub or file an issue.

langgraph
...
Design agents that reliably handle complex tasks with LangGraph, an agent runtime and low-level orchestration framework.
### How does LangGraph help?
...
Prevent agents from veering off course with easy-to-add moderation and quality controls.
Add human-in-the-loop checks to steer and approve agent actions.
...
LangGraph’s low-level primitives provide the flexibility needed to create fully customizable agents.
Design diverse control flows — single, multi-agent, hierarchical — all using one framework.
...
LangGraph’s built-in memory stores conversation histories and maintains context over time, enabling rich, personalized interactions across sessions.
Learn about agent memory
...
Bridge user expectations and agent capabilities with native token-by-token streaming, showing agent reasoning and actions in real time.
See how to use streaming
...
Learn the basics of LangGraph in this LangChain Academy Course.
You'll learn about how to leverage state, memory, human-in-the-loop, and more for your agents.
Enroll for free
...
Use high-level abstractions or fine-grained control as needed.
...
LangGraph provides a more expressive framework to handle companies’ unique tasks without restricting users to a single black-box cognitive architecture.
...
LangGraph will not add any overhead to your code and is specifically designed with streaming workflows in mind.
Is LangGraph open source?
Is it free?
Yes.
LangGraph is an MIT-licensed open-source library and is free to use.
### See what your agent is really doing

# LangGraph
Trusted by companies shaping the future of agents – including Klarna, Replit, Elastic, and more – LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents.
…
Then, create an agent using prebuilt components:
...
# pip install -qU "langchain[anthropic]" to call the model
from langgraph.prebuilt import create_react_agent
def get_weather(city: str) -> str:
"""Get weather for a given city."""
return f"It's always sunny in {city}!"
agent = create_react_agent(
model="anthropic:claude-3-7-sonnet-latest",
tools=[get_weather],
prompt="You are a helpful assistant"
# Run the agent
agent.invoke(
{"messages": [{"role": "user", "content": "what is the weather in sf"}]}
```
...
LangGraph provides low-level supporting infrastructure for
*any* long-running, stateful workflow or agent.
LangGraph does not abstract prompts or architecture, and provides the following central benefits:
- Durable execution: Build agents that persist through failures and can run for extended periods, automatically resuming from exactly where they left off.
- Human-in-the-loop: Seamlessly incorporate human oversight by inspecting and modifying agent state at any point during execution.
- Comprehensive memory: Create truly stateful agents with both short-term working memory for ongoing reasoning and long-term persistent memory across sessions.
- Debugging with LangSmith: Gain deep visibility into complex agent behavior with visualization tools that trace execution paths, capture state transitions, and provide detailed runtime metrics.
- Production-ready deployment: Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.
## LangGraph’s ecosystem¶
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents.
To improve your LLM application development, pair LangGraph with:
- LangSmith — Helpful for agent evals and observability.
...
- LangChain Academy: Learn the basics of LangGraph in our free, structured course.
...
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.

# 🚀 LangGraph Quickstart¶

In this tutorial, we will build a support chatbot in LangGraph that can:

**Answer common questions** by searching the web

**Maintain conversation state** across calls

**Route complex queries** to a human for review

**Use custom state** to control its behavior

**Rewind and explore** alternative conversation paths

…

## Part 1: Build a Basic Chatbot¶

We'll first create a simple chatbot using LangGraph. This chatbot will respond directly to user messages. Though simple, it will illustrate the core concepts of building with LangGraph. By the end of this section, you will have a built rudimentary chatbot.

Start by creating a

`StateGraph`. A

`StateGraph` object defines the structure of our chatbot as a "state machine". We'll add
`nodes` to represent the llm and functions our chatbot can call and

`edges` to specify how the bot should transition between these functions.

*API Reference: StateGraph | START | END | add_messages*

…

`Annotated`syntax.

Concept

When defining a graph, the first step is to define its

`State`. The

`State` includes the graph's schema and reducer functions that handle state updates. In our example,

`State` is a

`TypedDict` with one key:

`messages`. The

`add_messages` reducer function is used to append new messages to the list instead of overwriting it. Keys without a reducer annotation will overwrite previous values. Learn more about state, reducers, and related concepts in this guide.

…

**Notice** how the

`chatbot` node function takes the current

`State` as input and returns a dictionary containing an updated

`messages` list under the key "messages". This is the basic pattern for all LangGraph node functions.

The

`add_messages` function in our

`State` will append the llm's response messages to whatever messages are already in the state.

…

("anthropic:claude-3-5-sonnet-latest") def chatbot(state: State): return {"messages": [llm.invoke(state["messages"])]} # The first argument is the unique node name # The second argument is the function or object that will be called whenever # the node is used. graph_builder.add_node("chatbot", chatbot) graph_builder.set_entry_point("chatbot") graph_builder.set_finish_point("chatbot") graph = graph_builder.compile()`

…

```

{'query': "What's a 'node' in LangGraph?",

'follow_up_questions': None,

'answer': None,

'images': [],

'results': [{'title': "Introduction to LangGraph: A Beginner's Guide - Medium",

'url': 'https://medium.com/@cplog/introduction-to-langgraph-a-beginners-guide-14f9be027141',

'content': 'Stateful Graph: LangGraph revolves around the concept of a stateful graph, where each node in the graph represents a step in your computation, and the graph maintains a state that is passed around and updated as the computation progresses. LangGraph supports conditional edges, allowing you to dynamically determine the next node to execute based on the current state of the graph. We define nodes for classifying the input, handling greetings, and handling search queries. def classify_input_node(state): LangGraph is a versatile tool for building complex, stateful applications with LLMs. By understanding its core concepts and working through simple examples, beginners can start to leverage its power for their projects. Remember to pay attention to state management, conditional edges, and ensuring there are no dead-end nodes in your graph.',

'score': 0.7065353,

'raw_content': None},

{'title': 'LangGraph Tutorial: What Is LangGraph and How to Use It?',

'url': 'https://www.datacamp.com/tutorial/langgraph-tutorial',

'content': 'LangGraph is a library within the LangChain ecosystem that provides a framework for defining, coordinating, and executing multiple LLM agents (or chains) in a structured and efficient manner. By managing the flow of data and the sequence of operations, LangGraph allows developers to focus on the high-level logic of their applications rather than the intricacies of agent coordination. Whether you need a chatbot that can handle various types of user requests or a multi-agent system that performs complex tasks, LangGraph provides the tools to build exactly what you need. LangGraph significantly simplifies the development of complex LLM applications by providing a structured framework for managing state and coordinating agent interactions.',

'score': 0.5008063,

'raw_content': None}],

'response_time': 1.38}

```

…

```

from typing import Annotated

from langchain.chat_models import init_chat_model

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages

class State(TypedDict):

messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

# Modification: tell the LLM which tools it can call

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):

return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

```

…

```

def route_tools(

state: State,

):

"""

Use in the conditional_edge to route to the ToolNode if the last message

has tool calls. Otherwise, route to the end.

"""

if isinstance(state, list):

ai_message = state[-1]

elif messages := state.get("messages", []):

ai_message = messages[-1]

else:

raise ValueError(f"No messages found in input state to tool_edge: {state}")

if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:

return "tools"

return END

# The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if

# it is fine directly responding. This conditional routing defines the main agent loop.

graph_builder.add_conditional_edges(

"chatbot",

route_tools,

# The following dictionary lets you tell the graph to interpret the condition's outputs as a specific node

# It defaults to the identity function, but if you

# want to use a node named something else apart from "tools",

# You can update the value of the dictionary to something else

# e.g., "tools": "my_tools"

{"tools": "tools", END: END},



# Any time a tool is called, we return to the chatbot to decide the next step

graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge(START, "chatbot")

graph = graph_builder.compile()

```

…

```

Assistant: [{'text': "To provide you with accurate and up-to-date information about LangGraph, I'll need to search for the latest details. Let me do that for you.", 'type': 'text'}, {'id': 'toolu_01Q588CszHaSvvP2MxRq9zRD', 'input': {'query': 'LangGraph AI tool information'}, 'name': 'tavily_search_results_json', 'type': 'tool_use'}]

Assistant: [{"url": "https://www.langchain.com/langgraph", "content": "LangGraph sets the foundation for how we can build and scale AI workloads \u2014 from conversational agents, complex task automation, to custom LLM-backed experiences that 'just work'. The next chapter in building complex production-ready features with LLMs is agentic, and with LangGraph and LangSmith, LangChain delivers an out-of-the-box solution ..."}, {"url": "https://github.com/langchain-ai/langgraph", "content": "Overview. LangGraph is a library for building stateful, multi-actor applications with LLMs, used to create agent and multi-agent workflows. Compared to other LLM frameworks, it offers these core benefits: cycles, controllability, and persistence. LangGraph allows you to define flows that involve cycles, essential for most agentic architectures ..."}]

Assistant: Based on the search results, I can provide you with information about LangGraph:

1. Purpose:

LangGraph is a library designed for building stateful, multi-actor applications with Large Language Models (LLMs). It's particularly useful for creating agent and multi-agent workflows.

2. Developer:

LangGraph is developed by LangChain, a company known for its tools and frameworks in the AI and LLM space.

3. Key Features:

- Cycles: LangGraph allows the definition of flows that involve cycles, which is essential for most agentic architectures.

- Controllability: It offers enhanced control over the application flow.

- Persistence: The library provides ways to maintain state and persistence in LLM-based applications.

4. Use Cases:

LangGraph can be used for various applications, including:

- Conversational agents

- Complex task automation

- Custom LLM-backed experiences

5. Integration:

LangGraph works in conjunction with LangSmith, another tool by LangChain, to provide an out-of-the-box solution for building complex, production-ready features with LLMs.

6. Significance:

LangGraph is described as setting the foundation for building and scaling AI workloads. It's positioned as a key tool in the next chapter of LLM-based application development, particularly in the realm of agentic AI.

7. Availability:

LangGraph is open-source and available on GitHub, which suggests that developers can access and contribute to its codebase.

8. Comparison to Other Frameworks:

LangGraph is noted to offer unique benefits compared to other LLM frameworks, particularly in its ability to handle cycles, provide controllability, and maintain persistence.

LangGraph appears to be a significant tool in the evolving landscape of LLM-based application development, offering developers new ways to create more complex, stateful, and interactive AI systems.

Goodbye!

```

…

(tools) def chatbot(state: State): return {"messages": [llm_with_tools.invoke(state["messages"])]} graph_builder.add_node("chatbot", chatbot) tool_node = ToolNode(tools=[tool]) graph_builder.add_node("tools", tool_node) graph_builder.add_conditional_edges( "chatbot", tools_condition, ) # Any time a tool is called, we return to the chatbot to decide the next step graph_builder.add_edge("tools", "chatbot") graph_builder.set_entry_point("chatbot") graph = graph_builder.compile()`

…

`thread_id`, the graph loads its saved state, allowing the chatbot to pick up where it left off.

We will see later that

**checkpointing** is *much* more powerful than simple chat memory - it lets you save and resume complex state at any time for error recovery, human-in-the-loop workflows, time travel interactions, and more. But before we get too ahead of ourselves, let's add checkpointing to enable multi-turn conversations.

…

```

from typing import Annotated

from langchain.chat_models import init_chat_model

from langchain_tavily import TavilySearch

from langchain_core.messages import BaseMessage

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition

class State(TypedDict):

messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

tool = TavilySearch(max_results=2)

tools = [tool]

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):

return {"messages": [llm_with_tools.invoke(state["messages"])]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=[tool])

graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(

"chatbot",

tools_condition,



# Any time a tool is called, we return to the chatbot to decide the next step

graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge(START, "chatbot")

```

…

```

StateSnapshot(values={'messages': [HumanMessage(content='Hi there! My name is Will.', additional_kwargs={}, response_metadata={}, id='8c1ca919-c553-4ebf-95d4-b59a2d61e078'), AIMessage(content="Hello Will! It's nice to meet you. How can I assist you today? Is there anything specific you'd like to know or discuss?", additional_kwargs={}, response_metadata={'id': 'msg_01WTQebPhNwmMrmmWojJ9KXJ', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 405, 'output_tokens': 32}}, id='run-58587b77-8c82-41e6-8a90-d62c444a261d-0', usage_metadata={'input_tokens': 405, 'output_tokens': 32, 'total_tokens': 437}), HumanMessage(content='Remember my name?', additional_kwargs={}, response_metadata={}, id='daba7df6-ad75-4d6b-8057-745881cea1ca'), AIMessage(content="Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.", additional_kwargs={}, response_metadata={'id': 'msg_01E41KitY74HpENRgXx94vag', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 444, 'output_tokens': 58}}, id='run-ffeaae5c-4d2d-4ddb-bd59-5d5cbf2a5af8-0', usage_metadata={'input_tokens': 444, 'output_tokens': 58, 'total_tokens': 502})]}, next=(), config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef7d06e-93e0-6acc-8004-f2ac846575d2'}}, metadata={'source': 'loop', 'writes': {'chatbot': {'messages': [AIMessage(content="Of course, I remember your name, Will. I always try to pay attention to important details that users share with me. Is there anything else you'd like to talk about or any questions you have? I'm here to help with a wide range of topics or tasks.", additional_kwargs={}, response_metadata={'id': 'msg_01E41KitY74HpENRgXx94vag', 'model': 'claude-3-5-sonnet-20240620', 'stop_reason': 'end_turn', 'stop_sequence': None, 'usage': {'input_tokens': 444, 'output_tokens': 58}}, id='run-ffeaae5c-4d2d-4ddb-bd59-5d5cbf2a5af8-0', usage_metadata={'input_tokens': 444, 'output_tokens': 58, 'total_tokens': 502})]}}, 'step': 4, 'parents': {}}, created_at='2024-09-27T19:30:10.820758+00:00', parent_config={'configurable': {'thread_id': '1', 'checkpoint_ns': '', 'checkpoint_id': '1ef7d06e-859f-6206-8003-e1bd3c264b8f'}}, tasks=())

```

…

The snapshot above contains the current state values, corresponding config, and the

`next` node to process. In our case, the graph has reached an

`END` state, so

`next` is empty.

**Congratulations!** Your chatbot can now maintain conversation state across sessions thanks to LangGraph's checkpointing system. This opens up exciting possibilities for more natural, contextual interactions. LangGraph's checkpointing even handles **arbitrarily complex graph states**, which is much more expressive and powerful than simple chat memory.

…

```

from typing import Annotated

from langchain.chat_models import init_chat_model

from langchain_tavily import TavilySearch

from langchain_core.tools import tool

from typing_extensions import TypedDict

from langgraph.checkpoint.memory import MemorySaver

from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages

from langgraph.prebuilt import ToolNode, tools_condition

from langgraph.types import Command, interrupt

class State(TypedDict):

messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

@tool

def human_assistance(query: str) -> str:

"""Request assistance from a human."""

human_response = interrupt({"query": query})

return human_response["data"]

tool = TavilySearch(max_results=2)

tools = [tool, human_assistance]

llm = init_chat_model("anthropic:claude-3-5-sonnet-latest")

llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):

message = llm_with_tools.invoke(state["messages"])

# Because we will be interrupting during tool execution,

# we disable parallel tool calling to avoid repeating any

# tool invocations when we resume.

assert len(message.tool_calls) <= 1

return {"messages": [message]}

graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)

graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(

"chatbot",

tools_condition,



graph_builder.add_edge("tools", "chatbot")

graph_builder.add_edge(START, "chatbot")

```

…

**Congrats!** You've used an

`interrupt` to add human-in-the-loop execution to your chatbot, allowing for human oversight and intervention when needed. This opens up the potential UIs you can create with your AI systems. Since we have already added a

**checkpointer**, as long as the underlying persistence layer is running, the graph can be paused **indefinitely** and resumed at any time as if nothing had happened.

…

= interrupt({"query": query}) return human_response["data"] tool = TavilySearch(max_results=2) tools = [tool, human_assistance] llm = init_chat_model("anthropic:claude-3-5-sonnet-latest") llm_with_tools = llm.bind_tools(tools
) def chatbot(state: State): message = llm_with_tools.invoke(state["messages"]) assert(len(message.tool_calls) <= 1) return {"messages": [message]} graph_builder.add_node("chatbot", chatbot) tool_node = ToolNode(tools=tools) graph_builder.add_node("tools", tool_node) graph_builder.add_conditional_edges( "chatbot", tools_condition, ) graph_builder.add_edge("tools", "chatbot") graph_builder.add_edge(START, "chatbot") memory = MemorySaver() graph = graph_builder.compile(checkpointer=memory)`

…

Adding this information to the state makes it easily accessible by other graph nodes (e.g., a downstream node that stores or processes the information), as well as the graph's persistence layer.

Here, we will populate the state keys inside of our

`human_assistance` tool. This allows a human to review the information before it is stored in the state. We will again use

# 1. LangChain & LangGraph Cheat Sheet

- 1. LangChain & LangGraph Cheat Sheet

- 1.1 Quick Start (LCEL minimal chain)

- 1.2 Important Links

- 1.3 Getting Started

- 1.4 Core LangChain Components

- 1.5 Prompt Templates (String, Chat, Few-Shot)
- 1.6 LCEL (LangChain Expression Language)

- 1.7 Output Parsers (Pydantic, JSON, Structured)

- 1.8 Memory Systems

- 1.9 Agents & Tools

- 1.10 Agent Execution (loops, errors)

- 1.11 RAG - Retrieval Augmented Generation
- 1.12 Vector Stores (FAISS, Chroma, Pinecone, Weaviate)

- 1.13 Document Processing (Loaders, Splitters)

- 1.14 Embeddings (OpenAI, HF, Cohere, local)

- 1.15 LangGraph Basics (state)
- 1.16 LangGraph Construction (nodes/edges)

- 1.17 LangGraph Execution (invoke, stream, checkpoint)

- 1.18 Conditional Routing

- 1.19 Multi-Agent Patterns

- 1.20 Human-in-the-Loop

- 1.21 Serving & Deployment (LangServe + FastAPI)
- 1.22 Production Deployment (Docker, scaling)

- 1.23 LangSmith Monitoring

- 1.24 Caching & Optimization

- 1.25 RAG with LCEL (Modern Pattern)

- 1.26 Conversational RAG

- 1.27 Structured Output with Pydantic
- 1.28 Async Operations

- 1.29 Error Handling & Retries

- 1.30 Multi-Query Retrieval

- 1.31 Hybrid Retrieval (Dense + Sparse)

- 1.32 Contextual Compression

- 1.33 Streaming Responses

- 1.34 Function/Tool Calling
- 1.35 Batch Processing

- 1.36 Advanced Patterns (Reflection, ReAct, tools in graphs)

- 1.37 Best Practices

This cheat sheet provides a deep, end-to-end reference for LangChain and LangGraph: core components, LCEL, memory, agents, RAG, embeddings, graph construction, routing, serving/deployment, and monitoring. Each concept is shown with a concise explanation, ASCII/Unicode box-drawing diagram, practical code, and actionable tips.

## 1.1 Quick Start (LCEL minimal chain)

```

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([

("system", "You are concise."),

("user", "Question: {question}")

])

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "What is LangChain?"}))

```

…

## 1.3 Getting Started

**Brief:** Install core packages, set API keys, and verify environment.

**Diagram:**

…

```

pip install "langchain>=0.3" "langgraph>=0.2" langchain-openai langchain-community langchain-core

# Optional extras: vector stores, parsers, serving

pip install faiss-cpu chromadb pinecone-client weaviate-client pydantic openai fastapi uvicorn redis

```

…

## 1.4 Core LangChain Components

**Brief:** Models (LLMs vs Chat), Prompts, Output Parsers, Chains.

**Diagram:**

…

**Code:**

```

from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate

from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

prompt = ChatPromptTemplate.from_messages([

("system", "You are concise."),

("user", "Question: {question}")

])

chain = prompt | llm | StrOutputParser()

print(chain.invoke({"question": "What is LangChain?"}))

```

…

## 1.5 Prompt Templates (String, Chat, Few-Shot)

**Brief:** Parameterized prompts to control style and context.

**Diagram:**
```

┌─────────────┐ variables ┌─────────────────┐

│ Base Prompt │ ───────────→ │ Rendered Prompt │

└─────┬───────┘ └────────┬────────┘

│ few-shot examples │ to model

↓ ↓

┌─────────────┐ ┌───────────────┐

│ Example 1 │ │ Chat Messages │

├─────────────┤ └───────────────┘

│ Example 2 │

└─────────────┘

```

…

])

examples = [

{"text": "hello", "translation": "bonjour"},

{"text": "good night", "translation": "bonne nuit"},



example_prompt = PromptTemplate.from_template("Input: {text}\nOutput: {translation}")

few_shot = FewShotPromptTemplate(

examples=examples,

example_prompt=example_prompt,

prefix="Use examples to guide style.",

suffix="Input: {text}\nOutput:",

input_variables=["text"],



print(few_shot.format(text="thank you"))

```

…

## 1.6 LCEL (LangChain Expression Language)

**Brief:** Compose chains with

`|`, parallel branches, passthrough, streaming, async.

**Diagram (LCEL Pipe Flow):**
```

Input



├─→ ┌──────────┐ → ┌────────────┐ → ┌──────────────┐ → Output

│ │ Transform │ │ Transform │ │ Transform │

│ └──────────┘ └────────────┘ └──────────────┘



└─→ ┌───────────────┐

│ RunnableParallel│ (fan-out, then merge)

└───────────────┘

```
**Code:**

```

from langchain_core.runnables import RunnableParallel, RunnablePassthrough

from langchain_core.output_parsers import StrOutputParser

prompt = ChatPromptTemplate.from_messages([

("system", "Summarize and extract keywords."),

("user", "{text}")

])

branch = RunnableParallel(

summary=prompt | llm | StrOutputParser(),

keywords=prompt | llm | StrOutputParser(),



chain = RunnablePassthrough.assign(text=lambda x: x["text"]) | branch

result = chain.invoke({"text": "LangChain simplifies LLM orchestration."})

print(result)

```
**Tips:** - Use

`assign` to enrich inputs without losing originals. -

`astream()`/

`astream_events()` for streaming tokens/events. - Compose sync/async seamlessly; prefer async for I/O-heavy pipelines.

…

**Code:**

```

from pydantic import BaseModel, Field

from langchain.output_parsers import PydanticOutputParser

from langchain_core.prompts import ChatPromptTemplate

class Answer(BaseModel):

summary: str = Field(..., description="Brief answer")

sources: list[str]

parser = PydanticOutputParser(pydantic_object=Answer)
prompt = ChatPromptTemplate.from_messages([

("system", "Return JSON matching the schema."),

("user", "Question: {question}\n{format_instructions}")

]).partial(format_instructions=parser.get_format_instructions())

chain = prompt | llm | parser

print(chain.invoke({"question": "What is LangGraph?"}))

```

**Tips:** - Use

`OutputFixingParser` to auto-correct near-misses. - Prefer

`StructuredOutputParser`/

`PydanticOutputParser` for reliability. - Validate early before persisting to DBs.

…

```

**Code:**

```

from langchain.memory import (ConversationBufferMemory,

ConversationBufferWindowMemory, ConversationSummaryMemory,

ConversationEntityMemory)

from langchain.vectorstores import FAISS

from langchain.embeddings import OpenAIEmbeddings

buffer = ConversationBufferMemory(return_messages=True)

window = ConversationBufferWindowMemory(k=3, return_messages=True)

summary = ConversationSummaryMemory(llm=llm, return_messages=True)

entity = ConversationEntityMemory(llm=llm)

# Vector store memory

embedding = OpenAIEmbeddings()

vs = FAISS.from_texts(["Hello world"], embedding)

```

…

**Code:**

```

result = agent_executor.invoke({"input": "Plan weekend: check weather in NYC and suggest indoor/outdoor."})

# For streaming thoughts

for event in agent_executor.astream_events({"input": "..."}):

print(event)

```

**Tips:** - Set

`handle_parsing_errors=True` or custom handler for robust runs. - Cap

`max_iterations`; log intermediate steps. - Include tool observation snippets in prompts to avoid loops.

…

│ Map-Reduce │ Map chunks -> │ Scales, summaries │ More LLM calls │

│ │ partial, then │ │ │

│ │ reduce │ │ │

│ Refine │ Iterative add │ Keeps detail │ Sequential latency │

│ Map-Rerank │ Score each │ Better precision │ Costly reranking │

└────────────┴───────────────┴────────────────────┴──────────────────────┘

```

…

**Code:**

```

from langchain_openai import OpenAIEmbeddings

from langchain_community.embeddings import HuggingFaceEmbeddings, CohereEmbeddings

openai_emb = OpenAIEmbeddings(model="text-embedding-3-small")

hf_emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

cohere_emb = CohereEmbeddings(model="embed-english-light-v3.0", cohere_api_key="...")

```

…

## 1.15 LangGraph Basics (state)

**Brief:** Build graphs where nodes are steps; state carried via typed dicts/reducers.

**Diagram (StateGraph Execution):**

```

┌────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐

│ START │ → │ Node A │ → │ Node B │ → │ END │

└────────┘ └────┬─────┘ └────┬─────┘ └────────┘

│ │

└─────→──────┘ (conditional edge)

```

…

return {"message": state["message"], "steps": ["start"]}

def finish(state: GraphState):

return {"message": state["message"], "steps": state["steps"] + ["finish"]}

graph.add_node("start", start)

graph.add_node("finish", finish)

graph.add_edge("start", "finish")

graph.set_entry_point("start")

graph.set_finish_point("finish")

compiled = graph.compile()

print(compiled.invoke({"message": "hi", "steps": []}))

```

…

```

from langgraph.graph import StateGraph, END

g = StateGraph(GraphState)

g.add_node("decide", lambda s: {"route": "a" if "math" in s["message"] else "b"})

g.add_node("tool_a", lambda s: {"result": "used A"})

…

## 1.17 LangGraph Execution (invoke, stream, checkpoint)

**Brief:** Run graphs sync/async with streaming and persistence.

**Diagram:**

```

┌────────┐ invoke() ┌──────────┐ stream tokens ┌────────────┐

│ Client │────────────→│ Graph │────────────────→ │ Responses │

└────────┘ └──────────┘ └────────────┘

│ checkpoint

└────────────→ storage (Redis/S3/DB)

```

…

from langgraph.checkpoint.redis import RedisCheckpointSaver

import redis

r = redis.Redis(host="localhost", port=6379, db=0)

checkpointer = RedisCheckpointSaver(r)

compiled_ckpt = graph.compile(checkpointer=checkpointer)

run = compiled_ckpt.invoke({"message": "hi", "steps": []})

# ... later

compiled_ckpt.resume(run["checkpoint_id"])

```

**Tips:** - Use a checkpointer (e.g., Redis) for resumable flows. - Prefer streaming for chat UX; buffer for batch jobs. - Persist state for human handoffs or crash recovery.

…

**Code:**

```

def router(state):

if "finance" in state["message"]:

return "finance"

return "general"

add_conditional_edges(g, "decide", {"finance": "tool_b", "general": "tool_a"})

```

**Tips:** - Keep routing functions pure and deterministic when possible. - For LLM-based routing, constrain outputs (JSON labels) and validate. - Add default fallbacks to avoid dead ends.

…

## 1.21 Serving & Deployment (LangServe + FastAPI)

**Brief:** Expose chains/graphs as REST endpoints.

**Diagram (LangServe Deployment):**

```

Client → API Gateway → LangServe (FastAPI) → Chain/Graph → Response

```

**Code (LangServe):**

…

llm = ChatOpenAI(model="gpt-4o-mini")

embeddings = OpenAIEmbeddings()

vectorstore = FAISS.from_texts(

["LangChain simplifies LLM apps", "LCEL enables composition"],

embeddings



retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# Build RAG chain with LCEL

template = """Answer based on context:

Context: {context}

Question: {question}

Answer:"""

prompt = ChatPromptTemplate.from_template(template)

rag_chain = (

{"context": retriever, "question": RunnablePassthrough()}

| prompt
| llm
| StrOutputParser()


# Use

answer = rag_chain.invoke("What is LangChain?")

```

…

("system", "Answer using context:\n{context}"),

MessagesPlaceholder("chat_history"),

("human", "{input}"),

])

qa_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_retriever, qa_chain)

# Use with history

from langchain_core.messages import HumanMessage, AIMessage
chat_history = [

HumanMessage(content="What is LangChain?"),

AIMessage(content="LangChain is a framework for LLM apps."),



result = rag_chain.invoke({

"input": "What does it simplify?",

"chat_history": chat_history

})

```

**Tips:** - Store

`chat_history` in session/database for multi-turn conversations - Limit history to last 10 messages to control context window - Use

`ConversationBufferMemory` for automatic history management