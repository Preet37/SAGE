"""
Deep Research router — Tavily-powered web search for lesson enrichment,
topic deep-dives, and background research.
"""
import logging
import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import httpx

from ..deps import get_current_user
from ..models.user import User

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/research", tags=["research"])

TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
TAVILY_URL = "https://api.tavily.com/search"


class ResearchRequest(BaseModel):
    query: str
    topic_context: Optional[str] = None
    max_results: int = 8
    search_depth: str = "advanced"  # "basic" | "advanced"
    include_domains: Optional[list[str]] = None
    exclude_domains: Optional[list[str]] = None


class ResearchResult(BaseModel):
    title: str
    url: str
    content: str
    score: float
    published_date: Optional[str] = None


class ResearchResponse(BaseModel):
    query: str
    answer: Optional[str] = None
    results: list[ResearchResult]
    total: int


@router.post("/search", response_model=ResearchResponse)
async def deep_research(
    req: ResearchRequest,
    user: User = Depends(get_current_user),
):
    """Tavily deep web search for lesson/concept enrichment."""
    if not TAVILY_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="Research API not configured. Set TAVILY_API_KEY in backend/.env",
        )

    query = req.query.strip()
    if req.topic_context:
        query = f"{req.topic_context}: {query}"

    payload: dict = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": min(req.max_results, 15),
        "search_depth": req.search_depth,
        "include_answer": True,
        "include_raw_content": False,
    }
    if req.include_domains:
        payload["include_domains"] = req.include_domains
    if req.exclude_domains:
        payload["exclude_domains"] = req.exclude_domains

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            resp = await client.post(TAVILY_URL, json=payload)
            resp.raise_for_status()
            data = resp.json()
    except httpx.HTTPStatusError as e:
        logger.error("Tavily API error %s: %s", e.response.status_code, e.response.text[:300])
        raise HTTPException(status_code=502, detail="Research search failed. Please try again.")
    except Exception as e:
        logger.error("Tavily request failed: %s", e)
        raise HTTPException(status_code=502, detail="Research search unavailable.")

    results = [
        ResearchResult(
            title=r.get("title", ""),
            url=r.get("url", ""),
            content=r.get("content", "")[:500],
            score=r.get("score", 0.0),
            published_date=r.get("published_date"),
        )
        for r in data.get("results", [])
    ]

    return ResearchResponse(
        query=req.query,
        answer=data.get("answer"),
        results=results,
        total=len(results),
    )


@router.get("/lesson/{lesson_id}")
async def research_lesson_topic(
    lesson_id: str,
    user: User = Depends(get_current_user),
):
    """Auto-research a lesson's topics using Tavily."""
    from sqlmodel import Session
    from ..db import engine
    from ..models.learning import Lesson
    import json

    with Session(engine) as session:
        lesson = session.get(Lesson, lesson_id)
        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        try:
            concepts = json.loads(lesson.concepts or "[]")
        except Exception:
            concepts = []

        query = lesson.title
        if concepts:
            query += f" {' '.join(concepts[:3])}"

    return await deep_research(
        ResearchRequest(query=query, topic_context=None, max_results=6, search_depth="advanced"),
        user=user,
    )
