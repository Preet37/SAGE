# Source: https://huggingface.co/docs/diffusers/api/pipelines/controlnet
# Author: Hugging Face
# Author Slug: hugging-face
# Title: Diffusers API Reference: ControlNet Pipelines
# Fetched via: trafilatura
# Date: 2026-04-09

Diffusers documentation
ControlNet
ControlNet
ControlNet was introduced in [Adding Conditional Control to Text-to-Image Diffusion Models](https://huggingface.co/papers/2302.05543) by Lvmin Zhang, Anyi Rao, and Maneesh Agrawala.
With a ControlNet model, you can provide an additional control image to condition and control Stable Diffusion generation. For example, if you provide a depth map, the ControlNet model generates an image that’ll preserve the spatial information from the depth map. It is a more flexible and accurate way to control the image generation process.
The abstract from the paper is:
We present ControlNet, a neural network architecture to add spatial conditioning controls to large, pretrained text-to-image diffusion models. ControlNet locks the production-ready large diffusion models, and reuses their deep and robust encoding layers pretrained with billions of images as a strong backbone to learn a diverse set of conditional controls. The neural architecture is connected with “zero convolutions” (zero-initialized convolution layers) that progressively grow the parameters from zero and ensure that no harmful noise could affect the finetuning. We test various conditioning controls, eg, edges, depth, segmentation, human pose, etc, with Stable Diffusion, using single or multiple conditions, with or without prompts. We show that the training of ControlNets is robust with small (<50k) and large (>1m) datasets. Extensive results show that ControlNet may facilitate wider applications to control image diffusion models.
This model was contributed by [takuma104](https://huggingface.co/takuma104). ❤️
The original codebase can be found at [lllyasviel/ControlNet](https://github.com/lllyasviel/ControlNet), and you can find official ControlNet checkpoints on [lllyasviel’s](https://huggingface.co/lllyasviel) Hub profile.
Make sure to check out the Schedulers
[guide]to learn how to explore the tradeoff between scheduler speed and quality, and see the[reuse components across pipelines]section to learn how to efficiently load the same components into multiple pipelines.
StableDiffusionControlNetPipeline
class diffusers.StableDiffusionControlNetPipeline
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet.py#L162)
( vae: AutoencoderKL text_encoder: CLIPTextModel tokenizer: CLIPTokenizer unet: UNet2DConditionModel controlnet: diffusers.models.controlnets.controlnet.ControlNetModel | list[diffusers.models.controlnets.controlnet.ControlNetModel] | tuple[diffusers.models.controlnets.controlnet.ControlNetModel] | diffusers.models.controlnets.multicontrolnet.MultiControlNetModel scheduler: KarrasDiffusionSchedulers safety_checker: StableDiffusionSafetyChecker feature_extractor: CLIPImageProcessor image_encoder: CLIPVisionModelWithProjection = None requires_safety_checker: bool = True )
Parameters
[vae (](#diffusers.StableDiffusionControlNetPipeline.vae)[AutoencoderKL](/docs/diffusers/v0.37.1/en/api/models/autoencoderkl#diffusers.AutoencoderKL)) — Variational Auto-Encoder (VAE) model to encode and decode images to and from latent representations.[text_encoder (](#diffusers.StableDiffusionControlNetPipeline.text_encoder)[CLIPTextModel](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTextModel)) — Frozen text-encoder ([clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)).[tokenizer (](#diffusers.StableDiffusionControlNetPipeline.tokenizer)[CLIPTokenizer](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTokenizer)) — ACLIPTokenizer
to tokenize text.[unet (](#diffusers.StableDiffusionControlNetPipeline.unet)[UNet2DConditionModel](/docs/diffusers/v0.37.1/en/api/models/unet2d-cond#diffusers.UNet2DConditionModel)) — AUNet2DConditionModel
to denoise the encoded image latents.[controlnet (](#diffusers.StableDiffusionControlNetPipeline.controlnet)[ControlNetModel](/docs/diffusers/v0.37.1/en/api/models/controlnet#diffusers.ControlNetModel)orlist[ControlNetModel]
) — Provides additional conditioning to theunet
during the denoising process. If you set multiple ControlNets as a list, the outputs from each ControlNet are added together to create one combined additional conditioning.[scheduler (](#diffusers.StableDiffusionControlNetPipeline.scheduler)[SchedulerMixin](/docs/diffusers/v0.37.1/en/api/schedulers/overview#diffusers.SchedulerMixin)) — A scheduler to be used in combination withunet
to denoise the encoded image latents. Can be one of[DDIMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/ddim#diffusers.DDIMScheduler),[LMSDiscreteScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/lms_discrete#diffusers.LMSDiscreteScheduler), or[PNDMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/pndm#diffusers.PNDMScheduler).[safety_checker (](#diffusers.StableDiffusionControlNetPipeline.safety_checker)StableDiffusionSafetyChecker
) — Classification module that estimates whether generated images could be considered offensive or harmful. Please refer to the[model card](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5)for more details about a model’s potential harms.[feature_extractor (](#diffusers.StableDiffusionControlNetPipeline.feature_extractor)[CLIPImageProcessor](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPImageProcessor)) — ACLIPImageProcessor
to extract features from generated images; used as inputs to thesafety_checker
.
Pipeline for text-to-image generation using Stable Diffusion with ControlNet guidance.
This model inherits from [DiffusionPipeline](/docs/diffusers/v0.37.1/en/api/pipelines/overview#diffusers.DiffusionPipeline). Check the superclass documentation for the generic methods
implemented for all pipelines (downloading, saving, running on a particular device, etc.).
The pipeline also inherits the following loading methods:
[load_textual_inversion()](/docs/diffusers/v0.37.1/en/api/loaders/textual_inversion#diffusers.loaders.TextualInversionLoaderMixin.load_textual_inversion)for loading textual inversion embeddings[load_lora_weights()](/docs/diffusers/v0.37.1/en/api/loaders/lora#diffusers.loaders.StableDiffusionLoraLoaderMixin.load_lora_weights)for loading LoRA weights[save_lora_weights()](/docs/diffusers/v0.37.1/en/api/loaders/lora#diffusers.loaders.StableDiffusionLoraLoaderMixin.save_lora_weights)for saving LoRA weights[from_single_file()](/docs/diffusers/v0.37.1/en/api/loaders/single_file#diffusers.loaders.FromSingleFileMixin.from_single_file)for loading.ckpt
files[load_ip_adapter()](/docs/diffusers/v0.37.1/en/api/loaders/ip_adapter#diffusers.loaders.IPAdapterMixin.load_ip_adapter)for loading IP Adapters
__call__
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet.py#L907)
( prompt: str | list[str] = None image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] = None height: int | None = None width: int | None = None num_inference_steps: int = 50 timesteps: list = None sigmas: list = None guidance_scale: float = 7.5 negative_prompt: str | list[str] | None = None num_images_per_prompt: int | None = 1 eta: float = 0.0 generator: torch._C.Generator | list[torch._C.Generator] | None = None latents: torch.Tensor | None = None prompt_embeds: torch.Tensor | None = None negative_prompt_embeds: torch.Tensor | None = None ip_adapter_image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] | None = None ip_adapter_image_embeds: list[torch.Tensor] | None = None output_type: str | None = 'pil' return_dict: bool = True cross_attention_kwargs: dict[str, typing.Any] | None = None controlnet_conditioning_scale: float | list[float] = 1.0 guess_mode: bool = False control_guidance_start: float | list[float] = 0.0 control_guidance_end: float | list[float] = 1.0 clip_skip: int | None = None callback_on_step_end: typing.Union[typing.Callable[[int, int], NoneType], diffusers.callbacks.PipelineCallback, diffusers.callbacks.MultiPipelineCallbacks, NoneType] = None callback_on_step_end_tensor_inputs: list = ['latents'] **kwargs ) → [StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) or tuple
Parameters
[prompt (](#diffusers.StableDiffusionControlNetPipeline.__call__.prompt)str
orlist[str]
, optional) — The prompt or prompts to guide image generation. If not defined, you need to passprompt_embeds
.[image (](#diffusers.StableDiffusionControlNetPipeline.__call__.image)torch.Tensor
,PIL.Image.Image
,np.ndarray
,list[torch.Tensor]
,list[PIL.Image.Image]
,list[np.ndarray]
, —list[list[torch.Tensor]]
,list[list[np.ndarray]]
orlist[list[PIL.Image.Image]]
): The ControlNet input condition to provide guidance to theunet
for generation. If the type is specified astorch.Tensor
, it is passed to ControlNet as is.PIL.Image.Image
can also be accepted as an image. The dimensions of the output image defaults toimage
’s dimensions. If height and/or width are passed,image
is resized accordingly. If multiple ControlNets are specified ininit
, images must be passed as a list such that each element of the list can be correctly batched for input to a single ControlNet. Whenprompt
is a list, and if a list of images is passed for a single ControlNet, each will be paired with each prompt in theprompt
list. This also applies to multiple ControlNets, where a list of image lists can be passed to batch for each prompt and each ControlNet.[height (](#diffusers.StableDiffusionControlNetPipeline.__call__.height)int
, optional, defaults toself.unet.config.sample_size * self.vae_scale_factor
) — The height in pixels of the generated image.[width (](#diffusers.StableDiffusionControlNetPipeline.__call__.width)int
, optional, defaults toself.unet.config.sample_size * self.vae_scale_factor
) — The width in pixels of the generated image.[num_inference_steps (](#diffusers.StableDiffusionControlNetPipeline.__call__.num_inference_steps)int
, optional, defaults to 50) — The number of denoising steps. More denoising steps usually lead to a higher quality image at the expense of slower inference.[timesteps (](#diffusers.StableDiffusionControlNetPipeline.__call__.timesteps)list[int]
, optional) — Custom timesteps to use for the denoising process with schedulers which support atimesteps
argument in theirset_timesteps
method. If not defined, the default behavior whennum_inference_steps
is passed will be used. Must be in descending order.[sigmas (](#diffusers.StableDiffusionControlNetPipeline.__call__.sigmas)list[float]
, optional) — Custom sigmas to use for the denoising process with schedulers which support asigmas
argument in theirset_timesteps
method. If not defined, the default behavior whennum_inference_steps
is passed will be used.[guidance_scale (](#diffusers.StableDiffusionControlNetPipeline.__call__.guidance_scale)float
, optional, defaults to 7.5) — A higher guidance scale value encourages the model to generate images closely linked to the textprompt
at the expense of lower image quality. Guidance scale is enabled whenguidance_scale > 1
.[negative_prompt (](#diffusers.StableDiffusionControlNetPipeline.__call__.negative_prompt)str
orlist[str]
, optional) — The prompt or prompts to guide what to not include in image generation. If not defined, you need to passnegative_prompt_embeds
instead. Ignored when not using guidance (guidance_scale < 1
).[num_images_per_prompt (](#diffusers.StableDiffusionControlNetPipeline.__call__.num_images_per_prompt)int
, optional, defaults to 1) — The number of images to generate per prompt.[eta (](#diffusers.StableDiffusionControlNetPipeline.__call__.eta)float
, optional, defaults to 0.0) — Corresponds to parameter eta (η) from the[DDIM](https://huggingface.co/papers/2010.02502)paper. Only applies to the[DDIMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/ddim#diffusers.DDIMScheduler), and is ignored in other schedulers.[generator (](#diffusers.StableDiffusionControlNetPipeline.__call__.generator)torch.Generator
orlist[torch.Generator]
, optional) — Ato make generation deterministic.torch.Generator
[latents (](#diffusers.StableDiffusionControlNetPipeline.__call__.latents)torch.Tensor
, optional) — Pre-generated noisy latents sampled from a Gaussian distribution, to be used as inputs for image generation. Can be used to tweak the same generation with different prompts. If not provided, a latents tensor is generated by sampling using the supplied randomgenerator
.[prompt_embeds (](#diffusers.StableDiffusionControlNetPipeline.__call__.prompt_embeds)torch.Tensor
, optional) — Pre-generated text embeddings. Can be used to easily tweak text inputs (prompt weighting). If not provided, text embeddings are generated from theprompt
input argument.[negative_prompt_embeds (](#diffusers.StableDiffusionControlNetPipeline.__call__.negative_prompt_embeds)torch.Tensor
, optional) — Pre-generated negative text embeddings. Can be used to easily tweak text inputs (prompt weighting). If not provided,negative_prompt_embeds
are generated from thenegative_prompt
input argument.[ip_adapter_image — (](#diffusers.StableDiffusionControlNetPipeline.__call__.ip_adapter_image)PipelineImageInput
, optional): Optional image input to work with IP Adapters.[ip_adapter_image_embeds (](#diffusers.StableDiffusionControlNetPipeline.__call__.ip_adapter_image_embeds)list[torch.Tensor]
, optional) — Pre-generated image embeddings for IP-Adapter. It should be a list of length same as number of IP-adapters. Each element should be a tensor of shape(batch_size, num_images, emb_dim)
. It should contain the negative image embedding ifdo_classifier_free_guidance
is set toTrue
. If not provided, embeddings are computed from theip_adapter_image
input argument.[output_type (](#diffusers.StableDiffusionControlNetPipeline.__call__.output_type)str
, optional, defaults to"pil"
) — The output format of the generated image. Choose betweenPIL.Image
ornp.array
.[return_dict (](#diffusers.StableDiffusionControlNetPipeline.__call__.return_dict)bool
, optional, defaults toTrue
) — Whether or not to return a[StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput)instead of a plain tuple.[callback (](#diffusers.StableDiffusionControlNetPipeline.__call__.callback)Callable
, optional) — A function that calls everycallback_steps
steps during inference. The function is called with the following arguments:callback(step: int, timestep: int, latents: torch.Tensor)
.[callback_steps (](#diffusers.StableDiffusionControlNetPipeline.__call__.callback_steps)int
, optional, defaults to 1) — The frequency at which thecallback
function is called. If not specified, the callback is called at every step.[cross_attention_kwargs (](#diffusers.StableDiffusionControlNetPipeline.__call__.cross_attention_kwargs)dict
, optional) — A kwargs dictionary that if specified is passed along to theAttentionProcessor
as defined in.self.processor
[controlnet_conditioning_scale (](#diffusers.StableDiffusionControlNetPipeline.__call__.controlnet_conditioning_scale)float
orlist[float]
, optional, defaults to 1.0) — The outputs of the ControlNet are multiplied bycontrolnet_conditioning_scale
before they are added to the residual in the originalunet
. If multiple ControlNets are specified ininit
, you can set the corresponding scale as a list.[guess_mode (](#diffusers.StableDiffusionControlNetPipeline.__call__.guess_mode)bool
, optional, defaults toFalse
) — The ControlNet encoder tries to recognize the content of the input image even if you remove all prompts. Aguidance_scale
value between 3.0 and 5.0 is recommended.[control_guidance_start (](#diffusers.StableDiffusionControlNetPipeline.__call__.control_guidance_start)float
orlist[float]
, optional, defaults to 0.0) — The percentage of total steps at which the ControlNet starts applying.[control_guidance_end (](#diffusers.StableDiffusionControlNetPipeline.__call__.control_guidance_end)float
orlist[float]
, optional, defaults to 1.0) — The percentage of total steps at which the ControlNet stops applying.[clip_skip (](#diffusers.StableDiffusionControlNetPipeline.__call__.clip_skip)int
, optional) — Number of layers to be skipped from CLIP while computing the prompt embeddings. A value of 1 means that the output of the pre-final layer will be used for computing the prompt embeddings.[callback_on_step_end (](#diffusers.StableDiffusionControlNetPipeline.__call__.callback_on_step_end)Callable
,PipelineCallback
,MultiPipelineCallbacks
, optional) — A function or a subclass ofPipelineCallback
orMultiPipelineCallbacks
that is called at the end of each denoising step during the inference. with the following arguments:callback_on_step_end(self: DiffusionPipeline, step: int, timestep: int, callback_kwargs: Dict)
.callback_kwargs
will include a list of all tensors as specified bycallback_on_step_end_tensor_inputs
.[callback_on_step_end_tensor_inputs (](#diffusers.StableDiffusionControlNetPipeline.__call__.callback_on_step_end_tensor_inputs)list
, optional) — The list of tensor inputs for thecallback_on_step_end
function. The tensors specified in the list will be passed ascallback_kwargs
argument. You will only be able to include variables listed in the._callback_tensor_inputs
attribute of your pipeline class.
Returns
[StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) or tuple
If return_dict
is True
, [StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) is returned,
otherwise a tuple
is returned where the first element is a list with the generated images and the
second element is a list of bool
s indicating whether the corresponding generated image contains
“not-safe-for-work” (nsfw) content.
The call function to the pipeline for generation.
Examples:
>>> # !pip install opencv-python transformers accelerate
>>> from diffusers import StableDiffusionControlNetPipeline, ControlNetModel, UniPCMultistepScheduler
>>> from diffusers.utils import load_image
>>> import numpy as np
>>> import torch
>>> import cv2
>>> from PIL import Image
>>> # download an image
>>> image = load_image(
... "https://hf.co/datasets/huggingface/documentation-images/resolve/main/diffusers/input_image_vermeer.png"
... )
>>> image = np.array(image)
>>> # get canny image
>>> image = cv2.Canny(image, 100, 200)
>>> image = image[:, :, None]
>>> image = np.concatenate([image, image, image], axis=2)
>>> canny_image = Image.fromarray(image)
>>> # load control net and stable diffusion v1-5
>>> controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
>>> pipe = StableDiffusionControlNetPipeline.from_pretrained(
... "stable-diffusion-v1-5/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
... )
>>> # speed up diffusion process with faster scheduler and memory optimization
>>> pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
>>> # remove following line if xformers is not installed
>>> pipe.enable_xformers_memory_efficient_attention()
>>> pipe.enable_model_cpu_offload()
>>> # generate image
>>> generator = torch.manual_seed(0)
>>> image = pipe(
... "futuristic-looking woman", num_inference_steps=20, generator=generator, image=canny_image
... ).images[0]
enable_attention_slicing
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/pipeline_utils.py#L2040)
( slice_size: str | int = 'auto' )
Parameters
[slice_size (](#diffusers.StableDiffusionControlNetPipeline.enable_attention_slicing.slice_size)str
orint
, optional, defaults to"auto"
) — When"auto"
, halves the input to the attention heads, so attention will be computed in two steps. If"max"
, maximum amount of memory will be saved by running only one slice at a time. If a number is provided, uses as many slices asattention_head_dim // slice_size
. In this case,attention_head_dim
must be a multiple ofslice_size
.
Enable sliced attention computation. When this option is enabled, the attention module splits the input tensor in slices to compute attention in several steps. For more than one attention head, the computation is performed sequentially over each head. This is useful to save some memory in exchange for a small speed decrease.
> ⚠️ Don’t enable attention slicing if you’re already using
scaled_dot_product_attention
(SDPA) from PyTorch > 2.0 or xFormers. These attention computations are already very memory efficient so you won’t need to enable > this function. If you enable attention slicing with SDPA or xFormers, it can lead to serious slow downs!
Examples:
>>> import torch
>>> from diffusers import StableDiffusionPipeline
>>> pipe = StableDiffusionPipeline.from_pretrained(
... "stable-diffusion-v1-5/stable-diffusion-v1-5",
... torch_dtype=torch.float16,
... use_safetensors=True,
... )
>>> prompt = "a photo of an astronaut riding a horse on mars"
>>> pipe.enable_attention_slicing()
>>> image = pipe(prompt).images[0]
Disable sliced attention computation. If enable_attention_slicing
was previously called, attention is
computed in one step.
Enable sliced VAE decoding. When this option is enabled, the VAE will split the input tensor in slices to compute decoding in several steps. This is useful to save some memory and allow larger batch sizes.
Disable sliced VAE decoding. If enable_vae_slicing
was previously enabled, this method will go back to
computing decoding in one step.
enable_xformers_memory_efficient_attention
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/pipeline_utils.py#L1985)
( attention_op: typing.Optional[typing.Callable] = None )
Parameters
[attention_op (](#diffusers.StableDiffusionControlNetPipeline.enable_xformers_memory_efficient_attention.attention_op)Callable
, optional) — Override the defaultNone
operator for use asop
argument to thefunction of xFormers.memory_efficient_attention()
Enable memory efficient attention from [xFormers](https://facebookresearch.github.io/xformers/). When this
option is enabled, you should observe lower GPU memory usage and a potential speed up during inference. Speed
up during training is not guaranteed.
> ⚠️ When memory efficient attention and sliced attention are both enabled, memory efficient attention takes > precedent.
Examples:
>>> import torch
>>> from diffusers import DiffusionPipeline
>>> from xformers.ops import MemoryEfficientAttentionFlashAttentionOp
>>> pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
>>> pipe = pipe.to("cuda")
>>> pipe.enable_xformers_memory_efficient_attention(attention_op=MemoryEfficientAttentionFlashAttentionOp)
>>> # Workaround for not accepting attention shape using VAE for Flash Attention
>>> pipe.vae.enable_xformers_memory_efficient_attention(attention_op=None)
Disable memory efficient attention from [xFormers](https://facebookresearch.github.io/xformers/).
load_textual_inversion
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/loaders/textual_inversion.py#L271)
( pretrained_model_name_or_path: str | list[str] | dict[str, torch.Tensor] | list[dict[str, torch.Tensor]] token: str | list[str] | None = None tokenizer: 'PreTrainedTokenizer' | None = None text_encoder: 'PreTrainedModel' | None = None **kwargs )
Parameters
[pretrained_model_name_or_path (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.pretrained_model_name_or_path)str
oros.PathLike
orlist[str or os.PathLike]
orDict
orlist[Dict]
) — Can be either one of the following or a list of them:- A string, the model id (for example
sd-concepts-library/low-poly-hd-logos-icons
) of a pretrained model hosted on the Hub. - A path to a directory (for example
./my_text_inversion_directory/
) containing the textual inversion weights. - A path to a file (for example
./my_text_inversions.pt
) containing textual inversion weights. - A
[torch state dict](https://pytorch.org/tutorials/beginner/saving_loading_models.html#what-is-a-state-dict).
- A string, the model id (for example
[token (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.token)str
orlist[str]
, optional) — Override the token to use for the textual inversion weights. Ifpretrained_model_name_or_path
is a list, thentoken
must also be a list of equal length.[text_encoder (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.text_encoder)[CLIPTextModel](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTextModel), optional) — Frozen text-encoder ([clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)). If not specified, function will take self.tokenizer.[tokenizer (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.tokenizer)[CLIPTokenizer](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTokenizer), optional) — ACLIPTokenizer
to tokenize text. If not specified, function will take self.tokenizer.[weight_name (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.weight_name)str
, optional) — Name of a custom weight file. This should be used when:- The saved textual inversion file is in 🤗 Diffusers format, but was saved under a specific weight
name such as
text_inv.bin
. - The saved textual inversion file is in the Automatic1111 format.
- The saved textual inversion file is in 🤗 Diffusers format, but was saved under a specific weight
name such as
[cache_dir (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.cache_dir)str | os.PathLike
, optional) — Path to a directory where a downloaded pretrained model configuration is cached if the standard cache is not used.[force_download (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.force_download)bool
, optional, defaults toFalse
) — Whether or not to force the (re-)download of the model weights and configuration files, overriding the cached versions if they exist.[proxies (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.proxies)dict[str, str]
, optional) — A dictionary of proxy servers to use by protocol or endpoint, for example,{'http': 'foo.bar:3128', 'http://hostname': 'foo.bar:4012'}
. The proxies are used on each request.[local_files_only (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.local_files_only)bool
, optional, defaults toFalse
) — Whether to only load local model weights and configuration files or not. If set toTrue
, the model won’t be downloaded from the Hub.[hf_token (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.hf_token)str
or bool, optional) — The token to use as HTTP bearer authorization for remote files. IfTrue
, the token generated fromdiffusers-cli login
(stored in~/.huggingface
) is used.[revision (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.revision)str
, optional, defaults to"main"
) — The specific model version to use. It can be a branch name, a tag name, a commit id, or any identifier allowed by Git.[subfolder (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.subfolder)str
, optional, defaults to""
) — The subfolder location of a model file within a larger model repository on the Hub or locally.[mirror (](#diffusers.StableDiffusionControlNetPipeline.load_textual_inversion.mirror)str
, optional) — Mirror source to resolve accessibility issues if you’re downloading a model in China. We do not guarantee the timeliness or safety of the source, and you should refer to the mirror site for more information.
Load Textual Inversion embeddings into the text encoder of [StableDiffusionPipeline](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/text2img#diffusers.StableDiffusionPipeline) (both 🤗 Diffusers and
Automatic1111 formats are supported).
Example:
To load a Textual Inversion embedding vector in 🤗 Diffusers format:
from diffusers import StableDiffusionPipeline
import torch
model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
pipe.load_textual_inversion("sd-concepts-library/cat-toy")
prompt = "A <cat-toy> backpack"
image = pipe(prompt, num_inference_steps=50).images[0]
image.save("cat-backpack.png")
To load a Textual Inversion embedding vector in Automatic1111 format, make sure to download the vector first
(for example from [civitAI](https://civitai.com/models/3036?modelVersionId=9857)) and then load the vector
locally:
from diffusers import StableDiffusionPipeline
import torch
model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
pipe.load_textual_inversion("./charturnerv2.pt", token="charturnerv2")
prompt = "charturnerv2, multiple views of the same character in the same outfit, a character turnaround of a woman wearing a black jacket and red shirt, best quality, intricate details."
image = pipe(prompt, num_inference_steps=50).images[0]
image.save("character.png")
encode_prompt
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet.py#L298)
( prompt device num_images_per_prompt do_classifier_free_guidance negative_prompt = None prompt_embeds: torch.Tensor | None = None negative_prompt_embeds: torch.Tensor | None = None lora_scale: float | None = None clip_skip: int | None = None )
Parameters
[prompt (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.prompt)str
orlist[str]
, optional) — prompt to be encoded[device — (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.device)torch.device
): torch device[num_images_per_prompt (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.num_images_per_prompt)int
) — number of images that should be generated per prompt[do_classifier_free_guidance (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.do_classifier_free_guidance)bool
) — whether to use classifier free guidance or not[negative_prompt (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.negative_prompt)str
orlist[str]
, optional) — The prompt or prompts not to guide the image generation. If not defined, one has to passnegative_prompt_embeds
instead. Ignored when not using guidance (i.e., ignored ifguidance_scale
is less than1
).[prompt_embeds (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.prompt_embeds)torch.Tensor
, optional) — Pre-generated text embeddings. Can be used to easily tweak text inputs, e.g. prompt weighting. If not provided, text embeddings will be generated fromprompt
input argument.[negative_prompt_embeds (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.negative_prompt_embeds)torch.Tensor
, optional) — Pre-generated negative text embeddings. Can be used to easily tweak text inputs, e.g. prompt weighting. If not provided, negative_prompt_embeds will be generated fromnegative_prompt
input argument.[lora_scale (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.lora_scale)float
, optional) — A LoRA scale that will be applied to all LoRA layers of the text encoder if LoRA layers are loaded.[clip_skip (](#diffusers.StableDiffusionControlNetPipeline.encode_prompt.clip_skip)int
, optional) — Number of layers to be skipped from CLIP while computing the prompt embeddings. A value of 1 means that the output of the pre-final layer will be used for computing the prompt embeddings.
Encodes the prompt into text encoder hidden states.
get_guidance_scale_embedding
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet.py#L850)
( w: Tensor embedding_dim: int = 512 dtype: dtype = torch.float32 ) → torch.Tensor
Parameters
[w (](#diffusers.StableDiffusionControlNetPipeline.get_guidance_scale_embedding.w)torch.Tensor
) — Generate embedding vectors with a specified guidance scale to subsequently enrich timestep embeddings.[embedding_dim (](#diffusers.StableDiffusionControlNetPipeline.get_guidance_scale_embedding.embedding_dim)int
, optional, defaults to 512) — Dimension of the embeddings to generate.[dtype (](#diffusers.StableDiffusionControlNetPipeline.get_guidance_scale_embedding.dtype)torch.dtype
, optional, defaults totorch.float32
) — Data type of the generated embeddings.
Returns
torch.Tensor
Embedding vectors with shape (len(w), embedding_dim)
.
StableDiffusionControlNetImg2ImgPipeline
class diffusers.StableDiffusionControlNetImg2ImgPipeline
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet_img2img.py#L140)
( vae: AutoencoderKL text_encoder: CLIPTextModel tokenizer: CLIPTokenizer unet: UNet2DConditionModel controlnet: diffusers.models.controlnets.controlnet.ControlNetModel | list[diffusers.models.controlnets.controlnet.ControlNetModel] | tuple[diffusers.models.controlnets.controlnet.ControlNetModel] | diffusers.models.controlnets.multicontrolnet.MultiControlNetModel scheduler: KarrasDiffusionSchedulers safety_checker: StableDiffusionSafetyChecker feature_extractor: CLIPImageProcessor image_encoder: CLIPVisionModelWithProjection = None requires_safety_checker: bool = True )
Parameters
[vae (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.vae)[AutoencoderKL](/docs/diffusers/v0.37.1/en/api/models/autoencoderkl#diffusers.AutoencoderKL)) — Variational Auto-Encoder (VAE) model to encode and decode images to and from latent representations.[text_encoder (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.text_encoder)[CLIPTextModel](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTextModel)) — Frozen text-encoder ([clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)).[tokenizer (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.tokenizer)[CLIPTokenizer](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTokenizer)) — ACLIPTokenizer
to tokenize text.[unet (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.unet)[UNet2DConditionModel](/docs/diffusers/v0.37.1/en/api/models/unet2d-cond#diffusers.UNet2DConditionModel)) — AUNet2DConditionModel
to denoise the encoded image latents.[controlnet (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.controlnet)[ControlNetModel](/docs/diffusers/v0.37.1/en/api/models/controlnet#diffusers.ControlNetModel)orlist[ControlNetModel]
) — Provides additional conditioning to theunet
during the denoising process. If you set multiple ControlNets as a list, the outputs from each ControlNet are added together to create one combined additional conditioning.[scheduler (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.scheduler)[SchedulerMixin](/docs/diffusers/v0.37.1/en/api/schedulers/overview#diffusers.SchedulerMixin)) — A scheduler to be used in combination withunet
to denoise the encoded image latents. Can be one of[DDIMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/ddim#diffusers.DDIMScheduler),[LMSDiscreteScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/lms_discrete#diffusers.LMSDiscreteScheduler), or[PNDMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/pndm#diffusers.PNDMScheduler).[safety_checker (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.safety_checker)StableDiffusionSafetyChecker
) — Classification module that estimates whether generated images could be considered offensive or harmful. Please refer to the[model card](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5)for more details about a model’s potential harms.[feature_extractor (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.feature_extractor)[CLIPImageProcessor](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPImageProcessor)) — ACLIPImageProcessor
to extract features from generated images; used as inputs to thesafety_checker
.
Pipeline for image-to-image generation using Stable Diffusion with ControlNet guidance.
This model inherits from [DiffusionPipeline](/docs/diffusers/v0.37.1/en/api/pipelines/overview#diffusers.DiffusionPipeline). Check the superclass documentation for the generic methods
implemented for all pipelines (downloading, saving, running on a particular device, etc.).
The pipeline also inherits the following loading methods:
[load_textual_inversion()](/docs/diffusers/v0.37.1/en/api/loaders/textual_inversion#diffusers.loaders.TextualInversionLoaderMixin.load_textual_inversion)for loading textual inversion embeddings[load_lora_weights()](/docs/diffusers/v0.37.1/en/api/loaders/lora#diffusers.loaders.StableDiffusionLoraLoaderMixin.load_lora_weights)for loading LoRA weights[save_lora_weights()](/docs/diffusers/v0.37.1/en/api/loaders/lora#diffusers.loaders.StableDiffusionLoraLoaderMixin.save_lora_weights)for saving LoRA weights[from_single_file()](/docs/diffusers/v0.37.1/en/api/loaders/single_file#diffusers.loaders.FromSingleFileMixin.from_single_file)for loading.ckpt
files[load_ip_adapter()](/docs/diffusers/v0.37.1/en/api/loaders/ip_adapter#diffusers.loaders.IPAdapterMixin.load_ip_adapter)for loading IP Adapters
__call__
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet_img2img.py#L905)
( prompt: str | list[str] = None image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] = None control_image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] = None height: int | None = None width: int | None = None strength: float = 0.8 num_inference_steps: int = 50 guidance_scale: float = 7.5 negative_prompt: str | list[str] | None = None num_images_per_prompt: int | None = 1 eta: float = 0.0 generator: torch._C.Generator | list[torch._C.Generator] | None = None latents: torch.Tensor | None = None prompt_embeds: torch.Tensor | None = None negative_prompt_embeds: torch.Tensor | None = None ip_adapter_image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] | None = None ip_adapter_image_embeds: list[torch.Tensor] | None = None output_type: str | None = 'pil' return_dict: bool = True cross_attention_kwargs: dict[str, typing.Any] | None = None controlnet_conditioning_scale: float | list[float] = 0.8 guess_mode: bool = False control_guidance_start: float | list[float] = 0.0 control_guidance_end: float | list[float] = 1.0 clip_skip: int | None = None callback_on_step_end: typing.Union[typing.Callable[[int, int], NoneType], diffusers.callbacks.PipelineCallback, diffusers.callbacks.MultiPipelineCallbacks, NoneType] = None callback_on_step_end_tensor_inputs: list = ['latents'] **kwargs ) → [StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) or tuple
Parameters
[prompt (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.prompt)str
orlist[str]
, optional) — The prompt or prompts to guide image generation. If not defined, you need to passprompt_embeds
.[image (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.image)torch.Tensor
,PIL.Image.Image
,np.ndarray
,list[torch.Tensor]
,list[PIL.Image.Image]
,list[np.ndarray]
, —list[list[torch.Tensor]]
,list[list[np.ndarray]]
orlist[list[PIL.Image.Image]]
): The initial image to be used as the starting point for the image generation process. Can also accept image latents asimage
, and if passing latents directly they are not encoded again.[control_image (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.control_image)torch.Tensor
,PIL.Image.Image
,np.ndarray
,list[torch.Tensor]
,list[PIL.Image.Image]
,list[np.ndarray]
, —list[list[torch.Tensor]]
,list[list[np.ndarray]]
orlist[list[PIL.Image.Image]]
): The ControlNet input condition to provide guidance to theunet
for generation. If the type is specified astorch.Tensor
, it is passed to ControlNet as is.PIL.Image.Image
can also be accepted as an image. The dimensions of the output image defaults toimage
’s dimensions. If height and/or width are passed,image
is resized accordingly. If multiple ControlNets are specified ininit
, images must be passed as a list such that each element of the list can be correctly batched for input to a single ControlNet.[height (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.height)int
, optional, defaults toself.unet.config.sample_size * self.vae_scale_factor
) — The height in pixels of the generated image.[width (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.width)int
, optional, defaults toself.unet.config.sample_size * self.vae_scale_factor
) — The width in pixels of the generated image.[strength (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.strength)float
, optional, defaults to 0.8) — Indicates extent to transform the referenceimage
. Must be between 0 and 1.image
is used as a starting point and more noise is added the higher thestrength
. The number of denoising steps depends on the amount of noise initially added. Whenstrength
is 1, added noise is maximum and the denoising process runs for the full number of iterations specified innum_inference_steps
. A value of 1 essentially ignoresimage
.[num_inference_steps (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.num_inference_steps)int
, optional, defaults to 50) — The number of denoising steps. More denoising steps usually lead to a higher quality image at the expense of slower inference.[guidance_scale (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.guidance_scale)float
, optional, defaults to 7.5) — A higher guidance scale value encourages the model to generate images closely linked to the textprompt
at the expense of lower image quality. Guidance scale is enabled whenguidance_scale > 1
.[negative_prompt (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.negative_prompt)str
orlist[str]
, optional) — The prompt or prompts to guide what to not include in image generation. If not defined, you need to passnegative_prompt_embeds
instead. Ignored when not using guidance (guidance_scale < 1
).[num_images_per_prompt (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.num_images_per_prompt)int
, optional, defaults to 1) — The number of images to generate per prompt.[eta (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.eta)float
, optional, defaults to 0.0) — Corresponds to parameter eta (η) from the[DDIM](https://huggingface.co/papers/2010.02502)paper. Only applies to the[DDIMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/ddim#diffusers.DDIMScheduler), and is ignored in other schedulers.[generator (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.generator)torch.Generator
orlist[torch.Generator]
, optional) — Ato make generation deterministic.torch.Generator
[latents (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.latents)torch.Tensor
, optional) — Pre-generated noisy latents sampled from a Gaussian distribution, to be used as inputs for image generation. Can be used to tweak the same generation with different prompts. If not provided, a latents tensor is generated by sampling using the supplied randomgenerator
.[prompt_embeds (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.prompt_embeds)torch.Tensor
, optional) — Pre-generated text embeddings. Can be used to easily tweak text inputs (prompt weighting). If not provided, text embeddings are generated from theprompt
input argument.[negative_prompt_embeds (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.negative_prompt_embeds)torch.Tensor
, optional) — Pre-generated negative text embeddings. Can be used to easily tweak text inputs (prompt weighting). If not provided,negative_prompt_embeds
are generated from thenegative_prompt
input argument.[ip_adapter_image — (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.ip_adapter_image)PipelineImageInput
, optional): Optional image input to work with IP Adapters.[ip_adapter_image_embeds (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.ip_adapter_image_embeds)list[torch.Tensor]
, optional) — Pre-generated image embeddings for IP-Adapter. It should be a list of length same as number of IP-adapters. Each element should be a tensor of shape(batch_size, num_images, emb_dim)
. It should contain the negative image embedding ifdo_classifier_free_guidance
is set toTrue
. If not provided, embeddings are computed from theip_adapter_image
input argument.[output_type (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.output_type)str
, optional, defaults to"pil"
) — The output format of the generated image. Choose betweenPIL.Image
ornp.array
.[return_dict (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.return_dict)bool
, optional, defaults toTrue
) — Whether or not to return a[StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput)instead of a plain tuple.[cross_attention_kwargs (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.cross_attention_kwargs)dict
, optional) — A kwargs dictionary that if specified is passed along to theAttentionProcessor
as defined in.self.processor
[controlnet_conditioning_scale (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.controlnet_conditioning_scale)float
orlist[float]
, optional, defaults to 1.0) — The outputs of the ControlNet are multiplied bycontrolnet_conditioning_scale
before they are added to the residual in the originalunet
. If multiple ControlNets are specified ininit
, you can set the corresponding scale as a list.[guess_mode (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.guess_mode)bool
, optional, defaults toFalse
) — The ControlNet encoder tries to recognize the content of the input image even if you remove all prompts. Aguidance_scale
value between 3.0 and 5.0 is recommended.[control_guidance_start (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.control_guidance_start)float
orlist[float]
, optional, defaults to 0.0) — The percentage of total steps at which the ControlNet starts applying.[control_guidance_end (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.control_guidance_end)float
orlist[float]
, optional, defaults to 1.0) — The percentage of total steps at which the ControlNet stops applying.[clip_skip (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.clip_skip)int
, optional) — Number of layers to be skipped from CLIP while computing the prompt embeddings. A value of 1 means that the output of the pre-final layer will be used for computing the prompt embeddings.[callback_on_step_end (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.callback_on_step_end)Callable
,PipelineCallback
,MultiPipelineCallbacks
, optional) — A function or a subclass ofPipelineCallback
orMultiPipelineCallbacks
that is called at the end of each denoising step during the inference. with the following arguments:callback_on_step_end(self: DiffusionPipeline, step: int, timestep: int, callback_kwargs: Dict)
.callback_kwargs
will include a list of all tensors as specified bycallback_on_step_end_tensor_inputs
.[callback_on_step_end_tensor_inputs (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.__call__.callback_on_step_end_tensor_inputs)list
, optional) — The list of tensor inputs for thecallback_on_step_end
function. The tensors specified in the list will be passed ascallback_kwargs
argument. You will only be able to include variables listed in the._callback_tensor_inputs
attribute of your pipeline class.
Returns
[StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) or tuple
If return_dict
is True
, [StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) is returned,
otherwise a tuple
is returned where the first element is a list with the generated images and the
second element is a list of bool
s indicating whether the corresponding generated image contains
“not-safe-for-work” (nsfw) content.
The call function to the pipeline for generation.
Examples:
>>> # !pip install opencv-python transformers accelerate
>>> from diffusers import StableDiffusionControlNetImg2ImgPipeline, ControlNetModel, UniPCMultistepScheduler
>>> from diffusers.utils import load_image
>>> import numpy as np
>>> import torch
>>> import cv2
>>> from PIL import Image
>>> # download an image
>>> image = load_image(
... "https://hf.co/datasets/huggingface/documentation-images/resolve/main/diffusers/input_image_vermeer.png"
... )
>>> np_image = np.array(image)
>>> # get canny image
>>> np_image = cv2.Canny(np_image, 100, 200)
>>> np_image = np_image[:, :, None]
>>> np_image = np.concatenate([np_image, np_image, np_image], axis=2)
>>> canny_image = Image.fromarray(np_image)
>>> # load control net and stable diffusion v1-5
>>> controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float16)
>>> pipe = StableDiffusionControlNetImg2ImgPipeline.from_pretrained(
... "stable-diffusion-v1-5/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
... )
>>> # speed up diffusion process with faster scheduler and memory optimization
>>> pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
>>> pipe.enable_model_cpu_offload()
>>> # generate image
>>> generator = torch.manual_seed(0)
>>> image = pipe(
... "futuristic-looking woman",
... num_inference_steps=20,
... generator=generator,
... image=image,
... control_image=canny_image,
... ).images[0]
enable_attention_slicing
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/pipeline_utils.py#L2040)
( slice_size: str | int = 'auto' )
Parameters
[slice_size (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.enable_attention_slicing.slice_size)str
orint
, optional, defaults to"auto"
) — When"auto"
, halves the input to the attention heads, so attention will be computed in two steps. If"max"
, maximum amount of memory will be saved by running only one slice at a time. If a number is provided, uses as many slices asattention_head_dim // slice_size
. In this case,attention_head_dim
must be a multiple ofslice_size
.
Enable sliced attention computation. When this option is enabled, the attention module splits the input tensor in slices to compute attention in several steps. For more than one attention head, the computation is performed sequentially over each head. This is useful to save some memory in exchange for a small speed decrease.
> ⚠️ Don’t enable attention slicing if you’re already using
scaled_dot_product_attention
(SDPA) from PyTorch > 2.0 or xFormers. These attention computations are already very memory efficient so you won’t need to enable > this function. If you enable attention slicing with SDPA or xFormers, it can lead to serious slow downs!
Examples:
>>> import torch
>>> from diffusers import StableDiffusionPipeline
>>> pipe = StableDiffusionPipeline.from_pretrained(
... "stable-diffusion-v1-5/stable-diffusion-v1-5",
... torch_dtype=torch.float16,
... use_safetensors=True,
... )
>>> prompt = "a photo of an astronaut riding a horse on mars"
>>> pipe.enable_attention_slicing()
>>> image = pipe(prompt).images[0]
Disable sliced attention computation. If enable_attention_slicing
was previously called, attention is
computed in one step.
Enable sliced VAE decoding. When this option is enabled, the VAE will split the input tensor in slices to compute decoding in several steps. This is useful to save some memory and allow larger batch sizes.
Disable sliced VAE decoding. If enable_vae_slicing
was previously enabled, this method will go back to
computing decoding in one step.
enable_xformers_memory_efficient_attention
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/pipeline_utils.py#L1985)
( attention_op: typing.Optional[typing.Callable] = None )
Parameters
[attention_op (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.enable_xformers_memory_efficient_attention.attention_op)Callable
, optional) — Override the defaultNone
operator for use asop
argument to thefunction of xFormers.memory_efficient_attention()
Enable memory efficient attention from [xFormers](https://facebookresearch.github.io/xformers/). When this
option is enabled, you should observe lower GPU memory usage and a potential speed up during inference. Speed
up during training is not guaranteed.
> ⚠️ When memory efficient attention and sliced attention are both enabled, memory efficient attention takes > precedent.
Examples:
>>> import torch
>>> from diffusers import DiffusionPipeline
>>> from xformers.ops import MemoryEfficientAttentionFlashAttentionOp
>>> pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
>>> pipe = pipe.to("cuda")
>>> pipe.enable_xformers_memory_efficient_attention(attention_op=MemoryEfficientAttentionFlashAttentionOp)
>>> # Workaround for not accepting attention shape using VAE for Flash Attention
>>> pipe.vae.enable_xformers_memory_efficient_attention(attention_op=None)
Disable memory efficient attention from [xFormers](https://facebookresearch.github.io/xformers/).
load_textual_inversion
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/loaders/textual_inversion.py#L271)
( pretrained_model_name_or_path: str | list[str] | dict[str, torch.Tensor] | list[dict[str, torch.Tensor]] token: str | list[str] | None = None tokenizer: 'PreTrainedTokenizer' | None = None text_encoder: 'PreTrainedModel' | None = None **kwargs )
Parameters
[pretrained_model_name_or_path (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.pretrained_model_name_or_path)str
oros.PathLike
orlist[str or os.PathLike]
orDict
orlist[Dict]
) — Can be either one of the following or a list of them:- A string, the model id (for example
sd-concepts-library/low-poly-hd-logos-icons
) of a pretrained model hosted on the Hub. - A path to a directory (for example
./my_text_inversion_directory/
) containing the textual inversion weights. - A path to a file (for example
./my_text_inversions.pt
) containing textual inversion weights. - A
[torch state dict](https://pytorch.org/tutorials/beginner/saving_loading_models.html#what-is-a-state-dict).
- A string, the model id (for example
[token (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.token)str
orlist[str]
, optional) — Override the token to use for the textual inversion weights. Ifpretrained_model_name_or_path
is a list, thentoken
must also be a list of equal length.[text_encoder (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.text_encoder)[CLIPTextModel](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTextModel), optional) — Frozen text-encoder ([clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)). If not specified, function will take self.tokenizer.[tokenizer (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.tokenizer)[CLIPTokenizer](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTokenizer), optional) — ACLIPTokenizer
to tokenize text. If not specified, function will take self.tokenizer.[weight_name (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.weight_name)str
, optional) — Name of a custom weight file. This should be used when:- The saved textual inversion file is in 🤗 Diffusers format, but was saved under a specific weight
name such as
text_inv.bin
. - The saved textual inversion file is in the Automatic1111 format.
- The saved textual inversion file is in 🤗 Diffusers format, but was saved under a specific weight
name such as
[cache_dir (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.cache_dir)str | os.PathLike
, optional) — Path to a directory where a downloaded pretrained model configuration is cached if the standard cache is not used.[force_download (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.force_download)bool
, optional, defaults toFalse
) — Whether or not to force the (re-)download of the model weights and configuration files, overriding the cached versions if they exist.[proxies (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.proxies)dict[str, str]
, optional) — A dictionary of proxy servers to use by protocol or endpoint, for example,{'http': 'foo.bar:3128', 'http://hostname': 'foo.bar:4012'}
. The proxies are used on each request.[local_files_only (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.local_files_only)bool
, optional, defaults toFalse
) — Whether to only load local model weights and configuration files or not. If set toTrue
, the model won’t be downloaded from the Hub.[hf_token (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.hf_token)str
or bool, optional) — The token to use as HTTP bearer authorization for remote files. IfTrue
, the token generated fromdiffusers-cli login
(stored in~/.huggingface
) is used.[revision (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.revision)str
, optional, defaults to"main"
) — The specific model version to use. It can be a branch name, a tag name, a commit id, or any identifier allowed by Git.[subfolder (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.subfolder)str
, optional, defaults to""
) — The subfolder location of a model file within a larger model repository on the Hub or locally.[mirror (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.load_textual_inversion.mirror)str
, optional) — Mirror source to resolve accessibility issues if you’re downloading a model in China. We do not guarantee the timeliness or safety of the source, and you should refer to the mirror site for more information.
Load Textual Inversion embeddings into the text encoder of [StableDiffusionPipeline](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/text2img#diffusers.StableDiffusionPipeline) (both 🤗 Diffusers and
Automatic1111 formats are supported).
Example:
To load a Textual Inversion embedding vector in 🤗 Diffusers format:
from diffusers import StableDiffusionPipeline
import torch
model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
pipe.load_textual_inversion("sd-concepts-library/cat-toy")
prompt = "A <cat-toy> backpack"
image = pipe(prompt, num_inference_steps=50).images[0]
image.save("cat-backpack.png")
To load a Textual Inversion embedding vector in Automatic1111 format, make sure to download the vector first
(for example from [civitAI](https://civitai.com/models/3036?modelVersionId=9857)) and then load the vector
locally:
from diffusers import StableDiffusionPipeline
import torch
model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
pipe.load_textual_inversion("./charturnerv2.pt", token="charturnerv2")
prompt = "charturnerv2, multiple views of the same character in the same outfit, a character turnaround of a woman wearing a black jacket and red shirt, best quality, intricate details."
image = pipe(prompt, num_inference_steps=50).images[0]
image.save("character.png")
encode_prompt
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet_img2img.py#L276)
( prompt device num_images_per_prompt do_classifier_free_guidance negative_prompt = None prompt_embeds: torch.Tensor | None = None negative_prompt_embeds: torch.Tensor | None = None lora_scale: float | None = None clip_skip: int | None = None )
Parameters
[prompt (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.prompt)str
orlist[str]
, optional) — prompt to be encoded[device — (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.device)torch.device
): torch device[num_images_per_prompt (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.num_images_per_prompt)int
) — number of images that should be generated per prompt[do_classifier_free_guidance (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.do_classifier_free_guidance)bool
) — whether to use classifier free guidance or not[negative_prompt (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.negative_prompt)str
orlist[str]
, optional) — The prompt or prompts not to guide the image generation. If not defined, one has to passnegative_prompt_embeds
instead. Ignored when not using guidance (i.e., ignored ifguidance_scale
is less than1
).[prompt_embeds (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.prompt_embeds)torch.Tensor
, optional) — Pre-generated text embeddings. Can be used to easily tweak text inputs, e.g. prompt weighting. If not provided, text embeddings will be generated fromprompt
input argument.[negative_prompt_embeds (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.negative_prompt_embeds)torch.Tensor
, optional) — Pre-generated negative text embeddings. Can be used to easily tweak text inputs, e.g. prompt weighting. If not provided, negative_prompt_embeds will be generated fromnegative_prompt
input argument.[lora_scale (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.lora_scale)float
, optional) — A LoRA scale that will be applied to all LoRA layers of the text encoder if LoRA layers are loaded.[clip_skip (](#diffusers.StableDiffusionControlNetImg2ImgPipeline.encode_prompt.clip_skip)int
, optional) — Number of layers to be skipped from CLIP while computing the prompt embeddings. A value of 1 means that the output of the pre-final layer will be used for computing the prompt embeddings.
Encodes the prompt into text encoder hidden states.
StableDiffusionControlNetInpaintPipeline
class diffusers.StableDiffusionControlNetInpaintPipeline
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet_inpaint.py#L128)
( vae: AutoencoderKL text_encoder: CLIPTextModel tokenizer: CLIPTokenizer unet: UNet2DConditionModel controlnet: diffusers.models.controlnets.controlnet.ControlNetModel | list[diffusers.models.controlnets.controlnet.ControlNetModel] | tuple[diffusers.models.controlnets.controlnet.ControlNetModel] | diffusers.models.controlnets.multicontrolnet.MultiControlNetModel scheduler: KarrasDiffusionSchedulers safety_checker: StableDiffusionSafetyChecker feature_extractor: CLIPImageProcessor image_encoder: CLIPVisionModelWithProjection = None requires_safety_checker: bool = True )
Parameters
[vae (](#diffusers.StableDiffusionControlNetInpaintPipeline.vae)[AutoencoderKL](/docs/diffusers/v0.37.1/en/api/models/autoencoderkl#diffusers.AutoencoderKL)) — Variational Auto-Encoder (VAE) model to encode and decode images to and from latent representations.[text_encoder (](#diffusers.StableDiffusionControlNetInpaintPipeline.text_encoder)[CLIPTextModel](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTextModel)) — Frozen text-encoder ([clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)).[tokenizer (](#diffusers.StableDiffusionControlNetInpaintPipeline.tokenizer)[CLIPTokenizer](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTokenizer)) — ACLIPTokenizer
to tokenize text.[unet (](#diffusers.StableDiffusionControlNetInpaintPipeline.unet)[UNet2DConditionModel](/docs/diffusers/v0.37.1/en/api/models/unet2d-cond#diffusers.UNet2DConditionModel)) — AUNet2DConditionModel
to denoise the encoded image latents.[controlnet (](#diffusers.StableDiffusionControlNetInpaintPipeline.controlnet)[ControlNetModel](/docs/diffusers/v0.37.1/en/api/models/controlnet#diffusers.ControlNetModel)orlist[ControlNetModel]
) — Provides additional conditioning to theunet
during the denoising process. If you set multiple ControlNets as a list, the outputs from each ControlNet are added together to create one combined additional conditioning.[scheduler (](#diffusers.StableDiffusionControlNetInpaintPipeline.scheduler)[SchedulerMixin](/docs/diffusers/v0.37.1/en/api/schedulers/overview#diffusers.SchedulerMixin)) — A scheduler to be used in combination withunet
to denoise the encoded image latents. Can be one of[DDIMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/ddim#diffusers.DDIMScheduler),[LMSDiscreteScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/lms_discrete#diffusers.LMSDiscreteScheduler), or[PNDMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/pndm#diffusers.PNDMScheduler).[safety_checker (](#diffusers.StableDiffusionControlNetInpaintPipeline.safety_checker)StableDiffusionSafetyChecker
) — Classification module that estimates whether generated images could be considered offensive or harmful. Please refer to the[model card](https://huggingface.co/stable-diffusion-v1-5/stable-diffusion-v1-5)for more details about a model’s potential harms.[feature_extractor (](#diffusers.StableDiffusionControlNetInpaintPipeline.feature_extractor)[CLIPImageProcessor](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPImageProcessor)) — ACLIPImageProcessor
to extract features from generated images; used as inputs to thesafety_checker
.
Pipeline for image inpainting using Stable Diffusion with ControlNet guidance.
This model inherits from [DiffusionPipeline](/docs/diffusers/v0.37.1/en/api/pipelines/overview#diffusers.DiffusionPipeline). Check the superclass documentation for the generic methods
implemented for all pipelines (downloading, saving, running on a particular device, etc.).
The pipeline also inherits the following loading methods:
[load_textual_inversion()](/docs/diffusers/v0.37.1/en/api/loaders/textual_inversion#diffusers.loaders.TextualInversionLoaderMixin.load_textual_inversion)for loading textual inversion embeddings[load_lora_weights()](/docs/diffusers/v0.37.1/en/api/loaders/lora#diffusers.loaders.StableDiffusionLoraLoaderMixin.load_lora_weights)for loading LoRA weights[save_lora_weights()](/docs/diffusers/v0.37.1/en/api/loaders/lora#diffusers.loaders.StableDiffusionLoraLoaderMixin.save_lora_weights)for saving LoRA weights[from_single_file()](/docs/diffusers/v0.37.1/en/api/loaders/single_file#diffusers.loaders.FromSingleFileMixin.from_single_file)for loading.ckpt
files[load_ip_adapter()](/docs/diffusers/v0.37.1/en/api/loaders/ip_adapter#diffusers.loaders.IPAdapterMixin.load_ip_adapter)for loading IP Adapters
> This pipeline can be used with checkpoints that have been specifically fine-tuned for inpainting > (
[stable-diffusion-v1-5/stable-diffusion-inpainting]) as well as default text-to-image Stable Diffusion checkpoints > ([stable-diffusion-v1-5/stable-diffusion-v1-5]). Default text-to-image Stable Diffusion checkpoints might be preferable for ControlNets that have been fine-tuned on > those, such as[lllyasviel/control_v11p_sd15_inpaint].
__call__
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet_inpaint.py#L994)
( prompt: str | list[str] = None image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] = None mask_image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] = None control_image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] = None height: int | None = None width: int | None = None padding_mask_crop: int | None = None strength: float = 1.0 num_inference_steps: int = 50 guidance_scale: float = 7.5 negative_prompt: str | list[str] | None = None num_images_per_prompt: int | None = 1 eta: float = 0.0 generator: torch._C.Generator | list[torch._C.Generator] | None = None latents: torch.Tensor | None = None prompt_embeds: torch.Tensor | None = None negative_prompt_embeds: torch.Tensor | None = None ip_adapter_image: PIL.Image.Image | numpy.ndarray | torch.Tensor | list[PIL.Image.Image] | list[numpy.ndarray] | list[torch.Tensor] | None = None ip_adapter_image_embeds: list[torch.Tensor] | None = None output_type: str | None = 'pil' return_dict: bool = True cross_attention_kwargs: dict[str, typing.Any] | None = None controlnet_conditioning_scale: float | list[float] = 0.5 guess_mode: bool = False control_guidance_start: float | list[float] = 0.0 control_guidance_end: float | list[float] = 1.0 clip_skip: int | None = None callback_on_step_end: typing.Union[typing.Callable[[int, int], NoneType], diffusers.callbacks.PipelineCallback, diffusers.callbacks.MultiPipelineCallbacks, NoneType] = None callback_on_step_end_tensor_inputs: list = ['latents'] **kwargs ) → [StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) or tuple
Parameters
[prompt (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.prompt)str
orlist[str]
, optional) — The prompt or prompts to guide image generation. If not defined, you need to passprompt_embeds
.[image (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.image)torch.Tensor
,PIL.Image.Image
,np.ndarray
,list[torch.Tensor]
, —list[PIL.Image.Image]
, orlist[np.ndarray]
):Image
, NumPy array or tensor representing an image batch to be used as the starting point. For both NumPy array and PyTorch tensor, the expected value range is between[0, 1]
. If it’s a tensor or a list or tensors, the expected shape should be(B, C, H, W)
or(C, H, W)
. If it is a NumPy array or a list of arrays, the expected shape should be(B, H, W, C)
or(H, W, C)
. It can also accept image latents asimage
, but if passing latents directly it is not encoded again.[mask_image (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.mask_image)torch.Tensor
,PIL.Image.Image
,np.ndarray
,list[torch.Tensor]
, —list[PIL.Image.Image]
, orlist[np.ndarray]
):Image
, NumPy array or tensor representing an image batch to maskimage
. White pixels in the mask are repainted while black pixels are preserved. Ifmask_image
is a PIL image, it is converted to a single channel (luminance) before use. If it’s a NumPy array or PyTorch tensor, it should contain one color channel (L) instead of 3, so the expected shape for PyTorch tensor would be(B, 1, H, W)
,(B, H, W)
,(1, H, W)
,(H, W)
. And for NumPy array, it would be for(B, H, W, 1)
,(B, H, W)
,(H, W, 1)
, or(H, W)
.[control_image (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.control_image)torch.Tensor
,PIL.Image.Image
,list[torch.Tensor]
,list[PIL.Image.Image]
, —list[list[torch.Tensor]]
, orlist[list[PIL.Image.Image]]
): The ControlNet input condition to provide guidance to theunet
for generation. If the type is specified astorch.Tensor
, it is passed to ControlNet as is.PIL.Image.Image
can also be accepted as an image. The dimensions of the output image defaults toimage
’s dimensions. If height and/or width are passed,image
is resized accordingly. If multiple ControlNets are specified ininit
, images must be passed as a list such that each element of the list can be correctly batched for input to a single ControlNet.[height (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.height)int
, optional, defaults toself.unet.config.sample_size * self.vae_scale_factor
) — The height in pixels of the generated image.[width (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.width)int
, optional, defaults toself.unet.config.sample_size * self.vae_scale_factor
) — The width in pixels of the generated image.[padding_mask_crop (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.padding_mask_crop)int
, optional, defaults toNone
) — The size of margin in the crop to be applied to the image and masking. IfNone
, no crop is applied to image and mask_image. Ifpadding_mask_crop
is notNone
, it will first find a rectangular region with the same aspect ration of the image and contains all masked area, and then expand that area based onpadding_mask_crop
. The image and mask_image will then be cropped based on the expanded area before resizing to the original image size for inpainting. This is useful when the masked area is small while the image is large and contain information irrelevant for inpainting, such as background.[strength (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.strength)float
, optional, defaults to 1.0) — Indicates extent to transform the referenceimage
. Must be between 0 and 1.image
is used as a starting point and more noise is added the higher thestrength
. The number of denoising steps depends on the amount of noise initially added. Whenstrength
is 1, added noise is maximum and the denoising process runs for the full number of iterations specified innum_inference_steps
. A value of 1 essentially ignoresimage
.[num_inference_steps (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.num_inference_steps)int
, optional, defaults to 50) — The number of denoising steps. More denoising steps usually lead to a higher quality image at the expense of slower inference.[guidance_scale (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.guidance_scale)float
, optional, defaults to 7.5) — A higher guidance scale value encourages the model to generate images closely linked to the textprompt
at the expense of lower image quality. Guidance scale is enabled whenguidance_scale > 1
.[negative_prompt (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.negative_prompt)str
orlist[str]
, optional) — The prompt or prompts to guide what to not include in image generation. If not defined, you need to passnegative_prompt_embeds
instead. Ignored when not using guidance (guidance_scale < 1
).[num_images_per_prompt (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.num_images_per_prompt)int
, optional, defaults to 1) — The number of images to generate per prompt.[eta (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.eta)float
, optional, defaults to 0.0) — Corresponds to parameter eta (η) from the[DDIM](https://huggingface.co/papers/2010.02502)paper. Only applies to the[DDIMScheduler](/docs/diffusers/v0.37.1/en/api/schedulers/ddim#diffusers.DDIMScheduler), and is ignored in other schedulers.[generator (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.generator)torch.Generator
orlist[torch.Generator]
, optional) — Ato make generation deterministic.torch.Generator
[latents (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.latents)torch.Tensor
, optional) — Pre-generated noisy latents sampled from a Gaussian distribution, to be used as inputs for image generation. Can be used to tweak the same generation with different prompts. If not provided, a latents tensor is generated by sampling using the supplied randomgenerator
.[prompt_embeds (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.prompt_embeds)torch.Tensor
, optional) — Pre-generated text embeddings. Can be used to easily tweak text inputs (prompt weighting). If not provided, text embeddings are generated from theprompt
input argument.[negative_prompt_embeds (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.negative_prompt_embeds)torch.Tensor
, optional) — Pre-generated negative text embeddings. Can be used to easily tweak text inputs (prompt weighting). If not provided,negative_prompt_embeds
are generated from thenegative_prompt
input argument.[ip_adapter_image — (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.ip_adapter_image)PipelineImageInput
, optional): Optional image input to work with IP Adapters.[ip_adapter_image_embeds (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.ip_adapter_image_embeds)list[torch.Tensor]
, optional) — Pre-generated image embeddings for IP-Adapter. It should be a list of length same as number of IP-adapters. Each element should be a tensor of shape(batch_size, num_images, emb_dim)
. It should contain the negative image embedding ifdo_classifier_free_guidance
is set toTrue
. If not provided, embeddings are computed from theip_adapter_image
input argument.[output_type (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.output_type)str
, optional, defaults to"pil"
) — The output format of the generated image. Choose betweenPIL.Image
ornp.array
.[return_dict (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.return_dict)bool
, optional, defaults toTrue
) — Whether or not to return a[StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput)instead of a plain tuple.[cross_attention_kwargs (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.cross_attention_kwargs)dict
, optional) — A kwargs dictionary that if specified is passed along to theAttentionProcessor
as defined in.self.processor
[controlnet_conditioning_scale (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.controlnet_conditioning_scale)float
orlist[float]
, optional, defaults to 0.5) — The outputs of the ControlNet are multiplied bycontrolnet_conditioning_scale
before they are added to the residual in the originalunet
. If multiple ControlNets are specified ininit
, you can set the corresponding scale as a list.[guess_mode (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.guess_mode)bool
, optional, defaults toFalse
) — The ControlNet encoder tries to recognize the content of the input image even if you remove all prompts. Aguidance_scale
value between 3.0 and 5.0 is recommended.[control_guidance_start (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.control_guidance_start)float
orlist[float]
, optional, defaults to 0.0) — The percentage of total steps at which the ControlNet starts applying.[control_guidance_end (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.control_guidance_end)float
orlist[float]
, optional, defaults to 1.0) — The percentage of total steps at which the ControlNet stops applying.[clip_skip (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.clip_skip)int
, optional) — Number of layers to be skipped from CLIP while computing the prompt embeddings. A value of 1 means that the output of the pre-final layer will be used for computing the prompt embeddings.[callback_on_step_end (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.callback_on_step_end)Callable
,PipelineCallback
,MultiPipelineCallbacks
, optional) — A function or a subclass ofPipelineCallback
orMultiPipelineCallbacks
that is called at the end of each denoising step during the inference. with the following arguments:callback_on_step_end(self: DiffusionPipeline, step: int, timestep: int, callback_kwargs: Dict)
.callback_kwargs
will include a list of all tensors as specified bycallback_on_step_end_tensor_inputs
.[callback_on_step_end_tensor_inputs (](#diffusers.StableDiffusionControlNetInpaintPipeline.__call__.callback_on_step_end_tensor_inputs)list
, optional) — The list of tensor inputs for thecallback_on_step_end
function. The tensors specified in the list will be passed ascallback_kwargs
argument. You will only be able to include variables listed in the._callback_tensor_inputs
attribute of your pipeline class.
Returns
[StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) or tuple
If return_dict
is True
, [StableDiffusionPipelineOutput](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/gligen#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput) is returned,
otherwise a tuple
is returned where the first element is a list with the generated images and the
second element is a list of bool
s indicating whether the corresponding generated image contains
“not-safe-for-work” (nsfw) content.
The call function to the pipeline for generation.
Examples:
>>> # !pip install transformers accelerate
>>> from diffusers import StableDiffusionControlNetInpaintPipeline, ControlNetModel, DDIMScheduler
>>> from diffusers.utils import load_image
>>> import numpy as np
>>> import torch
>>> init_image = load_image(
... "https://huggingface.co/datasets/diffusers/test-arrays/resolve/main/stable_diffusion_inpaint/boy.png"
... )
>>> init_image = init_image.resize((512, 512))
>>> generator = torch.Generator(device="cpu").manual_seed(1)
>>> mask_image = load_image(
... "https://huggingface.co/datasets/diffusers/test-arrays/resolve/main/stable_diffusion_inpaint/boy_mask.png"
... )
>>> mask_image = mask_image.resize((512, 512))
>>> def make_canny_condition(image):
... image = np.array(image)
... image = cv2.Canny(image, 100, 200)
... image = image[:, :, None]
... image = np.concatenate([image, image, image], axis=2)
... image = Image.fromarray(image)
... return image
>>> control_image = make_canny_condition(init_image)
>>> controlnet = ControlNetModel.from_pretrained(
... "lllyasviel/control_v11p_sd15_inpaint", torch_dtype=torch.float16
... )
>>> pipe = StableDiffusionControlNetInpaintPipeline.from_pretrained(
... "stable-diffusion-v1-5/stable-diffusion-v1-5", controlnet=controlnet, torch_dtype=torch.float16
... )
>>> pipe.scheduler = DDIMScheduler.from_config(pipe.scheduler.config)
>>> pipe.enable_model_cpu_offload()
>>> # generate image
>>> image = pipe(
... "a handsome man with ray-ban sunglasses",
... num_inference_steps=20,
... generator=generator,
... eta=1.0,
... image=init_image,
... mask_image=mask_image,
... control_image=control_image,
... ).images[0]
enable_attention_slicing
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/pipeline_utils.py#L2040)
( slice_size: str | int = 'auto' )
Parameters
[slice_size (](#diffusers.StableDiffusionControlNetInpaintPipeline.enable_attention_slicing.slice_size)str
orint
, optional, defaults to"auto"
) — When"auto"
, halves the input to the attention heads, so attention will be computed in two steps. If"max"
, maximum amount of memory will be saved by running only one slice at a time. If a number is provided, uses as many slices asattention_head_dim // slice_size
. In this case,attention_head_dim
must be a multiple ofslice_size
.
Enable sliced attention computation. When this option is enabled, the attention module splits the input tensor in slices to compute attention in several steps. For more than one attention head, the computation is performed sequentially over each head. This is useful to save some memory in exchange for a small speed decrease.
> ⚠️ Don’t enable attention slicing if you’re already using
scaled_dot_product_attention
(SDPA) from PyTorch > 2.0 or xFormers. These attention computations are already very memory efficient so you won’t need to enable > this function. If you enable attention slicing with SDPA or xFormers, it can lead to serious slow downs!
Examples:
>>> import torch
>>> from diffusers import StableDiffusionPipeline
>>> pipe = StableDiffusionPipeline.from_pretrained(
... "stable-diffusion-v1-5/stable-diffusion-v1-5",
... torch_dtype=torch.float16,
... use_safetensors=True,
... )
>>> prompt = "a photo of an astronaut riding a horse on mars"
>>> pipe.enable_attention_slicing()
>>> image = pipe(prompt).images[0]
Disable sliced attention computation. If enable_attention_slicing
was previously called, attention is
computed in one step.
Enable sliced VAE decoding. When this option is enabled, the VAE will split the input tensor in slices to compute decoding in several steps. This is useful to save some memory and allow larger batch sizes.
Disable sliced VAE decoding. If enable_vae_slicing
was previously enabled, this method will go back to
computing decoding in one step.
enable_xformers_memory_efficient_attention
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/pipeline_utils.py#L1985)
( attention_op: typing.Optional[typing.Callable] = None )
Parameters
[attention_op (](#diffusers.StableDiffusionControlNetInpaintPipeline.enable_xformers_memory_efficient_attention.attention_op)Callable
, optional) — Override the defaultNone
operator for use asop
argument to thefunction of xFormers.memory_efficient_attention()
Enable memory efficient attention from [xFormers](https://facebookresearch.github.io/xformers/). When this
option is enabled, you should observe lower GPU memory usage and a potential speed up during inference. Speed
up during training is not guaranteed.
> ⚠️ When memory efficient attention and sliced attention are both enabled, memory efficient attention takes > precedent.
Examples:
>>> import torch
>>> from diffusers import DiffusionPipeline
>>> from xformers.ops import MemoryEfficientAttentionFlashAttentionOp
>>> pipe = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-2-1", torch_dtype=torch.float16)
>>> pipe = pipe.to("cuda")
>>> pipe.enable_xformers_memory_efficient_attention(attention_op=MemoryEfficientAttentionFlashAttentionOp)
>>> # Workaround for not accepting attention shape using VAE for Flash Attention
>>> pipe.vae.enable_xformers_memory_efficient_attention(attention_op=None)
Disable memory efficient attention from [xFormers](https://facebookresearch.github.io/xformers/).
load_textual_inversion
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/loaders/textual_inversion.py#L271)
( pretrained_model_name_or_path: str | list[str] | dict[str, torch.Tensor] | list[dict[str, torch.Tensor]] token: str | list[str] | None = None tokenizer: 'PreTrainedTokenizer' | None = None text_encoder: 'PreTrainedModel' | None = None **kwargs )
Parameters
[pretrained_model_name_or_path (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.pretrained_model_name_or_path)str
oros.PathLike
orlist[str or os.PathLike]
orDict
orlist[Dict]
) — Can be either one of the following or a list of them:- A string, the model id (for example
sd-concepts-library/low-poly-hd-logos-icons
) of a pretrained model hosted on the Hub. - A path to a directory (for example
./my_text_inversion_directory/
) containing the textual inversion weights. - A path to a file (for example
./my_text_inversions.pt
) containing textual inversion weights. - A
[torch state dict](https://pytorch.org/tutorials/beginner/saving_loading_models.html#what-is-a-state-dict).
- A string, the model id (for example
[token (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.token)str
orlist[str]
, optional) — Override the token to use for the textual inversion weights. Ifpretrained_model_name_or_path
is a list, thentoken
must also be a list of equal length.[text_encoder (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.text_encoder)[CLIPTextModel](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTextModel), optional) — Frozen text-encoder ([clip-vit-large-patch14](https://huggingface.co/openai/clip-vit-large-patch14)). If not specified, function will take self.tokenizer.[tokenizer (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.tokenizer)[CLIPTokenizer](https://huggingface.co/docs/transformers/v5.3.0/en/model_doc/clip#transformers.CLIPTokenizer), optional) — ACLIPTokenizer
to tokenize text. If not specified, function will take self.tokenizer.[weight_name (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.weight_name)str
, optional) — Name of a custom weight file. This should be used when:- The saved textual inversion file is in 🤗 Diffusers format, but was saved under a specific weight
name such as
text_inv.bin
. - The saved textual inversion file is in the Automatic1111 format.
- The saved textual inversion file is in 🤗 Diffusers format, but was saved under a specific weight
name such as
[cache_dir (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.cache_dir)str | os.PathLike
, optional) — Path to a directory where a downloaded pretrained model configuration is cached if the standard cache is not used.[force_download (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.force_download)bool
, optional, defaults toFalse
) — Whether or not to force the (re-)download of the model weights and configuration files, overriding the cached versions if they exist.[proxies (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.proxies)dict[str, str]
, optional) — A dictionary of proxy servers to use by protocol or endpoint, for example,{'http': 'foo.bar:3128', 'http://hostname': 'foo.bar:4012'}
. The proxies are used on each request.[local_files_only (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.local_files_only)bool
, optional, defaults toFalse
) — Whether to only load local model weights and configuration files or not. If set toTrue
, the model won’t be downloaded from the Hub.[hf_token (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.hf_token)str
or bool, optional) — The token to use as HTTP bearer authorization for remote files. IfTrue
, the token generated fromdiffusers-cli login
(stored in~/.huggingface
) is used.[revision (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.revision)str
, optional, defaults to"main"
) — The specific model version to use. It can be a branch name, a tag name, a commit id, or any identifier allowed by Git.[subfolder (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.subfolder)str
, optional, defaults to""
) — The subfolder location of a model file within a larger model repository on the Hub or locally.[mirror (](#diffusers.StableDiffusionControlNetInpaintPipeline.load_textual_inversion.mirror)str
, optional) — Mirror source to resolve accessibility issues if you’re downloading a model in China. We do not guarantee the timeliness or safety of the source, and you should refer to the mirror site for more information.
Load Textual Inversion embeddings into the text encoder of [StableDiffusionPipeline](/docs/diffusers/v0.37.1/en/api/pipelines/stable_diffusion/text2img#diffusers.StableDiffusionPipeline) (both 🤗 Diffusers and
Automatic1111 formats are supported).
Example:
To load a Textual Inversion embedding vector in 🤗 Diffusers format:
from diffusers import StableDiffusionPipeline
import torch
model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
pipe.load_textual_inversion("sd-concepts-library/cat-toy")
prompt = "A <cat-toy> backpack"
image = pipe(prompt, num_inference_steps=50).images[0]
image.save("cat-backpack.png")
To load a Textual Inversion embedding vector in Automatic1111 format, make sure to download the vector first
(for example from [civitAI](https://civitai.com/models/3036?modelVersionId=9857)) and then load the vector
locally:
from diffusers import StableDiffusionPipeline
import torch
model_id = "stable-diffusion-v1-5/stable-diffusion-v1-5"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to("cuda")
pipe.load_textual_inversion("./charturnerv2.pt", token="charturnerv2")
prompt = "charturnerv2, multiple views of the same character in the same outfit, a character turnaround of a woman wearing a black jacket and red shirt, best quality, intricate details."
image = pipe(prompt, num_inference_steps=50).images[0]
image.save("character.png")
encode_prompt
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/controlnet/pipeline_controlnet_inpaint.py#L282)
( prompt device num_images_per_prompt do_classifier_free_guidance negative_prompt = None prompt_embeds: torch.Tensor | None = None negative_prompt_embeds: torch.Tensor | None = None lora_scale: float | None = None clip_skip: int | None = None )
Parameters
[prompt (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.prompt)str
orlist[str]
, optional) — prompt to be encoded[device — (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.device)torch.device
): torch device[num_images_per_prompt (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.num_images_per_prompt)int
) — number of images that should be generated per prompt[do_classifier_free_guidance (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.do_classifier_free_guidance)bool
) — whether to use classifier free guidance or not[negative_prompt (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.negative_prompt)str
orlist[str]
, optional) — The prompt or prompts not to guide the image generation. If not defined, one has to passnegative_prompt_embeds
instead. Ignored when not using guidance (i.e., ignored ifguidance_scale
is less than1
).[prompt_embeds (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.prompt_embeds)torch.Tensor
, optional) — Pre-generated text embeddings. Can be used to easily tweak text inputs, e.g. prompt weighting. If not provided, text embeddings will be generated fromprompt
input argument.[negative_prompt_embeds (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.negative_prompt_embeds)torch.Tensor
, optional) — Pre-generated negative text embeddings. Can be used to easily tweak text inputs, e.g. prompt weighting. If not provided, negative_prompt_embeds will be generated fromnegative_prompt
input argument.[lora_scale (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.lora_scale)float
, optional) — A LoRA scale that will be applied to all LoRA layers of the text encoder if LoRA layers are loaded.[clip_skip (](#diffusers.StableDiffusionControlNetInpaintPipeline.encode_prompt.clip_skip)int
, optional) — Number of layers to be skipped from CLIP while computing the prompt embeddings. A value of 1 means that the output of the pre-final layer will be used for computing the prompt embeddings.
Encodes the prompt into text encoder hidden states.
StableDiffusionPipelineOutput
class diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput
[< source >](https://github.com/huggingface/diffusers/blob/v0.37.1/src/diffusers/pipelines/stable_diffusion/pipeline_output.py#L10)
( images: list[PIL.Image.Image] | numpy.ndarray nsfw_content_detected: list[bool] | None )
Parameters
[images (](#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput.images)list[PIL.Image.Image]
ornp.ndarray
) — list of denoised PIL images of lengthbatch_size
or NumPy array of shape(batch_size, height, width, num_channels)
.[nsfw_content_detected (](#diffusers.pipelines.stable_diffusion.StableDiffusionPipelineOutput.nsfw_content_detected)list[bool]
) — list indicating whether the corresponding generated image contains “not-safe-for-work” (nsfw) content orNone
if safety checking could not be performed.
Output class for Stable Diffusion pipelines.
[Update on GitHub](https://github.com/huggingface/diffusers/blob/main/docs/source/en/api/pipelines/controlnet.md)