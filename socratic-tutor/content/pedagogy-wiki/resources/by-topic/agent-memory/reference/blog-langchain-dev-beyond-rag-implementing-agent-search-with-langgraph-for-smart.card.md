# Card: LangGraph Agent Search Loop (Onyx) — cyclical graphs + evolving state
**Source:** https://blog.langchain.dev/beyond-rag-implementing-agent-search-with-langgraph-for-smarter-knowledge-retrieval/  
**Role:** explainer | **Need:** WORKING_EXAMPLE  
**Anchor:** Concrete LangGraph architecture for an agentic loop (search→decompose→answer→refine) showing why cyclical graphs matter and how state evolves across steps

## Key Content
- **Agent Search workflow (high-level loop):**
  1) **Initial search** on original question to gather context.  
  2) **Decompose** into narrower **sub-questions** (disambiguation + focused retrieval), informed by initial search.  
  3) For **each sub-question**, run a multi-step pipeline: **query expansion → search → document validation → reranking → sub-answer generation → sub-answer verification**.  
  4) **Compose initial answer** from retrieved docs + sub-answers.  
  5) If initial answer is lacking, **refinement loop**: re-decompose to address shortcomings using: (a) question + initial answer, (b) sub-questions/answers + unanswerable sub-questions, (c) **entity/relationship/term extraction** from initial search. Then generate **refined answer**.
- **Why LangGraph (design rationale):** flow maps naturally to **Nodes/Edges/State**; needs **control**, **parallelism**, **dependency management**, **streaming**, extensibility (incl. future **human-in-the-loop** and reruns with altered parameters).
- **Parallelism patterns:**
  - **Map-Reduce fan-out** for “identical flows” (e.g., validate each retrieved document in parallel; fan-out updates a bolded state key).
  - **Subgraphs as nodes** for “distinct segments” to avoid unnecessary waiting; they “always use subgraphs as nodes within the parent graph” (not invoked inside a node).
- **State management best practices (Pydantic):**
  - Build graph state by **inheriting** from per-node “update” models (grouped keys, defaults allowed, overlapping keys allowed).
  - **Defaults guidance:** define **input state keys without defaults** (except documented nested-subgraph exceptions). Define **updated keys as `type | None = None`**, except list keys expected to be appended by many nodes.
  - Avoid silent bugs where missing parent→subgraph key mapping + default values yields empty/incorrect state instead of errors.
- **Implementation detail:** prototype built in **~1 week / 1 FTE** to test end-to-end runtime, fan-out parallelization, subgraph parallelization, state management, streaming.

## When to surface
Use when a student asks how to structure a **LangGraph agent loop** (search/decompose/answer/refine), how **cyclical refinement** works, or how to manage **parallel sub-questions + state propagation** safely with subgraphs and Pydantic.