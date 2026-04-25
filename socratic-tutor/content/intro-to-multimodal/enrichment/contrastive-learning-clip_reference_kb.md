## Key Facts & Specifications

- **CLIP training objective (batch-level classification framing)**
  - CLIP is trained to predict which of the **N×N** possible image–text pairings in a batch are the true pairs, maximizing cosine similarity for the **N** true pairs and minimizing similarity for the **N²−N** incorrect pairings, using a **symmetric cross-entropy loss** over similarity scores (quoted in MachineCurve’s summary of Radford et al., 2021). (machinecurve.com, 2023-12-22: https://machinecurve.com/index.php/2023/12/22/clip-how-it-works-is-trained-and-used)

- **Temperature / logit scaling in OpenAI CLIP**
  - The **learnable temperature parameter** was initialized to the equivalent of **0.07** (referencing Wu et al., 2018) and **clipped** to prevent scaling logits by more than **100** to prevent training instability. (openai/CLIP Issue #46: https://github.com/openai/CLIP/issues/46)
  - OpenAI CLIP code clamps the exponentiated scale: `logit_scale = torch.clamp(self.logit_scale.exp(), max=100)`. (openai/CLIP Issue #46: https://github.com/openai/CLIP/issues/46)
  - Rationale for scaling: normalized dot products are in **[-1, 1]**, so scaling increases logit dynamic range; scale is clipped at **100** for numerical stability; commenters report it “reached 100” for all trained models. (openai/CLIP Issue #48: https://github.com/openai/CLIP/issues/48)

- **Cosine similarity / normalization rationale**
  - Using cosine similarity (via L2-normalized embeddings) helps **stabilize training** by limiting logit dynamic range; with cosine similarities in **[-1, 1]** and an upper-bounded temperature parameter, it helps prevent exploding predictions. (openai/CLIP Issue #68: https://github.com/openai/CLIP/issues/68)

- **Tokenizer / context length / special tokens**
  - OpenAI/OpenCLIP default context length is **77** tokens. (open_clip tokenizer: https://github.com/mlfoundations/open_clip/blob/main/src/open_clip/tokenizer.py; HF config also lists `max_position_embeddings` default 77: https://github.com/huggingface/transformers/blob/main/src/transformers/models/clip/configuration_clip.py)
  - Tokenizer adds special tokens `'<|startoftext|>'` and `'<|endoftext|>'`. (openai/CLIP simple_tokenizer.py: https://github.com/openai/CLIP/blob/main/clip/simple_tokenizer.py)
  - CLIP text vocab size default is **49408** in Hugging Face `CLIPTextConfig`. (Hugging Face `configuration_clip.py`: https://github.com/huggingface/transformers/blob/main/src/transformers/models/clip/configuration_clip.py)

- **Image preprocessing (OpenAI CLIP)**
  - CLIP “works best” at **224×224**; preprocessing described as: resize so the **shorter side becomes 224**, then **center crop** to **224×224**, convert pixels from **[0,255]** to **[0.0,1.0]**, then normalize. (openai/CLIP Issue #459: https://github.com/openai/CLIP/issues/459)
  - Common normalization constants used in CLIP/OpenCLIP examples:
    - mean = **(0.48145466, 0.4578275, 0.40821073)**
    - std = **(0.26862954, 0.26130258, 0.27577711)**
    (John O Whitaker course page: https://johnowhitaker.github.io/tglcourse/clip.html; OpenCLIP PreprocessCfg: https://www.mintlify.com/mlfoundations/open_clip/usage/image-preprocessing)

- **InfoNCE and mutual information bound (general InfoNCE)**
  - InfoNCE is used to estimate a lower bound on mutual information by discriminating a positive pair against **K** negatives; InfoNCE loss is:
    - \( L_K = -\log\left(\frac{e^{f(x^+,c)}}{e^{f(x^+,c)}+\sum_{i=1}^K e^{f(x_i^-,c)}}\right) \)
    - MI lower bound: \( I(x^+,c) \ge \log(K+1) - L_K \)
    (IJCAI 2022 “Rethinking InfoNCE”: https://www.ijcai.org/proceedings/2022/0348.pdf)
  - InfoNCE/INCE bound is **upper bounded by \(\log K\)**, so it becomes loose when \(I(X;Y) > \log K\). (Poole et al., 2019: http://proceedings.mlr.press/v97/poole19a/poole19a.pdf)

- **CLIP model hyperparameters (ViT variants table from a CVPR 2023 supplement)**
  - Table lists (among others):  
    - **ViT-B/32**: embedding dimension **512**, input resolution **224**, vision transformer **12 layers**, vision width **768**, vision heads **12**; text transformer **12 layers**, text width **512**, text heads **8**.  
    - **ViT-L/14**: embedding dimension **768**, input resolution **224**, vision transformer **24 layers**, vision width **1024**, vision heads **16**; text transformer **12 layers**, text width **768**, text heads **12**.  
    - **ViT-L/14-336px**: embedding dimension **768**, input resolution **336** (other values same as ViT-L/14).  
    (CVPR 2023 supplemental Table A.2: https://openaccess.thecvf.com/content/CVPR2023/supplemental/Wu_Bidirectional_Cross-Modal_Knowledge_CVPR_2023_supplemental.pdf)

- **Training compute/batch size facts (as reported by later papers)**
  - Original CLIP training: batch size **32768** and **256 V100 GPUs** (reported in ICCV 2023 supplemental). (Wei et al., ICCV 2023 supplemental: https://openaccess.thecvf.com/content/ICCV2023/supplemental/Wei_Improving_CLIP_Fine-tuning_ICCV_2023_supplemental.pdf)
  - FastCLIP paper reports: “CLIP uses **592 V100 GPUs**” (note: this conflicts with the ICCV 2023 supplemental’s “256 V100 GPUs”). (FastCLIP arXiv 2024: https://arxiv.org/html/2407.01445v1)

- **Zero-shot prompt effect (reported)**
  - Using the prompt template `"a photo of a {label}"` reportedly gave a **1.3 percentage point** improvement in ImageNet accuracy. (Pinecone zero-shot article: https://www.pinecone.io/learn/series/image-search/zero-shot-image-classification-clip/)

- **SigLIP (sigmoid loss) key quantitative claims**
  - Sigmoid loss does not require global batch normalization across all pairwise similarities; it operates on image–text pairs without a “global view” for normalization. (Zhai et al., ICCV 2023: https://openaccess.thecvf.com/content/ICCV2023/papers/Zhai_Sigmoid_Loss_for_Language_Image_Pre-Training_ICCV_2023_paper.pdf)
  - Sigmoid loss performs “significantly better” than softmax loss when batch size is **< 16k**; as batch size grows, the gap closes; performance saturates around **32k** batch size (both sigmoid and softmax), and very large batch sizes can hurt. (Zhai et al., ICCV 2023)
  - With **four TPUv4 chips**, they could fit **4096** batch size for a Base SigLIP vs **2048** for a corresponding CLIP model. (Zhai et al., ICCV 2023)
  - SigLIP from-scratch training reaches **73.4%** ImageNet zero-shot accuracy in **5 days** with **32 TPUv4 chips**; compared to prior works requiring ~**5** and **10** days on **256 TPUv3 cores** (FLIP and CLIP respectively, as stated in the paper). (Zhai et al., ICCV 2023)

- **OpenCLIP / LAION performance numbers (blog)**
  - OpenAI CLIP L/14: batch size **32k**, samples seen **13B**, ImageNet top-1 **75.4%**; MS COCO image retrieval Recall@5 **61.0%**; Flickr30k Recall@5 **87.0%**. (LAION “Giant OpenCLIP” blog, 2023-01-24: https://laion.ai/blog/giant-openclip/)
  - OpenCLIP G/14 trained on LAION-2B: ImageNet top-1 **80.1%** (and **80.3%** with CuPL prompts; **80.4%** at 280×280 with “squash” resize per Ross Wightman, as reported). (LAION blog, 2023-01-24)

- **Data curation / dataset facts**
  - LAION-5B size: **5.85 billion** CLIP-filtered image–text pairs; breakdown: **2.3B English**, **2.2B** in **100+** other languages, **1B** unassigned language. (LAION blog, 2022-03-31: https://laion.ai/blog/laion-5b/)
  - Re-LAION-5B filtering thresholds:
    - Re-LAION-5B-research: remove samples with **p_unsafe > 0.95** (with keyword-based text filters); removal reported as **1.121%** (22.42M from 2B; 65M from 5.8B). (LAION Re-LAION-5B blog: https://laion.ai/blog/relaion-5b/)
    - Re-LAION-5B-research-safe: remove majority of NSFW with **p_unsafe > 0.45**; removal **3.044%** (60.88M from 2B; 176M from 5.8B). (LAION Re-LAION-5B blog)
  - MetaCLIP paper reports (ViT-B, ImageNet zero-shot):
    - CLIP data: **63.4%** (WIT400M)
    - LAION-400M: **60.0%**
    - MetaCLIP 400M w/o balancing: **60.8%**
    - MetaCLIP balanced: **65.5%**
    - Raw English 400M: **57.4%**
    - Raw set ~1.1B after language ID: **54.1%**
    (MetaCLIP / “Demystifying CLIP Data” arXiv HTML: https://arxiv.org/html/2309.16671v4)
  - Same MetaCLIP paper states: MetaCLIP achieves **70.8%** vs CLIP **68.3%** on ViT-B models (zero-shot ImageNet classification). (arXiv: https://arxiv.org/html/2309.16671v4)

- **OpenAI CLIP repo ImageNet zero-shot reproduction notes**
  - GitHub issue reports notebook results: ResNet-50 top-1 **55.09**, top-5 **83.59**; ViT-B/32 top-1 **59.06**, top-5 **85.59**. (openai/CLIP Issue #24: https://github.com/openai/CLIP/issues/24)
  - Discrepancy noted by users between paper table numbers and notebook; user later reports they matched paper after switching to ImageNet validation set. (openai/CLIP Issue #24)

---

## Technical Details & Procedures

- **CLIP symmetric InfoNCE / cross-entropy implementation (formula form)**
  - A symmetric CLIP loss can be written as the average of two directional cross-entropies (image→text and text→image) over the similarity matrix. (Emergent Mind objective page: https://www.emergentmind.com/topics/clip-s-image-text-alignment-objective; MachineCurve example: https://machinecurve.com/index.php/2023/12/22/clip-how-it-works-is-trained-and-used)
  - Emergent Mind provides an explicit symmetric InfoNCE form:
    - \( \mathcal{L}_\mathrm{CLIP} = -\frac{1}{2N}\sum_{i=1}^N \left[\log\frac{\exp(\mathrm{sim}(x_i,t_i)/\tau)}{\sum_{j=1}^N \exp(\mathrm{sim}(x_i,t_j)/\tau)} + \log\frac{\exp(\mathrm{sim}(x_i,t_i)/\tau)}{\sum_{j=1}^N \exp(\mathrm{sim}(x_j,t_i)/\tau)}\right] \)
    (Emergent Mind embeddings page: https://www.emergentmind.com/topics/clip-image-and-text-embeddings)

- **OpenAI CLIP temperature initialization and clipping (training-side guidance from issues)**
  - Training code detail is partially missing from released inference-focused code; suggested training loop fix:
    - After `optimizer.step()`, check `logit_scale` and if it exceeds `log(100)`, set it to `log(100)` (so that `exp(logit_scale)` ≤ 100). (openai/CLIP Issue #46)
  - Suggested initialization:
    - `nn.init.constant_(self.logit_scale, np.log(1/0.07))` or `nn.Parameter(torch.tensor([np.log(1/0.07)]))`. (openai/CLIP Issue #46)
  - Hugging Face vs OpenAI discrepancy noted:
    - HF example: `self.logit_scale = nn.Parameter(torch.ones([]))`
    - OpenAI: `self.logit_scale = nn.Parameter(torch.ones([]) * np.log(1 / 0.07))`
    (HF transformers Issue #13430: https://github.com/huggingface/transformers/issues/13430)

- **OpenCLIP image preprocessing configuration**
  - OpenCLIP provides `create_model_and_transforms` returning `preprocess_train` and `preprocess_val`. Example:
    ```python
    model, preprocess_train, preprocess_val = open_clip.create_model_and_transforms(
      'ViT-B-32', pretrained='laion2b_s34b_b79k'
    )
    image_train = preprocess_train(Image.open('train.jpg'))
    image_val = preprocess_val(Image.open('val.jpg'))
    ```
    (OpenCLIP Mintlify docs: https://www.mintlify.com/mlfoundations/open_clip/usage/image-preprocessing)
  - `PreprocessCfg` parameters (example values):
    - `size=224`, `mode='RGB'`, `mean=(0.48145466, 0.4578275, 0.40821073)`, `std=(0.26862954, 0.26130258, 0.27577711)`, `interpolation='bicubic'`, `resize_mode='shortest'`, `fill_color=0`. (Mintlify OpenCLIP docs)

- **OpenAI CLIP-style preprocessing steps (as described in issue)**
  - Resize shortest edge to **224**, keep aspect ratio; center crop to **224×224**; convert to float in **[0,1]**; normalize. (openai/CLIP Issue #459)

- **Tokenization procedure (OpenCLIP)**
  - Default context length is **77**; tokenization returns tensor shape `[num_texts, context_length]`.
  - If token sequence exceeds context length, it is **truncated** and last token set to `eot_token_id`. (open_clip tokenizer: https://github.com/mlfoundations/open_clip/blob/main/src/open_clip/tokenizer.py)

- **Getting 512-d projected embeddings in Hugging Face**
  - To obtain projected embeddings (e.g., 512-d) from a CLIP vision model checkpoint that includes a projection head, use `CLIPVisionModelWithProjection` and read `outputs.image_embeds`. (HF forum thread: https://discuss.huggingface.co/t/how-to-get-an-embedding-of-size-512-using-clip-equal-to-open-clip/73849)

- **FastCLIP inner learning rate cosine schedule (exact formula)**
  - FastCLIP defines a cosine schedule for inner LR \(\gamma_t\):
    - \(\gamma_{t}=0.5\cdot(1+\cos(\pi\lfloor t/\hat{E}\rfloor/E))\cdot(1-\gamma_{\mathrm{min}})+\gamma_{\mathrm{min}}\)
    - \(\hat{E}\): iterations per epoch; \(E\): number of decay epochs; \(\gamma_t\) constant within an epoch; after epoch \(>E\), \(\gamma_t=\gamma_{\min}\).
    (FastCLIP arXiv HTML: https://arxiv.org/html/2407.01445v1)

---

## Comparisons & Trade-offs

- **Softmax (InfoNCE-style) vs Sigmoid loss (SigLIP)**
  - **Softmax loss** requires batch-level normalization across all pairwise similarities (and is applied twice due to asymmetry: normalize across images and across texts). (Zhai et al., ICCV 2023)
  - **Sigmoid loss** operates on pairs without requiring global normalization; simplifies distributed implementation and is described as more memory efficient. (Zhai et al., ICCV 2023)
  - Batch size regime:
    - Sigmoid loss “significantly better” when batch size **< 16k**; gap closes as batch size increases. (Zhai et al., ICCV 2023)
    - Both saturate around **32k** batch size; very large batch sizes can hurt. (Zhai et al., ICCV 2023)
  - Fixed-resource batch size fit example: Base SigLIP **4096** vs corresponding CLIP **2048** on **4 TPUv4 chips**. (Zhai et al., ICCV 2023)

- **Data curation impact (MetaCLIP vs WIT400M vs LAION-400M)**
  - With frozen model/training schedule, MetaCLIP reports substantial differences attributable to data:
    - WIT400M (CLIP): **63.4%** ImageNet zero-shot (ViT-B)
    - LAION-400M: **60.0%**
    - MetaCLIP balanced: **65.5%**
    (MetaCLIP arXiv: https://arxiv.org/html/2309.16671v4)

- **OpenAI CLIP vs OpenCLIP (blog-reported benchmarks)**
  - OpenAI CLIP L/14: ImageNet top-1 **75.4%** (batch size **32k**, samples seen **13B**). (LAION blog, 2023-01-24)
  - OpenCLIP G/14: ImageNet top-1 **80.1%** (batch size **160k**, trained on LAION-2B; additional notes about prompts/resolution). (LAION blog, 2023-01-24)

- **Conflicting reports on CLIP training GPU count**
  - ICCV 2023 supplemental: CLIP trained with **256 V100 GPUs** (batch size **32768**). (Wei et al., ICCV 2023 supplemental)
  - FastCLIP arXiv: “CLIP uses **592 V100 GPUs**.” (FastCLIP arXiv 2024)
  - These sources disagree; a tutor should flag this as a discrepancy rather than asserting one value.

---

## Architecture & Design Rationale

- **Dual-encoder design**
  - CLIP uses separate image and text encoders that produce vectors in a shared embedding space; similarity is computed between these vectors for alignment and retrieval/classification. (Pinecone “Using CLIP”: https://www.pinecone.io/learn/series/image-search/clip/; Lightly blog: https://www.lightly.ai/blog/clip-openai)

- **Why normalize embeddings + learn a temperature**
  - L2 normalization caps dot products to **[-1, 1]**, which stabilizes training; scaling (temperature/logit_scale) increases dynamic range so cross-entropy can express sharper distributions; scale is clipped (max **100**) to avoid numerical instability. (openai/CLIP Issues #48 and #68; Issue #46 for clipping)

- **Why symmetric loss (two directions)**
  - Symmetric objective averages image→text and text→image cross-entropy terms, supporting bidirectional retrieval behavior. (Emergent Mind objective page; MachineCurve explanation)

- **Why sigmoid loss can be more scalable (SigLIP rationale)**
  - Softmax-based contrastive loss needs global normalization and often materializes a |B|×|B| similarity matrix; sigmoid loss avoids global normalization and is described as enabling more memory-efficient implementations and larger batch sizes. (Zhai et al., ICCV 2023)

---

## Common Questions & Answers

- **Q: What exactly is CLIP optimizing in a batch?**
  - A: It predicts which of the **N×N** image–text pairings in a batch are the true pairs, maximizing similarity for the **N** true pairs and minimizing similarity for the **N²−N** incorrect pairings, using a **symmetric cross-entropy** over similarity scores. (machinecurve.com, 2023-12-22; Emergent Mind objective page)

- **Q: Why does CLIP L2-normalize embeddings and then scale logits?**
  - A: Normalization caps similarities to **[-1, 1]**, stabilizing training; scaling increases logit dynamic range; the scale is clipped at **100** to avoid numerical instability. (openai/CLIP Issue #48; openai/CLIP Issue #68; openai/CLIP Issue #46)

- **Q: What is the temperature initialization and clipping used in OpenAI CLIP training?**
  - A: The learnable temperature was initialized to the equivalent of **0.07** and the logit scale was clipped so logits are not scaled by more than **100**. (openai/CLIP Issue #46)

- **Q: Why do some implementations initialize `logit_scale` differently?**
  - A: A Hugging Face issue notes HF used `nn.Parameter(torch.ones([]))` while OpenAI used `nn.Parameter(torch.ones([]) * np.log(1/0.07))`, and warns incorrect initialization can cause training issues. (HF transformers Issue #13430)

- **Q: What image preprocessing does CLIP expect?**
  - A: CLIP was trained on **224×224** images; recommended preprocessing: resize shortest edge to **224** (keep aspect ratio), then center crop to **224×224**, convert pixels to **[0,1]**, then normalize. (openai/CLIP Issue #459)

- **Q: What is CLIP’s text context length and vocab size?**
  - A: Default context length is **77** tokens; Hugging Face `CLIPTextConfig` default vocab size is **49408**; tokenizer uses `'<|startoftext|>'` and `'<|endoftext|>'`. (open_clip tokenizer; HF configuration_clip.py; openai simple_tokenizer.py)

- **Q: How do I get the projected 512-d image embedding in Hugging Face?**
  - A: Use `CLIPVisionModelWithProjection` and read `outputs.image_embeds` (the projection layer maps to the shared embedding space). (HF forum thread: https://discuss.huggingface.co/t/how-to-get-an-embedding-of-size-512-using-clip-equal-to-open-clip/73849)

- **Q: Does prompt templating measurably help zero-shot classification?**
  - A: One report states that using `"a photo of a {label}"` improved ImageNet accuracy by **1.3 percentage points**. (Pinecone zero-shot article)

- **Q: How does SigLIP differ from CLIP’s softmax contrastive loss?**
  - A: SigLIP uses a pairwise **sigmoid loss** that does not require global batch normalization across all similarities; it performs better at batch sizes **<16k**, and both losses saturate around **32k** batch size. (Zhai et al., ICCV 2023)

- **Q: How many GPUs were used to train the original CLIP?**
  - A: Sources conflict: one paper supplement says **256 V100 GPUs** (batch size **32768**), while FastCLIP reports **592 V100 GPUs**. A tutor should present both and note the discrepancy. (Wei et al., ICCV 2023 supplemental; FastCLIP arXiv 2024)

