# Card: Options → SMDP framing + regret (UCRL-SMDP)
**Source:** http://proceedings.mlr.press/v54/fruit17a/fruit17a-supp.pdf  
**Role:** paper | **Need:** [FORMULA_SOURCE]  
**Anchor:** Formal mapping from MDP+options to SMDP; average-reward objective; regret definition; optimistic exploration (UCRL) adapted to options/macro-actions.

## Key Content
- **Option definition (Sec. 2):** option \(o=\{I_o,\beta_o,\pi_o\}\) with initiation set \(I_o\subset S\), termination prob. \(\beta_o:S\to[0,1]\), intra-option policy \(\pi_o:S\to A\).
- **MDP + options induces SMDP (Prop. 1):** \(M_O=\{S_O,O,p_O,r_O,\tau_O\}\), where  
  \(S_O=(\cup_o I_o)\cup(\cup_o\{s:\beta_o(s)>0\})\).  
  Transition: \(p_O(s,o,s')=\sum_{k\ge1} \Pr(s_k=s'\mid s,\pi_o)\,\beta_o(s')\).  
  \(r_O(s,o,s')\): cumulative reward until termination at \(s'\).  
  \(\tau_O(s,o,s')\): holding time (# primitive steps) until termination.
- **Average reward in SMDP (Prop. 2, Eq. 1):** with \(N(t)=\sup\{n:\sum_{i=1}^n\tau_i\le t\}\),  
  \(\rho^\pi(s)=\limsup_{t\to\infty}\mathbb E_\pi[\sum_{i=1}^{N(t)} r_i/t\mid s_0=s]\) (and \(\liminf\)). Communicating ⇒ stationary deterministic \(\pi^*\) exists with constant gain \(\rho^*\).
- **Optimality equation (Eq. 2):**  
  \(u^*(s)=\max_a\{r(s,a)-\rho^*\tau(s,a)+\sum_{s'}p(s'|s,a)u^*(s')\}\).
- **Regret for temporally-extended actions (Def. 1, Eq. 3):** after \(n\) decision steps,  
  \(\Delta(M,A,s,n)=(\sum_{i=1}^n\tau_i)\rho^*(M)-\sum_{i=1}^n r_i\). (Reduces to MDP regret when \(\tau_i=1\).)
- **UCRL-SMDP procedure (Sec. 3, Fig. 1):** episodic optimism. Each episode \(k\): build confidence set \(M_k\) over \(\tilde r,\tilde\tau,\tilde p\); run **Extended Value Iteration (EVI)** to pick optimistic \(\tilde M_k\) and policy \(\tilde\pi_k\); execute until some \((s,a)\) sample count doubles.
- **Uniformization to equivalent MDP (Eq. 4, Prop. 3):** choose \(\tau<\tau_{\min}\).  
  \(r^{eq}(s,a)=r(s,a)/\tau(s,a)\);  
  \(p^{eq}(s'|s,a)=\frac{\tau}{\tau(s,a)}(p(s'|s,a)-\delta_{s,s'})+\delta_{s,s'}\).  
  Optimal gain preserved; bias rescales by \(\tau^{-1}\).
- **EVI update (Eq. 5) + stop (Eq. 6):**  
  \(u_{j+1}(s)=\max_a\{\tilde r_{j+1}(s,a)/\tilde\tau_{j+1}(s,a)+\frac{\tau}{\tilde\tau_{j+1}(s,a)}(\tilde p_{j+1}^\top u_j-u_j(s))\}+u_j(s)\).  
  Stop when \(\max_s\Delta u-\min_s\Delta u<\varepsilon\); greedy policy is \(\varepsilon\)-optimal (Lemma 1). Use \(\varepsilon=R_{\max}/\sqrt{i_k}\).
- **Options vs primitive actions (Lemma 2):** for \(T_n=\sum_{i=1}^n\tau_i\),  
  \(\Delta(M,A,T_n)=\Delta(M_O,A,n)+T_n(\rho^*(M)-\rho^*(M_O))\). Linear term = policy-class restriction from options.
- **Holding times distribution (Lemma 3):** option holding times are **sub-exponential** in general; **sub-Gaussian iff a.s. bounded** (e.g., no cycles).
- **Regret bound (Thm. 1):** w.p. \(\ge 1-\delta\),  
  \(\Delta=O\big((D\sqrt S + C(M,n,\delta))R_{\max}\sqrt{SA\,n\log(n/\delta)}\big)\), where \(D\) is SMDP diameter (Def. 2, Eq. 7).  
  Lower bound (Thm. 2): \(\mathbb E[\Delta]=\Omega((\sqrt D+\sqrt{T_{\max}})R_{\max}\sqrt{SA\,n})\).
- **Sufficient condition for options to help (Eq. 9, Sec. 5, bounded holding times):** roughly  
  \(\frac{D_O\sqrt S + T_{\max}}{D\sqrt S\,\tau_{\min}}\le 1\) (longer options can reduce regret if they don’t blow up diameter / don’t reduce optimal gain).

## When to surface
Use when students ask how “tool calls/macro-actions” fit RL formally, how temporally-extended actions change the agent loop (decision steps vs primitive steps), or how exploration–exploitation/regret changes with options.