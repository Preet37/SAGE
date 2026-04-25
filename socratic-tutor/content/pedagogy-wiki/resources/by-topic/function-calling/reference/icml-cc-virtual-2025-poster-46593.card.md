# Card: Berkeley Function Calling Leaderboard (BFCL) — ICML 2025 Poster
**Source:** https://icml.cc/virtual/2025/poster/46593  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Benchmark setup (what BFCL evaluates + how it scores) for function-calling/tool-use, incl. single-turn and stateful agentic/dialog evaluation.

## Key Content
- **Definition (task):** *Function calling / tool use* = an LLM invoking external functions/APIs/user-defined tools in response to user queries (tool selection + arguments).
- **Benchmark scope (what is evaluated):**
  - **Serial and parallel function calls** (single tool vs multiple tools; sequential vs parallel).
  - **Various programming languages** (tool/function interfaces span multiple languages).
  - **Stateful multi-step “agentic” setting**: evaluates **abstention** (deciding not to call a tool) and **reasoning with memory/dynamic decision-making** over multiple steps.
- **Scoring / evaluation method (procedure):**
  - Uses a **novel Abstract Syntax Tree (AST) evaluation method** to judge whether a function call is valid/correct **by structure**, enabling scaling to **thousands of functions** without executing every tool “for real.”
- **Dataset construction (procedure):**
  - Built from a combination of **expert-curated** and **user-contributed** functions and associated prompts.
- **Design rationale (why these choices):**
  - Addresses two benchmark gaps: (1) difficulty of evaluating whether a function call is valid, and (2) difficulty acquiring **diverse, real-world functions**.
  - AST-based checking is chosen to make evaluation **reliable and scalable**.
- **Empirical takeaway (reported qualitatively in abstract):**
  - **State-of-the-art LLMs excel at single-turn calls**, but **memory, dynamic decision-making, and long-horizon reasoning** remain open challenges in multi-step settings.
- **Access point:** Live leaderboard referenced at **gorilla.cs.berkeley.edu/leaderboard.html**.

## When to surface
Use when students ask how BFCL evaluates tool/function calling (serial/parallel, single-turn vs dialog/agentic), how correctness is checked (AST-based), or what high-level performance gaps BFCL highlights (single-turn strong; multi-step memory/reasoning weaker).