"""Message types for the Deep Research agent protocol.

These mirror the uAgents Chat Protocol payloads — the in-process orchestrator
uses them as Pydantic models, and the Agentverse-deployable wrappers can use
them as `uagents.Model` definitions (same shape, different base class).
"""
from __future__ import annotations

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ───────── Knowledge graph primitives ─────────


class GraphNode(BaseModel):
    id: str
    type: Literal["paper", "author", "institution", "concept"]
    label: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class GraphEdge(BaseModel):
    source: str
    target: str
    type: Literal["cites", "authored", "affiliated", "topic_similar"]
    weight: float = 1.0


class KnowledgeGraph(BaseModel):
    nodes: list[GraphNode] = Field(default_factory=list)
    edges: list[GraphEdge] = Field(default_factory=list)

    def add_node(self, node: GraphNode) -> None:
        if not any(n.id == node.id for n in self.nodes):
            self.nodes.append(node)

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)


# ───────── Agent task / response messages ─────────


class ResearchTask(BaseModel):
    topic: str
    depth: int = 2  # 1 = papers only; 2 = + Tavily enrichment; 3 = + author graph
    max_papers: int = 25


class ValidationReport(BaseModel):
    confidence_score: float  # 0–1
    citation_density: float
    cross_source_agreement: float
    recency_score: float
    author_credibility: float
    conflicting_evidence: list[str] = Field(default_factory=list)
    recommended_next_queries: list[str] = Field(default_factory=list)
    summary: str = ""


class ExpertProfile(BaseModel):
    id: str  # OpenAlex author id or constructed id
    name: str
    role: Optional[str] = None
    organization: Optional[str] = None
    h_index: Optional[int] = None
    works_count: Optional[int] = None
    cited_by_count: Optional[int] = None
    relevance: float = 0.0
    email: Optional[str] = None
    email_confidence: Optional[float] = None
    apollo_data: dict[str, Any] = Field(default_factory=dict)


class OutreachRequest(BaseModel):
    expert_id: str
    subject: str
    body: str  # html-ish text


class ExpertResponse(BaseModel):
    expert_id: str
    received_at: str  # iso
    text: str
    sentiment: Optional[str] = None


# ───────── Stream events emitted to the UI ─────────


class StreamEvent(BaseModel):
    """Single event in the SSE stream for a research run."""

    agent: Literal["research", "validator", "concierge", "orchestrator"]
    kind: str  # e.g. "log", "graph_update", "validation", "expert", "outreach", "done", "error"
    payload: dict[str, Any] = Field(default_factory=dict)
