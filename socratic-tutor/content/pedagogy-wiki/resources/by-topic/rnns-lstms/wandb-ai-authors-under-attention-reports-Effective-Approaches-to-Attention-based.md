# Source: https://wandb.ai/authors/under-attention/reports/Effective-Approaches-to-Attention-based-Neural-Machine-Translation--Vmlldzo1MzQwMjA
# Author: Weights & Biases
# Author Slug: wandb
# Title: Effective Approaches to Attention-based Neural Machine Translation - W&B Report
# Fetched via: browser
# Date: 2026-04-07

Skip to main content
authors
Projects
under-attention
Reports
Effective Approaches to Attention-based Neural Machine Translation
Log in
Sign up
Share
Comment
Star
Effective Approaches to Attention-based Neural Machine Translation
Part III of our mini-series on attention.
Aritra Roy Gosthipaty, Devjyoti Chakraborty
Created on March 15, 2021
|
Updated on May 20, 2021
Comment
Introduction
In our previous report, we explained the delicate intricacies of Bahdanau's Attention while simultaneously laying a foundation of the entire Neural Machine Translation architecture. As mentioned before, in this report we talk about Effective Approaches to Attention-based Neural Machine Translation by Luong et. al.
Building on the intuition created by Bahdanau, the author's of this paper have tried to add their own twist to the normal Attention architecture, suggesting subtle changes to break through the limitations of the old architecture.
We will not be diving too deep into the attention mechanism in this report. This will be a comparison report with more attention to the visualizations and the results.
﻿Paper | Code﻿
Mathematical Intuition
Luong et. al. suggested some small and necessary changes to the architecture of the decoder network which helped in the task of neural machine translation. We will first talk about the encoder, the attention layer and then the decoder. While talking about the architecture we will also compare it with that of Bahdanau's.
﻿

A basic outline of the suggested architecture of Luong﻿
Encoder
In this paper the authors opt for a unidirectional recurrent neural architecture for the encoder. They mention that with unidirectionality the model considerably speeds up and becomes less computation hungry. For the encoder we choose a forward GRU which takes the present input 
𝑥
𝑡
x
t
	​

﻿
and past hidden state 
ℎ
𝑠
−
1
h
s−1
	​

﻿
as input while processing them into the present hidden state 
ℎ
𝑡
h
t
	​

﻿
.
ℎ
𝑠
=
𝑅
𝑁
𝑁
(
𝑥
𝑡
,
ℎ
𝑡
−
1
)
h
s
	​

=RNN(x
t
	​

,h
t−1
	​

)
﻿
After passing the entire source sentence to the Encoder we have a set of all the hidden states.
ℎ
𝑡
=
{
ℎ
1
,
.
.
.
,
ℎ
𝑇
𝑥
}
h
t
	​

={h
1
	​

,...,h
T
x
	​

	​

}
﻿
Decoder
At each time step 
𝑡
t
﻿
 in the decoding phase, the main motive is to capture the present hidden state of the decoder 
𝑠
𝑡
s
t
	​

﻿
 and then to derive a context vector 
𝑐
𝑡
c
t
	​

﻿
 that captures relevant source-side information.
Specifically, given the target hidden state 
𝑠
𝑡
s
t
	​

﻿
 and the source-side context vector 
𝑐
𝑡
c
t
	​

﻿
, we employ a simple concatenation layer to combine the information from both vectors to produce an attentional hidden state as follows:


𝑠
𝑡
~
=
tanh
⁡
(
𝑊
𝑐
[
𝑐
𝑡
;
𝑠
𝑡
]
)
s
t
	​

~
	​

=tanh(W
c
	​

[c
t
	​

;s
t
	​

])
﻿
The attention vector 
ℎ
𝑡
~
h
t
	​

~
	​

﻿
 is then fed through the SoftMax layer to produce the next decoder word.
𝑝
(
𝑦
𝑡
∣
𝑦
<
𝑡
,
𝑥
)
=
𝑠
𝑜
𝑓
𝑡
𝑚
𝑎
𝑥
(
𝑊
𝑠
𝑠
𝑡
~
)
p(y
t
	​

∣y
<t
	​

,x)=softmax(W
s
	​

s
t
	​

~
	​

)
﻿
Enough of mathematical jargons, let's focus only on the part where the authors have proposed changes to the attention layer.
Bahdanau goes from:
𝑠
𝑡
−
1
→
𝑎
𝑡
→
𝑐
𝑡
→
𝑠
𝑡
s
t−1
	​

→a
t
	​

→c
t
	​

→s
t
	​

﻿
Luong goes from:
𝑠
𝑡
→
𝑎
𝑡
→
𝑐
𝑡
→
𝑠
𝑡
~
s
t
	​

→a
t
	​

→c
t
	​

→
s
t
	​

~
	​

﻿
Input-Feeding Approach
With the present proposal the authors found out that they were not feeding the attention into the recurrent units of the decoder. This meant that the decoding system did not know which parts of the source sentence were attended to at the previous step.
With that in mind, they now propose to provide the attention to the next decoder unit along with the input and the hidden states. This proved to be a game changer. While Bahdanu's model already had this mechanism installed inside of it, Luong had to explicitly do it.
The GIF provided below 👇 shows the entire encoding and decoding mechanism as envisioned by Luong et. al.
﻿
Code
We shall move on to understand the salient parts of the architecture. The encoder architecture stays mostly similar to Bahdanau's, but we use a unidirectional for our baseline model. 
class Encoder(tf.keras.Model):
  def __init__(self,
               vocab_size,
               embedding_dim,
               enc_units,
               batch_sz):
    super(Encoder, self).__init__()
    self.batch_sz = batch_sz
    self.enc_units = enc_units
    self.embedding = L.Embedding(vocab_size, embedding_dim)
    self.gru = L.GRU(self.enc_units,
                     return_sequences=True,
                     return_state=True,
                     recurrent_initializer='glorot_uniform')
﻿

  def call(self,
           x,
           hidden_fd):
    x = self.embedding(x)
    output, fd_state = self.gru(x, initial_state = [hidden_fd])
    return output, fd_state
﻿

  def initialize_hidden_state(self):
    return tf.zeros((self.batch_sz, self.enc_units))
Now, where the magic happens. For our baseline, we have chose to recreate the global attention module from Luong's paper. The module takes the decoder hidden state and annotations (Output from the encoder) as its parameters. For global attention, the computations are similar to that of Bahdanau's attention. As we know that the difference lies in the way the decoder utilizes the output from the Attention modules. 
class LuongAttention(tf.keras.layers.Layer):
  def __init__(self, units):
    super(LuongAttention, self).__init__()
    self.W1 = L.Dense(units)
    self.W2 = L.Dense(units)
    self.W3 = L.Dense(units)
    self.W4 = L.Dense(units)
    self.V = L.Dense(1)
﻿

  def call(self, dec_hidden_state, annotations):
    dec_hidden_state_time = tf.expand_dims(dec_hidden_state, 1)
﻿

    score = self.V(tf.nn.tanh(
        self.W1(dec_hidden_state_time) + self.W2(annotations)))
﻿

    # attention_weights shape == (batch_size, max_length, 1)
    attention_weights = tf.nn.softmax(score, axis=1)
    
    # context_vector shape after sum == (batch_size, hidden_size)
    context_vector = attention_weights * annotations
    context_vector = tf.reduce_sum(context_vector, axis=1)
﻿

    mod_hidden = tf.nn.tanh(
        self.W3(context_vector) + self.W4(dec_hidden_state)
    )
﻿

    return mod_hidden, attention_weights
Keeping true to the difference in architecture, we use the output from the attention layer to predict output words. But the unmodified hidden state is fed to the next GRU cell, while the modified hidden state is concatenated with the next GRU input. This way, the sequence model retains information learned from the previous cells. 
 class Decoder(tf.keras.Model):
    def __init__(self, vocab_size, embedding_dim, dec_units, batch_sz):
        super(Decoder, self).__init__()
        self.batch_sz = batch_sz
        self.dec_units = dec_units
        self.embedding = L.Embedding(vocab_size, embedding_dim)
        self.gru = L.GRU(self.dec_units,
                            recurrent_initializer='glorot_uniform')
        self.fc = L.Dense(vocab_size)
        # used for attention
        self.attention = LuongAttention(self.dec_units)
﻿

    def call(self, x, dec_hidden_state, mod_hidden, annotations):
        x = self.embedding(x)
        x = tf.concat([tf.expand_dims(mod_hidden, 1), x], axis=-1)
        output = self.gru(x) #output here is the ht
﻿

        mod_hidden, attention_weights = self.attention(output, annotations)
        pred = self.fc(mod_hidden)
        return pred, output,  mod_hidden, attention_weights
    
    def initialize_hidden_state(self):
        return tf.zeros((self.batch_sz, self.dec_units))
For easier training, we once again coalesce all these separate modules into one single entity. Take note at how the indexes have to differ from Bahdanau's training step. Important thing to remember is that Luong works on the concurrent hidden step to output a modified concurrent hidden step for output words prediction, while Bahdanau works on the concurrent hidden step to output the next hidden step itself. 
class NMT(tf.keras.Model):
    def __init__(self, encoder, decoder):
        super(NMT, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
﻿

    def train_step(self, data):
        # Every sentence is different
        # We would not want the memory state to flow from
        # one sentence to other
        enc_hidden_fd = self.encoder.initialize_hidden_state()
        mod_hidden = self.decoder.initialize_hidden_state()
        inp, targ = data
        loss = 0
        with tf.GradientTape() as tape:
            annotations, enc_hidden_fd = self.encoder(inp, enc_hidden_fd)
            dec_hidden = enc_hidden_fd
            dec_input = tf.expand_dims([targ_lang.word_index['<start>']] * BATCH_SIZE, 1)
            # Teacher forcing - feeding the target as the next input
            for t in range(1, targ.shape[1]):
                # passing enc_output to the decoder
                predictions, dec_hidden, mod_hidden, att_weights = self.decoder(dec_input, dec_hidden, mod_hidden, annotations)
                loss += self.compiled_loss(targ[:, t], predictions)
                # using teacher forcing
                dec_input = tf.expand_dims(targ[:, t], 1)
        batch_loss = (loss / int(targ.shape[1]))
        variables = encoder.trainable_variables + decoder.trainable_variables
        gradients = tape.gradient(loss, variables)
        optimizer.apply_gradients(zip(gradients, variables))
        return {"custom_loss": batch_loss}
    
    def test_step(self, data):
        enc_hidden_fd = self.encoder.initialize_hidden_state()
        mod_hidden = self.decoder.initialize_hidden_state()
        inp, targ = data
        loss = 0
        annotations, enc_hidden_fd = self.encoder(inp, enc_hidden_fd)
        dec_hidden = enc_hidden_fd
        dec_input = tf.expand_dims([targ_lang.word_index['<start>']] * BATCH_SIZE, 1)
        # Teacher forcing - feeding the target as the next input
        for t in range(1, targ.shape[1]):
            # passing enc_output to the decoder
            predictions, dec_hidden, mod_hidden, att_weights = self.decoder(dec_input, dec_hidden, mod_hidden, annotations)
            loss += self.compiled_loss(targ[:, t], predictions)
            # using teacher forcing
            dec_input = tf.expand_dims(targ[:, t], 1)
        batch_loss = (loss / int(targ.shape[1]))
        return {"custom_loss": batch_loss}
Visualization 
Loss plot
﻿
Run set
4
﻿
Custom Attention Weights
Hover over the words to check out the attention weights associated to the translations.
﻿
Run set
3
﻿
Attention Heatmaps
Please click on the heatmaps for a better view.
﻿
Run set
3
﻿
Conclusion 
To actually understand the effect through the results, notice how the heatmaps formed from Luong has a much more concentrated pattern rather than Bahdanau. The result is also noted in our added custom charts, where we see which input word had how much impact in the formation of an output word. In direct comparison, we can conclude that our baseline Luong model worked slightly better than our Baseline Bahdanau model. However, Luong didn't stop at this. He introduced the concept of Local attention, which not only decreases computation time, but also narrows down the window of words in which our architecture will find relevancy in. In our next report, we compare the different kinds of changes each architecture brings, as well show ablations by changing certain parameters. 

The authors:

Name	Twitter	GitHub
Devjyoti Chakrobarty	@Cr0wley_zz	@cr0wley-zz
Aritra Roy Gosthipaty	@ariG23498	@ariG23498
﻿
Add a comment
Made with Weights & Biases. Sign up or log in to create reports like this one.
By clicking “Accept All Cookies”, you agree to the storing of cookies on your device to enhance site navigation, analyze site usage, and assist in our marketing efforts.
Cookies Settings Reject All Accept All