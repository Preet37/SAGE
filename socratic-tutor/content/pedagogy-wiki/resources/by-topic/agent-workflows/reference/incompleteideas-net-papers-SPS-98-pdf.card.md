# Card: Options Framework & Induced SMDP Equations
**Source:** http://incompleteideas.net/papers/SPS-98.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** Formal Options definition (⟨I, π, β⟩) + SMDP models/objectives/Bellman equations for temporally-extended actions

## Key Content
- **Option definition (Section 4):** An option is ⟨**I**, **π**, **β**⟩  
  - **Initiation set**: \(I \subseteq S\). Option available iff \(s\in I\).  
  - **Policy**: \( \pi: S\times A \to [0,1]\) (Markov) selects primitive actions while option runs.  
  - **Termination**: \( \beta: S^+ \to [0,1]\) gives probability option terminates upon arrival in state \(s\). Episodic terminal state has \(\beta(\text{terminal})=1\).
- **Primitive actions as options (Section 4):** action \(a\) corresponds to option with \(I=\{s: a\in A_s\}\), \(\beta(s)=1\ \forall s\), \(\pi(s,a)=1\).
- **SMDP “multi-time” option model (Section 5):** if option \(o\) initiated in \(s\) at time \(t\), terminates after random duration \(k\) in \(s_{t+k}\):  
  - Reward model (Eq. 5):  
    \[
    r^o_s = \mathbb{E}\left[r_{t+1}+\gamma r_{t+2}+\cdots+\gamma^{k-1}r_{t+k}\mid E(o,s,t)\right]
    \]
  - Discounted transition model (Eq. 6):  
    \[
    p^o_{ss'}=\sum_{j\ge1}\gamma^j \Pr(s_{t+k}=s',k=j\mid E(o,s,t))
    =\mathbb{E}\left[\gamma^k \mathbf{1}\{s_{t+k}=s'\}\mid E(o,s,t)\right]
    \]
- **Bellman equations over options (Section 5):** for Markov policy over options \(\mu(s,o)\):  
  - State value (Eq. 7): \(V^\mu(s)=\sum_{o\in O_s}\mu(s,o)\left[r^o_s+\sum_{s'}p^o_{ss'}V^\mu(s')\right]\)  
  - Option value (Eq. 8): \(Q^\mu(s,o)=r^o_s+\sum_{s'}p^o_{ss'}\sum_{o'\in O_{s'}}\mu(s',o')Q^\mu(s',o')\)
- **Optimality with restricted option set \(O\) (Eq. 9–11):**  
  \[
  V^*_O(s)=\max_{o\in O_s}\left[r^o_s+\sum_{s'}p^o_{ss'}V^*_O(s')\right]
  \]
  \[
  Q^*_O(s,o)=r^o_s+\sum_{s'}p^o_{ss'}\max_{o'\in O_{s'}}Q^*_O(s',o')
  \]
- **Key procedure (planning):** Synchronous Value Iteration with options (Eq. 12):  
  \(V_{k+1}(s)\leftarrow \max_{o\in O_s}\left[r^o_s+\sum_{s'\in S^+}p^o_{ss'}V_k(s')\right]\)

## When to surface
Use when students ask how to *formally define temporally-extended actions (options)*, how options induce an *SMDP*, or how to write *Bellman/value-iteration/Q-learning-style equations* for option-level planning/learning (e.g., supervisor choosing sub-agents/tools over variable durations).