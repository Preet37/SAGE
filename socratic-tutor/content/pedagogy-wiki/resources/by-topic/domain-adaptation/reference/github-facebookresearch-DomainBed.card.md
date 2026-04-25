# Card: DomainBed DG Experiment Surface (CLI, registries, sweeps)
**Source:** https://github.com/facebookresearch/DomainBed  
**Role:** code | **Need:** API_REFERENCE  
**Anchor:** Configuration/implementation surface for domain generalization experiments (datasets, algorithms, hparams registry, training + sweep scripts, model selection).

## Key Content
- **Purpose:** PyTorch suite for benchmarking **domain generalization** (per *In Search of Lost Domain Generalization*, arXiv:2007.01434). Official results for **commit `7df6f06`** provided in `domainbed/results/2020_10_06_7df6f06/results.tex`.
- **Algorithm registry (`domainbed/algorithms.py`):** includes ERM, IRM, GroupDRO, Mixup, MTL, MLDG, MMD, CORAL, DANN, CDANN, SagNet, ARM, VREx, RSC, SD, AND-Mask, IGA, Fish, SelfReg, SAND-mask, Fishr, TRM, IB-ERM, IB-IRM, CAD/CondCAD, Transfer, CausIRL (CORAL or MMD), EQRM, RDM, ADRMX, ERM++, URM.
- **Dataset registry (`domainbed/datasets.py`):** RotatedMNIST, ColoredMNIST, VLCS, PACS, Office-Home, TerraIncognita (subset), DomainNet, SVIRO (subset), WILDS FMoW, WILDS Camelyon17, Spawrious. Custom image datasets supported via folder structure: `dataset/domain/class/image.xyz`.
- **Backbones + hparams:** implementations use **ResNet50 / ResNet18**; hyperparameter grids defined in `domainbed/hparams_registry.py`.
- **Model selection methods (`domainbed/model_selection.py`):**
  - `IIDAccuracySelectionMethod`: validation subset from **training domains**.
  - `LeaveOneOutSelectionMethod`: validation subset from a **held-out domain** (not train/test).
  - `OracleSelectionMethod`: validation subset from the **test domain**.
- **Core CLI workflows:**
  - Download: `python3 -m domainbed.scripts.download --data_dir=./domainbed/data`
  - Train: `python3 -m domainbed.scripts.train --data_dir=... --algorithm IGA --dataset ColoredMNIST --test_env 2`
  - Sweep launch: `python -m domainbed.scripts.sweep launch --data_dir=... --output_dir=... --command_launcher MyLauncher`
  - Sweep scale defaults: “**tens of thousands**” models = (all algos × all datasets × **3 trials** × **20 hparam** samples). Can restrict via `--algorithms`, `--datasets`, `--n_hparams`, `--n_trials`.
  - Results: `python -m domainbed.scripts.collect_results --input_dir=...`
  - Cleanup/retry: `python -m domainbed.scripts.sweep delete_incomplete` then relaunch with identical args.
- **Tests:** `python -m unittest discover`; with datasets: `DATA_DIR=/path python -m unittest discover`.

## When to surface
Use when students ask how to *run/replicate DG experiments*, choose *train/val/test domain splits* (`test_env`, selection methods), or set up *sweeps/hyperparameter sampling* in DomainBed.