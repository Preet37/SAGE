# Source: https://lilianweng.github.io/posts/2021-12-31-nerf/
# Author: Lilian Weng
# Author Slug: lilian-weng
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-06
# Words: 2336
1. I Introduction
2. II Background 1.
II-A Existing Surveys on NeRF with Comparable Scope
2.
II-B Neural Radiance Field (NeRF) Theory
3.
II-C Datasets 1.
II-C1 Building-scale Dataset
2.
II-C2 Large-Scale Urban Datasets
3.
II-C3 Human Avatar/Face Dataset
4.
II-D Quality Assessment Metrics
…
2. III-B Improvements to Training and Inference Speed 1.
III-B1 Baked
2.
III-B2 Non-Baked
3.
III-C Few Shot/Sparse Training View NeRF
4.
III-D Generative and Conditional Models 1.
III-D1 Generative Adversarial Network-based methods
2. III-D2 Jointly Optimized Latent Models
3.
III-D3 Diffusion NeRF Models
5.
III-E Unbounded Scene and Scene Composition
6.
III-F Pose Estimation 1.
III-F1 NeRF and SLAM
7.
III-G Adjacent Methods for Neural Rendering 1.
III-G1 Explicit Representation and Fast MLP-less Volume Rendering
2.
III-G2 Ray Transformers
…
Neural Radiance Fields (NeRF) use differentiable volume rendering to learn a (typically) implicit neural scene representation, using Multi-Layer Perceptrons (MLPs) to store the geometry and lighting of a 3D scene as neural fields.
This learned representation can then be used to generate 2D images of the scene under novel, user-specified viewpoints (novel view synthesis).
…
In the baseline NeRF model, this is implemented by designing the MLP to be in two stages.
The first stage takes as input \mathbf{x} and outputs \sigma and a high-dimensional feature vector (256 in the original paper).
In the second stage, the feature vector is then concatenated with the viewing direction \mathbf{d}, and passed to an additional MLP, which outputs \mathbf{c}.
…
- •
For each pixel in the image being synthesized, send camera rays through the scene and generate a set of sampling points (see (a) in Fig. 1).
- •
For each sampling point, use the viewing direction and sampling location to compute local color and density using the NeRF MLP(s) (as shown in (b) in Fig. 1).
…
| |L=\sum_{r\in R}||\hat{C}(\mathbf{r})-C_{gt}(\mathbf{r})||_{2}^{2},| |(8)|
|--|--|--|--|
where C_{gt}(\mathbf{r}) is the ground truth color of the training image’s pixel associated to \mathbf{r}, and R is the batch of rays associated to the to-be-synthesized image.
…
The LLFF dataset [6] consists of 24 real-life scenes captured from handheld cellphone cameras.
The views are forward-facing towards the central object.
Each scene consists of 20-30 images.
The COLMAP [3] package was used to compute the poses of the images.
The usage of this dataset is comparable to that of the Realistic Synthetic dataset from [1]; the scenes are not too challenging for any particular NeRF model, and the dataset is well benchmarked, offering readily available comparisons to known methods.

2 Background 1. 2.1 Understating NeRF
...
NeRF uses a separate neural continuous volume representation network for each scene.
In (1, ), the authors demonstrate NeRF’s superior performance compared to prior works and also discuss how the work improves upon previous approaches that use multilayer perceptrons (MLP) to represent objects and scenes as continuous functions and the potential for more progress in efficiently optimizing and rendering NeRF.
…
- •
Queryable continuous: NeRF provides a continuous representation of a scene that can be efficiently queried at any point, enabling applications such as object manipulation and rendering.
- •
Unsupervised training: NeRF can be trained unsupervised, meaning it can learn to reconstruct a scene without explicit supervision.
- •
Wide applicability: NeRF can be applied to a wide spectrum of scenarios, including outdoor scenes, indoor scenes, and even microscopic structures.
…
By tracing camera rays through a scene, NeRF obtains a set of sampled 3D points, which are utilized alongside their corresponding 2D viewing directions as input to a neural network.
The output set comprises colors and densities, which collectively generate visually accurate scene representations.
Also, NeRF requires fewer images to generate a 3D scene than traditional computer vision and deep learning approaches, reducing the rendering time.
…
The NeRF algorithm involves several steps: data acquisition, network training, and rendering.
Figure 2 provides an overview of the NeRF scene representation and differentiable rendering procedure.
It shows the steps involved in synthesizing images, which include sampling 5D coordinates along camera rays, using an MLP to generate color and volume density, and compositing these values into an image using volume rendering techniques.
…
#### Data Acquisition
The first step in the NeRF algorithm is to acquire a set of 2D images of the scene from different viewpoints.
Next, these images are used to train the neural network to model the relationship between the 3D geometry and the scene’s appearance.
Ideally, the images should cover a wide range of viewpoints and lighting conditions to ensure the neural network can capture the full range of variability in the scene.
#### Network Training
The next step in the NeRF algorithm is to train a neural network to model the relationship between the 3D geometry and the scene’s appearance.
Specifically, the neural network takes as input a pair of coordinates (x,y) that corresponds to a 2D point in the image plane and a viewing direction vector and outputs a corresponding 3D point in the scene and its associated color.
This process is repeated for every pixel in the input images, resulting in a set of 3D points and colors that can be used to render the scene from any viewpoint.
…
#### Rendering
The final step in the NeRF algorithm is to use the trained neural network to render new views of the scene from arbitrary viewpoints.
This is done by querying the neural network for the radiance field at each point in the 3D space and using it to generate an image of the scene from the desired viewpoint.
…
Each object is rendered from 100 views for training and 200 views for testing, with the input being posed RGB images and the output a novel rendered view.
The authors created this dataset to complement the existing synthetic-NeRF dataset with more complex and diverse scenes to evaluate the NSVF method.
The images exhibit challenging materials, geometries, and lighting that push the boundaries of novel view synthesis techniques.
As a synthetic dataset, it provides perfect ground truth novel views for quantitative evaluation.
The Synthetic-NSVF dataset provides a challenging benchmark for evaluating representation learning and novel view synthesis methods on complex 3D scenes.
…
The dataset provides the Image sequences (49 or 64 images per scene) in uncompressed PNG format with a resolution of 1600x1200 pixels.
The images have uniform directional lighting and camera calibration information, including intrinsic parameters and extrinsic pose for each viewpoint.
It also provides fused high-resolution 3D point clouds from the structured light scans in XYZ text format with 10-14 million points per scene point cloud.
The points are roughly sampled at 0.2mm resolution, and observability masks indicate where the reference 3D points have data.
…
### 2.3.
Loss Function
NeRF has revolutionized novel view synthesis of complex 3D scenes by representing them as a continuous volumetric function that maps 5D coordinates of rays to properties such as color and density.
This approach renders high-quality novel views by querying the implicit neural representation.
NeRF learns these continuous scene representations from only sparse input views.
…
It reduces the error rate by 60% compared to NeRF and is faster by 7% with only half the number of parameters.
This is achieved by using a scale-aware structure and merging the separate “coarse” and “fine” MLPs of NeRF into a single MLP.
This innovation has the added benefit of reducing the complexity of the model and the computational overhead, making Mip-NeRF more efficient than its predecessor.
Figure 3 shows the comparison of NeRF and Mip-NeRF neural rendering methods.
...
The final neural point cloud is obtained by combining point clouds from multiple viewpoints, and the point generation networks and representation networks are trained end-to-end with a rendering loss.
This pipeline significantly reduces per-scene fitting time and achieves high-quality rendering.
The experiments demonstrate that Point-NeRF achieves state-of-the-art results on multiple datasets and effectively handles errors and outliers through the proposed pruning and growing mechanism.

A **neural radiance field** (**NeRF**) is a neural field for reconstructing a three-dimensional representation of a scene from two-dimensional images.
The NeRF model enables downstream applications of novel view synthesis, scene geometry reconstruction, and obtaining the reflectance properties of the scene.
Additional scene properties such as camera poses may also be jointly learned.
First introduced in 2020, it has since gained significant attention for its potential applications in computer graphics and content creation.
## Algorithm
The NeRF algorithm represents a scene as a radiance field parametrized by a deep neural network (DNN).
The network predicts a volume density and view-dependent emitted radiance given the spatial location \( (x,y,z) \) and viewing direction in Euler angles \( (\theta ,\Phi ) \) of the camera.
By sampling many points along camera rays, traditional volume rendering techniques can produce an image.
### Data collection
A NeRF needs to be retrained for each unique scene.
The first step is to collect images of the scene from different angles and their respective camera pose.
These images are standard 2D images and do not require a specialized camera or software.
Any camera is able to generate datasets, provided the settings and capture method meet the requirements for SfM (Structure from Motion).
…
### Training
For each sparse viewpoint (image and camera pose) provided, camera rays are marched through the scene, generating a set of 3D points with a given radiance direction (into the camera).
For these points, volume density and emitted radiance are predicted using the multi-layer perceptron (MLP).
An image is then generated through classical volume rendering.
Because this process is fully differentiable, the error between the predicted image and the original image can be minimized with gradient descent over multiple viewpoints, encouraging the MLP to develop a coherent model of the scene.
…
### Fourier feature mapping
...
Where \( \mathrm {v} \) is the input point, \( \mathrm {B} _{i} \) are the frequency vectors, and \( a_{i} \) are coefficients.
...
The output now included: volume density, surface normal, material parameters, distance to the first surface intersection (in any direction), and visibility of the external environment in any direction.
The inclusion of these new parameters lets the MLP learn material properties, rather than pure radiance values.
...
To avoid querying the large MLP for each point, this method bakes NeRFs into Sparse Neural Radiance Grids (SNeRG).
A SNeRG is a sparse voxel grid containing opacity and color, with learned feature vectors to encode view-dependent information.
A lightweight, more efficient MLP is then used to produce view-dependent residuals to modify the color and opacity.
To enable this compressive baking, small changes to the NeRF architecture were made, such as running the MLP once per pixel rather than for each point along the ray.
...
In 2022, researchers at Nvidia enabled real-time training of NeRFs through a technique known as Instant Neural Graphics Primitives.
An innovative input encoding reduces computation, enabling real-time training of a NeRF, an improvement orders of magnitude above previous methods.
The speedup stems from the use of spatial hash functions, which have \( O(1) \) access times, and parallelized architectures which run fast on modern GPUs.
...
Plenoxel (plenoptic volume element) uses a sparse voxel representation instead of a volumetric approach as seen in NeRFs.
Plenoxel also completely removes the MLP, instead directly performing gradient descent on the voxel coefficients.
Plenoxel can match the fidelity of a conventional NeRF in orders of magnitude less training time.

In recent years, the field of

*3D from multi-view* has become one of the most popular topics in computer vision conferences, with a high number of submitted papers each year. A groundbreaking paper in this field is the 2020 work titled **“NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis”**, proposing a simple concept of scene parameterization using neural networks.
NeRF models are not just capable of synthesizing novel views, it also takes care of View-Dependent scenes and is able to represent the depth map of a scene with complex occlusions. NeRF PyTorch offers an accessible implementation of this powerful model. *Instant NGP* and *Mip-NeRF360* are two robust adaptations of NeRF. For further reading and a deeper understanding, one can refer to these papers.
This article aims to explore the internal workings of the Original NeRF model by Mildenhall et al.,implementing it step-by-step in PyTorch, based on Yen-Chen Lin’s implementation. Additionally, we will cover how to

**train a NeRF model on a custom dataset** using PyTorch. We’ll guide you through the process and provide **code** and a **Colab notebook** to kickstart your own NeRF journey.
So, let’s get started! This blog post has been structured in the following way.

- Introduction

- Introduction to Volume Rendering

- NeRF MLP Network

- NeRF Positional Encoding

- Hierarchical Volume Sampling

- Training Details

- Code Implementation

- Train NeRF on Custom Dataset

- Experimentation

- Key Takeaways

- Conclusion

- References

**Download Code**To easily follow along this tutorial, please download code by clicking on the button below. It's FREE! Download Code

## Introduction

The NeRF paper is fairly straightforward to read if you have a background in computer graphics and 3D computer vision. However, if you don’t, don’t worry, we’ll cover the key 3D graphics concepts involved in the paper.

“NeRF can be explained with 3 words,
“Neural Volume Rendering” ,

Neural means there is a

learned Neural Network involved Volumetric implies we are specifically using

volume rendering not surface rendering Rendering is the process of

generating 2D images of a 3D scene from a specific viewpoint”

**Neural Radiance Fields (NeRF)** use a neural network to predict the color and volume density at each sampled point along rays projected from the camera frame in 3D space. These predictions are then combined using volume rendering to generate the final image of the scene.
The

*“Neural”* part of NeRF is an MLP (multi-layer perceptron) denoted by . This takes the camera location and viewing direction(, ) and predicts the emitted color from a point along the ray and the volume density () at that point. **Volume density** represents how much a point in a 3D space absorbs or scatters light, quantifying 