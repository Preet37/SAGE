## Core Definitions

**Production agent deployment** — “Agents are systems that independently accomplish tasks on your behalf,” where reliability comes from the *system* (model + tools + instructions + orchestration + monitoring/evals), not the model alone. In OpenAI’s practical guide, an agent is characterized by (1) the LLM controlling workflow execution (deciding what to do, recognizing completion, correcting, halting/handing off), and (2) tool access to gather context and take actions within guardrails. (Source: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Tool calling / tool use** — Tool use is when the model returns a *structured tool call* matching a developer-provided schema; the application (client tools) or provider (server tools) executes it and returns a tool result back to the model. Anthropic describes the loop as: model decides to call a tool based on the request + tool description, returns tool_use blocks, your app executes and sends tool_result (client tools), or Anthropic executes (server tools like web_search). (Source: https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

**Structured outputs (schema conformance)** — A production pattern where tool inputs/outputs are constrained to a declared schema so downstream code can validate and safely execute. Anthropic explicitly supports “strict tool use” (`strict: true`) to ensure tool calls match the schema exactly. (Source: https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

**Traces / runs (observability)** — “Traces are a series of steps that your application takes to go from input to output,” and each step is represented by a “run.” LangSmith uses traces/runs to visualize execution steps for debugging, evaluation, and monitoring. (Source: https://docs.langchain.com/oss/python/langgraph/observability)

**Offline vs online evaluation (agent reliability & evals)** — LangSmith distinguishes: **Offline evaluation** (“test before you ship”) on curated datasets to compare versions and catch regressions, and **Online evaluation** (“monitor in production”) on real user interactions in real time to detect issues and measure quality on live traffic. (Source: https://docs.langchain.com/langsmith/evaluation)

**Durable execution (workflow engines)** — Temporal persists an **Event History**: a durable log of events in a workflow execution. On failure, Temporal replays history to recreate state and continue, which requires workflow code to be deterministic: same input ⇒ same commands in the same sequence. (Sources: https://docs.temporal.io/encyclopedia/event-history/event-history-python and https://docs.temporal.io/encyclopedia/event-history/event-history-go)

**Deterministic workflow constraint** — A Temporal workflow is deterministic if every execution of its workflow definition produces the same commands in the same sequence given the same input; replay compares commands produced during replay to the event history, and mismatches break replay. (Sources: Temporal event history pages above)

**Human-in-the-loop (approval gating)** — A production oversight pattern where the agent proposes an action, the workflow pauses for human approval if risky, and proceeds/cancels based on a signal; Temporal highlights resource-efficient waiting (no compute while waiting), durable timers, and an audit trail of decisions. (Source: https://docs.temporal.io/ai-cookbook/human-in-the-loop-python)

**Session memory (conversation history store)** — In the OpenAI Agents SDK (Python), a `Session` stores conversation history for a specific session so agents can maintain context without manual memory management; it supports `get_items`, `add_items`, and `pop_item`. (Source: https://openai.github.io/openai-agents-python/ref/memory/session/)

**Input validation & guardrails (agent security)** — AWS prescriptive guidance frames user inputs as the primary attack vector for agentic systems (prompt injection/manipulation) and recommends defense-in-depth: automated prompt validation test suites (e.g., promptfoo), guardrails (e.g., Bedrock Guardrails prompt attack filters), prompt logging with metrics, and multi-layer sanitization. (Source: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html)

---

## Key Formulas & Empirical Results

**LangSmith evaluation workflow (operational “numbers” and structure)**  
LangSmith’s evaluation workflow explicitly separates offline vs online and describes a loop: create dataset → define evaluators → run experiment → analyze results; online: deploy → configure online evaluators with filters/sampling → monitor → feed failures back into datasets. (Source: https://docs.langchain.com/langsmith/evaluation)

**ReAct agent benchmarking: pass rate definition + experimental constants**  
- **PassRate**: \(\text{PassRate}=\frac{\#\text{passed runs}}{90}\) where 90 runs = 30 tasks × 3 stochastic repeats.  
- Pass requires (1) correct tool-calling trajectory (“nothing more, nothing less”) and (2) final email judged by an LLM rubric.  
- Task/tool constants: Calendar Scheduling expected trajectory avg **1.4** tool calls; Customer Support avg **2.7** tool calls and **7 tools** (+ send_email).  
- Key results (1-domain controls): Calendar Scheduling: **o1 71%**, **o3-mini 68%**; Customer Support: **claude-3.5-sonnet 83%**, **o3-mini 83%**, **o1 77%**.  
- Scaling domains: performance drops as domains/tools/context increase; longer trajectories degrade faster. (Source: https://blog.langchain.com/react-agent-benchmarking/)

**Latency-aware orchestration (LAMaS): critical-path latency + cost equations + defaults**  
- **Latency under parallel layers**: \(L=\sum_{l\in \mathcal{L}} \max_{o\in \mathcal{O}_l} t(o)\) (critical path across layers).  
- **Cost**: \(C=\sum_{l\in \mathcal{L}}\sum_{o\in \mathcal{O}_l} c(o)\).  
- **Global reward**: \(R = S - \lambda_c C - \lambda_l \hat{L}\).  
- Defaults/hyperparams reported: LLM **gpt-4o-mini-0718**, temperature **1**, layers \(L=4\), \(\lambda_c=0.1\), sampling times \(N=5\), threshold \(\tau=0.8\), \(\lambda_l=0.5\), tool scaling \(\alpha=50\) (1s tool time = 50 “virtual tokens”).  
- Reported CP reductions vs baseline with parallelism: e.g., GSM8K CP length **−38.0%**, HumanEval **−42.4%**, MATH **−46.1%** (with small score changes). (Source: https://arxiv.org/abs/2601.10560)

**Speculative actions (predict–verify): expected runtime ratio + empirical speedups**  
- Expected runtime ratio: \(\frac{\mathbb{E}[T_{\text{spec}}]}{\mathbb{E}[T_{\text{seq}}]}=\frac{1}{2-p}\left(1+\frac{l}{L}\right)\) where \(L\)=mean latency of actual API call, \(l\)=mean latency of speculative model, \(p\)=probability speculation matches next call.  
- Empirical: next-action prediction accuracy up to **55%**; up to **20% end-to-end lossless speedup** (abstract). (Source: https://arxiv.org/html/2510.04371v1)

---

## How It Works

### A. Tool-calling agent loop (provider-agnostic mechanics)
1. **Developer defines tools**: name + description + input schema (and optionally strict schema conformance, e.g., Anthropic `strict: true`). (Anthropic tool use doc)
2. **Model inference with tools enabled**: request includes tool definitions; model chooses whether to call a tool. (Anthropic tool use; OpenAI tools guide)
3. **Model emits structured tool call**:
   - Anthropic: response includes `stop_reason: "tool_use"` and one or more `tool_use` blocks. (Anthropic tool use)
4. **Executor runs tool**:
   - **Client tools**: your application executes the function and returns a `tool_result`.
   - **Server tools**: provider executes (e.g., web_search) and returns results directly. (Anthropic tool use)
5. **Model continues** with tool results in context; repeats until it returns a normal response without tool calls or hits an explicit “final output tool” condition (OpenAI guide notes Agents SDK loop semantics). (OpenAI practical guide PDF)

### B. Observability with LangSmith (LangGraph)
1. **Enable tracing** by environment variables:
   ```bash
   export LANGSMITH_TRACING=true
   export LANGSMITH_API_KEY=<your-api-key>
   ```
   Default project name is `default`. (LangGraph observability doc)
2. **Selective tracing** with `tracing_context(enabled=True)` to trace only specific invocations. (LangGraph observability doc)
3. **Project routing**:
   - Static: `LANGSMITH_PROJECT=my-agent-project`
   - Dynamic: `with ls.tracing_context(project_name="...", enabled=True): ...` (LangGraph observability doc)
4. **Interpretation**: traces show step-by-step runs (LLM calls, tool calls, subgraphs) to debug failures and feed evaluation datasets. (LangGraph observability + LangSmith evaluation docs)

### C. Reliability via durable workflows (Temporal)
1. Workflow code issues **commands** to Temporal service.
2. Service converts commands into **events** appended to **Event History** (durable, persisted).
3. On worker crash/failure, worker replays event history to reconstruct state and continue.
4. **Determinism requirement**: replay runs workflow code again and compares produced commands to history; non-determinism (e.g., random number) can cause mismatch and break replay. (Temporal event history docs)

### D. Human approval gating (Temporal “human-in-the-loop” cookbook)
1. LLM analyzes request and proposes an action.
2. If action is risky, workflow **pauses** and waits for approval via **Temporal Signal**.
3. If approved, execute action; if rejected or timed out, cancel/complete accordingly.
4. Benefits called out: resource-efficient waiting, durable timers, audit trail. (Temporal HITL cookbook)

### E. Fine-grained tool streaming (Anthropic) — handling partial JSON
When `eager_input_streaming: true` and streaming enabled:
1. `content_block_start` for a `tool_use` block includes placeholder `input: {}`.
2. Tool input arrives as multiple `input_json_delta` events with `partial_json` fragments.
3. Accumulate fragments into a string; on `content_block_stop`, parse JSON:
   ```python
   tool_inputs[event.index] = ""
   tool_inputs[event.index] += event.delta.partial_json
   parsed = json.loads(tool_inputs[event.index])
   ```
4. Edge case: stream may end mid-JSON (e.g., `max_tokens`), so code must handle invalid/incomplete JSON. (Source: https://docs.anthropic.com/ja/docs/agents-and-tools/tool-use/fine-grained-tool-streaming)

---

## Teaching Approaches

### Intuitive (no math): “Agents are apps with a probabilistic controller”
- The LLM is the *decision-maker*, but production reliability comes from everything around it: retrieval, tool schemas, retries, approvals, and monitoring.
- If you can’t *observe* what happened (traces) or *replay* what happened (durable workflows), you can’t debug or guarantee outcomes.

### Technical (with math): “Latency and reliability are system properties”
- Parallel orchestration changes latency from “sum of steps” to “critical path” (LAMaS \(L=\sum_l \max_o t(o)\)).
- Speculation changes expected runtime by overlapping likely next calls (Speculative Actions runtime ratio formula).
- Evals are formalized as offline experiments and online monitors; you close the loop by adding failing traces back into datasets (LangSmith evaluation workflow).

### Analogy-based: “Airplane autopilot”
- The model is the autopilot computer; tools are actuators/sensors; workflows are flight checklists; human-in-the-loop is the pilot’s approval for risky maneuvers; observability is the flight data recorder; evals are simulator tests + in-flight monitoring.

---

## Common Misconceptions

1. **“If the model is strong enough, I don’t need tools/evals/guardrails.”**  
   - Why wrong: sources emphasize agents as *systems*; LangSmith exists to debug/evaluate/monitor; AWS notes user input is primary attack vector; OpenAI guide recommends eval-first model selection and guardrails.  
   - Correct model: model capability helps, but production reliability comes from tool schemas, tracing, evaluation, and layered controls.

2. **“Tool calling is just the model printing JSON; it’s inherently reliable.”**  
   - Why wrong: Anthropic fine-grained streaming explicitly warns you may receive invalid/incomplete JSON; strict schema conformance is an *option* (`strict: true`), not automatic.  
   - Correct model: treat tool calls as untrusted input—validate schema, handle partial JSON, implement retries/repair.

3. **“Observability is optional; I can debug from logs.”**  
   - Why wrong: LangSmith defines traces as step-by-step runs; it’s designed to visualize execution steps and support evaluation/monitoring. Plain logs often miss hierarchy/causality across tool calls and subgraphs.  
   - Correct model: tracing is structured, queryable execution data that powers debugging + eval pipelines.

4. **“Workflows can call random/time APIs freely; replay will still work.”**  
   - Why wrong: Temporal replay requires determinism; mismatched commands during replay break durable execution.  
   - Correct model: keep workflow logic deterministic; push non-deterministic work into activities or controlled interfaces.

5. **“Human-in-the-loop means the human watches everything, so it’s safe.”**  
   - Why wrong: Temporal HITL pattern is *selective* (pause only for risky actions) and emphasizes durable waiting + audit trail; oversight effectiveness depends on structuring decision points, not maximal involvement. (Temporal HITL; oversight paper in sources also stresses structure/legibility, though details are broader.)  
   - Correct model: gate high-risk actions with explicit approval points and timeouts; log decisions.

---

## Worked Examples

### 1) Enable LangSmith tracing for a LangGraph agent (Python)
**Goal:** show a tutor-ready snippet for “how do I turn on tracing and isolate a test run?”

```bash
export LANGSMITH_TRACING=true
export LANGSMITH_API_KEY=<your-api-key>
export LANGSMITH_PROJECT=my-agent-project
```

Selective tracing for one call:
```python
import langsmith as ls

# traced
with ls.tracing_context(enabled=True, project_name="email-agent-test"):
    out = agent.invoke({
        "messages": [{"role": "user", "content": "Send a welcome email"}]
    })

# not traced (if global env var not set)
agent.invoke({
    "messages": [{"role": "user", "content": "Send another email"}]
})
```
What to point out mid-tutoring:
- “Trace selectively” is a production pattern for privacy/cost control. (Source: LangGraph observability doc)

### 2) Temporal human approval gate (conceptual execution path)
**Student prompt:** “Delete all test data from the production database”  
**Workflow behavior (from cookbook):**
1. LLM proposes action.
2. Marked risky ⇒ workflow pauses.
3. External approval arrives via Temporal Signal.
4. Approved ⇒ execute action; rejected/timeout ⇒ cancel/complete.  
Tutor emphasis:
- Waiting consumes no compute; timers survive disruptions; audit trail is complete. (Source: Temporal HITL cookbook)

### 3) Anthropic fine-grained tool streaming: accumulate partial JSON safely
Use when a student asks “why did my tool JSON parse fail during streaming?”

```python
import json
import anthropic

client = anthropic.Anthropic()
tool_inputs = {}  # index -> accumulated JSON string

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[{
        "name": "get_weather",
        "description": "Get current weather for a city",
        "eager_input_streaming": True,
        "input_schema": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"],
        },
    }],
    messages=[{"role": "user", "content": "Weather in Paris?"}],
) as stream:
    for event in stream:
        if event.type == "content_block_start" and event.content_block.type == "tool_use":
            tool_inputs[event.index] = ""
        elif event.type == "content_block_delta" and event.delta.type == "input_json_delta":
            tool_inputs[event.index] += event.delta.partial_json
        elif event.type == "content_block_stop" and event.index in tool_inputs:
            parsed = json.loads(tool_inputs[event.index])
            print(parsed)
```

Tutor notes:
- Placeholder `input: {}` is expected.
- Must handle incomplete JSON if stream ends early (`max_tokens`). (Source: fine-grained tool streaming doc)

---

## Comparisons & Trade-offs

| Decision | Option A | Option B | Choose A when | Choose B when | Sources |
|---|---|---|---|---|---|
| Evaluation timing | Offline eval (“test before you ship”) | Online eval (“monitor in production”) | You need regression testing, benchmarking, version comparison | You need live quality/safety monitoring on real traffic | https://docs.langchain.com/langsmith/evaluation |
| Tool execution location | Client tools | Server tools | You need custom integrations, private systems, full control | You want provider-managed execution (e.g., web_search) | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |
| Orchestration reliability | Ad-hoc agent loop | Durable workflow engine (Temporal) | Low-stakes, short tasks; simpler infra | Long-running, failure-prone, compliance/audit needs; need replay | Temporal event history docs |
| Latency optimization | Sequential tool calls | Parallel DAG / critical-path optimization | Simpler dependencies; low latency pressure | Tool-heavy workflows where wall-clock matters | https://arxiv.org/abs/2601.10560 |
| Latency optimization (advanced) | No speculation | Speculative actions (predict–verify) | You can’t safely pre-launch calls | Calls are reversible/idempotent; you can validate before commit | https://arxiv.org/html/2510.04371v1 |

---

## Prerequisite Connections

- **Basic tool calling semantics** → needed to understand structured outputs, strict schema conformance, and tool-result loops. (Anthropic tool use; OpenAI tools guide)
- **Tracing/observability concepts** → needed to reason about debugging and evaluation pipelines (trace → dataset → experiment). (LangGraph observability; LangSmith evaluation)
- **Determinism vs non-determinism** → needed to understand why durable replay works and what breaks it. (Temporal event history)
- **Security mindset (prompt injection as input attack)** → needed to justify guardrails and validation layers. (AWS agentic AI security guidance)

---

## Socratic Question Bank

1. **If your agent makes a wrong external API call, what artifacts would you want to inspect to debug it?**  
   *Good answer:* traces/runs showing tool calls + inputs/outputs; ideally linked to eval cases (LangSmith tracing/evals).

2. **What’s the difference between “the model produced invalid JSON” and “your system accepted invalid JSON”?**  
   *Good answer:* model outputs are untrusted; system must validate/repair; streaming can produce partial JSON (Anthropic streaming doc).

3. **Why does Temporal require workflow determinism, and what breaks if you violate it?**  
   *Good answer:* replay compares commands to event history; mismatch stops replay (Temporal event history).

4. **When would you add a human approval step, and what should happen on timeout?**  
   *Good answer:* risky actions; pause via signal; timeout completes safely (Temporal HITL cookbook).

5. **How do offline and online evals complement each other in a release cycle?**  
   *Good answer:* offline catches regressions pre-ship; online monitors live drift/issues; failures feed back into datasets (LangSmith evaluation).

6. **If you parallelize agent sub-tasks, what becomes the limiting factor for latency?**  
   *Good answer:* critical path (max per layer), not sum of all tasks (LAMaS formula).

7. **What conditions must hold for speculative actions to be “lossless”?**  
   *Good answer:* validate equivalence before commit; wrong-branch calls must be reversible/no side effects; have repair/rollback (Speculative Actions paper).

8. **What’s one concrete way to reduce prompt-injection risk besides “better prompting”?**  
   *Good answer:* automated prompt validation suites; guardrails; logging/metrics; layered sanitization (AWS guidance).

---

## Likely Student Questions

**Q: How do I enable LangSmith tracing for a LangGraph app?**  
→ **A:** Set `LANGSMITH_TRACING=true` and `LANGSMITH_API_KEY=<key>`; optionally set `LANGSMITH_PROJECT` for project name. (Source: https://docs.langchain.com/oss/python/langgraph/observability)

**Q: Can I trace only one invocation (not everything)?**  
→ **A:** Yes—use LangSmith’s `tracing_context(enabled=True)` context manager around the call you want traced. (Source: LangGraph observability doc)

**Q: What’s the difference between offline and online evaluation in LangSmith?**  
→ **A:** Offline = run on curated datasets during development to benchmark/compare/catch regressions; Online = evaluate real user interactions in production in real time for monitoring and alerting. (Source: https://docs.langchain.com/langsmith/evaluation)

**Q: Why does Temporal say workflows must be deterministic?**  
→ **A:** Because on failure, Temporal replays the persisted event history; the worker reruns workflow code to produce commands and compares them to the history—non-determinism causes mismatches and replay can’t continue. (Sources: Temporal event history Python/Go docs)

**Q: In Anthropic tool streaming, why do I sometimes get invalid JSON for tool inputs?**  
→ **A:** With fine-grained tool streaming (`eager_input_streaming`), tool input arrives as `partial_json` fragments without buffering/JSON validation; streams can end mid-JSON (e.g., `max_tokens`). You must accumulate fragments and handle incomplete JSON. (Source: https://docs.anthropic.com/ja/docs/agents-and-tools/tool-use/fine-grained-tool-streaming)

**Q: What does “strict tool use” do in Claude tool calling?**  
→ **A:** Adding `strict: true` to tool definitions ensures Claude’s tool calls always match your schema exactly. (Source: https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

**Q: How is “pass rate” defined in the LangChain ReAct benchmarking post?**  
→ **A:** PassRate = passed runs / 90, where 90 runs = 30 tasks × 3 repeats; passing requires correct tool trajectory and a rubric-judged final email. (Source: https://blog.langchain.com/react-agent-benchmarking/)

**Q: If I parallelize agent work, how do I compute latency?**  
→ **A:** LAMaS defines latency as critical path across layers: \(L=\sum_l \max_{o\in \mathcal{O}_l} t(o)\). (Source: https://arxiv.org/abs/2601.10560)

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student needs grounding on what an LLM is before discussing agents as systems.
- [AI Agents: Safety, Security, and Trust](https://youtube.com/watch?v=kJLiOGle3Lw) — Surface when: student asks about prompt injection, guardrails, or oversight.
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: student is confused about tool calling mechanics and schemas.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student needs the canonical planning/memory/tool-use/action architecture framing.
- [LangGraph agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks about orchestration patterns (graphs, supervisors, state).
- [OpenAI Agents SDK (Python)](https://openai.github.io/openai-agents-python/) — Surface when: student asks how agent loops, tools, and memory are represented in code.
- [OpenAI API Tools guide](https://platform.openai.com/docs/guides/tools) — Surface when: student asks about tool_choice, parallel tool calls, tool search, or MCP.
- [LangSmith Evaluation](https://docs.langchain.com/langsmith/evaluation) — Surface when: student asks “how do I set up evals before/after shipping?”
- [LangSmith Observability (LangGraph)](https://docs.langchain.com/oss/python/langgraph/observability) — Surface when: student asks “how do I debug my agent in production?”

---

## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: student is mixing up “LLM” vs “agent system” and needs the component diagram (planning/memory/tools).

![PoT offloads computation to Python code, unlike CoT's natural language steps. (Chen et al. 2022)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-03-15-prompt-engineering_003.png)  
Show when: student asks why coding agents often use code execution tools instead of pure natural-language reasoning.

---

## Key Sources

- [A practical guide to building agents (OpenAI PDF)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Defines agents as systems; emphasizes tools, guardrails, eval-first model selection, and orchestration tradeoffs.
- [LangSmith Evaluation](https://docs.langchain.com/langsmith/evaluation) — Clear offline vs online evaluation distinction and workflow for reliability loops.
- [LangGraph LangSmith Observability](https://docs.langchain.com/oss/python/langgraph/observability) — Concrete tracing enablement + selective tracing patterns.
- [Temporal Event History walkthrough](https://docs.temporal.io/encyclopedia/event-history/event-history-python) — Durable execution via event history + determinism requirement.
- [Anthropic Tool use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Canonical tool-use loop; strict schema conformance; client vs server tools.