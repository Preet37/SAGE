"""
Author registry — single source of truth for author/educator metadata.

Parses ``content/pedagogy-wiki/authors.md`` into an in-memory registry
with O(1) domain-to-author lookup.  Provides author resolution for
``download_source()`` and HTML-based extraction for unknown domains.

Public API:
    load_authors()                -> list[dict]
    resolve_author(url)           -> dict | None
    extract_author_from_html(html)-> str | None
    append_author(entry: dict)    -> None
    read_source_author(path)      -> dict | None
"""

import functools
import json
import logging
import re
from pathlib import Path
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

from ..config import WIKI_DIR as _WIKI_DIR  # noqa: E402 — must follow logger
_AUTHORS_PATH = _WIKI_DIR / "authors.md"

# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

_FIELD_RE = re.compile(r"^-\s+([\w\s]+?):\s*(.+)$")

_FIELD_MAP = {
    "slug": "slug",
    "type": "type",
    "domains": "domains",
    "homepage": "homepage",
    "aliases": "aliases",
    "canonical educator": "canonical_educator",
    "level": "level",
    "best topics": "best_topics",
    "style": "style",
    "pairs with": "pairs_with",
}

_LIST_FIELDS = {"domains", "aliases", "best_topics", "pairs_with"}


def _parse_authors_md(text: str) -> list[dict]:
    """Parse the ``## Block`` format into a list of author dicts."""
    blocks = re.split(r"\n(?=## )", text)
    authors: list[dict] = []

    for block in blocks:
        lines = block.strip().splitlines()
        if not lines:
            continue

        heading = lines[0].lstrip("#").strip()
        if not heading or heading.lower() == "author registry":
            continue

        entry: dict = {"name": heading}
        for line in lines[1:]:
            m = _FIELD_RE.match(line.strip())
            if not m:
                continue
            raw_key = m.group(1).strip().lower()
            raw_val = m.group(2).strip()
            key = _FIELD_MAP.get(raw_key)
            if not key:
                continue
            if key in _LIST_FIELDS:
                entry[key] = [v.strip() for v in raw_val.split(",") if v.strip()]
            elif key == "canonical_educator":
                entry[key] = raw_val.lower() in ("yes", "true", "1")
            else:
                entry[key] = raw_val

        if "slug" not in entry:
            entry["slug"] = re.sub(r"[^a-z0-9]+", "-", heading.lower()).strip("-")

        authors.append(entry)

    return authors


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

_REQUIRED_FIELDS = {"slug"}
_EDUCATOR_REQUIRED = {"level", "best_topics", "style", "pairs_with"}


def validate_registry(authors: list[dict] | None = None) -> list[str]:
    """Check every entry for structural problems.

    Returns a list of human-readable warning strings (empty = all good).
    Useful as a CI check or a quick ``python -m`` sanity test.
    """
    if authors is None:
        authors = _parse_authors_md(_AUTHORS_PATH.read_text(encoding="utf-8"))

    warnings: list[str] = []
    seen_slugs: set[str] = set()
    seen_domains: dict[str, str] = {}

    for i, a in enumerate(authors):
        label = a.get("name", f"entry #{i}")

        for req in _REQUIRED_FIELDS:
            if req not in a:
                warnings.append(f"{label}: missing required field '{req}'")

        slug = a.get("slug", "")
        if slug in seen_slugs:
            warnings.append(f"{label}: duplicate slug '{slug}'")
        seen_slugs.add(slug)

        for domain in a.get("domains", []):
            d = domain.lower().strip()
            if d in seen_domains:
                warnings.append(
                    f"{label}: domain '{d}' already claimed by '{seen_domains[d]}'"
                )
            seen_domains[d] = label

        if a.get("canonical_educator"):
            for field in _EDUCATOR_REQUIRED:
                if field not in a:
                    warnings.append(
                        f"{label}: canonical educator missing '{field}'"
                    )

    return warnings


# ---------------------------------------------------------------------------
# Cached registry + domain index
# ---------------------------------------------------------------------------

@functools.lru_cache(maxsize=1)
def _load_registry() -> tuple[list[dict], dict[str, dict]]:
    """Load and cache the author list + domain->author index."""
    if not _AUTHORS_PATH.exists():
        logger.warning("authors.md not found at %s", _AUTHORS_PATH)
        return [], {}

    authors = _parse_authors_md(_AUTHORS_PATH.read_text(encoding="utf-8"))
    domain_index: dict[str, dict] = {}

    for author in authors:
        for domain in author.get("domains", []):
            d = domain.lower().strip()
            domain_index[d] = author

    return authors, domain_index


def invalidate_cache() -> None:
    """Clear the cached registry (call after appending authors)."""
    _load_registry.cache_clear()
    get_name_index.cache_clear()


def load_authors() -> list[dict]:
    """Return the full list of author entries."""
    authors, _ = _load_registry()
    return authors


def get_author_by_slug(slug: str) -> dict | None:
    """O(n) slug lookup — fine for the ~40-entry registry."""
    for a in load_authors():
        if a.get("slug") == slug:
            return a
    return None


@functools.lru_cache(maxsize=1)
def get_name_index() -> dict[str, str]:
    """Build a lowercase-name/alias → canonical name index.

    Used for text-based mention matching (e.g. scanning lesson content
    for educator names). Returns ``{"karpathy": "Andrej Karpathy", ...}``.
    """
    index: dict[str, str] = {}
    for author in load_authors():
        name = author.get("name", "")
        if not name:
            continue
        index[name.lower()] = name
        slug = author.get("slug", "")
        if slug:
            index[slug] = name
        for alias in author.get("aliases", []):
            index[alias.lower()] = name
    return index


# ---------------------------------------------------------------------------
# Domain-based resolution
# ---------------------------------------------------------------------------

def _extract_domain_key(url: str) -> tuple[str, str]:
    """Return (bare_domain, path_prefixed_domain) for index lookup.

    For ``https://github.com/karpathy/nanoGPT`` returns:
        bare = "github.com"
        prefixed = "github.com/karpathy"
    """
    parsed = urlparse(url)
    bare = parsed.netloc.lower().replace("www.", "")
    first_seg = parsed.path.strip("/").split("/")[0].lower() if parsed.path.strip("/") else ""
    prefixed = f"{bare}/{first_seg}" if first_seg else bare
    return bare, prefixed


def resolve_author(url: str) -> dict | None:
    """Resolve a URL to its author entry via domain index.

    Tries path-prefixed match first (github.com/karpathy),
    then bare domain (karpathy.github.io).
    """
    _, domain_index = _load_registry()
    bare, prefixed = _extract_domain_key(url)

    if prefixed in domain_index:
        return domain_index[prefixed]
    if bare in domain_index:
        return domain_index[bare]
    return None


# ---------------------------------------------------------------------------
# HTML-based author extraction (for unknown domains)
# ---------------------------------------------------------------------------

_META_AUTHOR_RE = re.compile(
    r'<meta\s[^>]*name=["\']author["\']\s[^>]*content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_META_AUTHOR_REV_RE = re.compile(
    r'<meta\s[^>]*content=["\']([^"\']+)["\']\s[^>]*name=["\']author["\']',
    re.IGNORECASE,
)
_OG_AUTHOR_RE = re.compile(
    r'<meta\s[^>]*property=["\'](?:og:)?article:author["\']\s[^>]*content=["\']([^"\']+)["\']',
    re.IGNORECASE,
)
_JSONLD_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.DOTALL | re.IGNORECASE,
)
_BYLINE_RE = re.compile(
    r'class=["\'][^"\']*(?:byline|author|writer)[^"\']*["\'][^>]*>([^<]{2,80})<',
    re.IGNORECASE,
)


def _clean_author_name(raw: str) -> str | None:
    """Normalize and validate an extracted author string."""
    name = raw.strip().strip("/").strip()
    if not name or len(name) < 2 or len(name) > 120:
        return None
    if name.startswith("http") or "@" in name:
        return None
    noise = {"admin", "editor", "staff", "author", "unknown", "anonymous", "guest"}
    if name.lower() in noise:
        return None
    return name


def extract_author_from_html(html: str) -> str | None:
    """Extract author name from HTML meta tags / JSON-LD / byline patterns.

    Returns the cleaned author name string, or None if not found.
    No LLM call — deterministic and free.
    """
    # 1. <meta name="author" content="...">
    for pattern in (_META_AUTHOR_RE, _META_AUTHOR_REV_RE):
        m = pattern.search(html[:10_000])
        if m:
            name = _clean_author_name(m.group(1))
            if name:
                return name

    # 2. og:article:author
    m = _OG_AUTHOR_RE.search(html[:10_000])
    if m:
        name = _clean_author_name(m.group(1))
        if name:
            return name

    # 3. JSON-LD (Schema.org)
    for m in _JSONLD_RE.finditer(html[:50_000]):
        try:
            data = json.loads(m.group(1))
            items = data if isinstance(data, list) else [data]
            for item in items:
                author = item.get("author")
                if isinstance(author, dict):
                    author = author.get("name")
                elif isinstance(author, list):
                    names = [
                        a.get("name") if isinstance(a, dict) else str(a)
                        for a in author
                    ]
                    author = ", ".join(n for n in names if n)
                if author:
                    name = _clean_author_name(str(author))
                    if name:
                        return name
        except (json.JSONDecodeError, AttributeError):
            continue

    # 4. Byline class patterns
    m = _BYLINE_RE.search(html[:30_000])
    if m:
        name = _clean_author_name(m.group(1))
        if name:
            return name

    return None


# ---------------------------------------------------------------------------
# Paper author extraction (arXiv, ACL, etc.)
# ---------------------------------------------------------------------------

_ARXIV_ID_RE = re.compile(r"(?:arxiv\.org|ar5iv\.labs\.arxiv\.org)/(?:abs|html|pdf)/(\d{4}\.\d{4,5})")

_VENUE_SLUGS = frozenset({"arxiv", "acl-anthology", "jmlr", "neurips"})


def is_venue(slug: str) -> bool:
    """Return True if this author slug represents a publication venue, not a person."""
    return slug in _VENUE_SLUGS


def parse_arxiv_id(url: str) -> str | None:
    """Extract arXiv paper ID from a URL.

    Handles arxiv.org/abs/..., arxiv.org/html/..., arxiv.org/pdf/...,
    and ar5iv.labs.arxiv.org/html/... URLs. Strips version suffixes.
    """
    m = _ARXIV_ID_RE.search(url)
    if not m:
        return None
    return re.sub(r"v\d+$", "", m.group(1))


async def extract_arxiv_authors(arxiv_id: str) -> list[str]:
    """Fetch full author list from the arXiv API (free, no auth needed).

    Returns a list of author name strings, e.g.
    ``["Ashish Vaswani", "Noam Shazeer", ...]``.
    """
    import xml.etree.ElementTree as ET

    import httpx

    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    async with httpx.AsyncClient(timeout=30.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    root = ET.fromstring(resp.text)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    authors = []
    for el in root.findall(".//atom:entry/atom:author/atom:name", ns):
        if el.text and el.text.strip():
            authors.append(el.text.strip())
    return authors


def format_paper_authors(authors: list[str]) -> str:
    """Format an author list for the ``# Author:`` header.

    Single author: "Vaswani"
    Two authors: "Vaswani and Shazeer"
    Three or more: "Vaswani et al."
    """
    if not authors:
        return ""
    if len(authors) == 1:
        return authors[0]
    if len(authors) == 2:
        return f"{authors[0]} and {authors[1]}"
    return f"{authors[0]} et al."


# ---------------------------------------------------------------------------
# Append new authors to authors.md
# ---------------------------------------------------------------------------

def append_author(entry: dict) -> None:
    """Append a new author block to authors.md and invalidate cache.

    ``entry`` must have at least ``name`` and ``slug``.
    """
    name = entry["name"]
    slug = entry["slug"]

    existing_slugs = {a.get("slug") for a in load_authors()}
    if slug in existing_slugs:
        logger.debug("Author %s already in registry, skipping append", slug)
        return

    lines = [f"\n## {name}"]
    lines.append(f"- Slug: {slug}")
    if entry.get("type"):
        lines.append(f"- Type: {entry['type']}")
    if entry.get("domains"):
        domains = entry["domains"] if isinstance(entry["domains"], list) else [entry["domains"]]
        lines.append(f"- Domains: {', '.join(domains)}")
    if entry.get("homepage"):
        lines.append(f"- Homepage: {entry['homepage']}")
    if entry.get("aliases"):
        aliases = entry["aliases"] if isinstance(entry["aliases"], list) else [entry["aliases"]]
        lines.append(f"- Aliases: {', '.join(aliases)}")

    block = "\n".join(lines) + "\n"
    with open(_AUTHORS_PATH, "a", encoding="utf-8") as f:
        f.write(block)

    invalidate_cache()
    logger.info("Appended new author to registry: %s (%s)", name, slug)


# ---------------------------------------------------------------------------
# Read author from source .md header
# ---------------------------------------------------------------------------

_HEADER_AUTHOR_RE = re.compile(r"^#\s*Author:\s*(.+)$", re.MULTILINE)
_HEADER_SLUG_RE = re.compile(r"^#\s*Author Slug:\s*(.+)$", re.MULTILINE)


def read_source_author(path: str | Path) -> dict | None:
    """Parse ``# Author:`` / ``# Author Slug:`` from a source .md header.

    Returns ``{"name": ..., "slug": ...}`` or None if no author header found.
    Only reads the first 500 chars (the header area).
    """
    p = Path(path)
    if not p.exists():
        return None
    head = p.read_text(encoding="utf-8")[:500]
    m_name = _HEADER_AUTHOR_RE.search(head)
    m_slug = _HEADER_SLUG_RE.search(head)
    if m_name:
        return {
            "name": m_name.group(1).strip(),
            "slug": m_slug.group(1).strip() if m_slug else None,
        }
    return None


# ---------------------------------------------------------------------------
# CLI: python -m app.services.wiki_authors
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    authors = load_authors()
    warnings = validate_registry(authors)

    educators = [a for a in authors if a.get("canonical_educator")]
    others = [a for a in authors if not a.get("canonical_educator")]

    _, domain_index = _load_registry()

    print(f"Authors: {len(authors)} ({len(educators)} canonical educators, {len(others)} others)")
    print(f"Domain index: {len(domain_index)} domains mapped")

    if warnings:
        print(f"\n⚠ {len(warnings)} validation warning(s):")
        for w in warnings:
            print(f"  - {w}")
    else:
        print("\n✓ Registry is clean — no structural issues found.")
