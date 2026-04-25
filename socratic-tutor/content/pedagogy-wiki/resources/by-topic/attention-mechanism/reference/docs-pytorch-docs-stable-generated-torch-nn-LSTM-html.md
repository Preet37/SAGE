# Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.LSTM.html
# Title: LSTM — PyTorch documentation (stable)
# Fetched via: trafilatura
# Date: 2026-04-11

LSTM[#](#lstm)
-
class torch.nn.LSTM(input_size, hidden_size, num_layers=1, bias=True, batch_first=False, dropout=0.0, bidirectional=False, proj_size=0, device=None, dtype=None)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/nn/modules/rnn.py#L833)[#](#torch.nn.LSTM) Apply a multi-layer long short-term memory (LSTM) RNN to an input sequence. For each element in the input sequence, each layer computes the following function:
where is the hidden state at time t, is the cell state at time t, is the input at time t, is the hidden state of the layer at time t-1 or the initial hidden state at time 0, and , , , are the input, forget, cell, and output gates, respectively. is the sigmoid function, and is the Hadamard product.
In a multilayer LSTM, the input of the -th layer () is the hidden state of the previous layer multiplied by dropout where each is a Bernoulli random variable which is with probability
dropout
.If
proj_size > 0
is specified, LSTM with projections will be used. This changes the LSTM cell in the following way. First, the dimension of will be changed fromhidden_size
toproj_size
(dimensions of will be changed accordingly). Second, the output hidden state of each layer will be multiplied by a learnable projection matrix: . Note that as a consequence of this, the output of LSTM network will be of different shape as well. See Inputs/Outputs sections below for exact dimensions of all variables. You can find more details in[https://arxiv.org/abs/1402.1128](https://arxiv.org/abs/1402.1128).- Parameters:
input_size – The number of expected features in the input x
hidden_size – The number of features in the hidden state h
num_layers – Number of recurrent layers. E.g., setting
num_layers=2
would mean stacking two LSTMs together to form a stacked LSTM, with the second LSTM taking in outputs of the first LSTM and computing the final results. Default: 1bias – If
False
, then the layer does not use bias weights b_ih and b_hh. Default:True
batch_first – If
True
, then the input and output tensors are provided as (batch, seq, feature) instead of (seq, batch, feature). Note that this does not apply to hidden or cell states. See the Inputs/Outputs sections below for details. Default:False
dropout – If non-zero, introduces a Dropout layer on the outputs of each LSTM layer except the last layer, with dropout probability equal to
dropout
. Default: 0bidirectional – If
True
, becomes a bidirectional LSTM. Default:False
proj_size – If
> 0
, will use LSTM with projections of corresponding size. Default: 0
- Inputs: input, (h_0, c_0)
input: tensor of shape for unbatched input, when
batch_first=False
or whenbatch_first=True
containing the features of the input sequence. The input can also be a packed variable length sequence. Seeortorch.nn.utils.rnn.pack_padded_sequence()
for details.torch.nn.utils.rnn.pack_sequence()
h_0: tensor of shape for unbatched input or containing the initial hidden state for each element in the input sequence. Defaults to zeros if (h_0, c_0) is not provided.
c_0: tensor of shape for unbatched input or containing the initial cell state for each element in the input sequence. Defaults to zeros if (h_0, c_0) is not provided.
where:
- Outputs: output, (h_n, c_n)
output: tensor of shape for unbatched input, when
batch_first=False
or whenbatch_first=True
containing the output features (h_t) from the last layer of the LSTM, for each t. If ahas been given as the input, the output will also be a packed sequence. Whentorch.nn.utils.rnn.PackedSequence
bidirectional=True
, output will contain a concatenation of the forward and reverse hidden states at each time step in the sequence.h_n: tensor of shape for unbatched input or containing the final hidden state for each element in the sequence. When
bidirectional=True
, h_n will contain a concatenation of the final forward and reverse hidden states, respectively.c_n: tensor of shape for unbatched input or containing the final cell state for each element in the sequence. When
bidirectional=True
, c_n will contain a concatenation of the final forward and reverse cell states, respectively.
- Variables:
weight_ih_l[k] – the learnable input-hidden weights of the layer (W_ii|W_if|W_ig|W_io), of shape (4*hidden_size, input_size) for k = 0. Otherwise, the shape is (4*hidden_size, num_directions * hidden_size). If
proj_size > 0
was specified, the shape will be (4*hidden_size, num_directions * proj_size) for k > 0weight_hh_l[k] – the learnable hidden-hidden weights of the layer (W_hi|W_hf|W_hg|W_ho), of shape (4*hidden_size, hidden_size). If
proj_size > 0
was specified, the shape will be (4*hidden_size, proj_size).bias_ih_l[k] – the learnable input-hidden bias of the layer (b_ii|b_if|b_ig|b_io), of shape (4*hidden_size)
bias_hh_l[k] – the learnable hidden-hidden bias of the layer (b_hi|b_hf|b_hg|b_ho), of shape (4*hidden_size)
weight_hr_l[k] – the learnable projection weights of the layer of shape (proj_size, hidden_size). Only present when
proj_size > 0
was specified.weight_ih_l[k]_reverse – Analogous to weight_ih_l[k] for the reverse direction. Only present when
bidirectional=True
.weight_hh_l[k]_reverse – Analogous to weight_hh_l[k] for the reverse direction. Only present when
bidirectional=True
.bias_ih_l[k]_reverse – Analogous to bias_ih_l[k] for the reverse direction. Only present when
bidirectional=True
.bias_hh_l[k]_reverse – Analogous to bias_hh_l[k] for the reverse direction. Only present when
bidirectional=True
.weight_hr_l[k]_reverse – Analogous to weight_hr_l[k] for the reverse direction. Only present when
bidirectional=True
andproj_size > 0
was specified.
Note
All the weights and biases are initialized from where
Note
For bidirectional LSTMs, forward and backward are directions 0 and 1 respectively. Example of splitting the output layers when
batch_first=False
:output.view(seq_len, batch, num_directions, hidden_size)
.Note
For bidirectional LSTMs, h_n is not equivalent to the last element of output; the former contains the final forward and reverse hidden states, while the latter contains the final forward hidden state and the initial reverse hidden state.
Note
batch_first
argument is ignored for unbatched inputs.Note
proj_size
should be smaller thanhidden_size
.Warning
There are known non-determinism issues for RNN functions on some versions of cuDNN and CUDA. You can enforce deterministic behavior by setting the following environment variables:
On CUDA 10.1, set environment variable
CUDA_LAUNCH_BLOCKING=1
. This may affect performance.On CUDA 10.2 or later, set environment variable (note the leading colon symbol)
CUBLAS_WORKSPACE_CONFIG=:16:8
orCUBLAS_WORKSPACE_CONFIG=:4096:2
.See the
[cuDNN 8 Release Notes](https://docs.nvidia.com/deeplearning/cudnn/archives/cudnn-880/release-notes/rel_8.html)for more information.Note
If the following conditions are satisfied: 1) cudnn is enabled, 2) input data is on the GPU 3) input data has dtype
torch.float16
4) V100 GPU is used, 5) input data is not inPackedSequence
format persistent algorithm can be selected to improve performance.Examples:
>>> rnn = nn.LSTM(10, 20, 2) >>> input = torch.randn(5, 3, 10) >>> h0 = torch.randn(2, 3, 20) >>> c0 = torch.randn(2, 3, 20) >>> output, (hn, cn) = rnn(input, (h0, c0))