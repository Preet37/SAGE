# Card: LangSmith Datasets — Versioning, Splits, Filtering, Eval Inputs
**Source:** https://docs.langchain.com/langsmith/datasets  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Dataset creation/versioning primitives + identifiers (versions/tags/splits/examples) used as inputs to eval automation.

## Key Content
- **Core objects**
  - **Dataset** = collection of **examples** for repeatable evaluation.
  - **Example structure:**  
    - `inputs: dict` (passed to app)  
    - `reference_outputs: dict` *(optional; used for evaluation, not passed to app)*  
    - `metadata: dict` *(optional; enables filtered views)*
- **Dataset versioning (default = timestamp)**
  - Any **add/update/delete** of examples ⇒ **new dataset version** created automatically.
  - UI: **Examples** tab shows **latest** by default; selecting a past version (by timestamp) shows dataset state then; **examples are read-only** in past versions.
  - **Tests** tab shows experiments across versions (latest shown in Examples; experiments from all versions shown in Tests).
- **Tagging versions (human-readable milestones)**
  - UI: **+ Tag this version** (Examples tab).
  - SDK (Python): `client.update_dataset_tag(dataset_name=..., as_of=<timestamp>, tag="prod")`
  - Rationale: stable named versions (e.g., `"prod"`) for CI / regression testing.
- **Evaluate on a specific version / view**
  - Fetch examples for a version via `list_examples(dataset_name=..., as_of="latest" | <tag> | <timestamp>)`, then pass iterable to `evaluate/aevaluate(data=...)`.
- **Evaluate on filtered/split subsets**
  - Filter by metadata: `list_examples(dataset_name=..., metadata={"desired_key":"desired_value"})`
  - Evaluate on splits: `list_examples(dataset_name=..., splits=["test","training"])`
- **UI workflows to build datasets**
  - Add traces → dataset: from **Tracing Projects**, multi-select runs → **Add to Dataset**, or open run → **Add to → Dataset**.
  - Annotation queue: review/edit run → **Add to Dataset** (hotkey `D`); edits + run metadata carry over.
  - Playground: **Set up Evaluation** → select/create dataset → **+Row**; note: inline creation doesn’t support **nested keys**.

## When to surface
Use when students ask how to reference the *right dataset examples* for automated evaluations (by version tag/timestamp, split, or metadata filter) or how dataset changes affect reproducibility/CI.