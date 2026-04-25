# Source: https://www.arxiv.org/pdf/1512.08756v1.pdf
# Author: Colin Raffel and Daniel P. W. Ellis
# Title: Feed-Forward Networks with Attention Can Solve Some Long-Term Memory Problems (2015)
# Fetched via: jina
# Date: 2026-04-11

Title: 1512.08756v1.pdf



Number of Pages: 6

# Feed-Forward Networks with Attention Can Solve Some Long-Term Memory Problems 

Colin Raffel 

LabROSA, Columbia University 

craffel@gmail.com 

Daniel P. W. Ellis 

LabROSA, Columbia University 

dpwe@ee.columbia.edu 

## Abstract 

Recurrent neural networks (RNNs) have proven to be powerful models in prob-lems involving sequential data. Recently, RNNs have been augmented with “atten-tion” mechanisms which allow the network to focus on different parts of an input sequence when computing their output. We propose a simplified model of atten-tion which is applicable to feed-forward neural networks and demonstrate that it can solve some long-term memory problems (specifically, those where temporal order doesn’t matter). In fact, we show empirically that our model can solve these problems for sequence lengths which are both longer and more widely varying than the best results attained with RNNs. 

## 1 Models for Sequential Data 

Many problems in machine learning are best formulated using sequential data (i.e. data where a given observation may be dependent on previous observations), such as sequence transduction (producing a new sequence given an input sequence), sequence classification (producing a single label from an entire sequence), or sequence embedding (producing a single vector from an entire sequence). Appropriate models for these tasks must be able to capture temporal dependencies in sequences, potentially of arbitrary length. 

1.1 Recurrent Neural Networks 

One such class of models are recurrent neural networks (RNNs), which can be considered a learnable function f whose output ht = f (xt, h t−1) at time t depends on input xt and the model’s previous state ht−1. In the supervised setting, the parameters of f are optimized with respect to a loss function which measures f ’s performance. A common approach is to use backpropagation through time [1], which “unrolls” the RNN over time steps to compute the gradient of the parameters of f with respect to the loss. Because the same function f is applied repeatedly over time, this gradient can easily explode or vanish [2, 3, 4]. The use of gating architectures [3, 5], sophisticated optimization techniques [6, 7], gradient clipping [2, 8], and/or careful initialization [7, 9, 10, 11] can help mitigate this issue and has facilitated the success of RNNs in a variety of fields (see e.g. [12] for an overview). However, these approaches don’t solve the problem of vanishing and exploding gradients, and as a result RNNs are in practice typically only applied in tasks where sequential dependencies span at most hundreds of time steps [6, 7, 11, 3, 13, 14]. Very long sequences can also make training computationally inefficient due to the fact that RNNs must be evaluated sequentially and cannot be fully parallelized. 

1.2 Attention 

A recently proposed method for easier modeling of long-term dependencies is “attention”. Attention mechanisms allow for a more direct dependence between the state of the model at different points 1

> arXiv:1512.08756v1 [cs.LG] 29 Dec 2015

in time. Following the definition from [15], given a model which produces a hidden state ht at each time step, attention-based models compute a “context” vector ct as the weighted mean of the state sequence h by 

ct =

> T

∑

> j=1

αtj hj

where T is the total number of time steps in the input sequence and αtj is a weight computed at each time step t for each state hj . These context vectors are then used to compute a new state sequence 

s, where st depends on st−1, ct and, for sequence transduction, the model’s output at t − 1. The weightings αij are then computed by 

etj = a(st−1, h j )

αtj = exp( etj )

∑Tk=1 exp( etk )

where a is a learned function which can be thought of as computing a scalar importance value for hj given the value of hj and the previous state st−1. This formulation allows the new state sequence s to have more direct access to the entire state sequence h. Attention-based RNNs have proven effective in a variety of sequence transduction tasks, including machine translation [15], image captioning [16], and speech recognition [17, 18]. Attention can be seen as analogous to the “soft addressing” mechanisms of the recently proposed Neural Turing Machine [19] and End-To-End Memory Network [20] models. 

1.3 Feed-Forward Attention 

A straightforward simplification to the attention mechanism described above which would allow it to be applied to sequence embedding tasks could be formulated as follows: Instead of a sequence of context vectors, we produce a single context vector c as 

et = a(ht)

αt = exp( et)

∑Tk=1 exp( ek)

c =

> T

∑

> t=1

αtht

(1) As before, a is a learnable function, but it now only depends on ht. In this formulation, attention can be seen as producing a fixed-length embedding c of the input sequence by computing an adaptive weighted average of the state sequence h. A schematic of this form of attention is shown in Figure 1. A consequence of using an attention mechanism is the ability to integrate information over time. It follows that by using this simplified form of attention, a model could perform sequence embedding even if the calculation of ht was feed-forward, i.e. ht = f (xt). Using a feed-forward f could also result in large efficiency gains as the computation could be completely parallelized. While using a feed-forward model for sequential modeling sacrifices the ability to solve some problems, we show that for certain tasks, feed-forward networks with attention can be more effective than RNNs. We note here that feed-forward models without attention can be used for sequence embedding when the sequence length T is fixed, but when T varies across sequences, some form of temporal integra-tion is necessary. An obvious straightforward choice, which can be seen as an extreme oversimpli-fication of attention, would be to compute c as the unweighted average of the state sequence ht, i.e. 

c = 1

T

> T

∑

> t=1

ht (2) This form of integration is similar to the “global temporal pooling” described in [22], which is based on the “global average pooling” technique of [23]. We will also explore the effectiveness of this approach for sequence embedding. 2α1

# h1

# α2

# h2

# α3

# h3

# αT

# hT

# a(ht )

# cFigure 1: Schematic of our proposed “feed-forward” attention mechanism (cf. [21] Figure 1). Vec-tors in the hidden state sequence ht are fed into the learnable function a(ht) to produce a probability vector α. The vector c is computed as a weighted average of ht, with weighting given by α.

## 2 Toy Long-Term Memory Problems 

A common way to measure the long-term memory capabilities of a given model is to test it on the synthetic problems originally proposed in [3]. In this paper, we will focus on the “addition” and “multiplication” problems, which can be summarized as follows: The input is a two dimensional sequence, where one dimension is a random sequence sampled uniformly from [0 , 1] and the other dimension is a “mask” sequence. At two time steps, one in the first ten sequence steps and one before the sequence’s midpoint, the “mask” signal is 1; at the first and last time step it is -1; and at all other time steps it is 0. The goal is to perform addition or multiplication on the two values in the noise dimension which co-occur with the 1s in the mask dimension, which is meant to require that a model be able to store the correct values for the duration of the sequence. A sequence is considered correctly processed if the absolute difference between the predicted and target values is less than 

.04 . Slight variants of these tasks have also been used [7, 11, 9, 6], but we will follow the original definition from [3]. These two tasks are only a subset of the synthetic long-term memory problems which have been proposed; we focus on them here because they are the most commonly used and discuss the applicability of feed-forward attention on the remaining problems in Section 3. 

2.1 Model Details 

For all experiments, we used the following model: First, the state ht was computed from the input at each time step xt by 

ht = max( Wxh xt + bxh , 0.01) 

where Wxh ∈ RD×2, b xh ∈ RD . We tested models where the context vector c was then computed either as in Equation 1, with 

a(ht) = tanh( Whc ht + bhc )

where Whc ∈ R1×D , b hc ∈ R, or simply as the unweighted mean of h as in Equation 2. We then computed an intermediate vector 

s = max( Wcs c + bcs , 0.01) 

where Wcs ∈ RD×D , b ∈ RD from which the output was computed as 

y = max( Wsy s + bsy , 0.01) 

3Addition 

Sequence length ( T0) 50 100 500 1000 5000 10000 Attention 1 1 1 1 2 3Unweighted 1 1 1 2 8 17 

Multiplication 

Sequence length ( T0) 50 100 500 1000 5000 10000 Attention 1 2 4 2 15 6Unweighted 2 2 8 33 89.8% 80.8% Table 1: Number of epochs required to achieve perfect accuracy, or accuracy after 100 epochs (greyed-out values), for the experiment described in Section 2.2. where Wsy ∈ R1×D , bsy ∈ R. The “leaky rectifier” nonlinearity LReLU (x) = max( x, . 01) was proposed in [24]; we found that it improved early convergence so we used it in all of our models. For all experiments, we set D = 100 .We used the squared error of the output y against the target value for each sequence as an objective. Parameters were optimized using “adam”, a recently proposed stochastic optimization technique [25], with the optimization hyperparameters β1 and β2 set to the values suggested in [25] (.9 and .999 respectively). All weight matrices were initialized with entries drawn from a Gaussian distribution with a mean of zero and, for a matrix W ∈ RM ×N , a standard deviation of 1/√N . All bias vectors were initialized with zeros. We trained on mini-batches of 100 sequences and computed the accuracy on a held-out test set of 1000 sequences every epoch, defined as 1000 parameter updates. We stopped training when either 100% accuracy was attained on the test set, or after 100 epochs. All networks were implemented using Lasagne [26], which is built on top of Theano [27, 28]. 

2.2 Fixed-Length Experiment 

Traditionally, the sequence lengths tested in each task vary uniformly between [T0, 1.1T0] for dif-ferent values of T0. As T0 increases, the model must be able to handle longer-term dependencies. The largest value of T0 for which high accuracy was attained on a held-out test set varies across models, tasks, and papers. In the original paper describing the long short-term memory (LSTM) architecture [3], a small LSTM network was shown to be able to solve the addition problem up to T0 = 1000 and the multiplication problem up to T0 = 100 . [6] later showed that a “vanilla” (single-layer, densely-connected) recurrent network could solve both the addition and multiplica-tion problems for T0 = 200 when Hessian-Free optimization was used. The same model was used in [7], where Nesterov’s Accelerated Gradient was used instead for optimization which allowed the model to solve the addition and multiplication problems for T0 = 80 . By initializing a similarly structured recurrent network’s hidden-to-hidden weights to an identity matrix and using a rectifier activation function, [11] solved the addition problem up to T0 = 300 , which they claimed outper-formed an LSTM model. More recently, [13] utilized a regularizer which encourages subsequent hidden states to have similar norms, allowing a vanilla recurrent network to achieve some success on the addition problem for T0 = 400 . Related work in [14] showed that enforcing an orthogonality constraint on the hidden-to-hidden weight matrix of a vanilla RNN allowed it to nearly solve the addition problem for T0 = 400 and achieve some success for T0 = 750 . Finally, in [9] the addition and multiplication tasks were solved for T0 = 10000 and T0 = 1000 respectively by using a recur-rent network with a very large and carefully initialized hidden-to-hidden weight matrix which was not optimized, which sidesteps the issue of vanishing and exploding gradients. We therefore tested our proposed feed-forward attention models for T0 ∈{50 , 100 , 500 , 1000 , 5000 , 10000 }. The required number of epochs or accuracy after 100 epochs for each task, sequence length, and temporal integration method (adaptively weighted attention or unweighted mean) is shown in Table 1. For fair comparison, we report the best result achieved using any learning rate in {.0003 , . 001 , . 003 , . 01 }. From these results, it’s clear that the feed-forward attention model can quickly solve these long-term memory problems for longer sequence lengths than have been demonstrated with RNNs. Our model is also efficient: Processing one epoch of 100,000 sequences with T0 = 10000 took 254 seconds using an NVIDIA GTX 980 Ti 4GPU, while processing the same data with a single-layer vanilla RNN with a hidden dimensionality of 100 (resulting in a comparable number of parameters) took 917 seconds on the same hardware. In addition, there is a clear benefit to using the attention mechanism of Equation 1 instead of a simple unweighted average over time, which only incurs a marginal increase in the number of parameters (10,602 vs. 10,501, or less than 1%). 

2.3 Variable-length Experiment 

Because the range of sequence lengths [T0, 1.1T0] is small compared to the range of T0 values we evaluated, we further tested whether it was possible to train a single model which could cope with sequences with highly varying lengths. To our knowledge, such an experiment has not been con-ducted with RNNs. We trained models of the same architecture as used in the previous experiment on minibatches of sequences whose lengths were chosen uniformly at random between 50 and 10000 time steps. Using the attention mechanism of Equation 1, on held-out test sets of 1000 sequences, our model achieved 99.9% accuracy on the addition task and 99.4% on the multiplication task af-ter training for 100 epochs. This suggests that a single feed-forward network with attention can simultaneously model both short-term and very long-term dependencies, with a marginal decrease in accuracy. Using an unweighted average over time, we were only able to achieve accuracies of 77.4% and 55.5% on the variable-length addition and multiplication tasks, respectively. 

## 3 Discussion 

A clear limitation of our proposed model is that it will fail on any task where temporal order matters because computing an average over time discards order information. For example, on the two-symbol temporal order task [3] where a sequence must be classified in terms of whether two symbols 

X and Y appear in the order X, X ; Y, Y ; X, Y ; or Y, X , our model can differentiate between the 

X, X and Y, Y cases perfectly but cannot differentiate between the X, Y and Y, X cases at all. Nevertheless, we submit that for some real-world tasks involving sequential data, temporal order is substantially less important than being able to handle very long sequences. For example, in Joachims’ seminal paper on text document categorization [29], he posits that “word stems work well as representation units and that their ordering in a document is of minor importance for many tasks”. We also have shown in parallel work that our proposed feed-forward attention model can be used effectively for pruning large-scale (sub)sequence retrieval searches, even when the sequences are very long and high-dimensional [30]. Our results here further demonstrate that our model can be substantially more efficient than recurrent models on some classic long-term memory tasks. Further investigation on more real-world problems is warranted; for interested researchers, all of the code used in this experiment is available online. 1

## References 

[1] Paul J. Werbos. Backpropagation through time: what it does and how to do it. Proceedings of the IEEE , 78(10):1550–1560, 1990. [2] Razvan Pascanu, Tomas Mikolov, and Yoshua Bengio. On the difficulty of training recurrent neural networks. arXiv:1211.5063 , 2012. [3] Sepp Hochreiter and J¨ urgen Schmidhuber. Long short-term memory. Neural computation ,9(8):1735–1780, 1997. [4] Yoshua Bengio, Patrice Simard, and Paolo Frasconi. Learning long-term dependencies with gradient descent is difficult. IEEE Transactions on Neural Networks , 5(2):157–166, 1994. [5] Kyunghyun Cho, Bart Van Merri¨ enboer, Caglar Gulcehre, et al. Learning phrase representa-tions using RNN encoder-decoder for statistical machine translation. arXiv:1406.1078 , 2014. [6] James Martens and Ilya Sutskever. Learning recurrent neural networks with hessian-free op-timization. In Proceedings of the 28th International Conference on Machine Learning , pages 1033–1040, 2011. 

> 1https://github.com/craffel/sequence-embedding/tree/master/toy_problems

5[7] Ilya Sutskever, James Martens, George Dahl, and Geoffrey Hinton. On the importance of initialization and momentum in deep learning. In Proceedings of the 30th International Con-ference on Machine Learning , pages 1139–1147, 2013. [8] Alex Graves. Generating sequences with recurrent neural networks. arXiv:1308.0850 , 2013. [9] Herbert Jaeger. Long short-term memory in echo state networks: Details of a simulation study. Technical Report 27, Jacobs University, 2012. [10] Tomas Mikolov, Armand Joulin, Sumit Chopra, et al. Learning longer memory in recurrent neural networks. arXiv:1412.7753 , 2014. [11] Quoc V. Le, Navdeep Jaitly, and Geoffrey E. Hinton. A simple way to initialize recurrent networks of rectified linear units. arXiv:1504.00941 , 2015. [12] Alex Graves. Supervised sequence labelling with recurrent neural networks . Springer, 2012. [13] David Krueger and Roland Memisevic. Regularizing RNNs by stabilizing activations. arXiv preprint arXiv:1511.08400 , 2015. [14] Martin Arjovsky, Amar Shah, and Yoshua Bengio. Unitary evolution recurrent neural net-works. arXiv preprint arXiv:1511.06464 , 2015. [15] Dzmitry Bahdanau, Kyunghyun Cho, and Yoshua Bengio. Neural machine translation by jointly learning to align and translate. arXiv:1409.0473 , 2014. [16] Kelvin Xu, Jimmy Ba, Ryan Kiros, et al. Show, attend and tell: Neural image caption genera-tion with visual attention. arXiv preprint arXiv:1502.03044 , 2015. [17] William Chan, Navdeep Jaitly, Quoc V. Le, and Oriol Vinyals. Listen, attend and spell. arXiv preprint arXiv:1508.01211 , 2015. [18] Dzmitry Bahdanau, Jan Chorowski, Dmitriy Serdyuk, et al. End-to-end attention-based large vocabulary speech recognition. arXiv preprint arXiv:1508.04395 , 2015. [19] Alex Graves, Greg Wayne, and Ivo Danihelka. Neural turing machines. arXiv:1410.5401 ,2014. [20] Sainbayar Sukhbaatar, Arthur Szlam, Jason Weston, and Rob Fergus. End-to-end memory networks. arXiv:1503.08895 , 2015. [21] Kyunghyun Cho. Introduction to neural machine translation with GPUs (part 3). 

http://devblogs.nvidia.com/parallelforall/introduction-neural-machine-translation-gpus-part-3/ , 2015. [22] Sander Dieleman. Recommending music on Spotify with deep learning. 

http://benanne.github.io/2014/08/05/spotify-cnns.html , 2014. [23] Min Lin, Qiang Chen, and Shuicheng Yen. Network in network. arXiv preprint arXiv:1312.4400 , 2014. [24] Andrew L. Maas, Awni Y. Hannun, and Andrew Y. Ng. Rectifier nonlinearities improve neu-ral network acoustic models. In ICML Workshop on Deep Learning for Audio, Speech, and Language Processing , 2013. [25] Diederik Kingma and Jimmy Ba. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980 , 2014. [26] Sander Dieleman, Jan Schl¨ uter, Colin Raffel, et al. Lasagne: First release. https:// github.com/Lasagne/Lasagne , 2015. [27] Fr´ ed´ eric Bastien, Pascal Lamblin, Razvan Pascanu, et al. Theano: new features and speed improvements. In Deep Learning and Unsupervised Feature Learning NIPS 2012 Workshop ,2012. [28] James Bergstra, Olivier Breuleux, Fr´ ed´ eric Bastien, et al. Theano: a CPU and GPU math expression compiler. In Proceedings of the Python for scientific computing conference (SciPy) ,2010. [29] Thorsten Joachims. Text categorization with support vector machines: Learning with many relevant features . Springer, 1998. [30] Colin Raffel and Daniel P. W. Ellis. Pruning subsequence search with attention-based embed-ding. In Proceedings of the 41st IEEE International Conference on Acoustics, Speech, and Signal Processing , 2016 (to appear). 6