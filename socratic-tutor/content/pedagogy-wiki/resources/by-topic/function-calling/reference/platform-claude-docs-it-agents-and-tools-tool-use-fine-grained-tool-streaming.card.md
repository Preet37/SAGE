# Card: Fine-grained tool input streaming (eager_input_streaming)
**Source:** https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** Step-by-step procedure for streaming tool calls (incremental tool input emission, event framing, partial tool arguments)

## Key Content
- **Purpose / rationale:** Reduce latency by streaming tool parameter values **without buffering or JSON validation**, so large tool arguments can be consumed earlier (but may be **partial/invalid JSON**).
- **Enablement (request + tool):**
  - Set tool field: `eager_input_streaming: true` on any user-defined tool you want streamed.
  - Set request field: `stream: true`.
- **Empirical latency example (chunking behavior):**
  - *Without* fine-grained streaming: ~**15s delay**, many tiny chunks (e.g., `{"`, `query": "Ty`, `peScri`…).
  - *With* fine-grained streaming: ~**3s delay**, fewer/longer chunks (e.g., `{"query": "TypeScript 5.0 5.1 5.2 5.3` then ` new features comparison`).
- **Event framing + accumulation contract (tool_use input arrives as deltas):**
  - On `content_block_start` where `content_block.type == "tool_use"`: event contains placeholder `input: {}`; initialize accumulator: **Eq. 1** `input_json = ""`.
  - For each `content_block_delta` where `delta.type == "input_json_delta"`: **Eq. 2** `input_json += delta.partial_json` (partial JSON string fragments).
  - On `content_block_stop`: **Eq. 3** `parsed = json.loads(input_json)` (parse only after block closes).
  - Type mismatch (`input: {}` object vs `partial_json` string) is **intentional**: `{}` marks the slot; deltas build the real value.
- **Edge cases / defaults:** Because there’s no validation, stream may never form valid JSON; if stop reason `max_tokens` occurs, tool args may end mid-parameter—handle incomplete input explicitly.
- **Error recovery pattern:** To return malformed JSON to the model safely, wrap it: `{"INVALID_JSON": "<invalid json string>"}` (escape quotes/special chars).
- **SDK helpers:** Python/TS provide `stream.get_final_message()` / `stream.finalMessage()` to do accumulation automatically; manual accumulation is for reacting to partial input (progress UI, early downstream requests).
- **Data retention:** Eligible for **Zero Data Retention (ZDR)**; with ZDR, data isn’t stored after the API response returns.

## When to surface
Use when students ask how to stream tool-call arguments incrementally, interpret streaming events (`content_block_*`, `input_json_delta`), or handle partial/invalid JSON and `max_tokens` truncation during tool-use streaming.