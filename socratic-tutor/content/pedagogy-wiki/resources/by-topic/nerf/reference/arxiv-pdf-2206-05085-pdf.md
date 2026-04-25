# Source: https://arxiv.org/pdf/2206.05085.pdf
# Author: Cheng Sun et al.
# Title: Improved Direct Voxel Grid Optimization for Radiance Fields Reconstruction (DVGOv2)
# Fetched via: jina
# Date: 2026-04-09

Title: 2206.05085v4.pdf



Number of Pages: 5

> arXiv:2206.05085v4 [cs.GR] 2 Jul 2022

# Improved Direct Voxel Grid Optimization for Radiance Fields Reconstruction 

## Cheng Sun Min Sun Hwann-Tzong Chen National Tsing Hua University 

chengsun@gapp.nthu.edu.tw sunmin@ee.nthu.edu.tw htchen@cs.nthu.edu.tw 

## Abstract 

In this technical report, we improve the DVGO [ 9] frame-work (called DVGOv2), which is based on Pytorch and uses the simplest dense grid representation. First, we re-implement part of the Pytorch operations with cuda, achiev-ing 2–3× speedup. The cuda extension is automatically compiled just in time. Second, we extend DVGO to sup-port Forward-facing and Unbounded Inward-facing captur-ing. Third, we improve the space time complexity of the dis-tortion loss proposed by mip-NeRF 360 [ 1] from O(N 2) to 

O(N ). The distortion loss improves our quality and train-ing speed. Our efficient implementation could allow more future works to benefit from the loss. Project page: https:// sunset1995.github.io/ dvgo/ .Code: https:// github.com/ sunset1995/ DirectVoxGO .

## 1. Introduction 

Neural radiance fields [ 6] (NeRF) have provided an ap-pealing approach to novel view synthesis for the high qual-ity and flexibility to reconstruct the volume densities and view-dependent colors from multi-view calibrated images. However, NeRF runs very slow due to the processing time of multilayer perceptron (MLP) networks. Consider an MLP consisting of 8 layers with 256 hidden channels: To query a single point would require more than 520 k ≈

256 2 ·8 FLOPs. In each training iteration, there are typically 8,192 rays, each with 256 sampled points, which results in more than 1T FLOPs in total. Using an occupancy mask is one of the easiest ways to speed up. As the training progresses for a scene, we can gradually update an occupancy mask to deactivate some of the space with low density. Thanks to the occupancy mask, we can then skip most of the point queries in each itera-tion after training for a while. VaxNeRF [ 4] reports that a vanilla NeRF with the occupancy mask can achieve 2–8×

speedups for bounded inward-facing scenes [ 4]. Most of the recent works [ 2, 4, 7, 9, 10 ] on training time speedup use the occupancy mask trick. Recently, many works (Tab. 1) have emerged using ex-

Method Data structure Density Color 

DVGO [ 9] dense grid explicit hybrid Plenoxels [ 10 ] sparse grid explicit explicit Instant-NGP [ 7] hash table hybrid hybrid TensoRF [ 2] decomposed grid explicit hybrid 

Table 1. Overview of explicit radiance field representations. 

Various data structures have been realized to model the volume densities and view-dependent colors explicitly. The ‘hybrid’ in-dicates that the explicit representation is followed by an implicit representation (the MLP network). 

plicit representations to reduce training time from hours to minutes per scene. Querying an explicit representation re-quires only constant time computation, which is much more efficient than the few hundred thousand FLOPs per query. Even hybrid representations may benefit from the reduced computation for the speedup in training since the MLP network in a hybrid representation is typically much shal-lower than that in a fully implicit representation. DVGO [ 9]uses the simplest dense grid data structure in fully Pytorch implementation. Plenoxels [ 10 ] model the coefficients of spherical harmonic for view-dependent colors and realize a fully explicit (without MLP) representation. Plenoxels in-terpolation and rendering pipeline are fused in CUDA code. Instant-NGP [ 7] uses hash-table and hybrid representations for both densities and colors. Instant-NGP further improves the training time using C/C++ and fully-fused CUDA im-plementation. TensoRF [ 2] improves the memory footprint and scalability of the dense grid via tensor decomposition and directly modeling the low-rank components. This technical report presents DVGOv2. Compared to DVGO, DVGOv2 achieves another 2–3× speedup and ex-tends to forward-facing and unbounded inward-facing cap-turing. We also present an efficient realization of the distor-tion loss (reduced from O(N 2) to O(N )), which improves our quality and training time. DVGOv2 uses the simplest data structure and most of our intermediate steps are in Python interface. Meanwhile, DVGOv2 still demonstrates the good quality and convergence speed. 12. Efficient regularization 

Unlike the implicit MLP representation, the explicit rep-resentation is found to be more prone to producing artifacts of holes or floaters [ 10 ]. Thus, regularization losses are es-pecially important for achieving reasonable results on the unbounded real-world captured scenes. 

Efficient total variation (TV) loss. TV loss [ 8] is com-monly adapted to prevent unnecessary sharpness in explicit modeling [ 2, 10 ]. For each grid point, we compute the Hu-ber loss to its six nearest-neighbor grid points; we find that the Huber loss is better than L1 and L2 loss in our case. However, computing the TV loss is time-consuming for a large dense grid and requires many Pytorch API calls to implement, so we fuse them into a single CUDA kernel. Be-sides, we skip the forward pass and directly add the gradient into the Pytorch tensor, so the users have to call our API be-tween the normal backward pass and the optimization step (see Listing 1). Despite the CUDA extension, it still takes a lot of time, so we only compute the TV loss densely for all grid points in the first 10k iterations. After the 10k check-point, we only compute the TV loss for grid points involved in the current iteration ( i.e ., with non-zero gradients).       

> 1optimizer.zero_grad()
> 2# compute total_loss
> 3total_loss.backward()
> 4dvgo_model.total_variation_add_grad(
> 5tv_weight, dense_mode=(curr_step<10000))
> 6optimizer.step()

Listing 1. Call our efficient TV loss after the backward pass. 

Efficient O(N ) distortion loss. The distortion loss is pro-posed by mip-NeRF 360 [ 1]. For a ray with N sampled points, the loss is defined as 

Ldist (s, w ) =  

> N−1

∑ 

> i=0
> N−1

∑

> j=0

wiwj

∣∣∣∣

si + si+1 

2 − sj + sj+1 

2

∣∣∣∣

+ 1

3 

> N−1

∑

> i=0

w2 

> i

(si+1 − si) , (1) where (si+1 −si) is the length and (si+si+1 )/2 is the mid-point of the i-th query interval. The s is non-linearly nor-malized (from the near-far clipping distance to [0 , 1] ) to pre-vent overweighting the far query. The weight wi is for the 

i-th sample points. Despite we are using the point-based instead of the interval-based query (which is an interesting problem), we find it still beneficial to adapt the distortion loss. However, the straightforward implementation for the first term in Eq. ( 1) results in O(N 2) computation for a sin-gle ray. This is not a problem for mip-NeRF 360 as there are only 32 query intervals in the finest sampling. For the point-based query, there are typically more than 256 sam-pled points on each ray, which makes the computation non-trivial and consumes many GPU memory (more than 3G for a batch with 4,096 rays). Thus, we re-implement the first term to achieve 

O(N ) computation. Let the mid-point distance mi =(si+si+1 )/2 and mi < m i+1 . We can eliminate the di-agonal term ( i = k, j = k) and rewrite it into:             

> L1st dist =
> N−1∑
> i=0
> N−1∑
> j=0
> wiwj|mi−mj|
> = 2
> N−1∑
> i=1
> i−1∑
> j=0
> wiwj(mi−mj)=
> 2
> N−1∑
> i=1
> wimii−1∑
> j=0
> wj
> −
> 2
> N−1∑
> i=1
> wii−1∑
> j=0
> wjmj
> ,
> (2)

where we can compute and store the prefix sum of (w) and 

(w ⊙ m) first so we can directly lookup the results of the in-ner summation when computing the outer summation. The overall computation can thus be realized in O(N ).The derivative for wk is                          

> ∂
> ∂w k
> L1st dist
> = 2 ∂
> ∂w kk−1∑
> j=0
> wkwj(mk−mj) + 2 ∂
> ∂w kN−1∑
> i=k+1
> wiwk(mi−mk)= 2
> k−1∑
> j=0
> wj(mk−mj) + 2
> N−1∑
> i=k+1
> wi(mi−mk)= 2 mkk−1∑
> j=0
> wj−2
> k−1∑
> j=0
> wjmj+ 2
> N−1∑
> i=k+1
> wimj−2mkN−1∑
> i=k+1
> wi,
> (3)

where we can also compute and store the prefix and suffix sum of (w) and (w⊙m) so we can directly lookup the result when computing the derivative of every wk . The overall computation is also O(N ).We implement the efficient distortion loss as Pytorch CUDA extension and support uneven number of sampled points on each ray. We provide a self-contained package at 

https://github.com/sunset1995/torch efficient distloss . We will see that the distortion loss improves our rendering qual-ity and speed up our training, thanks to the compactness en-couraged by the loss. We believe the efficient distortion loss and our implementation can let more works benefit from mip-NeRF 360’s regularization technique as most NeRF-based methods have hundreds of sampled points on a ray. 

## 3. CUDA speedup 

There are lots of sequential point-wise operations in DVGO, each of which has an overhead for launching the CUDA kernel. So we re-implement these sequential point-wise operations into a single CUDA kernel to re-duce launching overhead. We refer interested reader to 2https://pytorch.org/tutorials/advanced/cpp extension.html .We use Pytorch’s just-in-time compilation mechanism, which automatically compiles the newly implemented C/C++ and CUDA code by the first time it is required. 

Re-implement Adam optimizer. There are about ten point-wise operations in an Adam optimization step. We fuse them into a single kernel and skip updating the grid points with zero gradients. 

Re-implement rendering utils. Originally, we sample an equal number of points on each ray for vectorized Pytorch implementation, where a large number of query points are outside the scene BBox. We now infer the ray BBox inter-section to sample query points parsimoniously for each ray (which is only applicable to bounded scene). Besides, we fuse about ten point-wise operations for the forward and the backward pass of the density to alpha function. In the vol-ume rendering accumulation procedure, we halt tracking a ray once the accumulated transmittance is less than 10 −3.

## 4. Mix of factors affecting speed and quality 

Please note that the comparisons on the training speed and the result quality in this report are affected by many fac-tors, not just the different scene representations as presented in Tab. 1.First, the computation devices are different. As shown in Tab. 2, the computing power across different works is not aligned, where we use the lowest spec GPU to mea-sure our training times. Second, Instant-NGP’s training pipeline is implemented in C++, while the other methods use Python/Pytorch. Instant-NGP and Plenoxels implement most of their computations ( e.g ., grid interpolation, ray-casting, volume rendering) in CUDA; DVGOv2 customizes part of the computation as CUDA extension, and most of the intermediate steps are still in Python interface; DVGO and TensoRF only use the built-in Pytorch API. Third, some implementation details such as regularization terms, policy of occupancy grid, and the other tricks can affect the quality and convergence speed as well. 

GPU FLOPs Memory Used by 

RTX 2080Ti 13.45T 11G DVGO [ 9], DVGOv2 Telsa V100 15.67T 16G TensoRF [ 2]Titan RTX 16.31T 24G Plenoxels [ 10 ]RTX 3090 35.58T 24G Instant-NGP [ 7]  

> Table 2. GPU specs. FLOPs are theoretical for float32.

## 5. Experiments 

5.1. Ablation study for the CUDA speedup 

We test the re-implementation with 160 3 voxels on the 

lego , mic , and ship scenes. The PSNRs of different ver-sion are roughly the same. We present the results in Tab. 3,where the training time is measured on an RTX 2080Ti GPU and is 2–3× faster than the original implementation. We use the improved implementation in the rest of this technical re-port. 

Adam Rendering lego mic ship 

11.5m 9.3m 14.6m 

✓ 8.7m 1.3x 6.4m 1.5x 12.1m 1.2x 

✓ ✓ 4.8m 2.4x 3.4m 2.7x 7.1m 2.1x  

> Table 3. Speedup by the improved implementation.

5.2. Bounded inward-facing scenes 

We evaluate DVGOv2 on two bounded inward-facining datasets—Synthetic-NeRF [6] and Tanks&Temples [3]dataset (bounded ver.). The results are summarized in Tab. 4. DVGOv2’s training time is two more times faster than DVGO. DVGOv2 also uses less training time than most of the recent methods despite using the lowest spec GPU. The result qualities are also comparable to the recent methods. The improvement by scaling to a higher grid res-olution is limited on the Tanks&Temples [ 3] dataset, per-haps because of the photometric variation between training views. 

Method Tr. time PSNR ↑ SSIM ↑ LPIPS (VGG) ↓

DVGO [ 9] 14.2m 31.95 0.957 0.053 Plenoxels [ 10 ] 11.1m 31.71 0.958 0.049 

Instant-NGP [ 7] 5m 33.18 - -TensoRF (S) [ 2] 13.9m 32.39 0.957 0.057 TensoRF (L) [ 2] 8.1m 32.52 0.959 0.053 TensoRF (L) [ 2] 17.6m 33.14 0.963 0.047 

DVGOv2 (S) 4.9m 31.91 0.956 0.054 DVGOv2 (L) 6.8m 32.76 0.962 0.046   

> (a) Results on Synthetic-NeRF [ 6] dataset. The results are aver-aged over 8 scenes.

Method Tr. time PSNR ↑ SSIM ↑ LPIPS (VGG) ↓

DVGO [ 9] 17.7m 28.41 0.911 0.155 

TensoRF (S) [ 2] - 28.06 0.909 0.155 TensoRF (L) [ 2] - 28.56 0.920 0.140 

DVGOv2 (S) 7.3m 28.29 0.910 0.157 DVGOv2 (L) 9.1m 28.69 0.918 0.143          

> (b) Results on Tanks&Temples [ 3] dataset (bounded ver.). The results are averaged over 5 scenes. Table 4. Results on bounded inward scenes. We only compare with the recent fast convergence approaches. Our small and large models use 160 3and 256 3voxels respectively, and both are mea-sured on an RTX 2080Ti GPU. Results breakdown and rendered videos: https://sunset1995.github.io/dvgo/results.html .

35.3. Forward-facing scenes 

Points parameterization and sampling. We use NeRF’s parameterization to warp the unbounded forward-facing frustum to a bounded volume. In this case, the dense voxel grid allocation is similar to the multiplane images (MPIs) [ 12 ], where we place D RGB-density images at fixed depths, each with X × Z resolution. Every ray is traced from the first to the D-th images with a step size of s

image, i.e ., there are 2D − 1 sampled points if s = 0 .5.

Implementation details. The number of depth layers is 

D=256 each with XZ =384 2 number of voxels. Sampling step size is s=1 .0 layer. The TV loss weights are 10 −5 for the density grid and 10 −6 for the feature grid; the distortion loss weight is 10 −2.

Results. We compare DVGOv2 with the recent fast con-vergence approaches in Tab. 5. DVGOv2 shows comparable quality using less training time on the lowest spec GPU. We also see that the efficient distortion loss makes our training faster and achieves better quality, thanks to the compactness encouraged by the loss. We also note that we achieve sim-ilar performance using a much lower grid resolution. This is perhaps due to the other challenges in the LLFF dataset (e.g ., fewer training views with some multi-view inconsis-tency due to real-world capturing), which hinders the gain by using higher grid resolution. 

Method Tr. time PSNR ↑ SSIM ↑ LPIPS (VGG) ↓ 

> Plenoxels [ 10 ]

24.2m 26.29 0.839 0.210  

> TensoRF (S) [ 2]

19.7m 26.51 0.832 0.217  

> TensoRF (L) [ 2]

25.7m 26.73 0.839 0.204    

> DVGOv2 w/o Ldist

13.9m 26.24 0.833 0.204  

> DVGOv2

10.9m 26.34 0.838 0.197          

> Table 5. Results on LLFF [ 5] dataset. ‡The results are averaged over 8 scenes. The effective grid resolution is 1408 ×1156 ×128 for Plenoxels and 640 3for TensoRF, while ours is about 384 2×256 .

5.4. Unbounded inward-facing scenes 

Points parameterization and sampling. We adapt mip-NeRF 360 [ 1] parameterization for the unbounded 360 scenes, which is 

x′ =

{x, ‖x‖p ≤ 1 ; (

1 + b − b

> ‖x‖p

) ( x

> ‖x‖p

)

, ‖x‖p > 1 . (4) We first rotate the world coordinate to align the first two PCA directions of camera positions with grid’s XY axis, which slightly improves our results. The world coordinate is then shifted to align with cameras’ centroid and scaled to cover all cameras near planes in a unit sphere. We allocate a cuboid voxel grid centered at the origin with length 2+2 b.The hyperparameter b> 0 controls the proportion of voxel grid points allocated to the background. The sampling step size is measured on the contracted space. The original p=2 

wastes around 50% of the grid points (a sphere in a cube), so we also try p=∞ to make a cuboid contracted space. 

Implementation details. The grid resolution is 320 3. We set α(init) = 10 −4 [9] with 0.5 voxel step size. The TV loss weights are 10 −6 for the density grid and 10 −7 for the feature grid; the distortion loss weight is 10 −2.

Results. We show our results on the unbounded inward-facing scenes in Tab. 6 and Tab. 7. On the Tanks&Temples [ 3] dataset (Tab. 6), we achieve compara-ble SSIM and LPIPS to NeRF++, while our quality is be-hind the Plenoxels due to the grid resolution limited by the dense grid. On the newly released mip-NeRF 360 dataset (Tab. 7), we achieve NeRF comparable PSNR and SSIM, while our LPIPS is still far behind. One improvement is scaling the grid resolution as we only use 320 3 voxels, while advanced data structures [ 2, 7, 10 ] are necessary in this case. However, DVGOv2 could still be a good starting point for its simplicity (Pytorch, dense grid) with reasonable quality. Using a cuboid contracted space significantly improves our results on mip-nerf 360 dataset, while it degrades the results on Tanks&Temples dataset perhaps due to the photometric inconsistency problem in the dataset. Again, the distortion loss [ 1] with our efficient realization improves our quality and training speed. 

Method Tr. time PSNR ↑ SSIM ↑ LPIPS (VGG) ↓ 

> NeRF++ [ 11 ]

hours 20.49 0.648 0.478  

> Plenoxels [ 10 ]

27.3m 20.40 0.696 0.420    

> DVGOv2 w/o Ldist

22.1m 20.08 0.649 0.495  

> DVGOv2

16.0m 20.10 0.653 0.477            

> Table 6. Results on Tanks&Temples [ 3] dataset. ‡The results are averaged over the 4 scenes organoized by NeRF++ [ 11 ]. The grid resolution of Plenoxels is 640 3for foreground and 2048 ×
> 1024 ×64 for background, while ours is a single 320 3grid shared by foreground and background.

Method Tr. time PSNR ↑ SSIM ↑ LPIPS (VGG) ↓ 

> NeRF [ 6]

hours 24.85 0.659 0.426  

> NeRF++ [ 11 ]

hours 26.21 0.729 0.348  

> mip-NeRF 360 [ 1]

hours 28.94 0.837 0.208    

> DVGOv2 w/o Ldist

16.4m 24.73 0.663 0.465   

> DVGOv2 p=2

13.2m 24.80 0.659 0.468   

> DVGOv2 p=∞

14.0m 25.24 0.680 0.446   

> DVGOv2 p=∞(∗)

15.6m 25.42 0.695 0.429            

> (∗)Longer grid scaling and decaying schedule.
> Table 7. Results on mip-NeRF-360 [ 1] dataset. ‡The results are averaged over only the publicly available 7 scenes .
> ‡Find out results breakdown and rendered video at:
> https://sunset1995.github.io/dvgo/results.html

4References 

[1] Jonathan T. Barron, Ben Mildenhall, Dor Verbin, Pratul P. Srinivasan, and Peter Hedman. Mip-nerf 360: Unbounded anti-aliased neural radiance fields. 2022. 1, 2, 4

[2] Anpei Chen, Zexiang Xu, Andreas Geiger, Jingyi Yu, and Hao Su. Tensorf: Tensorial radiance fields. arxiv CS.CV 2203.09517 , 2022. 1, 2, 3, 4

[3] Arno Knapitsch, Jaesik Park, Qian-Yi Zhou, and Vladlen Koltun. Tanks and temples: benchmarking large-scale scene reconstruction. ACM Trans. Graph. , 2017. 3, 4

[4] Naruya Kondo, Yuya Ikeda, Andrea Tagliasacchi, Yutaka Matsuo, Yoichi Ochiai, and Shixiang Shane Gu. Vaxnerf: Revisiting the classic for voxel-accelerated neural radiance field. arxiv CS.CV 2111.13112 , 2021. 1

[5] Ben Mildenhall, Pratul P. Srinivasan, Rodrigo Ortiz-Cayon, Nima Khademi Kalantari, Ravi Ramamoorthi, Ren Ng, and Abhishek Kar. Local light field fusion: Practical view syn-thesis with prescriptive sampling guidelines. In SIGGRAPH ,2019. 4

[6] Ben Mildenhall, Pratul P. Srinivasan, Matthew Tancik, Jonathan T. Barron, Ravi Ramamoorthi, and Ren Ng. Nerf: Representing scenes as neural radiance fields for view syn-thesis. In ECCV , 2020. 1, 3, 4

[7] Thomas M¨ uller, Alex Evans, Christoph Schied, and Alexan-der Keller. Instant neural graphics primitives with a multires-olution hash encoding. ACM Trans. Graph. , 2022. 1, 3, 4

[8] Leonid I. Rudin and Stanley J. Osher. Total variation based image restoration with free local constraints. In ICIP , 1994. 

2

[9] Cheng Sun, Min Sun, and Hwann-Tzong Chen. Direct voxel grid optimization: Super-fast convergence for radiance fields reconstruction. In CVPR , 2022. 1, 3, 4

[10] Alex Yu, Sara Fridovich-Keil, Matthew Tancik, Qinhong Chen, Benjamin Recht, and Angjoo Kanazawa. Plenoxels: Radiance fields without neural networks. In CVPR , 2022. 1,

2, 3, 4

[11] Kai Zhang, Gernot Riegler, Noah Snavely, and Vladlen Koltun. Nerf++: Analyzing and improving neural radiance fields. arxiv CS.CV 2010.07492 , 2020. 4

[12] Tinghui Zhou, Richard Tucker, John Flynn, Graham Fyffe, and Noah Snavely. Stereo magnification: learning view syn-thesis using multiplane images. ACM Trans. Graph. , 2018. 

4

5