## Core Definitions

**LLM agent planning** — As OpenAI’s “Practical guide to building agents” defines an agent, it is a system where an **LLM controls workflow execution**, decides what to do next, recognizes completion, and can correct or halt and hand control back to the user; it does so by **dynamically selecting tools** within guardrails. Planning, in this framing, is the part of the agent loop that decides the next actions (and often subgoals) to accomplish the user’s goal. Source: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

**Goal-directed loop (plan → act → observe → revise)** — In interactive/grounded settings, planning is not a one-time artifact but a **closed-loop** process: propose a plan, execute actions, observe environment feedback, and refine the plan when feedback indicates mismatch. This is explicit in systems like **Voyager’s iterative prompting** (generate code → execute → get feedback/errors → self-verify/critique → refine) and in **stepwise planning** benchmarks like VestaBench (multi-step interaction with observations and critic feedback across trials). Sources: https://arxiv.org/abs/2305.16291 ; https://aclanthology.org/2025.emnlp-industry.149.pdf

**Task decomposition / subgoal generation** — As Weng summarizes under “Planning – Subgoal and decomposition,” agents handle complex tasks by breaking them into **smaller, manageable subgoals**, often elicited via prompting (“What are the subgoals…?”) or structured task-specific instructions. Decomposition is a planning primitive that reduces long-horizon tasks into steps the agent can execute and verify. Source: https://lilianweng.github.io/posts/2023-06-23-agent/

**Plan execution** — In VestaBench’s formalization, the agent outputs a plan \(P=(a_1,\dots,a_n)\) with actions \(a_i\in\mathcal{A}\), executes them in a simulator \(S\), and the outcome is evaluated on the final environment state/graph \(G^*\) against success and safety criteria. This is the “execution” phase: turning planned steps into environment transitions and observations. Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

**Feedback-driven replanning** — AdaPlanner characterizes a key failure mode: agents that act greedily without planning or that follow **static, open-loop plans** degrade as horizon/complexity increases; AdaPlanner’s core contribution is to **refine its self-generated plan adaptively in response to environmental feedback**, using “in-plan” and “out-of-plan” refinement strategies. This is replanning: updating the plan based on what actually happened. Source: https://proceedings.nips.cc/paper_files/paper/2023/file/b5c8c1c117618267944b2617add0a766-Paper-Conference.pdf

**Multi-step reasoning (in service of planning)** — The “Multi-Step Reasoning with LLMs” survey frames a broad taxonomy of methods to **generate, evaluate, and control** multi-step reasoning, including approaches that go beyond linear chain-of-thought by using external tools, optimization loops, and self-reflection. In agent planning, multi-step reasoning is the internal computation used to choose subgoals/actions over multiple steps. Source: https://arxiv.org/html/2407.11511v2

**Tree-of-Thoughts (search-based planning over thoughts)** — Yao et al. define problem solving as **search over a tree** where a **state** is “input + sequence of thoughts so far,” and each step expands candidate “thoughts,” evaluates states (value/vote), and selects via BFS/DFS with pruning/backtracking. This is planning as explicit search rather than a single linear chain. Source: https://arxiv.org/abs/2305.10601 (and PDF: https://arxiv.org/pdf/2305.10601.pdf)

**Reflection (trial → feedback → memory → next attempt)** — Reflexion defines a loop where an Actor produces a trajectory, an Evaluator yields reward/feedback, and a Self-Reflection model converts that into **verbal reflections** stored in an episodic memory buffer that conditions later trials—improving behavior **without weight updates**. Reflection is a specific mechanism for feedback-driven improvement across attempts. Source: https://arxiv.org/abs/2303.11366

**Global plan (continuously updated) vs purely reactive steps** — GoalAct defines a **global plan** \(P=\{p_i\}_{i=1}^n\) (high-level skill steps, ending with Finish) and updates it over time \(P_t=\pi(u,T,H_t)\) based on user query, tools, and history. It positions ReAct as lacking global perspective and being prone to local branches, while continuous plan updates keep long-horizon coherence and executability. Source: https://arxiv.org/html/2504.16563v2


## Key Formulas & Empirical Results

### Planning / execution formalizations & metrics

**VestaBench planning definition + success/safety evaluation**
- Plan: \(P=(a_1,\dots,a_n)\), \(a_i\in\mathcal{A}\); execute in simulator \(S\) → final graph \(G^*\).
- “Successful and safe” iff predefined success + safety criteria are satisfied on \(G^*\).
- Metrics reported: **delivery rate**, **success rate**, **safety rate**.
Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

**VestaBench empirical findings (selected)**
- **One-go** (generate full plan once) is weakest; **stepwise** improves; **ReAct** improves success & safety on VestaBench-VH by ~**5%** and ~**10%** respectively (reported).
- Safety degrades with complexity: for ReAct+Critic (1) on VestaBench-VH, safety **66.67% (low)**, **48.64% (medium)**, **33.33% (high)**.
Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

### Search-based planning (Tree of Thoughts)

**ToT state and search components (definitions)**
- State \(s\): input + thoughts so far.
- Generate candidate thoughts \(T=\{t_i\}\); evaluate via **Value** \(V(s)\) or **Vote**; search via BFS/DFS with pruning/backtracking.
Source: https://arxiv.org/pdf/2305.10601.pdf

**ToT Game of 24 results (100 hard games)**
- IO 7.3%; CoT 4.0%; CoT-SC (k=100) 9.0%
- ToT BFS **b=1: 45%**; ToT BFS **b=5: 74%**
Source: https://arxiv.org/pdf/2305.10601.pdf

### Reflection / state-reflection results

**Reflexion memory sizing defaults**
- Long-term episodic memory bounded to **1–3 experiences** (often **3** for AlfWorld/HotPotQA; **1** for programming) to fit context limits.
Source: https://arxiv.org/abs/2303.11366

**Reflexion benchmark highlights**
- AlfWorld: ReAct+Reflexion completes **130/134** tasks; improves **+22% absolute** over strong baselines in **12** learning steps (reported).
- HumanEval (Python): baseline **0.80 pass@1** → Reflexion **0.91**.
Source: https://arxiv.org/abs/2303.11366

**ReflAct (goal–state reflection) results (Table 2 highlights)**
- GPT-4o: ReflAct ALFWorld **93.3** vs ReAct **85.1**.
- GPT-4o-mini: ReflAct ALFWorld **66.4** vs ReAct **53.0**.
- Llama-3.1-8B: ReflAct ALFWorld **60.5** vs ReAct **29.1**.
Source: https://arxiv.org/abs/2505.15182v2

### Global planning (GoalAct)

**GoalAct global plan equations**
- Global plan: \(P=\{p_i\}_{i=1}^{n}\), final step \(p_n\) is **Finish**.
- Plan update at time \(t\): \(P_t=\pi(u,T,H_t)\).
- History: \(H_t=\{(a_i,o_i)\}_{i=1}^{t-1}\).
Source: https://arxiv.org/html/2504.16563v2

**GoalAct benchmark result (LegalAgentBench, Table 2 highlight)**
- GPT-4o-mini (ALL): GoalAct **0.7720** vs ReAct **0.6161**, CodeAct **0.6275**, Plan-and-Execute **0.4503** (reported).
Source: https://arxiv.org/html/2504.16563v2

### Closed-loop planning from feedback (AdaPlanner)

**AdaPlanner headline results**
- ALFWorld and MiniWoB++: AdaPlanner outperforms SOTA baselines by **3.73%** and **4.11%** while using **2×** and **600× fewer samples**, respectively (reported).
Source: https://proceedings.nips.cc/paper_files/paper/2023/file/b5c8c1c117618267944b2617add0a766-Paper-Conference.pdf

### Latency-aware orchestration (planning under wall-clock constraints)

**LAMaS latency vs cost under parallelism**
- Latency (critical path): \(L=\sum_{l\in\mathcal{L}} \max_{o\in\mathcal{O}_l} t(o)\)
- Cost: \(C=\sum_{l\in\mathcal{L}}\sum_{o\in\mathcal{O}_l} c(o)\)
Claim supported: token cost and wall-clock latency diverge under parallel execution; optimize explicitly for critical path.
Source: https://arxiv.org/abs/2601.10560

**LAMaS key results vs MaAS (Table 2 highlights)**
- GSM8K: score 93.37 vs 93.13; CP len 913.5 vs 1474.6 (**−38.0%**)
- HumanEval: 92.11 vs 93.00; CP len 1042.7 vs 1810.8 (**−42.4%**)
- MATH: 52.26 vs 51.23; CP len 1195.8 vs 2218.5 (**−46.1%**)
Source: https://arxiv.org/abs/2601.10560

### Speculative actions (planning for speed)

**Speculative Actions expected runtime ratio (Proposition 1)**
\[
\frac{\mathbb{E}[T_{\text{spec}}]}{\mathbb{E}[T_{\text{seq}}]}=\frac{1}{2-p}\left(1+\frac{l}{L}\right)
\]
- \(L\): mean latency of actual API call; \(l\): mean latency of speculative model; \(p\): probability speculation matches true next call.
Claim supported: even “lossless” speculation has bounded speedups unless multi-step speculation is used; depends on accuracy \(p\) and overhead \(l\).
Source: https://arxiv.org/html/2510.04371v1


## How It Works

### A. Canonical goal-directed agent planning loop (closed-loop)

1. **Interpret goal + constraints**
   - Extract success criteria, safety constraints, and tool/action limits (VestaBench explicitly evaluates both success and safety on final state \(G^*\)).  
   Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

2. **Decompose into subgoals / plan steps**
   - Use decomposition prompting (Weng) or produce a global plan over skills (GoalAct’s \(P=\{p_i\}\)).  
   Sources: https://lilianweng.github.io/posts/2023-06-23-agent/ ; https://arxiv.org/html/2504.16563v2

3. **Select next action(s)**
   - Reactive: choose next tool/action from current context (ReAct-style).
   - Plan-guided: choose action that advances current plan step; optionally update the plan \(P_t=\pi(u,T,H_t)\).  
   Source: https://arxiv.org/html/2504.16563v2

4. **Execute**
   - Run tool calls / environment actions; in simulators, this transitions state and yields observation \(o\) (VestaBench stepwise trajectories interleave actions and observations).  
   Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

5. **Observe + evaluate**
   - Compare observation to expected progress; optionally use a critic/evaluator (VestaBench “critic J gives feedback \(f_i\)” at end of trials; Voyager uses a separate self-verification critic).  
   Sources: https://aclanthology.org/2025.emnlp-industry.149.pdf ; https://arxiv.org/abs/2305.16291

6. **Replan / refine**
   - If mismatch/failure: refine plan (AdaPlanner’s adaptive refinement; Voyager’s code repair loop; Reflexion’s reflection memory across trials).  
   Sources: https://proceedings.nips.cc/paper_files/paper/2023/file/b5c8c1c117618267944b2617add0a766-Paper-Conference.pdf ; https://arxiv.org/abs/2305.16291 ; https://arxiv.org/abs/2303.11366

7. **Stop**
   - Stop when success criteria met (GoalAct’s final step Finish; OpenAI agent loop stops when final output produced or no tool calls are returned).  
   Sources: https://arxiv.org/html/2504.16563v2 ; https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf

---

### B. Stepwise vs one-shot planning (VestaBench mechanics)

**One-go**
1. Generate full plan \(P=(a_1,\dots,a_n)\) once.
2. Execute all actions.
3. Evaluate success/safety on \(G^*\).

**Stepwise (multi-trial)**
1. For trial \(i\), execute step-by-step actions \(a_{i1}, a_{i2}, \dots\).
2. After each action, receive observation \(o_{ij}\) and state \(G_{ij}\).
3. End of trial: critic \(J\) produces feedback \(f_i\).
4. Repeat trials until Done or trials exhausted.

Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

---

### C. Planning as explicit search (Tree of Thoughts, BFS sketch)

```text
Initialize frontier with state s0 (input, no thoughts)
For depth d = 1..D:
  For each state s in frontier:
    Generate k candidate thoughts t1..tk from s
    Create successor states s' = s + t
    Evaluate each s' with Value V(s') or Vote among candidates
  Keep top b states (beam/BFS)
Return best complete solution state
```

Key knobs the tutor can ask about mid-conversation:
- Thought granularity (equation line vs paragraph)
- Evaluator type (value vs vote)
- Search (BFS beam width b vs DFS with pruning threshold)

Source: https://arxiv.org/pdf/2305.10601.pdf


## Teaching Approaches

### Intuitive (no math)
Planning is a **hypothesis about what will work**. The agent writes down a few steps, tries the first one, looks at what actually happened, and then either continues or edits the plan. Strong agents expect the world to surprise them, so they treat plans as **editable drafts**, not commitments (mirrors AdaPlanner/Voyager closed-loop refinement and VestaBench stepwise replanning).

### Technical (with math)
Model the interaction as a sequence of actions and observations (GoalAct history \(H_t=\{(a_i,o_i)\}\); VestaBench plan \(P=(a_1,\dots,a_n)\) executed to final state \(G^*\)). Planning is a policy that maps \((u,T,H_t)\) to an updated plan \(P_t\) (GoalAct), and execution produces new observations that update \(H_{t+1}\), enabling feedback-driven replanning.

### Analogy-based
- **GPS rerouting:** You have a destination (goal), a route (plan), and live traffic (observations). When a road is closed (tool failure / environment mismatch), you reroute (replan) rather than stubbornly following the original directions (open-loop plan).
- **Debugging code:** Voyager’s loop is literally “write code → run → read error → patch → rerun,” which is planning as iterative hypothesis testing. Source: https://arxiv.org/abs/2305.16291


## Common Misconceptions

1. **“If the model is smart enough, it should just output the whole plan once (one-shot) and execute it.”**  
   - Why wrong: VestaBench reports **direct one-go is weakest**, and stepwise/ReAct-style interaction improves outcomes; long-horizon tasks encounter unexpected state constraints and adversarial conditions.  
   - Correct model: Plans are **fragile under partial observability and constraints**; stepwise execution with observations and critic feedback supports replanning.  
   Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

2. **“ReAct-style ‘think then act’ is always better than not thinking.”**  
   - Why wrong: ReflAct shows that “thoughts strongly reweight actions” (entropy difference reported) and argues ReAct failures can come from **ungrounded internal state** and **short-sighted planning**; ReflAct’s goal–state reflection improves results substantially.  
   - Correct model: The content of intermediate reasoning matters; reflection should be **grounded in goal + state**, not just free-form next-action narration.  
   Source: https://arxiv.org/abs/2505.15182v2

3. **“Reflection is just retrying the same thing again.”**  
   - Why wrong: Reflexion’s loop explicitly converts feedback + trajectory into **verbal self-reflections** stored in memory and used to condition later trials; it’s a mechanism for **changing future behavior** without weight updates, not mere repetition.  
   - Correct model: Reflection = **feedback → distilled lesson → memory → policy conditioning**.  
   Source: https://arxiv.org/abs/2303.11366

4. **“Planning is only about correctness; latency/cost are separate engineering concerns.”**  
   - Why wrong: LAMaS formalizes latency as **critical path** \(L=\sum_l \max_{o\in\mathcal{O}_l} t(o)\) and cost as additive \(C=\sum_l\sum_o c(o)\); optimizing one doesn’t optimize the other under parallelism.  
   - Correct model: Planning/orchestration can be explicitly optimized for **wall-clock latency** and **token/tool cost** with different objectives.  
   Source: https://arxiv.org/abs/2601.10560

5. **“A global plan means you don’t need to adapt; you just execute the plan.”**  
   - Why wrong: GoalAct’s key move is that the global plan is **continuously updated** \(P_t=\pi(u,T,H_t)\) based on history; it’s not static Plan-and-Execute.  
   - Correct model: Global planning can provide long-horizon coherence *while still being adaptive* via frequent plan updates.  
   Source: https://arxiv.org/html/2504.16563v2


## Worked Examples

### Example 1: Stepwise replanning vs one-shot (toy “deliver item safely”)

**Setup (mirrors VestaBench concepts):**
- Goal: “Deliver a drink to the table.”
- Safety constraints: avoid “contamination” (don’t place drink on dirty surface).
- Action space \(\mathcal{A}\): `inspect(surface)`, `clean(surface)`, `place(item, surface)`, `deliver(item, dest)`.

**One-go plan (open-loop)**
1. `place(drink, counter)`
2. `deliver(drink, table)`

**Failure mode**
- Observation after step 1: counter is dirty (constraint violated). In VestaBench terms, final \(G^*\) would fail safety criteria even if delivery succeeds.

**Stepwise plan (closed-loop)**
1. `inspect(counter)` → observe “dirty”
2. Replan: insert safety subgoal “clean counter”
3. `clean(counter)` → observe “clean”
4. `place(drink, counter)` → observe “ok”
5. `deliver(drink, table)` → success + safe

**Tutor move:** explicitly ask the student what observation would trigger replanning, and what safety metric would fail in the one-go version (VestaBench reports separate success vs safety rates).  
Source anchor for stepwise vs one-go + safety evaluation: https://aclanthology.org/2025.emnlp-industry.149.pdf

---

### Example 2: Tree-of-Thoughts BFS on Game of 24 (structure, not full run)

**Problem:** numbers 4, 5, 6, 10 → make 24.

**ToT “thought” granularity:** one equation line (as in the ToT repo example output).

**BFS sketch (b=2, depth=3):**
- Depth 1 candidates (sample):
  - t1: `10 - 4 = 6`  (remaining: 5,6,6)
  - t2: `10 + 4 = 14` (remaining: 5,6,14)
  - t3: `6 / (10-4) = 1` (remaining: 1,5,? ) … etc
- Evaluate each resulting state with Value prompt labels (sure/maybe/impossible) → keep top b.
- Depth 2 expand survivors, etc.
- A known successful chain (from the repo example):
  - `10 - 4 = 6`
  - `5 * 6 = 30`
  - `30 - 6 = 24`

**Why this is a planning example:** the agent is not committing to one chain; it is **branching and pruning** based on heuristic evaluation, which ToT shows can dramatically outperform linear CoT on this task (74% vs 4% CoT in the paper’s 100-game setting).  
Sources: https://arxiv.org/pdf/2305.10601.pdf ; https://github.com/arpg/tree-of-thought-llm


## Comparisons & Trade-offs

| Approach | Core control loop | Strengths (per sources) | Typical failure modes / costs | When to choose |
|---|---|---|---|---|
| **One-shot / one-go plan** (VestaBench) | Plan once → execute → evaluate | Simple, low interaction overhead | Weakest on VestaBench; brittle to adversarial env/instructions; no mid-course correction | Only when environment is predictable and action feasibility is high |
| **Stepwise / ReAct-style** (VestaBench framing) | (Reason) → Act → Observe → repeat | Better success/safety than one-go on VestaBench-VH (reported gains) | Can still be unsafe under complexity; can get stuck in local branches | Interactive tasks where observations matter each step |
| **Global plan with continuous updates (GoalAct)** | Maintain plan \(P_t\) over skills; update using history | Better long-horizon coherence; improves LegalAgentBench vs ReAct/Plan-and-Execute | Requires maintaining/updating plan; still must ensure executability | Multi-branch tasks where local decisions derail progress |
| **Search-based planning (ToT)** | Expand multiple thoughts → evaluate → BFS/DFS | Large gains on searchy tasks (Game of 24: 74% ToT vs 4% CoT) | More compute (multiple samples + evaluator calls) | When single-path reasoning is unreliable; need backtracking |
| **Reflection across trials (Reflexion/ReflAct)** | Attempt → feedback → reflection/memory → next attempt | Improves performance without finetuning; ReflAct improves ALFWorld vs ReAct | Needs memory budget; reflection quality matters | When repeated attempts are allowed and feedback is informative |

Sources: VestaBench https://aclanthology.org/2025.emnlp-industry.149.pdf ; GoalAct https://arxiv.org/html/2504.16563v2 ; ToT https://arxiv.org/pdf/2305.10601.pdf ; Reflexion https://arxiv.org/abs/2303.11366 ; ReflAct https://arxiv.org/abs/2505.15182v2


## Prerequisite Connections

- **Tool use / action spaces** — Planning chooses actions \(a_i\in\mathcal{A}\) and depends on what tools/actions exist (explicit in VestaBench’s action set and OpenAI’s “tools within guardrails”). Sources: https://aclanthology.org/2025.emnlp-industry.149.pdf ; https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **Observations / feedback signals** — Replanning requires interpreting observations \(o\) and critic feedback \(f\) (VestaBench stepwise; Voyager execution errors; Reflexion rewards). Sources: https://aclanthology.org/2025.emnlp-industry.149.pdf ; https://arxiv.org/abs/2305.16291 ; https://arxiv.org/abs/2303.11366
- **Multi-step reasoning prompting** — CoT/ToT are prompting-level mechanisms that implement decomposition and search. Source: https://arxiv.org/pdf/2305.10601.pdf
- **Evaluation metrics** — Success vs safety vs partial completion (VestaBench metrics; ALFWorld success/goal-condition success). Sources: https://aclanthology.org/2025.emnlp-industry.149.pdf ; https://ar5iv.labs.arxiv.org/html/2010.03768


## Socratic Question Bank

1. **“If your plan fails at step 3, what *new information* did you learn from the environment, and how should that change the remaining steps?”**  
   Good answer: names a concrete observation/constraint violation and a plan edit (insert/remove/reorder subgoal).

2. **“What’s the difference between ‘the plan is wrong’ and ‘the execution failed’?”**  
   Good answer: distinguishes infeasible/unsafe plan vs tool error/invalid action; suggests different fixes (replan vs retry/repair).

3. **“In VestaBench terms, could you succeed but be unsafe? What metric would show that?”**  
   Good answer: yes; success rate vs safety rate are separate; unsafe completion fails safety criteria on \(G^*\).

4. **“Why might a global plan help compared to choosing the next action greedily?”**  
   Good answer: avoids local branches/local optima; maintains long-horizon coherence (GoalAct positioning vs ReAct).

5. **“When would you prefer ToT-style branching search over a single chain-of-thought?”**  
   Good answer: when there are many plausible next steps and early mistakes are costly; ToT can backtrack/prune.

6. **“What makes reflection different from just ‘trying again’?”**  
   Good answer: reflection distills feedback into memory that conditions the next attempt (Reflexion loop).

7. **“If you parallelize sub-agents, why might token cost go up while latency goes down?”**  
   Good answer: cost adds across parallel operators, latency follows critical path max-per-layer (LAMaS equations).

8. **“What observation would trigger you to update the plan \(P_t\) in GoalAct’s formulation?”**  
   Good answer: any \(o_t\) that changes feasibility/priority; plan update depends on history \(H_t\).


## Likely Student Questions

**Q: What’s the formal definition of a plan in these agent planning benchmarks?**  
→ **A:** In VestaBench, a plan is \(P=(a_1,\dots,a_n)\) with each action \(a_i\in\mathcal{A}\); executing in simulator \(S\) yields final environment graph \(G^*\), and success/safety are evaluated on \(G^*\). Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

**Q: What’s the concrete difference between “one-go” and “stepwise” planning?**  
→ **A:** “One-go” generates the full multi-action plan once and executes it; “stepwise” executes actions interleaved with observations and can run multiple trials, receiving critic feedback \(f_i\) at the end of each trial. Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

**Q: Is there evidence that stepwise/ReAct replanning is better than one-shot plans?**  
→ **A:** VestaBench reports direct one-go is weakest; direct stepwise improves; ReAct improves success & safety on VestaBench-VH by ~5% and ~10% respectively (reported). Source: https://aclanthology.org/2025.emnlp-industry.149.pdf

**Q: How does Tree-of-Thoughts differ from chain-of-thought in a measurable way?**  
→ **A:** ToT explicitly searches over multiple candidate “thoughts” per step using BFS/DFS plus value/vote evaluation; on Game of 24 (100 hard games), CoT is 4.0% while ToT BFS with beam \(b=5\) is 74%. Source: https://arxiv.org/pdf/2305.10601.pdf

**Q: What exactly is the Reflexion loop?**  
→ **A:** Trial \(t\): Actor generates trajectory; Evaluator produces reward \(r_t\); Self-Reflection model converts (trajectory, reward, memory) into textual feedback \(f_t\); memory updates \(mem \leftarrow mem \oplus f_t\); repeat. Memory is typically bounded to 1–3 experiences. Source: https://arxiv.org/abs/2303.11366

**Q: What is a “global plan” in GoalAct, and how is it updated?**  
→ **A:** Global plan \(P=\{p_i\}_{i=1}^n\) is a sequence of high-level skill steps ending with Finish; at time \(t\), it is updated as \(P_t=\pi(u,T,H_t)\) where \(H_t=\{(a_i,o_i)\}_{i=1}^{t-1}\). Source: https://arxiv.org/html/2504.16563v2

**Q: Why do people say cost and latency are different for agent orchestration?**  
→ **A:** Under parallelism (LAMaS), latency is critical path \(L=\sum_l \max_{o\in\mathcal{O}_l} t(o)\) while cost is additive \(C=\sum_l\sum_o c(o)\); running more operators in parallel can increase cost while reducing latency. Source: https://arxiv.org/abs/2601.10560

**Q: Is there a formula for how much speculative actions can speed up tool-heavy agents?**  
→ **A:** Speculative Actions gives \(\mathbb{E}[T_{\text{spec}}]/\mathbb{E}[T_{\text{seq}}]=\frac{1}{2-p}(1+\frac{l}{L})\), where \(p\) is next-call prediction accuracy, \(L\) tool latency, \(l\) speculator latency. Source: https://arxiv.org/html/2510.04371v1


## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: a student needs a systems-level mental model of LLMs as the “brain” behind agent loops (planning/tool use/memory framing).
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Paper Explained)](https://youtube.com/watch?v=_YXnMBQjGDo) — Surface when: the student confuses single-step answers vs multi-step reasoning and you need to motivate decomposition before agent planning.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student asks “what are the components of an agent?” or “where does planning fit vs memory/tools?”
- [LangGraph Conceptual Docs — Agentic Concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks how to implement planning loops as state machines/graphs with retries and state.
- [ReAct paper](https://arxiv.org/abs/2210.03629) — Surface when: student asks what the canonical “reason→act→observe” loop is and why it became standard.
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — Surface when: student asks how real agent loops terminate, handle tools/handoffs, or manage memory in production.
- [LangChain — LangGraph multi-agent workflows](https://blog.langchain.dev/langgraph-multi-agent-workflows) — Surface when: student asks about supervisor/worker patterns and orchestration beyond a single agent.


## Visual Aids

![HuggingGPT's four-stage pipeline: LLM plans, selects, executes, and responds. (Shen et al. 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_010.png)  
Show when: the student asks “what does the planning loop look like end-to-end with tools/models?” (plan → select tool/model → execute → respond).

![Tree of Thoughts explores branching reasoning paths beyond linear CoT. (Yao et al. 2022)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-03-15-prompt-engineering_002.png)  
Show when: the student asks why linear CoT fails on some planning/search tasks and what “branching + evaluation + backtracking” means.


## Key Sources

- [VestaBench (EMNLP Industry 2025)](https://aclanthology.org/2025.emnlp-industry.149.pdf) — Concrete one-go vs stepwise planning definitions, safety/success metrics, and empirical safety degradation with complexity.
- [Tree of Thoughts (Yao et al. 2023)](https://arxiv.org/pdf/2305.10601.pdf) — Canonical formulation of planning as search over thoughts with BFS/DFS and strong benchmark deltas.
- [Reflexion (Shinn et al. 2023)](https://arxiv.org/abs/2303.11366) — Precise reflection loop definition (trial→reflection→memory) and benchmark improvements without finetuning.
- [GoalAct (2025)](https://arxiv.org/html/2504.16563v2) — Formal definition of a continuously updated global plan \(P_t=\pi(u,T,H_t)\) and comparisons vs ReAct/Plan-and-Execute.
- [A practical guide to building agents (OpenAI)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Production-grounded definition of agents and the core “LLM controls workflow execution + tools within guardrails” framing.