# Curation Report: Agent Memory
**Topic:** `agent-memory` | **Date:** 2026-04-09 16:14
**Library:** 5 existing → 20 sources (15 added, 9 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (15)
- **[benchmark]** [[PDF] Evaluating Very Long-Term Conversational Memory of LLM Agents](https://aclanthology.org/2024.acl-long.747.pdf)
  Adds an established, memory-specific evaluation suite the tutor can cite when comparing memory strategies and discussing what “long-term conversational memory” means operationally and how it is measured.
- **[benchmark]** [LongBench: A Bilingual, Multitask Benchmark for Long Context Understanding](https://aclanthology.org/2024.acl-long.172.pdf)
  Provides widely cited benchmark structure and baseline numbers that can ground discussions of context-window vs retrieval/summarization approaches, even when not agent-specific.
- **[reference_doc]** [Responses | OpenAI API Reference](https://platform.openai.com/docs/api-reference/responses/list?lang=python)
  Gives the tutor citable, official parameter names and defaults relevant to implementing conversational memory and managing what is carried across turns.
- **[paper]** [The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries](https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf)
  Agent-memory curricula often mention MMR but lack a citable original equation and rationale; this paper is the canonical source and fills the missing mathematical formulation need.
- **[paper]** [BM25 and Beyond: Implementing and Evaluating a Search Engine (BM25 ranking functions compilation/implementation notes)](https://arxiv.org/pdf/0911.5046.pdf)
  The library lacks a primary/technical formula source for BM25; this provides explicit equations and implementation-oriented detail that a tutor can quote and derive from.
- **[explainer]** [Introduction to Information Retrieval (CS276) — BM25 etc. lecture notes](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf)
  Even if not a peer-reviewed paper, it’s an authoritative teaching artifact that makes the formulas teachable (definitions, intuition, parameter effects) and complements the more implementation-focused PDF.
- **[reference_doc]** [Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions)
  Thin official docs are precisely what a reference library needs for quoting parameter names/defaults; excluding this risks losing the most directly citable spec page for conversation-state handling.
- **[reference_doc]** [Create completion | OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions/create)
  The endpoint page is often more precise than the overview for implementers (exact payload shape); it’s valuable even if it overlaps with other API reference pages.
- **[paper]** [Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models](https://arxiv.org/html/2308.15022v3)
  This directly covers a core agent-memory mechanism (summarization-based memory) with an explicit algorithmic pipeline; it’s a high-value architecture/procedure source that complements retrieval-based memory.
- **[paper]** [The Use of MMR, Diversity-Based Reranking for Reordering Documents and Producing Summaries](https://www.cs.cmu.edu/~jgc/publication/MMR_DiversityBased_Reranking_SIGIR_1998.pdf) *(promoted by reviewer)*
  Agent-memory curricula often mention MMR but lack a citable original equation and rationale; this paper is the canonical source and fills the missing mathematical formulation need.
- **[paper]** [BM25 and Beyond: Implementing and Evaluating a Search Engine (BM25 ranking functions compilation/implementation notes)](https://arxiv.org/pdf/0911.5046.pdf) *(promoted by reviewer)*
  The library lacks a primary/technical formula source for BM25; this provides explicit equations and implementation-oriented detail that a tutor can quote and derive from.
- **[explainer]** [Introduction to Information Retrieval (CS276) — BM25 etc. lecture notes](https://web.stanford.edu/class/cs276/handouts/lecture12-bm25etc.pdf) *(promoted by reviewer)*
  Even if not a peer-reviewed paper, it’s an authoritative teaching artifact that makes the formulas teachable (definitions, intuition, parameter effects) and complements the more implementation-focused PDF.
- **[reference_doc]** [Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions) *(promoted by reviewer)*
  Thin official docs are precisely what a reference library needs for quoting parameter names/defaults; excluding this risks losing the most directly citable spec page for conversation-state handling.
- **[reference_doc]** [Create completion | OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions/create) *(promoted by reviewer)*
  The endpoint page is often more precise than the overview for implementers (exact payload shape); it’s valuable even if it overlaps with other API reference pages.
- **[paper]** [Recursively Summarizing Enables Long-Term Dialogue Memory in Large Language Models](https://arxiv.org/html/2308.15022v3) *(promoted by reviewer)*
  This directly covers a core agent-memory mechanism (summarization-based memory) with an explicit algorithmic pipeline; it’s a high-value architecture/procedure source that complements retrieval-based memory.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Reasoning models - OpenAI API** — [Reasoning models - OpenAI API](https://platform.openai.com/docs/guides/reasoning/managing-the-context-window)
  _Skipped because:_ Useful conceptual guidance, but overlaps with the Responses reference and is less precise for quoting concrete parameter defaults.
- **LongBench/LongBench/README.md at main · THUDM/LongBench** — [LongBench/LongBench/README.md at main · THUDM/LongBench](https://github.com/THUDM/LongBench/blob/main/LongBench/README.md)
  _Skipped because:_ Good for implementation pointers, but the ACL paper is more authoritative and citable for benchmark definitions and results.
- **Evaluating Very Long-Term Conversational Memory of ...** — [Evaluating Very Long-Term Conversational Memory of ...](https://arxiv.org/abs/2402.17753)
  _Skipped because:_ Redundant with the PDF version; the PDF is the more directly usable artifact for extracting tables, task definitions, and metrics.

## Reasoning
**Curator:** Selections prioritize authoritative, citable artifacts that directly add benchmark structure/metrics (LoCoMo, LongBench) and official API defaults (OpenAI Responses). Remaining needs weren’t well served by the provided candidates because they require primary IR formula sources, rigorous vector DB benchmarks, and true production case studies rather than marketing-style comparisons.
**Reviewer:** The curation is strong on benchmarks and agent overviews, but it’s missing canonical retrieval/reranking formula sources (MMR/BM25) and should include thin-but-citable official API endpoint docs plus a concrete long-term dialogue memory procedure paper.

---

# Curation Report: What Are AI Agents? Core Concepts and Architecture
**Topic:** `agent-memory` | **Date:** 2026-04-10 19:18
**Library:** 16 existing → 28 sources (12 added, 9 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (12)
- **[reference_doc]** [Function calling | OpenAI API](https://platform.openai.com/docs/guides/function-calling)
  Adds authoritative, citable specs for how agents invoke tools in practice (what you send, what you get back, and how selection is controlled), which is essential for answering precise student questions.
- **[benchmark]** [[2308.03688] AgentBench: Evaluating LLMs as Agents - arXiv](https://arxiv.org/abs/2308.03688)
  Provides concrete quantitative results and an evaluation framework the tutor can cite when discussing agent reliability and tradeoffs across task types.
- **[benchmark]** [WebArena: A Realistic Web Environment for Building Autonomous ...](https://arxiv.org/html/2307.13854v4)
  Gives a widely-used, concrete environment and measurable outcomes for tool-using/web-browsing agents, enabling grounded discussion of multi-step agent performance.
- **[explainer]** [उत्पादन के लिए तैयार एजेंटिक सिस्टम बनाना: शॉपिफाई साइडकिक ...](https://shopify.engineering/building-production-ready-agentic-systems)
  Adds a real-world, company-authored case study with concrete design rationale for building reliable agentic systems beyond toy demos.
- **[paper]** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://proceedings.neurips.cc/paper_files/paper/2023/file/271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf)
  Contributes a concrete alternative agent reasoning architecture with an algorithmic description that can be compared against reactive/tool-using loops on controllability and compute.
- **[paper]** [ReflAct: World-Grounded Decision Making in](https://arxiv.org/pdf/2505.15182v1.pdf)
  Adds a modern, structured ReAct-family architecture that supports explicit comparison discussions (reactive tool use vs grounded decision policies and reflection-like mechanisms).
- **[reference_doc]** [Tool use (function calling) - Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
  This is “thin” by design but exactly what a reference library needs: authoritative parameter names and payload shapes for a major provider, enabling precise cross-provider comparisons in agent tool invocation.
- **[paper]** [Reinforcing Language Agents via Policy Optimization with Action Decomposition](https://arxiv.org/html/2405.15821)
  It directly targets the missing formal RL framing for agents (beyond prompting), providing equations and a concrete training procedure that a tutor can use to connect agent loops to policy optimization.
- **[paper]** [Exploration–Exploitation in MDPs with Options (supplement)](http://proceedings.mlr.press/v54/fruit17a/fruit17a-supp.pdf)
  Even though it’s not LLM-specific, it supplies the missing formalism for hierarchical/temporally-extended actions—highly relevant for teaching tool calls as options with initiation/termination and value functions.
- **[reference_doc]** [Tool use (function calling) - Anthropic](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) *(promoted by reviewer)*
  This is “thin” by design but exactly what a reference library needs: authoritative parameter names and payload shapes for a major provider, enabling precise cross-provider comparisons in agent tool invocation.
- **[paper]** [Reinforcing Language Agents via Policy Optimization with Action Decomposition](https://arxiv.org/html/2405.15821) *(promoted by reviewer)*
  It directly targets the missing formal RL framing for agents (beyond prompting), providing equations and a concrete training procedure that a tutor can use to connect agent loops to policy optimization.
- **[paper]** [Exploration–Exploitation in MDPs with Options (supplement)](http://proceedings.mlr.press/v54/fruit17a/fruit17a-supp.pdf) *(promoted by reviewer)*
  Even though it’s not LLM-specific, it supplies the missing formalism for hierarchical/temporally-extended actions—highly relevant for teaching tool calls as options with initiation/termination and value functions.

## Near-Misses (6) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **API Reference - OpenAI API** — [API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/responses-streaming/response/function_call_arguments)
  _Skipped because:_ Useful for streaming semantics, but the function-calling guide is the more central, comprehensive anchor for tool schema and behavior.
- **Chat Completions | OpenAI API Reference** — [Chat Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat)
  _Skipped because:_ Important historically, but less aligned with current agent/tooling patterns than the dedicated function-calling guide.
- **Responses | OpenAI API Reference** — [Responses | OpenAI API Reference](https://platform.openai.com/docs/api-reference/responses/list?lang=python)
  _Skipped because:_ Broad endpoint reference; doesn’t focus as directly on tool-calling specifics as the function-calling guide.
- **Web search - OpenAI API** — [Web search - OpenAI API](https://platform.openai.com/docs/guides/tools-web-search?api-mode=responses&lang=python)
  _Skipped because:_ Narrow to one tool; less generally useful than the core function/tool calling specification for teaching agent tool invocation.
- **Benchmark Test-Time Scaling of General LLM Agents - arXiv** — [Benchmark Test-Time Scaling of General LLM Agents - arXiv](https://arxiv.org/html/2602.18998v1)
  _Skipped because:_ Potentially valuable, but AgentBench (original) and WebArena are more established anchors for baseline agent benchmarking and environment definition.
- **ScienceAgentBench - Holistic Agent Leaderboardhal.cs.princet** — [ScienceAgentBench - Holistic Agent Leaderboardhal.cs.princeton.edu › scienceagentbench](https://hal.cs.princeton.edu/scienceagentbench)
  _Skipped because:_ Leaderboard pages can change and may be less citable than the primary benchmark papers; kept out to prioritize stable, archival sources.

## Reasoning
**Curator:** Selections prioritize authoritative specs (OpenAI function calling), widely-cited benchmarks/environments with quantitative outcomes (AgentBench, WebArena), and concrete architecture/process descriptions for both production deployment (Shopify) and comparative reasoning frameworks (ToT, ReflAct). Gaps remain where no provided candidates covered formal RL/POMDP equations or non-OpenAI provider tool-calling specs.
**Reviewer:** The curation is strong on modern agent prompting/memory and benchmarking, but it should add at least one non-OpenAI official tool-calling spec and one RL/MDP-formal source (with equations) to fully cover core agent architecture foundations.

---

# Curation Report: Agent Memory: Short-Term Context and Long-Term Storage
**Topic:** `agent-memory` | **Date:** 2026-04-10 19:20
**Library:** 16 existing → 25 sources (9 added, 5 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (9)
- **[reference_doc]** [Index Parameter Range - Milvus go sdk v2.3.x/Index](https://milvus.io/api-reference/go/v2.3.x/Index/indexLimitations.md)
  Gives parameter-level, citable constraints for common ANN index/search knobs that directly affect agent long-term memory retrieval latency and quality.
- **[benchmark]** [Evaluating Very Long-Term Conversational Memory of LLM Agents](https://aclanthology.org/2024.acl-long.747.pdf)
  Adds standardized evaluation methodology and numbers for long-horizon memory—exactly what’s needed to discuss tradeoffs between storing raw logs, summarizing, and retrieval.
- **[explainer]** [Introducing Natural Language Search for Podcast Episodes](https://engineering.atspotify.com/2022/03/introducing-natural-language-search-for-podcast-episodes)
  Provides a real production case study with concrete system design details that map cleanly onto agent long-term memory retrieval stacks (embedding, indexing, serving, latency constraints).
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering (DPR)](https://aclanthology.org/2020.emnlp-main.550.pdf)
  This is a primary-source, equation-level reference for dense retrieval training and scoring—exactly what’s missing for teaching how long-term memory retrieval is learned and executed.
- **[paper]** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (RAG)](https://arxiv.org/pdf/2005.11401.pdf)
  RAG is the canonical formulation tying retrieval to generation with concrete equations and training procedure; it directly supports precise teaching of agent long-term memory via retrieval-augmented prompting.
- **[benchmark]** [A Benchmark for Procedural Memory Retrieval in Language Agents](https://arxiv.org/pdf/2511.21730.pdf)
  The current library leans toward conversational/factual long-term memory; this adds a complementary, numbers-driven evaluation axis (procedural memory) that’s central to agent behavior over time.
- **[paper]** [Dense Passage Retrieval for Open-Domain Question Answering (DPR)](https://aclanthology.org/2020.emnlp-main.550.pdf) *(promoted by reviewer)*
  This is a primary-source, equation-level reference for dense retrieval training and scoring—exactly what’s missing for teaching how long-term memory retrieval is learned and executed.
- **[paper]** [Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks (RAG)](https://arxiv.org/pdf/2005.11401.pdf) *(promoted by reviewer)*
  RAG is the canonical formulation tying retrieval to generation with concrete equations and training procedure; it directly supports precise teaching of agent long-term memory via retrieval-augmented prompting.
- **[benchmark]** [A Benchmark for Procedural Memory Retrieval in Language Agents](https://arxiv.org/pdf/2511.21730.pdf) *(promoted by reviewer)*
  The current library leans toward conversational/factual long-term memory; this adds a complementary, numbers-driven evaluation axis (procedural memory) that’s central to agent behavior over time.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **HNSW** — [HNSW](https://milvus.io/docs/index.md)
  _Skipped because:_ Potentially useful, but the candidate snippet appears to duplicate generic index tables; the explicit parameter-range reference page is more directly citable for defaults/limits.
- **Evaluating Very Long-Term Conversational Memory of ...** — [Evaluating Very Long-Term Conversational Memory of ...](https://arxiv.org/abs/2402.17753)
  _Skipped because:_ Redundant with the ACL Anthology PDF; the PDF is the stable, citable primary source.
- **Introducing Voyager: Spotify’s New Nearest-Neighbor Search .** — [Introducing Voyager: Spotify’s New Nearest-Neighbor Search ...](https://engineering.atspotify.com/2023/10/introducing-voyager-spotifys-new-nearest-neighbor-search-library)
  _Skipped because:_ Strong ANN deployment material, but less directly tied to memory-in-assistants outcomes than the natural-language search case study.

## Reasoning
**Curator:** Selected sources that are either official parameter specs (Milvus index/search ranges) or provide concrete empirical/deployment grounding (ACL long-term memory benchmark; Spotify dense retrieval architecture). The remaining needs require seminal DPR/RAG papers and more official vendor docs/rigorous comparisons than the provided candidates include.
**Reviewer:** The curation is strong on agent-context engineering and practical frameworks, but it should add DPR and RAG as primary formula/training sources and include at least one benchmark that quantifies procedural memory retrieval.

---

# Curation Report: Building Your First LangGraph Agent
**Topic:** `agent-memory` | **Date:** 2026-04-10 19:25
**Library:** 16 existing → 31 sources (15 added, 10 downloaded)
**Candidates evaluated:** 39
**Reviewer verdict:** needs_additions

## Added (15)
- **[reference_doc]** [graph-api.md](https://docs.langchain.com/oss/python/langgraph/graph-api.md)
  This is the most authoritative single place in the candidates for precise signatures, runtime entrypoints, and the mechanics of how state updates (especially messages) are represented and merged.
- **[code]** [langgraph/libs/prebuilt/langgraph/prebuilt/tool_node.py at main · langchain-ai/langgraph](https://github.com/langchain-ai/langgraph/blob/main/libs/prebuilt/langgraph/prebuilt/tool_node.py)
  Reading the maintained source is the fastest way to teach correct tool-calling wiring, expected message schema, and edge cases that aren’t always fully spelled out in tutorials.
- **[explainer]** [LangGraph](https://blog.langchain.dev/langgraph/)
  This provides the clearest official motivation and conceptual model to explain why LangGraph exists and how its execution model differs from simpler agent abstractions.
- **[benchmark]** [Comparing Open-Source AI Agent Frameworks - Langfuse](https://langfuse.com/blog/2025-03-19-ai-agent-comparison)
  Among the candidates, this is the most likely to be structured and practitioner-grounded (Langfuse is an observability vendor), making it useful for concrete, teachable comparisons rather than generic marketing.
- **[explainer]** [Is LangGraph Used In Production?](https://blog.langchain.dev/is-langgraph-used-in-production/)
  This is the most directly relevant official source in the candidates for teaching production concerns (debuggability, reliability patterns) even if it is lighter on hard metrics.
- **[reference_doc]** [Trace LangGraph applications - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/how-tos/trace-langgraph-applications/)
  Even if it feels "thin," it is authoritative and citable for how LangGraph apps are observed/debugged in practice—an essential production concern that the current library only covers narratively.
- **[reference_doc]** [LangGraph How-to: many-tools](https://langchain-ai.github.io/langgraph/how-tos/many-tools/)
  The unfilled need explicitly asks for an official runnable example covering multi-tool selection and routing; this how-to is more stable and teachable than GitHub discussions and complements reading ToolNode source.
- **[explainer]** [Beyond RAG: Implementing Agent Search with LangGraph for Smarter Knowledge Retrieval](https://blog.langchain.dev/beyond-rag-implementing-agent-search-with-langgraph-for-smarter-knowledge-retrieval/)
  This is an official LangChain engineering blog post that tends to include real architecture/procedure (not just marketing) and provides a richer end-to-end agent loop example than the basic quickstart.
- **[explainer]** [Announcing LangGraph v0.1 & LangGraph Cloud: Running agents at scale, reliably](https://blog.langchain.dev/langgraph-cloud/)
  While not a benchmark paper, it is one of the few official sources likely to describe the intended production architecture and operational model—useful to ground deployment discussions beyond anecdotal claims.
- **[explainer]** [Why do I need LangGraph Platform for agent deployment?](https://blog.langchain.dev/why-langgraph-platform/)
  The library is missing authoritative, citable deployment requirement lists tied to LangGraph; this fills that gap even if it lacks hard metrics.
- **[reference_doc]** [Trace LangGraph applications - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/how-tos/trace-langgraph-applications/) *(promoted by reviewer)*
  Even if it feels "thin," it is authoritative and citable for how LangGraph apps are observed/debugged in practice—an essential production concern that the current library only covers narratively.
- **[reference_doc]** [LangGraph How-to: many-tools](https://langchain-ai.github.io/langgraph/how-tos/many-tools/) *(promoted by reviewer)*
  The unfilled need explicitly asks for an official runnable example covering multi-tool selection and routing; this how-to is more stable and teachable than GitHub discussions and complements reading ToolNode source.
- **[explainer]** [Beyond RAG: Implementing Agent Search with LangGraph for Smarter Knowledge Retrieval](https://blog.langchain.dev/beyond-rag-implementing-agent-search-with-langgraph-for-smarter-knowledge-retrieval/) *(promoted by reviewer)*
  This is an official LangChain engineering blog post that tends to include real architecture/procedure (not just marketing) and provides a richer end-to-end agent loop example than the basic quickstart.
- **[explainer]** [Announcing LangGraph v0.1 & LangGraph Cloud: Running agents at scale, reliably](https://blog.langchain.dev/langgraph-cloud/) *(promoted by reviewer)*
  While not a benchmark paper, it is one of the few official sources likely to describe the intended production architecture and operational model—useful to ground deployment discussions beyond anecdotal claims.
- **[explainer]** [Why do I need LangGraph Platform for agent deployment?](https://blog.langchain.dev/why-langgraph-platform/) *(promoted by reviewer)*
  The library is missing authoritative, citable deployment requirement lists tied to LangGraph; this fills that gap even if it lacks hard metrics.

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **2. Add tools - Docs by LangChain** — [2. Add tools - Docs by LangChain](https://docs.langchain.com/oss/python/2-add-tools)
  _Skipped because:_ Useful for onboarding, but overlaps with the more central graph-api.md and is less comprehensive as an API reference for core primitives.
- **Trace LangGraph applications - Docs by LangChain** — [Trace LangGraph applications - Docs by LangChain](https://docs.langchain.com/langsmith/trace-with-langgraph)
  _Skipped because:_ Strong for observability workflows, but the lesson’s missing pieces prioritize core graph/tool APIs and execution semantics over tracing specifics.
- **Introducing the LangGraph Functional API** — [Introducing the LangGraph Functional API](https://blog.langchain.dev/introducing-the-langgraph-functional-api/)
  _Skipped because:_ Good conceptual material, but it may distract from the ‘first agent’ StateGraph-based mental model and primitives the lesson targets.
- **How Infor is Transforming Enterprise AI using LangGraph and ** — [How Infor is Transforming Enterprise AI using LangGraph and LangSmith](https://blog.langchain.dev/customers-infor/)
  _Skipped because:_ Potentially a better case study, but the preview suggests it may be more customer-story than architecture/metrics; kept the broader production overview instead.
- **Route each tool from the ToolNode to a different graph chain** — [Route each tool from the ToolNode to a different graph chain. #3004](https://github.com/langchain-ai/langgraph/discussions/3004)
  _Skipped because:_ Contains a helpful routing pattern, but GitHub discussions are less stable/authoritative than maintained source code for a reference library.

## Reasoning
**Curator:** Selections prioritize official LangChain/LangGraph documentation and maintained repository code for precision, plus official blog rationale for execution-model understanding; comparisons and production material are included only where the candidate appears structured and practically grounded.
**Reviewer:** Core LangGraph primitives are covered, but the library still lacks official runnable multi-tool routing examples and authoritative production/observability documentation that directly addresses the stated unfilled needs.
