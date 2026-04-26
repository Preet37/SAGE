"""Concierge Agent — expert ranking, contact discovery, and email outreach."""
from __future__ import annotations

import re
from typing import AsyncIterator
from urllib.parse import urlparse

from ..clients.apollo import ApolloClient
from ..clients.hunter import HunterClient
from ..clients.openalex import OpenAlexClient
from ..clients.sendgrid import SendGridClient
from ..protocol import ExpertProfile, OutreachRequest, StreamEvent


def _domain_from_institution(name: str | None) -> str | None:
    """Best-effort domain guess from institution name (e.g. 'University of Toronto' → 'utoronto.ca').

    For real production use this would lookup ROR/Wikidata. We use a small map
    plus a simple heuristic.
    """
    if not name:
        return None
    n = name.lower()
    known = {
        "stanford university": "stanford.edu",
        "mit": "mit.edu",
        "massachusetts institute of technology": "mit.edu",
        "harvard university": "harvard.edu",
        "university of toronto": "utoronto.ca",
        "university of california, berkeley": "berkeley.edu",
        "carnegie mellon university": "cmu.edu",
        "university of waterloo": "uwaterloo.ca",
        "university of cambridge": "cam.ac.uk",
        "university of oxford": "ox.ac.uk",
        "google deepmind": "deepmind.com",
        "openai": "openai.com",
        "google research": "google.com",
        "microsoft research": "microsoft.com",
        "meta ai": "meta.com",
    }
    return known.get(n)


class ConciergeAgent:
    name = "concierge"

    def __init__(
        self,
        openalex: OpenAlexClient,
        hunter: HunterClient,
        apollo: ApolloClient,
        sendgrid: SendGridClient,
    ) -> None:
        self.openalex = openalex
        self.hunter = hunter
        self.apollo = apollo
        self.sendgrid = sendgrid

    async def discover_experts(
        self, top_authors: list[dict]
    ) -> AsyncIterator[StreamEvent]:
        """Enrich + rank a list of {id, name, institution, score} authors."""

        yield StreamEvent(
            agent=self.name,
            kind="log",
            payload={
                "message": f"Discovering contact info for top {len(top_authors)} authors…",
                "hunter_enabled": self.hunter.enabled,
                "apollo_enabled": self.apollo.enabled,
            },
        )

        profiles: list[ExpertProfile] = []

        for a in top_authors:
            author_id = a.get("id") or ""
            name = a.get("name") or "(unknown)"
            institution = a.get("institution")
            score = float(a.get("score") or 0)

            # OpenAlex author detail for h-index / works count
            h_index = None
            works_count = None
            cited_by_count = None
            try:
                author = await self.openalex.get_author(author_id)
                summary = (author or {}).get("summary_stats") or {}
                h_index = summary.get("h_index")
                works_count = author.get("works_count")
                cited_by_count = author.get("cited_by_count")
                if not institution:
                    last_inst = author.get("last_known_institution") or {}
                    institution = last_inst.get("display_name")
            except Exception:
                pass

            profile = ExpertProfile(
                id=author_id,
                name=name,
                role=None,
                organization=institution,
                h_index=h_index,
                works_count=works_count,
                cited_by_count=cited_by_count,
                relevance=score,
            )

            # Apollo enrichment (optional)
            if self.apollo.enabled:
                try:
                    people = await self.apollo.search_people(
                        name=name, organization_name=institution
                    )
                    if people:
                        p0 = people[0]
                        profile.role = p0.get("title")
                        profile.email = profile.email or p0.get("email")
                        profile.apollo_data = {
                            "linkedin_url": p0.get("linkedin_url"),
                            "city": p0.get("city"),
                            "country": p0.get("country"),
                        }
                except Exception:
                    pass

            # Hunter email lookup (optional, only if Apollo didn't provide one).
            # Prefer the hardcoded institution → domain map for accuracy, but
            # fall back to passing the institution name as `company` — Hunter
            # resolves the domain itself, which works for arbitrary universities.
            if not profile.email and self.hunter.enabled and institution:
                domain = _domain_from_institution(institution)
                try:
                    if domain:
                        h = await self.hunter.find_email(
                            full_name=name, domain=domain
                        )
                    else:
                        h = await self.hunter.find_email(
                            full_name=name, company=institution
                        )
                    if h.get("email"):
                        profile.email = h["email"]
                        profile.email_confidence = (
                            float(h.get("score", 0) or 0) / 100.0
                        )
                except Exception:
                    pass

            profiles.append(profile)
            yield StreamEvent(
                agent=self.name,
                kind="expert",
                payload=profile.model_dump(),
            )

        yield StreamEvent(
            agent=self.name,
            kind="done",
            payload={"experts": [p.model_dump() for p in profiles]},
        )

    async def send_outreach(
        self, expert: ExpertProfile, request: OutreachRequest
    ) -> dict:
        """Send a single outreach email via SendGrid. Returns send result."""
        if not expert.email:
            return {"sent": False, "reason": "no email on record"}
        return await self.sendgrid.send_email(
            to_email=expert.email,
            to_name=expert.name,
            subject=request.subject,
            body=request.body,
        )
