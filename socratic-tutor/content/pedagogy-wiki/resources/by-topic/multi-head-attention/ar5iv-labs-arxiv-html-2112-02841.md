# Source: https://ar5iv.labs.arxiv.org/html/2112.02841
# Author: Weixuan Sun et al.
# Title: GETAM: Gradient-Weighted Element-Wise Transformer Attention Map for Weakly Supervised Semantic segmentation
# Fetched via: trafilatura
# Date: 2026-04-07

GETAM: Gradient-Weighted Element-Wise Transformer Attention Map
for Weakly Supervised Semantic segmentation
GETAM: Gradient-weighted Element-wise Transformer Attention Map for Weakly-supervised Semantic Segmentation
Abstract
Weakly-supervised semantic segmentation (WSSS) is challenging, particularly when image-level labels are used to supervise pixel-level prediction. To bridge their gap, a Class Activation Map (CAM) is usually generated to provide pixel-level pseudo labels. CAMs in Convolutional Neural Networks suffer from partial activation i.e. only the discriminative regions are activated. Transformer networks, on the other hand, are highly effective at exploring global context, potentially alleviating the partial activation issue. In this paper, we introduce the Gradient-weighted Element-wise Transformer Attention Map (GETAM) and propose the first transformer-based WSSS approach. GETAM can show fine scale class-wise activation, revealing different parts of the object across transformer layers. Further, we propose an activation-aware label-completion module to generate high-quality pseudo labels. Finally, we incorporate the proposed methods into an end-to-end framework for WSSS using double-backward propagation. Extensive experiments on PASCAL VOC and COCO dataset demonstrate that our results outperform not only the state-of-the-art end-to-end approaches by a significant margin, but also most of the multi-stage methods.
1 Introduction
Recent work on 2D image semantic segmentation has achieved great progress via
deep fully convolutional neural networks (FCNs) [[43](#bib.bib43)].
The success of these models [[80](#bib.bib80), [13](#bib.bib13), [12](#bib.bib12), [14](#bib.bib14)] comes from large training datasets with pixel-wise labels, which are laborious and expensive to obtain.
To relieve the labeling burden, multiple types of weak labels have been explored, including image-level labels [[27](#bib.bib27), [2](#bib.bib2), [21](#bib.bib21)], points [[6](#bib.bib6)],
scribbles [[62](#bib.bib62), [40](#bib.bib40), [59](#bib.bib59)] and bounding boxes [[15](#bib.bib15), [47](#bib.bib47), [36](#bib.bib36), [46](#bib.bib46), [57](#bib.bib57)].
In this paper, we focus on weakly-supervised semantic segmentation (WSSS) with image-level labels.
To bridge the gap between pixel-level classification and image-level annotation, it is essential to localize object classes in the image from image-level labels.
Most WSSS methods rely on the Class Activation Map (CAM) [[81](#bib.bib81)] as initial seeds from the image-level label to learn pixel-level labeling.
Typical multi-stage image-level WSSS methods usually adopt progressive steps [[66](#bib.bib66), [8](#bib.bib8), [77](#bib.bib77), [74](#bib.bib74), [23](#bib.bib23), [72](#bib.bib72), [30](#bib.bib30)]:
1) training a CNN classifier
to obtain object activation maps [[81](#bib.bib81), [66](#bib.bib66), [8](#bib.bib8), [23](#bib.bib23), [30](#bib.bib30), [26](#bib.bib26)];
2) refining the maps with non-learning [[71](#bib.bib71)] or learning based methods [[2](#bib.bib2), [27](#bib.bib27)]
to obtain pseudo labels; and
3) using these pseudo labels for fully-supervised training of an off-the-shelf semantic segmentation network, such as Deeplab [[13](#bib.bib13)].
Alternatively, recently end-to-end WSSS methods have become more prevalent [[74](#bib.bib74), [3](#bib.bib3), [78](#bib.bib78)].
In both cases, the quality of the initial response map plays a key role in WSSS. However, it is recognized by many approaches [[66](#bib.bib66), [8](#bib.bib8), [77](#bib.bib77), [74](#bib.bib74), [23](#bib.bib23), [72](#bib.bib72), [30](#bib.bib30), [71](#bib.bib71), [58](#bib.bib58), [69](#bib.bib69)] that CAMs suffer from two issues: 1) CAMs tend to only activate the discriminative regions of objects; 2) the rough object activation of CAMs loses accurate object shapes.
The main causes of above issues are limited receptive fields and the progressively down-sampled CNN feature maps.
Transformers [[61](#bib.bib61)] have achieved great success in various computer vision tasks, but transformer-based WSSS is yet to be well studied.
We argue that transformers have several appealing mechanisms for WSSS.
First, transformers are highly effective at exploring global context with long-range dependency modelling. Hence, one would expect they could address issues regarding the limited visual field of CNNs.
Also, after computing the initial embedding, vision transformers have a constant global receptive field at every layer
with constant dimensionality,
which could retain more accurate structure information [[49](#bib.bib49), [45](#bib.bib45)]. Further, transformers use self-attention to spread activation across the entire feature map rather than just discriminative regions, leading to more uniform activation.
We show that these properties are beneficial for generating object activation maps, as well for other dense prediction tasks [[49](#bib.bib49), [42](#bib.bib42), [5](#bib.bib5), [63](#bib.bib63), [54](#bib.bib54)].
Unfortunately, we observe extensive noise if we simply transplant the conventional CAM [[81](#bib.bib81)] into vision transformers (Fig. [2](#S2.F2)). Such noise leads to poor performance and is
believed
to arise along with the global context of the transformer architecture [[79](#bib.bib79)].
To address this, we closely study activation and propagation of the feature maps through transformer layers. Particularly, we explore element-wise weighting to couple the attention map (i.e. ) with its squared gradient
to
place greater emphasis on the gradient.
Further, as attention is progressively propagated and refined through the transformer layers, it reveals different parts of the object.
We sum the attention maps through transformer layers, leading to more uniformly activated
object maps, as shown in Fig. [1](#S1.F1). We refer to this as the Gradient-weighted Element-wise Transformer Attention Map (GETAM).
After obtaining class-wise attention maps,
we propose activation aware label completion, combining the obtained object activation with off-the-shelf saliency maps to generate pseudo segmentation labels.
In this way, we refine foreground object masks and actively discover objects in the background, leading to high-quality pseudo labels.
Finally, we propose a double-backward propagation mechanism to implement our framework in an end-to-end manner. Most WSSS methods require multiple stages, involving multiple models with different pipelines and tweaks, making them hard to train and implement.
Although the existing end-to-end approaches
[[48](#bib.bib48), [47](#bib.bib47), [73](#bib.bib73), [74](#bib.bib74), [3](#bib.bib3), [78](#bib.bib78)]
are elegant, they
show substantially inferior performance to multi-stage methods.
Our method is easy to implement and extensive experiments on the PASCAL VOC [[18](#bib.bib18)]
and COCO [[41](#bib.bib41)] datasets verify its effectiveness.
Our contributions can be summarised as: 1) We introduce the first weakly-supervised semantic segmentation framework based on vision transformer networks. The key to its performance is the Gradient-weighted Element-wise Transformer Attention Map (GETAM), capturing better object shapes than traditional CAMs. 2) We present activation-aware label completion guided by saliency maps to generate high-quality pseudo labels. 3) We propose a double-backward propagation mechanism to integrate our method in an end-to-end manner. Despite its simplicity, our method greatly boosts the performance of single-stage WSSS, and it is the first one to be competitive with multi-stage methods.
2 Related Work
2.1 Weakly Supervised Semantic Segmentation
To save labeling cost,
various WSSS methods have been proposed,
including those using image-level labels [[2](#bib.bib2), [47](#bib.bib47), [66](#bib.bib66), [8](#bib.bib8), [74](#bib.bib74), [72](#bib.bib72), [37](#bib.bib37)], scribbles [[40](#bib.bib40)], points [[6](#bib.bib6)], and bounding boxes [[15](#bib.bib15), [57](#bib.bib57), [36](#bib.bib36), [46](#bib.bib46)].
We mainly focus on image-level models. They
can be grouped into two families: multi-step, and
one-step
methods.
2.1.1 Multi-step methods
[[66](#bib.bib66), [8](#bib.bib8), [77](#bib.bib77), [74](#bib.bib74), [23](#bib.bib23), [72](#bib.bib72), [30](#bib.bib30), [2](#bib.bib2), [7](#bib.bib7), [37](#bib.bib37)] refine one or multiple sub-modules within the multi-model framework.
Among them, [[2](#bib.bib2)] predicts semantic
affinity between a pair of adjacent image coordinates supervised by initial activation, the network is then used to guide a random walk to generate pseudo labels.
[[7](#bib.bib7), [23](#bib.bib23)] utilize Mixup data augmentation to calibrate uncertainty in prediction. They randomly mix an image pair
to force the model to pay attention to extra regions in the image.
[[37](#bib.bib37)] directly uses saliency maps to constrain object activation during classification training, so the CAMs can better follow object shapes.
2.1.2 One-step methods
[[47](#bib.bib47)] adopts an expectation-maximisation mechanism, where intermediate predictions are used as segmentation labels.
[[74](#bib.bib74)] presents an
end-to-end framework to train classification and segmentation simultaneously, and integrates a method to obtain reliable segmentation pseudo labels.
[[3](#bib.bib3)] introduces normalised Global Weighted Pooling (nGWP) to obtain better CAMs for segmentation, and adopts a Stochastic gate to encourage information sharing between deep features and shallow representations to deal with complex scenes.
With all above solutions, end-to-end WSSS is still far from being well-studied, and has clear performance gaps from multi-step methods.
2.2 Network Visualization
Various works have been proposed for network visualization and are leveraged for tasks like weak semantic segmentation and weak object localization.
CAM [[81](#bib.bib81)] replaces the first fully-connected layer in image classifiers with a global average pooling layer to calculate class activation map.
In Grad-CAM family methods [[53](#bib.bib53), [29](#bib.bib29), [9](#bib.bib9)], the class-specific gradients flow to each feature map and methods adopt different ways to obtain a weighted sum of feature maps for visualization.
For the vision transformer, [[22](#bib.bib22)] proposes to couple semantic-agnostic attention maps and semantic-aware maps for weakly supervised object localization.
[[11](#bib.bib11), [10](#bib.bib10)] employ LRP-based relevance [[4](#bib.bib4)] combined with gradients to explore the interpretability of transformer attention. However, none of above methods are specially designed for WSSS.
3 Revisiting CAM in ViT
In this section, we revisit conventional CAMs [[2](#bib.bib2)] used in most WSSS methods.
We present a pilot experiment to investigate different activation mechanisms in convolutional and transformer backbones, demonstrating that the conventional CAM [[81](#bib.bib81)] and Grad-CAM [[52](#bib.bib52)] methods used in existing WSSS methods cannot be trivially transplanted to transformer-based approaches.
To generate a CAM in a CNN network, [[81](#bib.bib81)] feeds
convolutional feature maps into global average pooling (GAP) followed by a fully-connected layer to produce a categorical output.
For an image , activation maps for category are defined as:
,
where is the classifier’s weight for class and is the extracted feature at location .
Then, we copy the same CAM structure to the transformer.
Given the extracted feature maps , we obtain , where is the input image patch size, and is the feature embedding dimension. The first row is the [class] token.
We explore two strategies to manipulate and generate a feature map .
First, we add to every location of , we denote this method as CAM(add) in Fig. [2](#S2.F2).
Second, we ignore , and simply feed into linear classifier, we denote this method as CAM(ignore) in Fig. [2](#S2.F2).
As shown in Fig. [2](#S2.F2), if we simply follow the conventional method, the transformer CAMs are flawed, i.e., the activation is not correctly located on targeted objects and cannot be used to generate pseudo segmentation labels.
Due to the self-attention mechanism, every feature map location encodes information from the entire image in a fully connected manner. However, classification loss is indifferent to extensive activation across objects, requiring only a sufficient pooled global average value.
So per-location features may not contribute to local classification predictions, and activation shows noise across the image, or can be completely wrong.
Reliable CAMs are crucial for WSSS, but CNN-based CAMs cannot be naively migrated into vision transformers, i.e. changing backbones of current WSSS methods to transformers is non-trivial.
4 Approach
We show the overview of our framework in Fig. [3](#S2.F3).
Firstly, we introduce GETAM (Gradient-weighted Element-wise Transformer Attention Map), which generates better class-wise attention maps with image-level labels.
Then, we introduce activation aware-label completion, which uses saliency information to produce high-quality pseudo segmentation labels from the activation maps.
Finally, we present our double-backward propagation approach to implement our method into a single-stage framework.
4.1 GETAM
As discussed in Sec. [3](#S3), conventional CAM generation methods used in CNN backbones fail to generate reliable CAMs in transformers.
Thus, inspired by Grad-CAM [[52](#bib.bib52)], we design a gradient-based method to obtain class-wise attention maps for vision transformers.
Note that our method is substantially different to Grad-CAM [[52](#bib.bib52)], albeit also based on gradients.
In Grad-CAM [[52](#bib.bib52)], classification predictions are back propagated to the output feature maps of the final convolutional
layer.
The obtained gradients are global average pooled, and
used to weigh neuron
importance of the feature maps.
However, transformer networks use different structures for predictions. A transformer network consists of several successive transformer blocks, each composed of multi-head self-attention modules and feed-forward connections. The self-attention module on one of the multiple heads in a transformer block is defined as:
| (1) |
where are query, key and value matrices , is number of patches () and is feature dimensions.
The [class] is an extra learnable token in the first row of these matrices [[17](#bib.bib17)].
As shown in Fig. [5](#S4.F5), is the attention matrix which encodes the attention coefficient between any two positions in input images, i.e., every image token has contextual information from all other tokens.
Consequently,
the [class] token attends to all token information across the image. However, it is not affected by itself as it does not represent an image location.
We define .
We can reshape back to the image shape , and obtain a class-agnostic attention map, where every position in the map denotes its contribution to classification.
In every transformer block with multiple self-attention heads, we define as the average across all heads for simplicity.
As empirically verified in [[22](#bib.bib22)],
aggregates attention from all heads to display the object extent that possibly contributes to classification predictions (see the leftmost column
of Fig [4](#S4.F4)).
As is class agnostic, we couple it with its gradients
to obtain the class-wise attention map.
We back-propagate the classification
score for each class .
The graph is differentiated using the chain rule through the transformer network.
In the block,
the gradient map is obtained with respect to the attention matrix .
Referring to Fig. [5](#S4.F5), we extract the corresponding gradient map
of with respect to class .
As discussed in [[52](#bib.bib52), [9](#bib.bib9), [29](#bib.bib29)], a positive gradient corresponding
to a location in the feature map indicates that it has a positive influence on
the prediction score of the target class.
We find that this assertion still holds in vision transformers.
Each position in indicates the contribution of this token to the classification output of class .
4.1.1 Attention Gradient Coupling
We observe that
shows class-agnostic areas with possibly targeted objects and relatively clean background.
Further, we find is noisy but retains more complete and clear object shapes in comparison (see rightmost column of Fig. [4](#S4.F4)).
Based on the above observations, we propose to combine the attention map and its gradient inside every transformer block to generate reliable class-wise attention as shown in Fig. [5](#S4.F5).
Formally, the class-wise attention map of block for class is defined as:
| (2) |
We first use an element-wise multiplication to couple the attention map with its gradient map . Then, we perform another element-wise multiplication with . Different from Grad_CAM which uses a Global Average Pool of the Gradients, our attention map is weighted element-wise by the square of the gradient, and negative responses of attention and gradients are eliminated by the ReLUs. Our Attention-Gradient coupling can better harvest spatial locations that have positive contributions to the targeted class, while suppressing noisy regions. Squaring places greater emphasis on the gradient as it shows more complete object shapes than the CAMS.
4.1.2 Successive Attention Aggregation
After obtaining the class-wise attention map in a single transformer block, here we present an analysis on how to aggregate class attention maps from cascaded transformer blocks.
As commonly recognized by existing WSSS methods [[58](#bib.bib58), [56](#bib.bib56), [56](#bib.bib56), [76](#bib.bib76), [66](#bib.bib66)], the attention maps should not respond too sparsely (i.e., only highlighting discriminative regions), nor be overly smoothed.
Based on the above requirements, we first visualize the class-wise attention maps from different transformer blocks in Fig. [6](#S4.F6).
Unlike CNNs where low-level features contain too much noise that buries useful information [[67](#bib.bib67), [29](#bib.bib29)], we observe that the cascaded maps in vision transformers tend to focus on discriminative regions. For instance, in Fig. [6](#S4.F6) (bottom), attention maps from different layers reveal different regions of the cat (e.g., cheek, nose, chin, body and hand).
Thus, it is crucial to choose an appropriate fusion method to combine different class-wise attentions maps.
In this view, we present a numerical analysis of different fusion approaches (Fig. [7](#S4.F7)).
On the PASCAL VOC [[18](#bib.bib18)] training set, we apply three commonly adopted operations (element-wise multiplication, summation and matrix multiplication) to fuse the successive maps, and then visualize the distributions of the fused results after normalization.
As illustrated in Fig. [7](#S4.F7), element-wise multiplication will concentrate the values and most areas are suppressed, since the activation is canceled if the value is low
in any level of the transformer. Contrarily, matrix multiplication (dot production) will smooth the attention, leading to additional noise in non-object regions.
Based on the above analysis, we propose summation aggregation across cascaded attention maps, which encourages the final class-wise attention maps to cover accurate object areas and does not over-smooth them.
Formally, the attention maps are added through layers of the vision transformer:
| (3) |
Fig. [6](#S4.F6) shows that GETAM from the cascaded blocks (Eq. [3](#S4.E3))
captures reliable object shapes and suppresses noise.
See supplementary material for
qualitative comparison.
4.2 Activation Aware Label Completion
GETAM generates reliable class-wise attention maps.
However, the activation maps require refinement, so they can be served as pseudo segmentation labels.
To achieve this,
we first adopt pixel adaptive mask refinement (PAMR) [[3](#bib.bib3)],
a parameter-free recurrent module that efficiently refines pixel labels using local information.
Then, we propose
saliency constrained object masking and high activation object mining to obtain high-quality pseudo
labels.
The two solutions work collaboratively to
support accurate segmentation of salient objects, but do not suppress non-salient objects.
4.2.1 Saliency Constrained Object Masking
We observe that due to the global context of self-attention, candidate regions that may contribute to classification
are activated, leading to high recall of our activation maps for targeted objects.
Saliency maps from off-the-shelf models can provide precise foreground object shapes and have been used as background cues to many WSSS approaches [[19](#bib.bib19), [28](#bib.bib28), [34](#bib.bib34), [55](#bib.bib55), [65](#bib.bib65), [37](#bib.bib37), [71](#bib.bib71)].
Using a novel approach, we leverage
the saliency mask to constrain activated object regions, which is particularly necessary in our case for GETAM to combat additional activation on object boundaries.
First, based on object activation maps which have foreground classes,
we calculate an arbitrary background channel in a similar way to [[2](#bib.bib2)]:
,
where is a parameter to adjust background labels and
is the pixel position.
Then we concatenate
onto to form activation maps ,
and use to find the per-pixel highest activation.
After that, we can locate all possible objects in both salient and non-salient regions with rough boundaries, as shown in Fig. [8](#S4.F8) (a).
Then we adopt saliency maps
to refine object boundaries of , where
the current temporary background (0) is set to unknown (255) and
all non-salient regions
are set to background (0).
This is based on the observation
that the saliency maps normally provide accurate object boundaries [[71](#bib.bib71), [37](#bib.bib37), [64](#bib.bib64)].
Formally, consider activation maps with saliency map , then pixel of our pseudo label is:
| (4) |
4.2.2 High Activation Object Mining
With saliency constrained object masking, we obtain , where the structure of the instances that are consistent with salient objects is refined.
However, recall that existing salient object detection models are trained with class-agnostic objects and center bias, and so
non-salient objects may masked as background.
As shown in Fig. [8](#S4.F8)(b), the TV monitor and potted plant are mislabeled as background.
We then propose a high activation object mining strategy to solve this issue.
GETAM can correctly locate all desired objects in both salient and non-salient regions as shown in Fig. [8](#S4.F8)(a).
For class ,
we find high confidence regions by searching for pixels with activation greater than a threshold in non-salient regions.
We treat these
as pseudo labels of class in the background (see Fig. [8](#S4.F8)(c)).
In addition, we maintain another high-confidence conflict mask to register conflict areas in non-salient regions. That is,
if a pixel is highly activated by more than one class in the background, we regard it as conflict and label it as unknown (255) to avoid introducing incorrect labels.
Formally, high activation object mining is defined:
| (5) |
where is the high confidence threshold, empirically set to 0.9, i.e., if the activation at a pixel of class is higher than of all activation of the same object class, we regard it as highly activated and label it as , otherwise as background (0). We ablate in detail in the supplementary material.
We give a quantitative comparison of our pseudo labels to other methods in Table [3](#S5.T3). Our high-quality pseudo labels can be directly used to supervise an off-the-shelf semantic segmentation model.
They can also supervise a segmentation branch of the same vision transformer backbone in an end-to-end manner (detailed below).
4.3 Single-stage Double-backward Propagation
Most current WSSS methods [[66](#bib.bib66), [8](#bib.bib8), [77](#bib.bib77), [74](#bib.bib74), [23](#bib.bib23), [72](#bib.bib72), [30](#bib.bib30)] require multiple steps, generally involving
training
multiple models with
different pipelines and tweaks.
Inter-dependencies between the steps can easily influence final performance.
However,
the vision transformer shows properties that are especially advantageous for dense prediction tasks like semantic segmentation [[49](#bib.bib49), [42](#bib.bib42), [5](#bib.bib5), [63](#bib.bib63)].
Hence,
we propose an unified framework to train our WSSS method in an end-to-end manner.
As shown in Fig. [3](#S2.F3),
the framework has two parallel branches, i.e. a classification and a semantic segmentation branch.
Both branches share the same vision transformer backbone, and update the entire network simultaneously during training.
As illustrated in Fig. [9](#S4.F9),
the core of our approach is double-backward propagation.
That is, the network back propagates to compute GETAM without updating to obtain pseudo labels, then back propagates again to optimize the network supervised by these pseudo labels.
Each iteration consists of two back propagation operations but the network is only updated once.
Specifically, we first perform a forward pass to produce classification predictions without calculating the classification loss.
Then, for the target class , we back propagate its output to obtain GETAM.
We iterate to obtain class-wise attention maps for every class appearing in the image, and use them
to generate pseudo segmentation labels.
In the second back propagation step, we clear the gradients and perform another forward pass to generate classification and semantic segmentation predictions. With the pixel level pseudo labels and image level labels, we train our network with classification and segmentation predictions from the second back propagation.
Back propagating GETAM
leads to improved localization of objects and segmentation performance.
The proposed double-backward propagation does not rely on
multi-step WSSS training, and shows competitive performance (see Table [5](#S5.T5)).
5 Experiments
5.1 Setup and Implementation Details
Our method is evaluated on the PASCAL VOC [[18](#bib.bib18)] and MS-COCO datasets [[41](#bib.bib41)].
PASCAL VOC [[18](#bib.bib18)] has one background and 20 foreground classes. The official dataset consists of 1,446
training, 1,449 validation and 1456 test images.
We follow common practice [[24](#bib.bib24)], augmenting the training set to form a total of 10,582 images.
MS-COCO 2014 [[41](#bib.bib41)] contains 81 classes including the background class with 80k train and 40k val images and more complex scenes, which is more difficult for WSSS.
In addition, we adopt [[45](#bib.bib45)] as our saliency detection model by re-implementing it to generate saliency maps on both datasets.
The backbone network of our end-to-end framework is ViT [[17](#bib.bib17)]
.
We also test our method on other backbones including ViT-Hybrid [[17](#bib.bib17)], Deit [[60](#bib.bib60)] and Deit_Distilled [[60](#bib.bib60)].
Our end-to-end framework has two branches, i.e. a classification branch and segmentation branch, and they share the same vision transformer backbone.
For the segmentation branch, we adopt the decoder from
[[49](#bib.bib49)].
We train our network for 20 epochs, separated into two stages.
In the first 10 epochs we only update the classification branch in order to generate reliable class attention maps.
In the remaining 10 epochs we switch on the segmentation branch and simultaneously optimize two branches.
Further, our generated pseudo labels can also be used in a multi-stage fashion, we use the pseudo labels to train Deeplab v2 [[13](#bib.bib13)] with the ResNet-101 backbone.
Our model is implemented with PyTorch, with reproduction details in the supplementary material.
5.2 Ablation Studies
5.2.1 Effectiveness of GETAM
The proposed GETAM is a class-wise activation visualization method for vision transformers.
We explore different ways of generating CAMs on transformer backbones and report their performances on PASCAL VOC
as shown in Table [1](#S5.T1).
First, we directly leverage CAM [[81](#bib.bib81)] and Grad_CAM [[53](#bib.bib53)] on vision transformers as baselines.
The proposed GETAM achieves significant improvements over CAM and Grad_CAM (+16.4 mIoU and +9.2 mIoU), demonstrating that it is non-trivial to directly use existing visualization methods on the transformer networks.
TS_CAM [[22](#bib.bib22)] is a transformer based localization method, we follow its implementation and report the segmentation result.
Furthermore, in GETAM we propose to couple the attention maps with the square of corresponding gradients,
we implement a variation that we directly compute the element-wise production of the attention maps and gradient maps, we denote this method as
.
Our GETAM achieves a 2.6 mIoU improvement over this variation. It verifies the effectiveness of the coupling strategy of GETAM.
| Method | Backbone | CAM generation | mIoU(val) |
| CNN | CAM | 64.7 | |
| ViT |
TS_CAM[
|
5.2.2 Effectiveness of Activation Aware Label Completion
We propose activation aware label completion to generate pseudo labels from CAMs.
In Table [2](#S5.T2),
we demonstrate that the proposed Activation Aware Label Completion brings improvements over the CRF-based method under two settings.
For the CNN network it improves the baseline [[74](#bib.bib74)] by 2.1 mIoU,
for the ViT network the improvement is 7.7 mIoU.
This validates that our activation aware label completion helps generate better pseudo labels from the activation maps on both CNN and transformer backbones.
| Model | Backbone | CAM generation | Pseudo generation | mIoU(val) |
|
RRM[
|
| Methods | Train | Val |
| Multi stage methods | ||
|
SEAM[
|
[8](#bib.bib8)] + RW + CRF[56](#bib.bib56)][1](#bib.bib1)][56](#bib.bib56)][76](#bib.bib76)][69](#bib.bib69)] + CRF[35](#bib.bib35)] + RW + CRF[35](#bib.bib35)] + IRN + CRF[3](#bib.bib3)][3](#bib.bib3)] + CRF[17](#bib.bib17)].
5.2.3 Pseudo Label Quality
Pseudo label quality is crucial to segmentation performance for WSSS.
We extract the generated pseudo labels in our end-to-end training process and evaluate them for quality with the PASCAL VOC ground-truth.
The results in Table [3](#S5.T3) show that
the pseudo segmentation labels of GETAM outperform all end-to-end methods.
Further, recent state-of-the-art multi-step approaches focus on obtaining pseudo labels using sophisticated pipelines and training multiple networks, our pseudo labels are still comparable to the best of these.
In addition, we trained deeplabv2 [[13](#bib.bib13)] using our pseudo labels in an multi-stage manner
and achieve a 70.6 mIoU on the PASCAL validation set.
We report single-stage methods in Table [5](#S5.T5).
| Backbone | MIoU (Val) | MIoU (Test) |
|
AALR[
|
5.2.4 Results with Different Vision Transformer Backbones
We investigate different vision transformer backbones including ViT, ViT-Hybrid [[49](#bib.bib49)], Deit and Deit-Distilled [[60](#bib.bib60)] in our end-to-end WSSS framework, where all networks have 12 transformer layers
. In ViT_Hybrid, we aggregate attention maps from last 6 layers so as to decrease low-level noise from convolution, while in other backbones we aggregate attention from all 12 layers 111We refer the reader to the supplementary material for ablation..
As reported in Table [4](#S5.T4), our method performs consistently better than the previous state-of-the-art single-stage method AALR [[78](#bib.bib78)], validating the effectiveness of our approach.
The efficiency of the proposed GETAM on various backbones also makes it a visualization tool for transformer networks(Fig. [10](#S5.F10)).
It is widely recognized that convolutional structures in transformers provide performance gains in vision tasks [[17](#bib.bib17), [68](#bib.bib68), [16](#bib.bib16)]. Here we can see that ViT_Hybrid achieves the best performances among these backbones.
| Method | Backbone | Sup. | val | test | |
| Multi-stage |
SEAM[
|
[8](#bib.bib8)] (CVPR2020)[75](#bib.bib75)] (NeurIPS2020)[56](#bib.bib56)] (ICCV2021)[55](#bib.bib55)] (ECCV2020)[56](#bib.bib56)] (ICCV2021)[20](#bib.bib20)] (ECCV2020)[19](#bib.bib19)] (CVPR2020)[76](#bib.bib76)] (ICCV2021)[32](#bib.bib32)] (ICCV2021)[70](#bib.bib70)] (ICCV2021)[39](#bib.bib39)] (ICCV2021)[33](#bib.bib33)](NeurIPS2021)[71](#bib.bib71)] (CVPR2021)[30](#bib.bib30)] (AAAI2021)[51](#bib.bib51)] (IJCV2022)[69](#bib.bib69)] (CVPR2021)[37](#bib.bib37)](CVPR2021)[38](#bib.bib38)] (AAAI2022)[47](#bib.bib47)] (ICCV2015)[25](#bib.bib25)] (CVPR2016)[50](#bib.bib50)] (CVPR2017)[74](#bib.bib74)] (AAAI2020)[3](#bib.bib3)] (CVPR2020)[73](#bib.bib73)] (ICCV2019)[78](#bib.bib78)] (ACMMM2021)[41](#bib.bib41)], S: saliency.
| Method | Backbone | Single-stage | MIoU (val) |
|
SEC [
|
[27](#bib.bib27)] (CVPR2018)[65](#bib.bib65)] (IJCV2020)[44](#bib.bib44)] (AAAI2020)[66](#bib.bib66)] (CVPR2020)[75](#bib.bib75)] (NeurIPS2020)[56](#bib.bib56)] (ICCV2021)[70](#bib.bib70)] (ICCV2021)[37](#bib.bib37)] (CVPR2021)[51](#bib.bib51)] (IJCV2022)[32](#bib.bib32)] (ICCV2021)[39](#bib.bib39)] (ICCV2021)[38](#bib.bib38)] (AAAI2022)[33](#bib.bib33)] (NeurIPS2021)[41](#bib.bib41)]. GETAM is the first end-to-end method evaluated on MS-COCO that performs on par with existing methods.
5.3 Comparison to the State-of-the-art Methods
5.3.1 PASCAL VOC
In Table [5](#S5.T5), we give a detailed comparison of our proposed approach with other WSSS methods.
In the single-stage section,
we achieve significantly improved performance over all existing end-to-end methods. Comparing to previous state-of-the-art method AALR [[78](#bib.bib78)], we have an impressive 7.8% mIoU increase.
Compared to multi-stage methods,
our result
based on ViT_Hybrid (71.7 mIoU on val and 72.3 mIoU on test) achieves new state-of-the-art on PASCAL VOC.
And our single-stage performances with other transformers including ViT, Deit and Deit_Distilled are also significantly ahead of existing single-stage approaches, and competitive with multi-stage ones, showing the robustness of GETAM to transformer backbones.
Notably, our approach is the first single-stage method that outperforms the multi-stage methods, which employ sophisticated pipelines and train multiple networks.
For example, the previous state-of-the-art URN [[38](#bib.bib38)] requires three stages with many inter-dependencies, our single-stage method still outperforms it by 0.5 mIoU on val and 0.8 mIoU on test.
5.3.2 MS-COCO
To further demonstrate the proposed method’s effectiveness across different datasets, we evaluate it on the challenging MS-COCO dataset [[41](#bib.bib41)].
As shown in Table [6](#S5.T6), our method achieves 36.4% mIoU.
PMM [[39](#bib.bib39)], URN [[38](#bib.bib38)] and RIB [[33](#bib.bib33)] are the only methods that outperform ours. They are all multi-stage methods, requiring training at least two networks.
RIB [[33](#bib.bib33)] has four training steps to obtain final segmentation results.
Our method still outperforms them on PASCAL VOC (Table [5](#S5.T5)), which demonstrates promising ability when trained over different datasets.
Notably, our method is the first end-to-end WSSS method that has reported a result on MS-COCO which saves on training complexity.
6 Conclusion
In this paper, we propose a vision transformer based WSSS framework by exploring the activation mechanism for transformers. Specifically, we propose a new transformer-based activation visualisation approach, GETAM. It generates class-wise attention maps that can better capture the object shape compared to previous methods. Based on GETAM, we introduce an activation aware label completion module to generate high-quality pseudo labels, it adopts saliency information to refine foreground object masks without suppressing background objects. Finally, we present a novel double-backward propagation scheme to integrate the proposed modules into an end-to-end training framework. We validate GETAM on weakly the supervised semantic segmentation task, extensive experimental results on both multi-stage and single-stage training show the effectiveness of our method with different transformer backbones. The proposed method offers a new perspective for WSSS using vision transformers, and we believe that it can further facilitate related research areas.
References
- [1] Jiwoon Ahn, Sunghyun Cho, and Suha Kwak. Weakly supervised learning of instance segmentation with inter-pixel relations. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 2209–2218, Long Beach, CA, USA, 2019. Computer Vision Foundation / IEEE.
- [2] Jiwoon Ahn and Suha Kwak. Learning pixel-level semantic affinity with image-level supervision for weakly supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 4981–4990. Computer Vision Foundation / IEEE, 2018.
- [3] Nikita Araslanov and Stefan Roth. Single-stage semantic segmentation from image labels. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 4252–4261. Computer Vision Foundation / IEEE, June 2020.
- [4] Sebastian Bach, Alexander Binder, Grégoire Montavon, Frederick Klauschen, Klaus-Robert Müller, and Wojciech Samek. On pixel-wise explanations for non-linear classifier decisions by layer-wise relevance propagation. PloS one, 10(7):e0130140, 2015.
- [5] Hangbo Bao, Li Dong, and Furu Wei. Beit: Bert pre-training of image transformers, 2021.
- [6] Amy Bearman, Olga Russakovsky, Vittorio Ferrari, and Li Fei-Fei. What’s the point: Semantic segmentation with point supervision. In European Conference on Computer Vision (ECCV), pages 549–565, 2016.
- [7] Yu-Ting Chang, Qiaosong Wang, Wei-Chih Hung, Robinson Piramuthu, Yi-Hsuan Tsai, and Ming-Hsuan Yang. Mixup-cam: Weakly-supervised semantic segmentation via uncertainty regularization. In British Machine Vision Conference (BMVC), Virtual Event, UK, 2020. BMVA Press.
- [8] Yu-Ting Chang, Qiaosong Wang, Wei-Chih Hung, Robinson Piramuthu, Yi-Hsuan Tsai, and Ming-Hsuan Yang. Weakly-supervised semantic segmentation via sub-category exploration. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 8991–9000. Computer Vision Foundation / IEEE, 2020.
- [9] Aditya Chattopadhay, Anirban Sarkar, Prantik Howlader, and Vineeth N Balasubramanian. Grad-cam++: Generalized gradient-based visual explanations for deep convolutional networks. In 2018 IEEE winter conference on applications of computer vision (WACV), pages 839–847. IEEE, 2018.
- [10] Hila Chefer, Shir Gur, and Lior Wolf. Generic attention-model explainability for interpreting bi-modal and encoder-decoder transformers, 2021.
- [11] Hila Chefer, Shir Gur, and Lior Wolf. Transformer interpretability beyond attention visualization, 2021.
- [12] Liang-Chieh Chen, George Papandreou, Iasonas Kokkinos, Kevin Murphy, and Alan L. Yuille. Semantic image segmentation with deep convolutional nets and fully connected crfs. In Yoshua Bengio and Yann LeCun, editors, International Conference on Learning Representations (ICLR), 2015.
- [13] Liang-Chieh Chen, George Papandreou, Iasonas Kokkinos, Kevin Murphy, and Alan L Yuille. Deeplab: Semantic image segmentation with deep convolutional nets, atrous convolution, and fully connected crfs. IEEE Transactions on Pattern Analysis and Machine Intelligence (TPAMI), 40(4):834–848, 2017.
- [14] Liang-Chieh Chen, George Papandreou, Florian Schroff, and Hartwig Adam. Rethinking atrous convolution for semantic image segmentation. ArXiv e-prints, 2017.
- [15] Jifeng Dai, Kaiming He, and Jian Sun. Boxsup: Exploiting bounding boxes to supervise convolutional networks for semantic segmentation. In IEEE International Conference on Computer Vision (ICCV), pages 1635–1643, 2015.
- [16] Zihang Dai, Hanxiao Liu, Quoc Le, and Mingxing Tan. Coatnet: Marrying convolution and attention for all data sizes. Advances in Neural Information Processing Systems, 34, 2021.
- [17] Alexey Dosovitskiy, Lucas Beyer, Alexander Kolesnikov, Dirk Weissenborn, Xiaohua Zhai, Thomas Unterthiner, Mostafa Dehghani, Matthias Minderer, Georg Heigold, Sylvain Gelly, et al. An image is worth 16x16 words: Transformers for image recognition at scale. arXiv preprint arXiv:2010.11929, 2020.
- [18] Mark Everingham, Luc Van Gool, Christopher KI Williams, John Winn, and Andrew Zisserman. The pascal visual object classes (voc) challenge. International Journal of Computer Vision (IJCV), 88(2):303–338, 2010.
- [19] Junsong Fan, Zhaoxiang Zhang, Chunfeng Song, and Tieniu Tan. Learning integral objects with intra-class discriminator for weakly-supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 4283–4292. Computer Vision Foundation / IEEE, 2020.
- [20] Junsong Fan, Zhaoxiang Zhang, and Tieniu Tan. Employing multi-estimations for weakly-supervised semantic segmentation. In European Conference on Computer Vision (ECCV), pages 332–348, 2020.
- [21] Junsong Fan, Zhaoxiang Zhang, Tieniu Tan, Chunfeng Song, and Jun Xiao. Cian: Cross-image afﬁnity net for weakly supervised semantic segmentation. In AAAI Conference on Artificial Intelligence (AAAI), 2020.
- [22] Wei Gao, Fang Wan, Xingjia Pan, Zhiliang Peng, Qi Tian, Zhenjun Han, Bolei Zhou, and Qixiang Ye. Ts-cam: Token semantic coupled attention map for weakly supervised object localization, 2021.
- [23] Hongyu Guo, Yongyi Mao, and Richong Zhang. Mixup as locally linear out-of-manifold regularization. In AAAI Conference on Artificial Intelligence (AAAI), volume 33, pages 3714–3722, 2019.
- [24] Bharath Hariharan, Pablo Arbeláez, Lubomir Bourdev, Subhransu Maji, and Jitendra Malik. Semantic contours from inverse detectors. In IEEE International Conference on Computer Vision (ICCV), pages 991–998. IEEE, 2011.
- [25] Seunghoon Hong, Junhyuk Oh, Honglak Lee, and Bohyung Han. Learning transferrable knowledge for semantic segmentation with deep convolutional neural network. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 3204–3212. Computer Vision Foundation / IEEE, 2016.
- [26] Qibin Hou, PengTao Jiang, Yunchao Wei, and Ming-Ming Cheng. Self-erasing network for integral object attention. In Conference on Neural Information Processing Systems (NeurIPS), pages 549–559, 2018.
- [27] Zilong Huang, Xinggang Wang, Jiasi Wang, Wenyu Liu, and Jingdong Wang. Weakly-supervised semantic segmentation network with deep seeded region growing. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 7014–7023. Computer Vision Foundation / IEEE, 2018.
- [28] Peng-Tao Jiang, Qibin Hou, Yang Cao, Ming-Ming Cheng, Yunchao Wei, and Hong-Kai Xiong. Integral object mining via online attention accumulation. In IEEE International Conference on Computer Vision (ICCV), pages 2070–2079, 2019.
- [29] Peng-Tao Jiang, Chang-Bin Zhang, Qibin Hou, Ming-Ming Cheng, and Yunchao Wei. Layercam: Exploring hierarchical class activation maps for localization. IEEE Transactions on Image Processing (TIP), 30:5875–5888, 2021.
- [30] Beomyoung Kim, Sangeun Han, and Junmo Kim. Discriminative region suppression for weakly-supervised semantic segmentation. In AAAI Conference on Artificial Intelligence (AAAI), pages 1754–1761, 2021.
- [31] Alexander Kolesnikov and Christoph H Lampert. Seed, expand and constrain: Three principles for weakly-supervised image segmentation. In European Conference on Computer Vision (ECCV), pages 695–711. Springer, 2016.
- [32] Hyeokjun Kweon, Sung-Hoon Yoon, Hyeonseong Kim, Daehee Park, and Kuk-Jin Yoon. Unlocking the potential of ordinary classifier: Class-specific adversarial erasing framework for weakly supervised semantic segmentation. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pages 6994–7003, October 2021.
- [33] Jungbeom Lee, Jooyoung Choi, Jisoo Mok, and Sungroh Yoon. Reducing information bottleneck for weakly supervised semantic segmentation. Advances in Neural Information Processing Systems, 34, 2021.
- [34] Jungbeom Lee, Eunji Kim, Sungmin Lee, Jangho Lee, and Sungroh Yoon. Ficklenet: Weakly and semi-supervised semantic image segmentation using stochastic inference. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 5267–5276. Computer Vision Foundation / IEEE, 2019.
- [35] Jungbeom Lee, Eunji Kim, and Sungroh Yoon. Anti-adversarially manipulated attributions for weakly and semi-supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 4071–4080. Computer Vision Foundation / IEEE, 2021.
- [36] Jungbeom Lee, Jihun Yi, Chaehun Shin, and Sungroh Yoon. Bbam: Bounding box attribution map for weakly supervised semantic and instance segmentation, 2021.
- [37] Seungho Lee, Minhyun Lee, Jongwuk Lee, and Hyunjung Shim. Railroad is not a train: Saliency as pseudo-pixel supervision for weakly supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 5495–5505. Computer Vision Foundation / IEEE, 2021.
- [38] Yi Li, Yiqun Duan, Zhanghui Kuang, Yimin Chen, Wayne Zhang, and Xiaomeng Li. Uncertainty estimation via response scaling for pseudo-mask noise mitigation in weakly-supervised semantic segmentation. arXiv preprint arXiv:2112.07431, 2021.
- [39] Yi Li, Zhanghui Kuang, Liyang Liu, Yimin Chen, and Wayne Zhang. Pseudo-mask matters in weakly-supervised semantic segmentation. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pages 6964–6973, October 2021.
- [40] Di Lin, Jifeng Dai, Jiaya Jia, Kaiming He, and Jian Sun. Scribblesup: Scribble-supervised convolutional networks for semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 3159–3167. Computer Vision Foundation / IEEE, 2016.
- [41] Tsung-Yi Lin, Michael Maire, Serge Belongie, James Hays, Pietro Perona, Deva Ramanan, Piotr Dollár, and C Lawrence Zitnick. Microsoft coco: Common objects in context. In European Conference on Computer Vision (ECCV), pages 740–755, 2014.
- [42] Ze Liu, Yutong Lin, Yue Cao, Han Hu, Yixuan Wei, Zheng Zhang, Stephen Lin, and Baining Guo. Swin transformer: Hierarchical vision transformer using shifted windows. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 10012–10022, 2021.
- [43] Jonathan Long, Evan Shelhamer, and Trevor Darrell. Fully convolutional networks for semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 3431–3440. Computer Vision Foundation / IEEE, 2015.
- [44] Wenfeng Luo and Meng Yang. Learning saliency-free model with generic features for weakly-supervised semantic segmentation. In AAAI Conference on Artificial Intelligence (AAAI), pages 11717–11724, 2020.
- [45] Yuxin Mao, Jing Zhang, Zhexiong Wan, Yuchao Dai, Aixuan Li, Yunqiu Lv, Xinyu Tian, Deng-Ping Fan, and Nick Barnes. Transformer transforms salient object detection and camouflaged object detection, 2021.
- [46] Youngmin Oh, Beomjun Kim, and Bumsub Ham. Background-aware pooling and noise-aware loss for weakly-supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 6913–6922. Computer Vision Foundation / IEEE, 2021.
- [47] George Papandreou, Liang-Chieh Chen, Kevin P Murphy, and Alan L Yuille. Weakly-and semi-supervised learning of a deep convolutional network for semantic image segmentation. In IEEE International Conference on Computer Vision (ICCV), pages 1742–1750, 2015.
- [48] Pedro O Pinheiro and Ronan Collobert. From image-level to pixel-level labeling with convolutional networks. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 1713–1721. Computer Vision Foundation / IEEE, 2015.
- [49] René Ranftl, Alexey Bochkovskiy, and Vladlen Koltun. Vision transformers for dense prediction. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 12179–12188, 2021.
- [50] Anirban Roy and Sinisa Todorovic. Combining bottom-up, top-down, and smoothness cues for weakly supervised image segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 3529–3538. Computer Vision Foundation / IEEE, 2017.
- [51] Lixiang Ru, Bo Du, Yibing Zhan, and Chen Wu. Weakly-supervised semantic segmentation with visual words learning and hybrid pooling. International Journal of Computer Vision, pages 1–18, 2022.
- [52] Ramprasaath R Selvaraju, Michael Cogswell, Abhishek Das, Ramakrishna Vedantam, Devi Parikh, and Dhruv Batra. Grad-cam: Visual explanations from deep networks via gradient-based localization. In Proceedings of the IEEE international conference on computer vision, pages 618–626, 2017.
- [53] Ramprasaath R Selvaraju, Abhishek Das, Ramakrishna Vedantam, Michael Cogswell, Devi Parikh, and Dhruv Batra. Grad-cam: Why did you say that? arXiv preprint arXiv:1611.07450, 2016.
- [54] Robin Strudel, Ricardo Garcia, Ivan Laptev, and Cordelia Schmid. Segmenter: Transformer for semantic segmentation. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 7262–7272, 2021.
- [55] Guolei Sun, Wenguan Wang, Jifeng Dai, and Luc Van Gool. Mining cross-image semantics for weakly supervised semantic segmentation. arXiv preprint arXiv:2007.01947, 2020.
- [56] Kunyang Sun, Haoqing Shi, Zhengming Zhang, and Yongming Huang. Ecs-net: Improving weakly supervised semantic segmentation by using connections between class activation maps. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pages 7283–7292, October 2021.
- [57] Weixuan Sun, Jing Zhang, and Nick Barnes. 3d guided weakly supervised semantic segmentation. In Proceedings of the Asian Conference on Computer Vision, 2020.
- [58] Weixuan Sun, Jing Zhang, and Nick Barnes. Inferring the class conditional response map for weakly supervised semantic segmentation. In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision, pages 2878–2887, 2022.
- [59] Meng Tang, Federico Perazzi, Abdelaziz Djelouah, Ismail Ben Ayed, Christopher Schroers, and Yuri Boykov. On regularized losses for weakly-supervised cnn segmentation. In European Conference on Computer Vision (ECCV), pages 507–522, 2018.
- [60] Hugo Touvron, Matthieu Cord, Matthijs Douze, Francisco Massa, Alexandre Sablayrolles, and Hervé Jégou. Training data-efficient image transformers & distillation through attention. In International Conference on Machine Learning (ICML), pages 10347–10357. PMLR, 2021.
- [61] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. Advances in neural information processing systems, 30, 2017.
- [62] Paul Vernaza and Manmohan Chandraker. Learning random-walk label propagation for weakly-supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 7158–7166. Computer Vision Foundation / IEEE, 2017.
- [63] Wenhai Wang, Enze Xie, Xiang Li, Deng-Ping Fan, Kaitao Song, Ding Liang, Tong Lu, Ping Luo, and Ling Shao. Pvtv2: Improved baselines with pyramid vision transformer, 2021.
- [64] Xinggang Wang, Jiapei Feng, Bin Hu, Qi Ding, Longjin Ran, Xiaoxin Chen, and Wenyu Liu. Weakly-supervised instance segmentation via class-agnostic learning with salient images. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 10225–10235, 2021.
- [65] Xiang Wang, Shaodi You, Xi Li, and Huimin Ma. Weakly-supervised semantic segmentation by iteratively mining common object features. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 1354–1362. Computer Vision Foundation / IEEE, 2018.
- [66] Yude Wang, Jie Zhang, Meina Kan, Shiguang Shan, and Xilin Chen. Self-supervised equivariant attention mechanism for weakly supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 12275–12284. Computer Vision Foundation / IEEE, 2020.
- [67] Jun Wei, Qin Wang, Zhen Li, Sheng Wang, S Kevin Zhou, and Shuguang Cui. Shallow feature matters for weakly supervised object localization. In Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition, pages 5993–6001, 2021.
- [68] Haiping Wu, Bin Xiao, Noel Codella, Mengchen Liu, Xiyang Dai, Lu Yuan, and Lei Zhang. Cvt: Introducing convolutions to vision transformers. In Proceedings of the IEEE/CVF International Conference on Computer Vision, pages 22–31, 2021.
- [69] Tong Wu, Junshi Huang, Guangyu Gao, Xiaoming Wei, Xiaolin Wei, Xuan Luo, and Chi Harold Liu. Embedded discriminative attention mechanism for weakly supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 16765–16774. Computer Vision Foundation / IEEE, 2021.
- [70] Lian Xu, Wanli Ouyang, Mohammed Bennamoun, Farid Boussaid, Ferdous Sohel, and Dan Xu. Leveraging auxiliary tasks with affinity learning for weakly supervised semantic segmentation. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pages 6984–6993, October 2021.
- [71] Yazhou Yao, Tao Chen, Guo-Sen Xie, Chuanyi Zhang, Fumin Shen, Qi Wu, Zhenmin Tang, and Jian Zhang. Non-salient region object mining for weakly supervised semantic segmentation. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 2623–2632. Computer Vision Foundation / IEEE, 2021.
- [72] Sangdoo Yun, Dongyoon Han, Seong Joon Oh, Sanghyuk Chun, Junsuk Choe, and Youngjoon Yoo. Cutmix: Regularization strategy to train strong classifiers with localizable features. In IEEE International Conference on Computer Vision (ICCV), pages 6023–6032, 2019.
- [73] Yu Zeng, Yunzhi Zhuge, Huchuan Lu, and Lihe Zhang. Joint learning of saliency detection and weakly supervised semantic segmentation. In IEEE International Conference on Computer Vision (ICCV), pages 7223–7233, 2019.
- [74] Bingfeng Zhang, Jimin Xiao, Yunchao Wei, Mingjie Sun, and Kaizhu Huang. Reliability does matter: An end-to-end weakly supervised semantic segmentation approach. In AAAI Conference on Artificial Intelligence (AAAI), pages 12765–12772, 2020.
- [75] Dong Zhang, Hanwang Zhang, Jinhui Tang, Xiansheng Hua, and Qianru Sun. Causal intervention for weakly-supervised semantic segmentation. arXiv preprint arXiv:2009.12547, 2020.
- [76] Fei Zhang, Chaochen Gu, Chenyue Zhang, and Yuchao Dai. Complementary patch for weakly supervised semantic segmentation. In Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV), pages 7242–7251, October 2021.
- [77] Tianyi Zhang, Guosheng Lin, Weide Liu, Jianfei Cai, and Alex Kot. Splitting vs. merging: Mining object regions with discrepancy and intersection loss for weakly supervised semantic segmentation. In European Conference on Computer Vision (ECCV), 2020.
- [78] Xiangrong Zhang, Zelin Peng, Peng Zhu, Tianyang Zhang, Chen Li, Huiyu Zhou, and Licheng Jiao. Adaptive affinity loss and erroneous pseudo-label refinement for weakly supervised semantic segmentation. In Proceedings of the 29th ACM International Conference on Multimedia, pages 5463–5472, 2021.
- [79] Zizhao Zhang, Han Zhang, Long Zhao, Ting Chen, and Tomas Pfister. Aggregating nested transformers. In arXiv preprint arXiv:2105.12723, 2021.
- [80] Hengshuang Zhao, Jianping Shi, Xiaojuan Qi, Xiaogang Wang, and Jiaya Jia. Pyramid scene parsing network. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 2881–2890. Computer Vision Foundation / IEEE, 2017.
- [81] Bolei Zhou, Aditya Khosla, Agata Lapedriza, Aude Oliva, and Antonio Torralba. Learning deep features for discriminative localization. In IEEE Conference on Computer Vision and Pattern Recognition (CVPR), pages 2921–2929. Computer Vision Foundation / IEEE, 2016.