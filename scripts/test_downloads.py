#!/usr/bin/env python3
"""
Targeted download cascade test — exercise every fetch strategy on a
mix of URL types and report what works.

Usage:
    cd backend
    uv run python ../scripts/test_downloads.py                 # run all test URLs
    uv run python ../scripts/test_downloads.py --url "https://arxiv.org/abs/2404.10719"
    uv run python ../scripts/test_downloads.py --failed         # rerun only prior failures
    uv run python ../scripts/test_downloads.py --strategy       # test each strategy individually

What it tests:
    - URL normalization (arxiv PDF/abs → HTML rewrite)
    - trafilatura extraction
    - browser (playwright) extraction
    - search fallback (Perplexity/sonar summary)
    - Full cascade (download_url) end-to-end

Output:
    Console table + scripts/download_test_results.json
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
BACKEND_DIR = REPO_ROOT / "backend"
BACKEND_ENV = BACKEND_DIR / ".env"
SCRIPTS_DIR = Path(__file__).parent
RESULTS_PATH = SCRIPTS_DIR / "download_test_results.json"


def _load_env():
    if BACKEND_ENV.exists():
        for line in BACKEND_ENV.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, _, v = line.partition("=")
                os.environ.setdefault(k.strip(), v.strip())


_load_env()
sys.path.insert(0, str(BACKEND_DIR))

import logging
logging.basicConfig(level=logging.INFO, format="  %(name)s | %(message)s", stream=sys.stdout)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("openai").setLevel(logging.WARNING)
logging.getLogger("trafilatura").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# ── Test URLs covering different failure modes ──────────────────────
TEST_URLS = [
    # arxiv abstract page (previously returned only boilerplate)
    {
        "url": "https://arxiv.org/abs/2404.10719",
        "title": "Is DPO Superior to PPO for LLM Alignment? A Comprehensive Study",
        "expect": "full paper text, not just abstract metadata",
        "category": "arxiv-abs",
    },
    # arxiv PDF (binary — trafilatura can't parse)
    {
        "url": "https://arxiv.org/pdf/2212.08073.pdf",
        "title": "Constitutional AI: Harmlessness from AI Feedback",
        "expect": "full paper text via HTML rewrite or search fallback",
        "category": "arxiv-pdf",
    },
    # CDN-hosted PDF (not arxiv — no HTML rewrite available)
    {
        "url": "https://cdn.openai.com/papers/Training_language_models_to_follow_instructions_with_human_feedback.pdf",
        "title": "Training language models to follow instructions with human feedback",
        "expect": "paper content via search fallback",
        "category": "cdn-pdf",
    },
    # Conference proceedings PDF
    {
        "url": "https://proceedings.neurips.cc/paper_files/paper/2024/file/404df2480b6eef0486a1679e371894b0-Paper-Conference.pdf",
        "title": "Unpacking DPO and PPO: Disentangling Best Practices for Learning from Preferences",
        "expect": "paper content via search fallback",
        "category": "conference-pdf",
    },
    # Standard HTML blog post (should work with trafilatura — baseline)
    {
        "url": "https://huggingface.co/blog/rlhf",
        "title": "Illustrating Reinforcement Learning from Human Feedback (RLHF)",
        "expect": "full blog post text via trafilatura",
        "category": "html-blog",
    },
    # Docs page (should work — baseline)
    {
        "url": "https://huggingface.co/docs/trl/main/en/dpo_trainer",
        "title": "TRL DPO Trainer Documentation",
        "expect": "documentation text via trafilatura or browser",
        "category": "html-docs",
    },
]


def _preview(text: str, max_len: int = 200) -> str:
    text = text.replace("\n", " ").strip()
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text


def _quality_check(content: str, category: str) -> dict:
    """Basic quality heuristics for downloaded content."""
    words = len(content.split())
    lines = content.count("\n") + 1

    # Check for arxiv boilerplate pollution
    boilerplate_phrases = [
        "What is Connected Papers",
        "What is the Explorer",
        "arXivLabs",
        "Bibliographic Explorer",
        "export BibTeX",
    ]
    boilerplate_hits = sum(1 for phrase in boilerplate_phrases if phrase in content)

    # Check for precision signals (equations, numbers, technical terms)
    import re
    has_equations = bool(re.search(r'[=∝∑∏∫]|\\frac|\\mathbb|L_\{|\\pi|\\beta', content))
    has_numbers = bool(re.search(r'\d+\.\d+%|\d+\.\d{2,}', content))
    has_tables = "Table" in content or "| " in content or "Results" in content

    if category.startswith("arxiv") or category.endswith("pdf"):
        min_words = 500
        quality = "good" if words >= min_words and boilerplate_hits == 0 else "thin"
        if words < 200:
            quality = "bad"
    else:
        min_words = 200
        quality = "good" if words >= min_words else "thin"

    return {
        "words": words,
        "lines": lines,
        "boilerplate_hits": boilerplate_hits,
        "has_equations": has_equations,
        "has_numbers": has_numbers,
        "has_tables": has_tables,
        "quality": quality,
    }


async def _test_single_strategy(url: str, strategy: str, title: str = "") -> dict:
    """Test a single download strategy on a URL."""
    from app.services.wiki_downloader import (
        _fetch_with_trafilatura, _fetch_with_browser, _fetch_with_jina,
        _fetch_via_search, _normalize_arxiv_urls,
    )

    t0 = time.time()
    test_url = url

    if strategy == "trafilatura":
        variants = _normalize_arxiv_urls(url)
        result = {"url": url, "content": "", "error": "all variants failed"}
        for variant in variants:
            result = await _fetch_with_trafilatura(variant)
            if result.get("content"):
                result["note"] = f"succeeded on {variant}"
                break
    elif strategy == "browser":
        variants = _normalize_arxiv_urls(url)
        test_url = variants[0]
        result = await _fetch_with_browser(test_url)
    elif strategy == "jina":
        result = await _fetch_with_jina(url)
    elif strategy == "search":
        result = await _fetch_via_search(url, title=title)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

    elapsed = time.time() - t0
    return {
        "strategy": strategy,
        "url_tested": test_url,
        "success": bool(result.get("content")),
        "error": result.get("error", ""),
        "word_count": result.get("word_count", 0),
        "elapsed_s": round(elapsed, 1),
        "preview": _preview(result.get("content", "")),
    }


async def _test_cascade(url: str, title: str = "") -> dict:
    """Test the full download cascade (the real path)."""
    from app.services.wiki_downloader import download_url

    t0 = time.time()
    result = await download_url(url, title=title)
    elapsed = time.time() - t0

    content = result.get("content", "")
    category = "unknown"
    for t in TEST_URLS:
        if t["url"] == url:
            category = t["category"]
            break

    quality = _quality_check(content, category) if content else {}

    return {
        "success": bool(content),
        "via": result.get("via", "none"),
        "error": result.get("error", ""),
        "word_count": result.get("word_count", 0),
        "elapsed_s": round(elapsed, 1),
        "quality": quality,
        "preview": _preview(content),
    }


async def run_all(urls: list[dict], strategy_mode: bool = False) -> list[dict]:
    results = []

    for i, entry in enumerate(urls, 1):
        url = entry["url"]
        title = entry.get("title", "")
        category = entry.get("category", "unknown")

        print(f"\n{'─' * 70}")
        print(f"  [{i}/{len(urls)}] {category}: {url[:70]}")
        if title:
            print(f"  Title: {title}")
        print(f"  Expect: {entry.get('expect', '?')}")
        print(f"{'─' * 70}")

        record = {"url": url, "title": title, "category": category}

        if strategy_mode:
            print("\n  Testing each strategy individually:\n")
            for strat in ["trafilatura", "browser", "jina", "search"]:
                print(f"    {strat}... ", end="", flush=True)
                try:
                    r = await _test_single_strategy(url, strat, title=title)
                    status = f"OK ({r['word_count']}w, {r['elapsed_s']}s)" if r["success"] else f"FAIL: {r['error'][:60]}"
                    print(status)
                    record[f"strategy_{strat}"] = r
                except Exception as e:
                    print(f"ERROR: {e}")
                    record[f"strategy_{strat}"] = {"success": False, "error": str(e)}

        print("\n  Full cascade... ", end="", flush=True)
        cascade = await _test_cascade(url, title=title)
        status = f"OK via {cascade['via']} ({cascade['word_count']}w, {cascade['elapsed_s']}s)"
        if not cascade["success"]:
            status = f"FAIL: {cascade['error'][:80]}"
        print(status)
        record["cascade"] = cascade

        if cascade.get("quality"):
            q = cascade["quality"]
            flags = []
            if q.get("has_equations"):
                flags.append("equations")
            if q.get("has_numbers"):
                flags.append("numbers")
            if q.get("has_tables"):
                flags.append("tables")
            if q.get("boilerplate_hits", 0) > 0:
                flags.append(f"boilerplate({q['boilerplate_hits']})")
            print(f"  Quality: {q['quality']} | {q['words']}w, {q['lines']} lines | {', '.join(flags) or 'no precision signals'}")

        if cascade.get("preview"):
            print(f"  Preview: {cascade['preview'][:120]}")

        results.append(record)

    return results


def _print_summary(results: list[dict]):
    print(f"\n{'=' * 70}")
    print("  DOWNLOAD TEST SUMMARY")
    print(f"{'=' * 70}\n")

    print(f"  {'Category':<20} {'Via':<15} {'Words':>7} {'Time':>6} {'Quality':<8} {'Status'}")
    print(f"  {'─' * 20} {'─' * 15} {'─' * 7} {'─' * 6} {'─' * 8} {'─' * 15}")

    ok = 0
    fail = 0
    for r in results:
        c = r["cascade"]
        quality = c.get("quality", {}).get("quality", "n/a")
        if c["success"]:
            ok += 1
            line = f"  {r['category']:<20} {c['via']:<15} {c['word_count']:>7} {c['elapsed_s']:>5.1f}s {quality:<8} OK"
        else:
            fail += 1
            line = f"  {r['category']:<20} {'—':<15} {'—':>7} {c['elapsed_s']:>5.1f}s {'—':<8} FAIL: {c['error'][:30]}"
        print(line)

    print(f"\n  Result: {ok}/{len(results)} succeeded, {fail} failed")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    strategy_mode = "--strategy" in flags

    if "--url" in flags:
        idx = flags.index("--url")
        if args:
            custom_url = args[0]
        else:
            print("Usage: --url <URL>")
            sys.exit(1)
        urls = [{"url": custom_url, "title": "", "expect": "custom URL", "category": "custom"}]
    elif "--failed" in flags:
        if RESULTS_PATH.exists():
            prior = json.loads(RESULTS_PATH.read_text())
            urls = [r for r in prior if not r.get("cascade", {}).get("success")]
            if not urls:
                print("No prior failures found. Run without --failed first.")
                sys.exit(0)
            print(f"Retesting {len(urls)} prior failures...")
        else:
            print(f"No prior results at {RESULTS_PATH}. Run without --failed first.")
            sys.exit(1)
    else:
        urls = TEST_URLS

    results = asyncio.run(run_all(urls, strategy_mode=strategy_mode))
    _print_summary(results)

    RESULTS_PATH.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n  Results saved to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
