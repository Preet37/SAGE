# Source: https://github.com/Vchitect/VBench
# Title: [CVPR2024 Highlight] VBench - We Evaluate Video Generation
# Fetched via: trafilatura
# Date: 2026-04-09

This repository provides unified implementations for the VBench series of works, supporting comprehensive evaluation of video generative models across a wide spectrum of capabilities and settings.
If your questions are not addressed in this README, please contact Ziqi Huang at ZIQI002 [at] e [dot] ntu [dot] edu [dot] sg.
[Overview](#overview)- See this section for component locations and the differences between VBench, VBench++, and VBench-2.0.[Updates](#updates)[Evaluation Results](#evaluation_results)[Video Generation Models Info](https://github.com/Vchitect/VBench/tree/master/sampled_videos#what-are-the-details-of-the-video-generation-models)[Installation](#installation)[Usage](#usage)[Prompt Suite](#prompt_suite)[Sampled Videos](#sampled_videos)[Evaluation Method Suite](#evaluation_method_suite)[Citation and Acknowledgement](#citation_and_acknowledgement)
This repository provides unified implementations for the VBench series of works, supporting comprehensive evaluation of video generative models across a wide spectrum of capabilities and settings.
TL;DR: Evaluating Video Generation — Benchmark • Evaluation Dimensions • Evaluation Methods • Human Alignment • Insights
[VBench: Comprehensive Benchmark Suite for Video Generative Models]
[Ziqi Huang]∗,[Yinan He]∗,[Jiashuo Yu]∗,[Fan Zhang]∗,[Chenyang Si],[Yuming Jiang],[Yuanhan Zhang],[Tianxing Wu],[Qingyang Jin],[Nattapol Chanpaisit],[Yaohui Wang],[Xinyuan Chen],[Limin Wang],[Dahua Lin]+,[Yu Qiao]+,[Ziwei Liu]+
IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), 2024
We propose VBench, a comprehensive benchmark suite for video generative models. We design a comprehensive and hierarchical Evaluation Dimension Suite to decompose "video generation quality" into multiple well-defined dimensions to facilitate fine-grained and objective evaluation. For each dimension and each content category, we carefully design a Prompt Suite as test cases, and sample Generated Videos from a set of video generation models. For each evaluation dimension, we specifically design an Evaluation Method Suite, which uses carefully crafted method or designated pipeline for automatic objective evaluation. We also conduct Human Preference Annotation for the generated videos for each dimension, and show that VBench evaluation results are well aligned with human perceptions. VBench can provide valuable insights from multiple perspectives.
Note: The code and README for the VBench components are located [here](https://github.com/Vchitect/VBench/tree/master), relative path: .
.
@InProceedings{huang2023vbench,
title={{VBench}: Comprehensive Benchmark Suite for Video Generative Models},
author={Huang, Ziqi and He, Yinan and Yu, Jiashuo and Zhang, Fan and Si, Chenyang and Jiang, Yuming and Zhang, Yuanhan and Wu, Tianxing and Jin, Qingyang and Chanpaisit, Nattapol and Wang, Yaohui and Chen, Xinyuan and Wang, Limin and Lin, Dahua and Qiao, Yu and Liu, Ziwei},
booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
year={2024}
}
TL;DR: Extends VBench with (1) VBench-I2V for image-to-video, (2) VBench-Long for long videos, and (3) VBench-Trustworthiness covering fairness, bias, and safety.
[VBench++: Comprehensive and Versatile Benchmark Suite for Video Generative Models]
[Ziqi Huang]∗,[Fan Zhang]∗,[Xiaojie Xu],[Yinan He],[Jiashuo Yu],[Ziyue Dong],[Qianli Ma],[Nattapol Chanpaisit],[Chenyang Si],[Yuming Jiang],[Yaohui Wang],[Xinyuan Chen],[Ying-Cong Chen],[Limin Wang],[Dahua Lin]+,[Yu Qiao]+,[Ziwei Liu]+
IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 2025
VBench++ supports a wide range of video generation tasks, including text-to-video and image-to-video, with an adaptive Image Suite for fair evaluation across different settings. It evaluates not only technical quality but also the trustworthiness of generative models, offering a comprehensive view of model performance. We continually incorporate more video generative models into VBench to inform the community about the evolving landscape of video generation.
Note: The code and README for the VBench++ components are located at:
- (1) VBench-I2V (image-to-video):
[link](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_i2v), relative path:vbench2_beta_i2v
- (2) VBench-Long (long video evaluation):
[link](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_long), relative path:vbench2_beta_long
- (3) VBench-Trustworthiness (fairness, bias, and safety):
[link](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_trustworthiness), relative path:vbench2_beta_trustworthiness
*These modules belong to VBench++, not VBench, or VBench-2.0. However, to maintain backward compatibility for users who have already installed the repository, we preserve the original relative path names and provide this clarification here. *
@article{huang2025vbench++,
title={{VBench++}: Comprehensive and Versatile Benchmark Suite for Video Generative Models},
author={Huang, Ziqi and Zhang, Fan and Xu, Xiaojie and He, Yinan and Yu, Jiashuo and Dong, Ziyue and Ma, Qianli and Chanpaisit, Nattapol and Si, Chenyang and Jiang, Yuming and Wang, Yaohui and Chen, Xinyuan and Chen, Ying-Cong and Wang, Limin and Lin, Dahua and Qiao, Yu and Liu, Ziwei},
journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
year={2025},
doi={10.1109/TPAMI.2025.3633890}
}
TL;DR: Extends VBench to evaluate intrinsic faithfulness — a key challenge for next-generation video generation models.
[VBench-2.0: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness]
[Dian Zheng]∗,[Ziqi Huang]∗,[Hongbo Liu],[Kai Zou],[Yinan He],[Fan Zhang],[Yuanhan Zhang],[Jingwen He],[Wei-Shi Zheng]+,[Yu Qiao]+,[Ziwei Liu]+
[
Overview of VBench-2.0. (a) Scope of VBench-2.0. Video generative models have progressed from achieving superficial faithfulness in fundamental technical aspects such as pixel fidelity and basic prompt adherence, to addressing more complex challenges associated with intrinsic faithfulness, including commonsense reasoning, physics-based realism, human motion, and creative composition. While VBench primarily assessed early-stage technical quality, VBench-2.0 expands the benchmarking framework to evaluate these advanced capabilities, ensuring a more comprehensive assessment of next-generation models. (b) Evaluation Dimension of VBench-2.0. VBench-2.0 introduces a structured evaluation suite comprising five broad categories and 18 fine-grained capability dimensions.](/Vchitect/VBench/blob/master/VBench-2.0/asset/fig_paper_teaser.jpg)
Note: The code and README for the VBench-2.0 components are located at [link](https://github.com/Vchitect/VBench/tree/master/VBench-2.0), relative path: VBench-2.0
.
@article{zheng2025vbench2,
title={{VBench-2.0}: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness},
author={Zheng, Dian and Huang, Ziqi and Liu, Hongbo and Zou, Kai and He, Yinan and Zhang, Fan and Zhang, Yuanhan and He, Jingwen and Zheng, Wei-Shi and Qiao, Yu and Liu, Ziwei},
journal={arXiv preprint arXiv:2503.21755},
year={2025}
}
- [03/2026] VBench-I2V Arena released:
[View the generated videos here, and vote for your preferred video. You can explore videos generated by your chosen models following your chosen text prompts.](https://huggingface.co/spaces/Vchitect/VBenchI2V_Video_Arena) - [11/2025] VBench++ accepted to TPAMI:
- [05/2025] We support evaluating customized videos for VBench-2.0! See
[here](https://github.com/Vchitect/VBench/tree/master/VBench-2.0#new-evaluating-single-dimension-of-your-own-videos)for instructions. - [04/2025]
[Human Anomaly Detection for AIGC Videos](https://github.com/Vchitect/VBench/tree/master/VBench-2.0/vbench2/third_party/ViTDetector): We release the pipeline for evaluating human anatomical quality in AIGC videos, including a manually human anomaly dataset on real and AIGC videos, and the training pipeline for anomaly detection. - [03/2025] 🔥 Major Update! We released
[VBench-2.0](https://github.com/Vchitect/VBench/tree/master/VBench-2.0)! 🔥 Video generative models have progressed from achieving superficial faithfulness in fundamental technical aspects such as pixel fidelity and basic prompt adherence, to addressing more complex challenges associated with intrinsic faithfulness, including commonsense reasoning, physics-based realism, human motion, and creative composition. While VBench primarily assessed early-stage technical quality, VBench-2.0 expands the benchmarking framework to evaluate these advanced capabilities, ensuring a more comprehensive assessment of next-generation models. - [01/2025] PyPI Updates: v0.1.5 preprocessing bug fixes, torch>=2.0 support.
- [01/2025] VBench Arena released:
[View the generated videos here, and vote for your preferred video. This demo features over 180,000 generated videos, and you can explore videos generated by your chosen models (we already support 40 models) following your chosen text prompts.](https://huggingface.co/spaces/Vchitect/VBench_Video_Arena)
-
[09/2024] VBench-Long Leaderboard available: Our VBench-Long leaderboard now has 10 long video generation models. VBench leaderboard now has 40 text-to-video (both long and short) models. All video generative models are encouraged to participate!
-
[09/2024] PyPI Updates: PyPI package is updated to version
[0.1.4](https://github.com/Vchitect/VBench/releases/tag/v0.1.4): bug fixes and multi-gpu inference. -
[08/2024] Longer and More Descriptive Prompts:
[Available Here](https://github.com/Vchitect/VBench/tree/master/prompts/gpt_enhanced_prompts)! We follow[CogVideoX](https://github.com/THUDM/CogVideo?tab=readme-ov-file#prompt-optimization)'s prompt optimization technique to enhance VBench prompts using GPT-4o, making them longer and more descriptive without altering their original meaning. -
[08/2024] VBench Leaderboard update: Our leaderboard has 28 T2V models, 12 I2V models so far. All video generative models are encouraged to participate!
-
[06/2024] 🔥
[VBench-Long](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_long)🔥 is ready to use for evaluating longer Sora-like videos! -
[06/2024] Model Info Documentation: Information on video generative models in our
[VBench Leaderboard](https://huggingface.co/spaces/Vchitect/VBench_Leaderboard)is documented[HERE](https://github.com/Vchitect/VBench/tree/master/sampled_videos#what-are-the-details-of-the-video-generation-models). -
[05/2024] PyPI Update: PyPI package
vbench
is updated to version 0.1.2. This includes changes in the preprocessing for high-resolution images/videos forimaging_quality
, support for evaluating customized videos, and minor bug fixes. -
[04/2024] We release all the videos we sampled and used for VBench evaluation.
[See details](https://drive.google.com/drive/folders/13pH95aUN-hVgybUZJBx1e_08R6xhZs5X)[here](https://github.com/Vchitect/VBench/tree/master/sampled_videos). -
[03/2024] 🔥
[VBench-Trustworthiness](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_trustworthiness)🔥 We now support evaluating the trustworthiness (e.g., culture, fairness, bias, safety) of video generative models. -
[03/2024] 🔥
[VBench-I2V](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_i2v)🔥 We now support evaluating Image-to-Video (I2V) models. We also provide[Image Suite](https://drive.google.com/drive/folders/1fdOZKQ7HWZtgutCKKA7CMzOhMFUGv4Zx?usp=sharing). -
[03/2024] We support evaluating customized videos! See
[here](https://github.com/Vchitect/VBench/?tab=readme-ov-file#new-evaluate-your-own-videos)for instructions. -
[01/2024] PyPI package is released!
[. Simply](https://pypi.org/project/vbench/)pip install vbench
. -
[12/2023] 🔥
[VBench](https://github.com/Vchitect/VBench?tab=readme-ov-file#usage)🔥 Evaluation code released for 16 Text-to-Video (T2V) evaluation dimensions.['subject_consistency', 'background_consistency', 'temporal_flickering', 'motion_smoothness', 'dynamic_degree', 'aesthetic_quality', 'imaging_quality', 'object_class', 'multiple_objects', 'human_action', 'color', 'spatial_relationship', 'scene', 'temporal_style', 'appearance_style', 'overall_consistency']
-
[11/2023] Prompt Suites released. (See prompt lists
[here](https://github.com/Vchitect/VBench/tree/master/prompts))
See our leaderboard for the most updated ranking and numerical results (with models like Gen-3, Kling, Pika).
Additionally, we present radar charts separately for the evaluation results of open-source and closed-source models. The results are normalized per dimension for clearer comparisons.
See numeric values at our [Leaderboard](https://huggingface.co/spaces/Vchitect/VBench_Leaderboard) 🥇🥈🥉
See [model info](https://github.com/Vchitect/VBench/tree/master/sampled_videos#what-are-the-details-of-the-video-generation-models) for video generation models we used for evaluation.
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 # or any other PyTorch version with CUDA<=12.1
pip install vbench
To evaluate some video generation ability aspects, you need to install [detectron2](https://github.com/facebookresearch/detectron2) via:
pip install detectron2@git+https://github.com/facebookresearch/detectron2.git
If there is an error during [detectron2](https://github.com/facebookresearch/detectron2) installation, see [here](https://detectron2.readthedocs.io/en/latest/tutorials/install.html). Detectron2 is working only with CUDA 12.1 or 11.X.
Download [VBench_full_info.json](https://github.com/Vchitect/VBench/blob/master/vbench/VBench_full_info.json) to your running directory to read the benchmark prompt suites.
git clone https://github.com/Vchitect/VBench.git
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118 # or other version with CUDA<=12.1
pip install VBench
If there is an error during [detectron2](https://github.com/facebookresearch/detectron2) installation, see [here](https://detectron2.readthedocs.io/en/latest/tutorials/install.html).
Use VBench to evaluate videos, and video generative models.
- A Side Note: VBench is designed for evaluating different models on a standard benchmark. Therefore, by default, we enforce evaluation on the standard VBench prompt lists to ensure fair comparisons among different video generation models. That's also why we give warnings when a required video is not found. This is done via defining the set of prompts in
[VBench_full_info.json](https://github.com/Vchitect/VBench/blob/master/vbench/VBench_full_info.json). However, we understand that many users would like to use VBench to evaluate their own videos, or videos generated from prompts that does not belong to the VBench Prompt Suite, so we also added the function of Evaluating Your Own Videos. Simply setmode=custom_input
, and you can evaluate your own videos.
We support evaluating any video. Simply provide the path to the video file, or the path to the folder that contains your videos. There is no requirement on the videos' names.
- Note: We support customized videos / prompts for the following dimensions:
'subject_consistency', 'background_consistency', 'motion_smoothness', 'dynamic_degree', 'aesthetic_quality', 'imaging_quality'
To evaluate videos with customized input prompt, run our script with --mode=custom_input
:
python evaluate.py \
--dimension $DIMENSION \
--videos_path /path/to/folder_or_video/ \
--mode=custom_input
alternatively you can use our command:
vbench evaluate \
--dimension $DIMENSION \
--videos_path /path/to/folder_or_video/ \
--mode=custom_input
To evaluate using multiple gpus, we can use the following commands:
torchrun --nproc_per_node=${GPUS} --standalone evaluate.py ...args...
or
vbench evaluate --ngpus=${GPUS} ...args...
vbench evaluate --videos_path $VIDEO_PATH --dimension $DIMENSION
For example:
vbench evaluate --videos_path "sampled_videos/lavie/human_action" --dimension "human_action"
from vbench import VBench
my_VBench = VBench(device, <path/to/VBench_full_info.json>, <path/to/save/dir>)
my_VBench.evaluate(
videos_path = <video_path>,
name = <name>,
dimension_list = [<dimension>, <dimension>, ...],
)
For example:
from vbench import VBench
my_VBench = VBench(device, "vbench/VBench_full_info.json", "evaluation_results")
my_VBench.evaluate(
videos_path = "sampled_videos/lavie/human_action",
name = "lavie_human_action",
dimension_list = ["human_action"],
)
vbench evaluate \
--videos_path $VIDEO_PATH \
--dimension $DIMENSION \
--mode=vbench_category \
--category=$CATEGORY
or
python evaluate.py \
--dimension $DIMENSION \
--videos_path /path/to/folder_or_video/ \
--mode=vbench_category
We have provided scripts to download VideoCrafter-1.0 samples, and the corresponding evaluation scripts.
# download sampled videos
sh scripts/download_videocrafter1.sh
# evaluate VideoCrafter-1.0
sh scripts/evaluate_videocrafter1.sh
We have provided scripts for calculating the Total Score
, Quality Score
, and Semantic Score
in the Leaderboard. You can run them locally to obtain the aggregate scores or as a final check before submitting to the Leaderboard.
# Pack the evaluation results into a zip file.
cd evaluation_results
zip -r ../evaluation_results.zip .
# [Optional] get the total score of your submission file.
python scripts/cal_final_score.py --zip_file {path_to_evaluation_results.zip} --model_name {your_model_name}
You can submit the json file to [HuggingFace](https://huggingface.co/spaces/Vchitect/VBench_Leaderboard)
To calculate the Total Score, we follow these steps:
-
Normalization:
Each dimension's results are normalized using the following formula:Normalized Score = (dim_score - min_val) / (max_val - min_val)
-
Quality Score:
TheQuality Score
is a weighted average of the following dimensions:
subject consistency, background consistency, temporal flickering, motion smoothness, aesthetic quality, imaging quality, and dynamic degree. -
Semantic Score:
TheSemantic Score
is a weighted average of the following dimensions:
object class, multiple objects, human action, color, spatial relationship, scene, appearance style, temporal style, and overall consistency. -
Weighted Average Calculation:
The Total Score is a weighted average of theQuality Score
andSemantic Score
:Total Score = w1 * Quality Score + w2 * Semantic Score
The minimum and maximum values used for normalization in each dimension, as well as the weighting coefficients for the average calculation, can be found in the scripts/constant.py
file.
For Total Score Calculation for VBench-I2V, you can refer to [link](https://github.com/Vchitect/VBench/tree/master/vbench2_beta_i2v#submit-to-leaderboard).
[Optional] Please download the pre-trained weights according to the guidance in the model_path.txt
file for each model in the pretrained
folder to ~/.cache/vbench
.
We provide prompt lists are at prompts/
.
Check out [details of prompt suites](https://github.com/Vchitect/VBench/tree/master/prompts), and instructions for [how to sample videos for evaluation](https://github.com/Vchitect/VBench/tree/master/prompts).
To facilitate future research and to ensure full transparency, we release all the videos we sampled and used for VBench evaluation. You can download them on [Google Drive](https://drive.google.com/drive/folders/13pH95aUN-hVgybUZJBx1e_08R6xhZs5X).
See detailed explanations of the sampled videos [here](https://github.com/Vchitect/VBench/tree/master/sampled_videos).
We also provide detailed setting for the models under evaluation [here](https://github.com/Vchitect/VBench/tree/master/sampled_videos#what-are-the-details-of-the-video-generation-models).
To perform evaluation on one dimension, run this:
python evaluate.py --videos_path $VIDEOS_PATH --dimension $DIMENSION
- The complete list of dimensions:
['subject_consistency', 'background_consistency', 'temporal_flickering', 'motion_smoothness', 'dynamic_degree', 'aesthetic_quality', 'imaging_quality', 'object_class', 'multiple_objects', 'human_action', 'color', 'spatial_relationship', 'scene', 'temporal_style', 'appearance_style', 'overall_consistency']
Alternatively, you can evaluate multiple models and multiple dimensions using this script:
bash evaluate.sh
- The default sampled video paths:
vbench_videos/{model}/{dimension}/{prompt}-{index}.mp4/gif
Before evaluating the temporal flickering dimension, it is necessary to filter out the static videos first.
To filter static videos in the temporal flickering dimension, run this:
# This only filter out static videos whose prompt matches the prompt in the temporal_flickering.
python static_filter.py --videos_path $VIDEOS_PATH
You can adjust the filtering scope by:
# 1. Change the filtering scope to consider all files inside videos_path for filtering.
python static_filter.py --videos_path $VIDEOS_PATH --filter_scope all
# 2. Specify the path to a JSON file ($filename) to consider only videos whose prompts match those listed in $filename.
python static_filter.py --videos_path $VIDEOS_PATH --filter_scope $filename
Order is based on the time joining the project:
[Ziqi Huang],[Yinan He],[Jiashuo Yu],[Fan Zhang],[Nattapol Chanpaisit],[Xiaojie Xu],[Qianli Ma],[Ziyue Dong],[Dian Zheng],[Hongbo Liu],[Kai Zou]
This project wouldn't be possible without the following open-sourced repositories:
[AMT](https://github.com/MCG-NKU/AMT/), [UMT](https://github.com/OpenGVLab/unmasked_teacher), [RAM](https://github.com/xinyu1205/recognize-anything), [CLIP](https://github.com/openai/CLIP), [RAFT](https://github.com/princeton-vl/RAFT), [GRiT](https://github.com/JialianW/GRiT), [IQA-PyTorch](https://github.com/chaofengc/IQA-PyTorch/), [ViCLIP](https://github.com/OpenGVLab/InternVideo/tree/main/Data/InternVid), and [LAION Aesthetic Predictor](https://github.com/LAION-AI/aesthetic-predictor).
We are putting together [Awesome-Evaluation-of-Visual-Generation](https://github.com/ziqihuangg/Awesome-Evaluation-of-Visual-Generation), which collects works for evaluating visual generation.
Our related projects: [Evaluation Agent](https://vchitect.github.io/Evaluation-Agent-project/), [Uni-MMMU](https://vchitect.github.io/Uni-MMMU-Project/), and [WorldLens](https://worldbench.github.io/worldlens).
@InProceedings{zhang2024evaluationagent,
title = {Evaluation Agent: Efficient and Promptable Evaluation Framework for Visual Generative Models},
author = {Zhang, Fan and Tian, Shulin and Huang, Ziqi and Qiao, Yu and Liu, Ziwei},
booktitle={Annual Meeting of the Association for Computational Linguistics (ACL), 2025},
year = {2025}
}
@article{zou2025unimmmumassivemultidisciplinemultimodal,
title={{Uni-MMMU}: A Massive Multi-discipline Multimodal Unified Benchmark},
author = {Kai Zou and Ziqi Huang and Yuhao Dong and Shulin Tian and Dian Zheng and Hongbo Liu and Jingwen He and Bin Liu and Yu Qiao and Ziwei Liu},
journal={arXiv preprint arXiv:2510.13759},
year = {2025}
}
@article{worldlens,
title = {{WorldLens}: Full-Spectrum Evaluations of Driving World Models in Real World},
author = {Ao Liang and Lingdong Kong and Tianyi Yan and Hongsi Liu and Wesley Yang and Ziqi Huang and Wei Yin and Jialong Zuo and Yixuan Hu and Dekai Zhu and Dongyue Lu and Youquan Liu and Guangfeng Jiang and Linfeng Li and Xiangtai Li and Long Zhuo and Lai Xing Ng and Benoit R. Cottereau and Changxin Gao and Liang Pan and Wei Tsang Ooi and Ziwei Liu},
journal = {arXiv preprint arXiv:2512.xxxxx}
year = {2025}
}
How to Reach Us:
- Code Issues: Please open an
[issue](https://github.com/Vchitect/VBench/issues)in our GitHub repository for any problems or bugs. - Evaluation Requests: To submit your sampled videos for evaluation, please complete this
[Google Form](https://forms.gle/wHk1xe7ecvVNj7yAA). - General Inquiries: Check our
[FAQ](https://github.com/Vchitect/VBench/blob/master/README-FAQ.md)for common questions. For other questions, contact Ziqi Huang at ZIQI002 [at] e [dot] ntu [dot] edu [dot] sg.
If you find our repo useful for your research, please consider citing our paper:
@InProceedings{huang2023vbench,
title={{VBench}: Comprehensive Benchmark Suite for Video Generative Models},
author={Huang, Ziqi and He, Yinan and Yu, Jiashuo and Zhang, Fan and Si, Chenyang and Jiang, Yuming and Zhang, Yuanhan and Wu, Tianxing and Jin, Qingyang and Chanpaisit, Nattapol and Wang, Yaohui and Chen, Xinyuan and Wang, Limin and Lin, Dahua and Qiao, Yu and Liu, Ziwei},
booktitle={Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition},
year={2024}
}
@article{huang2025vbench++,
title={{VBench++}: Comprehensive and Versatile Benchmark Suite for Video Generative Models},
author={Huang, Ziqi and Zhang, Fan and Xu, Xiaojie and He, Yinan and Yu, Jiashuo and Dong, Ziyue and Ma, Qianli and Chanpaisit, Nattapol and Si, Chenyang and Jiang, Yuming and Wang, Yaohui and Chen, Xinyuan and Chen, Ying-Cong and Wang, Limin and Lin, Dahua and Qiao, Yu and Liu, Ziwei},
journal={IEEE Transactions on Pattern Analysis and Machine Intelligence},
year={2025},
doi={10.1109/TPAMI.2025.3633890}
}
@article{zheng2025vbench2,
title={{VBench-2.0}: Advancing Video Generation Benchmark Suite for Intrinsic Faithfulness},
author={Zheng, Dian and Huang, Ziqi and Liu, Hongbo and Zou, Kai and He, Yinan and Zhang, Fan and Zhang, Yuanhan and He, Jingwen and Zheng, Wei-Shi and Qiao, Yu and Liu, Ziwei},
journal={arXiv preprint arXiv:2503.21755},
year={2025}
}