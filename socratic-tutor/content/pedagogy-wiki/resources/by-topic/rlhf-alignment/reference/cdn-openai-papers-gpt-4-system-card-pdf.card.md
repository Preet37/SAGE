# Card: GPT-4 System Card — Deployment safety & eval methodology
**Source:** https://cdn.openai.com/papers/gpt-4-system-card.pdf  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Operational safety/deployment practices + evaluation framing (risk areas, mitigations, monitoring, red teaming)

## Key Content
- **Training pipeline (2-stage):** (1) Pre-train on large internet text to predict next token; (2) fine-tune with **RLHF** to produce outputs preferred by human labelers (Intro).
- **Model variants compared:** **GPT-4-early** (instruction-following, minimal mitigations) vs **GPT-4-launch** (fine-tuned for increased helpfulness/harmlessness; reflects mitigations) (Sec. 1.1).
- **Risk areas explicitly evaluated (list):** hallucinations; harmful content; representation/allocation/QoS harms; disinformation/influence ops; weapons proliferation; privacy; cybersecurity; risky emergent behaviors; interactions with other systems; economic impacts; acceleration; overreliance (Sec. 2).
- **Qualitative eval procedure:** iterative “red teaming” (stress/boundary/adversarial testing) starting Aug 2022; **>50 external experts** across domains (fairness, mis/disinfo, chemistry/biorisk, cybersecurity, nuclear, econ, HCI, law, education, healthcare, etc.); iterative rounds as mitigations added (Sec. 2.1.1).
- **Quantitative eval procedure:** internal automated evals for policy categories (e.g., hate, self-harm advice, illicit advice). Prompts designed to elicit each category; outputs labeled via **classifiers + human analysis**; used to compare checkpoints/models (Sec. 2.1.2).
- **Empirical results (hallucinations):** GPT-4-launch scored **+19 percentage points** vs latest GPT-3.5 at avoiding **open-domain** hallucinations; **+29 pp** at avoiding **closed-domain** hallucinations (Sec. 2.2).
- **Mitigation levers used:** reduce policy-violating content in pretraining data; fine-tune to **refuse** illicit instructions; reduce hallucinations using prior usage data; reduce jailbreak surface using prior exploit data; train new risk-vector classifiers integrated into monitoring/enforcement (Sec. 1.1).
- **Emergent/agentic risk eval:** ARC tested autonomous replication/resource acquisition with tool loop; preliminary finding: GPT-4 versions tested **ineffective** at autonomous replication “in the wild” (Sec. 2.9).

## When to surface
Use when students ask how aligned models are evaluated/mitigated for deployment (red teaming, quantitative safety evals, monitoring), or want concrete safety metrics (e.g., hallucination reductions, expert testing scope).