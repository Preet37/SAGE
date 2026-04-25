# Curation Report: Multi-Agent Systems
**Topic:** `multi-agent-systems` | **Date:** 2026-04-09 16:23
**Library:** 5 existing → 18 sources (13 added, 8 downloaded)
**Candidates evaluated:** 40
**Reviewer verdict:** needs_additions

## Added (13)
- **[explainer]** [Blackboard Architectures](https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf)
  Provides a classic, non-LLM multi-agent coordination pattern with explicit components and control rationale that can be mapped to modern agent orchestrators (shared state + specialized agents + scheduler).
- **[reference_doc]** [Last_speaker​](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/)
  Gives citable, precise API defaults and state/message handling rules needed to answer student questions about orchestration behavior and reproducibility.
- **[benchmark]** [[2308.03688] AgentBench: Evaluating LLMs as Agents - arXiv](https://arxiv.org/abs/2308.03688)
  Adds standardized evaluation protocols and quantitative results that can ground discussions of agent capability limits and what types of tasks degrade performance.
- **[explainer]** [CMU 15-281 Lecture 26: Multi-Agent Reinforcement Learning / Markov Games (Michael L. Littman)](https://www.cs.cmu.edu/~./15281-f19/lectures/15281_Fa19_Lecture_26_MARL.pdf)
  Even as slides, this is a compact, teachable source with the core equations and assumptions (observability, stationarity, equilibrium concepts) that the current library lacks.
- **[paper]** [Scalable Solution Methods for Dec-POMDPs with ...](https://arxiv.org/html/2508.21595v1)
  The unfilled need explicitly calls for Dec-POMDP formulations and solution methods; this paper is likely to provide both the math and algorithmic pipeline details beyond what LLM-agent blogs cover.
- **[paper]** [Expert Systems With Applications (1994): Blackboard systems architecture analysis (Stanford KSL)](https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf)
  If the curator is adding a blackboard explainer, this primary-source paper is more citable/authoritative and provides deeper design rationale than a secondary summary.
- **[paper]** [HLER: Human-in-the-Loop Economic Research via Multi-Agent ...](https://arxiv.org/html/2603.07444v1)
  This directly targets the missing deployment-case need: real-world architecture/process learnings with numbers and failure-handling policies, which are rare in agent papers.
- **[benchmark]** [Benchmarking Multi-Agent LLM Architectures for ...](https://arxiv.org/pdf/2603.22651.pdf)
  Even if framed as benchmarking, it can supply the “specific numbers” and architecture comparisons needed to teach design tradeoffs (coordination topology, message-passing, controller choices).
- **[explainer]** [CMU 15-281 Lecture 26: Multi-Agent Reinforcement Learning / Markov Games (Michael L. Littman)](https://www.cs.cmu.edu/~./15281-f19/lectures/15281_Fa19_Lecture_26_MARL.pdf) *(promoted by reviewer)*
  Even as slides, this is a compact, teachable source with the core equations and assumptions (observability, stationarity, equilibrium concepts) that the current library lacks.
- **[paper]** [Scalable Solution Methods for Dec-POMDPs with ...](https://arxiv.org/html/2508.21595v1) *(promoted by reviewer)*
  The unfilled need explicitly calls for Dec-POMDP formulations and solution methods; this paper is likely to provide both the math and algorithmic pipeline details beyond what LLM-agent blogs cover.
- **[paper]** [Expert Systems With Applications (1994): Blackboard systems architecture analysis (Stanford KSL)](https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf) *(promoted by reviewer)*
  If the curator is adding a blackboard explainer, this primary-source paper is more citable/authoritative and provides deeper design rationale than a secondary summary.
- **[paper]** [HLER: Human-in-the-Loop Economic Research via Multi-Agent ...](https://arxiv.org/html/2603.07444v1) *(promoted by reviewer)*
  This directly targets the missing deployment-case need: real-world architecture/process learnings with numbers and failure-handling policies, which are rare in agent papers.
- **[benchmark]** [Benchmarking Multi-Agent LLM Architectures for ...](https://arxiv.org/pdf/2603.22651.pdf) *(promoted by reviewer)*
  Even if framed as benchmarking, it can supply the “specific numbers” and architecture comparisons needed to teach design tradeoffs (coordination topology, message-passing, controller choices).

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **autogen_agentchat.teams — AutoGen - Microsoft Open Source** — [autogen_agentchat.teams — AutoGen - Microsoft Open Source](https://microsoft.github.io/autogen/stable/reference/python/autogen_agentchat.teams.html)
  _Skipped because:_ Likely broader and useful, but the provided candidate snippet repeats GroupChat details; the GroupChat reference page is the most directly citable for defaults and message-flow semantics.
- **FSM Group Chat -- User-specified agent transitions** — [FSM Group Chat -- User-specified agent transitions](https://microsoft.github.io/autogen/0.2/blog/2024/02/11/FSM-GroupChat/)
  _Skipped because:_ Good design pattern write-up, but less of a definitive API-default/spec reference than the formal GroupChat reference page.
- **Optimizing Latency and Cost in Multi-Agent Systems - HockeyS** — [Optimizing Latency and Cost in Multi-Agent Systems - HockeyStack](https://www.hockeystack.com/applied-ai/optimizing-latency-and-cost-in-multi-agent-systems)
  _Skipped because:_ Potentially valuable operational lessons, but it is a vendor blog and not as authoritative/citable as peer-reviewed or official engineering case studies with verifiable metrics.

## Reasoning
**Curator:** Selections prioritize (1) authoritative classic coordination architecture with explicit control/message-flow (blackboard), (2) official API docs with concrete defaults/semantics (AutoGen GroupChat), and (3) a standardized benchmark with quantitative results (AgentBench). Other needs lacked suitable candidates in the provided list.
**Reviewer:** The current library is strong on modern LLM-agent frameworks and one benchmark, but it still needs at least one formal multi-agent decision-making formulation source and at least one production-style case study with concrete metrics and operational policies.

---

# Curation Report: LangGraph Core Concepts: State, Nodes, and Edges
**Topic:** `multi-agent-systems` | **Date:** 2026-04-10 19:23
**Library:** 16 existing → 38 sources (22 added, 13 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (22)
- **[reference_doc]** [compile | langgraph - LangChain Reference Docs](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)
  This is the most authoritative, versioned surface for core runtime semantics the tutor will be asked about (what compile produces, what knobs exist, and how execution is exposed via Runnable methods).
- **[explainer]** [Reducers for other state members apart from messages #3459](https://github.com/langchain-ai/langgraph/discussions/3459)
  Directly targets reducer/merge mechanics (a core StateGraph concept) and provides authoritative navigation to the exact conceptual docs the tutor needs for explaining how partial updates are aggregated.
- **[code]** [langgraph/libs/langgraph/langgraph/graph/message.py at main · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/graph/message.py)
  Gives runnable, inspectable ground truth for how state updates are merged in practice—ideal for step-by-step tutoring and for answering precise questions about message accumulation behavior.
- **[benchmark]** [LangGraph in Production: Latency, Replay, and Scale | Aerospike](https://aerospike.com/blog/langgraph-production-latency-replay-scale)
  Adds production-oriented considerations (latency metrics, replay, resilience) that help the tutor teach why persistence/replay and execution semantics matter beyond toy examples.
- **[reference_doc]** [streamMode | @langchain/langgraph (CompiledStateGraph.streamMode)](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/streamMode)
  The current library lacks a crisp, citable definition of streaming modes; even if JS-focused, this page often lists the canonical mode names/behavior more explicitly than narrative docs and directly fills the streaming-semantics gap.
- **[reference_doc]** [CompiledStateGraph | @langchain/langgraph (JavaScript reference)](https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)
  It was rejected as overlapping, but it can provide additional, highly specific API surface details (especially around streaming/event APIs) that help answer precise tutor questions about execution interfaces.
- **[explainer]** [Problem with add_messages, message didn't get merged (langgraph issue #1568)](https://github.com/langchain-ai/langgraph/issues/1568)
  This is a high-signal edge case that reveals actual reducer/merge semantics in practice; it’s valuable for teaching what partial updates mean and how merges behave under concurrency.
- **[explainer]** [Cannot get messages merged after two parallel nodes (langgraph discussion #3914)](https://github.com/langchain-ai/langgraph/discussions/3914)
  The unfilled needs explicitly call out merge order and determinism; this discussion typically contains the most actionable, real-world explanation of how merges work when multiple nodes write the same key.
- **[explainer]** [Replace message history atomically (langgraph discussion #3810)](https://github.com/langchain-ai/langgraph/discussions/3810)
  This fills a common conceptual gap: distinguishing reducer-based accumulation from intentional replacement, which is central to teaching correct state design and replay-safe behavior.
- **[explainer]** [langgraph/how-tos/human_in_the_loop/edit-graph-state (discussion #938)](https://github.com/langchain-ai/langgraph/discussions/938)
  The library has HITL overviews, but not the precise semantics of state mutation/editing; this is exactly the kind of operational detail tutors get asked about.
- **[explainer]** [Dynamic Workflow Mode Implementation for Conditional Edges (langgraph discussion #3346)](https://github.com/langchain-ai/langgraph/discussions/3346)
  Conditional routing is core to nodes/edges, and this discussion can provide the missing 'how it really works' narrative beyond basic tutorials—especially around dynamic workflows.
- **[code]** [feature: Dynamic Workflow Mode Implementation for Conditional Edges (PR #3345)](https://github.com/langchain-ai/langgraph/pull/3345)
  PRs are often the most authoritative source for runtime semantics when docs lag; this directly supports teaching the execution model for conditional edges with concrete code.
- **[reference_doc]** [图定义 / Graphs reference (LangGraphCN) — StateGraph signature and reducers](https://www.langgraphcn.org/reference/graphs/)
  Even if unofficial/translated, it concisely states core semantics (partial updates + reducers) in a reference style; it can serve as a quick citation when the main docs are scattered.
- **[reference_doc]** [streamMode | @langchain/langgraph (CompiledStateGraph.streamMode)](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/streamMode) *(promoted by reviewer)*
  The current library lacks a crisp, citable definition of streaming modes; even if JS-focused, this page often lists the canonical mode names/behavior more explicitly than narrative docs and directly fills the streaming-semantics gap.
- **[reference_doc]** [CompiledStateGraph | @langchain/langgraph (JavaScript reference)](https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html) *(promoted by reviewer)*
  It was rejected as overlapping, but it can provide additional, highly specific API surface details (especially around streaming/event APIs) that help answer precise tutor questions about execution interfaces.
- **[explainer]** [Problem with add_messages, message didn't get merged (langgraph issue #1568)](https://github.com/langchain-ai/langgraph/issues/1568) *(promoted by reviewer)*
  This is a high-signal edge case that reveals actual reducer/merge semantics in practice; it’s valuable for teaching what partial updates mean and how merges behave under concurrency.
- **[explainer]** [Cannot get messages merged after two parallel nodes (langgraph discussion #3914)](https://github.com/langchain-ai/langgraph/discussions/3914) *(promoted by reviewer)*
  The unfilled needs explicitly call out merge order and determinism; this discussion typically contains the most actionable, real-world explanation of how merges work when multiple nodes write the same key.
- **[explainer]** [Replace message history atomically (langgraph discussion #3810)](https://github.com/langchain-ai/langgraph/discussions/3810) *(promoted by reviewer)*
  This fills a common conceptual gap: distinguishing reducer-based accumulation from intentional replacement, which is central to teaching correct state design and replay-safe behavior.
- **[explainer]** [langgraph/how-tos/human_in_the_loop/edit-graph-state (discussion #938)](https://github.com/langchain-ai/langgraph/discussions/938) *(promoted by reviewer)*
  The library has HITL overviews, but not the precise semantics of state mutation/editing; this is exactly the kind of operational detail tutors get asked about.
- **[explainer]** [Dynamic Workflow Mode Implementation for Conditional Edges (langgraph discussion #3346)](https://github.com/langchain-ai/langgraph/discussions/3346) *(promoted by reviewer)*
  Conditional routing is core to nodes/edges, and this discussion can provide the missing 'how it really works' narrative beyond basic tutorials—especially around dynamic workflows.
- **[code]** [feature: Dynamic Workflow Mode Implementation for Conditional Edges (PR #3345)](https://github.com/langchain-ai/langgraph/pull/3345) *(promoted by reviewer)*
  PRs are often the most authoritative source for runtime semantics when docs lag; this directly supports teaching the execution model for conditional edges with concrete code.
- **[reference_doc]** [图定义 / Graphs reference (LangGraphCN) — StateGraph signature and reducers](https://www.langgraphcn.org/reference/graphs/) *(promoted by reviewer)*
  Even if unofficial/translated, it concisely states core semantics (partial updates + reducers) in a reference style; it can serve as a quick citation when the main docs are scattered.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Making it easier to build human-in-the-loop agents with inte** — [Making it easier to build human-in-the-loop agents with interrupt](https://blog.langchain.dev/making-it-easier-to-build-human-in-the-loop-agents-with-interrupt/)
  _Skipped because:_ Strong design rationale for interrupts/HITL, but the existing library already includes official Interrupts and Human-in-the-loop docs, so this would be partially redundant versus filling other gaps.
- **CompiledStateGraph | @langchain/langgraph** — [CompiledStateGraph | @langchain/langgraph](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph)
  _Skipped because:_ Useful for JS users, but overlaps heavily with the Python `compile()` reference and doesn’t add as much unique, core-semantic detail as the Python reference page.

## Reasoning
**Curator:** Selections prioritize authoritative, directly citable material for core semantics (official API reference + source code for reducers) and add one production-oriented case study; generic third-party comparisons were excluded because they rarely provide precise, verifiable semantics or tables aligned to the requested criteria.
**Reviewer:** The curator’s additions are strong, but several high-signal reference/issue/PR sources should be included because they uniquely pin down streaming modes, parallel-merge semantics, and conditional-edge execution details that the current library still lacks.

---

# Curation Report: Why LangGraph? Graphs as Agent Control Flow
**Topic:** `multi-agent-systems` | **Date:** 2026-04-10 19:26
**Library:** 16 existing → 32 sources (16 added, 8 downloaded)
**Candidates evaluated:** 43
**Reviewer verdict:** needs_additions

## Added (16)
- **[explainer]** [LangGraph v0.2: Increased customization with new checkpointer ...](https://blog.langchain.com/langgraph-v0-2/)
  This is an official maintainer-authored design narrative that explains why LangGraph emphasizes stateful graphs with checkpointing and resumability, giving the tutor quotable rationale beyond tutorials.
- **[reference_doc]** [compile | langgraph - LangChain Reference Docs](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)
  The versioned reference docs are the most authoritative place to cite exact API semantics and defaults for compilation/execution, which students often ask about when debugging control flow.
- **[reference_doc]** [Checkpointing | LangChain Reference](https://reference.langchain.com/python/langgraph/checkpoints/)
  Checkpointing is central to LangGraph’s durability story; this reference provides the concrete types and semantics needed for precise answers about persistence, replay, and operational behavior.
- **[explainer]** [Getting Started](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)
  An AWS blog is a relatively authoritative deployment-oriented walkthrough that concretely ties LangGraph durability concepts to real infrastructure choices and operational steps.
- **[reference_doc]** [Types | LangChain Reference (LangGraph)](https://reference.langchain.com/python/langgraph/types/)
  It may look “thin,” but it’s exactly the kind of authoritative, versioned reference students need when debugging control-flow and resumability edge cases (what is raised/returned, what is serializable, etc.).
- **[reference_doc]** [entrypoint | langgraph (Functional API)](https://reference.langchain.com/python/langgraph/func/entrypoint)
  Even if the lesson emphasizes graphs as control flow, learners will ask how functional graphs map onto compiled execution; this page provides precise API semantics that tutorials often omit.
- **[benchmark]** [LangGraph in Production: Latency, Replay, and Scale | Aerospike](https://aerospike.com/blog/langgraph-production-latency-replay-scale)
  The library is currently light on quantitative evidence; if this post includes even a small set of measured latencies or replay costs, it directly supports the unfilled empirical need.
- **[benchmark]** [Performance Benchmarks - MCP Server with LangGraph](https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks)
  Even third-party benchmarks are valuable when they provide explicit numbers and methodology; this is one of the few candidates that plausibly contains a structured benchmark section.
- **[explainer]** [Persistence (concepts) | langchain-ai/langgraph (repo docs)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/persistence.md)
  This is primary-source documentation from the project itself and often contains operational details and invariants that don’t appear in the higher-level OSS docs pages.
- **[explainer]** [State Update After Interrupt Not Reaching Subgraph Node on Resume (LangGraph Discussion #4730)](https://github.com/langchain-ai/langgraph/discussions/4730)
  For teaching “graphs as agent control flow,” real failure modes around interrupts/resume are high-value; this thread provides a precise, reproducible scenario and maintainer clarification that students commonly hit.
- **[reference_doc]** [Types | LangChain Reference (LangGraph)](https://reference.langchain.com/python/langgraph/types/) *(promoted by reviewer)*
  It may look “thin,” but it’s exactly the kind of authoritative, versioned reference students need when debugging control-flow and resumability edge cases (what is raised/returned, what is serializable, etc.).
- **[reference_doc]** [entrypoint | langgraph (Functional API)](https://reference.langchain.com/python/langgraph/func/entrypoint) *(promoted by reviewer)*
  Even if the lesson emphasizes graphs as control flow, learners will ask how functional graphs map onto compiled execution; this page provides precise API semantics that tutorials often omit.
- **[benchmark]** [LangGraph in Production: Latency, Replay, and Scale | Aerospike](https://aerospike.com/blog/langgraph-production-latency-replay-scale) *(promoted by reviewer)*
  The library is currently light on quantitative evidence; if this post includes even a small set of measured latencies or replay costs, it directly supports the unfilled empirical need.
- **[benchmark]** [Performance Benchmarks - MCP Server with LangGraph](https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks) *(promoted by reviewer)*
  Even third-party benchmarks are valuable when they provide explicit numbers and methodology; this is one of the few candidates that plausibly contains a structured benchmark section.
- **[explainer]** [Persistence (concepts) | langchain-ai/langgraph (repo docs)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/persistence.md) *(promoted by reviewer)*
  This is primary-source documentation from the project itself and often contains operational details and invariants that don’t appear in the higher-level OSS docs pages.
- **[explainer]** [State Update After Interrupt Not Reaching Subgraph Node on Resume (LangGraph Discussion #4730)](https://github.com/langchain-ai/langgraph/discussions/4730) *(promoted by reviewer)*
  For teaching “graphs as agent control flow,” real failure modes around interrupts/resume are high-value; this thread provides a precise, reproducible scenario and maintainer clarification that students commonly hit.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Introducing the LangGraph Functional API - LangChain Blog** — [Introducing the LangGraph Functional API - LangChain Blog](https://blog.langchain.com/introducing-the-langgraph-functional-api/)
  _Skipped because:_ Useful for teaching the functional API style, but less directly focused on the core design rationale for graphs/state/cycles/interrupts than the v0.2 architecture/checkpointer discussion.
- **interrupt | langgraph** — [interrupt | langgraph](https://reference.langchain.com/python/langgraph/types/interrupt)
  _Skipped because:_ Strong for interrupt semantics, but the library already includes multiple interrupt/HITL docs; the compile + checkpointing references cover broader API defaults and execution semantics.
- **Checkpointing Architecture | langchain-ai/langgraph | DeepWi** — [Checkpointing Architecture | langchain-ai/langgraph | DeepWiki](https://deepwiki.com/langchain-ai/langgraph/4.1-checkpointing-architecture)
  _Skipped because:_ Potentially detailed, but it’s a third-party synthesized documentation layer rather than primary/official docs, so it’s less citable for exact semantics.
- **LangGraph vs AutoGen: How are These LLM Workflow ... - ZenML** — [LangGraph vs AutoGen: How are These LLM Workflow ... - ZenML](https://www.zenml.io/blog/langgraph-vs-autogen)
  _Skipped because:_ Provides a comparison narrative, but it’s not a rigorous feature-by-feature matrix with concrete criteria and measurable claims suitable as an authoritative comparison reference.

## Reasoning
**Curator:** Selections prioritize primary/official sources that add missing design rationale and precise, versioned API semantics (compile + checkpointing), plus one credible deployment-oriented walkthrough. Empirical and rigorous comparison needs remain unfilled because the provided candidates are mostly blog-level and not benchmark-grade.
**Reviewer:** The core LangGraph docs coverage is strong, but adding a few thin-but-authoritative reference pages plus any sources with explicit benchmark numbers and primary-source persistence semantics would materially improve depth and precision for this lesson.

---

# Curation Report: Persistence, Checkpointing, and Human-in-the-Loop
**Topic:** `multi-agent-systems` | **Date:** 2026-04-10 19:32
**Library:** 16 existing → 29 sources (13 added, 7 downloaded)
**Candidates evaluated:** 44
**Reviewer verdict:** needs_additions

## Added (13)
- **[reference_doc]** [Checkpointing | LangChain Reference](https://reference.langchain.com/python/langgraph/checkpoints/)
  This is the most authoritative, versioned place to quote exact interfaces, typed fields, and semantics needed for precise answers about LangGraph checkpoint objects and saver behavior.
- **[explainer]** [langgraph/docs/docs/concepts/functional_api.md at main · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/functional_api.md)
  Among the candidates, this is the closest to an authoritative, step-by-step conceptual description from the core repo that can be tied back to durable execution and interrupts mechanics.
- **[reference_doc]** [Architecture](https://docs.temporal.io/ai-cookbook/human-in-the-loop-python)
  Provides a crisp, structured reference implementation of HITL in a durable workflow engine, enabling direct comparison criteria (signals, waiting semantics, replay/durability expectations) against LangGraph.
- **[explainer]** [Part 2: Adding Durable Human-in-the-Loop to Our Research ...](https://learn.temporal.io/tutorials/ai/building-durable-ai-applications/human-in-the-loop/)
  Complements the cookbook with more pedagogical sequencing and rationale, helping the tutor explain design tradeoffs (determinism, replay, external side effects) across systems.
- **[code]** [GitHub - gotohuman/gotohuman-langgraph-lead-example](https://github.com/gotohuman/gotohuman-langgraph-lead-example)
  This is the most production-like code candidate: it shows how to wire a human approval loop into a LangGraph-driven process in a way that can be adapted to a durable backend and crash recovery demos.
- **[reference_doc]** [Persistence (LangGraph concepts doc in core repo)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/persistence.md)
  This is an authoritative, repo-adjacent spec-like description of persistence semantics that complements the versioned API reference with the missing conceptual contract (super-step granularity, threads as storage unit).
- **[reference_doc]** [checkpointer | @langchain/langgraph (JavaScript reference)](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer)
  Even if the library is Python-heavy, thin JS API docs are still high-value for answering interface-precision questions and for clarifying semantics when Python docs lag or differ.
- **[reference_doc]** [BaseCheckpointSaver.list | @langchain/langgraph-checkpoint (JavaScript reference)](https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list)
  The lesson is about persistence/checkpointing; retrieval APIs (list/get) are exactly where tutors need parameter-level precision, and this page is the canonical place to quote it.
- **[explainer]** [Temporal for Human-in-the-Loop: When You Don't Know How Long ...](https://danielfridljand.de/post/temporal-human-in-the-loop)
  While third-party, it is narrowly focused on the exact durability/HITL mechanics the lesson compares against; it adds a crisp end-to-end pattern that helps teach tradeoffs around long waits and recovery.
- **[reference_doc]** [Persistence (LangGraph concepts doc in core repo)](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/persistence.md) *(promoted by reviewer)*
  This is an authoritative, repo-adjacent spec-like description of persistence semantics that complements the versioned API reference with the missing conceptual contract (super-step granularity, threads as storage unit).
- **[reference_doc]** [checkpointer | @langchain/langgraph (JavaScript reference)](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer) *(promoted by reviewer)*
  Even if the library is Python-heavy, thin JS API docs are still high-value for answering interface-precision questions and for clarifying semantics when Python docs lag or differ.
- **[reference_doc]** [BaseCheckpointSaver.list | @langchain/langgraph-checkpoint (JavaScript reference)](https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list) *(promoted by reviewer)*
  The lesson is about persistence/checkpointing; retrieval APIs (list/get) are exactly where tutors need parameter-level precision, and this page is the canonical place to quote it.
- **[explainer]** [Temporal for Human-in-the-Loop: When You Don't Know How Long ...](https://danielfridljand.de/post/temporal-human-in-the-loop) *(promoted by reviewer)*
  While third-party, it is narrowly focused on the exact durability/HITL mechanics the lesson compares against; it adds a crisp end-to-end pattern that helps teach tradeoffs around long waits and recovery.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Checkpointer | langgraph - LangChain Reference Docs** — [Checkpointer | langgraph - LangChain Reference Docs](https://reference.langchain.com/python/langgraph/types/Checkpointer)
  _Skipped because:_ Overlaps heavily with the broader checkpointing reference page; kept the more comprehensive checkpointing entry as the single Python anchor.
- **getNextVersion** — [getNextVersion](https://reference.langchain.com/javascript/classes/_langchain_langgraph-checkpoint.BaseCheckpointSaver.html)
  _Skipped because:_ Useful for JS-specific API precision, but the library already skews Python-heavy and the Python checkpointing reference is the higher-leverage single pick.
- **Feature: handling concurrent interrupts #3895** — [Feature: handling concurrent interrupts #3895](https://github.com/langchain-ai/langgraph/discussions/3895)
  _Skipped because:_ Good real-world discussion of concurrency/interrupt UX, but it is not a stable, authoritative spec for semantics like locking/idempotency guarantees.
- **Beyond input(): Building Production-Ready Human-in-the-Loop ** — [Beyond input(): Building Production-Ready Human-in-the-Loop AI ...](https://dev.to/sreeni5018/beyond-input-building-production-ready-human-in-the-loop-ai-with-langgraph-2en9)
  _Skipped because:_ Potentially practical, but it is a third-party blog (less authoritative) and may not provide the concrete durability/metrics/architecture rigor required for a deployment case.

## Reasoning
**Curator:** Selections prioritize authoritative, versioned API references for precision (LangChain reference docs), and durable HITL workflow tutorials from Temporal for cross-system comparison and concrete mechanics; only one code example met the bar for an end-to-end, integration-oriented HITL flow.
**Reviewer:** The curator’s core picks are strong, but the library is missing a couple of high-leverage official persistence/checkpointer reference pages (especially retrieval/listing) and one focused HITL durability comparison source that directly supports the unfilled deployment/comparison needs.
