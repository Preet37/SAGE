# Card: LangGraph + gotoHuman human-approval (interrupt/resume) lead-email agent
**Source:** https://github.com/gotohuman/gotohuman-langgraph-lead-example  
**Role:** code | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end LangGraph + external human review integration surface (webhook-driven interrupt/resume), with persistence/checkpointing via Postgres env var.

## Key Content
- **Workflow (end-to-end procedure):**
  1. **Trigger** agent with a new lead email address.
     - **API trigger:** `HTTP POST [DEPLOY_URL]/api/agent` with JSON body: `{ "email": "new.lead@email.com" }`.
     - **Manual trigger in gotoHuman:** create a trigger form with a text input field **ID `email`** and configure the same webhook URL.
  2. Agent researches + drafts a personalized outreach email (LangGraph).
  3. Agent **requests human review/approval** in gotoHuman; reviewers see it in **gotoHuman inbox**.
  4. **Webhook callback** is invoked **for each review response** to **resume the graph** (interrupt/resume pattern).
  5. Human can **revise** draft before final send (approval workflow).
- **Review form setup:**
  - Import gotoHuman form template with **ID `OmmAnhbnWmird3oz60q2`**.
  - Configure **webhook URL** (deployment URL) used to resume execution after review.
  - Optional: generate a **short-lived public link** to share with reviewers.
- **Deployment/config defaults (env vars):**
  - `OPENAI_API_KEY=sk-proj-XXX`
  - `GOTOHUMAN_API_KEY=XYZ`
  - `GOTOHUMAN_FORM_ID=abcdef123`
  - `POSTGRES_CONN_STRING="postgres://..."`
- **Design rationale:** use gotoHuman as a **central dashboard** for approving critical actions/providing input; integrates with LangGraph via webhook to enable **durable, resumable** human-in-the-loop execution.

## When to surface
Use when students ask how to implement **human approval gates** in LangGraph with **interrupt/resume**, how to wire **webhooks** for resuming runs, or what minimal **env/config + API trigger** is needed for a working HITL example.