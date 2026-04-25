# Curation Report: Chain-of-Thought and Advanced Reasoning
**Topic:** `chain-of-thought` | **Date:** 2026-04-09 16:30
**Library:** 5 existing → 18 sources (13 added, 9 downloaded)
**Candidates evaluated:** 42
**Reviewer verdict:** needs_additions

## Added (13)
- **[paper]** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)
  This is the primary source that defines ToT and explains the design rationale for moving from token-level decoding to deliberate search over intermediate “thought” units.
- **[paper]** [Published as a conference paper at ICLR 2023](http://arxiv.org/pdf/2203.11171v4.pdf)
  Provides citable empirical improvements and ablations for a key advanced reasoning decoding method (self-consistency), including concrete task-by-task numbers.
- **[paper]** [Published as a conference paper at ICLR 2023](http://webdocs.cs.ualberta.ca/~dale/papers/iclr23b.pdf)
  Gives the formalism a tutor can quote when asked how self-consistency differs from greedy decoding and what objective it approximates.
- **[code]** [GitHub - arpg/tree-of-thought-llm: [NeurIPS 2023] Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://github.com/arpg/tree-of-thought-llm)
  Offers a concrete, inspectable reference implementation that a tutor can point to for reproducible procedural steps and prompt/control-logic patterns.
- **[reference_doc]** [Advanced usage - OpenAI API](https://platform.openai.com/docs/guides/text-generation/parameter-details)
  Provides the official definitions needed to precisely explain and reproduce decoding behaviors (sampling diversity, truncation limits, and token-probability controls).
- **[paper]** [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)
  The curator’s ICLR’23 self-consistency entries appear to be this paper but weren’t explicitly identified/linked; this is the canonical source with the exact tables and formal description a tutor will cite.
- **[paper]** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/pdf/2305.10601.pdf)
  They included ToT as a concept explainer, but the still-unfilled needs explicitly ask for ToT benchmark numbers and formal scoring/selection; the PDF is the easiest citable artifact for those tables/definitions.
- **[reference_doc]** [Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions/create)
  Rejected as “thin,” but thin is exactly what’s needed for a reference library: precise parameter definitions that a tutor can quote when explaining sampling, multiple candidates, and logging probabilities.
- **[reference_doc]** [API Reference - OpenAI API (Messages)](https://platform.openai.com/docs/api-reference/messages)
  The library currently has decoding semantics but lacks an authoritative schema reference for tool calling and multimodal inputs in the current API; this fills that explicit unfilled need.
- **[paper]** [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) *(promoted by reviewer)*
  The curator’s ICLR’23 self-consistency entries appear to be this paper but weren’t explicitly identified/linked; this is the canonical source with the exact tables and formal description a tutor will cite.
- **[paper]** [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/pdf/2305.10601.pdf) *(promoted by reviewer)*
  They included ToT as a concept explainer, but the still-unfilled needs explicitly ask for ToT benchmark numbers and formal scoring/selection; the PDF is the easiest citable artifact for those tables/definitions.
- **[reference_doc]** [Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/completions/create) *(promoted by reviewer)*
  Rejected as “thin,” but thin is exactly what’s needed for a reference library: precise parameter definitions that a tutor can quote when explaining sampling, multiple candidates, and logging probabilities.
- **[reference_doc]** [API Reference - OpenAI API (Messages)](https://platform.openai.com/docs/api-reference/messages) *(promoted by reviewer)*
  The library currently has decoding semantics but lacks an authoritative schema reference for tool calling and multimodal inputs in the current API; this fills that explicit unfilled need.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Tree of Thoughts: Deliberate Problem Solving with Large Lang** — [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://proceedings.neurips.cc/paper_files/paper/2023/file/271db9922b8d1f4dd7aaef84ed5ac703-Paper-Conference.pdf)
  _Skipped because:_ Same content as the arXiv ToT paper; kept the canonical arXiv entry to avoid duplication.
- **Chat Completions | OpenAI API Reference** — [Chat Completions | OpenAI API Reference](https://platform.openai.com/docs/api-reference/chat/create)
  _Skipped because:_ Useful endpoint surface, but the parameter-details guide is more concentrated on decoding/sampling semantics needed for reasoning-style prompting.
- **kyegomez/tree-of-thoughts: Plug in and Play ...** — [kyegomez/tree-of-thoughts: Plug in and Play ...](https://github.com/kyegomez/tree-of-thoughts)
  _Skipped because:_ Appears to mirror the same code pattern as other ToT repos; selected a single representative implementation to stay within the cap.

## Reasoning
**Curator:** Selections prioritize primary sources (ToT paper; self-consistency ICLR paper) for authoritative algorithms, equations, and benchmark tables, plus one representative ToT codebase and one official parameter reference to support reproducible decoding configurations.
**Reviewer:** The core picks are strong, but the library should explicitly include the canonical self-consistency paper plus thin-but-authoritative API reference pages and the ToT PDF for its benchmark tables and formal scoring details.
