---
title: "Prompting"
subject: "Large Language Models"
date: 2025-04-06
tags:
  - "subject/large-language-models"
  - "level/beginner"
  - "level/intermediate"
  - "level/advanced"
  - "educator/andrej-karpathy"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Andrej Karpathy"
  - "Lilian Weng"
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

# Prompting

## Video (best)
- **Andrej Karpathy** — "Intro to Large Language Models"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=zjkBMFhNj_g)
- Why: Karpathy's talk naturally covers how prompting works in the context of LLM inference, including zero-shot and few-shot patterns, temperature, and how the model responds to context. It's the most pedagogically grounded explanation of *why* prompting works, not just *how* to do it — rooted in the mechanics of next-token prediction. Already curated for this platform.
- Level: beginner/intermediate

> **Coverage note:** This video is a strong general LLM intro but does not deeply cover structured outputs, top-p sampling, or advanced prompting techniques. A more prompting-specific video would strengthen this topic.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Prompt Engineering"
- **Link:** [https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- Why: Weng's post is the gold standard written reference for prompting. It systematically covers zero-shot, few-shot, chain-of-thought, self-consistency, and structured output strategies with clear examples and citations. Her writing bridges intuition and rigor, making it suitable for learners who want depth without reading papers directly.
- Level: intermediate

[NOT VERIFIED] — URL structure is consistent with her blog conventions; confirm post slug is exact.

---

## Deep dive
- **DAIR.AI / Elvis Saravia** — "Prompt Engineering Guide"
- **Link:** [https://www.promptingguide.ai/](https://www.promptingguide.ai/)
- Why: The most comprehensive freely available reference covering the full prompting landscape: zero-shot, few-shot, chain-of-thought, ReAct, structured outputs, temperature/top-p parameters, and more. Actively maintained, well-organized, and widely used in both academic and industry settings. Serves as a living technical reference rather than a static article.
- Level: intermediate/advanced

---

## Original paper
- **Brown et al. (OpenAI), 2020** — "Language Models are Few-Shot Learners" (GPT-3 paper)
- **Link:** [https://arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
- Why: This is the seminal paper that introduced and formalized the concepts of zero-shot, one-shot, and few-shot prompting as distinct in-context learning paradigms. It is the foundational citation for virtually all prompting research. The results sections are readable without deep ML background, making it accessible to motivated learners.
- Level: intermediate/advanced

---

## Code walkthrough
- **OpenAI Cookbook** — "Techniques to improve reliability" (few-shot, structured outputs, temperature)
- **Link:** [https://cookbook.openai.com/articles/techniques_to_improve_reliability](https://cookbook.openai.com/articles/techniques_to_improve_reliability)
- Why: Hands-on, runnable examples demonstrating few-shot prompting, structured output formatting (JSON mode), and the practical effect of temperature and top-p on outputs. Uses the OpenAI API directly, which is the most common practical context learners will encounter. Bridges conceptual understanding to working code.
- Level: beginner/intermediate

[NOT VERIFIED] — OpenAI Cookbook URLs have shifted; confirm this slug resolves correctly.

---

## Coverage notes
- **Strong:** Zero-shot and few-shot prompting (well covered by GPT-3 paper + Weng blog + Karpathy video); in-context learning conceptual foundations; temperature intuition
- **Weak:** Top-p (nucleus) sampling mechanics — most resources mention it but few explain it deeply at a pedagogical level; structured outputs / JSON mode is underrepresented in video format
- **Gap:** No single excellent YouTube video exists that is *specifically* about prompting techniques end-to-end (zero-shot → few-shot → structured outputs → sampling parameters). Karpathy's video is the best available but is not a dedicated prompting tutorial. A video from a source like Serrano.Academy or a Stanford lecture specifically on prompt engineering would significantly strengthen this topic's video coverage.

---

## Cross-validation
This topic appears in 2 courses: **intro-to-agentic-ai**, **intro-to-llms**
- For `intro-to-llms`: the Karpathy video and GPT-3 paper are the natural anchors; Weng's blog provides the written complement.
- For `intro-to-agentic-ai`: the promptingguide.ai deep dive and OpenAI Cookbook are more actionable for learners building agents who need structured outputs and reliable prompting patterns.

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Demonstrations in ICL: labels often don’t matter
**Paper** · [source](https://arxiv.org/abs/2202.12837)

*Ablations on demonstration properties (label correctness, exemplar order, input distribution, random labels) isolating what drives ICL performance.*

<details>
<summary>Key content</summary>

- **ICL inference objective (classification/multi-choice)** (Section 3/4 framing): predict via  
  \[
  \hat y=\arg\max_{y\in C} P(y\mid x)
  \]
  **Zero-shot** (“No demonstrations”).  
  **k-shot** (“Demonstrations w/ gold labels”):  
  \[
  \hat y=\arg\max_{y\in C} P(y\mid x_1,y_1,\ldots,x_k,y_k,x)
  \]
  **Random-label ablation** (“Demonstrations w/ random labels”):  
  \[
  \hat y=\arg\max_{y\in C} P(y\mid x_1,\tilde y_1,\ldots,x_k,\tilde y_k,x)
  \]
  where \(C\) is the discrete label set; \((x_i,y_i)\) are demonstrations; \(\tilde y_i\) are randomly replaced labels.
- **Core empirical result (Section 4, Fig. 1/3):** Replacing gold labels in demonstrations with **random labels** causes only a **marginal** performance drop across **classification + multi-choice** tasks, consistent over **12 models including GPT-3**.
- **Meta-training effect (Section 4/6):** In **MetaICL**, the drop from randomizing demo labels is **0.1–0.9% absolute**, suggesting meta-trained ICL models **ignore input–label mapping** even more.
- **What actually drives gains (Section 5, Fig. 7–10):** demonstrations help mainly by specifying  
  1) **label space**, 2) **input-text distribution** (in-distribution examples matter), 3) **overall format** (input–label pairing).  
  Removing format (“labels only” or “inputs only” without pairing) is **close to or worse than** zero-shot.
- **Label-space ablation (Section 5.2):** For **direct** models, using labels from the **true label space** vs **random English-word labels** yields a **5–16% absolute** gap → label-space specification is a key contributor.

</details>

### 📄 Nucleus (top‑p) sampling definition & rationale
**Paper** · [source](https://arxiv.org/abs/1904.09751)

*Primary-source definition + algorithm for nucleus (top‑p) sampling; contrasts with top‑k/beam; explains “unreliable tail” and degeneration.*

<details>
<summary>Key content</summary>

- **LM factorization (Eq. 1):** For tokens \(x_{1:m+n}\),  
  \[
  P(x_{1:m+n})=\prod_{i=1}^{m+n} P(x_i \mid x_{1}\ldots x_{i-1})
  \]
  Generation proceeds token-by-token using a decoding strategy.
- **Nucleus / top‑p set (Section 3.1, Eq. 2):** Given next-token distribution \(P(x\mid x_{1:i-1})\) over vocabulary \(V\), define **top‑p vocabulary** \(V^{(p)}\subset V\) as the *smallest* set such that  
  \[
  \sum_{x\in V^{(p)}} P(x\mid x_{1:i-1}) \ge p
  \]
- **Renormalize + sample (Eq. 3):** Let \(p'=\sum_{x\in V^{(p)}} P(x\mid x_{1:i-1})\). Define truncated distribution  
  \[
  P'(x\mid x_{1:i-1})=
  \begin{cases}
  P(x\mid x_{1:i-1})/p' & x\in V^{(p)}\\
  0 & \text{otherwise}
  \end{cases}
  \]
  Then sample next token from \(P'\). **Candidate set size is dynamic** (expands/contracts with distribution shape).
- **Top‑k contrast (Section 3.2):** \(V^{(k)}\) is the size-\(k\) set maximizing \(\sum_{x\in V^{(k)}}P(x\mid \cdot)\); renormalize as Eq. 3. Unlike top‑p, the retained mass \(p'\) “can vary wildly” across steps.
- **Temperature (Eq. 4):** With logits \(u_l\) and temperature \(t\),  
  \[
  p(x=V_l\mid x_{1:i-1})=\frac{\exp(u_l/t)}{\sum_{l'}\exp(u_{l'}/t)}
  \]
  Lower \(t\in[0,1)\) skews toward high-probability tokens, reducing diversity.
- **Design rationale / empirical claims:** Beam/greedy (maximization) yields repetitive/generic “degeneration”; pure sampling can be incoherent due to an **“unreliable tail”** of many low-probability tokens. Authors report nucleus sampling best overall by human evaluation (HUSE) and matches human-like perplexity/diversity better than top‑k/beam.
- **Experimental defaults mentioned:** GPT‑2 Large (762M params); 5,000 conditional generations; max length 200 tokens; context = initial paragraph truncated to 1–40 tokens. HUSE: 200 generations × 20 annotations = 4,000 per decoding scheme; KNN with \(k=13\); smoothing for truncated methods by interpolating 0.1 mass of original distribution.

</details>

### 📄 Temperature Scaling for Neural Net Calibration
**Paper** · [source](https://proceedings.mlr.press/v70/guo17a/guo17a.pdf)

*Temperature scaling equation (logits ÷ T) + fitting T by NLL on validation set*

<details>
<summary>Key content</summary>

- **Perfect calibration definition (Eq. 1):**  
  \[
  \Pr(\hat Y = Y \mid \hat P = p)=p,\ \forall p\in[0,1]
  \]
  where \(\hat Y\) is predicted class, \(\hat P\) is predicted confidence.
- **Reliability diagram binning (Section 2):** Partition confidences into \(M\) bins \(I_m=((m-1)/M,m/M]\). For bin \(B_m\):  
  \[
  \text{acc}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\mathbf{1}(\hat y_i=y_i),\quad
  \text{conf}(B_m)=\frac{1}{|B_m|}\sum_{i\in B_m}\hat p_i
  \]
- **Expected Calibration Error (ECE) (Eq. 3):**  
  \[
  \text{ECE}=\sum_{m=1}^M \frac{|B_m|}{n}\,|\text{acc}(B_m)-\text{conf}(B_m)|
  \]
- **Negative Log Likelihood objective (Eq. 6):**  
  \[
  L=-\sum_{i=1}^n \log \hat\pi(y_i\mid x_i)
  \]
- **Temperature scaling (multiclass) (Eq. 9, Section 4.2):** Given logits vector \(z_i\), calibrated probs use softmax on scaled logits:  
  \[
  \sigma_{\text{SM}}(z_i/T)^{(k)}=\frac{e^{z_i^{(k)}/T}}{\sum_{j=1}^K e^{z_i^{(j)}/T}},\quad
  \hat q_i=\max_k \sigma_{\text{SM}}(z_i/T)^{(k)}
  \]
  \(T>0\) fit by **minimizing NLL on a held-out validation set**; model weights fixed. **Argmax unchanged** (accuracy unchanged).
- **Rationale:** Modern nets overfit NLL → overconfident; a **single scalar \(T\)** often corrects miscalibration (“intrinsically low dimensional”).
- **Empirical (Table 1, \(M=15\) bins):** CIFAR-100 ResNet-110 (SD) ECE **12.67% → 0.96%** with temperature scaling; CIFAR-10 ResNet-110 **4.6% → 0.54%**.
- **Implementation note:** Insert multiplicative constant \(1/T\) between logits and softmax; set \(T=1\) during training, tune after.

</details>

### 📊 GPT-3 Few-shot / One-shot / Zero-shot Evaluation Protocol & Benchmarks
**Benchmark** · [source](https://proceedings.neurips.cc/paper/2020/file/1457c0d6bfcb4967418bfb8ac142f64a-Paper.pdf)

*Definitions + evaluation protocol for 0S/1S/FS; benchmark tables showing scaling trends with model size and # in-context examples.*

<details>
<summary>Key content</summary>

- **Learning settings (Section 2 “Approach”):**
  - **Fine-tuning (FT):** update weights on supervised task data.
  - **Few-shot (FS):** provide **K demonstrations** (context→completion pairs) in the prompt; **no gradient updates**. Typical **K ≈ 10–100**, limited by **context window nctx = 2048** tokens.
  - **One-shot (1S):** FS with **K = 1**.
  - **Zero-shot (0S):** **task description/instruction only**, **K = 0**.
- **Few-shot evaluation procedure (Section 2.4):**
  - For each eval example, **randomly draw K examples from the task training set** as conditioning; delimiter **1–2 newlines** depending on task.
  - If no training set (e.g., **LAMBADA, StoryCloze**): draw conditioning examples from **dev**, evaluate on **test**.
  - Some tasks add a **natural-language prompt** and/or **answer formatting** changes.
  - **Free-form completion decoding:** **beam search** with **beam width = 4**, **length penalty α = 0.6**.
- **Key empirical results (Tables 3.1–3.5):**
  - **CoQA (F1):** 0S **81.5**, 1S **84.0**, FS **85.0**.
  - **TriviaQA (acc):** 0S **64.3**, 1S **68.0**, FS **71.2** (FS reported as SOTA in closed-book comparison).
  - **LAMBADA (acc):** 0S **76.2**, FS **86.4**.
  - **SuperGLUE (FS, 32 examples):** Avg **69.0**; notable: **COPA 52.0**, **ReCoRD F1 91.1**, **WiC 49.4** (near chance).
- **Design rationale (Intro/Fig 1.1):** performance improves with **model size** and **# in-context examples**; **gap between 0S/1S/FS often grows with capacity**, suggesting larger models are better at **in-context learning/meta-learning**.

</details>

### 📊 JSONSchemaBench metrics for structured-output constrained decoding
**Benchmark** · [source](https://arxiv.org/html/2501.10868v3)

*Compliance-rate + efficiency methodology for JSON-Schema–constrained decoding (incl. failure analysis; TTFT/TPOT)*

<details>
<summary>Key content</summary>

- **Constrained decoding definition (Intro):** masks invalid tokens at each step given constraints + prefix, forcing only valid tokens → schema-conpliant JSON.
- **Benchmark:** JSONSchemaBench = **9,558** real-world JSON Schemas (10 datasets; GitHub split by field count: trivial <10, easy 10–30, medium 30–100, hard 100–500, ultra >500). Experiments exclude GitHub-Trivial & GitHub-Ultra (too easy/hard).
- **Efficiency metrics (Sec. 4):**
  - **GCT** = Grammar Compilation Time (s)
  - **TTFT** = Time To First Token (s)
  - **TPOT** = Time Per Output Token after first (ms)
  - **Fairness:** compute efficiency on **intersection of covered instances across all engines** to avoid coverage bias.
  - **Setup:** Llama-3.1-8B-Instruct; single **A100 80GB**; batch=1. Outlines/Guidance/Llamacpp via llama.cpp; XGrammar via HF Transformers.
  - Example (GlaiveAI, llama.cpp backend): **LM-only TPOT 15.40ms** vs **Guidance 6.37ms** (TTFT 0.24s), **Llamacpp 29.98ms**, **Outlines GCT 3.48s, TTFT 3.65s, TPOT 30.33ms**.
- **Coverage notions (Sec. 5):**
  - **Declared coverage:** accepts schema w/o explicit reject/runtime error.
  - **Empirical coverage:** generated outputs validate against schema.
  - **True coverage:** constraints semantically equivalent to schema (ideal; not directly measurable).
  - **Compliance Rate (CR):** **CR = Empirical / Declared** (reliability conditional on accepting schema).
- **Coverage experiment defaults (Sec. 5.1):** Llama-3.2-1B-Instruct; prompt = instruction + **2-shot** examples; **greedy, temperature=0**, single sample; **40s compile timeout + 40s generation timeout**; validation via `jsonschema` (Draft 2020-12) with **format checks enabled**.
- **Empirical results (Sec. 5.2, selected):**
  - GitHub Easy: Guidance Declared **0.90**, Empirical **0.86**, **CR 0.96**; LM-only Empirical **0.65**.
  - GitHub Hard: Guidance Empirical **0.41** (CR **0.69**); LM-only **0.13**.
  - Closed-source (OpenAI/Gemini): often **low declared/empirical** but **CR ~1.00** (conservative feature subset).
- **Failure analysis via JSON Schema Test Suite (Sec. 5.3):**
  - Failure modes: **Over-constrained** (rejects valid instances) vs **Under-constrained** (allows invalid).
  - Category-level failures: Under-constrained counts—**Guidance 1** vs **XGrammar 38**; Compile errors—Outlines **42**, Llamacpp **37**, XGrammar **3**, Guidance **25**.
- **Quality (Sec. 6):** constrained decoding improved downstream accuracy up to ~**4%**; on reasoning tasks (Llama-3.1-8B): GSM8K **LM-only 80.1%** vs **Guidance 83.8%**.

</details>

### 📖 Chat Completions API — message schema, tools, streaming
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/chat)

*Canonical request/response objects for `/chat/completions`, message roles, tool-choice defaults, streaming options, and related JSON fields.*

<details>
<summary>Key content</summary>

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

</details>

### 📖 Schema-Constrained Decoding (Structured Outputs)
**Reference Doc** · [source](https://openai.com/index/introducing-structured-outputs-in-the-api/)

*Design rationale + mechanism for schema-constrained decoding vs JSON mode (guarantees/limits)*

<details>
<summary>Key content</summary>

- **JSON mode vs Structured Outputs**
  - JSON mode: improves validity of JSON but **does not guarantee conformance to a specific schema**.
  - **Structured Outputs:** designed to ensure outputs **exactly match developer-supplied JSON Schemas**.
- **How to enable (2 paths)**
  1. **Function calling:** set `strict: true` inside the tool/function definition → outputs match the supplied tool schema.
  2. **response_format:** set `response_format: { type: "json_schema", json_schema: { strict: true, schema: ... } }` → outputs match schema (supported on `gpt-4o-2024-08-06`, `gpt-4o-mini-2024-07-18`).
- **Reliability / empirical results**
  - On complex JSON schema-following evals: `gpt-4o-2024-08-06` + Structured Outputs scores **100%**; `gpt-4-0613` scores **<40%**.
  - Model training alone reached **93%** on benchmark; deterministic constrained decoding used to reach **100%** reliability.
- **Mechanism: constrained decoding (dynamic token masking)**
  - Convert JSON Schema → **context-free grammar (CFG)**.
  - During sampling, after **every token**, compute valid next tokens from CFG and **mask** invalid tokens (probability → **0**).
  - First request with a new schema incurs preprocessing latency; artifacts are cached for reuse.
- **Why CFG (vs FSM/regex)**
  - CFGs express broader languages; better for **nested/recursive** schemas (e.g., `$ref: "#"`) where FSMs struggle.
- **Operational limits**
  - Can still fail schema if **refusal**, **`max_tokens`/stop** truncation, or **parallel tool calls** (set `parallel_tool_calls: false`).
  - Structured Outputs ensures structure, **not correctness of values** (e.g., math step may be wrong).
  - First-schema latency: typical **<10s**, complex up to **~1 min**.
  - Refusals surfaced via `message.refusal` string; if no refusal and not interrupted (`finish_reason`), output matches schema.

</details>

### 📖 Structured Outputs & JSON Mode (OpenAI API)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/text-generation/json-mode)

*Concrete SDK pattern `client.responses.parse(...)` / `client.chat.completions.parse(...)` with typed schemas + documented constraints/behavior of Structured Outputs vs JSON mode.*

<details>
<summary>Key content</summary>

- **Structured Outputs (SO)**: guarantees **valid JSON + schema adherence** to supplied **JSON Schema** (`strict: true`), preventing missing required keys / invalid enums. Recommended over JSON mode when supported.
- **SDK parsing workflow (Python/Pydantic)**:
  - Chat Completions: `client.chat.completions.parse(..., response_format=MyModel)` → `completion.choices[0].message.parsed`
  - Responses API: `client.responses.parse(..., text_format=MyModel)` → `response.output_parsed`
- **When to use**:
  - **Function calling**: bridge model ↔ tools/functions/data.
  - **response_format / text.format**: structure the assistant’s *user-facing* response (e.g., tutoring UI sections).
- **Model support**:
  - SO via `response_format: {type:"json_schema", json_schema:{strict:true, schema:...}}` supported on **gpt-4o-mini**, **gpt-4o-mini-2024-07-18**, **gpt-4o-2024-08-06** and later snapshots.
  - **JSON mode**: `response_format: {type:"json_object"}` (Chat Completions) or `text.format: {type:"json_object"}` (Responses).
- **Refusals**: if safety refusal occurs, API includes a **refusal** field/content (programmatically detectable) rather than schema output.
- **Schema constraints (SO subset)**:
  - Root schema **must be an object** (not top-level `anyOf`).
  - **All fields must be required**; emulate optional via union with `null` (e.g., `"type": ["string","null"]`).
  - Objects must set **`additionalProperties: false`**.
  - Limits: **≤5000** total object properties, **≤10** nesting levels; total schema string length **≤120,000** chars; **≤1000** enum values overall.
  - Key ordering in output follows schema key order.
- **JSON mode gotcha**: must explicitly instruct output as **JSON**; API errors if “JSON” absent; otherwise model may emit endless whitespace.

</details>

### 📖 Structured Outputs (JSON Schema) — OpenAI Responses API
**Reference Doc** · [source](https://platform.openai.com/docs/guides/structured-outputs/)

*Exact request/response patterns + guarantees/limits for Structured Outputs (`client.responses.parse(...)`, schema subset, refusals, streaming, supported models)*

<details>
<summary>Key content</summary>

- **Guarantee (Structured Outputs):** Model output **always adheres to supplied JSON Schema** (type-safety; no missing required keys; no invalid enum values). Distinct from JSON mode which guarantees **valid JSON only**, not schema adherence.
- **Enable Structured Outputs (Responses API):**
  - SDK pattern (Python/Pydantic):  
    `response = client.responses.parse(model=..., input=[...], text_format=MyPydanticModel)` → parsed object at `response.output_parsed`.
  - REST/format equivalent: `text: { format: { type: "json_schema", strict: true, schema: ... } }`
- **Supported models (json_schema):** `gpt-4o-mini`, `gpt-4o-mini-2024-07-18`, `gpt-4o-2024-08-06` **and later**. Older models use **JSON mode**.
- **JSON mode enable:** `text: { format: { type: "json_object" } }`
  - Must explicitly instruct to output JSON; API errors if **“JSON”** not present in context. Risk: endless whitespace stream if not instructed.
- **Refusals:** If safety refusal occurs, response includes **`refusal`** content (programmatically detectable) rather than matching schema.
- **Streaming:** Use `client.responses.stream(..., text_format=Schema)`; handle events like `response.output_text.delta`, `response.refusal.delta`, `response.completed`. SDK recommended for parsing.
- **Schema subset + hard limits:**
  - Types: string, number, boolean, integer, object, array, enum, anyOf.
  - Root schema **must be object** (not anyOf). **All fields required**; emulate optional via union with `null` (e.g., `"type": ["string","null"]`).
  - Objects must set **`additionalProperties: false`**.
  - Limits: **≤5000** total object properties; **≤10** nesting levels; total schema string length **≤120,000** chars; **≤1000** enum values overall; per enum property string total **≤15,000** chars when >250 values.
  - Key ordering: output keys follow schema order.

</details>

---

## Related Topics

- [[topics/chain-of-thought|Chain-of-Thought]]
- [[topics/system-prompts|System Prompts]]
- [[topics/function-calling|Function Calling]]
- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/agentic-coding|Agentic Coding]]
