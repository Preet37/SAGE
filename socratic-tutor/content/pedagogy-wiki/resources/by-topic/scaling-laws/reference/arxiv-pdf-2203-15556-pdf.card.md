# Card: Chinchilla compute-optimal scaling (tokens vs parameters)
**Source:** https://arxiv.org/pdf/2203.15556.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Compute-optimal training prescription (Chinchilla-style): optimal tokens-to-parameters allocation from scaling-law fits + explicit equations/exponents.

## Key Content
- **Goal (Eq. 1):** choose parameters **N** and training tokens **D** to minimize final loss under compute budget **C**:  
  \[
  (N_{\text{opt}}(C),D_{\text{opt}}(C))=\arg\min_{N,D\ \text{s.t.}\ \text{FLOPs}(N,D)=C} L(N,D)
  \]
- **Compute model:** \(\text{FLOPs}(N,D)\approx 6ND\) (Section 3.3; Kaplan-style).
- **Parametric loss model (Eq. 2):**  
  \[
  \hat L(N,D)=E + A N^{\alpha} + B D^{\beta}
  \]
  Fit by minimizing Huber loss on log-loss (Eq. 3): \(\min \sum_i \text{Huber}_\delta(\log \hat L(N_i,D_i)-\log L_i)\), with \(\delta=10^{-3}\), optimized via L-BFGS.
- **Closed-form compute-optimal frontier (Eq. 4):**  
  \[
  N_{\text{opt}}(C)=G\left(\frac{C}{6}\right)^a,\quad D_{\text{opt}}(C)=G^{-1}\left(\frac{C}{6}\right)^b
  \]
  where \(G=\left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha+\beta}},\ a=\frac{\beta}{\alpha+\beta},\ b=\frac{\alpha}{\alpha+\beta}\).
- **Empirical exponents (Table 2):**  
  Approach1: \(a=0.50,\ b=0.50\); Approach2: \(a=0.49,\ b=0.51\); Approach3: \(a=0.46,\ b=0.54\). **Contrast:** Kaplan et al. (2020) \(a=0.73,\ b=0.27\). Interpretation: **scale tokens ~ proportionally with parameters** (doubling N ⇒ ~doubling D).
- **Key compute-optimal comparison:** Gopher compute \(C=5.76\times10^{23}\) FLOPs. Predicted optimal model size **~40–70B** params; they train **Chinchilla 70B on 1.4T tokens** (vs **Gopher 280B on 300B tokens**) at same compute.
- **Table 3 examples (Approach 1 projections):**  
  67B → \(5.76\times10^{23}\) FLOPs, **1.5T tokens**; 175B → \(3.85\times10^{24}\) FLOPs, **3.7T tokens**; 280B → \(9.90\times10^{24}\) FLOPs, **5.9T tokens**; 1T → \(1.27\times10^{26}\) FLOPs, **21.2T tokens**.
- **Procedure notes:** learning-rate cosine schedule length should **match token horizon D**; envelope-of-best-loss-per-FLOP (Approach 1) and IsoFLOP valleys (Approach 2) both recover similar scaling.

## When to surface
Use when students ask: “How many tokens should I train for a given model size/compute?” “What is the Chinchilla scaling law?” “Why smaller models trained longer can beat larger ones at same FLOPs?”