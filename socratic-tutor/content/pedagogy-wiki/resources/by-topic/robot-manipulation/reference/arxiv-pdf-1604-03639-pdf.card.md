# Card: MIT APC 2015 End-to-End Picking System (Perception→Primitives→Planning→Heuristic)
**Source:** https://arxiv.org/pdf/1604.03639.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** Deployed competition system architecture + concrete integration choices for shelf picking

## Key Content
- **Task setup (APC 2015):** 20 min autonomous run; 12 target bins in a **1.0 m (H) × 0.87 m (W) × 0.43 m (D)** region; bin openings vary (**19–22 cm** height, **25–30 cm** width) with lips that impede sliding/pulling. Items placed near front; not stacked/behind; not tightly packed.
- **Hardware choices & parameters (Sections IV-A/B):**
  - Arm: **ABB 1600ID**, tool max speed used **1 m/s**; hollow wrist for cable/air routing (maneuverability, fewer snags).
  - Gripper: **WSG-50** parallel jaw, **110 mm** opening, **70 N** max force; **force + position control** used for preloading spatula against shelf.
  - Custom fingers: thin aluminum plates; one finger has **compliant spring-steel spatula** (environment-assisted insertion); other integrates **suction cup** + in-line Venturi; **vacuum pressure sensor** for seal feedback.
  - Cameras: **2× Kinect2** (ToF, **0.8–4 m**, **512×424**) + arm-mounted **Intel RealSense** (structured light, **0.2–1.2 m**, **640×480**). Kinect2 IR can blind RealSense → cameras toggled during Percept primitive.
- **Software architecture (Section V, Fig. 7):** ROS-based; **central heuristic (state machine)** selects among **motion primitives** using camera + gripper encoder + suction pressure feedback; primitives executed via **Drake IK planner** (MATLAB; TCP+JSON interface).
- **Perception pipeline (Section V-A):**
  1) Transform pointcloud to shelf frame; filter outside shelf convex hull + NaNs.  
  2) Apply bin physical constraints (within walls; intersect thickened/up-shifted bin floor).  
  3) Run Capsen model-fitting on **depth-only** pointcloud + mask + constraints + known item IDs → multiple hypotheses with **log-likelihood scores** (IDs + 6D poses).  
  4) Reject hypotheses with COM outside bin; pick highest score.  
  5) Robustness: run **5×** on closest Kinect depth + **5×** on RealSense depth.
- **Motion primitives (Section V-B):** Percept (preselected 2 viewpoints/bin; IK with tolerance), Grasp (front approach; search pitch/yaw to avoid shelf lips; use spatula pretension if near wall), Scoop (preload spatula on floor via force control; push to back to capture), Suction (down/side; stop on contact via force control; verify expected contact height; up to **5 attempts** with XY jitter; confirm via pressure sensor), Topple (fast push above COM; re-perceive), Push-Rotate (reorient to expose graspable dimension; re-perceive).
- **Empirical outcome (Section VI):** Picked **7/12** items; **~7 min** before torque overload stop; scored **88 points**, **2nd** of 30+ teams. Initial failure: gripper reboot due to heavy TCP/IP traffic → **5 min** penalty.

## When to surface
Use for questions about real-world manipulation system integration: how to structure a shelf-picking pipeline, why primitives beat full planning for robustness/speed, and concrete sensing/gripper/calibration choices in a deployed competition robot.