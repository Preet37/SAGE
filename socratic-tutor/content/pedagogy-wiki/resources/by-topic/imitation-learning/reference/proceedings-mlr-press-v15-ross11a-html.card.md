# Card: DAgger = No-Regret Reduction for Imitation Learning
**Source:** https://proceedings.mlr.press/v15/ross11a.html  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** DAgger no-regret reduction and performance guarantee (dataset aggregation procedure + bound relating learned policy loss to online learning regret and expert loss).

## Key Content
- **Problem setting (sequential prediction / imitation learning):** future observations depend on previous predictions/actions ⇒ i.i.d. supervised learning assumptions fail; leads to compounding errors under **distribution shift** (train on expert states, test on learner-induced states). (Abstract)
- **Core algorithm (DAgger; iterative dataset aggregation):**
  - Iterate training while collecting data from the **current learned policy’s induced state distribution**.
  - Query the **expert** for the correct action/label on visited states.
  - **Aggregate** all collected (state, expert-action) pairs across iterations into a growing dataset.
  - Train a **single stationary deterministic policy** on the aggregated dataset each iteration. (Abstract)
- **Reduction to online learning / no-regret view:**
  - Treat each iteration as an online learning round with loss defined on the states visited by the current policy.
  - If the underlying learner is **no-regret**, then the procedure “must find a policy with good performance under the distribution of observations it induces” in sequential settings. (Abstract)
- **Design rationale vs prior approaches:**
  - Avoids training **non-stationary** or **stochastic** policies.
  - Avoids requiring a **large number of iterations** compared to some earlier methods; aims for stronger guarantees in non-i.i.d. sequential prediction. (Abstract)
- **Empirical claim (no numbers in excerpt):** reported to outperform previous approaches on **two challenging imitation learning problems** and a **benchmark sequence labeling** task. (Abstract)

## When to surface
Use when students ask why behavior cloning fails under distribution shift, what DAgger does differently, or how DAgger connects imitation learning to no-regret online learning guarantees.