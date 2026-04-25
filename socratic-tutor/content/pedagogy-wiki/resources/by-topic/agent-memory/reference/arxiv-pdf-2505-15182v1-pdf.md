# Source: https://arxiv.org/pdf/2505.15182v1.pdf
# Author: Jeonghye Kim et al.
# Title: ReflAct: World-Grounded Decision Making in
# Fetched via: jina
# Date: 2026-04-10

Title: 2505.15182v1.pdf



Number of Pages: 25

# ReflAct: World-Grounded Decision Making in LLM Agents via Goal-State Reflection 

Jeonghye Kim 1∗, Sojeong Rhee 1∗, Minbeom Kim 2, Dohyung Kim 2,Sangmook Lee 2, Youngchul Sung 1†, Kyomin Jung 2†,

> 1

KAIST, 2Seoul National University 

> {jeonghye.kim, sojeong.rhee, ycsung}@kaist.ac.kr, kjung@snu.ac.kr

Abstract 

Recent advances in LLM agents have largely built on reasoning backbones like ReAct (Yao et al., 2023), which interleave thought and ac-tion in complex environments. However, Re-Act often produces ungrounded or incoherent reasoning steps, leading to misalignment be-tween the agent’s actual state and goal. Our analysis finds that this stems from ReAct’s inability to maintain consistent internal be-liefs and goal alignment, causing compound-ing errors and hallucinations. To address this, we introduce ReflAct, a novel backbone that shifts reasoning from merely planning next ac-tions to continuously reflecting on the agent’s state relative to its goal . By explicitly ground-ing decisions in states and enforcing ongoing goal alignment, ReflAct dramatically improves strategic reliability. This design delivers sub-stantial empirical gains: ReflAct surpasses Re-Act by 27.7% on average, achieving a 93.3% success rate in ALFWorld. Notably, ReflAct even outperforms ReAct with added enhance-ment modules (e.g., Reflexion, WKM), show-ing that strengthening the core reasoning back-bone is key to reliable agent performance. 

1 Introduction 

Recent advancements in Large Language Mod-els (LLMs) have significantly enhanced their rea-soning capabilities, enabling LLM-based agents to perform complex multi-step decision making beyond static problem solving (Forootani, 2025; Chervonyi et al., 2025). As LLMs are extended into agentic frameworks where they interact with open-ended environments, the ability to solve long-horizon tasks through ongoing interaction and se-quential reasoning has become a central research focus (Zhou et al., 2023; Song et al., 2024). A large number of recent LLM agents build on the ReAct (Yao et al., 2023) framework, which in-  

> ∗Equal contribution.
> †Co-corresponding authors.

Figure 1: Comparison of reasoning influence in ReflAct and ReAct. While ReAct focuses on the current ob-servation and the next action at each timestep, ReflAct reflects on the internal belief state and the task goal. 

tegrates Chain-of-Thought (CoT) reasoning (Wei et al., 2022) with an action selection mechanism. Various extensions have been proposed to enhance this backbone by incorporating reflective iterations or memory components to improve reasoning per-formance (Shinn et al., 2024; Liu et al., 2023; Qiao et al., 2024). However, mounting evidence sug-gests that ReAct and its variants often deliver lim-ited benefits and can even deteriorate performance, especially in complex, partially observable, or dy-namic environments (Ma et al., 2025; Chang et al., 2024; Verma et al., 2024). These findings raise questions about the current direction of extending the basic ReAct reasoning-action framework. In this paper, we claim that true progress lies in fundamentally redesigning the backbone reasoning process itself, rather than adding complementary modules. Our analysis shows that the fundamental problem of current ReAct-based reasoning meth-ods is the frequent lack of proper grounding of generated thoughts on the agent’s historical con-text or overarching objective. These misaligned thoughts guide subsequent action choices. In dy-1

> arXiv:2505.15182v1 [cs.CL] 21 May 2025

namic or partially observable environments, such reasoning errors compound over time, leading to increasingly divergent internal beliefs, deteriorated decision quality, and failed task execution. To address this limitation, we introduce ReflAct (Reflect for Action) , a new backbone framework that shifts the focus of the agent’s thought from pre-dicting the next action to continuously reflecting on its current state in the context of the task goal ,as shown in Figure 1. Unlike previous approaches that layer reflective or memory modules onto the ReAct backbone (Shinn et al., 2024; Qiao et al., 2024; Xiong et al., 2025), ReflAct does not rely on such additional components but replaces the core reasoning–action cycle itself. That is, at each timestep, the agent evaluates whether its current trajectory and situation align with its intended long-term objective before selecting an action. This reflective thought mechanism enables early detec-tion of potential deviations and facilitates timely strategy adjustments, as we shall see shortly. By grounding decisions in actual observations and maintaining continuous goal alignment, ReflAct substantially reduces hallucination tendency and enhances long-term strategic coherence. We implemented ReflAct using both open-source (Llama 3.1-8B/70B-Instruct (Grattafiori et al., 2024)) and proprietary (GPT-4o-mini/4o (OpenAI, 2024)) LLMs, and evaluated it in three text-based environments: ALFWorld (Shridhar et al., 2021), ScienceWorld (Wang et al., 2022) and Jericho (Hausknecht et al., 2020), which require an agent to decompose the goal and acts over a long time horizon under partial observability. Empirical results show that ReflAct helps the agent better align its internal beliefs with the environment and promotes goal-consistent behavior. As a result, Re-flAct significantly outperforms ReAct by 36.4%, 8.5%, and 38.1% on ALFWorld, ScienceWorld, and Jericho, respectively. Notably, ReflAct also surpasses enhancement modules layered on top of existing backbones, demonstrating that revising the reasoning process itself can be more effective than adding new components. 

2 Preliminaries 

We model the agent’s task in a language-based en-vironment as a Partially Observable Markov Deci-sion Process (POMDP) (Puterman, 1990), defined as M = ⟨U , S, A, O, P, R⟩ , where u ∈ U is a task instruction, s ∈ S is the (hidden) environment state, a ∈ A is an action, o ∈ O is an observation, 

P is the transition function, and R is the reward function. In our setting, U, A and O are expressed in natural language. 

The ReAct Framework The ReAct framework (Yao et al., 2023) enables LLM agents to solve tasks through interleaved reasoning and action. To incorporate reasoning steps (thoughts), we extend the above POMDP by including a thought space 

T , where each thought τ ∈ T represents a natural language reasoning step generated by the agent. Then, this extended POMDP operates as follows. Given a task instruction u ∈ U , the agent follows a policy πθ that alternates between generating a thought as πthought  

> θ

and taking an executable action as πact  

> θ

. At each time step t, the agent receives an observation ot and forms a context ct = ( ht, o t),where ht = {u, τ 1, a 1, o 1, . . . , τ t, a t} is the history of previous interactions. Based on ct, the agent samples a thought from a context-conditioned dis-tribution: τt ∼ πthought  

> θ

(· | ct). This thought τt is then appended to the context to form an enriched input c′ 

> t

= ct ⊕ τt, which is used to select the next action: at ∼ πact  

> θ

(· | c′

> t

). The selected action at is executed to the environment, resulting in the next observation ot+1 . This reasoning–acting loop con-tinues until the task is completed or a predefined time limit is reached. 

3 Revisiting the Efficacy of Thought 

3.1 How Thought Impacts Action Selection 

Basically the thought τt functions as a reweighting mechanism for the action probability distribution of the policy πact  

> θ

by enriching the context ct into an augmented form: c′ 

> t

= ct ⊕ τt.We analyzed this process in detail using a task from ALFWorld (Shridhar et al., 2021), where the task is to find an apple, heat it, and place it in a garbage can. We implemented the policy πθ us-ing Llama-3.1-8B-Instruct (Grattafiori et al., 2024) and compared two agent variants: the NoThinking agent, which selects actions without intermediate reasoning, and the ReAct agent, which generates a reasoning step before each action. Figure 2 shows one instance of execution sequence. The sequence starts with the task description with initial obser-vation, followed by two cycles of thought-action-observation, ending with observation "You open the microwave 1. The microwave 1 is open. · · · ". Then, in the next thought step, we tried each of four cases: empty (i.e., no thought) and three thoughts 2in the middle of Figure 2, and observed the distri-bution on actions in the next step. 

> Figure 2: Changes in the action probability distribution when modifying thought in the ALFWorld ‘heat some apple and put it in garbagecan’ task.

First, without any thought (NoThinking), the agent assigns high probability to the heat action, still considering other actions such as ‘put’ and ‘go’ with non-negligible probabilities. Now, when a non-empty thought is provided, the next ac-tion probability distribution is directly influenced: THOUGHT 1 relevant to the task sharpens the distri-bution toward appropriate actions, leading to con-textually aligned selections. In contrast, T HOUGHT 

2 and T HOUGHT 3, injecting incorrect or conflict-ing information, bias the distribution and increase the likelihood of inappropriate actions. As seen, thought directly shapes the next action distribu-tion, either reinforcing correct decisions or causing misalignment depending on its quality. When the model is provided with a structured thought, it relies predominantly on that thought to drive de-cision making, thereby significantly reducing its dependence on the broader historical context. 

To quantify the overall impact of thought on the agent’s decision-making process, we measured the entropy of the agent’s action probability distribu-tion across 134 tasks from ALFWorld. Specifically, for a given timestep t, the entropy is defined as 

HNoThinking  

> t

= − X

> a∈A

πact  

> θ

(a | ct) log πact  

> θ

(a | ct)

HReAct  

> t

= − X

> a∈A

πact  

> θ

(a | c′

> t

) log πact  

> θ

(a | c′

> t

),

where c′ 

> t

= ct ⊕ τt and τt ∼ πthought  

> θ

(· | ct).We computed the entropy averaged over all timesteps and tasks, and the result is reported in Table 1. As shown in the table, the NoThinking     

> Table 1: Average entropy of the action probability distri-bution when performing 134 ALFWorld tasks using the Llama-3.1-8B-Instruct with NoThinking and ReAct.
> Model ¯HNoThinking ¯HReAct
> Llama-3-1-8B-Instruct 1.23 0.30

agent exhibits mean entropy of 1.23, whereas the ReAct agent yields a significantly lower value of 0.30. This substantial reduction in entropy implies that conditioning the policy on thought leads to more confident and focused behavior. 

3.2 The Problem of Ungrounded Thought 

Since action at is heavily influenced by thought 

τt ∼ πthought  

> θ

(· | ct), it is crucial that τt accu-rately captures the core decision-relevant informa-tion from the context ct = ( ht, o t). If the thought becomes ungrounded, meaning it is disconnected from the actual state, it can mislead the policy and induce a suboptimal or incorrect action. 

> Figure 3: Comparison of failure rates between NoThink-ing and ReAct on GPT-4o and Llama-3.1-8B-Instruct

To assess the overall performance degradation from ungrounded thought, we evaluated task fail-ure rates across 134 ALFWorld (Shridhar et al., 2021) tasks using πθ realized with GPT-4o (Ope-nAI, 2024) and Llama-3.1-8B-Instruct (Grattafiori et al., 2024). Figure 3 categorizes the outcomes into four groups: (1) only the NoThinking agent failed, (2) only the ReAct agent failed, (3) both failed, and (4) both succeeded. As shown in the fig-ure, incorporating thought can help the agent solve tasks that would otherwise fail without it. However, thought also introduces new risks, causing failures that could have been avoided without thought, even in stronger models like GPT-4o. To see the cause of the ReAct agent’s failure, we examined a failure case of the ReAct agent in ALF-World (Shridhar et al., 2021). As seen in Figure 4 (1), the agent is given a simple task: Find a soap bar, take it and place it on the countertop. After interacting with a soap bottle 2 in cabinet 1, the agent attempts to return to cabinet 1 to search for the soap bar even though it is not there, because the generated thought does not capture the current 3Figure 4: In the ALFWorld task ‘put a clean soapbar in countertop’, the agent picks up a soapbottle from cabinet 1 and puts it back, (1) while planning the next action, it redundantly tries to go back to cabinet 1 and fails, (2) after reflecting on the state and goal, it moves elsewhere and succeeds. 

situation in the context of goal properly from its observation history. This redundant and illogical behavior leads to a loop, and the agent ultimately fails to complete the task. A failure case in Sci-enceWorld is provided in Figure 9 in Appendix B. From the examples, we see that the agent fails due to two major reasoning limitations: (1) A lack of grounding in its internal state. The agent fails to maintain a coherent internal state, leading to inconsistency, e.g., revisiting a loca-tion it already visited or falsely assuming it is holding an object. (2) Short-sighted planning. The ReAct agent typically exhibits short-sighted planning, mak-ing decisions that appear locally plausible but disregard the long-term task goal. We recognize that these two shortcomings stem from incorrect guidance for the agent’s reasoning process although the agent has better reasoning capability. Indeed, for the same failure scenario in Figure 4 left branch, we input a reasoning guidance sentence different from that of ReAct, to focus not on predicting the next step but assess the agent’s current state in relation to the task goal, as seen in Figure 4 right branch. Now, it is seen that the agent can better align its action with the overall objective by reflecting on what it currently knows and what it aims to achieve. This is also valid for the ScienceWorld failure case in Figure 9 in Appendix B. 

4 Proposed Method: ReflAct 

In the LLM POMDP framework, a thought τt ∈ T 

should be generated so that it leads to the selec-tion of an action at that maximizes the expected long-term return when used to condition the ac-tion policy πact  

> θ

, where the long-term return is de-fined as Gt = P∞ 

> k=0

γkRt+k with discount factor 

γ ∈ [0 , 1) . Here, Rt+k is the immediate reward at time t + k. Thus, the optimal thought τ ∗ 

> t

can be defined as 

τ ∗ 

> t

= arg max  

> τ∈T

Ea∼πact    

> θ(·| ct⊕τ)

[E [Gt | st, a ]] ,

where ct denotes the current context and ⊕ de-notes concatenation. To maximize the expected long-term return, the thought τt should not be gen-erated from the observation solely to decide the next action. Instead, it should be formed with con-sideration of the final task goal at every time step, as illustrated in Figure 1. In this way, the agent can rely on thought for action generation without deviating from a goal-reaching path. Furthermore, since the environment is partially observable and the true state st is not directly accessible, the agent must rely on an internal belief state inferred from its interaction history. So, the generated thought should make this belief more explicit and stable, while encoding task-relevant reasoning that effec-tively guides the downstream policy toward the long-term objective. To achieve the generation of such thoughts, we do not use an additional module but exploit the LLM agent’s reasoning capability maximally. For 4this, we redesign a new thought generation instruc-tion to better guide thought generation as follows:  

> Instruction for ReflAct
> You should first reflect on the agent’s state in rela-tion to the task goal , and then output the action for this turn.

In this new design, we have the explicit guiding terms ‘agent’s state’, ‘task goal’ and their connec-tion term ‘in relation to’ to realize the desired state diagram of thought dependency in the lower part of Figure 1. Following this instruction, the agent engages in reflective reasoning to gain a clearer understanding of both the current situation and the intended goal. We refer to so-generated thought as reflection and name the new reflection-action process ReflAct . To formalize this, we define a reflection space K, where each reflection k ∈ K

is a structured representation that aims to explic-itly encode both the agent’s internal belief state M

and the task goal G. The belief state captures the agent’s current understanding of the state based on its interaction history, whereas the goal component provides a concise summary of what the agent is trying to achieve. By explicitly representing both in the reflection, ReflAct allows the agent to con-dition its subsequent decision-making on a more coherent and goal-aligned internal context. 

> Example of Thought vs Reflection Before Action
> Thought: Now I find a spraybottle 2. Next, I need to take it. Reflection: Currently, I am at cabinet 2 and have found a spraybottle 2, which brings me closer to completing the task of placing it on the toilet.

In addition, we incorporate one-shot examples based on the tasks from Yao et al. (2023); Xiong et al. (2025) modified with Reflections on the agent’s state in relation to the task goal, gener-ated by GPT-4o-mini (OpenAI, 2024). Above, we present an example describing the modification from Thought to Reflection. The complete set of one-shot examples is provided in Appendix H. 

5 Related Works 

Building on CoT reasoning (Wei et al., 2022), nu-merous approaches attempted to enhance LLM agent capability. ReAct (Yao et al., 2023) pio-neered the interleaving of reasoning with action steps for interactive environments, while Plan-and-Solve (Wang et al., 2023) introduced higher-level planning in the initial stage. Recent enhance-ment modules sought to improve ReAct’s CoT through various mechanisms: Reflexion (Shinn et al., 2024) through post-task analysis of fail-ures after task completion , WKM (Qiao et al., 2024), MPO (Xiong et al., 2025), and DC (Suz-gun et al., 2025) via external memory of envi-ronment knowledge, and RAFA (Liu et al., 2023) by generating and evaluating future possible tra-jectory predictions. However, when the ReAct backbone incorrectly grounds past observations, all these approaches suffer from degraded perfor-mance. Therefore, ReflAct retouches the reasoning process itself to enable more grounded and goal-aligned decision making. In our experiments, we will validate the importance of this approach com-pared to the design of enhancement modules, as well as its synergy with them. Additional related works are discussed in the Appendix A. 

6 Experiments 

6.1 Experimental Settings Benchmarks. We benchmarked ReflAct on three widely used text-based environments: ALFWorld (Shridhar et al., 2021), ScienceWorld (Wang et al., 2022), and Jericho (Hausknecht et al., 2020). ALF-World evaluates embodied agents on household tasks, ScienceWorld assesses procedural and scien-tific reasoning in educational scenarios, and Jeri-cho tests agents in classic interactive fiction games that require commonsense reasoning and memory. For evaluation, ALFWorld uses binary task success, while ScienceWorld and Jericho provide dense re-ward signals, enabling evaluation based on both success rate and average reward, calculated as the mean reward across all tasks. Additional bench-mark details are provided in Appendix C. 

Agent Models. We use GPT-4o and GPT-4o-mini (OpenAI, 2024), and Llama-3.1-8B/70B-Instruct (Grattafiori et al., 2024) as underlying models. GPT-4o variants serve as proprietary models, while Llama-3.1-Instruct variants represent open-source counterparts, each with large and small sizes. 

6.2 Comparison with Prior Methods Baselines. We first compare ReflAct with three reasoning frameworks. Details for each can be found in Appendix D.1. (1) NoThinking (Ma et al., 2025): The agent gen-erates an action directly at each time step without any reasoning step. 5Table 2: Performance comparison of ReflAct with NoThinking, ReAct, and Plan-and-Act across ALFWorld, ScienceWorld, and Jericho. SR and AR denote success ratio and average reward, respectively. Values in parentheses indicate percentage improvement over the NoThinking baseline.                                                                                                              

> Model Prompting ALFWorld ScienceWorld Jericho Average
> SR AR SR AR SR GPT-4o NoThinking 76.1 67.4 50.2 27.8 10.0 46.3 ReAct 85.1 68.7 55.9 50.4 20.0 56.0 (+21.0%) Plan-and-Act 85.8 68.7 55.0 45.6 20.0 55.0 (+18.8%)
> ReflAct 93.3 68.9 57.8 53.2 35.0 61.6 (+33.1%) GPT-4o-mini NoThinking 43.3 42.3 21.8 18.8 5.0 26.2 ReAct 53.0 49.1 37.0 29.8 15.0 36.8 (+40.2%) Plan-and-Act 59.0 51.8 35.5 37.1 15.0 39.7 (+51.1%)
> ReflAct 66.4 55.4 37.0 45.4 20.0 44.8 (+70.9%) Llama-3-1-8B -Instruct NoThinking 21.6 29.9 14.2 10.0 0.0 15.1 ReAct 29.1 43.0 27.5 12.8 0.0 22.5 (+48.5%) Plan-and-Act 30.6 34.2 14.7 10.6 0.0 18.0 (+19.0%)
> ReflAct 60.5 47.2 33.2 20.9 10.0 34.4 (+126.9%) Llama-3-1-70B -Instruct NoThinking 53.7 65.6 46.4 27.4 5.0 39.6 ReAct 81.3 66.4 53.1 33.9 10.0 48.9 (+23.5%) Plan-and-Act 81.3 67.7 52.6 29.6 10.0 48.2 (+21.8%)
> ReflAct 83.6 73.7 58.8 44.5 20.0 56.1 (+41.6%)

Figure 5: A comparison of ReAct, ReflAct, and various verbalization strategies (state, goal, state+goal, and state+goal with next-action reasoning), using Llama-3.1-8B-Instruct as the agent model. Bars represent success rate; the red dashed line indicates average reward. 

(2) ReAct (Yao et al., 2023): The agent first reasons about the next action at each time step and then generates an action. (3) Plan-and-Act: In addition to NoThinking and ReAct, we designed another reasoning framework inspired by Plan-and-Solve (Wang et al., 2023) for comparison. Here, the agent is instructed at the first timestep ( t = 1 ) to ‘plan your approach to the task, and then output the action.’ It performs reasoning only at this step and outputs actions without further thoughts in subsequent timesteps. 

Results. Table 2 presents the performance of ReflAct compared with the NoThinking, ReAct, and Plan-and-Act baselines across ALFWorld, Sci-enceWorld, and Jericho. As shown in the table, the ReAct agent outperforms the NoThinking agent, highlighting the effectiveness of the Thinking be-fore Action framework. Plan-and-Act, which be-gins with a single planning step and then executes actions directly, performs comparably or slightly better than ReAct in stronger models like GPT-4o. This suggests that when a model has enough capacity, initial goal-based reasoning is effective, and flawed intermediate reasoning may offer little benefit. However, in weaker models like Llama, Plan-and-Act underperforms because these models struggle to retain and follow the initial plan. In contrast, ReflAct, which reflects on both the state and the goal at every timestep, consistently out-performs all the baseline reasoning frameworks regardless of backbone model or task. Notably, ReflAct achieved performance improvements of 77.9%, 25.9%, and 101.1% over NoThinking in ALFWorld, ScienceWorld, and Jericho, respec-tively, and improvements of 36.4%, 8.5%, and 38.1% over ReAct in the same environments. Importance of Reflection over Simply Stating. 

To verify the source of ReflAct’s superior perfor-6mance gain, we conducted an ablation study. Re-flAct reflects on the agent’s state in relation to the task goal, so we compared this with variants in which the agent simply verbalizes its state, its goal, or both, without engaging in reflection. As shown in Figure 5, we evaluated four settings: the agent verbalizes (1) the current state, (2) the task goal, (3) both the state and the goal, and (4) the state and goal while also reasoning about the next action. The results indicate that merely stating the state or goal underperforms compared to the ReAct baseline. Adding an explicit next-action thought in addition to verbalizing the state and goal yields performance gains in ALFWorld compared to Re-Act, but still falls short of ReAct in ScienceWorld and Jericho. In contrast, ReflAct, which explic-itly reflects on the relationship between the state and the goal, demonstrates a substantially greater performance gain. These findings suggest that re-flection, specifically reasoning about the state in the context of the goal, is more effective than sim-ply verbalizing the state or the goal. 

6.3 ReflAct with Enhancement Modules 

We examine layering enhancement modules on top of ReflAct. We consider Reflexion (Shinn et al., 2024), the use of post-task reflection in ReAct to improve planning, and WKM (Qiao et al., 2024), which incorporates a parametric world model into ReAct. Discussion on RAFA (Liu et al., 2023), which focuses on long-sighted planning via next-state prediction, and MPO (Xiong et al., 2025), which improves planning through online prefer-ence learning, can be found in Appendix F. 

6.3.1 ReflAct and Reflexion 

Reflexion (Shinn et al., 2024) performs post-task reflection by analyzing failed trajectories and gen-erating improvement plans for future trials. Since post-task reflection operates independently of the underlying reasoning process, we analyze its im-pact when combined with three reasoning frame-works: NoThinking, ReAct, and ReflAct. Figure 6 shows the results of applying Reflex-ion to each backbone in ALFWorld and Jericho. We followed Shinn et al. (2024) in applying post-task reflection after each trial, repeating this for three trials. The results show that post-task re-flection generally improves performance across all base agents, except Llama NoThinking and ReAct in Jericho. However, even after applying Reflex-ion, the NoThinking and ReAct agents still fall 

> Figure 6: Success rate change with Reflexion post-task reflection (NoThinking, ReAct, ReflAct).

short of ReflAct’s trial 0 performance. This high-lights that when the initial reasoning backbone is weak, even repeated feedback across trials provides only limited benefit. Although post-task reflection aids reasoning by analyzing failures, enhancing in-task reflection through a stronger backbone proves more fundamental. Notably, the GPT-4o ReflAct agent with Reflexion achieved an unprecedented 94.8% success rate in ALFWorld, bringing house-hold robots one step closer to reality, given suffi-cient hardware support. 

6.3.2 ReflAct and WKM 

WKM (Qiao et al., 2024) improves LLM agents’ decision-making in interactive environments by using Task Knowledge for global planning and State Knowledge for local context. Its paramet-ric knowledge model, fine-tuned on knowledge-augmented trajectories, enables context-aware decision-making by referencing past similar situa-tions. WKM learns and utilizes an external knowl-edge model in contrast to ReflAct, which intends to perform internal state modeling within the rea-soning backbone. We applied WKM to ReAct and further exam-ined a scenario where state knowledge is placed immediately before action, replacing the thought, to guide the action. This allows us to assess the impact of explicit state knowledge compared to ReflAct’s internal state modeling. Figure 7 shows performance related to WKM. Applying WKM to ReAct results in a performance improvement, but it still falls short of ReflAct. Replacing the thought step with state knowledge to directly guide the ac-tion actually degrades performance, highlighting the side effect of incorrect guidance from the ex-7Figure 7: Performance: ReflAct, NoThinking, ReAct, and ReAct+WKM with thought replaced by WKM state knowledge (Llama-3.1-8B-Instruct as agent) 

ternal model. This suggests that encouraging the model to perform internal state modeling on its own can be more effective than relying on state knowledge generated by an external model. 

6.4 Further Discussion on ReflAct’s Ability 

In this section, we analyze how ReflAct success-fully solves tasks, and in Appendix G, we compare the hallucinated action ratio and token length be-tween ReflAct and baseline reasoning frameworks. 

6.4.1 Failure Ratio Comparison Between Reasoning Frameworks 

Building on the discussion of Figure 3 in Section 3.2, we analyze the proportion of tasks failed by the NoThinking, ReAct, and ReflAct agents across 134 tasks in the ALFWorld domain. 

Figure 8: Failure ratio comparison diagram of NoThink-ing, ReAct, and ReflAct on 134 ALFWorld tasks, using GPT-4o and Llama-3.1-8B-Instruct as agent models. 

Figure 8 illustrates the failure distribution among the three agents. Consistent with earlier observations, the NoThinking agent accounts for the largest number of unique failures, especially in tasks where it alone fails. The ReAct agent, while incorporating reasoning, introduces additional fail-ure cases not observed in NoThinking. This sug-gests that ungrounded or incorrect reasoning can lead to novel and potentially harmful errors. No-tably, there are no tasks in which only the ReflAct agent fails. ReflAct fails only in cases where other agents also fail, and does not introduce new failure modes. This highlights the benefit of reflection grounded in the agent’s state and task goal, sug-gesting that reflective reasoning contributes to safer and more reliable decision-making in LLM agents. 

6.4.2 ReflAct Self-Corrects Automatically 

LLM agents, especially when operating in unfa-miliar environments with only partially observable information, are prone to making mistakes. There-fore, it is essential that they possess the ability to self-correct by identifying the cause of their errors and adjusting their behavior accordingly to return to a correct course of action. The example below by a ReflAct agent demonstrates that ReflAct main-tains an internal belief over the current state and continuously aligns its decision-making with the task goal, enabling the agent to recognize mistakes and flexibly recover from them , ultimately guiding itself back onto the correct path. 

Your task is cool some lettuce and put it in countertop.                                                                                                       

> ... Action: take lettuce 1from countertop 2Obs: You pick up the lettuce 1from the countertop 2. Reflection: Iam at countertop 2, holding lettuce 1. Ineed to cool the lettuce before putting it on the countertop to complete the task. Action: cool lettuce 1with fridge 1Obs: Nothing happens. Reflection: Iam at countertop 2, holding lettuce 1. The action to cool the lettuce with the fridge did not work because I need to be at the fridge to perform that action.
> Action: go to fridge 1Obs: The fridge 1is open. In it, ... Reflection: Iam at fridge 1, holding lettuce 1. Ican cool the lettuce now that I’m at the fridge.
> Action: cool lettuce 1with fridge 1Obs: You cool the lettuce 1using the fridge 1. ...

7 Conclusion 

We have proposed ReflAct, a reflection-based rea-soning framework that addresses key limitations of ReAct. While ReAct focuses on next-action thinking, it often fails to maintain coherent internal beliefs about the environment and goal, leading to poor decisions in complex, partially observable tasks. In contrast, ReflAct emphasizes ongoing re-flection on state and goal, enabling more grounded and reliable decision making. Our experiments show that ReflAct consistently outperforms ReAct and other baselines, demonstrating the value of re-flection in long-horizon reasoning. We hope this work inspires further research into more robust and informative reasoning guidance for intelligent agents. 8Limitations 

While ReflAct shows strong performance in in-teractive agent environments, its applicability to other domains such as mathematics and coding remains unexplored. These tasks pose unique chal-lenges: mathematics requires step-by-step deduc-tion, while programming demands consistency in logic, state, and syntax. Extending ReflAct to these areas may require adapting its reflection mecha-nism to better align the current state with task-specific goals. Incorporating structured reason-ing that explicitly supports goal-state alignment could enhance performance, and we consider this a promising direction for future work. In addition, as discussed in Appendix G, Re-flAct results in a modest increase in token length compared to ReAct. To address this, it is worth ex-ploring more efficient formulations that retain the benefits of state-goal reflection while reducing ver-bosity. Possible approaches include compressing reflection outputs, using more concise representa-tions of reasoning steps, or integrating summariza-tion modules to maintain informativeness within a smaller token budget. Finally, there is growing interest in enhancing reasoning with external modules. Incorporating such components into ReflAct could further im-prove its reflection process. For example, an exter-nal verifier might evaluate reflected goals or sug-gest fixes for inconsistencies. Exploring such hy-brid architectures remains a promising direction for future research. 

Ethical Statements 

While LLM Agents represent powerful tools with significant practical applications, they also pose substantial risks if misused or deployed without proper safeguards. Of particular concern is their tendency to hallucinate or generate ungrounded rea-soning, which can lead to unreliable or potentially harmful decisions in real-world contexts. This re-search aims to address these challenges by develop-ing more grounded decision-making frameworks that enhance reliability and reduce hallucination. By focusing on improving the alignment between the agent’s internal beliefs and the actual environ-ment state, our work contributes to the broader goal of creating more trustworthy AI systems that can safely operate in complex, partially observable environments while maintaining consistent goal-directed behavior. 

References 

Ma Chang, Junlei Zhang, Zhihao Zhu, Cheng Yang, Yujiu Yang, Yaohui Jin, Zhenzhong Lan, Lingpeng Kong, and Junxian He. 2024. Agentboard: An an-alytical evaluation board of multi-turn llm agents. 

Advances in Neural Information Processing Systems ,37:74325–74362. Yuri Chervonyi, Trieu H Trinh, Miroslav Olšák, Xi-aomeng Yang, Hoang Nguyen, Marcelo Menegali, Junehyuk Jung, Vikas Verma, Quoc V Le, and Thang Luong. 2025. Gold-medalist performance in solv-ing olympiad geometry with alphageometry2. arXiv preprint arXiv:2502.03544 .Ali Forootani. 2025. A survey on mathematical rea-soning and optimization with large language models. 

arXiv preprint arXiv:2503.17726 .Aaron Grattafiori, Abhimanyu Dubey, Abhinav Jauhri, Abhinav Pandey, Abhishek Kadian, Ahmad Al-Dahle, Aiesha Letman, Akhil Mathur, Alan Schelten, Alex Vaughan, and 1 others. 2024. The llama 3 herd of models. arXiv preprint arXiv:2407.21783 .David Ha and Jürgen Schmidhuber. 2018. World mod-els. arXiv preprint arXiv:1803.10122 .Danijar Hafner, Timothy Lillicrap, Jimmy Ba, and Mo-hammad Norouzi. 2019. Dream to control: Learn-ing behaviors by latent imagination. arXiv preprint arXiv:1912.01603 .Danijar Hafner, Jurgis Pasukonis, Jimmy Ba, and Timo-thy Lillicrap. 2025. Mastering diverse control tasks through world models. Nature , pages 1–7. Shibo Hao, Yi Gu, Haodi Ma, Joshua Jiahua Hong, Zhen Wang, Daisy Zhe Wang, and Zhiting Hu. 2023. Reasoning with language model is planning with world model. arXiv preprint arXiv:2305.14992 .Matthew Hausknecht, Prithviraj Ammanabrolu, Marc-Alexandre Côté, and Xingdi Yuan. 2020. Interactive fiction games: A colossal adventure. In Proceedings of the AAAI Conference on Artificial Intelligence ,volume 34, pages 7903–7910. Matthew J Hausknecht and Peter Stone. 2015. Deep recurrent q-learning for partially observable mdps. In AAAI fall symposia , volume 45, page 141. Leslie Pack Kaelbling, Michael L Littman, and An-thony R Cassandra. 1998. Planning and acting in partially observable stochastic domains. Artificial intelligence , 101(1-2):99–134. Jacky Liang, Wenlong Huang, Fei Xia, Peng Xu, Karol Hausman, Brian Ichter, Pete Florence, and Andy Zeng. 2023. Code as policies: Language model programs for embodied control. In 2023 IEEE In-ternational Conference on Robotics and Automation (ICRA) , pages 9493–9500. IEEE. 

9Zhihan Liu, Hao Hu, Shenao Zhang, Hongyi Guo, Shuqi Ke, Boyi Liu, and Zhaoran Wang. 2023. Rea-son for future, act for now: A principled framework for autonomous llm agents with provable sample efficiency. arXiv preprint arXiv:2309.17382 .Wenjie Ma, Jingxuan He, Charlie Snell, Tyler Griggs, Sewon Min, and Matei Zaharia. 2025. Reasoning models can be effective without thinking. arXiv preprint arXiv:2504.09858 .Junhyuk Oh, Valliappa Chockalingam, Honglak Lee, and 1 others. 2016. Control of memory, active per-ception, and action in minecraft. In International conference on machine learning , pages 2790–2799. PMLR. OpenAI. 2024. Hello gpt-4o. Martin L Puterman. 1990. Markov decision processes. 

Handbooks in operations research and management science , 2:331–434. Shuofei Qiao, Runnan Fang, Ningyu Zhang, Yuqi Zhu, Xiang Chen, Shumin Deng, Yong Jiang, Pengjun Xie, Fei Huang, and Huajun Chen. 2024. Agent planning with world knowledge model. In The Thirty-eighth Annual Conference on Neural Information Process-ing Systems .Rafael Rafailov, Archit Sharma, Eric Mitchell, Christo-pher D Manning, Stefano Ermon, and Chelsea Finn. 2024. Direct preference optimization: Your language model is secretly a reward model. Advances in Neu-ral Information Processing Systems , 36. Andres Rodriguez, Ronald Parr, and Daphne Koller. 1999. Reinforcement learning using approximate belief states. Advances in Neural Information Pro-cessing Systems , 12. Julian Schrittwieser, Ioannis Antonoglou, Thomas Hu-bert, Karen Simonyan, Laurent Sifre, Simon Schmitt, Arthur Guez, Edward Lockhart, Demis Hassabis, Thore Graepel, and 1 others. 2020. Mastering atari, go, chess and shogi by planning with a learned model. 

Nature , 588(7839):604–609. Noah Shinn, Federico Cassano, Ashwin Gopinath, Karthik Narasimhan, and Shunyu Yao. 2024. Re-flexion: Language agents with verbal reinforcement learning. Advances in Neural Information Process-ing Systems , 36. Keisuke Shirai, Cristian C Beltran-Hernandez, Masashi Hamaya, Atsushi Hashimoto, Shohei Tanaka, Kento Kawaharazuka, Kazutoshi Tanaka, Yoshitaka Ushiku, and Shinsuke Mori. 2024. Vision-language inter-preter for robot task planning. In 2024 IEEE Inter-national Conference on Robotics and Automation (ICRA) , pages 2051–2058. IEEE. Mohit Shridhar, Xingdi Yuan, Marc-Alexandre Cote, Yonatan Bisk, Adam Trischler, and Matthew Hausknecht. 2021. {ALFW}orld: Aligning text and embodied environments for interactive learning. In 

International Conference on Learning Representa-tions .Yifan Song, Da Yin, Xiang Yue, Jie Huang, Sujian Li, and Bill Yuchen Lin. 2024. Trial and error: Exploration-based trajectory optimization of llm agents. In Proceedings of the 62nd Annual Meet-ing of the Association for Computational Linguistics (Volume 1: Long Papers) , pages 7584–7600. Mirac Suzgun, Mert Yuksekgonul, Federico Bianchi, Dan Jurafsky, and James Zou. 2025. Dynamic cheat-sheet: Test-time learning with adaptive memory. 

arXiv preprint arXiv:2504.07952 .Mudit Verma, Siddhant Bhambri, and Subbarao Kamb-hampati. 2024. On the brittle foundations of react prompting for agentic large language models. arXiv preprint arXiv:2405.13966 .Lei Wang, Wanyu Xu, Yihuai Lan, Zhiqiang Hu, Yunshi Lan, Roy Ka-Wei Lee, and Ee-Peng Lim. 2023. Plan-and-solve prompting: Improving zero-shot chain-of-thought reasoning by large language models. In 

Proceedings of the 61st Annual Meeting of the As-sociation for Computational Linguistics (Volume 1: Long Papers) , pages 2609–2634. Ruoyao Wang, Peter Jansen, Marc-Alexandre Côté, and Prithviraj Ammanabrolu. 2022. Scienceworld: Is your agent smarter than a 5th grader? In Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing , pages 11279–11298. Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, and 1 others. 2022. Chain-of-thought prompting elicits reasoning in large language models. Advances in neural information processing systems , 35:24824– 24837. Yiran Wu, Tianwei Yue, Shaokun Zhang, Chi Wang, and Qingyun Wu. 2024. Stateflow: Enhancing llm task-solving through state-driven workflows. In First Conference on Language Modeling .Weimin Xiong, Yifan Song, Qingxiu Dong, Bingchan Zhao, Feifan Song, Xun Wang, and Sujian Li. 2025. Mpo: Boosting llm agents with meta plan optimiza-tion. arXiv preprint arXiv:2503.02682 .Shunyu Yao, Jeffrey Zhao, Dian Yu, Nan Du, Izhak Shafran, Karthik R Narasimhan, and Yuan Cao. 2023. React: Synergizing reasoning and acting in language models. In The Eleventh International Conference on Learning Representations .Wangchunshu Zhou, Yuchen Eleanor Jiang, Long Li, Jialong Wu, Tiannan Wang, Shi Qiu, Jintian Zhang, Jing Chen, Ruipu Wu, Shuai Wang, and 1 oth-ers. 2023. Agents: An open-source framework for autonomous language agents. arXiv preprint arXiv:2309.07870 .

10 A Expanded Related Works 

Belief-State Modeling in RL. Reinforcement Learning (RL) has aimed to endow agents with an internal state representation that captures all relevant information from past observations (Ro-driguez et al., 1999). In partially observable en-vironments, this often takes the form of a belief state, a probability distribution over possible world states, which is updated as new observations are received. Kaelbling et al. (1998) describe plan-ning as tracking a sufficient statistic of the history (i.e., the belief), which serves as the agent’s core state for action selection. This approach has been further developed in deep RL, where agents learn to track belief states using recurrent neural net-works (Hausknecht and Stone, 2015), memory-augmented architectures (Oh et al., 2016), and world models (Ha and Schmidhuber, 2018). Vari-ous studies (Hafner et al., 2019; Schrittwieser et al., 2020; Hafner et al., 2025) have demonstrated the ef-fectiveness of belief state modeling, enabling more effective planning and reliable decision-making. 

State Representations in LLMs. Similar to belief-state modeling in RL, recent work on LLMs has explored how internal or external state rep-resentations can support reasoning and planning. One line of research adopts an extrinsic model-ing approach, inspired by the Code-as-Policies paradigm (Liang et al., 2023), in which observa-tions are structured into symbolic formats such as textual summaries, PDDL, or finite state machines, and explicitly injected into the prompt. These de-signs enhance grounding and interpretability in robotic tasks, but they typically rely on predefined code or external modules to maintain and update the state representation (Hao et al., 2023; Shirai et al., 2024; Wu et al., 2024). While prior work investigates whether LLMs internally form task-relevant abstractions, ReflAct advances this line of research by explicitly prompt-ing models to articulate and reflect on such ab-stractions. By encouraging LLMs to generate and reason over goal-conditioned state representations, ReflAct facilitates more grounded and efficient decision-making during interaction. 

Backbone Reasoning Frameworks. The emer-gence of LLMs has introduced new agent design paradigms, especially via prompting-based reason-ing strategies. CoT prompting (Wei et al., 2022) showed that models can handle complex tasks by outlining intermediate steps. ReAct (Yao et al., 2023) extended this to interactive settings by in-terleaving reasoning and action, while Plan-and-Solve (Wang et al., 2023) added high-level plan-ning before stepwise execution. However, recent studies (Ma et al., 2025) argue that these CoT-based approaches are often token-inefficient and prone to hallucinations. We attribute these reliabil-ity issues to the absence of an explicit belief state. ReflAct addresses this by maintaining and reflect-ing belief states to guide reasoning and improve both efficiency and reliability. 

Enhancement Reasoning Modules. Recently, a growing body of research has explored add-on or post-processing modules that operate on top of reasoning backbones to enhance reasoning capa-bilities. Reflexion (Shinn et al., 2024) improves performance by analyzing failed trajectories and storing insights for future use. WKM (Qiao et al., 2024) mitigates hallucinations by grounding deci-sions in a learned world model that reflects realistic dynamics. RAFA (Liu et al., 2023) strengthens the reasoning-acting link by imagining future trajecto-ries and evaluating them with separate Model and 

Critic components, forming a structured loop of planning, action, and feedback. Unlike these ap-proaches, ReflAct is not layered on top of a reason-ing backbone but instead redefines the backbone itself, enabling more efficient reasoning. 

B Another Case of the Problem of Ungrounded Thought 

In addition to the discussion of the ReAct agent’s failure case in Figure 4 in Section 3.2, we examine another failure case in ScienceWorld (Wang et al., 2022). As shown in Figure 9 (1), the agent is tasked with boiling lead. To do this, the agent must find lead, transfer it to a suitable heat source, and then boil it. During the previous steps, the agent successfully located the lead in the workshop. Now, the agent must carry it to the foundry. However, the agent mistakenly assumes that it is already holding the lead and proceeds with the next action based on this false assumption, ultimately resulting in a hallucination. In the same situation, similar to the discussion in Section 3.2, we replace the thought with a re-flection sentence about the current state and task goal, as seen in the right branch of Figure 9. This allows the agent to clearly recognize the current situation, make goal-aware long horizon decisions, and ultimately succeed in the task. 11 Figure 9: Another failure case of ReAct, following Figure 4, is seen in the ScienceWorld task boil lead. The agent finds the lead in the workshop. (1) It mistakenly believes it is holding the lead, proceeds with the task, and fails. (2) After reflecting on its current state in relation to the task goal, the agent correctly recognizes its situation, takes goal-aware actions, and successfully completes the task. 

C Benchmark Details 

• ALFWorld (Shridhar et al., 2021): ALFWorld is a text-based benchmark derived from the AL-FRED dataset, designed to evaluate an agent’s ability to interpret and execute natural language instructions in interactive, multi-step household tasks. It converts embodied vision-and-language tasks into textual form, allowing for assessment of high-level planning, language grounding, and sequential decision making in a simulated envi-ronment. • ScienceWorld (Wang et al., 2022): Science-World is a text-based benchmark for evaluating agents on scientific reasoning and procedural task completion. Grounded in standardized K–12 science curricula, it tests an agent’s ability to fol-low instructions, perform virtual experiments, make causal inferences, and manipulate objects across domains such as physics, chemistry, and biology. Tasks require multi-step interaction, hy-pothesis testing, and language grounding in a dynamic environment. • Jericho (Hausknecht et al., 2020): Jericho is a suite of text-based adventure games, each with distinct environments and roles. Tasks require completing a sequence of implicit subgoals, of-ten in specific order. Since these subgoals often do not follow intuitive causal logic, agents must rely on interaction to model the environment and accurately infer their current state. In ALFWorld, success is measured using a bi-nary signal: agents receive a reward of 1 only when the task is fully completed, and 0 otherwise. In contrast, the official environments of Science-World and Jericho provide both a success flag and a progress reward, which assigns a value between 0 and 1 based on the degree of task completion. However, we discovered a bug in both Science-World and Jericho where the success flag could be incorrectly set even when the progress reward was low or incomplete. For example, in Jericho, a task was sometimes marked as successful even when the agent died during execution. To address this, we adjusted the success criteria: a task was considered successful only if the progress reward was at least 0.7 in ScienceWorld, or exactly 1.0 in Jericho. In our experiments, the setups for ALFWorld and ScienceWorld were based on the official im-plementation by MPO (Xiong et al., 2025) ( https: //github.com/WeiminXiong/MPO ), and we used the same test set for evaluation. The ALFWorld test set consists of 134 tasks across six different household task types, including ‘pick-and-place’, ‘pick-heat-then-place’, and ‘pick-two-and-place’. The ScienceWorld test set includes 211 tasks across 24 different scientific experiment types, including ‘Boil’, ‘Test Conductivity of Unknown Substances’, and ‘Grow Fruit’. The experiments for Jericho were based on the implementation by AgentBoard (Chang et al., 2024) ( https://github.com/hkust-nlp/ AgentBoard ). The Jericho test set consists of 20 tasks, each corresponding to a different game, including 905, Acorncourt, Afflicted, Balances, Dragon, Jewel, Library, Omniquest, Reverb, Snack-time, Zenon, Zork1, Zork2, Zork3, Detective, Night, Pentari, Weapon, Darkhunt, and Loose. 12 D Baseline Details 

D.1 Baselines for Backbone Reasoning Frameworks 

We use the same environment code base and test set for all reasoning frameworks, including ReflAct. For specific environments, we follow existing im-plementations: ALFWorld and ScienceWorld are based on the implementation by MPO (Xiong et al., 2025), and Jericho is based on the implementation by AgentBoard (Chang et al., 2024), as described in detail in the section above. We implement base-line reasoning frameworks using the following in-structions: • Instruction for NoThinking   

> You should directly output the action in this turn.

• Instruction for ReAct   

> You should first think about the current condition and plan for your future actions, and then out-put your action in this turn.

Note that this ReAct instruction is from Song et al. (2024); Xiong et al. (2025). • Instruction for Plan-and-Act   

> You should first think about the given task and plan your approach to the task, and then output the action for this turn.

The one-shot example for ReAct is based on Yao et al. (2023); Xiong et al. (2025) and can be found in Appendix H. For NoThinking, we remove the thought step from all timesteps in the same example. For Plan-and-Act, we retain only the thought from the first timestep ( t = 1 ). We will release the public implementation repository after publication. 

D.2 Baselines for Enhancement Reasoning Modules 

In our experiments, we discuss four enhanced reasoning modules: Reflexion (Shinn et al., 2024) and WKM (Qiao et al., 2024) in Section 6.3, and RAFA (Liu et al., 2023), MPO (Xiong et al., 2025), and ReflAct in Appendix F. We implemented each module based on the official repositories provided by the original papers. For Reflexion, we used the official implementation on top of each environment’s base code: ALFWorld and Science-World from Xiong et al. (2025), and Jericho from Chang et al. (2024). In addition, for WKM, we used the publicly available dataset on Hugging Face ( https://huggingface.co/collections/ zjunlp/wkm-6684c611102213b6d8104f84 ) to reproduce the original setup and conducted experiments using WKM’s world model. • Reflexion (Shinn et al., 2024): https:// github.com/noahshinn/reflexion 

• WKM (Qiao et al., 2024): https://github. com/zjunlp/WKM 

• RAFA (Liu et al., 2023): https://github. com/agentification/RAFA_code 

• MPO (Xiong et al., 2025): https://github. com/WeiminXiong/MPO 

E Resources 

For inference with the Llama3.1-Instruct model, we used one A6000 48GB GPU for the 8B model and two A100 80GB GPUs for the 70B model. For training the WKM world model, we used four A6000 48GB GPUs. 

F More Discussion on Enhancement Modules 

F.1 ReflAct and RAFA 

RAFA (Liu et al., 2023) introduces a next-state prediction framework where a language model re-cursively expands a tree of possible future action-observation trajectories, selecting actions based on the highest estimated value. While this foresight aids long-term reasoning, ReflAct offers practical advantages in efficiency and grounded decision-making by internally modeling the current state. 

> Figure 10: Comparison between RAFA and ReflAct.

13 As shown in Figure 10, RAFA constructs a tree at each time step t, requiring 13 queries to the language model per step with depth d = 2 and branching factor b = 2 : 3 for action sampling, 6 for observation prediction, and 4 for value estima-tion. This overhead grows rapidly with depth due to exponential node expansion. In contrast, ReflAct needs only a single query per step to jointly pro-duce a reflection and action, offering constant cost and greater efficiency when latency or throughput is constrained. Figure 10 also highlights a behavioral difference between the two methods. Given the task "examine the alarmclock with the desklamp" in ALFWorld, both agents observe an alarmclock on desk 2. Re-flAct grounds its reflection in this state and selects the correct action, while RAFA relies on predicted trajectories that miss the action and lead to an un-related exploratory move. This shows that ReflAct aligns decisions more closely with the actual state, achieving more reliable behavior with significantly lower cost via a single LLM call per step. 

F.2 ReflAct and MPO 

Recently, Xiong et al. (2025) proposed a frame-work that enhances LLM agents by generating and refining high-level meta plans based on agent feed-back. The meta plans are initially learned through supervised fine-tuning on expert-generated exam-ples and subsequently optimized via preference-based learning (Rafailov et al., 2024) using feed-back from agent executions. The resulting meta planner can be applied to various agents in a plug-and-play manner without requiring additional retraining. Accordingly, we applied the pub-licly available ALFWorld MPO meta plans from 

https://github.com/WeiminXiong/MPO to No-Thinking, ReAct, and ReflAct, and compared the resulting performance gains. 

> Figure 11: Performance comparison across NoThinking, ReAct, and ReflAct when applying MPO meta-plan.

As shown in Figure 11, applying MPO meta plans to NoThinking and ReAct leads to substan-tial performance improvements. However, no-tably, even with these gains, NoThinking+MPO and ReAct+MPO still fall short of ReflAct’s perfor-mance. This further reinforces previous findings that strengthening the reasoning backbone itself is more crucial than simply adding enhancement modules to ReAct. Applying MPO meta plans to ReflAct results in slight performance gains for GPT-4o, but a minor performance drop for Llama-3.1-8B-Instruct. This may be due to the fact that the meta plans were trained on tasks different from those in the test set; in some out-of-distribution cases, they may offer misleading guidance that negatively impacts the agent’s behavior. The limited effectiveness of meta plans on ReflAct also suggests that its grounded decision-making already enables high-quality planning. 

G More Discussion on ReflAct’s Effects 

G.1 ReflAct Prevents Suboptimality Through Goal-Oriented Reasoning 

> Figure 12: Comparison of ReAct’s Thought and Re-flAct’s Reflection on a Jericho task: ReAct fixates on a found shovel, losing sight of the main goal and failing; ReflAct succeeds through goal-oriented reasoning.

ReflAct enables long-sighted planning by con-tinuously reflecting on the current state and goal. Figure 12 illustrates this with an example in a task where the agent must gather swimming-related items and ultimately reach a cylindrical room. As seen, ReAct fails due to short-sighted reasoning, whereas ReflAct successfully achieves the goal through consistent reflection on the state and ob-jective. 14 G.2 Token Length vs. Hallucination Action Rate in ReAct and ReflAct 

Here, we further compare ReflAct and ReAct in terms of token length and the hallucinated action rate. Specifically, token length refers to the number of tokens in each thought (or reflection) with action generated by the model, normalized by the number of steps to account for variations in agent trajectory length. The hallucinated action rate is defined as the proportion of actions that result in erroneous observations (e.g., "Nothing happens"). Both met-rics were averaged across the four agent models used in our experiments: GPT-4o, GPT-4o-mini, Llama-3.1-8B/70B-Instruct. 

> Figure 13: Comparison of the average token length and average hallucination action rate between ReAct and ReflAct in ALFWorld, ScienceWorld, and Jericho.

Figure 13 shows that ReflAct produces slightly longer token sequences than ReAct, as it incorpo-rates reflection on the current state and goal into its reasoning process. Interestingly, despite the increased token length, the hallucination rate de-creases. This suggests that hallucinations in LLM agents may not arise simply from increased rea-soning (i.e., overthinking), but rather from unstruc-tured or unguided reasoning processes. 15 H Prompt 

H.1 ALFWorld 

1) ReAct 

You are in the middle of a room. Looking quickly around you, you see acabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a countertop 1, a garbagecan 1, a handtowelholder 2, a handtowelholder 1, a sinkbasin 2, a sinkbasin 1, atoilet 1, a toiletpaperhanger 1, and a towelholder 1. Your task is to: put some spraybottle on toilet. Thought: To solve the task, I need to find and take a sparybottle, then put it on toilet. First I need to find a spraybottle. A spraybottle is more likely to appear in cabinet 1-4, countertop 1, toilet 1, sinkbasin 1-2, garbagecan 1. I can check one by one, starting by going to cabinet 1. Action: go to cabinet 1Observation: On the cabinet 1, you see a cloth 1, a soapbar 1, a soapbottle 1. Action: go to cabinet 2Observation: The cabinet 2 is closed. Action: open cabinet 2Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a candle 1, and a spraybottle 2. Thought: Now I find a spraybottle 2. Next, I need to take it. Action: take spraybottle 2 from cabinet 2Observation: You pick up the spraybottle 2 from the cabinet 2. Thought: Now I take a spraybottle 2. Next, I need to put it in/on toilet 1. Action: go to toilet 1Observation: On the toilet 1, you see a soapbottle 2. Action: put spraybottle 2 in/on toilet 1You put the spraybottle 2 in/on the toilet 1. 

Figure 14: Prompt for ALFWorld ReAct 

16 2) ReflAct 

You are in the middle of a room. Looking quickly around you, you see acabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a countertop 1, a garbagecan 1, a handtowelholder 2, a handtowelholder 1, a sinkbasin 2, a sinkbasin 1, atoilet 1, a toiletpaperhanger 1, and a towelholder 1. Your task is to: put some spraybottle on toilet. Reflection: To solve the task, I need to find and take a sparybottle, then put it on toilet. First I need to find a spraybottle. A spraybottle is more likely to appear in cabinet 1-4, countertop 1, toilet 1, sinkbasin 1-2, garbagecan 1. I can check one by one, starting by going to cabinet 1. Action: go to cabinet 1Observation: On the cabinet 1, you see a cloth 1, a soapbar 1, a soapbottle 1. Reflection: Currently, I am at cabinet 1, not holding anything, and am searching for a spraybottle to place on the toilet, but instead I find acloth, a soapbar, and a soapbottle. Action: go to cabinet 2Observation: The cabinet 2 is closed. Reflection: Currently, I am at cabinet 2, not holding anything, but the closed cabinet hinders me from finding the spraybottle needed to place on the toilet. Action: open cabinet 2Observation: You open the cabinet 2. The cabinet 2 is open. In it, you see a candle 1, and a spraybottle 2. Reflection: Currently, I am at cabinet 2 and have found a spraybottle 2, which brings me closer to completing the task of placing it on the toilet. Action: take spraybottle 2 from cabinet 2Observation: You pick up the spraybottle 2 from the cabinet 2. Reflection: Currently I am located at cabinet 2, now holding a spraybottle 2, and I am ready to complete the task of placing the spraybottle on the toilet, as I have obtained spraybottle 2. Action: go to toilet 1Observation: On the toilet 1, you see a soapbottle 2. Reflection: Currently, I am at toilet 1, still holding spraybottle 2, and the task is nearly complete, with only the placement remaining. Action: put spraybottle 2 in/on toilet 1Observation: You put the spraybottle 2 in/on the toilet 1. 

Figure 15: Prompt for ALFWorld ReflAct 

17 H.2 ScienceWorld 

1) ReAct 

Your task is to use chemistry to create green paint. When you are done, focus on the green paint. Thought: To solve the task, I need to find materials to create green paint, use those materials, and focus on the object specified in the task once it is identified. The materials for making green paint are likely to be found in an art studio. Action: look around Observation: This room is called the bedroom. In it, you see: the agent substance called air bed. On the bed is: a mattress. On the mattress is: a white pillow.. closet. The closet door is open. In the closet is: nothing. picture table. On the table is: nothing. You also see: A door to the hallway (that is open) Thought: The bedroom doesn’t have the materials I need. I should go to aplace where paint and painting supplies are likely to be found, such as an art studio. Action: teleport to art studio Observation: You teleport to the art studio. Thought: Now that I’m in the art studio, I should look around to find the necessary materials to create green paint. Action: look around Observation: This room is called the art studio. In it, you see: the agent substance called air large cupboard. The large cupboard door is open. In the large cupboard is: a drawer, a wood cup (containing yellow paint), a wood cup (containing blue paint), a wood cup (containing red paint). table. On the table is: a glass cup (containing nothing). wood cup (containing yellow paint) a wood cup (containing blue paint) wood cup (containing red paint) You also see: A door to the hallway (that is open) Thought: I see blue paint here, which is one of the primary colors needed to mix green paint. I should start by pouring it into an empty container to mix with another color. Action: pour cup containing blue paint in art studio in cup containing nothing Observation: You pour the contents of the wood cup into the glass cup. Thought: Yellow paint is the other primary color needed to mix with blue to create green. I should add the yellow paint to the container with blue paint. Action: pour cup containing yellow paint in art studio in cup containing blue paint in table Observation: You pour the contents of the wood cup into the glass cup. Thought: Now that I have both blue and yellow paint in the same container, Ineed to mix them together to create green paint. Action: mix cup containing blue paint and yellow paint Observation: Blue and yellow paint mix to produce green paint. Thought: The task is to create green paint and then focus on it. Now that the green paint is made, I should focus on the final product. Action: focus on green paint 

Figure 16: Prompt for ScienceWorld ReAct 

18 2) ReflAct 

Your task is to use chemistry to create green paint. When you are done, focus on the green paint. Reflection: To solve the task, I need to find materials to create green paint, use those materials, and focus on the object specified in the task once it is identified. The materials for making green paint are likely to be found in an art studio. Action: look around Observation: This room is called the bedroom. In it, you see: the agent substance called air bed. On the bed is: a mattress. On the mattress is: a white pillow.. closet. The closet door is open. In the closet is: nothing. picture table. On the table is: nothing. You also see: A door to the hallway (that is open) Reflection: Currently, I am in the bedroom, holding nothing and focused on nothing. There are no useful materials here to create the green paint I need to focus on. Action: teleport to art studio Observation: You teleport to the art studio. Reflection: Currently, I am in the art studio, holding nothing and focused on nothing. I need to look for materials to create green paint. Action: look around Observation: This room is called the art studio. In it, you see: the agent substance called air large cupboard. The large cupboard door is open. In the large cupboard is: a drawer, a wood cup (containing yellow paint), a wood cup (containing blue paint), a wood cup (containing red paint). table. On the table is: a glass cup (containing nothing). wood cup (containing yellow paint) a wood cup (containing blue paint) wood cup (containing red paint) You also see: A door to the hallway (that is open) Reflection: Currently, I am in the art studio, not holding anything. I’ve found the primary colors yellow, blue, and red, which can be used to make green paint, the substance I will need to focus on. Action: pour cup containing blue paint in art studio in cup containing nothing Observation: You pour the contents of the wood cup into the glass cup. Reflection: I poured blue paint into the glass cup. I’m now holding it and will next add yellow paint. Action: pour cup containing yellow paint in art studio in cup containing blue paint in table Observation: You pour the contents of the wood cup into the glass cup. Reflection: I’ve added yellow paint to the blue in the glass cup. I’m now holding a mix of blue and yellow paint, ready to be mixed into green. Action: mix cup containing blue paint and yellow paint Observation: Blue and yellow paint mix to produce green paint. Reflection: The task is to create green paint and then focus on it. Now that the green paint is made, I should focus on the final product. Action: focus on green paint 

Figure 17: Prompt for ScienceWorld ReflAct 

19 H.3 Jericho 

1) ReAct 

Goal: You are the warrior Link that needs to save the princess from the castle. Observation: You are at the path leading to the castle. The castle is to your north. There is a barrel in front of you. Thought: To solve the task, I first need to explore my surroundings to gather any useful items. Once prepared, I will move north into the castle, navigate to the princess’s location, interact with the princess and complete the rescue mission. Action: Examine barrel Observation: There is a gleaming elvish sword. Thought: The sword inside the barrel has a gleaming finish, which suggests it is of high quality and possibly enchanted. Taking this sword now will likely increase my chances of handling any immediate challenges. Action: take the sword Observation: The sword is taken Thought: I’m now armed. Advancing north into the castle should provide new opportunities for exploration and reveal the next critical steps. Action: north Observation: Main hall The castle is dimly lit, with lava flowing in many places. There is astaircase leading up to princess bedroom, a door to your north leading to the kitchen hall, and the door you just entered on your south Thought: Before making a move toward any specific direction, I need to evaluate what options are actually available to me right now. It would be helpful to check the possible actions I can take from here. Action: check valid actions Observation: south, north, up, look, examine staircase Thought: Among the available actions, ascending the staircase seems like the most direct route to explore. Since it leads upward and the hall below seems perilous, I’ll proceed to investigate what’s at the top of the stairs. Action: up Observation: Princess’s bedroom. Princess is sleeping in bed. Thought: I’ve entered a bedroom where the princess is lying unconscious. There are likely specific actions I can perform in this situation, and I should understand my options before taking a step that could have consequences. Checking what I can do here would be the most logical next move. Action: check valid actions Observation: wake up the princess, take out sword, down Thought: One of the available actions is to wake the princess, which might change the course of events. It seems like the most immediate and gentle way to interact with her. I’ll go ahead and try that first. Action: wake up the princess Observation: The princess wake up from the coma. Thank you my knight, she says. The task is finished. 

Figure 18: Prompt for Jericho ReAct 

20 2) ReflAct 

Goal: You are the warrior Link that needs to save the princess from the castle. Observation: You are at the path leading to the castle. The castle is to your north. There is a barrel in front of you. Reflection: To solve the task, I first need to explore my surroundings to gather any useful items. Once prepared, I will move north into the castle, navigate to the princess’s location, interact with the princess and complete the rescue mission. Action: Examine barrel Observation: There is a gleaming elvish sword. Reflection: I found a powerful elvish sword in the barrel. Since I currently have no weapons, this sword will be essential for protection once I enter the castle. Action: take the sword Observation: The sword is taken Reflection: I have obtained the elvish sword and am now equipped. With my weapon ready, I should head into the castle to continue the search for the princess. Action: north Observation: Main hall The castle is dimly lit, with lava flowing in many places. There is astaircase leading up to princess bedroom, a door to your north leading to the kitchen hall, and the door you just entered on your south Reflection: I have entered the main hall of the castle. The environment is dangerous with lava present. The staircase likely leads to the princess’s bedroom, which aligns with my goal. I should verify available actions first. Action: check valid actions Observation: south, north, up, look, examine staircase Reflection: The valid actions include going “up,” which matches the staircase that leads to the princess’s bedroom. This is likely the shortest path to the goal. Action: up Observation: Princess’s bedroom. Princess is sleeping in bed. Reflection: I have reached the princess, but she appears to be unconscious or in a coma. I need to determine how to safely wake her to complete the mission. Action: check valid actions Observation: wake up the princess, take out sword, down Reflection: The available actions include “wake up the princess,” which directly supports the goal of saving her. No threat is present, so this is the appropriate move. Action: wake up the princess Observation: The princess wake up from the coma. Thank you my knight, she says. The task is finished. 

Figure 19: Prompt for Jericho ReflAct 

21 I More Case Study 

ALFWorld : clean some soapbar and put it in cabinet. 

ReAct 

Goal: clean some soapbar and put it in cabinet. Thought: To solve the task, I need to find a soapbar, then clean it with sinkbasin, then put it in cabinet. First I need to find a soapbar. Asoapbar is more likely to appear in cabinet 1-4, countertop 1, sinkbasin 1-2, or toilet 1. I can check one by one, starting by going to cabinet 1. Action: go to cabinet 1... Action: go to cabinet 4Observation: You open the cabinet 4. The cabinet 4 is open. In it, you see a candle 1, and a cloth 2. Thought: Now I find a cloth 2 in cabinet 4, which I can use to clean the soapbar. Next, I need to find asoapbar. I will go to countertop 1to check if it contains a soapbar. Action: go to countertop 1Observation: On the countertop 1, you see a soapbar 1, and a soapbottle 1. Thought: Now I find a soapbar 1 on the countertop 1. Next, I need to clean it with sinkbasin. I will go to sinkbasin 1 to clean the soapbar. ∗∗ Ungrounded thought: The agent attempts to go to the sinkbasin without having taken the soapbar. Action: go to sinkbasin 1Observation: On the sinkbasin 1, you see nothing. Thought: Since the sinkbasin 1 is empty, I need to clean the soapbar 1 with something. I will use the cloth 2 from cabinet 4 to clean the soapbar. ∗∗ Hallucination: The agent performs an action without soapbar present. Action: use cloth 2

Observation: Nothing happens. Thought: Since using the cloth 2 did not have any effect, I need to find a way to use it to clean the soapbar. I will go back to the cabinet 4 and take the cloth 2 to use it with the sinkbasin 1. Action: take cloth 2 from cabinet 4Observation: Nothing happens. ... 

# Task Failed ReflAct 

Goal: clean some soapbar and put it in cabinet. Reflection: To solve the task, Ineed to find a soapbar, clean it with sinkbasin, and then put it in cabinet. First, I need to find asoapbar. A soapbar is more likely to appear in cabinet 1-4, countertop 1, or sinkbasin 1-2. I can check one by one, starting by going to cabinet 1. Action: go to cabinet 1... Action: go to countertop 1Observation: On the countertop 1, you see a soapbar 1, and a soapbottle 1. Reflection: Currently, I am at countertop 1, and I have found asoapbar 1, which I need to clean before placing it in the cabinet to complete the task. ∗∗ The agent performs an action that are goal-related and well grounded in the current situation. Action: take soapbar 1 from countertop 1

Observation: You pick up the soapbar 1 from the countertop 1. Reflection: Currently, I am at countertop 1, now holding soapbar 1, which I need to clean before placing it in the cabinet to complete my task. Observation: On the sinkbasin 1, you see nothing. Reflection:Currently, I am at sinkbasin 1, I’m holding a soapbar 1, and I am now ready to clean it before placing it in the cabinet to complete my task. Action: Action: clean soapbar 1with sinkbasin 1Observation: You clean the soapbar 1using the sinkbasin 1. ... 

# Task Succeed 

Figure 20: Case study for ALFWorld 

22 ScienceWorld : Your task is to boil tin. For compounds without a boiling point, combusting the substance is also acceptable. First, focus on the substance. Then, take actions that will cause it to change its state of matter. 

ReAct 

... Action: teleport to workshop Observation: You teleport to the workshop. Thought: Now that I’m in the workshop, I should look around to find tin. The workshop is a place where various projects and repairs are done, so I might find tin here in the form of scraps, sheets, or other objects. Action: look around Observation: This room is called the workshop. In it, you see: ... On the table is: a battery, a green wire, a metal pot (containing asubstance called tin), ... Thought: I found tin in the metal pot on the table! Now that I’ve located the tin, I should focus on it as per the task instructions. Action: focus on tin Observation: You focus on the tin. Thought: Now that I’ve focused on the tin, I need to take actions to boil or combust it. Since the tin is in a metal pot, I can use a heat source to boil it. I see a blast furnace in the foundry, which would be perfect for heating the tin. Ishould teleport back to the foundry and use the blast furnace. ∗∗ Ungrounded thought: The agent confirms the presence of tin and proceeds with planning, but does not actually possess the tin. Action: teleport to foundry Observation: You teleport to the foundry. Thought: Now that I’m back in the foundry, I should move the metal pot containing the tin to the blast furnace and then activate the blast furnace to heat the tin. Action: move metal pot to blast furnace Observation: No known action matches that input. Thought: It seems I made a mistake with the action. I should try again, using a different action to move the metal pot to the blast furnace. ∗∗ Hallucination: Although the agent recognizes the mistake, it continues to attempt the same invalid action. Action: move metal pot to blast furnace 

... 

# Task Failed ReflAct 

... Action: teleport to workshop Observation: You teleport to the workshop. Reflection: Currently, I am in the workshop, holding nothing and focused on nothing. I need to look for tin in this room. Action: look around Observation: This room is called the workshop. In it, you see: ... On the table is: a battery, a green wire, a metal pot (containing asubstance called tin), ... Reflection: Currently, I am in the workshop, holding nothing and focused on nothing. I’ve found a metal pot containing tin on the table, which is the substance I need to focus on and then boil or combust Action: focus on tin Observation: You focus on the tin. Reflection: I am now focused on the tin, which is contained in the metal pot on the table. To boil or combust the tin, I need to apply heat to it. I see a foundry in the environment, which is likely to have a heat source. Action: teleport to foundry ... Reflection: The blast furnace is now activated and ready to be used as aheat source. I need to move the tin from the metal pot in the workshop to the blast furnace in the foundry. 

Action: teleport to workshop Observation: You teleport to the workshop. Reflection: I am now back in the workshop, where the metal pot containing the tin is located. Ineed to move the tin to the blast furnace in the foundry. Action: move metal pot to blast furnace Observation: No known action matches that input. Reflection: I need to move the tin to the blast furnace, but the action is not recognized. Instead, I can pick up the metal pot and then teleport to the foundry. 

Action: pick up metal pot Observation: You move the metal pot to the inventory. Reflection: I am now back in the foundry, with the metal pot containing the tin in my inventory. I can now use the blast furnace to boil or combust the tin. 

... 

# Task Succeed 

Figure 21: Case study for ScienceWorld 

23 Jericho : You are a pizza delivery man. Today you are making a new delivery on your boss’s order. You need to find out by yourself who to deliver. 

ReAct 

... Observation: The note reads: "Stanley, Don’t forget to make your delivery to Mr. Calzone, located at the San Doppleton Courthouse. ... ... Observation: Street, Near Courthouse You are approaching the center of downtown San Doppleton. There is acourthouse to the south. The street runs east and west. Thought: It seems like I’m on the right track, as the courthouse is now visible to the south. I should head south to reach the courthouse and deliver the pizza to Mr. Calzone as instructed in the note. Action: South Observation: Courthouse You are in a crowded courthouse. The street is off to the north. The courtroom is currently abuzz with excitement as it seems that the pre-trial hearing of the infamous gangster, Guido "The Armadillo" Calzone is winding to aclose. Guido and his hotshot lawyer sit placidly at their table, while the flustered young district attorney who is prosecuting the case seems like she’s at her wits’ end. At the moment, the D.A. stands at the front of the courtroom, arguing over alegal point with the judge. Thought: I have arrived at the courthouse where Mr. Calzone is present. Since the courtroom is busy, 

I need to find a way to deliver the pizza to Mr. Calzone without causing a disruption. I should approach him or his lawyer to hand over the pizza box. 

Action: Show people box 

Observation: You can’t see any such thing. Thought: It seems that the action "show people box" was not understood in this context. I need to find amore direct way to deliver the pizza to Mr.Calzone. Since he is present in the courtroom, I should try to give the pizza box directly to him or his lawyer. ∗∗ Mismatched execution: The agent fails to specify the target, leading to another invalid action. Action: Give people box 

Observation: You can’t see any such thing. ... 

# Task Failed ReflAct 

... Observation: The note reads: "Stanley, Don’t forget to make your delivery to Mr. Calzone, located at the San Doppleton Courthouse. ... ... Observation: Street, Near Courthouse You are approaching the center of downtown San Doppleton. There is acourthouse to the south. The street runs east and west. Reflection: I’ve finally found the courthouse, which is located to the south of my current position. This is where I need to deliver the pizza to Mr. Calzone. Now that I’ve located the courthouse, I should proceed south to complete the delivery task. Action: South Observation: Courthouse You are in a crowded courthouse. The street is off to the north. The courtroom is currently abuzz with excitement as it seems that the pre-trial hearing of the infamous gangster, Guido "The Armadillo" Calzone is winding to aclose. Guido and his hotshot lawyer sit placidly at their table, while the flustered young district attorney who is prosecuting the case seems like she’s at her wits’ end. At the moment, the D.A. stands at the front of the courtroom, arguing over alegal point with the judge. Reflection: I’ve entered the courthouse where the pre-trial hearing for Guido "The Armadillo" Calzone is taking place. This is the location where I need to deliver the pizza to Mr. Calzone. Since I’ve found him, I should proceed with delivering the pizza to complete my task. ∗∗ Well-grounded and goal-aligned reasoning: The agent explicitly identifies the recipient and forms avalid, context-aware action. Action: Give pizza box to Guido Calzone 

Observation: Guido grins shiftily and takes the pizza from you. He hands it to his lawyer so he can eat it later. You walk away, congratulating yourself on a job well done. 

# Task Succeed 

Figure 22: Case study for Jericho 

24 Jericho : search for a mug in an inn. 

ReAct 

... Observation: Inside the Inn There are a few patches of mould on the walls and the floorboards creak slightly, but the building seems safe enough. ... You see some tables and chairs. ... You can go west (back outside) or down some steps. You can see a magnificently carved chair here. Thought: I’m inside the inn, and Ineed to find a mug. I should start by examining the tables and chairs to see if there’s a mug lying around. Action: Examine tables and chairs Observation: You can’t see any such thing. ... Action: Examine floorboards Observation: The floor is made of large, rather uneven rough floorboards, on which lie the remains of the scattered rushes once used as a floor covering. Thought: I’ve examined the floorboards, but I didn’t find amug. I should try to find something to pick up, and since I’m in the inn, I should check the inventory again to see if I have any other options, but it seems I’m empty-handed. I should try to find something to pick up. 

Action: Examine stone steps leading down ... Action: Examine the floorboards again Observation: I only understood you as far as wanting to examine the floor. Thought: I’ve tried examining various objects and places in the inn, but I didn’t find a mug. I should try to find something to pick up, and since I’m in the inn, I should check the inventory again to see if I have any other options, but it seems I’m empty-handed. I should try to find something to pick up. ∗∗ Short-sighted planning: The agent repeatedly focuses narrowly on immediate surroundings without reconsidering its strategy in light of prior failures. Action: Examine the rushes on the floor again Observation: I only understood you as far as wanting to examine the floor. ... 

# Task Failed ReflAct 

... Observation: Inside the Inn There are a few patches of mould on the walls and the floorboards creak slightly, but the building seems safe enough. ... You see some tables and chairs. ... You can go west (back outside) or down some steps. You can see a magnificently carved chair here. Reflection: I’ve entered the abandoned inn, the Troll’s Arms, and it appears to be old and dusty, but safe enough. I’ve seen some tables and chairs, and a dark, intricately-carved wooden chair in the corner. Since my goal is to search for a mug in an inn, I should investigate the tables and chairs to see if there’s anything useful. Action: Examine tables and chairs Observation: You can’t see any such thing. ... Action: Examine bar or counter Observation: I only understood you as far as wanting to examine the walls. Reflection: I’ve been trying to find a mug, but that didn’t reveal anything. I should try to think of adifferent approach to find the mug. 

Action: Down Observation: Inn Cellar The cellar seems to have been formed from anatural cavern in the rock under the inn, ... , which will remain cool in the slightly chill air. ... You can go up (to the inn) or west (into the dark tunnel). You can see an ancient silver coin and some barrels here. Reflection: I’ve been trying to find a mug, but so far, I haven’t found anything useful. I should try to think of a different approach to find the mug. The cellar seems like apromising location to search for amug, as it’s a storage area for the inn’s supplies. ∗∗ Reflecting on long-term goal: The agent adapts its exploration strategy based on environmental cues and prior search failures. Action: Examine barrels Observation: The barrels are now no more than rotten staves of dry wood, held together by the woodworm holding hands. You have found a pewter mug. 

# Task Succeed 

Figure 23: Another case study for Jericho 

25