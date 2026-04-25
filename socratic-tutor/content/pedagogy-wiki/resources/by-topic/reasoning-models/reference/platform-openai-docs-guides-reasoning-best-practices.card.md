# Card: Reasoning best practices (doc index only)
**Source:** https://platform.openai.com/docs/guides/reasoning/best-practices  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Entry point for OpenAI “Reasoning best practices” guidance; includes related navigation targets for controlling reasoning behavior (effort/latency/cost) and handling reasoning traces.

## Key Content
- The fetched page content is a **404 “Page not found”** response; no best-practice guidance, equations, empirical results, or parameter defaults are present in the retrieved text.
- The document shell exposes **adjacent/related doc endpoints** via navigation and search suggestions (useful as pointers during tutoring):
  - Reasoning section links:
    - **Reasoning models:** https://platform.openai.com/api/docs/guides/reasoning  
    - **Reasoning best practices:** https://platform.openai.com/api/docs/guides/reasoning-best-practices
  - Search suggestions shown on the page (as keywords students may ask about):
    - **responses create**, **reasoning_effort**, **realtime**, **prompt caching**
- The broader docs IA (information architecture) visible here indicates where operational controls likely live:
  - **Responses API** migration guide: https://platform.openai.com/api/docs/guides/migrate-to-responses
  - **Streaming responses:** https://platform.openai.com/api/docs/guides/streaming-responses
  - **Latency optimization** and **Cost optimization** sections (for managing reasoning latency/cost tradeoffs).

## When to surface
Use this card when a student asks for “Reasoning best practices” specifics and you need to redirect to the correct, currently valid docs pages (Reasoning models / reasoning-best-practices) or related parameters like `reasoning_effort` and Responses API usage.