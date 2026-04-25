# Curation Report: Agent Workflows and Patterns
**Topic:** `agent-workflows` | **Date:** 2026-04-09 18:39
**Library:** 7 existing → 21 sources (14 added, 8 downloaded)
**Candidates evaluated:** 44
**Reviewer verdict:** needs_additions

## Added (14)
- **[reference_doc]** [Op retries - Dagster Docs](https://docs.dagster.io/guides/build/ops/op-retries)
  Gives concrete, citable API-level knobs for retries/backoff at the workflow primitive level (ops), which maps cleanly to agent tool-call steps and failure handling.
- **[explainer]** [Event History walkthrough with the Go SDK - Temporal Docs](https://docs.temporal.io/encyclopedia/event-history/event-history-go)
  Provides an authoritative, mechanistic explanation of durable orchestration (event sourcing + determinism + replay) that underpins why agent workflows are modeled as state machines and how retries/failures behave.
- **[reference_doc]** [Executing jobs - Dagster Docs](https://docs.dagster.io/guides/build/jobs/job-execution)
  The library currently has retries but lacks the equally core execution/concurrency controls that govern fan-out/fan-in behavior and throughput; thin API docs here are exactly what a reference track needs.
- **[reference_doc]** [Run retries - Dagster deployment settings reference](https://docs.dagster.io/deployment/dagster-plus/deploying-code/full-deployments/full-deployment-settings-reference)
  The curator added op retries, but production agent workflows often need run/job-level retry semantics too; this page provides concrete configuration surface area and defaults/behavior.
- **[paper]** [Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://arxiv.org/html/2510.04371v1)
  Speculative execution is explicitly called out in the unfilled needs; this is a direct workflow-pattern paper (not just narrative) that can ground a tutor’s explanation with a concrete method and measured impact.
- **[paper]** [Reducing Latency of LLM Search Agent via Speculation ...](https://arxiv.org/html/2511.20048v1)
  Even a single table/figure with latency numbers for a real agent loop materially improves the library’s ability to teach latency/cost trade-offs across workflow patterns.
- **[explainer]** [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/html/2507.21504v1)
  The lesson needs empirical framing (what to measure and how) before any benchmark numbers are interpretable; a survey can supply the canonical metric vocabulary and experimental design guidance missing from the current library.
- **[paper]** [ESAA: Event Sourcing for Autonomous Agents in LLM-Based ...](https://arxiv.org/html/2602.23193v1)
  You already added Temporal’s replay model; this paper extends the same durability/replay idea specifically to LLM agents, giving a teachable bridge from workflow engines to agent memory/state patterns.
- **[reference_doc]** [Executing jobs - Dagster Docs](https://docs.dagster.io/guides/build/jobs/job-execution) *(promoted by reviewer)*
  The library currently has retries but lacks the equally core execution/concurrency controls that govern fan-out/fan-in behavior and throughput; thin API docs here are exactly what a reference track needs.
- **[reference_doc]** [Run retries - Dagster deployment settings reference](https://docs.dagster.io/deployment/dagster-plus/deploying-code/full-deployments/full-deployment-settings-reference) *(promoted by reviewer)*
  The curator added op retries, but production agent workflows often need run/job-level retry semantics too; this page provides concrete configuration surface area and defaults/behavior.
- **[paper]** [Speculative Actions: A Lossless Framework for Faster Agentic Systems](https://arxiv.org/html/2510.04371v1) *(promoted by reviewer)*
  Speculative execution is explicitly called out in the unfilled needs; this is a direct workflow-pattern paper (not just narrative) that can ground a tutor’s explanation with a concrete method and measured impact.
- **[paper]** [Reducing Latency of LLM Search Agent via Speculation ...](https://arxiv.org/html/2511.20048v1) *(promoted by reviewer)*
  Even a single table/figure with latency numbers for a real agent loop materially improves the library’s ability to teach latency/cost trade-offs across workflow patterns.
- **[explainer]** [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/html/2507.21504v1) *(promoted by reviewer)*
  The lesson needs empirical framing (what to measure and how) before any benchmark numbers are interpretable; a survey can supply the canonical metric vocabulary and experimental design guidance missing from the current library.
- **[paper]** [ESAA: Event Sourcing for Autonomous Agents in LLM-Based ...](https://arxiv.org/html/2602.23193v1) *(promoted by reviewer)*
  You already added Temporal’s replay model; this paper extends the same durability/replay idea specifically to LLM agents, giving a teachable bridge from workflow engines to agent memory/state patterns.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Run executor limits - Dagster Docs** — [Run executor limits - Dagster Docs](https://docs.dagster.io/guides/operate/managing-concurrency/run-executor-limits)
  _Skipped because:_ Strong for concurrency defaults (e.g., multiprocess executor using cpu_count), but the selected Dagster retries page better covers failure semantics; adding both would crowd out other unmet needs.
- **Temporal vs Airflow: Which Orchestrator Fits Your Workflows?** — [Temporal vs Airflow: Which Orchestrator Fits Your Workflows? - ZenML](https://www.zenml.io/blog/temporal-vs-airflow)
  _Skipped because:_ Useful narrative comparison, but it is third-party and typically less rigorous/complete than a structured, criteria-driven matrix spanning Temporal/Airflow/Prefect/Dagster/Step Functions.
- **LangChain Observability: How to Monitor LLM Apps with ... - ** — [LangChain Observability: How to Monitor LLM Apps with ... - SigNoz](https://signoz.io/blog/langchain-observability-with-opentelemetry/)
  _Skipped because:_ Good practical observability walkthrough, but it is not a production case study with concrete system metrics (throughput/p95/failure modes/cost per task) as requested.

## Reasoning
**Curator:** Selected the most authoritative, directly citable sources from the candidates: Dagster docs for concrete retry primitives and Temporal docs for the canonical durable execution model (event history + replay). The remaining needs require benchmark studies and structured cross-engine comparisons that the provided candidates do not adequately supply.
**Reviewer:** The curator’s Temporal replay + Dagster op-retry picks are strong, but the library still needs thin official execution/concurrency docs and at least one speculation/latency paper with concrete numbers to cover key workflow patterns and empirical trade-offs.

---

# Curation Report: Agent Planning: How Agents Decide What to Do Next
**Topic:** `agent-workflows` | **Date:** 2026-04-10 19:16
**Library:** 27 existing → 38 sources (11 added, 7 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (11)
- **[reference_doc]** [Function Calling - OpenAI Platform](https://platform.openai.com/docs/guides/function-calling?api-mode=chat)
  Gives authoritative, citable details on how tool calls are represented and controlled, which directly constrains agent planning loops (when to call tools, how to select tools, and how to parse/validate tool outputs).
- **[reference_doc]** [Structured Outputs - OpenAI API](https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat)
  Provides the precise mechanism for forcing plans, actions, and state updates into machine-checkable JSON—critical for reliable plan-execute-replan pipelines and for teaching how schema constraints change agent behavior.
- **[benchmark]** [ALFWorld: Aligning Text and Embodied Environments for Interactive Learning](https://ar5iv.labs.arxiv.org/html/2010.03768)
  Adds a widely-used long-horizon benchmark where planning quality and replanning matter; the paper provides concrete evaluation protocol and results that can be cited when discussing success rates and error modes.
- **[benchmark]** [[PDF] VESTABENCH: An Embodied Benchmark for Safe Long-Horizon Planning Under Multi-Constraint and Adversarial Settings](https://aclanthology.org/2025.emnlp-industry.149.pdf)
  Directly targets long-horizon planning under constraints (a core agent-planning failure mode) and supplies a modern benchmark framing that supports teaching tradeoffs between goal achievement and constraint satisfaction.
- **[paper]** [Enhancing LLM-Based Agents via Global Planning and ...](https://arxiv.org/html/2504.16563v2)
  Most likely among the candidates to provide a structured, research-style comparison of planning paradigms and their algorithmic differences, supporting teachable criteria like when global planning helps vs reactive acting.
- **[paper]** [Planning and Acting in Partially Observable Stochastic Domains](https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf)
  This is a seminal, equation-heavy reference that directly fills the decision-theoretic planning/replanning gap (belief updates + action selection under uncertainty) that LLM-agent surveys typically only summarize.
- **[paper]** [Reinforcement Learning: An Introduction (2nd ed.)](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)
  Even though it’s a textbook, it’s the most citable single source for the exact MDP/value-function machinery needed to teach agent planning rigorously and to map LLM planning heuristics onto formal objectives.
- **[reference_doc]** [Tool calling (OpenAI Platform Guide)](https://platform.openai.com/docs/guides/function-calling?lang=python)
  The curator’s rationale says “thin docs are valuable,” and this page is exactly that: stable, authoritative details and examples that constrain real agent planning/execution behavior and are easy to cite.
- **[paper]** [Planning and Acting in Partially Observable Stochastic Domains](https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf) *(promoted by reviewer)*
  This is a seminal, equation-heavy reference that directly fills the decision-theoretic planning/replanning gap (belief updates + action selection under uncertainty) that LLM-agent surveys typically only summarize.
- **[paper]** [Reinforcement Learning: An Introduction (2nd ed.)](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf) *(promoted by reviewer)*
  Even though it’s a textbook, it’s the most citable single source for the exact MDP/value-function machinery needed to teach agent planning rigorously and to map LLM planning heuristics onto formal objectives.
- **[reference_doc]** [Tool calling (OpenAI Platform Guide)](https://platform.openai.com/docs/guides/function-calling?lang=python) *(promoted by reviewer)*
  The curator’s rationale says “thin docs are valuable,” and this page is exactly that: stable, authoritative details and examples that constrain real agent planning/execution behavior and are easy to cite.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Assistants migration guide - OpenAI API** — [Assistants migration guide - OpenAI API](https://platform.openai.com/docs/assistants/how-it-works)
  _Skipped because:_ Useful context for migration, but less directly focused on the precise tool-calling/structured-output constraints that most affect planning-loop mechanics.
- **What's new in Assistants API Beta - OpenAI Platform** — [What's new in Assistants API Beta - OpenAI Platform](https://platform.openai.com/docs/assistants/whats-new)
  _Skipped because:_ Changelog-style content is harder to cite for stable defaults/constraints than the dedicated function-calling and structured-outputs guides.
- **ReEfBench: Quantifying the Reasoning Efficiency of LLMs - ar** — [ReEfBench: Quantifying the Reasoning Efficiency of LLMs - arXiv](https://arxiv.org/html/2601.03550v1)
  _Skipped because:_ Promising for efficiency metrics, but it is not clearly centered on agent planning/replanning benchmarks (success/steps/tool calls) compared to ALFWorld/VESTABENCH.

## Reasoning
**Curator:** Selections prioritize authoritative API specs that directly constrain planning loops and benchmark papers that provide standardized long-horizon planning evaluations with citable protocols/results; remaining gaps require classic decision-theoretic planning sources and real production case studies with hard metrics.
**Reviewer:** The library is strong on LLM-agent planning surveys/frameworks, but it still needs at least one canonical formal planning source (POMDP/MDP equations) and should not omit the official tool-calling guide page that provides the exact API-level constraints planners must obey.

---

# Curation Report: Multi-Agent Architectures: Supervisors and Subgraphs
**Topic:** `agent-workflows` | **Date:** 2026-04-10 19:28
**Library:** 27 existing → 37 sources (10 added, 7 downloaded)
**Candidates evaluated:** 44
**Reviewer verdict:** needs_additions

## Added (10)
- **[paper]** [Between MDPs and Semi-MDPs: Learning, Planning, and Representing Knowledge at Multiple Temporal Scales](http://incompleteideas.net/papers/SPS-98.pdf)
  Gives the canonical mathematical grounding for hierarchical delegation (supervisor selecting sub-policies) including termination and credit assignment in semi-MDPs—directly mappable to supervisor→subgraph routing.
- **[benchmark]** [Learning Latency-Aware Orchestration for Parallel Multi-Agent Systems](https://arxiv.org/pdf/2601.10560.pdf)
  Directly targets the missing controlled numeric comparisons for parallel multi-agent orchestration, including methodology and ablations that help teach why supervisor/subgraph topology changes latency and success.
- **[reference_doc]** [Handoffs - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/ref/handoffs/)
  Provides citable, versioned API surface for delegation primitives (handoffs) that a tutor can quote when students ask exactly what data is passed and how transcripts are mapped.
- **[code]** [Examples](https://openai.github.io/openai-agents-python/examples/)
  Adds executable reference implementations students can follow step-by-step to understand execution order, state passing, and how to structure multi-agent delegation in practice.
- **[paper]** [Learning Latency-Aware Orchestration for Parallel Multi-Agent Systems](https://arxiv.org/abs/2601.10560)
  Even if primarily a benchmark-style paper, it is one of the few candidates explicitly centered on latency-aware orchestration with concrete measured outcomes—directly relevant to supervisor/subgraph topology and the still-unfilled operational-metrics need.
- **[reference_doc]** [Responses API Reference (OpenAI)](https://platform.openai.com/docs/api-reference/responses)
  It was rejected as ‘not clearly aligned’, but thin API references are precisely what students need when implementing supervisors/subgraphs; it provides authoritative parameter names and payload shapes that govern orchestration behavior.
- **[paper]** [MasRouter: Learning to Route LLMs for Multi-Agent System](https://aclanthology.org/2025.acl-long.757.pdf)
  Supervisor/subgraph architectures hinge on routing decisions; this is a directly on-topic routing paper with concrete procedures and numbers, complementing the library’s current emphasis on frameworks/docs.
- **[paper]** [Learning Latency-Aware Orchestration for Parallel Multi-Agent Systems](https://arxiv.org/abs/2601.10560) *(promoted by reviewer)*
  Even if primarily a benchmark-style paper, it is one of the few candidates explicitly centered on latency-aware orchestration with concrete measured outcomes—directly relevant to supervisor/subgraph topology and the still-unfilled operational-metrics need.
- **[reference_doc]** [Responses API Reference (OpenAI)](https://platform.openai.com/docs/api-reference/responses) *(promoted by reviewer)*
  It was rejected as ‘not clearly aligned’, but thin API references are precisely what students need when implementing supervisors/subgraphs; it provides authoritative parameter names and payload shapes that govern orchestration behavior.
- **[paper]** [MasRouter: Learning to Route LLMs for Multi-Agent System](https://aclanthology.org/2025.acl-long.757.pdf) *(promoted by reviewer)*
  Supervisor/subgraph architectures hinge on routing decisions; this is a directly on-topic routing paper with concrete procedures and numbers, complementing the library’s current emphasis on frameworks/docs.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **OpenAI Responses model - OpenAI Agents SDK** — [OpenAI Responses model - OpenAI Agents SDK](https://openai.github.io/openai-agents-python/ref/models/openai_responses/)
  _Skipped because:_ Likely useful for tool-call/streaming schema details, but the provided candidate preview is not clearly aligned to orchestration defaults (timeouts/retries/concurrency) versus handoff mechanics.
- **The Logical Options Framework** — [The Logical Options Framework](https://proceedings.mlr.press/v139/araki21a/araki21a.pdf)
  _Skipped because:_ Strong HRL formalism, but Sutton et al. (1998) is the more canonical, broadly-cited foundation for options/semi-MDP equations and termination semantics.
- **Confusing/unexpected checkpointing behaviour with subgraphs ** — [Confusing/unexpected checkpointing behaviour with subgraphs · Issue #5639 · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/issues/5639)
  _Skipped because:_ Contains a minimal repro and real-world checkpointing nuance, but it is an issue thread (non-authoritative, potentially transient) rather than a stable, curated runnable example.

## Reasoning
**Curator:** Selections prioritize (1) canonical hierarchical-control math (options/semi-MDPs), (2) controlled empirical orchestration results with latency/cost ablations, and (3) official, typed API docs plus runnable examples for concrete supervisor→sub-agent delegation.
**Reviewer:** The library is strong on frameworks and agent-planning surveys, but it should add at least one authoritative API reference for execution semantics and one routing/orchestration paper with concrete latency/cost numbers to better support supervisor/subgraph teaching and the deployment-metrics gap.

---

# Curation Report: Comparing Agentic Frameworks: LangGraph, AutoGen, CrewAI, and OpenAI Assistants
**Topic:** `agent-workflows` | **Date:** 2026-04-10 19:40
**Library:** 27 existing → 44 sources (17 added, 9 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (17)
- **[reference_doc]** [Responses | OpenAI API Reference](https://platform.openai.com/docs/api-reference/responses)
  This is the authoritative, citable spec for the newer Responses API and is the best single source for exact parameters, object shapes, and defaults the tutor will be asked to quote.
- **[reference_doc]** [Streaming events | OpenAI API Reference](https://platform.openai.com/docs/api-reference/responses-streaming)
  Streaming is where students most often need exact event names and schemas; this reference enables precise explanations and correct code patterns.
- **[reference_doc]** [Persistence - Docs by LangChain](https://docs.langchain.com/oss/javascript/langgraph/persistence)
  Among the deployment-oriented candidates, this is the most authoritative and directly teaches the mechanics needed for production-grade durability and recovery.
- **[reference_doc]** [Run Config - OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/ref/run_config/)
  The current library has handoffs docs but lacks the authoritative, field-level configuration surface that students will ask about when implementing agent loops and controlling retries/turn limits.
- **[reference_doc]** [RunConfig / Runner.run - OpenAI Agents SDK (Python) Reference](https://openai.github.io/openai-agents-python/ref/run/)
  This is the thin-but-critical spec page that pins down how an Agents SDK run is initiated and what state objects look like—necessary for precise comparisons to LangGraph state machines and AutoGen conversation loops.
- **[reference_doc]** [Built-in session implementations - OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/sessions/)
  The lesson explicitly compares durability/state across frameworks; this fills a gap on the OpenAI Agents side analogous to LangGraph persistence/checkpointing docs.
- **[reference_doc]** [Memory - OpenAI Agents SDK (Python) Reference](https://openai.github.io/openai-agents-python/ref/memory/)
  Without this, comparisons of “memory” across LangGraph (state/checkpoints), AutoGen (conversation history), and Assistants/Threads risk being hand-wavy; this page provides the exact API surface.
- **[reference_doc]** [Session - OpenAI Agents SDK (Python) Memory Session Reference](https://openai.github.io/openai-agents-python/ref/memory/session/)
  This is the lowest-level, most citable definition of session/memory behavior in the Agents SDK—useful for a precise “threads vs sessions vs checkpoints” comparison.
- **[reference_doc]** [Streaming support | OpenAI API Reference](https://platform.openai.com/docs/api-reference/streaming)
  Even if “Streaming events” is already added, this page is the canonical umbrella reference that students often land on; it helps triangulate endpoint-specific event docs and reduces ambiguity.
- **[code]** [LangGraph discussion: human_in_the_loop (resume/edit state with checkpointing)](https://github.com/langchain-ai/langgraph/discussions/2290)
  Official docs explain primitives, but this thread captures an end-to-end HITL resume workflow that directly addresses a common failure mode and is closer to a runnable recipe than the conceptual pages.
- **[reference_doc]** [Run Config - OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/ref/run_config/) *(promoted by reviewer)*
  The current library has handoffs docs but lacks the authoritative, field-level configuration surface that students will ask about when implementing agent loops and controlling retries/turn limits.
- **[reference_doc]** [RunConfig / Runner.run - OpenAI Agents SDK (Python) Reference](https://openai.github.io/openai-agents-python/ref/run/) *(promoted by reviewer)*
  This is the thin-but-critical spec page that pins down how an Agents SDK run is initiated and what state objects look like—necessary for precise comparisons to LangGraph state machines and AutoGen conversation loops.
- **[reference_doc]** [Built-in session implementations - OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/sessions/) *(promoted by reviewer)*
  The lesson explicitly compares durability/state across frameworks; this fills a gap on the OpenAI Agents side analogous to LangGraph persistence/checkpointing docs.
- **[reference_doc]** [Memory - OpenAI Agents SDK (Python) Reference](https://openai.github.io/openai-agents-python/ref/memory/) *(promoted by reviewer)*
  Without this, comparisons of “memory” across LangGraph (state/checkpoints), AutoGen (conversation history), and Assistants/Threads risk being hand-wavy; this page provides the exact API surface.
- **[reference_doc]** [Session - OpenAI Agents SDK (Python) Memory Session Reference](https://openai.github.io/openai-agents-python/ref/memory/session/) *(promoted by reviewer)*
  This is the lowest-level, most citable definition of session/memory behavior in the Agents SDK—useful for a precise “threads vs sessions vs checkpoints” comparison.
- **[reference_doc]** [Streaming support | OpenAI API Reference](https://platform.openai.com/docs/api-reference/streaming) *(promoted by reviewer)*
  Even if “Streaming events” is already added, this page is the canonical umbrella reference that students often land on; it helps triangulate endpoint-specific event docs and reduces ambiguity.
- **[code]** [LangGraph discussion: human_in_the_loop (resume/edit state with checkpointing)](https://github.com/langchain-ai/langgraph/discussions/2290) *(promoted by reviewer)*
  Official docs explain primitives, but this thread captures an end-to-end HITL resume workflow that directly addresses a common failure mode and is closer to a runnable recipe than the conceptual pages.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **API Reference - OpenAI API** — [API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/assistants-streaming/events)
  _Skipped because:_ Useful for legacy Assistants streaming, but the library already has an Assistants deep dive and the bigger gap is the newer Responses/Agents surface.
- **Scaling AI Workflows using LangGraph | A thousand nodes** — [Scaling AI Workflows using LangGraph | A thousand nodes](https://www.athousandnodes.com/posts/scaling-langgraph-production)
  _Skipped because:_ Potentially valuable, but it is a third-party blog (not official docs) and may not provide reliably citable metrics or guarantees.

## Reasoning
**Curator:** The candidates for comparisons/benchmarks/case studies were largely third-party and not reliably empirical or maintained; the strongest authoritative gap-fillers were the official OpenAI Responses API references (core precision needs) and the official LangGraph persistence documentation (durability semantics).
**Reviewer:** The curator’s additions are strong, but the library still lacks the thin, authoritative OpenAI Agents SDK reference pages needed for precise runtime/state comparisons, plus at least one concrete HITL resume example for LangGraph.
