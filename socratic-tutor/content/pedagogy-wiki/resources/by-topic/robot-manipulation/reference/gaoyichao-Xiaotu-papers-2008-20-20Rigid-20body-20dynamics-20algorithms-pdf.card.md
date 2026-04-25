# Card: Manipulator dynamics via spatial vectors (RNEA/CRBA/ABA)
**Source:** https://gaoyichao.com/Xiaotu/papers/2008%20-%20Rigid%20body%20dynamics%20algorithms.pdf  
**Role:** explainer | **Need:** FORMULA_SOURCE  
**Anchor:** Derivations + pseudocode for RNEA (inverse dynamics), CRBA & ABA (forward dynamics), using 6D spatial vectors to build \(H(q)\)/\(M(q)\) and bias terms \(C(q,\dot q)\), incl. gravity/external forces.

## Key Content
- **Canonical equation of motion (Eq. 1.1):**  
  \[
  \tau = H(q)\,\ddot q + C(q,\dot q)
  \]
  \(q,\dot q,\ddot q\): generalized position/velocity/acceleration; \(\tau\): generalized forces; \(H\): joint-space inertia; \(C\): Coriolis/centrifugal + gravity + other non-\(\tau\) forces.
- **Forward/inverse dynamics function interfaces (Eqs. 1.2–1.3):**  
  \[
  \ddot q = FD(\text{model},q,\dot q,\tau),\qquad
  \tau = ID(\text{model},q,\dot q,\ddot q)
  \]
  with \(FD = H^{-1}(\tau - C)\), \(ID = H\ddot q + C\).
- **Spatial rigid-body equation (Eq. 1.5):**  
  \[
  f = I a + v \times^{*} (I v)
  \]
  \(v,a\): spatial (6D) velocity/acceleration; \(f\): spatial force; \(I\): spatial inertia; \(\times^{*}\): spatial cross-product operator.
- **Design rationale:** spatial (6D) notation unifies linear+angular quantities, reduces algebra, enables efficient recursion; spatial inertias add under rigid attachment: \(I_{\text{new}}=I_1+I_2\).
- **Algorithmic workflow (Chs. 5–7):**
  - **RNEA (inverse dynamics):** 2-pass recursion—forward pass propagates kinematics; backward pass accumulates subtree forces → joint torques \(\tau\).
  - **CRBA:** computes \(H(q)\) efficiently via composite rigid-body inertias.
  - **ABA:** forward dynamics recursion to compute \(\ddot q\) without explicitly forming \(H\).

## When to surface
Use when students ask how to compute \(M(q)\)/\(H(q)\), bias terms \(C(q,\dot q)\), or implement inverse/forward dynamics efficiently (RNEA/CRBA/ABA) for kinematic-tree robots using spatial vectors.