# Card: Waymo Safety Case (AUR) structure + evidence credibility
**Source:** https://assets.ctfassets.net/e6t5diu0txbw/66jOjPtNIjzawaK0ZjpU3q/7f081b392cf29a3355c97d0d758fe6cf/Waymo_Safety_Case_Approach.pdf  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Safety-case structure: hazard/risk framing, safety argumentation, evidence types (simulation + on-road) for deployment

## Key Content
- **Safety case definition (UL 4600:2022):** “Structured argument, supported by a body of evidence… that a system is safe for a given application in a given environment.”
- **Top-level goal:** **Absence of Unreasonable Risk (AUR)**; treated as a **risk assessment** problem requiring explicit **Acceptance Criteria (AC)** + **Validation Targets** (ISO 21448:2022; ISO/AWI TS 5083).
- **Key formula (risk):**  
  **Risk = P(harm) × Severity(harm)** (ISO 26262:2018 framing).  
  Variables: **P(harm)** probability of harm; **Severity(harm)** magnitude of harm.
- **Hazard decomposition (Section 2.2):** pin residual risk to 3 hazard categories:  
  1) **Architectural** (e.g., sensor placement blindspots)  
  2) **Behavioral** (e.g., unsafe proximity / driving behavior)  
  3) **In-service operational** (e.g., cargo securement, malicious access)
- **Causal chain framing (Section 2.2.1):** scenario triggering conditions → hazardous causal element/behavior → hazard manifestation → harm; risk influenced by **exposure** + **controllability** (ISO concepts).
- **Behavioral AC framework = 5D coverage space (Section 2.3):**  
  1) **Severity potential** (injury severity; AIS scale **1–6**)  
  2) **Conflict role** (ADS as **initiator** vs **responder**)  
  3) **Behavioral capability**: **regulatory compliance**, **conflict avoidance**, **collision avoidance**  
  4) **ADS functionality status**: **nominal** vs **degraded**  
  5) **Level of aggregation**: **event-level** + **aggregate-rate** ACs (use both; aggregates alone can miss rare scenario risks)
- **Safety determination lifecycle (Section 3.1):** (1) safety-by-design development → (2) readiness review using **on-road data (10+ years)** + **simulation** + expert judgment; failures to meet targets delay approval → (3) post-deploy monitoring for continuous confidence growth.
- **Credibility structuring (Section 4 overview):** **Case Credibility Assessment (CCA)** = credibility of **argument** (top-down) + credibility of **evidence** (bottom-up) + implementation credibility check.

## When to surface
Use when students ask how an L4 autonomous system justifies deployment safety: how hazards are categorized, how acceptance criteria/targets are set, and how simulation + on-road evidence is organized into a credible safety argument.