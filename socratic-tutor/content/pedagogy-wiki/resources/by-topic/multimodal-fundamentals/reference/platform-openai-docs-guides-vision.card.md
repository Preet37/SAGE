# Card: Vision inputs & image token costs (Node/Responses API)
**Source:** https://platform.openai.com/docs/guides/vision?lang=node  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Copy-pastable patterns + concrete limits/cost formulas for image+text requests and image sizing/tokenization

## Key Content
- **Send image + text (Responses API pattern):** `input` is an array of messages; each message `content` can mix:
  - `{type:"input_text", text:"..."}` and `{type:"input_image", image_url:"https://..."}`.
- **Image input methods:** (1) fully-qualified URL, (2) Base64 data URL, (3) `file_id` (via Files API). Multiple images allowed; **images count as tokens**.
- **Image requirements:** types **PNG/JPEG/WEBP/non-animated GIF**; **≤512 MB total payload/request**; **≤1500 images/request**; **no watermarks/logos**, **no NSFW**, must be human-legible.
- **Detail parameter (default = `auto`):** `low | high | original | auto`.
  - `low`: model sees **512×512** version (fast/cheap).
  - `high`: standard high-fidelity.
  - `original`: for **large/dense/spatial/computer-use** images; recommended for click-accuracy on **gpt-5.4+**.
- **Patch-based tokenization (32×32 patches) (Eq.1–4):**
  - **Eq.1** `original_patch_count = ceil(w/32) * ceil(h/32)`
  - If over patch budget, shrink: **Eq.2** `shrink_factor = sqrt((32^2 * patch_budget)/(w*h))`
  - **Eq.3** `adjusted_shrink_factor = shrink_factor * min(floor(w*shrink/32)/(w*shrink/32), floor(h*shrink/32)/(h*shrink/32))`
  - **Eq.4** `resized_patch_count = ceil(w’/32) * ceil(h’/32)`; then **tokens = resized_patch_count * multiplier** (capped by budget).
  - Multipliers: **1.62** (gpt-5.4-mini, gpt-5-mini, gpt-4.1-mini snapshot), **2.46** (…-nano), **1.72** (o4-mini).
  - Example (budget 1536): **1024×1024 → 1024 patches**; **1800×2400 → resized 1056×1408 → 1452 patches**.
- **Tile-based tokenization (GPT-4o/4.1/4o-mini/o1/o3/computer-use-preview):**
  - `detail:"low"` = fixed base tokens (model-specific).
  - `detail:"high"`: scale to fit **2048×2048**, then shortest side **768px**, count **512px tiles**; **total = base + tiles*tile_tokens**.
  - Table rows: **4o/4.1/4.5 base 85, tile 170**; **o1/o1-pro/o3 base 75, tile 150**; **computer-use-preview base 65, tile 129**; **gpt-5 base 70, tile 140**; **4o-mini base 2833, tile 5667**.
- **GPT Image 1 input cost:** like tile-based but shortest side **512px**; low fidelity **base 65, tile 129**; high fidelity adds **+4160** (square) or **+6240** (portrait/landscape-ish).

## When to surface
Use when students ask how to structure multimodal requests (text+image), choose `detail`, or estimate/compare image token costs and resizing behavior across model families.