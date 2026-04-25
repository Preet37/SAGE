# Curation Report: Imitation Learning
**Topic:** `imitation-learning` | **Date:** 2026-04-09 16:20
**Library:** 4 existing → 16 sources (12 added, 9 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (12)
- **[paper]** [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning](https://proceedings.mlr.press/v15/ross11a.html)
  This is the canonical DAgger formulation with the key theorem-level guarantees and the exact iterative data aggregation algorithm, enabling precise derivations and citations beyond high-level summaries.
- **[paper]** [Generative Adversarial Imitation Learning](https://proceedings.neurips.cc/paper_files/paper/2016/file/cc7e2b878868cbae992d1fb743995d8f-Paper.pdf)
  Provides the exact minimax objective, optimization procedure, and the theoretical link to IRL/occupancy matching that students often ask to see written out formally.
- **[benchmark]** [RT-1: Robotics Transformer for Real-World Control at Scale](https://arxiv.org/html/2212.06817v2)
  Gives concrete, citable numbers and experimental structure for large-scale robotics imitation with language conditioning, including generalization-focused evaluations.
- **[benchmark]** [RT-2: Vision-Language-Action Models](https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)
  Adds modern VLA empirical evidence with explicit trial counts, success metrics, and variant comparisons that help teach what improves open-vocabulary generalization.
- **[reference_doc]** [imitation.algorithms.dagger](https://imitation.readthedocs.io/en/latest/_api/imitation.algorithms.dagger.html)
  This is the most precise place to quote exact defaults and configuration knobs for a widely used imitation-learning stack, supporting reproducible teaching examples.
- **[explainer]** [Do As I Can, Not As I Say:](http://arxiv.org/pdf/2204.01691.pdf)
  Provides an authoritative, step-by-step system design for open-vocabulary, long-horizon manipulation and explains why grounding via value functions mitigates ungrounded language and distribution shift.
- **[paper]** [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger)](https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf)
  The library currently points to an arXiv entry, but this canonical PDF is the stable, citable version with the exact equations/guarantees a Socratic tutor will want to quote precisely.
- **[paper]** [Generative Adversarial Imitation Learning](https://arxiv.org/pdf/1606.03476.pdf)
  If the library only has an arXiv abstract page, the PDF is the actual value: it contains the exact objective, optimization details, and derivations students ask to see.
- **[benchmark]** [RT-1: Robotics Transformer for Real-World Control at Scale (project page)](https://robotics-transformer1.github.io)
  Even if the paper is already included, the official project page is often the fastest way to retrieve specific numbers, task lists, and evaluation setup details for teaching and citation.
- **[paper]** [A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger)](https://www.ri.cmu.edu/pub_files/2011/4/Ross-AISTATS11-NoRegret.pdf) *(promoted by reviewer)*
  The library currently points to an arXiv entry, but this canonical PDF is the stable, citable version with the exact equations/guarantees a Socratic tutor will want to quote precisely.
- **[paper]** [Generative Adversarial Imitation Learning](https://arxiv.org/pdf/1606.03476.pdf) *(promoted by reviewer)*
  If the library only has an arXiv abstract page, the PDF is the actual value: it contains the exact objective, optimization details, and derivations students ask to see.
- **[benchmark]** [RT-1: Robotics Transformer for Real-World Control at Scale (project page)](https://robotics-transformer1.github.io) *(promoted by reviewer)*
  Even if the paper is already included, the official project page is often the fastest way to retrieve specific numbers, task lists, and evaluation setup details for teaching and citation.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **DAgger#** — [DAgger#](https://imitation.readthedocs.io/en/latest/algorithms/dagger.html)
  _Skipped because:_ Useful narrative and example, but the API reference page is more precise for quoting exact parameters/defaults.
- **Behavioral Cloning (BC)#** — [Behavioral Cloning (BC)#](https://imitation.readthedocs.io/en/latest/algorithms/bc.html)
  _Skipped because:_ Good for usage, but it does not supply the missing formal covariate-shift/compounding-error derivations the tutor needs as a primary formula source.
- **SayCan: Grounding Language in Robotic Affordances** — [SayCan: Grounding Language in Robotic Affordances](https://say-can.github.io)
  _Skipped because:_ Great overview and media, but the PDF paper is the citable, detailed source with the exact method description.

## Reasoning
**Curator:** Selections prioritize primary papers for formal objectives/guarantees (DAgger, GAIL), modern robotics benchmarks with concrete success-rate tables (RT-1/RT-2), one precise API-default reference (imitation library), and one authoritative VLA design rationale source (SayCan). Gaps remain where no candidates covered MaxEnt IRL derivations or full end-to-end robotics implementation/docs.
**Reviewer:** The curator picked strong anchors, but the stable canonical PDFs for DAgger and GAIL (and the RT-1 official project page for quick access to concrete numbers/protocols) should be included as high-precision teaching references.
