# Curation Report: Physics Simulation
**Topic:** `physics-simulation` | **Date:** 2026-04-09 16:28
**Library:** 6 existing → 17 sources (11 added, 8 downloaded)
**Candidates evaluated:** 49
**Reviewer verdict:** needs_additions

## Added (11)
- **[paper]** [Robotic Learning Datasets and RT-X Models](https://arxiv.org/abs/2310.08864)
  Gives an end-to-end, citable description of how large robot foundation policies are trained from heterogeneous data, including the concrete representation choices a tutor must explain precisely.
- **[benchmark]** [SimBenchmark | Physics engine benchmark for robotics applications](https://leggedrobotics.github.io/SimBenchmark/)
  Provides structured, task-driven comparisons that help a tutor explain practical differences between engines (contact handling, stability, speed) with quantitative evidence.
- **[paper]** [Isaac Gym: High Performance GPU Based Physics](https://datasets-benchmarks-proceedings.neurips.cc/paper/2021/file/28dd2c7955ce926456240b2ff0100bde-Paper-round2.pdf)
  Directly supports teaching large-scale parallel simulation deployment: architecture choices, throughput claims, and the concrete mechanism that removes CPU bottlenecks.
- **[reference_doc]** [Index](https://docs.omniverse.nvidia.com/py/isaacsim/genindex.html)
  Best single entry point for precise, citable API details when students ask “what is the exact parameter/property name and where is it set?” across Isaac Sim components.
- **[reference_doc]** [Physics Simulation Fundamentals](https://docs.omniverse.nvidia.com/isaacsim/latest/simulation_fundamentals.html?highlight=Deformable%2520Body)
  Adds the conceptual and procedural grounding needed to explain how Isaac Sim/Omniverse physics actually advances state each timestep and how that relates to controller/policy integration.
- **[paper]** [Robust visual sim-to-real transfer for robotic manipulation](https://arxiv.org/pdf/2307.15320.pdf)
  This directly targets the still-unfilled need (empirical comparisons of sim-to-real strategies) and is more on-point than engine-performance KPIs; it provides concrete outcome metrics rather than just descriptive guidance.
- **[paper]** [A Review of Nine Physics Engines for Reinforcement Learning](https://arxiv.org/html/2407.08590v1)
  Even if SimBenchmark is the primary benchmark hub, this review can serve as a high-level, citable synthesis that helps a tutor explain why engines differ and how to choose among them, with broader coverage than a single benchmark suite.
- **[paper]** [Octo: An Open-Source Generalist Robot Policy](https://octo-models.github.io/paper.pdf)
  The curator rejected Octo as redundant with RT-X, but Octo is a fully specified, open-source-aligned reference with implementation-facing design rationale that often answers “how exactly is this trained?” questions better than dataset/model overview papers.
- **[paper]** [Robust visual sim-to-real transfer for robotic manipulation](https://arxiv.org/pdf/2307.15320.pdf) *(promoted by reviewer)*
  This directly targets the still-unfilled need (empirical comparisons of sim-to-real strategies) and is more on-point than engine-performance KPIs; it provides concrete outcome metrics rather than just descriptive guidance.
- **[paper]** [A Review of Nine Physics Engines for Reinforcement Learning](https://arxiv.org/html/2407.08590v1) *(promoted by reviewer)*
  Even if SimBenchmark is the primary benchmark hub, this review can serve as a high-level, citable synthesis that helps a tutor explain why engines differ and how to choose among them, with broader coverage than a single benchmark suite.
- **[paper]** [Octo: An Open-Source Generalist Robot Policy](https://octo-models.github.io/paper.pdf) *(promoted by reviewer)*
  The curator rejected Octo as redundant with RT-X, but Octo is a fully specified, open-source-aligned reference with implementation-facing design rationale that often answers “how exactly is this trained?” questions better than dataset/model overview papers.

## Near-Misses (4) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Octo: An Open-Source Generalist Robot Policy - arXiv** — [Octo: An Open-Source Generalist Robot Policy - arXiv](https://arxiv.org/abs/2405.12213)
  _Skipped because:_ Excellent for generalist policy training details, but the RT-X/Open X-Embodiment paper better matches the requested sim-vs-real mixture and standardized representation focus for a single-slot concept explainer.
- **Predictable behavior during contact simulation: a comparison** — [Predictable behavior during contact simulation: a comparison of ...](http://graphics.cs.cmu.edu/nsp/papers/ChungCAVW2016.pdf)
  _Skipped because:_ Strong contact-simulation comparison, but SimBenchmark is more up-to-date, broader, and maintained as a structured benchmark hub the tutor can reuse.
- **Simulation Performance Guide#** — [Simulation Performance Guide#](https://docs.omniverse.nvidia.com/kit/docs/omni_physics/106.5/dev_guide/guides/physics-performance.html)
  _Skipped because:_ Useful tuning guidance, but it is less directly about authoritative defaults/parameters than the Isaac Sim API index and fundamentals page given the limited slots.
- **Demonstrating GPU Parallelized Robot Simulation and ...** — [Demonstrating GPU Parallelized Robot Simulation and ...](https://arxiv.org/html/2410.00425v2)
  _Skipped because:_ Promising deployment/throughput content (ManiSkill3), but Isaac Gym is the more seminal, widely cited GPU-parallel sim deployment reference for robotics RL.

## Reasoning
**Curator:** Selections prioritize authoritative, citable sources that directly add missing capabilities: (1) foundation-model training pipeline details (RT-X/Open X-Embodiment), (2) quantitative engine comparisons (SimBenchmark), (3) real deployment architecture and throughput claims (Isaac Gym), and (4) official Isaac Sim API/procedural references for precise parameter and pipeline questions.
**Reviewer:** The curation is strong on engines and GPU simulation, but it still lacks a solid empirical sim-to-real strategy comparison source and would benefit from one synthesis-style engine comparison paper plus an implementation-detailed generalist-policy training reference.
