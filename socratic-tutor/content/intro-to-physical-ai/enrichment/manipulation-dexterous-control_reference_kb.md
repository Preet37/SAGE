## Core Definitions

**Grasp planning** — The process of choosing *how* a robot will make and maintain contact with an object (e.g., where to place fingers/cup, approach direction, and any regrasp sequence) so that the object can be lifted/manipulated while respecting kinematic limits and contact constraints. In deployed shelf/bin systems, grasp planning is often implemented as selecting among robust motion primitives (e.g., suction, scoop, topple) using sensor feedback rather than solving a single global plan (as described in the MIT APC system architecture and primitives) [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf), and similarly in the APC-winning system’s feedback-heavy primitives and error-handling automaton [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf).

**Dexterous manipulation** — Manipulation that exploits many degrees of freedom (DoF) and rich contact interactions to control an object’s pose/trajectory, often including multi-finger coordination, finger gaiting, and controlled use of gravity. OpenAI et al. describe learning “dexterous in-hand manipulation policies” that achieve object reorientation with emergent behaviors like finger gaiting and multi-finger coordination, trained in simulation and transferred to a physical Shadow Dexterous Hand via extensive randomization [https://arxiv.org/abs/1808.00177](https://arxiv.org/abs/1808.00177).

**Tactile sensing** — Sensing through physical contact that provides information about contact location/geometry/pressure/shear, enabling feedback in contact-rich tasks. In deployed manipulation systems, contact feedback is often mediated through wrist force/torque sensors and pressure sensors (e.g., suction seal detection) rather than vision alone (APC systems use wrist F/T and suction pressure feedback for robust execution) [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf), [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf). (Note: the provided sources mention tactile-like feedback via F/T and pressure; they do not provide a formal definition of GelSight beyond naming it as a key concept in this lesson.)

**In-hand manipulation** — Changing an object’s pose *within the grasp* (e.g., reorienting/rotating without setting it down), typically by coordinating multiple contacts and allowing controlled slip/roll. OpenAI et al. specifically frame their result as “in-hand manipulation” for object reorientation learned with RL in simulation and transferred to hardware [https://arxiv.org/abs/1808.00177](https://arxiv.org/abs/1808.00177).

**Degrees of freedom (DoF)** — The number of independent coordinates needed to specify a system’s configuration or motion. In manipulation contexts, DoF appears at multiple levels: robot arm joints (e.g., 7-DoF arms in APC systems), mobile base DoF (holonomic base adds planar DoF), and end-effector/object pose DoF (6-DoF pose). The APC-winning system highlights a 7-DoF arm on a holonomic base yielding “10 holonomic DOF total,” used to simplify reaching and reduce reliance on high-DoF motion planning [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf).

**Contact-rich manipulation** — Manipulation where task success depends on modeling/handling intermittent contacts, friction, stick–slip transitions, and unilateral constraints (non-penetration). The Unicomp paper formalizes contact-rich interaction by integrating rigid-body dynamics with complementarity constraints for normal contact and frictional constraints (LCP/MCP/NCP-style formulations) [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1).

**GelSight** — A tactile sensing modality named in the lesson’s key concepts; however, no provided source excerpt defines GelSight explicitly. (Tutor move: if a student asks, acknowledge the gap and pivot to the tactile sensing mechanisms explicitly documented here—wrist F/T and suction pressure feedback in APC systems—unless additional GelSight-specific material is introduced.)

---

## Key Formulas & Empirical Results

### Complementarity contact modeling (Unicomp)

**Linear Complementarity Problem (LCP) special case** (Unicomp Sec. 2.1): find \(x \ge 0\) such that  
\[
Mx + q \ge 0,\quad x^\top(Mx+q)=0
\]  
Supports: expressing unilateral contact constraints and mode switching (contact/no-contact) without explicit enumeration.  
Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

**Unilateral normal contact complementarity** (Unicomp Sec. 2.2):  
\[
0\le \lambda_n \perp \phi(q)\ge 0
\]  
- \(\lambda_n\): normal force magnitude (or impulse in discrete time)  
- \(\phi(q)\): signed normal gap at the contact point (ECP)  
Supports: non-penetration + non-adhesive contact (no tensile normal force).  
Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

**Discrete-time non-penetration complementarity** (Unicomp Eq. 25):  
\[
0\le p_n \perp (\phi^k + h\,v_n^{k+1} + \epsilon)\ge 0
\]  
- \(p_n\): normal impulse  
- \(h\): time step  
- \(v_n^{k+1}\): next-step normal relative velocity  
- \(\epsilon\): regulation term  
Supports: time-stepping simulation/control for contact-rich manipulation.  
Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

**Friction via ellipsoidal limit surface constraint** (Unicomp Eq. 7):  
\[
\left(\frac{\lambda_{t1}}{\mu \lambda_n}\right)^2+\left(\frac{\lambda_{t2}}{\mu \lambda_n}\right)^2+\left(\frac{\lambda_o}{\mu \lambda_n e_o}\right)^2 \le 1
\]  
- \(\lambda_{t1},\lambda_{t2}\): tangential friction forces  
- \(\lambda_o\): torsional friction moment  
- \(\mu\): friction coefficient  
- \(e_o\): torsional scaling parameter  
Supports: stick–slip transitions via optimization/complementarity rather than hand-coded modes.  
Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

**Implementation default (example)**: planar pushing experiments at fixed step \(h=0.001\) s (1000 Hz) on a single CPU core (Unicomp Sec. 5.2).  
Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

---

### Rigid-body manipulator dynamics (spatial vector algorithms)

**Canonical joint-space equation of motion** (Featherstone-style explainer Eq. 1.1):  
\[
\tau = H(q)\,\ddot q + C(q,\dot q)
\]  
- \(H(q)\): joint-space inertia matrix  
- \(C(q,\dot q)\): bias terms (Coriolis/centrifugal + gravity + other non-actuation forces)  
Supports: connecting control torques to accelerations; baseline for contact-aware control.  
Source: [https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf](https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf)

---

### Empirical deployment metrics (APC systems)

**APC-winning system performance**: 148/190 (77.8%) in competition; 10/12 targets; average pick 87 s (competition) [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf).  
Supports: real-world reliability constraints and failure modes in contact-rich picking.

**MIT APC 2015 system outcome**: picked 7/12 items; scored 88 points; stopped after ~7 min due to torque overload [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf).  
Supports: integration realities (sensing interference, error recovery, torque limits).

---

### Real-time control loop constraints (Franka libfranka)

**Control callback rate**: `Robot::control(...)` runs at 1 kHz; `time_step` is 0 on first invocation; stop by returning `franka::MotionFinished(command)` [https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html).  
Supports: why dexterous/contact control is typically implemented as fast feedback loops.

---

## How It Works

### A. Contact-rich manipulation as complementarity-constrained dynamics (Unicomp-style)

1. **Define rigid-body state and dynamics** (Newton–Euler / generalized coordinates).  
   - You have configuration \(q\), velocity \(V\) (or \(\dot q\)), mass/inertia \(M\).

2. **Introduce unilateral contact variables** at an equivalent contact point (ECP):  
   - Normal direction \(n\), tangential directions \(t_1,t_2\).  
   - Unknown normal magnitude \(\lambda_n\) (or impulse \(p_n\) in discrete time).  
   - Unknown friction wrench components \(\lambda_t\) and torsional \(\lambda_o\).

3. **Enforce non-penetration via complementarity**:  
   - Continuous: \(0\le \lambda_n \perp \phi(q)\ge 0\).  
   - Discrete time-stepping: \(0\le p_n \perp (\phi^k + h v_n^{k+1} + \epsilon)\ge 0\).  
   Interpretation: either (i) gap is positive and normal force/impulse is zero, or (ii) contact force/impulse is positive and the gap constraint is tight.

4. **Model friction with a limit surface** (ellipsoidal constraint) and maximum power dissipation.  
   - This yields stick/slide behavior as part of the solve (rather than if/else mode logic).

5. **Time-step update** (impulse-based):  
   - Compute “free” velocity update, then apply contact impulse:  
     \(V^{k+1}=V^k+M^{-1}(p+p_\text{ext})\) (Unicomp Eq. 22).  
   - Update pose via SE(3) integration (Unicomp Eq. 23).

6. **Solve the resulting MCP/LCP/NCP** for contact impulses/forces consistent with dynamics + constraints.

Tutor use: when a student asks “how do simulators handle stick–slip and non-penetration without enumerating modes?”, this is the mechanical answer.

---

### B. Robust grasp planning in deployed systems: “primitives + feedback + retries” (APC examples)

1. **Perceive enough to choose a primitive**, not necessarily full 6D pose with high precision.  
   - APC-winning system: shelf tracking via ICP, per-pixel classification, segment selection, bounding box fit for approach direction [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf).  
   - MIT APC: depth-only model fitting with constraints and multiple hypotheses; run multiple times across sensors [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf).

2. **Execute a motion primitive with contact feedback**. Examples:  
   - **Suction**: descend/approach, stop on contact via force control, verify expected contact height, confirm seal via pressure sensor; retry with XY jitter up to 5 attempts (MIT APC) [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf).  
   - **Top-down / side primitives** with force-guarded motions and suction (APC-winning) [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf).

3. **Use a state machine / hybrid automaton for error handling**.  
   - APC-winning example primitive: 26 states / 50 transitions, with 34 transitions for error handling (retract/reattempt on collisions; pressure detects grasp failure) [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf).

4. **Re-perceive after deliberate environment interactions** (topple, push-rotate) to simplify the next grasp (MIT APC) [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf).

Tutor use: when a student expects “one-shot grasp planning,” surface this as the common real-world pattern.

---

### C. Learning dexterous in-hand manipulation in simulation (OpenAI Dactyl summary)

1. **Train an RL policy in simulation** for object reorientation with a multi-finger hand.  
2. **Randomize physical and visual properties** (e.g., friction coefficients, object appearance) during training to support sim-to-real transfer.  
3. **Deploy on the physical hand**; behaviors like finger gaiting and coordinated multi-finger control can emerge without demonstrations.  
Source: [https://arxiv.org/abs/1808.00177](https://arxiv.org/abs/1808.00177)

Tutor use: when a student asks “how can RL in sim transfer to real dexterous hands?”

---

## Teaching Approaches

### Intuitive (no math): “Contacts are decisions the world makes with you”
- Dexterous manipulation is hard because the world “decides back”: when you push, you might stick, slip, or lose contact.
- Good systems either (a) **model** those decisions (contact solvers / complementarity), or (b) **avoid needing precision** by using embodiment + feedback primitives (suction, force-guarded moves, retries).
- RL-in-sim can discover strategies (finger gaiting, using gravity) that humans use, if the simulator exposes enough variability (randomization).

### Technical (with math): “Unilateral constraints + friction = complementarity”
- Non-penetration is naturally expressed as \(0\le \lambda_n \perp \phi(q)\ge 0\): you can’t have both positive gap and positive normal force.
- In time-stepping, impulses \(p_n\) satisfy \(0\le p_n \perp (\phi^k + h v_n^{k+1} + \epsilon)\ge 0\).
- Friction can be handled via a limit surface (ellipsoid) constraint tied to \(\mu \lambda_n\), enabling stick/slide outcomes from the solve rather than discrete mode logic.  
Source: Unicomp [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

### Analogy-based: “Suction cups vs fingers: reduce the problem’s required accuracy”
- Suction is like using a “wide basin of attraction”: you don’t need perfect finger placement; seal feedback (pressure) tells you if it worked.
- Multi-finger in-hand manipulation is like juggling: many DoF, many contacts, and you often intentionally allow controlled slip/roll.
- Hybrid automata/state machines are like “if this fails, do the next safe thing” playbooks—crucial in real deployments.  
Sources: APC systems [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf), [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf)

---

## Common Misconceptions

1. **“If I know the object pose accurately, grasping is basically solved.”**  
   - **Why wrong:** Real deployments report failures from contact uncertainty, calibration error (e.g., open-loop FK error up to 1 cm causing misses), and clutter interactions; systems rely on force/pressure feedback and retries rather than pure open-loop execution.  
   - **Correct model:** Grasp success is often dominated by *contact execution robustness* (force-guarded motions, seal detection, error recovery), not just pose estimation.  
   - **Source:** APC-winning failure analysis [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf)

2. **“Friction is just \(\|f_t\|\le \mu f_n\); you can ignore stick–slip details.”**  
   - **Why wrong:** Stick vs slip changes the effective constraints and object motion qualitatively; Unicomp explicitly models friction via a limit surface and complementarity conditions to capture transitions without manual mode switching.  
   - **Correct model:** Frictional contact is a coupled constraint/optimization problem; stick–slip emerges from satisfying complementarity + limit-surface constraints.  
   - **Source:** Unicomp friction + complementarity [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

3. **“Contact-rich manipulation requires full motion planning; feedback controllers are a hack.”**  
   - **Why wrong:** The APC-winning system argues for “feedback over planning,” using embodiment (suction) and hybrid-automaton primitives; many transitions are dedicated to error handling.  
   - **Correct model:** For many real tasks, *structured primitives + sensing feedback* outperform heavy planning in robustness/time-to-deploy. Planning is still needed for some cases (e.g., reorientation of bulky items), but not as the default for every motion.  
   - **Source:** APC-winning lessons [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf)

4. **“In-hand manipulation is just ‘grasping harder’ so the object doesn’t move.”**  
   - **Why wrong:** In-hand manipulation *requires* controlled relative motion at contacts (slip/roll) and coordinated multi-finger actions; OpenAI reports emergent finger gaiting and controlled use of gravity.  
   - **Correct model:** You intentionally manage contact modes and redistribute forces to move the object *within* the hand.  
   - **Source:** OpenAI dexterous in-hand manipulation abstract [https://arxiv.org/abs/1808.00177](https://arxiv.org/abs/1808.00177)

5. **“A 1 kHz control loop is optional; you can do dexterous control at camera frame rate.”**  
   - **Why wrong:** Real robot APIs (e.g., Franka) structure torque/motion control as 1 kHz callbacks; contact interactions can change faster than typical vision rates.  
   - **Correct model:** High-rate low-level control (1 kHz) stabilizes contact; higher-level perception/planning can run slower.  
   - **Source:** libfranka control loop docs [https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)

---

## Worked Examples

### Example 1: Reasoning through complementarity contact outcomes (no solver required)

**Goal:** Given the complementarity condition \(0\le \lambda_n \perp \phi(q)\ge 0\), enumerate physically valid cases.

1. **Case A: No contact**
   - Suppose the gap is positive: \(\phi(q) > 0\).  
   - Complementarity requires \(\lambda_n = 0\).  
   - Interpretation: object is separated; no normal force.

2. **Case B: Contact**
   - Suppose a normal force exists: \(\lambda_n > 0\).  
   - Complementarity requires \(\phi(q) = 0\).  
   - Interpretation: bodies touch (gap closed) and push on each other.

3. **Impossible case**
   - \(\phi(q) > 0\) and \(\lambda_n > 0\) violates complementarity.  
   - Interpretation: “pushing at a distance” is not allowed.

**Tutor move:** After the student gets this, extend to discrete time: \(0\le p_n \perp (\phi^k + h v_n^{k+1} + \epsilon)\ge 0\) and ask what it implies about next-step normal velocity when contact impulse is positive.  
Source: Unicomp [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

---

### Example 2: Skeleton of a 1 kHz Franka torque control loop (structure + gotchas)

```cpp
#include <franka/robot.h>
#include <franka/exception.h>
#include <franka/duration.h>
#include <franka/torques.h>

int main() {
  franka::Robot robot("ROBOT_IP");
  double time = 0.0;

  robot.control([&](const franka::RobotState& state, franka::Duration dt) -> franka::Torques {
    // Gotcha from docs: dt is 0 on the first invocation.
    time += dt.toSec();

    // Example: send zero torques initially; real controller would compute torques here.
    franka::Torques tau{{0,0,0,0,0,0,0}};

    // Stop condition pattern from docs:
    if (time > 2.0) {
      return franka::MotionFinished(tau);
    }
    return tau;
  });

  return 0;
}
```

**What this demonstrates (from libfranka docs):**
- `Robot::control` runs at **1 kHz** and expects fast callbacks.
- `time_step` is **0 on first invocation**.
- Stop by returning `franka::MotionFinished(command)`.  
Source: [https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)

---

## Comparisons & Trade-offs

| Approach | What it buys you | What it costs | When to choose | Sources |
|---|---|---|---|---|
| **Complementarity-based contact modeling (LCP/MCP/NCP)** | Principled handling of unilateral contact + friction; stick/slide emerges from solve | Requires solving constrained problems; modeling/solver complexity | Simulation, model-based control, analysis of contact modes | Unicomp [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1) |
| **Feedback primitives + hybrid automaton** | Robustness to perception error; explicit retries/error handling; fast to deploy | Task-specific engineering; limited generality | Industrial picking, cluttered bins/shelves, when reliability matters | APC-winning [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf), MIT APC [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf) |
| **RL in simulation with randomization (sim-to-real)** | Can discover complex multi-finger strategies (finger gaiting, gravity use) without demos | Training complexity; transfer depends on randomization coverage | High-DoF dexterous hands; in-hand reorientation | OpenAI Dactyl [https://arxiv.org/abs/1808.00177](https://arxiv.org/abs/1808.00177) |

---

## Prerequisite Connections

- **Rigid-body dynamics (\(\tau = H(q)\ddot q + C(q,\dot q)\))** — Needed to understand how commanded torques/forces interact with contact forces and accelerations. Source: [https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf](https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf)
- **Unilateral constraints & complementarity** — Needed to reason about non-penetration and contact/no-contact switching. Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)
- **Feedback control loops / real-time constraints** — Needed to understand why contact manipulation is implemented at high rate (e.g., 1 kHz). Source: [https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)
- **State-machine thinking for robustness** — Needed to understand deployed manipulation architectures (primitives, retries, error handling). Sources: [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf), [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf)

---

## Socratic Question Bank

1. **If \(\phi(q) > 0\), what must \(\lambda_n\) be, and what does that mean physically?**  
   *Good answer:* \(\lambda_n=0\); separated bodies, no normal force (Unicomp complementarity).

2. **Why does a suction end-effector reduce the burden on perception accuracy compared to finger grasps?**  
   *Good answer:* grasp success is less sensitive to exact contact; seal feedback (pressure) confirms success; primitives can retry (APC systems).

3. **In the discrete complementarity \(0\le p_n \perp (\phi^k + h v_n^{k+1} + \epsilon)\ge 0\), what does \(p_n>0\) imply about the term in parentheses?**  
   *Good answer:* it must be 0 (constraint tight), linking impulse to next-step normal motion (Unicomp Eq. 25).

4. **What failure modes in APC picking are *not* solved by better object recognition alone?**  
   *Good answer:* small objects missed due to FK error; bulky items stuck during removal; unpickable geometry (pencil cup mesh) (APC-winning Table I discussion).

5. **Why might a hybrid automaton have many “error handling” transitions?**  
   *Good answer:* contact is uncertain; collisions and grasp failures are common; explicit recovery improves robustness (APC-winning: many transitions dedicated to error handling).

6. **What does “emergent finger gaiting” suggest about the policy’s internal strategy?**  
   *Good answer:* it learned to reconfigure contacts over time to achieve reorientation, not just static grasping (OpenAI Dactyl abstract).

7. **Why is a 1 kHz loop relevant for contact-rich tasks even if vision is slower?**  
   *Good answer:* contact dynamics change quickly; low-level stabilization needs high-rate feedback; libfranka enforces 1 kHz control structure.

---

## Likely Student Questions

**Q: What’s the exact mathematical statement of an LCP used for contact?**  
→ **A:** In Unicomp’s Sec. 2.1, the LCP is: find \(x\ge 0\) such that \(Mx+q\ge 0\) and \(x^\top(Mx+q)=0\). This encodes complementarity between \(x\) and \(Mx+q\). Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

**Q: How is non-penetration enforced in discrete time in Unicomp?**  
→ **A:** With the complementarity constraint \(0\le p_n \perp (\phi^k + h\,v_n^{k+1} + \epsilon)\ge 0\), where \(p_n\) is normal impulse, \(\phi^k\) is current gap, \(h\) is step size, and \(\epsilon\) is a regulation term. Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

**Q: What friction model does Unicomp use for stick–slip?**  
→ **A:** It uses maximum power dissipation with an ellipsoidal limit surface constraint: \(\left(\frac{\lambda_{t1}}{\mu \lambda_n}\right)^2+\left(\frac{\lambda_{t2}}{\mu \lambda_n}\right)^2+\left(\frac{\lambda_o}{\mu \lambda_n e_o}\right)^2 \le 1\). Source: [https://arxiv.org/html/2602.04522v1](https://arxiv.org/html/2602.04522v1)

**Q: What’s a concrete example of “feedback over planning” in real manipulation systems?**  
→ **A:** The APC-winning system uses suction-based top-down and side primitives with force-guarded motions, executed by a hybrid automaton (example: 26 states / 50 transitions, with 34 transitions for error handling). Source: [https://www.roboticsproceedings.org/rss12/p36.pdf](https://www.roboticsproceedings.org/rss12/p36.pdf)

**Q: How did the MIT APC system detect suction grasp success and handle failures?**  
→ **A:** It used a vacuum pressure sensor to confirm seal; the Suction primitive could attempt up to 5 times with XY jitter, stopping on contact via force control and checking expected contact height. Source: [https://arxiv.org/pdf/1604.03639.pdf](https://arxiv.org/pdf/1604.03639.pdf)

**Q: What does OpenAI’s dexterous in-hand manipulation work claim about training data and transfer?**  
→ **A:** Policies were trained entirely in simulation with randomization of physical properties (e.g., friction coefficients) and object appearance, and transferred to a physical Shadow Dexterous Hand; it did not rely on human demonstrations, and behaviors like finger gaiting emerged. Source: [https://arxiv.org/abs/1808.00177](https://arxiv.org/abs/1808.00177)

**Q: What are the hard real-time constraints for a Franka control loop?**  
→ **A:** `Robot::control(...)` runs at 1 kHz; the callback must compute quickly; `time_step` is 0 on the first invocation; you stop by returning `franka::MotionFinished(command)`. Source: [https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html)

---

## Available Resources

### Videos
- [Deep Learning for Robot Manipulation (CS287 Advanced Robotics lecture)](https://youtube.com/watch?v=KhgCnMFhNd8) — **Surface when:** student asks for a structured lecture tying grasp planning + dexterous manipulation + learning-based control together.

### Articles & Tutorials
- [MIT Manipulation Notes (Tedrake): Perception, Planning, and Control](https://manipulation.csail.mit.edu/) — **Surface when:** student wants a rigorous reference spanning grasping, contact, and system integration.
- [MIT Manipulation Notes: Clutter / bin picking simulation setup](https://manipulation.csail.mit.edu/clutter.html) — **Surface when:** student asks how to generate diverse cluttered manipulation scenarios in simulation without invalid initial penetrations.
- [MIT OCW 6.832 Underactuated Robotics (Tedrake)](https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/) — **Surface when:** student needs deeper control/dynamics foundations behind manipulation.
- [Lilian Weng — Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — **Surface when:** student asks about agent architectures (planning/memory/tool use) rather than low-level manipulation mechanics.

---

## Visual Aids

![LLM-powered autonomous agent system overview. (Weng, 2023)](/api/wiki-images/physical-ai-foundations/images/lilianweng-posts-2023-06-23-agent_001.png)  
**Show when:** student conflates “robot manipulation policy” with “full agent”; use to separate planning/memory/tooling from low-level control loops.

---

## Key Sources

- [Unified complementarity contact model (Unicomp)](https://arxiv.org/html/2602.04522v1) — Most precise source here for contact-rich manipulation math: complementarity, discrete time-stepping, friction limit surface.
- [Learning Dexterous In-Hand Manipulation (OpenAI et al.)](https://arxiv.org/abs/1808.00177) — Canonical sim-to-real RL example for dexterous in-hand reorientation with emergent behaviors.
- [Amazon Picking Challenge Winning System](https://www.roboticsproceedings.org/rss12/p36.pdf) — Concrete deployment lessons: embodiment (suction), feedback primitives, hybrid automata, failure modes, reliability numbers.
- [MIT APC 2015 End-to-End Picking System](https://arxiv.org/pdf/1604.03639.pdf) — Detailed perception→primitive execution pipeline with force/pressure feedback and retry logic.
- [libfranka `franka::Robot` control loop docs](https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html) — Authoritative reference for 1 kHz real-time control loop structure and termination semantics.