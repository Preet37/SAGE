# Card: Berkeley Function Calling Leaderboard (BFCL) — benchmark scope & evaluation design
**Source:** https://proceedings.mlr.press/v267/patil25a.html  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Standardized evaluation of LLM tool/function-calling (incl. serial/parallel calls, abstention, stateful multi-step), using AST-based validity checking; points to the live leaderboard.

## Key Content
- **Definition (task):** *Function calling / tool use* = an LLM invoking **external functions/APIs/user-defined tools** in response to user queries (agentic capability).
- **Benchmark purpose (design rationale):** Created because there previously was **no standard benchmark** for function calling due to:
  1) difficulty of evaluating whether a function call is **valid**, and  
  2) difficulty acquiring **diverse, real-world functions**.
- **Evaluation coverage (procedures):**
  - Evaluates **serial** and **parallel** function calls.
  - Covers functions across **various programming languages**.
  - Uses a **novel Abstract Syntax Tree (AST) evaluation method** to judge calls; designed to **scale to thousands of functions**.
  - Benchmark construction uses a mix of **expert-curated** and **user-contributed** functions + associated prompts.
  - Includes evaluation of **abstention** and **reasoning in a stateful multi-step agentic setting** (not just single-turn).
- **Empirical takeaway (qualitative result):** Across many models, **state-of-the-art LLMs excel at single-turn calls**, but **memory, dynamic decision-making, and long-horizon reasoning** remain open challenges.
- **Where metrics live:** The paper states BFCL is accessible via the public leaderboard: **gorilla.cs.berkeley.edu/leaderboard.html** (periodically updated).

## When to surface
Use when students ask how tool/function-calling is benchmarked (validity checking, serial vs parallel calls, abstention/stateful evaluation) or when referencing BFCL as the de facto standard leaderboard for function-calling performance.