# Card: VestaBench (safe long-horizon planning under adversarial constraints)
**Source:** https://aclanthology.org/2025.emnlp-industry.149.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark construction + evaluation framework/metrics for multi-constraint long-horizon embodied planning with safety + adversarial instructions/environments

## Key Content
- **Benchmark design (Section 2):**
  - Built from **VirtualHome** (Evolving Graph Simulator) and **BEHAVIOR-100** (via **Embodied Agent Interface** simulator with an action-transition layer).
  - Two datasets:
    - **VestaBench-VH:** **100 tasks** with safety constraints (physical, electrical, contamination, etc.). **70** tasks in **normal or adversarial environments**; **30** tasks with **adversarial instructions** the agent must avoid.
    - **VestaBench-B50:** **50 tasks** from BEHAVIOR-100 augmented with safety constraints; simulator provides **30 actions**.
  - Key claim: only benchmark (per Table 1) combining **multi-constraint tasks** + **adversarial instructions** + **adversarial environments**, with a **guarantee tasks are safely achievable**.
- **Problem definition (Section 3):**
  - Given instruction **t**, agent **A** outputs plan **P = (a₁,…,aₙ)** with actions **aᵢ ∈ 𝒜**, executed in simulator **S** → final environment graph **G\***.
  - Plan is **successful and safe** iff **predefined success + safety goals/criteria** are satisfied on **G\***.
- **Planning strategies (Section 3, Fig. 3):**
  - **One-go:** generate full multi-action plan once → execute → evaluate.
  - **Stepwise:** interact for **n steps** and **m trials**; each step executes **aᵢⱼ** → observation **oᵢⱼ** + state **Gᵢⱼ**; trajectory **τᵢ = {a₁₁,o₁₁,a₁₂,o₁₂,…}**. End of each trial: critic **J** gives feedback **fᵢ**; repeat until **Done** or trials exhausted.
- **Evaluation metrics (Section 4.1):** report **delivery rate**, **success rate**, **safety rate**.
- **Empirical findings (Section 4.2–4.3):**
  - **Direct one-go** is weakest; **direct stepwise** improves but remains low.
  - **ReAct** improves macro/micro **success & safety** on **VestaBench-VH** by ~**5%** and ~**10%** respectively; minimal gains on **B50**.
  - **ReAct+Critic > ReAct+Reflexion** (attributed to stronger critic model).
  - Complexity hurts safety: for **ReAct+Critic (1)** on **VestaBench-VH**, safety **66.67% (low)**, **48.64% (medium)**, **33.33% (high)**.
  - Adversarial instructions: agents often generate unsafe plans; struggle to distinguish malicious from safe instructions.
- **Defaults/models (Section 4.1):** planning agents include **GPT-4.1-Mini** and **Qwen3-32B**; in **ReAct+Critic (1)**, **GPT-4.1** used as critic.

## When to surface
Use when students ask how to **evaluate LLM agent planning** under **multiple constraints**, **safety goals**, and **adversarial instructions/environments**, or when comparing **one-shot vs stepwise/ReAct-style replanning** with concrete safety/success metrics.