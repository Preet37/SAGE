# Source: https://huggingface.co/blog/gaussian-splatting
# Author: Hugging Face
# Author Slug: hugging-face
# Downloaded: 2026-04-06
# Words: 959
[
](#introduction-to-3d-gaussian-splatting)
Introduction to 3D Gaussian Splatting
[Update on GitHub](https://github.com/huggingface/blog/blob/main/gaussian-splatting.md)
[3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://huggingface.co/papers/2308.04079)that allows real-time rendering of photorealistic scenes learned from small samples of images. This article will break down how it works and what it means for the future of graphics.
[
](#what-is-3d-gaussian-splatting)
What is 3D Gaussian Splatting?
3D Gaussian Splatting is, at its core, a rasterization technique. That means:
- Have data describing the scene.
- Draw the data on the screen.
This is analogous to triangle rasterization in computer graphics, which is used to draw many triangles on the screen.
However, instead of triangles, it's gaussians. Here's a single rasterized gaussian, with a border drawn for clarity.
It's described by the following parameters:
- Position: where it's located (XYZ)
- Covariance: how it's stretched/scaled (3x3 matrix)
- Color: what color it is (RGB)
- Alpha: how transparent it is (α)
In practice, multiple gaussians are drawn at once.
That's three gaussians. Now what about 7 million gaussians?
Here's what it looks like with each gaussian rasterized fully opaque:
That's a very brief overview of what 3D Gaussian Splatting is. Next, let's walk through the full procedure described in the paper.
[
](#how-it-works)
How it works
[
](#1-structure-from-motion)
1. Structure from Motion
The first step is to use the Structure from Motion (SfM) method to estimate a point cloud from a set of images. This is a method for estimating a 3D point cloud from a set of 2D images. This can be done with the [COLMAP](https://colmap.github.io/) library.
[
](#2-convert-to-gaussians)
2. Convert to Gaussians
Next, each point is converted to a gaussian. This is already sufficient for rasterization. However, only position and color can be inferred from the SfM data. To learn a representation that yields high quality results, we need to train it.
[
](#3-training)
3. Training
The training procedure uses Stochastic Gradient Descent, similar to a neural network, but without the layers. The training steps are:
- Rasterize the gaussians to an image using differentiable gaussian rasterization (more on that later)
- Calculate the loss based on the difference between the rasterized image and ground truth image
- Adjust the gaussian parameters according to the loss
- Apply automated densification and pruning
Steps 1-3 are conceptually pretty straightforward. Step 4 involves the following:
- If the gradient is large for a given gaussian (i.e. it's too wrong), split/clone it
- If the gaussian is small, clone it
- If the gaussian is large, split it
- If the alpha of a gaussian gets too low, remove it
This procedure helps the gaussians better fit fine-grained details, while pruning unnecessary gaussians.
[
](#4-differentiable-gaussian-rasterization)
4. Differentiable Gaussian Rasterization
As mentioned earlier, 3D Gaussian Splatting is a rasterization approach, which draws the data to the screen. However, some important elements are also that it's:
- Fast
- Differentiable
The original implementation of the rasterizer can be found [here](https://github.com/graphdeco-inria/diff-gaussian-rasterization). The rasterization involves:
- Project each gaussian into 2D from the camera perspective.
- Sort the gaussians by depth.
- For each pixel, iterate over each gaussian front-to-back, blending them together.
Additional optimizations are described in [the paper](https://huggingface.co/papers/2308.04079).
It's also essential that the rasterizer is differentiable, so that it can be trained with stochastic gradient descent. However, this is only relevant for training - the trained gaussians can also be rendered with a non-differentiable approach.
[
](#who-cares)
Who cares?
Why has there been so much attention on 3D Gaussian Splatting? The obvious answer is that the results speak for themselves - it's high-quality scenes in real-time. However, there may be more to the story.
There are many unknowns as to what else can be done with Gaussian Splatting. Can they be animated? The upcoming paper [Dynamic 3D Gaussians: tracking by Persistent Dynamic View Synthesis](https://arxiv.org/pdf/2308.09713) suggests that they can. There are many other unknowns as well. Can they do reflections? Can they be modeled without training on reference images?
Finally, there is growing research interest in [Embodied AI](https://ieeexplore.ieee.org/iel7/7433297/9741092/09687596.pdf). This is an area of AI research where state-of-the-art performance is still orders of magnitude below human performance, with much of the challenge being in representing 3D space. Given that 3D Gaussian Splatting yields a very dense representation of 3D space, what might the implications be for Embodied AI research?
These questions call attention to the method. It remains to be seen what the actual impact will be.
[
](#the-future-of-graphics)
The future of graphics
So what does this mean for the future of graphics? Well, let's break it up into pros/cons:
Pros
- High-quality, photorealistic scenes
- Fast, real-time rasterization
- Relatively fast to train
Cons
- High VRAM usage (4GB to view, 12GB to train)
- Large disk size (1GB+ for a scene)
- Incompatible with existing rendering pipelines
- Static (for now)
So far, the original CUDA implementation has not been adapted to production rendering pipelines, like Vulkan, DirectX, WebGPU, etc, so it's yet to be seen what the impact will be.
There have already been the following adaptations:
These rely either on remote streaming (1) or a traditional quad-based rasterization approach (2-5). While a quad-based approach is compatible with decades of graphics technologies, it may result in lower quality/performance. However, [viewer #5](https://gsplat.tech/) demonstrates that optimization tricks can result in high quality/performance, despite a quad-based approach.
So will we see 3D Gaussian Splatting fully reimplemented in a production environment? The answer is probably yes. The primary bottleneck is sorting millions of gaussians, which is done efficiently in the original implementation using [CUB device radix sort](https://nvlabs.github.io/cub/structcub_1_1_device_radix_sort.html), a highly optimized sort only available in CUDA. However, with enough effort, it's certainly possible to achieve this level of performance in other rendering pipelines.
If you have any questions or would like to get involved, join the [Hugging Face Discord](https://hf.co/join/discord)!