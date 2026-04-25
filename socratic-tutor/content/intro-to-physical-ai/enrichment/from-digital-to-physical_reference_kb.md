## Core Definitions

**Physical AI**  
Physical AI systems are AI systems that must *perceive, reason about, and act in the real world* through a continuous perception→action loop, where uncertainty, safety, and real-time constraints dominate system design. This framing is supported by robotics “full stack” treatments that emphasize tight coupling between perception, planning, and control for real tasks (e.g., Tedrake’s manipulation notes emphasize that manipulation requires “significant interactions between perception, planning, and control” and that seemingly mundane tasks remain hard because of these coupled constraints) (https://manipulation.csail.mit.edu/intro.html).

**Embodied intelligence**  
Embodied intelligence is the view that intelligent behavior emerges from the interaction of an agent’s *body*, *sensors*, *actuators*, and *environment*, not just from abstract computation. In manipulation, Tedrake highlights that humans exploit contact and environment-assisted strategies (e.g., intentionally contacting a dishwasher slat to “let the plate rotate itself into position”), illustrating that embodiment can reduce the need for precise geometric planning (https://manipulation.csail.mit.edu/intro.html).

**Perception–action loop**  
A perception–action loop is the recurring cycle where an agent (1) senses the world, (2) updates an internal belief/state estimate, (3) selects an action, and (4) executes it, changing the world and future observations. In probabilistic robotics, this is formalized by the Bayes filter recursion over beliefs \(bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})\), where actions \(u_t\) and observations \(z_t\) jointly determine the state estimate used for decision-making (https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf).

**Real-time control**  
Real-time control is control computation performed under strict timing constraints where missing deadlines can degrade performance or cause unsafe behavior. A concrete example is libfranka’s `franka::Robot::control(...)` loop, which runs at **1 kHz** and requires the callback to compute quickly; the callback receives the latest `RobotState` and a `time_step` (notably **0 on the first invocation**) and must return a command each cycle (https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html).

**Sensor fusion**  
Sensor fusion is the process of combining multiple sensor measurements (often with a motion/process model) to estimate latent state more accurately/robustly than any single sensor. The “sensor-fusion” repository implements Kalman Filter (KF), Extended KF (EKF), and Unscented KF (UKF) with CV/CTRV process models and LiDAR/Radar measurement models, explicitly motivated by embedded constraints (templates, avoiding dynamic allocations) important for onboard real-time systems (https://github.com/TheGreatGalaxy/sensor-fusion).

**Autonomous systems**  
Autonomous systems are systems that sense, decide, and act without continuous human control, typically requiring (i) state estimation under uncertainty, (ii) planning/decision logic, (iii) closed-loop control, and (iv) safety arguments and monitoring. Waymo’s safety-case framing defines a safety case as a “structured argument, supported by a body of evidence… that a system is safe for a given application in a given environment,” with a top-level goal of **Absence of Unreasonable Risk (AUR)** (https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf).

---

## Key Formulas & Empirical Results

### Bayes filter (belief-state estimation backbone)
From *Probabilistic Robotics*:
- **Belief (posterior):**  
  \[
  bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})
  \]
- **Prediction belief:**  
  \[
  \overline{bel}(x_t)=p(x_t\mid z_{1:t-1},u_{1:t})
  \]
- **Markov assumptions enabling recursion:**  
  \[
  p(x_t\mid x_{0:t-1},z_{1:t-1},u_{1:t})=p(x_t\mid x_{t-1},u_t)
  \]
  \[
  p(z_t\mid x_{0:t},z_{1:t-1},u_{1:t})=p(z_t\mid x_t)
  \]
**Variables:** \(x_t\)=state, \(z_t\)=measurement, \(u_t\)=control/action.  
**Supports claim:** physical AI must maintain state under uncertainty; perception and action are coupled through belief updates.  
Source: https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf

### Real-time control loop constraint (Franka)
- libfranka `Robot::control(...)` runs at **1 kHz**; callback signature returns a command based on `(RobotState, Duration time_step)`; **`time_step` is 0 on first invocation**; stop by returning `franka::MotionFinished(command)`.  
**Supports claim:** physical AI must meet hard timing constraints in the perception–action loop.  
Source: https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html

### ROS 2 QoS: message delivery can fail due to incompatibility
- QoS is a set of policies; **incompatible QoS can prevent any message delivery**.  
- Default pub/sub profile: Keep last, **Depth=10**, Reliable, Volatile.  
- Sensor data profile rationale: prioritize timeliness → **Best effort** + smaller queue.  
**Supports claim:** real-time perception pipelines are constrained by communication semantics; “digital AI” assumptions (perfect message passing) don’t hold.  
Source: https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html

### Sensing modality robustness on ill-reflective surfaces (LiDAR vs RADAR vs Depth)
From https://arxiv.org/html/2309.10504:
- **Depth from disparity (stereo):**  
  \[
  Z=\frac{f\,b}{d}
  \]
- **RADAR range resolution:**  
  \[
  \Delta R=\frac{c}{2B}
  \]
- **Static ranging (selected results):**
  - Baseline (white): LiDAR max **10 m**, MAE **<5 cm up to 8.5 m**; RADAR max **7 m**, MAE ~**10–15 cm**; depth camera max **6 m**, MAE **61 cm at 6 m**.
  - Ill-reflective (black): LiDAR max **3 m** (33% of baseline); RADAR max **7.5 m**, MAE **<10 cm** for **≥2.5 m** (but more false positives at short range); depth camera keeps **6 m** max range.
**Supports claim:** physical AI perception is brittle to environment physics; fusion is often required.

### Tokenized robot actions + real-time rates (RT-2)
From https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf:
- Action space: 6-DoF end-effector \(\Delta\)pos + \(\Delta\)rot + gripper + terminate.
- **Discretization:** each continuous dim → **256 uniform bins**, represented as **8 integer tokens**.
- **Real-time serving:** RT-2-PaLI-X **55B ~1–3 Hz**, **5B ~5 Hz** (cloud TPU).
**Supports claim:** even “foundation-model” robot policies face tight control-rate constraints and must quantize/structure actions for execution.

### Diffusion Policy: real-time inference trick + benchmark gains
From https://roboticsproceedings.org/rss19/p026.pdf and https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf:
- **DDPM denoising update (sampling):**  
  \[
  x_{k-1}=\alpha\big(x_k-\gamma\,\epsilon_\theta(x_k,k)+\mathcal{N}(0,\sigma^2 I)\big)
  \]
- **Training objective (noise prediction):**  
  \[
  L=\mathrm{MSE}(\epsilon_k,\epsilon_\theta(x_0+\epsilon_k,k))
  \]
- **Speed:** DDIM example: **100 training steps, 10 inference steps → ~0.1s latency on RTX 3080**.
- **Headline performance:** average **+46.9%** success improvement across **15 tasks / 4 benchmarks** (IJRR/paper summary).
**Supports claim:** physical AI policies must be designed for closed-loop replanning and latency constraints.

### Safety case & risk framing (Waymo)
From https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf:
- **Risk framing:** **Risk = P(harm) × Severity(harm)** (ISO 26262 framing cited in doc).
- Safety case definition (UL 4600:2022): “Structured argument, supported by a body of evidence…”
**Supports claim:** physical AI must be justified with structured safety arguments, not just accuracy metrics.

---

## How It Works

### A. The physical perception→action loop (belief + control)
Use this when a student asks “what’s the actual loop?”
1. **Sense:** acquire measurements \(z_t\) (camera, LiDAR, RADAR, encoders, F/T, etc.).  
2. **Predict (using action/control):** propagate belief using the transition model and the executed control \(u_t\): compute \(\overline{bel}(x_t)\). (Bayes filter prediction)  
3. **Update (using measurement):** incorporate \(z_t\) via the measurement model to get \(bel(x_t)\). (Bayes rule update)  
4. **Decide/plan:** choose next action \(u_{t+1}\) based on current belief and task objective (can be classical planning, learned policy, hybrid automaton, etc.).  
5. **Act (real-time control):** send commands at the required rate (e.g., 1 kHz torque loop on Franka).  
6. **Safety checks:** monitor contacts/collisions, stale data, QoS events, and stop/recover if needed (e.g., collision thresholds in libfranka; QoS incompatibility in ROS 2 can silently break perception).  
Sources: Bayes filter (https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf), Franka control loop (https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html), ROS 2 QoS (https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

### B. Real-time Franka control callback mechanics (1 kHz)
Use when debugging “why does my controller behave weirdly at start / why did it stop?”
1. Create `franka::Robot robot(address, RealtimeConfig::kEnforce, ...)`.  
2. (Common pattern) call `setDefaultBehavior(robot)` early (official examples).  
3. Start `robot.control(callback, ...)`.  
4. **Each 1 kHz cycle:** callback receives `(RobotState, time_step)`; update your internal time with `time += time_step.toSec();`.  
5. **First cycle gotcha:** `time_step` is **0** on first invocation; many examples send safe initial commands (e.g., zero torques) when `time==0`.  
6. To stop gracefully, return `franka::MotionFinished(command)`.  
Sources: https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html and https://frankaemika.github.io/libfranka/examples__common_8h.html

### C. ROS 2 QoS “why aren’t my messages arriving?” checklist
Use when a student has a perception pipeline but no data arrives.
1. Identify publisher QoS “offered” and subscriber QoS “requested”.  
2. Check **Reliability** compatibility: publisher BestEffort cannot satisfy subscriber Reliable (explicitly incompatible).  
3. Check **Durability**: “latched” behavior requires both sides **Transient local**; Volatile→Transient local is incompatible.  
4. Check **History/Depth**: Depth only matters if History=Keep last.  
5. Check **Deadline/Liveliness**: Default→specified can be incompatible per ROS 2 rules.  
Source: https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html

### D. Sensor fusion (KF/EKF/UKF) as a real-time embedded design choice
Use when a student asks “why not just use a big neural net?”
1. Choose a **process model** (e.g., CV: constant velocity; CTRV: constant turn rate and velocity).  
2. Choose **measurement models** (LiDAR, RADAR).  
3. Run predict/update each measurement arrival; keep state vector (e.g., CV in 2D uses \([p_x,p_y,v_x,v_y]\) per repo description).  
4. Implementation detail for physical systems: avoid dynamic allocations; use templates; rely on Eigen for matrix ops—explicitly motivated as “crucial for embedded systems” in the repo.  
Source: https://github.com/TheGreatGalaxy/sensor-fusion

---

## Teaching Approaches

### Intuitive (no math): “Why physical is harder than digital”
- Digital AI can often assume: inputs are clean, time is flexible, and mistakes are reversible (retry a query, rerun a job).  
- Physical AI must assume: sensors fail in *structured* ways (e.g., LiDAR range collapses on black surfaces), actions have irreversible consequences (collisions), and computation must meet deadlines (1 kHz control, timely sensor streams).  
Anchor examples: LiDAR vs RADAR robustness (https://arxiv.org/html/2309.10504), Franka 1 kHz loop (https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html), ROS 2 QoS incompatibility (https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

### Technical (with math): “Belief + control under uncertainty”
- The core technical object is the belief \(bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})\).  
- Actions \(u_t\) affect both the world and the next belief via the transition model; measurements \(z_t\) update belief via the sensor model.  
- Real-time control constrains how quickly you can update belief and compute actions (e.g., 1 kHz callback).  
Source: Bayes filter equations (https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf) + Franka timing (https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)

### Analogy-based: “Robots are like a tight band, not a soloist”
- Perception, planning, control, comms, and safety are “instruments” that must stay in sync.  
- ROS 2 QoS is like the audio system: if settings mismatch, you might hear nothing (no messages delivered).  
- Sensors are like microphones with different failure modes; you blend them (fusion) so one mic dropping doesn’t end the performance.  
Sources: ROS 2 QoS incompatibility (https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html), modality failures (https://arxiv.org/html/2309.10504), fusion repo (https://github.com/TheGreatGalaxy/sensor-fusion)

---

## Common Misconceptions

1. **“If my perception model is accurate offline, it will work on the robot.”**  
   **Why wrong:** real sensors fail non-uniformly with environment physics; e.g., LiDAR max range drops from **10 m** (white) to **3 m** (black) in the cited study, changing downstream behavior. Offline datasets often underrepresent these conditions.  
   **Correct model:** perception must be designed for *robustness under modality-specific failure modes*; fusion and fallback behaviors matter.  
   Source: https://arxiv.org/html/2309.10504

2. **“Control is just sending actions; timing doesn’t matter much.”**  
   **Why wrong:** real controllers run at fixed rates; libfranka’s control loop is **1 kHz**, and callbacks must compute quickly. Missing deadlines can cause rejection/instability; also the first `time_step` is **0**, which can break naive integrators.  
   **Correct model:** control is a *real-time contract* (rate + latency + safe startup/stop semantics).  
   Source: https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html

3. **“ROS topics are like function calls—if I publish, subscribers will receive.”**  
   **Why wrong:** ROS 2 QoS incompatibility can prevent *any* message delivery; e.g., a subscriber requesting Reliable cannot match a BestEffort publisher.  
   **Correct model:** communication is governed by negotiated QoS policies; you must design QoS for timeliness vs completeness (sensor streams often BestEffort).  
   Source: https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html

4. **“A big end-to-end model removes the need for classical robotics structure.”**  
   **Why wrong:** even learned robot policies must respect action representations and control rates; RT-2 discretizes actions into **256 bins** per dimension (tokenized actions) and runs at only **~1–3 Hz** (55B) or **~5 Hz** (5B), implying additional low-level control structure is still needed.  
   **Correct model:** learned high-level policies often sit inside a larger stack with real-time control, safety limits, and state estimation.  
   Source: https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf

5. **“Safety is just ‘low crash rate’ or ‘high accuracy’.”**  
   **Why wrong:** safety cases require structured arguments and evidence; Waymo frames safety as **Absence of Unreasonable Risk (AUR)** and uses risk framing **Risk = P(harm) × Severity(harm)** plus acceptance criteria and validation targets.  
   **Correct model:** safety is an explicit *argument + evidence* process, not a single metric.  
   Source: https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf

---

## Worked Examples

### Example 1: Debugging a “silent” perception pipeline in ROS 2 (QoS mismatch)
**Scenario:** Student subscribes to `/camera/image` but callback never fires.

**Tutor script (steps to run mentally / in code review):**
1. Ask: “What QoS did you set on the subscriber? Did you use `SensorDataQoS()` or default?”  
2. Check likely mismatch: camera drivers often publish with **Best effort** (sensor data profile rationale), while student may have default **Reliable** subscription.  
3. Apply compatibility rule: **Publisher BestEffort → Subscriber Reliable = incompatible (No delivery)**.  
4. Fix: set subscriber QoS to BestEffort / sensor data profile (timeliness-first).  
**Grounding:** ROS 2 QoS compatibility table and sensor-data rationale.  
Source: https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html

### Example 2: Safe startup pattern for a 1 kHz Franka torque controller
**Scenario:** Student’s controller “spikes” on first cycle.

**Key facts to use:**
- `Robot::control` callback runs at **1 kHz**.  
- `time_step` is **0 on the first invocation**.  
- Official examples call `setDefaultBehavior(robot)` early and often send safe initial commands at `time==0`.  
Sources: https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html, https://frankaemika.github.io/libfranka/examples__common_8h.html

**Minimal pseudocode pattern (for tutor to reference):**
```cpp
double time = 0.0;

robot.control([&](const franka::RobotState& state, franka::Duration dt) {
  time += dt.toSec();

  if (dt.toSec() == 0.0) {
    // First cycle: avoid derivative/integrator blow-ups.
    return franka::Torques{{0,0,0,0,0,0,0}};
  }

  // ... compute torques quickly (1 kHz budget) ...
  franka::Torques tau = /* ... */;

  // Stop condition:
  // if (done) return franka::MotionFinished(tau);

  return tau;
});
```

### Example 3: Choosing sensors for dark/ill-reflective targets (fusion motivation)
**Scenario:** Student asks why their LiDAR-based tracker fails on black objects.

**Use the paper’s concrete numbers:**
- LiDAR max range drops from **10 m** (white) to **3 m** (black).  
- RADAR maintains ~**7–7.5 m** max range and can achieve **<10 cm** MAE beyond **2.5 m** (with caveats at short range).  
- Depth camera keeps **6 m** max range; depth error grows with distance (e.g., MAE **61 cm at 6 m** baseline).  
**Tutor move:** ask which failure mode they see (no returns vs noisy short-range false positives) and propose fusion/fallback logic.  
Source: https://arxiv.org/html/2309.10504

---

## Comparisons & Trade-offs

| Topic | Option A | Option B | Trade-off / When to choose |
|---|---|---|---|
| ROS 2 Reliability | Best effort | Reliable | Best effort may drop messages but is timely (recommended for sensor data); Reliable retries for completeness but can add latency/backpressure; incompatibility can block delivery entirely (ROS 2 QoS doc). |
| ROS 2 Durability | Volatile | Transient local | Transient local supports late-joiners (latched-like) but requires compatibility; Volatile avoids delivering outdated data (services profile rationale). |
| Sensing modality (ill-reflective surfaces) | LiDAR | RADAR / Depth camera | LiDAR can fail badly on black/ill-reflective surfaces (range collapse); RADAR more robust in that condition but can have false positives at short range; depth camera has different error scaling with distance (2309.10504). |
| Robot policy action representation | Continuous actions | Tokenized/discretized actions | RT-2 discretizes each action dim into **256 bins** and outputs tokens; simplifies interfacing with VLMs but introduces quantization and still faces low control rates (RT-2 paper). |
| Visuomotor policy generation | Direct regression (BC) | Diffusion over action sequences | Diffusion Policy uses iterative denoising; can model multimodality and uses receding-horizon replanning; needs inference acceleration (DDIM ~0.1s example) (Diffusion Policy papers). |

---

## Prerequisite Connections

- **Probability & conditional independence:** needed to understand Bayes filter assumptions (Markov transition and measurement independence) (https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf).  
- **Feedback control basics (sampling rate, stability intuition):** needed to appreciate why 1 kHz loops and startup transients matter (https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html).  
- **Systems/communication semantics:** needed to reason about ROS 2 QoS incompatibility and timeliness vs reliability trade-offs (https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html).  
- **Sensing physics intuition:** needed to interpret modality failure modes (reflectivity, disparity depth, radar resolution) (https://arxiv.org/html/2309.10504).

---

## Socratic Question Bank

1. **If your robot’s camera messages stop arriving after you “improve reliability,” what’s a concrete mechanism that could cause *zero* delivery?**  
   *Good answer:* QoS incompatibility (e.g., subscriber requests Reliable but publisher offers BestEffort) can prevent matching in ROS 2.

2. **Why does a Bayes filter include actions \(u_t\) in the belief \(p(x_t\mid z_{1:t},u_{1:t})\)? What breaks if you ignore them?**  
   *Good answer:* actions affect state evolution; ignoring them makes prediction wrong and forces the measurement update to “explain away” motion.

3. **In a 1 kHz torque loop, what’s the practical consequence of `time_step` being 0 on the first callback?**  
   *Good answer:* derivative/integrator terms can blow up or be undefined; need safe initialization.

4. **Given a black, low-reflectivity target, which sensor (LiDAR/RADAR/depth camera) is most likely to lose range first, and what number supports that?**  
   *Good answer:* LiDAR; max range drops to ~3 m vs 10 m baseline in the cited study.

5. **RT-2 runs at ~1–3 Hz (55B). What does that imply about the rest of the robot stack if you need smooth motion?**  
   *Good answer:* you need lower-level controllers running faster (e.g., impedance/torque control) and likely a hierarchy where RT-2 provides higher-level commands.

6. **Why might “Reliable” QoS be a bad default for high-rate sensors even if you “want all the data”?**  
   *Good answer:* timeliness matters; retries/backpressure can increase latency; sensor data profile prioritizes best-effort and small queues.

7. **What’s the difference between arguing “my system is safe” and presenting a safety case?**  
   *Good answer:* safety case is a structured argument with evidence for a specific ODD/application; Waymo frames it as AUR with acceptance criteria and targets.

8. **If LiDAR fails on a surface but RADAR has short-range false positives, what fusion behavior would you design?**  
   *Good answer:* modality-aware gating/weighting: rely on LiDAR when returns are valid; fall back to RADAR/depth when LiDAR unavailable; handle RADAR short-range with filtering/association logic.

---

## Likely Student Questions

**Q: “What exactly is the Bayes filter belief state?”**  
→ **A:** \(bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})\), the posterior over state given all measurements up to \(t\) and all controls up to \(t\). (https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf)

**Q: “Why can ROS 2 topics fail to deliver messages even though both nodes are running?”**  
→ **A:** ROS 2 uses QoS policy negotiation; **incompatible QoS can prevent any message delivery** (e.g., subscriber requests Reliable but publisher offers BestEffort is incompatible). (https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

**Q: “What’s the default ROS 2 pub/sub QoS?”**  
→ **A:** History=Keep last, **Depth=10**, Reliability=Reliable, Durability=Volatile (ROS 1–like defaults). (https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html)

**Q: “What rate does libfranka control run at, and what’s the first-cycle gotcha?”**  
→ **A:** `Robot::control(...)` runs at **1 kHz**; the callback’s `time_step` is **0 on the first invocation**. (https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)

**Q: “Do we have evidence that LiDAR is worse on black/ill-reflective surfaces?”**  
→ **A:** Yes—on black surfaces, LiDAR max range dropped to **3 m** vs **10 m** baseline (white), while RADAR maintained ~**7.5 m** max range in the cited experiments. (https://arxiv.org/html/2309.10504)

**Q: “How does RT-2 represent robot actions?”**  
→ **A:** It outputs actions as text tokens: 6-DoF end-effector \(\Delta\)pos/\(\Delta\)rot + gripper + terminate; each continuous dimension is discretized into **256 bins**, yielding **8 integer tokens** per action. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**Q: “What’s the Diffusion Policy training loss in one line?”**  
→ **A:** Noise-prediction MSE: \(L=\mathrm{MSE}(\epsilon_k,\epsilon_\theta(x_0+\epsilon_k,k))\) (and conditional variants for visuomotor control). (https://roboticsproceedings.org/rss19/p026.pdf; https://diffusion-policy.cs.columbia.edu/diffusion_policy_ijrr.pdf)

**Q: “What does a safety case mean in autonomous driving?”**  
→ **A:** Per UL 4600 (as quoted by Waymo), it’s a “structured argument, supported by a body of evidence… that a system is safe for a given application in a given environment,” with a top-level goal of **Absence of Unreasonable Risk (AUR)**. (https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf)

---

## Available Resources

### Videos
- [Deep Learning for Robot Manipulation (CS287 Advanced Robotics lecture)](https://youtube.com/watch?v=KhgCnMFhNd8) — Surface when: student asks for a rigorous lecture-style overview of modern robot manipulation learning and how it interfaces with control/perception.

### Articles & Tutorials
- [MIT OCW: Underactuated Robotics Lecture Series (Perception & Control)](https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/) — Surface when: student needs a rigorous control/perception foundation behind “perception–action loops” and real-time control.
- [Lilian Weng — “Autonomous Agents”](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student is mapping LLM-agent concepts (planning/memory/tool use) onto embodied/robot agents.
- [MIT Manipulation Notes (Tedrake)](https://manipulation.csail.mit.edu/) — Surface when: student asks why manipulation is hard and how perception/planning/control interact in real tasks.
- [MIT Manipulation: Clutter / Bin Picking chapter](https://manipulation.csail.mit.edu/clutter.html) — Surface when: student asks about simulation realism, object initialization without penetration, and why “looks good” physics can still be wrong up close.

---

## Visual Aids

![LLM-powered autonomous agent system overview. (Weng, 2023)](/api/wiki-images/physical-ai-foundations/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: student is confused about how “agent architecture” components (planning/memory/tool use) relate to embodied agents and the perception–action loop.

![ReAct reasoning trajectories across knowledge and decision tasks. (Yao et al., 2023)](/api/wiki-images/physical-ai-foundations/images/lilianweng-posts-2023-06-23-agent_002.png)  
Show when: student asks why explicit reasoning steps matter in an action–observation loop (useful bridge from digital agents to physical loops).

![Human memory taxonomy mapped to LLM agent memory components. (Weng, 2023)](/api/wiki-images/physical-ai-foundations/images/lilianweng-posts-2023-06-23-agent_008.png)  
Show when: student asks what “memory” means operationally for an agent that must act over time (connect to state/belief in robotics).

---

## Key Sources

- [Probabilistic Robotics (Bayes filter foundations)](https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf) — Primary source for belief-state definitions and Markov assumptions underlying perception under uncertainty.
- [ROS 2 QoS Policies + Standard Profiles (Iron)](https://docs.ros.org/en/iron/Concepts/Intermediate/About-Quality-of-Service-Settings.html) — Authoritative reference for real robot comms semantics; explains why data can silently not flow.
- [libfranka `franka::Robot` control loops (1 kHz callbacks)](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html) — Concrete API/timing constraints illustrating real-time control requirements.
- [Robustness of LiDAR vs RADAR vs Depth Camera on ill-reflective surfaces](https://arxiv.org/html/2309.10504) — Empirical modality failure data supporting “physical perception is brittle; fusion matters.”
- [Waymo Safety Case Approach (AUR)](https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf) — Concrete safety-case structure and risk framing for deployed autonomous physical systems.