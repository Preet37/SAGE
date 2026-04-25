# Card: SCDiar streaming diarization via token-level SCD + representative segments
**Source:** https://arxiv.org/pdf/2501.16641.pdf  
**Role:** paper | **Need:** DEPLOYMENT_CASE  
**Anchor:** Streaming diarization pipeline (token-level speaker change detection, caching, label mapping) + benchmark results

## Key Content
- **System blocks (Sec. II, Fig.1):** VAD → CIF-based ASR → **token-level SCD** (split transcript into homogeneous token segments) → SD network builds **segment–token similarity matrix** → **representative segment selection (optimization)** → **speaker label mapping + cache update** for streaming.
- **Token-level SCD (Sec. II-B, Eq.5–7):** Extract frame-level speaker features \(H\); align to token-level features \(Z\) via MHA using ASR token embeddings as queries; refine with BiLSTM + 1D-CNN (kernel=3); softmax gives per-token change probs; peak detection (`scipy.signal.find_peaks`) with threshold \(\tau\) (inference \(\tau=0.25\)) yields change tokens → segment timestamps (using CIF token timestamps, Eq.4). Training: freeze ASR; TPSP maps reference speaker labels onto hypothesis tokens; **focal loss** (\(\alpha=0.25,\gamma=2\)).
- **Length-aware similarity (Sec. II-C, Eq.12):** Instead of square cosine matrix, compute **rectangular** \(A\) where \(A_{t,s}\) = similarity between token \(t\) and segment \(s\) via refined token speaker embeddings; preserves **segment length/token count** for downstream selection. Training uses weighted BCE vs target matrix, weighted by token count (Eq.13).
- **Representative segment selection (Sec. II-D, Eq.14–15):** Choose binary vector \(x\) over segments (number of 1s = predicted #speakers) to minimize token overlap/miss; relax to bounded non-negative least squares (solved efficiently); threshold \(\sigma=0.3\) selects representative segments.
- **Streaming cache + label mapping (Sec. II-E):** Maintain cache centers \(C\). Steps: (1) cosine distance between new reps \(R\) and \(C\); discard too-similar reps (threshold 0.55). (2) append remaining reps as new speakers. (3) map speaker IDs to segments by cosine distance. (4) update cache center with matched embeddings weighted by token counts. Exclude segments with <10 tokens from rep selection/cache update.
- **Training strategy (Sec. II-F):** Multi-target loss \(L=L_{SD}+ \lambda L_{SCD}\) with \(\lambda=10\). **Split augmentation:** randomly split long segments into two during training to simulate SCD variability.
- **Empirical results (Sec. III-C, Table I; metrics cpWER/WDER):**
  - **AISHELL-4 (4–8 spk):** SCDiar **3.42 / 3.56** vs Core sample+VBx **10.09 / 7.84**; offline SlidingWindow+SpC **2.13 / 2.69** (SCDiar gap: +1.29 cpWER, +0.87 WDER).
  - **In-house (≥10 spk):** SCDiar **10.66 / 15.36** vs Core sample+VBx **21.65 / 19.23**; offline SlidingWindow+SpC **9.95 / 13.51**.
  - **Ablations:** w/o rep selection → AISHELL-4 **11.96 / 8.76**; In-house **13.63 / 16.29**. w/o split strategy → In-house cpWER **14.38** (worse than 10.66).
- **Latency/compute (Sec. III-B/III-C):** Max latency set by VAD max active segment length (default 15s). RTF on Xeon 6148 + V100: ASR **0.072**, SCD **0.004**, SD **0.009**. Performance degrades when streaming chunk <3s; stabilizes after ~10s.

## When to surface
Use when students ask how to design **real-time speaker-attributed ASR/diarization**: token-level SCD segmentation, handling short utterances via **representative segment selection**, and **streaming speaker cache/label mapping** with concrete thresholds and benchmark deltas vs offline/other online methods.