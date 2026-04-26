"""Validator Agent — scores hypothesis credibility from the knowledge graph."""
from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import AsyncIterator

from ..protocol import KnowledgeGraph, StreamEvent, ValidationReport


class ValidatorAgent:
    name = "validator"

    async def run(
        self,
        topic: str,
        graph: KnowledgeGraph,
        tavily_answer: str | None = None,
    ) -> AsyncIterator[StreamEvent]:
        yield StreamEvent(
            agent=self.name,
            kind="log",
            payload={"message": "Scoring credibility across citation density, recency, and source agreement…"},
        )

        papers = [n for n in graph.nodes if n.type == "paper"]
        authors = [n for n in graph.nodes if n.type == "author"]

        # Citation density: average citations per paper, normalised
        cite_counts = [
            int(p.metadata.get("cited_by_count") or 0) for p in papers
        ]
        avg_citations = mean(cite_counts) if cite_counts else 0.0
        citation_density = min(1.0, avg_citations / 100.0)

        # Recency: average year normalized to 0–1 (papers from last 5 yrs → 1.0)
        now_year = datetime.utcnow().year
        years = [
            int(p.metadata.get("year") or 0)
            for p in papers
            if p.metadata.get("year")
        ]
        if years:
            recency_score = max(
                0.0,
                min(1.0, 1 - (now_year - mean(years)) / 20),
            )
        else:
            recency_score = 0.0

        # Author credibility: how many authors have multiple papers in this set
        author_paper_count: dict[str, int] = {}
        for e in graph.edges:
            if e.type == "authored":
                author_paper_count[e.source] = author_paper_count.get(e.source, 0) + 1
        repeat_authors = sum(1 for c in author_paper_count.values() if c >= 2)
        author_credibility = (
            min(1.0, repeat_authors / max(1, len(authors) // 4))
            if authors
            else 0.0
        )

        # Cross-source agreement: do we have a Tavily answer that mentions
        # at least one concept seen in our paper set?
        cross_source_agreement = 0.0
        concepts: set[str] = set()
        for p in papers:
            for c in p.metadata.get("concepts", []) or []:
                if c:
                    concepts.add(c.lower())
        if tavily_answer and concepts:
            haystack = tavily_answer.lower()
            hits = sum(1 for c in concepts if c in haystack)
            cross_source_agreement = min(1.0, hits / 5.0)

        confidence = round(
            0.30 * citation_density
            + 0.25 * recency_score
            + 0.25 * author_credibility
            + 0.20 * cross_source_agreement,
            3,
        )

        # Detect conflicting evidence: papers with very low citations on a
        # well-cited topic, or wildly different concept clusters
        conflicting: list[str] = []
        if avg_citations > 50 and any(c < 5 for c in cite_counts):
            conflicting.append(
                "Some papers have <5 citations in a topic with 50+ avg — outliers may contradict consensus."
            )
        if not tavily_answer:
            conflicting.append("No web evidence retrieved; consensus check is partial.")

        next_queries = []
        if recency_score < 0.5:
            next_queries.append(f"{topic} 2024 OR 2025")
        if author_credibility < 0.4:
            next_queries.append(f"{topic} systematic review")
        if cross_source_agreement < 0.4:
            next_queries.append(f"{topic} criticism OR counter-evidence")

        report = ValidationReport(
            confidence_score=confidence,
            citation_density=round(citation_density, 3),
            cross_source_agreement=round(cross_source_agreement, 3),
            recency_score=round(recency_score, 3),
            author_credibility=round(author_credibility, 3),
            conflicting_evidence=conflicting,
            recommended_next_queries=next_queries,
            summary=(
                f"Reviewed {len(papers)} papers with {len(authors)} unique authors. "
                f"Average citations: {avg_citations:.1f}. "
                f"Confidence: {confidence:.2f}/1.00."
            ),
        )

        yield StreamEvent(
            agent=self.name,
            kind="validation",
            payload=report.model_dump(),
        )
        yield StreamEvent(agent=self.name, kind="done", payload=report.model_dump())
