# Source: https://github.com/facebookresearch/dinov2/blob/main/README.md
# Title: dinov2/README.md at main · facebookresearch/dinov2
# Fetched via: trafilatura
# Date: 2026-04-09

🆕 [2025-12-18] Added support for loading XRay-DINO backbone following [Advancing human-centric AI for robust X-ray analysis through holistic self-supervised learning](https://arxiv.org/pdf/2405.01469), more details are [here](#pretrained-backbone-xray-dino)
🆕 [2025-12-16] Added Channel-Adaptive DINO code following [Scaling Channel-Adaptive Self-Supervised Learning](https://openreview.net/forum?id=pT8sgtRVAf), more details are [here](#dinov2-for-biology)
🆕 [2025-12-16] Added Cell-DINO code following [Cell-DINO: Self-Supervised Image-based Embeddings for Cell Fluorescent Microscopy](to appear in Plos One Computational Biology), more details are [here](#dinov2-for-biology)
[2025-08-14] Please check out the more recent [DINOv3](https://github.com/facebookresearch/dinov3) effort continuing this line of work.
[2025-06-11] Added dino.txt inference code, following [DINOv2 Meets Text: A Unified Framework for Image- and Pixel-Level Vision-Language Alignment](https://arxiv.org/abs/2412.16334).
[2023-10-26] Added DINOv2 backbones with registers, following [Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588).
Maxime Oquab, Timothée Darcet, Théo Moutakanni, Huy V. Vo, Marc Szafraniec, Vasil Khalidov, Patrick Labatut, Armand Joulin, Piotr Bojanowski
[[ Paper #1](https://arxiv.org/abs/2304.07193)]
[] [](https://arxiv.org/abs/2309.16588)
Paper #2
[] [](https://ai.facebook.com/blog/dino-v2-computer-vision-self-supervised-learning/)
Blog
[] [](https://dinov2.metademolab.com)
Demo
[]](#citing-dinov2)
BibTeX
PyTorch implementation and pretrained models for DINOv2. For details, see the papers: [DINOv2: Learning Robust Visual Features without Supervision](https://arxiv.org/abs/2304.07193) and [Vision Transformers Need Registers](https://arxiv.org/abs/2309.16588).
DINOv2 models produce high-performance visual features that can be directly employed with classifiers as simple as linear layers on a variety of computer vision tasks; these visual features are robust and perform well across domains without any requirement for fine-tuning. The models were pretrained on a dataset of 142 M images without using any labels or annotations.
video-reference+dinov2.mp4
| model | # of params |
with registers |
ImageNet k-NN |
ImageNet linear |
download |
|---|---|---|---|---|---|
| ViT-S/14 distilled | 21 M | ❌ | 79.0% | 81.1% |
|
[backbone only](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_reg4_pretrain.pth)[backbone only](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_pretrain.pth)[backbone only](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_reg4_pretrain.pth)[backbone only](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_pretrain.pth)[backbone only](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_reg4_pretrain.pth)[backbone only](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_pretrain.pth)[backbone only](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_reg4_pretrain.pth)Please follow the instructions [here](https://pytorch.org/get-started/locally/) to install PyTorch (the only required dependency for loading the model). Installing PyTorch with CUDA support is strongly recommended.
A corresponding [model card](/facebookresearch/dinov2/blob/main/MODEL_CARD.md) is included in the repository.
import torch
# DINOv2
dinov2_vits14 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14')
dinov2_vitb14 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14')
dinov2_vitl14 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14')
dinov2_vitg14 = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitg14')
# DINOv2 with registers
dinov2_vits14_reg = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14_reg')
dinov2_vitb14_reg = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14_reg')
dinov2_vitl14_reg = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14_reg')
dinov2_vitg14_reg = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitg14_reg')
Request for downloading the model is here:
[https://ai.meta.com/resources/models-and-libraries/raydino-downloads/](https://ai.meta.com/resources/models-and-libraries/raydino-downloads/)
After filling the form, you will get an email with a temporary link. You can either download it using wget
and indicate the checkpoint path in your local filesystem, or you can directly use the URL from the email in the following code:
import torch
REPO_DIR = <PATH/TO/A/LOCAL/DIRECTORY/WHERE/THE/DINOV2/REPO/WAS/CLONED>
xray_dino_vitl16 = torch.hub.load(REPO_DIR, 'xray_dino_vitl16', source='local', weights=<CHECKPOINT/URL/OR/PATH>)
License Model weights are released under the FAIR Noncommercial Research License. See LICENSE_XRAY_DINO_MODEL for additional details.
| backbone | with registers |
download |
|---|---|---|
| ImageNet | ||
| ViT-S/14 distilled | ❌ |
linear head (
|
[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_reg4_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_reg4_linear4_head.pth))[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_linear4_head.pth))[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_reg4_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_reg4_linear4_head.pth))[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_linear4_head.pth))[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_reg4_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_reg4_linear4_head.pth))[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_linear4_head.pth))[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_lreg4_inear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_reg4_linear4_head.pth))The (full) classifier models can be loaded via PyTorch Hub:
import torch
# DINOv2
dinov2_vits14_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14_lc')
dinov2_vitb14_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14_lc')
dinov2_vitl14_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14_lc')
dinov2_vitg14_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitg14_lc')
# DINOv2 with registers
dinov2_vits14_reg_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14_reg_lc')
dinov2_vitb14_reg_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitb14_reg_lc')
dinov2_vitl14_reg_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14_reg_lc')
dinov2_vitg14_reg_lc = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitg14_reg_lc')
| backbone | download head | |
|---|---|---|
| NYUd | KITTI | |
| ViT-S/14 distilled |
linear (
|
[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_kitti_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_kitti_linear4_head.pth)),[DPT](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_kitti_dpt_head.pth)[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_nyu_linear4_head.pth)),[DPT](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_nyu_dpt_head.pth)[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_kitti_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_kitti_linear4_head.pth)),[DPT](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_kitti_dpt_head.pth)[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_nyu_linear4_head.pth)),[DPT](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_nyu_dpt_head.pth)[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_kitti_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_kitti_linear4_head.pth)),[DPT](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_kitti_dpt_head.pth)[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_nyu_linear4_head.pth)),[DPT](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_nyu_dpt_head.pth)[1 layer](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_kitti_linear_head.pth),[4 layers](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_kitti_linear4_head.pth)),[DPT](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_kitti_dpt_head.pth)| backbone | download model | download head | |
|---|---|---|---|
| ADE20K | ADE20K | VOC2012 | |
| ViT-S/14 distilled |
|
[linear](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_voc2012_linear_head.pth),[multi-scale](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_voc2012_ms_head.pth)[linear](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_ade20k_linear_head.pth),[multi-scale](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_ade20k_ms_head.pth)[linear](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_voc2012_linear_head.pth),[multi-scale](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_voc2012_ms_head.pth)[linear](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_ade20k_linear_head.pth),[multi-scale](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_ade20k_ms_head.pth)[linear](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_voc2012_linear_head.pth),[multi-scale](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_voc2012_ms_head.pth)[Mask2Former](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_ade20k_m2f.pth)[linear](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_ade20k_linear_head.pth),[multi-scale](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_ade20k_ms_head.pth)[linear](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_voc2012_linear_head.pth),[multi-scale](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_voc2012_ms_head.pth)| backbone | with registers |
download |
|---|---|---|
| ViT-L/14 distilled | ✅ |
|
The (full) dino.txt model can be loaded via PyTorch Hub:
import torch
# DINOv2
dinov2_vitl14_reg4_dinotxt_tet1280d20h24l = torch.hub.load('facebookresearch/dinov2', 'dinov2_vitl14_reg4_dinotxt_tet1280d20h24l')
The training and evaluation code requires PyTorch 2.0 and [xFormers](https://github.com/facebookresearch/xformers) 0.0.18 as well as a number of other 3rd party packages. Note that the code has only been tested with the specified versions and also expects a Linux environment. To setup all the required dependencies for training and evaluation, please follow the instructions below:
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) (Recommended) - Clone the repository and then create and activate a dinov2
conda environment using the provided environment definition:
conda env create -f conda.yaml
conda activate dinov2
[pip](https://pip.pypa.io/en/stable/getting-started/) - Clone the repository and then use the provided requirements.txt
to install the dependencies:
pip install -r requirements.txt
For dense tasks (depth estimation and semantic segmentation), there are additional dependencies (specific versions of mmcv
and mmsegmentation
) which are captured in the extras
dependency specifications:
[conda](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html) (Recommended):
conda env create -f conda-extras.yaml
conda activate dinov2-extras
[pip](https://pip.pypa.io/en/stable/getting-started/):
pip install -r requirements.txt -r requirements-extras.txt
The root directory of the dataset should hold the following contents:
<ROOT>/test/ILSVRC2012_test_00000001.JPEG
<ROOT>/test/[..]
<ROOT>/test/ILSVRC2012_test_00100000.JPEG
<ROOT>/train/n01440764/n01440764_10026.JPEG
<ROOT>/train/[...]
<ROOT>/train/n15075141/n15075141_9993.JPEG
<ROOT>/val/n01440764/ILSVRC2012_val_00000293.JPEG
<ROOT>/val/[...]
<ROOT>/val/n15075141/ILSVRC2012_val_00049174.JPEG
<ROOT>/labels.txt
The provided dataset implementation expects a few additional metadata files to be present under the extra directory:
<EXTRA>/class-ids-TRAIN.npy
<EXTRA>/class-ids-VAL.npy
<EXTRA>/class-names-TRAIN.npy
<EXTRA>/class-names-VAL.npy
<EXTRA>/entries-TEST.npy
<EXTRA>/entries-TRAIN.npy
<EXTRA>/entries-VAL.npy
These metadata files can be generated (once) with the following lines of Python code:
from dinov2.data.datasets import ImageNet
for split in ImageNet.Split:
dataset = ImageNet(split=split, root="<ROOT>", extra="<EXTRA>")
dataset.dump_extra()
Note that the root and extra directories do not have to be distinct directories.
Please adapt the [dataset class](/facebookresearch/dinov2/blob/main/dinov2/data/datasets/image_net_22k.py) to match your local setup.
dinov2
package should be included in the Python module search path, i.e. simply prefix the command to run with PYTHONPATH=.
.
Run DINOv2 training on 4 A100-80GB nodes (32 GPUs) in a SLURM cluster environment with submitit:
python dinov2/run/train/train.py \
--nodes 4 \
--config-file dinov2/configs/train/vitl16_short.yaml \
--output-dir <PATH/TO/OUTPUT/DIR> \
train.dataset_path=ImageNet:split=TRAIN:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET>
Training time is approximately 1 day and the resulting checkpoint should reach 81.6% on k-NN eval and 82.9% on linear eval.
The training code saves the weights of the teacher in the eval
folder every 12500 iterations for evaluation.
Run DINOv2 training on 12 A100-80GB nodes (96 GPUs) in a SLURM cluster environment with submitit:
python dinov2/run/train/train.py \
--nodes 12 \
--config-file dinov2/configs/train/vitl14.yaml \
--output-dir <PATH/TO/OUTPUT/DIR> \
train.dataset_path=ImageNet22k:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET>
Training time is approximately 3.3 days and the resulting checkpoint should reach 82.0% on k-NN eval and 84.5% on linear eval.
The training code saves the weights of the teacher in the eval
folder every 12500 iterations for evaluation.
The training code regularly saves the teacher weights. In order to evaluate the model, run the following evaluation on a single node:
python dinov2/run/eval/knn.py \
--config-file <PATH/TO/OUTPUT/DIR>/config.yaml \
--pretrained-weights <PATH/TO/OUTPUT/DIR>/eval/training_24999/teacher_checkpoint.pth \
--output-dir <PATH/TO/OUTPUT/DIR>/eval/training_24999/knn \
--train-dataset ImageNet:split=TRAIN:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET> \
--val-dataset ImageNet:split=VAL:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET>
python dinov2/run/eval/log_regression.py \
--config-file <PATH/TO/OUTPUT/DIR>/config.yaml \
--pretrained-weights <PATH/TO/OUTPUT/DIR>/eval/training_24999/teacher_checkpoint.pth \
--output-dir <PATH/TO/OUTPUT/DIR>/eval/training_24999/logreg \
--train-dataset ImageNet:split=TRAIN:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET> \
--val-dataset ImageNet:split=VAL:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET>
python dinov2/run/eval/linear.py \
--config-file <PATH/TO/OUTPUT/DIR>/config.yaml \
--pretrained-weights <PATH/TO/OUTPUT/DIR>/eval/training_24999/teacher_checkpoint.pth \
--output-dir <PATH/TO/OUTPUT/DIR>/eval/training_24999/linear \
--train-dataset ImageNet:split=TRAIN:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET> \
--val-dataset ImageNet:split=VAL:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET>
We release the weights from evaluating the different models:
| model | with registers |
ImageNet top-1 |
linear evaluation |
|---|---|---|---|
| ViT-S/14 distilled | ❌ | 81.1% |
|
[linear head weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vits14/dinov2_vits14_reg4_linear_head.pth)[linear head weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_linear_head.pth)[linear head weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitb14/dinov2_vitb14_reg4_linear_head.pth)[linear head weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_linear_head.pth)[linear head weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitl14/dinov2_vitl14_reg4_linear_head.pth)[linear head weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_linear_head.pth)[linear head weights](https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_reg4_linear_head.pth)The performance of the provided pretrained model weights can be evaluated as follows on ImageNet-1k:
python dinov2/run/eval/linear.py \
--config-file dinov2/configs/eval/vitg14_pretrain.yaml \
--pretrained-weights https://dl.fbaipublicfiles.com/dinov2/dinov2_vitg14/dinov2_vitg14_pretrain.pth \
--train-dataset ImageNet:split=TRAIN:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET> \
--val-dataset ImageNet:split=VAL:root=<PATH/TO/DATASET>:extra=<PATH/TO/DATASET>
A few notebooks are provided to help the community leverage the models and code:
[Depth estimation](https://github.com/facebookresearch/dinov2/blob/main/notebooks/depth_estimation.ipynb)- How to load and use the depth heads in combination with a matching backbone via mmcv[Semantic segmentation](https://github.com/facebookresearch/dinov2/blob/main/notebooks/semantic_segmentation.ipynb)- How to load and use the segmentation heads in combination with a matching backbone via mmcv, and also how to load and use the Mask2Former-based segmentation model trained on ADE20K
DINOv2 code and model weights are released under the Apache License 2.0. See [LICENSE](/facebookresearch/dinov2/blob/main/LICENSE) for additional details.
See [contributing](/facebookresearch/dinov2/blob/main/CONTRIBUTING.md) and the [code of conduct](/facebookresearch/dinov2/blob/main/CODE_OF_CONDUCT.md).
If you find this repository useful, please consider giving a star ⭐ and citation 🦖:
@misc{oquab2023dinov2,
title={DINOv2: Learning Robust Visual Features without Supervision},
author={Oquab, Maxime and Darcet, Timothée and Moutakanni, Theo and Vo, Huy V. and Szafraniec, Marc and Khalidov, Vasil and Fernandez, Pierre and Haziza, Daniel and Massa, Francisco and El-Nouby, Alaaeldin and Howes, Russell and Huang, Po-Yao and Xu, Hu and Sharma, Vasu and Li, Shang-Wen and Galuba, Wojciech and Rabbat, Mike and Assran, Mido and Ballas, Nicolas and Synnaeve, Gabriel and Misra, Ishan and Jegou, Herve and Mairal, Julien and Labatut, Patrick and Joulin, Armand and Bojanowski, Piotr},
journal={arXiv:2304.07193},
year={2023}
}
@misc{darcet2023vitneedreg,
title={Vision Transformers Need Registers},
author={Darcet, Timothée and Oquab, Maxime and Mairal, Julien and Bojanowski, Piotr},
journal={arXiv:2309.16588},
year={2023}
}
@misc{jose2024dinov2meetstextunified,
title={DINOv2 Meets Text: A Unified Framework for Image- and Pixel-Level Vision-Language Alignment},
author={Cijo Jose and Théo Moutakanni and Dahyun Kang and Federico Baldassarre and Timothée Darcet and Hu Xu and Daniel Li and Marc Szafraniec and Michaël Ramamonjisoa and Maxime Oquab and Oriane Siméoni and Huy V. Vo and Patrick Labatut and Piotr Bojanowski},
journal={arXiv:2412.16334},
year={2024}
}
The contents of the source code contained in the cell_dino folders, including the code and model weights, are intended for research use only. It is not for use in medical procedures, including any diagnostics, treatment, or curative applications. Do not use this model for any clinical purpose or as a substitute for professional medical judgement.
Alice V. De Lorenci, Seungeun Yi, Théo Moutakanni, Piotr Bojanowski, Camille Couprie, Juan C. Caicedo, Wolfgang M. Pernice,
with special thanks to Elouan Gardes for his contributions to the codebase.
Théo Moutakanni, Camille Couprie, Seungeun Yi, Elouan Gardes, Piotr Bojanowski, Hugo Touvron, Michael Doron, Zitong S. Chen, Nikita Moshkov, Mathilde Caron, Armand Joulin, Wolfgang M. Pernice, Juan C. Caicedo
to appear soon.
ℹ️ Please follow the link provided below to get access to all the model weights: once accepted, an e-mail will be sent with the complete list of URLs pointing to all the available model weights. These URLs can then be used to either:
- download the model or adapter weights to a local filesystem and point
torch.hub.load()
to these local weights via thepretrained_path
parameters, or - directly invoke
torch.hub.load()
to download and load a backbone from its URL via also thepretrained_url
parameter.
Download link:
[https://ai.meta.com/resources/models-and-libraries/cell-dino-downloads/](https://ai.meta.com/resources/models-and-libraries/cell-dino-downloads/)
import torch
REPO_DIR = <PATH/TO/A/LOCAL/DIRECTORY/WHERE/THE/DINOV2/REPO/WAS/CLONED>
# You can either download the URL link first, then load:
cell_dino_vits8 = torch.hub.load(REPO_DIR, 'cell_dino_cp_vits8', source='local', pretrained_path=<CHECKPOINT/PATH>)
# Or directly download the URL while using `torch.hub.load`:
cell_dino_vits8 = torch.hub.load(REPO_DIR, 'cell_dino_cp_vits8', source='local', pretrained_url=<CHECKPOINT/URL>)
# Similarily for other models:
cell_dino_vitl16_hpa_sc = torch.hub.load(REPO_DIR, 'cell_dino_hpa_vitl16', source='local', pretrained_path=<CHECKPOINT/PATH>)
cell_dino_vitl16_hpa_fov = torch.hub.load(REPO_DIR, 'cell_dino_hpa_vitl16', source='local', pretrained_path=<CHECKPOINT/PATH>)
channel_adaptive_dino_vitl16 = torch.hub.load(REPO_DIR, 'channel_adaptive_dino_vitl16', source='local', pretrained_path=<CHECKPOINT/PATH>)
cell_dino_vitl14 = torch.hub.load(REPO_DIR, 'cell_dino_hpa_vitl14', source='local', pretrained_path=<CHECKPOINT/PATH>)
Code is released under the CC BY NC License. See [LICENSE_CELL_DINO_CODE](/facebookresearch/dinov2/blob/main/LICENSE_CELL_DINO_CODE) for additional details.
Model weights are released under the FAIR Noncommercial Research License. See [LICENSE_CELL_DINO_CODE_WEIGHTS](/facebookresearch/dinov2/blob/main/LICENSE_CELL_DINO_CODE_WEIGHTS) for additional details.