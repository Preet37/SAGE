# Card: Responses API — message/items, formats, streaming, tool-choice
**Source:** https://platform.openai.com/docs/api-reference/responses/list?lang=python  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Definitions/defaults for Responses API objects: message/item formats, instruction hierarchy, output formats, streaming events, tool-choice, and includable extras.

## Key Content
- **Input message schema (EasyInputMessage):** `{role, content, phase, type}`.  
  - **Instruction hierarchy:** developer/system role instructions **take precedence** over user role instructions.  
  - Messages with **assistant** role are presumed to be model-generated in prior interactions.
- **Input content types (ResponseInputContent):** text/image/file.  
  - Text: `{type:"input_text", text}`  
  - Image: `{type:"input_image", image_url|file_id, detail}`  
  - File: `{type:"input_file", file_id|file_data, …}`
- **Output message schema (ResponseOutputMessage):** `{id, role, content, …}` with content parts such as:  
  - Text output: `{type:"output_text", text, annotations, logprobs}`  
  - Refusal: `{type:"refusal", refusal}`
- **Response status enum:** `completed | failed | in_progress | cancelled | queued | incomplete`.
- **Text output formatting (ResponseTextConfig / ResponseFormatTextConfig):**
  - Default response format: `{ "type": "text" }`.
  - Structured Outputs: `{ "type": "json_schema", name, schema, … }` (enforces schema match).
  - Older JSON mode (not recommended for gpt-4o+): `{ "type": "json_object" }` (valid JSON only).
- **Tool choice (ToolChoiceOptions):**  
  - `none` = no tools, message only; `auto` = model may choose; `required` = must call ≥1 tool.  
  - Forcing specific tools: e.g., `ToolChoiceFunction{name}`, `ToolChoiceCustom{name}`, `ToolChoiceMcp{server_label,name}`, `ToolChoiceShell`, `ToolChoiceApplyPatch`.
- **Streaming events:** granular deltas/done events for text/audio/transcripts, tool-call arguments, and lifecycle (`ResponseCreated`, `ResponseInProgress`, `ResponseCompleted`, `ResponseFailed`, etc.).
- **Include extra outputs (ResponseIncludable):** e.g., `file_search_call.results`, `web_search_call.action.sources`, `code_interpreter_call.outputs`, `message.output_text.logprobs`, `message.input_image.image_url`, `computer_call_output.output.image_url`, `reasoning.encrypted_content`.

## When to surface
Use when students ask how to structure multi-turn inputs/outputs, enforce JSON/structured responses, interpret streaming events/statuses, or control/require tool usage and included metadata (logprobs, search results, image URLs).