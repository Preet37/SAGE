# Card: bitsandbytes 4-bit Linear Layers (QLoRA)
**Source:** https://github.com/bitsandbytes-foundation/bitsandbytes/blob/main/docs/source/reference/nn/linear4bit.mdx  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact API surface for bitsandbytes 4-bit layers used in QLoRA-style finetuning: `Linear4bit`, `LinearFP4`, `LinearNF4`, and `Params4bit` (all via autodoc of their `__init__`).

## Key Content
- **QLoRA procedure (high-level workflow):**  
  1) **Quantize** a pretrained model’s weights to **4-bit**.  
  2) **Add LoRA** (low-rank adaptation) weights.  
  3) **Finetune LoRA parameters** “through the quantized weights” (i.e., base weights remain quantized while adapters are trained).  
  *(Section: “4-bit quantization”)*

- **4-bit layer/data-type options (design rationale):**
  - Introduces **two 4-bit quantization data types** for linear layers:  
    - **Float4** via `LinearFP4` (“standard Float4 data type”).  
    - **NormalFloat 4-bit** via `LinearNF4` (“4-bit NormalFloat”).  
  - **Rationale for NF4:** `LinearNF4` is “a quantization data type for **normally distributed data**” and **can improve performance** vs standard Float4.  
  *(Section: “4-bit quantization”)*

- **API entry points (consult autodoc for exact parameters/defaults):**
  - `bitsandbytes.nn.Linear4bit.__init__`
  - `bitsandbytes.nn.LinearFP4.__init__`
  - `bitsandbytes.nn.LinearNF4.__init__`
  - `bitsandbytes.nn.Params4bit.__init__`
  *(Sections: Linear4bit / LinearFP4 / LinearNF4 / Params4bit)*

## When to surface
Use when students ask which bitsandbytes 4-bit linear class to choose for QLoRA (FP4 vs NF4), or when they need the authoritative constructor/API details for `Linear4bit`/`LinearNF4`/`LinearFP4` and `Params4bit`.