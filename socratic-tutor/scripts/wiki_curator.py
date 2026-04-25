#!/usr/bin/env python3
"""
Wiki Curator — audit and fix data quality in pedagogy wiki source files.

Parses content/pedagogy-wiki/resources/by-topic/*.md, runs quality checks,
optionally auto-fixes issues, and produces a markdown report.

Usage:
    python scripts/wiki_curator.py                          # audit only
    python scripts/wiki_curator.py --fix                    # audit + auto-fix
    python scripts/wiki_curator.py --fix --rebuild          # fix + regenerate wiki
    python scripts/wiki_curator.py --validate-links         # check URLs resolve & titles match
    python scripts/wiki_curator.py --topic attention-mechanism  # single topic
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
_CONTENT = Path(os.environ.get("CONTENT_DIR", str(REPO_ROOT / "content"))).resolve()
SOURCE_DIR = _CONTENT / "pedagogy-wiki" / "resources" / "by-topic"
REPORT_PATH = REPO_ROOT / "scripts" / "wiki_curation_report.md"
LINK_CACHE_PATH = REPO_ROOT / "scripts" / ".link_validation_cache.json"
CACHE_TTL_DAYS = 7

# ---------------------------------------------------------------------------
# Known URL map — manually verified links for entries missing URLs/youtube_ids.
# Keys use (educator_substring, title_substring) for fuzzy matching.
# ---------------------------------------------------------------------------
KNOWN_URLS: dict[tuple[str, str], dict[str, str]] = {
    ("Jay Alammar", "Illustrated Transformer"): {
        "url": "https://jalammar.github.io/illustrated-transformer/",
    },
    ("Lilian Weng", "Prompt Engineering"): {
        "url": "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
    },
    ("Andrej Karpathy", "GPT Tokenizer"): {
        "youtube_id": "zduSFxRajkE",
    },
    ("LangChain", "LangGraph"): {
        "url": "https://blog.langchain.dev/langgraph-multi-agent-workflows",
    },
    ("Yannic Kilcher", "Switch Transformer"): {
        "youtube_id": "ccBMRryxGog",
    },
    ("Two Minute Papers", "Rubik"): {
        "url": "https://openai.com/research/solving-rubiks-cube",
    },
    ("MIT OpenCourseWare", "Underactuated Robotics"): {
        "url": "https://ocw.mit.edu/courses/6-832-underactuated-robotics-spring-2009/",
    },
    ("Stanford HAI", "AI Agents"): {
        "youtube_id": "kJLiOGle3Lw",
    },
    ("Yannic Kilcher", "MMLU"): {
        "url": "https://arxiv.org/abs/2009.03300",
    },
    ("Yannic Kilcher", "Domain Adaptation"): {
        "url": "https://arxiv.org/abs/2010.03978",
    },
    ("Karpathy", "Multimodal Learning"): {
        "url": "https://cs231n.stanford.edu/",
    },
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class Entry:
    """A single resource within a topic section."""
    educator: str
    title: str
    section: str
    url: str | None = None
    youtube_id: str | None = None
    has_why: bool = False
    level: str | None = None
    line_number: int = 0


@dataclass
class Issue:
    severity: str  # "error", "warning", "info"
    check: str
    message: str
    line: int = 0
    auto_fixed: bool = False


@dataclass
class TopicAudit:
    slug: str
    entries: list[Entry] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)
    fixes_applied: int = 0


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------
ENTRY_PAT = re.compile(
    r'^-\s+\*\*(.+?)\*\*\s+\u2014\s+[\u201c""](.+?)[\u201d""]',
    re.MULTILINE,
)
URL_PAT = re.compile(r"^-\s+(?:url|URL):\s+(https?://\S+)", re.MULTILINE)
YT_PAT = re.compile(r"^-\s+youtube_id:\s+(\S+)", re.MULTILINE)
YT_NONE_PAT = re.compile(r"^-\s+youtube_id:\s+None\b", re.MULTILINE)
WHY_PAT = re.compile(r"^-\s+Why:", re.MULTILINE)
LEVEL_PAT = re.compile(r"^-\s+Level:\s+(.+)", re.MULTILINE | re.IGNORECASE)
SECTION_PAT = re.compile(r"^##\s+(.+)", re.MULTILINE)


def parse_entries(text: str) -> list[Entry]:
    """Parse all resource entries from a topic source file."""
    sections = SECTION_PAT.split(text)
    entries: list[Entry] = []

    i = 1
    while i < len(sections):
        section_name = sections[i].strip()
        section_body = sections[i + 1] if i + 1 < len(sections) else ""
        i += 2

        if section_name.lower().startswith(("last verified", "coverage", "cross-validation")):
            continue

        for m in ENTRY_PAT.finditer(section_body):
            educator = m.group(1).strip()
            title = m.group(2).strip()

            next_entry = ENTRY_PAT.search(section_body, m.end())
            block = section_body[m.end():next_entry.start() if next_entry else len(section_body)]

            url_m = URL_PAT.search(block)
            yt_m = YT_PAT.search(block)
            yt_none = YT_NONE_PAT.search(block)
            why_m = WHY_PAT.search(block)
            level_m = LEVEL_PAT.search(block)

            yt_id = None
            if yt_m and not yt_none:
                raw_id = yt_m.group(1)
                if not raw_id.startswith("None"):
                    yt_id = raw_id.rstrip("`").strip('"').strip("'")

            line_num = text[:m.start() + section_body_offset(text, section_name)].count("\n") + 1

            entries.append(Entry(
                educator=educator,
                title=title,
                section=section_name,
                url=url_m.group(1) if url_m else None,
                youtube_id=yt_id,
                has_why=bool(why_m),
                level=level_m.group(1).strip() if level_m else None,
                line_number=line_num,
            ))

    return entries


def section_body_offset(text: str, section_name: str) -> int:
    """Find byte offset where a section starts in the full text."""
    pat = re.compile(rf"^##\s+{re.escape(section_name)}", re.MULTILINE)
    m = pat.search(text)
    return m.start() if m else 0


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------
def check_missing_links(entries: list[Entry]) -> list[Issue]:
    issues = []
    for e in entries:
        if not e.url and not e.youtube_id:
            issues.append(Issue(
                severity="error",
                check="missing_link",
                message=f"No URL or youtube_id: {e.educator} — \"{e.title}\" [{e.section}]",
                line=e.line_number,
            ))
    return issues


def check_youtube_none(text: str) -> list[Issue]:
    issues = []
    for m in YT_NONE_PAT.finditer(text):
        line_num = text[:m.start()].count("\n") + 1
        issues.append(Issue(
            severity="warning",
            check="youtube_none",
            message=f"Placeholder 'youtube_id: None identified' at line {line_num}",
            line=line_num,
        ))
    return issues


def check_url_casing(text: str) -> list[Issue]:
    issues = []
    for m in re.finditer(r"^-\s+URL:\s+", text, re.MULTILINE):
        line_num = text[:m.start()].count("\n") + 1
        issues.append(Issue(
            severity="info",
            check="url_casing",
            message=f"Uppercase 'URL:' should be 'url:' at line {line_num}",
            line=line_num,
        ))
    return issues


def check_level_casing(entries: list[Entry]) -> list[Issue]:
    issues = []
    for e in entries:
        if e.level and e.level != e.level.lower():
            issues.append(Issue(
                severity="info",
                check="level_casing",
                message=f"Level '{e.level}' not lowercase: {e.educator} [{e.section}]",
                line=e.line_number,
            ))
    return issues


def check_verify_flags(text: str) -> list[Issue]:
    issues = []
    for m in re.finditer(r"\[(?:NOT VERIFIED|VERIFY\b[^\]]*)\]", text):
        line_num = text[:m.start()].count("\n") + 1
        issues.append(Issue(
            severity="warning",
            check="verify_flag",
            message=f"Verification flag: {m.group(0)[:60]}",
            line=line_num,
        ))
    return issues


def check_missing_why(entries: list[Entry]) -> list[Issue]:
    issues = []
    for e in entries:
        if not e.has_why:
            issues.append(Issue(
                severity="info",
                check="missing_why",
                message=f"No 'Why:' field: {e.educator} — \"{e.title}\" [{e.section}]",
                line=e.line_number,
            ))
    return issues


def check_duplicate_urls(entries: list[Entry]) -> list[Issue]:
    issues = []
    seen: dict[str, Entry] = {}
    for e in entries:
        link = e.url or (f"youtube:{e.youtube_id}" if e.youtube_id else None)
        if not link:
            continue
        if link in seen:
            prev = seen[link]
            issues.append(Issue(
                severity="warning",
                check="duplicate_url",
                message=f"Duplicate link '{link}' in [{e.section}] and [{prev.section}]",
                line=e.line_number,
            ))
        else:
            seen[link] = e
    return issues


# ---------------------------------------------------------------------------
# Auto-fix: inject missing URLs from the known map
# ---------------------------------------------------------------------------
def lookup_known_url(educator: str, title: str) -> dict[str, str] | None:
    """Fuzzy match against KNOWN_URLS using substring matching."""
    for (edu_key, title_key), link_data in KNOWN_URLS.items():
        if edu_key.lower() in educator.lower() and title_key.lower() in title.lower():
            return link_data if link_data else None
    return None


def fix_missing_links(text: str, entries: list[Entry], issues: list[Issue]) -> tuple[str, int]:
    """Inject url/youtube_id lines for entries that can be resolved from KNOWN_URLS."""
    fixes = 0
    for issue in issues:
        if issue.check != "missing_link":
            continue

        entry = next(
            (e for e in entries if issue.message.endswith(f"[{e.section}]")
             and e.educator in issue.message and not e.url and not e.youtube_id),
            None,
        )
        if not entry:
            continue

        link_data = lookup_known_url(entry.educator, entry.title)
        if not link_data:
            continue

        title_pattern = re.escape(entry.title[:40])
        educator_pattern = re.escape(entry.educator[:30])
        block_re = re.compile(
            rf"(^-\s+\*\*{educator_pattern}.*?{title_pattern}.*$)",
            re.MULTILINE,
        )
        m = block_re.search(text)
        if not m:
            continue

        insert_after = m.end()
        if "youtube_id" in link_data:
            new_line = f"\n- youtube_id: {link_data['youtube_id']}"
        else:
            new_line = f"\n- url: {link_data['url']}"

        text = text[:insert_after] + new_line + text[insert_after:]
        issue.auto_fixed = True
        entry.url = link_data.get("url")
        entry.youtube_id = link_data.get("youtube_id")
        fixes += 1

    return text, fixes


def fix_youtube_none(text: str, issues: list[Issue]) -> tuple[str, int]:
    """Strip 'youtube_id: None identified' placeholder lines."""
    original = text
    text = re.sub(r"^-\s+youtube_id:\s+None\b.*\n?", "", text, flags=re.MULTILINE)
    fixes = 0
    if text != original:
        fixes = sum(1 for i in issues if i.check == "youtube_none")
        for i in issues:
            if i.check == "youtube_none":
                i.auto_fixed = True
    return text, fixes


_YT_JUNK_RE = re.compile(
    r"^(-\s+youtube_id:\s+)"          # prefix we keep
    r"[\*`\s]*"                        # leading junk: bold markers, backticks, spaces
    r"([A-Za-z0-9_-]{11})"            # the real 11-char ID
    r"[\*`\s]*"                        # trailing junk
    r"(\s*\[.*\])?"                    # optional [NOT VERIFIED] / [VERIFY] suffix
    r"\s*$",
    re.MULTILINE,
)

_YT_PURE_JUNK_RE = re.compile(
    r"^-\s+youtube_id:\s+"
    r"(?:\[NOT\b|\[VERIFY\b|\*\*None).*\n?",
    re.MULTILINE,
)


def fix_malformed_youtube_ids(text: str) -> tuple[str, int]:
    """Clean backticks, bold markers, and verification flags from youtube_id values."""
    fixes = 0

    def _clean_match(m: re.Match) -> str:
        nonlocal fixes
        prefix, video_id, _suffix = m.group(1), m.group(2), m.group(3)
        original_line = m.group(0)
        cleaned = f"{prefix}{video_id}"
        if cleaned.rstrip() != original_line.rstrip():
            fixes += 1
        return cleaned

    text = _YT_JUNK_RE.sub(_clean_match, text)

    for m in _YT_PURE_JUNK_RE.finditer(text):
        fixes += 1
    text = _YT_PURE_JUNK_RE.sub("", text)

    return text, fixes


# ---------------------------------------------------------------------------
# Dead URL replacements — maps known-dead URLs to their correct current URLs.
# Entries where the value is "" will have the line removed entirely.
# ---------------------------------------------------------------------------
DEAD_URL_REPLACEMENTS: dict[str, str] = {
    # Lilian Weng: wrong year (2022 → 2023)
    "https://lilianweng.github.io/posts/2022-01-27-the-transformer-family-v2/":
        "https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/",
    # Lilian Weng: hallucinated URLs → closest real posts
    "https://lilianweng.github.io/posts/2023-01-10-moe/":
        "https://lilianweng.github.io/posts/2021-09-25-train-large/",
    "https://lilianweng.github.io/posts/2023-09-06-lmm/":
        "https://lilianweng.github.io/posts/2022-06-09-vlm/",
    "https://lilianweng.github.io/posts/2023-03-15-constitutional-ai/":
        "https://arxiv.org/abs/2212.08073",
    "https://lilianweng.github.io/posts/2023-01-17-rlhf/":
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2021-01-02-rl/":
        "https://lilianweng.github.io/posts/2024-11-28-reward-hacking/",
    "https://lilianweng.github.io/posts/2021-12-31-nerf/":
        "https://arxiv.org/abs/2003.08934",
    "https://lilianweng.github.io/posts/2020-10-29-dlk/":
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "https://lilianweng.github.io/posts/2019-10-14-robot-dexterous-hand/":
        "https://lilianweng.github.io/posts/2022-06-09-vlm/",
    # Neo4j pages moved
    "https://neo4j.com/developer/kb/what-is-a-knowledge-graph/":
        "https://neo4j.com/blog/knowledge-graph/what-is-knowledge-graph",
    "https://neo4j.com/developer/semantic-web/":
        "https://neo4j.com/use-cases/knowledge-graph",
    # Simon Willison: URL changed
    "https://simonwillison.net/2023/May/2/prompt-injection/":
        "https://simonwillison.net/2023/Nov/27/prompt-injection-explained/",
    # NVIDIA blog moved
    "https://developer.nvidia.com/blog/mixture-of-experts-explained/":
        "https://developer.nvidia.com/blog/applying-mixture-of-experts-in-llm-architectures/",
    # HuggingFace speculative decoding blog moved
    "https://huggingface.co/blog/speculative-decoding":
        "https://huggingface.co/docs/transformers/assisted_decoding",
    # OpenAI GPT-4o URL changed
    "https://openai.com/index/gpt-4o/":
        "https://openai.com/blog/hello-gpt-4o",
    # Chip Huyen blog URL changed
    "https://www.cs.stanford.edu/~chenhuye/blog/":
        "https://huyenchip.com/blog/",
    # LangChain tutorial moved
    "https://langchain-ai.github.io/langgraph/tutorials/multi_agent/multi_agent_collaboration/":
        "https://langchain-ai.github.io/langgraph/tutorials/",
}


def fix_dead_urls(text: str) -> tuple[str, int]:
    """Replace known-dead URLs with their correct current URLs."""
    fixes = 0
    for old_url, new_url in DEAD_URL_REPLACEMENTS.items():
        if old_url in text:
            if new_url:
                text = text.replace(old_url, new_url)
            else:
                text = re.sub(
                    rf"^-\s+(?:url|URL):\s+{re.escape(old_url)}\s*\n?",
                    "", text, flags=re.MULTILINE,
                )
            fixes += 1
    return text, fixes


def fix_url_casing(text: str, issues: list[Issue]) -> tuple[str, int]:
    """Normalize uppercase URL: to url:."""
    original = text
    text = re.sub(r"^(-\s+)URL:", r"\1url:", text, flags=re.MULTILINE)
    fixes = 0
    if text != original:
        fixes = sum(1 for i in issues if i.check == "url_casing")
        for i in issues:
            if i.check == "url_casing":
                i.auto_fixed = True
    return text, fixes


# ---------------------------------------------------------------------------
# Link validation — fetch page/video title and compare to entry title
# ---------------------------------------------------------------------------
_TITLE_TAG_RE = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
_USER_AGENT = "Mozilla/5.0 (compatible; WikiCurator/1.0)"


def _load_link_cache() -> dict:
    if LINK_CACHE_PATH.exists():
        try:
            return json.loads(LINK_CACHE_PATH.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_link_cache(cache: dict) -> None:
    LINK_CACHE_PATH.write_text(json.dumps(cache, indent=2), encoding="utf-8")


def _cache_is_fresh(entry: dict) -> bool:
    ts = entry.get("checked_at", "")
    if not ts:
        return False
    try:
        checked = datetime.fromisoformat(ts)
        return (datetime.now() - checked).days < CACHE_TTL_DAYS
    except ValueError:
        return False


def _fetch_page_title(url: str) -> tuple[str, str | None]:
    """Fetch a URL and extract the <title> tag.

    Returns (status, title_or_None).
    Status is one of: "ok", "dead", "error".
    """
    req = urllib.request.Request(url, method="GET", headers={
        "User-Agent": _USER_AGENT,
        "Accept": "text/html",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "html" not in content_type and "text" not in content_type:
                return "ok", None
            body = resp.read(32768).decode("utf-8", errors="replace")
            m = _TITLE_TAG_RE.search(body)
            if m:
                title = m.group(1).strip()
                title = re.sub(r"\s+", " ", title)
                return "ok", title
            return "ok", None
    except urllib.error.HTTPError as e:
        if e.code in (404, 410, 451):
            return "dead", None
        return "error", None
    except (urllib.error.URLError, OSError, TimeoutError):
        return "error", None


def _validate_youtube(video_id: str) -> tuple[str, str | None]:
    """Check a YouTube video via oEmbed. Returns (status, video_title)."""
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
    req = urllib.request.Request(url, headers={"User-Agent": _USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return "ok", data.get("title")
    except urllib.error.HTTPError:
        return "dead", None
    except (urllib.error.URLError, OSError, TimeoutError, json.JSONDecodeError):
        return "error", None


def _titles_match(entry_title: str, page_title: str) -> bool:
    """Check if the page title is reasonably related to the entry title."""
    if not page_title:
        return True

    e = entry_title.lower()
    p = page_title.lower()

    if e in p or p in e:
        return True

    e_words = set(re.findall(r"\w{4,}", e))
    p_words = set(re.findall(r"\w{4,}", p))
    if not e_words:
        return True
    overlap = len(e_words & p_words) / len(e_words)
    return overlap >= 0.3


def validate_links(entries: list[Entry], cache: dict) -> list[Issue]:
    """Validate all URLs and YouTube IDs, returning issues for broken/mismatched links."""
    issues: list[Issue] = []
    checked = 0

    for e in entries:
        link_key = e.url or (f"youtube:{e.youtube_id}" if e.youtube_id else None)
        if not link_key:
            continue

        if link_key in cache and _cache_is_fresh(cache[link_key]):
            cached = cache[link_key]
            status = cached["status"]
            page_title = cached.get("page_title")
        else:
            if checked > 0:
                time.sleep(0.5)

            if e.youtube_id and not e.url:
                status, page_title = _validate_youtube(e.youtube_id)
            else:
                status, page_title = _fetch_page_title(e.url)

            cache[link_key] = {
                "status": status,
                "page_title": page_title,
                "checked_at": datetime.now().isoformat(),
            }
            checked += 1

        if status == "dead":
            issues.append(Issue(
                severity="error",
                check="dead_link",
                message=f"Dead link ({link_key}): {e.educator} — \"{e.title}\"",
                line=e.line_number,
            ))
        elif status == "error":
            issues.append(Issue(
                severity="warning",
                check="link_unreachable",
                message=f"Could not reach ({link_key}): {e.educator} — \"{e.title}\"",
                line=e.line_number,
            ))
        elif page_title and not _titles_match(e.title, page_title):
            issues.append(Issue(
                severity="warning",
                check="title_mismatch",
                message=(
                    f"Title mismatch: entry=\"{e.title[:50]}\" vs "
                    f"page=\"{page_title[:50]}\" ({link_key})"
                ),
                line=e.line_number,
            ))

    return issues


# ---------------------------------------------------------------------------
# Audit orchestration
# ---------------------------------------------------------------------------
def audit_topic(
    path: Path,
    fix: bool = False,
    validate: bool = False,
    link_cache: dict | None = None,
) -> TopicAudit:
    """Run all checks on a single topic file, optionally applying fixes."""
    text = path.read_text(encoding="utf-8")
    slug = path.stem
    entries = parse_entries(text)

    all_issues: list[Issue] = []
    all_issues.extend(check_missing_links(entries))
    all_issues.extend(check_youtube_none(text))
    all_issues.extend(check_url_casing(text))
    all_issues.extend(check_level_casing(entries))
    all_issues.extend(check_verify_flags(text))
    all_issues.extend(check_missing_why(entries))
    all_issues.extend(check_duplicate_urls(entries))

    total_fixes = 0
    if fix:
        text, n = fix_missing_links(text, entries, all_issues)
        total_fixes += n
        text, n = fix_youtube_none(text, all_issues)
        total_fixes += n
        text, n = fix_url_casing(text, all_issues)
        total_fixes += n
        text, n = fix_malformed_youtube_ids(text)
        total_fixes += n
        text, n = fix_dead_urls(text)
        total_fixes += n

        if total_fixes > 0:
            text = re.sub(r"\n{3,}", "\n\n", text)
            path.write_text(text, encoding="utf-8")

    if validate and link_cache is not None:
        all_issues.extend(validate_links(entries, link_cache))

    return TopicAudit(slug=slug, entries=entries, issues=all_issues, fixes_applied=total_fixes)


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def generate_report(audits: list[TopicAudit]) -> str:
    """Produce a markdown curation report."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_topics = len(audits)
    total_entries = sum(len(a.entries) for a in audits)
    total_issues = sum(len(a.issues) for a in audits)
    total_fixed = sum(a.fixes_applied for a in audits)
    unfixed = sum(1 for a in audits for i in a.issues if not i.auto_fixed)

    lines = [
        f"# Wiki Curation Report",
        f"",
        f"**Generated:** {now}",
        f"",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Topics scanned | {total_topics} |",
        f"| Resource entries | {total_entries} |",
        f"| Issues found | {total_issues} |",
        f"| Auto-fixed | {total_fixed} |",
        f"| Needs review | {unfixed} |",
        f"",
    ]

    by_check: dict[str, int] = {}
    for a in audits:
        for i in a.issues:
            by_check[i.check] = by_check.get(i.check, 0) + 1

    if by_check:
        lines.append("## Issues by type\n")
        lines.append("| Check | Count |")
        lines.append("|-------|-------|")
        for check, count in sorted(by_check.items(), key=lambda x: -x[1]):
            lines.append(f"| {check} | {count} |")
        lines.append("")

    topics_with_issues = [a for a in audits if a.issues]
    if topics_with_issues:
        lines.append("## Details by topic\n")
        for a in sorted(topics_with_issues, key=lambda x: -len(x.issues)):
            fixed_count = sum(1 for i in a.issues if i.auto_fixed)
            lines.append(f"### {a.slug} ({len(a.issues)} issues, {fixed_count} fixed)\n")
            for i in a.issues:
                status = "FIXED" if i.auto_fixed else i.severity.upper()
                lines.append(f"- [{status}] `{i.check}`: {i.message}")
            lines.append("")

    clean = [a for a in audits if not a.issues]
    if clean:
        lines.append(f"## Clean topics ({len(clean)})\n")
        lines.append(", ".join(a.slug for a in clean))
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> int:
    parser = argparse.ArgumentParser(description="Wiki source quality curator")
    parser.add_argument("--fix", action="store_true", help="Auto-fix issues in source files")
    parser.add_argument("--rebuild", action="store_true", help="Run topic_to_quartz.py after fixing")
    parser.add_argument("--validate-links", action="store_true",
                        help="Check URLs resolve and page titles match entries")
    parser.add_argument("--topic", type=str, help="Audit a single topic slug")
    args = parser.parse_args()

    if not SOURCE_DIR.exists():
        print(f"ERROR: {SOURCE_DIR} not found", file=sys.stderr)
        return 1

    if args.topic:
        paths = [SOURCE_DIR / f"{args.topic}.md"]
        if not paths[0].exists():
            print(f"ERROR: Topic not found: {args.topic}", file=sys.stderr)
            return 1
    else:
        paths = sorted(SOURCE_DIR.glob("*.md"))

    mode_parts = []
    if args.fix:
        mode_parts.append("fix")
    if args.validate_links:
        mode_parts.append("validate")
    mode_label = " + ".join(mode_parts) if mode_parts else "audit only"
    print(f"Scanning {len(paths)} topic files ({mode_label})")

    link_cache = _load_link_cache() if args.validate_links else None

    audits: list[TopicAudit] = []
    for path in paths:
        audit = audit_topic(
            path, fix=args.fix,
            validate=args.validate_links, link_cache=link_cache,
        )
        audits.append(audit)

        status = ""
        if audit.fixes_applied:
            status = f"  fixed={audit.fixes_applied}"
        if audit.issues:
            unfixed = sum(1 for i in audit.issues if not i.auto_fixed)
            status += f"  remaining={unfixed}" if unfixed else ""

        if audit.issues:
            print(f"  {audit.slug}: {len(audit.issues)} issues{status}")

    if link_cache is not None:
        _save_link_cache(link_cache)

    total_issues = sum(len(a.issues) for a in audits)
    total_fixed = sum(a.fixes_applied for a in audits)
    clean_count = sum(1 for a in audits if not a.issues)

    print(f"\nSummary: {total_issues} issues, {total_fixed} fixed, "
          f"{clean_count}/{len(audits)} topics clean")

    report = generate_report(audits)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Report: {REPORT_PATH}")

    if args.rebuild and total_fixed > 0:
        print("\nRunning topic_to_quartz.py...")
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "topic_to_quartz.py")],
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            print("ERROR: topic_to_quartz.py failed", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
