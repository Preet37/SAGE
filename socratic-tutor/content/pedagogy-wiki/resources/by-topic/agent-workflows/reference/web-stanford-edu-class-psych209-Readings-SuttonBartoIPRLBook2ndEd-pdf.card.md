# Card: Core RL/MDP + Bellman + DP + Q-learning (Sutton & Barto 2e)
**Source:** https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** MDP formalism, Bellman equations, policy/value iteration, Q-learning, planning/model connections

## Key Content
- **MDP dynamics & policy notation (Ch. 3, “Summary of Notation”)**
  - States \(s\in\mathcal S\), actions \(a\in\mathcal A(s)\), reward \(r\in\mathcal R\), discount \(\gamma\).
  - Policy: deterministic \(\pi(s)\) or stochastic \(\pi(a\mid s)\).
  - Transition model: \(p(s',r\mid s,a)\).
- **Return (Ch. 3):** \(G_t=\sum_{k=0}^{\infty}\gamma^k R_{t+k+1}\).
- **Value functions (Ch. 3):**
  - \(v_\pi(s)=\mathbb E_\pi[G_t\mid S_t=s]\)
  - \(q_\pi(s,a)=\mathbb E_\pi[G_t\mid S_t=s,A_t=a]\)
  - Optimal: \(v_*(s)=\max_\pi v_\pi(s)\), \(q_*(s,a)=\max_\pi q_\pi(s,a)\).
- **TD(0) / “backup” update shown in tic-tac-toe example (Sec. 1.5):**  
  **Eq. 1:** \(V(s)\leftarrow V(s)+\alpha\,[V(s')-V(s)]\) (step-size \(\alpha>0\)); illustrates bootstrapping from successor state estimate.
- **Q-learning (Ch. 6.5):** off-policy TD control update  
  **Eq. 2:** \(Q(S_t,A_t)\leftarrow Q(S_t,A_t)+\alpha\,[R_{t+1}+\gamma\max_a Q(S_{t+1},a)-Q(S_t,A_t)]\).
- **Design rationale (Ch. 1.3):** reward defines immediate goal; **value** is long-run desirability; estimating values is central because action choice should maximize expected long-run return, not immediate reward.
- **Planning/model-based connection (Ch. 1.3, Ch. 8):** a model predicts next state/reward; planning = deciding by considering possible futures; integrates planning, acting, learning.

## When to surface
Use when students ask for the formal RL objective/notation (MDPs, returns), how Bellman-style “backups” work, or how planning/model-based control relates to value/Q updates (e.g., receding-horizon vs learned value).