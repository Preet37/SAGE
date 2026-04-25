# System Prompts

## Video (best)
- **Andrej Karpathy** — "Let's build the GPT Tokenizer" — *Note: No single Karpathy video focuses specifically on system prompts and context window management.*
- youtube_id: zduSFxRajkE
- Why: No excellent dedicated video exists for system prompts, context window management, and message trimming as a unified topic. Karpathy's "Let's build ChatGPT" content touches on it but not as a primary focus.
- Level: N/A

> **Gap noted** — see Coverage Notes below.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Prompt Engineering"
- url: https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/
- Why: Weng's post covers system prompts in the context of how LLMs process structured inputs, including role-based prompting and context management. Her writing is technically precise, well-cited, and pedagogically structured — ideal for learners moving from "what is a prompt" to understanding system-level instructions and their interaction with conversation history.
- Level: intermediate

---

## Deep dive
- **Chip Huyen** — "Building LLM Applications for Production" (relevant section on context management)
- url: https://huyenchip.com/2023/04/11/llm-engineering.html
- Why: Huyen's production-focused writing addresses the practical realities of system prompts — how they consume context window tokens, strategies for message trimming, sliding window approaches, and summarization as a fallback. This is the most comprehensive practitioner-oriented treatment of the topic that bridges theory and deployment.
- Level: intermediate/advanced

---

## Original paper
- None identified
- Why: System prompts as a concept emerged from practice (OpenAI's ChatGPT API design, Anthropic's Claude API) rather than a single seminal paper. The closest foundational work would be InstructGPT (arxiv: https://arxiv.org/abs/2203.02155) which establishes the role-based instruction-following paradigm, but it does not specifically address system prompt mechanics, context window management, or message trimming as primary contributions. Citing it as "the" paper for this topic would be misleading.

---

## Code walkthrough
- **LangChain / OpenAI Cookbook** — "How to manage conversation history"
- url: https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb
- Why: The OpenAI Cookbook notebook directly demonstrates the `messages` array structure, system prompt placement, conversation history accumulation, and the practical problem of context overflow — making it the most direct hands-on implementation aligned with this topic's core concepts. Learners see exactly how system prompts interact with the sliding window of conversation history in real API calls.
- Level: beginner/intermediate

---

## Coverage notes
- **Strong:** Written/blog coverage of prompt engineering broadly (Weng, Huyen, OpenAI docs) is solid and pedagogically useful.
- **Weak:** Video content specifically focused on *system prompts + context window management + message trimming* as a unified topic is sparse. Most videos treat prompting generally without diving into the API-level mechanics of system messages.
- **Gap:** No high-quality YouTube explainer from a trusted educator (Karpathy, 3B1B, StatQuest, Serrano) specifically addresses system prompts, sliding window context management, and summarization strategies together. A purpose-built video for this platform would add significant value.
- **Gap:** No single seminal paper exists — this topic is defined by API design decisions and engineering practice rather than academic literature.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-agentic-ai**, **intro-to-llms**
- For `intro-to-llms`: emphasis should be on *what system prompts are* and how they fit into the message format / context window.
- For `intro-to-agentic-ai`: emphasis should shift to *managing long-running conversation history* — trimming, summarization, and sliding window strategies that keep agents functional across many turns.
- The Huyen deep dive is more appropriate for the agentic course; the Weng blog is more appropriate for the LLM intro course.

---

## Last Verified
2026-04-06