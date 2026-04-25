# Card: TRL DPOTrainer / DPOConfig API (losses, β, reference model)
**Source:** https://huggingface.co/docs/trl/main/en/dpo_trainer  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative parameter names/semantics for `DPOTrainer`/`DPOConfig` in TRL (β/temperature, reference model handling, loss variants)

## Key Content
- **DPO objective (core loss):** For prompt \(x\), preferred completion \(y_w\) (chosen), dispreferred \(y_l\) (rejected), policy \(\pi_\theta\), reference \(\pi_{\text{ref}}\), sigmoid \(\sigma\), and hyperparameter \(\beta\):  
  \[
  \mathcal{L}_{\text{DPO}} = -\log \sigma\Big(\beta\big[(\log \pi_\theta(y_w|x)-\log \pi_\theta(y_l|x))-(\log \pi_{\text{ref}}(y_w|x)-\log \pi_{\text{ref}}(y_l|x))\big]\Big)
  \]
  (Doc “Computing the loss”). **Rationale:** aligns to preferences without an explicit reward model; typically suppresses rejected likelihood.
- **Dataset format (preference pairs):** examples must contain `prompt` + `chosen` + `rejected` (standard text or conversational messages). Conversational datasets auto-apply chat template.
- **Reference model handling (`DPOTrainer(ref_model=...)`):**
  - If `ref_model` provided: used directly for reference log-probs.
  - If `None`: reference is the **initial policy** (model state before DPO training).
- **Key `DPOConfig` defaults:** `loss_type=["sigmoid"]`, `beta=0.1`, `max_length=1024`, `truncation_mode="keep_start"`, `disable_dropout=True`, `learning_rate=1e-6`, `logging_steps=10`, `gradient_checkpointing=True`, `precompute_ref_log_probs=False`, `sync_ref_model=False`.
- **Loss variants (`loss_type`):** `"sigmoid"`, `"hinge"`, `"ipo"`, `"exo_pair"` (requires `label_smoothing>0`, rec. `1e-3`), `"nca_pair"`, `"robust"` (`label_smoothing` in \([0,0.5)\)), `"bco_pair"`, `"sppo_hard"`, `"aot"`, `"aot_unpaired"`, `"apo_zero"`, `"apo_down"`, `"discopop"` (uses `discopop_tau`, default `0.05`), `"sft"`.
- **Multi-loss (MPO-style):** `loss_type=[...]` + `loss_weights=[...]` (example: `["sigmoid","bco_pair","sft"]` with `[0.8,0.2,1.0]`).
- **Constraints:** `sync_ref_model=True` incompatible with `precompute_ref_log_probs=True`; `precompute_ref_log_probs` not supported with `IterableDataset`; `use_weighting=True` not supported with AOT losses.
- **Logged metrics:** `rewards/chosen = logπθ - logπref`, `rewards/rejected`, `rewards/margins`, `rewards/accuracies`, plus `logps/*`, `logits/*`, `entropy`, `mean_token_accuracy`, etc.
- **VLM note:** set `DPOConfig(max_length=None)` to avoid truncating image tokens.

## When to surface
Use when students ask how TRL implements DPO (exact loss, β meaning), how the reference model is chosen/synced, what `loss_type` options mean, or which `DPOConfig` defaults/constraints apply.