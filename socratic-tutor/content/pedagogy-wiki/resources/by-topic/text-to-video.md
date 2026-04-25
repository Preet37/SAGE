# Text To Video

## Video (best)
- **Yannic Kilcher** — "Sora - OpenAI's Text-to-Video Model (Paper Explained)"
- youtube_id: _gCqFBFd_Ls
- Why: Yannic Kilcher provides rigorous technical breakdowns of the Sora technical report, covering the diffusion transformer architecture, temporal consistency, and spacetime patch representations — directly relevant to the core concepts in this topic.
- Level: intermediate/advanced

## Blog / Written explainer (best)
- **Lilian Weng** — "Video Generation Models as World Simulators"
- url: https://lilianweng.github.io/posts/2024-04-12-diffusion-video/
- Why: Lilian Weng's posts are consistently the gold standard for systematic, well-cited technical overviews. This post covers the evolution from image diffusion to video generation, temporal attention mechanisms, and consistency challenges — mapping directly onto the related concepts in this topic.
- Level: intermediate/advanced

## Deep dive
- **OpenAI Technical Report** — "Video generation models as world simulators (Sora Technical Report)"
- url: https://openai.com/research/video-generation-models-as-world-simulators
- Why: The Sora technical report is the most comprehensive publicly available reference on large-scale text-to-video generation, covering spacetime latent patches, temporal consistency, and scaling behavior. It is the de facto deep-dive reference for this topic.
- Level: advanced

## Original paper
- **Ho et al. / Singer et al.** — "Make-A-Video: Text-to-Video Generation without Text-Video Data"
- url: https://arxiv.org/abs/2209.14430
- Why: Make-A-Video is one of the most readable and pedagogically clear seminal papers in text-to-video, building directly on text-to-image diffusion and introducing the temporal attention extension in a well-explained way. It bridges text-to-image knowledge (which learners likely already have) with video generation, making it the most accessible entry point into the literature.
- Level: intermediate/advanced

## Code walkthrough
- None identified
- Why: There is no widely recognized, high-quality hands-on code walkthrough for text-to-video generation from a trusted educator (e.g., Karpathy, fast.ai) that is clearly documented and pedagogically structured. Most available notebooks are unofficial and of inconsistent quality. The closest practical resource is the Hugging Face Diffusers library documentation for text-to-video pipelines (https://huggingface.co/docs/diffusers/api/pipelines/text_to_video [NOT VERIFIED]), but this is API documentation rather than a true walkthrough.

## Coverage notes
- **Strong:** Conceptual explanation of Sora and diffusion-based video generation; temporal attention as an architectural concept; connection to text-to-image diffusion models
- **Weak:** Hands-on implementation walkthroughs are sparse — open-source text-to-video models (e.g., ModelScope, CogVideo) have limited pedagogical code resources
- **Gap:** No excellent beginner-level video exists that builds from first principles (e.g., "what makes video generation harder than image generation") without assuming prior knowledge of diffusion models. The connection between the related concepts listed (mel spectrogram, speech-to-speech, Whisper, VALL-E) and text-to-video is not well-served by any single resource — these appear to be from a multimodal course where audio and video generation are taught together, but no resource bridges them cleanly.

## Last Verified
2025-01-01 (resource existence based on training knowledge; URLs marked [NOT VERIFIED] should be confirmed before publishing to platform)