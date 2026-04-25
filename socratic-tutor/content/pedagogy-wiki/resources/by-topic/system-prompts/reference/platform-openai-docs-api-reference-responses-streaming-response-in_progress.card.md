# Card: Responses API — streaming + system instructions + truncation
**Source:** https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Request/response fields that control system instructions, conversation carryover, and context-window truncation (plus streaming via SSE).

## Key Content
- **System prompt injection (`instructions`)**
  - `instructions: string` = “A system (or developer) message inserted into the model’s context.”
  - **Carryover rule:** When using `previous_response_id`, **instructions from the previous response are not carried over** to the next response → enables swapping system/developer messages per turn.
- **Conversation state options (mutually exclusive)**
  - `previous_response_id: string` for multi-turn state; **cannot be used with** `conversation`.
  - `conversation: string | ResponseConversationParam`: items from the conversation are **prepended** to `input_items`; after completion, **input and output items are automatically added** to the conversation.
- **Context window / trimming behavior (`truncation`)**
  - `truncation: "auto" | "disabled"` (default **disabled**).
  - `"auto"`: if input exceeds context window, model **drops items from the beginning** of the conversation to fit.
  - `"disabled"`: if input would exceed context window, request **fails with 400**.
- **Streaming switch**
  - `stream: boolean`: if `true`, response is streamed via **server-sent events (SSE)**.
  - `stream_options: { include_obfuscation }` only when `stream: true`.
- **Token budgeting**
  - `max_output_tokens: number`: upper bound on generated tokens **including visible output + reasoning tokens**.
- **Concrete defaults/limits**
  - `temperature` range **0–2**; `top_p` range **0–1**; `top_logprobs` integer **0–20**.
  - `metadata`: up to **16** key-value pairs; key ≤ **64** chars, value ≤ **512** chars.
  - `safety_identifier`: string identifier, max **64** chars.

## When to surface
Use when students ask how system prompts/instructions persist across turns, how to manage/trim conversation history to fit the context window, or how to enable and reason about streaming responses and token limits.