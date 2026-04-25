# Card: Process-based Self-Rewarding (Stepwise Self-Judging + DPO)
**Source:** https://aclanthology.org/2025.findings-acl.930.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Procedure + equations for process-level (stepwise) self-rewarding/judging and iterative step-wise preference optimization.

## Key Content
- **Core pipeline (Fig. 1; §3.2–3.5):**
  1) Build **IFT** (step-by-step reasoning) by logically segmenting CoT solutions into steps (“Step n: …”) using GPT-o1; 28,889 NuminaMath samples.  
  2) Build **EFT** (step-wise LLM-as-a-Judge) via: train a **PRM** on PRM800k to label each step “+/-”; run **MCTS** on a policy model; pick best/worst step at same depth; GPT-o1 writes pairwise judgment + explanation; keep pairs consistent with PRM and consistent under swapped order (double-eval). Final EFT: 4,679 (train 4,167 / test 500).  
  3) Initialize **M1** by SFT on **EFT+IFT**.  
  4) Iteratively generate step-wise preference pairs with the model as judge, then train with **step-wise DPO** to get M2…Mn.
- **Step candidate scoring (Eq. 1–5; §3.3):** For step index \(l\), sample width \(w\) candidates  
  \(S_l=\{s_{l,1},...,s_{l,w}\}\) (Eq.1).  
  Pairwise win indicator \(O(s_{l,i},s_{l,j}\mid x,s_{1:l-1})\in\{0,1\}\).  
  \(Score_{l,i}=\sum_{j\neq i} O(s_{l,i},s_{l,j}\mid x,s_{1:l-1})\) (Eq.2).  
  Choose \(s^{best}_l=\arg\max Score_l\), \(s^{worst}_l=\arg\min Score_l\) (Eq.3–4); set next step \(s_l=s^{best}_l\) (Eq.5). If \(\max=\min\), **rollback** one step and discard that pair.
- **Step-wise DPO loss (Eq. 6–8; §3.4):**  
  \(A=\beta\log\frac{\pi_\theta(s^b_l\mid x,s_{1:l-1})}{\pi_{ref}(s^b_l\mid x,s_{1:l-1})}\),  
  \(B=\beta\log\frac{\pi_\theta(s^w_l\mid x,s_{1:l-1})}{\pi_{ref}(s^w_l\mid x,s_{1:l-1})}\).  
  \(L(\pi_\theta;\pi_{ref})=-\mathbb{E}_{D}\left[\log\sigma(A-B)\right]\).
- **Design rationale:** Step-wise **pairwise comparison** is more consistent than scoring whole solutions (Table 6: consistency 0.84 vs 0.72; agreement 0.88 vs 0.32). Fine-grained step rewards help long-chain math reasoning.
- **Key empirical results (Table 1–2):**  
  72B PSRLM improves avg to **60.6** at M4 (vs base 48.6). From M1→M4 (Table 2): **+10.0 AIME2024**, **+12.5 AMC2023**.  
  7B PSRLM M4 avg **55.7** (vs base 36.1); M1→M4 gains include **+10.0 AMC2023**, **+6.6 AIME2024**.
- **Defaults/params (§4):** generation temp 0.5, top_p 0.95; search width \(w=6\); max step iterations 20. PRM/MCTS prefilter: simulation_depth 3, num_iterations 100, temp 0.7, top_p 0.95. Step-wise DPO: 1 epoch, lr 5e-7, batch 32; M2/M3/M4 use 400/800/1200 questions for preference generation.

## When to surface
Use when a student asks how to do **process-level self-improvement** (stepwise judging/rewarding) vs outcome-only, or wants the **exact equations** for step selection and **step-wise DPO** plus concrete hyperparameters/results.