# Source: https://huggingface.co/docs/diffusers/api/pipelines/stable_diffusion/stable_diffusion
# Author: Hugging Face
# Author Slug: hugging-face
# Title: Diffusers API Reference: StableDiffusionPipeline
# Fetched via: search
# Date: 2026-04-09

# 🧨 Diffusers Pipelines
Pipelines provide a simple way to run state-of-the-art diffusion models in inference.
Most diffusion systems consist of multiple independently-trained models and highly adaptable scheduler
components - all of which are needed to have a functioning end-to-end diffusion system.
As an example, Stable Diffusion has three independently trained models:
- Autoencoder
- Conditional Unet
- CLIP text encoder
- a scheduler component, scheduler ,
- a CLIPImageProcessor ,
- as well as a safety checker . All of these components are necessary to run stable diffusion in inference even though they were trained or created independently from each other.
To that end, we strive to offer all open-sourced, state-of-the-art diffusion system under a unified API.
More specifically, we strive to provide pipelines that
- 1.
can load the officially published weights and yield 1-to-1 the same outputs as the original implementation according to the corresponding paper (*e.g.* LDMTextToImagePipeline , uses the officially released weights of High-Resolution Image Synthesis with Latent Diffusion Models ),
- 1.
have a simple user interface to run the model in inference (see the Pipelines API section),
- 1. are easy to understand with code that is self-explanatory and can be read along-side the official paper (see Pipelines summary ),
- 1.
can easily be contributed by the community (see the Contribution section).
**Note** that pipelines do not (and should not) offer any training functionality.
If you are looking for *official* training examples, please have a look at examples .
…
|Pipeline|Source|Tasks|Colab|
|--|--|--|--|
|dance diffusion|**Dance Diffusion**|*Unconditional Audio Generation*| |
|ddpm|**Denoising Diffusion Probabilistic Models**|*Unconditional Image Generation*| |
|ddim|**Denoising Diffusion Implicit Models**|*Unconditional Image Generation*| |
|latent_diffusion|**High-Resolution Image Synthesis with Latent Diffusion Models**|*Text-to-Image Generation*| |
|latent_diffusion_uncond|**High-Resolution Image Synthesis with Latent Diffusion Models**|*Unconditional Image Generation*| |
…
|stable_diffusion|**Stable Diffusion**|*Image-to-Image Text-Guided Generation*| |
|stable_diffusion|**Stable Diffusion**|*Text-Guided Image Inpainting*| |
|stochastic_karras_ve|**Elucidating the Design Space of Diffusion-Based Generative Models**|*Unconditional Image Generation*| |
**Note**: Pipelines are simple examples of how to play around with the diffusion systems as described in the corresponding papers.
However, most of them can be adapted to use different scheduler components or even different model components.
...
Diffusion models often consist of multiple independently-trained models or other previously existing components.
Each model has been trained independently on a different task and the scheduler can easily be swapped out and replaced with a different one.
During inference, we however want to be able to easily load all components and use them in inference - even if one component, *e.g.* CLIP's text encoder, originates from a different library, such as Transformers . To that end, all pipelines provide the following functionality:
…
`from_pretrained` method that accepts a Hugging Face Hub repository id, *e.g.* stable-diffusion-v1-5/stable-diffusion-v1-5 or a path to a local directory, *e.g.* "./stable-diffusion".
To correctly retrieve which models and components should be loaded, one has to provide a `model_index.json` file, *e.g.* stable-diffusion-v1-5/stable-diffusion-v1-5/model_index.json , which defines all components that should be loaded into the pipelines.
More specifically, for each model/component one needs to define the format `<name>: ["<library>", "<class name>"]`.
`<name>` is the attribute name given to the loaded instance of `<class name>` which can be found in the library or pipeline folder called `"<library>"`.
- `save_pretrained` that accepts a local path, *e.g.* `./stable-diffusion` under which all models/components of the pipeline will be saved.
For each component/model a folder is created inside the local path that is named after the given attribute name, *e.g.* `./stable_diffusion/unet`.
In addition, a `model_index.json` file is created at the root of the local path, *e.g.* `./stable_diffusion/model_index.json` so that the complete pipeline can again be instantiated
from the local path.
…
[`__call__`] method to use the pipeline in inference.
`__call__` defines inference logic of the pipeline and should ideally encompass all aspects of it, from pre-processing to forwarding tensors to the different models and schedulers, as well as post-processing.
The API of the `__call__` method can strongly vary from pipeline to pipeline.
*E.g.* a text-to-image pipeline, such as `StableDiffusionPipeline` should accept among other things the text prompt to generate the image.
A pure image generation pipeline, such as DDPMPipeline on the other hand can be run without providing any inputs.
To better understand what inputs can be adapted for each pipeline, one should look directly into the respective pipeline.
…
- **Self-contained**: A pipeline shall be as self-contained as possible.
More specifically, this means that all functionality should be either directly defined in the pipeline file itself, should be inherited from (and only from) the `DiffusionPipeline` class or be directly attached to the model and scheduler components of the pipeline.
- **Easy-to-use**: Pipelines should be extremely easy to use - one should be able to load the pipeline and use it for its designated task, *e.g.* text-to-image generation, in just a couple of lines of code.
Most logic including pre-processing, an unrolled diffusion loop, and post-processing should all happen inside the `__call__` method.
…
## Examples
### Text-to-Image generation with Stable Diffusion
```
# make sure you're logged in with `huggingface-cli login`
from diffusers import StableDiffusionPipeline, LMSDiscreteScheduler
pipe = StableDiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5")
pipe = pipe.to("cuda")
prompt = "a photo of an astronaut riding a horse on mars"
image = pipe(prompt).images[0]
image.save("astronaut_rides_horse.png")
```
### Image-to-Image text-guided generation with Stable Diffusion
The `StableDiffusionImg2ImgPipeline` lets you pass a text prompt and an initial image to condition the generation of new images.
```
import requests
from PIL import Image
from io import BytesIO
from diffusers import StableDiffusionImg2ImgPipeline
# load the pipeline
device = "cuda"
pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
"stable-diffusion-v1-5/stable-diffusion-v1-5",
torch_dtype=torch.float16,
).to(device)
# let's download an initial image
url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"
response = requests.get(url)
init_image = Image.open(BytesIO(response.content)).convert("RGB")
init_image = init_image.resize((768, 512))
prompt = "A fantasy landscape, trending on artstation"
images = pipe(prompt=prompt, image=init_image, strength=0.75, guidance_scale=7.5).images
images[0].save("fantasy_landscape.png")
```
You can also run this example on colab
...
The `StableDiffusionInpaintPipeline` lets you edit specific parts of an image by providing a mask and text prompt.
```
import PIL
import requests
import torch
from io import BytesIO
from diffusers import StableDiffusionInpaintPipeline
def download_image(url):
response = requests.get(url)
return PIL.Image.open(BytesIO(response.content)).convert("RGB")
img_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo.png"
mask_url = "https://raw.githubusercontent.com/CompVis/latent-diffusion/main/data/inpainting_examples/overture-creations-5sI6fQgYIuo_mask.png"
init_image = download_image(img_url).resize((512, 512))
mask_image = download_image(mask_url).resize((512, 512))
pipe = StableDiffusionInpaintPipeline.from_pretrained(
"runwayml/stable-diffusion-inpainting",
torch_dtype=torch.float16,
)
pipe = pipe.to("cuda")
prompt = "Face of a yellow cat, high resolution, sitting on a park bench"
image = pipe(prompt=prompt, image=init_image, mask_image=mask_image).images[0]
```
You can also run this example on colab

**Figure 1. Generate images gif or featured image here…**

- What is Hugging Face Diffusers?

- Setting Up Hugging Face Diffusers

- Text-to-Image with Stable Diffusion Pipeline

- Stable Diffusion Image-to-Image Pipeline

- Hugging Face Diffusers AutoPipeline

- AutoPipeline for Image-to-Image

- AutoPipeline for Image InPainting

- Dynamic Masking for Inpainting

- Key Takeaways

- Summary and Conclusion

…

## What is Hugging Face Diffusers?

The

**Diffusers **library by Hugging Face is one of the best libraries for pretrained diffusion models, image, video, and audio generation pipelines. It’s easy to use, and customizable, with a myriad of options to choose from. We can start generating or modifying images with Stable Diffusion models with just a few lines of code.
The following are some of the highlights of the libraries:

**Availability of all the official Stable Diffusion models**along with hundreds of fine-tuned models for task and image specific generation.

- Option to

**swap noise schedulers**with the same pipeline with just a single line of code change.

- Easy integration with Gradio to create seamless UI and shareable applications.

…

## Setting Up Hugging Face Diffusers

Before we jump into its image generation capabilities, we need to install the library along with some additional dependencies.

Install the Hugging Face Diffusers library using the pip command.

pip install diffusers

Along with that, we also need the Transformers and Accelerate libraries.

pip install transformers pip install accelerate

That’s all that is needed as part of setting up Diffusers for image generation. Let’s move into the code for generating images using Diffusers.

…

## Text-to-Image with Stable Diffusion Pipeline

The first step that needs to be done before generating images is

**setting the seed**. This will ensure the generation of the same images for the same prompt and the number of steps. This makes it easier for us to compare images generated from different models, schedulers, and the number of steps.

seed = 42
Here, we will use a seed value of 42.

The diffusers library provides several pipelines for different tasks to use Stable Diffusion models. The most common use case is text-to-image generation for which the diffusers library provides the

`StableDiffusionPipeline`.

Let’s start with creating an image using the pipeline along with the

…

### Stable Diffusion 1.5

First, import

`torch`,

`StableDiffusionPipeline`, and set the computation device.

import torch from diffusers import StableDiffusionPipeline

It is advised to run diffusion models on the GPU, which makes the processing much faster compared to the CPU. We define the GPU device in the following code block.

# Set computation device. device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

Before generating images, initialize the

`StableDiffusionPipeline` using the

`from_pretrained` method. This accepts the model name and a few other parameters, and then we load the pipeline to the GPU device.

pipe = StableDiffusionPipeline.from_pretrained( "runwayml/stable-diffusion-v1-5", use_safetensors=True, torch_dtype=torch.float16, ).to(device)
In the above code block, load the Stable Diffusion 1.5 model from the

`runwayml/stable-diffusion-v1-5` tag andalso use Safetensors and Float 16 data type.

`safetensors` is a new and secure file format for storing and loading tensors of saved models. This new format makes it difficult to store malicious code in saved models, which is becoming increasingly important with the evolution of Generative AI. In the code blocks shown, load safetensors by passing

…

Executing the above code block will download the model and configuration files for the first time if not already present.

The next code block defines a prompt and passes it through the pipeline to generate the image. We run the inference for 150 steps defined by the

`num_inference_steps` parameter. Additionally, we pass the seed to the pipeline so that we always get the same image.

…

### Stable Diffusion 2.1

We can use any Stable Diffusion model using StableDiffusionPipeline. The following example shows the use of

**Stable Diffusion 2.1** to generate an image.

pipe = StableDiffusionPipeline.from_pretrained( "stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16, variant="fp16" ) pipe = pipe.to(device)
While generating the above pipeline, we only need to change the model tag while keeping the other parameters the same.

Then. use the same prompt to generate an image.

prompt = "A photo of a large pirate ship sailing in the middle of a storm and lightning, highly detailed, unreal engine effect" image = pipe( prompt, num_inference_steps=150, generator=torch.manual_seed(seed) ).images[0] image
In most cases, Stable Diffusion 2.1 generates higher fidelity images compared to Stable Diffusion 1.5. It is apparent from the above image as well. Stable Diffusion 2.1 generates images at 768×768 resolution whereas Stable Diffusion 1.5 generates images at 512×512 resolution.

### Using Negative Prompt with StableDiffusionPipeline

When generating images, we would want to minimize distorted, blurry, and unattractive images as much as possible. For this, Diffusers’s pipeline provides a negative_prompt argument which accepts a prompt string signifying the parts that we do not want in the image.

Let’s try that out with Stable Diffusion 2.1.
prompt = "A photo of a large pirate ship sailing in the middle of a storm and lightning, highly detailed, unreal engine effect" image = pipe( prompt, num_inference_steps=150, generator=torch.manual_seed(seed), negative_prompt='low resolution, distorted, ugly, deformed, disfigured, poor details' ).images[0] image
This time, the model generates a much sharper image with more intricate details on the ship and better reflections on the water as well. However, we can also observe loss of detail in the raindrops. This is one of the adverse effects of using negative prompts. Sometimes, they may cause the loss of certain details while enhancing others.

### Swapping Schedulers

Stable Diffusion models use a scheduling technique at each time step to generate the images. You can learn more about schedulers in our Denoising Diffusion Probabilistic Models article.

We can also swap these schedulers to generate different images using the same prompt. In general, some schedulers work better than others. However, in most cases, we can safely leave it to the default setting which is

…

## Stable Diffusion Image-to-Image Pipeline

There are times when we want to transfer the style of one image to another generated image. This is more commonly known as style transfer. We can do so with the Hugging Face Diffusers library using the

`StableDiffusionImg2ImgPipeline`.

First, let’s import the required additional modules.

from PIL import Image from diffusers import StableDiffusionImg2ImgPipeline
Next, initialize a new pipeline and read a style image.

pipe = StableDiffusionImg2ImgPipeline.from_pretrained( 'stabilityai/stable-diffusion-2-1', torch_dtype=torch.float16 ).to(device) image_path = 'images/abstract_art_1.jpg' init_image = Image.open(image_path).convert("RGB") init_image = init_image.resize((768, 768)) init_image
The above is an abstract art image. resize it to 768×768 resolution as the Stable Diffusion 2.1 model will be used for image generation.

While executing the pipeline, we need to pass the

`init_image` and a prompt along with additional arguments needed for image generation.

prompt = "A fantasy landscape, with starry night sky, moonlit river, trending on artstation" image = pipe( prompt=prompt, image=init_image, num_inference_steps=150, strength=1, generator=torch.manual_seed(seed) ).images[0] image
The model outputs a beautiful image preserving the color of the initialization image while following the prompt aptly.

## Hugging Face Diffusers AutoPipeline

Remembering which pipeline to use can be confusing as individuals and even organizations can contribute models. To tackle this, diffusers provide the

`AutoPipeline` which detects the task based on the models and the arguments provided.

We can pass any model path from the Hugging Face Hub depending on the task, no matter which organization has contributed to it or even if it is a stable diffusion variation or not.
Let’s start with a text-to-image example.

from diffusers import AutoPipelineForText2Image

pipe = AutoPipelineForText2Image.from_pretrained( 'stabilityai/stable-diffusion-2-1', torch_dtype=torch.float16, use_safetensors=True ).to(device)

The rest of the code for generating images remains the same as in our previous approach.

…

For now, let’s focus on using

`AutoPipeline` for image inpainting with Stable Diffusion and Hugging Face Diffusers.

from diffusers import AutoPipelineForInpainting from diffusers.utils import load_image

For inpainting, we load the same Stable Diffusion 1.5.

pipeline = AutoPipelineForInpainting.from_pretrained( "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16, use_safetensors=True ).to(device)

…

rlkey=8t556dfxi1mr543j5fdwcg5mc&dl=1" init_image = load_image(img_url).convert("RGB") mask_image = load_image(mask_url).convert("RGB")

Following are the input images and masks.

The mask contains white pixels (255, 255, 255) in the region where the car is present and the rest is black pixels (0, 0, 0). That’s how the Stable Diffusion model knows where to generate the image based on the prompt.

…

## Key Takeaways

**Setting Up Hugging Face Diffusers:**Setting up the Diffusers library is easy and straightforward. It can simply be done with the pip command. **Access to Diffusion Model:**With Diffusers, users get access to hundreds of diffusion based models for image generation, image-to-image style transformer, image inpainting and more. **Running models and Schedulers:**With pipelines, it becomes extremely simple to run models and swap schedulers of different models as well. In fact, with the **AutoPipeline**, the overhead of the model path and initialization is handled by the library, leaving the user with creative task of generating amazing content.

Whether you're a developer or an everyday user, this quicktour will introduce you to 🧨 Diffusers and help you get up and generating quickly!
There are three main components of the library to know about:
- The [
```
DiffusionPipeline
```
] is a high-level end-to-end class designed to rapidly generate samples from pretrained diffusion models for inference.
- Popular pretrained model architectures and modules that can be used as building blocks for creating diffusion systems.
- Many different schedulers - algorithms that control how noise is added for training, and how to generate denoised images during inference.
The quicktour will show you how to use the [
```
DiffusionPipeline
```
] for inference, and then walk you through how to combine a model and scheduler to replicate what's happening inside the [
```
DiffusionPipeline
```
].
The quicktour is a simplified version of the introductory 🧨 Diffusers notebook to help you get started quickly.
If you want to learn more about 🧨 Diffusers' goal, design philosophy, and additional details about its core API, check out the notebook!
…
## DiffusionPipeline
The [
```
DiffusionPipeline
```
] is the easiest way to use a pretrained diffusion system for inference.
It is an end-to-end system containing the model and the scheduler.
You can use the [
```
DiffusionPipeline
```
] out-of-the-box for many tasks.
Take a look at the table below for some supported tasks, and for a complete list of supported tasks, check out the 🧨 Diffusers Summary table.
|**Task**|**Description**|**Pipeline**|
|--|--|--|
|Unconditional Image Generation|generate an image from Gaussian noise|unconditional_image_generation|
|Text-Guided Image Generation|generate an image given a text prompt|conditional_image_generation|
|Text-Guided Image-to-Image Translation|adapt an image guided by a text prompt|img2img|
…
```
DiffusionPipeline
```
] and specify which pipeline checkpoint you would like to download.
You can use the [
```
DiffusionPipeline
```
] for any checkpoint stored on the Hugging Face Hub.
In this quicktour, you'll load the
```
stable-diffusion-v1-5
```
…
```
~DiffusionPipeline.from_pretrained
```
] method:
```
>>> from diffusers import DiffusionPipeline
>>> pipeline = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", use_safetensors=True)
```
The [
```
DiffusionPipeline
```
] downloads and caches all modeling, tokenization, and scheduling components.
You'll see that the Stable Diffusion pipeline is composed of the [
```
UNet2DConditionModel
```
] and [
```
PNDMScheduler
```
] among other things:
```
>>> pipeline
StableDiffusionPipeline {
"_class_name": "StableDiffusionPipeline",
"_diffusers_version": "0.21.4",
...,
"scheduler": [
"diffusers",
"PNDMScheduler"
],
...,
"unet": [
"diffusers",
"UNet2DConditionModel"
],
"vae": [
"diffusers",
"AutoencoderKL"
]
}
```
…
### Local pipeline
You can also use the pipeline locally.
The only difference is you need to download the weights first:
```
!git lfs install
!git clone https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5
```
Then load the saved weights into the pipeline:
```
>>> pipeline = DiffusionPipeline.from_pretrained("./stable-diffusion-v1-5", use_safetensors=True)
```
Now, you can run the pipeline as you would in the section above.
…
```
PNDMScheduler
```
] with the [
```
EulerDiscreteScheduler
```
], load it with the [
```
~diffusers.ConfigMixin.from_config
```
] method:
```
>>> from diffusers import EulerDiscreteScheduler
>>> pipeline = DiffusionPipeline.from_pretrained("stable-diffusion-v1-5/stable-diffusion-v1-5", use_safetensors=True)
>>> pipeline.scheduler = EulerDiscreteScheduler.from_config(pipeline.scheduler.config)
```
…
Some of the most important parameters are:
- ```
sample_size
```
: the height and width dimension of the input sample.
- ```
in_channels
```
: the number of input channels of the input sample.
- ```
down_block_types
```
and
```
up_block_types
```
: the type of down- and upsampling blocks used to create the UNet architecture.
…
## Schedulers
Schedulers manage going from a noisy sample to a less noisy sample given the model output - in this case, it is the
```
noisy_residual
```
.
🧨 Diffusers is a toolbox for building diffusion systems. While the [
```
DiffusionPipeline
```
] is a convenient way to get started with a pre-built diffusion system, you can also choose your own model and scheduler components separately to build a custom diffusion system.

huggingface / **
diffusers ** Public

## Files

# pipeline_stable_diffusion_xl.py

## Latest commit

qgallouedec
and
github-actions[bot]

Use HF Papers ( #11567 )

May 19, 2025

c8bb1ff · May 19, 2025

## History
History

1313 lines (1155 loc) · 66.3 KB

# pipeline_stable_diffusion_xl.py

1313 lines (1155 loc) · 66.3 KB
```
# Copyright 2024 The HuggingFace Team. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0

…

# limitations under the License.

import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import torch
from transformers import (
    CLIPImageProcessor,
    CLIPTextModel,
    CLIPTextModelWithProjection,
    CLIPTokenizer,
    CLIPVisionModelWithProjection,
)
from ...callbacks import MultiPipelineCallbacks, PipelineCallback
from ...image_processor import PipelineImageInput, VaeImageProcessor
from ...loaders import (
    FromSingleFileMixin,
    IPAdapterMixin,
    StableDiffusionXLLoraLoaderMixin,
    TextualInversionLoaderMixin,
)
from ...models import AutoencoderKL, ImageProjection, UNet2DConditionModel
from ...models.attention_processor import (
    AttnProcessor2_0,
    FusedAttnProcessor2_0,
    XFormersAttnProcessor,
)
from ...models.lora import adjust_lora_scale_text_encoder
from ...schedulers import KarrasDiffusionSchedulers
from ...utils import (
    USE_PEFT_BACKEND,
    deprecate,
    is_invisible_watermark_available,
    is_torch_xla_available,
    logging,
    replace_example_docstring,
    scale_lora_layers,
    unscale_lora_layers,
)
from ...utils.torch_utils import randn_tensor
from ..pipeline_utils import DiffusionPipeline, StableDiffusionMixin
from .pipeline_output import StableDiffusionXLPipelineOutput

…

EXAMPLE_DOC_STRING = """
    Examples:
        ```py
        >>> import torch
        >>> from diffusers import StableDiffusionXLPipeline

        >>> pipe = StableDiffusionXLPipeline.from_pretrained(
        ... "stabilityai/stable-diffusion-xl-base-1.0", torch_dtype=torch.float16
        ... )
        >>> pipe = pipe.to("cuda")

        >>> prompt = "a photo of an astronaut riding a horse on mars"
        >>> image = pipe(prompt).images[0]
        ```
"""

…

Args:
        noise_cfg (`torch.Tensor`):
            The predicted noise tensor for the guided diffusion process.
        noise_pred_text (`torch.Tensor`):
            The predicted noise tensor for the text-guided diffusion process.
        guidance_rescale (`float`, *optional*, defaults to 0.0):
            A rescale factor applied to the noise predictions.
    Returns:
        noise_cfg (`torch.Tensor`): The rescaled noise prediction tensor.
    """
    std_text = noise_pred_text.std(dim=list(range(1, noise_pred_text.ndim)), keepdim=True)
    std_cfg = noise_cfg.std(dim=list(range(1, noise_cfg.ndim)), keepdim=True)
    # rescale the results from guidance (fixes overexposure)
    noise_pred_rescaled = noise_cfg * (std_text / std_cfg)
    # mix with the original results from guidance by factor guidance_rescale to avoid "plain looking" images
    noise_cfg = guidance_rescale * noise_pred_rescaled + (1 - guidance_rescale) * noise_cfg
    return noise_cfg

# Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.retrieve_timesteps
def retrieve_timesteps(
    scheduler,
    num_inference_steps: Optional[int] = None,
    device: Optional[Union[str, torch.device]] = None,
    timesteps: Optional[List[int]] = None,
    sigmas: Optional[List[float]] = None,
    **kwargs,
):
    r"""
    Calls the scheduler's `set_timesteps` method and retrieves timesteps from the scheduler after the call. Handles
    custom timesteps. Any kwargs will be supplied to `scheduler.set_timesteps`.
Args:
        scheduler (`SchedulerMixin`):
            The scheduler to get timesteps from.
        num_inference_steps (`int`):
            The number of diffusion steps used when generating samples with a pre-trained model. If used, `timesteps`
            must be `None`.
        device (`str` or `torch.device`, *optional*):
            The device to which the timesteps should be moved to. If `None`, the timesteps are not moved.
        timesteps (`List[int]`, *optional*):
            Custom timesteps used to override the timestep spacing strategy of the scheduler. If `timesteps` is passed,
            `num_inference_steps` and `sigmas` must be `None`.
        sigmas (`List[float]`, *optional*):
            Custom sigmas used to override the timestep spacing strategy of the scheduler. If `sigmas` is passed,
            `num_inference_steps` and `timesteps` must be `None`.

    Returns:
        `Tuple[torch.Tensor, int]`: A tuple where the first element is the timestep schedule from the scheduler and the
        second element is the number of inference steps.
    """
    if timesteps is not None and sigmas is not None:
        raise ValueError("Only one of `timesteps` or `sigmas` can be passed. Please choose one to set custom values")
    if timesteps is not None:
        accepts_timesteps = "timesteps" in set(inspect.signature(scheduler.set_timesteps).parameters.keys())

…

class StableDiffusionXLPipeline(
    DiffusionPipeline,
    StableDiffusionMixin,
    FromSingleFileMixin,
    StableDiffusionXLLoraLoaderMixin,
    TextualInversionLoaderMixin,
    IPAdapterMixin,
):
    r"""
    Pipeline for text-to-image generation using Stable Diffusion XL.
This model inherits from [`DiffusionPipeline`]. Check the superclass documentation for the generic methods the
    library implements for all the pipelines (such as downloading or saving, running on a particular device, etc.)

    The pipeline also inherits the following loading methods:
        - [`~loaders.TextualInversionLoaderMixin.load_textual_inversion`] for loading textual inversion embeddings

…

        - [`~loaders.IPAdapterMixin.load_ip_adapter`] for loading IP Adapters

    Args:
        vae ([`AutoencoderKL`]):
            Variational Auto-Encoder (VAE) Model to encode and decode images to and from latent representations.
        text_encoder ([`CLIPTextModel`]):
            Frozen text-encoder. Stable Diffusion XL uses the text portion of
            [CLIP](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPTextModel), specifically
            the [clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14) variant.
        text_encoder_2 ([` CLIPTextModelWithProjection`]):
            Second frozen text-encoder. Stable Diffusion XL uses the text and pool portion of
        [CLIP](https://huggingface.co/docs/transformers/model_doc/clip#transformers.CLIPTextModelWithProjection),
            specifically the
            [laion/CLIP-ViT-bigG-14-laion2B-39B-b160k](https://huggingface.co/laion/CLIP-ViT-bigG-14-laion2B-39B-b160k)
            variant.
        tokenizer (`CLIPTokenizer`):
            Tokenizer of class
            [CLIPTokenizer](https://huggingface.co/docs/transformers/v4.21.0/en/model_doc/clip#transformers.CLIPTokenizer).
        tokenizer_2 (`CLIPTokenizer`):
            Second Tokenizer of class
            [CLIPTokenizer](https://huggingface.co/docs/transformers/v4.21.0/en/model_doc/clip#transformers.CLIPTokenizer).
        unet ([`UNet2DConditionModel`]): Conditional U-Net architecture to denoise the encoded image latents.
        scheduler ([`SchedulerMixin`]):
            A scheduler to be used in combination with `unet` to denoise the encoded image latents. Can be one of
            [`DDIMScheduler`], [`LMSDiscreteScheduler`], or [`PNDMScheduler`].
        force_zeros_for_empty_prompt (`bool`, *optional*, defaults to `"True"`):
            Whether the negative prompt embeddings shall be forced to always be set to 0. Also see the config of
            `stabilityai/stable-diffusion-xl-base-1-0`.
        add_watermarker (`bool`, *optional*):
            Whether to use the [invisible_watermark library](https://github.com/ShieldMnt/invisible-watermark/) to
            watermark output images. If not defined, it will default to True if the package is installed, otherwise no
            watermarker will be used.
    """

    model_cpu_offload_seq = "text_encoder->text_encoder_2->image_encoder->unet->vae"
    _optional_components = [
        "tokenizer",
        "tokenizer_2",
        "text_encoder",
        "text_encoder_2",
        "image_encoder",
        "feature_extractor",
    ]
    _callback_tensor_inputs = [
        "latents",
        "prompt_embeds",
        "add_text_embeds",
        "add_time_ids",
    ]
    def __init__(
        self,
        vae: AutoencoderKL,
        text_encoder: CLIPTextModel,
        text_encoder_2: CLIPTextModelWithProjection,
        tokenizer: CLIPTokenizer,
        tokenizer_2: CLIPTokenizer,
        unet: UNet2DConditionModel,
        scheduler: KarrasDiffusionSchedulers,
        image_encoder: CLIPVisionModelWithProjection = None,
        feature_extractor: CLIPImageProcessor = None,
        force_zeros_for_empty_prompt: bool = True,
        add_watermarker: Optional[bool] = None,
    ):
        super().__init__()
        self.register_modules(
            vae=vae,
            text_encoder=text_encoder,
            text_encoder_2=text_encoder_2,
            tokenizer=tokenizer,
            tokenizer_2=tokenizer_2,
            unet=unet,
            scheduler=scheduler,
            image_encoder=image_encoder,
            feature_extractor=feature_extractor,
        )
        self.register_to_config(force_zeros_for_empty_prompt=force_zeros_for_empty_prompt)
        self.vae_scale_factor = 2 ** (len(self.vae.config.block_out_channels) - 1) if getattr(self, "vae", None) else 8
        self.image_processor = VaeImageProcessor(vae_scale_factor=self.vae_scale_factor)

…

        if add_watermarker:
            self.watermark = StableDiffusionXLWatermarker()
        else:
            self.watermark = None

    def encode_prompt(
        self,
        prompt: str,
        prompt_2: Optional[str] = None,
        device: Optional[torch.device] = None,
        num_images_per_prompt: int = 1,

…

If not defined, one has to pass
                `negative_prompt_embeds` instead. Ignored when not using guidance (i.e., ignored if `guidance_scale` is
                less than `1`).
            negative_prompt_2 (`str` or `List[str]`, *optional*):
                The prompt or prompts not to guide the image generation to be sent to `tokenizer_2` and

…

Can be used to easily tweak text inputs, *e.g.* prompt
                weighting. If not provided, pooled negative_prompt_embeds will be generated from `negative_prompt`
                input argument.
            lora_scale (`float`, *optional*):
                A lora scale that will be applied to all LoRA layers of the text encoder if LoRA layers are loaded.
            clip_skip (`int`, *optional*):
                Number of layers to be skipped from CLIP while computing the prompt embeddings. A value of 1 means that
                the output of the pre-final layer will be used for computing the prompt embeddings.
        """
        device = device or self._execution_device

        # set lora scale so that monkey patched LoRA
        # function of text encoder can correctly access it
        if lora_scale is not None and isinstance(self, StableDiffusionXLLoraLoaderMixin):
            self._lora_scale = lora_scale

            # dynamically adjust the LoRA scale
            if self.text_encoder is not None:
                if not USE_PEFT_BACKEND:

…

                else:
                    scale_lora_layers(self.text_encoder_2, lora_scale)

        prompt = [prompt] if isinstance(prompt, str) else prompt

        if prompt is not None:
            batch_size = len(prompt)
        else:
            batch_size = prompt_embeds.shape[0]

        # Define tokenizers and text encoders
        tokenizers = [self.tokenizer, self.tokenizer_2] if self.tokenizer is not None else [self.tokenizer_2]
        text_encoders = (
            [self.text_encoder, self.text_encoder_2] if self.text_encoder is not None else [self.text_encoder_2]
        )
        if prompt_embeds is None:
            prompt_2 = prompt_2 or prompt
            prompt_2 = [prompt_2] if isinstance(prompt_2, str) else prompt_2

            # textual inversion: process multi-vector tokens if necessary
            prompt_embeds_list = []
            prompts = [prompt, prompt_2]
            for prompt, tokenizer, text_encoder in zip(prompts, tokenizers, text_encoders):
                if isinstance(self, TextualInversionLoaderMixin):
                prompt = self.maybe_convert_prompt(prompt, tokenizer)

                text_inputs = tokenizer(
                    prompt,
                    padding="max_length",
                    max_length=tokenizer.model_max_length,
                    truncation=True,
                    return_tensors="pt",
                )

                text_input_ids = text_inputs.input_ids
                untruncated_ids = tokenizer(prompt, padding="longest", return_tensors="pt").input_ids

…

                        f" {tokenizer.model_max_length} tokens: {removed_text}"
                    )

                prompt_embeds = text_encoder(text_input_ids.to(device), output_hidden_states=True)

                # We are only ALWAYS interested in the pooled output of the final text encoder
                if pooled_prompt_embeds is None and prompt_embeds[0].ndim == 2:
                    pooled_prompt_embeds = prompt_embeds[0]

                if clip_skip is None:
                    prompt_embeds = prompt_embeds.hidden_states[-2]
                else:
                    # "2" because SDXL always indexes from the penultimate layer.
                    prompt_embeds = prompt_embeds.hidden_states[-(clip_skip + 2)]

…

                    output_hidden_states=True,
                )

                # We are only ALWAYS interested in the pooled output of the final text encoder
                if negative_pooled_prompt_embeds is None and negative_prompt_embeds[0].ndim == 2:
                    negative_pooled_prompt_embeds = negative_prompt_embeds[0]

…

        else:
            prompt_embeds = prompt_embeds.to(dtype=self.unet.dtype, device=device)

        bs_embed, seq_len, _ = prompt_embeds.shape
        # duplicate text embeddings for each generation per prompt, using mps friendly method
        prompt_embeds = prompt_embeds.repeat(1, num_images_per_prompt, 1)
        prompt_embeds = prompt_embeds.view(bs_embed * num_images_per_prompt, seq_len, -1)

        if do_classifier_free_guidance:
            # duplicate unconditional embeddings for each generation per prompt, using mps friendly method
            seq_len = negative_prompt_embeds.shape[1]

            if self.text_encoder_2 is not None:

…

    def encode_image(self, image, device, num_images_per_prompt, output_hidden_states=None):
        dtype = next(self.image_encoder.parameters()).dtype

        if not isinstance(image, torch.Tensor):
            image = self.feature_extractor(image, return_tensors="pt").pixel_values

        image = image.to(device=device, dtype=dtype)
        if output_hidden_states:
            image_enc_hidden_states = self.image_encoder(image, output_hidden_states=True).hidden_states[-2]
            image_enc_hidden_states = image_enc_hidden_states.repeat_interleave(num_images_per_prompt, dim=0)
            uncond_image_enc_hidden_states = self.image_encoder(
                torch.zeros_like(image), output_hidden_states=True

…

            image_embeds = image_embeds.repeat_interleave(num_images_per_prompt, dim=0)
            uncond_image_embeds = torch.zeros_like(image_embeds)

            return image_embeds, uncond_image_embeds

    # Copied from diffusers.pipelines.stable_diffusion.pipeline_stable_diffusion.StableDiffusionPipeline.prepare_ip_adapter_image_embeds

…

                single_image_embeds, single_negative_image_embeds = self.encode_image(
                    single_ip_adapter_image, device, 1, output_hidden_state
                )

                image_embeds.append(single_image_embeds[None, :])
                if do_classifier_free_guidance:
                    negative_image_embeds.append(single_negative_image_embeds[None, :])

10. Click **Launch**.
11. On the next page, click **Connect to Jupyter**.
12. In the Jupyter interface, click on the **New** tab and select **Terminal** where we will do our package installations.
…
```
# Copy this lines to install PyTorch with CUDA support in the terminal
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# Install diffusers, invisible_watermark, transformers, accelerate, and safetensors
pip install diffusers invisible_watermark transformers accelerate safetensors
```
13. In the Jupyter interface, click on the **New** tab and select **Python 3**.
Now you are ready to follow the guide below to set up Stable Diffusion.
## Setting up Stable Diffusion with Hugging Face's Diffusers Library
This guide will walk you through the process of generating and refining images using Hugging Face's Diffusers library.
Follow the steps below to install necessary packages, set up directories, load models, generate images, and refine them.
### Step 2: Import Required Libraries
Import the necessary libraries to use the DiffusionPipeline and other modules.
…
### Step 4: Load the Base Model
Load the base model from Hugging Face's repository.
```
# Load the base model
pipe = DiffusionPipeline.from_pretrained(
"stabilityai/stable-diffusion-xl-base-1.0",
torch_dtype=torch.float16,
use_safetensors=True,
variant="fp16"
)
pipe.to("cuda")
```
…
```
# Generate an image with the base model
prompt = "An astronaut riding a green horse"
image = pipe(prompt=prompt).images[0]
# Save the generated image
output_path = os.path.join(output_dir, "output_image.png")
image.save(output_path)
```
### Step 6: Load the Base and Refiner Models
Load the base and refiner models for further refinement.
```
# Load the base model with specific settings
base = DiffusionPipeline.from_pretrained(
"stabilityai/stable-diffusion-xl-base-1.0", # The pre-trained base model
torch_dtype=torch.float16, # Use 16-bit floating point precision for tensors
variant="fp16", # Specify the model variant as FP16
use_safetensors=True # Use safetensors format for loading the model
)
base.to("cuda") # Move the base model to the GPU for faster inference
# Load the refiner model with shared components and specific settings
refiner = DiffusionPipeline.from_pretrained(
"stabilityai/stable-diffusion-xl-refiner-1.0", # The pre-trained refiner model
text_encoder_2=base.text_encoder_2, # Share the second text encoder from the base model
vae=base.vae, # Share the Variational Autoencoder (VAE) from the base model
torch_dtype=torch.float16, # Use 16-bit floating point precision for tensors
use_safetensors=True, # Use safetensors format for loading the model
variant="fp16" # Specify the model variant as FP16
)
refiner.to("cuda") # Move the refiner model to the GPU for faster inference
```
…
```
# Define the steps and prompt
n_steps = 40 # Number of inference steps for generating and refining the image
high_noise_frac = 0.8 # Fraction of noise to apply during the denoising process
prompt = "A Flying Pig with a sword over a Volcano" # Text prompt for image generation
# Generate the latent image using the base model
latent_image = base(
prompt=prompt, # The text prompt to generate the initial image
num_inference_steps=n_steps, # Number of steps for the inference process
denoising_end=high_noise_frac, # End fraction of the denoising process
output_type="latent" # Output the result as a latent image
).images
# Refine the image using the refiner model
final_image = refiner(
prompt=prompt, # The same text prompt for refining the image
num_inference_steps=n_steps, # Number of steps for the refining process
denoising_start=high_noise_frac, # Start fraction of the denoising process
image=latent_image # The latent image generated by the base model
).images[0]
# Save the refined image
refined_output_path = os.path.join(output_dir, "refined_image.png") # Define the output path for the refined image
final_image.save(refined_output_path) # Save the refined image to the specified path
```
By following these steps, you can generate and refine images using Stable Diffusion and Hugging Face's Diffusers library.
Make sure to update the `output_dir` variable if you want to save images in a different directory.
For more information, visit the Hugging Face Stable Diffusion XL Base Model page.
*This document has been developed by the Center for Applied AI in Protein Dynamics.*