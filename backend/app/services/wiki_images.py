"""
Image extraction, annotation, and storage for the pedagogy wiki.

Pipeline per source page:
    1. Extract image candidates + surrounding context from HTML
    2. Heuristic pre-filter (remove logos, icons, tracking pixels)
    3. LLM annotation — filter, describe, tag concepts, suggest caption
    4. Download keepers and update images.json index
    5. (Optional) Multimodal tier-2 — vision LLM enhances annotations
       with visual details only the image itself can reveal
"""

import asyncio
import base64
import json
import logging
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

logger = logging.getLogger(__name__)

from ..config import WIKI_DIR as _WIKI_DIR  # noqa: E402 — must follow logger

# ---------------------------------------------------------------------------
# Heuristic constants
# ---------------------------------------------------------------------------

_JUNK_URL_RE = re.compile(
    r"gravatar|badge|logo|favicon|pixel|analytics|tracking|avatar|"
    r"icons?[/.]|emoji|spinner|loading|placeholder|spacer|blank|"
    r"1x1|share|social|button|arrow|chevron|widget|ads?[/.]|"
    r"banner[/.]|profile[-_]|thumb[-_]?nail|\.gif\?|beacon",
    re.IGNORECASE,
)

_CONTENT_EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".gif", ".webp"}
_NON_CONTENT_TAGS = {"nav", "header", "footer", "aside"}
_MIN_DIMENSION = 150

# Real words contain vowels; hex hashes almost never form vowel-bearing words
_VOWEL_WORD_RE = re.compile(r"[a-zA-Z]*[aeiouAEIOU][a-zA-Z]*")

def _guess_author(page_url: str) -> str:
    """Resolve author name from URL via the author registry."""
    from .wiki_authors import resolve_author
    entry = resolve_author(page_url)
    return entry.get("name", "") if entry else ""


# ---------------------------------------------------------------------------
# Step 1: Extract image candidates + context from HTML
# ---------------------------------------------------------------------------

def _parse_dimension(val) -> int | None:
    if val is None:
        return None
    try:
        return int(str(val).replace("px", "").replace("%", "").strip())
    except (ValueError, TypeError):
        return None


def _get_surrounding_text(element, max_chars: int = 1500) -> str:
    """Grab paragraph text near an image for context."""
    anchor = element.find_parent("figure") or element

    before_els = anchor.find_all_previous("p", limit=3)
    before = [
        el.get_text(strip=True)
        for el in reversed(before_els)
        if len(el.get_text(strip=True)) > 20
    ][:2]

    after_els = anchor.find_all_next("p", limit=3)
    after = [
        el.get_text(strip=True)
        for el in after_els
        if len(el.get_text(strip=True)) > 20
    ][:2]

    return "\n\n".join(before + after)[:max_chars]


def extract_images_from_html(
    html: str,
    page_url: str,
    *,
    js_dimensions: dict[str, tuple[int, int]] | None = None,
) -> list[dict]:
    """Parse HTML and return image candidates with surrounding context.

    Each candidate dict contains: src, alt, title, caption,
    section_heading, surrounding_text, width, height, in_content_area.
    """
    from bs4 import BeautifulSoup, Tag

    soup = BeautifulSoup(html, "html.parser")
    candidates: list[dict] = []
    seen: set[str] = set()

    for img in soup.find_all("img"):
        src = img.get("src") or img.get("data-src") or ""
        if not src or src.startswith("data:"):
            continue

        abs_src = urljoin(page_url, src)
        if abs_src in seen:
            continue
        seen.add(abs_src)

        alt = (img.get("alt") or "").strip()
        title = (img.get("title") or "").strip()

        width = _parse_dimension(img.get("width"))
        height = _parse_dimension(img.get("height"))
        if js_dimensions and abs_src in js_dimensions:
            js_w, js_h = js_dimensions[abs_src]
            if js_w and js_h:
                width, height = js_w, js_h

        caption = ""
        figure = img.find_parent("figure")
        if figure:
            figcap = figure.find("figcaption")
            if figcap:
                caption = figcap.get_text(strip=True)

        in_content = True
        for parent in img.parents:
            if isinstance(parent, Tag) and parent.name in _NON_CONTENT_TAGS:
                if not img.find_parent("figure"):
                    in_content = False
                break

        heading_el = img.find_previous(["h1", "h2", "h3", "h4", "h5", "h6"])
        section_heading = heading_el.get_text(strip=True) if heading_el else ""

        surrounding = _get_surrounding_text(img)

        candidates.append({
            "src": abs_src,
            "alt": alt,
            "title": title,
            "caption": caption,
            "section_heading": section_heading,
            "surrounding_text": surrounding,
            "width": width,
            "height": height,
            "in_content_area": in_content,
        })

    logger.info("Extracted %d raw image candidates from %s", len(candidates), page_url)
    return candidates


# ---------------------------------------------------------------------------
# Step 2: Heuristic pre-filter
# ---------------------------------------------------------------------------

def _get_extension(url: str) -> str | None:
    path = urlparse(url).path
    if "." in path:
        ext = "." + path.rsplit(".", 1)[-1].lower()
        if len(ext) <= 6:
            return ext
    return None


def _is_hash_filename(url: str) -> bool:
    """Detect filenames that are hashes, UUIDs, or numeric IDs (no words).

    Uses a vowel heuristic: real English words almost always contain
    vowels, but hex hashes (a-f + digits) rarely form vowel-bearing
    sequences of 3+ characters.
    """
    path = urlparse(url).path
    filename = path.rsplit("/", 1)[-1] if "/" in path else path
    stem = filename.rsplit(".", 1)[0] if "." in filename else filename
    stem = stem.split("?")[0]
    meaningful = [w for w in _VOWEL_WORD_RE.findall(stem) if len(w) >= 3]
    return len(meaningful) == 0


def heuristic_filter_images(candidates: list[dict]) -> list[dict]:
    """Remove obvious non-content images before the LLM pass."""
    filtered = []
    for c in candidates:
        src = c["src"]

        ext = _get_extension(src)
        if ext and ext not in _CONTENT_EXTENSIONS:
            continue

        if _JUNK_URL_RE.search(src):
            continue

        if not c.get("in_content_area", True):
            continue

        if _is_hash_filename(src) and not c.get("alt") and not c.get("caption"):
            continue

        w, h = c.get("width"), c.get("height")
        if w is not None and h is not None:
            if w < _MIN_DIMENSION or h < _MIN_DIMENSION:
                continue

        filtered.append(c)

    skipped = len(candidates) - len(filtered)
    if skipped:
        logger.info(
            "Heuristic filter: %d → %d images (%d removed)",
            len(candidates), len(filtered), skipped,
        )
    return filtered


# ---------------------------------------------------------------------------
# Step 3: LLM annotation
# ---------------------------------------------------------------------------

ANNOTATE_IMAGES_PROMPT = """\
You are annotating images from an educational blog/article for a teaching \
wiki. The blog author explains their diagrams in surrounding text — use \
that context to create rich, structured annotations.

PAGE: {page_title}
SOURCE: {page_url}
AUTHOR: {source_author}

IMAGES TO ANNOTATE:
{images_text}

For each image decide: is it EDUCATIONAL (diagram, chart, architecture, \
equation, code output, visualization) or NON-EDUCATIONAL (decorative, \
stock photo, author photo, UI chrome, social/share graphic)?

Return JSON:
{{
  "images": [
    {{
      "index": <image number from above>,
      "keep": true,
      "description": "What the image shows — be specific",
      "teaching_value": "HOW this helps a student learn, not just 'relevant'",
      "concepts": ["concept1", "concept2"],
      "when_to_show": "Actionable guidance for a tutor — when to surface it",
      "suggested_caption": "Under 15 words, with attribution"
    }}
  ]
}}

For non-educational images, return just:
{{ "index": <N>, "keep": false }}

IMPORTANT:
- Use the surrounding text to understand what the image teaches
- 'concepts' should use precise technical terms
- 'when_to_show' should be actionable for a tutor
- If you cannot determine what an image teaches, set keep=false

Return ONLY valid JSON.
"""


_ANNOTATE_BATCH_SIZE = 10


async def _annotate_batch(
    page_title: str,
    page_url: str,
    source_author: str,
    batch: list[dict],
    batch_offset: int,
) -> list[dict]:
    """Annotate a single batch of image candidates."""
    from .course_enricher import _call_llm_json

    images_text = ""
    for i, c in enumerate(batch, 1):
        filename = c["src"].rsplit("/", 1)[-1][:80]
        images_text += f"\n--- IMAGE {i} ---\n"
        images_text += f"File: {filename}\n"
        if c["alt"]:
            images_text += f"Alt text: {c['alt']}\n"
        if c["caption"]:
            images_text += f"Caption: {c['caption']}\n"
        if c["section_heading"]:
            images_text += f"Section: {c['section_heading']}\n"
        if c["width"] and c["height"]:
            images_text += f"Size: {c['width']}×{c['height']}\n"
        if c["surrounding_text"]:
            images_text += f"Context: {c['surrounding_text'][:800]}\n"

    prompt = ANNOTATE_IMAGES_PROMPT.format(
        page_title=page_title,
        page_url=page_url,
        source_author=source_author or "(unknown)",
        images_text=images_text,
    )

    result = await _call_llm_json(prompt, max_tokens=4096, temperature=0.0)

    annotated: list[dict] = []
    for ann in result.get("images", []):
        idx = ann.get("index", 0) - 1
        if 0 <= idx < len(batch):
            merged = {**batch[idx], **ann}
            annotated.append(merged)

    return annotated


async def annotate_images(
    page_title: str,
    page_url: str,
    source_author: str,
    candidates: list[dict],
) -> list[dict]:
    """Text-only LLM annotation, auto-batched for large image sets."""
    if not candidates:
        return []

    all_annotated: list[dict] = []
    num_batches = (len(candidates) + _ANNOTATE_BATCH_SIZE - 1) // _ANNOTATE_BATCH_SIZE

    if num_batches > 1:
        logger.info(
            "Annotating %d images in %d batches of %d for %s",
            len(candidates), num_batches, _ANNOTATE_BATCH_SIZE, page_url,
        )

    for batch_idx in range(num_batches):
        start = batch_idx * _ANNOTATE_BATCH_SIZE
        batch = candidates[start : start + _ANNOTATE_BATCH_SIZE]

        try:
            batch_results = await _annotate_batch(
                page_title, page_url, source_author, batch, start,
            )
            all_annotated.extend(batch_results)
        except Exception as e:
            logger.warning(
                "Annotation batch %d/%d failed for %s: %s",
                batch_idx + 1, num_batches, page_url, e,
            )

    kept = sum(1 for a in all_annotated if a.get("keep"))
    logger.info(
        "Annotation for %s: %d candidates → %d educational, %d dropped",
        page_url, len(candidates), kept, len(all_annotated) - kept,
    )
    return all_annotated


# ---------------------------------------------------------------------------
# Step 4: Download images and update images.json
# ---------------------------------------------------------------------------

def _images_dir(topic_slug: str) -> Path:
    return _WIKI_DIR / "resources" / "by-topic" / topic_slug / "images"


def _images_json_path(topic_slug: str) -> Path:
    return _images_dir(topic_slug) / "images.json"


def build_global_image_index() -> dict[str, Path]:
    """Map source_url → local file path across ALL topics.

    Used to avoid re-downloading the same image when a source page
    appears under multiple topics.
    """
    index: dict[str, Path] = {}
    by_topic = _WIKI_DIR / "resources" / "by-topic"
    if not by_topic.is_dir():
        return index
    for topic_dir in by_topic.iterdir():
        if not topic_dir.is_dir():
            continue
        json_path = topic_dir / "images" / "images.json"
        if not json_path.exists():
            continue
        try:
            entries = json.loads(json_path.read_text())
        except (json.JSONDecodeError, OSError):
            continue
        for entry in entries:
            src_url = entry.get("source_url", "")
            file_path = topic_dir / "images" / entry["file"]
            if src_url and src_url not in index and file_path.exists():
                index[src_url] = file_path
    return index


def load_images_json(topic_slug: str) -> list[dict]:
    """Load the images.json index for a topic. Returns [] if absent."""
    path = _images_json_path(topic_slug)
    if path.exists():
        try:
            return json.loads(path.read_text())
        except (json.JSONDecodeError, ValueError):
            return []
    return []


def _save_images_json(topic_slug: str, entries: list[dict]) -> None:
    path = _images_json_path(topic_slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(entries, indent=2))


def _read_image_dimensions(data: bytes) -> tuple[int | None, int | None]:
    """Read width/height from image file bytes (PNG/JPEG/GIF/SVG)."""
    if data[:8] == b"\x89PNG\r\n\x1a\n" and len(data) >= 24:
        import struct
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    if data[:2] == b"\xff\xd8":  # JPEG
        import struct
        i = 2
        while i < len(data) - 8:
            if data[i] != 0xFF:
                break
            marker = data[i + 1]
            if marker in (0xC0, 0xC1, 0xC2):
                h, w = struct.unpack(">HH", data[i + 5 : i + 9])
                return w, h
            length = struct.unpack(">H", data[i + 2 : i + 4])[0]
            i += 2 + length
    if data[:6] in (b"GIF87a", b"GIF89a") and len(data) >= 10:
        import struct
        w, h = struct.unpack("<HH", data[6:10])
        return w, h
    # SVG: parse viewBox or width/height attributes from the root <svg> element
    if b"<svg" in data[:500]:
        return _read_svg_dimensions(data)
    return None, None


def _read_svg_dimensions(data: bytes) -> tuple[int | None, int | None]:
    """Extract dimensions from SVG viewBox or width/height attributes."""
    try:
        text = data[:4096].decode("utf-8", errors="ignore")
    except Exception:
        return None, None

    svg_match = re.search(r"<svg[^>]*>", text, re.IGNORECASE | re.DOTALL)
    if not svg_match:
        return None, None
    svg_tag = svg_match.group(0)

    # Try viewBox first (most reliable): viewBox="minX minY width height"
    vb = re.search(r'viewBox\s*=\s*["\']([^"\']+)["\']', svg_tag)
    if vb:
        parts = vb.group(1).split()
        if len(parts) == 4:
            try:
                return int(float(parts[2])), int(float(parts[3]))
            except (ValueError, IndexError):
                pass

    # Fall back to width/height attributes
    w_match = re.search(r'width\s*=\s*["\']?([\d.]+)', svg_tag)
    h_match = re.search(r'height\s*=\s*["\']?([\d.]+)', svg_tag)
    if w_match and h_match:
        try:
            return int(float(w_match.group(1))), int(float(h_match.group(1)))
        except ValueError:
            pass

    return None, None


def _display_hint(width: int | None, height: int | None) -> str:
    """Suggest how to render based on aspect ratio."""
    if not width or not height:
        return "standard"
    ratio = width / height
    if ratio > 2.5:
        return "full_width"
    if ratio < 0.5:
        return "tall"
    return "standard"


async def download_images(
    topic_slug: str,
    source_slug: str,
    source_page_url: str,
    source_author: str,
    annotations: list[dict],
    *,
    global_image_index: dict[str, Path] | None = None,
) -> dict:
    """Download images marked keep=True and update images.json.

    If *global_image_index* maps source_url → existing local path,
    files are copied instead of re-downloaded (cross-topic dedup).
    """
    import shutil
    import httpx

    img_dir = _images_dir(topic_slug)
    img_dir.mkdir(parents=True, exist_ok=True)

    existing = load_images_json(topic_slug)
    existing_urls = {e["source_url"] for e in existing}

    keepers = [a for a in annotations if a.get("keep")]
    stats: dict[str, int] = {
        "downloaded": 0, "copied": 0, "skipped": 0, "failed": 0,
    }
    new_entries: list[dict] = []

    async with httpx.AsyncClient(
        timeout=30.0, follow_redirects=True,
        limits=httpx.Limits(max_connections=5),
    ) as client:
        for i, ann in enumerate(keepers):
            src_url = ann["src"]
            if src_url in existing_urls:
                stats["skipped"] += 1
                continue

            ext = _get_extension(src_url) or ".png"
            filename = f"{source_slug}_{i + 1:03d}{ext}"
            save_path = img_dir / filename

            image_bytes: bytes | None = None

            # Try copying from another topic first (dedup)
            existing_path = (global_image_index or {}).get(src_url)
            if existing_path and existing_path.exists():
                try:
                    shutil.copy2(existing_path, save_path)
                    image_bytes = save_path.read_bytes()
                    stats["copied"] += 1
                except OSError:
                    existing_path = None  # fall through to download

            download_failed = False
            if image_bytes is None:
                try:
                    resp = await client.get(src_url)
                    resp.raise_for_status()

                    ct = resp.headers.get("content-type", "")
                    if not any(t in ct for t in ("image/", "svg", "octet-stream")):
                        stats["failed"] += 1
                        download_failed = True
                    else:
                        image_bytes = resp.content
                        save_path.write_bytes(image_bytes)
                        stats["downloaded"] += 1
                except Exception as e:
                    logger.debug("Failed to download image %s: %s", src_url, e)
                    stats["failed"] += 1
                    download_failed = True

            # Read actual dimensions from file bytes when available
            w, h = ann.get("width"), ann.get("height")
            if image_bytes is not None:
                actual_w, actual_h = _read_image_dimensions(image_bytes)
                if actual_w and actual_h:
                    w, h = actual_w, actual_h

            file_size_kb = round(len(image_bytes) / 1024, 1) if image_bytes else None

            entry: dict = {
                "file": filename if not download_failed else None,
                "source_url": src_url,
                "source_page": source_page_url,
                "source_author": source_author,
                "alt": ann.get("alt", ""),
                "description": ann.get("description", ""),
                "teaching_value": ann.get("teaching_value", ""),
                "concepts": ann.get("concepts", []),
                "when_to_show": ann.get("when_to_show", ""),
                "suggested_caption": ann.get("suggested_caption", ""),
                "width": w,
                "height": h,
                "aspect_ratio": round(w / h, 2) if w and h else None,
                "display_hint": _display_hint(w, h),
                "file_size_kb": file_size_kb,
            }
            if download_failed:
                entry["url_only"] = True
            new_entries.append(entry)

            # Register in global index so later topics can copy from us
            if global_image_index is not None and src_url not in global_image_index:
                global_image_index[src_url] = save_path

    if new_entries:
        existing.extend(new_entries)
        _save_images_json(topic_slug, existing)
        logger.info(
            "images.json for %s: +%d images (%d total)",
            topic_slug, len(new_entries), len(existing),
        )

    return stats


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

async def process_source_images(
    topic_slug: str,
    page_title: str,
    page_url: str,
    raw_html: str,
    *,
    js_dimensions: dict[str, tuple[int, int]] | None = None,
    force: bool = False,
    global_image_index: dict[str, Path] | None = None,
) -> dict:
    """Full image pipeline for one source page.

    Returns a summary dict with extraction/filter/annotation/download counts.
    Pass *global_image_index* to deduplicate downloads across topics.
    """
    from .wiki_downloader import _source_slug

    # Skip if already processed
    if not force:
        existing = load_images_json(topic_slug)
        if any(e["source_page"] == page_url for e in existing):
            count = sum(1 for e in existing if e["source_page"] == page_url)
            logger.info("Images already extracted for %s (%d images)", page_url, count)
            return {"status": "already_processed", "existing_images": count}

    # Step 1: Extract
    candidates = extract_images_from_html(
        raw_html, page_url, js_dimensions=js_dimensions,
    )
    if not candidates:
        return {"status": "no_images", "extracted": 0}

    # Step 2: Heuristic filter
    filtered = heuristic_filter_images(candidates)
    if not filtered:
        return {
            "status": "all_filtered",
            "extracted": len(candidates),
            "after_filter": 0,
        }

    # Step 3: LLM annotation
    source_author = _guess_author(page_url)
    annotations = await annotate_images(
        page_title, page_url, source_author, filtered,
    )
    kept = [a for a in annotations if a.get("keep")]
    if not kept:
        return {
            "status": "none_educational",
            "extracted": len(candidates),
            "after_filter": len(filtered),
            "kept": 0,
        }

    # Step 4: Download (with cross-topic dedup if index provided)
    slug = _source_slug(page_url)
    dl_stats = await download_images(
        topic_slug, slug, page_url, source_author, annotations,
        global_image_index=global_image_index,
    )

    return {
        "status": "ok",
        "extracted": len(candidates),
        "after_filter": len(filtered),
        "annotated": len(annotations),
        "kept": len(kept),
        **dl_stats,
    }


# ---------------------------------------------------------------------------
# Step 5 (Tier 2): Multimodal enhancement — vision LLM sees the images
# ---------------------------------------------------------------------------

_VISION_BATCH_SIZE = 4
_VISION_SKIP_EXTENSIONS = {".svg"}

ENHANCE_IMAGES_PROMPT = """\
You are enhancing annotations for educational diagrams in a teaching wiki.

Each image already has a TEXT-BASED annotation derived from the blog's \
surrounding text. Now you can SEE the actual image. Your job is to add \
what only the image itself can tell you.

PAGE: {page_title}
SOURCE: {page_url}

IMAGES AND THEIR CURRENT ANNOTATIONS:
{images_section}

For each image, return:
{{
  "images": [
    {{
      "index": <image number from above>,
      "description": "Enhanced — what you SEE in the image, be specific",
      "teaching_value": "How this specific visual helps learning",
      "concepts": ["concept1", "concept2"],
      "visual_details": "Layout, components, arrows, colors, labels, \
notation — things only visible from the image itself"
    }}
  ]
}}

GUIDELINES:
- 'visual_details' is the KEY field — describe the image structure: \
  "3 parallel paths labeled Q, K, V feeding into a Concat block, \
  with MatMul and Scale steps shown as separate boxes in sequence"
- If the existing description is already good, keep it and focus on \
  adding visual_details
- Note any mathematical notation, axis labels, color-coding schemes
- Describe flow direction (left-to-right, top-to-bottom)
- Count components when relevant ("6 stacked encoder blocks")

Return ONLY valid JSON.
"""


def _image_to_base64_url(file_path: Path) -> str | None:
    """Read an image file and return a base64 data URL for the vision API."""
    if not file_path.exists():
        return None

    mime_map = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime = mime_map.get(file_path.suffix.lower())
    if not mime:
        return None

    b64 = base64.b64encode(file_path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


async def _call_vision_llm(
    messages: list[dict],
    *,
    max_tokens: int = 4096,
    temperature: float = 0.0,
    model: str | None = None,
) -> str:
    """Multimodal LLM call with image content blocks."""
    import httpx
    from ..config import get_settings

    settings = get_settings()
    resolved_model = (
        model
        or getattr(settings, "vision_llm_model", None)
        or settings.llm_model
    )

    headers = {
        "Authorization": f"Bearer {settings.llm_api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": resolved_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            f"{settings.llm_base_url}/chat/completions",
            headers=headers,
            json=payload,
        )
        if resp.status_code != 200:
            logger.error("Vision LLM returned %s: %s", resp.status_code, resp.text[:300])
        resp.raise_for_status()

    content = resp.json()["choices"][0]["message"]["content"].strip()
    logger.info("Vision LLM call: model=%s, response=%d chars", resolved_model, len(content))
    return content


async def _process_vision_batch(
    img_dir: Path,
    batch: list[dict],
    page_title: str,
    page_url: str,
    *,
    model: str | None = None,
    detail: str = "low",
) -> list[dict]:
    """Run one batch of images through the vision model."""

    images_section = ""
    for i, entry in enumerate(batch, 1):
        label = entry.get("file") or entry.get("source_url", f"image-{i}")
        images_section += (
            f"\n--- IMAGE {i}: {label} ---\n"
            f"Current description: {entry.get('description', '(none)')}\n"
            f"Current teaching_value: {entry.get('teaching_value', '(none)')}\n"
            f"Current concepts: {', '.join(entry.get('concepts', []))}\n"
        )

    prompt_text = ENHANCE_IMAGES_PROMPT.format(
        page_title=page_title,
        page_url=page_url,
        images_section=images_section,
    )

    # Interleave text references with image blocks.
    # Use local file (base64) when available, fall back to source URL directly.
    content_blocks: list[dict] = [{"type": "text", "text": prompt_text}]

    for i, entry in enumerate(batch, 1):
        label = entry.get("file") or entry.get("source_url", f"image-{i}")
        image_url_value: str | None = None

        local_file = entry.get("file")
        if local_file:
            file_path = img_dir / local_file
            image_url_value = _image_to_base64_url(file_path)

        if image_url_value is None:
            src = entry.get("source_url", "")
            if src.startswith("http"):
                image_url_value = src

        if image_url_value:
            content_blocks.append({
                "type": "text",
                "text": f"\n[Image {i}: {label}]",
            })
            content_blocks.append({
                "type": "image_url",
                "image_url": {"url": image_url_value, "detail": detail},
            })

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert at analyzing educational diagrams and "
                "technical illustrations. Return ONLY valid JSON."
            ),
        },
        {"role": "user", "content": content_blocks},
    ]

    raw = await _call_vision_llm(messages, max_tokens=4096, model=model)

    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

    result = json.loads(text)
    return result.get("images", [])


async def enhance_images_multimodal(
    topic_slug: str,
    *,
    source_page_url: str | None = None,
    batch_size: int = _VISION_BATCH_SIZE,
    model: str | None = None,
    detail: str = "low",
) -> dict:
    """Tier-2: vision LLM enhances text-based annotations.

    Looks at the actual downloaded images and adds ``visual_details``
    plus any corrections to description/concepts/teaching_value.

    Args:
        topic_slug: wiki topic containing the images
        source_page_url: limit to images from this page (None = all)
        batch_size: images per vision API call (default 4)
        model: vision-capable model ID (falls back to settings)
        detail: ``"low"`` (85 tokens/img) or ``"high"`` (more detail)

    Returns summary with counts of enhanced/skipped/errored images.
    """
    img_dir = _images_dir(topic_slug)
    entries = load_images_json(topic_slug)

    if not entries:
        return {"status": "no_images", "total": 0}

    # Collect processable images — include url-only entries (no local file)
    # since the vision API can fetch images directly from source URLs.
    to_process: list[dict] = []
    for entry in entries:
        if entry.get("visual_details"):
            continue
        file_name = entry.get("file") or ""
        ext = Path(file_name).suffix.lower() if file_name else ""
        if ext in _VISION_SKIP_EXTENSIONS:
            continue
        if source_page_url and entry.get("source_page") != source_page_url:
            continue
        has_local = bool(file_name) and (img_dir / file_name).exists()
        has_url = bool(entry.get("source_url", "").startswith("http"))
        if not has_local and not has_url:
            continue
        to_process.append(entry)

    if not to_process:
        already = sum(1 for e in entries if e.get("visual_details"))
        return {"status": "nothing_to_enhance", "total": len(entries),
                "already_enhanced": already}

    # Group by source page for coherent prompts
    by_page: dict[str, list[dict]] = {}
    for entry in to_process:
        page = entry.get("source_page", "unknown")
        by_page.setdefault(page, []).append(entry)

    enhanced_count = 0
    error_count = 0
    batch_count = 0

    for page_url, page_entries in by_page.items():
        page_title = page_entries[0].get("source_author", "") or page_url

        for batch_start in range(0, len(page_entries), batch_size):
            batch = page_entries[batch_start : batch_start + batch_size]
            batch_count += 1

            try:
                enhancements = await _process_vision_batch(
                    img_dir, batch, page_title, page_url,
                    model=model, detail=detail,
                )

                for enh in enhancements:
                    idx = enh.get("index", 0) - 1
                    if not (0 <= idx < len(batch)):
                        continue
                    target_file = batch[idx]["file"]
                    for e in entries:
                        if e["file"] != target_file:
                            continue
                        if enh.get("description"):
                            e["description"] = enh["description"]
                        if enh.get("teaching_value"):
                            e["teaching_value"] = enh["teaching_value"]
                        if enh.get("concepts"):
                            e["concepts"] = enh["concepts"]
                        if enh.get("visual_details"):
                            e["visual_details"] = enh["visual_details"]
                        e["multimodal_enhanced"] = True
                        enhanced_count += 1
                        break

            except Exception as exc:
                logger.warning(
                    "Vision batch %d failed for %s: %s",
                    batch_count, topic_slug, exc,
                )
                error_count += len(batch)

    if enhanced_count > 0:
        _save_images_json(topic_slug, entries)

    logger.info(
        "Multimodal enhancement for %s: %d enhanced, %d errors, %d batches",
        topic_slug, enhanced_count, error_count, batch_count,
    )
    return {
        "status": "ok",
        "total": len(entries),
        "processed": len(to_process),
        "enhanced": enhanced_count,
        "errors": error_count,
        "batches": batch_count,
    }
