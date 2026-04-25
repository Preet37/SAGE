# Source: https://www.cs.umd.edu/~zwicker/publications/EWASplatting-TVCG02.pdf
# Title: [PDF] EWA Splatting - UMD Department of Computer Science
# Fetched via: jina
# Date: 2026-04-09

Title: 223 223..238



Number of Pages: 16

# EWA Splatting Matthias Zwicker, Hanspeter Pfister, Member , IEEE ,Jeroen van Baar, and Markus Gross, Member , IEEE 

Abstract —In this paper, we present a framework for high quality splatting based on elliptical Gaussian kernels. To avoid aliasing artifacts, we introduce the concept of a resampling filter, combining a reconstruction kernel with a low-pass filter. Because of the similarity to Heckbert’s EWA (elliptical weighted average) filter for texture mapping, we call our technique EWA splatting. Our framework allows us to derive EWA splat primitives for volume data and for point-sampled surface data. It provides high image quality without aliasing artifacts or excessive blurring for volume data and, additionally, features anisotropic texture filtering for point-sampled surfaces. It also handles nonspherical volume kernels efficiently; hence, it is suitable for regular, rectilinear, and irregular volume datasets. Moreover, our framework introduces a novel approach to compute the footprint function, facilitating efficient perspective projection of arbitrary elliptical kernels at very little additional cost. Finally, we show that EWA volume reconstruction kernels can be reduced to surface reconstruction kernels. This makes our splat primitive universal in rendering surface and volume data. 

Index Terms —Rendering systems, volume rendering, texture mapping, splatting, antialiasing. 

# Ê

# 1 I NTRODUCTION 

# V OLUME rendering is an important technique in visualiz-ing acquired and simulated datasets in scientific and engineering applications. The ideal volume rendering algorithm reconstructs a continuous function in 3D, trans-forms this 3D function into screen space, and then evaluates opacity integrals along line-of-sights. In 1989, Westover [1], [2] introduced splatting for interactive volume rendering, which approximates this procedure. Splatting algorithms interpret volume data as a set of particles that are absorbing and emitting light. Line integrals are precomputed across each particle separately, resulting in footprint functions . Each footprint, or splat, spreads its contribution in the image plane. These contributions are composited back to front into the final image. On the other hand, laser range and image-based scanning techniques have produced some of the most complex and visually stunning graphics models to date [3], resulting in huge sets of surface point samples. Acommonly used approach is generating triangle meshes from the point data and using mesh reduction techniques to render them [4], [5]. In contrast, recent efforts have focused on direct rendering techniques for point samples without connectivity [6], [7], [8]. Most of these approaches are based on a splatting approach similar to splatting in volume rendering. In this paper, we present a framework for high quality splatting. Our derivation proceeds along similar lines as Heckbert’s elliptical weighted average (EWA) texture filter [9], therefore, we call our algorithm EWA splatting . The main feature of EWA splatting is that it integrates an elliptical Gaussian reconstruction kernel and a low-pass filter, there-fore preventing aliasing artifacts in the output image while avoiding excessive blurring. Moreover, we use the same framework to derive splat primitives for volume as well as for surface data. EWA volume splatting works with arbitrary elliptical Gaussian reconstruction kernels and efficiently supports perspective projection. Our method is based on a novel approach to compute the footprint function, which relies on the transformation of the volume data to so-called ray space .This transformation is equivalent to perspective projection. By using its local affine approximation at each voxel, we derive an analytic expression for the EWA footprint in screen space. The EWA volume splat primitive can be easily integrated into conventional volume splatting algorithms. Because of its flexibility, it can be utilized to render rectilinear, curvilinear, or unstructured volume datasets. The rasterization of the footprint is performed using forward differencing, requiring only one 1D footprint table for all reconstruction kernels and any viewing direction. EWA surface splatting is equivalent to a screen space formulation of the EWA texture filter for triangle rendering pipelines [10]. Hence, it provides high quality, anisotropic texture filtering for point-sampled surfaces. We will show that EWA surface splatting can be derived from EWA volume splatting by reducing Gaussian volume reconstruction kernels to surface reconstruction kernels. Hence, EWA splats are a universal rendering primitive for volume and for surface data. For example, we can perform high quality iso-surface rendering by flattening the 3D Gaussian kernels along the volume gradient. The paper is organized as follows: We discuss previous work in Section 2. In Section 3, we review fundamental results from signal processing theory that are needed to analyze aliasing. We also present the general concept of an ideal resampling filter that prevents aliasing during render-ing by combining a reconstruction kernel and a low-pass     

> IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002 223

. M. Zwicker and M. Gross are with the Computer Graphics Laboratory, ETH Zentrum, 8092 Zurich, Switzerland. E-mail: {zwicker, gross}@inf.ethz.ch. 

. H. Pfister and J. van Baar are with MERL—Mitsubishi Electric Research Laboratories, Cambridge, MA 02139. E-mail: {pfister, jeroen}@merl.com. Manuscript received 15 Feb. 2002; revised 15 Mar. 2002; accepted 2 Apr. 2002. For information on obtaining reprints of this article, please send e-mail to: tvcg@computer.org, and reference IEEECS Log Number 116207.   

> 1077-2626/02/$17.00 fl 2002 IEEE

filter. Next, we describe how to model volume rendering as a resampling process in Section 4, leading to the formula-tion of an ideal volume resampling filter. Similarly, we derive an ideal resampling filter for rendering point-sampled surfaces in Section 5. In Section 6, we introduce the EWA resampling filter, which uses elliptical Gaussians as reconstruction kernel and as low-pass filter. We present explicit formulas for both the EWA volume resampling filter and the EWA surface resampling filter. Moreover, we show how to derive the surface resampling filter as a special case of the volume resampling filter by flattening the volume reconstruction kernels. Finally, Sections 7 and 8 discuss our implementation and results and Section 9concludes the paper. 

# 2 PREVIOUS W ORK 

The original work on splatting in the context of volume rendering was presented by Westover [1]. Basic volume splatting algorithms suffer from inaccurate visibility deter-mination when compositing the splats from back to front. This leads to visible artifacts, such as color bleeding. Later, Westover [2] solved the problem using an axis-aligned sheet buffer. However, this technique is plagued by disturbing popping artifacts in animations. Recently, Mueller and Crawfis [11] proposed aligning the sheet buffers parallel to the image plane instead of parallel to an axis of the volume data. Additionally, they splat several slices of each reconstruction kernel separately. This technique is similar to slice-based volume rendering [12], [13] and does not suffer from popping artifacts. Mueller and Yagel [14] combine splatting with ray casting techniques to accelerate rendering with perspective projection. Laur and Hanrahan [15] describe a hierarchical splatting algorithm enabling pro-gressive refinement during rendering. Furthermore, Lippert and Gross [16] introduced a splatting algorithm that directly uses a wavelet representation of the volume data. Additional care has to be taken if the 3D kernels are not radially symmetric, as is the case for rectilinear, curvilinear, or irregular grids. In addition, for an arbitrary position in 3D, the contributions from all kernels must sum up to one. Otherwise, artifacts such as splotches occur in the image. For rectilinear grids, Westover [2] proposes using elliptical footprints that are warped back to a circular footprint. To render curvilinear grids, Mao [17] uses stochastic Poisson resampling to generate a set of new points whose kernels are spheres or ellipsoids. He computes the elliptical footprints very similarly to Westover [2]. As pointed out in Section 6.2, our technique can be used with rectilinear, curvilinear, and irregular grids to efficiently and accurately project and rasterize the elliptical splat kernels. Westover’s original framework does not deal with sampling rate changes due to perspective projections. Aliasing artifacts may occur in areas of the volume where the sampling rate of diverging rays falls below the volume grid sampling rate. The aliasing problem in volume splatting has first been addressed by Swan et al. [18] and Mueller et al. [19]. They use a distance-dependent stretch of the footprints to make them act as low-pass filters. In contrast, EWA splatting models both reconstructing and band limiting the texture function in a unified framework. The concept of representing surfaces as a set of points and using these as rendering primitives has been intro-duced in a pioneering report by Levoy and Whitted [20]. Due to the continuing increase in geometric complexity, their idea has recently gained more interest. QSplat [6] is a point rendering system that was designed to interactively render large data sets produced by modern scanning devices. Other researchers demonstrated the efficiency of point-based methods for rendering geometrically complex objects [7], [8]. In some systems, point-based representa-tions are temporarily stored in the rendering pipeline to accelerate rendering [21], [22]. We have systematically addressed the problem of representing texture functions on point-sampled objects and avoiding aliasing during rendering in [23]. The surface splatting technique can replace the heuristics used in previous methods and provide superior texture quality. We develop EWA splatting along similar lines to the seminal work of Heckbert [9], who introduced EWA filtering to avoid aliasing of surface textures. We recently extended his framework to represent and render texture functions on irregularly point-sampled surfaces [23] and to volume splatting [24]. Section 6.4 will show the connection between EWA volume and surface splatting. 

# 3 I DEAL RESAMPLING 3.1 Sampling and Aliasing 

Aliasing is a fundamental problem in computer graphics. Although, conceptually, computer graphics often deals with continuous representations of graphics models, in practice, computer-generated images are represented by a discrete array of samples. Image synthesis involves the conversion between continuous and discrete representations, which may cause aliasing artifacts such as moire ´ patterns and jagged edges, illustrated in Fig. 1, or flickering in animations. To study aliasing, it is useful to interpret images, surface textures, or volume data as multidimensional signals. In the following discussion, we will focus on one-dimensional signals and return to multidimensional signals in Sections 4 and 5. When a continuous signal is converted to a discrete signal it is evaluated, or sampled , on a discrete grid. To analyze the effects of sampling and to understand the relation between the continuous and the discrete representation of     

> 224 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002
> Fig. 1. Aliasing artifacts. Note the moire ´ patterns and jagged edges.

a signal, we review some definitions and results from signal processing theory. A filter is a process that takes a signal as an input and generates a modified signal or a response as an output. The easiest class of filters to understand are linear space invariant 

filters. A linear space invariant filter L is uniquely characterized by its impulse response hðxÞ, i.e., its output resulting from an impulse input. As a consequence, the response of a linear space invariant filter to any input signal 

fðxÞ is given by the convolution of fðxÞ and hðxÞ:

Lf fðxÞg ¼ 

Z þ1 ˇ1 

fðtÞhðx ˇ tÞdt ¼ ð f hÞð xÞ:

A fundamental approach to analyze a filter is to compute its eigenfunctions and eigenvalues. The eigenfunctions of linear time invariant filters are complex exponentials and the eigenvalues are given by the Fourier transform of its impulse response, which is called frequency response . The Fourier transform of a signal fðxÞ is called the spectrum of the signal, denoted by F ð!Þ, where ! is the angular frequency. We write fðxÞ $ F ð!Þ to relate the spatial and the frequency domain representation of the signal. One of the most useful properties of the Fourier transform is that the Fourier transform of the convolution of two signals is the product of their Fourier transforms, i.e., f g $ F G and vice versa, i.e., fg $ F G= 2.We analyze the sampling of a continuous signal using the Fourier transform and frequency domain representa-tions, shown in Fig. 2. Sampling a continuous signal acðxÞ

is performed by multiplying it with an impulse train iðxÞ,which is a sum of unit-spaced impulses, i.e., iðxÞ ¼ P 

> n

ðx ˇ nÞ (Fig. 2b). This yields the discrete signal 

aðxÞ ¼ a cðxÞiðx=T Þ, where T is the sample distance. In the frequency domain, this results in the spectrum of the discrete signal Að!Þ given by the convolution 

Að!Þ ¼ Acð!Þ Ið!Þ=2. Since the Fourier transform of the impulse train iðx=T Þ is another impulse train 

Ið!Þ ¼ ! s ið!=! sÞ, !s ¼ 2=T , the spectrum of the discrete signal consists of a superposition of replicas of the spectrum of the continuous signal spaced at a distance !s (Fig. 2c). To reconstruct the continuous signal, we have to eliminate all replicas of Ac from A except the central one. If the replicas do not overlap, this is achieved by multi-plying Að!Þ with a box function H ! s ð!Þ ¼ 1 for !  ! s and 0

otherwise. H ! s is called an ideal low-pass filter with cutoff frequency ! s, where ! s =2 is also called the Nyquist frequency of the sampling grid. In the spatial domain, the impulse response of H ! s is a sinc function. However, if the maximum frequency ! a in the spectrum of A c is higher than 

! s as shown in Fig. 2, the replicas overlap and it is impossible to reconstruct the original spectrum Ac from A

(Fig. 2c). High frequencies from the replicas appear as low frequencies in the original spectrum (Fig. 2e), which is called aliasing .

3.2 Antialiasing 

From the above discussion, we conclude that there are two approaches to reduce aliasing problems: We can either sample the continuous signal at a higher frequency or we eliminate frequencies above the Nyquist limit before sampling, which is called prefiltering . Since most signals of interest are not band limited, sampling at a higher frequency will alleviate, but not completely avoid, aliasing. Moreover, increasing the sampling frequency leads to higher memory and computational requirements of most algorithms. On the other hand, prefiltering is performed by applying a low-pass filter to the signal before sampling, hence it is the more theoretically justified antialiasing method. Using an ideal low-pass filter with cutoff frequency !s =2, the filtered signal will be band limited to the Nyquist frequency of the sampling grid and, thus, it can be reconstructed exactly. In practice, prefiltering is im-plemented as a convolution in the spatial domain, hence prefilters with a small support are desirable for efficiency reasons. However, the widths of a filter in the spatial and frequency domains are inversely related; therefore, some aliasing will be inevitable during sampling. 

3.3 Rendering and Ideal Resampling Filters 

In our framework, graphics models are represented as a set of irregularly spaced samples of multidimensional func-tions describing object attributes such as volume opacity (Section 4) or surface textures (Section 5). We reconstruct the continuous attribute functions by computing a weighted sum  

> ZWICKER ET AL.: EWA SPLATTING 225
> Fig. 2. Frequency analysis of aliasing.

f cðuÞ ¼ X

> k2

IN 

w k r kðuÞ; ð1Þ

where r k is called a reconstruction kernel centered at the sample position uk and wk is a sample value, e.g., the diffuse color at uk. We use the term source space to denote the domain of fcðuÞ.We interpret rendering an attribute function (1) as a resampling process, involving the three steps illustrated in Fig. 3: 

1. Project f cðuÞ from source to screen space, yielding the continuous screen space signal g cðxÞ:

g cðxÞ ¼ fPð f cÞgð xÞ; ð2Þ

where x are 2D screen space coordinates and projection is denoted by the projection operator P.Note that the operators P used for rendering (Sections 4 and 5) are linear in their arguments (however, this does not imply that the projection performed by P is a linear mapping). Therefore, we can reformulate (2) by first projecting the reconstruc-tion kernels before computing the sum: 

gcðxÞ ¼ P X

> k2

IN 

wk r k

0@1A8<:9=;ðxÞ ¼ X

> k2

IN 

wk p kðxÞ; ð3Þ

introducing the abbreviation p k ¼ P r k for the pro-jected reconstruction kernels. 

2. Band limit the screen space signal using a prefilter h,resulting in the continuous output function g0

> c

ðxÞ:

g0

> c

ðxÞ ¼ gcðxÞ hðxÞ ¼ 

Z

IR 2 gcðÞhðx ˇ Þd : ð4Þ

3. Sample the continuous output function by multi-plying it with an impulse train i to produce the discrete output gðxÞ:

gðxÞ ¼ g0

> c

ðxÞiðxÞ:

An explicit expression for the projected continuous output function can be derived by expanding the above relations in reverse order: 

g0

> c

ðxÞ ¼ 

Z

IR 2 P X

> k2

IN 

wk rk

0@1A8<:9=;ðÞhðx ˇ Þ d 

¼ X

> k2

IN 

wk

Z

IR 2 p kðÞhðx ˇ Þ d 

¼ X

> k2

IN 

wk  kðxÞ;

ð5Þ

where kðxÞ ¼ ð p k hÞð xÞ: ð6Þ

We call a projected and filtered reconstruction kernel kðxÞ

an ideal resampling kernel , which is expressed here as a convolution in screen space. Exploiting the linearity of the projection operator, (5) states that we can first project and filter each reconstruction kernel r k individually to derive the resampling kernels k and then sum up the contribu-tions of these kernels in screen space. In the following Sections 4 and 5, we will model the rendering process for volume data and for point-sampled surfaces, respectively, as a resampling problem by expres-sing it in the form of (5) and (6). Since this resampling technique is based on the prefiltering approach to antialias-ing, it leads to high image quality with few aliasing artifacts, irrespective of the spectrum of the unfiltered screen space signal. 

# 4 V OLUME RESAMPLING 

We distinguish two fundamental approaches to volume rendering: backward mapping algorithms that shoot rays through pixels on the image plane into the volume data and forward mapping algorithms that map the data onto the image plane. In the following discussion, we will describe a forward mapping technique. Mapping the data onto the image plane involves a sequence of intermediate steps where the data is transformed to different coordinate systems, as in conventional rendering pipelines. We introduce our terminology in Fig. 4. Note that the terms 

space and coordinate system are synonymous. The figure summarizes a forward mapping volume rendering pipeline ,where the data flows from the left to the right. As an overview, we briefly describe the coordinate systems and transformations that are relevant for our technique. We will deal in detail with the effect of the transformations in Section 6.2. The volume data is initially given in source space, which is usually called object space in     

> 226 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002
> Fig. 3. Projection, filtering, and sampling of a 1D attribute function.
> Fig. 4. The forward mapping volume rendering pipeline.

this context. To render the data from an arbitrary viewpoint, it is first mapped to camera space using the viewing transformation. The camera coordinate system is defined such that its origin is at the center of projection. We further transform the data to ray space , which is introduced in Section 4.1. Ray space is a non-Cartesian coordinate system that enables an easy formulation of the volume rendering equation. In ray space, the viewing rays are parallel to a coordinate axis, facilitating analytical integration of the volume function. We present the transformation from camera to ray space in Section 6.2; it is a key element of our technique. Since its purpose is similar to the projective transform used in rendering pipelines such as OpenGL, it is also called the projective mapping .Evaluating the volume rendering equation results in a 2D image in screen space . In a final step, this image is transformed to viewport coordinates . Focusing on the essential aspects of our technique, we are not covering the viewport transformation in the following explanations. However, it can be easily incorporated in an implementa-tion. Moreover, we do not discuss volume classification and shading in a forward mapping pipeline, but refer to [25] or [26] for a thorough discussion. 

4.1 Splatting Algorithms 

We review the low albedo approximation of the volume rendering equation [27], [28] as used for fast, direct volume rendering [2], [29], [25], [30]. The left part of Fig. 5 illustrates the corresponding situation in 2D. Starting from this form of the rendering equation, we discuss several simplifying assumptions leading to the well-known splatting formula-tion. Because of their efficiency, splatting algorithms [2], [25] belong to the most popular forward mapping volume rendering techniques. We slightly modify the conventional notation, intro-ducing our concept of ray space. We denote a point in ray space by a column vector of three coordinates 

x ¼ ð x0; x 1; x 2ÞT . Given a center of projection and aprojection plane, these three coordinates are interpreted geometrically as follows: The coordinates x0 and x1 specify a point on the projection plane. The ray intersecting the center of projection and the point ðx0; x 1Þ on the projection plane is called a viewing ray. Using the abbreviation 

x ¼ ð x0; x 1ÞT , we also refer to the viewing ray passing through ðx0; x 1Þ as x. The third coordinate x2 specifies the Euclidean distance from the center of projection to a point on the viewing ray. Note that our notation does not distinguish between a ray x and a point in ray space x;however, it will be clear from the context which one is meant. Furthermore, to simplify the notation, we will use any of the synonyms x, ðx; x 2ÞT , or ðx0; x 1; x 2ÞT to denote a point in ray space. The volume rendering equation describes the light intensity I ðxÞ at wavelength  that reaches the center of projection along the ray x with length L:

I ðxÞ ¼ 

Z L

> 0

cðx;  Þf0

> c

ðx;  Þeˇ

R     

> 0f0
> cðx; Þd

d; ð7Þ

where f0

> c

ðxÞ is the extinction function that defines the rate of light occlusion and cðxÞ is an emission coefficient. The exponential term can be interpreted as an attenuation factor .Finally, the product cðxÞf0

> c

ðxÞ is also called the source term 

[28], describing the light intensity scattered in the direction of the ray x at the point x2. In the following equations, we will omit the parameter , implying that (7) has to be evaluated separately for different wavelengths. Now, we assume that the extinction function in object space (i.e., source space) fcðuÞ is given in the form of (1) as a weighted sum of coefficients wk and reconstruction kernels 

rkðuÞ. This corresponds to a physical model where the volume consists of individual particles that absorb and emit light. The reconstruction kernels r k reflect the position and shape of individual particles. The particles can be irregu-larly spaced and may differ in shape; hence, the model is not restricted to regular data sets. Note that the extinction function in ray space f0

> c

ðxÞ is computed by concatenating a mapping ’ from object space to camera space and amapping 
 from camera space to ray space (see Fig. 4), yielding: 

f0

> c

ðxÞ ¼ f cð’ˇ1ð
ˇ1ðxÞÞÞ ¼ X

> k

wk r0

> k

ðxÞ; ð8Þ

where r0

> k

ðxÞ ¼ r kð’ˇ1ð
ˇ1ðxÞÞÞ is a reconstruction kernel in ray space. The mappings 
 and ’ will be discussed in detail in Section 6.2. Because of the linearity of integration, substituting (8) into (7) yields 

IðxÞ ¼ X

> k

w k

 Z L

> 0

cðx;  Þr0

> k

ðx;  Þ

Y

> j

eˇwj

R    

> 0r0
> jðx; Þd

d 



;

ð9Þ

which can be interpreted as a weighted sum of projected reconstruction kernels. So, in terms of (3), we have the correspondence I ¼ P 

> k

w k pk ¼ gc and, for consistency with Section 3, we will use gc from now on. To compute gc numerically, splatting algorithms make several simplifying assumptions, illustrated in the right part of Fig. 5. Usually, the reconstruction kernels r0

> k

ðxÞ have local support. The splatting approach assumes that these local  

> ZWICKER ET AL.: EWA SPLATTING 227
> Fig. 5. Volume rendering. Left: Illustrating the volume rendering equation in 2D. Right: Approximation in typical splatting algorithms

support areas do not overlap along a ray x and the reconstruction kernels are ordered front to back. We also assume that the emission coefficient is constant in the support of each reconstruction kernel along a ray; hence, we use the notation ckðx0; x 1Þ ¼ cðx0; x 1; x 2Þ, where ðx0; x 1; x 2Þ is in the support of r0

> k

. Moreover, we approximate the exponential function with the first two terms of its Taylor expansion, thus eˇx  1 ˇ x. Finally, we ignore self-occlu-sion. Exploiting these assumptions, we rewrite (9), yielding: 

gcðxÞ ¼ X

> k

wk ckðxÞq kðxÞ Ykˇ1

> j¼0

1 ˇ wj q jðxÞ

ˇ ; ð10 Þ

where q kðxÞ denotes an integrated reconstruction kernel, hence: 

qkðxÞ ¼ 

Z

IR r0

> k

ðx; x 2Þ dx 2: ð11 Þ

Equation (10) is the basis for all splatting algorithms. Westover [2] introduced the term footprint function for the integrated reconstruction kernels q k. The footprint function is a 2D function that specifies the contribution of a 3D kernel to each point on the image plane. Since integrating avolume along a viewing ray is analogous to projecting a point on a surface onto the image plane, the coordinates 

x ¼ ð x0; x 1ÞT are also called screen coordinates and we say that g cðxÞ and q kðxÞ are defined in screen space .Splatting is attractive because of its efficiency, which it derives from the use of preintegrated reconstruction kernels. Therefore, during volume integration, each sample point along a viewing ray is computed using a2D convolution. In contrast, ray-casting methods require a 3D convolution for each sample point. This provides splatting algorithms with an inherent advantage in render-ing efficiency. Moreover, splatting facilitates the use of higher quality kernels with a larger extent than the trilinear kernels typically employed by ray-casting. On the other hand, basic splatting methods are plagued by artifacts because of incorrect visibility determination. This problem is unavoidably introduced by the assumption that the reconstruction kernels do not overlap and are ordered back to front. It has been successfully addressed by several authors, as mentioned in Section 2. In contrast, our main contribution is a novel splat primitive that provides high quality antialiasing and efficiently supports elliptical kernels. We believe that our novel primitive is compatible with all state-of-the-art splatting algorithms. 

4.2 The Volume Resampling Filter 

The splatting equation (10) represents the output image as a 

continuous screen space signal gcðxÞ. In order to properly sample this function to a discrete output image without aliasing artifacts, it has to be band limited to match the Nyquist frequency of the discrete image. According to (4), we achieve this band limitation by convolving gcðxÞ with an appropriate low-pass filter hðxÞ, yielding the antialiased 

splatting equation 

g0

> c

ðxÞ ¼ ð g c hÞð xÞ ¼ X

> k

wk

Z

IR 2 ckðÞq kðÞ

Ykˇ1

> j¼0

1 ˇ wj q jðÞ

ˇ hðx ˇ Þ d: 

ð12 Þ

Unfortunately, the convolution integral in (12) cannot be computed explicitly because of the emission and attenua-tion terms. Hence, we make two simplifying assumptions to rearrange it, leading to an approximation that can be evaluated efficiently. First, we assume that the emission coefficient is approximately constant in the support of each footprint function q k, hence ckðxÞ  ck for all x in the support area. Together with the assumption that the emission coefficient is constant in the support of each reconstruction kernel along a viewing ray , this means that the emission coefficient is constant in the complete 3D support of each reconstruction kernel. In other words, this corresponds to per-voxel evaluation of the shading model or preshading [25], ignoring the effect of shading for antialiasing. Note that prefiltering methods for surface textures usually ignore aliasing due to shading, too. Additionally, we assume that the attenuation factor has an approximately constant value ok in the support of each footprint function. Hence: 

Ykˇ1

> j¼0

1 ˇ wj q jðxÞ

ˇ   o k ð13 Þ

for all x in the support area. A variation of the attenuation factor indicates that the footprint function is partially covered by a more opaque region in the volume data. Therefore, this variation can be interpreted as a “soft” edge. Ignoring such situations means that we cannot prevent edge aliasing. Again, this is similar to rendering surfaces, where edge and texture aliasing are handled by different algo-rithms as well. Exploiting these simplifications, we can rewrite (12) to: 

ðgc hÞð xÞ  X

> k

w k ck o k

Z

IR 2 q kðÞhðx ˇ Þ d 

¼ X

> k

w k ck o kðq k hÞð xÞ:

Following the terminology of Section 3.3 (see (6)), we call 

kðxÞ ¼ ck o kðq k hÞð xÞ ¼ ð pk hÞð xÞ ð14 Þ

an ideal volume resampling filter , combining a projected reconstruction kernel pk ¼ ck o k q k and a low-pass kernel h.Hence, we can approximate the antialiased splatting equation (12) by replacing the footprint function qk in the original splatting equation (10) with the resampling filter k.This means that, instead of band limiting the output function g cðxÞ directly, we band limit each footprint function separately. Under the assumptions described above, we get a splatting algorithm that produces a band limited output function respecting the Nyquist frequency of the raster image, therefore avoiding aliasing artifacts. Remember that the reconstruction kernels are integrated in ray space, resulting in footprint functions that vary     

> 228 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002

significantly in size and shape across the volume. Hence, the resampling filter in (14) is strongly space variant .Swan et al. presented an antialiasing technique for splatting [18] that is based on a uniform scaling of the reconstruction kernels to band limit the extinction function. Their technique produces similar results as our method for radially symmetric kernels. However, for more general kernels, e.g., elliptical kernels, uniform scaling is a poor approximation of ideal low-pass filtering. Aliasing artifacts cannot be avoided without introducing additional blurri-ness. On the other hand, our method provides nonuniform scaling in these cases, leading to superior image quality, as illustrated in Section 8. Moreover, our analysis above shows that band limiting the extinction function does not guarantee alias free images. Because of shading and edges, frequencies above the Nyquist limit persist. However, these effects are not discussed in [18]. 

# 5 SURFACE RESAMPLING 

When rendering point-sampled surfaces, the data flows through a similar pipeline as in forward mapping volume rendering (Fig. 4). In Section 5.1, we first explain how continuous attribute functions are conceptually defined on point-sampled surfaces. Then we introduce an expression similar to (7) for the continuous output function (i.e., the rendered image) in Section 5.2. 

5.1 Attribute Functions on Point-Sampled Surfaces 

We represent point-sampled surfaces as a set of irregularly spaced points fPkg in three-dimensional object space without connectivity. A point Pk has a position and a normal. It is associated with a reconstruction kernel r k and samples of the attribute functions, e.g., wrk ; w gk ; w bk that represent continuous functions for red, green, and blue color components. Without loss of generality, we perform all further calculations with scalar coefficients wk. Note that the basis functions r k and coefficients wk can be determined in a preprocessing step as described in [23]. We define a continuous function on the surface represented by the set of points, as illustrated in Fig. 6. Given a point Q anywhere on the surface in object space, shown left, we construct a local parameterization of the surface in a small neighborhood of Q, illustrated on the right. The points Q and Pk have local source space coordinates 

u and uk, respectively. Using the parameterization, we can define the continuous attribute function fcðuÞ on the surface as in (1): 

f cðuÞ ¼ X

> k2

IN 

wk r kðuÞ: ð15 Þ

We will choose basis functions r k that have local support or that are appropriately truncated. Then, u lies in the support of a small number of basis functions. Note that, in order to evaluate (15), the local parameterization has to be estab-lished in the union of these support areas only, which is very small. Furthermore, we will compute these local parameterizations on the fly during rendering, as described in Section 7.2. 

5.2 The Surface Resampling Filter 

Rendering a parameterized surface involves mapping the attribute function fcðuÞ from parameter, i.e., source space, to screen space. As illustrated in Fig. 7, we denote this 2D to 2D mapping by x ¼ mðuÞ. It is composed of a 2D to 3D parameterization from source to object space and a 3D to 2D projection from object to screen space, which are described in more detail in Section 6.3. Using m, we can write the continuous output function as 

gcðxÞ ¼ X

> k

wk cðxÞr0

> k

ðxÞ; ð16 Þ

where r0

> k

ðxÞ ¼ r kðmˇ1ðxÞÞ is a reconstruction kernel mapped to screen space. As in Section 4, c is the emission term arising from shading the surface. Again we assume that emission is constant in the support of each r0 

> k

in screen space, which is equivalent to per-point shading, therefore ignoring aliasing due to shading. So, the band limited output function according to (4) is 

ðgc hÞð xÞ ¼ X

> k

w k ckðr0 

> k

hÞxÞ: ð17 Þ

Similarly as in Section 4.2, we call 

kðxÞ ¼ ckðr0 

> k

hÞð xÞ ¼ ð p k hÞð xÞ ð18 Þ 

> ZWICKER ET AL.: EWA SPLATTING 229
> Fig. 6. Defining a texture function on the surface of a point-based object.
> Fig. 7. Mapping a surface function from parameter space to screen space.

an ideal surface resampling filter , combining a projected surface reconstruction kernel pkðxÞ ¼ ck r kðmˇ1ðxÞÞ and a low-pass kernel hðxÞ.

# 6 EWA R ESAMPLING F ILTERS 

For both volume and surface rendering, we choose elliptical Gaussians as reconstruction kernels and low-pass filters since they provide certain features that are crucial for our technique: Gaussians are closed under affine mappings and convolution and integrating a 3D Gaussian along one coordinate axis results in a 2D Gaussian. These properties enable us to analytically compute the volume and surface resampling filters ((14) and (18), respectively) as a single 2D Gaussian, as will be shown in Sections 6.2 and 6.3. In Section 6.1, we summarize the mathematical features of the Gaussians that are exploited in our derivation in the following sections. More details on Gaussians can be found in Heckbert’s master’s thesis [9]. 

6.1 Elliptical Gaussian Filters 

We define a 3D elliptical Gaussian G3

> V

ðx ˇ pÞ centered at a point p with a variance matrix V as: 

G3

> V

ðx ˇ pÞ ¼ 1

ð2Þ3=2jVj12

eˇ12ðxˇpÞT Vˇ1ðxˇpÞ; ð19 Þ

where jVj is the determinant of V. In this form, the Gaussian is normalized to a unit integral. In the case of a 3D Gaussian, V is a symmetric 3  3 matrix and x and p are column vectors ðx0; x 1; x 2ÞT and ðp0; p 1; p 2ÞT , respectively. Similarly to (19), an elliptical 2D Gaussian G2

> V

ðx ˇ pÞ is defined as: 

G2

> V

ðx ˇ pÞ ¼ 12jVj12

eˇ12ðxˇpÞT Vˇ1 ðxˇpÞ; ð20 Þ

where V is a 2  2 variance matrix and x and p are 2D vectors. Note that the normalization factor is different for 2D and 3D Gaussians. We can easily apply an arbitrary affine mapping u ¼

ðxÞ to a Gaussian of any dimension n, denoted by Gn

> V

. Let us define the affine mapping as ðxÞ ¼ Mx þ c, where M is an n  n matrix and c is a vector ðc1; . . . ; c nÞT . We substitute 

x ¼ ˇ1ðuÞ, yielding: 

Gn

> V

ðˇ1ðuÞ ˇ pÞ ¼ 1

jMˇ1j Gn 

> MVM T

ðu ˇ ðpÞÞ : ð21 Þ

Moreover, convolving two Gaussians with variance ma-trices V and Y results in another Gaussian with variance matrix V þ Y:

ðG n 

> V

Gn

> Y

Þð x ˇ pÞ ¼ G n

> VþY

ðx ˇ pÞ: ð22 Þ

Finally, integrating a normalized 3D Gaussian G3 

> V

along one coordinate axis yields a normalized 2D Gaussian G2

> ^VV

, hence: 

Z

IR G3

> V

ðx ˇ pÞ dx 2 ¼ G 2

> ^VV

ð^xx ˇ ^ppÞ; ð23 Þ

where ^xx ¼ ð x0; x 1ÞT and ^pp ¼ ð p0; p 1ÞT . The 2  2 variance matrix ^VV is easily obtained from the 3  3 matrix V by skipping the third row and column: 

V ¼

a b cb d ec e f

0@1A , a bb d

 

¼ ^VV: ð24 Þ

In the following, we will use GV to denote both 2D and 3D Gaussians, with the context clarifying which one is meant. 

6.2 The EWA Volume Resampling Filter 

In this section, we first describe how to map arbitrary elliptical Gaussian volume reconstruction kernels from object to ray space. Our derivation results in an analytic expression for the kernels in ray space r0

> k

ðxÞ as in (8). We will then be able to analytically integrate the kernels according to (11) and to convolve the footprint function qk

with a Gaussian low-pass filter h as in (22), yielding an elliptical Gaussian resampling filter k.

6.2.1 The Viewing Transformation 

The reconstruction kernels are initially given in source space, or object space , which has coordinates 

u ¼ ð u0; u 1; u 2ÞT . As in Section 4.1, we denote the Gaussian reconstruction kernels in object space by: 

rkðuÞ ¼ G Vk ðu ˇ ukÞ; ð25 Þ

where uk are the voxel positions in object space. For regular volume datasets, the variance matrices Vk are usually identity matrices. For rectilinear datasets, they are diagonal matrices, where the matrix elements contain the squared distances between voxels along each coordinate axis. Curvilinear and irregular grids have to be resampled to a more regular structure in general. For example, Mao et al. [31] describe a stochastic sampling approach with a method to compute the variance matrices for curvilinear volumes. We denote camera coordinates by a vector t ¼ ð t0; t 1; t 2ÞT .Object coordinates are transformed to camera coordinates using a mapping t ¼ ’ðuÞ, called viewing transformation . The viewing transformation is usually an affine mapping defined by a matrix W and a translation vector d as 

’ðuÞ ¼ Wu þ d.

6.2.2 The Projective Transformation 

We will concatenate the viewing transformation with a projective transformation that converts camera coordinates to ray coordinates, as illustrated in Fig. 8. Camera space is defined such that the origin of the camera coordinate system is at the center of projection and the projection plane is the plane t2 ¼ 1. Camera space and ray space are related by the mapping x ¼ 
ðtÞ. Using the definition of ray space from Section 4.1, 
ðtÞ and its inverse 
ˇ1ðtÞ are therefore given by: 

x0

x1

x2

0@1A ¼ 
ðtÞ ¼ 

t0=t 2

t1=t 2

kð t0; t 1; t 2ÞT k

0@1A ð26 Þ

t0

t1

t2

0@1A ¼ 
ˇ1ðxÞ ¼ 

x0=l  x2

x1=l  x21=l  x2

0@1A; ð27 Þ

where l ¼ kð x0; x 1; 1ÞT k.    

> 230 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002

Unfortunately, these mappings are not affine, so we cannot apply (21) directly to transform the reconstruction kernels from camera to ray space. To solve this problem, we introduce the local affine approximation 
k of the projective transformation. It is defined by the first two terms of the Taylor expansion of 
 at the point tk:


 kðtÞ ¼ xk þ Jk  ð t ˇ tkÞ; ð28 Þ

where tk is the center of a Gaussian in camera space and 

xk ¼ 
ðtkÞ is the corresponding position in ray space. The Jacobian Jk is given by the partial derivatives of 
 at the point tk:

Jk ¼ @
 @t ðtkÞ ¼ 

1=t k; 2 0 ˇtk; 0=t 2

> k; 2

0 1=t k; 2 ˇtk; 1=t 2

> k; 2

tk; 0=l 0 tk; 1=l 0 tk; 2=l 0

0@1A; ð29 Þ

where l0 ¼ kð t k; 0; t k; 1; t k; 2ÞT k.The local affine approximation of the compound map-ping from source to ray space x ¼ mkðuÞ is given by the concatenation of t ¼ ’ðuÞ and x ¼ 
 kðtÞ:

x ¼ mkðuÞ ¼ 
kð’ðuÞÞ ¼ JkWu þ xk þ Jkðd ˇ tkÞ:

We substitute u ¼ mˇ1 

> k

ðxÞ in (25) and apply (21) to map the reconstruction kernels to ray space, yielding the desired expression for r0

> k

ðxÞ:

r0

> k

ðxÞ ¼ G Vk ðmˇ1ðxÞ ˇ ukÞ¼ 1

jWˇ1Jˇ1 

> k

j GV0 

> k

ðx ˇ mðukÞÞ ; ð30 Þ

where V0 

> k

is the variance matrix in ray coordinates. According to (21), V0 

> k

is given by: 

V0 

> k

¼ JkWV kWT JTk : ð31 Þ

Note that, for uniform or rectilinear datasets, the product WV kWT has to be computed only once per frame since Vk is the same for all voxels and W only changes from frame to frame. Since the Jacobian is different for each voxel position, V0 

> k

has to be recalcu-lated for each voxel, requiring two 3  3 matrix multi-plications V0 

> k

¼ JkðWV kWT ÞJTk . In the case of curvilinear or irregular volumes, each reconstruction kernel has an individual variance matrix Vk. Our method efficiently handles this situation, requiring only one additional 3  3

matrix multiplication, i.e., V0 

> k

¼ ð JkWÞVkðJkWÞT . In con-trast, previous techniques [2], [31] cope with elliptical kernels by computing their projected extents in screen space and then establishing a mapping to a circular footprint table. However, this procedure is computationally expen-sive. It leads to a bad approximation of the integral of the reconstruction kernel, as pointed out in [14], [18]. As illustrated in Fig. 9, the local affine mapping is exact only for the ray passing through tk or xk, respectively. The figure is exaggerated to show the nonlinear effects in the exact mapping. The affine mapping essentially approxi-mates the perspective projection with an oblique ortho-graphic projection. Therefore, parallel lines are preserved and approximation errors grow with increasing ray diver-gence. However, the errors do not lead to visual artifacts in general [14] since the fan of rays intersecting a reconstruc-tion kernel has a small opening angle due to the local support of the reconstruction kernels. A common approach of performing splatting with perspective projection is to map the footprint function onto a footprint polygon in camera space in a first step. In the next step, the footprint polygon is projected to screen space and rasterized, resulting in the so-called footprint image . As mentioned in [14], however, this requires significant computational effort. In contrast, our framework efficiently performs perspective projection by mapping the volume to ray space, which requires only the computation of the Jacobian and two 3  3 matrix multiplications. For spherical reconstruction kernels, these matrix operations can be further optimized, as shown in Section 7.1.   

> ZWICKER ET AL.: EWA SPLATTING 231
> Fig. 8. Transforming the volume from camera to ray space. Top: camera space. Bottom: ray space. Fig. 9. Mapping a reconstruction kernel from camera to ray space. Top: camera space. Bottom: ray space. Left: local affine mapping. Right: exact mapping.

6.2.3 Integration and Band Limiting 

We integrate the Gaussian reconstruction kernel of (30) according to (11), resulting in a Gaussian footprint function q k:

q kðxÞ ¼ 

Z

IR 1

jWˇ1Jˇ1 

> k

j GV0 

> k

ðx ˇ xk ; x 2 ˇ x k2Þ dx 2

¼ 1

jWˇ1Jˇ1 

> k

j G^VV0

> k

ðx ˇ xkÞ;

ð32 Þ

where the 2  2 variance matrix ^VV0 

> k

of the footprint function is obtained from V0 

> k

by skipping the last row and column, as shown in (24). Finally, we choose a Gaussian low-pass filter 

hðxÞ ¼ G Vh ðxÞ, where the variance matrix Vh 2 IR 22 is typically the identity matrix. With (22), we compute the convolution in (14), yielding the EWA volume resampling filter , or EWA volume splat :

 kðxÞ ¼ ð p k hÞð xÞ¼ ck o k

1

jWˇ1Jˇ1 

> k

j ðG ^VV0

> k

GVh Þð x ˇ xkÞ¼ ck o k

1

jWˇ1Jˇ1 

> k

j G^VV0  

> kþVh

ðx ˇ xkÞ:

ð33 Þ

6.3 The EWA Surface Resampling Filter 

In this section, we first describe how to construct the local parameterizations that are needed to define surface attribute functions fcðuÞ (Section 5.1). Then, we derive a mapping x ¼ mðuÞ involving parameterization, viewing transformation, and perspective projection that transforms the attribute function from source to screen space, similarly to Section 6.2. 

6.3.1 Local Surface Parameterizations 

At each point Pk, a local surface parameterization k is defined by two orthogonal unit vectors e0 

> k

and e1 

> k

in the tangent plane of the surface. The tangent plane is given by the surface normal nk stored with each point Pk. Hence, each point u ¼ ð u0; u 1ÞT in the parameter domain corre-sponds to a point ^uu ¼ ð ^uu0; ^uu1; ^uu2ÞT on the surface in object space: 

^uu ¼ kðuÞ ¼ Pk þ Sku;

where Sk is a 3  2 matrix consisting of the column vectors 

e0 

> k

and e1

> k

.We denote the Gaussian surface reconstruction kernels in the parameter domain by r kðuÞ ¼ G Vk ðuÞ. The variance matrix Vk has to be chosen appropriately to match the local density of points around Pk. Restricting ourselves to radially symmetric kernels, Vk is a 2  2 identity matrix I

scaled by a factor 2, i.e., Vk ¼ 2I. The scaling  depends on the distance between Pk and its nearest neighbors, e.g., we choose  as the average distance to the six nearest neighbors. A more sophisticated analysis of the point distribution around Pk could be used to find suitable variance matrices of general elliptical kernels. 

6.3.2 The Viewing Transformation 

The viewing transformation that maps object coordinates ^uu

to camera coordinates t is defined as in Section 6.2, i.e., 

t ¼ ’ð^uuÞ ¼ W^ uu þ d.

6.3.3 Perspective Projection 

Surface points t in 3D camera space are projected to 2D screen space x by dividing by the depth coordinate t2. Hence, we use the same mapping 
 (see (26)) as for volumes, except that we do not need the third coordinate x2:

x0

x1

 

¼ 
ðtÞ ¼ t0=t 2

t1=t 2

 

:

We use the same local affine approximation 
k as in (28). Note that here the Jacobian Jk is a 2  3 matrix: 

Jk ¼ @
 @t ðtkÞ ¼ 1=t k; 2 0 ˇtk; 0=t 2

> k; 2

0 1=t k; 2 ˇtk; 1=t 2

> k; 2

 

: ð34 Þ

Concatenating k, ’, and 
k, we get the local affine approximation mk of the mapping from source space to screen space: 

x ¼ mkðuÞ ¼ 
kð’ð kðuÞÞÞ ¼ JkWS ku þ xk :

Substituting u ¼ mˇ1 

> k

ðxÞ and applying (21) we get the Gaussian surface reconstruction kernel in screen space: 

r0

> k

ðxÞ ¼ G Vk ðmˇ1 

> k

ðxÞ ˇ ukÞ¼ 1

jMˇ1 

> k

j GV0 

> k

ðx ˇ mkðukÞÞ ;

with the variance matri x V0 

> k

¼ MkVkMTk and 

Mk ¼ JkWS k 2 IR 2.

6.3.4 Band Limiting 

With a Gaussian low-pass filter h ¼ G Vh and using (18), the 

EWA surface resampling filter , or EWA surface splat , is: 

kðxÞ ¼ ckðr0 

> k

hÞð xÞ¼ ck

1

jMˇ1 

> k

j GV0  

> kþVh

ðx ˇ mkðukÞÞ : ð35 Þ

In (35), the resampling filter is a function in screen space. Since the mapping mk is affine and invertible, we can alternatively express it as a function in source space, too. We use 

x ˇ mkðukÞ ¼ JkJˇ1 

> k

ðx ˇ mkðukÞÞ ¼ Jkðmˇ1 

> k

ðxÞ ˇ ukÞ;

and substitute this into (25), yielding: 

 kðxÞ ¼ ckGVk þMˇ1  

> kVhMˇ1Tk

ðu ˇ ukÞ: ð36 Þ

This is the well-known source space EWA method [9] extended for irregular sample positions, which is mathematically equivalent to our screen space formulation. However, (36) involves backward mapping a point x from screen to the object surface, which is impractical for interactive rendering. It amounts to ray tracing the point cloud to find surface intersections. Additionally, the locations uk are irregularly positioned such that the evaluation of the resampling kernel     

> 232 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002

in object space is laborious. On the other hand, (35) can be implemented efficiently for point-based objects, as described in Section 7.2. 

6.4 Reduction from Volume to Surface Reconstruction Kernels 

Since our EWA volume resampling filter can handle arbitrary Gaussian reconstruction kernels, we can represent the structure of a volume data set more accurately by choosing the shape of the reconstruction kernels appro-priately. For example, we can improve the precision of isosurface rendering by flattening the reconstruction ker-nels in the direction of the surface normal. We will show below that an infinitesimally flat Gaussian volume kernel is equivalent to a Gaussian surface texture reconstruction kernel. In other words, we can extract and render a surface representation from a volume data set directly by flattening volume reconstruction kernels into surface reconstruction kernels. Our derivation is illustrated in Fig. 10. We construct a flattened Gaussian reconstruction kernel in object space by scaling an arbitrary Gaussian with variance matrix V along the third coordinate axis, i.e., using a scaling matrix diag ð1; 1; 1=s Þ. Applying (21), we find that the variance matrix Vs of the scaled Gaussian is: 

Vs ¼

v0;0 v0;1 v0;2=s 2

v1;0 v1;1 v1;2=s 2

v2;0=s 2 v2;1=s 2 v2;2=s 2

0@1A:

In the limit, if s ¼ 1 , Vs is equivalent to a 2D Gaussian with variance matrix ^VV that is parameterized onto the plane perpendicular to the third coordinate axis, where 

^VV ¼ v0;0 v0;1

v1;0 v1;1

 

is the upper left 2  2 matrix in V. Since the plane is defined by basis vectors ð1; 0; 0ÞT and ð0; 1; 0ÞT , parameterization yields: 

1 00 10 0

0@1A ^VV 1 0 00 1 0

 

¼ Vs for s ! 1 : ð37 Þ

In the limit, the third row and column of Vs contain only zeros. Therefore, projecting a Gaussian GVs to screen space via mapping to ray space (30) and integration (32), or using perspective projection as in (35), results in the same 2D variance matrix of the reconstruction kernel in screen space. In other words, it is equivalent to rendering the flattened Gaussian as a volume or as a surface reconstruc-tion kernel. 

# 7 I MPLEMENTATION 7.1 EWA Volume Splatting 

We implemented a volume rendering algorithm based on the EWA splatting equation. Our implementation is embedded in the VTK (visualization toolkit) framework [32]. We did not optimize our code for rendering speed. We use a sheet buffer to first accumulate splats from planes in the volume that are most parallel to the projection plane [2]. In a second step, the final image is computed by compositing the sheets back to front. Shading is performed using the gradient estimation functionality provided by VTK and the Phong illumination model. 

7.1.1 Algorithm 

We summarize the main steps that are required to compute the EWA splat for each voxel in Fig. 11. First, we compute the camera coordinates tk of the current voxel k by applying the viewing transformation to the voxel center. Using tk, we then evaluate the Jacobian Jk

as given in (29). In line 4, we transform the Gaussian reconstruction kernel from object to ray space. This transformation is implemented by (31) and it results in the 3  3 variance matrix V0 

> k

of the Gaussian in ray space. Remember that W is the rotational part of the viewing transformation, hence it is typically orthonormal. Addition-ally, for spherical kernels, Vk is the identity matrix. In this case, evaluation of (31) can be simplified significantly. Next, we project the voxel center from camera space to the screen by performing a perspective division on tk. This yields the 2D screen coordinates xk. Now, we are ready to set up the resampling filter  k according to (33). Its variance matrix is derived from V0 

> k

by omitting the third row and column and adding a 2  2 identity matrix for the low-pass filter. We compute the determinants 1=jJˇ1 

> k

j and 1=jWˇ1j that are used as normalization factors and we evaluate the shading model yielding the emission coefficient ck.          

> ZWICKER ET AL.: EWA SPLATTING 233
> Fig. 10. Reducing avolume reconstruction kernel to asurface reconstruction kernel by flattening the kernel in one dimension. Top: rendering a volume kernel. Bottom: rendering a surface kernel.
> Fig. 11. The EWA volume splatting algorithm.

7.1.2 Rasterization 

Finally, we rasterize the resampling filter in line 7. As can be seen from the definition of the elliptical Gaussian (19), we also need the inverse of the variance matrix, which is called the conic matrix . Let us denote the 2  2 conic matrix of the resampling filter by Q. Furthermore, we define the radial index function 

rðxxÞ ¼ xxT Q xx where xx ¼ ð xx0; xx1ÞT ¼ x ˇ xk :

Note that the contours of the radial index, i.e., r ¼ const: are concentric ellipses. For circular kernels, r is the squared distance to the circle center. The exponential function in (19) can now be written as eˇ12r. We store this function in a 1D lookup table. To evaluate the radial index efficiently, we use finite differencing. Since r is biquadratic in xx, we need only two additions to update r for each pixel. We rasterize r in a rectangular, axis-aligned bounding box centered around xk,as illustrated in Fig. 12. Typically, we use a threshold c ¼ 4

and evaluate the Gaussian only if rðxxÞ < c . Heckbert provides pseudocode of the rasterization algorithm in [9]. 

7.2 EWA Surface Splatting 

We can perform EWA surface splatting in our volume renderer using flattened volume reconstruction kernels, as described in Section 6.4. We have also implemented adedicated surface splatting renderer [23]. The EWA surface splatting algorithm essentially proceeds as described in Section 7.1. However, the depth complexity of a scene is greater than one in general, but only those splats that belong to the visible surface must be accumulated in a pixel. Since back-to-front ordering of unstructured point clouds during rendering is prohibitive, an alternative mechanism is required that separates the contributions of different surfaces. We use a z-buffer approach, computing the z

value of the tangent plane at Pk at each pixel that is covered by the splat. This can be performed efficiently by forward differencing, similar to the visibility splatting approach of [8]. To determine whether a new contribution belongs to the same surface as is already stored in a pixel, the difference between the new z value and the z value stored in the frame buffer is compared to a threshold. If the difference is smaller than the threshold, the contribution is added to the pixel. Otherwise, given that it is closer to the eye-point, the data of the frame buffer is replaced by the new contribution. It is straightforward to extend this approach to a multilayered z-buffer [33] (similar to an A-buffer [34]) that allows the display of semitransparent surfaces and edge antialiasing [23]. 

# 8 RESULTS 

The EWA resampling filter has a number of useful proper-ties, as illustrated in Fig. 13. When the projection to screen space minifies the attribute function (i.e., the volume or point-sampled surface), size and shape of the resampling filter are dominated by the low-pass filter, as in the left column of Fig. 13. In the middle column, the attribute function is magnified and the resampling filter is domi-nated by the reconstruction kernel. Since the resampling filter unifies a reconstruction kernel and a low-pass filter, it provides a smooth transition between magnification and minification. Moreover, the reconstruction kernel is scaled anisotropically in situations where the volume is stretched in one direction and shrunken in the other, as shown in the right column. In the bottom row, we show the filter shapes resulting from uniformly scaling the reconstruction kernel to avoid aliasing, as proposed by Swan et al. [18]. Essentially, the reconstruction kernel is enlarged such that its minor radius is at least as long as the minor radius of the low-pass filter. For spherical reconstruction kernels, or circular footprint functions, this is basically equivalent to the EWA resampling filter. However, for elliptical footprint functions, uniform scaling leads to overly blurred images in the direction of the major axis of the ellipse. We compare our method to Swan’s method in Fig. 14. The images on the left were rendered with EWA volume     

> 234 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002
> Fig. 12. Rasterizing the resampling filter.
> Fig. 13. Properties of the EWA resampling filter.

splats, those on the right with Swan’s uniformly scaled kernels. We used rectangular zebra textures with x and 

y dimensions of 1; 024  512 (in the first row) and 1; 024 

256 (in the second row) and mapped the textures to a square. This leads to elliptical reconstruction kernels with a ratio between the length of the major and minor radii of 2 to 

1 and 4 to 1, respectively. Clearly, the EWA filter produces a crisper image and, at the same time, does not exhibit aliasing artifacts. As the ratio between the major and minor radii of the reconstruction kernels increases, the difference from Swan’s method becomes more pronounced. For strongly anisotropic kernels, Swan’s uniform scaling pro-duces excessively blurred images, as shown on the right in Fig. 14. Each frame took approximately 6 seconds to render on an 866 MHz PIII processor. In Fig. 15, we compare EWA splatting using volume kernels on the left to surface reconstruction kernels on the right. The texture size is 512  512 in the x and y direction. Typically, the perspective projection of a spherical kernel is almost a circle. Therefore, rendering with volume kernels does not exhibit anisotropic texture filtering and produces textures that are slightly too blurry, similar to isotropic texture filters such as trilinear mipmapping. On the other hand, splatting surface kernels is equivalent to EWA texture filtering. Circular surface kernels are mapped to ellipses, which results in high image quality because of anisotropic filtering. In Fig. 16, we show a series of volume renderings of the UNC CT scan of a human head ( 256  256  225 ), the UNC engine ( 256  256  110 ), and the foot of the visible woman data set ( 152  261  220 ). The texture in the last example is rendered using EWA surface splatting, too. The images illustrate that our algorithm correctly renders semitranspar-ent objects as well. The skull of the UNC head, the bone of the foot, and the iso-surface of the engine were rendered with flattened surface splats oriented perpendicular to the volume gradient. All other voxels were rendered with EWA volume splats. Each frame took approximately 11 seconds to render on an 866 MHz PIII processor. Fig. 17 shows results of EWA surface splatting which were rendered using a dedicated surface splatting renderer [23]. The face in Fig. 17a was acquired by a laser range scanner. Fig. 17b illustrates high quality texturing on terrain data and Fig. 17c shows semi-transparent surfaces on the complex model of a helicopter. Table 1 shows the performance of our unoptimized software implementation of EWA surface splatting. The frame rates were measured on a 1.1 GHz AMD Athlon system with 1.5 GByte memory. We rendered to a frame buffer with a resolution of 256 

256 and 512  512 pixels, respectively.                     

> ZWICKER ET AL.: EWA SPLATTING 235
> Fig. 14. Comparison between EWA volume splatting and Swan et al. Top two rows: 1;024 512 3volume texture. Bottom two rows: 1;024 
> 256 3volume texture.
> Fig. 15. EWA volume splatting versus EWA surface splatting; 512 512 3volume texture.

# 9 CONCLUSIONS 

We present a new splat primitive, called the EWA resampling filter. Using a general signal processing frame-work, we derive a formulation of the EWA resampling filter for both volume and surface splatting. Our primitive provides high quality antialiasing, combining an elliptical Gaussian reconstruction kernel with a Gaus-sian low-pass filter. We use a novel approach of computing the footprint function for volume rendering. Exploiting the mathematical features of 2D and 3D Gaussians, our framework efficiently handles arbitrary elliptical reconstruction kernels and perspective projec-tion. Therefore, our primitive is suitable to render regular, rectilinear, curvilinear, and irregular volume data sets. Our formulation of the EWA surface resampling filter is equivalent to Heckbert’s EWA texture filter. It provides high quality, anisotropic texture filtering for point-sampled surfaces. Hence, we call our primitive universal , facilitating the render-ing of surface and volume data. We have not yet investigated whether other kernels besides elliptical Gaussians may be used with this frame-work. In principle, a resampling filter could be derived from any function that allows the analytic evaluation of the operations described in Section 6.1 and that is a good approximation of an ideal low-pass filter. To achieve interactive frame rates, we are currently investigating the use of graphics hardware to rasterize EWA splats as texture mapped polygons. Programmable vertex shaders of modern GPUs (graphics processing units) provide all operations to compute EWA resampling filters completely in hardware. To render nonrectilinear data sets, we are investigating fast back-to-front sorting algorithms. Furthermore, we want to experiment with our splat primitive in a postshaded volume rendering pipeline. The derivative of the EWA resampling filter could be used as a band-limited gradient kernel, hence avoiding aliasing caused by shading for noisy volume data.     

> 236 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002
> Fig. 16. Semitransparent objects rendered using EWA volume splatting. The skull of the UNC head, the iso-surface of the engine, and the bone of the foot are rendered with flattened surface splats. (a) UNC head. (b) UNC engine. (c) Visible Woman foot.
> Fig. 17. EWA surface splatting of a scan of a human face, textured terrain, and a complex point-sampled object with semi-transparent surfaces. (a) Scanned head. (b) Textured Terrain Data. (c) Semi-transparent surfaces.

TABLE 1 Rendering Performance for Fame Buffer Resolutions 

256  256 and 512  512 A CKNOWLEDGMENTS 

The authors would like to thank Paul Heckbert for his encouragement and helpful comments and Ron Perry and Liu Ren for many stimulating discussions. Many thanks to Lisa Sobierajski Avila for her help with our implementation of EWA volume splatting in vtk. Thanks to Jennifer Roderick Pfister and Martin Roth for proofreading the paper. 

# R EFERENCES 

[1] L. Westover, “Interactive Volume Rendering,” Proc. Chapel Hill Workshop Volume Visualization, C. Upson, ed., pp. 9-16, May 1989. 

[2] L. Westover, “Footprint Evaluation for Volume Rendering,” 

Computer Graphics, Proc. SIGGRAPH ’90, pp. 367-376, Aug. 1990. 

[3] M. Levoy, K. Pulli, B. Curless, S. Rusinkiewicz, D. Koller, L. Pereira, M. Ginzton, S. Anderson, J. Davis, J. Ginsberg, J. Shade, and D. Fulk, “The Digital Michelangelo Project: 3D Scanning of Large Statues,” Computer Graphics, SIGGRAPH 2000 Proc., pp. 131-144, July 2000. 

[4] H. Hoppe, T. DeRose, T. Duchampt, J. McDonald, and W. Stuetzle, “Surface Reconstruction from Unorganized Points,” Computer Graphics, SIGGRAPH ’92 Proc., pp. 71-78, July 1992. 

[5] B. Curless and M. Levoy, “A Volumetric Method for Building Complex Models from Range Images,” Computer Graphics, SIGGRAPH ’96 Proc., pp. 303-312, Aug. 1996. 

[6] S. Rusinkiewicz and M. Levoy, “Qsplat: A Multiresolution Point Rendering System for Large Meshes,” Computer Graphics, SIG-GRAPH 2000 Proc., pp. 343-352, July 2000. 

[7] J.P. Grossman and W. Dally, “Point Sample Rendering,” Rendering Techniques ’98, pp. 181-192, July 1998. 

[8] H. Pfister, M. Zwicker, J. van Baar, and M. Gross, “Surfels: Surface Elements as Rendering Primitives,” Computer Graphics, SIG-GRAPH 2000 Proc., pp. 335-342, July 2000. 

[9] P. Heckbert, “Fundamentals of Texture Mapping and Image Warping,” MS thesis, Dept. of Electrical Eng. and Computer Science, Univ. of California at Berkeley, June 1989. 

[10] N. Greene and P. Heckbert, “Creating Raster Omnimax Images from Multiple Perspective views Using the Elliptical Weighted Average Filter,” IEEE Computer Graphics and Applications, vol. 6, no. 3, pp. 21-27, June 1986. 

[11] K. Mueller and R. Crawfis, “Eliminating Popping Artifacts in Sheet Buffer-Based Splatting,” Proc. IEEE Visualization ’98, pp. 239-246, Oct. 1998. 

[12] A. Van Gelder and K. Kim, “Direct Volume Rendering with Shading via Three-Dimensional Textures,” Proc. ACM/IEEE Symp. Volume Visualization, pp. 23-30, Oct. 1996. 

[13] B. Cabral, N. Cam, and J. Foran, “Accelerated Volume Rendering and Tomographic Reconstruction Using Texture Mapping Hard-ware,” Proc. 1994 Workshop Volume Visualization, pp. 91-98, Oct. 1994. 

[14] K. Mueller and R. Yagel, “Fast Perspective Volume Rendering with Splatting by Utilizing a Ray-Driven Approach,” Proc. IEEE Visualization ’96, pp. 65-72, Oct. 1996. 

[15] D. Laur and P. Hanrahan, “Hierarchical Splatting: A Progressive Refinement Algorithm for Volume Rendering,” Computer Graphics, SIGGRAPH ’91 Proc., pp. 285-288, July-Aug. 1991. 

[16] L. Lippert and M.H. Gross, “Fast Wavelet Based Volume Rendering by Accumulation of Transparent Texture Maps,” 

Computer Graphics Forum, vol. 14, no. 3, pp. 431-444. Aug. 1995. 

[17] X. Mao, “Splatting of Non Rectilinear Volumes through Stochastic Resampling,” IEEE Trans. Visualization and Computer Graphics, 

vol. 2, no. 2, pp. 156-170. June 1996. 

[18] J.E. Swan, K. Mueller, T. Mo ¨ller, N. Shareef, R. Crawfis, and R. Yagel, “An Anti-Aliasing Technique for Splatting,” Proc. 1997 IEEE Visualization Conf., pp. 197-204, Oct. 1997. 

[19] K. Mueller, T. Moeller, J.E. Swan, R. Crawfis, N. Shareef, and R. Yagel, “Splatting Errors and Antialiasing,” IEEE Trans. Visualiza-tion and Computer Graphics, vol. 4, no. 2, pp. 178-191, Apr.-June 1998. 

[20] M. Levoy and T. Whitted, “The Use of Points as Display Primitives,” Technical Report TR 85-022, Dept. of Computer Science, Univ. of North Carolina at Chapel Hill, 1985. 

[21] T.W. Mark, L. McMillan, and G. Bishop, “Post-Rendering 3D Warping,” Proc. 1997 Symp. Interactive 3D Graphics, pp. 7-16, Apr. 1997. 

[22] J. Shade, S.J. Gortler, L. He, and R. Szeliski, “Layered Depth Images,” Computer Graphics SIGGRAPH ’98 Proc., pp. 231-242, July 1998. 

[23] M. Zwicker, H. Pfister, J. Van Baar, and M. Gross, “Surface Splatting,” Computer Graphics, SIGGRAPH 2001 Proc., July 2001. 

[24] M. Zwicker, H. Pfister, J. Van Baar, and M. Gross, “Ewa Volume Splatting,” Proc. IEEE Visualization 2001, pp. 29-36, Oct. 2001. 

[25] K. Mueller, T. Moeller, and R. Crawfis, “Splatting without the Blur,” Proc. 1999 IEEE Visualization Conf., pp. 363-370, Oct. 1999. 

[26] C. Wittenbrink, T. Malzbender, and M. Goss, “Opacity-Weighted Color Interpolation for Volume Sampling,” Proc. IEEE Symp. Volume Visualization, pp. 431-444, Oct. 1998. 

[27] J.T. Kajiya and B.P. Von Herzen, “Ray Tracing Volume Densities,” 

Computer Graphics, Proc. SIGGRAPH ’84, vol. 18, no. 3, pp. 165-174. July 1984. 

[28] N. Max, “Optical Models for Direct Volume Rendering,” IEEE Trans. Visualization and Computer Graphics, vol. 1, no. 2, pp. 99-108, June 1995. 

[29] P. Lacroute and M. Levoy, “Fast Volume Rendering Using a Shear-Warp Factorization of the Viewing Transform,” Computer Graphics, Proc. SIGGRAPH ’94, pp. 451-457, July 1994. 

[30] M. Levoy, “Display of Surfaces from Volume Data,” IEEE Computer Graphics and Applications, vol. 8, no. 3, pp. 29-37, May 1988. 

[31] X. Mao, L. Hong, and A. Kaufman, “Splatting of Curvilinear Volumes,” IEEE Visualization ’95 Proc., pp. 61-68, Oct. 1995. 

[32] W. Schroeder, K. Martin, and B. Lorensen, The Visualization Toolkit, 

second ed. Prentice Hall, 1998. 

[33] N. Jouppi and C. Chang, “z3: An Economical Hardware Technique for High-Quality Antialiasing and Transparency,” 

Proc. Eurographics/SIGGRAPH Workshop Graphics Hardware 1999, 

pp. 85-93, Aug. 1999. 

[34] L. Carpenter, “The A-Buffer, an Antialiased Hidden Surface Method,” Computer Graphics, SIGGRAPH ’84 Proc., vol. 18, pp. 103-108, July 1984. 

Matthias Zwicker is in his last year of the PhD program at the Computer Graphics Lab at ETH Zu ¨ rich, Switzerland. He has developed rendering algorithms and data structures for point-based surface representations. He has also extended this work toward high quality volume rendering. Other research interests concern compression of point-based data structures, acquisition of real world objects, and texturing of point-sampled surfaces. 

Hanspeter Pfister received the PhD degree in computer science in 1996 from the State University of New York at Stony Brook. He received the MS degree in electrical engineering from the Swiss Federal Institute of Technology (ETH) Zurich, Switzerland, in 1991. He is associate director and a research scientist at MERL—Mitsubishi Electric Research Laborator-ies—in Cambridge, Massachusetts. He is the chief architect of VolumePro, Mitsubishi Elec-tric’s real-time volume rendering hardware for PCs. His research interests include computer graphics, scientific visualization, and computer architecture. His work spans a range of topics, including point-based rendering and modeling, 3D scanning and 3D photography, and computer graphics hardware. Dr. Pfister has taught courses at major graphics conferences, including SIGGRAPH, IEEE Visualization, and Eurographics. He is an associate editor of the IEEE Transactions on Visualization and Computer Graphics (TVCG ), a member of the Executive Committee of the IEEE Technical Committee on Graphics and Visualization (TCVG), and has served as a member of international program committees of major graphics conferences. He is the general chair of the IEEE Visualization 2002 conference in Boston. He is a member of the ACM, ACM SIGGRAPH, IEEE, IEEE Computer Society, and Eurographics Association. ZWICKER ET AL.: EWA SPLATTING 237 Jeroen van Baar received the MS degree in computer science from Delft University of Technology, The Netherlands, in 1998. He is working at MERL—Mitsubishi Electric Re-search Labsoratories—in Cambridge, Massa-chusetts, as a member of the technical staff. His areas of interest include the broad fields of computer graphics, scientific visualization, and computer vision. 

Markus Gross received a degree in electrical and computer engineering and the PhD degree in computer graphics and image analysis, both from the University of Saarbru ¨cken, Germany. He is a professor of computer science and the director of the Computer Graphics Laboratory of the Swiss Federal Institute of Technology (ETH) in Zu ¨urich. From 1990 to 1994, Dr. Gross was with the Computer Graphics Center in Darm-stadt, where he established and directed the Visual Computing Group. His research interests include physics-based modeling, point-based methods, and multiresolution analysis. He has widely published and lectured on computer graphics and scientific visualization and he authored the book Visual Computing (Springer, 1994). Dr. Gross has taught courses at major graphics conferences including SIGGRAPH, IEEE Visualization, and Eurographics. He is an associate editor of IEEE Computer Graphics and Applications and has served as a member of international program committees of major graphics conferences. Dr. Gross was a papers cochair of the IEEE Visualization ’99 and Eurographics 2000 conferences. He is a member of the IEEE, ACM, and of the Eurographics Association. 

. For more information on this or any computing topic, please visit our Digital Library at http://computer.org/publications/dlib. 238 IEEE TRANSACTIONS ON VISUALIZATION AND COMPUTER GRAPHICS, VOL. 8, NO. 3, JULY-SEPTEMBER 2002