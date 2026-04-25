# Source: https://docs.pytorch.org/tutorials/intermediate/scaled_dot_product_attention_tutorial.html
# Title: (Beta) Implementing High-Performance Transformers with Scaled Dot-Product Attention
# Fetched via: trafilatura
# Date: 2026-04-11

Note
[Go to the end](#sphx-glr-download-intermediate-scaled-dot-product-attention-tutorial-py)
to download the full example code.
(Beta) Implementing High-Performance Transformers with Scaled Dot Product Attention (SDPA)[#](#beta-implementing-high-performance-transformers-with-scaled-dot-product-attention-sdpa)
Created On: Mar 15, 2023 | Last Updated: Oct 09, 2024 | Last Verified: Nov 05, 2024
Author: [Driss Guessous](https://github.com/drisspg)
Summary[#](#summary)
In this tutorial, we want to highlight a new torch.nn.functional
function
that can be helpful for implementing transformer architectures. The
function is named torch.nn.functional.scaled_dot_product_attention
.
For detailed description of the function, see the [PyTorch documentation](https://pytorch.org/docs/master/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention).
This function has already been incorporated into torch.nn.MultiheadAttention
and torch.nn.TransformerEncoderLayer
.
Overview[#](#overview)
At a high level, this PyTorch function calculates the
scaled dot product attention (SDPA) between query, key, and value according to
the definition found in the paper [Attention is all you
need](https://arxiv.org/abs/1706.03762). While this function can
be written in PyTorch using existing functions, a fused implementation can provide
large performance benefits over a naive implementation.
Fused implementations[#](#fused-implementations)
For CUDA tensor inputs, the function will dispatch into one of the following implementations:
[FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness](https://arxiv.org/abs/2205.14135)A PyTorch implementation defined in C++
Note
This tutorial requires PyTorch 2.0.0 or later.
import torch
import torch.nn as nn
import torch.nn.functional as F
device = "cuda" if [torch.cuda.is_available](https://docs.pytorch.org/docs/stable/generated/torch.cuda.is_available.html#torch.cuda.is_available)() else "cpu"
# Example Usage:
[query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.randn](https://docs.pytorch.org/docs/stable/generated/torch.randn.html#torch.randn)(2, 3, 8, device=device), [torch.randn](https://docs.pytorch.org/docs/stable/generated/torch.randn.html#torch.randn)(2, 3, 8, device=device), [torch.randn](https://docs.pytorch.org/docs/stable/generated/torch.randn.html#torch.randn)(2, 3, 8, device=device)
[F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention)([query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
tensor([[[-0.5290, -0.7623, -0.3667, -0.3698, 0.7481, 0.2924, 0.4968,
-0.1363],
[-0.5800, -0.7280, -0.2736, -0.3201, 0.8407, 0.3129, 0.7073,
-0.0773],
[-0.2222, -0.8456, -0.2038, -0.4420, 1.2466, 0.4532, 0.6103,
-0.6795]],
[[ 1.1713, -0.3183, 0.3010, -1.1103, -0.5999, -0.5721, 1.2821,
0.6156],
[ 1.1823, -0.2888, 0.2695, -1.0194, -0.5837, -0.4041, 1.2330,
0.5467],
[-0.3483, -0.3862, -0.6809, -0.5542, 0.4166, -0.1695, 1.1353,
0.7799]]], device='cuda:0')
Explicit Dispatcher Control[#](#explicit-dispatcher-control)
While the function will implicitly dispatch to one of the three implementations, the user can also explicitly control the dispatch via the use of a context manager. This context manager allows users to explicitly disable certain implementations. If a user wants to ensure the function is indeed using the fastest implementation for their specific inputs, the context manager can be used to sweep through measuring performance.
# Lets define a helpful benchmarking function:
import torch.utils.benchmark as benchmark
def benchmark_torch_function_in_microseconds(f, *args, **kwargs):
t0 = [benchmark.Timer](https://docs.pytorch.org/docs/stable/benchmark_utils.html#torch.utils.benchmark.Timer)(
stmt="f(*args, **kwargs)", globals={"args": args, "kwargs": kwargs, "f": f}
)
return t0.blocked_autorange().mean * 1e6
# Lets define the hyper-parameters of our input
batch_size = 32
max_sequence_len = 1024
num_heads = 32
embed_dimension = 32
[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype) = [torch.float16](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)
[query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.rand](https://docs.pytorch.org/docs/stable/generated/torch.rand.html#torch.rand)(batch_size, num_heads, max_sequence_len, embed_dimension, device=device, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype))
[key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.rand](https://docs.pytorch.org/docs/stable/generated/torch.rand.html#torch.rand)(batch_size, num_heads, max_sequence_len, embed_dimension, device=device, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype))
[value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.rand](https://docs.pytorch.org/docs/stable/generated/torch.rand.html#torch.rand)(batch_size, num_heads, max_sequence_len, embed_dimension, device=device, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype))
print(f"The default implementation runs in {benchmark_torch_function_in_microseconds([F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention), [query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor)):.3f} microseconds")
# Lets explore the speed of each of the 3 implementations
from torch.nn.attention import SDPBackend, [sdpa_kernel](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html#torch.nn.attention.sdpa_kernel)
with [sdpa_kernel](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html#torch.nn.attention.sdpa_kernel)([SDPBackend.MATH](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.SDPBackend.html#torch.nn.attention.SDPBackend)):
print(f"The math implementation runs in {math_time:.3f} microseconds")
with [sdpa_kernel](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html#torch.nn.attention.sdpa_kernel)([SDPBackend.FLASH_ATTENTION](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.SDPBackend.html#torch.nn.attention.SDPBackend)):
try:
flash_time=benchmark_torch_function_in_microseconds([F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention), [query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
print(f"The flash attention implementation runs in {flash_time:.3f} microseconds")
except RuntimeError:
print("FlashAttention is not supported. See warnings for reasons.")
with [sdpa_kernel](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html#torch.nn.attention.sdpa_kernel)([SDPBackend.EFFICIENT_ATTENTION](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.SDPBackend.html#torch.nn.attention.SDPBackend)):
try:
efficient_time=benchmark_torch_function_in_microseconds([F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention), [query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
print(f"The memory efficient implementation runs in {efficient_time:.3f} microseconds")
except RuntimeError:
print("EfficientAttention is not supported. See warnings for reasons.")
The default implementation runs in 2274.809 microseconds
The math implementation runs in 87433.647 microseconds
The flash attention implementation runs in 2277.896 microseconds
The memory efficient implementation runs in 4379.249 microseconds
Hardware dependence[#](#hardware-dependence)
Depending on what machine you ran the above cell on and what hardware is available, your results might be different. - If you don’t have a GPU and are running on CPU then with FP32 the context manager will have no effect and all three runs should return similar timings. - Depending on what compute capability your graphics card supports flash attention or memory efficient might have failed.
Causal Self Attention[#](#causal-self-attention)
Below is an example implementation of a multi-headed causal self
attention block inspired by
[Andrej Karpathy NanoGPT](https://github.com/karpathy/nanoGPT) repository.
class CausalSelfAttention([nn.Module](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module)):
def __init__(self, num_heads: int, embed_dimension: int, bias: bool=False, is_causal: bool=False, dropout:float=0.0):
super().__init__()
assert embed_dimension % num_heads == 0
# key, query, value projections for all heads, but in a batch
self.c_attn = [nn.Linear](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html#torch.nn.Linear)(embed_dimension, 3 * embed_dimension, bias=bias)
# output projection
self.c_proj = [nn.Linear](https://docs.pytorch.org/docs/stable/generated/torch.nn.Linear.html#torch.nn.Linear)(embed_dimension, embed_dimension, bias=bias)
# regularization
self.dropout = dropout
self.resid_dropout = [nn.Dropout](https://docs.pytorch.org/docs/stable/generated/torch.nn.Dropout.html#torch.nn.Dropout)(dropout)
self.num_heads = num_heads
self.embed_dimension = embed_dimension
# Perform causal masking
self.is_causal = is_causal
def forward(self, [x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor)):
# calculate query, key, values for all heads in batch and move head forward to be the batch dim
query_projected = self.c_attn([x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
batch_size = query_projected.size(0)
embed_dim = query_projected.size(2)
head_dim = embed_dim // (self.num_heads * 3)
[query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = query_projected.chunk(3, -1)
[query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor).view(batch_size, -1, self.num_heads, head_dim).transpose(1, 2)
[key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor).view(batch_size, -1, self.num_heads, head_dim).transpose(1, 2)
[value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor).view(batch_size, -1, self.num_heads, head_dim).transpose(1, 2)
if self.training:
dropout = self.dropout
is_causal = self.is_causal
else:
dropout = 0.0
is_causal = False
y = [F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention)([query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), attn_mask=None, dropout_p=dropout, is_causal=is_causal)
y = y.transpose(1, 2).view(batch_size, -1, self.num_heads * head_dim)
y = self.resid_dropout(self.c_proj(y))
return y
num_heads = 8
heads_per_dim = 64
embed_dimension = num_heads * heads_per_dim
[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype) = [torch.float16](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)
model = [CausalSelfAttention](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module)(num_heads=num_heads, embed_dimension=embed_dimension, bias=False, is_causal=True, dropout=0.1).to("cuda").to([dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)).eval()
print(model)
CausalSelfAttention(
(c_attn): Linear(in_features=512, out_features=1536, bias=False)
(c_proj): Linear(in_features=512, out_features=512, bias=False)
(resid_dropout): Dropout(p=0.1, inplace=False)
)
NestedTensor
and Dense tensor support[#](#nestedtensor-and-dense-tensor-support)
SDPA supports both NestedTensor
and Dense tensor inputs. NestedTensors
handle the case where the input is a batch of variable length sequences
without needing to pad each sequence to the maximum length in the batch. For more information about NestedTensors
see
[torch.nested](https://pytorch.org/docs/stable/nested.html) and [NestedTensors Tutorial](https://pytorch.org/tutorials/prototype/nestedtensor.html).
import random
def generate_rand_batch(
batch_size,
max_sequence_len,
embed_dimension,
pad_percentage=None,
[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[torch.float16](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype),
device="cuda",
):
if not pad_percentage:
return (
[torch.randn](https://docs.pytorch.org/docs/stable/generated/torch.randn.html#torch.randn)(
batch_size,
max_sequence_len,
embed_dimension,
[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype),
device=device,
),
None,
)
# Random sequence lengths
seq_len_list = [
int(max_sequence_len * (1 - random.gauss(pad_percentage, 0.01)))
for _ in range(batch_size)
]
# Make random entry in the batch have max sequence length
seq_len_list[random.randint(0, batch_size - 1)] = max_sequence_len
return (
[torch.nested.nested_tensor](https://docs.pytorch.org/docs/stable/nested.html#torch.nested.nested_tensor)(
[
[torch.randn](https://docs.pytorch.org/docs/stable/generated/torch.randn.html#torch.randn)(seq_len, embed_dimension,
[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype), device=device)
for seq_len in seq_len_list
]
),
seq_len_list,
)
[random_nt](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), _ = generate_rand_batch(32, 512, embed_dimension, pad_percentage=0.5, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype), device=device)
[random_dense](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), _ = generate_rand_batch(32, 512, embed_dimension, pad_percentage=None, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype), device=device)
# Currently the fused implementations don't support ``NestedTensor`` for training
[model.eval](https://docs.pytorch.org/docs/stable/generated/torch.nn.Module.html#torch.nn.Module.eval)()
with [sdpa_kernel](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.sdpa_kernel.html#torch.nn.attention.sdpa_kernel)([SDPBackend.FLASH_ATTENTION](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.SDPBackend.html#torch.nn.attention.SDPBackend)):
try:
print(f"Random NT runs in {benchmark_torch_function_in_microseconds(model, [random_nt](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor)):.3f} microseconds")
print(f"Random Dense runs in {benchmark_torch_function_in_microseconds(model, [random_dense](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor)):.3f} microseconds")
except RuntimeError:
print("FlashAttention is not supported. See warnings for reasons.")
/usr/local/lib/python3.10/dist-packages/torch/nested/__init__.py:256: UserWarning: The PyTorch API of nested tensors is in prototype stage and will change in the near future. We recommend specifying layout=torch.jagged when constructing a nested tensor, as this layout receives active development, has better operator coverage, and works with torch.compile. (Triggered internally at /pytorch/aten/src/ATen/NestedTensorImpl.cpp:178.)
return _nested.nested_tensor(
Random NT runs in 639.435 microseconds
Random Dense runs in 954.428 microseconds
Using SDPA with torch.compile
[#](#using-sdpa-with-torch-compile)
With the release of PyTorch 2.0, a new feature called
torch.compile()
has been introduced, which can provide
significant performance improvements over eager mode.
Scaled dot product attention is fully composable with torch.compile()
.
To demonstrate this, let’s compile the CausalSelfAttention
module using
torch.compile()
and observe the resulting performance improvements.
batch_size = 32
max_sequence_len = 256
[x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.rand](https://docs.pytorch.org/docs/stable/generated/torch.rand.html#torch.rand)(batch_size, max_sequence_len,
embed_dimension, device=device, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype))
print(
f"The non compiled module runs in {benchmark_torch_function_in_microseconds(model, [x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor)):.3f} microseconds")
compiled_model = [torch.compile](https://docs.pytorch.org/docs/stable/generated/torch.compile.html#torch.compile)(model)
# Let's compile it
compiled_model([x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
print(
f"The compiled module runs in {benchmark_torch_function_in_microseconds(compiled_model, [x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor)):.3f} microseconds")
The non compiled module runs in 424.988 microseconds
The compiled module runs in 533.148 microseconds
The exact execution time is dependent on machine, however the results for mine: The non compiled module runs in 166.616 microseconds The compiled module runs in 166.726 microseconds That is not what we were expecting. Let’s dig a little deeper. PyTorch comes with an amazing built-in profiler that you can use to inspect the performance characteristics of your code.
from torch.profiler import [profile](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler.profile), [record_function](https://docs.pytorch.org/docs/stable/generated/torch.autograd.profiler.record_function.html#torch.autograd.profiler.record_function), ProfilerActivity
activities = [[ProfilerActivity.CPU](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler.ProfilerActivity)]
if device == 'cuda':
activities.append([ProfilerActivity.CUDA](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler.ProfilerActivity))
with [profile](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler.profile)(activities=activities, record_shapes=False) as [prof](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler.profile):
with [record_function](https://docs.pytorch.org/docs/stable/generated/torch.autograd.profiler.record_function.html#torch.autograd.profiler.record_function)(" Non-Compilied Causal Attention"):
for _ in range(25):
model([x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
print([prof.key_averages](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler._KinetoProfile.key_averages)().table(sort_by="cuda_time_total", row_limit=10))
with [profile](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler.profile)(activities=activities, record_shapes=False) as [prof](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler.profile):
with [record_function](https://docs.pytorch.org/docs/stable/generated/torch.autograd.profiler.record_function.html#torch.autograd.profiler.record_function)("Compiled Causal Attention"):
for _ in range(25):
compiled_model([x](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
print([prof.key_averages](https://docs.pytorch.org/docs/stable/profiler.html#torch.profiler._KinetoProfile.key_averages)().table(sort_by="cuda_time_total", row_limit=10))
# For even more insights, you can export the trace and use ``chrome://tracing`` to view the results
#
# .. code-block:: python
#
# prof.export_chrome_trace("compiled_causal_attention_trace.json").
/usr/local/lib/python3.10/dist-packages/torch/profiler/profiler.py:224: UserWarning: Warning: Profiler clears events at the end of each cycle.Only events from the current cycle will be reported.To keep events across cycles, set acc_events=True.
_warn_once(
------------------------------------------------------- ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------
Name Self CPU % Self CPU CPU total % CPU total CPU time avg Self CUDA Self CUDA % CUDA total CUDA time avg # of Calls
------------------------------------------------------- ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------
Non-Compilied Causal Attention 16.46% 2.089ms 75.61% 9.593ms 9.593ms 0.000us 0.00% 10.836ms 10.836ms 1
Non-Compilied Causal Attention 0.00% 0.000us 0.00% 0.000us 0.000us 10.707ms 100.87% 10.707ms 10.707ms 1
aten::linear 1.01% 128.493us 35.31% 4.481ms 89.611us 0.000us 0.00% 8.011ms 160.221us 50
aten::matmul 2.03% 257.981us 31.83% 4.039ms 80.780us 0.000us 0.00% 8.011ms 160.221us 50
aten::mm 10.24% 1.299ms 27.90% 3.540ms 70.792us 7.789ms 73.38% 8.011ms 160.221us 50
ampere_fp16_s1688gemm_fp16_128x128_ldg8_f2f_tn 0.00% 0.000us 0.00% 0.000us 0.000us 5.577ms 52.54% 5.577ms 223.070us 25
aten::scaled_dot_product_attention 1.74% 220.235us 15.82% 2.007ms 80.276us 0.000us 0.00% 2.825ms 113.018us 25
aten::_scaled_dot_product_flash_attention 2.42% 306.557us 14.08% 1.787ms 71.467us 0.000us 0.00% 2.825ms 113.018us 25
aten::_flash_attention_forward 2.72% 344.767us 10.42% 1.322ms 52.899us 2.825ms 26.62% 2.825ms 113.018us 25
void pytorch_flash::flash_fwd_kernel<Flash_fwd_kerne... 0.00% 0.000us 0.00% 0.000us 0.000us 2.825ms 26.62% 2.825ms 113.018us 25
------------------------------------------------------- ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------
Self CPU time total: 12.688ms
Self CUDA time total: 10.614ms
------------------------------------------------------- ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------
Name Self CPU % Self CPU CPU total % CPU total CPU time avg Self CUDA Self CUDA % CUDA total CUDA time avg # of Calls
------------------------------------------------------- ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------
Compiled Causal Attention 0.00% 0.000us 0.00% 0.000us 0.000us 10.699ms 100.87% 10.699ms 10.699ms 1
Compiled Causal Attention 8.21% 1.053ms 80.30% 10.294ms 10.294ms 0.000us 0.00% 10.606ms 10.606ms 1
Torch-Compiled Region: 0/0 6.97% 893.073us 69.98% 8.971ms 358.826us 0.000us 0.00% 10.606ms 424.257us 25
CompiledFunction 7.85% 1.007ms 60.58% 7.766ms 310.626us 0.000us 0.00% 10.606ms 424.257us 25
## Call CompiledFxGraph fuwwtrzim7p3btsjlmoz3w4rdffp... 14.30% 1.834ms 52.73% 6.759ms 270.359us 0.000us 0.00% 10.606ms 424.257us 25
aten::mm 7.67% 983.718us 11.71% 1.501ms 30.024us 7.785ms 73.40% 7.785ms 155.701us 50
ampere_fp16_s1688gemm_fp16_128x128_ldg8_f2f_tn 0.00% 0.000us 0.00% 0.000us 0.000us 5.570ms 52.52% 5.570ms 222.809us 25
aten::_scaled_dot_product_flash_attention 1.93% 247.187us 13.00% 1.666ms 66.654us 0.000us 0.00% 2.821ms 112.855us 25
aten::_flash_attention_forward 2.67% 342.155us 9.55% 1.224ms 48.979us 2.821ms 26.60% 2.821ms 112.855us 25
void pytorch_flash::flash_fwd_kernel<Flash_fwd_kerne... 0.00% 0.000us 0.00% 0.000us 0.000us 2.821ms 26.60% 2.821ms 112.855us 25
------------------------------------------------------- ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------ ------------
Self CPU time total: 12.819ms
Self CUDA time total: 10.606ms
The previous code snippet generates a report of the top 10 PyTorch functions
that consumed the most GPU execution time, for both the compiled and non-compiled module.
The analysis reveals that the majority of time spent on the GPU is concentrated
on the same set of functions for both modules.
The reason for this here is that torch.compile
is very good at removing the
framework overhead associated with PyTorch. If your model is launching
large, efficient CUDA kernels, which in this case CausalSelfAttention
is, then the overhead of PyTorch can be hidden.
In reality, your module does not normally consist of a singular
CausalSelfAttention
block. When experimenting with [Andrej Karpathy NanoGPT](https://github.com/karpathy/nanoGPT) repository, compiling
the module took the time per train step from: 6090.49ms
to
3273.17ms
! This was done on commit: ae3a8d5
of NanoGPT training on
the Shakespeare dataset.
Using SDPA with attn_bias subclasses[#](#using-sdpa-with-attn-bias-subclasses)
# As of PyTorch 2.3, we have added a new submodule that contains tensor subclasses.
# Designed to be used with ``torch.nn.functional.scaled_dot_product_attention``.
# The module is named ``torch.nn.attention.bias`` and contains the following two
# utilities for generating causal attention variants:
#
# - ``torch.nn.attention.bias.causal_upper_left``
# - ``torch.nn.attention.bias.causal_lower_right``
#
# .. note::
# The current argument ``is_causal`` in ``torch.nn.functional.scaled_dot_product_attention``
# is the same as using ``torch.nn.attention.bias.causal_upper_left``.
#
from torch.nn.attention.bias import [causal_lower_right](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.causal_lower_right.html#torch.nn.attention.bias.causal_lower_right), [causal_upper_left](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.causal_upper_left.html#torch.nn.attention.bias.causal_upper_left)
batch_size = 32
sequence_length_q = 2
sequence_length_kv = 10
num_heads = 16
embed_dimension = 32
[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype) = [torch.float16](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)
[query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.rand](https://docs.pytorch.org/docs/stable/generated/torch.rand.html#torch.rand)(batch_size, num_heads, sequence_length_q, embed_dimension, device=device, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype))
[key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.rand](https://docs.pytorch.org/docs/stable/generated/torch.rand.html#torch.rand)(batch_size, num_heads, sequence_length_kv, embed_dimension, device=device, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype))
[value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [torch.rand](https://docs.pytorch.org/docs/stable/generated/torch.rand.html#torch.rand)(batch_size, num_heads, sequence_length_kv, embed_dimension, device=device, [dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype)=[dtype](https://docs.pytorch.org/docs/stable/tensor_attributes.html#torch.dtype))
[upper_left_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias) = [causal_upper_left](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.causal_upper_left.html#torch.nn.attention.bias.causal_upper_left)(sequence_length_q, sequence_length_kv)
[lower_right_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias) = [causal_lower_right](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.causal_lower_right.html#torch.nn.attention.bias.causal_lower_right)(sequence_length_q, sequence_length_kv)
print(type([upper_left_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias)))
print(type([lower_right_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias)))
assert type([upper_left_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias)) == type([lower_right_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias))
assert issubclass(type([upper_left_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias)), [torch.Tensor](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
# As you can see from the previous output, are the same type ``torch.nn.attention.bias.CausalBias``
# and subclass ``torch.Tensor``
# Lets see what these tensors look like
print([upper_left_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias))
print([lower_right_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias))
# Upper Left Bias aligns the causal attention mask to the upper left corner of the attention scores matrix.
# This only has an impact when the attention scores matrix is not square, which is common for decoding use cases.
# Another way of thinking about this concept is that when you use upper left bias,
# the 0th token in the query is aligned to the 0th token in the key, while for lower right bias,
# Assuming the attention score matrix is two dimensional, ``attn_score[0][0]`` is the attention score
# between the 0th token in the query and the 0th token in the key.
# For lower right bias, the sequence of q is aligned so that the last token in q is aligned to the last token in k
# (for example, ``attn_score[-1][-1])`` is all True since the last token in q is at the same position as the last token in k
# even if the sequence length of q and k are different.
# These objects are intended to be used with sdpa
[out_upper_left](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention)([query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [upper_left_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias))
[out_lower_right](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention)([query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [lower_right_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias))
[out_is_causal](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = [F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention)([query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), is_causal=True)
assert [torch.allclose](https://docs.pytorch.org/docs/stable/generated/torch.allclose.html#torch.allclose)([out_upper_left](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [out_is_causal](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
assert not [torch.allclose](https://docs.pytorch.org/docs/stable/generated/torch.allclose.html#torch.allclose)([out_upper_left](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [out_lower_right](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor))
# These attention biases should also be compatible with torch.compile
compiled_sdpa = [torch.compile](https://docs.pytorch.org/docs/stable/generated/torch.compile.html#torch.compile)([F.scaled_dot_product_attention](https://docs.pytorch.org/docs/stable/generated/torch.nn.functional.scaled_dot_product_attention.html#torch.nn.functional.scaled_dot_product_attention), fullgraph=True)
[out_upper_left](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor) = compiled_sdpa([query](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [key](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [value](https://docs.pytorch.org/docs/stable/tensors.html#torch.Tensor), [upper_left_bias](https://docs.pytorch.org/docs/stable/generated/torch.nn.attention.bias.CausalBias.html#torch.nn.attention.bias.CausalBias))
<class 'torch.nn.attention.bias.CausalBias'>
<class 'torch.nn.attention.bias.CausalBias'>
tensor([[ True, False, False, False, False, False, False, False, False, False],
[ True, True, False, False, False, False, False, False, False, False]])
tensor([[ True, True, True, True, True, True, True, True, True, False],
[ True, True, True, True, True, True, True, True, True, True]])
Conclusion[#](#conclusion)
In this tutorial, we have demonstrated the basic usage of
torch.nn.functional.scaled_dot_product_attention
. We have shown how
the sdpa_kernel
context manager can be used to assert a certain
implementation is used on GPU. As well, we built a simple
CausalSelfAttention
module that works with NestedTensor
and is torch
compilable. In the process we have shown how to the profiling tools can
be used to explore the performance characteristics of a user defined
module.
Total running time of the script: (0 minutes 6.073 seconds)