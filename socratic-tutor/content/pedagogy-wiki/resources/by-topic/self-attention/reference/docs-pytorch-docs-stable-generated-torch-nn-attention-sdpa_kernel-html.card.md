# Card: SDPA kernel selection via `torch.nn.attention.sdpa_kernel`
**Source:** https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Backend-selection semantics (FLASH_ATTENTION / EFFICIENT_ATTENTION / MATH), priority rules, and the exact context-manager mechanism that determines which SDPA kernel runs

## Key Content
- **Purpose:** `torch.nn.attention.sdpa_kernel(...)` is a **context manager** that controls which backend implementation is used by PyTorch’s **Scaled Dot-Product Attention (SDPA)** (e.g., `torch.nn.functional.scaled_dot_product_attention`).
- **Backends (explicit names):**
  - `FLASH_ATTENTION`
  - `EFFICIENT_ATTENTION`
  - `MATH`
- **Mechanism (workflow):**
  1. Enter `with torch.nn.attention.sdpa_kernel(...):`
  2. Inside the block, SDPA calls will **attempt to use only the allowed backend(s)** specified by the context.
  3. On exit, the previous SDPA backend configuration is restored (standard context-manager scoping).
- **Selection / priority semantics:**
  - When multiple backends are enabled in the context, PyTorch uses an internal **priority order** among `FLASH_ATTENTION`, `EFFICIENT_ATTENTION`, and `MATH` to pick the first applicable kernel for the given inputs/device.
  - If a higher-priority backend is enabled but **not applicable** for the current call (due to constraints such as device/dtype/shape/support), PyTorch **falls back** to the next enabled backend in the priority chain.
- **Default behavior control:** Use this context manager to **force math** (for debugging/numerical comparisons) or to **prefer fused kernels** (for performance) by enabling/disabling specific backends.

## When to surface
Use when a student asks “Which SDPA kernel is PyTorch using?”, “How do I force Flash/Efficient/Math attention?”, or “Why did SDPA fall back to math instead of flash?”