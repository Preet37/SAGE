# Card: AgentDojo — Benchmarking Prompt Injection in Tool-Calling Agents
**Source:** https://proceedings.neurips.cc/paper_files/paper/2024/file/97091a5177d8dc64b1da8bf3e1f6fb54-Paper-Datasets_and_Benchmarks_Track.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** AgentDojo methodology + utility/attack-success metrics for prompt-injection attacks/defenses (incl. ablations)

## Key Content
- **Benchmark scale & setup (Abstract, Sec. 3, Table 1):**
  - **97** realistic **user tasks**, **27** injection targets, **629** security test cases (cross-product per environment).
  - **4 environments:** Workspace, Slack, Travel, Banking.
  - **Tools:** total **74** tools (Table 1 lists 24/11/28/11 per env; text also mentions “70 tools”).
  - Tasks can require **up to 18 tool calls**, long contexts: **~7,000 GPT-4 tokens** data + **~4,000** tokens tool descriptions.
- **Metrics (Sec. 3.4):**
  - **Benign Utility** = fraction of user tasks solved with **no attack**.
  - **Utility Under Attack** = fraction of security cases where user task solved **without adversarial side effects** (complement sometimes called **untargeted ASR**).
  - **Targeted ASR** = fraction of security cases where **attacker goal achieved**.
  - **Adaptive attacker (“Max”)** over attacks {Aᵢ}: success on a case if **any** Aᵢ succeeds.
- **Core empirical results (Abstract, Sec. 4, Fig. 8–9, Table 2):**
  - Current LLMs solve **<66%** of tasks even **without attacks** (Abstract).
  - “Important message” injection: best agents see **<25% targeted ASR** (Abstract); Slack suite can reach **92% ASR** for GPT-4o (Fig. 7).
  - **Defense effect:** with an added attack detector, targeted ASR drops to **~8%** (Abstract).
  - **Tool filter defense** (isolation-lite): targeted ASR **7.5%** (Sec. 4.3); fails when task tools suffice for attack (**17%** of cases).
  - **Attacker knowledge ablation (Table 2, targeted ASR):** baseline **45.8%**; both correct user+model **47.7%** (+1.9%); wrong user **23.2%**; wrong model **23.7%**.
  - **Attack phrasing matters:** “Important message” > prior (InjecAgent / ignore-prev / TODO); “Max” adds **~10%** ASR boost (Fig. 8).
  - **Injection position:** end-of-tool-response most effective, up to **~70%** ASR vs GPT-4o (Sec. 4.2).
- **Design rationale (Sec. 3.1):** deterministic, state-based utility/security checks (not LLM judges) to avoid evaluation being hijacked by injections.

## When to surface
Use when students ask how to *measure* agent robustness to prompt injection, compare **utility vs ASR**, or want concrete numbers for defenses like **tool isolation/filtering** and **detectors**.