# Curation Report: Evaluation and Benchmarks
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-09 16:18
**Library:** 8 existing → 19 sources (11 added, 7 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (11)
- **[reference_doc]** [lm-evaluation-harness/docs/interface.md at big-refactor · EleutherAI/lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness/blob/big-refactor/docs/interface.md)
  This is the most direct, implementation-adjacent reference among the candidates for answering “how do I run this eval exactly?” questions with concrete flags and expected behaviors tied to the de facto standard harness.
- **[paper]** [A Systematic Study of Position Bias in LLM-as-a-Judge - arXiv.org](https://arxiv.org/abs/2406.07791)
  Adds a rigorous, step-by-step methodology for diagnosing and quantifying judge bias—exactly what a tutor needs to explain why LLM-as-judge can fail and how to validate/correct it.
- **[benchmark]** [Chatbot Arena: Benchmarking LLMs in the Wild with Elo Ratings](https://www.lmsys.org/blog/2023-05-03-arena/)
  Provides canonical, citable grounding for Chatbot Arena numbers and the evaluation design (pairwise preference aggregation into Elo), useful for “show me the numbers” and methodology discussions.
- **[paper]** [Evaluating Large Language Models Trained on Code](https://arxiv.org/pdf/2107.03374.pdf)
  This is the canonical place many later works cite for pass@k computation details; it directly fills the missing “metric formulas from trajectories/samples” need.
- **[reference_doc]** [Evals API Use-case - Monitoring stored completions](https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring)
  Even if tutorial-like, it is one of the few official, end-to-end examples of an evaluation/observability pipeline with a traceable process that matches the unfilled deployment-case need.
- **[paper]** [CMMLU: Measuring Massive Multitask Language Understanding in Chinese](https://aclanthology.org/2024.findings-acl.671.pdf)
  The library has MMLU (2009.03300) but lacks additional canonical benchmark tables with concrete numbers; CMMLU adds citable empirical results and protocol details for a major derivative benchmark.
- **[paper]** [MMLU-CF: A Contamination-free Multi-task Language Understanding Benchmark](https://aclanthology.org/2025.acl-long.656.pdf)
  This directly strengthens the “benchmark numbers with settings/model versions” need by addressing a core evaluation pitfall (data contamination) with concrete reported deltas.
- **[paper]** [Evaluating Large Language Models Trained on Code](https://arxiv.org/pdf/2107.03374.pdf) *(promoted by reviewer)*
  This is the canonical place many later works cite for pass@k computation details; it directly fills the missing “metric formulas from trajectories/samples” need.
- **[reference_doc]** [Evals API Use-case - Monitoring stored completions](https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring) *(promoted by reviewer)*
  Even if tutorial-like, it is one of the few official, end-to-end examples of an evaluation/observability pipeline with a traceable process that matches the unfilled deployment-case need.
- **[paper]** [CMMLU: Measuring Massive Multitask Language Understanding in Chinese](https://aclanthology.org/2024.findings-acl.671.pdf) *(promoted by reviewer)*
  The library has MMLU (2009.03300) but lacks additional canonical benchmark tables with concrete numbers; CMMLU adds citable empirical results and protocol details for a major derivative benchmark.
- **[paper]** [MMLU-CF: A Contamination-free Multi-task Language Understanding Benchmark](https://aclanthology.org/2025.acl-long.656.pdf) *(promoted by reviewer)*
  This directly strengthens the “benchmark numbers with settings/model versions” need by addressing a core evaluation pitfall (data contamination) with concrete reported deltas.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** — [[PDF] Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena - arXiv](https://arxiv.org/pdf/2306.05685.pdf)
  _Skipped because:_ Already present in the existing library (arxiv-abs-2306-05685), so adding it would be redundant.
- **Evals API Use-case - Detecting prompt regressions** — [Evals API Use-case - Detecting prompt regressions](https://developers.openai.com/cookbook/examples/evaluation/use-cases/regression)
  _Skipped because:_ Strong practical workflow, but the candidate set lacks a clearly more authoritative, metrics-and-impact-heavy production case study; this is more of a tutorial than a detailed observability/trajectory schema case study.

## Reasoning
**Curator:** Selections prioritize authoritative, citable sources that directly address missing capabilities: a concrete evaluation harness interface for precise execution details, a rigorous methodology paper for LLM-as-judge bias/validation, and the canonical Chatbot Arena benchmark write-up for empirical grounding. Other needs remain unfilled because the provided candidates don’t include primary metric-definition papers, HumanEval-specific empirical tables, or a truly metrics-driven production observability case study.
**Reviewer:** The curator’s additions are strong, but the library still needs at least one primary-source metric-formula reference (pass@k) and more canonical benchmark tables plus a concrete eval/observability pipeline example.

---

# Curation Report: Streaming, Debugging, and Observability in LangGraph
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:33
**Library:** 28 existing → 50 sources (22 added, 13 downloaded)
**Candidates evaluated:** 40
**Reviewer verdict:** needs_additions

## Added (22)
- **[explainer]** [Building LangGraph: Designing an Agent Runtime from first principles](https://blog.langchain.com/building-langgraph/)
  This is the most authoritative, end-to-end narrative of how/why LangGraph’s execution and streaming were designed, giving the tutor a principled explanation to pair with API-level details.
- **[reference_doc]** [Reliable streaming and efficient state management in LangGraph](https://changelog.langchain.com/announcements/reliable-streaming-and-efficient-state-management-in-langgraph)
  Changelog announcements are often the only place where practical guarantees and operationally relevant behavior changes are stated explicitly, which is crucial for debugging/replay expectations.
- **[reference_doc]** [Tracing SDK - OpenTelemetry](https://opentelemetry.io/docs/specs/otel/trace/sdk/)
  This provides the neutral, standards-based baseline needed to build a feature matrix and to explain how correlation IDs, sampling, and export pipelines work across vendors.
- **[explainer]** [Open vs. Closed Source](https://arize.com/docs/phoenix/resources/frequently-asked-questions/open-source-langsmith-alternative-arize-phoenix-vs.-langsmith)
  Adds an explicit, vendor-authored comparison that complements the OTel spec baseline and helps the tutor discuss tradeoffs (open-source vs managed, integration expectations).
- **[reference_doc]** [langgraph/how-tos/configuration/ #702 - GitHub (How to stream events / configuration)](https://github.com/langchain-ai/langgraph/discussions/702)
  Even if it’s “thin,” this is exactly the kind of canonical, parameter-level guidance that fills the missing API-reference gap around config wiring and streaming modes.
- **[code]** [Websocket implementation · langchain-ai/langgraph · Discussion #2028](https://github.com/langchain-ai/langgraph/discussions/2028)
  This directly addresses the missing end-to-end transport layer examples (SSE/WebSockets) that tutors need to teach real app integration beyond the core graph.stream API.
- **[code]** [LangGraph Streaming FastAPI (GitHub repo)](https://github.com/sheikhhanif/LangGraph_Streaming)
  A working repo is higher teaching value than prose: it gives a concrete baseline for SSE/WebSocket streaming and can be extended to show safe state exposure/redaction.
- **[reference_doc]** [Streaming with events stream API using FastAPI #17240 - GitHub (langchain discussion)](https://github.com/langchain-ai/langchain/discussions/17240)
  This is a pragmatic “glue” reference that often contains the exact integration gotchas (async iteration, response streaming) missing from official docs.
- **[reference_doc]** [graph stream with stream_mode=updates miss tool messages when using tools that return Command · Issue #2831 · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/issues/2831)
  For debugging/observability lessons, known failure modes and semantic gaps in streaming modes are crucial; this issue documents a concrete mismatch that a tutor should warn about.
- **[reference_doc]** [recursionLimit not honoured when sent via useStream · Issue #1482 · langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs/issues/1482)
  Even though it’s JS-focused, it surfaces a high-impact config/streaming pitfall (recursion_limit propagation) that maps to the broader lesson on config keys, defaults, and debugging unexpected control-flow.
- **[reference_doc]** [Where to add config to streamEvents? · Issue #318 · langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs/issues/318)
  This is exactly the “thin but precise” reference material that helps a tutor answer ‘where does config go?’ questions with specificity.
- **[reference_doc]** [streamEvents - How can I only stream the last node in the ... · Issue #320 · langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs/issues/320)
  Filtering streamed events by node/subgraph is a core teaching concept for observability; this issue captures real user intent and the practical constraints/solutions.
- **[reference_doc]** [Streaming API - Docs by LangChain (LangSmith)](https://docs.langchain.com/langsmith/streaming)
  The lesson is streaming + observability; this page provides the official counterpart for how streaming interacts with LangSmith runs, which helps connect event streaming to tracing semantics.
- **[reference_doc]** [langgraph/how-tos/configuration/ #702 - GitHub (How to stream events / configuration)](https://github.com/langchain-ai/langgraph/discussions/702) *(promoted by reviewer)*
  Even if it’s “thin,” this is exactly the kind of canonical, parameter-level guidance that fills the missing API-reference gap around config wiring and streaming modes.
- **[code]** [Websocket implementation · langchain-ai/langgraph · Discussion #2028](https://github.com/langchain-ai/langgraph/discussions/2028) *(promoted by reviewer)*
  This directly addresses the missing end-to-end transport layer examples (SSE/WebSockets) that tutors need to teach real app integration beyond the core graph.stream API.
- **[code]** [LangGraph Streaming FastAPI (GitHub repo)](https://github.com/sheikhhanif/LangGraph_Streaming) *(promoted by reviewer)*
  A working repo is higher teaching value than prose: it gives a concrete baseline for SSE/WebSocket streaming and can be extended to show safe state exposure/redaction.
- **[reference_doc]** [Streaming with events stream API using FastAPI #17240 - GitHub (langchain discussion)](https://github.com/langchain-ai/langchain/discussions/17240) *(promoted by reviewer)*
  This is a pragmatic “glue” reference that often contains the exact integration gotchas (async iteration, response streaming) missing from official docs.
- **[reference_doc]** [graph stream with stream_mode=updates miss tool messages when using tools that return Command · Issue #2831 · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/issues/2831) *(promoted by reviewer)*
  For debugging/observability lessons, known failure modes and semantic gaps in streaming modes are crucial; this issue documents a concrete mismatch that a tutor should warn about.
- **[reference_doc]** [recursionLimit not honoured when sent via useStream · Issue #1482 · langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs/issues/1482) *(promoted by reviewer)*
  Even though it’s JS-focused, it surfaces a high-impact config/streaming pitfall (recursion_limit propagation) that maps to the broader lesson on config keys, defaults, and debugging unexpected control-flow.
- **[reference_doc]** [Where to add config to streamEvents? · Issue #318 · langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs/issues/318) *(promoted by reviewer)*
  This is exactly the “thin but precise” reference material that helps a tutor answer ‘where does config go?’ questions with specificity.
- **[reference_doc]** [streamEvents - How can I only stream the last node in the ... · Issue #320 · langchain-ai/langgraphjs](https://github.com/langchain-ai/langgraphjs/issues/320) *(promoted by reviewer)*
  Filtering streamed events by node/subgraph is a core teaching concept for observability; this issue captures real user intent and the practical constraints/solutions.
- **[reference_doc]** [Streaming API - Docs by LangChain (LangSmith)](https://docs.langchain.com/langsmith/streaming) *(promoted by reviewer)*
  The lesson is streaming + observability; this page provides the official counterpart for how streaming interacts with LangSmith runs, which helps connect event streaming to tracing semantics.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **langgraph/docs/docs/cloud/how-tos/stream_events.md at main ·** — [langgraph/docs/docs/cloud/how-tos/stream_events.md at main · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/blob/main/docs/docs/cloud/how-tos/stream_events.md)
  _Skipped because:_ Useful how-to, but it does not reliably serve as an API reference for the full event schema/types, ordering guarantees, buffering/backpressure, and defaults the tutor needs for precision.
- **Implementing Compliant AI Tracing with LangSmith | Haitham S** — [Implementing Compliant AI Tracing with LangSmith | Haitham Shahin](https://hshahin.com/blog/langsmith-tracing-redaction/)
  _Skipped because:_ Strong practical guidance on redaction/compliance, but it’s third-party and narrower than a structured, multi-tool feature matrix or an official LangSmith spec/reference.

## Reasoning
**Curator:** Selections prioritize authoritative, durable references: (1) first-party LangGraph design rationale and reliability notes for execution/streaming mechanics, and (2) standards-based OpenTelemetry tracing specs plus a concrete Phoenix-vs-LangSmith comparison to support structured observability tradeoff discussions. The remaining gaps require more explicit API-schema references and runnable full-stack streaming examples than the provided candidates contain.
**Reviewer:** The library is strong on high-level LangGraph/LangSmith concepts, but it still needs a few “thin but precise” GitHub/official references and runnable FastAPI/SSE/WebSocket examples to cover event schema/config gotchas and real-world streaming integration.

---

# Curation Report: Real-World Agent Use Cases and Production Patterns
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:35
**Library:** 28 existing → 44 sources (16 added, 11 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (16)
- **[reference_doc]** [Streaming events | OpenAI API Reference](https://platform.openai.com/docs/api-reference/responses-streaming)
  Gives authoritative, citable details for how production streaming works (what events arrive, in what shape), enabling the tutor to answer precise questions about event handling, partial outputs, and tool-call streaming.
- **[reference_doc]** [Structured model outputs - OpenAI API](https://platform.openai.com/docs/guides/structured-outputs/json-mode)
  Complements streaming by covering the other half of production tool use: schema adherence and structured output constraints, which are frequently asked about when building reliable agents.
- **[benchmark]** [SpecTool: A Benchmark for Characterizing Errors in Tool-Use LLMs](https://ar5iv.labs.arxiv.org/html/2411.13547)
  Directly supports teaching reliability engineering for agents by providing concrete, categorized error statistics that map to real production mitigations (validation, retries, constrained decoding, tool selection checks).
- **[benchmark]** [[2308.03688] AgentBench: Evaluating LLMs as Agents - arXiv](https://arxiv.org/abs/2308.03688)
  Adds broad, quantitative agent performance data and diagnostic analyses that help the tutor explain how multi-step interaction degrades reliability and what to measure (round limits, completion distributions).
- **[explainer]** [Background Coding Agents: Predictable Results Through Strong ...](https://engineering.atspotify.com/2025/12/feedback-loops-background-coding-agents-part-3)
  Provides an industry case study with actionable architecture lessons (verification gates, iterative refinement, failure containment) that translate directly into production patterns for coding agents.
- **[explainer]** [Spotify's Journey with Our Background Coding Agent (Honk, Part 1)](https://engineering.atspotify.com/2025/11/spotifys-background-coding-agent-part-1)
  Adds a real-world deployment story that helps the tutor teach end-to-end production concerns (workflow integration, human-in-the-loop review, acceptable failure modes) beyond lab benchmarks.
- **[paper]** [Evaluating Large Language Models Trained on Code (Codex paper)](https://arxiv.org/abs/2107.03374)
  The library lacks a canonical, citable source for pass@k and related offline evaluation methodology; this paper is the standard reference and is more valuable than an abstract-only entry.
- **[paper]** [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf)
  Unfilled needs explicitly call for calibration/reliability metrics; this is the seminal, equation-heavy reference used across ML and is directly reusable for agent confidence/score calibration discussions.
- **[reference_doc]** [Streaming support | OpenAI API Reference](https://platform.openai.com/docs/api-reference/streaming)
  Even if thinner than the event-type page, this is still the canonical place for parameter names/defaults and is exactly the kind of spec-like citation needed when answering precise production questions.
- **[reference_doc]** [Streaming Messages - Anthropic API Docs](https://docs.anthropic.com/en/api/messages-streaming?debug_url=1&debug=1&debug=true)
  The lesson is about real-world production patterns; having at least one additional official streaming spec enables the tutor to teach provider-agnostic streaming handlers and compare event semantics.
- **[reference_doc]** [Fine-grained tool streaming - Anthropic Docs](https://docs.anthropic.com/ja/docs/agents-and-tools/tool-use/fine-grained-tool-streaming)
  Tool-call streaming is a core production concern for agents; this page provides concrete, citable details about incremental tool-use payloads that complement OpenAI’s streaming reference and improves concept coverage.
- **[paper]** [Evaluating Large Language Models Trained on Code (Codex paper)](https://arxiv.org/abs/2107.03374) *(promoted by reviewer)*
  The library lacks a canonical, citable source for pass@k and related offline evaluation methodology; this paper is the standard reference and is more valuable than an abstract-only entry.
- **[paper]** [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf) *(promoted by reviewer)*
  Unfilled needs explicitly call for calibration/reliability metrics; this is the seminal, equation-heavy reference used across ML and is directly reusable for agent confidence/score calibration discussions.
- **[reference_doc]** [Streaming support | OpenAI API Reference](https://platform.openai.com/docs/api-reference/streaming) *(promoted by reviewer)*
  Even if thinner than the event-type page, this is still the canonical place for parameter names/defaults and is exactly the kind of spec-like citation needed when answering precise production questions.
- **[reference_doc]** [Streaming Messages - Anthropic API Docs](https://docs.anthropic.com/en/api/messages-streaming?debug_url=1&debug=1&debug=true) *(promoted by reviewer)*
  The lesson is about real-world production patterns; having at least one additional official streaming spec enables the tutor to teach provider-agnostic streaming handlers and compare event semantics.
- **[reference_doc]** [Fine-grained tool streaming - Anthropic Docs](https://docs.anthropic.com/ja/docs/agents-and-tools/tool-use/fine-grained-tool-streaming) *(promoted by reviewer)*
  Tool-call streaming is a core production concern for agents; this page provides concrete, citable details about incremental tool-use payloads that complement OpenAI’s streaming reference and improves concept coverage.

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Structured Outputs - OpenAI API** — [Structured Outputs - OpenAI API](https://platform.openai.com/docs/guides/structured-outputs/example-response)
  _Skipped because:_ Useful examples, but the JSON-mode guide is the more generally reusable spec-style reference for constraints and enforcement.
- **Streaming API responses - OpenAI API** — [Streaming API responses - OpenAI API](https://platform.openai.com/docs/guides/streaming-responses?api-mode=responses)
  _Skipped because:_ Good tutorial framing, but the API reference page is more precise for enumerating event fields/types the tutor needs to cite.
- **AgentBench: Evaluating LLMs as Agents - arXiv** — [AgentBench: Evaluating LLMs as Agents - arXiv](https://arxiv.org/html/2308.03688v3)
  _Skipped because:_ Same work as the arXiv abstract entry; kept the canonical arXiv URL for stable citation.
- **ToolBench: LLM Tool-Use Benchmark - Emergent Mind** — [ToolBench: LLM Tool-Use Benchmark - Emergent Mind](https://www.emergentmind.com/topics/toolbench)
  _Skipped because:_ Secondary aggregator rather than the primary paper/code; better to cite the original benchmark publication directly.
- **Preprint** — [Preprint](https://lsh.plus/-lshwebsite/assets/publications/arxiv_toolllm/paper.pdf)
  _Skipped because:_ The candidate metadata appears mismatched/duplicative in the provided list; SpecTool and AgentBench more clearly match the stated empirical reliability needs from the candidates.

## Reasoning
**Curator:** Selections prioritize authoritative API specs for precise parameter/event details, plus benchmarks with quantitative tool/agent reliability data and a concrete industry deployment narrative for production patterns. Needs not well-covered by the provided candidates (formulas/statistics and rigorous orchestration comparisons) are left unfilled with targeted search hints.
**Reviewer:** The curation is strong on agent reliability/observability, but it should add canonical formula sources for pass@k and calibration metrics plus a couple of thin-but-authoritative streaming reference pages (including cross-provider tool-streaming) to better cover production evaluation and event-handling specifics.

---

# Curation Report: Capstone: Designing and Building a Production-Ready Agent
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:37
**Library:** 28 existing → 43 sources (15 added, 9 downloaded)
**Candidates evaluated:** 51
**Reviewer verdict:** needs_additions

## Added (15)
- **[reference_doc]** [How to use the REST API - Docs by LangChain](https://docs.langchain.com/langsmith/run-evals-api-only)
  This is the most directly operational/SDK-adjacent candidate, giving concrete API surface details the tutor can cite when teaching production evaluation automation and CI-style eval runs.
- **[reference_doc]** [Trace with API - Docs by LangChain](https://docs.langchain.com/langsmith/trace-with-api)
  Complements eval APIs with the production tracing side: how traces are represented and sent, which is essential for teaching observability, debugging, and auditability workflows.
- **[benchmark]** [[2308.03688] AgentBench: Evaluating LLMs as Agents](https://arxiv.org/abs/2308.03688)
  Provides citable, multi-domain empirical results for agentic behavior (not just single-turn QA), helping the tutor ground discussions of end-to-end agent performance and failure modes.
- **[benchmark]** [WebArena: A Realistic Web Environment for Building Autonomous Agents](https://arxiv.org/abs/2307.13854)
  Adds concrete numbers and a well-specified environment for long-horizon tool use (web navigation/actions), useful for teaching evaluation design, brittleness, and reliability in production-like settings.
- **[explainer]** [From prototype to production-ready agentic AI solution: A use case ...](https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics)
  While not a formal benchmark, it offers a concrete, production-oriented comparison framing (durability/replay/retries) that helps teach why workflow engines differ from agent orchestrators.
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550.pdf)
  This is a seminal retrieval paper whose value is in the exact loss/objective and training pipeline; it directly fills the missing “DPR contrastive loss” formula requirement.
- **[paper]** [The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries](https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf)
  MMR is frequently referenced in production RAG/agent retrieval stacks; this is the canonical source with the exact formula and rationale, not just secondary blog explanations.
- **[reference_doc]** [The Probabilistic Relevance Framework: BM25 and Beyond (Robertson & Zaragoza / CS276 handout)](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf)
  Even as a lecture handout, it’s a compact, citable formula reference that directly fills the missing BM25 equation need and is easier to teach from than scattered web summaries.
- **[reference_doc]** [LangSmith Evaluation (Docs by LangChain)](https://docs.langchain.com/langsmith/evaluation)
  It was rejected as “conceptual,” but for production readiness the exact evaluation object model and configuration knobs are reference-critical alongside the REST API pages.
- **[reference_doc]** [Manage datasets (Docs by LangChain)](https://docs.langchain.com/langsmith/datasets)
  This is “thin” by design but provides the concrete dataset operations and identifiers that production CI-style eval pipelines depend on; it closes a practical gap left by only having eval/trace endpoints.
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering](https://aclanthology.org/2020.emnlp-main.550.pdf) *(promoted by reviewer)*
  This is a seminal retrieval paper whose value is in the exact loss/objective and training pipeline; it directly fills the missing “DPR contrastive loss” formula requirement.
- **[paper]** [The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries](https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf) *(promoted by reviewer)*
  MMR is frequently referenced in production RAG/agent retrieval stacks; this is the canonical source with the exact formula and rationale, not just secondary blog explanations.
- **[reference_doc]** [The Probabilistic Relevance Framework: BM25 and Beyond (Robertson & Zaragoza / CS276 handout)](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf) *(promoted by reviewer)*
  Even as a lecture handout, it’s a compact, citable formula reference that directly fills the missing BM25 equation need and is easier to teach from than scattered web summaries.
- **[reference_doc]** [LangSmith Evaluation (Docs by LangChain)](https://docs.langchain.com/langsmith/evaluation) *(promoted by reviewer)*
  It was rejected as “conceptual,” but for production readiness the exact evaluation object model and configuration knobs are reference-critical alongside the REST API pages.
- **[reference_doc]** [Manage datasets (Docs by LangChain)](https://docs.langchain.com/langsmith/datasets) *(promoted by reviewer)*
  This is “thin” by design but provides the concrete dataset operations and identifiers that production CI-style eval pipelines depend on; it closes a practical gap left by only having eval/trace endpoints.

## Near-Misses (6) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Manage datasets - Docs by LangChain** — [Manage datasets - Docs by LangChain](https://docs.langchain.com/langsmith/manage-datasets)
  _Skipped because:_ Useful operationally, but less critical than trace/eval API references for production operations and doesn’t address the requested LangGraph Cloud deployment/auth/rate-limit specifics.
- **LangSmith Evaluation - Docs by LangChain** — [LangSmith Evaluation - Docs by LangChain](https://docs.langchain.com/langsmith/evaluation)
  _Skipped because:_ Good conceptual overview, but the API-only REST reference is more precise/citable for production automation.
- **Evaluation concepts - Docs by LangChain** — [Evaluation concepts - Docs by LangChain](https://docs.langchain.com/langsmith/evaluation-concepts)
  _Skipped because:_ Primarily conceptual; doesn’t add the concrete endpoint/payload details needed for the API_REFERENCE gap.
- **Temporal + LangGraph: A Two-Layer Architecture for Multi- ..** — [Temporal + LangGraph: A Two-Layer Architecture for Multi- ...](https://www.anup.io/temporal-langgraph-a-two-layer-architecture-for-multi-agent-coordination/)
  _Skipped because:_ Potentially useful, but it’s a third-party blog; the Temporal-hosted use case is a more authoritative source for the same comparison narrative.
- **AI Workflow Orchestration Platforms: 2026 Comparison** — [AI Workflow Orchestration Platforms: 2026 Comparison](https://www.digitalapplied.com/blog/ai-workflow-orchestration-platforms-comparison)
  _Skipped because:_ Likely broad and marketing-oriented; less trustworthy for precise criteria like determinism/replayability/state semantics than vendor or peer-reviewed sources.
- **A Real-world Task Benchmark for Evaluating LLM Agent ...** — [A Real-world Task Benchmark for Evaluating LLM Agent ...](https://arxiv.org/abs/2512.24565)
  _Skipped because:_ Promising, but the candidate snippet appears mismatched/duplicative (shows AgentBench text), making it hard to verify it adds distinct benchmark tables beyond the confirmed AgentBench/WebArena picks.

## Reasoning
**Curator:** Selections prioritize the most authoritative and citable candidates that directly add operational API specificity (LangSmith REST/trace APIs) and concrete agent benchmark tables (AgentBench, WebArena), plus one vendor-authored orchestration comparison pattern (Temporal + LangGraph) to partially address framework tradeoffs.
**Reviewer:** The library is strong on agent evaluation/observability, but it still lacks canonical retrieval formulas (BM25/DPR/MMR) and a couple of “thin but essential” LangSmith dataset/eval docs needed to teach production automation precisely.

---

# Curation Report: Framework Selection Criteria: Choosing the Right Tool for the Job
**Topic:** `evaluation-benchmarks` | **Date:** 2026-04-10 19:39
**Library:** 28 existing → 53 sources (25 added, 14 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (25)
- **[reference_doc]** [Activity Operations | Temporal Platform Documentation](https://docs.temporal.io/activity-operations)
  Gives authoritative, citable API-level definitions and operational defaults/behaviors for retries and timeouts—core knobs when using Temporal as a durable agent backbone.
- **[explainer]** [Event History walkthrough with the Python SDK - Temporal Docs](https://docs.temporal.io/encyclopedia/event-history/event-history-python)
  Provides a teachable, procedural explanation of event-sourced durable execution and deterministic replay—key concepts for justifying framework selection for long-running, interruptible agents.
- **[explainer]** [Architecture](https://docs.temporal.io/ai-cookbook/human-in-the-loop-python)
  Adds an implementation-oriented reference for human approval/interrupt mechanics in a production-grade workflow engine, directly mapping to agent oversight requirements.
- **[reference_doc]** [Temporal Docs — Activity retries (RetryPolicy fields, defaults, backoff behavior)](https://docs.temporal.io/activities#activity-retries)
  The current Temporal additions cover timeouts and replay, but framework selection criteria often hinge on retry semantics; this page is “thin” but provides the precise knobs and defaults needed for a criteria matrix.
- **[reference_doc]** [Temporal Docs — Workflow timeouts (Execution/Run/Task timeouts) and semantics](https://docs.temporal.io/workflows#workflow-timeouts)
  To teach selection criteria (durability, long-running behavior), you need both activity and workflow timeout semantics; this is a missing API-level complement to the Activity Operations page.
- **[reference_doc]** [AWS Step Functions Developer Guide — Amazon States Language (ASL) specification](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html)
  This is the canonical reference needed to compare orchestration expressiveness and failure handling against Temporal/LangGraph; it’s exactly the kind of “thin but precise” spec the library is missing.
- **[reference_doc]** [AWS Step Functions Developer Guide — Error handling (Retry/Catch) semantics](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html)
  Directly fills the unfilled need for official retry policy semantics and parameter names for Step Functions—critical for a criteria-based comparison and for teaching reliability tradeoffs.
- **[reference_doc]** [Azure Durable Functions — Overview (durable orchestrations, replay, deterministic constraints)](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview)
  Durable Functions is explicitly in the unfilled comparison set; this page provides the authoritative conceptual model needed to compare replay-based durability vs Temporal and agent frameworks.
- **[reference_doc]** [Azure Durable Functions — Timers (durable sleep/wait) and behavior](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-timers)
  Human-approval/wait is a core selection criterion; this is the official, citable reference for implementing HITL waits in Durable Functions.
- **[reference_doc]** [Azure Durable Functions — External events (raise/wait) for human-in-the-loop signaling](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-external-events)
  Directly addresses the unfilled need for official HITL interrupt/approval primitives in Azure Durable Functions, enabling apples-to-apples comparison with Temporal signals/queries.
- **[reference_doc]** [AWS Step Functions Developer Guide — Quotas and limits](https://docs.aws.amazon.com/step-functions/latest/dg/limits.html)
  The library lacks official “numbers pages” for orchestration frameworks; quotas/limits are often decisive in framework selection and are best sourced from AWS docs.
- **[benchmark]** [A Comprehensive Benchmark to Evaluate Agent Architectures in ... (Agent architecture benchmark)](https://arxiv.org/html/2509.10769v1)
  Even if only the abstract was previewed, this is exactly the kind of empirical, architecture-level evaluation the library is missing for “framework/orchestration strategy” selection; it likely contains the comparative tables needed for teaching tradeoffs.
- **[paper]** [How Do LLMs Fail In Agentic Scenarios? A Qualitative Analysis of ...](https://arxiv.org/html/2512.07497v2)
  Framework selection criteria needs a measurement vocabulary; this paper appears to provide concrete metrics and evaluation procedure that can be reused to compare orchestration approaches under failures.
- **[reference_doc]** [Temporal Docs — Events reference (authoritative event history event types)](https://docs.temporal.io/reference/events)
  Rejected as less pedagogical, but it’s precisely the kind of canonical reference needed when teaching durability/auditability and when mapping observability tooling to event history.
- **[reference_doc]** [Temporal Docs — Activity retries (RetryPolicy fields, defaults, backoff behavior)](https://docs.temporal.io/activities#activity-retries) *(promoted by reviewer)*
  The current Temporal additions cover timeouts and replay, but framework selection criteria often hinge on retry semantics; this page is “thin” but provides the precise knobs and defaults needed for a criteria matrix.
- **[reference_doc]** [Temporal Docs — Workflow timeouts (Execution/Run/Task timeouts) and semantics](https://docs.temporal.io/workflows#workflow-timeouts) *(promoted by reviewer)*
  To teach selection criteria (durability, long-running behavior), you need both activity and workflow timeout semantics; this is a missing API-level complement to the Activity Operations page.
- **[reference_doc]** [AWS Step Functions Developer Guide — Amazon States Language (ASL) specification](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-amazon-states-language.html) *(promoted by reviewer)*
  This is the canonical reference needed to compare orchestration expressiveness and failure handling against Temporal/LangGraph; it’s exactly the kind of “thin but precise” spec the library is missing.
- **[reference_doc]** [AWS Step Functions Developer Guide — Error handling (Retry/Catch) semantics](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-error-handling.html) *(promoted by reviewer)*
  Directly fills the unfilled need for official retry policy semantics and parameter names for Step Functions—critical for a criteria-based comparison and for teaching reliability tradeoffs.
- **[reference_doc]** [Azure Durable Functions — Overview (durable orchestrations, replay, deterministic constraints)](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-overview) *(promoted by reviewer)*
  Durable Functions is explicitly in the unfilled comparison set; this page provides the authoritative conceptual model needed to compare replay-based durability vs Temporal and agent frameworks.
- **[reference_doc]** [Azure Durable Functions — Timers (durable sleep/wait) and behavior](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-timers) *(promoted by reviewer)*
  Human-approval/wait is a core selection criterion; this is the official, citable reference for implementing HITL waits in Durable Functions.
- **[reference_doc]** [Azure Durable Functions — External events (raise/wait) for human-in-the-loop signaling](https://learn.microsoft.com/en-us/azure/azure-functions/durable/durable-functions-external-events) *(promoted by reviewer)*
  Directly addresses the unfilled need for official HITL interrupt/approval primitives in Azure Durable Functions, enabling apples-to-apples comparison with Temporal signals/queries.
- **[reference_doc]** [AWS Step Functions Developer Guide — Quotas and limits](https://docs.aws.amazon.com/step-functions/latest/dg/limits.html) *(promoted by reviewer)*
  The library lacks official “numbers pages” for orchestration frameworks; quotas/limits are often decisive in framework selection and are best sourced from AWS docs.
- **[benchmark]** [A Comprehensive Benchmark to Evaluate Agent Architectures in ... (Agent architecture benchmark)](https://arxiv.org/html/2509.10769v1) *(promoted by reviewer)*
  Even if only the abstract was previewed, this is exactly the kind of empirical, architecture-level evaluation the library is missing for “framework/orchestration strategy” selection; it likely contains the comparative tables needed for teaching tradeoffs.
- **[paper]** [How Do LLMs Fail In Agentic Scenarios? A Qualitative Analysis of ...](https://arxiv.org/html/2512.07497v2) *(promoted by reviewer)*
  Framework selection criteria needs a measurement vocabulary; this paper appears to provide concrete metrics and evaluation procedure that can be reused to compare orchestration approaches under failures.
- **[reference_doc]** [Temporal Docs — Events reference (authoritative event history event types)](https://docs.temporal.io/reference/events) *(promoted by reviewer)*
  Rejected as less pedagogical, but it’s precisely the kind of canonical reference needed when teaching durability/auditability and when mapping observability tooling to event history.

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Detecting Activity failures | Temporal Platform Documentatio** — [Detecting Activity failures | Temporal Platform Documentation](https://docs.temporal.io/encyclopedia/detecting-activity-failures)
  _Skipped because:_ Useful for failure taxonomy, but overlaps heavily with Activity Operations and is narrower for teaching the full API surface (timeouts + retries + execution semantics).
- **Temporal Events reference | Temporal Platform Documentation** — [Temporal Events reference | Temporal Platform Documentation](https://docs.temporal.io/references/events)
  _Skipped because:_ Authoritative event list, but less pedagogically effective than the event-history walkthrough for explaining replay mechanics step-by-step.
- **The Inner Workings of Temporal SDKs | Replay 2024** — [The Inner Workings of Temporal SDKs | Replay 2024](https://www.youtube.com/watch?v=XephqQtwPEE)
  _Skipped because:_ Potentially excellent depth, but video format is harder to cite for precise defaults/parameters compared to the written walkthrough and API docs.
- **AWS Step Functions vs Temporal: A Practical Developer Compar** — [AWS Step Functions vs Temporal: A Practical Developer Comparison](https://www.readysetcloud.io/blog/allen.helton/step-functions-vs-temporal/)
  _Skipped because:_ Helpful narrative comparison, but it is third-party and not a structured, criteria-mapped matrix across multiple frameworks (and may not be reliably citable for exact limits/defaults).
- **How to Build Human-in-the-Loop Oversight for AI Agents | Gal** — [How to Build Human-in-the-Loop Oversight for AI Agents | Galileo](https://galileo.ai/blog/human-in-the-loop-agent-oversight)
  _Skipped because:_ Good practical guidance, but it is marketing-oriented and not a primary, measurable production case study with concrete latency/cost/SLO outcomes.

## Reasoning
**Curator:** The selected additions prioritize authoritative, citable documentation and step-by-step mechanics for durable execution and HITL—core to framework selection—while leaving comparison matrices and cross-framework empirical benchmarks unfilled because the provided candidates are mostly third-party narratives without structured criteria or quantitative data.
**Reviewer:** The Temporal additions are strong, but the library still lacks the official Step Functions/Durable Functions API+limits pages and a couple of high-signal empirical benchmark/failure-metrics papers needed to teach framework selection with concrete parameters and numbers.
