---
title: "Model Context Protocol"
subject: "Agents & Reasoning"
date: 2026-04-10
tags:
  - "subject/agents-and-reasoning"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/anthropic"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Anthropic"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# MCP Tool Ecosystem

## Video (best)
- None identified

## Blog / Written explainer (best)
- **Anthropic** — "Model Context Protocol (MCP)"  
- **Link:** [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
- Why: Canonical, up-to-date overview of MCP concepts (clients/servers, primitives, transports) with documentation-style explanations.  
- Level: beginner/intermediate

## Deep dive
- **Anthropic (GitHub)** — "Model Context Protocol" (specs, SDKs, examples)  
- **Link:** [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)
- Why: Primary source for deeper details: protocol spec, reference implementations, and practical examples that clarify tool/resource/prompt primitives and composability patterns.  
- Level: intermediate/advanced

## Original paper
- None identified

## Code walkthrough
- **Anthropic** — "Build an MCP Server"  
- **Link:** [https://modelcontextprotocol.io/quickstart](https://modelcontextprotocol.io/quickstart)
- Why: Official quickstart with runnable examples for building MCP servers, wiring clients, and understanding transports.  
- Level: intermediate

## Coverage notes
- Strong: Model Context Protocol basics; MCP clients vs servers; tool/resource/prompt primitives; practical building guidance via official docs/repos.
- Weak: Independent third-party deep dives; comparative evaluations of tool registries and discovery patterns across ecosystems.
- Gap: A widely-cited, neutral "tool discovery + registries + client integration" explainer with concrete best practices and security considerations across transports.

---

## Additional Resources for Tutor Depth

> **16 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 MCP Production Deployment Patterns (CABP, ATBA, SERF)
**Paper** · [source](https://arxiv.org/html/2603.13417v1)

*Production procedures: observability/instrumentation, latency SLOs, threat model, production readiness checklist for MCP deployments*

<details>
<summary>Key content</summary>

- **MCP production gaps (Abstract/Intro):** missing protocol primitives: **identity propagation**, **adaptive tool budgeting**, **structured error semantics** → proposed mechanisms **CABP**, **ATBA**, **SERF**.
- **CABP broker pipeline (Sec. 5.3, 12.1):** six stages per JSON-RPC request:  
  1) JWT extraction from `Authorization` header  
  2) JWT validation (signature via JWKS, expiry, issuer)  
  3) Tool-level ACL resolution/enforcement  
  4) Context injection (inject `tenant_id`, `user_id`, scopes into request context)  
  5) Response sanitization (strip cross-tenant records)  
  6) Audit emission (log identity, tool, sanitized inputs, output summary, latency, status)  
  **Ops default:** validate JWT **every request**; if expired mid-chain return **-32600**; **never cache tokens**.  
  **Hypothesis H2:** CABP adds **<15ms median** overhead.
- **Timeouts & async (Sec. 6):** sequential chain example typical latencies: **200ms + 150ms + 300ms + 400ms + 500ms planner = 1,550ms**. Failure modes: per-tool timeout (30s), chain/session timeout (100s default), planner budget exhaustion, orphaned responses.  
  **MCP Tasks pattern:** `tools/call` with `task_augment:true` → return `taskId` (~**50ms**) → poll `tasks/get` with exponential backoff (**1s start, 30s cap**) → terminal status. **Task TTL: 15 min**. Rate-limit mispolling: **429 + Retry-After** if >1 req/s.
- **Latency SLOs (Sec. 6.3, 8.4):** p99 targets: **500ms reads**, **2s moderate queries**, **5s writes**; anything **>10s → async Tasks**. Alert on **p99 per-tool** exceeding planner budget.
- **SERF structured tool errors (Sec. 7, 12.3):** tool errors via `CallToolResult` with `isError:true` should include **`retryable`** + **`suggested_action(s)`**; taxonomy: `INVALID_INPUT`, `RESOURCE_NOT_FOUND`, `RESOURCE_EXHAUSTED`, `PERMISSION_DENIED`, `UPSTREAM_FAILURE`, `INTERNAL_ERROR` with deterministic recovery mapping.
- **Write safety (Sec. 7.4):** writes require **`idempotency_key`**; store key→response in Redis/DynamoDB with **24h TTL**. Suggested caching: **30s TTL** usage data; **5 min** project lists.
- **Observability checklist (Sec. 8):** instrument per-request fields (request_id, tool_name, user_id, tenant_id, latency_ms, status, error_code, output_size_bytes), aggregated p50/p95/p99 per tool, `/health` + `/ready`, security metrics (auth failures, token validation failures, cross-tenant attempts target **0**). Use **OpenTelemetry** trace propagation (parent trace per user request; span per tool call).
- **Threat model (Sec. 9):** T1 prompt injection via tool responses → broker sanitization + output schema enforcement; T2 data exfiltration → input minimization + broker auditing + egress allowlist; T3 privilege escalation via tool chaining → broker ACLs + explicit confirmation for side-effect tools + chain policy; T4 DoS via slow/large responses → broker timeouts + response size limits + circuit breakers.
- **Production readiness checklist (Sec. 11):**  
  **Contract:** descriptive tool names/descriptions; typed JSON Schema; side effects + idempotency documented.  
  **Resilience:** Tasks for long ops; idempotency keys; structured errors; circuit breakers.  
  **Operations:** health/readiness; per-tool metrics; broker JWT+ACL; audit log.

</details>

### 📄 MCP Security & Safety Threat Taxonomy + Defenses
**Paper** · [source](https://arxiv.org/pdf/2512.08290.pdf)

*Threat taxonomy + security/trust model for MCP ecosystems (prompt/tool/context attacks, governance layers, mitigations)*

<details>
<summary>Key content</summary>

- **MCP architecture/security boundary (Sec. II):** Host mediates all LLM interactions; **LLM never connects directly** to data sources/tools. Protocol uses **JSON-RPC 2.0** over **Stdio** (local isolation) or **SSE** (remote). Starts with **capability negotiation handshake** (declare supported features like resources/prompts/logging).
- **Core primitives (Sec. II-C):**
  - **Resources:** read-only context streams identified by URIs (e.g., `file:///logs/error.txt`), can support subscriptions.
  - **Prompts:** server-defined templates bundling resources + instructions (“best practice workflows”).
  - **Tools:** executable actions exposed by servers; host is policy enforcement point.
- **Security vs Safety convergence (Sec. I-B, III-B):** security breaches (e.g., indirect prompt injection) can trigger safety failures (model “honestly” believes it’s authorized), and safety failures (hallucinated parameters) can cause security breaches (exfiltration).
- **Security vulnerability taxonomy (Table III, Sec. IV-A):**  
  Context Poisoning; Prompt Injection; Unauthorized Context Injection; Data Leakage & Privacy; Cross-Session Contamination; Supply-Chain & Model-Switch; Protocol Abuse & Name Collisions; DoS & Resource Exhaustion. Includes **phases** (Install/Update/Exec) and **impacts** (e.g., unauthorized command execution, integrity breach, cost escalation).
- **Concrete empirical result (Sec. VII-A):** **43% of MCP server implementations tested** (Equixly) **executed unsafe shell calls**, enabling RCE risk.
- **Mitigation stack (Sec. VI):**
  - **ETDI**: **cryptographically signed tool manifests**, **immutable version identifiers**, registry-based approval; **verify signatures at load + invocation**; re-authorization on functional change (anti “rug-pull”).
  - **Capability-bound execution**: OAuth-enhanced tool definitions, least privilege, short-lived creds, **mTLS**, continuous verification (Zero Trust).
  - **Context validation/sanitization**: strict delimiters separating system/user/tool content; deterministic filtering of tool outputs; provenance tracking (e.g., DDG/MindGuard).
  - **Isolation + integrity**: sandboxing (e.g., gVisor syscall interception); schema validation + signatures + nonces/timestamps to prevent replay.

</details>

### 📄 Retriever-Aware Training (RAT) for API/Tool Calling (Gorilla)
**Paper** · [source](https://proceedings.neurips.cc/paper_files/paper/2024/file/e4c61f578ff07830f5c37378dd3ecb0d-Paper-Conference.pdf)

*RAT procedure for tool/API call generation conditioned on retrieved API docs + evaluation vs strong baselines*

<details>
<summary>Key content</summary>

- **Dataset (APIBench) construction (Sec. 3.1):**
  - **1,645 APIs** total: **TorchHub 95 (exhaustive)**, **TensorFlow Hub v2 626 (filtered from 801)**, **HuggingFace 925 (top-20 per domain)**.
  - Each API converted to JSON fields: `{domain, framework, functionality, api_name, api_call, api_arguments, environment_requirements, example_code, performance, description}`.
  - Self-instruct: **GPT-4** generates **10 instructions per API → 16,450 {instruction, API} pairs**; only **18 seed examples** hand-made (6 per hub).
- **Retriever-Aware Training (RAT) (Sec. 3.2):**
  - Training prompt appends retrieved doc:  
    **`<user_prompt> Use this API documentation for reference: <retrieved_API_doc_JSON>`**
  - Rationale: retrieved docs may be wrong (imperfect recall); RAT teaches model to **use relevant docs** and **ignore irrelevant retrieval** (“judge the retriever”), reducing hallucinations and improving robustness to **test-time doc/API changes**.
  - Inference modes: **zero-shot** (no retriever) vs **retrieval** (BM25 or GPT-Index top-1 doc appended; no extra prompt tuning).
- **Evaluation metrics (Sec. 3.3):**
  - **AST subtree matching** for functional correctness of single API call.
  - **Hallucination definition:** generated API call **not a subtree of any API** in database; **accuracy + error + hallucination = 1**.
  - Human check: **AST accuracy 0.78 = human 0.78**; **code executable 0.72** (100-sample).
- **Key empirical results (Table 1, 2):**
  - **TorchHub, GPT-Index retriever:** Gorilla **61.82% acc, 0% halluc** vs GPT-4 **59.13% acc, 1.07% halluc**.
  - **Zero-shot TorchHub:** Gorilla **59.13% acc, 6.98% halluc** vs GPT-4 **38.70% acc, 36.55% halluc**.
  - **Oracle retriever + Gorilla:** TorchHub **67.20% acc (0% halluc)**; HuggingFace **91.26% acc**; TensorHub **94.16% acc**.
  - Retrieval gap (Table 2, Gorilla trained w/ oracle retriever): eval with **GPT-Index degrades 29.20% acc**, **BM25 degrades 52.27% acc** vs oracle.
- **Defaults / hyperparameters (App. A.2, Table 6):**
  - Train **5 epochs**, **lr 2e-5** (cosine decay), **batch 64**, **warmup 0.03**, **weight decay 0**, **max seq 2048**, on **8×A100 40GB**.
  - Splits: HuggingFace **90/10**, TorchHub & TensorHub **80/20**.

</details>

### 📄 StableToolBench — stabilizing ToolBench evaluation & APIs
**Paper** · [source](https://aclanthology.org/2024.findings-acl.664.pdf)

*ToolBench instability causes + StableToolBench virtual API server + stable metrics (SoPR/SoWR) and protocols.*

<details>
<summary>Key content</summary>

- **ToolBench instability evidence (Section 2):**
  - Reproduced Pass Rates on ToolBench I1-Instruction drop vs reported (Table 9):  
    - GPT-3.5-0613+CoT: **41.5 → 35.2** (−32.5%)  
    - ToolLLaMA v2+CoT: **25.0 → 15.0** (−40%)  
    - ToolLLaMA v2+DFS: **57.0 → 34.0** (−40.4%)
  - **API status drift:** only **44.4% success**, **49.2% not available**, **6.4% not authorised** (Table 10). Not-available breakdown: parsing error **52.6%**, not connectable **30.0%**, parameter change **7.3%**, not found **7.2%** (Table 11).
- **Virtual API server (Section 3.1):**
  - **Cache key:** (category, tool, API name, arguments).  
  - **Calling rule:** cache hit → return; else try real API; if real API unavailable → **LLM API simulator**; then **save response back to cache**.
  - Cache sizes (Table 2): before filtration **352,630**, after **164,980**.
  - Simulator uses **gpt-4-turbo**, conditioned on API docs + up to **5 few-shot** cached real calls.
- **Stable evaluation system (Section 3.2):**
  - **Solvable-task filtering:** majority vote of **gpt-4-turbo, gemini-pro, claude-2**; solvable if ≥2 vote solvable. Total tasks **1,100**, solvable **765** (Table 3).
  - **SoPR (Solvable Pass Rate):** evaluate only solvable tasks with **gpt-4-turbo**; answer label → score: **Solved=1, Unsolved=0.5, Unsure=0**.
  - **SoWR:** if one solved & other unsolved → solved wins; otherwise **gpt-4-turbo** decides.
- **Evaluator reliability (Table 8):** GPT-4 Turbo accuracy: solvability **80%**, answer-solving **74%**, comparison **78%** vs GPT-3.5: **65% / 68% / 56%**.
- **Stability under tool failures:** with virtual server, SoPR changes remain within variance even when **50% tools forced down** (Figure 7/Table 12).

</details>

### 📊 Berkeley Function Calling Leaderboard (BFCL) — benchmark scope & evaluation design
**Benchmark** · [source](https://proceedings.mlr.press/v267/patil25a.html)

*Standardized evaluation of LLM tool/function-calling (incl. serial/parallel calls, abstention, stateful multi-step), using AST-based validity checking; points to the live leaderboard.*

<details>
<summary>Key content</summary>

- **Definition (task):** *Function calling / tool use* = an LLM invoking **external functions/APIs/user-defined tools** in response to user queries (agentic capability).
- **Benchmark purpose (design rationale):** Created because there previously was **no standard benchmark** for function calling due to:
  1) difficulty of evaluating whether a function call is **valid**, and  
  2) difficulty acquiring **diverse, real-world functions**.
- **Evaluation coverage (procedures):**
  - Evaluates **serial** and **parallel** function calls.
  - Covers functions across **various programming languages**.
  - Uses a **novel Abstract Syntax Tree (AST) evaluation method** to judge calls; designed to **scale to thousands of functions**.
  - Benchmark construction uses a mix of **expert-curated** and **user-contributed** functions + associated prompts.
  - Includes evaluation of **abstention** and **reasoning in a stateful multi-step agentic setting** (not just single-turn).
- **Empirical takeaway (qualitative result):** Across many models, **state-of-the-art LLMs excel at single-turn calls**, but **memory, dynamic decision-making, and long-horizon reasoning** remain open challenges.
- **Where metrics live:** The paper states BFCL is accessible via the public leaderboard: **gorilla.cs.berkeley.edu/leaderboard.html** (periodically updated).

</details>

### 📖 Claude Code ↔ MCP integration & deployment patterns
**Reference Doc** · [source](https://code.claude.com/docs/en/mcp)

*Real integration topology + configuration/ops constraints for connecting Claude Code (MCP client) to MCP servers (HTTP/SSE/stdio), incl. auth, scopes, governance, and output/tool-search limits.*

<details>
<summary>Key content</summary>

- **MCP server transport options (recommended order):**
  - **Remote HTTP** (recommended for remote/cloud services; most widely supported)
  - **Remote SSE**
  - **Local stdio** (runs local process; best for direct system access/custom scripts)
- **CLI ordering rule (critical):** options `--transport`, `--env`, `--scope`, `--header` **must come before** the server name; use `--` to separate server name from command/args passed to server.  
  - Example: `claude mcp add --transport stdio myserver -- npx server`  
  - Example: `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080`
- **Dynamic capability refresh:** supports `list_changed` notifications → tools/prompts/resources refresh without reconnect.
- **Channels (push into session):** server declares `claude/channel`; client opts in with `--channels` at startup.
- **Scopes & precedence:** local (default, private; stored in `~/.claude.json` under project path) vs **project** (team-shared `.mcp.json` at repo root) vs **user** (`~/.claude.json`, cross-project). **Precedence:** local > project > user. Local overrides Claude.ai connector entries.
- **`.mcp.json` env expansion:** `${VAR}` and `${VAR:-default}` supported in `command`, `args`, `env`, `url`, `headers`.
- **OAuth specifics:** default callback uses random port; fix with `--callback-port` for pre-registered redirect `http://localhost:PORT/callback`. If no Dynamic Client Registration, use `--client-id` + `--client-secret` (masked prompt). Override discovery via `oauth.authServerMetadataUrl` (requires Claude Code **v2.1.64+**).
- **Custom auth headers:** `headersHelper` runs shell command (10s timeout) returning JSON headers; dynamic overrides static. Env vars: `CLAUDE_CODE_MCP_SERVER_NAME`, `CLAUDE_CODE_MCP_SERVER_URL`. Runs only after workspace trust (project/local scope).
- **Output limits:** warn at **10,000 tokens**; default max **25,000 tokens**; configurable via `MAX_MCP_OUTPUT_TOKENS`. Per-tool override via `_meta["anthropic/maxResultSizeChars"]` up to **500,000 chars**.
- **Tool Search:** enabled by default (defer schemas; load on demand). If `ANTHROPIC_BASE_URL` is non-first-party, tool search disabled by default unless `ENABLE_TOOL_SEARCH` set. Values: unset / `true` / `auto` / `auto:<N>` (0–100%) / `false`. Requires models supporting `tool_reference` (Sonnet 4+, Opus 4+; Haiku unsupported).
- **Org governance:** exclusive `managed-mcp.json` (system paths: macOS `/Library/Application Support/ClaudeCode/managed-mcp.json`; Linux/WSL `/etc/claude-code/managed-mcp.json`; Windows `C:\Program Files\ClaudeCode\managed-mcp.json`). Or allow/deny lists (`allowedMcpServers`, `deniedMcpServers`) matching by `serverName`, exact `serverCommand` array, or wildcard `serverUrl` patterns; **denylist overrides allowlist**.

</details>

### 📖 LangChain MCP client behavior & adapter patterns
**Reference Doc** · [source](https://docs.langchain.com/oss/python/langchain/mcp)

*Concrete client integration behavior/defaults (stateless MultiServerMCPClient; per-invocation session lifecycle) + adapter-based tool/resource/prompt consumption.*

<details>
<summary>Key content</summary>

- **Definition:** MCP is an open protocol standardizing how apps provide **tools + context** to LLMs; LangChain uses **langchain-mcp-adapters** (built on the official **MCP Python SDK**) to consume MCP servers.
- **Default client lifecycle (stateless):** `MultiServerMCPClient` is **stateless by default**: **each tool invocation** creates a **fresh `ClientSession`**, executes the tool, then **cleans up** (per-invocation session lifecycle).
- **Stateful sessions (procedure):** If you need persistent context across calls (stateful server), explicitly manage lifecycle by creating a persistent `ClientSession` via **`client.session()`** (controls MCP session lifecycle per MCP spec).
- **Transports (comparison + rationale):**
  - **HTTP / streamable-http:** Uses HTTP requests; supports **custom headers** via connection config `headers` (also supported for **SSE**, but SSE is **deprecated by MCP spec**).
  - **stdio:** Client launches server as a **subprocess** and communicates over stdin/stdout; **inherently stateful** because subprocess persists for lifetime of the connection. **However**, with `MultiServerMCPClient` **without explicit session management**, each tool call still creates a **new session**.
- **Auth mechanism:** Provide custom auth by implementing **`httpx.Auth`** (supported via MCP SDK).
- **Adapter conversions (how LangChain consumes MCP primitives):**
  - **Tools:** MCP tools → LangChain **tools**; load via **`client.get_tools()`**.
  - **Structured tool output:** If tool returns `structuredContent`, adapter wraps it as **`MCPToolArtifact`** accessible via `ToolMessage.artifact`; interceptors can transform/append it.
  - **Multimodal tool output:** Multi-part content (text/images) → LangChain **standard content blocks**; access via `ToolMessage.content_blocks`.
  - **Resources:** MCP resources → LangChain **`Blob`**; load via **`client.get_resources()`** (or `load_mcp_resources` with a session).
  - **Prompts:** MCP prompts → LangChain **messages**; load via **`client.get_prompt()`** (or `load_mcp_prompt` with a session).
- **Interceptors (design rationale):** MCP servers are separate processes and can’t access LangGraph runtime (store/context/state); **interceptors** provide middleware-like control (modify requests, retries, dynamic headers, short-circuit) and can return **`Command`** to update state/control flow (e.g., `goto="__end__"`).

</details>

### 📖 Responses API Function/Tool Calling (fields + flow)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/function-calling?api-mode=responses)

*Exact Responses API tool/function-calling request/response fields, tool_choice behavior, tool call objects/arguments, and returning tool results.*

<details>
<summary>Key content</summary>

- **Tool-calling workflow (5 steps):** (1) `responses.create(..., tools=..., input=...)` → (2) model returns tool call(s) in `response.output` → (3) app executes tool(s) using provided args → (4) append tool results as `function_call_output` items → (5) call `responses.create` again with updated `input` to get final answer (or more calls).
- **Tool definition (function tool schema):**  
  `tools: [{ "type":"function", "name", "description", "parameters": JSONSchema, "strict": bool }]`
- **Function call item (in `response.output`):**  
  `{ "type":"function_call", "id":"fc_…", "call_id":"call_…", "name":"get_weather", "arguments":"{...JSON string...}" }`  
  `arguments` is **JSON-encoded string**; parse with `json.loads(...)`.
- **Returning tool results to model:** append to next request `input`:  
  `{ "type":"function_call_output", "call_id": <matching call_id>, "output": <string | array of image/file objects> }`
- **Multiple calls:** assume **0/1/many** tool calls per response; iterate `response.output` and handle each `function_call`.
- **Reasoning models requirement:** for GPT-5 / o4-mini, **pass back any reasoning items** from model responses along with tool outputs in the next `input`.
- **tool_choice options (defaults/controls):**
  - Default: `"auto"` (model may call 0/1/many tools)
  - `"required"` (must call ≥1 tool)
  - Force one tool: `{"type":"function","name":"get_weather"}`
  - Restrict without changing `tools`: `{"type":"allowed_tools","mode":"auto","tools":[{"type":"function","name":"get_weather"}, ...]}`
  - `"none"` imitates no tools.
- **Parallel calls:** set `parallel_tool_calls: false` to ensure **exactly 0 or 1** tool call per turn. Not available with built-in tools.
- **Strict mode (recommended):** `strict:true` enforces schema via structured outputs. Requirements: every object has `additionalProperties:false`; **all** `properties` fields listed in `required`; optional via union with `null` (e.g., `"type":["string","null"]`). In **Responses API**, schemas are normalized into strict by default unless `strict:false`.

</details>

### 📖 Streaming Responses API — event sequence & assembly
**Reference Doc** · [source](https://platform.openai.com/docs/guides/streaming-responses?api-mode=responses)

*Streaming event sequence + ordering/termination semantics (incl. tool/function-call argument deltas)*

<details>
<summary>Key content</summary>

- **Enable streaming (Responses API):** set `stream: true` / `stream=True` in `client.responses.create(...)`. Iterate events (`for await ... of stream` in JS; `for event in stream` in Python).
- **Core lifecycle events (text):**  
  - `response.created` → start boundary (contains `response.id`)  
  - `response.output_text.delta` → incremental token in `delta`  
  - `response.completed` → end boundary (contains full `response`)  
  - `error` / `response.error` → failure handling
- **Event typing:** each streamed object has `type` (schema-defined). Useful types include:  
  `response.output_item.added/done`, `response.content_part.added/done`, `response.output_text.delta`, `response.text.done`, plus tool-related: `response.function_call_arguments.delta` and `response.function_call_arguments.done`.
- **Text assembly procedure (message-per-token):**
  1. On `response.output_item.added`, note `output_index` and `item.id` when `item.type === "message"`.
  2. On `response.content_part.added`, note `content_index` for the message item.
  3. Append each `response.output_text.delta.delta` **only when** `(event.item_id, output_index, content_index)` match the target message content part.
  4. Treat `response.content_part.done` / `response.output_item.done` as “part/item fully generated”; `response.completed` as final completion boundary.
- **Tool/function-call argument assembly (streaming):**
  - Accumulate `response.function_call_arguments.delta` chunks in order for a given call (correlate by the event’s identifiers); finalize when `response.function_call_arguments.done` arrives, then parse the completed arguments string (e.g., JSON) before executing the tool.
- **Design rationale:** Responses API streaming uses **semantic, type-safe events** (preferred over legacy chunked streaming) to let apps listen only to relevant events and reliably reconstruct outputs.

</details>

### 📖 Streaming tool args — `response.function_call_arguments`
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/responses-streaming/response/function_call_arguments)

*Exact streaming field name(s) and payload shape used to reconstruct tool/function call arguments*

<details>
<summary>Key content</summary>

- **Endpoint:** `POST /v1/responses` creates a model response; supports **streaming** via Server-Sent Events (SSE) when `stream: true`.
- **Streaming control (request):**
  - `stream: boolean` — if `true`, response data is streamed as generated (SSE).
  - `stream_options: { include_obfuscation }` — only set when `stream: true`.
- **Tool/function calling configuration (request):**
  - `tools: [...]` — list of tools the model may call (built-in tools, MCP tools, or **function calls/custom tools** with typed args).
  - `tool_choice` — controls how the model selects tools (e.g., `"auto"`).
  - `parallel_tool_calls: boolean` — whether tool calls may run in parallel.
  - `max_tool_calls: number` — maximum total built-in tool calls processed in a response (across all built-in tools).
- **Include extra tool-related outputs (request `include: [...]`):**
  - `web_search_call.action.sources`
  - `code_interpreter_call.outputs`
  - `computer_call_output.output.image_url`
  - `file_search_call.results`
  - `message.input_image.image_url`
  - `message.output_text.logprobs`
  - `reasoning.encrypted_content`
- **Non-streamed response shape example (for orientation):**
  - Top-level `Response` includes `id`, `object:"response"`, `status`, `output:[...]`, `tools:[]`, `tool_choice`, `parallel_tool_calls`, `usage`, etc.
  - Assistant text appears under `output[].type:"message" → content[].type:"output_text" → text`.

</details>

### 📖 Structured Outputs / JSON mode (doc index only)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/structured-outputs/json-mode)

*JSON/Structured Outputs constraints & guarantees (JSON mode vs schema-based structured outputs; refusal signaling; schema definition/validation helpers)*

<details>
<summary>Key content</summary>

- **This fetch returned a 404 “Page not found”** for the target URL; no JSON-mode/structured-output constraints, guarantees, parameters, or examples are present in the retrieved text.
- The retrieved content is **navigation-only** for the OpenAI docs site and includes links (no technical details) to:
  - **Structured output** guide: `https://platform.openai.com/api/docs/guides/structured-outputs`
  - **Function calling** guide: `https://platform.openai.com/api/docs/guides/function-calling`
  - **Using tools** guide: `https://platform.openai.com/api/docs/guides/tools`
  - **Responses API migration** guide: `https://platform.openai.com/api/docs/guides/migrate-to-responses`
- No extractable items from this source for:
  - **Formulas/equations:** none
  - **Empirical results / numbers:** none (beyond HTTP 404)
  - **Procedures/steps:** none
  - **Defaults/parameters:** none
  - **Design rationale:** none

</details>

### 📋 # Source: https://modelcontextprotocol.io/specification/2025-06-18/basic/lifecycle
**Source** · 

### 📋 # Source: https://modelcontextprotocol.io/specification/2025-06-18/server/prompts
**Source** · 

### 📋 # Source: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
**Source** · 

### 📋 # Source: https://modelcontextprotocol.io/specification/2025-11-25
**Source** · 

### 📋 MCP stdio server end-to-end wiring (TypeScript SDK)
**Code** · [source](https://github.com/cyanheads/model-context-protocol-resources/blob/main/guides/mcp-server-development-guide.md)

*End-to-end stdio server setup pattern using MCP SDK (newline-delimited JSON-RPC on stdin/stdout; stderr-only logging) with concrete server + transport wiring.*

<details>
<summary>Key content</summary>

- **Protocol/transport constraints (stdio):**
  - MCP uses **JSON-RPC 2.0**; messages are **newline-delimited** over stdio.
  - **stdin**: only MCP messages in. **stdout**: only MCP messages out. **stderr**: logging.
- **Initialization lifecycle rule (critical):**
  - Before initialization completes, **only `ping` requests** and **server `logging` notifications** are permitted; **all other requests are forbidden** until client sends `initialized`.
- **JSON-RPC message requirements (table):**
  - **Request:** `jsonrpc:"2.0"`, **id required** (string/number), `method` required, `params` optional.
  - **Response:** `jsonrpc:"2.0"`, **id matches request**, exactly one of `result` or `error`.
  - **Notification:** `jsonrpc:"2.0"`, `method` required, **id forbidden**.
- **Concrete stdio server procedure (TypeScript):**
  1. Create `McpServer({ name, version }, { capabilities: { tools: { listChanged: false }}})`.
  2. Register a tool via `server.tool("greet", z.object({ name: z.string().min(1) }), async (input)=>({ content:[{type:"text", text:`Hello, ${input.name}! Welcome to MCP.`}] }))`.
  3. Create transport: `const transport = new StdioServerTransport();`
  4. Start: `await server.connect(transport);` and **log to stderr**.
- **Manual test command (exact):**
  - `echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"greet","arguments":{"name":"World"}}}' | node build/index.js`
- **Defaults/parameters (project setup):**
  - Node target: **ES2022**, TS module: **NodeNext**, output dir `./build`, root `./src`.
  - Example deps: `@modelcontextprotocol/sdk` **^1.11.0**, `zod` **^3.24.1**.

</details>

---

## Related Topics

- [[topics/function-calling|Function Calling]]
- [[topics/agent-skills-safety|Agent Skills & Safety]]
- [[topics/agentic-coding|Agentic Coding]]
- [[topics/agent-workflows|Agent Workflows]]
