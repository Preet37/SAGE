# Card: ComplEx scoring + logistic NLL objective
**Source:** https://arxiv.org/pdf/1606.06357.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** ComplEx scoring function (complex tri-linear product with conjugation) + training objective for link prediction

## Key Content
- **Link prediction probability (single relation):**  
  \(P(Y_{so}=1)=\sigma(X_{so})\) (Eq. 1), where \(Y_{so}\in\{-1,1\}\), \(\sigma(x)=\frac{1}{1+e^{-x}}\), and \(X_{so}\) is a real-valued score.
- **Hermitian dot product (complex vectors):**  
  \(\langle u,v\rangle := \overline{u}^{\top}v\) (Eq. 3), with \(u=\Re(u)+i\Im(u)\), \(\overline{u}=\Re(u)-i\Im(u)\). Conjugation breaks symmetry → can model antisymmetry.
- **ComplEx multi-relational scoring:**  
  \(P(Y_{rso}=1)=\sigma(\phi(r,s,o;\Theta))\) (Eq. 8) with  
  \(\phi(r,s,o;\Theta)=\Re(\langle w_r, e_s, \overline{e_o}\rangle)\) (Eq. 9)  
  \(=\Re\left(\sum_{k=1}^{K} w_{rk} e_{sk}\overline{e_{ok}}\right)\) (Eq. 10), where \(e_s,e_o,w_r\in\mathbb{C}^K\).  
  Real-only expansion (Eq. 11):  
  \(\langle \Re(w_r),\Re(e_s),\Re(e_o)\rangle+\langle \Re(w_r),\Im(e_s),\Im(e_o)\rangle+\langle \Im(w_r),\Re(e_s),\Im(e_o)\rangle-\langle \Im(w_r),\Im(e_s),\Re(e_o)\rangle\).  
  Symmetric if \(w_r\) real; antisymmetric if \(w_r\) purely imaginary.
- **Training objective (logistic negative log-likelihood):**  
  \(\min_{\Theta}\sum_{r(s,o)\in\Omega}\log(1+\exp(-Y_{rso}\phi(r,s,o;\Theta)))+\lambda\|\Theta\|_2^2\) (Eq. 12).  
  Negatives via **local closed world**: corrupt subject or object; generate \(\eta\) negatives per positive (runtime).
- **Optimization defaults:** mini-batch SGD + AdaGrad; early stopping on validation filtered MRR (checked every 50 epochs; max 1000). Grid: \(K\in\{10,20,50,100,150,200\}\), \(\lambda\in\{0.1,0.03,0.01,0.003,0.001,0.0003,0\}\), \(\alpha_0\in\{1.0,0.5,0.2,0.1,0.05,0.02,0.01\}\), \(\eta\in\{1,2,5,10\}\); batch size 100.
- **Key empirical results (Table 2):**  
  WN18 filtered MRR: ComplEx **0.941** (DistMult 0.822; TransE 0.454; HolE 0.938).  
  FB15K filtered MRR: ComplEx **0.692** (DistMult 0.654; HolE 0.524; TransE 0.380). Hits@1 FB15K: ComplEx **0.599**.
- **Negatives effect (FB15K):** with \(K=200,\lambda=0.01,\alpha_0=0.5\), \(\eta=100\) gives filtered MRR **0.737** and Hits@1 **64.8%**; performance drops at \(\eta=200\).

## When to surface
Use when students ask how ComplEx computes triple scores/probabilities, why complex conjugation enables antisymmetric relations, or what exact loss/negative-sampling/training setup is used for KG link prediction.