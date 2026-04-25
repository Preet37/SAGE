# Source: https://ar5iv.labs.arxiv.org/html/2101.05204
# Author: Frank Dellaert and Lin Yen-Chen
# Title: [2101.05204] Neural Volume Rendering: NeRF and Beyond - ar5iv
# Fetched via: trafilatura
# Date: 2026-04-09

Neural Volume Rendering: NeRF and Beyond
1 Introduction
Besides the COVID-19 pandemic and political upheaval in the US, 2020 was also the year in which neural volume rendering exploded onto the scene, triggered by the impressive NeRF paper by Mildenhall et al., ([2020](#bib.bib22)).
Both of us have tried to capture this excitement, Frank on a [blog post](https://dellaert.github.io/NeRF/) (Dellaert,, [2020](#bib.bib7)) and Yen-Chen in a [Github collection](https://github.com/yenchenlin/awesome-NeRF) (Yen-Chen,, [2020](#bib.bib40)).
This note is an annotated bibliography of the relevant papers, and we posted the associated bibtex file [on the repository](https://github.com/yenchenlin/awesome-NeRF).
To start with some definitions, the larger field of Neural Rendering is defined by the excellent review paper by Tewari et al., ([2020](#bib.bib35)) as
“deep image or video generation approaches that enable explicit or implicit control of scene properties such as illumination, camera parameters, pose, geometry, appearance, and semantic structure.”
It is a novel, data-driven solution to the long-standing problem in computer graphics of the realistic rendering of virtual worlds.
Neural volume rendering refers to methods that generate images or video by tracing a ray into the scene and taking an integral of some sort over the length of the ray. Typically a neural network like a multi-layer perceptron encodes a function from the 3D coordinates on the ray to quantities like density and color, which are integrated to yield an image.
Outline
Below we first discuss some very relevant related works that lead up to the “NeRF explosion”, then discuss the two papers that we think started it all, followed by an annotated bibliography on follow-up work. We are going wide rather than deep, and provide links to all project sites or Arxiv entries.
2 The Prelude: Neural Implicit Surfaces
The immediate precursors to neural volume rendering are the approaches that use a neural network to define an implicit surface representation. Many 3D-aware image generation approaches used voxels, meshes, point clouds, or other representations, typically based on convolutional architectures. But at CVPR 2019, no less than three papers introduced the use of neural nets as scalar function approximators to define occupancy and/or signed distance functions.
2.1 Occupancy and Signed Distance Functions
Below are the three papers from CVPR 2019, and one (PIFu) from ICCV 2019:
-
•
[Occupancy networks](https://avg.is.tuebingen.mpg.de/publications/occupancy-networks)(Mescheder et al.,,[2019](#bib.bib21)) introduce implicit, coordinate-based learning of occupancy. A network consisting of 5 ResNet blocks take a feature vector and a 3D point and predict binary occupancy. - •
- •
- •
2.2 Building on Implicit Functions
Several other approaches build on top of the implicit function idea.
-
•
[Structured Implicit Functions](https://ldif.cs.princeton.edu/)(Genova et al.,,[2019](#bib.bib14)) show that you can combine these implicit representations, e.g., simply by summing them. -
•
[CvxNet](https://cvxnet.github.io/)([Deng et al., 2020b,](#bib.bib9)) combines signed distance functions by taking a pointwise max (in 3D). The paper also has several other elegant techniques to reconstruct an object from depth or RGB images. - •
-
•
[Deep Local Shapes](https://arxiv.org/abs/2003.10983)(Chabra et al.,,[2020](#bib.bib3)) store a DeepSDF latent code in a voxel grid to represent larger, extended scenes. -
•
[Scene Representation Networks](https://vsitzmann.github.io/srns/)(Sitzmann et al.,,[2019](#bib.bib32)) or SRN are quite similar to DeepSDF in terms of architecture but adds a differentiable ray marching algorithm to find the closest point of intersection of a learned implicit surface, and add an MLP to regress color, enabling it to be learned from multiple posed images. -
•
[Differentiable Volumetric Rendering](https://avg.is.tuebingen.mpg.de/publications/niemeyer2020cvpr)(Niemeyer et al.,,[2019](#bib.bib24)) shows that an implicit scene representation can be coupled with a differentiable renderer, making it trainable from images, similar to SRN. They use the term volumetric renderer, but really the main contribution is a clever trick to make the computation of depth to the implicit surface differentiable: no integration over a volume is used. -
•
[Implicit Differentiable Renderer](https://lioryariv.github.io/idr/)(Yariv et al.,,[2020](#bib.bib39)) presents a similar technique, but has a more sophisticated surface light field representation, and also shows that it can refine camera pose during training. -
•
[Neural Articulated Shape Approximation](https://virtualhumans.mpi-inf.mpg.de/nasa/)([Deng et al., 2020c,](#bib.bib10)) or NASA composes implicit functions to represent articulated objects such as human bodies.
3 Neural Volume Rendering
As far as we know, two papers introduced volume rendering into the field, with NeRF being the simplest and ultimately the most influential.
A word about naming: the two papers below and all Nerf-style papers since build upon the work above that encode implicit surfaces, and so the term implicit neural methods is used quite a bit. However, especially in graphics that term is more associated with level-set representations for curves and surfaces. What they do have in common with occupancy/SDF-style networks is that MLP’s are used as functions from coordinates in 3D to a scalar or multi-variate fields, and hence these methods are also sometimes called coordinate-based scene representation networks. Of that larger set, we’re concerned with volume rendering versions of those below.
3.1 Neural Volumes
While not entirely in a vacuum, we believe volume rendering for view synthesis was introduced in the [Neural Volumes](https://research.fb.com/publications/neural-volumes-learning-dynamic-renderable-volumes-from-images/) paper by Lombardi et al., ([2019](#bib.bib19)), regressing a 3D volume of density and color, albeit still in a (warped) voxel-based representation. A latent code is decoded into a 3D volume, and a new image is then obtained by volume rendering.
One of the most interesting quotes from this paper hypothesizes about the success of neural volume rendering approaches (emphasis is ours):
[We] propose using a volumetric representation consisting of opacity and color at each position in 3D space, where rendering is realized through integral projection. During optimization, this semi-transparent representation of geometry disperses gradient information along the ray of integration, effectively widening the basin of convergence, enabling the discovery of good solutions.
We think that resonates with many people, and partially explains the success of neural volume rendering. We won’t go into any detail about the method itself, but the paper is a great read. Instead, let’s dive right into NeRF itself below…
3.2 NeRF
The paper that got everyone talking was the Neural Radiance Fields or [NeRF](https://www.matthewtancik.com/nerf) paper by Mildenhall et al., ([2020](#bib.bib22)). In essence, they take the DeepSDF architecture but regress not a signed distance function, but density and color. They then use an (easily differentiable) numerical integration method to approximate a true volumetric rendering step.
A NeRF model stores a volumetric scene representation as the weights of an MLP, trained on many images with known pose. New views are rendered by integrating the density and color at regular intervals along each viewing ray.
One of the reasons NeRF is able to render with great detail is because it encodes a 3D point and associated view direction on a ray using periodic activation functions, i.e., Fourier Features. This innovation was later generalized to multi-layer networks with periodic activations, aka SIREN (SInusoidal REpresentation Networks). Both were published later at NeurIPS 2020.
While the NeRF paper was ostensibly published at ECCV 2020, at the end of August, it first appeared on Arxiv in the middle of March, sparking an explosion of interest, not only because of the quality of the synthesized views, but perhaps even more so at the incredible detail in the visualized depth maps.
Arguably, the impact of the NeRF paper lies in its brutal simplicity: just an MLP taking in a 5D coordinate and outputting density and color. There are some bells and whistles, notably positional encoding and a stratified sampling scheme, but many researchers were taken aback (we think) that such a simple architecture could yield such impressive results. That being said, vanilla NeRF left many opportunities to improve upon:
-
•
It is slow, both for training and rendering.
-
•
It can only represent static scenes.
-
•
It “bakes in” lighting.
-
•
A trained NeRF representation does not generalize to other scenes/objects.
In this Arxiv-fueled computer vision world, these opportunities were almost immediately capitalized on, with almost 25 papers appearing on Arxiv in the span of six months. Below we list all of them we could find.
4 Performance
Several projects/papers aim at improving the rather slow training and rendering time of the original NeRF paper.
-
•
[JaxNeRF](https://github.com/google-research/google-research/tree/master/jaxnerf)([Deng et al., 2020a,](#bib.bib8)) uses JAX (https://github.com/google/jax) to dramatically speed up training using multiple devices, from days to hours. - •
-
•
[Learned Initializations](https://arxiv.org/abs/2012.02189)(Tancik et al.,,[2020](#bib.bib34)) uses meta-learning to find a good weight initialization for faster training. - •
- •
-
•
[Neural Sparse Voxel Fields](https://github.com/facebookresearch/NSVF)(Liu et al.,,[2020](#bib.bib18)) organize the scene into a sparse voxel octree to speed up rendering by a factor of 10.
5 Dynamic
At least four efforts focus on dynamic scenes, using a variety of schemes.
- •
- •
-
•
[Neural Scene Flow Fields](http://www.cs.cornell.edu/~zl548/NSFF/)(Li et al.,,[2020](#bib.bib16)) take a monocular video with known camera poses as input but use depth predictions as a prior, and regularize by also outputting scene flow, used in the loss. -
•
[Space-Time Neural Irradiance Fields](https://video-nerf.github.io/)(Xian et al.,,[2020](#bib.bib38)) simply use time as an additional input. Carefully selected losses are needed to successfully train this method to render free-viewpoint videos (from RGBD data!). -
•
NeRFlow (Du et al.,,
[2020](#bib.bib11)) uses a deformation MLP to model scene flow and integrates it across time to obtain the final deformation. - •
- •
Besides Nerfies, two other papers focus on avatars/portraits of people.
-
•
[Portrait NeRF](https://portrait-nerf.github.io/)(Gao et al.,,[2020](#bib.bib13)) creates static NeRF-style avatars but does so from a single RGB headshot. To make this work, light-stage training data is required. - •
6 Relighting
Another dimension in which NeRF-style methods have been augmented is in how to deal with lighting, typically through latent codes that can be used to re-light a scene.
- •
- •
-
•
[Neural Reflectance Fields](http://cseweb.ucsd.edu/~bisai/)(Bi et al.,,[2020](#bib.bib1)) improve on NeRF by adding a local reflection model in addition to density. It yields impressive relighting results, albeit from single point light sources. - •
7 Shape
Latent codes can also be used to encode shape priors.
- •
- •
- •
- •
8 Composition
It could be argued that none of this will scale to large scenes composed of many objects, so an exciting new area of interest is how to compose objects into volume-rendered scenes.
-
•
[Object-Centric Neural Scene Rendering](https://shellguo.com/osf/)(Guo et al.,,[2020](#bib.bib15)) learns ”Object Scattering Functions” in object-centric coordinate frames, allowing for composing scenes and realistically lighting them, using Monte Carlo rendering. - •
-
•
[Neural Scene Graphs](https://arxiv.org/abs/2011.10379)(Ost et al.,,[2020](#bib.bib25)) supports several object-centric NeRF models in a scene graph.
9 Pose Estimation
Finally, at least one paper has used NeRF rendering in the context of (known) object pose estimation.
10 Concluding Thoughts
Neural Volume Rendering and NeRF-style papers have exploded on the scene in 2020, and the last word has not been said. This note definitely does not rise to the level of a thorough review, but we hope that an annotated bibliography is useful for people working in this area or thinking of joining the fray.
However, it is far from clear -even in the face of all this excitement- that neural volume rendering is going to carry the day in the end. While the real world does have haze, smoke, transparencies, etc., in the end, most of the light is scattered into our eyes from surfaces. NeRF-style networks might be easily trainable because of their volume-based approach, but we already see a trend where authors are trying to discover or guess the surfaces after convergence. In fact, the stratified sampling scheme in the original NeRF paper is exactly that. Hence, as we learn from the NeRF explosion we can easily see the field moving back to SDF-style implicit representations or even voxels, at least at inference time.
References
- Bi et al., (2020) Bi, S., Xu, Z., Srinivasan, P., Mildenhall, B., Sulkavalli, K., Hašan, M., Hold-Geoffroy, Y., Kriegman, D., and Ramamoorthi, R. (2020). Neural reflectance fields for appearance acquisition. https://arxiv.org/abs/2008.03824.
- Boss et al., (2020) Boss, M., Braun, R., Jampani, V., Barron, J. T., Liu, C., and Lensch, H. (2020). NeRD: Neural reflectance decomposition from image collections. https://arxiv.org/abs/2012.03918.
- Chabra et al., (2020) Chabra, R., Lenssen, J., Ilg, E., Schmidt, T., Straub, J., Lovegrove, S., and Newcombe, R. (2020). Deep local shapes: Learning local SDF priors for detailed 3D reconstruction. In The European Conference on Computer Vision (ECCV).
- Chan et al., (2020) Chan, E., Monteiro, M., Kellnhofer, P., Wu, J., and Wetzstein, G. (2020). pi-GAN: Periodic implicit generative adversarial networks for 3D-aware image synthesis. https://arxiv.org/abs/2012.00926.
- Chen et al., (2020) Chen, Z., Tagliasacchi, A., and Zhang, H. (2020). BSP-Net: Generating compact meshes via binary space partitioning. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 45–54.
- Chen and Zhang, (2019) Chen, Z. and Zhang, H. (2019). Learning implicit fields for generative shape modeling. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 5939–5948.
- Dellaert, (2020) Dellaert, F. (2020). NeRF Explosion 2020. https://dellaert.github.io/NeRF/.
- (8) Deng, B., Barron, J. T., and Srinivasan, P. (2020a). JaxNeRF: an efficient JAX implementation of NeRF. https://github.com/google-research/google-research/tree/master/jaxnerf.
- (9) Deng, B., Genova, K., Yazdani, S., Bouaziz, S., Hinton, G., and Tagliasacchi, A. (2020b). CvxNet: Learnable convex decomposition. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 31–44.
- (10) Deng, B., Lewis, J., Jeruzalski, T., Pons-Moll, G., Hinton, G., Norouzi, M., and Tagliasacchi, A. (2020c). Neural articulated shape approximation. In The European Conference on Computer Vision (ECCV). Springer.
- Du et al., (2020) Du, Y., Zhang, Y., Yu, H.-X., Tenenbaum, J. B., and Wu, J. (2020). Neural radiance flow for 4D view synthesis and video processing. arXiv preprint arXiv:2012.09790.
- Gafni et al., (2020) Gafni, G., Thies, J., Zollhöfer, M., and Nießner, M. (2020). Dynamic neural radiance fields for monocular 4D facial avatar reconstruction. https://arxiv.org/abs/2012.03065.
- Gao et al., (2020) Gao, C., Shih, Y., Lai, W.-S., Liang, C.-K., and Huang, J.-B. (2020). Portrait neural radiance fields from a single image. https://arxiv.org/abs/2012.05903.
- Genova et al., (2019) Genova, K., Cole, F., Vlasic, D., Sarna, A., Freeman, W., and Funkhouser, T. (2019). Learning shape templates with structured implicit functions. In Proceedings of the IEEE International Conference on Computer Vision (ICCV), pages 7154–7164.
- Guo et al., (2020) Guo, M., Fathi, A., Wu, J., and Funkhouser, T. (2020). Object-centric neural scene rendering. https://arxiv.org/abs/2012.08503.
- Li et al., (2020) Li, Z., Niklaus, S., Snavely, N., and Wang, O. (2020). Neural scene flow fields for space-time view synthesis of dynamic scenes. https://arxiv.org/abs/2011.13084.
- Lindell et al., (2020) Lindell, D., Martel, J., and Wetzstein, G. (2020). AutoInt: Automatic integration for fast neural volume rendering. https://arxiv.org/abs/2012.01714.
- Liu et al., (2020) Liu, L., Gu, J., Lin, K. Z., Chua, T.-S., and Theobalt, C. (2020). Neural sparse voxel fields. In Advances in Neural Information Processing Systems (NeurIPS), volume 33.
- Lombardi et al., (2019) Lombardi, S., Simon, T., Saragih, J., Schwartz, G., Lehrmann, A., and Sheikh, Y. (2019). Neural volumes: Learning dynamic renderable volumes from images. ACM Trans. Graph.
- Martin-Brualla et al., (2020) Martin-Brualla, R., Radwan, N., Sajjadi, M., Barron, J. T., Dosovitskiy, A., and Duckworth, D. (2020). NeRF in the wild: Neural radiance fields for unconstrained photo collections. https://arxiv.org/abs/2008.02268.
- Mescheder et al., (2019) Mescheder, L., Oechsle, M., Niemeyer, M., Nowozin, S., and Geiger, A. (2019). Occupancy Networks: Learning 3D reconstruction in function space. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
- Mildenhall et al., (2020) Mildenhall, B., Srinivasan, P. P., Tancik, M., Barron, J. T., Ramamoorthi, R., and Ng, R. (2020). NeRF: Representing scenes as neural radiance fields for view synthesis. In The European Conference on Computer Vision (ECCV).
- Niemeyer and Geiger, (2020) Niemeyer, M. and Geiger, A. (2020). GIRAFFE: Representing scenes as compositional generative neural feature fields. https://arxiv.org/abs/2011.12100.
- Niemeyer et al., (2019) Niemeyer, M., Mescheder, L., Oechsle, M., and Geiger, A. (2019). Differentiable volumetric rendering: Learning implicit 3D representations without 3D supervision. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR).
- Ost et al., (2020) Ost, J., Mannan, F., Thürey, N., Knodt, J., and Heide, F. (2020). Neural scene graphs for dynamic scenes. https://arxiv.org/abs/2011.10379.
- Park et al., (2019) Park, J. J., Florence, P., Straub, J., Newcombe, R., and Lovegrove, S. (2019). DeepSDF: Learning continuous signed distance functions for shape representation. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR), pages 165–174.
- Park et al., (2020) Park, K., Sinha, U., Barron, J. T., Bouaziz, S., Goldman, D., Seitz, S., and Martin-Brualla, R. (2020). Deformable neural radiance fields. https://arxiv.org/abs/2011.12948.
- Pumarola et al., (2020) Pumarola, A., Corona, E., Pons-Moll, G., and Moreno-Noguer, F. (2020). D-NeRF: Neural radiance fields for dynamic scenes. https://arxiv.org/abs/2011.13961.
- Rebain et al., (2020) Rebain, D., Jiang, W., Yazdani, S., Li, K., Yi, K. M., and Tagliasacchi, A. (2020). DeRF: Decomposed radiance fields. https://arxiv.org/abs/2011.12490.
- Saito et al., (2019) Saito, S., Huang, Z., Natsume, R., Morishima, S., Kanazawa, A., and Li, H. (2019). PIFu: Pixel-aligned implicit function for high-resolution clothed human digitization. In Proceedings of the IEEE International Conference on Computer Vision (ICCV).
- Schwarz et al., (2020) Schwarz, K., Liao, Y., Niemeyer, M., and Geiger, A. (2020). Graf: Generative radiance fields for 3D-aware image synthesis. In Advances in Neural Information Processing Systems (NeurIPS), volume 33.
- Sitzmann et al., (2019) Sitzmann, V., Zollhöfer, M., and Wetzstein, G. (2019). Scene representation networks: Continuous 3D-structure-aware neural scene representations. In Advances in Neural Information Processing Systems (NeurIPS), pages 1121–1132.
- Srinivasan et al., (2020) Srinivasan, P., Deng, B., Zhang, X., Tancik, M., Mildenhall, B., and Barron, J. T. (2020). NeRV: Neural reflectance and visibility fields for relighting and view synthesis. https://arxiv.org/abs/2012.03927.
- Tancik et al., (2020) Tancik, M., Mildenhall, B., Wang, T., Schmidt, D., Srinivasan, P., Barron, J. T., and Ng, R. (2020). Learned initializations for optimizing coordinate-based neural representations. https://arxiv.org/abs/2012.02189.
- Tewari et al., (2020) Tewari, A., Fried, O., Thies, J., Sitzmann, V., Lombardi, S., Sunkavalli, K., Martin-Brualla, R., Simon, T., Saragih, J., Nießner, M., Pandey, R., Fanello, S., Wetzstein, G., Zhu, J.-Y., Theobalt, C., Agrawala, M., Shechtman, E., Goldman, D. B., and Zollhöfer, M. (2020). State of the Art on Neural Rendering. Computer Graphics Forum (EG STAR 2020).
- Tretschk et al., (2020) Tretschk, E., Tewari, A., Golyanik, V., Zollhöfer, M., Lassner, C., and Theobalt, C. (2020). Non-rigid neural radiance fields: Reconstruction and novel view synthesis of a deforming scene from monocular video. https://arxiv.org/abs/2012.12247.
- Trevithick and Yang, (2020) Trevithick, A. and Yang, B. (2020). GRF: Learning a general radiance field for 3D scene representation and rendering. https://arxiv.org/abs/2010.04595.
- Xian et al., (2020) Xian, W., Huang, J.-B., Kopf, J., and Kim, C. (2020). Space-time neural irradiance fields for free-viewpoint video. https://arxiv.org/abs/2011.12950.
- Yariv et al., (2020) Yariv, L., Kasten, Y., Moran, D., Galun, M., Atzmon, M., Basri, R., and Lipman, Y. (2020). Multiview neural surface reconstruction by disentangling geometry and appearance. In Advances in Neural Information Processing Systems (NeurIPS).
- Yen-Chen, (2020) Yen-Chen, L. (2020). Awesome neural radiance fields. https://github.com/yenchenlin/awesome-NeRF.
- Yen-Chen et al., (2020) Yen-Chen, L., Florence, P., Barron, J. T., Rodriguez, A., Isola, P., and Lin, T.-Y. (2020). iNeRF: Inverting neural radiance fields for pose estimation. https://arxiv.org/abs/2012.05877.
- Yu et al., (2020) Yu, A., Ye, V., Tancik, M., and Kanazawa, A. (2020). pixelNeRF: Neural radiance fields from one or few images. https://arxiv.org/abs/2012.02190.
- Yuan et al., (2021) Yuan, W., Lv, Z., Schmidt, T., and Lovegrove, S. (2021). STaR: Self-supervised tracking and reconstruction of rigid objects in motion with neural rendering. arXiv preprint arXiv:2101.01602.
- Zhang et al., (2020) Zhang, K., Riegler, G., Snavely, N., and Koltun, V. (2020). NERF++: Analyzing and improving neural radiance fields. https://arxiv.org/abs/2010.07492.