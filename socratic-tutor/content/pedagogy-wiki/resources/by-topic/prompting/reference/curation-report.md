# Curation Report: Prompting
**Topic:** `prompting` | **Date:** 2026-04-09 16:31
**Library:** 6 existing → 18 sources (12 added, 9 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (12)
- **[reference_doc]** [OpenAI Platform](https://platform.openai.com/docs/guides/structured-outputs/)
  This is the most authoritative single entry point for structured outputs, giving the tutor citable API surface details and the intended way to enforce schemas in production.
- **[reference_doc]** [Chat Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat)
  Complements the guide with the formal API schema and parameter semantics the tutor can quote when students ask for exact fields and defaults.
- **[benchmark]** [[PDF] Language Models are Few-Shot Learners - NIPS papers](https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf)
  Seminal quantitative evidence for prompting/ICL effects, with concrete accuracy numbers and controlled comparisons that directly answer “how much does few-shot help?”
- **[paper]** [Rethinking the Role of Demonstrations: What Makes In-Context ...](https://arxiv.org/abs/2202.12837)
  Gives the tutor mechanistic and empirical explanations for why exemplars help (or don’t), beyond GPT-3’s headline results.
- **[benchmark]** [JSONSchemaBench: A Rigorous Benchmark of Structured Outputs ...](https://arxiv.org/html/2501.10868v3)
  Provides a research-grade benchmark framing for comparing structured-output approaches with measurable validity and performance criteria.
- **[reference_doc]** [Constrained Decoding](https://openai.com/index/introducing-structured-outputs-in-the-api/)
  While not a full case study, it is an authoritative explanation of the production feature’s intent, guarantees, and tradeoffs—useful for teaching deployment-minded prompting.
- **[paper]** [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751)
  This is the canonical paper that introduced nucleus sampling and contains the exact procedure and evaluation tables—directly filling the missing primary-source formulation for top-p.
- **[paper]** [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf)
  Even though it’s about calibration (not decoding), it is a widely cited primary source for the mathematical definition of temperature scaling with explicit equations—useful when teaching what “temperature” means formally.
- **[reference_doc]** [Structured model outputs | OpenAI API (JSON mode / structured outputs examples)](https://platform.openai.com/docs/guides/text-generation/json-mode)
  The curator rejected it as redundant, but this page often contains the most copy-pastable, exact request/response examples and SDK-specific patterns that students ask for—thin docs are precisely what a reference library should preserve.
- **[paper]** [The Curious Case of Neural Text Degeneration](https://arxiv.org/abs/1904.09751) *(promoted by reviewer)*
  This is the canonical paper that introduced nucleus sampling and contains the exact procedure and evaluation tables—directly filling the missing primary-source formulation for top-p.
- **[paper]** [On Calibration of Modern Neural Networks](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf) *(promoted by reviewer)*
  Even though it’s about calibration (not decoding), it is a widely cited primary source for the mathematical definition of temperature scaling with explicit equations—useful when teaching what “temperature” means formally.
- **[reference_doc]** [Structured model outputs | OpenAI API (JSON mode / structured outputs examples)](https://platform.openai.com/docs/guides/text-generation/json-mode) *(promoted by reviewer)*
  The curator rejected it as redundant, but this page often contains the most copy-pastable, exact request/response examples and SDK-specific patterns that students ask for—thin docs are precisely what a reference library should preserve.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Structured Outputs - OpenAI API** — [Structured Outputs - OpenAI API](https://platform.openai.com/docs/guides/json-mode)
  _Skipped because:_ Overlaps heavily with the broader Structured Outputs guide; kept the more general guide plus the API reference instead.
- **Structured model outputs - OpenAI API** — [Structured model outputs - OpenAI API](https://platform.openai.com/docs/guides/structured-outputs/json-mode)
  _Skipped because:_ Redundant with the selected Structured Outputs guide; doesn’t add distinct parameter-spec detail beyond what the API reference covers.
- **Prompting vs JSON Mode vs Function Calling vs ... - BAML** — [Prompting vs JSON Mode vs Function Calling vs ... - BAML](https://boundaryml.com/blog/schema-aligned-parsing)
  _Skipped because:_ Useful practitioner comparison, but not as authoritative/citable as a benchmark paper for head-to-head metrics and methodology.
- **JSON mode vs Function Calling - API - OpenAI Developer Commu** — [JSON mode vs Function Calling - API - OpenAI Developer Community](https://community.openai.com/t/json-mode-vs-function-calling/476994)
  _Skipped because:_ Anecdotal discussion without systematic measurements; better as troubleshooting than as a reference-library source.

## Reasoning
**Curator:** Selections prioritize authoritative docs for exact API schemas/guarantees and seminal empirical papers for few-shot/ICL effects, plus a rigorous structured-output benchmark. Several needs (sampling formulas and true production case studies) are not met by the provided candidates and require targeted search.
**Reviewer:** The curation is strong on ICL and structured outputs, but it misses the primary-source nucleus sampling paper and a primary-source temperature-scaling formulation, plus a thin-but-valuable official JSON-mode/parse example page.
