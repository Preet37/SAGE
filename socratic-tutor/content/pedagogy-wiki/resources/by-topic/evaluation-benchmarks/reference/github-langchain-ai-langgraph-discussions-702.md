# Source: https://github.com/langchain-ai/langgraph/discussions/702
# Author: LangChain
# Author Slug: langchain
# Title: langgraph/how-tos/configuration/ #702 - GitHub (How to stream events / configuration)
# Fetched via: search
# Date: 2026-04-10

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
- Production-ready deployment: Deploy sophisticated agent systems confidently with scalable infrastructure designed to handle the unique challenges of stateful, long-running workflows.
## ​ LangGraph ecosystem
While LangGraph can be used standalone, it also integrates seamlessly with any LangChain product, giving developers a full suite of tools for building agents.
To improve your LLM application development, pair LangGraph with:
## LangSmith Observability
Trace requests, evaluate outputs, and monitor deployments in one place.
Prototype locally with LangGraph, then move to production with integrated observability and evaluation to build more reliable agent systems.
...
Contains agent abstractions built on top of LangGraph.
## ​ Acknowledgements
LangGraph is inspired by Pregel and Apache Beam.
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.
Edit this page on GitHub or file an issue.

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
LangGraph is inspired by Pregel and Apache Beam.
The public interface draws inspiration from NetworkX.
LangGraph is built by LangChain Inc, the creators of LangChain, but can be used without LangChain.

# LangGraph

## Tutorials

[Learn the basics](https://langchain-ai.github.io/langgraph/tutorials/introduction/): LLM should read this page when needing to build a LangGraph chatbot or when learning about chat agents with memory, human-in-the-loop functionality, and state management. This page provides a comprehensive LangGraph quickstart tutorial covering building a support chatbot with web search capability, conversation memory, human review routing, custom state management, and time travel functionality to explore alternative conversation paths.
[Local Deploy](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/): LLM should read this page when setting up a LangGraph app locally using `langgraph dev` and troubleshooting LangGraph server deployment. This page contains a quickstart guide for launching a LangGraph server locally, including installation steps, app creation from templates, environment setup, API testing with Python/JS SDKs, and links to deployment options and further documentation.
[Workflows and Agents](https://langchain-ai.github.io/langgraph/tutorials/workflows/): LLM should read this page when implementing agent systems, designing workflow architectures, or troubleshooting LLM orchestration strategies. The page covers patterns for LLM system design, comparing workflows (predefined paths) vs agents (dynamic control), with implementations of prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer, and agent patterns using both graph and functional APIs in LangGraph.

## Concepts 

[Concepts](https://langchain-ai.github.io/langgraph/concepts/): LLM should read this page when needing to understand LangGraph's key concepts or when planning to deploy LangGraph applications. Comprehensive guide covering LangGraph fundamentals (graph primitives, agents, multi-agent systems, breakpoints, persistence), features (time travel, memory, streaming), and LangGraph Platform deployment options (self-hosted, cloud, enterprise).
[Agent architectures](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/): LLM should read this page when designing agent architectures, implementing control flows for LLM applications, or customizing agent behavior patterns. This page covers different LLM agent architectures including routers, tool calling agents (ReAct), structured outputs, memory systems, planning capabilities, and advanced customization options like human-in-the-loop, parallelization, subgraphs, and reflection mechanisms.
[Application Structure](https://langchain-ai.github.io/langgraph/concepts/application_structure/): LLM should read this page when needing to understand LangGraph application structure, preparing to deploy a LangGraph application, or troubleshooting configuration issues. This page details the structure of LangGraph applications, including required components (graphs, langgraph.json config file, dependency files, optional .env), file organization patterns for Python/JavaScript projects, configuration file format with all supported fields, and how to specify dependencies, graphs, and environment variables.
[Assistants](https://langchain-ai.github.io/langgraph/concepts/assistants/): LLM should read this page when looking for information about LangGraph assistants, understanding assistant configuration in LangGraph Platform, or learning about versioning agent configurations. This page explains LangGraph assistants, which allow developers to modify agent configurations (prompts, models, etc.) without changing graph logic, supports versioning for tracking changes, and is available only in LangGraph Platform (not open source).
[Authentication & Access Control](https://langchain-ai.github.io/langgraph/concepts/auth/): LLM should read this page when implementing authentication in LangGraph Platform, designing access control for LangGraph applications, or troubleshooting security issues in LangGraph deployments. This page explains LangGraph's authentication and authorization system, covering the difference between authentication and authorization, system architecture, implementing custom auth handlers, common access patterns, and supported resources/actions for access control.

…

[Double Texting](https://langchain-ai.github.io/langgraph/concepts/double_texting/): LLM should read this page when handling concurrent user interactions in LangGraph Platform, implementing double-texting safeguards, or designing stateful conversation systems. This page explains four approaches to handling "double texting" in LangGraph (when users send a second message before the first completes): Reject, Enqueue, Interrupt, and Rollback, noting these features are currently only available in LangGraph Platform.

…

[Functional API](https://langchain-ai.github.io/langgraph/concepts/functional_api/): LLM should read this page when implementing workflows with persistent state, adding human-in-the-loop features, or converting existing code to use LangGraph. The page documents LangGraph's Functional API, which allows adding persistence, memory, and human-in-the-loop capabilities with minimal code changes using @entrypoint and @task decorators, handling serialization requirements, state management, and common patterns for parallel execution and error handling.
[Why LangGraph?](https://langchain-ai.github.io/langgraph/concepts/high_level/): LLM should read this page when understanding LangGraph's core capabilities, exploring LLM application infrastructure, or evaluating agent/workflow persistence options. LangGraph provides infrastructure for LLM applications with three key benefits: persistence for memory and human-in-the-loop capabilities, streaming of workflow events and LLM outputs, and tools for debugging and deployment via LangGraph Platform.
[Human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/): LLM should read this page when implementing human-in-the-loop workflows in LangGraph, designing approval systems with LLMs, or creating interactive multi-turn conversation agents. This page explains human-in-the-loop patterns in LangGraph using the interrupt function, showing how to pause graph execution for human review/input and resume with Command. Includes design patterns for approval workflows, state editing, tool call reviews, and multi-turn conversations, with code examples and warnings about execution flow and common pitfalls.

…

[LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/): LLM should read this page when seeking information about LangGraph Platform's components or evaluating production deployment options for agentic applications. The page details the LangGraph Platform, a commercial solution for deploying agentic applications, including its components (Server, Studio, CLI, SDK, Remote Graph) and key benefits like streaming support, background runs, long run handling, burstiness management, and human-in-the-loop capabilities.
[LangGraph Server](https://langchain-ai.github.io/langgraph/concepts/langgraph_server/): LLM should read this page when developing applications with LangGraph Server, deploying agent-based applications, or integrating persistent state management in agent workflows. LangGraph Server provides an API for creating and managing agent applications with key features like streaming endpoints, background runs, task queues, persistence, webhooks, cron jobs, and monitoring capabilities through a structured system of assistants, threads, runs, and stores.

…

[LangGraph Glossary](https://langchain-ai.github.io/langgraph/concepts/low_level/): LLM should read this page when needing to understand LangGraph terminology, implementing agent workflows as graphs, or developing modular multi-step AI systems. The page covers core LangGraph concepts including StateGraph, nodes, edges, state management, messaging, persistence, configuration, human-in-the-loop features, subgraphs, and visualization capabilities.
[Memory](https://langchain-ai.github.io/langgraph/concepts/memory/): LLM should read this page when implementing memory systems for AI agents, managing conversation context across sessions, or designing systems that require both short-term and long-term information retention. This page explains memory systems in LangGraph, covering short-term (thread-scoped) memory for managing conversation history and long-term memory across threads, with techniques for handling long conversations, summarizing past interactions, and organizing persistent memories in namespaces.

…

[Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/): LLM should read this page when needing to understand LangGraph persistence mechanisms, implementing stateful workflows, or managing conversation history across interactions. This page covers LangGraph's persistence features including checkpointers, threads, state snapshots, replay functionality, forking state, cross-thread memory via InMemoryStore, and semantic search capabilities for stored memories.

…

[LangGraph Platform Architecture](https://langchain-ai.github.io/langgraph/concepts/platform_architecture/): LLM should read this page when needing to understand LangGraph Platform's technical architecture or troubleshooting deployment issues. The page details how LangGraph Platform uses Postgres for persistent storage of user/run data and Redis for worker communication (run cancellation, output streaming) and ephemeral metadata storage (retry attempts).
[LangGraph's Runtime (Pregel)](https://langchain-ai.github.io/langgraph/concepts/pregel/): LLM should read this page when learning about LangGraph's runtime, implementing applications with Pregel directly, or understanding how LangGraph executes graph applications. Explains LangGraph's Pregel runtime which manages graph application execution through a three-phase process (Plan, Execution, Update), describes different channel types (LastValue, Topic, Context, BinaryOperatorAggregate), provides direct implementation examples, and contrasts the StateGraph API with the Functional API.

…

[Streaming](https://langchain-ai.github.io/langgraph/concepts/streaming/): LLM should read this page when implementing streaming features in LangGraph applications, understanding different streaming modes, or building responsive LLM applications. This page explains streaming in LangGraph, covering the main types (workflow progress, LLM tokens, custom updates) and streaming modes (values, updates, custom, messages, debug, events), with details on how to use multiple modes simultaneously and differences between LangGraph library and Platform implementations.

…

## How Tos

[How-to Guides](https://langchain-ai.github.io/langgraph/how-tos/): LLM should read this page when looking for specific implementation techniques in LangGraph or when trying to deploy LangGraph applications to production environments. This page contains an extensive collection of how-to guides for LangGraph, covering graph fundamentals, persistence, memory management, human-in-the-loop features, tool calling, multi-agent systems, streaming, and deployment options through LangGraph Platform.

…

[How to integrate LangGraph with AutoGen, CrewAI, and other frameworks](https://langchain-ai.github.io/langgraph/how-tos/autogen-integration/): LLM should read this page when integrating LangGraph with other agent frameworks, building multi-agent systems, or adding persistence features to agents. The page demonstrates how to combine LangGraph with AutoGen by calling AutoGen agents inside LangGraph nodes, showing code examples for setting up the integration with memory and conversation persistence.
[How to integrate LangGraph (functional API) with AutoGen, CrewAI, and other frameworks](https://langchain-ai.github.io/langgraph/how-tos/autogen-integration-functional/): LLM should read this page when integrating LangGraph with other agent frameworks, building multi-agent systems with different frameworks, or adding LangGraph features to existing agent systems. This page demonstrates how to integrate LangGraph's functional API with AutoGen, including code examples for creating a workflow that calls AutoGen agents, leveraging LangGraph's memory and persistence features.
[How to create branches for parallel node execution](https://langchain-ai.github.io/langgraph/how-tos/branching/): LLM should read this page when needing to implement parallel node execution in LangGraph, optimizing graph performance, or handling conditional branching in workflows. This page explains how to create branches for parallel execution in LangGraph using fan-out/fan-in mechanisms, reducer functions for state accumulation, handling exceptions during parallel execution, and implementing conditional branching logic between nodes.
[How to combine control flow and state updates with Command](https://langchain-ai.github.io/langgraph/how-tos/command): LLM should read this page when learning how to combine control flow with state updates in LangGraph, understanding Command objects, or navigating between parent graphs and subgraphs. This page explains how to use Command objects to simultaneously update state and control flow between nodes, demonstrates using Command.PARENT to navigate from subgraphs to parent graphs, and includes examples of implementing reducers for state updates across graph hierarchies.
[How to add runtime configuration to your graph](https://langchain-ai.github.io/langgraph/how-tos/configuration/): LLM should read this page when implementing runtime configuration for LangGraph, adding model selection options to agents, or enabling dynamic system messages. This page demonstrates how to configure LangGraph at runtime, including selecting different LLMs dynamically and adding custom configuration options like system messages through the configurable dictionary.

…

[How to edit graph state](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/edit-graph-state/): LLM should read this page when needing to implement human intervention in LangGraph workflows, wanting to edit graph state during execution, or implementing breakpoints in agent systems. This page explains how to edit graph state in LangGraph using breakpoints, including implementing human-in-the-loop interactions, setting up interruptions before specific nodes, and updating state during agent execution.
[How to Review Tool Calls](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/review-tool-calls/): LLM should read this page when implementing human review of tool calls, creating interactive agent workflows, or building approval systems for AI actions. This page explains how to implement human-in-the-loop review for tool calls in LangGraph, including approving tool calls, modifying tool calls manually, and providing natural language feedback to agents with complete code examples and explanations.

…

[How to define input/output schema for your graph](https://langchain-ai.github.io/langgraph/how-tos/input_output_schema/): LLM should read this page when needing to define separate input/output schemas for LangGraph, implementing schema-based data filtering, or understanding schema definitions in StateGraph. This page explains how to define distinct input and output schemas for a StateGraph, showing how input schema validates the provided data structure while output schema filters internal data to return only relevant information, with code examples demonstrating implementation.
[How to handle large numbers of tools](https://langchain-ai.github.io/langgraph/how-tos/many-tools/): LLM should read this page when handling large tool collections, implementing dynamic tool selection, or creating retrieval-based tool management in LangGraph. This page demonstrates how to manage large numbers of tools by using vector search to dynamically select relevant tools based on user queries, implementing tool selection nodes in LangGraph, and handling tool selection errors with retry mechanisms.

…

[How to add summary of the conversation history](https://langchain-ai.github.io/langgraph/how-tos/memory/add-summary-conversation-history/): LLM should read this page when implementing conversation summarization, managing context windows, or building chatbots with memory management. This page demonstrates how to add summary functionality to conversation history using LangGraph, including checking conversation length, creating summaries, and removing old messages while maintaining context.

…

[How to add multi-turn conversation in a multi-agent application](https://langchain-ai.github.io/langgraph/how-tos/multi-agent-multi-turn-convo/): LLM should read this page when implementing multi-turn conversations between agents, creating interactive agent systems with human input, or learning about langgraph interrupts and agent handoffs. This page demonstrates how to build a multi-agent system with multi-turn conversations, including human-in-the-loop interactions, agent handoffs, and state management using LangGraph, Command objects, and interrupts.
[How to add multi-turn conversation in a multi-agent application (functional API)](https://langchain-ai.github.io/langgraph/how-tos/multi-agent-multi-turn-convo-functional/): LLM should read this page when building multi-turn conversational agents, implementing agent-to-agent handoffs, or using interrupts to collect user input in LangGraph. This guide demonstrates how to create a multi-agent system with multi-turn conversations using LangGraph's functional API, featuring agent handoffs, interrupt mechanics for user input, and a complete example of travel and hotel advisor agents that can transfer control between each other.

…

[How to pass private state between nodes](https://langchain-ai.github.io/langgraph/how-tos/pass_private_state/): LLM should read this page when implementing data sharing between specific nodes in LangGraph, handling private state in graph workflows, or designing multi-node sequential processes with selective data visibility. This page demonstrates how to pass private data between specific nodes in a LangGraph without making it part of the main schema, using typed dictionaries to define both public and private states, and showing a three-node example where private data flows only between the first two nodes.
[How to add thread-level persistence to your graph](https://langchain-ai.github.io/langgraph/how-tos/persistence/): LLM should read this page when implementing persistence in LangGraph, needing to preserve context across user interactions, or learning about thread-level state management. This page explains how to add thread-level persistence to LangGraph applications using MemorySaver, including code examples for creating stateful conversations where context is maintained across multiple interactions.

…

[How to create and control loops](https://langchain-ai.github.io/langgraph/how-tos/recursion-limit/): LLM should read this page when building loops in computational graphs, needing to implement termination conditions, or handling recursion limits in LangGraph. The page explains how to create graphs with loops using conditional edges for termination, set recursion limits, handle GraphRecursionError, and implement complex loops with branches.

…

[How to create a sequence of steps](https://langchain-ai.github.io/langgraph/how-tos/sequence/): LLM should read this page when implementing sequential workflows in LangGraph, creating multi-step processes in applications, or learning about state management in graph-based systems. This page explains how to create sequences in LangGraph, covering methods for building sequential graphs using .add_node/.add_edge or the shorthand .add_sequence, defining state with TypedDict, creating nodes as functions that update state, and compiling/invoking graphs with examples.

…

[How to use subgraphs](https://langchain-ai.github.io/langgraph/how-tos/subgraph/): LLM should read this page when building complex systems with subgraphs, implementing multi-agent systems, or needing to share state between parent graphs and subgraphs. The page explains two methods for using subgraphs: adding compiled subgraphs when schemas share keys, and invoking subgraphs via node functions when schemas differ, with code examples for both approaches.

…

[How to transform inputs and outputs of a subgraph](https://langchain-ai.github.io/langgraph/how-tos/subgraph-transform-state/): LLM should read this page when needing to work with nested subgraphs, transforming state between parent and child graphs, or integrating independent state components in LangGraph. This page demonstrates how to transform inputs and outputs between parent graphs and subgraphs with different state structures, showing implementation of three nested graphs (parent, child, grandchild) with separate state dictionaries and transformation functions.
[How to view and update state in subgraphs](https://langchain-ai.github.io/langgraph/how-tos/subgraphs-manage-state/): LLM should read this page when working with state management in nested subgraphs, implementing human-in-the-loop patterns, or debugging complex graph flows. This guide covers viewing and updating state in LangGraph subgraphs, including how to resume execution from breakpoints, modify subgraph state, act as specific nodes, and work with multi-level nested subgraphs.

…

[Overview human-in-the-loop] (https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/): LangGraph supports robust human-in-the-loop (HIL) workflows, enabling human intervention at any point in an automated process.
[Add human-in-the-loop] (https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/): The interrupt function in LangGraph enables human-in-the-loop workflows by pausing the graph at a specific node, presenting information to a human, and resuming the graph with their input. It's useful for tasks like approvals, edits, or gathering additional context.

# Understanding Common Python Syntax Used in LangGraph

* Author: [JeongHo Shin](https://github.com/ThePurpleCollar)
* Peer Review:
* Proofread : [Chaeyoon Kim](https://github.com/chaeyoonyunakim)
* This is a part of [LangChain Open Tutorial](https://github.com/LangChain-OpenTutorial/LangChain-OpenTutorial)
[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/LangChain-OpenTutorial/LangChain-OpenTutorial/blob/main/17-LangGraph/01-Core-Features/01-LangGraph-Introduction.ipynb)[![
Open in GitHub](https://img.shields.io/badge/Open%20in%20GitHub-181717?style=flat-square\&logo=github\&logoColor=white)](https://github.com/LangChain-OpenTutorial/LangChain-OpenTutorial/blob/main/17-LangGraph/01-Core-Features/01-LangGraph-Introduction.ipynb)

## Overview

LangGraph is a powerful framework that allows you to design complex workflows for language models using a graph-based structure. It enhances the modularity, scalability, and efficiency in building AI-driven applications.

This tutorial explains key Python concepts frequently used in LangGraph, including `TypedDict` , `Annotated` , and the `add_messages` function. We will also compare these concepts with standard Python features to highlight their advantages and typical use cases.

### Table of Contents

* [Overview](#overview)
* [Environment Setup](#environment-setup)
* [Typedict](#typeddict)
* [Annotated](#annotated)
* [add\_messages](#add_messages)

### References

* [LangGraph](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
***

## Environment Setup

Setting up your environment is the first step. See the [Environment Setup](https://wikidocs.net/257836) guide for more details.

**\[Note]**

The langchain-opentutorial is a package of easy-to-use environment setup guidance, useful functions and utilities for tutorials.\
Check out the [`langchain-opentutorial`](https://github.com/LangChain-OpenTutorial/langchain-opentutorial-pypi) for more details.
```python
%%capture --no-stderr
%pip install langchain-opentutorial
```

```python
# Install required packages
from langchain_opentutorial import package

package.install(
    [
        "langsmith",
        "langchain",
        "langchain_core",
        "langchain-anthropic",
        "langchain_community",
        "langchain_text_splitters",
        "langchain_openai",
    ],
    verbose=False,
    upgrade=False,
)
```
You can set API keys in a `.env` file or set them manually.

\[Note] If you’re not using the `.env` file, no worries! Just enter the keys directly in the cell below, and you’re good to go.

```python
from dotenv import load_dotenv
from langchain_opentutorial import set_env

# Attempt to load environment variables from a .env file; if unsuccessful, set them manually.
if not load_dotenv():
    set_env(
        {
            "OPENAI_API_KEY": "",
            "LANGCHAIN_API_KEY": "",
            "LANGCHAIN_TRACING_V2": "true",
            "LANGCHAIN_ENDPOINT": "https://api.smith.langchain.com",
            "LANGCHAIN_PROJECT": "",  # set the project name same as the title
        }
    )
```
```
Environment variables have been set successfully.
```

## TypedDict

`TypedDict`, a feature within Python's `typing` module, empowers developers to define dictionaries possessing a fixed structure and explicit key-value types. This enforces type safety and improves code readability.

### Key Differences between `dict` and `TypedDict`
1. **Type Checking**

* `dict` : Does not provide type checking during runtime and development.
* `TypedDict`: Supports static type checking using tools like `mypy` or IDEs with type checking functionality enabled.

1. **Key and Value Specification**

* `dict` : Specifies generic key-value types (e.g., `Dict[str, str]` ).
* `TypedDict` : Explicitly defines the exact keys and their respective types.
1. **Flexibility**

* `dict` : Allows runtime addition or removal of keys without restriction.
* `TypedDict` : Enforces a predefined structure, prohibiting extra keys unless specifically designated.

### Benefits of using `TypedDict`

* **Type Safety** : Raises errors during development.
* **Readability** : Provides a clear schema for dictionaries.
* **IDE Support** : Enhances autocompletion and documentation.
* **Documentation** : Serves as self-documenting code.

### Example

`TypedDict` ensures type safety by enforcing fixed keys and types, unlike standard dictionaries that allow flexible key-value modifications.

```python
from typing import Dict, TypedDict

# Standard Python dictionary usage
sample_dict: Dict[str, str] = {
    "name": "Teddy",
    "age": "30",  # Stored as a string (allowed in dict)
    "job": "Developer",
}

# Using TypedDict
class Person(TypedDict):
    name: str
    age: int  # Defined as an integer
    job: str

typed_dict: Person = {"name": "Shirley", "age": 25, "job": "Designer"}

# Behavior with a standard dictionary
sample_dict["age"] = 35  # Type inconsistency is allowed
sample_dict["new_field"] = "Additional Info"  # Adding new keys is allowed

# Behavior with TypedDict
typed_dict["age"] = 35  # Correct usage
typed_dict["age"] = "35"  # Error: Type mismatch detected by type checker
typed_dict["new_field"] = "Additional Info"  # Error: Key not defined in TypedDict
```

The advantages of `TypedDict` are highlights when utilized in pair with static type checkers like `mypy`, and become apparent on IDEs such as PyCharm or VS Code, of which type-checking is enabled. These tools detect type inconsistencies and undefined keys during development, providing invaluable feedback to prevent runtime errors.

## Annotated

`Annotated`, also residing in Python's `typing` module, allows the addition of metadata to type hints. This feature supports functionality with additional context, improving code clarity and usability for both developers and development tools alike. For example, metadata can serve as supplementary documentation for readers or convey actionable information to tools.

### Benefits of using `Annotated`

* **Additional Context** : Adds metadata to enrich type hints, improving clarity for both developers and tools.
* **Enhanced Documentation** : Serves as self-contained documentation that can clarify the purpose and constraints of variables.
* **Validation** : Integrates with libraries like Pydantic to enforce data validation based on annotated metadata.
* **Framework-Specific Behavior** : Enables advanced features in frameworks like LangGraph by defining specialized operations.

### Syntax

* Type: Defines the variable's data type (e.g., `int`, `str`, `List[str]`, etc.).
* Metadata: Adds descriptive information about the variable (e.g., `"unit: cm"`, `"range: 0-100"`).

### Usage Example

`Annotated` enriches type hints with metadata, improving code clarity and intent.
```python
from typing import Annotated

# Basic usage of Annotated with metadata for descriptive purposes
name: Annotated[str, "User's name"]
age: Annotated[int, "User's age (0-150)"]
```

### Example with `Pydantic`

When used with `Pydantic`, `Annotated` ensures strict validation by enforcing constraints like type, range, and length. Invalid inputs trigger detailed error messages identifying the issue.

…

class Employee(BaseModel):
    id: Annotated[int, Field(..., description="Employee ID")]
    name: Annotated[str, Field(..., min_length=3, max_length=50, description="Name")]
    age: Annotated[int, Field(gt=18, lt=65, description="Age (19-64)")]
salary: Annotated[float, Field(gt=0, lt=10000, description="Salary (in units of 10,000, up to 10 billion)")]
    skills: Annotated[List[str], Field(min_items=1, max_items=10, description="Skills (1-10 items)")]

# Example of valid data
try:
    valid_employee = Employee(
        id=1, name="Teddynote", age=30, salary=1000, skills=["Python", "LangChain"]
    )
    print("Valid employee data:", valid_employee)
except ValidationError as e:
    print("Validation error:", e)

# Example of invalid data
try:
    invalid_employee = Employee(
        id=1,
        name="Ted",  # Name is too short
        age=17,  # Age is out of range
        salary=20000,  # Salary exceeds the maximum
        skills="Python",  # Skills is not a list
    )
except ValidationError as e:
    print("Validation errors:")
    for error in e.errors():
        print(f"- {error['loc'][0]}: {error['msg']}")
```

…

## add\_messages

The `add_messages` reducer function, referenced by the `messages` key, directs LangGraph to append new messages to an existing list.

In scenarios where state keys lack annotations, each update overwrites the previous value, retaining only the most recent data.

The `add_messages` function merges two inputs (`left` and `right` ) into a consolidated message list.

### Key Features

* **Message Lists Merging** : Combines two separate message lists into a signle unified list.
* **Append-Only State Maintenance** : Ensures new messages are added while preserving existing messages.
* **Messages with Matching IDs** : If an incoming message in `right` shares an ID with an existing message in `left`, it replaces the existing message. All remaining messages from `right` are appended to `left`.

### Parameters:

* `left` (Messages): The initial message list.
* `right` (Messages): A list of new messages to merge or a single message to add.

### Outputs:

* `Messages` : Returns a new message list with replacements as described above, merging `right` into `left`.

### Example

`add_messages` merges message lists by appending new messages when IDs differ and replacing existing ones if IDs match.

```python
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph.message import add_messages

# Example 1: Merging two message lists
# `msgs1` and `msgs2` are combined into a single list without overlapping IDs.
msgs1 = [HumanMessage(content="Hello?", id="1")]
msgs2 = [AIMessage(content="Nice to meet you!", id="2")]

result1 = add_messages(msgs1, msgs2)
print(result1)

# Example 2: Replacing messages with the same ID
# If `msgs2` contains a message with the same ID as one in `msgs1`,
# the message in `msgs2` replaces the corresponding message in `msgs1`.
msgs1 = [HumanMessage(content="Hello?", id="1")]
msgs2 = [HumanMessage(content="Nice to meet you!", id="1")]
result2 = add_messages(msgs1, msgs2)
print(result2)
```

```
[HumanMessage(content='Hello?', additional_kwargs={}, response_metadata={}, id='1'), AIMessage(content='Nice to meet you!', additional_kwargs={}, response_metadata={}, id='2')]
    [HumanMessage(content='Nice to meet you!', additional_kwargs={}, response_metadata={}, id='1')]
```