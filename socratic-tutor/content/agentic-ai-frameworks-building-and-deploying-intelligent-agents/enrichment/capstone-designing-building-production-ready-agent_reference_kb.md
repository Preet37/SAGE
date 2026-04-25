## Core Definitions

**End-to-end agent design (production-ready agent)**  
An agent is “anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators,” and its behavior is described by an *agent function* mapping percept sequences to actions (Russell & Norvig, *Intelligent Agents* chapter excerpt) https://cse-robotics.engr.tamu.edu/dshell/cs625/ch2.pdf. In production, “end-to-end” design means specifying (and instrumenting) the full loop from user input → state updates → tool calls/side effects → final output, including reliability, safety, and monitoring requirements (LangSmith Observability/Evaluation docs; agent evaluation taxonomy paper).

**LangGraph orchestration (graph-based agent execution)**  
LangGraph orchestrates agent/workflow logic as a graph whose execution proceeds in **super-steps** (“a single ‘tick’ of the graph where all nodes scheduled for that step execute”) and can persist state as checkpoints at each super-step boundary when compiled with a checkpointer (LangGraph JS checkpointer reference) https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer.

**Retrieval-Augmented Generation (RAG)**  
RAG combines a pre-trained generative model (parametric memory) with an explicit retriever over a non-parametric store (e.g., a dense vector index) to condition generation on retrieved passages; this improves factuality and enables updating knowledge without retraining (Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks”) https://arxiv.org/abs/2005.11401. Practitioner framing: RAG addresses knowledge cutoffs, lack of domain depth, and lack of private/proprietary data access in foundation models (Pinecone RAG explainer) https://www.pinecone.io/learn/retrieval-augmented-generation/.

**Structured tool calling / tool use (function calling)**  
Tool use lets a model decide when to call developer-defined or provider tools based on tool descriptions, returning a **structured tool call** that is executed by the application (client tools) or by the provider (server tools) (Anthropic tool use docs) https://docs.anthropic.com/en/docs/build-with-claude/tool-use. OpenAI similarly defines “tools” as configurations passed in the `tools` parameter enabling function calling, web/file search, remote MCP servers, etc., with optional control via `tool_choice` (OpenAI Tools guide) https://platform.openai.com/docs/guides/tools.

**Short-term vs long-term memory (agent memory, operational definition)**  
In production agent frameworks, “memory” often splits into (a) **in-session / in-thread conversational history** used to maintain context across turns, and (b) **durable/persistent state** stored outside the model context window to survive restarts and support long-running workflows. Example: the OpenAI Agents SDK defines a **Session** as storing conversation history for a specific session with methods like `get_items`, `add_items`, and `pop_item` (OpenAI Agents SDK memory session reference) https://openai.github.io/openai-agents-python/ref/memory/session/. LangGraph persistence stores graph state as checkpoints organized into threads (LangGraph checkpointer reference).

**Human-in-the-loop (HITL) checkpointing / approval gates**  
HITL in orchestration means the workflow can pause after proposing an action, wait for a human decision, then resume deterministically from persisted state. Temporal describes this as “do work → wait for human → continue” using **signals** to inject the decision and **durable waits** that consume no compute while waiting (Temporal HITL blog; Temporal AI cookbook) https://danielfridljand.de/post/temporal-human-in-the-loop and https://docs.temporal.io/ai-cookbook/human-in-the-loop-python. LangGraph similarly requires persistence/checkpointing to “inspect, interrupt, and approve graph steps” and resume execution (LangGraph checkpointer reference).

**Observability and tracing (LangSmith)**  
A trace is “a series of steps that your application takes to go from input to output,” where each step is represented by a run; LangSmith visualizes these runs for debugging, evaluation, and monitoring (LangSmith Observability docs) https://docs.langchain.com/oss/python/langgraph/observability.

**Agent evaluation (offline/online; metrics taxonomy)**  
Agent evaluation can be organized by **objectives** (behavior, capabilities, reliability, safety/alignment) and **process** (interaction mode, evaluation data, metric computation, tooling, contexts) (LLM Agent Evaluation Metrics & Benchmark Construction) https://arxiv.org/html/2507.21504v1. LangSmith distinguishes **Offline evaluation** (“test before you ship” on curated datasets) vs **Online evaluation** (“monitor in production” on real user interactions) (LangSmith Evaluation docs) https://docs.langchain.com/langsmith/evaluation.

---

## Key Formulas & Empirical Results

### Agent behavior: success and consistency
- **Success Rate (SR)** / Task Success Rate: binary reward `{0,1}` for goal achievement; aggregated over tasks (Agent eval metrics taxonomy) https://arxiv.org/html/2507.21504v1.
- **pass@k**: succeeds at least once in *k* attempts (multi-trial success).  
- **pass^** (stricter): succeeds in **all** *k* attempts; used for mission-critical consistency (same source).

### Latency and cost metrics
- **TTFT (Time To First Token)**: delay until first streamed token (agent eval metrics taxonomy) https://arxiv.org/html/2507.21504v1.
- **End-to-End Request Latency**: time until complete response (more relevant for async agents) (same source).
- **Cost proxy**: estimated from `#input tokens + #output tokens` (same source).  
  Tool use can add tokens via tool schemas and tool call/result blocks (Anthropic tool use pricing notes) https://docs.anthropic.com/en/docs/build-with-claude/tool-use.

### Tool-use capability metrics (selection + parameters)
- **Invocation Accuracy** (call tool vs not), **Tool Selection Accuracy**, **Retrieval Accuracy** (rank-based). Ranking metrics: **MRR**, **NDCG** (agent eval metrics taxonomy) https://arxiv.org/html/2507.21504v1.
- Parameter evaluation: **parameter name F1**; **execution-based evaluation** runs tool calls to catch semantic errors beyond AST validity (same source).

### Planning / trajectory metrics
- **Node F1** (tool set), **Edge F1** / **Normalized Edit Distance** (tool sequence/graph structure), stepwise “next tool” alignment, **Step Success Rate** (agent eval metrics taxonomy) https://arxiv.org/html/2507.21504v1.

### Reliability under production-like stress (benchmark framing)
- ReliabilityBench argues single-run success overestimates production reliability; evaluates **consistency**, **robustness to perturbations**, and **fault tolerance under infrastructure failures** (ReliabilityBench) https://arxiv.org/html/2601.06112v1.

### LangGraph persistence mechanics (implementation facts)
- When compiled with a checkpointer, LangGraph “saves a snapshot of the graph state … at every step of execution, organized into threads,” enabling HITL, time travel debugging, and fault tolerance (LangGraph JS checkpointer reference) https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer.
- Checkpoints are created at **super-step boundaries** (same source).

---

## How It Works

### A. Production agent loop in LangGraph (conceptual sequence)
1. **Receive input** (user message/event) and initialize/merge into graph state.
2. **Route** to the next node(s) based on edges/conditions (graph orchestration).
3. **LLM reasoning step** (often a node) produces either:
   - a final response, or
   - a **tool call** (structured), or
   - a control decision (e.g., “needs retrieval”, “needs approval”).
4. **Tool execution node** runs the tool call in application code (client tool) or via provider (server tool), then writes a tool result back into state.
5. **RAG node(s)** (optional) retrieve documents and add grounded context into state before generation.
6. **Approval gate node** (optional) interrupts/persists state and waits for human input; then resumes.
7. **Finalize** response and emit output; persist trace + evaluation signals.

### B. LangGraph persistence + threads + checkpoints (mechanics)
**What persistence gives you (LangGraph):**
- **Human-in-the-loop**: inspect/interrupt/approve steps; must resume from saved state.
- **Time travel**: replay prior executions; fork from checkpoints.
- **Fault tolerance**: restart from last successful step if nodes fail.  
Source: LangGraph checkpointer reference https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer.

**Key objects:**
- **Thread**: unique `thread_id` that is the primary key for storing/retrieving checkpoints. You must pass it in config under `configurable` when invoking a graph with a checkpointer (same source).
- **Checkpoint**: snapshot of thread state at a point in time (`StateSnapshot`).
- **Super-step**: boundary at which checkpoints are created; you can only resume from a checkpoint (super-step boundary).

**Practical implication (common bug pattern):**  
If you don’t compile with a checkpointer (or don’t pass `thread_id`), each run starts fresh; message reducers like `add_messages` won’t accumulate across separate invocations because there is no persisted thread state (LangGraph issue #1568 discussion) https://github.com/langchain-ai/langgraph/issues/1568.

### C. HITL waiting pattern (Temporal as reference architecture)
Temporal’s HITL pattern (Temporal blog + cookbook):
1. Workflow does work and sets status `AWAITING_APPROVAL`.
2. Workflow **waits** on a condition (durable wait) with optional timeout.
3. External UI/service sends a **signal** (approve/reject) into the workflow.
4. Workflow resumes and continues approved path, or cancels/rejects on timeout.  
Sources: https://danielfridljand.de/post/temporal-human-in-the-loop and https://docs.temporal.io/ai-cookbook/human-in-the-loop-python.

### D. LangSmith observability (enable + selective tracing)
- Enable tracing via environment variables:  
  ```bash
  export LANGSMITH_TRACING=true
  export LANGSMITH_API_KEY=<your-api-key>
  ```
  Default project: `default` (LangSmith Observability docs) https://docs.langchain.com/oss/python/langgraph/observability.
- Trace selectively with `tracing_context(enabled=True)` and optionally set `project_name` dynamically (same source).

### E. Evaluation workflow (LangSmith)
**Offline evaluation (before shipping):**
1. Create dataset (manual, historical traces, synthetic).
2. Define evaluators (human, code rules, LLM-as-judge, pairwise).
3. Run experiment (repetitions, concurrency, caching).
4. Analyze/compare experiments (benchmarking, regression tests, backtesting).  
Source: LangSmith Evaluation docs https://docs.langchain.com/langsmith/evaluation.

**Online evaluation (in production):**
1. Deploy; each interaction creates a run.
2. Configure online evaluators (safety, format validation, reference-free judge) with filters/sampling.
3. Monitor in real time; alerting/anomaly detection.
4. Feed failing traces back into offline datasets.  
Source: same.

---

## Teaching Approaches

### Intuitive (no math): “Assembly line with checkpoints”
- The agent is an assembly line: each station (node) does one job (retrieve, decide, call tool, summarize).
- A checkpointer is the barcode scanner that records the package after every station so you can pause for approval, recover from failures, or replay what happened.
- Observability is the CCTV footage (trace) showing each station’s work.

### Technical (with metrics): “Optimize for SR + pass@k + tool accuracy”
- Production readiness isn’t just SR; you also care about **pass@k** (stochastic consistency), latency (TTFT, end-to-end), and tool correctness (invocation accuracy, parameter F1, execution-based eval).
- Offline evals measure regressions; online evals detect drift and real-user failures (LangSmith evaluation model; agent eval taxonomy).

### Analogy-based: “Git for agent state + CI for agent quality”
- Checkpoints/threads ≈ git commits/branches: you can time-travel, fork, and resume.
- Offline evals ≈ CI test suite; online evals ≈ production monitoring/alerts.
- Tool calling schemas ≈ typed function signatures; strict schemas reduce runtime surprises (Anthropic “strict tool use” concept).

---

## Common Misconceptions

1. **“If I use `add_messages`, my chat history will automatically persist across turns.”**  
   - **Why wrong:** Reducers define *how to merge state within an execution*, but persistence across separate invocations requires a checkpointer + `thread_id`. Without it, the graph restarts each run.  
   - **Correct model:** Use a checkpointer (e.g., `MemorySaver`) and pass `configurable.thread_id` so state is stored in a thread and reloaded next turn (LangGraph checkpointer ref; LangGraph issue #1568).

2. **“RAG guarantees no hallucinations.”**  
   - **Why wrong:** RAG provides retrieved context, but the generator can still ignore/misuse it; RAG is a mitigation for knowledge gaps and grounding, not a proof system (Lewis et al. RAG; Pinecone RAG limitations framing).  
   - **Correct model:** Treat RAG as adding *non-parametric memory* and provenance potential; still evaluate groundedness and correctness with evals.

3. **“Tool calling is just prompting; schema doesn’t matter much.”**  
   - **Why wrong:** Tool calls are structured outputs that your system executes; schema mismatch becomes runtime failure or unsafe side effects. Anthropic explicitly supports **strict tool use** to guarantee schema conformance (Anthropic tool use docs).  
   - **Correct model:** Tool schemas are contracts; validate parameters and prefer execution-based evaluation for semantic correctness (agent eval taxonomy).

4. **“Offline evaluation is enough; once it passes tests, production is fine.”**  
   - **Why wrong:** LangSmith distinguishes offline vs online; production introduces new distributions, user behaviors, and failures. ReliabilityBench emphasizes robustness and fault tolerance under stress conditions beyond single-run success.  
   - **Correct model:** Use offline evals for regression + online evals for monitoring and feedback loops (LangSmith evaluation; ReliabilityBench).

5. **“Human-in-the-loop means polling a database until someone approves.”**  
   - **Why wrong:** Temporal highlights polling wastes resources and is fragile; durable waits + signals allow long waits without compute and survive restarts (Temporal HITL blog/cookbook).  
   - **Correct model:** Model approval as an interruptible wait with an external signal/callback and a timeout policy.

---

## Worked Examples

### 1) LangGraph: persistent conversation memory across turns (fixing the “messages replaced” issue)

**Problem symptom:** each user turn prints state with only the latest message; history not appended.

**Cause:** graph is re-invoked without persistence; state doesn’t survive between runs.

**Fix (from LangGraph issue #1568):** compile with a checkpointer and pass `thread_id`.

```python
from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver  # persistence

from langchain_openai import ChatOpenAI

class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    model = ChatOpenAI(temperature=0.1, model_name="gpt-3.5-turbo")
    return {"messages": [model.invoke(state["messages"])]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)

# Key change: add checkpointer
graph = graph_builder.compile(checkpointer=MemorySaver())

thread_config = {"configurable": {"thread_id": "1"}}

while True:
    user_input = input("User: ")
    if user_input.lower() in ["quit", "exit", "q"]:
        break

    for event in graph.stream({"messages": ("user", user_input)}, thread_config):
        for value in event.values():
            print("Assistant:", value["messages"][-1].content)
```

**What to point out while tutoring:**
- `thread_id` is the primary key for storing/retrieving checkpoints (LangGraph checkpointer ref).
- Without it, the checkpointer can’t resume after interrupts or accumulate state across runs.

### 2) LangSmith: enable tracing + isolate a test run into a project

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_PROJECT=my-agent-project
```

Or dynamically (Python):

```python
import langsmith as ls

with ls.tracing_context(project_name="email-agent-test", enabled=True):
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Send a welcome email"}]
    })
```

Source: LangSmith Observability docs https://docs.langchain.com/oss/python/langgraph/observability.

### 3) HITL approval: durable wait + signal (Temporal pattern sketch)

Temporal’s cookbook describes: analyze request → if risky, pause for approval via signal → execute if approved, cancel if rejected/timed out (Temporal AI cookbook) https://docs.temporal.io/ai-cookbook/human-in-the-loop-python.

Use this as a reference pattern when students ask “how do I wait days for approval without burning compute?”

---

## Comparisons & Trade-offs

| Design choice | Option A | Option B | When to choose |
|---|---|---|---|
| Evaluation timing | **Offline eval** (datasets, experiments) | **Online eval** (production traces) | Offline to catch regressions pre-ship; online to detect drift/issues on live traffic (LangSmith Evaluation). |
| Reliability metric | **pass@k** (≥1 success in k) | **pass^** (success in all k) | pass@k for “can it succeed sometimes”; pass^ for mission-critical consistency (agent eval taxonomy). |
| Tool correctness scoring | **Schema/AST validity** | **Execution-based evaluation** | Execution-based catches semantic errors even if schema matches (agent eval taxonomy). |
| HITL waiting | Polling loop | Durable wait + signal | Durable wait avoids resource burn and survives restarts (Temporal HITL blog/cookbook). |
| Observability platform | LangSmith (closed source) | Phoenix (open source) | Phoenix if you need open-source + free self-hosting; LangSmith if you want tight LangChain ecosystem integration (Phoenix vs LangSmith FAQ). |

Sources: LangSmith Evaluation/Observability docs; agent eval taxonomy paper; Temporal HITL resources; Phoenix vs LangSmith comparison https://arize.com/docs/phoenix/resources/frequently-asked-questions/open-source-langsmith-alternative-arize-phoenix-vs.-langsmith.

---

## Prerequisite Connections

- **Basic agent model (percepts → actions)**: needed to reason about what “state,” “tools,” and “environment” mean in an agent loop (Russell & Norvig excerpt).
- **Tool calling / function signatures**: needed to understand structured tool schemas and why parameter validation matters (Anthropic/OpenAI tools docs).
- **Retrieval + embeddings conceptually**: needed to understand why RAG helps with knowledge cutoffs and private data grounding (Lewis et al.; Pinecone RAG).
- **Testing/monitoring mindset**: needed to understand offline vs online evals and why production reliability differs from demo success (LangSmith eval docs; ReliabilityBench framing).

---

## Socratic Question Bank

1. **If your agent succeeds 90% of the time on a dataset, what could still make it unsafe or unusable in production?**  
   *Good answer:* mentions consistency (multi-trial), robustness to perturbations, tool failures, latency/cost, safety checks; ties to offline vs online eval.

2. **Where exactly does “memory” live in your design: in the prompt, in a database, or in checkpoints—and what breaks if the process restarts?**  
   *Good answer:* distinguishes context window vs persisted state; mentions thread_id/checkpointer or session storage.

3. **What’s the difference between “tool selection accuracy” and “parameter name F1,” and why might both matter?**  
   *Good answer:* selection is choosing correct tool; parameter F1 checks correct argument fields; both needed for correct execution.

4. **When would you prefer pass^ over pass@k? What product requirement does that reflect?**  
   *Good answer:* mission-critical consistency; must succeed every time, not just occasionally.

5. **If you add RAG, what new failure modes do you introduce?**  
   *Good answer:* retrieval errors, irrelevant context, ranking issues; need retrieval accuracy metrics (MRR/NDCG) and groundedness checks.

6. **What should trigger a human approval checkpoint in your graph?**  
   *Good answer:* risky/irreversible actions; policy thresholds; tool categories; includes timeout/escalation.

7. **What would you look for in a trace to debug a wrong final answer?**  
   *Good answer:* inspect runs per node, tool calls/results, retrieved docs, branching decisions; use LangSmith trace visualization.

8. **How would you turn a production failure into a regression test?**  
   *Good answer:* add failing trace/example to dataset; create evaluator; run offline experiment; redeploy; monitor online.

---

## Likely Student Questions

**Q: Why didn’t my LangGraph messages accumulate across turns even though I used `add_messages`?**  
→ **A:** Without a checkpointer, the graph restarts each run; to persist and merge messages across turns you must compile with a checkpointer and pass `configurable.thread_id`, because checkpoints are stored per thread and loaded via `thread_id` (LangGraph checkpointer ref; LangGraph issue #1568) https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer and https://github.com/langchain-ai/langgraph/issues/1568.

**Q: What exactly is a “super-step” in LangGraph and why does it matter?**  
→ **A:** A super-step is a single tick where all scheduled nodes execute (possibly in parallel); LangGraph creates a checkpoint at each super-step boundary, and you can only resume/time-travel from checkpoints (LangGraph checkpointer ref) https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer.

**Q: How do I enable LangSmith tracing for my agent?**  
→ **A:** Set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY=<key>`; traces log to project `default` unless you set `LANGSMITH_PROJECT` or use `tracing_context(project_name=..., enabled=True)` (LangSmith Observability docs) https://docs.langchain.com/oss/python/langgraph/observability.

**Q: What’s the difference between offline and online evaluation in LangSmith?**  
→ **A:** Offline runs on curated datasets during development to compare versions and catch regressions; online evaluates real user interactions in production in real time to detect issues and measure quality on live traffic (LangSmith Evaluation docs) https://docs.langchain.com/langsmith/evaluation.

**Q: What metrics should I use to evaluate a tool-using agent?**  
→ **A:** For tool use: invocation accuracy, tool selection accuracy, retrieval accuracy (MRR/NDCG), parameter name F1, and execution-based evaluation to catch semantic errors (agent eval taxonomy) https://arxiv.org/html/2507.21504v1.

**Q: What does pass@k mean, and when do I need pass^?**  
→ **A:** pass@k = succeeds at least once in k attempts; pass^ = succeeds in all k attempts and is used for mission-critical consistency (agent eval taxonomy) https://arxiv.org/html/2507.21504v1.

**Q: How can a workflow wait days for human approval without burning resources?**  
→ **A:** Use durable waits and signals (Temporal): the workflow pauses on a wait condition and resumes when an external signal delivers the decision; no polling inside the workflow, and timeouts can bound waiting (Temporal HITL blog/cookbook) https://danielfridljand.de/post/temporal-human-in-the-loop and https://docs.temporal.io/ai-cookbook/human-in-the-loop-python.

**Q: Does RAG just mean “search then paste into the prompt”?**  
→ **A:** In the RAG formulation, generation is conditioned on retrieved passages from a non-parametric store accessed by a retriever, combining parametric and non-parametric memory; it’s a general recipe for knowledge-intensive tasks (Lewis et al.) https://arxiv.org/abs/2005.11401.

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — **Surface when:** student needs the “LLM as cognitive core” framing for agents (tools/memory/action loop).
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — **Surface when:** student is confused about structured tool calls vs normal prompting.
- [Multi-Agent Systems with LangGraph](https://youtube.com/watch?v=Mi5wOpAgixw) — **Surface when:** student asks how to structure complex graphs/supervisors/subgraphs.

### Articles & Tutorials
- [LLM Powered Autonomous Agents (Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/) — **Surface when:** student wants a unified mental model of planning/memory/tool use.
- [LangGraph agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — **Surface when:** student asks “what orchestration patterns exist beyond a single loop?”
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — **Surface when:** student asks how session memory is represented in an SDK.
- [RAG paper (Lewis et al.)](https://arxiv.org/abs/2005.11401) — **Surface when:** student asks for the canonical definition of RAG and parametric vs non-parametric memory.

---

## Visual Aids

![API-Bank pseudo-code showing LLM decision logic for tool selection and execution. (Li et al. 2023)](/api/wiki-images/agent-memory/images/lilianweng-posts-2023-06-23-agent_011.png)  
**Show when:** student asks “what does the tool-use decision loop look like step-by-step?” or “how do we evaluate tool selection vs execution?”

![Internet-augmented LLMs retrieve, chunk, rank, then prompt with evidence. (Source: Internet-augmented LMs paper)](/api/wiki-images/evaluation-benchmarks/images/eugeneyan-writing-llm-patterns_011.webp)  
**Show when:** student asks for a concrete RAG pipeline picture (retrieve → chunk → rank → prompt).

---

## Key Sources

- [LLM Agent Evaluation Metrics & Benchmark Construction](https://arxiv.org/html/2507.21504v1) — taxonomy + concrete metrics (SR, pass@k, TTFT, tool-use metrics).
- [LangGraph checkpointer reference](https://reference.langchain.com/javascript/langchain-langgraph/index/CompiledStateGraph/checkpointer) — authoritative mechanics of threads/checkpoints/super-steps and why persistence is required for HITL/time travel/fault tolerance.
- [LangSmith Evaluation](https://docs.langchain.com/langsmith/evaluation) — offline vs online evaluation workflows and operational loop.
- [LangSmith Observability (LangGraph)](https://docs.langchain.com/oss/python/langgraph/observability) — tracing enablement, selective tracing, project metadata.
- [Retrieval-Augmented Generation (Lewis et al.)](https://arxiv.org/abs/2005.11401) — canonical RAG definition: parametric + non-parametric memory via retrieval.