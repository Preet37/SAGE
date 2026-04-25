# Source: https://iclr.cc/archive/www/lib/exe/fetch.php%3Fmedia=iclr2015:bahdanau-iclr2015.pdf
# Title: [PDF] Neural Machine Translation by Jointly Learning to Align and Translate
# Fetched via: search
# Date: 2026-04-09

by Jointly Learning
to Align and Translate
Dzmitry Bahdanau*
*work was done during an internship at Université de Montreal
KyungHyun Cho, Yoshua Bengio
This Talk Is About...
… a neural network that translates…
Neural Machine Translation
input 
sentence 
output 
sentence 
neural 
net
input 
sentence 
output 
sentence 
neural net
SMT
input 
sentence 
output 
sentence 
SMT
neural net
different 
from
(Schwenk et al. 2006)
(Devlin et al. 2014)
Encoder-Decoder Approach
(Ñeco&Forcada, 1997)
(Kalchbrenner et al., 2013)
(Cho et al., 2014)
(Sutskever et al., 2014)
input 
sentence 
decoder
output 
sentence 
fixed size
representation
encoder
Encoder
Representation
RNN Encoder-Decoder (Cho et al. 2014):
Decoder
RNN Encoder-Decoder: Issues
●
has to remember the whole sentence
●
fixed size representation can be the bottleneck
●
humans do it differently
performance drops on   
long sentences:
…
Key Idea
Tell Decoder what is now translated:
The agreement on European Economic Area was signed in August 1992.
L'accord sur ???
L'accord sur l'Espace économique européen a été signé en ???
Have such hints computed by the net itself!
New Encoder
Bidirectional RNN: hj contains xj together with its context (..., xj-1, xj+1, …).
(h1, …, hL) is the new variable-length representation instead of fixed-length c.
New Decoder
Step i:
compute alignment
compute context
generate new output
compute new decoder state
Alignment Model
●
nonlinearity (tanh) is crucial!
●
simplest model possible
●
is precomputed => 
quadratic complexity with low 
constant
(1)
(2)
Experiment: English to French
Model:
●
RNN Search, 1000 units 
Baseline: 
●
RNN Encoder-Decoder, 1000 units 
●
Moses, a SMT system (Koehn et al. 2007)
Data: 
●
English to French translation, 348 million words,
●
30000 words + UNK token for the networks, all words for Moses
Training: 
●
Minimize mean log P(y|x,θ) w.r. θ
●
log P(y|x,θ) is differentiable w.r. θ => usual methods
Quantitative Results
no performance drop on long sentences
much better than RNN 
Encoder-Decoder
without unknown words 
comparable with the 
SMT system
…
Qualitative Results: Alignment
[penalty???]
Related Work: Neural MT
●Sutskever et al.
(2014)
○
30.6 BLEU with 4-layer LSTM Encoder-Decoder, 90k words
●Jean et al.
(2015)
○
32.8 BLEU, RNNSearch, 500k words by importance sampling
●Better results by using dictionaries and ensembles
○
Jean et al.
(2015), Luong et al.
(2015), both achieve state-of-the-
art
Related Work: Attention Mechanisms
●First differentiable attention model for handwriting 
...
○monotonic alignment only
○predicts shifts instead of selecting location
Our alignment model is an attention mechanism.
●Non-differentiable attention mechanism for image 
classification: (Mnih et al. 2014)
Summary
●
Novel approach to neural machine translation
○
No fixed size representation
○
Plausible alignments
●
Applicable to many other structured input/output problems
○
response generation (not exactly, but Shang et. al 2015)
○
speech recognition (Chorowski et. al 2014)
○
caption generation (Xu et. al, 2015)
○
video description generation (Yao et. al, 2015)
Thanks!

**arXiv:1409.0473** (cs)
...
# Title: Neural Machine Translation by Jointly Learning to Align and Translate
Authors:Dzmitry Bahdanau, Kyunghyun Cho, Yoshua Bengio
…
Abstract:Neural machine translation is a recently proposed approach to machine translation.
Unlike the traditional statistical machine translation, the neural machine translation aims at building a single neural network that can be jointly tuned to maximize the translation performance.
The models proposed recently for neural machine translation often belong to a family of encoder-decoders and consists of an encoder that encodes a source sentence into a fixed-length vector from which a decoder generates a translation.
In this paper, we conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture, and propose to extend this by allowing a model to automatically (soft-)search for parts of a source sentence that are relevant to predicting a target word, without having to form these parts as a hard segment explicitly.
With this new approach, we achieve a translation performance comparable to the existing state-of-the-art phrase-based system on the task of English-to-French translation.
Furthermore, qualitative analysis reveals that the (soft-)alignments found by the model agree well with our intuition.
|Comments:|Accepted at ICLR 2015 as oral presentation|
|--|--|
|Subjects:|Computation and Language (cs.CL); Machine Learning (cs.LG); Neural and Evolutionary Computing (cs.NE); Machine Learning (stat.ML)|
|Cite as:|arXiv:1409.0473 [cs.CL]|
| |(or arXiv:1409.0473v7 [cs.CL] for this version)|
| |https://doi.org/10.48550/arXiv.1409.0473 arXiv-issued DOI via DataCite|

# Neural Machine Translation by Jointly Learning to Align and Translate
@article{Bahdanau2014NeuralMT, title={Neural Machine Translation by Jointly Learning to Align and Translate}, author={Dzmitry Bahdanau and Kyunghyun Cho and Yoshua Bengio}, journal={CoRR}, year={2014}, volume={abs/1409.0473}, url={https://api.semanticscholar.org/CorpusID:11212020} }
It is conjecture that the use of a fixed-length vector is a bottleneck in improving the performance of this basic encoder-decoder architecture, and it is proposed to extend this by allowing a model to automatically (soft-)search for parts of a source sentence that are relevant to predicting a target word, without having to form these parts as a hard segment explicitly.
## Topics
...
This model has an attention mechanism that enables the decoder to generate a translated word while softly aligning it with phrases as well as words of the source sentence, and is called a tree-to-sequence NMT model, extending a sequence- to-sequence model with the source-side phrase structure.
## 33 References

# Neural Machine Translation by Jointly Learning to Align and Translate
(Bahdanau et al., 2014) orally at ICLR 2015
...
This paper was the first to show that an end-to-end neural system for machine translation (MT) could compete with the status quo.
When neural models started devouring MT, the dominant model was encoder–decoder.
This reduces a sentence to a fixed-size vector (basically smart hashing), then rehydrates that vector using the decoder into a target-language sentence.
The main contribution of this paper, an “attention mechanism”, lets the system focus on little portions of the source sentence as needed, bringing alignment to the neural world.
Information can be distributed, rather than squeezed into monolithic chunks.
In general, the approach to MT looks for the sentence $\mathbf{e}$ that maximizes $p(\mathbf{e} \mid \mathbf{f})$.
(Think of E and F representing English and French; the goal is to translate into English.)
Popular neural approaches from Cho et al. and Sutskever et al. used recurrent neural networks for their encoder and decoder.
The RNN combines the current word with information it has learnt about past words to produce a vector for each input token.
Sutskever et al.
(2014) took the last of these outputs as their fixed-size representation, the context.
The danger here is that information from early in the sentence can be heavily diluted.
The decoder is less interesting conceptually.
It defines the probability of a word in terms of the context and all prior generated words.
The decoder’s job is to find a sentence that maximizes the probability of an entire sentence.
The encoder–decoder framework’s fixed-size representations make long sentences challenging.
Bahdanau et al. reintroduce the “alignment” idea from non-neural MT—a mapping between positions in the source and target sentences.
It shows, e.g., which words in
`the blue house` give rise to the word
`maison` in
`le maison bleu`.
In simpler words, which parts translated into which parts?
The attention mechanism is an alteration of both the decoder and the encoder.
This time, the encoder change is less exciting: they use a bidirectional RNN now, which is two RNNs where one starts from the end of the sentence.
Its outputs now contain information from before and after the word in question.
The decoder is now no longer conditioned on just the single, sentence-level context.
A weighted sum of the encoder outputs is used instead.
The weights are a softmax of the alignment scores between the given decoder position and the encoder output vectors.
The scores come out of a simple neural network.
Note that unlike in traditional machine translation, the alignment is not considered to be a latent variable.
Instead, the alignment model directly computes a soft alignment, which allows the gradient of the cost function to be backpropagated through.
This gradient can be used to train the alignment model as well as the whole translation model jointly.
With this new approach the information can be spread throughout the sequence of annotations, which can be selectively retrieved by the decoder accordingly.
Another benefit of their approach is that it’s a soft alignment, rather than a hard one.
Not only does this make it differentiable (and learnable by a NN), but also it helps for agreement.
Consider the source phrase [the man] which was translated into [l’ homme].
Any hard alignment will map [the] to [l’] and [man] to [homme].
This is not helpful for translation, as one must consider the word following [the] to determine whether it should be translated into [le], [la], [les] or [l’].
Our soft-alignment solves this issue naturally by letting the model look at both [the] and [man], and in this example, we see that the model was able to correctly translate [the] into [l’].
Quantitatively, their attention model outperforms the normal encoder-decoder framework.
I’m doubtful of one claim, though—that the encoder-decoder model choked on long sentences.
Scores kept going up, by about the same percentage as the attention model did.
They’re just lower to begin with.
The Bahdanau et al. model also nears the performance of a big-deal phrase-based model that supplemented the training data with a monolingual corpus.
This is big for showing the viability of end-to-end neural MT.

NEURAL MACHINE TRANSLATION
BY JOINTLY LEARNING TO ALIGN AND TRANSLATE
Dzmitry Bahdanau
Jacobs University Bremen, Germany
KyungHyun Cho
Yoshua Bengio∗
Universit´e de Montr´eal
ABSTRACT
Neural machine translation is a recently proposed approach to machine transla-
tion. Unlike the traditional statistical machine translation, the neural machine
translation aims at building a single neural network that can be jointly tuned to
maximize the translation performance. The models proposed recently for neu-
ral machine translation often belong to a family of encoder–decoders and encode
a source sentence into a fixed-length vector from which a decoder generates a

…

having to form these parts as a hard segment explicitly. With this new approach,
we achieve a translation performance comparable to the existing state-of-the-art
phrase-based system on the task of English-to-French translation. Furthermore,
qualitative analysis reveals that the (soft-)alignments found by the model agree
well with our intuition.
1
INTRODUCTION
Neural machine translation is a newly emerging approach to machine translation, recently proposed
by Kalchbrenner and Blunsom (2013), Sutskever et al. (2014) and Cho et al. (2014b). Unlike the
traditional phrase-based translation system (see, e.g., Koehn et al., 2003) which consists of many
small sub-components that are tuned separately, neural machine translation attempts to build and
train a single, large neural network that reads a sentence and outputs a correct translation.
Most of the proposed neural machine translation models belong to a family of encoder–
decoders (Sutskever et al., 2014; Cho et al., 2014a), with an encoder and a decoder for each lan-
guage, or involve a language-specific encoder applied to each sentence whose outputs are then com-
pared (Hermann and Blunsom, 2014). An encoder neural network reads and encodes a source sen-
tence into a fixed-length vector. A decoder then outputs a translation from the encoded vector. The
whole encoder–decoder system, which consists of the encoder and the decoder for a language pair,
is jointly trained to maximize the probability of a correct translation given a source sentence.
A potential issue with this encoder–decoder approach is that a neural network needs to be able to
compress all the necessary information of a source sentence into a fixed-length vector. This may

…

to align and translate jointly. Each time the proposed model generates a word in a translation, it
(soft-)searches for a set of positions in a source sentence where the most relevant information is
concentrated. The model then predicts a target word based on the context vectors associated with
these source positions and all the previous generated target words.
∗CIFAR Senior Fellow
1
arXiv:1409.0473v6  [cs.CL]  24 Apr 2015

…

while decoding the translation. This frees a neural translation model from having to squash all the
information of a source sentence, regardless of its length, into a fixed-length vector. We show this
allows a model to cope better with long sentences.
In this paper, we show that the proposed approach of jointly learning to align and translate achieves
significantly improved translation performance over the basic encoder–decoder approach. The im-
provement is more apparent with longer sentences, but can be observed with sentences of any
length. On the task of English-to-French translation, the proposed approach achieves, with a single
model, a translation performance comparable, or close, to the conventional phrase-based system.
Furthermore, qualitative analysis reveals that the proposed model finds a linguistically plausible
(soft-)alignment between a source sentence and the corresponding target sentence.
2
BACKGROUND: NEURAL MACHINE TRANSLATION
From a probabilistic perspective, translation is equivalent to finding a target sentence y that max-
imizes the conditional probability of y given a source sentence x, i.e., arg maxy p(y | x). In
neural machine translation, we fit a parameterized model to maximize the conditional probability
of sentence pairs using a parallel training corpus. Once the conditional distribution is learned by a
translation model, given a source sentence a corresponding translation can be generated by searching
for the sentence that maximizes the conditional probability.
Recently, a number of papers have proposed the use of neural networks to directly learn this condi-

…

phrase-based machine translation system on an English-to-French translation task.1 Adding neural
components to existing translation systems, for instance, to score the phrase pairs in the phrase
table (Cho et al., 2014a) or to re-rank candidate translations (Sutskever et al., 2014), has allowed to

…

to align and translate simultaneously.
In the Encoder–Decoder framework, an encoder reads the input sentence, a sequence of vectors
x = (x1, · · · , xTx), into a vector c.2 The most common approach is to use an RNN such that
ht = f (xt, ht−1)

…

3
LEARNING TO ALIGN AND TRANSLATE
In this section, we propose a novel architecture for neural machine translation. The new architecture
consists of a bidirectional RNN as an encoder (Sec. 3.2) and a decoder that emulates searching
through a source sentence during decoding a translation (Sec. 3.1).

…

i match. The score is based on the RNN hidden state si−1 (just before emitting yi, Eq. (4)) and the
j-th annotation hj of the input sentence.
We parametrize the alignment model a as a feedforward neural network which is jointly trained with
all the other components of the proposed system. Note that unlike in traditional machine translation,
3

…

See Fig. 1 for the graphical illustration of the proposed model.
4
EXPERIMENT SETTINGS
We evaluate the proposed approach on the task of English-to-French translation. We use the bilin-
gual, parallel corpora provided by ACL WMT ’14.3 As a comparison, we also report the perfor-

…

For more details on the architectures of the models and training procedure used in the experiments,
see Appendices A and B.
5
RESULTS
5.1
QUANTITATIVE RESULTS
In Table 1, we list the translation performances measured in BLEU score. It is clear from the table
that in all the cases, the proposed RNNsearch outperforms the conventional RNNencdec. More

…

tokens when only the sentences having no unknown
words were evaluated (last column).
5.2
QUALITATIVE ANALYSIS
5.2.1
ALIGNMENT
The proposed approach provides an intuitive way to inspect the (soft-)alignment between the words
in a generated translation and those in a source sentence. This is done by visualizing the annotation

…

figure, we see that the model correctly translates a phrase [European Economic Area] into [zone
´economique europ´een]. The RNNsearch was able to correctly align [zone] with [Area], jumping
over the two words ([European] and [Economic]), and then looked one word back at a time to

…

must consider the word following [the] to determine whether it should be translated into [le], [la],
[les] or [l’]. Our soft-alignment solves this issue naturally by letting the model look at both [the] and
[man], and in this example, we see that the model was able to correctly translate [the] into [l’]. We

…

In conjunction with the quantitative results presented already, these qualitative observations con-
firm our hypotheses that the RNNsearch architecture enables far more reliable translation of long
sentences than the standard RNNencdec model.
In Appendix C, we provide a few more sample translations of long source sentences generated by
the RNNencdec-50, RNNsearch-50 and Google Translate along with the reference translations.

…

annotations only move in one direction. In the context of machine translation, this is a severe limi-
tation, as (long-distance) reordering is often needed to generate a grammatically correct translation
(for instance, English-to-German).
Our approach, on the other hand, requires computing the annotation weight of every word in the
source sentence for each word in the translation. This drawback is not severe with the task of
translation in which most of input and output sentences are only 15–40 words. However, this may
limit the applicability of the proposed scheme to other tasks.
8

…

translation system. Traditionally, a neural network trained as a target-side language model has been
used to rescore or rerank a list of candidate translations (see, e.g., Schwenk et al., 2006).
Although the above approaches were shown to improve the translation performance over the state-
of-the-art machine translation systems, we are more interested in a more ambitious objective of
designing a completely new translation system based on neural networks. The neural machine trans-
lation approach we consider in this paper is therefore a radical departure from these earlier works.
Rather than using a neural network as a part of the existing system, our model works on its own and
generates a translation from a source sentence directly.
7
CONCLUSION
The conventional approach to neural machine translation, called an encoder–decoder approach, en-
codes a whole input sentence into a fixed-length vector from which a translation will be decoded.
We conjectured that the use of a fixed-length context vector is problematic for translating long sen-
tences, based on a recent empirical study reported by Cho et al. (2014b) and Pouget-Abadie et al.

…

the alignment mechanism, are jointly trained towards a better log-probability of producing correct
translations.
We tested the proposed model, called RNNsearch, on the task of English-to-French translation. The
experiment revealed that the proposed RNNsearch outperforms the conventional encoder–decoder
model (RNNencdec) significantly, regardless of the sentence length and that it is much more ro-
bust to the length of a source sentence. From the qualitative analysis where we investigated the
(soft-)alignment generated by the RNNsearch, we were able to conclude that the model can cor-
rectly align each target word with the relevant words, or their annotations, in the source sentence as
it generated a correct translation.