# Card: Multi-agent orchestration benchmark (SEC filing extraction)
**Source:** https://arxiv.org/pdf/2603.22651.pdf  
**Role:** benchmark | **Need:** DEPLOYMENT_CASE  
**Anchor:** Comparative tables across multi-agent orchestration architectures with measurable outcomes + ablations + scaling

## Key Content
- **Architectures compared (Sec. III):**
  - **A Sequential pipeline:** fixed agent chain; cumulative JSON state passed forward; max context **128K**; split long docs into sections then merge.
  - **B Parallel fan-out + merge:** dispatcher routes sections to domain extractors; merge agent resolves conflicts via **confidence-weighted voting**.
  - **C Hierarchical supervisor-worker:** supervisor maintains task queue; **confidence threshold = 0.85**; low-confidence fields re-assigned; **max 2 re-extraction iterations**; supports **heterogeneous model routing**.
  - **D Reflexive self-correcting loop:** verifier checks (1) format, (2) cross-field consistency, (3) **source grounding**; example rule: **Total Assets = Total Liabilities + Equity**; **max 3 correction iterations**, else emit best-confidence with low-confidence flag.
- **Dataset (Sec. IV-A):** **10,000** SEC filings: **4k 10-K (avg 187,340 tokens)**, **4k 10-Q (82,150)**, **2k 8-K (14,820)**; **25 fields** across financial metrics (10), governance (8), exec comp (7).
- **Defaults (Sec. IV-C):** temperature **0.0** for extraction calls; **0.3** for supervisor/critique.
- **Primary results (Table III):** (Claude 3.5 Sonnet)
  - Sequential: **F1 0.903**, cost **$0.187**, latency **38.7s**
  - Parallel: **F1 0.914**, cost **$0.221**, latency **21.3s**
  - Hierarchical: **F1 0.929**, cost **$0.261**, latency **46.2s**
  - Reflexive: **F1 0.943**, cost **$0.430**, latency **74.1s**
  - Key tradeoff: hierarchical achieves **98.5%** of reflexive F1 at **60.7%** of cost.
- **Ablations on hierarchical+Claude (Tables V–VIII):**
  - Semantic cache (embed sim **0.95**, text-embedding-3-small): field-level cache cost **$0.171** (−34.5%), F1 **0.924**.
  - Model routing: **2-tier (Claude+Mixtral)** F1 **0.912**, cost **$0.127** (−51.3%).
  - Retries: escalation (retry with stronger model) best F1 **0.931**.
  - Combined “Hierarchical-Optimized”: **F1 0.924**, cost **$0.148**, latency **30.2s** (near-sequential cost).
- **Scaling (Table IX):** reflexive degrades fastest: F1 **0.943→0.871** from **1K→100K docs/day**; sequential most resilient (**0.903→0.886**). Reflexive falls below hierarchical by **50K/day** due to queueing/timeouts truncating correction loops.

## When to surface
Use for questions about choosing multi-agent orchestration patterns (sequential/parallel/hierarchical/reflexive) under **accuracy–cost–latency** constraints, and for **production scaling**/throughput planning with concrete benchmark numbers.