# Agent Fundamentals

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- youtube_id: zjkBMFhNj_g
- Why: While not exclusively about agents, Karpathy's treatment of LLMs as the cognitive core of agents, including tool use, memory, and autonomous action loops, provides the clearest conceptual foundation for understanding why LLM agents work the way they do. His systems-level thinking maps directly onto agent architecture concepts.
- Level: beginner/intermediate

> Karpathy's video is well-known and covers LLM systems thinking that maps to agent architecture concepts. No single YouTube video from the preferred educators focuses exclusively on agent fundamentals with full depth.

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM Powered Autonomous Agents"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: This is the canonical written reference for LLM agent fundamentals. Weng systematically covers the four pillars — planning, memory, tool use, and action — with clear diagrams and concrete examples. It introduces ReAct, Plan-and-Execute, reflection, and self-correction in a single coherent framework. Widely cited in both academic and practitioner communities.
- Level: intermediate

## Deep dive
- **LangGraph / LangChain** — "LangGraph Conceptual Documentation: Agents"
- url: https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/
- Why: Provides the most thorough technical treatment of agent loops, orchestration patterns, state management, and multi-agent coordination as actually implemented in production systems. Covers the agent loop, reactivity vs. proactivity, and orchestration patterns (supervisor, hierarchical) with code-grounded explanations. Directly relevant to LangGraph, CrewAI-style patterns, and the OpenAI Agents SDK mental model.
- Level: intermediate/advanced

## Original paper
- **Yao et al., 2022** — "ReAct: Synergizing Reasoning and Acting in Language Models"
- url: https://arxiv.org/abs/2210.03629
- Why: ReAct is the most readable and foundational paper for understanding the agent loop as a concrete algorithmic pattern. It introduces the interleaving of reasoning traces and actions that underpins virtually every modern LLM agent framework (LangGraph, AutoGen, CrewAI, OpenAI Agents SDK). Short, well-structured, and directly teachable.
- Level: intermediate

## Code walkthrough
- **OpenAI** — "OpenAI Agents SDK Quickstart / Cookbook"
- url: https://openai.github.io/openai-agents-python/
- Why: The OpenAI Agents SDK (released 2025) provides the cleanest minimal implementation of the agent loop — tools, handoffs, guardrails — with official documentation and runnable examples. It is pedagogically superior to older LangChain agent examples because the abstractions are simpler and the code more readable for learners encountering agents for the first time.
- Level: beginner/intermediate

> **Alternative if above unverified:** The [LangGraph "Build a Basic Agent" tutorial](https://langchain-ai.github.io/langgraph/tutorials/introduction/) is a well-maintained, beginner-friendly code walkthrough covering the agent loop with explicit state graphs.

---

## Coverage notes
- **Strong:** Written/blog coverage is excellent — Lilian Weng's post is genuinely one of the best educational resources in the entire ML ecosystem for this topic.
- **Strong:** Paper coverage is strong; ReAct is short, readable, and directly maps to practitioner frameworks.
- **Weak:** Video coverage from top educators (Karpathy, 3Blue1Brown, Yannic Kilcher) does not yet include a dedicated, comprehensive agent-fundamentals explainer. Most videos either treat agents superficially or focus on a specific framework rather than the underlying concepts.
- **Gap:** No single video cleanly covers the full conceptual stack: agent loop → goal-directed behavior → reactivity/proactivity → reflection → orchestration patterns. This is a genuine content gap in the preferred educator tier.
- **Gap:** AutoGen and CrewAI specifically lack deep-dive pedagogical resources from authoritative educators; most content is vendor documentation or low-quality tutorial blogs.
- **Emerging:** The OpenAI Agents SDK (2025) is too new for mature third-party educational content; official docs are currently the best available source.

---

## Last Verified
2025-01-01 (resources from 2023–2025; SDK links marked due to potential URL changes post-release)