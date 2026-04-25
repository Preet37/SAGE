## Key Facts & Specifications

### Anthropic Claude “computer use” tool (API)
- **Recommended safety setup**
  - Use a **dedicated virtual machine or container with minimal privileges** to reduce risk of system attacks/accidents. (Anthropic Claude API Docs, “Computer use tool”: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
  - **Avoid giving the model access to sensitive data** (e.g., account login information). (Anthropic Claude API Docs: same URL)
  - **Limit internet access to an allowlist of domains** to reduce exposure to malicious content. (Anthropic Claude API Docs: same URL)
  - **Ask a human to confirm** decisions with meaningful real-world consequences and tasks requiring affirmative consent (examples given: **accepting cookies**, **executing financial transactions**, **agreeing to terms of service**). (Anthropic Claude API Docs: same URL)
- **Prompt injection risk**
  - “In some circumstances, Claude will follow commands found in content even if it conflicts with the user's instructions,” including instructions on webpages or in images. (Anthropic Claude API Docs: same URL)
  - Anthropic states the model is trained to resist prompt injections and adds an extra defense layer: **classifiers automatically run on prompts** to flag potential prompt injections; when detected in screenshots, the system **steers the model to ask for user confirmation** before the next action. Opt-out requires contacting support. (Anthropic Claude API Docs: same URL)
- **Data retention**
  - Computer use is described as a **client-side tool**: screenshots, mouse actions, keyboard inputs, and files are captured/stored in **your environment**, not by Anthropic; Anthropic processes screenshots/action requests **in real time** and “does not retain them after the response is returned.” (Anthropic Claude API Docs: same URL)
- **API request parameters shown in docs (example)**
  - Header includes `anthropic-version: 2023-06-01` and beta flag `anthropic-beta: computer-use-2025-11-24`. (Anthropic Claude API Docs: same URL)
  - Example tool config includes:
    - `type: "computer_20251124"`, `display_width_px: 1024`, `display_height_px: 768`, `display_number: 1`. (Anthropic Claude API Docs: same URL)
  - Example model string: `claude-opus-4-6`. (Anthropic Claude API Docs: same URL)
- **Agent loop terminology**
  - Repeating tool-use steps without user input is referred to as the **“agent loop.”** (Anthropic Claude API Docs: same URL)
  - The API response uses `stop_reason: "tool_use"` to signal intent to call a tool. (Anthropic Claude API Docs: same URL)

### OpenAI Images & Vision (Responses API)
- **Supported image input types**
  - File types: **PNG**, **JPEG/JPG**, **WEBP**, **non-animated GIF**. (OpenAI Vision Guide: https://platform.openai.com/docs/guides/vision ; also mirrored at https://developers.openai.com/api/docs/guides/images-vision?api-mode=responses)
- **Size limits**
  - **Up to 50 MB total payload size per request**
  - **Up to 500 individual image inputs per request** (OpenAI Vision Guide: same URLs)
- **Other image requirements**
  - **No watermarks or logos**
  - **No NSFW content**
  - **Clear enough for a human to understand** (OpenAI Vision Guide: same URLs)
- **Image detail control**
  - `detail` parameter supports `low`, `high`, or `auto`; default is `auto` if omitted. (OpenAI Vision Guide: https://platform.openai.com/docs/guides/vision)
  - Using `low` detail: model processes a **512px × 512px** version with a **budget of 85 tokens** (as stated in the guide). (OpenAI Vision Guide: same URL)
- **Endpoints and use cases**
  - **Responses API**: analyze images as input and/or generate images as output.
  - **Images API**: generate images as output (optionally using images as input).
  - **Chat Completions API**: analyze images and use them as input to generate text or audio. (OpenAI Vision Guide: same URLs)

### OmniParser (Microsoft Research, 2024)
- Purpose: a “screen parsing module” that converts UI screenshots into **structured elements** to improve action grounding. (Microsoft OmniParser page: https://microsoft.github.io/OmniParser/ ; Microsoft Research article: https://www.microsoft.com/en-us/research/articles/omniparser-for-pure-vision-based-gui-agent/)
- **Datasets curated (reported sizes)**
  - Interactable icon detection dataset: **67k unique screenshot images** labeled with bounding boxes of interactable icons derived from DOM tree. (OmniParser site: https://microsoft.github.io/OmniParser/)
  - Icon description dataset: **7k icon-description pairs** for fine-tuning the caption model. (OmniParser site: same URL)
- **Benchmarks mentioned**
  - Improves GPT-4V performance on **ScreenSpot**; on **Mind2Web** and **AITW**, OmniParser with **screenshot-only input** outperforms GPT-4V baselines requiring extra information outside the screenshot. (OmniParser site and arXiv HTML: https://arxiv.org/abs/2408.00203 ; https://arxiv.org/html/2408.00203v1)
- **Set-of-Marks (SoM) prompting context**
  - The paper notes GPT-4V is “unable to produce the exact x-y coordinate” and SoM overlays bounding boxes with numeric IDs to ground actions to a box rather than raw coordinates; prior SoM solutions relied on parsed HTML boxes, limiting to web tasks. (OmniParser arXiv HTML: https://arxiv.org/html/2408.00203v1)

### SeeClick (2024)
- SeeClick is a visual GUI agent that **only relies on screenshots** for task automation. (SeeClick arXiv HTML: https://arxiv.org/html/2401.10935v1)
- **ScreenSpot dataset size**
  - “Over **600 screenshots** and **1200 instructions**” spanning iOS, Android, macOS, Windows, and web. (SeeClick arXiv HTML: same URL)
- **GUI grounding metric definition**
  - “Click accuracy” = proportion of samples where predicted location falls inside the ground-truth element bounding box; predicted location is the generated point or the center of a generated bounding box. (SeeClick arXiv HTML: same URL)
- **MiniWob training-data comparison**
  - SeeClick “outperforms the visual baseline Pix2Act with only **0.3% training data** on MiniWob.” (SeeClick arXiv HTML: same URL)
- **AITW click accuracy improvement claim**
  - SeeClick shows an “**8 percentage point improvement** in click accuracy over the LVLM baseline Qwen-VL” (as described in the paper text). (SeeClick arXiv HTML: same URL)

### CogAgent (CVPR 2024 / arXiv 2312.08914)
- Model described as an **18-billion-parameter** VLM specializing in GUI understanding and navigation. (CogAgent arXiv HTML: https://arxiv.org/html/2312.08914v1)
- **Input resolution**
  - Supports **1120 × 1120** input resolution using low- and high-resolution image encoders. (CogAgent arXiv HTML: same URL; CVPR PDF: https://openaccess.thecvf.com/content/CVPR2024/papers/Hong_CogAgent_A_Visual_Language_Model_for_GUI_Agents_CVPR_2024_paper.pdf)
- **Grounding box format**
  - Bounding box format `[[x0,y0,x1,y1]]` with coordinates normalized to **[000,999]**. (CogAgent arXiv HTML: same URL)
- **Pretraining dataset sizes**
  - Visual grounding dataset: **40M images** with image-caption pairs sampled from LAION-115M, associating entities with bounding boxes. (CogAgent arXiv HTML: same URL)
  - CCS400K dataset: **400,000 web page screenshots**; includes visible DOM elements and rendered boxes; supplemented with **140 million** REC and REG QA pairs. (CogAgent arXiv HTML: same URL)
- **Claimed benchmark outcome (qualitative)**
  - Using only screenshots, CogAgent outperforms LLM-based methods consuming extracted HTML on Mind2Web and AITW (stated qualitatively; specific numbers not included in the provided snippet). (CogAgent arXiv HTML: same URL)

### Ferret-UI / Ferret-UI Lite (Apple, 2024+)
- Ferret-UI (ECCV 2024) introduces “any-resolution” handling; each screen divided into **2 sub-images** based on aspect ratio (horizontal split for portrait, vertical for landscape), encoded separately before sending to LLM. (Apple research page: https://machinelearning.apple.com/research/ferretui-mobile ; ECCV PDF: https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/08095.pdf)
- Ferret-UI Lite:
  - Model size: **3B** (“3B Ferret-UI Lite agent”). (Apple Ferret-UI Lite page: https://machinelearning.apple.com/research/ferret-ui)
  - Reported scores:
    - GUI grounding: **91.6%** (ScreenSpot-V2), **53.3%** (ScreenSpot-Pro), **61.2%** (OSWorld-G). (Apple Ferret-UI Lite page: same URL)
    - GUI navigation success rates: **28.0%** (AndroidWorld), **19.8%** (OSWorld). (Apple Ferret-UI Lite page: same URL)

### Multimodal chain-of-thought / hallucination mitigation (VIC, 2024)
- Paper claim: “thinking while looking” multimodal CoT can fail to mitigate hallucinations; proposes **Visual Inference Chain (VIC)** that constructs reasoning chains using textual context **before** introducing visual input (“thinking before looking”), reporting improved zero-shot performance and hallucination mitigation across multiple benchmarks (MMVP, HallusionBench, POPE, MME, MathVista, SEED-Bench). (Thinking Before Looking / VIC: https://ar5iv.labs.arxiv.org/html/2411.12591)

### Prompt injection attacks on multimodal agents
- Image-based Prompt Injection (IPI) paper reports up to **64% attack success** “under stealth constraints” in their evaluation (COCO dataset, GPT-4-turbo; 12 adversarial prompt strategies). (arXiv: https://arxiv.org/abs/2603.03637)
- CrossInject paper reports **at least +26.4%** increase in attack success rates compared to existing injection attacks (average across tasks), and frames this as cross-modal prompt injection against LVLM-driven agents. (arXiv HTML: https://arxiv.org/html/2504.14348v1)

### OCR benchmarks (assistive tech study)
- Study benchmarks four OCR engines: **Google Vision**, **PaddleOCR 3.0**, **EasyOCR**, **Tesseract**; reports Google Vision highest overall accuracy, PaddleOCR close behind as strongest open-source alternative; accuracy declines with increased walking speed and wider viewing angles. (arXiv HTML: https://arxiv.org/html/2602.02223v1)

---

## Technical Details & Procedures

### Anthropic computer use: API call + agent loop (as documented)
- **cURL request skeleton (from docs)**
  - Endpoint: `https://api.anthropic.com/v1/messages`
  - Headers:
    - `content-type: application/json`
    - `x-api-key: $ANTHROPIC_API_KEY`
    - `anthropic-version: 2023-06-01`
    - `anthropic-beta: computer-use-2025-11-24`
  - Body fields shown:
    - `model`: e.g., `"claude-opus-4-6"`
    - `max_tokens`: e.g., `1024`
    - `tools`: includes `computer_20251124` with `display_width_px`, `display_height_px`, `display_number`; plus optional `text_editor_*` and `bash_20250124`. (Anthropic Claude API Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- **Documented “How computer use works” workflow**
  1. Provide Claude with the computer use tool + user prompt requiring desktop interaction.
  2. Claude decides whether to use the tool; if yes, constructs a formatted tool request; API response has `stop_reason: tool_use`.
  3. Your application executes the requested tool action(s) and returns results.
  4. Claude continues calling tools until completion; repetition of steps is the “agent loop.” (Anthropic Claude API Docs: same URL)
- **Implementation responsibility**
  - Claude cannot execute the tool directly; your application must implement screenshot capture, mouse movements, keyboard inputs, etc. (Anthropic Claude API Docs: same URL)
- **Example action dispatcher (from docs)**
  - Pseudocode handles action types like `screenshot`, `left_click` with `params["coordinate"]`, and `type` with `params["text"]`. (Anthropic Claude API Docs: same URL)
- **Iteration limiting**
  - Reference `sampling_loop` includes `max_iterations: int = 10` “to prevent infinite loops” and notes iteration limits prevent runaway API costs. (Anthropic Claude API Docs: same URL)
- **Prompting tips (docs)**
  - Dropdowns/scrollbars can be tricky with mouse movements; try prompting keyboard shortcuts.
  - For repeatable tasks, include example screenshots and tool calls of successful outcomes.
  - If login is needed, docs suggest providing credentials inside `<robot_credentials>` tags, while warning this increases prompt injection risk and recommending reviewing mitigation guidance. (Anthropic Claude API Docs: same URL)

### OpenAI Responses API: image input patterns (as documented)
- **Passing an image URL**
  - `input` is an array of messages; `content` includes `{"type":"input_text"}` and `{"type":"input_image","image_url":"https://..."}`. (OpenAI Vision Guide: https://platform.openai.com/docs/guides/vision)
- **Passing Base64 data URL**
  - Encode file to base64; pass `image_url: f"data:image/jpeg;base64,{base64_image}"`. (OpenAI Vision Guide: same URL)
- **Passing a file ID**
  - Upload via Files API with `purpose="vision"`; then pass `{"type":"input_image","file_id": file_id}`. (OpenAI Vision Guide: same URL)
- **Image generation via tool call**
  - Responses API example uses `tools=[{"type":"image_generation"}]` and extracts outputs where `output.type == "image_generation_call"`. (OpenAI Vision Guide: same URL)

### OmniParser: parsing outputs (described)
- Inputs: **user task + UI screenshot**
- Outputs:
  1. Screenshot with **bounding boxes + numeric IDs** overlaid
  2. “Local semantics” containing extracted text and icon descriptions. (OmniParser site: https://microsoft.github.io/OmniParser/)

### Ferret-UI: “any resolution” preprocessing (described)
- Each screen divided into **2 sub-images** based on aspect ratio:
  - Portrait: **horizontal division**
  - Landscape: **vertical division**
- Both sub-images encoded separately before being sent to LLMs. (Apple Ferret-UI page: https://machinelearning.apple.com/research/ferretui-mobile ; ECCV PDF: https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/08095.pdf)

---

## Comparisons & Trade-offs

### Screenshot-only agents vs structured-UI (HTML/view hierarchy) approaches
- **SeeClick** argues structured data can be lengthy (HTML) or inaccessible (desktops), and proposes screenshot-only automation; introduces ScreenSpot as a cross-platform grounding benchmark. (SeeClick: https://arxiv.org/html/2401.10935v1)
- **OmniParser** claims screenshot-only input with its parsing module can outperform GPT-4V baselines that require extra information outside screenshots on Mind2Web and AITW. (OmniParser: https://arxiv.org/abs/2408.00203)
- **CogAgent** claims screenshot-only input can outperform LLM methods consuming extracted HTML on Mind2Web and AITW. (CogAgent: https://arxiv.org/html/2312.08914v1)

### Grounding representations: raw coordinates vs boxes/IDs
- OmniParser paper notes GPT-4V struggles to output exact x-y coordinates; Set-of-Marks overlays boxes with numeric IDs so the model selects a box rather than emitting coordinates. (OmniParser arXiv HTML: https://arxiv.org/html/2408.00203v1)
- CogAgent uses normalized coordinate format and bounding boxes (normalized to [000,999]) in its grounding data format. (CogAgent arXiv HTML: https://arxiv.org/html/2312.08914v1)

### Model/agent performance snapshots (reported)
- **Ferret-UI Lite (3B)** reports grounding scores: 91.6% (ScreenSpot-V2), 53.3% (ScreenSpot-Pro), 61.2% (OSWorld-G); navigation success: 28.0% (AndroidWorld), 19.8% (OSWorld). (Apple: https://machinelearning.apple.com/research/ferret-ui)
- **SeeClick** reports:
  - ScreenSpot: dataset described; click accuracy metric defined.
  - MiniWob: beats Pix2Act with 0.3% training data.
  - AITW: +8 percentage points click accuracy vs Qwen-VL baseline. (SeeClick: https://arxiv.org/html/2401.10935v1)

### Vision input cost/latency trade-off (OpenAI `detail`)
- `detail="low"` uses a 512×512 representation and “budget of 85 tokens,” intended to save tokens and speed up responses; `high` provides better understanding when high-resolution detail is needed. (OpenAI Vision Guide: https://platform.openai.com/docs/guides/vision)

### Safety controls: model-internal vs system-enforced
- Anthropic docs describe **automatic classifiers** that steer toward user confirmation when prompt injection is suspected in screenshots, but also emphasize developers should isolate the environment and avoid sensitive data. (Anthropic Claude API Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Microsoft Learn emphasizes **defense-in-depth** and **deterministic human-in-the-loop enforced by orchestrator logic**, plus least privilege and explicit action schemas. (Microsoft Learn: https://learn.microsoft.com/en-us/security/zero-trust/sfi/secure-agentic-systems)
- A third-party critique argues “confirm before acting” fails if not enforced outside the model; recommends least privilege, external approval gates, and kill switches that revoke tokens/stop queues. (RavenTek blog: https://www.raventek.com/confirm-before-acting-is-not-a-safety-system/)  
  - Note: this is not an official standard; treat as commentary, but it aligns conceptually with Microsoft Learn’s “deterministic HITL” and least privilege guidance.

---

## Architecture & Design Rationale

### Why GUI agents use perception → planning → acting loops
- A GUI agent architecture is commonly described as three modules:
  - **Perception**: extract semantic info from UI elements (buttons, text boxes, icons) either via APIs/view hierarchy (for text-only LMs) or via screenshots (for MLLMs).
  - **Planning**: translate perceived state + task into action plans; some methods incorporate reflection/feedback and dynamic replanning.
  - **Acting**: convert plans into executable actions (click, swipe, type). (Survey excerpt: https://arxiv.org/html/2504.20464v2)
- Rationale for screenshot-based perception:
  - View hierarchy can fail for dynamic/custom-drawn content; screenshots capture what’s actually visible. (Survey excerpt: https://arxiv.org/html/2504.20464v2)

### Why “screen parsing” modules (OmniParser) exist
- OmniParser argues general multimodal models are limited by lack of robust screen parsing that:
  1) reliably identifies interactable icons, and  
  2) understands semantics and associates intended actions with correct regions. (OmniParser: https://microsoft.github.io/OmniParser/ ; https://arxiv.org/abs/2408.00203)
- Design: fine-tune a **detection model** (interactable regions) + **caption model** (functional semantics), producing structured elements and local semantics to improve grounding. (OmniParser: same URLs)

### Why “any-resolution” / multi-crop approaches are used for UI
- Ferret-UI notes UI screens have elongated aspect ratios and smaller objects (icons/text) than natural images; it uses “any resolution” by splitting into two sub-images and encoding separately to magnify details. (Apple Ferret-UI: https://machinelearning.apple.com/research/ferretui-mobile ; ECCV PDF: https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/08095.pdf)

### Why agent loops must be orchestrated outside the model (computer use tools)
- Anthropic explicitly states Claude does not directly connect to the environment; the application translates tool requests into actions and returns results; the tool must be executed by the application. (Anthropic Claude API Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- This separation supports sandboxing and least privilege (recommended in the same doc), and enables deterministic enforcement (e.g., confirmation gates, allowlists) at the application layer.

### Why memory/retrieval tools are proposed for long-horizon GUI tasks
- PAL-UI argues long-horizon tasks are hard due to memory limitations; visual observations are “heavier than text” and images encode into many tokens; proposes a retrieval tool to fetch specific historical screenshots on demand during planning. (PAL-UI: https://arxiv.org/pdf/2510.00413.pdf)

---

## Common Questions & Answers

### Q1) Who stores screenshots and interaction traces when using Anthropic’s computer use tool?
- Anthropic states computer use is a **client-side tool**: screenshots, mouse actions, keyboard inputs, and files are captured/stored in **your environment**, not by Anthropic; Anthropic processes images/action requests in real time and “does not retain them after the response is returned.” (Anthropic Claude API Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)

### Q2) What signals that Claude wants to call a tool in the computer use workflow?
- The docs state the API response has `stop_reason` of **`tool_use`**, signaling Claude’s intent to use a tool. (Anthropic Claude API Docs: same URL)

### Q3) Can Claude execute mouse/keyboard actions directly?
- No. Anthropic states the computer use tool must be **explicitly executed by your application**; you implement screenshot capture, mouse movements, keyboard inputs, etc. (Anthropic Claude API Docs: same URL)

### Q4) What are OpenAI’s image input limits in the vision guide?
- Supported types: PNG, JPEG/JPG, WEBP, non-animated GIF.
- Limits: **50 MB total payload per request**, **500 images per request**. (OpenAI Vision Guide: https://platform.openai.com/docs/guides/vision)

### Q5) What does OpenAI’s `detail="low"` do for image understanding?
- The guide says it can save tokens and speed up responses; it uses a **512×512** version of the image with a **budget of 85 tokens**. (OpenAI Vision Guide: https://platform.openai.com/docs/guides/vision)

### Q6) How is “click accuracy” defined for GUI grounding in SeeClick?
- Click accuracy is the proportion of test samples where the predicted click location falls inside the ground-truth element bounding box; predicted location is the generated point or the center of a generated bounding box. (SeeClick: https://arxiv.org/html/2401.10935v1)

### Q7) What is ScreenSpot and how big is it (per SeeClick)?
- ScreenSpot is described as a realistic GUI grounding dataset across mobile, desktop, and web; it contains **over 600 screenshots** and **1200 instructions** spanning iOS, Android, macOS, Windows, and web. (SeeClick: https://arxiv.org/html/2401.10935v1)

### Q8) What datasets did OmniParser curate and what are their sizes?
- Interactable icon detection dataset: **67k unique screenshot images**.
- Icon description dataset: **7k icon-description pairs**. (OmniParser: https://microsoft.github.io/OmniParser/)

### Q9) What is a concrete example of a multimodal prompt injection risk for GUI agents?
- Anthropic warns Claude may follow commands found in webpage content or images even if they conflict with user instructions. (Anthropic Claude API Docs: https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)
- Research papers demonstrate attacks:
  - Image-based Prompt Injection reports up to **64%** attack success under stealth constraints. (arXiv: https://arxiv.org/abs/2603.03637)
  - CrossInject reports **≥ +26.4%** higher average attack success rates than existing injection methods. (arXiv HTML: https://arxiv.org/html/2504.14348v1)

### Q10) What does Microsoft recommend for securing agentic systems?
- Microsoft Learn recommends a **defense-in-depth** strategy and lists controls across layers, including:
  - Input/output filtering, guardrails, logging/observability
  - Application-layer controls like **agents as microservices**, **explicit action schemas**, **deterministic HITL enforced by orchestrator logic**, and **least privilege**. (Microsoft Learn: https://learn.microsoft.com/en-us/security/zero-trust/sfi/secure-agentic-systems)