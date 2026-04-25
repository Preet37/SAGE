# Source: https://arxiv.org/pdf/2212.01758.pdf
# Author: Yunhao Ge et al.
# Title: LiT: Zero-Shot Transfer with Locked-image Text Tuning
# Fetched via: jina
# Date: 2026-04-09

Title: 2212.01758v2.pdf



Number of Pages: 11

# Improving Zero-shot Generalization and Robustness of Multi-modal Models 

## Yunhao Ge 1,2∗, Jie Ren 1∗, Andrew Gallagher 1, Yuxiao Wang 1, Ming-Hsuan Yang 1,Hartwig Adam 1, Laurent Itti 2, Balaji Lakshminarayanan 1†, Jiaping Zhao 1†

> 1

## Google Research 2University of Southern California      

> ∗co-first author, †correspondence to {balajiln, jiapingz }@google.com

## Abstract 

Multi-modal image-text models such as CLIP and LiT have demonstrated impressive performance on image clas-sification benchmarks and their zero-shot generalization ability is particularly exciting. While the top-5 zero-shot accuracies of these models are very high, the top-1 accu-racies are much lower (over 25% gap in some cases). We investigate the reasons for this performance gap and find that many of the failure cases are caused by ambiguity in the text prompts. First, we develop a simple and efficient zero-shot post-hoc method to identify images whose top-1 prediction is likely to be incorrect, by measuring consis-tency of the predictions w.r.t. multiple prompts and image transformations. We show that our procedure better pre-dicts mistakes, outperforming the popular max logit base-line on selective prediction tasks. Next, we propose a simple and efficient way to improve accuracy on such uncertain im-ages by making use of the WordNet hierarchy; specifically we augment the original class by incorporating its parent and children from the semantic label hierarchy, and plug the augmentation into text prompts. We conduct experiments on both CLIP and LiT models with five different ImageNet-based datasets. For CLIP, our method improves the top-1 accuracy by 17.13% on the uncertain subset and 3.6% on the entire ImageNet validation set. We also show that our method improves across ImageNet shifted datasets, four other datasets, and other model architectures such as LiT. 

The proposed method 1 is hyperparameter-free, requires no additional model training and can be easily scaled to other large multi-modal architectures. Code is available at https://github.com/gyhandy/Hierarchy-CLIP .

## 1. Introduction 

Vision-language multi-modal models trained on large-scale data have achieved significant success in numerous domains and have demonstrated excellent zero-shot gener-alization ability [7, 12, 18, 19, 20, 28]. Given a test image and a set of candidate class labels, one can compute the similarity between the embedding of the image and the em-bedding of each candidate class labels, and predict the class 

> 1Work carried out mainly at Google

as the one with the highest similarity. The zero-shot top-1

accuracy for ImageNet [4] using CLIP variants (CLIP ViT-L) matches the performance of the original ResNet model trained from scratch. Recently, CLIP has been found to be more robust to distribution shift than ResNet, achieving good performance on ImageNet-V2 [21], ImageNet-R [9], ImageNet-A [11], and ImageNet-Sketch [25]. We noticed a large gap between the top-1 accuracy and top-5 accuracy, 64.2% vs. 89.4% respectively, revealing potential headroom for improvement. We investigated the cases where the top-1 prediction was incorrect but the top-5

prediction was correct, and identified several typical failure modes. Despite the well-known multi-label issues in Ima-geNet [1], we found many of the remaining failure cases are caused by noise and ambiguous text prompts related to the WordNet hierarchical structure of ImageNet. Some class names are quite general so that the model cannot correctly match images from their specific subclasses. For example, the hot-air balloon images belonging to the “balloon” class were misclassified as “airship”, see Figure 1 middle. On the other hand, some class names are too specific such that the model fails to correlate them with their more generic super-classes. For example, 96% of images with ground truth label “tusker” are wrongly classified as other elephant classes such as “Asian elephant”, see Figure 1 left. The fail-ure modes analysis suggests that the text encoder is very sensitive to inputs and as a result, the overall classification lacks robustness. Inspired by these observations, we propose to first iden-tify the subset of images whose top-1 prediction is likely to be incorrect, and then improve the accuracy for those images by a principled framework to augment their class labels by WordNet hierarchy. To estimate whether an im-age has an incorrect prediction, i.e., to estimate the predic-tion confidence, we use the consistency of predictions under different text prompt templates and image augmentations as a signal for prediction confidence estimation. Although prediction confidence estimation has been well studied in single-modal classification models, we found those com-monly used confidence scores, maximum softmax proba-

> arXiv:2212.01758v2 [cs.CV] 25 May 2023

bility [10] and maximum logit score [8], are not always re-liable for the multi-modal CLIP and LiT models due to the poor calibration of the logits scores. For example, among the 1K classes in ImageNet, the class with the greatest mean logit value (computed as the cosine similarity between im-age and text embeddings) is “fig” (the fruit). Though we don’t have access to CLIP private training data, we hypoth-esize that this might be due to “fig” being a common abbre-viation for “figure”, which frequently occurs in the training data and thus includes many non-fruit illustrations. In this work, we first propose a simple yet efficient zero-shot confidence estimation method better suited for CLIP, based on predictions’ self-consistency over different text prompts and image perturbations. [26] proposed using self-consistency among multiple model outputs to improve the reasoning accuracy of large language models. Here we extend the idea for confidence estimation in multi-modal models by measuring consistency of predictions under mul-tiple input text prompts and image transformations . Our method is effective at predicting mistakes; the identified low confidence subset has significantly lower top-1 accu-racy (21.58%) than the average accuracy (64.18%). Next, to improve the accuracy for the low confidence subset, we develop a label augmentation technique using Word-Net label hierarchy. Our method leverages semantic in-formation from ancestors (top-down) as well as children (bottom-up) and improves the top-1 accuracy of the subset to 38.71% (17.13% improvement). Our method not only improves model accuracy, but also model robustness, im-proving on ImageNet variants with distribution shift such as ImageNet-v2, ImageNet-R, ImageNet-Adversarial and Imagenet-Sketch. The main contributions of this work are: • We identified several failure modes for zero-shot Im-ageNet classification using multi-modal models, and our findings suggest that the text encoder is very sen-sitive to prompts. To improve the prediction accuracy, prompts need to be better designed. • We propose a simple yet efficient zero-shot confidence score that is better suited for multi-modal models, based on predictions’ self-consistency under different text prompts and image perturbations. • We develop a label augmentation technique that uses both ancestor and children labels from WordNet. By applying the label augmentation to the previously iden-tified low confidence subset of images, we signifi-cantly improve their prediction accuracy. 

## 2. Related work 

Confidence estimation. Reliably estimating the confi-dence of a prediction is helpful for downstream decision making and can ensure the safe deployment of machine learning models. A well-calibrated confidence estimation should assign low scores for incorrect predictions and high score for correct predictions. Maximum softmax probabil-ity [10] and maximum logit [8] are the most commonly used confidence scores for classification problems, because of their simplicity and computational efficiency. Recent works propose more sophisticated confidence estimation methods which either involve modifications to the classi-fication models or significantly increase the inference time. For example, Bayesian approaches such as Gaussian Pro-cess layer [16] and dropout-based variational inference [6] assume the weights in the neural networks are random vari-ables such that the final prediction follows a distribution. A large variance of a prediction indicates the low confidence of the prediction. Non-Bayesian methods such as ensemble-based methods which aggregate the predictions from mul-tiple models to improve the robustness of the confidence estimation [14, 27]. Those sophisticated methods were de-veloped and studied in the single-modal models, and the ap-plication to multi-modal models is not straightforward. In addition, those methods mostly require modification to the model and additional training, which becomes challenging to multi-modal models since the training data are generally not publicly available. In our work, we focus on a zero-shot confidence estimation that is exclusively designed for multi-modal models. Our method does not require addi-tional training, and is simple, efficient, and effective. 

Prompt engineering. Prompt engineering and learning has attracted much attention in vision and learning since the introduction of image-text models [12, 19, 28]. The image-text models align images and their text descriptions into a common space, which facilitates model generaliza-tion to unseen categories at inference time. However, it has been observed that downstream image classification accu-racy highly depends on the specific input prompts. This mo-tivates researchers to either fine-tune or auto-learn prompts when adapting multi-modal models to downstream vision tasks. [29, 30] propose CoOp and CoCoOp to automatically learn the prompt word embeddings in the few-shot settings, and show significant improvements over the vanilla zero-shot image classification based-on prompting. These are learning based approaches, requiring supervised data from downstream tasks, while our proposed method is zero-shot and post-hoc without using any supervised data. In concur-rent work, [24] proposes learning prompt embeddings in an unsupervised manner by minimizing the entropy of the av-eraged prediction probability distribution, where each pre-diction is based on a random augmentation applied to the input image. Our work differs from [24] in the sense that we do not learn an input-dependent prompt embedding. In-stead we only selectively modify the prompts using knowl-edge hierarchy for images that have unreliable predictions, and our modified new prompt is natural language rather than a numerical embedding. Figure 1. Typical failure modes in the cases where top-5 prediction was correct but top-1 was wrong. 

Label hierarchy. Label hierarchy or label ontology are re-lational graphs among semantic labels. WordNet is one of the most widely used concept ontologies, and it has been used for visual recognition problems. Fergus et al. [5] lever-age the WordNet hierarchy to define a semantic distance between any two categories and use this semantic distance to share labels. Deng et al. [3] propose a hierarchy and exclusion graph to explicitly model the semantic relations among labels, and significantly improve object classifica-tion by exploiting the rich label hierarchy. The idea of se-mantic distance defined on the WordNet ontology graph is also used in [22, 23] for transferring knowledge in zero-shot learning problems. We are similar to the above work in that we utilize the label semantics encoded by the label hierar-chy as well, but label hierarchy in our case is used in the multi-modality scenarios: textual labels and visual images are represented in the same latent space, therefore, the hi-erarchy structure is directly exploited in the representation space to steer the recognition process. 

## 3. Zero-shot inference failure case analysis 

Given that the top-1 accuracy (64.2%) is much lower than top-5 accuracy (89.4%) for zero-shot ImageNet clas-sification using CLIP, we investigated the failure cases that are “top-5 correct but top-1 wrong” (12605 images, 25.2% of all test images). Table. 1 in Suppl. shows some represen-tative classes. The failure modes are summarized as: 

(1) Class name does not specify super-class name: Some classes, whose class names do not have their WordNet an-cestor (e.g., “tusker”, one of 1k ImageNet classes, does not have its parent “elephant” in the class name), may have a relatively lower score than other classes, which explicitly have the ancestor present in the class name (e.g., “Asian elephant”). See examples in Fig. 1 (Left). 

(2) Class name does not specify sub-class name : If the class name is too abstract, then its CLIP embedding is not necessarily close to the image embedding: e.g, CLIP wrongly classifies most images from “balloon” class as air-ship, see Fig. 1 (Middle). That is because there are dis-tinct kinds of balloons, each belonging to a different se-mantic subgroup. Relying on the text embedding of the fine-grained children’s class names (e.g., using “hot-air bal-loon”) often fixes these errors. [1] reported the similar issue of label ambiguity in ImageNet. 

(3) Inconsistent naming between class names: Some ImageNet class names are nouns, but others are adjective-prefixed nouns. This may make CLIP text embedding bi-ased, see one example in Fig. 1 (Right) where images from “screw” class are misclassified as “metal nail”. 

## 4. Proposed Method 

As shown in Section 3, CLIP models can be sensitive to different text prompts for images in certain classes. In this section, we first propose a confidence estimation method to identify low confidence predictions. We show that the identified subset has much lower accuracy than the average (Sec.4.1). We next develop a principled method that uti-lizes knowledge hierarchy to improve the accuracy of the low confidence subset, and consequently improve the over-all accuracy on the whole datasets (Sec. 4.2). 

4.1. Self-consistent zero-shot confidence estimation 

Given an image x and a candidate class name c, where 

c ∈ C , |C| = 1000 , the CLIP model encodes x and c respec-tively by its image encoder fimage and text encoder ftext ,denoted as zm = fimage (x) and zc = ftext (c). The pre-diction logit score is defined as logit (x, c ) = cos( zm, zc),where cos( ·, ·) is the cosine similarity between two vectors, and the predicted class is arg max c∈C logit (x, c ). We esti-mate the confidence by the self-consistency rate when ap-plying different context prompts and image augmentations. 

Confidence estimation via text prompts. To improve the zero-shot classifier’s performance, the CLIP paper [19] hand crafted various context prompts, e.g. “Aphoto of a big {label }” and “ A photo of aplane 

> car
> dog
> bird
> …
> Prompt -1
> Prompt -2
> Prompt -n
> …
> Left-right flip
> Up-down flip
> rotation
> crop
> …
> Start with Top-5 predicti ons

Figure 2. Our zero-shot classification pipeline consists of 2 steps: confidence estimation via self-consistency (left block) and top-down and bottom-up label augmentation using the WordNet hierarchy (right block). See Algorithms 1 and 2 for pseudocode. 

small {label }”), for different datasets for the pur-pose of prompt ensembling: For an image x, given a set of context prompts T , the ensembled logit score is logit (x, T (c)) = 1

> |T |

P 

> t∈T

logit (x, t (c)) , where t(c) de-notes the new prompt after applying context prompt t(·) to 

c. Here instead of using the prompts for ensembling, we make use of the prompts to define our confidence score. Given a set of prompts T , we apply each of the prompt t(·)

for the classifier, and see if the top-1 prediction is the same as that when applying no prompt. We use the percentage of prompts that have consistent top-1 prediction with that without prompt as the confidence score ST (x), i.e. 

ST (x) = 

P 

> t∈T

1{ˆc(x, t ) = ˆ c(x, ∅)}|T |  (1) where ˆc(x, ∅) = arg max c∈C logit (x, c ) is the top-1 prediction using the pure class name, and ˆc(x, t ) =arg max c∈C logit (x, t (c)) is the top-1 prediction when ap-plying prompt t(·). Intuitively, a reliable prediction should have highly consistent top-1 predictions when context prompts are applied or not, and therefore should have a high confidence score ST (x) with respect to the prompt set T ,and vice versa. 

Confidence estimation via image perturbation. We can also estimate the confidence of a prediction based on the self-consistency when applying different perturbations to the input image. Intuitively, if the top-1 predictions are inconsistent when applying different image perturbations, the prediction is unreliable. Specifically, we consider the common image transformations, left-right flip, rotation, crop, etc., and apply the perturbation method b(·) to the input image, and infer the predicted class as ˆc(x, b ) =arg max c∈C logit (b(x), c ). We define the confidence score with respect to a set of image perturbations B as, 

SB(x) = 

P 

> b∈B

1{ˆc(x, b ) = ˆ c(x, ∅)}|B|  (2) We expect a high confidence prediction to have highly con-sistent prediction when applying different image perturba-tions, and therefore to have a high confidence score SB(x)

with respect to the image perturbation set B.

Determining the low confidence subset by combining the two confidence estimations. The confidence score we proposed in Eq. (1) and Eq. (2) are continuous values. A threshold needs to be determined if we want to select a sub-set of examples with low confidence using the continuous confidence score. In practice, the threshold can be chosen based on the requirement of recall and precision trade-off in the real application. In our study, to bypass the threshold se-lection, we propose to use a binary criterion for determining the low confidence set. For IamgeNet dataset, the CLIP paper [19] designed to-tal 80 context prompts. We define four sets based on the 80 prompts: the first 40 prompts T1, the last 40 prompts 

T2, all 80 prompts T3, and no prompts T4 = ∅. We ap-ply the four different sets of prompts to the classifier and see if their top-1 predictions are all consistent or not, i.e. 

ˆc(x, T1) = ˆc(x, T2) = ˆc(x, T3) = ˆc(x, T4). Then we determine the low confidence subset OT as those exam-ples who have inconsistent predictions among the 4 prompts sets. We studied other choices such as using a random set of 40 prompts as T1, or splitting the 80 prompts into more subgroups, and found the results were very similar. Similarly we also determine a low confidence subset OB

based on image perturbations. In practice we found left-right flip works the best among the above mentioned pertur-bations. Thus for simplicity, we compare the top-1 predic-tion when applying the left-right flip to the input image and Algorithm 1: Zero-shot confidence estimation                                                                         

> Input: Input images X={xi}Ni=1 , Candidate class set C,image encoder fimage and text encoder ftext , text threshold τt, image threshold τi
> Output: Low confidence set O
> 1Low confidence set OT← ∅ ▷Confidence estimation via text prompts
> 2Sample Ldifferent context prompt t1,t2. . . tL
> 3for xi∈ X do
> 4Compute ST(xi)based on Eq. (1)
> 5if ST(xi)> τ tthen
> xihas high confidence prediction
> else
> OT← O T∪xi
> 6Low confidence set OB← ∅ ▷Confidence estimation via image perturbation
> 7Sample Mperturbation methods b1, . . . , b M
> 8for xi∈ X do
> Compute SB(xi)based on Eq. (2)
> 9if SB(xi)> τ ithen
> xihas high confidence prediction
> else
> OB← O B∪xi
> 10 O ← O T∪ O B

the top-1 prediction when using raw image. If their predic-tions are not consistent, that example will be included into the low confidence set OB.Finally, we use the union of the two low confidence sets 

OT identified using the text prompts and and OB identified using the image perturbations as the final low confidence subset O in the following experiments. Algorithm 1 shows the low confidence set generation process. 

4.2. Top-down and bottom-up label augmentation using WordNet hierarchy 

Through extensive analysis of the incorrect predictions among the identified unreliable predictions, we found that many of them are caused by CLIP’s lack of robustness to prompts. Instead of tuning the prompt templates, we focus on how to augment {label } in “ A photo of a

> {label }

”. A proper prompt that specifies both the generic type and the more specific sub-types of this class are very important for correctly classifying the image. However, the ImageNet [4] class names are not all defined with similar specificity and some classes are more abstract than others, e.g. 350 classes have children, while the rest of the classes have no children. See Suppl. Fig. 1 for more details. To make the ImageNet classification problem better suited to CLIP, we leverage the underlying WordNet hierarchy and develop a top-down and bottom-up class name augmenta-tion method to improve zero-shot prediction accuracy for unreliable predictions. The WordNet hierarchy is a semantic concept ontology, with nodes being cognitive synonyms indicating different concepts, and edges indicating the super-subordinate rela-tion between concepts. Traveling upward from leaf nodes to the root, the concepts start from the very specific to the generic. For example, starting from the edge node “straw-berry” to the root are “berry”, “edible fruit”, “produce”, “food”, “solid”, “matter”, and “physical entity” (the root). As we have seen in the failure mode analysis, many of the imageNet class names suffer from either being too abstract or being too specific, so that their concepts do not align well with the visual concepts the CLIP model learned in training. We propose using the WordNet knowledge hierarchy to aug-ment the class labels in prompts so that the CLIP model has a better match between the image and prompts. 

Top-down: augmenting class names with parent. As shown in failure case analysis, adding the super-class name to reduce ambiguity and to encourage the model’s atten-tion on the generic concept is helpful for improving the ac-curacy. Therefore we propose using WordNet to find the parent node of the raw class name, and concatenate it to the class name, i.e. logit (x, c ) = logit (x, [c; p(c)]) where 

p(c) is the parent node’s name of the class name c, and 

[c; p(c)] means the string concatenation of the class name and the parent name. We apply the method to top-5 pre-dicted classes. Using the newly defined class names, we are able to re-rank the top-5 predictions for the identified unreliable subset of images. Note that WordNet contains a few very abstract class names for nodes, such as “physical entity”, “artifact”, “matter”, etc. We found that such parent nodes are not informative, hence we remove them. There are also many academic words in WordNet, for example the parent node of sea anemone is “anthozoan”, which can be rare in CLIP training data. Adding those academic words to class name makes the prediction even less robust. So we simplify the WordNet by pruning based on an estimation of the word frequency in CLIP training data by using embed-ding norm. 

Bottom-up: augmenting class names with children. 

Some ImageNet class names are generally abstract, but the ImageNet images may belong to a specific subtype of the class. For example, “balloon” is a class name in ImageNet, but most balloon images in ImageNet are actually “hot-air balloon”, which is a child of “balloon” in WordNet hier-archy. The logit score for a parent class is not necessarily higher than the score for its child classes, mismatching with hierarchy prior. To accurately classify the images using CLIP, we need to augment the class name with fine-grained child subclasses. For each class c having children in the WordNet hierarchy, we redefine the logit score as the max score over itself and all its children, i.e., logit (x, c ) =max {logit (x, c ), logit (x, c 1), . . . , logit (x, c r )}, where 

c1 . . . c r are the r children of the node c in the WordNet Algorithm 2: Top-down and bottom-up class label augmentation using WordNet hierarchy                                                

> Input: Input image x∈ O , top-5 candidate class set
> Ctop 5, sparse WordNet hierarchy H, image encoder fimage and text encoder ftext
> Output: Predicted class of x
> 1Candidate class set C ← ∅
> 2for c∈ C top 5do
> C ← C ∪ [c;parent (c)] , where parent (c)is the parent of cin H▷Top-down
> 3if chas r≥1children c1. . . c rin H then
> C ← C ∪ { [cj;parent (c)] }rj=1 ▷Bottom-up
> 4ˆc←arg max c∈C logit (x, c )
> if ˆc∈ C top 5then
> final prediction ←ˆc
> else
> final prediction ←parent (ˆ c)

hierarchy. We apply this bottom-up method to top-5

predicted class names, and re-rank the top predictions. 

Combining Top-down and bottom-up. In practice, we use both children and the ancestor(parent) to augment each class c, to transfer semantic information bidirectionally in both top-down and bottom-up way: the ancestor(parent) class is more generic than c, and has better chance to dis-ambiguate instance from a more abstract level; on the other hand, children categories have more specific attribute de-scription, and the attribute descriptions are semantically meaningful representations bridging the gap between the image embedding and its abstract class concept c. Then the final logit score between x and c is: 

logit (x, c ) = max {logit (x, [c; p(c)]) ,

logit (x, [c1; p(c)]) , . . . , logit (x, [cr ; p(c)]) } (3) where p(c) is parent of c, and c1 . . . c r are c’s children. The 

ˆc, where ˆc ∈ C top 5, with the maximal logit score is the pre-dicted class of x. See Algorithm 2 for details. 

## 5. Experiments and Results 

Our proposed method is composed of two steps and we conduct experiments to verify the effectiveness of each step: (1) Use zero-shot confidence estimation to identify the low confidence subset of samples (see Fig. 3 for the results), and (2) Augment the class label using top-down and bottom-up strategies based on the sparsified WordNet on the low confidence subset to improve the accuracy (See Table 1 and Table 2 for the results). 

5.1. Our proposed confidence score is better suited for selective prediction than baselines 

A well-calibrated confidence estimator should score high for those correct predictions, and low for incorrect predic-tions. As a result, a good confidence estimator should be a good predictor for prediction correctness. We plot the receiver operating characteristic (ROC) curve and compute the area under the ROC curve (AUC) as a quantitative mea-sure to compare our proposed confidence estimation with the baselines. An AUROC of 1.0 indicates perfect sepa-ration between correct and incorrect predictions, and 0.5 means the two groups are not distinguishable. Maximum logit score, max c∈C logit (x, c ) is one of the most commonly used confidence score for classification problems in single modal models [8], so we consider it as our baseline. Fig. 3a and 3c clearly show that our confidence score is signifi-cantly better than the baseline method at distinguishing be-tween correct and incorrect predictions, for both CLIP and LiT models. The AUC score for our proposed method is above 0.8 while that for the baseline method is around 0.7. We also compare our method with the baseline in the scenario of selective prediction. Given a budget of absten-tion rate α%, the best strategy is to abstain the α% samples with the lowest confidence scores. If the confidence score is well calibrated, the accuracy for the abstained set will be low and as an evidence the accuracy of the remaining set would be high. We plot the selective prediction curves [14], which reports the accuracy on the remaining set as a func-tion of the abstention rate. Fig. 3b and 3d show that our proposed confidence score results in higher accuracy than the baseline maximum logit score at all abstention rates for both CLIP and LiT. Prompt ensemble has been shown to improve accuracy and robustness of the prediction, so here we also compare ours with the maximum logit score after applying prompt ensemble. As shown in the selective prediction curves, al-though the prompt ensemble indeed helps to achieve higher accuracy (dashed line) than that using the pure class name (solid line), it is still inferior to our proposed method. 

5.2. Using hierarchy to help improve zero-shot ac-curacy on low confidence subset 

Using top-down and bottom-up label augmentation sig-nificantly improves the accuracy on the low confidence sub-set. We apply the top-down and bottom-up label augmenta-tion on the low confidence subset: to better combine child and parent name, we create a prompt template to trans-form the child and parent name pairs into a new class name 

˜c in natural language: “ {child } which is a kind of 

> {parent }

” (different prompt templates may have different results). Table 1 shows improvement of 17.13% on the top-1 accuracy (from 21.58% to 38.71%) for the identified low confidence subset of samples, and overall 3.6% on the top-1 accuracy (64.18% to 67.78%) for all samples in ImageNet. We show similar improvement on the zero-shot accuracy for ImageNet shifted datasets. To investigate if our method works for other multi-modal models, we apply it to the LiT [28] model and observe that our method improves accuracy (a) CLIP: Calibration ROC and AUC 0.0 0.2 0.4 0.6 0.8 1.0  

> False Positive Rate
> 0.0 0.2 0.4 0.6 0.8 1.0
> True Positive Rate
> Ours | AUC:0.84 Max logits (baseline)| AUC:0.67 Max logits with prompt (baseline)| AUC:0.68

(b) CLIP: Selective prediction 0.0 0.2 0.4 0.6 0.8 1.0 

> Abstention Rate
> 0.65 0.70 0.75 0.80 0.85 0.90
> Top-1 Accuracy
> Max logits (baseline) Max logits with prompt (baseline) Ours

(c) LiT: Calibration ROC and AUC 0.0 0.2 0.4 0.6 0.8 1.0  

> False Positive Rate
> 0.0 0.2 0.4 0.6 0.8 1.0
> True Positive Rate
> Ours | AUC:0.81 Max logits (baseline)| AUC:0.70 Max logits with prompt (baseline)| AUC:0.69

(d) LiT: Selective Prediction 0.0 0.2 0.4 0.6 0.8 1.0 

> Abstention Rate
> 0.70 0.75 0.80 0.85 0.90
> Top-1 Accuracy
> Max logits (baseline) Max logits with prompt (baseline) Ours

Figure 3. ROC plots (left column) show that our proposed confidence score is better at distinguishing correct and incorrect predictions and results in higher AUC scores than baselines for both CLIP (ViT-B/16) (a) and LiT (ViT-B/32)(c). Selective prediction curves (right column) show that our proposed confidence score is better at abstaining incorrect predictions and as a result the accuracy of the remaining set is higher than the baselines for both CLIP (ViT-B/16) (b) and LiT (ViT-B/32) (d). Table 1. CLIP (ViT-B/16) and LiT (ViT-B/32) zero-shot top-1 accuracy comparison between baseline and ours (w/ hierarchy). 

CLIP (Ours) Hierarchy-CLIP LiT (Ours) Hierarchy-LiT ImageNet [4] Low conf. set 21.58% 38.71% 31.18% 37.25% 

Full set 64.18% 67.78% 68.26% 69.41% 

ImageNet-v2 [21] Low conf. set 17.77% 32.50% 27.08% 31.45% 

Full set 58.06% 61.07% 60.11% 61.11% 

ImageNet-R [9] Low conf. set 16.79% 27.91% 21.82% 22.93% 

Full set 56.88% 59.46% 66.54% 66.75% 

ImageNet-Adversarial [11] Low conf. set 10.13% 18.44% 7.19% 8.95% 

Full set 26.12% 29.23% 13.93% 14.56% 

ImageNet-Sketch [25] Low conf set 13.74% 23.18% 21.51% 24.42% 

Full set 44.71% 47.28% 52.47% 53.17% 

for LiT models as well. See Supp. Fig. 2 for qualitative visualization. 

Generalizability to non-ImageNet datasets To show the generalizability of our methods on non-ImageNet datasets, We conducted experiments on 4 additional datasets: Caltech-101 [15] (101 categories), Flower-102 [17] (102 flower categories), Food-101 [2] (101 food categories) and Cifar-100 [13] (100 categories). For each dataset, a subset of their categories are exist/aligned with WordNet hierar-chy, we only apply our method on those WordNet aligned class names, where we could find their ancestor and chil-dren. We keep the other class names unmodified. We use CLIP (ViT-B/16) as multi-modal model. Table 2 shows that our method consistently improved accuracy on the low-confidence set (low) and the entire set (full): 

Table 2. Generalizability to non-ImageNet datasets (CLIP (ViT-B/16) zero-shot top-1 accuracy). 

Dataset orig (low) ours (low) orig (full) ours (full) Caltech-101 [15] 10.6 % 27.2% (+16.6%) 74.1% 77.1% (+3.0%) Flower102 [17] 20.0% 29.4% (+9.4%) 63.7% 65.3% (+1.6%) Food-101 [2] 28.2% 49.0% (+20.8%) 84.7% 86.8% (+2.1%) Cifar-100 [13] 9.4% 17.5% (+8.1%) 31.8% 35.2% (+3.4%) 

5.3. Ablation study 

Generalizability to other backbones To study the gen-eralization of our method to different model architectures and sizes, we used 4 additional backbones of CLIP, includ-ing convolutional neural network (CNN) based backbones (ResNet-50, ResNet-101) and vision transformer (ViT) based backbones (ViT-B/32, ViT-B/16 and ViT-l/14). Ta-ble 3 shows the improved accuracy after using our method Table 3. Generalizability to different backbones with CLIP. backbone ResNet-50 ResNet-101 ViT-B/32 ViT-B/16 ViT-l/14 ACC (low) +14.25% +12.97% +15.12% + 17.13% +18.89% ACC (full) +3.73% +3.71% +3.65% + 3.60% +3.23% Table 4. CLIP (ViT-B-16) zero-shot top-1 accuracy comparison with prompt ensemble.                           

> Ensemble only Hierarchy and Ensemble ImageNet [21] Low conf. set 41.05% 42.09%
> Full set 68.48% 68.86%
> ImageNet-v2 [21] Low conf. set 36.39% 36.34% Full set 62.02% 62.00% ImageNet-R [9] Low conf. set 35.13% 36.12%
> Full set 60.21% 60.62%
> ImageNet-Adversarial [11] Low conf. set 21.13% 22.00%
> Full set 30.59% 31.07%
> ImageNet-Sketch [25] Low conf. set 27.13% 26.56% Full set 48.52% 48.26%

on ImageNet with CLIP models of different backbones. Our method achieves consistently improved accuracies. 

Our hierarchy-based label augmentation is complimen-tary to prompt ensembling. Prompt ensembling (PE) [19] requires a set of manually crafted prompt templates, and the zero-shot performance is sensitive to the set of prompts the model uses. Alternatively, our proposed method does not require a dedicated tuning of the prompt templates. We directly augment the class name with knowl-edge of the hierarchy from WordNet. In addition, PE is computationally intensive because it needs to infer the em-beddings of 80 prompt templates where each is applied with 1000 ImageNet classes, while our method only need to infer once for each of the predicted top-5 labels. Our method is more straightforward and interpretable given that it clearly shows the contribution of parent/child in the decision. In-tuitively, PE is typically focused on fixing {class } and aug-menting contextual templates, while our method augments the {class } with a fixed contextual template. To verify if our hierarchy-based method is complimentary with prompt en-sembling, we apply prompt ensembling after applying our top-down and bottom-up label augmentation. For the low confidence set, we first create a prompt template to trans-form the child and parent name pairs into a new class name 

˜c in natural language: “ {child } which is a kind of 

{parent }”. Then we apply the 80 prompts designed by the CLIP paper [19] individually to the new class name ˜c, and then ensemble them. For the high confidence set, since we do not modify the class name using hierarchy information, we only apply the prompt ensemble. The performance is shown in Table 4. We compare the zero-shot accuracy using the vanilla prompt ensembling method proposed in CLIP, and the zero-shot accuracy using our combined version of hierarchy-based class name augmentation and prompt en-sembling. As shown in the table, using both hierarchy and prompt ensembling achieves better or on par accuracy with the prompt ensemble alone, suggesting that the two 

Table 5. Effect of threshold of confidence score on zero-shot ac-curacy.                      

> Threshold Low conf. set size Acc on low conf. set Acc on full set 0.47 10000 19.40% 68.72% 0.52 11000 20.82% 68.78% 0.57 12000 22.06% 68.82% 0.62 13000 23.58% 68.85% 0.66 14000 25.01% 68.88%
> 0.70 15000 26.51% 68.86%

methods can be combined. Considering the prompt ensem-ble requires manually designed prompt templates and much greater inference time, our hierarchy-based class name aug-mentation is simple, efficient and effective. We also com-puted IoU of corrected low-confidence instances ( low set )between PE and our method: the IoU is 0.55, which implies the two methods are complementary for fixing errors. 

Effect of threshold of confidence score on zero-shot ac-curacy. In Table 1 we use a binary criterion to determine the low confidence set. We can alternatively use the contin-uous confidence score by choosing a threshold based on the trade-off between precision and recall. Changing the thresh-old of the confidence score can lead to different numbers of samples in the low confidence set. We study the effect of threshold on zero-shot accuracy. Table 5 shows the overall accuracy with different thresholds. We find that the overall accuracy is relatively robust to the threshold selection, in the wide range from 0.47 to 0.70. 

## 6. Conclusion 

Multi-modal models’ generalization and robustness is critical for deployment. Motivated by the big gap between top-1 and top-5 accuracy in ImageNet zero-shot classifica-tion, we investigated the failure modes and found that the model’s prediction is very sensitive to text prompts. We de-scribe a simple but efficient zero-shot post-hoc method to identify a subset of samples that are most likely to be pre-dicted wrongly by a measure of self-consistency. For those in the low confidence subset, we use the WordNet hierarchy to augment class labels to enhance the robustness, result-ing in up to 17.13% accuracy improvement on ImageNet. We show our method provides consistent improvement over other distribution shifted datasets (ImageNet variants), four other datasets, and is generalizable to other image-text mod-els and different backbones. 

Acknowledgments This work was supported in part by C-BRIC (one of six centers in JUMP, a Semiconductor Re-search Corporation (SRC) program sponsored by DARPA), DARPA (HR00112190134) and the Army Research Office (W911NF2020053). The authors affirm that the views ex-pressed herein are solely their own, and do not represent the views of the United States government or any agency thereof. References 

[1] Lucas Beyer, Olivier J H´ enaff, Alexander Kolesnikov, Xi-aohua Zhai, and A¨ aron van den Oord. Are we done with imagenet? arXiv preprint arXiv:2006.07159 , 2020. 1, 3 [2] Lukas Bossard, Matthieu Guillaumin, and Luc Van Gool. Food-101 – mining discriminative components with random forests. In European Conference on Computer Vision , 2014. 7[3] Jia Deng, Nan Ding, Yangqing Jia, Andrea Frome, Kevin Murphy, Samy Bengio, Yuan Li, Hartmut Neven, and Hartwig Adam. Large-scale object classification using label relation graphs. In ECCV , pages 48–64, 2014. 3 [4] Jia Deng, Wei Dong, Richard Socher, Li-Jia Li, Kai Li, and Li Fei-Fei. Imagenet: A large-scale hierarchical image database. In 2009 IEEE conference on computer vision and pattern recognition , pages 248–255. Ieee, 2009. 1, 5, 7 [5] Rob Fergus, Hector Bernal, Yair Weiss, and Antonio Tor-ralba. Semantic label sharing for learning with many cate-gories. In ECCV , pages 762–775, 2010. 3 [6] Yarin Gal and Zoubin Ghahramani. Dropout as abayesian approximation: Representing model uncertainty in deep learning. arxiv e-prints, page. arXiv preprint arXiv:1506.02142 , 3, 2015. 2 [7] Yunhao Ge, Jiashu Xu, Brian Nlong Zhao, Laurent Itti, and Vibhav Vineet. Dall-e for detection: Language-driven con-text image synthesis for object detection. arXiv preprint arXiv:2206.09592 , 2022. 1 [8] Dan Hendrycks, Steven Basart, Mantas Mazeika, Moham-madreza Mostajabi, Jacob Steinhardt, and Dawn Song. Scaling out-of-distribution detection for real-world settings. 

arXiv preprint arXiv:1911.11132 , 2019. 2, 6 [9] Dan Hendrycks, Steven Basart, Norman Mu, Saurav Kada-vath, Frank Wang, Evan Dorundo, Rahul Desai, Tyler Zhu, Samyak Parajuli, Mike Guo, et al. The many faces of robust-ness: A critical analysis of out-of-distribution generalization. In ICCV , 2021. 1, 7, 8 [10] Dan Hendrycks and Kevin Gimpel. A baseline for detect-ing misclassified and out-of-distribution examples in neural networks. arXiv preprint arXiv:1610.02136 , 2016. 2 [11] Dan Hendrycks, Kevin Zhao, Steven Basart, Jacob Stein-hardt, and Dawn Song. Natural adversarial examples. In 

CVPR , 2021. 1, 7, 8 [12] Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc Le, Yun-Hsuan Sung, Zhen Li, and Tom Duerig. Scaling up visual and vision-language representation learning with noisy text supervision. In ICML , pages 4904– 4916, 2021. 1, 2 [13] Alex Krizhevsky, Geoffrey Hinton, et al. Learning multiple layers of features from tiny images. 2009. 7 [14] Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell. Simple and scalable predictive uncertainty esti-mation using deep ensembles. NeurIPS , 30, 2017. 2, 6 [15] FF Li, M Andreetto, MA Ranzato, and P Perona. Cal-tech101. Computational Vision Group, California Institute of Technology , 2003. 7 [16] Jeremiah Zhe Liu, Shreyas Padhy, Jie Ren, Zi Lin, Yeming Wen, Ghassen Jerfel, Zack Nado, Jasper Snoek, Dustin Tran, and Balaji Lakshminarayanan. A simple approach to im-prove single-model deep uncertainty via distance-awareness. 

arXiv preprint arXiv:2205.00403 , 2022. 2 [17] Maria-Elena Nilsback and Andrew Zisserman. Automated flower classification over a large number of classes. In 2008 Sixth Indian Conference on Computer Vision, Graphics & Image Processing , pages 722–729. IEEE, 2008. 7 [18] Hieu Pham, Zihang Dai, Golnaz Ghiasi, Kenji Kawaguchi, Hanxiao Liu, Adams Wei Yu, Jiahui Yu, Yi-Ting Chen, Minh-Thang Luong, Yonghui Wu, et al. Combined scal-ing for open-vocabulary image classification. arXiv preprint arXiv:2111.10050 , 2021. 1 [19] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, et al. Learn-ing transferable visual models from natural language super-vision. In ICML , pages 8748–8763, 2021. 1, 2, 3, 4, 8 [20] Aditya Ramesh, Mikhail Pavlov, Gabriel Goh, Scott Gray, Chelsea Voss, Alec Radford, Mark Chen, and Ilya Sutskever. Zero-shot text-to-image generation. In International Confer-ence on Machine Learning , pages 8821–8831. PMLR, 2021. 1[21] Benjamin Recht, Rebecca Roelofs, Ludwig Schmidt, and Vaishaal Shankar. Do ImageNet classifiers generalize to Im-ageNet? In ICML , 2019. 1, 7, 8 [22] Marcus Rohrbach, Michael Stark, and Bernt Schiele. Eval-uating knowledge transfer and zero-shot learning in a large-scale setting. In CVPR , pages 1641–1648, 2011. 3 [23] Marcus Rohrbach, Michael Stark, Gy¨ orgy Szarvas, Iryna Gurevych, and Bernt Schiele. What helps where–and why? semantic relatedness for knowledge transfer. In CVPR , pages 910–917, 2010. 3 [24] Manli Shu, Weili Nie, De-An Huang, Zhiding Yu, Tom Goldstein, Anima Anandkumar, and Chaowei Xiao. Test-time prompt tuning for zero-shot generalization in vision-language models. arXiv preprint arXiv:2209.07511 , 2022. 2[25] Haohan Wang, Songwei Ge, Zachary Lipton, and Eric P Xing. Learning robust global representations by penaliz-ing local predictive power. In NeurIPS , pages 10506–10518, 2019. 1, 7, 8 [26] Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, and Denny Zhou. Self-consistency improves chain of thought reasoning in language models. arXiv preprint arXiv:2203.11171 , 2022. 2 [27] Yeming Wen, Dustin Tran, and Jimmy Ba. Batchensemble: an alternative approach to efficient ensemble and lifelong learning. arXiv preprint arXiv:2002.06715 , 2020. 2 [28] Xiaohua Zhai, Xiao Wang, Basil Mustafa, Andreas Steiner, Daniel Keysers, Alexander Kolesnikov, and Lucas Beyer. Lit: Zero-shot transfer with locked-image text tuning. In 

CVPR , pages 18123–18133, 2022. 1, 2, 6 [29] Kaiyang Zhou, Jingkang Yang, Chen Change Loy, and Zi-wei Liu. Conditional prompt learning for vision-language models. In CVPR , pages 16816–16825, 2022. 2 [30] Kaiyang Zhou, Jingkang Yang, Chen Change Loy, and Ziwei Liu. Learning to prompt for vision-language models. IJCV ,130(9):2337–2348, 2022. 2 Appendix A. Analyzing the classes for which the top-5 prediction is correct but the top-1 predic-tion is mostly incorrect                      

> Ground Truth Class Name Error rate tusker 94% missile 94% terrapin 92% collie 90% screw 90% mushroom 88% Appenzeller Sennenhund 84% snoek fish 84% husky 82% parallel bars 82% gazelle 82% sailboat 82% corn cob 80% analog clock 78% cornet 78% gossamer-winged butterfly 76% green mamba 76% tiger cat 74% hare 74% canoe 72% Table 6. List of top 20 classes where the top-5 prediction is correct but the top-1 prediction is mostly incorrect: sorted descendingly by error rate. The % indicates the proportion of images within the class whose top-5 prediction is correct but whose top-1 prediction is incorrect.

## B. Locating the 1000 ImageNet classes at WordNet hierarchy 

Fig. 4 shows the location of the 1000 ImageNet classes within the WordNet hierarchy. The 1000 ImageNet class names are at different levels of WordNet hierarchy with dif-ferent degrees of abstraction. 350 are super-classes with sub-classes as the children, while the remaining 650 are leaf nodes with no children. (b) The distribution of the number of children: 12.7% of the classes have one child node and 16.6% have 2-4 child nodes. 

## C. Additional results 

Qualitative visualization. Figure 5 shows a qualitative visualization on more typical failure modes in the cases where our top-down and bottom-up prompt augmentation using the WordNet hierarchy method fixes the error.       

> Table 7. Effect of WordNet sparsity on zero-shot top-1 accuracy on ImageNet with CLIP.
> % of remaining words acc overall 100% 68.52% 40% 68.52% 30% 68.72%
> 20% 68.72%
> 10% 68.72%

Effect of the model architecture and size on selected low-confidence sets on ImageNet. We found a more power-ful backbone leads to a smaller low-confidence sets (e.g., the low-confidence sets of ViT-l14 and ResNet-50 contain 8,557 and 13,106 images, respectively). 

Benefits to Top-5 accuracy. If we apply our top-down and bottom-up label augmentation method to re-rank top-10 classes, we see it can improve the top-5 on the low con-fidence set from 77.4% to 80.2%. We also find reranking top-10 further improves top-1 performance vs. re-ranking top-5 only. 

Sparsifying WordNet using the norm of text embedding. 

WordNet contains many academic words that are rarely used in common usage of English, and hence unlikely to occur frequently in the captions used for CLIP training. For example, “anthozoan, actinozoan”, “coelenterate”, “gastro-pod”, etc.. Directly using the raw WordNet with academic words as parents is not helpful for improving zero-shot ac-curacy, and can even hurt the performance. Though we do not have access to the CLIP private data, we studied the norm of the word embedding vector and found it is corre-lated with word frequency. We compute the L2 norm of the prompt embedding when plugging in the word into promt templates, i.e., ∥ftext (t(c)) ∥, t ∈ T . We found that the vari-ance of the norm, Var t∈T (∥ftext (t(c)) ∥), is correlated with word frequency. Rare words tend to have small variances, while common words tend to have large variances. For ex-ample, the variance of the rare word “anthozoan” is 0.118, while the variance of a more common word “workplace” is 0.724. We use this statistic to filter out rare words in Word-Net. We removed 60% of the nodes in WordNet and only kept the top 40% nodes with the highest variance and found this may work slightly better than using the whole WordNet in some cases. Our intuition behind the correlation between the norm variance and the word frequency is that, for a fre-quent word that has many examples in the CLIP training data, the CLIP model learns a very precise text embedding such that it has the capability to tell the semantic differ-ence under different contexts, e.g., “ a photo of a nice 

> {label }

” and “ a photo of a weird {label }”. Figure 4. (a) The 1000 ImageNet class names are at different levels of WordNet hierarchy with different degree of abstraction. 350 of them are super-class with sub-classes as the children, while the rest 650 of them have no children. (b) The distribution of the number of children: 12.7% of the classes have one child node, 16.6% of the classes have 2-4 child nodes. Failure mode 1: Class name does not specify super-class name 

90% of images with ground truth label “collie” are wrongly classified as other dog classes such as “Shetland Sheepdog”. Concatenating the parent class name “dog” fixes such errors. 

Failure mode 2: Class name does not specify sub-class name 

Failure mode 3: Inconsistent naming between class names 

Ground Truth: Collie 

Misclassified as: Shetland Sheepdog 

Parent: Dog 

Ground Truth: mink 

Misclassified as: European polecat 

Child: American mink 

Ground Truth: motorboat 

Misclassified as: trimaran 

Child: hydrofoil 

90% “collie” images wrongly classified as other dog classes which explicitly specifies “dog” e.g. “Shetland Sheepdog” 

78% of images with ground truth label “mink” are wrongly classified as other animal classes such as “European polecat”. Using child class names for “mink” (e.g. “American mink”) fixes such errors. 

62% of images with ground truth label “motorboat” are wrongly classified as other boat classes such as “trimaran”. Using child class names for “motorboat” (e.g. “hydrofoil”) fixes such errors. 

Figure 5. Qualitative visualization on typical failure modes for cases where our top-down and bottom-up prompt augmentation using the WordNet hierarchy method fixes the errors. In each case, the image is originally mis-classified but is correctly classified with our proposed method. 

Effect of WordNet sparsity on zero-shot accuracy We evaluate the effect of the degree of sparsity of WordNet on the downstream zero-shot accuracy. We sparsify the Word-Net based on word frequency, which is measured by em-bedding variance as described in the previous section. Here we study the effect of sparsity on the downstream zero-shot accuracy. Table 7 shows the overall accuracy on ImageNet using CLIP model with different levels of WordNet sparsi-ties .