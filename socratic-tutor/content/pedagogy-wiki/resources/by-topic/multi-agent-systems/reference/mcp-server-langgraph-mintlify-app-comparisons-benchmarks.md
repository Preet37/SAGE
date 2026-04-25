# Source: https://mcp-server-langgraph.mintlify.app/comparisons/benchmarks
# Title: Performance Benchmarks - MCP Server with LangGraph
# Fetched via: trafilatura
# Date: 2026-04-10

Overview
This page documents real-world performance benchmarks for MCP Server with LangGraph and competitor frameworks. All tests use identical hardware, equivalent workloads, and the same LLM provider for fair comparison.Benchmark Methodology
Test Environment
All benchmarks run on standardized hardware:| Specification | Value |
|---|---|
| Cloud Provider | Google Cloud Platform |
| Instance Type | n2-standard-4 |
| vCPUs | 4 (Intel Xeon @ 2.3GHz) |
| Memory | 16 GB RAM |
| Storage | SSD (1000 IOPS) |
| Network | 10 Gbps |
| Region | us-central1 |
Test Configuration
Common Parameters:- LLM Provider: Gemini 2.0 Flash (for cost-effective testing)
- Load Testing Tool: k6 (
[k6.io](https://k6.io)) - Test Duration: 5 minutes per scenario (after 1-minute ramp-up)
- Runs: Average of 3 test runs
- Monitoring: Prometheus + Grafana for metrics collection
- Simple Agent: Single-node workflow, basic tool execution
- Multi-Agent: 3-agent sequential coordination
- Complex Workflow: 5-node graph with conditional branching
- High Concurrency: 100+ concurrent requests
Benchmark Results
Simple Agent Workflow
Scenario: Single-node agent answering factual questions using Gemini Flash.MCP Server with LangGraph (Self-Hosted on Cloud Run)
| Metric | Value | Notes |
|---|---|---|
| Throughput | 142 req/s | Sustained over 5 minutes |
| Latency (p50) | 245 ms | Median response time |
| Latency (p95) | 890 ms | 95th percentile |
| Latency (p99) | 1,210 ms | 99th percentile |
| Error Rate | 0.02% | Less than 1 error per 5,000 requests |
| CPU Usage | 68% avg | Peak: 85% |
| Memory Usage | 4.2 GB avg | Peak: 5.8 GB |
LangGraph Cloud (Managed Platform)
| Metric | Value | Notes |
|---|---|---|
| Throughput | 135 req/s | Slightly lower due to platform overhead |
| Latency (p50) | 280 ms | +35ms vs self-hosted |
| Latency (p95) | 950 ms | Similar to self-hosted |
| Latency (p99) | 1,450 ms | +240ms vs self-hosted |
| Error Rate | 0.05% | Acceptable |
| Cost | $675/5min | $0.001 per node execution |
Multi-Agent Coordination
Scenario: 3-agent workflow (researcher → analyzer → writer) with sequential execution.MCP Server with LangGraph (Kubernetes on GKE)
| Metric | Value | Notes |
|---|---|---|
| Throughput | 48 req/s | Lower due to multi-agent overhead |
| Latency (p50) | 1,850 ms | Median for 3-agent workflow |
| Latency (p95) | 4,200 ms | 95th percentile |
| Latency (p99) | 6,100 ms | 99th percentile |
| Error Rate | 0.08% | Acceptable for complex workflow |
| Horizontal Scaling | ✅ Linear | 2x pods = ~2x throughput |
CrewAI (Self-Hosted)
| Metric | Value | Notes |
|---|---|---|
| Throughput | 52 req/s | Faster for simple sequential workflows |
| Latency (p50) | 1,650 ms | Lower latency (-200ms) |
| Latency (p95) | 3,800 ms | Faster execution |
| Latency (p99) | 5,400 ms | More consistent |
| Error Rate | 0.12% | Slightly higher |
| Horizontal Scaling | ⚠️ Manual | Requires custom setup |
Why CrewAI is Faster: CrewAI’s role-based delegation model has lower orchestration overhead for simple sequential tasks. MCP Server’s StateGraph provides more flexibility but adds minimal latency for complex workflows with conditionals and loops.
Complex Workflow with Conditionals
Scenario: 5-node graph with conditional branching, error handling, and state persistence.MCP Server with LangGraph
| Metric | Value | Notes |
|---|---|---|
| Throughput | 32 req/s | Complex state management |
| Latency (p50) | 2,800 ms | Median for complex workflow |
| Latency (p95) | 6,500 ms | 95th percentile |
| Latency (p99) | 9,200 ms | 99th percentile |
| Error Rate | 0.15% | Low given complexity |
| State Persistence | ✅ Built-in | Redis checkpointing |
| Fault Tolerance | ✅ Automatic | Retry on failure |
OpenAI AgentKit (Platform)
| Metric | Value | Notes |
|---|---|---|
| Throughput | N/A | Visual builder not suitable for benchmark |
| Latency | N/A | Platform doesn’t expose metrics |
| Error Rate | Unknown | No programmatic access |
| Cost | ~$5,000/mo | For 1M complex requests (estimated) |
High Concurrency Load Test
Scenario: 100 concurrent virtual users sending requests continuously for 10 minutes.MCP Server with LangGraph (Kubernetes with HPA)
| Metric | Value | Notes |
|---|---|---|
| Max Throughput | 425 req/s | With auto-scaling to 10 pods |
| Latency (p50) | 320 ms | Under high load |
| Latency (p95) | 1,200 ms | Acceptable degradation |
| Latency (p99) | 2,400 ms | 99th percentile |
| Error Rate | 0.25% | Rate limits from LLM provider |
| Auto-Scaling | ✅ Automatic | HPA scaled 2→10 pods |
| Recovery Time | 45 seconds | From spike to steady state |
Google ADK (Vertex AI Agent Engine)
| Metric | Value | Notes |
|---|---|---|
| Max Throughput | 380 req/s | Managed scaling |
| Latency (p50) | 360 ms | Slightly higher |
| Latency (p95) | 1,450 ms | +250ms vs MCP Server |
| Error Rate | 0.18% | Good reliability |
| Auto-Scaling | ✅ Automatic | Platform-managed |
| Cost | Higher | Vertex AI fees + compute |
Cost-Performance Analysis
Cost per 1M Requests (Complex Workflow)
| Framework | Infrastructure | LLM Costs | Total | Notes |
| MCP Server (GKE) | $300 | $12 | $312 | Self-hosted, Gemini Flash |
| MCP Server (Cloud Run) | $500 | $12 | $512 | Serverless, auto-scaling |
| LangGraph Cloud | $5,000 | $0 | $5,000 | Platform fees (node executions) |
| Google ADK | $1,000 | $15 | $1,015 | Vertex AI Agent Engine |
| OpenAI AgentKit | $0 | $5,000 | $5,000 | GPT-4 costs + web search |
Scaling Characteristics
Horizontal Scaling Efficiency
Vertical Scaling
| CPU/Memory | Throughput | Cost Efficiency |
|---|---|---|
| 2 vCPU / 8GB | 75 req/s | Baseline |
| 4 vCPU / 16GB | 142 req/s | 90% efficient |
| 8 vCPU / 32GB | 260 req/s | 87% efficient |
Real-World Performance Expectations
Production Deployment Estimates
Scenario 1: Healthcare Startup (HIPAA-compliant)- Load: 50K requests/month
- Configuration: MCP Server on GKE (2 pods, n2-standard-2)
- Performance: p95 latency under 1s, 99.95% uptime
- Cost: ~$150/month (infrastructure + LLM)
- Load: 10M requests/month
- Configuration: MCP Server on GKE (12 pods, n2-standard-4, multi-region)
- Performance: p95 latency under 2s, 99.99% uptime
- Cost: ~$1,200/month (infrastructure + LLM)
- Load: 500K requests/month
- Configuration: MCP Server on GKE (4 pods, n2-highmem-4, private cluster)
- Performance: p95 latency under 1.5s, 99.99% uptime
- Cost: ~$500/month (infrastructure + LLM)
Benchmark Limitations
What These Benchmarks Don’t Measure
- ❌ Cold Start Performance: All tests measured warm instances (excluding cold starts)
- ❌ Network Latency: Tests run in same region as LLM provider (minimal network overhead)
- ❌ Complex Tool Execution: Simple tools used (web search, database queries not benchmarked)
- ❌ Long-Running Workflows: Tests limited to under 10 second workflows
- ❌ Memory-Intensive Workloads: Benchmarks focus on CPU/network, not memory-bound operations
Factors That Impact Your Performance
- LLM Provider Response Time: Gemini/Claude/GPT have different latencies
- Tool Execution Time: Complex tool calls (database queries, API calls) add latency
- Network Geography: Distance to LLM provider affects response time
- Workflow Complexity: More nodes, conditionals, and loops increase latency
- State Persistence: Checkpointing to Redis/PostgreSQL adds overhead
Running Your Own Benchmarks
Want to validate these results in your environment?
See
[tests/benchmarks/README.md](https://github.com/vishnu2kmohan/mcp-server-langgraph/tree/main/tests/benchmarks)for detailed instructions.
Frequently Asked Questions
Why is CrewAI faster for simple workflows?
Why is CrewAI faster for simple workflows?
CrewAI’s role-based delegation model has lower orchestration overhead for simple sequential tasks (researcher → writer → editor). MCP Server’s LangGraph StateGraph provides more flexibility (conditionals, loops, human-in-the-loop) but adds minimal latency (~50-100ms) for complex workflows.Use CrewAI if: Simple sequential workflows, prototyping, learning
Use MCP Server if: Production deployments, complex workflows, enterprise features needed
How accurate are these benchmarks?
How accurate are these benchmarks?
These benchmarks provide relative comparisons with controlled variables (same hardware, LLM provider, duration). Absolute numbers will vary in your environment based on:
- Network latency to LLM provider
- Tool execution time (database queries, API calls)
- Workflow complexity (our tests use simple workflows)
- Instance type and configuration
What about OpenAI AgentKit benchmarks?
What about OpenAI AgentKit benchmarks?
OpenAI AgentKit’s visual builder doesn’t support programmatic load testing. Platform doesn’t expose performance metrics or support API-driven benchmarking. Cost estimates based on public pricing ($10/1k web search calls, GPT-4 API costs).
Why focus on Gemini Flash for benchmarks?
Why focus on Gemini Flash for benchmarks?
Reasons:
- Cost-effective: 20x cheaper than GPT-4 (10-30 per 1M tokens)
- Fast: Low latency for responsive testing
- Fair comparison: Available across all frameworks (via LiteLLM)
- Representative: Realistic for production use cases balancing cost/performance
Do these benchmarks include LLM API time?
Do these benchmarks include LLM API time?
Yes, benchmarks include end-to-end latency:
- Network round-trip to LLM provider
- LLM inference time
- Framework orchestration overhead
- State persistence (if applicable)
Contributing Benchmarks
Have benchmark results to share? We welcome contributions:- Fork the repository
- Run benchmarks using our methodology (same hardware, config)
- Document all parameters (instance type, LLM provider, workflow)
- Submit PR with results to
tests/benchmarks/RESULTS.md
[CONTRIBUTING.md](https://github.com/vishnu2kmohan/mcp-server-langgraph/blob/main/CONTRIBUTING.md)for guidelines.
Run Benchmarks Yourself
Clone repo and validate results
Compare Frameworks
Full framework comparison guide
Production Deployment
Deploy to production
Multi-LLM Setup
Optimize costs with multiple providers
Benchmark Transparency: All benchmark scripts, configurations, and raw results are open-source in our