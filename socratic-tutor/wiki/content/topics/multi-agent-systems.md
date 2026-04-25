---
title: "Multi-Agent Systems"
subject: "Agents & Reasoning"
date: 2025-01-01
tags:
  - "subject/agents-and-reasoning"
  - "level/intermediate"
  - "level/advanced"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Lilian Weng"
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

# Multi Agent Systems

## Video (best)
- **Harrison Chase (LangChain)** — "Multi-Agent Systems with LangGraph"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=Mi5wOpAgixw)
- Why: N/A — see coverage notes below
- Level: intermediate

> **Coverage note:** 3Blue1Brown, Andrej Karpathy, Yannic Kilcher, StatQuest, and Serrano.Academy do not have well-known dedicated videos on multi-agent systems as of my knowledge cutoff. The best video content exists in conference talks and framework-specific tutorials, but I cannot confirm exact YouTube IDs without risk of hallucination.

**None identified** from preferred educator list with a verifiable YouTube ID.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM-powered Autonomous Agents"
- **Link:** [https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Why: Weng's post is the most cited, pedagogically structured written explainer covering agent architectures, memory, tool use, and multi-agent coordination patterns. It bridges theory and practice with clear diagrams and references to seminal work. While it covers single-agent foundations heavily, the multi-agent and orchestration sections are the best freely available written treatment from a trusted author.
- Level: intermediate

---

## Deep dive
- **AutoGen / Microsoft Research Documentation & Technical Report**
- **Link:** [https://microsoft.github.io/autogen/stable/index.html](https://microsoft.github.io/autogen/stable/index.html)
- Why: The AutoGen framework documentation is the most comprehensive technical reference for multi-agent system design patterns including supervisor patterns, hierarchical teams, human-in-the-loop, blackboard/shared state, and conflict resolution. It combines conceptual explanation with architectural diagrams and is actively maintained by a research team. The accompanying technical report (see paper section) grounds it academically.
- Level: advanced

---

## Original paper
- **Wu et al. (2023)** — "AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation"
- **Link:** [https://arxiv.org/abs/2308.08155](https://arxiv.org/abs/2308.08155)
- Why: This is the most readable and widely adopted seminal paper specifically on LLM-based multi-agent systems. It introduces the conversational multi-agent paradigm, covers agent roles, message passing, human-in-the-loop integration, and flexible conversation topologies (peer-to-peer, hierarchical). It is highly cited and directly maps to the related concepts listed for this topic. More accessible than earlier MAS literature from classical AI.
- Level: intermediate/advanced

---

## Code walkthrough
- **LangChain / LangGraph** — "LangGraph Multi-Agent Tutorials (Supervisor & Hierarchical Patterns)"
- **Link:** [https://langchain-ai.github.io/langgraph/tutorials/introduction/](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- Why: LangGraph's official tutorials provide the best hands-on code walkthroughs for the exact patterns listed in this topic — supervisor pattern, hierarchical teams, handoffs, shared state, human-in-the-loop, and peer-to-peer architectures. The code is minimal, well-commented, and directly tied to conceptual diagrams. It uses Python and is appropriate for learners in an agentic AI course context.
- Level: intermediate

---

## Coverage notes
- **Strong:** Written explainers (Lilian Weng), framework documentation (AutoGen, LangGraph), and the AutoGen paper cover agent roles, message passing, supervisor patterns, hierarchical teams, and human-in-the-loop very well.
- **Weak:** Blackboard pattern and classical conflict resolution/consensus mechanisms are underserved in LLM-era resources; most coverage comes from classical MAS literature (Weiss 1999) rather than modern tutorials.
- **Gap:** No high-quality YouTube explainer exists from the preferred educator list (3B1B, Karpathy, Yannic, StatQuest, Serrano) for multi-agent LLM systems specifically. This is a meaningful content gap for the platform — a custom video may be warranted. Conference talks (e.g., from NeurIPS or AI Engineer Summit) exist but lack the pedagogical structure of the preferred educators.
- **Gap:** Debate-and-consensus mechanisms (e.g., Society of Mind-style approaches, Du et al. 2023 "Improving Factuality via Multi-Agent Debate") are covered in papers but have no strong standalone tutorial resource.

---

---

## Additional Resources for Tutor Depth

> **35 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Blackboard Architecture (Components + Control Alternatives)
**Paper** · [source](https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf)

*Architecture-level decomposition of blackboard systems with explicit component roles and control-cycle rationale*

<details>
<summary>Key content</summary>

- **Blackboard architecture = 3 components** (Intro, Fig. 1):  
  1) **Blackboard** (global database / shared solution state), 2) **Knowledge Sources (KSs)** (agents that create/modify blackboard contents), 3) **Control component** (realizes behavior in serial computing environment).
- **Task characteristics suited to blackboards** (Sec. 3.1):  
  (1) complex/ill-structured, large spaces; systematic generation infeasible;  
  (2) **opportunistic**, situation-dependent invocation of diverse knowledge; control decisions made during solving (not pre-set paths);  
  (3) mix of **synthetic + analytic** processes (bottom-up fusion + top-down model-based reasoning).
- **Solution strategies and architectural implications** (Secs. 3.2–4):  
  - **Search**: needs **generator + evaluator**; in HEARSAY-II, KS **action** generates hypotheses; KS **condition** does look-ahead; scheduler performs global evaluation (Fig. 3). Condition/action may be scheduled separately; blackboard can change between them → may require re-evaluation (Sec. 5.3.1).  
  - **Recognition**: **match → apply**; KS condition specifies situations; scheduler selects best **region/event** to process next (Fig. 4).
- **Blackboard structure defaults** (Sec. 5.1): organized into **levels** (abstraction/compositional hierarchies). **Level object as class**, nodes as instances; nodes created dynamically; attribute values may include **credibility, timestamps, history**. **Panels**: multiple hierarchies; common second panel = **control info** (e.g., BB1).
- **KS design pattern** (Sec. 5.2, Fig. 5): **condition + action**; condition often **multi-stage filters**: context-independent **trigger** then context-dependent filters; action modifies solution state and may post goals/expectations.
- **Control design axes** (Sec. 5.3): schedulable entities (whole KS vs condition/action), **event-oriented vs knowledge-oriented scheduling** (Figs. 6–7), posting/noticing events, and where **control data** lives (event records vs scheduling queue vs control panel).

</details>

### 📄 Det-Dec-POMDP formalism + IDPP (JESP best-response via Det-POMDP)
**Paper** · [source](https://arxiv.org/html/2508.21595v1)

*Dec-POMDP/Det-Dec-POMDP tuple definition; determinism assumptions; scalable solution procedure (IDPP) via best-response Det-POMDPs*

<details>
<summary>Key content</summary>

- **Det-Dec-POMDP definition (Def. 1, Sec. 4):** tuple  
  \[
  \langle I,S,A,Z,T,O,R,\gamma,b_0\rangle
  \]
  where \(I=\{1,\dots,n\}\) agents; \(S\) states; **joint actions** \(A=\times_i A_i\); **joint observations** \(Z=\times_i Z_i\); **deterministic** transition \(T:S\times A\to S\); **deterministic** observation \(O:A\times S\to Z\); reward \(R\); discount \(\gamma\); initial belief \(b_0\in \Delta(S)\).  
  Local policy: \(\pi_i\) maps **local action-observation history** to action. **Uncertainty only in \(b_0\)**; thereafter dynamics fully deterministic via \(T,O\).
- **Belief property (Sec. 4):** in deterministic POMDPs, belief support **monotonically decreases** as deterministic observations rule out inconsistent states.
- **Why hard despite determinism (Sec. 5):** initial-state uncertainty induces many possible observation sequences ⇒ **exponential joint history space**; sufficient-statistic/occupancy approaches become intractable (esp. thousands of observations/agent).
- **IDPP procedure (Sec. 5, Alg. 2):** JESP-style iterative best response: repeatedly pick agent \(i\), **fix other agents’ FSC policies**, build \(i\)’s best-response model, solve, update \(i\)’s policy; iterate until convergence (Nash equilibrium policy set).
- **Key reduction (Thm. 1, Sec. 5):** with other agents’ FSCs fixed, agent \(i\)’s best-response model is a **Det-POMDP** on extended state  
  \[
  \bar S_i = \{(s, q_{-i}, o_i)\}
  \]
  (environment state \(s\), other agents’ FSC nodes \(q_{-i}\), and \(i\)’s current observation \(o_i\)); transition becomes deterministic because other agents’ actions/nodes and \(O\) are deterministic.
- **Solver choice (Sec. 5):** IDPP solves each best-response Det-POMDP using **Det-MCVI** (Schutz et al. 2025), exploiting determinism for scalability.
- **Heuristic initialization (Sec. 5, Alg. 3):** avoid joint-observation planning: assume others follow a default **MDP policy** \(\mu:S\to A\); compute each agent’s initial policy via standard value iteration in a deterministic model.
- **Empirical setup defaults (Sec. 6):** planning time limit **10,000 s**; MARL training budget **10,000 episodes**, max **100 steps/episode**; MCJESP uses **1 s per FSC node** planning budget.
- **Key empirical claim (Sec. 6):** optimal finite-horizon **MAA\*** fails even at horizon **10** due to memory exhaustion; **IDPP maintains low memory** by avoiding enumeration of joint histories; IDPP outperforms others on large instances where InfJESP fails.

</details>

### 📄 HLER human-in-the-loop multi-agent research pipeline (ops metrics + gates)
**Paper** · [source](https://arxiv.org/html/2603.07444v1)

*Production-oriented multi-agent pipeline decisions with operational metrics/tradeoffs + human-in-the-loop escalation gates*

<details>
<summary>Key content</summary>

- **Architecture (Section 3.1):** Central **orchestrator** dispatches tasks to specialized agents and maintains shared state **RunState** (records intermediate outputs). Sequential workflow: **Data Audit → Data Profiling → Questioning → Data Collection → Analysis → Writing → Self-Critique → Review**. Agent outputs stored as structured objects and passed forward.
- **Human decision gates (Section 3.1, 3.4):**
  1) **Research Question Selection** (PI chooses among candidates)  
  2) **Publication Decision** (final quality gate)
- **Agent roles (Section 3.2):**
  - **DataAuditAgent:** builds variable inventory from headers/schema to prevent proposing missing variables.
  - **DataProfilingAgent:** summary stats, missingness, distributions, correlations; flags endogeneity risks; outputs **DataProfile**.
  - **QuestionAgent:** **dataset-aware hypothesis generation** conditioned on audit + profile (availability, missingness, distributional diagnostics).
  - **Data agents:** retrieve/merge from public APIs (World Bank, FRED, OpenAlex) + local datasets.
  - **EconometricsAgent:** executes OLS, fixed-effects panel, DiD, event-study; exports tables/figures/structured summaries.
  - **PaperAgent:** drafts full manuscript; versioned (e.g., `draft_v1.md`, `draft_v2.md`).
  - **ReviewerAgent:** scores (1–10) on novelty, identification credibility, data quality, clarity, policy relevance; issues revision requests.
- **Two-loop control (Section 3.3):**
  - **Question quality loop:** generate → feasibility screen → **human selects**; can regenerate with modified constraints.
  - **Research revision loop:** reviewer requests → re-analysis + rewrite → re-review; typically **converges in 2–4 iterations**.
- **Empirical results (Section 4):**
  - **Feasible questions:** dataset-aware **87% (69/79)** vs unconstrained **41% (34/82)**. Unconstrained failures: **42%** missing variables; **35%** design incompatible.
  - **End-to-end completion:** **86% (12/14)** runs completed; 2 failed at econometrics (fixed-effects convergence on sparse subsamples) with graceful halt + logs.
  - **Revision improves scores:** overall mean **4.8 → 5.9 → 6.3** (v1, v2, final). Biggest gains: **clarity +2.1**, **identification +1.4**; novelty ~**+0.3**.
  - **Ops metrics:** runtime **20–25 min/run**; API cost **$0.8–$1.5/run** (vs AI Scientist **$6–$15**).
- **Implementation defaults (Section 3.5):** Python; LLM via **Anthropic Claude Sonnet 4.6** (model-agnostic); structured schema objects (e.g., `ResearchQuestion`, `DataProfile`, `AnalysisResult`); manuscripts in Markdown → PDF via Pandoc/LaTeX.

</details>

### 📊 AgentBench (LLM-as-Agent benchmark + failure modes)
**Benchmark** · [source](https://arxiv.org/abs/2308.03688)

*AgentBench suite definition (8 environments) + comparative results (29 LLMs) + categorized failure modes*

<details>
<summary>Key content</summary>

- **Formalization (Section 2):** Interactive evaluation of an LLM agent is modeled as a **POMDP**:  
  \[
  \langle \mathcal{S}, \mathcal{A}, \mathcal{T}, \mathcal{R}, \mathcal{I}, \mathcal{O}\rangle
  \]
  where \(\mathcal{S}\)=state space, \(\mathcal{A}\)=action space, \(\mathcal{T}\)=transition function, \(\mathcal{R}\)=reward, \(\mathcal{I}\)=task-instruction space, \(\mathcal{O}\)=observation space; LLM agent denoted \(\pi\).
- **8 environments (Section 3):**
  - Code-grounded: **OS (bash/Ubuntu Docker, metric SR)**; **DB (authentic SQL, metric SR)**; **KG (partially observable KG QA, metric F1)**.
  - Game-grounded: **DCG Aquawar (metric win rate)**; **LTP (yes/no/irrelevant host, metric “game progress”)**; **HH ALFWorld (metric SR)**.
  - Web-grounded: **WS WebShop (metric reward)**; **WB Mind2Web (metric step SR)**.
- **Dataset scale & defaults (Section 4.1):** Dev/Test total sizes **269 / 1,014**; ~**3k / 11k** inference calls (≈ MMLU). Estimated rounds per problem **5–50**. **Temperature=0** (greedy). Context truncated to **≤3500 tokens**; omitted history marked with `"[NOTICE] messages are omitted."`
- **Overall score procedure (Section 4.1):** avoid naive averaging; **rescale each task’s average score** across evaluated models, then weighted average using **fixed weights = reciprocal of average score** per task (Table 2 weights: OS 10.8, DB 13.0, KG 13.9, DCG 12.0, LTP 3.5, HH 13.0, WS 30.7, WB 11.6).
- **Failure/finish reasons (Section 2, 4.3):** **CLE**, **Invalid Format (IF)**, **Invalid Action (IA)**, **Task Limit Exceeded (TLE)**, **Complete**. IF/IA mainly instruction-following; TLE indicates weak multi-turn reasoning/decision-making.
- **Key empirical results (Table 3, Section 4.2):**
  - **gpt-4** best on **6/8** datasets; **HH SR = 78%**.
  - **API vs OSS gap:** average overall score **OSS 0.51 vs API 2.32**; all API models **>1.00** overall.
  - Best OSS (≤70B) reported: **CodeLLaMA-34B overall 0.96**, still below **gpt-3.5-turbo overall 2.32**.
- **Outcome ratios example (Table 4):** predominant failure is **TLE**; e.g., **KG TLE 67.9%**, **LTP TLE 82.5%**; **DB IF 53.3%**; **HH IA 64.1%**.
- **Design rationale:** evaluate “primitive” **CoT + Action** prompting (no ensembles/reflection/search) as cheapest/common deployment; environments isolated via **Docker** + per-task workers; API-centric toolkit via **HTTP server-client**.

</details>

### 📊 LangGraph production metrics: latency, checkpoints, replay, scale
**Benchmark** · [source](https://aerospike.com/blog/langgraph-production-latency-replay-scale)

*Operational framing + concrete latency/storage math for production agent workflows (TTFT/TPOT targets, checkpointing, replay/idempotency, fan-out amplification).*

<details>
<summary>Key content</summary>

- **Interactive latency targets (MLPerf framing):** real-time systems often target **TTFT < 1s** and **TPOT in “tens of ms”** to feel responsive; orchestration overhead must fit inside these budgets.
- **LangGraph execution model (supersteps):** each step has **3 phases**: (1) *plan* which actors/nodes to execute, (2) *execute* selected actors in parallel, (3) *apply updates*. Intermediate updates aren’t visible until the next step → clearer race-condition boundaries and replay points.
- **Eq. 1 — Checkpoint write rate sizing:**  
  **writes/sec = steps_per_request × requests/sec**  
  Example from source: **12 steps/request** and **2,000 req/s ⇒ 24,000 writes/s** (plus reads for resume/inspection).
- **Checkpoint alignment:** checkpoints persist at **superstep boundaries**; snapshot count scales with **#steps**, not wall-clock runtime.
- **Replay/resume semantics:** workflows can **pause and resume** (even **up to a week** later) by restoring state and **replaying from a safe point**. To avoid duplicated side effects (e.g., “write ticket twice”, “charge twice”), **non-deterministic/side-effectful operations must be isolated as separate tasks**; design for **determinism + idempotency**.
- **State types:** (a) **thread-local execution state** keyed by **thread_id** for checkpointing/resume; (b) **cross-thread long-term memory** with **TTL** and optional similarity search (**semantic search disabled by default; requires index + compatible store**).
- **Tool catalog default guidance:** OpenAI function calling guidance cited: keep **< 20 functions** available at once for higher accuracy; function definitions are injected into system message and billed as input tokens.
- **Empirical comparison:** external benchmark (5-agent workflow × **100 runs**) reports LangGraph **>2× faster than CrewAI**; CrewAI had ~**5s of a 9s** segment as tool-interaction gap; LangGraph passes **state deltas** vs full histories (token/latency savings).

</details>

### 📊 MCP Server + LangGraph Performance Benchmarks
**Benchmark** · [source](https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks)

*Benchmark tables comparing latency/throughput/error/cost for LangGraph-based MCP server vs alternatives under controlled conditions.*

<details>
<summary>Key content</summary>

- **Benchmark methodology / defaults**
  - Hardware (GCP): **n2-standard-4**, **4 vCPU (Intel Xeon 2.3GHz)**, **16GB RAM**, **SSD 1000 IOPS**, **10Gbps**, region **us-central1**.
  - LLM: **Gemini 2.0 Flash**. Load tool: **k6**. Duration: **5 min** per scenario after **1-min ramp-up**. **Avg of 3 runs**. Metrics: **Prometheus + Grafana**.
  - Workloads: **Simple Agent (single node)**; **Multi-Agent (3 sequential agents)**; **Complex Workflow (5-node graph w/ conditionals)**; **High Concurrency (100+ concurrent)**.
- **Empirical results (end-to-end latency includes LLM + network + orchestration + persistence)**
  - **Simple Agent (MCP+LangGraph, Cloud Run self-hosted):** **142 req/s**, p50 **245ms**, p95 **890ms**, p99 **1210ms**, error **0.02%**, CPU **68% avg (85% peak)**, mem **4.2GB avg (5.8GB peak)**.
  - **Simple Agent (LangGraph Cloud):** **135 req/s**, p50 **280ms**, p95 **950ms**, p99 **1450ms**, error **0.05%**, cost **$675/5min** (**$0.001/node execution**).
  - **Multi-Agent 3-step (MCP+LangGraph on GKE):** **48 req/s**, p50 **1850ms**, p95 **4200ms**, p99 **6100ms**, error **0.08%**, scaling **~linear** (2× pods ≈ 2× throughput).
  - **Multi-Agent (CrewAI self-hosted):** **52 req/s**, p50 **1650ms**, p95 **3800ms**, p99 **5400ms**, error **0.12%**; rationale: lower overhead for simple sequential delegation.
  - **Complex 5-node conditional graph (MCP+LangGraph):** **32 req/s**, p50 **2800ms**, p95 **6500ms**, p99 **9200ms**, error **0.15%**; **Redis checkpointing**, **automatic retries**.
  - **High concurrency (100 VUs; MCP+LangGraph on K8s+HPA):** max **425 req/s** (autoscale **2→10 pods**), p50 **320ms**, p95 **1200ms**, p99 **2400ms**, error **0.25%**, recovery **45s**.
  - **High concurrency (Google ADK):** max **380 req/s**, p50 **360ms**, p95 **1450ms**, error **0.18%**, cost **higher** (Vertex fees).
- **Cost-per-1M complex requests**
  - MCP (GKE): **$312** (infra **$300** + LLM **$12**); MCP (Cloud Run): **$512**; LangGraph Cloud: **$5000**; Google ADK: **$1015**.
- **Scaling table (vertical)**
  - **2 vCPU/8GB: 75 req/s** (baseline); **4 vCPU/16GB: 142 req/s (90% efficient)**; **8 vCPU/32GB: 260 req/s (87% efficient)**.

</details>

### 📊 Multi-agent orchestration benchmark (SEC filing extraction)
**Benchmark** · [source](https://arxiv.org/pdf/2603.22651.pdf)

*Comparative tables across multi-agent orchestration architectures with measurable outcomes + ablations + scaling*

<details>
<summary>Key content</summary>

- **Architectures compared (Sec. III):**
  - **A Sequential pipeline:** fixed agent chain; cumulative JSON state passed forward; max context **128K**; split long docs into sections then merge.
  - **B Parallel fan-out + merge:** dispatcher routes sections to domain extractors; merge agent resolves conflicts via **confidence-weighted voting**.
  - **C Hierarchical supervisor-worker:** supervisor maintains task queue; **confidence threshold = 0.85**; low-confidence fields re-assigned; **max 2 re-extraction iterations**; supports **heterogeneous model routing**.
  - **D Reflexive self-correcting loop:** verifier checks (1) format, (2) cross-field consistency, (3) **source grounding**; example rule: **Total Assets = Total Liabilities + Equity**; **max 3 correction iterations**, else emit best-confidence with low-confidence flag.
- **Dataset (Sec. IV-A):** **10,000** SEC filings: **4k 10-K (avg 187,340 tokens)**, **4k 10-Q (82,150)**, **2k 8-K (14,820)**; **25 fields** across financial metrics (10), governance (8), exec comp (7).
- **Defaults (Sec. IV-C):** temperature **0.0** for extraction calls; **0.3** for supervisor/critique.
- **Primary results (Table III):** (Claude 3.5 Sonnet)
  - Sequential: **F1 0.903**, cost **$0.187**, latency **38.7s**
  - Parallel: **F1 0.914**, cost **$0.221**, latency **21.3s**
  - Hierarchical: **F1 0.929**, cost **$0.261**, latency **46.2s**
  - Reflexive: **F1 0.943**, cost **$0.430**, latency **74.1s**
  - Key tradeoff: hierarchical achieves **98.5%** of reflexive F1 at **60.7%** of cost.
- **Ablations on hierarchical+Claude (Tables V–VIII):**
  - Semantic cache (embed sim **0.95**, text-embedding-3-small): field-level cache cost **$0.171** (−34.5%), F1 **0.924**.
  - Model routing: **2-tier (Claude+Mixtral)** F1 **0.912**, cost **$0.127** (−51.3%).
  - Retries: escalation (retry with stronger model) best F1 **0.931**.
  - Combined “Hierarchical-Optimized”: **F1 0.924**, cost **$0.148**, latency **30.2s** (near-sequential cost).
- **Scaling (Table IX):** reflexive degrades fastest: F1 **0.943→0.871** from **1K→100K docs/day**; sequential most resilient (**0.903→0.886**). Reflexive falls below hierarchical by **50K/day** due to queueing/timeouts truncating correction loops.

</details>

### 📖 AutoGen GroupChat & GroupChatManager (speaker selection + defaults)
**Reference Doc** · [source](https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/)

*Concrete parameter defaults + semantics for GroupChat/GroupChatManager (admin, rounds, function-call filtering, auto speaker selection, last_speaker)*

<details>
<summary>Key content</summary>

- **GroupChat dataclass fields (core config):**
  - `agents`: list of participating agents; `messages`: group message list; `max_round`: max conversation rounds.
  - `admin_name` default **"Admin"**; **KeyboardInterrupt** causes admin agent to take over.
  - `func_call_filter` default **True**: if a message is a *function call suggestion*, next speaker must be an agent whose `function_map` contains that function name.
- **Speaker selection configuration (defaults + options):**
  - `speaker_selection_method` default **"auto"**. Allowed: `"auto"`, `"manual"`, `"random"`, `"round_robin"` (case-insensitive), or a **Callable** `(last_speaker, groupchat) -> Agent | str | None`.
    - Callable may return: an `Agent` in the chat; a string selecting a default method; or `None` to terminate gracefully.
  - `max_retries_for_selecting_speaker` default **2** (auto mode requery attempts when LLM returns multiple/no names).
  - `allow_repeat_speaker` default **True**; can be `False` (no repeats) or a **list of Agents** allowed to repeat.
  - `allowed_or_disallowed_speaker_transitions` (dict) + `speaker_transitions_type` (`"allowed"`/`"disallowed"`). Mutually exclusive with `allow_repeat_speaker`.
- **Auto speaker selection workflow (procedure):**
  1. Create nested **two-agent** chat: *speaker selector* + *speaker validator*.
  2. Inject group messages; selector proposes next agent.
  3. If invalid (multiple/none), append follow-up prompt and retry up to `max_retries_for_selecting_speaker`.
  4. If still unresolved, fallback: **next agent in list**.
- **Prompt templates (defaults):**
  - `select_speaker_message_template` default: role-play instruction with `{roles}` and `{agentlist}`; appears **first** in context.
  - `select_speaker_prompt_template` default: “Read the above… select next role from {agentlist}… Only return the role.” Appears **last**; set to `None` to disable.
  - Follow-ups: `select_speaker_auto_multiple_template`, `select_speaker_auto_none_template` (both enforce returning **ONLY** one case-sensitive agent name).
- **GroupChatManager `last_speaker` property (semantics):**
  - Agents receive messages from the manager; `sender.last_speaker` reveals the **real originating agent** of the last group message.

</details>

### 📖 BaseCheckpointSaver.list (LangGraph.js checkpoint listing)
**Reference Doc** · [source](https://reference.langchain.com/javascript/langchain-langgraph-checkpoint/BaseCheckpointSaver/list)

*Concrete semantics + parameters for listing checkpoints (filters/pagination) on `BaseCheckpointSaver`*

<details>
<summary>Key content</summary>

- **Core concepts**
  - **Checkpoint** = snapshot of graph state at a superstep (enables “memory”, resumability, human-in-the-loop).
  - **CheckpointTuple** = `{ checkpoint, config, metadata, pendingWrites }` (checkpoint plus associated config/metadata/pending writes).
  - **Thread** = unique `thread_id` grouping a series of checkpoints (supports multi-tenant separation).
- **Required/optional run identifiers (configurable config)**
  - Always pass `thread_id`.
  - Optionally pass `checkpoint_id` to resume from a specific checkpoint within a thread.
  - Examples:
    - `{ configurable: { thread_id: "1" } }`
    - `{ configurable: { thread_id: "1", checkpoint_id: "0c62ca34-ac19-445d-bbb0-5b4984975b2a" } }`
- **Design rationale: pending writes for durable execution**
  - If a node fails mid-superstep, LangGraph stores **pending checkpoint writes** from nodes that already succeeded so resuming from that superstep avoids re-running successful nodes.
- **`BaseCheckpointSaver.list` / `alist` parameters (checkpoint retrieval semantics)**
  - `config`: base configuration used to scope listing (typically includes `configurable.thread_id`).
  - `filter`: additional filtering criteria (metadata filter).
  - `before`: list checkpoints created **before** this configuration (cursor-style pagination).
  - `limit`: maximum number of checkpoints to return.
  - Returns: `Iterator[CheckpointTuple]` (sync) / `AsyncIterator[CheckpointTuple]` (async).
- **Procedure: list checkpoints (JS example)**
  - `for await (const checkpoint of checkpointer.list(readConfig)) { console.log(checkpoint); }`

</details>

### 📖 CompiledStateGraph runtime surface (JS)
**Reference Doc** · [source](https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)

*Methods/properties on the compiled graph artifact (invoke/stream/batch/state/checkpointing/interrupts/config)*

<details>
<summary>Key content</summary>

- **What it is:** `CompiledStateGraph` is the **final result** of building + compiling a `StateGraph`; **do not instantiate directly**—create via `StateGraph.compile()`. (Since v0.3; docs shown for v1.2.8)
- **Core execution methods**
  - `invoke(): Promise<ExtractStateType<O, O>>` — run graph once with input + config; returns **final output state** (per `outputChannels`).
  - `batch(): Promise<OperationResults<Op>>` — execute multiple operations in one batch (more efficient than individual runs).
  - `stream(): Promise<IterableReadableStream<StreamOutputMap<...>>>` — primary real-time observation API; emits per enabled `streamMode`.
  - `streamEvents(): IterableReadableStream<StreamEvent>` — stream runnable events.
- **Streaming defaults & modes**
  - `streamMode: StreamMode[]` **defaults to `["values"]`**.
  - Supported modes listed: `"values"` (full state each step), `"updates"` (state changes), `"messages"`, `"custom"`, `"tools"` (tool lifecycle events), `"debug"` (execution tracing). (`stream()` docs also mention `"checkpoints"` and `"tasks"` as streamable event types.)
  - `streamChannels` optional; **if not specified, all channels are streamed**.
- **State persistence / HITL**
  - `checkpointer: boolean | BaseCheckpointSaver<number>` — when provided, **saves a checkpoint at every superstep**; when `false/undefined`, checkpointing disabled and graph **cannot save/restore**.
  - `getState(): Promise<StateSnapshot>` and `getStateHistory(): AsyncIterableIterator<StateSnapshot>` **require a checkpointer**.
  - `updateState(): Promise<RunnableConfig<...>>` — update graph state (requires checkpointer); used for **human-in-the-loop**, breakpoints, external inputs.
  - Interrupt controls: `interruptBefore` / `interruptAfter`: `"*"` or `"__start__"` or `N[]` (node names) to interrupt around nodes.
- **Validation/config defaults**
  - `autoValidate: boolean` **defaults to `true`** (validate structure at compile).
  - `debug: boolean` **defaults to `false`**.
  - `withConfig(...)` returns a **new instance** (immutable merge pattern).
  - `validate(): this` checks: **no orphaned nodes**, valid input/output channels, valid interrupt configs.
- **Graph introspection**
  - `getGraph()` / `getGraphAsync()` return a **drawable** `Graph`.
  - `getSubgraphsAsync()` yields nested Pregel subgraphs (also deprecated sync `getSubgraphs()`).

</details>

### 📖 LangGraph Checkpointing (Threads, Checkpoints, Replay)
**Reference Doc** · [source](https://reference.langchain.com/python/langgraph/checkpoints/)

*checkpointing API surface (checkpointer interfaces/classes), persistence semantics, replay/resume configuration*

<details>
<summary>Key content</summary>

- **Core requirement (config):** to persist/resume, pass `thread_id` in config:  
  `config = {"configurable": {"thread_id": "my-thread"}}`; `graph.invoke(inputs, config)`  
  `thread_id` is the **primary key** for storing/retrieving checkpoints; without it no save/resume/time-travel.
- **Checkpoint metadata (TypedDict):**  
  `source: Literal["input","loop","update","fork"]` (origin of checkpoint)  
  `step: int` with conventions: `-1` = first `"input"` checkpoint; `0` = first `"loop"` checkpoint; increasing thereafter.
- **Checkpoint (TypedDict) fields:**  
  `id: str` (unique, **monotonically increasing**; sortable)  
  `channel_values: dict[str, Any]` (deserialized channel snapshots)  
  `channel_versions: {channel -> version}` (monotonic version strings)  
  `versions_seen: {node_id -> {channel -> version}}` (drives which nodes execute next).
- **BaseCheckpointSaver API (sync + async):** `get`, `get_tuple`, `list`, `put`, `put_writes`, `delete_thread`; async: `aget`, `aget_tuple`, `alist`, `aput`, `aput_writes`, `adelete_thread`; plus `get_next_version(current)->V` (must be monotonically increasing; can be float).
- **Super-step semantics:** checkpoint saved at each **super-step boundary** (“tick” where scheduled nodes run). Resume/replay only from checkpoints.
- **StateSnapshot key fields (for `graph.get_state*`):** `values`, `next: tuple[str,...]`, `config` (includes `thread_id`, `checkpoint_ns`, `checkpoint_id`), `metadata` (includes `source`, `writes`, `step`), `created_at`, `parent_config`, `tasks`.
- **Checkpoint namespace (`checkpoint_ns`):** `""` for root graph; `"node_name:uuid"` for subgraph; nested joined by `|`.
- **Empirical example:** sequential `START->A->B->END` yields **4 checkpoints**: empty/START-next; input/next=A; after A/next=B; after B/next=().
- **Replay rule:** invoke with prior `checkpoint_id` to re-run **after** it; steps **before** are skipped (replayed from saved results). LLM/tool calls/interrupts **after** checkpoint are re-triggered.

</details>

### 📖 LangGraph Functional API `@entrypoint`
**Reference Doc** · [source](https://reference.langchain.com/python/langgraph/func/entrypoint)

*Exact decorator/function signature + runtime semantics (inputs/config binding, execution, persistence)*

<details>
<summary>Key content</summary>

- **Purpose:** `entrypoint` decorator defines a LangGraph workflow in *functional style* (sync or async).
- **Decorator signature (v1.1.6):**  
  `entrypoint(self, checkpointer: BaseCheckpointSaver | None = None, store: BaseStore | None = None, cache: BaseCache | None = None, context_schema: type[ContextT] | None = None, cache_policy: CachePolicy | None = None, retry_policy: RetryPolicy | Sequence[RetryPolicy] | None = None, **kwargs: Unpack[DeprecatedKwargs] = {})`
- **Decorated function signature rule:** must accept **one positional input parameter** (any type). To pass multiple inputs, use a **dict**.
- **Injectable runtime parameters (auto-injected at run time):**
  - `config`: `RunnableConfig` (run-time configuration values)
  - `previous`: previous return value for the same **thread id** (only if `checkpointer` provided)
  - `runtime`: `Runtime` (run info incl. context, store, writer)
- **State management / persistence:**
  - `previous` is available only when a checkpointer is enabled and the same `config["configurable"]["thread_id"]` is used across invocations.
  - To **return one value but checkpoint another**, return `entrypoint.final[value_type, save_type](value=..., save=...)`. Next run’s `previous` receives the **saved** value.
- **Execution patterns:**
  - `.invoke(input, config)` runs once.
  - `.stream(input_or_Command, config)` streams results; can resume after `interrupt(...)` using `Command(resume=...)`.
- **Deprecation:** `config_schema` deprecated since v0.6.0; use `context_schema` (removal in v2.0.0).

</details>

### 📖 LangGraph Runtime Types (interrupts, streaming, state snapshots)
**Reference Doc** · [source](https://reference.langchain.com/python/langgraph/types/)

*Canonical type definitions that constrain what nodes can return/raise and what the runner expects (interrupts, streaming, checkpointing, dynamic sends, state snapshots).*

<details>
<summary>Key content</summary>

- **Interrupting execution (HITL)**
  - `interrupt(value: Any) -> Any`: first call **raises `GraphInterrupt`** and surfaces `value` to the client; graph later resumes via `Command(resume=...)` and **re-executes the node from the start**.
  - Multiple `interrupt()` calls in one node: resume values are matched **by call order**, scoped **per task** (not shared across tasks).
  - **Requires checkpointing enabled** (interrupt relies on persisted state).
  - Interrupt info surfaced in stream as `{'__interrupt__': (Interrupt(value=..., id=...),)}`.
- **Checkpoint configuration**
  - `Checkpointer = None | bool | BaseCheckpointSaver`
    - `True`: enable persistent checkpointing for subgraph
    - `False`: disable even if parent has one
    - `None`: inherit from parent
- **Streaming modes**
  - `StreamMode = Literal["values","updates","checkpoints","tasks","debug","messages","custom"]`
    - `"values"`: emit full state after each step (incl. interrupts)
    - `"updates"`: emit node/task names + returned updates (each update separately if multiple in a step)
    - `"messages"`: token-by-token LLM messages + metadata
    - `"checkpoints"`: emit when checkpoint created (format like `get_state()`)
    - `"tasks"`: task start/finish + results/errors
    - `"debug"`: includes `"checkpoints"` + `"tasks"`
    - `"custom"`: emit via `StreamWriter`
  - `StreamWriter = Callable[[Any], None]`: injected kwarg; **no-op unless** `stream_mode="custom"`.
- **Retry defaults (`RetryPolicy`, v0.2.24)**
  - `initial_interval=0.5s`, `backoff_factor=2.0`, `max_interval=128.0s`, `max_attempts=3`, `jitter=True`.
- **Caching (`CachePolicy`)**
  - `key_func` default: `default_cache_key` (hashes input via pickle).
- **Dynamic fan-out**
  - `Send(node: str, arg: Any)`: used in conditional edges to invoke a node next step with **custom per-send state** (map-reduce style).
- **State snapshot structure (`StateSnapshot`)**
  - `next: tuple[str,...]`, `config: RunnableConfig`, `metadata: CheckpointMetadata|None`, `parent_config: RunnableConfig|None`, `tasks: tuple[PregelTask,...]`.
- **Reducer bypass**
  - `Overwrite(value=...)`: bypass `BinaryOperatorAggregate` reducer; multiple `Overwrite` to same channel in one super-step ⇒ `InvalidUpdateError`.

</details>

### 📖 LangGraph StateGraph node signature + reducers
**Reference Doc** · [source](https://www.langgraphcn.org/reference/graphs/)

*Explicit node signature `State -> Partial<State>` and per-key reducer annotation semantics*

<details>
<summary>Key content</summary>

- **Core abstraction (StateGraph):** Nodes communicate by **reading/writing a shared state**.
- **Node signature (Eq. 1):**  
  **`node: State -> Partial<State>`**  
  Meaning: each node receives the full current `State` and returns a **dict of updates** (a “partial” state) containing only keys it wants to write.
- **Per-key reducers (Eq. 2):**  
  Each state key may be annotated with a **reducer** used to aggregate multiple node updates to that key in the same step.  
  **Reducer signature:** **`reducer: (Value, Value) -> Value`**  
  Used when multiple nodes emit updates for the same key; reducer combines them into one value.
- **Reducer annotation mechanism:** Use `typing_extensions.Annotated` in a `TypedDict` state schema, e.g.  
  `x: Annotated[list, reducer]` (state key `x` is a list aggregated via `reducer`).
- **Edge execution rule:** `add_edge(start_key: str | list[str], end_key: str)`  
  - Single `start_key`: downstream runs after that node completes.  
  - Multiple `start_key` list: downstream waits for **ALL** listed start nodes to complete.
- **Compilation result:** `compile()` returns `CompiledStateGraph` implementing `Runnable` with methods like `invoke`, `stream`, `ainvoke`, `astream`.
- **Streaming modes (enumeration):** `StreamMode ∈ {"values","updates","debug","messages","custom"}`  
  - `"values"`: emit full state after each step  
  - `"updates"`: emit per-node updates/events

</details>

### 📖 LangGraph `streamMode` (CompiledStateGraph) — modes & semantics
**Reference Doc** · [source](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/streamMode)

*Enumerated stream modes, what each yields, and defaults*

<details>
<summary>Key content</summary>

- **Default:** `CompiledStateGraph.streamMode: StreamMode[]` **defaults to `["values"]`**.
- **Supported stream modes (pass to `graph.stream()` / `graph.astream()` via `streamMode`):**
  - **`"values"` → `ValuesStreamPart`:** streams the **full state snapshot after each step**.
  - **`"updates"` → `UpdatesStreamPart`:** streams **state updates after each step**; **multiple updates in the same step are streamed separately**. Output includes **node name → update** mapping.
  - **`"messages"` → `MessagesStreamPart`:** streams **2-tuples `(LLM token/messageChunk, metadata)`** from LLM calls. (Docs note message events can be emitted even when the LLM is run with `.invoke` rather than `.stream`.)
  - **`"custom"` → `CustomStreamPart`:** streams **arbitrary custom data** emitted from nodes via `config.writer(...)` / `get_stream_writer`.
  - **`"checkpoints"` → `CheckpointStreamPart`:** streams **checkpoint events** (same format as `get_state()`).
  - **`"tools"`:** streams tool-call lifecycle events: `on_tool_start`, `on_tool_event`, `on_tool_end`, `on_tool_error`.
  - **`"debug"`:** streams **all available execution info** (node name + full state; “as much information as possible”).
- **Multiple modes at once:** set `streamMode: ["updates","custom", ...]`. Stream yields **tuples `[mode, chunk]`** (mode name + that mode’s data).
- **Unified StreamPart format:** examples use `version="v2"` where each yielded item has `{ type, data, ... }`.
- **Subgraphs:** `subgraphs: true` streams outputs from nested subgraphs; chunks may include a namespace field (e.g., `ns`) to distinguish subgraph vs root.

</details>

### 📖 `StateGraph.compile()` (LangGraph Python)
**Reference Doc** · [source](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

*Exact `StateGraph.compile()` signature/params + compiled graph is a `Runnable` (`invoke/stream/batch/async`)*

<details>
<summary>Key content</summary>

- **Core model (StateGraph):**
  - Nodes communicate via **shared state**.
  - **Node signature:** `State -> Partial<State>` (returns an update dict merged into existing state).
  - **Optional reducers per state key:** annotate a key with a reducer to aggregate multiple updates.
    - **Reducer signature (Eq. 1):** `(Value, Value) -> Value` (left/current, right/update).
- **Must compile to execute:** `StateGraph` is a **builder**; call `.compile()` to get an executable graph supporting `invoke()`, `stream()`, `ainvoke()`, `astream()`.
- **`compile()` signature (Python):**
  ```python
  compile(
    checkpointer: Checkpointer = None,
    *,
    cache: BaseCache | None = None,
    store: BaseStore | None = None,
    interrupt_before: All | list[str] | None = None,
    interrupt_after: All | list[str] | None = None,
    debug: bool = False,
    name: str | None = None,
  ) -> CompiledStateGraph[StateT, ContextT, InputT, OutputT]
  ```
  - **Defaults:** `checkpointer=None`, `cache=None`, `store=None`, `interrupt_before=None`, `interrupt_after=None`, `debug=False`, `name=None`.
  - **Return:** `CompiledStateGraph` implementing **Runnable** (invokable, streamable, batchable, async).
- **Execution flow procedure (Quickstart):**
  1. Define `State` schema (e.g., `TypedDict`).
  2. Write node functions returning partial updates.
  3. Add nodes + edges (`START` → …).
  4. `app = graph.compile()` then `app.invoke(initial_state)`.
- **Conditional looping example:** `add_conditional_edges("increment", should_continue)` where `should_continue` returns `"increment"` until `count < 3`, else `END`; result reaches `count: 3`.

</details>

### 📋 # Source: https://danielfridljand.de/post/temporal-human-in-the-loop
**Source** · 

### 📋 # Source: https://docs.temporal.io/ai-cookbook/human-in-the-loop-python
**Source** · 

### 📋 # Source: https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/functional_api.md
**Source** · 

### 📋 # Source: https://github.com/langchain-ai/langgraph/blob/main/docs/docs/concepts/persistence.md
**Source** · 

### 📋 # Source: https://github.com/langchain-ai/langgraph/issues/1568
**Source** · 

### 🔍 Atomic message replacement vs reducers (LangGraph StateGraph)
**Explainer** · [source](https://github.com/langchain-ai/langgraph/discussions/3810)

*Node return-type rules + reducer semantics (replace vs append) + replay/idempotency implications*

<details>
<summary>Key content</summary>

- **StateGraph contract (Core rule):** Each node reads **State** and returns a **Partial\<State\>** update. Returned keys are merged into shared state.
- **Reducer semantics (per-key aggregation):** A state key can be annotated with a reducer used to combine multiple updates.  
  **Reducer signature (Eq. 1):** `reducer(left: Value, right: UpdateValue) => Value`  
  - `left` = current accumulated state value  
  - `right` = node’s returned update for that key
- **Append-style messages reducer (example):**  
  `messages: Annotation<BaseMessage[]>({ reducer: (left, right) => left.concat(Array.isArray(right) ? right : [right]), default: () => [] })`  
  **Default:** `messages` starts as `[]`.
- **Implication for “replace history atomically”:** If `messages` uses an **append reducer**, returning `{"messages": [...]}` will **append**, not overwrite. To **overwrite/replace**, define `messages` with a reducer that **returns `right` as the new value** (i.e., replacement reducer) so the update is atomic at the state-key level.
- **Idempotency / replay rationale:** Durable execution + retries/replay can re-run nodes; **append reducers can duplicate messages** on re-execution. Replacement reducers (or otherwise idempotent update logic) avoid duplication by making the update deterministic for a given run.
- **Execution workflow:** Build graph (`addNode`, `addEdge(START, node)`, `addEdge(node, END)`), then **must call** `.compile()` before `.invoke()`.

</details>

### 🔍 Blackboard System Architecture & Control Cycle
**Explainer** · [source](https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf)

*Architecture-level decomposition (blackboard, knowledge sources, control) + event-driven control/message flow for opportunistic problem solving.*

<details>
<summary>Key content</summary>

- **Core components (Basic Blackboard Architecture, Summary sections):**
  - **Blackboard** = *global database containing ALL solution-state data*; organized into **levels** (often matching a solution decomposition / abstraction hierarchy) and **nodes** (attribute–value structures). Nodes can be **created/deleted dynamically**; nodes across levels can be **linked** (inter-node relations).
  - **Knowledge Sources (KSs)** = event-triggered specialist modules (“demons”) containing rules/procedures/tables; **only KSs may modify the blackboard**; KSs are **procedurally independent** (no KS references another KS directly).
  - **Control component** = event-based scheduling: selects focus of attention (context), selects events, selects and invokes triggered KS instances.

- **KS protocol / structure (Knowledge Sources summary):**
  - **Condition part** often split into **trigger** (event tokens) + **precondition** (executability test) + other filters.
  - **Action part** performs blackboard modifications, I/O, and **posts events**.

- **Primitive knowledge application cycle (Control III):**
  1) **Select an event**  
  2) **Select KS(s) triggered** by that event (in the event’s context)  
  3) **Execute KS instance** → **creates new events** (repeat)

- **Event-driven control loop with multiple event lists (Control Design Choices / Control Flow):**
  - Loop: **Select event list → select event(s) → determine triggered KSs → invoke KS(s)**.
  - Supports **clocked events** (activate when evaluation-time ≤ current time) and **periodic events** (repost with time incremented by Δt).
  - Scheduling alternatives: round-robin vs fixed priority vs dynamic utility weights; FIFO/LIFO/priority by token or time&token; execute one vs all triggered KSs.

- **Concrete example numbers (PROTEAN/881 state example):** Agenda shows **Executable: 98, 94, 86** (rated KSARs), illustrating rating-based scheduling.

</details>

### 🔍 Conditional Edges & Dynamic Routing Semantics (LangGraph)
**Explainer** · [source](https://github.com/langchain-ai/langgraph/discussions/3346)

*Conditional edge routing function signatures + runtime evaluation semantics (how next nodes are chosen/applied)*

<details>
<summary>Key content</summary>

- **Node function contract (core pattern):** `node(state) -> dict` returning **partial state updates** (e.g., `{"messages": [new_msg]}`), which are merged into graph state via reducers (example uses `add_messages` to **append** rather than overwrite).
- **Conditional edge procedure (runtime routing):**
  1. Execute a node (e.g., `"chatbot"`) to produce state updates.
  2. Evaluate a **routing function** on the current input (either a messages list or a state dict containing `"messages"`).
  3. Routing function returns a **label** (e.g., `"tools"` or `END`).
  4. `add_conditional_edges(from_node, router, mapping)` interprets router outputs via an optional **mapping dict** (defaults to identity if omitted).
- **Routing function signature/semantics (example `route_tools(state)`):**
  - Accepts either:
    - `state: list` (treated as messages; uses `state[-1]`), or
    - `state: dict` with `state.get("messages", [])` (uses last message).
  - Decision rule:
    - If last AI message has attribute `tool_calls` and `len(tool_calls) > 0` ⇒ return `"tools"`
    - Else ⇒ return `END`
  - Error behavior: if no messages found ⇒ raises `ValueError("No messages found...")`.
- **Looping design rationale:** After tool execution, add a normal edge `"tools" -> "chatbot"` so the LLM can decide next step; this forms the main agent loop.
- **Default/parameter notes shown:**
  - Conditional mapping example: `{"tools": "tools", END: END}` (lets you rename targets, e.g., `"tools": "my_tools"`).
  - Human-in-the-loop tool example asserts `len(message.tool_calls) <= 1` to avoid repeated invocations on resume when interrupts/checkpointing are used.

</details>

### 🔍 Custom state reducers beyond `add_messages`
**Explainer** · [source](https://github.com/langchain-ai/langgraph/discussions/3459)

*Concrete guidance and pointers on custom reducers beyond `add_messages`, incl. official “Reducers” concept section + state-reducers how-to.*

<details>
<summary>Key content</summary>

- **Reducer definition (per-state-key):** Each key/channel in LangGraph `State` has an **independent reducer** that merges a node’s *update* into the prior state value.  
  - **Default reducer (override):** if no reducer specified, updates **replace** the prior value.
- **Reducer function form (Eq. 1):**  
  `new_value = reducer(old_value, update_value)`  
  - `old_value`: current state value for that key  
  - `update_value`: partial update returned by a node for that key
- **Procedure: define reducers in state schema**
  - **JS/TS (Annotation):**
    ```ts
    const State = Annotation.Root({
      bar: Annotation<string[]>({
        reducer: (state, update) => state.concat(update),
        default: () => [],
      }),
    });
    ```
  - **Python (conceptual parallel):** define a typed state schema and attach reducer logic per field (messages commonly use a prebuilt reducer).
- **Concrete behavior examples**
  - **Example A (no reducers):** input `{foo:1, bar:["hi"]}`; node returns `{foo:2}` ⇒ state `{foo:2, bar:["hi"]}`; later `{bar:["bye"]}` ⇒ `{foo:2, bar:["bye"]}` (overwrite).
  - **Example B (custom reducer for `bar`):** with `concat` reducer + default `[]`; input `{foo:1, bar:["hi"]}`; later update `{bar:["bye"]}` ⇒ `{foo:1, bar:["hi","bye"]}`.
- **Design rationale for messages reducer:** naive `concat` breaks **manual edits** (e.g., human-in-the-loop) because it always appends; `messagesStateReducer` handles **message IDs** (overwrite existing) and **deserializes** OpenAI-style `{role, content}` into LangChain `BaseMessage`.
- **Prebuilt state:** `MessagesAnnotation` / `MessagesState` provides `messages: BaseMessage[]` with `messagesStateReducer`; can be extended via `...MessagesAnnotation.spec`.

</details>

### 🔍 Durable Human-in-the-Loop with Temporal (Signals, Waits, Queries)
**Explainer** · [source](https://learn.temporal.io/tutorials/ai/building-durable-ai-applications/human-in-the-loop/)

*Step-by-step mechanics for durable approval gates (signals + wait_condition + query) with retry-safe state persistence.*

<details>
<summary>Key content</summary>

- **Core rationale (durability for HITL):**
  - Human decisions are **durably stored in Workflow history**; after crashes/timeouts, the Workflow **resumes without re-asking** for approval.
  - `workflow.wait_condition(...)` pauses without consuming CPU; Temporal records the “waiting” checkpoint and resumes only when condition becomes true.

- **Signal data model (Step 1):**
  - `UserDecision = {KEEP, EDIT, WAIT}` (enum).
  - `UserDecisionSignal(decision: UserDecision, additional_prompt: str="")` (dataclass).

- **Workflow state persistence (Step 2):**
  - Instance vars persist across execution/replay:
    - `_current_prompt: str`
    - `_user_decision: UserDecisionSignal = UserDecisionSignal(decision=WAIT)`
    - (for queries) `_research_result: str = ""`

- **Signal handler (Step 3):**
  - `@workflow.signal async def user_decision_signal(decision_data): self._user_decision = decision_data`

- **Approval/edit loop (Step 4 + waiting):**
  - Loop:
    1) `research_facts = execute_activity(llm_call, start_to_close_timeout=30s)`
    2) Store for query: `_research_result = research_facts["choices"][0]["message"]["content"]`
    3) **Gate:** `await workflow.wait_condition(lambda: _user_decision.decision != WAIT)`
    4) If `KEEP`: exit loop → `create_pdf` activity (`start_to_close_timeout=20s`)
    5) If `EDIT`: append `additional_prompt` to `_current_prompt`, set `llm_call_input.prompt`, then **reset** `_user_decision = WAIT` and repeat.

- **Query support:**
  - `@workflow.query def get_research_result(self)->str: return _research_result`
  - Queries are synchronous read-only; **do not create history events**; can query during/after completion.

- **Client interactions:**
  - `handle = client.get_workflow_handle(workflow_id)`
  - Send signal: `await handle.signal("user_decision_signal", UserDecisionSignal(decision=KEEP|EDIT,...))`
  - Query: `await handle.query(GenerateReportWorkflow.get_research_result)`

</details>

### 🔍 Durable LangGraph Agents w/ DynamoDBSaver
**Explainer** · [source](https://aws.amazon.com/blogs/database/build-durable-ai-agents-with-langgraph-and-amazon-dynamodb/)

*End-to-end durable agent architecture using LangGraph + DynamoDB as checkpoint store (schema/flow for resume/replay)*

<details>
<summary>Key content</summary>

- **Why LangGraph (graph control flow):** Define **nodes** (tasks) and **edges** (control flow) that can **branch, merge, and loop** (cyclic graphs), enabling complex, stateful workflows beyond linear chains.
- **Core persistence concepts (LangGraph):**
  - **Thread** = unique identifier for accumulated state across runs; must pass `thread_id` in config:  
    **Eq. 1 (Thread config):** `{"configurable": {"thread_id": "1"}}`
  - **Checkpoint** = snapshot saved each **super-step** as a `StateSnapshot` containing: config, metadata, state channel values, next nodes to execute, and task info (errors/interrupts).
  - Example: a **2-node graph** yields **4 checkpoints**: empty at `START`, after user input (before `node_a`), after `node_a` output (before `node_b`), final after `node_b` at `END`.
- **Why persistence matters (production rationale):** In-memory checkpoints are **ephemeral + local** → lost on restart; multi-worker runs have isolated state → cannot resume across workers or recover mid-run. Persistent store enables **resume, replay, human-in-the-loop, time travel debugging, audit**.
- **DynamoDBSaver design (langgraph-checkpoint-aws):**
  - **Small checkpoint threshold:** `< 350 KB` stored directly in **DynamoDB** (serialized item + metadata: `thread_id`, `checkpoint_id`, timestamps, state).
  - **Large checkpoints:** `≥ 350 KB` state stored in **S3**; DynamoDB stores an S3 pointer; retrieval transparently loads from S3.
  - **Cost/lifecycle knobs:** `ttl_seconds` (auto-expire checkpoints) and `enable_checkpoint_compression` (serialize+compress to reduce DynamoDB/S3 costs).
- **Required DynamoDB table schema:** partition key **`PK` (String)** and sort key **`SK` (String)**.
- **IAM permissions (minimum):**
  - DynamoDB: `GetItem`, `PutItem`, `Query`, `BatchGetItem`, `BatchWriteItem`
  - S3 (large checkpoints): `PutObject`, `GetObject`, `DeleteObject`, `PutObjectTagging`, plus bucket lifecycle `GetBucketLifecycleConfiguration`, `PutBucketLifecycleConfiguration`.

</details>

### 🔍 Durable execution + interrupt/resume + state updates (LangGraph #4730)
**Explainer** · [source](https://github.com/langchain-ai/langgraph/discussions/4730)

*Concrete edge-case behavior context: state persistence + interrupt/resume patterns (esp. around human-in-the-loop) and how state is updated via reducers; pointers to subgraph concepts for nested graphs.*

<details>
<summary>Key content</summary>

- **LangGraph core model (Graphs as control flow):**
  - **State** = shared snapshot passed to nodes; defined as `TypedDict`/Pydantic + **reducers** that specify how updates apply.
  - **Nodes**: functions `node(state) -> dict` emitting partial state updates.
  - **Edges**: determine next node(s); can be conditional or fixed.
  - Runtime proceeds in discrete **“super-steps”** (Pregel-inspired): nodes execute, emit messages along edges; execution halts when all nodes are inactive and no messages are in transit.
- **Reducer formula (state update rule):**
  - For key `messages` with reducer `add_messages`: **append** new messages rather than overwrite.  
    Example reducer shown: `messages: Annotated[list, lambda x, y: x + y]` where `x`=prior list, `y`=new list.
  - Keys **without** reducer annotations **overwrite** previous values.
- **Durable execution / memory procedure (checkpointing):**
  1. Compile graph with a `checkpointer` (example: `memory = MemorySaver(); graph = builder.compile(checkpointer=memory)`).
  2. Invoke with `configurable.thread_id` to persist/load state across calls.
  3. State is saved after each step; later invocations with same `thread_id` resume from saved checkpoint.
- **Human-in-the-loop procedure (interrupt/resume):**
  - Tool uses `interrupt({"query": query})` and returns `human_response["data"]`.
  - **Design rationale:** disable parallel tool calling when interrupts can occur to avoid repeating tool invocations on resume: `assert len(message.tool_calls) <= 1`.
- **Defaults/parameters shown:**
  - `TavilySearch(max_results=2)`
  - Example recursion limit usage: `graph.invoke(..., {"recursion_limit": 10})`.

</details>

### 📋 Dynamic Workflow Mode for Conditional Edges (workflow_mode)
**Code** · [source](https://github.com/langchain-ai/langgraph/pull/3345)

*PR description of an alternate conditional-edge execution procedure + compile-time flag (`workflow_mode=True`) and requirements (`path_map` or `Literal`)*

<details>
<summary>Key content</summary>

- **Problem (conditional edges + parallelism):**
  - Workflow expectation: **each node executes only once** unless explicitly handled otherwise.
  - In conditional branching (selector node **A** with branches **Type 1** and **Type 2**) where **both branches converge to node E**, LangGraph’s **parallel processing** can cause **node E to execute only once** (i.e., convergence behavior depends on runtime scheduling/structure rather than intended workflow semantics).
  - Reported discrepancy: adding an extra node **D** after **B** (without changing logical intent) can change whether **E executes once or twice**, implying non-rigorous conditional-edge triggering based on graph shape.

- **Proposed solution / procedure: “Dynamic Workflow Mode”**
  - Add an **Analyzer** that **maintains the directed graph of actual execution paths** during runtime.
  - During execution, **dynamically adjust trigger conditions for subsequent nodes** based on the **actual path taken**, so nodes in the workflow execute **exactly once** per run (unless special logic says otherwise).
  - Rationale: because nodes/paths are **dynamically generated**, **branch paths can’t be fully determined pre-execution**, so path selection must be **dynamic at runtime**.

- **Configuration / defaults:**
  - Enable via compilation: `compile(workflow_mode=True)`.
  - **When `workflow_mode=True`:** must provide **either** `path_map` **or** a `Literal` return type for the conditional function (**only one required**).
  - `path_map`/`Literal` must **cover all possible execution paths**.
  - Default: if `workflow_mode` is unset or `False`, **original LangGraph execution mode** is used (backward compatible).

</details>

### 📋 LangGraph + gotoHuman human-approval (interrupt/resume) lead-email agent
**Code** · [source](https://github.com/gotohuman/gotohuman-langgraph-lead-example)

*End-to-end LangGraph + external human review integration surface (webhook-driven interrupt/resume), with persistence/checkpointing via Postgres env var.*

<details>
<summary>Key content</summary>

- **Workflow (end-to-end procedure):**
  1. **Trigger** agent with a new lead email address.
     - **API trigger:** `HTTP POST [DEPLOY_URL]/api/agent` with JSON body: `{ "email": "new.lead@email.com" }`.
     - **Manual trigger in gotoHuman:** create a trigger form with a text input field **ID `email`** and configure the same webhook URL.
  2. Agent researches + drafts a personalized outreach email (LangGraph).
  3. Agent **requests human review/approval** in gotoHuman; reviewers see it in **gotoHuman inbox**.
  4. **Webhook callback** is invoked **for each review response** to **resume the graph** (interrupt/resume pattern).
  5. Human can **revise** draft before final send (approval workflow).
- **Review form setup:**
  - Import gotoHuman form template with **ID `OmmAnhbnWmird3oz60q2`**.
  - Configure **webhook URL** (deployment URL) used to resume execution after review.
  - Optional: generate a **short-lived public link** to share with reviewers.
- **Deployment/config defaults (env vars):**
  - `OPENAI_API_KEY=sk-proj-XXX`
  - `GOTOHUMAN_API_KEY=XYZ`
  - `GOTOHUMAN_FORM_ID=abcdef123`
  - `POSTGRES_CONN_STRING="postgres://..."`
- **Design rationale:** use gotoHuman as a **central dashboard** for approving critical actions/providing input; integrates with LangGraph via webhook to enable **durable, resumable** human-in-the-loop execution.

</details>

### 📋 LangGraph `add_messages` reducer (exact merge + deletion semantics)
**Code** · [source](https://github.com/langchain-ai/langgraph/blob/main/libs/langgraph/langgraph/graph/message.py)

*Reference implementation of message-state reducer utilities (`add_messages`), including ID-based merging, conversion helpers, and `RemoveMessage` behavior.*

<details>
<summary>Key content</summary>

- **Reducer signature (Eq. 1):**  
  `add_messages(left, right, *, format: Literal["langchain-openai"]|None=None) -> Messages`  
  - `Messages = list[MessageLikeRepresentation] | MessageLikeRepresentation`
- **Wrapper behavior:** must pass **both** `left` and `right` (non-null) or neither (returns `partial`); else raises `ValueError("Must specify non-null arguments for both 'left' and 'right'...")`.
- **Coercion pipeline (Procedure A):**
  1. If `left`/`right` not a list → wrap into list.
  2. Convert to `BaseMessage` via `convert_to_messages(...)`.
  3. Convert chunks to full messages via `message_chunk_to_message(...)`.
  4. **Assign missing IDs:** if `m.id is None` → `m.id = str(uuid.uuid4())` (done for all in `left` and `right`).
- **Remove-all sentinel (Procedure B):**
  - Constant: `REMOVE_ALL_MESSAGES = "__remove_all__"`.
  - If any `RemoveMessage` in `right` has `m.id == REMOVE_ALL_MESSAGES`, return **only** messages **after** that index: `right[remove_all_idx+1:]` (drops all prior state).
- **ID-based merge rule (Eq. 2):**
  - Build `merged = left.copy()` and `merged_by_id = {m.id: index}`.
  - For each `m` in `right`:
    - If `m.id` exists: replace `merged[existing_idx] = m`. If `m` is `RemoveMessage`, mark ID for deletion.
    - If `m.id` missing in `left`:
      - If `m` is `RemoveMessage` → **error**: deleting non-existent ID.
      - Else append and record index.
  - After loop: filter out IDs marked for deletion.
- **Formatting parameter:**
  - `format=="langchain-openai"` → `_format_messages` uses `convert_to_openai_messages` then `convert_to_messages`.
  - Any other truthy `format` → `ValueError("Unrecognized format=...")`.
- **State schema helper:**  
  `MessagesState(TypedDict): messages: Annotated[list[AnyMessage], add_messages]`
- **Deprecation:** `MessageGraph(StateGraph)` is deprecated (since v1.0.0; removed v2.0.0); it uses `Annotated[list[AnyMessage], add_messages]` as the whole state.

</details>

### 🔍 LangGraph execution + state editing (super-steps, reducers, checkpoints)
**Explainer** · [source](https://github.com/langchain-ai/langgraph/discussions/938)

*End-to-end execution model (state representation, manual edits, update semantics) + how it relates to checkpoints/threads*

<details>
<summary>Key content</summary>

- **Graph primitives (definition):**  
  - **State** = shared snapshot (schema + per-key **reducers**).  
  - **Nodes** = functions that take current `state` (optionally `config`, `runtime`) and **return partial updates** (dict of keys→values).  
  - **Edges** = routing logic (fixed or conditional) selecting next node(s).
- **Execution model (Pregel-like “super-steps”):**  
  - Nodes start **inactive**; become **active** when they receive a message (state) on an incoming edge/channel.  
  - Active nodes run, emit updates/messages; recipients run in the **next super-step**.  
  - Nodes with no incoming messages “vote to halt” (become inactive).  
  - **Termination condition:** all nodes inactive **and** no messages in transit.
- **Reducers (per state key):**  
  - Default reducer = **overwrite** (latest update replaces prior value).  
  - Example reducer for chat history: `add_messages` appends to `messages` and handles message IDs + deserialization.
- **Parallelism rule:** if a node has **multiple outgoing edges**, **all** destination nodes execute **in parallel** in the next super-step.
- **Schema filtering + write-anywhere rule:** nodes may **write to any channel** in the graph’s *internal* state union, even if their **input schema** is a subset (input/output schemas can filter external I/O).
- **Checkpointing/thread config:** state snapshots include `values`, `next`, and `config` with `thread_id` + `checkpoint_id`; using the same `thread_id` reloads saved state for multi-turn continuity.
- **Human-in-the-loop procedure:** `interrupt(prompt_or_payload)` pauses; resume via `graph.invoke(Command(resume=...))`. Example: first call pauses; second call resumes with `"yes"`.

</details>

### 🔍 LangGraph v0.2 — Checkpointers, durability, replay/resume
**Explainer** · [source](https://blog.langchain.com/langgraph-v0-2/)

*Maintainer rationale for standardizing checkpointer interfaces; how persistence enables durable, replayable graph/state execution.*

<details>
<summary>Key content</summary>

- **Core design pillar:** LangGraph includes a built-in **persistence layer** via **checkpointers**. A checkpointer **saves a checkpoint of graph state at each step** (step-level durability).
- **Capabilities enabled by step checkpoints:**
  - **Session memory:** store checkpoint history of user interactions; **resume** from a saved checkpoint in follow-up interactions.
  - **Error recovery:** **continue from last successful step checkpoint** after failures.
  - **Human-in-the-loop:** tool approval, wait for human input, edit agent actions.
  - **Time travel / forking:** edit graph state at any point in execution history and create an alternative execution from that point (“fork the thread”).
- **Rationale for v0.2 changes:** community demand for DB-specific checkpointers (Postgres/Redis/MongoDB) existed, but **no clear blueprint** for custom implementations; v0.2 introduces **standardized interfaces + dedicated libraries** to simplify creation/customization and foster a community ecosystem.
- **New checkpointer library ecosystem (interchangeable implementations):**
  - `langgraph_checkpoint`: base interfaces **`BaseCheckpointSaver`**, **`SerializationProtocol`**; includes **`MemorySaver`** (in-memory).
  - `langgraph_checkpoint_sqlite`: **SQLite** implementation (local/experimentation).
  - `langgraph_checkpoint_postgres`: production-grade **Postgres** implementation (open-sourced from LangGraph Cloud).
- **Postgres checkpointer optimizations:**
  - Write-side: **Postgres pipeline mode** to reduce roundtrips; store **each channel value separately and versioned** so each checkpoint stores **only changed values**.
  - Read-side: **cursor** for list endpoint to efficiently fetch long thread histories.
- **Imports / installs (namespace packages):**
  - `from langgraph.checkpoint.base import BaseCheckpointSaver`
  - `from langgraph.checkpoint.memory import MemorySaver`
  - `from langgraph.checkpoint.sqlite import SqliteSaver` (requires `pip install langgraph-checkpoint-sqlite`)
  - `from langgraph.checkpoint.postgres import PostgresSaver` (requires `pip install langgraph-checkpoint-postgres`)
- **Versioning:** checkpointer libs follow **semantic versioning starting at 1.0**; breaking changes in main interfaces → **major bump** (e.g., `langgraph_checkpoint` 2.0 implies implementations update to 2.0).
- **Breaking rename:** `thread_ts` → `checkpoint_id`; `parent_ts` → `parent_checkpoint_id` (still recognized if passed via config).

</details>

### 🔍 Markov Games (Multi-Agent RL) + Minimax-Q
**Explainer** · [source](https://www.cs.cmu.edu/~./15281-f19/lectures/15281_Fa19_Lecture_26_MARL.pdf)

*Formal Markov game definition; value/objectives; reduction from MDP to multi-agent; Minimax-Q update + LP.*

<details>
<summary>Key content</summary>

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

</details>

### 🔍 Merging state after parallel nodes (reducers + ordering)
**Explainer** · [source](https://github.com/langchain-ai/langgraph/discussions/3914)

*How LangGraph combines state updates from parallel branches; reducer requirements; what ordering/determinism to expect.*

<details>
<summary>Key content</summary>

- **Execution/merge model (parallel branches):**
  - When multiple nodes run “in parallel” and each returns a partial state update (a dict), LangGraph **merges updates field-by-field** using the state schema’s **reducers**.
  - **Reducer signature (Eq. 1):** `reducer(existing_value, new_value) -> updated_value`
- **Reducer annotation in typed state (procedure):**
  - Define a `TypedDict` state and annotate merge behavior with `typing.Annotated[field_type, reducer]`.
  - Example (code pattern):
    - `count: Annotated[int, operator.add]`  → updates **accumulate** (`count += delta`)
    - `data: Annotated[dict, merge_dicts]` where `merge_dicts(existing, new) = {**existing, **new}`
    - `messages: Annotated[list, add_messages]` → appends messages; `add_messages` is the recommended reducer for chat history (handles duplicates by message ID).
- **Default behavior (important):**
  - **Without a reducer**, a field update **overwrites** the existing value (last write wins), so parallel branches can appear to “not merge.”
- **Built-in reducers / common choices:**
  - `operator.add`: sums numbers / concatenates lists.
  - `operator.or_`: merges dicts (with overwrite on key conflicts).
  - Custom reducers for policies like max: `keep_max(existing, new) = max(existing, new)`.
- **Ordering expectation (design rationale):**
  - For parallel updates, **do not rely on branch completion order** for correctness; instead, make merges deterministic by using appropriate reducers (especially for lists/messages).

</details>

---

## Related Topics

- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/function-calling|Function Calling]]
- [[topics/agent-skills-safety|Agent Skills & Safety]]
- [[topics/agent-workflows|Agent Workflows]]
