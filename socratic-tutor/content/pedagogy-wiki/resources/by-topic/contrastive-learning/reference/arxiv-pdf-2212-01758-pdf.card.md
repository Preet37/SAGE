# Card: LiT/CLIP Zero-shot Robustness via Self-Consistency + WordNet Hierarchy
**Source:** https://arxiv.org/pdf/2212.01758.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Concrete zero-shot ImageNet(+shift) numbers for CLIP/LiT; post-hoc confidence via self-consistency; hierarchy-based label augmentation procedure.

## Key Content
- **Zero-shot logit (cosine sim):**  
  \(z_m=f_{\text{image}}(x)\), \(z_c=f_{\text{text}}(c)\).  
  \(\text{logit}(x,c)=\cos(z_m,z_c)\); predict \(\hat c(x,\emptyset)=\arg\max_{c\in C}\text{logit}(x,c)\). (Sec. 4.1)
- **Prompt self-consistency confidence (Eq. 1):** for prompt set \(T\),  
  \(S_T(x)=\frac{1}{|T|}\sum_{t\in T}\mathbf{1}\{\hat c(x,t)=\hat c(x,\emptyset)\}\), where \(\hat c(x,t)=\arg\max_{c\in C}\text{logit}(x,t(c))\).
- **Image-perturbation self-consistency (Eq. 2):** for transforms \(B\),  
  \(S_B(x)=\frac{1}{|B|}\sum_{b\in B}\mathbf{1}\{\hat c(x,b)=\hat c(x,\emptyset)\}\), where \(\hat c(x,b)=\arg\max_{c}\text{logit}(b(x),c)\). Best single perturbation: **left-right flip**.
- **Low-confidence set construction:** union \(O=O_T\cup O_B\). For ImageNet, split CLIP’s **80 prompts** into \(T_1\) (first 40), \(T_2\) (last 40), \(T_3\) (all 80), \(T_4=\emptyset\); mark low-confidence if top-1 predictions disagree across sets.
- **Hierarchy label augmentation (Sec. 4.2, Alg. 2):** rerank only **top-5** predicted classes using WordNet parent \(p(c)\) and children \(c_1..c_r\). Combined score (Eq. 3):  
  \(\text{logit}(x,c)=\max\{\text{logit}(x,[c;p(c)]), \text{logit}(x,[c_1;p(c)]),...,\text{logit}(x,[c_r;p(c)])\}\). Natural-language template used: “**{child} which is a kind of {parent}**”. Prune overly abstract/rare WordNet terms; rarity estimated via **variance of text-embedding norms across prompts**.
- **Empirical results (Table 1):**  
  - **CLIP ViT-B/16** ImageNet top-1: low-conf **21.58→38.71%** (+17.13); full **64.18→67.78%** (+3.60).  
  - **LiT ViT-B/32** ImageNet top-1: low-conf **31.18→37.25%**; full **68.26→69.41%**.  
  - Shifted sets (CLIP full): ImageNet-v2 **58.06→61.07**, IN-R **56.88→59.46**, IN-A **26.12→29.23**, IN-Sketch **44.71→47.28**.
- **Confidence estimator quality (Fig. 3):** AUROC vs max-logit baseline: **CLIP 0.84 vs 0.67**, **LiT 0.81 vs 0.70**; better selective prediction at all abstention rates.

## When to surface
Use when students ask about (1) why CLIP/LiT zero-shot top-1 lags top-5, (2) confidence/abstention for dual-encoder models, or (3) concrete benchmark gains from post-hoc prompt/hierarchy methods on ImageNet and its shifts.