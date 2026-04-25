# Curation Report: Domain Adaptation
**Topic:** `domain-adaptation` | **Date:** 2026-04-09 16:17
**Library:** 7 existing → 19 sources (12 added, 9 downloaded)
**Candidates evaluated:** 47
**Reviewer verdict:** needs_additions

## Added (12)
- **[paper]** [Analysis of Representations for Domain Adaptation](https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf)
  Gives a rigorous, citable bound clarifying when domain-invariant representations can fail (conditional shift), which helps answer “what’s the exact bound and when does it apply?” beyond the classic covariate-shift story.
- **[paper]** [On Learning Invariant Representations for Domain Adaptation](http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf)
  Complements the NeurIPS version with a focused treatment of invariant representations and their theoretical limitations, giving the tutor additional precise statements to cite and contrast with Ben-David-style discrepancy bounds.
- **[benchmark]** [Benchmarking Unsupervised Domain Adaptation Methods ...](https://arxiv.org/html/2407.11676v2)
  Directly targets the need for consolidated benchmark numbers and protocol clarity, which is essential when students ask “what accuracy does method X get on dataset Y under the standard setup?”
- **[benchmark]** [VisDA: The Visual Domain Adaptation Challenge](https://ar5iv.labs.arxiv.org/html/1710.06924)
  Provides authoritative, citable benchmark results and the canonical evaluation framing for VisDA, useful both for precise numbers and for explaining why the benchmark is structured as it is.
- **[explainer]** [Active Exploration for System Identification in Robotic Manipulation](https://arxiv.org/html/2404.12308v2)
  Gives a concrete, procedural reference for system identification as a sim-to-real tool (what data to collect, what objective to optimize, and how it plugs into policy learning), grounding “reality gap” mitigation beyond domain randomization.
- **[code]** [GitHub - facebookresearch/DomainBed: DomainBed is a suite to test domain generalization algorithms](https://github.com/facebookresearch/DomainBed)
  Acts as the de facto API reference for a widely used DG/UDA-adjacent tooling ecosystem, letting the tutor point to concrete defaults, config schemas, and reproducible experiment structure.
- **[paper]** [i-Sim2Real: Reinforcement Learning of Robotic Policies in Tight Human-Robot Interaction](https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf)
  This directly fills the missing “authoritative end-to-end sim-to-real” need with a concrete, reproducible procedure (explore→identify→train/optimize) rather than only conceptual domain randomization.
- **[paper]** [Closing the Sim-to-Real Loop: Bayesian Domain Randomization for Sim-to-Real Transfer](https://arxiv.org/pdf/1810.05687.pdf)
  Even if not full sysID, it is a canonical, citable sim-to-real training procedure that complements domain randomization posts with a rigorous, step-by-step method and concrete experimental evidence.
- **[paper]** [Reinforcement Learning for Humanoid Robot with Zero-Shot Sim-to-Real Transfer](https://arxiv.org/html/2404.05695v2)
  This is exactly the kind of modern, end-to-end sim-to-real robotics example students ask for (what to randomize, how to train, what results to expect), and it points to the Isaac ecosystem that the library currently lacks.
- **[paper]** [i-Sim2Real: Reinforcement Learning of Robotic Policies in Tight Human-Robot Interaction](https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf) *(promoted by reviewer)*
  This directly fills the missing “authoritative end-to-end sim-to-real” need with a concrete, reproducible procedure (explore→identify→train/optimize) rather than only conceptual domain randomization.
- **[paper]** [Closing the Sim-to-Real Loop: Bayesian Domain Randomization for Sim-to-Real Transfer](https://arxiv.org/pdf/1810.05687.pdf) *(promoted by reviewer)*
  Even if not full sysID, it is a canonical, citable sim-to-real training procedure that complements domain randomization posts with a rigorous, step-by-step method and concrete experimental evidence.
- **[paper]** [Reinforcement Learning for Humanoid Robot with Zero-Shot Sim-to-Real Transfer](https://arxiv.org/html/2404.05695v2) *(promoted by reviewer)*
  This is exactly the kind of modern, end-to-end sim-to-real robotics example students ask for (what to randomize, how to train, what results to expect), and it points to the Isaac ecosystem that the library currently lacks.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **DomainBed/domainbed/algorithms.py at main · facebookresearch** — [DomainBed/domainbed/algorithms.py at main · facebookresearch/DomainBed](https://github.com/facebookresearch/DomainBed/blob/main/domainbed/algorithms.py)
  _Skipped because:_ Useful for pinpointing algorithm implementations, but the repo-level entry is a better single reference for API surface, configs, and reproducibility context.
- **On Learning Invariant Representations for Domain Adaptation ** — [On Learning Invariant Representations for Domain Adaptation (Supplementary)](http://proceedings.mlr.press/v97/zhao19a/zhao19a-supp.pdf)
  _Skipped because:_ Valuable extra proofs/details, but the main paper already anchors the key theoretical statements; keep the library minimal.
- **Bayesian Domain Randomization for Sim-to-Real Transfer** — [Bayesian Domain Randomization for Sim-to-Real Transfer](http://www.arxiv.org/pdf/2003.02471v2.pdf)
  _Skipped because:_ Strong for domain randomization with Bayesian updating, but the missing need is specifically system identification and end-to-end sim-to-real codebases; this is more about optimizing randomization distributions than full sysID pipelines.
- **UDA-Bench: Revisiting Common Assumptions in ...** — [UDA-Bench: Revisiting Common Assumptions in ...](https://arxiv.org/html/2409.15264v1)
  _Skipped because:_ Likely overlaps with the other UDA benchmarking candidate; selected only one to stay within the total-additions cap.

## Reasoning
**Curator:** Selections prioritize (1) rigorous, citable theory for when/why adaptation works or fails, (2) authoritative benchmark/protocol sources for exact numbers, and (3) concrete procedural references and tooling that enable reproducible teaching examples; remaining gaps are specifically end-to-end sim-to-real robotics codebases and official simulator DR API docs.
**Reviewer:** The curator’s theory/benchmark/DG tooling choices are strong, but the library still lacks at least one authoritative, end-to-end sim-to-real robotics pipeline paper (with concrete procedures and results) to cover the stated unfilled needs.
