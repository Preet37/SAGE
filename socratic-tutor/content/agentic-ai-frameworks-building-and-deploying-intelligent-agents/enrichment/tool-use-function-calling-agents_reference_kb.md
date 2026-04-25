## Core Definitions

**Tool use / tool calling** — Tool use is the capability where a model can *request* that an external tool be run, using a structured tool call, and then incorporate the returned tool result into subsequent reasoning and responses. In Anthropic’s framing, Claude “decides when to call a tool based on the user's request and the tool's description,” returns a structured `tool_use` block, and the application (client tools) or Anthropic (server tools) executes it and returns a `tool_result`. (Anthropic Docs — Tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use)

**Function calling** — Function calling (also called tool calling) is a tool-use pattern where tools are defined as functions with a JSON Schema (or OpenAPI-subset) parameter contract; the model emits a structured function call (name + arguments), the application executes the function, and the result is sent back to the model to continue the loop. OpenAI describes it as a “multi-step conversation between your application and a model,” where you define tools, receive tool calls, execute them, and send tool outputs back for a final response (or more calls). (OpenAI Function Calling Guide: https://platform.openai.com/docs/guides/function-calling)

**Tool definition (schema/contract)** — A tool definition is the metadata the model uses to decide *whether* and *how* to call a tool: at minimum a unique `name`, a natural-language `description`, and an `inputSchema`/`parameters` JSON Schema describing expected arguments; some ecosystems also support an `outputSchema` for validating structured tool results. MCP defines tools as `{name, title?, description, inputSchema, outputSchema?, annotations?}`. (MCP Tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Tool invocation (tool call)** — A tool invocation is the model’s structured request to run a tool with specific arguments. In OpenAI Responses API, tool calls appear as `response.output` items of type `function_call` with fields including `name`, `call_id`, and `arguments` (a JSON-encoded string). The app must execute the tool and return a `function_call_output` referencing the same `call_id`. (OpenAI Responses function calling reference: https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**Tool result handling (observation)** — Tool result handling is the application + model protocol for returning tool outputs (including errors) back into the conversation so the model can condition on them. MCP allows tool results to contain unstructured `content` (multi-part text/image/audio/resource links) and/or `structuredContent` (JSON object), optionally validated against an `outputSchema`. (MCP Tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Action space (agent actions)** — In ReAct’s formalism, an agent’s action space \(\mathcal{A}\) consists of environment-affecting actions (e.g., tool calls), while reasoning traces live in a separate language space \(\mathcal{L}\) that does not affect the environment. ReAct “augments action space with an unlimited language space” for thoughts, interleaving Thought → Action → Observation. (ReAct paper card, arXiv: https://arxiv.org/abs/2210.03629)

**External API integration** — External API integration is the engineering pattern where the model emits a tool call, but the *application* (or a server tool provider) performs the real network/API operation and returns results. OpenAI and Gemini both emphasize that the model does not execute tools; the app executes and returns outputs. (OpenAI tools guide: https://platform.openai.com/docs/guides/tools ; Gemini function calling card: https://ai.google.dev/gemini-api/docs/function-calling)

**Plan → act → observe loop (agentic loop)** — A repeated control loop where the model plans/decides, acts by calling tools, observes tool outputs, and repeats until it can answer. OpenAI describes a 5-step tool calling flow (request with tools → receive tool call → execute → send tool output → receive final response or more calls). ReAct frames this as interleaved Thought/Action/Observation trajectories. (OpenAI Function Calling Guide: https://platform.openai.com/docs/guides/function-calling ; ReAct: https://arxiv.org/abs/2210.03629)

---

## Key Formulas & Empirical Results

**ReAct interaction formalism (context + policy)** — ReAct defines observations \(o_t \in \mathcal{O}\), actions \(a_t \in \mathcal{A}\), and context
\[
c_t = (o_1, a_1, \ldots, o_{t-1}, a_{t-1}, o_t), \quad \pi(a_t \mid c_t)
\]
and adds a language space \(\mathcal{L}\) for “Thought” traces that do not affect the environment. Supports the claim that tool calls are *actions* and tool outputs are *observations* in a formal loop. (ReAct card: https://arxiv.org/abs/2210.03629)

**ReAct empirical improvements (selected)** — Reported prompting results (PaLM-540B) show tool/action interleaving helps in interactive settings:
- ALFWorld success: Act-only 45 vs ReAct 71 (2-shot)
- WebShop success: Act-only 30.1 vs ReAct 40 (1-shot)  
Supports the claim that explicit Thought/Action/Observation structuring can improve tool-using behavior. (ReAct card: https://arxiv.org/abs/2210.03629)

**BFCL taxonomy + pitfall** — Databricks’ analysis of BFCL notes “Relevance Detection can be gamed—if a model never calls tools, it can score 100% on this subset.” Supports the claim that evaluation must check both *correct calling* and *correct abstention* without rewarding degenerate “never call.” (Databricks BFCL/NFCL card: https://www.databricks.com/blog/unpacking-function-calling-eval)

**Decoding default for reliability** — Databricks reports BFCL accuracy can vary by ~10% depending on decoding; “Temperature 0.0 usually best for programmatic tool calling.” Supports the operational default: low temperature for schema adherence. (Databricks card: https://www.databricks.com/blog/unpacking-function-calling-eval)

**Claude strict tool use limits (schema compilation constraints)** — Claude structured outputs docs list explicit limits for strict tool use compilation:
- 20 strict tools/request
- 24 total optional parameters across all strict schemas
- 16 parameters using union types (`anyOf` or `type: [...]`)
- Compilation timeout 180s; too complex → 400 “Schema is too complex for compilation”  
Supports the claim that schema design must consider compiler limits. (Claude structured outputs card: https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

**OpenAI Responses API tool call object shape (critical field types)** — In Responses API, a function call item includes:
`{ type:"function_call", id:"fc_…", call_id:"call_…", name:"...", arguments:"{...JSON string...}" }`  
Supports the claim that `arguments` must be parsed from a JSON-encoded string and that `call_id` is the join key for returning outputs. (OpenAI Responses function calling card: https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**Parallelism control (OpenAI)** — `parallel_tool_calls: false` ensures “exactly 0 or 1 tool call per turn” (not available with built-in tools). Supports the design choice to simplify orchestration when needed. (OpenAI Responses function calling card: https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**MCP transport norms (stdio framing)** — MCP stdio requires each JSON-RPC message be newline-delimited and “MUST NOT contain embedded newlines.” Supports robust parsing/IO handling in tool servers. (MCP transports card: https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

**LangChain MCP client default session lifecycle** — `MultiServerMCPClient` is stateless by default: each tool invocation creates a fresh `ClientSession`, executes, then cleans up. Supports the claim that stateful MCP servers require explicit session management. (LangChain MCP card: https://docs.langchain.com/oss/python/langchain/mcp)

---

## How It Works

### A. Generic tool-calling loop (plan → act → observe)
1. **Assemble context**: system instructions + conversation history + **tool definitions** (names/descriptions/schemas). (OpenAI function calling flow: https://platform.openai.com/docs/guides/function-calling)
2. **Model decides** whether to answer directly or emit one or more **tool calls** (function calls). (OpenAI tools guide: https://platform.openai.com/docs/guides/tools)
3. If the model emits tool calls, the API response indicates tool usage (e.g., Claude `stop_reason: "tool_use"` for client tools). (Anthropic tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
4. **Application executes** the tool(s) using the provided structured arguments (the model does not execute tools). (OpenAI function calling: https://platform.openai.com/docs/guides/function-calling ; Gemini card: https://ai.google.dev/gemini-api/docs/function-calling)
5. **Return tool results** to the model in the next turn using the protocol’s tool-result message type (e.g., OpenAI `function_call_output` with matching `call_id`; Gemini `functionResponse` with matching `id`; Claude `tool_result`). (OpenAI Responses card: https://platform.openai.com/docs/guides/function-calling?api-mode=responses ; Gemini card: https://ai.google.dev/gemini-api/docs/function-calling ; Anthropic tool use: https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
6. **Model observes** tool outputs and either:
   - produces a final user-facing answer, or
   - emits additional tool calls (compositional/sequential calling), repeating the loop. (Gemini compositional calling: https://ai.google.dev/gemini-api/docs/function-calling ; OpenAI flow: https://platform.openai.com/docs/guides/function-calling)

### B. OpenAI Responses API: exact mechanics (function tools)
**1) Define tools**
```json
{
  "type": "function",
  "name": "get_weather",
  "description": "Get the weather for a location.",
  "parameters": { "type": "object", "properties": { "...": {} }, "required": ["..."] },
  "strict": true
}
```
Tool definitions are passed in `tools=[...]`. (OpenAI Responses card: https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**2) Model returns tool call(s)**  
Look in `response.output` for items with `type:"function_call"`. Key fields:
- `name`: which function to call
- `arguments`: JSON-encoded string (must parse)
- `call_id`: identifier you must echo back with the output  
(OpenAI Responses card: https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**3) Execute + return outputs**  
In the next `responses.create`, append:
```json
{
  "type": "function_call_output",
  "call_id": "call_...",
  "output": "..."
}
```
(OpenAI Responses card: https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**4) Parallel tool calls**  
- Default: model may emit 0/1/many calls.
- To force at most one call per turn: `parallel_tool_calls: false`. (OpenAI Responses card)

**5) Tool choice control**  
`tool_choice` options include `"auto"`, `"required"`, `"none"`, forcing a specific tool, or restricting to an allowed subset without changing `tools`. (OpenAI Responses card)

### C. MCP tool invocation (client ↔ server)
1. Client discovers tools via `tools/list`. (MCP tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
2. Client invokes via `tools/call` with arguments validated against `inputSchema`. (MCP tools spec)
3. Server returns a tool result with:
   - `content` (unstructured, multi-part) and/or
   - `structuredContent` (JSON), ideally also serialized into a text block for backward compatibility. (MCP tools spec)
4. If `outputSchema` is provided:
   - server MUST conform,
   - client SHOULD validate. (MCP tools spec)

---

## Teaching Approaches

### Intuitive (no math)
- “The model can’t *do* things; it can only *ask* for things to be done.”
- Tools are the “verbs” you give the agent (search, fetch, calculate, write to DB).
- Function calling is the standardized way the model asks: *tool name + typed arguments*.
- The app runs the tool, then the model reads the result and continues. (OpenAI tool calling flow: https://platform.openai.com/docs/guides/function-calling)

### Technical (with math)
- Frame as a policy \(\pi(a_t \mid c_t)\) over an action space \(\mathcal{A}\) where actions include tool calls; tool outputs are observations \(o_t\). ReAct separates “Thought” traces into \(\mathcal{L}\) (non-environment-affecting) while tool calls are in \(\mathcal{A}\). (ReAct: https://arxiv.org/abs/2210.03629)
- Reliability hinges on constraining the action emission channel (schemas / strict tool use) and validating observations (tool result schemas). (Claude strict tool use: https://platform.claude.com/docs/en/build-with-claude/structured-outputs ; MCP outputSchema: https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

### Analogy-based
- “The model is a dispatcher; tools are employees.”
- Tool definitions are the employee handbook (what each employee does, what form to fill out).
- Tool calls are filled-out forms; tool results are completed work orders returned to the dispatcher.
- Strict schemas are like forcing the dispatcher to use a digital form with required fields so the employee can always execute it. (OpenAI strict + Claude strict tool use docs)

---

## Common Misconceptions

1) **“The model executes the API call itself.”**  
- **Why wrong:** OpenAI and Gemini both describe a loop where the model emits a call request, and the *application executes code* and returns outputs; the model does not run tools. (OpenAI function calling: https://platform.openai.com/docs/guides/function-calling ; Gemini card: https://ai.google.dev/gemini-api/docs/function-calling)  
- **Correct model:** The model selects tools + arguments; your runtime performs side effects and returns observations.

2) **“If I provide a JSON Schema, the model will always follow it.”**  
- **Why wrong:** Schema adherence depends on enforcement mode. Claude requires `tools[].strict: true` for guaranteed schema validation on tool names/inputs; otherwise you can still see malformed calls. (Claude structured outputs: https://platform.claude.com/docs/en/build-with-claude/structured-outputs)  
- **Correct model:** Use strict/constrained decoding where available; otherwise validate and retry/repair.

3) **“Tool calling success is just ‘did it call the right tool’.”**  
- **Why wrong:** Benchmarks separate multiple dimensions: tool selection, argument correctness, parallel/nested calls, and *abstention* (deciding no tool is needed). BFCL includes relevance detection; Databricks notes it can be gamed if a model never calls tools. (BFCL cards: https://proceedings.mlr.press/v267/patil25a.html ; Databricks: https://www.databricks.com/blog/unpacking-function-calling-eval)  
- **Correct model:** Evaluate selection + arguments + sequencing + abstention, and guard against degenerate strategies.

4) **“Tool results are always plain text.”**  
- **Why wrong:** MCP tool results can be multi-part (text/image/audio/resource links) and/or structured JSON in `structuredContent`, optionally validated by `outputSchema`. (MCP tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools)  
- **Correct model:** Treat tool outputs as typed payloads; parse structured content and validate when possible.

5) **“More tools in context always helps.”**  
- **Why wrong:** LangChain’s ReAct benchmarking shows adding domains/tools/context can degrade pass rates; longer tool trajectories degrade faster as domains increase. (LangChain ReAct benchmarking card: https://blog.langchain.com/react-agent-benchmarking/)  
- **Correct model:** Keep active toolsets small; consider tool search / deferred loading where supported. (OpenAI tools guide mentions tool_search: https://platform.openai.com/docs/guides/tools)

---

## Worked Examples

### Example 1 — OpenAI Responses API function calling (single tool, full loop)

**Goal:** user asks for a horoscope; model calls `get_horoscope(sign)`; app executes; model responds. This mirrors OpenAI’s guide structure and the Responses API tool-call object shapes. (OpenAI function calling guide + Responses card)

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

# 1) Send user input + tools
input_list = [{"role": "user", "content": "What is my horoscope? I am an Aquarius."}]
resp1 = client.responses.create(model="gpt-5", tools=tools, input=input_list)

# 2) Extract tool calls
tool_calls = [item for item in resp1.output if item.type == "function_call"]
if not tool_calls:
    print(resp1.output_text)
    raise SystemExit

call = tool_calls[0]
args = json.loads(call.arguments)  # arguments is a JSON-encoded string (per docs)
result = get_horoscope(**args)

# 3) Send tool output back, keyed by call_id
input_list.extend(resp1.output)  # include prior model output items as context
input_list.append({
    "type": "function_call_output",
    "call_id": call.call_id,
    "output": result
})

resp2 = client.responses.create(model="gpt-5", tools=tools, input=input_list)
print(resp2.output_text)
```

**Tutor notes (what to emphasize mid-conversation):**
- `arguments` is a **string containing JSON**; you must parse it. (OpenAI Responses card: https://platform.openai.com/docs/guides/function-calling?api-mode=responses)
- The join key for returning results is `call_id` via `function_call_output`. (Same source)
- Expect 0/1/many tool calls; iterate `resp.output`. (Same source)

### Example 2 — Gemini: parallel calls + `id` mapping
Gemini may emit multiple `functionCall`s in one turn; each has a unique `id`, and you return `functionResponse` with the same `id` so results can be returned in any order. (Gemini card: https://ai.google.dev/gemini-api/docs/function-calling)

**Tutor move:** ask the student what breaks if they assume “results come back in the same order” (answer: parallelism; must map by `id`).

---

## Comparisons & Trade-offs

| Choice | What it is | Pros | Cons / gotchas | Source |
|---|---|---|---|---|
| **Client tools vs Server tools (Anthropic)** | Client tools run in your app; server tools run on Anthropic infra | Client tools: full control, integrate private systems. Server tools: no execution wiring | Client tools require tool_result plumbing; server tools may have extra usage pricing | https://docs.anthropic.com/en/docs/build-with-claude/tool-use |
| **Strict tool use / constrained decoding vs “best effort”** | Enforce schema-valid tool calls | Fewer malformed calls; type-safe required fields | Schema complexity limits; refusals/max_tokens can still break JSON | https://platform.claude.com/docs/en/build-with-claude/structured-outputs |
| **Parallel tool calls vs single-call turns (OpenAI)** | Model emits multiple calls per response vs forcing 0/1 | Parallel can reduce latency and steps | Harder orchestration; may need to disable via `parallel_tool_calls:false` | https://platform.openai.com/docs/guides/function-calling?api-mode=responses |
| **MCP stdio vs Streamable HTTP** | Local subprocess newline-delimited JSON-RPC vs HTTP endpoint with SSE/JSON | stdio: local isolation; HTTP: remote services, resumability/session IDs | stdio forbids embedded newlines; HTTP requires version/session headers and origin validation | https://modelcontextprotocol.io/specification/2025-06-18/basic/transports |
| **Stateless vs stateful MCP sessions (LangChain)** | New session per tool call vs persistent session | Stateless is simple and robust | Stateful servers require explicit session lifecycle management | https://docs.langchain.com/oss/python/langchain/mcp |

---

## Prerequisite Connections

- **JSON Schema basics** — Tool definitions and strict tool use rely on JSON Schema fields like `type`, `properties`, `required`, and (in some systems) `additionalProperties:false`. (OpenAI Responses strict notes; Claude structured outputs)
- **Client/server responsibility split** — Students must understand the model emits requests; the app executes tools and returns outputs. (OpenAI + Gemini docs)
- **Agent loop / state** — Tool calling is multi-turn; you must carry forward conversation history and tool outputs. (OpenAI 5-step flow; Temporal agentic loop recipe emphasizes accumulated history: https://docs.temporal.io/ai-cookbook/agentic-loop-tool-call-openai-python)
- **Error handling mindset** — Tool execution can fail; protocols include error channels (MCP protocol errors vs tool execution errors). (MCP tools spec)

---

## Socratic Question Bank

1) **“Where does the tool actually run, and what evidence do you have from the protocol?”**  
Good answer: distinguishes model emitting a call vs app/server executing; cites call/output message types.

2) **“If the model returns two tool calls in one turn, how do you match outputs to calls?”**  
Good answer: uses `call_id` (OpenAI) or `id` (Gemini) mapping; doesn’t rely on order.

3) **“What’s the difference between ‘calling the right tool’ and ‘calling it correctly’?”**  
Good answer: separates selection vs argument schema correctness vs semantic correctness.

4) **“How would you design a tool schema to reduce ambiguity for the model?”**  
Good answer: specific descriptions, enums, required fields; keep toolset small (Gemini best practices mention 10–20 active tools).

5) **“What failure mode happens if you never evaluate abstention?”**  
Good answer: relevance detection gaming (Databricks BFCL pitfall).

6) **“Why might you disable parallel tool calls?”**  
Good answer: simplify orchestration, enforce stepwise dependencies; references `parallel_tool_calls:false`.

7) **“In MCP stdio transport, what breaks if your JSON contains newlines?”**  
Good answer: violates framing rule “messages MUST NOT contain embedded newlines.”

8) **“What’s one reason strict schemas still might not yield parseable output?”**  
Good answer: refusal or truncation (`max_tokens`) cases in Claude structured outputs docs.

---

## Likely Student Questions

**Q: What exactly does the model return when it wants me to run a function in OpenAI’s Responses API?**  
→ **A:** A `response.output` item with `type:"function_call"` including `name`, `call_id`, and `arguments` where `arguments` is a **JSON-encoded string** you must parse; you return a `function_call_output` with the same `call_id`. (https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**Q: How do I force the model to call a tool (or forbid tool use)?**  
→ **A:** Use `tool_choice`: `"required"` forces ≥1 tool call; `"none"` forbids tool calls; you can also force a specific tool by name or restrict to an allowed subset via `{"type":"allowed_tools", ...}`. (https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**Q: How do I ensure only one tool call happens per turn?**  
→ **A:** Set `parallel_tool_calls: false` to ensure exactly 0 or 1 tool call per turn (note: not available with built-in tools). (https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

**Q: What does “strict tool use” actually guarantee in Claude?**  
→ **A:** Setting `tools[].strict: true` guarantees schema validation on tool names and tool inputs via constrained decoding; it reduces malformed calls, but refusals (`stop_reason:"refusal"`) or truncation (`stop_reason:"max_tokens"`) can still prevent schema-matching outputs. (https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

**Q: Why do function-calling benchmarks disagree or feel misleading?**  
→ **A:** Databricks notes BFCL subsets like Relevance Detection can be gamed (never call tools → 100% on that subset), and scores can vary ~10% with decoding; temperature 0.0 is usually best for programmatic tool calling. (https://www.databricks.com/blog/unpacking-function-calling-eval)

**Q: In MCP, can tools return structured JSON, and how should clients treat it?**  
→ **A:** Yes—tools can return `structuredContent` (JSON object). If an `outputSchema` is provided, servers MUST conform and clients SHOULD validate structured results against it; for backward compatibility servers should also serialize the JSON into a text content block. (https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Q: Why might my MCP tool behave statelessly even though the server supports state?**  
→ **A:** In LangChain, `MultiServerMCPClient` is stateless by default: each tool invocation creates a fresh `ClientSession` and cleans up; for stateful behavior you must explicitly manage a persistent session. (https://docs.langchain.com/oss/python/langchain/mcp)

---

## Available Resources

### Videos
- [OpenAI Function Calling - Full Beginner Walkthrough (James Briggs)](https://youtube.com/watch?v=aqdWSYWC_LI) — **Surface when:** the student needs a code-first walkthrough of defining JSON schemas, parsing tool calls, and returning tool outputs.

### Articles & Tutorials
- [OpenAI — Function Calling Guide](https://platform.openai.com/docs/guides/function-calling) — **Surface when:** student asks for authoritative request/response fields, `tool_choice`, parallel calls, or strict mode behavior.
- [OpenAI — Tools Guide](https://platform.openai.com/docs/guides/tools) — **Surface when:** student asks what built-in tools exist (web search, file search, tool search, MCP) and how to enable them.
- [Anthropic — Tool use (Claude)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — **Surface when:** student asks client vs server tools, `stop_reason:"tool_use"`, or pricing/token overhead considerations.
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — **Surface when:** student needs the broader agent architecture context (planning/memory/tool use) beyond API mechanics.
- [Temporal — Basic Agentic Loop with Tool Calling](https://docs.temporal.io/ai-cookbook/agentic-loop-tool-call-openai-python) — **Surface when:** student asks how to implement a durable multi-turn tool loop with retries handled outside the LLM client.
- [Model Context Protocol (MCP) — Overview/spec](https://modelcontextprotocol.io/) — **Surface when:** student asks what MCP is and how tools/resources/prompts are standardized.

---

## Visual Aids

![Function-calling agent flow: interpret, call tool, use results, respond (DAIR.AI).](/api/wiki-images/function-calling/images/promptingguide-ai-agents-function-calling_001.png)  
**Show when:** student is confused about the end-to-end loop (user request → tool call → tool execution → observation → final answer).

![LLM-powered autonomous agent system overview. (Weng, 2023)](/api/wiki-images/function-calling/images/lilianweng-posts-2023-06-23-agent_001.png)  
**Show when:** student asks “where do tools fit in an agent?” (planning/memory/tool use components).

![ReAct reasoning trajectories across knowledge and decision tasks. (Yao et al., 2023)](/api/wiki-images/function-calling/images/lilianweng-posts-2023-06-23-agent_002.png)  
**Show when:** student asks why interleaving reasoning with actions helps, or how Thought/Action/Observation differs from “just call tools.”

---

## Key Sources

- [OpenAI API Docs — Function calling](https://platform.openai.com/docs/guides/function-calling) — Canonical tool-calling flow + Responses API fields and controls (`tool_choice`, parallelism, strict).
- [Anthropic Docs — Tool use (Claude)](https://docs.anthropic.com/en/docs/build-with-claude/tool-use) — Clear distinction between client vs server tools and the `tool_use`/`tool_result` loop.
- [MCP Specification — Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) — Normative definition of tool schemas and structured/unstructured tool results.
- [Claude Structured Outputs / Strict tool use](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) — Concrete guarantees + explicit schema complexity limits and failure modes.
- [ReAct (arXiv:2210.03629)](https://arxiv.org/abs/2210.03629) — Formal Thought/Action/Observation framing and empirical evidence for interleaving actions with reasoning.