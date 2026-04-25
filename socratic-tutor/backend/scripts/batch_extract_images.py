"""
Batch image extraction for existing wiki sources.

Scans all downloaded source .md files, re-fetches HTML, and runs
the tier-1 image pipeline (extract → heuristic filter → LLM annotate
→ download).

Usage:
    cd backend

    # Dry run — show what would be processed, no fetching
    PYTHONUNBUFFERED=1 uv run python scripts/batch_extract_images.py --dry-run

    # First 10 image-rich sources (blogs) as a test batch
    PYTHONUNBUFFERED=1 uv run python scripts/batch_extract_images.py --limit 10

    # All sources
    PYTHONUNBUFFERED=1 uv run python scripts/batch_extract_images.py

    # Only specific topics
    PYTHONUNBUFFERED=1 uv run python scripts/batch_extract_images.py --topics cnns,rnns-lstms

    # Skip sources that already have images extracted
    PYTHONUNBUFFERED=1 uv run python scripts/batch_extract_images.py --skip-existing

    # Rehydrate: download missing image files from images.json metadata
    # (use after cloning the repo — no LLM calls needed)
    PYTHONUNBUFFERED=1 uv run python scripts/batch_extract_images.py --rehydrate
    PYTHONUNBUFFERED=1 uv run python scripts/batch_extract_images.py --rehydrate --topics self-attention
"""

import asyncio
import json
import logging
import os
import re
import sys
import time
from pathlib import Path

logger = logging.getLogger(__name__)

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("TESTING_PIPELINE", "1")

from app.services.wiki_images import (
    process_source_images,
    load_images_json,
    build_global_image_index,
    _guess_author,
)

_WIKI_DIR = Path(os.environ.get("CONTENT_DIR", str(Path(__file__).resolve().parent.parent.parent / "content"))).resolve() / "pedagogy-wiki"
_SOURCES_DIR = _WIKI_DIR / "resources" / "by-topic"

# Domains likely to have educational diagrams worth extracting
_IMAGE_RICH_DOMAINS = {
    "jalammar.github.io",
    "lilianweng.github.io",
    "colah.github.io",
    "d2l.ai",
    "cs231n.github.io",
    "course.fast.ai",
    "huyenchip.com",
    "dellaert.github.io",
    "matthewtancik.com",
    "sebastianraschka.com",
    "magazine.sebastianraschka.com",
    "blog.paperspace.com",
    "distill.pub",
    "arpitbhayani.me",
    "jaykmody.com",
    "machinelearningmastery.com",
    "eugeneyan.com",
    "wandb.ai",
    "ar5iv.labs.arxiv.org",
    "arxiv.org",
    "docs.cleanrl.dev",
    "compneuro.neuromatch.io",
    "outcomeschool.com",
    "codegenes.net",
    "mbrenndoerfer.com",
    "geeksforgeeks.org",
    "apxml.com",
    "huggingface.co",
    "cookbook.openai.com",
    "openai.com",
    "slds.lmu.de",
}


def discover_sources(
    topics: list[str] | None = None,
    image_rich_only: bool = False,
) -> list[dict]:
    """Scan wiki source .md files and return a list of source descriptors.

    Each descriptor: {topic_slug, url, title, file_path, domain}
    """
    sources = []
    topic_dirs = sorted(_SOURCES_DIR.iterdir()) if _SOURCES_DIR.is_dir() else []

    for topic_dir in topic_dirs:
        if not topic_dir.is_dir():
            continue
        topic_slug = topic_dir.name
        if topics and topic_slug not in topics:
            continue

        for md_file in sorted(topic_dir.glob("*.md")):
            if md_file.name in ("curation-report.md",):
                continue

            first_lines = md_file.read_text(errors="ignore").split("\n", 5)[:5]
            url = None
            for line in first_lines:
                if line.startswith("# Source: "):
                    url = line[len("# Source: "):].strip()
                    break

            if not url:
                continue

            from urllib.parse import urlparse
            domain = urlparse(url).hostname or ""

            if image_rich_only and not any(d in domain for d in _IMAGE_RICH_DOMAINS):
                continue

            title_line = ""
            for line in first_lines:
                if not line.startswith("#"):
                    title_line = line.strip()
                    if title_line:
                        break

            sources.append({
                "topic_slug": topic_slug,
                "url": url,
                "title": title_line or md_file.stem,
                "file_path": str(md_file),
                "domain": domain,
            })

    return sources


def _already_processed(topic_slug: str, url: str) -> int:
    """Return count of images already extracted for this source page."""
    existing = load_images_json(topic_slug)
    return sum(1 for e in existing if e.get("source_page") == url)


_html_cache: dict[str, str] = {}


async def fetch_html(url: str) -> str | None:
    """Fetch raw HTML with caching, trafilatura first, browser fallback."""
    if url in _html_cache:
        return _html_cache[url]

    html = await _fetch_trafilatura(url)

    # If trafilatura got very little HTML, try browser for JS-heavy sites
    if not html or len(html) < 2000:
        browser_html = await _fetch_browser(url)
        if browser_html and len(browser_html) > len(html or ""):
            html = browser_html

    if html:
        _html_cache[url] = html
    return html


async def _fetch_trafilatura(url: str) -> str | None:
    try:
        import trafilatura
        return await asyncio.to_thread(trafilatura.fetch_url, url)
    except Exception as e:
        logger.debug("Trafilatura fetch failed for %s: %s", url, e)
        return None


async def _fetch_browser(url: str) -> str | None:
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        return None

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="networkidle", timeout=30000)
            html = await page.content()
            await browser.close()
            return html
    except Exception as e:
        logger.debug("Browser fetch failed for %s: %s", url, e)
        return None


async def process_batch(
    sources: list[dict],
    *,
    skip_existing: bool = True,
    max_concurrent: int = 3,
) -> dict:
    """Process a batch of sources through the tier-1 image pipeline."""
    sem = asyncio.Semaphore(max_concurrent)

    # Build global image index for cross-topic dedup
    print("  Building global image index for dedup...")
    global_index = build_global_image_index()
    print(f"  Index: {len(global_index)} images already on disk\n")

    results = {
        "processed": 0,
        "skipped": 0,
        "fetch_failed": 0,
        "no_images": 0,
        "total_images": 0,
        "total_downloaded": 0,
        "total_copied": 0,
        "errors": [],
        "per_source": [],
    }

    async def _process_one(src: dict) -> dict:
        topic = src["topic_slug"]
        url = src["url"]
        title = src["title"]
        domain = src["domain"]

        if skip_existing:
            count = _already_processed(topic, url)
            if count > 0:
                print(f"  SKIP  {domain[:25]:25s}  {topic:25s}  ({count} images exist)")
                results["skipped"] += 1
                return {"status": "skipped", "existing": count}

        async with sem:
            print(f"  FETCH {domain[:25]:25s}  {topic:25s}  {title[:40]}")
            t0 = time.monotonic()

            html = await fetch_html(url)
            if not html:
                print(f"  FAIL  {domain[:25]:25s}  could not fetch HTML")
                results["fetch_failed"] += 1
                return {"status": "fetch_failed"}

            try:
                result = await process_source_images(
                    topic_slug=topic,
                    page_title=title,
                    page_url=url,
                    raw_html=html,
                    force=False,
                    global_image_index=global_index,
                )
            except Exception as e:
                msg = f"{domain}: {e}"
                print(f"  ERR   {domain[:25]:25s}  {e}")
                results["errors"].append(msg)
                return {"status": "error", "error": str(e)}

            elapsed = time.monotonic() - t0
            kept = result.get("kept", 0)
            downloaded = result.get("downloaded", 0)
            copied = result.get("copied", 0)
            status = result.get("status", "?")

            if downloaded > 0 or copied > 0:
                parts = []
                if downloaded:
                    parts.append(f"{downloaded} new")
                if copied:
                    parts.append(f"{copied} dedup")
                print(f"  DONE  {domain[:25]:25s}  {topic:25s}  "
                      f"{kept} kept, {', '.join(parts)}  ({elapsed:.1f}s)")
                results["total_images"] += kept
                results["total_downloaded"] += downloaded
                results["total_copied"] += copied
            else:
                print(f"  DONE  {domain[:25]:25s}  {topic:25s}  "
                      f"0 images ({status})  ({elapsed:.1f}s)")
                results["no_images"] += 1

            results["processed"] += 1
            result["elapsed"] = round(elapsed, 1)
            result["topic"] = topic
            result["url"] = url
            results["per_source"].append(result)
            return result

    tasks = [_process_one(src) for src in sources]
    await asyncio.gather(*tasks)

    return results


def print_summary(results: dict, sources: list[dict]):
    """Print a summary of the batch run."""
    print(f"\n{'=' * 70}")
    print(f"  BATCH SUMMARY")
    print(f"{'=' * 70}")
    print(f"  Sources scanned:  {len(sources)}")
    print(f"  Processed:        {results['processed']}")
    print(f"  Skipped:          {results['skipped']}")
    print(f"  Fetch failed:     {results['fetch_failed']}")
    print(f"  No images found:  {results['no_images']}")
    print(f"  Total kept:       {results['total_images']}")
    print(f"  Downloaded (new): {results['total_downloaded']}")
    print(f"  Copied (dedup):   {results['total_copied']}")

    if results["errors"]:
        print(f"\n  ERRORS ({len(results['errors'])}):")
        for e in results["errors"]:
            print(f"    - {e[:80]}")

    # Per-topic summary
    topic_counts: dict[str, int] = {}
    for r in results["per_source"]:
        t = r.get("topic", "?")
        topic_counts[t] = topic_counts.get(t, 0) + r.get("downloaded", 0)

    if topic_counts:
        print(f"\n  PER-TOPIC IMAGES:")
        for topic, count in sorted(topic_counts.items()):
            if count > 0:
                print(f"    {topic:30s}  {count} images")

    # Show total disk usage
    total_kb = 0
    for topic_dir in sorted(_SOURCES_DIR.iterdir()):
        if not topic_dir.is_dir():
            continue
        img_dir = topic_dir / "images"
        if img_dir.is_dir():
            for f in img_dir.iterdir():
                if f.suffix.lower() in (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"):
                    total_kb += f.stat().st_size / 1024

    if total_kb > 0:
        print(f"\n  TOTAL DISK: {total_kb / 1024:.1f} MB across all topics")


async def rehydrate(
    topics: list[str] | None = None,
    max_concurrent: int = 5,
) -> None:
    """Download missing image files from images.json metadata.

    No LLM calls — just reads each topic's images.json and fetches
    any image files that don't exist locally. Use after cloning the
    repo or to restore images after a clean.
    """
    import httpx

    print(f"{'=' * 70}")
    print(f"  REHYDRATE: Download images from metadata")
    print(f"{'=' * 70}")

    by_topic = _SOURCES_DIR
    if not by_topic.is_dir():
        print("  No wiki topics found")
        return

    # Collect all missing images
    to_download: list[tuple[Path, str]] = []  # (save_path, source_url)
    already_exist = 0

    for topic_dir in sorted(by_topic.iterdir()):
        if not topic_dir.is_dir():
            continue
        topic_slug = topic_dir.name
        if topics and topic_slug not in topics:
            continue

        json_path = topic_dir / "images" / "images.json"
        if not json_path.exists():
            continue

        try:
            entries = json.loads(json_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue

        img_dir = topic_dir / "images"
        for entry in entries:
            file_path = img_dir / entry["file"]
            if file_path.exists():
                already_exist += 1
            else:
                to_download.append((file_path, entry["source_url"]))

    print(f"  Already on disk: {already_exist}")
    print(f"  Missing files:   {len(to_download)}")

    if not to_download:
        print("  Nothing to download!")
        return

    # Download missing files with concurrency limit
    sem = asyncio.Semaphore(max_concurrent)
    downloaded = 0
    failed = 0

    async def _dl(save_path: Path, url: str):
        nonlocal downloaded, failed
        async with sem:
            try:
                async with httpx.AsyncClient(
                    timeout=30.0, follow_redirects=True,
                ) as client:
                    resp = await client.get(url)
                    resp.raise_for_status()
                    save_path.parent.mkdir(parents=True, exist_ok=True)
                    save_path.write_bytes(resp.content)
                    downloaded += 1
            except Exception as e:
                failed += 1
                logger.debug("Failed to download %s: %s", url, e)

    print(f"  Downloading {len(to_download)} images (concurrency={max_concurrent})...\n")
    t0 = time.monotonic()

    # Show progress by topic
    by_topic_missing: dict[str, int] = {}
    for path, _ in to_download:
        topic = path.parent.parent.name
        by_topic_missing[topic] = by_topic_missing.get(topic, 0) + 1

    for topic, count in sorted(by_topic_missing.items()):
        print(f"    {topic:30s}  {count} files")

    print()
    tasks = [_dl(path, url) for path, url in to_download]
    await asyncio.gather(*tasks)

    elapsed = time.monotonic() - t0
    print(f"  Downloaded: {downloaded}")
    print(f"  Failed:     {failed}")
    print(f"  Time:       {elapsed:.0f}s")


async def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch image extraction for wiki sources")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show sources that would be processed")
    parser.add_argument("--limit", type=int, default=0,
                        help="Process only first N sources (0 = all)")
    parser.add_argument("--topics", type=str, default="",
                        help="Comma-separated topic slugs to process")
    parser.add_argument("--skip-existing", action="store_true", default=True,
                        help="Skip sources with images already extracted (default)")
    parser.add_argument("--no-skip-existing", action="store_true",
                        help="Re-process even if images exist")
    parser.add_argument("--image-rich-only", action="store_true",
                        help="Only process known image-rich domains (blogs)")
    parser.add_argument("--concurrency", type=int, default=3,
                        help="Max concurrent fetches (default 3)")
    parser.add_argument("--rehydrate", action="store_true",
                        help="Download missing image files from images.json (no LLM)")
    args = parser.parse_args()

    topics = [t.strip() for t in args.topics.split(",") if t.strip()] or None

    if args.rehydrate:
        await rehydrate(topics=topics, max_concurrent=args.concurrency)
        return

    skip_existing = not args.no_skip_existing

    print(f"{'=' * 70}")
    print(f"  BATCH IMAGE EXTRACTION")
    print(f"{'=' * 70}")

    sources = discover_sources(topics=topics, image_rich_only=args.image_rich_only)
    print(f"  Found {len(sources)} source files across wiki")

    if args.image_rich_only:
        print(f"  (filtered to image-rich domains only)")

    if args.limit:
        sources = sources[:args.limit]
        print(f"  Limited to first {args.limit} sources")

    if args.dry_run:
        print(f"\n  DRY RUN — would process {len(sources)} sources:\n")
        for src in sources:
            existing = _already_processed(src["topic_slug"], src["url"])
            marker = f" ({existing} images)" if existing else ""
            skip = " [SKIP]" if existing and skip_existing else ""
            print(f"    {src['topic_slug']:30s}  {src['domain']:30s}{marker}{skip}")
        return

    print(f"  Processing {len(sources)} sources (concurrency={args.concurrency})...\n")

    t0 = time.monotonic()
    results = await process_batch(
        sources,
        skip_existing=skip_existing,
        max_concurrent=args.concurrency,
    )
    elapsed = time.monotonic() - t0

    print_summary(results, sources)
    print(f"\n  Total time: {elapsed:.0f}s")


if __name__ == "__main__":
    asyncio.run(main())
