# Card: Live API Bench (NL2SQL → Invocable Tool-Calling APIs)
**Source:** https://arxiv.org/pdf/2506.11266.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Pipeline converting BIRD-SQL NL2SQL into executable API sequences (SLOT/SEL/REST) + results tables for LLMs and ReAct agents

## Key Content
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

## When to surface
Use when students ask about **tool-calling evaluation**, **ReAct vs direct tool calls**, or how to **construct/measure** multi-step API benchmarks (SLOT/SEL/REST) and interpret **completion-rate** results.