# Card: SayCan scoring = LLM “Say” × affordance “Can”
**Source:** http://arxiv.org/pdf/2204.01691.pdf  
**Role:** explainer | **Need:** CONCEPT_EXPLAINER  
**Anchor:** SayCan scoring rule combining LLM prior over skill sequences with value-function grounding

## Key Content
- **Setup (Section 3):** Given high-level instruction **i**, current state **s**, and a discrete skill set **Π**. Each skill **π ∈ Π** has:
  - language label **ℓπ** (e.g., “pick up the sponge”)
  - affordance / success probability **p(cπ | s, ℓπ)** where **cπ** is Bernoulli “skill completes successfully”.
- **LLM task-grounding:** score each candidate skill label as next step via **p(ℓπ | i)** (in practice conditioned on prior chosen steps appended to prompt).
- **SayCan factorization (Section 3):** probability a skill makes progress on instruction:
  - **p(ci | i, s, ℓπ) ∝ p(cπ | s, ℓπ) · p(ℓπ | i)**  
  Interpreted as **world-grounding × task-grounding**.
- **Selection rule (Section 3 / Alg. 1):**
  - For each step **n**, compute  
    **pLLMπ = p(ℓπ | i, ℓπₙ₋₁, …, ℓπ₀)**  
    **paffordanceπ = p(cπ | sₙ, ℓπ)**  
    **pcombinedπ = paffordanceπ · pLLMπ**  
    Choose **πₙ = argmaxπ pcombinedπ**, execute, update state, repeat until token **“done”**.
- **Affordances via RL value functions (Section 2,4):** with sparse terminal reward **1** on success else **0**, TD-learned value corresponds to affordance probability.
- **Empirical results (Table 2, mock kitchen, 101 tasks):**
  - **PaLM-SayCan:** Plan **84%**, Execute **74%**
  - **No VF (no affordance grounding):** Plan **67%**
  - **Generative + projection:** Plan **74%**
  - **BC NL:** Execute **0%** total; **BC USE:** Execute **9%** total (60% only on single primitives).
- **Real kitchen generalization (Table 2):** Plan **81%**, Execute **60%**.
- **LLM ablation (Table 3):** **PaLM-SayCan 84/74** vs **FLAN-SayCan 70/61** (plan/execute).

## When to surface
Use when students ask how SayCan combines language-model planning with feasibility/affordance grounding, or want the exact scoring rule, algorithm loop, and the quantitative benefit of adding value-function grounding.