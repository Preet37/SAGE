# Source: https://ar5iv.labs.arxiv.org/html/2402.04779
# Author: Qingyu Yin et al.
# Title: StableMask: Refining Causal Masking in Decoder Transformers
# Fetched via: trafilatura
# Date: 2026-04-11

StableMask: Refining Causal Masking in Decoder-only Transformer
Abstract
The decoder-only Transformer architecture with causal masking and relative position encoding (RPE) has become the de facto choice in language modeling. Despite its exceptional performance across various tasks, we have identified two limitations: First, it requires all attention scores to be non-zero and sum up to 1, even if the current embedding has sufficient self-contained information. This compels the model to assign disproportional excessive attention to specific tokens. Second, RPE-based Transformers are not universal approximators due to their limited capacity at encoding absolute positional information, which limits their application in position-critical tasks. In this work, we propose StableMask: a parameter-free method to address both limitations by refining the causal mask. It introduces pseudo-attention values to balance attention distributions and encodes absolute positional information via a progressively decreasing mask ratio. StableMask’s effectiveness is validated both theoretically and empirically, showing significant enhancements in language models with parameter sizes ranging from 71M to 1.4B across diverse datasets and encoding methods. We further show that it naturally supports (1) efficient extrapolation without special tricks such as StreamingLLM and (2) easy integration with existing attention optimization techniques.
1 Introduction
Large Language Models (LLMs) have revolutionized natural language processing for their task-agnostic in-context learning paradigm (Brown et al., [2020](#bib.bib3)). The core of LLMs is the decoder-only Transformer architecture (Vaswani et al., [2017](#bib.bib32); Radford et al., [2019](#bib.bib25)), characterized by the self-attention mechanism and relative positional encoding (RPE) to aggregate information and catch the dependency among tokens. It has exhibited superior zero-shot generalization capabilities in comparison to its encoder-decoder counterparts, leading to its increased prevalence in pre-trained LLMs (Lester et al., [2021](#bib.bib14); Patel et al., [2023](#bib.bib21)). Despite the impressive success, we identified two important issues within this architecture.
The first issue arises from the softmax function used in self-attention, as its outputs consist solely of non-zero values summing up to 1 (Pang et al., [2019](#bib.bib18)). This forces to allocate a certain distribution of attention probability across all available tokens, even when the current token already has sufficient self-contained information (Xiao et al., [2023](#bib.bib33)) or when the attention mechanism does not need to prioritize any token (Hua et al., [2022](#bib.bib7); Bondarenko et al., [2023](#bib.bib2)). In such cases, the model tends to allocate disproportional attention scores to specific tokens like punctuation marks. This problem is exacerbated in decoder-only models as the varied sequence length leads to an extremely uneven attention distribution, particularly on the initial tokens. While approaches have been proposed to mitigate this issue, they all entail significant complexity. e.g., modifying the sparseness of softmax (Laha et al., [2018](#bib.bib13)), or adding dedicated tokens to absorb unnecessary attention (Darcet et al., [2023](#bib.bib5)).
The second limitation is associated with various relative positional encoding strategies (Ke et al., [2020](#bib.bib10)), e.g. ALiBi (Press et al., [2022](#bib.bib24)), T5 (Raffel et al., [2020](#bib.bib26)), and RoPE (Su et al., [2021](#bib.bib29)). Compared with absolute position encoding (APE), RPE has achieved state-of-the-art performance in most natural language task. It also exhibits better extrapolation capabilities, and naturally preserves invariant properties
for several important transformations like rotation and translation, making it more widely used in Transformers (Press et al., [2022](#bib.bib24)). However, RPE fails to capture enough absolute positional information as the softmax always generates a right stochastic matrix (Luo et al., [2022](#bib.bib15)), i.e., a square matrix where each row consists of non-negative real numbers adding up to 1.
This restricts its application in situations where such positional information is crucial. Previous attempts to address this, such as URPE (Luo et al., [2022](#bib.bib15)), added learnable relative position matrices atop the softmax outputs, which hurt the extrapolation capabilities because of the non-extensibility of learnable parameters.
In this paper, we propose StableMask – a tailored approach to address both issues by carefully modifying the causal mask in the decoder-based transformers. It introduces extra pseudo attention scores to the upper triangular attention matrix, which stabilizes the normalization constant of attention scores within each row regardless of the sequence length and token position. This allows the model to allocate excess attention to these dedicated pseudo scores. Moreover, StableMask progressively ensures that the result of softmax is not a right stochastic matrix. With a decreasing mask ratio (i.e. the sum of each row after softmax), it enables the model to encode a measurement of absolute position during the softmax stage, while remaining consistent with the decaying inter-token dependency used in RPE, thus effectively maintaining its extrapolation capability.
StableMask’s effectiveness has been thoroughly validated through extensive testing on multiple language models across a diverse array of both synthetic and realistic tasks.
It represents a substantial advancement in refining the attention mechanisms for decoder-only Transformers, overcoming the inherent limitations while retaining their core strengths.
A key advantage of StableMask is its parameter-free nature. As StableMask is implemented solely as a direct replacement for the causal mask, it is highly compatibile with the Transformer’s native architecture (such as different position encodings, attention optimizations or extrapolation techniques). For instance, we have presented an implementation of StableMask that is optimized for hardware efficiency, aligning with the principles of FlashAttention (Dao et al., [2022](#bib.bib4)). This allows StableMask to seamlessly integrate into the ecosystem of Transformer models, thereby expanding its potential applications.
Our core contributions can be summarized as follows:
-
1.
We identified two issues in the commonly used decoder-only Transformer architecture: the disproportional attention distribution and the inability to accurately capture positional information.
-
2.
We propose StableMask, an efficient and easily integrable solution to effectively address both issues by carefully modifying the causal mask.
-
3.
We validate the effectiveness of StableMask across multiple tasks and encoding methods.
-
4.
We present a hardware-efficient version of StableMask to optimize its practical applicability.
2 Preliminary
Self-Attention
Let be the input sequence, be the sequence length and be the dimensionality of the hidden state.
The self-attention mechanism in Transformer architectures calculates attention scores between each pair of words to capture dependencies between words and learn contextual information effectively.
Let denote the attention score matrix and be the attention score between the -th word and the -th word. We have
where represent the Query, Key, and Value matrices derived from (Vaswani et al., [2017](#bib.bib32)). In decoder-only models, is further modified by a causal mask and a softmax operation:
| (1) |
The following holds to prevent the model from attending to future tokens:
| (2) | |||||
| (3) |
Position Encoding
The raw Transformer without position encodings is insensitive to permutational rearrangements.
Two chief methods have been employed to remove this insensitivity: absolute position encoding (APE) and relative position encoding (RPE). APE assigns an index-dependent vector at each position to the word embeddings. These assigned vectors are usually trainable parameters to represent absolute positions of each input token (Kenton & Toutanova, [2019](#bib.bib11); Radford et al., [2019](#bib.bib25)).
More recently, RPE such as ALiBi (Press et al., [2022](#bib.bib24)), T5 (Raffel et al., [2020](#bib.bib26)) and RoPE (Su et al., [2021](#bib.bib29)) took a different approach by incorporating relative distances of positions into the attention score matrix. RPEs can be mainly classified into additive (T5, ALiBi, etc.) or multiplicative (RoPE, etc.):
| Add: | (4) | ||||
| Mul: | (5) |
where . are rotary forms usually in complex values and is a Topelitz matrix. Given its consistent demonstrated improvements over APE, RPE has emerged as the default choice in LLMs.
3 Problem
Despite the exceptional performance, we identified two key issues associated with self-attention and RPE.
Disproportional Attention
The first issue arises from the softmax function used in
self-attention. Given that the softmax function requires all attention scores to be non-zero and sum up to 1, it necessitates an inescapable distribution of attention across on all visible tokens. However, previous studies (Shen et al., [2019](#bib.bib28); Hassid et al., [2022](#bib.bib6); Bondarenko et al., [2023](#bib.bib2); Xiao et al., [2023](#bib.bib33)) have shown that the attention mechanism often requires very few important tokens, and the others are merely distractions. In this case, the requirement imposed by the softmax function prevents the model from effectively zeroing out the attention scores for irrelevant tokens. Some of these irrelevant tokens, such as initial tokens or non-functional words like punctuation marks, are more frequently observed by other tokens. In consequence, as shown in Figure [1](#S1.F1), the model tends to allocate disproportional attention (DA) to them. We refer to these tokens which are not semantically relevant, but receive disproportional attention values, as DA tokens111Appendix [A](#A1) offers an information-theoretic definition and interpretation of the DA issue.. The existence of DA tokens can lead to various undesired problems, e.g., perplexity surge in length extrapolation or sensitivity to irrelevant noise (Xiao et al., [2023](#bib.bib33)).
Interestingly, the extent of this DA phenomenon varies across token positions within the decoder-only language model. It is most prominent at the beginning of a sequence, and gradually eases towards the end (as seen in Figure [1](#S1.F1)(b)). Intuitively, as the token position increases, more tokens participate in the softmax operation and even assigning a very small probability to each token can result in a significant accumulative probability. As a result, DA tokens cannot receive as much attention values as they do near the beginning of a sequence.
Existing solutions, such as StreamingLLM (Xiao et al., [2023](#bib.bib33)) and ViT Register (Darcet et al., [2023](#bib.bib5)), have attempted to address this by introducing Artificial Tokens (AT) to absorb excess attention, so that real tokens can be freed from getting unnecessary DA. We term them as AT-based methods. However, as said, the severity of the DA issue varies along token positions. We hypothesize that adding a fixed number of tokens across all sequences is not position-adaptive and thereby cannot fully address the DA issue.
Inability to Encode Absolute Position
Despite its superior performance, RPE that modifies does not ensure is also sensitive to position. For instance, when all inputs are identical vectors, the outputs are also guaranteed to be equal because the output of softmax generates a right stochastic matrix 222For a more in-depth discussion on all-identical inputs and their relation to DA, refer to Appendix [B.1](#A2.SS1).. Therefore, RPE can perform poorly in tasks where positional information is critical.
To verify this limitation of RPEs, we designed specialized datasets, inspired by URPE (Luo et al., [2022](#bib.bib15)), which focus on tasks requiring absolute positional information while maintaining consistent input sequences (check Appendix [B.2](#A2.SS2) for details). We report the average accuracy of various models in Figure [1](#S1.F1)(c). The results demonstrate that models relying exclusively on RPEs exhibit poor performance, confirming the inferiority of RPE in capturing absolute positional information.
One obvious solution to the limitation is to directly replace RPE with APE. However, as mentioned, APE has its own problems such as poor extrapolation, rotation and translation variant, worse prediction accuracy, etc (Su et al., [2021](#bib.bib29); Press et al., [2022](#bib.bib24)).
Another approach is to add additional parameters to the matrix after the softmax to re-encode absolute positional information. For example, URPE (Luo et al., [2022](#bib.bib15))
adds a learnable Toeplitz matrix to the softmax matrix via:
| (6) |
The URPE approach, while successfully encoding absolute positional information, has several drawbacks. First, it requires additional learnable parameters which complicates themodel optimization. Second, because the matrix is fixed, models trained with this method loses its ability to input context that is longer than the training length.
4 StableMask
In the previous section, we analyzed two problems with the decoder-only Transformer architecture commonly used in contemporary LLMs: disproportional attention and inability to encode absolute position. Disproportional attention happens when certain attention heads share no need to allocate any attention logits but have to due to the softmax mechanism, and this issue is more pronounced at the beginning of the sequence in the decoder. The inability to encode absolute position comes from the result of softmax: it is a right stochastic matrix, with the sum of each row equals one always, so its output is insensitive to absolute positions.
To address the above two problems, we seek a solution by introducing pseudo-attention scores into the softmax operation. Specifically, the solution should simultaneously meet the following requirements:
-
(i)
It can provide additional pseudo-attention scores to accommodate excess attention logits, thereby freeing DA tokens from the responsibility of absorbing unnecessary attention values.
-
(ii)
These additional pseudo-attention scores need to adhere to the property of DA in a decoder-only model, i.e. larger at the beginning of the sequence and smaller towards the end of the sequence.
-
(iii)
It ensures that the result of softmax is not a right stochastic matrix, i.e. the sum of each row is not 1, so that positional information can be encoded.
In the following section, we show that all of the above three requirements can be met by carefully modifying the causal mask applied after softmax.
4.1 Pseudo-attention Score
To meet the requirement (i) and (ii), we propose constructing a StableMask attention score matrix :
| (7) |
Here, we call these as pseudo-attention scores. When the current attention head does not depend too much on its previous context, it can choose to store unnecessary attention values on these pseudo-attention scores. For each row (all attention scores for the -th token), the sequence length it can attend to is fixed to be . Therefore there will be pseudo-attention scores in each row for excessive attention allocation. This fulfills requirement (ii), which involves having more pseudo-attention values towards the beginning of a sequence. can be calculated using the following method:
| (8) |
The problem then becomes how should the values of these pseudo-attention scores be set. At the start of training, the distribution of the scaled attention scores has a mean of . These attention scores are also influenced by position encoding, and commonly used RPEs typically exhibit decay with increasing relative distance. Therefore, pseudo-attention scores should not significantly disrupt the original distribution of attention scores, and they should also align with the characteristics of the relative position encoding used by the model. Consequently, for , it should conform to:
| (9) |
where is a decay rate hyperparameter. Therefore, the attention score matrix with StableMask should be:
| (10) |
Finally, we can replace the traditional causal mask operation in Equation ([1](#S2.E1)) with:
| (11) | |||||
Here the inside masks the attention score matrix with pseudo-attention scores, whereas the outside replaces the scores which need masking with 0 again. Therefore, StableMask still maintains the characteristics of causal decoding, ensuring that information does not leak from subsequent tokens.
4.2 StableMask Encodes Absolute Position
StableMask introduces a set of pseudo-attention scores. Therefore, for those real attention scores (the lower triangular part of the attention matrix ), their sum after softmax will not be 1, meeting the requirement (iii). Concretely, let denote the real attention scores of the -th row and denote the pseudo-attention scores in the -th row, we have:
where and are the real/pseudo attention in each row.
We reconsider the question posed in Section [3](#S3.SS0.SSS0.Px2): whether the model can encode positional information for an identical input sequence . The answer is affirmative:
notice that increases as increases (all s are equal), and decreases as increases, we have
which means after Equation , the output attention values will be monotonic:
This indicates that absolute positional information is effectively captured.
In general, a Transformer decoder with StableMask has the ability to encode absolute positional information:
Theorem 4.1.
Let be an input sequence of length to the StableMask model . Then, the first layer of can recover absolute positions in the hidden state . That is, there exist , , and for the first attention layer, along with and for the first feed-forward layer, that computes absolute positions and pass them to the next layer.
The complete proof can be found in Appendix [C](#A3).
4.3 Inference and Length Extrapolation
In Section [4.1](#S4.SS1), we introduced the computation process of StableMask. During the training phase, StableMask can be readily applied in parallel within a batch to backpropagate the training loss.
During inference, attention computation is usually performed serially and employs KV caching (Tang et al., [2021](#bib.bib30); Pope et al., [2023](#bib.bib23)).
StableMask in its original form is not cost-effective for inference, because it does not support the use of KV caching.
During the inference stage, when the sequence length is changed e.g. from to for causal decoding, attention layers need to recalculate the softmax results.
For the first rows, an additional pseudo-attention value is added, invalidating the previously calculated attention (see Figure [3](#S4.F3)).
This renders KV caching unusable, significantly increasing the cost of inference.
| WikiText-103 | MiniPile | |||||||
|---|---|---|---|---|---|---|---|---|
| Model | *PE | #Params | PPL | Model | *PE | #Params | PPL 1 Epoch | PPL 2 Epoch |
| BLOOM | ALiBi | 71M | BLOOM | ALiBi | 160M | |||
| BLOOM-SM | ALiBi | 71M | BLOOM-SM | ALiBi | 160M | |||
| OpenLLaMA | RoPE | 71M | OpenLLaMA | RoPE | 160M | |||
| OpenLLaMA-SM | RoPE | 71M | OpenLLaMA-SM | RoPE | 160M | |||
| BLOOM | ALiBi | 160M | BLOOM | ALiBi | 430M | |||
| BLOOM-SM | ALiBi | 160M | BLOOM-SM | ALiBi | 430M | |||
| OpenLLaMA | RoPE | 160M | OpenLLaMA | RoPE | 430M | |||
| OpenLLaMA-SM | RoPE | 160M | OpenLLaMA-SM | RoPE | 430M | |||
| *: positional encoding type |
Our solution is simple:
we pad the sequence to the training length while compressing the padded tokens into a single suffix token.
Assuming the current sequence length is ,
we first append a suffix token to the end of the sequence (See Figure [2](#S3.F2) (f) and Figure [3](#S4.F3)).
At this point, the size of the attention matrix becomes .
Then, in the additional last column, we add a factor :
The last row of comes from the suffix and will not be utilized for generation. This makes each row equivalent to the case when the sequence length is the same as the training length, allowing us to use KV caching.
Next, we deal with the length extrapolation scenario, i.e. inputs that are longer than the pretraining length limit.
Notice that when reaches the maximum training length , becomes .
This setup prevents the model from continuing to generate values beyond the training length.
Therefore, during extrapolation, we set , where is the current sequence length. in long sequences is a very small number after applying the softmax, and its value will approach zero as grows. However, the presence of this term still ensures that the softmax result is not a right stochastic matrix, thereby asymptotically encoding absolute positional information.
In addition, when the sequence length is very long, the phenomenon of disproportional attention nearly disappears, as we concluded in Section [3](#S3.SS0.SSS0.Px1). Hence the pseudo-attention score does not need to maintain a large value.
4.4 Hardware-Efficient Implementation of StableMask
FlashAttention (Dao et al., [2022](#bib.bib4)) represents a major advance in accelerating the Transformer architecture. It avoids repeated data transfers between GPU’s High Bandwidth Memory (HBM) and processing units, by segmenting and sequentially processing the matrix on-chip.
StableMask’s integration into this framework is seamless, requiring only minimal modifications. In the FlashAttention paradigm, the query , key , and value matrices are partitioned into blocks , , , each of dimension . Then each block is fetched for computation. The attention scores for blocks and are derived from the on-chip computation:
.
With the incorporation of StableMask into FlashAttention, two additional fused operations are introduced as follows:
| (12) |
where and correspond to the StableMask matrices, segmented into blocks with and loaded on-chip.
We include a complete formula derivation and pseudocode implementation in Appendix [D](#A4).
| Model | PPL / Tokens | DownStream Tasks | |||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
| 5B | 10B | 15B | 20B | 25B | LBD | PIQA | ARCE | ARCC | OBQA | WG | |
| OpenLLaMA | 15.4±.2 | 14.8±.3 | 12.4±.3 | 11.7±.2 | 10.7±.3 | 59.4 | 67.1 | 51.4 | 25.6 | 31.4 | 53.5 |
| OpenLLaMa-SM | 15.0±.2 | 14.6±.1 | 11.9±.1 | 11.3±.4 | 10.4±.3 | 59.6 | 67.1 | 51.7 | 25.6 | 32.6 | 54.1 |
5 Experiments
In this section, we present extensive experiments to rigorously evaluate the performance of our proposed method.
5.1 StableMask Solves Two Problems
Our initial assessment confirms the efficacy of the StableMask model in addressing the two problems in Transformer models. The experimental results have been presented in Figure [1](#S1.F1). Firstly, concerning the disproportionate attention problem, we perform a comparative visualization of the attention heads in models with and without StableMask. By calculating the attention probability ratios for the first token and various token types, we observed that StableMask largely rectifies the issue of abnormal attention distribution. With StableMark, both initial tokens and punctuation marks experience a significant reduction in attention values. Regarding the second issue of encoding absolute positional information, we evaluated the model’s fitting capabilities on a specially designed dataset, comparing StableMask with various Position Encoding approaches. The findings indicate StableMask adeptly encodes absolute positional information, thereby effectively remedying the limitations inherent in relative position encoding. We also provided a visualization of the new attention score matrix after softmax with StableMask in Appendix [F](#A6).
5.2 StableMask Improves Model Performance
We further tested the performance of StableMask on various model architectures and position encodings. Our experiments leverage models built on BLOOM (LLaMA architecture with ALiBi) and OpenLLaMA (Touvron et al., [2023](#bib.bib31)) (RoPE (Su et al., [2021](#bib.bib29))) architectures. Detail settings could be checked in the Appendix [E](#A5).
Performance on Wikitext-103 and MiniPile (Table [1](#S4.T1)): Empirical evidence underscores the efficacy of models employing StableMask when trained on both Wikitext-103 (Merity et al., [2016](#bib.bib16)) and MiniPile (Kaddour, [2023](#bib.bib8)). These models demonstrate enhanced perplexity (PPL) scores, a pattern consistent across different architectures and sizes, including those with ALiBi and RoPE, and spanning parameter scales of 71M to 400M. Notably, within those datasets, models integrating StableMask consistently outshine their counterparts lacking this feature.
Impact on Scaling Performance (Table [2](#S4.T2)): The Pile is an extensive open-source dataset tailored for large-scale language modeling. We pretrained a 1.4B model with LLaMA architecture on the Pile dataset with 25B tokens. In the context of scaling of tokens, the model with StableMask consistently achieves better PPL scores compared to the standard OpenLLaMA model, showing the scaling ability of models with StableMask.
Effectiveness in Downstream Tasks (Table [2](#S4.T2)): When examining pre-trained models on downstream tasks like LAMBADA (Paperno et al., [2016](#bib.bib19)), PIQA (Bisk et al., [2019](#bib.bib1)), ARC-Easy (Yadav et al., [2019](#bib.bib34)), ARC-Challenge (Yadav et al., [2019](#bib.bib34)), OpenbookQA (Mihaylov et al., [2018](#bib.bib17)), and Winogrande (Sakaguchi et al., [2021](#bib.bib27)), model with StableMask shows a general trend of improved performance. It suggests that StableMask not only improves language understanding in the pretraining stage but also enhances effectiveness in downstream tasks.
5.3 Extrapolation Capability
As StableMask resolves the problem of DA tokens, it naturally addresses the attention sink issue (Xiao et al., [2023](#bib.bib33)), where initial tokens get large attention values and removing them from the attention window leads to a surge in perplexity. The models with our proposed StableMask do not need to preserve tokens at the beginning of the sequence during window-based extrapolation and avoid causing generation failures.
As shown in Figure [4](#S4.F4), when using the RoPE position encoding, the extrapolation perplexity quickly explodes without StableMask. When StableMask is applied, the extrapolation perplexity remains stable with window
attention, where only the most recent KVs are cached.
Furthermore, we believe that the parameter-free nature of StableMask facilitates its seamless integration with other extrapolation methods, a prospect we leave for future exploration.
| Methods | PPL | Pseudo Value | PPL |
|---|---|---|---|
| Baseline | 22.5 | 22.5 | |
| Learnable AT | 21.6 | 0 | 21.5 |
| Fixed Value AT | 22.4 | 22.2 | |
| StableMask | 21.1 | Positional Decay | 21.1 |
5.4 StableMask vs AT-based Methods
In Section [3](#S3), we discussed that the artificial token (AT)-based methods are one alternative method to mitigate the DA problem. These artificial tokens could be either learnable, i.e. added before the embedding layer, or fixed as constant vectors, e.g. zero vector. However, we find that as AT-based methods provide the same number of tokens for all sequences, its benefit is not as significant as StableMask (see Table [3](#S5.T3)) since the severity of the DA issue varies along the sequence. For fair comparison, we retrained OpenLLaMA models using the AT method and StableMask on the MiniPile dataset.
5.5 Impact on Inference Efficiency
In Section [4.3](#S4.SS3), we introduced StableMask for Inference, which changes the form of the mask to allow for more efficient inference strategies like KV cache. To validate its effectiveness, we tested the inference efficiency of a standard Transformer (Baseline), a model using StableMask (SM), and a model using StableMask for Inference (SM-I). We present the results in Figure [5](#S5.F5) and find that StableMask for Inference significantly improved the model’s inference efficiency, making it comparable to the efficiency of traditional Transformers.
5.6 Effects of Pseudo Attention Value
In Section [4](#S4), we introduced positional linear decay, making the pseudo-attention scores align with the characteristics of real attention scores.w
To validate its rationality, we conducted ablation experiments on various types of pseudo-attention scores. These experiments included four modes: (a) No addition of pseudo-attention scores, i.e., maintaining a mask of negative infinity.
(b) Padding with zeros, which aligns with the values of attention score distribution.
(c) Padding with a value different from the attention score distribution, e.g. .
(d) The positional decay method we proposed.
Our ablation studies, as detailed in Table [3](#S5.T3), demonstrate that a decay value like deviates significantly from the original attention matrix’s distribution, leading to diminished pretraining performance. The implementation of positional decay, however, excels in the training phase, showcasing state-of-the-art performance.
6 Related Work
Several studies have attempted to address issues inherent in the attention mechanism and softmax operation. A pivotal contribution by (Hassid et al., [2022](#bib.bib6)) raised questions about the role of certain heads in the attention mechanism. They discovered that substituting a subset of heads with constant diagonal matrices could even enhance model performance, suggesting that part of the model’s attention heads do not need to attend to any tokens other than themselves.
Quantizable Transformer (Bondarenko et al., [2023](#bib.bib2)) and StreamingLLM (Xiao et al., [2023](#bib.bib33)) identified a tendency in some attention heads to accumulate probabilities on the initial few tokens or on tokens similar to punctuation marks. Bondarenko et al. ([2023](#bib.bib2)) demonstrated that this behavior impacts model quantization, proposing a solution by trimming softmax and employing gated attention. StreamingLLM, on the other hand, observed that this phenomenon affects windowed attention, and addressed it by preserving the initial tokens.
Darcet et al. ([2023](#bib.bib5)) proposed adding “register tokens” which are essentially artificial places for the real tokens to attend to. The added tokens serve as a way to absorb the excessive attention that would otherwise accumulate on the initial tokens.
However, the previous approach of adding or using extra tokens either (1) uses fixed values or weights which does not account for possible distributional shifts when extrapolating to longer sequences; (2) does not explore its potential interference with positional embeddings; (3) adds extra parameters or computation to the attention layer, while not making clear whether existing optimization techniques are still applicable; (4) does not provide a theoretical framework for understanding the phenomenon more deeply.
7 Conclusion
StableMask represents a significant advancement in the field of language modeling, by simultaneously addressing two limitations of the decoder-only Transformer architecture: disproportional attention and inability to encode absolute position. By refining the causal mask with pseudo-attention values, StableMask adeptly balances attention distributions and encodes absolute positional information through a progressively decreasing mask ratio. It preserves the inherent distribution of the attention score matrix and enhances the model’s ability in various natural language tasks.
While StableMask demonstrates much potential, it is not without its constraints. One notable limitation is the slightly increased computational demand compared to conventional attention mechanisms. However, as the increased computation is only one matrix multiplication, we believe this overhead is negligible. Furthermore, StableMask inherently encodes absolute positional information, necessitating careful calibration to prevent the model from being adversely affected. We anticipate that forthcoming research will further refine our approach and overcome these challenges.
8 Acknowledgement
We thank Songlin Yang and other collaborators for the suggestions on language expression and image design in this paper.
References
- Bisk et al. (2019) Bisk, Y., Zellers, R., Bras, R. L., Gao, J., and Choi, Y. Piqa: Reasoning about physical commonsense in natural language, 2019.
- Bondarenko et al. (2023) Bondarenko, Y., Nagel, M., and Blankevoort, T. Quantizable transformers: Removing outliers by helping attention heads do nothing. arXiv preprint arXiv:2306.12929, 2023.
- Brown et al. (2020) Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., Neelakantan, A., Shyam, P., Sastry, G., Askell, A., et al. Language models are few-shot learners. Advances in Neural Information Processing Systems, 33:1877–1901, 2020.
- Dao et al. (2022) Dao, T., Fu, D., Ermon, S., Rudra, A., and Ré, C. Flashattention: Fast and memory-efficient exact attention with io-awareness. Advances in Neural Information Processing Systems, 35:16344–16359, 2022.
- Darcet et al. (2023) Darcet, T., Oquab, M., Mairal, J., and Bojanowski, P. Vision transformers need registers. arXiv preprint arXiv:2309.16588, 2023.
- Hassid et al. (2022) Hassid, M., Peng, H., Rotem, D., Kasai, J., Montero, I., Smith, N. A., and Schwartz, R. How much does attention actually attend? questioning the importance of attention in pretrained transformers, 2022.
- Hua et al. (2022) Hua, W., Dai, Z., Liu, H., and Le, Q. Transformer quality in linear time. In International Conference on Machine Learning, pp. 9099–9117. PMLR, 2022.
- Kaddour (2023) Kaddour, J. The minipile challenge for data-efficient language models, 2023.
- Kazemnejad et al. (2023) Kazemnejad, A., Padhi, I., Ramamurthy, K. N., Das, P., and Reddy, S. The impact of positional encoding on length generalization in transformers, 2023.
- Ke et al. (2020) Ke, G., He, D., and Liu, T.-Y. Rethinking positional encoding in language pre-training. arXiv preprint arXiv:2006.15595, 2020.
- Kenton & Toutanova (2019) Kenton, J. D. M.-W. C. and Toutanova, L. K. Bert: Pre-training of deep bidirectional transformers for language understanding. In Proceedings of NAACL-HLT, pp. 4171–4186, 2019.
- Kim et al. (2023) Kim, J., Kim, M., and Mozafari, B. Provable memorization capacity of transformers. In International Conference on Learning Representations, 2023.
- Laha et al. (2018) Laha, A., Chemmengath, S. A., Agrawal, P., Khapra, M., Sankaranarayanan, K., and Ramaswamy, H. G. On controllable sparse alternatives to softmax. Advances in Neural Information Processing Systems, 31, 2018.
- Lester et al. (2021) Lester, B., Al-Rfou, R., and Constant, N. The power of scale for parameter-efficient prompt tuning. In Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing, pp. 3045–3059, 2021.
- Luo et al. (2022) Luo, S., Li, S., Zheng, S., Liu, T.-Y., Wang, L., and He, D. Your transformer may not be as powerful as you expect. Advances in Neural Information Processing Systems, 35:4301–4315, 2022.
- Merity et al. (2016) Merity, S., Xiong, C., Bradbury, J., and Socher, R. Pointer sentinel mixture models. arXiv preprint arXiv:1609.07843, 2016.
-
Mihaylov et al. (2018)
Mihaylov, T., Clark, P., Khot, T., and Sabharwal, A.
Can a suit of armor conduct electricity? a new dataset for open book question answering.
In Conference on Empirical Methods in Natural Language Processing, 2018.
URL
[https://api.semanticscholar.org/CorpusID:52183757](https://api.semanticscholar.org/CorpusID:52183757). - Pang et al. (2019) Pang, T., Xu, K., Dong, Y., Du, C., Chen, N., and Zhu, J. Rethinking softmax cross-entropy loss for adversarial robustness. In International Conference on Learning Representations, 2019.
- Paperno et al. (2016) Paperno, D., Kruszewski, G., Lazaridou, A., Pham, Q. N., Bernardi, R., Pezzelle, S., Baroni, M., Boleda, G., and Fernández, R. The lambada dataset: Word prediction requiring a broad discourse context. arXiv preprint arXiv:1606.06031, 2016.
- Park et al. (2021) Park, S., Yun, C., Lee, J., and Shin, J. Minimum width for universal approximation. In International Conference on Learning Representations, 2021.
- Patel et al. (2023) Patel, A., Li, B., Rasooli, M. S., Constant, N., Raffel, C., and Callison-Burch, C. Bidirectional language models are also few-shot learners. In The Eleventh International Conference on Learning Representations, 2023.
- Polyanskiy & Wu (2016) Polyanskiy, Y. and Wu, Y. Strong data-processing inequalities for channels and bayesian networks, 2016.
- Pope et al. (2023) Pope, R., Douglas, S., Chowdhery, A., Devlin, J., Bradbury, J., Heek, J., Xiao, K., Agrawal, S., and Dean, J. Efficiently scaling transformer inference. Proceedings of Machine Learning and Systems, 5, 2023.
- Press et al. (2022) Press, O., Smith, N., and Lewis, M. Train short, test long: Attention with linear biases enables input length extrapolation. In International Conference on Learning Representations, 2022.
- Radford et al. (2019) Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I., et al. Language models are unsupervised multitask learners. OpenAI blog, 1(8):9, 2019.
- Raffel et al. (2020) Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., Zhou, Y., Li, W., and Liu, P. J. Exploring the limits of transfer learning with a unified text-to-text transformer. The Journal of Machine Learning Research, 21(1):5485–5551, 2020.
- Sakaguchi et al. (2021) Sakaguchi, K., Bras, R. L., Bhagavatula, C., and Choi, Y. Winogrande: An adversarial winograd schema challenge at scale. Communications of the ACM, 64(9):99–106, 2021.
- Shen et al. (2019) Shen, X., Zhao, Y., Su, H., and Klakow, D. Improving latent alignment in text summarization by generalizing the pointer generator. In Proceedings of the 2019 conference on empirical methods in natural language processing and the 9th international joint conference on natural language processing (EMNLP-IJCNLP), pp. 3762–3773, 2019.
- Su et al. (2021) Su, J., Lu, Y., Pan, S., Murtadha, A., Wen, B., and Liu, Y. Roformer: Enhanced transformer with rotary position embedding. arXiv preprint arXiv:2104.09864, 2021.
- Tang et al. (2021) Tang, Z., Li, C., Ge, J., Shen, X., Zhu, Z., and Luo, B. Ast-transformer: Encoding abstract syntax trees efficiently for code summarization. In 2021 36th IEEE/ACM International Conference on Automated Software Engineering (ASE), pp. 1193–1195. IEEE, 2021.
- Touvron et al. (2023) Touvron, H., Martin, L., Stone, K., Albert, P., Almahairi, A., Babaei, Y., Bashlykov, N., Batra, S., Bhargava, P., Bhosale, S., et al. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288, 2023.
- Vaswani et al. (2017) Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A. N., Kaiser, Ł., and Polosukhin, I. Attention is all you need. Advances in Neural Information Processing Systems, 30, 2017.
- Xiao et al. (2023) Xiao, G., Tian, Y., Chen, B., Han, S., and Lewis, M. Efficient streaming language models with attention sinks. arXiv preprint arXiv:2309.17453, 2023.
-
Yadav et al. (2019)
Yadav, V., Bethard, S., and Surdeanu, M.
Quick and (not so) dirty: Unsupervised selection of justification sentences for multi-hop question answering.
In Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing and the 9th International Joint Conference on Natural Language Processing (EMNLP-IJCNLP). Association for Computational Linguistics, 2019.
doi: 10.18653/v1/d19-1260.
URL
[http://dx.doi.org/10.18653/v1/D19-1260](http://dx.doi.org/10.18653/v1/D19-1260). - Yun et al. (2020) Yun, C., Bhojanapalli, S., Rawat, A. S., Reddi, S. J., and Kumar, S. Are transformers universal approximators of sequence-to-sequence functions? In International Conference on Learning Representations, 2020.
Appendix A Detailed Explanation of the DA Issue
The traditional dot-product attention makes the assumption that the next token is strongly related to the previous context. However, the mutual information could be small, especially in the initial parts of the sequence. We formalize this (counter-)intuition by defining the following concepts:
Definition A.1.
A causally isotropic data distribution of discrete random variables satisfies that for any set of indices , does not depend on the value of , where denotes entropy333Causal isotropy is a strict condition. We use it for demonstration purposes only: it isolates the effect of data variability in judging the disproportionality of attention..
Definition A.2.
A layer-wise decoder for a data distribution accepts any data point , and computes deterministically layers of intermediate representations , such that for , only receives inputs from (we define as or its embedding).
Definition A.3.
An contextual layer-wise decoder satisfies that for any two possible inputs and , if , then , where () is evaluated on input ().
Our definition of contextual decoder aligns with the definition of contextual mapping in previous works (Yun et al., [2020](#bib.bib35); Kim et al., [2023](#bib.bib12)), which guarantees that certain different inputs are mapped to different representations, although their definition of contextual mapping is more focused on the seq2seq setting.
Next, we make the following observations:
Proposition A.4.
For a layer-wise decoder on a data distribution, the prefixes of its intermediate representation at the -th layer satisfy
-
1.
for all ;
-
2.
if the decoder is contextual;
-
3.
for all and all if the data is causally isotropic;
-
4.
for all if the decoder is contextual and the data is causally isotropic.
Proof.
-
1.
Notice that is a Markov chain. By the data processing inequality (Polyanskiy & Wu,
[2016](#bib.bib22)), . -
2.
For any , let be the set of inputs where , which is equivalent to by the deterministic nature of decoder.
By the definition of contextual layer-wise decoder,
(13) Therefore,
(by conditional independence) (14) (15) (16) -
3.
Note that (
[14](#A1.E14)) can be written as a weighted average, which we denote as :(17) Similarly, with a slightly different definition of ,
(18) Apply Jensen’s inequality to the function , we have for any ,
Therefore,
(by causal isotropy) (20) -
4.
Apply causal isotropy to (
[15](#A1.E15)).
∎
We are now ready to define the disproportionality of attention:
Definition A.5.
Let inputs sampled from a data distribution run through a contextual layer-wise decoder with attention layers. If for at least one possible input , the attention after softmax in the -th layer satisfy
| (21) |
for some and , then this attention layer is said to have disproportional attention towards initial tokens on this input. The overall degree of disproportionality of an attention layer can be measured by the total probability of such inputs .
Note that by Proposition [A.4](#A1.Thmtheorem4), the following always holds:
| (22) |
This justifies our choice of the threshold for detecting the disproportionality of attention. Moreover, if the data is causally isotropic, the specific values of data do not matter for how much attention the model should pay.
In this work, we handle the DA problem by pseudo-attention scores and we offer a probabilistic interpretation. First, we clarify that the problem does not lie in the query-key-value mechanism of attention, but rather lies in the nature of autoregression: the history does not represent a complete description of the future, and the probability that the future deviates from the history must be taken into account, and more so at the beginning. Thus the output of an attention layer at earlier positions should be able to signal to the subsequent layers a higher variance of estimation compared to later positions. The failure of reliably doing so leads to the model having to allocate computation elsewhere to rectify the signal, such as excessive attention towards irrelevant tokens (Xiao et al., [2023](#bib.bib33)) and “no-op” heads (Bondarenko et al., [2023](#bib.bib2)), or becoming totally paralyzed (Appendix [B.1](#A2.SS1)). StableMask parameterizes this inductive bias orthogonal to decoder-only Transformers with RPE by pseudo-attention scores in the causal mask that decays over time.
Appendix B Further Explanation of Position Encoding
B.1 The Unit Test of Absolute Position-Awareness
Training a decoder-only Transformer with no PE will fail on data points that consist of all identical tokens, because the outputs of each layer are all identical vectors. Consequently, it is impossible for the model to predict different output distributions at different positions. We regard such all-identical inputs with different outputs at different positions as the “unit test” of absolute position awareness. We showed that Transformers with RPE cannot pass this test (Appendix [B.2](#A2.SS2)).
One way to pass the test without using explicit PE was proposed, by prepending a special token to the input sequence (Kazemnejad et al., [2023](#bib.bib9)). It breaks the symmetry in all positions and provides a way for the decoder to recognize absolute position. We note that this solution is equivalent to the AT-based method used to solve the DA issue (Section [3](#S3.SS0.SSS0.Px1)). This inspires us to see the test from the viewpoint of DA. Indeed, we have
Theorem B.1.
There exists a causally isotropic data distribution (defined in Appendix [A](#A1)) such that any regular Transformer decoder has a high probability of being (weakly) disproportional in all of its attention layers.
Proof.
Consider the following task: for any input , output the last token with probability , or a random token otherwise. The training dataset is constructed by a sampling algorithm that correctly does the task repeatedly.
The training dataset is causally isotropic: for every set of observed variables , , depends only on the largest element of , not on the specific values of variables.
Moreover, the probability density of this dataset concentrates most on the all-identical sequences, because as time goes on, sequences in the dataset are increasingly likely to copy themselves.
Last, we need to check that regular Transformer decoders have (weakly) disproportional attention on all identical sequences in all the attention layers. Note that although for , holds because of conditional independence between and given . On the other hand, holds because the softmax in a regular Transformer always gives positive attention. So the model has a weak disproportional attention towards initial tokens. ∎
Intuitively speaking, if the inputs are all identical, then the model only needs to know the last token and the sequence length in order to decide the output. All other attention can be regarded as (weakly) disproportional. However, inputs constructed this way only account for an exponentially small total probability in real datasets, so we separate this issue from the issue of disproportional attention.
B.2 Experiment of RPE’s Inability to Encode Absolute Position
To demonstrate that RPE cannot encode absolute positional information as discussed in Section [3](#S3.SS0.SSS0.Px2), we designed several experiments that require knowledge of absolute positional relationships. These experiments primarily include three tasks:
-
(1)
Absolute Position Mapping: Given an input sequence of “”, the model needs to accurately map each position to its absolute position. In other words, we expect an output of “”.
-
(2)
Absolute Position Identification: Given an input sequence of “”, where [ABE] encodes a special character at a specific position, the model needs to output the absolute position corresponding to the location encoded by [ABE]. In this case, we expect an output of “”, where represents the current position.
-
(3)
Odd-Even Number Counting: Given an input sequence of “”, the model needs to output a sequence of consecutive odd and even numbers, such as “”. This task also relies on the model’s ability to recognize absolute positional information.
| Accuracy | |||
| PE* | Task (1) | Task (2) | Task (3) |
| APE | |||
| Learnable | 96.7% | 94.3% | 97.6% |
| Sinusoidal | 98.1% | 99.1% | 96.2% |
| RPE | |||
| ALiBi | 21.7% | 26.7% | 46.5% |
| T5 | 22.4% | 24.5% | 42.7% |
| RoPE | 25.3% | 24.7% | 43.1% |
| *: positional encoding type |
Our experiments were conducted using a model with 160 million parameters, trained on four V100 GPUs. For detailed training hyperparameters, one can refer to the training details on the Wikitext-103 dataset (Appendix [E](#A5)).
Appendix C StableMask Encodes Absolute Positional Information
In this section, we present how StableMask can recover absolute positions in the hidden state using fewer portions of the model, than prepending a special token to the sequence (Appendix [B.1](#A2.SS1)). Our proof is inspired by NoPE (Kazemnejad et al., [2023](#bib.bib9)) but differs substantially in that they require three dimensions of hidden states at free disposal, while ours only needs two and is arguably more natural.
Theorem C.1.
Let be an input sequence of length to the StableMask model . Then, the first layer of can recover absolute positions in the hidden state . That is, there exist , , and for the first attention layer, along with and for the first feed-forward layer, that computes absolute positions and pass them to the next layer.
Proof.
We focus on the goal of reconstructing an index-dependent function at the end of the first attention layer. After reconstructing , recovering from it can be done by the universal approximation power of feed-forward networks (Park et al., [2021](#bib.bib20)).
For this, we need to gain control of a single head in the first attention layer, and use two hidden dimensions in the embedding layer. Note that this approach does not alter the rest of the Transformer model.
First, we specify the word embedding matrix as follows: the first row of is set to 1, which serves as the input vector; The second row of is set to 0, which serves as the output vector. Then, we have:
| (23) |
where . The word embeddings for the input sequence are retrieved from the embedding matrix by:
| (24) |
Second, for head dimension , we specify the weights of the selected attention head in the first layer. Specifically, we set , and
| (25) |
Consequently, all the query-key matching results are zero:
| (26) |
while takes the first row of , which is the input vector, and sets everywhere else zero:
| (27) |
We now calculate the output of attention. First, since the key-query matching results are all zero, the attention score matrix with StableMask is
| (28) |
Therefore,
| (29) |
| (30) |
Finally, is used to move the first row of to the second row:
| (31) |
Adding the residuals back to the input, we are done:
| (32) |
where denotes values computed by other heads in the first layer, which we assumed to not interfere with the first two hidden dimensions. ∎
Appendix D FlashAttention with StableMask
D.1 Introduction to FlashAttention
FlashAttention (Dao et al., [2022](#bib.bib4)) is a state-of-the-art method designed to enhance the performance of attention mechanisms in Transformer models, particularly addressing the efficiency constraints imposed by modern GPU memory hierarchies. Traditional attention mechanisms suffer from significant computational overhead, predominantly due to the necessity of storing and accessing large intermediate matrices, such as the softmax-normalized attention scores, from the High Bandwidth Memory (HBM). This process is inherently memory-bound due to the quadratic dependency on the sequence length, leading to extensive memory accesses and thus increased wall-clock time.
The A100 GPU, for instance, showcases the discrepancy in memory speeds within its hierarchy, having a significantly faster on-chip SRAM compared to the larger HBM. FlashAttention optimizes for this architectural detail by reducing HBM reads and writes. It achieves a sub-quadratic number of HBM accesses by employing techniques like tiling and recomputation, which allow for the attention computation to be performed in smaller, more manageable blocks within the on-chip SRAM. This block-based approach mitigates the need to store large intermediate matrices, especially beneficial during the backward pass of model training where intermediate values are traditionally saved to HBM.
Furthermore, FlashAttention incorporates kernel fusion in its implementation, enabling a single CUDA kernel to handle the entire computation process – from loading inputs from HBM, through all the computation steps (such as matrix multiplication and softmax), to writing the results back to HBM. This minimizes the frequency of costly memory accesses and contributes to an overall faster computation, without compromising the accuracy of the attention mechanism. As a result, FlashAttention stands out as an efficient primitive for both memory-bound and compute-bound operations within the GPU’s memory hierarchy, offering a significant improvement in the execution of Transformer models.
D.2 Derivation
In the FlashAttention paradigm, the query , key , and value matrices are partitioned into blocks , , , each of dimension . Then each block is fetched for computation. The attention scores for blocks and are derived from the on-chip computation: . With the incorporation of StableMask, two additional on-chip operations are introduced:
| (33) |
where and correspond to the StableMask matrices, segmented into blocks with , and loaded on-chip. The safe softmax operation, analogous to that in FlashAttention, proceeds as follows:
| (34) | |||||
| (35) | |||||
| (36) |
Subsequently, the algorithm rectifies the attention score matrix to account for zeros necessitated by the causal mask, so the final output is computed as:
| (37) |
D.3 A Typical Implementation of FlashAttention 2
(The parts that are different from the original algorithm are marked in purple.)
Appendix E Training Details
| Parameters | 71M | 160M | 400M | 1.4B |
| Embedding Size | 512 | 768 | 1024 | 2048 |
| Hidden Size (Attention) | 512 | 1536 | 2048 | 4096 |
| Hidden Size (FFN) | 2048 | 3072 | 2048 | 8192 |
| Expanding Rate (FFN) | 4 | 4 | 2 | 4 |
| Activation Function | SwishGeLU | SwishGeLU | SwishGeLU | SwishGeLU |
| Normalization Type | RMSNorm | RMSNorm | RMSNorm | RMSNorm |
| Positional Encoding | RoPE / ALiBi | RoPE / ALiBi | RoPE / ALiBi | RoPE |
| Tokenizer | GPT2 Tokenizer | GPT2 Tokenizer | GPT2 Tokenizer | GPT2 Tokenizer |
| Vocabulary Size | 50257 | 50257 | 50257 | 50257 |
| # of Attention Heads | 8 | 12 | 16 | 16 |
| # of Layers | 6 | 12 | 16 | 24 |
| Hyperparameters for Wikitext-103 | Hyperparameters for MiniPile | Hyperparameters for the Pile | |||
|---|---|---|---|---|---|
| Data | WikiText-103 | Data | MiniPile | Data | Pile |
| Sequence Length | 512 | Sequence Length | 512 / 1024 | Sequence Length | 1024 |
| Batch Size | 64 | Batch Size | 128 | Batch Size | 128 |
| Tokens per Batch | 32768 | Tokens per Batch | 65536 / 131072 | Tokens per Batch | 131072 |
| Total Steps | 50k | Steps per Epoch | 22k | Total Steps | 200k |
| Warmup Steps | 4k | Total Epoch | 2 | Warmup Steps | 4k |
| Beginning Learning Rate | 1e-6 | Warmup Steps | 4k | Beginning Learning Rate | 5e-6 |
| Peak Learning Rate | 6e-4 | Beginning Learning Rate | 1e-6 | Peak Learning Rate | 2e-4 |
| Learning Rate Decay | Linear | Peak Learning Rate | 4e-4 | Learning Rate Decay | Cosine |
| Optimizer | AdamW | Learning Rate Decay | Linear | Optimizer | AdamW |
| Adam | Optimizer | AdamW | Adam | ||
| Adam | 0.9 | Adam | Adam | 0.9 | |
| Adam | 0.98 | Adam | 0.9 | Adam | 0.98 |
| Hidden Dropout | 0 | Adam | 0.98 | Hidden Dropout | 0 |
| GELU Dropout | 0 | Hidden Dropout | 0 | GELU Dropout | 0 |
| Attention Dropout (if needed) | 0 | GELU Dropout | 0 | Attention Dropout (if needed) | 0 |
| Weight Decay | 0.01 | Attention Dropout (if needed) | 0 | Weight Decay | 0.1 |
| Gradient Clipping Value | 1 | Weight Decay | 0.1 | Gradient Clipping Value | 1 |
| Head-wise | True | Gradient Clipping Value | 1 | Head-wise | True |
| Value | 0.5 | Head-wise | True | Value | 0.5 |
Appendix F Visualization of Attention Heads with StableMask
See pages 1, 3, 4, 5, 6, 7, 8 of [image/output_score.pdf](image/output_score.pdf)