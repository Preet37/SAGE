# Source: https://aclanthology.org/2025.emnlp-industry.149.pdf
# Title: [PDF] VESTABENCH: An Embodied Benchmark for Safe Long-Horizon Planning Under Multi-Constraint and Adversarial Settings
# Fetched via: search
# Date: 2026-04-10

## VestaBench: An Embodied Benchmark for Safe Long-Horizon Planning Under Multi-Constraint and Adversarial Settings
##### Abstract
Large language models (LLMs) are applied to reasoning and (automated) planning across diverse domains, from travel itineraries to embodied AI tasks.
However, concerns have been raised about their suitability for long-horizon tasks involving multiple constraints, as they are prone to hallucinations, particularly in adversarial scenarios.
Safety reasoning also becomes critical for embodied AI agents, which interact with their physical environments to complete tasks on behalf of humans.
However, existing (safety) benchmarks fail to represent a diverse range of multi-constraint tasks that require long-horizon planning with a focus on safety.
To address this, we propose VESTABENCH, a benchmark curated using VirtualHome and BEHAVIOR-100.
Our VESTABENCH includes (1) tasks that can be achieved safely under adversarial and multi-constraint settings, as well as (2) adversarial instructions that the agent must avoid.
Our experiments with state-of-the-art LLM-based baselines reveal that they perform poorly against our tasks, not only achieving low success rates but also suffering significantly compromised safety outcomes.
This observation reinforces the limitations of LLMs in generating safe plans when faced with adversarial settings or instructions.
Finally, we believe that our findings benefit the research and industry communities.- **Anthology ID:**
2025.emnlp-industry.149
- **Volume:**
Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track
- **Month:**
November
- **Year:**
2025
- **Address:**
Suzhou (China)
- **Editors:**
Saloni Potdar, Lina Rojas-Barahona, Sebastien Montella
- **Venue:**
EMNLP
- **SIG:**
- **Publisher:**
Association for Computational Linguistics
- **Note:**
- **Pages:**
2122–2145
- **Language:**
- **URL:**
https://aclanthology.org/2025.emnlp-industry.149/
- **DOI:**
10.18653/v1/2025.emnlp-industry.149
- **Cite (ACL):**
Tanmana Sadhu, Yanan Chen, and Ali Pesaranghader.
2025. VestaBench: An Embodied Benchmark for Safe Long-Horizon Planning Under Multi-Constraint and Adversarial Settings.
In *Proceedings of the 2025 Conference on Empirical Methods in Natural Language Processing: Industry Track*, pages 2122–2145, Suzhou (China).
Association for Computational Linguistics.
- **Cite (Informal):**
VestaBench: An Embodied Benchmark for Safe Long-Horizon Planning Under Multi-Constraint and Adversarial Settings (Sadhu et al., EMNLP 2025)
- **PDF:**
https://aclanthology.org/2025.emnlp-industry.149.pdf

November 4-9, 2025 ©2025 Association for Computational Linguistics
VESTABENCH: An Embodied Benchmark for Safe Long-Horizon Planning
Under Multi-Constraint and Adversarial Settings
Tanmana Sadhu*, Yanan Chen*, and Ali Pesaranghader*, †
LG Electronics, Toronto AI Lab, Toronto, Canada
{tanmana.sadhu, yanan.chen, ali.pesaranghader}@lge.com
Abstract
Large language models (LLMs) are applied to
reasoning and (automated) planning across di-
verse domains, from travel itineraries to em-
bodied AI tasks. However, concerns have been
raised about their suitability for long-horizon
tasks involving multiple constraints, as they are
prone to hallucinations, particularly in adver-
sarial scenarios. Safety reasoning also becomes
critical for embodied AI agents, which interact
with their physical environments to complete
tasks on behalf of humans. However, existing
(safety) benchmarks fail to represent a diverse
range of multi-constraint tasks that require
long-horizon planning with a focus on safety.
To address this, we propose VESTABENCH1, a
benchmark curated using VirtualHome (Puig
et al., 2018) and BEHAVIOR-100 (Srivastava
et al., 2021). Our VESTABENCH includes (1)
tasks that can be achieved safely under adver-
sarial and multi-constraint settings, as well as
(2) adversarial instructions that the agent must
avoid. Our experiments with state-of-the-art
LLM-based baselines reveal that they perform
poorly against our tasks, not only achieving low
success rates but also suffering significantly
compromised safety outcomes. This observa-
tion reinforces the limitations of LLMs in gen-
erating safe plans when faced with adversarial
settings or instructions. Finally, we believe that
our findings benefit the research and industry
communities.
1
Introduction
LLMs have recently been used to develop agents
capable of performing tasks in a wide range of do-
mains. Indeed, with the growing interest in Physi-
cal AI, LLM-based embodied agents have emerged
as a primary focus of research. In this context, an

…

to perform the task. While LLM agents show great
promise, a key question the community is now ad-
dressing is whether these agents can effectively
handle tasks that require long-horizon planning un-
der multi-constraint settings as well as adversarial
environments. This becomes even more crucial
when safety is an integral part of the planning pro-
cess, as agents are deployed in homes, restaurants,
and other real-world settings.
Most existing (embodied) benchmarks, such as
ALFWorld (Shridhar et al., 2021), are designed to
evaluate whether agents can generate executable
plans that successfully complete a given task. In
contrast, safety benchmarks typically focus on ad-
versarial instructions that the agent must avoid.
That is, most of them do not serve as planning
benchmarks that explicitly consider safety in task
execution. More importantly, these benchmarks
also overlook adversarial environments, which
commonly exist in the real world, that may con-
fuse the agent and potentially lead to hazardous
consequences. This highlights the importance of
safety benchmarks that support long-horizon, multi-
constraint planning under adversarial environments.
Table 1 compares the existing benchmarks.
To address this gap, we propose VESTABENCH,
a safety benchmark comprising household chores
that require multi-constraint planning across vary-
ing levels of complexity. The benchmark comprises
tasks set in either normal or adversarial environ-
ments, along with tasks that involve adversarial
instructions. To curate this benchmark, we used the
VirtualHome simulator (Puig et al., 2018) and the
BEHAVIOR-100 dataset (Srivastava et al., 2021),
resulting in two datasets: VestaBench-VH with
100 tasks, and VestaBench-B50 with 50 tasks. Ex-
amples 1 and 2 are representative tasks.
2122
Figure 1: Illustrative Example: This example illustrates (a) the environment state before and after executing an
LLM-generated plan, and (b) the step-by-step execution of actions from the ground-truth plan, for the given task
“Wash the salmon in the kitchen sink, heat it in the microwave, and place it on the kitchen table”.
We summarize our contributions below:
• We propose VESTABENCH, a benchmark for
household chores that supports long-horizon,
multi-constraint planning, and includes both
normal and adversarial environments, as well
as tasks with adversarial instructions.
• We explore two distinct planning strategies for
embodied tasks in our experiments: “one-go”
and “stepwise” planning.
• We evaluate the performance of state-of-the-
art planning methods, including ReAct, ReAct
+ Reflexion, and ReAct + Critic (i.e., LLM-as-
Judge), on VESTABENCH, and show that they
fail to complete a significant portion of tasks
both successfully and safely.
• We further assess the impact of replanning and
incorporating safety guidelines into prompts
on the performance of LLM-based agents.
2
VESTABENCH
Our VESTABENCH2 consists of two datasets, i.e.,
VestaBench-VH and VestaBench-B50, that are cu-
rated using the VirtualHome3 simulator (Puig et al.,
2018) and the BEHAVIOR-1004 benchmark (Sri-
vastava et al., 2021), respectively. Recall that our
benchmark comprises (1) short- to long-horizon
tasks that must be completed safely under multi-
2https://github.com/tanmana5/vestabench
3http://virtual-home.org/
4https://behavior.stanford.edu/behavior-100
constraint settings in normal or adversarial envi-
ronments, and (2) adversarial instructions that the
agent must avoid (only in VestaBench-VH). We

…

curs. This platform offers two simulators, namely,
the Unity Simulator and the Evolving Graph Sim-
ulator. Using the Evolving Graph Simulator, we
curated 100 tasks that incorporate safety constraints
related to physical, electrical, contamination, and
other types of hazards. Out of the 100 tasks, 70 are
set in either normal or adversarial environments,
and 30 are specifically designed around adversarial
instructions. Figure 2 shows the distribution of risk
categories in VestaBench-VH, in which a task can
be associated with more than one category. Finally,
Example 1 is a representative task from this dataset.
VestaBench-B50. We augmented 50 tasks, from
BEHAVIOR-100, with safety constraints. Since
the original BEHAVIOR lacks an action-transition
model layer, we borrow the simulator from Em-
bodied Agent Interface5 (Li et al., 2024b), which
provides this layer for BEHAVIOR. This simulator
offers 30 actions that agents can use to change the
states of objects. Example 2 presents a task drawn
from the dataset.
5https://embodied-agent-interface.github.io/
2123

…

Dist.: The percentages are calculated based on the total
number of category assignments across all tasks (i.e.,
132) but not the total number of tasks (i.e., 100). That
is, more than one category can be assigned to each task.
Table 1 compares the existing benchmarks with
VESTABENCH. Our benchmark is the only bench-
mark that offers multi-constraint tasks (or instruc-
tions) featuring both adversarial instructions as
well as adversarial environments with a guarantee
that the tasks can be completed safely. We provide
more details in Appendix A.
3
Framework
Problem Definition. Given a task instruction t, the
agent A is required to generate a plan P, defined as
a sequence of actions a1, a2, . . . , an, where each
action ai ∈A, to be executed by the simulator S.
After successful execution, the updated state of the
environment is represented as a graph G∗, which
is then evaluated against predefined success and
safety goals or criteria. A plan is considered both
successful and safe if these criteria are satisfied.
Planning Strategy. We consider “one-go” and
“stepwise” planning strategies, ideal for direct and
iterative planning, respectively, as shown in Figure
3. We describe each strategy in detail next.
One-go Planning. In the one-go planning approach,
the agent A generates a plan P, consisting of mul-
tiple actions, in a single attempt for a given in-
struction or task. Once the plan is generated, it is
executed by the simulator S. Upon successful exe-
cution, the environment graph G∗, which represents
the updated state of the environment, is evaluated.
Due to its straightforwardness, this planning strat-
egy is well-suited for direct planning scenarios.
Stepwise Planning. The agent A interacts with the
environment for n steps and m trials to finish the
task. At each step, the agent selects and executes
an action, aij, where i ∈m and j ∈n, which is
processed by the simulator S that returns an ob-
servation, oij, along with the updated state, Gij, of
the environment. This interaction continues for a
(pre-defined) number of steps, constituting a tra-
jectory τi = {a11, o11, a12, o12, ...}. At the end of
each trial, a critic J evaluates the (so far generated)
plan Pi and provides feedback, fi. This feedback
guides the agent in refining its strategy or decision-
making process for future trials. This process con-
tinues until the agent generates the “Done” action
or exhausts all trials. If the plan is executable, the
updated environment state, G∗, is passed on for
evaluation. This strategy suits iterative planning,
i.e., where interactions occur between the agent
and the simulator/environment.
Stepwise Planning
One-Go Planning
Instruction
VirtualHome
(EvolvingGraph)
Embodied Agent
Interface
(EvalGibson)
Plan 
 
Agent 
LLM (e.g., Qwen3)
If Yes:
 Graph 
 
Evaluation
Module
Successful?
Safe?
If No:
"Agent Failed."
Is 
executable?
Failed...
Simulator 
Failed...
Instruction
Critic / Self-Reflect 
LLM (e.g., GPT-4.1)

…

ran all trials, and
 executable?
If Yes:
Trajectory 
If No:
Ran all trials?
If Yes: "Agent Failed"
Successful?
Safe?
Figure 3: Framework: Two planning strategies are
available: One-go and Stepwise. The One-go strategy is
suitable for direct planning, where all planning actions
are generated together, while the Stepwise strategy is
better suited for iterative planning, where actions are
generated one step at a time.
2124

…

is among the few benchmarks that offer safely achievable tasks requiring multi-constraint planning with varying
levels of complexity.
4
Experimental Evaluation
4.1
Settings
LLM Models. After exhaustive preliminary experi-
ments, we utilize GPT-4.1-Mini6 and Qwen3-32B7
(Yang et al., 2025a) as the planning agents, and

…

"init_graph_id": 9,
"final_graph_id": 9
}
Example 1: VestaBench-VH Representative Task:
This is a long-horizon task against an adversarial en-
vironment with multiple success and safety constraints.
2023). Refer to Appendix B.1 for details.
Evaluation Metrics. We mainly report the results
of the delivery, success, and safety rates (as de-
scribed in Appendix B.2).
4.2
Experimental Results
RQ1: LLM Agents Performance. Our goal is to
study how well LLM agents perform on short- to
long-horizon tasks requiring safe, multi-constraint
planning in normal and adversarial environments,

…

"safety_goals": [
[
"not",
"open",
"bottom_cabinet_no_top_80"
],
[
"not",
"toggled_on",
"sink_82"
],
...
],
"trajectory": [
{
"action": "OPEN",
"object": "bottom_cabinet_no_top_80"
},
{
"action": "RIGHT_GRASP",
"object": "rag_0"
},
...
]
}
Example 2: VestaBench-B50 Representative Task:
This is a long-horizon task with multiple success and
safety constraints.
2125

…

-
55.0
62.40
31.0
44.52
14.34
-
60.0
75.10
56.0
50.49
30.59
Table 2: Main Results: GPT-4.1-Mini and Qwen3-32B are used as planning agents. Recall that, ‘(1)’ means one
round of replanning. In ReAct + Reflexion (1), the same model used for planning is also used for reflection. As for
ReAct + Critic (1), GPT-4.1 is the critic model.
ning agents on VestaBench-VH and VestaBench-
B50. For brevity, we focus only on GPT-4.1-Mini,
as similar observations hold for Qwen3-32B. A
quick observation is that the Direct (One-go) strat-
egy yields the weakest performance, with notably
low delivery, success, and safety rates. In contrast,
switching to Direct (Stepwise) leads to improved
results, outperforming one-go planning, though the
overall performance remains low. ReAct demon-
strated approximately 5% and 10% improvements
in both macro and micro success and safety rates on
VestaBench-VH, respectively. However, the gains
on VestaBench-B50 are minimal. Further perfor-
mance improvements are observed with reflective
methods, where ReAct + Critic outperforms ReAct
+ Reflexion. This can be attributed to the use of a
stronger critic model in ReAct + Critic (1).
Additionally, GPT-4.1-Mini and Qwen3-32B
show comparable macro-level performance on
VestaBench-VH, whereas GPT-4.1-Mini outper-
forms Qwen3-32B on VestaBench-B50. This differ-
ence can be attributed to the varying complexity of
tasks across the two datasets, as well as the fact that
the tasks in VestaBench-VH are designed by us, re-

…

emphasizing the current limitations of LLM agents
in managing the challenges posed by our embodied
tasks, especially with regard to safety.
RQ2: Refinement and Replanning. We report
VestaBench-VH
VestaBench-B50
Method
Success Rate (%)
Safety Rate (%)
Success Rate (%)

…

provement, with the gains being more substantial
on VestaBench-B50 than on VestaBench-VH. This
difference can be attributed to the increased diffi-
culty of tasks in VestaBench-VH, which includes
both adversarial environments and adversarial in-
structions. However, it is worth mentioning that re-

…

presents the results of this ablation study. In gen-
eral, we observe a decrease in safety rates against
both datasets compared to the results reported in Ta-
ble 2. For VestaBench-VH, GPT-4.1-Mini shows
2126

…

safety guidelines as effectively as GPT-4.1-Mini,
when comparing the results in Tables 2 and 4. For
VestaBench-B50, both models exhibit a clear de-
cline in safety rates, with the exception of Re-
Act + Reflexion (1) and ReAct + Critic (1) with
GPT-4.1-Mini. This could be attributed to the
benefits of replanning, which may have prompted
GPT-4.1-Mini to account for additional factors
such as safety during the subsequent trial(s).
4.3
Discussion
Task Complexity vs. Performance. After analyz-
ing the results by task complexity, we observe that
both success and safety rates decrease as tasks be-
come more complex. For instance, for ReAct +
Critic (1) on VestaBench-VH, the safety rates are
66.67%, 48.64%, and 33.33% for low, medium,
and high complexity tasks, respectively. Refer to
Appendix D.1 for further details.
Risk Category vs. Performance.
Table 5 re-
ports the performance on VestaBench-VH and
VestaBench-B50 across different safety and risk
categories. It may be noted here that for both bench-

…

appliances, correctly identifying the relevant de-
vices, and executing actions in the proper sequence.
Risk Type
Num.
Tasks
Success Rate (%)
Safety Rate (%)
Macro
Micro
Macro
Micro
VestaBench-VH
Physical Hazard
41
53.65
34.14
23.72

…

respectively.
Adversarial Instructions. Experiments on adver-
sarial instructions reveal that the LLM agents are
prone to generating unsafe actions and plans in
such scenarios, indicating their inability to distin-
guish malicious instructions from safe ones. Fur-
ther details are provided in Appendix D.2.

…

ing, and robustness. EmbodiedBench (Yang et al.,
2025b) aggregates tasks from multiple embodied
datasets with various environments. The Embodied
Agent Interface (Li et al., 2024b) unifies embod-
ied tasks through a standardized interface, modular
LLM components, and detailed error metrics.

…

der ambiguous or adversarial task instructions and
risky environments; however, it does not provide
explicit safety annotations. Agent-SafetyBench
(Zhang et al., 2024) introduces a diverse set of tasks
covering various interaction settings, task types,
and failure modes. AgentSafe (Liu et al., 2025)
consists of scenarios requiring avoidance of unsafe
actions during goal-directed tasks, however, it does
not include explicitly adversarial environments.
Although these benchmarks present valuable
safety challenges and reveal significant limitations
in the safety awareness of LLM-based planning
agents, most fail to include both adversarial instruc-
tions and adversarial environments collectively. In
addition, they often do not include multi-constraint
tasks or a range of planning complexities within
the annotations. To address these limitations, we
introduce VESTABENCH, a benchmark for multi-
constraint, long-horizon planning under adversarial
conditions (either adversarial instructions or envi-
ronments), where safety is a central concern.
Recall that, Table 1 provides a comparison between
our benchmarks and those mentioned above.
6
Conclusion
In this paper, we propose VESTABENCH, a bench-
mark that offers a diverse range of multi-constraint
tasks that require long-horizon planning with a fo-
cus on safety. Our experiments reveal that LLM
agents, including GPT-4.1-Mini and Qwen3-32B,
struggle with complex planning tasks, particularly
under safety constraints and adversarial environ-
ments. Replanning can help to have further im-
provements, but it requires additional trials, leading
to higher computational and time costs. Removing

1. 1 Introduction
2. 2 Related Work 1. 2.1 Vision-Language Model on Embodied AI
   2. 2.2 Safety of Embodied AI
3. 3 HomeSafeBench 1. 3.1 Task Definition
   2. 3.2 Construction and Quality Control Procedure 1. Annotation of Potential Hazard Locations
   2. Annotation of Object Attributes
   3. Rule-based Sample Generation
   3. 3.3 Dataset Statistics

…

###### Abstract

Embodied agents can identify and report safety hazards in the home environments. Accurately evaluating their capabilities in home safety inspection tasks is curcial, but existing benchmarks suffer from two key limitations. First, they oversimplify safety inspection tasks by using textual descriptions of the environment instead of direct visual information, which hinders the accurate evaluation of embodied agents based on Vision-Language Models (VLMs).
Second, they use a single, static viewpoint for environmental observation, which restricts the agents’ free exploration and cause the omission of certain safety hazards, especially those that are occluded from a fixed viewpoint. To alleviate these issues, we propose HomeSafeBench, a benchmark with 12,900 data points covering five common home safety hazards: fire, electric shock, falling object, trips, and child safety.
HomeSafeBench provides dynamic first-person perspective images from simulated home environments, enabling the evaluation of VLM capabilities for home safety inspection. By allowing the embodied agents to freely explore the room, HomeSafeBench provides multiple dynamic perspectives in complex environments for a more thorough inspection. Our comprehensive evaluation of mainstream VLMs on HomeSafeBench reveals that even the best-performing model achieves an F1-score of only 10.23%, demonstrating significant limitations in current VLMs.

…

This modality transformation discards critical spatial information, as nuanced spatial concepts are simplified into inadequate positional relationship descriptions in text, thus failing to evaluate the general visual understanding capabilities of VLM-based embodied agents. Second, they rely on fixed-view cameras for hazard identification. The fixed and limited field-of-view is susceptible to occlusion, potentially causing the embodied VLM agents to overlook hazards.
To address the lack of visual presentations and flexible viewpoints in existing home inspection benchmarks, we propose HomeSafeBench, a comprehensive benchmark for evaluating safety inspection performance of embodied VLMs under free exploration with visual feedback. The construction of HomeSafeBench combines human annotation and rule-based generation, obtaining a large scale dataset with significant diversity.

…

Each instance represents a room environment containing multiple hazards, and agents are instructed to autonomously explore the room to report these hazards. During the inspection, the VLM-based agents interacts with the environment to acquire egocentric visual perspectives, identifies hazards within the current field-of-view, and autonomously determines subsequent actions. The process is shown in Figure 1.
We conduct a systematic evaluation on mainstream VLMs using HomeSafeBench. Our results show that existing VLMs have significant capability deficiency in identifying potential home safety hazards under the paradigm of free exploration with visual feedback. Even the top-performing proprietary VLMs like Qwen-VL-Max and GPT-4o achieve an F1 score under 10%. Our finding indicates that current VLMs are not yet reliable for real-world applications in home safety inspection.

…

- •

  We introduce HomeSafeBench, a novel benchmark for embodied VLMs on home safety inspection, which enables visual feedback and agentic free exploration. HomeSafeBench contains 12,900 instances across five categories of common household safety hazards, including fire, electric shock, falling object, trip, and child safety hazards. Its quality is ensured through carefully designed construction process and extensive reviews.
- •

  We conduct a comprehensive evaluation of prevalent VLMs using HomeSafeBench. Our results show the significant limitations of existing models in home safety inspection tasks under a free exploration paradigm with visual feedback, demonstrating that HomeSafeBench is a highly challenging benchmark.
- •

  We conduct an in-depth analysis of VLM agents’ free exploration during safety inspections to understand the root of their deficiencies. We demonstrate that while free exploration is crucial for a successful inspection, it remains a significant challenge for VLM agents, especially in complex environments and over a larger number of interaction steps.

…

Our proposed HomeSafeBench introduces a challenging multi-task scenario in the embodied VLM tasks, which is to discover safety hazards in the room as much as possible, and complete the room safety inspection. Such home safety inspection task requires not only the VLM to identify safety hazards, but also to independently decide the next action with the space perception and planning capability. Compared to existing work, HomeSafeBench introduces a novel and challenging task that is of great practical use.

…

## 3 HomeSafeBench

### 3.1 Task Definition

We propose a home safety hazard inspection task in which an embodied agent actively navigates a simulated 3D home environment to identify and report safety hazards. Following real-world home safety guidelines, we define five categories of common household hazards in our benchmark. Each category represents a specific configuration of item placement that poses a safety risk.

…

Formally, let the initial state denoted as s_{0} with a ground-truth hazard set \mathcal{H}. At each discrete time step t, the agent policy \pi is to identify hazards \hat{\mathcal{H}}_{t} with the current observation, and select an action a_{t}\in\mathcal{A}. The state is then transitioned following the transition function f, updating the observation.

…

The action space \mathcal{A} consists of basic navigation primitives such as move-forward, turn-left, turn-right, and look-up, as detailed in Appendix A. After executing a sequence of actions \{a_{0},a_{1},\dots,a_{T-1}\} within a step budget T, the final identified hazard set is defined as the union of the hazard sets identified at each step.

…

Task performance is evaluated by comparing the reported hazards \hat{\mathcal{H}} against the ground-truth hazards \mathcal{H} using the precision, recall, and F1 score. A hazard is considered correctly reported if both its category and the name of the associated item are correct. Note that we do not require a perfect match for the item name. Instead, we use a rule-based matching system for a more flexible and reliable evaluation, as detailed in Appendix A.

…

### 3.2 Construction and Quality Control Procedure

HomeSafeBench is constructed based on the engine of VirtualHome by combining manual annotation and rule-based generation. The careful reviews are conducted through out the construction process to ensure the correctness and quality of the benchmark. The construction process consists of three stages, as shown in Figure 2.

#### Annotation of Potential Hazard Locations

Firstly, the spatial locations within the virtual environment that are likely to contain safety hazards are annotated, such as the top of a refrigerator, inside a sink, or on a stove. The process is performed by two annotators, each responsible for six rooms across three environments (12 rooms in total). To ensure annotation quality, the annotators cross-verify each other’s annotation case by case, filter out locations with low risks, and the final annotations reflect consensus between the annotators. Each identified location is assigned exactly one hazard type tag. In total, we obtain 136 annotated hazard locations across all environments.

…

#### Rule-based Sample Generation

Finally, the final samples of HomeSafeBench are generated following the combination rule of locations and objects. Specifically, based on the potential hazard types associated with these locations, we place suitable objects with corresponding attributes at the sampled positions. For instance, a location tagged as fire hazard (e.g., a stove) may have an object of paper placed on it, while a location tagged as falling object hazard (e.g., the top of a refrigerator) may have a glass cup assigned to it.
For quality control of the final samples, we conduct tests in two ways. First, we randomly select 100 samples, examine every hazard of the gold labels in the virtual environment. It is verified that all the hazard points marked are indeed risky and the placement of items is visually discoverable. Second, we randomly select other 100 sample, and manually conduct inspection with no golden label given. The Precision, Recall, and F1 scores achieve 82.29%, 69.50%, and 75.36% for human inspection, validating that the tasks in HomeSafeBench are solvable.

…

### 4.2 Main Result

Table 3: Main results of embodied VLMs on HomeSafeBench. Best scores among all models are shown in bold. Prec and Rec refer to Precision and Recall respectively. |Models|Subset|Subset|Subset|Others|Others|Others|All|All|All|
|--|--|--|--|--|--|--|--|--|--|

…

As detailed in Appendix A, the subset contains more hazard points in obvious places which are easier to notice. Comparison between results of different test sets show that the subset generally obtains higher scores, which meets our expectations. However, the final results are still very low compared to human scores (75.36% F1 score), again validating the tasks of home safety inspection from HomeSafeBench pose strong challenges to VLMs.

## 5 Analysis

In the introduction of HomeSafeBench, we utilize an interactive simulated environment to enable free-exploration for home safety inspection, bridging the gap between evaluation and real-world performance. In the design of VLM embodied agents, we allow the VLM to control the agent’s free exploration by generating navigation primitives such as move-forward, turn-left, turn-right, and look-up, as detailed in Appendix A.
The paradigm of free exploration plays a crucial role in our proposed HomeSafeBench. On one hand, it introduces more flexibility to home safety inspection tasks thus raising its upper-bound capability. On the other hand, it places greater demands on embodied agents and poses greater challenges for VLMs, which potentially leads to the low performance of current models, as shown in Table 3.

…

The results are shown in Table 4. When deprived of the ability to explore freely, all models suffer from a consistent and significant decrease in F1 scores. Although Qwen2.5-VL, Qwen-VL-Max, and Gemma3-12B models achieve improvements in precision compared to when deprived, they suffer from a more significant recall drop due to insufficient environmental information and occlusion, finally scoring lower F1. These results indicate that enabling the VLM to control the agent’s free exploration is a key factor in ensuring the model’s effectiveness in safety inspection tasks.

…

### 5.3 Free Exploration under Multi-Turn Interaction

The free exploration in HomeSafeBench involves multi-turn interaction with the virtual environment. A natural question under this paradigm is, how will the effectiveness of free exploration be affected as the number of turn grows. Therefore, we conduct an investigation by setting the maximum number of turns to 30, and calculating the model score every five turns.

…

## 6 Conclusion

To address the limitations of fixed viewpoints and the loss of critical visual information during home safety inspection evaluation, we propose HomeSafeBench, a benchmark for embodied VLM evaluation on home safety inspection tasks, featured by first-person visual perception and interactive free exploration. HomeSafeBench comprises a large-scale and multi-category dataset constructed based on the VirtualHome simulation environment, containing 12,900 samples with significant variations across five common hazard categories, including fire, electric shock, falling objects, falls, and child safety hazards. The correctness and quality of HomeSafeBench is ensured by human reviews throughout the annotation process.
Using HomeSafeBench, we systematically evaluate the mainstream VLMs, highlighting significant shortcomings of existing models in safety hazard identification and exploration strategies. In particular, we conduct a in-depth analysis on the free exploration pattern of embodied VLMs on home safety inspection tasks. The analysis reveals not only the importance of free exploration, but also the significant weaknesses of VLMs in effective navigation especially in complex environment under a multi-turn paradigm, partially explaining the deficiency of them to conduct safety inspection.
Focusing on the home safety inspection task, our work provide a solid foundation through the comprehensive benchmarking of embodied VLMs. On a broader impact, our key findings indicate the weaknesses of current VLMs on purposeful navigation and hazard identification, and can inspire future work for a general VLM capability improvement.

## 7 Ethics statement

Our work falls under the category of embodied agents controlled by VLMs, a field that carries certain inherent risks. However, as a benchmark built upon existing theory and application, our study introduces little additional risks beyond current ones. Moreover, this work proposes HomeSafeBench specifically for security checks, which aims to enhance the safety of embodied VLM systems and thus has a substantial positive impact.

…

### B.2 Prompt

Our experiments used multiple prompts. To ensure reproducibility, this section demonstrates the prompts used.

In the main experiment, we used HomeSafeBench to evaluate a mainstream VLM. To ensure the VLM fully understood the task, we split the inspection task into Task 1 and Task 2, describing each task’s requirements in detail. For ease of evaluation, we specified the output format and required the VLM to strictly adhere to it. We also provided three examples to facilitate contextual learning for the VLM. As shown in Figure 4.

…

### C.1 Example of Hazard location

HomeSafeBench dataset comprises 3 distinct environments, each containing 4 different room types, resulting in a total of 12 scenarios. During the data construction phase, the process requires the initial annotation of hazard locations. To illustrate the specifics of our annotation methodology, for all 12 scenarios, a number of Hazard locations are selected, ensuring that at least one instance of each type of hazard is included. An example of a hazard location is presented in Figure 6.

###### Abstract
Embodied Planning is dedicated to the goal of creating agents capable of executing long-horizon tasks in complex physical worlds.
However, existing embodied planning benchmarks frequently feature short-horizon tasks and coarse-grained action primitives.
To address this challenge, we introduce CookBench, a benchmark for long-horizon planning in complex cooking scenarios.
By leveraging a high-fidelity simulation environment built upon the powerful Unity game engine, we define frontier AI challenges in a complex, realistic environment.
The core task in CookBench is designed as a two-stage process.
First, in Intention Recognition, an agent needs to accurately parse a user’s complex intent.
Second, in Embodied Interaction, the agent should execute the identified cooking goal through a long-horizon, fine-grained sequence of physical actions.
Unlike existing embodied planning benchmarks, we refine the action granularity to a spatial level that considers crucial operational information while abstracting away low-level robotic control.
Besides, We provide a comprehensive toolset that encapsulates the simulator.
Its unified API supports both macro-level operations, such as placing orders and purchasing ingredients, and a rich set of fine-grained embodied actions for physical interaction, enabling researchers to focus on high-level planning and decision-making.
Furthermore, we present an in-depth analysis of state-of-the-art, closed-source Large Language Model and Vision-Language Model, revealing their major shortcomings and challenges posed by complex, long-horizon tasks.
The full benchmark will be open-sourced to facilitate future research.
## Introduction
The core vision of Embodied AI (Liu et al.
...
Our analysis shows that while these leading models exhibit certain planning capabilities, the long-horizon challenges of CookBench still pose a severe test.
Through a systematic analysis of their performance, we identify critical shortcomings in areas such as long-horizon state tracking and physical commonsense reasoning.
These findings are not a declaration of failure, but rather illuminate the core technical directions that must be addressed to build more capable embodied agents for the a future.
…
- •
A Novel Benchmark for Long-Horizon Planning.
We introduce CookBench, a complex, knowledge-driven benchmark with an average task length of 120 steps, designed to rigorously evaluate long-horizon planning capabilities.
- •
A Large-Scale Dataset and Task Suite.
We provide a comprehensive, bilingual dataset with 14,394 instructions for complex intent recognition, alongside a challenging suite of embodied interaction tasks, including 131 single-dish and approximately 4,446 multi-dish scenarios.
…
|Benchmark|Benchmark|- Task & Eval.
-|- Task & Eval.
...
This stage evaluates the agent’s capacity to translate the structured intent from Task 1 into a concrete, long-horizon sequence of physical actions.
The goal is to follow a recipe and successfully prepare one or more dishes in a dynamic, physics-based kitchen environment.
The tasks consist of 131 single-dish and 4,446 multi-dish scenarios, consistent with the dish combinations in Stage 1.
As shown in Figure 2, the planning model needs to devise the action names and parameters to complete the task, based on the atomic action library, perceptual information, and scene information.
…
The agent receives dynamic Perceptual Feedback through its “eyes”.
This involves using a Vision-Language Model(VLM) to continuously analyze RGB images from the environment, providing feedback on the execution status of its actions (e.g., success or failure) and detecting unexpected situations (e.g., a dropped item).
...
The tasks in CookBench inherently follow a two-stage process: first, an Intention Recognition stage, where the agent should parse natural language instructions into structured cooking goals; and second, an Embodied Execution stage, where the agent should perform long-horizon physical interactions in the simulator based on these goals.
To systematically evaluate the capability boundaries of current SOTA models against the challenges of each stage, we have designed a series of decoupled experiments.
…

�
�
���
���
������
���
������
���
���
���
���
������
�������
���
�������
�������
�������
Figure 1.
Framework Overview.
Different from existing vision language navigation, object loco-navigation, and demand-driven navigation
benchmarks, LH-VLN divides navigation into multiple subtasks, requiring the agent to complete these tasks sequentially within the scene.
…
capturing the complexity of long-horizon, multi-stage tasks
and accurately assess the agent’s task execution and detailed
sub-task performance with reasonable metrics, and 3) a spe-
cialized method to equip agents with adaptive memory for
complex navigation.
In this work, we provide a compre-
hensive solution that addresses these three aspects, laying
…
able creation of richly varied navigation tasks that support
advanced model training and long-horizon VLN evaluation.
Benchmark-wise, existing VLN benchmarks [17, 20, 48]
are limited by their simple task structures, low data diver-
sity, and constrained instructional flexibility, which restrict
model generalization and hinder support for complex, long-
horizon tasks.
These benchmarks often rely on manual an-
notation, making them labor-intensive to create and less
scalable for handling multi-stage tasks [21, 46].
To over-
come these challenges, we build Long-Horizon Planning
and Reasoning in VLN (LHPR-VLN) based on the NavGen
platform.
LHPR-VLN is the first LH-VLN benchmark that
consists of 3,260 tasks with an average of 150 task steps.
This large-scale benchmark captures the depth and variety
required for evaluating long-horizon VLN, encompassing a
wide range of sub-task structures and navigation complex-
…
Independent Success Rate (ISR), to assess success for each
subtasks, capturing the model’s performance at each step
and offering a more detailed evaluation of execution across
the full scope of LH-VLN challenges.
Existing VLN methods typically rely on discretizing the
environment into static points for path prediction, limiting
adaptability in complex, dynamic settings [2, 24, 39, 47].
…
tasks, each averaging 150 steps, and propose three new
metrics for detailed, sub-task-level evaluation.
• We present the MGDM model, designed to enhance
model adaptability in dynamic settings through combined
short-term and long-term memory mechanisms.
2. Related Work
2.1.
Vision-Language Navigation
Embodied Vision-Language Navigation (VLN) aims to en-
able agents to perform navigation tasks in complex envi-
12079
…
The progression of VLN tasks has been propelled by a range
of datasets, each introducing unique challenges and enhanc-
ing evaluation benchmarks for embodied agents perform-
ing tasks in complex environments.
Early datasets, such
as Room-to-Room (R2R) [3] and its extension Room-for-
Room (R4R) [12], focus on step-by-step navigation through
...
tasks in highly complex environments.
3. Platform, Benchmark, and Metrics
We developed a data generation platform named NavGen,
specifically designed to support the data needs of the LH-
VLN task.
Based on this platform, we created the LHPR-
VLN benchmark to evaluate model performance in terms of
long-term planning capabilities within this task.
…
evaluated based on the agent’s final positional state relative
to the target.
Table 1 presents a comparison between repre-
sentative VLN benchmarks, our LHPR-VLN is the first LH-
VLN benchmark, containing 3,260 multi-stage and step-by-
step VLN tasks from 216 complex scenes, with an average
…
also construct the LHPR-VLN benchmark, which provides
three new metrics for detailed, sub-task-level evaluation.
Additionally, we present the MGDM model, designed to
enhance model adaptability in dynamic settings through
combined short-term and long-term memory mechanisms,
achieving outstanding performance on the LH-VLN task.
12085