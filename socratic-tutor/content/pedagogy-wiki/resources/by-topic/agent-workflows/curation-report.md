# Curation Report: Agent Planning: How Agents Decide What to Do Next
**Topic:** `agent-workflows` | **Date:** 2026-04-10 18:55
**Library:** 7 existing → 19 sources (12 added, 8 downloaded)
**Candidates evaluated:** 30
**Reviewer verdict:** needs_additions

## Added (12)
- **[paper]** [Understanding the planning of LLM agents: A survey](https://arxiv.org/abs/2402.02716)
  A focused survey that systematizes LLM-agent planning: planning-loop formulations, plan representations, subgoal decomposition strategies, and replanning/feedback mechanisms—useful as a unifying reference beyond framework docs.
   — covers: A concrete definition of LLM agent planning as a loop (goal -> plan -> act -> observe -> update), including plan representations and termination conditions, Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples, Feedback-driven replanning: how observations are compared to expectations, when to revise vs continue, and how to incorporate environment signals to reduce hallucinations, Goal-directed behavior in agents: explicit goals, constraints, reward/utility proxies, and how goals control next-action decisions
- **[paper]** [Perceive, Reflect, and Plan: Designing LLM Agent for Goal ...](https://arxiv.org/html/2408.04168v3)
  Provides a concrete agentic workflow (Perceive→Reflect→Plan) with an explicit loop structure, termination/updates, and case studies/prompt examples that make planning and replanning mechanics more operational than most high-level overviews.
   — covers: A concrete definition of LLM agent planning as a loop (goal -> plan -> act -> observe -> update), including plan representations and termination conditions, Feedback-driven replanning: how observations are compared to expectations, when to revise vs continue, and how to incorporate environment signals to reduce hallucinations, Multi-step reasoning explanations with step-by-step examples (beyond just mentioning chain-of-thought/ReAct)
- **[paper]** [Describe, Explain, Plan and Select:](https://proceedings.neurips.cc/paper_files/paper/2023/file/6b8dfb8c0c12e6fafc6c256cb08a5ca7-Paper-Conference.pdf)
  A strong, peer-reviewed treatment of decomposing tasks into structured intermediate artifacts (description/explanation/plan) and then selecting actions—helpful for teaching plan representations and action selection in multi-step decision loops.
   — covers: A concrete definition of LLM agent planning as a loop (goal -> plan -> act -> observe -> update), including plan representations and termination conditions, Multi-step reasoning explanations with step-by-step examples (beyond just mentioning chain-of-thought/ReAct), Goal-directed behavior in agents: explicit goals, constraints, reward/utility proxies, and how goals control next-action decisions
- **[paper]** [[PDF] arXiv:2404.11584v1 [cs.AI] 17 Apr 2024](https://arxiv.org/pdf/2404.11584.pdf)
  Adds concrete execution mechanics for tool-using agents via a multi-agent planning/coding/tool-use pipeline, including tool selection, state/memory updates, and iterative online planning—complementing LangGraph/AutoGen docs with an evaluated algorithmic blueprint.
   — covers: Plan execution mechanics in tool-using agents (action selection, sequencing, tool-call/observation handling, error handling/retries), Feedback-driven replanning: how observations are compared to expectations, when to revise vs continue, and how to incorporate environment signals to reduce hallucinations, Goal-directed behavior in agents: explicit goals, constraints, reward/utility proxies, and how goals control next-action decisions
- **[paper]** [AdaPlanner: Adaptive Planning from Feedback](https://proceedings.nips.cc/paper_files/paper/2023/file/b5c8c1c117618267944b2617add0a766-Paper-Conference.pdf)
  This is a strong, peer-reviewed NeurIPS planning paper squarely about adapting plans from feedback—exactly the replanning/control loop mechanics the lesson emphasizes, and more authoritative than many LLM-agent-only writeups.
   — covers: Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples
- **[paper]** [Multi-Step Reasoning with Large Language Models (survey)](https://arxiv.org/html/2407.11511v2)
  Even if not strictly “agent planning,” this survey is a high-utility reference for step generation/evaluation/control—useful for teaching how agents decide the next step and how to structure/score intermediate steps beyond framework docs.
   — covers: Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples
- **[paper]** [How to think step-by-step: A mechanistic understanding of chain-of-thought reasoning](https://arxiv.org/abs/2402.18312)
  This provides unusually clear, mechanistic grounding for step-by-step decomposition and control; it can strengthen the lesson’s explanation of why/when stepwise plans help and how to shape next-action decisions.
   — covers: Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples
- **[tutorial]** [RePLan: Robotic Replanning with Perception and Language Models (review)](https://www.themoonlight.io/fr/review/replan-robotic-replanning-with-perception-and-language-models)
  While secondary, this is a uniquely clear, teaching-oriented walkthrough of perception→replanning loops in embodied settings; it can concretely illustrate observation/expectation mismatch and when to revise vs continue.
   — covers: Plan execution mechanics in tool-using agents (action selection, sequencing, tool-call/observation handling, error handling/retries)
- **[paper]** [AdaPlanner: Adaptive Planning from Feedback](https://proceedings.nips.cc/paper_files/paper/2023/file/b5c8c1c117618267944b2617add0a766-Paper-Conference.pdf) *(promoted by reviewer)*
  This is a strong, peer-reviewed NeurIPS planning paper squarely about adapting plans from feedback—exactly the replanning/control loop mechanics the lesson emphasizes, and more authoritative than many LLM-agent-only writeups.
   — fills: Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples
- **[paper]** [Multi-Step Reasoning with Large Language Models (survey)](https://arxiv.org/html/2407.11511v2) *(promoted by reviewer)*
  Even if not strictly “agent planning,” this survey is a high-utility reference for step generation/evaluation/control—useful for teaching how agents decide the next step and how to structure/score intermediate steps beyond framework docs.
   — fills: Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples
- **[paper]** [How to think step-by-step: A mechanistic understanding of chain-of-thought reasoning](https://arxiv.org/abs/2402.18312) *(promoted by reviewer)*
  This provides unusually clear, mechanistic grounding for step-by-step decomposition and control; it can strengthen the lesson’s explanation of why/when stepwise plans help and how to shape next-action decisions.
   — fills: Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples
- **[tutorial]** [RePLan: Robotic Replanning with Perception and Language Models (review)](https://www.themoonlight.io/fr/review/replan-robotic-replanning-with-perception-and-language-models) *(promoted by reviewer)*
  While secondary, this is a uniquely clear, teaching-oriented walkthrough of perception→replanning loops in embodied settings; it can concretely illustrate observation/expectation mismatch and when to revise vs continue.
   — fills: Plan execution mechanics in tool-using agents (action selection, sequencing, tool-call/observation handling, error handling/retries)

## Near-Misses (11) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Watch Every Step! LLM Agent Learning via Iterative Ste** — [[PDF] Watch Every Step! LLM Agent Learning via Iterative Step-Level ...](https://aclanthology.org/2024.emnlp-main.93.pdf)
  _Skipped because:_ Likely valuable for step-level supervision, but it is more about learning/training signals than a clear, reusable planning/execution framework for teaching core agent planning loops.
- **Michał Zawalski** — [Michał Zawalski](https://arxiv.org/html/2406.03361)
  _Skipped because:_ Covers hierarchical subgoal methods (HRL/search) but appears less directly tied to LLM agent planning and tool-using execution, making it a weaker fit for this lesson’s focus.
- **2.4 Evaluating Sub-Goal...** — [2.4 Evaluating Sub-Goal...](https://arxiv.org/html/2401.14043v2)
  _Skipped because:_ Overlaps heavily with the HRL-style subgoal discussion and is unclear/unstable as a standalone, citable source from the provided title/landing page.
- **Subgoal Ordering and Goal Augmentation** — [Subgoal Ordering and Goal Augmentation](https://www.ijcai.org/Proceedings/87-2/Papers/092.pdf)
  _Skipped because:_ Seminal for classical planning, but too disconnected from modern LLM agent loops/tool execution to justify inclusion over more directly applicable agent-planning sources.
- **[PDF] Landmark-Guided Subgoal Generation in Hierarchical ...** — [[PDF] Landmark-Guided Subgoal Generation in Hierarchical ...](https://proceedings.neurips.cc/paper/2021/file/ee39e503b6bedf0c98c388b7e8589aca-Paper.pdf)
  _Skipped because:_ High-quality HRL subgoal generation, but it doesn’t translate cleanly into promptable LLM-agent subgoal generation with worked tool-using examples.
- **[PDF] Generate Subgoal Images before Act: Unlocking the Chai** — [[PDF] Generate Subgoal Images before Act: Unlocking the Chain-of ...](https://openaccess.thecvf.com/content/CVPR2024/papers/Ni_Generate_Subgoal_Images_before_Act_Unlocking_the_Chain-of-Thought_Reasoning_in_CVPR_2024_paper.pdf)
  _Skipped because:_ Interesting for vision agents, but too modality-specific (subgoal images) for a general lesson on LLM agent planning and tool execution.
- **[PDF] Efficient Multi-Agent Collaboration with Tool Use for ** — [[PDF] Efficient Multi-Agent Collaboration with Tool Use for Online Planning ...](https://aclanthology.org/2025.findings-naacl.54.pdf)
  _Skipped because:_ Potentially strong, but the provided candidate list already includes the arXiv PDF for the same work; adding both would be redundant without confirming substantive differences.
- **Edinburgh Research Explorer** — [Edinburgh Research Explorer](https://www.pure.ed.ac.uk/ws/portalfiles/portal/482086583/DaganEtalLanguageGamification2024DynamicPlanning_final_version_.pdf)
  _Skipped because:_ The landing/title metadata is too unclear from the candidate snippet to confidently curate it as a stable, on-topic planning reference.
- **TAPE: Tool-Guided Adaptive Planning and Constrained Executio** — [TAPE: Tool-Guided Adaptive Planning and Constrained Execution in Language Model Agents](https://www.arxiv.org/pdf/2602.19633.pdf)
  _Skipped because:_ Looks directly on-target for constrained execution, but it is dated 2026 and beyond typical vetted coverage; would need extra scrutiny/validation before inclusion.
- **Learning to use tools via cooperative and interactive agents** — [Learning to use tools via cooperative and interactive agents](https://scholarlypublications.universiteitleiden.nl/access/item:4249454/download)
  _Skipped because:_ Could be relevant, but the candidate snippet appears mismatched/duplicative with MACT content and the venue/metadata aren’t clear enough to ensure it adds distinct value.
- **[PDF] arXiv:2404.11584v1 [cs.AI] 17 Apr 2024 - Rivista AI** — [[PDF] arXiv:2404.11584v1 [cs.AI] 17 Apr 2024 - Rivista AI](https://www.rivista.ai/wp-content/uploads/2024/06/2404.11584v1.pdf)
  _Skipped because:_ Redundant mirror of the arXiv PDF; prefer the canonical arXiv URL for stability and citation.

## Uncovered Gaps (2) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Methods for subgoal generation (prompt patterns, heuristics, search/planning algorithms, prioritization) with worked examples
- Plan execution mechanics in tool-using agents (action selection, sequencing, tool-call/observation handling, error handling/retries)

## Reasoning
**Curator:** Selections prioritize authoritative, citable papers that concretely define planning loops, representations, and replanning, plus at least one evaluated tool-use execution pipeline to complement existing framework docs. HRL-style subgoal papers were mostly excluded because they don’t translate into practical LLM-agent subgoal prompting/execution examples for this lesson.
**Reviewer:** The current set is solid for modern LLM-agent loop formulations, but it under-serves concrete subgoal-generation/search and replanning-from-feedback; adding one or two authoritative planning/control references (e.g., AdaPlanner) plus a strong multi-step reasoning control survey would materially strengthen the lesson.

---

# Curation Report: Multi-Agent Architectures: Supervisors and Subgraphs
**Topic:** `agent-workflows` | **Date:** 2026-04-10 19:02
**Library:** 15 existing → 23 sources (8 added, 5 downloaded)
**Candidates evaluated:** 30
**Reviewer verdict:** needs_additions

## Added (8)
- **[reference_doc]** [Subgraphs - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/use-subgraphs)
  Authoritative, stable documentation that concretely explains what LangGraph subgraphs are, how to package multi-node workflows as reusable modules, and how to compose them into larger graphs.
   — covers: LangGraph subgraphs: what a subgraph is, how to package a multi-node/agent workflow as a reusable module, and how to compose subgraphs into larger graphs
- **[reference_doc]** [AI Agent Orchestration Patterns - Azure Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns)
  A reputable, engineering-focused patterns guide that adds concrete orchestration fundamentals (including parallelism patterns and coordination responsibilities) beyond the existing research-heavy library.
   — covers: Parallel execution in multi-agent/graph runtimes: fan-out/fan-in patterns, concurrency controls, merging/aggregation strategies, and failure handling, General multi-agent system fundamentals: communication patterns, coordination strategies, role specialization, and orchestration responsibilities
- **[reference_doc]** [Handoffs - OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/handoffs/)
  This is the most direct, high-authority, implementation-level reference for delegation/handoffs (task transfer, state passing, and routing) from the primary vendor whose SDK explicitly names the pattern.
   — covers: Agent delegation and handoffs: protocols for transferring task, state, and tool results; criteria for selecting delegate agents; examples using OpenAI Agents SDK
- **[reference_doc]** [Handoffs | OpenAI Agents SDK (JavaScript)](https://openai.github.io/openai-agents-js/guides/handoffs/)
  Complements the Python handoffs doc with JS-specific mechanics and examples; worth including if the teaching wiki supports both ecosystems or wants language-agnostic conceptual coverage backed by concrete code.
   — covers: Agent delegation and handoffs: protocols for transferring task, state, and tool results; criteria for selecting delegate agents; examples using OpenAI Agents SDK
- **[reference_doc]** [A practical guide to building agents - OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)
  High-authority, curated guidance that typically covers orchestration patterns (including delegation/handoffs and tool/agent boundaries) in a more conceptual, teachable way than SDK docs alone.
   — covers: Supervisor (router/controller) agent pattern: definition, routing logic, maintaining small context, coordinating specialist agents, and concrete examples, Agent delegation and handoffs: protocols for transferring task, state, and tool results; criteria for selecting delegate agents; examples using OpenAI Agents SDK, Agents-as-tools pattern: how an agent is exposed/invoked like a tool, interface contracts (inputs/outputs), and tracing/debugging implications
- **[reference_doc]** [Handoffs - OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/handoffs/) *(promoted by reviewer)*
  This is the most direct, high-authority, implementation-level reference for delegation/handoffs (task transfer, state passing, and routing) from the primary vendor whose SDK explicitly names the pattern.
   — fills: Agent delegation and handoffs: protocols for transferring task, state, and tool results; criteria for selecting delegate agents; examples using OpenAI Agents SDK
- **[reference_doc]** [Handoffs | OpenAI Agents SDK (JavaScript)](https://openai.github.io/openai-agents-js/guides/handoffs/) *(promoted by reviewer)*
  Complements the Python handoffs doc with JS-specific mechanics and examples; worth including if the teaching wiki supports both ecosystems or wants language-agnostic conceptual coverage backed by concrete code.
   — fills: Agent delegation and handoffs: protocols for transferring task, state, and tool results; criteria for selecting delegate agents; examples using OpenAI Agents SDK
- **[reference_doc]** [A practical guide to building agents - OpenAI](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) *(promoted by reviewer)*
  High-authority, curated guidance that typically covers orchestration patterns (including delegation/handoffs and tool/agent boundaries) in a more conceptual, teachable way than SDK docs alone.
   — fills: Supervisor (router/controller) agent pattern: definition, routing logic, maintaining small context, coordinating specialist agents, and concrete examples, Agent delegation and handoffs: protocols for transferring task, state, and tool results; criteria for selecting delegate agents; examples using OpenAI Agents SDK, Agents-as-tools pattern: how an agent is exposed/invoked like a tool, interface contracts (inputs/outputs), and tracing/debugging implications

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Subgraphs - Docs by LangChain** — [Subgraphs - Docs by LangChain](https://7x.mintlify.app/oss/javascript/langgraph/use-subgraphs)
  _Skipped because:_ Likely overlaps heavily with the Python subgraphs doc; adding both would be redundant unless the lesson explicitly needs JS examples.
- **LangGraph Intro - Structuring AI Agent Workflows with Subgra** — [LangGraph Intro - Structuring AI Agent Workflows with Subgraphs in LangGraph](https://www.youtube.com/watch?v=52oj4SPUHRA)
  _Skipped because:_ Potentially useful, but video content is harder to skim/verify and is redundant once the official subgraphs docs are included.
- **DynTaskMAS: A Dynamic Task Graph-driven Framework for ... - ** — [DynTaskMAS: A Dynamic Task Graph-driven Framework for ... - arXiv](https://arxiv.org/html/2503.07675v1)
  _Skipped because:_ Promising for parallel/dynamic task graphs, but it’s early and framework-specific; the library benefits more from broadly applicable, authoritative patterns docs first.
- **Learning Latency-Aware Orchestration for Parallel Multi-Agen** — [Learning Latency-Aware Orchestration for Parallel Multi-Agent ...](https://arxiv.org/html/2601.10560v1)
  _Skipped because:_ Out of scope for a practical supervisor/subgraph lesson (optimization-focused) and appears to be a very new preprint with unclear adoption/impact.
- **Parallel Fan-Out - openagent** — [Parallel Fan-Out - openagent](https://openagenthub.io/patterns/orchestration/parallel/)
  _Skipped because:_ Unclear authority and the snippet looks boilerplate/duplicated; not confident it provides deep, reliable guidance beyond what Azure’s patterns page covers.
- **Concurrent Multi-Agent Orchestration: Fan-out/Fan-in with Mi** — [Concurrent Multi-Agent Orchestration: Fan-out/Fan-in with Microsoft ...](https://arafattehsin.com/blog/agent-orchestration-patterns-part-3/)
  _Skipped because:_ Could be practical, but it’s a personal blog (stability/authority risk) and overlaps with the more durable Azure Architecture Center patterns resource.
- **Choosing the right orchestration pattern for multi-agent sys** — [Choosing the right orchestration pattern for multi-agent systems](https://www.kore.ai/blog/choosing-the-right-orchestration-pattern-for-multi-agent-systems)
  _Skipped because:_ Likely a high-level vendor blog; may describe the supervisor pattern but typically lacks the concrete routing/state/handoff mechanics needed to fill the gaps.
- **Design Patterns for Multi-Agent Systems: Building Supervisor** — [Design Patterns for Multi-Agent Systems: Building Supervisor to ...](https://www.trixlyai.com/blog/technical-14/design-patterns-for-multi-agent-systems-building-supervisor-to-worker-architectures-93)
  _Skipped because:_ Appears to mirror the Kore.ai content in the preview and is not an obviously authoritative or canonical reference.
- **Router-Supervisor Pattern | Esy Agents Reference** — [Router-Supervisor Pattern | Esy Agents Reference](https://esy.com/agents/patterns/router-supervisor/)
  _Skipped because:_ A pattern page could help, but authority and depth are unclear; the preview suggests it may be derivative rather than a substantive, original treatment.
- **How to Use the Supervisor Pattern for Multi-Agent Voice AI S** — [How to Use the Supervisor Pattern for Multi-Agent Voice AI Systems](https://livekit.com/blog/supervisor-pattern-voice-agents)
  _Skipped because:_ Narrow (voice-agent specific) and likely implementation-tied; doesn’t clearly generalize to supervisor routing, delegation protocols, and reusable subgraph composition.
- **Architecting Multi-Agent Systems: Solving the 'Supervisor Bo** — [Architecting Multi-Agent Systems: Solving the 'Supervisor Bottleneck ...](https://dev.to/ameer-pk/architecting-multi-agent-systems-solving-the-supervisor-bottleneck-in-production-286g)
  _Skipped because:_ DEV.to is often uneven and less stable as a canonical reference; without clear depth/examples, it’s risky to include in a high-quality shelf.
- **LangGraph Subgraphs: A Guide to Modular AI Agents ...** — [LangGraph Subgraphs: A Guide to Modular AI Agents ...](https://dev.to/sreeni5018/langgraph-subgraphs-a-guide-to-modular-ai-agents-development-31ob)
  _Skipped because:_ Redundant with the official LangGraph subgraphs documentation and likely less precise/maintained.
- **Building Complex AI Workflows with LangGraph - DEV Community** — [Building Complex AI Workflows with LangGraph - DEV Community](https://dev.to/jamesli/building-complex-ai-workflows-with-langgraph-a-detailed-explanation-of-subgraph-architecture-1dj5)
  _Skipped because:_ Redundant with official docs and blog quality/maintenance is uncertain compared to LangChain’s documentation.

## Uncovered Gaps (3) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Supervisor (router/controller) agent pattern: definition, routing logic, maintaining small context, coordinating specialist agents, and concrete examples
- Agent delegation and handoffs: protocols for transferring task, state, and tool results; criteria for selecting delegate agents; examples using OpenAI Agents SDK
- Agents-as-tools pattern: how an agent is exposed/invoked like a tool, interface contracts (inputs/outputs), and tracing/debugging implications

## Reasoning
**Curator:** The strongest additions are authoritative, stable references that directly address missing practical architecture guidance: official LangGraph subgraph docs and Microsoft’s orchestration patterns. Most other candidates are vendor/personal blogs or redundant subgraph explainers that don’t reliably add depth beyond these two.
**Reviewer:** The curator’s additions are solid for LangGraph subgraphs and general orchestration patterns, but the library still needs at least the OpenAI Agents SDK handoffs references (and ideally OpenAI’s practical guide) to directly close the delegation/handoff and supervisor-style routing gaps with authoritative sources.

---

# Curation Report: Comparing Agentic Frameworks: LangGraph, AutoGen, CrewAI, and OpenAI Assistants
**Topic:** `agent-workflows` | **Date:** 2026-04-10 19:13
**Library:** 20 existing → 30 sources (10 added, 7 downloaded)
**Candidates evaluated:** 30
**Reviewer verdict:** needs_additions

## Added (10)
- **[reference_doc]** [Introduction - CrewAI Documentation](https://docs.crewai.com/en/introduction)
  Authoritative, stable docs that define CrewAI’s core primitives (agents/roles, crews, tasks, processes) and provide the canonical mental model needed to compare role-based coordination against LangGraph/AutoGen/Assistants.
   — covers: CrewAI fundamentals: roles, crews/teams, tasks, process models, and examples of role-based coordination, Comparative control-flow models across frameworks: explicit graphs (LangGraph) vs conversational multi-agent orchestration (AutoGen) vs role-based teams (CrewAI) vs managed tool-calling loops (Assistants/Agents)
- **[reference_doc]** [Tasks - CrewAI Documentation](https://docs.crewai.com/en/concepts/tasks)
  Goes deeper than an overview by detailing how tasks are specified, assigned, and executed within a crew, which is essential for understanding CrewAI’s process model and role/task coordination mechanics.
   — covers: CrewAI fundamentals: roles, crews/teams, tasks, process models, and examples of role-based coordination
- **[paper]** [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155)
  Seminal/primary source describing AutoGen’s abstractions (conversable agents, interaction patterns, tool/human modes) and the rationale behind conversation-driven orchestration—material not covered by the repo/docs alone.
   — covers: AutoGen core abstractions and mechanics: multi-agent conversation patterns, agent types, message routing/turn-taking, tool use, and human-in-the-loop collaboration examples, Comparative control-flow models across frameworks: explicit graphs (LangGraph) vs conversational multi-agent orchestration (AutoGen) vs role-based teams (CrewAI) vs managed tool-calling loops (Assistants/Agents)
- **[reference_doc]** [Assistants API deep dive - OpenAI API](https://platform.openai.com/docs/assistants/deep-dive)
  Directly addresses Assistants API lifecycle details (threads, runs, tool-calling loop, tool resources) needed for an accurate comparison with LangGraph/AutoGen/CrewAI beyond the Agents SDK handoffs pages already in the library.
   — covers: OpenAI Assistants API specifics (not just Agents SDK): threads/sessions, runs, tool-calling loop, persistence, guardrails, and lifecycle examples, Comparative control-flow models across frameworks: explicit graphs (LangGraph) vs conversational multi-agent orchestration (AutoGen) vs role-based teams (CrewAI) vs managed tool-calling loops (Assistants/Agents)
- **[reference_doc]** [Durable execution - Docs by LangChain (LangGraph)](https://docs.langchain.com/oss/python/langgraph/durable-execution)
  This is the canonical, framework-authoritative documentation for checkpointing/replay/resume semantics in LangGraph and directly addresses the stated durability gap with concrete mechanics and examples.
   — covers: Durable execution in LangGraph: checkpointing, state persistence, replay/resume semantics, failure recovery, and concrete usage examples
- **[reference_doc]** [Memory store (Persistence) - Docs by LangChain (LangGraph)](https://docs.langchain.com/oss/python/langgraph/persistence)
  Pairs with Durable Execution by specifying the persistence layer (memory store/checkpointers) needed to make durability real in deployments; it’s primary-source documentation rather than a blog interpretation.
   — covers: Durable execution in LangGraph: checkpointing, state persistence, replay/resume semantics, failure recovery, and concrete usage examples
- **[tutorial]** [Build durable AI agents with LangGraph and Amazon DynamoDB - AWS Database Blog](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)
  While not as canonical as LangChain docs, it’s a high-authority institutional walkthrough showing an end-to-end durable execution setup (real persistence backend, operational considerations) that students often need to see once.
   — covers: Durable execution in LangGraph: checkpointing, state persistence, replay/resume semantics, failure recovery, and concrete usage examples
- **[reference_doc]** [Durable execution - Docs by LangChain (LangGraph)](https://docs.langchain.com/oss/python/langgraph/durable-execution) *(promoted by reviewer)*
  This is the canonical, framework-authoritative documentation for checkpointing/replay/resume semantics in LangGraph and directly addresses the stated durability gap with concrete mechanics and examples.
   — fills: Durable execution in LangGraph: checkpointing, state persistence, replay/resume semantics, failure recovery, and concrete usage examples
- **[reference_doc]** [Memory store (Persistence) - Docs by LangChain (LangGraph)](https://docs.langchain.com/oss/python/langgraph/persistence) *(promoted by reviewer)*
  Pairs with Durable Execution by specifying the persistence layer (memory store/checkpointers) needed to make durability real in deployments; it’s primary-source documentation rather than a blog interpretation.
   — fills: Durable execution in LangGraph: checkpointing, state persistence, replay/resume semantics, failure recovery, and concrete usage examples
- **[tutorial]** [Build durable AI agents with LangGraph and Amazon DynamoDB - AWS Database Blog](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/) *(promoted by reviewer)*
  While not as canonical as LangChain docs, it’s a high-authority institutional walkthrough showing an end-to-end durable execution setup (real persistence backend, operational considerations) that students often need to see once.
   — fills: Durable execution in LangGraph: checkpointing, state persistence, replay/resume semantics, failure recovery, and concrete usage examples

## Near-Misses (11) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **CrewAI: A Practical Guide to Role-Based Agent Orchestration** — [CrewAI: A Practical Guide to Role-Based Agent Orchestration](https://www.digitalocean.com/community/tutorials/crewai-crash-course-role-based-agent-orchestration)
  _Skipped because:_ Potentially useful, but it’s a third-party tutorial (and dated 2026) that is less authoritative than the official CrewAI docs for a curated “best sources” shelf.
- **Implementation approach for...** — [Implementation approach for...](https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-frameworks/crewai.html)
  _Skipped because:_ Likely higher-level prescriptive guidance and may be thin on concrete CrewAI mechanics compared to CrewAI’s own concept docs.
- **Assistants API - OpenAI Platform** — [Assistants API - OpenAI Platform](https://platform.openai.com/docs/assistants)
  _Skipped because:_ Good reference, but the Deep Dive is the more substantive single pick for lifecycle/tool-loop specifics; adding both would be redundant.
- **Azure OpenAI Assistants API (Preview) (classic) - Microsoft ** — [Azure OpenAI Assistants API (Preview) (classic) - Microsoft Learn](https://learn.microsoft.com/en-us/azure/foundry-classic/openai/concepts/assistants)
  _Skipped because:_ Useful for Azure-specific deployment, but it’s a parallel surface area and can diverge from OpenAI’s canonical API details; not essential for the core comparison lesson.
- **OpenAI Assistants API: Production Patterns and Best Practice** — [OpenAI Assistants API: Production Patterns and Best Practices](https://michaeljohnpena.com/blog/2024-01-03-assistants-api-patterns/)
  _Skipped because:_ Could add practical patterns, but it’s a personal blog and overlaps with the official Deep Dive; for a small high-quality library, the official doc is the safer inclusion.
- **Agent Skills: OpenAI Assistants API v2** — [Agent Skills: OpenAI Assistants API v2](https://agent-skills.md/skills/ovachiever/droid-tings/openai-assistants)
  _Skipped because:_ Not clearly an authoritative or stable primary source compared to OpenAI’s own documentation.
- **Notes 1 | PDF | Artificial Intelligence - Scribd** — [Notes 1 | PDF | Artificial Intelligence - Scribd](https://www.scribd.com/document/948620521/Notes1)
  _Skipped because:_ Unclear provenance and stability; not appropriate for a curated, high-trust teaching wiki.
- **arXiv:2308.08155v2 [cs.AI] 3 Oct 2023** — [arXiv:2308.08155v2 [cs.AI] 3 Oct 2023](https://arxiv.org/pdf/2308.08155/v1.pdf)
  _Skipped because:_ Redundant with the arXiv abstract page; the abs URL is sufficient and more stable for citation.
- **[PDF] AUTOGEN: ENABLING NEXT-GEN LLM APPLICATIONS VIA MULTI ** — [[PDF] AUTOGEN: ENABLING NEXT-GEN LLM APPLICATIONS VIA MULTI ...](http://ryenwhite.com/papers/WuLLMAgents2024.pdf)
  _Skipped because:_ Third-party hosted PDF of the same AutoGen paper; prefer the canonical arXiv entry.
- **Published as a conference paper at COLM 2024** — [Published as a conference paper at COLM 2024](https://www.microsoft.com/en-us/research/uploads/prodnew/2023/08/LLM_agent.pdf)
  _Skipped because:_ Likely another copy/version of the AutoGen paper; redundant once the canonical arXiv source is included.
- **[PDF] Implementation, Insights, and Prospects in Multi-Agent** — [[PDF] Implementation, Insights, and Prospects in Multi-Agent Systems](https://juekong-research.com/data/publications/Autogen.pdf)
  _Skipped because:_ Non-canonical hosting and unclear versioning relative to the primary AutoGen publication.

## Uncovered Gaps (2) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Durable execution in LangGraph: checkpointing, state persistence, replay/resume semantics, failure recovery, and concrete usage examples
- Human-in-the-loop in LangGraph (and others): interrupts, approvals, review steps, and implementation patterns

## Reasoning
**Curator:** Add only canonical, high-signal sources that directly fill the missing framework-specific mechanics: official CrewAI docs, the seminal AutoGen paper, and OpenAI’s Assistants deep dive. Other candidates are redundant copies, less authoritative tutorials, or off-scope/unstable sources.
**Reviewer:** The curator’s core picks are strong for conceptual comparison, but they missed the most direct, authoritative LangGraph sources that close the stated durability/persistence gap (and an institutional implementation example).
