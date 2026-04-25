# Card: Amazon Picking Challenge (APC) Winning System — System-Building Lessons
**Source:** https://www.roboticsproceedings.org/rss12/p36.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** System-level lessons from APC deployments: integration choices, feedback-heavy manipulation, failure modes, reliability numbers.

## Key Content
- **Task & scoring (Sec. II):** Pick **12/25** known-bin objects from **12 bins** in **20 min**. Correct pick: **10/15/20 pts** depending on **0–3** extra objects in bin; difficult-object bonus **up to +3**; wrong object **−12**.
- **Environment constraints (Sec. II):** Bin opening **21×28 cm**, depth **43 cm**; reflective metal floors degrade RGB-D; harsh lighting (front “white”, back “black”).
- **Hardware (Sec. III-A):**
  - **7-DOF Barrett WAM** on **holonomic XR4000 base** → **10 holonomic DOF** total; mobility simplifies reaching; avoids high-DOF motion planning by using feedback controllers.
  - **Suction end-effector:** vacuum cleaner **250 W**, lifts **up to 1.5 kg**; thin nozzle fits between objects; grasp success insensitive to exact contact → relaxes perception/pose accuracy. Fails on **meshed pencil cup**.
  - Sensors: arm RGB-D (Asus XTion), wrist **6-axis F/T**, tube pressure sensor, base laser (SICK LMS-200).
- **Motion generation (Sec. III-B):** Two primitives:
  - **Top-down:** descend until F/T contact, then suction.
  - **Side:** force-guarded push orthogonal to wall to align object, then suction.
  - Execution via **hybrid automaton**: example primitive **26 states / 50 transitions**, **34** for error handling (retract/reattempt on collisions; pressure detects grasp failure).
- **Perception pipeline (Sec. III-C, Fig. 7):** Shelf tracking via **ICP** → crop bin → per-pixel features (6): hue/white-gray-black, edge, distance-to-shelf, height-above-ground, image-plane height (if no depth), depth-present flag → histogram likelihoods from manually segmented training → per-pixel class probabilities (only objects known in bin + bin) → smooth/argmax labeling → select segment with max target prob → point cloud → outlier filter → **bounding box fit** (size constrained to known object dims) for approach direction.
- **Empirical results (Sec. IV):**
  - Competition: **148/190 (77.8%)**, **10/12** targets; avg pick **87 s**; 2nd place **88**, 3rd **35**.
  - Post-hoc: **200 min**, **95** picks, **85** targets; mean **117.6 pts (σ=29.2)** = **62.5%** of available; only **1/10** trials would place 2nd.
  - Failures over **120 attempts** (Table I): **13** recognition; **9** bulky stuck at removal; **9** small objects missed (open-loop FK error **up to 1 cm**); **2** displaced objects; **2** pencil cup (unpickable).
- **Design rationale (Sec. V):** Favor **tight integration**, **embodiment** (simple suction), **feedback over planning** (most teams used motion planning; **80%** used it, **44%** MoveIt), and **task-specific assumptions** (known shelf + known bin contents) to achieve robustness; planning needed for in-bin reorientation of bulky items.

## When to surface
Use for questions about why APC-style systems prioritize feedback primitives + embodiment, how hybrid automata enable robust error handling, and what concrete failure modes/metrics appear in real deployments.