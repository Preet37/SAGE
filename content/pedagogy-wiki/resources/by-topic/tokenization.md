# Tokenization

## Video (best)
- **Andrej Karpathy** — "Let's build the GPT Tokenizer"
- youtube_id: zduSFxRajkE
- Why: Karpathy builds a BPE tokenizer from scratch, covering byte-level encoding, vocabulary construction, special tokens, and the quirks that cause LLM failures. It's the most thorough hands-on treatment of tokenization available on YouTube — 2+ hours of dense, practical content that bridges theory and implementation seamlessly. Already validated in the existing curation.
- Level: intermediate

## Blog / Written explainer (best)
- **Hugging Face / NLP Course** — "Tokenizers (Chapter 6: Building a Tokenizer, Block by Block)"
- url: https://huggingface.co/learn/nlp-course/chapter6/1
- Why: The HF NLP course chapter on tokenizers is the most pedagogically complete written resource: it covers BPE, WordPiece, Unigram, and SentencePiece with clear diagrams, worked examples, and runnable code. It directly addresses subword tokens, vocabulary size trade-offs, and special tokens — all the related concepts listed for this topic.
- Level: beginner–intermediate

## Deep dive
- **Lilian Weng** — "Reducing the Cost of LLM Training: Tokenization and Vocabulary"
- url: https://lilianweng.github.io/posts/2023-01-27-the-transformer-family-v2/ [VERIFY — this is the Transformer Family v2 post, not a tokenization deep-dive; a dedicated tokenization post URL needs identification]
- Why: Weng's writing is the gold standard for comprehensive technical surveys. Her posts synthesize original papers, implementation details, and empirical findings in one place.
- Level: advanced

> ⚠️ **Note:** I am not fully confident in the exact URL above. A more reliably verifiable deep-dive alternative is:
- **HuggingFace Tokenizers documentation / conceptual guide**
- url: https://huggingface.co/docs/tokenizers/conceptual/algorithm
- Why: Covers BPE, Unigram, and WordPiece algorithms with pseudocode and complexity analysis. Authoritative, maintained, and technically precise.
- Level: intermediate–advanced

## Original paper
- **Sennrich et al. (2016)** — "Neural Machine Translation of Rare Words with Subword Units" (the BPE tokenization paper)
- url: https://arxiv.org/abs/1508.07909
- Why: This is the seminal paper that introduced Byte Pair Encoding to NLP tokenization. It is short (~9 pages), clearly written, and directly motivated the subword tokenization approach used in virtually every modern LLM. The most important single paper for this topic.
- Level: intermediate

## Code walkthrough
- **Andrej Karpathy** — "Let's build the GPT Tokenizer" (same video, but the accompanying repo is the code walkthrough)
- url: https://github.com/karpathy/minbpe
- Why: The `minbpe` repository implements a minimal, readable BPE tokenizer in ~200 lines of Python. It is the clearest available code reference for understanding how tokenization actually works, with tests and a training script. Directly accompanies the video above, making it ideal for paired study.
- Level: intermediate

## Coverage notes
- **Strong:** BPE algorithm, subword tokens, vocabulary size trade-offs, special tokens, GPT-style tokenization — all excellently covered by Karpathy's video + minbpe + HF NLP course.
- **Weak:** Speech tokenization (EnCodec, Residual Vector Quantization) — the resources above focus on text tokenization. The multimodal/audio tokenization angle is underserved by the curated resources.
- **Gap:** No single excellent YouTube video exists specifically for **speech tokenization / EnCodec / RVQ** as used in audio LLMs (e.g., AudioLM, MusicGen). The intro-to-multimodal course will need a dedicated resource for this sub-topic. The EnCodec paper itself (arxiv.org/abs/2210.13438) is the best available reference, but no strong pedagogical explainer video has been identified.

## Cross-validation
This topic appears in 2 courses: **intro-to-llms** (text tokenization focus: BPE, vocabulary, special tokens) and **intro-to-multimodal** (speech tokenization focus: EnCodec, RVQ). The existing curated videos (all `zduSFxRajkE`, duplicated 5×) cover the LLM side well but leave the multimodal/speech side without a dedicated resource. Deduplication of the five identical entries is recommended.

## Last Verified
2025-04-06