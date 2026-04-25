# Source: https://gist.github.com/airalcorn2/50ec06517ce96ecc143503e21fa6cb91
# Title: A simple script for extracting the attention weights from a PyTorch Transformer
# Fetched via: trafilatura
# Author: Michael A. Alcorn
# Author Slug: michael-alcorn
# Date: 2026-04-07

-
-
Save airalcorn2/50ec06517ce96ecc143503e21fa6cb91 to your computer and use it in GitHub Desktop.
[Learn more about bidirectional Unicode characters](https://github.co/hiddenchars)
| # Inspired by: https://towardsdatascience.com/the-one-pytorch-trick-which-you-should-know-2d5e9c1da2ca. | |
| # Monkey patching idea suggested by @kklemon here: | |
| # https://gist.github.com/airalcorn2/50ec06517ce96ecc143503e21fa6cb91?permalink_comment_id=4407423#gistcomment-4407423. | |
| import torch | |
| from torch import nn | |
| def patch_attention(m): | |
| forward_orig = m.forward | |
| def wrap(*args, **kwargs): | |
| kwargs["need_weights"] = True | |
| kwargs["average_attn_weights"] = False | |
| return forward_orig(*args, **kwargs) | |
| m.forward = wrap | |
| class SaveOutput: | |
| def __init__(self): | |
| self.outputs = [] | |
| def __call__(self, module, module_in, module_out): | |
| self.outputs.append(module_out[1]) | |
| def clear(self): | |
| self.outputs = [] | |
| d_model = 512 | |
| nhead = 8 | |
| dim_feedforward = 2048 | |
| dropout = 0.0 | |
| num_layers = 6 | |
| encoder_layer = nn.TransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout) | |
| transformer = nn.TransformerEncoder(encoder_layer, num_layers) | |
| transformer.eval() | |
| save_output = SaveOutput() | |
| patch_attention(transformer.layers[-1].self_attn) | |
| hook_handle = transformer.layers[-1].self_attn.register_forward_hook(save_output) | |
| seq_len = 20 | |
| X = torch.rand(seq_len, 1, d_model) | |
| with torch.no_grad(): | |
| out = transformer(X) | |
| print(save_output.outputs[0][0]) |
[@PaulOppelt](https://github.com/PaulOppelt) - it looks like the implementations for the various Transformer layers have changed a lot in the nearly two years since I posted this. The easiest thing to do (which isn't particularly easy!) might be to just write custom TransformerEncoder
and TransformerEncoderLayer
classes where you set need_weights=True
in the self.self_attn
call in _sa_block
.
The attention module can be easily patched to return attention weights. This will also work flawlessly with the rest of the Transformer implementation, as it simply disregards the output anyway.
...
def patch_attention(m):
forward_orig = m.forward
def wrap(*args, **kwargs):
kwargs['need_weights'] = True
kwargs['average_attn_weights'] = False
return forward_orig(*args, **kwargs)
m.forward = wrap
for module in transformer.modules():
if isinstance(module, nn.MultiheadAttention):
utils.patch_attention(module)
module.register_forward_hook(save_output)
Thanks, [@kklemon](https://github.com/kklemon). I've incorporated your monkey patching suggestion into the gist (with credit).
If I set batch_first=True
and use X = torch.rand(1, seq_len, d_model)
, it returns []
for the attention weights, seems like patch_attention
does not work. Do you know how to solve this problem? Thanks :)
[@77komorebi](https://github.com/77komorebi) - as you can see [here](https://github.com/pytorch/pytorch/blob/d7f6bfe651e6e45eecfc04f04ea26303b9a96e13/torch/nn/modules/transformer.py#L589), using batch_first=True
leads to the TransformerEncoderLayer
layer calling torch._transformer_encoder_layer_fwd
. As a result, the MultiheadAttention
layer is never called, and so the forward hook is never activated (the code for how hooks are used in Module
s can be found [here](https://github.com/pytorch/pytorch/blob/0a0acce515cb378c9bc1e174b827a786a1d63a3d/torch/nn/modules/module.py#L1504)).
[@airalcorn2](https://github.com/airalcorn2) Thanks!
Hi all, thanks for this script it is very helpful. When I run it as is I run out of GPU memory. But when I run it like this
patch_attention(model.transformer_layer.self_attn)
save_output = SaveOutput()
hook_handle = model.transformer_layer.self_attn.register_forward_hook(save_output)
I do not. Is extracting the weights from the TransformerEncoderLayer not as useful as extracting them directly from the layers? Thanks in advance
[Sign up for free](/join?source=comment-gist)to join this conversation on GitHub. Already have an account?
[Sign in to comment](/login?return_to=https%3A%2F%2Fgist.github.com%2Fairalcorn2%2F50ec06517ce96ecc143503e21fa6cb91)
hey :) for me it returns None for the attention weights if I run your code. I suspect it is because in F.multi_head_attention_forward, need_weights is set to false in the implementation of an encoder layer. This variable is also not accessible since it is manually set to false and not provided as a function argument. Do you now why this is or if there is a way around?