# Card: Robust visual sim-to-real via domain randomization + proxy tuning
**Source:** https://arxiv.org/pdf/2307.15320.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Quantitative sim-to-real manipulation results + DR ablations; proxy task for selecting DR parameters.

## Key Content
- **Policy + loss (Eq. 1, Sec. III-A):** Learn closed-loop visuomotor policy \(\pi_\theta(a_t|o_t)\). Action \(a_t=(v_t,\omega_t,g_t)\) with \(v_t\in\mathbb{R}^3\) linear vel, \(\omega_t\in\mathbb{R}^3\) angular vel, \(g_t\in\{0,1\}\) gripper open/close. Train by behavior cloning:  
  \[
  L=\lambda L_{\text{MSE}}((\hat v_t,\hat\omega_t),(v_t,\omega_t))+(1-\lambda)L_{\text{BCE}}(\hat g_t,g_t)
  \]
  with \(\lambda=0.8\).
- **Architecture (Fig. 2):** Two RGB cameras (90° baseline). Input: last 3 frames per view + last 3 proprioceptive values \(P_t=[pos_t,\sin\phi_t,\cos\phi_t]\). ResNet-18 per view → 512-d each; concat + MLP (2 layers, 512 hidden, ReLU).
- **DR components + tuned defaults (Sec. III-B, V-D):**
  - Textures: randomize robot/table/wall/floor (not objects). AmbientCG (1203 textures) >> procedural.
  - Lighting: sample light position on sphere: distance [1,3] m; azimuth [0, \(\pi/2\)]; polar [\(\pi/10\), \(4\pi/10\)]. Randomize diffuse/specular/ambient around 0.3 with offset in \([-0.6,0.6]\).
  - Object color: HSV offsets best at \(\phi_o=(0.05,0.1,0.1)\) (too large confuses colors).
  - Camera: position \(\pm10\) cm; angle \(\pm0.05\) rad; FOV \(\pm1^\circ\).
- **Proxy task (Sec. III-C):** Cube localization (3 colored cubes) predicts 3D cube positions relative to gripper; used to greedily pick DR params offline; correlates with real policy success.
- **Key empirical results:**
  - **Sim policy design (Table I, avg success in sim):** baseline (1 view, 1 frame) 44.97%; +2nd view 65.43%; +3 frames 93.94%; +proprio 98.34%.
  - **Proxy DR ablation (Table II, mean position error cm on real images):** 20k synth no DR 7.55 (default)/8.22 (variations); +ACG textures 2.52/3.53; +obj color 1.62/2.92; +camera 1.33/2.70; +2D aug 0.95/1.97; 100k synth +full DR 0.48/1.39. Real-only (750 imgs) 0.72/3.08 (worse under variations than synth+DR).
  - **Real robot success (Table III, 20 trials/task):** 2D aug only = 0/20 all tasks; +ACG textures avg 11.3/20; +light+obj color avg 14.0/20; +camera (full DR) avg 18.6/20 ≈ 93%.
  - **Robustness vs limited real data (Table IV, stacking):** DR avg 17.3/20 vs real-only 13.2/20; textured tablecloth DR 20/20 vs real-only 1/20.

## When to surface
Use when students ask how to choose/tune domain randomization for sim-to-real manipulation, or want concrete success-rate/ablation evidence comparing 2D aug vs 3D DR, textures, lighting, color, and camera randomization.