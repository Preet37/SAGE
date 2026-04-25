# Card: Domain Adaptation Generalization Bound (A-distance + labeling disagreement)
**Source:** https://proceedings.neurips.cc/paper/2006/file/b1b0432ceafb0ce714426e9114852ac7-Paper.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Upper bound on target risk including (i) source empirical risk, (ii) domain discrepancy via \(d_{\mathcal H}\) (A-distance), and (iii) conditional/labeling-function disagreement term \(\lambda\).

## Key Content
- **Setup (Sec. 2):** Representation \(R:X\to Z\). Induced feature distributions: \(\Pr_{\tilde D}[B]=\Pr_D[R^{-1}(B)]\). Induced labeling: \(\tilde f(z)=\mathbb E_D[f(x)\mid R(x)=z]\).  
  Predictor \(h:Z\to\{0,1\}\). Errors:  
  \[
  \epsilon_S(h)=\mathbb E_{z\sim \tilde D_S}\big[|\tilde f(z)-h(z)|\big],\quad
  \epsilon_T(h)=\mathbb E_{z\sim \tilde D_T}\big[|\tilde f(z)-h(z)|\big].
  \]
- **A-distance / \(\mathcal H\)-divergence (Sec. 3.1–3.2):** For subset family \(\mathcal A\),  
  \[
  d_{\mathcal A}(D,D')=2\sup_{A\in\mathcal A}|\Pr_D[A]-\Pr_{D'}[A]|.
  \]
  For hypothesis class \(\mathcal H\), use \(\mathcal A=\{Z_h:h\in\mathcal H\}\) and denote \(d_{\mathcal H}(\tilde D_S,\tilde D_T)\).
- **Labeling disagreement / conditional shift term (Sec. 3.1):** \(\tilde f\) is **\(\lambda\)-close** to \(\mathcal H\) if  
  \[
  \inf_{h\in\mathcal H}\big(\epsilon_S(h)+\epsilon_T(h)\big)\le \lambda.
  \]
- **Main bound (Thm. 1, Sec. 3.2):** For VC-dim \(d\), labeled source sample size \(m\), w.p. \(\ge 1-\delta\), \(\forall h\in\mathcal H\):  
  \[
  \epsilon_T(h)\le \hat\epsilon_S(h)+\sqrt{\frac{4}{m}\Big(d\log\frac{2em}{d}+\log\frac{4}{\delta}\Big)}+d_{\mathcal H}(\tilde D_S,\tilde D_T)+\lambda.
  \]
- **Computable version with unlabeled samples (Thm. 2):** With unlabeled \(\tilde U_S,\tilde U_T\) of size \(m'\):  
  \[
  \epsilon_T(h)\le \hat\epsilon_S(h)+4\sqrt{\frac{d\log\frac{2em}{d}+\log\frac{4}{\delta}}{m}}+\lambda+d_{\mathcal H}(\tilde U_S,\tilde U_T)+4\sqrt{\frac{d\log(2m')+\log\frac{4}{\delta}}{m'}}.
  \]
- **Estimating \(d_{\mathcal H}\) from domain-classification (Sec. 4):** Given \(\tilde U_S,\tilde U_T\) (each size \(m'\)), define domain-discrimination error  
  \[
  \mathrm{err}(h)=\frac{1}{2m'}\sum_{i=1}^{2m'}\big|h(z_i)-\mathbf 1[z_i\in \tilde U_S]\big|.
  \]
  Then  
  \[
  d_{\mathcal A}(\tilde U_S,\tilde U_T)=2\Big(1-2\min_{h'\in\mathcal H}\mathrm{err}(h')\Big).
  \]
  For linear separators, exact optimization NP-hard; authors approximate via convex surrogate (modified Huber loss) + SGD.
- **Empirical numbers (Sec. 5.3, Fig. 2b; PoS WSJ→MEDLINE, projection dim \(d=200\)):**  
  - Identity: Huber loss 0.003, A-distance 1.796, target error 0.253  
  - Random Proj: Huber loss 0.254, A-distance 0.223, target error 0.561  
  - SCL: Huber loss 0.07, A-distance 0.211, target error 0.216  
  Data: 100 labeled WSJ sentences (~2500 words); 1M unlabeled words (500k/domain) to estimate A-distance.

## When to surface
Use when students ask for a **formal target-risk bound in domain adaptation** (sim-to-real, covariate shift) that separates **source error**, **domain discrepancy**, and **labeling-function disagreement (\(\lambda\))**, or how to **estimate discrepancy via a domain classifier**.