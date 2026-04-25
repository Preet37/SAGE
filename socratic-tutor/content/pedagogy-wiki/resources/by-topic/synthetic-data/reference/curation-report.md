# Curation Report: Synthetic Data and Self-Improvement
**Topic:** `synthetic-data` | **Date:** 2026-04-09 18:39
**Library:** 4 existing → 18 sources (14 added, 10 downloaded)
**Candidates evaluated:** 45
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [[2401.10020] Self-Rewarding Language Models - arXiv](https://arxiv.org/abs/2401.10020)
  Gives a concrete, citable formulation of 'RLHF without humans' via self-generated preference data and iterative alignment, including the exact optimization target and training loop.
- **[paper]** [Reinforcement Learning with Verifiable Noisy Rewards - arXiv](https://arxiv.org/abs/2601.04411)
  Provides an algorithmic formulation and theoretical framing for verification-based rewards (unit tests/judges) that a tutor can use to explain RLVR mechanics and failure modes precisely.
- **[paper]** [FineWeb2: One Pipeline to Scale Them All — Adapting Pre-Training ...](https://arxiv.org/html/2506.20920v1)
  An authoritative, end-to-end description of modern large-scale data preparation that can be used to teach practical decontamination/dedup/filtering workflows and their rationale.
- **[paper]** [Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 14255–14273](https://aclanthology.org/2024.acl-long.769.pdf)
  Directly targets the 'synthetic-data knobs' problem from the filtering angle, offering empirical tables that help a tutor discuss how filtering choices change performance and efficiency.
- **[paper]** [[PDF] Automatic Instruction Evolving for Large Language Models](https://aclanthology.org/2024.emnlp-main.397.pdf)
  Adds concrete experimental evidence about evol-style rewriting choices and their effect on instruction-tuning outcomes, supporting precise discussions of diversity/complexity knobs.
- **[paper]** [Balancing Cost and Effectiveness of Synthetic Data Generation Strategies for LLMs](https://arxiv.org/html/2409.19759v2)
  While not a product postmortem, it provides concrete cost/quality metrics and decision criteria that translate well to 'deployment-like' constraints (budget, verification, and ROI).
- **[paper]** [Why Self-Rewarding Works: Theoretical Guarantees for Iterative Alignment of Language Models](https://arxiv.org/pdf/2601.22513.pdf)
  The current library has the SRLM objective but lacks a theory/guarantees companion; this paper gives precise conditions and proof-style framing that a tutor can use to teach stability and failure modes rigorously.
- **[paper]** [Process-based Self-Rewarding Language Models](https://aclanthology.org/2025.findings-acl.930.pdf)
  It materially extends SRLM beyond outcome preference pairs into process supervision, which is a key conceptual axis for self-improvement loops (especially for reasoning/code) and provides concrete algorithmic procedure.
- **[paper]** [Evol-Instruct (EMNLP 2024 main paper, pages 6998–7018)](https://aclanthology.org/anthology-files/pdf/emnlp/2024.emnlp-main.397.pdf)
  This is directly aligned with the unfilled reproducible evol-style pipeline need; the candidate list snippet is thin, but the full paper typically contains the concrete generation/refinement recipe and quantitative results worth citing.
- **[benchmark]** [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)
  The lesson explicitly needs benchmark leakage/overlap audit procedures; while not a full modern LLM decontamination report, this provides a citable, method-focused evaluation protocol and leakage-related rationale in a high-stakes domain (code).
- **[paper]** [Why Self-Rewarding Works: Theoretical Guarantees for Iterative Alignment of Language Models](https://arxiv.org/pdf/2601.22513.pdf) *(promoted by reviewer)*
  The current library has the SRLM objective but lacks a theory/guarantees companion; this paper gives precise conditions and proof-style framing that a tutor can use to teach stability and failure modes rigorously.
- **[paper]** [Process-based Self-Rewarding Language Models](https://aclanthology.org/2025.findings-acl.930.pdf) *(promoted by reviewer)*
  It materially extends SRLM beyond outcome preference pairs into process supervision, which is a key conceptual axis for self-improvement loops (especially for reasoning/code) and provides concrete algorithmic procedure.
- **[paper]** [Evol-Instruct (EMNLP 2024 main paper, pages 6998–7018)](https://aclanthology.org/anthology-files/pdf/emnlp/2024.emnlp-main.397.pdf) *(promoted by reviewer)*
  This is directly aligned with the unfilled reproducible evol-style pipeline need; the candidate list snippet is thin, but the full paper typically contains the concrete generation/refinement recipe and quantitative results worth citing.
- **[benchmark]** [Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374) *(promoted by reviewer)*
  The lesson explicitly needs benchmark leakage/overlap audit procedures; while not a full modern LLM decontamination report, this provides a citable, method-focused evaluation protocol and leakage-related rationale in a high-stakes domain (code).

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Data Preparation for LLM Pretraining** — [[PDF] Data Preparation for LLM Pretraining](https://web.stanford.edu/class/cs246/slides/20-guest.pdf)
  _Skipped because:_ Useful as a teaching aid, but less citable/complete than a full technical paper/report for exact procedures and reproducible details.
- **Balancing Cost and Effectiveness of Synthetic Data** — [Balancing Cost and Effectiveness of Synthetic Data](http://arxiv.org/pdf/2409.19759.pdf)
  _Skipped because:_ Duplicate of the selected arXiv HTML entry; kept only one canonical URL.
- **[PDF] Teaching Language Model Agents How to Self-Improve - N** — [[PDF] Teaching Language Model Agents How to Self-Improve - NIPS papers](https://proceedings.neurips.cc/paper_files/paper/2024/file/639d992f819c2b40387d4d5170b8ffd7-Paper-Conference.pdf)
  _Skipped because:_ Strong self-improvement case study, but less directly focused on formal RLVR/RLAIF loss formulations than the selected SRLM + RLVR-noise papers.

## Reasoning
**Curator:** Selections prioritize sources that (1) provide explicit objectives/update rules for self-improvement (SRLM + RLVR) and (2) supply authoritative, step-by-step data pipeline and empirical ablations on evolving/filtering knobs; remaining gaps are mainly reproducible code and true production postmortems.
**Reviewer:** The curator’s additions are strong on iterative self-rewarding and filtering, but the library still benefits from adding theory for SRLM, process-based self-rewarding procedures, and at least one evol-style end-to-end recipe plus a concrete evaluation/leakage case study.
