# Card: Temperature Scaling for Neural Net Calibration
**Source:** https://proceedings.mlr.press/v70/guo17a/guo17a.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Temperature scaling equation (logits ÷ T) + fitting T by NLL on validation set

## Key Content
- **Perfect calibration definition (Eq. 1):**  
  \[
  \Pr(\hat Y = Y \mid \hat P = p)=p,\ \forall p\in[0,1]
  \]
  where \(\hat Y\) is predicted class, \(\hat P\) is predicted confidence.
- **Reliability diagram binning (Section 2):** Partition confidences into \(M\) bins \(I_m=((m-1)/M,m/M]\). For bin \(B_m\):  
  \[
  \text{acc}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\mathbf{1}(\hat y_i=y_i),\quad
  \text{conf}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\hat p_i
  \]
- **Expected Calibration Error (ECE) (Eq. 3):**  
  \[
  \text{ECE}=\sum_{m=1}^M \frac{|B_m|}{n}\,|\text{acc}(B_m)-\text{conf}(B_m)|
  \]
- **Negative Log Likelihood objective (Eq. 6):**  
  \[
  L=-\sum_{i=1}^n \log \hat\pi(y_i\mid x_i)
  \]
- **Temperature scaling (multiclass) (Eq. 9, Section 4.2):** Given logits vector \(z_i\), calibrated probs use softmax on scaled logits:  
  \[
  \sigma_{\text{SM}}(z_i/T)^{(k)}=\frac{e^{z_i^{(k)}/T}}{\sum_{j=1}^K e^{z_i^{(j)}/T}},\quad
  \hat q_i=\max_k \sigma_{\text{SM}}(z_i/T)^{(k)}
  \]
  \(T>0\) fit by **minimizing NLL on a held-out validation set**; model weights fixed. **Argmax unchanged** (accuracy unchanged).
- **Rationale:** Modern nets overfit NLL → overconfident; a **single scalar \(T\)** often corrects miscalibration (“intrinsically low dimensional”).
- **Empirical (Table 1, \(M=15\) bins):** CIFAR-100 ResNet-110 (SD) ECE **12.67% → 0.96%** with temperature scaling; CIFAR-10 ResNet-110 **4.6% → 0.54%**.
- **Implementation note:** Insert multiplicative constant \(1/T\) between logits and softmax; set \(T=1\) during training, tune after.

## When to surface
Use when students ask how to “calibrate” classifier probabilities, what “temperature” does to softmax, or how to fit a temperature parameter (objective + steps).