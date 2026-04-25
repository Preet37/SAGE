# Card: ReflAct (Reflection-for-Action) vs ReAct Backbone
**Source:** https://arxiv.org/pdf/2505.15182v1.pdf  
**Role:** paper | **Need:** COMPARISON_DATA  
**Anchor:** World-grounded ReAct-style thought/action loop variant with explicit goal grounding + decision procedure

## Key Content
- **POMDP framing (Section 2):** Task as \(M=\langle U,S,A,O,P,R\rangle\). Instruction \(u\in U\), hidden state \(s\in S\), action \(a\in A\), observation \(o\in O\). \(U,A,O\) are natural language.
- **ReAct loop formalization (Section 2):** Context \(c_t=(h_t,o_t)\), where \(h_t=\{u,\tau_1,a_1,o_1,\dots,\tau_t,a_t\}\).  
  Thought: \(\tau_t\sim \pi^{thought}_\theta(\cdot\mid c_t)\).  
  Augmented context: \(c'_t=c_t\oplus \tau_t\).  
  Action: \(a_t\sim \pi^{act}_\theta(\cdot\mid c'_t)\).
- **Thought strongly reweights actions (Section 3.1):** Average action-distribution entropy over 134 ALFWorld tasks (Llama-3.1-8B-Instruct):  
  \(\bar H_{NoThinking}=1.23\) vs \(\bar H_{ReAct}=0.30\) (Table 1).
- **Core failure modes of ReAct (Section 3.2):** (1) incoherent internal belief/state (revisits, false “holding” assumptions), (2) short-sighted planning vs long-term goal → compounding errors/hallucinations.
- **ReflAct objective (Section 4):** Long-term return \(G_t=\sum_{k=0}^\infty \gamma^k R_{t+k}\), \(\gamma\in[0,1)\). Optimal thought:  
  \(\tau^*_t=\arg\max_{\tau\in T}\mathbb{E}_{a\sim \pi^{act}_\theta(\cdot\mid c_t\oplus\tau)}[\mathbb{E}[G_t\mid s_t,a]]\).
- **ReflAct procedure (Section 4):** Replace “next-action thinking” with **goal-state reflection each step**. Prompt: *“reflect on the agent’s state in relation to the task goal, then output the action.”* Reflection space \(K\): structured encoding of belief state \(M\) + goal \(G\).
- **Empirical gains (Table 2):** Success Rate (SR) improvements of ReflAct over ReAct: **ALFWorld +36.4%**, **ScienceWorld +8.5%**, **Jericho +38.1%**. Example rows:  
  - GPT-4o ALFWorld SR: ReAct 85.1 → ReflAct **93.3**.  
  - Llama-3.1-8B ALFWorld SR: ReAct 29.1 → ReflAct **60.5**.
- **Safety/reliability (Fig. 8):** “No tasks where only ReflAct fails”; ReAct introduces unique failures vs NoThinking.
- **Defaults/params:** ALFWorld test set **134 tasks**; ScienceWorld **211**; Jericho **20**. Reflexion trials repeated **3**. RAFA cost example: depth \(d=2\), branching \(b=2\) ⇒ **13 LLM queries/step** vs ReflAct **1**.

## When to surface
Use when students ask how agent “reasoning loops” fail (hallucinated thoughts, belief drift) and how to redesign ReAct-style backbones to stay grounded in **state + goal** with measurable reliability gains.