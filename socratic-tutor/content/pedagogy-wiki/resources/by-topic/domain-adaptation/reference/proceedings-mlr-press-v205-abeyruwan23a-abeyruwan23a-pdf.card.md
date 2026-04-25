# Card: i-S2R (Iterative Sim-to-Real) for Human-Robot Table Tennis
**Source:** https://proceedings.mlr.press/v205/abeyruwan23a/abeyruwan23a.pdf  
**Role:** paper | **Need:** WORKING_EXAMPLE  
**Anchor:** Iterative sim↔real RL pipeline that updates a *human behavior model* from real interaction data to reduce sim-to-real gap in tight HRI; includes transfer/generalization results.

## Key Content
- **Objective / MDP (Section 3):** MDP \((S,A,R,p)\), policy \(\pi_\theta:S\to A\), maximize expected return  
  \[
  \mathbb{E}\left[\sum_{t=1}^{N} r(s_t,\pi_\theta(s_t))\right]
  \]
  Episodes simplified: start with a hit (no serve); episode = single ball throw + return; reward encourages cooperative returns → longer rallies.
- **Iterative-Sim-to-Real procedure (Section 4, Fig. 2):**
  1) Collect initial human-only data \(D_0\) (player hits across table, no robot).  
  2) Fit initial human ball distribution model \(M_0\).  
  3) Train policy in sim on balls sampled from \(M_k\) → \(\theta_k^S\).  
  4) Deploy + **real fine-tune with human-in-loop** → \(\theta_k^R\); collect interaction hits → update dataset \(D_{k+1}\).  
  5) Update human model \(M_{k+1}\) from \(D_{k+1}\); continue sim training from \(\theta_k^R\). Repeat until model deltas shrink (they found ~3 iterations sufficient).
- **Human behavior model (Section 4):** uniform distribution defined by **16 numbers**: min/max of initial ball position (6), velocity (6), and landing \(x,y\) on robot side (4). Fit per-trajectory initial pos/vel by Nelder–Mead minimizing Euclidean trajectory error; remove outliers via DBSCAN; take per-dimension min/max.
- **RL optimizer (Section 3):** Blackbox Gradient Sensing (BGS), an ES method optimizing smoothed objective (Eq. 1):  
  \[
  F_\sigma(\theta)=\mathbb{E}_{\delta\sim\mathcal{N}(0,I)}[F(\theta+\sigma\delta)]
  \]
  Uses orthogonal perturbation ensembles + “elite-choice” sample selection; other RL (PPO, SAC, QT-OPT) didn’t transfer as well.
- **System / policy defaults (Section 5):** 8-DOF robot (6-DOF arm + 2D linear actuator). Obs = 3D ball pos + 8 joint angles = 11D; stack past **7** obs → input size \(8\times 11\). Action = 8 joint velocities at **75 Hz**. Policy net: 3-layer 1D dilated gated CNN. Sim: PyBullet; add uniform ball obs noise = **2× ball diameter** per timestep; must simulate sensor/action latency (Gaussian from real measurements) or transfer “completely failed.”
- **Key empirical results (Abstract, Section 6–7):**
  - Final performance: **22 hits average**, **150 best** rally.  
  - For **80% of players**, i-S2R rallies **70%–175% longer** than S2R+FT baseline (beginner ≈70%, intermediate ≈175%).  
  - Aggregated: i-S2R ≈ **9%** higher rally length than S2R+FT.  
  - Cross-eval generalization: i-S2R retains ~**70%** of self-performance vs S2R+FT ~**30%** (Fig. 7).  
  - S2R-Oracle+FT (trained on penultimate learned human model) matches i-S2R with only **35%** of real fine-tuning budget → gains largely from improved human model.

## When to surface
Use for questions about **domain adaptation / sim-to-real in HRI**, especially iterative system identification of *human behavior distributions*, why latency/noise modeling matters, and how iterative sim↔real updates improve **transfer and generalization**.