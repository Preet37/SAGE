## Core Definitions

**Tokenization**  
Tokenization is the preprocessing step that converts raw text into a sequence of discrete **tokens** (often subword units) that can be mapped to integer IDs in a fixed **vocabulary**; models operate on these IDs (e.g., via an embedding lookup) rather than on raw strings. Hugging Face describes a tokenizer as the component that “breaks down raw text into smaller units called tokens” and outputs numerical representations such as `input_ids` (token IDs) and `attention_mask` (masking for padding) for model consumption (Hugging Face Tokenizers conceptual guide: https://huggingface.co/docs/tokenizers/conceptual/algorithm; HF Transformers example output shown in the same guide).

**Byte Pair Encoding (BPE)**  
BPE is a subword tokenization algorithm that starts from a base alphabet and **iteratively merges the most frequent adjacent pair** of symbols to form new symbols until reaching a target vocabulary size. The arXiv comparison card summarizes BPE as: “start with all symbols; iteratively merge most frequent pair until target vocab size” (https://arxiv.org/html/2411.17669v1). Karpathy’s `minbpe` implements a **byte-level** BPE variant that runs on UTF-8 bytes, always allocating the 256 single-byte tokens first and then learning merges on top (https://github.com/karpathy/minbpe).

**Subword tokens**  
Subword tokens are token units smaller than full words but larger than characters/bytes, learned so that frequent character sequences become single tokens while rare words can be represented as sequences of smaller units. Sennrich et al. motivate subword units as a way to handle open-vocabulary translation by encoding rare/unknown words as sequences of subword units (https://arxiv.org/abs/1508.07909).

**Vocabulary size**  
Vocabulary size is the number of distinct tokens a tokenizer can emit (including any reserved/special tokens). In the tokenizer comparison benchmark, vocab sizes are explicitly varied (e.g., 400, 800, 1600, 3200, 6400) to measure effects on overlap, efficiency (“fertility”), contextual specialization, and boundary alignment (https://arxiv.org/html/2411.17669v1).

**Special tokens**  
Special tokens are reserved tokens with predefined roles (e.g., sequence boundaries, padding, unknown, etc.) that are handled explicitly by the tokenizer/model pipeline. Karpathy’s `minbpe` notes that the GPT-2/GPT-4-style regex tokenizer “handles special tokens, if any” as part of the tokenization system (https://github.com/karpathy/minbpe). (The exact inventory/semantics of special tokens is model-specific; the key tutor point is that they are reserved IDs with non-linguistic control meaning.)

---

## Key Formulas & Empirical Results

### Heaps’ Law (vocabulary growth vs token count)
From the tokenizer comparison benchmark (Eq. 1):  
\[
V(N) = K \, N^{\beta}
\]  
- \(V\): estimated vocabulary size  
- \(N\): total token count  
- \(K\): typically **10–100**  
- \(\beta\): typically **0.4–0.6**  
**Claim supported:** Across tokenizers, vocabulary growth follows Heaps’ Law closely; SentencePiece saturates slightly faster (https://arxiv.org/html/2411.17669v1).

### Shared-token overlap vs vocabulary size (BPE vs WordPiece vs SentencePiece/Unigram)
From the same benchmark (Section IV-A):  
- At vocab **400**:  
  - BPE–WordPiece overlap **0.98**  
  - BPE–SentencePiece **0.83**  
  - WordPiece–SentencePiece **0.84**  
- At vocab **6400**:  
  - BPE–WordPiece **0.72**  
  - SentencePiece overlap with each **0.47**  
**Claim supported:** Tokenizer vocabularies diverge more as vocab size increases; SentencePiece differs most at large vocab (https://arxiv.org/html/2411.17669v1).

### Efficiency metric: fertility (#tokens per sequence)
Benchmark definition (Section IV-B): **Fertility = number of tokens needed to encode a sequence.**  
Reported trends (protein benchmark):  
- In training vocab: BPE learns **longest average tokens**, then WordPiece; SentencePiece shortest.  
- In test data: trend reverses: **BPE shortest**, WordPiece next, **SentencePiece longest**.  
- Fertility ordering reported: **BPE higher fertility**, SentencePiece lower, WordPiece in-between (https://arxiv.org/html/2411.17669v1).  
**Tutor note:** Students often conflate “average token length” with “fertility”; this benchmark reports both and shows they can behave differently between training vocab and test encodings.

### Contextual exponence (contextual specialization proxy)
Metric (Section IV-C): **# unique neighbors per token** in test data.  
Result: for vocab **800–3200**, beyond ~first **100 tokens**, **BPE has lower distinct-neighbor counts** → more contextually consistent/specialized tokens; at vocab **6400**, SentencePiece plot flattens; WordPiece becomes more BPE-like after ~**300 tokens** (https://arxiv.org/html/2411.17669v1).

### Domain boundary alignment (token boundaries vs annotated domains)
Setup (Section IV-D): PROSITE domains: **4,646 domains** in **3,377** test sequences.  
A domain is a “hit” if **domain start aligns with token start AND domain end aligns with token end**.  
Result: **BPE best**, but performance **declines as vocab increases** (longer tokens); boundary alignment correlates with **shorter token lengths**; overall accuracy “relatively low” even at small vocabs (https://arxiv.org/html/2411.17669v1).  
**Claim supported:** Tokenization choices can destroy meaningful boundaries in non-NLP sequences; larger vocab can worsen boundary alignment.

### Concrete BPE toy example (Wikipedia string) as implemented in `minbpe`
Karpathy’s example: train on `"aaabdaaabac"` with base 256 byte tokens + **3 merges**:  
- `tokenizer.train(text, 256 + 3)`  
- `tokenizer.encode(text)` → `[258, 100, 258, 97, 99]`  
- `tokenizer.decode([258, 100, 258, 97, 99])` → original string  
Also notes: bytes for `a,b,c,d` are 97,98,99,100 (ASCII) (https://github.com/karpathy/minbpe).  
**Claim supported:** BPE creates new token IDs beyond the base byte IDs; encoding/decoding is exact.

---

## How It Works

### A. Byte-level BPE training (mechanics)
Grounded in the BPE description from the benchmark (merge most frequent pair) and the byte-level implementation notes from `minbpe`.

1. **Convert text to a base symbol sequence**  
   - Byte-level BPE: UTF-8 encode the string into bytes; initial symbols are byte values 0–255 (Karpathy `minbpe`).

2. **Initialize vocabulary**  
   - Start with all base symbols (bytes).  
   - Set a target vocab size \(V_{\text{target}}\). In `minbpe`, this is `256 + num_merges`.

3. **Count adjacent pairs**  
   - Over the training corpus represented as sequences of symbols, count frequency of each adjacent pair `(s_i, s_{i+1})`.

4. **Merge the most frequent pair**  
   - Create a new symbol representing the concatenation of that pair.  
   - Replace all occurrences of that pair in the corpus with the new symbol.

5. **Repeat until target vocab size reached**  
   - Each merge adds one new token to the vocabulary.  
   - Stop when you have performed enough merges to reach \(V_{\text{target}}\).

6. **Save merges + vocab**  
   - The tokenizer is defined by the base symbols plus the ordered list of merges (Karpathy `minbpe` provides save/load utilities).

### B. Encoding (tokenizing new text) with a trained BPE tokenizer
1. **Convert input text to bytes** (byte-level BPE).  
2. **Apply merges in learned order**  
   - Greedily apply the merge rules so that any pair that matches a learned merge can be combined, respecting the merge priority order (as implemented in BPE tokenizers; `minbpe` provides `encode`).
3. **Output token IDs**  
   - Each resulting symbol corresponds to a token ID in the vocabulary.

### C. Decoding (detokenizing)
1. **Map token IDs back to byte sequences** (each token corresponds to a byte string).  
2. **Concatenate bytes** and UTF-8 decode back to text (`minbpe` demonstrates exact round-trip decode).

### D. Where special tokens fit (implementation-level view)
- Special tokens are typically **reserved IDs** that the tokenizer recognizes and inserts/keeps intact (Karpathy notes special-token handling in the regex tokenizer variant).  
- In many pipelines (HF), tokenization outputs `input_ids` plus masks like `attention_mask` for padding control (HF conceptual guide).

---

## Teaching Approaches

### Intuitive (no math)
- Tokenization is a **compression-like** step: it tries to represent text using a set of reusable pieces.  
- If a chunk appears often (like “ing” or “http”), it becomes a single token; rare words become sequences of smaller pieces.  
- BPE learns these pieces by repeatedly “gluing together” the most common adjacent pair it sees.

### Technical (with math/metrics)
- BPE training is an iterative optimization over symbol sequences: at each step choose the adjacent pair with maximum empirical frequency and add it to the vocabulary (benchmark definition: “merge most frequent pair”).  
- Tokenizer quality/behavior can be measured by:
  - **Fertility**: number of tokens needed to encode a sequence (efficiency proxy).  
  - **Contextual exponence**: unique neighbor count per token (specialization proxy).  
  - **Boundary alignment**: whether token boundaries match annotated boundaries (structure preservation).  
- Vocabulary growth follows **Heaps’ Law** \(V(N)=K N^\beta\) with typical \(K\in[10,100]\), \(\beta\in[0.4,0.6]\) (benchmark).

### Analogy-based
- Think of tokens as **LEGO bricks**:
  - A small vocabulary is like having only tiny bricks: you can build anything, but it takes many bricks (high fertility).  
  - A large vocabulary is like having many specialized bricks: you can build common structures quickly, but you may get awkward mismatches at boundaries (e.g., a brick spans across where you “wanted” a seam), and the set of bricks differs more across tokenizers as vocab grows (overlap drops in the benchmark).

---

## Common Misconceptions

1. **“Tokens are the same as words.”**  
   - **Why wrong:** Modern LLM tokenizers typically use **subword** units; a “word” may be split into multiple tokens, and a token may be only part of a word. Sennrich et al. explicitly motivate subword units to handle rare/unknown words by splitting them (https://arxiv.org/abs/1508.07909).  
   - **Correct model:** Tokens are learned text pieces (often subwords) chosen to balance reuse and coverage.

2. **“BPE understands meaning; it merges semantically related pieces.”**  
   - **Why wrong:** BPE merges are driven by **frequency of adjacent pairs**, not semantics (benchmark definition; Karpathy’s implementation).  
   - **Correct model:** BPE is a data-driven string segmentation method; any semantic usefulness is indirect (frequent patterns often correlate with morphemes, but not guaranteed).

3. **“A bigger vocabulary always makes tokenization more efficient.”**  
   - **Why wrong:** The benchmark shows trade-offs: boundary alignment can **decline as vocab increases** because tokens get longer and span across meaningful boundaries (protein domain alignment result) (https://arxiv.org/html/2411.17669v1).  
   - **Correct model:** Larger vocab can reduce token count for frequent patterns, but can worsen boundary preservation and change generalization behavior.

4. **“All subword tokenizers converge to basically the same vocabulary.”**  
   - **Why wrong:** Overlap drops substantially at larger vocab sizes: e.g., BPE–WordPiece overlap falls from **0.98 (v=400)** to **0.72 (v=6400)**; SentencePiece overlap with each falls to **0.47** at **6400** (https://arxiv.org/html/2411.17669v1).  
   - **Correct model:** Different training objectives (frequency merges vs likelihood-based merges vs unigram pruning) yield increasingly different vocabularies as capacity grows.

5. **“If I can decode tokens back to text, tokenization can’t cause model ‘foot-guns’.”**  
   - **Why wrong:** Even with perfect invertibility (byte-level BPE round-trips exactly in `minbpe`), segmentation choices affect sequence length (fertility), boundary alignment, and contextual specialization—changing what the model can represent efficiently and what patterns it learns (benchmark metrics; Karpathy’s warning that many LLM oddities trace back to tokenization in the referenced video transcript).  
   - **Correct model:** Tokenization is lossless at the string level (often), but not neutral for modeling.

---

## Worked Examples

### 1) Minimal byte-level BPE with `minbpe` (exact, runnable)
From Karpathy’s repository example (https://github.com/karpathy/minbpe):

```python
from minbpe import BasicTokenizer

tokenizer = BasicTokenizer()
text = "aaabdaaabac"

# 256 base byte tokens + 3 merges
tokenizer.train(text, 256 + 3)

ids = tokenizer.encode(text)
print(ids)  # [258, 100, 258, 97, 99]

roundtrip = tokenizer.decode(ids)
print(roundtrip)  # "aaabdaaabac"
```

**Tutor prompts while stepping through:**
- Ask what the base vocabulary is (answer: 256 bytes).  
- Ask why token IDs exceed 255 (answer: merges create new tokens, e.g., 258).  
- Ask what `100` corresponds to (answer: byte for `'d'` per ASCII note in repo).

### 2) Inspecting tokenization outputs in Hugging Face (IDs + attention mask)
Hugging Face conceptual guide shows that calling a tokenizer returns `input_ids` and `attention_mask` (https://huggingface.co/docs/tokenizers/conceptual/algorithm). A typical pattern:

```python
from transformers import AutoTokenizer

tok = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
res = tok("I love you! I love you! I love you!")
print(res["input_ids"])
print(res["attention_mask"])
```

**What to emphasize (sourced):**
- `input_ids` are token IDs; `attention_mask` indicates which positions are real tokens vs padding (HF guide).

---

## Comparisons & Trade-offs

### Subword tokenizer families (as defined in the benchmark)
| Tokenizer | Training rule (per source) | Notable behavioral notes from benchmark | When to choose (tutoring guidance grounded in metrics) |
|---|---|---|---|
| **BPE** | Iteratively **merge most frequent pair** until target vocab (https://arxiv.org/html/2411.17669v1) | In test data: **shortest avg tokens** (trend reversal noted); **higher fertility** than SentencePiece; more contextually consistent tokens (lower distinct-neighbor counts) for vocab 800–3200; **best boundary alignment** in protein domains but declines with larger vocab | Choose when you want a simple, widely used merge-based tokenizer; highlight specialization metric and boundary alignment result when discussing structure sensitivity |
| **WordPiece** | Like BPE but merges based on **likelihood improvement** after adding token (https://arxiv.org/html/2411.17669v1) | Often intermediate between BPE and SentencePiece on fertility; becomes more BPE-like at large vocab after ~300 tokens in contextual exponence plots | Choose when discussing likelihood-driven merges; useful contrast vs frequency-only BPE |
| **SentencePiece (Unigram LM)** | Treats input as raw stream; start large and **iteratively discard tokens** to reach target vocab (https://arxiv.org/html/2411.17669v1) | Shortest avg tokens in training vocab but longest in test data (trend reversal noted); overlap with others drops to **0.47** at vocab 6400; Heaps’ Law saturation slightly faster | Choose when you want a pruning/unigram perspective and to discuss why vocabularies diverge at scale |

**Additional trade-off axis: vocabulary size**
- Increasing vocab size tends to reduce overlap between tokenizers (numbers above) and can worsen boundary alignment due to longer tokens (protein domain result) (https://arxiv.org/html/2411.17669v1).

---

## Prerequisite Connections

- **Discrete vocabulary + embedding lookup**: Students need the idea that token IDs index rows of an embedding table (Karpathy transcript describes mapping integers to embedding vectors in a GPT-from-scratch context).  
- **UTF-8 / bytes**: Byte-level BPE operates on UTF-8 bytes; understanding “bytes as base symbols” clarifies why tokenization is invertible and language-agnostic (Karpathy `minbpe`).  
- **Frequency counts / greedy iteration**: BPE training is repeated counting + merging of most frequent pairs (benchmark definition; `minbpe` implementation).  
- **Train vs test distribution shift**: Benchmark reports different token-length trends in training vocab vs test data; students should be ready to reason about distribution shift (https://arxiv.org/html/2411.17669v1).

---

## Socratic Question Bank

1. **If a tokenizer is byte-level BPE, what is the smallest possible vocabulary before any merges—and why?**  
   *Good answer:* 256 tokens for all possible byte values; merges add tokens beyond that (Karpathy `minbpe`).

2. **What exactly determines the next merge in BPE training? What information does it *not* use?**  
   *Good answer:* Most frequent adjacent pair; it does not use semantics or model loss directly (benchmark BPE definition).

3. **How could two tokenizers trained on the same data end up with very different vocabularies at large vocab sizes?**  
   *Good answer:* Different objectives/algorithms; benchmark shows overlap dropping (e.g., SentencePiece overlap 0.47 at 6400).

4. **What does “fertility” measure, and why might it matter for an LLM?**  
   *Good answer:* #tokens to encode a sequence; affects sequence length/compute and what fits in context (benchmark definition).

5. **Why might increasing vocabulary size reduce boundary alignment with meaningful units (like protein domains)?**  
   *Good answer:* Longer tokens span across boundaries; benchmark reports alignment declines as vocab increases.

6. **If decoding perfectly reconstructs the original text, can tokenization still change model behavior? Give one metric-based reason.**  
   *Good answer:* Yes—fertility, contextual exponence, boundary alignment change; benchmark provides these metrics.

7. **Heaps’ Law says \(V(N)=K N^\beta\). If \(\beta\) is between 0.4 and 0.6, what does that imply about how fast vocabulary grows with more data?**  
   *Good answer:* Sublinear growth; doubling tokens increases vocab by less than 2× (benchmark provides typical \(\beta\)).

8. **In the benchmark, why is it interesting that average token length trends reverse between training vocab and test data?**  
   *Good answer:* It shows learned token inventory properties don’t directly predict encoding behavior on new data; distribution shift matters (benchmark IV-B).

---

## Likely Student Questions

**Q: What’s the exact rule BPE uses to build the vocabulary?**  
→ **A:** BPE starts with base symbols and repeatedly **merges the most frequent adjacent pair** until reaching the target vocabulary size (https://arxiv.org/html/2411.17669v1). Karpathy’s byte-level BPE starts from the **256 UTF-8 byte tokens** and then learns merges (https://github.com/karpathy/minbpe).

**Q: How is WordPiece different from BPE?**  
→ **A:** In the benchmark summary, **WordPiece** is “like BPE but merges based on **likelihood improvement** of the training data after adding the token,” whereas **BPE** merges the **most frequent pair** (https://arxiv.org/html/2411.17669v1).

**Q: What is SentencePiece/Unigram doing differently?**  
→ **A:** The benchmark describes SentencePiece (Unigram LM) as treating input as a **raw stream** (space is a character) and using a Unigram approach: start with a large set of tokens and **iteratively discard tokens** until reaching the target vocab size (https://arxiv.org/html/2411.17669v1).

**Q: What does “fertility” mean in tokenizer evaluation?**  
→ **A:** Fertility is defined as the **number of tokens needed to encode a sequence** (https://arxiv.org/html/2411.17669v1, Section IV-B).

**Q: Do different tokenizers actually learn the same tokens if trained on the same corpus?**  
→ **A:** Not necessarily; overlap decreases with vocab size. In the benchmark: at vocab **400**, BPE–WordPiece overlap is **0.98**, but at vocab **6400** it drops to **0.72**; SentencePiece overlap with each is **0.47** at **6400** (https://arxiv.org/html/2411.17669v1).

**Q: What is Heaps’ Law and why is it relevant here?**  
→ **A:** The benchmark gives Heaps’ Law \(V(N)=K N^\beta\) with typical \(K=10\text{–}100\) and \(\beta=0.4\text{–}0.6\), describing how vocabulary size grows sublinearly with token count; they report tokenizers follow it closely (https://arxiv.org/html/2411.17669v1).

**Q: Can a larger vocabulary make boundary-related behavior worse?**  
→ **A:** Yes; in the protein domain boundary alignment test, **BPE performs best**, but alignment **declines as vocabulary increases** because tokens get longer; alignment correlates with shorter token lengths (https://arxiv.org/html/2411.17669v1).

**Q: Can you show a concrete BPE training/encoding example with real token IDs?**  
→ **A:** Karpathy’s `minbpe` example trains on `"aaabdaaabac"` with `256+3` vocab size and encodes to `[258, 100, 258, 97, 99]`, decoding back exactly to the original string (https://github.com/karpathy/minbpe).

---

## Available Resources

### Videos
- [Let’s build the GPT Tokenizer](https://youtube.com/watch?v=zduSFxRajkE) — **Surface when:** the student asks for an end-to-end, implementation-first walkthrough of BPE tokenization, byte-level quirks, and “foot-guns” that cause LLM oddities.

### Articles & Tutorials
- [Hugging Face NLP Course — Chapter 6.1 (Training a tokenizer)](https://huggingface.co/learn/nlp-course/chapter6/1) — **Surface when:** the student wants a structured path to training a tokenizer from scratch and comparing BPE/WordPiece/Unigram in practice.
- [Hugging Face Tokenizers conceptual guide](https://huggingface.co/docs/tokenizers/conceptual/algorithm) — **Surface when:** the student asks what tokenizers output (`input_ids`, `attention_mask`) or wants algorithm-level descriptions/pseudocode.
- [Sennrich et al. (2016) — Neural Machine Translation of Rare Words with Subword Units](https://arxiv.org/abs/1508.07909) — **Surface when:** the student asks *why* subword tokenization became standard (open vocabulary, rare words).
- [Karpathy — minbpe repository](https://github.com/karpathy/minbpe) — **Surface when:** the student wants minimal code to train/encode/decode BPE and see byte-level details.

---

## Key Sources

- [Subword tokenizers (BPE vs WordPiece vs SentencePiece/Unigram) — comparison metrics & scaling](https://arxiv.org/html/2411.17669v1) — empirical comparisons, definitions of fertility/contextual exponence, overlap numbers, Heaps’ Law, boundary alignment results.  
- [Karpathy — minbpe](https://github.com/karpathy/minbpe) — concrete byte-level BPE implementation details and a fully specified toy example with token IDs.  
- [Hugging Face Tokenizers conceptual guide](https://huggingface.co/docs/tokenizers/conceptual/algorithm) — authoritative description of tokenizer role and common outputs (`input_ids`, `attention_mask`).  
- [Sennrich et al. (2016)](https://arxiv.org/abs/1508.07909) — canonical motivation for subword units to handle rare/OOV words in neural models.