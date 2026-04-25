# Card: KIE benchmarks have train/test template leakage (SROIE, FUNSD)
**Source:** https://arxiv.org/pdf/2304.14936.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Empirical evidence that standard KIE benchmarks overestimate generalization due to train/test template similarity; proposes resampled “0% overlap” splits and reports performance drops.

## Key Content
- **Problem/Rationale (Sec. 3.1):** Official IID splits can include near-duplicate document templates across train/test, enabling memorization rather than **generalization to unseen templates** (real-world domain shift).
- **Task formalization (Eq. 1, Sec. 2.3):** Token classification for KIE with IOB tags.  
  - Tokens: \(T=\{t_i\}_{0<i\le n}\) from document \(D\); image \(I\).  
  - Entity types \(m\) ⇒ classes \(2m+1\) (B-entity, I-entity, O).  
  - Classifier: \(F(t_i\mid T,I)=c,\; c\in\{1,\dots,2m+1\}\). Entity correct only if all span tokens correctly tagged.
- **Template similarity quantification (Sec. 3.2):**
  - **SROIE:** group receipts by **business/template**; found **75% template replication in the official test set** (abstract). Group sizes range **1–76** receipts.
  - **FUNSD:** define form similarity via question overlap:  
    \[
    \text{Overlap}(doc_A,doc_B)=\frac{\text{Count}(Questions_A\cap Questions_B)}{\max(\lvert Questions_A\rvert,\lvert Questions_B\rvert)}
    \]
    Use threshold **0.7**; in official test set, **8/50 = 16%** forms share a template with training.
  - **Resampling rule:** ensure each template group appears in **only one split** (“0% overlap”).
- **Training defaults (Sec. 4.1):** batch size **2**; Adam; LR **2e-5**; halve LR every **10 epochs** w/o val-F1 improvement; stop when LR < **1e-7**; pick best val-F1. For each experiment: fixed test set; create **4** train/val splits (80/20) from remaining data; report average.
- **Empirical impact (Tables 1–2, Sec. 4.3):**
  - **SROIE:** average F1 drops **94.34 → 85.60**; best F1 **96.55 → 89.38**. Text-only models drop **~10.5 F1** vs multimodal **~7.5 F1**.
  - **FUNSD:** text-only models drop **~3.5 F1** vs multimodal **~0.5 F1** on adjusted splits.

## When to surface
Use when students ask why SROIE/FUNSD scores may not reflect real-world KIE generalization, how to design fairer splits, or what evidence shows template leakage inflates benchmark performance.