# Card: Repairing malformed streamed JSON tool arguments (Anthropic fine-grained tool streaming)
**Source:** https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming  
**Role:** explainer | **Need:** WORKING_EXAMPLE  
**Anchor:** Concrete recovery procedure for malformed/partial streamed JSON tool arguments (buffering, incremental parsing, repair/retry strategy).

## Key Content
- **Feature + config:** Anthropic **fine-grained tool streaming** streams tool-argument deltas before the full argument is complete. Enable via HTTP beta header:  
  `anthropic-beta: fine-grained-tool-streaming-2025-05-14`.
- **Trade-off (correctness):** With this beta, **partial and even final tool-call JSON may be invalid** and may not match the tool JSON schema (unlike OpenAI Structured Outputs guarantees).
- **Design rationale:** Adopt despite invalid JSON risk to improve **speed/UX** by rendering partially generated code immediately (e.g., `code` parameter).
- **Schema simplification tactic (reduce invalid JSON):**
  - Problem schema allowed `["string","null"]` for `insertAfterBlockId`, causing model to emit **unquoted UUIDs** (invalid JSON):  
    Invalid: `"insertAfterBlockId": 123e4567-e89b-12d3-a456-426614174000`  
    Valid: `"insertAfterBlockId": "123e4567-e89b-12d3-a456-426614174000"`
  - Fix: restrict to `"type": "string"` and use **empty string** to mean “insert at beginning”.
- **Repair workflow (buffer → repair → parse):**
  1. **Accumulate** streamed tool-call deltas into one string (don’t repair each delta).
  2. Run `untruncate-json` to complete truncated JSON.
  3. Run `jsonrepair` to fix malformed JSON.
  4. Then parse/validate against schema.
- **Middleware interception (Vercel AI SDK):** AI SDK may throw `AI_JSONParseError` before yielding final tool-call chunk; intercept in **language model middleware** (`wrapStream`) and repair `chunk.args` when `chunk.type === 'tool-call'`, then enqueue repaired chunk. Wrap model with `wrapLanguageModel({ middleware: repairToolArgsMiddleware })`.

## When to surface
Use when students ask how to handle **invalid/partial JSON** from **streamed tool calls** (Anthropic fine-grained tool streaming), especially in **Vercel AI SDK** pipelines or when designing **tool schemas** to reduce JSON breakage.