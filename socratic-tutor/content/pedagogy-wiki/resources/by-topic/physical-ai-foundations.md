# Physical AI Foundations

## Video (best)
- **MIT OpenCourseWare / Russ Tedrake** — "Underactuated Robotics Lecture Series (Perception & Control)"
- url: https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/
- Why: Russ Tedrake's MIT 6.832 lectures are the closest rigorous academic treatment of the perception-action loop, embodied intelligence, and autonomous systems foundations. However, no single YouTube video cleanly covers "Physical AI Foundations" as a unified topic with the sensor fusion + embodied intelligence framing used in modern Physical AI discourse.
- Level: advanced

> ⚠️ **Coverage Gap Note:** No single YouTube explainer from the preferred educators (3Blue1Brown, Karpathy, Yannic, StatQuest) covers Physical AI Foundations as a unified concept. The term "Physical AI" as used by NVIDIA/industry (convergence of perception, action, and embodied intelligence) is too recent (2023–2024) for polished explainers to exist.

**Best available alternative:**
- **NVIDIA GTC Keynote clips** — Jensen Huang's GTC 2024 "Physical AI" segment on YouTube provides the conceptual framing, but is a product keynote, not a pedagogical resource. [Video ID: _waPvOwL9Z8 (GTC March 2025 Keynote)]

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Autonomous Agents" (covers embodied intelligence, perception-action loops, and agent grounding)
- url: https://lilianweng.github.io/posts/2023-06-23-agent/
- Why: Weng's characteristic depth and clarity covers the cognitive architecture underlying Physical AI — perception, memory, action, and tool use — with rigorous citations. While not exclusively about robotics hardware, it is the best written explainer from a trusted educator that addresses the embodied intelligence and perception-action loop concepts central to this topic. Her treatment bridges the gap between LLM-based reasoning and physical grounding.
- Level: intermediate/advanced

---

## Deep dive
- **Author/Source** — Russ Tedrake, "Robotic Manipulation: Perception, Planning, and Control" (MIT Open Textbook)
- url: https://manipulation.csail.mit.edu/
- Why: This is the most comprehensive freely available technical reference covering the full stack of Physical AI: depth cameras, sensor fusion, perception-action loops, grasping, and manipulation planning. Written by one of the field's leading researchers, it includes code, lecture notes, and problem sets. Covers sim-to-real, tactile sensing concepts, and safety considerations. Far more rigorous than any blog post for learners who need implementation depth.
- Level: advanced

---

## Original paper
- **None identified** — Physical AI as a unified concept does not have a single seminal "founding paper" in the way that, e.g., the Transformer or AlexNet do. The topic is a convergence of multiple subfields.

**Closest candidates (use with caveat):**
- For embodied intelligence: Pfeifer & Bongard's work, or the RT-2 paper (arxiv.org/abs/2307.15818) for vision-language-action models
- For sensor fusion foundations: No single canonical paper
- For tactile sensing (GelSight): Yuan et al., 2017 — "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force" https://pmc.ncbi.nlm.nih.gov/articles/PMC5751610/

> Recommendation: Do not force a single paper here. Assign RT-2 + one tactile sensing paper as a paired reading instead.

---

## Code walkthrough
- **Source** — MIT Manipulation Course Notebooks (Drake-based)
- url: https://manipulation.csail.mit.edu/clutter.html
- Why: Tedrake's course provides runnable Jupyter/Colab notebooks using the Drake simulator that walk through perception pipelines (depth cameras, point clouds), grasp planning, and sensor integration — directly mapping to the core concepts of Physical AI Foundations. These are the most pedagogically complete hands-on implementations available for this topic from a credible academic source.
- Level: advanced

**Alternative for beginners:**
- NVIDIA Isaac Sim tutorials cover sensor fusion and robot perception in a more accessible way, but require proprietary software setup. [NOT VERIFIED]

---

## Coverage notes
- **Strong:** Perception-action loop, embodied intelligence (conceptual), manipulation and depth cameras (Tedrake's materials), autonomous systems architecture
- **Weak:** Tactile sensing (GelSight) — no strong standalone tutorial exists outside research lab pages; LiDAR-specific educational content tends to live in autonomous driving courses, not general Physical AI courses
- **Weak:** Safety certification for physical AI systems — this is a genuine educational gap; most content is either too theoretical (formal verification literature) or too domain-specific (automotive ISO 26262)
- **Gap:** No high-quality beginner-to-intermediate YouTube series exists for Physical AI Foundations as a unified topic. This is a significant gap for the platform — original content creation would add real value here.
- **Gap:** Sensor fusion for humanoid robots specifically (as opposed to autonomous vehicles) has almost no dedicated educational resources outside of proprietary robot SDK documentation.

---

## Last Verified
2025-01-01 (resource landscape as of knowledge cutoff; URLs marked must be checked before publication)