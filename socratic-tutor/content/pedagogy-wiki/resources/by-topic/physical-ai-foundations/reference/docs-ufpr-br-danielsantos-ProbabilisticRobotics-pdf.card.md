# Card: Bayes Filter → Kalman/EKF foundations
**Source:** https://docs.ufpr.br/~danielsantos/ProbabilisticRobotics.pdf  
**Role:** reference_doc | **Need:** FORMULA_SOURCE  
**Anchor:** Bayes filter framing; Markov assumptions; KF/EKF live in Ch.3 (Gaussian filters)

## Key Content
- **Belief (posterior) definition (Eq. 2.35):**  
  \[
  bel(x_t)=p(x_t\mid z_{1:t},u_{1:t})
  \]
  where \(x_t\)=state at time \(t\), \(z_t\)=measurement, \(u_t\)=control.
- **Prediction belief (Eq. 2.36):**  
  \[
  \overline{bel}(x_t)=p(x_t\mid z_{1:t-1},u_{1:t})
  \]
- **Markov/conditional independence assumptions:**  
  **State transition (Eq. 2.33):**  
  \[
  p(x_t\mid x_{0:t-1},z_{1:t-1},u_{1:t})=p(x_t\mid x_{t-1},u_t)
  \]
  **Measurement model (Eq. 2.34):**  
  \[
  p(z_t\mid x_{0:t},z_{1:t-1},u_{1:t})=p(z_t\mid x_t)
  \]
  These define a **DBN/HMM** with transition \(p(x_t\mid x_{t-1},u_t)\) and sensor model \(p(z_t\mid x_t)\) plus initial \(p(x_0)\).
- **Bayes rule (Eq. 2.15):**  
  \[
  p(x\mid y)=\eta\,p(y\mid x)p(x)
  \]
  (\(\eta\)=normalizer independent of \(x\)).
- **Total probability (Eq. 2.11–2.12):**  
  \[
  p(x)=\sum_y p(x\mid y)p(y)\quad\text{or}\quad p(x)=\int p(x\mid y)p(y)\,dy
  \]
- **Gaussian PDF (Eq. 2.4):**  
  \[
  \mathcal N(x;\mu,\Sigma)=\det(2\pi\Sigma)^{-1/2}\exp\{-\tfrac12(x-\mu)^T\Sigma^{-1}(x-\mu)\}
  \]
  (basis for KF/EKF in **Chapter 3**).

## When to surface
Use when students ask how sensing and action update state estimates (Bayes filter), what assumptions justify recursion (Markov), or when deriving/connecting KF/EKF predict-update steps to the general Bayes filter.