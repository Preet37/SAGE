# Card: Messages endpoint (Chat Completions → Messages list)
**Source:** https://platform.openai.com/docs/api-reference/messages  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Current API surface location for “Messages” related to Chat Completions, within the broader OpenAI API reference navigation (useful for grounding discussions of message-structured inputs and where message objects live in the API).

## Key Content
- **Where “Messages” fits in the API reference (navigation path):**
  - **Chat Completions → Chat Completions →** includes operations for completions and a **Messages** subresource.
  - The reference lists **“List chat completions (…/chat/completions/subresources/messages/methods/list)”** indicating a dedicated endpoint to **list messages associated with chat completions**.
- **Related modern API surfaces (for reasoning/tooling discussions):**
  - The docs emphasize the **Responses API** as the primary modern surface (see “Responses API” section in the same reference tree), including:
    - **Responses** methods: create/retrieve/delete/list input items/count input tokens/cancel/compact.
    - **Streaming events** for Responses.
  - **Tools & function calling** are documented as core concepts (linked from the same reference hub): “Function calling”, “Using tools”, “Structured output”, “Images and vision”, “Audio”.
- **Key parameter names surfaced in the reference search/navigation (useful keywords to cite precisely):**
  - `response_format`, `parallel_tool_calls`, `reasoning_effort` (shown as suggested search terms in the API docs UI).

## When to surface
Use this card when a student asks **where message objects/endpoints are documented** (especially “messages list” under Chat Completions) or when you need to **name exact modern API knobs** (e.g., `reasoning_effort`, `parallel_tool_calls`, `response_format`) while discussing structured/multimodal reasoning setups.