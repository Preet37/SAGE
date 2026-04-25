---
title: "System Prompts"
subject: "Large Language Models"
date: 2026-04-06
tags:
  - "subject/large-language-models"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/lilian-weng"
  - "educator/chip-huyen"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Lilian Weng"
  - "Chip Huyen"
levels:
  - "beginner"
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# System Prompts

## Video (best)
- **Andrej Karpathy** — "Let's build the GPT Tokenizer" — *Note: No single Karpathy video focuses specifically on system prompts and context window management.*
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zduSFxRajkE)
- Why: No excellent dedicated video exists for system prompts, context window management, and message trimming as a unified topic. Karpathy's "Let's build ChatGPT" content touches on it but not as a primary focus.
- Level: N/A

> **Gap noted** — see Coverage Notes below.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Prompt Engineering"
- **Link:** [https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- Why: Weng's post covers system prompts in the context of how LLMs process structured inputs, including role-based prompting and context management. Her writing is technically precise, well-cited, and pedagogically structured — ideal for learners moving from "what is a prompt" to understanding system-level instructions and their interaction with conversation history.
- Level: intermediate

---

## Deep dive
- **Chip Huyen** — "Building LLM Applications for Production" (relevant section on context management)
- **Link:** [https://huyenchip.com/2023/04/11/llm-engineering.html](https://huyenchip.com/2023/04/11/llm-engineering.html)
- Why: Huyen's production-focused writing addresses the practical realities of system prompts — how they consume context window tokens, strategies for message trimming, sliding window approaches, and summarization as a fallback. This is the most comprehensive practitioner-oriented treatment of the topic that bridges theory and deployment.
- Level: intermediate/advanced

---

## Original paper
- None identified
- Why: System prompts as a concept emerged from practice (OpenAI's ChatGPT API design, Anthropic's Claude API) rather than a single seminal paper. The closest foundational work would be InstructGPT (arxiv: https://arxiv.org/abs/2203.02155) which establishes the role-based instruction-following paradigm, but it does not specifically address system prompt mechanics, context window management, or message trimming as primary contributions. Citing it as "the" paper for this topic would be misleading.

---

## Code walkthrough
- **LangChain / OpenAI Cookbook** — "How to manage conversation history"
- **Link:** [https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb](https://github.com/openai/openai-cookbook/blob/main/examples/How_to_format_inputs_to_ChatGPT_models.ipynb)
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

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 CogCanvas (verbatim-grounded artifacts for long conversations)
**Paper** · [source](https://www.arxiv.org/pdf/2601.00821.pdf)

*Concrete architecture pattern for long-conversation management: extract *verbatim-grounded* artifacts (avoid summary drift), store in a temporal-aware graph, retrieve/inject adaptively; includes empirical comparisons vs truncation/summarization/RAG/GraphRAG.*

<details>
<summary>Key content</summary>

- **Problem & rationale (Intro):** Summarization is *lossy* and causes “recursive information decay” (iterative abstraction drops nuance). Example constraint: “use type hints **everywhere**” becomes “prefers type hints.” Controlled benchmark exact match: **Summarization 19.0% vs verbatim-grounded retrieval 93.0%**.
- **Artifact data structure (Section 3.1, Eq. 1):** `CanvasObject = (type, content, grounding_quote, source, embedding, turn_index, confidence)` where `type ∈ {Decision, Todo, KeyFact, Reminder, Insight}`; **grounding_quote is verbatim** for traceability/hallucination tolerance.
- **Extraction workflow (Section 3.2, Eq. 2):** Per turn `t`, call an extraction LLM using prior objects to avoid duplicates. **Two-pass “gleaning”**: 2nd pass targets pronouns/omitted subjects/implicit causality/temporal expressions; merge+dedupe.
- **Graph construction (Section 3.2, Eq. 3–4):** Embed each object with sentence encoder; create edges via cosine similarity plus **keyword overlap + temporal heuristics** (reference edges; causal edges for type pairs with similarity+temporal constraints; extra temporal-heuristic causal edges for recent KeyFacts/Reminders influencing later Decisions).
- **Adaptive injection (Section 3.3, Eq. 5):** Hybrid retrieval = semantic + lexical keyword score; **adaptive top‑k by query complexity** (multi-hop/temporal get larger k). Two-stage retrieval: coarse top‑20 → **BGE reranker** → greedy pack into token budget.
- **Empirical results:**
  - Controlled (Table 2): **CogCanvas Recall 97.5%, Exact 93.0%**; RAG(k=10) 93.5/89.5; GraphRAG 83.5/70.0; Summarization 19.0/14.0; Truncation (recent 5 turns) poor.
  - Multi-hop benchmark (Table 3): **CogCanvas Pass 81.0%, KW 90.2%, Causal 87.5%, Impact 92.6%**; RAG Pass 55.5%; GraphRAG 40.0%; Summarization 0.0%.
  - LoCoMo real-world (Table 4): **CogCanvas 32.4% overall vs RAG 24.6% (+7.8pp)**; **Temporal 32.7% vs 12.1% (+20.6pp)**; Multi-hop 41.7% vs 40.6 (+1.1pp); 1-hop 26.6 vs 24.6 (+2.0pp).
- **Ablation (Table 5):** Biggest contributor **reranking** (remove → **32.4%→20.9%, −11.5pp**). Remove graph expansion: 32.4→25.8 (−6.6pp). Remove gleaning: 32.4→30.7 (−1.7pp).
- **Defaults/hyperparams (Appendix A/B):** Extraction model **GPT‑4o‑mini**, embeddings **text-embedding-3-small**; retrieval **Top‑15**, max **2000 tokens**; temperatures **0.1 (extract)**, **0.0 (generate)**. Token cost per query (Appendix B): **CogCanvas ~1,250 tokens** vs RAG(top‑5) 1,500; Summ 2,000; GraphRAG 3,000; Full context 10,000.

</details>

### 📄 InstructGPT RLHF pipeline (SFT → RM → PPO/PPO-ptx)
**Paper** · [source](https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf)

*Step-by-step InstructGPT pipeline + datasets + evaluation numbers + key equations (RM loss, PPO-ptx objective)*

<details>
<summary>Key content</summary>

- **3-step training pipeline (Section 3.1, Fig. 2):**
  1) **Supervised fine-tuning (SFT):** collect labeler demonstrations on prompts; fine-tune GPT-3.  
  2) **Reward model (RM):** collect **rankings** of multiple model outputs per prompt; train RM to predict preferences.  
  3) **RLHF via PPO:** optimize SFT policy against RM reward with **KL penalty** to SFT; variant **PPO-ptx** mixes in pretraining gradients to reduce “alignment tax”.
- **Datasets (Section 3.2):** SFT ~**13k** training prompts; RM **33k**; PPO **31k** (API-only). Prompts deduped by long common prefix; cap **200 prompts/user**; splits by **user ID**; training prompts filtered for **PII**.
- **SFT hyperparams (Section 3.5):** **16 epochs**, cosine LR decay, residual dropout **0.2**; select checkpoint by **RM score** (not val loss).
- **RM loss (Eq. 1):**  
  \[
  \text{loss}(\theta)= -\frac{1}{\binom{K}{2}}\; \mathbb{E}_{(x,y_w,y_l)\sim D}\left[\log \sigma(r_\theta(x,y_w)-r_\theta(x,y_l))\right]
  \]  
  where \(x\)=prompt, \(y_w\)=preferred completion, \(y_l\)=less-preferred, \(r_\theta\)=scalar RM output, \(K\)=#responses ranked (**4–9**). Train all \(\binom{K}{2}\) comparisons per prompt as one batch element to reduce overfitting.
- **PPO-ptx objective (Eq. 2):**  
  \[
  \mathbb{E}_{(x,y)\sim D_{\pi^\text{RL}_\phi}}\!\left[r_\theta(x,y)-\beta \log\frac{\pi^\text{RL}_\phi(y|x)}{\pi^\text{SFT}(y|x)}\right] + \gamma \mathbb{E}_{x\sim D_\text{pretrain}}[\log \pi^\text{RL}_\phi(x)]
  \]  
  \(\beta\)=KL coef; \(\gamma\)=pretraining-mix coef (**PPO: \(\gamma=0\)**).
- **Key empirical results (Abstract/Section 4):**
  - **1.3B InstructGPT preferred over 175B GPT-3** (human eval).  
  - **175B InstructGPT preferred over 175B GPT-3: 85±3%**; over **few-shot prompted GPT-3: 71±4%**.  
  - Closed-domain hallucination rate: **21% (InstructGPT) vs 41% (GPT-3)**.  
  - Held-out labelers: similar preferences; RM cross-group accuracy **69.6±0.9%** vs **72.4±0.4%** in-group.

</details>

### 📄 Recursive Summarization for Long-Term Dialogue Memory (LLM-Rsum)
**Paper** · [source](https://arxiv.org/html/2308.15022v3)

*Empirical evaluation of recursive summarization as dialogue memory; ablations and downstream response quality under long-history constraints.*

<details>
<summary>Key content</summary>

- **Problem:** Long dialogue histories degrade consistency; even large context windows struggle to *use* past info effectively (“Lost in the middle” effect cited).
- **Core factorization (Section 3, Eq. 1):**  
  \(p(y \mid H, x) = p(M \mid H)\; p(y \mid M, x)\)  
  - \(H\): past sessions (multi-session dialogue history)  
  - \(x\): current session context at step \(t\)  
  - \(y\): response  
  - \(M\): available memory after a session
- **Memory iteration (Section 4.1, Eq. 2):**  
  \(M_s = \text{LLM}(P_m;\; M_{s-1}, S_s)\)  
  - \(S_s\): full dialogue of session \(s\)  
  - \(P_m\): memory-iteration prompt (task definition + step-by-step instructions + inputs: old memory + current session)  
  - Iterated per session; initial memory = `"none"`.
- **Response generation (Section 4.2, Eq. 3):**  
  \(y = \text{LLM}(P_g;\; M, x)\) using latest memory as primary reference; step-by-step prompting helps.
- **Main results (Session 5, Table 3; ChatGPT backbone):**
  - **MSC:** ChatGPT-Rsum F1 **20.48** vs ChatGPT **19.41**; BScore **86.89** vs **86.13**; human Consistency **1.45** vs **1.32**.
  - **Carecall:** ChatGPT-Rsum F1 **14.02** vs ChatGPT **13.69**; Consistency **1.70** vs **1.43**.
  - Retrieval can hurt: Carecall ChatGPT-BM25(k=3) F1 **12.64**; ChatGPT-DPR(k=3) F1 **12.21** (both < vanilla).
- **Ablation (Table 5, MSC):** W/O Memory F1 **18.94** (drop); **Gt. Memory** F1 **20.46** but BLEU-1/2 **21.50/12.40** < Ours **21.83/12.59** (gold memory “fragmented”; recursive memory more cohesive/easy-to-digest).
- **LLM-as-judge (GPT-4, Table 4, MSC):** Average score ChatGPT-Rsum **82.41** > MemoryBank **80.05** > MemoChat **76.21** > ChatGPT **75.32**.
- **Defaults/params:** temperature **0**; retriever top-k **3 or 5**; evaluate mainly sessions **4–5**; input lengths ≤ **4k** tokens in datasets.

</details>

### 📊 Agent Memory Taxonomy + Benchmarks + Metrics
**Benchmark** · [source](https://arxiv.org/html/2603.07670v1)

*Structured taxonomy of memory mechanisms + evaluation/metric stack + benchmark landscape (LoCoMo, MemBench, MemoryAgentBench, MemoryArena)*

<details>
<summary>Key content</summary>

- **Agent memory loop (Section 2; Eq. 1–2):** At step *t*, agent receives input \(x_t\) (user msg/sensor/tool output) and outputs action \(a_t\), consulting memory \(M_t\). Memory is updated via a **write–manage–read** loop: reads from \(M_t\); writes/manages (summarize, dedup, score priority, resolve contradictions, delete). Memory acts like a **belief state** in a POMDP.
- **Design objectives (Section 2.3):** Utility, Efficiency (token/latency/storage), Adaptivity, Faithfulness (stale/hallucinated recall can be worse than none), Governance (privacy/deletion/access control). Key tension: “store everything” boosts utility but harms efficiency/governance.
- **Taxonomy (Section 3):**
  - **Temporal scope:** working (context window), episodic (timestamped experiences), semantic (abstracted prefs/rules), procedural (skills/scripts; e.g., Voyager skill library).
  - **Substrate:** context text; vector stores (ANN/FAISS); structured DB/KG; executable repos; hybrids (e.g., MemGPT tiers).
  - **Control policy:** heuristic rules; prompted self-control (memory ops as tools); learned control (RL).
- **Mechanisms & pitfalls (Section 4):**
  - Context compression: sliding window, rolling/hierarchical summaries, task-conditioned compression; risk **summarization drift** + “lost in the middle.”
  - **MemGPT virtual context:** main context (“RAM”) + recall DB (“disk”) + archival vector store (“cold”); tool-like ops (e.g., `archival_memory_search`, `core_memory_append`).
  - **AgeMem RL pipeline:** 5 ops as tools—store/retrieve/update/summarize/discard; 3 stages: supervised warm-up → task-level RL → step-level GRPO.
- **Empirical comparisons (Sections 2.4, 5):**
  - Generative Agents: removing reflection degrades to repetitive behavior within **48 simulated hours**.
  - Voyager: removing skill library slows tech-tree milestones by **15.3**.
  - MemoryArena: long-context-only baseline drops completion from **>80% to ~45%** vs active memory agent.
  - Reflexion: **91% pass@1** HumanEval vs **80%** GPT-4 w/o reflection.
- **Benchmarks table (Section 5.3):**
  - LoCoMo (2024): multi-session ✓, multi-turn ✓, agentic –, forgetting –, multimodal ✓; up to **35 sessions**, **300+ turns**, **9k–16k tokens**.
  - MemBench (2025): multi-turn ✓; metrics: effectiveness/efficiency/#ops/capacity vs store growth.
  - MemoryAgentBench (2025): selective forgetting ✓; probes retrieval, test-time learning, long-range understanding, forgetting.
  - MemoryArena (2026): multi-session ✓, agentic tasks ✓; exposes recall→utility gap (LoCoMo “aces” can fall to **40–60%**).
- **Metric stack (Section 5.4):** (1) task effectiveness; (2) memory quality (precision/recall, contradiction rate, staleness, coverage); (3) efficiency (latency, prompt tokens, retrieval calls, storage growth); (4) governance (privacy leakage, deletion compliance, access violations).

</details>

### 📖 Responses API — message/items, formats, streaming, tool-choice
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/responses/list?lang=python)

*Definitions/defaults for Responses API objects: message/item formats, instruction hierarchy, output formats, streaming events, tool-choice, and includable extras.*

<details>
<summary>Key content</summary>

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

</details>

### 📖 Responses API — streaming + system instructions + truncation
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/responses-streaming/response/in_progress?lang=curl)

*Request/response fields that control system instructions, conversation carryover, and context-window truncation (plus streaming via SSE).*

<details>
<summary>Key content</summary>

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

</details>

### 📋 # Source: https://platform.openai.com/docs/api-reference/debugging-requests
**Source** · 

### 🔍 Prompt engineering page status (404)
**Explainer** · [source](https://platform.openai.com/docs/guides/prompt-engineering/strategy-write-clear-instructions)

*Link intended to provide “Write clear instructions” prompting heuristics, but currently resolves to a docs 404.*

<details>
<summary>Key content</summary>

- **Document availability:** The fetched page returns **HTTP 404: Not Found** (“Page not found”).
- **No extractable technical content:** The retrieved text contains **no prompting heuristics**, **no procedures**, **no equations**, **no empirical results**, and **no defaults/parameters** related to “Write clear instructions.”
- **Navigation context present (non-substantive):** The 404 page includes general docs navigation links (e.g., “Prompt guidance,” “Prompting,” “Prompt engineering,” “Citation formatting,” “Compaction,” “Token counting,” “Prompt caching”), but **does not provide** the referenced strategy content itself.

</details>

### 🔍 Prompt engineering — “Provide reference text” (link currently 404)
**Explainer** · [source](https://platform.openai.com/docs/guides/prompt-engineering/strategy-provide-reference-text)

*Procedure for grounding outputs in supplied text + instructing citation/quoting behavior*

<details>
<summary>Key content</summary>

- **Retrieval status:** The fetched page content is **“Page not found” (HTTP 404)**; no strategy/procedure text is present in the provided source excerpt.
- **Available actionable items in excerpt (navigation pointers only):**
  - Docs include a **“Prompt engineering”** guide hub: https://platform.openai.com/api/docs/guides/prompt-engineering
  - A dedicated **“Citation formatting”** guide is listed under Prompting: https://platform.openai.com/api/docs/guides/citation-formatting
  - Related context-management topics are listed (for grounding via managed context), including:
    - **Conversation state:** https://platform.openai.com/api/docs/guides/conversation-state  
    - **Compaction:** https://platform.openai.com/api/docs/guides/compaction  
    - **Counting tokens:** https://platform.openai.com/api/docs/guides/token-counting  
    - **Prompt caching:** https://platform.openai.com/api/docs/guides/prompt-caching  
  - Tooling for grounding via retrieval is listed:
    - **File search:** https://platform.openai.com/api/docs/guides/tools-file-search  
    - **Retrieval:** https://platform.openai.com/api/docs/guides/retrieval  
- **No equations, parameters, or step-by-step grounding workflow** are included in the excerpt (only site navigation and the 404 message).

</details>

---

## Related Topics

- [[topics/prompting|Prompting]]
- [[topics/function-calling|Function Calling]]
- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/agentic-coding|Agentic Coding]]
