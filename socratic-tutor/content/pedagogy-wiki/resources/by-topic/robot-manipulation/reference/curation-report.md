# Curation Report: Robot Manipulation
**Topic:** `robot-manipulation` | **Date:** 2026-04-09 16:33
**Library:** 2 existing → 13 sources (11 added, 8 downloaded)
**Candidates evaluated:** 50
**Reviewer verdict:** needs_additions

## Added (11)
- **[explainer]** [[PDF] Rigid Body Dynamics Algorithms](https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf)
  This is a canonical, equation-heavy reference for rigid-body dynamics with implementable algorithms, letting the tutor derive and compute manipulator dynamics precisely rather than hand-waving.
- **[benchmark]** [[PDF] MANISKILL-HAB: A BENCHMARK FOR LOW-LEVEL ...](https://proceedings.iclr.cc/paper_files/paper/2025/file/27aa3a0e6d63db269977bb2df5607cb8-Paper-Conference.pdf)
  Adds concrete, citable performance numbers and ablation-driven insights for contact-rich manipulation learning, supporting quantitative comparisons and discussion of what design choices matter.
- **[reference_doc]** [◆ Robot() [1/2]](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)
  Provides authoritative, vendor-maintained API details needed to teach how real-time manipulation controllers are actually implemented and what interfaces/constraints the SDK imposes.
- **[reference_doc]** [◆ setDefaultBehavior()](https://frankaemika.github.io/libfranka/examples__common_8h.html)
  Gives a concrete, citable “known-good” configuration pattern from official examples, useful for teaching safe defaults and typical initialization steps in manipulation pipelines.
- **[paper]** [[PDF] Lessons from the Amazon Picking Challenge: Four Aspects of ...](https://www.roboticsproceedings.org/rss12/p36.pdf)
  Adds real-world, end-to-end manipulation system considerations (robustness, integration, failure handling) that are often missing from purely algorithmic sources.
- **[paper]** [A Summary of Team MIT’s Approach to the Amazon Picking Challenge](https://arxiv.org/pdf/1604.03639.pdf)
  Even if less “lessons learned” focused than the chosen APC paper, it is an authoritative, implementation-oriented stack description that helps teach how a full manipulation system is assembled and debugged.
- **[paper]** [A Unified Complementarity-based Approach for Rigid-Body Dynamics and Contact](https://arxiv.org/html/2602.04522v1)
  This directly targets the currently unfilled contact modeling need (complementarity + Coulomb friction) with a unified, equation-heavy treatment suitable for precise derivations and solver-ready formulations.
- **[paper]** [Visuomotor Policy Learning via Action Diffusion](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf)
  The library currently has contact-rich benchmark numbers (ManiSkill-HAB) but lacks a canonical, procedure-rich reference for modern imitation-learning pipelines that are widely used for manipulation.
- **[paper]** [A Summary of Team MIT’s Approach to the Amazon Picking Challenge](https://arxiv.org/pdf/1604.03639.pdf) *(promoted by reviewer)*
  Even if less “lessons learned” focused than the chosen APC paper, it is an authoritative, implementation-oriented stack description that helps teach how a full manipulation system is assembled and debugged.
- **[paper]** [A Unified Complementarity-based Approach for Rigid-Body Dynamics and Contact](https://arxiv.org/html/2602.04522v1) *(promoted by reviewer)*
  This directly targets the currently unfilled contact modeling need (complementarity + Coulomb friction) with a unified, equation-heavy treatment suitable for precise derivations and solver-ready formulations.
- **[paper]** [Visuomotor Policy Learning via Action Diffusion](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf) *(promoted by reviewer)*
  The library currently has contact-rich benchmark numbers (ManiSkill-HAB) but lacks a canonical, procedure-rich reference for modern imitation-learning pipelines that are widely used for manipulation.

## Near-Misses (3) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **franka_ros2** — [franka_ros2](https://frankaemika.github.io/docs/franka_ros2.html?highlight=test)
  _Skipped because:_ Useful for ROS 2 integration, but the candidate snippet is mostly example-launch narrative and is less directly citable for precise API defaults than the libfranka class/API pages.
- **ManiSkill-HAB: A Benchmark for Low-Level Manipulation in ...** — [ManiSkill-HAB: A Benchmark for Low-Level Manipulation in ... - arXiv](https://arxiv.org/html/2412.13211v3)
  _Skipped because:_ Same work as the PDF version; kept the PDF as the more stable, citable artifact for tables/ablations.
- **Analysis and Observations from the First Amazon Picking Chal** — [Analysis and Observations from the First Amazon Picking Challenge](https://arxiv.org/abs/1601.05484)
  _Skipped because:_ Relevant APC context, but the selected RSS lessons paper is more directly focused on manipulation-system takeaways rather than fulfillment-center picking logistics/metrics.

## Reasoning
**Curator:** Selections prioritize authoritative, equation- and table-heavy sources (Featherstone; ManiSkill-HAB) plus official SDK references (libfranka) and a real-world deployment lessons paper (APC) to balance precise derivations, empirical benchmarks, and practical system constraints.
**Reviewer:** The curator’s picks are strong, but adding one APC system-architecture paper, one complementarity-based contact modeling formula source, and one canonical modern manipulation learning pipeline paper would materially improve concept coverage and teachability.
