# Source: https://lilianweng.github.io/posts/2023-09-06-lmm/
# Author: Lilian Weng
# Author Slug: lilian-weng
# Fetched via: search fallback (Perplexity)
# Downloaded: 2026-04-06
# Words: 2178
This post aims to review recent developments in how to effectively use test-time compute (i.e. “thinking time”) and why it helps.

1. 1 Introduction
2. 2 Related Work
3. 3 Method 1. 3.1 Visual Feature Extraction
   2. 3.2 Long-term Temporal Modeling
   3. 3.3 Text Decoding
4. 4 Experiments 1. 4.1 Tasks and Datasets
   2. 4.2 Implementation Details
   3. 4.3 Main Results
   4. 4.4 Ablation Studies
   5. 4.5 Visualization
5. 5 Conclusion
6. A Additional Experiments
7. B More Qualitative Results
8. C Relations to Concurrent Works
9. D Experiment Details
10. E Limitation and Future Work

…

###### Abstract
With the success of large language models (LLMs), integrating the vision model into LLMs to build vision-language foundation models has gained much more interest recently. However, existing LLM-based large multimodal models (*e.g*., Video-LLaMA, VideoChat) can only take in a limited number of frames for short video understanding.
In this study, we mainly focus on designing an efficient and effective model for long-term video understanding. Instead of trying to process more frames simultaneously like most existing work, we propose to process videos in an online manner and store past video information in a memory bank. This allows our model to reference historical video content for long-term analysis without exceeding LLMs’ context length constraints or GPU memory limits.
Our memory bank can be seamlessly integrated into current multimodal LLMs in an off-the-shelf manner. We conduct extensive experiments on various video understanding tasks, such as long-video understanding, video question answering, and video captioning, and our model can achieve state-of-the-art performances across multiple datasets.

## 1 Introduction
Large language models (LLMs) have gained significant popularity in the natural language processing field.
By pre-training on large-scaled textual data, LLMs (*e.g*. GPT [1, 2, 3, 4], LLaMA [5, 6]) have demonstrated remarkable abilities to perform both generative and discriminative tasks with a unified framework.
Recently, there has been a growing interest in utilizing LLMs on multimodal tasks. By integrating LLMs with visual encoders, they can take images and videos as input and show incredible capabilities in various visual understanding tasks, such as captioning, question answering [7, 8, 9, 10, 11, 12, 13], classification, detection, and segmentation [14, 15, 16, 17, 18, 19, 20].
To handle video inputs, some prior large multimodal models [7, 9] directly feed the concatenated query embeddings of each frame along the temporal axis into LLMs. However, the inherent context length limitation of LLMs and GPU memory consumption restrict the number of video frames that can be processed. For example, LLaMA has a context length limitation of 2048 while large multimodal models like LLaVA [8] and BLIP-2 [7, 9] take in 256 and 32 tokens per image respectively.

…

With these in mind, we introduce a Memory-Augmented Large Multimodal Model (MA-LMM), aiming for efficient and effective long-term video modeling. MA-LMM adopts a structure similar to existing large multimodal models [7, 9, 12], which comprise a visual encoder to extract visual features, a querying transformer to align the visual and text embedding spaces, and a large language model.
As illustrated in Figure 1(a), as opposed to directly feeding visual encoder outputs to the querying transformer, we opt for an online processing approach that takes video frames sequentially and stores the video features in the proposed long-term memory bank. This strategy of sequentially processing video frames and leveraging a memory bank significantly reduces the GPU memory footprint for long video sequences.
It also effectively addresses the constraints posed by the limited context length in LLMs as demonstrated in Figure 1(b). Our design provides a solution for long-term video understanding with large multimodal models with great advantages over prior approaches [7, 9, 12, 21, 13] which consume huge GPU memory and require a large number of input text tokens.
The core contribution of our approach is the introduction of a long-term memory bank that captures and aggregates historical video information.
Specifically, the memory bank aggregates past video features in an auto-regressive manner, which can be referenced during subsequent video sequence processing.
Also, our memory bank is designed to be compatible with the Q-Former, where it acts as the key and value in the attention operation for long-term temporal modeling.
As a result, it can be seamlessly integrated into existing large multimodal models in an off-the-shelf manner to enable long-term video modeling ability.
To further enhance efficiency, we propose a memory bank compression method that maintains the length of the memory bank constant relative to the input video length. By selecting and averaging the most similar adjacent frame features, it can preserve all the temporal information while significantly reducing the temporal redundancies in long videos.
We summarize our main contributions as follows:

- •

  We introduce a novel long-term memory bank design to enhance existing large multimodal models, equipping them with long-term video modeling capability.
- •

  Our model significantly reduces the GPU memory usage and addresses LLMs’ context length limitations by processing video sequences in an online fashion.
- •

  Our approach has achieved new state-of-the-art performances on various downstreaming video tasks, including long-term video understanding, video question answering, and video captioning.

…

Flamingo [22] proposes to connect powerful pre-trained vision-only and language-only models and achieve state-of-the-art performance in few-shot learning tasks. BLIP-2 [7] introduces a lightweight querying transformer to bridge the modality gap between the frozen pre-trained image encoder and frozen LLMs. Despite having significantly fewer trainable parameters, it performs well on various multimodal tasks.
LLaVA [8] employs a simple linear layer to project image features into the text embedding space and efficiently finetunes LLMs [23] for better performance. Building upon BLIP-2, MiniGPT-4 [10] collects a large-scale high-quality dataset of image-text pairs and achieves better language generation ability. VisionLLM [15] leverages the reasoning and parsing capacities of LLMs, producing strong performance on multiple fine-grained object-level and coarse-grained reasoning tasks.

…

Based on this motivation, Video-LLaMA [12] enhances BLIP-2 structure by adding an additional video querying transformer to explicitly model the temporal relationship. Similarly, building on LLaVA [8], Video-ChatGPT [21] simply average pools the frame-level features across spatial and temporal dimensions to generate video-level representation.
VideoChat [13] utilizes perception models to generate action and object annotations, which are then forwarded to LLMs for further reasoning. Despite the advancements, these models are primarily designed for short videos. Inspired by the Token Merging [24] which averages highly similar tokens to reduce the computation cost, we propose an extension of this idea to video data, specifically along the temporal axis.

…

## 3 Method
We introduce MA-LMM, a memory-augmented large multimodal model for long-term video understanding.
Instead of processing more frames simultaneously as most video understanding methods [42, 31, 43, 44, 45, 46, 47, 48, 49], we propose to auto-regressively process video frames in an online manner, which draws inspiration from the online processing fashion with long-term memory design presented in MeMViT [41].
Figure 2(a) illustrates the overview of our MA-LMM framework. Following similar practices of large multimodal models [7, 9, 8, 12], the overall model architecture can be divided into three parts: (1) visual feature extraction with a frozen visual encoder (Sec. 3.1), (2) long-term temporal modeling with a trainable querying transformer (Q-Former) to align the visual and text embedding spaces (Sec. 3.2), and (3) text decoding with a frozen large language model (Sec. 3.3).

### 3.1 Visual Feature Extraction
This design draws inspiration from the cognitive processes humans use to handle long-term visual information. Instead of concurrently processing extensive duration of signals, humans process them in a sequential manner, correlate current visual inputs with past memories for comprehension, and selectively retain salient information for subsequent reference [41]. Similarly, our MA-LMM processes video frames sequentially, dynamically associating new frame input with historical data stored in the long-term memory bank, ensuring that only discriminative information is conserved for later use. This selective retention facilitates a more sustainable and efficient approach to video understanding, which further allows the model to automatically support online video reasoning tasks.
Formally, given a sequence of T video frames, we pass each video frame into a pre-trained visual encoder and obtain the visual features V=[v_{1},v_{2},..,v_{T}],v_{t}\in\mathbb{R}^{P\times C}, where P is the number of patches for each frame and C is the channel dimension for the extracted frame feature. Then we inject temporal ordering information into the frame-level features by a position embedding layer (PE) as

…

In our experiments, Q-Former outputs 32 tokens for each image, which is more efficient than 256 tokens produced by LLaVA [8]. Each Q-Former block consists of two attention submodules: (1) cross-attention layer, which interacts with the raw visual embedding extracted from the frozen visual encoder, and (2) self-attention layer, which models interactions within the input queries.
Different from the original Q-Former in BLIP-2 that only attends to the current frame’s embedding, we design a long-term memory bank consisting of the visual memory bank and the query memory bank, which accumulates the past video information and augments the input to cross- and self-attention layers for effective long-term video understanding.
Visual Memory Bank. The visual memory bank stores the raw visual features of each frame extracted from the frozen visual encoder. Specifically, for the current time step t, the visual memory bank contains the concatenated list of past visual features F_{t}=\texttt{Concat}[f_{1},f_{2},..,f_{t}],F_{t}\in\mathbb{R}^{tP\times C}. Given the input query z_{t}, the visual memory bank acts as the key and value as:

…

Query Memory Bank. Different from the fixed visual memory bank which stores the raw and static visual features, the query memory bank accumulates input queries of each timestep, represented as Z_{t}=\texttt{Concat}[z_{1},z_{2},..,z_{t}],Z_{t}\in\mathbb{R}^{tN\times C}. By storing these queries, we maintain a dynamic memory of the model’s understanding and processing of each frame up to the current timestep via the Q-Former. The query memory bank also acts as key and value as:

…

similar to the Eq 2. Then we apply the same attention operation as Eq. 3. At each time step, z_{t} contains the learned important information specifically for each video till the current timestep t. Different from the static visual memory bank, the input queries z_{t} evolve through cascaded Q-Former blocks during the model training, capturing distinct video concepts and patterns at increasing levels of abstraction. As a result, each self-attention layer has a unique query memory bank, where the contained input queries are updated during the training time.

…

### 3.3 Text Decoding

As we process video frames in an auto-regressive manner, the Q-Former output at the final timestep contains all historical information, which is then fed into the LLM.
Therefore, we can significantly reduce the number of input text tokens from N*T to N, addressing the context length limitation of the current LLMs and substantially easing the GPU memory requirements. During training, given a labeled dataset consisting of video and text pairs, our model is supervised with the standard cross entropy loss as:
| |\mathcal{L}=-\frac{1}{S}\sum_{i=1}^{S}\log P(w_{i}|w_{<i},V).| |(8)|
|--|--|--|--|

in which V represents the input video, and w_{i} is the i-th ground-truth text token. During training, we update the parameters of the Q-Former while keeping the weights of both the visual encoder and the language model frozen.

…

### 4.2 Implementation Details

For the visual encoder, we adopt the pre-trained image encoder ViT-G/14 [71] from EVA-CLIP [72], it can be further changed to other clip-based video encoders. We use the pre-trained Q-Former weights from InstructBLIP [9] and adopt Vicuna-7B [73] as the LLM. All the experiments are conducted on 4 A100 GPUs. More details about training and evaluation are described in the supplementary material.

…

This results in significant improvement in most tasks, enhancing the average top-1 accuracy by 3.8% compared to the S5 [36] model. Unlike previous video-based models which process all video frames simultaneously in an offline manner and predict probabilities for each class, our MA-LMM processes video frames in an online fashion and directly outputs the text label for each class type.

…

Video Captioning. To further evaluate the capabilities of our MA-LMM in generating free-form text, we conduct experiments on the standard video captioning datasets including MSRVTT [66], MSVD [67] and YouCook2 [68] in Table 4. Although these datasets only consist of videos with short duration and our model is initially pre-trained merely on image-text dataset pairs, our MA-LMM exhibits outstanding performances across all the metrics.

div

## 🧠 What is LMLM?
Neural language models entangle language and knowledge, making it hard to verify, update, or forget facts.
**Large Memory Language Models (LMLMs)** address this by combining:
- **Internal memory** (parameters) for fluency and reasoning
- **External memory** (database) for accurate, editable knowledge
This enables:
- Improved perplexity during pretraining
- Higher factual accuracy, without sacrificing general language understanding
- Instant editing or forgetting of specific facts via database updates
## Table of Contents
- Quick Start
...
We provide a custom Hugging Face model class `LlamaForLMLM` with a built-in `generate_with_lookup` method.
Below is a minimal example of how to use LMLM for inference.
For the full script, see `scripts/eval/example_lmlm_inference.sh`.
```
from transformers import AutoTokenizer
from lmlm.modeling_lmlm import LlamaForLMLM
from lmlm.database import DatabaseManager
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token
db = DatabaseManager().load_database(database_path) if database_path else None
model = LlamaForLMLM.from_pretrained_with_db(model_path, db_manager=db, use_special_tokens=True).cuda().eval()
output = model.generate_with_lookup(
prompt='Tell me a bio 