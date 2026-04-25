# Card: MCP Server + LangGraph Performance Benchmarks
**Source:** https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark tables comparing latency/throughput/error/cost for LangGraph-based MCP server vs alternatives under controlled conditions.

## Key Content
- **Benchmark methodology / defaults**
  - Hardware (GCP): **n2-standard-4**, **4 vCPU (Intel Xeon 2.3GHz)**, **16GB RAM**, **SSD 1000 IOPS**, **10Gbps**, region **us-central1**.
  - LLM: **Gemini 2.0 Flash**. Load tool: **k6**. Duration: **5 min** per scenario after **1-min ramp-up**. **Avg of 3 runs**. Metrics: **Prometheus + Grafana**.
  - Workloads: **Simple Agent (single node)**; **Multi-Agent (3 sequential agents)**; **Complex Workflow (5-node graph w/ conditionals)**; **High Concurrency (100+ concurrent)**.
- **Empirical results (end-to-end latency includes LLM + network + orchestration + persistence)**
  - **Simple Agent (MCP+LangGraph, Cloud Run self-hosted):** **142 req/s**, p50 **245ms**, p95 **890ms**, p99 **1210ms**, error **0.02%**, CPU **68% avg (85% peak)**, mem **4.2GB avg (5.8GB peak)**.
  - **Simple Agent (LangGraph Cloud):** **135 req/s**, p50 **280ms**, p95 **950ms**, p99 **1450ms**, error **0.05%**, cost **$675/5min** (**$0.001/node execution**).
  - **Multi-Agent 3-step (MCP+LangGraph on GKE):** **48 req/s**, p50 **1850ms**, p95 **4200ms**, p99 **6100ms**, error **0.08%**, scaling **~linear** (2× pods ≈ 2× throughput).
  - **Multi-Agent (CrewAI self-hosted):** **52 req/s**, p50 **1650ms**, p95 **3800ms**, p99 **5400ms**, error **0.12%**; rationale: lower overhead for simple sequential delegation.
  - **Complex 5-node conditional graph (MCP+LangGraph):** **32 req/s**, p50 **2800ms**, p95 **6500ms**, p99 **9200ms**, error **0.15%**; **Redis checkpointing**, **automatic retries**.
  - **High concurrency (100 VUs; MCP+LangGraph on K8s+HPA):** max **425 req/s** (autoscale **2→10 pods**), p50 **320ms**, p95 **1200ms**, p99 **2400ms**, error **0.25%**, recovery **45s**.
  - **High concurrency (Google ADK):** max **380 req/s**, p50 **360ms**, p95 **1450ms**, error **0.18%**, cost **higher** (Vertex fees).
- **Cost-per-1M complex requests**
  - MCP (GKE): **$312** (infra **$300** + LLM **$12**); MCP (Cloud Run): **$512**; LangGraph Cloud: **$5000**; Google ADK: **$1015**.
- **Scaling table (vertical)**
  - **2 vCPU/8GB: 75 req/s** (baseline); **4 vCPU/16GB: 142 req/s (90% efficient)**; **8 vCPU/32GB: 260 req/s (87% efficient)**.

## When to surface
Use when students ask for **quantitative evidence** about LangGraph/MCP performance (latency/throughput/error), **scaling behavior**, or **cost tradeoffs** vs CrewAI/Google ADK/LangGraph Cloud under controlled benchmarks.