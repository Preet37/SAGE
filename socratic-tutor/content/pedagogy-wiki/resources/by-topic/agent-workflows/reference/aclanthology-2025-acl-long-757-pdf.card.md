# Card: MasRouter (MAS Routing: topology + roles + LLMs)
**Source:** https://aclanthology.org/2025.acl-long.757.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** Routing policy formulation + training objective/procedure + benchmark cost/quality tradeoffs

## Key Content
- **MAS search space & instance (Eq. 1, Sec. 3.1):** Search space \(S=(\mathcal M,\mathcal R,\mathcal T)\) with LLM pool \(\mathcal M\) (size \(N_m\)), role set \(\mathcal R\) (size \(N_r\)), collaboration modes \(\mathcal T\) (size \(N_t\)). A MAS instance  
  \[
  \mathbf S=\{\{M_i\}_{i=1}^k,\{R_i\}_{i=1}^k,T\},\; M_i\in\mathcal M,\; R_i\in\mathcal R,\; T\in\mathcal T
  \]
- **MASR definition (Eq. 2):** Router defines \( \pi(\mathbf S)=P(\mathbf S\mid Q)\) mapping query \(Q\) to a tailored MAS.
- **Cost–utility objective (Eq. 3):**  
  \[
  \max_{P(\mathbf S|Q)}\; \mathbb E_{(Q,a)\sim D,\;\mathbf S\sim P(\mathbf S|Q)}\big[U(\mathbf S;Q,a)-\lambda\,C(\mathbf S;Q)\big]
  \]
  \(U\)=performance vs oracle \(a\); \(C\)=expected cost (tokens/API calls); \(\lambda\)=tradeoff.
- **Cascaded controller (Eq. 5):** \(F_\theta = F_{\theta m}\circ F_{\theta r}\circ F_{\theta t}\): collaboration determiner \(F_{\theta t}:Q\to T\); role allocator \(F_{\theta r}:(Q,T)\to \{R_i\}\); LLM router \(F_{\theta m}:(Q,T,\{R_i\})\to \{M_i\}\).
- **Collaboration determiner (Eq. 6–7):** variational latent \(H\): \(F_{\theta t}(T|Q)=\int p_g(T|H)p_h(H|Q)dH\), with \(p_h(H|Q)=\mathcal N(\mu_t(Q),\mathrm{diag}(\sigma_t^2(Q)))\); softmax via temperature \(\tau\).
- **Dynamic agent count (Sec. 4.1):** \(k=\lceil \delta(H)\cdot \gamma\rceil\), \(\delta:[0,1]\), \(\gamma\)=max agents.
- **Role cascade (Eq. 8–9):** sequential role sampling \(\prod_{\ell=1}^k \pi^r_\ell(R_\ell|Q,T,R_{<\ell})\) with softmax temperature \(\tau\).
- **LLM routing multinomial (Eq. 10–12):** assigns \(k\) agents across \(N_m\) LLMs; multinomial coefficient approximated with Gamma to keep gradients: \(\Gamma(\delta(H)\gamma+1)/\prod_i\Gamma(n_i+1)\).
- **Training (Eq. 13, Sec. 4.4):** minimize \(\mathbb E[-p(a|Q)+\lambda C(\mathbf S;Q)]\); optimized with **policy gradient** (Williams, 1992).
- **Empirical headline (Table 1):** MasRouter best avg **85.93** vs RouterDC **82.42** (+3.51). On **MBPP**: MasRouter **84.00** vs AFlow **82.20** (+1.80) and AgentPrune **75.40** (+8.60). On **HumanEval**: MasRouter **90.62** vs RouterDC **87.75** (+2.87).
- **Cost results:** overhead on HumanEval reduced **$0.363 → $0.185** (intro). Plug-in (Table 2): MacNet HumanEval cost **$0.488 → $0.404** with +MasRouter, performance **86.82 → 88.37**; MAD HumanEval cost **$1.248 → $1.096**, performance **86.05 → 87.60**.
- **Defaults (Sec. 5.1):** learning rate \(\alpha=0.01\); temperature \(\tau=1\); \(\lambda\in\{5,15,25\}\); iterations \(K\in\{5,10\}\); max agents \(\gamma=6\). LLM pool: gpt-4o-mini-0718, claude-3.5-haiku, gemini-1.5-flash, llama-3.1-70b; temp=1.

## When to surface
Use when students ask how a supervisor/router should choose **(a)** collaboration topology, **(b)** agent roles/count, and **(c)** which LLM per agent under a **quality–cost** objective, or when comparing routing strategies with concrete benchmark numbers.