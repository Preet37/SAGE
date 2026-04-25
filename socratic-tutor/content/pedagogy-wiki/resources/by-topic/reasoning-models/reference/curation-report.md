# Curation Report: Reasoning Models
**Topic:** `reasoning-models` | **Date:** 2026-04-09 18:37
**Library:** 7 existing → 27 sources (20 added, 13 downloaded)
**Candidates evaluated:** 47
**Reviewer verdict:** needs_additions

## Added (20)
- **[reference_doc]** [OpenAI Platform: Reasoning Guide](https://platform.openai.com/docs/guides/reasoning)
  This is the most authoritative place to cite API semantics for reasoning models, including how to invoke them and what knobs exist to trade off latency/cost vs reasoning depth.
- **[reference_doc]** [API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/responses-streaming/response/reasoning)
  Gives precise, citable field-level details needed to answer student questions about what the API returns for reasoning traces and how to parse/handle them programmatically.
- **[explainer]** [Safety](https://openai.com/index/learning-to-reason-with-llms/)
  This is the closest official narrative tying together training intent, test-time compute, and product behavior for o1-style reasoning models, which the tutor can use to explain design rationale.
- **[reference_doc]** [[PDF] OpenAI o1 System Card](https://cdn.openai.com/o1-system-card-20241205.pdf)
  System cards are the most citable sources for what is and isn’t exposed in reasoning traces and how safety constraints shape model behavior and outputs.
- **[paper]** [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171)
  Provides a canonical, widely-cited test-time compute scaling method with concrete curves/tables that the tutor can use to explain pass@k-like improvements via multiple samples and aggregation.
- **[paper]** [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs ... - arXiv](https://arxiv.org/html/2501.12948v1)
  Among the candidates, this is the most authoritative single document for DeepSeek-R1’s methods and results, enabling structured comparisons to o1/o3-style models.
- **[paper]** [Let's reward step by step: Step-Level reward model as the Navigators for Reasoning](https://arxiv.org/abs/2310.10080)
  This is directly on the missing PRM/step-level reward topic and is likely to contain the concrete loss/objective and credit-assignment details the library currently lacks.
- **[paper]** [Process Reward Models for Reflective Mathematical Reasoning](https://aclanthology.org/2025.findings-emnlp.253.pdf)
  Findings papers often include the exact formulations and ablations needed for teaching; this one is tightly aligned with PRM vs ORM and reflective reasoning, which is currently under-sourced.
- **[explainer]** [OpenAI o3 and o4-mini System Card](https://openai.com/index/o3-o4-mini-system-card/)
  The library currently anchors on o1; adding the o3/o4-mini system card improves coverage of the broader 'reasoning model' family and typically includes concrete evaluation numbers and trace/safety policies useful for precise teaching.
- **[explainer]** [OpenAI o3 and o4-mini System Card (PDF)](https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf)
  If the goal is precision-first citation, the PDF is usually the best artifact for tables and exact wording; it complements the o1 system card and helps cover compute/performance tradeoffs with concrete numbers.
- **[explainer]** [OpenAI o3-mini System Card (PDF)](https://cdn.openai.com/o3-mini-system-card-feb10.pdf)
  Even if overlapping conceptually, o3-mini may include distinct tables or operational constraints; those specific numbers are valuable for a tutor explaining model-to-model differences within the reasoning lineup.
- **[paper]** [Trading inference-time compute for adversarial robustness](https://cdn.openai.com/papers/trading-inference-time-compute-for-adversarial-robustness-20250121_1.pdf)
  This appears to contain concrete, citable numbers and a focused compute-at-test-time narrative; it strengthens the lesson’s core theme (compute vs reasoning quality) beyond product docs.
- **[reference_doc]** [Reasoning best practices | OpenAI API](https://platform.openai.com/docs/guides/reasoning/best-practices)
  Even if 'thin,' best-practices pages often contain the most actionable, parameter-specific operational advice that students ask about; it complements the guide/reference by explaining intended usage and tradeoffs.
- **[paper]** [Let's reward step by step: Step-Level reward model as the Navigators for Reasoning](https://arxiv.org/abs/2310.10080) *(promoted by reviewer)*
  This is directly on the missing PRM/step-level reward topic and is likely to contain the concrete loss/objective and credit-assignment details the library currently lacks.
- **[paper]** [Process Reward Models for Reflective Mathematical Reasoning](https://aclanthology.org/2025.findings-emnlp.253.pdf) *(promoted by reviewer)*
  Findings papers often include the exact formulations and ablations needed for teaching; this one is tightly aligned with PRM vs ORM and reflective reasoning, which is currently under-sourced.
- **[explainer]** [OpenAI o3 and o4-mini System Card](https://openai.com/index/o3-o4-mini-system-card/) *(promoted by reviewer)*
  The library currently anchors on o1; adding the o3/o4-mini system card improves coverage of the broader 'reasoning model' family and typically includes concrete evaluation numbers and trace/safety policies useful for precise teaching.
- **[explainer]** [OpenAI o3 and o4-mini System Card (PDF)](https://cdn.openai.com/pdf/2221c875-02dc-4789-800b-e7758f3722c1/o3-and-o4-mini-system-card.pdf) *(promoted by reviewer)*
  If the goal is precision-first citation, the PDF is usually the best artifact for tables and exact wording; it complements the o1 system card and helps cover compute/performance tradeoffs with concrete numbers.
- **[explainer]** [OpenAI o3-mini System Card (PDF)](https://cdn.openai.com/o3-mini-system-card-feb10.pdf) *(promoted by reviewer)*
  Even if overlapping conceptually, o3-mini may include distinct tables or operational constraints; those specific numbers are valuable for a tutor explaining model-to-model differences within the reasoning lineup.
- **[paper]** [Trading inference-time compute for adversarial robustness](https://cdn.openai.com/papers/trading-inference-time-compute-for-adversarial-robustness-20250121_1.pdf) *(promoted by reviewer)*
  This appears to contain concrete, citable numbers and a focused compute-at-test-time narrative; it strengthens the lesson’s core theme (compute vs reasoning quality) beyond product docs.
- **[reference_doc]** [Reasoning best practices | OpenAI API](https://platform.openai.com/docs/guides/reasoning/best-practices) *(promoted by reviewer)*
  Even if 'thin,' best-practices pages often contain the most actionable, parameter-specific operational advice that students ask about; it complements the guide/reference by explaining intended usage and tradeoffs.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Reasoning models - OpenAI API** — [Reasoning models - OpenAI API](https://platform.openai.com/docs/guides/reasoning/quickstart)
  _Skipped because:_ Overlaps heavily with the main Reasoning Guide and is less useful than the API reference page for precise field/stream semantics.
- **Reasoning best practices | OpenAI API** — [Reasoning best practices | OpenAI API](https://platform.openai.com/docs/guides/reasoning-best-practices)
  _Skipped because:_ Helpful operational tips, but it is less “precision-first” than the core guide + API reference for defaults, parameters, and schemas.
- **OpenAI o1 System Card** — [OpenAI o1 System Card](https://openai.com/index/openai-o1-system-card/)
  _Skipped because:_ The HTML page is redundant with the PDF; the PDF is preferable for stable citation and complete details.
- **[PDF] Evaluation of DeepSeek AI Models** — [[PDF] Evaluation of DeepSeek AI Models](https://www.nist.gov/system/files/documents/2025/09/30/CAISI_Evaluation_of_DeepSeek_AI_Models.pdf)
  _Skipped because:_ Potentially strong for standardized evaluation, but the candidate preview is not specific enough here to confirm it contains the needed cross-model comparisons (o1/o3 vs R1) and consistent cost/latency metrics.

## Reasoning
**Curator:** Selections prioritize official OpenAI documentation for API semantics and system-card-level constraints, plus the most authoritative available primary sources for o1-style rationale and for empirical test-time sampling gains and DeepSeek-R1 comparisons. PRM-vs-ORM math and comprehensive compute-scaling/verifier ablations are not adequately covered by the provided candidates.
**Reviewer:** The curation is strong on RLHF and OpenAI reasoning-model API semantics, but it should add at least one PRM/step-level reward formulation paper and one o3/o4-mini system-card/compute-tradeoff source to cover missing equations and concrete evaluation/compute tradeoff numbers.
