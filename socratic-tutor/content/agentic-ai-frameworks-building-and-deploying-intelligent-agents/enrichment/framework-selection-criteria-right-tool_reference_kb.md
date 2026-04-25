## Core Definitions

**Framework selection (agent/orchestration context)**  
Framework selection is the process of choosing an orchestration/runtime stack for an agent by starting from *production requirements* (durability, human oversight, deployment constraints, scalability, observability/evals) and mapping them to concrete framework primitives (e.g., durable execution, interrupts, tracing, scalable serving). *Tutor note:* in this lesson, “framework” includes workflow orchestrators (Temporal, AWS Step Functions) and agent orchestration runtimes (LangGraph), plus observability/eval platforms (LangSmith, Phoenix).

**Durable execution**  
LangGraph describes durable execution as the ability to “persist through failures… automatically resuming from exactly where they left off” (LangGraph repo README: “Durable execution”). Temporal provides durable execution via persisted **Event History** and **replay**: events are “persisted to the database… durable… survive a crash,” and a worker can “replay” history to recreate workflow state (Temporal Event History walkthrough). Step Functions provides durability at the managed service level, but with explicit limits on execution time, history size, and payload sizes (AWS Step Functions quotas/limits).

**Checkpointing / persistence (LangGraph)**  
LangGraph’s `checkpointer` persistence “saves graph state as checkpoints… at every step of execution, organized into threads,” enabling “human-in-the-loop workflows, conversational memory, time travel debugging, and fault-tolerant execution” (LangGraph JS `CompiledStateGraph.checkpointer` reference). A **thread** is a unique `thread_id` used as the primary key for storing/retrieving checkpoints; without it, the checkpointer cannot save state or resume after an interrupt (same reference).

**Interrupts / human-in-the-loop (HITL)**  
LangChain’s human-in-the-loop middleware can “pause execution and wait for a decision” by issuing an **interrupt** when a tool call matches a policy; the “graph state is saved using LangGraph’s persistence layer… and resume later” (LangChain HITL docs). Built-in decision types are **approve**, **edit**, and **reject** (same source). Temporal supports HITL by modeling “do work → wait for human → continue” with **signals** (human decision injected), **queries** (read-only state for UI), and “durable waits” that consume no compute while waiting (Fridljand blog; Temporal AI cookbook HITL example).

**Deterministic replay (Temporal)**  
Temporal requires workflows to be deterministic for replay: a workflow is deterministic if “every execution… produces the same Commands in the same sequence given the same input.” During replay, the worker re-runs workflow code and compares produced commands to the event history; mismatches due to non-determinism prevent replay from continuing (Temporal Event History walkthrough).

**Observability & tracing (agent systems)**  
LangSmith positions tracing as capturing “execution paths… state transitions… runtime metrics” (LangGraph overview/README) and provides an API ingestion example for “runs” with hierarchical ordering (`dotted_order`) (LangSmith “Trace with API” doc). Observability is used both for debugging and for production monitoring.

**Offline vs online evaluation (LangSmith)**  
LangSmith defines **Offline Evaluation** as “test before you ship” on curated datasets to compare versions and catch regressions, and **Online Evaluation** as “monitor in production” by evaluating real user interactions in real time (LangSmith Evaluation docs). The workflow includes dataset creation, evaluator definition (human/code/LLM-as-judge/pairwise), experiments, and analysis (same source).

**Deployment constraints (practical meaning)**  
Deployment constraints are the non-functional requirements that restrict where/how the agent runs (e.g., self-hosting vs SaaS, data retention, quotas/limits, max execution duration, request/payload sizes, throttling). Example: Step Functions has hard limits like **1 MB** max request size and **256 KiB** max input/output per state/task/execution (AWS Step Functions limits).

**Abstraction tolerance (team fit)**  
Abstraction tolerance is how much “framework magic” a team is willing to accept (e.g., Temporal’s determinism constraints and replay model; LangGraph’s explicit state graph + checkpointer + thread model; Step Functions’ state machine definition constraints and service quotas). *Tutor note:* this is a selection criterion because it affects developer velocity, debugging, and operational risk.

---

## Key Formulas & Empirical Results

### AWS Step Functions — feasibility numbers (quotable constraints)
Source: AWS Step Functions Quotas & Limits.

- **Max execution time:** Standard **1 year**; Express **5 minutes**.  
  *Supports:* choosing Standard for long-running workflows / HITL waits; Express for short, high-throughput tasks.

- **Max input/output size (task/state/execution):** **256 KiB** UTF‑8 string (both Standard and Express).  
  *Supports:* deciding whether you must externalize state to S3/DB and pass references.

- **State machine definition size:** **1 MB (hard)**.  
  *Supports:* complexity ceiling for orchestration logic.

- **API max request size:** **1 MB per request (hard)** (includes headers + request data).  
  *Supports:* integration feasibility and payload design.

- **Execution history size:** Standard **25,000 events** (exceeding causes execution failure).  
  *Supports:* avoiding overly chatty step transitions; motivates compaction/external logging.

- **Execution history retention after close:** Standard **90 days** (can request reduction to **30 days**); Express **14 days**.  
  *Supports:* compliance/audit requirements.

- **HTTP Task duration:** **60 seconds (hard)**.  
  *Supports:* tool/API call design; long calls need async patterns.

- **Open executions (Standard):** **1,000,000 per account per Region**.  
  *Supports:* concurrency planning.

- **StartExecution throttling (token bucket; soft/increasable):**  
  - Standard: **1300/300** (us-east-1, us-west-2, eu-west-1); **800/150** (other regions)  
  - Express: **6000/6000** (all regions)  
  *Supports:* throughput sizing and region choice.

### Temporal — determinism requirement (mechanical claim)
Source: Temporal Event History walkthrough.

- **Determinism definition:** same input ⇒ same **Commands** in same sequence; replay compares generated commands to **Event History**; mismatch breaks replay.  
  *Supports:* selection trade-off: durability + replay vs constraints on workflow code.

### LangGraph — persistence mechanics (key defaults/requirements)
Source: LangGraph JS `checkpointer` reference; LangGraph issue #1568.

- **Checkpoint frequency:** “snapshot… saved at every step of execution” at **super-step** boundaries.  
- **Required config:** must provide `thread_id` in `configurable` config to persist/resume.  
- **Common failure mode:** without a checkpointer, “graph will restart after each run” (issue #1568 maintainer response).  
  *Supports:* selection criterion: statefulness requires explicit persistence wiring.

### LangSmith — evaluation modes (operational result)
Source: LangSmith Evaluation docs.

- **Offline eval:** dataset-based experiments pre-ship.  
- **Online eval:** production traces evaluated with sampling/filters to control cost.  
  *Supports:* selection criterion: built-in eval loop vs DIY.

---

## How It Works

### A production-first framework selection flow (tutor script)
1. **Write down the “must not fail” requirements** (not features):  
   - Do we need **durable execution** across crashes/deploys?  
   - Do we need **HITL pauses** that can last hours/days?  
   - What are the **payload/state sizes** and how often does state change?  
   - What are the **throughput/concurrency** targets?  
   - What are the **audit/retention** needs?  
   - Do we need **self-hosting** or can we use SaaS?

2. **Translate requirements into primitives** (map to capabilities):  
   - Durability ⇒ persisted state + resume (Temporal replay; LangGraph checkpointer; Step Functions managed executions).  
   - HITL ⇒ interrupts/signals + resumability (LangGraph interrupts + checkpointer; Temporal signals + wait_condition; Step Functions “wait for callback” patterns *not in provided sources—avoid details*).  
   - Observability ⇒ tracing + evals (LangSmith tracing/evals; Phoenix vs LangSmith trade-offs).  
   - Deployment constraints ⇒ quotas/limits + hosting model (Step Functions hard limits; Phoenix open-source; LangSmith self-hosting paid per Phoenix FAQ).

3. **Check “hard limits” early** (fast elimination):  
   - If you need >5 minutes single execution, Step Functions **Express** is out (limit: 5 minutes).  
   - If you need >256 KiB state per step, Step Functions requires externalization (256 KiB limit).  
   - If you need extremely long HITL waits, Step Functions Standard supports up to **1 year** execution time; Temporal supports durable waits; LangGraph supports interrupts with persistence (sources above).

4. **Assess team abstraction tolerance**:  
   - Temporal: accept deterministic workflow constraints + replay mental model (Temporal docs).  
   - LangGraph: accept explicit state graph + thread/checkpointer model (LangGraph refs).  
   - Step Functions: accept AWS service model + state machine definition constraints + event history cap (AWS limits).

5. **Decide build vs buy for observability/evals**:  
   - If you need integrated tracing/evals: LangSmith offers offline+online eval workflows (LangSmith eval docs).  
   - If you need open-source/self-host without paywall: Phoenix is open source and self-hosting is free; LangSmith is closed source and self-hosting is paid (Phoenix vs LangSmith FAQ).

### Mechanics: LangGraph persistence + HITL (what must be wired)
Source: LangGraph checkpointer reference; LangChain HITL docs; LangGraph issue #1568.

1. **Compile graph with a checkpointer** (otherwise each run is stateless).  
2. **Invoke/stream with `configurable.thread_id`** so checkpoints are stored under a thread.  
3. **When an interrupt triggers**, execution halts; state is persisted at the last super-step boundary.  
4. **Human reviews tool call(s)** and returns decision(s): approve/edit/reject.  
5. **Graph resumes** from the checkpoint using the same `thread_id`.

### Mechanics: Temporal HITL (signals + durable waits)
Source: Fridljand blog; Temporal AI cookbook HITL.

1. Workflow does work, sets status to awaiting approval.  
2. Workflow **waits** on a condition with a timeout (durable timer).  
3. External UI/service sends a **signal** with approve/reject.  
4. Workflow resumes immediately on signal; UI can **query** state while waiting.  
5. Because state is in event history, the workflow survives worker crashes and restarts (Temporal replay model).

---

## Teaching Approaches

### Intuitive (no math)
Pick the framework the way you’d pick a database: start with **operational guarantees** (durability, scaling, auditability), then check whether the tool’s **native primitives** match your workflow (pause/resume, human approvals, tracing). Only after that worry about developer ergonomics.

### Technical (with concrete constraints)
Treat selection as a constraint satisfaction problem:
- If your workflow needs long-running executions, Step Functions Express fails the constraint (**5 minutes** max).  
- If your workflow needs large per-step state, Step Functions fails beyond **256 KiB** unless you externalize.  
- If you need “resume exactly where you left off” with strong correctness, Temporal’s replay + event history provides that, but forces **determinism**.  
- If you need graph-structured agent orchestration with interrupts, LangGraph provides checkpoints per super-step, but you must supply `thread_id` and a checkpointer.

### Analogy-based
- **Step Functions** is like a managed conveyor belt with strict package size limits and a maximum belt length (payload/history/time caps).  
- **Temporal** is like a flight recorder + autopilot: everything is logged (event history), and after a crash it replays the tape to reconstruct state—so the “pilot script” must be deterministic.  
- **LangGraph** is like a state machine you build yourself, but with a built-in “save game” system (checkpoints) that only works if you name the save slot (`thread_id`).

---

## Common Misconceptions

1. **“If I annotate `add_messages`, LangGraph will remember messages automatically across turns.”**  
   - **Why wrong:** Without a **checkpointer**, the graph restarts each run; state reducers don’t persist across separate invocations. This shows up in practice: messages appear replaced rather than appended.  
   - **Correct model:** Reducers define *how to merge state within a run*; persistence across runs requires compiling with a checkpointer and using a `thread_id` (LangGraph issue #1568; checkpointer reference).

2. **“Human-in-the-loop just means showing the model’s plan to a human.”**  
   - **Why wrong:** Effective HITL requires the system to **pause safely** and **resume** after human input; that needs persisted state and an interrupt/signal mechanism.  
   - **Correct model:** HITL is an execution-control primitive: LangGraph uses **interrupts** + persistence; Temporal uses **signals** + durable waits + queries (LangChain HITL docs; Fridljand; Temporal AI cookbook).

3. **“Durable execution is just retries.”**  
   - **Why wrong:** Retries don’t reconstruct in-memory state or guarantee exactly-once progression through a multi-step workflow. Temporal durability is based on **event history + replay**; LangGraph durability is based on **checkpoints** at super-step boundaries.  
   - **Correct model:** Durable execution means the workflow can resume from a persisted state snapshot/log after failures (Temporal Event History; LangGraph checkpointer reference).

4. **“Step Functions can orchestrate any agent because it’s ‘serverless’.”**  
   - **Why wrong:** Step Functions has hard limits: **256 KiB** per step input/output, **25,000 events** history cap, **5 minutes** max for Express executions, **60s** HTTP task cap, etc.  
   - **Correct model:** Step Functions is feasible when your workflow fits within these quotas or you externalize state and design around limits (AWS limits card).

5. **“Observability is optional; we can add it later.”**  
   - **Why wrong:** Agent systems are stochastic and multi-step; without traces you can’t reliably debug or evaluate regressions. LangSmith explicitly frames evals as an iterative loop: production traces → datasets → offline experiments → redeploy (LangSmith Evaluation docs).  
   - **Correct model:** Treat tracing/evals as selection criteria, not an afterthought—especially if you need online monitoring.

---

## Worked Examples

### Example 1 — Fixing “LangGraph forgot my messages” (persistence + thread_id)
Grounded in: LangGraph issue #1568; LangGraph checkpointer reference.

**Symptom:** each user turn starts a fresh state; messages don’t append.

**Minimal Python sketch (pattern):**
```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    # return next assistant message (omitted)
    return {"messages": [{"role": "assistant", "content": "..." }]}

builder = StateGraph(State)
builder.add_node("chatbot", chatbot)
builder.add_edge(START, "chatbot")
builder.add_edge("chatbot", END)

# 1) compile with a checkpointer
graph = builder.compile(checkpointer=MemorySaver())

# 2) provide a thread_id on each call
thread_config = {"configurable": {"thread_id": "1"}}

# 3) now state persists across turns
graph.invoke({"messages": [("user", "hi")]}, thread_config)
graph.invoke({"messages": [("user", "and then?")]}, thread_config)
```

**Tutor moves (what to emphasize mid-conversation):**
- Ask: “Are you compiling with a checkpointer?”  
- Ask: “Are you passing `configurable.thread_id` every time?”  
- Quote: “When invoking a graph with a checkpointer, you must specify a `thread_id`…” (LangGraph checkpointer ref).

### Example 2 — Temporal HITL approval (signal + wait_condition)
Grounded in: Fridljand blog; Temporal AI cookbook HITL.

**Core workflow shape (conceptual code from source):**
```python
@workflow.signal
async def approve(self, reviewer_id: str) -> None:
    if self._status != Status.AWAITING_APPROVAL or self._decision is not None:
        return
    self._decision = "approved"
    self._approved_by = reviewer_id

@workflow.run
async def run(self, timeout_days: int) -> dict:
    self._status = Status.AWAITING_APPROVAL
    try:
        await workflow.wait_condition(
            lambda: self._decision is not None,
            timeout=timedelta(days=timeout_days),
        )
    except TimeoutError:
        self._status = Status.REJECTED
        return {"status": "timeout"}
    return {"status": "approved"}
```

**Tutor moves:**
- Highlight “resource efficient waiting… consumes no compute resources” (Temporal AI cookbook).  
- Connect to selection: if you need multi-day approvals, pick a system with durable waits/signals.

---

## Comparisons & Trade-offs

| Requirement / Criterion | LangGraph (w/ checkpointer) | Temporal | AWS Step Functions |
|---|---|---|---|
| Long-running workflows | Designed for “long-running, stateful agents” (LangGraph overview/README) | Workflows can wait durably; replay restores state (Temporal docs/blog) | Standard supports **1 year** execution; Express **5 min** (AWS limits) |
| HITL pause/resume | Interrupts + persistence; requires `thread_id` + checkpointer (LangChain HITL; LangGraph checkpointer ref) | Signals + queries + durable waits (Fridljand; Temporal AI cookbook) | Possible but bounded by service limits; must fit payload/history/time caps (AWS limits) |
| Durability mechanism | Checkpoints at super-step boundaries (LangGraph checkpointer ref) | Event history persisted; deterministic replay (Temporal Event History) | Managed service execution state; hard caps on history/events (AWS limits) |
| Key constraint | Must wire persistence correctly (`thread_id`) or state resets (issue #1568) | Workflow code must be deterministic for replay (Temporal Event History) | Hard limits: **256 KiB** I/O, **25k** events, **60s** HTTP task, etc. (AWS limits) |
| Observability/evals ecosystem | Integrates with LangSmith for tracing/debugging (LangGraph overview) | (Not covered in provided sources) | (Not covered in provided sources) |
| Evals (offline/online) | Via LangSmith (offline + online) (LangSmith eval docs) | (Not covered) | (Not covered) |

**When to choose which (source-grounded heuristics):**
- Choose **Step Functions Standard** when you need managed orchestration with known quotas and your workflow fits within **256 KiB** per-step payload and **25,000** history events, and may run up to **1 year** (AWS limits).  
- Choose **Temporal** when you need robust long waits + external approvals via **signals**, and you can accept **deterministic replay** constraints (Temporal docs; Fridljand; Temporal AI cookbook).  
- Choose **LangGraph** when you want explicit agent orchestration with **interrupts** and checkpoint-based persistence, and you’re prepared to manage `thread_id`/checkpointers and leverage LangSmith for tracing/evals (LangGraph overview; checkpointer ref; LangChain HITL; issue #1568).

---

## Prerequisite Connections

- **Statefulness vs stateless execution:** needed to understand why `thread_id` + checkpointer matters (LangGraph checkpointer ref; issue #1568).  
- **Event logs vs snapshots:** needed to compare Temporal event history replay vs LangGraph checkpoints (Temporal Event History; LangGraph checkpointer ref).  
- **Human-in-the-loop control points:** needed to reason about interrupts/signals and safe pause/resume (LangChain HITL; Temporal AI cookbook).  
- **Operational limits/quotas:** needed to eliminate infeasible orchestrators early (AWS Step Functions limits).

---

## Socratic Question Bank

1. **“Where does the ‘truth’ of workflow state live in your design—memory, DB rows, an event log, or checkpoints?”**  
   *Good answer:* identifies a durable source (Temporal event history; LangGraph checkpoints; Step Functions managed execution state) and implications.

2. **“If the worker process crashes mid-run, what exactly lets you resume—and from what boundary?”**  
   *Good answer:* Temporal replays event history; LangGraph resumes from last super-step checkpoint; Step Functions resumes managed execution.

3. **“What’s the longest time your system must be able to wait for a human, and what should it cost while waiting?”**  
   *Good answer:* recognizes durable waits (Temporal “consumes no compute”; LangGraph interrupts with persistence) and Step Functions Standard 1-year cap.

4. **“What’s your largest per-step state payload, and can you keep it under 256 KiB?”**  
   *Good answer:* uses Step Functions 256 KiB limit; proposes externalizing state if needed.

5. **“How will you debug a bad agent decision two weeks after it happened?”**  
   *Good answer:* mentions tracing + retention; LangSmith traces; Step Functions retention 90/14 days; need logs/audit trail.

6. **“What’s your team’s tolerance for constraints like ‘workflow code must be deterministic’?”**  
   *Good answer:* explains Temporal replay determinism and trade-off.

7. **“Do you need offline regression tests and online monitoring for quality?”**  
   *Good answer:* distinguishes LangSmith offline vs online evaluation and how it feeds a feedback loop.

8. **“Which limits are hard vs soft in your chosen platform?”**  
   *Good answer:* Step Functions hard limits (1 MB request, 256 KiB I/O, 60s HTTP task) vs throttles that are soft/increasable.

---

## Likely Student Questions

**Q: “Why did my LangGraph messages not append even though I used `add_messages`?”**  
→ **A:** Without a checkpointer, the graph restarts each run; you must compile with a checkpointer and pass `configurable.thread_id` so checkpoints persist and state can be merged across turns (LangGraph issue #1568; LangGraph checkpointer reference).

**Q: “What exactly is a `thread_id` in LangGraph persistence?”**  
→ **A:** A thread is a unique identifier used as the primary key for storing and retrieving checkpoints; when invoking a graph with a checkpointer, you **must** specify `thread_id` in the `configurable` config or it can’t save/resume state (LangGraph checkpointer reference).

**Q: “How long can AWS Step Functions run?”**  
→ **A:** Standard workflows can run up to **1 year**; Express workflows up to **5 minutes** (AWS Step Functions limits).

**Q: “What’s the max payload size in Step Functions?”**  
→ **A:** Max input/output size for a task/state/execution is **256 KiB** (UTF‑8 string) for both Standard and Express; max API request size is **1 MB** per request (AWS Step Functions limits).

**Q: “What happens if a Step Functions execution history gets too big?”**  
→ **A:** Standard has a max execution history size of **25,000 events**; if exceeded, the execution fails (AWS Step Functions limits).

**Q: “Why does Temporal require deterministic workflows?”**  
→ **A:** Temporal restores workflow state by replaying the persisted event history; during replay, the worker re-runs workflow code and compares generated commands to the history. If non-determinism changes the command sequence, replay can’t continue (Temporal Event History walkthrough).

**Q: “How does Temporal do human approval without polling?”**  
→ **A:** The workflow waits on a condition (durable wait) and external systems send the decision via **signals**; UIs can read state via **queries** (Fridljand blog; Temporal AI cookbook HITL).

**Q: “What’s the difference between offline and online evaluation in LangSmith?”**  
→ **A:** Offline evaluation runs experiments on curated datasets before shipping; online evaluation scores real production interactions in real time with sampling/filters to manage cost (LangSmith Evaluation docs).

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student needs grounding on what an “agent” is and why orchestration/memory/tool use exist at all (context for why frameworks differ).
- [AI Agents: Safety, Security, and Trust](https://youtube.com/watch?v=kJLiOGle3Lw) — Surface when: student asks how oversight/guardrails relate to framework choice (HITL as risk control).
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — Surface when: student asks how LangGraph structures multi-agent orchestration and why state graphs help.

### Articles & Tutorials
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — Surface when: student asks about “memory/session” abstractions vs orchestration frameworks; use to contrast lightweight session memory with durable workflow state.
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student needs the canonical decomposition of agents (planning/memory/tools) before mapping to framework primitives.
- [LangGraph agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks for orchestration patterns (supervisor, multi-agent) and how they map to graphs.
- [Yao et al., 2022 — ReAct](https://arxiv.org/abs/2210.03629) — Surface when: student asks about agent loop patterns (reason+act) and how orchestration frameworks execute them.

---

## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
**Show when:** student is mixing up “agent design components” (planning/memory/tools) with “framework primitives” (durability/interrupts/tracing). Use this to anchor the *requirements → primitives* mapping.

---

## Key Sources

- [AWS Step Functions — Quotas & Limits](https://docs.aws.amazon.com/step-functions/latest/dg/limits.html) — authoritative hard numbers that often decide feasibility (timeouts, payloads, history caps, throttles).
- [Temporal Docs — Event History walkthrough (Python)](https://docs.temporal.io/encyclopedia/event-history/event-history-python) — explains durability via event history + replay and why determinism is required.
- [LangGraph JS reference — `CompiledStateGraph.checkpointer`](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer) — precise mechanics of checkpoints, threads, super-steps; required for HITL/time travel/fault tolerance.
- [LangSmith Evaluation](https://docs.langchain.com/langsmith/evaluation) — concrete offline vs online evaluation definitions and workflow for production quality loops.
- [LangChain Human-in-the-loop docs](https://docs.langchain.com/oss/python/langchain/human-in-the-loop) — how interrupts + persistence implement approval/edit/reject control in agent tool calls.