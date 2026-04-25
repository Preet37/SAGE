# Card: OpenAI API Model Catalog (selection + limits)
**Source:** https://platform.openai.com/docs/models  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Model availability/capability matrix + documented limits (context/output), tool compatibility, and pricing pointers.

## Key Content
- **Default model choice guidance (Choosing a model):**
  - Start with **`gpt-5.4`** for **complex reasoning and coding**.
  - For **lower latency/cost**, choose **`gpt-5.4-mini`** or **`gpt-5.4-nano`**.
- **Common capability baseline (latest OpenAI models):**
  - Support **text + image input**, **text output**, **multilingual**, and **vision**.
  - Available via the **Responses API** and **Client SDKs**.
- **Frontier model rows (key empirical numbers):**
  - **`gpt-5.4`**
    - Pricing: **$2.50 / input MTok**, **$15 / output MTok**
    - **Context window:** **1M tokens**
    - **Max output:** **128K tokens**
    - Tools: **Functions, Web search, File search, Computer use**
    - Knowledge cutoff: **Aug 31, 2025**
    - Latency: **Fast**
  - **`gpt-5.4-mini`**
    - Pricing: **$0.75 / input MTok**, **$4.50 / output MTok**
    - **Context window:** **400K tokens**
    - **Max output:** **128K tokens**
    - Tools: **Functions, Web search, File search, Computer use**
    - Knowledge cutoff: **Aug 31, 2025**
    - Latency: **Faster**
  - **`gpt-5.4-nano`**
    - Pricing: **$0.20 / input MTok**, **$1.25 / output MTok**
    - **Context window:** **400K tokens**
    - **Max output:** **128K tokens**
    - Tools: **Functions, Web search, File search, MCP**
    - Knowledge cutoff: **Aug 31, 2025**
    - Latency: **Faster**
- **Specialized model categories listed:** **Image**, **Realtime (speech-to-speech)**, **Speech generation (TTS)**, **Transcription (STT)**.

## When to surface
Use this card when students ask which OpenAI model to pick (reasoning vs latency/cost), what **context/output token limits** apply, what **tools** a model supports, or where **video/audio/image** model families live in the catalog.