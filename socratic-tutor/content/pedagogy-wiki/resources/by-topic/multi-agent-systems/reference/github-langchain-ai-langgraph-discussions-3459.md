# Source: https://github.com/langchain-ai/langgraph/discussions/3459
# Author: LangChain
# Author Slug: langchain
# Title: Reducers for other state members apart from messages #3459
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
…
## LangChain
Provides integrations and composable components to streamline LLM application development.
Contains agent abstractions built on top of LangGraph.

Design agents that reliably handle complex tasks with LangGraph, an agent runtime and low-level orchestration framework.
### How does LangGraph help?
...
Prevent agents from veering off course with easy-to-add moderation and quality controls.
Add human-in-the-loop checks to steer and approve agent actions.
...
LangGraph’s low-level primitives provide the flexibility needed to create fully customizable agents.
Design diverse control flows — single, multi-agent, hierarchical — all using one framework.
See different agent architectures
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

…

[How to create branches for parallel node execution](https://langchain-ai.github.io/langgraph/how-tos/branching/): LLM should read this page when needing to implement parallel node execution in LangGraph, optimizing graph performance, or handling conditional branching in workflows. This page explains how to create branches for parallel execution in LangGraph using fan-out/fan-in mechanisms, reducer functions for state accumulation, handling exceptions during parallel execution, and implementing conditional branching logic between nodes.

…

[How to edit graph state](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/edit-graph-state/): LLM should read this page when needing to implement human intervention in LangGraph workflows, wanting to edit graph state during execution, or implementing breakpoints in agent systems. This page explains how to edit graph state in LangGraph using breakpoints, including implementing human-in-the-loop interactions, setting up interruptions before specific nodes, and updating state during agent execution.
[How to Review Tool Calls](https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/review-tool-calls/): LLM should read this page when implementing human review of tool calls, creating interactive agent workflows, or building approval systems for AI actions. This page explains how to implement human-in-the-loop review for tool calls in LangGraph, including approving tool calls, modifying tool calls manually, and providing natural language feedback to agents with complete code examples and explanations.

…

[How to define input/output schema for your graph](https://langchain-ai.github.io/langgraph/how-tos/input_output_schema/): LLM should read this page when needing to define separate input/output schemas for LangGraph, implementing schema-based data filtering, or understanding schema definitions in StateGraph. This page explains how to define distinct input and output schemas for a StateGraph, showing how input schema validates the provided data structure while output schema filters internal data to return only relevant information, with code examples demonstrating implementation.

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

…

[Overview human-in-the-loop] (https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/): LangGraph supports robust human-in-the-loop (HIL) workflows, enabling human intervention at any point in an automated process.
[Add human-in-the-loop] (https://langchain-ai.github.io/langgraph/how-tos/human_in_the_loop/add-human-in-the-loop/): The interrupt function in LangGraph enables human-in-the-loop workflows by pausing the graph at a specific node, presenting information to a human, and resuming the graph with their input. It's useful for tasks like approvals, edits, or gathering additional context.

# 1.
LangChain & LangGraph Cheat Sheet
- 1.
...
- 1.37 Best Practices
This cheat sheet provides a deep, end-to-end reference for LangChain and LangGraph: core components, LCEL, memory, agents, RAG, embeddings, graph construction, routing, serving/deployment, and monitoring.
Each concept is shown with a concise explanation, ASCII/Unicode box-drawing diagram, practical code, and actionable tips.
## 1.1 Quick Start (LCEL minimal chain)
```
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
...
Client → API Gateway → LangServe (FastAPI) → Chain/Graph → Response
...
**Code (LangServe):**
...
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
...
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
...
**Tips:** - Store

# LangGraph Glossary¶
## Graphs¶

At its core, LangGraph models agent workflows as graphs. You define the behavior of your agents using three key components:



`State`: A shared data structure that represents the current snapshot of your application. It is represented by an

`Annotation`object.



`Nodes`: JavaScript/TypeScript functions that encode the logic of your agents. They receive the current
`State`as input, perform some computation or side-effect, and return an updated

`State`.



`Edges`: JavaScript/TypeScript functions that determine which

`Node`to execute next based on the current

`State`. They can be conditional branches or fixed transitions.

By composing

`Nodes` and
`Edges`, you can create complex, looping workflows that evolve the

`State` over time. The real power, though, comes from how LangGraph manages that

`State`. To emphasize:

`Nodes` and

`Edges` are nothing more than JavaScript/TypeScript functions - they can contain an LLM or just good ol' JavaScript/TypeScript code.
In short:

*nodes do the work. edges tell what to do next*.

LangGraph's underlying graph algorithm uses message passing to define a general program. When a Node completes its operation, it sends messages along one or more edges to other node(s). These recipient nodes then execute their functions, pass the resulting messages to the next set of nodes, and the process continues. Inspired by Google's Pregel system, the program proceeds in discrete "super-steps."
A super-step can be considered a single iteration over the graph nodes. Nodes that run in parallel are part of the same super-step, while nodes that run sequentially belong to separate super-steps. At the start of graph execution, all nodes begin in an

`inactive` state. A node becomes

`active` when it receives a new message (state) on any of its incoming edges (or "channels"). The active node then runs its function and responds with updates. At the end of each super-step, nodes with no incoming messages vote to
`halt` by marking themselves as

`inactive`. The graph execution terminates when all nodes are

`inactive` and no messages are in transit.

### StateGraph¶

The

`StateGraph` class is the main graph class to use. This is parameterized by a user defined

`State` object. (defined using the

`Annotation` object and passed as the first argument)

…

### Compiling your graph¶

To build your graph, you first define the state, you then add nodes and edges, and then you compile it. What exactly is compiling your graph and why is it needed?

Compiling is a pretty simple step. It provides a few basic checks on the structure of your graph (no orphaned nodes, etc). It is also where you can specify runtime args like checkpointers and breakpoints. You compile your graph by just calling the

…

## State¶

The first thing you do when you define a graph is define the

`State` of the graph. The

`State` includes information on the structure of the graph, as well as

`reducer` functions which specify how to apply updates to the state. The schema of the

`State` will be the input schema to all

`Nodes` and

`Edges` in the graph, and should be defined using an

`Annotation` object. All

`Nodes` will emit updates to the

`State` which are then applied using the specified

`reducer` function.

…

#### Multiple schemas¶

Typically, all graph nodes communicate with a single state annotation. This means that they will read and write to the same state channels. But, there are cases where we want more control over this:

- Internal nodes can pass information that is not required in the graph's input / output.

- We may also want to use different input / output schemas for the graph. The output might, for example, only contain a single relevant output key.

…

*all* keys relevant to graph operations. But, we also define

`input` and

`output` schemas that are sub-sets of the "internal" schema to constrain the input and output of the graph. See this guide for more detail.

Let's look at an example:
```
import {

Annotation,

START,

StateGraph,

StateType,

UpdateType,

} from "@langchain/langgraph";

const InputStateAnnotation = Annotation.Root({

user_input: Annotation<string>,

});

const OutputStateAnnotation = Annotation.Root({

graph_output: Annotation<string>,

});

const OverallStateAnnotation = Annotation.Root({

foo: Annotation<string>,
bar: Annotation<string>,

user_input: Annotation<string>,

graph_output: Annotation<string>,

});

const node1 = async (state: typeof InputStateAnnotation.State) => {

// Write to OverallStateAnnotation

return { foo: state.user_input + " name" };

};

const node2 = async (state: typeof OverallStateAnnotation.State) => {
// Read from OverallStateAnnotation, write to OverallStateAnnotation

return { bar: state.foo + " is" };

};

const node3 = async (state: typeof OverallStateAnnotation.State) => {

// Read from OverallStateAnnotation, write to OutputStateAnnotation

return { graph_output: state.bar + " Lance" };

…

UpdateType<(typeof OutputStateAnnotation)["spec"]>,

typeof START,

(typeof InputStateAnnotation)["spec"],

(typeof OutputStateAnnotation)["spec"]

>({

input: InputStateAnnotation,

output: OutputStateAnnotation,

stateSchema: OverallStateAnnotation,

})

.addNode("node1", node1)

.addNode("node2", node2)

.addNode("node3", node3)

.addEdge("__start__", "node1")

.addEdge("node1", "node2")

.addEdge("node2", "node3")

.compile();

await graph.invoke({ user_input: "My" });

```

…

*can write to any state channel in the graph state.* The graph state is the union of of the state channels defined at initialization, which includes

`OverallStateAnnotation` and the filters

`InputStateAnnotation` and

`OutputStateAnnotation`.

### Reducers¶

Reducers are key to understanding how updates from nodes are applied to the

`State`. Each key in the

`State` has its own independent reducer function. If no reducer function is explicitly specified then it is assumed that all updates to that key should override it. Let's take a look at a few examples to understand them better.
**Example A:**

```

import { StateGraph, Annotation } from "@langchain/langgraph";

const State = Annotation.Root({

foo: Annotation<number>,

bar: Annotation<string[]>,

});

const graphBuilder = new StateGraph(State);

```

In this example, no reducer functions are specified for any key. Let's assume the input to the graph is
`{ foo: 1, bar: ["hi"] }`. Let's then assume the first

`Node` returns

`{ foo: 2 }`. This is treated as an update to the state. Notice that the

`Node` does not need to return the whole

`State` schema - just an update. After applying this update, the
`State` would then be

`{ foo: 2, bar: ["hi"] }`. If the second node returns

`{ bar: ["bye"] }` then the

`State` would then be

`{ foo: 2, bar: ["bye"] }`

**Example B:**
```

import { StateGraph, Annotation } from "@langchain/langgraph";

const State = Annotation.Root({

foo: Annotation<number>,

bar: Annotation<string[]>({

reducer: (state: string[], update: string[]) => state.concat(update),

default: () => [],

}),

});

const graphBuilder = new StateGraph(State);

```

…

`Node`. Note that the first key remains unchanged. Let's assume the input to the graph is

`{ foo: 1, bar: ["hi"] }`. Let's then assume the first

`Node` returns

`{ foo: 2 }`. This is treated as an update to the state. Notice that the

…

`State` would then be

`{ foo: 2, bar: ["hi", "bye"] }`. Notice here that the

`bar` key is updated by concatenating the two arrays together.

### Working with Messages in Graph State¶

#### Why use messages?¶

Most modern LLM providers have a chat model interface that accepts a list of messages as input. LangChain's

`ChatModel` in particular accepts a list of

`Message` objects as inputs. These messages come in a variety of forms such as

`HumanMessage` (user input) or

`AIMessage` (LLM response). To read more about what message objects are, please refer to this conceptual guide.

#### Using Messages in your Graph¶

In many cases, it is helpful to store prior conversation history as a list of messages in your graph state. To do so, we can add a key (channel) to the graph state that stores a list of

`Message` objects and annotate it with a reducer function (see
`messages` key in the example below). The reducer function is vital to telling the graph how to update the list of

`Message` objects in the state with each state update (for example, when a node sends an update). If you don't specify a reducer, every state update will overwrite the list of messages with the most recently provided value.
However, you might also want to manually update messages in your graph state (e.g. human-in-the-loop). If you were to use something like

`(a, b) => a.concat(b)` as a reducer, the manual state updates you send to the graph would be appended to the existing list of messages, instead of updating existing messages. To avoid that, you need a reducer that can keep track of message IDs and overwrite existing messages, if updated. To achieve this, you can use the prebuilt

…

#### Serialization¶

In addition to keeping track of message IDs, the

`messagesStateReducer` function will also try to deserialize messages into LangChain

`Message` objects whenever a state update is received on the

`messages` channel. This allows sending graph inputs / state updates in the following format:

```

// this is supported



messages: [new HumanMessage({ content: "message" })];



// and this is also supported



messages: [{ role: "user", content: "message" }];



```

…

#### MessagesAnnotation¶

Since having a list of messages in your state is so common, there exists a prebuilt annotation called

`MessagesAnnotation` which makes it easy to use messages as graph state.

`MessagesAnnotation` is defined with a single

`messages` key which is a list of

`BaseMessage` objects and uses the

…

The state of a

`MessagesAnnotation` has a single key called

`messages`. This is an array of

`BaseMessage`s, with

`messagesStateReducer` as a reducer.

`messagesStateReducer` basically adds messages to the existing list (it also does some nice extra things, like convert from OpenAI message format to the standard LangChain message format, handle updates based on message IDs, etc).
We often see an array of messages being a key component of state, so this prebuilt state is intended to make it easy to use messages. Typically, there is more state to track than just messages, so we see people extend this state and add more fields, like:

```

import { Annotation, MessagesAnnotation } from "@langchain/langgraph";

const StateWithDocuments = Annotation.Root({

...MessagesAnnotation.spec, // Spread in the messages state

documents: Annotation<string[]>,

});

```

…

```

import type { BaseMessage } from "@langchain/core/messages";

import { MessagesZodMeta, StateGraph } from "@langchain/langgraph";

import { registry } from "@langchain/langgraph/zod";

import { z } from "zod/v4";

const MessagesZodState = z.object({

messages: z.custom<BaseMessage[]>().register(registry, MessagesZodMeta),

});

const graph = new StateGraph(MessagesZodState)

.addNode(...)

...

```

…

Behind the scenes, functions are converted to RunnableLambda's, which adds batch and streaming support to your function, along with native tracing and debugging.

`START` Node¶

The

`START` Node is a special node that represents the node sends user input to the graph. The main purpose for referencing this node is to determine which nodes should be called first.

…

## Edges¶

Edges define how the logic is routed and how the graph decides to stop. This is a big part of how your agents work and how different nodes communicate with each other. There are a few key types of edges:

- Normal Edges: Go directly from one node to the next.

- Conditional Edges: Call a function to determine which node(s) to go to next.

- Entry Point: Which node to call first when user input arrives.

- Conditional Entry Point: Call a function to determine which node(s) to call first when user input arrives.

…

`Node` should be different (one for each generated object).

To support this design pattern, LangGraph supports returning

`Send` objects from conditional edges.

`Send` takes two arguments: first is the name of the node, and second is the state to pass to that node.

```

const continueToJokes = (state: { subjects: string[] }) => {

return state.subjects.map(

(subject) => new Send("generate_joke", { subject })

);

};

const graph = new StateGraph(...)

.addConditionalEdges("nodeA", continueToJokes)

.compile();

```

…

`Command` object from node functions:

```

import { StateGraph, Annotation, Command } from "@langchain/langgraph";

const StateAnnotation = Annotation.Root({

foo: Annotation<string>,

});

const myNode = (state: typeof StateAnnotation.State) => {

return new Command({

// state update

update: {

foo: "bar",

},

// control flow

goto: "myOtherNode",

});

};

```

…

```

import { tool } from "@langchain/core/tools";

const lookupUserInfo = tool(async (input, config) => {

const userInfo = getUserInfo(config);

return new Command({

// update state keys

update: {

user_info: userInfo,

messages: [

new ToolMessage({

content: "Successfully looked up user information",

tool_call_id: config.toolCall.id,

}),

],

},

});

}, {

name: "lookup_user_info",

description: "Use this to look up user information to better assist them with their questions.",

schema: z.object(...)

});

```

…

### Human-in-the-loop¶

`Command` is an important part of human-in-the-loop workflows: when using

`interrupt()` to collect user input,

`Command` is then used to supply the input and resume execution via

`new Command({ resume: "User input" })`. Check out this conceptual guide for more information.

## Persistence¶

LangGraph provides built-in persistence for your agent's state using checkpointers. Checkpointers save snapshots of the graph state at every superstep, allowing resumption at any time. This enables features like human-in-the-loop interactions, memory management, and fault-tolerance. You can even directly manipulate a graph's state after its execution using the appropriate

`get` and

`update` methods. For more details, see the conceptual guide for more information.

…

## Storage¶

LangGraph provides built-in document storage through the BaseStore interface. Unlike checkpointers, which save state by thread ID, stores use custom namespaces for organizing data. This enables cross-thread persistence, allowing agents to maintain long-term memories, learn from past interactions, and accumulate knowledge over time. Common use cases include storing user profiles, building knowledge bases, and managing global preferences across all threads.

…

- For threads at the end of the graph (i.e. not interrupted) you can change the entire topology of the graph (i.e. all nodes and edges, remove, add, rename, etc)

- For threads currently interrupted, we support all topology changes other than renaming / removing nodes (as that thread could now be about to enter a node that no longer exists) -- if this is a blocker please reach out and we can prioritize a solution.

…

## Configuration¶

When creating a graph, you can also mark that certain parts of the graph are configurable. This is commonly done to enable easy switching between models or system prompts. This allows you to create a single "cognitive architecture" (the graph) but have multiple different instances of it.

You can then pass this configuration into the graph using the
`configurable` config field.

```

const config = { configurable: { llm: "anthropic" } };

await graph.invoke(inputs, config);

```

You can then access and use this configuration inside a node:

```

const nodeA = (state, config) => {

const llmType = config?.configurable?.llm;

let llm: BaseChatModel;

if (llmType) {

const llm = getLlm(llmType);



...

};

```

See this guide for a full breakdown on configuration

…

Read this how-to to learn more about how the recursion limit works.

`interrupt`¶

Use the interrupt function to

**pause** the graph at specific points to collect user input. The

`interrupt` function surfaces interrupt information to the client, allowing the developer to collect user input, validate the graph state, or make decisions before resuming execution.

…

Resuming the graph is done by passing a

`Command` object to the graph with the

`resume` key set to the value returned by the

`interrupt` function.

Read more about how the

`interrupt` is used for

**human-in-the-loop** workflows in the Human-in-the-loop conceptual guide.

**Note:** The

`interrupt` function is not currently available in web environments.

## Breakpoints¶

Breakpoints pause graph execution at specific points and enable stepping through execution step by step. Breakpoints are powered by LangGraph's

**persistence layer**, which saves the state after each graph step. Breakpoints can also be used to enable **human-in-the-loop** workflows, thou