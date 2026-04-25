# Card: Isaac Sim simulation fundamentals (USD ↔ PhysX pipeline)
**Source:** https://docs.omniverse.nvidia.com/isaacsim/latest/simulation_fundamentals.html?highlight=Deformable%2520Body  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** System-level description of Isaac Sim’s simulation stack: USD scene representation, PhysX GPU simulation, sensor simulation, and integration points (ROS 2, Omnigraph, Replicator, Isaac Lab).

## Key Content
- **Core purpose (What Isaac Sim is):** A reference application on **NVIDIA Omniverse Kit** for developing, simulating, and testing **AI-driven robots** in **physically-based virtual environments**.
- **Scene representation (USD):**
  - Isaac Sim uses **Universal Scene Description (USD)** as the **unifying data interchange format** at the heart of the platform.
  - USD is described as **extensible**, **open source**, and used broadly beyond VFX (architecture, robotics, manufacturing).
- **Physics + rendering backend:**
  - Simulation uses a **high-fidelity GPU-based PhysX engine**.
  - Supports **multi-sensor RTX rendering** “at industrial scale.”
  - Sensor simulation examples explicitly listed: **cameras**, **RTX Lidars**, **contact sensors**.
- **Workflow/toolchain integration points:**
  - **Import** workflows: **Onshape**, **URDF**, **MuJoCo XML (MJCF)**.
  - **Synthetic data**: **Replicator**.
  - **Graph orchestration**: **Omnigraph**.
  - **Physics tuning**: PhysX simulation parameter tuning to match reality.
  - **Training/control**: **Isaac Lab** for RL training of control agents.
  - **Deployment/bridging**: **ROS 2 bridge APIs** + integration with **NVIDIA Isaac ROS** packages.
- **Architecture rationale:**
  - Built on **Omniverse Kit** plugin system (lightweight plugins; C interfaces for API compatibility; Python interpreter for scripting).
  - Designed to **collaborate with existing tools**, not replace them; supports standalone apps or partial integration.

## When to surface
Use when students ask how Isaac Sim is structured (USD/Kit/PhysX), what components handle physics vs sensors vs data generation, or what import/ROS/RL tooling is officially part of the Isaac Sim workflow.