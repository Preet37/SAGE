# Card: PyTorch SDPA backend enum (SDPBackend)
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.SDPBackend.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative enum of Scaled Dot-Product Attention (SDPA) backends and their intended meaning/usage in code

## Key Content
- **Object:** `torch.nn.attention.SDPBackend` (an enum) used to **select/identify which implementation (“backend”)** PyTorch uses for **scaled dot-product attention (SDPA)**.
- **Backends (enum members):**
  - `SDPBackend.MATH` — **math/reference** implementation of SDPA (general-purpose; correctness-oriented).
  - `SDPBackend.FLASH_ATTENTION` — **FlashAttention**-style fused kernel backend for SDPA (performance-oriented when supported).
  - `SDPBackend.EFFICIENT_ATTENTION` — **memory-efficient attention** backend for SDPA (optimized for reduced memory use when supported).
  - `SDPBackend.CUDNN_ATTENTION` — **cuDNN attention** backend for SDPA (uses cuDNN-provided implementation when supported).
- **How it’s used (conceptually):**
  - The enum values are passed/checked by SDPA-related APIs to **control or report** which backend is active for an attention call.
  - Typical usage pattern is “choose a backend” (e.g., prefer fused kernels) while retaining a safe fallback (`MATH`) when specialized kernels are unavailable.
- **Terminology alignment:** “SDP” here refers to **Scaled Dot-Product Attention** (the operation underlying transformer attention).

## When to surface
Use this card when a student asks: “What SDPA backends does PyTorch support?”, “What does `SDPBackend.FLASH_ATTENTION` mean?”, or “How do I force/identify the attention kernel PyTorch is using?”