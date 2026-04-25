# Source: https://github.com/langchain-ai/langgraph/discussions/2290
# Author: LangChain
# Author Slug: langchain
# Title: LangGraph discussion: human_in_the_loop (resume/edit state with checkpointing)
# Fetched via: search
# Date: 2026-04-10

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
...
Learn the basics of LangGraph in this LangChain Academy Course.
You'll learn about how to leverage state, memory, human-in-the-loop, and more for your agents.
Enroll for free
...
Build and ship agents fast with any model provider.
Use high-level abstractions or fine-grained control as needed.
...
LangGraph sets the foundation for how we can build and scale AI workloads — from conversational agents, complex task automation, to custom LLM-backed experiences that 'just work'.
...
LangGraph provides a more expressive framework to handle companies’ unique tasks without restricting users to a single black-box cognitive architecture.

*By Nuno Campos*

**Summary:** We launched LangGraph as a low level agent framework nearly two years ago, and have already seen companies like LinkedIn, Uber, and Klarna use it to build production ready agents. LangGraph builds upon feedback from the super popular LangChain framework, and rethinks how agent frameworks should work for production. We aimed to find the right abstraction for AI agents, and decided that was little to no abstraction at all. Instead, we focused on control and durability. This post shares our design principles and approach to designing LangGraph based on what we’ve learned about building reliable agents.

…

We started LangGraph as a reboot of LangChain’s super popular chains and agents more than two years ago. We decided that starting fresh would give us the most leeway to address all the feedback we had received since the launch of the original `langchain` open source library (in countless GitHub issues, discussions, Discord, Slack and Twitter posts).
The main thing we heard was that `langchain` was easy to get started but hard to customize and scale.
This time around, our top goal was to make LangGraph what you’d use to run your agents in production. When we had to make tradeoffs, we prioritized production-readiness over how easy it would be for people to get started.
In this post, we’ll share our process for scoping and designing LangGraph.
- First: we cover what’s different about building agents compared to traditional software.
- Next: we discuss how we turned these differences into required features.
- Finally: we show how we designed and tested our framework for these requirements.

The result is a low-level, production ready agent framework that scales with both the size and throughput of your agents.

## 1. What do agents need?

The first two questions we asked were, “Do we actually need to build LangGraph?” And, “Why can’t we use an existing framework to put agents in production?” To answer these questions, we had to define what makes an agent different (or similar) to previous software. By building many agents ourselves and working with teams like Uber, LinkedIn, Klarna, and Elastic, we boiled these down to 3 key differences.

…

### Managing latency

The first defining quality and challenge of LLM-based agents is **latency**. We used to measure the latency of our backend endpoints in milliseconds. Now, we need to measure agent run times in seconds, minutes, or soon hours.
This is because LLMs themselves are slow and are becoming slower with test-time compute. It’s also because we often need multiple LLM calls to achieve our desired results, with looping agents, and chaining LLM prompts to fix earlier output. And, we usually need to add non-LLM steps before and after the LLM call. For instance, you might need to get database rows into the context or create guardrails and verifiers to check the LLM call for accuracy.

…

- **Parallelization.** Whenever there were multiple steps to your agent, when the next step doesn’t need the output of the previous one, then you could run them in parallel. But to do this reliably in production you want to avoid data races between your parallel steps.
- **Streaming.** When you can’t reduce the actual latency of your agent any further without making it produce worse results, then you turn to perceived latency. Here the key unlock comes from showing useful information to the user while the agent is running, which can go all the way from a progress bar, or key actions taken by the agent, all the way to streaming LLM messages token-by-token in real-time to the end-user.

…

So we knew we had to add two more features to the list:

- **Task queue.** Queues eliminate one common source of failure by disconnecting the running of the agent from the request that triggered it. They provide the primitives to retry the agent reliably and fairly when needed.
- **Checkpointing.** This saves snapshots of the computation state at intermediate stages and makes it a lot cheaper to retry when it does fail.

…

### What developers need to build agents

This is how we built our shortlist of the six features most developers need when taking agents to production.

- Parallelization – to save actual latency
- Streaming – to save perceived latency
- Task queue – to reduce number of retries
- Checkpointing – to reduce the cost of each retry
- Human-in-the-loop - to collaborate with the user
- Tracing - to learn how users use it
If the agent you’re building doesn’t need most of these features (eg. because it’s a very short agent without tools and a single prompt), then you might not need LangGraph, or any other framework.

As we thought about building for each of these features, we also realized that developers wouldn’t adopt a framework that that provided all those features at the cost of making their LLM app perceivably slower to end users. Especially for agents deployed as chatbots. That made **low latency** our final overarching requirement.

…

**First, the runtime of the library is independent from the developer SDKs.** The SDKs are the public interfaces (classes, functions, methods, constants, etc) that developers use when building their agents. We currently offer two – **StateGraph** and the **imperative/functional API**. The runtime (which we call PregelLoop) implements each of the features listed earlier, plans the computation graph for each agent invocation, and executes it.

…

**Second, we wanted to provide each of the 6 features as building blocks, with the developer free to pick which to use in their agent at any point in time.** For instance, the ability to interrupt/resume for human-in-the-loop scenarios doesn’t get in your way until you reach for it (which is as easy as adding a call to the `interrupt()` function in one of your nodes).

…

## 4. The LangGraph runtime

With all this in mind, let’s look at how LangGraph implements each of the 6 features we wanted to have (as a reminder, these are parallelization, streaming, checkpointing, human-in-the-loop, tracing and a task queue).

…

Agents too can be written directly as a single function with one big while loop. But when you do that, you lose the ability to implement features like checkpointing or human-in-the-loop. (Note: While it may technically be possible to interrupt execution of some kinds of subroutines, like generators, that execution state can’t be saved in a portable format that can be resumed from a different machine at a different time.)

### Execution algorithm

Once you make the choice to structure agents into multiple discrete steps, you need to choose some algorithm to organize its execution. Even if it’s a naive one that feels like “no algorithm,” which is where LangGraph started before launch. The problem with using “no algorithm” is, while it may seem simpler, you’re making it up as you go along, and end up with unexpected results.
(For instance, an early version of a precursor to LangGraph suffered from non-deterministic behavior with concurrent nodes). The usual DAG algorithms (topological sort and friends) are out of the picture, given we need loops. We ended up building on top of the BSP/ Pregel algorithm, because it provides deterministic concurrency, with full support for loops (cycles).
Our execution algorithm works like this:

- **Channels** contain data (any Python/JS data type), and have a name and current version (a monotonically increasing string)
- **Nodes** are functions to run, which subscribe to one or more channels, and run whenever they change
- One or more channels are mapped to **input**, ie. the starting input to the agent is written to those channels, and therefore triggers any nodes subscribed to them
- One or more channels are mapped to **output**, ie. the return value of the agent is the value of those channels when execution halts
The execution proceeds in a loop, where each iteration

- Selects the 1 or more nodes to run, by comparing current channel versions and the last versions seen by each of their subscribers
- Executes those nodes in parallel, with independent copies of the channel values (ie. the state, so they don’t affect each other while running)
- Nodes modify their local copy of the state while running
- Once all nodes finish, the updates from each copy of the state are applied to their respective channels, in a deterministic order (this is what guarantees no data races), and the channel versions are bumped
The execution loop stops when there are no more nodes to run (ie. after comparing channels with their subscriptions we find all nodes have seen the most recent version of their subscribed channels), or when we run out of iteration steps (a constant the developer can set).

…

**Parallelization**. This algorithm is designed for safe parallelization without data races, it automatically selects parallel execution whenever the dependencies between the nodes allow, it executes parallel nodes with isolated state copies, and it applies updates from nodes in an order which doesn’t depend on which one started or finished first (as that can change between executions).
This ensures that the execution order and latency of each node never influences the final output of the agent. Given LLMs are non-deterministic, we felt this was an important property, to ensure that variability in your outputs is never the fault of the agent framework, making it a lot easier to debug issues.
- **Streaming**. Structured execution models (ie. where the computation is split into discrete steps and/or nodes) offer many more opportunities for emitting intermediate output and updates throughout. Our execution engine collects streaming output from inside nodes while they are running, as well as at the step boundaries, without requiring any custom developer code. This has enabled us to offer 6 distinct stream modes in LangGraph, values, updates, messages, tasks, checkpoints and custom. A streaming chatbot might use messages stream mode, while a longer running agent might use updates mode.
- **Checkpointing**. Again, structured execution is what makes this feasible. We want to save checkpoints that can be resumed on any machine, an arbitrary amount of time after they were saved – ie. checkpoints that don’t rely on keeping a process running in a specific machine, or keeping any live data in memory. To enable this we record serialised channel values (by default serialised to MsgPack, optionally encrypted), their version strings, and a record of which channel versions each node has most recently seen.
- **Human-in-the-loop**. The same checkpointing that enables fault tolerance can also be used to power “expected interruptions” of the agent, ie. giving the agent the ability to interrupt itself to ask the user or developer for input before continuing. Usually this capability is implemented by leaving the agent running while it waits for the input to arrive, but sadly that scales neither in time nor in volume. If you have many agents interrupted simultaneously, or if you want to wait several days (or months!) before replying, then actual interruption (powered by checkpointing to resume again from the same point) is the only way to go.
- **Tracing**. Another nice property of using structured execution is you get very clear steps to inspect the progress of your agent, while it runs and after the fact. We had previously built LangSmith as the first LLM observability platform, so naturally LangGraph integrates natively with it. Today we have also LangGraph Studio, where you can debug your agent while it’s running, and LangGraph can also emit OTEL traces for wider compatibility.
- **Task queue**. This was out of scope for a Python library such as LangGraph, so we ended up creating LangGraph Platform to answer this need.

All in all, this architecture delivers the 6 key features needed for agents. At the same time, it makes creating and debugging agents faster, thanks to the structured approach, and the tools to explore it. And finally, it does so with an excellent performance profile, which scales with the size of your agent, and the throughput you need in production –  more on this in the next section.

…

- The number of nodes (individual steps, usually functions)
- The number of edges (or the connections between nodes, which can be fixed or conditional)
- The number of channels (or the keys in your state object)
- The number of active nodes (to be executed in parallel in a given step)
- The length of invocation history (previous steps of the current invocation)
- The number of threads (independent invocations on different inputs and context)

Now, let’s list the key **moments in an invocation** of a LangGraph agent, and see how each scales with each variable:
- Starting or resuming invocation, which consists of transferring from storage the most recent checkpoint for that thread, and deserializing it
- Planning the next invocation step, where we decide which nodes to execute next, and prepare their inputs
- Running the active nodes for a step, where we execute the code for each node, producing writes to channels and edges
- Finishing an invocation step, which consists of applying updates to each channel (running channel reducers and bumping channel versions) and saving the latest checkpoint (serializing and transferring to storage)

Note there is no ‘finishing invocation’ action as execution simply stops when the planning action returns no nodes to execute next.

In summary, this is how each action scales with agent size:

…

- Scales **linearly with number of nodes**, for each node there is one hidden control channel holding the current state of its incoming edges
- **Constant on the number of edges** as the state of all edges for each destination node is collapsed into a single control channel
- Scales **linearly with number of channels**, for each channel there is a serialized representation of its current value

…

- **Constant on the number of nodes**, when finishing the previous step we store the list of updated channels, which lets us avoid iterating over all nodes when planning the next one
- **Constant on the number of edges**, as all edges are collapsed into a single trigger channel per node
- Scales **linearly with the number of channels**, when assembling the input for each node we loop over channels to check which are currently set
- Scales **linearly with number of active nodes**, for each node to execute in this step we assemble the input and configuration to use for its invocation
- **Constant on the length of history**, as we only deal with the latest checkpoint, which aggregates all previous writes
- **Constant on number of threads**, as threads are completely independent, and each invocation only touches a single one

…

- **Constant on the number of nodes**, only nodes active in a step influence the running of that step
- Scales **linearly on the number of edges** of the nodes active in this step, each active node publishes to each of its outgoing edges
- Scales **linearly on the number of channels**, for each active node we check if the node returned an update to its value (when using a dictionary return value we optimize this to be constant on the number of channels, and just iterate over the keys of the return value)
- Scales **linearly with the number of active nodes**, each active node is executed concurrently
- **Constant on the length of history**, we don’t deal with history at this time
- **Constant on number of threads**, as threads are completely independent, and each invocation only touches a single one

Lastly, finishing a step:
- Scales **linearly with number of nodes**, for each node there is one hidden control channel holding the current state of its incoming edges
- **Constant on the number of edges** as the state of all edges for each destination node is collapsed into a single control channel
- Scales **linearly with number of channels**, each channel is updated with the writes from the active nodes, and its version is bumped
- Scales **linearly with number of active nodes**, as we collect writes from each active node
- **Constant on the length of history**, as we only deal with the latest checkpoint, which aggregates all previous writes
- **Constant on number of threads**, as threads are completely independent, and each invocation only touches a single one

### Community links
- Community guidelines
- docs.langchain.com/oss/python/langgraph
## Discussions

# 1.
LangChain & LangGraph Cheat Sheet
...
- 1.37 Best Practices
This cheat sheet provides a deep, end-to-end reference for LangChain and LangGraph: core components, LCEL, memory, agents, RAG, embeddings, graph construction, routing, serving/deployment, and monitoring.
Each concept is shown with a concise explanation, ASCII/Unicode box-drawing diagram, practical code, and actionable tips.
## 1.1 Quick Start (LCEL minimal chain)
...
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
...
Client → API Gateway → LangServe (FastAPI) → Chain/Graph → Response
```
**Code (LangServe):**
...
template = """Answer based on context:
Context: {context}
...
prompt = ChatPromptTemplate.from_template(template)
...
{"context": retriever, "question": RunnablePassthrough()}
| prompt
| llm
| StrOutputParser()
# Use
answer = rag_chain.invoke("What is LangChain?")
...
# Use with history
from langchain_core.messages import HumanMessage, AIMessage
chat_history = [
HumanMessage(content="What is LangChain?"),
AIMessage(content="LangChain is a framework for LLM apps."),
result = rag_chain.invoke({
"input": "What does it simplify?",
"chat_history": chat_history
})
...
**Tips:** - Store

# LangGraph

## Tutorials

[Learn the basics](https://langchain-ai.github.io/langgraph/tutorials/introduction/): LLM should read this page when needing to build a LangGraph chatbot or when learning about chat agents with memory, human-in-the-loop functionality, and state management. This page provides a comprehensive LangGraph quickstart tutorial covering building a support chatbot with web search capability, conversation memory, human review routing, custom state management, and time travel functionality to explore alternative conversation paths.

…

[Workflows and Agents](https://langchain-ai.github.io/langgraph/tutorials/workflows/): LLM should read this page when implementing agent systems, designing workflow architectures, or troubleshooting LLM orchestration strategies. The page covers patterns for LLM system design, comparing workflows (predefined paths) vs agents (dynamic control), with implementations of prompt chaining, parallelization, routing, orchestrator-worker, evaluator-optimizer, and agent patterns using both graph and functional APIs in LangGraph.

## Concepts 

[Concepts](https://langchain-ai.github.io/langgraph/concepts/): LLM should read this page when needing to understand LangGraph's key concepts or when planning to deploy LangGraph applications. Comprehensive guide covering LangGraph fundamentals (graph primitives, agents, multi-agent systems, breakpoints, persistence), features (time travel, memory, streaming), and LangGraph Platform deployment options (self-hosted, cloud, enterprise).
[Agent architectures](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/): LLM should read this page when designing agent architectures, implementing control flows for LLM applications, or customizing agent behavior patterns. This page covers different LLM agent architectures including routers, tool calling agents (ReAct), structured outputs, memory systems, planning capabilities, and advanced customization options like human-in-the-loop, parallelization, subgraphs, and reflection mechanisms.
[Application Structure](https://langchain-ai.github.io/langgraph/concepts/application_structure/): LLM should read this page when needing to understand LangGraph application structure, preparing to deploy a LangGraph application, or troubleshooting configuration issues. This page details the structure of LangGraph applications, including required components (graphs, langgraph.json config file, dependency files, optional .env), file organization patterns for Python/JavaScript projects, configuration file format with all supported fields, and how to specify dependencies, graphs, and environment variables.
[Assistants](https://langchain-ai.github.io/langgraph/concepts/assistants/): LLM should read this page when looking for information about LangGraph assistants, understanding assistant configuration in LangGraph Platform, or learning about versioning agent configurations. This page explains LangGraph assistants, which allow developers to modify agent configurations (prompts, models, etc.) without changing graph logic, supports versioning for tracking changes, and is available only in LangGraph Platform (not open source).
[Authentication & Access Control](https://langchain-ai.github.io/langgraph/concepts/auth/): LLM should read this page when implementing authentication in LangGraph Platform, designing access control for LangGraph applications, or troubleshooting security issues in LangGraph deployments. This page explains LangGraph's authentication and authorization system, covering the difference between authentication and authorization, system architecture, implementing custom auth handlers, common access patterns, and supported resources/actions for access control.

…

[Double Texting](https://langchain-ai.github.io/langgraph/concepts/double_texting/): LLM should read this page when handling concurrent user interactions in LangGraph Platform, implementing double-texting safeguards, or designing stateful conversation systems. This page explains four approaches to handling "double texting" in LangGraph (when users send a second message before the first completes): Reject, Enqueue, Interrupt, and Rollback, noting these features are currently only available in LangGraph Platform.
[Durable Execution](https://langchain-ai.github.io/langgraph/concepts/durable_execution/): LLM should read this page when needing to understand durable execution in LangGraph, implementing workflow persistence, or troubleshooting workflow resumption. This page explains durable execution in LangGraph: how workflows save progress to resume later, requirements (checkpointers and thread IDs), determinism guidelines for consistent replay, using tasks to encapsulate non-deterministic operations, and approaches for pausing/resuming workflows.

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

[Time Travel ⏱️](https://langchain-ai.github.io/langgraph/concepts/time-travel/): LLM should read this page when debugging LLM-based agent behavior, analyzing decision-making paths, or exploring alternative execution branches in LangGraph. This page explains LangGraph's Time Travel debugging features: Replaying (reproducing past actions up to specific checkpoints) and Forking (creating alternative execution paths from specific points), with code examples for retrieving checkpoints, configuring replay, and creating forked states.

## How Tos

[How-to Guides](https://langchain-ai.github.io/langgraph/how-tos/): LLM should read this page when looking for specific implementation techniques in LangGraph or when trying to deploy LangGraph applications to production environments. This page contains an extensive collection of how-to guides for LangGraph, covering graph fundamentals, persistence, memory management, human-in-the-loop features, tool calling, multi-agent systems, streaming, and deployment options through LangGraph Platform.

…

[How to integrate LangGraph with AutoGen, CrewAI, and other frameworks](https://langchain-ai.github.io/langgraph/how-tos/autogen-integration/): LLM should read this page when integrating LangGraph with other agent frameworks, building multi-agent systems, or adding persistence features to agents. The page demonstrates how to combine LangGraph with AutoGen by calling AutoGen agents inside LangGraph nodes, showing code examples for setting up the integration with memory and conversation persistence.
[How to integrate LangGraph (functional API) with AutoGen, CrewAI, and other frameworks](https://langchain-ai.github.io/langgraph/how-tos/autogen-integration-functional/): LLM should read this page when integrating LangGraph with other agent frameworks, building multi-agent systems with different frameworks, or adding LangGraph features to existing agent systems. This page demonstrates how to integrate LangGraph's functional API with AutoGen, including code examples for creating a workflow that calls AutoGen agents, leveraging LangGraph's memory and persistence features.
[How to create branches for parallel node execution](https://langchain-ai.github.io/langgraph/how-tos/branching/): LLM should read this page when needing to implement parallel node execution in LangGraph, optimizing graph performance, or handling conditional branching in workflows. This page explains how to create branches for parallel execution in LangGraph using fan-out/fan-in mechanisms, reducer functions for state accumulation, handling exceptions during parallel execution, and implementing conditional branching logic between nodes.

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