# Card: Evals API — Monitoring stored completions for regressions
**Source:** https://developers.openai.com/cookbook/examples/evaluation/use-cases/completion-monitoring  
**Role:** reference_doc | **Need:** DEPLOYMENT_CASE  
**Anchor:** Production-ish workflow: log stored completions, create eval + runs, detect prompt regressions, iterate across prompt/model versions.

## Key Content
- **Logging for later evals (production observability)**
  - Set `store=True` on `client.chat.completions.create(...)` to log requests/responses for later evaluation.
  - Alternative: enable org-wide logging “on by default” in admin data controls: `platform.openai.com/settings/organization/data-controls/data-retention`.
  - Use **metadata** to segment use-cases and versions, e.g. `metadata={"prompt_version": "v1", "usecase": "push_notifications_summarizer"}`.

- **Evals structure (configuration vs execution)**
  - **Eval** = shared configuration: `data_source_config` + `testing_criteria`.
  - **Run** = an execution of an Eval over a specific data source slice (e.g., prompt version), producing a report URL.

- **Data source config (stored completions)**
  - `data_source_config = {"type":"stored_completions","metadata":{"usecase":"push_notifications_summarizer"}}`
  - Variables exposed to graders:
    - `{{item.input}}` = messages sent to the completion call
    - `{{sample.output_text}}` = assistant response text

- **Testing criteria (LLM-as-judge label grader)**
  - Grader type: `"type": "label_model"`, model: `"o3-mini"`.
  - Labels: `["correct","incorrect"]`; passing: `["correct"]`.
  - Grader prompt judges whether summary is “concise and snappy”.

- **Run creation patterns (regression detection)**
  - Compare prompt versions by filtering stored completions:
    - Run v1: `metadata={"prompt_version":"v1"}`
    - Run v2: `metadata={"prompt_version":"v2"}`
  - Generate **new** completions for a different model using stored inputs:
    - `input_messages={"type":"item_reference","item_reference":"item.input"}`
    - `model="gpt-4o"` (vs stored `gpt-4o-mini`)

## When to surface
Use when students ask how to set up an offline evaluation loop for a deployed LLM app: logging outputs, slicing by metadata (prompt/version), grading with an LLM judge, and comparing runs to catch regressions.