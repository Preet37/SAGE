## Core Definitions

**Message passing.** Message passing is a coordination mechanism where agents communicate by sending discrete messages (often natural language or structured payloads) that become the other agents’ observations and drive their next actions. In AutoGen’s *GroupChat*, messages are stored in a shared `messages` list and a manager selects the next speaker based on configuration (e.g., `"auto"`, `"round_robin"`) and constraints like `func_call_filter` (AutoGen GroupChat docs: https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/).

**Shared state.** Shared state is a common, persistent representation of “what we know so far” that multiple agents read from and/or write to while solving a task. In the HLER pipeline, a central orchestrator maintains a shared **RunState** that records intermediate outputs as structured objects passed forward through stages (HLER paper: https://arxiv.org/html/2603.07444v1). In blackboard systems, the **blackboard** is explicitly “the global database containing all solution-state data,” organized into levels and nodes (Stanford blackboard explainer: https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf).

**Blackboard pattern.** The blackboard pattern is a shared-state coordination architecture with three parts: (1) a **blackboard** (global solution state), (2) **knowledge sources (KSs)**—specialist modules that are procedurally independent and (in the classic formulation) are the only components allowed to modify the blackboard—and (3) a **control component** that schedules which KS runs next based on events/agenda ratings (Stanford blackboard papers: https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf and https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf).

**Handoffs.** A handoff is an explicit transfer of control/responsibility from one agent (or stage) to another, typically accompanied by a state snapshot or structured artifact so the next agent can continue without re-deriving context. In HLER, handoffs occur stage-to-stage (e.g., Data Profiling → Questioning) via structured objects stored in RunState (https://arxiv.org/html/2603.07444v1). In AutoGen GroupChat, a “handoff” is operationalized as *speaker selection*—the manager chooses the next agent to act (https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/).

**Human-in-the-loop (HITL).** Human-in-the-loop is a control pattern where a human is inserted as a decision-maker at specific gates or interrupts to ensure oversight, especially for high-stakes choices or quality thresholds. HLER uses two explicit human decision gates: (1) **Research Question Selection** and (2) **Publication Decision** (https://arxiv.org/html/2603.07444v1). LangGraph highlights “human-in-the-loop” as a core orchestration capability: inspecting and modifying agent state at any point during execution (LangGraph docs landing page: https://langchain-ai.github.io/langgraph/).

**Conflict resolution.** Conflict resolution is the mechanism for reconciling inconsistent agent outputs or competing hypotheses/actions. In the SEC filing extraction benchmark, the parallel fan-out + merge architecture resolves conflicts via a **confidence-weighted voting** merge agent; hierarchical supervisors reassign low-confidence fields using a **confidence threshold (0.85)** and capped iterations; reflexive loops use verifier checks (format, cross-field consistency, source grounding) with bounded correction iterations (SEC benchmark: https://arxiv.org/pdf/2603.22651.pdf). In blackboard systems, conflict resolution can be implemented via the control component’s scheduling/agenda selection (event-driven selection of which KS to run next) (Stanford blackboard explainer: https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf).

**Scaling (multi-agent coordination).** Scaling refers to maintaining acceptable accuracy/reliability while increasing throughput, concurrency, or task size—often requiring architectural changes (sequential vs parallel vs hierarchical vs reflexive) and operational controls (iteration caps, caching, routing). The SEC benchmark reports that reflexive architectures degrade fastest at high volume (e.g., F1 drops from **0.943→0.871** when scaling **1K→100K docs/day**) due to queueing/timeouts truncating correction loops, while sequential is more resilient (**0.903→0.886**) (https://arxiv.org/pdf/2603.22651.pdf).

---

## Key Formulas & Empirical Results

### Speculative Actions expected runtime ratio (predict–verify)
From “Speculative Actions” (https://arxiv.org/html/2510.04371v1):

\[
\frac{\mathbb{E}[T_{\text{spec}}]}{\mathbb{E}[T_{\text{seq}}]}=\frac{1}{2-p}\left(1+\frac{l}{L}\right)
\]

- **Variables:**  
  - \(L\): mean latency of the actual (authoritative) API/tool call  
  - \(l\): mean latency of the speculative model (with \(l < L\))  
  - \(p\): probability the speculator correctly predicts the next call  
- **Claim supported:** speculation can reduce end-to-end latency by overlapping future tool calls; idealized bound implies up to ~50% reduction as \(l\to 0\), \(p\to 1\) (single-step), with multi-step speculation potentially exceeding.

**Empirical:** next-action prediction accuracy “up to **55%**” and “up to **20%** end-to-end lossless speedup” (same source).

### SPAgent (speculation + scheduling) empirical latency
From SPAgent (https://arxiv.org/html/2511-20048v1):

- Directly sampled speculative actions match post-reasoning action **73.4% at step 1**, dropping to **~11%** later steps.
- Tool latency in setup: Wikipedia API **~1.5s/request**.
- Serving results: **24.2% mean latency reduction on average, up to 69.6%** vs naive; under load > **2 rps**, “Speculative Actions” can become **up to 49.3% slower than naive** (scheduling/load sensitivity).
- Default speculative samples: **k=4** (diminishing returns beyond).
- Action Buffer memory footprint: **~200 Bytes/task**.

### SEC filing extraction benchmark: architecture trade-offs + scaling
From (https://arxiv.org/pdf/2603.22651.pdf), Claude 3.5 Sonnet:

**Primary results (Table III):**
- Sequential: **F1 0.903**, cost **$0.187**, latency **38.7s**
- Parallel: **F1 0.914**, cost **$0.221**, latency **21.3s**
- Hierarchical: **F1 0.929**, cost **$0.261**, latency **46.2s**
- Reflexive: **F1 0.943**, cost **$0.430**, latency **74.1s**

**Implementation defaults:**
- Extraction calls temperature **0.0**; supervisor/critique **0.3**
- Hierarchical confidence threshold **0.85**
- Max iterations: hierarchical re-extraction **2**; reflexive correction **3**

**Scaling (Table IX):**
- Reflexive F1 **0.943→0.871** from **1K→100K docs/day**
- Sequential F1 **0.903→0.886** over same scale
- Interpretation in paper: reflexive degrades fastest due to queueing/timeouts truncating correction loops.

### HLER pipeline: feasibility + ops metrics + HITL gates
From (https://arxiv.org/html/2603.07444v1):

- Human decision gates: **Research Question Selection**, **Publication Decision**
- Dataset-aware question feasibility: **87% (69/79)** vs unconstrained **41% (34/82)**  
  - Unconstrained failures: **42%** missing variables; **35%** design incompatible
- End-to-end completion: **86% (12/14)** runs completed; 2 failed at econometrics with graceful halt + logs
- Revision loop improves reviewer scores: mean **4.8 → 5.9 → 6.3** (v1, v2, final); biggest gains clarity **+2.1**, identification **+1.4**
- Ops metrics: runtime **20–25 min/run**; API cost **$0.8–$1.5/run**

### ESAA: event-sourced orchestration verification + overheads
From (https://arxiv.org/html/2602.23193v1):

- Event log: `activity.jsonl` append-only ordered by `event_seq`
- Projection hash: `projection_hash_sha256 = SHA256(canonicalize(roadmap.json))` (canonicalization aligned with RFC 8785 JCS per paper)
- Concurrency model: agents can run in parallel, but results are validated and appended **sequentially** to preserve total order
- Overhead: JSON envelope + validation preamble **~200–500 tokens/invocation**; validation+persistence **sub-second/event**

### AutoGen GroupChat defaults (speaker selection / constraints)
From (https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/):

- `admin_name` default **"Admin"**; KeyboardInterrupt causes admin takeover
- `speaker_selection_method` default **"auto"**
- `func_call_filter` default **True** (function-call suggestion constrains next speaker to an agent that can execute that function)
- `max_retries_for_selecting_speaker` default **2**
- `allow_repeat_speaker` default **True**
- Auto speaker selection uses a nested two-agent chat (selector + validator); fallback after retries is “next agent in list”

---

## How It Works

### A. Blackboard coordination control cycle (classic event-driven)
From Stanford blackboard explainer (https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf):

1) **Blackboard holds global solution state** organized into levels/nodes; nodes can be created/deleted dynamically and linked across levels.  
2) **Knowledge Sources (KSs)** watch for relevant changes via **events** (event tokens).  
3) Each KS has:
   - **Trigger**: what event types activate it
   - **Precondition/executability tests**: whether it should run now
   - **Action**: modifies blackboard, performs I/O, and **posts new events**
4) **Control component loop** (“primitive knowledge application cycle”):
   1. Select an event  
   2. Select KS(s) triggered by that event (in context)  
   3. Execute a KS instance → creates new events → repeat
5) **Conflict resolution via scheduling:** if multiple KSs are triggered, the control component chooses which to run (priority, utility weights, FIFO/LIFO, etc.; scheduling alternatives described in the same source).

Tutor move: when a student asks “how do multiple experts coordinate without directly calling each other?”, quote: KSs are “procedurally independent” and “no KS references another KS directly” (same source).

### B. Orchestrator + shared RunState pipeline (HLER)
From HLER (https://arxiv.org/html/2603.07444v1):

1) Central **orchestrator** dispatches tasks to specialized agents.  
2) Orchestrator maintains shared **RunState** storing intermediate outputs as structured objects.  
3) Workflow is sequential stages:  
   **Data Audit → Data Profiling → Questioning → Data Collection → Analysis → Writing → Self-Critique → Review**  
4) Two loops:
   - **Question quality loop:** generate candidate questions → feasibility screen → **human selects** → possibly regenerate with constraints  
   - **Research revision loop:** reviewer requests → re-analysis + rewrite → re-review (typically converges **2–4** iterations)
5) HITL gates: human chooses research question; human decides publication.

### C. Event-sourced shared state with deterministic replay (ESAA)
From ESAA (https://arxiv.org/html/2602.23193v1):

1) Agent emits **structured intentions only** (validated JSON), e.g., `agent.result`, `issue.report`.  
2) Deterministic orchestrator:
   - validates against JSON Schema + boundary rules
   - appends to `activity.jsonl` (append-only, ordered)
   - applies effects via orchestrator-owned actions (e.g., `orchestrator.file.write`)
3) Projection step: build/update `roadmap.json` (materialized read model) and compute `projection_hash_sha256`.  
4) Verification: `esaa verify` replays the event log → reprojects → compares hash; emits `verify.ok` or `verify.fail`.  
5) Concurrency: agents can run in parallel, but event append is sequential to preserve total order and detect conflicts (e.g., overlapping file modifications) before applying.

### D. Multi-agent extraction architectures (sequential / parallel / hierarchical / reflexive)
From SEC benchmark (https://arxiv.org/pdf/2603.22651.pdf):

- **Sequential:** fixed chain; cumulative JSON state passed forward; long docs split into sections then merged.
- **Parallel fan-out + merge:** dispatcher routes sections to extractors; merge agent resolves conflicts via **confidence-weighted voting**.
- **Hierarchical supervisor-worker:** supervisor maintains task queue; if field confidence < **0.85**, reassign; max **2** re-extraction iterations; supports heterogeneous model routing.
- **Reflexive loop:** verifier checks format, cross-field consistency, and source grounding; max **3** correction iterations; else emit best-confidence with low-confidence flag.

---

## Teaching Approaches

### Intuitive (no math): “Team chat vs shared whiteboard vs flight recorder”
- **Message passing** = team chat: agents send each other notes.  
- **Shared state / blackboard** = shared whiteboard: everyone updates one place; a facilitator decides what to do next.  
- **Event sourcing (ESAA)** = flight recorder: every change is logged so you can replay exactly what happened and audit it.

### Technical (with math): “Latency overlap and throughput limits”
- Use Speculative Actions formula to reason about when speculation helps: if tool latency \(L\) is large and prediction probability \(p\) is non-trivial, overlapping calls reduces expected runtime.  
- Then connect to SPAgent’s serving result: speculation can *hurt* under load without scheduling (Speculative Actions can be slower than naive at >2 rps per SPAgent), so coordination must include resource-aware scheduling.

### Analogy-based: “Blackboard = operating room board + pager system”
- Blackboard levels/nodes = patient chart sections; KSs = specialists; events = pager alerts; control component = charge nurse deciding which specialist acts next based on urgency/priority.

---

## Common Misconceptions

1) **“If agents share state, they don’t need to message each other.”**  
   - **Why wrong:** Shared state answers “what is known,” but you still need a *control policy* for “who acts next” and “what triggers action.” Blackboard systems explicitly separate blackboard (data) from control (scheduling) and KS triggers/events (Stanford blackboard explainer).  
   - **Correct model:** Shared state + event/trigger mechanism + scheduler (control component) is what yields coordination.

2) **“Blackboard means every agent can freely write anything anywhere.”**  
   - **Why wrong:** In classic blackboard architecture, **only KSs may modify the blackboard**, and KSs are procedurally independent (no direct references) (Stanford blackboard explainer). ESAA goes further: agents have **no direct write permission**; orchestrator validates and applies effects (ESAA).  
   - **Correct model:** Treat writes as privileged operations governed by contracts/control, not a free-for-all.

3) **“Human-in-the-loop just means a human can read the output at the end.”**  
   - **Why wrong:** HLER uses explicit **decision gates** mid-pipeline (question selection) and at the end (publication decision), changing the trajectory and preventing wasted work (HLER). LangGraph frames HITL as inspecting/modifying state “at any point” (LangGraph docs).  
   - **Correct model:** HITL is a *designed control point* (gate/interrupt) with authority to redirect, approve, or stop.

4) **“More reflection/verification loops always improve production performance.”**  
   - **Why wrong:** SEC benchmark shows reflexive has best F1 at low scale but is most expensive/slow and degrades fastest at high throughput (queueing/timeouts truncate loops), falling behind hierarchical at scale (SEC benchmark scaling table).  
   - **Correct model:** Reflexive loops trade accuracy for cost/latency and can become brittle under load; iteration caps and architecture choice matter.

5) **“Speculation is always a free speedup if predictions are sometimes right.”**  
   - **Why wrong:** SPAgent reports that a baseline “Speculative Actions” approach can become **slower than naive** under load (>2 rps) due to inference overhead and scheduling effects (SPAgent).  
   - **Correct model:** Speculation needs scheduling/load-awareness and guardrails; otherwise overhead can dominate.

---

## Worked Examples

### Example 1: Minimal blackboard-style loop (event → triggered KS → write → new event)
Goal: show the *mechanics* (not a full framework).

```python
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Any, Optional

@dataclass
class Event:
    type: str
    payload: dict = field(default_factory=dict)

@dataclass
class Blackboard:
    data: Dict[str, Any] = field(default_factory=dict)

@dataclass
class KS:
    name: str
    trigger: Callable[[Event, Blackboard], bool]
    action: Callable[[Event, Blackboard], List[Event]]  # returns newly posted events

def control_loop(bb: Blackboard, agenda: List[Event], knowledge_sources: List[KS], max_steps: int = 20):
    steps = 0
    while agenda and steps < max_steps:
        event = agenda.pop(0)  # FIFO event selection (one of many possible schedulers)
        triggered = [ks for ks in knowledge_sources if ks.trigger(event, bb)]
        # Conflict resolution via scheduling: here, run all triggered in list order
        for ks in triggered:
            new_events = ks.action(event, bb)
            agenda.extend(new_events)
        steps += 1
    return bb

# --- Define KSs ---
def trig_on_start(ev, bb): return ev.type == "start"
def act_create_hypothesis(ev, bb):
    bb.data["hypothesis"] = "H1: revenue increased due to X"
    return [Event("hypothesis.created")]

def trig_on_hypothesis(ev, bb): return ev.type == "hypothesis.created"
def act_request_review(ev, bb):
    bb.data["needs_review"] = True
    return [Event("review.requested")]

bb = Blackboard()
agenda = [Event("start")]
kss = [
    KS("HypothesisKS", trig_on_start, act_create_hypothesis),
    KS("ReviewKS", trig_on_hypothesis, act_request_review),
]
final_bb = control_loop(bb, agenda, kss)
print(final_bb.data)
```

**Tutor notes (tie to sources):**
- This mirrors the Stanford cycle: select event → select triggered KS → execute → post new events (https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf).
- To discuss conflict resolution, swap FIFO for priority/utility scheduling (the source lists alternatives).

### Example 2: Conflict resolution by confidence-weighted merge (parallel fan-out + merge)
Inspired by SEC benchmark’s “merge agent resolves conflicts via confidence-weighted voting” (https://arxiv.org/pdf/2603.22651.pdf).

```python
from collections import defaultdict

# Each extractor returns candidate values with confidences
extractor_outputs = [
    {"TotalAssets": ("100", 0.60), "CEO": ("Alice", 0.90)},
    {"TotalAssets": ("110", 0.80), "CEO": ("Alice", 0.55)},
    {"TotalAssets": ("110", 0.70), "CEO": ("Bob",   0.65)},
]

def confidence_weighted_vote(outputs):
    votes = defaultdict(lambda: defaultdict(float))  # field -> value -> weight
    for out in outputs:
        for field, (value, conf) in out.items():
            votes[field][value] += conf
    merged = {}
    for field, value_weights in votes.items():
        merged[field] = max(value_weights.items(), key=lambda kv: kv[1])[0]
    return merged

print(confidence_weighted_vote(extractor_outputs))
# Example result: {'TotalAssets': '110', 'CEO': 'Alice'}
```

**Tutor prompts:**
- Ask what happens if two values tie; what additional rule would you add (e.g., prefer grounded source, or trigger supervisor re-extraction like hierarchical architecture with threshold 0.85)?

---

## Comparisons & Trade-offs

| Pattern | Coordination mechanism | Strengths (per sources) | Weaknesses / risks (per sources) | When to choose |
|---|---|---|---|---|
| Sequential pipeline | Fixed handoffs + cumulative state | Resilient at scale (SEC: smallest F1 drop at high throughput); simple | Lower peak accuracy than reflexive; less parallelism | High throughput, predictable workloads (SEC benchmark) |
| Parallel fan-out + merge | Parallel extraction + merge conflict resolution | Lower latency (SEC: 21.3s vs 38.7s sequential) | Needs merge/conflict logic; may reduce consistency | Document sectioning, independent subtasks (SEC benchmark) |
| Hierarchical supervisor-worker | Supervisor queue + confidence threshold + retries | Near-reflexive accuracy at lower cost (SEC: 0.929 F1 at $0.261); bounded retries | More latency than parallel; supervisor complexity | When you need quality control with bounded cost/iterations (SEC benchmark) |
| Reflexive self-correcting loop | Verifier checks + correction iterations | Best F1 at low scale (SEC: 0.943) | Highest cost/latency; degrades fastest at high throughput (SEC scaling) | When accuracy dominates and throughput is modest (SEC benchmark) |
| Blackboard system | Shared blackboard + event-driven KS scheduling | Opportunistic problem solving; modular specialists; control resolves conflicts via scheduling | Requires careful control design; scheduling complexity | Ill-structured tasks needing diverse expertise (Stanford blackboard papers) |
| Event-sourced orchestration (ESAA) | Append-only event log + deterministic orchestrator + replay | Auditable, replayable, conflict-detectable; agents can’t directly write effects | Token overhead (200–500 tokens/invocation); orchestrator complexity | High auditability/safety needs; long-running workflows (ESAA) |

---

## Prerequisite Connections

- **Tool-using agent loops (Reason→Act→Observe).** Many coordination patterns assume agents take actions and observe results iteratively; ReAct formalizes this interaction style (https://arxiv.org/abs/2210.03629).  
- **Basic concurrency concepts (parallelism, queues, scheduling).** Needed to understand why reflexive loops degrade under load and why SPAgent emphasizes scheduling (SPAgent; SEC scaling).  
- **State machines / workflow execution.** Helpful for understanding orchestrators, durable execution, and HITL interrupts (LangGraph docs: https://langchain-ai.github.io/langgraph/).  
- **Evaluation metrics (success rate, latency, cost).** Needed to interpret architecture trade-offs and scaling tables (agent eval metrics taxonomy: https://arxiv.org/html/2507.21504v1).

---

## Socratic Question Bank

1) **If two agents disagree on a field value, what are three different conflict-resolution mechanisms you could apply, and what assumptions does each require?**  
   - Good answer: confidence-weighted merge (SEC), supervisor re-extraction with threshold (SEC), verifier consistency rules with bounded iterations (SEC), or scheduling/agenda choice (blackboard).

2) **What’s the difference between “shared state” and “shared control”?**  
   - Good answer: shared state is the data store (RunState/blackboard); control is who decides next action (orchestrator/control component/speaker selection).

3) **Where would you place a human-in-the-loop gate in a pipeline, and what decision would it make? Why there?**  
   - Good answer: like HLER’s question selection and publication decision; rationale: high leverage points.

4) **Why might a reflexive architecture lose to a hierarchical one at high throughput even if it has higher F1 at low throughput?**  
   - Good answer: queueing/timeouts truncate correction loops; cost/latency explode; SEC scaling result.

5) **In a blackboard system, why is it important that KSs don’t directly call each other?**  
   - Good answer: procedural independence; coordination via blackboard + control; reduces coupling (Stanford blackboard explainer).

6) **Speculation: what must be true about side effects for “pre-launching” actions to be safe?**  
   - Good answer: idempotent/reversible/sandboxed; actor verifies before commit (Speculative Actions paper).

7) **If you had to debug a long-running multi-agent run, what artifact would you want: a chat transcript, a shared state snapshot, or an event log? What does each miss?**  
   - Good answer: event log enables deterministic replay/verification (ESAA); transcript may be ambiguous; snapshot lacks causality.

8) **How would you cap costs in a supervisor-worker system without destroying accuracy?**  
   - Good answer: confidence threshold + max iterations (SEC hierarchical: 0.85, max 2), caching/model routing ablations (SEC).

---

## Likely Student Questions

**Q: What are the three components of a blackboard architecture?**  
→ **A:** (1) **Blackboard** (global database/shared solution state), (2) **Knowledge Sources** (specialist modules that create/modify blackboard contents), and (3) **Control component** (scheduling/behavior in a serial environment) (https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf).

**Q: What is the basic blackboard control cycle?**  
→ **A:** Select an event → select KS(s) triggered by that event (in context) → execute KS instance → it modifies the blackboard and posts new events → repeat (https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf).

**Q: In AutoGen GroupChat, what are the key defaults for speaker selection?**  
→ **A:** `speaker_selection_method="auto"`, `max_retries_for_selecting_speaker=2`, `allow_repeat_speaker=True`, `admin_name="Admin"`, and `func_call_filter=True` (https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/).

**Q: What does `func_call_filter=True` do in AutoGen GroupChat?**  
→ **A:** If a message is a function call suggestion, the next speaker must be an agent whose `function_map` contains that function name (https://microsoft.github.io/autogen/0.2/docs/reference/agentchat/groupchat/).

**Q: What are the concrete accuracy–cost–latency trade-offs between sequential/parallel/hierarchical/reflexive orchestration?**  
→ **A:** On SEC extraction (Claude 3.5 Sonnet): Sequential **F1 0.903**, **$0.187**, **38.7s**; Parallel **0.914**, **$0.221**, **21.3s**; Hierarchical **0.929**, **$0.261**, **46.2s**; Reflexive **0.943**, **$0.430**, **74.1s** (https://arxiv.org/pdf/2603.22651.pdf).

**Q: Why does reflexive orchestration degrade at high throughput?**  
→ **A:** The benchmark reports reflexive degrades fastest (F1 **0.943→0.871** from **1K→100K docs/day**) due to queueing/timeouts truncating correction loops; sequential is more resilient (**0.903→0.886**) (https://arxiv.org/pdf/2603.22651.pdf).

**Q: What are HLER’s human-in-the-loop gates?**  
→ **A:** (1) **Research Question Selection** (PI chooses among candidates) and (2) **Publication Decision** (final quality gate) (https://arxiv.org/html/2603.07444v1).

**Q: How does ESAA make agent runs auditable and replayable?**  
→ **A:** It stores an append-only ordered event log (`activity.jsonl`), builds a projection (`roadmap.json`) with a SHA-256 hash over canonicalized state, and verifies by replaying the log and comparing hashes (`esaa verify`) (https://arxiv.org/html/2602.23193v1).

---

## Available Resources

### Videos
- [Multi-Agent Systems with LangGraph (YouTube)](https://www.youtube.com/watch?v=Mi5wOpAgixw) — Surface when: a student asks *why multi-agent systems help with context limits / parallelism / specialization* or wants a high-level tour of common multi-agent architectures.

### Articles & Tutorials
- [LangGraph (Docs)](https://langchain-ai.github.io/langgraph/) — Surface when: students ask about *durable execution* or *human-in-the-loop interrupts* in stateful agent workflows.
- [LangGraph: Multi-agent collaboration tutorial](https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi_agent_collaboration/) — Surface when: students want a concrete “how do I wire multiple agents together?” walkthrough.
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: students need grounding on *planning/memory/tools* as prerequisites to orchestration.
- [Microsoft AutoGen](https://microsoft.github.io/autogen/) — Surface when: students ask about *multi-agent conversation frameworks* and practical coordination patterns.
- [ReAct paper](https://arxiv.org/abs/2210.03629) — Surface when: students ask about the canonical *reason→act→observe* loop that many orchestrations wrap.

---

## Visual Aids

![LLM-powered autonomous agent system overview with planning, memory, and tools. (Weng, 2023)](/api/wiki-images/multi-agent-systems/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: the student is missing the “big picture” of how orchestration relates to planning/memory/tool use.

![ReAct reasoning trajectories vs. Act-only baseline across knowledge and decision tasks. (Yao et al., 2023)](/api/wiki-images/multi-agent-systems/images/lilianweng-posts-2023-06-23-agent_002.png)  
Show when: explaining why tool-using loops are sequential by default and why coordination/latency tricks (speculation, parallelism) matter.

---

## Key Sources

- [Blackboard System Architecture & Control Cycle](https://stacks.stanford.edu/file/druid:nh044zx3884/nh044zx3884.pdf) — Most precise description of blackboard components, KS triggering, and the event-driven control loop.
- [Blackboard Architecture (Components + Control Alternatives)](https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf) — Adds control design axes and how scheduling differs under search vs recognition.
- [Multi-agent orchestration benchmark (SEC filing extraction)](https://arxiv.org/pdf/2603.22651.pdf) — Concrete, quantitative trade-offs across sequential/parallel/hierarchical/reflexive architectures plus scaling behavior.
- [HLER human-in-the-loop multi-agent research pipeline](https://arxiv.org/html/2603.07444v1) — Real pipeline with shared RunState, revision loops, and explicit human decision gates with ops metrics.
- [ESAA — Event-Sourced Agent Orchestration](https://arxiv.org/html/2602.23193v1) — Auditable shared-state design via event sourcing, deterministic replay, and hash-verified projections.