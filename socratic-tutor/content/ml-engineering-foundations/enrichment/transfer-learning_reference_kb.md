## Key Facts & Specifications

- **ImageNet dataset scale (commonly used for pretraining CNNs)**
  - ImageNet contains **1.2 million images** with **1000 categories**. (Note_08.pdf, “Transfer Learning & CNN Case Studies”, http://www.joonseok.net/viplab/courses/mlvu_2021_1/notes/Note_08.pdf)

- **PyTorch transfer learning tutorial: concrete hyperparameters and timings (ResNet-18)**
  - Uses `resnet18(weights='IMAGENET1K_V1')` and replaces the final layer with `nn.Linear(num_ftrs, 2)`. (PyTorch Transfer Learning Tutorial, https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)
  - Fine-tuning example optimizer: **SGD lr=0.001, momentum=0.9**. (PyTorch tutorial URL above)
  - LR schedule: `StepLR(step_size=7, gamma=0.1)` i.e., **decay LR by factor 0.1 every 7 epochs**. (PyTorch tutorial URL above)
  - Training duration estimate: **15–25 min on CPU**, **< 1 minute on GPU** for the tutorial run. (PyTorch tutorial URL above)
  - Example run (fine-tuning all parameters): **Best val Acc: 0.934641**, training complete in **0m 37s**, `num_epochs=25`. (PyTorch tutorial URL above)
  - Example run (fixed feature extractor): **Best val Acc: 0.947712**, training complete in **0m 28s**, `num_epochs=25`. (PyTorch tutorial URL above)
  - Fixed-feature-extractor CPU time: “**about half the time** compared to previous scenario” because gradients aren’t computed for most of the network (but forward still is). (PyTorch tutorial URL above)

- **Freezing parameters in PyTorch**
  - To freeze parameters so gradients are not computed in `backward()`, set `requires_grad = False`. (PyTorch tutorial URL above)
  - PyTorch forum example: freezing layers 1–6 out of 10 “layers” in ResNet-50 by iterating `model.children()` and setting `param.requires_grad=False` for selected children. (PyTorch Forums thread, https://discuss.pytorch.org/t/how-the-pytorch-freeze-network-in-some-layers-only-the-rest-of-the-training/7088)

- **Optimizer parameter filtering when some parameters are frozen**
  - PyTorch core dev guidance: explicitly filter parameters passed to the optimizer:
    - `optimizer.SGD(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)` (PyTorch GitHub issue #679, https://github.com/pytorch/pytorch/issues/679)
  - If you include a parameter with `requires_grad=False` as an `nn.Parameter` in an optimizer, you can get an error: **“optimizing a parameter that doesn't require gradients”**. (PyTorch GitHub issue #679 URL above)

- **Hugging Face Transformers learning-rate schedules: exact behavior**
  - `get_linear_schedule_with_warmup`: LR **increases linearly from 0 to initial optimizer LR** during warmup, then **decreases linearly from initial LR to 0** by `num_training_steps`. (Transformers `optimization.py`, https://github.com/huggingface/transformers/blob/main/src/transformers/optimization.py)
  - `get_cosine_schedule_with_warmup`: LR **increases linearly from 0 to initial LR** during warmup, then **decreases following cosine** from initial LR to **0** by end. Default `num_cycles=0.5`. (Transformers `optimization.py` URL above)
  - `get_cosine_with_hard_restarts_schedule_with_warmup`: cosine decay to **0** with **hard restarts**, default `num_cycles=1`. (Transformers `optimization.py` URL above)

- **Warmup example with explicit numbers (fine-tuning schedule explanation)**
  - Example: training for **1,000 steps** with **100 warmup steps**; LR increases from **0 to 2e-5** during first 100 steps, then decreases linearly to **0**. (Milvus AI quick reference, https://milvus.io/ai-quick-reference/what-is-the-learning-rate-schedule-used-during-finetuning)

- **STILTs (intermediate-task fine-tuning) reported benchmark numbers**
  - Repo claim: **GLUE score 82.0** for “BERT on STILTs” vs **80.5** without STILTs. (zphang/bert_on_stilts README, https://github.com/zphang/bert_on_stilts/blob/master/README.md)
  - Paper (ar5iv mirror) reports: GLUE score **81.8** and **1.4 point improvement over BERT**; notes reduced variance across random restarts. (Phang et al., 2018; ar5iv HTML, https://ar5iv.labs.arxiv.org/html/1811.01088)

- **STILTs procedure/training regime details**
  - STILTs experiments: (i) unsupervised pretraining; (ii) intermediate labeled task; (iii) target task fine-tuning. (Phang et al., 2018 ar5iv URL above)
  - Training details: **three-epoch training limit** for both supplementary training and target-task fine-tuning; **fresh optimizer for each phase**; add **single task-specific randomly initialized output layer**. (Phang et al., 2018 ar5iv URL above)
  - For limited-data tasks (CoLA, MRPC, STS, RTE): **20 random restarts** and report best validation run. (Phang et al., 2018 ar5iv URL above)
  - Repo notes STILTs benefits on tasks with **<10k training examples**. (bert_on_stilts README URL above)

- **EWC (Elastic Weight Consolidation): explicit loss form and hyperparameter ranges (from provided sources)**
  - EWC loss form:  
    \[
    \ell_{\text{EWC}}(\boldsymbol{\theta})=\ell_{\text{new}}(\boldsymbol{\theta})+\frac{\lambda}{2}\sum_{i=1}^{N_{\text{params}}}F_{\text{old}}^{i,i}(\theta^{i}-\hat{\theta}_{\text{old}}^{i})^{2}
    \]
    (ArXiv HTML “On the Computation of the Fisher Information…”, https://arxiv.org/html/2502.11756v1)
  - Fisher Information Matrix definition:  
    \(I(\theta)=\mathbb{E}_D[\nabla_\theta L(\theta)\nabla_\theta L(\theta)^T]\). (OpenReview PDF, https://openreview.net/pdf/96bc3cdd41dda199d62b66f479e97475c16a84f5.pdf)
  - A replication/extension study reports cross-validation ranges:
    - Batch sizes: **32, 64, 128**
    - Momentum: **0–0.9**
    - L2 regularization \(\lambda\): **1·10^-5 to 1**
    - EWC \(\lambda\): **1 to 1·10^4**  
    (ArXiv HTML 2507.10485v1, https://arxiv.org/html/2507.10485v1)

- **Domain/task-adaptive pretraining efficiency claim (selective pretraining)**
  - For TAPT on BERT-based models: training **only the embedding layer** can be sufficient to adapt vocabulary and achieve comparable performance; this trains **78% fewer parameters** during TAPT. (Ladkat et al., 2022, https://arxiv.org/abs/2209.12943)

- **Feature hierarchy / transfer learning rationale with specific numbers**
  - In AlexNet feature extraction scenario: hidden layer before classifier yields a **4096-D vector** (“CNN codes”). (Note_08.pdf URL above)
  - Training modern ConvNets on ImageNet can take **2–3 weeks across multiple GPUs**. (Note_08.pdf URL above)
  - Fine-tuning learning rate choice in one CNN transfer study: start fine-tuning with learning rate **0.001**, described as **1/10-th** the initial learning rate used for ImageNet training; reduce LR by factor **10 every 20,000 iterations**. (Pulkit et al., 2014 arXiv PDF, http://arxiv.org/pdf/1407.1610.pdf)

- **Empirical comparison: feature extraction vs fine-tuning (3D ResNet-50)**
  - Feature extraction (frozen): **Test accuracy 85.2 ± 0.6**, **F1 83.5 ± 0.5**, **loss 1.20 ± 0.04**, training duration **Short (≈10 epochs)**, computational cost **Low**. (Table 5, https://pmc.ncbi.nlm.nih.gov/articles/PMC12615596/table/Tab5/)
  - Fine-tuning (unfrozen last block): **Test accuracy 89.8 ± 0.5**, **F1 88.6 ± 0.4**, **loss 0.85 ± 0.03**, training duration **Longer (≈15 epochs)**, computational cost **High**. (Same Table 5 URL)

- **Early stopping: concrete callback parameters**
  - Keras example: `EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)` used with `model.fit(..., epochs=10, ...)`. (Weights & Biases report, https://wandb.ai/ayush-thakur/huggingface/reports/Examples-of-Early-Stopping-in-HuggingFace-Transformers--Vmlldzo0MzE2MTM)

- **GradES (component-wise early stopping) reported speed/accuracy numbers**
  - Claims: reduces fine-tuning time by **50%** while maintaining or improving accuracy across eight benchmarks; across five models **0.6B–14B** parameters. (GradES arXiv HTML, https://arxiv.org/html/2509.01842v3)
  - Table example: **6.79× speedup** vs classic early stopping on Qwen3-0.6B (reported **907s vs 6,155s** for LoRA fine-tuning). (GradES arXiv HTML URL above)
  - Example accuracy comparison: **67.30% (GradES)** vs **67.37% (classic early stopping)** (as cited in the paper text). (GradES arXiv HTML URL above)
  - Reported training-time reduction range: **35–66%** across five models; FLOPs reduction **45–71%** vs baseline full fine-tuning. (GradES arXiv HTML URL above)
  - Reported best average accuracy: **92.81%** with \(\tau=1.5\), \(\alpha=0.5\); most significant speedup at \(\tau=9.0\), \(\alpha=0.1\). (GradES arXiv HTML URL above)

---

## Technical Details & Procedures

### A. PyTorch: Fine-tuning a pretrained ResNet-18 (all parameters trainable)
Source: PyTorch Transfer Learning Tutorial (https://docs.pytorch.org/tutorials/beginner/transfer_learning_tutorial.html)

```python
model_ft = models.resnet18(weights='IMAGENET1K_V1')
num_ftrs = model_ft.fc.in_features
model_ft.fc = nn.Linear(num_ftrs, 2)

criterion = nn.CrossEntropyLoss()

optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)

# Decay LR by a factor of 0.1 every 7 epochs
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)

model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,
                       num_epochs=25)
```

### B. PyTorch: ConvNet as fixed feature extractor (freeze backbone)
Source: PyTorch Transfer Learning Tutorial (same URL)

```python
model_conv = torchvision.models.resnet18(weights='IMAGENET1K_V1')
for param in model_conv.parameters():
    param.requires_grad = False

num_ftrs = model_conv.fc.in_features
model_conv.fc = nn.Linear(num_ftrs, 2)

criterion = nn.CrossEntropyLoss()

optimizer_conv = optim.SGD(model_conv.fc.parameters(), lr=0.001, momentum=0.9)

exp_lr_scheduler = lr_scheduler.StepLR(optimizer_conv, step_size=7, gamma=0.1)

model_conv = train_model(model_conv, criterion, optimizer_conv,
                         exp_lr_scheduler, num_epochs=25)
```

### C. PyTorch: Freeze only some layers using `children()`
Source: PyTorch Forums (https://discuss.pytorch.org/t/how-the-pytorch-freeze-network-in-some-layers-only-the-rest-of-the-training/7088)

```python
model_ft = models.resnet50(pretrained=True)
ct = 0
for child in model_ft.children():
    ct += 1
    if ct < 7:
        for param in child.parameters():
            param.requires_grad = False
```

### D. PyTorch: Ensure optimizer only sees trainable parameters
Source: PyTorch GitHub issue #679 (https://github.com/pytorch/pytorch/issues/679)

```python
optimizer = torch.optim.SGD(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=1e-3
)
```

### E. Hugging Face Transformers: exact LR schedule definitions (linear + warmup)
Source: `transformers/optimization.py` (https://github.com/huggingface/transformers/blob/main/src/transformers/optimization.py)

- Warmup phase (`current_step < num_warmup_steps`):
  - `lr_multiplier = current_step / max(1, num_warmup_steps)`
- Decay phase:
  - `lr_multiplier = max(0.0, (num_training_steps - current_step) / max(1, num_training_steps - num_warmup_steps))`
- API:
  - `get_linear_schedule_with_warmup(optimizer, num_warmup_steps, num_training_steps, last_epoch=-1)`

### F. Hugging Face Trainer: selecting cosine scheduler via `TrainingArguments`
Source: HF forum thread (https://discuss.huggingface.co/t/using-cosine-lr-scheduler-via-trainingarguments-in-trainer/14783)

- To use cosine scheduler in `Trainer`, set:
  - `lr_scheduler_type` to `"cosine"` (as stated in the thread).

### G. STILTs: workflow and example command (fine-tuning from an MNLI model)
Source: `bert_on_stilts` README (https://github.com/zphang/bert_on_stilts/blob/master/README.md)

```bash
export PRETRAINED_MODEL_PATH=/path/to/mnli.p
export TASK=rte
export OUTPUT_PATH=rte_output
python glue/train.py \
  --task_name $TASK \
  --do_train --do_val --do_test --do_val_history \
  --do_save \
  --do_lower_case \
  --bert_model bert-large-uncased \
  --bert_load_path $PRETRAINED_MODEL_PATH \
  --bert_load_mode model_only \
  --bert_save_mode model_all \
  --train_batch_size 24 \
  --learning_rate 2e-5 \
  --output_dir $OUTPUT_PATH
```

### H. Early stopping (Keras) with explicit parameters
Source: W&B report (https://wandb.ai/ayush-thakur/huggingface/reports/Examples-of-Early-Stopping-in-HuggingFace-Transformers--Vmlldzo0MzE2MTM)

```python
early_stopper = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)
model.fit(trainloader, epochs=10, validation_data=validloader, callbacks=[early_stopper])
```

---

## Comparisons & Trade-offs

- **Fine-tuning vs fixed feature extractor (PyTorch tutorial ResNet-18 example)**
  - Accuracy:
    - Fine-tuning all params: best val Acc **0.934641** (PyTorch tutorial)
    - Fixed feature extractor: best val Acc **0.947712** (PyTorch tutorial)
  - Time:
    - Fine-tuning run: **0m 37s**
    - Fixed feature extractor run: **0m 28s**
    - CPU expectation: fixed feature extractor takes **about half the time** vs fine-tuning scenario (PyTorch tutorial)
  - Trade-off described: freezing avoids gradient computation for most layers (faster), but forward pass still required. (PyTorch tutorial)

- **Feature extraction vs fine-tuning (3D ResNet-50 backbone, Table 5)**
  - Feature extraction (frozen) vs fine-tuning (unfrozen last block):
    - Accuracy: **85.2 ± 0.6** vs **89.8 ± 0.5**
    - F1: **83.5 ± 0.5** vs **88.6 ± 0.4**
    - Loss: **1.20 ± 0.04** vs **0.85 ± 0.03**
    - Training duration: **≈10 epochs** vs **≈15 epochs**
    - Compute cost: **Low** vs **High**  
    (https://pmc.ncbi.nlm.nih.gov/articles/PMC12615596/table/Tab5/)

- **STILTs vs no STILTs (GLUE)**
  - Repo claim: **82.0 vs 80.5** GLUE. (bert_on_stilts README)
  - Paper claim: **81.8** GLUE and **+1.4** over BERT. (Phang et al., 2018 ar5iv)
  - Discrepancy note: README and paper report slightly different absolute GLUE scores (82.0 vs 81.8), but both indicate improvement over a non-STILTs baseline. (Both sources above)

- **Classic early stopping vs GradES**
  - Classic early stopping requires validation forward passes; paper notes this is expensive and leads practitioners to validate infrequently (“typically every few thousand training steps”). (GradES arXiv HTML)
  - GradES reports:
    - Up to **6.79×** speedup in a cited example (907s vs 6,155s) while keeping accuracy close (67.30% vs 67.37%). (GradES arXiv HTML)

- **TAPT efficiency via selective parameter training**
  - Training only BERT embedding layer during TAPT: **78% fewer parameters trained** while achieving “comparable performance” (as claimed by the paper). (Ladkat et al., 2022, https://arxiv.org/abs/2209.12943)

---

## Architecture & Design Rationale

- **Why freezing speeds training**
  - PyTorch tutorial explains that when most parameters have `requires_grad=False`, gradients “don’t need to be computed for most of the network,” reducing compute; forward still runs. (PyTorch transfer learning tutorial)

- **Why pretrained CNN features transfer**
  - Note_08 describes that early ConvNet layers learn general features (e.g., “edge detectors or color blob detectors”) useful across tasks, while later layers become more specific to the original dataset classes (e.g., ImageNet dog-breed distinctions). (Note_08.pdf URL)
  - Practical implication in the same note: use pretrained ConvNet as fixed feature extractor by removing last FC layer and training a new classifier on extracted features (e.g., AlexNet **4096-D** “CNN codes”). (Note_08.pdf URL)

- **Why fine-tuning uses smaller learning rates in some transfer setups**
  - Pulkit et al. (2014) describe fine-tuning with SGD starting at **0.001**, explicitly stated as **1/10-th** the initial ImageNet training LR, “to prevent clobbering the CNN’s initialization to control overfitting,” and decaying by **10× every 20,000 iterations**. (http://arxiv.org/pdf/1407.1610.pdf)

- **Why AdamW differs from L2 regularization (conceptual rationale)**
  - The AdamW article explains that Adam breaks the equivalence between L2 regularization and weight decay due to adaptive learning rates; AdamW “decouples weight decay from the gradient-based update.” (mbrenndoerfer.com article, https://mbrenndoerfer.com/writing/adamw-optimizer-decoupled-weight-decay)
  - Note: This source is an explanatory article rather than an official framework doc; treat as secondary guidance.

- **Why EWC targets “important” parameters**
  - EWC adds a quadratic penalty weighted by Fisher diagonal elements \(F^{i,i}\), so parameters with higher Fisher (proxy for importance) are penalized more for moving away from old-task optimum \(\hat{\theta}_{old}\). (https://arxiv.org/html/2502.11756v1; OpenReview FIM definition PDF)

---

## Common Questions & Answers

- **Q: How do I freeze a pretrained model in PyTorch so it doesn’t compute gradients?**  
  - Set `param.requires_grad = False` for the parameters you want frozen; PyTorch tutorial states this prevents gradients from being computed in `backward()`. (PyTorch transfer learning tutorial)

- **Q: If I freeze parameters, do I also need to change the optimizer?**  
  - PyTorch core devs recommend explicitly filtering optimizer parameters to those with `requires_grad=True`, e.g.  
    `optimizer.SGD(filter(lambda p: p.requires_grad, model.parameters()), lr=1e-3)`. (PyTorch GitHub issue #679)

- **Q: What’s the difference between “fine-tuning” and “fixed feature extractor” in the PyTorch tutorial?**  
  - Fine-tuning: optimizer is constructed over `model_ft.parameters()` (all parameters).  
  - Fixed feature extractor: set all `requires_grad=False`, replace final FC, and optimize only `model_conv.fc.parameters()`. (PyTorch transfer learning tutorial)

- **Q: How much faster is feature extraction compared to fine-tuning in the PyTorch example?**  
  - The tutorial states on CPU it takes “about half the time” vs fine-tuning, because gradients aren’t computed for most layers. (PyTorch transfer learning tutorial)

- **Q: What exactly does `get_linear_schedule_with_warmup` do in Transformers?**  
  - It creates an LR schedule that increases linearly from **0 to the optimizer’s initial LR** during warmup, then decreases linearly from initial LR to **0** by `num_training_steps`. (Transformers `optimization.py`)

- **Q: How do I select cosine LR scheduling in Hugging Face `Trainer`?**  
  - In `TrainingArguments`, set `lr_scheduler_type` to `"cosine"` (per HF forum guidance). (HF forum thread: https://discuss.huggingface.co/t/using-cosine-lr-scheduler-via-trainingarguments-in-trainer/14783)

- **Q: What is STILTs and what gains does it report?**  
  - STILTs = supplementary training on an intermediate labeled task before target fine-tuning. (Phang et al., 2018 ar5iv)  
  - Reported GLUE improvements:
    - README: **82.0 vs 80.5** (bert_on_stilts README)
    - Paper: **81.8** and **+1.4** over BERT (Phang et al., 2018 ar5iv)  
  - Note discrepancy in absolute score between README and paper; both indicate improvement.

- **Q: What is the EWC penalty term (formula) used to reduce catastrophic forgetting?**  
  - \(\ell_{EWC}(\theta)=\ell_{new}(\theta)+\frac{\lambda}{2}\sum_i F_{old}^{i,i}(\theta^i-\hat{\theta}_{old}^i)^2\). (https://arxiv.org/html/2502.11756v1)

- **Q: Is there evidence that fine-tuning improves accuracy vs feature extraction?**  
  - In a 3D ResNet-50 comparison, fine-tuning the last block improved test accuracy from **85.2 ± 0.6** to **89.8 ± 0.5** and F1 from **83.5 ± 0.5** to **88.6 ± 0.4**, with longer training (**≈15 vs ≈10 epochs**) and higher compute cost. (Table 5, https://pmc.ncbi.nlm.nih.gov/articles/PMC12615596/table/Tab5/)

- **Q: Can early stopping be configured with specific patience and restoring best weights?**  
  - Example shown: `EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)`. (W&B report URL)

- **Q: Why might classic early stopping be expensive for large transformers, and what’s an alternative?**  
  - GradES paper states validation-based early stopping is costly because each validation step requires full forward passes through all layers for all validation samples; practitioners validate infrequently (“typically every few thousand training steps”). (GradES arXiv HTML)  
  - GradES alternative: freeze components when gradient-change magnitude falls below threshold \(\tau\); reports time reductions **35–66%** and FLOPs reductions **45–71%** vs baseline full fine-tuning. (GradES arXiv HTML)