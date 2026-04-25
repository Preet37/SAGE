# Source: https://github.com/langchain-ai/langgraph/discussions/2028
# Author: LangChain
# Author Slug: langchain
# Title: Websocket implementation · langchain-ai/langgraph · Discussion #2028
# Fetched via: search
# Date: 2026-04-10

langgraph
...
Design agents that reliably handle complex tasks with LangGraph, an agent runtime and low-level orchestration framework.
### How does LangGraph help?
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
...
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
Other agentic frameworks can work for simple, generic tasks but fall short for complex tasks bespoke to a company’s needs.
LangGraph provides a more expressive framework to handle companies’ unique tasks without restricting users to a single black-box cognitive architecture.
Does LangGraph impact the performance of my app?
LangGraph will not add any overhead to your code and is specifically designed with streaming workflows in mind.
Is LangGraph open source?
Is it free?
Yes.
LangGraph is an MIT-licensed open-source library and is free to use.
### See what your agent is really doing

Trusted by companies shaping the future of agents— including Klarna, Uber, J.P. Morgan, and more— LangGraph is a low-level orchestration framework and runtime for building, managing, and deploying long-running, stateful agents.
LangGraph is very low-level, and focused entirely on agent **orchestration**.
Before using LangGraph, we recommend you familiarize yourself with some of the components used to build agents, starting with models and tools.
We will commonly use LangChain components throughout the documentation to integrate models and tools, but you don’t need to use LangChain to use LangGraph.
If you are just getting started with agents or want a higher-level abstraction, we recommend you use LangChain’s agents that provide prebuilt architectures for common LLM and tool-calling loops.
LangGraph is focused on the underlying capabilities important for agent orchestration: durable execution, streaming, human-in-the-loop, and more.
…
Then, create a simple hello world example:
```
import { StateSchema, MessagesValue, GraphNode, StateGraph, START, END } from "@langchain/langgraph";
const State = new StateSchema({
messages: MessagesValue,
});
const mockLlm: GraphNode<typeof State> = (state) => {
return { messages: [{ role: "ai", content: "hello world" }] };
};
const graph = new StateGraph(State)
.addNode("mock_llm", mockLlm)
.addEdge(START, "mock_llm")
.addEdge("mock_llm", END)
.compile();
await graph.invoke({ messages: [{ role: "user", content: "hi!" }] });
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
Contains agent abstractions built on top of LangGraph.
## ​ Acknowledgements
LangGraph is inspired by Pregel and Apache Beam.
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.
Edit this page on GitHub or file an issue.

- ### Discussions are moving to the LangChain Forum!
...
- Community guidelines
- docs.langchain.com/oss/python/langgraph
## Discussions

# Guides
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/index/): This page provides an overview of the LangGraph project, including its logo and essential scripts for functionality within MkDocs. It also includes a reference to the README.md file for detailed information about the project. The content is designed to be user-friendly and visually appealing.
- [LangGraph Quickstart Guide](https://langchain-ai.github.io/langgraph/agents/agents/): This quickstart guide provides step-by-step instructions for setting up and using LangGraph's prebuilt components to create agentic systems. It covers prerequisites, installation, agent creation, configuration of language models, and advanced features like memory and structured output. Ideal for developers looking to leverage LangGraph for building intelligent agents.
- [Getting Started with LangGraph: Building AI Agents](https://langchain-ai.github.io/langgraph/concepts/why-langgraph/): This page provides an overview of LangGraph, a platform designed for developers to create adaptable AI agents. It highlights key features such as reliability, extensibility, and streaming support, and offers a series of tutorials to help users build a support chatbot with various capabilities. By following the tutorials, developers will learn to implement essential functionalities like conversation state management and human-in-the-loop controls.
- [Building a Basic Chatbot with LangGraph](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/): This tutorial guides you through the process of creating a basic chatbot using LangGraph. It covers prerequisites, installation of necessary packages, and step-by-step instructions to set up a state machine for the chatbot. By the end of the tutorial, you will have a functional chatbot that can engage in simple conversations.

…

- [Implementing Memory in Chatbots with LangGraph](https://langchain-ai.github.io/langgraph/tutorials/get-started/3-add-memory/): This page provides a comprehensive guide on how to add memory functionality to chatbots using LangGraph's persistent checkpointing feature. It details the steps to create a `MemorySaver` checkpointer, compile the graph, and interact with the chatbot to maintain context across multiple interactions. Additionally, it explains how to inspect the state of the chatbot and highlights the advantages of checkpointing over simple memory solutions.
- [Implementing Human-in-the-Loop Controls in LangGraph](https://langchain-ai.github.io/langgraph/tutorials/get-started/4-human-in-the-loop/): This page provides a comprehensive guide on adding human-in-the-loop controls to LangGraph workflows, enabling agents to pause execution for human input. It details the use of the `interrupt` function to facilitate user feedback and outlines the steps to integrate a `human_assistance` tool into a chatbot. Additionally, the tutorial covers graph compilation, visualization, and resuming execution with human input.
- [Customizing State in LangGraph for Enhanced Chatbot Functionality](https://langchain-ai.github.io/langgraph/tutorials/get-started/5-customize-state/): This tutorial guides you through the process of adding custom fields to the state in LangGraph, enabling complex behaviors in your chatbot without relying solely on message lists. You will learn how to implement human-in-the-loop controls to verify information before it is stored in the state. By the end of this tutorial, you will have a deeper understanding of state management and how to enhance your chatbot's capabilities.
- [Implementing Time Travel in LangGraph Chatbots](https://langchain-ai.github.io/langgraph/tutorials/get-started/6-time-travel/): This page provides a comprehensive guide on utilizing the time travel functionality in LangGraph to enhance chatbot interactions. It covers how to rewind, add steps, and replay the state history of a chatbot, allowing users to explore different outcomes and fix mistakes. Additionally, it includes code snippets and practical examples to help developers implement these features effectively.

…

- [Agent Development with LangGraph](https://langchain-ai.github.io/langgraph/agents/overview/): This page provides an overview of agent development using LangGraph, highlighting its prebuilt components and capabilities for building agent-based applications. It explains the structure of an agent, key features such as memory integration and human-in-the-loop control, and outlines the package ecosystem available for developers. With LangGraph, users can focus on application logic while leveraging robust infrastructure for state management and feedback.
- [Guide to Running Agents in LangGraph](https://langchain-ai.github.io/langgraph/agents/run_agents/): This page provides a comprehensive overview of how to execute agents in LangGraph, detailing both synchronous and asynchronous methods. It covers input and output formats, streaming capabilities, and how to manage execution limits to prevent infinite loops. Additionally, it includes code examples and links to further resources for deeper understanding.
- [Streaming Data in LangGraph](https://langchain-ai.github.io/langgraph/agents/streaming/): This page provides an overview of streaming data types in LangGraph, including agent progress, LLM tokens, and custom updates. It includes code examples for both synchronous and asynchronous streaming methods. Additionally, it covers how to stream multiple modes and disable streaming when necessary.

…

- [Using Tools in LangChain](https://langchain-ai.github.io/langgraph/agents/tools/): This page provides an overview of how to define, customize, and manage tools within the LangChain framework. It covers creating simple tools, handling tool errors, and utilizing prebuilt integrations for enhanced functionality. Additionally, it discusses advanced features such as memory management and controlling tool behavior during agent execution.
- [Integrating MCP with LangGraph Agents](https://langchain-ai.github.io/langgraph/agents/mcp/): This page provides a comprehensive guide on how to integrate the Model Context Protocol (MCP) with LangGraph agents using the `langchain-mcp-adapters` library. It includes installation instructions, example code for using MCP tools, and guidance on creating custom MCP servers. Additional resources for further reading on MCP are also provided.
- [Understanding Context in LangGraph Agents](https://langchain-ai.github.io/langgraph/agents/context/): This page provides an overview of how to supply context to agents in LangGraph, detailing the three primary types: Config, State, and Long-Term Memory. It explains how to use these context types to enhance agent behavior, customize prompts, and access context in tools. Additionally, it includes code examples for implementing context in various scenarios.
- [Understanding Memory in LangGraph for Conversational Agents](https://langchain-ai.github.io/langgraph/agents/memory/): This documentation page provides an overview of the two types of memory supported by LangGraph: short-term and long-term memory. It explains how to implement these memory types in conversational agents, including code examples and best practices for managing message history. Additionally, it covers the use of persistent storage and tools for enhancing memory functionality.
- [Implementing Human-in-the-Loop in LangGraph](https://langchain-ai.github.io/langgraph/agents/human-in-the-loop/): This documentation page provides a comprehensive guide on how to implement Human-in-the-Loop (HIL) features in LangGraph, allowing for human review and approval of tool calls in agents. It covers the use of the `interrupt()` function to pause execution for human input, along with practical examples and code snippets. Additionally, it explains how to create a wrapper to add HIL capabilities to any tool seamlessly.
- [Building Multi-Agent Systems](https://langchain-ai.github.io/langgraph/agents/multi-agent/): This page provides an overview of multi-agent systems, detailing how to create and manage them using supervisor and swarm architectures. It includes practical examples of implementing a flight and hotel booking assistant using the LangGraph libraries. Additionally, the page explains the concept of handoffs between agents, allowing for seamless communication and task delegation.

…

- [Agent Chat UI Documentation](https://langchain-ai.github.io/langgraph/agents/ui/): This page provides comprehensive guidance on using the Agent Chat UI for interacting with LangGraph agents. It covers setup instructions, features like human-in-the-loop workflows, and the integration of generative UI components. Users can find links to relevant resources and tips for customizing their chat experience.
- [Overview of Agent Architectures in LLM Applications](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/): This page provides a comprehensive overview of various agent architectures used in large language model (LLM) applications, highlighting their control flows and functionalities. It discusses key concepts such as routers, tool-calling agents, memory management, and planning, along with customization options for specific tasks. Additionally, it covers advanced features like human-in-the-loop, parallelization, subgraphs, and reflection mechanisms to enhance agent performance.
- [Understanding Workflows and Agents in LangGraph](https://langchain-ai.github.io/langgraph/tutorials/workflows/): This documentation page provides an in-depth overview of workflows and agents within LangGraph, highlighting their differences and use cases. It covers various patterns for building agentic systems, including setup instructions, building blocks, and advanced concepts like prompt chaining, parallelization, and routing. Additionally, it offers practical examples and code snippets to help users implement these workflows effectively.
- [Understanding LangGraph: Core Concepts and Components](https://langchain-ai.github.io/langgraph/concepts/low_level/): This documentation page provides an in-depth overview of the core concepts of LangGraph, focusing on how agent workflows are modeled as graphs. It covers essential components such as States, Nodes, and Edges, and explains how they interact to create complex workflows. Additionally, it discusses graph compilation, message handling, and configuration options to enhance the functionality of your graphs.
- [LangGraph Runtime Overview](https://langchain-ai.github.io/langgraph/concepts/pregel/): This page provides a comprehensive overview of the LangGraph runtime, specifically focusing on the Pregel execution model. It details the structure and functionality of actors and channels within the Pregel framework, along with examples of how to implement applications. Additionally, it introduces high-level APIs for creating Pregel applications using StateGraph and Functional API.
- [Using the LangGraph API: A Comprehensive Guide](https://langchain-ai.github.io/langgraph/how-tos/graph-api/): This documentation provides a detailed overview of how to utilize the LangGraph Graph API, covering essential concepts such as state management, node creation, and control flow. It includes practical examples for building sequences, branches, and loops, as well as advanced features like retry policies and async execution. Additionally, the guide offers insights into visualizing graphs and integrating with external tools.
- [LangGraph Streaming System](https://langchain-ai.github.io/langgraph/concepts/streaming/): This page provides an overview of the streaming capabilities of LangGraph, enabling real-time updates for enhanced user experiences. It details the types of data that can be streamed, including workflow progress, LLM tokens, and custom updates. Additionally, it outlines various functionalities and modes available for streaming within the LangGraph framework.
- [Streaming Outputs in LangGraph](https://langchain-ai.github.io/langgraph/how-tos/streaming/): This documentation page provides an overview of how to utilize the streaming capabilities of LangGraph, including synchronous and asynchronous streaming methods. It covers various stream modes, such as updates, values, and custom data, along with examples of how to implement them in your graphs. Additionally, it discusses the integration of Large Language Models (LLMs) and how to handle streaming outputs effectively.
- [LangGraph Persistence and Checkpointing](https://langchain-ai.github.io/langgraph/concepts/persistence/): This page provides an in-depth overview of the persistence layer in LangGraph, focusing on the use of checkpointers to save graph states at each super-step. It covers key concepts such as threads, checkpoints, state retrieval, and memory management, along with practical examples and code snippets. Additionally, it discusses advanced features like time travel, fault tolerance, and the integration of memory stores for cross-thread information retention.
- [Understanding Durable Execution in LangGraph](https://langchain-ai.github.io/langgraph/concepts/durable_execution/): This page provides an overview of durable execution, a technique that allows workflows to save their progress and resume from key points. It details the requirements for implementing durable execution in LangGraph, including the use of persistence and tasks to ensure deterministic and consistent replay. Additionally, it covers how to handle pausing, resuming, and recovering workflows effectively.
- [Implementing Memory in LangGraph for AI Applications](https://langchain-ai.github.io/langgraph/how-tos/persistence/): This documentation page provides a comprehensive guide on adding persistence to AI applications using LangGraph. It covers both short-term and long-term memory implementations, including code examples for managing conversation context and user-specific data. Additionally, it discusses the use of various storage backends and semantic search capabilities for enhanced memory management.
- [Understanding Memory in AI Agents](https://langchain-ai.github.io/langgraph/concepts/memory/): This documentation page provides an in-depth overview of memory types in AI agents, focusing on short-term and long-term memory. It explains how these memory types can be implemented and managed within applications using LangGraph, including techniques for handling conversation history and storing memories. Additionally, it discusses the importance of memory in enhancing user interactions and the various strategies for writing and updating memories.
- [Memory Management in LangGraph for AI Applications](https://langchain-ai.github.io/langgraph/how-tos/memory/): This page provides an overview of memory management in LangGraph, focusing on short-term and long-term memory functionalities essential for conversational agents. It includes detailed instructions on how to implement memory strategies such as trimming, summarizing, and deleting messages to optimize conversation tracking without exceeding context limits. Code examples are provided to illustrate the implementation of these memory management techniques.
- [Human-in-the-Loop Workflows in LangGraph](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/): This page provides an overview of the human-in-the-loop (HIL) capabilities within LangGraph, highlighting how human intervention can enhance automated processes. It details key features such as persistent execution state and flexible integration points, along with typical use cases for validating outputs and providing context. Additionally, it outlines the implementation of HIL through specific functions and primitives.
- [Implementing Human-in-the-Loop Workflows with Interrupts](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/): This documentation page provides a comprehensive guide on using the `interrupt` function in LangGraph to facilitate human-in-the-loop workflows. It covers the implementation details, design patterns, and best practices for pausing graph execution to gather human input, as well as how to resume execution with that input. Additionally, it highlights common pitfalls and offers extended examples to illustrate various use cases.
- [Understanding Breakpoints in LangGraph](https://langchain-ai.github.io/langgraph/concepts/breakpoints/): This page provides an overview of breakpoints in LangGraph, which allow users to pause graph execution at specific points for inspection. It explains how breakpoints utilize the persistence layer to save the graph state and how execution can be resumed after inspection. An illustrative example is included to demonstrate the concept visually.
- [Using Breakpoints in Graph Execution](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/breakpoints/): This page provides a comprehensive guide on how to implement breakpoints in graph execution for debugging purposes. It covers the requirements for setting breakpoints, the difference between static and dynamic breakpoints, and includes code examples for both compile-time and run-time configurations. Additionally, it explains how to manage breakpoints in subgraphs.

…

- [Using Time-Travel in LangGraph](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/time-travel/): This page provides a comprehensive guide on how to implement time-travel functionality in LangGraph. It outlines the steps to run a graph, identify checkpoints, modify graph states, and resume execution from specific checkpoints. Additionally, an example workflow is included to illustrate the process of generating and modifying jokes using LangGraph.

…

- [Understanding Subgraphs in LangGraph](https://langchain-ai.github.io/langgraph/concepts/subgraphs/): This page provides an overview of subgraphs in LangGraph, explaining their role as encapsulated nodes within larger graphs. It discusses the benefits of using subgraphs, such as facilitating multi-agent systems and enabling independent team work. Additionally, it outlines the communication methods between parent graphs and subgraphs, detailing scenarios involving shared and different state schemas.
- [Using Subgraphs in LangGraph](https://langchain-ai.github.io/langgraph/how-tos/subgraph/): This guide provides an overview of how to effectively use subgraphs within LangGraph, including communication methods between parent graphs and subgraphs. It covers shared and different state schemas, setup instructions, and examples for implementing subgraphs in multi-agent systems. Additionally, it discusses persistence, state management, and streaming outputs from subgraphs.

…

- [Building Multi-Agent Systems with LangGraph](https://langchain-ai.github.io/langgraph/how-tos/multi_agent/): This guide provides an overview of how to build multi-agent systems using LangGraph, focusing on the implementation of handoffs for agent communication. It covers the creation of independent agents, the use of handoffs to transfer control and data between agents, and examples of prebuilt multi-agent architectures. Additionally, it includes code snippets and best practices for managing agent interactions and state.
- [Understanding the Functional API in LangGraph](https://langchain-ai.github.io/langgraph/concepts/functional_api/): This documentation page provides an overview of the Functional API in LangGraph, detailing its key features such as persistence, memory, and human-in-the-loop capabilities. It explains how to define workflows using the `@entrypoint` and `@task` decorators, along with examples and best practices for implementing workflows with state management and streaming. Additionally, it compares the Functional API with the Graph API, highlighting their differences and use cases.
- [Functional API Documentation](https://langchain-ai.github.io/langgraph/how-tos/use-functional-api/): This page provides comprehensive guidance on using the Functional API, including creating workflows, handling parallel execution, and integrating with other APIs. It covers various features such as retry policies, caching, and human-in-the-loop workflows, along with practical examples. Additionally, it discusses memory management strategies for both short-term and long-term use cases.
- [Overview of LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/): The LangGraph Platform is designed for developing, deploying, and managing long-running agent workflows with ease. This page outlines the platform's features, including streaming support, background runs, and memory management, which enhance the performance and reliability of agent applications. Additionally, it provides links to resources for getting started and deploying agents effectively.

…

- [Overview of LangGraph Platform Components](https://langchain-ai.github.io/langgraph/concepts/langgraph_components/): This page provides a comprehensive overview of the various components that make up the LangGraph Platform. It details the functionalities of each component, including the LangGraph Server, CLI, Studio, SDKs, and the control and data planes. Users can learn how these components work together to facilitate the development, deployment, and management of LangGraph applications.
- [LangGraph Server Documentation](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/): This page provides an overview of the LangGraph Server, an API designed for creating and managing agent-based applications. It details the server versions, application structure, deployment components, and the use of assistants, persistence, and task queues. Additionally, it includes links to further resources and guides for effective deployment and usage.

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
```

from typing import Annotated

from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END

from langgraph.graph.message import add_messages

class State(TypedDict):

# Messages have the type "list". The `add_messages` function

# in the annotation defines how this state key should be updated

# (in this case, it appends messages to the list, rather than overwriting them)

messages: Annotated[list, add_messages]

graph_builder = StateGraph(State)

```
Our graph can now handle two key tasks:

- Each

`node`can receive the current

`State`as input and output an update to the state.

- Updates to

`messages`will be appended to the existing list rather than overwriting it, thanks to the prebuilt

`add_messages`function used with the
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

**Congratulations!**You've built your first chatbot using LangGraph. This bot can engage in basic conversation by taking user input and generating responses using an LLM. You can inspect a LangSmith Trace for the call above at the provided link.

However, you may have noticed that the bot's knowledge is limited to what's in its training data. In the next part, we'll add a web search tool to expand the bot's knowledge and make it more capable.

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
The results are page summaries our chat bot can use to answer questions.

Next, we'll start defining our graph. The following is all

**the same as in Part 1**, except we have added

`bind_tools` on our LLM. This lets the LLM know the correct JSON format to use if it wants to use our search engine.

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

## Part 3: Adding Memory to the Chatbot¶

Our chatbot can now use tools to answer user questions, but it doesn't remember the context of previous interactions. This limits its ability to have coherent, multi-turn conversations.

LangGraph solves this problem through

**persistent checkpointing**. If you provide a

`checkpointer` when compiling the graph and a

`thread_id` when calling your graph, LangGraph automatically saves the state after each step. When you invoke the graph again using the same
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

## Part 5: Customizing State¶

So far, we've relied on a simple state with one entry-- a list of messages. You can go far with this simple state, but if you want to define complex behavior without relying on the message list, you can add additional fields to the state. Here we will demonstrate a new scenario, in which the chatbot is using its search tool to find specific information, and forwarding them to a human for review. Let's have the chatbot research the birthday of an entity. We will add

…

Adding this information to the state makes it easily accessible by other graph nodes (e.g., a downstream node that stores or processes the information), as well as the graph's persistence layer.

Here, we will populate the state keys inside of our

`human_assistance` tool. This allows a human to review the information before it is stored in the state. We will again use