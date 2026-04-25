# Card: StableToolBench — stabilizing ToolBench evaluation & APIs
**Source:** https://aclanthology.org/2024.findings-acl.664.pdf  
**Role:** paper | **Need:** EMPIRICAL_DATA  
**Anchor:** ToolBench instability causes + StableToolBench virtual API server + stable metrics (SoPR/SoWR) and protocols.

## Key Content
- **ToolBench instability evidence (Section 2):**
  - Reproduced Pass Rates on ToolBench I1-Instruction drop vs reported (Table 9):  
    - GPT-3.5-0613+CoT: **41.5 → 35.2** (−32.5%)  
    - ToolLLaMA v2+CoT: **25.0 → 15.0** (−40%)  
    - ToolLLaMA v2+DFS: **57.0 → 34.0** (−40.4%)
  - **API status drift:** only **44.4% success**, **49.2% not available**, **6.4% not authorised** (Table 10). Not-available breakdown: parsing error **52.6%**, not connectable **30.0%**, parameter change **7.3%**, not found **7.2%** (Table 11).
- **Virtual API server (Section 3.1):**
  - **Cache key:** (category, tool, API name, arguments).  
  - **Calling rule:** cache hit → return; else try real API; if real API unavailable → **LLM API simulator**; then **save response back to cache**.
  - Cache sizes (Table 2): before filtration **352,630**, after **164,980**.
  - Simulator uses **gpt-4-turbo**, conditioned on API docs + up to **5 few-shot** cached real calls.
- **Stable evaluation system (Section 3.2):**
  - **Solvable-task filtering:** majority vote of **gpt-4-turbo, gemini-pro, claude-2**; solvable if ≥2 vote solvable. Total tasks **1,100**, solvable **765** (Table 3).
  - **SoPR (Solvable Pass Rate):** evaluate only solvable tasks with **gpt-4-turbo**; answer label → score: **Solved=1, Unsolved=0.5, Unsure=0**.
  - **SoWR:** if one solved & other unsolved → solved wins; otherwise **gpt-4-turbo** decides.
- **Evaluator reliability (Table 8):** GPT-4 Turbo accuracy: solvability **80%**, answer-solving **74%**, comparison **78%** vs GPT-3.5: **65% / 68% / 56%**.
- **Stability under tool failures:** with virtual server, SoPR changes remain within variance even when **50% tools forced down** (Figure 7/Table 12).

## When to surface
Use when students ask how to benchmark tool-use agents reproducibly (API drift, evaluator randomness), or how to design stable tool-call environments and metrics (SoPR/SoWR, caching + simulation).