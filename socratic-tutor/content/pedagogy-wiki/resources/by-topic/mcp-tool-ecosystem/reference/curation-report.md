# Curation Report: Model Context Protocol
**Topic:** `mcp-tool-ecosystem` | **Date:** 2026-04-09 18:30
**Library:** 1 existing → 15 sources (14 added, 9 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (14)
- **[reference_doc]** [Specification - Model Context Protocol](https://modelcontextprotocol.io/specification/2025-11-25)
  This is the most authoritative single source for exact MCP wire-level behavior, message shapes, and lifecycle semantics the tutor can quote precisely.
- **[paper]** [Systematization of Knowledge: Security and Safety in the Model Context Protocol Ecosystem](https://arxiv.org/pdf/2512.08290.pdf)
  Provides a structured, citable rationale for MCP security boundaries and risks, enabling the tutor to explain not just what MCP does but how to reason about safe deployments.
- **[code]** [Model Context Protocol (MCP) Server Development Guide … - GitHub](https://github.com/cyanheads/model-context-protocol-resources/blob/main/guides/mcp-server-development-guide.md)
  Gives a runnable implementation blueprint and debugging-relevant operational details (stdio constraints) that students commonly get wrong when building their first MCP server.
- **[reference_doc]** [Model Context Protocol (MCP) - Docs by LangChain](https://docs.langchain.com/oss/python/langchain/mcp)
  Adds practical interoperability details and a de facto comparison point (LangChain tool interfaces vs MCP) with specific behavioral defaults useful for teaching integration tradeoffs.
- **[reference_doc]** [Tools — Model Context Protocol Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
  Even if “thin,” this is exactly the parameter-level, wire-shape reference a Socratic tutor needs to answer precise questions about tool exposure and invocation semantics.
- **[reference_doc]** [Prompts — Model Context Protocol Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)
  Prompts are a core MCP surface area; having the dedicated spec page prevents hand-wavy explanations and supports exact quoting of fields and lifecycle behavior.
- **[reference_doc]** [Lifecycle / stdio — Model Context Protocol Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)
  This fills a common teaching gap: students routinely get lifecycle and stdio framing wrong, and the spec page is the authoritative source for those operational rules.
- **[paper]** [Design Patterns for Deploying AI Agents with Model Context Protocol (MCP)](https://arxiv.org/html/2603.13417v1)
  This directly targets the unfilled deployment need with concrete operational dimensions (instrumentation, SLOs, readiness checklist) that go beyond SDK how-tos.
- **[reference_doc]** [Connect Claude Code to tools via MCP — Claude Code Docs](https://code.claude.com/docs/en/mcp)
  It’s an authoritative, real-world client deployment guide that can ground lessons in how MCP is actually used in a production-grade tool, complementing the protocol spec.
- **[reference_doc]** [Tools — Model Context Protocol Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) *(promoted by reviewer)*
  Even if “thin,” this is exactly the parameter-level, wire-shape reference a Socratic tutor needs to answer precise questions about tool exposure and invocation semantics.
- **[reference_doc]** [Prompts — Model Context Protocol Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts) *(promoted by reviewer)*
  Prompts are a core MCP surface area; having the dedicated spec page prevents hand-wavy explanations and supports exact quoting of fields and lifecycle behavior.
- **[reference_doc]** [Lifecycle / stdio — Model Context Protocol Specification (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle) *(promoted by reviewer)*
  This fills a common teaching gap: students routinely get lifecycle and stdio framing wrong, and the spec page is the authoritative source for those operational rules.
- **[paper]** [Design Patterns for Deploying AI Agents with Model Context Protocol (MCP)](https://arxiv.org/html/2603.13417v1) *(promoted by reviewer)*
  This directly targets the unfilled deployment need with concrete operational dimensions (instrumentation, SLOs, readiness checklist) that go beyond SDK how-tos.
- **[reference_doc]** [Connect Claude Code to tools via MCP — Claude Code Docs](https://code.claude.com/docs/en/mcp) *(promoted by reviewer)*
  It’s an authoritative, real-world client deployment guide that can ground lessons in how MCP is actually used in a production-grade tool, complementing the protocol spec.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Architecture overview - Model Context Protocol** — [Architecture overview - Model Context Protocol](https://modelcontextprotocol.io/docs/learn/architecture)
  _Skipped because:_ Useful conceptual overview, but less normative and less detailed than the specification and the security paper for the missing needs.
- **MCP vs LangChain vs RAG: AI Context Management ...** — [MCP vs LangChain vs RAG: AI Context Management ...](https://tetrate.io/learn/ai/mcp/mcp-vs-alternatives)
  _Skipped because:_ Likely higher-level and marketing-oriented; less reliable as a structured, citable feature matrix than primary docs and concrete adapter behavior.

## Reasoning
**Curator:** Selections prioritize the normative MCP specification for precision, a peer-reviewed security/systematization paper for deep conceptual grounding, and concrete implementation docs for hands-on teaching; remaining gaps are production metrics case studies and a truly authoritative cross-protocol feature matrix.
**Reviewer:** The curator picked strong core sources, but the library should add the official per-surface spec pages (tools/prompts/lifecycle) and at least one deployment-focused paper/doc to cover production readiness and operational practice.

---

# Curation Report: Tool Use and Function Calling in Agents
**Topic:** `mcp-tool-ecosystem` | **Date:** 2026-04-10 19:15
**Library:** 5 existing → 16 sources (11 added, 7 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (11)
- **[reference_doc]** [Function calling - OpenAI API](https://platform.openai.com/docs/guides/function-calling?api-mode=responses)
  This is the most authoritative spec-like guide among the candidates for OpenAI tool calling, giving the tutor citable field names and behavioral semantics needed for precise Q&A about schemas and tool selection.
- **[reference_doc]** [Structured model outputs - OpenAI API](https://platform.openai.com/docs/guides/structured-outputs/json-mode)
  Complements function calling by covering the exact structured-output mechanisms and constraints that govern tool argument formatting and robust parsing/validation.
- **[benchmark]** [The Berkeley Function Calling Leaderboard (BFCL): From Tool Use ...](https://proceedings.mlr.press/v267/patil25a.html)
  Directly supplies quantitative, comparable numbers (accuracy/latency/cost) for tool/function calling across models—useful for teaching tradeoffs and citing concrete benchmarks.
- **[paper]** [[PDF] Towards Stable Large-Scale Benchmarking on Tool Learning of ...](https://aclanthology.org/2024.findings-acl.664.pdf)
  Adds methodological rigor beyond a dataset description, helping the tutor explain what tool-use scores mean, how they’re computed, and what pitfalls/controls matter in empirical evaluation.
- **[paper]** [[PDF] Gorilla: Large Language Model Connected with Massive APIs](https://proceedings.neurips.cc/paper_files/paper/2024/file/e4c61f578ff07830f5c37378dd3ecb0d-Paper-Conference.pdf)
  Provides an explicit training formulation for tool-use grounded in API documentation retrieval, giving the tutor a concrete, citable pipeline for how models learn to map intents to API calls.
- **[reference_doc]** [Function calling | OpenAI API](https://platform.openai.com/docs/guides/function-calling)
  Even if it overlaps with the Responses API reference, this guide typically contains the most teachable, end-to-end examples and best-practice patterns that directly fill the missing “authoritative working example” need.
- **[reference_doc]** [Streaming API responses - OpenAI API](https://platform.openai.com/docs/guides/streaming-responses?api-mode=responses)
  Tool calling in production often uses streaming; this page provides concrete event/field semantics needed to teach robust assembly/validation of streamed tool arguments.
- **[reference_doc]** [API Reference - Responses streaming: response.function_call_arguments](https://platform.openai.com/docs/api-reference/responses-streaming/response/function_call_arguments)
  This is “thin” but highly valuable: it gives exact field names and object structure that a Socratic tutor can cite when students ask about streaming tool-call deltas and parsing.
- **[reference_doc]** [Function calling | OpenAI API](https://platform.openai.com/docs/guides/function-calling) *(promoted by reviewer)*
  Even if it overlaps with the Responses API reference, this guide typically contains the most teachable, end-to-end examples and best-practice patterns that directly fill the missing “authoritative working example” need.
- **[reference_doc]** [Streaming API responses - OpenAI API](https://platform.openai.com/docs/guides/streaming-responses?api-mode=responses) *(promoted by reviewer)*
  Tool calling in production often uses streaming; this page provides concrete event/field semantics needed to teach robust assembly/validation of streamed tool arguments.
- **[reference_doc]** [API Reference - Responses streaming: response.function_call_arguments](https://platform.openai.com/docs/api-reference/responses-streaming/response/function_call_arguments) *(promoted by reviewer)*
  This is “thin” but highly valuable: it gives exact field names and object structure that a Socratic tutor can cite when students ask about streaming tool-call deltas and parsing.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **8.1 Ablation Study** — [8.1 Ablation Study](https://arxiv.org/html/2411.13547v2)
  _Skipped because:_ Likely contains ToolBench ablations, but the candidate metadata is ambiguous (section-level title) and the ACL Findings PDF is a clearer, citable benchmarking-methods reference.
- **ToolBench, an evaluation suite for LLM tool manipulation ...** — [ToolBench, an evaluation suite for LLM tool manipulation ...](https://github.com/sambanova/toolbench)
  _Skipped because:_ Useful implementation, but the library needs more authoritative, citable benchmark methodology/results first; this repo is better as a secondary implementation pointer.
- **Tool calling** — [Tool calling](https://platform.openai.com/docs/guides/function-calling?lang=python)
  _Skipped because:_ Overlaps heavily with the Responses-mode function calling guide; the Responses-mode page is the better single anchor for exact modern request/response fields.
- **REACT: Revealing Evolutionary Action Consequence Trajectorie** — [REACT: Revealing Evolutionary Action Consequence Trajectories](https://arxiv.org/pdf/2404.03359.pdf)
  _Skipped because:_ This is an unrelated RL interpretability paper and not the ReAct (Reasoning+Acting) tool-use formulation needed for agent tool-calling loops.

## Reasoning
**Curator:** Selections prioritize authoritative API specs (OpenAI docs) and high-signal quantitative benchmarks (BFCL, ToolBench methodology), plus a concrete training pipeline paper (Gorilla/RAT) to support mechanistic teaching of how tool-use models are trained and evaluated. Thin or non-authoritative deployment/blog candidates were excluded in favor of citable primary sources.
**Reviewer:** The curator’s core picks are strong, but they missed a few thin-yet-critical official docs that uniquely cover end-to-end and streaming tool-calling mechanics—key for robust implementation teaching.
