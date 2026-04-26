"""Research Agent — builds a knowledge graph from OpenAlex + Tavily."""
from __future__ import annotations

from collections import Counter
from typing import AsyncIterator

from ..clients.openalex import OpenAlexClient
from ..clients.tavily import TavilyClient
from ..protocol import (
    GraphEdge,
    GraphNode,
    KnowledgeGraph,
    ResearchTask,
    StreamEvent,
)


class ResearchAgent:
    name = "research"

    def __init__(
        self, openalex: OpenAlexClient, tavily: TavilyClient
    ) -> None:
        self.openalex = openalex
        self.tavily = tavily

    async def run(self, task: ResearchTask) -> AsyncIterator[StreamEvent]:
        """Build a knowledge graph for the topic. Yields stream events."""

        graph = KnowledgeGraph()

        yield StreamEvent(
            agent=self.name,
            kind="log",
            payload={"message": f"Searching OpenAlex for: {task.topic}"},
        )

        # Step 1: papers from OpenAlex
        try:
            works = await self.openalex.search_works(task.topic, per_page=task.max_papers)
        except Exception as e:
            yield StreamEvent(
                agent=self.name,
                kind="error",
                payload={"message": f"OpenAlex error: {e}"},
            )
            works = []

        yield StreamEvent(
            agent=self.name,
            kind="log",
            payload={"message": f"OpenAlex returned {len(works)} works."},
        )

        author_relevance: Counter[str] = Counter()
        author_meta: dict[str, dict] = {}

        for w in works:
            wid = w.get("id", "")
            if not wid:
                continue
            graph.add_node(
                GraphNode(
                    id=wid,
                    type="paper",
                    label=w.get("title") or "(untitled)",
                    metadata={
                        "year": w.get("publication_year"),
                        "doi": w.get("doi"),
                        "cited_by_count": w.get("cited_by_count", 0),
                        "openalex_url": wid,
                        "concepts": [
                            c.get("display_name")
                            for c in (w.get("concepts") or [])[:5]
                        ],
                    },
                )
            )

            for auth in (w.get("authorships") or [])[:5]:
                a = (auth.get("author") or {})
                aid = a.get("id")
                if not aid:
                    continue
                inst = (auth.get("institutions") or [])
                inst0 = inst[0] if inst else {}
                graph.add_node(
                    GraphNode(
                        id=aid,
                        type="author",
                        label=a.get("display_name") or "(unknown author)",
                        metadata={
                            "orcid": a.get("orcid"),
                            "institution": inst0.get("display_name"),
                            "country": inst0.get("country_code"),
                        },
                    )
                )
                graph.add_edge(GraphEdge(source=aid, target=wid, type="authored"))
                author_relevance[aid] += 1 + (w.get("cited_by_count") or 0) // 25
                author_meta[aid] = {
                    "name": a.get("display_name"),
                    "institution": inst0.get("display_name"),
                }

                if inst0.get("id"):
                    graph.add_node(
                        GraphNode(
                            id=inst0["id"],
                            type="institution",
                            label=inst0.get("display_name") or "(institution)",
                            metadata={"country": inst0.get("country_code")},
                        )
                    )
                    graph.add_edge(
                        GraphEdge(source=aid, target=inst0["id"], type="affiliated")
                    )

        yield StreamEvent(
            agent=self.name,
            kind="graph_update",
            payload={
                "nodes": len(graph.nodes),
                "edges": len(graph.edges),
                "top_authors": [
                    {"id": aid, **author_meta.get(aid, {}), "score": score}
                    for aid, score in author_relevance.most_common(10)
                ],
            },
        )

        # Step 2: Tavily enrichment for cross-source agreement
        if task.depth >= 2 and self.tavily.enabled:
            yield StreamEvent(
                agent=self.name,
                kind="log",
                payload={"message": "Enriching with Tavily web search…"},
            )
            try:
                tav = await self.tavily.search(task.topic, max_results=8)
            except Exception as e:
                yield StreamEvent(
                    agent=self.name,
                    kind="error",
                    payload={"message": f"Tavily error: {e}"},
                )
                tav = {"results": [], "answer": None}
            yield StreamEvent(
                agent=self.name,
                kind="tavily",
                payload={
                    "answer": tav.get("answer"),
                    "results": [
                        {
                            "title": r.get("title"),
                            "url": r.get("url"),
                            "content": (r.get("content") or "")[:600],
                        }
                        for r in (tav.get("results") or [])[:8]
                    ],
                },
            )

        yield StreamEvent(
            agent=self.name,
            kind="done",
            payload={
                "graph": graph.model_dump(),
                "top_authors": [
                    {"id": aid, **author_meta.get(aid, {}), "score": score}
                    for aid, score in author_relevance.most_common(10)
                ],
            },
        )
