# Source: https://jarbus.net/blog/numerical-stability-in-flash-attention/
# Author: jarbus
# Author Slug: jarbus
# Title: Numerical Stability in Flash Attention - - jarbus
# Fetched via: search
# Date: 2026-04-11

Flash attention, a recent implementation of attention which makes less calls to high-bandwidth memory, uses a version of the softmax function which is numerically stable.
In this post, I’ll briefly showcase how this is done and an example of an unstable softmax.
The softmax function is used in machine learning to convert a vector of
real numbers to a vector of probabilities which sum to 1, and is defined as:
```
softmax(x) = [exp(x[i]) / sum([exp(xj) for xj in x]) for xi in x]
```
where x is a vector of real numbers.
The python implementation below is numerically unstable because it involves
exponentiation of large numbers, which can lead to overflow.
Crucially,
underflow is not an issue, because exp(x) approaches zero when x is a large
negative number.
```
import numpy as np
def unstable_softmax(x):
fx_unstable = np.exp(x)
return fx_unstable / np.sum(fx_unstable)
```
The following implementation is stable however, because there is no
exponentiation of large numbers:
```
def stable_softmax(x):
fx_stable = x - np.max(x)
return np.exp(fx_stable) / np.sum(np.exp(fx_stable))
```
Instead, the max of the vector is subtracted from each element.
This does not
change the result of the softmax after the division as this subtraction is also
performed in the denominator, thus cancelling out.
Let’s compare the two implementations:
```
>>> a = np.array([6.0, -3, 15], dtype=np.float32)
>>> stable_softmax(a)
[1.2339458e-04 1.5228101e-08 9.9987662e-01]
>>> unstable_softmax(a)
[1.2339458e-04 1.5228101e-08 9.9987656e-01]
```
As you can see, the results are mostly equal, save for a few digits.
Now let’s look at what happens with 16 bits of precision:
```
>>> a = np.array([6.0, -3, 15], dtype=np.float16)
>>> unstable_softmax(a)
[ 0. 0. nan]
>>> stable_softmax(a)
[ 1.234e-04 0.000e+00 1.000e+00]
```
When working with 16 bits of precision, we observe that exp(15) produces a numerical overflow
which turns the third element into a NaN.
This is because exp(15) produces a value that can
not be represented by a float16.
To recap, we showed that softmax is numerically unstable, especially when working with small precision bits.
Because softmax uses exponentials in the numerator and denominator, we can subtract all exponents by the maximum exponent, constraining all the values between 0 and 1 and preventing numerical overflow.

## Description
...
However, as was also noted in #10 , there seems to be a slight, but potentially significant numerical mismatch with the reference Pytorch attention implementation.
A quick check of the computed values with a 768-dimension, 4,096 sequence length setup yields:
```
plain_fwd = attention_ref(qkv, attention_mask_bool, dropout_p, causal=causal)
flash_fwd = flash_attn_func(qkv[0], cu_seqlens, dropout_p, max_seqlen_in_batch, causal=causal)
delta = plain_fwd - flash_fwd
total_value = lambda val: val.abs().sum().item()
print(f'Total Activations: plain={total_value(plain_fwd):.2f}, flash={total_value(flash_fwd):.2f}, delta: {total_value(delta):.2f}')
# Total Activations: plain=65408.00, flash=65408.00, delta: 7.32
```
That is, while both functions achieve the same total value, small differences sum up to a meaningful delta.
An inspection of the difference shows that about 86% of the values in `delta` are "true" zeros, with the remainder being off by about 1.7e-5 on average.
Locations where the delta was non-zero were not particularly different in absolute activation.
Note that I removed all padding and replaced `qkv_unpad` with `qkv[0]` to make these more comparable -- using `qkv_unpad` even without any padding tokens present cause the `delta` to grow to 93.31 and the total activations to diverge.
I also disabled dropout to ensure this is not due to randomness in the function itself.
...
I think that amount of numerical error might be expected since we're using fp16 .
This topic of numerical error is super interesting.
...
More details: we probably want to compare the numerical error of the Pytorch implementation in fp16 - Pytorch implementation in fp32, and Flash (in fp16) - Pytorch implementation in fp32.
They have similar max absolute error, and FlashAttention has slightly higher relative error.
This could be because of the difference in the order of operations.
Btw you can cast the delta to float so that summation doesn't exceed 64K (which is the limit of fp16).
```
ref_fp32_fwd = attention_ref(qkv, attention_mask_bool, dropout_p, causal=causal, upcast=True)
ref_fwd = attention_ref(qkv, attention_mask_bool, dropout_p, causal=causal)
flash_fwd = flash_attn_func(qkv_unpad, cu_seqlens, dropout_p, max_seqlen_in_batch, causal=causal)
flash_fwd = rearrange(flash_fwd, '(b s) h d -> b s h d', b = batch_size)
delta_ref = ref_fwd - ref_fp32_fwd
delta_flash = flash_fwd - ref_fp32_fwd
total_value = lambda val: val.float().abs().sum().item()
print(f'Reference fp16 max absolute error = {delta_ref.abs().max().item()}')
print(f'Reference fp16 mean relative error = {total_value(delta_ref) / total_value(ref_fp32_fwd)}')
print(f'Flash max absolute error = {delta_flash.abs().max().item()}')
print(f'Flash mean relative error = {total_value(delta_flash) / total_value(ref_fp32_fwd)}')
# Reference fp16 max absolute error = 6.103515625e-05
# Reference fp16 mean relative error = 7.466496773477096e-05
# Flash max absolute error = 6.103515625e-05
# Flash mean relative error = 0.00011073935366785967
```
As another example of order of operations causing numerical differences, if you simply multiply the result by 3.0 then divide it by 3.0, you get a numerical difference of the same magnitude.
```
delta_mul = ref_fwd - (ref_fwd * 3.0) / 3.0
print(f'Multiply fp16 max absolute error = {delta_mul.abs().max().item()}')
print(f'Multiply fp16 mean relative error = {total_value(delta_mul) / total_value(ref_fwd)}')
# Multiply fp16 max absolute error = 6.103515625e-05
# Multiply fp16 mean relative error = 8.713470482512265e-05
```
Btw we're working on implementing FlashAttention for bf16 format.
The folk wisdom seems to be that bf16 training is more stable than fp16 training in general.
> Btw we're working on implementing FlashAttention for bf16 format.
...
I guess the only other risk would be if these kinds of small deltas are more prone to occurring in large attention values, since the softmax would then amplify such differences, which can even cause overflows.
I haven't noticed a consistent skew like that so far, but it might still explain the instabilities that others noticed.
...
bf16 is now supported.
@tridao tremendous!

…
Abstract:Training large-scale machine learning models poses distinct system challenges, given both the size and complexity of today's workloads.
Recently, many organizations training state-of-the-art Generative AI models have reported cases of instability during training, often taking the form of loss spikes.
Numeric deviation has emerged as a potential cause of this training instability, although quantifying this is especially challenging given the costly nature of training runs.
In this work, we develop a principled approach to understanding the effects of numeric deviation, and construct proxies to put observations into context when downstream effects are difficult to quantify.
As a case study, we apply this framework to analyze the widely-adopted Flash Attention optimization.
We find that Flash Attention sees roughly an order of magnitude more numeric deviation as compared to Baseline Attention at BF16 when measured during an isolated forward pass.
We then use a data-driven analysis based on the Wasserstein Distance to provide upper bounds on how this numeric deviation impacts model weights during training, finding that the numerical deviation present in Flash Attention is 2-5 times less significant than low-precision training.
|Subjects:|Machine Learning (cs.LG); Distributed, Parallel, and Cluster Computing (cs.DC)|
...
|Cite as:|arXiv:2405.02803 [cs.LG]|
| |(or arXiv:2405.02803v1 [cs.LG] for this version)|
| |https://doi.org/10.48550/arXiv.2405.02803 arXiv-issued DOI via DataCite|

1. I Introduction
2. II Background 1. II-A Attention as a System-Performance Bottleneck
   2. II-B Understanding Flash Attention
3. III Experimental Methodology
4. IV Quantifying Numeric Deviation Through Microbenchmark 1. IV-A Sweep Numerical Precision
   2. IV-B Sweep Algorithm Changes
5. V Contextualizing Numeric Deviation Via Weight Differences
6. VI Discussion and Future Work
7. VII Conclusion

…

In this work, we develop a principled approach to understanding the effects of numeric deviation, and construct proxies to put observations into context when downstream effects are difficult to quantify. As a case study, we apply this framework to analyze the widely-adopted Flash Attention optimization. We find that Flash Attention sees roughly an order of magnitude more numeric deviation as compared to Baseline Attention at BF16 when measured during an isolated forward pass.
We then use a data-driven analysis based on the Wasserstein Distance to provide upper bounds on how this numeric deviation impacts model weights during training, finding that the numerical deviation present in Flash Attention is 2-5 times less significant than low-precision training.

…

One under-explored potential cause of training instability is numeric deviation. Numeric deviation between an optimization and its corresponding baseline can lead to the gradual accumulation of errors, which over the course of training have the potential to culminate in loss spikes that require a resetting of the model state [1]. This is challenging to quantify, as training’s stochastic nature suggests some level of numeric deviation might be acceptable, yet determining the threshold for when training becomes unstable proves difficult.
In this work, we develop a principled quantitative approach to understanding numeric deviation in training optimizations. Our approach consists of two phases, including (i) developing a microbenchmark to perturb numeric precision in the given optimization, and (ii) evaluating how numeric deviation translates to changes in model weights through a data-driven analysis based on Wasserstein distance.
This ultimately allows us to provide an upper bound on the amount of numeric deviation for a given optimization, and helps to contextualize the improvement within known techniques. We aim to use this principled analysis to evaluate different state-of-the-art optimization techniques and identify whether they are likely to introduce unintended instabilities when used to train large models.
As a case study, we analyze the state-of-the-art optimization technique Flash Attention [2], and quantify the potential numeric deviation introduced. Flash Attention is a widely-adopted technique used to speed up the attention mechanism, often considered a system bottleneck in transformer models [11]. However, while offering increased speedup and reduced memory accesses, Flash Attention depends on algorithm optimizations that have the potential to contribute to increased numeric deviation.
Specifically, we hypothesize that the addition of rescaling factors could introduce unintentional approximation that leads to numeric tradeoff, which could later impact training stability. We analyze Flash Attention in the context of multi-modal Text-to-Image workloads in order to determine the potential significance of numeric deviation between Flash Attention and its baseline.

…

- •

  We design a microbenchmark to isolate the impact of numerical precision on numeric deviation. Our microbenchmark serves as a technique to measure and quantify numeric deviation resulting from traditionally black-box optimizations such as Flash Attention. By perturbing aspects not typically available through the provided kernel, we initially find Flash Attention sees roughly an order of magnitude more numeric deviation as compared to Baseline Attention at low numerical precision (BF16).
- •

  We perform a data-driven analysis based on the Wasserstein Distance metric to contextualize this observed numeric deviation and form an upper bound for the impact on downstream model properties. In our case study, we are able to bound the impact of this observed numerical deviation, and find that Flash Attention introduces roughly 2-5\times less model weight deviation as compared to low-precision training.
Our investigations underscore the importance of developing a principled approach to not only quantify, but contextualize, the impact of training optimizations on numeric deviation. By constructing proxies to put this numeric deviation in context, we aim to reason about the likelihood of downstream model effects (i.e., training instability) that are traditionally difficult to measure.

## II Background

As a case study for this work, we analyze the state-of-the-art optimization Flash Attention and its potential numeric deviation from Baseline Attention. The Attention operation has been the focus of myraid optimizations as of late. Attention is currently the main system-performance bottleneck of the Transformer architecture, which is a widely adopted technique in modern machine learning algorithms known for its effectiveness in modeling sequence-to-sequence tasks [11].

### II-A Attention as a System-Performance Bottleneck

The Attention operation essentially derives a weighted sum that represents how much emphasis a model should place on all previous words when generating a new token [11]. The key computation in Attention involves matrix-multiplications and softmax. Three representations (Query, Key, Value) are first derived from the input vector, each having dimension N\times d , where N is the sequence length and d is the model dimension.
The dot product of the Query and Key values then form a N\times N matrix, which scales quadratically in size with sequence length. This so-called similarity matrix subsequently undergoes a softmax operation, before being multiplied with the Value matrix to complete the computation. The full operation is described below:

Attention(Q,K,V)=softmax(Q\dot{K}^{T}/\sqrt{d_{k}})V
Given this quadratic scaling with sequence length, myraid techniques have been proposed to accelerate the Attention mechanism, including system-aware methods such as Flash Attention [2].

### II-B Understanding Flash Attention

Flash Attention is a recently proposed technique that is designed to accelerate the Attention bottleneck characteristic of Transformers [2]. As an IO aware technique, it aims to minimize the memory overhead of the large N\times N similarity matrix typically used in the attention mechanism. It essentially uses the traditional techniques of tiling and recomputation, along with an online softmax trick, in order to only calculate the matrix one tile at a time [2].
As shown in Figure 1, the introduction of tiling eliminates the need for the large similarity matrix to be materialized. The block/tile size is defined by B_{c}=\lceil M/4d\rceil and B_{r}=min(\lceil M/4d\rceil,d), where M is the size of the SRAM and d is the model dimension. This ensures the block fits inside SRAM, and thus eliminates the need for the large matrix to be loaded/stored from HBM.
However, since the online softmax technique requires global information about the matrix, Flash Attention must incorporate re-scaling factors in order to allow for consistent calculations since global information is no longer available when computing on a single block. While introducing relatively minimal overhead, these additional re-scaling factors do introduce extra computation that is calculated per tile.
Flash Attention comes with timing performance speedup as well as more efficient resource utilization; we find that it yields a 14% speedup of forward + backward pass for our example text-to-image model. However, it has also been hypothesized that the additional computation introduced by rescaling factors of Flash Attention could introduce numeric deviation when used in text-to-image model training, and we aim to investigate this below.

## III Experimental Methodology

We first develop a microbenchmark to isolate and study the numeric deviation caused by Flash Attention.
A summary of our microbenchmark design can be found in Figure 2. As shown, we numerically re-implement Flash Attention in order to analyze different numerical precisions and apply potential optimizations at each step of the algorithm, which is not easily done with the original CUDA implementation.
This is necessary, as the Flash Attention kernel currently only supports FP16 and BF16 number formats. The Flash Attention kernel is also a wrapped API call of CUDA code, making it challenging to perturb the algorithm to examine the impact on numeric deviation. In contrast, our microbenchmark design allows for varying precision inputs and modifications inside the algorithm. We validate our microbenchmark against the original Flash Attention kernel.
We further devise a technique to compare the output of the Attention matrix at each step during model execution. We modify the model code to compute both Baseline Attention and Flash Attention each time Attention is called, which allows for identical input matrices and an exact output matrix comparison. To contextualize this, we additionally quantify the difference in model weights throughout training via identical and independent training runs, using the max\_difference and Wasserstein\ Distance metrics, which are further detailed in Section V.
For training experiments we use a type of Generative AI workload that converts text inputs to images (i.e., Text-to-Image model). We retrain the model using the Shutterstock dataset and run our experiments across a cluster of NVIDIA 80GB A100 GPUs.

## IV Quantifying Numeric Deviation Through Microbenchmark

We first analyze the impact of Flash Attention during the forward pass. We utilize our microbenchmark to examine how different numerical precisions impact the output matrix of the Attention calculation, given the same randomly initialized query, key, value vectors.

### IV-A Sweep Numerical Precision

We find that numerical precision has an impact on the output of Flash Attention, causing it to deviate from the output of Baseline Attention. We quantify this through a measure of the maximum difference between attention output matrices taken elementwise, which serves as an upper bound on the possible deviation. As Figure 3 shows, when using different number formats varying from BF16 to FP64, the numeric deviation between Flash Attention and Baseline Attention decreases with increasing number of mantissa bits. This suggests the numeric difference is a result of approximation inherent with fewer mantissa bits.
We then subsequently compare this to the behavior of Baseline Attention. For a common standard of comparison, we set a ”golden value” of Attention to be Baseline Attention at FP64. We then compare the maximum difference of the Attention output at different number formats to this golden value, as shown in Figure 4.
Note we plot the maximum difference between Flash Attention outputs and this golden value (blue bars), while comparing Baseline Attention outputs to this golden value for comparison as well (red bars). We find that Flash Attention sees roughly 10\times more numeric deviation as compared to Baseline Attention at BF16. A detailed discussion on whether this level of deviation is significant can be found in Section V.
To analyze this observed numeric deviation further, we sweep the sequence length of our matrices while keeping the tile size and SRAM size the same. As shown in Figure 5, as sequence length increases, the numerical deviation between Flash Attention and Baseline Attention increases, when measured by both (a) the maximum difference upper bound, and (b) the mean and standard deviation of that difference. Since a larger sequence length implies a larger N\times N intermediate matrix that must be tiled while the tile size stays the same, more rescaling is needed. This presents more opportunities for precision errors to accumulate, and thus more deviation.

### IV-B Sweep Algorithm Changes

We further leverage the microbenchmark design to experiment with different optimizations so we can better understand the effects of this numeric deviation. Figure 6 shows several algorithm changes and their corresponding impact on observed numeric deviation. For each experiment, we sweep block area (defined according to Bc and Br dimensions introduced in Section II), and plot the corresponding maximum difference between Attention matrix outputs. We highlight how this changes at the four precisions analyzed in Section IV-A. Figure 6a shows how swapping the order of the block dimensions leads to larger numerical difference between Flash Attention and Baseline Attention.
Notably, we additionally find that larger block/tile sizes lead to smaller numeric deviation (Figure 6c). This is because less re-scaling calculations are needed with larger tile sizes, since there are fewer tiles needed to cover the original N\times N matrix. Note that other perturbations such as constraining tile sizes to be square does not have an impact on numeric deviation, since this does not drastically change the number of re-scaling calculations needed to be performed (Figure 6b).

## V Contextualizing Numeric Deviation Via Weight Differences

While Flash Attention may cause numeric deviation of the Attention output during a forward pass, our ultimate goal is to determine whether this has any impact during model training, in order to investigate whether it contributes to training instability. We thus aim to quantify whether Flash Attention changes the model during training — i.e., if the observed Attention output difference from Section IV is reflected in model weights that are updated during training.
We utilize two metrics to measure the model weight difference between a model trained with Baseline Attention as compared to Flash Attention. We first calculate max\_difference, by finding the absolute value of the difference between weight matrices and taking the maximum to give an upper bound on the deviation, as shown below:

torch.max(torch.abs(flash\_attn-baseline\_attn))

…

Using these two metrics, we subsequently quantify how model weights change throughout the course of training when Flash Attention is implemented as compared to Baseline Attention. As shown in Figure 7, the incorporation of Flash Attention does in fact change the model weights throughout training, as measured by both Wasserstein Distance and Max Difference, and as training continues, this difference only increases. This suggests that models trained with Flash Attention converge to a different model than an identical one trained with Baseline Attention.
However, training is a stochastic process and some model architecture changes can yield comparable results in terms of downstream effects and accuracy. Thus, even if the model weights differ between a model trained with Flash Attention and Baseline Attention, is this significant? Training models to completion and evaluating accuracy is a costly and resource-intensive task, especially for large models where training takes on order of months. We therefore formulate a proxy to understand (a) how significant these weight changes are? and (b) can we put this into context with standard weight changes in other widely-adopted training optimizations?
To achieve this, we devise a series of experiments to compare how weight differences change over the course of training under different scenarios. In addition to comparing training runs with Flash and Baseline Attention, we quantify the weight difference of identical training runs where weights are initialized to different random values at the beginning of training. This provides a bound, since random weight initialization is a commonly-used technique [8], and typically produces equivalent results.
Furthermore, we also measure the change in model weights of models trained with different precisions. Numeric precision (i.e., FP16 vs FP32) has potential to cause changes downstream, and this serves as an upper bound for determining the significance of Flash Attention weights.
Figure 8 shows the relative weight differences over the course of training as measured using Wasserstein Distance. We find that the rate of change of weight deviation for a model using Flash Attention is comparable or less than the deviation from a different model initialization (note the slope of red and blue curves). Furthermore, we see that the rate of change of weights when using FP16 vs FP32 is higher and more variable than the rate of change for different model initializations.
These results provide a proxy to suggest that although numeric deviation occurs with Flash Attention, it is bounded by random model initialization and low-precision training, and introduces roughly 2-5\times less model weight deviation as compared to low-precision training.

## VI Discussion and Future Work

Our work takes the first step towards addressing the question, Is Flash Attention Stable, yet there is still more work that needs to be done before drawing a conclusive answer. Since training instability is challenging and costly to isolate, we explore numeric deviation, which is hypothesized to be a potential cause. Through our principled numeric deviation analysis, we make progress towards this goal by developing a framework to quantify numeric deviation and develop proxies to bound the impact of this deviation in terms of model weights. However, ultimately linking this numeric deviation back to training instability requires further investigation.
Our numeric quantification methodology opens up a broader set of inquiries, including understanding how various other optimizations impact numeric deviation. Although this analysis is focused on Flash Attention, future work should aim to widen the scope, and investigate additional training optimizations and their corresponding numeric deviation from the appropriate baseline. For example, investigating the numeric deviation caused by the Winograd Algorithm compared to traditional convolution, or various other Attention optimizations, kernel fusion techniques, etc.

# The FlashAttention CUDA Kernel Line by Line
Flash Attention is a memory-efficient algorithm for computing attention in transformers.
Let's break down the CUDA implementation block by block.
The core innovation of Flash Attention is processing attention in blocks while maintaining numerical stability through careful tracking of maximum values and partial sums.
The algorithm achieves memory efficiency by never materializing the full attention matrix while still producing mathematically equivalent results to the standard attention mechanism.
…
```
#include <cuda.h>
#include <cuda_runtime.h>
#define CEIL_DIV(x, y) ((x) >= 0 ? (((x) + (y) - 1) / (y)) : ((x) / (y)))
```
…
```
template <const int Br, const int Bc>
__global__ void flash_attn_kernel(float* Q, float* K, float* V, int N, int d, int Tr, int Tc, float scale, float* l, float* m, float* O)
```
This declares a CUDA kernel with template parameters `Br` and `Bc` which represent the block sizes for rows and columns.
The function takes:
- Q, K, V: Query, Key, and Value matrices
- N: Sequence length
- d: Head dimension
- Tr, Tc: Number of blocks in rows and columns
- scale: Scaling factor for attention scores
- l, m: Auxiliary arrays for the numerically stable softmax computation
- O: Output matrix
…
```
int tx = threadIdx.x;
int bx = blockIdx.x;
int by = blockIdx.y;
int qkv_off = (bx * gridDim.y * N * d) + (by * N * d);
int lm_off = (bx * gridDim.y * N) + (by * N);
```
This section retrieves the thread and block indices (tx, bx, by) that identify which thread is executing.
It then calculates two important offset values: qkv_off for accessing the Q, K, V matrices and lm_off for accessing the auxiliary arrays l and m.
These offsets ensure each block processes the correct portion of the input data.
…
```
extern __shared__ float smem[];
float* Qi = smem;
float* Kj = Qi + Br * d;
float* Vj = Kj + Bc * d;
float* Sij = Vj + Bc * d;
float* Oi = Sij + Br * Bc;
float* li = Oi + Br * d;
float* li_new = li + Br;
float* mi = li_new + Br;
float* mi_new = mi + Br;
float* mij_dash = mi_new + Br;
```
This section partitions the shared memory into different regions for:
- Qi: Current block of Query matrix
- Kj: Current block of Key matrix
- Vj: Current block of Value matrix
- Sij: Attention scores
- Oi: Output accumulator
- li, li_new, mi, mi_new, mij_dash: Softmax computation variables
**Main Processing Loops**
The kernel uses two nested loops:
1. Outer loop over Key/Value blocks (`j`)
2. Inner loop over Query blocks (`i`)
**Key-Value Loading**
```
for (int j = 0; j < Tc; j++) {
int loads_per_thread = CEIL_DIV(d, Br);
for (int e = 0; e < loads_per_thread; e++) {
int idx = e * (Br * Bc) + tx;
if (idx < Bc * d) {
int row = idx / d;
int col = idx % d;
if (j * Bc + row < N) {
Kj[row * d + col] = K[qkv_off + (j * Bc + row) * d + col];
Vj[row * d + col] = V[qkv_off + (j * Bc + row) * d + col];
}
}
}
__syncthreads();
```
This section loads the current block of K and V matrices into shared memory, with bounds checking to prevent out-of-bounds access.
Let's break down the main computation loop which processes each block of queries:
**Loading Query and Output Data**
```
for (int e = 0; e < loads_per_thread; e++) {
int idx = e * (Br * Bc) + tx;
if (idx < Br * d) {
int row = idx / d;
int col = idx % d;
if (i * Br + row < N) {
Qi[row * d + col] = Q[qkv_off + (i * Br + row) * d + col];
Oi[row * d + col] = O[qkv_off + (i * Br + row) * d + col];
}
}
}
```
This section loads the current block of Query matrix and Output accumulator into shared memory.
Each thread may load multiple elements to ensure efficient memory access patterns.
The bounds checking ensures we don't access out-of-bounds memory when N isn't perfectly divisible by the block size.
**Thread Position Calculation and Max/Sum Loading**
```
int s_row = tx / Bc;
int s_col = tx % Bc;
if (s_col == 0) {
mi[s_row] = m[lm_off + (i * Br) + s_row];
li[s_row] = l[lm_off + (i * Br) + s_row];
}
__syncthreads();
```
Each thread calculates its position in the shared memory block.
The first thread in each row (`s_col == 0`) loads the running maximum and sum values needed for the numerically stable softmax computation.
**Computing Attention Scores**
```
float acc = 0.f;
for (int k = 0; k < d; k++)
acc += Qi[s_row * d + k] * Kj[s_col * d + k];
acc *= scale;
Sij[s_row * Bc + s_col] = acc;
```
This computes the scaled dot product attention scores between the Query and Key matrices.
Each thread computes one element of the attention score matrix Sij.
**Numerically Stable Softmax Computation**
```
if (s_col == 0) {
float row_m = -INFINITY, row_l = 0.f;
// Find max for numerical stability
for (int c = 0; c < Bc; c++) {
float val = Sij[s_row * Bc + c];
if (val > row_m) {
row_m = val;
}
}
// Compute exponentials and sum
for (int c = 0; c < Bc; c++) {
float exp_val = expf(Sij[s_row * Bc + c] - row_m);
Sij[s_row * Bc + c] = exp_val;
row_l += exp_val;
}
// Update running max and sum
mij_dash[s_row] = row_m;
mi_new[s_row] = max(mi[s_row], row_m);
li_new[s_row] = expf(mi[s_row] - mi_new[s_row]) * li[s_row] +
expf(row_m - mi_new[s_row]) * row_l;
}
```
This implements the numerically stable softmax algorithm.
For each row:
1. Find the maximum value for numerical stability
2. Compute exponentials normalized by the maximum
3. Sum the normalized exponentials
4. Update the running maximum and sum for the online softmax computation
**Output Computation and Update**
```
for (int col = s_col; col < d; col += Bc) {
float acc = 0.f;
for (int c = 0; c < Bc; c++)
acc += Sij[s_row * Bc + c] * Vj[c * d + col];
int global_row = (i * Br) + s_row;
if (global_row < N) {
Oi[s_row * d + col] = (1 / li_new[s_row]) *
((li[s_row] * expf(mi[s_row] - mi_new[s_row]) * Oi[s_row * d + col]) +
(expf(mij_dash[s_row] - mi_new[s_row]) * acc));
O[qkv_off + global_row * d + col] = Oi[s_row * d + col];
}
}
```
This final section:
1. Computes the matrix multiplication between the softmax probabilities and the Value matrix
2. Updates the output using the online softmax algorithm
3. Each thread may compute multiple output elements (when d > Bc)
4. The reason for the complex update formula is to ensure numerical stability while accumulating partial results
…
Finally, we update the running maximum and sum values in global memory for the next iteration.
This is crucial for the online softmax computation across blocks.