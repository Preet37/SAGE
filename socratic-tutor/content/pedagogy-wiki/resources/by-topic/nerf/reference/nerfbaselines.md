# Source: https://nerfbaselines.github.io
# Title: NerfBaselines
# Fetched via: trafilatura
# Date: 2026-04-09

Baselines
NerfBaselines is a framework for evaluating and comparing existing NeRF methods. Currently, most official implementations use different dataset loaders, evaluation protocols, and metrics which renders the comparison of methods difficult. Therefore, this project aims to provide a unified interface for running and evaluating methods on different datasets in a consistent way using the same metrics. But instead of reimplementing the methods, we use the official implementations and wrap them so that they can be run easily using the same interface.
Mip-NeRF 360 is a collection of four indoor and five outdoor object-centric scenes. The camera trajectory is an orbit around the object with fixed elevation and radius. The test set takes each n-th frame of the trajectory as test views.
|
Paper's PSNR: 27.04
Authors evaluated on larger images which were downscaled to the target size (avoiding JPEG compression artifacts) instead of using the official provided downscaled images. As mentioned in the 3DGS paper, this increases results slightly ~0.5 dB PSNR.
Paper's SSIM: 0.805
Authors evaluated on larger images which were downscaled to the target size (avoiding JPEG compression artifacts) instead of using the official provided downscaled images. As mentioned in the 3DGS paper, this increases results slightly ~0.5 dB PSNR.
Paper's PSNR: 27.26
Paper's SSIM: 0.810
Paper's PSNR: 27.29
Experiments use the default 'ours' configuration. There is also 'big' configuration which uses more resources and achieves better results.
Paper's PSNR: 27.20
Paper's SSIM: 0.815
Paper's LPIPS (VGG): 0.214
Paper's PSNR: 27.79
Authors evaluated on larger images which were downscaled to the target size (avoiding JPEG compression artifacts) instead of using the official provided downscaled images. As mentioned in the 3DGS paper, this increases results slightly ~0.5 dB PSNR.
Paper's SSIM: 0.827
Authors evaluated on larger images which were downscaled to the target size (avoiding JPEG compression artifacts) instead of using the official provided downscaled images. As mentioned in the 3DGS paper, this increases results slightly ~0.5 dB PSNR.
Paper's LPIPS (VGG): 0.203
Authors evaluated on larger images which were downscaled to the target size (avoiding JPEG compression artifacts) instead of using the official provided downscaled images. As mentioned in the 3DGS paper, this increases results slightly ~0.5 dB PSNR.
Paper's PSNR: 27.69
Paper's SSIM: 0.792
Paper's LPIPS (VGG): 0.237
Paper's PSNR: 28.54
Paper's SSIM: 0.828
Paper's LPIPS (VGG): 0.189
Blender (nerf-synthetic) is a synthetic dataset used to benchmark NeRF methods. It consists of 8 scenes of an object placed on a white background. Cameras are placed on a semi-sphere around the object. Scenes are licensed under various CC licenses.
|
Paper's PSNR: 31.00
Paper's SSIM: 0.947
Paper's LPIPS (VGG): 0.081
Paper's PSNR: 32.52
Paper's SSIM: 0.982
Paper's PSNR: 33.18
Instant-NGP trained and evaluated on black background instead of white.
Paper's PSNR: 33.68
Paper's PSNR: 33.14
Paper's SSIM: 0.963
Paper's LPIPS (VGG): 0.047
Paper's PSNR: 33.31
Paper's PSNR: 33.88
The method was trained and evaluated on black background instead of white, which is the default in NerfBaselines. The results are not part of the paper (only results for `Ours (sorted)` are reported), but are provided in the GitHub repository.
Paper's SSIM: 0.970
The method was trained and evaluated on black background instead of white, which is the default in NerfBaselines. The results are not part of the paper (only results for `Ours (sorted)` are reported), but are provided in the GitHub repository.
Paper's PSNR: 33.80
Exact hyperparameters for Blender dataset are not provided in the released source code. The default parameters were used in NerfBaselines likely leading to worse results.
Paper's SSIM: 0.970
Exact hyperparameters for Blender dataset are not provided in the released source code. The default parameters were used in NerfBaselines likely leading to worse results.
Paper's PSNR: 33.09
Paper's SSIM: 0.971
Paper's LPIPS (VGG): 0.031
Tanks and Temples is a benchmark for image-based 3D reconstruction. The benchmark sequences were acquired outside the lab, in realistic conditions. Ground-truth data was captured using an industrial laser scanner. The benchmark includes both outdoor scenes and indoor environments. The dataset is split into three subsets: training, intermediate, and advanced.
|
LLFF is a dataset of forward-facing scenes with a small variation in camera pose. NeRF methods usually use NDC-space parametrization for the scene representation.
|
Paper's PSNR: 26.73
Paper's SSIM: 0.839
Paper's LPIPS (VGG): 0.204
Hierarchical 3DGS is a dataset released with H3DGS paper. We implement the two public single-chunks scenes (SmallCity, Campus) used for evaluation. To collect the dataset, authors used a bicycle helmet on which they mounted 6 GoPro HERO6 Black cameras (5 for the Campus scene). They collected SmallCity and BigCity captures on a bicycle, riding at around 6–7km/h, while Campus was captured on foot wearing the helmet. Poses were estimated using COLMAP with custom parameters and hierarchical mapper. Additinal per-chunk bundle adjustment was performed. It is recommended to use exposure modeling with this dataset
|
Paper's PSNR: 25.39
Results in the paper were evaluated using different tau (0, 3, 6, 15), where tau=0 is the slowest, but highest quality. We choose tau=6 - consistent with most experiments in the paper, providing a good trade-off between quality and speed.
Paper's SSIM: 0.806
Results in the paper were evaluated using different tau (0, 3, 6, 15), where tau=0 is the slowest, but highest quality. We choose tau=6 - consistent with most experiments in the paper, providing a good trade-off between quality and speed.
Modified Mip-NeRF 360 dataset with small train set (12 or 24) views. The dataset is used to evaluate sparse-view NVS methods.
|
ZipNeRF is a dataset with four large scenes: Berlin, Alameda, London, and NYC, (1000-2000 photos each) captured using fisheye cameras. This implementation uses undistorted images which are provided with the dataset and the downsampled resolutions are between 1392 × 793 and 2000 × 1140 depending on scene. It is recommended to use exposure modeling with this dataset if available.
|
Photo Tourism is a dataset of images of famous landmarks, such as the Sacre Coeur, the Trevi Fountain, and the Brandenburg Gate. The images were captured by tourist at different times of the day and year, images have varying lighting conditions and occlusions. The evaluation protocol is based on NeRF-W, where the image appearance embeddings are optimized on the left side of the image and the metrics are computed on the right side of the image.
|
Paper's PSNR: 24.70
The original paper reports metrics for test images where the appearance embedding is estimated from the full test image, not just the left half as in the official evaluation protocol. The reported numbers are computed using the official evaluation protocol and are, therefore, lower than the numbers reported in the paper.
Paper's SSIM: 0.865
The original paper reports metrics for test images where the appearance embedding is estimated from the full test image, not just the left half as in the official evaluation protocol. The reported numbers are computed using the official evaluation protocol and are, therefore, lower than the numbers reported in the paper.
Paper's LPIPS: 0.124
The original paper reports metrics for test images where the appearance embedding is estimated from the full test image, not just the left half as in the official evaluation protocol. The reported numbers are computed using the official evaluation protocol and are, therefore, lower than the numbers reported in the paper.
SeaThru-NeRF dataset contains four underwater forward-facing scenes.
|
If you use this code in your research, please cite the following paper:
@inproceedings{kulhanek2025nerfbaselines,
title={\{N}erf{B}aselines: Consistent and Reproducible Evaluation of Novel View Synthesis Methods},
author={Jonas Kulhanek and Torsten Sattler},
year={2025},
booktitle={Proceedings of the 39th International Conference on Neural Information Processing Systems (NeurIPS 2025)},
}
We want to thank Brent Yi and the [NerfStudio Team](https://github.com/nerfstudio-project/nerfstudio) for helpful discussions regarding the NerfStudio codebase.
This work was supported by the Czech Science Foundation (GAČR) EXPRO (grant no. 23-07973X), the Grant Agency of the Czech Technical University in Prague (grant no. SGS24/095/OHK3/2T/13), and by the Ministry of Education, Youth and Sports of the Czech Republic through the e-INFRA CZ (ID:90254).
The NerfBaselines project is licensed under the [MIT license](https://raw.githubusercontent.com/nerfbaselines/nerfbaselines/main/LICENSE).
Each implemented method is licensed under the license provided by the authors of the method.
For the currently implemented methods, the following licenses apply:
- 2D Gaussian Splatting:
[custom, research only](https://raw.githubusercontent.com/hbb1/2d-gaussian-splatting/main/LICENSE.md) - 3DGRT:
[Apache 2.0](https://raw.githubusercontent.com/nv-tlabs/3dgrut/refs/heads/main/LICENSE) - 3DGS-MCMC:
[custom, research only](https://raw.githubusercontent.com/ubc-vision/3dgs-mcmc/refs/heads/main/LICENSE.md) - 3DGUT:
[Apache 2.0](https://raw.githubusercontent.com/nv-tlabs/3dgrut/refs/heads/main/LICENSE) - CamP:
[Apache 2.0](https://raw.githubusercontent.com/jonbarron/camp_zipnerf/main/LICENSE) - COLMAP:
[BSD](https://colmap.github.io/license.html) - DropGaussian:
[custom, research only](https://raw.githubusercontent.com/DCVL-3D/DropGaussian_release/refs/heads/main/LICENSE_GAUSSIAN_SPLATTING.md),[Apache 2.0](https://raw.githubusercontent.com/DCVL-3D/DropGaussian_release/refs/heads/main/LICENSE) - Gaussian Opacity Fields:
[custom, research only](https://raw.githubusercontent.com/autonomousvision/gaussian-opacity-fields/main/LICENSE.md) - Gaussian Splatting:
[custom, research only](https://raw.githubusercontent.com/graphdeco-inria/gaussian-splatting/main/LICENSE.md) - GS-W:
[unknown] - gsplat:
[Apache 2.0](https://raw.githubusercontent.com/nerfstudio-project/gsplat/main/LICENSE) - H3DGS:
[custom, research only](https://raw.githubusercontent.com/graphdeco-inria/hierarchical-3d-gaussians/refs/heads/main/LICENSE.md),[custom, research only](https://raw.githubusercontent.com/graphdeco-inria/gaussian-splatting/refs/heads/main/LICENSE.md) - Instant NGP:
[custom, research only](https://raw.githubusercontent.com/NVlabs/instant-ngp/master/LICENSE.txt) - K-Planes:
[BSD 3](https://raw.githubusercontent.com/sarafridov/K-Planes/main/LICENSE) - Mip-NeRF 360:
[Apache 2.0](https://raw.githubusercontent.com/google-research/multinerf/main/LICENSE) - Mip-Splatting:
[custom, research only](https://raw.githubusercontent.com/autonomousvision/mip-splatting/main/LICENSE.md) - NeRF:
[MIT](https://github.com/bmild/nerf/blob/master/LICENSE) - NeRF-W (reimplementation):
[MIT](https://raw.githubusercontent.com/kwea123/nerf_pl/master/LICENSE) - NerfStudio:
[Apache 2.0](https://raw.githubusercontent.com/nerfstudio-project/nerfstudio/main/LICENSE) - Octree-GS:
[custom, research only](https://raw.githubusercontent.com/city-super/Octree-GS/refs/heads/main/LICENSE.md) - PGSR:
[custom, research only](https://raw.githubusercontent.com/zju3dv/PGSR/refs/heads/main/LICENSE.md) - Scaffold-GS:
[custom, research only](https://raw.githubusercontent.com/city-super/Scaffold-GS/main/LICENSE.md) - SeaThru-NeRF:
[Apache 2.0](https://raw.githubusercontent.com/deborahLevy130/seathru_NeRF/master/LICENSE) - SparseGS:
[custom, research only](https://raw.githubusercontent.com/ForMyCat/SparseGS/refs/heads/master/LICENSE.md) - Student Splatting Scooping:
[custom, research only](https://raw.githubusercontent.com/realcrane/3D-student-splating-and-scooping/refs/heads/main/submodules/diff-t-rasterization/LICENSE.md),[GPL-2.0](https://raw.githubusercontent.com/realcrane/3D-student-splating-and-scooping/refs/heads/main/LICENSE) - Taming 3DGS:
[MIT](https://raw.githubusercontent.com/humansensinglab/taming-3dgs/refs/heads/main/LICENSE.md),[custom, research only](https://raw.githubusercontent.com/humansensinglab/taming-3dgs/refs/heads/main/LICENSE_ORIGINAL.md) - TensoRF:
[MIT](https://github.com/apchenstu/TensoRF/blob/main/LICENSE) - Tetra-NeRF:
[MIT](https://raw.githubusercontent.com/jkulhanek/tetra-nerf/master/LICENSE) - WildGaussians:
[MIT](https://raw.githubusercontent.com/jkulhanek/wild-gaussians/main/LICENSE),[custom, research only](https://raw.githubusercontent.com/graphdeco-inria/gaussian-splatting/main/LICENSE.md) - Zip-NeRF:
[Apache 2.0](https://raw.githubusercontent.com/jonbarron/camp_zipnerf/main/LICENSE)