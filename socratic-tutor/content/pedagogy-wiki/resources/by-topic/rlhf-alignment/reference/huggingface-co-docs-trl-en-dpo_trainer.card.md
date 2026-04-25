# Card: TRL DPOTrainer (API + dataset schema + key knobs)
**Source:** https://huggingface.co/docs/trl/en/dpo_trainer  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Authoritative DPOTrainer configuration (β/temperature, reference model handling, loss variants) and expected dataset schema for preference pairs

## Key Content
- **DPO objective (core idea):** train on preference pairs (prompt *x*, preferred completion *y_w*, dispreferred *y_l*) to increase the **log-likelihood margin** of *y_w* vs *y_l* **relative to a reference model** π_ref, without an explicit reward model. Uses a **classification-style loss** with sigmoid; **β** controls preference strength / deviation from reference.  
  - Implicit rewards logged:  
    - `rewards/chosen = β * (log πθ(y_w|x) − log πref(y_w|x))`  
    - `rewards/rejected = β * (log πθ(y_l|x) − log πref(y_l|x))`  
    - `rewards/margins = rewards/chosen − rewards/rejected`
- **Expected dataset (preference format):** must contain `chosen` and `rejected`, optionally `prompt` (recommended).  
  - Standard explicit: `{"prompt": "...", "chosen": "...", "rejected": "..."}`  
  - Standard implicit: `{"chosen": "...", "rejected": "..."}`  
  - Conversational explicit: `prompt/chosen/rejected` are lists of `{role, content}`; chat template auto-applied.
- **Reference model handling (DPOTrainer `ref_model`):**
  - If `ref_model` provided: used directly for reference log-probs.
  - If `None`: reference is the **initial policy** (model state before DPO starts).
- **Key config defaults (DPOConfig):** `beta=0.1`, `loss_type=["sigmoid"]`, `max_length=1024`, `truncation_mode="keep_start"`, `learning_rate=1e-6`, `gradient_checkpointing=True`, `disable_dropout=True`, `precompute_ref_log_probs=False`, `sync_ref_model=False`.
- **Loss variants (`loss_type`):** `"sigmoid"` (default), `"hinge"` (β is reciprocal margin), `"ipo"` (β is τ), `"exo_pair"` (requires `label_smoothing>0`, rec. `1e-3`), `"robust"` (`label_smoothing` in `[0,0.5)`), `"aot"`/`"aot_unpaired"`, `"apo_zero"`/`"apo_down"`, `"discopop"` (temperature `discopop_tau=0.05`), `"bco_pair"`, `"sppo_hard"`, `"sft"`. Supports **multi-loss** lists + `loss_weights` (e.g., MPO: `["sigmoid","bco_pair","sft"]` with `[0.8,0.2,1.0]`).
- **Constraints:** `sync_ref_model=True` incompatible with `precompute_ref_log_probs=True`; `precompute_ref_log_probs` not supported with `IterableDataset`; `use_weighting=True` not supported with AOT losses.

## When to surface
Use when students ask how to structure preference-pair datasets for DPO, how TRL chooses/updates the reference model, what β/temperature means, or which `loss_type`/config defaults and incompatibilities apply in `DPOTrainer`.