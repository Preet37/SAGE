# Card: Retriever-Aware Training (RAT) for API/Tool Calling (Gorilla)
**Source:** https://proceedings.neurips.cc/paper_files/paper/2024/file/e4c61f578ff07830f5c37378dd3ecb0d-Paper-Conference.pdf  
**Role:** paper | **Need:** FORMULA_SOURCE  
**Anchor:** RAT procedure for tool/API call generation conditioned on retrieved API docs + evaluation vs strong baselines

## Key Content
- **Dataset (APIBench) construction (Sec. 3.1):**
  - **1,645 APIs** total: **TorchHub 95 (exhaustive)**, **TensorFlow Hub v2 626 (filtered from 801)**, **HuggingFace 925 (top-20 per domain)**.
  - Each API converted to JSON fields: `{domain, framework, functionality, api_name, api_call, api_arguments, environment_requirements, example_code, performance, description}`.
  - Self-instruct: **GPT-4** generates **10 instructions per API → 16,450 {instruction, API} pairs**; only **18 seed examples** hand-made (6 per hub).
- **Retriever-Aware Training (RAT) (Sec. 3.2):**
  - Training prompt appends retrieved doc:  
    **`<user_prompt> Use this API documentation for reference: <retrieved_API_doc_JSON>`**
  - Rationale: retrieved docs may be wrong (imperfect recall); RAT teaches model to **use relevant docs** and **ignore irrelevant retrieval** (“judge the retriever”), reducing hallucinations and improving robustness to **test-time doc/API changes**.
  - Inference modes: **zero-shot** (no retriever) vs **retrieval** (BM25 or GPT-Index top-1 doc appended; no extra prompt tuning).
- **Evaluation metrics (Sec. 3.3):**
  - **AST subtree matching** for functional correctness of single API call.
  - **Hallucination definition:** generated API call **not a subtree of any API** in database; **accuracy + error + hallucination = 1**.
  - Human check: **AST accuracy 0.78 = human 0.78**; **code executable 0.72** (100-sample).
- **Key empirical results (Table 1, 2):**
  - **TorchHub, GPT-Index retriever:** Gorilla **61.82% acc, 0% halluc** vs GPT-4 **59.13% acc, 1.07% halluc**.
  - **Zero-shot TorchHub:** Gorilla **59.13% acc, 6.98% halluc** vs GPT-4 **38.70% acc, 36.55% halluc**.
  - **Oracle retriever + Gorilla:** TorchHub **67.20% acc (0% halluc)**; HuggingFace **91.26% acc**; TensorHub **94.16% acc**.
  - Retrieval gap (Table 2, Gorilla trained w/ oracle retriever): eval with **GPT-Index degrades 29.20% acc**, **BM25 degrades 52.27% acc** vs oracle.
- **Defaults / hyperparameters (App. A.2, Table 6):**
  - Train **5 epochs**, **lr 2e-5** (cosine decay), **batch 64**, **warmup 0.03**, **weight decay 0**, **max seq 2048**, on **8×A100 40GB**.
  - Splits: HuggingFace **90/10**, TorchHub & TensorHub **80/20**.

## When to surface
Use when students ask how to train/evaluate LLMs for **tool/function calling with retrieved documentation**, how to **define/measure API hallucinations**, or why retrieval can **help or hurt** without retriever-aware training.