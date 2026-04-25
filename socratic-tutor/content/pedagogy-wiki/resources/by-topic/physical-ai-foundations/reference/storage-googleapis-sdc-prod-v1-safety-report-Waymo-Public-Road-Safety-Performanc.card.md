# Card: Waymo public-road safety metrics & benchmarks
**Source:** https://storage.googleapis.com/sdc-prod/v1/safety-report/Waymo-Public-Road-Safety-Performance-Data.pdf  
**Role:** benchmark | **Need:** DEPLOYMENT_CASE  
**Anchor:** Operational safety metrics + comparative crash/incident rates for public-road autonomous operation

## Key Content
- **Exposure (Abstract):** >6.1M miles automated driving in Phoenix ODD; includes **65,000 miles driverless** (2019–first 9 months 2020).
- **Event accounting (Section 3):** **47 total contact events** = **18 actual** + **29 simulated** (from counterfactual “what-if” post-disengagement simulation). **1 event during driverless operation.**
- **Severity framework (Section 2.3 / Table 1 description):** Events categorized using **ISO 26262 severity classes S0–S3** (S0 no injury expected → S3 possible critical injuries). Waymo estimates injury likelihood using **AIS-linked** probabilities; severity estimation uses **impact object, impact velocity, impact geometry**, and **ΔV / principle direction of force**.
- **Airbag-deployment-level events (Table 1 notes):** **8 most severe events** defined as involving **actual or expected airbag deployment**; **all 8** involved road rule violations/other errors by human road users. **No actual or predicted S2 or S3 events.**
- **Counterfactual simulation workflow (Section 2.3):**
  1) Re-simulate AV post-disengagement using recorded **pre-disengage state** (position/attitude/velocity/acceleration) + **recorded sensor observations** to generate AV’s counterfactual trajectory.  
  2) If needed, simulate other agents using deterministic **human collision-avoidance behavior models** (calibrated on naturalistic collision/near-collision data; response triggered by deviations from expectations).  
  3) Infer contact; assign severity via national crash databases; add scenario to regression library.
- **Collision-mode result (Discussion):** **0 actual or simulated** events in **“road departure, fixed object, rollover”** typology (noted as **27% of US roadway fatalities**).
- **Benchmarking rationale (Comparison benchmarks):** Comparisons to human crash stats are hard due to **ODD specificity**, **different crash definitions** (Waymo includes minor contacts), and **model assumptions**; use **rates per mile** and confidence bounds (6.1M miles supports S0/S1 signal, not rare S2/S3).

## When to surface
Use when students ask how AV safety is quantified on public roads (miles, event rates, severity classes), how disengagement “what-if” simulations work, or how to compare AV crash performance to human benchmarks while controlling for ODD and reporting differences.