#!/usr/bin/env python3
"""
Automated wiki update pipeline.

Usage:
    python3 scripts/update_wiki.py           # full update
    python3 scripts/update_wiki.py --no-build  # skip Quartz build (content only)
    python3 scripts/update_wiki.py --dry-run   # show what would change, don't write

What it does:
  1. Scan content/pedagogy-wiki/resources/by-topic/ for all topic slugs
  2. Compare against wiki_config.json to find new/unclassified topics
  3. If new topics found → one LLM call to classify them into subjects
     and suggest related topics
  4. Update wiki_config.json with the new assignments
  5. Re-run topic_to_quartz.py to regenerate all wiki content
  6. Run npx quartz build to rebuild the static site

Environment:
    LLM_API_KEY   — API key for the NVIDIA inference API
    LLM_BASE_URL  — Base URL (default: https://inference-api.nvidia.com)
    LLM_MODEL     — Model ID (default: openai/openai/gpt-5.2)

These are read from backend/.env if present.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).parent.parent
_CONTENT = Path(os.environ.get("CONTENT_DIR", str(REPO_ROOT / "content"))).resolve()
SOURCE_DIR = _CONTENT / "pedagogy-wiki" / "resources" / "by-topic"
CONFIG_PATH = REPO_ROOT / "wiki_config.json"
WIKI_DIR = REPO_ROOT / "wiki"
BACKEND_ENV = REPO_ROOT / "backend" / ".env"
BACKEND_SETTINGS = REPO_ROOT / "backend" / "settings.yaml"

# ---------------------------------------------------------------------------
# Load environment (from backend/.env if present)
# ---------------------------------------------------------------------------

def load_env() -> None:
    if BACKEND_ENV.exists():
        for line in BACKEND_ENV.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, val = line.partition("=")
                os.environ.setdefault(key.strip(), val.strip())


def load_llm_settings() -> dict:
    """Read base_url and default model from backend/settings.yaml."""
    try:
        import yaml
        with open(BACKEND_SETTINGS) as f:
            cfg = yaml.safe_load(f)
        return {
            "base_url": cfg.get("llm", {}).get("base_url", "https://inference-api.nvidia.com"),
            "model": cfg.get("models", {}).get("tutor", {}).get("model_id", "openai/openai/gpt-5.2"),
        }
    except Exception:
        return {
            "base_url": "https://inference-api.nvidia.com",
            "model": "openai/openai/gpt-5.2",
        }

# ---------------------------------------------------------------------------
# Config helpers
# ---------------------------------------------------------------------------

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"ERROR: {CONFIG_PATH} not found.", file=sys.stderr)
        sys.exit(1)
    with open(CONFIG_PATH) as f:
        return json.load(f)


def save_config(cfg: dict) -> None:
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2, ensure_ascii=False)
    print(f"  Saved {CONFIG_PATH}")

# ---------------------------------------------------------------------------
# LLM classification
# ---------------------------------------------------------------------------

CLASSIFY_SYSTEM = """\
You are a curriculum taxonomy expert for an AI/ML education platform.
You will be given:
  1. The existing subject taxonomy (subject name → list of topic slugs)
  2. A list of new topic slugs to classify

Your job:
  - Assign each new topic to the most appropriate existing subject.
  - If a new topic genuinely doesn't fit any existing subject, propose a new subject name.
  - For each new topic, also suggest 2-4 related existing topic slugs based on conceptual proximity.
  - Optionally suggest a human-readable title override if the slug has awkward casing (e.g. "cnns" → "CNNs").

Respond with ONLY valid JSON in this exact format:
{
  "classifications": [
    {
      "slug": "new-topic-slug",
      "subject": "Existing Subject Name or New Subject Name",
      "related_topics": ["existing-slug-1", "existing-slug-2"],
      "title_override": "Optional Title or null"
    }
  ],
  "new_subjects": [
    {
      "name": "New Subject Name",
      "slug": "new-subject-slug",
      "description": "One sentence description of this subject area."
    }
  ]
}
"""


def classify_new_topics(new_slugs: list[str], cfg: dict) -> dict:
    """Call LLM to classify new topic slugs. Returns parsed JSON response."""
    llm_settings = load_llm_settings()
    api_key = os.environ.get("LLM_API_KEY", "")
    base_url = os.environ.get("LLM_BASE_URL", llm_settings["base_url"])
    model = os.environ.get("LLM_MODEL", llm_settings["model"])

    if not api_key:
        print("WARNING: LLM_API_KEY not set — skipping LLM classification.")
        print("         Assigning new topics to 'Foundational AI' as default.")
        print("         Update wiki_config.json manually to fix subject assignments.")
        return {"classifications": [
            {"slug": s, "subject": "Foundational AI", "related_topics": [], "title_override": None}
            for s in new_slugs
        ], "new_subjects": []}

    try:
        from openai import OpenAI
    except ImportError:
        print("ERROR: openai package not installed. Run: pip install openai", file=sys.stderr)
        sys.exit(1)

    # Build taxonomy summary for the prompt
    by_subject: dict[str, list[str]] = {}
    for slug, subject in cfg["subject_map"].items():
        by_subject.setdefault(subject, []).append(slug)

    taxonomy_lines = []
    for subject, slugs in sorted(by_subject.items()):
        taxonomy_lines.append(f"  {subject}: {', '.join(slugs)}")
    taxonomy_str = "\n".join(taxonomy_lines)

    user_prompt = f"""Current taxonomy:
{taxonomy_str}

New topics to classify:
{chr(10).join(f'  - {s}' for s in new_slugs)}

Classify each new topic and suggest related existing topics."""

    print(f"\n  Calling LLM ({model}) to classify {len(new_slugs)} new topic(s)...")

    client = OpenAI(api_key=api_key, base_url=f"{base_url}/v1")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": CLASSIFY_SYSTEM},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON even if wrapped in markdown code fences
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
    if json_match:
        raw = json_match.group(1)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"WARNING: LLM returned invalid JSON ({e}). Raw response:\n{raw}", file=sys.stderr)
        return {"classifications": [
            {"slug": s, "subject": "Foundational AI", "related_topics": [], "title_override": None}
            for s in new_slugs
        ], "new_subjects": []}


def apply_classifications(result: dict, cfg: dict, dry_run: bool) -> int:
    """Apply LLM classification results to wiki_config. Returns count of changes."""
    changes = 0
    existing_slugs = set(cfg["subject_map"].keys())

    # Add any new subjects first
    for new_sub in result.get("new_subjects", []):
        name = new_sub["name"]
        slug = new_sub["slug"]
        desc = new_sub.get("description", "")
        if name not in cfg["subject_slugs"]:
            print(f"  [new subject] {name} ({slug})")
            if not dry_run:
                cfg["subject_slugs"][name] = slug
                cfg["subject_descriptions"][name] = desc
            changes += 1

    for item in result.get("classifications", []):
        topic_slug = item["slug"]
        subject = item["subject"]
        related = [r for r in item.get("related_topics", []) if r in existing_slugs]
        title_override = item.get("title_override")

        print(f"  [classify] {topic_slug} → {subject}"
              + (f" | related: {related}" if related else "")
              + (f" | title: {title_override}" if title_override else ""))

        if not dry_run:
            cfg["subject_map"][topic_slug] = subject
            if related:
                cfg["related_topics"][topic_slug] = related
                # Add back-links: add this topic to related topics' lists
                for rel_slug in related:
                    back = cfg["related_topics"].setdefault(rel_slug, [])
                    if topic_slug not in back:
                        back.append(topic_slug)
            if title_override:
                cfg["title_overrides"][topic_slug] = title_override
        changes += 1

    return changes

# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def run_transform(dry_run: bool) -> None:
    if dry_run:
        print("\n  [dry-run] Would run: python3 scripts/topic_to_quartz.py")
        return
    print("\nRunning topic_to_quartz.py...")
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "scripts" / "topic_to_quartz.py")],
        cwd=REPO_ROOT,
    )
    if result.returncode != 0:
        print("ERROR: topic_to_quartz.py failed.", file=sys.stderr)
        sys.exit(1)


def run_quartz_build(dry_run: bool) -> None:
    if dry_run:
        print("\n  [dry-run] Would run: npx quartz build")
        return
    print("\nBuilding Quartz site...")
    result = subprocess.run(["npx", "quartz", "build"], cwd=WIKI_DIR)
    if result.returncode != 0:
        print("ERROR: Quartz build failed.", file=sys.stderr)
        sys.exit(1)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Update the SocraticTutor wiki")
    parser.add_argument("--no-build", action="store_true", help="Skip Quartz build step")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    args = parser.parse_args()

    load_env()

    print("=" * 60)
    print("SocraticTutor Wiki Update")
    print("=" * 60)

    # Step 1: Find all topic slugs in the source directory
    if not SOURCE_DIR.exists():
        print(f"ERROR: {SOURCE_DIR} not found.", file=sys.stderr)
        sys.exit(1)

    source_slugs = {p.stem for p in SOURCE_DIR.glob("*.md")}
    print(f"\nFound {len(source_slugs)} topic files in source directory")

    # Step 2: Load config and find new topics
    cfg = load_config()
    classified_slugs = set(cfg["subject_map"].keys())
    new_slugs = sorted(source_slugs - classified_slugs)

    if new_slugs:
        print(f"\nNew topics not yet in wiki_config.json ({len(new_slugs)}):")
        for s in new_slugs:
            print(f"  - {s}")

        # Step 3: LLM classification
        result = classify_new_topics(new_slugs, cfg)

        # Step 4: Apply to config
        print("\nApplying classifications:")
        changes = apply_classifications(result, cfg, args.dry_run)

        if not args.dry_run and changes > 0:
            save_config(cfg)
            print(f"  Updated wiki_config.json with {changes} new entries")
    else:
        print("\nNo new topics found — wiki_config.json is up to date")

    # Step 5: Regenerate content
    run_transform(args.dry_run)

    # Step 6: Build Quartz
    if not args.no_build:
        run_quartz_build(args.dry_run)

    print("\n" + "=" * 60)
    if args.dry_run:
        print("Dry run complete — no files were modified")
    else:
        print("Wiki update complete")
    print("=" * 60)


if __name__ == "__main__":
    main()
