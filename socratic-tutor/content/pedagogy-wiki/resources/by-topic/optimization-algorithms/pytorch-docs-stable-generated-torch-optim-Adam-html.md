# Source: https://pytorch.org/docs/stable/generated/torch.optim.Adam.html
# Author: PyTorch
# Author Slug: pytorch
# Downloaded: 2026-04-06
# Words: 1885
Adam[#](#adam)
-
class torch.optim.Adam(params, lr=0.001, betas=(0.9, 0.999), eps=1e-08, weight_decay=0, amsgrad=False, *, foreach=None, maximize=False, capturable=False, differentiable=False, fused=None, decoupled_weight_decay=False)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/adam.py#L34)[#](#torch.optim.Adam) Implements Adam algorithm.
For further details regarding the algorithm we refer to
[Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980).- Parameters:
params (iterable) – iterable of parameters or named_parameters to optimize or iterable of dicts defining parameter groups. When using named_parameters, all parameters in all groups should be named
lr (
[float](https://docs.python.org/3/library/functions.html#float),[Tensor](../tensors.html#torch.Tensor), optional) – learning rate (default: 1e-3). A tensor LR is not yet supported for all our implementations. Please use a float LR if you are not also specifying fused=True or capturable=True.betas (
[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[Union[[float](https://docs.python.org/3/library/functions.html#float),[Tensor](../tensors.html#torch.Tensor)], Union[[float](https://docs.python.org/3/library/functions.html#float),[Tensor](../tensors.html#torch.Tensor)]], optional) – coefficients used for computing running averages of gradient and its square. If a tensor is provided, must be 1-element. (default: (0.9, 0.999))eps (
[float](https://docs.python.org/3/library/functions.html#float), optional) – term added to the denominator to improve numerical stability (default: 1e-8)weight_decay (
[float](https://docs.python.org/3/library/functions.html#float), optional) – weight decay (L2 penalty) (default: 0)decoupled_weight_decay (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – if True, this optimizer is equivalent to AdamW and the algorithm will not accumulate weight decay in the momentum nor variance. (default: False)amsgrad (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – whether to use the AMSGrad variant of this algorithm from the paper[On the Convergence of Adam and Beyond](https://openreview.net/forum?id=ryQu7f-RZ)(default: False)foreach (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – whether foreach implementation of optimizer is used. If unspecified by the user (so foreach is None), we will try to use foreach over the for-loop implementation on CUDA, since it is usually significantly more performant. Note that the foreach implementation uses ~ sizeof(params) more peak memory than the for-loop version due to the intermediates being a tensorlist vs just one tensor. If memory is prohibitive, batch fewer parameters through the optimizer at a time or switch this flag to False (default: None)maximize (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – maximize the objective with respect to the params, instead of minimizing (default: False)capturable (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – whether this instance is safe to capture in a graph, whether for CUDA graphs or for torch.compile support. Tensors are only capturable when on supported[accelerators](../torch.html#accelerators). Passing True can impair ungraphed performance, so if you don’t intend to graph capture this instance, leave it False (default: False)differentiable (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – whether autograd should occur through the optimizer step in training. Otherwise, the step() function runs in a torch.no_grad() context. Setting to True can impair performance, so leave it False if you don’t intend to run autograd through this instance (default: False)fused (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) – whether the fused implementation is used. Currently, torch.float64, torch.float32, torch.float16, and torch.bfloat16 are supported. (default: None)
Note
The foreach and fused implementations are typically faster than the for-loop, single-tensor implementation, with fused being theoretically fastest with both vertical and horizontal fusion. As such, if the user has not specified either flag (i.e., when foreach = fused = None), we will attempt defaulting to the foreach implementation when the tensors are all on CUDA. Why not fused? Since the fused implementation is relatively new, we want to give it sufficient bake-in time. To specify fused, pass True for fused. To force running the for-loop implementation, pass False for either foreach or fused.
Note
A prototype implementation of Adam and AdamW for MPS supports torch.float32 and torch.float16.
-
add_param_group(param_group)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L1106)[#](#torch.optim.Adam.add_param_group) Add a param group to the
s param_groups.Optimizer
This can be useful when fine tuning a pre-trained network as frozen layers can be made trainable and added to the
as training progresses.Optimizer
- Parameters:
param_group (
[dict](https://docs.python.org/3/library/stdtypes.html#dict)) – Specifies what Tensors should be optimized along with group specific optimization options.
-
load_state_dict(state_dict)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L883)[#](#torch.optim.Adam.load_state_dict) Load the optimizer state.
- Parameters:
state_dict (
[dict](https://docs.python.org/3/library/stdtypes.html#dict)) – optimizer state. Should be an object returned from a call to.state_dict()
Warning
Make sure this method is called after initializing
, as calling it beforehand will overwrite the loaded learning rates.torch.optim.lr_scheduler.LRScheduler
Note
The names of the parameters (if they exist under the “param_names” key of each param group in
) will not affect the loading process. To use the parameters’ names for custom cases (such as when the parameters in the loaded state dict differ from those initialized in the optimizer), a customstate_dict()
register_load_state_dict_pre_hook
should be implemented to adapt the loaded dict accordingly. Ifparam_names
exist in loaded state dictparam_groups
they will be saved and override the current names, if present, in the optimizer state. If they do not exist in loaded state dict, the optimizerparam_names
will remain unchanged.Example
>>> model = torch.nn.Linear(10, 10) >>> optim = torch.optim.SGD(model.parameters(), lr=3e-4) >>> scheduler1 = torch.optim.lr_scheduler.LinearLR( ... optim, ... start_factor=0.1, ... end_factor=1, ... total_iters=20, ... ) >>> scheduler2 = torch.optim.lr_scheduler.CosineAnnealingLR( ... optim, ... T_max=80, ... eta_min=3e-5, ... ) >>> lr = torch.optim.lr_scheduler.SequentialLR( ... optim, ... schedulers=[scheduler1, scheduler2], ... milestones=[20], ... ) >>> lr.load_state_dict(torch.load("./save_seq.pt")) >>> # now load the optimizer checkpoint after loading the LRScheduler >>> optim.load_state_dict(torch.load("./save_optim.pt"))
-
register_load_state_dict_post_hook(hook, prepend=False)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L847)[#](#torch.optim.Adam.register_load_state_dict_post_hook) Register a load_state_dict post-hook which will be called after
is called. It should have the following signature:load_state_dict()
hook(optimizer) -> None
The
optimizer
argument is the optimizer instance being used.The hook will be called with argument
self
after callingload_state_dict
onself
. The registered hook can be used to perform post-processing afterload_state_dict
has loaded thestate_dict
.- Parameters:
hook (Callable) – The user defined hook to be registered.
prepend (
[bool](https://docs.python.org/3/library/functions.html#bool)) – If True, the provided posthook
will be fired before all the already registered post-hooks onload_state_dict
. Otherwise, the providedhook
will be fired after all the already registered post-hooks. (default: False)
- Returns:
a handle that can be used to remove the added hook by calling
handle.remove()
- Return type:
torch.utils.hooks.RemovableHandle
-
register_load_state_dict_pre_hook(hook, prepend=False)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L808)[#](#torch.optim.Adam.register_load_state_dict_pre_hook) Register a load_state_dict pre-hook which will be called before
is called. It should have the following signature:load_state_dict()
hook(optimizer, state_dict) -> state_dict or None
The
optimizer
argument is the optimizer instance being used and thestate_dict
argument is a shallow copy of thestate_dict
the user passed in toload_state_dict
. The hook may modify the state_dict inplace or optionally return a new one. If a state_dict is returned, it will be used to be loaded into the optimizer.The hook will be called with argument
self
andstate_dict
before callingload_state_dict
onself
. The registered hook can be used to perform pre-processing before theload_state_dict
call is made.- Parameters:
hook (Callable) – The user defined hook to be registered.
prepend (
[bool](https://docs.python.org/3/library/functions.html#bool)) – If True, the provided prehook
will be fired before all the already registered pre-hooks onload_state_dict
. Otherwise, the providedhook
will be fired after all the already registered pre-hooks. (default: False)
- Returns:
a handle that can be used to remove the added hook by calling
handle.remove()
- Return type:
torch.utils.hooks.RemovableHandle
-
register_state_dict_post_hook(hook, prepend=False)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L649)[#](#torch.optim.Adam.register_state_dict_post_hook) Register a state dict post-hook which will be called after
is called.state_dict()
It should have the following signature:
hook(optimizer, state_dict) -> state_dict or None
The hook will be called with arguments
self
andstate_dict
after generating astate_dict
onself
. The hook may modify the state_dict inplace or optionally return a new one. The registered hook can be used to perform post-processing on thestate_dict
before it is returned.- Parameters:
hook (Callable) – The user defined hook to be registered.
prepend (
[bool](https://docs.python.org/3/library/functions.html#bool)) – If True, the provided posthook
will be fired before all the already registered post-hooks onstate_dict
. Otherwise, the providedhook
will be fired after all the already registered post-hooks. (default: False)
- Returns:
a handle that can be used to remove the added hook by calling
handle.remove()
- Return type:
torch.utils.hooks.RemovableHandle
-
register_state_dict_pre_hook(hook, prepend=False)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L617)[#](#torch.optim.Adam.register_state_dict_pre_hook) Register a state dict pre-hook which will be called before
is called.state_dict()
It should have the following signature:
hook(optimizer) -> None
The
optimizer
argument is the optimizer instance being used. The hook will be called with argumentself
before callingstate_dict
onself
. The registered hook can be used to perform pre-processing before thestate_dict
call is made.- Parameters:
hook (Callable) – The user defined hook to be registered.
prepend (
[bool](https://docs.python.org/3/library/functions.html#bool)) – If True, the provided prehook
will be fired before all the already registered pre-hooks onstate_dict
. Otherwise, the providedhook
will be fired after all the already registered pre-hooks. (default: False)
- Returns:
a handle that can be used to remove the added hook by calling
handle.remove()
- Return type:
torch.utils.hooks.RemovableHandle
-
register_step_post_hook(hook)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L596)[#](#torch.optim.Adam.register_step_post_hook) Register an optimizer step post hook which will be called after optimizer step.
It should have the following signature:
hook(optimizer, args, kwargs) -> None
The
optimizer
argument is the optimizer instance being used.- Parameters:
hook (Callable) – The user defined hook to be registered.
- Returns:
a handle that can be used to remove the added hook by calling
handle.remove()
- Return type:
torch.utils.hooks.RemovableHandle
-
register_step_pre_hook(hook)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L573)[#](#torch.optim.Adam.register_step_pre_hook) Register an optimizer step pre hook which will be called before optimizer step.
It should have the following signature:
hook(optimizer, args, kwargs) -> None or modified args and kwargs
The
optimizer
argument is the optimizer instance being used. If args and kwargs are modified by the pre-hook, then the transformed values are returned as a tuple containing the new_args and new_kwargs.- Parameters:
hook (Callable) – The user defined hook to be registered.
- Returns:
a handle that can be used to remove the added hook by calling
handle.remove()
- Return type:
torch.utils.hooks.RemovableHandle
-
state_dict()
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L683)[#](#torch.optim.Adam.state_dict) Return the state of the optimizer as a
.dict
It contains two entries:
state
: a Dict holding current optimization state. Its contentdiffers between optimizer classes, but some common characteristics hold. For example, state is saved per parameter, and the parameter itself is NOT saved.
state
is a Dictionary mapping parameter ids to a Dict with state corresponding to each parameter.
param_groups
: a List containing all parameter groups where eachparameter group is a Dict. Each parameter group contains metadata specific to the optimizer, such as learning rate and weight decay, as well as a List of parameter IDs of the parameters in the group. If a param group was initialized with
named_parameters()
the names content will also be saved in the state dict.
NOTE: The parameter IDs may look like indices but they are just IDs associating state with param_group. When loading from a state_dict, the optimizer will zip the param_group
params
(int IDs) and the optimizerparam_groups
(actualnn.Parameter
s) in order to match state WITHOUT additional verification.A returned state dict might look something like:
{ 'state': { 0: {'momentum_buffer': tensor(...), ...}, 1: {'momentum_buffer': tensor(...), ...}, 2: {'momentum_buffer': tensor(...), ...}, 3: {'momentum_buffer': tensor(...), ...} }, 'param_groups': [ { 'lr': 0.01, 'weight_decay': 0, ... 'params': [0] 'param_names' ['param0'] (optional) }, { 'lr': 0.001, 'weight_decay': 0.5, ... 'params': [1, 2, 3] 'param_names': ['param1', 'layer.weight', 'layer.bias'] (optional) } ] }
-
step(closure=None)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/adam.py#L214)[#](#torch.optim.Adam.step) Perform a single optimization step.
- Parameters:
closure (Callable, optional) – A closure that reevaluates the model and returns the loss.
-
zero_grad(set_to_none=True)
[[source]](https://github.com/pytorch/pytorch/blob/v2.11.0/torch/optim/optimizer.py#L1027)[#](#torch.optim.Adam.zero_grad) Reset the gradients of all optimized
s.torch.Tensor
- Parameters:
set_to_none (
[bool](https://docs.python.org/3/library/functions.html#bool), optional) –Instead of setting to zero, set the grads to None. Default:
True
This will in general have lower memory footprint, and can modestly improve performance. However, it changes certain behaviors. For example:
When the user tries to access a gradient and perform manual ops on it, a None attribute or a Tensor full of 0s will behave differently.
If the user requests
zero_grad(set_to_none=True)
followed by a backward pass,.grad
s are guaranteed to be None for params that did not receive a gradient.torch.optim
optimizers have a different behavior if the gradient is 0 or None (in one case it does the step with a gradient of 0 and in the other it skips the step altogether).