# Card: Sora Videos API (create/poll/download, refs, edits, extensions)
**Source:** https://platform.openai.com/docs/guides/video-generation  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Concrete request/response schema + constraints for production text-to-video usage

## Key Content
- **Deprecation:** Sora 2 video generation models + Videos API shut down **Sep 24, 2026** (affects **/videos**, models **sora-2**, **sora-2-pro**, **sora-2-2025-10-06**, **sora-2-2025-12-08**, **sora-2-pro-2025-10-06**).
- **Models & capabilities:**  
  - **sora-2** = faster iteration; **sora-2-pro** = higher fidelity, production quality; use pro for **1080p exports (1920×1080 or 1080×1920)**.  
  - Both support **16s and 20s** generations.
- **Core async workflow (Videos API):**
  1) **POST `/v1/videos`** → returns job object `{id, status, model, progress, seconds, size}` (status: **queued/in_progress/completed/failed**).  
  2) Poll **GET `/v1/videos/{video_id}`** (suggested **10–20s** interval; exponential backoff). Or use **webhooks**.  
  3) When **completed**, download MP4 via **GET `/v1/videos/{video_id}/content`**. Download URLs valid **≤ 1 hour**.
- **Webhooks:** event types **`video.completed`** and **`video.failed`**; payload includes `data.id` = video job id.
- **Supporting assets:** `/content?variant=thumbnail` (webp) or `variant=spritesheet` (jpg); default `variant=video`.
- **Image reference (first frame conditioning):** `input_reference` with **jpeg/png/webp**; must **match target `size`**. JSON form accepts `{file_id}` or `{image_url}`; multipart supports file upload.
- **Characters (consistency):** upload MP4 to **POST `/v1/videos/characters`**, then include `characters: [{id: "char_..."}]` and **mention character name verbatim in prompt**. Best: **2–4s**, **16:9 or 9:16**, **720p–1080p**; **max 2 characters**. **No characters in extensions.**
- **Extensions:** **POST `/v1/videos/extensions`** with source `{video:{id}}` + prompt; each adds **≤20s**; extend **≤6 times** → **max total 120s**; **no characters/image refs**.
- **Edits:** **POST `/v1/videos/edits`** with `{video:{id}}` (model inferred) + prompt; if uploading video, set `model` explicitly. Remix endpoint deprecated.
- **Batch:** supports **POST `/v1/videos` only**, **JSON only** (no multipart); upload assets first; batch outputs downloadable **≤24h**.
- **Library mgmt:** **GET `/v1/videos`** supports `limit`, `after`, `order`; **DELETE `/v1/videos/{video_id}`**.
- **Guardrails:** only **<18-suitable** content; **copyrighted characters/music rejected**; **no real people/public figures**; human-likeness character uploads blocked by default; **input images with human faces rejected**.

## When to surface
Use when students ask how to call Sora via API (endpoints, polling vs webhooks, download variants), or about hard constraints (durations, resolutions, extensions limits, Batch limitations, and safety/eligibility restrictions).