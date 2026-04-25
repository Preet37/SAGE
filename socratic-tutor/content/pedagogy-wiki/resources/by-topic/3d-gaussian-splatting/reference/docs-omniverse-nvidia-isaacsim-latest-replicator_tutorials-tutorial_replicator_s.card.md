# Card: Isaac Sim + Omniverse Replicator (Scene-Based SDG) — Core Concepts
**Source:** https://docs.omniverse.nvidia.com/isaacsim/latest/replicator_tutorials/tutorial_replicator_scene_based_sdg.html?highlight=COCO  
**Role:** explainer | **Need:** WORKING_EXAMPLE  
**Anchor:** Step-by-step scene-based synthetic data generation (SDG) in Isaac Sim/Replicator (triggers, writers, annotations such as COCO) with runnable script patterns.

## Key Content
- **What Isaac Sim is (definition):** A reference application built on **NVIDIA Omniverse** for developing, simulating, and testing **AI-driven robots** in **physically-based virtual environments**.
- **Core enabling tech (design rationale):**
  - Uses **Universal Scene Description (USD)** as the *unifying interchange format* for scenes/assets; USD is **open-source**, **extensible**, and widely adopted across VFX, robotics, manufacturing, etc.
  - Simulation uses a **high-fidelity GPU-based PhysX engine**, enabling **industrial-scale** simulation and **multi-sensor RTX rendering**.
  - Direct GPU access supports simulated sensors: **cameras**, **RTX Lidars**, and **contact sensors**—used to build **digital twins** so pipelines can run before deploying on real robots.
- **Synthetic data workflow components (procedure-level pointers):**
  - Synthetic data collection is done with **Replicator** (SDG tooling).
  - Environment orchestration can be done through **Omnigraph**.
  - Physics realism can be tuned via **PhysX simulation parameters** to better match reality (sim-to-real).
- **Integration/deployment context (why it matters):**
  - Omniverse Kit provides plugin-based app infrastructure and a Python interpreter for scripting/extensions.
  - Bridges exist for **ROS 2** and integration with **NVIDIA Isaac ROS** for real robot communication.

## When to surface
Use when students ask how Isaac Sim/Omniverse structures scene-based synthetic data generation (Replicator), why USD is central, or how digital-twin simulation + RTX sensors + PhysX fit into an SDG pipeline for downstream tasks (e.g., 3D Gaussian Splatting training data).