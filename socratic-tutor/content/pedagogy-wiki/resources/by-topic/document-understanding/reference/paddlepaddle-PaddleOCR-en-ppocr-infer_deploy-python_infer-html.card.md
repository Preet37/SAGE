# Card: PaddleOCR 3.0 Python/CLI Inference (PP-OCRv5 pipeline + deployment knobs)
**Source:** https://paddlepaddle.github.io/PaddleOCR/en/ppocr/infer_deploy/python_infer.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** End-to-end PaddleOCR inference pipeline (detector + recognizer + optional orientation/unwarp/textline orientation), with concrete CLI/Python API usage and default-ish deployment settings (CPU/GPU, HPI).

## Key Content
- **General OCR pipeline modules (mandatory/optional):** mandatory **text detection + text recognition**; optional **document image orientation classification**, **text image correction (unwarping/rectification)**, **text line orientation classification** (pipeline described near “General OCR pipeline…”).
- **Python API (PP-OCRv5):**
  - `from paddleocr import PaddleOCR`
  - `ocr = PaddleOCR(use_doc_orientation_classify=False, use_doc_unwarping=False, use_textline_orientation=False)`
  - `result = ocr.predict(input="test.png")`; per-result: `res.print()`, `res.save_to_img("output")`, `res.save_to_json("output")`.
- **Python API (PP-StructureV3):** `from paddleocr import PPStructureV3`; `pipeline = PPStructureV3(use_doc_orientation_classify=False, use_doc_unwarping=False)`; `output = pipeline.predict(input="test.png")`; save: JSON + Markdown.
- **CLI examples:** `paddleocr ocr -i test.png --use_doc_orientation_classify False ...`; PP-ChatOCRv4 doc: `paddleocr pp_chatocrv4_doc -i test.png -k number --qianfan_api_key ... --use_doc_orientation_classify False`.
- **High-Performance Inference (HPI) rationale:** enable `enable_hpi` to auto-select backend (Paddle Inference / OpenVINO / ONNX Runtime / TensorRT) + built-in multithreading/FP16; example speedups on **NVIDIA T4**: **PP-OCRv5_mobile_rec latency −73.1%**, **PP-OCRv5_mobile_det −40.4%**.
- **Benchmark rows (selected):**
  - Doc orientation model **PP-LCNet_x1_0_doc_ori**: **Top-1 99.06%**, size **7 MB**, GPU **2.62→0.59 ms** (Normal/HPI), CPU **3.24→1.19 ms**.
  - Detector **PP-OCRv5_server_det**: Hmean **83.8**, size **84.3 MB**, GPU **89.55→70.19 ms**, CPU **383.15 ms**.
  - Detector **PP-OCRv5_mobile_det**: Hmean **79.0**, size **4.7 MB**, GPU **10.67→6.36 ms**, CPU **57.77→28.15 ms**.
  - Recognizer **PP-OCRv5_server_rec**: avg acc **86.38%**, size **81 MB**, GPU **8.46→2.36 ms**, CPU **31.21 ms**.
  - Recognizer **PP-OCRv5_mobile_rec**: avg acc **81.29%**, size **16 MB**, GPU **5.43→1.46 ms**, CPU **21.20→5.32 ms**.
- **Mobile (Paddle-Lite) key parameters:** compile with `--with_cv=ON --with_extra=ON`; `paddle_lite_opt` outputs `.nb` (set `--optimize_out_type naive_buffer` for mobile). Example config values: `max_side_len 960`, `det_db_thresh 0.3`, `det_db_box_thresh 0.5`, `det_db_unclip_ratio 1.6`, `use_direction_classify 0`, `rec_image_height 48` (PP-OCRv3; PP-OCRv2 uses 32).

## When to surface
Use when students ask how to run PaddleOCR end-to-end (CLI/Python), which optional preprocessing modules to toggle, or how CPU/GPU + HPI settings and model choices trade off accuracy, latency, and size (including mobile Paddle-Lite deployment knobs).