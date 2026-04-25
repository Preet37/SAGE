# Card: Isaac Sim Python API Index (Physics/Simulation/DR)
**Source:** https://docs.omniverse.nvidia.com/py/isaacsim/genindex.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative Python API surface + config/workflow snippets for Isaac Sim / Isaac Lab (simulation stepping, scene setup, articulations, sensors, domain randomization).

## Key Content
- **Core simulation/world callbacks (lookup exact signatures in index):**  
  `SimulationContext.add_physics_callback()`, `add_render_callback()`, `add_stage_callback()`, `add_timeline_callback()`; corresponding clears: `clear_physics_callbacks()`, `clear_render_callbacks()`, `clear_stage_callbacks()`, `clear_timeline_callbacks()`. Also `World.add_task()`, `World.add_world_view()`, `World.clear()`.
- **Scene construction primitives:**  
  `Scene.add_default_ground_plane()`, `Scene.add_ground_plane()`, `WorldInterface.add_cuboid()/add_sphere()/add_cone()/add_cylinder()`, `SceneRegistry.add_rigid_object()/add_robot()/add_sensor()` and `*_view()` variants.
- **Articulation control API surface:**  
  `Articulation.apply_action()`, `ArticulationController.apply_action()`, `ArticulationView.apply_action()`; DOF metadata: `dof_names`, `dof_properties`; body metadata: `body_names`.
- **PhysicsContext toggles:** `PhysicsContext.enable_gpu_dynamics()`, `enable_fabric()`.
- **Domain randomization timing conversion (Eq. 1):**  
  `time_s = num_steps * (decimation * dt)`  
  where `dt` = sim timestep (s), `decimation` = controlFrequencyInv renamed, `num_steps` = steps between randomizations.
- **Empirical/default config numbers (from config table/snippet):**  
  Example sim `dt = 1/120 ≈ 0.0083 s`; `decimation = 2` (→ 60 Hz control). Gravity `[0,0,-9.81]`. Solver iterations: position `4`, velocity `0`. Contact: `contact_offset=0.02`, `rest_offset=0.001`, `bounce_threshold_velocity=0.2`. `max_depenetration_velocity=100.0`. GPU buffers: `gpu_max_rigid_contact_count=524288`, `gpu_max_rigid_patch_count=81920`, `gpu_heap_capacity=67108864`, `gpu_temp_buffer_capacity=16777216`, `gpu_max_num_partitions=8`.
- **Workflow rationale (Isaac Lab vs OmniIsaacGymEnvs):** resets can occur based on *current-step* state (restriction removed); canonical loop: apply actions → step sim → collect states → compute dones/rewards → reset → compute observations (no required `post_physics_step`).

## When to surface
Use when students ask for exact Isaac Sim/Isaac Lab API method names (callbacks, articulation actions, scene setup) or need concrete sim/DR timing (`dt`, `decimation`, Eq. 1) and common PhysX parameter defaults.