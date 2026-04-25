# Inference Optimization

## Video (best)
- **Andrej Karpathy** — "State of GPT"
- youtube_id: jkrNMKz9pWU
- Why: Clear, systems-aware overview of how inference works in practice (latency/throughput constraints, KV cache, batching, serving considerations) from an LLM practitioner perspective.
- Level: Intermediate

## Blog / Written explainer (best)
- **Hugging Face (Blog)** — "Speculative Decoding"
- Why: Practical, readable explanation of speculative decoding with intuition, algorithm sketch, and why it improves throughput without changing model quality.
- Level: Intermediate
- url: https://huggingface.co/docs/transformers/assisted_decoding

## Deep dive
- **vLLM (Project Docs)** — "PagedAttention and vLLM"
- Why: Primary reference for paged attention and KV-cache memory management in a modern high-throughput serving engine; directly relevant to continuous batching and KV cache optimization.
- Level: Advanced
- url: https://docs.vllm.ai/ [VERIFY] (navigate to PagedAttention / architecture sections)

## Original paper
- **Kwon et al.** — "Efficient Memory Management for Large Language Model Serving with PagedAttention"
- Why: Foundational paper behind vLLM’s paged attention approach; key for understanding KV cache optimization and high-throughput serving.
- Level: Advanced
- url: https://arxiv.org/abs/2309.06180

## Code walkthrough
- **vLLM (GitHub)** — "vLLM: a high-throughput and memory-efficient inference and serving engine for LLMs"
- Why: Best “read-the-source” entry point for continuous batching, KV cache management, and paged attention in a production-grade serving system.
- Level: Advanced
- url: https://github.com/vllm-project/vllm

## Coverage notes
- Strong: vLLM + paged attention; KV cache optimization concepts; speculative decoding overview.
- Weak: Quantization methods (GPTQ/AWQ/GGUF) consolidated “best” explainer; TensorRT-LLM and Triton Inference Server deep, beginner-friendly walkthroughs.
- Gap: Medusa decoding (and other multi-token decoding variants) and a single, high-quality comparative guide across GPTQ vs AWQ vs GGUF with inference tradeoffs.

## Last Verified
2026-04-09