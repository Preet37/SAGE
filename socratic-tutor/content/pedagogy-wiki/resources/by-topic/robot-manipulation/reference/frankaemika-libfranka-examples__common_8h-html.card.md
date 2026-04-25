# Card: libfranka `setDefaultBehavior()` + collision behavior pattern
**Source:** https://frankaemika.github.io/libfranka/examples__common_8h.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official example pattern: call `setDefaultBehavior(robot)` early; then optionally override `Robot::setCollisionBehavior(...)` thresholds before realtime control.

## Key Content
- **Canonical startup workflow (official examples):**
  1. Construct `franka::Robot robot(<hostname/ip>)`.
  2. Call `setDefaultBehavior(robot);` (helper used across examples to apply a safe baseline configuration before motion/control).
  3. Move to a known joint configuration (example uses `q_goal = {0, -π/4, 0, -3π/4, 0, π/2, π/4}` with `MotionGenerator(0.5, q_goal)`).
  4. Optionally **override collision thresholds** via `robot.setCollisionBehavior(...)`.
  5. Start realtime control (e.g., `robot.startTorqueControl()` or `robot.control(...)`) and loop at ~1 kHz.

- **Collision behavior thresholds (example numbers):** `robot.setCollisionBehavior(...)` is called with **8 arrays** (torque/force, lower/upper, accel/decel vs constant-velocity phases). Example values:
  - Joint torque thresholds (7-DoF), repeated across phases/bounds:  
    `{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}`
  - Cartesian force thresholds (6 axes), repeated across phases/bounds:  
    `{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}`

- **Realtime loop detail:** callback/`readOnce()` period is **0 on first cycle**; examples send a safe initial command (e.g., zero torques) when `time == 0`.

## When to surface
Use when students ask “What does `setDefaultBehavior()` do / why call it first?”, “How do official libfranka examples set collision thresholds?”, or when debugging unsafe/too-sensitive collision behavior in Franka control bring-up.