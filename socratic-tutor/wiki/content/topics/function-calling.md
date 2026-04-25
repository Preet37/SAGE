---
title: "Function Calling"
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

# Function Calling

## Video (best)
- **Andrej Karpathy** — No dedicated function-calling video exists from the preferred educators.
- **Fallback: James Briggs (Pinecone)** — "OpenAI Function Calling - Full Beginner Walkthrough"
- **Watch:** [YouTube](https://www.youtube.com/watch?v=aqdWSYWC_LI)
- Why: James Briggs consistently produces clear, code-first walkthroughs of OpenAI tooling. This video covers the JSON schema definition, the tool-use loop, and parsing model responses — exactly the mechanics learners need before building agents.
- Level: beginner/intermediate

## Blog / Written explainer (best)
- **Lilian Weng** — "LLM Powered Autonomous Agents"
- **Link:** [https://lilianweng.github.io/posts/2023-06-23-agent/](https://lilianweng.github.io/posts/2023-06-23-agent/)
- Why: Weng's post is the canonical written reference for how tool use / function calling fits into the broader agentic architecture. It covers the tool-use loop, JSON schema design, and the reasoning cycle (plan → act → observe) with rigorous detail and clean diagrams. It contextualizes function calling rather than treating it as an isolated API trick.
- Level: intermediate/advanced

## Deep dive
- **OpenAI Official Documentation** — "Function Calling Guide"
- **Link:** [https://platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
- Why: The authoritative technical reference covering the full lifecycle: defining tool schemas, parallel tool calling, strict mode JSON schema enforcement, streaming with tool calls, and error handling patterns. Updated as the API evolves. No third-party resource matches its completeness or accuracy for implementation details.
- Level: intermediate

## Original paper
- **Patil et al. (2023)** — "Gorilla: Large Language Model Connected with Massive APIs"
- **Link:** [https://arxiv.org/abs/2305.15334](https://arxiv.org/abs/2305.15334)
- Why: This is the most readable seminal paper specifically on LLMs calling external APIs/tools. It introduces the retrieval-augmented approach to tool use, benchmarks hallucination in API calls, and directly motivates why structured function schemas matter. More focused on function calling mechanics than the broader ReAct or Toolformer papers.
- Level: advanced

## Code walkthrough
- **DeepLearning.AI** — "Functions, Tools and Agents with LangChain" (short course)
- **Link:** [https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/](https://www.deeplearning.ai/short-courses/functions-tools-agents-langchain/)
- Why: Hands-on Jupyter notebooks co-created with LangChain covering function/tool definition, the tool-use loop, parallel tool calling, and building a complete agent. Taught by Harrison Chase. Free to audit. Covers both raw OpenAI function calling and the abstraction layer — ideal for learners who need to see both levels.
- Level: beginner/intermediate

---

## Coverage notes
- **Strong:** JSON schema definition, the tool-use loop, OpenAI API mechanics, agentic context (Weng), hands-on code (DeepLearning.AI)
- **Weak:** Model Context Protocol (MCP) specifically — no single resource covers MCP + function calling together well yet; E2B sandboxed execution in the context of tool use; text-to-SQL as a function-calling pattern
- **Gap:** No high-quality video from the *preferred* educator list (3Blue1Brown, Karpathy, Kilcher, StatQuest, Serrano, Stanford/MIT) exists specifically for function calling as of early 2025. The topic is too API-specific for their typical mathematical/conceptual focus. The James Briggs recommendation above should be ****-ed for the exact video ID before publishing. Parallel tool calling and streaming tool calls also lack dedicated deep-dive video content.
- **Gap:** Error recovery patterns (retrying malformed tool calls, fallback strategies) are covered only incidentally in existing resources — no dedicated tutorial exists.

---

## Additional Resources for Tutor Depth

> **28 sources** — papers, official docs, working code, benchmarks, and deep explainers that give the AI tutor precision on this topic.

### 📄 ReAct (Reason+Act) Thought–Action–Observation Loop
**Paper** · [source](https://arxiv.org/abs/2210.03629)

*Core ReAct procedure (interleaved reasoning traces + actions) + benchmark tables/ablations (QA + interactive envs)*

<details>
<summary>Key content</summary>

- **Core formalism (Section 2):** Agent interacts over time steps. Observation \(o_t \in \mathcal{O}\), action \(a_t \in \mathcal{A}\), context  
  \[
  c_t = (o_1, a_1, \ldots, o_{t-1}, a_{t-1}, o_t), \quad \pi(a_t \mid c_t)
  \]
  ReAct **augments action space** with an unlimited **language space** \(\mathcal{L}\) for **reasoning traces (“Thought”)** that do **not** affect the environment; actions do and yield observations.
- **Procedure / workflow (prompting):**
  - Use a **frozen PaLM-540B** with **few-shot in-context trajectories** formatted as **Thought → Action → Observation** loops until terminal **Answer/Buy**.
  - **Reasoning-heavy tasks (HotpotQA/FEVER):** **dense alternation** of thought and action each step.
  - **Decision-making tasks (ALFWorld/WebShop):** **sparse thoughts** placed at key points; model decides asynchronous thought/action occurrence.
- **Design rationale:** Thoughts help **plan/decompose goals**, **track/update plans**, **extract key observation info**, **handle exceptions/loops**; actions enable **grounding via external info** (e.g., Wikipedia API), reducing hallucination/error propagation vs CoT.
- **Key empirical results (PaLM-540B prompting):**
  - **HotpotQA EM (6-shot):** Standard 28.7; CoT 29.4; Act-only 25.7; **ReAct 27.4**; **Best ReAct+CoT 35.1**.
  - **FEVER Acc (3-shot):** Standard 57.1; CoT 56.3; Act-only 58.9; **ReAct 60.9**; **Best ReAct+CoT 64.6**.
  - **ALFWorld success (2-shot):** Act-only 45; **ReAct 71**; IL baseline 37.
  - **WebShop success (1-shot):** Act-only 30.1; **ReAct 40**; IL baseline 29.1.
  - **Ablation (ALFWorld):** **ReAct vs IM-style (ReAct-IM): 71 vs 53** success.
- **Defaults/parameters:** CoT self-consistency baseline samples **21** trajectories with **temperature 0.7**; ReAct+CoT methods reach CoT-SC(21) using **~3–5 samples**.

</details>

### 📄 Reflexion (verbal RL via reflection + episodic memory)
**Paper** · [source](https://arxiv.org/abs/2305.15334)

*Explicit agent-loop alternative/extension to ReAct: reflection + memory + evaluator; concrete failure-recovery procedure with empirical gains*

<details>
<summary>Key content</summary>

- **Core idea (Section 3):** Reinforce an LLM agent **without weight updates** by converting task feedback into **verbal reflections** stored in **episodic (long-term) memory** used in later trials (“verbal reinforcement”).
- **Modular architecture (Section 3):**
  - **Actor** \(M_a\): generates text/actions (can be **CoT** or **ReAct**).
  - **Evaluator** \(M_e\): scores trajectory \(\tau_t\) with reward (exact match for reasoning; heuristics; or LLM-based evaluation).
  - **Self-Reflection** \(M_{sr}\): given **reward signal** (often binary success/fail), **trajectory**, and **memory** \(mem\), generates actionable reflection; append to \(mem\).
- **Memory design (Section 3):**
  - **Short-term memory:** current trajectory/history (within an episode).
  - **Long-term memory:** stored self-reflections (across episodes), used as “self-hints” to guide future actions.
- **Agent loop (“Reflexion process”, Section 3):** trial \(t\): Actor interacts → produces trajectory \(\tau_t\) → Evaluator scores → Self-Reflection writes reflection → update \(mem\) → retry until success (or stopping rule).
- **Concrete self-eval heuristic (AlfWorld):** trigger self-reflection if (i) same action + same response repeats **>3 cycles**, or (ii) actions in episode **>30** (inefficient planning).
- **Empirical results (from paper text):**
  - **HumanEval:** **91% pass@1** (Reflexion) vs **80%** (GPT-4 prior SOTA).
  - **AlfWorld:** **+22% absolute** improvement over strong baselines in **12** iterative learning steps.
  - **HotPotQA:** **+20%** improvement over baselines.
  - **HumanEval (learning gain):** up to **+11%** improvement reported.
  - **ReAct + Reflexion:** completes **130/134** AlfWorld tasks; ReAct-only improvement **halts between trials 6–7**.
  - **Ablation:** adding self-reflection yields **+8% absolute** boost over episodic-memory-only advantage.

</details>

### 📄 ToolGen metrics + workflow for multi-step tool use
**Paper** · [source](https://arxiv.org/html/2410.03439v1)

*ToolBench/StableToolBench metrics + quantitative results; unified tool retrieval+calling procedure*

<details>
<summary>Key content</summary>

- **Unified generative tool retrieval/calling (Section 3):** represent each API/tool as a **unique virtual token** (vocab expansion). Agent iterates: plan/thought → select tool → generate args → observe feedback until **finish token** or max turns.
- **Tool virtualization (Sec. 3.2, Appx B):** *Atomic indexing* maps each tool to **one token** like `<<tool name&&api name>>`; embedding init = average embedding of tool name.
- **Training objectives (Sec. 3.3–3.5):**
  - **Tool memorization loss (Eq. in Sec. 3.3):** fine-tune to output tool token given tool description. Variables: θ (LLM params), *d* (tool documentation/description).
  - **Retrieval training loss (Sec. 3.4):** fine-tune to output relevant tool tokens given user query. Variables: θ_mem (after memorization), *q* (query), *T(q)* (relevant tools).
  - **Agent-tuning workflow (Sec. 3.5):** generate **Thought + Action token**, fetch tool doc, then generate **Arguments** (decomposed vs ReAct “all-at-once”).
- **Constrained beam search (Sec. 3.6, Appx C):** build **disjunctive trie** over valid tool-token IDs; during action generation **mask logits** outside trie → reduces nonexistent-tool hallucinations; applied at retrieval + action steps.
- **Empirical retrieval results (Table 1, NDCG@k):**
  - **In-domain:** ToolGen vs ToolRetriever  
    - I1 NDCG@1: **89.17 vs 80.50**; I2 NDCG@1: **91.45 vs 71.18**; I3 NDCG@5: **90.16 vs 64.70**.
  - **Multi-domain:** ToolGen vs ToolRetriever  
    - I1 NDCG@1: **87.67 vs 72.31**; I3 NDCG@5: **84.79 vs 42.92**.
- **End-to-end agent eval (StableToolBench; Table 4):**
  - Metrics: **SoPR** (solvable pass rate), **SoWR** (win rate vs GPT-3.5 reference).
  - **With retriever:** ToolGen Avg **SoPR 53.28**, **SoWR 51.51** (ToolLlama Avg SoPR 51.55, SoWR 49.70).
  - **With ground-truth tools:** ToolGen Avg **SoPR 54.19**, **SoWR 49.70**.
- **Indexing rationale (Sec. 4.3, 5.3):** semantic indexing best for retrieval, but **atomic best end-to-end** (Table 5 atomic Avg SoPR **55.00** vs semantic **51.87**) due to lower hallucination.
- **Defaults/hyperparams (Sec. 4.1, 5.1):** base **Llama-3-8B**; vocab 128,256 → +46,985 = **175,241**; tool memorization **8 epochs**, retrieval **1 epoch**; context truncated **6,144**; ToolGen max **16 turns** (~5 actions + final), ToolLlama **6 turns**; trained with cosine LR schedule, **3% warmup**, Deepspeed ZeRO-3 on **4×A100**.

</details>

### 📊 API-Bank benchmark (tool-augmented LLM eval + results)
**Benchmark** · [source](https://aclanthology.org/anthology-files/pdf/emnlp/2023.emnlp-main.187.pdf)

*API-Bank benchmark design (Call / Retrieve+Call / Plan+Retrieve+Call), executable evaluation protocol, and quantitative success rates across models.*

<details>
<summary>Key content</summary>

- **Ability grading (Sec. 2.1):** derived from 2 axes: *(Few vs Many APIs in pool)* and *(Single vs Several API calls per turn)* → merged into 3 evaluated abilities:  
  1) **Call** (APIs known)  
  2) **Retrieve+Call** (APIs unknown; retrieve then call single API)  
  3) **Plan+Retrieve+Call** (APIs unknown; iterative plan/retrieve/call multiple APIs)
- **Evaluation system (Sec. 3):** **73 runnable APIs**; evaluation set **314 dialogues**, **753 API calls** (discarded **21.5%** of 400 annotated). Multi-turn allowed; multi-call supported.
- **API Search / ToolSearcher (Sec. 3.1):** required before every other API call in retrieval settings. Model condenses demand → **keywords**; system embeds keywords + API metadata, uses **cosine similarity**, returns top-matching API metadata.
- **Metrics (Sec. 3.3):**
  - **API-call correctness (Accuracy):** correct if predicted call yields **same DB query/modification and same returned results** as annotated call.
  - **Response quality:** **ROUGE-L** after tool execution.
- **Main results (Table 3, zero-shot unless noted):** API-call correctness (Total / Call / Retrieve+Call / Plan+Retrieve+Call)
  - **GPT-4:** **60.24% / 63.66% / 37.04% / 70.00%**
  - **GPT-3.5-turbo:** **47.16% / 59.40% / 38.52% / 22.00%**
  - **Lynx-7B (fine-tuned):** **39.58% / 49.87% / 30.37% / 20.00%**
  - **Alpaca-7B:** **15.19% / 24.06% / 5.19% / 0.00%**
  - **GPT-3 Davinci:** **0.57% / 0.50% / 1.48% / 0.00%**
- **Fine-tuning defaults (Sec. 7):** Lynx initialized from Alpaca/LLaMA-7B; **3 epochs**, **batch size 256**, **lr 2e-5**. Multi-agent data gen cost **$0.1/dialogue** vs **$8** manual (~**98%** savings).

</details>

### 📊 Berkeley Function Calling Leaderboard (BFCL) — ICML 2025 Poster
**Benchmark** · [source](https://icml.cc/virtual/2025/poster/46593)

*Benchmark setup (what BFCL evaluates + how it scores) for function-calling/tool-use, incl. single-turn and stateful agentic/dialog evaluation.*

<details>
<summary>Key content</summary>

- **Definition (task):** *Function calling / tool use* = an LLM invoking external functions/APIs/user-defined tools in response to user queries (tool selection + arguments).
- **Benchmark scope (what is evaluated):**
  - **Serial and parallel function calls** (single tool vs multiple tools; sequential vs parallel).
  - **Various programming languages** (tool/function interfaces span multiple languages).
  - **Stateful multi-step “agentic” setting**: evaluates **abstention** (deciding not to call a tool) and **reasoning with memory/dynamic decision-making** over multiple steps.
- **Scoring / evaluation method (procedure):**
  - Uses a **novel Abstract Syntax Tree (AST) evaluation method** to judge whether a function call is valid/correct **by structure**, enabling scaling to **thousands of functions** without executing every tool “for real.”
- **Dataset construction (procedure):**
  - Built from a combination of **expert-curated** and **user-contributed** functions and associated prompts.
- **Design rationale (why these choices):**
  - Addresses two benchmark gaps: (1) difficulty of evaluating whether a function call is valid, and (2) difficulty acquiring **diverse, real-world functions**.
  - AST-based checking is chosen to make evaluation **reliable and scalable**.
- **Empirical takeaway (reported qualitatively in abstract):**
  - **State-of-the-art LLMs excel at single-turn calls**, but **memory, dynamic decision-making, and long-horizon reasoning** remain open challenges in multi-step settings.
- **Access point:** Live leaderboard referenced at **gorilla.cs.berkeley.edu/leaderboard.html**.

</details>

### 📊 FunctionChat-Bench (tool-use dialog eval + error taxonomy)
**Benchmark** · [source](https://arxiv.org/html/2411.14054v1)

*Evaluation methodology + output-type taxonomy for tool-use dialogs (single-call vs dialog) + quantitative results across models*

<details>
<summary>Key content</summary>

- **Output-type taxonomy (Sec. 2.1):** 4 model output types in tool-use dialogs  
  1) **Tool Call** (function name + JSON arguments)  
  2) **Answer Completion** (convey tool result to user, preserve semantics)  
  3) **Slot Question** (ask for missing required params)  
  4) **Relevance Detection** (general chat or out-of-scope request; reject/handle without tools)
- **Dataset design (Sec. 3):**
  - **Singlecall:** 500 items; must directly produce Tool Call; **25 functions × 4 queries × 5 tool-list settings**. Tool-list settings: length **1/4/8** with similarity **random vs close**; composition proportions: **0.20 each** for {1.exact, 4.random, 4.close, 8.random, 8.close}. Param types: **integer, number, boolean, string**.
  - **Dialog:** **45 dialogs**, each **3–8 turns** (median **4**, avg **4.44**); **200** evaluated model turns: Tool Call **70**, Answer Completion **71**, Slot Question **36**, Relevance Detection **23**.
- **Evaluation workflow (Sec. 4–5):** Generate model outputs → **LLM-as-judge** (gpt-4-0125-preview) pass/fail per turn using type-specific rubrics + ground truth (+ “acceptable arguments” for Tool Call) → human review adjusts judge errors (App. C).
- **Key empirical results (Sec. 5, Tables 3–4):**
  - **Singlecall AVG (%):** gpt-3.5-turbo **91.4**, gpt-4-turbo **89.6**, gpt-4o **87.6**, solar-1-mini-chat **83.6**, gemini-1.0-pro **64.4**, gemini-1.5-pro **61.2**, functionary-medium **57.0**, gemini-1.5-flash **53.0**.
  - **Dialog micro-AVG:** gpt-4-turbo **0.96**, gpt-4o **0.94**, gpt-3.5-turbo **0.84**, gemini-1.5-pro **0.82**, gemini-1.5-flash **0.81**, gemini-1.0-pro **0.73**, functionary-medium **0.73**, solar **0.53**. Solar especially low: Slot Question **0.08**, Relevance **0.13**.
- **Error taxonomy (Sec. 6.2):**
  - Tool Call: missing call, wrong/unknown function, redundant slot-asking, invented/omitted args, type/format errors (e.g., ints as floats/strings; positive→negative), Korean numeral misunderstandings.
  - Answer Completion: unrelated output; **altering tool results** (notably Gemini).
  - Slot Question: hallucinate required params and call tool; ask for already-given info.
  - Relevance: over-tooling irrelevant chat; fabricate unsupported tools/features.

</details>

### 📊 Live API Bench (NL2SQL → Invocable Tool-Calling APIs)
**Benchmark** · [source](https://arxiv.org/pdf/2506.11266.pdf)

*Pipeline converting BIRD-SQL NL2SQL into executable API sequences (SLOT/SEL/REST) + results tables for LLMs and ReAct agents*

<details>
<summary>Key content</summary>

- **Benchmark construction (Section 3):** Transform BIRD-SQL dev set (11 DBs; avg **7 tables**, **73 columns**, **358K rows**/DB) into **three NL2API datasets** with (i) OpenAPI specs, (ii) live implementations, (iii) NL questions + **ground-truth API sequences**, (iv) databases. Keep only instances where API sequence output **matches SQL output**.
- **Three API formulations (Intro, §3):**
  - **SLOT:** 7 generic Python tools: `aggregate_data, filter_data, group_data_by, retrieve_data, select_unique_values, sort_data, transform_data`. JOINs handled in an **initialization step** producing one joined table (models don’t do JOINs). Tools (except `retrieve_data`) write intermediate results to **CSV files** and return file paths; sequences can be **up to 8 calls**.
  - **SEL:** Expand categorical args into separate functions (e.g., `filter_data(condition=equal_to)` → `select_data_equal_to`), plus **column-specific “get” functions**; toolset varies per instance.
  - **REST:** **One GET endpoint per query** (single-call tasks). Generated via 4-stage agentic pipeline: **(i)** code-gen agent (FastAPI), **(ii)** de-dup agent, **(iii)** execution module, **(iv)** verifier/filter agent (discard mismatches).
- **Dataset scale table (§3):**
  - SLOT-BIRD: **665 queries**, **7 tools**, **2.7 calls/query**, **3.29 slots/call**
  - SEL-BIRD: **651 queries**, **1256 tools**, **2.9 calls/query**, **0.05 slots/call**
  - REST-BIRD: **1257 queries**, **1250 tools**, **1 call/query**, **1.38 slots/call**
- **Metrics (§4.1.1):** (i) **position-aware intent** P/R/F1 vs ground-truth sequence; (ii) **slot** P/R/F1 conditional on correct intent; (iii) **Completion Rate** = fraction producing **ground-truth final answer**.
- **Empirical results (Table §4.1.1): completion rates (LLMs):**
  - SLOT: best shown **DeepSeek-V3 0.07**, **Qwen2.5-72B 0.06**, GPT4o **0.03**
  - SEL: best shown **Qwen2.5-72B 0.16**, DeepSeek-V3/GPT4o **0.09**
  - REST: best shown **Qwen2.5-72B 0.47**, GPT4o **0.38**, Llama-3.3-70B **0.42**
- **ReAct agent gains (Table §4.3):** GPT4o completion improves to **0.15 (SLOT)**, **0.12 (SEL)**, **0.50 (REST)** with fixed TAO-loop budget; agents face **stuck/loop** issues mainly on SLOT/SEL.
- **Design rationale:** NL2SQL provides diverse real DBs + executable semantics; converting SQL→API sequences yields **deterministic verified answers** and stresses **sequencing, parameter generation, response parsing, error handling**.

</details>

### 📊 ReAct (Reason+Act) Pattern — v3 Empirical Results & Workflow
**Benchmark** · [source](https://arxiv.org/abs/2210.03629v3)

*Updated experimental details/tables (v3 numbers for reproducibility)*

<details>
<summary>Key content</summary>

- **Core setup (agent context):** At time step *t*, agent receives observation \(o_t \in \mathcal{O}\) and takes action \(a_t \in \mathcal{A}\) via policy \(\pi(a_t \mid c_t)\), where  
  \(c_t = (o_1, a_1, \ldots, o_{t-1}, a_{t-1}, o_t)\). (Section 2)
- **ReAct procedure (prompting):** Prompt a frozen LLM (notably **PaLM-540B**) with few-shot **human trajectories** containing interleaved **Thought (reasoning trace)** and **Act (domain action)** plus **Obs (environment feedback)**.  
  - **Reasoning-heavy tasks (HotpotQA/FEVER):** dense alternation of Thought→Act→Obs steps.  
  - **Decision-making tasks (ALFWorld/WebShop):** **sparse thoughts** at key points; model decides asynchronous thought/action placement. (Model Overview / Section 2)
- **Key empirical results (PaLM-540B prompting):**
  - **HotpotQA (Exact Match, 6-shot):** Standard 28.7; CoT (reason-only) 29.4; Act-only 25.7; ReAct 27.4; **Best ReAct+CoT method 35.1**.  
  - **FEVER (Accuracy, 3-shot):** Standard 57.1; CoT 56.3; Act-only 58.9; ReAct 60.9; **Best ReAct+CoT method 64.6**.  
  - **ALFWorld (2-shot success %):** Act-only 45; **ReAct 71** (vs imitation learning baseline 37).  
  - **WebShop (1-shot success %):** Act-only 30.1; **ReAct 40** (vs imitation learning baseline 29.1). (Tables in main text)
- **Defaults/parameters:** CoT self-consistency baseline samples **21** trajectories, decoding **temperature 0.7**. (Section 3)
- **Fine-tuning pipeline:** Use **3,000 successful trajectories** generated by prompted PaLM-540B to fine-tune smaller PaLM models (e.g., **PaLM-8B/62B**); finetuned ReAct becomes strongest among Standard/CoT/Act/ReAct on HotpotQA scaling plot. (Section 3)

</details>

### 📊 ReAct Agent Benchmarking (LangChain Email Assistant)
**Benchmark** · [source](https://blog.langchain.com/react-agent-benchmarking/)

*Methodology + results on how adding domains/tools/context affects single ReAct agent performance (tool trajectories + rubric-judged outputs)*

<details>
<summary>Key content</summary>

- **Core question:** When does a *single* ReAct agent become overloaded as domains (instructions+tools) are added, causing performance drop?
- **Definitions:**  
  - *Domain* = conceptual responsibility bundle = **instructions + tools** (e.g., Calendar Scheduling, Customer Support).  
  - *Trajectory* = ordered sequence of tool calls.
- **Evaluation metric (Eq. 1: Pass rate):**  
  \[
  \text{PassRate}=\frac{\#\text{passed runs}}{90}
  \]
  where **90 runs** = 30 tasks × 3 stochastic repeats. Scores reported as “passing tests / 90”.
- **Pass condition:** task **passes iff** (1) tool-calling trajectory matches expected (correct tools + order; “nothing more, nothing less”) **and** (2) final email (via `send_email`) satisfies an **LLM-as-judge rubric** (boolean checks like `valid_email`, `more_deployments`).
- **Task sets / defaults:**  
  - Calendar Scheduling: 30 tasks; tools `get_cal`, `schedule_cal` (+ `send_email`); avg expected trajectory **1.4** tool calls.  
  - Customer Support: 30 tasks; **7 tools** (`get_org_info`, `get_customer_info`, `set_seats`, `set_deployments`, `apply_grant`, `get_billing_id`, `get_customer_invoices` + `send_email`); avg expected trajectory **2.7** tool calls.
- **Experimental procedure:** control agents have only their domain; then **append** additional generated domains’ instructions to the **system prompt** and **bind** their tools; same instructions/tool descriptions across models (not optimized per model). Stop testing a model when pass rate **<10%**.
- **Models benchmarked:** claude-3.5-sonnet, gpt-4o, o1, o3-mini, llama-3.3-70B.
- **Key results (1-domain controls):**
  - Calendar Scheduling: **o1 71%**, **o3-mini 68%** best; **gpt-4o** and **llama-3.3-70B** worst; llama-3.3-70B **0%** (failed to call `send_email` even with only scheduling domain).
  - Customer Support: **claude-3.5-sonnet 83%**, **o3-mini 83%**, **o1 77%**; llama-3.3-70B **21%**.
- **Scaling domains/context:** more domains/tools → worse instruction recall (“Lost in the Middle” expectation). Examples: Calendar Scheduling **gpt-4o drops to 2% at 7 domains**; **o3-mini drops sharply** with irrelevant domains; **o1 more stable**; claude-3.5-sonnet initially lower on scheduling but **more stable** as domains increase.
- **Trajectory-length effect:** longer trajectories degrade faster. For Customer Support, grouped as **<3 vs ≥3** tool calls; sample sizes **17 tasks (51 runs)** short vs **13 tasks (39 runs)** long; all top models show steeper decline for **≥3** when moving from 1 domain → 7 domains.
- **Overall conclusions:** (1) more context + more tools degrade performance, (2) longer trajectories degrade more quickly, (3) **o1/o3-mini/claude-3.5-sonnet** outperform **gpt-4o/llama-3.3-70B**, (4) **o3-mini** matches top models at small context but drops more as context grows.

</details>

### 📊 ReSpAct vs ReAct — Empirical gains from “Speak” in the thought–action loop
**Benchmark** · [source](https://arxiv.org/html/2411.00927v1)

*Benchmark results + ablations showing benefits of adding dialogue (“Speak”) to ReAct-style reasoning/acting agents (AlfWorld, WebShop, MultiWOZ).*

<details>
<summary>Key content</summary>

- **Agent formalism (Section 3):**
  - Environment loop: at time *t*, agent receives observation \(o_t \in \mathcal{O}\), chooses action \(a_t \in \mathcal{A}\) via policy \(\pi\).
  - **Context** \(c_t \in \mathcal{C}\) includes current observation + history: \(c_t = (o_t, a_{<t}, o_{<t})\).
  - ReSpAct expands language-space actions into **dialogue actions** \(a_t^{dlg}\): agent emits an utterance; **user response is appended to observations**, updating \(c_t\) for subsequent thoughts/actions.
- **Core procedure (Section 4):**
  - Frozen GPT models (not finetuned), few-shot prompting with **interleaved**: thoughts (“think”), environment actions, **speak actions**, and user responses.
  - **AlfWorld eval:** 134 unseen games; **6 prompt permutations** per task type (choose 2 of 3 annotated trajectories → 6 prompts). ReAct uses same trajectories **with speak removed**.
  - **User simulator** used for scalable evaluation; user types: Helpful Knowledgeable / Helpful Perturbed / Unhelpful (Appendix A.1; Table 4).
- **Key empirical results:**
  - **AlfWorld success (Table 1):** GPT-4o **ReAct best-of-6 80.6%** vs **ReSpAct best-of-6 87.3%**; averages **79.4%** vs **85.3%**.
  - **User quality ablation (Table 4, “All”):** Helpful Knowledgeable **85.3%**, Helpful Perturbed **52.9%**, Unhelpful **32.09%**, Human Expert **88.8%**.
  - **Inner Monologue ablation (Table 5):** **ReSpAct best-of-6 87.3%** vs **ReSpAct-IM 48.5%** (ReAct-IM 53.0%).
  - **WebShop (Table 3):** ReAct score **20.1**, SR **8%**; ReSpAct(User-Sim) score **32.7**, SR **12%**; ReSpAct(Human) score **85.8**, SR **50%**.
  - **MultiWOZ (Table 2):** GPT-4o-mini ReAct turns **5.1**, Inform **66.7**, Success **48.8** vs ReSpAct turns **6.5**, Inform **72.2**, Success **51.8**.
- **Design rationale (Intro/Section 3/5):**
  - Dialogue reduces **assumption-making** and mitigates **error propagation** in long reasoning traces; but too much interaction (IM-style) becomes “chatty” and hurts completion.

</details>

### 📖 CompiledStateGraph runtime contract (LangGraph JS)
**Reference Doc** · [source](https://reference.langchain.com/javascript/classes/_langchain_langgraph.index.CompiledStateGraph.html)

*Compiled graph runtime contract in JS: invoke/stream signatures, config handling, and what the compiled artifact exposes*

<details>
<summary>Key content</summary>

- **What it is:** `CompiledStateGraph` is the **final artifact** produced by `StateGraph.compile()` (should not be instantiated directly). Version **v1.2.8**, **since v0.3**.
- **Primary execution APIs**
  - `invoke(input, config?) → Promise<ExtractStateType<O, O>>`: run graph once with a single input + optional per-call config override.
  - `stream(input, config?) → Promise<IterableReadableStream<StreamOutputMap<...>>>`: real-time execution stream.
  - `streamEvents() → IterableReadableStream<StreamEvent>`: stream event objects.
- **Streaming defaults & modes**
  - `streamMode: StreamMode[]` default = `["values"]`.
  - Supported modes (doc list):  
    - `"values"` full state after each step  
    - `"updates"` state deltas after each step  
    - `"messages"` messages emitted inside nodes  
    - `"custom"` custom node events  
    - `"tools"` tool-call lifecycle events (`on_tool_start`, `on_tool_event`, `on_tool_end`, `on_tool_error`)  
    - `"debug"` execution/debug events  
    - (also mentioned under `stream`): `"checkpoints"`, `"tasks"`
  - `streamChannels` optional; if omitted, **all channels** streamed.
- **Config & immutability**
  - `config: LangGraphRunnableConfig` is the **default execution config**, overridable per invocation.
  - `withConfig(newConfig) → CompiledStateGraph`: returns a **new instance** with merged config (immutable pattern).
- **State persistence / HITL**
  - `checkpointer: boolean | BaseCheckpointSaver`: if provided, checkpoints **every superstep**; if `false/undefined`, no save/restore.
  - `getState()`, `getStateHistory()`, `updateState()` **require a checkpointer**.
  - `interruptBefore` / `interruptAfter`: `"*"` or `"__start__"` or `N[]` node names for human-in-the-loop breakpoints.
- **Other key knobs:** `autoValidate` default `true`; `debug` default `false`; `retryPolicy`; `stepTimeout` (ms per superstep); optional `cache`; optional long-term `store`.

</details>

### 📖 Fine-grained tool input streaming (eager_input_streaming)
**Reference Doc** · [source](https://platform.claude.com/docs/it/agents-and-tools/tool-use/fine-grained-tool-streaming)

*Step-by-step procedure for streaming tool calls (incremental tool input emission, event framing, partial tool arguments)*

<details>
<summary>Key content</summary>

- **Purpose / rationale:** Reduce latency by streaming tool parameter values **without buffering or JSON validation**, so large tool arguments can be consumed earlier (but may be **partial/invalid JSON**).
- **Enablement (request + tool):**
  - Set tool field: `eager_input_streaming: true` on any user-defined tool you want streamed.
  - Set request field: `stream: true`.
- **Empirical latency example (chunking behavior):**
  - *Without* fine-grained streaming: ~**15s delay**, many tiny chunks (e.g., `{"`, `query": "Ty`, `peScri`…).
  - *With* fine-grained streaming: ~**3s delay**, fewer/longer chunks (e.g., `{"query": "TypeScript 5.0 5.1 5.2 5.3` then ` new features comparison`).
- **Event framing + accumulation contract (tool_use input arrives as deltas):**
  - On `content_block_start` where `content_block.type == "tool_use"`: event contains placeholder `input: {}`; initialize accumulator: **Eq. 1** `input_json = ""`.
  - For each `content_block_delta` where `delta.type == "input_json_delta"`: **Eq. 2** `input_json += delta.partial_json` (partial JSON string fragments).
  - On `content_block_stop`: **Eq. 3** `parsed = json.loads(input_json)` (parse only after block closes).
  - Type mismatch (`input: {}` object vs `partial_json` string) is **intentional**: `{}` marks the slot; deltas build the real value.
- **Edge cases / defaults:** Because there’s no validation, stream may never form valid JSON; if stop reason `max_tokens` occurs, tool args may end mid-parameter—handle incomplete input explicitly.
- **Error recovery pattern:** To return malformed JSON to the model safely, wrap it: `{"INVALID_JSON": "<invalid json string>"}` (escape quotes/special chars).
- **SDK helpers:** Python/TS provide `stream.get_final_message()` / `stream.finalMessage()` to do accumulation automatically; manual accumulation is for reacting to partial input (progress UI, early downstream requests).
- **Data retention:** Eligible for **Zero Data Retention (ZDR)**; with ZDR, data isn’t stored after the API response returns.

</details>

### 📖 Gemini Function/Tool Calling (Compositional + Parallel)
**Reference Doc** · [source](https://ai.google.dev/gemini-api/docs/function-calling)

*Gemini function/tool calling request/response schema + execution loop (functionDeclarations → model functionCall parts → app executes → return functionResponse with matching `id`), incl. modes and compositional/parallel calling.*

<details>
<summary>Key content</summary>

- **Core workflow (4-step loop):**
  1) **Declare tools**: send `tools: [{ functionDeclarations: [ {name, description, parameters(OpenAPI-subset)} ] }]`.  
  2) **Model decides** (AUTO/VALIDATED) whether to emit **text** or a structured **`functionCall`** with `{id, name, args}`. *(Gemini 3 always returns a unique `id` for each functionCall.)*  
  3) **App executes** the named function using `args` (model never executes tools).  
  4) **Return result** in next turn as **`functionResponse`** including the **exact same `id`** so the API maps results to calls; model then produces final user-facing text.
- **Function declaration schema (OpenAPI subset):** `name` (no spaces/special chars), `description` (specific), `parameters: {type:"object", properties:{...}, required:[...]}`; use `enum` for fixed choices; strong typing reduces errors.
- **Parallel calling:** model may emit multiple `functionCall`s in one turn; results can be returned **in any order** because mapping uses `id`.
- **Compositional (sequential) calling:** model chains calls (e.g., `get_weather_forecast(location)` → `set_thermostat_temperature(temperature)`), repeating the loop until no more calls.
- **Function calling modes (`tool_config.function_calling_config.mode`):**
  - `AUTO`: model chooses text vs call (default when only function tools enabled).
  - `VALIDATED`: constrains to text or valid calls; better schema adherence (default when combining tools/structured output).
  - `ANY`: **always** call a function; optional `allowed_function_names`.
  - `NONE`: prohibit function calls.
- **Critical parsing note:** don’t assume `functionCall` is last in `parts`; iterate all parts (esp. when mixing built-in tools).
- **Best-practice defaults:** keep active tools ~**10–20**; use low temperature (e.g., **0**) for reliable calls; validate high-stakes actions with user.

</details>

### 📖 LangGraph Checkpointing & Persistence (threads, checkpoints, replay)
**Reference Doc** · [source](https://reference.langchain.com/python/langgraph/checkpoints/)

*Checkpointing/persistence API surface (checkpointer interfaces + attaching to compiled graph) for durable memory, resume, time-travel*

<details>
<summary>Key content</summary>

- **Attach persistence to a graph**
  - Compile with a checkpointer: `graph = builder.compile(checkpointer=checkpointer, store=store)` (store optional; checkpointer enables threads/checkpoints).
  - **Must pass `thread_id`** on invoke/stream/batch to persist/resume:  
    `config = {"configurable": {"thread_id": "my-thread"}}`; `graph.invoke(inputs, config)`.  
    `thread_id` is the **primary key** for storing/retrieving checkpoints; without it no save/resume/time-travel.
- **Core objects**
  - **CheckpointMetadata** fields: `source ∈ {'input','loop','update','fork'}`; `step: int` where `-1` = first `"input"` checkpoint, `0` = first `"loop"` checkpoint, increasing thereafter.
  - **Checkpoint** fields: `id: str` (unique, monotonically increasing), `channel_values: dict[str, Any]`, `channel_versions`, `versions_seen` (per-node channel versions seen; drives scheduling).
  - **StateSnapshot** (returned by `graph.get_state*`): `values`, `next` (tuple of next node names; empty `()` means complete), `config` (includes `thread_id`, `checkpoint_ns`, `checkpoint_id`), `metadata` (includes `source`, `writes`, `step`), `created_at`, `parent_config`, `tasks`.
- **Super-step procedure (empirical count)**
  - Checkpoints are created at each **super-step boundary** (“tick”). Example sequential graph `START→A→B→END` yields **4 checkpoints**: empty/START-next, input/node_a-next, after A/node_b-next, after B/complete.
- **Namespaces**
  - `checkpoint_ns=""` for root graph; subgraph checkpoints use `"node_name:uuid"`; nested join with `|`. Accessible in-node via `config["configurable"]["checkpoint_ns"]`.
- **Replay/time travel**
  - Invoke with a prior `checkpoint_id` to **skip** nodes before it (replayed from saved results) and **re-execute** nodes after it (LLM/API/interrupts re-trigger).
- **Checkpointer interface (BaseCheckpointSaver)**
  - Sync: `get`, `get_tuple`, `list`, `put`, `put_writes`, `delete_thread`, `get_next_version`.
  - Async counterparts: `aget`, `aget_tuple`, `alist`, `aput`, `aput_writes`, `adelete_thread`.
  - Example implementation: `InMemorySaver`; SQLite example: `SqliteSaver.from_conn_string(":memory:")`.

</details>

### 📖 LangGraph StateGraph + runtime controls (invoke/stream/interrupt/durability)
**Reference Doc** · [source](https://reference.langchain.com/python/langgraph/graphs/)

*Graph execution semantics + runtime knobs (invoke/stream/interrupt/durability/context); StateGraph structure for iterative agent loops*

<details>
<summary>Key content</summary>

- **Core abstraction (StateGraph):** Nodes communicate via shared **state**. Each node signature: **State → Partial\<State\>** (returns only updated keys). State keys may be `Annotated[..., reducer]` where reducer aggregates multiple node writes: **reducer(Value_left, Value_right) → Value**.
- **Reducer example (list append):**  
  `def reducer(a: list, b: int | None) -> list: return a + [b] if b is not None else a`
- **Context (immutable runtime data):** Provide via `context_schema` and pass at run time: `compiled.invoke(input, context={...})`. Node can accept `runtime: Runtime[Context]` and read `runtime.context.get("r", 1.0)`.
- **Worked numeric example (logistic map step):**  
  **Eq. 1:** `next_value = x * r * (1 - x)` where `x = state["x"][-1]`, `r = runtime.context["r"]`.  
  With input `{"x": 0.5}` and `context={"r": 3.0}`, output becomes `{'x': [0.5, 0.75]}` (since 0.5·3·0.5 = 0.75) using list reducer.
- **Graph construction procedures:**
  - `add_node(name?, fn)` (if name omitted, inferred from callable name).
  - `add_edge(start_key | [start_keys], end_key)`; multiple start keys = wait for **ALL** to complete.
  - `add_conditional_edges(source, path, path_map?)`; if `path` returns **END**, graph stops.
  - `compile(checkpointer=None, interrupt_before=None, interrupt_after=None, debug=False, name=None) → CompiledStateGraph`.
- **Run-time knobs (CompiledStateGraph):**
  - `invoke/ainvoke(..., stream_mode="values", output_keys=None, interrupt_before=None, interrupt_after=None, durability=None)`
  - `stream/astream(..., stream_mode=None)` modes: `"values"`, `"updates"`, `"custom"`, `"messages"` (token stream as `(token, metadata)`), `"checkpoints"`, `"tasks"`, plus `"debug"` in `astream`.
  - `durability` options: `"sync"`, `"async"` (default), `"exit"`.

</details>

### 📖 MCP Transport Norms (stdio + Streamable HTTP)
**Reference Doc** · [source](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

*Normative MCP transport definitions: stdio subprocess lifecycle + Streamable HTTP (POST/GET, SSE), JSON-RPC framing, sessions, resumability, security, version header.*

<details>
<summary>Key content</summary>

- **stdio transport**
  - Client **launches server as subprocess**.
  - Server reads JSON-RPC from **stdin**, writes JSON-RPC to **stdout**.
  - **Framing:** each message is a single JSON-RPC request/notification/response **delimited by newline**; messages **MUST NOT contain embedded newlines**.
  - Server **MAY** log UTF‑8 to **stderr**.
  - Server **MUST NOT** write anything to **stdout** that isn’t a valid MCP message; client **MUST NOT** write anything to **stdin** that isn’t a valid MCP message.

- **Streamable HTTP transport (replaces HTTP+SSE from 2024‑11‑05)**
  - Server **MUST** expose a **single MCP endpoint path** supporting **POST and GET** (e.g., `https://example.com/mcp`).
  - **Security:** validate **Origin** header (DNS rebinding); local servers **SHOULD** bind to **127.0.0.1** not `0.0.0.0`; **SHOULD** authenticate.
  - **Client → server:** each JSON-RPC message = **new HTTP POST**.
    - Client **MUST** send `Accept: application/json, text/event-stream`.
    - POST body **MUST** be a **single** JSON-RPC msg.
    - If input is **response/notification** and accepted: **202 Accepted** (no body); else HTTP error (e.g., **400**), body **MAY** be JSON-RPC error **without id**.
    - If input is a **request**: server returns either `Content-Type: text/event-stream` (SSE) or `application/json` (single JSON); client **MUST** support both.
    - SSE behavior: stream **SHOULD** include the response; server **MAY** send related requests/notifications before responding; **SHOULD NOT** close before response unless session expires; **SHOULD** close after response.
    - Disconnects **SHOULD NOT** imply cancellation; cancel via **CancelledNotification**.
  - **Server → client listening:** client **MAY** `GET` with `Accept: text/event-stream`; server returns SSE or **405**.
    - On GET SSE: server **MAY** send requests/notifications; **MUST NOT** send responses unless **resuming** a prior stream.
  - **Multiple SSE streams:** client **MAY** keep multiple; server **MUST NOT** broadcast same JSON-RPC message on multiple streams.
  - **Resumability:** server **MAY** set SSE `id`; if present, **MUST** be globally unique within session (or client). Client **SHOULD** resume with `Last-Event-ID`; server **MAY** replay only messages from that same stream; **MUST NOT** replay messages from other streams.
  - **Sessions:** server **MAY** issue `Mcp-Session-Id` on InitializeResult response; ID **SHOULD** be globally unique + cryptographically secure; **MUST** be visible ASCII **0x21–0x7E**. If issued, client **MUST** include `Mcp-Session-Id` on subsequent requests. Missing required session ID → **400**. Terminated session → **404**; on 404 client **MUST** start new session (new InitializeRequest w/o session ID). Client **SHOULD** `DELETE` with `Mcp-Session-Id` to end session; server **MAY** return **405**.
  - **Protocol version header (HTTP):** client **MUST** send `MCP-Protocol-Version: <version>` (e.g., `2025-06-18`). If missing and server can’t infer, server **SHOULD** assume **2025-03-26**. Invalid/unsupported version → **400**.

</details>

### 📖 NeMo ReAct Agent (Thought/Action/Observation Loop)
**Reference Doc** · [source](https://docs.nvidia.com/nemo/agent-toolkit/1.3/workflows/about/react-agent.html)

*End-to-end ReAct agent workflow structure + tool registration/invocation + loop orchestration in NeMo Agent Toolkit*

<details>
<summary>Key content</summary>

- **ReAct loop (workflow):** Observation (receive question) → **Thought** (reason step-by-step) → **Action** (select tool by name/description) → **Action Input** → **Observation** (tool result) → repeat until **Final Answer**.
- **Required ReAct output formats (prompt contract):**
  - Tool call:
    - `Question: ...`
    - `Thought: ...`
    - `Action: <one of [{tool_names}]>`
    - `Action Input: <JSON object or "None">`
    - `Observation: wait for the human/tool response; do not assume`
  - Final:
    - `Thought: I now know the final answer`
    - `Final Answer: ...`
- **Prompt variables required when customizing:** must include `{tools}` and `{tool_names}` and instruct the model to emit the ReAct format.
- **YAML configuration (as workflow):**
  - `workflow: _type: react_agent`
  - `tool_names: [wikipedia_search, current_datetime, code_generation, math_agent]`
  - `llm_name: nim_llm`
  - Example: `verbose: true`, `parse_agent_response_max_retries: 2`
- **YAML configuration (as function/tool):** define tools under `functions:` then `_type: react_agent`, `tool_names: [...]`, optional `description` (tool description when exposed to other agents).
- **Defaults/parameters:**
  - `verbose: False`
  - `retry_agent_response_parsing_errors: True`
  - `parse_agent_response_max_retries: 1`
  - `tool_call_max_retries: 1`
  - `max_tool_calls: 15`
  - `pass_tool_call_errors_to_agent: True`
  - `normalize_tool_input_quotes: True` (fallback: replace single→double quotes for JSON parsing)
  - `max_history: 15`
  - `include_tool_input_schema_in_tool_description: True` (appends: `Arguments must be provided as a valid JSON object following this format: {tool_schema}`)
  - `workflow_alias: None`
  - `description: "ReAct Agent Workflow"`
- **Design rationale / limitations:** sequential Think→Act→Observe increases LLM calls (latency/cost), prompt-sensitive, hallucination risk, error propagation in long chains, no parallelism.
- **Requirement:** install `nvidia-nat[langchain]`.

</details>

### 📖 Prompt caching (Claude API) — cost/latency control for iterative loops
**Reference Doc** · [source](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

*Cacheable prompt prefixes + billing/TTL implications for multi-step agent/ReAct/tool loops*

<details>
<summary>Key content</summary>

- **Mechanism (prefix caching):** Caches the **entire prompt prefix** in order **tools → system → messages**, up to and including the block marked with `cache_control`. Cache hits require **100% identical** content (incl. images) through the breakpoint.
- **Two enablement modes:**
  - **Automatic caching:** top-level `"cache_control": {"type":"ephemeral"}`; breakpoint auto-moves to **last cacheable block** as conversation grows.
  - **Explicit breakpoints:** put `cache_control` on specific content blocks; up to **4 breakpoints**.
- **Core algorithm (explicit) (Section “How automatic prefix checking works”):**
  1) **Write only at breakpoints** (one cache entry = hash of prefix ending at breakpoint).  
  2) **Read by lookback:** if no hit at breakpoint, walk backward **1 block at a time** to find a prior **write**.  
  3) **Lookback window = 20 blocks** (breakpoint counts as 1st checked). If last write is >20 blocks back, no hit unless you add another breakpoint earlier.
- **Common pitfall:** placing breakpoint on a **changing block** (timestamp/per-request suffix) yields repeated **cache writes** and **no reads**; move breakpoint to last **stable** block.
- **Defaults/params:**
  - Cache type: `"ephemeral"` only.
  - **TTL default = 5 minutes**; optional `"ttl":"1h"` (higher cost). Cache refreshed at no extra cost on use.
- **Pricing multipliers (all models):** 5m **writes = 1.25×** base input; 1h **writes = 2×** base input; **reads = 0.1×** base input. Example row: **Claude Opus 4.6** base input **$5/MTok**, 5m writes **$6.25/MTok**, 1h writes **$10/MTok**, reads **$0.50/MTok**, output **$25/MTok**.
- **Token accounting (Eq. 1):**  
  `total_input_tokens = cache_read_input_tokens + cache_creation_input_tokens + input_tokens`  
  where `input_tokens` = tokens **after last breakpoint**.
- **Minimum cacheable length:** Opus 4.6/4.5 **4096** tokens; Sonnet 4.6 **2048**; many others **1024** (silent no-cache if below).
- **Thinking blocks:** cannot be directly marked cacheable; can be cached when included in prior assistant turns; **count as input tokens when read**. Non-tool-result user content can strip prior thinking blocks.

</details>

### 📖 StateGraph.compile → CompiledStateGraph runtime contract
**Reference Doc** · [source](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/compile)

*`StateGraph.compile()` binds state schema + reducers into an executable `CompiledStateGraph` (Runnable) exposing `invoke/stream` and accepting `config` + `context`.*

<details>
<summary>Key content</summary>

- **StateGraph model (runtime semantics)**
  - Nodes communicate via shared state; each node signature: **State → Partial<State>**.
  - State keys may be annotated with a **reducer** to aggregate multiple updates: **(Value, Value) → Value** (left = current value, right = update value).
- **Compile requirement**
  - `StateGraph` is a **builder** and **cannot execute** directly; must call **`.compile()`** to get an executable graph supporting: `invoke()`, `stream()`, `ainvoke()`, `astream()`.
- **`compile()` signature (Python)**
  - `compile(checkpointer=None, *, cache=None, store=None, interrupt_before=None, interrupt_after=None, debug=False, name=None) -> CompiledStateGraph`
  - Key defaults: `debug=False`, `name=None`, `checkpointer=None`.
- **Compiled graph capabilities (CompiledStateGraph)**
  - Implements **Runnable** interface: can be invoked, streamed, batched, async.
  - Core methods: `invoke`, `ainvoke`, `stream`, `astream`, plus state ops: `get_state`, `get_state_history`, `update_state`, `bulk_update_state` (bulk requires a checkpointer).
- **`invoke()` signature essentials**
  - `invoke(input, config=None, *, context=None, stream_mode="values", print_mode=(), output_keys=None, interrupt_before=None, interrupt_after=None, durability=None, **kwargs)`
  - `context` is **static run-scoped context** (added in v0.6.0) for immutable data (e.g., `user_id`, `db_conn`).
- **Reducer example (logistic map)**
  - State: `x: Annotated[list, reducer]`; reducer appends new values.
  - `compiled.invoke({"x": 0.5}, context={"r": 3.0})` ⇒ `{'x': [0.5, 0.75]}` where `next = x * r * (1 - x)`.

</details>

### 📖 Structured Outputs / JSON mode — doc index (404 snapshot)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/structured-outputs/json-mode?context=without_parse)

*Intended to cover exact request/response fields + behavioral guarantees for JSON mode vs Structured Outputs; fetched content is a “Page not found” snapshot plus docs navigation.*

<details>
<summary>Key content</summary>

- **HTTP result:** Target URL returned **404: Not Found** (“Page not found”).
- **No API semantics present:** The fetched page contains **no** concrete details about:
  - `response_format` fields, JSON mode invocation, or Structured Outputs guarantees
  - request/response schemas, tool/function calling payloads, streaming event shapes
  - defaults/parameters, error-handling procedures, or comparisons between modes
- **Navigation pointers (relevant alternative docs to consult):**
  - Core concepts: **Structured output** (`/api/docs/guides/structured-outputs`)
  - Core concepts: **Function calling** (`/api/docs/guides/function-calling`)
  - Core concepts: **Using tools** (`/api/docs/guides/tools`)
  - Run & scale: **Streaming** (`/api/docs/guides/streaming-responses`)
  - Suggested search terms shown on page: `response_format`, `reasoning_effort`, `streaming`, `tools`

</details>

### 📖 Structured Outputs — Supported Schemas (link currently 404)
**Reference Doc** · [source](https://platform.openai.com/docs/guides/structured-outputs/supported-schemas?context=ex2)

*Supported JSON Schema subset/constraints for Structured Outputs*

<details>
<summary>Key content</summary>

- **This URL returns HTTP 404 (“Page not found”)** and does **not** contain the promised “Supported schemas” details in the fetched text.
- The fetched page is a **docs navigation shell** listing relevant OpenAI Platform guide entry points (no schema keywords/types/constraints are provided here):
  - **Structured output guide:** https://platform.openai.com/api/docs/guides/structured-outputs
  - **Function calling guide:** https://platform.openai.com/api/docs/guides/function-calling
  - **Using tools guide:** https://platform.openai.com/api/docs/guides/tools
  - **Streaming responses guide:** https://platform.openai.com/api/docs/guides/streaming-responses
  - **MCP & Connectors guide:** https://platform.openai.com/api/docs/guides/tools-connectors-mcp
- No **equations**, **empirical results**, **defaults/parameters**, or **procedural steps** about:
  - accepted JSON Schema keywords/types,
  - strictness/validation behavior,
  - handling invalid schemas,
  - enforcement guarantees,
  appear in the retrieved content.

</details>

### 📖 Structured outputs (JSON outputs + strict tool use)
**Reference Doc** · [source](https://platform.claude.com/docs/en/build-with-claude/structured-outputs)

*Tool name + tool input schema validation guarantees; how Claude enforces/returns structured outputs*

<details>
<summary>Key content</summary>

- **Two complementary features**
  - **JSON outputs** via `output_config.format`: constrains *Claude’s response text* to **valid JSON** matching a provided **JSON Schema**; returned in `response.content[0].text`.
  - **Strict tool use** via `tools[].strict: true`: guarantees **schema validation on tool names and tool inputs** (grammar-constrained sampling).
  - Can be used **independently or together** in one request.
- **Why (design rationale):** avoids malformed JSON / schema violations (missing required fields, wrong types). Guarantees schema-compliant outputs via **constrained decoding** → “no JSON.parse() errors,” type-safe required fields, fewer retries.
- **Procedure (JSON outputs quick start)**
  1. Define JSON Schema (`type`, `properties`, `required`, `additionalProperties: false`).
  2. Send request with `output_config.format: { type: "json_schema", schema: ... }`.
  3. Parse JSON from `response.content[0].text`.
- **Property ordering rule:** output object fields ordered as **required first (schema order)**, then **optional (schema order)**.
- **Failure modes (still possible):**
  - `stop_reason: "refusal"` → may not match schema (200 OK; billed).
  - `stop_reason: "max_tokens"` → truncated/incomplete JSON; retry with higher `max_tokens`.
- **Performance/caching defaults**
  - Grammar compilation adds **first-request latency**.
  - Compiled grammars cached **24 hours since last use**.
  - Cache invalidated if **schema structure** changes or **tool set** changes; changing only tool `name`/`description` does **not** invalidate.
- **Schema complexity limits (explicit)**
  - **20** strict tools/request.
  - **24** total optional parameters across all strict schemas.
  - **16** parameters using union types (`anyOf` or `type: [...]`).
  - Too complex → **400** “Schema is too complex for compilation”; compilation timeout **180s**.
- **Compatibility:** works with streaming, batch, token counting; **incompatible with citations** (400) and **message prefilling**.

</details>

### 📋 # Source: https://docs.anthropic.com/en/docs/build-with-claude/tool-use
**Source** · 

### 📋 # Source: https://docs.langchain.com/oss/python/langgraph/observability
**Source** · 

### 📋 # Source: https://platform.openai.com/docs/guides/tools
**Source** · 

### 🔍 Function-calling evals (BFCL vs NFCL) + practical pitfalls
**Explainer** · [source](https://www.databricks.com/blog/unpacking-function-calling-eval)

*Practical evaluation breakdown for function calling: metrics to track, failure modes, and why leaderboard scores can mislead (with concrete benchmark setups).*

<details>
<summary>Key content</summary>

- **Function calling requirements (Section 1):** model must (1) interpret request, (2) decide whether tools are needed, (3) emit a **correctly formatted call** with correct arguments (typically via **JSON schema**).
- **BFCL taxonomy (Section 2):**
  - *Simple Function* (1 tool; generate args), *Multiple Function* (choose among 2–4 tools + args), *Parallel Function* (same tool invoked multiple times), *Parallel Multiple Function* (multiple tools, multiple invocations), *Relevance Detection* (none relevant → **no call**).
  - **Scoring:** AST-based matching (parse call → extract args → compare to ground truth). Authors found AST accuracy correlates with executable eval; they used AST only.
  - **Pitfall:** Relevance Detection can be gamed—if a model never calls tools, it can score **100%** on this subset.
- **NFCL taxonomy (Section 2):** categories by API source; implemented as **static dummy Python functions** with real API-like signatures.
  - NVD (2 APIs, ~**30 args** each), VirusTotal (**12** APIs), OTX (**9** simple APIs; easiest), Places (nested calls up to **7** deep), Climate (parallel + nested), VirusTotal Nested, NVD Nested (very hard; **no model >10%** in authors’ tests).
  - **Scoring:** exact string match of final call (rare false positives; can cause false negatives).
- **Empirical sensitivity (Section 3):** BFCL accuracy can vary by **~10%** depending on decoding; **Temperature 0.0** usually best for programmatic tool calling. Public BFCL used **T=0.7** and bespoke parsing for DBRX → unfair comparisons.
- **Prompting/protocol that improved results (Section 4):**
  - Put tool definitions in **system prompt** (token savings in multi-turn).
  - Enforce strict output: tool list inside `<tools>`; tool calls as **valid JSON list** between `{tool_call_start}`…`{tool_call_end}` with keys `"name"` and `"arguments"`.
  - Guiding rules: don’t hallucinate tools; don’t call irrelevant tools; **never call same function twice with same args**; user executes tools and returns results next turn.
  - Few-shot “check each tool for relevance” improved BFCL Relevance Detection: **Llama3-70b 63.75%→75.41%**, **Llama3-8b 19.58%→78.33%**; **DBRX 84.58%→77.08%** (because flawed outputs previously inflated relevance score).
- **Design rationale (Section 4–5):** no single leaderboard is sufficient; combine BFCL+NFCL; interpret scores holistically; consider **structured generation / constrained decoding** (Outlines, Guidance, SGlang) for schema guarantees.

</details>

### 🔍 ReAct = Interleaved Reasoning + Acting (Thought/Action/Observation)
**Explainer** · [source](https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/)

*High-level design rationale + walkthrough of the interleaved reasoning/action pattern aligned to the ReAct paper*

<details>
<summary>Key content</summary>

- **Core pattern (trajectory loop):**  
  **Thought (reasoning trace)** → **Action (text action/tool call)** → **Observation (env feedback)** → repeat.  
  - *Thought* updates the model’s **internal state/context** (does **not** affect environment).  
  - *Action* affects the **external environment** (“Env”) and yields an *Observation*.
- **Design rationale:**  
  - **CoT (reason-only)**: strong reasoning but **ungrounded** (can’t update knowledge via external world).  
  - **Act-only**: can interact but lacks **abstract goal reasoning/working memory** for long horizons.  
  - **ReAct** combines both: **reason→act** (plan/adjust actions) and **act→reason** (gather info to ground reasoning), improving **interpretability/diagnosability/controllability** via human-readable trajectories.
- **Prompting procedure (frozen PaLM-540B):** few-shot in-context examples that include **domain-specific actions** (e.g., “search” for QA; “go to” for navigation) + **free-form reasoning traces**.  
  - If **reasoning-heavy tasks**: **alternate** reasoning and actions across multiple steps.  
  - If **action-heavy decision-making**: include **sparse reasoning**; let the LM decide **asynchronous** placement of thoughts vs actions.
- **Fine-tuning pipeline:** use **ReAct-prompted PaLM-540B** to generate trajectories; **filter to successful trajectories**; fine-tune smaller **PaLM-8B/62B** on them.
- **Empirical results (PaLM-540B prompting):**
  - **HotPotQA (EM, 6-shot):** Standard 28.7; CoT 29.4; Act-only 25.7; **ReAct 27.4**; **Best ReAct+CoT 35.1**.  
  - **FEVER (Acc, 3-shot):** Standard 57.1; CoT 56.3; Act-only 58.9; **ReAct 60.9**; **Best ReAct+CoT 64.6**.  
  - **ALFWorld (2-shot success %):** Act-only 45; **ReAct 71**.  
  - **WebShop (1-shot success %):** Act-only 30.1; **ReAct 40**.
- **Human-in-the-loop:** editing a few **reasoning trace sentences** can redirect behavior (e.g., replace hallucinated thought with hints).

</details>

### 🔍 Repairing malformed streamed JSON tool arguments (Anthropic fine-grained tool streaming)
**Explainer** · [source](https://andyjakubowski.com/engineering/handling-invalid-json-in-anthropic-fine-grained-tool-streaming)

*Concrete recovery procedure for malformed/partial streamed JSON tool arguments (buffering, incremental parsing, repair/retry strategy).*

<details>
<summary>Key content</summary>

- **Feature + config:** Anthropic **fine-grained tool streaming** streams tool-argument deltas before the full argument is complete. Enable via HTTP beta header:  
  `anthropic-beta: fine-grained-tool-streaming-2025-05-14`.
- **Trade-off (correctness):** With this beta, **partial and even final tool-call JSON may be invalid** and may not match the tool JSON schema (unlike OpenAI Structured Outputs guarantees).
- **Design rationale:** Adopt despite invalid JSON risk to improve **speed/UX** by rendering partially generated code immediately (e.g., `code` parameter).
- **Schema simplification tactic (reduce invalid JSON):**
  - Problem schema allowed `["string","null"]` for `insertAfterBlockId`, causing model to emit **unquoted UUIDs** (invalid JSON):  
    Invalid: `"insertAfterBlockId": 123e4567-e89b-12d3-a456-426614174000`  
    Valid: `"insertAfterBlockId": "123e4567-e89b-12d3-a456-426614174000"`
  - Fix: restrict to `"type": "string"` and use **empty string** to mean “insert at beginning”.
- **Repair workflow (buffer → repair → parse):**
  1. **Accumulate** streamed tool-call deltas into one string (don’t repair each delta).
  2. Run `untruncate-json` to complete truncated JSON.
  3. Run `jsonrepair` to fix malformed JSON.
  4. Then parse/validate against schema.
- **Middleware interception (Vercel AI SDK):** AI SDK may throw `AI_JSONParseError` before yielding final tool-call chunk; intercept in **language model middleware** (`wrapStream`) and repair `chunk.args` when `chunk.type === 'tool-call'`, then enqueue repaired chunk. Wrap model with `wrapLanguageModel({ middleware: repairToolArgsMiddleware })`.

</details>

---

## Related Topics

- [[topics/agent-fundamentals|Agent Fundamentals]]
- [[topics/system-prompts|System Prompts]]
- [[topics/multi-agent-systems|Multi-Agent Systems]]
- [[topics/mcp-tool-ecosystem|Model Context Protocol]]
