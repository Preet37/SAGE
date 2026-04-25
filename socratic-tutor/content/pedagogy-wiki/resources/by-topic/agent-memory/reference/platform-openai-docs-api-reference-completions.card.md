# Card: Completions API — conversation + defaults
**Source:** https://platform.openai.com/docs/api-reference/completions  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact request fields/defaults (e.g., `background` default=false, `conversation` default=null) and how conversation items are prepended to `input_items`.

## Key Content
- **Endpoint purpose:** Create a text completion from a model; request supports attaching/continuing a **conversation state** via a `conversation` field.
- **Conversation field (stateful context):**
  - `conversation`: **default = `null`**.  
  - When provided, the API uses the referenced conversation’s stored items as prior context.
  - **Ordering rule:** conversation items are **prepended** to the request’s `input_items` (i.e., effective context = `conversation.items + input_items`). This matters for **context window** budgeting and “what the model sees first.”
- **Background execution:**
  - `background`: **default = `false`**.  
  - When `true`, the completion can run asynchronously (“background mode”), useful for long tasks without holding an interactive connection.
- **Context-management implication (design rationale):**
  - Prepending conversation history ensures continuity across turns while letting the caller supply new `input_items` each request.
  - Because the model has a finite **context window**, long conversations may require **message trimming/compaction/summarization** on the client side (sliding window) to keep the most relevant items in the effective input.
- **Practical procedure (workflow):**
  1. Start with `conversation=null` for a fresh interaction.
  2. Persist the returned conversation identifier (if used by your integration).
  3. On later turns, send `conversation=<id>` plus new `input_items`; remember the API will place prior items before your new items.

## When to surface
Use when students ask how to “remember” prior turns with the Completions API, what defaults apply (`background`, `conversation`), or why older messages affect context length and require trimming/summarization.