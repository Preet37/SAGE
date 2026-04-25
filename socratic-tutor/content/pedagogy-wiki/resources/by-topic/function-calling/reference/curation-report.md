# Curation Report: Function Calling and Tool Use
**Topic:** `function-calling` | **Date:** 2026-04-09 16:20
**Library:** 5 existing → 19 sources (14 added, 9 downloaded)
**Candidates evaluated:** 50
**Reviewer verdict:** needs_additions

## Added (14)
- **[reference_doc]** [OpenAI Platform](https://platform.openai.com/docs/guides/structured-outputs/supported-schemas?context=ex2)
  This is the most directly citable spec-like page for what schema features are actually supported, which is essential for teaching precise guarantees and failure modes when designing tool/function schemas.
- **[reference_doc]** [Transports - Model Context Protocolmodelcontextprotocol.io › specification › basic › transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)
  This is an official MCP specification page with concrete, step-by-step transport behavior that a tutor can use to explain handshake/message flow and implementation details without relying on secondary summaries.
- **[benchmark]** [FunctionChat-Bench: Comprehensive Evaluation of ...](https://arxiv.org/html/2411.14054v1)
  Provides empirical measurements and structured rubrics/error categories that can be cited when discussing reliability (selection correctness, formatting/tool-call errors) and how to evaluate improvements.
- **[explainer]** [Beyond the Leaderboard: Unpacking Function Calling Evaluation](https://www.databricks.com/blog/unpacking-function-calling-eval)
  Adds practitioner-oriented guidance on measuring and improving tool-calling reliability, complementing academic benchmarks with actionable evaluation design and interpretation.
- **[reference_doc]** [Structured model outputs (Structured Outputs / JSON mode) — OpenAI API](https://platform.openai.com/docs/guides/structured-outputs/json-mode?context=without_parse)
  Even if the supported-schema subset page is the best spec for keywords, this page is the canonical “how to use it” reference with concrete parameters/behavior that a tutor needs when teaching implementation details and failure modes.
- **[reference_doc]** [Structured outputs — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)
  Cross-vendor grounding is valuable for teaching the general concept of schema-constrained tool inputs; this is official documentation with precise guarantees that complements OpenAI’s schema constraints.
- **[reference_doc]** [Fine-grained tool streaming — Claude API Docs](https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)
  This directly supports the unfilled “streaming tool-use loop” need with an authoritative, implementation-oriented description of how tool streaming works in practice.
- **[explainer]** [Handling invalid JSON in Anthropic's fine-grained tool streaming](https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming)
  While not official, it fills a key production gap the library still has: what to do when streamed tool arguments are invalid mid-flight—exactly the kind of operational detail needed for retries/backoff and robustness.
- **[benchmark]** [The Berkeley Function Calling Leaderboard (BFCL) — ICML Poster](https://icml.cc/virtual/2025/poster/46593)
  FunctionChat-Bench is good, but BFCL is a widely referenced complementary benchmark/leaderboard with concrete quantitative results that help teach evaluation design and compare failure modes across settings.
- **[reference_doc]** [Structured model outputs (Structured Outputs / JSON mode) — OpenAI API](https://platform.openai.com/docs/guides/structured-outputs/json-mode?context=without_parse) *(promoted by reviewer)*
  Even if the supported-schema subset page is the best spec for keywords, this page is the canonical “how to use it” reference with concrete parameters/behavior that a tutor needs when teaching implementation details and failure modes.
- **[reference_doc]** [Structured outputs — Claude API Docs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) *(promoted by reviewer)*
  Cross-vendor grounding is valuable for teaching the general concept of schema-constrained tool inputs; this is official documentation with precise guarantees that complements OpenAI’s schema constraints.
- **[reference_doc]** [Fine-grained tool streaming — Claude API Docs](https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming) *(promoted by reviewer)*
  This directly supports the unfilled “streaming tool-use loop” need with an authoritative, implementation-oriented description of how tool streaming works in practice.
- **[explainer]** [Handling invalid JSON in Anthropic's fine-grained tool streaming](https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming) *(promoted by reviewer)*
  While not official, it fills a key production gap the library still has: what to do when streamed tool arguments are invalid mid-flight—exactly the kind of operational detail needed for retries/backoff and robustness.
- **[benchmark]** [The Berkeley Function Calling Leaderboard (BFCL) — ICML Poster](https://icml.cc/virtual/2025/poster/46593) *(promoted by reviewer)*
  FunctionChat-Bench is good, but BFCL is a widely referenced complementary benchmark/leaderboard with concrete quantitative results that help teach evaluation design and compare failure modes across settings.

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Structured model outputs - OpenAI API** — [Structured model outputs - OpenAI API](https://platform.openai.com/docs/guides/structured-outputs/json-mode)
  _Skipped because:_ Useful overview, but the supported-schemas page is more specification-like for teaching exact constraints and schema keyword support.
- **Structured Outputs** — [Structured Outputs](https://platform.openai.com/docs/guides/structured-outputs?api-mode=responses)
  _Skipped because:_ Good general guide, but less focused on the precise schema subset/constraints than the supported-schemas reference.
- **Transports - Model Context Protocol** — [Transports - Model Context Protocol](https://modelcontextprotocol.io/specification/2025-03-26/basic/transports)
  _Skipped because:_ Appears to be an older dated version of the same spec section; the newer 2025-06-18 version is preferable as the primary reference.
- **Base Protocol** — [Base Protocol](https://modelcontextprotocol.info/specification/draft/basic/)
  _Skipped because:_ Draft/mirror site rather than the canonical modelcontextprotocol.io spec, so it is less authoritative for citation.
- **An Efficient Tool Learning Method via Parallel Tool Invocati** — [An Efficient Tool Learning Method via Parallel Tool Invocation - arXiv](https://arxiv.org/html/2501.12432v1)
  _Skipped because:_ Valuable for training methods and parallel invocation, but less directly aligned to the requested reliability metrics (validity/accuracy/error-recovery) than FunctionChat-Bench plus an eval-focused practitioner writeup.

## Reasoning
**Curator:** Selections prioritize canonical specs for schema constraints and MCP transport mechanics, plus the strongest available benchmark/evaluation sources for quantitative tool-calling reliability. The candidate set lacked truly authoritative production reference implementations and metric-rich real-world sandbox case studies, so those needs remain unfilled.
**Reviewer:** The curator’s core picks are strong, but the library should add a couple of thin-but-canonical structured-output docs plus at least one authoritative tool-streaming reference and a complementary benchmark with concrete reported numbers.

---

# Curation Report: The ReAct Pattern: Synergizing Reasoning and Acting
**Topic:** `function-calling` | **Date:** 2026-04-10 19:19
**Library:** 16 existing → 34 sources (18 added, 11 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (18)
- **[reference_doc]** [Compositional function calling](https://ai.google.dev/gemini-api/docs/function-calling)
  Adds official, parameter-level Gemini tool-calling semantics the tutor can cite when mapping ReAct 'Action/Observation' to provider APIs and explaining constraints/structure of tool calls.
- **[benchmark]** [ReSpAct: Harmonizing Reasoning, Speaking, and Acting ...](https://arxiv.org/html/2411.00927v1)
  Directly targets the missing benchmark/ablation need with concrete cross-task numbers and comparisons that help a tutor answer 'how much does ReAct help, and where?'.
- **[reference_doc]** [ReAct Agent — NVIDIA NeMo Agent Toolkit (1.3)](https://docs.nvidia.com/nemo/agent-toolkit/1.3/workflows/about/react-agent.html)
  Provides an authoritative, reproducible implementation reference beyond LangChain/LangGraph, useful for teaching concrete engineering patterns and debugging surfaces.
- **[benchmark]** [Results](https://blog.langchain.com/react-agent-benchmarking/)
  Adds practical, operations-oriented evidence (how to benchmark and what to measure) that complements academic tables and helps teach deployment tradeoffs.
- **[reference_doc]** [OpenAI API Docs — Tools (tool calling, tool_choice, parallel tool calls, structured outputs)](https://platform.openai.com/docs/guides/tools)
  The library cites OpenAI function calling, but the newer Tools docs are the canonical reference for current defaults/controls (including parallelism and structured outputs) that materially affect ReAct loop behavior.
- **[reference_doc]** [Anthropic Docs — Tool use (Claude)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
  One of the explicitly unfilled needs is Anthropic tool-use defaults/constraints; this is the primary citable source for implementing ReAct-style Action/Observation with Claude.
- **[reference_doc]** [Anthropic Docs — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)
  ReAct-style loops are token- and latency-heavy; prompt caching is a concrete, provider-official lever that helps teach deployment tradeoffs with measurable cost/latency impact.
- **[paper]** [ReAct: Synergizing Reasoning and Acting in Language Models (official paper)](https://arxiv.org/abs/2210.03629)
  Already included, but several candidate links are duplicates/mirrors; the arXiv version is the definitive citable artifact—keep this as the single canonical reference and avoid adding mirrors like blog reposts/DeepWiki.
- **[paper]** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2305.15334)
  The library lists the arXiv ID but not the title/role; this is one of the most-cited adjacent agent-loop patterns and is directly relevant to the unfilled ReAct-vs-Reflexion comparison need.
- **[benchmark]** [ReAct: Synergizing Reasoning and Acting in Language Models (v3 with updated experiments)](https://arxiv.org/abs/2210.03629v3)
  If the tutor needs to cite exact metrics/ablations, pinning a specific version (v3) avoids ambiguity when numbers differ across revisions.
- **[explainer]** [Google Research Blog — ReAct: Synergizing Reasoning and Acting in Language Models](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)
  While not a substitute for the paper, this is an authoritative, pedagogically clear companion that helps a Socratic tutor explain the intuition and mechanics without immediately diving into dense tables.
- **[reference_doc]** [OpenAI API Docs — Tools (tool calling, tool_choice, parallel tool calls, structured outputs)](https://platform.openai.com/docs/guides/tools) *(promoted by reviewer)*
  The library cites OpenAI function calling, but the newer Tools docs are the canonical reference for current defaults/controls (including parallelism and structured outputs) that materially affect ReAct loop behavior.
- **[reference_doc]** [Anthropic Docs — Tool use (Claude)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) *(promoted by reviewer)*
  One of the explicitly unfilled needs is Anthropic tool-use defaults/constraints; this is the primary citable source for implementing ReAct-style Action/Observation with Claude.
- **[reference_doc]** [Anthropic Docs — Prompt caching](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching) *(promoted by reviewer)*
  ReAct-style loops are token- and latency-heavy; prompt caching is a concrete, provider-official lever that helps teach deployment tradeoffs with measurable cost/latency impact.
- **[paper]** [ReAct: Synergizing Reasoning and Acting in Language Models (official paper)](https://arxiv.org/abs/2210.03629) *(promoted by reviewer)*
  Already included, but several candidate links are duplicates/mirrors; the arXiv version is the definitive citable artifact—keep this as the single canonical reference and avoid adding mirrors like blog reposts/DeepWiki.
- **[paper]** [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2305.15334) *(promoted by reviewer)*
  The library lists the arXiv ID but not the title/role; this is one of the most-cited adjacent agent-loop patterns and is directly relevant to the unfilled ReAct-vs-Reflexion comparison need.
- **[benchmark]** [ReAct: Synergizing Reasoning and Acting in Language Models (v3 with updated experiments)](https://arxiv.org/abs/2210.03629v3) *(promoted by reviewer)*
  If the tutor needs to cite exact metrics/ablations, pinning a specific version (v3) avoids ambiguity when numbers differ across revisions.
- **[explainer]** [Google Research Blog — ReAct: Synergizing Reasoning and Acting in Language Models](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/) *(promoted by reviewer)*
  While not a substitute for the paper, this is an authoritative, pedagogically clear companion that helps a Socratic tutor explain the intuition and mechanics without immediately diving into dense tables.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Combine built-in tools and function calling | Gemini API** — [Combine built-in tools and function calling | Gemini API](https://ai.google.dev/gemini-api/docs/tool-combination)
  _Skipped because:_ Useful for multi-tool setups, but the core function-calling doc is the more fundamental parameter/spec anchor for ReAct.
- **ReAct vs Plan-and-Execute: A Practical Comparison of LLM Age** — [ReAct vs Plan-and-Execute: A Practical Comparison of LLM Agent ...](https://dev.to/jamesli/react-vs-plan-and-execute-a-practical-comparison-of-llm-agent-patterns-4gh9)
  _Skipped because:_ Has practical comparisons but is not an authoritative/primary source and may not be reliably citable for defaults or rigorous criteria.
- **Optimizing Agentic Workflows using Meta-tools - arXiv** — [Optimizing Agentic Workflows using Meta-tools - arXiv](https://arxiv.org/html/2601.22037v2)
  _Skipped because:_ Strong for workflow optimization from traces, but it is not clearly a ReAct-specific production case study with concrete cost/latency/tool-call-rate metrics tied to a deployed system.

## Reasoning
**Curator:** Selections prioritize authoritative specs (Gemini function calling) and primary empirical evidence (ReSpAct benchmarks), plus implementation/benchmarking references from major tooling ecosystems (NeMo, LangChain) to improve both precision and teachable engineering practice. Generic or non-authoritative comparisons were excluded in favor of sources that are more citable and reproducible.
**Reviewer:** The core ReAct paper and LangGraph/Gemini coverage are solid, but the library still needs provider-official Anthropic tool-use references and at least one canonical adjacent-loop paper (Reflexion) to support structured comparisons and deployment-relevant constraints.

---

# Curation Report: Implementing a ReAct Agent with LangGraph
**Topic:** `function-calling` | **Date:** 2026-04-10 19:30
**Library:** 16 existing → 28 sources (12 added, 8 downloaded)
**Candidates evaluated:** 43
**Reviewer verdict:** needs_additions

## Added (12)
- **[reference_doc]** [compile | langgraph - LangChain Reference Docs](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)
  This is the most direct low-level entry point for precise semantics of how a StateGraph becomes an executable runtime, which is foundational for explaining reducers, routing, and execution behavior.
- **[reference_doc]** [Checkpointing | LangChain Reference](https://reference.langchain.com/python/langgraph/checkpoints/)
  Adds authoritative details needed to teach persistence, replay/resume, and how state is stored between steps—critical for real ReAct loops beyond toy examples.
- **[benchmark]** [[PDF] API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs](https://aclanthology.org/anthology-files/pdf/emnlp/2023.emnlp-main.187.pdf)
  Provides citable empirical numbers and a concrete benchmark methodology for iterative tool use, enabling the tutor to discuss failure modes and performance tradeoffs with evidence.
- **[reference_doc]** [LangSmith Observability - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/observability)
  Gives an official, actionable observability path for LangGraph agents, supporting instruction on debugging, monitoring, and operational controls in iterative execution.
- **[reference_doc]** [Graphs | LangChain Reference](https://reference.langchain.com/python/langgraph/graphs/)
  Even if “thin,” this is exactly the kind of authoritative API surface that clarifies defaults and failure modes for cyclic ReAct loops (infinite-loop prevention), which is core to teaching safe agent execution.
- **[reference_doc]** [CompiledStateGraph (LangGraph JS API Reference)](https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)
  The library currently anchors compile/runtime semantics mainly in Python; this fills cross-language precision for the compiled runtime object, which helps teach the conceptual contract independent of language.
- **[paper]** [ToolGen: Unified Tool Retrieval and Calling via Generation](https://arxiv.org/html/2410.03439v1)
  This is not just an abstract—it's a concrete method paper with an evaluation protocol and numbers that can support the lesson’s discussion of iterative tool-use performance and failure modes beyond ReAct itself.
- **[benchmark]** [Invocable APIs derived from NL2SQL datasets for LLM Tool-Calling (Live API Bench)](https://arxiv.org/pdf/2506.11266.pdf)
  Directly fills the need for specific quantitative comparisons on tool-calling in interactive environments, and provides a reproducible benchmark design that’s useful for teaching evaluation of ReAct-style loops.
- **[reference_doc]** [Graphs | LangChain Reference](https://reference.langchain.com/python/langgraph/graphs/) *(promoted by reviewer)*
  Even if “thin,” this is exactly the kind of authoritative API surface that clarifies defaults and failure modes for cyclic ReAct loops (infinite-loop prevention), which is core to teaching safe agent execution.
- **[reference_doc]** [CompiledStateGraph (LangGraph JS API Reference)](https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html) *(promoted by reviewer)*
  The library currently anchors compile/runtime semantics mainly in Python; this fills cross-language precision for the compiled runtime object, which helps teach the conceptual contract independent of language.
- **[paper]** [ToolGen: Unified Tool Retrieval and Calling via Generation](https://arxiv.org/html/2410.03439v1) *(promoted by reviewer)*
  This is not just an abstract—it's a concrete method paper with an evaluation protocol and numbers that can support the lesson’s discussion of iterative tool-use performance and failure modes beyond ReAct itself.
- **[benchmark]** [Invocable APIs derived from NL2SQL datasets for LLM Tool-Calling (Live API Bench)](https://arxiv.org/pdf/2506.11266.pdf) *(promoted by reviewer)*
  Directly fills the need for specific quantitative comparisons on tool-calling in interactive environments, and provides a reproducible benchmark design that’s useful for teaching evaluation of ReAct-style loops.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **GraphRecursionError | langgraph** — [GraphRecursionError | langgraph](https://reference.langchain.com/python/langgraph/errors/GraphRecursionError)
  _Skipped because:_ Useful for recursion_limit specifics, but narrower than the compile + checkpointing references for covering the broader runtime semantics the tutor is missing.
- **API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs** — [API-Bank: A Comprehensive Benchmark for Tool-Augmented LLMs](https://arxiv.org/abs/2304.08244)
  _Skipped because:_ Redundant with the ACL Anthology PDF version; the PDF is more directly usable as a stable, citable artifact.
- **Open Source Observability for LangGraph - Langfuse** — [Open Source Observability for LangGraph - Langfuse](https://langfuse.com/guides/cookbook/integration_langgraph)
  _Skipped because:_ Good practical integration guide, but the official LangSmith/LangChain observability docs are more authoritative for defaults and canonical tracing concepts.
- **AI Agent Frameworks: A Detailed Comparison** — [AI Agent Frameworks: A Detailed Comparison](https://www.turing.com/resources/ai-agent-frameworks)
  _Skipped because:_ Likely helpful but tends to be high-level/marketing-style; not clearly a rigorous feature matrix with verifiable details on determinism, persistence, and runtime semantics.

## Reasoning
**Curator:** Selections prioritize authoritative LangGraph reference docs for precise runtime/persistence semantics and a peer-reviewed benchmark (API-Bank) for citable tool-use performance data; remaining needs require either a vetted end-to-end repo or more rigorous comparative/production studies than the provided candidates.
**Reviewer:** The curator’s core picks are strong, but a few “thin” official LangGraph reference pages and two benchmark/method papers with concrete evaluation procedures and numbers should be added to cover runtime limits/error semantics and tool-use empirical grounding.
