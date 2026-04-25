# Curation Report: System Prompts
**Topic:** `system-prompts` | **Date:** 2026-04-09 16:36
**Library:** 4 existing → 18 sources (14 added, 9 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (14)
- **[reference_doc]** [Responses | OpenAI API Reference](https://platform.openai.com/docs/api-reference/responses/list?lang=python)
  This is the most authoritative place to cite exact parameter names, defaults, and the concrete schema for how instructions and conversation items are represented in the modern OpenAI API.
- **[paper]** [[PDF] Training language models to follow instructions with human feedback](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)
  Gives primary-source training rationale for instruction-following behavior that makes system/developer/user prompting effective, with enough procedural detail to teach the mechanism rather than just describe it.
- **[paper]** [Recursively Summarizing Enables Long-Term Dialogue Memory in ...](https://arxiv.org/html/2308.15022v3)
  Directly supports quantitative teaching about summarization vs. truncation tradeoffs and how long-context management affects instruction-following and task accuracy.
- **[benchmark]** [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and ...](https://arxiv.org/html/2603.07670v1)
  Provides a comparative framework and explicit criteria/metrics the tutor can use to contrast memory strategies by cost/latency/faithfulness/performance across context lengths.
- **[reference_doc]** [Streaming events | OpenAI API Reference (Responses streaming)](https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl)
  Even if “thin,” this is the authoritative place for precise streaming event semantics and payload shapes—critical for production-grade system-prompt handling and multi-turn state assembly.
- **[reference_doc]** [Debugging requests | OpenAI API Reference](https://platform.openai.com/docs/api-reference/debugging-requests)
  This fills a practical gap: how to diagnose instruction-following failures and verify what was sent/received, with exact field names that a tutor can cite and students can implement.
- **[explainer]** [Prompt engineering (Write clear instructions) | OpenAI Platform Docs](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions)
  The library currently leans research/blog for prompting; adding the official guide gives canonical, teachable “do X, not Y” patterns aligned with OpenAI’s current API behavior.
- **[explainer]** [Prompt engineering (Provide reference text) | OpenAI Platform Docs](https://platform.openai.com/docs/guides/prompt-engineering/strategy-provide-reference-text)
  This is a high-leverage system-prompt pattern with clear procedural guidance; it complements RLHF/InstructGPT by showing how to operationalize “follow instructions” into verifiable behavior.
- **[paper]** [Verbatim-Grounded Artifact Extraction for Long LLM Conversations](https://www.arxiv.org/pdf/2601.00821.pdf)
  This directly targets the unfilled production need (summary drift/failure modes) with a specific method and measurements, making it more actionable than generic “summarize history” advice.
- **[reference_doc]** [Streaming events | OpenAI API Reference (Responses streaming)](https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl) *(promoted by reviewer)*
  Even if “thin,” this is the authoritative place for precise streaming event semantics and payload shapes—critical for production-grade system-prompt handling and multi-turn state assembly.
- **[reference_doc]** [Debugging requests | OpenAI API Reference](https://platform.openai.com/docs/api-reference/debugging-requests) *(promoted by reviewer)*
  This fills a practical gap: how to diagnose instruction-following failures and verify what was sent/received, with exact field names that a tutor can cite and students can implement.
- **[explainer]** [Prompt engineering (Write clear instructions) | OpenAI Platform Docs](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions) *(promoted by reviewer)*
  The library currently leans research/blog for prompting; adding the official guide gives canonical, teachable “do X, not Y” patterns aligned with OpenAI’s current API behavior.
- **[explainer]** [Prompt engineering (Provide reference text) | OpenAI Platform Docs](https://platform.openai.com/docs/guides/prompt-engineering/strategy-provide-reference-text) *(promoted by reviewer)*
  This is a high-leverage system-prompt pattern with clear procedural guidance; it complements RLHF/InstructGPT by showing how to operationalize “follow instructions” into verifiable behavior.
- **[paper]** [Verbatim-Grounded Artifact Extraction for Long LLM Conversations](https://www.arxiv.org/pdf/2601.00821.pdf) *(promoted by reviewer)*
  This directly targets the unfilled production need (summary drift/failure modes) with a specific method and measurements, making it more actionable than generic “summarize history” advice.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **API Reference - OpenAI API** — [API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/realtime-server-events/conversation/item/truncated)
  _Skipped because:_ Useful for truncation event semantics in Realtime, but narrower than the core Responses reference for teaching general system-prompt and history handling.
- **Diagnosing Retrieval vs. Utilization Bottlenecks in LLM Agen** — [Diagnosing Retrieval vs. Utilization Bottlenecks in LLM Agent Memory](https://arxiv.org/html/2603.02473v1)
  _Skipped because:_ Strong for diagnosing memory failures, but overlaps with the broader mechanisms-and-evaluation coverage of the selected survey and doesn’t add as much general-purpose comparison structure.
- **[PDF] Evaluating Very Long-Term Conversational Memory of LLM** — [[PDF] Evaluating Very Long-Term Conversational Memory of LLM Agents](https://aclanthology.org/2024.acl-long.747.pdf)
  _Skipped because:_ Good benchmark-style evaluation, but the selected survey better consolidates mechanisms and evaluation criteria for a reference library slot.
- **Constitutional AI: Harmlessness from AI Feedback - arXiv** — [Constitutional AI: Harmlessness from AI Feedback - arXiv](https://arxiv.org/abs/2212.08073)
  _Skipped because:_ Excellent for safety/steerability rationale, but less directly tied to system-vs-developer-vs-user instruction hierarchy than the RLHF/InstructGPT primary source for this lesson.

## Reasoning
**Curator:** Selections prioritize (1) official API documentation for exact, citable specs and (2) primary/empirical papers that explain why instruction hierarchy works and quantify long-context memory management tradeoffs. Deployment-case candidates provided here appear non-authoritative/duplicative from the previews, so that need is left unfilled pending a stronger primary source.
**Reviewer:** The core picks are strong, but adding a few thin-but-authoritative API reference pages plus one concrete long-conversation artifact/grounding paper would materially improve teachability and production realism for system prompts.
