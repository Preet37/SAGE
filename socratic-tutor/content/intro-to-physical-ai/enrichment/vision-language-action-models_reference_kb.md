## Core Definitions

**Vision-Language-Action (VLA) model**  
As Zitkovich et al. (RT-2) describe it, a VLA model is a *pretrained vision-language model* adapted so that, given images and a natural-language instruction, it outputs **robot actions as text tokens**—i.e., the model’s “language” output is repurposed to represent low-level control commands. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**Robotics Transformer (RT-1)**  
RT-1 is a **language-conditioned vision policy** trained via **imitation learning / behavior cloning** to map a short history of camera images plus a task instruction to **discretized action tokens** for real-robot control in a closed loop. The RT-1 paper formalizes this as learning \(\pi(a_t \mid o_{t-5:t}, \ell)\) from demonstration data. (https://arxiv.org/html/2212.06817v2; https://robotics-transformer1.github.io)

**RT-2**  
RT-2 is a VLA approach that takes a pretrained vision-language model and **co-fine-tunes** it so it can emit **robot action tokens** while retaining broad web-scale visual-linguistic knowledge; the key mechanism is representing actions as text-like integer tokens and training with a mixture of robot trajectories and original web VLM data. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**SayCan**  
SayCan is a planning-and-grounding method that selects the next robot skill by multiplying (i) an LLM’s probability that a skill is a good next step given the instruction (“**Say**”) and (ii) an affordance/success probability for executing that skill in the current state (“**Can**”). The combined score is used greedily step-by-step until “done.” (http://arxiv.org/pdf/2204.01691.pdf)

**Open-vocabulary manipulation**  
In the RT-1/RT-2 context, “open-vocabulary” refers to following **natural-language instructions** that can vary widely (including **unseen instructions/objects**) rather than selecting from a small fixed set of task IDs; RT-1 reports explicit evaluation on **unseen instructions** and RT-2 emphasizes generalization and emergent instruction/object reasoning. (https://arxiv.org/html/2212.06817v2; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**Affordance grounding**  
In SayCan, affordance grounding is the use of a learned estimate \(p(c_\pi \mid s, \ell_\pi)\) (probability a skill completes successfully) to ensure the plan is feasible in the current world state; the paper notes this can be obtained from RL value functions with sparse terminal reward. (http://arxiv.org/pdf/2204.01691.pdf)

---

## Key Formulas & Empirical Results

### RT-1: behavior cloning objective (imitation learning)
RT-1 is trained with behavior cloning minimizing negative log-likelihood of demonstrated actions:  
\[
\min_\theta \; \mathbb{E}_{(o,\ell,a)\sim D}\left[-\log \pi_\theta(a\mid o,\ell)\right]
\]  
- \(o\): observations (RT-1 uses a history window of images)  
- \(\ell\): language instruction  
- \(a\): demonstrated action  
**Claim supported:** RT-1 is an imitation-learned language-conditioned policy (not RL in the main training loop). (https://arxiv.org/html/2212.06817v2)

### RT-1: action/control defaults (implementation-relevant)
- **Input:** history of **6 images** + language instruction.  
- **Action dims:** **11** = 7 arm (x,y,z,roll,pitch,yaw,gripper) + 3 base (x,y,yaw) + 1 **mode** {arm/base/terminate}.  
- **Discretization:** each dim into **256 bins**; trained with categorical cross-entropy (causal masking in Transformer).  
- **Control rate:** closed-loop at **≥ 3 Hz**; inference budget **< 100 ms**.  
**Claim supported:** RT-1 is a tokenized, real-time, closed-loop policy. (https://arxiv.org/html/2212.06817v2; https://robotics-transformer1.github.io)

### RT-1: dataset scale
- **130k** successful demonstration episodes  
- **13 robots**, collected over **17 months**  
- **700+ instructions** (paper mentions **744 instructions**) grouped into **9 skills**  
**Claim supported:** RT-1’s generalization is driven by large, diverse real-robot data. (https://arxiv.org/html/2212.06817v2; https://robotics-transformer1.github.io)

### RT-1: success rates (real robot)
From RT-1 Table 2 (as summarized in the paper and project page):  
- **Seen tasks:** **97%**  
- **Unseen instructions:** **76%**  
- **Distractors:** **83%**  
- **New backgrounds/environments:** **59%**  
**Claim supported:** strong performance on seen tasks and measurable generalization/robustness gaps. (https://arxiv.org/html/2212.06817v2; https://robotics-transformer1.github.io)

### RT-1: diversity vs quantity ablation (key takeaway)
- Reducing data while keeping diversity hurts generalization (example: **51% data → unseen 52%, distractors 39%**).  
- Narrowing diversity (keeping 97% data but only 75% tasks) drops overall performance (example: **All to 54%**, **distractors to 42%**).  
**Claim supported:** **task diversity > raw episode count** for generalization in RT-1. (https://arxiv.org/html/2212.06817v2)

### RT-2: action encoding as text tokens (VLA mechanism)
- Action space: 6-DoF end-effector displacement + gripper extension + **terminate**.  
- Continuous dimensions discretized into **256 uniform bins**.  
- Action represented as **8 integer tokens** in an output string like:  
  **“terminate Δposx Δposy Δposz Δrotx Δroty Δrotz gripper”**  
**Claim supported:** RT-2 turns control into a constrained language modeling problem. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

### RT-2: tokenization choices (practical detail)
- **PaLI-X:** integers up to 1000 have unique tokens → map bins directly to integer tokens.  
- **PaLM-E:** overwrite **256 least-frequent tokens** to serve as action vocabulary (“symbol tuning”).  
**Claim supported:** action-token integration depends on the base VLM tokenizer. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

### RT-2: training recipe (co-fine-tuning)
- Prompt format: **“Q: what action should the robot take to [instruction]? A:”**  
- **Co-fine-tuning** on (robot trajectories + original web VLM data) with **upweighted robot sampling** improves generalization vs robot-only finetuning (reduces forgetting).  
- During robot-action decoding, restrict vocabulary to valid action tokens.  
**Claim supported:** mixing web VLM data is a deliberate anti-forgetting/generalization strategy. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

### RT-2: inference rates
- **55B** model: **1–3 Hz**  
- **5B** model: **~5 Hz**  
**Claim supported:** real-time control is feasible but rate depends on model size/serving. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

### RT-2: evaluation scale + headline results
- **~6,000** real-robot evaluation trajectories across seen + generalization settings.  
- RT-2 generalization: **~2×** improvement over next best baselines (RT-1, MOO) on average; **~6×** over other baselines (e.g., VC-1/R3M variants).  
- Language-Table sim (Table 1): **RT-2-PaLI-3B 90±10** vs **BC-Zero 72±3**, **RT-1 74±13**, **LAVA 77±4**.  
**Claim supported:** RT-2 improves generalization and transfers VLM capabilities into control. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

### SayCan: scoring rule (“Say” × “Can”)
Given instruction \(i\), state \(s\), skill set \(\Pi\), each skill \(\pi\) has label \(\ell_\pi\) and completion event \(c_\pi\). SayCan uses:  
\[
p(c_i \mid i, s, \ell_\pi) \propto p(c_\pi \mid s, \ell_\pi)\cdot p(\ell_\pi \mid i)
\]  
Selection at each step \(n\):  
- \(p_{\text{LLM},\pi} = p(\ell_\pi \mid i, \ell_{\pi_{n-1}},\dots,\ell_{\pi_0})\)  
- \(p_{\text{afford},\pi} = p(c_\pi \mid s_n, \ell_\pi)\)  
- \(p_{\text{combined},\pi} = p_{\text{afford},\pi}\cdot p_{\text{LLM},\pi}\)  
Choose \(\pi_n = \arg\max_\pi p_{\text{combined},\pi}\).  
**Claim supported:** explicit factorization of task-likelihood and feasibility. (http://arxiv.org/pdf/2204.01691.pdf)

### SayCan: empirical benefit of affordance grounding
Mock kitchen (101 tasks, Table 2):  
- **PaLM-SayCan:** Plan **84%**, Execute **74%**  
- **No VF (no affordance grounding):** Plan **67%**  
Real kitchen generalization (Table 2): Plan **81%**, Execute **60%**.  
**Claim supported:** grounding improves planning success and end-to-end execution. (http://arxiv.org/pdf/2204.01691.pdf)

---

## How It Works

### RT-1 (Robotics Transformer) control loop (closed-loop token policy)
1. **Observe**: collect a rolling window of **6 images** from the robot camera(s). (RT-1) (https://arxiv.org/html/2212.06817v2)  
2. **Condition on instruction**: embed the natural-language instruction (RT-1 uses Universal Sentence Encoder per paper). (https://arxiv.org/html/2212.06817v2)  
3. **Vision-language tokenization**: EfficientNet visual features are **FiLM-conditioned** on the instruction embedding to make features task-relevant; TokenLearner compresses tokens. (https://arxiv.org/html/2212.06817v2; https://robotics-transformer1.github.io)  
4. **Transformer policy**: a decoder-only Transformer attends over the resulting tokens and predicts **categorical distributions** over discretized action bins (256/bin per dimension). (https://arxiv.org/html/2212.06817v2)  
5. **Decode action**: choose action tokens (arm/base/mode/terminate) and map bins back to control commands. (https://robotics-transformer1.github.io)  
6. **Execute at ~3 Hz**: apply the action; repeat until **terminate** or max steps. (https://robotics-transformer1.github.io; https://arxiv.org/html/2212.06817v2)

### RT-2 (VLA) training + inference mechanics
**Training (co-fine-tuning)**
1. Start from a pretrained VLM (e.g., PaLI-X or PaLM-E as described). (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)  
2. Convert robot trajectories into supervised examples where:
   - **Input**: image(s) + instruction in a VQA-like prompt:  
     `Q: what action should the robot take to [instruction]? A:`  
   - **Target**: an **8-token** action string (terminate + 6DoF bins + gripper). (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)  
3. **Co-fine-tune** on a mixture of:
   - robot trajectory data  
   - original web VLM data  
   with **upweighted robot sampling** to learn control while reducing catastrophic forgetting of web knowledge. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)  
4. During decoding for robot control, **constrain the output vocabulary** to valid action tokens. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**Inference (closed-loop control)**
1. At each timestep, feed current image(s) + instruction prompt.  
2. Decode the next **action-token string** under the constrained vocabulary.  
3. Convert bins to continuous deltas and execute; repeat at **1–3 Hz (55B)** or **~5 Hz (5B)**. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

### SayCan (LLM planning grounded by affordances)
At each step \(n\) (Algorithm 1 style loop in the paper): (http://arxiv.org/pdf/2204.01691.pdf)
1. Enumerate candidate skills \(\pi \in \Pi\) with language labels \(\ell_\pi\).  
2. Compute **LLM score** \(p(\ell_\pi \mid i, \text{previous chosen skills})\).  
3. Compute **affordance score** \(p(c_\pi \mid s_n, \ell_\pi)\) (probability the skill will succeed in current state).  
4. Multiply: \(p_{\text{combined}} = p_{\text{LLM}}\cdot p_{\text{affordance}}\).  
5. Choose argmax skill, execute it, update state, repeat until “done”.

---

## Teaching Approaches

### Intuitive (no math): “One model that can see, read, and act”
- **RT-1**: “A robot policy that looks at recent camera frames and the instruction, then outputs the next joystick-like command repeatedly until it decides it’s done.”  
- **RT-2**: “Take a big vision-language model that already knows lots from the web, and teach it a new ‘language’: instead of answering with words, it answers with action codes.”  
- **SayCan**: “The LLM proposes what to do next; a separate feasibility model vetoes steps that won’t work right now.”

### Technical (with math): “Tokenized control as conditional sequence modeling”
- RT-1 is behavior cloning minimizing \(\mathbb{E}[-\log \pi_\theta(a\mid o,\ell)]\) with discretized action bins (256/bin). (https://arxiv.org/html/2212.06817v2)  
- RT-2 reframes control as generating an 8-token action string conditioned on image+instruction, trained by co-fine-tuning with web VLM data to reduce forgetting. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)  
- SayCan selects skills by maximizing \(p(\ell_\pi\mid i,\text{history})\cdot p(c_\pi\mid s,\ell_\pi)\). (http://arxiv.org/pdf/2204.01691.pdf)

### Analogy-based: “Translator + constrained output”
- RT-2 is like a translator that converts “what you see + what you’re asked” into a **restricted codebook** (action tokens). The “restricted vocabulary” decoding is like forcing the translator to only output valid opcodes. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)  
- SayCan is like choosing a route using (a) a map of what *should* get you to the destination (LLM) and (b) live traffic/road closures (affordances). (http://arxiv.org/pdf/2204.01691.pdf)

---

## Common Misconceptions

1. **“RT-2 is just RT-1 with more robot data.”**  
   **Why wrong:** RT-2’s defining change is *architectural/training framing*: it adapts a pretrained **vision-language model** to output **actions as text tokens** and uses **co-fine-tuning with web VLM data**; RT-1 is a dedicated robotics Transformer trained on robot demos with a specific tokenization pipeline.  
   **Correct model:** RT-1 = robotics-first BC policy; RT-2 = VLM-first VLA model with action-token language and mixed-data co-finetuning. (https://arxiv.org/html/2212.06817v2; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

2. **“Open-vocabulary means the robot can do any task without training.”**  
   **Why wrong:** RT-1 still shows a gap between **seen (97%)** and **unseen instructions (76%)**, and robustness drops further in new backgrounds (**59%**). RT-2 improves generalization but is still evaluated on specific task distributions and settings.  
   **Correct model:** “Open-vocabulary” here means language variability and some generalization to unseen instructions/objects, not unlimited capability. (https://arxiv.org/html/2212.06817v2; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

3. **“SayCan is end-to-end robot control like RT-1/RT-2.”**  
   **Why wrong:** SayCan selects among a **discrete set of skills** \(\Pi\) using LLM probabilities and affordance probabilities; it is not directly outputting low-level continuous control deltas each timestep.  
   **Correct model:** SayCan = high-level skill sequencing with grounding; RT-1/RT-2 = low-level closed-loop action prediction. (http://arxiv.org/pdf/2204.01691.pdf; https://robotics-transformer1.github.io; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

4. **“Affordances in SayCan are just heuristics.”**  
   **Why wrong:** The paper explicitly interprets affordances as **success probabilities** \(p(c_\pi\mid s,\ell_\pi)\) and notes they can come from **RL value functions** trained with sparse terminal reward.  
   **Correct model:** Affordance grounding is a learned feasibility estimator (often value-function-derived), multiplied with the LLM prior. (http://arxiv.org/pdf/2204.01691.pdf)

5. **“Discretizing actions into tokens makes the robot ‘less continuous’ and therefore can’t do precise control.”**  
   **Why wrong:** Both RT-1 and RT-2 discretize continuous action dimensions into **256 bins** and run in a **closed loop** (RT-1 ≥3 Hz; RT-2 1–5 Hz depending on size), so precision can come from repeated small corrections over time.  
   **Correct model:** Tokenization is a modeling/optimization choice; closed-loop execution can recover fine behavior through sequential corrections. (https://arxiv.org/html/2212.06817v2; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

---

## Worked Examples

### Worked Example 1: Compute SayCan’s next-skill choice from “Say” × “Can”
**Goal:** show the tutor a concrete numeric example of the selection rule.

Suppose instruction \(i\): “Clean the table.” Current state \(s_n\): robot is near sink; table has a sponge and a cup.

Candidate skills \(\Pi\) with labels:
- \(\pi_1\): \(\ell_{\pi_1}=\) “pick up the sponge”
- \(\pi_2\): \(\ell_{\pi_2}=\) “pick up the cup”
- \(\pi_3\): \(\ell_{\pi_3}=\) “wipe the table”

Assume the LLM (task-grounding) gives:
- \(p_{\text{LLM},1}=p(\ell_{\pi_1}\mid i,\text{history})=0.40\)
- \(p_{\text{LLM},2}=0.35\)
- \(p_{\text{LLM},3}=0.25\)

Assume affordance model (world-grounding) gives:
- \(p_{\text{afford},1}=p(c_{\pi_1}\mid s_n,\ell_{\pi_1})=0.90\) (sponge reachable)
- \(p_{\text{afford},2}=0.20\) (cup is behind clutter)
- \(p_{\text{afford},3}=0.10\) (can’t wipe without holding sponge)

Compute combined:
- \(\pi_1\): \(0.40 \times 0.90 = 0.36\)
- \(\pi_2\): \(0.35 \times 0.20 = 0.07\)
- \(\pi_3\): \(0.25 \times 0.10 = 0.025\)

**Decision:** choose \(\pi_1\) (“pick up the sponge”) because it maximizes \(p_{\text{combined}}\). This is exactly the paper’s stepwise argmax rule. (http://arxiv.org/pdf/2204-01691.pdf)

### Worked Example 2: RT-2 action token string (format-level example)
**Goal:** give the tutor something concrete to point to when students ask “what does the model actually output?”

RT-2 represents one timestep’s action as an 8-integer-token string:  
**“terminate Δposx Δposy Δposz Δrotx Δroty Δrotz gripper”**  
where each non-terminate dimension is discretized into **256 bins**. The paper shows example outputs as integer token IDs/bins (e.g., “1 128 91 241 5 101 127 …”). (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

Tutor move: ask the student to identify which token corresponds to “terminate” and why vocabulary restriction during decoding matters (only valid action tokens allowed). (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

---

## Comparisons & Trade-offs

| Approach | What it outputs | Training signal | Strengths (per sources) | Limitations (per sources) | When to choose |
|---|---|---|---|---|---|
| **RT-1** (Robotics Transformer) | Discretized low-level action tokens (11 dims; includes mode/terminate) at **≥3 Hz** | Behavior cloning NLL on robot demos | High seen-task success (**97%**) and decent unseen instruction generalization (**76%**); robust to distractors (**83%**) | Performance drops in new backgrounds (**59%**); depends on diverse robot data | When you want a dedicated real-robot policy trained on large multi-task demo data (https://arxiv.org/html/2212.06817v2) |
| **RT-2** (VLA) | 8-token action string (terminate + 6DoF + gripper), **1–5 Hz** depending on size | Co-fine-tuning on robot + web VLM data; constrained decoding | Improves generalization (~**2×** over RT-1/MOO on average); emergent instruction/object reasoning; ~6k real-robot eval | Requires serving large VLMs; control rate depends on model size | When you want to leverage web-scale VLM knowledge for robot generalization (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf) |
| **SayCan** | Next discrete **skill** from a library \(\Pi\) | Multiply LLM prior and affordance probability | Better planning with grounding (Plan **84%** vs **67%** without VF); real kitchen Plan **81%**, Execute **60%** | Limited by skill library; not direct low-level control | When you have reusable skills and need grounded long-horizon task decomposition (http://arxiv.org/pdf/2204.01691.pdf) |

---

## Prerequisite Connections

- **Behavior cloning / imitation learning basics**: RT-1’s objective is explicitly NLL behavior cloning on demonstrations. (https://arxiv.org/html/2212.06817v2)  
- **Tokenization / discretization of continuous actions**: both RT-1 and RT-2 discretize actions into **256 bins** and treat control as token prediction. (https://arxiv.org/html/2212.06817v2; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)  
- **Closed-loop vs open-loop control**: RT-1 runs at **≥3 Hz** until terminate; RT-2 runs at **1–5 Hz** depending on size. (https://robotics-transformer1.github.io; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)  
- **Planning vs control decomposition**: SayCan is skill-level planning with feasibility grounding, distinct from end-to-end action prediction. (http://arxiv.org/pdf/2204.01691.pdf)

---

## Socratic Question Bank

1. **If RT-1 gets 97% on seen tasks but 59% on new backgrounds, what does that suggest about what it learned—and what it didn’t?**  
   *Good answer:* it learned strong task execution under familiar visual distributions; generalization to distribution shifts (backgrounds/environments) is harder. (https://arxiv.org/html/2212.06817v2)

2. **Why does RT-2 bother to constrain the decoding vocabulary during robot-action generation? What failure would happen otherwise?**  
   *Good answer:* unconstrained decoding could emit arbitrary language tokens not corresponding to valid action bins; constraint ensures outputs map to executable actions. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

3. **In SayCan, can a skill with very high LLM probability still be rejected? Under what numeric condition?**  
   *Good answer:* yes—if affordance \(p(c_\pi\mid s,\ell_\pi)\) is low enough that the product score loses to other skills. (http://arxiv.org/pdf/2204.01691.pdf)

4. **RT-2 co-fine-tunes on robot data plus web VLM data. What problem is that trying to prevent?**  
   *Good answer:* forgetting general VLM knowledge; co-training helps generalization vs robot-only finetuning. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

5. **Both RT-1 and RT-2 discretize actions into 256 bins. Why might closed-loop control make discretization less problematic?**  
   *Good answer:* repeated replanning/corrections each timestep can approximate fine continuous behavior over time. (https://arxiv.org/html/2212.06817v2; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

6. **What’s the key difference between “planning success” and “execution success” in SayCan’s reported results?**  
   *Good answer:* planning success measures whether the chosen skill sequence is correct; execution success includes whether skills actually succeed in the environment (e.g., 84% plan vs 74% execute). (http://arxiv.org/pdf/2204.01691.pdf)

7. **RT-1’s ablation suggests diversity matters more than quantity. What kind of dataset change would increase diversity without increasing episode count?**  
   *Good answer:* add more distinct tasks/instructions/skills while keeping total episodes similar; the paper shows narrowing task diversity hurts performance even with similar data volume. (https://arxiv.org/html/2212.06817v2)

8. **If you had a strong library of robot skills already, would you reach for SayCan or RT-2 first—and why?**  
   *Good answer:* SayCan naturally composes discrete skills with grounding; RT-2 is end-to-end low-level control and may be heavier to deploy. (http://arxiv.org/pdf/2204.01691.pdf; https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

---

## Likely Student Questions

**Q: What exactly are RT-1’s reported success rates on seen vs unseen tasks?** → **A:** RT-1 reports **97%** success on **seen** tasks/instructions and **76%** on **unseen instructions**; robustness tests include **83%** with distractors and **59%** in new backgrounds/environments. (https://arxiv.org/html/2212.06817v2; https://robotics-transformer1.github.io)

**Q: What is RT-1’s action space and how often does it act?** → **A:** RT-1 outputs discretized tokens for **11 action dimensions**: 7D arm (x,y,z,roll,pitch,yaw,gripper) + 3D base (x,y,yaw) + 1 discrete **mode** (arm vs base vs terminate). It runs closed-loop at **~3 Hz** until terminate or max steps. (https://arxiv.org/html/2212.06817v2; https://robotics-transformer1.github.io)

**Q: How does RT-2 represent a robot action as “text”?** → **A:** RT-2 discretizes each continuous action dimension into **256 bins** and outputs an **8-integer-token** string: **terminate, Δposx, Δposy, Δposz, Δrotx, Δroty, Δrotz, gripper**. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**Q: What’s the practical difference between RT-2’s PaLI-X vs PaLM-E tokenization for actions?** → **A:** With **PaLI-X**, integers up to 1000 already have unique tokens so bins can map directly to integer tokens; with **PaLM-E**, RT-2 overwrites the **256 least-frequent tokens** to create an action vocabulary (“symbol tuning”). (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**Q: Why does RT-2 co-fine-tune on web VLM data in addition to robot trajectories?** → **A:** The RT-2 paper states co-fine-tuning on (robot + original web VLM data) with **upweighted robot sampling** improves generalization compared to robot-only finetuning by reducing forgetting of web knowledge. (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

**Q: What is SayCan’s exact scoring rule?** → **A:** For each candidate skill \(\pi\) with label \(\ell_\pi\), compute \(p_{\text{LLM}}=p(\ell_\pi\mid i,\text{history})\) and \(p_{\text{afford}}=p(c_\pi\mid s,\ell_\pi)\); multiply \(p_{\text{combined}}=p_{\text{LLM}}\cdot p_{\text{afford}}\) and pick the argmax each step until “done.” (http://arxiv.org/pdf/2204.01691.pdf)

**Q: What evidence shows affordance grounding helps in SayCan?** → **A:** In the mock kitchen (101 tasks), **PaLM-SayCan** achieves **84% plan / 74% execute**, while removing the value function (“No VF”) drops planning to **67%**. (http://arxiv.org/pdf/2204.01691.pdf)

**Q: How big was RT-2’s evaluation and what’s the headline improvement?** → **A:** RT-2 reports **~6,000 real-robot evaluation trajectories** and states generalization improves by about **~2×** over next best baselines (RT-1, MOO) on average, and **~6×** over other baselines (e.g., VC-1/R3M variants). (https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf)

---

## Available Resources

### Videos
- [Imitation Learning (CS285 Lecture 2)](https://youtube.com/watch?v=zDvcNTVkDxk) — **Surface when:** a student is confused about behavior cloning vs distribution shift vs dataset aggregation (background for why closed-loop robotics policies care about generalization).

### Articles & Tutorials
- [Lilian Weng — Policy Gradient (includes broader RL/IL context)](https://lilianweng.github.io/posts/2018-04-08-policy-gradient/) — **Surface when:** a student needs a refresher on RL notation (states/actions/returns) before discussing value functions as affordances in SayCan.
- [UC Berkeley RAIL CS285 course hub](https://rail.eecs.berkeley.edu/deeprlcourse/) — **Surface when:** the student asks for a rigorous course-style treatment of imitation learning and distribution shift.

---

## Key Sources

- [RT-2: “Robotic Transformer 2” (Zitkovich et al., PMLR)](https://proceedings.mlr.press/v229/zitkovich23a/zitkovich23a.pdf) — definitive source for VLA framing, action-as-text tokenization, co-fine-tuning recipe, and RT-2 evaluation claims.  
- [RT-1 paper (HTML)](https://arxiv.org/html/2212.06817v2) — authoritative for RT-1 objective, architecture defaults, dataset scale, and success-rate tables/ablations.  
- [RT-1 project page](https://robotics-transformer1.github.io) — quick lookup for RT-1 control loop details and headline empirical numbers.  
- [SayCan paper](http://arxiv.org/pdf/2204.01691.pdf) — exact “Say × Can” scoring rule, algorithm loop, and planning/execution results showing the value of affordance grounding.