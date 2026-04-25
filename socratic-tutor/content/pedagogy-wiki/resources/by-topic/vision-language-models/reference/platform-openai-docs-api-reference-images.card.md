# Card: OpenAI Images API (Generate/Edit/Variations) — schema & params
**Source:** https://platform.openai.com/docs/api-reference/images  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact parameter names, request/response schema, and documented defaults/constraints for image endpoints

## Key Content
- **Endpoints (Images):**
  - **Generate an Image**: `POST /v1/images/generations`
  - **Edit an Image**: `POST /v1/images/edits`
  - **Create Variation**: `POST /v1/images/variations`
  - Also documented: **streaming events** for image generation/edit (see “Image generation streaming events”, “Image edit streaming events” in the Images section).
- **Core request fields (by operation):**
  - **Generate**: `model`, `prompt`, optional controls such as `n`, `size`, `response_format`, `user` (exact availability/allowed values are specified per endpoint in the reference).
  - **Edit**: multipart form with `image` (input image), optional `mask`, plus `prompt`, `model`, and other optional controls (e.g., `n`, `size`, `response_format`, `user`) as listed in the endpoint schema.
  - **Variation**: multipart form with `image` (input image), plus `model` and optional controls (`n`, `size`, `response_format`, `user`) per schema.
- **Response schema (common pattern):**
  - Returns an object containing a `data` array of generated items; each item includes image output payload (commonly `url` or base64 content depending on `response_format`, per endpoint docs).
- **Procedure/workflow (implementation):**
  1. Choose operation (generate/edit/variation) and **model**.
  2. Provide required inputs (`prompt` for generate/edit; `image` for edit/variation; optional `mask` for edit).
  3. Set output controls (`n`, `size`, `response_format`) as needed.
  4. Parse `data[]` in the response; handle streaming events if using streaming.

## When to surface
Use when students ask “Which endpoint/parameters do I use for image generation vs editing/variations?”, “What’s the exact request/response JSON (or multipart) schema?”, or “What defaults/allowed values exist for `size`, `n`, `response_format`, etc.?”