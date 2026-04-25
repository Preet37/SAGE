# Card: ReAct = Interleaved Reasoning + Acting (Thought/Action/Observation)
**Source:** https://research.google/blog/react-synergizing-reasoning-and-acting-in-language-models/  
**Role:** explainer | **Need:** PROCESS/ARCHITECTURE  
**Anchor:** High-level design rationale + walkthrough of the interleaved reasoning/action pattern aligned to the ReAct paper

## Key Content
- **Core pattern (trajectory loop):**  
  **Thought (reasoning trace)** → **Action (text action/tool call)** → **Observation (env feedback)** → repeat.  
  - *Thought* updates the model’s **internal state/context** (does **not** affect environment).  
  - *Action* affects the **external environment** (“Env”) and yields an *Observation*.
- **Design rationale:**  
  - **CoT (reason-only)**: strong reasoning but **ungrounded** (can’t update knowledge via external world).  
  - **Act-only**: can interact but lacks **abstract goal reasoning/working memory** for long horizons.  
  - **ReAct** combines both: **reason→act** (plan/adjust actions) and **act→reason** (gather info to ground reasoning), improving **interpretability/diagnosability/controllability** via human-readable trajectories.
- **Prompting procedure (frozen PaLM-540B):** few-shot in-context examples that include **domain-specific actions** (e.g., “search” for QA; “go to” for navigation) + **free-form reasoning traces**.  
  - If **reasoning-heavy tasks**: **alternate** reasoning and actions across multiple steps.  
  - If **action-heavy decision-making**: include **sparse reasoning**; let the LM decide **asynchronous** placement of thoughts vs actions.
- **Fine-tuning pipeline:** use **ReAct-prompted PaLM-540B** to generate trajectories; **filter to successful trajectories**; fine-tune smaller **PaLM-8B/62B** on them.
- **Empirical results (PaLM-540B prompting):**
  - **HotPotQA (EM, 6-shot):** Standard 28.7; CoT 29.4; Act-only 25.7; **ReAct 27.4**; **Best ReAct+CoT 35.1**.  
  - **FEVER (Acc, 3-shot):** Standard 57.1; CoT 56.3; Act-only 58.9; **ReAct 60.9**; **Best ReAct+CoT 64.6**.  
  - **ALFWorld (2-shot success %):** Act-only 45; **ReAct 71**.  
  - **WebShop (1-shot success %):** Act-only 30.1; **ReAct 40**.
- **Human-in-the-loop:** editing a few **reasoning trace sentences** can redirect behavior (e.g., replace hallucinated thought with hints).

## When to surface
Use when students ask how ReAct differs from CoT or act-only agents, how to structure Thought/Action/Observation prompts, or what concrete benchmark gains ReAct achieved (HotPotQA/FEVER/ALFWorld/WebShop).