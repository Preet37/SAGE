# Card: VBench (CVPR’24) — Reproducible Video-Gen Evaluation + Scoring
**Source:** https://github.com/Vchitect/VBench  
**Role:** benchmark | **Need:** EMPIRICAL_DATA  
**Anchor:** Reference implementation (scripts/configs/CLI) to compute VBench metrics and aggregate scores for reproducible comparisons.

## Key Content
- **What VBench evaluates (16 dimensions; released 12/2023):**  
  `['subject_consistency','background_consistency','temporal_flickering','motion_smoothness','dynamic_degree','aesthetic_quality','imaging_quality','object_class','multiple_objects','human_action','color','spatial_relationship','scene','temporal_style','appearance_style','overall_consistency']`
- **Design rationale:** enforce **standard prompt lists** for fair model comparison via `vbench/VBench_full_info.json`; warns when required videos missing. Supports **custom videos** when `--mode=custom_input` (no filename requirements).
- **Custom-input supported dimensions (subset):**  
  `subject_consistency, background_consistency, motion_smoothness, dynamic_degree, aesthetic_quality, imaging_quality`
- **Core workflow (CLI):**
  - Install: `pip install vbench` (+ PyTorch; Detectron2 needed for some dimensions; Detectron2 works with CUDA 12.1 or 11.x).  
  - Evaluate: `vbench evaluate --videos_path $VIDEO_PATH --dimension $DIMENSION`  
  - Custom videos: `vbench evaluate --dimension $DIMENSION --videos_path ... --mode=custom_input`  
  - Multi-GPU: `vbench evaluate --ngpus=${GPUS} ...` or `torchrun --nproc_per_node=${GPUS} --standalone evaluate.py ...`
- **Temporal flicker preprocessing:** run `static_filter.py --videos_path $VIDEOS_PATH` before `temporal_flickering` (options: `--filter_scope all` or JSON prompt list).
- **Aggregate scoring formulas (Leaderboard scripts):**
  - **Normalization (Eq. 1):** `norm = (dim_score - min_val) / (max_val - min_val)`  
  - **Quality Score:** weighted avg of `{subject, background, temporal_flickering, motion_smoothness, aesthetic_quality, imaging_quality, dynamic_degree}`  
  - **Semantic Score:** weighted avg of `{object_class, multiple_objects, human_action, color, spatial_relationship, scene, appearance_style, temporal_style, overall_consistency}`  
  - **Total Score (Eq. 2):** `Total = w1*Quality + w2*Semantic`  
  - `min/max` and weights in `scripts/constant.py`; compute via `scripts/cal_final_score.py --zip_file ... --model_name ...`

## When to surface
Use when students ask how to **evaluate/compare text-to-video models**, compute **VBench dimension metrics**, run **custom-video evaluation**, or reproduce **leaderboard-style normalized/weighted total scores**.