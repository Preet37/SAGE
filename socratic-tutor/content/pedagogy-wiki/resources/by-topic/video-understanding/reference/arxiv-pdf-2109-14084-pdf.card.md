# Card: VideoCLIP pre-training pipeline (overlap positives + retrieval hard negatives)
**Source:** https://arxiv.org/pdf/2109.14084.pdf  
**Role:** paper | **Need:** CONCEPT_EXPLAINER  
**Anchor:** Training pipeline details for video-text contrastive pretraining: overlapped positives, retrieval-mined hard negatives, InfoNCE objective, key hyperparams/results.

## Key Content
- **Encoders (Sec. 3.1):**
  - Video tokens: \(x^v = f_{\theta_{\text{MLP}}}(\text{stopgrad}(f_{\theta_{\text{CNN}}}(c^v)))\) (Eq. 1). CNN is **frozen**.
  - Transformers: \(h^v=f_{\theta_v}(x^v),\; h^t=f_{\theta_t}(x^t)\) (Eq. 2).
  - Global clip embeddings via **average pooling**: \(z^v=\text{AvgPool}(h^v),\; z^t=\text{AvgPool}(h^t)\) (Eq. 3). Rationale: encourages token-level reps (helps localization/segmentation); [CLS] pooling hurts (Table 7).
- **Contrastive objective (Sec. 3.2):**
  - Symmetric InfoNCE (Eq. 4):  
    \(\mathcal{L}=-\sum_{(v,t)\in B}\big(\log \text{NCE}(z^v,z^t)+\log \text{NCE}(z^t,z^v)\big)\).
  - Video→Text NCE (Eq. 5):  
    \(\text{NCE}(z^v,z^t)=\dfrac{\exp(z^v\cdot z_t^+/\tau)}{\sum_{z\in\{z_t^+,z_t^-\}}\exp(z^v\cdot z/\tau)}\). Negatives \(z_t^-\) are **other texts in batch**; symmetric for text→video.
- **Positive pair construction = temporal overlap (Sec. 3.3):**
  1) sample a **text clip first**; 2) sample a timestamp within it as video center; 3) grow a **random-duration** video clip (up to ~32s). Rationale: strict start/end alignment often low semantic relevance.
- **Hard negatives via retrieval-augmented batching (Sec. 3.4, Alg. 1):**
  - Each epoch: compute per-video global feature \(z_V=\frac{1}{2|B_V|}\sum_{(v,t)\in B_V}(z^v+z^t)\); build FAISS index; for random video \(V\), retrieve **2k-NN**, then **sample k videos** to form a cluster/batch so clips from different but similar videos become hard negatives.
- **Defaults / hyperparams (Sec. 5.3):**
  - Video encoder: S3D pretrained on HowTo100M; 30fps; **1 token/sec**, dim 512 → MLP to 768; max **32 video tokens** (3–32s).
  - Text: 8–61 tokens (plus [CLS],[SEP]); avg ASR ~2.4 tokens/sec.
  - Batch: **k=32 videos**, **16 pairs/video** ⇒ \(|B|=512\). Temperature \(\tau=1.0\).
  - Init: BERT-base uncased; **6 layers** for video, **12** for text.
  - Train: 8×V100 32GB, fp16, **25 epochs**; Adam lr 5e-5, warmup 1000, poly decay, betas (0.9,0.98), grad clip 2.0.
- **Key empirical deltas (Table 7, Youcook2 zero-shot R@1):**
  - Full VideoCLIP: **22.7** (R@5 50.4, R@10 63.1)
  - w/o retrieval: **18.5**; w/o retrieval + w/o overlap: **12.4**
  - MIL-NCE clips+loss: **16.1**; use [CLS]: **22.1**; retrieve k directly: **22.5**; use first 32s for retrieval: **20.1**
- **Headline zero-shot results:**
  - Youcook2 retrieval: **22.7 R@1** (Table 1); COIN action segmentation: **58.9%** frame acc (Table 4); MSR-VTT VideoQA: **73.9%** (Table 3).

## When to surface
Use when students ask how video-text contrastive pretraining forms positives/negatives, why temporal overlap helps, how retrieval-mined hard negatives are implemented, or what concrete hyperparameters/results support these design choices.