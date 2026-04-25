# Card: LangSmith REST API — Run evals (API-only)
**Source:** https://docs.langchain.com/langsmith/run-evals-api-only  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** LangSmith REST API endpoints + request/response patterns to run experiments/evals without SDKs (auth headers, dataset/session/run/feedback schema)

## Key Content
- **Auth (all requests):** HTTP header `x-api-key: $LANGSMITH_API_KEY`.
- **Core workflow (single experiment/session):**
  1. **Fetch dataset examples** (filter by dataset id):  
     `GET https://api.smith.langchain.com/api/v1/examples` with query `dataset=<dataset_id>`.
  2. **Create experiment = tracer session** (ties runs to dataset):  
     `POST /api/v1/sessions` JSON:  
     - `start_time` (ISO8601 UTC), `reference_dataset_id` (string)  
     - optional: `name`, `description`, `extra.metadata`  
     Response includes `id` = `experiment_id`.
  3. **Create runs for each example** (you must do parent/child + linking):  
     `POST /api/v1/runs` JSON fields:  
     - `id` (uuid hex), `name`, `run_type` (e.g., `"chain"`, `"llm"`)  
     - `inputs` (object), `start_time` (ISO8601 UTC)  
     - **Required for experiments:** `reference_example_id` (example id), `session_id` (experiment id)  
     - optional: `parent_run_id` (to form hierarchy).
  4. **Update/close runs with outputs:**  
     `PATCH /api/v1/runs/{run_id}` JSON: `outputs` (object), `end_time` (ISO8601 UTC).
  5. **Close experiment/session:**  
     `PATCH /api/v1/sessions/{session_id}` JSON: `end_time` (ISO8601 UTC).
- **Add evaluation feedback (scoring):**
  - Query root runs: `POST /api/v1/runs/query` JSON:  
    `session: [experiment_id]`, `is_root: true`, `select: ["id","reference_example_id","outputs"]`.
  - Create feedback: `POST /api/v1/feedback` JSON:  
    `run_id`, `key` (e.g., `"correctness"`), `score` (e.g., `1.0`/`0.0`), optional `comment`.
- **Pairwise/comparative experiments:**
  - Create: `POST /api/v1/datasets/comparative` JSON:  
    `experiment_ids` (list), `reference_dataset_id`, `name`, optional `description`, `extra.metadata`.
  - Fetch: `GET /api/v1/datasets/{dataset_id}/comparative` with `id=<comparative_experiment_id>`.
  - Rank via feedback: `POST /api/v1/feedback` with `key:"ranked_preference"`, `score` (1 preferred else 0), plus `feedback_group_id` and `comparative_experiment_id`.

## When to surface
Use when a student asks how to run LangSmith evaluations without SDKs, how to structure sessions/runs (reference_example_id + session_id), or how to post correctness/ranking feedback via REST endpoints.