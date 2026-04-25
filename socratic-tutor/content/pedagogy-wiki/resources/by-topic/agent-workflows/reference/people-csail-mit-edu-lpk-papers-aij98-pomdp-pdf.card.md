# Card: POMDP formalism—belief updates & value iteration
**Source:** https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Formal POMDP formulation with belief-state updates, value functions, and planning/acting loop assumptions (explicit equations and definitions).

## Key Content
- **MDP definition (Sec. 2.1):** tuple ⟨S, A, T, R⟩ with finite states/actions.  
  - Transition: \(T(s,a,s') = \Pr(s' \mid s,a)\)  
  - Reward: \(R(s,a)\) expected immediate reward.
- **Discounted return objective (Sec. 2.2):** maximize  
  \(\mathbb{E}\left[\sum_{t=0}^{\infty}\gamma^t r_t\right]\), with \(0<\gamma<1\).
- **MDP Bellman optimality equation (Sec. 2.2):**  
  **(Bellman\*)** \(V^*(s)=\max_a\left[R(s,a)+\gamma\sum_{s'\in S}T(s,a,s')V^*(s')\right]\).  
  Greedy policy: \(\pi_V(s)=\arg\max_a\left[R(s,a)+\gamma\sum_{s'}T(s,a,s')V(s')\right]\).
- **Value iteration algorithm (Alg. 1):** initialize \(V_1(s)=0\). Iterate  
  \(Q_t^a(s)=R(s,a)+\gamma\sum_{s'}T(s,a,s')V_{t-1}(s')\); \(V_t(s)=\max_a Q_t^a(s)\).  
  Stop when \(|V_t(s)-V_{t-1}(s)|<\varepsilon\ \forall s\). Error bound:  
  \(\max_s |V^{\pi_{V_t}}(s)-V^*(s)| < \frac{2\varepsilon\gamma}{1-\gamma}\).
- **POMDP definition (Sec. 3.1):** tuple ⟨S, A, T, R, Ω, O⟩ with observations Ω and observation model  
  \(O(s',a,o)=\Pr(o\mid s',a)\).
- **Belief state update (Sec. 3.3):** belief \(b(s)\) over S; after action a, obs o:  
  **(BeliefUpdate)** \(b'(s')=\eta\; O(s',a,o)\sum_{s\in S}T(s,a,s')\,b(s)\), where \(\eta\) normalizes.
- **Belief-MDP reward (Sec. 3.4):** \(\rho(b,a)=\sum_{s\in S} b(s)R(s,a)\).  
  Rationale: belief equals true occupation probabilities under correct model ⇒ \(\rho\) is true expected reward.
- **Piecewise-linear convex value over beliefs (Sec. 4.1):** for t-step policy trees p with vector \(\alpha_p=\langle V_p(s_1),...,V_p(s_n)\rangle\):  
  \(V_p(b)=b\cdot \alpha_p\); **(PWLC)** \(V_t(b)=\max_{p} b\cdot \alpha_p\).

## When to surface
Use when students ask how an agent should plan/act under partial observability (belief states), how to update beliefs from action+observation, or how value iteration/Bellman equations ground multi-step planning and replanning.