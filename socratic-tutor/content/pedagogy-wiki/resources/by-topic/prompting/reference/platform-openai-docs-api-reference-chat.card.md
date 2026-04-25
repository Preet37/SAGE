# Card: Chat Completions API — message schema, tools, streaming
**Source:** https://platform.openai.com/docs/api-reference/chat  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Canonical request/response objects for `/chat/completions`, message roles, tool-choice defaults, streaming options, and related JSON fields.

## Key Content
- **Endpoint & operations**
  - Create: `POST /chat/completions`
  - List: `GET /chat/completions`
  - Get: `GET /chat/completions/{completion_id}`
  - Update: `POST /chat/completions/{completion_id}`
  - Delete: `DELETE /chat/completions/{completion_id}`
  - Get stored messages: `GET /chat/completions/{completion_id}/messages`
- **Core response object**
  - `ChatCompletion = { id, choices, created, ... }` (response returned by model based on provided messages)
  - Streaming: `ChatCompletionChunk = { id, choices, created, ... }`
- **Message roles & precedence**
  - `ChatCompletionRole` includes `"developer"`, `"system"`, `"user"`, …
  - `ChatCompletionDeveloperMessageParam = { role, content, name }`: developer instructions the model should follow; **with o1 models and newer, developer messages replace previous system messages**.
  - `ChatCompletionSystemMessageParam = { role, content, name }`: same purpose, but developer messages preferred for o1+.
  - User message: `ChatCompletionUserMessageParam = { role, content, name }`
- **Multimodal content parts**
  - `ChatCompletionContentPartText = { type, text }`
  - `ChatCompletionContentPartImage = { type, image_url }`
  - `ChatCompletionContentPartInputAudio = { type, input_audio }`
  - Refusal part: `{ type, refusal }`
- **Audio output**
  - Output object: `ChatCompletionAudio = { id, data, expires_at, transcript }`
  - Request params: `ChatCompletionAudioParam = { format, voice }` (**required** when requesting modalities `["audio"]`)
  - Modalities: `ChatCompletionModality = "text" | "audio"`
- **Tools & tool choice (defaults matter)**
  - Tool types: `ChatCompletionTool = function tool | custom tool`
  - Force a function call: `ChatCompletionFunctionCallOption = { name }`
  - `tool_choice`: `"none" | "auto" | "required" | AllowedToolChoice | NamedToolChoice | NamedToolChoiceCustom`
    - `"none"` = model won’t call tools; generates a message
    - `"auto"` = model may choose message vs tool call(s)
    - `"required"` = model must call ≥1 tool
    - **Defaults:** `"none"` when **no tools** present; `"auto"` when **tools** are present
- **Streaming options**
  - `ChatCompletionStreamOptions = { include_obfuscation, include_usage }` (only when `stream: true`)

## When to surface
Use when students ask how to structure chat requests/responses (messages, roles, multimodal parts), how tool calling is controlled (especially `tool_choice` defaults), or how streaming/audio fields are represented in JSON.