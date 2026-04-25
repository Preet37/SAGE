## Core Definitions

**Function calling (tool calling).** As OpenAI’s Function calling guide describes it, function calling is a multi-step conversation pattern where a model can *request* that your application execute a named tool/function with structured arguments (typically defined by a JSON schema), then the application executes it and returns the tool output to the model so it can produce a final answer (or request more tool calls). (OpenAI Function calling guide: https://platform.openai.com/docs/guides/function-calling)

**Tool schema (function tool definition).** In OpenAI’s guide, a “function tool” is defined by a JSON schema-like `parameters` object describing the expected input fields (types, required fields, descriptions). The model uses this schema to format tool calls with arguments your application can parse and execute. (https://platform.openai.com/docs/guides/function-calling)

**JSON Schema (in tool use).** In MCP, each tool definition includes an `inputSchema` that is explicitly a JSON Schema describing expected parameters; tools may also provide an `outputSchema` to validate structured results. (MCP Tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Tool-use loop.** OpenAI’s guide gives a 5-step loop: (1) send model a request with tools, (2) receive tool call, (3) execute tool in your app, (4) send tool output back to model, (5) receive final response (or more tool calls). (https://platform.openai.com/docs/guides/function-calling)

**Parallel tool calling.** Databricks’ function-calling eval taxonomy (BFCL) explicitly includes “Parallel Function” (same tool invoked multiple times) and “Parallel Multiple Function” (multiple tools, multiple invocations) as distinct capabilities to evaluate. (Databricks blog: https://www.databricks.com/blog/unpacking-function-calling-eval)

**Error handling (tool calling / MCP tools).** MCP defines two error reporting mechanisms for tools: (1) protocol errors via standard JSON-RPC errors (e.g., unknown tool, invalid arguments, server errors), and (2) tool execution errors returned in tool results. (MCP Tools spec: https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Model Context Protocol (MCP).** MCP is an open protocol that standardizes how LLM applications connect to external context and capabilities using JSON-RPC 2.0 between hosts/clients/servers, supporting primitives like tools, resources, and prompts, plus lifecycle/capability negotiation and multiple transports (stdio, Streamable HTTP). (MCP overview/spec: https://modelcontextprotocol.io/specification/2025-11-25 and lifecycle/transports: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle, https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

**MCP tools (model-controlled).** MCP’s Tools spec states tools are “model-controlled,” meaning the model can discover and invoke tools automatically based on context and user prompts; the protocol does not mandate a specific UI interaction model. (https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Structured tool result (MCP).** MCP tool results can include unstructured `content` (multiple content items like text/image/audio/resource links) and/or `structuredContent` (a JSON object). For backwards compatibility, a tool that returns structured content *should* also return the serialized JSON in a TextContent block. (https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**MCP prompts (user-controlled).** MCP Prompts are “user-controlled”: servers expose prompt templates intended for explicit user selection (e.g., slash commands), though the protocol doesn’t mandate the UI. (https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)

---

## Key Formulas & Empirical Results

### Tool-calling loop (procedural “5 steps”)
OpenAI’s function calling flow is explicitly described as five high-level steps:  
1) request with tools → 2) tool call → 3) execute → 4) send tool output → 5) final response (or more tool calls).  
Supports the claim: tool calling is inherently multi-turn and application-mediated. (https://platform.openai.com/docs/guides/function-calling)

### Function-calling evaluation taxonomies (BFCL / NFCL)
Databricks summarizes BFCL categories: **Simple Function**, **Multiple Function**, **Parallel Function**, **Parallel Multiple Function**, **Relevance Detection**.  
Supports the claim: reliability includes *abstention* and *parallelism*, not just “valid JSON.” (https://www.databricks.com/blog/unpacking-function-calling-eval)

### Decoding default that improves tool calling
Databricks reports **Temperature 0.0 usually best** for programmatic tool calling; BFCL accuracy can vary by **~10%** depending on decoding settings.  
Supports the claim: tool-call correctness is sensitive to decoding configuration. (https://www.databricks.com/blog/unpacking-function-calling-eval)

### FunctionChat-Bench dataset sizes + results (tool-use dialogs)
- **Singlecall:** 500 items; tool list lengths **1/4/8**; dialog set: **45 dialogs**, **200** evaluated turns.  
- **Singlecall AVG (%):** gpt-3.5-turbo **91.4**, gpt-4-turbo **89.6**, gpt-4o **87.6**, etc.  
- **Dialog micro-AVG:** gpt-4-turbo **0.96**, gpt-4o **0.94**, gpt-3.5-turbo **0.84**, etc.  
Supports the claim: single-turn tool-call performance differs from multi-turn dialog performance; slot questions and relevance detection matter. (FunctionChat-Bench: https://arxiv.org/html/2411.14054v1)

### Claude structured outputs / strict tool use limits & defaults
From Claude structured outputs docs:
- Grammar compilation cached **24 hours since last use**.
- Limits: **20** strict tools/request; **24** total optional parameters across all strict schemas; **16** union-type parameters (`anyOf` or `type: [...]`).
- Compilation timeout **180s**; too complex → **400** “Schema is too complex for compilation”.
- Failure modes: `stop_reason: "refusal"` may not match schema; `stop_reason: "max_tokens"` can truncate JSON.  
Supports the claim: schema enforcement has operational constraints and failure modes. (https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

### Fine-grained tool input streaming accumulation “equations”
Claude fine-grained tool streaming describes explicit accumulation:
- Initialize: `input_json = ""`
- For each delta: `input_json += delta.partial_json`
- On stop: `parsed = json.loads(input_json)`  
Supports the claim: streamed tool args are delivered as string deltas and must be accumulated then parsed. (https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)

### MCP transport norms (stdio + Streamable HTTP)
Key normative requirements (selected):
- **stdio framing:** newline-delimited JSON-RPC; messages **MUST NOT contain embedded newlines**; stdout must contain only MCP messages.  
- **HTTP:** client **MUST** send `MCP-Protocol-Version` header; server may issue `Mcp-Session-Id`; missing required session ID → **400**; terminated session → **404**; on **404** client **MUST** start new session.  
Supports the claim: robust tool-use loops depend on transport/session/version rules. (https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

### MCP production deployment patterns (CABP/ATBA/SERF) — concrete numbers
From the MCP deployment patterns paper card:
- CABP overhead hypothesis: **<15ms median**.
- Example sequential chain latency: **200 + 150 + 300 + 400 + 500 + planner = 1,550ms**.
- Suggested p99 SLOs: **500ms reads**, **2s moderate queries**, **5s writes**; **>10s → async Tasks**.
- Tasks polling: start **1s** backoff, cap **30s**; TTL **15 min**; mispolling >1 req/s → **429 + Retry-After**.
- Writes require `idempotency_key` with **24h TTL** storage.  
Supports the claim: production tool calling needs budgets, async patterns, idempotency, and structured errors. (https://arxiv.org/html/2603.13417v1)

### Claude Code MCP operational limits
Claude Code MCP docs:
- Output warning at **10,000 tokens**, default max **25,000 tokens**; configurable via `MAX_MCP_OUTPUT_TOKENS`.
- Per-tool override `_meta["anthropic/maxResultSizeChars"]` up to **500,000 chars**.  
Supports the claim: clients impose practical output limits; tool design must account for them. (https://code.claude.com/docs/en/mcp)

---

## How It Works

### A. Canonical tool-calling loop (OpenAI-style)
1. **Define tools** your app can execute (function name, description, JSON schema parameters). (OpenAI guide)
2. **Send model request** including the tool definitions and the user message(s). (OpenAI guide)
3. **Model decides** whether to answer directly or emit a **tool call** (name + arguments). (OpenAI guide; Databricks “Relevance Detection” category highlights the “no call” case)
4. **Application executes** the tool call:
   - Parse arguments (validate against schema if you enforce it).
   - Call external API/database/internal code.
5. **Send tool output back** to the model in a follow-up request.
6. **Model produces final answer** (or emits additional tool calls; loop repeats). (OpenAI guide)

Tutor move: when a student asks “where does the tool actually run?” emphasize: the model *requests*; the application *executes*; the model never directly hits the network in this pattern. (OpenAI guide; MCP architecture similarly mediates via host/client/server per security paper card: https://arxiv.org/pdf/2512.08290.pdf)

### B. MCP tool discovery + invocation (protocol mechanics)
**Discovery**
1. Server declares `tools` capability during initialization (lifecycle negotiation). (MCP lifecycle: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle)
2. Client requests tool list via `tools/list` (supports pagination). (MCP tools spec)

**Invocation**
3. Client invokes a tool via `tools/call` with `name` and `arguments`. (MCP tools spec)
4. Server returns a **Tool Result**:
   - Unstructured `content` (possibly multiple blocks: text/image/audio/resource links/embedded resources), and/or
   - `structuredContent` JSON object (and should also include serialized JSON in text for backwards compatibility). (MCP tools spec)
5. If server provided `outputSchema`:
   - Server **MUST** return structured results conforming to it.
   - Client **SHOULD** validate results against it. (MCP tools spec)

**List changes**
6. If server declared `listChanged`, it **SHOULD** send `notifications/tools/list_changed` when tool list changes. (MCP tools spec)

### C. MCP lifecycle constraints that affect tool-use loops
1. **Initialization MUST be first** interaction. (MCP lifecycle)
2. Client **SHOULD NOT** send requests other than pings before server responds to `initialize`. (MCP lifecycle)
3. Server **SHOULD NOT** send requests other than pings/logging before receiving `initialized`. (MCP lifecycle)
4. Implementations **SHOULD** set timeouts; on timeout, sender **SHOULD** issue cancellation notification and stop waiting. (MCP lifecycle)

### D. Transport-level constraints (MCP)
**stdio**
- Client launches server subprocess; JSON-RPC messages are newline-delimited; messages must not contain embedded newlines; stdout must be MCP-only; stderr may be used for logs. (MCP transports)

**Streamable HTTP**
- Single endpoint supports POST/GET; client must send `Accept: application/json, text/event-stream`; server may respond with SSE or JSON; session IDs via `Mcp-Session-Id`; protocol version header `MCP-Protocol-Version` required. (MCP transports)

### E. Streaming tool arguments (Claude fine-grained tool streaming)
When `eager_input_streaming: true` and `stream: true`, tool input arrives as **string deltas** (`input_json_delta`) that must be accumulated and parsed at the end of the tool-use block:
- Start: `input_json = ""`
- Delta: `input_json += delta.partial_json`
- Stop: `json.loads(input_json)`  
Docs explicitly warn: no buffering/validation → may be partial/invalid JSON; handle `max_tokens` truncation. (https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)

---

## Teaching Approaches

### Intuitive (no math): “LLM as a dispatcher”
- The model is a **dispatcher**: it reads the user request, decides whether it needs outside help, and if so, emits a structured “job ticket” (tool name + fields).
- Your app is the **worker**: it executes the job and returns results.
- The model then **writes the user-facing response** using those results.  
Grounding: OpenAI’s 5-step flow; Databricks “Relevance Detection” highlights that sometimes the dispatcher chooses “no job ticket.” (OpenAI guide; Databricks blog)

### Technical (protocol-centric): “JSON-RPC + schemas + validation”
- In MCP, tools are discoverable (`tools/list`) and invocable (`tools/call`) over JSON-RPC 2.0.
- Inputs are constrained by `inputSchema` (JSON Schema); outputs can be constrained by `outputSchema`, where server MUST conform and client SHOULD validate.
- Errors split into protocol errors (JSON-RPC) vs tool execution errors (tool result marked error).  
Grounding: MCP tools spec. (https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

### Analogy-based: “Restaurant ordering”
- Tool schema = menu item definition (what options exist, what’s required).
- Tool call = placing an order with options filled in.
- Tool output = the dish delivered back.
- Parallel tool calling = ordering multiple dishes at once.
- Error handling = kitchen says “out of stock” (execution error) vs waiter says “that item isn’t on the menu” (protocol/unknown tool).  
Grounding: MCP’s “unknown tool” vs “tool execution errors” split; Databricks parallel categories. (MCP tools spec; Databricks blog)

---

## Common Misconceptions

1. **“If the model can call tools, it can directly access the internet / database.”**  
   - **Why wrong:** In OpenAI’s described flow, the model emits a tool call, but *your application* executes it and returns the output. In MCP’s architecture, the host mediates interactions; tools are exposed by servers and invoked via the client/host, not directly by the model.  
   - **Correct model:** The LLM is a controller that *requests* actions; the runtime (app/host) is the executor and policy gate. (OpenAI guide; MCP security architecture summary: https://arxiv.org/pdf/2512.08290.pdf)

2. **“Valid JSON means the tool call is correct.”**  
   - **Why wrong:** Benchmarks separate “Tool Call” correctness from other dialog behaviors; FunctionChat-Bench reports errors like wrong function, invented/omitted args, type/format errors even when output is parseable. Databricks also emphasizes relevance detection and parallel/nested complexity.  
   - **Correct model:** Correctness = right tool + right arguments + right decision to call (or abstain) + correct use of tool results in the final answer. (FunctionChat-Bench: https://arxiv.org/html/2411.14054v1; Databricks blog)

3. **“The model should always call a tool if tools are available.”**  
   - **Why wrong:** Databricks’ BFCL includes **Relevance Detection** (none relevant → no call). FunctionChat-Bench also treats “Relevance Detection” as a distinct output type in dialogs.  
   - **Correct model:** Tool use is conditional; abstention is part of the skill. (Databricks blog; FunctionChat-Bench)

4. **“Streaming tool arguments are always valid JSON as they arrive.”**  
   - **Why wrong:** Claude fine-grained tool streaming explicitly streams parameter values “without buffering or JSON validation,” and warns the stream may never form valid JSON; `max_tokens` can truncate mid-argument.  
   - **Correct model:** Treat streamed tool args as an *incremental string* that you accumulate and only parse at the end; implement repair/retry if needed. (Claude fine-grained streaming doc; Jakubowski repair workflow: https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming)

5. **“MCP tools and MCP prompts are the same thing.”**  
   - **Why wrong:** MCP spec distinguishes interaction models: **tools are model-controlled** (model can discover/invoke), while **prompts are user-controlled** (intended for explicit user selection).  
   - **Correct model:** Tools = executable actions for the model; Prompts = reusable templates/workflows surfaced to users. (MCP tools spec; MCP prompts spec)

---

## Worked Examples

### 1) End-to-end OpenAI function tool loop (minimal, from the guide’s structure)
Use this when a student needs the *mechanics* of the 2-request pattern.

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
        "sign": {
          "type": "string",
          "description": "An astrological sign like Taurus or Aquarius",
        },
      },
      "required": ["sign"],
    },
  },
]

def get_horoscope(sign: str) -> str:
  return f"{sign}: Next Tuesday you will befriend a baby otter."

input_list = [{"role": "user", "content": "What is my horoscope? I am an Aquarius."}]

# 1) Ask model (with tools)
resp1 = client.responses.create(
  model="gpt-5",
  tools=tools,
  input=input_list,
)

# 2) If model requested a tool call, execute it in your app
# (Exact response parsing fields depend on SDK version; the guide’s key idea is:
#  model -> tool call -> app executes -> app sends tool output back.)
```

**Tutor notes (what to emphasize mid-conversation):**
- The tool schema is what makes the model emit `{"sign": "Aquarius"}` instead of free-form text. (OpenAI guide)
- The loop is multi-turn: you *must* send tool output back for the model to incorporate it. (OpenAI guide)

Source: OpenAI Function calling guide (example structure and schema fields): https://platform.openai.com/docs/guides/function-calling

### 2) MCP stdio server “greet” tool (TypeScript wiring)
Use when a student asks “what does an MCP tool server look like?”

Key steps (from the MCP server dev guide):
1. Create server with tools capability.
2. Register tool `greet` with input validation (example uses `zod`).
3. Connect via `StdioServerTransport`.
4. Ensure stdout is MCP-only; log to stderr.

Manual test (exact command from the guide):
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"greet","arguments":{"name":"World"}}}' | node build/index.js
```

Source: MCP stdio server development guide (TypeScript SDK example):  
https://github.com/cyanheads/model-context-protocol-resources/blob/main/guides/mcp-server-development-guide.md

### 3) Handling invalid streamed JSON tool args (repair pipeline)
Use when a student hits malformed JSON with fine-grained tool streaming.

Jakubowski’s recommended workflow:
1. **Accumulate** streamed deltas into one string (don’t repair each delta).
2. Run `untruncate-json` to complete truncated JSON.
3. Run `jsonrepair` to fix malformed JSON.
4. Parse and validate against schema.

Also: simplify schemas to reduce invalid JSON (example: avoid `["string","null"]` union that led to unquoted UUIDs; use `type: "string"` and empty string sentinel).  
Source: https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming

---

## Comparisons & Trade-offs

| Topic | Option A | Option B | Trade-off / When to choose |
|---|---|---|---|
| Tool exposure primitive (MCP) | **Tools** (model-controlled) | **Prompts** (user-controlled) | Use tools for executable actions the model can autonomously invoke; use prompts for user-invoked templates/workflows. (MCP tools/prompts specs) |
| Tool output shape (MCP) | `content` (unstructured, multimodal) | `structuredContent` (+ optional `outputSchema`) | Use structured outputs when downstream code needs reliable parsing/validation; include text serialization for compatibility. (MCP tools spec) |
| MCP transport | **stdio** | **Streamable HTTP** | stdio is subprocess + newline-delimited JSON-RPC; HTTP adds sessions, SSE/JSON responses, version headers, origin checks. Choose based on local vs remote deployment and security constraints. (MCP transports spec) |
| Tool-call reliability strategy | “Best effort” generation | **Constrained decoding / strict tool use** | Claude docs: `tools[].strict: true` enforces tool name + input schema via grammar-constrained sampling, reducing JSON/schema errors but with schema complexity limits and compilation latency. (Claude structured outputs doc) |
| Tool-use performance evaluation | Single-turn call accuracy | Dialog/agentic evaluation | FunctionChat-Bench shows multi-turn behaviors (slot questions, answer completion, relevance detection) matter; single-turn scores don’t fully predict dialog performance. (FunctionChat-Bench) |

---

## Prerequisite Connections

- **JSON & JSON Schema basics.** Tool schemas and structured outputs rely on understanding types, required fields, and validation. (OpenAI function tool parameters; MCP `inputSchema`/`outputSchema`)
- **Client–server / RPC mental model.** MCP is JSON-RPC 2.0 over transports; tool calling is an application-mediated request/response loop. (MCP spec; OpenAI loop)
- **API error handling.** Distinguish protocol-level errors vs execution-level errors; design retries and user prompts accordingly. (MCP tools spec; SERF structured errors in deployment patterns card)
- **Streaming fundamentals.** Fine-grained tool streaming delivers partial argument strings; you must accumulate and handle truncation. (Claude fine-grained streaming doc)

---

## Socratic Question Bank

1. **“In the tool-calling loop, which component actually executes the API request—and why is that separation important?”**  
   *Good answer:* The application/host executes; separation enables policy, auth, auditing, and prevents the model from directly accessing systems. (OpenAI loop; MCP architecture)

2. **“Given a tool list, when should the model *not* call any tool?”**  
   *Good answer:* When no tool is relevant; abstention is part of correctness (relevance detection). (Databricks BFCL; FunctionChat-Bench taxonomy)

3. **“If you get valid JSON arguments but the wrong function name, is that a ‘formatting’ problem or a ‘tool selection’ problem?”**  
   *Good answer:* Tool selection; correctness includes choosing the right tool. (FunctionChat-Bench error taxonomy)

4. **“What’s the difference between an MCP protocol error and a tool execution error?”**  
   *Good answer:* Protocol errors are JSON-RPC errors (unknown tool/invalid args/server errors); execution errors are tool-result-level failures. (MCP tools spec)

5. **“Why might streaming tool arguments increase UX speed but decrease correctness?”**  
   *Good answer:* Because it streams without validation; partial/invalid JSON can occur; you trade latency for robustness. (Claude fine-grained streaming doc)

6. **“If an MCP server provides an `outputSchema`, what are the MUST/SHOULD obligations on server vs client?”**  
   *Good answer:* Server MUST conform; client SHOULD validate. (MCP tools spec)

7. **“What failure mode happens if your schema is too complex for strict tool compilation (Claude), and what does the API return?”**  
   *Good answer:* 400 “Schema is too complex for compilation”; compilation timeout 180s. (Claude structured outputs doc)

8. **“How would you evaluate a model that ‘never calls tools’ on a benchmark that includes relevance detection?”**  
   *Good answer:* It can game relevance-detection subsets; need balanced metrics and categories. (Databricks pitfall)

---

## Likely Student Questions

**Q: What are the exact steps in OpenAI’s tool calling flow?**  
→ **A:** The guide lists five steps: (1) request with tools, (2) receive tool call, (3) execute tool in your app, (4) send tool output back, (5) receive final response (or more tool calls). (https://platform.openai.com/docs/guides/function-calling)

**Q: In MCP, what fields define a tool and how are inputs/outputs specified?**  
→ **A:** A tool definition includes `name`, optional `title`, `description`, `inputSchema` (JSON Schema), optional `outputSchema`, and optional `annotations`. Results can include `content` (unstructured blocks) and/or `structuredContent` (JSON). (https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Q: If an MCP tool provides an output schema, who validates what?**  
→ **A:** MCP says: if `outputSchema` is provided, servers **MUST** return structured results conforming to it, and clients **SHOULD** validate structured results against it. (https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Q: What are the two error mechanisms for MCP tools?**  
→ **A:** (1) Protocol errors via standard JSON-RPC errors (unknown tools, invalid arguments, server errors), and (2) tool execution errors returned in tool results. (https://modelcontextprotocol.io/specification/2025-06-18/server/tools)

**Q: What’s the key difference between MCP prompts and tools in terms of who controls them?**  
→ **A:** Tools are designed to be **model-controlled** (model can discover/invoke automatically), while prompts are **user-controlled** (intended for explicit user selection), though MCP doesn’t mandate a UI. (Tools: https://modelcontextprotocol.io/specification/2025-06-18/server/tools; Prompts: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)

**Q: What decoding setting tends to improve function-calling reliability in practice?**  
→ **A:** Databricks reports temperature **0.0** is usually best for programmatic tool calling, and accuracy can vary by ~**10%** depending on decoding. (https://www.databricks.com/blog/unpacking-function-calling-eval)

**Q: What are common tool-use dialog failure modes beyond “bad JSON”?**  
→ **A:** FunctionChat-Bench lists errors like missing call, wrong/unknown function, redundant slot-asking, invented/omitted args, type/format errors; also “Answer Completion” failures like altering tool results. (https://arxiv.org/html/2411.14054v1)

**Q: With Claude fine-grained tool streaming, how do I reconstruct tool arguments?**  
→ **A:** Accumulate `partial_json` deltas into a string (`input_json += delta.partial_json`) and parse only when the tool-use block stops (`json.loads(input_json)`); docs warn it may be invalid/truncated. (https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)

---

## Available Resources

### Videos
- [OpenAI Function Calling - Full Beginner Walkthrough (James Briggs)](https://youtube.com/watch?v=aqdWSYWC_LI) — Surface when: the student needs a code-first walkthrough of defining JSON schemas, parsing tool calls, and implementing the tool-use loop end-to-end.

### Articles & Tutorials
- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — Surface when: the student asks for the authoritative API flow, tool definition fields, or parallel tool calling behavior.
- [Lilian Weng — LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) — Surface when: the student asks how function calling fits into agent loops (plan/act/observe) and broader agent architecture.
- [Google Research — Function calling overview + examples](https://goo.gle/4eEOLXR) — Surface when: the student wants a second vendor’s framing/use cases (augment knowledge, extend capabilities, take actions) and code examples.
- [Anthropic — Model Context Protocol (MCP) site/spec](https://modelcontextprotocol.io/) — Surface when: the student asks what MCP is and how tools/resources/prompts fit together.
- [Patil et al. (2023) — Gorilla: LLM connected with massive APIs](https://arxiv.org/abs/2305.15334) — Surface when: the student asks why models hallucinate API calls and how retrieval helps tool correctness.
- [Databricks — Unpacking function-calling eval (BFCL vs NFCL)](https://www.databricks.com/blog/unpacking-function-calling-eval) — Surface when: the student asks how to measure tool-calling quality and why leaderboards can mislead.
- [FunctionChat-Bench paper](https://arxiv.org/html/2411.14054v1) — Surface when: the student asks about multi-turn tool-use evaluation (slot questions, answer completion, relevance detection).

---

## Visual Aids

![LLM-powered autonomous agent system overview. (Weng, 2023)](/api/wiki-images/function-calling/images/lilianweng-posts-2023-06-23-agent_001.png)  
Show when: the student is confused about where “tools/function calling” sits relative to planning and memory in an agent.

![ReAct reasoning trajectories across knowledge and decision tasks. (Yao et al., 2023)](/api/wiki-images/function-calling/images/lilianweng-posts-2023-06-23-agent_002.png)  
Show when: the student struggles to understand the action–observation loop and why tool outputs change subsequent reasoning.

---

## Key Sources

- [OpenAI — Function calling guide](https://platform.openai.com/docs/guides/function-calling) — Authoritative description of the tool-calling loop and function tool schemas.
- [MCP Specification — Tools (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/server/tools) — Normative definitions for tool discovery, invocation, schemas, structured results, and error handling.
- [MCP Specification — Transports (2025-06-18)](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports) — Normative transport/session/versioning rules that affect real tool-use loops.
- [Databricks — Unpacking function-calling eval](https://www.databricks.com/blog/unpacking-function-calling-eval) — Practical taxonomy + pitfalls (relevance detection gaming, decoding sensitivity).
- [FunctionChat-Bench](https://arxiv.org/html/2411.14054v1) — Tool-use dialog taxonomy, dataset design, and quantitative results highlighting multi-turn failure modes.