---
title: "Chain-of-Thought"
subject: "Large Language Models"
date: 2025-01-01
tags:
  - "subject/large-language-models"
  - "level/intermediate"
  - "level/advanced"
  - "educator/yannic-kilcher"
  - "educator/lilian-weng"
  - "resource/video"
  - "resource/blog"
  - "resource/deep-dive"
  - "resource/paper"
  - "resource/code"
educators:
  - "Yannic Kilcher"
  - "Lilian Weng"
levels:
  - "intermediate"
  - "advanced"
resources:
  - "video"
  - "blog"
  - "deep-dive"
  - "paper"
  - "code"
---

# Chain Of Thought

## Video (best)
- **Yannic Kilcher** — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models (Paper Explained)"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=_YXnMBQjGDo)
- Why: Kilcher systematically walks through the original Wei et al. paper, explaining *why* intermediate reasoning steps improve LLM performance — not just *that* they do. His paper-reading format is ideal for learners who want mechanistic understanding rather than surface-level intuition.
- Level: intermediate

> ⚠️ **Coverage note:** I have moderate confidence in this specific video ID. The video title and Kilcher's coverage of this paper are well-established, but the 11-character ID should be verified before publishing.

---

## Blog / Written explainer (best)
- **Lilian Weng** — "Prompt Engineering"
- **Link:** [https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/)
- Why: Weng dedicates a substantial, rigorous section to Chain-of-Thought (standard CoT, zero-shot CoT, self-consistency, Tree of Thoughts, and multimodal CoT) with clean diagrams and citations. It serves as a single-stop written reference covering all related concepts listed for this topic. Her writing bridges intuition and technical depth exceptionally well.
- Level: intermediate

---

## Deep dive
- **Author** — Lilian Weng (same post serves dual purpose) / alternatively the original survey
- **Link:** [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)
- Why: "A Survey of Chain of Thought Reasoning in Large Language Models" (Chu et al.) is the most comprehensive technical taxonomy of CoT variants — covering standard CoT, zero-shot CoT, self-consistency, least-to-most prompting, Tree of Thoughts, and multimodal CoT — with structured comparisons across benchmarks. Better as a deep-dive reference than the original paper for breadth. [NOT VERIFIED]
- Level: advanced

---

## Original paper
- **Wei et al. (Google Brain), 2022** — "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"
- **Link:** [https://arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)
- Why: This is the seminal paper that named and formalized the concept. It is unusually readable for an NLP paper — the examples are concrete, the ablations are clear, and the core insight (few-shot exemplars with reasoning steps unlock emergent reasoning) is presented accessibly. Essential primary source.
- Level: intermediate/advanced

> ⚠️ **Note:** There is a potential ID collision between the Wei et al. original paper and the survey paper above. Please verify both arxiv IDs independently before publishing. The Wei et al. paper is confirmed to exist on arxiv; the exact ID needs cross-checking.

---

## Code walkthrough
- **None identified** — No single canonical hands-on CoT implementation tutorial from a top educator (Karpathy, fast.ai, etc.) has been confirmed with a verifiable URL.

**Closest alternatives to verify:**
- The `langchain` documentation includes a CoT prompting walkthrough: https://python.langchain.com/docs/tutorials/ [NOT VERIFIED]
- Hugging Face's open-source cookbook has CoT examples but no single definitive notebook URL I can confirm with confidence.

---

## Coverage notes
- **Strong:** Written/blog coverage (Lilian Weng's post is excellent and confirmed). Original paper is well-documented and readable.
- **Weak:** Hands-on code walkthroughs — CoT is primarily a prompting technique, so "implementation" is lightweight, and no educator has produced a definitive standalone coding tutorial comparable to, say, Karpathy's nanoGPT.
- **Gap:** No confirmed high-quality video specifically on **multimodal CoT** (Zhang et al., 2023) exists from a preferred educator. Tree of Thoughts also lacks a dedicated video from the preferred educator list. General CoT video coverage exists but IDs need verification.

---

## Cross-validation
This topic appears in 3 courses: **intro-to-agentic-ai**, **intro-to-llms**, **intro-to-multimodal**

| Course | Relevant aspect |
|---|---|
| intro-to-llms | Core CoT concept, zero-shot CoT, self-consistency |
| intro-to-agentic-ai | Tree of Thoughts, ReAct-style reasoning chains |
| intro-to-multimodal | Multimodal CoT (Zhang et al., 2023) |

The Lilian Weng blog post covers all three course contexts in a single resource, making it the highest-leverage written resource across the curriculum.

---

---

## Additional Resources for Tutor Depth

> **9 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 Self-Consistency (SC) decoding for Chain-of-Thought
**Paper** · [source](https://arxiv.org/abs/2203.11171)

*Definition + decoding procedure: sample multiple CoT reasoning paths, marginalize paths, aggregate answers (majority/most consistent); benchmark gains vs greedy CoT.*

<details>
<summary>Key content</summary>

- **Core method (Fig. 1; Section “Self-consistency over diverse reasoning paths”):** Replace **greedy decoding** in CoT prompting with:
  1) **CoT prompt** the LM (few-shot CoT exemplars or zero-shot “let’s think step by step”).  
  2) **Sample** a *diverse set* of outputs from the decoder to obtain pairs \((r_i, a_i)\), where \(r_i\) = reasoning path tokens, \(a_i\) = final answer.  
  3) **Marginalize out reasoning paths** and choose the **most consistent answer** by aggregating over \(\{a_i\}\) (e.g., majority vote).
- **Latent-variable view:** Introduces latent \(r_i\) (reasoning) with \(r_i \rightarrow a_i\); reasoning is optional and used only to reach \(a_i\); aggregate over sampled paths to select answer.
- **Defaults / parameters (Section 3.2):**
  - Reported results averaged over **10 runs**.
  - Each run samples **40 outputs** independently (**40 reasoning paths**).
  - Diversity controlled via **sampling temperature** (robust across a range; temperature \(=0\) is deterministic/greedy).
- **Empirical gains (Abstract; Tables 2–3):** SC improves CoT accuracy by:
  - **GSM8K:** **+17.9%**
  - **SVAMP:** **+11.0%**
  - **AQuA:** **+12.2%**
  - **StrategyQA:** **+6.4%**
  - **ARC-challenge:** **+3.9%**
- **Design rationale:** Complex problems admit multiple reasoning paths to a unique answer; agreement across diverse paths increases confidence; SC avoids greedy local-optima/repetition and reduces single-sample stochasticity; **no fine-tuning, no verifier/reranker, no extra annotation** (“self-ensemble” on one model).

</details>

### 📄 Self-Consistency (Sample-and-Marginalize) for CoT Decoding
**Paper** · [source](http://webdocs.cs.ualberta.ca/~dale/papers/iclr23b.pdf)

*Self-consistency selection objective: marginalize/aggregate over sampled rationales → majority-vote (or weighted) answer selection; explicit decoding procedure + notation.*

<details>
<summary>Key content</summary>

- **Core procedure (Figure 1; Section 2):**
  1) Prompt LM with **chain-of-thought exemplars**.  
  2) **Sample** a diverse set of outputs (reasoning paths) from the decoder (not greedy).  
  3) **Marginalize out reasoning paths** and **aggregate final answers** to pick the most consistent answer.
- **Notation (Section 2):** sample \(m\) candidate outputs indexed by \(i=1,\dots,m\).  
  - Final answers \(a_i \in \mathcal{A}\) (fixed answer set).  
  - Latent reasoning path \(r_i\) (token sequence) leading to \(a_i\) (reasoning optional: \(r_i \rightarrow a_i\)).
- **Self-consistency objective (majority vote; Section 2):**
  \[
  \hat a=\arg\max_{a}\sum_{i=1}^{m}\mathbf{1}(a_i=a)
  \]
- **Optional probability-weighted aggregation (Eq. 1, length-normalized):**
  \[
  P(r_i,a_i\mid \text{prompt},q)=\exp\left(\frac{1}{K}\sum_{k=1}^{K}\log P(t_k\mid \text{prompt},q,t_{1:k-1})\right)
  \]
  where \(t_k\) is the \(k\)-th token in \((r_i,a_i)\), \(K\)=#tokens.
- **Empirical aggregation comparison (Table 1, PaLM-540B):** majority vote (“Unweighted sum”) strong: GSM8K **74.4**, MultiArith **99.3**, AQuA **48.3**, SVAMP **86.6**, CSQA **80.7**, ARC-c **88.7**.
- **Main gains vs greedy CoT (Tables 2–3):** PaLM-540B GSM8K **56.5→74.4 (+17.9)**; AQuA **35.8→48.3 (+12.5)**; SVAMP **79.0→86.6 (+7.6)**; StrategyQA **75.3→81.6 (+6.3)**; ARC-c **85.2→88.7 (+3.5)**.
- **Defaults (Section 3.1):** typically **40 sampled outputs** per run; sampling: UL2/LaMDA \(T=0.5, k=40\); PaLM \(T=0.7, k=40\); GPT-3 \(T=0.7\) (no top-k).

</details>

### 📄 Self-Consistency for Chain-of-Thought (ICLR 2023)
**Paper** · [source](http://arxiv.org/pdf/2203.11171v4.pdf)

*Benchmark tables/ablations comparing self-consistency vs greedy CoT across reasoning datasets + sampling settings + accuracy gains.*

<details>
<summary>Key content</summary>

- **Method (Self-Consistency; “sample-and-marginalize”, Sec. 2):**
  1) Prompt LM with **CoT exemplars**.  
  2) **Sample** \(m\) diverse outputs \((r_i, a_i)\) from decoder (reasoning path \(r_i\), final answer \(a_i \in \mathcal{A}\)).  
  3) **Aggregate** by marginalizing out \(r_i\): majority vote  
     \[
     a^*=\arg\max_{a\in\mathcal{A}}\sum_{i=1}^{m}\mathbf{1}(a_i=a)
     \]
- **Optional probability-weighted aggregation (Eq. 1, length-normalized):**
  \[
  P(r_i,a_i\mid \text{prompt},q)=\exp\Big(\frac{1}{K}\sum_{k=1}^{K}\log P(t_k\mid \text{prompt},q,t_{<k})\Big)
  \]
  where \(t_k\) are output tokens, \(K\)=#tokens in \((r_i,a_i)\). Finding: **majority vote ≈ normalized weighted sum**; unnormalized weighting performs worse.
- **Sampling defaults (Sec. 3.1):** typically **40 samples**, averaged over **10 runs**.  
  - UL2-20B & LaMDA-137B: temperature \(T=0.5\), top-\(k=40\)  
  - PaLM-540B: \(T=0.7\), top-\(k=40\)  
  - GPT-3: \(T=0.7\), **no top-\(k\)**
- **Key empirical gains (Tables 2–3; absolute accuracy):**
  - **PaLM-540B:** GSM8K **56.5→74.4 (+17.9)**; SVAMP **79.0→86.6 (+7.6)**; AQuA **35.8→48.3 (+12.5)**; ARC-c **85.2→88.7 (+3.5)**; StrategyQA **75.3→81.6 (+6.3)**.
  - **GPT-3 code-davinci-002:** GSM8K **60.1→78.0 (+17.9)**; SVAMP **75.8→86.8 (+11.0)**; AQuA **39.8→52.0 (+12.2)**; StrategyQA **73.4→79.8 (+6.4)**; ARC-c **83.6→87.5 (+3.9)**.
- **Ablations/Comparisons:** More sampled paths improves accuracy (Fig. 2). Self-consistency **beats sample-and-rank** (Fig. 3) and **beam search** (Table 6); beam search reduces diversity.

</details>

### 📄 Tree of Thoughts (ToT) = deliberate search over “thoughts”
**Paper** · [source](https://arxiv.org/abs/2305.10601)

*Algorithmic ToT procedure: generate thoughts → evaluate states (value/vote) → control search (BFS/DFS with pruning/backtracking)*

<details>
<summary>Key content</summary>

- **Problem framing (Sec. 3):** Solve by **search over a tree**.  
  - **State/node** = input + sequence of thoughts so far (a partial solution).  
  - **Thought** = coherent text unit (size chosen so it’s (i) generatable/diverse and (ii) evaluable).
- **ToT instantiation requires 4 choices (Sec. 3):**  
  1) **Thought decomposition** (e.g., Crosswords: a few words; Game of 24: one equation line; Creative writing: a plan paragraph).  
  2) **Thought generation** from state *s*: propose/sample multiple candidate next thoughts (i.i.d. sampling works well when thought space is rich).  
  3) **State evaluation heuristic** over frontier states *S*:  
     - **Value** each state: \(V(s)\) via LM prompt → scalar (1–10) or labels (e.g., sure/maybe/impossible).  
     - **Vote** across states: compare candidates and pick most promising (aggregate multiple votes for robustness).  
  4) **Search algorithm:**  
     - **BFS (Alg. 1):** keep top-*b* states per depth; prune early.  
     - **DFS (Alg. 2):** follow most promising; **prune** if value below threshold; **backtrack** to parent to explore alternatives.
- **Empirical results (Game of 24, Sec. 4.1; 100 hard games):**  
  - IO 7.3%; CoT 4.0%; CoT-SC (k=100) 9.0%  
  - ToT BFS **b=1: 45%**, **b=5: 74%**  
  - Best-of-100: IO 33%, CoT 49% (still < ToT b=5).
- **Defaults/params used in experiments:** GPT-4 chat completion, temperature **0.7**. Game of 24 ToT: **3 thought steps**; value labels sure/maybe/impossible; sample values multiple times per thought. Crosswords DFS: max **100** search steps; depth ≤ **10** (no overwriting filled letters).

</details>

### 📄 Tree of Thoughts (ToT) — deliberate search over “thoughts”
**Paper** · [source](https://arxiv.org/pdf/2305.10601.pdf)

*Empirical ToT gains (Game of 24, Creative Writing, Crosswords) + ToT search components (generate/evaluate/search; value/vote).*

<details>
<summary>Key content</summary>

- **Core formulation (Sec. 3):** Problem solving as **search over a tree**.  
  - **State** \(s\): input + sequence of thoughts so far (partial solution).  
  - **Thought**: coherent text unit (size chosen per task: equation line / plan paragraph / crossword word).
- **Thought generation (Sec. 3):** from state \(s\), generate candidates \(T=\{t_i\}\) via LM prompting (i.i.d. sampling or sequential proposals conditioned on \(s\)).
- **State evaluation heuristics (Sec. 3):**
  - **Value:** \(V(s)\) from a value prompt → scalar (e.g., 1–10) or labels (e.g., **sure/maybe/impossible**) mapped to numeric scores; can sample multiple times and aggregate.
  - **Vote:** given frontier \(S\), sample votes to pick most promising state: \( \text{Vote}(S)\rightarrow s^\*\).
- **Search algorithms (Sec. 3):**
  - **BFS (Alg. 1):** keep top \(b\) states per depth step (beam-like). Used when depth is small and early pruning helps (Game of 24, Creative Writing).
  - **DFS (Alg. 2):** expand best-looking state; **prune** if \(V(s)<v_{\text{th}}\); **backtrack** on prune or completion. Used for Crosswords; step budget **100**.
- **Empirical results — Game of 24 (Sec. 4.1, 100 hard games):**  
  IO 7.3%; CoT 4.0%; CoT-SC (k=100) 9.0%; **ToT BFS b=1: 45%**; **ToT BFS b=5: 74%**; IO+Refine (k=10) 27%; IO best-of-100 33%; CoT best-of-100 49%.  
  Setup: 3 ToT steps (3 intermediate equations); evaluator labels sure/maybe/impossible; temperature **0.7**.
- **Creative Writing (Sec. 4.2, 100 inputs):** GPT-4 coherency score (1–10, avg of 5 evals): **ToT 7.56** vs IO 6.19 vs CoT 6.93; humans prefer ToT over CoT **41/100** (CoT over ToT 21/100). ToT: depth 2 (plan→passage), **5 votes** each step, breadth limit \(b=1\).
- **Crosswords (Sec. 4.3):** ToT DFS improves letter/word/game metrics; solves **4/20** games; oracle “+best state” solves **7/20**; ablations show **-prune worse**, **-backtrack word success 25%**.

</details>

### 📖 Completions API — decoding controls & reproducibility
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/completions/create)

*Parameter-level semantics for multi-sample decoding + reproducibility controls (n, best_of, logprobs, temperature, top_p, max_tokens, stop, seed)*

<details>
<summary>Key content</summary>

- **Endpoint:** `POST /completions` creates a completion for provided `prompt` + parameters; returns a **Completion object** (or a sequence if streamed).
- **Model (`model`)**: string ID (examples listed: `"gpt-3.5-turbo-instruct"`, `"davinci-002"`, `"babbage-002"`).
- **Prompt (`prompt`) types:** string | array of strings | array of token IDs (numbers) | array of token arrays. If omitted, model generates as from start of new document; `<|endoftext|>` is training-time document separator.
- **Multi-sample decoding:**
  - `n` (min **1**, max **128**): number of completions to generate **per prompt**; increases token usage.
  - `best_of` (min **0**, max **20**): generates `best_of` candidates **server-side** and returns the **single best** by **highest log probability per token**. **Cannot be streamed.**
  - Constraint: when used together, **`best_of` must be > `n`**; `best_of` = candidates, `n` = returned.
- **Token/probability controls:**
  - `max_tokens` (min **0**): max generated tokens; **prompt_tokens + max_tokens ≤ model context length**.
  - `temperature` range **[0, 2]**; higher = more random, lower = more deterministic. Recommendation: change **temperature OR top_p**, not both.
  - `top_p` range **[0, 1]** nucleus sampling: consider tokens within top_p probability mass (e.g., **0.1 → top 10% mass**).
  - `logprobs` (min **0**, max **5**): return logprobs for **logprobs most likely tokens** plus the chosen token (up to **logprobs+1** entries).
- **Stopping:** `stop` string or array (up to **4** sequences); returned text **excludes** stop sequence. **Not supported with reasoning models `o3` and `o4-mini`.**
- **Reproducibility:** `seed` (int64): best-effort deterministic sampling with same seed+params; not guaranteed—monitor `system_fingerprint`.
- **Streaming:** `stream: true` sends SSE token events; terminates with `data: [DONE]`. `best_of` disables streaming.

</details>

### 📖 Messages endpoint (Chat Completions → Messages list)
**Reference Doc** · [source](https://platform.openai.com/docs/api-reference/messages)

*Current API surface location for “Messages” related to Chat Completions, within the broader OpenAI API reference navigation (useful for grounding discussions of message-structured inputs and where message objects live in the API).*

<details>
<summary>Key content</summary>

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

</details>

### 📖 OpenAI API “Advanced usage – parameter details” (404 index only)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/text-generation/parameter-details)

*Doc navigation pointers for sampling/reasoning parameter semantics (target page missing)*

<details>
<summary>Key content</summary>

- **HTTP result:** Target URL returns **404: Not Found** (“Page not found”).
- **Available on-page guidance:** Use **Docs search**; suggested queries shown:
  - `responses create`
  - `reasoning_effort`
  - `realtime`
  - `prompt caching`
- **Relevant doc locations surfaced by navigation (for parameter semantics elsewhere):**
  - **Core concepts → Text generation**: https://platform.openai.com/api/docs/guides/text
  - **Reasoning → Reasoning models**: https://platform.openai.com/api/docs/guides/reasoning
  - **Reasoning → Reasoning best practices**: https://platform.openai.com/api/docs/guides/reasoning-best-practices
  - **Run and scale → Streaming**: https://platform.openai.com/api/docs/guides/streaming-responses
  - **Context management → Prompt caching**: https://platform.openai.com/api/docs/guides/prompt-caching
  - **API Reference overview**: https://platform.openai.com/api/reference/overview
  - **Migration pointer:** “Responses API” guide: https://platform.openai.com/api/docs/guides/migrate-to-responses
- **No equations / defaults / parameter definitions** are present in the fetched content; it is purely a site navigation + error page.

</details>

### 📋 # Source: https://github.com/arpg/tree-of-thought-llm
**Source** ·

---

## Related Topics

- [[topics/prompting|Prompting]]
- [[topics/system-prompts|System Prompts]]
- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/reasoning-models|Reasoning Models]]
