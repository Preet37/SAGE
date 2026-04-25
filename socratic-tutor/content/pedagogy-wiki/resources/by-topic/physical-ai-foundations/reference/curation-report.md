# Curation Report: Physical AI Foundations
**Topic:** `physical-ai-foundations` | **Date:** 2026-04-09 16:28
**Library:** 2 existing → 16 sources (14 added, 10 downloaded)
**Candidates evaluated:** 46
**Reviewer verdict:** needs_additions

## Added (14)
- **[reference_doc]** [Quality of Service settings — ROS 2 Documentation](https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
  Gives authoritative, citable ROS 2 middleware semantics needed to teach real-time perception/control tradeoffs (best-effort vs reliable, transient-local vs volatile) and how QoS choices affect latency and data loss.
- **[paper]** [RT-2: Vision-Language-Action Models](https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)
  Provides concrete, widely-cited quantitative results for multimodal (vision+language+action) policies and a clear description of the VLA tokenization/training pipeline that connects web-scale pretraining to robot control.
- **[paper]** [Visuomotor Policy Learning via Action Diffusion - arXiv](https://arxiv.org/abs/2303.04137)
  Adds a strong, modern baseline with explicit training/inference procedure and broad benchmark coverage, useful for teaching sample efficiency and policy class tradeoffs versus BC/RL.
- **[paper]** [Assessing the Robustness of LiDAR, Radar and Depth Cameras ...](https://arxiv.org/html/2309.10504)
  Supports structured modality tradeoff discussions with empirical evidence (not just qualitative claims), helping the tutor justify sensor selection and fusion motivations.
- **[explainer]** [[PDF] Waymo Safety Case Approach White Paper](https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf)
  Provides a real-world, production-oriented safety-case methodology that the tutor can use to explain how autonomy systems are validated and argued safe beyond pure model performance.
- **[benchmark]** [Waymo Public Road Safety Performance Data](https://storage.googleapis.com/sdc-prod/v1/safety-report/Waymo-Public-Road-Safety-Performance-Data.pdf)
  Adds quantitative, deployment-grade reliability/safety performance data that can ground discussions of real-world autonomy evaluation and monitoring.
- **[reference_doc]** [Probabilistic Robotics (Thrun, Burgard, Fox) — PDF](https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf)
  This is the canonical, equation-heavy reference for estimation foundations; it directly fills the missing core math need with derivations and standard notation that a tutor can cite precisely.
- **[paper]** [Visuomotor Policy Learning via Action Diffusion (Diffusion Policy) — IJRR PDF](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf)
  The curator added an arXiv version, but the IJRR/RSS camera-ready PDF is more stable/citable and typically contains the cleanest algorithm box, hyperparameters, and final tables—ideal for a reference library.
- **[paper]** [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion — RSS 2023 Proceedings](https://roboticsproceedings.org/rss19/p026.pdf)
  Proceedings PDFs are archival and less likely to change than arXiv/website mirrors; this is the version most suitable for precise citations of the training/inference pipeline and reported numbers.
- **[code]** [sensor-fusion (KF/EKF/UKF with Radar/LiDAR models) — GitHub](https://github.com/TheGreatGalaxy/sensor-fusion)
  While not as authoritative as a textbook, it provides executable, inspectable implementations that help a tutor connect the math (state-space, Jacobians, noise matrices) to real sensor fusion pipelines.
- **[reference_doc]** [Probabilistic Robotics (Thrun, Burgard, Fox) — PDF](https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf) *(promoted by reviewer)*
  This is the canonical, equation-heavy reference for estimation foundations; it directly fills the missing core math need with derivations and standard notation that a tutor can cite precisely.
- **[paper]** [Visuomotor Policy Learning via Action Diffusion (Diffusion Policy) — IJRR PDF](https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf) *(promoted by reviewer)*
  The curator added an arXiv version, but the IJRR/RSS camera-ready PDF is more stable/citable and typically contains the cleanest algorithm box, hyperparameters, and final tables—ideal for a reference library.
- **[paper]** [Diffusion Policy: Visuomotor Policy Learning via Action Diffusion — RSS 2023 Proceedings](https://roboticsproceedings.org/rss19/p026.pdf) *(promoted by reviewer)*
  Proceedings PDFs are archival and less likely to change than arXiv/website mirrors; this is the version most suitable for precise citations of the training/inference pipeline and reported numbers.
- **[code]** [sensor-fusion (KF/EKF/UKF with Radar/LiDAR models) — GitHub](https://github.com/TheGreatGalaxy/sensor-fusion) *(promoted by reviewer)*
  While not as authoritative as a textbook, it provides executable, inspectable implementations that help a tutor connect the math (state-space, Jacobians, noise matrices) to real sensor fusion pipelines.

## Near-Misses (5) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Quality of Service settings — ROS 2 Documentation** — [Quality of Service settings — ROS 2 Documentation](https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Quality-of-Service-Settings.html)
  _Skipped because:_ Rolling can change and is less stable for citing defaults than a fixed release (Iron).
- **About Quality of Service settings — ROS 2 Documentation: Gal** — [About Quality of Service settings — ROS 2 Documentation: Galactic ...](https://docs.ros.org/en/galactic/Concepts/About-Quality-of-Service-Settings.html)
  _Skipped because:_ Older release; Iron is a better balance of stability and modern ROS 2 behavior.
- **sensor_msgs/PointCloud2 Documentation** — [sensor_msgs/PointCloud2 Documentation](http://docs.ros.org/en/noetic/api/sensor_msgs/html/msg/PointCloud2.html)
  _Skipped because:_ ROS 1 (Noetic) message docs are useful but don’t address ROS 2 QoS defaults/specs that were explicitly requested.
- **Graph-Based vs. Error State Kalman Filter- ...** — [Graph-Based vs. Error State Kalman Filter- ...](https://arxiv.org/pdf/2404.00691.pdf)
  _Skipped because:_ Strong for filter-vs-graph SLAM comparison, but the chosen modality-robustness paper better matches the sensing-modality comparison need.
- **Accelerating the pace of learning** — [Accelerating the pace of learning](https://waymo.com/blog/2017/02/accelerating-pace-of-learning)
  _Skipped because:_ Blog post is less citable/technical than the safety-case white paper and the performance-data PDF.

## Reasoning
**Curator:** Selections prioritize authoritative, citable documents that add either hard defaults/specs (ROS 2 QoS) or concrete quantitative results and deployment-grade metrics (RT-2, Diffusion Policy, Waymo). Needs without adequate candidates (control/estimation formulas and vendor SDK specs) are left unfilled with targeted search hints.
**Reviewer:** The curator’s additions are strong for ROS 2 QoS, VLA policies, and deployment safety, but the library still needs a canonical estimation/control math reference and should prefer stable camera-ready Diffusion Policy PDFs for citable procedures and tables.
