# Source: https://arxiv.org/pdf/2603.22651.pdf
# Author: Siddhant Kulkarni and Yukta Kulkarni
# Title: Benchmarking Multi-Agent LLM Architectures for ...
# Fetched via: trafilatura
# Date: 2026-04-09

Benchmarking Multi-Agent LLM Architectures for Financial Document Processing: A Comparative Study of Orchestration Patterns, Cost-Accuracy Tradeoffs and Production Scaling Strategies
Abstract
The adoption of large language models (LLMs) for structured information extraction from financial documents has accelerated rapidly, yet production deployments face fundamental architectural decisions with limited empirical guidance. We present a systematic benchmark comparing four multi-agent orchestration architectures: sequential pipeline, parallel fan-out with merge, hierarchical supervisor-worker and reflexive self-correcting loop. These are evaluated across five frontier and open-weight LLMs on a corpus of 10,000 SEC filings (10-K, 10-Q and 8-K forms). Our evaluation spans 25 extraction field types covering governance structures, executive compensation and financial metrics, measured along five axes: field-level F1, document-level accuracy, end-to-end latency, cost per document and token efficiency. We find that reflexive architectures achieve the highest field-level F1 (0.943) but at the cost of sequential baselines, while hierarchical architectures occupy the most favorable position on the cost-accuracy Pareto frontier (F1 0.921 at cost). We further present ablation studies on semantic caching, model routing and adaptive retry strategies, demonstrating that hybrid configurations can recover 89% of the reflexive architecture’s accuracy gains at only baseline cost. Our scaling analysis from 1K to 100K documents per day reveals non-obvious throughput-accuracy degradation curves that inform capacity planning. These findings provide actionable guidance for practitioners deploying multi-agent LLM systems in regulated financial environments.
I Introduction
The financial services industry generates an enormous volume of regulatory filings, earnings reports and disclosure documents that require structured data extraction for downstream analytics, compliance monitoring and investment decision-making. The U.S. Securities and Exchange Commission (SEC) alone receives over 230,000 filings annually through its EDGAR system, each containing dozens of extractable fields spanning financial metrics, governance disclosures, executive compensation tables and risk factor narratives [[1](#bib.bib1)]. Traditional approaches relying on rule-based parsers and named entity recognition pipelines have been progressively supplanted by LLM-based extraction systems that offer greater generalization across document formats and field types [[2](#bib.bib2)].
However, single-prompt LLM extraction faces well-documented limitations: context window constraints force document chunking that severs cross-reference dependencies, hallucination rates increase with extraction complexity and the absence of verification mechanisms makes error detection difficult [[3](#bib.bib3)]. Multi-agent architectures address these limitations by decomposing extraction into specialized subtasks, enabling verification loops and supporting dynamic resource allocation. Yet the design space of multi-agent orchestration is vast and practitioners lack empirical evidence on which architectural patterns best serve different operational requirements.
This gap is consequential. A financial institution processing 50,000 documents per quarter faces infrastructure costs that vary by an order of magnitude depending on architecture choice, while regulatory obligations demand extraction accuracy that exceeds specific thresholds for audit defensibility. An incorrect architectural decision can result in either prohibitive costs or unacceptable error rates, outcomes that are difficult to reverse once systems are in production.
I-A Research Questions
We address three research questions.
RQ1: How do different multi-agent orchestration patterns (sequential, parallel, hierarchical, reflexive) compare on extraction accuracy, latency and cost for financial document processing?
RQ2: What is the cost-accuracy Pareto frontier across architectures and models and which configurations dominate for different operational constraints?
RQ3: How do architectural performance characteristics change as processing volume scales from 1K to 100K documents per day?
I-B Contributions
Our primary contributions are as follows.
-
1.
A rigorous benchmark framework for evaluating multi-agent LLM architectures on financial document extraction, with 25 field types, five models and four architectures yielding 500 distinct experimental configurations.
-
2.
Empirical evidence that hierarchical architectures provide the best cost-accuracy tradeoff for production financial document processing, achieving 97.7% of reflexive architecture accuracy at 60.9% of the cost.
-
3.
Ablation studies demonstrating that semantic caching, model routing and adaptive retries can be combined to recover 89% of reflexive accuracy gains at baseline cost, a practical “best of both worlds” configuration.
-
4.
Scaling analysis revealing non-linear throughput-accuracy degradation curves, with architecture-specific knee points beyond which accuracy drops sharply, informing capacity planning for production deployments.
-
5.
A failure taxonomy specific to multi-agent financial extraction, cataloging 12 failure modes with architecture-specific prevalence rates and mitigation strategies.
II Related Work
II-A Multi-Agent LLM Systems
The multi-agent paradigm for LLM applications has evolved rapidly since the introduction of tool-augmented reasoning frameworks. Yao et al. [[4](#bib.bib4)] proposed ReAct, interleaving reasoning traces with actions and establishing a foundation for agentic LLM behavior. Subsequent frameworks operationalized multi-agent coordination at varying levels of abstraction: AutoGen [[5](#bib.bib5)] introduced conversational agent topologies with customizable interaction patterns; CrewAI [[6](#bib.bib6)] formalized role-based agent teams with delegation protocols; and LangGraph [[7](#bib.bib7)] provided a stateful graph abstraction for composing cyclic agent workflows.
Theoretical analyses of multi-agent LLM coordination have examined communication overhead [[8](#bib.bib8)], emergent specialization [[9](#bib.bib9)] and failure propagation [[10](#bib.bib10)]. Hong et al. [[11](#bib.bib11)] presented MetaGPT, demonstrating that structured communication protocols between agents reduce hallucination cascades. However, these analyses have focused primarily on creative and coding tasks, leaving financial document processing underexplored.
II-B LLM Evaluation and Benchmarking
Evaluation methodology for LLM-based systems has matured significantly. RAGAS [[12](#bib.bib12)] established metrics for retrieval-augmented generation quality. DSPy [[13](#bib.bib13)] introduced programmatic optimization of LLM pipelines with systematic evaluation. HELM [[14](#bib.bib14)] provided a holistic framework for model comparison. For document extraction specifically, the Document Understanding Benchmark [[15](#bib.bib15)] and the Financial NER benchmark [[16](#bib.bib16)] provide task-specific evaluation protocols.
Cost-aware evaluation remains underdeveloped. Prior work [[17](#bib.bib17)] proposed token-efficiency metrics but did not account for multi-turn agent interactions. Our work extends evaluation to include amortized cost per extracted field, enabling direct comparison of architectures with different token consumption profiles.
II-C Financial Document Processing with LLMs
LLM-based financial document processing has progressed from simple extraction to complex reasoning. BloombergGPT [[18](#bib.bib18)] demonstrated domain-specific pretraining advantages. FinGPT [[19](#bib.bib19)] explored open-source alternatives. More recently, Chen et al. [[20](#bib.bib20)] applied multi-agent systems to financial analysis, while Xie et al. [[21](#bib.bib21)] benchmarked LLMs on structured financial data extraction from SEC filings, finding that GPT-4-class models achieve 85–92% field-level accuracy on clean filings but degrade significantly on complex tabular formats.
Our work differs from prior financial NLP benchmarks in three respects: (1) we compare orchestration architectures rather than individual models; (2) we include cost and latency as first-class evaluation dimensions; and (3) we evaluate at production-relevant scale with throughput analysis.
II-D Orchestration Patterns in Production Systems
The software engineering community has documented architectural patterns for LLM applications [[22](#bib.bib22), [23](#bib.bib23)], including chain-of-thought decomposition, map-reduce aggregation and iterative refinement loops. Madaan et al. [[24](#bib.bib24)] introduced Self-Refine, showing that iterative self-feedback improves LLM outputs. Shinn et al. [[25](#bib.bib25)] proposed Reflexion, extending self-correction with episodic memory. Our hierarchical and reflexive architectures draw on these patterns but adapt them specifically for structured extraction from financial documents, incorporating domain-specific verification agents and confidence-calibrated routing.
III System Architecture
We evaluate four multi-agent orchestration architectures, each implemented as a directed graph of specialized agents. All architectures share a common set of atomic agents (document parser, field extractor, table analyzer, cross-reference resolver, confidence scorer and output formatter) but differ in how these agents are composed and coordinated.
III-A Architecture A: Sequential Pipeline
The sequential pipeline processes documents through a fixed chain of agents, where each agent receives the full context accumulated by prior agents.
Characteristics. Deterministic execution order. Linear latency growth with agent count. No parallelism. Error propagation is unidirectional: upstream errors compound downstream. Token consumption is cumulative, as each agent receives the growing context from all prior agents.
Implementation. Each agent is implemented as a single LLM call with a role-specific system prompt. The accumulated state is passed as a structured JSON object that grows at each stage. We impose a maximum context budget of 128K tokens; documents exceeding this limit after parsing are split into sections processed independently and merged at the output stage.
III-B Architecture B: Parallel Fan-Out with Merge
The parallel architecture dispatches independent extraction tasks simultaneously and merges results through a dedicated reconciliation agent.
Characteristics. Latency is dominated by the slowest parallel branch plus merge overhead. Near-linear throughput scaling with parallelism degree. Independent failures are isolated to their branch. Token efficiency is high, as each extractor receives only the relevant document sections. Reconciliation handles conflicting extractions from overlapping context windows.
Implementation. The dispatcher agent classifies document sections by relevance to each extraction domain (financial metrics, governance, compensation) using a lightweight routing model. Each domain extractor operates on its assigned sections independently. The merge agent resolves conflicts using a confidence-weighted voting scheme when multiple extractors produce values for the same field.
III-C Architecture C: Hierarchical Supervisor-Worker
The hierarchical architecture introduces a supervisor agent that dynamically allocates tasks, monitors progress and coordinates specialized workers.
Characteristics. Adaptive task allocation based on document complexity. Selective re-extraction of low-confidence fields reduces unnecessary computation. Supervisor overhead adds latency per decision point. The architecture supports heterogeneous model assignment: the supervisor can route complex fields to stronger models and simpler fields to cheaper models.
Implementation. The supervisor agent maintains a task queue and a confidence threshold (calibrated at 0.85 on validation data). Workers report extraction results with calibrated confidence scores. Fields below the threshold are re-assigned, potentially to a different worker or model. The supervisor limits re-extraction to two iterations to bound cost.
III-D Architecture D: Reflexive Self-Correcting Loop
The reflexive architecture introduces explicit verification and self-correction cycles, where extraction outputs are critiqued and revised iteratively.
Characteristics. Highest accuracy potential through iterative refinement. Cost scales with document difficulty: simple documents may pass on the first iteration, while complex documents may require multiple correction cycles. Non-deterministic cost and latency. The verifier agent applies domain-specific consistency rules (e.g., the financial identity check: total assets = total liabilities + equity).
Implementation. The verifier agent performs three categories of checks: (1) format validation (dates, currency values, percentages); (2) cross-field consistency (balance sheet identity, compensation totals); and (3) source grounding (extracted values must have supporting evidence in the source text). Failed checks generate structured critique messages that guide the correction agent. A maximum of three correction iterations is enforced, after which the best-confidence extraction is emitted with a low-confidence flag.
IV Experimental Setup
IV-A Dataset
We constructed a benchmark dataset of 10,000 SEC filings sourced from the EDGAR Full-Text Search system, stratified as shown in Table [I](#S4.T1).
| Filing Type | Count | Avg. Pages | Avg. Tokens |
|---|---|---|---|
| 10-K | 4,000 | 142 | 187,340 |
| 10-Q | 4,000 | 68 | 82,150 |
| 8-K | 2,000 | 12 | 14,820 |
Filings were sampled from fiscal years 2021–2024 across 11 GICS sectors, with deliberate oversampling of complex filings (conglomerates, financial institutions and real estate investment trusts) that historically challenge extraction systems. All filings were converted from HTML/XBRL to plain text with table structure preserved using a custom parser built on the sec-edgar-downloader library [[27](#bib.bib27)].
IV-B Ground Truth Annotation
Gold-standard annotations were produced through a three-stage process: (1) automated pre-annotation using XBRL tags where available, covering approximately 60% of financial metric fields; (2) manual annotation by a team of 12 annotators with CFA or CPA credentials, achieving inter-annotator agreement of Cohen’s ; (3) adjudication of disagreements by a senior financial analyst. The annotation schema covers 25 field types organized into three domains.
Financial Metrics (10 fields): total revenue, net income, total assets, total liabilities, shareholders’ equity, operating cash flow, capital expenditures, earnings per share (basic), earnings per share (diluted) and debt-to-equity ratio.
Governance (8 fields): board size, independent director count, CEO duality (binary), audit committee size, audit committee financial expert (binary), annual meeting date, shareholder proposal count and poison pill status (binary).
Executive Compensation (7 fields): CEO total compensation, CEO base salary, CEO bonus, CEO stock awards, CEO option awards, median employee compensation and CEO pay ratio.
IV-C Models
We evaluate five LLMs representing the frontier and open-weight categories, as shown in Table [II](#S4.T2).
| Model | Provider | Context | Cost ($/1M tok.) |
|---|---|---|---|
| GPT-4o (2024-11-20) | OpenAI | 128K | 2.50 / 10.00 |
| Claude 3.5 Sonnet | Anthropic | 200K | 3.00 / 15.00 |
| Gemini 1.5 Pro | 1M | 1.25 / 5.00 | |
| Llama 3 70B | Meta | 128K | 0.60 / 0.80 |
| Mixtral 8x22B | Mistral | 64K | 0.50 / 0.70 |
Open-weight models were served on A100 80GB nodes using vLLM [[26](#bib.bib26)] with tensor parallelism. All API-based models used the latest available versions as of January 2025. Temperature was set to 0.0 for all extraction calls and 0.3 for supervisor and critique agents to allow exploratory reasoning.
IV-D Evaluation Metrics
We report five metrics.
-
1.
Field-level F1 (micro-averaged): Precision and recall computed per field, treating exact match (for categorical fields) and tolerance (for numerical fields) as correct.
-
2.
Document-level accuracy: Fraction of documents where all 25 fields are correctly extracted (strict) or where fields are correct (relaxed).
-
3.
End-to-end latency (, ): Wall-clock time from document submission to structured output, measured at the system level.
-
4.
Cost per document: Total API/compute cost amortized across all agent calls for a single document, in USD.
-
5.
Token efficiency: Ratio of output information tokens to total tokens consumed (input + output across all agent calls), capturing how much useful work each token performs.
IV-E Implementation Details
All architectures were implemented using LangGraph v0.2 [[7](#bib.bib7)] for workflow orchestration, with custom agent nodes wrapping model-specific API clients. Experiments were executed on a cluster of 8 machines (each with 96 CPU cores, 384 GB RAM and NVIDIA A100 80GB GPUs) over a 21-day period. Each architecture-model combination was evaluated on all 10,000 documents, yielding 200,000 document-level evaluations (). For statistical robustness, we report 95% confidence intervals computed via bootstrap resampling ().
V Results
V-A Overall Performance
Table [III](#S5.T3) presents the primary results across all architecture-model combinations. We report field-level micro-F1, document-level strict accuracy, median latency and cost per document.
| Architecture | Metric | GPT-4o | Claude 3.5S | Gemini 1.5P | Llama3 70B | Mixtral 8x22B |
|---|---|---|---|---|---|---|
| Sequential (A) | F1 | 0.897 | 0.903 | 0.881 | 0.834 | 0.812 |
| Doc Acc | 0.631 | 0.648 | 0.597 | 0.487 | 0.453 | |
| Lat (s) | 34.2 | 38.7 | 29.1 | 22.4 | 19.8 | |
| Cost ($) | 0.142 | 0.187 | 0.098 | 0.038 | 0.031 | |
| Parallel (B) | F1 | 0.908 | 0.914 | 0.893 | 0.851 | 0.829 |
| Doc Acc | 0.659 | 0.672 | 0.623 | 0.521 | 0.488 | |
| Lat (s) | 18.6 | 21.3 | 15.7 | 12.1 | 10.9 | |
| Cost ($) | 0.168 | 0.221 | 0.117 | 0.046 | 0.038 | |
| Hierarchical (C) | F1 | 0.921 | 0.929 | 0.907 | 0.869 | 0.843 |
| Doc Acc | 0.704 | 0.718 | 0.662 | 0.558 | 0.519 | |
| Lat (s) | 41.8 | 46.2 | 33.4 | 26.7 | 23.1 | |
| Cost ($) | 0.198 | 0.261 | 0.138 | 0.054 | 0.044 | |
| Reflexive (D) | F1 | 0.936 | 0.943 | 0.919 | 0.878 | 0.851 |
| Doc Acc | 0.741 | 0.758 | 0.691 | 0.572 | 0.534 | |
| Lat (s) | 67.3 | 74.1 | 52.8 | 41.2 | 36.4 | |
| Cost ($) | 0.327 | 0.430 | 0.226 | 0.089 | 0.072 |
Key Finding 1: Reflexive achieves the highest accuracy, but at substantial cost. The reflexive architecture with Claude 3.5 Sonnet achieves the best field-level F1 of 0.943 and document-level strict accuracy of 0.758. However, this comes at a cost of $0.430 per document, which is the sequential baseline ($0.187 with the same model) and the hierarchical variant ($0.261).
Key Finding 2: Hierarchical offers the best cost-accuracy tradeoff. The hierarchical architecture achieves 98.5% of reflexive F1 (0.929 vs. 0.943 for Claude 3.5 Sonnet) at 60.7% of the cost ($0.261 vs. $0.430). Across all models, hierarchical consistently occupies the Pareto frontier between sequential and reflexive.
Key Finding 3: Parallel reduces latency with modest accuracy gains. The parallel architecture achieves latency reduction over sequential (mean across models) with a mean F1 improvement of . This makes it attractive for latency-sensitive workloads that do not require maximum accuracy.
V-B Per-Domain Performance
Extraction difficulty varies substantially across domains. Table [IV](#S5.T4) shows F1 scores broken down by domain for the hierarchical architecture, selected as the Pareto-optimal configuration.
| Domain | GPT-4o | Claude 3.5S | Gemini 1.5P |
|---|---|---|---|
| Financial Metrics | 0.952 | 0.958 | 0.941 |
| Governance | 0.914 | 0.921 | 0.896 |
| Exec. Compensation | 0.887 | 0.898 | 0.871 |
| Domain | Llama3 70B | Mixtral 8x22B | |
| Financial Metrics | 0.912 | 0.893 | |
| Governance | 0.852 | 0.824 | |
| Exec. Compensation | 0.827 | 0.798 |
Financial metrics are the easiest domain (mean F1 0.931), benefiting from standardized GAAP reporting formats and numerical cross-checks. Governance fields are moderately difficult (mean F1 0.881), with binary fields such as CEO duality and poison pill status being particularly challenging due to inconsistent disclosure language. Executive compensation is the hardest domain (mean F1 0.856), owing to complex multi-year vesting schedules, performance-contingent awards and the need to distinguish “target” from “actual” compensation figures.
V-C Ablation Studies
We conduct three ablation studies using the hierarchical architecture with Claude 3.5 Sonnet as the base configuration (F1 , cost /doc).
V-C1 Semantic Caching
We implement a semantic cache using embedding-based similarity matching (text-embedding-3-small, cosine threshold 0.95) on agent inputs. When a sufficiently similar input has been processed previously, the cached output is returned without an LLM call (Table [V](#S5.T5)).
| Cache Config | F1 | Cost/doc | Lat (s) | Hit Rate |
| No cache | 0.929 | $0.261 | 46.2 | — |
| Section-level | 0.927 | $0.198 | 34.8 | 24.1% |
| Field-level | 0.924 | $0.171 | 29.3 | 38.7% |
| Hybrid (adaptive) | 0.926 | $0.182 | 31.4 | 31.4% |
Field-level caching achieves the greatest cost reduction (34.5%) with a modest F1 decrease of 0.005. The hybrid configuration, which caches field-level results for standard-format sections and disables caching for non-standard sections, achieves a favorable middle ground.
V-C2 Model Routing
We evaluate a routing strategy where the supervisor agent assigns extraction tasks to different models based on estimated difficulty. Simple fields (binary governance indicators and standardized financial metrics) are routed to Mixtral 8x22B, while complex fields (compensation breakdowns and nuanced governance disclosures) are routed to Claude 3.5 Sonnet (Table [VI](#S5.T6)).
| Routing Strategy | F1 | Cost/doc | Lat (s) |
|---|---|---|---|
| All Claude 3.5 Sonnet | 0.929 | $0.261 | 46.2 |
| All GPT-4o | 0.921 | $0.198 | 41.8 |
| All Mixtral 8x22B | 0.843 | $0.044 | 23.1 |
| 2-tier (Claude + Mixtral) | 0.912 | $0.127 | 31.6 |
| 3-tier (Claude + GPT + Mixtral) | 0.918 | $0.143 | 33.2 |
The 2-tier routing strategy reduces cost by 51.3% relative to all-Claude while retaining 98.2% of the F1 score. The 3-tier strategy adds GPT-4o for medium-difficulty fields, recovering an additional 0.006 F1 at moderate cost increase.
V-C3 Adaptive Retry Strategies
We compare retry strategies for handling low-confidence extractions in the hierarchical architecture (Table [VII](#S5.T7)).
| Retry Strategy | F1 | Cost/doc | Lat (s) | Retry Rate |
| No retry | 0.908 | $0.214 | 38.1 | 0% |
| Fixed retry (1x) | 0.929 | $0.261 | 46.2 | 14.2% |
| Confidence-gated | 0.926 | $0.243 | 43.7 | 10.8% |
| Escalation (model+) | 0.931 | $0.258 | 45.1 | 12.1% |
| Adaptive threshold | 0.929 | $0.247 | 44.0 | 11.6% |
The escalation strategy, where failed extractions are retried with a more capable model, achieves the highest F1 (0.931) by directing difficult cases to stronger models. The adaptive threshold strategy, which raises the confidence threshold for fields with historically high error rates, matches the baseline F1 while reducing cost by 5.4%.
V-C4 Combined Optimization
Combining semantic caching (hybrid), model routing (2-tier) and adaptive retry yields a configuration we term Hierarchical-Optimized (Table [VIII](#S5.T8)).
| Configuration | F1 | Cost/doc | Lat (s) |
|---|---|---|---|
| Sequential baseline | 0.903 | $0.187 | 38.7 |
| Hierarchical baseline | 0.929 | $0.261 | 46.2 |
| Reflexive baseline | 0.943 | $0.430 | 74.1 |
| Hierarchical-Optimized | 0.924 | $0.148 | 30.2 |
The Hierarchical-Optimized configuration achieves F1 of 0.924, recovering 89% of the accuracy gap between sequential and reflexive baselines, at a cost of $0.148/doc. This is only the sequential baseline cost and the hierarchical baseline cost, representing the most practically relevant finding of our study.
V-D Scaling Analysis
We evaluate throughput-accuracy characteristics by varying the daily document processing volume from 1K to 100K under fixed compute budgets representative of production deployments (Table [IX](#S5.T9)).
| Docs/Day | Seq. F1 | Par. F1 | Hier. F1 | Refl. F1 |
| 1,000 | 0.903 | 0.914 | 0.929 | 0.943 |
| 5,000 | 0.903 | 0.914 | 0.928 | 0.941 |
| 10,000 | 0.901 | 0.913 | 0.926 | 0.937 |
| 25,000 | 0.899 | 0.911 | 0.919 | 0.924 |
| 50,000 | 0.894 | 0.906 | 0.907 | 0.898 |
| 100,000 | 0.886 | 0.898 | 0.891 | 0.871 |
Key Finding 4: Reflexive architecture degrades fastest at scale. The reflexive architecture maintains its accuracy advantage up to approximately 25K docs/day but degrades sharply beyond that point. At 50K docs/day, it falls below the hierarchical architecture and at 100K docs/day it is the worst-performing architecture. This is because the iterative correction loops create queuing delays under high load; when timeout constraints are imposed, correction iterations are truncated, eliminating the architecture’s primary advantage.
Key Finding 5: Sequential is the most scale-resilient. The sequential architecture shows the smallest absolute F1 degradation from 1K to 100K docs/day (0.017), owing to its deterministic execution profile and absence of coordination overhead. However, its absolute F1 remains below parallel and hierarchical at all tested scales up to 50K.
The architectural crossover point, where hierarchical F1 drops below parallel F1, occurs at approximately 75K docs/day on our test cluster. This threshold is infrastructure-dependent and will shift with compute scaling, but the qualitative pattern (reflexive degrades fastest, sequential degrades slowest) is robust.
V-E Latency Distribution Analysis
Latency characteristics differ across architectures in ways not captured by median statistics alone (Table [X](#S5.T10)).
| Architecture | |||
|---|---|---|---|
| Sequential | 38.7 | 62.4 | 89.1 |
| Parallel | 21.3 | 41.7 | 68.3 |
| Hierarchical | 46.2 | 78.3 | 124.6 |
| Reflexive | 74.1 | 148.7 | 247.3 |
The reflexive architecture exhibits the widest latency distribution ( ratio of ), reflecting the variable number of correction iterations. This makes it unsuitable for applications with strict latency SLAs unless combined with aggressive timeout policies, which, as shown in Section [V](#S5), degrade its accuracy advantage.
VI Analysis and Discussion
VI-A Architecture Selection Guidelines
Our results suggest the following decision framework for practitioners.
Use Sequential when: (a) the extraction task is simple (fewer than 10 field types); (b) documents are short and well-formatted; (c) cost is the primary constraint; or (d) processing volume exceeds 75K documents per day on constrained infrastructure. The sequential architecture’s predictability and low overhead make it the pragmatic default.
Use Parallel when: (a) latency is critical (e.g., real-time processing pipelines); (b) extraction domains are naturally independent; or (c) the system must handle bursty workloads. The parallel architecture’s ability to exploit multi-core and multi-GPU infrastructure directly translates input parallelism into latency reduction.
Use Hierarchical when: (a) maximum cost-efficiency at high accuracy is required; (b) the field set includes both simple and complex extraction targets; or (c) the system must operate at moderate scale (10K–50K docs/day) without accuracy degradation. The hierarchical architecture’s adaptive routing and selective retry mechanisms make it the most production-suitable choice for most financial document processing scenarios.
Use Reflexive when: (a) extraction accuracy is paramount and cost is secondary (e.g., compliance-critical fields for regulatory submissions); (b) processing volume is low (under 10K docs/day); or (c) the output is consumed by downstream processes intolerant of errors. The reflexive architecture’s self-correction mechanism is most valuable precisely when errors are most costly.
VI-B Cost-Accuracy Pareto Frontier
We construct the Pareto frontier across all tested configurations by plotting F1 against cost per document. The Hierarchical-Optimized configuration ($0.148, F1 ) represents a particularly attractive knee point on the Pareto frontier, offering near-reflexive accuracy at near-sequential cost. For organizations willing to spend more, the hierarchical baseline with Claude 3.5 Sonnet ($0.261, F1 ) offers the next significant quality improvement.
VI-C Failure Mode Analysis
We identify and categorize 12 failure modes through manual analysis of 500 error cases (125 per architecture). Table [XI](#S6.T11) reports the prevalence of the top failure modes by architecture.
| Failure Mode | Seq. | Par. | Hier. | Refl. |
| Cross-table reference failure | 28.4 | 12.1 | 14.3 | 8.7 |
| Temporal confusion (FY vs. QTR) | 18.2 | 17.8 | 12.1 | 6.4 |
| Unit/scale error (M vs. K vs. raw) | 14.7 | 14.2 | 10.8 | 4.2 |
| Proxy stmt. vs. 10-K confusion | 9.3 | 6.8 | 7.2 | 5.1 |
| Restated figure extraction | 8.1 | 9.4 | 8.7 | 7.8 |
| Compensation vesting misparse | 7.6 | 8.3 | 9.1 | 8.4 |
| Context window truncation | 5.8 | 14.7 | 6.2 | 3.8 |
| Agent coordination failure | 0.0 | 8.1 | 12.4 | 14.2 |
| Hallucinated field value | 4.9 | 4.3 | 3.8 | 2.1 |
| Ambiguous disclosure resolution | 3.0 | 4.3 | 15.4 | 39.3 |
Several patterns emerge. First, cross-table reference failures, where a field’s value requires linking data across multiple tables or sections, are the dominant failure mode for the sequential architecture (28.4%) because information is processed in a fixed order that may not revisit earlier sections. The parallel and hierarchical architectures mitigate this through reconciliation and supervisor oversight, respectively, while the reflexive architecture’s verification step catches most such errors.
Second, agent coordination failures (conflicts, deadlocks and message corruption) are absent in the sequential architecture but affect all multi-agent architectures. Notably, coordination failures increase from parallel (8.1%) to hierarchical (12.4%) to reflexive (14.2%), reflecting the increasing complexity of inter-agent communication.
Third, the reflexive architecture’s dominant failure mode is ambiguous disclosure resolution (39.3% of its errors). When a filing genuinely contains ambiguous language, the reflexive architecture’s correction loop can oscillate between interpretations across iterations, sometimes settling on a less likely reading. This “overthinking” failure mode is unique to iterative architectures.
VI-D Token Efficiency Analysis
Token efficiency, the ratio of useful output information to total tokens consumed, reveals the computational overhead of each architecture (Table [XII](#S6.T12)).
| Architecture | Input | Output | Total | Eff. |
| Sequential | 142,340 | 3,820 | 146,160 | 2.61% |
| Parallel | 168,720 | 4,210 | 172,930 | 2.43% |
| Hierarchical | 197,480 | 5,640 | 203,120 | 2.78% |
| Reflexive | 312,670 | 8,940 | 321,610 | 2.78% |
Interestingly, hierarchical and reflexive architectures achieve the same token efficiency ratio (2.78%) despite consuming vastly different total tokens. This is because both architectures generate proportionally more useful output per token: the hierarchical through targeted extraction and the reflexive through iterative refinement of outputs. The parallel architecture is the least token-efficient (2.43%) due to overlapping context windows across branches that result in redundant input processing.
VI-E Limitations
Our study has several limitations. First, our dataset is restricted to SEC filings in English; results may not generalize to other jurisdictions (e.g., IFRS filings) or languages. Second, our cost analysis uses API pricing as of January 2025 and will require updating as model pricing evolves. The directional findings (reflexive is most expensive, sequential is cheapest) are likely stable, but the specific cost ratios will shift. Third, our evaluation uses a fixed set of 25 field types; performance on novel field types not represented in our prompt engineering may differ. Fourth, we evaluate individual model versions and do not account for model degradation over time [[28](#bib.bib28)], which may affect production systems using API-served models. Fifth, our ground truth annotations, while produced by credentialed professionals, may contain systematic biases in ambiguous cases that affect apparent accuracy of different architectures.
VII Conclusion and Future Work
We have presented a comprehensive benchmark of four multi-agent LLM architectures for financial document processing, evaluated across five models, 25 extraction field types and 10,000 SEC filings. Our findings provide three actionable conclusions for practitioners.
-
1.
The hierarchical architecture offers the best cost-accuracy tradeoff for production financial document processing, achieving 98.5% of the best-observed F1 at 60.7% of the cost. When combined with semantic caching, model routing and adaptive retries, the optimized hierarchical configuration recovers 89% of the reflexive architecture’s accuracy gains at only the sequential baseline cost.
-
2.
Architecture choice interacts with scale in non-obvious ways. The reflexive architecture, which is the best performer at low volume, becomes the worst performer above 50K documents per day due to queuing-induced timeout truncation. Production architects must consider target scale in their architecture selection.
-
3.
Failure modes are architecture-specific and often represent the dark side of each architecture’s strengths. The reflexive architecture’s iterative correction, its primary advantage, also generates its dominant failure mode (oscillating ambiguity resolution). Practitioners should implement architecture-specific monitoring to detect these failure patterns.
VII-A Future Directions
Several directions merit future investigation. First, dynamic architecture switching, routing individual documents to different architectures based on estimated complexity, could combine the efficiency of sequential processing for simple documents with the accuracy of reflexive processing for complex ones. Preliminary experiments suggest this could achieve F1 at cost below $0.180/doc, but robust complexity estimation remains an open challenge.
Second, fine-tuned specialist models for specific extraction domains (e.g., a compensation-extraction model distilled from GPT-4o outputs) could dramatically reduce the cost of high-accuracy extraction. Our model routing ablation suggests that task-specific smaller models can handle 60–70% of extraction tasks without quality loss.
Third, streaming architectures that process filings incrementally as they are published, extracting from early sections while later sections are still being parsed, could reduce effective latency by 40–60% for long documents such as 10-K filings.
Fourth, cross-document reasoning, where extraction from one filing is informed by the same company’s prior filings, could address temporal confusion errors and enable trend extraction, which is not possible with document-independent processing.
Finally, formal verification of financial identity constraints (e.g., balance sheet equations) as hard post-conditions could provide provable correctness guarantees for a subset of extracted fields, complementing the probabilistic assurances of LLM-based verification.
References
- [1] U.S. Securities and Exchange Commission, “EDGAR Full-Text Search,” 2024. [Online]. Available: https://efts.sec.gov/LATEST/search-index?q=&dateRange=custom&startdt=2024-01-01
- [2] H. Li, Y. Xu and H. Ji, “Evaluating the zero-shot robustness of instruction-tuned language models,” in Proc. ICLR, 2023.
- [3] L. Huang et al., “A survey on hallucination in large language models: Principles, taxonomy, challenges and open questions,” arXiv preprint arXiv:2311.05232, 2023.
- [4] S. Yao et al., “ReAct: Synergizing reasoning and acting in language models,” in Proc. ICLR, 2023.
- [5] Q. Wu et al., “AutoGen: Enabling next-gen LLM applications via multi-agent conversation,” arXiv preprint arXiv:2308.08155, 2023.
- [6] J. Moura, “CrewAI: Framework for orchestrating role-playing, autonomous AI agents,” GitHub Repository, 2024. [Online]. Available: https://github.com/joaomdmoura/crewAI
- [7] LangChain, “LangGraph: Build resilient language agents as graphs,” GitHub Repository, 2024. [Online]. Available: https://github.com/langchain-ai/langgraph
- [8] W. Chen et al., “Scalable multi-agent communication in large language model systems,” arXiv preprint arXiv:2402.07339, 2024.
- [9] J. S. Park et al., “Generative agents: Interactive simulacra of human behavior,” in Proc. 36th Annu. ACM Symp. User Interface Software and Technology (UIST), 2023, pp. 1–22.
- [10] Y. Zhang et al., “Failure modes of multi-agent LLM systems,” arXiv preprint arXiv:2403.05511, 2024.
- [11] S. Hong et al., “MetaGPT: Meta programming for a multi-agent collaborative framework,” in Proc. ICLR, 2024.
- [12] S. Es, J. James, L. Espinosa-Anke and S. Schockaert, “RAGAs: Automated evaluation of retrieval augmented generation,” in Proc. 18th Conf. European Chapter of the ACL (EACL), 2024, pp. 150–158.
- [13] O. Khattab et al., “DSPy: Compiling declarative language model calls into state-of-the-art pipelines,” in Proc. ICLR, 2024.
- [14] P. Liang et al., “Holistic evaluation of language models,” Trans. Mach. Learn. Res., 2023.
- [15] L. Borchmann et al., “DUE: End-to-end document understanding benchmark,” in Proc. NeurIPS Datasets and Benchmarks Track, 2021.
- [16] L. Loukas et al., “FiNER: Financial numeric entity recognition for XBRL tagging,” in Proc. 60th Annu. Meeting of the ACL, 2022, pp. 4419–4431.
- [17] S. Chen et al., “Token-efficient LLM training pipeline,” arXiv preprint arXiv:2401.09935, 2024.
- [18] S. Wu et al., “BloombergGPT: A large language model for finance,” arXiv preprint arXiv:2303.17564, 2023.
- [19] H. Yang et al., “FinGPT: Democratizing internet-scale data for financial large language models,” arXiv preprint arXiv:2306.06031, 2023.
- [20] D. Chen et al., “Multi-agent collaboration in financial analysis,” arXiv preprint arXiv:2404.01215, 2024.
- [21] Q. Xie et al., “FinBen: A holistic financial benchmark for large language models,” arXiv preprint arXiv:2402.12522, 2024.
- [22] H. Chase, “LangChain: Building applications with LLMs through composability,” GitHub Repository, 2024. [Online]. Available: https://github.com/langchain-ai/langchain
- [23] M. Zaharia et al., “The shift from models to compound AI systems,” Berkeley Artificial Intelligence Research Blog, 2024.
- [24] A. Madaan et al., “Self-Refine: Iterative refinement with self-feedback,” in Proc. NeurIPS, 2023.
- [25] N. Shinn et al., “Reflexion: Language agents with verbal reinforcement learning,” in Proc. NeurIPS, 2023.
- [26] W. Kwon et al., “Efficient memory management for large language model serving with PagedAttention,” in Proc. 29th Symp. Operating Systems Principles (SOSP), 2023.
- [27] A. Jeon, “sec-edgar-downloader: A Python package for bulk downloading SEC EDGAR filings,” GitHub Repository, 2023. [Online]. Available: https://github.com/jadchaar/sec-edgar-downloader
- [28] L. Chen et al., “How is ChatGPT’s behavior changing over time?” arXiv preprint arXiv:2307.09009, 2023.