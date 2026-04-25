# Card: Images API (Generate/Edit/Variations) — DALL·E 3 parameter constraints
**Source:** https://platform.openai.com/docs/api-reference/images?lang=node.js  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Images endpoints + request/response schema; DALL·E 3 constraints/defaults (sizes, quality, etc.)

## Key Content
- **Endpoints (Images resource)**
  - **Generate an image:** `POST /v1/images/generations`
  - **Edit an image:** `POST /v1/images/edits`
  - **Create variation:** `POST /v1/images/variations`
  - Streaming event specs exist for generation/edit (see “Image generation streaming events”, “Image edit streaming events” in API reference nav).

- **Core request fields (Generate)**
  - `model`: image model identifier (e.g., DALL·E 3).
  - `prompt`: text prompt describing desired image.
  - `n`: number of images to generate (commonly `1` for DALL·E 3).
  - `size`: **allowed (DALL·E 3):** `1024x1024`, `1024x1792`, `1792x1024`.
  - `quality`: **default:** `"standard"`; **option:** `"hd"`.
  - `response_format`: typically `"url"` or `"b64_json"` (controls whether you receive hosted URLs or base64 payloads).
  - `user`: optional end-user identifier for tracking/abuse monitoring.

- **Edit workflow (inpainting/outpainting)**
  - Provide an `image` plus optional `mask` (mask indicates editable region), along with `prompt` and other generation params (e.g., `size`, `response_format`).

- **Response schema (common)**
  - Returns an object with a `data` array; each element contains either a `url` (if `response_format="url"`) or `b64_json` (if `response_format="b64_json"`).

## When to surface
Use this card when students ask: “What sizes/quality options does DALL·E 3 support?”, “What are the Images API endpoints and required fields?”, or “How do I do inpainting/outpainting via the edit endpoint and mask?”