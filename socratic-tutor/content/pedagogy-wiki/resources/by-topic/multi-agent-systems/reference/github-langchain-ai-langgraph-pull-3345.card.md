# Card: Dynamic Workflow Mode for Conditional Edges (workflow_mode)
**Source:** https://github.com/langchain-ai/langgraph/pull/3345  
**Role:** code | **Need:** PROCESS/ARCHITECTURE  
**Anchor:** PR description of an alternate conditional-edge execution procedure + compile-time flag (`workflow_mode=True`) and requirements (`path_map` or `Literal`)

## Key Content
- **Problem (conditional edges + parallelism):**
  - Workflow expectation: **each node executes only once** unless explicitly handled otherwise.
  - In conditional branching (selector node **A** with branches **Type 1** and **Type 2**) where **both branches converge to node E**, LangGraph’s **parallel processing** can cause **node E to execute only once** (i.e., convergence behavior depends on runtime scheduling/structure rather than intended workflow semantics).
  - Reported discrepancy: adding an extra node **D** after **B** (without changing logical intent) can change whether **E executes once or twice**, implying non-rigorous conditional-edge triggering based on graph shape.

- **Proposed solution / procedure: “Dynamic Workflow Mode”**
  - Add an **Analyzer** that **maintains the directed graph of actual execution paths** during runtime.
  - During execution, **dynamically adjust trigger conditions for subsequent nodes** based on the **actual path taken**, so nodes in the workflow execute **exactly once** per run (unless special logic says otherwise).
  - Rationale: because nodes/paths are **dynamically generated**, **branch paths can’t be fully determined pre-execution**, so path selection must be **dynamic at runtime**.

- **Configuration / defaults:**
  - Enable via compilation: `compile(workflow_mode=True)`.
  - **When `workflow_mode=True`:** must provide **either** `path_map` **or** a `Literal` return type for the conditional function (**only one required**).
  - `path_map`/`Literal` must **cover all possible execution paths**.
  - Default: if `workflow_mode` is unset or `False`, **original LangGraph execution mode** is used (backward compatible).

## When to surface
Use when students ask how LangGraph evaluates/executes **conditional edges**, why **converging branches** can change downstream execution counts, or what `workflow_mode=True` changes at **compile/execution time** (including `path_map`/`Literal` requirements).