# Card: Azure Speech TTS SSML surface (voice, prosody, style, audio)
**Source:** https://learn.microsoft.com/en-us/azure/ai-services/speech-service/speech-synthesis-markup-voice  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact SSML elements/attributes for Azure Speech TTS: required `<voice>` in `<speak>`, multi-voice docs, prosody/emphasis/style/role/lang/audio/backgroundaudio/audioduration/viseme/voiceconversion.

## Key Content
- **Document rule:** Inside each `<speak ...>` root, **at least one** `<voice>` element is required; you can include **multiple** `<voice>` blocks (different voices/languages/settings).
- **`<voice>` attributes:**  
  - `name` = voice name (or **custom voice model name**).  
  - `effect` (optional): `eq_car` (car/bus enclosed auto playback compensation), `eq_telecomhp8k` (telecom narrowband; **use 8 kHz** sampling rate). Missing/invalid → ignored.
- **Multi-talker:** Use `<voice name='en-US-MultiTalker-Ava-Andrew:DragonHDLatestNeural'><mstts:dialog><mstts:turn speaker="ava|andrew">...</mstts:turn>...</mstts:dialog></voice>`.
- **Styles/roles:** `<mstts:express-as style="..." styledegree="..." role="...">`  
  - `style` required; invalid/missing → whole element ignored (neutral).  
  - `styledegree` optional **0.01–2** (default **1**).  
  - `role` optional: `Girl|Boy|YoungAdultFemale|YoungAdultMale|OlderAdultFemale|OlderAdultMale|SeniorFemale|SeniorMale`.
- **Language override (multilingual voices only):** `<lang xml:lang="locale">...</lang>`; `xml:lang` required. Non-multilingual voices don’t support `<lang>`. `<speak>` default language must be `xml:lang="en-US"` in examples.
- **Prosody:** `<prosody pitch|contour|range|rate|volume>`  
  - **Rate:** multiplier **0.5–2** or `%` or constants `x-slow/slow/medium/fast/x-fast`.  
  - **Pitch:** absolute `Hz`, relative `+/-Hz` or `+/-st`, `%`, or constants `x-low/low/medium/high/x-high` (~0.55…1.45).  
  - **Volume:** absolute **0.0–100.0** (default **100.0**), relative `+/-`, `%`, or constants `silent…x-loud`.
- **Emphasis:** `<emphasis level="reduced|none|moderate|strong">` (default **moderate**); word-level emphasis only for **en-US-GuyNeural, en-US-DavisNeural, en-US-JaneNeural**.
- **Insert audio:** `<audio src="https://...">fallback text/SSML</audio>`; formats: **mp3/wav/opus/ogg/flac/wma**; total response (text+audio) **≤600s**; HTTPS required.
- **Audio duration control:** `<mstts:audioduration value="20s|2000ms"/>` applies to enclosing `<voice>`; allowed scaling **0.5–2×** original; **max 300s** output.
- **Background audio:** `<mstts:backgroundaudio .../>` must be **first child of `<speak>`**; only **one** per SSML. `volume 0–100` (default **1**), `fadein/fadeout 0–10000 ms` (default **0**).
- **Visemes:** `<mstts:viseme type="redlips_front|FacialExpression"/>` (locale limits: redlips_front en-US; FacialExpression en-US & zh-CN).
- **Voice conversion (preview):** `<mstts:voiceconversion url="https://..."/>` input audio **<100 MB**; **ignores** SSML prosody/pronunciation and any text; target voice set by `<voice name="...">`.

## When to surface
Use when students ask “How do I write SSML for Azure TTS to change voice/style/rate/pitch/volume/accent, mix audio, add background music, control duration, get visemes, or do voice conversion/multi-speaker dialogue?”