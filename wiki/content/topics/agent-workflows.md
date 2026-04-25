---
title: "Agent Workflows"
subject: "Agents & Reasoning"
date: 2026-04-09
tags:
  - "subject/agents-and-reasoning"
  - "level/intermediate"
  - "level/advanced"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  []
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Agent Workflows

## Video (best)
- **LangChain** — "LangGraph: Build Stateful, Multi-Agent Workflows"
- **Link:** [https://blog.langchain.dev/langgraph-multi-agent-workflows](https://blog.langchain.dev/langgraph-multi-agent-workflows)
- Why: LangGraph is one of the clearest, widely-used introductions to DAG/state-machine style orchestration for agents (nodes, edges, conditional routing, retries).
- Level: intermediate

## Blog / Written explainer (best)
- **Lilian Weng (OpenAI)** — "LLM Powered Autonomous Agents"
- **Link:** [https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Why: High-signal overview of agent building blocks and patterns (planning, tool use, memory) that underpin real workflows; good conceptual grounding before orchestration/production details.
- Level: intermediate

## Deep dive
- **LangChain Docs** — "LangGraph"
- **Link:** [https://langchain-ai.github.io/langgraph/](https://langchain-ai.github.io/langgraph/)
- Why: Practical deep dive into orchestration patterns: DAG-like graphs, conditional branching, cycles, persistence/checkpointing, streaming, and human-in-the-loop patterns.
- Level: intermediate/advanced
- **Microsoft** — "AutoGen"
- **Link:** [https://microsoft.github.io/autogen/stable/index.html](https://microsoft.github.io/autogen/stable/index.html)
- Why: Multi-agent conversation/workflow patterns, tool execution, and coordination; useful for parallel/role-based agent workflows and production-ish patterns.
- Level: intermediate/advanced

## Original paper
- **ReAct** — "ReAct: Synergizing Reasoning and Acting in Language Models"
- **Link:** [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)
- Why: Foundational pattern for tool-using agent loops (reason → act → observe), which is the core of many sequential chains and orchestration designs.
- Level: intermediate
- **MRKL** — "MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning"
- **Link:** [https://arxiv.org/abs/2205.00445](https://arxiv.org/abs/2205.00445)
- Why: Early, influential framing for routing/orchestrating between tools and modules (a precursor to many workflow-engine patterns).
- Level: intermediate

## Code walkthrough
- **LangChain (GitHub)** — "LangGraph" (examples)
- **Link:** [https://github.com/langchain-ai/langgraph](https://github.com/langchain-ai/langgraph)
- Why: Concrete reference implementations for graph/DAG orchestration, streaming, retries, and human-in-the-loop checkpoints.
- Level: intermediate
- **Microsoft (GitHub)** — "AutoGen" (examples)
- **Link:** [https://github.com/microsoft/autogen](https://github.com/microsoft/autogen)
- Why: End-to-end multi-agent workflow examples (coordinator/worker patterns, tool calls, conversation-driven orchestration).
- Level: intermediate

## Coverage notes
- Strong: orchestration-patterns (DAG/graph orchestration, sequential chains, conditional routing), workflow engines (LangGraph), multi-agent coordination (AutoGen), core agent loop pattern (ReAct).
- Weak: production-patterns specifics (agent-as-API design, robust retry/fallback taxonomies, streaming UX patterns) in a single canonical explainer; agent-deployment details are scattered across vendor docs.
- Gap: agent tracing/observability and deployment SRE guidance (latency management, cost optimization) in one stable, vendor-neutral “best” resource; likely needs a dedicated page or curated set of vendor/OSS observability docs.

---

## Additional Resources for Tutor Depth

> **31 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Core RL/MDP + Bellman + DP + Q-learning (Sutton & Barto 2e)
**Paper** · [source](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)

*MDP formalism, Bellman equations, policy/value iteration, Q-learning, planning/model connections*

<details>
<summary>Key content</summary>

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

</details>

### 📄 ESAA — Event-Sourced Agent Orchestration (CQRS-style)
**Paper** · [source](https://arxiv.org/html/2602.23193v1)

*Architecture/procedure for representing agent execution as an event-sourced log with deterministic replay + hash-verified projections*

<details>
<summary>Key content</summary>

- **Core separation (Section 3):** LLM agent emits **structured intentions only** (e.g., `agent.result`, `issue.report`) in **validated JSON**; a **deterministic orchestrator** validates, persists, and applies effects (agent has **no direct write permission**).
- **Canonical artifacts (.roadmap/, Section 3.1):**
  - `activity.jsonl`: **append-only** ordered event log (`event_seq`).
  - `roadmap.json`: **materialized read-model** (projection) incl. `projection_hash_sha256`.
  - Contracts: `AGENT_CONTRACT.yaml`, `ORCHESTRATOR_CONTRACT.yaml` (allowed actions + prohibitions, e.g., deny agent `file.write`).
  - PARCER profiles (`PARCER_PROFILE.*.yaml`): metaprompting constraints (Persona/Audience/Rules/Context/Execution/Response) enforcing strict JSON envelope.
- **Trace-first + immutability (Section 3.2):** record event **before** irreversible effects; **“done immutability rule”**: completed tasks don’t regress—defects create new `issue.report` → new hotfix path.
- **Deterministic verification (Section 3.3, 4.2):**
  - Compute **SHA-256** over **canonicalized** projected state: `projection_hash_sha256 = SHA256(canonicalize(roadmap.json))` (canonicalization aligned with RFC 8785 JCS).
  - `esaa verify`: replay log → reproject → compare hash; emits `verify.ok` or `verify.fail`.
- **Orchestrator pipeline (Section 4.2):** validate (JSON Schema + boundary rules) → `output.rejected` if violation → apply effects via `orchestrator.file.write` → append events → reproject `roadmap.json` → verify via replay+hash.
- **Concurrency model (Section 3.4):** agents run in parallel, but results are **validated and appended sequentially**, preserving **total order**; orchestrator can detect conflicts (e.g., overlapping file mods) before applying.
- **Empirical results (Case studies, Tables 1–2):**
  - CS1 landing page: **9 tasks, 49 events**, `run.status=success`, `verify_status=ok`, `output.rejected=0`. Cycle: `attempt.create → orchestrator.dispatch → agent.result → orchestrator.file.write → task.update` (repeat) → `verify.ok → run.end`.
  - CS2 clinic-asr: **50 tasks, 86 events**, **4 concurrent agents**, **15 phases (8 completed)**; at analysis **31/50 tasks done (62%)**; distribution: **30 claims, 30 completions, 17 promotes, 8 phase.complete, 1 version init**; `output.rejected=0`; log size **~15 KB**; run duration **~15 hours**.
- **Overheads (Section 6.6):** JSON envelope + validation preamble **~200–500 tokens/invocation**; validation+persistence **sub-second/event**.

</details>

### 📄 GoalAct = continuously updated global plan + hierarchical execution
**Paper** · [source](https://arxiv.org/html/2504.16563v2)

*Taxonomy/positioning of agent architectures (ReAct vs Plan-and-Execute vs CodeAct) and how “global planning” changes decision flow*

<details>
<summary>Key content</summary>

- **Problem framing (Intro):**
  - **ReAct**: incremental “Thought–Action–Observation” w/o global perspective → can get stuck in **local branches/local optima** on multi-branch tasks.
  - **Plan-and-Execute**: makes a global plan then executes + adjusts via feedback, but plans often **non-executable** (exceed agent action space).
  - **Execution trade-off**: text/json tool calls are stable but limited (no loops/conditionals); code actions (CodeAct) are expressive but can be unstable in unpredictable tool environments; writing tasks not well-solved by code alone.
- **Global plan definition (Section 3.1):**
  - **Eq. (1):** global plan \(P=\{p_i\}_{i=1}^{n}\), where \(p_i\) is the *i-th plan step* and has corresponding action \(a_i\). Plan steps specify **high-level skills** (not low-level actions). Final step \(p_n\) is always **Finish**.
  - **Eq. (2):** at time \(t\), update plan \(P_t = \pi(u, T, H_t)\), where \(\pi\) is the update policy; \(u\)=user query; \(T\)=available tools; \(H_t\)=history.
  - **Eq. (3):** history \(H_t=\{(a_i,o_i)\}_{i=1}^{t-1}\), where \(o_i\)=observation from executing \(a_i\); \(H_1=\emptyset\).
  - Rationale: **tight coupling** of planning+execution via continuous plan updates → coherent long-term goals + executability.
- **Hierarchical execution (Section 3.2):** plan over **skills** (searching/coding/writing/…) then pick tools/params within skill.
  - Searching: simple/stable; limited expressiveness (no loops/branches).
  - Coding: python enables loops/branches; higher complexity → more error-prone with uncertain tool outputs.
  - Writing: needed for tasks like legal document generation; not solved by code/search alone.
- **Empirical results (LegalAgentBench, Table 2; temp=0):**
  - **GoalAct SOTA**; average success-rate improvement **+12.22%** over second-best (reported).
  - GPT-4o-mini **ALL**: GoalAct **0.7720** vs ReAct **0.6161**, CodeAct **0.6275**, Plan-and-Solve **0.4196**, Plan-and-Execute **0.4503**.
  - GLM-4-Plus **ALL**: GoalAct **0.8710** vs ReAct **0.7499**, CodeAct **0.6648**.
- **Ablation (Table 3, GLM-4-Plus):** removing global plan drops **ALL** from **0.8710 → 0.7896** (−8.14%).

</details>

### 📄 Latency-aware orchestration via critical path (LAMaS)
**Paper** · [source](https://arxiv.org/abs/2601.10560)

*Method: orchestration/search space (layered DAG/parallel), latency reward + critical-path credit assignment, and latency/cost tradeoffs + ablations.*

<details>
<summary>Key content</summary>

- **Parallel execution + critical path definition (Sec. 3.1–3.3):** Operators are atomic nodes (each may include multiple LLM/tool calls). Operators are selected **per layer** and run **in parallel within a layer** after removing intra-layer dependencies (refinement ops consume **previous-layer** outputs to avoid synchronization barriers).
- **Latency vs cost under parallelism:**
  - **Latency (critical path), Eq. (1):** \(L=\sum_{l\in \mathcal{L}} \max_{o\in \mathcal{O}_l} t(o)\), where \(\mathcal{O}_l\) are operators executed at layer \(l\), \(t(o)\) is operator time.
  - **Cost, Eq. (2):** \(C=\sum_{l\in \mathcal{L}}\sum_{o\in \mathcal{O}_l} c(o)\) (token/$ cost adds across all operators).
- **Controller/search space (Sec. 3.4):** Probabilistic **agentic supernet DAG**; controller samples operators **layer-by-layer** with autoregressive factorization (Eq. 3). **Threshold-based sampling** (Eq. 4): select highest-scoring operators until cumulative confidence exceeds threshold \(\tau\) (controls width/parallelism). **EarlyExit** ends generation immediately if selected.
- **Reward + credit assignment:**
  - **Global reward, Eq. (5):** \(R = S - \lambda_c C - \lambda_l \hat{L}\) (task score \(S\), cost \(C\), latency proxy \(\hat{L}\)).
  - **Critical operator per layer, Eq. (6):** \(o_l^*=\arg\max_{o\in \mathcal{O}_l}\hat{t}(o)\).
  - **CP-aware operator rewards, Eq. (7):** apply latency penalty **only** to \(o_l^*\) to avoid credit assignment error.
  - **Training, Eq. (8):** policy gradient on sampled trajectories; reward normalization via EMA mean/variance.
- **Latency proxy for evaluation/optimization (Eq. 9):** CP length \(=\sum_l \max_{o\in \mathcal{O}_l}(\text{output tokens}(o)+\alpha\cdot \text{tool seconds}(o))\); \(\alpha=50\) (1s tool time = 50 “virtual tokens”).
- **Key results (Tables 2–4):** vs MaAS (same space, parallel enabled):
  - **GSM8K:** Score 93.37 vs 93.13; **CP len 913.5 vs 1474.6 (−38.0%)**
  - **HumanEval:** 92.11 vs 93.00; **CP len 1042.7 vs 1810.8 (−42.4%)**
  - **MATH:** 52.26 vs 51.23; **CP len 1195.8 vs 2218.5 (−46.1%)**
  - Cost/CP examples (Table 3): GSM8K LAMaS cost **0.88** vs MaAS **0.56**; HumanEval LAMaS **0.10** vs MaAS **0.08**; MATH LAMaS **0.99** vs MaAS **0.37**.
- **Ablations (Table 4):**
  - **w/o latency weight (but parallel deps removed):** GSM8K CP **1215.9** (vs 913.5) and cost **1.73** (vs 0.88); HumanEval CP **1629.3** (vs 1042.7); MATH score **48.97** (vs 52.26) and CP **1342.1** (vs 1195.8).
  - **w/o CP credit (HumanEval):** score **91.60**, cost **0.12**, CP **1197.5** (worse than LAMaS 1042.7).
- **Defaults/hyperparams (Sec. 4.1):** LLM **gpt-4o-mini-0718**, temperature **1**; supernet layers \(L=4\); cost penalty \(\lambda_c=0.1\); sampling times \(N=5\); threshold \(\tau=0.8\); latency weight \(\lambda_l=0.5\) (normalized by factor **50** in objective); tool scaling \(\alpha=50\).

</details>

### 📄 MasRouter (MAS Routing: topology + roles + LLMs)
**Paper** · [source](https://aclanthology.org/2025.acl-long.757.pdf)

*Routing policy formulation + training objective/procedure + benchmark cost/quality tradeoffs*

<details>
<summary>Key content</summary>

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

</details>

### 📄 Options Framework & Induced SMDP Equations
**Paper** · [source](http://incompleteideas.net/papers/SPS-98.pdf)

*Formal Options definition (⟨I, π, β⟩) + SMDP models/objectives/Bellman equations for temporally-extended actions*

<details>
<summary>Key content</summary>

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

</details>

### 📄 POMDP formalism—belief updates & value iteration
**Paper** · [source](https://people.csail.mit.edu/lpk/papers/aij98-pomdp.pdf)

*Formal POMDP formulation with belief-state updates, value functions, and planning/acting loop assumptions (explicit equations and definitions).*

<details>
<summary>Key content</summary>

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

</details>

### 📄 SPAgent — Speculation to Reduce Search-Agent Latency
**Paper** · [source](https://arxiv.org/html/2511.20048v1)

*End-to-end latency benchmarks for a ReAct-style search agent using speculation + scheduling (not just microbenchmarks)*

<details>
<summary>Key content</summary>

- **Problem:** ReAct “Reason→Action” is strictly serial: full LLM reasoning must finish before tool execution; both inference and tool time are substantial contributors to wall-clock latency (Sec. I, II-A).
- **Key observation:** Directly sampled speculative actions (no reasoning tokens) match the post-reasoning action **73.4% at step 1**, but can drop to **~11% in later steps** (Fig. 1b, Sec. III-A).
- **Two-phase adaptive speculation (Sec. III):**
  - **Aggressive Speculation Phase:** skip reasoning; directly sample actions, execute via **Action Server**; reduces LLM inference time (Sec. III-B).
  - **Verified Speculation Phase:** run normal reasoning while **parallel** speculative action sampling+execution; reuse result if speculative action matches; else fallback to executing correct action (Sec. III-C).
  - **Phase transition:** self-reflection scoring of speculative actions on **1–5 scale**; switch when all scores < threshold **τ**. Accuracy saturates once **τ ≥ 3**; **τ=2 or 3** best latency/accuracy tradeoff (Fig. 4, Sec. III-D).
- **Action Server (Sec. III-E):** in-memory thread-safe dict “Action Buffer” mapping action→state/result; avoids redundant tool calls; footprint **~200 Bytes/task**.
- **Scheduling (Sec. IV):**
  - **Intra-speculation objective (Eq. 1):** maximize **expected overlap benefit − inference overhead** by selecting subset of main requests for speculation.
  - **Expected overlap benefit (Eq. 2):** with hit prob **p** and **k** speculative samples, benefit scales with **1 − (1−p)^k** times average tool time **t_act** (variables in Table I).
  - **Overheads:** decode overhead (Eq. 3) + prefill overhead (Eq. 4) using engine-profiled hybrid-batch times.
  - **Inter-request scheduling:** SJF-like “speculation-first” so short (<10 token) speculative jobs finish before long reasoning jobs (Sec. IV-B).
- **Empirical results (Sec. V):**
  - Tool latency: Wikipedia API **~1.5 s/request** (Setup).
  - **Single-request:** SPAgent reduces **LLM time 23.8%** and **un-overlapped action exec 29.4%** on average vs naive; “Speculative Actions” can **increase inference latency up to 26%** (Sec. V-B, Fig. 7).
  - **Serving:** SPAgent achieves **24.2% mean latency reduction on avg, up to 69.6%** vs naive & Speculative Actions; Speculative Actions becomes **up to 49.3% slower than naive** when load > **2 rps** (Fig. 8).
  - **Accuracy:** generally on par; **Qwen2.5-32B TriviaQA +>5%** accuracy gain (Table II).
  - **Action Buffer hit rate:** typically **~40%** in single-request (Fig. 9a). Default speculative samples **k=4** (diminishing returns beyond) (Fig. 9b).

</details>

### 📄 Speculative Actions (predict–verify for faster agents)
**Paper** · [source](https://arxiv.org/html/2510.04371v1)

*Procedure/algorithm for speculative tool/action execution (predict-verify) + measured latency reductions & trade-offs*

<details>
<summary>Key content</summary>

- **Core idea (Section 2):** Treat each agent step as an **API call** with non-trivial latency. Break strict sequentiality by running **Speculator(s)** (fast, cheap) in parallel with **Actor(s)** (slow, authoritative). Speculator predicts next action (API + params) and often predicted observation/state delta; Actor validates and commits.
- **Algorithm 1 (cache + async futures):**
  - Maintain cache mapping **API call specifier → pending future response**.
  - While waiting for true response at step *t*, Speculator predicts likely next call(s) for step *t+1* and **pre-launches** them asynchronously.
  - At time of issuing the real next call: if cache hit, **skip invocation** and only `await` the already-running future; else call normally.
  - **Lossless via:** (a) semantic guards (Actor confirms equivalence before commit), (b) safety envelope (only idempotent/reversible/sandboxed side effects), (c) repair paths (rollback/compensating actions).
- **Assumptions (Section 2):**
  1) Speculation accuracy: implied next call matches true next call with probability **p > 0**.  
  2) Concurrent + reversible pre-launch: wrong-branch calls have no external side effects or can be rolled back.
- **Proposition 1 (expected runtime ratio):** Let **L** = mean latency of actual API call, **l** = mean latency of speculative model (with **l < L**), **p** = per-step probability speculative branch implies correct next call (independent). Then expected runtime ratio  
  \[
  \frac{\mathbb{E}[T_{\text{spec}}]}{\mathbb{E}[T_{\text{seq}}]}=\frac{1}{2-p}\left(1+\frac{l}{L}\right)
  \]
  (Appendix A). Implies **≤50%** ideal latency reduction when **l→0** and **p→1**; multi-step speculation can exceed this bound.
- **Empirical results (Abstract + Section 3/4):**
  - Next-action prediction accuracy **up to 55%**; **up to 20% end-to-end lossless speedup** (Abstract).
  - **E-commerce (-bench retail):** **22%–38%** API-call prediction accuracy; low-budget speculators run **2–3s**, below ~**30s** user typing time; multi-model speculation improves accuracy; ~**34%** accuracy at typing-time threshold (Appendix B.2).
  - **HotpotQA (Wikipedia multi-hop):** top-3 strict-match next-call accuracy **up to 55%**; top-3 >> top-1 (Section 3.3).
  - **OS tuning (lossy extension, last-write-wins):** p95 latency (ms): **Untuned 102.97**, **Actor-only 54.00**, **Actor+Spec 37.93** (Section 4.2). Convergence: **10–15s** (Actor+Spec) vs **~200s** (Actor-only); Spec-only stuck at **0.55ms → 36.24ms**, while Actor+Spec reaches **0.2ms → 30.26ms** (Section 4.2). Tuned parameter: Linux CFS **min_granularity_ns** range **50,000–50,000,000 ns**; default **3ms** (Appendix B.3.1).
- **Cost/latency trade-off:** More speculative calls (larger top-*k*, wider beams) ↑ accuracy but ↑ token/API cost; self-hosted LLMs can mitigate via batching (Section 2, Appendix B.1/B.3.3).

</details>

### 📊 ALFWorld task suite + success metrics (planning benchmark)
**Benchmark** · [source](https://ar5iv.labs.arxiv.org/html/2010.03768)

*Task suite definition + standardized success metrics for long-horizon interactive tasks (ALFWorld), enabling numeric comparisons of planning/decomposition methods*

<details>
<summary>Key content</summary>

- **ALFWorld setup (Section 2):** Parallel aligned environments: **TextWorld** (high-level text actions) + **ALFRED/THOR** embodied simulator (low-level robot primitives). Uses **PDDL** latent state to generate equivalent TextWorld games from ALFRED scenes.
- **Task types + dataset sizes (Table 1):** Pick&Place (train 790 / seen 35 / unseen 24), Examine in Light (308/13/18), Clean&Place (650/27/31), Heat&Place (459/16/23), Cool&Place (533/25/21), Pick Two&Place (813/24/17). **All:** train **3,553**, seen **140**, unseen **134**.
- **Embodied action primitives:** MoveAhead, RotateLeft/Right, LookUp/Down, Pickup, Put, Open, Close, ToggleOn/Off.  
  **TextWorld high-level actions:** `goto {recep}`, `take {obj} from {recep}`, `put {obj} in/on {recep}`, `open/close {recep}`, `toggle {obj}{recep}`, `clean/heat/cool {obj} with {recep}`.
- **Splits definition:** **Seen** = rooms seen in training but new object placements/appearances; **Unseen** = **unseen rooms** with different layouts/receptacles (OOD generalization).
- **Success metrics (Section 4.1):** report **task success rate** and **goal-condition success rate** (ALFRED metric for partial completion; e.g., “put a hot potato on countertop” has 3 goal-conditions: heat something; put potato on countertop; heat potato + put on countertop).
- **Key embodied results (Table 2, All Tasks):** Seq2Seq **6% (15)** seen / **5% (14)** unseen; **BUTLER 19% (31)** seen / **10% (20)** unseen; **BUTLER-Oracle 37% (46)** seen / **26% (37)** unseen. Parentheses = goal-condition success.
- **Training pipeline defaults (Appendix B):** DAgger IL; **50K episodes** (text agents), max **50 steps/episode**, replay buffer **500K episodes**, batch collect **10**, update every **5** steps, sample **64**, LR **0.001**, grad clip **5**, expert assistance anneal **100%→1% over 50K** episodes. Beam-search recovery at eval: beam width **10**, try **top-5** candidates.

</details>

### 📊 Latency-aware parallel orchestration via critical path (LAMaS)
**Benchmark** · [source](https://arxiv.org/pdf/2601.10560.pdf)

*Experimental tables + equations showing latency (critical path) vs cost/accuracy for parallel DAG orchestration; ablations on latency reward + critical-path credit assignment.*

<details>
<summary>Key content</summary>

- **Parallel latency vs cost distinction (Section 3.3):**  
  - **Latency (critical path), Eq. 1:** \(L=\sum_{l\in \mathcal{L}} \max_{o\in \mathcal{O}_l} t(o)\)  
    - \(\mathcal{L}\): layers; \(\mathcal{O}_l\): operators executed in parallel at layer \(l\); \(t(o)\): operator time.  
  - **Cost, Eq. 2:** \(C=\sum_{l\in \mathcal{L}} \sum_{o\in \mathcal{O}_l} c(o)\) (token/$ cost accumulates additively).
- **Controller sampling (Eq. 4):** threshold-based subset selection per layer: pick highest-scoring operators until cumulative confidence exceeds threshold \(\tau\); EarlyExit ends generation.
- **Reward (Eq. 5):** global reward combines task score \(S\), cost penalty, and **latency proxy** penalty.  
- **Critical-path-aware credit assignment (Eq. 6–7):** identify per-layer critical operator \(o_l^\*\!=\arg\max_{o\in \mathcal{O}_l}\hat{t}(o)\); apply latency penalty **only** to bottleneck operators to avoid credit assignment error under parallelism.
- **Latency proxy metric (Eq. 9):** CP length (CP len) sums, per layer, the max of (output tokens + scaled tool time). Tool scaling: **1 sec = 50 virtual tokens**.
- **Key results vs MaAS (Table 2):**  
  - GSM8K: **93.37%** score, **CP 913.5** vs MaAS 93.13%, CP 1474.6 (**-38.0%**).  
  - HumanEval: **92.11%**, **CP 1042.7** vs 93.00%, CP 1810.8 (**-42.4%**).  
  - MATH: **52.26%**, **CP 1195.8** vs 51.23%, CP 2218.5 (**-46.1%**).
- **Fixed baselines tradeoffs (Table 3 examples):** GSM8K Generate CP 405.2 (92.80%, cost 0.31) vs LAMaS CP 913.5 (93.37%, cost 0.88); CoT*5+SC cost **1.96** with CP 488.3 (92.99%).
- **Ablations (Table 4):**  
  - **w/o latency weight:** GSM8K CP **1215.9** (vs 913.5) and cost **1.73** (vs 0.88). HumanEval CP **1629.3** (vs 1042.7).  
  - **w/o CP credit (HumanEval):** CP **1197.5** (vs 1042.7), score 91.60 (vs 92.11).
- **Defaults (Section 4.1):** LLM **gpt-4o-mini-0718**, temperature **1**; layers \(=5\); sampling times \(=5\); activation threshold \(\tau=0.8\); latency weight \(\lambda_L=0.5\) (normalized by 50); cost penalty \(\lambda_C=0.1\).

</details>

### 📊 VestaBench (safe long-horizon planning under adversarial constraints)
**Benchmark** · [source](https://aclanthology.org/2025.emnlp-industry.149.pdf)

*Benchmark construction + evaluation framework/metrics for multi-constraint long-horizon embodied planning with safety + adversarial instructions/environments*

<details>
<summary>Key content</summary>

- **Benchmark design (Section 2):**
  - Built from **VirtualHome** (Evolving Graph Simulator) and **BEHAVIOR-100** (via **Embodied Agent Interface** simulator with an action-transition layer).
  - Two datasets:
    - **VestaBench-VH:** **100 tasks** with safety constraints (physical, electrical, contamination, etc.). **70** tasks in **normal or adversarial environments**; **30** tasks with **adversarial instructions** the agent must avoid.
    - **VestaBench-B50:** **50 tasks** from BEHAVIOR-100 augmented with safety constraints; simulator provides **30 actions**.
  - Key claim: only benchmark (per Table 1) combining **multi-constraint tasks** + **adversarial instructions** + **adversarial environments**, with a **guarantee tasks are safely achievable**.
- **Problem definition (Section 3):**
  - Given instruction **t**, agent **A** outputs plan **P = (a₁,…,aₙ)** with actions **aᵢ ∈ 𝒜**, executed in simulator **S** → final environment graph **G\***.
  - Plan is **successful and safe** iff **predefined success + safety goals/criteria** are satisfied on **G\***.
- **Planning strategies (Section 3, Fig. 3):**
  - **One-go:** generate full multi-action plan once → execute → evaluate.
  - **Stepwise:** interact for **n steps** and **m trials**; each step executes **aᵢⱼ** → observation **oᵢⱼ** + state **Gᵢⱼ**; trajectory **τᵢ = {a₁₁,o₁₁,a₁₂,o₁₂,…}**. End of each trial: critic **J** gives feedback **fᵢ**; repeat until **Done** or trials exhausted.
- **Evaluation metrics (Section 4.1):** report **delivery rate**, **success rate**, **safety rate**.
- **Empirical findings (Section 4.2–4.3):**
  - **Direct one-go** is weakest; **direct stepwise** improves but remains low.
  - **ReAct** improves macro/micro **success & safety** on **VestaBench-VH** by ~**5%** and ~**10%** respectively; minimal gains on **B50**.
  - **ReAct+Critic > ReAct+Reflexion** (attributed to stronger critic model).
  - Complexity hurts safety: for **ReAct+Critic (1)** on **VestaBench-VH**, safety **66.67% (low)**, **48.64% (medium)**, **33.33% (high)**.
  - Adversarial instructions: agents often generate unsafe plans; struggle to distinguish malicious from safe instructions.
- **Defaults/models (Section 4.1):** planning agents include **GPT-4.1-Mini** and **Qwen3-32B**; in **ReAct+Critic (1)**, **GPT-4.1** used as critic.

</details>

### 📖 Dagster job execution + per-run concurrency controls
**Reference Doc** · [source](https://docs.dagster.io/guides/build/jobs/job-execution)

*Run executor configuration knobs (e.g., `max_concurrent`, `tag_concurrency_limits`) and how steps are scheduled within a run*

<details>
<summary>Key content</summary>

- **Default execution behavior**
  - By default, Dagster runs jobs with **`multiprocess_executor`**: each step runs in its **own process**, and **independent steps can run in parallel**.
- **Execution entry points (procedures)**
  - **UI:** Launchpad → **Launch Run**; includes config editor for runtime config.
  - **CLI:** `dg launch --jobs my_job` (launches asynchronously via the instance run launcher).
  - **Python:** `JobDefinition.execute_in_process()` returns `ExecuteInProcessResult`.
- **Executor configuration (per-run)**
  - Each `JobDefinition` has an `executor_def` (an `ExecutorDefinition`) controlling isolation/parallelism (in-process ↔ multiprocess ↔ k8s pods, etc.).
  - **Toggle to in-process via run config YAML:**
    ```yaml
    execution:
      config:
        in_process:
    ```
- **Multiprocess knobs (defaults/parameters)**
  - `max_concurrent`: limits **max concurrent subprocesses** within a run.
    - Example sets **`max_concurrent: 4`**.
  - `start_method`: controls subprocess spawn method; example uses **`forkserver`** to reduce per-process overhead.
- **Op-level concurrency limits (per-run)**
  - `tag_concurrency_limits`: caps concurrent ops matching a **tag key** or **key-value**; if launching an op would exceed a limit, it **stays queued**.
  - Example: overall **`max_concurrent: 4`**, plus at most **2** ops with tag `database=redshift`:
    ```yaml
    tag_concurrency_limits:
      - key: database
        value: redshift
        limit: 2
    ```
  - Applies **per-run only**; cross-run limits via `celery_executor` / `celery_k8s_job_executor`.

</details>

### 📖 Dagster op retry policies (RetryPolicy & RetryRequested)
**Reference Doc** · [source](https://docs.dagster.io/guides/build/ops/op-retries)

*Dagster op retry policy configuration (max_retries, delay/backoff/jitter) and retry behavior at the op boundary during job execution*

<details>
<summary>Key content</summary>

- **Core behavior (Overview):** When an exception occurs during **op execution**, Dagster can **retry that op within the same job run** (retry happens at the **op boundary**, not by rerunning the whole job).
- **Two mechanisms (Relevant APIs / Using op retries):**
  - **Declarative:** attach `dagster.RetryPolicy` to an op (or job / invocation) so retries are requested automatically on exception.
  - **Manual:** raise `dagster.RetryRequested` from inside the op body to conditionally request a retry.
- **RetryPolicy parameters (Section “RetryPolicy”):**
  - `max_retries` = maximum retry attempts (example: `max_retries=3`)
  - `delay` = base delay between retries in seconds (example: `delay=0.2` → 200ms)
  - `backoff` modifies delay by attempt number (example enum: `Backoff.EXPONENTIAL`)
  - `jitter` adds randomness to delay (example enum: `Jitter.PLUS_MINUS`)
  - **Delay formula (Eq. 1, conceptual):** `wait_time(attempt) = f(delay, backoff, jitter, attempt_number)` where `backoff` scales with attempt and `jitter` perturbs the result.
- **Where to set policy (Section “RetryPolicy”):**
  1. On op definition: `@op(retry_policy=RetryPolicy(...))`
  2. On a specific invocation: `problematic.with_retry_policy(flakey_op_policy)()`
  3. On a job for all contained ops: `@job(op_retry_policy=default_policy)`
  - Example job-level defaults/overrides: `default_policy = RetryPolicy(max_retries=1)`, override op with `RetryPolicy(max_retries=10)`.
- **RetryRequested usage (Section “RetryRequested”):**
  - Pattern: `try/except` → `if should_retry(e): raise RetryRequested(max_retries=1, seconds_to_wait=1) from e`
  - `raise ... from e` preserves original exception info in Dagster.
- **Applies to asset jobs too:** `define_asset_job(..., op_retry_policy=RetryPolicy(max_retries=3))`.

</details>

### 📖 Dagster+ run-level retries (full deployment settings)
**Reference Doc** · [source](https://docs.dagster.io/deployment/dagster-plus/deploying-code/full-deployments/full-deployment-settings-reference)

*Run-level retry configuration in Dagster+ deployment settings; boundary vs op/asset-level retries*

<details>
<summary>Key content</summary>

- **Where configured:** Full deployment settings are **YAML**. Run retries live under `run_retries:` (Section “Run retries”).
- **Core parameter (Eq. 1 — Run retry cap):**  
  `max_run_retry_attempts = run_retries.max_retries`  
  - **Definition:** Maximum number of times Dagster+ will attempt to retry a **failed run**.  
  - **Default:** `0` (no run retries).  
  - **Behavior:** If `run_retries.max_retries` is **undefined**, Dagster+ uses its default.
- **Failure-scope toggle (boundary vs op/asset retries):** `run_retries.retry_on_asset_or_op_failure`  
  - **Meaning:** Whether to retry runs that failed because **assets or ops** in the run failed.  
  - **Rationale:** Set to `false` to **only** retry failures due to the **run worker crashing/unexpectedly terminating**, and rely on **op/asset-level retry policies** for op/asset failures (explicit separation of concerns: run-level vs op/asset-level).  
  - **Version gate:** Setting this to `false` changes behavior only on **Dagster version ≥ 1.6.7**.
- **Example snippet:**  
  ```yaml
  run_retries:
    max_retries: 0
  ```
- **Related operational defaults (often confused with retries):** `run_monitoring.start_timeout_seconds: 1200`, `cancel_timeout_seconds: 1200`, `max_runtime_seconds: 7200` (timeouts affect run state transitions, not retry count).

</details>

### 📖 LangGraph Persistence & Checkpoint Semantics
**Reference Doc** · [source](https://docs.langchain.com/oss/javascript/langgraph/persistence)

*Concrete checkpoint/persistence semantics (checkpointer configuration, what state is stored, resume/replay behavior) and canonical durable-execution pattern in LangGraph.*

<details>
<summary>Key content</summary>

- **Persistence model:** Compile a LangGraph with a **checkpointer** to save a **checkpoint (StateSnapshot)** at **every super-step** (a “tick” where all scheduled nodes run, potentially in parallel). Enables **HITL**, **memory**, **time travel**, **fault tolerance**.
- **Required config (threading):** Must pass `thread_id` in config to persist/resume:  
  **Config formula:** `config = { configurable: { thread_id: "<id>" } }`  
  Checkpointer uses `thread_id` as the **primary key**; without it, it cannot save state or resume after interrupts.
- **Checkpoint contents (StateSnapshot fields):**
  - `values`: state channel values at checkpoint
  - `next`: node names to execute next (`[]` means complete)
  - `config`: includes `thread_id`, `checkpoint_ns`, `checkpoint_id`
  - `metadata`: `source` ∈ {"input","loop","update"}, `writes` (node outputs), `step` (super-step counter)
  - `createdAt`, `parentConfig`, `tasks` (task id/name/error/interrupts; may include subgraph state)
- **Empirical checkpoint count example:** For sequential `START -> A -> B -> END`, invoking once yields **exactly 4 checkpoints**: (1) empty/START next, (2) input saved/nodeA next, (3) nodeA outputs/nodeB next, (4) nodeB outputs/complete. Reducers accumulate (e.g., `bar` becomes `['a','b']`).
- **Replay semantics:** Invoke with prior `checkpoint_id` to re-execute **after** that checkpoint; earlier nodes skipped. **LLM calls/API requests/interrupts are re-triggered** during replay.
- **Fault tolerance + pending writes:** If a node fails mid super-step, LangGraph stores **pending writes** from successful nodes; on resume you **don’t re-run** successful nodes.
- **Namespaces:** `checkpoint_ns=""` for root; subgraph checkpoints use `"node_name:uuid"`; nested join with `|`. Accessible via `config.configurable.checkpoint_ns`.
- **APIs:** `graph.getState(config)` (latest or specific `checkpoint_id`), `graph.getStateHistory(config)` (most recent first), `graph.updateState()` creates a **new** checkpoint; reducer channels **accumulate**.
- **Defaults/infra:** Agent Server / LangGraph API handle checkpointing (and stores) automatically. Checkpointer libs: `MemorySaver` (in-memory), `SqliteSaver`, `PostgresSaver`, `MongoDBSaver`, `RedisSaver`. Base interface methods: `.put`, `.putWrites`, `.getTuple`, `.list`.

</details>

### 📖 OpenAI Agents SDK (Python) — RunConfig & RunOptions
**Reference Doc** · [source](https://openai.github.io/openai-agents-python/ref/run_config/)

*Exact `RunConfig` fields + runtime hooks/tracing/session/handoff controls; `RunOptions` chaining + error handlers.*

<details>
<summary>Key content</summary>

- **RunConfig (dataclass): config for an entire agent run**
  - **Model selection**
    - `model: str | Model | None = None` — if set, **overrides every agent’s model**; `model_provider` must resolve string names.
    - `model_provider: ModelProvider = MultiProvider()` — default provider (docs: “Defaults to OpenAI”).
    - `model_settings: ModelSettings | None` — **non-null values override agent-specific** model settings.
  - **Handoffs**
    - `handoff_input_filter: HandoffInputFilter | None` — global filter for all handoffs; **per-handoff filter takes precedence**.
    - `nest_handoff_history` — **default disabled**; when `True`, wraps prior run history into **one assistant message** before handoff if no custom filter.
    - `handoff_history_mapper: HandoffHistoryMapper | None` — runs **only when** `nest_handoff_history=True`; maps normalized transcript → history passed to next agent. If `None`, runner collapses transcript into one assistant message.
  - **Guardrails**
    - `input_guardrails: list[InputGuardrail] | None` — run on **initial** run input.
    - `output_guardrails: list[OutputGuardrail] | None` — run on **final** run output.
  - **Tracing/telemetry knobs**
    - `tracing_disabled` — disables tracing entirely.
    - `tracing: TracingConfig | None`
    - `trace_include_sensitive_data` — if `False`, spans exist but **tool/LLM inputs/outputs omitted**.
    - `workflow_name`, `trace_id` (custom), `group_id` (link traces), `trace_metadata` (dict).
  - **Session/memory**
    - `session_input_callback: SessionInputCallback | None` — default: **append new input** to session history; custom callback can merge history+input.
    - `session_settings: SessionSettings | None` — non-null overrides session defaults (e.g., retrieval item count).
  - **Pre-model/tool hooks**
    - `call_model_input_filter(agent, context, ModelInputData) -> ModelInputData` — invoked **immediately before** model call; can edit instructions/items (e.g., token limits, add system prompt).
    - `tool_error_formatter(ToolErrorFormatterArgs) -> str | None` — format tool errors; `None` uses SDK default.
  - **Reasoning item IDs**
    - `reasoning_item_id_policy: None/"preserve"|"omit"` — preserve IDs or strip them from next-turn model input.

- **RunOptions (TypedDict): arguments for AgentRunner methods**
  - `previous_response_id`, `auto_previous_response_id` (auto chaining first turn), `conversation_id`
  - `error_handlers: RunErrorHandlers | None` keyed by error kind; currently supports **`max_turns`**.

</details>

### 📖 OpenAI Agents SDK (Python) — Session backends & persistence semantics
**Reference Doc** · [source](https://openai.github.io/openai-agents-python/sessions/)

*Concrete session backends + what’s stored, how runs resume, and how conversation state is represented.*

<details>
<summary>Key content</summary>

- **Core session semantics (client-side memory):**
  - **Before each run:** Runner fetches session history via `session.get_items(...)` and **prepends** it to the new turn input.
  - **After each run:** Runner **persists all new items** from the run (user input, assistant outputs, tool calls, etc.) into the session.
  - **Result:** Subsequent `Runner.run(..., session=...)` includes **full stored history** automatically (no manual `.to_input_list()`).
- **Mutual exclusivity (important constraint):** Sessions **cannot** be combined with `conversation_id`, `previous_response_id`, or `auto_previous_response_id` in the same run. Use sessions *or* OpenAI server-managed continuation mechanisms.
- **Resuming interrupted / HITL runs:** If a run pauses for approval, resume by calling `Runner.run(...)` again **with the same session** (or another instance pointing to the same backing store) so history continues consistently.
- **History merge control (procedure):** `RunConfig.session_input_callback(history, new_input) -> final_input`
  - Receives **copies** of `history` and `new_input` (safe to mutate).
  - Returned list controls model input **for that turn**, but SDK persists **only new-turn items** (filtering/reordering old history doesn’t re-save it).
  - Example policy: keep last **10** history items: `history[-10:] + new_input`.
- **Retrieval limiting (default/parameter):** `SessionSettings(limit=None)` retrieves **all** items (default). `limit=N` retrieves **most recent N** items; set per-run via `RunConfig(session_settings=SessionSettings(limit=50))`.
- **Built-in backends (comparison table):**
  - `SQLiteSession` (file-backed or in-memory), `AsyncSQLiteSession` (aiosqlite), `RedisSession`, `SQLAlchemySession`, `DaprSession` (supports TTL + consistency options), `OpenAIConversationsSession` (OpenAI Conversations API), wrappers: `OpenAIResponsesCompactionSession` (Responses API `responses.compact`), `EncryptedSession` (encryption + TTL), `AdvancedSQLiteSession` (branching/analytics).
- **Compaction specifics:** `OpenAIResponsesCompactionSession` can auto-compact after turns; **may block streaming** until compaction completes. Modes: `"previous_response_id"` (best when chaining response IDs), `"input"` (rebuild from session items), default `"auto"`; if `ModelSettings(store=False)`, `"auto"` falls back to input-based compaction. Do **not** wrap `OpenAIConversationsSession` with compaction wrapper.

</details>

### 📖 Responses API Streaming Event Types (Server-Sent Events / WS)
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/responses-streaming)

*Enumerated Responses streaming event types + payload shapes (delta vs done, lifecycle/termination, tool-call streaming)*

<details>
<summary>Key content</summary>

- **Response lifecycle status values (`ResponseStatus`):** `"queued"`, `"in_progress"`, `"completed"`, `"failed"`, `"cancelled"`, `"incomplete"`.
- **Top-level termination/lifecycle events (each includes `type`, `sequence_number`, and often `response`):**
  - `ResponseCreatedEvent` `{ response, sequence_number, type }`
  - `ResponseQueuedEvent` `{ response, sequence_number, type }`
  - `ResponseInProgressEvent` `{ response, sequence_number, type }`
  - `ResponseCompletedEvent` `{ response, sequence_number, type }`
  - `ResponseFailedEvent` `{ response, sequence_number, type }`
  - `ResponseIncompleteEvent` `{ response, sequence_number, type }`
  - `ResponseErrorEvent` `{ code, message, param, … }` (error during streaming)
- **Output structure events (robust client should handle item/content boundaries):**
  - `ResponseOutputItemAddedEvent` `{ item, output_index, sequence_number, type }`
  - `ResponseOutputItemDoneEvent` `{ item, output_index, sequence_number, type }`
  - `ResponseContentPartAddedEvent` / `ResponseContentPartDoneEvent` `{ content_index, item_id, output_index, … }`
- **Text streaming (delta → done):**
  - `ResponseTextDeltaEvent` `{ content_index, delta, item_id, output_index, … }`
  - `ResponseTextDoneEvent` `{ content_index, item_id, logprobs, … }`
- **Refusal streaming:** `ResponseRefusalDeltaEvent` / `ResponseRefusalDoneEvent` with `{ content_index, delta/refusal, item_id, output_index, … }`.
- **Audio streaming:** `ResponseAudioDeltaEvent` `{ delta, sequence_number, type }` and `ResponseAudioDoneEvent`; transcript equivalents `ResponseAudioTranscriptDeltaEvent` / `Done`.
- **Tool-call streaming patterns (all keyed by `item_id`, `output_index`, `sequence_number`):**
  - Function args: `ResponseFunctionCallArgumentsDeltaEvent` `{ delta, item_id, output_index, … }` → `…DoneEvent` `{ arguments, name, item_id, … }`
  - Code interpreter code: `…CallCodeDeltaEvent` → `…CallCodeDoneEvent` plus `…InProgress/Interpreting/Completed`
  - Web/file search: `…InProgress` → `…Searching` → `…Completed`
  - Image gen: `…InProgress/Generating` → `…PartialImage` → `…Completed`
  - MCP tool calls: args delta/done + in_progress/completed/failed; list-tools in_progress/completed/failed
- **Include-able extra fields (`ResponseIncludable`):** `"file_search_call.results"`, `"web_search_call.results"`, `"web_search_call.action.sources"`, `"code_interpreter_call.outputs"`, `"computer_call_output.output.image_url"`, `"message.input_image.image_url"`, `"message.output_text.logprobs"`, `"reasoning.encrypted_content"`.

</details>

### 📖 Responses API — tool calls, streaming events, execution controls
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/responses)

*Exact request/response schema for tool calls, streaming events, and fields controlling execution (tool_choice, parallel tool calls where supported, truncation/limits) that determine what a supervisor can delegate and how results are returned*

<details>
<summary>Key content</summary>

- **Core endpoints (Responses):**
  - Create: `POST /responses`
  - Get: `GET /responses/{response_id}`
  - Delete: `DELETE /responses/{response_id}`
  - Cancel: `POST /responses/{response_id}/cancel`
  - Compact: `POST /responses/compact`
  - List input items: `GET /responses/{response_id}/input_items`
  - Input token counts: `POST /responses/input_tokens`
- **Instruction hierarchy (input messages):** `EasyInputMessage {role, content, ...}` where **developer/system instructions override user**; `assistant` role is treated as prior model output.
- **Tool execution control (`tool_choice`):**
  - `ToolChoiceOptions`: `"none" | "auto" | "required"`
    - `none`: model **will not** call tools; generates a message.
    - `auto`: model may choose message vs tool call(s).
    - `required`: model **must** call ≥1 tool.
  - Forcing specific tools (objects): `ToolChoiceFunction {name}`, `ToolChoiceCustom {name}`, `ToolChoiceMcp {server_label, name}`, `ToolChoiceShell {type}`, `ToolChoiceApplyPatch {type}`, `ToolChoiceAllowed {mode, tools}` (constrain to a set).
- **Response lifecycle status (`ResponseStatus`):** `"queued" | "in_progress" | "completed" | "failed" | "cancelled" | "incomplete"`.
- **Streaming/event model:** server emits typed events including `ResponseCreatedEvent`, `ResponseInProgressEvent`, `ResponseCompletedEvent`, `ResponseFailedEvent`, `ResponseIncompleteEvent`, plus granular deltas/done events for text/audio/refusals and tool calls (e.g., `ResponseFunctionCallArgumentsDelta/Done`, `ResponseMcpCall...`, `ResponseWebSearchCall...`, `ResponseFileSearchCall...`, `ResponseCodeInterpreterCall...`).
- **Including extra tool/output data (`include[]`: `ResponseIncludable`):**
  - `web_search_call.action.sources`, `file_search_call.results`, `web_search_call.results`
  - `code_interpreter_call.outputs`
  - `computer_call_output.output.image_url`
  - `message.input_image.image_url`
  - `message.output_text.logprobs`
  - `reasoning.encrypted_content`
- **Output formatting:** `text.format` supports `{type:"text"}` (default), `{type:"json_schema"}` (Structured Outputs), `{type:"json_object"}` (older JSON mode; “not recommended for gpt-4o and newer”).

</details>

### 📖 Runner.run & RunConfig (OpenAI Agents SDK, Python)
**Reference Doc** · [source](https://openai.github.io/openai-agents-python/ref/run/)

*Canonical runner signatures, accepted input types, and multi-turn lifecycle semantics*

<details>
<summary>Key content</summary>

- **Canonical async runner signature (Runner.run):**  
  `await Runner.run(starting_agent, input, *, context=None, max_turns=DEFAULT_MAX_TURNS, hooks=None, run_config=None, error_handlers=None, previous_response_id=None, auto_previous_response_id=False, conversation_id=None, session=None) -> RunResult`
  - **Input types:** `input ∈ { str | list[TResponseInputItem] | RunState[TContext] }`
  - **starting_agent:** `Agent[TContext]` (required)

- **Lifecycle loop (workflow semantics):**  
  1) Invoke agent with given input  
  2) **Stop condition:** if agent produces **final output** of type `agent.output_type`  
  3) If **handoff** occurs: repeat loop with the new agent  
  4) Else: execute **tool calls** (if any), then re-run loop

- **Turn definition / limit:**  
  `max_turns` counts **one AI invocation per turn**, **including tool calls**.

- **Exceptions (unless handled):**  
  - `MaxTurnsExceeded` when `max_turns` exceeded  
  - `GuardrailTripwireTriggered` when a guardrail tripwire triggers  
  - **Guardrail note:** *Only the first agent’s input guardrails are run.*

- **Multi-turn / state parameters:**  
  - `previous_response_id`: Responses API optimization to avoid resending prior-turn input  
  - `conversation_id`: uses Responses API conversation state; runner reads/writes items; recommended only if exclusively using OpenAI models (other providers won’t write to Conversation)  
  - `session`: automatic conversation history management

- **Sync + streaming variants:**  
  - `Runner.run_sync(...)`: wraps `run`; won’t work inside an existing event loop (e.g., Jupyter/async frameworks).  
  - `Runner.run_streamed(...) -> RunResultStreaming`: provides method to stream semantic events.

- **RunConfig key overrides (global):**  
  - `model`: overrides every agent’s model  
  - `model_provider`: resolves string model names (default: OpenAI via `MultiProvider`)  
  - `model_settings`: non-null values override agent-specific settings  
  - `input_guardrails` (initial input), `output_guardrails` (final output)  
  - `handoff_input_filter` (global; per-handoff filter takes precedence)  
  - `nest_handoff_history` (beta, default False) + `handoff_history_mapper` (used when nesting True)  
  - `call_model_input_filter` (edit model input pre-call), `tool_error_formatter`  
  - tracing controls: `tracing_disabled`, `tracing`, `workflow_name`, `trace_id`, `group_id`, `trace_metadata`, `trace_include_sensitive_data`  
  - `reasoning_item_id_policy`: `None/"preserve"` keeps IDs; `"omit"` strips IDs

</details>

### 📖 Streaming API responses (SSE) — Responses vs Chat Completions
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/streaming)

*Central index of streaming behavior across endpoints (SSE framing, event types, lifecycle patterns, and robust client iteration).*

<details>
<summary>Key content</summary>

- **Default behavior:** API returns the model’s *entire* output in one HTTP response; **streaming** lets clients process output incrementally while generation continues.
- **Enable streaming (Responses API):** set **`stream: true`** (JS) / **`stream=True`** (Python) in `client.responses.create(...)`, then iterate events (`for await ...` / `for event in stream`).
- **Transport:** HTTP streaming uses **Server-Sent Events (SSE)** with **semantic, typed events** (type-safe schemas).  
  - Persistent alternative: **WebSocket mode** (incremental inputs via **`previous_response_id`**) is referenced separately.
- **Common lifecycle events (Responses streaming):**
  - `response.created`
  - `response.output_text.delta`
  - `response.completed`
  - `error`
- **Event typing (examples from union list):** `ResponseCreatedEvent`, `ResponseInProgressEvent`, `ResponseCompletedEvent`, `ResponseOutputTextDelta`, `ResponseFunctionCallArgumentsDelta/Done`, tool-call progress events (file search, code interpreter), plus `Error`.
- **Chat Completions streaming:** set **`stream: true`** / **`stream=True`** on `chat.completions.create(...)`. Stream returns **data-only SSE chunks**.
  - Key parsing rule: streamed chunks use **`choices[0].delta`** (not `message`).  
    - `delta` may contain a **role token**, **content token**, or **nothing** (example shows `{}` at end).
  - To print only text: write `chunk.choices[0]?.delta?.content || ""` (JS) or check `delta.content is not None` (Python).
- **Design rationale:** OpenAI recommends **Responses API for streaming** because it’s “designed with streaming in mind” and uses **semantic events**.
- **Moderation risk:** streaming partial outputs makes moderation harder; may affect approved usage.

</details>

### 📖 Structured Outputs (JSON Schema enforcement)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/structured-outputs?api-mode=chat)

*JSON schema-based structured output constraints + enforcement behavior via `response_format` / `text.format`*

<details>
<summary>Key content</summary>

- **What it guarantees:** Structured Outputs ensures the model output **adheres to your supplied JSON Schema** (not just valid JSON). Prevents missing required keys and invalid enum values.
- **How to enable (Responses API):** set `text: { format: { type: "json_schema", strict: true, schema: {...} } }` or use SDK helpers (`responses.parse` with Pydantic / Zod).
- **When to use which:**
  - **Function calling**: when connecting model to tools/functions/data in your system.
  - **`response_format` / `text.format` schema**: when you want the assistant’s **user-facing response** structured for UI, tutoring steps, extraction, etc.
- **Structured Outputs vs JSON mode (table facts):**
  - Valid JSON: both **Yes**
  - Schema adherence: Structured Outputs **Yes**; JSON mode **No**
  - Structured Outputs compatible models: **gpt-4o-mini**, **gpt-4o-mini-2024-07-18**, **gpt-4o-2024-08-06** and later (JSON mode works on broader set incl. `gpt-3.5-turbo`, `gpt-4-*`, `gpt-4o-*`).
  - JSON mode enable: `text: { format: { type: "json_object" } }`
- **Refusals:** If the model refuses for safety, output may not match schema; API includes a **`refusal`** content item/field so refusals are programmatically detectable.
- **Schema rules/limits (enforced):**
  - Root schema **must be an object** (cannot be top-level `anyOf`).
  - **All fields must be required**; emulate optional via union with `null` (e.g., `"type": ["string","null"]`).
  - Objects must set **`additionalProperties: false`**.
  - Limits: **≤5000** total object properties, **≤10** nesting levels; total string size **≤120,000** chars; **≤1000** enum values overall.
  - Key ordering: output keys follow schema key order.
- **Supported JSON Schema subset:** types `string, number, boolean, integer, object, array, enum, anyOf`; supports `$defs` and recursion (`$ref: "#"`, etc.). Unsupported keywords include `allOf`, `not`, `if/then/else`, etc.

</details>

### 📖 Tool/Function Calling Schema & Control Knobs (OpenAI Responses API)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/function-calling?api-mode=chat)

*Tool-calling request/response schema (tool definitions, tool_choice behavior, tool call arguments), plus planning-loop-relevant fields like `parallel_tool_calls`*

<details>
<summary>Key content</summary>

- **Tool-calling workflow (5 steps):**  
  1) Request model with `tools` available → 2) Model returns tool call(s) → 3) App executes tool(s) → 4) App sends tool outputs back → 5) Model returns final answer or more tool calls.
- **Tool definition schema (function tools):**  
  `{"type":"function","name":..., "description":..., "parameters": JSONSchema, "strict": bool}`.  
  Example includes `additionalProperties:false` and `required:[...]`.
- **Tool call item (model → app):** response `output` array contains items with:  
  `type:"function_call"`, `call_id`, `name`, `arguments` (JSON-encoded string). Multiple calls may appear in one turn.
- **Tool output item (app → model):** append to next request input:  
  `{"type":"function_call_output","call_id": <from tool call>, "output": <string | array of image/file objects>}`.
- **Reasoning-model constraint:** for GPT-5 / o4-mini, **any reasoning items returned alongside tool calls must be passed back** with tool outputs in the next request.
- **`tool_choice` behaviors (defaults & forcing):**  
  - Default: `"auto"` (0, 1, or many tool calls)  
  - `"required"` (must call ≥1 tool)  
  - Force one tool: `{"type":"function","name":"get_weather"}`  
  - Restrict without changing `tools`: `{"type":"allowed_tools","mode":"auto","tools":[...]}`
  - `"none"` imitates passing no tools.
- **Parallelism control:** `parallel_tool_calls:false` ⇒ model can call **exactly 0 or 1** tool per turn. (Parallel calling not possible with built-in tools.)
- **Strict mode requirements (Structured Outputs):** if `strict:true`: every object must set `additionalProperties:false` and **all** `properties` must be in `required`; optional fields use union types like `["string","null"]`.

</details>

### 📖 Typed Handoffs (Supervisor → Sub-agent) in OpenAI Agents SDK
**Reference Doc** · [source](https://openai.github.io/openai-agents-python/ref/handoffs/)

*Precise, typed handoff interfaces for transferring context/state to a delegated agent (filters, history nesting, schemas, enable/disable).*

<details>
<summary>Key content</summary>

- **Core type aliases**
  - **HandoffInputFilter (Eq. 1):**  
    `Callable[[HandoffInputData], MaybeAwaitable[HandoffInputData]]`  
    Filters/edits the data passed to the next agent.
  - **HandoffHistoryMapper (Eq. 2):**  
    `Callable[[list[TResponseInputItem]], list[TResponseInputItem]]`  
    Maps prior transcript → nested summary payload.

- **HandoffInputData (dataclass) fields**
  - `input_history: str | tuple[TResponseInputItem, ...]` — history before `Runner.run()`.
  - `pre_handoff_items: tuple[RunItem, ...]` — items generated before the turn where handoff invoked.
  - `new_items: tuple[RunItem, ...]` — items generated during current turn **including** the triggering item and the tool output message representing the handoff output.
  - `run_context: RunContextWrapper[Any] | None = None` — optional (backwards compatibility).
  - `input_items: tuple[RunItem, ...] | None = None` — if set, used **instead of** `new_items` to build next agent input (lets you filter duplicates for model input while keeping full `new_items` in session history).
  - `clone(**kwargs) -> HandoffInputData` — copy with modifications.

- **Handoff (dataclass) behavior/params**
  - `input_json_schema` — schema exposed to model as tool parameters; describes structured payload passed to `on_invoke_handoff` and **does not replace** next agent’s main input.
  - `on_invoke_handoff: Callable[[RunContextWrapper[Any], str], Awaitable[TAgent]]` — receives (1) handoff run context, (2) LLM JSON args string (or `""` if schema empty); must return an agent.
  - `input_filter: HandoffInputFilter | None` — default: next agent sees entire conversation history; can remove older inputs/tools, etc. **Streaming note:** results of this function are not streamed; earlier items already streamed.
  - `strict_json_schema` — recommended `True` to increase correct JSON input.
  - `is_enabled: bool | Callable[[RunContextWrapper[Any], AgentBase[Any]], MaybeAwaitable[bool]] = True` — disabled handoffs hidden from LLM at runtime.
  - `nest_handoff_history` — per-handoff override of run-level nesting behavior.

- **History nesting utilities**
  - `default_handoff_history_mapper(transcript)` → **single assistant message** summarizing transcript.
  - `nest_handoff_history(handoff_input_data, history_mapper=None)` → summarizes previous transcript for next agent.
  - Wrapper markers: `get_conversation_history_wrappers()`, `set_conversation_history_wrappers(...)`, `reset_conversation_history_wrappers()`.

- **Factory: `handoff(...) -> Handoff`**
  - Key args: `agent` (required), `tool_name_override`, `tool_description_override`, `on_handoff` (+ optional `input_type` for validation/parsing), `input_filter`, `nest_handoff_history`, `is_enabled`.

</details>

### 📋 # Source: https://docs.temporal.io/encyclopedia/event-history/event-history-go
**Source** · 

### 📋 # Source: https://openai.github.io/openai-agents-python/ref/memory/
**Source** · 

### 📋 # Source: https://openai.github.io/openai-agents-python/ref/memory/session/
**Source** · 

### 🔍 LLM Agent Evaluation Metrics & Benchmark Construction
**Explainer** · [source](https://arxiv.org/html/2507.21504v1)

*Definitions/taxonomy of agent evaluation metrics + how benchmarks/evals are run (offline/online, tooling, contexts)*

<details>
<summary>Key content</summary>

- **Two-dimensional taxonomy (Section 2):**
  - **Evaluation Objectives (what):** Agent Behavior, Agent Capabilities, Reliability, Safety & Alignment.
  - **Evaluation Process (how):** Interaction Mode, Evaluation Data, Metrics Computation Methods, Evaluation Tooling, Evaluation Contexts.
- **Agent Behavior metrics (Section 3.1):**
  - **Task completion:** **Success Rate (SR)** / Task Success Rate / Overall Success Rate; **Task Goal Completion (TGC)**; **Pass Rate**; binary reward **{0,1}** for goal achievement.
  - **Multi-trial success:** **pass@k** = succeeds at least once in *k* attempts; stricter **pass^** = succeeds in **all** *k* attempts (used for mission-critical consistency).
  - **Latency:** **TTFT (Time To First Token)** = delay until first streamed token; **End-to-End Request Latency** = time until complete response (more relevant for async agents).
  - **Cost:** estimated from **#input tokens + #output tokens** (usage-based pricing proxy).
- **Tool-use capability metrics (Section 3.2.1):**
  - **Invocation Accuracy** (call tool vs not), **Tool Selection Accuracy**, **Retrieval Accuracy** (rank-based); ranking metrics: **MRR**, **NDCG**.
  - Parameter evaluation: **parameter name F1**; **execution-based evaluation** runs tool calls to catch semantic errors beyond AST validity.
- **Planning/reasoning metrics (Section 3.2.2):** **Node F1** (tool set), **Edge F1** / **Normalized Edit Distance** (tool sequence/graph structure), stepwise “next tool” alignment (T-Eval), **Progress Rate** (trajectory vs expected), **Step Success Rate** (% plan steps executed).
- **Evaluation process (Section 4):**
  - **Offline/static** datasets vs **online/dynamic** (simulators/users); **Evaluation-driven Development (EDD)** + **AgentOps** loop for continuous monitoring/regression detection.
  - Metric computation methods: **code-based** (assertions), **LLM-as-a-judge**, **human-in-the-loop** (gold standard for subjective/safety).

</details>

### 📋 LangGraph human-in-the-loop via checkpointed interrupts (Pregel runtime)
**Code** · [source](https://github.com/langchain-ai/langgraph/discussions/2290)

*Concrete pattern for pausing/resuming execution (human input) using checkpointing + deterministic graph runtime.*

<details>
<summary>Key content</summary>

- **Design rationale (production agents):** LangGraph prioritizes **control + durability** over “easy start.” Agents differ from classic software mainly due to **latency (seconds→minutes→hours)** and need for: **Parallelization, Streaming, Task queue, Checkpointing, Human-in-the-loop, Tracing** (six-feature shortlist).
- **Why structured graphs (not one big while-loop):** Splitting into discrete nodes enables **checkpointing + human-in-the-loop**; execution state of arbitrary subroutines can’t be portably saved/resumed across machines.
- **Execution algorithm (Pregel/BSP) procedure (Section “Execution algorithm”):**
  - **Channels**: named data containers with **version** = monotonically increasing string.
  - **Nodes**: functions subscribing to channels; run when subscribed channel versions change.
  - **Input mapping**: initial input written to input channels triggers subscribed nodes.
  - **Output mapping**: agent returns values of output channels when execution halts.
  - **Per-iteration loop**:
    1) Select runnable nodes by comparing channel versions vs last-seen versions.  
    2) Execute selected nodes **in parallel** with **isolated copies** of state.  
    3) Nodes write updates locally.  
    4) Apply updates to channels in a **deterministic order** (prevents data races), bump versions.
  - Stop when no nodes runnable or **iteration limit** reached (developer-set constant).
- **Checkpointing details:** Save **serialized channel values** (default **MsgPack**, optionally encrypted), channel version strings, and “which versions each node has seen.” Enables resume **on any machine**, arbitrarily later.
- **Human-in-the-loop mechanism:** Add `interrupt()` inside a node to **pause**; later **resume from checkpoint** with human input (scales better than keeping processes waiting).

</details>

### 📋 OpenAI Agents SDK — Examples Index (Patterns & Multi-Agent Building Blocks)
**Code** · [source](https://openai.github.io/openai-agents-python/examples/)

*Runnable end-to-end examples demonstrating agent composition and handoffs (supervisor-to-specialist patterns) with concrete execution flow and payload shapes.*

<details>
<summary>Key content</summary>

- **Where to find runnable implementations:** All examples live in the repo under `examples/` with categorized subfolders: https://github.com/openai/openai-agents-python/tree/main/examples
- **Agent design patterns (multi-agent relevant):** `examples/agent_patterns/` includes concrete patterns for:
  - **Agents as tools** (including streaming events):  
    - `examples/agent_patterns/agents_as_tools_streaming.py`  
    - **Structured tool inputs:** `examples/agent_patterns/agents_as_tools_structured.py`
  - **Parallel agent execution** (pattern category explicitly listed).
  - **Conditional tool usage** and **forcing tool use**: `examples/agent_patterns/forcing_tool_use.py`
  - **Guardrails & judging:** input/output guardrails, “LLM as a judge,” routing, streaming guardrails.
  - **Human-in-the-loop (HITL)** with approval + state serialization:  
    - `examples/agent_patterns/human_in_the_loop.py`  
    - Streaming HITL: `examples/agent_patterns/human_in_the_loop_stream.py`  
    - Custom rejection messages: `examples/agent_patterns/human_in_the_loop_custom_rejection.py`
- **Handoffs (delegation/message filtering):** `examples/handoffs/` provides practical handoff flows with message filtering:
  - `examples/handoffs/message_filter.py`
  - Streaming variant: `examples/handoffs/message_filter_streaming.py`
- **Basic execution plumbing useful for orchestration:** `examples/basic/` includes lifecycle hooks (`examples/basic/lifecycle_example.py`), streaming outputs, retry management (`examples/basic/retry.py`), and websocket streaming with shared session helper (`examples/basic/stream_ws.py`).

</details>

---

## Related Topics

- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/multi-agent-systems|Multi-Agent Systems]]
- [[topics/function-calling|Function Calling]]
- [[topics/mcp-tool-ecosystem|Model Context Protocol]]
- [[topics/agentic-coding|Agentic Coding]]
