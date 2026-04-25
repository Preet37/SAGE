# Card: DALL·E 3 — model-specific constraints, pricing, rate limits
**Source:** https://platform.openai.com/docs/models/dall-e-3  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Model-specific behavior/constraints for DALL·E 3 (supported endpoints, sizes, pricing, rate limits)

## Key Content
- **What DALL·E 3 does:** Generates a **new image from a text prompt**; “currently supports… create a new image with a specific size.”
- **Modalities / capabilities**
  - **Input:** Text only  
  - **Output:** Image only  
  - **Not supported:** Audio, Video
- **Endpoints listed for image workflows**
  - **Image generation:** `v1/images/generations`
  - **Image edit:** `v1/images/edits`
- **Supported output sizes (and used for pricing tiers)**
  - `1024x1024`
  - `1024x1536`
  - `1536x1024`
- **Pricing (per image)**
  - **Standard quality**
    - `1024x1024`: **$0.04**
    - `1024x1536`: **$0.08**
    - `1536x1024`: **$0.08**
  - **HD quality**
    - `1024x1024`: **$0.08**
    - `1024x1536`: **$0.12**
    - `1536x1024`: **$0.12**
  - **Quick comparison (Standard, 1024x1024):** DALL·E 3 **$0.04** vs DALL·E 2 **$0.02**
- **Rate limits (images per minute, RPM)**
  - Free: **Not supported**
  - Tier 1: **500 img/min**
  - Tier 2: **2500 img/min**
  - Tier 3: **5000 img/min**
  - Tier 4: **7500 img/min**
  - Tier 5: **10000 img/min**
- **Model naming / snapshots:** Alias/snapshot shown as `dall-e-3` (marked “Deprecated” in the listing).

## When to surface
Use when students ask which parameters/sizes are supported for DALL·E 3, what it costs per image (Standard vs HD), which endpoints to call for generation vs edits, or what rate limits apply by usage tier.