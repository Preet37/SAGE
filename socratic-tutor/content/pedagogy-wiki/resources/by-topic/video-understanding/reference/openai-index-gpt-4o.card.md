# Card: GPT‑4o multimodal (incl. video) capability anchor
**Source:** https://openai.com/index/gpt-4o/  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Official top-level statements on GPT‑4o modality handling (text/audio/image/video), rollout status, and latency/cost/rate-limit comparisons.

## Key Content
- **Multimodal I/O claim (core spec):** GPT‑4o (“omni”) *“accepts as input any combination of text, audio, image, and video and generates any combination of text, audio, and image outputs.”* (Video is explicitly listed as **input**; outputs listed: text/audio/image.)
- **Latency (audio):** Responds to audio inputs in **as little as 232 ms**, **avg 320 ms** (human-like conversational timing).
- **Prior Voice Mode pipeline (procedure):** 3-model chain:  
  1) audio→text transcription model → 2) GPT‑3.5/GPT‑4 text-in/text-out → 3) text→audio model.  
  **Rationale:** This pipeline loses information (can’t directly observe **tone**, **multiple speakers**, **background noises**) and can’t output **laughter/singing/emotion**.
- **GPT‑4o design change (procedure/rationale):** Trained **end-to-end** as a **single neural network** across **text, vision, audio** so all inputs/outputs are processed by the same network (preserves paralinguistic/audio context).
- **API availability + rollout status:** Developers can access GPT‑4o in the API **as a text and vision model**; OpenAI planned to launch **audio and video** API support to a **small group of trusted partners** “in the coming weeks” (from May 13, 2024 post).
- **Cost/speed/rate limits (empirical comparisons):** **2× faster**, **50% cheaper**, and **5× higher rate limits** vs **GPT‑4 Turbo** (API).

## When to surface
Use when students ask whether GPT‑4o supports **video/audio**, what modalities are **input vs output**, or need **official numbers** for latency, cost, speed, and rollout status for video/audio in the API.