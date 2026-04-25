# Agent Workflows

## Video (best)
- **LangChain** — "LangGraph: Build Stateful, Multi-Agent Workflows"
- url: https://blog.langchain.dev/langgraph-multi-agent-workflows
- Why: LangGraph is one of the clearest, widely-used introductions to DAG/state-machine style orchestration for agents (nodes, edges, conditional routing, retries).
- Level: intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "LLM Powered Autonomous Agents"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: High-signal overview of agent building blocks and patterns (planning, tool use, memory) that underpin real workflows; good conceptual grounding before orchestration/production details.
- Level: intermediate

## Deep dive
- **LangChain Docs** — "LangGraph"
- url: https://langchain-ai.github.io/langgraph/
- Why: Practical deep dive into orchestration patterns: DAG-like graphs, conditional branching, cycles, persistence/checkpointing, streaming, and human-in-the-loop patterns.
- Level: intermediate/advanced
- **Microsoft** — "AutoGen"
- url: https://microsoft.github.io/autogen/stable/index.html
- Why: Multi-agent conversation/workflow patterns, tool execution, and coordination; useful for parallel/role-based agent workflows and production-ish patterns.
- Level: intermediate/advanced

## Original paper
- **ReAct** — "ReAct: Synergizing Reasoning and Acting in Language Models"
- url: https://arxiv.org/abs/2210.03629
- Why: Foundational pattern for tool-using agent loops (reason → act → observe), which is the core of many sequential chains and orchestration designs.
- Level: intermediate
- **MRKL** — "MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning"
- url: https://arxiv.org/abs/2205.00445
- Why: Early, influential framing for routing/orchestrating between tools and modules (a precursor to many workflow-engine patterns).
- Level: intermediate

## Code walkthrough
- **LangChain (GitHub)** — "LangGraph" (examples)
- url: https://github.com/langchain-ai/langgraph
- Why: Concrete reference implementations for graph/DAG orchestration, streaming, retries, and human-in-the-loop checkpoints.
- Level: intermediate
- **Microsoft (GitHub)** — "AutoGen" (examples)
- url: https://github.com/microsoft/autogen
- Why: End-to-end multi-agent workflow examples (coordinator/worker patterns, tool calls, conversation-driven orchestration).
- Level: intermediate

## Coverage notes
- Strong: orchestration-patterns (DAG/graph orchestration, sequential chains, conditional routing), workflow engines (LangGraph), multi-agent coordination (AutoGen), core agent loop pattern (ReAct).
- Weak: production-patterns specifics (agent-as-API design, robust retry/fallback taxonomies, streaming UX patterns) in a single canonical explainer; agent-deployment details are scattered across vendor docs.
- Gap: agent tracing/observability and deployment SRE guidance (latency management, cost optimization) in one stable, vendor-neutral “best” resource; likely needs a dedicated page or curated set of vendor/OSS observability docs.


> **[Structural note]** "Agent Planning: How Agents Decide What to Do Next" appears to have sub-concepts:
> llm agent planning, subgoal generation, plan execution, feedback-driven replanning, multi-step reasoning, goal-directed behavior
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Multi-Agent Architectures: Supervisors and Subgraphs" appears to have sub-concepts:
> multi-agent systems, agent delegation, agents as tools, agent orchestration
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Comparing Agentic Frameworks: LangGraph, AutoGen, CrewAI, and OpenAI Assistants" appears to have sub-concepts:
> autogen, openai assistants api, control flow, multi-agent orchestration, durable execution, human-in-the-loop
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*

## Last Verified
2026-04-09