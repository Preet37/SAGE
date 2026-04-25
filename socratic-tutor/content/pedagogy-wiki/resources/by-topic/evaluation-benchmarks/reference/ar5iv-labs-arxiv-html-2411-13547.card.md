# Card: SpecTool tool-use error taxonomy + metrics
**Source:** https://ar5iv.labs.arxiv.org/html/2411.13547  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Quantitative taxonomy + measurement of tool-use failure modes (schema/argument/format vs planning/selection), with model breakdowns and feedback-based evaluation.

## Key Content
- **SpecTool dataset (Section 4):** 150 human-annotated tool-use queries across **10 environments** (Tools, Movies, Travel, Sports, Entertainment, Data, Social, Media, Weather, Video Images; table also lists Patent, Spaceflight). Overall averages: **6.8 interactions/query**, **6.2 APIs/query**. Example env stats: Movies **30 queries**, **11 avg interactions**, **11.5 avg APIs**; Patent **20**, **6**, **7.2**; Spaceflight **25**, **9**, **10**.
- **7 error patterns (Section 3):**
  - **IAC** Insufficient API Calls (too few calls to complete task)
  - **IAV** Incorrect Argument Value (incl. missing required args)
  - **IAN** Incorrect Argument Name (hallucinated arg names)
  - **IAT** Incorrect Argument Type
  - **RAC** Repeated API Calls (exact repeats)
  - **IFN** Incorrect Function Name (hallucinated tool)
  - **IFE** Invalid Format Error (violates required parseable format)
- **Evaluation workflow (Section 5):** deterministic environments; agent gets instructions + tool list + format requirements. A **constructive feedback mechanism** checks: (1) parse/format, (2) action in allowed action space (else list valid actions), (3) argument validity (else list valid args + descriptions), (4) argument types (else specify correct types). Only then execute tool and feed observation back.
- **Metrics (Section 6):** Let **N** = max steps; **GT** = labeled ground-truth trajectories.
  - For **IFN/IAN/IAT/IFE/RAC**: error accuracy = **1 − (# API calls exhibiting that error / N)**.
  - For **IAC/IAV**: computed vs each labeled trajectory **g**: **1 − (# API calls with errors w.r.t. GT trajectory g / N)**.
  - Higher metric = fewer errors; aligned with success rate.
- **Key empirical results (Table 3):** Success rates: **GPT-4-0125-preview 0.71** (best), **xLAM-8x22b 0.68**, **xLAM-7b 0.64**, **Code-Llama-13b 0.54**, **GPT-3.5-turbo-1106 0.53**, **Meta-Llama3-8b 0.27**, **Vicuna-13b-16k 0.16**, **Mixtral-8x7b 0.10**. Example error metrics for GPT-4-0125: **RAC 1.00, IFE 1.00, IAC 0.84, IAV 0.94, IAN 0.94, IFN 0.94**.
- **Design rationale (Sections 1–2, 6–7):** prior benchmarks mostly report success-only; SpecTool adds **diagnostic error breakdown**, **multiple valid GT trajectories**, and **feedback** to expose brittle tool-call failures (schema/format/selection) that propagate downstream.

## When to surface
Use when students ask how to **evaluate/diagnose agent tool-calling reliability**, distinguish **planning vs schema/argument/format errors**, or want **quantitative comparisons** of tool-use failure modes across LLMs and the impact of **feedback/retries**.