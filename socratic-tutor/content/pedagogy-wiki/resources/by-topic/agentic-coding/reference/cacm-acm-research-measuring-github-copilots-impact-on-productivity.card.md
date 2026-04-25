# Card: Measuring GitHub Copilot’s Impact on Productivity (telemetry + survey)
**Source:** https://cacm.acm.org/research/measuring-github-copilots-impact-on-productivity/  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Measured productivity impacts + how Copilot usage telemetry relates to perceived productivity (ACM CACM write-up; DOI:10.1145/3633453)

## Key Content
- **Study design (survey + telemetry, 2022 preview):**
  - Survey emailed to **17,420** preview users; **2,047** responses matched to IDE telemetry.
  - Focus period: **4 weeks** leading up to survey completion (most responses within first **2 days**, on/before **Feb 12, 2022**).
  - Survey built on **SPACE**; used **S, P, C, E** (excluded self-reported Activity). Aggregate productivity = **mean of 12 measures** (11 SPACE statements + “I am more productive…”), excluding skipped items.
- **Telemetry event funnel (Table 1):** `opportunity`, `shown`, `accepted`, `accepted_char`, `mostly_unchanged_X` (Levenshtein distance < **33%**) at **X ∈ {30,120,300,600}s**, `unchanged_X` at same X, and `(active) hour`.
- **Core metric formulas (Table 2; “X_per_Y” normalization):**
  - **Acceptance rate** = `accepted_per_shown` = (# accepted completions) / (# shown completions).
  - **Shown rate** = `shown_per_opportunity`.
  - **Acceptance frequency** = `accepted_per_active_hour`.
  - **Contribution speed** = `accepted_char_per_active_hour`.
  - **Persistence rate** = `unchanged_X_per_accepted`; **Fuzzy persistence** = `mostly_unchanged_X_per_accepted`.
- **Key empirical findings:**
  - **Acceptance rate is the strongest positive predictor of perceived productivity**, outperforming persistence-based metrics.
  - PLS regression: **Component 1 explains 43.2%** of variance; **Component 2 explains 21.2%**; both draw strongly from acceptance rate.
- **Controlled experiment (speed):** **95** pro developers, JS HTTP server task.
  - Completion success: **78% (Copilot)** vs **70% (control)**.
  - Time: **1h11m (Copilot)** vs **2h41m (control)** ⇒ **55% faster**; *P* = **.0017**; 95% CI **[21%, 89%]**.

## When to surface
Use when students ask how Copilot productivity is *measured* (telemetry metrics, acceptance/persistence) or want *quantitative* evidence (55% faster experiment; acceptance rate best predictor of perceived productivity).