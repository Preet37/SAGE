# Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.GRU.html
# Title: GRU — PyTorch 2.11 documentation
# Fetched via: trafilatura
# Date: 2026-04-11

GRU[#](#gru)
-
class torch.nn.GRU(input_size, hidden_size, num_layers=1, bias=True, batch_first=False, dropout=0.0, bidirectional=False, device=None, dtype=None)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/nn/modules/rnn.py#L1212)[#](#torch.nn.GRU) Apply a multi-layer gated recurrent unit (GRU) RNN to an input sequence. For each element in the input sequence, each layer computes the following function:
where is the hidden state at time t, is the input at time t, is the hidden state of the layer at time t-1 or the initial hidden state at time 0, and , , are the reset, update, and new gates, respectively. is the sigmoid function, and is the Hadamard product.
In a multilayer GRU, the input of the -th layer () is the hidden state of the previous layer multiplied by dropout where each is a Bernoulli random variable which is with probability
dropout
.- Parameters:
input_size – The number of expected features in the input x
hidden_size – The number of features in the hidden state h
num_layers – Number of recurrent layers. E.g., setting
num_layers=2
would mean stacking two GRUs together to form a stacked GRU, with the second GRU taking in outputs of the first GRU and computing the final results. Default: 1bias – If
False
, then the layer does not use bias weights b_ih and b_hh. Default:True
batch_first – If
True
, then the input and output tensors are provided as (batch, seq, feature) instead of (seq, batch, feature). Note that this does not apply to hidden or cell states. See the Inputs/Outputs sections below for details. Default:False
dropout – If non-zero, introduces a Dropout layer on the outputs of each GRU layer except the last layer, with dropout probability equal to
dropout
. Default: 0bidirectional – If
True
, becomes a bidirectional GRU. Default:False
- Inputs: input, h_0
input: tensor of shape for unbatched input, when
batch_first=False
or whenbatch_first=True
containing the features of the input sequence. The input can also be a packed variable length sequence. Seeortorch.nn.utils.rnn.pack_padded_sequence()
for details.torch.nn.utils.rnn.pack_sequence()
h_0: tensor of shape or containing the initial hidden state for the input sequence. Defaults to zeros if not provided.
where:
- Outputs: output, h_n
output: tensor of shape for unbatched input, when
batch_first=False
or whenbatch_first=True
containing the output features (h_t) from the last layer of the GRU, for each t. If ahas been given as the input, the output will also be a packed sequence.torch.nn.utils.rnn.PackedSequence
h_n: tensor of shape or containing the final hidden state for the input sequence.
- Variables:
weight_ih_l[k] – the learnable input-hidden weights of the layer (W_ir|W_iz|W_in), of shape (3*hidden_size, input_size) for k = 0. Otherwise, the shape is (3*hidden_size, num_directions * hidden_size)
weight_hh_l[k] – the learnable hidden-hidden weights of the layer (W_hr|W_hz|W_hn), of shape (3*hidden_size, hidden_size)
bias_ih_l[k] – the learnable input-hidden bias of the layer (b_ir|b_iz|b_in), of shape (3*hidden_size)
bias_hh_l[k] – the learnable hidden-hidden bias of the layer (b_hr|b_hz|b_hn), of shape (3*hidden_size)
Note
All the weights and biases are initialized from where
Note
For bidirectional GRUs, forward and backward are directions 0 and 1 respectively. Example of splitting the output layers when
batch_first=False
:output.view(seq_len, batch, num_directions, hidden_size)
.Note
batch_first
argument is ignored for unbatched inputs.Note
The calculation of new gate subtly differs from the original paper and other frameworks. In the original implementation, the Hadamard product between and the previous hidden state is done before the multiplication with the weight matrix W and addition of bias:
This is in contrast to PyTorch implementation, which is done after
This implementation differs on purpose for efficiency.
Note
If the following conditions are satisfied: 1) cudnn is enabled, 2) input data is on the GPU 3) input data has dtype
torch.float16
4) V100 GPU is used, 5) input data is not inPackedSequence
format persistent algorithm can be selected to improve performance.Examples:
>>> rnn = nn.GRU(10, 20, 2) >>> input = torch.randn(5, 3, 10) >>> h0 = torch.randn(2, 3, 20) >>> output, hn = rnn(input, h0)