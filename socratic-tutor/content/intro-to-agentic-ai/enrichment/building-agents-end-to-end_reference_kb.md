## Core Definitions

**Agent loop**: An agent is a system that “independently accomplish[es] tasks on your behalf,” where the LLM **controls workflow execution**, dynamically selects tools within guardrails, and can halt/hand control back to the user on failure. In production implementations, an agent loop repeatedly: (a) asks the model what to do next, (b) executes any tool calls, (c) feeds tool outputs back, and (d) stops when a termination condition is met (e.g., final output or no more tool calls). (OpenAI practical guide PDF: https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf; OpenAI Agents SDK overview: https://openai.github.io/openai-agents-python/)

**System prompts / system instructions**: System/developer instructions are high-priority messages inserted into the model context that steer behavior. In the OpenAI Responses API, `instructions` is explicitly “a system (or developer) message inserted into the model’s context,” and **is not carried over** when you continue a conversation via `previous_response_id` (you must resend/replace it each turn if needed). (OpenAI Responses streaming reference: https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl)

**Structured outputs**: A set of API features that constrain model outputs to machine-parseable structures. For OpenAI, **Structured Outputs** (JSON Schema with `strict: true`) guarantees the model output **adheres to the supplied JSON Schema** (type-safe, required keys present, enums valid), distinct from “JSON mode” which only guarantees valid JSON. For Anthropic, “JSON outputs” constrain assistant text to valid JSON matching a schema, and “strict tool use” (`tools[].strict: true`) guarantees tool name + tool input schema validation via constrained decoding. (OpenAI structured outputs guide: https://platform.openai.com/docs/guides/structured-outputs/; OpenAI JSON mode vs SO guide: https://platform.openai.com/docs/guides/text-generation/json-mode; OpenAI blog on Structured Outputs: https://openai.com/index/introducing-structured-outputs-in-the-api/; Anthropic structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

**Error recovery (agent runtime)**: The set of mechanisms that detect and handle failures during an agent run—e.g., malformed tool arguments, tool execution errors, timeouts, truncation (`max_tokens`), refusals, network disconnects, and session expiry—by retrying, repairing, escalating to a human, or safely terminating. Sources emphasize concrete failure modes like truncated JSON (`stop_reason: "max_tokens"`), refusals, and malformed streamed tool arguments, plus transport-level recovery like resumable SSE streams and explicit cancellation notifications. (Anthropic fine-grained tool streaming + recovery: https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming; malformed JSON repair example: https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming; MCP transport resumability/cancellation: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports; OpenAI structured outputs failure modes: https://platform.openai.com/docs/guides/text-generation/json-mode)

**Streaming (responses + tool calls)**: Incremental delivery of model output and/or tool-call arguments over time (often via SSE). OpenAI supports SSE streaming with `stream: true` in the Responses API. Anthropic supports fine-grained streaming of tool inputs (`eager_input_streaming: true`) where tool arguments arrive as deltas that may be partial/invalid JSON until the tool block ends. (OpenAI Responses streaming: https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl; Anthropic fine-grained tool streaming: https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)

**Agent testing (stochastic systems)**: Evaluation practices for agents must account for non-determinism and multi-step tool interactions. Relevant sources emphasize: (a) benchmark-style metrics for tool-use and prompt-injection robustness (utility under attack, ASR), (b) sensitivity to decoding settings (e.g., temperature), and (c) continuous testing suites for prompt injection and adversarial inputs. (AgentDojo: https://arxiv.org/abs/2406.13352; Databricks function-calling eval pitfalls: https://www.databricks.com/blog/unpacking-function-calling-eval; AWS agentic AI security testing guidance: https://docs.aws.amazon.com/prescriptive-guidance/latest/agentic-ai-security/best-practices-input-validation.html)


## Key Formulas & Empirical Results

**Cost-aware multi-tool agent objective** (formalizes “success vs cost/latency/tool calls” tradeoff):  
\[
\max_\theta\ \mathbb{E}_{\tau\sim \pi_\theta}\big[ R(\tau)-\lambda\, C(\tau)\big]
\]  
- \(\pi_\theta\): agent policy over actions (tool call or terminate) conditioned on history/memory  
- \(R(\tau)\): task reward/success  
- \(C(\tau)\): cost (e.g., number of tool calls, latency, API fees, risk)  
- \(\lambda\): tradeoff weight  
Supports: why production agents explicitly optimize for fewer tool calls / lower latency while maintaining reliability. (Multi-tool orchestration explainer: https://arxiv.org/html/2603.22862v2)

**Tree of Thoughts (ToT) empirical gains** (search-based agent loop vs single-path reasoning):  
- Game of 24 (GPT-4, temp=0.7): ToT BFS **b=1: 45%**, **b=5: 74%** vs CoT **4.0%** and CoT-SC(k=100) **9.0%**.  
Supports: branching + evaluation/backtracking can dramatically improve reliability on some tasks. (ToT paper: https://arxiv.org/abs/2305.10601)

**Voyager loop defaults + stopping rule** (example of explicit “repair loop”):  
- Iterative refinement until verified success; if stuck **after 4 rounds**, abandon and request a new task.  
- Temperatures: **0** for most components; curriculum **0.1**.  
Supports: production-like “bounded retries” and explicit exit conditions. (Voyager: https://arxiv.org/abs/2305.16291)

**Structured Outputs reliability claim (OpenAI blog)**:  
- On complex schema-following evals: `gpt-4o-2024-08-06` + Structured Outputs scored **100%**; `gpt-4-0613` scored **<40%**.  
Supports: constrained decoding can be a step-change in reliability vs prompt-only formatting. (OpenAI Structured Outputs blog: https://openai.com/index/introducing-structured-outputs-in-the-api/)

**Structured Outputs schema constraints (OpenAI guides)**:  
- Root schema must be **object**; **all fields required** (optional via union with `null`); objects must set `additionalProperties: false`.  
- Limits: **≤5000** total object properties; **≤10** nesting levels; schema string length **≤120,000** chars; **≤1000** enum values overall.  
Supports: why schemas sometimes fail compilation/validation and how to design within limits. (OpenAI SO guide: https://platform.openai.com/docs/guides/structured-outputs/; JSON-mode/SO guide: https://platform.openai.com/docs/guides/text-generation/json-mode)

**Anthropic strict tool use + JSON outputs failure modes**:  
- Even with schema constraints, failures still possible on **refusal** or **`max_tokens` truncation** (incomplete JSON).  
Supports: why you still need truncation handling and refusal branches. (Anthropic structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

**Fine-grained tool input streaming latency example (Anthropic)**:  
- Without fine-grained streaming: ~**15s delay** with many tiny chunks; with it: ~**3s delay** with fewer/longer chunks.  
Supports: why teams accept partial/invalid JSON risk to improve UX/TTFT. (Anthropic fine-grained tool streaming: https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)

**AgentDojo prompt-injection benchmark scale + defense numbers**:  
- 4 environments, **74 tools**, **97 user tasks**, **629 security test cases**; tool chains up to **18 tool calls**.  
- Tool filtering defense lowers ASR to **7.5%** (on GPT-4o in their setup).  
Supports: why injection testing must be systematic and why “minimize tools exposed” is powerful. (AgentDojo: https://arxiv.org/abs/2406.13352)

**Function-calling eval sensitivity (Databricks)**:  
- BFCL accuracy can vary by **~10%** depending on decoding; **temperature 0.0** usually best for programmatic tool calling.  
Supports: why agent tests must pin decoding settings and run multiple trials. (Databricks: https://www.databricks.com/blog/unpacking-function-calling-eval)

**MCP transport norms (robustness requirements)**:  
- stdio framing: each JSON-RPC message is newline-delimited; messages **MUST NOT contain embedded newlines**; server **MUST NOT** write non-protocol bytes to stdout.  
- Streamable HTTP: single endpoint supports POST/GET; resumability via SSE `id` + `Last-Event-ID`; sessions via `Mcp-Session-Id`; missing required session id → **400**, terminated session → **404** (client must re-initialize).  
Supports: why transport correctness is part of “agent reliability.” (MCP spec: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)


## How It Works

### A. Canonical production agent loop (tool-using)
1. **Assemble context**
   - Include system/developer instructions (high priority).
   - Include user request + any relevant memory/state.
   - Include tool definitions (schemas) if using tool calling. (OpenAI function calling guide: https://platform.openai.com/docs/guides/function-calling)

2. **Model step**
   - Call the model (optionally streaming).
   - Model returns either:
     - a normal assistant message, or
     - one or more tool calls (name + arguments). (OpenAI function calling guide)

3. **Validate + execute tool calls**
   - If using schema-constrained tool calling (e.g., OpenAI Structured Outputs / Anthropic strict tools), tool args are guaranteed to match schema *unless refusal/truncation interrupts* (see failure modes below).
   - Execute tool(s) in application code; capture outputs/errors.

4. **Feed tool outputs back**
   - Send tool outputs to the model in a follow-up request.
   - Repeat until termination condition.

5. **Exit conditions**
   - OpenAI practical guide (Agents SDK behavior): loop ends when either:
     1) a **final-output tool** is invoked, or
     2) the model returns a response **without tool calls**. (OpenAI practical guide PDF)

6. **Guardrails + escalation**
   - Apply layered guardrails; escalate on high-risk actions or repeated failures. (OpenAI practical guide PDF; Swiss-cheese guardrails paper: https://arxiv.org/html/2408.02205v3)

### B. OpenAI Responses API: system instructions + conversation carryover + truncation
Key mechanics a tutor may need to recall precisely:
- `instructions` is inserted as system/developer context.
- If you use `previous_response_id`, **instructions are not carried over** to the next response. (OpenAI Responses streaming reference)
- `truncation: "auto"` drops items from the **beginning** of conversation to fit context; `truncation: "disabled"` fails with **400** if too long. (OpenAI Responses streaming reference)

### C. Streaming tool-call arguments (Anthropic fine-grained tool streaming)
When `stream: true` and tool has `eager_input_streaming: true`:
1. On `content_block_start` with `content_block.type == "tool_use"`:
   - event includes placeholder `input: {}`  
   - initialize accumulator: `input_json = ""` (Anthropic fine-grained tool streaming doc)

2. For each `content_block_delta` where `delta.type == "input_json_delta"`:
   - append: `input_json += delta.partial_json`

3. On `content_block_stop`:
   - parse once: `parsed = json.loads(input_json)`

Edge cases:
- Stream may never form valid JSON; if stop reason is `max_tokens`, args may end mid-field. Handle explicitly. (Anthropic fine-grained tool streaming doc)

### D. Transport-level streaming/resume (MCP Streamable HTTP)
If using MCP tools over Streamable HTTP:
1. Client sends each JSON-RPC message as a **new HTTP POST** to a single MCP endpoint path.
2. Server may respond with SSE (`text/event-stream`) or single JSON (`application/json`); client must support both.
3. Resumability:
   - server may set SSE `id` (globally unique within session/stream)
   - client resumes with `Last-Event-ID`
   - server must not replay messages from other streams.
4. Sessions:
   - server may issue `Mcp-Session-Id` on InitializeResult
   - client must include it on subsequent requests; missing required → **400**
   - terminated session → **404**, client must start new session. (MCP spec)


## Teaching Approaches

### Intuitive (no math): “LLM as a controller with a checklist”
- The model is not just “chatting”; it’s choosing the next step: answer, call a tool, or stop.
- Production reliability comes from: (1) **tight instructions**, (2) **structured outputs** so code can trust parsing, (3) **retries/repair** when tools or JSON fail, (4) **streaming** for responsiveness, and (5) **tests** that measure end-to-end behavior, not single responses.

### Technical (with math): “Policy over actions with cost”
- Model+tools define a policy \(\pi_\theta(a_t\mid h_t,m_t)\) that chooses either a tool call \((t,x)\) or termination \(r\).
- Production design is choosing \(\lambda\) in \(\mathbb{E}[R(\tau)-\lambda C(\tau)]\): more verification/retries increases \(R\) but also increases \(C\) (latency, tool calls, risk). (Multi-tool orchestration explainer)

### Analogy-based: “Compiler + runtime”
- **System prompt + schemas** are like a type system / interface definition.
- **Tool execution** is runtime.
- **Streaming** is incremental compilation output.
- **Error recovery** is exception handling + retries.
- **Testing** is integration tests with flaky dependencies (because sampling is stochastic).


## Common Misconceptions (required)

1. **“If I set JSON mode / ask for JSON, I’m guaranteed schema-correct output.”**  
   - Why wrong: OpenAI distinguishes **JSON mode** (valid JSON only) from **Structured Outputs** (schema adherence). JSON mode can still violate your schema (missing keys, wrong types).  
   - Correct model: Use **Structured Outputs** (`json_schema`, `strict: true`) when you need schema guarantees; JSON mode is weaker. (OpenAI SO guide; JSON-mode/SO guide; OpenAI blog)

2. **“Once I set system instructions, they persist automatically across turns.”**  
   - Why wrong: In OpenAI Responses API, when using `previous_response_id`, **instructions from the previous response are not carried over**.  
   - Correct model: Treat system/developer instructions as per-turn configuration; resend/replace them explicitly when chaining responses. (OpenAI Responses streaming reference)

3. **“Streaming tool arguments means I can parse JSON as it arrives.”**  
   - Why wrong: Anthropic fine-grained tool streaming explicitly streams **partial/invalid JSON** deltas; you’re supposed to accumulate a string and parse only at block end.  
   - Correct model: Accumulate `partial_json` into a buffer; parse on `content_block_stop`; handle truncation (`max_tokens`) and invalid JSON. (Anthropic fine-grained tool streaming doc)

4. **“If the network disconnects, the tool call is cancelled.”**  
   - Why wrong: MCP Streamable HTTP says disconnects **should not imply cancellation**; cancellation is explicit via a CancelledNotification.  
   - Correct model: Design idempotent tools and explicit cancellation semantics; don’t assume TCP/SSE disconnect equals cancel. (MCP transport spec)

5. **“A single benchmark score tells me my agent is good.”**  
   - Why wrong: Function-calling evals can be misleading (e.g., “Relevance Detection” can be gamed by never calling tools), and scores can vary ~10% with decoding settings.  
   - Correct model: Use multiple metrics/suites (benign utility + under-attack utility + ASR; multiple function-calling categories) and pin decoding settings (often temperature 0.0 for tool calling). (Databricks function-calling eval; AgentDojo)


## Worked Examples

### 1) OpenAI Responses API: Structured Outputs (schema-validated JSON) + refusal handling (Python SDK pattern)
Use when student asks: “How do I guarantee the model returns parseable, typed JSON?”

```python
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI()

class TutorPlan(BaseModel):
    goal: str
    steps: list[str]
    stop_condition: str

response = client.responses.parse(
    model="gpt-4o-mini",
    input=[{"role": "user", "content": "Design an agent loop for tool use with retries."}],
    text_format=TutorPlan,  # Structured Outputs via schema
)

# If not refused, parsed object is available:
plan = response.output_parsed
print(plan.goal, plan.steps, plan.stop_condition)
```

Tutor notes (grounded behaviors):
- Structured Outputs guarantees schema adherence when not refused/interrupted. (OpenAI SO guide; JSON-mode/SO guide)
- If safety refusal occurs, response includes **refusal content** rather than matching schema. (OpenAI SO guide; JSON-mode/SO guide)

### 2) Anthropic fine-grained tool input streaming: accumulate deltas then parse
Use when student asks: “What do I do with `input_json_delta` events?”

Pseudocode based on the documented accumulation contract:

```python
input_json = ""

on_event(event):
    if event.type == "content_block_start" and event.content_block.type == "tool_use":
        input_json = ""  # initialize accumulator

    if event.type == "content_block_delta" and event.delta.type == "input_json_delta":
        input_json += event.delta.partial_json  # append partial JSON string

    if event.type == "content_block_stop":
        # parse only at the end
        args = json.loads(input_json)
        run_tool(args)
```

Tutor notes:
- Placeholder `input: {}` at start is intentional; deltas build the real value. (Anthropic fine-grained tool streaming doc)
- If `max_tokens` stops generation, JSON may be incomplete; you need a recovery path. (Anthropic fine-grained tool streaming doc)

### 3) Repair strategy for malformed streamed tool args (when you accept invalid JSON risk)
Use when student asks: “What if the final streamed tool args are still invalid JSON?”

The referenced workflow:
1. Accumulate all deltas into one string.
2. Run `untruncate-json` to complete truncated JSON.
3. Run `jsonrepair` to fix malformed JSON.
4. Parse + validate against schema. (Andy Jakubowski: https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming)

Also: schema simplification can reduce invalid JSON (e.g., avoid `["string","null"]` if it causes unquoted UUID emissions; use empty string sentinel instead). (Same source)


## Comparisons & Trade-offs

| Choice | What you get | What can still go wrong | When to choose | Sources |
|---|---|---|---|---|
| OpenAI **Structured Outputs** (`json_schema`, `strict: true`) | Output adheres to JSON Schema (type-safe, required keys) | Refusal; truncation (`max_output_tokens`); interruptions | Any production path needing reliable parsing/types | https://platform.openai.com/docs/guides/structured-outputs/ ; https://platform.openai.com/docs/guides/text-generation/json-mode ; https://openai.com/index/introducing-structured-outputs-in-the-api/ |
| OpenAI **JSON mode** (`json_object`) | Valid JSON only | Schema violations; “endless whitespace” risk if “JSON” not in context | Quick prototypes; legacy models; when schema not needed | https://platform.openai.com/docs/guides/text-generation/json-mode |
| Anthropic **JSON outputs** (`output_config.format`) | Assistant text is valid JSON matching schema | Refusal; `max_tokens` truncation | When you want the *assistant message* to be JSON | https://platform.claude.com/docs/en/build-with-claude/structured-outputs |
| Anthropic **strict tool use** (`tools[].strict: true`) | Tool name + tool inputs schema-validated | Refusal; truncation | When tool calls must be schema-correct | https://platform.claude.com/docs/en/build-with-claude/structured-outputs |
| Anthropic **fine-grained tool streaming** (`eager_input_streaming`) | Lower latency; tool args arrive early | Partial/invalid JSON during stream; may end invalid | UX-sensitive apps; progressive rendering | https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming |
| Single-agent vs multi-agent orchestration | Simpler vs more modular delegation | Multi-agent adds coordination overhead | Start single-agent; split when tool overload/complex logic | https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf |


## Prerequisite Connections

- **Tool calling / function calling basics**: Needed to understand the multi-step “model → tool call → execute → tool output → model” loop. (OpenAI function calling guide)
- **JSON Schema fundamentals**: Needed to design schemas within Structured Outputs constraints and interpret validation failures. (OpenAI SO guide; Anthropic structured outputs)
- **Streaming/SSE basics**: Needed to reason about partial outputs, TTFT, and resumability. (OpenAI Responses streaming; MCP Streamable HTTP; Anthropic fine-grained streaming)
- **Prompt injection threat model**: Needed to understand why guardrails and tool filtering matter in production. (AgentDojo; AWS guidance)


## Socratic Question Bank

1. **If your agent sometimes returns malformed JSON, what are the three most likely root causes: schema weakness, truncation, or refusal—and how would you distinguish them in logs?**  
   *Good answer:* Mentions refusal channel vs schema output; `max_tokens` truncation; whether using Structured Outputs vs JSON mode; streaming partials.

2. **What’s your agent’s explicit stop condition, and what happens if the model keeps calling tools forever?**  
   *Good answer:* Names a bounded loop (max tool calls / max turns) and a termination rule like “no tool calls” or “final-output tool.”

3. **If you switch from non-streaming to streaming, what new failure modes appear in your tool-call pipeline?**  
   *Good answer:* Partial/invalid JSON deltas; need accumulation; UI consistency; truncation mid-argument.

4. **How would you design a test that detects regressions when decoding randomness changes outcomes?**  
   *Good answer:* Fix temperature (often 0.0 for tool calling), run multiple seeds/samples, track distributional metrics, not single outputs; use suites like AgentDojo-style utility/ASR.

5. **Why might exposing fewer tools reduce prompt-injection success rates? What’s the tradeoff?**  
   *Good answer:* Tool filtering reduces attack surface; tradeoff is planning difficulty when tools can’t be preselected. (AgentDojo)

6. **In OpenAI Responses API, what happens to your system instructions when you use `previous_response_id`? How does that affect agent design?**  
   *Good answer:* Instructions not carried over; must resend/replace each turn. (OpenAI Responses streaming reference)

7. **If an SSE stream disconnects mid-response, do you assume cancellation? What does MCP recommend?**  
   *Good answer:* Disconnect ≠ cancel; cancel explicitly; resumability via `Last-Event-ID`. (MCP spec)

8. **What’s the difference between “valid JSON” and “schema-valid JSON,” and why does it matter for tool execution safety?**  
   *Good answer:* JSON mode vs Structured Outputs; schema-valid prevents missing required fields/wrong types. (OpenAI guides)


## Likely Student Questions (lookup table)

**Q: In OpenAI Responses API, do `instructions` persist when I pass `previous_response_id`?**  
→ **A:** No. “Instructions from the previous response are not carried over to the next response” when using `previous_response_id`. (https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl)

**Q: What’s the difference between JSON mode and Structured Outputs on OpenAI?**  
→ **A:** JSON mode guarantees **valid JSON only**; Structured Outputs guarantees the output **adheres to your JSON Schema** (required keys, types, enums). (https://platform.openai.com/docs/guides/text-generation/json-mode; https://platform.openai.com/docs/guides/structured-outputs/)

**Q: What are the hard schema constraints for OpenAI Structured Outputs?**  
→ **A:** Root must be an **object**; **all fields required** (optional via union with `null`); `additionalProperties: false`; limits include **≤5000** total properties, **≤10** nesting levels, schema string length **≤120,000** chars, **≤1000** enum values overall. (https://platform.openai.com/docs/guides/text-generation/json-mode; https://platform.openai.com/docs/guides/structured-outputs/)

**Q: Why does my Anthropic streamed tool call have `input: {}` but then deltas are strings?**  
→ **A:** That mismatch is intentional: `{}` is a placeholder slot; the real tool input arrives as `input_json_delta` fragments that you concatenate into a string and parse at `content_block_stop`. (https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)

**Q: If my streamed tool args are invalid JSON at the end, what’s a concrete recovery approach?**  
→ **A:** Accumulate the full argument string, then repair (e.g., `untruncate-json` then `jsonrepair`), then parse/validate; also consider simplifying schemas that trigger invalid emissions. (https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming)

**Q: How does MCP stdio framing work—can I print logs to stdout?**  
→ **A:** No. Each JSON-RPC message is newline-delimited and **must not contain embedded newlines**; server **must not** write anything to stdout that isn’t a valid MCP message. Logs may go to **stderr**. (https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

**Q: What metrics should I use to test prompt-injection robustness for tool agents?**  
→ **A:** AgentDojo reports **Benign Utility**, **Utility Under Attack**, and **Targeted ASR** (attack success rate), across 629 security cases built from user×injection tasks. (https://arxiv.org/abs/2406.13352)

**Q: Why do my function-calling eval scores change when I change temperature?**  
→ **A:** Function-calling accuracy can vary by ~**10%** depending on decoding; Databricks notes **temperature 0.0** is usually best for programmatic tool calling. (https://www.databricks.com/blog/unpacking-function-calling-eval)


## Available Resources

### Videos
- [Intro to Large Language Models](https://youtube.com/watch?v=zjkBMFhNj_g) — Surface when: student needs a systems-level mental model of LLMs as the “cognitive core” behind agent loops.
- [AI Agents: Safety, Security, and Trust](https://youtube.com/watch?v=kJLiOGle3Lw) — Surface when: student asks about guardrails, prompt injection, and operational safety for agents.
- [OpenAI Function Calling - Full Beginner Walkthrough](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: student is stuck on the mechanics of tool calling end-to-end.
- [Let's build the GPT Tokenizer](https://youtube.com/watch?v=zduSFxRajkE) — Surface when: student asks about context windows, token budgeting, or why truncation happens.

### Articles & Tutorials
- [LLM Powered Autonomous Agents (Weng)](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: student wants the canonical breakdown of planning/memory/tools/reflection.
- [LangGraph: Agentic concepts](https://langchain-ai.github.io/langgraph/concepts/agentic_concepts/) — Surface when: student asks how to implement orchestration with persistence/streaming/HITL.
- [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) — Surface when: student asks for a production-ready agent loop abstraction with tracing/guardrails.
- [Tree of Thoughts paper](https://arxiv.org/abs/2305.10601) — Surface when: student asks how to make agents more reliable via search/backtracking.
- [OpenAI Function calling guide](https://platform.openai.com/docs/guides/function-calling) — Surface when: student needs exact tool-calling flow steps and payload structure.


## Visual Aids

![LLM agent architecture: planning, memory, and tool use components. (Weng, 2023)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: student is confused about “what parts exist besides the model” (planning vs memory vs tools) and how they connect in an end-to-end agent.

![Tree of Thoughts explores branching reasoning paths beyond linear CoT. (Yao et al. 2022)](/api/wiki-images/agent-fundamentals/images/lilianweng-posts-2023-03-15-prompt-engineering_002.png)  
Show when: student asks why “retrying” isn’t the same as “search,” or how BFS/DFS-style orchestration differs from single-shot prompting.


## Key Sources

- [A practical guide to building agents (OpenAI)](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) — Production framing: what an agent is, loop exit conditions, guardrails, single vs multi-agent tradeoffs.
- [Structured Outputs guide (OpenAI)](https://platform.openai.com/docs/guides/structured-outputs/) — Authoritative guarantees/constraints for schema-adherent JSON.
- [JSON mode vs Structured Outputs (OpenAI)](https://platform.openai.com/docs/guides/text-generation/json-mode) — Precise comparison, refusal behavior, schema constraints, SDK `parse(...)` patterns.
- [Fine-grained tool input streaming (Anthropic)](https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming) — Exact streaming event mechanics and accumulation contract for tool args.
- [MCP Transport Norms (stdio + Streamable HTTP)](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) — Normative transport requirements for robust tool-use over MCP (framing, sessions, resumability, cancellation).