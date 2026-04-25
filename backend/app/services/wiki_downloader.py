"""
Wiki content downloader — reusable download and enrichment functions.

Provides high-level operations for the course creation pipeline:
- ``download_url``: fetch content from a URL with cascading fallbacks
- ``download_source``: fetch + save to a wiki topic directory
- ``enrich_wiki_topic``: download multiple sources into a topic directory
- ``bootstrap_new_wiki_topic``: create a new topic page + concept-map entry
"""

import asyncio
import json
import logging
import re
import time
from pathlib import Path
from urllib.parse import urlparse

import httpx

from ..config import get_settings

logger = logging.getLogger(__name__)

from ..config import WIKI_DIR as _WIKI_DIR  # noqa: E402 — must follow logger
_CONCEPT_MAP_PATH = _WIKI_DIR / "concept-map.md"
_PENDING_DIR = _WIKI_DIR / ".pending"

_MIN_DOWNLOAD_WORDS = 80
_JUNK_PHRASES = [
    "redirecting...", "sign in", "we read every piece of feedback",
    "enable javascript", "please enable cookies", "just a moment",
    "access denied", "403 forbidden",
]

_http_client: httpx.AsyncClient | None = None


def _get_http_client() -> httpx.AsyncClient:
    global _http_client
    if _http_client is None or _http_client.is_closed:
        _http_client = httpx.AsyncClient(
            timeout=120.0,
            limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
        )
    return _http_client


_BOILERPLATE_LINES = frozenset({
    "{{ message }}", "Skip to content", "Navigation Menu",
    "References & Citations", "export BibTeX citation", "Loading...",
    "Bibliographic and Citation Tools", "Recommenders and Search Tools",
    "Code, Data and Media Associated with this Article", "Demos",
    "GO", "Search", "Bookmark", "BibTeX formatted citation",
    "Bibliographic Tools", "Code, Data, Media", "Related Papers",
    "quick links",
})

_BOILERPLATE_PREFIXES = (
    "Bibliographic Explorer",
    "Connected Papers",
    "Litmaps",
    "scite Smart Citations",
    "alphaXiv",
    "CatalyzeX",
    "DagsHub",
    "Gotit.pub",
    "GotitPub",
    "Hugging Face",
    "Huggingface",
    "Papers with Code",
    "ScienceCast",
    "Influence Flower",
    "CORE Recommender",
    "arXivLabs",
    "[What is ",
    "| Name | Name |",
    "[Skip to ",
    "We gratefully acknowledge",
    "Have an idea for a project",
    "Both individuals and organizations that work with arXivLabs",
    "Which authors of this paper",
    "About arXivLabs",
    "Replicate _(",
    "TXYZ.AI _(",
    "Data provided by:",
    "Current browse context",
    "Change to browse by",
    "Focus to learn",
    "arXiv-issued DOI",
    "Submission history",
    "Authors:",
    "View a PDF of the paper titled",
    "Subjects:",
    "Cite as:",
    "Full-text links:",
    "Access Paper",
    "Markdown Content:",
    "URL Source:",
    "Published Time:",
    "[Learn about arXiv",
    "[View PDF]",
)

_BOILERPLATE_RE = re.compile(
    r"^("
    r"\[?(cs|stat|math|eess|q-bio|q-fin)\]?"         # arxiv category nav
    r"|[-*]\s*\[x\]\s"                                 # toggle checkboxes
    r"|!\[Image\s*\d*:"                                 # nav images
    r"|\[!\[Image\s*\d*:"                               # linked nav images
    r"|\*\s*\[.*?\]\(https://arxiv\.org/"               # arxiv nav bullet links
    r"|\*\s*\[.*?\]\(https://info\.arxiv\.org/"         # arxiv info links
    r"|\[<prev\]|\[next>\]"                             # prev/next nav
    r"|\[new\]\(|\[recent\]\("                          # new/recent links
    r"|\*\s*\[About\]|\*\s*\[Help\]"                    # footer links
    r"|\*\s*\[Contact\]|\*\s*\[Subscribe\]"
    r"|\*\s*\[Copyright\]|\*\s*\[Privacy"
    r"|\*\s*\[Web Accessibility"
    r"|\*\s*\[arXiv Operational"
    r"|\*\s*\[Login\]|\*\s*\[Help Pages\]"
    r"|\*\s*\[Author\]|\*\s*\[Venue\]"
    r"|\*\s*\[Institution\]|\*\s*\[Topic\]"
    r"|×$"                                              # close button
    r")"
)


def _clean_extracted_text(text: str) -> str:
    lines = text.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            cleaned.append(line)
            continue
        # Strip markdown heading markers for comparison
        bare = stripped.lstrip("#").strip()
        if stripped in _BOILERPLATE_LINES or bare in _BOILERPLATE_LINES:
            continue
        if any(stripped.startswith(p) or bare.startswith(p)
               for p in _BOILERPLATE_PREFIXES):
            continue
        if stripped == "|---|---|---|---|---|":
            continue
        if _BOILERPLATE_RE.match(stripped):
            continue
        cleaned.append(line)
    return "\n".join(cleaned).strip()


def _is_junk_content(text: str) -> bool:
    lower = text.lower().strip()
    for phrase in _JUNK_PHRASES:
        if lower.startswith(phrase) or lower == phrase:
            return True
    return len(text.split()) < _MIN_DOWNLOAD_WORDS


def _source_slug(url: str) -> str:
    parsed = urlparse(url)
    path = parsed.path.strip("/").replace("/", "-")
    host = parsed.hostname or ""
    host = host.replace("www.", "").replace(".com", "").replace(".io", "")
    host = host.replace(".github", "").replace(".org", "")
    slug = f"{host}-{path}" if path else host
    slug = re.sub(r'[^a-zA-Z0-9_-]', '-', slug)
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug[:80]


# ---------------------------------------------------------------------------
# URL normalization helpers
# ---------------------------------------------------------------------------

_ARXIV_PDF_RE = re.compile(r'arxiv\.org/pdf/(\d{4}\.\d{4,5})(v\d+)?(\.pdf)?$')
_ARXIV_ABS_RE = re.compile(r'arxiv\.org/abs/(\d{4}\.\d{4,5})(v\d+)?$')


def _normalize_arxiv_urls(url: str) -> list[str]:
    """Return a list of arxiv URL variants to try, best first.

    For an arxiv PDF or abstract URL, returns [html, abs, original].
    Not all papers have HTML versions, so we try multiple.
    """
    for pat in (_ARXIV_PDF_RE, _ARXIV_ABS_RE):
        m = pat.search(url)
        if m:
            paper_id = m.group(1)
            version = m.group(2) or ""
            candidates = [
                f"https://arxiv.org/html/{paper_id}{version}",
                f"https://arxiv.org/abs/{paper_id}{version}",
            ]
            return [c for c in candidates if c != url] + [url]
    return [url]


def _normalize_url(url: str) -> tuple[str, str | None]:
    """Normalize a URL for better downloadability.

    Returns (normalized_url, original_url_or_None).  If the URL was
    rewritten the second element is the original; otherwise ``None``.
    """
    variants = _normalize_arxiv_urls(url)
    if len(variants) > 1:
        return variants[0], url
    return url, None


def _is_pdf_url(url: str) -> bool:
    """Heuristic: does this URL point to a PDF?"""
    path = urlparse(url).path.lower()
    return path.endswith(".pdf") or "/pdf/" in path


_THIN_CONTENT_WORDS = 500


def _is_thin(result: dict) -> bool:
    """Content exists but is probably not the full page/paper."""
    if not result.get("content"):
        return True
    return result.get("word_count", 0) < _THIN_CONTENT_WORDS


# ---------------------------------------------------------------------------
# Fetch functions (cascading: trafilatura -> jina -> browser -> search)
# ---------------------------------------------------------------------------

async def _fetch_with_trafilatura(url: str) -> dict:
    try:
        import trafilatura
        downloaded = await asyncio.to_thread(trafilatura.fetch_url, url)
        if not downloaded:
            return {"url": url, "content": "", "error": "fetch_url returned None"}
        text = await asyncio.to_thread(
            trafilatura.extract, downloaded,
            include_links=True, include_tables=True,
            favor_recall=True, output_format="txt",
        )
        if not text:
            return {"url": url, "content": "", "error": "extract returned None"}
        text = _clean_extracted_text(text)
        if _is_junk_content(text):
            return {"url": url, "content": "", "error": "junk content"}
        return {"url": url, "content": text, "word_count": len(text.split()),
                "_raw_html": downloaded}
    except Exception as e:
        return {"url": url, "content": "", "error": str(e)}


async def _fetch_with_browser(url: str) -> dict:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return {"url": url, "content": "", "error": "playwright not installed"}
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0.0.0 Safari/537.36"
                )
            )
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(2000)

            # Capture raw HTML and rendered image dimensions before cleanup
            raw_html = await page.content()
            js_image_data = await page.evaluate("""() => {
                const data = {};
                for (const img of document.querySelectorAll('img')) {
                    if (img.src && img.naturalWidth > 0) {
                        data[img.src] = [img.naturalWidth, img.naturalHeight];
                    }
                }
                return data;
            }""")

            text = await page.evaluate("""() => {
                for (const sel of ['nav', 'footer', 'header', '.sidebar',
                    '[role="navigation"]', '.cookie-banner', '#cookie-consent']) {
                    for (const el of document.querySelectorAll(sel)) el.remove();
                }
                const main = document.querySelector(
                    'main, article, .content, .post-content, #content'
                );
                return (main || document.body).innerText;
            }""")
            await browser.close()
        if not text or not text.strip():
            return {"url": url, "content": "", "error": "empty page"}
        text = _clean_extracted_text(text)
        if len(text.split()) < _MIN_DOWNLOAD_WORDS:
            return {"url": url, "content": "", "error": f"only {len(text.split())} words"}
        return {"url": url, "content": text, "word_count": len(text.split()),
                "via": "browser", "_raw_html": raw_html,
                "_js_image_data": js_image_data}
    except Exception as e:
        return {"url": url, "content": "", "error": f"browser: {str(e)[:120]}"}


async def _fetch_with_jina(url: str) -> dict:
    """Fetch clean markdown via Jina Reader API.

    Jina handles JS-rendered pages, complex layouts, and some PDFs.
    Free tier, no API key required for basic use.
    """
    jina_url = f"https://r.jina.ai/{url}"
    try:
        client = _get_http_client()
        resp = await client.get(
            jina_url,
            headers={"Accept": "text/markdown"},
            timeout=30.0,
        )
        resp.raise_for_status()
        text = resp.text.strip()
        if not text:
            return {"url": url, "content": "", "error": "jina returned empty"}
        text = _clean_extracted_text(text)
        if _is_junk_content(text):
            return {"url": url, "content": "", "error": "jina: junk content"}
        return {"url": url, "content": text, "word_count": len(text.split()), "via": "jina"}
    except Exception as e:
        return {"url": url, "content": "", "error": f"jina: {str(e)[:120]}"}


async def _fetch_via_search(url: str, *, title: str = "") -> dict:
    """Ask a search-augmented LLM to summarize the content at *url*.

    For papers/PDFs, uses a more targeted prompt that requests equations,
    results tables, and methodology details — the kind of precision
    anchors the reference KB needs.

    Supports two backends (same as ``course_enricher._search``):

    1. NVIDIA Inference Hub — ``LLM_API_KEY`` against
       ``{llm_base_url}/v1/search/perplexity-search``
    2. Direct Perplexity Sonar — ``SEARCH_API_KEY`` against
       ``{search_base_url}/chat/completions``
    """
    settings = get_settings()

    if _is_pdf_url(url) or "arxiv.org" in url:
        query = (
            f"Provide a detailed technical summary of this paper: {url}\n"
            f"{f'Title: {title}' if title else ''}\n"
            f"Include: (1) the exact problem formulation and key equations/loss functions, "
            f"(2) main empirical results with specific numbers from tables, "
            f"(3) key algorithmic steps or procedures, "
            f"(4) important ablations or comparisons. "
            f"Be precise — include variable names, numerical results, and table data."
        )
    else:
        query = (
            f"Provide a detailed, comprehensive summary of the content at this URL. "
            f"Include all key concepts, code examples, and technical details. "
            f"URL: {url}"
        )

    has_dedicated_search_key = bool(
        settings.search_api_key
        and settings.search_base_url
        and settings.search_api_key != settings.llm_api_key
    )

    try:
        client = _get_http_client()

        if has_dedicated_search_key:
            headers = {
                "Authorization": f"Bearer {settings.search_api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": "sonar",
                "messages": [{"role": "user", "content": query}],
                "max_tokens": 4096,
            }
            resp = await client.post(
                f"{settings.search_base_url}/chat/completions",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            content = resp.json()["choices"][0]["message"]["content"].strip()
        elif settings.llm_api_key and settings.llm_base_url:
            headers = {
                "Authorization": f"Bearer {settings.llm_api_key}",
                "Content-Type": "application/json",
            }
            payload = {"query": query, "max_results": 5}
            resp = await client.post(
                f"{settings.llm_base_url}/v1/search/perplexity-search",
                headers=headers, json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            parts = []
            for r in data.get("results", []):
                snippet = r.get("snippet", r.get("content", r.get("text", "")))
                if snippet:
                    parts.append(snippet)
            content = "\n\n".join(parts)
        else:
            return {"url": url, "content": "", "error": "search not configured"}

        if len(content.split()) < _MIN_DOWNLOAD_WORDS:
            return {"url": url, "content": "", "error": "search returned too little"}
        return {"url": url, "content": content, "word_count": len(content.split()), "via": "search"}
    except Exception as e:
        return {"url": url, "content": "", "error": f"search: {e}"}


async def download_url(url: str, *, title: str = "") -> dict:
    """Fetch content from a URL with cascading fallbacks.

    Returns ``{"url", "content", "word_count", "via"}`` on success,
    ``{"url", "content": "", "error"}`` on failure.

    Strategy — each stage can produce a result.  If the result is
    *thin* (< 500 words) it is stashed as a fallback and the cascade
    continues.  The first *non-thin* result wins; if every stage is
    thin the best (most words) fallback is returned.

    Cascade order:

    1. **trafilatura** — fast static HTML extraction.  For arxiv URLs
       we try the HTML rendering first, then the abstract page.
    2. **browser** — headless Chromium (handles JS-rendered sites).
    3. **Jina Reader** — ``r.jina.ai`` markdown API.  Handles JS,
       complex layouts, and some PDFs.  No API key required.
    4. **search** — ask a search-augmented LLM (Perplexity / NVIDIA
       Hub) to summarize the content.  For papers/PDFs this uses a
       precision-oriented prompt requesting equations and results.
    """
    original_url = url
    variants = _normalize_arxiv_urls(url)
    if len(variants) > 1:
        logger.info("URL variants: %s", " → ".join(variants))

    best_thin: dict | None = None

    def _stash_or_return(result: dict) -> dict | None:
        """Return the result if it's substantial; stash it otherwise."""
        nonlocal best_thin
        if not result.get("content"):
            return None
        result["url"] = original_url
        if not _is_thin(result):
            return result
        if best_thin is None or result.get("word_count", 0) > best_thin.get("word_count", 0):
            best_thin = result
            logger.info("Stashed thin result (%dw via %s), continuing cascade",
                        result.get("word_count", 0), result.get("via", "?"))
        return None

    # 1. trafilatura on each URL variant
    for variant in variants:
        result = await _fetch_with_trafilatura(variant)
        if result.get("content"):
            result["via"] = "trafilatura"
        ret = _stash_or_return(result)
        if ret:
            return ret

    # 2. browser (playwright) — handles JS-rendered sites
    result = await _fetch_with_browser(variants[0])
    ret = _stash_or_return(result)
    if ret:
        return ret

    # 3. Jina Reader — handles JS, complex layouts, some PDFs
    result = await _fetch_with_jina(original_url)
    ret = _stash_or_return(result)
    if ret:
        return ret

    # 4. search fallback — use original URL for best LLM retrieval
    result = await _fetch_via_search(original_url, title=title)
    ret = _stash_or_return(result)
    if ret:
        return ret

    # All strategies were thin or failed — return the best thin result
    if best_thin:
        logger.info("Using best thin fallback (%dw via %s)",
                    best_thin.get("word_count", 0), best_thin.get("via", "?"))
        return best_thin

    # Total failure
    result["url"] = original_url
    return result


_YT_RE = re.compile(
    r'(?:youtube\.com/watch\?.*v=|youtu\.be/|youtube\.com/embed/)'
    r'([A-Za-z0-9_-]{11})'
)


def _extract_youtube_id(url: str) -> str | None:
    """Extract the 11-char YouTube video ID from common URL patterns."""
    m = _YT_RE.search(url)
    return m.group(1) if m else None


async def _fetch_oembed(youtube_id: str) -> dict:
    """Fetch video metadata from YouTube oEmbed (no API key needed)."""
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={youtube_id}&format=json"
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(oembed_url)
            resp.raise_for_status()
            return resp.json()
    except Exception as e:
        logger.warning("oEmbed failed for %s: %s", youtube_id, e)
        return {}


def _fetch_transcript(youtube_id: str) -> str:
    """Fetch auto-generated transcript text (no API key needed)."""
    try:
        from youtube_transcript_api import YouTubeTranscriptApi
        snippets = YouTubeTranscriptApi.get_transcript(youtube_id)
        return " ".join(s["text"] for s in snippets)
    except Exception as e:
        logger.info("Transcript unavailable for %s: %s", youtube_id, e)
        return ""


async def _save_video_stub(
    url: str,
    topic_slug: str,
    *,
    title: str = "",
    track: str = "pedagogy",
    audience: str = "",
) -> dict:
    """Write a video metadata stub with oEmbed info + transcript.

    For YouTube URLs, fetches metadata via oEmbed and transcript via
    youtube-transcript-api. For non-YouTube URLs, writes a minimal
    stub with just the URL and title.

    Returns dict matching ``download_source`` shape (saved, path, word_count).
    """
    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    if track == "reference":
        dl_dir = topics_dir / topic_slug / "reference"
    else:
        dl_dir = topics_dir / topic_slug
    dl_dir.mkdir(parents=True, exist_ok=True)

    slug = _source_slug(url)
    out_path = dl_dir / f"{slug}.md"

    if out_path.exists():
        return {"saved": False, "path": str(out_path), "reason": "already exists",
                "word_count": len(out_path.read_text().split())}

    yt_id = _extract_youtube_id(url)
    today = time.strftime("%Y-%m-%d")

    channel = ""
    if yt_id:
        oembed = await _fetch_oembed(yt_id)
        if oembed.get("title") and not title:
            title = oembed["title"]
        channel = oembed.get("author_name", "")

        transcript = await asyncio.get_event_loop().run_in_executor(
            None, _fetch_transcript, yt_id,
        )
    else:
        transcript = ""

    lines = [
        f"# Source: {url}",
        f"# Title: {title}",
        f"# Type: video",
    ]
    if yt_id:
        lines.append(f"# youtube_id: {yt_id}")
    if channel:
        lines.append(f"# Author: {channel}")
        lines.append(f"# Author Slug: {re.sub(r'[^a-z0-9]+', '-', channel.lower()).strip('-')}")
    if audience:
        lines.append(f"# Audience: {audience}")
    lines.append(f"# Downloaded: {today}")
    lines.append(f"# Via: video-metadata")
    lines.append("")

    if transcript:
        lines.append("## Transcript")
        lines.append("")
        lines.append(transcript)
    else:
        lines.append("(Video content — no transcript available; embed via source URL)")

    content = "\n".join(lines) + "\n"
    out_path.write_text(content)
    word_count = len(content.split())
    logger.info("Saved video stub: %s (%d words, transcript=%s)",
                slug, word_count, "yes" if transcript else "no")
    return {"saved": True, "path": str(out_path), "word_count": word_count,
            "url": url, "via": "video-metadata"}


async def download_source(
    url: str,
    topic_slug: str,
    *,
    title: str = "",
    extract_images: bool = False,
    track: str = "pedagogy",
    audience: str = "",
) -> dict:
    """Download a URL and save it to a wiki topic directory.

    Returns dict with ``saved``, ``path``, ``word_count`` on success.
    Resolves author via the author registry and writes ``# Author:`` /
    ``# Author Slug:`` headers for downstream consumers.

    When ``track="reference"``, saves to a ``reference/`` subdirectory
    under the topic folder instead of the topic folder itself.
    """
    from .wiki_authors import (
        resolve_author, extract_author_from_html, append_author,
        is_venue, parse_arxiv_id, extract_arxiv_authors, format_paper_authors,
    )

    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    if track == "reference":
        dl_dir = topics_dir / topic_slug / "reference"
    else:
        dl_dir = topics_dir / topic_slug
    dl_dir.mkdir(parents=True, exist_ok=True)

    slug = _source_slug(url)
    out_path = dl_dir / f"{slug}.md"

    if out_path.exists() and out_path.stat().st_size > 200:
        existing_text = out_path.read_text()
        cleaned_words = len(_clean_extracted_text(existing_text).split())
        if cleaned_words >= _THIN_CONTENT_WORDS:
            return {"saved": False, "path": str(out_path), "reason": "already exists",
                    "word_count": len(existing_text.split())}
        logger.info("Existing file is thin (%dw cleaned < %d), re-downloading: %s",
                    cleaned_words, _THIN_CONTENT_WORDS, slug)

    result = await download_url(url, title=title)
    if not result.get("content"):
        return {"saved": False, "url": url, "error": result.get("error", "no content")}

    via = result.get("via", "unknown")
    today = time.strftime("%Y-%m-%d")

    # --- Author resolution ---
    author_name = ""
    author_slug = ""
    author_entry = resolve_author(url)

    if author_entry and is_venue(author_entry.get("slug", "")):
        # Venue (arXiv, ACL, JMLR, NeurIPS) — resolve to real paper authors
        arxiv_id = parse_arxiv_id(url)
        if arxiv_id:
            try:
                paper_authors = await extract_arxiv_authors(arxiv_id)
                author_name = format_paper_authors(paper_authors)
            except Exception as e:
                logger.warning("arXiv API failed for %s: %s", arxiv_id, e)
                author_name = ""
        author_slug = ""
    elif author_entry:
        author_name = author_entry.get("name", "")
        author_slug = author_entry.get("slug", "")
    elif result.get("_raw_html"):
        extracted = extract_author_from_html(result["_raw_html"])
        if extracted:
            author_name = extracted
            author_slug = re.sub(r"[^a-z0-9]+", "-", extracted.lower()).strip("-")
            domain = urlparse(url).netloc.replace("www.", "")
            append_author({
                "name": extracted,
                "slug": author_slug,
                "type": "person",
                "domains": [domain],
                "homepage": f"https://{domain}",
            })

    header_lines = [f"# Source: {url}"]
    if author_name:
        header_lines.append(f"# Author: {author_name}")
    if author_slug:
        header_lines.append(f"# Author Slug: {author_slug}")
    header_lines.extend([f"# Title: {title}", f"# Fetched via: {via}", f"# Date: {today}"])
    if audience:
        header_lines.append(f"# Audience: {audience}")
    header = "\n".join(header_lines) + "\n\n"

    out_path.write_text(header + result["content"])

    logger.info("Downloaded %s -> %s (%d words)", url, out_path.name, result.get("word_count", 0))
    response = {
        "saved": True,
        "path": str(out_path),
        "word_count": result.get("word_count", 0),
        "via": via,
    }

    if extract_images and result.get("_raw_html"):
        try:
            from .wiki_images import process_source_images

            image_result = await process_source_images(
                topic_slug=topic_slug,
                page_title=title or slug,
                page_url=url,
                raw_html=result["_raw_html"],
                js_dimensions=result.get("_js_image_data"),
            )
            response["images"] = image_result
        except Exception as e:
            logger.warning("Image extraction failed for %s: %s", url, e)
            response["images"] = {"status": "error", "error": str(e)}

    return response


async def enrich_wiki_topic(
    topic_slug: str,
    sources: list[dict],
    *,
    max_concurrent: int = 3,
    extract_images: bool = False,
    track: str = "pedagogy",
    audience: str = "",
) -> dict:
    """Download multiple sources into a wiki topic directory.

    Args:
        topic_slug: wiki topic (e.g. 'attention-mechanism')
        sources: list of ``{"url": str, "title": str}`` dicts
        extract_images: also extract, annotate, and store educational images
        track: ``"pedagogy"`` (default) or ``"reference"``
        audience: audience tag for downloaded sources (e.g. ``"practitioner"``)

    Returns summary with counts of saved/skipped/failed.
    """
    sem = asyncio.Semaphore(max_concurrent)
    results = {"saved": 0, "skipped": 0, "failed": 0, "details": []}

    async def _dl(src: dict) -> dict:
        async with sem:
            src_audience = src.get("audience", audience)
            role = src.get("role", "")
            if role.startswith("video"):
                return await _save_video_stub(
                    src["url"], topic_slug, title=src.get("title", ""),
                    track=track, audience=src_audience,
                )
            return await download_source(
                src["url"], topic_slug, title=src.get("title", ""),
                extract_images=extract_images,
                track=track,
                audience=src_audience,
            )

    futures = [asyncio.ensure_future(_dl(s)) for s in sources if s.get("url")]
    for coro in asyncio.as_completed(futures):
        r = await coro
        if r.get("saved"):
            results["saved"] += 1
        elif r.get("reason") == "already exists":
            results["skipped"] += 1
        else:
            results["failed"] += 1
        results["details"].append(r)

    return results


# ---------------------------------------------------------------------------
# Source curation — LLM curates additions to the wiki library per lesson
# ---------------------------------------------------------------------------

CURATE_LIBRARY_PROMPT = """\
You are curating a teaching wiki — a small, high-quality library of the \
best resources on each topic. Think of it as the "recommended reading" \
shelf you would build for a colleague.

LESSON: {lesson_title}

{course_profile}

YOUR CURRENT LIBRARY FOR THIS TOPIC ({existing_count} sources):
{existing_sources}

CONCEPT GAPS (what the library does not yet cover well):
{gaps_list}

CANDIDATE SOURCES FOUND VIA SEARCH:
{candidates_text}

YOUR TASK:
Look at your current library. Look at the gaps. Look at the candidates.
Which candidates, if any, would genuinely improve this library?

A source earns a spot ONLY if it:
- Substantively covers one or more gaps (not just mentions them)
- Adds something the existing library does not already have
- Is high quality: clear writing, reputable author, stable URL
- A single great source that covers 3 gaps is better than 3 mediocre \
sources covering 1 gap each

Do NOT add sources that are redundant with what the library already has.
Do NOT add thin content (forum posts, abstracts, stubs).
It is perfectly fine — even expected — to add ZERO sources if the \
candidates are not good enough.

IMPORTANT: Seminal research papers (arxiv, ACL Anthology, NeurIPS, ICML) \
and authoritative textbook chapters (d2l.ai, MIT OCW) deserve extra \
consideration — even if the search snippet is thin, these are often the \
highest-value sources for a curated library. Don't skip a landmark paper \
just because its snippet is an abstract.

MULTI-MODAL BALANCE: A great library serves multiple learning styles. \
If the current library has no video content and a good video/video_tutorial \
candidate exists, prefer adding it — learners benefit from seeing concepts \
demonstrated visually. YouTube tutorials from recognized educators \
(deeplearning.ai, Anthropic, etc.) are especially \
valuable. Assign role "video" or "video_tutorial" so downstream tools \
handle them correctly.

Return JSON:
{{
  "additions": [
    {{
      "url": "exact URL from candidates above",
      "title": "source title",
      "role": "tutorial|paper|reference_doc|code|video|video_tutorial",
      "why": "1-2 sentences: what this adds to the library that it lacks",
      "gaps_covered": ["which gaps from the list above this source covers"],
      "level": "beginner|intermediate|advanced",
      "audience": "technical|practitioner|general|all"
    }}
  ],
  "near_misses": [
    {{
      "url": "exact URL",
      "title": "source title",
      "why_not": "1 sentence: why this was close but didn't make the cut"
    }}
  ],
  "uncovered_gaps": ["gaps from the list above that NO candidate covers well"],
  "reasoning": "1-2 sentences: overall curation rationale"
}}

Return ONLY valid JSON.
"""


def get_existing_source_urls(topic_slug: str) -> set[str]:
    """Scan a wiki topic directory for existing source URLs.

    Reads ``# Source:`` headers from downloaded markdown files.
    """
    topic_dir = _WIKI_DIR / "resources" / "by-topic" / topic_slug
    urls: set[str] = set()
    if not topic_dir.is_dir():
        return urls
    for f in topic_dir.glob("*.md"):
        try:
            first_line = f.read_text(errors="ignore").split("\n", 1)[0]
            if first_line.startswith("# Source:"):
                url = first_line.replace("# Source:", "").strip()
                if url:
                    urls.add(url)
        except Exception:
            pass
    return urls


def _get_existing_source_details(topic_slug: str) -> list[dict]:
    """Get title and URL for each existing source in a topic directory."""
    topic_dir = _WIKI_DIR / "resources" / "by-topic" / topic_slug
    sources: list[dict] = []
    if not topic_dir.is_dir():
        return sources
    for f in sorted(topic_dir.glob("*.md")):
        try:
            text = f.read_text(errors="ignore")
            lines = text.split("\n", 4)
            url = ""
            title = ""
            for line in lines[:4]:
                if line.startswith("# Source:"):
                    url = line.replace("# Source:", "").strip()
                elif line.startswith("# Title:"):
                    title = line.replace("# Title:", "").strip()
            if url:
                sources.append({"url": url, "title": title or f.stem})
        except Exception:
            pass
    return sources


async def curate_best_sources(
    lesson_title: str,
    concept_gaps: list[str],
    search_results_by_gap: dict[str, list[dict]],
    existing_source_urls: set[str],
    *,
    topic_slug: str = "",
    course_profile: dict | None = None,
) -> dict:
    """Curate library additions for a lesson in one batched LLM call.

    Shows the LLM the existing library, the concept gaps, and all
    candidate sources, then asks which (if any) genuinely improve the
    collection. Returns::

        {
            "picks": [{"url", "title", "role", "why", "gaps_covered", "level"}, ...],
            "all_candidates": [{"gap", "url", "title"}, ...],
        }
    """
    from .course_enricher import _call_llm_json

    # Build existing library description
    if topic_slug:
        existing_details = _get_existing_source_details(topic_slug)
    else:
        existing_details = [{"url": u, "title": ""} for u in sorted(existing_source_urls)]

    existing_text = "\n".join(
        f"- {s['title'] or s['url'][:60]}  ({s['url']})"
        for s in existing_details
    ) or "(empty — no sources yet)"

    # Build gaps list
    gaps_list = "\n".join(f"- {g}" for g in concept_gaps)

    # Build deduplicated candidate list from all search results
    all_candidates: list[dict] = []
    candidates_by_url: dict[str, dict] = {}
    for gap, results in search_results_by_gap.items():
        for r in results:
            snippet = r.get("content", "")[:1000]
            for c in r.get("citations", []):
                url = c.get("url", "") if isinstance(c, dict) else str(c)
                title = c.get("title", "") if isinstance(c, dict) else ""
                if url and url not in existing_source_urls:
                    all_candidates.append({"gap": gap, "url": url, "title": title})
                    if url not in candidates_by_url:
                        candidates_by_url[url] = {
                            "url": url, "title": title,
                            "snippet": snippet, "gaps": [gap],
                        }
                    else:
                        if gap not in candidates_by_url[url]["gaps"]:
                            candidates_by_url[url]["gaps"].append(gap)

    if not candidates_by_url:
        return {"picks": [], "all_candidates": all_candidates}

    # Format candidates, prioritizing those that cover multiple gaps
    sorted_candidates = sorted(
        candidates_by_url.values(),
        key=lambda c: len(c["gaps"]),
        reverse=True,
    )

    candidates_text = ""
    for i, cand in enumerate(sorted_candidates[:15]):
        gaps_str = ", ".join(cand["gaps"][:4])
        candidates_text += (
            f"\n--- CANDIDATE {i + 1} ---\n"
            f"URL: {cand['url']}\n"
            f"Title: {cand['title']}\n"
            f"Relevant to gaps: {gaps_str}\n"
            f"Content preview: {cand['snippet'][:600]}\n"
        )

    from .course_generator import _format_course_profile
    prompt = CURATE_LIBRARY_PROMPT.format(
        lesson_title=lesson_title,
        course_profile=_format_course_profile(course_profile),
        existing_count=len(existing_details),
        existing_sources=existing_text,
        gaps_list=gaps_list,
        candidates_text=candidates_text,
    )

    try:
        result = await _call_llm_json(prompt, max_tokens=4096, temperature=0.0)
    except Exception as e:
        logger.warning("Library curation failed for %r: %s", lesson_title, e)
        return {"picks": [], "all_candidates": all_candidates}

    additions = result.get("additions", [])
    near_misses = result.get("near_misses", [])
    uncovered_gaps = result.get("uncovered_gaps", [])
    reasoning = result.get("reasoning", "")

    picks = [a for a in additions if a.get("url")]

    if reasoning:
        logger.info("Curation for %r: %s", lesson_title, reasoning)
    logger.info(
        "Curation for %r: %d additions, %d near-misses, %d uncovered gaps "
        "(%d candidates, %d gaps)",
        lesson_title, len(picks), len(near_misses), len(uncovered_gaps),
        len(candidates_by_url), len(concept_gaps),
    )
    return {
        "picks": picks,
        "near_misses": near_misses,
        "uncovered_gaps": uncovered_gaps,
        "reasoning": reasoning,
        "all_candidates": all_candidates,
    }


# ---------------------------------------------------------------------------
# Post-curation audit — reviewer catches what the curator missed
# ---------------------------------------------------------------------------

AUDIT_CURATION_PROMPT = """\
You are reviewing a colleague's curation decisions for a teaching wiki. \
Your job is to catch any high-value sources they may have overlooked — \
especially seminal papers, authoritative textbooks, or uniquely clear \
explanations.

LESSON: {lesson_title}

CURRENT LIBRARY ({existing_count} sources):
{existing_sources}

WHAT THE CURATOR ADDED:
{picks_text}

NEAR-MISSES (curator considered but rejected):
{near_misses_text}

STILL-UNCOVERED GAPS:
{uncovered_gaps_text}

OTHER CANDIDATES THE CURATOR DID NOT CONSIDER (from the full search):
{remaining_candidates_text}

YOUR TASK:
Review the curation. Are there any sources in the near-misses or \
remaining candidates that the curator should have included? Focus on:

1. SEMINAL PAPERS the curator may have skipped because the snippet was \
thin (arxiv abstracts look thin but the papers are invaluable)
2. HIGH-AUTHORITY SOURCES from known institutions (MIT, Stanford, d2l.ai)
3. SOURCES THAT FILL UNCOVERED GAPS — the curator left gaps open, \
do any candidates address them?
4. NEAR-MISSES worth promoting — was the rejection reason weak?

Be selective. Only promote sources that genuinely earn a spot. If the \
curator made good choices, say so.

Return JSON:
{{
  "promotions": [
    {{
      "url": "exact URL",
      "title": "source title",
      "role": "tutorial|paper|reference_doc|code|video|video_tutorial",
      "why": "1-2 sentences: why this was missed and deserves a spot",
      "gaps_covered": ["which uncovered gaps this addresses"]
    }}
  ],
  "verdict": "good|needs_additions",
  "summary": "1 sentence: overall assessment"
}}

Return ONLY valid JSON.

Return ONLY valid JSON.
"""


async def audit_curation(
    lesson_title: str,
    curation_result: dict,
    all_candidates_by_url: dict[str, dict],
    existing_details: list[dict],
) -> dict:
    """Review curation decisions and flag potential misses.

    Takes the output of ``curate_best_sources`` and a second-opinion
    LLM pass to catch overlooked high-value sources.

    Returns::

        {
            "promotions": [{"url", "title", "role", "why", "gaps_covered"}, ...],
            "verdict": "good" | "needs_additions",
            "summary": str,
        }
    """
    from .course_enricher import _call_llm_json

    picks = curation_result.get("picks", [])
    near_misses = curation_result.get("near_misses", [])
    uncovered_gaps = curation_result.get("uncovered_gaps", [])

    # Build existing library text
    existing_text = "\n".join(
        f"- {s['title'] or s['url'][:60]}  ({s['url']})"
        for s in existing_details
    ) or "(empty)"

    # Build picks text
    if picks:
        picks_text = "\n".join(
            f"- [{p.get('role', '?')}] {p.get('title', p['url'][:60])}\n"
            f"  Covers: {', '.join(p.get('gaps_covered', []))}\n"
            f"  Why: {p.get('why', 'no reason given')}"
            for p in picks
        )
    else:
        picks_text = "(none — curator added nothing)"

    # Build near-misses text
    if near_misses:
        near_misses_text = "\n".join(
            f"- {nm.get('title', nm.get('url', '?')[:60])}: "
            f"{nm.get('why_not', 'no reason given')}"
            for nm in near_misses
        )
    else:
        near_misses_text = "(none reported)"

    # Build uncovered gaps text
    uncovered_gaps_text = "\n".join(
        f"- {g}" for g in uncovered_gaps
    ) if uncovered_gaps else "(all gaps addressed)"

    # Build remaining candidates (ones the curator didn't pick or near-miss)
    picked_urls = {p["url"] for p in picks}
    near_miss_urls = {nm.get("url", "") for nm in near_misses}
    known_urls = picked_urls | near_miss_urls

    remaining = [
        c for url, c in all_candidates_by_url.items()
        if url not in known_urls
    ]
    # Prioritize by multi-gap coverage and known high-authority domains
    _authority_domains = {
        "arxiv.org", "aclanthology.org", "proceedings.neurips.cc",
        "proceedings.mlr.press", "d2l.ai", "openreview.net",
        "mit.edu", "stanford.edu", "cs.cmu.edu",
    }

    def _authority_score(c: dict) -> int:
        from urllib.parse import urlparse
        domain = urlparse(c["url"]).netloc.lower()
        bonus = 3 if any(d in domain for d in _authority_domains) else 0
        return len(c.get("gaps", [])) + bonus

    remaining.sort(key=_authority_score, reverse=True)

    if remaining[:10]:
        remaining_text = ""
        for i, cand in enumerate(remaining[:10]):
            gaps_str = ", ".join(cand.get("gaps", [])[:3])
            remaining_text += (
                f"\n- [{i + 1}] {cand['title'] or cand['url'][:60]}\n"
                f"  URL: {cand['url']}\n"
                f"  Relevant to: {gaps_str}\n"
                f"  Preview: {cand.get('snippet', '')[:300]}\n"
            )
    else:
        remaining_text = "(none)"

    prompt = AUDIT_CURATION_PROMPT.format(
        lesson_title=lesson_title,
        existing_count=len(existing_details),
        existing_sources=existing_text,
        picks_text=picks_text,
        near_misses_text=near_misses_text,
        uncovered_gaps_text=uncovered_gaps_text,
        remaining_candidates_text=remaining_text,
    )

    try:
        result = await _call_llm_json(prompt, max_tokens=2048, temperature=0.0)
    except Exception as e:
        logger.warning("Curation audit failed for %r: %s", lesson_title, e)
        return {"promotions": [], "verdict": "good", "summary": f"Audit failed: {e}"}

    promotions = [p for p in result.get("promotions", []) if p.get("url")]
    verdict = result.get("verdict", "good")
    summary = result.get("summary", "")

    logger.info(
        "Audit for %r: %s — %d promotions. %s",
        lesson_title, verdict, len(promotions), summary,
    )
    return {
        "promotions": promotions,
        "verdict": verdict,
        "summary": summary,
    }


async def evaluate_and_filter_sources(
    lesson_title: str,
    concepts: list[str],
    search_results: list[dict],
    *,
    auto_approve_threshold: int = 4,
    approved_tiers: tuple[str, ...] = ("authoritative", "educational"),
) -> dict:
    """Quality-gate search results before wiki download.

    Calls the existing ``_evaluate_batch`` from course_enricher to score
    each search result on relevance (1-5) and quality_tier, then splits
    into three buckets:

    - **approved**: relevance >= threshold AND tier in approved_tiers
    - **proposed**: borderline (relevance 3, or tier "community")
    - **rejected**: relevance <= 2 or tier "low"

    Returns::

        {
            "approved":  [{"url": str, "title": str, "relevance": int, "quality_tier": str}, ...],
            "proposed":  [...],
            "rejected":  [...],
        }
    """
    from .course_enricher import _evaluate_batch

    if not search_results:
        return {"approved": [], "proposed": [], "rejected": []}

    # Dedup search results by cited URLs to avoid evaluating the same
    # source multiple times across teaching/reference tracks
    seen_urls: set[str] = set()
    deduped_results: list[dict] = []
    for r in search_results:
        citations = r.get("citations", [])
        new_citations = []
        for c in (citations if isinstance(citations, list) else []):
            url = c.get("url", "") if isinstance(c, dict) else str(c)
            if url and url not in seen_urls:
                seen_urls.add(url)
                new_citations.append(c)
        if new_citations:
            deduped = dict(r)
            deduped["citations"] = new_citations
            deduped_results.append(deduped)

    if len(deduped_results) < len(search_results):
        logger.info(
            "Deduped search results for %r: %d → %d results (%d duplicate URLs removed)",
            lesson_title, len(search_results), len(deduped_results),
            len(search_results) - len(deduped_results),
        )

    evaluations = await _evaluate_batch(
        lesson_title, concepts, deduped_results, batch_start_index=0,
    )

    approved: list[dict] = []
    proposed: list[dict] = []
    rejected: list[dict] = []

    for ev in evaluations:
        relevance = ev.get("relevance", 0)
        tier = ev.get("quality_tier", "low")
        citations = ev.get("original_citations", [])

        sources = []
        for c in (citations if isinstance(citations, list) else []):
            if isinstance(c, dict) and c.get("url"):
                sources.append({
                    "url": c["url"],
                    "title": c.get("title", ""),
                    "relevance": relevance,
                    "quality_tier": tier,
                    "topics_covered": ev.get("topics_covered", []),
                })
            elif isinstance(c, str) and c:
                sources.append({
                    "url": c,
                    "title": "",
                    "relevance": relevance,
                    "quality_tier": tier,
                    "topics_covered": ev.get("topics_covered", []),
                })

        if relevance >= auto_approve_threshold and tier in approved_tiers:
            approved.extend(sources)
        elif relevance <= 2 or tier == "low":
            rejected.extend(sources)
        else:
            proposed.extend(sources)

    # Deduplicate by URL, keeping highest relevance
    def _dedup(items: list[dict]) -> list[dict]:
        seen: dict[str, dict] = {}
        for item in items:
            url = item["url"]
            if url not in seen or item["relevance"] > seen[url]["relevance"]:
                seen[url] = item
        return list(seen.values())

    approved = _dedup(approved)
    proposed = _dedup(proposed)
    rejected = _dedup(rejected)

    # If a URL appears in approved, remove it from proposed/rejected
    approved_urls = {s["url"] for s in approved}
    proposed = [s for s in proposed if s["url"] not in approved_urls]
    rejected = [s for s in rejected if s["url"] not in approved_urls]

    logger.info(
        "Quality gate for %r: %d approved, %d proposed, %d rejected",
        lesson_title, len(approved), len(proposed), len(rejected),
    )
    return {"approved": approved, "proposed": proposed, "rejected": rejected}


def save_proposals(
    topic_slug: str,
    proposals: list[dict],
    *,
    run_label: str = "",
    track: str = "pedagogy",
) -> Path:
    """Write proposals.json for human review / audit trail.

    Appends to any existing proposals file so history accumulates
    across runs.  When ``track="reference"``, writes to the
    ``reference/`` subdirectory.
    """
    if track == "reference":
        topics_dir = _WIKI_DIR / "resources" / "by-topic" / topic_slug / "reference"
    else:
        topics_dir = _WIKI_DIR / "resources" / "by-topic" / topic_slug
    topics_dir.mkdir(parents=True, exist_ok=True)
    proposals_path = topics_dir / "proposals.json"

    existing: list[dict] = []
    if proposals_path.exists():
        try:
            existing = json.loads(proposals_path.read_text())
        except (json.JSONDecodeError, ValueError):
            existing = []

    entry = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "run_label": run_label,
        "sources": proposals,
    }
    existing.append(entry)

    proposals_path.write_text(json.dumps(existing, indent=2))
    logger.info("Saved %d proposals to %s", len(proposals), proposals_path)


def save_curation_report(
    topic_slug: str,
    lesson_title: str,
    *,
    curation: dict,
    audit: dict,
    existing_details: list[dict],
    download_result: dict | None = None,
    track: str = "pedagogy",
) -> Path:
    """Write a human-readable curation-report.md for quick review.

    Surfaces only actionable items: what was added, near-misses worth
    considering, reviewer promotions, and uncovered gaps that need
    manual sourcing.  When ``track="reference"``, writes to the
    ``reference/`` subdirectory.
    """
    if track == "reference":
        topics_dir = _WIKI_DIR / "resources" / "by-topic" / topic_slug / "reference"
    else:
        topics_dir = _WIKI_DIR / "resources" / "by-topic" / topic_slug
    topics_dir.mkdir(parents=True, exist_ok=True)
    report_path = topics_dir / "curation-report.md"

    picks = curation.get("picks", [])
    near_misses = curation.get("near_misses", [])
    uncovered = curation.get("uncovered_gaps", [])
    curator_reasoning = curation.get("reasoning", "")
    all_candidates = curation.get("all_candidates", [])

    promotions = audit.get("promotions", [])
    verdict = audit.get("verdict", "good")
    reviewer_summary = audit.get("summary", "")

    total_added = len(picks) + len(promotions)
    saved = download_result.get("saved", 0) if download_result else "?"
    failed = download_result.get("failed", 0) if download_result else 0

    lines: list[str] = []
    ts = time.strftime("%Y-%m-%d %H:%M")
    lines.append(f"# Curation Report: {lesson_title}")
    lines.append(f"**Topic:** `{topic_slug}` | **Date:** {ts}")
    lines.append(f"**Library:** {len(existing_details)} existing → "
                 f"{len(existing_details) + total_added} sources "
                 f"({total_added} added, {saved} downloaded"
                 f"{f', {failed} failed' if failed else ''})")
    lines.append(f"**Candidates evaluated:** {len(set(c.get('url', '') for c in all_candidates))}")
    lines.append(f"**Reviewer verdict:** {verdict}")
    lines.append("")

    # --- Added ---
    lines.append(f"## Added ({total_added})")
    if not picks and not promotions:
        lines.append("_No sources added — library is sufficient._")
    for p in picks:
        gc = p.get("gaps_covered", [])
        gc_str = f" — covers: {', '.join(gc)}" if gc else ""
        lines.append(f"- **[{p.get('role', '?')}]** [{p.get('title', 'Untitled')}]({p['url']})")
        lines.append(f"  {p.get('why', '')}")
        if gc_str:
            lines.append(f"  {gc_str}")
    for p in promotions:
        gc = p.get("gaps_covered", [])
        gc_str = f" — fills: {', '.join(gc)}" if gc else ""
        lines.append(f"- **[{p.get('role', '?')}]** [{p.get('title', 'Untitled')}]({p['url']}) "
                     f"*(promoted by reviewer)*")
        lines.append(f"  {p.get('why', '')}")
        if gc_str:
            lines.append(f"  {gc_str}")
    lines.append("")

    # --- Near-Misses ---
    if near_misses:
        lines.append(f"## Near-Misses ({len(near_misses)}) — Worth a Second Look")
        lines.append("_The curator considered these but passed. "
                     "Override if you disagree._")
        lines.append("")
        for nm in near_misses:
            title = nm.get("title", nm.get("url", "?"))
            url = nm.get("url", "")
            why_not = nm.get("why_not", "No reason given")
            url_line = f" — [{title}]({url})" if url else f" — {title}"
            lines.append(f"- **{title[:60]}**{url_line if url else ''}")
            lines.append(f"  _Skipped because:_ {why_not}")
        lines.append("")

    # --- Uncovered Gaps ---
    if uncovered:
        lines.append(f"## Uncovered Gaps ({len(uncovered)}) — No Good Candidates Found")
        lines.append("_Consider manually sourcing these, or run "
                     "enrichment again with different search terms._")
        lines.append("")
        for gap in uncovered:
            lines.append(f"- {gap}")
        lines.append("")

    # --- Reasoning ---
    if curator_reasoning or reviewer_summary:
        lines.append("## Reasoning")
        if curator_reasoning:
            lines.append(f"**Curator:** {curator_reasoning}")
        if reviewer_summary:
            lines.append(f"**Reviewer:** {reviewer_summary}")
        lines.append("")

    report_text = "\n".join(lines)

    # Append to existing report (accumulate across runs)
    if report_path.exists():
        existing = report_path.read_text()
        report_text = existing + "\n---\n\n" + report_text

    report_path.write_text(report_text)
    logger.info("Saved curation report to %s", report_path)
    return report_path
    return proposals_path


# ---------------------------------------------------------------------------
# Reference track — precision-first curation for tutor reference KB
# ---------------------------------------------------------------------------

_REFERENCE_AUTHORITY_DOMAINS = {
    "arxiv.org", "aclanthology.org", "proceedings.neurips.cc",
    "proceedings.mlr.press", "openreview.net",
    "pytorch.org", "tensorflow.org", "huggingface.co",
    "docs.python.org", "openai.com",
    "d2l.ai", "mit.edu", "stanford.edu", "cs.cmu.edu",
}

_REFERENCE_PENALIZE_PATTERNS = [
    "medium.com/@", "towardsdatascience.com",
    "analyticsvidhya.com", "kdnuggets.com",
    "explained in 5 min", "for beginners",
]

_PRECISION_SIGNAL_RE = re.compile(
    r'(\d+\.?\d*\s*%|'       # percentage numbers
    r'=\s*\d|'               # equations with numbers
    r'\\frac|\\sum|\\prod|'  # LaTeX formulas
    r'```|'                  # code blocks
    r'default[s]?\s*[=:]|'   # default values
    r'benchmark|ablation)',   # benchmark/ablation mentions
    re.IGNORECASE,
)


def _filter_reference_candidates(
    search_results_by_need: dict[str, list[dict]],
    existing_urls: set[str],
    *,
    max_per_need: int = 5,
    max_total: int = 20,
) -> tuple[list[dict], dict[str, list[dict]]]:
    """Pre-filter and group search candidates for the reference curator.

    Deduplicates by URL, boosts authority domains and precision signals,
    penalizes tutorial-heavy sources, then returns the top candidates
    grouped by the need they were found for.

    Returns ``(all_candidates_flat, grouped_candidates)`` where
    grouped_candidates maps need_type to a ranked list of candidates.
    """
    candidates_by_url: dict[str, dict] = {}
    all_flat: list[dict] = []

    for need_type, results in search_results_by_need.items():
        for r in results:
            snippet = r.get("content", "")[:1200]
            for c in r.get("citations", []):
                url = c.get("url", "") if isinstance(c, dict) else str(c)
                title = c.get("title", "") if isinstance(c, dict) else ""
                if not url or url in existing_urls:
                    continue
                all_flat.append({"need_type": need_type, "url": url, "title": title})
                if url not in candidates_by_url:
                    candidates_by_url[url] = {
                        "url": url, "title": title,
                        "snippet": snippet,
                        "needs": [need_type],
                        "score": 0,
                    }
                else:
                    if need_type not in candidates_by_url[url]["needs"]:
                        candidates_by_url[url]["needs"].append(need_type)

    # Score each candidate
    for cand in candidates_by_url.values():
        domain = urlparse(cand["url"]).netloc.lower()

        # Multi-need coverage
        cand["score"] += len(cand["needs"]) * 2

        # Authority domain boost
        if any(d in domain for d in _REFERENCE_AUTHORITY_DOMAINS):
            cand["score"] += 5

        # Precision signal boost
        if _PRECISION_SIGNAL_RE.search(cand["snippet"]):
            cand["score"] += 3

        # Penalize tutorial-heavy domains
        url_lower = cand["url"].lower()
        if any(p in url_lower for p in _REFERENCE_PENALIZE_PATTERNS):
            cand["score"] -= 4

    # Group by need and take top N per group
    grouped: dict[str, list[dict]] = {}
    for cand in candidates_by_url.values():
        for need in cand["needs"]:
            grouped.setdefault(need, []).append(cand)

    for need in grouped:
        grouped[need].sort(key=lambda c: c["score"], reverse=True)
        grouped[need] = grouped[need][:max_per_need]

    # Build deduplicated top-N across all groups
    seen: set[str] = set()
    final_grouped: dict[str, list[dict]] = {}
    total = 0
    for need in sorted(grouped.keys()):
        need_list: list[dict] = []
        for cand in grouped[need]:
            if cand["url"] not in seen and total < max_total:
                seen.add(cand["url"])
                need_list.append(cand)
                total += 1
        if need_list:
            final_grouped[need] = need_list

    return all_flat, final_grouped


CURATE_REFERENCE_PROMPT = """\
You are curating a **reference library for a Socratic tutor** — a \
small, high-quality collection of authoritative sources that deepen \
the tutor's ability to teach this topic. The tutor needs sources for \
two purposes:

1. **Precision** — exact formulas, benchmark numbers, API defaults, \
   and citable facts the tutor can quote when a student asks for \
   specifics.
2. **Understanding** — detailed process descriptions, design rationale, \
   step-by-step procedures, and concept breakdowns the tutor can use \
   to explain *how* and *why* things work.

Both are equally important. A paper describing a novel training \
pipeline step by step is as valuable as one with a benchmark table.

LESSON: {lesson_title}

EXISTING LIBRARY ({existing_count} sources):
{existing_sources}

REFERENCE NEEDS (what the tutor is missing):
{needs_text}

CANDIDATES (grouped by need):
{candidates_text}

YOUR TASK: For each reference need above, pick the BEST candidate — \
the one that gives the tutor the most useful, authoritative material \
for teaching. Pick at most 2 per need, 6 total.

SELECTION CRITERIA (all valued equally — pick what best fills each need):
- SEMINAL PAPERS — whether they contain equations, training procedures, \
  architectural descriptions, or empirical results
- OFFICIAL DOCUMENTATION — parameter specs, API surface, defaults
- PROCESS DESCRIPTIONS — step-by-step training pipelines, system \
  designs, algorithmic procedures from authoritative sources
- BENCHMARK STUDIES — concrete performance numbers and ablations
- IMPLEMENTATIONS — working code, cookbook recipes, derivations

IMPORTANT:
- For each pick, your "anchor" field MUST name a specific element the \
  source contributes. This can be a formula, a number, a default value, \
  a code pattern, a step-by-step procedure, or a design rationale. \
  "Provides good background" is NOT acceptable, but "detailed \
  description of the critique-revision-RLAIF pipeline" IS acceptable.
- If no candidate adequately fills a need, mark it as unfilled with a \
  search_hint the tutor can use at runtime.
- It is perfectly fine to add ZERO sources. Thin or generic content \
  has no place in a reference library.
- Seminal papers with thin snippets (just an abstract) are STILL worth \
  adding — the paper itself is the value, not the snippet.

Return JSON:
{{
  "additions": [
    {{
      "url": "exact URL from candidates above",
      "title": "source title",
      "role": "paper|reference_doc|code|benchmark|explainer",
      "need_type": "which need this fills",
      "anchor": "specific element: formula, number, default, code pattern, procedure, or design rationale",
      "why": "1-2 sentences: what this adds to the tutor's ability to teach"
    }}
  ],
  "near_misses": [
    {{
      "url": "exact URL",
      "title": "source title",
      "why_not": "1 sentence: why this was close but didn't make the cut"
    }}
  ],
  "unfilled_needs": [
    {{
      "need_type": "which need remains unfilled",
      "description": "what was needed",
      "search_hint": "a query the tutor could use to search at runtime"
    }}
  ],
  "reasoning": "1-2 sentences: overall curation rationale"
}}

Return ONLY valid JSON.
"""


async def curate_reference_sources(
    lesson_title: str,
    typed_needs: list[dict],
    search_results_by_need: dict[str, list[dict]],
    existing_source_urls: set[str],
    *,
    topic_slug: str = "",
) -> dict:
    """Curate precision reference sources for the reference track.

    Takes typed needs from ``assess_reference_needs`` and grouped search
    results.  Returns picks, near-misses, and unfilled needs (ramps).

    Returns::

        {
            "picks": [{"url", "title", "role", "need_type", "anchor", "why"}, ...],
            "near_misses": [{"url", "title", "why_not"}, ...],
            "unfilled_needs": [{"need_type", "description", "search_hint"}, ...],
            "reasoning": str,
            "all_candidates": [{"need_type", "url", "title"}, ...],
        }
    """
    from .course_enricher import _call_llm_json

    if topic_slug:
        existing_details = _get_existing_source_details(topic_slug)
    else:
        existing_details = [{"url": u, "title": ""} for u in sorted(existing_source_urls)]

    existing_text = "\n".join(
        f"- {s['title'] or s['url'][:60]}  ({s['url']})"
        for s in existing_details
    ) or "(empty — no sources yet)"

    # Build needs text
    needs_text = "\n".join(
        f"- [{n['need_type']}] {n.get('description', '')}"
        for n in typed_needs
    )

    # Filter and group candidates
    all_candidates, grouped = _filter_reference_candidates(
        search_results_by_need, existing_source_urls,
    )

    if not grouped:
        return {
            "picks": [],
            "near_misses": [],
            "unfilled_needs": [
                {
                    "need_type": n["need_type"],
                    "description": n.get("description", ""),
                    "search_hint": (n.get("search_queries") or [""])[0],
                }
                for n in typed_needs
            ],
            "reasoning": "No candidates found for any reference need",
            "all_candidates": all_candidates,
        }

    # Format candidates grouped by need
    candidates_text = ""
    for need_type, cands in grouped.items():
        candidates_text += f"\n--- FOR NEED: {need_type} ---\n"
        for i, cand in enumerate(cands):
            candidates_text += (
                f"\nCandidate {i + 1}:\n"
                f"URL: {cand['url']}\n"
                f"Title: {cand['title']}\n"
                f"Preview: {cand['snippet'][:600]}\n"
            )

    prompt = CURATE_REFERENCE_PROMPT.format(
        lesson_title=lesson_title,
        existing_count=len(existing_details),
        existing_sources=existing_text,
        needs_text=needs_text,
        candidates_text=candidates_text,
    )

    try:
        result = await _call_llm_json(prompt, max_tokens=4096, temperature=0.0)
    except Exception as e:
        logger.warning("Reference curation failed for %r: %s", lesson_title, e)
        return {
            "picks": [],
            "near_misses": [],
            "unfilled_needs": [],
            "reasoning": f"LLM error: {e}",
            "all_candidates": all_candidates,
        }

    additions = result.get("additions", [])
    near_misses = result.get("near_misses", [])
    unfilled_needs = result.get("unfilled_needs", [])
    reasoning = result.get("reasoning", "")

    picks = [a for a in additions if a.get("url")]

    if reasoning:
        logger.info("Reference curation for %r: %s", lesson_title, reasoning)
    logger.info(
        "Reference curation for %r: %d picks, %d near-misses, %d unfilled "
        "(%d candidates evaluated)",
        lesson_title, len(picks), len(near_misses), len(unfilled_needs),
        len(all_candidates),
    )

    return {
        "picks": picks,
        "near_misses": near_misses,
        "unfilled_needs": unfilled_needs,
        "reasoning": reasoning,
        "all_candidates": all_candidates,
    }


# ---------------------------------------------------------------------------
# Reference track — reviewer audit
# ---------------------------------------------------------------------------

AUDIT_REFERENCE_PROMPT = """\
You are reviewing a colleague's curation of a reference library for a \
Socratic tutor. Your job is to catch high-value sources they may have \
overlooked — sources that would genuinely help the tutor teach this \
topic with depth and precision.

LESSON: {lesson_title}

CURRENT LIBRARY ({existing_count} sources):
{existing_sources}

WHAT THE CURATOR ADDED (reference track):
{picks_text}

NEAR-MISSES (curator considered but rejected):
{near_misses_text}

STILL-UNFILLED NEEDS:
{unfilled_needs_text}

OTHER CANDIDATES THE CURATOR DID NOT CONSIDER:
{remaining_candidates_text}

YOUR TASK:
Review the curation. Are there any sources in the near-misses or \
remaining candidates that should have been included? Focus on:

1. SEMINAL PAPERS skipped because the snippet was just an abstract — \
the paper itself is the value, whether it contains equations, \
training procedures, or design rationale
2. OFFICIAL DOCUMENTATION pages rejected for being "thin" — thin API \
docs are exactly what a reference library needs (parameter names, defaults)
3. SOURCES WITH SPECIFIC NUMBERS that fill unfilled needs — even a \
single benchmark table is valuable
4. PROCESS/ARCHITECTURE SOURCES — authoritative descriptions of how a \
key method works (training pipelines, system designs, algorithmic \
procedures). A paper describing a novel training procedure is as \
valuable as one with a benchmark table
5. CONCEPT COVERAGE — if a core lesson concept has no source at all \
in the library, flag near-misses or candidates that cover it

Be selective. Only promote sources that deliver something specific \
and useful for teaching. If the curator made good choices, say so.

Return JSON:
{{
  "promotions": [
    {{
      "url": "exact URL",
      "title": "source title",
      "role": "paper|reference_doc|code|benchmark|explainer",
      "need_type": "which unfilled need this addresses",
      "anchor": "specific element: formula, number, procedure, design rationale, or concept coverage",
      "why": "1-2 sentences: why this was missed and deserves a spot"
    }}
  ],
  "verdict": "good|needs_additions",
  "summary": "1 sentence: overall assessment"
}}

Return ONLY valid JSON.
"""


async def audit_reference_curation(
    lesson_title: str,
    curation_result: dict,
    all_candidates_by_url: dict[str, dict],
    existing_details: list[dict],
) -> dict:
    """Review reference curation decisions and flag potential misses.

    Same pattern as ``audit_curation`` but with precision-first criteria.

    Returns::

        {
            "promotions": [{"url", "title", "role", "need_type", "anchor", "why"}, ...],
            "verdict": "good" | "needs_additions",
            "summary": str,
        }
    """
    from .course_enricher import _call_llm_json

    picks = curation_result.get("picks", [])
    near_misses = curation_result.get("near_misses", [])
    unfilled_needs = curation_result.get("unfilled_needs", [])

    existing_text = "\n".join(
        f"- {s['title'] or s['url'][:60]}  ({s['url']})"
        for s in existing_details
    ) or "(empty)"

    if picks:
        picks_text = "\n".join(
            f"- [{p.get('role', '?')}] {p.get('title', p['url'][:60])}\n"
            f"  Need: {p.get('need_type', '?')}\n"
            f"  Anchor: {p.get('anchor', 'not specified')}\n"
            f"  Why: {p.get('why', 'no reason given')}"
            for p in picks
        )
    else:
        picks_text = "(none — curator added nothing)"

    if near_misses:
        near_misses_text = "\n".join(
            f"- {nm.get('title', nm.get('url', '?')[:60])}: "
            f"{nm.get('why_not', 'no reason given')}"
            for nm in near_misses
        )
    else:
        near_misses_text = "(none reported)"

    if unfilled_needs:
        unfilled_needs_text = "\n".join(
            f"- [{un['need_type']}] {un.get('description', '')}"
            for un in unfilled_needs
        )
    else:
        unfilled_needs_text = "(all needs addressed)"

    # Remaining candidates not picked or near-missed
    picked_urls = {p["url"] for p in picks}
    near_miss_urls = {nm.get("url", "") for nm in near_misses}
    known_urls = picked_urls | near_miss_urls

    remaining = [
        c for url, c in all_candidates_by_url.items()
        if url not in known_urls
    ]

    def _ref_authority_score(c: dict) -> int:
        domain = urlparse(c["url"]).netloc.lower()
        bonus = 5 if any(d in domain for d in _REFERENCE_AUTHORITY_DOMAINS) else 0
        precision = 3 if _PRECISION_SIGNAL_RE.search(c.get("snippet", "")) else 0
        return len(c.get("needs", [])) + bonus + precision

    remaining.sort(key=_ref_authority_score, reverse=True)

    if remaining[:10]:
        remaining_text = ""
        for i, cand in enumerate(remaining[:10]):
            needs_str = ", ".join(cand.get("needs", [])[:3])
            remaining_text += (
                f"\n- [{i + 1}] {cand['title'] or cand['url'][:60]}\n"
                f"  URL: {cand['url']}\n"
                f"  Relevant to: {needs_str}\n"
                f"  Preview: {cand.get('snippet', '')[:300]}\n"
            )
    else:
        remaining_text = "(none)"

    prompt = AUDIT_REFERENCE_PROMPT.format(
        lesson_title=lesson_title,
        existing_count=len(existing_details),
        existing_sources=existing_text,
        picks_text=picks_text,
        near_misses_text=near_misses_text,
        unfilled_needs_text=unfilled_needs_text,
        remaining_candidates_text=remaining_text,
    )

    try:
        result = await _call_llm_json(prompt, max_tokens=2048, temperature=0.0)
    except Exception as e:
        logger.warning("Reference audit failed for %r: %s", lesson_title, e)
        return {"promotions": [], "verdict": "good", "summary": f"Audit error: {e}"}

    promotions = result.get("promotions", [])
    promotions = [p for p in promotions if p.get("url")]

    logger.info(
        "Reference audit for %r: %s — %d promotions — %s",
        lesson_title,
        result.get("verdict", "?"),
        len(promotions),
        result.get("summary", ""),
    )

    return {
        "promotions": promotions,
        "verdict": result.get("verdict", "good"),
        "summary": result.get("summary", ""),
    }


# ---------------------------------------------------------------------------
# Reference track — source card extraction
# ---------------------------------------------------------------------------

_CARD_MIN_SOURCE_WORDS = 800

EXTRACT_CARD_PROMPT = """\
You are creating a **reference card** for a Socratic AI tutor. The tutor \
will consult this card during live conversations with students to ground \
its answers in authoritative sources.

SOURCE METADATA:
- Title: {title}
- URL: {url}
- Role: {role}
- Curated for need: {need_type}
- Key anchor: {anchor}
- Lesson: {lesson_title}
- Lesson concepts: {concepts}

FULL SOURCE TEXT (may be very long — extract only what matters):
{source_text}

YOUR TASK: Extract a concise reference card (~200-300 words) containing \
ONLY the information a tutor needs from this source. Focus on:

1. **Key formulas/equations** — write them out with variable definitions
2. **Key empirical results** — specific numbers, table rows, comparisons
3. **Key procedures/steps** — training pipelines, algorithms, workflows
4. **Design rationale** — why the authors made specific choices
5. **Defaults/parameters** — any configuration values, hyperparameters

Format the card as markdown:

```
# Card: [short title]
**Source:** [url]
**Role:** [role] | **Need:** [need_type]
**Anchor:** [what this source provides]

## Key Content
- [bullet points with specific facts, equations, numbers, procedures]
- [include equation names/numbers for cross-reference: "Eq. 1", "Section 3"]
- [cite specific numbers: "1.3B preferred over 175B", not "smaller preferred"]

## When to surface
[1-2 sentences: what student questions should trigger consulting this source]
```

RULES:
- Be SPECIFIC — include actual numbers, actual equations, actual steps
- Do NOT summarize vaguely ("discusses RLHF") — extract concrete facts
- Do NOT exceed 300 words — this must be compact
- If the source text is thin (just an abstract), extract what's there \
  and state the definition/process clearly from what IS available — \
  do NOT add disclaimers like "not defined" or "missing from excerpt"
- The full source is always available for deep lookup — this card is \
  the tutor's quick-reference index to know WHAT is in the source \
  and WHEN to consult it
"""


async def extract_reference_card(
    source_text: str,
    *,
    url: str = "",
    title: str = "",
    role: str = "",
    need_type: str = "",
    anchor: str = "",
    lesson_title: str = "",
    concepts: list[str] | None = None,
) -> str:
    """Extract a concise reference card from a full source document.

    Uses the curation metadata (anchor, role, need_type) to focus the
    extraction on what the tutor actually needs.  Returns markdown text.

    For short sources (< 800 words), returns the source as-is since
    it's already compact enough to use directly.
    """
    cleaned = _clean_extracted_text(source_text)
    if len(cleaned.split()) < _CARD_MIN_SOURCE_WORDS:
        logger.info("Source %s is short (%dw after cleaning), using as-is",
                     title or url[:50], len(cleaned.split()))
        return cleaned

    from .course_enricher import _call_llm

    # Truncate very long sources to fit in LLM context
    max_source_chars = 60000
    truncated = cleaned[:max_source_chars]
    if len(cleaned) > max_source_chars:
        truncated += "\n\n[... remainder truncated for extraction ...]"

    prompt = EXTRACT_CARD_PROMPT.format(
        title=title,
        url=url,
        role=role,
        need_type=need_type,
        anchor=anchor,
        lesson_title=lesson_title,
        concepts=", ".join(concepts or []),
        source_text=truncated,
    )

    try:
        card = await _call_llm(prompt, max_tokens=1500, temperature=0.0)
        card = card.strip()
        if card.startswith("```"):
            card = card.split("\n", 1)[-1]
            if card.endswith("```"):
                card = card[:-3]
            card = card.strip()
        logger.info("Extracted card for %s: %dw",
                     title or url[:50], len(card.split()))
        return card
    except Exception as e:
        logger.warning("Card extraction failed for %s: %s", title or url[:50], e)
        return ""


_CARD_SEMAPHORE = asyncio.Semaphore(5)


async def extract_cards_for_sources(
    topic_slug: str,
    picks: list[dict],
    *,
    lesson_title: str = "",
    concepts: list[str] | None = None,
) -> dict:
    """Extract reference cards for all downloaded sources in a topic.

    Reads each source file, calls ``extract_reference_card``, and saves
    the card as ``{slug}.card.md`` next to the full source.  Runs up to
    5 extractions in parallel using a semaphore.

    Returns ``{"extracted": int, "skipped": int, "failed": int}``.
    """
    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    ref_dir = topics_dir / topic_slug / "reference"
    if not ref_dir.is_dir():
        return {"extracted": 0, "skipped": 0, "failed": 0}

    pick_by_url = {}
    for p in picks:
        url = p.get("url", "")
        if url:
            pick_by_url[url] = p

    skipped = 0
    pending: list[tuple[Path, Path, dict, str]] = []

    for src_file in sorted(ref_dir.iterdir()):
        if src_file.suffix != ".md":
            continue
        if src_file.name.endswith(".card.md"):
            continue
        if src_file.name in ("curation-report.md",):
            continue

        source_text = src_file.read_text()
        first_line = source_text.split("\n", 1)[0]
        url = ""
        if first_line.startswith("# Source:"):
            url = first_line.replace("# Source:", "").strip()

        card_path = src_file.with_suffix(".card.md")
        if card_path.exists() and card_path.stat().st_size > 100:
            skipped += 1
            continue

        meta = pick_by_url.get(url, {})
        pending.append((src_file, card_path, meta, source_text))

    async def _extract_one(
        src_file: Path, card_path: Path, meta: dict, source_text: str,
    ) -> bool:
        async with _CARD_SEMAPHORE:
            card = await extract_reference_card(
                source_text,
                url=meta.get("url", ""),
                title=meta.get("title", src_file.stem),
                role=meta.get("role", ""),
                need_type=meta.get("need_type", ""),
                anchor=meta.get("anchor", ""),
                lesson_title=lesson_title,
                concepts=concepts,
            )
        if card:
            card_path.write_text(card)
            logger.info("Saved card: %s (%dw)", card_path.name, len(card.split()))
            return True
        return False

    results = await asyncio.gather(
        *(_extract_one(sf, cp, m, st) for sf, cp, m, st in pending),
        return_exceptions=True,
    )

    extracted = sum(1 for r in results if r is True)
    failed = sum(1 for r in results if r is not True)

    return {"extracted": extracted, "skipped": skipped, "failed": failed}


def _write_pending_item(
    item_type: str,
    topic_slug: str,
    data: dict,
    course: str = "",
) -> Path:
    """Write a pending wiki change to the staging area for later review."""
    _PENDING_DIR.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%dT%H%M%S")
    filename = f"{ts}_{item_type}_{topic_slug}.json"
    item = {
        "type": item_type,
        "topic_slug": topic_slug,
        "course": course,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "data": data,
    }
    out_path = _PENDING_DIR / filename
    out_path.write_text(json.dumps(item, indent=2))
    logger.info("Wrote pending %s item for %s: %s", item_type, topic_slug, filename)
    return out_path


def bootstrap_new_wiki_topic(
    proposed_slug: str,
    concepts: list[str],
    lesson_title: str,
    *,
    course_title: str = "",
) -> str:
    """Stage a new wiki topic page and concept-map entry for review.

    The topic subdirectory is created immediately (downloads need it),
    but the ``.md`` page and concept-map update are written to
    ``.pending/`` for human-reviewed merge.

    Returns the slug of the (staged) topic.
    """
    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    topics_dir.mkdir(parents=True, exist_ok=True)
    page_path = topics_dir / f"{proposed_slug}.md"

    if page_path.exists():
        logger.info("Topic page already exists: %s", proposed_slug)
        return proposed_slug

    # Create subdirectory immediately — downloads land here before merge
    (topics_dir / proposed_slug).mkdir(exist_ok=True)

    today = time.strftime("%Y-%m-%d")
    concept_lines = "\n".join(f"- {c}" for c in concepts)

    page_content = f"""# {lesson_title}

## Key Concepts
{concept_lines}

## Core Resources

*(To be populated by enrichment pipeline)*

## Coverage Assessment

- **Status:** Auto-created during course generation
- **Created:** {today}
- **Needs:** Research and resource curation for all listed concepts

## Last Verified
{today} (auto-created, needs manual review)
"""

    subtopic_slug = re.sub(r'[^a-z0-9]+', '-', lesson_title.lower().strip()).strip('-')[:40]
    concept_map_entry = (
        f"\n# {proposed_slug}\n"
        f"**{lesson_title}** — 1 subtopics, {len(concepts)} concepts\n\n"
        f"## {subtopic_slug}\n"
    )
    for c in concepts:
        concept_map_entry += f"- {c.lower()}\n"

    _write_pending_item(
        "new_topic",
        proposed_slug,
        {
            "page_content": page_content,
            "concept_map_entry": concept_map_entry,
            "concepts": concepts,
        },
        course=course_title,
    )

    sentinel = _WIKI_DIR / ".needs-rebuild"
    sentinel.touch()

    return proposed_slug


# ---------------------------------------------------------------------------
# Resource page regeneration — fills in bootstrapped stub pages
# ---------------------------------------------------------------------------

_HAND_CURATED_MARKERS = (
    "## Video (best)",
    "## Blog / Written explainer",
    "## Deep dive",
    "## Original paper",
    "## Code walkthrough",
)

RESOURCE_PAGE_PROMPT = """\
You are organizing a wiki resource page for a teaching library. Given the \
downloaded source files and images for a topic, classify each source and \
write a structured resource page.

TOPIC: {topic_slug}

{course_profile}

DOWNLOADED SOURCES:
{sources_text}

AVAILABLE IMAGES:
{images_text}

Write a Markdown resource page using these section headers (include only \
sections that have matching sources):

## Video (best)
## Blog / Written explainer (best)
## Deep dive
## Original paper
## Code walkthrough
## Official documentation
## Tutorial / Getting started

For each resource entry, use this format:
- **Author** — "Title"
- url: <url>  (or youtube_id: <id> for YouTube videos)
- Why: 1-2 sentences explaining what this resource uniquely contributes
- Level: beginner|intermediate|advanced
- Audience: technical|practitioner|general|all

At the end, add:
## Coverage notes
- **Strong:** areas well covered by the sources above
- **Weak:** areas with thin coverage
- **Gap:** important areas not covered at all

Write ONLY the Markdown content. No preamble.
"""


async def regenerate_resource_page(
    topic_slug: str,
    course_profile: dict | None = None,
) -> bool:
    """Regenerate a topic's resource page from its downloaded sources.

    Skips hand-curated pages (those with standard section headers like
    ``## Video (best)``).  For bootstrapped stubs, scans the topic
    directory for downloaded sources, classifies them via LLM, and
    writes a structured resource page.

    Returns True if the page was regenerated, False if skipped.
    """
    from .course_enricher import _call_llm

    topics_dir = _WIKI_DIR / "resources" / "by-topic"
    page_path = topics_dir / f"{topic_slug}.md"

    if not page_path.exists():
        logger.info("No resource page for %s — skipping regeneration", topic_slug)
        return False

    existing_text = page_path.read_text(errors="ignore")

    is_hand_curated = any(marker in existing_text for marker in _HAND_CURATED_MARKERS)
    if is_hand_curated:
        logger.info("Hand-curated resource page for %s — skipping regeneration", topic_slug)
        return False

    topic_dir = topics_dir / topic_slug
    sources_info: list[str] = []
    if topic_dir.is_dir():
        for f in sorted(topic_dir.glob("*.md")):
            try:
                text = f.read_text(errors="ignore")
                lines = text.split("\n")
                url = ""
                author = ""
                title_line = ""
                for line in lines[:6]:
                    if line.startswith("# Source:"):
                        url = line.replace("# Source:", "").strip()
                    elif line.startswith("# Author:"):
                        author = line.replace("# Author:", "").strip()
                    elif line.startswith("# Title:"):
                        title_line = line.replace("# Title:", "").strip()
                snippet = "\n".join(lines[6:])[:500]
                sources_info.append(
                    f"File: {f.name}\n"
                    f"URL: {url}\nAuthor: {author}\nTitle: {title_line}\n"
                    f"Preview: {snippet}\n"
                )
            except Exception:
                pass

    if not sources_info:
        logger.info("No downloaded sources for %s — skipping regeneration", topic_slug)
        return False

    images_text = "(none)"
    images_json = topic_dir / "images" / "images.json"
    if images_json.exists():
        try:
            imgs = json.loads(images_json.read_text())
            img_lines = []
            for img in imgs[:10]:
                img_lines.append(
                    f"- {img.get('filename', '?')}: {img.get('caption', 'no caption')}"
                )
            images_text = "\n".join(img_lines) or "(none)"
        except Exception:
            pass

    from .course_generator import _format_course_profile
    prompt = RESOURCE_PAGE_PROMPT.format(
        topic_slug=topic_slug,
        course_profile=_format_course_profile(course_profile),
        sources_text="\n---\n".join(sources_info),
        images_text=images_text,
    )

    try:
        result = await _call_llm(prompt, max_tokens=4096, temperature=0.1)
        if not result or len(result.strip()) < 50:
            logger.warning("LLM returned empty resource page for %s", topic_slug)
            return False
    except Exception as e:
        logger.warning("Resource page generation failed for %s: %s", topic_slug, e)
        return False

    structural_notes = []
    for line in existing_text.split("\n"):
        if line.startswith("> **[Structural note]"):
            note_lines = [line]
            idx = existing_text.index(line) + len(line) + 1
            remaining = existing_text[idx:]
            for next_line in remaining.split("\n"):
                if next_line.startswith(">"):
                    note_lines.append(next_line)
                else:
                    break
            structural_notes.append("\n".join(note_lines))

    page_content = f"# {topic_slug.replace('-', ' ').title()}\n\n{result.strip()}\n"
    if structural_notes:
        page_content += "\n\n" + "\n\n".join(structural_notes) + "\n"

    _write_pending_item(
        "resource_page",
        topic_slug,
        {
            "page_content": page_content,
            "source_count": len(sources_info),
        },
    )
    logger.info("Staged resource page: %s.md (%d sources)", topic_slug, len(sources_info))
    return True
