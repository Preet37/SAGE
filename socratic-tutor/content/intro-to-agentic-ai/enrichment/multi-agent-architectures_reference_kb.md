## Core Definitions

**Multi-agent system (MAS).** A multi-agent system is an approach where multiple agents (often LLM-driven) collaborate to accomplish tasks, enabling specialization and parallel work. As described in the LangGraph tutorial, the focus is on *agent orchestration* for “long-running, stateful agents,” emphasizing durable execution, streaming, and human-in-the-loop control rather than a single monolithic prompt-response loop (LangGraph docs: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi_agent_collaboration/).

**Agent role (specialization).** An agent role is a scoped responsibility assigned to an agent (e.g., auditing data, extracting a field, reviewing a draft) so the overall system can divide labor. In the HLER pipeline, roles are explicitly separated (e.g., `DataAuditAgent`, `DataProfilingAgent`, `EconometricsAgent`, `PaperAgent`, `ReviewerAgent`) and their outputs are stored as structured objects passed forward (HLER paper: https://arxiv.org/html/2603.07444v1).

**Supervisor / orchestrator pattern.** A supervisor (or orchestrator) is a central controller that dispatches tasks to specialized agents and maintains shared state across steps. In HLER, a central orchestrator dispatches tasks and maintains a shared `RunState` that records intermediate outputs (HLER paper: https://arxiv.org/html/2603.07444v1). In the SEC filing benchmark, the “hierarchical supervisor-worker” design has a supervisor that maintains a task queue and reassigns low-confidence fields (SEC benchmark: https://arxiv.org/pdf/2603.22651.pdf).

**Hierarchical teams.** A hierarchical multi-agent architecture organizes agents into layers (e.g., supervisor → workers → verifier), where higher-level agents allocate work and enforce quality thresholds. The SEC benchmark defines a hierarchical supervisor-worker architecture with a confidence threshold (0.85) and bounded re-extraction iterations (max 2) (https://arxiv.org/pdf/2603.22651.pdf).

**Peer-to-peer (P2P) collaboration.** Peer-to-peer collaboration is a coordination style where agents interact as equals (no single fixed supervisor), negotiating task division and integrating results through conversation patterns. AutoGen frames multi-agent applications as “multiple agents that can converse with each other to accomplish tasks,” where interaction behaviors can be programmed in natural language or code (AutoGen paper: https://arxiv.org/abs/2308.08155).

**Debate and consensus.** Debate/consensus is a coordination mechanism where multiple agents propose competing answers and a merge/verifier process resolves disagreements (e.g., voting, confidence weighting, or rule-based consistency checks). In the SEC benchmark’s parallel fan-out + merge architecture, conflicts are resolved via **confidence-weighted voting**; in the reflexive architecture, a verifier checks formatting, cross-field consistency, and source grounding with bounded correction loops (https://arxiv.org/pdf/2603.22651.pdf).

**Shared state / blackboard.** A blackboard system is an architecture with (1) a **blackboard** as a global database of solution state, (2) independent specialist modules called **Knowledge Sources (KSs)** that modify the blackboard, and (3) a **control component** that schedules which KS runs next based on events and context. The Stanford blackboard references emphasize that KSs are procedurally independent and coordinate only through the shared blackboard plus control scheduling (https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf; https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf).

---

## Key Formulas & Empirical Results

### Orchestration benchmark results (SEC filing extraction)
**Architectures compared (Sec. III)** and primary results (Claude 3.5 Sonnet) (https://arxiv.org/pdf/2603.22651.pdf):

- **Sequential pipeline:** F1 **0.903**, cost **$0.187**, latency **38.7s**
- **Parallel fan-out + merge:** F1 **0.914**, cost **$0.221**, latency **21.3s**
- **Hierarchical supervisor-worker:** F1 **0.929**, cost **$0.261**, latency **46.2s**
- **Reflexive self-correcting loop:** F1 **0.943**, cost **$0.430**, latency **74.1s**

**Key claim supported:** measurable accuracy–cost–latency trade-offs; hierarchical achieves **98.5%** of reflexive F1 at **60.7%** of cost (paper’s stated comparison).

**Implementation defaults (Sec. IV-C):**
- temperature **0.0** for extraction calls
- temperature **0.3** for supervisor/critique

**Hierarchical design defaults (Sec. III):**
- confidence threshold **0.85**
- max **2** re-extraction iterations

**Reflexive loop defaults (Sec. III):**
- verifier checks: (1) format, (2) cross-field consistency, (3) source grounding
- example consistency rule: **Total Assets = Total Liabilities + Equity**
- max **3** correction iterations; else emit best-confidence with low-confidence flag

**Scaling result (Table IX):**
- reflexive degrades fastest: F1 **0.943 → 0.871** from **1K → 100K docs/day**
- sequential most resilient: **0.903 → 0.886**
- reflexive falls below hierarchical by **50K/day** due to queueing/timeouts truncating correction loops

---

### HLER human-in-the-loop multi-agent research pipeline (ops metrics + gates)
From HLER (https://arxiv.org/html/2603.07444v1):

**Pipeline stages (Sec. 3.1):**  
Data Audit → Data Profiling → Questioning → Data Collection → Analysis → Writing → Self-Critique → Review

**Human decision gates (Sec. 3.1, 3.4):**
1) Research Question Selection (PI chooses among candidates)  
2) Publication Decision (final quality gate)

**Two-loop control (Sec. 3.3):**
- Question quality loop: generate → feasibility screen → human selects → regenerate if needed
- Research revision loop: reviewer requests → re-analysis + rewrite → re-review; typically converges in **2–4 iterations**

**Empirical results (Sec. 4):**
- Dataset-aware question generation feasibility: **87% (69/79)** vs unconstrained **41% (34/82)**
  - Unconstrained failures: **42%** missing variables; **35%** design incompatible
- End-to-end completion: **86% (12/14)** runs completed; 2 failed at econometrics with graceful halt + logs
- Revision improves reviewer scores: mean **4.8 → 5.9 → 6.3** (v1, v2, final)
  - Biggest gains: clarity **+2.1**, identification **+1.4**; novelty ~**+0.3**
- Ops metrics: runtime **20–25 min/run**; API cost **$0.8–$1.5/run** (vs AI Scientist **$6–$15**)

**Key claim supported:** structured roles + shared state + HITL gates improve feasibility and reliability while controlling cost/runtime.

---

### AutoGen GroupChat defaults (speaker selection + function-call filtering)
From AutoGen 0.2 reference (https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/):

**GroupChat defaults:**
- `admin_name` default **"Admin"**
- `func_call_filter` default **True**
- `speaker_selection_method` default **"auto"**
- `max_retries_for_selecting_speaker` default **2**
- `allow_repeat_speaker` default **True**

**Auto speaker selection mechanism (procedural claim in docs):**
- uses a nested two-agent chat: *speaker selector* + *speaker validator*
- retries up to `max_retries_for_selecting_speaker`; if unresolved, fallback to next agent in list

**Key claim supported:** orchestration frameworks encode concrete coordination policies (speaker selection, tool/function routing constraints) that materially affect multi-agent behavior.

---

### AgentBench: evaluation numbers + failure modes for LLM agents
From AgentBench (https://arxiv.org/abs/2308.03688):

**8 environments** and metrics:
- OS (bash/Ubuntu Docker, SR), DB (SQL, SR), KG (F1), DCG Aquawar (win rate), LTP (game progress), HH ALFWorld (SR), WS WebShop (reward), WB Mind2Web (step SR)

**Dataset sizes (Sec. 4.1):** Dev/Test **269 / 1,014**; ~**3k / 11k** inference calls; rounds/problem **5–50**.

**Defaults (Sec. 4.1):**
- Temperature **0** (greedy)
- Context truncated to **≤3500 tokens**; omitted history marked with `"[NOTICE] messages are omitted."`

**Failure/finish reasons:** CLE, Invalid Format (IF), Invalid Action (IA), Task Limit Exceeded (TLE), Complete.

**Outcome ratios example (Table 4):**
- KG TLE **67.9%**
- LTP TLE **82.5%**
- DB IF **53.3%**
- HH IA **64.1%**

**Key claim supported:** interactive agent performance is often limited by multi-turn decision-making (TLE) and tool/action formatting (IF/IA), motivating multi-agent decomposition and verification.

---

## How It Works

### A. Supervisor/orchestrator pipeline with shared state (HLER-style)
Use this when a student asks “what does the orchestrator actually do?”

1) **Initialize shared run state** (HLER calls it `RunState`) to store intermediate artifacts as structured objects (e.g., `DataProfile`, `ResearchQuestion`, `AnalysisResult`) (https://arxiv.org/html/2603.07444v1).
2) **Dispatch to specialist agents in a fixed or semi-fixed sequence**:  
   Data Audit → Data Profiling → Questioning → Data Collection → Analysis → Writing → Self-Critique → Review.
3) **Persist each agent’s output** into shared state (not just free-form text), so downstream agents can condition on validated artifacts (e.g., QuestionAgent conditions on audit + profile).
4) **Apply control loops**:
   - **Question quality loop:** generate candidates → feasibility screen → **human selects** → optionally regenerate with constraints.
   - **Revision loop:** ReviewerAgent requests changes → re-analysis + rewrite → re-review; typically **2–4 iterations**.
5) **Human decision gates** at high-impact points:
   - choose research question
   - final publication decision
6) **Graceful failure handling**: if a stage fails (e.g., econometrics convergence), halt with logs rather than producing an ungrounded final report (HLER reports 2/14 failures handled this way).

---

### B. Hierarchical supervisor-worker with confidence thresholds (SEC benchmark)
Use this when a student asks “how does hierarchical differ from sequential/parallel?”

1) **Supervisor maintains a task queue** of extraction targets (fields/sections) (https://arxiv.org/pdf/2603.22651.pdf).
2) **Workers extract assigned fields** from document sections.
3) **Supervisor evaluates confidence** for each extracted field.
4) If confidence < **0.85**, **reassign** the field for re-extraction (possibly with different prompts/models); cap at **2** re-extraction iterations.
5) **Merge results** into a final structured output.

Key mechanical point: hierarchy adds *adaptive rework* based on confidence, rather than a one-pass chain.

---

### C. Parallel fan-out + merge with conflict resolution (SEC benchmark)
1) **Dispatcher splits** long documents into sections.
2) **Domain extractors run in parallel** on different sections/fields.
3) **Merge agent resolves conflicts** using **confidence-weighted voting** (https://arxiv.org/pdf/2603.22651.pdf).

Key mechanical point: parallelism reduces latency (21.3s vs 38.7s sequential in the benchmark) but needs an explicit merge policy.

---

### D. Reflexive self-correcting loop (SEC benchmark)
1) Produce an initial extraction.
2) **Verifier checks**:
   - format validity
   - cross-field consistency (e.g., accounting identity)
   - source grounding
3) If issues found, request correction and repeat up to **3** iterations; otherwise stop.
4) If max iterations reached, emit best-confidence output with low-confidence flags.

Key mechanical point: reflexive loops trade cost/latency for higher F1 (0.943) but degrade under high throughput due to queueing/timeouts (scaling table).

---

### E. Blackboard-style coordination (classic shared-state MAS)
Use this when a student asks “isn’t this just shared memory?”

1) **Blackboard** holds the global solution state, organized into levels/nodes; nodes can be created/deleted dynamically (https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf).
2) **Knowledge Sources (KSs)** are independent specialists; they do not call each other directly—coordination is via blackboard updates/events.
3) **Control component** runs an event-driven cycle:
   1) select an event  
   2) select triggered KS(s) in context  
   3) execute KS instance → modifies blackboard and posts new events  
   (repeat) (same Stanford source)
4) Scheduling can be priority/utility-based, FIFO/LIFO, etc. (control design alternatives described in the Stanford references).

---

## Teaching Approaches

### Intuitive (no math)
- **Why multi-agent:** one agent gets overloaded (context limits, “context rot” noted in the LangGraph video transcript) and can’t parallelize. Multiple agents let you split work (research in parallel, specialized extraction, separate reviewer).
- **What changes:** you add *coordination*: who speaks next, how results merge, when to retry, when to escalate to a human.

### Technical (with formal models)
- **Interactive agents as POMDPs:** AgentBench models interactive evaluation as a POMDP \(\langle \mathcal{S},\mathcal{A},\mathcal{T},\mathcal{R},\mathcal{I},\mathcal{O}\rangle\) with an LLM policy \(\pi\) (https://arxiv.org/abs/2308.03688).  
- **Multi-agent planning formalism (optional extension):** Det-Dec-POMDP is defined as \(\langle I,S,A,Z,T,O,R,\gamma,b_0\rangle\) with deterministic \(T\) and \(O\) (uncertainty only in \(b_0\)) (https://arxiv.org/html/2508.21595v1). This gives a rigorous lens for “multiple agents + partial information + coordination.”

### Analogy-based
- **Film production analogy:** supervisor = producer; workers = camera/sound/editing; verifier = quality control; blackboard = shared production board; human gate = executive sign-off.
- **Hospital analogy:** triage nurse (supervisor) routes to specialists; labs run in parallel; attending physician (reviewer) checks consistency and signs off.

---

## Common Misconceptions

1) **“Multi-agent just means multiple prompts; there’s no real architecture.”**  
   **Why wrong:** The sources show concrete control policies: confidence thresholds (0.85), bounded retries (2 re-extractions; 3 correction loops), speaker selection rules, and function-call filtering (SEC benchmark; AutoGen GroupChat docs).  
   **Correct model:** Multi-agent architecture = *agents + coordination mechanism* (dispatch, merge, verification, retries, shared state).

2) **“A supervisor pattern is always better than peer-to-peer.”**  
   **Why wrong:** The SEC benchmark shows trade-offs: reflexive/hierarchical improve F1 but increase cost/latency; at scale reflexive degrades faster (queueing/timeouts) and can fall below hierarchical by 50K/day (https://arxiv.org/pdf/2603.22651.pdf).  
   **Correct model:** Choose coordination based on constraints (accuracy vs cost vs latency vs throughput). Central control can bottleneck.

3) **“Parallel fan-out always improves quality because you get more coverage.”**  
   **Why wrong:** Parallel architectures require conflict resolution; the benchmark explicitly adds a merge agent with confidence-weighted voting, implying naive parallel outputs can disagree (https://arxiv.org/pdf/2603.22651.pdf).  
   **Correct model:** Parallelism mainly improves latency/throughput; quality depends on merge/verifier design.

4) **“If you add a verifier/reflection loop, quality will keep improving indefinitely.”**  
   **Why wrong:** Reflexive architecture caps corrections (max 3 iterations) and at high throughput its F1 degrades due to timeouts truncating loops (scaling table) (https://arxiv.org/pdf/2603.22651.pdf).  
   **Correct model:** Verification loops have diminishing returns and operational failure modes; you must bound iterations and plan for scaling.

5) **“Shared state means agents directly coordinate with each other.”**  
   **Why wrong:** In blackboard systems, KSs are procedurally independent and do not reference each other directly; only KSs modify the blackboard, and control schedules them (Stanford blackboard references).  
   **Correct model:** Shared state can *reduce coupling* by making coordination indirect (via state + events), not direct messaging.

---

## Worked Examples

### Example 1: Choose an orchestration pattern for SEC-style extraction (numbers-driven)
**Student scenario:** “I need to extract structured fields from long documents; what architecture should I pick?”

Use the SEC benchmark table (https://arxiv.org/pdf/2603.22651.pdf):

1) If you need **lowest latency** among compared systems:  
   - **Parallel fan-out + merge** latency **21.3s** (best), F1 **0.914**, cost **$0.221**.
2) If you need **best F1** and can pay:  
   - **Reflexive** F1 **0.943**, but cost **$0.430**, latency **74.1s**, and degrades fastest at high throughput.
3) If you want **near-best F1** with much lower cost than reflexive:  
   - **Hierarchical** F1 **0.929** at cost **$0.261** (paper notes 98.5% of reflexive F1 at 60.7% cost).
4) If you need **throughput robustness** at very high volume:  
   - scaling shows **sequential** degrades least (0.903→0.886) while reflexive degrades most (0.943→0.871).

**Tutor move:** ask the student to specify which constraint is binding (latency, cost, F1, throughput), then map to the table.

---

### Example 2: Implement a minimal AutoGen GroupChat with round-robin vs auto speaker selection
This is a *mechanical* example to illustrate coordination knobs from the AutoGen GroupChat reference (https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/).

```python
# Pseudocode-style sketch (focus: config knobs from the docs)
from autogen.agentchat import GroupChat, GroupChatManager

groupchat = GroupChat(
    agents=[agent_a, agent_b, agent_c],
    messages=[],
    max_round=10,
    admin_name="Admin",                 # default per docs
    speaker_selection_method="round_robin",  # or "auto"
    func_call_filter=True,              # default per docs
    allow_repeat_speaker=True,          # default per docs
    max_retries_for_selecting_speaker=2 # default per docs (auto mode)
)

manager = GroupChatManager(groupchat=groupchat)
```

**What to point out while tutoring:**
- Switching `"round_robin"` → `"auto"` activates the documented selector+validator mechanism and retry behavior.
- With `func_call_filter=True`, if a message suggests a function call, the next speaker must be an agent whose `function_map` contains that function name (docs).

---

### Example 3: HLER-style research pipeline as a state machine (role separation + gates)
Use this when a student asks “how do I structure a research multi-agent workflow?”

**Pipeline skeleton from HLER** (https://arxiv.org/html/2603.07444v1):

1) DataAuditAgent produces variable inventory (prevents proposing missing variables).
2) DataProfilingAgent computes summary stats/missingness/correlations; outputs `DataProfile`.
3) QuestionAgent generates dataset-aware hypotheses conditioned on audit+profile.
4) **Human gate:** PI selects research question among candidates.
5) Data agents retrieve/merge external data (World Bank, FRED, OpenAlex) + local datasets.
6) EconometricsAgent runs OLS / fixed-effects panel / DiD / event-study; exports tables/figures/structured summaries.
7) PaperAgent drafts manuscript (versioned markdown).
8) Self-critique + ReviewerAgent scores novelty/identification/data quality/clarity/policy relevance; issues revision requests.
9) Iterate revision loop (typically 2–4 iterations).
10) **Human gate:** publication decision.

**Tutor move:** ask the student where they want (a) structured artifacts, (b) human gates, (c) bounded iteration.

---

## Comparisons & Trade-offs

| Pattern | Coordination mechanism | Strengths (per sources) | Weaknesses / risks (per sources) | When to choose |
|---|---|---|---|---|
| Sequential pipeline | Fixed chain; state passed forward | Lower cost than reflexive; resilient at scale (sequential F1 0.903→0.886 at 1K→100K/day) (SEC benchmark) | Higher latency than parallel; errors can propagate | When throughput robustness and simplicity matter |
| Parallel fan-out + merge | Dispatcher + parallel workers + merge voting | Lowest latency in benchmark (21.3s) (SEC benchmark) | Needs conflict resolution (confidence-weighted voting) | When latency is key and tasks decompose cleanly |
| Hierarchical supervisor-worker | Supervisor queue + confidence threshold + retries | Higher F1 than sequential/parallel (0.929); bounded rework (threshold 0.85, max 2 retries) (SEC benchmark) | Higher latency/cost than parallel/sequential | When quality matters but reflexive is too expensive |
| Reflexive self-correcting loop | Verifier checks + correction iterations | Best F1 (0.943) (SEC benchmark) | Highest cost/latency; degrades fastest at high throughput due to timeouts | When maximum accuracy is worth cost and volume is moderate |
| Blackboard (shared state + scheduler) | KSs post events; control schedules | Supports opportunistic problem solving; KS independence; event-driven control (Stanford blackboard refs) | Requires careful control/scheduling design | When many specialists contribute opportunistically to shared solution state |

---

## Prerequisite Connections

- **Single-agent LLM agent loop (planning/memory/tools).** Weng’s agent overview frames the components (planning, memory, tool use) that become modularized across agents in MAS (https://lilianweng.github.io/posts/2023-06-23-agent/).
- **Tool calling + action validity.** AgentBench failure modes (Invalid Format/Invalid Action) motivate why multi-agent systems often include verifiers and routing constraints (https://arxiv.org/abs/2308.03688).
- **Stateful workflows.** LangGraph emphasizes long-running, stateful orchestration (durable execution, HITL), which is foundational for multi-step multi-agent pipelines (https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi_agent_collaboration/).
- **Basic evaluation metrics (F1, latency, cost).** The SEC benchmark’s comparisons require interpreting these operational metrics (https://arxiv.org/pdf/2603.22651.pdf).

---

## Socratic Question Bank

1) **If you had to cut latency in half, which coordination change would you try first: parallel fan-out or adding a verifier loop? Why?**  
   *Good answer:* parallel fan-out targets latency directly (SEC benchmark shows 21.3s vs 38.7s sequential), verifier loops increase latency.

2) **What failure mode are you trying to prevent by adding a verifier agent: invalid format, wrong content, or long-horizon stalling? How would you detect it?**  
   *Good answer:* ties to AgentBench IF/IA/TLE categories and proposes checks (format validators, action schema checks, step limits).

3) **Where would you place a human decision gate in your pipeline, and what’s the cost of placing it earlier vs later?**  
   *Good answer:* references HLER gates (question selection; publication decision) and explains early gate prevents wasted downstream compute.

4) **In a hierarchical system, what does a confidence threshold actually *do* operationally? What happens when it’s too high or too low?**  
   *Good answer:* threshold triggers re-extraction (0.85 in SEC benchmark); too high increases retries/cost/latency; too low reduces quality.

5) **Why might reflexive self-correction degrade at high throughput even if it’s best at low volume?**  
   *Good answer:* queueing/timeouts truncate correction loops; scaling table shows reflexive F1 drops fastest.

6) **If two parallel agents disagree, what merge rule would you use and why: majority vote, confidence-weighted voting, or a consistency constraint?**  
   *Good answer:* cites confidence-weighted voting (SEC benchmark) and/or consistency rules (assets = liabilities + equity).

7) **What information must be stored in shared state so downstream agents don’t “re-discover” it? Give one concrete artifact.**  
   *Good answer:* `DataProfile`, variable inventory, extracted fields with provenance/confidence (HLER/SEC benchmark).

8) **How would you know your multi-agent system is failing due to coordination rather than model capability?**  
   *Good answer:* points to IF/IA/TLE patterns (AgentBench) and suggests instrumentation (logs, retries, speaker selection traces).

---

## Likely Student Questions

**Q: What are the concrete accuracy–cost–latency trade-offs between sequential, parallel, hierarchical, and reflexive multi-agent orchestration?**  
→ **A:** In the SEC filing extraction benchmark (Claude 3.5 Sonnet), sequential F1 **0.903** cost **$0.187** latency **38.7s**; parallel F1 **0.914** cost **$0.221** latency **21.3s**; hierarchical F1 **0.929** cost **$0.261** latency **46.2s**; reflexive F1 **0.943** cost **$0.430** latency **74.1s** (https://arxiv.org/pdf/2603.22651.pdf).

**Q: What does the hierarchical supervisor do differently from a sequential pipeline?**  
→ **A:** The hierarchical supervisor maintains a task queue and uses a **confidence threshold = 0.85** to decide when to reassign low-confidence fields for re-extraction, with **max 2 re-extraction iterations** (https://arxiv.org/pdf/2603.22651.pdf). A sequential pipeline is a fixed chain without adaptive rework.

**Q: How does the reflexive self-correcting loop decide what to fix?**  
→ **A:** A verifier checks (1) format, (2) cross-field consistency, and (3) source grounding; it can enforce rules like **Total Assets = Total Liabilities + Equity** and runs up to **3 correction iterations** before emitting best-confidence output with flags (https://arxiv.org/pdf/2603.22651.pdf).

**Q: Why can reflexive systems get worse at high throughput?**  
→ **A:** The benchmark reports reflexive F1 degrades from **0.943→0.871** as volume scales **1K→100K docs/day**, attributed to queueing/timeouts truncating correction loops; sequential degrades least (**0.903→0.886**) (https://arxiv.org/pdf/2603.22651.pdf).

**Q: What are the default coordination settings in AutoGen GroupChat (speaker selection, retries, admin, function routing)?**  
→ **A:** `admin_name="Admin"`, `speaker_selection_method="auto"`, `max_retries_for_selecting_speaker=2`, `allow_repeat_speaker=True`, and `func_call_filter=True` (https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/).

**Q: What does `func_call_filter=True` actually enforce?**  
→ **A:** If a message is a function call suggestion, the next speaker must be an agent whose `function_map` contains that function name (AutoGen GroupChat docs: https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/).

**Q: What evidence is there that role specialization + shared state improves outcomes?**  
→ **A:** In HLER, dataset-aware question generation conditioned on audit+profile yields **87% (69/79)** feasible questions vs **41% (34/82)** unconstrained; unconstrained failures include **42%** missing variables and **35%** incompatible designs (https://arxiv.org/html/2603.07444v1).

**Q: What are common failure modes when evaluating LLMs as interactive agents?**  
→ **A:** AgentBench categorizes failures as Invalid Format (IF), Invalid Action (IA), Task Limit Exceeded (TLE), etc.; example rates include KG TLE **67.9%**, LTP TLE **82.5%**, DB IF **53.3%**, HH IA **64.1%** (https://arxiv.org/abs/2308.03688).

---

## Available Resources

### Videos
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: the student asks *why* multi-agent systems help (parallelism, specialization, context limits) or wants a framework-oriented overview.

### Articles & Tutorials
- [LLM-powered Autonomous Agents (Lilian Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: the student needs grounding in agent components (planning/memory/tools) before discussing multi-agent orchestration.
- [AutoGen (stable docs)](https://microsoft.github.io/autogen/stable/index.html) — Surface when: the student asks how to prototype multi-agent apps in Python or wants framework options (extensions, runtimes).
- [AutoGen paper: “Enabling Next-Gen LLM Applications via Multi-Agent Conversation”](https://arxiv.org/abs/2308.08155) — Surface when: the student asks for an academic reference motivating multi-agent conversation patterns.
- [LangGraph multi-agent collaboration tutorial](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi_agent_collaboration/) — Surface when: the student asks about orchestration infrastructure (durable execution, HITL, stateful workflows).

---

## Visual Aids

![LLM-powered autonomous agent system overview with planning, memory, and tools. (Weng, 2023)](/api/wiki-images/multi-agent-systems/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: the student is mixing up “agent components” (planning/memory/tools) with “multi-agent orchestration”; use to separate *inside one agent* vs *across agents*.

![Reflexion's self-reflection loop: Actor, Evaluator, and episodic memory. (Shinn & Labash, 2023)](/api/wiki-images/multi-agent-systems/images/lilianweng-posts-2023-06-23-agent_003.png)  
Show when: the student asks what a “reflexive” or “self-correcting” loop looks like mechanically; connect to the SEC benchmark’s verifier/correction iterations.

---

## Key Sources

- [Multi-agent orchestration benchmark (SEC filing extraction)](https://arxiv.org/pdf/2603.22651.pdf) — Best concrete, numbers-first comparison of sequential/parallel/hierarchical/reflexive patterns with scaling behavior.
- [HLER human-in-the-loop multi-agent research pipeline](https://arxiv.org/html/2603.07444v1) — Detailed production-style orchestrator + shared state (`RunState`) + explicit roles + human gates + ops metrics.
- [AutoGen GroupChat reference (0.2)](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/) — Precise coordination defaults (speaker selection, retries, function-call filtering) that often matter in real systems.
- [Blackboard System Architecture & Control Cycle (Stanford)](https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf) — Canonical shared-state + event-driven control model for coordinating specialists.
- [AgentBench](https://arxiv.org/abs/2308.03688) — Empirical failure modes and evaluation setup for LLM agents in interactive environments; useful for motivating verification and decomposition.