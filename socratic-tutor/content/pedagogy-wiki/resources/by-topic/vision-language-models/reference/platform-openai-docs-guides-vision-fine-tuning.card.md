# Card: Vision fine-tuning — dataset format + constraints
**Source:** https://platform.openai.com/docs/guides/vision-fine-tuning  
**Role:** reference_doc | **Need:** WORKING_EXAMPLE  
**Anchor:** End-to-end procedure for vision fine-tuning: dataset format expectations, training workflow, and operational constraints

## Key Content
- **What it is / model:** Vision fine-tuning = **supervised fine-tuning (SFT)** with **image inputs** to improve image understanding; best for **image classification** and **fixing instruction-following failures on complex prompts**. Use with **`gpt-4o-2024-08-06`**.
- **Training data format (JSONL):** Each line is a JSON object with `"messages"` (chat-style). Image inputs appear in a user message as a **content array** containing objects like:  
  - `{ "type": "image_url", "image_url": { "url": "<http(s) URL or data URL base64>" } }`  
  - Images may be **HTTP URLs** or **data URLs (Base64)**.  
  - **Constraint:** You **cannot** include images in messages with the **`assistant`** role (images are inputs only).
- **Image data requirements (hard limits):**
  - Max **50,000** examples that contain images (text-only examples not counted).
  - Max **10 images per example**.
  - Max **10 MB per image**.
  - Formats: **JPEG, PNG, WEBP** only.
  - Color mode: **RGB or RGBA**.
- **Content moderation filtering (pre-training scan):** Images containing **people, faces, children, CAPTCHAs** are **excluded** (and may add latency during validation).
  - Common skip reasons + fixes: inaccessible URL → make public; too large → meet size limits; invalid format → meet format rules; contains restricted entities → remove image.
- **Cost/quality control via `detail` parameter (per image):**
  - `detail: "low"` → image resized to **512×512** and represented by **85 tokens** regardless of original size (reduces training cost).
  - `detail` can be **`low` / `high` / `auto`**; affects fidelity + token count + cost.
- **Post-training safety gate:** Completed fine-tuned models are evaluated across **13 safety categories**; each has a pass threshold; failing categories can **block deployment**. Debug via fine-tuning **events** endpoint; look for event type **`moderation_checks`**.

## When to surface
Use when a student asks how to **format vision fine-tuning JSONL**, what **image limits/allowed formats** are, how to **reduce cost with `detail`**, or why images might be **skipped/blocked** (moderation + safety checks).