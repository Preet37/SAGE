# Card: ALFWorld task suite + success metrics (planning benchmark)
**Source:** https://ar5iv.labs.arxiv.org/html/2010.03768  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Task suite definition + standardized success metrics for long-horizon interactive tasks (ALFWorld), enabling numeric comparisons of planning/decomposition methods

## Key Content
- **ALFWorld setup (Section 2):** Parallel aligned environments: **TextWorld** (high-level text actions) + **ALFRED/THOR** embodied simulator (low-level robot primitives). Uses **PDDL** latent state to generate equivalent TextWorld games from ALFRED scenes.
- **Task types + dataset sizes (Table 1):** Pick&Place (train 790 / seen 35 / unseen 24), Examine in Light (308/13/18), Clean&Place (650/27/31), Heat&Place (459/16/23), Cool&Place (533/25/21), Pick Two&Place (813/24/17). **All:** train **3,553**, seen **140**, unseen **134**.
- **Embodied action primitives:** MoveAhead, RotateLeft/Right, LookUp/Down, Pickup, Put, Open, Close, ToggleOn/Off.  
  **TextWorld high-level actions:** `goto {recep}`, `take {obj} from {recep}`, `put {obj} in/on {recep}`, `open/close {recep}`, `toggle {obj}{recep}`, `clean/heat/cool {obj} with {recep}`.
- **Splits definition:** **Seen** = rooms seen in training but new object placements/appearances; **Unseen** = **unseen rooms** with different layouts/receptacles (OOD generalization).
- **Success metrics (Section 4.1):** report **task success rate** and **goal-condition success rate** (ALFRED metric for partial completion; e.g., “put a hot potato on countertop” has 3 goal-conditions: heat something; put potato on countertop; heat potato + put on countertop).
- **Key embodied results (Table 2, All Tasks):** Seq2Seq **6% (15)** seen / **5% (14)** unseen; **BUTLER 19% (31)** seen / **10% (20)** unseen; **BUTLER-Oracle 37% (46)** seen / **26% (37)** unseen. Parentheses = goal-condition success.
- **Training pipeline defaults (Appendix B):** DAgger IL; **50K episodes** (text agents), max **50 steps/episode**, replay buffer **500K episodes**, batch collect **10**, update every **5** steps, sample **64**, LR **0.001**, grad clip **5**, expert assistance anneal **100%→1% over 50K** episodes. Beam-search recovery at eval: beam width **10**, try **top-5** candidates.

## When to surface
Use when students ask how to **evaluate long-horizon agent planning** (success vs partial success), how **seen vs unseen** generalization is defined, or need **benchmark numbers** comparing planning/decomposition approaches on ALFWorld/ALFRED-style tasks.