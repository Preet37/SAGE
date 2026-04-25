# Pocket Tutor → Melange (mobile / on-device) deployment

This is the recipe for taking SAGE's distilled tutor model and deploying it
to a real end-user phone (CPU / GPU / NPU) via [Zetic Melange](https://melange.zetic.ai/).
The web Pocket Tutor (`/pocket`) is the in-browser counterpart that runs
through WebGPU + WebLLM; this doc covers the native mobile path.

## What runs where

| Task | Runtime | Why on-device |
|---|---|---|
| Q&A on a cached lesson | Llama-3.2-1B / Phi-3.5-mini | Zero-latency response, works offline, no tokens leave the phone |
| Speech-to-text for voice tutoring | Whisper tiny / distil-whisper | Microphone input never leaves the device |
| Comprehension self-check (sentence classifier) | distil-bert / mobilebert | Cheap, frequent — cloud cost would dominate |
| **Cloud fallback only:** | | |
| Web search & paper lookup | SAGE backend (Perplexity) | Requires fresh internet data |
| Heavy reasoning on novel topics | SAGE Cloud Tutor (Groq, llama-3.3-70b) | Larger model only when needed |

## Step 1 — Pick & quantize the base model

Start from a small instruction-tuned base. The Pocket Tutor web demo uses:
- `meta-llama/Llama-3.2-1B-Instruct` (recommended baseline, ~880MB after q4)
- `microsoft/Phi-3.5-mini-instruct` (better step-by-step reasoning, ~1.9GB after q4)

Quantize for mobile:

```bash
pip install transformers optimum onnxruntime
optimum-cli export onnx \
  --model meta-llama/Llama-3.2-1B-Instruct \
  --task text-generation-with-past \
  --device cpu \
  --quantize int4 \
  out/sage-tutor-1b
```

## Step 2 — Convert with Melange

```bash
pip install zetic-melange
melange compile \
  --model out/sage-tutor-1b/model.onnx \
  --target ios-npu,android-gpu \
  --output dist/sage-tutor-1b.melange
```

Melange will benchmark the model on a connected device or simulator and
emit a single `.melange` bundle that contains the weights plus per-target
kernels for CPU, GPU, and NPU.

## Step 3 — Embed in the mobile companion

For an iOS / Android wrapper around the SAGE web app:

```swift
// iOS — load the bundle and wire it to a UITextView
let melange = try MelangeRuntime(contentsOf: bundleURL("sage-tutor-1b.melange"))
let response = try await melange.generate(
  prompt: question,
  system: SAGE_POCKET_SYSTEM_PROMPT,
  maxTokens: 256
)
```

```kotlin
// Android — same idea
val melange = Melange.load(context, "sage-tutor-1b.melange")
val response = melange.generate(question, SAGE_POCKET_SYSTEM_PROMPT, 256)
```

## Step 4 — Cloud handoff

The mobile app should detect when the question requires fresh information
(e.g. user types "latest paper on X", or the on-device model emits low
confidence) and POST to the existing SAGE Cloud Tutor:

```
POST  https://<your-sage-host>/tutor/chat
Authorization: Bearer <jwt>
Body:  { "lesson_id": "...", "messages": [...] }
```

This gives the user the **best of both**: instant private answers for the
common case, with a clear, observable handoff when the cloud is genuinely
needed. The same handoff pattern is what the web Pocket Tutor links to via
the "use Cloud Tutor instead" button.

## Benchmarks to record

For the demo, capture these numbers via Melange's bench tool and surface
them in the UI:

```bash
melange bench dist/sage-tutor-1b.melange --target ios-npu --prompt-tokens 128 --gen-tokens 128
```

Report: time-to-first-token, tokens/sec, peak memory, total energy.
The web Pocket Tutor already shows tokens/sec live so judges can compare.
