# Card: libfranka `franka::Robot` control loops (1 kHz callbacks)
**Source:** https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Robot API surface for real-time control loops: `Robot::control` callback structure, motion generators, torque commands, and command/feedback interfaces.

## Key Content
- **Connection & setup**
  - `Robot(franka_address, realtime_config=RealtimeConfig::kEnforce, log_size=50)` establishes network connection.
  - `realtime_config=kEnforce`: throws if realtime priority cannot be set; `Ignore` disables this behavior.
  - `log_size`: number of last states kept for logging; provided when `ControlException` is thrown.
  - `serverVersion() -> uint16_t` returns robot server software version.
  - `loadModel()` loads model library from robot.

- **State reading**
  - `read(read_callback: bool(const RobotState&))`: loop reading robot state; **cannot run while a control/motion loop is running**.
  - `readOnce() -> RobotState`: blocks until next state update.

- **Real-time control loop (core procedure)**
  - `control(...)` runs at **1 kHz**; callback must compute quickly to be accepted.
  - Callback signature: `(const RobotState& robot_state, franka::Duration time_step) -> CommandType`.
  - **Time update pattern:** `time += time_step.toSec();` at start of callback.
  - **Stopping a motion:** return `franka::MotionFinished(command)` (e.g., `MotionFinished(Torques)`).
  - **Important detail:** `time_step` is **0 on the first invocation**.
  - **Mutual exclusion:** only **one** `control`/motion-generator loop active at a time; otherwise `ControlException` / `InvalidOperationException`.

- **Control overloads & defaults**
  - Torque-only: `control(Torques cb, limit_rate=true, cutoff_frequency=kDefaultCutoffFrequency)`.
  - Torque + motion generator: joint positions/velocities or Cartesian pose/velocities.
  - Motion-generator-only: `control(JointPositions|JointVelocities|CartesianPose|CartesianVelocities cb, controller_mode=ControllerMode::kJointImpedance, limit_rate=true, cutoff_frequency=...)`.
  - `limit_rate=true` by default; note: “could distort your motion!”
  - `cutoff_frequency`: 1st-order low-pass on commanded signal; set to `franka::kMaxCutoffFrequency` to disable.

- **Non-real-time commands (don’t call inside loops)**
  - `setCollisionBehavior(...)`: thresholds; between lower/upper => “contact” in `RobotState`; above upper => “collision” and robot stops.
  - `setJointImpedance(K_theta[7])`, `setCartesianImpedance(K_x[6])`, `setGuidingMode(bool[6], elbow)`, `setK(EE_T_K[16])`, `setEE(NE_T_EE[16])`, `setLoad(mass, F_x_Cload[3], inertia[9])`, `setFilters(...)` (**1–1000 Hz**, 1000 Hz = no filtering), `automaticErrorRecovery()`, `stop()` (preempts other thread’s loop with `ControlException`).

## When to surface
Use when students ask how to implement a Franka real-time torque/impedance controller, how `Robot::control` callbacks are structured/terminated, what defaults (1 kHz, `limit_rate`, filters) apply, or which commands must not be called inside control loops.