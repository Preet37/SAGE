# Source: https://arxiv.org/pdf/2602.18968.pdf
# Author: Tao Zhe et al.
# Title: Robust and Efficient Tool Orchestration via Layered Execution Structures with Reflective Correction
# Fetched via: trafilatura
# Date: 2026-04-10

Robust and Efficient Tool Orchestration via Layered
Execution Structures with Reflective Correction
Abstract
Tool invocation is a core capability of agentic systems, yet failures often arise not from individual tool calls but from how multiple tools are organized and executed together. Existing approaches tightly couple tool execution with step-wise language reasoning or explicit planning, leading to brittle behavior and high execution overhead. To overcome these limitations, we revisit tool invocation from the perspective of tool orchestration. Our key insight is that effective orchestration does not require precise dependency graphs or fine-grained planning. Instead, a coarse-grained layer structure suffices to provide global guidance, while execution-time errors can be corrected locally. Specifically, we model tool orchestration as learning a layered execution structure that captures high-level tool dependencies, inducing layer-wise execution through context constraints. To handle execution-time failures, we introduce a schema-aware reflective correction mechanism that detects and repairs errors locally. This design confines errors to individual tool calls and avoids re-planning entire execution trajectories. This structured execution paradigm enables a lightweight and reusable orchestration component for agentic systems. Experimental results show that our approach achieves robust tool execution while reducing execution complexity and overhead. Code will be made publicly available.
1 Introduction
Large language model (LLM)-based agentic systems have emerged as a dominant paradigm for tackling complex, real-world tasks that require perception, decision-making, and action (Schick et al., [2023](#bib.bib1); Qin et al., [2023](#bib.bib3)).
At the core of this paradigm is tool invocation, which enables agents to interact with external environments and perform operations beyond parametric knowledge.
Recent industry visions, most notably articulated by NVIDIA, point toward hybrid agent architectures that rely on LLMs for high-level planning and small language models (SLMs) for scalable execution (Belcak et al., [2025](#bib.bib2)).
In this setting, the primary challenge is no longer invoking individual tools, but reliably coordinating multiple tools over long horizons.
As a result, failures increasingly come from tool orchestration, rather than individual tool calls.
Errors in ordering and dependency management propagate through execution and lead to fluent but incorrect outcomes, particularly for SLMs with limited context and recovery capacity. (Lu et al., [2023](#bib.bib31); Jiang et al., [2025](#bib.bib5); Mekala et al., [2024](#bib.bib47); Zhu et al., [2025b](#bib.bib6)).
For instance, as shown in Figure [1](#S0.F1), consider a SLM agent tasked with computing quarterly revenue using multiple tools.
A correct execution verifies data semantics, such as fiscal period and currency, before performing computation, whereas an incorrect execution invokes the calculation tool prematurely on unverified values.
Although the premature computation is numerically valid, it produces a semantically incorrect intermediate result that irreversibly contaminates subsequent execution.
This example illustrates that tool execution order is a structural constraint that directly determines system verifiability and correctness—yet current approaches struggle to enforce such constraints reliably.
Prior tool orchestration approaches largely fall into two paradigms, both of which are suboptimal for small language models.
The first paradigm is step-wise and reactive (e.g., ReAct (Yao et al., [2022](#bib.bib4))), where agents decide actions incrementally
without an explicit global structure. As a result, these methods often
miss implicit prerequisites, leading to dead-end toolchains or excessive
computation overhead. The second paradigm is plan-then-execute
(e.g., HuggingGPT (Shen et al., [2023](#bib.bib7)), PS (Wang et al., [2023](#bib.bib35))),
which constructs a global plan upfront and executes it sequentially.
While such plans provide high-level guidance, they are brittle to
runtime deviations, such as schema mismatches, format collapse, or empty tool outputs,
and typically rely on ad-hoc retries rather than principled repair.
Recent work addresses these limitations through SLM fine-tuning,
including decision-tree search (Qin et al., [2023](#bib.bib3)) and layer-wise
DAG execution (Zhu et al., [2025a](#bib.bib12)), but incurs training costs.
Consequently, existing approaches lack a unified mechanism that jointly provides global structural awareness and local error resilience during execution.
To bridge these gaps, our aim is to enable agents to orchestrate multiple tools in a manner that combines global awareness of tool dependencies with robustness to execution-time errors. Rather than predicting tool calls step by step or following a rigid plan, we ask: How can structured yet resilient tool execution be achieved, especially without time-consuming fine-tuning of SLMs? Achieving this goal, however, involves two key research challenges as follows:
-
•
Challenge 1: Fast induction of a coarse execution sketch. In multi-tool tasks, tool dependencies are implicit and combinatorially complex, making manual specification of execution order prohibitively costly and unscalable. The challenge is to quickly infer a rough execution sketch that captures essential prerequisites without exhaustive planning or tool-specific rules.
-
•
Challenge 2: Faithful execution with effective failure repair. Even with a reasonable execution sketch, execution-time errors are unavoidable due to noisy tools and hidden constraints. The challenge is to identify execution errors and repair them locally under the induced structure, rather than allowing errors to cascade through the chain of tool invocation.
To address these challenges, we propose a Robust and Efficient Tool Orchestration framework based on layered execution structures with reflective correction, named RETO. The key idea is to decouple the global organization from local execution by inducing a coarse execution structure and correcting errors during execution rather than committing to an exact plan. Specifically, RETO includes three key stages: Learn (layer execution sketch). RETO employs a lightweight layer predictor to infer a coarse layer structure, organizing tools into ordered layers based on implicit prerequisite relations from task and tool descriptions. Execute (context-constrained invocation). Guided by the layer structure, RETO invokes tools layer by layer, restricting each step to relevant tools and previously validated outputs. This constraint reduces decision complexity and limits error propagation, enabling stable execution for SLMs. Reflect and Repair (local correction). Since execution-time errors are unavoidable, RETO employs schema-aware reflective correction to identify invalid or inconsistent tool outputs and perform local repair within the layer structure, rather than replan globally. This design confines failures to individual tool calls and prevents cascading errors in long multi-tool executions. To summarize, our contributions are threefold:
-
•
Problem. We reformulate tool orchestration from step-wise tool selection to structured execution control via layer structures. This perspective frames orchestration as a system-level execution problem.
-
•
Algorithm. We propose RETO, a robust and efficient tool orchestration framework. It combines layered execution structures with reflective local correction to support structured and resilient multi-tool execution.
-
•
Evaluation. We evaluate RETO on large-scale real-world tool benchmarks across different scenarios. The results demonstrate consistent improvements in effectiveness, robustness, efficiency, and generalization.
2 Related Work
Tool Learning for LLMs.
Teaching LLMs to use external tools has emerged as a key paradigm for extending model capabilities beyond static parametric knowledge (Schick et al., [2023](#bib.bib1); Qin et al., [2023](#bib.bib3)).
Early work focused on constructing benchmarks and datasets for tool use (Patil et al., [2024](#bib.bib16); Tang et al., [2023](#bib.bib17); Huang et al., [2023](#bib.bib18)).
ToolBench (Qin et al., [2023](#bib.bib3)) introduced a large-scale benchmark with over 16,000 real-world APIs and proposed DFSDT (Depth-First Search-based Decision Tree) for multi-step tool invocation.
Subsequent work improved efficiency through A* search pruning (Zhuang et al., [2023](#bib.bib19)) and compiler-based parallel execution (Kim et al., [2024](#bib.bib20)), or enhanced reliability via self-reflection (Du et al., [2024](#bib.bib21)) and preference optimization (Chen et al., [2024](#bib.bib22)). However, hallucination and instability still hinder reliable tool invocation (Patil et al., [2025](#bib.bib60)).
Planning Paradigms for Tool Use.
Prior work on tool orchestration can be broadly grouped into two paradigms by how it organizes tool dependencies during execution.
Reactive methods like ReAct (Yao et al., [2022](#bib.bib4)) and Reflexion (Shinn et al., [2023](#bib.bib8)) interleave reasoning and action step-by-step, offering flexibility but lacking global dependency awareness.
Plan-then-execute methods like HuggingGPT (Shen et al., [2023](#bib.bib7)) and Plan-and-Solve (Wang et al., [2023](#bib.bib35); Xu et al., [2023](#bib.bib61)) first generate a complete plan before execution, but struggle with runtime failures due to the disconnect between planning and execution. Recent work (Wu et al., [2024](#bib.bib43)) reveals that attention biases and auto-regressive loss fundamentally limit LLMs’ ability to navigate graph-structured decisions.
Our work bridges these paradigms: we offload coarse-grained layer prediction to a lightweight module, providing global dependency awareness while keeping execution locally adaptive to runtime failures.
Efficient Tool Learning with Smaller Models.
Smaller language models offer computational efficiency but struggle with multi-tool orchestration due to limited context capacity and weaker long-horizon reasoning (Belcak et al., [2025](#bib.bib2)).
Prior work addresses this by internalizing tool-related knowledge into LLMs through fine-tuning.
DTA-Tool (Zhu et al., [2025a](#bib.bib12)) transforms sequential trajectories into DAG structures and fine-tunes LLMs for parallel execution.
GAP (Wu et al., [2025](#bib.bib44)) combines supervised fine-tuning with reinforcement learning to generate dependency graphs.
ToolGen (Wang et al., [2024](#bib.bib62))
fine-tunes LLMs to internalize tool knowledge for autonomous retrieval and execution.
Shen et al. (Shen et al., [2024](#bib.bib27)) distribute tasks across
multiple fine-tuned agents. While effective, these approaches rely on LLM fine-tuning, incurring training cost and limiting adaptability to evolving tool sets.
Our work takes a different path: we offload planning to a lightweight external module and use context-constrained execution to reduce the per-step reasoning burden on off-the-shelf SLMs, enabling competitive performance without any LLM fine-tuning.
3 Methodology
3.1 Framework Overview
Figure [2](#S3.F2) gives an overview of RETO.
At a high level, RETO separates global structure from local execution for small LM agents.
It consists of three components:
(1) Learn: Layer Execution Sketch, which predicts a coarse execution layer for each tool, providing a global scaffold without enumerating all pairwise edges;
(2) Execute: Context-Constrained Invocation, which runs tools layer by layer and restricts the SLM to tools in the current layer, keeping the effective context short; and
(3) Reflect and Repair: Local Correction, which monitors tool outputs with error checks and triggers local correction when a call fails or returns uninformative results.
This design moves global planning into a lightweight structural predictor, while the SLM focuses on short-horizon tool use with explicit failure handling.
3.2 Learn: Layer Execution Sketch
Multi-tool tasks often fail when the model violates prerequisite dependencies, causing downstream errors. Explicitly constructing a full dependency graph or complete plan is expensive and brittle in practice, requiring many fine-grained decisions. Instead, we assign each tool to an execution layer to form a coarse execution sketch. A tool in layer may depend on outputs from layers . During execution, the model fills tool arguments based on tool schemas and outputs from earlier layers. This enables fine-grained information flow without predicting pairwise dependency edges. Tools within a layer can be executed in parallel. Formally, given a user query and candidate tools , we predict an execution layer for each tool , where is the maximum number of layers. means is executed first in the coarse order, and means may depend on outputs from layers .
Input Representation.
We embed the query and each tool document into a shared -dimensional space using a pre-trained text encoder:
| (1) | ||||
| (2) |
where is a textualized tool document, formed by concatenating the tool name, description, and parameter schema (and optionally other metadata when available).
Layer Predictor.
We design a lightweight neural network that takes query and tool embeddings as input and predicts layer assignments. The model consists of three stages: (1) Projection. Since the query and tools play different semantic roles, we apply separate projections with LayerNorm and ReLU:
| (3) | ||||
| (4) |
where are learnable and denotes LayerNorm. We concatenate them into a sequence
| (5) |
(2) Contextual Encoding. The concatenated sequence is processed by a Transformer Encoder, allowing the query and tools to exchange information via self-attention:
| (6) | ||||
| (7) |
Through this mechanism, each tool representation integrates task semantics from the query and functional information from other candidate tools, enabling the model to capture dependency cues among tools under the query.
(3) Ordinal Output.We cast layer prediction as ordinal regression (Cao et al., [2020](#bib.bib54))
to exploit the inherent layer order. For layers, we predict
cumulative probabilities:
| (8) |
where is the sigmoid, is shared across thresholds, and are learnable biases. We decode the layer by
| (9) |
Training.
Given ground-truth layer , we construct cumulative binary labels and minimize weighted binary cross-entropy:
| (10) |
where balances class imbalance at each threshold.
Inference.
The predicted layer follows Eq. ([9](#S3.E9)), counting exceeded thresholds. The predictor additionally enforces schema-level constraints: if a tool’s required input matches another tool’s output type in the available document, it is shifted to a subsequent layer to ensure valid execution order.
3.3 Execute: Context-Constrained Invocation
Given the layer assignments from §[3.2](#S3.SS2), we execute tools one layer at a time.
At layer , the LM only sees the schemas of the current-layer tools and the tool outputs from earlier layers, along with brief execution instructions.
This design prevents out-of-turn tool calls, keeps the effective context compact, and breaks multi-step reasoning into per-layer decisions. It is particularly helpful for small models in long-context settings (Liu et al., [2024](#bib.bib50); Levy et al., [2024](#bib.bib51)).
Execution Protocol.
Let denote the set of tools assigned to layer . For each layer , we construct a prompt that includes the current layer index (out of ), the schemas of , the original query, prior tool outputs, and brief execution instructions. The LM generates tool calls with arguments; we execute same-layer calls in parallel under the layer plan and append observations for subsequent layers. We enforce the constraint by omitting tools outside from the tool list, preventing out-of-turn calls by construction. The LM retains autonomy over how many times to call each tool and with what arguments. The layer assignment only determines when a tool becomes available to the LM agent.
Answer Synthesis.
Finally, after all layers execution is complete, we force a dedicated Finish call. The LLM receives an execution summary of all observations and must produce a final_answer grounded only in this summary. We explicitly instruct: “if required information is missing, acknowledge the limitation.” This prevents hallucinating results for tools that failed or were never executed.
3.4 Reflect and Repair: Local Correction
Even with a correct tool plan, small LMs often produce invalid tool calls: arguments may miss required fields, contain type or enum errors, or trigger runtime failures under hidden constraints (e.g., unexpected keyword arguments, validation errors). If such calls are executed as-is, they pollute the context with noisy error messages and make later reasoning depend on corrupted observations. To both prevent this pollution and salvage useful calls when possible, we wrap each tool call in a reflect–then–repair mechanism that (i) validates arguments against tool schemas before execution and (ii) performs error-driven local repair under a fixed budget. This localized reflection avoids costly trajectory-level retries while preventing error accumulation across layers.
Schema Gate.
For each tool , we build a JSON-schema index from its ToolBench specification (required keys, top-level properties, primitive types, and enums). Given a tool call with arguments , the Schema Gate applies a lightweight validator:
| (11) |
where Valid checks that all required keys are present and that the types and enum values of existing keys match the schema. Unknown top-level keys are simply dropped. Accepted calls are executed normally; rejected calls are skipped and passed to the repair module together with a structured error report (missing fields, type errors, enum violations, and dropped keys). This gate removes many systematic argument errors before they reach the environment, while remaining cheap and tool-agnostic.
Repair mechanism.
As shown in algorithm [1](#alg1). For each rejected or failed call with schema and diagnosis , we apply an error-driven repair operator under a per-trajectory budget . first tries cheap deterministic edits (e.g., removing unexpected keys). If these fail and the diagnosis suggests argument issues, it falls back to an LLM-driven repair based on the error message. All repaired calls are re-validated by the Schema Gate before execution. Once is exhausted, errors are logged but not retried.
Compared to naive retries, this reflect–then–repair operator isolates errors at individual tool calls rather than entire trajectories. Repairs are kept off the main dialogue trace, preventing context pollution and avoiding global re-planning.
4 Experiment
4.1 Experiment Settings
Datasets.
We evaluate on StableToolBench (Guo et al., [2024](#bib.bib13)), which provides a caching system and API simulator to mitigate instability of real-time APIs while preserving the task distribution of ToolBench (Qin et al., [2023](#bib.bib3)). Test cases span three generalization dimensions: Inst. (unseen instructions, same tools), Tool (unseen tools, same category), and Cat. (unseen tools, unseen category). Task complexity varies across three scenarios: I1 (single-tool), I2 (intra-category multi-tool), and I3 (intra-collection multi-tool), with difficulty increasing from I1-Inst. to I3-Inst.
To train the layer predictor, we derive supervision from the training portion of ToolBench. We reuse the structured execution trajectories released with DTA-Tool (Zhu et al., [2025a](#bib.bib12)), mapping each tool call to a layer index based on its structure in the execution tree, and then split the resulting layer-labeled data into training, validation, and test sets for model selection.
Baselines and Models.
We compare three execution strategies: ReAct (Yao et al., [2022](#bib.bib4)),
DFSDT (Qin et al., [2023](#bib.bib3)), and our plan-then-execute approach.
To evaluate across model scales and training regimes, we test on:
(1) non-tool-tuned models: Qwen2.5-7B-Instruct (Yang et al., [2024](#bib.bib14))
and LLaMA-3.1-8B-Instruct (Meta AI, [2024](#bib.bib15));
(2) tool-tuned model: ToolLLaMA (Qin et al., [2023](#bib.bib3)), which is fine-tuned on the ToolBench training set for tool use; and
(3) closed-source models: GPT-3.5-0613 and GPT-3.5-1106, as a reference for proprietary model performance.
To further examine how SLM scale affects performance, we also evaluate Qwen2.5-3B/1.5B/0.5B-Instruct.
| Method | Backbone | Tool-tuned | I1-Inst. | I1-Tool | I1-Cat. | I2-Inst. | I2-Cat. | I3-Inst. | Avg. |
|---|---|---|---|---|---|---|---|---|---|
| Closed-source LLMs | |||||||||
| ReAct | GPT-3.5-0613 | – | 50.1±0.6 | 51.6±0.4 | 49.8±0.3 | 37.3±0.8 | 40.3±0.7 | 43.2±1.5 | 45.4 |
| ReAct | GPT-3.5-1106 | – | 49.8±1.2 | 51.3±1.3 | 40.1±0.3 | 39.8±1.2 | 49.2±0.7 | 59.6±0.8 | 48.3 |
| Open-source LLMs | |||||||||
| ReAct | ToolLLaMA-7B | ✓ | 31.5±0.8 | 34.0±0.4 | 39.5±0.5 | 25.5±0.4 | 34.5±0.8 | 32.8±0.0 | 33.0 |
| DFSDT | ToolLLaMA-7B | ✓ | 48.8±2.4 | 48.9±1.0 | 48.9±0.4 | 37.3±0.4 | 45.8±1.0 | 53.0±2.0 | 47.1 |
| ReAct | LLaMA-3.1-8B | ✗ | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0 |
| DFSDT | LLaMA-3.1-8B | ✗ | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0±0.0 | 0.0 |
| RETO (Ours) | LLaMA-3.1-8B | ✗ | 14.0±0.8 | 17.4±1.6 | 22.9±0.6 | 16.7±0.8 | 16.8±1.3 | 14.5±1.9 | 17.1 |
| ReAct | Qwen2.5-7B | ✗ | 8.4±0.3 | 11.0±0.3 | 8.1±0.3 | 11.3±0.8 | 17.2±0.8 | 1.1±0.8 | 9.5 |
| DFSDT | Qwen2.5-7B | ✗ | 5.7±0.3 | 15.3±0.3 | 10.1±0.3 | 17.1±0.8 | 24.7±0.8 | 0.5±0.4 | 12.2 |
| RETO (Ours) | Qwen2.5-7B | ✗ | 50.3±0.5 | 50.9±0.6 | 54.4±1.0 | 46.5±1.8 | 52.4±1.1 | 42.5±0.7 | 49.5 |
Evaluation Metrics.
Following the StableToolBench work (Guo et al., [2024](#bib.bib13)), we report two metrics: (1) Solvable Pass Rate (SoPR): the percentage of
solvable tasks that the model successfully completes, as judged by
GPT-4o; and (2) Solvable Win Rate (SoWR): the percentage of
tasks where the model’s output is preferred over a GPT-3.5-0613+ReAct
baseline, using GPT-4o as the judge. SoWR is computed as
, where
, , and denote the
number of wins, ties, and total comparisons, respectively. We average
results over three runs to mitigate the variance from LLM-based automatic evaluation.
4.2 Experimental Results
4.2.1 Overall performance
This experiment aims to answer: Whether our method can lift non-tool-tuned SLMs to a Solvable Pass Rate comparable to tool-tuned and proprietary agents.
To this end, we evaluate three reasoning methods (ReAct, DFSDT, and our RETO) across different model backbones, including non-tool-tuned open-source models (Qwen2.5-7B, LLaMA-3.1-8B), a tool-tuned model (ToolLLaMA-7B), and closed-source models (GPT-3.5). We report SoPR evaluated by GPT-4o with three independent runs (Table [1](#S4.T1)).
We observe three findings.
First, traditional methods perform poorly on non-tool-tuned models: ReAct and DFSDT yield low SoPR on both backbones.
Second, RETO improves non-tool-tuned models, lifting
Qwen2.5-7B from 12.2% (DFSDT) to 49.5%, and LLaMA-3.1-8B from 0.0% to 17.1%.
Third, RETO on Qwen2.5-7B surpasses tool-tuned ToolLLaMA-7B and exceeds both GPT-3.5 ReAct baselines.
The key driver is that ReAct and DFSDT
require a single model to handle long-horizon reasoning in one trace,
where early mistakes cascade through subsequent steps.
RETO separates these concerns: a planner provides a coarse
dependency sketch, and the LM operates within this scaffold with
schema checks and local repair. This turns entangled reasoning into
short, well-scoped decisions that match the effective context window
of non-tool-tuned SLMs.
In summary, RETO enables non-tool-tuned open-source models to reach performance comparable to tool-tuned counterparts and proprietary LLMs.
4.2.2 Answer quality evaluation
This experiment aims to answer: whether our method delivers tool-tuned-level answer quality from non-tool-tuned SLMs.
To this end, we follow the StableToolBench protocol to report Solvable Win Rate. For each test instance, GPT-4o compares a model’s answer with that of GPT-3.5-0613 + ReAct. We evaluate three configurations: ToolLLaMA-7B + DFSDT (tool-tuned), Qwen2.5-7B + RETO and LLaMA-3.1-8B + RETO.
As shown in Figure [3](#S4.F3), non-tool-tuned Qwen2.5-7B with RETO is comparable to tool-tuned ToolLLaMA-7B + DFSDT in average win rate, with both configurations exceeding 50% parity on several subsets. LLaMA-3.1-8B, however, lags behind. (For details before merging the tie label, please refer to Appendix [A.5](#A1.SS5).)
These results indicate that RETO helps bridge the gap between non-tool-tuned and tool-tuned SLMs. The performance gap between Qwen2.5-7B and LLaMA-3.1-8B may stem from
differences in instruction-following ability, as faithful execution of the execution sketch depends on the backbone’s capability to follow instructions.
In summary, our method lifts capable non-tool-tuned SLMs to match tool-tuned baselines in answer quality when evaluated against GPT-3.5-0613.
4.2.3 Ablation: backbone size
This experiment aims to answer: whether our framework remains effective as model size decreases?
To this end, we evaluate our framework across four backbone sizes from the Qwen2.5 series (0.5B, 1.5B, 3B, and 7B). We report the solvable pass rate on six test sets.
As shown in Figure [4](#S4.F4), performance scales with model size, but the degradation is gradual. The 7B model achieves the best average SoPR, with the 3B model close behind. The 1.5B model shows moderate drops but remains functional across most subsets. The 0.5B model, however, struggles noticeably, particularly on harder tasks (I2, I3).
The underlying reason is that RETO reduces the reasoning burden at each step by constraining the action space and limiting context to layer-relevant information. Local repair further compensates for mistakes and drift that smaller models are more prone to make. Together, these mechanisms allow smaller models to remain effective and robust within well-scoped decisions.
In summary, our framework maintains strong performance from 7B down to 1.5B, with noticeable degradation only at 0.5B. This suggests that practitioners can deploy smaller backbones to reduce cost while preserving most accuracy.
4.2.4 Ablation: execution sketch and repair
This experiment aims to answer: whether execution sketch and repair individually contribute to performance?
To this end, we ablate two components. w/o Execution Sketch exposes all tools rather than layer-constrained subsets. w/o Repair removes the Reflect-and-Repair module. We report SoPR on three representative subsets.
As shown in Figure [5](#S4.F5), both components contribute to performance. Removing the execution sketch or repair module causes a noticeable drop in SoPR, indicating that both modules are necessary for the full method’s effectiveness.
The underlying driver is that the execution sketch constrains the action space to a subset of relevant tools at each step, reducing the chance of selecting and invoking incorrect tools. The Reflect-and-Repair module allows the model to repair failed calls and salvage useful calls when possible, rather than letting errors propagate.
In summary, both the execution sketch and repair module contribute to the method’s effectiveness. The ablation confirms that constraining the search space and enabling failure repair are necessary for the robust performance of our methods.
| Total Tokens | Steps | |||||
|---|---|---|---|---|---|---|
| Test Set | DFSDT | RETO | DFSDT | RETO | ||
| I1-Inst. | 19586 | 5952 | -69.6% | 7.4 | 4.4 | -40.5% |
| I1-Tool | 20911 | 6009 | -71.3% | 6.8 | 4.0 | -41.2% |
| I1-Cat. | 12534 | 3022 | -75.9% | 5.6 | 2.7 | -51.8% |
| I2-Inst. | 23587 | 6530 | -72.3% | 8.5 | 4.5 | -47.1% |
| I2-Cat. | 17236 | 4885 | -71.7% | 6.9 | 3.2 | -53.6% |
| I3-Inst. | 23080 | 3507 | -84.8% | 9.2 | 2.8 | -69.6% |
4.2.5 Efficiency analysis
This experiment aims to answer: whether our framework improves inference efficiency over DFSDT?
To this end, we compare ToolLLaMA + DFSDT with Qwen2.5-7B + RETO in token consumption and inference steps. We exclude ReAct as efficiency comparisons are meaningful only between methods with comparable success rates.
As shown in Table [2](#S4.T2),
our method consistently reduces both token usage and step count across all test sets, with larger reductions on more complex tasks.
The reduction stems from two factors. First, separating planning from execution keeps each prompt short: the caller LM sees only the current-layer context rather than the accumulated history. Second, the pre-computed execution layer eliminates exploratory steps and enables parallel invocation of independent tools within the same layer.
In summary, our method achieves comparable accuracy to tool-tuned baselines while substantially reducing both token consumption and inference steps.
4.2.6 Parameter sensitivity analysis
This experiment aims to answer: how performance varies with layer prediction hyperparameter choices?
To this end, we vary the projection dimension from 64 to 1024 with per-head dimension fixed at 8, and vary the per-head dimension from 2 to 32 with projection dimension fixed at 256. We report SoPR on I1-Tool and I3-Inst. datasets.
Figure [6](#S5.F6) shows that performance remains stable across a wide range of hyperparameter settings. Varying from 64 to 1024 or from 2 to 32 produces only minor fluctuations in SoPR on both I1-Tool and I3-Inst. Neither extremely small nor large values cause significant degradation.
The underlying driver is that the layer predictor mainly needs to capture coarse tool dependencies, and moderate representational capacity is sufficient for producing a useful execution scaffold.
In summary, the predictor is robust to hyperparameter choices.
4.2.7 Case study
The quantitative results above show what performance gains RETO achieves; we now examine why baselines fail.
Figure [7](#S5.F7) presents a representative example where Qwen2.5-7B with ReAct fails completely, while the same model with
RETO succeeds. Without layer constraints, the SLM suffers from format collapse and response hallucination, producing fabricated tool responses before any API is actually called. This matches the
failure pattern illustrated in Figure [1](#S0.F1): fluent
but ungrounded outputs that cascade into unrecoverable states.
In contrast, RETO’s layer-wise execution restricts each step to a small subset of tools, reducing decision complexity and ensuring grounded responses. Detailed case study traces are provided in Appendix [A.11](#A1.SS11).
5 Conclusion
In this paper, we propose RETO, a layered tool invocation framework that revisits tool invocation from the perspective of tool orchestration, designed to decouple global organization from local tool calls and achieve robust execution with reduced complexity and overhead. Concretely, RETO first encodes the task query and tool descriptions and predicts a coarse-grained layer assignment for each tool. This layered structure restricts the tools considered at each step through context constraints and keeps the language model focused on a smaller subset of tools and observations, reducing execution complexity. During execution, the model only chooses among tools in the current layer while conditioning on outcomes from previous layers, so that high-level dependencies are respected without requiring a fully specified plan. On top of this, a reflective error-recovery module performs error-based repair for individual tool calls, improving robustness by keeping failures local to the offending call. Extensive experiments show that equipping an untuned 7B backbone with RETO achieves solvable pass rates close to domain-specific tool-tuned agents and proprietary agents, while using substantially fewer tokens. Ablation studies further confirm that both the layered execution structure and reflective error recovery are necessary to sustain these robustness and efficiency gains. In future work, we aim to improve the quality of induced execution structures and explore tighter integration with lightweight training signals. Another promising direction is to push RETO to smaller and more resource-constrained language models, enabling reliable tool orchestration in broader deployment settings.
Impact Statement
This paper presents work whose goal is to advance the field of Machine Learning. There are many potential societal consequences of our work, none which we feel must be specifically highlighted here.
References
-
Small language models are the future of agentic ai.
arXiv preprint arXiv:2506.02153.
Cited by:
[§1](#S1.p1.1),[§2](#S2.SS0.SSS0.Px3.p1.1). -
Rank consistent ordinal regression for neural networks with application to age estimation.
Pattern Recognition Letters 140, pp. 325–331.
Cited by:
[§3.2](#S3.SS2.SSS0.Px2.p2.2). -
Advancing tool-augmented large language models: integrating insights from errors in inference trees.
Advances in Neural Information Processing Systems 37, pp. 106555–106581.
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1). -
Anytool: self-reflective, hierarchical agents for large-scale api calls.
arXiv preprint arXiv:2402.04253.
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1). -
Stabletoolbench: towards stable large-scale benchmarking on tool learning of large language models.
arXiv preprint arXiv:2403.07714.
Cited by:
[§A.1](#A1.SS1.p2.2),[§A.4](#A1.SS4.p1.1),[Table 3](#A1.T3),[Table 3](#A1.T3.3.2),[§4.1](#S4.SS1.SSS0.Px1.p2.4),[§4.1](#S4.SS1.p1.1). -
Metatool benchmark for large language models: deciding whether to use tools and which to use.
arXiv preprint arXiv:2310.03128.
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1). -
NaviAgent: bilevel planning on tool dependency graphs for function calling.
arXiv preprint arXiv:2506.19500.
Cited by:
[§1](#S1.p1.1). -
An llm compiler for parallel function calling.
In Forty-first International Conference on Machine Learning,
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1). -
Same task, more tokens: the impact of input length on the reasoning performance of large language models.
arXiv preprint arXiv:2402.14848.
Cited by:
[§3.3](#S3.SS3.p1.1). -
Lost in the middle: how language models use long contexts.
Transactions of the Association for Computational Linguistics 12, pp. 157–173.
Cited by:
[§3.3](#S3.SS3.p1.1). -
Chameleon: plug-and-play compositional reasoning with large language models.
Advances in Neural Information Processing Systems 36, pp. 43447–43478.
Cited by:
[§1](#S1.p1.1). -
Toolverifier: generalization to new tools via self-verification.
In Findings of the Association for Computational Linguistics: EMNLP 2024,
pp. 5026–5041.
Cited by:
[§1](#S1.p1.1). -
Introducing llama 3.1: our most capable models to date.
External Links:
[Link](https://ai.meta.com/blog/meta-llama-3-1/)Cited by:[§4.1](#S4.SS1.SSS0.Px1.p1.1). -
Gorilla: large language model connected with massive apis.
Advances in Neural Information Processing Systems 37, pp. 126544–126565.
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1). -
The berkeley function calling leaderboard (bfcl): from tool use to agentic evaluation of large language models.
In Forty-second International Conference on Machine Learning,
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1). -
Toolllm: facilitating large language models to master 16000+ real-world apis.
arXiv preprint arXiv:2307.16789.
Cited by:
[§A.1](#A1.SS1.p2.2),[§A.3](#A1.SS3.p1.1),[§1](#S1.p1.1),[§1](#S1.p3.1),[§2](#S2.SS0.SSS0.Px1.p1.1),[§4.1](#S4.SS1.SSS0.Px1.p1.1),[§4.1](#S4.SS1.p1.1). -
Toolformer: language models can teach themselves to use tools.
Advances in Neural Information Processing Systems 36, pp. 68539–68551.
Cited by:
[§1](#S1.p1.1),[§2](#S2.SS0.SSS0.Px1.p1.1). -
Small llms are weak tool learners: a multi-llm agent.
arXiv preprint arXiv:2401.07324.
Cited by:
[§2](#S2.SS0.SSS0.Px3.p1.1). -
Hugginggpt: solving ai tasks with chatgpt and its friends in hugging face.
Advances in Neural Information Processing Systems 36, pp. 38154–38180.
Cited by:
[§1](#S1.p3.1),[§2](#S2.SS0.SSS0.Px2.p1.1). -
Reflexion: language agents with verbal reinforcement learning.
Advances in Neural Information Processing Systems 36, pp. 8634–8652.
Cited by:
[§2](#S2.SS0.SSS0.Px2.p1.1). -
Toolalpaca: generalized tool learning for language models with 3000 simulated cases.
arXiv preprint arXiv:2306.05301.
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1). -
Plan-and-solve prompting: improving zero-shot chain-of-thought reasoning by large language models.
arXiv preprint arXiv:2305.04091.
Cited by:
[§1](#S1.p3.1),[§2](#S2.SS0.SSS0.Px2.p1.1). -
Optimizing aesthetic perception through human-ai teaming for subtle dimension identification in art annotation.
IEEE Transactions on Learning Technologies.
Cited by:
[§A.3](#A1.SS3.p1.1). -
Toolgen: unified tool retrieval and calling via generation.
arXiv preprint arXiv:2410.03439.
Cited by:
[§2](#S2.SS0.SSS0.Px3.p1.1). -
Beyond react: a planner-centric framework for complex tool-augmented llm reasoning.
arXiv preprint arXiv:2511.10037.
Cited by:
[§A.3](#A1.SS3.p1.1). -
GAP: graph-based agent planning with parallel tool use and reinforcement learning.
arXiv preprint arXiv:2510.25320.
Cited by:
[§2](#S2.SS0.SSS0.Px3.p1.1). -
Can graph learning improve planning in llm-based agents?.
Advances in Neural Information Processing Systems 37, pp. 5338–5383.
Cited by:
[§2](#S2.SS0.SSS0.Px2.p1.1). -
Rewoo: decoupling reasoning from observations for efficient augmented language models.
arXiv preprint arXiv:2305.18323.
Cited by:
[§2](#S2.SS0.SSS0.Px2.p1.1). -
Qwen2.5 technical report.
arXiv preprint arXiv:2412.15115.
Cited by:
[§4.1](#S4.SS1.SSS0.Px1.p1.1). -
React: synergizing reasoning and acting in language models.
In The eleventh international conference on learning representations,
Cited by:
[§1](#S1.p3.1),[§2](#S2.SS0.SSS0.Px2.p1.1),[§4.1](#S4.SS1.SSS0.Px1.p1.1). -
Divide-then-aggregate: an efficient tool learning method via parallel tool invocation.
arXiv preprint arXiv:2501.12432.
Cited by:
[§A.1](#A1.SS1.p2.2),[§A.3](#A1.SS3.p1.1),[§1](#S1.p3.1),[§2](#S2.SS0.SSS0.Px3.p1.1),[§4.1](#S4.SS1.p1.1). -
Where llm agents fail and how they can learn from failures.
arXiv preprint arXiv:2509.25370.
Cited by:
[§1](#S1.p1.1). -
Toolchain*: efficient action space navigation in large language models with a* search.
arXiv preprint arXiv:2310.13227.
Cited by:
[§2](#S2.SS0.SSS0.Px1.p1.1).
Appendix A Appendix
A.1 Experimental Settings
All experiments are conducted on an Ubuntu 22.04.5 LTS operating system, powered by an AMD Ryzen Threadripper PRO 7965WX 24-core processor, using Python 3.12.7 and PyTorch 2.5.1 as the framework.
For text encoding, we use ToolBench_IR_bert_based_uncased (Qin et al., [2023](#bib.bib3)) with embedding dimension 768. The layer predictor uses a projection dimension of 256, 8 attention heads, 2 Transformer layers, and a dropout rate of 0.1. We derive layer supervision from the structured execution trajectories released with DTA-Tool (Zhu et al., [2025a](#bib.bib12)), mapping each tool call to a layer index. From the original 21,342 trajectories, we extract 5,035 samples with multi-layer annotations and split them into train/val/test sets (80/10/10), training for 10 epochs with a learning rate of 1e-3 and selecting the best model based on validation performance.
For ReAct and DFSDT experiments, we follow the settings in (Guo et al., [2024](#bib.bib13)). For tool responses, we use the authors’ MirrorAPI LLM with cached results for efficiency and reproducibility, as recommended.
In addition, we set the maximum number of layers and repair budget for all experiments.
A.2 Limitations
Our framework avoids reconstructing the entire planning trajectory and instead performs layer-constrained execution with local, error-driven repair. As a result, it may struggle when failures require global revisions (e.g., earlier high-level decisions must be reconsidered) rather than localized argument or tool-selection fixes. In addition, our current recovery focuses on API invocation and schema/content checks; richer diagnosis signals and more principled rollback policies could further improve robustness without incurring substantial tuning or token overhead. Finally, we rely on the provided tool set and tool documentation; integrating tool retrieval and document refinement into the orchestration loop is a promising direction.
A.3 Extended Discussion on Related Work
We adopt DFSDT with ToolLLaMA (Qin et al., [2023](#bib.bib3)), which is the standard baseline on StableToolBench for tool-tuned tool orchestration. We compare against it to show that non-tool-tuned SLMs can reach comparable performance through orchestration design alone.
Our work relates to but differs from recent fine-tuning approaches. DTA-Tool (Zhu et al., [2025a](#bib.bib12)) fine-tunes LLMs on DAG-structured trajectories for layer-wise execution. We derive layer supervision from their released data, but take a different path: our layer predictor is external and lightweight, leaving the SLM frozen. Concurrent work by Wei et al. (Wei et al., [2025](#bib.bib63)) trains a dedicated LLM Planner via SFT and RL (Wang et al., [2026](#bib.bib64)), paired with GPT-4o as executor. In contrast, we target non-tool-tuned SLMs as a robust executor with explicit error recovery, prioritizing lightweight deployment and avoiding complex and costly training requirements. Both fine-tuning directions remain compatible with our framework and merit future exploration to further improve effectiveness in resource-constrained settings.
A.4 Dataset Statistics
Table [3](#A1.T3) summarizes the dataset statistics from
StableToolBench (Guo et al., [2024](#bib.bib13)). We use the Solvable subset for evaluation.
[2024](#bib.bib13))).
| I1-I | I1-C | I1-T | I2-I | I2-C | I3-I | Total | |
|---|---|---|---|---|---|---|---|
| Full | 200 | 200 | 200 | 200 | 200 | 100 | 1,100 |
| Solvable | 163 | 153 | 158 | 106 | 124 | 61 | 765 |
A.5 SoWR results before merging the tie label
Table [4](#A1.T4) reports the raw win/lose/tie counts
underlying the SoWR results in Figure [3](#S4.F3). The tie counts are
merged as half-wins when computing the final SoWR metric.
| LLaMA-3.1-8B | Qwen2.5-7B | ToolLLaMA-7B | |||||||
| Test Set | Win | Lose | Tie | Win | Lose | Tie | Win | Lose | Tie |
| I1-Inst. | 41 | 110 | 12 | 74 | 88 | 1 | 95 | 68 | 0 |
| I1-Tool | 40 | 100 | 18 | 69 | 85 | 4 | 83 | 75 | 0 |
| I1-Cat. | 59 | 86 | 8 | 95 | 57 | 1 | 81 | 72 | 0 |
| I2-Inst. | 33 | 57 | 16 | 60 | 45 | 1 | 65 | 41 | 0 |
| I2-Cat. | 32 | 62 | 30 | 71 | 45 | 8 | 65 | 58 | 1 |
| I3-Inst. | 18 | 43 | 0 | 25 | 35 | 1 | 32 | 29 | 0 |
A.6 Prompt
Allowed tools this step: {tool_names}
Rules:
- If a tool requires an ID (e.g., title_id, peopleid), you MUST first call a search tool to find the correct ID.
- Do NOT hallucinate or make up IDs. Only use IDs returned from previous tool calls.
- If no search tool is available in this step and you don’t have a valid ID, skip that tool.
You MUST respond in this exact format:
Action: <tool_name>
Action Input: <JSON arguments>
All tool executions are complete.
=== EXECUTION SUMMARY ===
{executed_summary}
=========================
You MUST call the tool ‘Finish’ exactly once.
Rules:
- Do NOT call any other tool.
- Output exactly TWO lines in the following format.
- Action must be exactly: Finish
- Action Input must be a JSON object with keys: return_type, final_answer
- final_answer MUST be grounded ONLY in EXECUTION SUMMARY; if missing, say the limitation.
FORMAT (exactly two lines):
Action: Finish
Action Input: {"return_type":"give_answer","final_answer":"..."}
Note: {executed_summary} is dynamically generated from the tool execution history, listing each tool name and its returned result.
You must fix the arguments for tool: {tool_name}
Rules:
- You MUST output exactly ONE tool call.
- The tool name MUST be exactly: {tool_name}
- The arguments MUST be a JSON object.
- Only use keys defined in the schema.
- Do NOT call Finish.
- Do NOT output any plain text.
=== TOOL SCHEMA ===
{schema_summary}
===================
Previous arguments:
{prev_args_json}
Tool execution error:
{tool_error_text}
Now output ONLY in this JSON format:
{"tool_calls":[{"name":"{tool_name}","arguments":{...}}]}
Note: {schema_summary} contains the tool’s parameter schema, including required fields and types. {tool_error_text} is the actual error message returned from the failed tool execution.
A.7 Error Recovery Example
Query: “Fetch comedy movies from 2000-2019 using the Bollywood Recommendations tool, and find similar movies to Titanic.”
Analysis: The LLM correctly interprets the API’s year format constraint and converts the year range “2000-2019” to a valid 4-digit year “2000”. This demonstrates the error recovery module’s ability to understand natural language error messages and generate appropriate parameter fixes without human intervention.
A.8 Layer Prediction Examples
A.9 Complete Execution Trace Example
Query: “I’m planning a surprise birthday party for my best friend and I want to create personalized QR code invitations for the guests. Can you generate QR codes with unique data for each guest? Additionally, I need to research popular keywords related to party planning and decorations to optimize my event website.”
Analysis: This example demonstrates a complete two-layer execution. Layer 1 performs keyword research while Layer 2 generates a QR code. Since these tools have no data dependencies, they could potentially be executed in parallel. The final step synthesizes results from both tools into a coherent response.
A.10 Case Study
Query: “I’m writing an article about the benefits of exercise for mental health. Retrieve web search results for scientific studies on this topic using the Bing Search API. Additionally, find relevant images to accompany the article using the Image Search API.”
Analysis: This example demonstrates a three-layer execution. Layer 1 retrieves scientific articles from NCBI. Layer 2 finds relevant images from Mind.org and WHO. Layer 3 (email search) is automatically skipped as irrelevant. The final step synthesizes results into a coherent response with source URLs.
A.11 Failure Analysis: Baseline vs. RETO
Query: “I want to surprise my family by tracking the delivery of the gift package with the tracking ID 6045e2f44e1b233199a5e77a. Can you provide me with the current status? Also, fetch the relevant information for the Pack & Send reference number ’ReferenceNumberHere’. Additionally, check the health of the suivi-colis API.”
A.11.1 Baseline Failure (Qwen2.5-7B + ReAct)
Thought: I will check the health... Action Action Input...Human:
Thought: I have received the data... Action: Finish
"The status is delivered...package is on its way...API is healthy."Human:... Observation: {"error": "Tool input parse error..."} Result: The entire hallucinated sequence was produced in one autoregressive pass. No API was actually called; all “results” (delivered, on its way, healthy) are fabricated. Step 2: Recovery Attempt (Same Pattern + Infinite Loop) Thought: The API call failed, I will try the next step. Action: api_tracking_for_pack_send Action Input: {"reference": "ReferenceNumberHere"}Thought: Same hallucination pattern, plus a new failure mode—infinite restart loop:
Thought: The Pack & Send API call failed... Action: health_for_suivi_colis
Thought: The suivi-colis API health check was successful, but I couldn’t
get the tracking data... I will inform the user about the failure.
Action: Finish "Unable to retrieve the tracking data..."
Assistant: I give up and restart.
Assistant: I give up and restart.
... (repeated 30+ times within single output) Observation: {"error": "Tool input parse error..."} Note: The model claims “health check was successful” despite no API being executed. Steps 3 to End: Unrecoverable Same pattern repeats until max limit is reached. Without external constraints to enforce step-by-step execution, the model continues to “predict” future turns rather than execute and wait for actual API responses. Once hallucination begins, it cascades uncontrollably with no self-correction mechanism. Final Status: Failed APIs executed: 0
Analysis: The baseline failure illustrates why unconstrained tool execution is fundamentally brittle for multi-tool tasks. Facing all multiple tools document simultaneously with no structural guidance, the model attempts to “shortcut” the entire execution by predicting future turns autoregressively—fabricating both intermediate results and final answers without actual API grounding. This produces fluent but entirely fictional outputs (e.g., “delivered” vs. real status “booked in Eldoret”). The failure is not recoverable because each hallucinated turn compounds the next, and the model has no mechanism to verify its predictions against real observations. In contrast, RETO’s layer-wise constraints reduce the per-step decision space, while the recovery mechanism and parallel execution help maintain a simple, grounded, and effective tool invocation trajectory.
A.11.2 RETO Success (Qwen2.5-7B + RETO)
Observation: Each step is constrained to 2–3 allowed tools. The model executes one tool, waits for the actual response, then proceeds to the next layer. The final answer is grounded exclusively in real observations—correctly reporting “booked in Eldoret, pending in Nairobi” (matching the API response) and honestly acknowledging that Pack & Send tracking was not found.
Available APIs (7): get_tracking_data_for_create_container_tracking, api_tracking_for_pack_send, health_for_suivi_colis, latest_for_suivi_colis, all_for_suivi_colis, il_for_turkey_postal_codes, parse_for_gs1parser
Relevant APIs (3): get_tracking_data_for_create_container_tracking, api_tracking_for_pack_send, health_for_suivi_colis