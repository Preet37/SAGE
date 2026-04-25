# Source: https://arxiv.org/pdf/2601.14277.pdf
# Author: Uygar Kurt
# Title: [PDF] Which Quantization Should I Use? A Unified Evaluation of llama.cpp ...
# Fetched via: trafilatura
# Date: 2026-04-09

Which Quantization Should I Use? A Unified Evaluation of llama.cpp Quantization on Llama-3.1-8B-Instruct
Abstract
Quantization is a practical technique for making large language models easier to deploy by reducing the precision used to store and operate on model weights. This can lower memory use and improve runtime feasibility on constrained hardware, which is especially relevant for users running models locally. Quantization in llama.cpp enables large language models to run on commodity hardware, but available formats are often evaluated inconsistently, making it hard to choose among schemes. We present a unified empirical study of the llama.cpp quantization on a single modern model, Llama-3.1-8B-Instruct (FP16, GGUF), covering 3–8 bit K-quant and legacy formats. We evaluate downstream task performance across standard reasoning, knowledge, instruction-following, and truthfulness benchmarks, and also measure perplexity and CPU throughput (prefill/decoding) alongside model size, compression, and quantization time. Ultimately, this work is a practical guide for choosing a llama.cpp quantization scheme, helping readers make informed, context-aware decisions for their intended use and resource budget.
1 Introduction
Large language models (LLMs) have rapidly become a core building block of modern AI systems. Yet, their computational and memory requirements remain a significant barrier to deployment on non-datacenter-scale hardware. A dense 8–70 B parameter model in full-precision FP16 commonly requires tens to hundreds of gigabytes of memory for inference, placing it beyond the reach of commodity CPUs, consumer GPUs, and edge devices. Quantization replaces high-precision floating-point weights and activations with low-precision integer or custom formats. It has therefore become a central technique for making LLMs practical in resource-constrained settings. Prior work has demonstrated that 8-bit and even 4-bit representations can preserve most of the predictive performance of full-precision transformers while reducing memory and bandwidth costs by factors of 2 to 4 [[24](https://arxiv.org/html/2601.14277v1#bib.bib11)][[6](https://arxiv.org/html/2601.14277v1#bib.bib2)][[5](https://arxiv.org/html/2601.14277v1#bib.bib7)], enabling the deployment of models with tens or hundreds of billions of parameters on a single accelerator.
The research community has developed a rich family of quantization methods for LLMs, including mixed-precision matrix multiplication (LLM.int8()) [[3](https://arxiv.org/html/2601.14277v1#bib.bib1)], post-training weight-only methods such as GPTQ [[6](https://arxiv.org/html/2601.14277v1#bib.bib2)] and AWQ [[15](https://arxiv.org/html/2601.14277v1#bib.bib3)], and fine-tuning approaches such as QLoRA [[4](https://arxiv.org/html/2601.14277v1#bib.bib4)]. These methods are often evaluated in PyTorch-based pipelines using a small number of base models, and a large volume of recent work has begun to systematically compare their behavior across benchmarks and microscaling formats [[7](https://arxiv.org/html/2601.14277v1#bib.bib12)][[10](https://arxiv.org/html/2601.14277v1#bib.bib13)][[28](https://arxiv.org/html/2601.14277v1#bib.bib14)][[13](https://arxiv.org/html/2601.14277v1#bib.bib15)][[27](https://arxiv.org/html/2601.14277v1#bib.bib16)][[17](https://arxiv.org/html/2601.14277v1#bib.bib17)].
llama.cpp111https://github.com/ggml-org/llama.cpp is a community-driven, highly optimized C/C++ inference engine targeting CPUs and lightweight GPUs. The primary goal of llama.cpp is to enable "LLM inference with minimal setup and state-of-the-art performance on a wide range of hardware," and it is widely adopted for running quantized open-weight models locally. To support this goal, llama.cpp implements a large set of weight-only quantization formats in the GGUF file format, including the original schemes (Q4_0, Q4_1, Q5_0, Q5_1, Q8_0), which divides the weight matrices into groups, and the more recent "K-quant" family (Q2_K, Q3_K*, Q4_K*, Q5_K*, Q6_K), which use superblocks and additional tricks to improve quality at a given model size. These formats have primarily been designed and iterated in an engineering-driven, community-centric workflow. New quantizers are introduced and tuned via GitHub issues, pull requests, and third-party model conversions, rather than through formal algorithmic descriptions and peer-reviewed evaluation. As a result, practical guidance on "which GGUF quantization to use" is dominated by anecdotal advice and perplexity measurements, with no unified experimental framework for comparison.
This situation poses a significant challenge. Users of llama.cpp must choose among a dozen or more quantization configurations that trade off model size, inference speed, and quality in non-obvious ways. Yet existing evaluations typically (i) focus on language-model perplexity on Wikitext-2 or similar corpora, (ii) mix results across heterogeneous base models and instruction-tuned variants, and (iii) rarely report downstream task performance in a unified way. Consequently, it is difficult to answer even basic questions such as "How much quality do I lose by moving from Q8_0 to Q4_K_M on a modern Llama-3-class model?" or "Do 3-bit K-quants remain usable on downstream tasks?" in a principled, model-specific manner.
In this paper, we address this gap by presenting a comprehensive empirical study of the llama.cpp quantization methods using widely available Llama-3.1-8B-Instruct [[8](https://arxiv.org/html/2601.14277v1#bib.bib18)]. We quantify the trade-offs among model quality, memory footprint, and quantization cost across a broad set of GGUF formats, ranging from 3-bit to 8-bit weights. Concretely, we:
-
•
Evaluate 13 quantization configurations (Q3_K*, Q4_0/1, Q4_K*, Q5_0/1, Q5_K*, Q6_K, Q8_0) alongside a full-precision FP16 baseline, all derived from the same Llama-3.1-8B-Instruct checkpoint and quantized with the official llama.cpp tooling.
-
•
Measure downstream performance on a suite of established benchmarks that probe reasoning, world knowledge, and instruction-following: GSM8K [
[2](https://arxiv.org/html/2601.14277v1#bib.bib19)], HellaSwag [[25](https://arxiv.org/html/2601.14277v1#bib.bib20)], IFEval [[29](https://arxiv.org/html/2601.14277v1#bib.bib21)], MMLU [[9](https://arxiv.org/html/2601.14277v1#bib.bib22)], and TruthfulQA [[16](https://arxiv.org/html/2601.14277v1#bib.bib23)]. These scores complement perplexity on Wikitext-2 [[18](https://arxiv.org/html/2601.14277v1#bib.bib24)], providing a richer view of how quantization affects actual task behavior. -
•
We conduct a thorough analysis of the size reduction, benchmark score reduction, and perplexity increase across different quantization schemes, on which strategy is best to use in which situation.
-
•
Characterize efficiency trade-offs by reporting model size, compression ratio, and wall-clock quantization time on a dual-socket Intel Xeon Platinum 8488C system with AVX-512/BF16 support, using a common GGUF FP16 input model.
-
•
We evaluate CPU inference throughput (prefill and decoding) for all quantization configurations, highlighting the impact of quantization choices on real-world inference performance.
-
•
We open-sourced all quantized models generated in this paper on HuggingFace for the community to use and replicate our results 222https://huggingface.co/uygarkurt/Llama-3.1-8B-Instruct-GGUF.
By grounding our analysis in a single, strong, widely deployed model and a consistent evaluation pipeline, we aim to consolidate fragmented knowledge about the llama.cpp quantization into quantitative, reproducible evidence. Beyond providing practical recommendations for choosing GGUF quantization schemes for Llama-3.1-8B-Instruct, our study offers a template for future work on other architectures and backends, and highlights where the community-driven formats of llama.cpp aligns with, or diverges from, the behavior predicted by more general LLM quantization theory.
2 Background & Related Work
2.1 Post Training Quantization of Large Language Models
Modern large language models (LLMs) are usually trained and distributed in floating-point (e.g., FP16/BF16/FP32). The llama.cpp toolchain targets efficient local inference by applying post-training quantization (PTQ) to the model weights and storing them in GGUF/GGML quantized tensor formats (e.g., Q4_0, Q4_1, Q5_0, Q8_0, Q*_K, IQ*). At runtime, the model loads these quantized weight tensors—often via memory mapping—and executes optimized kernels that operate directly on the packed low-bit representations. Activations are generally maintained in floating-point precision (FP16/FP32/BF16 depending on the backend and build), although some quantized kernels temporarily quantize activations (e.g., to Q8_0) within individual operations.
In llama.cpp, the GGML/GGUF formats use block-wise uniform quantization. They pack weights into quantized integer values and store a small amount of per-block metadata (a scale, and sometimes an offset) needed to map between real values and quantized integer values. Concretely, for a real scalar w and an integer code range with levels, an affine quantizer has the form
| (1) |
with scale and integer zero-point . In GGML-style weight quantization, ([1](https://arxiv.org/html/2601.14277v1#S2.E1)) is instantiated per block rather than per tensor. For a block vector (typically for the standard formats), one stores block metadata (or an equivalent parameterization) and packed quantized integer values for each entry .
This view makes the connection between named GGML quantization types and affine quantizers explicit. For example, Q4_0 is a symmetric, block-wise 4-bit quantizer in which each block of floats stores a single scale and 4-bit signed quantized integer values that represent integers in (packed as nibbles); dequantization is equivalent to a symmetric affine quantizer with and . By contrast, Q4_1 is an affine (asymmetric) block quantizer that stores both a block scale and a block offset (often described as a stored minimum), so that dequantization takes the form
| (2) |
which corresponds to ([1](https://arxiv.org/html/2601.14277v1#S2.E1)) with a nonzero effective offset. The same block-wise pattern extends to other basic formats (Q5_0, Q5_1, Q8_0), differing mainly in and in whether an offset/minimum is stored.
A useful first-order characterization of the accuracy–bit-width trade-off comes from the standard high-resolution approximation: away from clipping, the scalar quantization error is modeled as uniform on with step size . For a symmetric -bit uniform quantizer over with , one has , giving
| (3) |
so that increasing by one bit typically reduces the modeled variance by a factor of (subject to deviations from the assumptions due to clipping, heavy tails, and non-uniform error weighting). In llama.cpp, block-wise quantization changes the relevant and from a global tensor range to a local block range, which is precisely why finer grouping (smaller blocks / more scales) often improves quality at a fixed nominal bit-width.
In the PTQ taxonomy, llama.cpp is primarily employs weight-only quantization. It quantizes weights offline into GGUF for inference, rather than storing quantized activations.
Quant types also differ by grouping/metadata. Standard formats quantize blocks of weights with a per-block scale (and sometimes an offset/min), whereas the _K family uses -weight super-blocks split into smaller groups with additional (often quantized) scale/min metadata to improve low-bit fidelity, i.e., a hierarchical affine quantizer.
2.2 llama.cpp and Its Quantization Schemes
| Scheme | Bits (approx.) | Brief description / intuition |
| Q3_K_S | K-block 3-bit, “small” variant, emphasizes compression | |
| Q3_K_M | K-block 3-bit, “medium” trade-off | |
| Q3_K_L | K-block 3-bit, “large” / quality-oriented | |
| Q4_0 | Older 4-bit scheme, simple, widely available | |
| Q4_1 | 4-bit with different scaling design | |
| Q4_K_S/M | Newer K-block 4-bit, tuned for speed / quality | |
| Q5_0/1 | 5-bit schemes, near-FP16 quality in many tasks | |
| Q5_K_* | K-block 5-bit, more modern variants | |
| Q6_K | High-quality, near-FP16 | |
| Q8_0 | Very close to FP16, reference-ish baseline |
llama.cpp is a C/C++ inference engine designed to run LLaMA and compatible transformer models with minimal dependencies and high efficiency across CPUs and GPUs. It relies on the GGML tensor library and the GGUF model format, which stores model weights (optionally quantized) alongside metadata for memory-mapped, zero-copy loading. Within this ecosystem, quantization is a first-class feature. Most deployment scenarios rely on quantized GGUF models rather than full-precision checkpoints.
The project supports a rich set of quantization formats, implemented as custom GGML tensor types. At a high level, these fall into two main families relevant to our study. Standard block-wise integer formats (Q4_0, Q4_1, Q5_0, Q5_1, Q8_0) and the more recent K-quant formats (Q2_K, Q3_K_S/M/L, Q4_K_S/M, Q5_K_S/M, Q6_K).
All are weight-only and operate on fixed-size blocks or super-blocks, leaving
selected tensors (e.g. layer norms, embeddings) at higher precision. For convenience, these quantization types are summarized in Table [1](https://arxiv.org/html/2601.14277v1#S2.T1).
Standard integer formats.
The classic or the legacy formats in llama.cpp are:
-
•
Q4_0, Q4_1 (4-bit). Q4_0 is symmetric (no zero-point), while Q4_1 adds a per-block offset/zero-point (affine quantization), which can better accommodate asymmetric weight distributions.
-
•
Q5_0, Q5_1 (5-bit). The 5-bit analogs of Q4_0/Q4_1: symmetric (_0) versus affine (_1). The larger integer grid (e.g., typically spanning ) can reduce quantization error at a modest memory increase.
-
•
Q8_0 (8-bit). Symmetric 8-bit quantization, which is commonly used as a high-fidelity baseline in GGUF pipelines, trades higher storage for accuracy closer to FP16 in many settings.
K-quant formats.
The K-quant family introduces a hierarchical super-block structure that provides additional flexibility in allocating bits and metadata within a tensor. A typical K-quant format partitions weights into super-blocks of 256 values and stores multiple (often quantized) scale/min parameters per sub-block. Some variants also use mixed precision across sub-blocks. This leads to a non-integer effective bits-per-weight (bpw), e.g., bpw for Q3_K_S and bpw for Q4_K_M. The suffixes _S, _M, and _L denote small/medium/large variants that trade off compression and fidelity. Within this family, we focus on:
-
•
3-bit: Q3_K_S, Q3_K_M, Q3_K_L. Variants with effective bit-widths of roughly , , and bits. S prioritizes smaller metadata and faster kernels, M balances speed/quality, and L allocates more information to improve reconstruction fidelity.
-
•
4-bit: Q4_K_S, Q4_K_M. Effective bit-widths of roughly and bits; typically higher-fidelity than Q4_0/Q4_1 at similar (or slightly higher) size.
-
•
5-bit: Q5_K_S, Q5_K_M. Effective bit-widths of roughly and bits, offering a further quality/size trade-off.
-
•
6-bit baseline: Q6_K. A high-fidelity K-quant with effective bit-width around bits, often used when accuracy is prioritized while still reducing memory versus FP16.
Crucially, these schemes are largely community-driven. New formats, effective bit estimates, and recommended usage patterns have emerged through GitHub issues, pull requests, and informal benchmark reports. While recent documentation has begun to systematize this knowledge, there remains no unified, model-specific evaluation that compares these formats on a modern LLM using a common pipeline.
2.3 Existing Quantization Benchmarks
A growing body of work examines how quantization impacts LLM quality and deployment cost, typically reporting trade-offs among perplexity, downstream accuracy, latency, and memory footprint. Much of this literature focuses on post-training quantization (PTQ) and related recipes such as LLM.int8(), GPTQ, AWQ, SpQR, SmoothQuant [[22](https://arxiv.org/html/2601.14277v1#bib.bib6)], Quip# [[21](https://arxiv.org/html/2601.14277v1#bib.bib25)], and QLoRA, and is evaluated across multiple model families (GPT[[1](https://arxiv.org/html/2601.14277v1#bib.bib26)], OPT[[26](https://arxiv.org/html/2601.14277v1#bib.bib27)], LLaMA[[19](https://arxiv.org/html/2601.14277v1#bib.bib28)][[20](https://arxiv.org/html/2601.14277v1#bib.bib29)][[8](https://arxiv.org/html/2601.14277v1#bib.bib18)], Qwen [[23](https://arxiv.org/html/2601.14277v1#bib.bib30)]) and heterogeneous task suites. More recent empirical work has also expanded coverage to newer instruction-tuned and multimodal-capable backbones, including targeted studies of LLaMA 3 quantization behavior across bit-widths and methods [[10](https://arxiv.org/html/2601.14277v1#bib.bib13)], as well as stack- and model-specific analyses for newly released families such as Qwen3 [[28](https://arxiv.org/html/2601.14277v1#bib.bib14)].
Recent studies also move toward more standardized, multi-method comparisons. Jin et al.[[12](https://arxiv.org/html/2601.14277v1#bib.bib8)] provide a broad evaluation of quantization strategies across multiple model scales, emphasizing efficiency–quality trade-offs and discussing when perplexity can serve as a proxy for downstream behavior. Complementary benchmarking efforts, including the qLLM-eval framework [[14](https://arxiv.org/html/2601.14277v1#bib.bib9)] and related evaluations of quantized LLMs, compare multiple PTQ approaches (e.g., AWQ and SmoothQuant) across tasks spanning language modeling, classification, and question answering [[14](https://arxiv.org/html/2601.14277v1#bib.bib9)]. LLMC [[7](https://arxiv.org/html/2601.14277v1#bib.bib12)] further pushes in this direction by offering a unified compression toolkit intended to enable fairer comparisons across a wide range of quantization configurations, numeric formats, and model types (including vision-language settings). At the same time, the community has increasingly emphasized behavioral coverage beyond easy accuracy proxies: large-scale evaluations across instruction-following and hallucination-style benchmarks highlight that quantization effects can vary substantially with task difficulty and model size [[13](https://arxiv.org/html/2601.14277v1#bib.bib15)]. Other reports are more domain- or stack-specific, such as cross-lingual analyses for LLaMA-family models or industrial evaluations that focus on particular formats (e.g., FP8) and hardware/software ecosystems [[11](https://arxiv.org/html/2601.14277v1#bib.bib10)]. In parallel, dedicated studies on reasoning-focused models and benchmarks show that aggressive low-bit settings can be especially risky for multi-step reasoning, and that conclusions can depend on whether weights, activations, and/or KV cache are quantized [[17](https://arxiv.org/html/2601.14277v1#bib.bib17)].
Despite this progress, the existing evidence is often less actionable for llama.cpp style deployment. First, many evaluations remain perplexity-centric (often on corpora such as WikiText-2 or C4) and include only limited downstream coverage; while perplexity is informative, it does not fully characterize instruction-following, reasoning, or safety-relevant behavior that dominates real-world use of instruction-tuned models. Second, results are frequently aggregated across different base models and task suites, which confounds direct, format-to-format comparisons and makes it difficult to isolate the interaction between bit-width, quantization scheme, and a single modern architecture (e.g., Llama 3.1–8B). Third, most academic benchmarks operate in PyTorch/JAX with generic quantization operators, and to our knowledge do not systematically evaluate the GGUF-specific quantization formats as implemented in llama.cpp (e.g., Q3_K_S/M/L, Q4_K_S/M, Q5_K_S/M, Q6_K, and Q4_0/Q4_1/Q5_0/Q5_1/Q8_0), despite their widespread practical use. Even model-specific deployment-oriented studies [[27](https://arxiv.org/html/2601.14277v1#bib.bib16)] typically compare quantization at the level of bit-width or strategy, rather than at the level of concrete GGUF formats, and therefore do not directly inform GGUF format selection in llama.cpp pipelines.
Our study addresses this gap by fixing a single widely deployed model (Llama-3.1-8B Instruct), quantizing it with the official llama.cpp toolchain across a broad set of GGUF formats, and evaluating all variants under a unified pipeline. We report both perplexity and a diverse set of downstream benchmarks (e.g., GSM8K, HellaSwag, IFEval, MMLU, TruthfulQA), while controlling the base model, evaluation harness, and hardware environment to enable an apples-to-apples comparison of llama.cpp quantization schemes that complement prior method-centric studies and newer multi-task evaluations.
3 Experimental Setup
3.1 Base Model & Environment
All experiments use Llama-3.1-8B-Instruct converted to GGUF and evaluated in F16 as the reference (original) model. For all evaluations, prompts were formatted using the default Llama-3.1-8B-Instruct chat template. The resulting input GGUF file size is MiB ( GiB). Quantization and evaluation were performed on a dual-socket CPU server with two Intel Xeon Platinum 8488C processors, totaling physical cores ( threads), with AVX-512 and BF16 support enabled. We used llama.cpp (commit b7600) 333[https://github.com/ggml-org/llama.cpp/tree/b7600](https://github.com/ggml-org/llama.cpp/tree/b7600) for GGUF quantization and perplexity/throughput measurements, and the EleutherAI evaluation harness lm_eval (v0.4.9.2) 444[https://github.com/EleutherAI/lm-evaluation-harness/tree/v0.4.9.2](https://github.com/EleutherAI/lm-evaluation-harness/tree/v0.4.9.2) for downstream benchmark scoring. We used the default evaluation harness and llama.cpp configurations for downstream benchmark scoring and perplexity scoring.
3.2 Quantization Configurations
We evaluate community-standard llama.cpp GGUF quantization schemes spanning nominal 3–8 bit weight formats: , , , , and . All quantized models are produced from the same FP16 GGUF reference input using the official llama.cpp quantization utility (e.g., llama-quantize/quantize), with the scheme identifier as the only varying parameter. A canonical command pattern is:
./llama-quantize <f16.gguf> <out.gguf> <SCHEME>
We measure wall-clock quantization time on the same machine used for inference.
Let denote the FP16 input model size and the resulting quantized size. We compute size reduction as .
3.3 Evaluation Tasks & Datasets
To characterize the accuracy–efficiency trade-offs induced by llama.cpp quantization, we evaluate each model on a benchmark suite designed for broad coverage: multi-step math (GSM8K), commonsense multiple-choice reasoning (HellaSwag), instruction following (IFEval), broad knowledge (MMLU), truthfulness (TruthfulQA), and intrinsic language modeling quality (WikiText-2 Perplexity). Because strong base models typically perform well on these axes in full precision, this suite makes it easy to detect where quantization degrades capabilities (or leaves them largely intact), rather than relying on a single proxy task.
We evaluate mathematical reasoning on GSM8K (task version v3) using 5-shot prompting. Commonsense reasoning is evaluated on HellaSwag (task version v1); instruction following is measured with IFEval (task version v4); broad knowledge is evaluated on MMLU (task version v2); and truthfulness is assessed with TruthfulQA. Finally, we report perplexity on WikiText-2 as a prompt-independent measure of language modeling quality. WikiText-2 is obtained via llama.cpp ./scripts/get-wikitext-2.sh, and perplexity is computed with identical runtime settings across quantization schemes. We also record throughput under fixed settings of (prompt processing) and (token generation), enabling direct quality–speed comparisons.
The benchmark scores GSM8K, HellaSwag, IFEval, MMLU and TruthfulQA is evaluated with the LLM Evaluation Harness, while WikiText-2 perplexity and throughput are computed separately using llama.cpp’s evaluation script, since it provides the perplexity implementation used by llama-bench and llama-perplexity by llama.cpp.
4 Quantization Results and Trade-offs
4.1 Overall Accuracy-Compression behavior
Table [2](https://arxiv.org/html/2601.14277v1#S4.T2) summarizes a clear but non-monotonic relationship between nominal bit-width, downstream accuracy, and intrinsic language-modeling quality. Complete evaluation suite with full metrics can be viewed in Appendix [B](https://arxiv.org/html/2601.14277v1#A2). As expected, the most aggressive 3-bit configurations deliver the largest space savings, but they also introduce the largest average degradation across the benchmark suite. The strongest compression point, Q3_K_S, achieves the highest reduction yet yields the largest drop in the unweighted benchmark mean (Avg), and it also exhibits the largest perplexity increase on WikiText-2. Moving within the 3-bit family (Q3_K_M and Q3_K_L) reduces the damage substantially, indicating that the implementation details of a quantization format (e.g., scaling granularity and block structure) matter at least as much as the headline “3-bit” label.
More interestingly, Q5_0 and Q5_1 quantization schemes slightly exceed the F16 baseline on the downstream mean under our fixed decoding and evaluation protocol. In Table [2](https://arxiv.org/html/2601.14277v1#S4.T2), Q5_0 attains the highest Avg among all configurations while still reducing model size by roughly sixty-five percent. These small gains over F16 should be interpreted cautiously. Even with deterministic decoding, finite benchmark sets introduce evaluation variance, and modest improvements can reflect noise or idiosyncrasies of the scoring pipeline rather than true general superiority. The robust takeaway is that a carefully chosen mid-bit quantization can preserve the baseline capability envelope surprisingly well while dramatically reducing storage and improving throughput.
| Benchmarks () | |||||||||
| Bits | Quant | Size Reduction (%) | GSM8K | HSwag | IFEval | MMLU | TQA | Avg | PPL |
| F16 (baseline) | – | 77.63 | 72.51 | 78.93 | 63.50 | 54.79 | 69.47 | 7.32 | |
| 3 | Q3_K_S | 77.23 | 68.31 | 71.87 | 73.89 | 59.31 | 54.08 | 65.49 | 8.96 |
| Q3_K_M | 75.03 | 73.16 | 73.41 | 77.19 | 62.01 | 54.56 | 68.07 | 7.96 | |
| Q3_K_L | 73.14 | 74.07 | 73.54 | 79.14 | 62.31 | 54.84 | 68.78 | 7.81 | |
| 4 | Q4_0 | 71.03 | 75.66 | 71.88 | 77.46 | 62.20 | 52.68 | 67.98 | 7.74 |
| Q4_1 | 68.11 | 76.04 | 71.29 | 78.45 | 63.17 | 55.01 | 68.79 | 7.72 | |
| Q4_K_S | 70.83 | 77.33 | 72.79 | 80.26 | 62.06 | 53.40 | 69.17 | 7.62 | |
| Q4_K_M | 69.41 | 77.41 | 72.35 | 79.06 | 62.43 | 54.49 | 69.15 | 7.56 | |
| 5 | Q5_0 | 65.19 | 79.08 | 72.63 | 80.14 | 63.18 | 54.57 | 69.92 | 7.43 |
| Q5_1 | 62.27 | 78.47 | 72.08 | 79.79 | 63.68 | 54.62 | 69.73 | 7.43 | |
| Q5_K_S | 65.19 | 75.66 | 72.67 | 79.50 | 63.36 | 53.90 | 69.02 | 7.43 | |
| Q5_K_M | 64.35 | 78.54 | 72.33 | 78.67 | 62.80 | 54.45 | 69.36 | 7.40 | |
| 6 | Q6_K | 58.98 | 78.17 | 72.48 | 77.63 | 63.17 | 54.71 | 69.23 | 7.35 |
| 8 | Q8_0 | 46.87 | 77.48 | 72.52 | 78.79 | 63.43 | 54.81 | 69.41 | 7.33 |
GSM8K: flexible-extract. HSwag: acc_norm). IFEval: mean of four accuracies (instruction/prompt loose/strict). MMLU: acc. TQA: MC2 accuracy. Avg: unweighted mean of the five benchmark scores (GSM8K, HSwag, IFEval, MMLU, TQA), excluding PPL. PPL: WikiText-2 perplexity (lower is better). Cells show means rounded to 2 decimals; standard errors and additional breakdowns are reported in Appendix [B](https://arxiv.org/html/2601.14277v1#A2).
4.2 Task Sensitivity Under Quantization
The per-benchmark columns in Table [2](https://arxiv.org/html/2601.14277v1#S4.T2) make clear that quantization reshapes model behavior in a task-dependent way rather than inducing a uniform accuracy shift. Multi-step arithmetic reasoning on GSM8K is among the most sensitive dimensions: relative to the F16 baseline of , the most aggressive 3-bit configuration Q3_K_S drops to (a point change), while moving within the 3-bit family already recovers a substantial fraction of the loss, reaching for Q3_K_M and for Q3_K_L. At 4 bits, the gap largely closes, with Q4_0 and Q4_1 scoring and , and the K-quantized variants essentially matching baseline at (Q4_K_S) and (Q4_K_M). Several 5-bit and higher settings even exceed F16 on GSM8K, including Q5_0 at , Q5_1 at , Q5_K_M at , and Q6_K at , while Q5_K_S is a notable exception that falls back to despite sharing the same nominal bit-width. This non-monotonicity indicates that GSM8K is sensitive not just to bit-width, but to the particular quantization format and its induced error structure.
In contrast, commonsense multiple-choice accuracy on HellaSwag is comparatively stable across the entire sweep. The F16 baseline is , and most quantized variants remain within roughly a one-point neighborhood: the lowest value appears at Q4_1 with , whereas the strongest scores slightly exceed baseline, such as Q3_K_L at and Q3_K_M at . Even the 8-bit entry Q8_0 essentially reproduces baseline at . This small variation, even with large changes in compression ratio, suggests that HellaSwag performance is largely unaffected by the noise introduced by these quantization schemes.
Instruction-following robustness, as measured by IFEval, sits between these extremes. While Q3_K_S shows a sizable regression from (F16) down to , several mid-bit settings are not merely resilient but improve over baseline. Notably, Q3_K_L reaches , Q4_K_S increases to , and Q5_0 attains , indicating that moderate quantization can preserve (and occasionally enhance) instruction-following outcomes. At the same time, improvements are not guaranteed by higher precision: Q6_K drops to and Q8_0 remains close to baseline at , reinforcing that IFEval is sensitive to format details rather than bit-width alone.
Broad knowledge on MMLU shows moderate sensitivity with a clear failure mode at the most aggressive setting but otherwise small fluctuations. From a baseline of , Q3_K_S declines to , yet most other configurations stay within about a point of F16. For example, Q4_1 and Q6_K both score , Q8_0 reaches , and Q5_1 slightly surpasses baseline at .
For TruthfulQA, although Q4_0 dips to versus for F16, many formats remain close, including Q4_1 at and Q8_0 at .
These benchmark-specific behaviors are reflected in the overall average as well: Q3_K_S produces the largest aggregate drop (Avg vs. ), while most 4–8 bit schemes cluster tightly near baseline, and Q5_0 achieves the highest mean at .
Finally, the perplexity column provides a useful complementary signal about how aggressively each scheme perturbs the model distribution. F16 yields , whereas the most aggressive 3-bit setting Q3_K_S increases perplexity to , broadly aligning with its across-task accuracy losses. However, perplexity is not a complete predictor of downstream behavior: several 5-bit variants share essentially the same PPL (e.g., for Q5_0, Q5_1, and Q5_K_S) while exhibiting markedly different GSM8K and IFEval outcomes, underscoring that task sensitivity depends on how quantization error interacts with the computation pattern demanded by a benchmark rather than on distributional fit alone.
4.3 Pareto Frontier Analysis: Size Reduction and Performance Tradeoff
Figure [1](https://arxiv.org/html/2601.14277v1#S4.F1) summarizes the compression–quality trade-off using two derived metrics from Table [2](https://arxiv.org/html/2601.14277v1#S4.T2). The x-axis reports reduction as the compression ratio (%), and the y-axis reports AvgLoss (%) computed from the table [2](https://arxiv.org/html/2601.14277v1#S4.T2)’s Avg column as a relative change with respect to the F16 baseline, i.e., , so that negative values correspond to a slight improvement over baseline. Under this two-objective view, a configuration is Pareto-optimal when no other configuration simultaneously achieves higher reduction and lower AvgLoss, and the Pareto frontier therefore enumerates the operating points that remain defensible once both memory savings and aggregate downstream quality are considered.
Reading the frontier from the quality-preserving end, Q5_0 is the most favorable point in terms of AvgLoss, achieving a reduction while slightly improving the aggregate mean (AvgLoss ). This is not merely a marginal win. It also removes several nearby options from consideration because they are strictly dominated under the two metrics, including Q5_1, Q5_K_S, and Q5_K_M, all of which deliver less reduction and higher AvgLoss than Q5_0. When additional compression is required, the frontier moves to Q4_K_S, which increases reduction to while keeping the quality penalty small (AvgLoss ). This point captures a strong trade-off within the 4-bit family, and it dominates plausible alternatives such as Q4_K_M and Q4_1 by offering both higher reduction and lower AvgLoss.
Pushing further toward maximum compression, Q3_K_L reaches reduction with AvgLoss , representing a modest additional compression gain for a still-controlled aggregate degradation. Q3_K_M attains a reduction with AvgLoss , and becomes Pareto-optimal because no other evaluated scheme achieves at least as much reduction with lower AvgLoss. At the extreme end, Q3_K_S attains the largest reduction in the table () and remains Pareto-optimal only because no other scheme matches its reduction, but this comes with a substantially larger quality cost (AvgLoss ), making it appropriate primarily when memory footprint is the overriding constraint.
This Pareto framing also makes clear why more bits are not automatically better once compression is explicitly valued. Schemes like Q6_K and Q8_0 stay close to baseline quality, but they are nevertheless dominated because Q5_0 provides both higher reduction and lower AvgLoss. In practical terms, the efficient set implied by Figure [1](https://arxiv.org/html/2601.14277v1#S4.F1) is compact: Q5_0 is the accuracy-favoring choice with meaningful compression, Q4_K_S is the natural balanced default when stronger reduction is needed, Q3_K_L offers a further compression step with moderate additional loss, Q3_K_M provides an additional compression step at a higher but still controlled aggregate loss, and Q3_K_S is the maximum-reduction endpoint for the most memory-constrained deployments.
4.4 Throughput Analysis
Table [3](https://arxiv.org/html/2601.14277v1#S4.T3) complements the accuracy results with throughput measured under standardized settings (pp=512, tg=128). Token-generation speed (tg128) increases substantially for lower-bit schemes, with the most compressed formats producing the largest gains. This behavior is consistent with quantization reducing memory bandwidth pressure and improving cache residency, which are often limiting factors in CPU inference. The most compressed configuration achieves the highest token-generation throughput, making it attractive for interactive settings where latency per generated token dominates.
Prompt-processing throughput (pp512) varies more irregularly. Unlike pure decoding, prompt processing can be affected by different kernel choices, memory access patterns, and the balance between compute and bandwidth across formats. The key operational point is that throughput improvements are not solely determined by nominal bit-width, and measuring both pp and tg under a fixed configuration is important when the application alternates between long prompts and long generations.
When we combine throughput with the Pareto analysis, Q4_K_S again appears as a strong default. It sits on the non-dominated accuracy–compression frontier while delivering a large generation-speed gain relative to F16. In contrast, Q3_K_S maximizes throughput and compression, but the associated accuracy loss is large enough that it is best treated as a specialized choice for constrained environments rather than a general-purpose setting.
| Scheme | pp512 | tg128 |
| F16 | 79.57 1.00 | 2.83 0.01 |
| Q3_K_S | 57.39 3.01 | 9.91 0.03 |
| Q3_K_M | 68.86 1.36 | 6.52 0.23 |
| Q3_K_L | 58.34 1.93 | 7.93 0.06 |
| Q4_0 | 97.35 0.68 | 4.36 0.20 |
| Q4_1 | 55.20 1.61 | 6.80 0.15 |
| Q4_K_S | 92.52 1.53 | 4.65 0.15 |
| Q4_K_M | 87.70 0.70 | 5.12 0.37 |
| Q5_0 | 61.44 2.47 | 6.66 0.06 |
| Q5_1 | 45.98 2.17 | 6.33 0.26 |
| Q5_K_S | 55.31 1.67 | 5.98 0.02 |
| Q5_K_M | 58.24 2.05 | 6.85 0.13 |
| Q6_K | 59.81 1.07 | 6.33 0.13 |
| Q8_0 | 71.42 3.15 | 5.03 0.16 |
[3.1](https://arxiv.org/html/2601.14277v1#S3.SS1)
4.5 Choosing Quantization Scheme In Practice
Table 4 is intended as a quick, deployment-oriented guide for selecting a quantization format without having to scan the full set of results. When memory and disk are the primary bottlenecks, lower-bit K-quants deliver the largest reductions and strong speedups, but Table 4 makes clear that the most aggressive settings also incur the largest perplexity increases and average benchmark drops.
For general-purpose interactive use, the table points to mid-bit formats as sensible defaults: 4-bit K-quants typically offer near-maximal compression at 4-bit while keeping task performance close to the FP16 baseline, and a high-quality 5-bit option is a common step up when additional quality margin is needed. When preserving behavior is the priority (e.g., instruction following or reasoning sensitivity), Table 4 favors these mid-bit regimes over very low-bit choices, while conservative 6–8 bit settings remain appropriate when perplexity and downstream drift must be minimized, and memory budgets allow.
| Scenario | Primary constraint / goal | Deployable regimes (examples) | Trade-offs (from your results) |
|---|---|---|---|
| Edge / disk- or RAM-limited serving | Minimize footprint; accept visible quality loss | 3-bit (ultra-compressed): Q3_K_S, Q3_K_L | Biggest size reduction and very strong tg speedups, but the largest Avg drops and highest PPL increases (especially Q3_K_S); Q3_K_M is the safer 3-bit choice. |
| Interactive chat on CPU (general-purpose) | Best overall balance of size, quality, and speed | 4–5 bit (balanced default): Q4_K_S; also Q4_0, Q4_K_M; or Q5_0 if size allows | Q4_K_S gives near-max 4-bit compression with Avg close to F16 and solid tg gains; Q5_0 is larger but delivers the strongest Avg and faster tg. |
| Throughput-first serving (quality-aware) | Max tokens/s at acceptable quality | 3–5 bit: Q3_K_M (if loss is OK), Q5_0/Q5_K_M (safer), Q4_K_S (more compression) | 3-bit maximizes speed but can hurt math/instruction tasks; Q5_0/Q5_K_M keep quality near (or above) baseline while staying very fast; Q4_K_S trades some throughput for more compression. |
| Accuracy-first CPU deployment (not full F16) | Minimize behavior drift vs baseline; accept larger model | 6–8 bit (conservative): Q6_K, Q8_0 | Perplexity is closest to F16 and downstream deltas are small, but compression is weaker than the best 4–5 bit options. |
| Math-/reasoning-heavy workloads | Protect GSM8K-style multi-step performance | 5-bit or strong 4-bit: Q5_0 (also Q5_1), Q4_K_S | Avoid aggressive 3-bit (notably Q3_K_S) which shows the largest GSM8K drop; Q5_0 and Q4_K_S preserve downstream performance with substantial compression. |
| Instruction-following sensitive applications | Protect IFEval-like compliance | 4–5 bit: Q4_K_S, Q5_0 (also Q4_K_M) | IFEval stays strong for several mid-bit schemes; 3-bit is more likely to reduce compliance. |
| Calibration / “LM quality” sensitive (proxy via PPL) | Keep perplexity close to baseline | 6–8 bit (or good 5-bit): Q6_K, Q8_0, Q5_K_M (or Q5_0) | PPL generally worsens as compression increases; if PPL is a hard guardrail, prefer Q6/Q8, with a 5-bit option (e.g., Q5_K_M / Q5_0) as a middle ground. |
5 Conclusion
This paper provides a unified empirical comparison of widely used llama.cpp GGUF quantization formats for a modern instruction-tuned model under a single controlled pipeline, reporting downstream task performance alongside intrinsic quality, footprint, and practical efficiency. The results show that mid-bit quantization can preserve capabilities surprisingly well. In our setting, 5-bit configurations offer an especially strong trade-off, maintaining (and in some cases slightly improving) aggregate downstream scores relative to the FP16 baseline while substantially reducing model size, whereas the most aggressive 3-bit setting exhibits the clearest and most consistent degradations, particularly on reasoning-heavy evaluations.
A key takeaway is that the quantization format matters, not just the nominal bit-width: schemes with similar perplexity can diverge meaningfully on instruction-following and reasoning benchmarks, so intrinsic metrics alone are insufficient to select deployment defaults. These findings motivate a simple evidence-based guidance: prefer high-performing 5-bit options as a robust default when memory is limited but quality is important, consider well-tuned 4-bit K-quant variants when footprint must be pushed further with modest loss, and treat 3-bit choices as budget-driven compromises. Future work should extend the same protocol across additional model families and sizes, diverse hardware targets, and longer-context regimes, and should analyze how format design choices mechanistically relate to the observed task-specific regressions.
References
-
[1]
(2020)
Language models are few-shot learners.
Advances in neural information processing systems 33, pp. 1877–1901.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[2]
(2021)
Training verifiers to solve math word problems.
arXiv preprint arXiv:2110.14168.
Cited by:
[2nd item](https://arxiv.org/html/2601.14277v1#S1.I1.i2.p1.1). -
[3]
(2022)
Gpt3. int8 (): 8-bit matrix multiplication for transformers at scale.
Advances in neural information processing systems 35, pp. 30318–30332.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1). -
[4]
(2023)
Qlora: efficient finetuning of quantized llms.
Advances in neural information processing systems 36, pp. 10088–10115.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1). -
[5]
(2023)
Spqr: a sparse-quantized representation for near-lossless llm weight compression.
arXiv preprint arXiv:2306.03078.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p1.1). -
[6]
(2022)
Gptq: accurate post-training quantization for generative pre-trained transformers.
arXiv preprint arXiv:2210.17323.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p1.1),[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1). -
[7]
(2024)
Llmc: benchmarking large language model quantization with a versatile compression toolkit.
In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing: Industry Track,
pp. 132–152.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1),[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p2.1). -
[8]
(2024)
The llama 3 herd of models.
arXiv preprint arXiv:2407.21783.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p5.1),[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[9]
(2020)
Measuring massive multitask language understanding.
arXiv preprint arXiv:2009.03300.
Cited by:
[2nd item](https://arxiv.org/html/2601.14277v1#S1.I1.i2.p1.1). -
[10]
(2024)
An empirical study of llama3 quantization: from llms to mllms.
Visual Intelligence 2 (1), pp. 36.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1),[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[11]
Comparing modern llm quantization methods across natural languages.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p2.1). -
[12]
(2024)
A comprehensive evaluation of quantization strategies for large language models.
In Findings of the Association for Computational Linguistics ACL 2024,
pp. 12186–12215.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p2.1). -
[13]
(2024)
Exploring the trade-offs: quantization methods, task difficulty, and model size in large language models from edge to giant.
arXiv preprint arXiv:2409.11055.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1),[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p2.1). -
[14]
(2024)
Evaluating quantized large language models.
External Links: 2402.18158
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p2.1). -
[15]
(2024)
Awq: activation-aware weight quantization for on-device llm compression and acceleration.
Proceedings of machine learning and systems 6, pp. 87–100.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1). -
[16]
(2022)
Truthfulqa: measuring how models mimic human falsehoods.
In Proceedings of the 60th annual meeting of the association for computational linguistics (volume 1: long papers),
pp. 3214–3252.
Cited by:
[2nd item](https://arxiv.org/html/2601.14277v1#S1.I1.i2.p1.1). -
[17]
(2025)
Quantization hurts reasoning? an empirical study on quantized reasoning models.
arXiv preprint arXiv:2504.04823.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1),[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p2.1). -
[18]
(2017)
Regularizing and optimizing lstm language models.
arXiv preprint arXiv:1708.02182.
Cited by:
[2nd item](https://arxiv.org/html/2601.14277v1#S1.I1.i2.p1.1). -
[19]
(2023)
Llama: open and efficient foundation language models.
arXiv preprint arXiv:2302.13971.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[20]
(2023)
Llama 2: open foundation and fine-tuned chat models.
arXiv preprint arXiv:2307.09288.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[21]
(2024)
Quip#: even better llm quantization with hadamard incoherence and lattice codebooks.
arXiv preprint arXiv:2402.04396.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[22]
(2023)
Smoothquant: accurate and efficient post-training quantization for large language models.
In International conference on machine learning,
pp. 38087–38099.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[23]
(2025)
Qwen3 technical report.
arXiv preprint arXiv:2505.09388.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[24]
(2022)
Zeroquant: efficient and affordable post-training quantization for large-scale transformers.
Advances in neural information processing systems 35, pp. 27168–27183.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p1.1). -
[25]
(2019)
Hellaswag: can a machine really finish your sentence?.
arXiv preprint arXiv:1905.07830.
Cited by:
[2nd item](https://arxiv.org/html/2601.14277v1#S1.I1.i2.p1.1). -
[26]
(2022)
Opt: open pre-trained transformer language models.
arXiv preprint arXiv:2205.01068.
Cited by:
[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[27]
(2025)
Quantitative analysis of performance drop in deepseek model quantization.
arXiv preprint arXiv:2505.02390.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1),[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p3.5). -
[28]
(2025)
An empirical study of qwen3 quantization.
arXiv preprint arXiv:2505.02214.
Cited by:
[§1](https://arxiv.org/html/2601.14277v1#S1.p2.1),[§2.3](https://arxiv.org/html/2601.14277v1#S2.SS3.p1.1). -
[29]
(2023)
Instruction-following evaluation for large language models.
arXiv preprint arXiv:2311.07911.
Cited by:
[2nd item](https://arxiv.org/html/2601.14277v1#S1.I1.i2.p1.1).
Appendix A Quantization Timings
Table [5](https://arxiv.org/html/2601.14277v1#A1.T5) summarizes the deployment-side properties of each GGUF quantization scheme evaluated in this study: the resulting model size (MiB), the corresponding size reduction relative to the FP16 GGUF input, and the wall-clock time required to perform the quantization with the official llama.cpp tooling on our evaluation system. These measurements complement the main-text quality and throughput results by making explicit the storage savings and one-time conversion overhead associated with each format, which are often decisive constraints in CPU and edge-oriented deployments.
| Scheme | Bits | Size (MiB) | Size reduction (%) | Quant time (s) |
| Q3_K_S | 3 | 3487.27 | 77.23 | 27.04 |
| Q3_K_M | 3 | 3825.27 | 75.03 | 31.82 |
| Q3_K_L | 3 | 4114.27 | 73.14 | 31.37 |
| Q4_0 | 4 | 4437.80 | 71.03 | 27.35 |
| Q4_1 | 4 | 4885.12 | 68.11 | 27.76 |
| Q4_K_S | 4 | 4467.80 | 70.83 | 42.84 |
| Q4_K_M | 4 | 4685.30 | 69.41 | 42.19 |
| Q5_0 | 5 | 5332.43 | 65.19 | 28.21 |
| Q5_1 | 5 | 5779.74 | 62.27 | 29.46 |
| Q5_K_S | 5 | 5332.43 | 65.19 | 37.47 |
| Q5_K_M | 5 | 5459.93 | 64.35 | 36.47 |
| Q6_K | 6 | 6282.97 | 58.98 | 31.19 |
| Q8_0 | 8 | 8137.64 | 46.87 | 29.26 |
Appendix B Full Quantization Results
Table LABEL:tab:benchmark-quant reports the complete set of benchmark outputs underlying the aggregated scores in the main results table, including mean performance (and where applicable, standard error) for each quantization type on every reported task/metric. In addition to overall scores, the table includes alternative scoring variants (e.g., two GSM8K exact-match criteria), multiple views of instruction-following for IFEval (instruction-level vs prompt-level, each under loose vs strict evaluation), MMLU broken down into subject areas, and TruthfulQA reported for multiple-choice variant.
The accuracy/metric abbreviations denote the specific scoring variants used by the evaluation harness. For GSM8K, the reported metric is EM (Exact Match), i.e., the percentage of problems where the model’s final answer exactly matches the gold answer after extraction; FE (Flexible Extract) and SM (Strict Match) specify the extraction filter used before computing EM (FE is lenient in extracting the final numeric answer from text, while SM is stricter about the expected final-answer format). For HellaSwag, A indicates raw multiple-choice acc (accuracy) and AN indicates acc_norm, i.e., normalized accuracy. For IFEval, ILL/ILS correspond to instruction-level loose/strict accuracy (inst_level_loose_acc / inst_level_strict_acc) and PLL/PLS to prompt-level loose/strict accuracy (prompt_level_loose_acc / prompt_level_strict_acc). For MMLU, A denotes overall acc (accuracy), with additional rows reporting subject-group accuracies. And for TruthfulQA, the generation setting reports BA/BD as bleu_acc (BLEU-based accuracy) and bleu_dif (BLEU-based difference), while the multiple-choice settings MC1 and MC2 report A as acc (accuracy).
Unless otherwise noted, the benchmarks were run under the following harness versions and shot settings: GSM8K v3 (5-shot), HellaSwag v1 (0-shot), IFEval v4 (0-shot), MMLU v2 (0-shot), and TruthfulQA v3 (0-shot), with the exception that TruthfulQA MC1 uses v2.
| QType | Task | Metric | Value |
| F16 (baseline) | GSM8K (FE) | EM | 77.63 1.15 |
| GSM8K (SM) | EM | 24.64 1.19 | |
| HellaSwag | A | 57.40 0.49 | |
| HellaSwag | AN | 72.51 0.45 | |
| IFEval | ILL | 83.81 | |
| IFEval | ILS | 81.06 | |
| IFEval | PLL | 77.08 1.81 | |
| IFEval | PLS | 73.75 1.89 | |
| MMLU | A | 63.50 0.38 | |
| MMLU Humanities | A | 59.21 0.68 | |
| MMLU Other | A | 71.97 0.78 | |
| MMLU Social Sciences | A | 74.59 0.77 | |
| MMLU Stem | A | 50.71 0.84 | |
| TruthfulQA Gen | BA | 46.27 1.75 | |
| TruthfulQA Gen | BD | -22.91 23.06 | |
| TruthfulQA MC1 | A | 39.53 1.71 | |
| TruthfulQA MC2 | A | 54.79 1.60 | |
| Q3_K_S | GSM8K (FE) | EM | 68.31 1.28 |
| GSM8K (SM) | EM | 22.14 1.14 | |
| HellaSwag | A | 56.54 0.49 | |
| HellaSwag | AN | 71.87 0.45 | |
| IFEval | ILL | 79.50 | |
| IFEval | ILS | 76.86 | |
| IFEval | PLL | 71.16 1.95 | |
| IFEval | PLS | 68.02 2.01 | |
| MMLU | A | 59.31 0.39 | |
| MMLU Humanities | A | 52.67 0.68 | |
| MMLU Other | A | 67.81 0.82 | |
| MMLU Social Sciences | A | 70.07 0.81 | |
| MMLU Stem | A | 50.36 0.86 | |
| TruthfulQA Gen | BA | 47.37 1.75 | |
| TruthfulQA Gen | BD | -30.76 32.44 | |
| TruthfulQA MC1 | A | 36.96 1.69 | |
| TruthfulQA MC2 | A | 54.08 1.58 | |
| Q3_K_M | GSM8K (FE) | EM | 73.16 1.22 |
| GSM8K (SM) | EM | 9.86 0.82 | |
| HellaSwag | A | 57.62 0.49 | |
| HellaSwag | AN | 73.41 0.44 | |
| IFEval | ILL | 82.49 | |
| IFEval | ILS | 79.14 | |
| IFEval | PLL | 75.97 1.84 | |
| IFEval | PLS | 71.16 1.95 | |
| MMLU | A | 62.01 0.39 | |
| MMLU Humanities | A | 58.04 0.69 | |
| MMLU Other | A | 68.81 0.81 | |
| MMLU Social Sciences | A | 71.60 0.79 | |
| MMLU Stem | A | 51.86 0.85 | |
| TruthfulQA Gen | BA | 43.57 1.74 | |
| TruthfulQA Gen | BD | -40.98 33.19 | |
| TruthfulQA MC1 | A | 39.53 1.71 | |
| TruthfulQA MC2 | A | 54.56 1.58 | |
| Q3_K_L | GSM8K (FE) | EM | 74.07 1.21 |
| GSM8K (SM) | EM | 10.54 0.85 | |
| HellaSwag | A | 57.28 0.49 | |
| HellaSwag | AN | 73.54 0.44 | |
| IFEval | ILL | 84.41 | |
| IFEval | ILS | 80.94 | |
| IFEval | PLL | 77.82 1.79 | |
| IFEval | PLS | 73.38 1.90 | |
| MMLU | A | 62.31 0.39 | |
| MMLU Humanities | A | 58.75 0.69 | |
| MMLU Other | A | 69.68 0.80 | |
| MMLU Social Sciences | A | 71.08 0.80 | |
| MMLU Stem | A | 51.79 0.85 | |
| TruthfulQA Gen | BA | 41.74 1.73 | |
| TruthfulQA Gen | BD | -36.16 27.06 | |
| TruthfulQA MC1 | A | 39.05 1.71 | |
| TruthfulQA MC2 | A | 54.84 1.58 | |
| Q4_0 | GSM8K (FE) | EM | 75.66 1.18 |
| GSM8K (SM) | EM | 18.95 1.08 | |
| HellaSwag | A | 56.76 0.49 | |
| HellaSwag | AN | 71.88 0.45 | |
| IFEval | ILL | 83.09 | |
| IFEval | ILS | 79.98 | |
| IFEval | PLL | 75.42 1.85 | |
| IFEval | PLS | 71.35 1.95 | |
| MMLU | A | 62.20 0.39 | |
| MMLU Humanities | A | 57.56 0.69 | |
| MMLU Other | A | 69.91 0.80 | |
| MMLU Social Sciences | A | 72.93 0.78 | |
| MMLU Stem | A | 51.06 0.85 | |
| TruthfulQA Gen | BA | 52.88 1.75 | |
| TruthfulQA Gen | BD | 30.93 26.02 | |
| TruthfulQA MC1 | A | 38.31 1.70 | |
| TruthfulQA MC2 | A | 52.68 1.60 | |
| Q4_1 | GSM8K (FE) | EM | 76.04 1.18 |
| GSM8K (SM) | EM | 23.58 1.17 | |
| HellaSwag | A | 56.28 0.50 | |
| HellaSwag | AN | 71.29 0.45 | |
| IFEval | ILL | 84.05 | |
| IFEval | ILS | 80.22 | |
| IFEval | PLL | 77.26 1.80 | |
| IFEval | PLS | 72.27 1.93 | |
| MMLU | A | 63.17 0.39 | |
| MMLU Humanities | A | 58.94 0.69 | |
| MMLU Other | A | 70.68 0.79 | |
| MMLU Social Sciences | A | 72.93 0.78 | |
| MMLU Stem | A | 52.55 0.85 | |
| TruthfulQA Gen | BA | 44.80 1.74 | |
| TruthfulQA Gen | BD | -33.30 31.46 | |
| TruthfulQA MC1 | A | 38.56 1.70 | |
| TruthfulQA MC2 | A | 55.01 1.61 | |
| Q4_K_S | GSM8K (FE) | EM | 77.33 1.15 |
| GSM8K (SM) | EM | 17.29 1.04 | |
| HellaSwag | A | 57.56 0.49 | |
| HellaSwag | AN | 72.79 0.44 | |
| IFEval | ILL | 85.01 | |
| IFEval | ILS | 81.89 | |
| IFEval | PLL | 79.11 1.75 | |
| IFEval | PLS | 75.05 1.86 | |
| MMLU | A | 62.06 0.39 | |
| MMLU Humanities | A | 58.17 0.69 | |
| MMLU Other | A | 69.58 0.80 | |
| MMLU Social Sciences | A | 71.60 0.79 | |
| MMLU Stem | A | 51.13 0.85 | |
| TruthfulQA Gen | BA | 51.77 1.75 | |
| TruthfulQA Gen | BD | 12.04 25.97 | |
| TruthfulQA MC1 | A | 37.45 1.69 | |
| TruthfulQA MC2 | A | 53.40 1.59 | |
| Q4_K_M | GSM8K (FE) | EM | 77.41 1.15 |
| GSM8K (SM) | EM | 14.48 0.97 | |
| HellaSwag | A | 57.26 0.49 | |
| HellaSwag | AN | 72.35 0.45 | |
| IFEval | ILL | 84.05 | |
| IFEval | ILS | 80.82 | |
| IFEval | PLL | 77.63 1.79 | |
| IFEval | PLS | 73.75 1.89 | |
| MMLU | A | 62.43 0.39 | |
| MMLU Humanities | A | 58.98 0.69 | |
| MMLU Other | A | 69.49 0.80 | |
| MMLU Social Sciences | A | 72.41 0.79 | |
| MMLU Stem | A | 50.87 0.85 | |
| TruthfulQA Gen | BA | 47.12 1.75 | |
| TruthfulQA Gen | BD | -17.69 27.79 | |
| TruthfulQA MC1 | A | 37.45 1.69 | |
| TruthfulQA MC2 | A | 54.49 1.60 | |
| Q5_0 | GSM8K (FE) | EM | 79.08 1.12 |
| GSM8K (SM) | EM | 37.68 1.33 | |
| HellaSwag | A | 57.41 0.49 | |
| HellaSwag | AN | 72.63 0.44 | |
| IFEval | ILL | 85.01 | |
| IFEval | ILS | 82.13 | |
| IFEval | PLL | 78.56 1.77 | |
| IFEval | PLS | 74.86 1.87 | |
| MMLU | A | 63.18 0.38 | |
| MMLU Humanities | A | 58.87 0.69 | |
| MMLU Other | A | 71.55 0.78 | |
| MMLU Social Sciences | A | 73.87 0.77 | |
| MMLU Stem | A | 50.94 0.84 | |
| TruthfulQA Gen | BA | 49.08 1.75 | |
| TruthfulQA Gen | BD | 3.46 32.99 | |
| TruthfulQA MC1 | A | 39.17 1.71 | |
| TruthfulQA MC2 | A | 54.57 1.60 | |
| Q5_1 | GSM8K (FE) | EM | 78.47 1.13 |
| GSM8K (SM) | EM | 20.62 1.11 | |
| HellaSwag | A | 56.91 0.49 | |
| HellaSwag | AN | 72.08 0.45 | |
| IFEval | ILL | 84.53 | |
| IFEval | ILS | 81.77 | |
| IFEval | PLL | 78.19 1.78 | |
| IFEval | PLS | 74.68 1.87 | |
| MMLU | A | 63.68 0.38 | |
| MMLU Humanities | A | 59.36 0.69 | |
| MMLU Other | A | 71.58 0.79 | |
| MMLU Social Sciences | A | 74.39 0.77 | |
| MMLU Stem | A | 51.89 0.84 | |
| TruthfulQA Gen | BA | 45.78 1.74 | |
| TruthfulQA Gen | BD | -32.95 31.31 | |
| TruthfulQA MC1 | A | 39.53 1.71 | |
| TruthfulQA MC2 | A | 54.62 1.59 | |
| Q5_K_S | GSM8K (FE) | EM | 75.66 1.18 |
| GSM8K (SM) | EM | 17.13 1.04 | |
| HellaSwag | A | 57.19 0.49 | |
| HellaSwag | AN | 72.67 0.44 | |
| IFEval | ILL | 84.53 | |
| IFEval | ILS | 81.53 | |
| IFEval | PLL | 77.82 1.79 | |
| IFEval | PLS | 74.12 1.88 | |
| MMLU | A | 63.36 0.38 | |
| MMLU Humanities | A | 59.34 0.69 | |
| MMLU Other | A | 71.81 0.78 | |
| MMLU Social Sciences | A | 73.77 0.77 | |
| MMLU Stem | A | 50.87 0.84 | |
| TruthfulQA Gen | BA | 45.65 1.74 | |
| TruthfulQA Gen | BD | -13.25 23.12 | |
| TruthfulQA MC1 | A | 38.92 1.71 | |
| TruthfulQA MC2 | A | 53.90 1.59 | |
| Q5_K_M | GSM8K (FE) | EM | 78.54 1.13 |
| GSM8K (SM) | EM | 19.41 1.09 | |
| HellaSwag | A | 57.16 0.49 | |
| HellaSwag | AN | 72.33 0.45 | |
| IFEval | ILL | 83.69 | |
| IFEval | ILS | 80.70 | |
| IFEval | PLL | 76.89 1.81 | |
| IFEval | PLS | 73.38 1.90 | |
| MMLU | A | 62.80 0.39 | |
| MMLU Humanities | A | 58.85 0.69 | |
| MMLU Other | A | 71.39 0.79 | |
| MMLU Social Sciences | A | 73.68 0.78 | |
| MMLU Stem | A | 49.64 0.84 | |
| TruthfulQA Gen | BA | 43.82 1.74 | |
| TruthfulQA Gen | BD | 2.38 22.63 | |
| TruthfulQA MC1 | A | 38.56 1.70 | |
| TruthfulQA MC2 | A | 54.45 1.59 | |
| Q6_K | GSM8K (FE) | EM | 78.17 1.14 |
| GSM8K (SM) | EM | 20.17 1.11 | |
| HellaSwag | A | 57.37 0.49 | |
| HellaSwag | AN | 72.48 0.45 | |
| IFEval | ILL | 82.85 | |
| IFEval | ILS | 79.98 | |
| IFEval | PLL | 75.60 1.85 | |
| IFEval | PLS | 72.09 1.93 | |
| MMLU | A | 63.17 0.38 | |
| MMLU Humanities | A | 59.09 0.69 | |
| MMLU Other | A | 71.29 0.79 | |
| MMLU Social Sciences | A | 74.26 0.77 | |
| MMLU Stem | A | 50.46 0.85 | |
| TruthfulQA Gen | BA | 47.86 1.75 | |
| TruthfulQA Gen | BD | -4.51 25.13 | |
| TruthfulQA MC1 | A | 39.41 1.71 | |
| TruthfulQA MC2 | A | 54.71 1.59 | |
| Q8_0 | GSM8K (FE) | EM | 77.48 1.15 |
| GSM8K (SM) | EM | 23.50 1.17 | |
| HellaSwag | A | 57.42 0.49 | |
| HellaSwag | AN | 72.52 0.45 | |
| IFEval | ILL | 83.81 | |
| IFEval | ILS | 80.70 | |
| IFEval | PLL | 77.45 1.80 | |
| IFEval | PLS | 73.20 1.91 | |
| MMLU | A | 63.43 0.38 | |
| MMLU Humanities | A | 59.13 0.68 | |
| MMLU Other | A | 71.90 0.78 | |
| MMLU Social Sciences | A | 74.59 0.76 | |
| MMLU Stem | A | 50.62 0.84 | |
| TruthfulQA Gen | BA | 46.02 1.74 | |
| TruthfulQA Gen | BD | -16.41 25.01 | |
| TruthfulQA MC1 | A | 39.41 1.71 | |
| TruthfulQA MC2 | A | 54.81 1.60 |