# Card: Markov Games (Multi-Agent RL) + Minimax-Q
**Source:** https://www.cs.cmu.edu/~./15281-f19/lectures/15281_Fa19_Lecture_26_MARL.pdf  
**Role:** explainer | **Need:** FORMULA_SOURCE  
**Anchor:** Formal Markov game definition; value/objectives; reduction from MDP to multi-agent; Minimax-Q update + LP.

## Key Content
- **Markov game definition (Slide 15)**:  
  - Agents: \(N\). States: \(S\) (joint configuration).  
  - Actions per agent: \(A_1,\dots,A_N\). Joint action \((a_1,\dots,a_N)\).  
  - Transition: \(T(s,a_1,\dots,a_N,s')\) = \(P(s' \mid s, a_1,\dots,a_N)\).  
  - Rewards: \(R_i(s,a_1,\dots,a_N)\) for each agent \(i\).
- **Policies + objective (Slide 17)**: stochastic policy \(\pi_i(s,a)=P(a\mid s)\). Agent \(i\) maximizes discounted return \(\sum_t \gamma^t r_t^i\) (discount \(\gamma\)).
- **Single-agent value iteration (Slide 20, Eq. SA-Bellman)**:  
  \(V_{k+1}(s)=\max_a \sum_{s'} P(s'|s,a)\big(R(s,a,s')+\gamma V_k(s')\big)\).  
  \(Q^*(s,a)=R(s,a)+\gamma\sum_{s'}P(s'|s,a)V^*(s')\), \(V^*(s)=\max_a Q^*(s,a)\).
- **Two-player zero-sum Markov game backup (Slides 21–22, Eq. MG-Bellman)**:  
  \(Q^*(s,a_1,a_2)=R(s,a_1,a_2)+\gamma\sum_{s'}P(s'|s,a_1,a_2)V^*(s')\).  
  \(V^*(s)=\max_{\pi_1\in\Delta(A_1)}\min_{a_2\in A_2}\sum_{a_1}\pi_1(s,a_1)\,Q^*(s,a_1,a_2)\).
- **Minimax-Q algorithm (Slides 24–27, Eq. MMQ-update)**:  
  \(Q(s,a_1,a_2)\leftarrow (1-\alpha)Q(s,a_1,a_2)+\alpha\big(r_1+\gamma V(s')\big)\).  
  \(V(s)\leftarrow \min_{a_2}\sum_{a_1}\pi_1(s,a_1)Q(s,a_1,a_2)\).  
  \(\pi_1(s,\cdot)\leftarrow \arg\max_{\pi_1'\in\Delta(A_1)} \min_{a_2}\sum_{a_1}\pi_1'(s,a_1)Q(s,a_1,a_2)\).  
  Action selection: \(\epsilon\)-greedy w.r.t. \(\pi_1\).
- **LP to compute \(\max\min\) policy (Slide 31, Eq. LP)**: maximize \(v\) s.t.  
  \(v \le \sum_{a_1}\pi_1'(s,a_1)Q(s,a_1,a_2)\ \forall a_2\); \(\sum_{a_1}\pi_1'(s,a_1)=1\); \(\pi_1'(s,a_1)\ge 0\).
- **Defaults/examples**: Matching pennies example uses \(\gamma=0.9\) (Slide 29); init \(Q\leftarrow 1\), \(V\leftarrow 1\), \(\pi_1\) uniform; step size example \(\alpha=1/\#\text{visits}(a_1,a_2)\) (Slide 31).  
- **Evaluation workflow (Slides 36–38)**: train \(\pi_1\) against (self-play / random / other learner), then **test** by fixing \(\pi_1\) and training/evaluating \(\pi_2\) including best response \(BR(\pi_1)\) via single-agent RL (treat fixed opponent as environment).

## When to surface
Use when students ask for the formal Markov game definition, Bellman-style equations in zero-sum Markov games, or the exact Minimax-Q update/LP used to compute the maximin policy and how MARL evaluation via best response is set up.