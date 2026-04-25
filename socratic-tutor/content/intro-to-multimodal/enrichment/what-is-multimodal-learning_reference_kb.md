## Core Definitions

**Modality**  
A *modality* is a type of data channel with its own structure and statistics—e.g., text tokens, image pixels/patches/regions, audio waveforms, video frames. Multimodal methods treat each modality as a distinct input space that must be encoded and related to others (e.g., vision features vs. language token embeddings). (Weng, “Generalized Visual Language Models” https://lilianweng.github.io/posts/2022-06-09-vlm/)

**Multi-modal learning**  
*Multi-modal learning* builds models that process and connect multiple modalities (e.g., image+text) to perform tasks requiring joint understanding (captioning, VQA, retrieval). A common pattern is: (1) encode each modality, then (2) fuse information so the model can reason across them. Weng frames modern VLMs as extending pretrained language models to “consume visual signals,” via strategies like treating image patches as tokens, prefixing image embeddings, or using cross-attention to inject vision into language layers. (Weng https://lilianweng.github.io/posts/2022-06-09-vlm/)

**Alignment (multimodal)**  
*Alignment* is establishing semantic relationships across modalities—often by mapping them into a shared space so corresponding items (e.g., an image and its caption) are close/related. The fusion survey explicitly distinguishes: alignment = “establish semantic relationships across modalities,” while fusion = “combine aligned information into unified predictions,” and notes many methods struggle to fuse well without alignment first. (Multimodal Alignment & Fusion survey https://arxiv.org/html/2411.17040v1)

**Fusion (multimodal)**  
*Fusion* is the mechanism for combining information from multiple modalities into a representation used for prediction/decoding. The fusion survey defines fusion as combining (already aligned) information into unified predictions, and organizes fusion by *when/how* modalities interact (early vs late vs hybrid; attention-based; encoder–decoder configurations). (https://arxiv.org/html/2411.17040v1)

**Fusion strategies (taxonomy)**  
A *fusion strategy* specifies where and how modalities are combined:  
- **Early fusion (feature-level / data-level)**: combine modalities early to capture interactions sooner.  
- **Late fusion (decision-level / model-level)**: combine per-modality outputs/decisions; often more robust to missing modalities.  
- **Hybrid fusion**: mixes early and late.  
The survey also describes encoder–decoder fusion forms: data-level (concat raw inputs → shared encoder), feature-level (extract per-modality features → combine → decoder; described as “often most effective”), and model-level (combine model outputs). (https://arxiv.org/html/2411.17040v1)

**Early fusion**  
*Early fusion* combines modalities before (or during) deep representation learning so the model can learn cross-modal interactions throughout the network. The fusion survey emphasizes early fusion’s ability to capture inter-modal interactions earlier than late fusion. (https://arxiv.org/html/2411.17040v1)

**Late fusion**  
*Late fusion* combines modalities after separate processing—e.g., averaging/stacking logits or combining decisions. The fusion survey highlights late fusion’s robustness, including robustness to missing modalities. (https://arxiv.org/html/2411.17040v1)

**Cross-attention fusion**  
*Cross-attention fusion* uses attention where queries from one modality attend to keys/values from another modality, enabling dynamic, content-dependent weighting of cross-modal information. ViLBERT implements this as two-stream co-attention (vision attends to language and language attends to vision). LXMERT similarly uses bidirectional cross-attention between language and object features. (ViLBERT https://proceedings.neurips.cc/paper_files/paper/2019/file/c74d97b01eae257e44aa9d5bade97baf-Paper.pdf; LXMERT https://aclanthology.org/D19-1514.pdf)

---

## Key Formulas & Empirical Results

### Canonical Correlation Analysis (CCA) for explicit alignment (survey)
**Goal:** project two modalities into a common space maximizing correlation.  
\[
\max_{w_x,w_y}\ \rho(X w_x,\; Y w_y)
\]
- \(X, Y\): data matrices from two modalities  
- \(w_x, w_y\): linear projection vectors  
- \(\rho\): correlation coefficient between projected variables  
**Claim supported:** explicit alignment can be done by maximizing cross-modal correlation; linearity motivates nonlinear variants (KCCA/DCCA). (https://arxiv.org/html/2411.17040v1)

### Scaled dot-product attention for attention-based fusion (survey)
\[
\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\!\left(\frac{QK^\top}{\sqrt{d_k}}\right)V
\]
- \(Q\): queries, \(K\): keys, \(V\): values  
- \(d_k\): key dimension (scaling)  
**Claim supported:** attention-based fusion dynamically weights modality features; helps with multimodal noise/uncertainty but increases compute/data needs. (https://arxiv.org/html/2411.17040v1)

### ViLBERT: two-stream co-attention (mechanism + pretraining signals)
**Mechanism (conceptual):** swap key/value across modalities in co-attentional Transformer layers:  
- vision stream update uses \(Q_v\) from vision hidden states and \(K_w,V_w\) from language hidden states  
- language stream update uses \(Q_w\) from language and \(K_v,V_v\) from vision  
**Pretraining tasks (key details):**
- Mask ~15% words + regions; region features zeroed 90% / unchanged 10%; predict region semantic class distribution with KL divergence to detector distribution.  
- Alignment task: use holistic reps \(h_{\text{IMG}}, h_{\text{CLS}}\); combine by element-wise product \(h_{\text{IMG}}\odot h_{\text{CLS}}\) → linear → aligned/not.  
**Transfer numbers (Table 1):** pretrained vs no-pretrain: VQA test-dev 70.55 vs 68.93; VCR Q→AR 54.04 vs 49.48; Image retrieval R@1 58.20 vs 45.50; zero-shot retrieval R@1 31.86. (https://proceedings.neurips.cc/paper_files/paper/2019/file/c74d97b01eae257e44aa9d5bade97baf-Paper.pdf)

### LXMERT: bidirectional cross-attention + pretraining objectives
**Cross-modality encoder (per layer):** bidirectional cross-attn then self-attn in each stream:  
\(\hat h_i^k=\text{CrossAtt}_{L\to R}(h_i^{k-1},\{v_j^{k-1}\})\),  
\(\hat v_j^k=\text{CrossAtt}_{R\to L}(v_j^{k-1},\{h_i^{k-1}\})\), then self-attn within language and within vision.  
**Pretraining tasks:** masked cross-modality LM; masked object prediction (feature regression + label classification); cross-modality matching; image QA. (https://aclanthology.org/D19-1514.pdf)

### Fusion-stage empirical comparisons (survey + FOD paper)

**Data-level fusion vs decision-level fusion (survey):**  
YOLO-style raw camera+LiDAR data-level fusion reported ~**5%** improvement in vehicle detection vs decision-level (late) fusion. (https://arxiv.org/html/2411.17040v1)

**Model-level fusion gains (survey):**  
Quality-control/predictive-maintenance model-level fusion reported **30% reduction in prediction variance** and **45% accuracy increase** vs traditional methods. (https://arxiv.org/html/2411.17040v1)

**Parallel vs concatenation vs cascading fusion (FOD ablation, Table 4; 50K pretrain steps):**  
- MSCOCO TR@1/IR@1: concat 72.5/54.2; cascading 73.0/54.5; **parallel 73.5/55.4**  
- Flickr30k TR@1/IR@1: concat 92.6/80.5; cascading 91.7/81.2; **parallel 93.1/81.6**  
**Claim supported:** fusion *configuration* measurably affects retrieval performance; parallel fusion can be best in this setup. (https://aclanthology.org/2023.findings-acl.316.pdf)

---

## How It Works

### A. Generic multimodal pipeline (tutor “walkthrough”)
1. **Choose modalities + task**  
   Example tasks: image-text retrieval, VQA, captioning (Weng’s VLM overview). (https://lilianweng.github.io/posts/2022-06-09-vlm/)
2. **Encode each modality**  
   - Text → token embeddings via a language model stack (BERT-like in ViLBERT/LXMERT).  
   - Image → region features (e.g., Faster R-CNN regions in ViLBERT; object features + box coords in LXMERT). (ViLBERT; LXMERT)
3. **(Optional but common) Align representations**  
   - Explicit alignment: CCA-style correlation maximization (linear) as a conceptual baseline. (Fusion survey)  
   - Learned alignment: contrastive or matching objectives (e.g., ViLBERT’s aligned/not classifier using \(h_{\text{IMG}}\odot h_{\text{CLS}}\)). (ViLBERT)
4. **Fuse information** (pick a fusion strategy)
   - **Early fusion:** combine features early (concat/merge tokens/regions) so self-attention can learn interactions throughout. (Fusion survey; Weng’s “treat patches as tokens” framing)  
   - **Cross-attention fusion:** one modality attends to the other (ViLBERT co-attention; LXMERT cross-modality encoder).  
   - **Late fusion:** combine per-modality predictions/decisions. (Fusion survey)
5. **Train with multimodal objectives**  
   - Masked modeling across modalities (ViLBERT masked words+regions; LXMERT masked LM + masked objects).  
   - Matching/alignment classification (ViLBERT alignment; LXMERT cross-modality matching).  
6. **Use fused representation for downstream prediction**  
   - Retrieval: similarity between image/text embeddings (common in dual-encoder setups; FOD focuses on retrieval metrics).  
   - VQA/NLVR: classifier head on fused [CLS]-like representation (LXMERT).  

### B. Cross-attention fusion mechanics (two common “reference implementations”)

**1) Two-stream co-attention (ViLBERT)**
1. Maintain **separate** vision and language streams.  
2. In a co-attention layer:  
   - Update vision stream by attending to language (vision queries; language keys/values).  
   - Update language stream by attending to vision (language queries; vision keys/values).  
3. Repeat across multiple co-attention layers; then use task heads. (ViLBERT)

**2) Cross-modality encoder blocks (LXMERT)**
1. Start with language vectors \(h_i\) and object vectors \(v_j\).  
2. Apply **bidirectional cross-attention** to produce \(\hat h_i, \hat v_j\).  
3. Apply **self-attention** within each modality stream.  
4. Stack layers; use [CLS] language vector as cross-modal output. (LXMERT)

### C. Fusion placement as a design knob (FOD “detachable fusion” idea)
1. Use a dual-encoder backbone (ViT for image, BERT-like for text).  
2. Add a **parallel** fusion path on the text side: self-attention + cross-attention averaged (\(\tfrac12(M_l^s+M_l^c)\)).  
3. Because fusion is detachable, you can remove it at inference for efficiency while retaining dual-encoder retrieval behavior. (FOD https://aclanthology.org/2023.findings-acl.316.pdf)

---

## Teaching Approaches

### Intuitive (no math)
- “Each modality is a different language.” Multimodal learning builds a translator and a meeting room: encoders translate each modality into vectors; alignment makes sure “cat” in text corresponds to “cat” in pixels; fusion is how the model combines what each modality says to answer questions or retrieve matches. (Fusion survey distinction: alignment vs fusion)

### Technical (with math)
- Alignment can be formalized as learning projections that maximize cross-modal agreement (CCA: maximize \(\rho(Xw_x, Yw_y)\)).  
- Fusion can be implemented with attention: \(\text{softmax}(QK^\top/\sqrt{d_k})V\), where queries from one modality attend to keys/values from another (cross-attention). (Fusion survey; ViLBERT/LXMERT as concrete architectures)

### Analogy-based
- **Early fusion** is like two people co-writing from the first sentence (rich interaction, but requires both present and can be complex).  
- **Late fusion** is like two people writing separate reports and merging conclusions (robust if one report is missing, but less fine-grained interaction).  
- **Cross-attention fusion** is like a meeting where each person asks targeted questions of the other (“vision attends to language” and vice versa). (Fusion survey; ViLBERT co-attention)

---

## Common Misconceptions

1) **“Multimodal learning just means you concatenate inputs.”**  
- **Why wrong:** Concatenation is only one *fusion configuration* (data-level/feature-level). The survey distinguishes early/late/hybrid and attention-based fusion; ViLBERT/LXMERT show cross-attention mechanisms that are not simple concatenation.  
- **Correct model:** Fusion is a design space (concat, parallel, cascading, cross-attention, decision-level), and choice affects performance/robustness. (Fusion survey; FOD ablations; ViLBERT/LXMERT)

2) **“Alignment and fusion are the same thing.”**  
- **Why wrong:** The fusion survey explicitly separates them: alignment establishes semantic relationships (often shared space), fusion combines aligned info into predictions; poor alignment can make fusion fail.  
- **Correct model:** Treat alignment as “make modalities comparable/related,” fusion as “use those relationships to compute outputs.” (https://arxiv.org/html/2411.17040v1)

3) **“Cross-attention is just self-attention with a different name.”**  
- **Why wrong:** In cross-attention, queries come from one modality while keys/values come from another; ViLBERT explicitly swaps key/value across modalities in co-attention layers.  
- **Correct model:** Self-attention mixes within a sequence/stream; cross-attention mixes *across* streams (vision↔language). (ViLBERT; LXMERT)

4) **“Late fusion is always worse than early fusion.”**  
- **Why wrong:** The survey notes late fusion is robust to missing modalities; early fusion can capture richer interactions but may be less robust when a modality is absent/noisy.  
- **Correct model:** Late fusion trades interaction richness for robustness and modularity; early fusion trades robustness for deeper cross-modal interaction. (Fusion survey)

5) **“If I have a multimodal model, it automatically ‘grounds’ language in vision.”**  
- **Why wrong:** ViLBERT and LXMERT include explicit alignment/matching objectives and masked multimodal modeling; grounding/alignment is trained, not automatic.  
- **Correct model:** Grounding emerges from objectives/architectures that force cross-modal correspondence (matching, contrastive, cross-attention). (ViLBERT; LXMERT; fusion survey alignment emphasis)

---

## Worked Examples

### Example 1: Compute cross-attention fusion (single-head) on toy vectors
Use this when a student asks “what does cross-attention *do* numerically?”

```python
import numpy as np

def softmax(x):
    x = x - x.max(axis=-1, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis=-1, keepdims=True)

# Toy setup: language queries attend to vision keys/values
# Q: 2 text tokens, d=3
Q = np.array([[1.0, 0.0, 1.0],
              [0.0, 1.0, 1.0]])

# K,V: 3 vision regions, d=3
K = np.array([[1.0, 0.0, 0.0],
              [0.0, 1.0, 0.0],
              [1.0, 1.0, 0.0]])
V = np.array([[10.0, 0.0, 0.0],
              [0.0, 10.0, 0.0],
              [5.0, 5.0, 0.0]])

d_k = K.shape[1]
scores = (Q @ K.T) / np.sqrt(d_k)          # QK^T / sqrt(d_k)
weights = softmax(scores)                  # softmax(...)
out = weights @ V                          # ... V

print("scores:\n", scores)
print("weights:\n", weights)
print("cross-attn output:\n", out)
```

**Tutor notes (tie to sources):**
- This is exactly the survey’s attention equation \(\text{softmax}(QK^\top/\sqrt{d_k})V\). (https://arxiv.org/html/2411.17040v1)  
- Interpret `weights` as “which vision regions each text token attends to.” This is the core of cross-attention fusion used in ViLBERT/LXMERT (architecturally scaled up to multi-head + deep stacks). (ViLBERT; LXMERT)

### Example 2: Use FOD ablation numbers to reason about fusion choice
Prompt the student: “If parallel fusion improves IR@1 from 54.2→55.4 on MSCOCO at 50K steps, what does that suggest about fusion placement?”

**Lookup numbers (Table 4):**
- Concatenation: TR@1/IR@1 = 72.5/54.2  
- Cascading: 73.0/54.5  
- **Parallel: 73.5/55.4**  
(FOD https://aclanthology.org/2023.findings-acl.316.pdf)

**Tutor move:** ask them to hypothesize why parallel helps (e.g., preserves unimodal self-attention while adding cross-attention in parallel), then connect back to “fusion is a design knob.”

---

## Comparisons & Trade-offs

| Choice | What it is (per sources) | Strengths | Weaknesses / risks | When to choose |
|---|---|---|---|---|
| Early fusion | Combine modalities early to capture interactions sooner (fusion survey) | Rich cross-modal interactions | Less robust if a modality missing; can be compute-heavy | When both modalities reliably present and fine-grained interactions matter |
| Late fusion | Combine decisions/outputs; robust to missing modalities (fusion survey) | Robustness, modularity | May miss token/region-level interactions | When modalities may be missing or you want modular unimodal experts |
| Cross-attention fusion | Queries from one modality attend to keys/values from another (survey); implemented as co-attention (ViLBERT) or cross-modality encoder (LXMERT) | Dynamic, content-dependent fusion; handles noise/uncertainty (survey) | More compute/data needs (survey) | When you need flexible grounding between modalities (VQA, reasoning) |
| Concatenation vs Cascading vs Parallel (FOD) | Alternative fusion placements on text side (FOD) | Parallel best in reported retrieval ablation | Architecture-specific; adds complexity | When you want detachable fusion and strong retrieval metrics |

---

## Prerequisite Connections

- **Transformers attention basics**: needed to understand why cross-attention fusion is \(\text{softmax}(QK^\top/\sqrt{d_k})V\) and how “queries/keys/values” differ across modalities. (Fusion survey equation; ViLBERT/LXMERT)
- **Representation learning / embeddings**: needed to understand alignment as mapping modalities into a shared space (CCA; matching objectives). (Fusion survey; ViLBERT alignment task)
- **Encoder vs decoder roles**: needed to interpret “encoder–decoder fusion forms” and where fusion happens (data-level/feature-level/model-level). (Fusion survey)

---

## Socratic Question Bank

1) **If alignment is poor, what failure would you expect from fusion?**  
Good answer: fused model can’t reliably connect corresponding concepts across modalities; survey notes fusion often struggles without alignment first.

2) **In cross-attention, what comes from which modality: Q vs K/V? Why does that matter?**  
Good answer: Q from the “updating” modality, K/V from the “conditioning” modality; enables “language attends to vision” or vice versa (ViLBERT).

3) **When might late fusion outperform early fusion in practice?**  
Good answer: missing/noisy modality scenarios; late fusion robustness to missing modalities (survey).

4) **Why might attention-based fusion require more data/compute than simpler fusion?**  
Good answer: attention dynamically weights features and increases model capacity/compute; survey explicitly notes increased compute/data needs.

5) **Given FOD’s ablation, what hypothesis explains parallel > concatenation?**  
Good answer: parallel preserves unimodal processing while injecting cross-modal info; aligns with “detachable fusion” idea (FOD Eq. 5).

6) **How do ViLBERT and LXMERT differ in how they structure cross-modal interaction?**  
Good answer: ViLBERT uses two-stream co-attention layers; LXMERT uses a cross-modality encoder with bidirectional cross-attn then self-attn.

7) **What does the element-wise product \(h_{\text{IMG}}\odot h_{\text{CLS}}\) in ViLBERT’s alignment head imply?**  
Good answer: it’s a simple interaction feature combining holistic image/text reps for match classification (ViLBERT).

8) **What does the ~5% gain from raw camera+LiDAR fusion vs decision-level fusion suggest about fusion stage?**  
Good answer: earlier/data-level fusion can capture complementary signals better than combining final decisions (survey empirical note).

---

## Likely Student Questions

**Q: What’s the difference between “alignment” and “fusion” in multimodal learning?**  
→ **A:** The fusion survey defines *alignment* as establishing semantic relationships across modalities (often via a shared space), while *fusion* is combining aligned information into unified predictions; it notes many methods struggle to fuse well without alignment first. (https://arxiv.org/html/2411.17040v1)

**Q: What’s the actual attention equation used for attention-based fusion?**  
→ **A:** \(\mathrm{Attention}(Q,K,V)=\mathrm{softmax}\left(\frac{QK^\top}{\sqrt{d_k}}\right)V\), where \(Q\)=queries, \(K\)=keys, \(V\)=values, \(d_k\)=key dimension. (https://arxiv.org/html/2411.17040v1)

**Q: How does ViLBERT implement cross-attention fusion?**  
→ **A:** ViLBERT uses a two-stream architecture (vision + language) with co-attentional Transformer layers where vision updates use \(Q_v\) from vision and \(K_w,V_w\) from language (“vision attends to language”), and language updates use \(Q_w\) from language and \(K_v,V_v\) from vision (“language attends to vision”). (https://proceedings.neurips.cc/paper_files/paper/2019/file/c74d97b01eae257e44aa9d5bade97baf-Paper.pdf)

**Q: What pretraining objectives do classic vision-language models use to learn alignment?**  
→ **A:** Examples: ViLBERT uses masked multimodal modeling (mask words + regions) and a multimodal alignment task (aligned/not) using \(h_{\text{IMG}}\odot h_{\text{CLS}}\). LXMERT uses masked cross-modality LM, masked object prediction (feature regression + label classification), cross-modality matching, and image QA. (ViLBERT; LXMERT)

**Q: Is early fusion actually better than late fusion? Any numbers?**  
→ **A:** The fusion survey reports a YOLO-style raw camera+LiDAR *data-level* fusion giving ~**5%** vehicle detection improvement vs *decision-level (late) fusion* in that setting. It also notes late fusion is robust to missing modalities. (https://arxiv.org/html/2411.17040v1)

**Q: What’s “parallel fusion” and does it help?**  
→ **A:** In FOD, a parallel text layer averages self-attention output and cross-attention output (\(\tilde M_l=\tfrac12(M_l^s+M_l^c)\)), making fusion detachable. In Table 4 (50K steps), parallel beats concatenation/cascading on retrieval (e.g., MSCOCO IR@1 **55.4** vs **54.2** concat). (https://aclanthology.org/2023.findings-acl.316.pdf)

**Q: What is CCA doing in multimodal alignment?**  
→ **A:** The survey describes CCA as learning linear projections \(w_x,w_y\) so that the correlation \(\rho(Xw_x, Yw_y)\) between projected modalities is maximized; limitation is linearity, motivating nonlinear variants. (https://arxiv.org/html/2411.17040v1)

---

## Available Resources

### Videos
- [CS224N Guest Lecture: Reinforcement Learning from Human Feedback](https://youtube.com/watch?v=zjrM-MW-0y0) — Surface when: student confuses “alignment” in multimodal learning with “alignment” in RLHF; use to disambiguate terms and contexts.
- [InstructGPT paper explained (Yannic Kilcher)](https://youtube.com/watch?v=VIARnQFSeHk) — Surface when: same as above; also when student asks about “alignment” meaning safety vs representation alignment.

### Articles & Tutorials
- [Lilian Weng — Generalized Visual Language Models](https://lilianweng.github.io/posts/2022-06-09-vlm/) — Surface when: student asks “what are the main architectural families for VLMs?” or needs a map of early fusion vs prefix vs cross-attention approaches.
- [Multimodal Alignment & Fusion survey (arXiv HTML)](https://arxiv.org/html/2411.17040v1) — Surface when: student asks for crisp definitions (alignment vs fusion), fusion taxonomy, or the attention/CCA equations and empirical fusion-stage deltas.

---

## Visual Aids

![Stable Diffusion: text encoder feeds numeric representations to image generator. (Alammar)](/api/wiki-images/multimodal-fundamentals/images/jalammar-illustrated-stable-diffusion_003.png)  
Show when: student needs an immediate, concrete example of a system that combines text + image generation components; use to emphasize “multimodal system = multiple encoders/modules + fusion/conditioning.”

![img2img: Stable Diffusion accepts both image and text inputs. (Alammar)](/api/wiki-images/multimodal-fundamentals/images/jalammar-illustrated-stable-diffusion_002.png)  
Show when: student asks “what does it mean to condition on an image and text together?”; use as a familiar multimodal input example.

![VisualGPT uses gated cross-attention (SRAU) to balance visual and linguistic signals. (Chen et al. 2021)](/api/wiki-images/multimodal-fundamentals/images/lilianweng-posts-2022-06-09-vlm_010.png)  
Show when: student asks “what does cross-attention fusion look like inside a model?”; use to point at cross-attention as a fusion mechanism (even if the specific gating details aren’t needed).

---

## Key Sources

- [Multimodal Alignment & Fusion — core equations + fusion taxonomy](https://arxiv.org/html/2411.17040v1) — Primary for alignment vs fusion definitions, early/late/hybrid taxonomy, and attention/CCA equations plus concrete fusion-stage improvements.
- [ViLBERT (NeurIPS 2019)](https://proceedings.neurips.cc/paper_files/paper/2019/file/c74d97b01eae257e44aa9d5bade97baf-Paper.pdf) — Canonical two-stream co-attention implementation and multimodal pretraining tasks with transfer numbers.
- [LXMERT (ACL 2019)](https://aclanthology.org/D19-1514.pdf) — Explicit cross-modality encoder equations and a clear set of multimodal pretraining objectives.
- [FOD: Flexible VLP via detachable parallel fusion](https://aclanthology.org/2023.findings-acl.316.pdf) — Concrete ablations comparing fusion configurations (concat/cascading/parallel) with retrieval metrics.