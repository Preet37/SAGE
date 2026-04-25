# Card: Responses API — conversation state, truncation, and token limits
**Source:** https://platform.openai.com/docs/api-reference/responses/list?lang=python  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete request/response fields & defaults for production conversation state handling (`previous_response_id`, `conversation`, `truncation`, `max_output_tokens`, `background`).

## Key Content
- **Conversation state (multi-turn)**
  - `previous_response_id: string|null` — “Use this to create multi-turn conversations.” **Cannot be used with** `conversation`.
  - `conversation: object|null` — “Input items and output items from this response are automatically added to this conversation.”
- **Context window handling (truncation)**
  - `truncation: "auto" | "disabled"` with **default = `"disabled"`**.
    - `"auto"`: if context exceeds model window, API **drops input items in the middle** to fit.
    - `"disabled"`: if response would exceed context window, request **fails with 400**.
- **Output length control**
  - `max_output_tokens: int|null` — upper bound on tokens generated **including visible output + reasoning tokens**.
- **Background execution**
  - `background: boolean|null` — whether to run the model response in the background.
- **Tool-call controls**
  - `parallel_tool_calls: boolean` — allow parallel tool calls.
  - `max_tool_calls: int|null` — max **total** built-in tool calls across the response; further attempts ignored.
  - `tool_choice: string|object`, `tools: array` — configure tool selection and availability.
- **Retrieving / auditing history**
  - `GET /v1/responses/{response_id}` retrieve a Response by id.
  - `GET /v1/responses/{response_id}/input_items` lists input items; pagination `limit` **1–100 (default 20)**, `order` default **`desc`**.
  - Conversations: `POST /v1/conversations` (add up to **20** initial items); `GET /v1/conversations/{id}/items` with `limit` **default 20**, `order` **desc**.
- **Usage accounting**
  - `usage`: `input_tokens`, `output_tokens`, `total_tokens`, plus `cached_tokens` and `reasoning_tokens`.

## When to surface
Use when students ask how to persist/trim conversation history, implement sliding windows/summarization safely, or choose between stateless (`previous_response_id`) vs stored (`conversation`) conversation state and token limits.