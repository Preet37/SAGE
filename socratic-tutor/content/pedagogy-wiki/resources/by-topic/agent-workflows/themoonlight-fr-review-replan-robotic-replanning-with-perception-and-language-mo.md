# Source: https://www.themoonlight.io/fr/review/replan-robotic-replanning-with-perception-and-language-models
# Title: RePLan: Robotic Replanning with Perception and Language Models (review)
# Fetched via: trafilatura
# Date: 2026-04-10

This paper introduces REPLAN, a novel framework that enables robots to autonomously replan and adapt their actions online to achieve long-horizon tasks, even in the face of unforeseen obstacles or ambiguous goals. It leverages the strengths of both Large Language Models (LLMs) and Vision Language Models (VLMs) to achieve this.
Core Problem & Motivation:
Current robot planning methods, especially those using LLMs, struggle with real-world uncertainties. LLMs can generate syntactically correct plans but lack "physical grounding," meaning they don't understand the state of the environment. VLMs, on the other hand, can perceive the environment but lack the complex reasoning abilities of LLMs. The paper addresses the need for robots that can:
- Plan for long-horizon tasks (multi-step tasks).
- Verify the correctness of their plans.
- Obtain feedback to adjust plans online (replanning).
- Execute tasks in open-ended environments with minimal human intervention.
REPLAN Framework Overview:
REPLAN is a hierarchical system with five key modules that work together to enable autonomous robotic task completion:
- High-Level LLM Planner: This module takes a user-specified goal (in natural language) as input and generates a list of abstract subtasks. It uses a "ReAct"-like prompting scheme, which allows it to break down complex problems into smaller, more manageable steps. It can handle both specific and open-ended goals. If the initial plan fails, this module can propose new plans, incorporating feedback from the VLM Perceiver.
- VLM Perceiver: This module provides physical grounding by analyzing images of the robot's environment. The High-Level Planner decides what information to query from the Perceiver (e.g., "Is there a kettle in front of the microwave?"). The Perceiver provides answers about object states and attributes, which the Planner then uses to update its world knowledge. It receives very specific prompts for querying information from the scene. It also samples multiple answers to ensure the answers are consistent with the environment.
- Low-Level LLM Planner: This module translates the high-level subtasks into low-level reward functions that the robot can execute. It first generates a motion plan (a natural language description of the actions the robot should take). Then, it translates this motion plan into reward functions (e.g., "minimize the distance between the robot's hand and the apple").
- Motion Controller: This module receives the reward functions and controls the robot's actions to satisfy those functions. The paper uses MuJoCo MPC (MJPC), a real-time predictive controller, for motion control. MJPC takes the reward functions and determines the optimal sequence of actions for the robot to take.
- LLM & VLM Verifier: This module checks the outputs of the High-Level and Low-Level Planners for errors and inconsistencies. It verifies that each step proposed by the planners is necessary to achieve the goal. It also corrects any hallucinations or inaccuracies in the observations made by the Perceiver, ensuring that the plans are consistent with the robot's understanding of the environment. The Verifier constrains the use of VLMs for answering questions about the world.
Core Methodology (Detailed & Technical):
The key innovation of REPLAN lies in its intelligent integration of LLMs and VLMs, along with a robust verification mechanism. Here's a more detailed look at the methodology:
- Hierarchical Planning: The system employs a hierarchical approach, breaking down complex tasks into a sequence of subtasks and then translating those subtasks into low-level control actions. This allows for reasoning at different levels of abstraction.
- Prompt Engineering: The LLMs and VLMs are guided by carefully designed prompts that encourage reasoning and accurate information retrieval. The prompts are tailored to the specific tasks and the capabilities of each module.
- VLM-Driven Feedback Loop: The VLM Perceiver plays a crucial role in providing feedback to the High-Level Planner. The Planner uses this feedback to replan when the robot encounters obstacles or fails to achieve its subtasks. This creates a closed-loop system where the robot can adapt to changing environmental conditions.
- MPC-Based Motion Control: The Motion Controller uses Model Predictive Control (MPC) to generate optimal trajectories for the robot. MPC is a control technique that predicts the future behavior of the system and optimizes the control actions to achieve a desired goal while satisfying constraints. In this case, the cost function to be minimized is the negative of the reward function provided by the Low-Level Planner.
- The control problem is defined as: minimize over future states
x1:T
and control inputsu1:T
the sum of costsc(xt, ut)
from timet=0
toT
, subject to the system dynamicsxt+1 = f(xt, ut)
. xt
is the state vector at time stept
(e.g., robot joint angles, object positions).ut
is the control input vector at time stept
(e.g., motor torques).f
is the transition function that defines how the state evolves from one time step to the next based on the control input. This is derived from the MuJoCo physics engine.c(xt, ut)
is the cost function at time stept
, which is defined as the negative of the sum of weighted rewards:c(xt, ut) = - Σ(wi * ri(xt, ut, ϕi))
, wherewi
is the weight of thei
-th reward,ri
is thei
-th reward function, andϕi
are the parameters of thei
-th reward. These parameters specify the target objects and distances for the reward functions.- The optimization problem is solved using a predictive sampling implementation within MuJoCo.
- The control problem is defined as: minimize over future states
- Verification for Robustness: The LLM Verifier ensures the plans produced are error-free and all the steps are useful for achieving the overall task. The Verifier performs object remapping to ensure that the Perceiver and LLM Planners conform to the same object syntax.
- Multi-Answer Consolidation from the VLM: REPLAN is robust to VLM hallucinations since the LLM consolidates multiple answers from the VLM to generate a summary that is consistent with its object knowledge.
Reasoning and Control (RC) Benchmark:
To evaluate REPLAN's performance, the authors created a new benchmark called the Reasoning and Control (RC) benchmark. It consists of eight long-horizon tasks that require both causal reasoning and exploration. These tasks are designed to be challenging for existing robot planning methods, as they involve unforeseen obstacles, ambiguous goals, and the need for online replanning.
Experimental Results:
The experiments demonstrate that REPLAN significantly outperforms baseline methods, including a Language to Rewards framework. REPLAN achieves a 4x improvement in task completion rates and can successfully adapt to unforeseen obstacles and challenges during task execution. Ablation studies show that each module in the REPLAN pipeline (VLM Perceiver, LLM Verifier, and replanning) is essential for achieving robust performance.
Limitations:
The paper acknowledges that REPLAN's performance depends on the VLM's ability to accurately recognize objects and interpret spatial relationships. The authors also identify failure cases related to communication errors between the LLM and MPC, inconsistencies in LLM reasoning, and limitations in the VLM's ability to provide detailed explanations.
Overall Contribution:
REPLAN offers a promising approach to enabling robots to autonomously plan and execute long-horizon tasks in complex and uncertain environments. The framework's intelligent integration of LLMs