## Core Definitions

**Pre-training**  
Chip Huyen describes pretraining as the most resource-intensive phase in building systems like ChatGPT, noting that for InstructGPT, pretraining consumed **98% of overall compute and data resources**; conceptually it is the phase where a model is trained on large-scale, broad, “indiscriminate” internet data before instruction tuning and RLHF polish it for user-facing behavior (Huyen, *RLHF*). The vLLM paper states the autoregressive language-modeling objective as a product of next-token probabilities over a sequence, i.e., predicting tokens sequentially conditioned on prior tokens (Kwon et al., *vLLM*).

**Data curation**  
The Pile paper operationalizes data curation as constructing a large corpus from many component datasets with explicit **mixture weighting/upsampling**, plus preprocessing steps like extracting text from Common Crawl WARC using **jusText**, and applying filtering/dedup and evaluation decontamination (e.g., **13-gram overlap filtering**) to reduce benchmark contamination (Gao et al., *The Pile*).

**Distributed training**  
PyTorch’s DDP documentation defines distributed data-parallel training as wrapping a module so that replicas on multiple processes/GPUs **all-reduce gradients** across a process group; it does **not shard inputs**, so the user must shard data (e.g., `DistributedSampler`) (PyTorch docs, *DistributedDataParallel*). PyTorch’s FSDP docs define fully sharded training as sharding **parameters (and typically gradients and optimizer state)** across ranks, using **all-gather** to materialize parameters for compute and **reduce-scatter** to shard gradients (PyTorch docs, *FSDP*; PyTorch tutorial, *FSDP2*).

**Data parallelism**  
DDP is the canonical PyTorch implementation: each rank holds a full model replica, processes different data, and synchronizes by **all-reducing gradients** (PyTorch docs, *DDP*). Megatron-LM describes composing data parallelism with tensor model parallelism by forming tensor-parallel groups of size \(t\) and data-parallel groups of size \(d\) such that total GPUs \(n=t\cdot d\) (Shoeybi et al., *Megatron-LM*).

**Tensor parallelism (tensor model parallelism / intra-layer parallelism)**  
Megatron-LM defines tensor model parallelism as splitting individual layer weight matrices across GPUs (e.g., partitioning Transformer MLP and attention projection matrices) so each GPU computes partial results, then uses collectives (e.g., **all-reduce**, **all-gather**) to assemble the full activations/gradients needed for correctness (Shoeybi et al., *Megatron-LM*).

**Mixed precision**  
PyTorch AMP defines mixed precision as running some operations in **float32** for stability (e.g., reductions) and others in a lower precision (`float16` or `bfloat16`) for speed, using `torch.autocast` to choose dtypes per op and (for fp16) `GradScaler` to mitigate gradient underflow by scaling/unscaling the loss and gradients (PyTorch docs, *AMP*; *AMP examples*). The FP16 mixed-precision paper formalizes loss scaling and dynamic loss scaling to avoid fp16 underflow/overflow while keeping FP32 master weights for updates (Micikevicius et al., 2017).

**bf16 (bfloat16)**  
The BF16 paper defines BFLOAT16 as a 16-bit floating format that keeps **FP32-like exponent range** (same exponent bits as FP32) but fewer mantissa bits, enabling mixed-precision training that often avoids FP16-style loss scaling due to reduced underflow/overflow risk; it reports empirical convergence/accuracy parity with FP32 across tasks (Kalamkar et al., 2019).

---

## Key Formulas & Empirical Results

### Autoregressive LM objective (serving paper, but objective is general)
\[
P(x_{n+1:n+T}\mid x_{1:n})=\prod_{t=1}^{T} P(x_{n+t}\mid x_{1:n+t-1})
\]
- Supports: what “next-token prediction” means mechanically (Kwon et al., *vLLM*).

### Training compute approximations & scaling laws
- **Kaplan et al. compute**: \(C \approx 6 N B S\) FLOPs (non-embedding params), where \(N\)=params, \(B\)=batch tokens, \(S\)=steps (Kaplan et al., 2020).  
- **Chinchilla compute model**: \(\text{FLOPs}(N,D)\approx 6ND\), where \(D\)=training tokens (Hoffmann et al., 2022).  
- **Chinchilla compute-optimal frontier**:
\[
N_{\text{opt}}(C)=G\left(\frac{C}{6}\right)^a,\quad D_{\text{opt}}(C)=G^{-1}\left(\frac{C}{6}\right)^b
\]
with \(G=\left(\frac{\alpha A}{\beta B}\right)^{\frac{1}{\alpha+\beta}}\), \(a=\frac{\beta}{\alpha+\beta}\), \(b=\frac{\alpha}{\alpha+\beta}\) (Hoffmann et al., 2022).  
- **Empirical exponents (Chinchilla Table 2)**: \(a\approx 0.46\text{–}0.50\), \(b\approx 0.50\text{–}0.54\) → tokens scale roughly proportionally with parameters at compute-optimality (Hoffmann et al., 2022).

### Megatron-LM tensor-parallel communication & composition
- **Per-layer tensor-parallel comm volume**: approx \(\approx 8\,b\,s\,h\) elements communicated per layer for tensor-parallel all-reduces (microbatch \(b\), seq \(s\), hidden \(h\)); “twice each in forward and backward” when accounting for attention+MLP patterns (Shoeybi et al., *Megatron-LM*).  
- **Group composition**: total GPUs \(n=t\cdot d\) for tensor-parallel size \(t\) and data-parallel size \(d\) (Shoeybi et al., *Megatron-LM*).  
- **Scaling result**: 8.3B params on **512 GPUs** with **8-way tensor parallelism** achieved **15.1 PFLOP/s** and **76%** scaling efficiency vs single-GPU baseline (Shoeybi et al., *Megatron-LM*).

### FlashAttention exact speed/memory benchmarks
- For \(N{=}1024,d{=}64\), 16 heads, batch 64 on A100 (fwd+bwd):  
  - Standard attention: **35.3 GB** HBM R/W, **35.1 ms**  
  - FlashAttention: **4.4 GB** HBM R/W, **11.7 ms** (Dao et al., 2022).  
- End-to-end: BERT-large seq 512 on 8×A100: **15% faster** (20.0±1.5 min → 17.4±1.4 min) (Dao et al., 2022).

### PyTorch DDP defaults/knobs (often asked)
- `bucket_cap_mb`: default **25 MiB** when `None` (PyTorch docs, *DDP*).  
- `broadcast_buffers=True` (default): buffers broadcast from rank 0 each iteration (PyTorch docs, *DDP*).  
- `find_unused_parameters=False` (default) (PyTorch docs, *DDP*).  
- `static_graph=False` (default) (PyTorch docs, *DDP*).

### PyTorch AMP defaults/semantics
- `torch.autocast(device_type, dtype=None, enabled=True, cache_enabled=True)`; if `dtype=None`, default dtype is **CUDA: float16**, **CPU: bfloat16** (PyTorch docs, *AMP*).  
- Backward under autocast is “not recommended”; backward runs in the dtype used by corresponding forward ops (PyTorch docs, *AMP*).

### FP16 numeric limits (why loss scaling exists)
- FP16 max normalized: **65,504**; min normalized: \(2^{-14}\approx 6.10\times 10^{-5}\); min denormal: \(2^{-24}\approx 5.96\times 10^{-8}\) (Micikevicius et al., 2017).

### BF16 numeric format (range argument)
- BF16 (sign,exp,mant) = (1,8,7); max normal **3.38e38**; min normal **1.17e−38**; **no subnormals** (Kalamkar et al., 2019 PDF Table 1).  
- Empirical parity examples: AlexNet top-1 **57.4% FP32** vs **57.2% BF16**; ResNet-50 FP32 **74.7%** vs BF16 **74.7%** (Kalamkar et al., 2019).

### Production-style throughput (FSDP pretraining benchmark)
- Llama2-7B-style pretraining: **3,700 tokens/sec/GPU** on **128× A100 80GB**, ~**40B tokens/day**, **MFU=57%**, **HFU=57%** (PyTorch blog, *Maximizing Training Throughput*).  
- Claim: near-linear scaling to **512 GPUs**; extrapolated **<2 weeks** to train 7B to **2T tokens** on 512 GPUs (same source).  
- Mixed precision used: **bf16** (same source).

### Float8 + FSDP2 throughput gains (H100)
- Tokens/sec/GPU (wps), seq=8K:  
  - 70B: bf16 **956** → float8 **1430** (**+50%**)  
  - 405B (TP4): **149** → **227** (**+52%**) (PyTorch blog, *Float8 + FSDP2*).  
- At 512 H100s: 70B **960→1448 (+51%)**; 405B **152→217 (+43%)** (same source).

### The Pile: mixture weighting & BPB metric
- The Pile: **825.18 GiB** raw; **22** components; effective size **1254.20 GiB** after upsampling (“epochs”) (Gao et al.).  
- BPB:
\[
\text{BPB} = (L_T/L_B)\cdot \ell/\ln(2)
\]
where \(\ell\)=NLL loss, \(L_T\)=token length, \(L_B\)=UTF-8 byte length; for GPT-2 tokenizer on Pile, \(L_T/L_B=0.29335\) tokens/byte (Gao et al.).

---

## How It Works

### A. Pre-training loop at scale (mechanics the tutor can narrate)
1. **Sample a batch of token sequences** from a curated mixture (e.g., Pile components with upsampling weights) (Gao et al.).  
2. **Forward pass under mixed precision**  
   - Use `torch.autocast("cuda", ...)` to run many ops in lower precision (AMP docs).  
   - Compute next-token logits and the autoregressive loss (objective form in vLLM paper).  
3. **Backward pass**  
   - For fp16: call `scaler.scale(loss).backward()`; grads are scaled to avoid underflow (AMP examples; Micikevicius et al.).  
   - For bf16: often no loss scaling is needed due to FP32-like exponent range (Kalamkar et al.).  
4. **Distributed synchronization (depends on parallelism strategy)**  
   - **DDP (data parallel)**: gradients are **all-reduced** across ranks; parameters are assumed to stay in sync via identical optimizer steps (PyTorch DDP docs).  
   - **FSDP**: parameters are sharded; before each layer’s compute, ranks **all-gather** shards to materialize full params; after backward, grads are **reduce-scattered** back into shards (PyTorch FSDP docs; FSDP2 tutorial).  
   - **Tensor parallel (Megatron)**: within a layer, partial matmuls happen on each GPU; collectives (all-reduce/all-gather) assemble correct activations/gradients (Shoeybi et al.).  
5. **Optimizer step**  
   - FP16 MP: keep **FP32 master weights** and apply update in FP32; copy/convert as needed (Micikevicius et al.).  
   - AMP canonical order: `scaler.step(optimizer)` (unscales internally), then `scaler.update()` (AMP examples).  
6. **Repeat for trillions of tokens**; choose token horizon \(D\) relative to model size \(N\) using compute-optimal guidance (Hoffmann et al.).

### B. Megatron-LM tensor parallelism (Transformer MLP, step-by-step)
**Goal:** split a single layer across \(t\) GPUs (intra-layer).
1. Let MLP weights be \(A\in\mathbb{R}^{H\times 4H}\), \(B\in\mathbb{R}^{4H\times H}\).  
2. **Column-parallel first linear**: split \(A\) column-wise into \(A_i\) across \(t\) GPUs. Each GPU computes \(X A_i\) locally and applies GeLU locally.  
3. **Row-parallel second linear**: split \(B\) row-wise so each GPU consumes its local activation shard; each GPU produces a partial output.  
4. **All-reduce** partial outputs to form the full \(H\)-dimensional output (Shoeybi et al.).  
5. Similar partitioning applies to attention projections (QKV column-parallel; output projection row-parallel) (Shoeybi et al.).  
6. **Compose with data parallelism**: total GPUs \(n=t\cdot d\) (Shoeybi et al.).

### C. PyTorch AMP canonical step ordering (fp16 case)
```python
scaler = torch.amp.GradScaler("cuda")

for batch in loader:
    optimizer.zero_grad(set_to_none=True)
    with torch.autocast("cuda", dtype=torch.float16):
        loss = model(batch).loss
    scaler.scale(loss).backward()

    # optional: unscale then clip
    scaler.unscale_(optimizer)
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

    scaler.step(optimizer)  # skips step if inf/NaN
    scaler.update()
```
- Ordering and constraints (e.g., unscale only once per optimizer per step) are from PyTorch AMP examples.

---

## Teaching Approaches

### Intuitive (no math)
- **Pretraining** is “teaching the model to predict the next token” on a huge, messy corpus; it’s expensive because you do it for trillions of tokens (Huyen notes it dominates compute).  
- **Scaling** requires splitting work across many GPUs: either give each GPU different data (data parallel), shard the model weights (FSDP), or split individual layers (tensor parallel).  
- **Mixed precision** speeds things up by using smaller number formats where safe; bf16 is popular because it keeps FP32-like range (Kalamkar et al.; PyTorch blog uses bf16).

### Technical (with math)
- Use the autoregressive factorization \( \prod_t P(x_{t}\mid x_{<t}) \) (vLLM) and compute model \( \text{FLOPs}\approx 6ND \) (Chinchilla) to connect “tokens trained” to compute.  
- Explain tensor-parallel MLP: column-parallel \(A\), row-parallel \(B\), and why an **all-reduce** is required to sum partial outputs (Megatron-LM).  
- Explain fp16 stability: gradients can underflow below fp16 min normal; loss scaling multiplies loss by \(S\) and later divides grads by \(S\) (Micikevicius et al.).

### Analogy-based
- **Data parallelism**: many chefs each cook the same recipe (same model) on different ingredients (data shards), then average their “taste adjustments” (gradient all-reduce).  
- **FSDP**: the recipe book (parameters) is split across chefs; before cooking a step, they photocopy the needed page (all-gather), then put pages back (reshard) (PyTorch FSDP/FSDP2).  
- **Tensor parallelism**: a single dish step is split—each chef prepares a slice of the sauce (matrix multiply shard), then they combine sauces (all-reduce) (Megatron-LM).

---

## Common Misconceptions

1. **“DDP automatically splits my dataset across GPUs.”**  
   - Why wrong: PyTorch DDP explicitly “does not shard inputs”; the user must shard (e.g., `DistributedSampler`) (DDP docs).  
   - Correct model: DDP synchronizes gradients; *you* ensure each rank sees different data.

2. **“In DDP, parameters are broadcast every iteration to keep replicas identical.”**  
   - Why wrong: DDP docs state parameters are **never broadcast each iteration**; it assumes identical optimizer updates after gradient all-reduce. Only **buffers** may be broadcast each iteration if `broadcast_buffers=True` (default).  
   - Correct model: initialization sync + gradient all-reduce + identical optimizer steps keep params aligned.

3. **“Mixed precision just means converting the whole model to fp16/bf16.”**  
   - Why wrong: AMP docs warn not to manually call `.half()`/`.bfloat16()` when using autocast; autocast chooses per-op dtypes and keeps some ops in fp32 for stability.  
   - Correct model: mixed precision is *selective* precision; forward under autocast, backward outside autocast.

4. **“bf16 is basically fp16, so it needs loss scaling the same way.”**  
   - Why wrong: BF16 keeps FP32-like exponent range (Table 1 in Kalamkar et al. PDF) and is described as often avoiding FP16-style loss scaling; fp16’s limited range motivates scaling (Micikevicius et al.).  
   - Correct model: fp16 often needs scaling due to underflow/overflow risk; bf16 often doesn’t (though you still must manage numerical stability generally).

5. **“Tensor parallelism is just data parallelism with a different name.”**  
   - Why wrong: Megatron-LM tensor parallelism splits *within a layer* (e.g., partitioning \(A\) and \(B\)) and requires intra-layer collectives; data parallelism replicates the full model and all-reduces gradients (Megatron-LM; DDP docs).  
   - Correct model: data parallel = replicate model, split data; tensor parallel = split model computation/weights, coordinate activations/partials.

---

## Worked Examples

### 1) Minimal DDP vs AMP ordering (single-node sketch)
**Purpose:** give the tutor a concrete “what code changes” example grounded in PyTorch docs.

```python
# torchrun --nproc_per_node=8 train.py
import torch, torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

def main():
    dist.init_process_group("nccl")
    local_rank = int(os.environ["LOCAL_RANK"])
    torch.cuda.set_device(local_rank)

    model = MyLM().cuda()
    ddp = DDP(model, device_ids=[local_rank], output_device=local_rank)

    opt = torch.optim.AdamW(ddp.parameters(), lr=3e-4)
    scaler = torch.amp.GradScaler("cuda")

    for batch in loader:  # loader should use DistributedSampler per DDP docs
        opt.zero_grad(set_to_none=True)
        with torch.autocast("cuda", dtype=torch.float16):
            loss = ddp(batch).loss
        scaler.scale(loss).backward()
        scaler.step(opt)
        scaler.update()
```

Tutor notes to surface:
- “DDP does not shard inputs” → must use `DistributedSampler` (DDP docs).  
- Autocast wraps forward+loss only; backward not under autocast (AMP docs).  
- `GradScaler` step/update ordering is canonical (AMP examples).

### 2) Megatron-style tensor-parallel MLP (shape reasoning)
Given hidden size \(H\), MLP expansion \(4H\), tensor-parallel degree \(t\):
- Split \(A\in\mathbb{R}^{H\times 4H}\) into \(t\) column shards \(A_i\in\mathbb{R}^{H\times (4H/t)}\).  
- Each GPU computes \(X A_i\) → activation shard \(\in\mathbb{R}^{b s \times (4H/t)}\).  
- Split \(B\in\mathbb{R}^{4H\times H}\) into \(t\) row shards \(B_i\in\mathbb{R}^{(4H/t)\times H}\).  
- Each GPU computes partial output \(Y_i = \text{GeLU}(X A_i) B_i \in \mathbb{R}^{b s \times H}\).  
- **All-reduce** sum across GPUs to get full \(Y=\sum_i Y_i\) (Megatron-LM).

---

## Comparisons & Trade-offs

| Technique | What is replicated vs sharded? | Main collective(s) | Pros | Cons / when it breaks |
|---|---|---|---|---|
| **DDP (data parallel)** | Full model replicated on each rank | Gradient **all-reduce** | Simple; strong overlap via bucketing (`bucket_cap_mb` default 25 MiB) (DDP docs) | Memory scales poorly with model size (each GPU holds full params/optim state) |
| **FSDP (ZeRO-3-like)** | Params (and grads/optim state) **sharded** across ranks | **all-gather** params; **reduce-scatter** grads (FSDP docs; FSDP2 tutorial) | Much lower memory; enables larger models | More communication orchestration; peak memory depends on prefetch/reshard settings |
| **Tensor parallel (Megatron)** | Individual layer weights/compute sharded within a layer | **all-reduce/all-gather** within layer (Megatron-LM) | Enables models too large for single GPU even with sharding; good for very large layers/vocab | Requires careful partitioning; adds intra-layer comm; often combined with data parallel |

When to choose (grounded guidance):
- If model fits per GPU: start with **DDP** (DDP docs describe it as gradient all-reduce wrapper).  
- If memory is the bottleneck: **FSDP/FSDP2** (docs define sharding of params/grads/optim state).  
- If even sharded params per rank are too large or you need intra-layer scaling: add **tensor parallelism** (Megatron-LM composition \(n=t\cdot d\)).

---

## Prerequisite Connections

- **Autoregressive next-token prediction**: needed to understand what pretraining optimizes (objective in vLLM).  
- **Backprop + gradient-based optimization**: needed to understand why gradients must be synchronized and why loss scaling works (AMP examples; Micikevicius et al.).  
- **Collective communication (all-reduce/all-gather/reduce-scatter)**: needed to reason about DDP/FSDP/tensor-parallel correctness and bottlenecks (DDP docs; FSDP docs; Megatron-LM).  
- **Floating-point formats (fp16 vs bf16)**: needed to understand stability/throughput tradeoffs and why bf16 often avoids loss scaling (AMP docs; Kalamkar et al.; Micikevicius et al.).

---

## Socratic Question Bank

1. **If DDP “doesn’t shard inputs,” what *must* you change in the dataloader to avoid every GPU seeing identical batches?**  
   - Good answer: use a distributed sampler / per-rank sharding; DDP only syncs grads (DDP docs).

2. **Why does Megatron’s tensor-parallel MLP need an all-reduce after the second linear? What would be wrong without it?**  
   - Good answer: each GPU produces a partial contribution to the same \(H\)-dim output; must sum partials to match the full matmul (Megatron-LM).

3. **In AMP, why is backward under autocast “not recommended”? What dtype does backward use instead?**  
   - Good answer: backward uses the dtype chosen for corresponding forward ops; autocast is intended for forward/loss region (AMP docs).

4. **What numerical problem does loss scaling solve in fp16, and what’s the basic mechanism?**  
   - Good answer: fp16 grads underflow to 0; scale loss by \(S\), backprop scaled grads, then unscale before update (Micikevicius et al.; AMP docs).

5. **Why might bf16 reduce the need for loss scaling compared to fp16?**  
   - Good answer: bf16 keeps FP32-like exponent range (Kalamkar et al. Table 1), reducing underflow/overflow risk.

6. **If you have a fixed compute budget, what does Chinchilla suggest about how tokens \(D\) should scale with parameters \(N\)?**  
   - Good answer: compute-optimal exponents \(a\approx b\approx 0.5\) imply scaling tokens roughly proportionally with parameters (Hoffmann et al.).

7. **What’s the difference between “all-reduce gradients” (DDP) and “all-gather parameters + reduce-scatter gradients” (FSDP)?**  
   - Good answer: DDP keeps full params everywhere and averages grads; FSDP shards params and reconstructs them only when needed (PyTorch DDP vs FSDP/FSDP2).

8. **FlashAttention claims big speedups without approximating attention—what is the core systems reason?**  
   - Good answer: avoids materializing \(N\times N\) attention matrices in HBM via IO-aware tiling and fused kernels; reduces HBM reads/writes (Dao et al., 2022).

---

## Likely Student Questions

**Q: What exactly does DDP synchronize, and what does it *not* do for me?**  
→ **A:** DDP synchronizes by **all-reducing gradients** across replicas in a process group; it **does not shard inputs**, so you must shard the dataset yourself (e.g., `DistributedSampler`) (PyTorch DDP docs).

**Q: Are parameters broadcast every iteration in DDP?**  
→ **A:** No—DDP states “parameters are never broadcast each iteration”; it assumes identical optimizer updates after gradient all-reduce. Buffers (e.g., BatchNorm stats) *are* broadcast from rank 0 each iteration if `broadcast_buffers=True` (default) (PyTorch DDP docs).

**Q: What’s the correct AMP training loop order in PyTorch?**  
→ **A:** Forward+loss under `autocast`, then `scaler.scale(loss).backward()`, then `scaler.step(optimizer)`, then `scaler.update()`; unscale before clipping via `scaler.unscale_(optimizer)` (PyTorch AMP examples).

**Q: Why does fp16 need loss scaling, and what are the numeric limits involved?**  
→ **A:** fp16 has limited range (max normalized **65,504**, min normalized \(\approx 6.10\times 10^{-5}\)); gradients can underflow to 0. Loss scaling multiplies loss by \(S\) to amplify gradients, then divides by \(S\) before the optimizer update; dynamic scaling reduces \(S\) on Inf/NaN and increases after many stable steps (Micikevicius et al., 2017).

**Q: Why is bf16 often preferred for large-scale training?**  
→ **A:** BF16 keeps FP32-like exponent range (BF16 max normal **3.38e38**, min normal **1.17e−38**) while using fewer mantissa bits, which reduces fp16-style underflow/overflow issues and can avoid loss scaling; it shows empirical parity with FP32 on tasks like ResNet-50 and AlexNet (Kalamkar et al., 2019).

**Q: How does Megatron’s tensor parallelism split a Transformer MLP?**  
→ **A:** Split first MLP weight \(A(H\times 4H)\) **column-wise** so each GPU computes \(XA_i\) and GeLU locally; split second weight \(B(4H\times H)\) **row-wise** so each GPU consumes its activation shard; then **all-reduce** partial outputs to form the full \(H\)-dim output (Shoeybi et al., Megatron-LM).

**Q: What does Chinchilla say about “how many tokens to train”?**  
→ **A:** Under compute budget \(C\) with FLOPs \(\approx 6ND\), Chinchilla fits a loss model and derives compute-optimal \(N_{\text{opt}}(C)\) and \(D_{\text{opt}}(C)\) with exponents \(a\approx 0.46\text{–}0.50\), \(b\approx 0.50\text{–}0.54\), implying tokens should scale roughly proportionally with parameters at compute-optimality (Hoffmann et al., 2022).

**Q: What concrete throughput numbers exist for large-scale pretraining stacks?**  
→ **A:** PyTorch reports Llama2-7B-style pretraining at **3,700 tokens/sec/GPU** on **128× A100 80GB** (~**40B tokens/day**) with **MFU=57%** and near-linear scaling to **512 GPUs** (PyTorch blog, *Maximizing Training Throughput*). For float8 on H100 with FSDP2, 70B improves from **956→1430 tokens/sec/GPU (+50%)** at seq=8K (PyTorch blog, *Float8 + FSDP2*).

---

## Available Resources

### Videos
- [Let’s build micrograd](https://www.youtube.com/watch?v=VMj-3S1tku0) — Surface when: the student is shaky on backprop/SGD and you need a concrete grounding for “what gradients are” before discussing distributed gradient synchronization.
- [Let’s build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY) — Surface when: the student asks what a language model is doing during pretraining (next-token prediction) and how tokens are generated left-to-right.

### Articles & Tutorials
- [An overview of gradient descent optimization algorithms](https://www.ruder.io/optimizing-gradient-descent/) — Surface when: the student asks why AdamW is common in pretraining or how momentum/Adam differ (optimizer intuition).
- [PyTorch AMP documentation](https://docs.pytorch.org/docs/stable/amp.html) — Surface when: the student asks about `autocast` defaults (CUDA fp16 vs CPU bf16) or “why not backward under autocast.”
- [PyTorch AMP examples](https://docs.pytorch.org/docs/stable/notes/amp_examples.html) — Surface when: the student asks for the exact correct step order, clipping, or gradient accumulation with AMP.
- [PyTorch DistributedDataParallel docs](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html) — Surface when: the student asks about DDP defaults (`bucket_cap_mb`, `broadcast_buffers`, `static_graph`) or why their data isn’t sharded.
- [PyTorch FSDP docs](https://docs.pytorch.org/docs/stable/fsdp.html) — Surface when: the student asks what `FULL_SHARD` means or how all-gather/reduce-scatter relate to memory.
- [PyTorch FSDP2 tutorial](https://docs.pytorch.org/tutorials/intermediate/FSDP_tutorial.html) — Surface when: the student asks how `fully_shard()` works (DTensor params, prefetching, mixed precision policy).

---

## Visual Aids

![EDA improves text classification accuracy, especially with limited training data. (Wei & Zou 2019)](/api/wiki-images/optimization-algorithms/images/lilianweng-posts-2022-04-15-data-gen_001.png)  
Show when: the student conflates “data curation” with “data augmentation”; use this to pivot into “augmentation is one tool, but pretraining corpora like The Pile are curated via mixture weighting + filtering.”

---

## Key Sources

- [Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism](https://arxiv.org/abs/1909.08053) — definitive step-by-step tensor-parallel partitioning + required collectives and composition with data parallelism.
- [PyTorch DistributedDataParallel documentation](https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html) — authoritative semantics/defaults for gradient all-reduce data parallelism.
- [PyTorch AMP documentation](https://docs.pytorch.org/docs/stable/amp.html) — authoritative autocast/GradScaler semantics and defaults (fp16 vs bf16 behavior).
- [Training Compute-Optimal Large Language Models (Chinchilla)](https://arxiv.org/pdf/2203.15556.pdf) — compute-optimal tokens-vs-parameters equations and fitted exponents.
- [BFLOAT16: The secret to high performance on Cloud TPUs](https://arxiv.org/abs/1905.12322) — numeric-format rationale and empirical BF16≈FP32 convergence evidence.