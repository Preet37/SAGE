# Source: https://docs.agentscope.io/basic-concepts/context-and-memory
# Title: Context and Memory - AgentScope
# Fetched via: jina
# Date: 2026-04-10

Title: Context and Memory - AgentScope


# Context and Memory - AgentScope


[AgentScope home page![Image 1: dark logo](https://mintcdn.com/agentscope-ai-786677c7/ypv6xWD33tVApmTg/logo/agentscope.svg?fit=max&auto=format&n=ypv6xWD33tVApmTg&q=85&s=1c9a848ffa88ffa648f07542fe23e3e7)![Image 2: dark logo](https://mintcdn.com/agentscope-ai-786677c7/ypv6xWD33tVApmTg/logo/agentscope.svg?fit=max&auto=format&n=ypv6xWD33tVApmTg&q=85&s=1c9a848ffa88ffa648f07542fe23e3e7)](https://docs.agentscope.io/)


English

Search...

⌘K Ask AI

Search...

Navigation

Basic Concepts

Context and Memory

[Guides](https://docs.agentscope.io/)

*   [Home Page](https://agentscope.io/)
*   [Blog](https://agentscope.io/blogs/)

##### Get Started

*   [What is AgentScope?](https://docs.agentscope.io/)
*   [Quickstart](https://docs.agentscope.io/quickstart)

##### Tutorial

*   [Personal Research Assistant](https://docs.agentscope.io/tutorial/tutorial_research_agent)
*   [Multi-Agent Customer Support System](https://docs.agentscope.io/tutorial/tutorial_sales_agent)

##### Out-of-box Agents

*   [Alias](https://docs.agentscope.io/out-of-box-agents/alias)
*   [Browser-use Agent](https://docs.agentscope.io/out-of-box-agents/browser-use)
*   [Deep Research](https://docs.agentscope.io/out-of-box-agents/deep-research)
*   [Finance Analysis](https://docs.agentscope.io/out-of-box-agents/alias-finance)
*   [Data Science](https://docs.agentscope.io/out-of-box-agents/data-science)
*   [DataJuicer Agent](https://docs.agentscope.io/out-of-box-agents/datajuicer-agent)
*   [EvoTraders](https://docs.agentscope.io/out-of-box-agents/evo-trader)

##### Basic Concepts

*   [Message](https://docs.agentscope.io/basic-concepts/msg)
*   [Agent](https://docs.agentscope.io/basic-concepts/agent)
*   [Model](https://docs.agentscope.io/basic-concepts/model)
*   [Context and Memory](https://docs.agentscope.io/basic-concepts/context-and-memory)
*   [Tool](https://docs.agentscope.io/basic-concepts/tool)

##### Building Blocks

*   [Agent](https://docs.agentscope.io/building-blocks/agent)
*   [Models](https://docs.agentscope.io/building-blocks/models)
*   [Memory](https://docs.agentscope.io/building-blocks/context-and-memory)
*   [RAG](https://docs.agentscope.io/building-blocks/rag)
*   [Tool Capabilities](https://docs.agentscope.io/building-blocks/tool-capabilities)
*   [Hooking Functions](https://docs.agentscope.io/building-blocks/hooking-functions)
*   [Orchestration](https://docs.agentscope.io/building-blocks/orchestration)

##### Observe & Evaluate

*   [Observability](https://docs.agentscope.io/observe-and-evaluate/observability)
*   [Evaluation](https://docs.agentscope.io/observe-and-evaluate/evaluation)

##### Tune Agent

*   [Overview](https://docs.agentscope.io/tune-agent/tune-your-first-agent)
*   [Model Selection](https://docs.agentscope.io/tune-agent/model-selection-tuning)
*   [Prompt Tuning](https://docs.agentscope.io/tune-agent/prompt-tuning)
*   [Reinforcement Learning](https://docs.agentscope.io/tune-agent/model-weights-tuning)
*   [Multi-Agent Tuning](https://docs.agentscope.io/tune-agent/tune-multi-agents)

##### Deploy & Serve

*   [Agent as Service](https://docs.agentscope.io/deploy-and-serve/agent-as-service)
*   [Sandbox and Tool](https://docs.agentscope.io/deploy-and-serve/sandbox-and-tool)

##### Others

*   [FAQ](https://docs.agentscope.io/others/faq)

On this page

*   [Why It Matters](https://docs.agentscope.io/basic-concepts/context-and-memory#why-it-matters)
*   [Three Layers in AgentScope](https://docs.agentscope.io/basic-concepts/context-and-memory#three-layers-in-agentscope)
*   [Context (inference-time input)](https://docs.agentscope.io/basic-concepts/context-and-memory#context-inference-time-input)
*   [Short-Term Memory (session state)](https://docs.agentscope.io/basic-concepts/context-and-memory#short-term-memory-session-state)
*   [Long-Term Memory (cross-session knowledge)](https://docs.agentscope.io/basic-concepts/context-and-memory#long-term-memory-cross-session-knowledge)
*   [How They Work Together](https://docs.agentscope.io/basic-concepts/context-and-memory#how-they-work-together)
*   [Context Management vs Memory Management](https://docs.agentscope.io/basic-concepts/context-and-memory#context-management-vs-memory-management)
*   [Summary](https://docs.agentscope.io/basic-concepts/context-and-memory#summary)

Basic Concepts

# Context and Memory

Copy page

Background about Context and Memory

Copy page

This document introduces how AgentScope handles context and memory in agent workflows.

For implementation details and APIs, see [Context and Memory](https://docs.agentscope.io/building-blocks/context-and-memory).

* * *

## [​](https://docs.agentscope.io/basic-concepts/context-and-memory#why-it-matters)

Why It Matters

Without memory, an agent treats every turn as a new conversation. With memory, it can:
*   keep conversation continuity,
*   remember user preferences and task state,
*   retrieve useful history when needed.

In AgentScope, this is built around `Msg`, memory backends, and prompt construction.

* * *

## [​](https://docs.agentscope.io/basic-concepts/context-and-memory#three-layers-in-agentscope)

Three Layers in AgentScope

### [​](https://docs.agentscope.io/basic-concepts/context-and-memory#context-inference-time-input)

Context (inference-time input)

**Context** is the final input sent to the model for one inference call.In AgentScope terms, it is typically assembled from:
*   system instructions,
*   current user `Msg`,
*   selected short-term history,
*   retrieved long-term memory,
*   tool results.

Context is fast and direct, but limited by token budget.
### [​](https://docs.agentscope.io/basic-concepts/context-and-memory#short-term-memory-session-state)

Short-Term Memory (session state)

Short-term memory tracks the current session and usually stores `Msg` objects.In AgentScope, this is provided by `MemoryBase` implementations (for example: `InMemoryMemory`, `RedisMemory`, `AsyncSQLAlchemyMemory`).Common usage:
*   recent conversation turns,
*   temporary task progress,
*   marked messages (such as `hint`, `summary`, `tool_result`).

### [​](https://docs.agentscope.io/basic-concepts/context-and-memory#long-term-memory-cross-session-knowledge)

Long-Term Memory (cross-session knowledge)

Long-term memory stores information that should survive session boundaries.In AgentScope, this is abstracted by `LongTermMemoryBase` implementations. Typical content includes:
*   stable user preferences,
*   important facts from previous interactions,
*   retrievable semantic memories.

* * *

## [​](https://docs.agentscope.io/basic-concepts/context-and-memory#how-they-work-together)

How They Work Together

A typical agent turn looks like this:
1.   Load recent session memory (short-term).
2.   Retrieve relevant long-term memory (if needed).
3.   Build model context with current user input and retrieved signals.
4.   Run model inference.
5.   Write new messages back to short-term memory, and optionally persist key facts to long-term memory.

This loop is often managed inside the agent’s reply lifecycle (for example, in `ReActAgent` workflows).

* * *

## [​](https://docs.agentscope.io/basic-concepts/context-and-memory#context-management-vs-memory-management)

Context Management vs Memory Management

In practice, the boundary is soft:
*   **Memory management** focuses on storing, retrieving, marking, and updating information.
*   **Context management** focuses on selecting and assembling the right subset of that information into the model input.

So memory provides the source material, and context decides what enters the current inference window.

* * *

## [​](https://docs.agentscope.io/basic-concepts/context-and-memory#summary)

Summary

| Layer | What it is | AgentScope mapping |
| --- | --- | --- |
| **Context** | Input for one inference | Prompt assembled from `Msg` + retrieved memory + tool outputs |
| **Short-Term Memory** | Session-level working state | `MemoryBase` backends storing and filtering `Msg` |
| **Long-Term Memory** | Persistent cross-session knowledge | `LongTermMemoryBase` retrieval and storage |

Good agent behavior depends less on storing everything, and more on selecting the **right memory at the right time**.

[Model](https://docs.agentscope.io/basic-concepts/model)[Tool](https://docs.agentscope.io/basic-concepts/tool)

⌘I

[x](https://x.com/agentscope)[github](https://github.com/agentscope-ai)[discord](https://discord.gg/eYMpfnkG8h)

[Powered by This documentation is built and hosted on Mintlify, a developer documentation platform](https://www.mintlify.com/?utm_campaign=poweredBy&utm_medium=referral&utm_source=agentscope-ai-786677c7)

Assistant

Responses are generated using AI and may contain mistakes.