# Card: Images & Vision API (schema + image handling + costs)
**Source:** https://platform.openai.com/docs/guides/images-vision?api-mode=chat  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact request/response schema variants, image input handling (URL/base64/file_id), detail levels, resizing + token cost rules, constraints/limits

## Key Content
- **Endpoints & use cases**
  - **Responses API:** analyze images as input and/or generate images as output (via tools).
  - **Chat Completions API:** analyze images → generate text/audio.
  - **Images API:** generate images (optionally with image inputs).
- **Image input methods (Responses/Chat):** provide **(1)** fully-qualified **URL**, **(2)** **Base64 data URL**, or **(3)** **file_id** (Files API). Multiple images allowed; **images count as tokens**.
- **Responses API schema (vision input):** `input=[{"role":"user","content":[{"type":"input_text","text":...},{"type":"input_image","image_url":...,"detail":...}]}]`
- **Image requirements/limits**
  - Types: **PNG, JPEG/JPG, WEBP, non-animated GIF**
  - Limits: **≤512 MB total payload/request**, **≤1500 images/request**
  - Other: **no watermarks/logos**, **no NSFW**, must be **human-legible**; **CAPTCHAs blocked**
- **Detail parameter (default = auto):** `"low" | "high" | "original"(gpt-5.4+) | "auto"`
  - **low:** 512×512 proxy; faster/cheaper
  - **original:** for dense/spatial/computer-use; recommended for click-accuracy on **gpt-5.4+**
- **Patch-based tokenization (Eq.1–4)**
  - **Eq.1:** `original_patch_count = ceil(w/32)*ceil(h/32)`
  - If over **patch_budget**, shrink:  
    **Eq.2:** `shrink_factor = sqrt((32^2*patch_budget)/(w*h))`  
    **Eq.3:** `adjusted_shrink_factor = shrink_factor * min(floor(w*shrink/32)/(w*shrink/32), floor(h*shrink/32)/(h*shrink/32))`
  - **Eq.4:** `resized_patch_count = ceil(w’/32)*ceil(h’/32)`; billed tokens = `resized_patch_count * multiplier`
  - Multipliers: **gpt-5.4-mini 1.62; gpt-5.4-nano 2.46; gpt-5-mini 1.62; gpt-5-nano 2.46; gpt-4.1-mini(2025-04-14) 1.62; gpt-4.1-nano(2025-04-14) 2.46; o4-mini 1.72**
  - Patch budgets/resizing: **high** up to **1536 patches or 2048px max dim** (many minis); **gpt-5.4+ original** up to **10,000 patches or 6000px max dim**
- **Tile-based tokenization (GPT-4o/4.1/4o-mini/o1/o3/computer-use-preview)**
  - For `"high"`: scale to fit **2048×2048**, then shortest side **768px**, count **512px tiles**, add base tokens.
  - Base/tile tokens: **gpt-5: 70/140; 4o/4.1/4.5: 85/170; 4o-mini: 2833/5667; o1/o1-pro/o3: 75/150; computer-use-preview: 65/129**
  - **GPT Image 1:** like tile-based but shortest side **512px**; low fidelity base **65** + tile **129**; high fidelity adds **+4160** (square) or **+6240** (portrait/landscape-ish).

## When to surface
Use when students ask how to **send images** (URL/base64/file_id), choose **detail levels**, understand **limits**, or estimate **vision token costs/resizing behavior** across model families/endpoints.