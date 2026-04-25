# Card: GenEval — object-focused T2I alignment benchmark & scoring
**Source:** https://proceedings.neurips.cc/paper_files/paper/2023/file/a3bf71c7c63f0c3bcb7ff67c67b1e7b1-Paper-Datasets_and_Benchmarks.pdf  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** GenEval protocol + binary correctness scoring for object/attribute/relation alignment; human-agreement validation; model comparison table.

## Key Content
- **Tasks & prompt templates (Table 1; 553 prompts total; 4 images/prompt):**
  - Single object (80): “a photo of a/an [OBJECT]”
  - Two object (99): “a photo of a/an [OBJECT A] and a/an [OBJECT B]”
  - Counting (80): “a photo of [NUMBER] [OBJECT]s”, NUMBER ∈ {2,3,4}
  - Colors (94): “a photo of a/an [COLOR] [OBJECT]”
  - Position (100): “a photo of a/an [OBJECT A] [REL POS] a/an [OBJECT B]”, REL POS ∈ {above, below, left of, right of}
  - Attribute binding (100): “a photo of a/an [COLOR A] [OBJECT A] and a/an [COLOR B] [OBJECT B]”
  - Objects: 80 MS-COCO classes (some renamed); Colors: 11 basic terms but **exclude gray**; exclude “person” for color tasks.
- **Evaluation pipeline (Section 3.2):**
  - **Instance segmentation:** Mask2Former (MMDetection), default conf **0.3**; for **counting use 0.9** (reduces spurious low-conf boxes).
  - **Position rule (Appendix C.3):** centroids (xA,yA),(xB,yB) with min-offset threshold **c=0.1**:  
    - B right of A if **xB > xA + c(wA+wB)**; left if **xB < xA − c(wA+wB)**  
    - B below A if **yB > yA + c(hA+hB)**; above if **yB < yA − c(hA+hB)**  
    where w*, h* are bbox width/height.
  - **Color classification:** CLIP ViT-L/14 zero-shot over candidate colors using prompts “a photo of a [COLOR] [OBJECT]”; **crop to bbox + mask background to gray** improves agreement (Table 4).
- **Scoring (Section 3.2):** per-image **binary correctness** (“all prompt elements satisfied”); average per task; overall score = mean across 6 tasks; also outputs error breakdown (missing objects, wrong count/position/color).
- **Human agreement (Section 4):** 6,000 annotations / 1,200 images; GenEval **83%** vs inter-annotator **88%**; on unanimous subset GenEval **91%** (CLIPScore **87%**). GenEval beats threshold-tuned CLIPScore especially on counting (+22 pts agreement).
- **Benchmark results (Table 2, overall GenEval):** minDALL-E **0.23**, SDv1.5 **0.43**, SDv2.1 **0.50**, SD-XL **0.55**, IF-XL **0.61**. Hard tasks remain low: **position best 0.15 (SD-XL)** / **0.13 (IF-XL)**; **attribute binding best 0.35 (IF-XL)**.

## When to surface
Use when students ask how to *measure prompt-following/compositional correctness* in text-to-image (objects, counts, spatial relations, color binding), or want concrete benchmark numbers comparing diffusion models beyond CLIPScore/FID.