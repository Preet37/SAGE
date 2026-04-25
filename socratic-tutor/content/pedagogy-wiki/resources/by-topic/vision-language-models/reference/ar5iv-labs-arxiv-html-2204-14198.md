# Source: https://ar5iv.labs.arxiv.org/html/2204.14198
# Author: Jean-Baptiste Alayrac et al.
# Title: Flamingo: a Visual Language Model for Few-Shot Learning (ar5iv HTML)
# Fetched via: trafilatura
# Date: 2026-04-09

\ul
Flamingo: a Visual Language Model
for Few-Shot Learning
Abstract
Building models that can be rapidly adapted to novel tasks using only a handful of annotated examples is an open challenge for multimodal machine learning research. We introduce Flamingo, a family of Visual Language Models (VLM) with this ability. We propose key architectural innovations to: (i) bridge powerful pretrained vision-only and language-only models, (ii) handle sequences of arbitrarily interleaved visual and textual data, and (iii) seamlessly ingest images or videos as inputs. Thanks to their flexibility, Flamingo models can be trained on large-scale multimodal web corpora containing arbitrarily interleaved text and images, which is key to endow them with in-context few-shot learning capabilities. We perform a thorough evaluation of our models, exploring and measuring their ability to rapidly adapt to a variety of image and video tasks. These include open-ended tasks such as visual question-answering, where the model is prompted with a question which it has to answer; captioning tasks, which evaluate the ability to describe a scene or an event; and close-ended tasks such as multiple-choice visual question-answering. For tasks lying anywhere on this spectrum, a single Flamingo model can achieve a new state of the art with few-shot learning, simply by prompting the model with task-specific examples. On numerous benchmarks, Flamingo outperforms models fine-tuned on thousands of times more task-specific data.
1 Introduction
One key aspect of intelligence is the ability to quickly learn to perform a new task given a short instruction [[33](#bib.bib33), [70](#bib.bib70)].
While initial progress has been made towards a similar capability in computer vision,
the most widely used paradigm still consists of first pretraining on a large amount of supervised data, before fine-tuning the model on the task of interest [[66](#bib.bib66), [118](#bib.bib118), [143](#bib.bib143)].
However, successful fine-tuning often requires many thousands of annotated data points.
In addition, it often requires careful per-task hyperparameter tuning and is also resource intensive.
Recently, multimodal vision-language models trained with a contrastive objective [[50](#bib.bib50), [85](#bib.bib85)] have enabled zero-shot adaptation to novel tasks, without the need for fine-tuning.
However, because these models simply provide a similarity score between a text and an image, they can only address limited use cases such as classification, where a finite set of outcomes is provided beforehand.
They crucially lack the ability to generate language, which makes them less suitable to more open-ended tasks such as captioning or visual question-answering.
Others have explored visually-conditioned language generation [[124](#bib.bib124), [114](#bib.bib114), [17](#bib.bib17), [119](#bib.bib119), [132](#bib.bib132)] but have not yet shown good performance in low-data regimes.
We introduce Flamingo, a Visual Language Model (VLM) that sets a new state of the art in few-shot learning on a wide range of open-ended vision and language tasks, simply by being prompted with a few input/output examples, as illustrated in Figure [1](#S0.F1).
Of the 16 tasks we consider, Flamingo also surpasses the fine-tuned state of the art on 6 tasks, despite using orders of magnitude less task-specific training data (see Figure [2](#S0.F2)).
To achieve this, Flamingo takes inspiration from recent work on large language models (LMs) which are good few-shot learners [[11](#bib.bib11), [86](#bib.bib86), [42](#bib.bib42), [18](#bib.bib18)].
A single large LM can
achieve strong performance on many tasks using only its text interface: a few examples of a task are provided to the model as a prompt, along with a query input, and the model generates a continuation to produce a predicted output for that query.
We show that the same can be done for image and video understanding tasks such as classification, captioning, or question-answering: these can be cast as text prediction problems with visual input conditioning.
The difference from a LM is that the model must be able to ingest a multimodal prompt containing images and/or videos interleaved with text.
Flamingo models have this capability—they are
visually-conditioned autoregressive text generation models able to ingest a sequence of text tokens interleaved with images and/or videos, and produce text as output.
Flamingo models leverage two complementary pre-trained and frozen models: a vision model which can “perceive” visual scenes and a large LM which performs a basic form of reasoning.
Novel architecture components are added in between these models to connect them in a way that preserves the knowledge they have accumulated during computationally intensive pre-training.
Flamingo models are also able to ingest high-resolution images or videos thanks to a Perceiver-based [[48](#bib.bib48)] architecture that can produce a small fixed number of visual tokens per image/video, given a large and variable number of visual input features.
A crucial aspect for the performance of large LMs is that they are trained on a large amount of text data. This training provides general-purpose generation capabilities that allows these LMs to perform well when prompted with task examples. Similarly, we demonstrate that the way we train the Flamingo models is crucial for their final performance. They are trained on a carefully chosen
mixture of complementary large-scale multimodal data coming only from the web, without using any data annotated for machine learning purposes. After this training, a Flamingo model can be directly adapted to vision tasks via simple few-shot learning without any task-specific tuning.
Contributions. In summary, our contributions are the following: (i) We introduce the Flamingo family of VLMs which can perform various multimodal tasks (such as captioning, visual dialogue, or visual question-answering) from only a few input/output examples. Thanks to architectural innovations, the Flamingo models can efficiently accept arbitrarily interleaved visual data and text as input and generate text in an open-ended manner. (ii) We quantitatively evaluate how Flamingo models can be adapted to various tasks via few-shot learning. We notably reserve a large set of held-out benchmarks which have not been used for validation of any design decisions or hyperparameters of the approach. We use these to estimate unbiased few-shot performance. (iii) Flamingo sets a new state of the art in few-shot learning on a wide array of 16 multimodal language and image/video understanding tasks. On 6 of these 16 tasks, Flamingo also outperforms the fine-tuned state of the art despite using only 32 task-specific examples, around 1000 times less task-specific training data than the current state of the art. With a larger annotation budget, Flamingo can also be effectively fine-tuned to set a new state of the art on five additional challenging benchmarks: VQAv2, VATEX, VizWiz, MSRVTTQA, and HatefulMemes.
2 Approach
This section describes Flamingo: a visual language model that accepts text interleaved with images/videos as input and outputs free-form text. The key architectural components shown in Figure [3](#S2.F3)
are chosen to leverage pretrained vision and language models and bridge them effectively.
First, the Perceiver Resampler (Section [2.1](#S2.SS1)) receives spatio-temporal features from the Vision Encoder (obtained from either an image or a video) and outputs a fixed number of visual tokens.
Second, these visual tokens are used to condition the frozen LM using freshly initialised cross-attention layers (Section [2.2](#S2.SS2)) that are interleaved between the pretrained LM layers.
These new layers offer an expressive way for the LM to incorporate visual information for the next-token prediction task. Flamingo models the likelihood of text conditioned on interleaved images and videos as follows:
| (1) |
where is the -th language token of the input text, is the set of preceding tokens, is the set of images/videos preceding token in the interleaved sequence and is parametrized by a Flamingo model.
The ability to handle interleaved text and visual sequences (Section [2.3](#S2.SS3)) makes it natural to use Flamingo models for in-context few-shot learning, analogously to GPT-3 with few-shot text prompting.
The model is trained on a diverse mixture of datasets as described in Section [2.4](#S2.SS4).
2.1 Visual processing and the Perceiver Resampler
Vision Encoder: from pixels to features.
Our vision encoder is a pretrained and frozen Normalizer-Free ResNet (NFNet) [[10](#bib.bib10)] – we use the F6 model.
We pretrain the vision encoder using a contrastive objective on our datasets of image and text pairs, using the two-term contrastive loss from Radford et al. [[85](#bib.bib85)].
We use the output of the final stage, a 2D spatial grid of features that is flattened to a 1D sequence.
For video inputs, frames are sampled at 1 FPS and encoded independently to obtain a 3D spatio-temporal grid of features to which learned temporal embeddings are added.
Features are then flattened to 1D before being fed to the Perceiver Resampler.
More details on the contrastive model training and performance are given in Appendix [B.1.3](#A2.SS1.SSS3) and Appendix [B.3.2](#A2.SS3.SSS2), respectively.
Perceiver Resampler: from varying-size large feature maps to few visual tokens.
This module connects the vision encoder to the frozen language model as shown in Figure [3](#S2.F3).
It takes as input a variable number of image or video features from the vision encoder and produces a fixed number of visual outputs (64),
reducing the computational complexity of the vision-text cross-attention.
Similar to Perceiver [[48](#bib.bib48)] and DETR [[13](#bib.bib13)], we learn a predefined number of latent input queries
which are fed to a Transformer and cross-attend to the visual features.
We show in our ablation studies (Section [3.3](#S3.SS3)) that using such a vision-language resampler module outperforms a plain Transformer and an MLP.
We provide an illustration, more architectural details, and pseudo-code in Appendix [A.1.1](#A1.SS1.SSS1).
2.2 Conditioning frozen language models on visual representations
Text generation is performed by a Transformer decoder, conditioned on the visual representations produced by the Perceiver Resampler. We interleave pretrained and frozen text-only LM blocks with blocks trained from scratch that cross-attend to the visual output from the Perceiver Resampler.
Interleaving new gated xattn-dense layers within a frozen pretrained LM.
We freeze the pretrained LM blocks, and insert gated cross-attention dense blocks (Figure [4](#S2.F4)) between the original layers, trained from scratch.
To ensure that at initialization, the conditioned model yields the same results as the original language model, we use a -gating mechanism [[41](#bib.bib41)].
This multiplies the output of a newly added layer by before adding it to the input representation from the residual connection, where is a layer-specific learnable scalar initialized to [[4](#bib.bib4)].
Thus, at initialization, the model output matches that of the pretrained LM, improving training stability and final performance.
In our ablation studies (Section [3.3](#S3.SS3)), we compare the proposed gated xattn-dense layers against recent alternatives [[22](#bib.bib22), [68](#bib.bib68)] and explore the effect of how frequently these additional layers are inserted to trade off between efficiency and expressivity.
See Appendix [A.1.2](#A1.SS1.SSS2) for more details.
Varying model sizes.
We perform experiments across three models sizes, building on the 1.4B, 7B, and 70B parameter Chinchilla models [[42](#bib.bib42)]; calling them respectively Flamingo-3B, Flamingo-9B and Flamingo-80B.
For brevity, we refer to the last as Flamingo throughout the paper.
While increasing the parameter count of the frozen LM and the trainable vision-text gated xattn-dense modules, we maintain a fixed-size frozen vision encoder and trainable Perceiver Resampler across the different models (small relative to the full model size).
See Appendix [B.1.1](#A2.SS1.SSS1) for further details.
2.3 Multi-visual input support: per-image/video attention masking
The image-causal modelling introduced in Equation ([1](#S2.E1)) is obtained by masking the full text-to-image cross-attention matrix,
limiting which visual tokens the model sees at each text token.
At a given text token, the model attends to the visual tokens of the image that appeared just before it in the interleaved sequence, rather than to all previous images (formalized and illustrated in Appendix [A.1.3](#A1.SS1.SSS3)).
Though the model only directly attends to a single image at a time, the dependency on all previous images remains via self-attention in the LM.
This single-image cross-attention scheme importantly allows the model to seamlessly generalise to any number of visual inputs, regardless of how many are used during training.
In particular, we use only up to 5 images per sequence when training on our interleaved datasets, yet our model is able to benefit from sequences of up to 32 pairs (or “shots”) of images/videos and corresponding texts during evaluation.
We show in Section [3.3](#S3.SS3) that this scheme is more effective than allowing the model to cross-attend to all previous images directly.
2.4 Training on a mixture of vision and language datasets
We train the Flamingo models on a mixture of three kinds of datasets, all scraped from the web: an interleaved image and text dataset derived from webpages, image-text pairs, and video-text pairs.
M3W: Interleaved image and text dataset.
The few-shot capabilities of Flamingo models rely on training on interleaved text and image data.
For this purpose, we collect the MultiModal MassiveWeb (M3W) dataset.
We extract both text and images from the HTML of approximately 43 million webpages, determining the positions of images relative to the text based on the relative positions of the text and image elements in the Document Object Model (DOM).
An example is then constructed by inserting <image> tags in plain text at the locations of the images on the page, and inserting a special <EOC> (end of chunk) token (added to the vocabulary and learnt) prior to any image and at the end of the document.
From each document, we sample a random subsequence of tokens and take up to the first images included in the sampled sequence.
Further images are discarded in order to save compute.
More details are provided in Appendix [A.3](#A1.SS3).
Pairs of image/video and text.
For our image and text pairs we first leverage the ALIGN [[50](#bib.bib50)] dataset, composed of 1.8 billion images paired with alt-text.
To complement this dataset, we collect our own dataset of image and text pairs targeting better quality and longer descriptions: LTIP (Long Text & Image Pairs) which consists of 312 million image and text pairs.
We also collect a similar dataset but with videos instead of still images: VTP (Video & Text Pairs) consists of 27 million short videos (approximately 22 seconds on average) paired with sentence descriptions.
We align the syntax of paired datasets with the syntax of M3W by prepending <image> and appending <EOC> to each training caption (see Appendix [A.3.3](#A1.SS3.SSS3) for details).
Multi-objective training and optimisation strategy. We train our models by minimizing a weighted sum of per-dataset expected negative log-likelihoods of text, given the visual inputs:
| (2) |
where and are the -th dataset and
its weighting, respectively.
Tuning the per-dataset weights is key to performance.
We accumulate gradients over all datasets, which we found outperforms a “round-robin” approach [[17](#bib.bib17)].
We provide further training details and ablations in Appendix [B.1.2](#A2.SS1.SSS2).
2.5 Task adaptation with few-shot in-context learning
Once Flamingo is trained, we use it to tackle a visual task by conditioning it on a multimodal interleaved prompt. We evaluate the ability of our models to rapidly adapt to new tasks using in-context learning, analogously to GPT-3 [[11](#bib.bib11)], by interleaving support example pairs in the form of or , followed by the query visual input, to build a prompt (details in Appendix [A.2](#A1.SS2)).
We perform open-ended evaluations using beam search for decoding, and close-ended evaluations using our model’s log-likelihood to score each possible answer.
We explore zero-shot generalization by prompting the model with two text-only examples from the task, with no corresponding images.
Evaluation hyperparameters and additional details are given in Appendix [B.1.5](#A2.SS1.SSS5).
3 Experiments
Our goal is to develop models that can rapidly adapt to diverse and challenging tasks.
For this, we consider a wide array of 16 popular multimodal image/video and language benchmarks.
In order to validate model design decisions during the course of the project, 5 of these benchmarks were used as part of our development (dev) set: COCO, OKVQA, VQAv2, MSVDQA and VATEX.
Performance estimates on the dev benchmarks may be biased, as a result of model selection.
We note that this is also the case for prior work which makes use of similar benchmarks to validate and ablate design decisions.
To account for this, we report performance on an additional set of 11 benchmarks,
spanning captioning, video question-answering, as well as some less commonly explored capabilities such as visual dialogue and multi-choice question-answering tasks.
The evaluation benchmarks are described in Appendix [B.1.4](#A2.SS1.SSS4).
We keep all evaluation hyperparameters fixed across all benchmarks.
Depending on the task, we use four few-shot prompt templates we describe in more detail in
Appendix [B.1.5](#A2.SS1.SSS5).
We emphasize that we do not validate any design decisions on these 11 benchmarks and use them solely to estimate unbiased few-shot learning performance of our models.
Concretely, estimating few-shot learning performance of
a model involves prompting it with a set of support samples and evaluating it on a set of query samples.
For the dev benchmarks that are used both to validate design decisions and hyperparameters, as well as to report final performance, we therefore use four subsets:
validation support, validation query, test support and test query.
For other benchmarks, we need only the latter two.
We report in Appendix [B.1.4](#A2.SS1.SSS4) how we form these subsets.
We report the results of the Flamingo models on few-shot learning in Section [3.1](#S3.SS1).
Section [3.2](#S3.SS2) gives Flamingo fine-tuned results.
An ablation study is given in Section [3.3](#S3.SS3).
Appendix [B.2](#A2.SS2) provides more results including Flamingo’s performance on the ImageNet and Kinetics700 classification tasks, and on our contrastive model’s performance.
Appendix [C](#A3) includes additional qualitative results.
3.1 Few-shot learning on vision-language tasks
| Method | FT | Shot |
OKVQA (I) |
VQAv2 (I) |
COCO (I) |
MSVDQA (V) |
VATEX (V) |
VizWiz (I) |
Flick30K (I) |
MSRVTTQA (V) |
iVQA (V) |
YouCook2 (V) |
STAR (V) |
VisDial (I) |
TextVQA (I) |
NextQA (I) |
HatefulMemes (I) |
RareAct (V) |
||||||||||||||||||||||||||||||||||||||||||||||||
|
✗ |
|
43.3 |
(16) |
|
38.2 |
(4) |
|
32.2 |
(0) |
|
35.2 |
(0) |
|
- | - | - |
19.2 |
(0) |
|
12.2 |
(0) |
|
- |
39.4 |
(0) |
|
11.6 |
(0) |
|
- | - |
66.1 |
(0) |
|
40.7 |
(0) |
|
||||||||||||||||||||||||||||
| Flamingo-3B | ✗ | 0 | 41.2 | 49.2 | 73.0 | 27.5 | 40.1 | 28.9 | 60.6 | 11.0 | 32.7 | 55.8 | 39.6 | 46.1 | 30.1 | 21.3 | 53.7 | 58.4 | ||||||||||||||||||||||||||||||||||||||||||||||||
| ✗ | 4 | 43.3 | 53.2 | 85.0 | 33.0 | 50.0 | 34.0 | 72.0 | 14.9 | 35.7 | 64.6 | 41.3 | 47.3 | 32.7 | 22.4 | 53.6 | - | |||||||||||||||||||||||||||||||||||||||||||||||||
| ✗ | 32 | 45.9 | 57.1 | 99.0 | 42.6 | 59.2 | 45.5 | 71.2 | 25.6 | 37.7 | 76.7 | 41.6 | 47.3 | 30.6 | 26.1 | 56.3 | - | |||||||||||||||||||||||||||||||||||||||||||||||||
| Flamingo-9B | ✗ | 0 | 44.7 | 51.8 | 79.4 | 30.2 | 39.5 | 28.8 | 61.5 | 13.7 | 35.2 | 55.0 | 41.8 | 48.0 | 31.8 | 23.0 | 57.0 | 57.9 | ||||||||||||||||||||||||||||||||||||||||||||||||
| ✗ | 4 | 49.3 | 56.3 | 93.1 | 36.2 | 51.7 | 34.9 | 72.6 | 18.2 | 37.7 | 70.8 | \ul42.8 | 50.4 | 33.6 | 24.7 | 62.7 | - | |||||||||||||||||||||||||||||||||||||||||||||||||
| ✗ | 32 | 51.0 | 60.4 | 106.3 | 47.2 | 57.4 | 44.0 | 72.8 | 29.4 | 40.7 | 77.3 | 41.2 | 50.4 | 32.6 | 28.4 | 63.5 | - | |||||||||||||||||||||||||||||||||||||||||||||||||
| Flamingo | ✗ | 0 | 50.6 | 56.3 | 84.3 | 35.6 | 46.7 | 31.6 | 67.2 | 17.4 | 40.7 | 60.1 | 39.7 | 52.0 | 35.0 | 26.7 | 46.4 | \ul60.8 | ||||||||||||||||||||||||||||||||||||||||||||||||
| ✗ | 4 | 57.4 | 63.1 | 103.2 | 41.7 | 56.0 | 39.6 | 75.1 | 23.9 | 44.1 | 74.5 | 42.4 | 55.6 | 36.5 | 30.8 | 68.6 | - | |||||||||||||||||||||||||||||||||||||||||||||||||
| ✗ | 32 | \ul57.8 | 67.6 | 113.8 | \ul52.3 | 65.1 | 49.8 | \ul75.4 | 31.0 | \ul45.3 | 86.8 | 42.2 | 55.6 | 37.9 | \ul33.5 | 70.0 | - | |||||||||||||||||||||||||||||||||||||||||||||||||
|
✔ |
|
(10K) |
|
(444K) |
|
(500K) |
|
(27K) |
|
(500K) |
|
(20K) |
|
(30K) |
|
(130K) |
|
(6K) |
|
(10K) |
|
(46K) |
|
(123K) |
|
(20K) |
|
(38K) |
|
(9K) |
|
- |
Few-shot results.
Results are given in Table [1](#S3.T1).
Flamingo outperforms by a large margin all previous zero-shot or few-shot methods on the 16 benchmarks considered.
This is achieved with as few as four examples per task, demonstrating practical and efficient adaptation of vision models to new tasks.
More importantly, Flamingo is often competitive with state-of-the-art methods additionally fine-tuned on up to hundreds of thousands of annotated examples.
On six tasks, Flamingo even outperforms the fine-tuned SotA despite using a single set of model weights and only 32 task-specific examples.
Finally, despite having only used the dev benchmarks for design decisions, our results generalize well to the other benchmarks, confirming the generality of our approach.
Scaling with respect to parameters and shots.
As shown in Figure [2](#S0.F2), the larger the model, the better the few-shot performance, similar to GPT-3 [[11](#bib.bib11)].
The performance also improves with the number of shots.
We further find that the largest model better exploits larger numbers of shots.
Interestingly, even though our Flamingo models were trained with sequences limited to only 5 images on M3W, they are still able to benefit from up to 32 images or videos during inference.
This demonstrates the flexibility of the Flamingo architecture for processing a variable number of videos or images.
3.2 Fine-tuning Flamingo as a pretrained vision-language model
While not the main focus of our work, we verify that when given more data, Flamingo models can be adapted to a task by fine-tuning their weights.
In Table [2](#S3.T2), we explore fine-tuning our largest model, Flamingo, for a given task with no limit on the annotation budget.
In short, we do so by fine-tuning the model on a short schedule with a small learning rate by additionally unfreezing the vision backbone to accommodate a higher input resolution (details in Appendix [B.2.2](#A2.SS2.SSS2)).
We find that we can improve results over our previously presented in-context few-shot learning results, setting a new state of the art on five additional tasks: VQAv2, VATEX, VizWiz, MSRVTTQA, and HatefulMemes.
| Method | VQAV2 | COCO | VATEX | VizWiz | MSRVTTQA | VisDial | YouCook2 | TextVQA | HatefulMemes | ||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| test-dev | test-std | test | test | test-dev | test-std | test | valid | test-std | valid | valid | test-std | test seen | |
| 32 shots | 67.6 | - | 113.8 | 65.1 | 49.8 | - | 31.0 | 56.8 | - | 86.8 | 36.0 | - | 70.0 |
| Fine-tuned | 82.0 | 82.1 | 138.1 | 84.2 | 65.7 | 65.4 | 47.4 | 61.8 | 59.7 | 118.6 | 57.1 | 54.1 | 86.6 |
| 81.3† | 81.3† | 149.6† | 81.4† | 57.2† | 60.6† | 46.8 | 75.2 | 75.4† | 138.7 | 54.7 | 73.7 | 84.6† | |
| SotA | [
|
[133](#bib.bib133)][119](#bib.bib119)][153](#bib.bib153)][65](#bib.bib65)][65](#bib.bib65)][51](#bib.bib51)][79](#bib.bib79)][123](#bib.bib123)][132](#bib.bib132)][137](#bib.bib137)][84](#bib.bib84)][152](#bib.bib152)]3.3 Ablation studies
| Ablated | Flamingo-3B | Changed | Param. | Step | COCO | OKVQA | VQAv2 | MSVDQA | VATEX | Overall | |
| setting | original value | value | count | time | CIDEr | top1 | top1 | top1 | CIDEr | score | |
| Flamingo-3B model | 3.2B | 1.74s | 86.5 | 42.1 | 55.8 | 36.3 | 53.4 | 70.7 | |||
| (i) | Training data | All data | w/o Video-Text pairs | 3.2B | 1.42s | 84.2 | 43.0 | 53.9 | 34.5 | 46.0 | 67.3 |
| w/o Image-Text pairs | 3.2B | 0.95s | 66.3 | 39.2 | 51.6 | 32.0 | 41.6 | 60.9 | |||
| Image-Text pairs LAION | 3.2B | 1.74s | 79.5 | 41.4 | 53.5 | 33.9 | 47.6 | 66.4 | |||
| w/o M3W | 3.2B | 1.02s | 54.1 | 36.5 | 52.7 | 31.4 | 23.5 | 53.4 | |||
| (ii) | Optimisation | Accumulation | Round Robin | 3.2B | 1.68s | 76.1 | 39.8 | 52.1 | 33.2 | 40.8 | 62.9 |
| (iii) | Tanh gating | ✓ | ✗ | 3.2B | 1.74s | 78.4 | 40.5 | 52.9 | 35.9 | 47.5 | 66.5 |
| (iv) | Cross-attention | gated xattn-dense | Vanilla xattn | 2.4B | 1.16s | 80.6 | 41.5 | 53.4 | 32.9 | 50.7 | 66.9 |
| architecture | Grafting | 3.3B | 1.74s | 79.2 | 36.1 | 50.8 | 32.2 | 47.8 | 63.1 | ||
| (v) | Cross-attention frequency | Every | Single in middle | 2.0B | 0.87s | 71.5 | 38.1 | 50.2 | 29.1 | 42.3 | 59.8 |
| Every 4th | 2.3B | 1.02s | 82.3 | 42.7 | 55.1 | 34.6 | 50.8 | 68.8 | |||
| Every 2nd | 2.6B | 1.24s | 83.7 | 41.0 | 55.8 | 34.5 | 49.7 | 68.2 | |||
| (vi) | Resampler | Perceiver | MLP | 3.2B | 1.85s | 78.6 | 42.2 | 54.7 | 35.2 | 44.7 | 66.6 |
| Transformer | 3.2B | 1.81s | 83.2 | 41.7 | 55.6 | 31.5 | 48.3 | 66.7 | |||
| (vii) | Vision encoder | NFNet-F6 | CLIP ViT-L/14 | 3.1B | 1.58s | 76.5 | 41.6 | 53.4 | 33.2 | 44.5 | 64.9 |
| NFNet-F0 | 2.9B | 1.45s | 73.8 | 40.5 | 52.8 | 31.1 | 42.9 | 62.7 | |||
| (viii) | Freezing LM | ✓ | ✗ (random init) | 3.2B | 2.42s | 74.8 | 31.5 | 45.6 | 26.9 | 50.1 | 57.8 |
| ✗ (pretrained) | 3.2B | 2.42s | 81.2 | 33.7 | 47.4 | 31.0 | 53.9 | 62.7 |
In Table [3](#S3.T3), we report our ablation results using Flamingo-3B on the validation subsets of the five dev benchmarks with 4 shots.
Note that we use smaller batch sizes and a shorter training schedule compared to the final models.
The Overall score is obtained by dividing each benchmark score by its state-of-the-art (SotA) performance from Table [1](#S3.T1) and averaging the results.
More details and results are given in Appendix [B.3](#A2.SS3) and Table [10](#A2.T10).
Importance of the training data mixture.
As shown in row (i), getting the right training data plays a crucial role.
In fact, removing the interleaved image-text dataset M3W leads to a decrease of more than in performance while removing the conventional paired image-text pairs also decreases performance (by ), demonstrating the need for different types of datasets.
Moreover, removing our paired video-text dataset negatively affects performance on all video tasks.
We ablate replacing our image-text pairs (ITP) by the publicly available LAION-400M dataset [[96](#bib.bib96)], which leads to a slight degradation in performance.
We show in row (ii) the importance of our gradient accumulation strategy compared to using round-robin updates [[17](#bib.bib17)].
Visual conditioning of the frozen LM.
We ablate the use of the 0-initialized tanh gating when merging the cross-attention output to the frozen LM output in row (iii).
Without it, we see a drop of in our overall score.
Moreover, we have noticed that disabling the 0-initialized tanh gating leads to training instabilities.
Next, we ablate different conditioning architectures in row (iv).
vanilla xattn, refers to the vanilla cross-attention from the original Transformer decoder [[115](#bib.bib115)].
In the grafting approach from [[68](#bib.bib68)], the frozen LM is used as is with no additional layers inserted, and a stack of interleaved self-attention and cross-attention layers that take the frozen LM output are learnt from scratch.
Overall, we show that our gated xattn-dense conditioning approach works best.
Compute/Memory vs. performance trade-offs. In row (v), we ablate the frequency at which we add new gated xattn-dense blocks. Although adding them at every layer is better, it significantly increases the number of trainable parameters and time complexity of the model. Notably, inserting them every fourth block accelerates training by while only decreasing the overall score by . In light of this trade-off, we maximize the number of added layers under hardware constraints and add a gated xattn-dense every fourth layer for Flamingo-9B and every seventh for Flamingo-80B. We further compare in row (vi) the Perceiver Resampler to a MLP and a vanilla Transformer given a parameter budget. Both underperform the Perceiver Resampler while also being slower.
Vision encoder.
In row (vii), we compare our NFNet-F6 vision encoder pretrained with contrastive learning (details in Appendix [B.1.3](#A2.SS1.SSS3)) to the publicly available CLIP ViT-L/14 [[85](#bib.bib85)] model trained at 224 resolution.
Our NFNet-F6 has a advantage over the CLIP ViT-L/14 and over a smaller NFNet-F0 encoder, which highlights the importance of using a strong vision backbone.
Freezing LM components prevents catastrophic forgetting. We verify the importance of freezing the LM layers at training in row (viii).
If trained from scratch, we observe a large performance decrease of .
Interestingly, fine-tuning our pretrained LM also leads to a drop in performance of .
This indicates an instance of “catastrophic forgetting” [[71](#bib.bib71)], in which the model progressively forgets its pretraining while training on a new objective. In our setting, freezing the language model is a better alternative to training with the pre-training dataset (MassiveText) in the mixture.
4 Related work
Language modelling and few-shot adaptation.
Language modelling has recently made substantial progress following the introduction of Transformers [[115](#bib.bib115)].
The paradigm of first pretraining on a vast amount of data followed by an adaptation on a downstream task has become standard [[75](#bib.bib75), [32](#bib.bib32), [52](#bib.bib52), [44](#bib.bib44), [23](#bib.bib23), [87](#bib.bib87), [108](#bib.bib108), [11](#bib.bib11)].
In this work, we build on the 70B Chinchilla language model [[42](#bib.bib42)] as the base LM for Flamingo.
Numerous works have explored techniques to adapt language models to novel tasks using a few examples.
These include adding small adapter modules [[43](#bib.bib43)], fine-tuning a small part of the LM [[141](#bib.bib141)], showing in-context examples in the prompt [[11](#bib.bib11)], or optimizing the prompt [[60](#bib.bib60), [56](#bib.bib56)] through gradient descent.
In this paper, we take inspiration from the in-context [[11](#bib.bib11)] few-shot learning technique instead of more involved few-shot learning approaches based on metric learning [[24](#bib.bib24), [117](#bib.bib117), [103](#bib.bib103), [112](#bib.bib112)] or meta-learning [[27](#bib.bib27), [7](#bib.bib7), [155](#bib.bib155), [91](#bib.bib91), [31](#bib.bib31), [6](#bib.bib6)].
When language meets vision.
These LM breakthroughs have been influential for vision-language modelling.
In particular, BERT [[23](#bib.bib23)] inspired a large body of vision-language work [[66](#bib.bib66), [106](#bib.bib106), [16](#bib.bib16), [38](#bib.bib38), [121](#bib.bib121), [61](#bib.bib61), [109](#bib.bib109), [151](#bib.bib151), [118](#bib.bib118), [59](#bib.bib59), [29](#bib.bib29), [28](#bib.bib28), [142](#bib.bib142), [143](#bib.bib143), [101](#bib.bib101), [107](#bib.bib107)].
We differ from these approaches as Flamingo models do not require fine-tuning on new tasks.
Another family of vision-language models is based on contrastive learning [[2](#bib.bib2), [85](#bib.bib85), [50](#bib.bib50), [146](#bib.bib146), [82](#bib.bib82), [74](#bib.bib74), [5](#bib.bib5), [140](#bib.bib140), [57](#bib.bib57), [138](#bib.bib138), [49](#bib.bib49)].
Flamingo differs from contrastive models as it can generate text,
although we build and rely upon them for our vision encoder.
Similar to our work are VLMs able to generate text in an autoregressive manner [[116](#bib.bib116), [25](#bib.bib25), [67](#bib.bib67), [45](#bib.bib45), [19](#bib.bib19)].
Concurrent works [[124](#bib.bib124), [17](#bib.bib17), [119](#bib.bib119), [154](#bib.bib154), [58](#bib.bib58)] also propose to formulate numerous vision tasks as text generation problems.
Building on top of powerful pretrained language models has been explored in several recent works.
One recent line of work [[114](#bib.bib114), [26](#bib.bib26), [78](#bib.bib78), [68](#bib.bib68), [136](#bib.bib136), [144](#bib.bib144)] proposes to freeze the pretrained LM weights to prevent catastrophic forgetting [[71](#bib.bib71)].
We follow this idea by freezing the Chinchilla LM layers [[42](#bib.bib42)] and adding learnable layers within the frozen LM.
We differ from prior work by introducing the first LM that can ingest arbitrarily interleaved images, videos, and text.
Web-scale vision and language training datasets.
Manually annotated vision and language datasets are costly to obtain and thus relatively small (10k-100k) in scale [[139](#bib.bib139), [15](#bib.bib15), [3](#bib.bib3), [69](#bib.bib69), [122](#bib.bib122), [129](#bib.bib129)].
To alleviate this lack of data, numerous works [[50](#bib.bib50), [98](#bib.bib98), [14](#bib.bib14), [110](#bib.bib110)] automatically scrape readily available paired vision-text data.
In addition to such paired data, we show the importance of also training on entire multimodal webpages containing interleaved images and text as a single sequence.
Concurrent work CM3 [[1](#bib.bib1)] proposes to generate HTML markup from pages, while we simplify the text prediction task by only generating plain text.
We emphasize few-shot learning and vision tasks while CM3 [[1](#bib.bib1)] primarily evaluates on language-only benchmarks in a zero-shot or fine-tuned setup.
5 Discussion
Limitations. First, our models build on pretrained LMs, and as a side effect, directly inherit their weaknesses. For example, LM priors are generally helpful, but may play a role in occasional hallucinations and ungrounded guesses. Furthermore, LMs generalise poorly to sequences longer than the training ones. They also suffer from poor sample efficiency during training. Addressing these issues can accelerate progress in the field and enhance the abilities of VLMs like Flamingo.
Second, the classification performance of Flamingo lags behind that of state-of-the-art contrastive models [[85](#bib.bib85), [82](#bib.bib82)].
These models directly optimize for text-image retrieval, of which classification is a special case.
In contrast, our models handle a wider range of tasks, such as open-ended ones.
A unified approach to achieve the best of both worlds is an important research direction.
Third, in-context learning has significant advantages over gradient-based few-shot learning methods, but also suffers from drawbacks depending on the characteristics of the application at hand.
We demonstrate the effectiveness of in-context learning when access is limited to only a few dozen examples.
In-context learning also enables simple deployment, requiring only inference,
generally with no hyperparameter tuning needed.
However, in-context learning is known to be highly sensitive to various aspects of the demonstrations [[148](#bib.bib148), [80](#bib.bib80)],
and its inference compute cost and absolute performance scale poorly with the number of shots beyond this low-data regime.
There may be opportunities to combine few-shot learning methods to leverage their complementary benefits.
We discuss the limitations of our work in more depth in Appendix [D.1](#A4.SS1).
Societal impacts.
In terms of societal impacts, Flamingo offers a number of benefits while carrying some risks.
Its ability to rapidly adapt to a broad range of tasks have the potential to enable non-expert users to obtain
good
performance in data-starved regimes, lowering the barriers to both beneficial and malicious applications.
Flamingo is exposed to the same risks as large language models, such as outputting offensive language, propagating social biases and stereotypes, as well as leaking private information [[126](#bib.bib126), [42](#bib.bib42)].
Its ability to additionally handle visual inputs poses specific risks such as gender and racial biases relating to the contents of the input images, similar to a number of visual recognition systems [[37](#bib.bib37), [147](#bib.bib147), [12](#bib.bib12), [21](#bib.bib21), [97](#bib.bib97)].
We refer the reader to Appendix [D.2](#A4.SS2) for a more extensive discussion of the societal impacts of our work, both positive and negative;
as well as mitigation strategies and early investigations of risks relating to racial or gender bias and toxic outputs.
Finally we note that, following prior work focusing on language models [[111](#bib.bib111), [81](#bib.bib81), [72](#bib.bib72)],
the few-shot capabilities of Flamingo could be useful for mitigating such risks.
Conclusion. We proposed Flamingo, a general-purpose family of models that can be applied to image and video tasks with minimal task-specific training data. We also qualitatively explored interactive abilities of Flamingo such as “chatting” with the model, demonstrating flexibility beyond traditional vision benchmarks. Our results suggest that connecting pre-trained large language models with powerful visual models is an important step towards general-purpose visual understanding.
Acknowledgments and Disclosure of Funding.
This research was funded by DeepMind. We would like to thank many colleagues for useful discussions, suggestions, feedback, and advice, including: Samuel Albanie, Relja Arandjelović, Kareem Ayoub, Lorrayne Bennett, Adria Recasens Continente, Tom Eccles, Nando de Freitas, Sander Dieleman, Conor Durkan, Aleksa Gordić, Raia Hadsell, Will Hawkins, Lisa Anne Hendricks, Felix Hill, Jordan Hoffmann, Geoffrey Irving, Drew Jaegle, Koray Kavukcuoglu, Agustin Dal Lago, Mateusz Malinowski, Soňa Mokrá, Gaby Pearl, Toby Pohlen, Jack Rae, Laurent Sifre, Francis Song, Maria Tsimpoukelli, Gregory Wayne, and Boxi Wu.
References
- Aghajanyan et al. [2022] Armen Aghajanyan, Bernie Huang, Candace Ross, Vladimir Karpukhin, Hu Xu, Naman Goyal, Dmytro Okhonko, Mandar Joshi, Gargi Ghosh, Mike Lewis, and Luke Zettlemoyer. CM3: A causal masked multimodal model of the internet. arXiv:2201.07520, 2022.
- Alayrac et al. [2020] Jean-Baptiste Alayrac, Adria Recasens, Rosalia Schneider, Relja Arandjelović, Jason Ramapuram, Jeffrey De Fauw, Lucas Smaira, Sander Dieleman, and Andrew Zisserman. Self-supervised multimodal versatile networks. Conference on Neural Information Processing Systems, 2020.
- Antol et al. [2015] Stanislaw Antol, Aishwarya Agrawal, Jiasen Lu, Margaret Mitchell, Dhruv Batra, C. Lawrence Zitnick, and Devi Parikh. VQA: Visual question answering. In International Conference on Computer Vision, 2015.
- Bachlechner et al. [2021] Thomas Bachlechner, Bodhisattwa Prasad Majumder, Henry Mao, Gary Cottrell, and Julian McAuley. ReZero is all you need: Fast convergence at large depth. In Uncertainty in Artificial Intelligence, 2021.
- Bain et al. [2021] Max Bain, Arsha Nagrani, Gül Varol, and Andrew Zisserman. Frozen in time: A joint video and image encoder for end-to-end retrieval. In International Conference on Computer Vision, 2021.
- Bertinetto et al. [2016] Luca Bertinetto, João F. Henriques, Jack Valmadre, Philip Torr, and Andrea Vedaldi. Learning feed-forward one-shot learners. Conference on Neural Information Processing Systems, 2016.
- Bertinetto et al. [2018] Luca Bertinetto, Joao F. Henriques, Philip H. S. Torr, and Andrea Vedaldi. Meta-learning with differentiable closed-form solvers. arXiv:1805.08136, 2018.
-
Bradbury et al. [2018]
James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary,
Dougal Maclaurin, George Necula, Adam Paszke, Jake VanderPlas, Skye
Wanderman-Milne, and Qiao Zhang.
JAX: composable transformations of Python+NumPy programs,
2018.
URL
[http://github.com/google/jax](http://github.com/google/jax). - Bridle [1990] John S. Bridle. Probabilistic interpretation of feedforward classification network outputs, with relationships to statistical pattern recognition. In Neurocomputing, 1990.
- Brock et al. [2021] Andrew Brock, Soham De, Samuel L. Smith, and Karen Simonyan. High-performance large-scale image recognition without normalization. arXiv:2102.06171, 2021.
- Brown et al. [2020] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners. In Conference on Neural Information Processing Systems, 2020.
- Buolamwini and Gebru [2018] Joy Buolamwini and Timnit Gebru. Gender shades: Intersectional accuracy disparities in commercial gender classification. In ACM Conference on Fairness, Accountability, and Transparency, 2018.
- Carion et al. [2020] Nicolas Carion, Francisco Massa, Gabriel Synnaeve, Nicolas Usunier, Alexander Kirillov, and Sergey Zagoruyko. End-to-end object detection with transformers. In European Conference on Computer Vision, 2020.
- Changpinyo et al. [2021] Soravit Changpinyo, Piyush Sharma, Nan Ding, and Radu Soricut. Conceptual 12M: Pushing web-scale image-text pre-training to recognize long-tail visual concepts. In IEEE Computer Vision and Pattern Recognition, 2021.
- Chen et al. [2015] Xinlei Chen, Hao Fang, Tsung-Yi Lin, Ramakrishna Vedantam, Saurabh Gupta, Piotr Dollár, and C Lawrence Zitnick. Microsoft COCO captions: Data collection and evaluation server. arXiv:1504.00325, 2015.
- Chen et al. [2020] Yen-Chun Chen, Linjie Li, Licheng Yu, Ahmed El Kholy, Faisal Ahmed, Zhe Gan, Yu Cheng, and Jingjing Liu. UNITER: Universal image-text representation learning. In European Conference on Computer Vision, 2020.
- Cho et al. [2021] Jaemin Cho, Jie Lei, Hao Tan, and Mohit Bansal. Unifying vision-and-language tasks via text generation. In International Conference on Machine Learning, 2021.
- Chowdhery et al. [2022] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel. PaLM: Scaling language modeling with pathways. arXiv:2204.02311, 2022.
- Dai et al. [2022] Wenliang Dai, Lu Hou, Lifeng Shang, Xin Jiang, Qun Liu, and Pascale Fung. Enabling multimodal generation on clip via vision-language knowledge distillation. In ACL Findings, 2022.
- Das et al. [2017] Abhishek Das, Satwik Kottur, Khushi Gupta, Avi Singh, Deshraj Yadav, José MF Moura, Devi Parikh, and Dhruv Batra. Visual dialog. In IEEE Computer Vision and Pattern Recognition, 2017.
- De Vries et al. [2019] Terrance De Vries, Ishan Misra, Changhan Wang, and Laurens Van der Maaten. Does object recognition work for everyone? In IEEE Computer Vision and Pattern Recognition, 2019.
- Desai and Johnson [2021] Karan Desai and Justin Johnson. VirTex: Learning visual representations from textual annotations. In IEEE Computer Vision and Pattern Recognition, 2021.
- Devlin et al. [2018] Jacob Devlin, Ming-Wei Chang, Kenton Lee, and Kristina Toutanova. BERT: Pre-training of deep bidirectional transformers for language understanding. arXiv:1810.04805, 2018.
- Doersch et al. [2020] Carl Doersch, Ankush Gupta, and Andrew Zisserman. CrossTransformers: spatially-aware few-shot transfer. Conference on Neural Information Processing Systems, 2020.
- Donahue et al. [2015] Jeffrey Donahue, Lisa Anne Hendricks, Sergio Guadarrama, Marcus Rohrbach, Subhashini Venugopalan, Kate Saenko, and Trevor Darrell. Long-term recurrent convolutional networks for visual recognition and description. In IEEE Computer Vision and Pattern Recognition, 2015.
- Eichenberg et al. [2021] Constantin Eichenberg, Sidney Black, Samuel Weinbach, Letitia Parcalabescu, and Anette Frank. MAGMA–multimodal augmentation of generative models through adapter-based finetuning. arXiv:2112.05253, 2021.
- Finn et al. [2017] Chelsea Finn, Pieter Abbeel, and Sergey Levine. Model-agnostic meta-learning for fast adaptation of deep networks. In International Conference on Machine Learning, 2017.
- Fu et al. [2021] Tsu-Jui Fu, Linjie Li, Zhe Gan, Kevin Lin, William Yang Wang, Lijuan Wang, and Zicheng Liu. VIOLET: End-to-end video-language transformers with masked visual-token modeling. arXiv:2111.12681, 2021.
- Gan et al. [2020] Zhe Gan, Yen-Chun Chen, Linjie Li, Chen Zhu, Yu Cheng, and Jingjing Liu. Large-scale adversarial training for vision-and-language representation learning. In Conference on Neural Information Processing Systems, 2020.
- Gebru et al. [2021] Timnit Gebru, Jamie Morgenstern, Briana Vecchione, Jennifer Wortman Vaughan, Hanna Wallach, Hal Daumé III, and Kate Crawford. Datasheets for datasets. Communications of the ACM, 2021.
- Gordon et al. [2018] Jonathan Gordon, John Bronskill, Matthias Bauer, Sebastian Nowozin, and Richard E. Turner. Meta-learning probabilistic inference for prediction. arXiv:1805.09921, 2018.
- Graves [2013] Alex Graves. Generating sequences with recurrent neural networks. arXiv:1308.0850, 2013.
- Griffiths et al. [2019] Thomas L. Griffiths, Frederick Callaway, Michael B. Chang, Erin Grant, Paul M. Krueger, and Falk Lieder. Doing more with less: meta-reasoning and meta-learning in humans and machines. Current Opinion in Behavioral Sciences, 2019.
- Gui et al. [2021] Liangke Gui, Borui Wang, Qiuyuan Huang, Alex Hauptmann, Yonatan Bisk, and Jianfeng Gao. KAT: A knowledge augmented transformer for vision-and-language. arXiv:2112.08614, 2021.
- Gurari et al. [2018] Danna Gurari, Qing Li, Abigale J. Stangl, Anhong Guo, Chi Lin, Kristen Grauman, Jiebo Luo, and Jeffrey P. Bigham. VizWiz grand challenge: Answering visual questions from blind people. In IEEE Computer Vision and Pattern Recognition, 2018.
- Haviv et al. [2022] Adi Haviv, Ori Ram, Ofir Press, Peter Izsak, and Omer Levy. Transformer language models without positional encodings still learn positional information. arXiv:2203.16634, 2022.
- Hendricks et al. [2018] Lisa Anne Hendricks, Kaylee Burns, Kate Saenko, Trevor Darrell, and Anna Rohrbach. Women also snowboard: Overcoming bias in captioning models. In European Conference on Computer Vision, 2018.
- Hendricks et al. [2021] Lisa Anne Hendricks, John Mellor, Rosalia Schneider, Jean-Baptiste Alayrac, and Aida Nematzadeh. Decoupling the role of data, attention, and losses in multimodal transformers. Annual Meeting of the Association for Computational Linguistics, 2021.
- Hendrycks and Gimpel [2016] Dan Hendrycks and Kevin Gimpel. Gaussian error linear units (GELUs). arXiv:1606.08415, 2016.
-
Hennigan et al. [2020]
Tom Hennigan, Trevor Cai, Tamara Norman, and Igor Babuschkin.
Haiku: Sonnet for JAX, 2020.
URL
[http://github.com/deepmind/dm-haiku](http://github.com/deepmind/dm-haiku). - Hochreiter and Schmidhuber [1997] Sepp Hochreiter and Jürgen Schmidhuber. Long short-term memory. Neural Computation, 1997.
- Hoffmann et al. [2022] Jordan Hoffmann, Sebastian Borgeaud, Arthur Mensch, Elena Buchatskaya, Trevor Cai, Eliza Rutherford, Diego de Las Casas, Lisa Anne Hendricks, Johannes Welbl, Aidan Clark, Eric Noland Tom Hennigan, Katie Millican, George van den Driessche, Bogdan Damoc, Aurelia Guy, Simon Osindero, Karen Simonyan, Erich Elsen, Jack W. Rae, Oriol Vinyals, and Laurent Sifre. Training compute-optimal large language models. arXiv:2203.15556, 2022.
- Houlsby et al. [2019] Neil Houlsby, Andrei Giurgiu, Stanislaw Jastrzebski, Bruna Morrone, Quentin De Laroussilhe, Andrea Gesmundo, Mona Attariyan, and Sylvain Gelly. Parameter-efficient transfer learning for NLP. In International Conference on Machine Learning, 2019.
- Howard and Ruder [2018] Jeremy Howard and Sebastian Ruder. Universal language model fine-tuning for text classification. arXiv:1801.06146, 2018.
- Hu et al. [2021] Xiaowei Hu, Zhe Gan, Jianfeng Wang, Zhengyuan Yang, Zicheng Liu, Yumao Lu, and Lijuan Wang. Scaling up vision-language pre-training for image captioning. arXiv:2111.12233, 2021.
- Huang et al. [2019] Lun Huang, Wenmin Wang, Jie Chen, and Xiao-Yong Wei. Attention on attention for image captioning. In International Conference on Computer Vision, 2019.
- Islam et al. [2021] Md Amirul Islam, Matthew Kowal, Sen Jia, Konstantinos G. Derpanis, and Neil D. B. Bruce. Global pooling, more than meets the eye: Position information is encoded channel-wise in CNNs. In International Conference on Computer Vision, 2021.
- Jaegle et al. [2021] Andrew Jaegle, Felix Gimeno, Andy Brock, Oriol Vinyals, Andrew Zisserman, and Joao Carreira. Perceiver: General perception with iterative attention. In International Conference on Machine Learning, 2021.
- Jain et al. [2021] Aashi Jain, Mandy Guo, Krishna Srinivasan, Ting Chen, Sneha Kudugunta, Chao Jia, Yinfei Yang, and Jason Baldridge. MURAL: multimodal, multitask retrieval across languages. arXiv:2109.05125, 2021.
- Jia et al. [2021] Chao Jia, Yinfei Yang, Ye Xia, Yi-Ting Chen, Zarana Parekh, Hieu Pham, Quoc V. Le, Yun-Hsuan Sung, Zhen Li, and Tom Duerig. Scaling up visual and vision-language representation learning with noisy text supervision. arXiv:2102.05918, 2021.
- Jinpeng Wang et al. [2022] Alex Jinpeng Wang, Yixiao Ge, Rui Yan, Yuying Ge, Xudong Lin, Guanyu Cai, Jianping Wu, Ying Shan, Xiaohu Qie, and Mike Zheng Shou. All in one: Exploring unified video-language pre-training. arXiv:2203.07303, 2022.
- Jozefowicz et al. [2016] Rafal Jozefowicz, Oriol Vinyals, Mike Schuster, Noam Shazeer, and Yonghui Wu. Exploring the limits of language modeling. arXiv:1602.02410, 2016.
- Kaplan et al. [2020] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. arXiv:2001.08361, 2020.
- Kiela et al. [2020] Douwe Kiela, Hamed Firooz, Aravind Mohan, Vedanuj Goswami, Amanpreet Singh, Pratik Ringshia, and Davide Testuggine. The Hateful Memes Challenge: Detecting hate speech in multimodal memes. Conference on Neural Information Processing Systems, 2020.
-
Larochelle [2021]
Hugo Larochelle.
Few-shot classification by recycling deep learning.
Invited Talk at the S2D-OLAD Workshop, ICLR 2021, 2021.
URL
[https://slideslive.com/38955350/fewshot-classification-by-recycling-deep-learning](https://slideslive.com/38955350/fewshot-classification-by-recycling-deep-learning). - Lester et al. [2021] Brian Lester, Rami Al-Rfou, and Noah Constant. The power of scale for parameter-efficient prompt tuning. arXiv:2104.08691, 2021.
- Li et al. [2021] Junnan Li, Ramprasaath Selvaraju, Akhilesh Gotmare, Shafiq Joty, Caiming Xiong, and Steven Chu Hong Hoi. Align before fuse: Vision and language representation learning with momentum distillation. In Conference on Neural Information Processing Systems, 2021.
- Li et al. [2022] Junnan Li, Dongxu Li, Caiming Xiong, and Steven Hoi. BLIP: Bootstrapping language-image pre-training for unified vision-language understanding and generation. arXiv:2201.12086, 2022.
- Li et al. [2020a] Linjie Li, Yen-Chun Chen, Yu Cheng, Zhe Gan, Licheng Yu, and Jingjing Liu. HERO: Hierarchical encoder for video+language omni-representation pre-training. arXiv:2005.00200, 2020a.
- Li and Liang [2021] Xiang Lisa Li and Percy Liang. Prefix-tuning: Optimizing continuous prompts for generation. arXiv:2101.00190, 2021.
- Li et al. [2020b] Xiujun Li, Xi Yin, Chunyuan Li, Pengchuan Zhang, Xiaowei Hu, Lei Zhang, Lijuan Wang, Houdong Hu, Li Dong, Furu Wei, Yejin Choi, and Jianfeng Gao. Oscar: Object-semantics aligned pre-training for vision-language tasks. In European Conference on Computer Vision, 2020b.
- Lippe et al. [2020] Phillip Lippe, Nithin Holla, Shantanu Chandra, Santhosh Rajamanickam, Georgios Antoniou, Ekaterina Shutova, and Helen Yannakoudakis. A multimodal framework for the detection of hateful memes. arXiv:2012.12871, 2020.
- Liu et al. [2021a] Jiachang Liu, Dinghan Shen, Yizhe Zhang, Bill Dolan, Lawrence Carin, and Weizhu Chen. What makes good in-context examples for GPT-3? arXiv:2101.06804, 2021a.
- Liu et al. [2017] Siqi Liu, Zhenhai Zhu, Ning Ye, Sergio Guadarrama, and Kevin Murphy. Optimization of image description metrics using policy gradient methods. In International Conference on Computer Vision, 2017.
- Liu et al. [2021b] Yu Liu, Lianghua Huang, Liuyihang Song, Bin Wang, Yingya Zhang, and Pan Pan. Enhancing textual cues in multi-modal transformers for VQA. VizWiz Challenge 2021, 2021b.
- Lu et al. [2019] Jiasen Lu, Dhruv Batra, Devi Parikh, and Stefan Lee. ViLBERT: Pretraining task-agnostic visiolinguistic representations for vision-and-language tasks. Conference on Neural Information Processing Systems, 2019.
- Luo et al. [2020] Huaishao Luo, Lei Ji, Botian Shi, Haoyang Huang, Nan Duan, Tianrui Li, Jason Li, Taroon Bharti, and Ming Zhou. UniVL: A unified video and language pre-training model for multimodal understanding and generation. arXiv:2002.06353, 2020.
- Luo et al. [2022] Ziyang Luo, Yadong Xi, Rongsheng Zhang, and Jing Ma. VC-GPT: Visual conditioned GPT for end-to-end generative vision-and-language pre-training. arXiv:2201.12723, 2022.
- Marino et al. [2019] Kenneth Marino, Mohammad Rastegari, Ali Farhadi, and Roozbeh Mottaghi. OK-VQA: A visual question answering benchmark requiring external knowledge. In IEEE Computer Vision and Pattern Recognition, 2019.
- Markman [1989] Ellen M. Markman. Categorization and naming in children: Problems of induction. MIT Press, 1989.
- McCloskey and Cohen [1989] Michael McCloskey and Neil J. Cohen. Catastrophic interference in connectionist networks: The sequential learning problem. The Psychology of Learning and Motivation, 1989.
- Menick et al. [2022] Jacob Menick, Maja Trebacz, Vladimir Mikulik, John Aslanides, Francis Song, Martin Chadwick, Mia Glaese, Susannah Young, Lucy Campbell-Gillingham, Geoffrey Irving, and Nat McAleese. Teaching language models to support answers with verified quotes. arXiv:2203.11147, 2022.
- Miech et al. [2020a] Antoine Miech, Jean-Baptiste Alayrac, Ivan Laptev, Josef Sivic, and Andrew Zisserman. RareAct: A video dataset of unusual interactions. arxiv:2008.01018, 2020a.
- Miech et al. [2020b] Antoine Miech, Jean-Baptiste Alayrac, Lucas Smaira, Ivan Laptev, Josef Sivic, and Andrew Zisserman. End-to-end learning of visual representations from uncurated instructional videos. In IEEE Computer Vision and Pattern Recognition, 2020b.
- Mikolov et al. [2010] Tomas Mikolov, Martin Karafiát, Lukas Burget, Jan Cernockỳ, and Sanjeev Khudanpur. Recurrent neural network based language model. Interspeech, 2010.
- Min et al. [2022] Sewon Min, Xinxi Lyu, Ari Holtzman, Mikel Artetxe, Mike Lewis, Hannaneh Hajishirzi, and Luke Zettlemoyer. Rethinking the role of demonstrations: What makes in-context learning work? arXiv:2202.12837, 2022.
- Mitchell et al. [2019] Margaret Mitchell, Simone Wu, Andrew Zaldivar, Parker Barnes, Lucy Vasserman, Ben Hutchinson, Elena Spitzer, Inioluwa Deborah Raji, and Timnit Gebru. Model cards for model reporting. In ACM Conference on Fairness, Accountability, and Transparency, 2019.
- Mokady et al. [2021] Ron Mokady, Amir Hertz, and Amit H. Bermano. ClipCap: CLIP prefix for image captioning. arXiv:2111.09734, 2021.
- Murahari et al. [2020] Vishvak Murahari, Dhruv Batra, Devi Parikh, and Abhishek Das. Large-scale pretraining for visual dialog: A simple state-of-the-art baseline. In European Conference on Computer Vision, 2020.
- Perez et al. [2021] Ethan Perez, Douwe Kiela, and Kyunghyun Cho. True few-shot learning with language models. Conference on Neural Information Processing Systems, 2021.
- Perez et al. [2022] Ethan Perez, Saffron Huang, Francis Song, Trevor Cai, Roman Ring, John Aslanides, Amelia Glaese, Nat McAleese, and Geoffrey Irving. Red teaming language models with language models. arXiv:2202.03286, 2022.
- Pham et al. [2021] Hieu Pham, Zihang Dai, Golnaz Ghiasi, Hanxiao Liu, Adams Wei Yu, Minh-Thang Luong, Mingxing Tan, and Quoc V. Le. Combined scaling for zero-shot transfer learning. arXiv:2111.10050, 2021.
- Press et al. [2022] Ofir Press, Noah Smith, and Mike Lewis. Train short, test long: Attention with linear biases enables input length extrapolation. In International Conference on Learning Representations, 2022.
- Qiao et al. [2021] Yixuan Qiao, Hao Chen, Jun Wang, Yihao Chen, Xianbin Ye, Ziliang Li, Xianbiao Qi, Peng Gao, and Guotong Xie. Winner team Mia at TextVQA Challenge 2021: Vision-and-language representation learning with pre-trained sequence-to-sequence model. arXiv:2106.15332, 2021.
- Radford et al. [2021] Alec Radford, Jong Wook Kim, Chris Hallacy, Aditya Ramesh, Gabriel Goh, Sandhini Agarwal, Girish Sastry, Amanda Askell, Pamela Mishkin, Jack Clark, Gretchen Krueger, and Ilya Sutskever. Learning transferable visual models from natural language supervision. arXiv:2103.00020, 2021.
- Rae et al. [2021] Jack W. Rae, Sebastian Borgeaud, Trevor Cai, Katie Millican, Jordan Hoffmann, Francis Song, John Aslanides, Sarah Henderson, Roman Ring, Susannah Young, Eliza Rutherford, Tom Hennigan, Jacob Menick, Albin Cassirer, Richard Powell, George van den Driessche, Lisa Anne Hendricks, Maribeth Rauh, Po-Sen Huang, Amelia Glaese, Johannes Welbl, Sumanth Dathathri, Saffron Huang, Jonathan Uesato, John Mellor, Irina Higgins, Antonia Creswell, Nat McAleese, Amy Wu, Erich Elsen, Siddhant Jayakumar, Elena Buchatskaya, David Budden, Esme Sutherland, Karen Simonyan, Michela Paganini, Laurent Sifre, Lena Martens, Xiang Lorraine Li, Adhiguna Kuncoro, Aida Nematzadeh, Elena Gribovskaya, Domenic Donato, Angeliki Lazaridou, Arthur Mensch, Jean-Baptiste Lespiau, Maria Tsimpoukelli, Nikolai Grigorev, Doug Fritz, Thibault Sottiaux, Mantas Pajarskas, Toby Pohlen, Zhitao Gong, Daniel Toyama, Cyprien de Masson d’Autume, Yujia Li, Tayfun Terzi, Vladimir Mikulik, Igor Babuschkin, Aidan Clark, Diego de Las Casas, Aurelia Guy, Chris Jones, James Bradbury, Matthew Johnson, Blake Hechtman, Laura Weidinger, Iason Gabriel, William Isaac, Ed Lockhart, Simon Osindero, Laura Rimell, Chris Dyer, Oriol Vinyals, Kareem Ayoub, Jeff Stanway, Lorrayne Bennett, Demis Hassabis, Koray Kavukcuoglu, and Geoffrey Irving. Scaling language models: Methods, analysis & insights from training Gopher. arXiv:2112.11446, 2021.
- Raffel et al. [2019] Colin Raffel, Noam Shazeer, Adam Roberts, Katherine Lee, Sharan Narang, Michael Matena, Yanqi Zhou, Wei Li, and Peter J. Liu. Exploring the limits of transfer learning with a unified text-to-text transformer. arXiv:1910.10683, 2019.
- Rajbhandari et al. [2020] Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. ZeRO: Memory optimizations toward training trillion parameter models. In International Conference for High Performance Computing, Networking, Storage and Analysis, 2020.
- Ramesh et al. [2022] Aditya Ramesh, Prafulla Dhariwal, Alex Nichol, Casey Chu, and Mark Chen. Hierarchical text-conditional image generation with clip latents. arXiv:2204.06125, 2022.
- Rennie et al. [2017] Steven J. Rennie, Etienne Marcheret, Youssef Mroueh, Jarret Ross, and Vaibhava Goel. Self-critical sequence training for image captioning. In IEEE Computer Vision and Pattern Recognition, 2017.
- Requeima et al. [2019] James Requeima, Jonathan Gordon, John Bronskill, Sebastian Nowozin, and Richard E. Turner. Fast and flexible multi-task classification using conditional neural adaptive processes. Conference on Neural Information Processing Systems, 2019.
- Reynolds and McDonell [2021] Laria Reynolds and Kyle McDonell. Prompt programming for large language models: Beyond the few-shot paradigm. In Extended Abstracts of the 2021 CHI Conference on Human Factors in Computing Systems, 2021.
- Rudinger et al. [2018] Rachel Rudinger, Jason Naradowsky, Brian Leonard, and Benjamin Van Durme. Gender bias in coreference resolution. arXiv:1804.09301, 2018.
- Russakovsky et al. [2015] Olga Russakovsky, Jia Deng, Hao Su, Jonathan Krause, Sanjeev Satheesh, Sean Ma, Zhiheng Huang, Andrej Karpathy, Aditya Khosla, Michael Bernstein, Alexander C. Berg, and Li Fei-Fei. ImageNet large scale visual recognition challenge. International Journal of Computer Vision, 2015.
- Sanh et al. [2022] Victor Sanh, Albert Webson, Colin Raffel, Stephen H. Bach, Lintang Sutawika, Zaid Alyafeai, Antoine Chaffin, Arnaud Stiegler, Teven Le Scao, Arun Raja, Manan Dey, M. Saiful Bari, Canwen Xu, Urmish Thakker, Shanya Sharma Sharma, Eliza Szczechla, Taewoon Kim, Gunjan Chhablani, Nihal Nayak, Debajyoti Datta, Jonathan Chang, Mike Tian-Jian Jiang, Han Wang, Matteo Manica, Sheng Shen, Zheng Xin Yong, Harshit Pandey, Rachel Bawden, Thomas Wang, Trishala Neeraj, Jos Rozen, Abheesht Sharma, Andrea Santilli, Thibault Fevry, Jason Alan Fries, Ryan Teehan, Stella Biderman, Leo Gao, Tali Bers, Thomas Wolf, and Alexander M. Rush. Multitask Prompted Training Enables Zero-Shot Task Generalization. In International Conference on Learning Representations, 2022.
- Schuhmann et al. [2021] Christoph Schuhmann, Richard Vencu, Romain Beaumont, Robert Kaczmarczyk, Clayton Mullis, Aarush Katta, Theo Coombes, Jenia Jitsev, and Aran Komatsuzaki. Laion-400m: Open dataset of clip-filtered 400 million image-text pairs. arXiv:2111.02114, 2021.
- Schwemmer et al. [2020] Carsten Schwemmer, Carly Knight, Emily D. Bello-Pardo, Stan Oklobdzija, Martijn Schoonvelde, and Jeffrey W. Lockhart. Diagnosing gender bias in image recognition systems. Socius, 2020.
- Sharma et al. [2018] Piyush Sharma, Nan Ding, Sebastian Goodman, and Radu Soricut. Conceptual Captions: A cleaned, hypernymed, image alt-text dataset for automatic image captioning. In Annual Meeting of the Association for Computational Linguistics, 2018.
- Shoeybi et al. [2019] Mohammad Shoeybi, Mostofa Patwary, Raul Puri, Patrick LeGresley, Jared Casper, and Bryan Catanzaro. Megatron-LM: Training multi-billion parameter language models using model parallelism. arXiv:2104.08691, 2019.
- Singh et al. [2019] Amanpreet Singh, Vivek Natarajan, Meet Shah, Yu Jiang, Xinlei Chen, Dhruv Batra, Devi Parikh, and Marcus Rohrbach. Towards VQA models that can read. In IEEE Computer Vision and Pattern Recognition, 2019.
- Singh et al. [2021] Amanpreet Singh, Ronghang Hu, Vedanuj Goswami, Guillaume Couairon, Wojciech Galuba, Marcus Rohrbach, and Douwe Kiela. FLAVA: A foundational language and vision alignment model. arXiv:2112.04482, 2021.
- Smaira et al. [2020] Lucas Smaira, João Carreira, Eric Noland, Ellen Clancy, Amy Wu, and Andrew Zisserman. A short note on the Kinetics-700-2020 human action dataset. arXiv:2010.10864, 2020.
- Snell et al. [2017] Jake Snell, Kevin Swersky, and Richard Zemel. Prototypical networks for few-shot learning. Conference on Neural Information Processing Systems, 2017.
- So et al. [2021] David R So, Wojciech Mańke, Hanxiao Liu, Zihang Dai, Noam Shazeer, and Quoc V. Le. Primer: Searching for efficient transformers for language modeling. arXiv:2109.08668, 2021.
- Strubell et al. [2019] Emma Strubell, Ananya Ganesh, and Andrew McCallum. Energy and policy considerations for deep learning in NLP. arXiv:1906.02243, 2019.
- Su et al. [2019] Weijie Su, Xizhou Zhu, Yue Cao, Bin Li, Lewei Lu, Furu Wei, and Jifeng Dai. VL-BERT: Pre-training of generic visual-linguistic representations. arXiv:1908.08530, 2019.
- Sun et al. [2019] Chen Sun, Austin Myers, Carl Vondrick, Kevin Murphy, and Cordelia Schmid. VideoBERT: A joint model for video and language representation learning. In International Conference on Computer Vision, 2019.
- Sutskever et al. [2011] Ilya Sutskever, James Martens, and Geoffrey E. Hinton. Generating text with recurrent neural networks. In International Conference on Machine Learning, 2011.
- Tan and Bansal [2019] Hao Tan and Mohit Bansal. LXMERT: Learning cross-modality encoder representations from transformer. In Conference on Empirical Methods in Natural Language Processing, 2019.
- Thomee et al. [2016] Bart Thomee, David A Shamma, Gerald Friedland, Benjamin Elizalde, Karl Ni, Douglas Poland, Damian Borth, and Li-Jia Li. YFCC100M: The new data in multimedia research. Communications of the ACM, 2016.
- Thoppilan et al. [2022] Romal Thoppilan, Daniel De Freitas, Jamie Hall, Noam Shazeer, Apoorv Kulshreshtha, Heng-Tze Cheng, Alicia Jin, Taylor Bos, Leslie Baker, Yu Du, YaGuang Li, Hongrae Lee, Huaixiu Steven Zheng, Amin Ghafouri, Marcelo Menegali, Yanping Huang, Maxim Krikun, Dmitry Lepikhin, James Qin, Dehao Chen, Yuanzhong Xu, Zhifeng Chen, Adam Roberts, Maarten Bosma, Vincent Zhao, Yanqi Zhou, Chung-Ching Chang, Igor Krivokon, Will Rusch, Marc Pickett, Pranesh Srinivasan, Laichee Man, Kathleen Meier-Hellstern, Meredith Ringel Morris, Tulsee Doshi, Renelito Delos Santos, Toju Duke, Johnny Soraker, Ben Zevenbergen, Vinodkumar Prabhakaran, Mark Diaz, Ben Hutchinson, Kristen Olson, Alejandra Molina, Erin Hoffman-John, Josh Lee, Lora Aroyo, Ravi Rajakumar, Alena Butryna, Matthew Lamm, Viktoriya Kuzmina, Joe Fenton, Aaron Cohen, Rachel Bernstein, Ray Kurzweil, Blaise Aguera-Arcas, Claire Cui, Marian Croak, Ed Chi, and Quoc Le. LaMDA: Language models for dialog applications. arXiv:2201.08239, 2022.
- Tian et al. [2020] Yonglong Tian, Yue Wang, Dilip Krishnan, Joshua B. Tenenbaum, and Phillip Isola. Rethinking few-shot image classification: a good embedding is all you need? In European Conference on Computer Vision, 2020.
- Touvron et al. [2019] Hugo Touvron, Andrea Vedaldi, Matthijs Douze, and Hervé Jégou. Fixing the train-test resolution discrepancy. Conference on Neural Information Processing Systems, 2019.
- Tsimpoukelli et al. [2021] Maria Tsimpoukelli, Jacob Menick, Serkan Cabi, SM Eslami, Oriol Vinyals, and Felix Hill. Multimodal few-shot learning with frozen language models. Conference on Neural Information Processing Systems, 2021.
- Vaswani et al. [2017] Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Łukasz Kaiser, and Illia Polosukhin. Attention is all you need. In Conference on Neural Information Processing Systems, 2017.
- Vinyals et al. [2015] Oriol Vinyals, Alexander Toshev, Samy Bengio, and Dumitru Erhan. Show and tell: A neural image caption generator. In International Conference on Computer Vision, 2015.
- Vinyals et al. [2016] Oriol Vinyals, Charles Blundell, Timothy Lillicrap, Koray Kavukcuoglu, and Daan Wierstra. Matching networks for one shot learning. Conference on Neural Information Processing Systems, 2016.
- Wang et al. [2021a] Jianfeng Wang, Xiaowei Hu, Zhe Gan, Zhengyuan Yang, Xiyang Dai, Zicheng Liu, Yumao Lu, and Lijuan Wang. UFO: A unified transformer for vision-language representation learning. arXiv:2111.10023, 2021a.
- Wang et al. [2022a] Peng Wang, An Yang, Rui Men, Junyang Lin, Shuai Bai, Zhikang Li, Jianxin Ma, Chang Zhou, Jingren Zhou, and Hongxia Yang. Unifying architectures, tasks, and modalities through a simple sequence-to-sequence learning framework. arXiv:2202.03052, 2022a.
- Wang et al. [2022b] Thomas Wang, Adam Roberts, Daniel Hesslow, Teven Le Scao, Hyung Won Chung, Iz Beltagy, Julien Launay, and Colin Raffel. What language model architecture and pretraining objective work best for zero-shot generalization? arXiv:2204.05832, 2022b.
- Wang et al. [2021b] Wenhui Wang, Hangbo Bao, Li Dong, and Furu Wei. VLMo: Unified vision-language pre-training with mixture-of-modality-experts. arXiv:2111.02358, 2021b.
- Wang et al. [2019] Xin Wang, Jiawei Wu, Junkun Chen, Lei Li, Yuan-Fang Wang, and William Yang Wang. VATEX: A large-scale, high-quality multilingual dataset for video-and-language research. In International Conference on Computer Vision, 2019.
- Wang et al. [2020] Yue Wang, Shafiq Joty, Michael Lyu, Irwin King, Caiming Xiong, and Steven Hoi. VD-BERT: A unified vision and dialog transformer with BERT. In Conference on Empirical Methods in Natural Language Processing, 2020.
- Wang et al. [2021c] Zirui Wang, Jiahui Yu, Adams Wei Yu, Zihang Dai, Yulia Tsvetkov, and Yuan Cao. SimVLM: Simple visual language model pretraining with weak supervision. arXiv:2108.10904, 2021c.
- Wei et al. [2021] Jason Wei, Maarten Bosma, Vincent Y. Zhao, Kelvin Guu, Adams Wei Yu, Brian Lester, Nan Du, Andrew M. Dai, and Quoc V. Le. Finetuned language models are zero-shot learners. arXiv:2109.01652, 2021.
- Weidinger et al. [2021] Laura Weidinger, John Mellor, Maribeth Rauh, Conor Griffin, Jonathan Uesato, Po-Sen Huang, Myra Cheng, Mia Glaese, Borja Balle, Atoosa Kasirzadeh, Zac Kenton, Sasha Brown, Will Hawkins, Tom Stepleton, Courtney Biles, Abeba Birhane, Julia Haas, Laura Rimell, Lisa Anne Hendricks, William Isaac, Sean Legassick, Geoffrey Irving, and Iason Gabriel. Ethical and social risks of harm from language models. arXiv:2112.04359, 2021.
- Wortsman et al. [2022] Mitchell Wortsman, Gabriel Ilharco, Samir Yitzhak Gadre, Rebecca Roelofs, Raphael Gontijo-Lopes, Ari S. Morcos, Hongseok Namkoong, Ali Farhadi, Yair Carmon, Simon Kornblith, and Ludwig Schmidt. Model soups: averaging weights of multiple fine-tuned models improves accuracy without increasing inference time. arXiv:2203.05482, 2022.
- Wu et al. [2021] Bo Wu, Shoubin Yu, Zhenfang Chen, Joshua B. Tenenbaum, and Chuang Gan. STAR: A Benchmark for Situated Reasoning in Real-World Videos. In Conference on Neural Information Processing Systems, 2021.
- Xiao et al. [2021] Junbin Xiao, Xindi Shang, Angela Yao, and Tat-Seng Chua. Next-QA: Next phase of question-answering to explaining temporal actions. In IEEE Computer Vision and Pattern Recognition, 2021.
- Xu et al. [2017] Dejing Xu, Zhou Zhao, Jun Xiao, Fei Wu, Hanwang Zhang, Xiangnan He, and Yueting Zhuang. Video question answering via gradually refined attention over appearance and motion. In ACM Multimedia, 2017.
- Xu et al. [2022] Hanwei Xu, Yujun Chen, Yulun Du, Nan Shao, Yanggang Wang, Haiyu Li, and Zhilin Yang. Zeroprompt: Scaling prompt-based pretraining to 1,000 tasks improves zero-shot generalization. arXiv:2201.06910, 2022.
- Xu et al. [2021] Hu Xu, Gargi Ghosh, Po-Yao Huang, Prahal Arora, Masoumeh Aminzadeh, Christoph Feichtenhofer, Florian Metze, and Luke Zettlemoyer. VLM: Task-agnostic video-language model pre-training for video understanding. arXiv:2105.09996, 2021.
- Yan et al. [2021] Ming Yan, Haiyang Xu, Chenliang Li, Junfeng Tian, Bin Bi, Wei Wang, Weihua Chen, Xianzhe Xu, Fan Wang, Zheng Cao, Zhicheng Zhang, Qiyu Zhang, Ji Zhang, Songfang Huang, Fei Huang, Luo Si, and Rong Jin. Achieving human parity on visual question answering. arXiv:2111.08896, 2021.
- Yan et al. [2022] Shen Yan, Xuehan Xiong, Anurag Arnab, Zhichao Lu, Mi Zhang, Chen Sun, and Cordelia Schmid. Multiview transformers for video recognition. arXiv:2201.04288, 2022.
- Yang et al. [2021a] Antoine Yang, Antoine Miech, Josef Sivic, Ivan Laptev, and Cordelia Schmid. Just ask: Learning to answer questions from millions of narrated videos. In International Conference on Computer Vision, 2021a.
- Yang et al. [2021b] Zhengyuan Yang, Zhe Gan, Jianfeng Wang, Xiaowei Hu, Yumao Lu, Zicheng Liu, and Lijuan Wang. An empirical study of GPT-3 for few-shot knowledge-based VQA. In National Conference on Artificial Intelligence (AAAI), 2021b.
- Yang et al. [2021c] Zhengyuan Yang, Yijuan Lu, Jianfeng Wang, Xi Yin, Dinei Florencio, Lijuan Wang, Cha Zhang, Lei Zhang, and Jiebo Luo. TAP: Text-aware pre-training for text-VQA and text-caption. In IEEE Computer Vision and Pattern Recognition, 2021c.
- Yao et al. [2021] Lewei Yao, Runhui Huang, Lu Hou, Guansong Lu, Minzhe Niu, Hang Xu, Xiaodan Liang, Zhenguo Li, Xin Jiang, and Chunjing Xu. FILIP: Fine-grained interactive language-image pre-training. arXiv:2111.07783, 2021.
- Young et al. [2014] Peter Young, Alice Lai, Micah Hodosh, and Julia Hockenmaier. From image descriptions to visual denotations: New similarity metrics for semantic inference over event descriptions. Annual Meeting of the Association for Computational Linguistics, 2014.
- Yuan et al. [2021] Lu Yuan, Dongdong Chen, Yi-Ling Chen, Noel Codella, Xiyang Dai, Jianfeng Gao, Houdong Hu, Xuedong Huang, Boxin Li, Chunyuan Li, Ce Liu, Mengchen Liu, Zicheng Liu, Yumao Lu, Yu Shi, Lijuan Wang, Jianfeng Wang, Bin Xiao, Zhen Xiao, Jianwei Yang, Michael Zeng, Luowei Zhou, and Pengchuan Zhang. Florence: A new foundation model for computer vision. arXiv:2111.11432, 2021.
- Zaken et al. [2021] Elad Ben Zaken, Shauli Ravfogel, and Yoav Goldberg. BitFit: Simple parameter-efficient fine-tuning for transformer-based masked language-models. arXiv:2106.10199, 2021.
- Zellers et al. [2021] Rowan Zellers, Ximing Lu, Jack Hessel, Youngjae Yu, Jae Sung Park, Jize Cao, Ali Farhadi, and Yejin Choi. MERLOT: Multimodal neural script knowledge models. Conference on Neural Information Processing Systems, 2021.
- Zellers et al. [2022] Rowan Zellers, Jiasen Lu, Ximing Lu, Youngjae Yu, Yanpeng Zhao, Mohammadreza Salehi, Aditya Kusupati, Jack Hessel, Ali Farhadi, and Yejin Choi. MERLOT reserve: Neural script knowledge through vision and language and sound. In IEEE Computer Vision and Pattern Recognition, 2022.
- Zeng et al. [2022] Andy Zeng, Adrian Wong, Stefan Welker, Krzysztof Choromanski, Federico Tombari, Aveek Purohit, Michael Ryoo, Vikas Sindhwani, Johnny Lee, Vincent Vanhoucke, and Pete Florence. Socratic models: Composing zero-shot multimodal reasoning with language. arXiv:2204.00598, 2022.
- Zhai et al. [2021a] Xiaohua Zhai, Alexander Kolesnikov, Neil Houlsby, and Lucas Beyer. Scaling vision transformers. arXiv:2106.04560, 2021a.
- Zhai et al. [2021b] Xiaohua Zhai, Xiao Wang, Basil Mustafa, Andreas Steiner, Daniel Keysers, Alexander Kolesnikov, and Lucas Beyer. LiT: Zero-shot transfer with locked-image text tuning. arXiv:2111.07991, 2021b.
- Zhao et al. [2021a] Dora Zhao, Angelina Wang, and Olga Russakovsky. Understanding and evaluating racial biases in image captioning. In IEEE Computer Vision and Pattern Recognition, 2021a.
- Zhao et al. [2021b] Zihao Zhao, Eric Wallace, Shi Feng, Dan Klein, and Sameer Singh. Calibrate before use: Improving few-shot performance of language models. In International Conference on Machine Learning, 2021b.
- Zhou et al. [2018] Luowei Zhou, Chenliang Xu, and Jason J. Corso. Towards automatic learning of procedures from web instructional videos. In National Conference on Artificial Intelligence (AAAI), 2018.
- Zhou et al. [2020] Luowei Zhou, Hamid Palangi, Lei Zhang, Houdong Hu, Jason Corso, and Jianfeng Gao. Unified vision-language pre-training for image captioning and VQA. In National Conference on Artificial Intelligence (AAAI), 2020.
- Zhu and Yang [2020] Linchao Zhu and Yi Yang. ActBERT: Learning global-local video-text representations. In IEEE Computer Vision and Pattern Recognition, 2020.
- Zhu [2020] Ron Zhu. Enhance multimodal transformer with external label and in-domain pretrain: Hateful meme challenge winning solution. arXiv:2012.08290, 2020.
- Zhu et al. [2019] Xinxin Zhu, Longteng Guo, Peng Yao, Shichen Lu, Wei Liu, and Jing Liu. Vatex video captioning challenge 2020: Multi-view features and hybrid reward strategies for video captioning. arXiv:1910.11102, 2019.
- Zhu et al. [2021] Xizhou Zhu, Jinguo Zhu, Hao Li, Xiaoshi Wu, Xiaogang Wang, Hongsheng Li, Xiaohua Wang, and Jifeng Dai. Uni-Perceiver: Pre-training unified architecture for generic perception for zero-shot and few-shot tasks. arXiv:2112.01522, 2021.
- Zintgraf et al. [2019] Luisa Zintgraf, Kyriacos Shiarli, Vitaly Kurin, Katja Hofmann, and Shimon Whiteson. Fast context adaptation via meta-learning. In International Conference on Machine Learning, 2019.
Checklist
-
1.
For all authors…
-
(a)
Do the main claims made in the abstract and introduction accurately reflect the paper’s contributions and scope? [Yes]
-
(b)
Did you describe the limitations of your work? [Yes] See Section
[5](#S5). - (c)
-
(d)
Have you read the ethics review guidelines and ensured that your paper conforms to them? [Yes]
-
(a)
-
2.
If you are including theoretical results…
-
(a)
Did you state the full set of assumptions of all theoretical results? [N/A]
-
(b)
Did you include complete proofs of all theoretical results? [N/A]
-
(a)
-
3.
If you ran experiments…
-
(a)
Did you include the code, data, and instructions needed to reproduce the main experimental results (either in the supplemental material or as a URL)? [No] The code and the data are proprietary.
- (b)
-
(c)
Did you report error bars (e.g., with respect to the random seed after running experiments multiple times)? [No] We do not observe large enough variance in our training runs to justify the computation cost incurred by multiple training runs. For the largest models, it is not feasible within our compute budget.
-
(d)
Did you include the total amount of compute and the type of resources used (e.g., type of GPUs, internal cluster, or cloud provider)? [Yes] Details can be found in Appendix
[B.1.2](#A2.SS1.SSS2). In short, our largest run was trained on 1536 TPU chips for 15 days.
-
(a)
-
4.
If you are using existing assets (e.g., code, data, models) or curating/releasing new assets…
-
(a)
If your work uses existing assets, did you cite the creators? [Yes] We properly cited the prior methods on which our work is based, as well as prior datasets when appropriate (e.g., ALIGN).
-
(b)
Did you mention the license of the assets? [N/A] The assets we used are previous work for which we cited papers. We do mention the license of all visual assets we use for the figures of the paper in Appendix
[G](#A7). -
(c)
Did you include any new assets either in the supplemental material or as a URL? [No]
- (d)
- (e)
-
(a)
-
5.
If you used crowdsourcing or conducted research with human subjects…
-
(a)
Did you include the full text of instructions given to participants and screenshots, if applicable? [N/A]
-
(b)
Did you describe any potential participant risks, with links to Institutional Review Board (IRB) approvals, if applicable? [N/A]
-
(c)
Did you include the estimated hourly wage paid to participants and the total amount spent on participant compensation? [N/A]
-
(a)
Appendix
We provide an overview of the Appendix below.
Method (Appendix [A](#A1)).
We first provide additional details about our model in Appendix [A.1](#A1.SS1):
- •
- •
- •
-
•
Hyperparameters for all model architectures are given in Appendix
[A.1.4](#A1.SS1.SSS4).
We then explain how we evaluate our models using in-context few-shot learning in Appendix [A.2](#A1.SS2). This includes details on how we build the few-shot prompt, how we get predictions for open- and close-ended tasks, how we obtain the zero-shot numbers, and how we leverage retrieval and ensembling to take advantage of more annotated examples.
Finally, in Appendix [A.3](#A1.SS3), we provide more details on our training datasets:
Experiments (Appendix [B](#A2)).
We first provide additional training and evaluation details in Appendix [B.1](#A2.SS1), including:
-
•
Details on Flamingo-3B, Flamingo-9B and Flamingo in Appendix
[B.1.1](#A2.SS1.SSS1), -
•
The training hyperparameters in Appendix
[B.1.2](#A2.SS1.SSS2), -
•
More details on the Contrastive model pretraining in Appendix
[B.1.3](#A2.SS1.SSS3), -
•
Details on our evaluation benchmarks and splits in Appendix
[B.1.4](#A2.SS1.SSS4), -
•
A discussion on the few-shot learning hyperparameters in Appendix
[B.1.5](#A2.SS1.SSS5), - •
Next, we give additional results obtained by our models in Appendix [B.2](#A2.SS2) including the performance of the Flamingo models on classification tasks in Appendix [B.2.1](#A2.SS2.SSS1), detailed fine-tuning results in Appendix [B.2.2](#A2.SS2.SSS2), and zero-shot results from our contrastive models (Appendix [B.2.3](#A2.SS2.SSS3)).
Finally, we provide more ablation studies in Appendix [B.3](#A2.SS3) for both the Flamingo models (Appendix [B.3.1](#A2.SS3.SSS1)) and our contrastive pretrained Visual Encoders (Appendix [B.3.2](#A2.SS3.SSS2)).
Qualitative results (Appendix [C](#A3)). More qualitative results are given in Appendix [C](#A3): Figure [10](#A3.F10) (single image sample), Figure [11](#A3.F11) (dialogue examples), and Figure [12](#A3.F12) (video examples).
Discussion (Appendix [D](#A4)).
We provide a more complete discussion on our work, including limitations, failure cases, broader impacts and societal impacts of our work in Appendix [D](#A4).
Appendix A Method
A.1 Model details
A.1.1 Perceiver Resampler
Expanding on our brief description in Section [2.1](#S2.SS1),
Figure [5](#A1.F5) provides an illustration of our Perceiver Resampler processing an example video, together with pseudo-code.
Our Perceiver Resampler is similar in spirit to the Perceiver models proposed by Jaegle et al. [[48](#bib.bib48)].
We learn a predefined number of latent input queries, and cross-attend to the flattened visual features .
These visual features are obtained by first adding a learnt temporal position encoding to each feature within a given video frame (an image being considered as a single-frame video).
Note that we only use temporal encodings and no explicit spatial grid position encodings;
we did not observe improvements from the latter.
This rationale behind is likely that CNNs, such as our NFNet encoder, are known to implicitly include spatial information channel-wise [[47](#bib.bib47)].
The visual features are then flattened and concatenated as illustrated in Figure [5](#A1.F5).
The number of output tokens of the Perceiver Resampler is equal to the number of learnt latent queries.
Unlike in DETR and Perceiver, the keys and values computed from the learnt latents are concatenated to the keys and values obtained from , which we found to perform slightly better.
A.1.2 gated xattn-dense details
We provide in Figure [4](#S2.F4) an illustration of a gated xattn-dense block and how it connects to a frozen LM block, together with pseudo-code.
We also plot in Figure [6](#A1.F6) the evolution of the absolute value of the gating values as a function of training progress (from to ) at different layers of the LM stack for the Flamingo-3B model composed of 24 LM layers.
All layers of the frozen LM stack seem to utilize the visual information as the gating absolute values quickly grow in absolute value from their 0 initializations.
We also note that the absolute values seem to grow with the depth.
However, it is difficult to draw strong conclusions from this observation: the scale of the activations before gating may also vary with depth.
Future work is required to better understand the effect of these added layers on the optimization dynamics and on the model itself.
A.1.3 Multi-visual input support
We illustrate in Figure [7](#A1.F7) the masking approach we use to limit the number of visual tokens that a certain text token sees.
We also formalize our notation for the interleaved sequences of images/videos and text.
Interleaved sequences of visual data and text.
We consider interleaved image/video and text examples: each example holds a sequence of text , a sequence of images/videos , and the sequence of positions of the images in the text. Based on the visual data positions, we define a function that assigns to each text position the index of the last image/video appearing before this position (or if no visual data appears before the position).
The function defines which visual inputs we consider usable to predict token in Equation ([1](#S2.E1)): the set of preceding tokens , and the set of preceding images/videos .
A.1.4 Transformer architecture
| Perceiver Resampler | gated xattn-dense | Frozen LM | ||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L | D | H | Act. | L | D | H | Act. | L | D | H | Act. | |
| Flamingo-3B | 6 | 1536 | 16 | Sq. ReLU | 24 | 2048 | 16 | Sq. ReLU | 24 | 2048 | 16 | GeLU |
| Flamingo-9B | 6 | 1536 | 16 | Sq. ReLU | 10 | 4096 | 32 | Sq. ReLU | 40 | 4096 | 32 | GeLU |
| Flamingo | 6 | 1536 | 16 | Sq. ReLU | 12 | 8192 | 64 | Sq. ReLU | 80 | 8192 | 64 | GeLU |
[104](#bib.bib104)].
We list in Table [4](#A1.T4) the number of layers (), the hidden dimension (), the number of heads (), and the FFW activation (Act.) used for each transformer component of our Flamingo models.
The dimension of keys and values in each configuration is given by (96 for the Perceiver Resampler; 128 for gated xattn-dense and the frozen LM),
and the hidden dimension of each feed-forward MLP is .
Note that the frozen LM was trained with the GeLU activation [[39](#bib.bib39)], while the remaining trainable transformer layers use the Squared ReLU activation [[104](#bib.bib104)], which we found to outperform GeLU.
A.2 In-context few-shot evaluation details
In-context learning with Flamingo models.
We evaluate the ability of our models to rapidly adapt to new tasks using in-context learning, following an analogous approach to the one used in GPT-3 [[11](#bib.bib11)].
In detail, we are given a set of support examples in the form of or (where the or is the input visual and the is the expected response and any additional task-specific information, e.g., a question) and a single visual query for which we want our model to make a prediction.
Given this, we build a multimodal prompt by concatenating the support examples followed by the visual query as illustrated by Figure [8](#A1.F8).
Unless specified otherwise, we choose the concatenation order at random.
Open-ended and close-ended evaluations.
In an open-ended setting, the model’s sampled text following the query image is then taken as its prediction for the image, stopping at the first <EOC> (“end of chunk”) token prediction. Unless specified otherwise, we always use beam search with a beam size of 3. In a close-ended setting, all possible outputs are independently appended to the query image, and we score each of the resulting sequences using the log-likelihood estimated by our model. These scores are then used to rank the candidate outputs in decreasing order, from most confident to least confident.
Zero-shot generalization.
In the absence of few-shot examples, approaches commonly rely on prompt engineering [[85](#bib.bib85)] to condition the model at inference using a suitable natural language description of the task.
Validation of such prompts can significantly impact performance but requires access to a number of annotated examples and cannot therefore be considered truly zero-shot.
Furthermore, Perez et al. [[80](#bib.bib80)] have shown that such validation procedures are generally not robust with access to only a handful of samples during validation.
To report zero-shot performance in our work,
we instead build a prompt with two examples from the downstream tasks where we remove their corresponding images or videos.
For example, for the task illustrated at the top of Figure [8](#A1.F8), the prompt would be “<BOS>Output: This is a cat wearing sunglasses.<EOC>Output: Three elephants walking in the savanna.<EOC><image> Output:” and no support images would be fed to the model.
We observed that only showing one, instead of two, text examples in the prompt is highly detrimental as the model is biased towards producing text output similar to the single provided text example.
Providing more than two text examples helps but only marginally.
We hence use two text examples in all zero-shot results for practicality.
In practice, we believe this is not more cumbersome than finding a good natural text description for a given task.
This relates to recent findings on the aspects of demonstrations that are key drivers of performance [[76](#bib.bib76)].
For close-ended tasks, where we use the model to score different possible answers, we observe it is not necessary to provide a single text example in the zero-shot prompt.
Retrieval-based In-Context Example Selection [[136](#bib.bib136)].
When the size of the support set exceeds a certain limit, it can become difficult to leverage all the examples with in-context learning:
first because it becomes excessively expensive to fit all the examples in the prompt, and second because there is a risk of poor generalization when the prompt size exceeds the size of the sequence used during training [[83](#bib.bib83)].
In such situations, it is appealing to use a form of prompt selection to both limit the sequence length as well as potentially improve the prompt quality which can in turn lead to better performance [[63](#bib.bib63)].
In particular, we follow the Retrieval-based In-Context Example Selection (RICES) approach introduced by [[136](#bib.bib136)].
In detail, given a query image, we retrieve similar images in the support set by comparing the visual features extracted from our frozen pretrained visual encoder.
We then build the prompt by concatenating the top- most similar examples.
Since LMs are sensitive to the ordering in the prompt due to recency bias [[148](#bib.bib148)], we order the examples by increasing order of similarity, such that the most similar support example appears right before the query.
We notably show the effectiveness of this approach in classification settings with multiple hundreds of classes (see Appendix [B.2.1](#A2.SS2.SSS1)) where we are given one or more images/videos per class, yielding a number of examples that would not otherwise fit in the prompt.
Prompt ensembling.
We also explore ensembling the outputs of the model across multiple prompts in the close-ended setting. This can notably be combined with RICES where ensembling can be done over multiple permutations of the ranked nearest neighbors. Specifically, for a given answer, we average the log likelihoods estimated by the model over 6 random permutations of the selected few-shot examples.
A.3 Training dataset details
We train the Flamingo models on a carefully chosen mixture of datasets illustrated in Figure [9](#A1.F9) and described next.
A.3.1 M3W collection
The selection and scraping of web pages for M3W follows a similar process to the one used for collecting the MassiveWeb dataset [[86](#bib.bib86)]. We start by filtering out non-English documents.
We also remove those that do not pass internal filters,
which identify explicit content across images, videos, and text. We use a custom scraper to extract salient content from the remaining documents, in the form of plain text interleaved with images, as described in Section [2.4](#S2.SS4).
The text in M3W is collected in a similar fashion to that of MassiveWeb,
but we also collect any images present at the same level in the HTML tree. We discard documents for which the scraping process does not yield any images.
We then apply similar text filtering heuristics, to remove low quality documents and reduce repetition, as well as some image filters to remove images that are too small (either width or height less than 64 pixels), too wide or narrow (aspect ratio greater than 3 in either direction), or unambiguously low quality (e.g. single-colour images). We discard documents that no longer contain any images following this filtering step.
A.3.2 M3W image-placement augmentation
During evaluation of Flamingo models, we prompt the model with an image and ask it to generate text for that image. This lends itself to a natural sequencing at inference time in which the image comes before the corresponding text output.
However, the correspondence between images and text in our interleaved M3W dataset (Section [2.4](#S2.SS4)) is in general unknown (and potentially not well-defined in certain cases).
As a motivating example, a simple webpage might be structured in either of the following ways:
-
(a)
This is my dog! <dog image> This is my cat! <cat image>
-
(b)
<dog image> That was my dog! <cat image> That was my cat!
The text-aligned image indices (indices) might “ideally” be chosen such that at each point in the text, the index points to the most semantically relevant image for that text – i.e., the next image in example (a), and the previous image in example (b). In the absence of a general way to determine semantic correspondence between text and images on webpages “in the wild”, we make a simplifying assumption that the most relevant image at any given point in the text is either the last image appearing before the text token, or the image immediately following it (as in the simple examples above), and choose indices accordingly.
During training, for each webpage sampled, we sample with probability whether indices are chosen to map text to the previous or next image.
This inevitably means we make the semantically “unnatural” choice – e.g., associating the text “This is my cat!” with the dog image in (a) above – around half of the time.
We ablate this choice in Section [3.3](#S3.SS3), finding a small advantage to setting over either (always the previous image index) or (always the next image index).
This suggests that there may be a beneficial “data augmentation” effect to this randomisation.
A.3.3 LTIP and VTP: Visual data paired with text
Along with our interleaved image and text dataset, we use several paired vision and text web datasets for training.
One dataset is ALIGN [[50](#bib.bib50)], composed of 1.8 billion images paired with alt-text.
ALIGN is large, but noisy and limited to images.
The images are often poorly described by the corresponding alt-text annotation.
For this reason, we augment it with two datasets: LTIP (Long Text & Image Pairs) consists of 312 million images, and VTP (Video & Text Pairs) consists of 27 million short videos (approximately 22 seconds on average). Both datasets are paired with more descriptive captions.
For instance, the average number of tokens of an ALIGN text description is 12.4 per image, while it is 20.5 for the LTIP dataset.
The LTIP and VTP datasets were collected by crawling fewer than ten websites targeting high-quality and rich image descriptions.
These single-image and single-video datasets are preprocessed analogously to the M3W data preprocessing described previously, adding the <image> tag at the beginning of the sequence (immediately after <BOS>), and the <EOC> token after the text (before <EOS>).
We deduplicated these datasets against all our benchmarks (against both the training and the evaluation sets) using image similarity, as detailed in Appendix [A.3.4](#A1.SS3.SSS4).
Datasheets for LTIP and VTP are respectively given in Appendix [F.2.1](#A6.SS2.SSS1) and Appendix [F.2.2](#A6.SS2.SSS2).
A.3.4 Dataset deduplication against evaluation tasks
We used an internal deduplication tool to deduplicate our training datasets from our evaluation datasets. This deduplication pipeline relies on a trained visual encoder which maps embedding closer together when they are potential duplicates. Once the image embeddings have been computed, a fast approximate nearest neighbor search is performed on the training images to retrieve duplicate candidates from the validation datasets. For the paired image-text dataset, we have deduplicated our LTIP and ALIGN training images against: ImageNet (train, val), COCO (train, valid, test), OK-VQA (train, valid, test), VQAv2 (train, valid, test), Flickr30k (train, valid, test), VisDial (train, valid, test).
We did not deduplicate our image datasets against VizWiz, HatefulMemes and TextVQA as we performed these evaluations only after having trained our Flamingo models. However, we believe this had no impact on our results as the images from these datasets are unlikely to be scraped from the web; VizWiz images were obtained using a specific mobile app and only available for download, HatefulMemes memes were created by researchers instead of being scraped on the web and finally TextVQA images are from OpenImages.
Note that we did not run the deduplication on the M3W dataset as one training example is a full webpage of interleaved paragraph with several images, unlikely to contain images from our benchmark suite. To verify this hypothesis, we have obtained near-duplicate statistics on the 185M individual images from M3W and the results are the following: in total, 1314 potential duplicates were found from the validation and test splits of ImageNet, COCO, OK-VQA, VQAv2, Flickr30k and VisDial. Out of the 1314 candidates, only 125 are exact duplicates.
For the video datasets, we did not perform any deduplication of VTP (27M videos) as none of the collected VTP videos were obtained from YouTube or Flickr, which are the sources of all of our video evaluation datasets collected on the Internet.
Appendix B Experiments
B.1 Training and evaluation details
B.1.1 Models
| Requires | Frozen | Trainable | Total | |||
|---|---|---|---|---|---|---|
| model sharding | Language | Vision | gated xattn-dense | Resampler | count | |
| Flamingo-3B | ✗ | 1.4B | 435M | 1.2B (every) | 194M | 3.2B |
| Flamingo-9B | ✗ | 7.1B | 435M | 1.6B (every 4th) | 194M | 9.3B |
| Flamingo | ✓ | 70B | 435M | 10B (every 7th) | 194M | 80B |
We perform experiments across three model sizes, where we scale the frozen language model from 1.4B to 7B and 70B; and adapt the parameter count of other components accordingly.
We keep the pretrained vision encoder frozen across all experiments and use a NFNet-F6 model trained contrastively (see Appendix [B.1.3](#A2.SS1.SSS3)), unless explicitly stated otherwise in the ablation study.
We use a Perceiver Resampler with approximately 200M parameters across all three model sizes.
The decision on how many gated xattn-dense layers to interleave is mainly driven by a trade-off between memory constraints and downstream performance. We identified the optimal trade-off at small model scales, before transferring our findings to the large model architecture.
We obtain three models, Flamingo-3B, Flamingo-9B and Flamingo-80B, detailed below:
-
•
The Flamingo-3B model builds on top of a 1.4B frozen language model from [
[42](#bib.bib42)]. Before each transformer block, we add a gated xattn-dense layer attending to the visual inputs; this accounts for 1.4B additional learned parameters. -
•
The Flamingo-9B model builds on top of a 7B frozen language model from [
[42](#bib.bib42)]. Starting from the very first layer and before every fourth transformer blocks, we add a gated xattn-dense layer attending to the visual inputs; this accounts for 1.8B additional learned parameters. -
•
The Flamingo-80B model builds on top of the frozen Chinchilla 70B language model [
[42](#bib.bib42)]. Starting from the very first layer and before every seventh transformer blocks, we add a gated xattn-dense layer attending to the visual inputs; this accounts for 10B additional learned parameters. For simplicity, we refer to this model as simply Flamingo throughout the paper.
In Table [5](#A2.T5) we report the parameter count of each component of our models, as well as model sharding requirements.
We provide more Transformer architecture details in Appendix [A.1.4](#A1.SS1.SSS4).
The Flamingo model card [[77](#bib.bib77)] is also given in Appendix [E](#A5).
B.1.2 Training details for the Flamingo models
Data augmentation and preprocessing.
Empirically we find that it is effective to stochastically prepend the paired dataset text samples with a single space character, with probability 0.5. We attribute this to the fact that our subword tokenizer maps the beginning of various words to a different token depending on whether it is preceded by a space. This allows us to enforce invariance to this tokenizer artifact, without degrading significantly correctness of the punctuation which is already lacking in many of these samples. We observe that this leads to substantial improvement across tasks.
The visual inputs are resized to while preserving their aspect ratios, padding the image with the mean value if required.
Note that this is higher than the resolution used for the contrastive pretraining of our Vision Encoder (see Appendix [B.1.3](#A2.SS1.SSS3)).
The increase in resolution during the final stage training was motivated by [[113](#bib.bib113)] showing one can obtain improved performance at a higher test-time resolution when using CNNs.
This increase in resolution also comes with only a moderate computational and memory cost as no backpropagation is performed through the frozen Vision Encoder.
We also employ random left/right flips and color augmentation.
For interleaved datasets (Section [2.4](#S2.SS4)) we also employ augmentation by lightly randomizing the selected image indices with a hyperparameter when sampling examples from the M3W dataset.
This augmentation is detailed in Appendix [A.3.2](#A1.SS3.SSS2) and our choice of is ablated in Appendix [B.3.1](#A2.SS3.SSS1).
For video training, we temporally sample a clip of 8 frames sampled at one frame per second (fps) from each training video.
Although our model was trained with a fixed number of 8 frames, at inference time, we input 30 frames at 3 FPS.
This is achieved by linearly interpolating the learnt temporal position embedding of the Perceiver Resampler at inference time.
Loss and optimisation.
All our models are trained using the AdamW optimizer with global norm clipping of , no weight decay for the Perceiver Resampler and weight decay of 0.1 for the other trainable parameters. The learning rate is increased linearly from to up over the first 5000 steps then held constant for the duration of training (no improvements were observed from decaying the learning rate). Unless specified otherwise we train our models for steps. Four datasets are used for training: M3W, ALIGN, LTIP and VTP with weights of , , and respectively. These weights were obtained empirically at a small model scale and kept fixed afterwards. Batch sizes depend on the setting and are given in the next sections.
Infrastructure and implementation.
Our model and associated infrastructure were implemented using JAX [[8](#bib.bib8)] and Haiku [[40](#bib.bib40)]. All training and evaluation was performed on TPUv4 instances. The largest model containing 80 billion parameters is trained on chips for 15 days and sharded across 16 devices.
Megatron type sharding [[99](#bib.bib99)] is used to enable 16-way model parallelism for all Embedding / Self-Attention / Cross-Attention / FFW layers, while the NFNet vision layers were unsharded. ZeRO stage 1 [[88](#bib.bib88)] is used to shard the optimizer state. All trained parameters and optimizer accumulators are stored and updated in float32; all activations and gradients are computed in bfloat16 after downcasting of parameters from float32 to bfloat16. Frozen parameters are stored and applied in bfloat16.
B.1.3 Contrastive model details
The vision encoder is trained from scratch, together with a language encoder. Using these encoders, images and text pairs are separately encoded and projected to a shared embedding space and L2 normalized.
From these embeddings, we maximize the similarity of paired embeddings and minimize the similarity of unpaired embeddings, using a multi-class cross-entropy loss, where the paired image-texts are treated as positive examples and the rest of the batch as negative examples.
We use the same loss as in CLIP [[85](#bib.bib85)], which consists of two contrastive losses, one from text to image and the other from image to text. We use a learnable temperature parameter in the final log-softmax layer [[9](#bib.bib9)].
The text-to-image loss is as follows:
| (3) |
And the image-to-text loss is defined analogously:
| (4) |
The sum of the two losses is minimized.
Here, and are, respectively, the normalized embedding of the vision and language component of the -th element of a batch.
is a trainable inverse temperature parameter and is the number of elements in the batch.
We use the BERT [[23](#bib.bib23)] architecture for the language encoder. The outputs of the language and vision encoders are mean-pooled (across tokens and spatial locations, respectively) before being projected to the shared embedding space. We only use the weights from the contrastive vision encoder in the main Flamingo models.
The vision encoder is pretrained on the ALIGN and LTIP datasets.
The training image resolution is , the joint embedding space is size and the batch size is 16,384.
It is trained for million parameter update steps, each of which consist of two gradient calculation steps (more details below) on 512 TPUv4 chips. The learning rate is decayed linearly from to zero over the course of training. Images have random color augmentation and horizontal flips applied during training. We use the tokenizer employed by Jia et al. [[50](#bib.bib50)].
The Adam optimizer is used to optimize the network, and we apply label smoothing of .
We apply adaptive gradient clipping (AGC) [[10](#bib.bib10)] to the NFNet encoder and global norm gradient clipping of 10 for the BERT encoder.
To evaluate the pretrained model, we track zero-shot image classification and retrieval.
For zero-shot image classification, we use image-text retrieval between the images and the class names.
Following Radford et al. [[85](#bib.bib85)] we use “prompt-ensembling” in which we embed multiple texts using templates such as ‘‘A photo of a {class_name}’’ and average the resulting embedding.
B.1.4 Evaluation benchmarks
| Dataset | dev | Gen. | Custom prompt | Task description | Eval set | Metric | |
|---|---|---|---|---|---|---|---|
| Image |
ImageNet-1k [
|
[15](#bib.bib15)]
[3](#bib.bib3)]
[3](#bib.bib3)][69](#bib.bib69)]
[3](#bib.bib3)][139](#bib.bib139)]
[35](#bib.bib35)]
[3](#bib.bib3)][100](#bib.bib100)]
[3](#bib.bib3)][20](#bib.bib20)]
[54](#bib.bib54)]
[102](#bib.bib102)]
[122](#bib.bib122)]
[130](#bib.bib130)]
[149](#bib.bib149)]
[130](#bib.bib130)]
[135](#bib.bib135)]
[135](#bib.bib135)][73](#bib.bib73)]
[129](#bib.bib129)]
[128](#bib.bib128)]
[B.1.5](#A2.SS1.SSS5)).
Our goal is to develop models that can rapidly adapt to diverse and challenging tasks in the few-shot setting.
For this, we consider a wide array of popular image and video benchmarks summarized in Table [6](#A2.T6).
In total we chose multimodal image/video and language benchmarks, spanning tasks that require some language understanding (visual question answering, captioning, visual dialogue) as well as two standard image and video classification benchmarks (ImageNet and Kinetics).
Note that for the video datasets collected from YouTube (i.e., all video datasets except NextQA and STAR), we evaluated our model on all the publicly available video as of April 2022.
dev benchmarks.
In order to validate design decisions of our model over the course of the project, we selected five benchmarks from the multimodal image/video and language benchmarks as well as ImageNet and Kinetics for classification as our development set (referred as dev). To maximise its relevance, we choose the most challenging and widely studied benchmarks for captioning, visual question-answering and classification tasks on both images and videos.
Dataset splits for the dev benchmarks.
Concretely, estimating few-shot learning performance of a model consists of adapting it on a set of support samples and evaluating it on a set of query samples. As a result, any evaluation set should be composed of two disjoint subsets containing respectively the support and the query samples. For the dev benchmarks that are used both to validate design decisions and hyperparameters, as well as to report final performance, we therefore use four subsets:
-
•
validation support: contains support samples for validation;
-
•
validation query: contains query samples for validation;
-
•
test support: contains support samples for final performance estimation;
-
•
test query: contains query samples for final performance estimation.
In practice, for the test query subset, we use the subset that prior works report results on, for apples-to-apples comparison. While the validation set would be a natural choice for the validation query subset, we note that this is not possible for all benchmarks, since some benchmarks do not have an official validation set (e.g. OKVQA) and for others, the validation is commonly used to report final performance in place of the test set (e.g. ImageNet or COCO). For simplicity, we use a subset of the original training set as the validation query subset. Finally, we also use additional disjoint subsets of the training set as respectively the validation support subset and the test support subset.
We now describe in more detail how we form the latter three subsets. For captioning tasks, open-ended evaluation is efficient so we evaluate on a large number of samples. Specifically, for COCO, we use the same number of samples as used in the Karpathy splits for evaluation sets (5000). For VATEX, because the training set is of limited size, we only evaluate over 1024 samples, reserving the rest for support sets. For question-answering tasks, we evaluate over 1024 samples; chosen to make both open- and close-ended evaluation reasonably fast. For image classification tasks, we evaluate over 10 images per class: 10,000 samples for ImageNet, and 7000 samples for Kinetics700. As for the support sets, for both validation and final performance estimation, we use 2048 samples across all tasks, except for classification tasks where we scale this to 32 samples per class, to better estimate expected performance for each class.
Unbiased few-shot performance estimation.
Few-shot learning performance estimates on the dev benchmarks may be biased, in the sense that over the course of this project, design decisions were made based on the performance obtained on these benchmarks.
We note that this is the case for prior work which also make use of these benchmarks to validate and ablate their own design decisions.
To account for this bias and provide unbiased few-shot learning performance estimates, we report performance on a remaining set of 11 benchmarks.
Among those, some span the same open-ended image and video tasks as our dev benchmarks (captioning and visual question-answering).
But we also look at more specific benchmarks in order to explore less explored capabilities.
These notably include:
TextVQA [[100](#bib.bib100)] which specifically assesses OCR capabilities through question-answering;
VisDial [[20](#bib.bib20)], a visual dialogue benchmark;
HatefulMemes [[54](#bib.bib54)] a vision and text classification benchmark;
NextQA [[129](#bib.bib129)] which specially focuses on causality and temporal relation;
STAR [[128](#bib.bib128)], a multiple-choice question answering task;
and RareAct [[73](#bib.bib73)], a benchmark measuring compositionality in action recognition.
We emphasize that we do not validate any design decisions on these benchmarks and use them solely to estimate unbiased few-shot learning performance after Flamingo training is done.
B.1.5 Few-shot learning evaluation hyperparameters
In few-shot learning, hyperparameter selection implicitly increases the number of shots as it requires additional validation examples.
If those are not taken into account, as is often the case in practice, few-shot performance can be overestimated [[80](#bib.bib80)].
Similarly, cross-validation of benchmark-specific hyperparameters such as the prompt should be considered as a particularly basic few-shot learning method, where one selects the task-specific prompt over the set of shots.
But other learning approaches might be more effective in making use of these labelled examples.
Given the negative results reported by [[80](#bib.bib80)] in terms of the robustness of cross-validation and unless mentioned otherwise, all benchmarks are run using a single set of evaluation hyperparameters, including the prompts.
We optimize hyperparameters jointly across the validation subsets of the dev benchmarks and do not perform any benchmark-specific cross-validation of hyperparameters, aside from a few exceptions, as we detail next.
Except for HatefulMemes and RareAct, we always use the prompt “‘‘Output: {output}” for all non-question-answering tasks, and “Question: {question} Answer: {answer}” for all question-answering / visual dialogue tasks.
In particular, for VisDial [[20](#bib.bib20)], we use the previously described prompt to encode each questions/answers in the dialogue and the provided image caption is prepended to the dialogue history without any prompt.
For HatefulMemes [[54](#bib.bib54)], we use a specific prompt to incorporate the OCR information provided as input which is: “is an image with written: "{meme_text}" on it. Is it hateful? Answer: {answer}”, where the answer is either yes or no.
Note that this is the only dataset where we explicitly provide OCR text “meme_text” as input to Flamingo models.
For TextVQA, we do not make use of the provided OCR transcripts and instead directly rely on the off-the-shelf OCR capabilities of the Flamingo models.
For RareAct, a zero-shot benchmark, we change the verb names to the third person, add an article before each noun and use the prompt “Caption: a person {verb + object}”.
B.1.6 Dialogue prompt
This is a conversation between a human, User, and an intelligent visual AI, Flamingo. User sends images, and Flamingo describes them.
User: <a cat image>
Flamingo: That is a cat. It’s a tiny kitten with really cute big ears.
User: <a dinner image>
Flamingo: This is a picture of a group of people having dinner. They are having a great time!
User: Can you guess what are they celebrating?
Flamingo: They might be celebrating the end of a successful project or maybe a birthday?
User: <a graph image>
Flamingo: This is a graph, it looks like a cumulative density function graph.
B.2 Additional performance results
B.2.1 Few-shot learning on classification tasks
| Model | Method | Prompt size | shots/class |
|
|
||||
| SotA | Fine-tuned | - | full | 90.9 [
|
[134](#bib.bib134)][82](#bib.bib82)][85](#bib.bib85)][136](#bib.bib136)] as well as prompt ensembling. We also observe the same trend as with the vision-language benchmarks: bigger models do better and more shots help.
We consider applying the Flamingo models to well-studied classification benchmarks like ImageNet or Kinetics700. Results are given in Table [7](#A2.T7).
We observe a similar pattern as in
other experiments:
larger model tend to perform better.
Second, given that few-shot classification tasks often come with more training examples (e.g., 1000 for ImageNet with 1 example per class), using methods to scale to larger support sets is beneficial.
RICES (Retrieval In-Context Example Selection [[136](#bib.bib136)] described in Appendix [A.2](#A1.SS2.SSS0.Px4)) performs substantially better than simply selecting examples randomly for inclusion in the prompt.
Indeed, Flamingo achieves a improvement in ImageNet classification when selecting 16 support examples out of using RICES, compared to choosing the same number of examples randomly.
Ensembling multiple prompts further boosts results.
However, note that Flamingo models underperform the current dominant contrastive paradigm for classification tasks;
in particular, they underperform the very contrastive model used as their vision encoder (see Appendix [D.1](#A4.SS1) on Flamingo’s limitations for more details).
Finally, state-of-the-art zero-shot models on ImageNet such as BASIC [[82](#bib.bib82)] and LiT [[146](#bib.bib146)] are particularly optimized on classification tasks as they are trained on JFT-3B [[145](#bib.bib145)], a dataset with images and labels.
Improving the performance of VLMs such as Flamingo on classification tasks is an interesting direction for future work.
B.2.2 Fine-tuning Flamingo as a pretrained vision-language model
To fine-tune Flamingo models on a downstream task, we train them on data batches from the task of interest in the same format as the single-image/video datasets described in Section [2.4](#S2.SS4).
Freezing and hyperparameters.
When fine-tuning Flamingo, we keep the underlying LM layers frozen and train the same Flamingo layers as during pretraining. We also increase the resolution of the input images from to . Unlike in the pretraining phase, we also fine-tune the base visual encoder, finding that this typically improves results, likely due in part to the higher input resolution.
We choose certain hyperparameters on a per-task basis by grid search on a validation subset of the training set (or on the official or standard validation set where available). These hyperparameters include the learning rate (ranging from to ) and decay schedule (exponential decay by factors of ), number of training steps, batch size (either or ), and whether visual data augmentation (color augmentation, random horizontal flips) is used.
Results.
In Table [8](#A2.T8), we present additional results for per-task Flamingo fine-tuning.
When provided access to a large-scale task-specific dataset with many thousands of examples, we find that we can improve results over our previously presented in-context few-shot learning results,
setting a new state of the art on five tasks: VQAv2, VATEX, VizWiz, MSRVTTQA, and HatefulMemes.
For example, on VQAv2, we observe improved results at , outperforming our results achieved with 32-shot in-context learning () as well as the previous state of the art (, Yan et al. [[133](#bib.bib133)]).
Although these fine-tuning results come at high computational cost relative to the previously presented in-context few-shot learning results – among other challenges like hyperparameter tuning – they further demonstrate the power of VLM pretraining for visual understanding even in the presence of large amounts of task-specific training data.
In some cases our results likely trail the state of the art due in part to the fact that we simply optimise log-likelihood and do not make use of common task-specific metric optimisation tricks, such as
CIDEr optimisation [[90](#bib.bib90), [64](#bib.bib64)] for COCO captioning, and
fine-tuning on dense annotations for VisDial [[79](#bib.bib79)].
For example, Murahari et al. [[79](#bib.bib79)] report a relative improvement in NDCG on VisDial from such dense annotation fine-tuning.
| Method |
VQAV2 |
COCO |
VATEX |
VizWiz |
MSRVTTQA |
VisDial |
YouCook2 |
TextVQA |
HatefulMemes |
||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| test-dev | test-std | test | test | test-dev | test-std | test | valid | test-std | valid | valid | test-std | test seen | |
| Flamingo - 32 shots | 67.6 | - | 113.8 | 65.1 | 49.8 | - | 31.0 | 56.8 | - | 86.8 | 36.0 | - | 70.0 |
| SimVLM [
|
[119](#bib.bib119)]
[140](#bib.bib140)]
[140](#bib.bib140)][140](#bib.bib140)][124](#bib.bib124)][153](#bib.bib153)][51](#bib.bib51)][79](#bib.bib79)][79](#bib.bib79)][132](#bib.bib132)][137](#bib.bib137)][84](#bib.bib84)][62](#bib.bib62)][133](#bib.bib133)][133](#bib.bib133)][119](#bib.bib119)][153](#bib.bib153)][65](#bib.bib65)][65](#bib.bib65)][123](#bib.bib123)][152](#bib.bib152)]B.2.3 Zero-shot performance of the pretrained contrastive model
| Flickr30K | COCO | |||||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| image-to-text | text-to-image | image-to-text | text-to-image | |||||||||
| R@1 | R@5 | R@10 | R@1 | R@5 | R@10 | R@1 | R@5 | R@10 | R@1 | R@5 | R@10 | |
|
Florence [
|
[50](#bib.bib50)]
[85](#bib.bib85)]
A crucial part of our approach is the Vision Encoder, pretrained separately using contrastive learning and kept frozen when training Flamingo models.
We report zero-shot image classification results on ImageNet, Kinetics700 and retrieval results on Flick30K and COCO.
The classification results are presented in Table [7](#A2.T7) while the retrieval results are given in Table [9](#A2.T9).
For the retrieval tasks, our model outperforms the current state-of-the-art contrastive dual encoder approaches CLIP [[85](#bib.bib85)], ALIGN [[50](#bib.bib50)] and Florence [[140](#bib.bib140)].
However, we underperform the zero-shot state-of-the-art on Kinetics700 (CLIP) and the zero-shot state-of-the-art on ImageNet (BASIC).
However, as noted earlier, BASIC [[82](#bib.bib82)] is particularly optimized for classification:
it is trained on the JFT-3B [[145](#bib.bib145)] dataset which has images with labels rather than captions.
We have noticed training on image and short text descriptions similar to labels significantly helps for ImageNet but is detrimental for retrieval benchmarks which require capturing rich scene descriptions instead.
Since our goal is to use the Vision Encoder as a feature extractor for the Flamingo models in order to capture the whole scene and not just the main object, we favor retrieval metrics over classification ones.
We provide more details about the contrastive pretraining in Appendix [B.1.3](#A2.SS1.SSS3).
B.3 Extended ablation studies
B.3.1 Flamingo
| Ablated | Flamingo 3B | Changed | Param. | Step | COCO | OKVQA | VQAv2 | MSVDQA | VATEX | Overall | |
| setting | value | value | count | time | CIDEr | top1 | top1 | top1 | CIDEr | score | |
| Flamingo 3B model (short training) | 3.2B | 1.74s | 86.5 | 42.1 | 55.8 | 36.3 | 53.4 | 70.7 | |||
| (i) | Resampler | Medium | Small | 3.1B | 1.58s | 81.1 | 40.4 | 54.1 | 36.0 | 50.2 | 67.9 |
| size | Large | 3.4B | 1.87s | 84.4 | 42.2 | 54.4 | 35.1 | 51.4 | 69.0 | ||
| (ii) | Multi-Img att. | Only last | All previous | 3.2B | 1.74s | 70.0 | 40.9 | 52.0 | 32.1 | 46.8 | 63.5 |
| (iii) | 0.5 | 0.0 | 3.2B | 1.74s | 85.0 | 41.6 | 55.2 | 36.7 | 50.6 | 69.6 | |
| 1.0 | 3.2B | 1.74s | 81.3 | 43.3 | 55.6 | 36.8 | 52.7 | 70.4 | |||
| (iv) | LM pretraining | MassiveText | C4 | 3.2B | 1.74s | 81.3 | 34.4 | 47.1 | 60.6 | 53.9 | 62.8 |
| (v) | Freezing Vision | ✓ | ✗ (random init) | 3.2B | 4.70s* | 74.5 | 41.6 | 52.7 | 31.4 | 35.8 | 61.4 |
| ✗ (pretrained) | 3.2B | 4.70s* | 83.5 | 40.6 | 55.1 | 34.6 | 50.7 | 68.1 | |||
| (vi) | Co-train LM | ✗ | ✓ (random init) | 3.2B | 5.34s* | 69.3 | 29.9 | 46.1 | 28.1 | 45.5 | 55.9 |
| on MassiveText | ✓ (pretrained) | 3.2B | 5.34s* | 83.0 | 42.5 | 53.3 | 35.1 | 51.1 | 68.6 | ||
| (vii) | Dataset | M3W+ITP+VTP | LAION400M and CLIP | 3.1B | 0.86s | 61.4 | 37.9 | 50.9 | 27.9 | 29.7 | 54.7 |
| and Vision encoder | and NFNetF6 | M3W+LAION400M+VTP and CLIP | 3.1B | 1.58s | 76.3 | 41.5 | 53.4 | 32.5 | 46.1 | 64.9 |
Ablation study experimental setup.
As in Table [10](#A2.T10), we report per-task results and the Overall score (see Section [3.3](#S3.SS3)) for Flamingo-3B on the validation subsets of the 5 dev multimodal benchmarks with 4 shots in Table [10](#A2.T10).
We perform the ablation using batch size of for M3W, for ALIGN, for LTIP and for VTP.
Models are trained for 1 million gradient steps (meaning 250,000 gradient updates, for the base model as we accumulate gradients over four datasets).
Resampler size.
We further investigate the architectural design of the Resampler in row (i) of Table [10](#A2.T10).
We ablate the size of our Resampler with three options: Small, Medium (default value for all Flamingo models), and Large.
We see that the best performance is achieved with a medium size Resampler.
Moreover, when scaled together with the frozen LM, we observed that increasing the size of the Perceiver Resampler lead to unstable training.
We thus made a conservative choice to keep the same medium Resampler size for all our Flamingo models.
Effect of how many images are cross-attended to.
In the interleaved image-text scenario, we ablate whether the model can only attend to the single most recent previous image, or to all the previous images (row (ii) of Table [10](#A2.T10)).
We can see that the single image case leads to significantly better results ( better in the overall score).
One potential explanation is that when attending to all previous images, there is no explicit way of disambiguating between different images in the cross-attention inputs.
Nonetheless, recent work has shown that such disambiguation is still possible implicitly through the causal attention mechanism [[36](#bib.bib36)].
We also explored more explicit ways to enable this while attending to all previous images by modifying the image tags to include an index (<image 1>, <image 2>, etc.) and/or learning absolute index embeddings added to the cross-attention features for each image.
These strategies were not as robust as our method when the number of images per sequence changes between training and test time.
Such a property is desirable to reduce the number of images per sequence during training for better efficiency (we use at training time) while still generalizing to many images for few-shot evaluation (we go up to at test time).
For these reasons, we keep the single image cross-attention strategy for the Flamingo models.
Note that while the model cannot explicitly attend to all previous images due to this masking strategy, it can still implicitly attend to them from the language-only self-attention that propagates all previous images’ features via the previous text tokens.
M3W image placement data augmentation.
Given a webpage, we don’t know in advance if the text of the page will mention the previous or the next image in the two-dimensional layout of the page DOM.
For this reason, we explore a data augmentation on M3W controlled by which indicates whether a given text token attends to the previous or the next image (see more details in Appendix [A.3.2](#A1.SS3.SSS2)).
The default value means that for each webpage sampled, we decide uniformly at random whether the model attends to the previous or next image.
means the model always attends to the previous image while means the model always attends to the following image.
The results (row (iii) of Table [10](#A2.T10)) show that using this randomization is beneficial.
Language model pretraining.
To measure the importance of text pretraining, we compare the performance of using a frozen decoder-only Transformer either pretrained on MassiveText (our main model) or pretrained on the C4 dataset [[87](#bib.bib87)] (row (iv) of Table [10](#A2.T10)).
Using the C4 dataset (which is smaller and less filtered than MassiveText) for training leads to a significant loss in performance ( overall).
We note that the performance notably decreases for tasks that involve more language understanding such as visual question-answering tasks (OKVQA, VQAv2 and MSVDQA) while it remains on par for tasks that do not require as much language understanding (COCO, VATEX).
This highlights the importance of pretraining the LM on a high-quality text-only dataset.
Freezing the vision encoder.
During Flamingo training, we freeze the pretrained components (Vision Encoder and LM layers) while training newly added components from scratch.
We ablate in (v) of Table [10](#A2.T10) this freezing decision by training the Vision Encoder weights either from scratch or initialized with the contrastive vision-language task.
If trained from scratch, we observe that the performance decreases by a large margin of .
Starting from pretrained weights still leads to a drop in performance of while also increasing the compute cost of the training.
Alternative to freezing the LM by co-training on MassiveText.
Another approach for preventing catastrophic forgetting is to co-train on MassiveText [[86](#bib.bib86)], the dataset that was used to pretrain the language model.
Specifically, we add MassiveText to the training mixture, with a weight of (best performing after a small grid search), using a sequence length of and the exact same setting as the pretraining of Chinchilla [[42](#bib.bib42)] for computing the text-only training loss.
In order to co-train on MassiveText, we need to unfreeze the language model but we keep the vision encoder frozen.
We perform two ablations in row (vi) of Table [10](#A2.T10): starting from a pretrained language model (with a learning rate multiplier of of the LM weights) versus initializing from scratch (with the same learning rate everywhere).
In both cases, the overall scores are worse than our baseline which starts from the language model, pretrained on MassiveText, and is kept frozen throughout training.
This indicates that the strategy of freezing the language model to avoid catastrophic forgetting is beneficial.
Even more importantly, freezing the LM is computationally cheaper as no gradient updates of the LM weights are required and we do not need to train on an additional dataset.
This computational argument is even more relevant for our largest model, Flamingo-80B, where we freeze almost of the overall weights.
Additional experiments using the LAION400M dataset.
B.3.2 Dataset mixing strategies for the contrastive pretraining
| Dataset | Combination | ImageNet | COCO | |||||
|---|---|---|---|---|---|---|---|---|
| strategy | accuracy | image-to-text | text-to-image | |||||
| top-1 | R@1 | R@5 | R@10 | R@1 | R@5 | R@10 | ||
| LTIP | None | 40.8 | 38.6 | 66.4 | 76.4 | 31.1 | 57.4 | 68.4 |
| ALIGN | None | 35.2 | 32.2 | 58.9 | 70.6 | 23.7 | 47.7 | 59.4 |
| LTIP + ALIGN | Accumulation | 45.6 | 42.3 | 68.3 | 78.4 | 31.5 | 58.3 | 69.0 |
| LTIP + ALIGN | Data merged | 38.6 | 36.9 | 65.8 | 76.5 | 15.2 | 40.8 | 55.7 |
| LTIP + ALIGN | Round-robin | 41.2 | 40.1 | 66.7 | 77.6 | 29.2 | 55.1 | 66.6 |
One key to achieving strong results was the inclusion of our new dataset LTIP alongside ALIGN for training. Despite being a smaller dataset ALIGN by a factor of 6, a contrastive model trained on only LTIP outperforms one trained only on ALIGN on our evaluation metrics, suggesting that dataset quality may be more important than scale in the regimes in which we operate. We also find that a model trained on both ALIGN and LTIP outperforms those trained on the two datasets individually and that how the datasets are combined is important.
To demonstrate this, we train a small model with an NFNet-F0 vision encoder, BERT-mini language encoder and batch size 2048 for 1 million gradient-calculation steps on ALIGN, LTIP and a mixture of the two. The results are presented in Table [11](#A2.T11). It shows the results of training models on the combined datasets using three different merging regimes:
-
•
Data merged: Batches are constructed by merging examples from each dataset into one batch.
-
•
Round-robin: We alternate batches of each dataset, updating the parameters on each batch.
-
•
Accumulation: We compute a gradient on a batch from each dataset. These gradients are then weighted and summed and use to update the parameters.
Across all evaluation metrics, we find that the Accumulation method outperforms other methods of combining the datasets. Although the LTIP dataset is 5 smaller than the ALIGN dataset, this ablation study suggests that the quality of the training data can be more important than its abundance.
Appendix C Qualitative results
In addition to the samples in Figure [1](#S0.F1),
in this section we provide selected samples covering different interaction modalities in Figures [10](#A3.F10), [11](#A3.F11), and [12](#A3.F12). Unlike the quantitative benchmark results which use beam search with a beam width of 3 for decoding, all qualitative results presented in this section use greedy decoding for faster sampling.
Figure [10](#A3.F10) shows the simplest form of interaction where a single image is provided followed by a text prompt either in the form of a question or the start of a caption.
Even though the model is not trained specifically for the question and answer format, the capabilities of the pretrained language model allows this adaptation.
In many of these examples, Flamingo can do at least one step of implicit inference. Some of the objects are not named in the prompt but their properties are queried directly. Based on its visual input, the model manages to recall the knowledge relevant to the referred object and thus produces the correct answer.
Vision networks trained contrastively have been shown to learn character recognition capabilities [[85](#bib.bib85)]. We observe that Flamingo preserves this capability in the full model, in some cases for text that is rather small with respect to the size of the image.
Since our model can accept inputs in the form of arbitrary sequences of visuals and language, we test its abilities to hold an extended dialogue with interleaved images and text. Figure [11](#A3.F11) shows some samples which are generated by prompting the model with a brief dialogue (Appendix [B.1.6](#A2.SS1.SSS6)) followed by user interaction including image insertions. Even after several rounds of interaction Flamingo can still successfully attend to the image and reply to questions that can not be guessed by language alone. We observe that multiple images can be separately attended: simple comparisons and inferences are handled properly.
Lastly, we investigated similar capabilities with video inputs as they present some extra challenges compared to images. Figure [12](#A3.F12) shows some selected samples. As seen in the figure, in some cases Flamingo can successfully integrate information from multiple frames (e.g., videos scanning through a scene or text) and answer questions involving temporal understanding (e.g., in the last example, with the word “after”).
|
|
|
|
|
|
|
|
|
|
[B.1.6](#A2.SS1.SSS6)) containing a dialogue with 3 corresponding images, but it is not fine-tuned for dialogue in any other way.
Appendix D Discussion
D.1 Limitations, failure cases and opportunities
Here, we describe some limitations and failure cases of our models, as well as opportunities for further improving our models and extending their abilities.
Classification performance.
Although our visual language models have important advantages over contrastive models (e.g., few-shot learning and open-ended generation capabilities), their performance lags behind that of contrastive models on classification tasks.
We believe this is because the contrastive training objective directly optimizes for text-image retrieval, and in practice, the evaluation procedure for classification can be thought of as a special case of image-to-text retrieval [[85](#bib.bib85)]. This is not the case for the language modeling objective we use to train our visual language models
and this may contribute to the observed performance gap on classification tasks.
In particular, Zhao et al. [[148](#bib.bib148)] have shown that language models suffer from various biases arising from the training data distribution, the set of samples used in the prompt, and their order.
They also show that such issues can be mitigated with calibration techniques,
provided one can assume a certain prior distribution (e.g., uniform) over the label space.
This assumption doesn’t hold in general, and further research is needed to develop techniques to address these issues in the few-shot setting.
More generally, seeking objectives, architectures, or evaluation procedures that could bridge the gap between these two classes of models is a promising research direction.
Legacies of language models.
Our models build on powerful pretrained causal language models, and as a side effect, directly inherit their weaknesses.
For instance, causal modeling of the conditioning inputs is strictly less expressive than bidirectional modeling.
In this direction, recent work has shown that non-causal masked language modeling adaptation [[120](#bib.bib120)] followed by multitask fine-tuning [[95](#bib.bib95), [125](#bib.bib125), [131](#bib.bib131)] can efficiently improve the zero-shot performance of causal decoder-only language models.
Furthermore, transformer-based language models tend to generalize poorly to test sequences significantly longer than the training ones [[83](#bib.bib83)].
In settings where the expected text output is too long, the ability of the models to leverage enough shots for few-shot learning can be affected.
For instance, for the VisDial dataset [[20](#bib.bib20)], a single shot consists of an image followed by a long dialogue composed of 21 different sentences.
A sequence of 32 VisDial shots is thus composed of at least sentences, which in practice means that the prompt length ranges from to tokens.
This is significantly longer than the maximum sequence length () our LMs have been trained on [[42](#bib.bib42)].
To this end, we have capped our reported results on VisDial at 16 shots.
On another note, while our ablations demonstrate the importance of the language model priors inherited from frozen language models, we suspect that they may play a role in occasional hallucinations and ungrounded guesses observed in open-ended dialogue settings. We provide and analyze examples of such behaviours in Figure [13](#A4.F13).
Finally, language modeling suffers from poor sample efficiency during pretraining [[11](#bib.bib11)].
Mitigating this issue has the potential to greatly accelerate progress in the field,
by improving turnaround of large-scale training runs and in turn increasing the feasibility of more systematic exploration of design decisions at larger scales.
Further discussion on typical weaknesses observed for large LMs can be found in [[11](#bib.bib11), [86](#bib.bib86)].
Trade-offs of few-shot learning methods.
In the paper, we use in-context learning as our “go-to” few-shot learning method (see Section [2.5](#S2.SS5)).
This method has notable advantages over gradient-based approaches such as fine-tuning.
Indeed, in-context learning requires almost no hyperparameter tuning, works reasonably well in the very low data regime (dozens of examples), and only requires inference, simplifying deployment.
In contrast, gradient-based approaches require carefully tuned design choices to avoid overfitting (either by proper learning rate schedule or architecture design [[43](#bib.bib43)]) and often need more data (thousands) to work well.
This motivated our focus on in-context learning;
however, this approach also has drawbacks we discuss next.
Inference compute cost.
The compute cost of in-context learning with transformer models scales linearly with the number of shots if one can reuse the few-shot prompt for multiple query samples (by caching the keys and values) and quadratically otherwise.
In contrast, gradient-based few-shot learning approaches [[43](#bib.bib43)] have constant complexity with respect to the number of shots during inference.
Prompt sensitivity.
In-context learning has also been shown to be disconcertingly sensitive to various aspects of the demonstrations, such as the order of the samples [[148](#bib.bib148)] or their format.
Leveraging more shots.
When using in-context learning, performance plateaus rapidly as the number of few-shot samples increases beyond 32.
This proves a striking contrast with typical gradient-based methods, for which the amount of correctly paired training data is a critical factor for performance.
We note that RICES (Retrieval In-Context Example Selection [[136](#bib.bib136)] described in Appendix [A.2](#A1.SS2)) effectively mitigates this issue for classification tasks (Appendix [B.2.1](#A2.SS2.SSS1)), but still faces similar issues beyond a small number of example per class.
Task location.
Recent work on understanding what makes in-context learning effective sheds some light on a possible explanation for why more shots do not always help [[92](#bib.bib92), [76](#bib.bib76)].
In more detail, Brown et al. [[11](#bib.bib11)] raise the question of whether in-context learning actually “learns” new tasks at inference time based on the provided input-output mappings, or simply recognizes and identifies tasks learned during training. On this question, the findings of Reynolds and McDonell [[92](#bib.bib92)] suggest that the latter is the key driver of performance across diverse settings, and refer it as task location.
Similarly, Min et al. [[76](#bib.bib76)] show that the mapping from input to output generally has limited impact on few-shot performance, as opposed to specifying the overall format of the examples.
In line with these findings, we also observe non-trivial zero-shot performance using prompt without any images, hence also highlighting that the format of the task matters significantly.
Intuitively, a handful of samples may often be enough to perform task location well, but the model may generally not be able to leverage further samples at inference time to refine its behaviour.
In summary, there is no “golden” few-shot method that would work well in all scenarios. In particular, the best choice of few-shot learning approach strongly depends on characteristics of the application, an important one being the number of annotated samples. On this point, in our work, we demonstrate that in-context learning is highly effective in the data-starved regime (32 samples or fewer). There may be opportunities to combine different methods to leverage their complementary benefits, in particular when targeting less data-constrained data regimes (e.g., hundreds of samples).
Extending the visual and text interface.
Natural language is a powerful and versatile input/output interface to provide descriptions of visual tasks to the model and generate outputs or estimate conditional likelihoods over possible outputs. However, it may be a cumbersome interface for tasks that involve conditioning on or predicting more structured outputs such as bounding boxes (or their temporal and spatio-temporal counterparts); as well as making spatially (or temporally and spatio-temporally) dense predictions. Furthermore, some vision tasks, such as predicting optical flow, involve predicting in continuous space, which is not something our model is designed to handle out of the box. Finally, one may consider additional modalities besides vision that may be complementary, such as audio. All of these directions have the potential to extend the range of tasks that our models can handle; and even improve performance on the ones we focus on, thanks to synergies between the corresponding abilities.
Scaling laws for vision-language models.
In this work, we scale Flamingo models up to 80B parameters and provide some initial insights on their scaling behaviour across evaluation benchmarks, summarized in Figure [2](#S0.F2).
In the language space, an important line of work has focused on establishing scaling laws for language models [[53](#bib.bib53), [42](#bib.bib42)].
In the vision domain, Zhai et al. [[145](#bib.bib145)] take a step in this direction.
Similar efforts have yet to be made for vision-language models, including contrastive models, as well as visual language models such as the ones we propose.
While language modeling scaling law research has focused on perplexity as the golden metric, we speculate that it may be more directly useful for our purposes
to establish such trends in terms of aggregate downstream evaluation task performance.
D.2 Benefits, risks and mitigation strategies
D.2.1 Benefits
Accessibility.
A system like Flamingo offers a number of potential societal benefits, some of which we will discuss in this section.
Broadly, the fact that Flamingo is capable of task generalisation makes it suitable for use cases that have not been the focus of vision research historically.
Typical vision systems are trained to solve a particular problem by training on large databases of manually annotated task-specific examples, making them poorly suited for applications outside of the narrow use cases for which they were deliberately trained.
On the other hand, Flamingo is trained in a minimally constrained setting, endowing it with strong few-shot task induction capabilities.
As we’ve shown in our qualitative examples (Appendix [C](#A3)), Flamingo can also be used through a “chat”-like interface for open-ended dialogue.
Such capabilities could enable non-expert end users to apply models like Flamingo even to low-resource problems for which little to no task-specific training data has been collected, and where queries might be posed in a variety of formats and writing styles.
In this direction, we have shown that Flamingo achieves strong performance on the VizWiz challenge111[https://vizwiz.org/](https://vizwiz.org/), which promotes visual recognition technologies to assist visually impaired people.
A dialogue interface could also promote better understanding and interpretability of visual language models.
It could help highlight issues with bias, fairness, and toxicity the model may pick up on from the training data.
Overall, we believe that Flamingo represents an important step towards making state-of-the-art visual recognition technology more broadly accessible and useful for many diverse applications.
Model recycling.
From a modeling perspective, although Flamingo is computationally expensive to train, it importantly leverages pretrained frozen language models and visual encoders. We demonstrated that new modalities can be introduced into frozen models, thereby avoiding expensive retraining.
As such models continue to grow in size and computational demands, “recycling” them will become increasingly important from an environmental perspective (as well as a practical one), as
described in Larochelle [[55](#bib.bib55)] and
explored in Strubell et al. [[105](#bib.bib105)] for language models.
We hope such results may inspire further research into how existing models can be repurposed efficiently rather than trained from scratch.
D.2.2 Risks and mitigation strategies
This section provides some early investigations of the potential risks of models like Flamingo.
This study is preliminary and we foresee that further research efforts should be undertaken to better assess those risks.
We also discuss potential mitigation strategies towards safely deploying these models.
Note that as explained in our Model Card [[77](#bib.bib77)] in Appendix [E](#A5), this model was developed for research purposes only and should not be used in specific applications before proper risk analyses are conducted and mitigation strategies are explored.
By construction, Flamingo inherits the risks of Large LMs.
Recall that a large part of our model is obtained by freezing the weights of an existing language model [[42](#bib.bib42)].
In particular, if provided with no images Flamingo falls back to language model behavior.
As such Flamingo is exposed to the same risks of large language models: it can output potentially offensive language, propagate social biases and stereotypes, as well as leaking private information [[126](#bib.bib126)].
In particular, we refer to the analysis presented in the Chinchilla paper (Hoffmann et al. [[42](#bib.bib42)], Section 4.2.7) in terms of gender bias on the Winogender dataset [[93](#bib.bib93)] which demonstrate that even though this model is less biased towards gender than previous models [[86](#bib.bib86)], gender biases are still present.
In terms of unprompted toxicity, we also refer to the analysis from Chinchilla [[42](#bib.bib42)] which highlights that overall the propensity of the model to produce toxic outputs when not prompted to do so is rather low, as measured by computing the PerspectiveAPI toxicity score on 25,000 samples.
Weidinger et al. [[126](#bib.bib126)] detail possible long-term mitigation strategies for these risks.
They include social or public policy interventions, such as the creation of regulatory frameworks and guidelines; careful product design, for instance relating to user interface decisions; and research at the intersection between AI Ethics and NLP, such as building better benchmarks and improving mitigation strategies.
In the short term, effective approaches include relying on prompting to mitigate any biases and harmful outputs [[86](#bib.bib86)].
Next, we explore the additional risks incurred by Flamingo’s additional visual input capabilities.
| CIDEr difference | CIDER | ||
| female - male = | darker - lighter = | overall | |
| AoANet [
|
[61](#bib.bib61)]
[147](#bib.bib147)].
Gender and racial biases when prompted with images.
Previous work has studied biases that exist in captioning systems [[37](#bib.bib37), [147](#bib.bib147)].
Such modeling biases can result in real-world harms if deployed without care.
For AI systems to be useful to society as a whole, their performance should not depend on the perceived skin tone or gender of the subjects – they should work equally well for all populations.
However, current automatic vision system performance has been reported to vary with race, gender or when applied across different demographics and geographic regions [[12](#bib.bib12), [21](#bib.bib21), [97](#bib.bib97)].
As a preliminary study assessing how Flamingo’s performance varies between populations, we follow the study proposed in Zhao et al. [[147](#bib.bib147)] and report how the captioning performance of our model varies on COCO as a function of gender and race.
Note that we use a different evaluation protocol from the one proposed by Zhao et al. [[147](#bib.bib147)]; in that work, they measure results across 5 pretrained models and compute confidence intervals across aggregated per-model scores.
Here, we have just one copy of our model (due to its high training cost), and we instead perform statistical tests on the per-sample CIDEr scores across the splits from Zhao et al. [[147](#bib.bib147)].
We report the results in Table [12](#A4.T12).
Overall, when comparing the CIDEr scores aggregated among images labeled as female versus male, as well as when comparing darker skin versus lighter skin, we find there are no statistically significant differences in the per-sample CIDEr scores. To compare the two sets of samples, we use a two-tailed -test with unequal variance, and among the four comparisons considered, the lowest -value we find is , well above typical statistical significance thresholds (e.g. a common rejection threshold might be ). This implies that the differences in scores are indistinguishable from random variation under the null hypothesis that the mean scores are equal. We note that a failure to reject the null hypothesis and demonstrate a significant difference does not imply that there are no significant differences; it is possible that a difference exists that could be demonstrated with larger sample sizes, for example. However, these preliminary results are nonetheless encouraging.
Toxicity when prompted with images.
We also evaluate the toxicity of Flamingo using the Perspective API222 [https://perspectiveapi.com/](https://perspectiveapi.com/) to evaluate the toxicity of the model’s generated captions when prompted with images from the COCO test set.
We observe that some captions are labelled as potentially toxic by the classifier;
however, when examining them manually, we do not observe any clear toxicity – output captions are appropriate for the images provided.
Overall, based on our own experiences interacting with the system throughout the course of the project, we have not observed toxic outputs when given “safe-for-work” imagery.
However this does not mean the model is incapable of producing toxic outputs, especially if probed with “not-safe-for-work” images and/or toxic text.
A more thorough exploration and study would be needed if such a model were put in production.
Applying Flamingo for mitigation strategies.
Thanks to its ability to rapidly adapt in low-resource settings, Flamingo could itself be applied in addressing some of the issues described above.
For instance, following Thoppilan et al. [[111](#bib.bib111)], adequately conditioned or fine-tuned Flamingo models could be used for filtering purposes of toxic or harmful samples in the training data.
In their work, they observe significant improvements relating to safety and quality when fine-tuning on the resulting data.
Furthermore, during evaluation, such adapted models could be used to down-rank or exclude outputs that might be classified as offensive, promoting social biases and stereotypes or leaking private information, thus accelerating progress in this direction even for low-resource tasks.
Our results on the HatefulMemes benchmark represent a promising step in this direction.
Recent work in the language modeling space has also shown success in training an LM to play the role of a “red team” and generate test cases, so as to automatically find cases where another target LM behaves in a harmful way [[81](#bib.bib81)].
A similar approach could be derived for our setting.
Enabling the model to support outputs with reference to particular locations within the visual inputs, or to external verified quotes is also an interesting direction [[72](#bib.bib72), [111](#bib.bib111)].
Finally, in Figure [11](#A3.F11), we provide qualitative examples demonstrating that Flamingo can explain its own outputs, suggesting avenues to explainability and interpretability using the model’s text interface.
Appendix E Flamingo Model Card
We present a model card for Flamingo in Table LABEL:tab:model-card, following the framework presented by Mitchell et al. [[77](#bib.bib77)].
[77](#bib.bib77)].
| Model Details | |
| Model Date | March 2022 |
| Model Type |
Transformer-based autoregressive language model, conditioned on visual features from a convnet-based encoder. Additional transformer-based cross-attention layers incorporate vision features into the language model’s text predictions.
(See Section
|
[42](#bib.bib42),[86](#bib.bib86)] for the language only component of this work. We refer to our study presented in Appendix[D.2.2](#A4.SS2.SSS2)for a toxicity analysis when the model is conditioned on an image.[B.1.4](#A2.SS1.SSS4)spanning various vision and language tasks such as classification (ImageNet, Kinetics700, HatefulMemes), image and video captioning (COCO, VATEX, Flickr30K, YouCook2, RareAct), visual question answering (OKVQA, VizWiz, TextVQA, VQAv2, MSRVTTQA, MSVDQA, iVQA, STAR, NextQA) and visual dialog (VisDiag). This was tested either in an open ended setting where Flamingo generate language and we compare the outputs with the ground truth or in a close ended setting where we directly score various outcomes using the likelihood of the model.[6](#A2.T6)for a detailed list.[50](#bib.bib50)], the Datasheet in Appendix[F.1](#A6.SS1), Appendix[F.2.1](#A6.SS2.SSS1), Appendix[F.2.2](#A6.SS2.SSS2)[3](#S3)for the full details of our quantitative study.[86](#bib.bib86)]. More work is needed on mitigation approaches to toxic content and other types of risks associated with language models, such as those discussed in Weidinger et al. [[126](#bib.bib126)].[126](#bib.bib126)].[126](#bib.bib126)].Appendix F Datasheets
F.1 M3W dataset
We follow the framework defined by Gebru et al. [[30](#bib.bib30)] and provide the datasheet for M3W in Table LABEL:tab:m3w-datasheet.
[30](#bib.bib30)].
| Motivation | |
| For what purpose was the dataset created? Who created the dataset? Who funded the creation of the dataset? | The dataset was created for pre-training vision-language models and was created by researchers and engineers. |
| Any other comments? | None. |
| Composition | |
| What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? | All instances of the dataset are documents from the web containing interleaved text and images. |
| How many instances are there in total (of each type, if appropriate)? | There are 43.3M instances (documents) in total, with a total of 185M images and 182 GB of text. |
| Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set? | The dataset is a sample from a larger set. |
| What data does each instance consist of? |
Each instance is made up of a sequence of UTF-8 bytes encoding the document’s text, as well as a sequence of integers indicating the positions of images in the text, and the images themselves in compressed format (see Section
|
[A.3.1](#A1.SS3.SSS1).F.2 Image and video text pair datasets
F.2.1 Datasheet for LTIP
[30](#bib.bib30)].
| Motivation | |
| For what purpose was the dataset created? Who created the dataset? Who funded the creation of the dataset? | The dataset was created for pre-training vision-language models and was created by researchers and engineers. |
| Any other comments? | None. |
| Composition | |
| What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? | All instances of the dataset are image-text pairs. |
| How many instances are there in total (of each type, if appropriate)? | The dataset contains 312M image-text pairs. |
| Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set? | The dataset is a sample from a larger set. |
| What data does each instance consist of? |
Each instance is made up of a sequence of UTF-8 bytes encoding the document’s text, and an image in compressed format (see Appendix
|
F.2.2 Datasheet for VTP
[30](#bib.bib30)].
| Motivation | |
| For what purpose was the dataset created? Who created the dataset? Who funded the creation of the dataset? | The dataset was created for pre-training vision-language models and was created by researchers and engineers. |
| Any other comments? | None. |
| Composition | |
| What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? | All instances of the dataset are video-text pairs. |
| How many instances are there in total (of each type, if appropriate)? | The dataset contains 27M video-text pairs. |
| Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set? | The dataset is a sample from a larger set. |
| What data does each instance consist of? |
Each instance is made up of a sequence of UTF-8 bytes encoding the document’s text, and a video in compressed format (see Appendix
|
Appendix G Credit for visual content
-
•
Figure
[1](#S0.F1):-
–
Row 1: All images are provided under license by Unsplash.
-
–
Row 2: All images are under the public domain.
-
–
Row 3: First two images are provided under license by Unsplash.
-
–
Row 5: Available from DALL·E 2 [
[89](#bib.bib89)]. -
–
Row 6: First two are provided under license by Unsplash, the third one is provided by Wikimedia Commons, licensed under CC BY-ND 2.0.
-
–
Row 7: The images are provided by Wikimedia Commons, licensed under CC BY-ND 2.0.
-
–
Row 8: The images are provided by Wikimedia Commons, licensed under CC BY-ND 2.0.
-
–
Row 9: This video is from YFCC100M, licensed under CC BY-ND 2.0.
-
–
Dialogue 1: Available from DALL·E 2 [
[89](#bib.bib89)]. -
–
Dialogue 2: The first icon is provided under license by Flaticon, the second image is provided under license by Unsplash, the third one is provided under license by Sketchfab.
-
–
Dialogue 3: Available from CLIP [
[85](#bib.bib85)]. -
–
Dialogue 4: Chicago and Tokyo pictures obtained from Unsplash.
-
–
- •
- •