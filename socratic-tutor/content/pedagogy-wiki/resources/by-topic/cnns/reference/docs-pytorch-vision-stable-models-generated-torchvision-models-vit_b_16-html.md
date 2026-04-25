# Source: https://docs.pytorch.org/vision/stable/models/generated/torchvision.models.vit_b_16.html
# Title: vit_b_16 — Torchvision documentation (stable)
# Fetched via: search
# Date: 2026-04-09

# vit_b_16¶
-
**torchvision.models.vit_b_16(***,*weights: [] = None*,*progress: = True*,***kwargs:*) VisionTransformer ¶**
Constructs a vit_b_16 architecture from . - **Parameters:** - **weights**(, optional) – The pretrained weights to use.
See below for more details and possible values.
By default, no pre-trained weights are used.
- **progress**(*,* *optional*) – If True, displays a progress bar of the download to stderr.
Default is True.
- ****kwargs**– parameters passed to the ``` torchvision.models.vision_transformer.VisionTransformer ``` base class.
Please refer to the for more details about this class.
…
***class* torchvision.models.ViT_B_16_Weights(*value*)¶**
The model builder above accepts the following values as the ``` weights ``` parameter.
``` ViT_B_16_Weights.DEFAULT ``` is equivalent to ``` ViT_B_16_Weights.IMAGENET1K_V1 ``` . You can also use strings, e.g. ``` weights='DEFAULT' ``` or ``` weights='IMAGENET1K_V1' ``` .
**ViT_B_16_Weights.IMAGENET1K_V1**: These weights were trained from scratch by using a modified version of ’s training recipe.
Also available as ``` ViT_B_16_Weights.DEFAULT ``` . acc@1 (on ImageNet-1K) 81.072 acc@5 (on ImageNet-1K) 95.318 categories tench, goldfish, great white shark, … (997 omitted) num_params 86567656
min_size height=224, width=224 recipe GFLOPS 17.56 File size 330.3 MB The inference transforms are available at ``` ViT_B_16_Weights.IMAGENET1K_V1.transforms ``` and perform the following preprocessing operations: Accepts ``` PIL.Image ``` , batched ``` (B, C, H, W) ``` and single ``` (C, H, W) ``` image ``` torch.Tensor ``` objects.
The images are resized to ``` resize_size=[256] ``` using ``` interpolation=InterpolationMode.BILINEAR ``` , followed by a central crop of ``` crop_size=[224] ``` . Finally the values are first rescaled to ``` [0.0, 1.0] ``` and then normalized using ``` mean=[0.485, 0.456, 0.406] ``` and ``` std=[0.229, 0.224, 0.225] ``` .
**ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1**: These weights are learnt via transfer learning by end-to-end fine-tuning the original weights on ImageNet-1K data.
acc@1 (on ImageNet-1K) 85.304 acc@
5 (on ImageNet-1K) 97.65 categories tench, goldfish, great white shark, … (997 omitted) recipe license num_params 86859496 min_size height=384, width=384 GFLOPS 55.48 File size 331.4 MB The inference transforms are
available at ``` ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1.transforms ``` and perform the following preprocessing operations: Accepts ``` PIL.Image ``` , batched ``` (B, C, H, W) ``` and single ``` (C, H, W) ``` image ``` torch.Tensor ``` objects.
The images are resized to ``` resize_size=[384] ``` using ``` interpolation=InterpolationMode.BICUBIC ``` , followed by a central crop of ``` crop_size=[384] ``` . Finally the values are first rescaled to ``` [0.0, 1.0] ``` and then normalized using ``` mean=[0.485, 0.456, 0.406] ``` and ``` std=[0.229, 0.224, 0.225] ``` .
**ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1**: These weights are composed of the original frozen trunk weights and a linear classifier learnt on top of them trained on ImageNet-1K data.
acc@1 (on ImageNet-1K) 81.886 acc
@5 (on ImageNet-1K) 96.18 categories tench, goldfish, great white shark, … (997 omitted) recipe license num_params 86567656 min_size height=224, width=224 GFLOPS 17.56 File size 330.3 MB The inference transforms
are available at ``` ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1.transforms ``` and perform the following preprocessing operations: Accepts ``` PIL.Image ``` , batched ``` (B, C, H, W) ``` and single ``` (C, H, W) ``` image ``` torch.Tensor ``` objects.
The images are resized to ``` resize_size=[224] ``` using ``` interpolation=InterpolationMode.BICUBIC ``` , followed by a central crop of ``` crop_size=[224] ``` . Finally the values are first rescaled to ``` [0.0, 1.0] ``` and then normalized using ``` mean=[0.485, 0.456, 0.406] ``` and ``` std=[0.229, 0.224, 0.225] ``` .

# vit_b_16¶
-
**torchvision.models.vit_b_16(***,*weights: [] = None*,*progress: = True*,***kwargs:*) VisionTransformer ¶**
Constructs a vit_b_16 architecture from . - **Parameters:** - **weights**(, optional) – The pretrained weights to use.
See below for more details and possible values.
By default, no pre-trained weights are used.
- **progress**(*,* *optional*) – If True, displays a progress bar of the download to stderr.
Default is True.
- ****kwargs**– parameters passed to the ``` torchvision.models.vision_transformer.VisionTransformer ``` base class.
Please refer to the for more details about this class.
…
***class* torchvision.models.ViT_B_16_Weights(*value*)¶**
The model builder above accepts the following values as the ``` weights ``` parameter.
``` ViT_B_16_Weights.DEFAULT ``` is equivalent to ``` ViT_B_16_Weights.IMAGENET1K_V1 ``` . You can also use strings, e.g. ``` weights='DEFAULT' ``` or ``` weights='IMAGENET1K_V1' ``` .
**ViT_B_16_Weights.IMAGENET1K_V1**: These weights were trained from scratch by using a modified version of ’s training recipe.
Also available as ``` ViT_B_16_Weights.DEFAULT ``` . acc@1 (on ImageNet-1K) 81.072 acc@5 (on ImageNet-1K) 95.318 categories tench, goldfish, great white shark, … (997 omitted) num_params 86567656
min_size height=224, width=224 recipe GFLOPS 17.56 File size 330.3 MB The inference transforms are available at ``` ViT_B_16_Weights.IMAGENET1K_V1.transforms ``` and perform the following preprocessing operations: Accepts ``` PIL.Image ``` , batched ``` (B, C, H, W) ``` and single ``` (C, H, W) ``` image ``` torch.Tensor ``` objects.
The images are resized to ``` resize_size=[256] ``` using ``` interpolation=InterpolationMode.BILINEAR ``` , followed by a central crop of ``` crop_size=[224] ``` . Finally the values are first rescaled to ``` [0.0, 1.0] ``` and then normalized using ``` mean=[0.485, 0.456, 0.406] ``` and ``` std=[0.229, 0.224, 0.225] ``` .
**ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1**: These weights are learnt via transfer learning by end-to-end fine-tuning the original weights on ImageNet-1K data.
acc@1 (on ImageNet-1K) 85.304 acc@
5 (on ImageNet-1K) 97.65 categories tench, goldfish, great white shark, … (997 omitted) recipe license num_params 86859496 min_size height=384, width=384 GFLOPS 55.48 File size 331.4 MB The inference transforms are
available at ``` ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1.transforms ``` and perform the following preprocessing operations: Accepts ``` PIL.Image ``` , batched ``` (B, C, H, W) ``` and single ``` (C, H, W) ``` image ``` torch.Tensor ``` objects.
The images are resized to ``` resize_size=[384] ``` using ``` interpolation=InterpolationMode.BICUBIC ``` , followed by a central crop of ``` crop_size=[384] ``` . Finally the values are first rescaled to ``` [0.0, 1.0] ``` and then normalized using ``` mean=[0.485, 0.456, 0.406] ``` and ``` std=[0.229, 0.224, 0.225] ``` .
**ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1**: These weights are composed of the original frozen trunk weights and a linear classifier learnt on top of them trained on ImageNet-1K data.
acc@1 (on ImageNet-1K) 81.886 acc
@5 (on ImageNet-1K) 96.18 categories tench, goldfish, great white shark, … (997 omitted) recipe license num_params 86567656 min_size height=224, width=224 GFLOPS 17.56 File size 330.3 MB The inference transforms
are available at ``` ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1.transforms ``` and perform the following preprocessing operations: Accepts ``` PIL.Image ``` , batched ``` (B, C, H, W) ``` and single ``` (C, H, W) ``` image ``` torch.Tensor ``` objects.
The images are resized to ``` resize_size=[224] ``` using ``` interpolation=InterpolationMode.BICUBIC ``` , followed by a central crop of ``` crop_size=[224] ``` . Finally the values are first rescaled to ``` [0.0, 1.0] ``` and then normalized using ``` mean=[0.485, 0.456, 0.406] ``` and ``` std=[0.229, 0.224, 0.225] ``` .

# vit_b_16¶
torchvision.models.vit_b_16(
*※*, *weights: [] = None*, *progress: = True*, ***kwargs:*) VisionTransformer ¶
构建 中的 vit_b_16 架构。
- 参数:
**weights**(, 可选) – 使用的预训练权重。有关更多详细信息和可能的值，请参见下面的 。默认情况下，不使用预训练权重。
**progress**( *,* *optional*) – 如果为 True，则在 stderr 上显示下载进度条。默认为 True。
****kwargs**– 传递给
`torchvision.models.vision_transformer.VisionTransformer`基类的参数。有关此类更多详细信息，请参阅 。
*class*torchvision.models.ViT_B_16_Weights( *value*)¶
上面的模型构建器接受以下值作为
`weights`参数。
`ViT_B_16_Weights.DEFAULT`等同于
`ViT_B_16_Weights.IMAGENET1K_V1`。您也可以使用字符串，例如
`weights='DEFAULT'`或
`weights='IMAGENET1K_V1'`。
**ViT_B_16_Weights.IMAGENET1K_V1**:
这些权重是通过使用 的训练配方的修改版本从头开始训练的。也可用作
`ViT_B_16_Weights.DEFAULT`。
acc@1 (在 ImageNet-1K 上)
81.072
acc@5 (在 ImageNet-1K 上)
95.318
类别
丁鲱、金鱼、大白鲨、...
(省略 997 个)
参数数量
86567656
min_size
height=224, width=224
...
推理转换可在
`ViT_B_16_Weights.IMAGENET1K_V1.transforms`获得，并执行以下预处理操作：接受
`PIL.Image`、批处理的
`(B, C, H, W)`和单通道
`(C, H, W)`图像
`torch.Tensor`对象。使用
`interpolation=InterpolationMode.BILINEAR`将图像缩放到
`resize_size=[256]`，然后进行中心裁剪
`crop_size=[224]`。最后，值首先缩放到
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。
**ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1**:
这些权重是通过在 ImageNet-1K 数据上进行端到端微调原始 权重来学习的。
acc@1 (在 ImageNet-1K 上)
85.304
acc@5 (在 ImageNet-1K 上)
97.65
类别
丁鲱、金鱼、大白鲨、...
(省略 997 个)
...
`(B, C, H, W)`和单通道
`(C, H, W)`图像
`torch.Tensor`对象。使用
`interpolation=InterpolationMode.BICUBIC`将图像缩放到
`resize_size=[384]`，然后进行中心裁剪
`crop_size=[384]`。最后，值首先缩放到
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。
**ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1**:
这些权重由原始冻结的 主干权重和一个在 ImageNet-1K 数据上训练的线性分类器组成。
acc@1 (在 ImageNet-1K 上)
81.886
acc@5 (在 ImageNet-1K 上)
96.18
类别
丁鲱、金鱼、大白鲨、...
(省略 997 个)
...
`interpolation=InterpolationMode.BICUBIC`将图像缩放到
`resize_size=[224]`，然后进行中心裁剪
`crop_size=[224]`。最后，值首先缩放到
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。

# vit_b_16¶
torchvision.models.vit_b_16(
***, *weights: [] = None*, *progress: = True*, ***kwargs:*) VisionTransformer ¶
根据构建 vit_b_16 架构。
- 参数：
**weights**(，可选) – 要使用的预训练权重。有关更多详细信息和可能的值，请参见下面的。默认情况下，不使用任何预训练权重。
**progress**( *，* *可选*) – 如果为 True，则将下载进度条显示到标准错误输出。默认为 True。
****kwargs**– 传递给
`torchvision.models.vision_transformer.VisionTransformer`基类的参数。有关此类的更多详细信息，请参阅。
*类*torchvision.models.ViT_B_16_Weights( *value*)¶
上面的模型构建器接受以下值作为
`weights`参数。
`ViT_B_16_Weights.DEFAULT`等效于
`ViT_B_16_Weights.IMAGENET1K_V1`。您也可以使用字符串，例如
`weights='DEFAULT'`或
`weights='IMAGENET1K_V1'`。
**ViT_B_16_Weights.IMAGENET1K_V1**:
这些权重是使用的修改版训练配方从头开始训练的。也可作为
`ViT_B_16_Weights.DEFAULT`使用。
acc@1（在 ImageNet-1K 上）
81.072
acc@5（在 ImageNet-1K 上）
95.318
类别
海鞘、金鱼、大白鲨、……（省略 997 个）
参数数量
86567656
最小尺寸
高度=224，宽度=224
配方
GFLOPS
17.56
文件大小
330.3 MB
推理变换可在
`ViT_B_16_Weights.IMAGENET1K_V1.transforms`中获得，并执行以下预处理操作：接受
`PIL.Image`、批处理
`(B, C, H, W)`和单个
`(C, H, W)`图像
`torch.Tensor`对象。图像使用
`interpolation=InterpolationMode.BILINEAR`调整到
`resize_size=[256]`，然后进行
`crop_size=[224]`的中心裁剪。最后，值首先重新缩放至
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。
**ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1**:
这些权重通过端到端微调原始权重在 ImageNet-1K 数据上进行迁移学习获得。
…
最小尺寸
高度=384，宽度=384
GFLOPS
55.48
...
331.4 MB
...
`ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1.transforms`中获得，并执行以下预处理操作：接受
`PIL.Image`、批处理
`(B, C, H, W)`和单个
`(C, H, W)`图像
`torch.Tensor`对象。图像使用
`interpolation=InterpolationMode.BICUBIC`调整到
`resize_size=[384]`，然后进行
`crop_size=[384]`的中心裁剪。最后，值首先重新缩放至
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。
**ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1**:
这些权重由原始冻结的主干权重和在其之上学习的线性分类器组成，该分类器在 ImageNet-1K 数据上进行训练。
acc@1（在 ImageNet-1K 上）
…
GFLOPS
...
`(B, C, H, W)`和单个
`(C, H, W)`图像
`torch.Tensor`对象。图像使用
`interpolation=InterpolationMode.BICUBIC`调整到
`resize_size=[224]`，然后进行
`crop_size=[224]`的中心裁剪。最后，值首先重新缩放至
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。

# vit_b_16¶
torchvision.models.vit_b_16(
***, *weights: [] = None*, *progress: = True*, ***kwargs:*) VisionTransformer ¶
构建了一个vit_b_16架构，源自 。
- Parameters:
**weights**(, 可选) – 使用的预训练权重。有关更多详情和可能的值，请参见下面的。默认情况下，不使用预训练权重。
**progress**( *,* *可选*) – 如果为True，则在stderr上显示下载进度条。默认值为True。
****kwargs**– 传递给
`torchvision.models.vision_transformer.VisionTransformer`基类的参数。请参阅以获取有关此类的更多详细信息。
*class*torchvision.models.ViT_B_16_Weights( *value*)¶
上面的模型构建器接受以下值作为
`weights`参数。
`ViT_B_16_Weights.DEFAULT`等同于
`ViT_B_16_Weights.IMAGENET1K_V1`。你也可以使用字符串，例如
`weights='DEFAULT'`或
`weights='IMAGENET1K_V1'`。
**ViT_B_16_Weights.IMAGENET1K_V1**:
这些权重是通过使用修改后的训练方法从头开始训练的。
也可作为
`ViT_B_16_Weights.DEFAULT`使用。
准确率@1（在ImageNet-1K上）
81.072
acc@5 (在 ImageNet-1K 上)
95.318
…
`ViT_B_16_Weights.IMAGENET1K_V1.transforms`获取，并执行以下预处理操作：接受
`PIL.Image`、批处理
`(B, C, H, W)`和单张
`(C, H, W)`图像
`torch.Tensor`对象。图像使用
`interpolation=InterpolationMode.BILINEAR`调整大小为
`resize_size=[256]`，然后进行
`crop_size=[224]`的中心裁剪。最后，值首先重新缩放到
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。
**ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1**:
这些权重是通过迁移学习，在ImageNet-1K数据上对原始的 权重进行端到端微调而学习的。
…
最小尺寸
高度=384, 宽度=384
GFLOPS
55.48
文件大小
331.4 MB
推理转换可在
`ViT_B_16_Weights.IMAGENET1K_SWAG_E2E_V1.transforms`处获得，并执行以下预处理操作：接受
`PIL.Image`、批处理
`(B, C, H, W)`和单张
`(C, H, W)`图像
`torch.Tensor`对象。图像使用
`interpolation=InterpolationMode.BICUBIC`调整大小为
`resize_size=[384]`，然后进行
`crop_size=[384]`的中心裁剪。最后，值首先重新缩放到
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。
**ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1**:
这些权重由原始的冻结主干权重和在ImageNet-1K数据上训练的线性分类器组成。
准确率@1（在ImageNet-1K上）
81.886
…
17.56
文件大小
330.3 MB
推理转换可在
`ViT_B_16_Weights.IMAGENET1K_SWAG_LINEAR_V1.transforms`中找到，并执行以下预处理操作：接受
`PIL.Image`、批处理
`(B, C, H, W)`和单张
`(C, H, W)`图像
`torch.Tensor`对象。图像使用
`interpolation=InterpolationMode.BICUBIC`调整大小为
`resize_size=[224]`，然后进行
`crop_size=[224]`的中心裁剪。最后，值首先重新缩放到
`[0.0, 1.0]`，然后使用
`mean=[0.485, 0.456, 0.406]`和
`std=[0.229, 0.224, 0.225]`进行归一化。