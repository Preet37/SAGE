"""Deep Research — multi-agent research and expert outreach.

Agents:
  ResearchAgent      → OpenAlex + Tavily knowledge graph construction
  ValidatorAgent     → multi-step credibility scoring
  ConciergeAgent     → Apollo enrichment + Hunter contact lookup + SendGrid outreach

Each agent is a plain async class with a `run()` method that yields events
through a shared event bus. The orchestrator chains them and exposes the
event stream over SSE for the UI. The classes are designed to also wrap
into `uagents` Agents for Agentverse deployment (see agent_runner.py).
"""
