# Card: Whisper Audio Transcription — Create Endpoint
**Source:** https://platform.openai.com/docs/api-reference/whisper/create  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Whisper transcription endpoint parameters and defaults (model, response_format, temperature, language, timestamp granularities) + request/response schema.

## Key Content
- **Endpoint (Audio → Text):** Create a transcription by uploading an audio file and selecting a Whisper model.
- **Core request fields (multipart form):**
  - `file` (required): audio file upload.
  - `model` (required): Whisper model identifier to use for transcription.
- **Optional request parameters (common controls):**
  - `language`: ISO language code to bias/force transcription language (improves accuracy/latency when known).
  - `prompt`: text prompt to guide style/terminology (useful for names, jargon).
  - `response_format`: output format selector (e.g., plain text vs structured JSON variants).
  - `temperature`: sampling temperature for decoding; lower = more deterministic, higher = more varied.
  - `timestamp_granularities`: controls whether timestamps are returned and at what granularity (e.g., segment- and/or word-level timestamps) when using structured formats.
- **Response schema (varies by `response_format`):**
  - Text formats return the transcript as text.
  - JSON formats return structured objects (e.g., transcript text plus timing/segment metadata when timestamps enabled).
- **Procedure/workflow:**
  1. Send multipart request with `file` + `model`.
  2. Optionally set `language`, `prompt`, `temperature`, `response_format`.
  3. If you need timings, choose a structured `response_format` and set `timestamp_granularities`.
  4. Parse response according to chosen format (text vs JSON with segments/words).

## When to surface
Use when students ask how to call Whisper transcription in the OpenAI API, what parameters control output format/timestamps/language, or how to structure requests and parse responses for captions/subtitles in text-to-video pipelines.