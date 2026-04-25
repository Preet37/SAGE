# Card: Production agent architecture & deployment tradeoffs
**Source:** https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf  
**Role:** explainer | **Need:** DEPLOYMENT_CASE  
**Anchor:** Concrete architecture guidance for production agents (tools, orchestration, evaluation/monitoring, guardrails) + latency/cost vs reliability tradeoffs

## Key Content
- **Definition (What is an agent):** “Agents are systems that independently accomplish tasks on your behalf.” Key characteristics:  
  1) **LLM controls workflow execution** (decides, recognizes completion, can proactively correct; on failure can **halt + transfer control to user**).  
  2) **Tool access** to gather context + take actions; **dynamic tool selection** within **guardrails**. (Sec. “What is an agent?”)
- **When to build an agent (use-case filter):** prioritize workflows that resisted deterministic automation:  
  - **Complex decision-making** (e.g., refund approval)  
  - **Difficult-to-maintain rules** (e.g., vendor security reviews)  
  - **Heavy unstructured data** (e.g., insurance claim processing) (Sec. “When should you build an agent?”)
- **Core components (architecture):** **Model + Tools + Instructions** (Sec. “Agent design foundations”).
- **Model selection procedure (latency/cost vs accuracy):**  
  1) **Set up evals** to establish a **performance baseline**  
  2) Start with **most capable model** for all tasks  
  3) **Swap in smaller/faster models** where acceptable to optimize **cost + latency** (Sec. “Selecting your models”).
- **Tool taxonomy:** **Data tools** (retrieve context), **Action tools** (write/execute changes), **Orchestration tools** (agents as tools). Standardize + document + test tools for reuse/versioning. (Sec. “Defining tools”)
- **Agent loop / run exit conditions (Agents SDK):** `Runner.run()` loops until either:  
  1) **final-output tool** invoked (specific output type), or  
  2) model returns a response **without tool calls**. (Sec. “Single-agent systems”)
- **Orchestration defaults:** start **single-agent**, add tools incrementally; move to **multi-agent** when:  
  - **Complex logic** (many if/then branches)  
  - **Tool overload** due to overlapping/similar tools (note: some succeed with **>15 distinct tools**, others struggle with **<10 overlapping**). (Sec. “When to consider creating multiple agents”)
- **Multi-agent patterns:**  
  - **Manager (agents as tools):** one manager delegates via tool calls; best when one agent should control workflow + user interaction.  
  - **Decentralized handoffs:** peer agents transfer control; good for **triage**. (Sec. “Multi-agent systems”)
- **Guardrails + human intervention triggers:**  
  - Layer guardrails: **(1) data privacy/content safety**, **(2) add based on real failures**, **(3) optimize security + UX**.  
  - **Risk-rate tools** (low/medium/high) using: read vs write, reversibility, permissions, financial impact; use ratings to **pause checks** or **escalate**.  
  - Human intervention triggers: **exceeding failure thresholds** (retry/action limits) and **high-risk actions** (e.g., cancel orders, large refunds, payments). (Guardrails section)

## When to surface
Use when students ask how to design/deploy an LLM agent in production: choosing models for cost/latency, structuring tools/instructions, deciding single vs multi-agent orchestration, defining run loops/exit conditions, and implementing guardrails + human-in-the-loop escalation.