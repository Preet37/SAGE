## Key Facts & Specifications

### LoRA (Low-Rank Adaptation)
- **Core method**: LoRA **freezes** pre-trained weights and **injects trainable rank-decomposition matrices** into Transformer layers for downstream adaptation. (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- **Update parameterization**: For a pre-trained weight matrix \(W_0 \in \mathbb{R}^{d \times k}\), LoRA constrains the update via:
  - \(W_0 + \Delta W = W_0 + BA\), where \(B \in \mathbb{R}^{d \times r}\), \(A \in \mathbb{R}^{r \times k}\), and \(r \ll \min(d,k)\). (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)
- **No additional inference latency (by construction)**: At deployment, compute and store \(W = W_0 + BA\) and run inference “as usual”; switching tasks can be done by subtracting/adding different \(BA\) terms. (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)
- **Reported scaling results (GPT-3 175B)**:
  - LoRA can reduce **trainable parameters by 10,000×** and **GPU memory requirement by 3×** compared to GPT-3 175B fine-tuned with Adam. (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- **Which attention matrices to adapt (GPT-3 175B study)**:
  - Under a fixed **parameter budget of 18M** (≈ **35MB in FP16**), adapting **both \(W_q\) and \(W_v\)** gave the best overall performance; adapting only \(W_q\) or only \(W_k\) was “significantly lower.” (Hu et al., 2021, Table 5 discussion, https://arxiv.org/html/2106.09685v2)
  - In that setup: **18M parameters corresponds to \(r=8\)** if adapting **one** attention weight type, or **\(r=4\)** if adapting **two** types, across **96 layers**. (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)
- **Trainable parameter count formula (as stated in LoRA paper)**:
  - When applying LoRA to self-attention weights, trainable parameters are:  
    \(|\Theta| = 2 \times \hat{L}_{\text{LoRA}} \times d_{\text{model}} \times r\), where \(\hat{L}_{\text{LoRA}}\) is the number of weight matrices LoRA is applied to. (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)

### QLoRA (Quantized LoRA)
- **Goal/claim**: QLoRA reduces memory enough to fine-tune a **65B** parameter model on a **single 48GB GPU** while preserving **full 16-bit finetuning task performance**. (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314)
- **Mechanism**: Backpropagates gradients through a **frozen, 4-bit quantized** pretrained model into LoRA adapters. (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314)
- **Memory comparison (65B)**:
  - Regular 16-bit finetuning of **LLaMA 65B** requires **more than 780 GB** of GPU memory (paper statement). (Dettmers et al., 2023 NeurIPS PDF, https://proceedings.neurips.cc/paper_files/paper/2023/file/1feb87871436031bdc0f2beaa62a049b-Paper-Conference.pdf)
  - QLoRA reduces average memory requirements for finetuning a **65B** model from **>780GB** to **<48GB**. (Dettmers et al., 2023 NeurIPS PDF, same URL)
- **NF4**:
  - NF4 is a **4-bit data type** from the QLoRA paper, “adapted for weights initialized from a normal distribution,” and is recommended for **training 4-bit base models**. (Transformers bitsandbytes docs, https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)
  - QLoRA paper: NF4 is “information theoretically optimal for normally distributed weights.” (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314)
- **Double quantization**:
  - QLoRA paper: saves **about 0.37 bits per parameter** on average (≈ **3 GB for a 65B model**). (Dettmers et al., 2023 NeurIPS PDF, same URL)
  - Detailed derivation in paper (blocksize 64 example): constants overhead reduced from **0.5 bits/param** to **0.127 bits/param**, a reduction of **0.373 bits/param**. (Dettmers et al., 2023 NeurIPS PDF, same URL)
- **Paged optimizers**:
  - Use **NVIDIA unified memory** to manage memory spikes (paper). (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314)
  - Paper runtime note: for **65B on 48GB GPUs**, with **batch size 16**, paged optimizers provide the **same training speed** as regular optimizers (as reported). (Dettmers et al., 2023 NeurIPS PDF, same URL)
- **Vicuna benchmark result (Guanaco)**:
  - Guanaco reaches **99.3%** of ChatGPT performance level on the Vicuna benchmark and requires **24 hours** of finetuning on a single GPU (paper claim). (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314)

### BitsAndBytes / Transformers quantization facts
- **8-bit quantization**: “halves the memory-usage” (Transformers docs). (https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)
- **Nested (double) quantization**: saves an additional **0.4 bits/parameter** (Transformers v4.46.0 bitsandbytes docs). (https://huggingface.co/docs/transformers/v4.46.0/quantization/bitsandbytes)
  - **Discrepancy note**: QLoRA paper reports **0.373 bits/parameter** reduction (Dettmers et al., 2023 NeurIPS PDF), while Transformers docs summarize nested quantization as **0.4 bits/parameter**. Treat as different reporting precision/rounding. (Both URLs above)
- **Hardware minimums (Transformers docs)**:
  - NF4/FP4 quantization: **NVIDIA Pascal (GTX 10X0 series, P100) or newer GPUs**. (Transformers bitsandbytes docs, https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)
  - LLM.int8(): **NVIDIA Turing (RTX 20X0 series, T4) or newer GPUs**. (same URL)

### Full fine-tuning memory arithmetic examples (authoritative blog sources in results)
- **Google Cloud example (4B model, BF16)**:
  - Model size: **4B × 2 bytes = 8 GB**
  - Gradients: **4B × 2 bytes = 8 GB**
  - Optimizer states (AdamW): **2 × 4B × 2 bytes = 16 GB**
  - Baseline static HBM: **32 GB** (8 + 8 + 16). (Google Cloud blog, https://cloud.google.com/blog/topics/developers-practitioners/decoding-high-bandwidth-memory-a-practical-guide-to-gpu-memory-for-fine-tuning-ai-models/)
- **Same Google Cloud post, LoRA example (adds 20M trainable params)**:
  - LoRA gradients: **20M × 2 bytes = 40 MB**
  - LoRA optimizer states: **2 × 20M × 2 bytes = 80 MB**
  - New static HBM: **≈ 8.12 GB** (8 GB + 40 MB + 80 MB). (same URL)

### Empirical compute/memory trade-off (single-source benchmark)
- QLoRA trade-off reported in one experiment:
  - Memory savings: **33%**
  - Runtime increase: **39%**
  - Example numbers:
    - LoRA (16-bit bf16): **1.85 h**, **21.33 GB**
    - QLoRA (4-bit Normal Floats): **2.79 h**, **14.18 GB**  
  (Sebastian Raschka, “Practical Tips…”, https://magazine.sebastianraschka.com/p/practical-tips-for-finetuning-llms)

---

## Technical Details & Procedures

### LoRA math and deployment procedure (paper)
- **Training-time**:
  - Keep \(W_0\) frozen; train only \(A\) and \(B\) such that \(\Delta W = BA\). (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)
- **Inference-time merge**:
  - Compute/store merged weights \(W = W_0 + BA\) to avoid extra inference latency. (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)

### Hugging Face PEFT: `LoraConfig` parameters (reference)
From PEFT LoRA docs (Hugging Face):
- Key fields and defaults shown in docs:
  - `r: int = 8`
  - `lora_alpha: int = 8`
  - `lora_dropout: float = 0.0`
  - `target_modules: Optional[Union[list[str], str]] = None`
  - `exclude_modules: Optional[...] = None`
  - `fan_in_fan_out: bool = False` (set `True` for GPT-2 `Conv1D` weight layout)
  - `bias: Literal['none','all','lora_only'] = 'none'`
  - `use_rslora: bool = False` (scaling becomes `lora_alpha/math.sqrt(r)` vs default `lora_alpha/r`)
  - `modules_to_save: Optional[list[str]] = None`
  - `init_lora_weights`: default init sets **LoRA B weight to 0**, making adapter a **no-op before training**.  
  (PEFT docs, https://huggingface.co/docs/peft/en/package_reference/lora)
- `target_modules` behavior:
  - If `'all-linear'`, targets all linear/Conv1D modules (excluding output layer if model is a `PreTrainedModel`).
  - If unspecified, modules chosen by architecture; if unknown, error and user must specify.
  - String uses regex match; list uses exact match or suffix match.  
  (PEFT docs, same URL)
- `bias` warning:
  - If `bias` is `'all'` or `'lora_only'`, biases are updated; even when disabling adapters, output may differ from base model. (PEFT docs, same URL)

### PEFT: applying LoRA (code pattern shown in docs)
- Example (Seq2Seq):
```python
from transformers import AutoModelForSeq2SeqLM
from peft import LoraModel, LoraConfig

config = LoraConfig(
    task_type="SEQ_2_SEQ_LM",
    r=8,
    lora_alpha=32,
    target_modules=["q", "v"],
    lora_dropout=0.01,
)

model = AutoModelForSeq2SeqLM.from_pretrained("t5-base")
lora_model = LoraModel(model, config, "default")
```
(PEFT docs, https://huggingface.co/docs/peft/package_reference/lora)

### PEFT: merging LoRA into base model (`merge_and_unload`)
- Forum-confirmed workflow:
  - A `PeftModelForCausalLM` inherits LoRA merge methods; you can call:
    - `merged_model = model_to_merge.merge_and_unload()`  
  (Hugging Face forum thread, https://discuss.huggingface.co/t/help-with-merging-lora-weights-back-into-base-model/40968)
- Example steps (from same thread; includes saving adapter then merging):
```python
peft_model.save_pretrained(lora_adapter, save_adapter=True, save_config=True)

model_to_merge = PeftModel.from_pretrained(
    AutoModelForCausalLM.from_pretrained(base_model, torch_dtype=torch.bfloat16),
    lora_adapter
)
merged_model = model_to_merge.merge_and_unload()
merged_model.save_pretrained(merged_model)
```
(Forum thread, same URL)
- **Disk size note (forum explanation)**:
  - Merged model has parameters of base model **plus** inserted LoRA adapter parameters; thus `# params merged_model > # params base_model`, increasing size. (Forum thread, same URL)
  - Ensure same dtype on reload to maintain comparable size (example uses `torch_dtype=torch.bfloat16`). (Forum thread, same URL)

### PEFT: saving additional fully-tuned modules with LoRA adapters (`modules_to_save`)
- If combining LoRA with selective full fine-tuning, recommended approach is to set those layers in `modules_to_save=[...]` so they are saved inside `adapter_model.safetensors` and restored when loading adapter. (PEFT GitHub issue #2647, https://github.com/huggingface/peft/issues/2647)

### Transformers + bitsandbytes: quantized loading via `BitsAndBytesConfig`
- **8-bit example**:
```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
quantization_config = BitsAndBytesConfig(load_in_8bit=True)
model_8bit = AutoModelForCausalLM.from_pretrained(
    "bigscience/bloom-1b7",
    device_map="auto",
    quantization_config=quantization_config
)
```
(Transformers docs, https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)
- **4-bit + compute dtype example**:
```python
import torch
from transformers import BitsAndBytesConfig
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)
```
(Transformers docs, same URL)
- **NF4 example**:
```python
from transformers import BitsAndBytesConfig
nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
)
model_nf4 = AutoModelForCausalLM.from_pretrained(
    model_id, dtype="auto", quantization_config=nf4_config
)
```
(Transformers docs, same URL)
- **Double quantization example**:
```python
from transformers import BitsAndBytesConfig
double_quant_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
)
```
(Transformers docs, same URL)
- **HF blog quickstart**:
  - Load 4-bit with `load_in_4bit=True` and `device_map="auto"`. (HF blog, https://huggingface.co/blog/4bit-transformers-bitsandbytes)
  - Recommendation: avoid manual `.to(device)` after loading with `device_map`. (same URL)

### PEFT developer guide: merging multiple LoRA adapters (TIES/DARE)
- Load base model, load multiple adapters with names, then merge via `add_weighted_adapter()` with:
  - `combination_type` (e.g., `"ties"`)
  - `density` (fraction of weights to keep)
  - weights often start at `1.0`; values > `1.0` “typically produce better results” (guide statement).  
  (PEFT developer guide, https://huggingface.co/docs/peft/developer_guides/model_merging)
- Example:
```python
adapters = ["norobots", "adcopy", "sql"]
weights = [2.0, 1.0, 1.0]
adapter_name = "merge"
density = 0.2
model.add_weighted_adapter(adapters, weights, adapter_name, combination_type="ties", density=density)
```
(PEFT developer guide, same URL)

---

## Comparisons & Trade-offs

### LoRA vs full fine-tuning (paper + memory examples)
- LoRA vs full fine-tuning on GPT-3 175B:
  - **10,000× fewer trainable parameters** and **3× less GPU memory** (LoRA paper). (Hu et al., 2021, https://arxiv.org/abs/2106.09685)
- Memory overhead reduction illustrated (Google Cloud example):
  - Full FT baseline static HBM for 4B BF16 model: **32 GB** (model + grads + AdamW states). (Google Cloud blog URL above)
  - With LoRA adding 20M trainable params: static HBM **≈ 8.12 GB**; training overhead shrinks from **24 GB** to **120 MB** (40MB grads + 80MB optimizer). (same URL)

### LoRA vs adapters (inference latency)
- LoRA paper explicitly contrasts with adapters:
  - LoRA has **no additional inference latency**, “unlike adapters.” (Hu et al., 2021, https://arxiv.org/abs/2106.09685)

### QLoRA vs LoRA (memory vs runtime)
- Raschka benchmark:
  - QLoRA: **33% memory savings** but **39% increased runtime** (in that experiment). (Raschka URL above)
- Unsloth doc claims (guidance, not a benchmark):
  - LoRA (16-bit) “slightly faster and slightly more accurate” but uses “significantly more VRAM (4× more than QLoRA).”
  - QLoRA uses 4-bit precision, “reducing VRAM usage by over 75%.”  
  (Unsloth guide, https://unsloth.ai/docs/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)  
  **Note**: These are guidance statements; they may not match Raschka’s measured 33% memory savings.

### NF4 vs FP4 / Int4 (QLoRA paper)
- QLoRA paper states NF4 yields “better empirical results than 4-bit Integers and 4-bit Floats.” (Dettmers et al., 2023 NeurIPS PDF, same URL)

---

## Architecture & Design Rationale

### Why low-rank updates (LoRA)
- LoRA hypothesis: weight updates during adaptation have low “intrinsic rank,” inspired by findings that learned over-parameterized models can reside on a low intrinsic dimension. (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)
- LoRA’s bottleneck structure imposes a low-rank constraint on updates while keeping \(W_0\) frozen. (Hu et al., 2021, same URL)

### Why merging eliminates inference latency (LoRA)
- Because \(BA\) has the same shape as \(W_0\), you can precompute \(W = W_0 + BA\) and run the same forward pass as the base model. (Hu et al., 2021, same URL)

### Why NF4 and double quantization (QLoRA)
- NF4 is designed for weights “initialized from a normal distribution” and is recommended for training 4-bit base models. (Transformers bitsandbytes docs URL above)
- Double quantization targets the overhead of quantization constants; QLoRA provides explicit bit accounting showing reduction to **0.127 bits/param** (from **0.5 bits/param**) for constants in a blocksize-64 example. (Dettmers et al., 2023 NeurIPS PDF)

### Why paged optimizers (QLoRA)
- Paged optimizers use NVIDIA unified memory to avoid OOM from memory spikes (especially with long sequences / checkpointing). (Dettmers et al., 2023, https://arxiv.org/abs/2305.14314)

---

## Common Questions & Answers

### 1) “What exactly is trained in LoRA?”
- Only the low-rank matrices \(A\) and \(B\) are trained; the pre-trained weights \(W_0\) are frozen, and the effective weight is \(W_0 + BA\). (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)

### 2) “Why does LoRA not add inference latency?”
- You can merge the adapter into the base weight by computing and storing \(W = W_0 + BA\) and then run inference normally; this “guarantees” no additional latency compared to a fine-tuned model. (Hu et al., 2021, https://arxiv.org/html/2106.09685v2)

### 3) “Which attention projections should I target first?”
- In LoRA’s GPT-3 175B study with a fixed 18M parameter budget, adapting **both \(W_q\) and \(W_v\)** gave the best overall results; adapting only \(W_q\) or only \(W_k\) was significantly worse. (Hu et al., 2021, Table 5 discussion, https://arxiv.org/html/2106.09685v2)

### 4) “How does QLoRA make 65B fine-tuning possible on one GPU?”
- QLoRA fine-tunes by backpropagating through a **frozen 4-bit quantized** base model into LoRA adapters, and introduces NF4, double quantization, and paged optimizers; it reports reducing 65B finetuning memory from **>780GB** to **<48GB**. (Dettmers et al., 2023 NeurIPS PDF, same URL)

### 5) “How much memory does double quantization save?”
- QLoRA reports saving **0.373 bits per parameter** (blocksize-64 example), and summarizes this as “about **0.37 bits/parameter**,” approximately **3 GB for a 65B model**. (Dettmers et al., 2023 NeurIPS PDF)

### 6) “How do I load a model in 4-bit NF4 with Transformers?”
```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig

nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    model_id,
    dtype="auto",
    quantization_config=nf4_config,
)
```
(Transformers bitsandbytes docs, https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)

### 7) “How do I merge a trained LoRA adapter back into the base model in PEFT?”
- A `PeftModelForCausalLM` can call `merge_and_unload()` to return a base model with LoRA applied. (HF forum, https://discuss.huggingface.co/t/help-with-merging-lora-weights-back-into-base-model/40968)

### 8) “Why did my saved model get bigger after merging?”
- Forum explanation: merged model has base parameters **plus** inserted LoRA adapter parameters, so parameter count (and size) increases. Also, dtype mismatches on reload can affect size; use consistent `torch_dtype`. (HF forum thread URL above)

### 9) “How do I ensure some layers are fully fine-tuned and saved alongside the adapter?”
- Use `modules_to_save=[...]` in `LoraConfig` so those layers are stored in `adapter_model.safetensors` and restored when loading the adapter. (PEFT issue #2647, https://github.com/huggingface/peft/issues/2647)

### 10) “What are the minimum GPU requirements for NF4/FP4 quantization?”
- Transformers docs list **NVIDIA Pascal (GTX 10X0 series, P100) or newer** for NF4/FP4 quantization. (Transformers bitsandbytes docs, https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)