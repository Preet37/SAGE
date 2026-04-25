# Source: https://apxml.com/courses/introduction-to-transformer-models/chapter-2-self-attention-multi-head-attention/query-key-value-vectors
# Author: APXML
# Author Slug: apxml
# Title: Query, Key, and Value Vectors in Self-Attention
# Fetched via: trafilatura
# Date: 2026-04-07

Self-attention aims for each word in an input sequence to determine the relevance of every other word (including itself) within that specific context. To achieve this comparison and subsequent information weighting, each input word's embedding is transformed into three distinct representations: the Query, Key, and Value vectors.
For example, take an input sequence like "thinking machine". Each word is initially represented by an embedding vector. Let's denote the embedding for "thinking" as and for "machine" as . These vectors hold the initial, context-independent meaning of the words.
For the self-attention calculation, we don't directly compare these embeddings. Instead, we project each embedding into three separate vector spaces using three unique weight matrices learned during training. These are commonly denoted as , , and .
Specifically, for every input embedding in the sequence, we compute:
- A Query vector:
- A main vector:
- A Value vector:
This process generates a unique set of query, and value vectors for each word in the input sequence. These derived vectors typically have a dimension ( for keys and queries, for values) that might be smaller than the original embedding dimension (). The requirement is that the dimensions of Query and Key vectors () must be identical to allow for their comparison via dot products.
We can visualize this transformation for a single input token:
Derivation of Query (q), (k), and Value (v) vectors from a single input embedding (xᵢ) using learned weight matrices (W^Q, W^K, W^V).
To understand the roles of these vectors, imagine searching a database:
- Query (Q): Represents the current word's perspective, asking "What information is relevant to me?". For a specific word , its query vector is used to probe all other words.
- Key (K): Represents the 'label' or identifier for the information a word carries. Each word has a key vector . The query is compared against all keys to calculate an attention score, indicating how relevant word is to word .
- Value (V): Represents the actual content or meaning of a word. Each word also has a value vector . Once the attention score between and is computed, it's used to weight the corresponding value vector .
Essentially, the interaction between a Query vector and a Key vector determines the strength of connection or attention weight from word to word . The Value vector provides the information that gets passed from word back to word , scaled by this attention weight.
An important aspect is that the weight matrices , , and are parameters learned during the model training process. Initially random, they are adjusted through backpropagation so the model learns the most effective way to project input embeddings into these Q, K, and V spaces for the task at hand (e.g., machine translation, text summarization). This learning process allows the model to understand complex relationships and dependencies within the input sequence.
Having generated these Query, Key, and Value vectors for every word, we are now equipped to calculate the actual attention scores. The next section details how the Scaled Dot-Product Attention mechanism utilizes these vectors to compute the precise attention weights that define how information flows between words in the sequence.
Was this section helpful?
[Attention Is All You Need](https://proceedings.neurips.cc/paper_files/paper/2017/file/3f5ee243547dee91fbd053c1c4a845aa-Paper.pdf), Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, Illia Polosukhin, 2017 Advances in Neural Information Processing Systems 30 (NIPS 2017)[DOI: 10.55919/nips.2017.00078](https://doi.org/10.55919/nips.2017.00078)- The foundational paper introducing the Transformer architecture and the self-attention mechanism, defining the Query, Key, and Value concepts.[CS224N: Natural Language Processing with Deep Learning - Lecture 10: Transformers and Pretraining](https://web.stanford.edu/class/cs224n/materials/cs224n-2023-lecture10-transformers.pdf), Danqi Chen, John Hewitt, Christopher Manning, 2023 (Stanford University) - Provides an in-depth educational explanation of self-attention and the roles of Query, Key, and Value vectors within the Transformer model.[Natural Language Processing with Transformers](https://www.oreilly.com/library/view/natural-language-processing/9781098132439/), Lewis Tunstall, Leandro von Werra, Thomas Wolf, 2022 (O'Reilly Media) - A practical guide explaining the QKV mechanism as part of Transformer models and their applications in natural language processing.
© 2026 ApX Machine Learning[AI Ethics & Transparency](/transparency)[•](/sustainability)