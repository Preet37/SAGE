## Core Definitions

**LLM-powered agent (AI agent)**: “Agents are systems that independently accomplish tasks on your behalf.” Key characteristics include: (1) the **LLM controls workflow execution** (decides what to do next, recognizes completion, can correct itself; on failure can halt and transfer control to the user), and (2) **tool access** to gather context and take actions with **dynamic tool selection** inside **guardrails**. (OpenAI, *A practical guide to building agents*, “What is an agent?” https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Agent architecture (core components)**: A minimal production framing is **Model + Tools + Instructions**. The model is the decision-maker, tools provide external capabilities (data/actions/orchestration), and instructions constrain behavior and define success criteria. (OpenAI, *A practical guide to building agents*, “Agent design foundations” https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Reasoning loop / agent loop**: An agent is an LLM embedded in a **loop** that repeatedly (a) observes state/context, (b) decides/plans next step, (c) acts (often via tool calls), and (d) incorporates observations/results back into state until an exit condition is met. In the OpenAI Agents SDK description, `Runner.run()` loops until either a **final-output tool** is invoked or the model returns a response **without tool calls**. (OpenAI, *A practical guide to building agents*, “Single-agent systems” https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Perception and action (agent-environment interface)**: “An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators.” The agent’s behavior can be described as an **agent function** mapping percept sequences to actions. (Russell & Norvig, *Intelligent Agents*, Ch. 2 excerpt https://cse-robotics.engr.tamu.edu/dshell/cs625/ch2.pdf)

**Planning and task decomposition**: Planning is the agent’s process of turning a goal into an actionable sequence of steps, often decomposing into subgoals. A key architecture distinction is whether planning is **incremental** (e.g., ReAct-style step-by-step) or maintains a **continuously updated global plan** that is revised using execution history and available tools. (GoalAct paper summary https://arxiv.org/html/2504.16563v2)

**Tool use / function calling**: Tool use is when the model emits a **structured tool call** (name + arguments) that the application (client tools) or provider (server tools) executes, then returns results to the model as tool outputs. Claude’s docs describe the loop: model outputs tool_use → app executes → app sends tool_result; server tools run on provider infra. (Anthropic tool use docs https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

**Tool taxonomy (data vs action vs orchestration tools)**: Tools can be categorized as **data tools** (retrieve context), **action tools** (make changes), and **orchestration tools** (agents as tools). Standardize, document, and test tools for reuse/versioning. (OpenAI, *A practical guide to building agents*, “Defining tools” https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Short-term vs long-term memory (in agent systems)**: In practice, “memory” splits into (a) **session/conversation history** used as immediate context and (b) longer-lived stores (e.g., databases/vector stores) used for retrieval across time. In the OpenAI Agents SDK, a **Session** “stores conversation history for a specific session, allowing agents to maintain context without requiring explicit manual memory management.” (OpenAI Agents SDK Memory reference https://openai.github.io/openai-agents-python/ref/memory/ and Session reference https://openai.github.io/openai-agents-python/ref/memory/session/)

**Autonomous decision-making (what makes it an agent vs a single LLM call)**: The defining difference is that the system gives the model **control over the workflow**—it can decide which tools/steps to take next, when to stop, and when to escalate/hand control back—rather than executing a fixed, developer-authored sequence. (OpenAI, *A practical guide to building agents*, “What is an agent?” https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

---

## Key Formulas & Empirical Results

### ReAct loop formalization (thought → action conditioned on observation/history)
From ReflAct vs ReAct framing: context \(c_t=(h_t,o_t)\) where \(h_t=\{u,\tau_1,a_1,o_1,\dots,\tau_t,a_t\}\).  
Thought: \(\tau_t\sim \pi^{thought}_\theta(\cdot\mid c_t)\).  
Action: \(a_t\sim \pi^{act}_\theta(\cdot\mid c_t\oplus \tau_t)\).  
Supports the claim that “reasoning” tokens can strongly shape subsequent action selection in tool loops. (ReflAct paper card https://arxiv.org/pdf/2505.15182v1.pdf)

**Empirical (entropy reduction)**: Average action-distribution entropy over 134 ALFWorld tasks (Llama-3.1-8B-Instruct):  
\(\bar H_{NoThinking}=1.23\) vs \(\bar H_{ReAct}=0.30\).  
Supports: adding explicit “thought” can make action selection more decisive/peaked. (ReflAct card, Table 1 https://arxiv.org/pdf/2505.15182v1.pdf)

### ReflAct improvements over ReAct (success rates)
Success Rate (SR) improvements reported: **ALFWorld +36.4%**, **ScienceWorld +8.5%**, **Jericho +38.1%**. Example: GPT-4o ALFWorld SR ReAct 85.1 → ReflAct 93.3.  
Supports: redesigning the loop to reflect on **state relative to goal** can improve reliability. (ReflAct card https://arxiv.org/pdf/2505.15182v1.pdf)

### GoalAct global plan definitions + ablation
- Global plan \(P=\{p_i\}_{i=1}^{n}\), final step \(p_n\) is **Finish**.  
- Plan update: \(P_t = \pi(u, T, H_t)\), where \(u\)=user query, \(T\)=tools, \(H_t\)=history.  
- History: \(H_t=\{(a_i,o_i)\}_{i=1}^{t-1}\).  
**Ablation**: removing global plan drops ALL success from **0.8710 → 0.7896** (−8.14%) for GLM-4-Plus.  
Supports: continuously updated global planning helps avoid local branches. (GoalAct card https://arxiv.org/html/2504.16563v2)

### WebArena benchmark numbers (web agents are still hard)
Best GPT-4 agent overall **14.41%** end-to-end success vs **human 78.24%** on **812** tasks.  
Supports: long-horizon tool/UI agents remain unreliable in realistic environments. (WebArena card https://arxiv.org/html/2307.13854v4)

### LangChain ReAct benchmarking (tool overload / “lost in the middle”)
- PassRate \(=\#\text{passed runs}/90\) (30 tasks × 3 repeats).  
- Adding domains/tools degrades performance; example: Calendar Scheduling **gpt-4o drops to 2% at 7 domains**.  
Supports: more tools/instructions can overload a single agent; motivates orchestration and tool curation. (LangChain benchmarking card https://blog.langchain.com/react-agent-benchmarking/)

### Function-calling eval pitfalls + decoding sensitivity
- BFCL accuracy can vary by **~10%** depending on decoding; **Temperature 0.0** usually best for programmatic tool calling.  
- Relevance Detection can be gamed (never call tools → high score on that subset).  
Supports: tool-calling reliability needs careful eval design and decoding defaults. (Databricks function-calling eval card https://www.databricks.com/blog/unpacking-function-calling-eval)

### Voyager agent loop defaults (concrete parameters)
Voyager uses: **gpt-4-0314** (code/curriculum/verification), **gpt-3.5-turbo-0301** (self-ask), embeddings **text-embedding-ada-002**; temperatures **0** except curriculum **0.1**; abandon after **4 rounds** of refinement.  
Supports: a full agent is more than “prompting”—it’s a structured generate→execute→repair→verify loop with memory. (Voyager card https://arxiv.org/abs/2305.16291)

### Speculative Actions expected runtime ratio (latency optimization)
Expected runtime ratio:
\[
\frac{\mathbb{E}[T_{\text{spec}}]}{\mathbb{E}[T_{\text{seq}}]}=\frac{1}{2-p}\left(1+\frac{l}{L}\right)
\]
Where \(L\)=mean latency of actual API call, \(l\)=mean latency of speculative model, \(p\)=probability speculative next call matches true next call.  
Supports: predict–verify can reduce wall-clock latency, bounded by speculation accuracy and overhead. (Speculative Actions card https://arxiv.org/html/2510.04371v1)

### OpenAI “when selecting models” procedure (production tradeoffs)
Procedure: (1) set up evals baseline, (2) start with most capable model, (3) swap smaller/faster models where acceptable to optimize cost/latency.  
Supports: systematic model selection for agent components. (OpenAI practical guide https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

---

## How It Works

### A. Minimal single-agent tool loop (production-oriented)
1. **Input arrives**: user goal + any context.
2. **Agent prompt assembly**: combine **Instructions** + relevant **Memory/session history** + tool schemas/descriptions (Tools).
3. **Model step**: model outputs either:
   - **Tool call(s)** (structured), or
   - **Final response** (no tool calls).
4. **Tool execution** (if called):
   - Application executes tool(s) (data retrieval or side-effecting action).
   - Tool results are appended to the run history as observations.
5. **Loop**: feed updated history back to the model for the next decision.
6. **Exit conditions** (OpenAI Agents SDK description): loop ends when either:
   - a **final-output tool** is invoked, or
   - the model returns a response **without tool calls**.  
   (OpenAI practical guide https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

### B. Tool use mechanics (function calling) in a client-executed loop (Claude-style description)
1. You provide the model a list of tools (name + description + schema).
2. Model decides to call a tool and returns a structured **tool_use** block (stop_reason: `"tool_use"`).
3. Your application executes the function (client tool) and sends back a **tool_result**.
4. Model continues, possibly calling more tools or producing final text.  
(Anthropic tool use docs https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

### C. A concrete “agent loop with verification + memory” (Voyager pattern)
1. **Curriculum proposes next task** given ultimate goal + agent state + history.
2. **Retrieve skills** from a skill library (embedding search).
3. **Generate executable code** as the action.
4. **Execute code** in environment; collect feedback/errors.
5. **Self-verification** checks success; if fail, critique.
6. **Iterate repair** until success; if stuck after **4 rounds**, abandon and request new task.
7. **Commit new skill** to library on success.  
(Voyager card https://arxiv.org/abs/2305.16291)

### D. Guardrails + human intervention triggers (production safety)
1. **Layer guardrails**: start with privacy/content safety; add guardrails based on observed failures; then optimize security + UX.
2. **Risk-rate tools** (low/medium/high) based on read vs write, reversibility, permissions, financial impact.
3. **Escalate to human** when:
   - exceeding failure thresholds (retry/action limits), or
   - attempting high-risk actions (cancel orders, large refunds, payments).  
(OpenAI practical guide https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

---

## Teaching Approaches

### Intuitive (no math)
- “A chatbot answers once. An agent **keeps going**: it checks what it knows, decides what to do next, uses tools to get/modify information, and repeats until the goal is done.”
- Emphasize the **control shift**: the model chooses the next step, not the developer’s fixed script. (OpenAI practical guide)

### Technical (with math)
- Frame as sequential decision-making with partial observability: at each time \(t\), the agent conditions on history \(h_t\) and observation \(o_t\), produces an internal thought \(\tau_t\), then selects action \(a_t\). (ReflAct/ReAct formalization: https://arxiv.org/pdf/2505.15182v1.pdf)
- Contrast architectures by where planning lives:
  - ReAct: local step-by-step.
  - GoalAct: maintain/update a global plan \(P_t=\pi(u,T,H_t)\). (GoalAct: https://arxiv.org/html/2504.16563v2)

### Analogy-based
- **Intern with a checklist**: LLM is the intern; tools are “company systems” (calendar, database, email); memory is the intern’s notebook; guardrails are manager approvals for risky actions.
- **Robot model**: sensors/percepts and actuators/actions (Russell & Norvig agent definition).

---

## Common Misconceptions

1. **“An agent is just a bigger/better prompt.”**  
   - Why wrong: a prompt alone is a **single model call**; an agent is a **system** where the model **controls workflow execution** and can repeatedly call tools and update state until completion.  
   - Correct model: agent = **LLM + loop + tools + memory + exit conditions/guardrails**. (OpenAI practical guide)

2. **“If the model can call tools, it’s automatically reliable.”**  
   - Why wrong: tool use introduces new failure modes: wrong tool selection, wrong arguments, irrelevant calls, and evaluation pitfalls (e.g., relevance detection gaming). Performance degrades with more tools/domains.  
   - Correct model: tool calling needs **evals**, careful decoding (often **T=0.0**), and tool curation/orchestration. (Databricks eval pitfalls; LangChain benchmarking)

3. **“ReAct-style ‘thinking’ always improves agents.”**  
   - Why wrong: ReAct can fail via incoherent belief/state and short-sighted planning; reflection grounded in goal/state (ReflAct) shows large SR gains.  
   - Correct model: the loop design matters; “thought” should be **goal- and state-grounded**, not just verbose reasoning. (ReflAct card)

4. **“Long context window = long-term memory solved.”**  
   - Why wrong: long-context models still struggle on long-term conversational benchmarks; LoCoMo best long-context QA F1 reported is **51.6** vs human **87.9**, and adversarial/unanswerable cases are especially weak.  
   - Correct model: long-term memory often needs **stored observations/summaries + retrieval**, not just stuffing everything into context. (LoCoMo card https://aclanthology.org/2024.acl-long.747.pdf)

5. **“Multi-agent is always better than single-agent.”**  
   - Why wrong: production guidance recommends starting **single-agent** and moving to multi-agent only when complexity/tool overload demands it; multi-agent adds coordination overhead, latency, and failure modes.  
   - Correct model: choose the **lowest complexity** that meets reliability needs; use multi-agent patterns (manager-as-tools, handoffs) when justified. (OpenAI practical guide)

---

## Worked Examples

### Example 1: Minimal tool-using agent loop (pseudo-code you can adapt)
Goal: answer a user question that may require web/search or database lookup, then produce a final response.

```python
MAX_STEPS = 8
history = []  # session memory (short-term)

tools = {
  "lookup_order": lookup_order,     # data tool
  "issue_refund": issue_refund,     # action tool (high risk)
  "final": lambda text: text        # final-output tool concept
}

for step in range(MAX_STEPS):
    model_input = {
        "instructions": SYSTEM_INSTRUCTIONS,
        "history": history,
        "tools": TOOL_SCHEMAS
    }

    output = llm(model_input)

    if output.type == "tool_call":
        # Guardrails: risk-rate tool and possibly escalate
        if output.name == "issue_refund":
            raise HumanApprovalRequired(output)

        result = tools[output.name](**output.arguments)
        history.append({"role": "tool_result", "name": output.name, "content": result})
        continue

    # Exit condition: model returns without tool calls
    return output.text

raise RuntimeError("Exceeded step limit")
```

**Tutor notes (tie to sources):**
- Exit conditions mirror OpenAI’s description: stop when final-output tool invoked or no tool calls. (OpenAI practical guide)
- Guardrails/human approval for high-risk actions (refunds/payments) are explicitly recommended. (OpenAI practical guide)
- If students ask “what counts as memory here?”: `history` is session memory; long-term memory would be a separate store/retriever. (OpenAI Agents SDK Memory/Session references)

### Example 2: “Global plan updated each step” (GoalAct-style skeleton)
```text
Initialize plan P1 = π(user_query u, tools T, history H1=∅)

For t = 1..:
  choose next skill/action ai consistent with current plan Pt
  execute ai -> observe oi
  update history H_{t+1} = H_t ∪ {(ai, oi)}
  update plan P_{t+1} = π(u, T, H_{t+1})
  if plan indicates Finish: stop
```
**Tutor notes:** This matches the paper’s definitions \(P_t=\pi(u,T,H_t)\), \(H_t=\{(a_i,o_i)\}\), and “Finish” as final plan step. (GoalAct card)

---

## Comparisons & Trade-offs

| Architecture / Pattern | Core idea | Strengths | Common failure modes | When to choose |
|---|---|---|---|---|
| **Direct model call** | One-shot response, no loop/tools | Lowest complexity/latency | Can’t fetch fresh data or act | When task is single-step (OpenAI practical guide “use-case filter” implies agents for workflows resisting deterministic automation) |
| **Single agent + tools (ReAct-like loop)** | Iterate Thought/Action/Observation with tool calls | Flexible, simple to start | Tool overload; belief drift; local optima | Default starting point; add tools incrementally (OpenAI practical guide) |
| **Plan-and-Execute** | Make global plan then execute | Better long-horizon structure | Plans can be non-executable (exceed action space) | When tasks benefit from upfront structure but tools are stable (GoalAct positioning) |
| **GoalAct (continuous global plan updates)** | Maintain and update global plan \(P_t\) using history | Avoids local branches; improves success in LegalAgentBench | More planning overhead | When multi-branch tasks need coherence + executability (GoalAct results/ablation) |
| **Multi-agent (manager delegates / handoffs)** | Specialized agents coordinated | Reduces tool overload; specialization | Coordination overhead, latency, new failure modes | When single agent struggles with complex logic or overlapping tools (OpenAI practical guide) |

**Selection guidance grounded in sources:** OpenAI recommends starting single-agent and moving to multi-agent when logic becomes complex or tool overlap overloads the model; some agents succeed with >15 tools, others struggle with <10 overlapping tools. (OpenAI practical guide)

---

## Prerequisite Connections

- **LLMs as next-token predictors**: students need to understand an LLM is a text generator; agents wrap it in control logic (Karpathy video is a common foundation; listed resource).
- **Function calling / structured outputs**: tool use requires understanding schemas and structured calls (Anthropic tool use; OpenAI tools guide).
- **State/history in sequential decision-making**: agent behavior depends on observation + history (Russell & Norvig percept sequence; ReAct formalization).
- **Basic software architecture**: tools, orchestration, monitoring/guardrails are system components, not “prompt tricks” (OpenAI practical guide; LangGraph deployment rationale).

---

## Socratic Question Bank

1. **“What’s the smallest change you’d make to turn a chatbot into an agent?”**  
   *Good answer:* add a loop where the model can decide next steps and call tools; define exit conditions.

2. **“If an agent keeps calling tools forever, what design elements are missing?”**  
   *Good answer:* explicit exit conditions, iteration limits, and/or guardrails/human escalation (OpenAI practical guide mentions retry/action limits).

3. **“Why might adding more tools make an agent worse, not better?”**  
   *Good answer:* tool overload and instruction recall issues; benchmarking shows performance drops as domains/tools increase (LangChain ReAct benchmarking).

4. **“What’s the difference between ‘memory’ as chat history and long-term memory?”**  
   *Good answer:* session stores conversation items; long-term memory is external persistent store + retrieval (OpenAI Agents SDK Session; LoCoMo findings about observations/RAG).

5. **“How would you decide whether to use ReAct vs a global-plan approach?”**  
   *Good answer:* ReAct can get stuck in local branches; global plan updates help long-horizon multi-branch tasks (GoalAct positioning + ablation).

6. **“Which tools require human approval and why?”**  
   *Good answer:* high-risk, irreversible, financial-impact actions (cancel orders, large refunds, payments) per OpenAI guardrails guidance.

7. **“What would you measure to know your agent is improving?”**  
   *Good answer:* task success + tool-trajectory correctness; use evals baseline then optimize models (OpenAI practical guide; LangChain pass criteria).

8. **“Why can a function-calling benchmark be misleading?”**  
   *Good answer:* relevance detection subset can be gamed; decoding temperature affects scores (Databricks eval pitfalls).

---

## Likely Student Questions

**Q: What’s the crisp definition of an AI agent (vs an LLM)?**  
→ **A:** OpenAI defines agents as “systems that independently accomplish tasks on your behalf,” characterized by the **LLM controlling workflow execution** and having **tool access** with dynamic selection inside guardrails. (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Q: What are the core components of an agent architecture?**  
→ **A:** OpenAI’s “agent design foundations” lists **Model + Tools + Instructions** as the core components. (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Q: When does an agent run stop in a typical SDK loop?**  
→ **A:** In OpenAI’s Agents SDK description, `Runner.run()` loops until either (1) a **final-output tool** is invoked or (2) the model returns a response **without tool calls**. (https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf)

**Q: Why do ReAct agents fail on long tasks?**  
→ **A:** ReflAct identifies ReAct failure modes including (1) incoherent internal belief/state and (2) short-sighted planning vs long-term goal, leading to compounding errors/hallucinations. (https://arxiv.org/pdf/2505.15182v1.pdf)

**Q: Do global plans actually help, or is it just theory?**  
→ **A:** GoalAct reports higher success rates on LegalAgentBench and an ablation where removing the global plan drops ALL success from **0.8710 to 0.7896** (GLM-4-Plus). (https://arxiv.org/html/2504.16563v2)

**Q: How bad are web-browsing agents today?**  
→ **A:** On WebArena (812 tasks), best GPT-4 agent reported **14.41%** end-to-end success vs **human 78.24%**. (https://arxiv.org/html/2307.13854v4)

**Q: Why does tool calling get worse when I add more tools?**  
→ **A:** LangChain’s ReAct benchmarking shows pass rates drop as domains/tools are appended; e.g., Calendar Scheduling **gpt-4o drops to 2% at 7 domains**, consistent with “lost in the middle”/overload effects. (https://blog.langchain.com/react-agent-benchmarking/)

**Q: What decoding settings matter for function calling?**  
→ **A:** Databricks reports BFCL accuracy can vary by ~10% with decoding, and **temperature 0.0** is usually best for programmatic tool calling. (https://www.databricks.com/blog/unpacking-function-calling-eval)

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — **Surface when:** student lacks the mental model of what an LLM is (core “cognitive engine” before adding tools/loops/memory).
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — **Surface when:** student is confused about schemas/arguments, or how tool calls are represented and executed.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — **Surface when:** student wants a canonical breakdown of planning/memory/tool use with diagrams.
- [LangGraph Conceptual Docs — Agentic Concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — **Surface when:** student asks how to implement loops/branching/multi-agent orchestration in real systems.
- [ReAct (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — **Surface when:** student asks for the original Thought–Action–Observation prompting pattern.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — **Surface when:** student asks “what does an agent SDK actually provide?” (runner loop, memory, handoffs, tools).
- [OpenAI API Tools Guide](https://platform.openai.com/docs/guides/tools) — **Surface when:** student asks about tool_choice, parallel tool calls, remote MCP, or built-in tools.

---

## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
**Show when:** student asks “what are the parts of an agent?” or confuses tools vs memory vs planning.

![HuggingGPT's four-stage pipeline: LLM plans, selects, executes, and responds. (Shen et al. 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_010.png)  
**Show when:** student asks how a single LLM can orchestrate multiple tools/models in a pipeline.

![Generative agent architecture: memory, reflection, and planning modules. (Park et al. 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_012.png)  
**Show when:** student asks what “reflection” means or how long-term memory influences planning.

---

## Key Sources

- [OpenAI — A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Most direct, quotable production definition of “agent” + architecture components, loops, guardrails, and deployment tradeoffs.
- [ReflAct paper (arXiv:2505.15182)](https://arxiv.org/pdf/2505.15182v1.pdf) — Formalizes ReAct loop and documents concrete failure modes + success-rate gains from goal-grounded reflection.
- [GoalAct paper (arXiv:2504.16563)](https://arxiv.org/html/2504.16563v2) — Clear taxonomy vs ReAct/Plan-and-Execute/CodeAct and defines continuously updated global planning with ablations.
- [WebArena benchmark](https://arxiv.org/html/2307.13854v4) — Strong empirical evidence that realistic web agents remain far from human reliability.
- [OpenAI Agents SDK Memory reference](https://openai.github.io/openai-agents-python/ref/memory/) — Precise definition of session memory as implemented in a real agent SDK.