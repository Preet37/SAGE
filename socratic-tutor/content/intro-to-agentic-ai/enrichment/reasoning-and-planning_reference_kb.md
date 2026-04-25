## Core Definitions

**Chain-of-thought (CoT).** Wei et al. define chain-of-thought prompting as eliciting “a series of intermediate reasoning steps” from a language model, typically by providing exemplars that include intermediate steps, so the model decomposes a multi-step problem into smaller steps before producing a final answer (Wei et al., 2022; Google Research blog summary). CoT is a *single-path* reasoning trace: one sampled rationale leading to one answer.

**ReAct.** Yao et al. define ReAct as prompting LLMs to generate **reasoning traces and task-specific actions in an interleaved manner**, where reasoning helps induce/track/update plans and handle exceptions, and actions let the model interface with external sources (e.g., Wikipedia API or an interactive environment) to gather information and reduce hallucination/error propagation (Yao et al., 2022).

**Plan-and-execute.** Weng describes planning as an agent capability where the agent **breaks down a large task into smaller subgoals** and then carries them out, often with tool use and iterative refinement; the key distinction is an explicit *plan* (subgoals/decomposition) followed by *execution* steps, rather than purely reactive next-action selection (Weng, “LLM Powered Autonomous Agents”).

**Tree of Thoughts (ToT).** Yao et al. define Tree of Thoughts as representing problem solving as **search over a tree** where a **state** is the input plus the sequence of thoughts so far (a partial solution), and each step expands multiple candidate “thoughts,” evaluates them (value/vote), and selects states to continue—enabling BFS/DFS-style exploration and backtracking beyond linear CoT/ReAct (Yao et al., 2023).

**Reflection.** Weng characterizes reflection as an agent’s ability to do **self-criticism/self-reflection over past actions**, learn from mistakes, and refine future steps (Weng, “LLM Powered Autonomous Agents”). Reflexion formalizes this as converting feedback/reward plus trajectory into **verbal self-reflections** stored in memory and reused in later trials, improving performance without weight updates (Shinn et al., 2023).

**Self-correction.** SELF-REFINE defines self-correction as an iterative loop where the *same model* generates an initial output, produces feedback on it, and refines it repeatedly until a stopping criterion is met—no extra models, no training, no RL required (Madaan et al., 2023). Reflexion is a related but distinct self-correction approach that stores reflections in memory across *trials* (Shinn et al., 2023).

---

## Key Formulas & Empirical Results

### Self-Consistency (SC) decoding for CoT (Wang et al., 2022)
**Procedure (sample-and-marginalize):** sample multiple CoT outputs \((r_i, a_i)\) and select the most consistent final answer by aggregating over answers.
- **Majority vote objective:**
\[
a^*=\arg\max_{a\in\mathcal{A}}\sum_{i=1}^{m}\mathbf{1}(a_i=a)
\]
Variables: \(m\)=#samples; \(r_i\)=reasoning path; \(a_i\)=final answer; \(\mathcal{A}\)=answer set.

**Defaults reported:** typically **40 samples**, averaged over **10 runs**; temperature settings include **\(T=0.7\)** for PaLM-540B and GPT-3 code-davinci-002 (paper tables/appendix details).

**Empirical gains (absolute accuracy improvements vs greedy CoT; GPT-3 code-davinci-002):**
- GSM8K **60.1 → 78.0 (+17.9)**
- SVAMP **75.8 → 86.8 (+11.0)**
- AQuA **39.8 → 52.0 (+12.2)**
- StrategyQA **73.4 → 79.8 (+6.4)**
- ARC-challenge **83.6 → 87.5 (+3.9)**  
(From Wang et al., 2022 tables; also summarized in the curated card.)

**Claim supported:** sampling diverse reasoning paths and voting improves reliability/accuracy without training.

---

### Tree of Thoughts (ToT) search loop + results (Yao et al., 2023)
**State definition:** \(s = (\text{input} + \text{thoughts so far})\).  
**Evaluation heuristics:**
- **Value:** \(V(s)\) from a value prompt (scalar or labels like sure/maybe/impossible mapped to scores).
- **Vote:** compare a set of states \(S\) and pick best via a vote prompt.

**Search algorithms:**
- **BFS:** keep top \(b\) states per depth (beam-like).
- **DFS:** expand best state; prune if \(V(s) < v_{\text{th}}\); backtrack.

**Game of 24 (100 hard games; GPT-4, temp=0.7):**
- IO **7.3%**
- CoT **4.0%**
- CoT-SC (k=100) **9.0%**
- ToT BFS **b=1: 45%**
- ToT BFS **b=5: 74%**
- IO+Refine (k=10) **27%**
- IO best-of-100 **33%**
- CoT best-of-100 **49%**  
(From Yao et al., 2023.)

**Claim supported:** explicit search over thoughts can dramatically outperform single-path CoT and even heavy sampling baselines on search-y tasks.

---

### SELF-REFINE loop (Madaan et al., 2023)
**Algorithm equations:**
1) Initial generation:
\[
y_0 = M(p_{\text{gen}} \parallel x)
\]
2) Feedback:
\[
fb_t = M(p_{\text{fb}} \parallel x \parallel y_t)
\]
3) Refine:
\[
y_{t+1} = M(p_{\text{refine}} \parallel x \parallel y_t \parallel fb_t)
\]
(or with full history concatenation across iterations)

Variables: \(M\)=single LLM; \(x\)=input; \(y_t\)=draft; \(fb_t\)=feedback; \(p_{\text{gen}}, p_{\text{fb}}, p_{\text{refine}}\)=prompt templates; \(\parallel\)=concatenation.

**Defaults:** iterate until stop criterion; **max 4 iterations**; greedy decoding with **temperature 0.7** (as reported).

**Selected empirical gains (Table 1):**
- Dialogue Response (GPT-4): **25.4 → 74.6 (+49.2)**
- Constrained Generation (ChatGPT): **44.0 → 67.0 (+23.0)**
- Code Optimization (GPT-4): **27.3 → 36.0 (+8.7)**
- Sentiment Reversal (ChatGPT): **11.4 → 43.2 (+31.8)**

**Claim supported:** iterative feedback/refinement improves outputs without training.

---

### Reflexion (Shinn et al., 2023)
**Loop (Algorithm 1):** trial → evaluator reward → self-reflection text → memory update → next trial.  
**Memory default:** bound episodic memory to **1–3 experiences** (often **3** for AlfWorld/HotPotQA; **1** for programming) to fit context.

**Empirical highlights:**
- **AlfWorld:** ReAct+Reflexion completes **130/134** tasks; improves **+22% absolute** over strong baselines in **12** learning steps.
- **HumanEval (Python):** baseline **0.80 pass@1 → 0.91** with Reflexion.

**Claim supported:** reflection + memory across attempts improves success without weight updates.

---

### ReflAct benchmark results (Zhang et al., 2025)
**ReAct loop as described (POMDP framing):** at time \(t\), context \(c_t\) → thought \(\tau_t\) → action \(a_t\) conditioned on \([c_t;\tau_t]\) → observation \(o_{t+1}\).

**Key finding (ALFWorld entropy; Llama-3.1-8B-Instruct):**
- NoThinking mean entropy **1.23**
- ReAct mean entropy **0.30**  
Claim: thoughts strongly reweight action distribution; bad thoughts can mislead.

**Main results (Table 2):**
- **GPT-4o:** ReflAct ALFWorld **93.3** vs ReAct **85.1**
- **GPT-4o-mini:** ReflAct ALFWorld **66.4** vs ReAct **53.0**
- **Llama-3.1-8B:** ReflAct ALFWorld **60.5** vs ReAct **29.1**  
Claim: goal–state reflection each step improves robustness; ReAct introduces unique failures.

---

## How It Works

### 1) Chain-of-Thought prompting (single-path)
1. Provide exemplars (few-shot) that include intermediate reasoning steps, or use a zero-shot trigger like “Let’s think step by step” (as commonly described in CoT prompting guides; see DAIR.AI CoT page and Wei et al. framing).
2. Model generates a linear rationale (intermediate steps) followed by a final answer.
3. Tutor note: CoT increases *test-time computation* by spending tokens on decomposition; it does not guarantee correctness.

---

### 2) Self-Consistency decoding (CoT + sampling + vote)
1. Prompt with CoT exemplars.
2. Sample \(m\) diverse completions (temperature > 0), producing \((r_i, a_i)\).
3. Aggregate answers (majority vote per formula) to select \(a^*\).
4. Optionally: track distribution of answers as a confidence proxy (agreement rate), but the paper’s core selection is the argmax vote.

---

### 3) ReAct (reason ↔ act interleaving)
A canonical ReAct step pattern:
1. **Observation**: receive environment/tool output (e.g., retrieved text, webpage state, game state).
2. **Reasoning trace**: generate a short thought about what to do next (plan update, hypothesis, next subgoal).
3. **Action**: emit a tool call / environment action.
4. Loop until termination condition (task solved, step limit, or failure).

Tutor emphasis from ReflAct benchmark: the thought \(\tau_t\) changes the action distribution; ungrounded thoughts can systematically bias actions.

---

### 4) Tree of Thoughts (ToT): explicit search over thoughts
**Core loop (paper framing):** thought expansion → evaluation → selection/backtracking.

**BFS-style ToT (beam-like):**
1. Initialize state \(s_0\) = (input, empty thoughts).
2. For depth \(d = 1..D\):
   - **Generate** candidate next thoughts \(t\) for each frontier state \(s\).
   - Form successor states \(s' = s + t\).
   - **Evaluate** each \(s'\) via value prompt \(V(s')\) or vote among states.
   - **Select** top \(b\) states to keep as new frontier.
3. Return best completed solution state.

**DFS-style ToT (with pruning/backtracking):**
1. Expand the most promising state.
2. If evaluator says impossible / \(V(s) < v_{\text{th}}\), prune subtree and backtrack.
3. Continue until solved or step budget exhausted (paper uses step budget 100 for crosswords).

---

### 5) SELF-REFINE (single-model iterative improvement)
1. Generate initial draft \(y_0\).
2. Produce feedback \(fb_0\) on \(y_0\) (prompted to be specific/actionable).
3. Refine into \(y_1\) using \(x, y_0, fb_0\).
4. Repeat until stop criterion or max iterations (default max 4).

---

### 6) Reflexion (trial-based reflection + memory)
1. Run an attempt (actor policy: CoT or ReAct) to produce a trajectory.
2. Evaluator returns reward/score (can be sparse).
3. Reflection model converts (trajectory, reward, memory) into a short textual lesson \(f_t\).
4. Append \(f_t\) to episodic memory buffer (bounded 1–3 experiences).
5. Next trial conditions on memory to avoid repeating mistakes.

---

## Teaching Approaches

### Intuitive (no math)
- **CoT**: “Write down your steps so you don’t skip anything.”
- **Self-consistency**: “Solve it 40 times in different ways and trust the answer that keeps coming back.”
- **ReAct**: “Think a bit, do one action, look at what happened, then think again.”
- **ToT**: “Instead of one line of reasoning, branch into multiple possibilities and keep the best branches.”
- **Reflection/self-correction**: “After failing, write a short note about what went wrong and use it next time.”

### Technical (with math / formalism)
- **SC**: latent-variable view \(r_i \rightarrow a_i\); marginalize \(r_i\) by voting over \(a_i\).
- **ToT**: define state \(s\) as partial solution; define operators that propose next thoughts; use heuristic evaluation \(V(s)\) or voting; run BFS/DFS with pruning/backtracking.
- **Tool-agent objective framing** (multi-tool explainer): maximize expected success minus cost \(\mathbb{E}[R(\tau)-\lambda C(\tau)]\) to reason about tool-call budgets/latency vs robustness.

### Analogy-based
- **ToT vs CoT**: “CoT is walking one trail; ToT is exploring a trail map with forks and backtracking.”
- **ReAct**: “Like playing a text adventure: you alternate between planning and taking a move based on the new room description.”
- **Reflexion**: “Like keeping a lab notebook of mistakes so the next experiment avoids the same failure mode.”

---

## Common Misconceptions (Required)

1) **“Chain-of-thought means the model is guaranteed to reason correctly.”**  
   - Why wrong: CoT is just a prompting/decoding pattern; it can still hallucinate steps or make arithmetic slips. Empirically, ToT can massively outperform CoT on search tasks (Game of 24: CoT 4.0% vs ToT BFS b=5 74%).  
   - Correct model: CoT increases *token budget for decomposition* but remains a single sampled path; reliability often needs sampling (SC) or search (ToT) or tool feedback (ReAct).

2) **“Self-consistency picks the ‘best reasoning’ by scoring rationales.”**  
   - Why wrong: SC (as defined) **marginalizes out reasoning paths** and selects the most frequent final answer via majority vote; it does not require a separate verifier/reranker.  
   - Correct model: SC is a *self-ensemble*: sample many \((r_i,a_i)\), then vote on \(a_i\).

3) **“ReAct always helps because adding thoughts makes actions smarter.”**  
   - Why wrong: ReflAct reports that thoughts strongly reweight action distributions (entropy drop 1.23 → 0.30), so **bad/un-grounded thoughts can mislead** and introduce unique failures; ReAct is not monotonic improvement.  
   - Correct model: ReAct is powerful when thoughts stay grounded in observations/tools; reflection that explicitly tracks goal–state (ReflAct) can reduce failure modes.

4) **“Tree of Thoughts is just ‘sample more’ like best-of-N.”**  
   - Why wrong: ToT is not only sampling; it adds **explicit state evaluation** (value/vote) and **search control** (BFS/DFS, pruning, backtracking). Best-of-N lacks structured backtracking and stateful selection across steps.  
   - Correct model: ToT is *search over partial solutions* with heuristics, not just multiple independent full solutions.

5) **“SELF-REFINE and Reflexion are the same thing.”**  
   - Why wrong: SELF-REFINE is an **intra-attempt** iterative draft→feedback→refine loop; Reflexion is **inter-attempt** learning where reflections are stored in memory and used in later trials.  
   - Correct model: SELF-REFINE improves a single output iteratively; Reflexion improves an agent across retries by accumulating experience summaries.

---

## Worked Examples

### Example A — Self-Consistency majority vote (minimal runnable Python)
Use when a student asks “how do I implement SC voting?”

```python
from collections import Counter

def self_consistency_vote(final_answers):
    """
    final_answers: list[str] of a_i from sampled CoT outputs (r_i, a_i)
    returns: (best_answer, counts)
    """
    counts = Counter(final_answers)
    best = counts.most_common(1)[0][0]
    return best, counts

# Example: 8 sampled solutions produced these final answers
answers = ["42", "41", "42", "42", "40", "42", "41", "42"]
best, counts = self_consistency_vote(answers)
print(best)    # "42"
print(counts)  # Counter({'42': 5, '41': 2, '40': 1})
```

Tutor notes:
- Map this directly to \(a^*=\arg\max_a \sum_i \mathbf{1}(a_i=a)\) (Wang et al., 2022).
- If the student asks “how many samples?”: paper commonly uses **40** samples.

---

### Example B — ToT BFS skeleton (search loop structure)
Use when a student asks “what’s the actual ToT loop?”

```python
def tot_bfs(initial_state, propose, value, breadth_b=5, depth_D=3):
    """
    initial_state: s0
    propose(s) -> list of candidate thoughts t
    value(s) -> numeric heuristic V(s)
    """
    frontier = [initial_state]
    for _depth in range(depth_D):
        candidates = []
        for s in frontier:
            for t in propose(s):
                s2 = s.add_thought(t)   # state transition: s' = s + t
                candidates.append((value(s2), s2))
        # keep top-b by heuristic value
        candidates.sort(key=lambda x: x[0], reverse=True)
        frontier = [s for _, s in candidates[:breadth_b]]
    # return best final state
    return max(frontier, key=value)
```

Tutor notes grounded in ToT paper:
- “State = input + thoughts so far.”
- Evaluation can be **value** or **vote**; BFS keeps top \(b\) states per depth.
- Empirical anchor: Game of 24 jumps to **74%** with BFS \(b=5\) (GPT-4, temp=0.7).

---

### Example C — SELF-REFINE loop (prompt-role separation)
Use when a student asks “how do I structure prompts for self-correction?”

Pseudo-structure (from equations in SELF-REFINE):
1. `p_gen || x` → draft \(y_0\)
2. `p_fb || x || y_t` → feedback \(fb_t\)
3. `p_refine || x || y_t || fb_t` → refined \(y_{t+1}\)
4. Stop when feedback indicates done or after **max 4** iterations.

Key tutor move: emphasize feedback must be **specific/actionable** (paper reports generic feedback reduces performance).

---

## Comparisons & Trade-offs

| Technique | Core mechanism | Strengths (per sources) | Common failure mode / cost | When to choose |
|---|---|---|---|---|
| CoT | Single sampled intermediate steps | Helps decomposition; emergent gains at scale (Wei et al.) | Still single-path; can lock into wrong path | Simple multi-step reasoning where one path is usually enough |
| Self-Consistency | Sample many CoT paths + majority vote | Large accuracy gains (e.g., GSM8K +17.9) without training | More tokens/latency (e.g., 40 samples) | When you can afford extra inference cost for reliability |
| ReAct | Interleave reasoning + actions/tools | Reduces hallucination via tool interaction; interpretable trajectories (Yao et al.) | Ungrounded thoughts can mislead actions (ReflAct finding) | Interactive tasks needing retrieval/tool use and stepwise control |
| ToT | Search over thought tree with value/vote + BFS/DFS | Big gains on search/planning tasks (Game of 24: 74% with BFS b=5) | More orchestration complexity; evaluator quality matters | Problems with branching, backtracking, or multiple plausible partial solutions |
| SELF-REFINE | Draft→feedback→refine iterations | Strong improvements without extra models/training | Iteration cost; feedback quality critical | Writing/code improvement where iterative editing works well |
| Reflexion | Reflection memory across trials | Improves success across retries (AlfWorld 130/134; HumanEval 0.91) | Needs evaluator signal + memory management | When repeated attempts are allowed and learning from failure matters |

---

## Prerequisite Connections

- **Sampling vs greedy decoding (temperature/top-p).** Needed to understand why SC and ToT rely on *diverse samples* rather than deterministic outputs (SC defaults use temperature sampling).
- **Search concepts (BFS/DFS, pruning, backtracking).** Needed to understand ToT’s explicit tree search control loop.
- **Tool-use / environment feedback loops.** Needed to understand ReAct-style interleaving and why observations ground reasoning.
- **Prompt roles / prompt chaining.** Needed to understand SELF-REFINE’s separation into generation/feedback/refine prompts and iterative prompting patterns.

---

## Socratic Question Bank

1) **If you sample 40 CoT solutions and get 3 different final answers, what would SC do—and what does the vote distribution tell you?**  
Good answer: pick the majority answer via the argmax vote; distribution indicates agreement/confidence proxy.

2) **Describe a task where linear CoT is likely to fail but ToT would help. What property of the task makes branching/backtracking necessary?**  
Good answer: tasks with many forks/partial solutions (e.g., Game of 24, crosswords); need to explore alternatives.

3) **In ReAct, why might adding a “thought” ever make performance worse?**  
Good answer: thought reweights action distribution; ungrounded thought biases actions (ReflAct entropy evidence).

4) **What’s the difference between SELF-REFINE and Reflexion in terms of *where learning happens*?**  
Good answer: SELF-REFINE iterates within one output; Reflexion stores reflections across trials in memory.

5) **What does ToT call a “state,” and why is that definition useful for search?**  
Good answer: state = input + thoughts so far; enables evaluation and selection of partial solutions.

6) **If you had a strict latency budget, which would you drop first: SC sampling, ToT breadth, or reflection iterations—and why?**  
Good answer: trade off extra samples/branches/iterations vs reliability; justify with cost.

7) **How would you design a value prompt vs a vote prompt for ToT evaluation? What’s the difference in what they output?**  
Good answer: value outputs scalar/labels per state; vote compares a set and selects best.

8) **What kind of feedback signal does Reflexion need to be effective, and what happens if it’s too sparse or noisy?**  
Good answer: needs evaluator reward/heuristic; too sparse/noisy makes reflections less actionable.

---

## Likely Student Questions

**Q: What is the exact self-consistency selection rule?**  
→ **A:** Wang et al. define SC as sampling \(m\) outputs \((r_i,a_i)\) and selecting the answer by majority vote: \(a^*=\arg\max_{a}\sum_{i=1}^{m}\mathbf{1}(a_i=a)\) (Wang et al., 2022).

**Q: How many samples does self-consistency typically use in the paper?**  
→ **A:** The self-consistency paper commonly uses **40 sampled outputs** per run and reports results averaged over **10 runs** (Wang et al., 2022).

**Q: What’s the concrete ToT loop—what are the steps?**  
→ **A:** ToT is an explicit search loop: represent a **state** as input + thoughts so far; **generate** candidate next thoughts; **evaluate** states via a value prompt \(V(s)\) or a vote prompt; then **search** using BFS (keep top \(b\) states per depth) or DFS (prune when \(V(s)\) below threshold and backtrack) (Yao et al., 2023).

**Q: How much better is ToT than CoT on a real benchmark?**  
→ **A:** On Game of 24 (100 hard games, GPT-4, temp=0.7), CoT is **4.0%** while ToT BFS with breadth **b=5** is **74%** (Yao et al., 2023).

**Q: What are the SELF-REFINE equations / roles?**  
→ **A:** SELF-REFINE uses one model \(M\): \(y_0=M(p_{gen}\|x)\); \(fb_t=M(p_{fb}\|x\|y_t)\); \(y_{t+1}=M(p_{refine}\|x\|y_t\|fb_t)\), iterating until stop or **max 4 iterations** (Madaan et al., 2023).

**Q: How is Reflexion different from just retrying?**  
→ **A:** Reflexion converts feedback/reward plus the trajectory into **verbal self-reflections** stored in an episodic memory buffer (often **1–3 experiences**) and conditions future trials on that memory—improving without weight updates (Shinn et al., 2023).

**Q: Does ReAct always help compared to not thinking?**  
→ **A:** Not necessarily; ReflAct reports that adding thoughts (ReAct) strongly changes action distributions (entropy **1.23 → 0.30** on ALFWorld for Llama-3.1-8B-Instruct), so ungrounded thoughts can mislead; their goal–state reflection approach improves success vs ReAct across multiple models (Zhang et al., 2025).

**Q: Where can I see a concrete ToT implementation and what knobs matter?**  
→ **A:** The official repo https://github.com/arpg/tree-of-thought-llm includes a minimal Game of 24 script and key args like `method_generate` (sample/propose), `method_evaluate` (value/vote), `n_generate_sample`, `n_evaluate_sample`, and `n_select_sample` (breadth \(b\)).

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: the student needs systems-level intuition for what an LLM is and why agent loops (planning/tool use/memory) are built around it.
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Paper Explained)](https://youtube.com/watch?v=_YXnMBQjGDo) — Surface when: the student wants a paper-walkthrough of CoT and why intermediate steps help.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student asks for a unified view of planning, memory, tool use, reflection.
- [Lilian Weng — Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) — Surface when: student asks for CoT variants (SC, ToT) in one place.
- [LangGraph — Agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks how to implement agent/workflow orchestration with state, routing, and human-in-the-loop.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — Surface when: student asks for production-oriented primitives (agents, tools, handoffs, guardrails).
- [ReAct paper (arXiv)](https://arxiv.org/abs/2210.03629) — Surface when: student asks for the original definition and motivation for interleaving reasoning and acting.

---

## Visual Aids

![Tree of Thoughts explores branching reasoning paths beyond linear CoT. (Yao et al. 2022)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-03-15-prompt-engineering_002.png)  
Show when: student is stuck on “how is ToT different from CoT/self-consistency?”—use to point at branching + evaluation + selection.

![Generative agent architecture: memory, reflection, and planning modules. (Park et al. 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_012.png)  
Show when: student asks how reflection fits into an agent system (memory stream → reflection → planning).

---

## Key Sources

- [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601) — Defines ToT states/thoughts, value/vote evaluation, BFS/DFS with pruning/backtracking, and reports large benchmark gains.
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) — Defines sample-and-marginalize voting rule and reports consistent accuracy gains with concrete sampling defaults.
- [SELF-REFINE: Iterative Refinement with Self-Feedback](https://arxiv.org/pdf/2303.17651.pdf) — Provides explicit generate/feedback/refine equations, stopping criteria, and iteration defaults.
- [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) — Formalizes reflection-as-memory across trials and reports improvements on AlfWorld/HotPotQA/HumanEval.
- [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) — Original definition/motivation for interleaving reasoning traces with actions/tools.