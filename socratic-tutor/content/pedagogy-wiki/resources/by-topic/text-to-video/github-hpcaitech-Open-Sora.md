# Source: https://github.com/hpcaitech/Open-Sora
# Downloaded: 2026-04-06
# Words: 1470
# Author: HPC-AI Tech
# Author Slug: hpc-ai-tech
We design and implement Open-Sora, an initiative dedicated to efficiently producing high-quality video. We hope to make the model, tools and all details accessible to all. By embracing open-source principles, Open-Sora not only democratizes access to advanced video generation techniques, but also offers a streamlined and user-friendly platform that simplifies the complexities of video generation. With Open-Sora, our goal is to foster innovation, creativity, and inclusivity within the field of content creation.
🎬 For a professional AI video-generation product, try [Video Ocean](https://video-ocean.com/) — powered by a superior model.
- [2025.03.12] 🔥 We released Open-Sora 2.0 (11B). 🎬 11B model achieves
[on-par performance](#evaluation)with 11B HunyuanVideo & 30B Step-Video on 📐VBench & 📊Human Preference. 🛠️ Fully open-source: checkpoints and training codes for training with only $200K.[[report]](https://arxiv.org/abs/2503.09642v1) - [2025.02.20] 🔥 We released Open-Sora 1.3 (1B). With the upgraded VAE and Transformer architecture, the quality of our generated videos has been greatly improved 🚀.
[[checkpoints]](#open-sora-13-model-weights)[[report]](/hpcaitech/Open-Sora/blob/main/docs/report_04.md)[[demo]](https://huggingface.co/spaces/hpcai-tech/open-sora) - [2024.12.23] The development cost of video generation models has saved by 50%! Open-source solutions are now available with H200 GPU vouchers.
[[blog]](https://company.hpc-ai.com/blog/the-development-cost-of-video-generation-models-has-saved-by-50-open-source-solutions-are-now-available-with-h200-gpu-vouchers)[[code]](https://github.com/hpcaitech/Open-Sora/blob/main/scripts/train.py)[[vouchers]](https://colossalai.org/zh-Hans/docs/get_started/bonus/) - [2024.06.17] We released Open-Sora 1.2, which includes 3D-VAE, rectified flow, and score condition. The video quality is greatly improved.
[[checkpoints]](#open-sora-12-model-weights)[[report]](/hpcaitech/Open-Sora/blob/main/docs/report_03.md)[[arxiv]](https://arxiv.org/abs/2412.20404) - [2024.04.25] 🤗 We released the
[Gradio demo for Open-Sora](https://huggingface.co/spaces/hpcai-tech/open-sora)on Hugging Face Spaces. - [2024.04.25] We released Open-Sora 1.1, which supports 2s~15s, 144p to 720p, any aspect ratio text-to-image, text-to-video, image-to-video, video-to-video, infinite time generation. In addition, a full video processing pipeline is released.
[[checkpoints]](#open-sora-11-model-weights)[[report]](/hpcaitech/Open-Sora/blob/main/docs/report_02.md) - [2024.03.18] We released Open-Sora 1.0, a fully open-source project for video generation.
Open-Sora 1.0 supports a full pipeline of video data preprocessing, training with
[acceleration, inference, and more. Our model can produce 2s 512x512 videos with only 3 days training.](https://github.com/hpcaitech/ColossalAI)[[checkpoints]](#open-sora-10-model-weights)[[blog]](https://hpc-ai.com/blog/open-sora-v1.0)[[report]](/hpcaitech/Open-Sora/blob/main/docs/report_01.md) - [2024.03.04] Open-Sora provides training with 46% cost reduction.
[[blog]](https://hpc-ai.com/blog/open-sora)
📍 Since Open-Sora is under active development, we remain different branches for different versions. The latest version is [main](https://github.com/hpcaitech/Open-Sora). Old versions include: [v1.0](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.0), [v1.1](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.1), [v1.2](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.2), [v1.3](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.3).
Demos are presented in compressed GIF format for convenience. For original quality samples and their corresponding prompts, please visit our [Gallery](https://hpcaitech.github.io/Open-Sora/).
| 5s 1024×576 | 5s 576×1024 | 5s 576×1024 |
|---|---|---|
OpenSora 1.0 Demo
Videos are downsampled to .gif
for display. Click for original videos. Prompts are trimmed for display,
see [here](/hpcaitech/Open-Sora/blob/main/assets/texts/t2v_samples.txt) for full prompts.
[Tech Report of Open-Sora 2.0](https://arxiv.org/abs/2503.09642v1)[Step by step to train or finetune your own model](/hpcaitech/Open-Sora/blob/main/docs/train.md)[Step by step to train and evaluate an video autoencoder](/hpcaitech/Open-Sora/blob/main/docs/ae.md)[Visit the high compression video autoencoder](/hpcaitech/Open-Sora/blob/main/docs/hcae.md)- Reports of previous version (better see in according branch):
[Open-Sora 1.3](/hpcaitech/Open-Sora/blob/main/docs/report_04.md): shift-window attention, unified spatial-temporal VAE, etc.[Open-Sora 1.2](/hpcaitech/Open-Sora/blob/main/docs/report_03.md),[Tech Report](https://arxiv.org/abs/2412.20404): rectified flow, 3d-VAE, score condition, evaluation, etc.[Open-Sora 1.1](/hpcaitech/Open-Sora/blob/main/docs/report_02.md): multi-resolution/length/aspect-ratio, image/video conditioning/editing, data preprocessing, etc.[Open-Sora 1.0](/hpcaitech/Open-Sora/blob/main/docs/report_01.md): architecture, captioning, etc.
📍 Since Open-Sora is under active development, we remain different branches for different versions. The latest version is [main](https://github.com/hpcaitech/Open-Sora). Old versions include: [v1.0](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.0), [v1.1](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.1), [v1.2](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.2), [v1.3](https://github.com/hpcaitech/Open-Sora/tree/opensora/v1.3).
# create a virtual env and activate (conda as an example)
conda create -n opensora python=3.10
conda activate opensora
# download the repo
git clone https://github.com/hpcaitech/Open-Sora
cd Open-Sora
# Ensure torch >= 2.4.0
pip install -v . # for development mode, `pip install -v -e .`
pip install xformers==0.0.27.post2 --index-url https://download.pytorch.org/whl/cu121 # install xformers according to your cuda version
pip install flash-attn --no-build-isolation
Optionally, you can install flash attention 3 for faster speed.
git clone https://github.com/Dao-AILab/flash-attention # 4f0640d5
cd flash-attention/hopper
python setup.py install
Our 11B model supports 256px and 768px resolution. Both T2V and I2V are supported by one model. 🤗 [Huggingface](https://huggingface.co/hpcai-tech/Open-Sora-v2) 🤖 [ModelScope](https://modelscope.cn/models/luchentech/Open-Sora-v2).
Download from huggingface:
pip install "huggingface_hub[cli]"
huggingface-cli download hpcai-tech/Open-Sora-v2 --local-dir ./ckpts
Download from ModelScope:
pip install modelscope
modelscope download hpcai-tech/Open-Sora-v2 --local_dir ./ckpts
Our model is optimized for image-to-video generation, but it can also be used for text-to-video generation. To generate high quality videos, with the help of flux text-to-image model, we build a text-to-image-to-video pipeline. For 256x256 resolution:
# Generate one given prompt
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_256px.py --save-dir samples --prompt "raining, sea"
# Save memory with offloading
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_256px.py --save-dir samples --prompt "raining, sea" --offload True
# Generation with csv
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_256px.py --save-dir samples --dataset.data-path assets/texts/example.csv
For 768x768 resolution:
# One GPU
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_768px.py --save-dir samples --prompt "raining, sea"
# Multi-GPU with colossalai sp
torchrun --nproc_per_node 8 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_768px.py --save-dir samples --prompt "raining, sea"
You can adjust the generation aspect ratio by --aspect_ratio
and the generation length by --num_frames
. Candidate values for aspect_ratio includes 16:9
, 9:16
, 1:1
, 2.39:1
. Candidate values for num_frames should be 4k+1
and less than 129.
You can also run direct text-to-video by:
# One GPU for 256px
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/256px.py --prompt "raining, sea"
# Multi-GPU for 768px
torchrun --nproc_per_node 8 --standalone scripts/diffusion/inference.py configs/diffusion/inference/768px.py --prompt "raining, sea"
Given a prompt and a reference image, you can generate a video with the following command:
# 256px
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/256px.py --cond_type i2v_head --prompt "A plump pig wallows in a muddy pond on a rustic farm, its pink snout poking out as it snorts contentedly. The camera captures the pig's playful splashes, sending ripples through the water under the midday sun. Wooden fences and a red barn stand in the background, framed by rolling green hills. The pig's muddy coat glistens in the sunlight, showcasing the simple pleasures of its carefree life." --ref assets/texts/i2v.png
# 256px with csv
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/256px.py --cond_type i2v_head --dataset.data-path assets/texts/i2v.csv
# Multi-GPU 768px
torchrun --nproc_per_node 8 --standalone scripts/diffusion/inference.py configs/diffusion/inference/768px.py --cond_type i2v_head --dataset.data-path assets/texts/i2v.csv
During training, we provide motion score into the text prompt. During inference, you can use the following command to generate videos with motion score (the default score is 4):
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_256px.py --save-dir samples --prompt "raining, sea" --motion-score 4
We also provide a dynamic motion score evaluator. After setting your OpenAI API key, you can use the following command to evaluate the motion score of a video:
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_256px.py --save-dir samples --prompt "raining, sea" --motion-score dynamic
| Score | 1 | 4 | 7 |
|---|---|---|---|
We take advantage of ChatGPT to refine the prompt. You can use the following command to refine the prompt. The function is available for both text-to-video and image-to-video generation.
export OPENAI_API_KEY=sk-xxxx
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_256px.py --save-dir samples --prompt "raining, sea" --refine-prompt True
To make the results reproducible, you can set the random seed by:
torchrun --nproc_per_node 1 --standalone scripts/diffusion/inference.py configs/diffusion/inference/t2i2v_256px.py --save-dir samples --prompt "raining, sea" --sampling_option.seed 42 --seed 42
Use --num-sample k
to generate k
samples for each prompt.
We test the computational efficiency of text-to-video on H100/H800 GPU. For 256x256, we use colossalai's tensor parallelism, and --offload True
is used. For 768x768, we use colossalai's sequence parallelism. All use number of steps 50. The results are presented in the format:
| Resolution | 1x GPU | 2x GPUs | 4x GPUs | 8x GPUs |
|---|---|---|---|---|
| 256x256 | ||||
| 768x768 |
On [VBench](https://huggingface.co/spaces/Vchitect/VBench_Leaderboard), Open-Sora 2.0 significantly narrows the gap with OpenAI’s Sora, reducing it from 4.52% → 0.69% compared to Open-Sora 1.2.
Human preference results show our model is on par with HunyuanVideo 11B and Step-Video 30B.
With strong performance, Open-Sora 2.0 is cost-effective.
Thanks goes to these wonderful contributors:
If you wish to contribute to this project, please refer to the [Contribution Guideline](/hpcaitech/Open-Sora/blob/main/CONTRIBUTING.md).
Here we only list a few of the projects. For other works and datasets, please refer to our report.
[ColossalAI](https://github.com/hpcaitech/ColossalAI): A powerful large model parallel acceleration and optimization system.[DiT](https://github.com/facebookresearch/DiT): Scalable Diffusion Models with Transformers.[OpenDiT](https://github.com/NUS-HPC-AI-Lab/OpenDiT): An acceleration for DiT training. We adopt valuable acceleration strategies for training progress from OpenDiT.[PixArt](https://github.com/PixArt-alpha/PixArt-alpha): An open-source DiT-based text-to-image model.[Flux](https://github.com/black-forest-labs/flux): A powerful text-to-image generation model.[Latte](https://github.com/Vchitect/Latte): An attempt to efficiently train DiT for video.[HunyuanVideo](https://github.com/Tencent/HunyuanVideo/tree/main?tab=readme-ov-file): Open-Source text-to-video model.[StabilityAI VAE](https://huggingface.co/stabilityai/sd-vae-ft-mse-original): A powerful image VAE model.[DC-AE](https://github.com/mit-han-lab/efficientvit): Deep Compression AutoEncoder for image compression.[CLIP](https://github.com/openai/CLIP): A powerful text-image embedding model.[T5](https://github.com/google-research/text-to-text-transfer-transformer): A powerful text encoder.[LLaVA](https://github.com/haotian-liu/LLaVA): A powerful image captioning model based on[Mistral-7B](https://huggingface.co/mistralai/Mistral-7B-v0.1)and[Yi-34B](https://huggingface.co/01-ai/Yi-34B).[PLLaVA](https://github.com/magic-research/PLLaVA): A powerful video captioning model.[MiraData](https://github.com/mira-space/MiraData): A large-scale video dataset with long durations and structured caption.
@article{opensora,
title={Open-sora: Democratizing efficient video production for all},
author={Zheng, Zangwei and Peng, Xiangyu and Yang, Tianji and Shen, Chenhui and Li, Shenggui and Liu, Hongxin and Zhou, Yukun and Li, Tianyi and You, Yang},
journal={arXiv preprint arXiv:2412.20404},
year={2024}
}
@article{opensora2,
title={Open-Sora 2.0: Training a Commercial-Level Video Generation Model in $200k},
author={Xiangyu Peng and Zangwei Zheng and Chenhui Shen and Tom Young and Xinying Guo and Binluo Wang and Hang Xu and Hongxin Liu and Mingyan Jiang and Wenjun Li and Yuhui Wang and Anbang Ye and Gang Ren and Qianran Ma and Wanying Liang and Xiang Lian and Xiwen Wu and Yuting Zhong and Zhuangyan Li and Chaoyu Gong and Guojun Lei and Leijun Cheng and Limin Zhang and Minghao Li and Ruijie Zhang and Silan Hu and Shijie Huang and Xiaokang Wang and Yuanheng Zhao and Yuqi Wang and Ziang Wei and Yang You},
year={2025},
journal={arXiv preprint arXiv:2503.09642},
}