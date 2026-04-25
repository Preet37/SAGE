# Curation Report: Image Generation and Editing
**Topic:** `image-generation` | **Date:** 2026-04-09 18:33
**Library:** 3 existing → 16 sources (13 added, 9 downloaded)
**Candidates evaluated:** 48
**Reviewer verdict:** needs_additions

## Added (13)
- **[paper]** [[PDF] Photorealistic Text-to-Image Diffusion Models with Deep Language ...](https://papers.neurips.cc/paper_files/paper/2022/file/ec795aeadae0b7d230fa35cbaf04c041-Paper-Conference.pdf)
  Provides an authoritative, system-level account of how prompt understanding is handled via text-encoder selection/scaling and how that integrates into a multi-stage generation pipeline, with concrete rationale and ablations.
- **[reference_doc]** [Images | OpenAI API Reference](https://platform.openai.com/docs/api-reference/images?lang=node.js)
  Official, citable API surface with defaults and constraints the tutor can quote when students ask exactly what parameters exist and what values are permitted.
- **[benchmark]** [GENEVAL: An Object-Focused Framework for Evaluating ...](https://proceedings.neurips.cc/paper_files/paper/2023/file/a3bf71c7c63f0c3bcb7ff67c67b1e7b1-Paper-Datasets_and_Benchmarks.pdf)
  Adds concrete, reproducible prompt-following numbers and an evaluation methodology that is widely referenced for compositional correctness beyond generic FID-style fidelity metrics.
- **[paper]** [ImageReward: Learning and Evaluating Human Preferences for Text-to-Image Generation](https://arxiv.org/abs/2304.05977)
  Gives a concrete, citable preference-model formulation and empirical evidence for reranking/selection aligned with human judgments—directly useful for teaching practical generation selection workflows.
- **[paper]** [Pick-a-Pic: An Open Dataset of User Preferences for](https://proceedings.neurips.cc/paper_files/paper/2023/file/73aacd8b3b05b4b503d58310b523553c-Paper-Conference.pdf)
  Complements ImageReward with an open preference dataset and a widely used scoring model, enabling structured comparisons and practical guidance for reranking multiple generations.
- **[paper]** [IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models](http://arxiv.org/pdf/2308.06721.pdf)
  This directly fills the stated gap on IP-Adapter math/architecture; it’s a primary source with implementable details that a tutor can cite precisely.
- **[benchmark]** [Human Evaluation of Text-to-Image Models on a Multi-Task Benchmark](https://arxiv.org/html/2211.12112)
  Provides concrete numbers from a human evaluation (not just FID), which is explicitly requested for preference/quality comparisons and is useful for teaching evaluation methodology.
- **[benchmark]** [Holistic Evaluation of Text-to-Image Models](https://proceedings.neurips.cc/paper_files/paper/2023/file/dd83eada2c3c74db3c7fe1c087513756-Paper-Datasets_and_Benchmarks.pdf)
  This is exactly the kind of “tables with numbers” source the library is missing for broad, multi-axis evaluation; it complements GenEval by covering more than object/attribute correctness.
- **[reference_doc]** [OpenAI Docs: DALL·E 3 model documentation](https://platform.openai.com/docs/models/dall-e-3)
  Even if “thin,” model pages often contain the exact constraints and caveats students ask about; it’s a canonical complement to the endpoint reference already included.
- **[paper]** [IP-Adapter: Text Compatible Image Prompt Adapter for Text-to-Image Diffusion Models](http://arxiv.org/pdf/2308.06721.pdf) *(promoted by reviewer)*
  This directly fills the stated gap on IP-Adapter math/architecture; it’s a primary source with implementable details that a tutor can cite precisely.
- **[benchmark]** [Human Evaluation of Text-to-Image Models on a Multi-Task Benchmark](https://arxiv.org/html/2211.12112) *(promoted by reviewer)*
  Provides concrete numbers from a human evaluation (not just FID), which is explicitly requested for preference/quality comparisons and is useful for teaching evaluation methodology.
- **[benchmark]** [Holistic Evaluation of Text-to-Image Models](https://proceedings.neurips.cc/paper_files/paper/2023/file/dd83eada2c3c74db3c7fe1c087513756-Paper-Datasets_and_Benchmarks.pdf) *(promoted by reviewer)*
  This is exactly the kind of “tables with numbers” source the library is missing for broad, multi-axis evaluation; it complements GenEval by covering more than object/attribute correctness.
- **[reference_doc]** [OpenAI Docs: DALL·E 3 model documentation](https://platform.openai.com/docs/models/dall-e-3) *(promoted by reviewer)*
  Even if “thin,” model pages often contain the exact constraints and caveats students ask about; it’s a canonical complement to the endpoint reference already included.

## Near-Misses (2) — Worth a Second Look
_The curator considered these but passed. Override if you disagree._

- **Image generation - OpenAI API** — [Image generation - OpenAI API](https://platform.openai.com/docs/guides/image-generation?image-generation-model=dall-e-3)
  _Skipped because:_ Useful tutorial-style examples, but the API reference page is more authoritative for exact parameter defaults/constraints and is easier to cite precisely.
- **Pick-a-Pic: An Open Dataset of User Preferences for Text- ..** — [Pick-a-Pic: An Open Dataset of User Preferences for Text- ...](https://arxiv.org/html/2305.01569)
  _Skipped because:_ HTML rendering is convenient, but the NeurIPS PDF is the canonical, citable version for a reference library.

## Reasoning
**Curator:** Selections prioritize canonical papers and official docs that provide either (a) system-level design rationale for prompt understanding (Imagen) or (b) citable, concrete specs/metrics (OpenAI Images API, GenEval, ImageReward/PickScore). Editing-specific diffusion math and Midjourney/FLUX official parameter references were not adequately covered by the provided candidates.
**Reviewer:** The curator’s additions are strong, but the library still needs a primary IP-Adapter formula source and at least one human/holistic benchmark with concrete tables, plus the model-specific DALL·E 3 doc page for authoritative parameter/behavior constraints.
