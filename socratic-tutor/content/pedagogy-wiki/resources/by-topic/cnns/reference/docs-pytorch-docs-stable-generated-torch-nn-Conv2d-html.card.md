# Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
# Title: Conv2d — PyTorch 2.11 documentation
# Fetched via: trafilatura
# Date: 2026-04-09

Conv2d[#](#conv2d)
-
class torch.nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0, dilation=1, groups=1, bias=True, padding_mode='zeros', device=None, dtype=None)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/nn/modules/conv.py#L378)[#](#torch.nn.Conv2d) Applies a 2D convolution over an input signal composed of several input planes.
In the simplest case, the output value of the layer with input size and output can be precisely described as:
where is the valid 2D
[cross-correlation](https://en.wikipedia.org/wiki/Cross-correlation)operator, is a batch size, denotes a number of channels, is a height of input planes in pixels, and is width in pixels.This module supports
[TensorFloat32](../notes/cuda.html#tf32-on-ampere).On certain ROCm devices, when using float16 inputs this module will use
[different precision](../notes/numerical_accuracy.html#fp16-on-mi200)for backward.stride
controls the stride for the cross-correlation, a single number or a tuple.padding
controls the amount of padding applied to the input. It can be either a string {‘valid’, ‘same’} or an int / a tuple of ints giving the amount of implicit padding applied on both sides.dilation
controls the spacing between the kernel points; also known as the à trous algorithm. It is harder to describe, but this[link](https://github.com/vdumoulin/conv_arithmetic/blob/master/README.md)has a nice visualization of whatdilation
does.groups
controls the connections between inputs and outputs.in_channels
andout_channels
must both be divisible bygroups
. For example,At groups=1, all inputs are convolved to all outputs.
At groups=2, the operation becomes equivalent to having two conv layers side by side, each seeing half the input channels and producing half the output channels, and both subsequently concatenated.
At groups=
in_channels
, each input channel is convolved with its own set of filters (of size ).
The parameters
kernel_size
,stride
,padding
,dilation
can either be:a single
int
– in which case the same value is used for the height and width dimensiona
tuple
of two ints – in which case, the first int is used for the height dimension, and the second int for the width dimension
Note
When groups == in_channels and out_channels == K * in_channels, where K is a positive integer, this operation is also known as a “depthwise convolution”.
In other words, for an input of size , a depthwise convolution with a depthwise multiplier K can be performed with the arguments .
Note
In some circumstances when given tensors on a CUDA device and using CuDNN, this operator may select a nondeterministic algorithm to increase performance. If this is undesirable, you can try to make the operation deterministic (potentially at a performance cost) by setting
torch.backends.cudnn.deterministic = True
. See[Reproducibility](../notes/randomness.html)for more information.Note
padding='valid'
is the same as no padding.padding='same'
pads the input so the output has the shape as the input. However, this mode doesn’t support any stride values other than 1.Note
This module supports complex data types i.e.
complex32, complex64, complex128
.- Parameters:
in_channels (
[int](https://docs.python.org/3/library/functions.html#int)) – Number of channels in the input imageout_channels (
[int](https://docs.python.org/3/library/functions.html#int)) – Number of channels produced by the convolutionstride (
[int](https://docs.python.org/3/library/functions.html#int)or[tuple](https://docs.python.org/3/library/stdtypes.html#tuple), optional) – Stride of the convolution. Default: 1padding (
[int](https://docs.python.org/3/library/functions.html#int),[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)or[str](https://docs.python.org/3/library/stdtypes.html#str), optional) – Padding added to all four sides of the input. Default: 0dilation (
[int](https://docs.python.org/3/library/functions.html#int)or[tuple](https://docs.python.org/3/library/stdtypes.html#tuple), optional) – Spacing between kernel elements. Default: 1groups (
[int](https://docs.python.org/3/library/functions.html#int), optional) – Number of blocked connections from input channels to output channels. Default: 1bias (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – IfTrue
, adds a learnable bias to the output. Default:True
padding_mode (
[str](https://docs.python.org/3/library/stdtypes.html#str), optional) –'zeros'
,'reflect'
,'replicate'
or'circular'
. Default:'zeros'
- Shape:
Input: or
Output: or , where
- Variables:
Examples
>>> # With square kernels and equal stride >>> m = nn.Conv2d(16, 33, 3, stride=2) >>> # non-square kernels and unequal stride and with padding >>> m = nn.Conv2d(16, 33, (3, 5), stride=(2, 1), padding=(4, 2)) >>> # non-square kernels and unequal stride and with padding and dilation >>> m = nn.Conv2d(16, 33, (3, 5), stride=(2, 1), padding=(4, 2), dilation=(3, 1)) >>> input = torch.randn(20, 16, 50, 100) >>> output = m(input)