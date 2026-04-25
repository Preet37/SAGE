---
title: "Agent Fundamentals"
subject: "Agents & Reasoning"
date: 2025-01-01
tags:
  - "subject/agents-and-reasoning"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Lilian Weng"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Agent Fundamentals

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- Why: While not exclusively about agents, Karpathy's treatment of LLMs as the cognitive core of agents, including tool use, memory, and autonomous action loops, provides the clearest conceptual foundation for understanding why LLM agents work the way they do. His systems-level thinking maps directly onto agent architecture concepts.
- Level: beginner/intermediate

> Karpathy's video is well-known and covers LLM systems thinking that maps to agent architecture concepts. No single YouTube video from the preferred educators focuses exclusively on agent fundamentals with full depth.

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM Powered Autonomous Agents"
- **Link:** [https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Why: This is the canonical written reference for LLM agent fundamentals. Weng systematically covers the four pillars — planning, memory, tool use, and action — with clear diagrams and concrete examples. It introduces ReAct, Plan-and-Execute, reflection, and self-correction in a single coherent framework. Widely cited in both academic and practitioner communities.
- Level: intermediate

## Deep dive
- **LangGraph / LangChain** — "LangGraph Conceptual Documentation: Agents"
- **Link:** [https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/)
- Why: Provides the most thorough technical treatment of agent loops, orchestration patterns, state management, and multi-agent coordination as actually implemented in production systems. Covers the agent loop, reactivity vs. proactivity, and orchestration patterns (supervisor, hierarchical) with code-grounded explanations. Directly relevant to LangGraph, CrewAI-style patterns, and the OpenAI Agents SDK mental model.
- Level: intermediate/advanced

## Original paper
- **Yao et al., 2022** — "ReAct: Synergizing Reasoning and Acting in Language Models"
- **Link:** [https://arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)
- Why: ReAct is the most readable and foundational paper for understanding the agent loop as a concrete algorithmic pattern. It introduces the interleaving of reasoning traces and actions that underpins virtually every modern LLM agent framework (LangGraph, AutoGen, CrewAI, OpenAI Agents SDK). Short, well-structured, and directly teachable.
- Level: intermediate

## Code walkthrough
- **OpenAI** — "OpenAI Agents SDK Quickstart / Cookbook"
- **Link:** [https://openai.github.io/openai-agents-python/](https://openai.github.io/openai-agents-python/)
- Why: The OpenAI Agents SDK (released 2025) provides the cleanest minimal implementation of the agent loop — tools, handoffs, guardrails — with official documentation and runnable examples. It is pedagogically superior to older LangChain agent examples because the abstractions are simpler and the code more readable for learners encountering agents for the first time.
- Level: beginner/intermediate

> **Alternative if above unverified:** The [LangGraph "Build a Basic Agent" tutorial](https://langchain-ai.github.io/langgraph/tutorials/introduction/) is a well-maintained, beginner-friendly code walkthrough covering the agent loop with explicit state graphs.

---

## Coverage notes
- **Strong:** Written/blog coverage is excellent — Lilian Weng's post is genuinely one of the best educational resources in the entire ML ecosystem for this topic.
- **Strong:** Paper coverage is strong; ReAct is short, readable, and directly maps to practitioner frameworks.
- **Weak:** Video coverage from top educators (Karpathy, 3Blue1Brown, Yannic Kilcher) does not yet include a dedicated, comprehensive agent-fundamentals explainer. Most videos either treat agents superficially or focus on a specific framework rather than the underlying concepts.
- **Gap:** No single video cleanly covers the full conceptual stack: agent loop → goal-directed behavior → reactivity/proactivity → reflection → orchestration patterns. This is a genuine content gap in the preferred educator tier.
- **Gap:** AutoGen and CrewAI specifically lack deep-dive pedagogical resources from authoritative educators; most content is vendor documentation or low-quality tutorial blogs.
- **Emerging:** The OpenAI Agents SDK (2025) is too new for mature third-party educational content; official docs are currently the best available source.

---

---

## Additional Resources for Tutor Depth

> **11 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Reflexion loop (verbal RL via self-reflection + memory)
**Paper** · [source](https://arxiv.org/abs/2303.11366)

*Reflexion loop definition (trial → self-reflection → memory update → next attempt), objective framing, key ablations/results*

<details>
<summary>Key content</summary>

- **Core idea (Abstract, Sec. 1, 3):** Improve an LLM agent **without weight updates** by converting environment feedback (binary/scalar or free-form) into **verbal self-reflections** stored in an **episodic memory buffer** used as context in later trials (“semantic gradient”).
- **Modular formulation (Sec. 3):**  
  - **Actor** (LLM policy) generates text/actions conditioned on observation + memory `mem` (actors explored: **CoT**, **ReAct**).  
  - **Evaluator** scores a generated trajectory with reward `r_t` (exact match for QA; heuristics for decision-making; LLM-based evaluator also explored).  
  - **Self-Reflection model** (LLM) takes `(trajectory, sparse reward, mem)` → produces **verbal experience summary** `f_t`, appended to `mem`.
- **Reflexion process loop (Algorithm 1, Sec. 3):**  
  Trial `t`: Actor interacts → trajectory; Evaluator computes scalar reward `r_t`; Self-Reflection amplifies `{r_t}` + trajectory into textual feedback `f_t`; **memory update:** `mem ← mem ⊕ f_t`; repeat until Evaluator deems correct.  
  **Defaults:** bound long-term memory to **1–3 experiences** (often **3** for AlfWorld/HotPotQA; **1** for programming) to fit context limits.
- **Empirical results (Sec. 4):**
  - **AlfWorld:** ReAct+Reflexion completes **130/134** tasks; improves **+22% absolute** over strong baselines in **12** learning steps; baseline plateaus around trials **6–7**; heuristic triggers reflection if same action/response repeats **>3 cycles** or actions **>30**.
  - **HotPotQA:** **+20%** improvement; Reflexion enables retries until **3 consecutive failures**; ablation: self-reflection gives **+8% absolute** over episodic-memory-only.
  - **HumanEval (Python):** baseline **0.80** pass@1 → Reflexion **0.91** (paper notes surpassing GPT-4 0.80).  
  - **Rust ablation (50 hardest HumanEval RS):** Base **0.60**; no tests + reflection **0.52**; tests w/o reflection **0.60**; full Reflexion **0.68**.
- **Programming pipeline defaults (Sec. 4.3):** self-generate unit tests via CoT; AST-filter for syntactic validity; sample up to **6** tests; prefer false negatives over false positives.

</details>

### 📄 SELF-REFINE (Generate → Feedback → Refine loop)
**Paper** · [source](https://arxiv.org/pdf/2303.17651.pdf)

*Self-Refine algorithm loop + equations + stopping criterion + prompt roles*

<details>
<summary>Key content</summary>

- **Core idea (Sec. 1–2):** Use a *single* LLM \(M\) as generator, feedback provider, and refiner; no supervised training, no RL, no extra models.
- **Algorithm 1 (SELF-REFINE loop):**
  1) **Initial generation (Eq. 1):**  
     \[
     y_0 = M(p_{\text{gen}} \parallel x)
     \]
  2) For iterations \(t=0,1,\dots\):  
     **Feedback (Eq. 2):**  
     \[
     fb_t = M(p_{\text{fb}} \parallel x \parallel y_t)
     \]
     **Stop check:** break if \(stop(fb_t, t)\) is true (either max-iteration \(t\) or a stop indicator/score extracted from feedback; Sec. 2).  
     **Refine (Eq. 3 / instantiated as Eq. 4 with history):**  
     \[
     y_{t+1} = M(p_{\text{refine}} \parallel x \parallel y_t \parallel fb_t)
     \]
     \[
     y_{t+1} = M(p_{\text{refine}} \parallel x \parallel y_0 \parallel fb_0 \parallel \dots \parallel y_t \parallel fb_t)
     \]
  - **Notation:** \(x\)=input; \(y_t\)=draft at iteration \(t\); \(fb_t\)=feedback; \(\parallel\)=concatenation; prompts \(p_{\text{gen}}, p_{\text{fb}}, p_{\text{refine}}\) are task-specific few-shot templates.
- **Feedback design rationale (Sec. 2, Sec. 4):** Prompt feedback to be **actionable** (concrete improvement action) and **specific** (points to concrete phrases/issues). Generic/no feedback reduces performance (Table 2).
- **Defaults/parameters (Sec. 3.1):** Iterate until criterion met, **max 4 iterations**; greedy decoding with **temperature 0.7**.
- **Key empirical results (Table 1):** SELF-REFINE improves base LLMs across tasks (absolute gains shown):
  - Dialogue Response (GPT-4): **25.4 → 74.6** (**+49.2**)
  - Constrained Generation (ChatGPT): **44.0 → 67.0** (**+23.0**)
  - Code Optimization (GPT-4): **27.3 → 36.0** (**+8.7**)
  - Sentiment Reversal (ChatGPT): **11.4 → 43.2** (**+31.8**)
- **Iteration gains (Fig. 4):** Example average scores improve with iterations (diminishing returns): Constrained Gen **29.0 (y0) → 49.7 (y3)**.

</details>

### 📄 Tree of Thoughts (ToT) search/plan loop
**Paper** · [source](https://arxiv.org/abs/2305.10601)

*Explicit search/plan loop: thought expansion → evaluation → selection/backtracking (BFS/DFS), beyond single-path CoT/ReAct*

<details>
<summary>Key content</summary>

- **Problem-solving as tree search (Sec. 3):** represent a **state** as partial solution = *(input + sequence of thoughts so far)*; solve by searching a **tree of thoughts** (nodes=states, edges=next-thought operators).
- **Core ToT design questions (Sec. 3):**
  1) **Thought decomposition:** choose “thought” granularity (e.g., crossword word; equation line; writing plan paragraph). Must be small enough to sample diverse candidates, big enough to evaluate promise.  
  2) **Thought generation:** from state \(s\), generate candidate next thoughts \(t\) via prompting (often i.i.d. samples from a “propose” prompt).  
  3) **State evaluation (heuristic):** LM provides heuristic values:
     - **Value:** \(V(s)\) via a value prompt → scalar (1–10) or labels (e.g., sure/maybe/impossible) mapped to scores.
     - **Vote:** compare a set of states \(S\) and pick best via vote prompt; can sample multiple votes and aggregate.
  4) **Search algorithm:** plug in BFS or DFS.
- **BFS (Alg. 1):** maintain top \(b\) states per depth step; prune using evaluator; suited to shallow fixed-depth tasks.
- **DFS (Alg. 2):** expand most promising state until solved or evaluator says impossible (threshold); then **prune subtree and backtrack**; used for deeper variable-depth tasks.
- **Empirical results (Game of 24, Sec. 4.1, GPT-4, temp=0.7):**
  - IO 7.3%; CoT 4.0%; CoT-SC (k=100) 9.0%
  - ToT BFS **b=1: 45%**; **b=5: 74%**
  - IO+Refine (k=10): 27%; IO best-of-100: 33%; CoT best-of-100: 49%
- **Creative Writing (Sec. 4.2):** ToT depth=2 (plan→passage), breadth limit \(b=1\), **5 votes** each step. Avg GPT-4 coherency: ToT 7.56 vs IO 6.19 vs CoT 6.93; human prefs: ToT>CoT 41/100, CoT>ToT 21/100.
- **Crosswords (Sec. 4.3):** ToT uses DFS with pruning; constrain thoughts to not change filled letters; max ~10 steps; DFS step limit 100; backtracking ablation hurts.

</details>

### 📄 Voyager agent loop (curriculum + skill library + iterative prompting)
**Paper** · [source](https://arxiv.org/abs/2305.16291)

*Concrete agent architecture procedure: automatic curriculum, skill library, iterative prompting, and code/tool execution loop with explicit components*

<details>
<summary>Key content</summary>

- **Core architecture (Sec. 2; Fig. 2):** Voyager = (1) **Automatic curriculum** (task proposer), (2) **Skill library** (code memory), (3) **Iterative prompting mechanism** (generate→execute→repair loop with feedback + self-verification).
- **Agent loop (Fig. 2 / Sec. 2.3):**
  1) Curriculum (GPT-4) proposes next task given **ultimate goal** “discover as many diverse things as possible,” plus agent state + history.  
  2) Retrieve relevant skills from library (embedding search).  
  3) GPT-4 generates/edits **executable code** (program-as-action).  
  4) Execute code in environment → collect **environment feedback** + **execution errors**.  
  5) **Self-verification** (separate GPT-4 critic) checks success; if fail, returns critique.  
  6) Repeat code refinement until verified success; then **commit code as a new skill**; else if stuck **after 4 rounds**, abandon and request a new task.
- **Automatic curriculum prompt inputs (Sec. 2.1):** (i) directives/constraints (task not too hard), (ii) full agent state (inventory, equipment, nearby blocks/entities, biome, time, health/hunger, position), (iii) completed + failed tasks, (iv) extra context via **GPT-3.5 self-ask/self-answer** (used for budget).
- **Skill library mechanics (Sec. 2.2):** store each skill as **executable code**; index by **embedding of its description**; retrieve using embedding of self-generated plans + environment feedback; encourages **compositional** skill building and mitigates catastrophic forgetting.
- **Iterative prompting feedback types (Sec. 2.3):** (1) environment feedback (e.g., missing ingredients), (2) interpreter error traces, (3) self-verification success check + critique.
- **Defaults/parameters (Sec. 3.1):** models: **gpt-4-0314** (code/curriculum/verification), **gpt-3.5-turbo-0301** (NLP self-ask), embeddings: **text-embedding-ada-002**; temperatures: **0** for all except curriculum **0.1**.
- **Empirical results (Sec. 3.3):** within **160 prompting iterations**, Voyager discovers **63 unique items**; Voyager is **the only method** to unlock **diamond** tech-tree level; skill library enables **zero-shot generalization** in a new world (Voyager solves all tested tasks; baselines fail within **50 iterations**).

</details>

### 📊 A3T (ActRe + ReAct) Closed-Loop Self-Improving Agents on AlfWorld/WebShop
**Benchmark** · [source](https://arxiv.org/html/2403.14589v3)

*Reported success rates on AlfWorld/WebShop (1-shot + iterative rounds), plus training loop + key ablations*

<details>
<summary>Key content</summary>

- **Core idea (Sec. 2.1):** Autonomous Annotation of Agent Trajectories (A3T) pairs a **ReAct** policy agent (reason→act) with an **ActRe** prompting agent (act→reason). When the policy **randomly samples an external action** \(a_t'\), it queries ActRe to generate a posterior rationale \(r_t'\), forming a synthetic ReAct step \((o_t, r_t', a_t')\). Environment terminal reward labels trajectory success.
- **Policy gradient objective (Eq. 1):** maximize  
  \[
  \sum_{\tau\in\mathcal{D}} s(\tau)\sum_{t}\log p_\theta(x_t\mid x_{<t})
  \]
  where \(\tau\) is a trajectory; \(x_t\) are token strings including observations and agent outputs (reasoning or actions); \(s(\tau)\) is trajectory score/reward; \(p_\theta\) is the fine-tuned LLM. They **keep world-modeling tokens** (observations) in the likelihood term.
- **Contrastive structuring (Eq. 2):** for a task with successful \(\tau^+\) and failed \(\tau^-\), objective becomes SFT on successes + likelihood contrast between \(\tau^+\) and \(\tau^-\). **Binarize failed rewards** with \(s(\tau^-)=0\); require multiple successes per task to avoid instability (Remark 3).
- **Defaults / hyperparams (Appx A):** exploration probability \(p=0.1\); if **3 consecutive invalid actions**, force resample + ActRe rationale. AlfWorld: collect **40 trajectories** per failed task. WebShop: force **3 trajectories**, stop at first success or cap **20**. Training: **QLoRA** on **Mistral-7B-Instruct-v0.2**; LoRA rank **16**, alpha **32**; tune **q_proj/v_proj** only; **nf4** quantization; optimizer **paged AdamW 32-bit**; LR **1e-4**; epochs: **10** (Round 0), **6** (Rounds 1–3) + checkpoint averaging. Round 0 bootstraps with **1-shot ReAct prompting** (gpt-3.5-turbo-instruct-0914); ActRe uses **gpt-3.5-turbo-instruct-0914**.
- **Empirical results (Sec. 3):**
  - **AlfWorld:** **1-shot success 96%**; **100% success with 4 iterative rounds**. Round totals on held-out unseen: **82 → 99 → 100 → 100** (Rounds 0–3).
  - **WebShop:** **1-shot success 49.0%** (human avg **50.0%**); after **4-shot iterative refinement: 54.8%** (human experts **59.6%**). Across rounds (Table 6): success **40.0 → 61.1 → 69.4 → 73.9** with reward \(R\) **68.5 → 85.2 → 88.9 → 90.6**.
- **Ablation takeaways (Sec. 4.1/Table 7):** policy gradient > supervised variants; **binarized rewards** improve success vs using original real-valued rewards; best filtering uses reward threshold **\(r=1\)** (success-only) for training trajectories.

</details>

### 📊 ReflAct (Goal–State Reflection) Benchmark Results
**Benchmark** · [source](https://arxiv.org/abs/2505.15182v2)

*Benchmark tables + ablations showing iterative/reflective backbone gains (ALFWorld/ScienceWorld/Jericho) and comparisons vs ReAct + modules (Reflexion, WKM)*

<details>
<summary>Key content</summary>

- **Agent-as-POMDP (Section 2):** Task as POMDP \((\mathcal{S},\mathcal{A},\mathcal{O},T,R)\) with natural-language instruction \(x\), hidden state \(s\), action \(a\), observation \(o\).  
  **ReAct loop:** at time \(t\), context \(c_t\) (history) → sample thought \(\tau_t \sim p(\tau \mid c_t)\); append to form \(\tilde c_t=[c_t;\tau_t]\) → action \(a_t \sim \pi(a\mid \tilde c_t)\) → observe \(o_{t+1}\).
- **Thought affects action distribution (Section 3.1):** entropy over action distribution across 134 ALFWorld tasks (Llama-3.1-8B-Instruct):  
  NoThinking mean entropy **1.23** vs ReAct **0.30** (Table 1) → thoughts strongly “reweight” actions; bad thoughts can mislead.
- **ReflAct rationale (Sections 1,4):** ReAct failures from (i) **ungrounded internal state** and (ii) **short-sighted planning**; ReflAct replaces “next-action thinking” with **continuous reflection on agent state in relation to task goal** each step (explicit belief-state + goal in reflection).
- **Core objective (Section 4):** maximize expected long-term return \(G=\sum_t \gamma^t r_t\); “optimal thought” defined as one maximizing expected return when conditioning policy on \([c;\text{thought}]\).
- **Main benchmark results (Table 2):**  
  - **GPT-4o:** ReflAct ALFWorld **93.3** vs ReAct **85.1**; avg **61.6** vs **56.0**.  
  - **GPT-4o-mini:** ReflAct ALFWorld **66.4** vs ReAct **53.0**; avg **44.8** vs **36.8**.  
  - **Llama-3.1-8B:** ReflAct ALFWorld **60.5** vs ReAct **29.1**; avg **34.4** vs **22.5**.  
  - **Llama-3.1-70B:** ReflAct avg **56.1** vs ReAct **48.9**.
- **Modules/iterations:** Reflexion applied for **3 trials**; even then, NoThinking/ReAct+Reflexion < **ReflAct trial 0**; GPT-4o ReflAct+Reflexion reaches **94.8%** ALFWorld (Section 6.3.1). WKM improves ReAct but still < ReflAct; replacing thought with external “state knowledge” **degrades** (Section 6.3.2).
- **Safety-style finding (Section 6.4.1):** On 134 ALFWorld tasks, **no tasks where only ReflAct fails**; ReAct introduces unique failures.

</details>

### 📖 AutoGen 0.2 AgentChat API—core knobs & orchestration entry points
**Reference Doc** · [source](https://microsoft.github.io/autogen/0.2/docs/reference/)

*Cross-class defaults/knobs beyond `ConversableAgent` (multi-agent orchestration, tool/code execution utilities, termination/turn limits)*

<details>
<summary>Key content</summary>

- **Agent definition (conceptual contract):** In AutoGen, an *agent* is an entity that can **send messages**, **receive messages**, and **generate a reply** using **models, tools, human inputs, or mixtures**.
- **Built-in agent baseline:** `ConversableAgent` supports configurable components including:
  - **List of LLMs** via `llm_config`
  - **Function/tool executor**
  - **Human-in-the-loop component**
  - Extensibility via `registered_reply` (add custom reply behaviors/components).
- **Key configuration defaults/knobs shown:**
  - `code_execution_config=False` → code execution **off** (example explicitly notes default off).
  - `human_input_mode="NEVER"` → fully autonomous (never asks user for input).
  - `llm_config={"config_list":[{"model":"gpt-4","api_key":...}]}` → canonical multi-config pattern.
- **Core procedures (agent loop entry points):**
  - Single-turn reply: `generate_reply(messages=[{"role":"user","content":...}])`
  - Multi-turn agent-to-agent chat: `initiate_chat(other_agent, message=..., max_turns=2)` (example uses `max_turns=2` to cap dialogue length).
- **Code execution utilities (executors):**
  - Local: `autogen.coding.LocalCommandLineCodeExecutor(work_dir="coding")`
  - Docker (context-managed): `with autogen.coding.DockerCommandLineCodeExecutor(work_dir="coding") as code_executor: ...`
  - Passed into `UserProxyAgent(..., code_execution_config={"executor": code_executor})`
- **Design rationale (stated):** Multi-agent conversations simplify **orchestration/automation/optimization** of complex LLM workflows; modular components enable composability and maintainability.

</details>

### 📖 AutoGen ConversableAgent knobs (init + reply loop)
**Reference Doc** · [source](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/conversable_agent/)

*`ConversableAgent.__init__` signature + defaults; `human_input_mode`; `MAX_CONSECUTIVE_AUTO_REPLY` behavior; default reply-function order*

<details>
<summary>Key content</summary>

- **Core behavior (agent loop):** After receiving each message, agent sends a reply unless message is a termination message. Override `generate_reply()` to change auto-reply behavior.
- **Constructor signature + defaults:**
  - `__init__(name, system_message="You are a helpful AI Assistant.", is_termination_msg=None, max_consecutive_auto_reply=None, human_input_mode="TERMINATE", function_map=None, code_execution_config=False, llm_config=None, default_auto_reply="", description=None, chat_messages=None, silent=None)`
  - `description` default: `system_message`.
  - `llm_config`: `None` ⇒ uses `self.DEFAULT_CONFIG` (defaults to `False`); `False` disables LLM-based auto reply.
  - `code_execution_config=False` disables code execution; if dict: keys include `work_dir`, `use_docker` (default `True`), `timeout`, `last_n_messages` (default `"auto"`).
- **Consecutive auto-reply limit (Eq. 1):**
  - Let `N = max_consecutive_auto_reply`.
  - If `N is None`: use class attribute `MAX_CONSECUTIVE_AUTO_REPLY` as limit.
  - If `N = 0`: **no auto reply** generated.
- **Human input modes (procedural rules):**
  - `"ALWAYS"`: prompt human every received message; stop if human input is `"exit"` OR (`is_termination_msg` true and no human input).
  - `"TERMINATE"` (default): prompt human only on termination msg OR when auto-reply count reaches `N`.
  - `"NEVER"`: never prompt; stop when auto-reply count reaches `N` OR `is_termination_msg` true.
- **Default reply-function chain (order matters):**
  1) `check_termination_and_human_reply` → 2) `generate_function_call_reply` (deprecated) → 3) `generate_tool_calls_reply` → 4) `generate_code_execution_reply` → 5) `generate_oai_reply`.  
  Each returns `(final, reply)`; if `final=False`, continue to next.

</details>

### 📖 CrewAI Agent/Crew/Flow Fundamentals (repo + docs entrypoints)
**Reference Doc** · [source](https://github.com/crewAIInc/crewAI)

*Authoritative surfaces for creating Agents/Tasks/Crews, selecting process modes, and orchestrating Crews inside Flows; install/run defaults and telemetry controls.*

<details>
<summary>Key content</summary>

- **Install / environment**
  - Requires **Python >= 3.10 and < 3.14**.
  - Install: `uv pip install crewai`; optional tools: `uv pip install 'crewai[tools]'`; embeddings/tiktoken fix: `uv pip install 'crewai[embeddings]'`.
  - Default model connection: **OpenAI API by default** (set `OPENAI_API_KEY`); other LLMs via docs “LLM Connections” (e.g., local models).
- **Project scaffold (CLI procedure)**
  - Create: `crewai create crew <project_name>` → generates `src/<project>/main.py`, `crew.py`, `config/agents.yaml`, `config/tasks.yaml`, `tools/`.
  - Run: `crewai run` or `python src/<project>/main.py`. Dependency ops: `crewai install` (optional), `crewai update` if poetry-related error.
- **Core orchestration parameters (shown in examples)**
  - `Crew(agents=[...], tasks=[...], process=Process.sequential, verbose=True)`  
  - Process modes mentioned: **sequential** and **hierarchical** (hierarchical “assigns a manager” for planning/delegation/validation).
  - `Task(description="... {var} ...", expected_output="...", agent=<Agent>, output_file="report.md")`
  - `Crew.kickoff(inputs={...})` passes named template variables into task descriptions.
- **Flows: event-driven control + conditions**
  - Decorators: `@start`, `@listen`, `@router`; logical combinators: `or_(...)`, `and_(...)`.
  - Pattern: Flow step returns dict matching task template vars; later step runs a Crew and routes based on state.
- **Empirical comparison (repo claim)**
  - CrewAI Flows reported **5.76× faster** than LangGraph in a QA task example (linked notebook).
- **Telemetry defaults/control**
  - Anonymous telemetry collects: CrewAI/Python versions, OS/CPU class, #agents/#tasks, process type, whether memory/delegation used, parallel vs sequential, model used, roles, tool names.
  - Disable via env var: `OTEL_SDK_DISABLED=true`. Opt-in detailed telemetry: `Crew(share_crew=True)`.

</details>

### 🔍 Multi-tool orchestration objective + production tradeoffs
**Explainer** · [source](https://arxiv.org/html/2603.22862v2)

*Production-oriented architecture/process discussion for reliable, efficient multi-tool agents (cost/latency vs robustness/safety)*

<details>
<summary>Key content</summary>

- **Problem formulation (Section 2):** Multi-tool instance includes task/query, interactive environment with latent state \(s_t\) and observation \(o_t\), and tool inventory \(\mathcal{T}\) with schemas. Tool execution interface:  
  \[
  \text{Exec}(t, x)\rightarrow (y, s')
  \]
  where \(t\) is tool, \(x\) valid arguments, \(y\) feedback (JSON/text/error), \(s'\) post-call state.
- **History + memory:** interaction history up to time \(t\): \(h_t=\{(a_i,f_i)\}_{i=1}^{t}\). Internal memory \(m_t\) updated from history (e.g., scratchpad summary / retrieved records).
- **Agent policy + actions:** at step \(t\), choose action \(a_t\) (tool call \((t,x)\) or terminate with final answer \(r\)); policy conditions on history+memory: \(\pi_\theta(a_t\mid h_t,m_t)\).
- **Trajectory + cost-aware objective (Section 2):** trajectory \(\tau=(h_T,m_T)\) with variable horizon \(T\). Generic objective trades off success vs cost:  
  \[
  \max_\theta\ \mathbb{E}_{\tau\sim \pi_\theta}\big[ R(\tau)-\lambda\, C(\tau)\big]
  \]
  where \(C(\tau)\) can include **#tool calls, latency, API fees, risk**.
- **Design rationale (Sections 3,5,6):**
  - Shift from **single-call correctness** to **end-to-end executability/robustness** over long horizons with feedback, re-planning, and state mutation.
  - **Parallelism** reduces latency but write-tools introduce **race conditions/state inconsistency** → need dependency-aware scheduling + transaction/rollback ideas (e.g., bounded workflows, delayed commit/compensation).
  - Efficiency levers: **dynamic tool retrieval (Top‑K)** to avoid “Lost in the Middle”; **adaptive model routing/cascades**; **caching/memory** to reduce repeated attempts.

</details>

### 🔍 Production agent architecture & deployment tradeoffs
**Explainer** · [source](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

*Concrete architecture guidance for production agents (tools, orchestration, evaluation/monitoring, guardrails) + latency/cost vs reliability tradeoffs*

<details>
<summary>Key content</summary>

- **Definition (What is an agent):** “Agents are systems that independently accomplish tasks on your behalf.” Key characteristics:  
  1) **LLM controls workflow execution** (decides, recognizes completion, can proactively correct; on failure can **halt + transfer control to user**).  
  2) **Tool access** to gather context + take actions; **dynamic tool selection** within **guardrails**. (Sec. “What is an agent?”)
- **When to build an agent (use-case filter):** prioritize workflows that resisted deterministic automation:  
  - **Complex decision-making** (e.g., refund approval)  
  - **Difficult-to-maintain rules** (e.g., vendor security reviews)  
  - **Heavy unstructured data** (e.g., insurance claim processing) (Sec. “When should you build an agent?”)
- **Core components (architecture):** **Model + Tools + Instructions** (Sec. “Agent design foundations”).
- **Model selection procedure (latency/cost vs accuracy):**  
  1) **Set up evals** to establish a **performance baseline**  
  2) Start with **most capable model** for all tasks  
  3) **Swap in smaller/faster models** where acceptable to optimize **cost + latency** (Sec. “Selecting your models”).
- **Tool taxonomy:** **Data tools** (retrieve context), **Action tools** (write/execute changes), **Orchestration tools** (agents as tools). Standardize + document + test tools for reuse/versioning. (Sec. “Defining tools”)
- **Agent loop / run exit conditions (Agents SDK):** `Runner.run()` loops until either:  
  1) **final-output tool** invoked (specific output type), or  
  2) model returns a response **without tool calls**. (Sec. “Single-agent systems”)
- **Orchestration defaults:** start **single-agent**, add tools incrementally; move to **multi-agent** when:  
  - **Complex logic** (many if/then branches)  
  - **Tool overload** due to overlapping/similar tools (note: some succeed with **>15 distinct tools**, others struggle with **<10 overlapping**). (Sec. “When to consider creating multiple agents”)
- **Multi-agent patterns:**  
  - **Manager (agents as tools):** one manager delegates via tool calls; best when one agent should control workflow + user interaction.  
  - **Decentralized handoffs:** peer agents transfer control; good for **triage**. (Sec. “Multi-agent systems”)
- **Guardrails + human intervention triggers:**  
  - Layer guardrails: **(1) data privacy/content safety**, **(2) add based on real failures**, **(3) optimize security + UX**.  
  - **Risk-rate tools** (low/medium/high) using: read vs write, reversibility, permissions, financial impact; use ratings to **pause checks** or **escalate**.  
  - Human intervention triggers: **exceeding failure thresholds** (retry/action limits) and **high-risk actions** (e.g., cancel orders, large refunds, payments). (Guardrails section)

</details>

---

## Related Topics

- [[topics/function-calling|Function Calling]]
- [[topics/agent-memory|Agent Memory]]
- [[topics/agent-skills-safety|Agent Skills & Safety]]
- [[topics/multi-agent-systems|Multi-Agent Systems]]
- [[topics/prompting|Prompting]]
- [[topics/agent-workflows|Agent Workflows]]
- [[topics/agentic-coding|Agentic Coding]]
