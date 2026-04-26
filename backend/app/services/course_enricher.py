"""
Course enrichment primitives.

LLM helpers (_call_llm, _call_llm_json), search backends (_search),
query generation, web search with gap analysis, and result evaluation.
Used by wiki_downloader, wiki_images, chat_actions, and test_pipeline.
"""

import asyncio
import json
import logging
import re
from pathlib import Path
from typing import AsyncGenerator
from urllib.parse import urlparse

import httpx

logger = logging.getLogger(__name__)

from ..config import get_settings


def _slugify_title(title: str) -> str:
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    return slug.strip("-")[:80]

# ---------------------------------------------------------------------------
# LLM + Search helpers
# ---------------------------------------------------------------------------

_http_client: httpx.AsyncClient | None = None
# Caps concurrent LLM API calls (used inside _call_llm).
# asyncio.gather in dedup/synthesis can schedule many tasks, but only this
# many will actually be in-flight at once — the rest queue behind the semaphore.
_llm_semaphore = asyncio.Semaphore(5)


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=300.0,
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5,
            ),
        )
    return _http_client


async def _call_llm(
    prompt: str,
    *,
    max_tokens: int = 4096,
    temperature: float = 0.2,
    timeout: float | None = None,
    system: str | None = None,
    model: str | None = None,
) -> str:
    settings = get_settings()
    chosen_model = model or settings.llm_model
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = {
        "model": chosen_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    import time
    async with _llm_semaphore:
        t0 = time.monotonic()
        client = _get_http_client()
        req_timeout = httpx.Timeout(timeout) if timeout else None
        resp = await client.post(
            f"{settings.llm_base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=req_timeout,
        )
        if resp.status_code != 200:
            body = resp.text[:500]
            logger.error(
                "LLM API returned %s: %s", resp.status_code, body,
            )
        resp.raise_for_status()
        elapsed = time.monotonic() - t0
    content = resp.json()["choices"][0]["message"]["content"].strip()
    logger.warning(
        "LLM call: %.1fs | prompt ~%d chars | response ~%d chars",
        elapsed, len(prompt), len(content),
    )
    return content


_JSON_SYSTEM = (
    "Respond with ONLY valid JSON. No markdown fences, no explanation, "
    "no text before or after the JSON object."
)


async def _call_llm_json(prompt: str, **kwargs) -> dict:
    kwargs.setdefault("system", _JSON_SYSTEM)
    raw = await _call_llm(prompt, **kwargs)
    text = raw.strip()
    # Fallback: strip code fences if the model still wraps
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
    # Strip control characters that LLMs sometimes embed in JSON strings
    import re as _re
    text = _re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        logger.error(
            "LLM returned invalid JSON (%d chars). Tail: ...%s",
            len(raw), raw[-200:] if raw else "(empty)",
        )
        raise


async def _search(query: str) -> dict:
    """Run a single search query via the configured search API.

    Supports two backends:
      1. NVIDIA Inference Hub (default) — uses LLM_API_KEY against
         /v1/search/perplexity-search
      2. Direct Perplexity API — when SEARCH_API_KEY is set, uses it
         against the configured search.base_url
    """
    settings = get_settings()

    has_dedicated_search_key = bool(
        settings.search_api_key
        and settings.search_base_url
        and settings.search_api_key != settings.llm_api_key
    )

    if has_dedicated_search_key:
        return await _search_perplexity(query, settings)
    elif settings.llm_api_key and settings.llm_base_url:
        return await _search_nvidia(query, settings)
    else:
        return {"query": query, "results": [], "error": "Search not configured"}


async def _search_nvidia(query: str, settings) -> dict:
    """Search via NVIDIA Inference Hub's Perplexity endpoint."""
    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "max_results": 5,
    }
    try:
        client = _get_http_client()
        resp = await client.post(
            f"{settings.llm_base_url}/v1/search/perplexity-search",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()

        # Extract content from NVIDIA search response
        results = data.get("results", [])
        content_parts = []
        citations = []
        for r in results:
            snippet = r.get("snippet", r.get("content", r.get("text", "")))
            if snippet:
                content_parts.append(snippet)
            url = r.get("url", r.get("link", ""))
            title = r.get("title", "")
            if url:
                citations.append({"title": title, "url": url})

        content = "\n\n".join(content_parts)
        return {
            "query": query,
            "content": content[:15000],
            "citations": citations,
            "content_length": len(content),
        }
    except Exception as e:
        return {"query": query, "results": [], "error": str(e)}


async def _search_perplexity(query: str, settings) -> dict:
    """Search via direct Perplexity Sonar API."""
    headers = {
        "Authorization": f"Bearer {settings.search_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar",
        "messages": [{"role": "user", "content": query}],
    }
    try:
        client = _get_http_client()
        resp = await client.post(
            f"{settings.search_base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        citations = data.get("citations", [])
        return {
            "query": query,
            "content": content[:15000],
            "citations": citations,
            "content_length": len(content),
        }
    except Exception as e:
        return {"query": query, "results": [], "error": str(e)}


# ---------------------------------------------------------------------------
# Query generation
# ---------------------------------------------------------------------------

QUERY_STRATEGIES = {
    "natural_question": {
        "label": "Natural Question",
        "instruction": """\
Generate 2-3 search queries written as NATURAL QUESTIONS a practitioner would \
ask to deeply understand this topic. Each question should target a different \
aspect of the lesson — do NOT ask the same question with different wording.

Good: "How does LangChain AgentExecutor decide when to stop iterating?"
Good: "What is the difference between zero-shot and conversational ReAct agents?"
Bad:  "LangChain AgentExecutor overview" (keyword soup, not a question)
Bad:  "How does AgentExecutor work?" then "How does AgentExecutor function?" (same question)
""",
    },
    "specific_lookup": {
        "label": "Doc/API Lookup",
        "instruction": """\
Generate 2-3 search queries designed to find SPECIFIC documentation pages, API \
references, configuration parameters, code examples, or technical specs. Use \
precise names — tool versions, function signatures, parameter names, CLI flags.

Good: "site:python.langchain.com AgentExecutor max_iterations parameter"
Good: "OpenAI function calling API JSON schema specification 2024"
Bad:  "LangChain documentation" (too broad)
Bad:  "agent configuration" (no specific tool or parameter)
""",
    },
    "comparative": {
        "label": "Comparative",
        "instruction": """\
Generate 2-3 search queries that COMPARE or CONTRAST the lesson's tools/concepts \
against alternatives. Each query must name at least two specific things being \
compared and target a concrete dimension (performance, API design, use case fit).

Good: "LangChain AgentExecutor vs CrewAI task delegation performance comparison"
Good: "ReAct prompting vs chain-of-thought for multi-step tool use accuracy"
Bad:  "best agent framework" (no specific comparison)
Bad:  "LangChain vs others" (no concrete dimension)
""",
    },
    "failure_edge_case": {
        "label": "Failure & Edge Cases",
        "instruction": """\
Generate 2-3 search queries targeting PROBLEMS, FAILURES, LIMITATIONS, and \
EDGE CASES. Reference specific error messages, failure modes, known issues, \
or scenarios where things break. These should help someone debug or avoid pitfalls.

Good: "LangChain AgentExecutor OutputParserException infinite retry loop fix"
Good: "ReAct agent hallucinated tool names wrong action format common causes"
Bad:  "agent problems" (too generic)
Bad:  "limitations of AI agents" (no specific tool or failure mode)
""",
    },
    "multimedia": {
        "label": "Multimedia & Video Tutorials",
        "instruction": """\
Generate 2-3 search queries to find the BEST tutorial videos and multimedia \
for this topic. Target:
- YouTube tutorials from recognized educators
- Official product walkthroughs and demos from vendors
- Conference talks, workshop recordings, or online course segments
- Interactive tutorials (deeplearning.ai, fast.ai, etc.)

Use 'site:youtube.com' or include 'tutorial video' in queries. Include \
recent years (2024-2026) for recency. If the lesson is about a specific \
product/tool, search for that product's official channel.

Good: "site:youtube.com Anthropic Claude Code getting started tutorial 2025"
Good: "deeplearning.ai agentic AI course Andrew Ng"
Bad:  "AI tutorial" (too generic)
Bad:  "video" (meaningless without specifics)
""",
    },
}

STRATEGY_PROMPT = """\
You are generating web search queries for a knowledge enrichment system.

{course_context}{course_profile}
LESSON TITLE: {title}
{lesson_context}
KEY CONCEPTS: {concepts}

YOUR TASK — {strategy_label} queries:
{strategy_instruction}

RULES:
- Use real tool names, API names, parameter names from the lesson — not \
  generic domain terms
- Write as a human would type into Google — natural phrasing
- Every query must target UNIQUE information — no overlapping results
- Generate the exact number of queries requested in the instructions above

Return a JSON object:
{{
  "queries": ["query1", "query2", ...]
}}

Return ONLY valid JSON.
"""

DYNAMIC_STRATEGY_PROMPT = """\
You are an expert at identifying UNIQUE, LESSON-SPECIFIC angles that generic \
search strategies would miss.

{course_context}{course_profile}
LESSON TITLE: {title}
{lesson_context}
KEY CONCEPTS: {concepts}

EXISTING SEARCH STRATEGIES already cover:
- Natural practitioner questions
- Specific doc/API lookups
- Comparative / contrastive queries
- Failure modes and edge cases

YOUR TASK: Identify 1-2 search angles that are SPECIFIC to this lesson's \
content and would NOT be covered by the generic strategies above. Then \
generate 2-3 search queries for each angle.

Examples of good custom angles:
- "security_implications" for a lesson on tool calling (sandboxing, injection)
- "scaling_patterns" for a lesson on memory management (token budgets, pruning)
- "real_world_deployments" for a lesson on agent architectures (case studies)
- "mathematical_foundations" for a lesson on reasoning patterns (formal proofs)

Return a JSON object:
{{
  "custom_strategies": [
    {{
      "id": "short_snake_case_id",
      "label": "Human-Readable Label",
      "queries": ["query1", "query2", "query3"]
    }}
  ]
}}

Return 1-2 strategies with 2-3 queries each. Return ONLY valid JSON.
"""


async def generate_queries(
    lessons: list,
    *,
    course_description: str = "",
    wiki_available: bool = False,
    concept_gaps: dict[str, list[str]] | None = None,
    course_profile: dict | None = None,
) -> AsyncGenerator[str, None]:
    """Generate search queries for each lesson using strategy-focused
    LLM calls per lesson (run concurrently). Yields SSE events.

    When ``concept_gaps`` is provided (``{lesson_slug: [research_topic, ...]``),
    uses those directly as search queries — no LLM query generation needed.
    These come from ``assess_wiki_coverage``'s concept-level gap analysis.

    When wiki_available=True, skips 'natural_question' and 'specific_lookup'
    strategies since the wiki already covers canonical resource discovery.
    Only 'comparative' and 'failure_edge_case' run, plus dynamic strategies.
    """

    total = len(lessons)
    all_queries = {}

    if wiki_available:
        strategies = [
            (k, v) for k, v in QUERY_STRATEGIES.items()
            if k in ("comparative", "failure_edge_case", "multimedia")
        ]
        logger.info("Wiki-aware enrichment: using %d strategies (incl. multimedia)", len(strategies))
    else:
        strategies = list(QUERY_STRATEGIES.items())

    course_context = ""
    if course_description:
        course_context = f"COURSE: {course_description}\n\n"

    from .course_generator import _format_course_profile
    profile_text = _format_course_profile(course_profile)
    if profile_text:
        profile_text += "\n\n"

    for i, lesson in enumerate(lessons):
        title = lesson.get("title", "Untitled")
        lesson_slug = lesson.get("slug") or _slugify_title(title) or f"lesson-{i}"

        # Fast path: one search per concept gap
        if concept_gaps and lesson_slug in concept_gaps:
            gap_descriptions = concept_gaps[lesson_slug]

            vendor = (course_profile or {}).get("vendor", "")
            tone = (course_profile or {}).get("tone", "")
            if tone == "practical-hands-on":
                gap_prefix = "best tutorial OR getting started guide"
            elif tone == "technical-precise":
                gap_prefix = "best technical reference OR original paper"
            else:
                gap_prefix = "best teaching resource OR original paper"
            if vendor:
                gap_prefix += f" {vendor}"

            enrichment_queries = [
                f"{gap_prefix}: {gap}"
                for gap in gap_descriptions
            ]

            multimedia_query = f"site:youtube.com {title} tutorial"
            if vendor:
                multimedia_query = f"site:youtube.com {vendor} {title} tutorial"
            categories = {
                "enrichment": enrichment_queries,
                "multimedia": [multimedia_query],
            }
            all_queries[lesson_slug] = categories
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i + 1,
                "total": total,
                "status": "done",
                "lesson_slug": lesson_slug,
                "queries": categories,
                "query_count": len(enrichment_queries),
            })
            continue

        content = lesson.get("content", "")
        summary = lesson.get("summary", "")
        if content:
            lesson_context = f"LESSON CONTENT (excerpt):\n{content[:4000]}"
        elif summary:
            lesson_context = f"LESSON SUMMARY:\n{summary}"
        else:
            lesson_context = ""
        concepts_str = ", ".join(lesson.get("concepts", []))

        yield _sse({
            "type": "progress",
            "lesson_title": title,
            "index": i + 1,
            "total": total,
            "status": "generating_queries",
        })

        async def _run_strategy(strategy_id: str, strategy: dict) -> tuple[str, list]:
            prompt = STRATEGY_PROMPT.format(
                title=title,
                lesson_context=lesson_context,
                concepts=concepts_str,
                course_context=course_context,
                course_profile=profile_text,
                strategy_label=strategy["label"],
                strategy_instruction=strategy["instruction"],
            )
            try:
                result = await _call_llm_json(prompt, max_tokens=2048)
                return strategy_id, result.get("queries", [])
            except Exception:
                return strategy_id, []

        async def _run_dynamic() -> list[tuple[str, list]]:
            prompt = DYNAMIC_STRATEGY_PROMPT.format(
                title=title,
                lesson_context=lesson_context,
                concepts=concepts_str,
                course_context=course_context,
                course_profile=profile_text,
            )
            try:
                result = await _call_llm_json(prompt, max_tokens=2048)
                custom = result.get("custom_strategies", [])
                return [
                    (s.get("id", f"custom_{j}"), s.get("queries", []))
                    for j, s in enumerate(custom)
                ]
            except Exception:
                return []

        try:
            fixed_tasks = [_run_strategy(sid, sdata) for sid, sdata in strategies]
            dynamic_task = _run_dynamic()
            fixed_results, dynamic_results = await asyncio.gather(
                asyncio.gather(*fixed_tasks),
                dynamic_task,
            )

            categories: dict[str, list[str]] = {}
            for strategy_id, queries in fixed_results:
                categories[strategy_id] = queries
            for strategy_id, queries in dynamic_results:
                categories[strategy_id] = queries

            all_queries[lesson_slug] = categories
            total_q = sum(len(qs) for qs in categories.values())
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i + 1,
                "total": total,
                "status": "done",
                "lesson_slug": lesson_slug,
                "queries": categories,
                "query_count": total_q,
            })
        except Exception as e:
            all_queries[lesson_slug] = {}
            yield _sse({
                "type": "progress",
                "lesson_title": title,
                "index": i + 1,
                "total": total,
                "status": "error",
                "error": str(e),
            })

    yield _sse({"type": "queries", "data": all_queries})
    yield _sse({"type": "done"})


# ---------------------------------------------------------------------------
# Web search + gap analysis
# ---------------------------------------------------------------------------

async def run_search(queries_by_lesson: dict) -> AsyncGenerator[str, None]:
    """Run approved search queries. Yields SSE events."""
    all_results = {}
    total_queries = sum(
        len(q)
        for cats in queries_by_lesson.values()
        for q in cats.values()
    )
    index = 0

    for lesson_slug, categories in queries_by_lesson.items():
        lesson_results = {}
        for category, queries in categories.items():
            cat_results = []
            for query in queries:
                index += 1
                yield _sse({
                    "type": "progress",
                    "query": query,
                    "category": category,
                    "lesson_slug": lesson_slug,
                    "index": index,
                    "total": total_queries,
                    "status": "searching",
                })

                result = await _search(query)
                cat_results.append(result)

                yield _sse({
                    "type": "progress",
                    "query": query,
                    "category": category,
                    "lesson_slug": lesson_slug,
                    "index": index,
                    "total": total_queries,
                    "status": "done",
                    "content_length": result.get("content_length", 0),
                })

            lesson_results[category] = cat_results
        all_results[lesson_slug] = lesson_results

        yield _sse({
            "type": "lesson_search_done",
            "lesson_slug": lesson_slug,
            "results": lesson_results,
            "query_count": sum(len(qs) for qs in lesson_results.values()),
        })

    gap_report = _analyze_gaps(all_results)

    yield _sse({"type": "search_results", "data": all_results, "gap_report": gap_report})
    yield _sse({"type": "done"})


def _analyze_gaps(results: dict) -> dict:
    """Analyze search results for coverage gaps."""
    report = {}
    for lesson_slug, categories in results.items():
        lesson_gaps = []
        for category, cat_results in categories.items():
            total_chars = sum(len(r.get("content", "")) for r in cat_results)
            zero_results = sum(1 for r in cat_results if r.get("error") or not r.get("content"))
            if total_chars < 5000:
                lesson_gaps.append({
                    "category": category,
                    "issue": "thin_content",
                    "total_chars": total_chars,
                })
            if zero_results > 0:
                lesson_gaps.append({
                    "category": category,
                    "issue": "zero_results",
                    "count": zero_results,
                })
        report[lesson_slug] = lesson_gaps
    return report


# ---------------------------------------------------------------------------
# Result evaluation (used by wiki_downloader for source curation)
# ---------------------------------------------------------------------------

_SOURCE_TYPE_MAP: dict[str, str] = {
    "arxiv.org": "paper", "ar5iv.labs.arxiv.org": "paper",
    "proceedings.neurips.cc": "paper", "proceedings.mlr.press": "paper",
    "aclanthology.org": "paper", "openreview.net": "paper",
    "semanticscholar.org": "paper", "par.nsf.gov": "paper",
    "github.com": "docs", "huggingface.co": "docs",
    "pytorch.org": "docs", "docs.nvidia.com": "docs",
    "openai.com": "docs", "paperswithcode.com": "docs",
}


def _classify_source_url(url: str) -> str:
    domain = urlparse(url).netloc.replace("www.", "")
    if domain in _SOURCE_TYPE_MAP:
        return _SOURCE_TYPE_MAP[domain]
    if domain.endswith(".edu") or domain.endswith(".gov"):
        return "paper"
    if any(k in domain for k in ("stackoverflow", "stackexchange", "reddit", "forum")):
        return "forum"
    return "blog"


# ── Evaluation prompts & functions ──

EVALUATE_PROMPT = """\
You are evaluating search results for relevance and quality to support a \
technical learning platform's knowledge base.

LESSON TITLE: {title}
LESSON KEY CONCEPTS: {concepts}

Below are {count} search results. For EACH result, evaluate:

1. **relevance** (1-5): How relevant is this content to the lesson topic?
   1=completely off-topic, 2=tangentially related, 3=somewhat relevant, \
4=directly relevant, 5=highly relevant core material

2. **quality_tier**: Classify the content quality:
   - "authoritative": Official documentation, peer-reviewed papers, specs
   - "educational": Well-written tutorials, reputable tech blogs, courses
   - "community": Forum answers, discussions, Stack Overflow
   - "low": Thin content, SEO spam, outdated, or inaccurate

3. **key_extracts**: Extract 3-5 of the most important SPECIFIC facts, \
claims, or technical details. Each extract must be a self-contained \
statement a tutor could cite. Include the source URL with each extract.

4. **topics_covered**: Which subtopics of the lesson does this result address?

5. **skip_reason**: If relevance < 3, explain briefly why (null otherwise)

SEARCH RESULTS:
{results_text}

Return a JSON object:
{{
  "evaluations": [
    {{
      "result_index": 0,
      "relevance": 4,
      "quality_tier": "authoritative",
      "key_extracts": [
        {{"fact": "Specific factual claim", "source_url": "https://...", "source_title": "Title"}}
      ],
      "topics_covered": ["subtopic1", "subtopic2"],
      "skip_reason": null
    }}
  ]
}}

CRITICAL RULES:
- Source URLs must be EXACTLY as provided — never fabricate URLs
- Extracts must be SPECIFIC facts (parameters, API details, numbers), \
not vague summaries like "discusses the topic"
- Be strict with quality_tier — most blog posts are "educational" at best
- Evaluate each result independently
- Return exactly {count} evaluations, one per result, in order

Return ONLY valid JSON.
"""


_EVAL_CONTENT_LIMIT = 2000
_EVAL_SUB_BATCH_SIZE = 4


def _build_result_text(results: list[dict], start_index: int) -> str:
    """Format search results for the evaluation prompt, capped per result."""
    parts: list[str] = []
    for j, r in enumerate(results):
        content = r.get("content", "")[:_EVAL_CONTENT_LIMIT]
        citations = r.get("citations", [])

        citation_info = []
        for c in (citations if isinstance(citations, list) else []):
            if isinstance(c, dict):
                url = c.get("url", "")
                title = c.get("title", "")
                source_type = _classify_source_url(url) if url else "unknown"
                citation_info.append(f"  [{source_type}] {title} — {url}")
            elif isinstance(c, str):
                source_type = _classify_source_url(c)
                citation_info.append(f"  [{source_type}] {c}")

        citations_block = "\n".join(citation_info) if citation_info else "  (none)"
        parts.append(
            f"\n--- RESULT {start_index + j} ---\n"
            f"Query: {r.get('query', 'N/A')}\n"
            f"Sources:\n{citations_block}\n"
            f"Content:\n{content}\n"
        )
    return "".join(parts)


async def _evaluate_sub_batch(
    lesson_title: str,
    concepts: list[str],
    results_batch: list[dict],
    batch_start_index: int,
) -> list[dict]:
    """Evaluate a small sub-batch of search results (max ~4)."""
    results_text = _build_result_text(results_batch, batch_start_index)

    prompt = EVALUATE_PROMPT.format(
        title=lesson_title,
        concepts=", ".join(concepts),
        count=len(results_batch),
        results_text=results_text,
    )

    try:
        data = await _call_llm_json(prompt, max_tokens=4096, temperature=0.1)
        evaluations = data.get("evaluations", [])
        for ev in evaluations:
            ri = ev.get("result_index", 0)
            local_idx = ri - batch_start_index
            if 0 <= local_idx < len(results_batch):
                orig = results_batch[local_idx]
                ev["original_query"] = orig.get("query", "")
                ev["original_citations"] = orig.get("citations", [])
                ev["content_length"] = orig.get("content_length", 0)
                ev["search_category"] = orig.get("_search_category", "general")
        return evaluations
    except Exception as e:
        logger.warning(
            "Evaluation sub-batch failed for '%s' (idx %d-%d): %s",
            lesson_title, batch_start_index,
            batch_start_index + len(results_batch) - 1, e,
        )
        return [
            {
                "result_index": batch_start_index + j,
                "relevance": 3,
                "quality_tier": "educational",
                "key_extracts": [],
                "topics_covered": [],
                "skip_reason": f"evaluation_error: {e}",
                "original_query": results_batch[j].get("query", ""),
                "original_citations": results_batch[j].get("citations", []),
                "content_length": results_batch[j].get("content_length", 0),
                "search_category": results_batch[j].get("_search_category", "general"),
            }
            for j in range(len(results_batch))
        ]


async def _evaluate_batch(
    lesson_title: str,
    concepts: list[str],
    results_batch: list[dict],
    batch_start_index: int,
) -> list[dict]:
    """Evaluate search results by splitting into small sub-batches.

    Splits results into groups of ``_EVAL_SUB_BATCH_SIZE`` and evaluates
    them concurrently. Each sub-batch gets ~2k chars of content per result
    to keep prompts under LLM context limits.
    """
    if not results_batch:
        return []

    sub_batches: list[tuple[list[dict], int]] = []
    for i in range(0, len(results_batch), _EVAL_SUB_BATCH_SIZE):
        chunk = results_batch[i : i + _EVAL_SUB_BATCH_SIZE]
        sub_batches.append((chunk, batch_start_index + i))

    tasks = [
        _evaluate_sub_batch(lesson_title, concepts, chunk, idx)
        for chunk, idx in sub_batches
    ]
    sub_results = await asyncio.gather(*tasks)

    evaluations: list[dict] = []
    for batch_evals in sub_results:
        evaluations.extend(batch_evals)
    return evaluations




def _sse(data: dict) -> str:
    return f"data: {json.dumps(data)}\n\n"


# ---------------------------------------------------------------------------
# Reference track — needs-driven search for precision sources
# ---------------------------------------------------------------------------

REFERENCE_NEEDS_PROMPT = """\
You are identifying what a Socratic tutor would need to consult for \
deep, grounded answers about this topic. The tutor already has \
pedagogical sources (explainers, tutorials, overviews). You are looking \
for **reference material** that deepens the tutor's understanding — \
both for precision (exact formulas, benchmark numbers, API defaults) \
and for comprehension (how methods actually work, why they were \
designed that way, step-by-step procedures the tutor can break down \
for students).

Think about what a student might ask:
- "What's the actual formula?" → needs a paper with the derivation
- "How does this actually work step by step?" → needs a process description
- "Why was it designed this way?" → needs design rationale from the authors
- "Show me the numbers" → needs benchmark results or ablation tables
- "How do I actually use this?" → needs API docs or working examples
- "Who uses this in production?" → needs deployment case studies

LESSON TITLE: {title}
KEY CONCEPTS: {concepts}
LESSON SUMMARY: {summary}

{course_profile}

EXISTING PEDAGOGY SOURCES (the tutor already has these):
{existing_sources}

YOUR TASK: Identify 3-5 specific **reference needs** — types of \
material that are missing from the pedagogy sources above. \
For each need, generate 1-2 targeted search queries to find it.

NEED TYPES (use exactly these labels):
- FORMULA_SOURCE — a paper or derivation containing the key equation, \
  algorithm, or mathematical formulation
- EMPIRICAL_DATA — benchmark results, ablation studies, performance \
  comparisons with specific numbers
- API_REFERENCE — official documentation, SDK reference, configuration \
  defaults, parameter specifications
- WORKING_EXAMPLE — complete working code, cookbook recipe, or \
  implementation guide from an authoritative source
- DEPLOYMENT_CASE — real-world production use case with concrete \
  metrics, architecture description, or lessons learned
- COMPARISON_DATA — structured comparison of alternatives with \
  specific criteria (not just opinion)
- CONCEPT_EXPLAINER — an authoritative source that describes a key \
  process, architecture, or design rationale in depth (e.g., a \
  seminal paper's training pipeline, the design decisions behind \
  a method, a detailed walkthrough of how a system works)

RULES:
- Only identify needs that the existing pedagogy sources do NOT cover
- Each need must describe something SPECIFIC — not "general info about X"
- Search queries should use precise terms: author names, paper titles, \
  site: operators for official docs, metric names for benchmarks
- Not every topic needs all types — skip types that don't apply
- Aim for diversity: a good set of needs covers both precision \
  (formulas, numbers) and understanding (processes, rationale)
- Limit to 3-5 needs total, 1-2 queries per need

Return JSON:
{{
  "needs": [
    {{
      "need_type": "FORMULA_SOURCE|EMPIRICAL_DATA|API_REFERENCE|WORKING_EXAMPLE|DEPLOYMENT_CASE|COMPARISON_DATA|CONCEPT_EXPLAINER",
      "description": "What specifically is needed — name the formula, \
the benchmark, the API, the process, or the use case",
      "search_queries": ["query1", "query2"]
    }}
  ],
  "reasoning": "1-2 sentences: what gaps exist in the pedagogy sources \
for both precision and understanding"
}}

Return ONLY valid JSON.
"""


async def assess_reference_needs(
    topic_slug: str,
    lesson_title: str,
    concepts: list[str],
    *,
    lesson_summary: str = "",
    existing_source_summaries: list[str] | None = None,
    course_profile: dict | None = None,
) -> dict:
    """Analyze a topic and identify typed precision needs for the reference track.

    Examines the existing pedagogy sources and determines what types of
    precision material (formulas, benchmarks, API docs, case studies)
    are missing.

    Returns::

        {
            "needs": [
                {
                    "need_type": "FORMULA_SOURCE|EMPIRICAL_DATA|...",
                    "description": "what specifically is needed",
                    "search_queries": ["query1", "query2"],
                }
            ],
            "reasoning": str,
            "all_queries": ["query1", "query2", ...],
        }
    """
    if existing_source_summaries:
        existing_text = "\n".join(
            f"- {s}" for s in existing_source_summaries
        )
    else:
        # Load pedagogy source names from wiki
        from .course_generator import load_wiki_context
        wiki_ctx = load_wiki_context(concepts, topic_slugs={topic_slug})
        source_names = []
        for slug_sources in wiki_ctx.get("source_content", {}).values():
            for src in slug_sources:
                content = src["content"]
                first_lines = content.split("\n", 5)
                source_line = next(
                    (l for l in first_lines if l.startswith("# Source:")),
                    src["file"],
                )
                source_names.append(source_line.replace("# Source: ", ""))
        existing_text = "\n".join(f"- {s}" for s in source_names) or "(none)"

    from .course_generator import _format_course_profile
    prompt = REFERENCE_NEEDS_PROMPT.format(
        title=lesson_title,
        concepts=", ".join(concepts),
        summary=lesson_summary,
        existing_sources=existing_text,
        course_profile=_format_course_profile(course_profile),
    )

    try:
        result = await _call_llm_json(prompt, max_tokens=2048, temperature=0.2)
    except Exception as e:
        logger.warning("Reference needs analysis failed for %r: %s", lesson_title, e)
        return {"needs": [], "reasoning": f"LLM error: {e}", "all_queries": []}

    needs = result.get("needs", [])
    reasoning = result.get("reasoning", "")

    # Flatten all queries for convenient consumption
    all_queries: list[str] = []
    for need in needs:
        for q in need.get("search_queries", []):
            if q and q not in all_queries:
                all_queries.append(q)

    logger.info(
        "Reference needs for %r: %d needs, %d queries — %s",
        lesson_title, len(needs), len(all_queries), reasoning,
    )

    return {
        "needs": needs,
        "reasoning": reasoning,
        "all_queries": all_queries,
    }


async def enrich_reference_track(
    lesson_title: str,
    topic_slug: str,
    concepts: list[str],
    *,
    lesson_summary: str = "",
    course_profile: dict | None = None,
) -> dict:
    """Run the full reference track pipeline for a single lesson/topic.

    1. Assess reference needs (LLM-driven, topic-adaptive)
    2. Run targeted searches for each need
    3. Filter + curate + audit candidates
    4. Download picks to ``reference/`` subdirectory
    5. Save proposals + curation report + ramps

    Returns summary dict with counts and unfilled needs (ramps).
    """
    from .wiki_downloader import (
        curate_reference_sources,
        audit_reference_curation,
        _get_existing_source_details,
        get_existing_source_urls,
        enrich_wiki_topic,
        save_proposals,
        save_curation_report,
    )

    # Step 1: Assess reference needs
    needs_result = await assess_reference_needs(
        topic_slug, lesson_title, concepts,
        lesson_summary=lesson_summary,
        course_profile=course_profile,
    )
    typed_needs = needs_result["needs"]
    all_queries = needs_result["all_queries"]

    if not typed_needs:
        logger.info("No reference needs identified for %r", lesson_title)
        return {
            "needs": 0, "queries": 0, "searches": 0,
            "picks": 0, "promotions": 0, "downloads": 0,
            "unfilled_needs": [],
        }

    # Step 2: Run searches, grouped by need_type
    search_results_by_need: dict[str, list[dict]] = {}
    total_searches = 0
    for need in typed_needs:
        need_type = need["need_type"]
        need_results: list[dict] = []
        for query in need.get("search_queries", []):
            result = await _search(query)
            need_results.append(result)
            total_searches += 1
        search_results_by_need[need_type] = need_results

    # Step 3: Get existing reference sources
    existing_urls = get_existing_source_urls(topic_slug)

    # Step 4: Curate
    curation = await curate_reference_sources(
        lesson_title, typed_needs, search_results_by_need,
        existing_urls, topic_slug=topic_slug,
    )

    picks = curation["picks"]
    all_candidates = curation["all_candidates"]

    # Step 5: Audit
    existing_details = _get_existing_source_details(topic_slug)

    # Build candidates_by_url for the auditor
    candidates_by_url: dict[str, dict] = {}
    for need_type, results in search_results_by_need.items():
        for r in results:
            snippet = r.get("content", "")[:1200]
            for c in r.get("citations", []):
                url = c.get("url", "") if isinstance(c, dict) else str(c)
                t = c.get("title", "") if isinstance(c, dict) else ""
                if url and url not in existing_urls and url not in candidates_by_url:
                    candidates_by_url[url] = {
                        "url": url, "title": t,
                        "snippet": snippet, "needs": [need_type],
                    }
                elif url in candidates_by_url:
                    if need_type not in candidates_by_url[url].get("needs", []):
                        candidates_by_url[url]["needs"].append(need_type)

    audit = await audit_reference_curation(
        lesson_title, curation, candidates_by_url, existing_details,
    )

    promotions = audit.get("promotions", [])
    if promotions:
        picks.extend(promotions)

    # Step 6: Download picks to reference/ subdirectory
    dl_result = None
    downloads = 0
    if picks:
        sources = [{"url": p["url"], "title": p.get("title", "")} for p in picks]
        dl_result = await enrich_wiki_topic(
            topic_slug, sources, extract_images=False, track="reference",
        )
        downloads = dl_result.get("saved", 0)

    # Step 7: Save audit trail
    unfilled_needs = curation.get("unfilled_needs", [])

    if all_candidates:
        save_proposals(
            topic_slug,
            [{"url": c.get("url", ""), "title": c.get("title", ""),
              "need_type": c.get("need_type", "")} for c in all_candidates],
            run_label=f"reference-track:{lesson_title}",
            track="reference",
        )

    save_curation_report(
        topic_slug, lesson_title,
        curation=curation, audit=audit,
        existing_details=existing_details,
        download_result=dl_result,
        track="reference",
    )

    # Step 8: Save ramps (unfilled needs) for KB prompt injection
    if unfilled_needs:
        import json as _json
        from ..config import WIKI_DIR as _wiki
        ramps_dir = _wiki / "resources" / "by-topic" / topic_slug / "reference"
        ramps_dir.mkdir(parents=True, exist_ok=True)
        ramps_path = ramps_dir / "ramps.json"
        _json.dumps(unfilled_needs)  # validate serializable
        ramps_path.write_text(_json.dumps(unfilled_needs, indent=2))
        logger.info("Saved %d ramps to %s", len(unfilled_needs), ramps_path)

    # Step 9: Extract reference cards from downloaded sources
    cards_result = {"extracted": 0, "skipped": 0, "failed": 0}
    if downloads > 0:
        from .wiki_downloader import extract_cards_for_sources
        cards_result = await extract_cards_for_sources(
            topic_slug, picks,
            lesson_title=lesson_title,
            concepts=concepts,
        )
        logger.info(
            "Reference cards for %r: %d extracted, %d skipped, %d failed",
            lesson_title, cards_result["extracted"],
            cards_result["skipped"], cards_result["failed"],
        )

    return {
        "needs": len(typed_needs),
        "queries": len(all_queries),
        "searches": total_searches,
        "picks": len(curation["picks"]),
        "promotions": len(promotions),
        "downloads": downloads,
        "cards_extracted": cards_result.get("extracted", 0),
        "unfilled_needs": unfilled_needs,
        "reasoning": needs_result.get("reasoning", ""),
    }
