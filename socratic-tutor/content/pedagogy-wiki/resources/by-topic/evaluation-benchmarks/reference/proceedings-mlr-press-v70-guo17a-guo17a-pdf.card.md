# Card: Neural Network Calibration Metrics & Temperature Scaling (Guo et al., 2017)
**Source:** https://proceedings.mlr.press/v70/guo17a/guo17a.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Definitions of calibration metrics (ECE/MCE), reliability diagrams, temperature scaling procedure

## Key Content
- **Perfect calibration definition (Eq. 1):**  
  \[
  \mathbb{P}(\hat Y = Y \mid \hat P = p)=p,\ \forall p\in[0,1]
  \]  
  where \(\hat Y\) is predicted label, \(Y\) true label, \(\hat P\) confidence (probability assigned to \(\hat Y\)).
- **Reliability diagram binning (Section 2):** Partition predictions into \(M\) confidence bins \(I_m=(\frac{m-1}{M},\frac{m}{M}]\). Let \(B_m=\{i:\hat p_i\in I_m\}\).  
  \[
  \text{acc}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\mathbf{1}(\hat y_i=y_i),\quad
  \text{conf}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\hat p_i
  \]
- **Expected Calibration Error (ECE) (Eq. 3):**  
  \[
  \mathrm{ECE}=\sum_{m=1}^M \frac{|B_m|}{n}\,|\text{acc}(B_m)-\text{conf}(B_m)|
  \]
- **Maximum Calibration Error (MCE) (Eq. 5):**  
  \[
  \mathrm{MCE}=\max_{m\in\{1,\dots,M\}}|\text{acc}(B_m)-\text{conf}(B_m)|
  \]
- **Negative Log Likelihood (NLL) (Eq. 6):** \(L=-\sum_{i=1}^n \log \hat\pi(y_i|x_i)\).
- **Temperature scaling (multiclass) (Eq. 9, Section 4.2):** with logits \(z_i\), temperature \(T>0\):  
  \[
  \hat q_i=\max_k \mathrm{softmax}(z_i/T)_k
  \]
  Optimize \(T\) on a **held-out validation set** by minimizing **NLL**; **predicted class unchanged** (argmax invariant), so **accuracy unchanged**. \(T>1\) softens; \(T\to\infty\Rightarrow 1/K\); \(T\to 0\Rightarrow 1\).
- **Empirical defaults/results:** ECE reported with **\(M=15\) bins** (Table 1). Example: **CIFAR-100 ResNet-110 (SD)** ECE **12.67% → 0.96%** with temperature scaling (Figure 4/Table 1). **CIFAR-10 ResNet-110** ECE **4.6% → 0.83%**. Temperature scaling often best on vision tasks.
- **Compute/implementation note:** temperature scaling is **1D convex optimization**; reported ~**10 iterations** with conjugate gradient; implement by inserting a scalar multiply \(1/T\) between logits and softmax.

## When to surface
Use when students ask how to *measure* calibration (ECE/MCE, reliability diagrams) or how to *fix overconfidence* in deployed classifiers/agents via post-hoc temperature scaling without changing accuracy.