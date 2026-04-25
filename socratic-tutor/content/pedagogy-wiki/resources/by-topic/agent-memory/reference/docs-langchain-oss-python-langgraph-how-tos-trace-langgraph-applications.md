# Source: https://docs.langchain.com/oss/python/langgraph/how-tos/trace-langgraph-applications/
# Title: Trace LangGraph applications - Docs by LangChain
# Fetched via: search
# Date: 2026-04-10

Trusted by companies shaping the future of agents— including Klarna, Uber, J.P. Morgan, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.
LangGraph is very low-level, and focused entirely on agent **orchestration**.
Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with models and tools.
We will commonly use LangChain components throughout the documentation to integrate models and tools, but you don’t need to use LangChain to use LangGraph.
...
LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.
## ​ Install
```
pip install -U langgraph
```
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
- Production-ready deployment: Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.
## ​ LangGraph ecosystem
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents.
To improve your LLM application development, pair LangGraph with:
## LangSmith Observability
Trace requests, evaluate outputs, and monitor deployments in one place.
Prototype locally with LangGraph, then move to production with integrated observability and evaluation to build more reliable agent systems.
## LangSmith Deployment
Deploy and scale agents effortlessly with a purpose-built deployment platform for long running, stateful workflows.
Discover, reuse, configure, and share agents across teams — and iterate quickly with visual prototyping in Studio.
## LangChain
Provides integrations and composable components to streamline LLM application development.
Contains agent abstractions built on top of LangGraph.
...
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.

Design agents that reliably handle complex tasks with LangGraph, an agent runtime and low-level orchestration framework.
...
Prevent agents from veering off course with easy-to-add moderation and quality controls.
Add human-in-the-loop checks to steer and approve agent actions.
Add human-in-the-loop
...
LangGraph’s low-level primitives provide the flexibility needed to create fully customizable agents.
Design diverse control flows — single, multi-agent, hierarchical — all using one framework.
See different agent architectures
...
LangGraph’s built-in memory stores conversation histories and maintains context over time, enabling rich, personalized interactions across sessions.
Learn about agent memory
#### First-class streaming for better UX design
Bridge user expectations and agent capabilities with native token-by-token streaming, showing agent reasoning and actions in real time.
See how to use streaming
...
Learn the basics of LangGraph in this LangChain Academy Course.
You'll learn about how to leverage state, memory, human-in-the-loop, and more for your agents.
Enroll for free
...
Build and ship agents fast with any model provider.
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
LangSmith, our agent engineering platform, helps developers debug every agent decision, eval changes, and deploy in one click.

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
Tools for deploying and connecting to the LangGraph Platform.
- SDK (Python): Python SDK for interacting with instances of the LangGraph Server.
- SDK (JS/TS): JavaScript/TypeScript SDK for interacting with instances of the LangGraph Server.
- RemoteGraph:
`Pregel`abstraction for connecting to LangGraph Server instances.

Trusted by companies shaping the future of agents – including Klarna, Replit, Elastic, and more – LangGraph is a low-level orchestration framework for building, managing, and deploying long-running, stateful agents.
…
Then, create an agent using prebuilt components:
*API Reference: create_react_agent*
```
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
…
## Core benefits¶
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
Debug poor-performing LLM app runs, evaluate agent trajectories, gain visibility in production, and improve performance over time.
- LangSmith Deployment — Deploy and scale agents effortlessly with a purpose-built deployment platform for long running, stateful workflows.
Discover, reuse, configure, and share agents across teams — and iterate quickly with visual prototyping in LangGraph Studio.
...
## Additional resources¶
- Guides: Quick, actionable code snippets for topics such as streaming, adding memory & persistence, and design patterns (e.g. branching, subgraphs, etc.).
- Reference: Detailed reference on core classes, methods, how to use the graph and checkpointing APIs, and higher-level prebuilt components.
- Examples: Guided examples on getting started with LangGraph.
- LangChain Forum: Connect with the community and share all of your technical questions, ideas, and feedback.
- LangChain Academy: Learn the basics of LangGraph in our free, structured course.
- Templates: Pre-built reference apps for common agentic workflows (e.g. ReAct agent, memory, retrieval etc.) that can be cloned and adapted.

Course

Imagine you're building a complex, multi-agent large language model (LLM) application. It's exciting, but it comes with challenges: managing the state of various agents, coordinating their interactions, and handling errors effectively. This is where LangGraph can help.

LangGraph is a library within the LangChain ecosystem designed to tackle these challenges head-on. LangGraph provides a framework for defining, coordinating, and executing multiple LLM agents (or chains) in a structured manner.
It simplifies the development process by enabling the creation of cyclical graphs, which are essential for developing agent runtimes. With LangGraph, we can easily build robust, scalable, and flexible multi-agent systems.

If you want to learn more about the LangChain ecosystem, I recommend this introduction to LangChain. You can also check out our LangGraph video tutorial below.

## What Is LangGraph?

LangGraph enables us to create stateful, multi-actor applications utilizing LLMs as easily as possible. It extends the capabilities of LangChain, introducing the ability to create and manage cyclical graphs, which are pivotal for developing sophisticated agent runtimes. The core concepts of LangGraph include: graph structure, state management, and coordination.

### Graph structure

Imagine your application as a directed graph. In LangGraph, each node represents an LLM agent, and the edges are the communication channels between these agents. This structure allows for clear and manageable workflows, where each agent performs specific tasks and passes information to other agents as needed.

### State management

One of LangGraph's standout features is its automatic state management. This feature enables us to track and persist information across multiple interactions. As agents perform their tasks, the state is dynamically updated, ensuring the system maintains context and responds appropriately to new inputs.

### Coordination

LangGraph ensures agents execute in the correct order and that necessary information is exchanged seamlessly. This coordination is vital for complex applications where multiple agents need to work together to achieve a common goal. By managing the flow of data and the sequence of operations, LangGraph allows developers to focus on the high-level logic of their applications rather than the intricacies of agent coordination.

…

### Simplified development

LangGraph abstracts away the complexities associated with state management and agent coordination. This means developers can define their workflows and logic without worrying about the underlying mechanisms that ensure data consistency and proper execution order. This simplification accelerates the development process and reduces the likelihood of errors. It’s a game-changer!

### Flexibility

With LangGraph, developers have the flexibility to define their own agent logic and communication protocols. This allows for highly customized applications tailored to specific use cases. Whether you need a chatbot that can handle various types of user requests or a multi-agent system that performs complex tasks, LangGraph provides the tools to build exactly what you need. It’s all about giving you the power to create.

### Scalability

LangGraph is built to support the execution of large-scale multi-agent applications. Its robust architecture can handle a high volume of interactions and complex workflows, enabling the development of scalable systems that can grow with your needs. This makes it suitable for enterprise-level applications and scenarios where performance and reliability are critical.

### Fault tolerance

Reliability is a core consideration in the design of LangGraph. The library includes mechanisms for gracefully handling errors, ensuring that your application can continue to operate even when individual agents encounter issues. This fault tolerance is essential for maintaining the stability and robustness of complex multi-agent systems. Peace of mind is just a feature away.

…

### Basic Concepts

Nodes: Nodes represent units of work within your LangGraph. They are typically Python functions that perform a specific task, such as:

- Interacting with an LLM
- Calling a tool or API
- Performing some data manipulation
- Receiving user input
- Executing business logic

In LangGraph, you can add nodes using the

…

syntax.
Edges: Edges are communication channels between nodes. They define the flow of information and the order of execution. You can add edges using the

…

syntax.
State: The state is a central object updated over time by the nodes in the graph. It manages the internal state of your application and can be overridden or added to, depending on the application's requirements. This state can hold things such as:

- Conversation history: A list of messages between the agent and the user.
- Contextual data: Information relevant to the current task or interaction.
- Internal variables: Flags, counters, or other variables to track the agent's progress and behavior.

## Building a Simple LangGraph Application

Here’s a step-by-step example of creating a basic chatbot application using LangGraph.

…

object to structure the chatbot as a state machine. The

…

is a class object defined with a single key

…

```
add_messages()
```

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

node as both the entry and finish points of the graph to indicate where to start and end the process.
```
# Set entry and finish points
graph_builder.set_entry_point("chatbot")
graph_builder.set_finish_point("chatbot")
```
Step 4: Compile and Visualize the Graph

Compile the graph to create a CompiledGraph object, and optionally, we can visualize the graph structure using the code below:

…

### Step 5: Run the chatbot

Finally, we implement a loop to continuously prompt the user for input, process it through the graph, and print the assistant's response. The loop exits when the user types

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

LangGraph allows you to create custom node types to implement complex agent logic. This provides flexibility and control over your application's behavior.
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

that encapsulates custom logic and interacts with the LLM. This provides a more structured and maintainable way to implement complex node behaviors.

### Edge types

LangGraph supports different edge types to handle various communication patterns between nodes. One useful type is the conditional edge, which allows for decision-making based on a node's output.

To create a conditional edge, you need three components:

1. The upstream node: The node's output decides the next step.
2. A function: This function evaluates the upstream node's output and determines the next node to execute, returning a string that represents the decision.
3. A mapping: This mapping links the possible outcomes of the function to the corresponding nodes to be executed.

…

Here, after the “model” node is called, we can either exit the graph (”end”) and return to the user, or we can continue (”continue”) and call a tool—depending on what the user decides!

### State management

LangGraph offers powerful state management techniques, which include using external databases like SQLite, PostgreSQL, and MongoDB, or cloud storage solutions like Amazon S3, Google Cloud Storage, and Azure Blob Storage to store and retrieve your agent's state, enabling reliability and scalability.

Here's an example of using a SQLite database for state management:
```
from langgraph.checkpoint.sqlite import SqliteSaver
# Connect to the SQLite database
memory = SqliteSaver.from_conn_string(":memory:")
# Compile the graph with the checkpointer
graph = graph_builder.compile(checkpointer=memory)
```

### Error handling

LangGraph also provides mechanisms for error handling:

- Exceptions: Node functions can raise exceptions to signal errors during execution. You can catch and handle these exceptions to prevent your graph from crashing.
- Retry mechanisms: You can implement retry logic within your nodes to handle transient errors, such as network issues or API timeouts.
- Logging: Use logging to record errors and track the execution of your graph.

…

### Autonomous agents

For applications requiring autonomous decision-making, LangGraph enables the creation of agents that can perform tasks independently based on user inputs and predefined logic.

These agents can execute complex workflows, interact with other systems, and adapt to new information dynamically. LangGraph's structured framework ensures that each agent operates efficiently and effectively, making it suitable for tasks like automated customer support, data processing, and system monitoring.

### Multi-Agent systems

LangGraph excels in building applications where multiple agents collaborate to achieve a common goal. For example, different agents can manage inventory, process orders, and coordinate deliveries in a supply chain management system. LangGraph's coordination capabilities ensure that each agent communicates effectively, sharing information and making decisions in a synchronized manner. This leads to more efficient operations and better overall system performance.

…

## Conclusion

LangGraph significantly simplifies the development of complex LLM applications by providing a structured framework for managing state and coordinating agent interactions.

Potential developments for LangGraph include integration with other LangChain components, support for new LLM models, and the introduction of more advanced agent runtimes from academia.

If you want to learn more about developing applications within the LangChain ecosystem, I recommend this course on developing LLM applications with LangChain.