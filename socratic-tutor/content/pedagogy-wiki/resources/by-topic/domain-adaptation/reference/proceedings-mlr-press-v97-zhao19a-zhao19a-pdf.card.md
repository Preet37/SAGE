# Card: Invariant representations can fail in Domain Adaptation
**Source:** http://proceedings.mlr.press/v97/zhao19a/zhao19a.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Formal bounds/counterexamples for invariant representation learning; sufficient/necessary conditions via conditional shift + label-marginal mismatch.

## Key Content
- **DA setup/notation (Sec. 2):** Source domain ⟨D_S, f_S⟩, target ⟨D_T, f_T⟩ with deterministic labels Y=f(X). Hypothesis h: X→{0,1}. Risk: ε_S(h,f):=E_{x~D_S}[|h(x)-f(x)|]; ε_S(h):=ε_S(h,f_S) (similarly ε_T).
- **H-divergence (Def. 2.1):** A_H:={h^{-1}(1) | h∈H}.  
  d_H(D,D′):= sup_{A∈A_H} |Pr_D(A) − Pr_{D′}(A)|.
- **Classic DA bound (Thm 2.1, Eq. (1)):** For VC-dim d, w.p. ≥1−δ, ∀h∈H:  
  ε_T(h) ≤ \hat ε_S(h) + ½ d_{HΔH}(\hat D_S,\hat D_T) + λ* + O(√((d log n + log(1/δ))/n)),  
  where h*:=argmin_{h∈H} ε_S(h)+ε_T(h), λ*:=ε_S(h*)+ε_T(h*).
- **Counterexample (Sec. 4.1, Fig. 1):** X=Z=R.  
  D_S=U(−1,0), f_S(x)=0 if x≤−½ else 1.  
  D_T=U(1,2), f_T(x)=0 if x≥3/2 else 1.  
  There exists h*(x)=1 iff x∈(−½,3/2) with **0 error on both**.  
  But with g(x)=I_{x≤0}(x+1)+I_{x>0}(x−1): induced D_ZS=D_ZT=U(0,1) (perfectly invariant), yet **∀h: ε_S(h∘g)+ε_T(h∘g)=1** (smaller source error ⇒ larger target error). Here λ*_g=1.
- **Sufficient-condition bound without λ\* (Thm 4.1):** For H⊆[0,1]^X, ∀h∈H:  
  ε_T(h) ≤ ε_S(h) + d_{\tilde H}(D_S,D_T) + min{E_{D_S}|f_S−f_T|, E_{D_T}|f_S−f_T|},  
  where \tilde H := { sgn(|h(x)−h′(x)|−t) : h,h′∈H, t∈[0,1] }.  
  Note: E_{D_S}|f_S−f_T|=ε_S(f_T), E_{D_T}|f_S−f_T|=ε_T(f_S) (cross-domain errors).
- **Info-theoretic lower bound (Sec. 4.3):** With Markov chain X→^g Z→^h Ŷ and JS distance d_JS:  
  Lemma 4.8: d_JS(D_{Y_S},D_{Y_T}) ≤ d_JS(D_{Z_S},D_{Z_T}) + √ε_S(h∘g)+√ε_T(h∘g).  
  Thm 4.3: if d_JS(D_{Y_S},D_{Y_T}) ≥ d_JS(D_{Z_S},D_{Z_T}), then  
  ε_S(h∘g)+ε_T(h∘g) ≥ ½ ( d_JS(D_{Y_S},D_{Y_T}) − d_JS(D_{Z_S},D_{Z_T}) )^2.  
  ⇒ If label marginals differ, forcing invariance (small d_JS(D_ZS,D_ZT)) can **force large joint error**.
- **Empirical pipeline (Sec. 5):** DANN on MNIST/USPS/SVHN (10 classes). Preprocess to grayscale 16×16. Classifier: 2 conv layers (5×5 kernels; 10 then 20 channels) → FC 1280→100 → softmax(10). Discriminator: conv features → FC 500→100 → 1-unit domain output. Observation: target accuracy rises quickly (<10 iters) then decreases with continued training (over-training hurts when label distributions differ).

## When to surface
Use when students claim “domain-invariant features + low source error guarantees low target error,” or ask for formal bounds/counterexamples involving conditional shift, label shift, and invariant representation learning.