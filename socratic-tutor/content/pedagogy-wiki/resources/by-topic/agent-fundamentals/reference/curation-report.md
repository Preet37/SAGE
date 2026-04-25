# Curation Report: Agent Fundamentals
**Topic:** `agent-fundamentals` | **Date:** 2026-04-09 16:11
**Library:** 6 existing → 24 sources (18 added, 11 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (18)
- **[paper]** [[PDF] arXiv:2303.17651v2 [cs.CL] 25 May 2023](https://arxiv.org/pdf/2303.17651.pdf)
  Adds a primary-source, step-by-step formulation of iterative self-correction/refinement that the tutor can cite and translate into pseudocode for agent loops.
- **[reference_doc]** [agentchat.conversable_agent | AutoGen 0.2](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/)
  Provides authoritative, citable parameter surfaces and default behaviors for AutoGen’s core agent base class, enabling precise answers about configuration knobs.
- **[benchmark]** [3.1 Alfworld](https://arxiv.org/html/2403.14589v3)
  Contributes concrete benchmark numbers and iterative-improvement ablations on standard agentic environments useful for comparing agent strategies empirically.
- **[explainer]** [[PDF] A practical guide to building agents - OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
  Adds an authoritative, practitioner-oriented deployment reference that the tutor can use to ground discussions of real-world agent design decisions and operational constraints.
- **[paper]** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
  Agent Fundamentals typically needs a canonical planning-loop reference; ToT is a widely-cited primary source with concrete algorithm structure that maps cleanly to Plan-and-Execute style tutoring.
- **[paper]** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366)
  The library has Self-Refine but lacks the seminal Reflexion formulation; this paper is the standard citation for reflection-as-memory updates in agent loops.
- **[paper]** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291)
  Provides an authoritative end-to-end agent loop with tools and long-horizon memory/skills—useful for teaching how “agent = policy + memory + tools + learning loop” is operationalized.
- **[reference_doc]** [CrewAI (official repository and docs)](https://github.com/crewAIInc/crewAI)
  The unfilled needs explicitly call for CrewAI runtime defaults/knobs; the official repo/docs are the most citable place for exact parameter names and behaviors.
- **[reference_doc]** [AutoGen 0.2 API Reference (index)](https://microsoft.github.io/autogen/0.2/docs/reference/)
  Even if “thin,” the index is valuable for quickly locating canonical signatures/defaults across the framework—especially for group chat and orchestration pieces.
- **[benchmark]** [ReflAct: World-Grounded Decision Making in LLM Agents](https://arxiv.org/abs/2505.15182v2)
  Directly fills the request for specific comparative numbers on standard agent environments; the appendices are often where the most teachable tables live.
- **[explainer]** [The Evolution of Tool Use in LLM Agents](https://arxiv.org/html/2603.22862v2)
  The library has a general OpenAI deployment guide, but this adds a concrete, experience-driven systems narrative that helps teach why certain agent design choices win in practice.
- **[paper]** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) *(promoted by reviewer)*
  Agent Fundamentals typically needs a canonical planning-loop reference; ToT is a widely-cited primary source with concrete algorithm structure that maps cleanly to Plan-and-Execute style tutoring.
- **[paper]** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) *(promoted by reviewer)*
  The library has Self-Refine but lacks the seminal Reflexion formulation; this paper is the standard citation for reflection-as-memory updates in agent loops.
- **[paper]** [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://arxiv.org/abs/2305.16291) *(promoted by reviewer)*
  Provides an authoritative end-to-end agent loop with tools and long-horizon memory/skills—useful for teaching how “agent = policy + memory + tools + learning loop” is operationalized.
- **[reference_doc]** [CrewAI (official repository and docs)](https://github.com/crewAIInc/crewAI) *(promoted by reviewer)*
  The unfilled needs explicitly call for CrewAI runtime defaults/knobs; the official repo/docs are the most citable place for exact parameter names and behaviors.
- **[reference_doc]** [AutoGen 0.2 API Reference (index)](https://microsoft.github.io/autogen/0.2/docs/reference/) *(promoted by reviewer)*
  Even if “thin,” the index is valuable for quickly locating canonical signatures/defaults across the framework—especially for group chat and orchestration pieces.
- **[benchmark]** [ReflAct: World-Grounded Decision Making in LLM Agents](https://arxiv.org/abs/2505.15182v2) *(promoted by reviewer)*
  Directly fills the request for specific comparative numbers on standard agent environments; the appendices are often where the most teachable tables live.
- **[explainer]** [The Evolution of Tool Use in LLM Agents](https://arxiv.org/html/2603.22862v2) *(promoted by reviewer)*
  The library has a general OpenAI deployment guide, but this adds a concrete, experience-driven systems narrative that helps teach why certain agent design choices win in practice.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **API Reference — AutoGen - Microsoft Open Source** — [API Reference — AutoGen - Microsoft Open Source](https://microsoft.github.io/autogen/dev/reference/index.html)
  _Skipped because:_ Broader index but less directly anchored to specific default values/knobs than the focused ConversableAgent reference page.
- **Guardrails** — [Guardrails](https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/)
  _Skipped because:_ Overlaps with the PDF version; the PDF is more stable/citable as a single artifact for a reference library.

## Reasoning
**Curator:** Selections prioritize primary-source algorithm loops (Self-Refine), official API defaults (AutoGen), and at least one concrete benchmark source plus an authoritative deployment guide; remaining gaps require sources not present in the candidate set (notably Plan-and-Execute/Reflexion originals, CrewAI/LangGraph defaults, and runnable end-to-end examples).
**Reviewer:** The curator’s additions are solid, but the library still misses a few canonical primary sources for planning/reflection loops plus thin-but-critical API references and at least one more benchmark-heavy agent paper with standard-environment tables.
