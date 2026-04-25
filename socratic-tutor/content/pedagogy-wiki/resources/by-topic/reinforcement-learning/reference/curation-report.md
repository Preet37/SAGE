# Curation Report: Reinforcement Learning
**Topic:** `reinforcement-learning` | **Date:** 2026-04-09 16:33
**Library:** 9 existing → 23 sources (14 added, 10 downloaded)
**Candidates evaluated:** 38
**Reviewer verdict:** needs_additions

## Added (14)
- **[paper]** [Soft Actor-Critic: Off-Policy Maximum Entropy Deep Reinforcement Learning with a Stochastic Actor](https://proceedings.mlr.press/v80/haarnoja18b/haarnoja18b.pdf)
  This is the primary, citable SAC formulation with the equations and training procedure needed for precise tutoring beyond blog-level summaries.
- **[paper]** [[1812.05905] Soft Actor-Critic Algorithms and Applications](https://arxiv.org/abs/1812.05905)
  Complements the original SAC paper with the widely-used temperature auto-tuning formulation and clearer end-to-end algorithm details.
- **[benchmark]** [Benchmarks for Spinning Up Implementations](https://spinningup.openai.com/en/latest/spinningup/bench.html)
  Provides directly comparable empirical numbers for PPO and SAC on canonical continuous-control tasks, useful for answering “which is better and by how much?” with citations.
- **[paper]** [[1709.06560] Deep Reinforcement Learning that Matters](https://arxiv.org/abs/1709.06560)
  Adds critical context for interpreting PPO-vs-SAC benchmark numbers and teaches students why single-score comparisons can be misleading.
- **[paper]** [[1912.12294] Learning by Cheating](https://arxiv.org/abs/1912.12294)
  Gives an end-to-end, design-rationale-heavy driving RL pipeline that concretely explains how perception and control are integrated via privileged training and distillation.
- **[paper]** [[1901.08652] Learning agile and dynamic motor skills for legged robots](https://arxiv.org/abs/1901.08652)
  A strong near-production robotics RL case study with concrete system architecture and evaluation, ideal for teaching deployment constraints and sim2real methodology.
- **[paper]** [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347)
  The library already contains this arXiv ID, but the curator’s “still-unfilled need” indicates they haven’t anchored PPO’s exact math to the authors’ paper; this is the canonical formula source needed for precise tutoring.
- **[paper]** [Proximal Policy Optimization Algorithms (revised arXiv version)](https://arxiv.org/abs/1707.06347v2)
  If the library entry points to a generic record, pinning a specific stable version helps avoid equation/notation drift across revisions when students ask for exact objectives.
- **[benchmark]** [mujoco-benchmark (Tianshou-based MuJoCo benchmark suite)](https://github.com/ChenDRAG/mujoco-benchmark)
  Even if not as canonical as Spinning Up, it provides additional specific numbers and cross-algorithm comparisons that help answer “how big is the gap?” and triangulate results beyond one benchmark source.
- **[benchmark]** [Policy Information Capacity (supplementary: benchmark details)](http://proceedings.mlr.press/v139/furuta21a/furuta21a-supp.pdf)
  The snippet looks like “just a link,” but the supplement is where the concrete benchmark numbers and settings live—useful for teaching evaluation rigor and for citing specific results.
- **[paper]** [Proximal Policy Optimization Algorithms](https://arxiv.org/abs/1707.06347) *(promoted by reviewer)*
  The library already contains this arXiv ID, but the curator’s “still-unfilled need” indicates they haven’t anchored PPO’s exact math to the authors’ paper; this is the canonical formula source needed for precise tutoring.
- **[paper]** [Proximal Policy Optimization Algorithms (revised arXiv version)](https://arxiv.org/abs/1707.06347v2) *(promoted by reviewer)*
  If the library entry points to a generic record, pinning a specific stable version helps avoid equation/notation drift across revisions when students ask for exact objectives.
- **[benchmark]** [mujoco-benchmark (Tianshou-based MuJoCo benchmark suite)](https://github.com/ChenDRAG/mujoco-benchmark) *(promoted by reviewer)*
  Even if not as canonical as Spinning Up, it provides additional specific numbers and cross-algorithm comparisons that help answer “how big is the gap?” and triangulate results beyond one benchmark source.
- **[benchmark]** [Policy Information Capacity (supplementary: benchmark details)](http://proceedings.mlr.press/v139/furuta21a/furuta21a-supp.pdf) *(promoted by reviewer)*
  The snippet looks like “just a link,” but the supplement is where the concrete benchmark numbers and settings live—useful for teaching evaluation rigor and for citing specific results.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **[PDF] Learning by Cheating** — [[PDF] Learning by Cheating](http://proceedings.mlr.press/v100/chen20a/chen20a.pdf)
  _Skipped because:_ Redundant with the arXiv version; kept only one canonical entry to conserve library slots.
- **Learning by cheating** — [Learning by cheating](https://ar5iv.labs.arxiv.org/html/1912.12294)
  _Skipped because:_ HTML mirror is convenient but less canonical than the arXiv record for citation and long-term stability.
- **Learning dexterity | OpenAI** — [Learning dexterity | OpenAI](https://openai.com/index/learning-dexterity/)
  _Skipped because:_ Excellent narrative and visuals, but the arXiv/SciRobotics-style papers are more equation/procedure/metric dense for a reference library.
- **[1808.00177] Learning Dexterous In-Hand Manipulation** — [[1808.00177] Learning Dexterous In-Hand Manipulation](https://arxiv.org/abs/1808.00177)
  _Skipped because:_ Strong deployment case, but only one deployment slot remained and the legged-locomotion paper provides broader system-architecture and control-stack details for tutoring.

## Reasoning
**Curator:** Selections prioritize primary-source equations (SAC), standardized benchmark numbers plus reproducibility context, and concrete end-to-end pipelines/case studies for driving and real-robot deployment. PPO’s original formulation is not present among candidates, so it is left explicitly unfilled with a targeted search hint.
**Reviewer:** The curator’s core picks are strong, but they missed that PPO’s own paper already in the library should be explicitly used to fill the unfilled PPO-formula need, and a couple of candidate benchmark sources add valuable concrete numbers for cross-checking PPO/SAC performance.
