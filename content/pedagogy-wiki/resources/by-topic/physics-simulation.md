# Physics Simulation

## Video (best)
- **Two Minute Papers** — "OpenAI Trains a Hand to Solve a Rubik's Cube"
- url: https://openai.com/research/solving-rubiks-cube
- Why: No single YouTube video cleanly covers the full scope of physics simulation for robotics/AI (domain randomization, MuJoCo, Isaac Sim, parallel simulation together). Two Minute Papers covers adjacent results but not the pedagogical fundamentals.
- Level: intermediate

> **Note:** No excellent dedicated explainer video exists on YouTube that covers physics simulation for Physical AI as a unified topic. The closest candidates are NVIDIA GTC talks (not on YouTube in standard form) and scattered robotics lectures.

**Partial alternative:**
- **Yannic Kilcher** — covers RT-X and foundation model papers but not simulation infrastructure
- **Stanford CS329L / CS336** lectures touch on sim-to-real but are not cleanly indexed as standalone YouTube videos

## Blog / Written explainer (best)
- **Lilian Weng** — "Domain Randomization for Sim-to-Real Transfer"
- url: https://lilianweng.github.io/posts/2019-05-05-domain-randomization/
- Why: Weng's post is the most cited, pedagogically structured written explainer on domain randomization — the core technique linking physics simulation to real-world robot learning. It covers the motivation, taxonomy (uniform vs. structured randomization), and key results with clear diagrams. Directly relevant to MuJoCo/Isaac Sim workflows.
- Level: intermediate

## Deep dive
- **MuJoCo Documentation & Technical Reference** — DeepMind/Google
- url: https://mujoco.readthedocs.io/en/stable/overview.html
- Why: The official MuJoCo docs are the most comprehensive technical reference for physics simulation in AI/ML robotics contexts. They cover rigid body dynamics, contact modeling, actuator models, and integration with Python/RL frameworks. MuJoCo is the de facto standard simulator for the concepts in this topic cluster (Octo, RT-X, and most foundation model robot training use it).
- Level: advanced

## Original paper
- **Todorov et al. (2012)** — "MuJoCo: A physics engine for model-based control"
- url: https://homes.cs.washington.edu/~todorov/papers/TodorovIROS12.pdf
- Why: MuJoCo is the foundational simulator underpinning the majority of modern robot learning research. This paper introduces the core design philosophy — fast, differentiable, contact-rich simulation — that makes it suitable for RL and imitation learning at scale. Readable and concise (~6 pages).
- Level: advanced

**Honorable mention for domain randomization:**
- Tobin et al. (2017) "Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World"
- url: https://arxiv.org/abs/1703.06907
- Why: The seminal paper establishing domain randomization as a practical sim-to-real technique.

## Code walkthrough
- **NVIDIA Isaac Lab Tutorials** — Official hands-on implementation notebooks
- url: https://isaac-sim.github.io/IsaacLab/main/source/tutorials/index.html
- Why: Isaac Lab (built on Isaac Sim) provides the most complete code walkthrough for modern GPU-accelerated parallel simulation, directly covering concepts like domain randomization, rigid body dynamics, and integration with robot learning pipelines. The tutorials progress from environment setup through RL training with domain randomization — matching the topic's concept list most completely.
- Level: intermediate/advanced

**Alternative for MuJoCo specifically:**
- DeepMind MuJoCo Colab tutorials: https://github.com/google-deepmind/mujoco/tree/main/python/tutorial [NOT VERIFIED]

---

## Coverage notes
- **Strong:** Domain randomization (Lilian Weng blog is excellent), MuJoCo fundamentals (official docs + paper), Isaac Sim code (official tutorials)
- **Weak:** NVIDIA GR00T and Octo-specific simulation pipelines — these are very new (2024) and pedagogical resources lag behind
- **Gap:** No high-quality YouTube video exists that unifies physics simulation + domain randomization + parallel GPU simulation + foundation model robotics as a single explainer. This is a genuine content gap in the public AI education ecosystem as of early 2025.
- **Gap:** Photorealistic rendering for sim-to-real (NeRF/Gaussian Splatting in simulation loops) has almost no dedicated pedagogical coverage yet.
- **Gap:** RT-X dataset and its relationship to simulation is covered in the paper but not in accessible tutorial form.

## Last Verified
2025-01-15 (resource existence checked against known publications; Isaac Lab URL structure as docs reorganize frequently)