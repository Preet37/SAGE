# Curation Report: Streaming, Debugging, and Observability in LangGraph
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:07
**Library:** 8 existing → 19 sources (11 added, 7 downloaded)
**Candidates evaluated:** 35
**Reviewer verdict:** needs_additions

## Added (11)
- **[reference_doc]** [Streaming - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/streaming)
  Authoritative LangGraph streaming reference covering the event model and multiple stream modes (state snapshots, per-step updates, and token streaming) with stable, maintained docs.
   — covers: LangGraph streaming APIs and event model (how to stream graph execution to clients), Token-level streaming with LangGraph-integrated chat models (how to surface incremental LLM tokens), Step/node-level streaming in LangGraph (streaming per-node outputs and state updates)
- **[reference_doc]** [Memory store](https://docs.langchain.com/oss/python/langgraph/persistence)
  Covers LangGraph checkpointing/persistence and how state snapshots are saved per step (threads), enabling inspection, replay/time-travel style debugging, and fault tolerance—core to intermediate-state observability.
   — covers: How to inspect intermediate LangGraph state (state snapshots, checkpoints, per-step state diffs)
- **[reference_doc]** [How to stream events¶](https://langchain-ai.github.io/langgraph/cloud/how-tos/stream_events/)
  Adds the deployment/client-side streaming event API details (including resumable streaming via last event ID) that are essential for streaming graph execution to real clients in production.
   — covers: LangGraph streaming APIs and event model (how to stream graph execution to clients)
- **[reference_doc]** [Trace with OpenTelemetry - Docs by LangChain (LangSmith)](https://docs.langchain.com/langsmith/trace-with-opentelemetry)
  This is the most authoritative, maintained reference for getting LangGraph/LangChain traces into a vendor-neutral telemetry pipeline (OTel), which is central to production observability beyond LangSmith’s UI.
   — covers: Tracing for LangGraph (integration with LangSmith/OpenTelemetry, spans, metadata captured), Observability fundamentals for agentic graphs (logs/metrics/traces, correlation IDs, sampling), Production monitoring for LangGraph agents (latency, tool error rates, token/cost metrics, alerts, dashboards)
- **[reference_doc]** [Introducing End-to-End OpenTelemetry Support in LangSmith](https://blog.langchain.com/end-to-end-opentelemetry-langsmith/)
  Pairs well with the OTel how-to by explaining the end-to-end architecture and practical implications (propagation, correlation, backends), which helps learners reason about tracing design choices in production.
   — covers: Tracing for LangGraph (integration with LangSmith/OpenTelemetry, spans, metadata captured), Observability fundamentals for agentic graphs (logs/metrics/traces, correlation IDs, sampling)
- **[paper]** [AgentOps: Enabling Observability of LLM Agents](https://arxiv.org/html/2411.05285v2)
  Even if early, it directly targets the missing conceptual layer (AgentOps/observability taxonomy for agentic systems) and can anchor the lesson’s observability fundamentals beyond tool-specific docs.
   — covers: Observability fundamentals for agentic graphs (logs/metrics/traces, correlation IDs, sampling), Production monitoring for LangGraph agents (latency, tool error rates, token/cost metrics, alerts, dashboards)
- **[video]** [Strategies for debugging agents with LangGraph Studio](https://www.youtube.com/watch?v=5vEC0Y4sV8g)
  This is one of the few candidates that appears to directly address the biggest uncovered gap—practical debugging workflows (visualization, replay/inspection) in the official-ish tooling ecosystem—where the current library is otherwise thin.
   — covers: LangGraph debugging workflows (debug mode, visualization, replaying runs, identifying failing nodes)
- **[reference_doc]** [Trace with OpenTelemetry - Docs by LangChain (LangSmith)](https://docs.langchain.com/langsmith/trace-with-opentelemetry) *(promoted by reviewer)*
  This is the most authoritative, maintained reference for getting LangGraph/LangChain traces into a vendor-neutral telemetry pipeline (OTel), which is central to production observability beyond LangSmith’s UI.
   — fills: Tracing for LangGraph (integration with LangSmith/OpenTelemetry, spans, metadata captured), Observability fundamentals for agentic graphs (logs/metrics/traces, correlation IDs, sampling), Production monitoring for LangGraph agents (latency, tool error rates, token/cost metrics, alerts, dashboards)
- **[reference_doc]** [Introducing End-to-End OpenTelemetry Support in LangSmith](https://blog.langchain.com/end-to-end-opentelemetry-langsmith/) *(promoted by reviewer)*
  Pairs well with the OTel how-to by explaining the end-to-end architecture and practical implications (propagation, correlation, backends), which helps learners reason about tracing design choices in production.
   — fills: Tracing for LangGraph (integration with LangSmith/OpenTelemetry, spans, metadata captured), Observability fundamentals for agentic graphs (logs/metrics/traces, correlation IDs, sampling)
- **[paper]** [AgentOps: Enabling Observability of LLM Agents](https://arxiv.org/html/2411.05285v2) *(promoted by reviewer)*
  Even if early, it directly targets the missing conceptual layer (AgentOps/observability taxonomy for agentic systems) and can anchor the lesson’s observability fundamentals beyond tool-specific docs.
   — fills: Observability fundamentals for agentic graphs (logs/metrics/traces, correlation IDs, sampling), Production monitoring for LangGraph agents (latency, tool error rates, token/cost metrics, alerts, dashboards)
- **[video]** [Strategies for debugging agents with LangGraph Studio](https://www.youtube.com/watch?v=5vEC0Y4sV8g) *(promoted by reviewer)*
  This is one of the few candidates that appears to directly address the biggest uncovered gap—practical debugging workflows (visualization, replay/inspection) in the official-ish tooling ecosystem—where the current library is otherwise thin.
   — fills: LangGraph debugging workflows (debug mode, visualization, replaying runs, identifying failing nodes)

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Streaming API - Docs by LangChain** — [Streaming API - Docs by LangChain](https://docs.langchain.com/langsmith/streaming)
  _Skipped because:_ Largely overlaps with the LangGraph streaming docs and the cloud stream-events how-to; adds little incremental coverage for this lesson.
- **How to stream¶** — [How to stream¶](https://langgraph.agentdevhub.com/how-tos/streaming/)
  _Skipped because:_ Useful, but redundant with the official LangChain/LangGraph streaming docs; prefer the canonical maintained documentation.
- **Stream outputs - GitHub Pages** — [Stream outputs - GitHub Pages](https://langchain-ai.github.io/langgraph/how-tos/streaming/)
  _Skipped because:_ Overlaps heavily with the OSS Python streaming docs; keep one canonical streaming reference to avoid redundancy.
- **Streaming - Docs by LangChain** — [Streaming - Docs by LangChain](https://docs.langchain.com/oss/javascript/langgraph/streaming)
  _Skipped because:_ Good for JS users, but the library additions already cover the streaming model; add only if the lesson explicitly targets JavaScript.
- **How to stream LLM tokens from your graph** — [How to stream LLM tokens from your graph](https://langchain-ai.github.io/langgraphjs/how-tos/stream-tokens/)
  _Skipped because:_ Narrow (token streaming in JS) and redundant given the broader Python streaming reference; include only for a JS-focused track.
- **langgraph/docs/docs/cloud/how-tos/stream_events.md at main ·** — [langgraph/docs/docs/cloud/how-tos/stream_events.md at main · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/cloud/how-tos/stream_events.md)
  _Skipped because:_ Same content as the rendered GitHub Pages stream-events doc; prefer the stable rendered documentation URL.
- **Checkpointing | LangChain Referencereference.langchain.com ›** — [Checkpointing | LangChain Referencereference.langchain.com › python › langgraph › checkpoints](https://reference.langchain.com/python/langgraph/checkpoints/)
  _Skipped because:_ Likely overlaps with the persistence/memory store doc; keep the more narrative, concept-oriented persistence page as the primary reference.
- **langgraph/docs/docs/concepts/persistence.md at main · langch** — [langgraph/docs/docs/concepts/persistence.md at main · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/persistence.md)
  _Skipped because:_ Redundant with the rendered persistence docs; prefer the stable docs site URL over a repo file view.
- **LangGraph Streaming 101: 5 Modes to Build Responsive AI Appl** — [LangGraph Streaming 101: 5 Modes to Build Responsive AI Applications](https://dev.to/sreeni5018/langgraph-streaming-101-5-modes-to-build-responsive-ai-applications-4p3f)
  _Skipped because:_ Third-party blog content that appears to mirror official docs; not clearly adding depth beyond canonical references.
- **Checkpoints and Human-Computer Interaction in LangGraph** — [Checkpoints and Human-Computer Interaction in LangGraph](https://dev.to/jamesli/checkpoints-and-human-computer-interaction-in-langgraph-26bk)
  _Skipped because:_ Potentially helpful, but likely derivative of official persistence/checkpointing docs; prefer authoritative sources for core mechanics.
- **Getting Started** — [Getting Started](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)
  _Skipped because:_ Good vendor-specific implementation guidance, but narrower (DynamoDB) and less directly focused on state inspection/debugging concepts than the official persistence docs.
- **Real-Time Streaming in LangGraph | Node vs LLM Streaming Mad** — [Real-Time Streaming in LangGraph | Node vs LLM Streaming Made Simple](https://www.youtube.com/watch?v=_8rf7Ln1CdQ)
  _Skipped because:_ May be useful, but video quality/stability varies and it’s likely redundant with the official streaming docs; include only if you want a video supplement.

## Uncovered Gaps (4) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- LangGraph debugging workflows (debug mode, visualization, replaying runs, identifying failing nodes)
- Tracing for LangGraph (integration with LangSmith/OpenTelemetry, spans, metadata captured)
- Observability fundamentals for agentic graphs (logs/metrics/traces, correlation IDs, sampling)
- Production monitoring for LangGraph agents (latency, tool error rates, token/cost metrics, alerts, dashboards)

## Reasoning
**Curator:** The strongest additions are the official LangGraph docs that directly and substantively cover streaming (including event/resumability) and persistence/checkpointing for intermediate state inspection. The remaining candidates are mostly redundant mirrors, narrower language-specific variants, or third-party summaries that don’t add enough beyond canonical references.
**Reviewer:** The streaming and persistence choices are solid and appropriately canonical, but the lesson still needs at least one authoritative tracing/OTel reference and one concrete LangGraph debugging workflow resource to close the largest observability gaps.

---

# Curation Report: Real-World Agent Use Cases and Production Patterns
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:09
**Library:** 15 existing → 20 sources (5 added, 3 downloaded)
**Candidates evaluated:** 30
**Reviewer verdict:** needs_additions

## Added (5)
- **[paper]** [CODEAGENT: Enhancing Code Generation with Tool-Integrated Agent Systems for Real-World Repo-level Coding Challenges](https://aclanthology.org/2024.acl-long.737.pdf)
  Adds a rigorous, peer-reviewed treatment of the repo-level coding agent pattern, including tool integration and iterative workflows—coverage that’s largely missing from the current library’s production/eval/observability focus.
   — covers: Code generation agent pattern: repo context ingestion, toolchain integration (git, tests, linters), patch generation/apply, iterative debugging, sandboxing, security constraints, Agent reliability and evaluation: offline/online eval frameworks, golden datasets, task success metrics, tool-call correctness, hallucination/grounding measures, continuous regression testing and monitoring
- **[paper]** [ReliabilityBench: Evaluating LLM Agent Reliability Under Production ...](https://arxiv.org/html/2601.06112v1)
  This directly targets the library’s biggest missing “production reliability” layer (robustness under failures, metamorphic testing, chaos/fault injection) and is more on-point for agent production patterns than generic LLM eval tooling already included.
   — covers: Production deployment patterns for agents: architecture, hosting, scaling, state/persistence, queues, rate limits, cost controls, observability (tracing/logging/metrics), SLOs, rollout/versioning, Robust error handling: tool failure taxonomy, retries with backoff, timeouts, circuit breakers, idempotency, validation/repair loops, fallback strategies
- **[paper]** [Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988)
  Even if narrower than CodeAgent, it’s a high-leverage complement: it isolates and quantifies a key production pain point (repo context packaging/selection) that strongly affects real-world coding-agent success and evaluation design.
   — covers: Production deployment patterns for agents: architecture, hosting, scaling, state/persistence, queues, rate limits, cost controls, observability (tracing/logging/metrics), SLOs, rollout/versioning
- **[paper]** [ReliabilityBench: Evaluating LLM Agent Reliability Under Production ...](https://arxiv.org/html/2601.06112v1) *(promoted by reviewer)*
  This directly targets the library’s biggest missing “production reliability” layer (robustness under failures, metamorphic testing, chaos/fault injection) and is more on-point for agent production patterns than generic LLM eval tooling already included.
   — fills: Production deployment patterns for agents: architecture, hosting, scaling, state/persistence, queues, rate limits, cost controls, observability (tracing/logging/metrics), SLOs, rollout/versioning, Robust error handling: tool failure taxonomy, retries with backoff, timeouts, circuit breakers, idempotency, validation/repair loops, fallback strategies
- **[paper]** [Are Repository-Level Context Files Helpful for Coding Agents?](https://arxiv.org/abs/2602.11988) *(promoted by reviewer)*
  Even if narrower than CodeAgent, it’s a high-leverage complement: it isolates and quantifies a key production pain point (repo context packaging/selection) that strongly affects real-world coding-agent success and evaluation design.
   — fills: Production deployment patterns for agents: architecture, hosting, scaling, state/persistence, queues, rate limits, cost controls, observability (tracing/logging/metrics), SLOs, rollout/versioning

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **8 Deploying agents and agentic systems** — [8 Deploying agents and agentic systems](https://www.manning.com/preview/ai-agents-in-action-second-edition/chapter-8)
  _Skipped because:_ Likely strong on deployment patterns, but as a preview chapter it may be incomplete/paywalled and less stable/accessible for a teaching wiki than fully available sources.
- **CodeAgent: Enhancing Code Generation with Tool- ...** — [CodeAgent: Enhancing Code Generation with Tool- ...](https://arxiv.org/html/2401.07339v2)
  _Skipped because:_ Redundant with the ACL Anthology version of the same work; the Anthology PDF is the more canonical, citable venue copy.
- **Are Repository-Level Context Files Helpful for Coding Agents** — [Are Repository-Level Context Files Helpful for Coding Agents? - arXiv](https://www.arxiv.org/abs/2602.11988)
  _Skipped because:_ Potentially useful but narrower (context files) and less directly about end-to-end agent toolchains than CodeAgent; would be a second-order add after the core paper.
- **Deploying AI Agents to Production: Architecture, Infrastruct** — [Deploying AI Agents to Production: Architecture, Infrastructure, and ...](https://machinelearningmastery.com/deploying-ai-agents-to-production-architecture-infrastructure-and-implementation-roadmap/)
  _Skipped because:_ Practical but blog-level and often higher-level; may not add enough beyond existing observability/debugging resources to justify inclusion over more authoritative deployment references.
- **Beyond the Notebook: 4 Architectural Patterns for Production** — [Beyond the Notebook: 4 Architectural Patterns for Production-Ready ...](https://dev.to/fmquaglia/beyond-the-notebook-4-architectural-patterns-for-production-ready-ai-agents-3a16)
  _Skipped because:_ Dev.to posts are typically uneven and can be thin; not clearly authoritative enough for a high-quality curated shelf.
- **Shadow Testing In Production** — [Shadow Testing In Production](https://www.agentik-os.com/blog/agent-deployment-patterns-production)
  _Skipped because:_ Covers an important rollout technique, but appears to be a vendor blog and likely too narrow (shadow testing only) without broader production architecture depth.
- **Chapter 13: Production Deployment & Scaling AI Agents** — [Chapter 13: Production Deployment & Scaling AI Agents](https://guidesfor.dev/applied-agentic-ai-2026-guide/production-deployment-scaling/)
  _Skipped because:_ Unclear authorship/reputation and the snippet appears duplicated; not enough signal of quality/stability to include.
- **[PDF] An Empirical Study of Multi-Agent RAG for Real-World U** — [[PDF] An Empirical Study of Multi-Agent RAG for Real-World University ...](https://www.arxiv.org/pdf/2507.11272.pdf)
  _Skipped because:_ Could help with research-assistant/RAG workflows, but without clearer evidence of strong methodology and broadly reusable patterns, it’s hard to prioritize over more established RAG/grounding references.
- **Open-Source Agentic Hybrid RAG Framework for Scientific ... ** — [Open-Source Agentic Hybrid RAG Framework for Scientific ... - arXiv](https://arxiv.org/html/2508.05660v1)
  _Skipped because:_ Framework-style papers can be implementation-specific and less generalizable; the candidate list doesn’t provide enough detail to confirm it substantively covers citation/grounding and evaluation loops.
- **[PDF] An Empirical Evaluation of a Multi-Agent Framework for** — [[PDF] An Empirical Evaluation of a Multi-Agent Framework for Retrieval ...](https://d197for5662m48.cloudfront.net/documents/publicationstatus/273020/preprint_pdf/d6bce72bd2f35cbdcaf07db93401a95d.pdf)
  _Skipped because:_ Appears to be an unreviewed preprint with uncertain venue/impact; may not meet the “high quality, reputable, stable” bar for a core teaching wiki.
- **[PDF] Fnu Neha1 and Deepshikha Bhati1 1Dept. of Computer Sci** — [[PDF] Fnu Neha1 and Deepshikha Bhati1 1Dept. of Computer Science ...](https://d197for5662m48.cloudfront.net/documents/publicationstatus/276113/preprint_pdf/d0ad4a1b24cbb2ee88d0e0ab48c34862.pdf)
  _Skipped because:_ Insufficient bibliographic clarity and likely low signal/quality; not suitable for a curated recommended-reading shelf.
- **[PDF] Master Thesis Agentic Retrieval Augmented Generation f** — [[PDF] Master Thesis Agentic Retrieval Augmented Generation for ...](https://cig.fi.upm.es/wp-content/uploads/TFM_RAMIRO_LOPEZ_CENTO.pdf)
  _Skipped because:_ Theses can be valuable but are uneven and less canonical; without clear evidence of standout novelty/rigor, it’s not a top-tier addition.

## Uncovered Gaps (4) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Production deployment patterns for agents: architecture, hosting, scaling, state/persistence, queues, rate limits, cost controls, observability (tracing/logging/metrics), SLOs, rollout/versioning
- Research assistant agent pattern: retrieval (RAG) pipelines, source selection/ranking, citation/grounding, multi-step research workflows, summarization with provenance, fact-checking loops
- Customer support automation: ticket triage, knowledge base retrieval, CRM/helpdesk integrations, escalation/handoff to humans, policy compliance, QA review, deflection and CSAT metrics
- Robust error handling: tool failure taxonomy, retries with backoff, timeouts, circuit breakers, idempotency, validation/repair loops, fallback strategies

## Reasoning
**Curator:** Most candidates are blog-level or unclear-quality sources; the one clear, high-authority addition is the ACL CodeAgent paper, which directly fills the repo-level coding agent/toolchain gap and adds evaluation-relevant insights without duplicating existing observability/eval tooling references.
**Reviewer:** The CodeAgent addition is strong, but the shelf still lacks a truly agent-specific reliability/failure-testing anchor and a focused repo-context study that materially improves the “real-world coding agent” production pattern coverage.

---

# Curation Report: Capstone: Designing and Building a Production-Ready Agent
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:10
**Library:** 18 existing → 26 sources (8 added, 5 downloaded)
**Candidates evaluated:** 35
**Reviewer verdict:** needs_additions

## Added (8)
- **[paper]** [[2512.08769] A Practical Guide for Designing, Developing, and Deploying Agentic AI](https://arxiv.org/abs/2512.08769)
  Adds an end-to-end, production-oriented methodology (requirements → architecture → deployment/ops) that your current library lacks, tying design choices to real workflow implementation considerations.
   — covers: A complete end-to-end production agent design methodology (requirements, architecture, safety, deployment, operations)
- **[reference_doc]** [LangGraph overview - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/overview)
  Provides the authoritative entry point for LangGraph’s orchestration model (state graphs, durable execution concepts, and core primitives) and is the most stable, canonical source among the candidates for deeper LangGraph study.
   — covers: LangGraph orchestration in depth: state modeling, node/edge patterns, control flow, persistence semantics, retries, streaming, deployment
- **[reference_doc]** [Interrupts - Docs by LangChain (LangGraph)](https://docs.langchain.com/oss/python/langgraph/interrupts)
  This is the canonical, high-authority reference for pause/resume semantics in LangGraph and directly enables production-grade approval gates and audit-friendly workflows—one of the explicitly uncovered gaps.
   — covers: Human-in-the-loop approval checkpoints in LangGraph: interrupt/pause-resume, approval gates, audit trails
- **[reference_doc]** [Human-in-the-loop - Docs by LangChain](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)
  Pairs with LangGraph interrupts to show end-to-end HITL patterns (approval, edits, escalation) using official primitives; more authoritative and durable than third-party blog tutorials.
   — covers: Human-in-the-loop approval checkpoints in LangGraph: interrupt/pause-resume, approval gates, audit trails
- **[paper]** [Towards More Standardized AI Evaluation: From Models to Agents](https://arxiv.org/html/2602.18029v1)
  Even if the snippet looks thin, this targets the missing “standardized evaluation for agents” layer (beyond model eval harnesses) and is directly aligned with designing offline/online eval, regression testing, and monitoring for agentic systems.
   — covers: Agent evaluation: offline/online eval design, harnesses, rubrics, automated evaluation, regression testing, monitoring and drift
- **[reference_doc]** [Interrupts - Docs by LangChain (LangGraph)](https://docs.langchain.com/oss/python/langgraph/interrupts) *(promoted by reviewer)*
  This is the canonical, high-authority reference for pause/resume semantics in LangGraph and directly enables production-grade approval gates and audit-friendly workflows—one of the explicitly uncovered gaps.
   — fills: Human-in-the-loop approval checkpoints in LangGraph: interrupt/pause-resume, approval gates, audit trails
- **[reference_doc]** [Human-in-the-loop - Docs by LangChain](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) *(promoted by reviewer)*
  Pairs with LangGraph interrupts to show end-to-end HITL patterns (approval, edits, escalation) using official primitives; more authoritative and durable than third-party blog tutorials.
   — fills: Human-in-the-loop approval checkpoints in LangGraph: interrupt/pause-resume, approval gates, audit trails
- **[paper]** [Towards More Standardized AI Evaluation: From Models to Agents](https://arxiv.org/html/2602.18029v1) *(promoted by reviewer)*
  Even if the snippet looks thin, this targets the missing “standardized evaluation for agents” layer (beyond model eval harnesses) and is directly aligned with designing offline/online eval, regression testing, and monitoring for agentic systems.
   — fills: Agent evaluation: offline/online eval design, harnesses, rubrics, automated evaluation, regression testing, monitoring and drift

## Near-Misses (13) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **A Practical Guide for Designing, Developing, and Deploying .** — [A Practical Guide for Designing, Developing, and Deploying ... - arXiv (HTML)](https://arxiv.org/html/2512.08769v1)
  _Skipped because:_ Redundant with the arXiv abstract/canonical entry; prefer the stable canonical arXiv URL for citation and long-term access.
- **A Practical Guide for Designing, Developing, and Deploying .** — [A Practical Guide for Designing, Developing, and Deploying ...](https://www.sciencestack.ai/paper/2512.08769)
  _Skipped because:_ Third-party mirror/aggregator; less stable/authoritative than the canonical arXiv source.
- **Guide to Production-Grade Agentic AI** — [Guide to Production-Grade Agentic AI](https://www.emergentmind.com/papers/2512.08769)
  _Skipped because:_ Secondary summary/portal rather than the primary paper; adds little beyond the canonical arXiv version.
- **2512.08769** — [2512.08769](https://papers.cool/arxiv/2512.08769)
  _Skipped because:_ Aggregator page; not as reputable or stable as arXiv for a curated teaching wiki.
- **LangGraph AI Framework 2025: Complete Architecture Guide + .** — [LangGraph AI Framework 2025: Complete Architecture Guide + ...](https://latenode.com/blog/ai-frameworks-technical-infrastructure/langgraph-multi-agent-orchestration/langgraph-ai-framework-2025-complete-architecture-guide-multi-agent-orchestration-analysis)
  _Skipped because:_ Likely a third-party blog that may be helpful but is less authoritative than the official LangGraph docs for core semantics and patterns.
- **[PDF] Orchestrating Agentic State Machines with LangGraph - ** — [[PDF] Orchestrating Agentic State Machines with LangGraph - GitHub Pages](https://conf42.github.io/static/slides/Rajeshwari%20Sah%20-%20Conf42%20Machine%20Learning%202026.pdf)
  _Skipped because:_ Conference slides are typically thinner and less precise than official docs for persistence/retries/semantics; good supplement but not a core shelf item.
- **LangGraph: Modular LLM Agent Orchestration** — [LangGraph: Modular LLM Agent Orchestration](https://www.emergentmind.com/topics/langgraph)
  _Skipped because:_ Topic hub/summary rather than a primary technical reference; overlaps with the official docs without adding durable details.
- **LangGraph Architecture - Emergent Mind** — [LangGraph Architecture - Emergent Mind](https://www.emergentmind.com/topics/langgraph-architecture)
  _Skipped because:_ Secondary overview; not as definitive as the official documentation for implementation semantics.
- **Evaluating Advanced Chunking Strategies for Retrieval-Augmen** — [Evaluating Advanced Chunking Strategies for Retrieval-Augmented ...](https://arxiv.org/abs/2504.19754)
  _Skipped because:_ Potentially useful for chunking evaluation, but it’s narrow (chunking-focused) and doesn’t clearly cover the broader production RAG pipeline (indexing, retrieval strategies, grounding/citations, end-to-end retrieval eval) needed for this capstone.
- **An Empirical Evaluation of RAG Architectures for Policy Docu** — [An Empirical Evaluation of RAG Architectures for Policy Document ...](https://arxiv.org/abs/2601.15457)
  _Skipped because:_ Likely domain-specific (policy documents) and may not generalize into a foundational, production RAG reference for the capstone without more evidence of broad coverage.
- **Comparative Evaluation of Advanced Chunking for Retrieval ..** — [Comparative Evaluation of Advanced Chunking for Retrieval ...](https://pmc.ncbi.nlm.nih.gov/articles/PMC12649634/)
  _Skipped because:_ Appears to mirror the chunking-evaluation theme; still too narrow versus the capstone’s need for end-to-end RAG production guidance.
- **Chunking, Retrieval, and Re-ranking: An Empirical Evaluation** — [Chunking, Retrieval, and Re-ranking: An Empirical Evaluation of ...](https://tldr.takara.ai/p/2601.15457v1)
  _Skipped because:_ TL;DR summary is not a primary source and is too thin for a curated, high-quality teaching library.
- **RAG Chunking Strategy | GPT-trainer Blog** — [RAG Chunking Strategy | GPT-trainer Blog](https://gpt-trainer.com/blog/rag+chunking+strategy)
  _Skipped because:_ Vendor blog content is less reliable/neutral and typically less rigorous than peer-reviewed or canonical documentation sources.

## Uncovered Gaps (5) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- RAG fundamentals and production details: chunking, embeddings, indexing, retrieval strategies, grounding/citations, evaluation of retrieval
- Structured tool calling implementation details: schema design, validation, tool error handling, tool-result integration patterns
- Human-in-the-loop approval checkpoints in LangGraph: interrupt/pause-resume, approval gates, audit trails
- Observability for agents: tracing/logging/metrics, how to instrument LangGraph runs, debugging workflows
- Agent evaluation: offline/online eval design, harnesses, rubrics, automated evaluation, regression testing, monitoring and drift

## Reasoning
**Curator:** Only two candidates clearly add non-redundant, high-authority coverage: the arXiv practical guide for end-to-end production methodology and the official LangGraph overview as the canonical orchestration reference. The remaining candidates are either mirrors/summaries, less authoritative third-party content, or too narrow (chunking-only) to fill the capstone’s broader RAG/tooling/eval/ops gaps.
**Reviewer:** The curator’s additions are solid, but the library still needs the official LangGraph HITL/interrupt docs and at least one agent-focused evaluation paper to close the most explicit remaining gaps.

---

# Curation Report: Framework Selection Criteria: Choosing the Right Tool for the Job
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:12
**Library:** 23 existing → 30 sources (7 added, 5 downloaded)
**Candidates evaluated:** 30
**Reviewer verdict:** needs_additions

## Added (7)
- **[paper]** [An Empirical Study of Agent Developer Practices in AI Agent Frameworks](https://arxiv.org/pdf/2512.01939.pdf)
  Adds evidence-based insight into how practitioners actually choose and use agent frameworks, which can be translated into concrete selection criteria (ergonomics, extensibility, debugging/ops fit) beyond what the current library’s framework docs provide.
   — covers: A structured framework-selection decision process for agent frameworks (mapping production requirements to framework primitives), Build vs buy tradeoffs for agent orchestration frameworks (maintenance, extensibility, lock-in, ecosystem, compliance)
- **[paper]** [Building AI Agents for Autonomous Clouds: Challenges and Design Principles](https://dl.acm.org/doi/pdf/10.1145/3698038.3698525)
  Provides principled guidance on deploying/operating agents in real cloud environments (security, reliability, control loops, failure modes), helping connect deployment constraints and SLOs to framework capabilities.
   — covers: Deployment constraints for agent systems (on-prem vs cloud, data residency, auth/secrets, networking, cost/latency SLOs) and how they affect framework choice, Scalability/serving considerations for agents (concurrency, durable queues, retries, backpressure, multi-tenancy) and framework support, Observability and evaluation for agents (tracing models, metrics, offline/online evals, regression testing, prompt/tool-call audits)
- **[paper]** [The Evolution of Agentic AI Software Architecture](https://arxiv.org/html/2602.10479)
  Likely offers a broad architecture taxonomy and progression of agentic system designs, useful for mapping requirements (control, state, coordination, reliability) to architectural primitives when selecting a framework.
   — covers: A structured framework-selection decision process for agent frameworks (mapping production requirements to framework primitives), Scalability/serving considerations for agents (concurrency, durable queues, retries, backpressure, multi-tenancy) and framework support, Build vs buy tradeoffs for agent orchestration frameworks (maintenance, extensibility, lock-in, ecosystem, compliance)
- **[paper]** [Comparing Human Oversight Strategies for Computer-Use Agents](https://arxiv.org/html/2604.04918v1)
  Directly targets the library’s explicitly still-uncovered gap with a concrete oversight strategy design space (risk-gating, confirmations, supervisory co-execution) and implementation considerations that translate into framework selection criteria (interrupt primitives, auditability, policy hooks).
   — covers: Human oversight patterns in production agents (interrupts, approval gates, escalation, audit trails) and selection implications
- **[paper]** [On the Quest for Effectiveness in Human Oversight](https://arxiv.org/html/2404.04059v2)
  A higher-level but still rigorous companion to oversight-strategy comparisons: it helps justify when/why to require human checkpoints and what “effective oversight” means, which is crucial for turning oversight into concrete framework requirements (review queues, traceability, escalation paths).
   — covers: Human oversight patterns in production agents (interrupts, approval gates, escalation, audit trails) and selection implications
- **[paper]** [Comparing Human Oversight Strategies for Computer-Use Agents](https://arxiv.org/html/2604.04918v1) *(promoted by reviewer)*
  Directly targets the library’s explicitly still-uncovered gap with a concrete oversight strategy design space (risk-gating, confirmations, supervisory co-execution) and implementation considerations that translate into framework selection criteria (interrupt primitives, auditability, policy hooks).
   — fills: Human oversight patterns in production agents (interrupts, approval gates, escalation, audit trails) and selection implications
- **[paper]** [On the Quest for Effectiveness in Human Oversight](https://arxiv.org/html/2404.04059v2) *(promoted by reviewer)*
  A higher-level but still rigorous companion to oversight-strategy comparisons: it helps justify when/why to require human checkpoints and what “effective oversight” means, which is crucial for turning oversight into concrete framework requirements (review queues, traceability, escalation paths).
   — fills: Human oversight patterns in production agents (interrupts, approval gates, escalation, audit trails) and selection implications

## Near-Misses (12) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] A Systematic Approach to Agent Architecture Selection** — [[PDF] A Systematic Approach to Agent Architecture Selection](https://www.ijcttjournal.org/2025/Volume-73%20Issue-5/IJCTT-V73I5P105.pdf)
  _Skipped because:_ The venue and authorship signals are weaker/less established, and it’s unclear from the preview whether it provides a rigorous, actionable decision procedure beyond high-level guidance.
- **Multi-Agent Decision Framework: A Systematic Approach to ...** — [Multi-Agent Decision Framework: A Systematic Approach to ...](https://ijcttjournal.org/2025/Volume-73%20Issue-5/IJCTT-V73I5P105.pdf)
  _Skipped because:_ Duplicate of Candidate 1 (same URL) and does not clear the quality/rigor bar versus stronger archival sources.
- **The Complete AI Agent Decision Framework** — [The Complete AI Agent Decision Framework](https://machinelearningmastery.com/the-complete-ai-agent-decision-framework/)
  _Skipped because:_ MachineLearningMastery posts are often practical but can be uneven and less citable; this is likely too generic compared with stronger peer-reviewed/archival sources.
- **8.1 Deployment Options – Cloud, On-Premise, and Hybrid Syste** — [8.1 Deployment Options – Cloud, On-Premise, and Hybrid Systems](https://agenticaiguide.ai/ch_8/sec_8-1.html)
  _Skipped because:_ Potentially useful, but the site’s authority/stability is unclear and it may not go deep enough on concrete constraints-to-framework mapping.
- **#31: Deploying and Securing Agentic AI Systems: Best Practic** — [#31: Deploying and Securing Agentic AI Systems: Best Practices & Challenges [8-min read].](https://aiwithkt.substack.com/p/31-deploying-and-securing-agentic)
  _Skipped because:_ Substack posts are typically opinionated and not durable/authoritative enough for a high-quality teaching wiki unless uniquely deep.
- **Scaling AI Agents — From 10 to 10,000 Concurrent Agents** — [Scaling AI Agents — From 10 to 10,000 Concurrent Agents](https://agentcenter.cloud/blogs/scaling-ai-agents-production)
  _Skipped because:_ Likely practical, but appears vendor/blog content with uncertain rigor and may not provide framework-agnostic, reusable selection criteria.
- **Production Considerations** — [Production Considerations](https://www.arunbaby.com/ai-agents/0054-scaling-multi-agent-systems/)
  _Skipped because:_ Personal blog content with unclear depth and authority; may be redundant with better sources on scaling/ops principles.
- **Scaling Agent Systems: Architecture That Survives Growth** — [Scaling Agent Systems: Architecture That Survives Growth](https://www.agentik-os.com/blog/scaling-agent-systems-architecture)
  _Skipped because:_ Another vendor/blog-style article; may contain good advice but is less reliable than archival papers for a curated core library.
- **Adaptive AI Agent Placement and Migration in Edge ...** — [Adaptive AI Agent Placement and Migration in Edge ...](https://arxiv.org/html/2508.03345v1)
  _Skipped because:_ Seems focused on edge placement/migration research rather than practical deployment constraints and framework selection for production agent systems.
- **11th International Workshop on Science Gateways (IWSG 2019),** — [11th International Workshop on Science Gateways (IWSG 2019), 12-14 June 2019](https://ceur-ws.org/Vol-2975/paper1.pdf)
  _Skipped because:_ Workshop proceedings are broad and not clearly targeted to agent framework selection; likely too indirect for the stated gaps.
- **What is Scalability in Multi-Agent Systems?** — [What is Scalability in Multi-Agent Systems?](https://dl.acm.org/doi/pdf/10.1145/336595.337033)
  _Skipped because:_ Potentially foundational but also quite old and may not address modern serving concerns (queues, retries, multi-tenancy, observability) in a way that informs today’s framework choices.
- **oopsla2000-final-pdf.PDF** — [oopsla2000-final-pdf.PDF](https://static.aminer.org/pdf/20170130/pdfs/oopsla/xcsyoq8gavfdiabv1epkpjje6wub9hwy.pdf)
  _Skipped because:_ Title/metadata are unclear, making it hard to validate relevance and quality; likely not a stable, well-identified reference for this lesson.

## Uncovered Gaps (1) — No Good Candidates Found
_Consider manually sourcing these, or run enrichment again with different search terms._

- Human oversight patterns in production agents (interrupts, approval gates, escalation, audit trails) and selection implications

## Reasoning
**Curator:** Priority was given to archival, citable papers that add missing decision/architecture and deployment/ops principles beyond the existing LangGraph/LangSmith docs and evaluation resources; most blog/vendor candidates were excluded due to weaker authority or likely redundancy.
**Reviewer:** The curator’s additions are directionally strong on architecture/deployment, but the library still needs at least one rigorous human-oversight paper to close the stated gap and make framework-selection criteria actionable for approval/interrupt/audit workflows.
