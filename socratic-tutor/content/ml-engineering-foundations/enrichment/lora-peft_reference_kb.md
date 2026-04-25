## Key Facts & Specifications

### LoRA (Low-Rank Adaptation)
- **Core method**: LoRA “freezes the pre-trained model weights and injects trainable rank decomposition matrices into each layer of the Transformer architecture,” reducing trainable parameters for downstream tasks. (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- **Parameter/memory reductions (reported)**:
  - Compared to GPT-3 175B fine-tuned with Adam, LoRA can reduce **trainable parameters by 10,000×** and **GPU memory requirement by 3×**. (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- **Latency claim**: LoRA has “**no additional inference latency**” (contrasted with adapters) and can have “higher training throughput.” (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- **Scaling of LoRA update (as described in secondary source)**:
  - A common formulation is: \(\Delta W = (\alpha/r)BA\). (Skellam.ai blog, undated, https://skellam.ai/low-rank-adaptation-lora-a-deep-dive-into-efficient-fine-tuning-of-large-models/)
  - **Note**: This scaling is not explicitly quoted in the arXiv snippet shown in the search results; treat as secondary-source support.

### Hugging Face PEFT `LoraConfig` (selected verified parameters/behaviors)
- `r` is the “Lora attention dimension (the ‘rank’).” (Hugging Face PEFT source, `config.py`, https://github.com/huggingface/peft/blob/main/src/peft/tuners/lora/config.py)
- `target_modules` matching rules:
  - String → regex match; list → exact match or suffix match; special value `'all-linear'` targets all linear/Conv1D modules (excluding output layer for `PreTrainedModel`). (PEFT `config.py`, URL above)
- `fan_in_fan_out=True` is needed for layers storing weights as `(fan_in, fan_out)`; example: **GPT-2 `Conv1D`**. (PEFT `config.py`, URL above)
- `bias` can be `'none'`, `'all'`, or `'lora_only'`; training biases can change outputs even when adapters are disabled. (PEFT `config.py`, URL above)
- `use_rslora=True` changes scaling to `lora_alpha/math.sqrt(r)`; otherwise default is `lora_alpha/r`. (PEFT `config.py`, URL above)
- Initialization defaults:
  - Default initializes **A with Kaiming-uniform and B with zeros**, producing an identity/no-op adapter initially. (PEFT LoRA dev guide, https://github.com/huggingface/peft/blob/main/docs/source/developer_guides/lora.md)
  - `init_lora_weights="gaussian"` initializes A with Gaussian and B with zeros. (PEFT LoRA dev guide, URL above)
  - `init_lora_weights=False` makes LoRA **not** an identity transform (debug/testing). (PEFT LoRA dev guide, URL above)
- EVA rank redistribution:
  - `rho (>= 1.0)`; “maximum rank for a layer is `lora_r * rho`”; default `rho=2.0`. (PEFT `config.py`, URL above)

### QLoRA (Quantized LoRA)
- **Goal/claim**: QLoRA reduces memory enough to fine-tune a **65B** parameter model on a **single 48GB GPU** while preserving full 16-bit finetuning task performance. (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314; NeurIPS 2023 PDF)
- **Performance claim**: Guanaco reaches **99.3% of ChatGPT performance** on the Vicuna benchmark, requiring **24 hours** of finetuning on a single GPU. (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314; NeurIPS 2023 PDF)
- **Key innovations**:
  - **NF4**: “information theoretically optimal for normally distributed weights.” (Dettmers et al., 2023, arXiv/NeurIPS PDF)
  - **Double Quantization**: saves “about **0.37 bits per parameter** (approximately **3 GB for a 65B model**).” (Dettmers et al., 2023, NeurIPS PDF)
  - **Paged Optimizers**: manage memory spikes; uses NVIDIA Unified Memory paging. (Dettmers et al., 2023, NeurIPS PDF)
- **Memory numbers (explicit)**:
  - Regular 16-bit finetuning of LLaMA **65B** requires **>780 GB** GPU memory; QLoRA reduces to **<48 GB**. (Dettmers et al., 2023, NeurIPS PDF)
  - QLoRA reduces average memory requirements of finetuning a 65B model from **>780GB** to **<48GB**. (Dettmers et al., 2023, NeurIPS PDF)
  - A statement in the NeurIPS PDF: “(7B parameters) requires just **5 GB** of memory…” (context: QLoRA vs Alpaca model comparison). (Dettmers et al., 2023, NeurIPS PDF)
- **NF4 vs FP4**:
  - Table claim: NF4 with double quantization matches BF16 performance; FP4 is “consistently one percentage point behind.” (Dettmers et al., 2023, NeurIPS PDF, Table 3 description in snippet)

### bitsandbytes compute dtype behavior (QLoRA-related)
- `bnb_4bit_compute_dtype` is “the type that is used for the multiplication”; weights are decompressed to that type for matmul; outputs are converted back to the original input dtype. (bitsandbytes issue #1515, 2025, https://github.com/bitsandbytes-foundation/bitsandbytes/issues/1515)
- `prepare_model_for_kbit_training` is used “to set up the gradient flow and do quantization in the proper way so that gradients flow through the quantized weights.” (bitsandbytes issue #1515, 2025, URL above)
- Recommendation from the same thread: use compute type in **16-bit**, embeddings in **16-bit**, and layer norms in **32-bit**. (bitsandbytes issue #1515, 2025, URL above)

### Deployment/serving performance facts (merged vs unmerged)
- Unmerged LoRA adapters add inference overhead; merging removes overhead. (Fireworks AI docs, https://docs.fireworks.ai/guides/understanding_lora_performance)
- Fireworks AI reports:
  - TTFT overhead: loading weights “on the order of **tens of milliseconds**” and prompt processing time increases by about **10–30%** for unmerged LoRA. (Fireworks AI docs, URL above)

### NVIDIA NIM LoRA adapter format and supported modules
- **NeMo-format LoRA directory** must contain **one `.nemo` file**. (NVIDIA NIM docs, https://docs.nvidia.com/nim/large-language-models/latest/peft.html)
- **Hugging Face Transformers format** requires `adapter_config.json` and one of `{adapter_model.safetensors, adapter_model.bin}`. (NVIDIA NIM docs, URL above)
- Supported target modules:
  - NeMo: `["gate_proj","o_proj","up_proj","down_proj","k_proj","q_proj","v_proj","attention_qkv"]`. (NVIDIA NIM docs, URL above)
  - HF format: `["gate_proj","o_proj","up_proj","down_proj","k_proj","q_proj","v_proj"]`. (NVIDIA NIM docs, URL above)
- NeMo attention may fuse QKV into a single projection; LoRA learns a single low-rank projection for combined QKV. (NVIDIA NIM docs, URL above)

---

## Technical Details & Procedures

### Apply LoRA with Hugging Face PEFT (core workflow)
- Create config and wrap model:
  ```python
  from peft import LoraConfig, get_peft_model
  config = LoraConfig(
      r=16,
      lora_alpha=32,
      target_modules=["q", "v"],  # example from blog
      lora_dropout=0.05,
      bias="none",
      task_type=TaskType.SEQ_2_SEQ_LM,
  )
  model = get_peft_model(model, config)
  ```
  (Heidloff blog example, https://heidloff.net/article/efficient-fine-tuning-lora/; parameter definitions in PEFT `config.py`)

- For int8 training preparation (example):
  ```python
  model = AutoModelForSeq2SeqLM.from_pretrained(..., load_in_8bit=True, device_map="auto")
  model = prepare_model_for_int8_training(model)
  model = get_peft_model(model, lora_config)
  ```
  (Heidloff blog, URL above)

### Scoping LoRA to specific layers/blocks in PEFT (`layers_to_transform`, `layers_pattern`)
- `layers_to_transform`: list of layer indices to transform; if not specified, all layers in `target_modules` are transformed. (PEFT issue #2155 discussion snippet, https://github.com/huggingface/peft/issues/2155)
- `layers_pattern`: pattern for the layer container name (common defaults include `layers`, `h`, `blocks`, etc.); needed for “exotic and custom models.” (PEFT issue #2155, URL above)
- Example fix for LlamaModel scoping:
  ```python
  lora_config = LoraConfig(
      r=8,
      lora_alpha=16,
      target_modules=["q_proj", "k_proj", "v_proj"],
      layers_to_transform=[0, 31],
      layers_pattern="layers",
      lora_dropout=0,
      bias="none",
  )
  ```
  (PEFT issue #2155, URL above)

### Merging LoRA adapters into base weights (PEFT)
- `merge_and_unload()` merges LoRA weights into base weights. (PEFT discussion #1727, 2024, https://github.com/huggingface/peft/discussions/1727)
- If you want to discard adapters without merging, use `unload()`. (PEFT discussion #1727, URL above)
- Practical merge steps (forum workflow):
  1) load base model  
  2) train with PEFT  
  3) save adapter  
  4) reload base model (half/full precision)  
  5) load adapter into base model  
  6) `merge_and_unload()`  
  7) save merged model  
  (Hugging Face forum thread, https://discuss.huggingface.co/t/help-with-merging-lora-weights-back-into-base-model/40968)

- `modules_to_save` for selectively fully-trained layers:
  - Recommended approach: set `modules_to_save=["foo","bar",...]` so those layers are saved inside `adapter_model.safetensors` and reloaded with the adapter. (PEFT issue #2647, https://github.com/huggingface/peft/issues/2647)
  - When running `model = model.merge_and_unload()`, those weights “should be automatically merged, together with the LoRA layers.” (PEFT issue #2647, URL above)

### QLoRA loading configuration (Transformers + bitsandbytes)
- Typical 4-bit NF4 config (example shown in multiple sources):
  ```python
  from transformers import BitsAndBytesConfig
  bnb_config = BitsAndBytesConfig(
      load_in_4bit=True,
      bnb_4bit_quant_type="nf4",
      bnb_4bit_use_double_quant=True,
      bnb_4bit_compute_dtype=torch.bfloat16,  # or torch.float16
  )
  ```
  (Dettmers et al., 2023 describes NF4/DQ; example configs shown in Manal El Aidouni blog and other guides: https://manalelaidouni.github.io/4Bit-Quantization-Models-QLoRa.html)

- `prepare_model_for_kbit_training()` purpose (bitsandbytes):
  - Sets up gradient flow so gradients flow through quantized weights. (bitsandbytes issue #1515, 2025, URL above)

### NVIDIA NIM: downloading and directory setup (commands)
- Example commands to download LoRAs from NGC:
  ```bash
  export LOCAL_PEFT_DIRECTORY=~/loras
  mkdir $LOCAL_PEFT_DIRECTORY
  pushd $LOCAL_PEFT_DIRECTORY
  ngc registry model download-version "nim/meta/llama3-8b-instruct-lora:nemo-math-v1"
  ngc registry model download-version "nim/meta/llama3-8b-instruct-lora:hf-math-v1"
  popd
  chmod -R 777 $LOCAL_PEFT_DIRECTORY
  ```
  (NVIDIA NIM docs, https://docs.nvidia.com/nim/large-language-models/latest/peft.html)

- Example to download a LoRA from Hugging Face Hub into a NIM-compatible directory:
  ```bash
  mkdir $LOCAL_PEFT_DIRECTORY/llama3-lora
  huggingface-cli download <Hugging Face LoRA name> adapter_config.json adapter_model.safetensors \
    --local-dir $LOCAL_PEFT_DIRECTORY/llama3-lora
  chmod -R 777 $LOCAL_PEFT_DIRECTORY
  ```
  (NVIDIA NIM docs, URL above)

---

## Comparisons & Trade-offs

### LoRA vs full fine-tuning
- LoRA can reduce trainable parameters by **10,000×** and GPU memory requirement by **3×** vs GPT-3 175B fine-tuned with Adam (as reported). (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- LoRA reported to perform “on-par or better than fine-tuning” on RoBERTa, DeBERTa, GPT-2, GPT-3. (Hu et al., 2021, arXiv)

### LoRA vs adapters (inference latency)
- LoRA: “unlike adapters, no additional inference latency.” (Hu et al., 2021, arXiv)
- Adapters: cannot be easily merged into base weights; thus add persistent inference compute (comparison described in ApX PEFT comparison page). (ApX comparison page, https://apxml.com/courses/fine-tuning-adapting-large-language-models/chapter-4-parameter-efficient-fine-tuning/comparison-peft-techniques)

### QLoRA vs LoRA (training memory)
- QLoRA: enables finetuning **65B** on **single 48GB GPU**. (Dettmers et al., 2023, arXiv/NeurIPS)
- QLoRA reduces finetuning memory for 65B from **>780GB** to **<48GB**. (Dettmers et al., 2023, NeurIPS PDF)
- Trainable parameters: QLoRA trains LoRA adapters; base model is frozen and quantized. (Dettmers et al., 2023, arXiv/NeurIPS)

### NF4 vs FP4 / Int4 (quantization quality)
- NF4 is described as information-theoretically optimal for normally distributed weights. (Dettmers et al., 2023, arXiv/NeurIPS)
- NF4 + double quantization matches BF16 performance; FP4 is ~**1 percentage point behind** in the cited table description. (Dettmers et al., 2023, NeurIPS PDF snippet)

### Merged vs unmerged LoRA at inference
- Unmerged LoRA adds overhead; merging removes it. (Fireworks AI docs)
- Fireworks AI quantifies unmerged overhead:
  - TTFT overhead: “tens of milliseconds”
  - Prompt processing time: **+10–30%**
  (Fireworks AI docs, https://docs.fireworks.ai/guides/understanding_lora_performance)
- NVIDIA NIM blog: merging avoids additional inference latency but is less flexible (single task per deployment); dynamic loading supports serving/batching multiple tasks concurrently. (NVIDIA blog, https://developer.nvidia.com/blog/seamlessly-deploying-a-swarm-of-lora-adapters-with-nvidia-nim/)

---

## Architecture & Design Rationale

### Why low-rank updates (LoRA)
- LoRA is motivated by the idea that adaptation can be achieved by injecting trainable low-rank matrices while freezing base weights, reducing trainable parameters and memory. (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- LoRA’s design enables task switching by storing small adapter weights separately and (optionally) merging them into base weights for deployment without extra latency. (Hu et al., 2021, arXiv; Microsoft LoRA GitHub, https://github.com/microsoft/LoRA)

### Why merging removes inference overhead
- When adapters are served dynamically (unmerged), inference must apply additional computations per adapted layer; merging pre-applies the update into the base weights so runtime uses the standard forward path. (Fireworks AI docs; NVIDIA NIM blog)

### Why NF4 and double quantization (QLoRA)
- NF4 is designed for normally distributed weights and is claimed information-theoretically optimal for that distribution. (Dettmers et al., 2023, arXiv/NeurIPS)
- Double quantization reduces overhead by quantizing the quantization constants; saves ~0.37 bits/parameter (~3GB for 65B). (Dettmers et al., 2023, NeurIPS PDF)
- Paged optimizers use NVIDIA Unified Memory paging to manage memory spikes. (Dettmers et al., 2023, NeurIPS PDF)

### Why `layers_pattern` matters in PEFT scoping
- In PEFT, `target_modules` matches module names; if those names appear in multiple submodules (common in multimodal models), you may need `layers_to_transform` + `layers_pattern` to scope which layer container indices apply to. (PEFT issue #2155, https://github.com/huggingface/peft/issues/2155)

---

## Common Questions & Answers

### Q1) Does LoRA add inference latency?
- LoRA is reported to have “no additional inference latency” (contrasted with adapters). (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- In practice, serving **unmerged** adapters can slow inference; Fireworks AI attributes slowdown partly to “unmerged LoRA weights” and reports prompt processing time increases by **10–30%** and TTFT overhead on the order of **tens of milliseconds**. (Fireworks AI docs, https://docs.fireworks.ai/guides/understanding_lora_performance)
- Reconciliation: LoRA can be merged to eliminate overhead; unmerged serving introduces overhead. (Fireworks AI docs; NVIDIA NIM blog)

### Q2) What exactly does `merge_and_unload()` do in PEFT?
- `model.merge_and_unload()` “will merge the LoRA weights into the base weights.” (PEFT discussion #1727, 2024, https://github.com/huggingface/peft/discussions/1727)
- If you want to remove adapters without merging, use `model.unload()`. (PEFT discussion #1727)

### Q3) Why do I get “Target modules … not found in the base model”?
- PEFT’s `target_modules` matches module names by exact/suffix match (list) or regex (string). If names don’t match the model’s module naming, PEFT raises this error. (PEFT `config.py`, https://github.com/huggingface/peft/blob/main/src/peft/tuners/lora/config.py)
- If you use `layers_to_transform`, you may also need to set `layers_pattern` to the correct layer container name (e.g., `"layers"`). (PEFT issue #2155, https://github.com/huggingface/peft/issues/2155)

### Q4) What files must a LoRA adapter include for NVIDIA NIM?
- Hugging Face Transformers format: must include `adapter_config.json` and one of `adapter_model.safetensors` or `adapter_model.bin`. (NVIDIA NIM docs, https://docs.nvidia.com/nim/large-language-models/latest/peft.html)
- NeMo format: directory must contain one `.nemo` file. (NVIDIA NIM docs, URL above)

### Q5) What is NF4 and why is it used in QLoRA?
- QLoRA introduces “4-bit NormalFloat (NF4), a new data type that is information theoretically optimal for normally distributed weights.” (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314; NeurIPS PDF)

### Q6) What does `bnb_4bit_compute_dtype` control?
- It is “the type that is used for the multiplication”; weights are decompressed to that type for matmul; outputs are converted back to the original input dtype. (bitsandbytes issue #1515, 2025, https://github.com/bitsandbytes-foundation/bitsandbytes/issues/1515)

### Q7) What is `prepare_model_for_kbit_training()` for?
- It is used “to set up the gradient flow and do quantization in the proper way so that gradients flow through the quantized weights.” (bitsandbytes issue #1515, 2025, URL above)

### Q8) Which target modules are supported by NVIDIA NIM for LoRA?
- HF format supported target modules: `["gate_proj","o_proj","up_proj","down_proj","k_proj","q_proj","v_proj"]`. (NVIDIA NIM docs, https://docs.nvidia.com/nim/large-language-models/latest/peft.html)
- NeMo format additionally supports `"attention_qkv"` (and notes fused QKV). (NVIDIA NIM docs, URL above)