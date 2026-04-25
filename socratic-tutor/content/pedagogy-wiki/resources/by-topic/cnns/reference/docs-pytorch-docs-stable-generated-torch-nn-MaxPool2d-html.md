# Source: https://docs.pytorch.org/docs/stable/generated/torch.nn.MaxPool2d.html
# Title: MaxPool2d — PyTorch documentation (stable)
# Fetched via: browser
# Date: 2026-04-09

Rate this Page
★
★
★
★
★
MaxPool2d
class torch.nn.MaxPool2d(kernel_size, stride=None, padding=0, dilation=1, return_indices=False, ceil_mode=False)
[source]

Applies a 2D max pooling over an input signal composed of several input planes.

In the simplest case, the output value of the layer with input size 
(
𝑁
,
𝐶
,
𝐻
,
𝑊
)
(N,C,H,W)
, output 
(
𝑁
,
𝐶
,
𝐻
𝑜
𝑢
𝑡
,
𝑊
𝑜
𝑢
𝑡
)
(N,C,H
out
	​

,W
out
	​

)
 and kernel_size 
(
𝑘
𝐻
,
𝑘
𝑊
)
(kH,kW)
 can be precisely described as:

𝑜
𝑢
𝑡
(
𝑁
𝑖
,
𝐶
𝑗
,
ℎ
,
𝑤
)
=
	
max
⁡
𝑚
=
0
,
…
,
𝑘
𝐻
−
1
max
⁡
𝑛
=
0
,
…
,
𝑘
𝑊
−
1


	
input
(
𝑁
𝑖
,
𝐶
𝑗
,
stride[0]
ℎ
+
𝑚
,
stride[1]
𝑤
+
𝑛
)
out(N
i
	​

,C
j
	​

,h,w)=
	​

m=0,…,kH−1
max
	​

n=0,…,kW−1
max
	​

input(N
i
	​

,C
j
	​

,stride[0]×h+m,stride[1]×w+n)
	​


If padding is non-zero, then the input is implicitly padded with negative infinity on both sides for padding number of points. dilation controls the spacing between the kernel points. It is harder to describe, but this link has a nice visualization of what dilation does.

Note

When ceil_mode=True, sliding windows are allowed to go off-bounds if they start within the left padding or the input. Sliding windows that would start in the right padded region are ignored.

The parameters kernel_size, stride, padding, dilation can either be:

a single int – in which case the same value is used for the height and width dimension

a tuple of two ints – in which case, the first int is used for the height dimension, and the second int for the width dimension

Parameters
:

kernel_size (int | tuple[int, int]) – the size of the window to take a max over

stride (int | tuple[int, int]) – the stride of the window. Default value is kernel_size

padding (int | tuple[int, int]) – Implicit negative infinity padding to be added on both sides

dilation (int | tuple[int, int]) – a parameter that controls the stride of elements in the window

return_indices (bool) – if True, will return the max indices along with the outputs. Useful for torch.nn.MaxUnpool2d later

ceil_mode (bool) – when True, will use ceil instead of floor to compute the output shape

Shape:

Input: 
(
𝑁
,
𝐶
,
𝐻
𝑖
𝑛
,
𝑊
𝑖
𝑛
)
(N,C,H
in
	​

,W
in
	​

)
 or 
(
𝐶
,
𝐻
𝑖
𝑛
,
𝑊
𝑖
𝑛
)
(C,H
in
	​

,W
in
	​

)

Output: 
(
𝑁
,
𝐶
,
𝐻
𝑜
𝑢
𝑡
,
𝑊
𝑜
𝑢
𝑡
)
(N,C,H
out
	​

,W
out
	​

)
 or 
(
𝐶
,
𝐻
𝑜
𝑢
𝑡
,
𝑊
𝑜
𝑢
𝑡
)
(C,H
out
	​

,W
out
	​

)
, where

𝐻
𝑜
𝑢
𝑡
=
⌊
𝐻
𝑖
𝑛
+
2
∗
padding[0]
−
dilation[0]
(
kernel_size[0]
−
1
)
−
1
stride[0]
+
1
⌋
H
out
	​

=⌊
stride[0]
H
in
	​

+2∗padding[0]−dilation[0]×(kernel_size[0]−1)−1
	​

+1⌋
𝑊
𝑜
𝑢
𝑡
=
⌊
𝑊
𝑖
𝑛
+
2
∗
padding[1]
−
dilation[1]
(
kernel_size[1]
−
1
)
−
1
stride[1]
+
1
⌋
W
out
	​

=⌊
stride[1]
W
in
	​

+2∗padding[1]−dilation[1]×(kernel_size[1]−1)−1
	​

+1⌋

Examples:

>>> # pool of square window of size=3, stride=2
>>> m = nn.MaxPool2d(3, stride=2)
>>> # pool of non-square window
>>> m = nn.MaxPool2d((3, 2), stride=(2, 1))
>>> input = torch.randn(20, 16, 50, 32)
>>> output = m(input)

forward(input)
[source]

Runs the forward pass.

 On this page
 Show Source
PyTorch Libraries
ExecuTorch
Helion
torchao
kineto
torchtitan
TorchRL
torchvision
torchaudio
tensordict
PyTorch on XLA Devices