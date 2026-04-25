## Core Definitions

**ReAct pattern** — As described in Google Research’s ReAct overview and the ReAct paper (Yao et al., 2022), *ReAct* is an agent prompting/policy pattern where a language model generates **interleaved reasoning traces and task-specific actions** in a loop, typically formatted as **Thought → Action → Observation → …**, until a terminal **Answer/Buy** (or other finish action). Reasoning traces help the model “induce, track, and update action plans,” while actions let it “interface with external sources… to gather additional information,” improving interpretability and reducing hallucination/error propagation by grounding on observations. Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629), [ReAct project site](https://react-lm.github.io).

**Thought–Action–Observation (TAO) cycle** — In ReAct’s trajectory loop, a **Thought** is a language-space reasoning trace that updates the agent’s internal context but **does not affect the environment**; an **Action** is an external/environment-affecting step (e.g., a tool call like search, navigation, purchase) that produces an **Observation** (environment feedback) which is appended to context for the next step. Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629).

**Chain-of-thought (CoT) reasoning** — In this lesson’s framing (consistent with ReAct’s motivation), CoT is a prompting approach where the model produces intermediate natural-language reasoning steps to decompose and solve problems, but (in “reason-only” form) it is **ungrounded** because it cannot update knowledge from external tools/environments during the reasoning process. Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629), [Weng (agents)](https://lilianweng.github.io/posts/2023-06-23-agent/).

**Reasoning traces** — In ReAct, “reasoning traces” are the explicit **Thought** strings interleaved with actions; they are human-readable and intended to make trajectories more interpretable/diagnosable and easier to edit (“human-in-the-loop” correction by changing a few thought sentences). Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct project site](https://react-lm.github.io), [ReAct paper](https://arxiv.org/abs/2210.03629).

**Tool calling / function calling** — OpenAI defines tool (function) calling as a **multi-step conversation** where you provide the model a set of tools (often JSON-schema functions), the model emits a **tool call** (name + arguments), the application executes it, then sends the **tool output** back so the model can produce a final response or more calls. OpenAI’s guide summarizes this as a five-step flow: request with tools → receive tool call → execute → send tool output → receive final response (or more calls). Sources: [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling), [OpenAI Tools guide](https://platform.openai.com/docs/guides/tools).

**Task decomposition (in agents)** — As Weng describes in the “Planning” component of LLM agents, task decomposition is breaking a complex task into smaller subgoals/steps so an agent can handle long-horizon work more reliably; ReAct’s Thought steps often serve as the decomposition/plan updates, while Actions execute substeps and Observations provide feedback. Sources: [Weng (agents)](https://lilianweng.github.io/posts/2023-06-23-agent/), [ReAct paper](https://arxiv.org/abs/2210.03629).

**Grounded reasoning** — In ReAct’s motivation, grounding means using **external actions/tools** to obtain observations that constrain and update reasoning, reducing hallucinations and error propagation compared to purely internal reasoning. Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629).

---

## Key Formulas & Empirical Results

### ReAct interaction formalism (paper definition)
From Yao et al. (2022), at time step *t* the agent conditions on context:
\[
c_t = (o_1, a_1, \ldots, o_{t-1}, a_{t-1}, o_t), \quad \pi(a_t \mid c_t)
\]
- \(o_t \in \mathcal{O}\): observation at time *t*  
- \(a_t \in \mathcal{A}\): action at time *t*  
- \(c_t\): full interaction history up to current observation  
- \(\pi\): policy induced by the prompted LM  
ReAct augments the action space with a language space \(\mathcal{L}\) for “Thought” traces that do not affect the environment. Source: [ReAct paper](https://arxiv.org/abs/2210.03629).

### Benchmark deltas reported for ReAct (prompting on PaLM-540B)
From the ReAct paper and Google Research blog summary (same numbers):
- **HotpotQA EM (6-shot):** Standard 28.7; CoT 29.4; Act-only 25.7; **ReAct 27.4**; **Best ReAct+CoT 35.1**  
- **FEVER Acc (3-shot):** Standard 57.1; CoT 56.3; Act-only 58.9; **ReAct 60.9**; **Best ReAct+CoT 64.6**  
- **ALFWorld success (2-shot):** Act-only 45; **ReAct 71**  
- **WebShop success (1-shot):** Act-only 30.1; **ReAct 40**  
Claim supported: interleaving reasoning with actions improves interactive decision-making success and can improve fact verification/QA when combined with grounding actions. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/).

### Ablation: “inner monologue” style hurts vs ReAct
ReAct paper reports (ALFWorld): **ReAct 71 vs ReAct-IM 53** success. Claim supported: the specific interleaving format matters; not all “more reasoning text” helps. Source: [ReAct paper](https://arxiv.org/abs/2210.03629).

### ReSpAct: adding “Speak” can improve success (but depends on interaction quality)
From ReSpAct vs ReAct (2024):
- **AlfWorld success (GPT-4o, best-of-6 prompts):** **ReAct 80.6%** vs **ReSpAct 87.3%**  
- User quality ablation (“All”): Helpful Knowledgeable **85.3%**, Helpful Perturbed **52.9%**, Unhelpful **32.09%**, Human Expert **88.8%**  
- Inner-monologue ablation: **ReSpAct best-of-6 87.3%** vs **ReSpAct-IM 48.5%**  
Claim supported: adding dialogue actions (a kind of “act” channel) can reduce assumption-making and improve outcomes, but noisy/unhelpful feedback degrades performance. Source: [ReSpAct paper](https://arxiv.org/html/2411.00927v1).

### ReAct agents on Live API Bench (NL2API)
From Live API Bench (2025):
- GPT4o completion rates (direct LLM): **0.03 (SLOT)**, **0.09 (SEL)**, **0.38 (REST)**  
- With a **ReAct agent** (fixed TAO-loop budget): GPT4o improves to **0.15 (SLOT)**, **0.12 (SEL)**, **0.50 (REST)**  
Claim supported: a TAO loop can materially improve multi-step API execution success vs single-pass tool calling, though agents can still get stuck/loop (noted especially on SLOT/SEL). Source: [Live API Bench](https://arxiv.org/pdf/2506.11266.pdf).

### Tool-calling reliability defaults (empirical pitfall)
Databricks function-calling eval analysis notes decoding sensitivity and that **temperature 0.0 is usually best** for programmatic tool calling; BFCL accuracy can vary by ~10% depending on decoding. Claim supported: tool calling is brittle; use low temperature for schema adherence. Source: [Databricks blog](https://www.databricks.com/blog/unpacking-function-calling-eval).

---

## How It Works

### A. ReAct as a generic agent loop (mechanics)
1. **Initialize context** with the user goal + any system/developer instructions + tool descriptions (if tools exist).
2. **Thought:** model writes a short reasoning trace that (a) decomposes the task, (b) decides what info is missing, (c) selects the next action.
3. **Action:** model emits an environment action (e.g., `Search[...]`, `Click[...]`, `CallTool{name,args}`).
4. **Observation:** environment/tool returns feedback (search results, API output, error message, page content). Append it to the context.
5. Repeat steps 2–4 until a terminal action/answer is produced.

Key operational detail: **Thought does not change the world; Action does.** Observation is the grounding signal that constrains the next Thought. Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629).

### B. Tool calling loop (OpenAI platform framing)
OpenAI’s function/tool calling flow (5 steps):
1) Make a request to the model with tools it could call  
2) Receive a tool call from the model  
3) Execute code on the application side with input from the tool call  
4) Make a second request to the model with the tool output  
5) Receive a final response from the model (or more tool calls)

This is the “Action → Observation” half of ReAct implemented via API calls; the model’s reasoning traces are typically interleaved in the assistant messages between tool calls. Source: [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling).

### C. Practical prompt format (what the tutor can suggest)
A minimal ReAct-style transcript format (paper/blog style):
- `Thought: ...`
- `Action: <tool or env action>`
- `Observation: <tool result>`
- (repeat)
- `Answer: ...` (terminal)

ReAct paper notes **dense alternation** for reasoning-heavy tasks (HotpotQA/FEVER) and **sparse thoughts** for action-heavy tasks (ALFWorld/WebShop), with asynchronous placement of thoughts vs actions. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/).

---

## Teaching Approaches

### Intuitive (no math)
ReAct is “**think a little, do one checkable thing, look at what happened, then think again**.” The key upgrade over chain-of-thought is that the model doesn’t have to *pretend it knows*—it can take an action (search, query a database, run code), then use the observation to correct course. (Grounding via observations is the anti-hallucination lever.) Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629).

### Technical (with math)
Model the agent as a policy \(\pi(a_t \mid c_t)\) over a history context \(c_t\). ReAct expands the action space with language “Thought” tokens that update \(c_t\) without changing the environment, while tool/environment actions produce observations \(o_{t+1}\) that update \(c_{t+1}\). The performance gain comes from reducing uncertainty in \(c_t\) by acquiring informative observations rather than relying on parametric memory alone. Source: [ReAct paper](https://arxiv.org/abs/2210.03629).

### Analogy-based
ReAct is like **debugging with print statements and unit tests**:
- Thought = your hypothesis about what’s wrong / what to do next  
- Action = run a test / query a log / call an API  
- Observation = the test output  
You iterate until the hypothesis matches reality and you can ship the fix. This maps to ReAct’s emphasis on interpretability/diagnosability via human-readable trajectories. Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct project site](https://react-lm.github.io).

---

## Common Misconceptions

1) **“ReAct just means ‘show your chain-of-thought’.”**  
Why wrong: ReAct is not only reasoning text; it requires **actions that change the environment** and **observations** that feed back into the next step. CoT alone is “reason-only” and can be ungrounded.  
Correct model: ReAct = **interleaving** reasoning traces with **tool/env actions** and using observations to update the plan (TAO loop). Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629).

2) **“If I add more reasoning text (inner monologue), performance always improves.”**  
Why wrong: ReAct reports an ablation where an IM-style variant performs worse on ALFWorld (**71 vs 53**). ReSpAct similarly shows IM variants can collapse performance (e.g., **87.3% → 48.5%**).  
Correct model: The benefit comes from *useful* reasoning placed at decision points and grounded by observations; extra verbose monologue can distract or propagate errors. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [ReSpAct paper](https://arxiv.org/html/2411.00927v1).

3) **“Tool calling is the same as ReAct.”**  
Why wrong: Tool calling is an API mechanism for emitting structured calls and returning results; ReAct is a **policy/prompting pattern** that specifies *how to alternate* reasoning and acting and how to use observations to revise reasoning. You can do tool calling without explicit TAO reasoning, and you can do ReAct with non-API “actions” (e.g., textual environment commands).  
Correct model: Tool calling implements the **Action/Observation** channel; ReAct specifies the **interleaving** with reasoning traces. Sources: [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling), [ReAct paper](https://arxiv.org/abs/2210.03629).

4) **“Once tools are enabled, the model will always use them when needed.”**  
Why wrong: Tool use requires (a) deciding tools are relevant, (b) selecting the right tool, (c) producing valid arguments. Databricks notes decoding/prompting can swing accuracy and that relevance detection can be gamed; FunctionChat-Bench shows multi-turn tool-use has distinct failure modes (slot questions, relevance detection, answer completion).  
Correct model: Tool use is a learned behavior with failure modes; you often need low temperature, strong schemas, and evaluation/guardrails. Sources: [Databricks blog](https://www.databricks.com/blog/unpacking-function-calling-eval), [FunctionChat-Bench](https://arxiv.org/html/2411.14054v1).

5) **“Observations are just extra context; they don’t change the reasoning qualitatively.”**  
Why wrong: ReAct’s central claim is that observations reduce hallucination/error propagation by letting the model **update knowledge** rather than relying on internal parametric memory; Live API Bench shows completion jumps when using a ReAct agent loop (e.g., GPT4o **0.03→0.15** on SLOT).  
Correct model: Observations are the grounding signal that makes the loop *closed*; without them, the agent is open-loop and more likely to drift. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [Live API Bench](https://arxiv.org/pdf/2506.11266.pdf).

---

## Worked Examples

### Example 1: Minimal ReAct-style tool loop (OpenAI function calling)
Goal: show the tutor a concrete “TAO loop” skeleton aligned to OpenAI’s 5-step tool calling flow.

```python
from openai import OpenAI
import json

client = OpenAI()

tools = [
  {
    "type": "function",
    "name": "get_horoscope",
    "description": "Get today's horoscope for an astrological sign.",
    "parameters": {
      "type": "object",
      "properties": {
        "sign": {"type": "string", "description": "An astrological sign like Taurus or Aquarius"}
      },
      "required": ["sign"]
    }
  }
]

def get_horoscope(sign: str) -> str:
    return f"{sign}: Next Tuesday you will befriend a baby otter."

messages = [{"role": "user", "content": "What is my horoscope? I am an Aquarius."}]

while True:
    resp = client.responses.create(
        model="gpt-5",
        tools=tools,
        input=messages,
    )

    # If the model produced tool calls, execute them and append tool outputs.
    tool_calls = [o for o in resp.output if o.type == "tool_call"]
    if tool_calls:
        for call in tool_calls:
            if call.name == "get_horoscope":
                result = get_horoscope(**call.arguments)
                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                })
        continue

    # Otherwise, we have a final response (no more actions).
    print(resp.output_text)
    break
```

Tutor notes (what to point out live):
- This implements OpenAI’s “request → tool call → execute → send tool output → final response” loop. Source: [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling).
- In ReAct terms: the model’s intermediate assistant messages contain the **Thought** (if you prompt for it), the tool call is the **Action**, and the tool result you append is the **Observation**. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [OpenAI Tools guide](https://platform.openai.com/docs/guides/tools).

### Example 2: Paper-style ReAct transcript (tool = “Wikipedia search”)
Use as a whiteboard example (not runnable here, but matches ReAct’s QA framing).

```
Thought: I need two-hop evidence; I should search for entity A first.
Action: Search[Entity A wikipedia]
Observation: <snippet mentioning relation to Entity B>
Thought: Now I should verify the claim about Entity B.
Action: Search[Entity B wikipedia]
Observation: <snippet confirming the needed fact>
Thought: I can now answer with grounded evidence.
Answer: <final answer>
```

Tutor notes:
- This is the “reasoning-heavy” dense alternation style described for HotpotQA/FEVER. Source: [ReAct paper](https://arxiv.org/abs/2210.03629).

---

## Comparisons & Trade-offs

| Approach | What it does | Strengths (per sources) | Weaknesses / failure modes (per sources) | When to choose |
|---|---|---|---|---|
| CoT (reason-only) | Generate reasoning steps, no external actions | Strong reasoning decomposition | Can be **ungrounded**, hallucinate, error propagation | When no tools/env exist or task is self-contained |
| Act-only | Take actions without explicit reasoning traces | Can interact with environment | Lacks abstract planning/working memory; may fail to synthesize | Simple reactive tasks; when you want minimal verbosity |
| **ReAct** | Interleave Thought + Action + Observation | Better grounding, interpretability; strong gains on ALFWorld/WebShop; improves FEVER | Still can fail; format matters (IM ablations worse) | Multi-step tasks needing both planning and tool use |
| ReSpAct | Adds “Speak” (dialogue) actions into loop | Higher success on AlfWorld/WebShop/MultiWOZ in reported results | Sensitive to user/helpfulness; too chatty IM variants hurt | When user interaction can reduce assumptions |

Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReSpAct paper](https://arxiv.org/html/2411.00927v1).

---

## Prerequisite Connections

- **Chain-of-thought prompting**: needed to understand what “reasoning traces” are and why intermediate steps can help; ReAct builds on CoT but adds grounding actions. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [Weng (agents)](https://lilianweng.github.io/posts/2023-06-23-agent/).
- **Tool/function calling basics**: needed to understand how “Action/Observation” is implemented in APIs (OpenAI tools/functions). Sources: [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling), [OpenAI Tools guide](https://platform.openai.com/docs/guides/tools).
- **Agent loop concept (planning + feedback)**: needed to reason about multi-step execution, stopping conditions, and debugging trajectories. Source: [Weng (agents)](https://lilianweng.github.io/posts/2023-06-23-agent/).

---

## Socratic Question Bank

1) **If the model is hallucinating facts, which part of the TAO loop is missing or weak?**  
Good answer: missing/insufficient **Actions** to retrieve evidence, or not incorporating **Observations** into subsequent Thoughts (ungrounded reasoning).

2) **In your own words, what’s the difference between a Thought and an Action in ReAct?**  
Good answer: Thought updates internal context only; Action changes environment / triggers tool; Observation comes back.

3) **When would you want “dense alternation” vs “sparse thoughts”?**  
Good answer: dense for reasoning-heavy QA/verification; sparse for action-heavy interactive tasks (as described in ReAct).

4) **Suppose a tool call fails (bad args). What should the next Thought do?**  
Good answer: interpret the observation/error, revise plan/arguments, possibly ask for missing slots, then act again.

5) **Why might adding more “inner monologue” reduce performance?**  
Good answer: ablations show IM variants can distract; the key is useful reasoning + grounding, not verbosity.

6) **How would you tell whether a failure is due to tool selection vs reasoning vs observation parsing?**  
Good answer: inspect the trajectory: wrong tool chosen (Action), wrong plan (Thought), or misread tool output (Observation→Thought).

7) **What’s one reason to set temperature low for tool calling?**  
Good answer: improves schema adherence; Databricks notes T=0.0 usually best and decoding can swing accuracy.

8) **What does it mean that ReAct trajectories are “debuggable”?**  
Good answer: human-readable Thought/Action/Observation lets you pinpoint where it went wrong and edit thoughts to redirect (per Google blog/project site).

---

## Likely Student Questions

**Q: What exactly is the ReAct loop format?** → **A:** ReAct trajectories interleave **Thought → Action → Observation** repeatedly until a terminal **Answer/Buy**; Thought is a reasoning trace that doesn’t affect the environment, Action does, and Observation is environment feedback appended to context. Sources: [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/), [ReAct paper](https://arxiv.org/abs/2210.03629).

**Q: How is ReAct different from chain-of-thought?** → **A:** CoT is “reason-only” and can be ungrounded; ReAct adds **actions** to query external sources/environments and uses **observations** to update reasoning, reducing hallucination/error propagation. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/).

**Q: What benchmark evidence shows ReAct helps?** → **A:** ReAct paper reports ALFWorld success **45 (Act-only) → 71 (ReAct)** and WebShop **30.1 → 40**; FEVER accuracy **58.9 (Act-only) → 60.9 (ReAct)**; and “Best ReAct+CoT” improves HotpotQA EM to **35.1**. Sources: [ReAct paper](https://arxiv.org/abs/2210.03629), [Google Research blog](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/).

**Q: Is “tool calling” the same thing as ReAct?** → **A:** No. Tool calling is an API workflow (OpenAI’s 5-step flow) for structured calls and returning tool outputs; ReAct is a prompting/policy pattern that alternates reasoning traces with actions and uses observations to revise the plan. Sources: [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling), [ReAct paper](https://arxiv.org/abs/2210.03629).

**Q: What’s the formal definition of the context the agent conditions on?** → **A:** ReAct paper defines \(c_t = (o_1, a_1, \ldots, o_{t-1}, a_{t-1}, o_t)\) and the policy \(\pi(a_t \mid c_t)\). Source: [ReAct paper](https://arxiv.org/abs/2210.03629).

**Q: Why do people recommend temperature 0 for tool calling?** → **A:** Databricks’ function-calling eval analysis reports tool-calling accuracy can vary with decoding and that **temperature 0.0 is usually best** for programmatic tool calling. Source: [Databricks blog](https://www.databricks.com/blog/unpacking-function-calling-eval).

**Q: Does adding dialogue (“Speak”) help beyond ReAct?** → **A:** ReSpAct reports GPT-4o AlfWorld best-of-6 success **80.6% (ReAct) → 87.3% (ReSpAct)**, but performance depends strongly on user helpfulness (e.g., Helpful Perturbed **52.9%**, Unhelpful **32.09%**). Source: [ReSpAct paper](https://arxiv.org/html/2411.00927v1).

**Q: Do ReAct agents help on real tool-sequencing benchmarks?** → **A:** Live API Bench reports GPT4o completion improves with a ReAct agent to **0.15 (SLOT)**, **0.12 (SEL)**, **0.50 (REST)** vs direct LLM **0.03/0.09/0.38** respectively. Source: [Live API Bench](https://arxiv.org/pdf/2506.11266.pdf).

---

## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student needs broader agent foundations (LLM as “brain”) before ReAct/tool loops.
- [Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Paper Explained)](https://youtube.com/watch?v=_YXnMBQjGDo) — Surface when: student confuses CoT vs ReAct or asks why intermediate reasoning helps at all.
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: student asks how to implement the Action/Observation part in an API.

### Articles & Tutorials
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student asks where ReAct fits among planning/memory/tool use patterns.
- [LangGraph — Agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks how to implement agent loops/workflows with state and debugging in practice.
- [Yao et al., 2022 — ReAct](https://arxiv.org/abs/2210.03629) — Surface when: student asks for the original formalism, ablations, or benchmark tables.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — Surface when: student asks about production primitives (agent loop, tools, tracing, guardrails).
- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — Surface when: student asks for the exact tool-calling flow and schema expectations.
- [OpenAI — Tools guide](https://platform.openai.com/docs/guides/tools) — Surface when: student asks what tool types exist (web search, file search, remote MCP, etc.) and how `tools`/`tool_choice` work.

---

## Visual Aids

![ReAct reasoning trajectories across knowledge and decision-making tasks. (Yao et al., 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_002.png)  
Show when: student needs a concrete picture of **Thought/Action/Observation** trajectories and how ReAct differs from act-only.

---

## Key Sources

- [ReAct: Synergizing Reasoning and Acting in Language Models (Yao et al., 2022)](https://arxiv.org/abs/2210.03629) — Primary source for the TAO loop, formalism, and benchmark/ablation numbers.
- [Google Research blog — ReAct overview](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/) — Clear, quotable explanation of why interleaving reasoning and acting improves grounding and debuggability.
- [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling) — Canonical implementation flow for tool calls (5-step loop) used to realize ReAct “actions” in production.
- [ReSpAct paper (2024)](https://arxiv.org/html/2411.00927v1) — Empirical evidence and ablations on extending ReAct with dialogue (“Speak”) actions.
- [Live API Bench (2025)](https://arxiv.org/pdf/2506.11266.pdf) — Quantitative evidence that ReAct-style agents improve completion on executable multi-step API benchmarks.