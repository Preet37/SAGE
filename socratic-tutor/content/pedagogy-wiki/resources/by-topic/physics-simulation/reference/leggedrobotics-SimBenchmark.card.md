# Card: SimBenchmark — contact-rich physics engine comparison
**Source:** https://leggedrobotics.github.io/SimBenchmark/  
**Role:** benchmark | **Need:** COMPARISON_DATA  
**Anchor:** Benchmark suite comparing multiple physics engines on contact-rich robotics tasks using speed–accuracy curves + task-specific metrics (trajectory error, energy/momentum, penetration drift) and summarized rankings.

## Key Content
- **Motivation / rationale:** Contact dynamics accuracy + runtime are critical for legged robotics (feet–terrain contact drives whole-body motion). Contact dynamics is **NP-hard** due to non-convexity/discontinuity; engines use relaxed approximations with different accuracy/speed tradeoffs.
- **Multibody dynamics complexity:** naive articulated dynamics for **n links** has **O(n³)** complexity; modern engines use **linear-complexity** algorithms for efficiency.
- **Engines evaluated:** RaiSim (unreleased, proprietary), Bullet (2006, zlib), ODE (2001, GPL/BSD), MuJoCo (2015, proprietary), DART (2012, BSD).
- **Model/solver/integration (table facts):**
  - Contacts: RaiSim hard; Bullet hard/soft; ODE hard/soft; MuJoCo soft; DART hard.
  - Solvers: RaiSim bisection; Bullet MLCP; ODE LCP; MuJoCo Newton/PGS/CG; DART LCP.
  - Integrators: mostly semi-implicit Euler; MuJoCo also RK4.
  - Coordinates: ODE maximal; others minimal.
- **Evaluation methodology (procedure):**
  - Compare **speed–accuracy curves** (ideal = top-right).
  - For simple single-body few-contact cases: use **analytical trajectory** reference from **Newton rigid-body dynamics + Coulomb friction cone**.
  - For complex systems: evaluate generic quantities (**total kinetic energy**, **linear momentum**) + **penetration error** (position-level drift; should be 0 for rigid hard contacts).
- **Tests:** Rolling (friction), Bouncing (elastic collision), 666 balls (hard contact), Elastic 666 (energy), ANYmal PD (speed), ANYmal momentum, ANYmal energy.
- **Summary rankings (+ more is better):**
  - Rolling: Bullet +++; RaiSim ++; MuJoCo +; ODE −; DART −.
  - ANYmal PD: RaiSim +++++; MuJoCo ++++; Bullet +++; ODE +; DART ++.
  - ANYmal Momentum: ODE +++++; MuJoCo ++++ (RK4) / ++ (Euler); RaiSim +++; Bullet ++; DART +.
  - ANYmal Energy: MuJoCo +++++ (RK4) / +++ (Euler); RaiSim ++++; Bullet +++; ODE ++; DART +.
- **Noted limitations:** ODE/DART LCP can fail to simulate slip; DART poor with many objects; Bullet severe drift without post-solver correction; MuJoCo soft contact can’t control elasticity + consistent slip (needs post-process).

## When to surface
Use when students ask “which simulator is more accurate/fast for contacts or legged robots?”, “how to benchmark physics engines,” or “why engines differ on friction, drift, momentum/energy preservation.”