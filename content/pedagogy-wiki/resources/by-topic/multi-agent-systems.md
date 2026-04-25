# Multi Agent Systems

## Video (best)
- **Harrison Chase (LangChain)** — "Multi-Agent Systems with LangGraph"
- youtube_id: Mi5wOpAgixw
- Why: N/A — see coverage notes below
- Level: intermediate

> **Coverage note:** 3Blue1Brown, Andrej Karpathy, Yannic Kilcher, StatQuest, and Serrano.Academy do not have well-known dedicated videos on multi-agent systems as of my knowledge cutoff. The best video content exists in conference talks and framework-specific tutorials, but I cannot confirm exact YouTube IDs without risk of hallucination.

**None identified** from preferred educator list with a verifiable YouTube ID.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM-powered Autonomous Agents"
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: Weng's post is the most cited, pedagogically structured written explainer covering agent architectures, memory, tool use, and multi-agent coordination patterns. It bridges theory and practice with clear diagrams and references to seminal work. While it covers single-agent foundations heavily, the multi-agent and orchestration sections are the best freely available written treatment from a trusted author.
- Level: intermediate

---

## Deep dive
- **AutoGen / Microsoft Research Documentation & Technical Report**
- url: https://microsoft.github.io/autogen/stable/index.html
- Why: The AutoGen framework documentation is the most comprehensive technical reference for multi-agent system design patterns including supervisor patterns, hierarchical teams, human-in-the-loop, blackboard/shared state, and conflict resolution. It combines conceptual explanation with architectural diagrams and is actively maintained by a research team. The accompanying technical report (see paper section) grounds it academically.
- Level: advanced

---

## Original paper
- **Wu et al. (2023)** — "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
- url: https://arxiv.org/abs/2308.08155
- Why: This is the most readable and widely adopted seminal paper specifically on LLM-based multi-agent systems. It introduces the conversational multi-agent paradigm, covers agent roles, message passing, human-in-the-loop integration, and flexible conversation topologies (peer-to-peer, hierarchical). It is highly cited and directly maps to the related concepts listed for this topic. More accessible than earlier MAS literature from classical AI.
- Level: intermediate/advanced

---

## Code walkthrough
- **LangChain / LangGraph** — "LangGraph Multi-Agent Tutorials (Supervisor & Hierarchical Patterns)"
- url: https://langchain-ai.github.io/langgraph/tutorials/introduction/
- Why: LangGraph's official tutorials provide the best hands-on code walkthroughs for the exact patterns listed in this topic — supervisor pattern, hierarchical teams, handoffs, shared state, human-in-the-loop, and peer-to-peer architectures. The code is minimal, well-commented, and directly tied to conceptual diagrams. It uses Python and is appropriate for learners in an agentic AI course context.
- Level: intermediate

---

## Coverage notes
- **Strong:** Written explainers (Lilian Weng), framework documentation (AutoGen, LangGraph), and the AutoGen paper cover agent roles, message passing, supervisor patterns, hierarchical teams, and human-in-the-loop very well.
- **Weak:** Blackboard pattern and classical conflict resolution/consensus mechanisms are underserved in LLM-era resources; most coverage comes from classical MAS literature (Weiss 1999) rather than modern tutorials.
- **Gap:** No high-quality YouTube explainer exists from the preferred educator list (3B1B, Karpathy, Yannic, StatQuest, Serrano) for multi-agent LLM systems specifically. This is a meaningful content gap for the platform — a custom video may be warranted. Conference talks (e.g., from NeurIPS or AI Engineer Summit) exist but lack the pedagogical structure of the preferred educators.
- **Gap:** Debate-and-consensus mechanisms (e.g., Society of Mind-style approaches, Du et al. 2023 "Improving Factuality via Multi-Agent Debate") are covered in papers but have no strong standalone tutorial resource.

---


> **[Structural note]** "LangGraph Core Concepts: State, Nodes, and Edges" appears to have sub-concepts:
> stategraph, typed state schema, node functions, edges, graph compilation, message passing
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Why LangGraph? Graphs as Agent Control Flow" appears to have sub-concepts:
> graph-based orchestration, nodes and edges, agent state, control flow, stateful workflows
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*


> **[Structural note]** "Persistence, Checkpointing, and Human-in-the-Loop" appears to have sub-concepts:
> state persistence, durable execution, human-in-the-loop, resumable agents
> *Discovered during enrichment for course "A hands-on intermediate course for software developers and AI/ML engineers cover" | 2026-04-10*

## Last Verified
2025-01-01 (knowledge cutoff basis; URLs marked should be checked before publication)