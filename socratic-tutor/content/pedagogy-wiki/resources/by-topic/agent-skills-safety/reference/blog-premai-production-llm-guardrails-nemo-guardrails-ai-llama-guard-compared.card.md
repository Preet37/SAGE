# Card: Production LLM Guardrails — Tool & Latency/FP Trade-offs
**Source:** https://blog.premai.io/production-llm-guardrails-nemo-guardrails-ai-llama-guard-compared/  
**Role:** explainer | **Need:** COMPARISON_DATA  
**Anchor:** Side-by-side comparison of NeMo Guardrails vs Guardrails AI vs Llama Guard (+ LLM Guard), with latency, deployment patterns, and production trade-offs.

## Key Content
- **Guardrail stages + latency budgets (Table):** Input (prompt injection/PII/banned topics) **50–200ms**; Output (toxicity/secrets/off-topic) **100–500ms**; Retrieval (poisoned chunks/sensitive docs) **20–100ms**.
- **False-positive compounding math (Eq. 1):**  
  - \(P(\text{all correct}) = a^n\) where \(a\)=per-guard accuracy, \(n\)=#guards.  
  - \(P(\ge 1 \text{ false positive}) = 1 - a^n\).  
  - Example: \(a=0.9, n=5 \Rightarrow 1-0.9^5=0.41\) (**41%** flagged). Table: 5 guards @95% ⇒ **23%** FP; 5 @99% ⇒ **5%** FP.
- **Latency tiers:** Tier1 rules **µs–10ms**; Tier2 classifiers **20–100ms**; Tier3 LLM-judge **500ms–8s**. Rationale: **layer + early exit** to keep average latency low.
- **Tool selection matrix (key rows):**  
  - **NeMo Guardrails:** dialog/topic steering; **medium** latency; **T4** GPU; open source; adds **1 LLM call** for flow routing; rail types: **input/output/dialog/retrieval/execution** (execution wraps tool calls).  
  - **Guardrails AI:** structured output validation via **RAIL** specs; latency **20–200ms** per validator; supports **server mode** (`guardrails start ...`); `on_fail`: **REFRAIN/FIX/EXCEPTION/NOOP**.  
  - **LLM Guard:** scanner pipeline; **20–200ms**; anonymize/deanonymize with **Vault** (in-memory mappings).  
  - **Llama Guard 3-8B:** LLM classifier; **800ms P50**; needs **A100**; vision moderation; categories **S1–S13**; customizable via system prompt.
- **Empirical P50 latency (benchmarks):** Regex **<1ms**; LLM Guard toxicity **45ms** (5-guard pipeline **120ms**); Presidio PII **35ms**; Guardrails AI pipeline **300–500ms**; NeMo input check **150–400ms** (pipeline **600ms–1.2s**); Llama Guard **800ms**.
- **Accuracy (datasets):** ToxiGen F1: Llama Guard 3 **0.89** vs OpenAI Moderation **0.82**. JailbreakBench detection/FP: Regex **35%/2%**, PromptGuard(BERT) **72%/8%**, LLM Guard inj **78%/12%**, Llama Guard 3 **85%/15%**, **NeMo+Nemotron 89%/11%**.
- **Cost for 1M req/mo:** Regex **~$20**; LLM Guard **~$150**; Guardrails AI **~$200**; Llama Guard(A100) **~$800**; OpenAI Moderation **$200 API**; GPT-4 judge **$3k–10k**.
- **Deployment patterns:** **Sidecar proxy**, **middleware**, **async pipeline** (Kafka worker). Monitoring: track **P50/P95/P99**, block spikes, error rate, queue depth; graceful degradation via **timeouts + fallback** (fail open vs closed).

## When to surface
Use when students ask how to choose/compose guardrail tools, estimate latency/cost, manage false positives, or design a layered production guardrail architecture (including RAG and agent/tool-call safety).