"""SAGE 6-agent swarm.

Sub-agents (orchestrated by `orchestrator.Orchestrator`):
  - pedagogy:    chooses teaching strategy (scaffold | socratic | extend)
  - content:     generates the answer via LLM + retrieved sources
  - concept_map: extracts concept nodes/edges from the turn
  - assessment:  produces a check-for-understanding question
  - peer_match:  suggests complementary study peers
  - progress:    computes mastery deltas from verification

LLM provider chain (see `base.LLM.from_env`):
  Anthropic Claude (primary) → ASI1-Mini (Fetch.ai fallback) → Stub (offline)
"""

from app.agents.base import Agent, AgentContext, AgentMessage, LLM  # noqa: F401
from app.agents.orchestrator import Orchestrator  # noqa: F401
