# Card: Blackboard Architecture (Components + Control Alternatives)
**Source:** https://stacks.stanford.edu/file/druid:mq853nj9727/mq853nj9727.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Architecture-level decomposition of blackboard systems with explicit component roles and control-cycle rationale

## Key Content
- **Blackboard architecture = 3 components** (Intro, Fig. 1):  
  1) **Blackboard** (global database / shared solution state), 2) **Knowledge Sources (KSs)** (agents that create/modify blackboard contents), 3) **Control component** (realizes behavior in serial computing environment).
- **Task characteristics suited to blackboards** (Sec. 3.1):  
  (1) complex/ill-structured, large spaces; systematic generation infeasible;  
  (2) **opportunistic**, situation-dependent invocation of diverse knowledge; control decisions made during solving (not pre-set paths);  
  (3) mix of **synthetic + analytic** processes (bottom-up fusion + top-down model-based reasoning).
- **Solution strategies and architectural implications** (Secs. 3.2–4):  
  - **Search**: needs **generator + evaluator**; in HEARSAY-II, KS **action** generates hypotheses; KS **condition** does look-ahead; scheduler performs global evaluation (Fig. 3). Condition/action may be scheduled separately; blackboard can change between them → may require re-evaluation (Sec. 5.3.1).  
  - **Recognition**: **match → apply**; KS condition specifies situations; scheduler selects best **region/event** to process next (Fig. 4).
- **Blackboard structure defaults** (Sec. 5.1): organized into **levels** (abstraction/compositional hierarchies). **Level object as class**, nodes as instances; nodes created dynamically; attribute values may include **credibility, timestamps, history**. **Panels**: multiple hierarchies; common second panel = **control info** (e.g., BB1).
- **KS design pattern** (Sec. 5.2, Fig. 5): **condition + action**; condition often **multi-stage filters**: context-independent **trigger** then context-dependent filters; action modifies solution state and may post goals/expectations.
- **Control design axes** (Sec. 5.3): schedulable entities (whole KS vs condition/action), **event-oriented vs knowledge-oriented scheduling** (Figs. 6–7), posting/noticing events, and where **control data** lives (event records vs scheduling queue vs control panel).

## When to surface
Use when students ask how the **blackboard pattern** decomposes into components, how **agents/KSs coordinate via shared state**, or how **control cycles** differ under **search vs recognition** and **event- vs knowledge-oriented scheduling**.