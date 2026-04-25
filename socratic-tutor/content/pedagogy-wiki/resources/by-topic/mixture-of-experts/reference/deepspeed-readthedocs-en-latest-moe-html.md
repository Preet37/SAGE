# Source: https://deepspeed.readthedocs.io/en/latest/moe.html
# Title: Mixture of Experts (MoE)
# Fetched via: search
# Date: 2026-04-09

# Mixture of Experts (MoE)
## Layer specification
*class*deepspeed.moe.layer.MoE( *hidden_size: int*, *expert: Module*, *num_experts: int = 1*, *ep_size: int = 1*, *k: int = 1*, *capacity_factor: float = 1.0*, *eval_capacity_factor
: float = 1.0*, *min_capacity: int = 4*, *use_residual: bool = False*, *noisy_gate_policy: Optional[str] = None*, *drop_tokens: bool = True*, *use_rts: bool = True*, *use_tutel: bool = False*, *enable_expert_tensor_parallelism: bool = False*, *top2_2nd_expert_sampling: bool = True*)
Initialize an MoE layer.
- Parameters
**hidden_size**( *int*) – the hidden dimension of the model, importantly this is also the input and output dimension.
**expert**( *nn.Module*) – the torch module that defines the expert (e.g., MLP, torch.linear).
**num_experts**( *int* *,* *
optional*) – default=1, the total number of experts per layer.
**ep_size**( *int* *,* *optional*) – default=1, number of ranks in the expert parallel world or group.
**k**( *int* *,* *optional*) – default=1, top-k gating
value, only supports k=1 or k=2.
**capacity_factor**( *float* *,* *optional*) – default=1.0, the capacity of the expert at training time.
**eval_capacity_factor**( *float* *,* *optional*) – default=1.0, the capacity
of the expert at eval time.
**min_capacity**( *int* *,* *optional*) – default=4, the minimum capacity per expert regardless of the capacity_factor.
**use_residual**( *bool* *,* *optional*) – default=False, make this MoE layer a Residual MoE
() layer.
**noisy_gate_policy**( *str* *,* *optional*) – default=None, noisy gate policy, valid options are ‘Jitter’, ‘RSample’ or ‘None’.
**drop_tokens**( *bool* *,* *optional*) – default=True, whether to drop tokens - (
setting to False is equivalent to infinite capacity).
**use_rts**( *bool* *,* *optional*) – default=True, whether to use Random Token Selection.
**use_tutel**( *bool* *,* *optional*) – default=False, whether to use Tutel optimizations (if installed).
**enable_expert_tensor_parallelism**( *bool* *,* *optional*) – default=False, whether to use tensor parallelism for experts **top2_2nd_expert_sampling**( *bool* *,* *optional*) – default=True, whether to perform sampling for 2nd expert
Initialize internal Module state, shared by both nn.Module and ScriptModule.
forward(
*hidden_states: Tensor*, *used_token: Optional[Tensor] = None*) Tuple[Tensor, Tensor, Tensor]
MoE forward
- Parameters
**hidden_states**( *Tensor*) – input to the layer **used_token**( *Tensor* *,* *optional*) – default: None, mask only used tokens
- Returns
A tuple including output, gate loss, and expert count.
output (Tensor): output of the model
l_aux (Tensor): gate loss value
exp_counts (Tensor): expert count

DeepSpeed-MoE Inference introduces several important features on top of the inference optimization for dense models (DeepSpeed-Inference blog post). It embraces several different types of parallelism, i.e. data-parallelism and tensor-slicing for the non-expert parameters and expert-parallelism and expert-slicing for the expert parameters.
To maximize the aggregate memory-bandwidth, we provide the communication scheduling with parallelism coordination to effectively group and route tokens with the same critical-data-path. Moreover, we propose new modeling optimizations, PR-MoE and MoS, to reduce MoE model size while maintaining accuracy. For more information on the DeepSpeed MoE inference optimization, please refer to our blog post.
DeepSpeed provides a seamless inference mode for the variant of MoE models that are trained via the DeepSpeed-MoE library (MoE tutorial). To do so, one needs to simply use the deepspeed-inference engine to initialize the model to run the model in the eval mode.

## MoE Inference Performance

In modern production environments, powerful DL models are often served using hundreds of GPU devices to meet the traffic demand and deliver low latency. It is important to explore how these two broad goals of high throughput and low latency can be realized for MoE model inference at scale.
For dense models, throughput can be increased by using multiple GPUs and data parallelism (independent replicas with no inter-GPU communication), whereas lower latency can be achieved by techniques like tensor-slicing to partition the model across multiple GPUs. The best case scaling in terms of total throughput is linear with respect to the increasing number of GPUs, i.e., a constant throughput per GPU.
This is possible for pure data parallel inference scenarios as there is no communication between GPUs. To reduce latency, tensor-slicing style of model parallelism has proven to be beneficial but it comes with the cost - communication overhead between GPUs - which often lowers per GPU throughput and results in sublinear scaling of total throughput. In other words, for dense models, we cannot leverage parallelism to optimize both latency and throughput at the same time; there is a tradeoff between them. MoE inference, however, provides unique opportunities to offer optimized latency and throughput simultaneously while scaling to a large number of devices.
Figure below shows how we achieve both low latency and super-linear throughput increase simultaneously. We discuss this at length in our paper.

## End-to-End MoE Inference Example

In this part, we elaborate the usage of MoE inference support in the DeepSpeed library using an end-to-end example.

### Initializing for Inference

For inference with DeepSpeed-MoE, use `init_inference` API to load the DeepSpeed MoE model for inference. Here, you can specify the model-parallelism/tensor-slicing degree (mp_size), expert parallelism degree (ep_size), and number of experts (moe_experts).
We create various process groups based on minimum of the world_size (total number of GPUs) and expert parallel size. By using this group, we can partition the experts among expert-parallel GPUs. If number of experts is lower than total number of GPUs, DeepSpeed-MoE leverages expert-slicing for partitioning the expert parameters between the expert-parallel GPUs.
Furthermore, if the model has not been loaded with the appropriate checkpoint, you can also provide the checkpoint description using a `json` file or simply pass the `'checkpoint'` path to load the model. To inject the high-performance inference kernels, you can set `replace_with_kernel_inject` to True.
```

import deepspeed
import torch.distributed as dist

# Set expert-parallel size
world_size = dist.get_world_size()
expert_parallel_size = min(world_size, args.num_experts)

# create the MoE model
moe_model = get_model(model, ep_size=expert_parallel_size)
...

# Initialize the DeepSpeed-Inference engine
ds_engine = deepspeed.init_inference(moe_model,
mp_size=tensor_slicing_size,
dtype=torch.half,
moe_experts=args.num_experts,
checkpoint=args.checkpoint_path,
replace_with_kernel_inject=True,)
model = ds_engine.module
output = model('Input String')

```

### Various configuration options

Here, we show a text-generation example using an MoE model for which we can specify the model-parallel size and number of experts.
DeepSpeed inference-engine takes care of creating the different parallelism groups using the tensor-slicing degree, number of experts, and the total number of GPUs used for running the MoE model. Regarding the expert parameters, we first use the expert-parallelism to assign each group of experts to one GPU. If number of GPUs is higher than number of experts, we use expert-slicing to partition each expert vertically/horizontally across the GPUs.
Let’s take a look at some of the parameters passed to run our example. Please refer to DeepSpeed-Example for a complete generate-text inference example.
```
generate_samples_gpt.py \
--tensor-model-parallel-size 1 \
--num-experts ${experts} \
--num-layers 24 \
--hidden-size 2048 \
--num-attention-heads 32 \
--max-position-embeddings 1024 \
--tokenizer-type GPT2BPETokenizer \
--load $checkpoint_path \
--fp16 \
--ds-inference \

```

### Performance for standard MoE model

In order to show the performance scaling of DeepSpeed-MoE inference with increasing number of GPUs, we consider a 52B model architecture with 128 experts and 1.3B dense model using the parameters shown in the script above. In this example, we set tensor-slicing degree to one since the non-expert part of the model is relatively small (805M parameters). We use the last flag, `ds-inference`, to switch between DeepSpeed-MoE and PyTorch implementations.
For DeepSpeed-MoE inference, we show our results in this tutorial using two versions: 1) Generic, the current open source version of the DeepSpeed library that includes support for flexible parallelism and PR-MoE model optimization, and 2) Specialized, the most optimized version of DeepSpeed MoE inference system including special computation and communication kernels that will be released later. As mentioned in our blog post, MoE inference optimizations will be released in a staged fashion.
Figure below shows the inference performance of three different configuration, PyTorch, DeepSpeed-MoE (Generic), and DeepSpeed-MoE (Specialized), running on 8, 16, and 32 GPUs. Compared to PyTorch, DeepSpeed-MoE obtains significantly higher performance benefit as we increased the number of GPUs.
By using the generic DeepSpeed-MoE inference, we can get between 24% to 60% performance improvement over PyTorch. Additionally, by enabling the full features of DeepSpeed-MoE inference, such as communication optimization and MoE customized kernels, the performance speedup gets boosted (2x – 3.2x).

### Faster Performance and Lower Inference Cost using PR-MoE optimizations

To select between different MoE structures, we add a new parameter in our inference example, called `mlp-type`, to select between the `'standard'` MoE structure and the `'residual'` one to enable the modeling optimizations offered by PR-MoE. In addition to changing the `mlp-type`, we need to pass the number of experts differently when using PR-MoE.
In contrast to standard MoE which uses the same number of experts for each MoE layer, PR-MoE uses different expert-count for the initial layers than the deeper layers of the network. Below is an example of PR-MoE using a mixture of 64 and 128 experts for every other layers:
```
experts="64 64 64 64 64 64 64 64 64 64 128 128"
generate_samples_gpt.py \
--tensor-model-parallel-size 1 \
--num-experts ${experts} \
--mlp_type 'residual' \
--num-layers 24 \
--hidden-size 2048 \
--num-attention-heads 16 \
--max-position-embeddings 1024 \
--tokenizer-type GPT2BPETokenizer \
--load $checkpoint_path \
--fp16 \
--ds-inference \

```
To evaluate the performance of PR-MoE, we use the two model structures, `'standard'` and `'residual'` and the configuration parameters as shown in the table below. Since we cannot fit the non-expert part of the 24B+MoE-128 on a single GPU, we use a model-parallel size larger than one. We choose the tensor-slicing degree in order to get the best performance benefit.
|Model|Size (billions)|#Layers|Hidden size|MP degree|EP degree|
|--|--|--|--|--|--|
|2.4B+MoE-128|107.7|16|3584|1|64 - 128|
|24B+MoE-128|1046.9|30|8192|8|64 - 128|
We use 1 node (8 A100 GPUs) to run inference on the 2.4B+MoE-128 and 8 nodes (64 A100 GPUs) for the 24B+MoE-128. Figure below shows the performance of three different configurations: MoE-Standard (PyTorch), MoE-Standard (DeepSpeed-Generic), PR-MoE (DeepSpeed-Generic).
By using the standard-MoE DeepSpeed improves inference performance by 1.4x and 1.65x compared to PyTorch for the two models, respectively. Furthermore, by using the PR-MoE, we can improve the performance speedups to 1.81x and 1.87x, while keeping the model quality maintained.
More performance results and scaling toward bigger models and larger number of GPUs can be seen from our blog post and paper.

Congratulations! You have completed the DeepSpeed MoE inference tutorial.

DeepSpeed v0.5 introduces new support for training Mixture of Experts (MoE) models.
MoE models are an emerging class of sparsely activated models that have sublinear compute costs with respect to their parameters.
For example, the Switch Transformer consists of over 1.6 trillion parameters, while the compute required to train it is approximately equal to that of a 10 billion-parameter dense model.
This increase in model size offers tremendous accuracy gains for a constant compute budget.
For more details on results and further discussion, please see our press release: DeepSpeed powers 8x larger MoE model training with high performance.
## Getting started with a simple MoE example
**Note:** DeepSpeed MoE requires Pytorch 1.8 or above.
As a simple starting point we will show how to apply DeepSpeed MoE to a cifar10 example.
Please refer to
our cifar10 example going forward.
...
DeepSpeed MoE supports five different forms of parallelism, and it exploits both GPU and CPU memory.
Its flexible design enables users to mix different types of prevalent parallelism techniques, as shown in the table below.
|Short Name|Flexible Parallelism Configurations|Benefit|
|--|--|--|
|E|Expert|Scales the model size by increasing the number of experts|
|E + D|Expert + Data|Accelerates training throughput by scaling to multiple data parallel groups|
|E + Z|Expert + ZeRO-powered data|Partitions the nonexpert parameters to support larger base models|
|E + D + M|Expert + Data + Model|Supports massive hidden sizes and even larger base models than E+Z|
|E + D + Z|Expert + Data + ZeRO-powered data|Supports massive hidden sizes and even larger base models than E+Z+M|
|E + Z-Off + M|Expert + ZeRO-Offload + Model|Leverages both GPU and CPU memory for large MoE models on limited # of GPUs|
To support different forms of parallelism, we create various process groups inside DeepSpeed.
The helper functions that DeepSpeed uses reside in `deepspeed/utils/groups.py`
Note: The following function has been deprecated now and model training code does not need to call this anymore.
```
deepspeed.utils.groups.initialize(ep_size="desired expert-parallel world size")
```
Instead, the MoE layer API now accepts `ep_size` as an argument in addition to `num_experts`.
This new API allows users to create MoE models, which can have a different number of experts and a different expert parallelism degree for each MoE layer.
The GPUs (or ranks) participating in an expert-parallel group of size `ep_size` will distribute the total number of experts specified by the layer.
### MoE layer API
The `hidden_size` is the input dimension of a particular layer and the output dimension is the same as that.
This could lead to some changes to your model definition, especially for vision/convolutional models because the input/output dimensions don’t match in certain cases.
E.g. in the CIFAR-10 example, we modify the third fully connected layer to add the MoE layer.
To cater for this, we need to add an additional fully-connected layer, whose input dimension is equal to the output dimension of the MoE layer.
…
```
self.fc3 = nn.Linear(84, 10)
...
…
```
self.fc3 = nn.Linear(84, 84)
self.fc3 = deepspeed.moe.layer.MoE(hidden_size=84, expert=self.fc3, num_experts=args.num_experts, ep_size=<desired expert-parallel world size> ...)
self.fc4 = nn.Linear(84, 10)
```
### Pyramid-Residual MoE
Recently, we proposed a novel Pyramid-Residual MoE (PR-MoE) model architecture.
To create such an MoE model, the users need to do two additional things:
1. To make a pyramid structure, pass `num_experts` as a list e.g. `[4, 8]`.
2. Use the `use_residual` flag to indicate that the MoE layer is now a Residual MoE layer.
```
self.experts = deepspeed.moe.layer.MoE(hidden_size=input_dim, expert=ExpertModule(), num_experts=[..], ep_size=ep_size, use_residual=True)
```
### An Example Scenario
Given a total number of GPUs in our world size and a subset of GPUs in our expert-parallel world as follows.
...
WORLD_SIZE = 4
EP_WORLD_SIZE = 2
EXPERTS = [8]
```
The model code needs to use the `deepspeed.moe.layer.MoE` API as follows.
```
self.experts = deepspeed.moe.layer.MoE(hidden_size=input_dim, expert=ExpertModule(), num_experts=EXPERTS, ep_size=EP_WORLD_SIZE)
```
With the above code, the DeepSpeed runtime will be set to train an MoE model with a total of 8 experts on 4 GPUs in 4 experts/GPU mode.
We call this the E + D mode as described earlier in the table.
```
import torch
import deepspeed
import deepspeed.utils.groups as groups
from deepspeed.moe.layer import MoE
WORLD_SIZE = 4
EP_WORLD_SIZE = 2
EXPERTS = 8
fc3 = torch.nn.Linear(84, 84)
fc3 = MoE(hidden_size=84, expert=self.fc3, num_experts=EXPERTS, ep_size=EP_WORLD_SIZE, k=1)
fc4 = torch.nn.Linear(84, 10)
```
For a runnable end-to-end example that covers both the standard MoE architecture, as well as the PR-MoE model, please look at the cifar10 example.
In addition, see the advanced usage section of this tutorial that links to a more comprehensive example for NLG models.
...
To use MoE Layers in DeepSpeed, we rely on two parameter groups that are passed to an optimizer.
A concrete example to create such groups is available from the cifar10 example.
The relevant function that creates these param groups is as follows.
```
def create_moe_param_groups(model):
from deepspeed.moe.utils import split_params_into_different_moe_groups_for_optimizer
parameters = {'params': [p for p in model.parameters()], 'name': 'parameters'}
return split_params_into_different_moe_groups_for_optimizer(parameters)
```
The above param groups can then be fed to the ZeRO stage-2 optimizer as follows.
```
net = Net()
parameters = create_moe_param_groups(net)
model_engine, optimizer, trainloader, __ = deepspeed.initialize(
args=args, model=net, model_parameters=parameters, training_data=trainset)
```
...
To run the cifar10 example with ZeRO-Offload (stage 2) and MoE, please set the `ds_config` flags
```
"zero_optimization": {
"stage": 2,
"allgather_partitions": true,
"reduce_scatter": true,
"allgather_bucket_size": 50000000,
"reduce_bucket_size": 50000000,
"overlap_comm": true,
"contiguous_gradients": true,
"cpu_offload": true
}
```
An additional optimization to save memory for extremely large model training on limited number of GPUs has also been introduced.
Please enable that using the following config flag to the fp16 optimizer in `ds_config`.
```
"fp16": {
"enabled": true,
"fp16_master_weights_and_grads": true,
}
```
## Random Token Selection
We have devised a new technique called “Random Token Selection” that greatly improves convergence.
Random token selection addresses the limitation of biased selection problem in MoE model training.
Our upcoming paper describes this technique and its results in detail.
This feature is already part of the DeepSpeed runtime and is enabled by default so users can take advantage without any config flags or command-line arguments.

There have been numerous efforts to reduce compute requirements to train large models without sacrificing model quality. To this end, architectures based on Mixture of Experts (MoE) have paved a promising path, enabling sub-linear compute requirements with respect to model parameters and allowing for improved model quality without increasing training cost.

…

To address these above challenges, the DeepSpeed team, as part of Microsoft’s  AI at Scale initiative, has been exploring new applications and optimizations for MoE models at scale. These can lower the training and inference cost of large models, while also enabling the ability to train and serve the next generation of models affordably on today’s hardware.
Here, we are happy to share our findings and innovations for MoE models and systems that 1) **reduce training cost by 5x**, 2) **reduce MoE parameter size by up to 3.7x** **and ** 3) **reduce MoE inference latency by 7.3x at an unprecedented scale and offer up to 4.5x faster and 9x cheaper inference for MoE models compared to quality-equivalent dense models:**
1. **5x reduction in training cost for natural language generation (NLG) models**: We extend the scope of MoE models to beyond just encoder-decoder models and sequence-to-sequence tasks, demonstrating that MoE can reduce the training cost of NLG models like those in the GPT family or MT-NLG by 5x while obtaining the same model quality. Data scientists can now train models of superior quality previously only possible with 5x more hardware resources.

…

**The training cost reduction of MoE is not free and comes at the expense of increasing the total number of parameters required to achieve the same model quality as dense models. PR-MoE is a hybrid dense and MoE model created using residual connections, applying experts only where they are most effective. PR-MoE reduces MoE model parameter size by up to 3x with no change to model quality.
In addition, we leverage staged knowledge distillation to learn a Mixture-of-Students model that further leads to up to 3.7x model size reduction while retaining similar model quality.** **Reduced model size and improved parameter efficiency with Pyramid-Residual-MoE (PR-MoE)** **Architecture and Mixture-of-Students (MoS):**
3. **Fast and economical MoE inference at unprecedented scale:** The DeepSpeed-MoE (DS-MoE) inference system enables efficient scaling of inference workloads on hundreds of GPUs, providing up to 7.3x reduction in inference latency and cost when compared with existing systems. It offers ultra-fast inference latencies (25 ms) for trillion-parameter MoE models. DS-MoE also offers up to 4.5x faster and 9x cheaper inference for MoE models compared to quality-equivalent dense models by combining both system and model optimizations.

…

### Our MoE-based NLG model architecture

To create an MoE-based NLG model, we studied a transformer-based NLG model similar to those of the GPT family. To complete training in a reasonable timeframe, the following models were selected: 350M (24 layers, 1024 hidden size, 16 attention heads), 1.3B (24 layers, 2048 hidden size, 16 attention heads), and 6.7B (32 layers, 4096 hidden size, 32 attention heads).
We use “350M+MoE-128” to denote a MoE model that uses 350M dense model as the base model and adds 128 experts on every other feedforward layer.

### MoE training infrastructure and dataset

We pretrained both the dense and MoE versions of the above models using DeepSpeed (opens in new tab) on 128 NVIDIA Ampere A100 GPUs (Azure ND A100 instances (opens in new tab)). These Azure instances are powered by the latest Azure HPC docker images (opens in new tab) that provide a fully optimized environment and best performing library versions of NCCL, Mellanox OFED, Sharp, and CUDA. DeepSpeed uses a combination of data-parallel and expert-parallel training to effectively scale MoE model training and is capable of training MoE models with trillions of parameters on hundreds of GPUs.

…

*Table 1: Zero-shot evaluation results (last six columns) for different dense and MoE NLG models. All zero-shot evaluation results use the accuracy metric.*

…

This compute cost reduction can directly be translated into throughput gain, training time and training cost reduction by leveraging the efficient DeepSpeed MoE training system. Table 2 shows the training throughput of 1.3B+MoE-128 compared with the 6.7B dense model on 128 NVIDIA A100 GPUs.

…

To reduce model size and improve parameter efficiency, we’ve made innovations in the MoE model architecture that reduce the overall model size by up to 3 times without affecting model quality. We also leverage knowledge distillation to learn a Mixture-of-Students (MoS) model, with a smaller model capacity as the teacher PR-MoE but preserve the teacher model accuracy.

…

### Mixture-of-Students: Distillation for even smaller model size and faster inference

Model compression and distillation present additional opportunities to improve inference performance further. While there are many ways for model compression, such as quantization and pruning, we focus on reducing the number of layers of each expert in MoE and using knowledge distillation to compress the resulting student model to achieve a similar performance to the teacher MoE.
Since MoE structure brings significant benefits by enabling sparse training and inference, our task-agnostic distilled MoE model, which we call Mixture of Students (MoS), inherits these benefits while still providing the flexibility to compress into a dense model. We note that while existing work primarily considers small transformers (a few hundred parameters) and dense encoder-based LM models (like BERT), we focus on studying knowledge distillation for sparse MoE-based auto-generative language models on a multi-billion parameter scale.

…

- To apply knowledge distillation for MoE, we first train a teacher MoE model using the same training hyperparameters and datasets as in the previous section. The teacher model is 350M+PR-MoE-32/64 and 1.3B+PR-MoE-64/128, respectively. We reduce the depth of the teacher model to 21 (12.5%) to obtain a student model, and we force the student to imitate the outputs from the teacher MoE on the training dataset.

…

Our study shows that it is possible to reach similar performance—such as in zero-shot evaluation on many downstream tasks—for a smaller MoE model pretrained with knowledge distillation. The MoS achieve comparable accuracy to the teacher MoE model, retaining 99.3% and 99.1% of the performance despite having 12.5% fewer layers. This enables an additional 12.5% model size reduction. When combined with PR-MoE, it leads to up to 3.7x model size reduction.

## DeepSpeed-MoE inference: Serving MoE models at unprecedented scale and speed

Optimizing for MoE inference latency and cost is crucial for MoE models to be useful in practice. During inference the batch size is generally small, so the inference latency of an MoE model depends primarily on time it takes to load the model parameters from main memory, contrasting with the conventional belief that lesser compute should lead to faster inference. So, inference performance mainly depends on two factors: the overall model size and the overall achievable memory bandwidth.
In the previous section, we presented PR-MoE and distillation to optimize the model size. This section presents our solution to maximize the achievable memory bandwidth by creating a multi-GPU MoE inferencing system that can leverage the aggregated memory bandwidth across dozens of distributed GPUs to speed up inference. Together, DeepSpeed offers an unprecedented scale and efficiency to serve massive MoE models with** 7.3x better latency and cost compared to baseline MoE systems, and up to 4.5x faster and 9x cheaper MoE inference compared to quality-equivalent dense models.**

### MoE inference performance is an interesting paradox

From the best-case view, each token of an MoE model only activates a single expert at each MoE layer, resulting in a critical data path that is equivalent to the base model size, orders-of-magnitude smaller than the actual model size. For example, when inferencing with a 1.3B+MoE-128 model, each input token needs just 1.3 billion parameters, even though the overall model size is 52 billion parameters.
From the worst-case view, the aggregate parameters needed to process a group of tokens can be as large as the full model size, in the example, the entire 52 billion parameters, making it challenging to achieve short latency and high throughput.

### Design goals for the DS-MoE inference system

The design goal of our optimizations is to steer the performance toward the best-case view. This requires careful orchestration and partitioning of the model to group and route all tokens with the same critical data path together to reduce data access per device and achieve maximum aggregate bandwidth. An overview of how DS-MoE tackles this design goal by embracing multi-dimensional parallelism inherent in MoE models is illustrated in Figure 3.
**DS-MoE inference system is centered around three well-coordinated optimizations:**

- The DS-MoE Inference system is designed to minimize the critical data path per device and maximize the achievable aggregate memory bandwidth across devices, which is achieved by: 1) expert parallelism and expert-slicing on expert parameters and 2) data parallelism and tensor-slicing for non-expert parameters.
**Expert parallelism and expert-slicing for expert parameters:** We partition experts across devices, group all tokens of using the same experts under the same critical data path, and parallelize processing of the token groups with different critical paths among different devices using expert parallelism.
 In the example of 1.3B+MoE-128, when expert parallelism is equal to 128, each GPU only processes a single token group corresponding to the experts on that device.
This results in a sequential path that is 1.3 billion parameters per device, 5x smaller than its quality-equivalent dense model with 6.7B parameters. Therefore, in theory, an MoE-based model has the potential to run up to 5x faster than its quality-equivalent dense model using expert parallelism assuming no communication overhead, a topic we discuss in the next section.
In addition, we propose “expert-slicing” to leverage the concept of tensor-slicing for the parameters within an expert. This additional dimension of parallelism is helpful for latency stringent scenarios that we scale to more devices than the number of experts.
**Data parallelism and Tensor-slicing for non-expert parameters:** Within a node, we use tensor-slicing to partition the non-expert parameters, leveraging aggregate GPU memory bandwidth of all GPUs to accelerate the processing. While it is possible to perform tensor-slicing across nodes, the communication overhead of tensor-slicing along with reduced compute granularity generally makes inter-node tensor-slicing inefficient.
To scale non-expert parameters across multiple nodes, we use data parallelism by creating non-expert parameter replicas processing different batches across nodes that incurs no communication overhead or reduction in compute granularity.
 Figure 3 above shows an example scenario for distributed MoE inference highlighting different parts of the MoE model, how the model and data are partitioned, and what form of parallelism is used to deal with each piece.

…

Despite the plug-in optimizations, it is difficult to scale expert parallelism to many devices as the latency increases linearly with the increase in devices. To address this critical scaling challenge, we design two new communication optimization strategies that exploit the underlying point-to-point NCCL operations and custom CUDA kernels to perform necessary data-layout transformations.
**Hierarchical All-to-All**: We implement a hierarchical all-to-all as a two-step process with a data-layout transformation, followed by an intra-node all-to-all, followed by a second data-layout transformation and a final inter-node all-to-all. This reduces the communication hops from O (p) to O (G+p/G), where G is the number of GPUs in a node and p is the total number of GPU devices.
Figure 4 shows the design overview of this implementation. Despite the 2x increase in communication volume, this hierarchical implementation allows for better scaling for small batch sizes as communication at this message size is more latency-bound than bandwidth-bound.**Parallelism Coordinated Communication Optimization:** Combining expert parallelism and tensor-slicing with data parallelism within a single model is non-trivial.
Tensor-slicing splits individual operators across GPUs and requires all-reduce between them, while expert parallelism places expert operators across GPUs without splitting them and requires all-to-all between them. By design, a naïve approach to handle these communication steps will be inefficient.
 To this end, we propose a novel design, as shown in Figure 5, that performs all-to-all only on a subset of devices that share the same tensor-slicing rank instead of all expert-parallel processes.
As a result, the latency of all-to-all can be reduced to O(p/L) instead of O(p) where L is the tensor-slicing parallelism degree. This reduced latency enables us to scale inference to hundreds of GPU devices.
- DS-MoE inference system consists of highly optimized kernels targeting both transformer and MoE-related operations. These kernels aim for maximizing the bandwidth utilization by fusing the operations that work in producer-consumer fashion. In addition to computation required for the transformer layers (explained in this blog post), MoE models require the following additional operations:
1. a gating function that determines the assignment of tokens to experts, where the result is represented as a sparse tensor.
 2. a sparse einsum operator, between the one-hot tensor and all the tokens, which sorts the ordering of the tokens based on the assigned expert ID.
 3. a final einsum that scales and re-sorts the tokens back to their original ordering.

…

We optimize these operators using dense representation and kernel-fusion. First, we fuse the gating function into a single kernel, and use a dense token-to-expert mapping table to represent the assignment from tokens to experts, greatly reducing the kernel launch overhead, as well as memory and compute overhead from the sparse representation.
Second, to optimize the remaining two sparse einsums, we implement them as data layout transformations using the above-mentioned mapping table, to first sort them based on the expert id and then back to its original ordering without requiring any sparse einsum, reducing the complexity of these operations from SxExMxc to SxMxc. Combined, these optimizations result in over 6x reduction in MoE kernel related latency.

### Low latency and high throughput at unprecedented scale

In modern production environments, powerful DL models are often served using hundreds of GPU devices to meet the traffic demand and deliver low latency. Here we demonstrate the performance of DS-MoE Inference System on a 256 A100 with 40 GB GPUs. Table 3 shows various model configurations used for performance comparisons in this section.
|Model|Size (billions)|# of Layers|Hidden size|Model-Parallel degree|Expert-Parallel degree|
|--|--|--|--|--|--|
|2.4B+MoE-128|107.7|16|3,584|1|128|
|8B+MoE-128|349.0|40|4,096|4|128|
|24B+MoE-128|1,046.9|30|8,192|8|128|
|47B+MoE-128|2,024.0|58|8,192|8|128|
We scale MoE models from 107 billion parameters to 2 trillion parameters. To offer a strong baseline for comparison, we utilize a full-featured distributed PyTorch implementation that is capable of both tensor-slicing and expert-parallelism. Figure 6 shows the results for all these model configurations:
- DeepSpeed MoE achieves up to 7.3x reduction in latency while achieving up to 7.3x higher throughput compared to the baseline.
- By effectively exploiting hundreds of GPUs in parallel, DeepSpeed MoE achieves an unprecedented scale for inference at incredibly low latencies – a staggering trillion parameter MoE model can be inferenced under 25ms.
By combining the system optimizations offered by the DS-MoE inference system and model innovations of PR-MoE and MoS, DeepSpeed MoE delivers two more benefits:
1. Reduce the minimum number of GPUs required to perform inference on these models. Figure 7 shows a comparison of three model variants along with the baseline: 1) standard MoE Model (8b-MoE-128), 2) PR-MoE model, and 3) PR-MoE+MoS model. The PR-MoE+MoS model performs the best as expected. The key observation is that the PR-MoE and MoS optimizations allow us to use 16 GPUs instead of 32 GPUs to perform this inference.
2. Further improve both latency and throughput of various MoE model sizes (as shown in Figure 8).

…

When using PyTorch, MoE model inference is more expensive and slower compared to its quality-equivalent dense models. This is true for both model sizes. However, the optimizations in DS-MoE reverse this trend and make MoE model inference both faster and cheaper compared to quality-equivalent dense models. This is a critical result, showing MoE’s benefits over dense beyond training but also on inference latency and cost, which is important to real-world deployments.

…

The benefits increase for larger models because DS-MoE leverages parallelism-coordinated optimization to reduce communication overhead when using tensor-slicing on non-expert part of model. Furthermore, we can take advantage of expert-slicing at this scale, which enables us to scale to a higher number of GPUs compared to the PyTorch baseline.
In addition, for the larger 1.5 trillion-parameter MoE model, we observed 2x additional improvement in throughput over latency as shown in Figure 10. This is because MoE models can run with half the tensor-slicing degree of the dense model (8-way vs. 16-way) and thus two times higher batch size.
Overall, DeepSpeed MoE delivers up to 4.5x faster and up to 9x cheaper MoE model inference compared to serving quality-equivalent dense models using PyTorch. With benefits that scale with model size and hardware resources, as shown from these results, it makes us believe that MoE models will be crucial to bring the next generation of advances in AI scale.

…

To enable practical and efficient inference for MoE models, we offer novel PR-MoE model architecture and MoS distillation technique to significantly reduce the memory requirements of these models. We also offer an MoE inference framework to achieve incredibly low latency and cost at an unprecedented model scale. Combining these innovations, we are able to make these MoE models not just feasible to serve but able to be used for inference at lower latency and cost than their quality-equivalent dense counterparts.

…

With this release of DeepSpeed, we are releasing a generic end-to-end framework for training and inference of MoE-based models. The MoE training support and optimizations are made available in full. The MoE inference optimizations will be released in two phases. The generic flexible parallelism framework for MoE inference is being released today. Optimizations related to computation kernels and communication will be released in future.

Power Next-Generation AI Scale
Samyam Rajbhandari 1 Conglong Li 1 Zhewei Yao 1 Minjia Zhang 1 Reza Yazdani Aminabadi 1
Ammar Ahmad Awan 1 Jeff Rasley 1 Yuxiong He 1
Abstract
As the training of giant dense models hits the
boundary on the availability and capability of
the hardware resources today, Mixture-of-Experts
(MoE) models have become one of the most
promising model architectures due to their signifi-
cant training cost reduction compared to quality-
equivalent dense models.
Their training cost sav-
ing is demonstrated from encoder-decoder models
(prior works) to a 5x saving for auto-aggressive
language models (this work).
However, due to the
much larger model size and unique architecture,
how to provide fast MoE model inference remains
challenging and unsolved, limiting their practical
usage.
To tackle this, we present DeepSpeed-
MoE, an end-to-end MoE training and inference
solution, including novel MoE architecture de-
signs and model compression techniques that re-
duce MoE model size by up to 3.7x, and a highly
optimized inference system that provides 7.3x
better latency and cost compared to existing MoE
inference solutions.
DeepSpeed-MoE offers an
unprecedented scale and efficiency to serve mas-
sive MoE models with up to 4.5x faster and 9x
cheaper inference compared to quality-equivalent
dense models.
We hope our innovations and sys-
tems help open a promising path to new directions
…
staged knowledge distillation to create a distilled version
of PR-MoE, which we call Mixture-of-Students (MoS),
that further reduce model size by 12.5% while retaining
99.3% performance of the teacher (see Section 4).
• We develop DeepSpeed-MoE inference system, a highly
optimized MoE inference system which enables efficient
scaling of inference workloads on hundreds of GPUs,
providing up to 7.3x reduction in inference latency and
cost when compared with existing MoE inference solu-
tions (see Section 5).
It offers ultra-fast inference la-
tencies (under 25 ms) for trillion-parameter MoE mod-
els.
DeepSpeed-MoE also offers up to 4.5x faster and 9x
cheaper inference for MoE models compared to quality-
equivalent dense models by combining both system and
model optimizations.
Together, our innovations and systems enable MoE to be
a more effective and economic alternative comparing to
…
possible.
Software The generic DeepSpeed-MoE end-to-end frame-
work for training and inference of MoE-based models is
open-sourced as part of the DeepSpeed software, and the
experiments presented in this paper were conducted on
the Microsoft Azure AI platform.
Please find the code,
tutorials, and documents at DeepSpeed GitHub (https:
…
Artetxe et al., 2021) primarily focuses on MoE training;
(2) we propose PR-MoE architecture and MoS knowledge
distillation to achieve better MoE parameter efficiency and
on-par/better zero-shot eval quality as described in Section 3;
(3) we develop DeepSpeed-MoE inference system to effi-
...
ger model sizes by leveraging flexible combinations of dif-
ferent types of parallelism including tensor-slicing, data
parallelism, ZeRO (Rajbhandari et al., 2020)-powered data
parallelism, and expert parallelism.
FastMoE (He et al.,
...
We implement a hierarchical all-to-all as a two-step
process with a data-layout transformation, followed by an
intra-node all-to-all, followed by a second data-layout trans-
formation, and a final inter-node all-to-all.
This reduces the
communication hops from O(p) to O(G + p/G), where G