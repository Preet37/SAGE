# Card: SACN (WGCN + Conv-TransE) for Knowledge Base Completion
**Source:** http://arxiv.org/pdf/1811.04441v2.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** SACN/Conv-TransE definitions + link-prediction results (MRR/Hits@K) on FB15k-237, WN18RR (+ Attr variant)

## Key Content
- **KG setting:** triples \((s,r,o)\); link prediction evaluated with **filtered** ranking (filter valid triples before ranking). Metrics: **Hits@1/3/10** and **MRR** (Experiments).
- **WGCN encoder (Eq. 1–5):** multi-relational GCN with learnable relation-type weights \(\alpha_t\).
  - Node update (with self-loop) (Eq. 3):  
    \[
    h^{l+1}_i=\sigma\Big(\sum_{j\in N_i}\alpha^l_t\, h^l_j W^l + h^l_i W^l\Big)
    \]
    where \(h^l_i\in\mathbb{R}^{F_l}\), \(W^l\in\mathbb{R}^{F_l\times F_{l+1}}\), \(\sigma\)=activation.
  - Weighted adjacency (Eq. 4): \(A^l=\sum_{t=1}^T \alpha^l_t A_t + I\). Layer form (Eq. 5): \(H^{l+1}=\sigma(A^l H^l W^l)\).
- **Attributes as nodes:** represent each attribute type as an **attribute node** (not sparse vectors); connect via \((entity, relation, attribute)\) triples to “bridge” entities.
- **Conv-TransE decoder (Eq. 6–8):** no reshaping; uses \(2\times k\) kernels over stacked \((e_s,e_r)\) to preserve translational behavior.
  - Convolution (Eq. 6):  
    \(m_c(e_s,e_r,n)=\sum_{\tau=0}^{K-1}\omega_c(\tau,0)\hat e_s(n+\tau)+\omega_c(\tau,1)\hat e_r(n+\tau)\).
  - Score (Eq. 7): \(\psi(e_s,e_o)= f(\mathrm{vec}(M(e_s,e_r))W)\, e_o\); probability (Eq. 8): \(p=\sigma(\psi)\).
- **Empirical results (Table 3):**
  - **FB15k-237:** ConvE Hits@10/3/1/MRR = **0.49/0.35/0.24/0.32**; Conv-TransE **0.51/0.37/0.24/0.33**; **SACN 0.54/0.39/0.26/0.35**; **SACN+Attr 0.55/0.40/0.27/0.36**.
  - **WN18RR:** ConvE **0.48/0.43/0.39/0.46**; Conv-TransE **0.52/0.47/0.43/0.46**; **SACN 0.54/0.48/0.43/0.47**.
- **Hyperparameter defaults (Experimental Setup):** grid ranges—LR {0.01, 0.005, 0.003, 0.001}, dropout {0.0–0.5}, embedding {100,200,300}, kernels {50,100,200,300}, kernel size {2×1,2×3,2×5}; **WGCN uses 2 layers**. Good settings: dropout **0.2**, LR **0.003**, emb **200**; kernels **100** (FB15k-237) / **300** (WN18RR).
- **Kernel size effect (Table 4, FB15k-237):** SACN MRR improves **0.345 (2×1)** → **0.351 (2×3)** → **0.352 (2×5)**; SACN+Attr MRR **0.351** → **0.360** (2×3/2×5).

## When to surface
Use when students ask how GCN structure + convolutional decoders improve KG link prediction, or need concrete Hits@K/MRR comparisons (ConvE vs Conv-TransE vs SACN) and the exact WGCN/Conv-TransE equations.