# Source: https://web.stanford.edu/~jurafsky/slp3/old_dec21/10.pdf
# Title: Speech and Language Processing (3rd ed. draft) — Chapter 10: Machine Translation and Encoder-Decoder Models
# Fetched via: jina
# Date: 2026-04-11

Title: 10.pdf



Number of Pages: 31

Speech and Language Processing. Daniel Jurafsky & James H. Martin. Copyright © 2021. All rights reserved. Draft of December 29, 2021. 

CHAPTER 

# 10 Machine Translation and Encoder-Decoder Models 

“I want to talk the dialect of your people. It’s no use of talking unless people understand what you say.” 

Zora Neale Hurston, Moses, Man of the Mountain 1939, p. 121 

This chapter introduces machine translation (MT ), the use of computers to trans-machine translation MT late from one language to another. Of course translation, in its full generality, such as the translation of literature, or poetry, is a difficult, fascinating, and intensely human endeavor, as rich as any other area of human creativity. Machine translation in its present form therefore focuses on a number of very practical tasks. Perhaps the most common current use of machine translation is for information access . We might want to translate some instructions on the web, information access 

perhaps the recipe for a favorite dish, or the steps for putting together some furniture. Or we might want to read an article in a newspaper, or get information from an online resource like Wikipedia or a government webpage in a foreign language. 

MT for information access is probably one of the most com-mon uses of NLP technology, and Google Translate alone (shown above) translates hundreds of billions of words a day be-tween over 100 languages. Another common use of machine translation is to aid human translators. MT sys-tems are routinely used to produce a draft translation that is fixed up in a post-editing post-editing 

phase by a human translator. This task is often called computer-aided translation 

or CAT . CAT is commonly used as part of localization : the task of adapting content CAT localization or a product to a particular language community. Finally, a more recent application of MT is to in-the-moment human commu-nication needs. This includes incremental translation, translating speech on-the-fly before the entire sentence is complete, as is commonly used in simultaneous inter-pretation. Image-centric translation can be used for example to use OCR of the text on a phone camera image as input to an MT system to translate menus or street signs. The standard algorithm for MT is the encoder-decoder network, also called the encoder-decoder 

sequence to sequence network, an architecture that can be implemented with RNNs or with Transformers. We’ve seen in prior chapters that RNN or Transformer archi-tecture can be used to do classification (for example to map a sentence to a positive or negative sentiment tag for sentiment analysis), or can be used to do sequence la-beling (for example to assign each word in an input sentence with a part-of-speech, or with a named entity tag). For part-of-speech tagging, recall that the output tag is associated directly with each input word, and so we can just model the tag as output 

yt for each input word xt .2 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

Encoder-decoder or sequence-to-sequence models are used for a different kind of sequence modeling in which the output sequence is a complex function of the entire input sequencer; we must map from a sequence of input words or tokens to a sequence of tags that are not merely direct mappings from individual words. Machine translation is exactly such a task: the words of the target language don’t necessarily agree with the words of the source language in number or order. Consider translating the following made-up English sentence into Japanese. (10.1) English: He wrote a letter to a friend 

Japanese: tomodachi 

friend 

ni 

to 

tegami-o 

letter 

kaita 

wrote Note that the elements of the sentences are in very different places in the different languages. In English, the verb is in the middle of the sentence, while in Japanese, the verb kaita comes at the end. The Japanese sentence doesn’t require the pronoun 

he , while English does. Such differences between languages can be quite complex. In the following ac-tual sentence from the United Nations, notice the many changes between the Chinese sentence (we’ve given in red a word-by-word gloss of the Chinese characters) and its English equivalent. (10.2) 大会/General Assembly 在/on 1982 年/1982 12 月/December 10 日/10 通过

了/adopted 第37 号/37th 决议/resolution ，核准了/approved 第二

次/second 探索/exploration 及/and 和平peaceful 利用/using 外层空

间/outer space 会议/conference 的/of 各项/various 建议/suggestions 。

On 10 December 1982 , the General Assembly adopted resolution 37 in which it endorsed the recommendations of the Second United Nations Conference on the Exploration and Peaceful Uses of Outer Space . Note the many ways the English and Chinese differ. For example the order-ing differs in major ways; the Chinese order of the noun phrase is “peaceful using outer space conference of suggestions” while the English has “suggestions of the ... conference on peaceful use of outer space”). And the order differs in minor ways (the date is ordered differently). English requires the in many places that Chinese doesn’t, and adds some details (like “in which” and “it”) that aren’t necessary in Chinese. Chinese doesn’t grammatically mark plurality on nouns (unlike English, which has the “-s” in “recommendations”), and so the Chinese must use the modi-fier 各项/various to make it clear that there is not just one recommendation. English capitalizes some words but not others. Encoder-decoder networks are very successful at handling these sorts of com-plicated cases of sequence mappings. Indeed, the encoder-decoder algorithm is not just for MT; it’s the state of the art for many other tasks where complex mappings between two sequences are involved. These include summarization (where we map from a long text to its summary, like a title or an abstract), dialogue (where we map from what the user said to what our dialogue system should respond), semantic parsing (where we map from a string of words to a semantic representation like logic or SQL), and many others. We’ll introduce the algorithm in sections Section 10.2, and in following sections give important components of the model like beam search decoding , and we’ll discuss how MT is evaluated , introducing the simple chrF metric. But first, in the next section, we begin by summarizing the linguistic background to MT: key differences among languages that are important to consider when con-sidering the task of translation. 10.1 • LANGUAGE DIVERGENCES AND TYPOLOGY 3

## 10.1 Language Divergences and Typology 

Some aspects of human language seem to be universal , holding true for every lan-universal 

guage, or are statistical universals, holding true for most languages. Many universals arise from the functional role of language as a communicative system by humans. Every language, for example, seems to have words for referring to people, for talking about eating and drinking, for being polite or not. There are also structural linguistic universals; for example, every language seems to have nouns and verbs (Chapter 8), has ways to ask questions, or issue commands, linguistic mechanisms for indicating agreement or disagreement. Yet languages also differ in many ways, and an understanding of what causes such translation divergences will help us build better MT models. We often distin-translation divergence 

guish the idiosyncratic and lexical differences that must be dealt with one by one (the word for ”dog” differs wildly from language to language), from systematic dif-ferences that we can model in a general way (many languages put the verb before the direct object; others put the verb after the direct object). The study of these system-atic cross-linguistic similarities and differences is called linguistic typology . This typology 

section sketches some typological facts that impact machine translation; the inter-ested reader should also look into WALS, the World Atlas of Language Structures, which gives many typological facts about languages (Dryer and Haspelmath, 2013). 

10.1.1 Word Order Typology 

As we hinted it in our example above comparing English and Japanese, languages differ in the basic word order of verbs, subjects, and objects in simple declara-tive clauses. German, French, English, and Mandarin, for example, are all SVO SVO 

(Subject-Verb-Object ) languages, meaning that the verb tends to come between the subject and object. Hindi and Japanese, by contrast, are SOV languages, mean-SOV 

ing that the verb tends to come at the end of basic clauses, and Irish and Arabic are 

VSO languages. Two languages that share their basic word order type often have VSO 

other similarities. For example, VO languages generally have prepositions , whereas 

OV languages generally have postpositions .Let’s look in more detail at the example we saw above. In this SVO English sentence, the verb wrote is followed by its object a letter and the prepositional phrase 

to a friend , in which the preposition to is followed by its argument a friend . Arabic, with a VSO order, also has the verb before the object and prepositions. By contrast, in the Japanese example that follows, each of these orderings is reversed; the verb is 

preceded by its arguments, and the postposition follows its argument. (10.3) English: He wrote a letter to a friend 

Japanese: tomodachi 

friend 

ni 

to 

tegami-o 

letter 

kaita 

wrote Arabic: katabt 

wrote 

ris¯ ala 

letter 

li 

to 

˙sadq 

friend Other kinds of ordering preferences vary idiosyncratically from language to lan-guage. In some SVO languages (like English and Mandarin) adjectives tend to appear before verbs, while in others languages like Spanish and Modern Hebrew, adjectives appear after the noun: (10.4) Spanish bruja verde English green witch 4 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

(a) (b)  

> Figure 10.1 Examples of other word order differences: (a) In German, adverbs occur in initial position that in English are more natural later, and tensed verbs occur in second posi-tion. (b) In Mandarin, preposition phrases expressing goals often occur pre-verbally, unlike in English.

Fig. 10.1 shows examples of other word order differences. All of these word order differences between languages can cause problems for translation, requiring the system to do huge structural reorderings as it generates the output. 

10.1.2 Lexical Divergences 

Of course we also need to translate the individual words from one language to an-other. For any translation, the appropriate word can vary depending on the context. The English source-language word bass , for example, can appear in Spanish as the fish lubina or the musical instrument bajo . German uses two distinct words for what in English would be called a wall : Wand for walls inside a building, and Mauer for walls outside a building. Where English uses the word brother for any male sib-ling, Chinese and many other languages have distinct words for older brother and 

younger brother (Mandarin gege and didi , respectively). In all these cases, trans-lating bass , wall , or brother from English would require a kind of specialization, disambiguating the different uses of a word. For this reason the fields of MT and Word Sense Disambiguation (Chapter 18) are closely linked. Sometimes one language places more grammatical constraints on word choice than another. We saw above that English marks nouns for whether they are singular or plural. Mandarin doesn’t. Or French and Spanish, for example, mark grammat-ical gender on adjectives, so an English translation into French requires specifying adjective gender. The way that languages differ in lexically dividing up conceptual space may be more complex than this one-to-many translation problem, leading to many-to-many mappings. For example, Fig. 10.2 summarizes some of the complexities discussed by Hutchins and Somers (1992) in translating English leg, foot , and paw , to French. For example, when leg is used about an animal it’s translated as French jambe ; but about the leg of a journey, as French etape ; if the leg is of a chair, we use French 

pied .Further, one language may have a lexical gap , where no word or phrase, short lexical gap 

of an explanatory footnote, can express the exact meaning of a word in the other language. For example, English does not have a word that corresponds neatly to Mandarin xi` ao or Japanese oyak¯ ok¯ oo (in English one has to make do with awkward phrases like filial piety or loving child , or good son/daughter for both). Finally, languages differ systematically in how the conceptual properties of an event are mapped onto specific words. Talmy (1985, 1991) noted that languages can be characterized by whether direction of motion and manner of motion are marked on the verb or on the “satellites”: particles, prepositional phrases, or ad-verbial phrases. For example, a bottle floating out of a cave would be described in English with the direction marked on the particle out , while in Spanish the direction 10.1 • LANGUAGE DIVERGENCES AND TYPOLOGY 5etape patte 

jambe pied 

paw 

foot leg   

> JOURNEY ANIMAL
> HUMAN CHAIR
> ANIMAL
> BIRD
> HUMAN

Figure 10.2 The complex overlap between English leg , foot , etc., and various French trans-lations as discussed by Hutchins and Somers (1992). 

would be marked on the verb: (10.5) English: The bottle floated out. 

Spanish: La The botella bottle sali´ oexited flotando .

floating. 

Verb-framed languages mark the direction of motion on the verb (leaving the verb-framed 

satellites to mark the manner of motion), like Spanish acercarse ‘approach’, al-canzar ‘reach’, entrar ‘enter’, salir ‘exit’. Satellite-framed languages mark the satellite-framed 

direction of motion on the satellite (leaving the verb to mark the manner of motion), like English crawl out , float off , jump down , run after . Languages like Japanese, Tamil, and the many languages in the Romance, Semitic, and Mayan languages fam-ilies, are verb-framed; Chinese as well as non-Romance Indo-European languages like English, Swedish, Russian, Hindi, and Farsi are satellite framed (Talmy 1991, Slobin 1996). 

10.1.3 Morphological Typology 

Morphologically , languages are often characterized along two dimensions of vari-ation. The first is the number of morphemes per word, ranging from isolating isolating 

languages like Vietnamese and Cantonese, in which each word generally has one morpheme, to polysynthetic languages like Siberian Yupik (“Eskimo”), in which a polysynthetic 

single word may have very many morphemes, corresponding to a whole sentence in English. The second dimension is the degree to which morphemes are segmentable, ranging from agglutinative languages like Turkish, in which morphemes have rel-agglutinative 

atively clean boundaries, to fusion languages like Russian, in which a single affix fusion 

may conflate multiple morphemes, like -om in the word stolom (table-SG -INSTR -

> DECL

1), which fuses the distinct morphological categories instrumental, singular, and first declension. Translating between languages with rich morphology requires dealing with struc-ture below the word level, and for this reason modern systems generally use subword models like the wordpiece or BPE models of Section 10.7.1. 

10.1.4 Referential density 

Finally, languages vary along a typological dimension related to the things they tend to omit. Some languages, like English, require that we use an explicit pronoun when talking about a referent that is given in the discourse. In other languages, however, we can sometimes omit pronouns altogether, as the following example from Spanish shows 1: 

> 1Here we use the / 0-notation; we’ll introduce this and discuss this issue further in Chapter 22

6 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

(10.6) [El jefe] i dio con un libro. / 0i Mostr´ o a un descifrador ambulante. [The boss] came upon a book. [He] showed it to a wandering decoder. Languages that can omit pronouns are called pro-drop languages. Even among pro-drop 

the pro-drop languages, there are marked differences in frequencies of omission. Japanese and Chinese, for example, tend to omit far more than does Spanish. This dimension of variation across languages is called the dimension of referential den-sity . We say that languages that tend to use more pronouns are more referentially referential density 

dense than those that use more zeros. Referentially sparse languages, like Chinese or Japanese, that require the hearer to do more inferential work to recover antecedents are also called cold languages. Languages that are more explicit and make it easier cold language 

for the hearer are called hot languages. The terms hot and cold are borrowed from hot language 

Marshall McLuhan’s 1964 distinction between hot media like movies, which fill in many details for the viewer, versus cold media like comics, which require the reader to do more inferential work to fill out the representation (Bickel, 2003). Translating from languages with extensive pro-drop, like Chinese or Japanese, to non-pro-drop languages like English can be difficult since the model must somehow identify each zero and recover who or what is being talked about in order to insert the proper pronoun. 

## 10.2 The Encoder-Decoder Model 

Encoder-decoder networks, or sequence-to-sequence networks, are models ca-encoder-decoder 

pable of generating contextually appropriate, arbitrary length, output sequences. Encoder-decoder networks have been applied to a very wide range of applications including machine translation, summarization, question answering, and dialogue. The key idea underlying these networks is the use of an encoder network that takes an input sequence and creates a contextualized representation of it, often called the context . This representation is then passed to a decoder which generates a task-specific output sequence. Fig. 10.3 illustrates the architecture …    

> Encoder
> Decoder
> Context
> …
> x1x2xn
> y1y2ym

Figure 10.3 The encoder-decoder architecture. The context is a function of the hidden representations of the input, and may be used by the decoder in a variety of ways. 

Encoder-decoder networks consist of three components: 1. An encoder that accepts an input sequence, xn

> 1

, and generates a corresponding sequence of contextualized representations, hn

> 1

. LSTMs, convolutional net-works, and Transformers can all be employed as encoders. 2. A context vector , c, which is a function of hn

> 1

, and conveys the essence of the input to the decoder. 10.3 • ENCODER -D ECODER WITH RNN S 7

3. A decoder , which accepts c as input and generates an arbitrary length se-quence of hidden states hm 

> 1

, from which a corresponding sequence of output states ym 

> 1

, can be obtained. Just as with encoders, decoders can be realized by any kind of sequence architecture. 

## 10.3 Encoder-Decoder with RNNs 

Let’s begin by describing an encoder-decoder network based on a pair of RNNs. 2

Recall the conditional RNN language model from Chapter 9 for computing p(y),the probability of a sequence y. Like any language model, we can break down the probability as follows: 

p(y) = p(y1)p(y2|y1)p(y3|y1, y2)... P(ym|y1, ..., ym−1) (10.7) 

At a particular time t, we pass the prefix of t − 1 tokens through the language model, using forward inference to produce a sequence of hidden states, ending with the hidden state corresponding to the last word of the prefix. We then use the final hidden state of the prefix as our starting point to generate the next token. More formally, if g is an activation function like tanh or ReLU, a function of the input at time t and the hidden state at time t − 1, and f is a softmax over the set of possible vocabulary items, then at time t the output yt and hidden state ht are computed as: 

ht = g(ht−1, xt ) (10.8) 

yt = f (ht ) (10.9) 

We only have to make one slight change to turn this language model with au-toregressive generation into a translation model that can translate from a source text source 

in one language to a target text in a second: add a sentence separation marker at target 

the end of the source text, and then simply concatenate the target text. We briefly introduced this idea of a sentence separator token in Chapter 9 when we considered using a Transformer language model to do summarization, by training a conditional language model. If we call the source text x and the target text y, we are computing the probability 

p(y|x) as follows: 

p(y|x) = p(y1|x)p(y2|y1, x)p(y3|y1, y2, x)... P(ym|y1, ..., ym−1, x) (10.10) 

Fig. 10.4 shows the setup for a simplified version of the encoder-decoder model (we’ll see the full model, which requires attention , in the next section). Fig. 10.4 shows an English source text (“the green witch arrived”), a sentence separator token ( <s> , and a Spanish target text (“ lleg´ o la bruja verde ”). To trans-late a source text, we run it through the network performing forward inference to generate hidden states until we get to the end of the source. Then we begin autore-gressive generation, asking for a word in the context of the hidden layer from the end of the source input as well as the end-of-sentence marker. Subsequent words are conditioned on the previous hidden state and the embedding for the last word generated.  

> 2Later we’ll see how to use pairs of Transformers as well; it’s even possible to use separate architectures for the encoder and decoder.

8 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS Source Text 

Target Text 

> hn
> embedding
> layer
> hidden
> layer(s)
> softmax

the green 

llegó 

witch arrived <s> llegó 

la 

la 

bruja 

bruja 

verde 

verde 

</s> 

> (output of source is ignored)
> Separator

Figure 10.4 Translating a single sentence (inference time) in the basic RNN version of encoder-decoder ap-proach to machine translation. Source and target sentences are concatenated with a separator token in between, and the decoder uses context information from the encoder’s last hidden state. 

Let’s formalize and generalize this model a bit in Fig. 10.5. (To help keep things straight, we’ll use the superscripts e and d where needed to distinguish the hidden states of the encoder and the decoder.) The elements of the network on the left process the input sequence x and comprise the encoder . While our simplified fig-ure shows only a single network layer for the encoder, stacked architectures are the norm, where the output states from the top layer of the stack are taken as the fi-nal representation. A widely used encoder design makes use of stacked biLSTMs where the hidden states from top layers from the forward and backward passes are concatenated as described in Chapter 9 to provide the contextualized representations for each time step. Encoder  

> Decoder
> hn
> hd
> 1
> he3he2he1hd
> 2
> hd
> 3
> hd
> 4
> embedding
> layer
> hidden
> layer(s)
> softmax

x1 x2

y1

> hd
> n

x3 xn <s> y1

y2

y2

y3

y3

y4

yn

</s>     

> hen=c=hd0
> (output is ignored during encoding)

Figure 10.5 A more formal version of translating a sentence at inference time in the basic RNN-based encoder-decoder architecture. The final hidden state of the encoder RNN, hen, serves as the context for the decoder in its role as hd 

> 0

in the decoder RNN. 

The entire purpose of the encoder is to generate a contextualized representation of the input. This representation is embodied in the final hidden state of the encoder, 

hen. This representation, also called c for context , is then passed to the decoder. The decoder network on the right takes this state and uses it to initialize the first 10.3 • ENCODER -D ECODER WITH RNN S 9

hidden state of the decoder. That is, the first decoder RNN cell uses c as its prior hidden state hd 

> 0

. The decoder autoregressively generates a sequence of outputs, an element at a time, until an end-of-sequence marker is generated. Each hidden state is conditioned on the previous hidden state and the output generated in the previous state. hd1 hd2 hdi      

> y1y2yi
> c
> ……
> …
> Figure 10.6 Allowing every hidden state of the decoder (not just the first decoder state) to be influenced by the context cproduced by the encoder.

One weakness of this approach as described so far is that the influence of the context vector, c, will wane as the output sequence is generated. A solution is to make the context vector c available at each step in the decoding process by adding it as a parameter to the computation of the current hidden state, using the following equation (illustrated in Fig. 10.6): 

hdt = g( ˆyt−1, hdt−1, c) (10.11) 

Now we’re ready to see the full equations for this version of the decoder in the basic encoder-decoder model, with context available at each decoding timestep. Recall that g is a stand-in for some flavor of RNN and ˆ yt−1 is the embedding for the output sampled from the softmax at the previous step: 

c = hen

hd 

> 0

= chdt = g( ˆyt−1, hdt−1, c)

zt = f (hdt )

yt = softmax (zt ) (10.12) 

Finally, as shown earlier, the output y at each time step consists of a softmax com-putation over the set of possible outputs (the vocabulary, in the case of language modeling or MT). We compute the most likely output at each time step by taking the argmax over the softmax output: ˆyt = argmax w∈VP(w|x, y1... yt−1) (10.13) 

10.3.1 Training the Encoder-Decoder Model 

Encoder-decoder architectures are trained end-to-end, just as with the RNN language models of Chapter 9. Each training example is a tuple of paired strings, a source and a target. Concatenated with a separator token, these source-target pairs can now serve as training data. For MT, the training data typically consists of sets of sentences and their transla-tions. These can be drawn from standard datasets of aligned sentence pairs, as we’ll discuss in Section 10.7.2. Once we have a training set, the training itself proceeds as with any RNN-based language model. The network is given the source text and then starting with the separator token is trained autoregressively to predict the next word, as shown in Fig. 10.7. 10 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS Encoder 

Decoder 

embedding 

layer 

hidden 

layer(s) 

softmax 

the green 

llegó 

witch arrived <s> llegó 

la 

la 

bruja 

bruja 

verde 

verde 

</s> gold 

answers 

L1 =

-log P( y1)

x1 x2 x3 x4 

> <latexit sha1_base64="qOO6QdUN4jKU+f2F+W9QLLbCasc=">AAAB8XicbVBNS8NAEJ3Urxq/qh69BIvgqSQq6rHoxWMF+4FtKJvttl262YTdiRBC/4UXD4p49d9489+4aXPQ1gcDj/dmmJkXxIJrdN1vq7Syura+Ud60t7Z3dvcq+wctHSWKsiaNRKQ6AdFMcMmayFGwTqwYCQPB2sHkNvfbT0xpHskHTGPmh2Qk+ZBTgkZ67I0JZunUtu1+perW3BmcZeIVpAoFGv3KV28Q0SRkEqkgWnc9N0Y/Iwo5FWxq9xLNYkInZMS6hkoSMu1ns4unzolRBs4wUqYkOjP190RGQq3TMDCdIcGxXvRy8T+vm+Dw2s+4jBNkks4XDRPhYOTk7zsDrhhFkRpCqOLmVoeOiSIUTUh5CN7iy8ukdVbzLmvn9xfV+k0RRxmO4BhOwYMrqMMdNKAJFCQ8wyu8Wdp6sd6tj3lrySpmDuEPrM8fWfaQDg==</latexit>

ˆy

L2 =

-log P(y 2)

L3 =

-log P(y 3)

L4 =

-log P(y 4)

L5 =

-log P(y 5) per-word 

loss 

L = 1

T

TX

i=1 

Li

y1 y2 y3 y4 y5

Total loss is the average 

cross-entropy loss per 

target word: 

Figure 10.7 Training the basic RNN encoder-decoder approach to machine translation. Note that in the decoder we usually don’t propagate the model’s softmax outputs ˆ yt , but use teacher forcing to force each input to the correct gold value for training. We compute the softmax output distribution over ˆ y in the decoder in order to compute the loss at each token, which can then be averaged to compute a loss for the sentence. 

Note the differences between training (Fig. 10.7) and inference (Fig. 10.4) with respect to the outputs at each time step. The decoder during inference uses its own estimated output ˆ yt as the input for the next time step xt+1. Thus the decoder will tend to deviate more and more from the gold target sentence as it keeps generating more tokens. In training, therefore, it is more common to use teacher forcing in the teacher forcing 

decoder. Teacher forcing means that we force the system to use the gold target token from training as the next input xt+1, rather than allowing it to rely on the (possibly erroneous) decoder output ˆ yt . This speeds up training. 

## 10.4 Attention 

The simplicity of the encoder-decoder model is its clean separation of the encoder— which builds a representation of the source text—from the decoder, which uses this context to generate a target text. In the model as we’ve described it so far, this context vector is hn, the hidden state of the last (nth) time step of the source text. This final hidden state is thus acting as a bottleneck : it must represent absolutely everything about the meaning of the source text, since the only thing the decoder knows about the source text is what’s in this context vector (Fig. 10.8). Information at the beginning of the sentence, especially for long sentences, may not be equally well represented in the context vector. The attention mechanism is a solution to the bottleneck problem, a way of attention mechanism 

allowing the decoder to get information from all the hidden states of the encoder, not just the last hidden state. In the attention mechanism, as in the vanilla encoder-decoder model, the context vector c is a single vector that is a function of the hidden states of the encoder, that is, c = f (he

1 . . . hen). Because the number of hidden states varies with the size of the 10.4 • ATTENTION 11 Encoder Decoder bottleneck    

> bottleneck
> Figure 10.8 Requiring the context cto be only the encoder’s final hidden state forces all the information from the entire source sentence to pass through this representational bottleneck.

input, we can’t use the entire tensor of encoder hidden state vectors directly as the context for the decoder. The idea of attention is instead to create the single fixed-length vector c by taking a weighted sum of all the encoder hidden states. The weights focus on (‘attend to’) a particular part of the source text that is relevant for the token the decoder is currently producing. Attention thus replaces the static context vector with one that is dynamically derived from the encoder hidden states, different for each token in decoding. This context vector, ci, is generated anew with each decoding step i and takes all of the encoder hidden states into account in its derivation. We then make this context available during decoding by conditioning the computation of the current decoder hidden state on it (along with the prior hidden state and the previous output generated by the decoder), as we see in this equation (and Fig. 10.9): 

hdi = g( ˆyi−1, hdi−1, ci) (10.14) hd1 hd2 hdi      

> y1y2yi
> c1c2ci
> ……
> Figure 10.9 The attention mechanism allows each hidden state of the decoder to see a different, dynamic, context, which is a function of all the encoder hidden states.

The first step in computing ci is to compute how much to focus on each encoder state, how relevant each encoder state is to the decoder state captured in hdi−1. We capture relevance by computing— at each state i during decoding—a score (hdi−1, hej)

for each encoder state j.The simplest such score, called dot-product attention , implements relevance as dot-product attention 

similarity: measuring how similar the decoder hidden state is to an encoder hidden state, by computing the dot product between them: 

score (hdi−1, hej) = hdi−1 · hej (10.15) 

The score that results from this dot product is a scalar that reflects the degree of similarity between the two vectors. The vector of these scores across all the encoder hidden states gives us the relevance of each encoder state to the current step of the decoder. To make use of these scores, we’ll normalize them with a softmax to create a vector of weights, αi j , that tells us the proportional relevance of each encoder hidden 12 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 


αi j = softmax (score (hdi−1, hej) ∀ j ∈ e)= exp (score (hdi−1, hej)

∑

k exp (score (hdi−1, hek)) (10.16) 

Finally, given the distribution in α, we can compute a fixed-length context vector for the current decoder state by taking a weighted average over all the encoder hidden states. 

ci = ∑

j

αi j hej (10.17) 

With this, we finally have a fixed-length context vector that takes into account information from the entire encoder state that is dynamically updated to reflect the needs of the decoder at each step of decoding. Fig. 10.10 illustrates an encoder-decoder network with attention, focusing on the computation of one context vector 

ci.Encoder 

Decoder 

hdi-1 he3he2he1 hdihidden 

layer(s) 

x1 x2

yi

x3 xn

yi-1 yi

yi+1 

hen

ci

.2 .1 .3 .4 

attention 

weights 

ci-1 

ci 

> <latexit sha1_base64="TNdNmv/RIlrhPa6LgQyjjQLqyBA=">AAACAnicdVDLSsNAFJ3UV62vqCtxM1gEVyHpI9Vd0Y3LCvYBTQyT6bSddvJgZiKUUNz4K25cKOLWr3Dn3zhpK6jogQuHc+7l3nv8mFEhTfNDyy0tr6yu5dcLG5tb2zv67l5LRAnHpIkjFvGOjwRhNCRNSSUjnZgTFPiMtP3xRea3bwkXNAqv5SQmboAGIe1TjKSSPP3AEUngjVIHsXiIvJSOpnB4Q7zR1NOLpmGaVbtqQdOwLbtk24qY5Yp9VoOWsjIUwQINT393ehFOAhJKzJAQXcuMpZsiLilmZFpwEkFihMdoQLqKhiggwk1nL0zhsVJ6sB9xVaGEM/X7RIoCISaBrzoDJIfit5eJf3ndRPZP3ZSGcSJJiOeL+gmDMoJZHrBHOcGSTRRBmFN1K8RDxBGWKrWCCuHrU/g/aZUMyzbKV5Vi/XwRRx4cgiNwAixQA3VwCRqgCTC4Aw/gCTxr99qj9qK9zltz2mJmH/yA9vYJSymYCA==</latexit>

X

j

↵ij he

j

↵ij <latexit sha1_base64="y8s4mGdpwrGrBnuSR+p1gJJXYdo=">AAAB/nicdVDJSgNBEO2JW4zbqHjy0hgEL4YeJyQBL0EvHiOYBbIMPT09mTY9C909QhgC/ooXD4p49Tu8+Td2FkFFHxQ83quiqp6bcCYVQh9Gbml5ZXUtv17Y2Nza3jF391oyTgWhTRLzWHRcLClnEW0qpjjtJILi0OW07Y4up377jgrJ4uhGjRPaD/EwYj4jWGnJMQ+Cgedk7NSa9IgXq955MKDOrWMWUQnNAFGpYtfsakUTZNtWGUFrYRXBAg3HfO95MUlDGinCsZRdCyWqn2GhGOF0UuilkiaYjPCQdjWNcEhlP5udP4HHWvGgHwtdkYIz9ftEhkMpx6GrO0OsAvnbm4p/ed1U+bV+xqIkVTQi80V+yqGK4TQL6DFBieJjTTARTN8KSYAFJkonVtAhfH0K/yets5JVKdnX5WL9YhFHHhyCI3ACLFAFdXAFGqAJCMjAA3gCz8a98Wi8GK/z1pyxmNkHP2C8fQICDpWK</latexit> 

hd

i 1 · he

j

……

Figure 10.10 A sketch of the encoder-decoder network with attention, focusing on the computation of ci. The context value ci is one of the inputs to the computation of hdi . It is computed by taking the weighted sum of all the encoder hidden states, each weighted by their dot product with the prior decoder hidden state hdi−1.

It’s also possible to create more sophisticated scoring functions for attention models. Instead of simple dot product attention, we can get a more powerful function that computes the relevance of each encoder hidden state to the decoder hidden state by parameterizing the score with its own set of weights, Ws.

score (hdi−1, hej) = hdt−1Wshej

The weights Ws, which are then trained during normal end-to-end training, give the network the ability to learn which aspects of similarity between the decoder and encoder states are important to the current application. This bilinear model also allows the encoder and decoder to use different dimensional vectors, whereas the simple dot-product attention requires that the encoder and decoder hidden states have the same dimensionality. 10.5 • BEAM SEARCH 13 

## 10.5 Beam Search 

The decoding algorithm we gave above for generating translations has a problem (as does the autoregressive generation we introduced in Chapter 9 for generating from a conditional language model). Recall that algorithm: at each time step in decoding, the output yt is chosen by computing a softmax over the set of possible outputs (the vocabulary, in the case of language modeling or MT), and then choosing the highest probability token (the argmax): ˆyt = argmax w∈VP(w|x, y1... yt−1) (10.18) 

Choosing the single most probable token to generate at each step is called greedy greedy 

decoding; a greedy algorithm is one that make a choice that is locally optimal, whether or not it will turn out to have been the best choice with hindsight. Indeed, greedy search is not optimal, and may not find the highest probability translation. The problem is that the token that looks good to the decoder now might turn out later to have been the wrong choice! Let’s see this by looking at the search tree , a graphical representation of the search tree 

choices the decoder makes in searching for the best translation, in which we view the decoding problem as a heuristic state-space search and systematically explore the space of possible outputs. In such a search tree, the branches are the actions, in this case the action of generating a token, and the nodes are the states, in this case the state of having generated a particular prefix. We are searching for the best action sequence, i.e. the target string with the highest probability. Fig. 10.11 demonstrates the problem, using a made-up example. Notice that the most probable sequence is 

ok ok </s> (with a probability of .4*.7*1.0), but a greedy search algorithm will fail to find it, because it incorrectly chooses yes as the first word since it has the highest local probability. start  

> ok
> yes
> </s>
> ok
> yes
> </s>
> ok
> yes
> </s>
> </s>
> </s>
> </s>
> </s>
> t2t3
> p(t 1|source)
> t1
> p(t 2|source, t 1)
> p(t 3|source, t 1,t 2)
> .1
> .5
> .4
> .2
> .4
> .3
> .1
> .2
> .7
> 1.0
> 1.0
> 1.0
> 1.0

Figure 10.11 A search tree for generating the target string T = t1,t2, ... from the vocabulary 

V = {yes , ok , <s> }, given the source string, showing the probability of generating each token from that state. Greedy search would choose yes at the first time step followed by yes , instead of the globally most probable sequence ok ok .

Recall from Chapter 8 that for part-of-speech tagging we used dynamic pro-gramming search (the Viterbi algorithm) to address this problem. Unfortunately, dynamic programming is not applicable to generation problems with long-distance dependencies between the output decisions. The only method guaranteed to find the 14 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

best solution is exhaustive search: computing the probability of every one of the V T

possible sentences (for some length value T ) which is obviously too slow. Instead, decoding in MT and other sequence generation problems generally uses a method called beam search . In beam search, instead of choosing the best token beam search 

to generate at each timestep, we keep k possible tokens at each step. This fixed-size memory footprint k is called the beam width , on the metaphor of a flashlight beam beam width 

that can be parameterized to be wider or narrower. Thus at the first step of decoding, we compute a softmax over the entire vocab-ulary, assigning a probability to each word. We then select the k-best options from this softmax output. These initial k outputs are the search frontier and these k initial words are called hypotheses . A hypothesis is an output sequence, a translation-so-far, together with its probability. a

…

aardvark 

.. 

arrived 

.. 

the 

…

zebra 

start 

t1 

> a
> …
> aardvark
> ..
> the
> ..
> witch
> …
> zebra
> a
> …
> aardvark
> ..
> green
> ..
> witch
> …
> zebra

t2   

> hd1
> y1
> EOS
> y1
> y2
> y2
> hd1hd2
> the
> the EOS
> hd2
> green
> green
> y3
> hd1hd2
> arrived
> arrived EOS
> y2

t3   

> hd1hd2
> the
> the EOS
> y2
> hd1hd2
> the
> the EOS
> hd2
> witch
> witch
> y3
> a
> …
> mage
> ..
> the
> ..
> witch
> …
> zebra
> arrived
> …
> aardvark
> ..
> green
> ..
> who
> …
> zebra
> y3
> y3

Figure 10.12 Beam search decoding with a beam width of k = 2. At each time step, we choose the k best hypotheses, compute the V possible extensions of each hypothesis, score the resulting k ∗V possible hypotheses and choose the best k to continue. At time 1, the frontier is filled with the best 2 options from the initial state of the decoder: arrived and the . We then extend each of those, compute the probability of all the hypotheses so far ( arrived the , arrived aardvark , the green , the witch ) and compute the best 2 (in this case the green and the witch ) to be the search frontier to extend on the next step. On the arcs we show the decoders that we run to score the extension words (although for simplicity we haven’t shown the context value ci that is input at each step). 

At subsequent steps, each of the k best hypotheses is extended incrementally by being passed to distinct decoders, which each generate a softmax over the entire vocabulary to extend the hypothesis to every possible next token. Each of these k ∗V

hypotheses is scored by P(yi|x, y<i): the product of the probability of current word choice multiplied by the probability of the path that led to it. We then prune the k ∗V

hypotheses down to the k best hypotheses, so there are never more than k hypotheses 10.5 • BEAM SEARCH 15 

at the frontier of the search, and never more than k decoders. Fig. 10.12 illustrates this process with a beam width of 2. This process continues until a </s> is generated indicating that a complete can-didate output has been found. At this point, the completed hypothesis is removed from the frontier and the size of the beam is reduced by one. The search continues until the beam has been reduced to 0. The result will be k hypotheses. Let’s see how the scoring works in detail, scoring each node by its log proba-bility. Recall from Eq. 10.10 that we can use the chain rule of probability to break down p(y|x) into the product of the probability of each word given its prior context, which we can turn into a sum of logs (for an output string of length t): 

score (y) = log P(y|x)= log (P(y1|x)P(y2|y1, x)P(y3|y1, y2, x)... P(yt |y1, ..., yt−1, x)) =

> t

∑

> i=1

log P(yi|y1, ..., yi−1, x) (10.19) 

Thus at each step, to compute the probability of a partial translation, we simply add the log probability of the prefix translation so far to the log probability of generating the next token. Fig. 10.13 shows the scoring for the example sentence shown in Fig. 10.12, using some simple made-up probabilities. Log probabilities are negative or 0, and the max of two log probabilities is the one that is greater (closer to 0). start 

arrived 

the 

the 

witch 

green 

witch 

mage 

who  

> y2y3

log P(y 1|x) 

> y1

log P(y 2|y 1,x) log P(y 3|y 2,y 1,x) 

> -.92
> -1.6
> -1.2
> -.69
> -2.3
> -.69
> -1.6
> -2.3

arrived -.11  

> -.51

witch 

> -.36
> -.22

END  

> -.51

END 

> -2.3

at 

> -1.61

by 

log P(y 4|y 3,y 2,y 1,x) log P(y 5|y 4,y 3,y 2,y 1,x) 

arrived 

came -1.6    

> y4y5
> log P(arrived|x) log P(arrived witch|x)
> log P(the|x)
> log P(the green|x)
> log P(the witch|x)
> =-1.6
> log P (arrived the|x) log P (“the green witch arrived”|x)
> = log P (the|x) + log P(green|the,x)
> + log P(witch | the, green,x)
> +logP(arrived|the,green,witch,x)
> +log P(END|the,green,witch,arrived,x)
> = -2.3
> = -3.9
> = -1.6
> = -2.1
> =-.92
> -2.1
> -3.2
> -4.4
> -2.2
> -2.5
> -3.7
> -2.7
> -3.8
> -2.7
> -4.8

Figure 10.13 Scoring for beam search decoding with a beam width of k = 2. We maintain the log probability of each hypothesis in the beam by incrementally adding the logprob of generating each next token. Only the top 

k paths are extended to the next step. 

Fig. 10.14 gives the algorithm. One problem arises from the fact that the completed hypotheses may have differ-ent lengths. Because models generally assign lower probabilities to longer strings, a naive algorithm would also choose shorter strings for y. This was not an issue during the earlier steps of decoding; due to the breadth-first nature of beam search all the hypotheses being compared had the same length. The usual solution to this is 16 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

function BEAM DECODE (c, beam width ) returns best paths 

y0, h0 ← 0

path ← () 

complete paths ← () 


frontier ← 〈 state 〉 ;initial frontier 

while frontier contains incomplete paths and beamwidth > 0

extended frontier ← 〈〉 

for each state ∈ frontier do 

y ← DECODE (state )

for each word i ∈ Vocabulary do 

successor ← NEW STATE (state , i, yi)

extended frontier ← ADD TOBEAM (successor , extended frontier ,

beam width )

for each state in extended frontier do if state is complete do 

complete paths ← APPEND (complete paths , state )

extended frontier ← REMOVE (extended frontier , state )

beam width ← beam width - 1 

frontier ← extended frontier 

return completed paths 

function NEW STATE (state , word , word prob ) returns new state 

function ADD TOBEAM (state , frontier , width ) returns updated frontier 

if LENGTH (frontier ) < width then 

frontier ← INSERT (state , frontier )

else if SCORE (state ) > SCORE (W ORST OF(frontier )) 

frontier ← REMOVE (W ORST OF(frontier )) 

frontier ← INSERT (state , frontier )

return frontier 

Figure 10.14 Beam search decoding. 

to apply some form of length normalization to each of the hypotheses, for example simply dividing the negative log probability by the number of words: 

score (y) = − log P(y|x) = 1

T

> t

∑

> i=1

− log P(yi|y1, ..., yi−1, x) (10.20) 

Beam search is common in large production MT systems, generally with beam widths k between 5 and 10. What do we do with the resulting k hypotheses? In some cases, all we need from our MT algorithm is the single best hypothesis, so we can return that. In other cases our downstream application might want to look at all 

k hypotheses, so we can pass them all (or a subset) to the downstream application with their respective scores. 10.6 • ENCODER -D ECODER WITH TRANSFORMERS 17 

## 10.6 Encoder-Decoder with Transformers 

The encoder-decoder architecture can also be implemented using transformers (rather than RNN/LSTMs) as the component modules. At a high-level, the architecture, sketched in Fig. 10.15, is quite similar to what we saw for RNNs. It consists of an encoder that takes the source language input words X = x1, ..., xT and maps them to an output representation Henc = h1, ..., hT ; usually via N = 6 stacked encoder blocks. The decoder, just like the encoder-decoder RNN, is essentially a conditional language model that attends to the encoder representation and generates the target words one by one, at each timestep conditioning on the source sentence and the previously generated target language words. Encoder       

> The green
> llego
> witch arrived
> <s> llego
> la
> la
> bruja
> bruja
> verde
> verde
> </s>
> Decoder
> hhhh
> cross-attention
> transformer
> blocks

Figure 10.15 The encoder-decoder architecture using transformer components. The encoder uses the trans-former blocks we saw in Chapter 9, while the decoder uses a more powerful block with an extra encoder-decoder attention layer. The final output of the encoder Henc = h1, ..., hT is used to form the K and V inputs to the cross-attention layer in each decoder block. 

But the components of the architecture differ somewhat from the RNN and also from the transformer block we’ve seen. First, in order to attend to the source lan-guage, the transformer blocks in the decoder has an extra cross-attention layer. Recall that the transformer block of Chapter 9 consists of a self-attention layer that attends to the input from the previous layer, followed by layer norm, a feed for-ward layer, and another layer norm. The decoder transformer block includes an extra layer with a special kind of attention, cross-attention (also sometimes called cross-attention 

encoder-decoder attention or source attention ). Cross-attention has the same form as the multi-headed self-attention in a normal transformer block, except that while the queries as usual come from the previous layer of the decoder, the keys and values come from the output of the encoder .That is, the final output of the encoder Henc = h1, ..., ht is multiplied by the cross-attention layer’s key weights WK and value weights WV, but the output from the prior decoder layer Hdec [i−1] is multiplied by the cross-attention layer’s query weights WQ:

Q = WQHdec [i−1]; K = WKHenc ; V = WVHenc (10.21) 

CrossAttention (Q, K, V) = softmax 

( QK ᵀ

√dk

)

V (10.22) 18 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS Self-Attention Layer 

> Layer Normalize
> Feedforward Layer
> Layer Normalize

Encoder    

> x1x2x3xn…
> +
> +
> Causal Self-Attention Layer
> Layer Normalize
> Cross-Attention Layer
> Layer Normalize

Decoder    

> +
> +
> hnhnhn…
> Feedforward Layer
> Layer Normalize
> +
> hn
> Encoder
> Block 1
> Block 2
> Block 3
> y3y2y1…yn
> Decoder
> Block 1
> Block 2
> Block 3
> Linear Layer

Figure 10.16 The transformer block for the encoder and the decoder. Each decoder block has an extra cross-attention layer, which uses the output of the final encoder layer Henc =

h1, ..., ht to produce its key and value vectors. 

The cross attention thus allows the decoder to attend to each of the source language words as projected into the the entire encoder final output representations. The other attention layer in each decoder block, the self-attention layer, is the same causal (left-to-right) self-attention that we saw in Chapter 9. The self-attention in the encoder, however, is allowed to look ahead at the entire source language text. In training, just as for RNN encoder-decoders, we use teacher forcing, and train autoregressively, at each time step predicting the next token in the target language, using cross-entropy loss. 

## 10.7 Some practical details on building MT systems 

10.7.1 Tokenization 

Machine translation systems generally use a fixed vocabulary, A common way to generate this vocabulary is with the BPE or wordpiece algorithms sketched in Chap-wordpiece 

ter 2. Generally a shared vocabulary is used for the source and target languages, which makes it easy to copy tokens (like names) from source to target, so we build the wordpiece/BPE lexicon on a corpus that contains both source and target lan-guage data. Wordpieces use a special symbol at the beginning of each token; here’s a resulting tokenization from the Google MT system (Wu et al., 2016): 

words : Jet makers feud over seat width with big orders at stake 

wordpieces : J et makers fe ud over seat width with big orders at stake 

We gave the BPE algorithm in detail in Chapter 2; here are more details on the wordpiece algorithm, which is given a training corpus and a desired vocabulary size 10.7 • SOME PRACTICAL DETAILS ON BUILDING MT SYSTEMS 19 

V, and proceeds as follows: 1. Initialize the wordpiece lexicon with characters (for example a subset of Uni-code characters, collapsing all the remaining characters to a special unknown character token). 2. Repeat until there are V wordpieces: (a) Train an n-gram language model on the training corpus, using the current set of wordpieces. (b) Consider the set of possible new wordpieces made by concatenating two wordpieces from the current lexicon. Choose the one new wordpiece that most increases the language model probability of the training corpus. A vocabulary of 8K to 32K word pieces is commonly used. 

10.7.2 MT corpora 

Machine translation models are trained on a parallel corpus , sometimes called a parallel corpus 

bitext , a text that appears in two (or more) languages. Large numbers of paral-lel corpora are available. Some are governmental; the Europarl corpus (Koehn, Europarl 

2005), extracted from the proceedings of the European Parliament, contains between 400,000 and 2 million sentences each from 21 European languages. The United Na-tions Parallel Corpus contains on the order of 10 million sentences in the six official languages of the United Nations (Arabic, Chinese, English, French, Russian, Span-ish) Ziemski et al. (2016). Other parallel corpora have been made from movie and TV subtitles, like the OpenSubtitles corpus (Lison and Tiedemann, 2016), or from general web text, like the ParaCrawl corpus of 223 million sentence pairs between 23 EU languages and English extracted from the CommonCrawl Ba˜ n´ on et al. (2020). 

Sentence alignment 

Standard training corpora for MT come as aligned pairs of sentences. When creating new corpora, for example for underresourced languages or new domains, these sen-tence alignments must be created. Fig. 10.17 gives a sample hypothetical sentence alignment. F1: -Bonjour, dit le petit prince. 

> F2: -Bonjour, dit le marchand de pilules perfectionnées qui
> apaisent la soif.
> F3: On en avale une par semaine et l'on n'éprouve plus le
> besoin de boire.
> F4: -C’est une grosse économie de temps, dit le marchand.
> F5: Les experts ont fait des calculs.
> F6: On épargne cinquante-trois minutes par semaine.
> F7: “Moi, se dit le petit prince, si j'avais cinquante-trois minutes
> à dépenser, je marcherais tout doucement vers une fontaine..."
> E1: “Good morning," said the little prince.
> E2: “Good morning," said the merchant.
> E3: This was a merchant who sold pills that had
> been perfected to quench thirst.
> E4: You just swallow one pill a week and you
> won’t feel the need for anything to drink.
> E5: “They save a huge amount of time," said the merchant.
> E6: “Fifty −three minutes a week."
> E7: “If I had fifty −three minutes to spend?" said the
> little prince to himself.
> E8: “I would take a stroll to a spring of fresh water”

Figure 10.17 A sample alignment between sentences in English and French, with sentences extracted from Antoine de Saint-Exupery’s Le Petit Prince and a hypothetical translation. Sentence alignment takes sentences 

e1, ..., en, and f1, ..., fn and finds minimal sets of sentences that are translations of each other, including single sentence mappings like (e 1,f 1), (e 4,f 3), (e 5,f 4), (e 6,f 6) as well as 2-1 alignments (e 2/e 3,f 2), (e 7/e 8,f 7), and null alignments (f 5). 20 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

Given two documents that are translations of each other, we generally need two steps to produce sentence alignments: • a cost function that takes a span of source sentences and a span of target sen-tences and returns a score measuring how likely these spans are to be transla-tions. • an alignment algorithm that takes these scores to find a good alignment be-tween the documents. Since it is possible to induce multilingual sentence embeddings (Artetxe and Schwenk, 2019), cosine similarity of such embeddings provides a natural scoring function (Schwenk, 2018). Thompson and Koehn (2019) give the following cost function between two sentences or spans x,y from the source and target documents respectively: 

c(x, y) = (1 − cos (x, y)) nSents (x) nSents (y)

∑Ss=1 1 − cos (x, ys) + ∑Ss=1 1 − cos (xs, y) (10.23) 

where nSents () gives the number of sentences (this biases the metric toward many alignments of single sentences instead of aligning very large spans). The denom-inator helps to normalize the similarities, and so x1, ..., xS, y1, ..., yS, are randomly selected sentences sampled from the respective documents. Usually dynamic programming is used as the alignment algorithm (Gale and Church, 1993), in a simple extension of the minimum edit distance algorithm we introduced in Chapter 2. Finally, it’s helpful to do some corpus cleanup by removing noisy sentence pairs. This can involve handwritten rules to remove low-precision pairs (for example re-moving sentences that are too long, too short, have different URLs, or even pairs that are too similar, suggesting that they were copies rather than translations). Or pairs can be ranked by their multilingual embedding cosine score and low-scoring pairs discarded. 

10.7.3 Backtranslation 

We’re often short of data for training MT models, since parallel corpora may be limited for particular languages or domains. However, often we can find a large monolingual corpus, to add to the smaller parallel corpora that are available. 

Backtranslation is a way of making use of monolingual corpora in the target backtranslation 

language by creating synthetic bitexts. In backtranslation, we train an intermediate target-to-source MT system on the small bitext to translate the monolingual target data to the source language. Now we can add this synthetic bitext (natural target sentences, aligned with MT-produced source sentences) to our training data, and retrain our source-to-target MT model. For example suppose we want to translate from Navajo to English but only have a small Navajo-English bitext, although of course we can find lots of monolingual English data. We use the small bitext to build an MT engine going the other way (from English to Navajo). Once we translate the monolingual English text to Navajo, we can add this synthetic Navajo/English bitext to our training data. Backtranslation has various parameters. One is how we generate the backtrans-lated data; we can run the decoder in greedy inference, or use beam search. Or we can do sampling, or Monte Carlo search . In Monte Carlo decoding, at each Monte Carlo search 

timestep, instead of always generating the word with the highest softmax proba-bility, we roll a weighted die, and use it to choose the next word according to its 10.8 • MT E VALUATION 21 

softmax probability. This works just like the sampling algorithm we saw in Chap-ter 3 for generating random sentences from n-gram language models. Imagine there are only 4 words and the softmax probability distribution at time t is ( the : 0.6, green :0.2, a: 0.1, witch : 0.1). We roll a weighted die, with the 4 sides weighted 0.6, 0.2, 0.1, and 0.1, and chose the word based on which side comes up. Another parameter is the ratio of backtranslated data to natural bitext data; we can choose to upsample the bitext data (include multiple copies of each sentence). In general backtranslation works surprisingly well; one estimate suggests that a system trained on backtranslated text gets about 2/3 of the gain as would training on the same amount of natural bitext (Edunov et al., 2018). 

## 10.8 MT Evaluation 

Translations are evaluated along two dimensions: 1. adequacy: how well the translation captures the exact meaning of the source adequacy 

sentence. Sometimes called faithfulness or fidelity .2. fluency: how fluent the translation is in the target language (is it grammatical, fluency 

clear, readable, natural). Using humans to evaluate is most accurate, but automatic metrics are also used for convenience. 

10.8.1 Using Human Raters to Evaluate MT 

The most accurate evaluations use human raters, such as online crowdworkers, to evaluate each translation along the two dimensions. For example, along the dimen-sion of fluency , we can ask how intelligible, how clear, how readable, or how natural the MT output (the target text) is. We can give the raters a scale, for example, from 1 (totally unintelligible) to 5 (totally intelligible, or 1 to 100, and ask them to rate each sentence or paragraph of the MT output. We can do the same thing to judge the second dimension, adequacy , using raters to assign scores on a scale. If we have bilingual raters, we can give them the source sentence and a proposed target sentence, and rate, on a 5-point or 100-point scale, how much of the information in the source was preserved in the target. If we only have monolingual raters but we have a good human translation of the source text, we can give the monolingual raters the human reference translation and a target machine translation and again rate how much information is preserved. An alternative is to do ranking : give the raters a pair of candidate translations, and ask them which one ranking 

they prefer. Training of human raters (who are often online crowdworkers) is essential; raters without translation expertise find it difficult to separate fluency and adequacy, and so training includes examples carefully distinguishing these. Raters often disagree (sources sentences may be ambiguous, raters will have different world knowledge, raters may apply scales differently). It is therefore common to remove outlier raters, and (if we use a fine-grained enough scale) normalizing raters by subtracting the mean from their scores and dividing by the variance. 22 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

10.8.2 Automatic Evaluation 

While humans produce the best evaluations of machine translation output, running a human evaluation can be time consuming and expensive. For this reason automatic metrics are often used. Automatic metrics are less accurate than human evaluation, but can help test potential system improvements, and even be used as an automatic loss function for training. In this section we introduce two families of such metrics, those based on character- or word-overlap and those based on embedding similarity. 

Automatic Evaluation by Character Overlap: chrF 

The simplest and most robust metric for MT evaluation is called chrF , which stands chrF 

for character F-score (Popovi´ c, 2015). chrF (along with many other earlier related metrics like BLEU, METEOR, TER, and others) is based on a simple intuition de-rived from the pioneering work of Miller and Beebe-Center (1956): a good machine translation will tend to contain characters and words that occur in a human trans-lation of the same sentence. Consider a test set from a parallel corpus, in which each source sentence has both a gold human target translation and a candidate MT translation we’d like to evaluate. The chrF metric ranks each MT target sentence by a function of the number of character n-gram overlaps with the human translation. Given the hypothesis and the reference, chrF is given a parameter k indicating the length of character n-grams to be considered, and computes the average of the 

k precisions (unigram precision, bigram, and so on) and the average of the k recalls (unigram recall, bigram recall, etc.): 

chrP percentage of character 1-grams, 2-grams, ..., k-grams in the hypothesis that occur in the reference, averaged. 

chrR percentage of character 1-grams, 2-grams,..., k-grams in the reference that occur in the hypothesis, averaged. The metric then computes an F-score by combining chrP and chrR using a weighting parameter β . It is common to set β = 2, thus weighing recall twice as much as precision: chrF β = ( 1 + β 2) chrP · chrR 

β 2 · chrP + chrR (10.24) 

For β = 2, that would be: chrF2 = 5 · chrP · chrR 4 · chrP + chrR For example, consider two hypotheses that we’d like to score against the refer-ence translation witness for the past . Here are the hypotheses along with chrF values computed using parameters k = β = 2 (in real examples, k would be a higher number like 6): REF: witness for the past, 

HYP1: witness of the past, chrF2,2 = .86 HYP2: past witness chrF2,2 = .62 Let’s see how we computed that chrF value for HYP1 (we’ll leave the compu-tation of the chrF value for HYP2 as an exercise for the reader). First, chrF ignores spaces, so we’ll remove them from both the reference and hypothesis: REF: witnessforthepast, (18 unigrams, 17 bigrams) HYP1: witnessofthepast, (17 unigrams, 16 bigrams) 10.8 • MT E VALUATION 23 

Next let’s see how many unigrams and bigrams match between the reference and hypothesis: unigrams that match: w i t n e s s f o t h e p a s t , (17 unigrams) bigrams that match: wi it tn ne es ss th he ep pa as st t, (13 bigrams) We use that to compute the unigram and bigram precisions and recalls: unigram P: 17/17 = 1 unigram R: 17/18 = .944 bigram P: 13/16 = .813 bigram R: 13/17 = .765 Finally we average to get chrP and chrR, and compute the F-score: chrP = ( 17 /17 + 13 /16 )/2 = .906 chrR = ( 17 /18 + 13 /17 )/2 = .855 chrF2,2 = 5 chrP ∗ chrR 4chrP + chrR = .86 chrF is simple, robust, and correlates very well with human judgments in many languages (Kocmi et al., 2021). There are various alternative overlap metrics. For example, before the development of chrF, it was common to use a word-based overlap metric called BLEU (for BiLingual Evaluation Understudy), that is purely precision-based rather than combining precision and recall (Papineni et al., 2002). The BLEU score for a corpus of candidate translation sentences is a function of the n-gram word precision over all the sentences combined with a brevity penalty computed over the corpus as a whole. Because BLEU is a word-based metric, it is very sensitive to word tokenization, making it difficult to compare across situations, and doesn’t work as well in languages with complex morphology. 

Statistical Significance Testing for MT evals 

Character or word overlap-based metrics like chrF (or BLEU, or etc.) are mainly used to compare two systems, with the goal of answering questions like: did the new algorithm we just invented improve our MT system? To know if the difference between the chrF scores of two MT systems is a significant difference, we use the paired bootstrap test, or the similar randomization test. To get a confidence interval on a single chrF score using the bootstrap test, recall from Section ?? that we take our test set (or devset) and create thousands of pseudo-testsets by repeatedly sampling with replacement from the original test set. We now compute the chrF score of each of the pseudo-testsets. If we drop the top 2.5% and bottom 2.5% of the scores, the remaining scores will give us the 95% confidence interval for the chrF score of our system. To compare two MT systems A and B, we draw the same set of pseudo-testsets, and compute the chrF scores for each of them. We then compute the percentage of pseudo-test-sets in which A has a higher chrF score than B. 

chrF: Limitations 

While automatic character and word-overlap metrics like chrF or BLEU are useful, they have important limitations. chrF is very local: a large phrase that is moved around might barely change the chrF score at all, and chrF can’t evaluate cross-sentence properties of a document like its discourse coherence (Chapter 22). chrF and similar automatic metrics also do poorly at comparing very different kinds of systems, such as comparing human-aided translation against machine translation, or 24 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

different machine translation architectures against each other (Callison-Burch et al., 2006). Instead, automatic overlap metrics like chrF are most appropriate when eval-uating changes to a single system. 

10.8.3 Automatic Evaluation: Embedding-Based Methods 

The chrF metric is based on measuring the exact character n-grams a human refer-ence and candidate machine translation have in common. However, this criterion is overly strict, since a good translation may use alternate words or paraphrases. A solution first pioneered in early metrics like METEOR (Banerjee and Lavie, 2005) was to allow synonyms to match between the reference x and candidate ˜ x. More recent metrics use BERT or other embeddings to implement this intuition. For example, in some situations we might have datasets that have human as-sessments of translation quality. Such datasets consists of tuples (x, ˜x, r), where 

x = ( x1, . . . , xn) is a reference translation, ˜ x = ( ˜x1, . . . , ˜xm) is a candidate machine translation, and r ∈ R is a human rating that expresses the quality of ˜ x with respect to x. Given such data, algorithms like COMET (Rei et al., 2020) BLEURT (Sellam et al., 2020) train a predictor on the human-labeled datasets, for example by passing 

x and ˜ x through a version of BERT (trained with extra pretraining, and then fine-tuned on the human-labeled sentences), followed by a linear layer that is trained to predict r. The output of such models correlates highly with human labels. In other cases, however, we don’t have such human-labeled datasets. In that case we can measure the similarity of x and ˜ x by the similarity of their embeddings. The BERTS CORE algorithm (Zhang et al., 2020) shown in Fig. 10.18, for example, passes the reference x and the candidate ˜ x through BERT, computing a BERT em-bedding for each token xi and ˜ x j. Each pair of tokens (xi, ˜x j) is scored by its cosine 

xi· ˜x j

|xi|| ˜x j | . Each token in x is matched to a token in ˜ x to compute recall, and each token in ˜x is matched to a token in x to compute precision (with each token greedily matched to the most similar token in the corresponding sentence). BERTS CORE provides precision and recall (and hence F 1): 

RBERT = 1

|x|

∑

xi∈x

max 

˜x j ∈ ˜x xi · ˜x j PBERT = 1

| ˜x|

∑

˜x j ∈ ˜x

max 

xi∈x xi · ˜x j (10.25) Published as a conference paper at ICLR 2020 

Reference 

the weather is 

cold today 

Candidate 

it is freezing today 

Candidate 

Contextual 

Embedding 

Pairwise Cosine 

Similarity 

RBERT = (0 .713  1.27)+(0 .515  7.94)+ ... 

1.27+7 .94+1 .82+7 .90+8 .88 <latexit sha1_base64="OJyoKlmBAgUA0KDtUcsH/di5BlI=">AAACSHicbZDLattAFIaPnLRJ3JvTLrsZYgoJAqFxGqwsCqal0FVJQ5wELCNG41EyZHRh5ijECL1EnqAv002X2eUZsumipXRR6Mj2Ipf+MPDznXM4Z/64UNKg7187raXlR49XVtfaT54+e/6is/7y0OSl5mLIc5Xr45gZoWQmhihRieNCC5bGShzFZx+a+tG50Ebm2QFOCzFO2UkmE8kZWhR1ov2oClFcYPX+4/5BXZN3JEw049Wm7/XpdogyFYZQr9ffci3aoTsL1Pd23265oZrkaOqqaXAb5FIv6DXOdwMvCOqo0/U9fyby0NCF6Q52/15+BYC9qHMVTnJepiJDrpgxI+oXOK6YRsmVqNthaUTB+Bk7ESNrM2aPGVezIGryxpIJSXJtX4ZkRm9PVCw1ZprGtjNleGru1xr4v9qoxCQYVzIrShQZny9KSkUwJ02qZCK14Kim1jCupb2V8FNmc0SbfduGQO9/+aE57HnU9+gX2h18hrlW4TVswCZQ6MMAPsEeDIHDN7iBn/DL+e78cH47f+atLWcx8wruqNX6B8dUrVw=</latexit> <latexit sha1_base64="RInTcZkWiVBnf/ncBstCvatCtG4=">AAACSHicbZDPShxBEMZ7Nproxugaj14al4AyMEyvyoyHwGIQPImKq8LOMvT09mhjzx+6a0KWYV4iL5EnySXH3HwGLx4U8SDYs7sHo/mg4eNXVVT1F+VSaHDda6vxbmb2/Ye5+ebHhU+LS63lz6c6KxTjPZbJTJ1HVHMpUt4DAZKf54rTJJL8LLr6VtfPvnOlRZaewCjng4RepCIWjIJBYSs8DssA+A8od/eOT6oKf8VBrCgr113HI5sBiIRrTJyOt2EbtE22p8hzdrY27EAOM9BVWTfYNbKJ43dq59q+4/tV2Gq7jjsWfmvI1LS7O08/f3nLi4dh628wzFiR8BSYpFr3iZvDoKQKBJO8agaF5jllV/SC941NqTlmUI6DqPAXQ4Y4zpR5KeAxfTlR0kTrURKZzoTCpX5dq+H/av0CYn9QijQvgKdssiguJIYM16nioVCcgRwZQ5kS5lbMLqnJEUz2TRMCef3lt+a04xDXIUek3T1AE82hVbSG1hFBHuqifXSIeoih3+gG3aF76491az1Yj5PWhjWdWUH/qNF4BkPYrbk=</latexit> <latexit sha1_base64="RInTcZkWiVBnf/ncBstCvatCtG4=">AAACSHicbZDPShxBEMZ7Nproxugaj14al4AyMEyvyoyHwGIQPImKq8LOMvT09mhjzx+6a0KWYV4iL5EnySXH3HwGLx4U8SDYs7sHo/mg4eNXVVT1F+VSaHDda6vxbmb2/Ye5+ebHhU+LS63lz6c6KxTjPZbJTJ1HVHMpUt4DAZKf54rTJJL8LLr6VtfPvnOlRZaewCjng4RepCIWjIJBYSs8DssA+A8od/eOT6oKf8VBrCgr113HI5sBiIRrTJyOt2EbtE22p8hzdrY27EAOM9BVWTfYNbKJ43dq59q+4/tV2Gq7jjsWfmvI1LS7O08/f3nLi4dh628wzFiR8BSYpFr3iZvDoKQKBJO8agaF5jllV/SC941NqTlmUI6DqPAXQ4Y4zpR5KeAxfTlR0kTrURKZzoTCpX5dq+H/av0CYn9QijQvgKdssiguJIYM16nioVCcgRwZQ5kS5lbMLqnJEUz2TRMCef3lt+a04xDXIUek3T1AE82hVbSG1hFBHuqifXSIeoih3+gG3aF76491az1Yj5PWhjWdWUH/qNF4BkPYrbk=</latexit> <latexit sha1_base64="fGWl4NCvlvtMu17rjLtk25oWpdc=">AAACSHicbZBLS+RAFIUrPT7bVzsu3RQ2ghIIqVbpuBgQRZiVqNgqdJpQqa5oYeVB1Y1ME/Lz3Lic3fwGNy6UwZ2VNgtfBwoO372Xe+uEmRQaXPef1fgxMTk1PTPbnJtfWFxqLf8812muGO+xVKbqMqSaS5HwHgiQ/DJTnMah5BfhzUFVv7jlSos0OYNRxgcxvUpEJBgFg4JWcBoUPvA/UOwfnp6VJf6F/UhRVmy4Tpds+SBirjFxOt1N26AdslOjrrO7vWn7cpiCLouqwa6QTRyvUznX9hzPK4NW23XcsfBXQ2rTRrWOg9Zff5iyPOYJMEm17hM3g0FBFQgmedn0c80zym7oFe8bm1BzzKAYB1HidUOGOEqVeQngMX0/UdBY61Ecms6YwrX+XKvgd7V+DpE3KESS5cAT9rYoyiWGFFep4qFQnIEcGUOZEuZWzK6pyRFM9k0TAvn85a/mvOMQ1yEnpL13VMcxg1bRGtpABHXRHvqNjlEPMXSHHtATerburUfrv/Xy1tqw6pkV9EGNxisxMKq0</latexit> 

1.27 

7.94 

1.82 

7.90 

8.88 

idf 

weights 

Importance Weighting 

(Optional) 

Maximum Similarity 

x<latexit sha1_base64="f2yzimwbR/Dgjzp6tZ360fHRqNI=">AAAB6HicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cW7Ae0oWy2k3btZhN2N2IJ/QVePCji1Z/kzX/jts1BWx8MPN6bYWZekAiujet+O4W19Y3NreJ2aWd3b/+gfHjU0nGqGDZZLGLVCahGwSU2DTcCO4lCGgUC28H4dua3H1FpHst7M0nQj+hQ8pAzaqzUeOqXK27VnYOsEi8nFchR75e/eoOYpRFKwwTVuuu5ifEzqgxnAqelXqoxoWxMh9i1VNIItZ/ND52SM6sMSBgrW9KQufp7IqOR1pMosJ0RNSO97M3E/7xuasJrP+MySQ1KtlgUpoKYmMy+JgOukBkxsYQyxe2thI2ooszYbEo2BG/55VXSuqh6btVrXFZqN3kcRTiBUzgHD66gBndQhyYwQHiGV3hzHpwX5935WLQWnHzmGP7A+fwB5jmM/A==</latexit> <latexit sha1_base64="f2yzimwbR/Dgjzp6tZ360fHRqNI=">AAAB6HicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cW7Ae0oWy2k3btZhN2N2IJ/QVePCji1Z/kzX/jts1BWx8MPN6bYWZekAiujet+O4W19Y3NreJ2aWd3b/+gfHjU0nGqGDZZLGLVCahGwSU2DTcCO4lCGgUC28H4dua3H1FpHst7M0nQj+hQ8pAzaqzUeOqXK27VnYOsEi8nFchR75e/eoOYpRFKwwTVuuu5ifEzqgxnAqelXqoxoWxMh9i1VNIItZ/ND52SM6sMSBgrW9KQufp7IqOR1pMosJ0RNSO97M3E/7xuasJrP+MySQ1KtlgUpoKYmMy+JgOukBkxsYQyxe2thI2ooszYbEo2BG/55VXSuqh6btVrXFZqN3kcRTiBUzgHD66gBndQhyYwQHiGV3hzHpwX5935WLQWnHzmGP7A+fwB5jmM/A==</latexit> <latexit sha1_base64="f2yzimwbR/Dgjzp6tZ360fHRqNI=">AAAB6HicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cW7Ae0oWy2k3btZhN2N2IJ/QVePCji1Z/kzX/jts1BWx8MPN6bYWZekAiujet+O4W19Y3NreJ2aWd3b/+gfHjU0nGqGDZZLGLVCahGwSU2DTcCO4lCGgUC28H4dua3H1FpHst7M0nQj+hQ8pAzaqzUeOqXK27VnYOsEi8nFchR75e/eoOYpRFKwwTVuuu5ifEzqgxnAqelXqoxoWxMh9i1VNIItZ/ND52SM6sMSBgrW9KQufp7IqOR1pMosJ0RNSO97M3E/7xuasJrP+MySQ1KtlgUpoKYmMy+JgOukBkxsYQyxe2thI2ooszYbEo2BG/55VXSuqh6btVrXFZqN3kcRTiBUzgHD66gBndQhyYwQHiGV3hzHpwX5935WLQWnHzmGP7A+fwB5jmM/A==</latexit> <latexit sha1_base64="f2yzimwbR/Dgjzp6tZ360fHRqNI=">AAAB6HicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cW7Ae0oWy2k3btZhN2N2IJ/QVePCji1Z/kzX/jts1BWx8MPN6bYWZekAiujet+O4W19Y3NreJ2aWd3b/+gfHjU0nGqGDZZLGLVCahGwSU2DTcCO4lCGgUC28H4dua3H1FpHst7M0nQj+hQ8pAzaqzUeOqXK27VnYOsEi8nFchR75e/eoOYpRFKwwTVuuu5ifEzqgxnAqelXqoxoWxMh9i1VNIItZ/ND52SM6sMSBgrW9KQufp7IqOR1pMosJ0RNSO97M3E/7xuasJrP+MySQ1KtlgUpoKYmMy+JgOukBkxsYQyxe2thI2ooszYbEo2BG/55VXSuqh6btVrXFZqN3kcRTiBUzgHD66gBndQhyYwQHiGV3hzHpwX5935WLQWnHzmGP7A+fwB5jmM/A==</latexit> 

ˆx<latexit sha1_base64="5QTnVRVSrnyzznVU7d5bF5u03Iw=">AAAB7nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cK9gPaUDbbTbt0swm7E7GE/ggvHhTx6u/x5r9x0+agrQ8GHu/NMDMvSKQw6LrfTmltfWNzq7xd2dnd2z+oHh61TZxqxlsslrHuBtRwKRRvoUDJu4nmNAok7wST29zvPHJtRKwecJpwP6IjJULBKFqp0x9TzJ5mg2rNrbtzkFXiFaQGBZqD6ld/GLM04gqZpMb0PDdBP6MaBZN8VumnhieUTeiI9yxVNOLGz+bnzsiZVYYkjLUthWSu/p7IaGTMNApsZ0RxbJa9XPzP66UYXvuZUEmKXLHFojCVBGOS/06GQnOGcmoJZVrYWwkbU00Z2oQqNgRv+eVV0r6oe27du7+sNW6KOMpwAqdwDh5cQQPuoAktYDCBZ3iFNydxXpx352PRWnKKmWP4A+fzB7A8j8k=</latexit> <latexit sha1_base64="5QTnVRVSrnyzznVU7d5bF5u03Iw=">AAAB7nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cK9gPaUDbbTbt0swm7E7GE/ggvHhTx6u/x5r9x0+agrQ8GHu/NMDMvSKQw6LrfTmltfWNzq7xd2dnd2z+oHh61TZxqxlsslrHuBtRwKRRvoUDJu4nmNAok7wST29zvPHJtRKwecJpwP6IjJULBKFqp0x9TzJ5mg2rNrbtzkFXiFaQGBZqD6ld/GLM04gqZpMb0PDdBP6MaBZN8VumnhieUTeiI9yxVNOLGz+bnzsiZVYYkjLUthWSu/p7IaGTMNApsZ0RxbJa9XPzP66UYXvuZUEmKXLHFojCVBGOS/06GQnOGcmoJZVrYWwkbU00Z2oQqNgRv+eVV0r6oe27du7+sNW6KOMpwAqdwDh5cQQPuoAktYDCBZ3iFNydxXpx352PRWnKKmWP4A+fzB7A8j8k=</latexit> <latexit sha1_base64="5QTnVRVSrnyzznVU7d5bF5u03Iw=">AAAB7nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cK9gPaUDbbTbt0swm7E7GE/ggvHhTx6u/x5r9x0+agrQ8GHu/NMDMvSKQw6LrfTmltfWNzq7xd2dnd2z+oHh61TZxqxlsslrHuBtRwKRRvoUDJu4nmNAok7wST29zvPHJtRKwecJpwP6IjJULBKFqp0x9TzJ5mg2rNrbtzkFXiFaQGBZqD6ld/GLM04gqZpMb0PDdBP6MaBZN8VumnhieUTeiI9yxVNOLGz+bnzsiZVYYkjLUthWSu/p7IaGTMNApsZ0RxbJa9XPzP66UYXvuZUEmKXLHFojCVBGOS/06GQnOGcmoJZVrYWwkbU00Z2oQqNgRv+eVV0r6oe27du7+sNW6KOMpwAqdwDh5cQQPuoAktYDCBZ3iFNydxXpx352PRWnKKmWP4A+fzB7A8j8k=</latexit> <latexit sha1_base64="5QTnVRVSrnyzznVU7d5bF5u03Iw=">AAAB7nicbVBNS8NAEJ3Ur1q/qh69LBbBU0lE0GPRi8cK9gPaUDbbTbt0swm7E7GE/ggvHhTx6u/x5r9x0+agrQ8GHu/NMDMvSKQw6LrfTmltfWNzq7xd2dnd2z+oHh61TZxqxlsslrHuBtRwKRRvoUDJu4nmNAok7wST29zvPHJtRKwecJpwP6IjJULBKFqp0x9TzJ5mg2rNrbtzkFXiFaQGBZqD6ld/GLM04gqZpMb0PDdBP6MaBZN8VumnhieUTeiI9yxVNOLGz+bnzsiZVYYkjLUthWSu/p7IaGTMNApsZ0RxbJa9XPzP66UYXvuZUEmKXLHFojCVBGOS/06GQnOGcmoJZVrYWwkbU00Z2oQqNgRv+eVV0r6oe27du7+sNW6KOMpwAqdwDh5cQQPuoAktYDCBZ3iFNydxXpx352PRWnKKmWP4A+fzB7A8j8k=</latexit> 

> Reference

Figure 1: Illustration of the computation of the recall metric R BERT . Given the reference x and candidate ˆx, we compute BERT embeddings and pairwise cosine similarity. We highlight the greedy matching in red, and include the optional idf importance weighting. We experiment with different models (Section 4), using the tokenizer provided with each model. Given a tokenized reference sentence x = hx 1 , . . . , x k i, the embedding model generates a se-quence of vectors hx 1 , . . . , x k i. Similarly, the tokenized candidate ˆx = hˆx 1 , . . . , ˆx m i is mapped to hˆx 1 , . . . , ˆx l i. The main model we use is BERT, which tokenizes the input text into a sequence of word pieces (Wu et al., 2016), where unknown words are split into several commonly observed sequences of characters. The representation for each word piece is computed with a Transformer encoder (Vaswani et al., 2017) by repeatedly applying self-attention and nonlinear transformations in an alternating fashion. BERT embeddings have been shown to benefit various NLP tasks (Devlin et al., 2019; Liu, 2019; Huang et al., 2019; Yang et al., 2019a). 

Similarity Measure The vector representation allows for a soft measure of similarity instead of exact-string (Papineni et al., 2002) or heuristic (Banerjee & Lavie, 2005) matching. The cosine 

Figure 10.18 The computation of BERTS CORE recall from reference x and candidate ˆ x,from Figure 1 in Zhang et al. (2020). This version shows an extended version of the metric in which tokens are also weighted by their idf values. 10.9 • BIAS AND ETHICAL ISSUES 25 

## 10.9 Bias and Ethical Issues 

Machine translation raises many of the same ethical issues that we’ve discussed in earlier chapters. For example, consider MT systems translating from Hungarian (which has the gender neutral pronoun ˝o) or Spanish (which often drops pronouns) into English (in which pronouns are obligatory, and they have grammatical gender). When translating a reference to a person described without specified gender, MT systems often default to male gender (Schiebinger 2014, Prates et al. 2019). And MT systems often assign gender according to culture stereotypes of the sort we saw in Section ?? . Fig. 10.19 shows examples from Prates et al. (2019), in which Hun-garian gender-neutral ˝o is a nurse is translated with she , but gender-neutral ˝o is a CEO is translated with he . Prates et al. (2019) find that these stereotypes can’t com-pletely be accounted for by gender bias in US labor statistics, because the biases are 

amplified by MT systems, with pronouns being mapped to male or female gender with a probability higher than if the mapping was based on actual labor employment statistics. 

Hungarian (gender neutral) source English MT output 

˝o egy ´ apol´ o she is a nurse ˝o egy tud´ os he is a scientist ˝o egy m´ ern¨ ok he is an engineer ˝o egy p´ ek he is a baker ˝o egy tan´ ar she is a teacher ˝o egy vesk¨ uv˝ oszervez˝ o she is a wedding organizer ˝o egy vez´ erigazgat´ o he is a CEO  

> Figure 10.19 When translating from gender-neutral languages like Hungarian into English, current MT systems interpret people from traditionally male-dominated occupations as male, and traditionally female-dominated occupations as female (Prates et al., 2019).

Similarly, a recent challenge set, the WinoMT dataset (Stanovsky et al., 2019) shows that MT systems perform worse when they are asked to translate sentences that describe people with non-stereotypical gender roles, like “The doctor asked the nurse to help her in the operation”. Many ethical questions in MT require further research. One open problem is developing metrics for knowing what our systems don’t know. This is because MT systems can be used in urgent situations where human translators may be unavailable or delayed: in medical domains, to help translate when patients and doctors don’t speak the same language, or in legal domains, to help judges or lawyers communi-cate with witnesses or defendants. In order to ‘do no harm’, systems need ways to assign confidence values to candidate translations, so they can abstain from giving confidence 

incorrect translations that may cause harm. Another is the need for low-resource algorithms that can translate to and from all the world’s languages, the vast majority of which do not have large parallel train-ing texts available. This problem is exacerbated by the tendency of many MT ap-proaches to focus on the case where one of the languages is English (Anastasopou-los and Neubig, 2020). ∀ et al. (2020) propose a participatory design process to encourage content creators, curators, and language technologists who speak these 

low-resourced languages to participate in developing MT algorithms. They pro-low-resourced languages 

vide online groups, mentoring, and infrastructure, and report on a case study on developing MT algorithms for low-resource African languages. 26 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

## 10.10 Summary 

Machine translation is one of the most widely used applications of NLP, and the encoder-decoder model, first developed for MT is a key tool that has applications throughout NLP. • Languages have divergences , both structural and lexical, that make translation difficult. • The linguistic field of typology investigates some of these differences; lan-guages can be classified by their position along typological dimensions like whether verbs precede their objects. • Encoder-decoder networks (either for RNNs or transformers) are composed of an encoder network that takes an input sequence and creates a contextu-alized representation of it, the context . This context representation is then passed to a decoder which generates a task-specific output sequence. • The attention mechanism in RNNs, and cross-attention in transformers, al-lows the decoder to view information from all the hidden states of the encoder. • For the decoder, choosing the single most probable token to generate at each step is called greedy decoding. • In beam search , instead of choosing the best token to generate at each timestep, we keep k possible tokens at each step. This fixed-size memory footprint k is called the beam width .• Machine translation models are trained on a parallel corpus , sometimes called a bitext , a text that appears in two (or more) languages. • Backtranslation is a way of making use of monolingual corpora in the target language by running a pilot MT engine backwards to create synthetic bitexts. • MT is evaluated by measuring a translation’s adequacy (how well it captures the meaning of the source sentence) and fluency (how fluent or natural it is in the target language). Human evaluation is the gold standard, but automatic evaluation metrics like chrF , which measure character n-gram overlap with human translations, or more recent metrics based on embedding similarity, are also commonly used. 

## Bibliographical and Historical Notes 

MT was proposed seriously by the late 1940s, soon after the birth of the computer (Weaver, 1949/1955). In 1954, the first public demonstration of an MT system pro-totype (Dostert, 1955) led to great excitement in the press (Hutchins, 1997). The next decade saw a great flowering of ideas, prefiguring most subsequent develop-ments. But this work was ahead of its time—implementations were limited by, for example, the fact that pending the development of disks there was no good way to store dictionary information. As high-quality MT proved elusive (Bar-Hillel, 1960), there grew a consensus on the need for better evaluation and more basic research in the new fields of for-mal and computational linguistics. This consensus culminated in the famously crit-ical ALPAC (Automatic Language Processing Advisory Committee) report of 1966 (Pierce et al., 1966) that led in the mid 1960s to a dramatic cut in funding for MT BIBLIOGRAPHICAL AND HISTORICAL NOTES 27 

in the US. As MT research lost academic respectability, the Association for Ma-chine Translation and Computational Linguistics dropped MT from its name. Some MT developers, however, persevered, and there were early MT systems like M´ et´ eo, which translated weather forecasts from English to French (Chandioux, 1976), and industrial systems like Systran. In the early years, the space of MT architectures spanned three general mod-els. In direct translation , the system proceeds word-by-word through the source-language text, translating each word incrementally. Direct translation uses a large bilingual dictionary, each of whose entries is a small program with the job of trans-lating one word. In transfer approaches, we first parse the input text and then ap-ply rules to transform the source-language parse into a target language parse. We then generate the target language sentence from the parse tree. In interlingua ap-proaches, we analyze the source language text into some abstract meaning repre-sentation, called an interlingua . We then generate into the target language from this interlingual representation. A common way to visualize these three early ap-proaches was the Vauquois triangle shown in Fig. 10.20. The triangle shows the Vauquois triangle 

increasing depth of analysis required (on both the analysis and generation end) as we move from the direct approach through transfer approaches to interlingual ap-proaches. In addition, it shows the decreasing amount of transfer knowledge needed as we move up the triangle, from huge amounts of transfer at the direct level (al-most all knowledge is transfer knowledge for each word) through transfer (transfer rules only for parse trees or thematic roles) through interlingua (no specific transfer knowledge). We can view the encoder-decoder network as an interlingual approach, with attention acting as an integration of direct and transfer, allowing words or their representations to be directly accessed by the decoder. source 

> text
> target
> text
> Direct Translation
> Transfer
> Interlingua
> Source Text:
> Semantic/Syntactic
> Structure
> Target Text:
> Semantic/Syntactic
> Structure
> source language
> analysis
> source language
> analysis
> target language
> generation

Figure 10.20 The Vauquois (1968) triangle. 

Statistical methods began to be applied around 1990, enabled first by the devel-opment of large bilingual corpora like the Hansard corpus of the proceedings of the Canadian Parliament, which are kept in both French and English, and then by the growth of the Web. Early on, a number of researchers showed that it was possible to extract pairs of aligned sentences from bilingual corpora, using words or simple cues like sentence length (Kay and R¨ oscheisen 1988, Gale and Church 1991, Gale and Church 1993, Kay and R¨ oscheisen 1993). At the same time, the IBM group, drawing directly on the noisy channel model for speech recognition, proposed two related paradigms for statistical MT . These statistical MT 

include the generative algorithms that became known as IBM Models 1 through IBM Models 

5, implemented in the Candide system. The algorithms (except for the decoder) Candide 

were published in full detail— encouraged by the US government who had par-28 CHAPTER 10 • MACHINE TRANSLATION AND ENCODER -D ECODER MODELS 

tially funded the work— which gave them a huge impact on the research community (Brown et al. 1990, Brown et al. 1993). The group also developed a discriminative approach, called MaxEnt (for maximum entropy, an alternative formulation of logis-tic regression), which allowed many features to be combined discriminatively rather than generatively (Berger et al., 1996), which was further developed by Och and Ney (2002). By the turn of the century, most academic research on machine translation used statistical MT. An extended approach, called phrase-based translation was devel-phrase-based translation 

oped, based on inducing translations for phrase-pairs (Och 1998, Marcu and Wong 2002, Koehn et al. (2003), Och and Ney 2004, Deng and Byrne 2005, inter alia). Once automatic metrics like BLEU were developed (Papineni et al., 2002), use log linear formulation (Och and Ney, 2004) to directly optimize evaluation metrics like BLEU in a method known as Minimum Error Rate Training , or MERT (Och, MERT 

2003), also drawing from speech recognition models (Chou et al., 1993). Toolkits like GIZA (Och and Ney, 2003) and Moses (Koehn et al. 2006, Zens and Ney 2007) Moses 

were widely used. There were also approaches around the turn of the century that were based on syntactic structure (Chapter 12). Models based on transduction grammars (also transduction grammars 

called synchronous grammars assign a parallel syntactic tree structure to a pair of sentences in different languages, with the goal of translating the sentences by ap-plying reordering operations on the trees. From a generative perspective, we can view a transduction grammar as generating pairs of aligned sentences in two lan-guages. Some of the most widely used models included the inversion transduction grammar (Wu, 1996) and synchronous context-free grammars (Chiang, 2005),  

> inversion transduction grammar

Neural networks had been applied at various times to various aspects of machine translation; for example Schwenk et al. (2006) showed how to use neural language models to replace n-gram language models in a Spanish-English system based on IBM Model 4. The modern neural encoder-decoder approach was pioneered by Kalchbrenner and Blunsom (2013), who used a CNN encoder and an RNN decoder. Cho et al. (2014) (who coined the name “encoder-decoder”) and Sutskever et al. (2014) then showed how to use extended RNNs for both encoder and decoder. The idea that a generative decoder should take as input a soft weighting of the inputs, the central idea of attention, was first developed by Graves (2013) in the context of handwriting recognition. Bahdanau et al. (2015) extended the idea, named it “attention” and applied it to MT. The transformer encoder-decoder was proposed by Vaswani et al. (2017) (see the History section of Chapter 9). Beam-search has an interesting relationship with human language processing; (Meister et al., 2020) show that beam search enforces the cognitive property of uni-form information density in text. Uniform information density is the hypothe-sis that human language processors tend to prefer to distribute information equally across the sentence (Jaeger and Levy, 2007). Research on evaluation of machine translation began quite early. Miller and Beebe-Center (1956) proposed a number of methods drawing on work in psycholin-guistics. These included the use of cloze and Shannon tasks to measure intelligibility as well as a metric of edit distance from a human translation, the intuition that un-derlies all modern overlap-based automatic evaluation metrics. The ALPAC report included an early evaluation study conducted by John Carroll that was extremely in-fluential (Pierce et al., 1966, Appendix 10). Carroll proposed distinct measures for fidelity and intelligibility, and had raters score them subjectively on 9-point scales. Much early evaluation work focuses on automatic word-overlap metrics like BLEU EXERCISES 29 

(Papineni et al., 2002), NIST (Doddington, 2002), TER (Translation Error Rate) 

(Snover et al., 2006), Precision and Recall (Turian et al., 2003), and METEOR 

(Banerjee and Lavie, 2005); character n-gram overlap methods like chrF (Popovi´ c, 2015) came later. More recent evaluation work, echoing the ALPAC report, has emphasized the importance of careful statistical methodology and the use of human evaluation (Kocmi et al., 2021; Marie et al., 2021). The early history of MT is surveyed in Hutchins 1986 and 1997; Nirenburg et al. (2002) collects early readings. See Croft (1990) or Comrie (1989) for introductions to linguistic typology. 

## Exercises 

10.1 Compute by hand the chrF2,2 score for HYP2 on page 22 (the answer should round to .62). 30 Chapter 10 • Machine Translation and Encoder-Decoder Models 

Anastasopoulos, A. and G. Neubig. 2020. Should all cross-lingual embeddings speak English? ACL .Artetxe, M. and H. Schwenk. 2019. Massively multilingual sentence embeddings for zero-shot cross-lingual transfer and beyond. TACL , 7:597–610. Bahdanau, D., K. H. Cho, and Y. Bengio. 2015. Neural ma-chine translation by jointly learning to align and translate. 

ICLR 2015 .Banerjee, S. and A. Lavie. 2005. METEOR: An automatic metric for MT evaluation with improved correlation with human judgments. Proceedings of ACL Workshop on In-trinsic and Extrinsic Evaluation Measures for MT and/or Summarization .Ba˜ n´ on, M., P. Chen, B. Haddow, K. Heafield, H. Hoang, M. Espl` a-Gomis, M. L. Forcada, A. Kamran, F. Kirefu, P. Koehn, S. Ortiz Rojas, L. Pla Sempere, G. Ram´ ırez-S´ anchez, E. Sarr´ ıas, M. Strelec, B. Thompson, W. Waites, D. Wiggins, and J. Zaragoza. 2020. ParaCrawl: Web-scale acquisition of parallel corpora. ACL .Bar-Hillel, Y. 1960. The present status of automatic transla-tion of languages. In F. Alt, editor, Advances in Comput-ers 1 , pages 91–163. Academic Press. Berger, A., S. A. Della Pietra, and V. J. Della Pietra. 1996. A maximum entropy approach to natural language process-ing. Computational Linguistics , 22(1):39–71. Bickel, B. 2003. Referential density in discourse and syntac-tic typology. Language , 79(2):708–736. Brown, P. F., J. Cocke, S. A. Della Pietra, V. J. Della Pietra, F. Jelinek, J. D. Lafferty, R. L. Mercer, and P. S. Roossin. 1990. A statistical approach to machine translation. Com-putational Linguistics , 16(2):79–85. Brown, P. F., S. A. Della Pietra, V. J. Della Pietra, and R. L. Mercer. 1993. The mathematics of statistical machine translation: Parameter estimation. Computational Lin-guistics , 19(2):263–311. Callison-Burch, C., M. Osborne, and P. Koehn. 2006. Re-evaluating the role of BLEU in machine translation re-search. EACL .Chandioux, J. 1976. M ´ ET ´EO : un syst` eme op´ erationnel pour la traduction automatique des bulletins m´ et´ eorologiques destin´ es au grand public. Meta , 21:127–133. Chiang, D. 2005. A hierarchical phrase-based model for sta-tistical machine translation. ACL .Cho, K., B. van Merri¨ enboer, C. Gulcehre, D. Bahdanau, F. Bougares, H. Schwenk, and Y. Bengio. 2014. Learn-ing phrase representations using RNN encoder–decoder for statistical machine translation. EMNLP .Chou, W., C.-H. Lee, and B. H. Juang. 1993. Minimum error rate training based on n-best string models. ICASSP .Comrie, B. 1989. Language Universals and Linguistic Ty-pology , 2nd edition. Blackwell. Croft, W. 1990. Typology and Universals . Cambridge Uni-versity Press. Deng, Y. and W. Byrne. 2005. HMM word and phrase align-ment for statistical machine translation. HLT-EMNLP .Doddington, G. 2002. Automatic evaluation of machine translation quality using n-gram co-occurrence statistics. 

HLT .Dostert, L. 1955. The Georgetown-I.B.M. experiment. In 

Machine Translation of Languages: Fourteen Essays ,pages 124–135. MIT Press. Dryer, M. S. and M. Haspelmath, editors. 2013. The World Atlas of Language Structures Online . Max Planck Insti-tute for Evolutionary Anthropology, Leipzig. Available online at http://wals.info .Edunov, S., M. Ott, M. Auli, and D. Grangier. 2018. Under-standing back-translation at scale. EMNLP .

∀, W. Nekoto, V. Marivate, T. Matsila, T. Fasubaa, T. Kolawole, T. Fagbohungbe, S. O. Akinola, S. H. Muhammad, S. Kabongo, S. Osei, S. Freshia, R. A. Niyongabo, R. M. P. Ogayo, O. Ahia, M. Meressa, M. Adeyemi, M. Mokgesi-Selinga, L. Okegbemi, L. J. Martinus, K. Tajudeen, K. Degila, K. Ogueji, K. Siminyu, J. Kreutzer, J. Webster, J. T. Ali, J. A. I. Orife, I. Ezeani, I. A. Dangana, H. Kamper, H. Elsahar, G. Duru, G. Kioko, E. Murhabazi, E. van Biljon, D. Whitenack, C. Onyefuluchi, C. Emezue, B. Dossou, B. Sibanda, B. I. Bassey, A. Olabiyi, A. Ramkilowan, A. ¨ Oktem, A. Ak-infaderin, and A. Bashir. 2020. Participatory research for low-resourced machine translation: A case study in African languages. Findings of EMNLP .Gale, W. A. and K. W. Church. 1991. A program for aligning sentences in bilingual corpora. ACL .Gale, W. A. and K. W. Church. 1993. A program for aligning sentences in bilingual corpora. Computational Linguis-tics , 19:75–102. Graves, A. 2013. Generating sequences with recurrent neural networks. ArXiv. Hutchins, W. J. 1986. Machine Translation: Past, Present, Future . Ellis Horwood, Chichester, England. Hutchins, W. J. 1997. From first conception to first demon-stration: The nascent years of machine translation, 1947– 1954. A chronology. Machine Translation , 12:192–252. Hutchins, W. J. and H. L. Somers. 1992. An Introduction to Machine Translation . Academic Press. Jaeger, T. F. and R. P. Levy. 2007. Speakers optimize infor-mation density through syntactic reduction. NeurIPS .Kalchbrenner, N. and P. Blunsom. 2013. Recurrent continu-ous translation models. EMNLP .Kay, M. and M. R¨ oscheisen. 1988. Text-translation align-ment. Technical Report P90-00143, Xerox Palo Alto Re-search Center, Palo Alto, CA. Kay, M. and M. R¨ oscheisen. 1993. Text-translation align-ment. Computational Linguistics , 19:121–142. Kocmi, T., C. Federmann, R. Grundkiewicz, M. Junczys-Dowmunt, H. Matsushita, and A. Menezes. 2021. To ship or not to ship: An extensive evaluation of automatic met-rics for machine translation. ArXiv. Koehn, P. 2005. Europarl: A parallel corpus for statistical machine translation. MT summit, vol. 5 .Koehn, P., H. Hoang, A. Birch, C. Callison-Burch, M. Fed-erico, N. Bertoldi, B. Cowan, W. Shen, C. Moran, R. Zens, C. Dyer, O. Bojar, A. Constantin, and E. Herbst. 2006. Moses: Open source toolkit for statistical machine translation. ACL .Koehn, P., F. J. Och, and D. Marcu. 2003. Statistical phrase-based translation. HLT-NAACL .Exercises 31 

Lison, P. and J. Tiedemann. 2016. Opensubtitles2016: Ex-tracting large parallel corpora from movie and tv subti-tles. LREC .Marcu, D. and W. Wong. 2002. A phrase-based, joint proba-bility model for statistical machine translation. EMNLP .Marie, B., A. Fujita, and R. Rubino. 2021. Scientific credi-bility of machine translation research: A meta-evaluation of 769 papers. ACL 2021 .McLuhan, M. 1964. Understanding Media: The Extensions of Man . New American Library. Meister, C., T. Vieira, and R. Cotterell. 2020. If beam search is the answer, what was the question? EMNLP .Miller, G. A. and J. G. Beebe-Center. 1956. Some psycho-logical methods for evaluating the quality of translations. 

Mechanical Translation , 3:73–80. Nirenburg, S., H. L. Somers, and Y. Wilks, editors. 2002. 

Readings in Machine Translation . MIT Press. Och, F. J. 1998. Ein beispielsbasierter und statis-tischer Ansatz zum maschinellen Lernen von nat¨ urlichsprachlicher ¨Ubersetzung . Ph.D. thesis, Uni-versit¨ at Erlangen-N¨ urnberg, Germany. Diplomarbeit (diploma thesis). Och, F. J. 2003. Minimum error rate training in statistical machine translation. ACL .Och, F. J. and H. Ney. 2002. Discriminative training and maximum entropy models for statistical machine transla-tion. ACL .Och, F. J. and H. Ney. 2003. A systematic comparison of various statistical alignment models. Computational Lin-guistics , 29(1):19–51. Och, F. J. and H. Ney. 2004. The alignment template ap-proach to statistical machine translation. Computational Linguistics , 30(4):417–449. Papineni, K., S. Roukos, T. Ward, and W.-J. Zhu. 2002. Bleu: A method for automatic evaluation of machine transla-tion. ACL .Pierce, J. R., J. B. Carroll, E. P. Hamp, D. G. Hays, C. F. Hockett, A. G. Oettinger, and A. J. Perlis. 1966. Lan-guage and Machines: Computers in Translation and Lin-guistics . ALPAC report. National Academy of Sciences, National Research Council, Washington, DC. Popovi´ c, M. 2015. chrF: character n-gram F-score for auto-matic MT evaluation. Proceedings of the Tenth Workshop on Statistical Machine Translation .Prates, M. O. R., P. H. Avelar, and L. C. Lamb. 2019. Assess-ing gender bias in machine translation: a case study with Google Translate. Neural Computing and Applications ,32:6363–6381. Rei, R., C. Stewart, A. C. Farinha, and A. Lavie. 2020. COMET: A neural framework for MT evaluation. 

EMNLP .Schiebinger, L. 2014. Scientific research must take gender into account. Nature , 507(7490):9. Schwenk, H. 2018. Filtering and mining parallel data in a joint multilingual space. ACL .Schwenk, H., D. Dechelotte, and J.-L. Gauvain. 2006. Con-tinuous space language models for statistical machine translation. COLING/ACL .Sellam, T., D. Das, and A. Parikh. 2020. BLEURT: Learning robust metrics for text generation. ACL .Slobin, D. I. 1996. Two ways to travel. In M. Shibatani and S. A. Thompson, editors, Grammatical Construc-tions: Their Form and Meaning , pages 195–220. Claren-don Press. Snover, M., B. Dorr, R. Schwartz, L. Micciulla, and J. Makhoul. 2006. A study of translation edit rate with targeted human annotation. AMTA-2006 .Stanovsky, G., N. A. Smith, and L. Zettlemoyer. 2019. Eval-uating gender bias in machine translation. ACL .Sutskever, I., O. Vinyals, and Q. V. Le. 2014. Sequence to sequence learning with neural networks. NeurIPS .Talmy, L. 1985. Lexicalization patterns: Semantic structure in lexical forms. In T. Shopen, editor, Language Typology and Syntactic Description, Volume 3 . Cambridge Univer-sity Press. Originally appeared as UC Berkeley Cognitive Science Program Report No. 30, 1980. Talmy, L. 1991. Path to realization: A typology of event conflation. BLS-91 .Thompson, B. and P. Koehn. 2019. Vecalign: Improved sen-tence alignment in linear time and space. EMNLP .Turian, J. P., L. Shen, and I. D. Melamed. 2003. Evaluation of machine translation and its evaluation. Proceedings of MT Summit IX .Vaswani, A., N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin. 2017. Atten-tion is all you need. NeurIPS .Vauquois, B. 1968. A survey of formal grammars and al-gorithms for recognition and transformation in machine translation. IFIP Congress 1968 .Weaver, W. 1949/1955. Translation. In W. N. Locke and A. D. Boothe, editors, Machine Translation of Lan-guages , pages 15–23. MIT Press. Reprinted from a mem-orandum written by Weaver in 1949. Wu, D. 1996. A polynomial-time algorithm for statistical machine translation. ACL .Wu, Y., M. Schuster, Z. Chen, Q. V. Le, M. Norouzi, W. Macherey, M. Krikun, Y. Cao, Q. Gao, K. Macherey, J. Klingner, A. Shah, M. Johnson, X. Liu, Ł. Kaiser, S. Gouws, Y. Kato, T. Kudo, H. Kazawa, K. Stevens, G. Kurian, N. Patil, W. Wang, C. Young, J. Smith, J. Riesa, A. Rudnick, O. Vinyals, G. S. Corrado, M. Hughes, and J. Dean. 2016. Google’s neural machine translation system: Bridging the gap between human and machine translation. ArXiv preprint arXiv:1609.08144. Zens, R. and H. Ney. 2007. Efficient phrase-table represen-tation for machine translation with applications to online MT and speech translation. NAACL-HLT .Zhang, T., V. Kishore, F. Wu, K. Q. Weinberger, and Y. Artzi. 2020. Bertscore: Evaluating text generation with BERT. 

ICLR 2020 .Ziemski, M., M. Junczys-Dowmunt, and B. Pouliquen. 2016. The United Nations parallel corpus v1.0. LREC .