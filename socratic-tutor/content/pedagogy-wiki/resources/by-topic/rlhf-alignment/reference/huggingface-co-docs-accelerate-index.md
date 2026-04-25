# Source: https://huggingface.co/docs/accelerate/index
# Author: Hugging Face
# Author Slug: hugging-face
# Title: Hugging Face Accelerate Documentation
# Fetched via: search
# Date: 2026-04-09

# An Introduction to HuggingFace's Accelerate Library

In this article, we dive into the internal workings of the Accelerate library from HuggingFace, to answer "could Accelerate really be this easy?"

Comment

As someone who first spent around a day implementing Distributed Data Parallel (DDP) in PyTorch and then spent around 5 mins doing the same thing using HuggingFace's new Accelerate library, I was intrigued and amazed by the simplicity of the package.
"Could it really be this easy?" I asked myself, and we discuss the result in this article.

Accelerate: GitHub | Docs | Commit ID at the time of writing this post

As part of this article, we will be looking at the source code of HuggingFace Accelerate, but at times, I will skip some parts of the code for simplicity. Also, we will not be looking at TPU-related code and only focus on how HuggingFace Accelerate works for single and multi-GPU environments.
Please note that this post is not an introduction to Distributed Data Parallel (DDP). For an introduction to DDP, please refer to the following wonderful resources:

- PyTorch Distributed Training by Lei Mao

- Distributed data-parallel training in PyTorch by Kevin Kaichuang Yang

Here's an overview of what we'll cover in this article:

### Table of Contents

Distributed Data Parallel in PyTorch Introduction to HuggingFace AccelerateInside HuggingFace AccelerateStep 1: Initializing the AcceleratorStep 2: Getting objects ready for DDP using the Accelerator Conclusion

So, let's get started!

…

- Initialize a process group using torch.distributed package: dist.init_process_group(backend="nccl")

- Take care of variables such as local_world_size and local_rank to handle correct device placement based on the process index.

- Add a sampler of type torch.utils.data.distributed.DistributedSampler to the DataLoader such that the batch get's split appropriately and only a subset of it is passed to the GPUs based on the local_rank of the process.
- Wrap the model inside DistributedDataParallel class passing in the device_ids such that a replica of the model can be created on each of the GPUs.

And more! This process is error-prone and time-consuming, especially if you're doing it for the first time.

Enter HuggingFace Accelerate to the rescue!

## Introduction to HuggingFace Accelerate

Please note that this is not an official example. For that, please refer to the docs here.

We just lost around 50 lines of boilerplate code thanks to HuggingFace Accelerate and Sylvain Gugger. And the same script can now work on a single GPU, multi-GPUs, and TPUs!
I personally haven't tried working with TPUs but just being able to use the same script when training on single & multi GPUs is enough for me. ;)

Basically, all we need to do now to implement training on multi-GPUs is the following:

from accelerate import Acceleratoraccelerator = Accelerator()# dummy code to get dataloaders, model & optimizertrain_dataloader, eval_dataloader, model, optimizer = get_everything()# prepare for DDP using acceleratortrain_dataloader, eval_dataloader, model, optimizer = accelerator.prepare(train_dataloader, eval_dataloader, model, optimizer)
And that's pretty much it! Just passing our object's dataloaders, model, and optimizer through accelerator.prepare can get them ready for us. But how can these two lines of code be enough to look after everything?

That's the exact same question I asked myself. Below, let's shed some light on the internal mechanisms of HuggingFace Accelerate and try to answer this question.

## Inside HuggingFace Accelerate

Before we start digging into the source code, let's keep in mind that there are two key steps to using HuggingFace Accelerate:

- Initialize Accelerator: accelerator = Accelerator()

- Prepare the objects such as dataloader, optimizer & model: train_dataloader, model, optimizer = accelerator.prepare(train_dataloader, model, optimizer)

We are going to understand what goes on in each of these two key steps next.

Please note that from this point on, this article becomes code heavy as we start looking into the source code step-by-step.

## Step 1: Initializing the Accelerator

Every time we initialize an Accelerator, accelerator = Accelerator(), the first thing that happens is that the Accelerator's state is set to be an instance of AcceleratorState class. From the source code:
class Accelerator:def __init__(self,device_placement: bool = True,split_batches: bool = False,fp16: bool = None,cpu: bool = False,rng_types: Optional[List[Union[str, RNGType]]] = None,kwargs_handlers: Optional[List[KwargsHandler]] = None,):# initialize stateself.state = AcceleratorState(fp16=fp16, cpu=cpu, _from_accelerator=True)

We pass in a bunch of variables - fp16, cpu & from_accelerator and that's it. That's how the self.state is set for each Accelerator.

#### What is this AcceleratorState class?

You can find this class's source code here, but essentially all it does is set the appropriate value for the following variables depending on which type of hardware is available:

- distributed_type

- num_processes

- process_index

- local_process_index

- use_fp16

The shorter version of the __init__ method of the AcceleratorState looks something like:
class AcceleratorState:_shared_state = {}def __init__(self, fp16: bool = None, cpu: bool = False, _from_accelerator: bool = False):self.__dict__ = self._shared_stateif not getattr(self, "initialized", False):if is_tpu_available() and not cpu:# setup all TPU related variableselif int(os.environ.get("LOCAL_RANK", -1)) != -1 and not cpu:# setup all MULTI-GPU related variableselse:# setup single GPU or CPU related variables depending on whether CUDA is availableself.initialized = True
Can you see now what I meant by saying that AcceleratorState sets a particular value for the variables based on the hardware?"

#### How does AcceleratorState know which hardware is available?

Well, that's just a bunch of if-else conditions in the __init__ method that we saw above:

if is_tpu_available() and not cpu:# setup variables for TPUelif int(os.environ.get("LOCAL_RANK", -1)) != -1 and not cpu:# setup variables for MULTI_GPUelse:# setup variables for SINGLE_GPU or CPU depending on whether CUDA is available

#### How does AcceleratorState set the variables depending on hardware?

Taking a single node with multiple GPUs as an example, in that case, the __init__ method for AcceleratorState looks like this:

…

= -1 and not cpu:self.distributed_type = DistributedType.MULTI_GPUif not torch.distributed.is_initialized():torch.distributed.init_process_group(backend="nccl")self.num_processes = torch.distributed.get_world_size()self.process_index = torch.distributed.get_rank()self.local_process_index = int

…

Having a look at the source code above, we can see that self.distributed_type gets set to DistributedType.MULTI_GPU which is nothing but a type that has string value 'MULTI_GPU'.

So, in essence, self.distributed_type is set to a string value of 'MULTI_GPU'.

Next, we initialize the distributed processes as we did in our PyTorch DDP script with 'nccl' backend. This is pretty standard, as we do need to initialize a process group before starting out with distributed training.
Next, in the code, we can see that we get the number of processes from the process group itself and also the process_index for each of our individual processes. Note that the process_index is going to be different for each process. Same for the local_process_index.

The only time when local_process_index and process_index are going to be different is when we are training using multiple-nodes. That is, training on multiple machines with multiple GPUs. This has also been explained further on the PyTorch forums here.

…

## Step 2: Getting objects ready for DDP using the Accelerator

### HuggingFace Accelerate - prepare_model

From the four steps I shared in the DDP in PyTorch section, all we need to do is pretty much wrap the model in DistributedDataParallel class from PyTorch, passing in the device IDs - right?

…

And there it is! That's exactly what we are doing inside the prepare_model method. Since device_placement is set to True by default, first, we move the model to self.device.

Note that each process has its own device.

Next, we wrap the model inside DistributedDataParallel class, passing in a list of device IDs which is the local_process_index that's separate for each process again! So, we have been able to achieve the same result as our pure PyTorch script, while at the same abstracting away all the complexity from the users. This is neat!

…

### HuggingFace Accelerate -> Prepare DataLoaders

The prepare_dataloaders method is a bit more complex and it is responsible for breaking the dataset into subsets based on the process_index inside the process group, making sure that each GPU only ever gets a subset of the data.

HuggingFace Accelerate achieves this by updating the data sampler inside the given DataLoader and updating the sampler to be an instance of type BatchSamplerShard. Also, the DataLoader itself gets wrapped inside DataLoaderShard.
Essentially, we grab some key information from the existing DataLoader:

new_dataset = dataloader.datasetnew_batch_sampler = dataloader.batch_samplergenerator = getattr(dataloader, "generator", None)new_batch_sampler = BatchSamplerShard(dataloader.batch_sampler,num_processes=num_processes,process_index=process_index,split_batches=split_batches,)

First, we grab the dataset, existing batch sampler, and generator if it exists from our given PyTorch DataLoader. Next, we create a new batch sampler which is an instance of `BatchSamplerShard class. Let's look at this class in detail next.

### BatchSamplerShard

The BatchSamplerShard class is responsible for breaking the dataset into subsets based on the process_index and making sure that the appropriate subsets of the data get sent to the correct device. Let's look at the high-level source code of this class.

…

= num_processesself.process_index = process_indexself.split_batches = split_batchesself.batch_size = batch_sampler.batch_sizeself.drop_last = batch_sampler.drop_lastdef __len__(self):if len(self.batch_sampler) % self.num_processes == 0:return len(self.batch_sampler) // self.num_processeslength = len(self.batch_sampler) // self.num_processesreturn length if self.drop_last else length + 1def __iter__(self):return self._iter_with_split() if self.split_batches else self._iter_with_no_split()
Okay, great, so this class accepts some variables like batch_sampler, num_processes, process_index, split_batches, batch_size & drop_last. Note that the process_index and num_processes values are coming from the accelerator's prepare method itself.

So then, what's the main idea?

Well, we want the data to be split into subsets based on the process_index and make sure that the subsets are different and don't overlap.

#### How is this achieved inside the BatchSamplerShard class?

The BatchSamplerShard class has an __iter__ method that yields the correct batches based on the process_index.

Let's assume we are going with split_batches = False. In this case, the self._iter_with_no_split method gets called. So, let's look at the source code of this method.
Starting with the first part of this method:

def _iter_with_no_split(self):initial_data = []batch_to_yield = []for idx, batch in enumerate(self.batch_sampler):# We gather the initial indices in case we need to circle back at the end.if not self.drop_last and idx < self.num_processes:initial_data += batch# We identify

…

Let's try and grasp the main idea of this method by looking at the above source code. We already know that self.batch_sampler has been set to existing DataLoader's batch_sampler, so by iterating over it, we get our batch.

BUT! Since we need to split the data into parts based on the process_index, that means that we can't send this whole data out, as otherwise, all our GPUs would be getting the complete dataset.
To do that, first, we add some data indices to initial_data list. This is in case we need to circle back and add more data later on.

Next, based on the process_index, we can identify the batch we want to yield as in the code:

if idx % self.num_processes == self.process_index:batch_to_yield = batch
Assuming we have 2 num_processes, then for process_index==0, going by our example, this just returns [0, 1, 2, 3], and for process_index==1, this returns [4, 5, 6, 7].

So, that's it! We have successfully sharded our batch into subsets based on the process_index. Isn't this cool?

…

I leave it as an exercise to the reader to understand this function but it's really straightforward and clean!

## Conclusion

That's really most of it! This article does not explain the entirety of HuggingFace Accelerate, but I hope I have been able to shed some light on how it works and how it's structured.

I have already started using the package for my internal workflows, and it's been really easy to use! Also, please note that this article is based on my understanding of the package, and the official documentation by HuggingFace would be a better place to learn more about the package.

- 1. What is Hugging Face Accelerate?
- 2. Key Features and Capabilities
- 2.1 Minimal Code Changes Required
- 2.2 Distributed Training Strategies
- 2.3 Mixed Precision Support
- 3. Getting Started with Accelerate
- 3.1 Installation and Setup
- 3.2 Basic Usage Pattern
- 4. ND-Parallel Multi-GPU Training
- 4.1 Data Parallelism (DP)
- 4.2 Fully Sharded Data Parallel (FSDP)
- 4.3 Tensor Parallelism (TP)
- 5. The Accelerator Class
- 5.1 Initialization and Configuration
- 5.2 Model and Data Preparation
- 6. Advanced Features and Integrations
- 6.1 Big Model Inference
- 6.2 Notebook Launcher
- 6.3 Experiment Tracking
- 7. Best Practices and Optimization Tips

…

## What is Hugging Face Accelerate?

Hugging Face Accelerate is a lightweight PyTorch library designed to make distributed training and inference accessible to everyone. It acts as a thin wrapper around PyTorch that enables you to run the same training code across various hardware configurations—from a single CPU to multiple GPUs or TPUs—without major code modifications.

The library was created to bridge the gap between native PyTorch distributed training (which requires significant boilerplate code) and high-level frameworks that abstract away too much control. Accelerate gives you the simplicity of automatic device management while preserving full control over your training loop, making it ideal for researchers and practitioners who need flexibility.
Unlike traditional distributed training approaches that require extensive knowledge of distributed systems, Accelerate automates the complex parts while keeping your PyTorch code recognizable. You maintain the same training logic you're familiar with, and Accelerate handles device placement, gradient synchronization, and distributed communication behind the scenes.
The library supports a wide range of training configurations including single-node multi-GPU, multi-node distributed training, mixed precision training (fp8, fp16, bf16), and integration with popular frameworks like DeepSpeed and Fully Sharded Data Parallel (FSDP). This versatility makes it suitable for training everything from small models on a single GPU to massive language models across hundreds of GPUs.

## Key Features and Capabilities

Hugging Face Accelerate provides a comprehensive set of features that simplify distributed training while maintaining performance and flexibility. The library is built around three core principles: minimal code changes, maximum compatibility, and unified interfaces for different distributed strategies.

### Minimal Code Changes Required

One of Accelerate's most compelling features is that it requires only 4-5 lines of code to transform a standard PyTorch training script into a distributed training program. The typical pattern involves initializing an Accelerator object, preparing your model and data loaders through the accelerator, and replacing standard backward passes with accelerator-managed versions.

This minimal intervention approach means you can take existing PyTorch code and make it distributed-ready in minutes rather than hours. The library automatically detects your hardware configuration and applies the appropriate optimizations, whether you're running on a laptop with a single GPU or a cluster with hundreds of nodes.
The code remains readable and maintainable because Accelerate doesn't force you to adopt a new training paradigm. Your training loop structure stays intact, making it easy to debug, modify, and understand what's happening at each step.

### Distributed Training Strategies

Accelerate provides unified interfaces for multiple distributed training strategies, allowing you to switch between them with configuration changes rather than code rewrites. The library supports Data Parallelism (DP), Distributed Data Parallel (DDP), Fully Sharded Data Parallel (FSDP), and DeepSpeed integration.

Data Parallelism replicates your model across multiple devices, with each device processing a different batch of data. This is the simplest form of distributed training and works well for models that fit comfortably in GPU memory. Accelerate handles the gradient aggregation and parameter synchronization automatically.
For larger models, Accelerate offers FSDP support, which shards model parameters, gradients, and optimizer states across devices. This dramatically reduces memory requirements per device, enabling training of models that would otherwise be impossible. The FSDP implementation is configurable through Accelerate's ParallelismConfig, allowing fine-grained control over sharding strategies.
DeepSpeed integration provides access to advanced optimization techniques like ZeRO (Zero Redundancy Optimizer) stages, gradient accumulation, and efficient mixed precision training. Accelerate makes DeepSpeed accessible through simple configuration files, eliminating the need to understand DeepSpeed's complex API directly.

### Mixed Precision Support

Accelerate includes comprehensive support for mixed precision training, which can significantly accelerate training and reduce memory consumption. The library supports multiple precision formats including fp16 (half precision), bf16 (brain float 16), and the newer fp8 (8-bit floating point) format.

Mixed precision works by performing most operations in lower precision while maintaining critical operations in full precision to preserve numerical stability. Accelerate handles the complexity of managing different precision levels automatically, including gradient scaling to prevent underflow and selective operation casting.
The fp8 support is particularly noteworthy, as it can provide up to 2x speedup over fp16 on supported hardware while maintaining model accuracy. Accelerate integrates with TransformerEngine for MXFP8 block scaling, enabling efficient fp8 training for transformer-based models. Recent updates have expanded fp8 support with use_mxfp8_block_scaling configuration options.
Hardware compatibility is automatically detected, with Accelerate falling back to appropriate precision levels based on your GPU capabilities. This ensures your code runs optimally regardless of whether you're using older GPUs that only support fp16 or cutting-edge hardware with fp8 tensor cores.

## Getting Started with Accelerate

Getting started with Hugging Face Accelerate is straightforward, requiring only a few steps to transform your existing PyTorch code into a distributed training setup. The library is designed to be beginner-friendly while offering advanced features for experienced practitioners.

…

. The library has minimal dependencies and integrates seamlessly with existing PyTorch installations. For specific hardware configurations or advanced features, you may need additional dependencies like DeepSpeed or Intel Extension for PyTorch.
After installation, you should run

…

to generate a configuration file that specifies your hardware setup and training preferences. This interactive command-line tool asks questions about your environment—number of GPUs, whether you want to use DeepSpeed or FSDP, mixed precision preferences, and more.
The configuration is saved to a YAML file that Accelerate uses to automatically set up your distributed training environment. You can have multiple configuration files for different scenarios (single GPU development, multi-GPU training, cluster deployment) and switch between them as needed.
For quick prototyping or notebooks, you can skip the configuration step and let Accelerate automatically detect your setup, though explicit configuration is recommended for production training runs.

### Basic Usage Pattern

The basic Accelerate pattern involves four key steps: initialize the Accelerator, prepare your model and data loaders, modify the training loop, and handle distributed-specific operations. Here's the typical workflow:

First, create an Accelerator instance at the beginning of your script. This object serves as the central controller for all distributed operations. Then, pass your model, optimizer, and data loaders to

…

, which wraps them with distributed-aware versions.
In your training loop, replace

…

instead of regular print statements to avoid duplicate output from multiple processes.
For model saving and checkpointing, Accelerate provides utilities like

…

to ensure synchronized operations across all processes. The library handles the complexity of determining which process should save checkpoints and when to synchronize.
The official documentation at huggingface.co/docs/accelerate provides detailed tutorials with code examples for common scenarios, making it easy to adapt the patterns to your specific use case.

…

## The Accelerator Class

The Accelerator class is the heart of the Hugging Face Accelerate library, serving as the main entry point for all distributed training operations. Understanding how to use this class effectively is key to leveraging Accelerate's full capabilities.

### Initialization and Configuration

When you instantiate an Accelerator object, it automatically detects your distributed training setup and initializes all necessary components. The detection process examines environment variables, available hardware, and your configuration file to determine the appropriate backend and training strategy.

You can override automatic detection by passing specific arguments to the Accelerator constructor. Common parameters include mixed_precision (to specify fp16, bf16, or fp8), gradient_accumulation_steps (for handling larger effective batch sizes), and log_with (to specify experiment tracking backends like TensorBoard or Weights & Biases).
The Accelerator also provides utility methods for querying the distributed environment, such as accelerator.num_processes (total number of processes), accelerator.process_index (current process ID), and accelerator.is_main_process (whether this is the primary process for logging and saving).

Recent updates have added support for Intel XPUs through automatic device detection, and SwanLab has been added as a supported experiment tracking backend. The Accelerator seamlessly handles these different platforms through the same unified API.

…

method is where Accelerate performs its magic, transforming regular PyTorch objects into distributed-aware versions. You pass your model, optimizer, data loaders, and optionally learning rate schedulers to this method, and it returns wrapped versions that handle all distributed operations automatically.
During preparation, Accelerate moves your model to the appropriate device(s), wraps it with the configured distributed backend (DDP, FSDP, etc.), enables mixed precision if requested, and modifies data loaders to ensure each process receives different data batches.
The wrapped model behaves like a regular PyTorch model from your code's perspective—you call forward passes, backward passes, and optimizer steps exactly as before. But behind the scenes, Accelerate is managing device placement, gradient synchronization, and distributed communication.

One important detail is that prepare() should be called after defining your model and optimizer but before starting training. The method handles initialization order dependencies automatically, ensuring everything is set up correctly regardless of which distributed strategy you're using.

## Advanced Features and Integrations

Beyond basic distributed training, Accelerate includes several advanced features that address common challenges in large-scale machine learning.

### Big Model Inference

Big Model Inference is a feature designed to make loading and running inference with extremely large models more accessible. Many state-of-the-art models are too large to fit in the memory of a single GPU, making inference challenging.

Accelerate's Big Model Inference capabilities include model sharding across multiple GPUs, offloading to CPU or disk when necessary, and efficient memory management during inference. The library can automatically determine an optimal sharding strategy based on available hardware and model architecture.
This feature is particularly valuable for running inference with models like large language models that may have hundreds of billions of parameters. Accelerate handles the complexity of coordinating inference across sharded model components while presenting a simple interface to the user.

…

for recording metrics, which automatically handles distributed logging (ensuring metrics are only logged from the main process to avoid duplicates).
This integration means you don't need to add platform-specific logging code throughout your training script. Accelerate abstracts the differences between tracking platforms, allowing you to switch between them by changing a single configuration parameter.

…

## Accelerate vs Other Frameworks

Hugging Face Accelerate occupies a unique position in the distributed training landscape, offering a different trade-off than both low-level PyTorch distributed primitives and high-level frameworks like PyTorch Lightning or Hugging Face Transformers Trainer.

Compared to native PyTorch distributed training (using DDP, FSDP, or torch.distributed directly), Accelerate provides significant boilerplate reduction. Native PyTorch requires manual process group initialization, explicit device placement, careful handling of distributed-specific code paths, and custom checkpoint management. Accelerate handles all of this automatically while maintaining the same level of control over the training loop.

…

to synchronize all processes before or after saving operations, ensuring consistency across the distributed setup.
Accelerate supports a wide range of hardware including NVIDIA GPUs (with CUDA), AMD GPUs (with ROCm), Intel XPUs, Google TPUs, Apple Silicon (MPS), and CPUs for training and inference. Recent updates have expanded Intel XPU support significantly. The library automatically detects available hardware and configures appropriate backends. Mixed precision support varies by hardware—fp16 is widely supported, bf16 requires recent GPUs, and fp8 requires cutting-edge hardware like NVIDIA H100 GPUs with Hopper architecture.
Accelerate introduces minimal performance overhead because it's a thin wrapper around PyTorch's native distributed primitives. The library doesn't add abstraction layers that slow down computation—it primarily handles setup, device management, and coordination. In most cases, training with Accelerate is as fast as using PyTorch distributed training directly. The main performance consideration is choosing the right distributed strategy and mixed precision settings for your hardware, which Accelerate makes easier through its configuration system.

huggingface / **
...
```
accelerator = Accelerator(log_with="trackio")
config={"learning_rate": 0.001, "batch_size": 32}
# init_kwargs in order to host the dashboard on spaces
init_kwargs = {"trackio": {"space_id": "hf_username/space_name"}
accelerator.init_trackers("example_project", config=config, init_kwargs=init_kwargs})

Disclaimer: This post has been translated to English using a machine translation model.
...
`Accelerate` is a Hugging Face library that allows running the same PyTorch code in any distributed setup by adding only four lines of code.
## Installation
To install
`accelerate` with
`pip`, simply run:
`pip install accelerate`
And with
`conda`:
`conda install -c conda-forge accelerate`
## Configuration
In each environment where
`accelerate` is installed, the first thing to do is to configure it.
To do this, run in a terminal:
``accelerate config``
!accelerate configCopied
--------------------------------------------------------------------------------In which compute environment are you running?This machine--------------------------------------------------------------------------------multi-GPUHow many different machines will you use (use more than 1 for multi-node training)?
...
In most of the
`accelerate` documentation, it is explained how to use
`accelerate` with scripts, so for now we will do it this way and at the end we will explain how to do it with a notebook.
First, we are going to create a folder where we will save the scripts
!mkdir accelerate_scriptsCopied
Now we write the base code in a script
%%writefile accelerate_scripts/01_code_base.py import torchfrom torch.utils.data import DataLoaderfrom torch.optim import Adamfrom datasets import load_datasetfrom transformers import AutoTokenizer, AutoModelForSequenceClassificationimport evaluatefrom fastprogress.fastprogress import master_bar, progress_bar dataset = load_dataset("tweet_eval", "emoji")
…
Overwriting accelerate_scripts/01_code_base.py
And now we run it
%%time !python accelerate_scripts/01_code_base.pyCopied
...
#### Code with accelerate
Now we replace some things
- First, we import
`Accelerator`and initialize it
`from accelerate import Accelerator`
accelerator = Accelerator()
- We don't do the typical anymore
``` python
torch.device("cuda" if torch.cuda.is_available() else "cpu")
```
- But we let
`accelerate`choose the device.
`device = accelerator.device`
- We pass the relevant elements for training through the
`prepare`method and no longer do
`model.to(device)`
`model, optimizer, dataloader["train"], dataloader["validation"] = prepare(model, optimizer, dataloader["train"], dataloader["validation"])`
- We no longer send the data and model to the GPU with
`.to(device)`since
`accelerate`has taken care of it with the
`prepare`method.
- Instead of performing backpropagation with
`loss.backward()`, we let
`accelerate`handle it with
`accelerator.backward(loss)`
…
%%writefile accelerate_scripts/02_accelerate_base_code.py import torchfrom torch.utils.data import DataLoaderfrom torch.optim import Adamfrom datasets import load_datasetfrom transformers import AutoTokenizer, AutoModelForSequenceClassificationimport evaluatefrom fastprogress.fastprogress import master_bar, progress_bar # Importamos e inicializamos Acceleratorfrom
accelerate import Acceleratoraccelerator = Accelerator() dataset = load_dataset("tweet_eval", "emoji")num_classes = len(dataset["train"].info.features["label"].names)max_len = 130 checkpoints = "cardiffnlp/twitter-roberta-base-irony"tokenizer = AutoTokenizer.from_pretrained(checkpoints
…
))for i in master_progress_bar: model.train() progress_bar_train = progress_bar(dataloader["train"], parent=master_progress_bar) for batch in progress_bar_train: optimizer.zero_grad() input_ids = batch["input_ids"]#.to(device) attention_mask = batch["attention_mask"]#.to(device) labels
= batch["label"]#.to(device) outputs = model(input_ids=input_ids, attention_mask=attention_mask) loss = loss_function(outputs['logits'], labels) master_progress_bar.child.comment = f'loss: {loss}' # loss.backward() accelerator.backward(loss) optimizer.step() print(f"End of training
…
Overwriting accelerate_scripts/02_accelerate_base_code.py
...
Now let's run it.
To execute the
`accelerate` scripts, use the command
`accelerate launch`
`accelerate launch script.py`
%%time !accelerate launch accelerate_scripts/02_accelerate_base_code.pyCopied

huggingface / **
accelerate ** Public
...
Below are a variety of utility functions that 🤗 Accelerate provides, broken down by use-case.