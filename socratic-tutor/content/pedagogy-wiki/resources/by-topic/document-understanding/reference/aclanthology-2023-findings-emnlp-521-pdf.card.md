# Card: Gaussian-biased layout attention (LAGaBi)
**Source:** https://aclanthology.org/2023.findings-emnlp.521.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Explicit math for injecting 2D geometry into attention via polar coords + Gaussian bias; ablations/impact

## Key Content
- **Polar relative geometry (Section 3.1):** For query token *i* and key token *j*, using normalized top-left box coords \((x_i,y_i)\), \((x_j,y_j)\):  
  - Distance \(\rho_{ij}=\sqrt{(x_j-x_i)^2+(y_j-y_i)^2\) (Eq. 1), \(\rho_{ij}\in[0,1]\)  
  - Angle \(\theta_{ij}=\tan^{-1}\left(\frac{y_j-y_i}{x_j-x_i}\right)\) (Eq. 2), \(\theta_{ij}\in[-\pi/2,\pi/2]\)  
  - Spatial relation \(u_{ij}=(\rho_{ij},\theta_{ij})\).
- **Gaussian layout bias + attention injection (Section 3.2):** Modify single-head attention distribution:  
  \[
  a_{ij}=\frac{\exp\left(\frac{q_i k_j^\top}{\sqrt{d_k}}+\alpha\,(g(u_{ij})-1)\right)}{\sum_{j=1}^N \exp\left(\frac{q_i k_j^\top}{\sqrt{d_k}}+\alpha\,(g(u_{ij})-1)\right)}
  \]  
  (Eq. 3) where \(q_i,k_j\) are query/key vectors, \(d_k\) head dim, \(\alpha\) trade-off.  
  Bias from 2D Gaussian kernel:  
  \[
  g(u)=\exp\left(-\tfrac12 (u-\mu)^\top \Sigma^{-1}(u-\mu)\right)
  \]
  (Eq. 4), with learnable \(\mu\in\mathbb{R}^{2\times1}\), \(\Sigma\in\mathbb{R}^{2\times2}\) **diagonal** (2 params). Kernels differ per head, **shared across layers**. Extra params \(=2\times2\times N_{\text{heads}}\) (e.g., 12 heads → **48 params**). Layout affects **queries/keys, not values**.
- **Defaults/training:** Coordinates normalized to integers \([0,1000]\); special tokens get empty box \([0,0,0,0]\). Fine-tune 2000 steps, batch 16; Adam; LR \(5e{-5}\) (FUNSD) / \(7e{-5}\) (CORD/XFUND). \(\alpha\) tuned best at **4** (CORD val: 94.77 at \(\alpha=4\); Table 4).
- **Key results (F1):**  
  - RoBERTa baseline: FUNSD **66.48**, CORD **93.54** (Table 1).  
  - RoBERTa+LAGaBi (no doc pretrain): FUNSD **84.84** (+18.36), CORD **95.97** (+2.43).  
  - RoBERTa+LAGaBi (1M doc pretrain): FUNSD **89.15**, CORD **96.56**.  
  - Ablations (Table 3, FUNSD / CORD val): baseline 66.48/92.29; +embedding 69.59/92.67; +linear bias 76.32/93.00; +fixed Gaussian 83.81/93.00; +Euclidean dist 73.05/93.72; +angle only 84.48/94.70; +2D-xy dist 79.85/94.21; **full LAGaBi 84.84/94.77**. Angle > distance; learnable Gaussian > fixed/linear.

## When to surface
Use when students ask “how do layout-aware transformers inject 2D geometry into attention?” or need concrete equations/ablations comparing polar+Gaussian biases vs Cartesian distances/embeddings in document understanding.