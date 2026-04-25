# Card: OpenAI Vision Inputs (Schemas, Detail Levels, Token Cost)
**Source:** https://platform.openai.com/docs/guides/images-vision  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official request/response patterns for sending images to vision-capable models (URL/base64/file_id), `detail` behavior, and image tokenization constraints.

## Key Content
- **Send images to models (3 methods):**
  - **URL**: provide fully qualified image URL.
  - **Base64 data URL**: `data:image/jpeg;base64,{BASE64}`.
  - **File ID**: upload via Files API with `purpose:"vision"`, then reference `file_id`.
- **Chat Completions schema (image input):** message `content` array with parts:
  - `{ "type":"text", "text":"..." }`
  - `{ "type":"image_url", "image_url": { "url":"...", "detail":"auto|low|high|original" } }`
- **Responses API schema (image input):** `input` array of items; user `content` parts:
  - `{ "type":"input_text", "text":"..." }`
  - `{ "type":"input_image", "image_url":"..." , "detail":"..." }` or `{ "type":"input_image", "file_id":"..." }`
- **Image input requirements:**
  - Types: PNG, JPEG/JPG, WEBP, **non-animated** GIF
  - Limits: **512 MB total payload/request**, **1500 images/request**
  - Other: no watermarks/logos, no NSFW, must be human-legible
- **`detail` parameter (default = `auto`):**
  - `low`: model gets **512×512** low-res (fast/cheap)
  - `high`: standard high-fidelity understanding
  - `original`: for large/dense/spatially sensitive/computer-use images; available on **gpt-5.4+**
- **Model resizing/patch budgets (32×32 patch-based families):**
  - `gpt-5.4`+: `high` ≤ **2,500 patches** or **2048px max dim**; `original` ≤ **10,000 patches** or **6000px max dim**
  - `gpt-5-mini/nano`, `o4-mini`, `gpt-4.1-mini/nano (2025-04-14)` : `high` ≤ **1,536 patches** or **2048px max dim**
- **Patch token cost formula (Section: Patch-based tokenization):**
  - **Eq.1** `original_patch_count = ceil(width/32) * ceil(height/32)`
  - If over budget, scale down:  
    **Eq.2** `shrink_factor = sqrt((32^2 * patch_budget)/(width*height))`  
    **Eq.3** `adjusted_shrink_factor = shrink_factor * min( floor(width*shrink_factor/32)/(width*shrink_factor/32), floor(height*shrink_factor/32)/(height*shrink_factor/32) )`
  - **Eq.4** `resized_patch_count = ceil(resized_width/32) * ceil(resized_height/32)` (capped by budget)
  - **Eq.5 billed_tokens = resized_patch_count * multiplier**
    - Multipliers: `gpt-5.4-mini` **1.62**, `gpt-5.4-nano` **2.46**, `gpt-5-mini` **1.62**, `gpt-5-nano` **2.46**, `gpt-4.1-mini*` **1.62**, `gpt-4.1-nano*` **2.46**, `o4-mini` **1.72**
- **Worked examples (1,536 patch budget):**
  - 1024×1024 → patch count **1024** (no resize)
  - 1800×2400 → resized to **1056×1408**, patch count **1452**

## When to surface
Use when students ask how to pass images to OpenAI models (URL vs base64 vs file_id), what `detail` does, payload limits, or how image token costs/resizing are computed.