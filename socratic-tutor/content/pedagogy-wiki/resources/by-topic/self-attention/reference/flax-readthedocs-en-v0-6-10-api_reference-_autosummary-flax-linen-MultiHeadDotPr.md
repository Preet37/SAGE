# Source: https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html
# Title: flax.linen.MultiHeadDotProductAttention
# Fetched via: jina
# Date: 2026-04-11

Title: flax.linen.MultiHeadDotProductAttention


# flax.linen.MultiHeadDotProductAttention

Ctrl+K


*   [Quick start](https://flax.readthedocs.io/en/v0.6.10/getting_started.html)
*   [Guides](https://flax.readthedocs.io/en/v0.6.10/guides/index.html)- [x] 
    *   [Flax fundamentals](https://flax.readthedocs.io/en/v0.6.10/guides/index_flax_fundamentals.html)- [x] 
        *   [JAX 101](https://jax.readthedocs.io/en/latest/jax-101/index.html)
        *   [Flax Basics](https://flax.readthedocs.io/en/v0.6.10/guides/flax_basics.html)
        *   [Managing Parameters and State](https://flax.readthedocs.io/en/v0.6.10/guides/state_params.html)
        *   [`setup` vs `compact`](https://flax.readthedocs.io/en/v0.6.10/guides/setup_or_nncompact.html)
        *   [Dealing with Flax Module arguments](https://flax.readthedocs.io/en/v0.6.10/guides/arguments.html)

    *   [Data preprocesing](https://flax.readthedocs.io/en/v0.6.10/guides/index_data_preprocessing.html)- [x] 
        *   [Processing the entire Dataset](https://flax.readthedocs.io/en/v0.6.10/guides/full_eval.html)

    *   [Training techniques](https://flax.readthedocs.io/en/v0.6.10/guides/index_training_techniques.html)- [x] 
        *   [Batch normalization](https://flax.readthedocs.io/en/v0.6.10/guides/batch_norm.html)
        *   [Dropout](https://flax.readthedocs.io/en/v0.6.10/guides/dropout.html)
        *   [Learning rate scheduling](https://flax.readthedocs.io/en/v0.6.10/guides/lr_schedule.html)
        *   [Transfer learning](https://flax.readthedocs.io/en/v0.6.10/guides/transfer_learning.html)
        *   [Save and load checkpoints](https://flax.readthedocs.io/en/v0.6.10/guides/use_checkpointing.html)

    *   [Parallel training](https://flax.readthedocs.io/en/v0.6.10/guides/index_parallel_training.html)- [x] 
        *   [Ensembling on multiple devices](https://flax.readthedocs.io/en/v0.6.10/guides/ensembling.html)
        *   [Scale up Flax Modules on multiple devices with `pjit`](https://flax.readthedocs.io/en/v0.6.10/guides/flax_on_pjit.html)

    *   [Model inspection](https://flax.readthedocs.io/en/v0.6.10/guides/index_model_inspection.html)- [x] 
        *   [Model surgery](https://flax.readthedocs.io/en/v0.6.10/guides/model_surgery.html)
        *   [Extracting intermediate values](https://flax.readthedocs.io/en/v0.6.10/guides/extracting_intermediates.html)

    *   [Converting and upgrading](https://flax.readthedocs.io/en/v0.6.10/guides/index_converting_and_upgrading.html)- [x] 
        *   [Convert PyTorch models to Flax](https://flax.readthedocs.io/en/v0.6.10/guides/convert_pytorch_to_flax.html)
        *   [Migrate checkpointing to Orbax](https://flax.readthedocs.io/en/v0.6.10/guides/orbax_upgrade_guide.html)
        *   [Upgrading my codebase to Optax](https://flax.readthedocs.io/en/v0.6.10/guides/optax_update_guide.html)
        *   [Upgrading my codebase to Linen](https://flax.readthedocs.io/en/v0.6.10/guides/linen_upgrade_guide.html)

    *   [The Sharp Bits](https://flax.readthedocs.io/en/v0.6.10/notebooks/flax_sharp_bits.html)

*   [Examples](https://flax.readthedocs.io/en/v0.6.10/examples.html)- [x] 
    *   [Core examples](https://flax.readthedocs.io/en/v0.6.10/examples_core_examples.html)
    *   [Google Research examples](https://flax.readthedocs.io/en/v0.6.10/examples_google_research_examples.html)
    *   [Repositories that use Flax](https://flax.readthedocs.io/en/v0.6.10/examples_repositories_that_use_flax.html)
    *   [Community examples](https://flax.readthedocs.io/en/v0.6.10/examples_community_examples.html)

*   [Glossary](https://flax.readthedocs.io/en/v0.6.10/glossary.html)
*   [Developer notes](https://flax.readthedocs.io/en/v0.6.10/developer_notes/index.html)- [x] 
    *   [The Flax Module lifecycle](https://flax.readthedocs.io/en/v0.6.10/developer_notes/module_lifecycle.html)
    *   [Lifted transformations](https://flax.readthedocs.io/en/v0.6.10/developer_notes/lift.html)
    *   [FLIPs](https://github.com/google/flax/tree/main/docs/flip)

*   [The Flax philosophy](https://flax.readthedocs.io/en/v0.6.10/philosophy.html)
*   [How to contribute](https://flax.readthedocs.io/en/v0.6.10/contributing.html)
*   [API Reference](https://flax.readthedocs.io/en/v0.6.10/api_reference/index.html)- [x] 
    *   [flax.config package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.config.html)
    *   [flax.core.frozen_dict package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.core.frozen_dict.html)
    *   [flax.error package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.errors.html)
    *   [flax.jax_utils package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.jax_utils.html)
    *   [flax.linen package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.linen.html)- [x] 
        *   [flax.linen.enable_named_call](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.enable_named_call.html)
        *   [flax.linen.disable_named_call](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.disable_named_call.html)
        *   [flax.linen.override_named_call](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.override_named_call.html)
        *   [flax.linen.tabulate](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.tabulate.html)
        *   [flax.linen.vmap](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.vmap.html)
        *   [flax.linen.scan](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.scan.html)
        *   [flax.linen.jit](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.jit.html)
        *   [flax.linen.remat](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.remat.html)
        *   [flax.linen.remat_scan](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.remat_scan.html)
        *   [flax.linen.map_variables](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.map_variables.html)
        *   [flax.linen.jvp](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.jvp.html)
        *   [flax.linen.vjp](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.vjp.html)
        *   [flax.linen.custom_vjp](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.custom_vjp.html)
        *   [flax.linen.while_loop](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.while_loop.html)
        *   [flax.linen.cond](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.cond.html)
        *   [flax.linen.switch](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.switch.html)
        *   [flax.linen.Partitioned](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Partitioned.html)
        *   [flax.linen.with_partitioning](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.with_partitioning.html)
        *   [flax.linen.get_partition_spec](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.get_partition_spec.html)
        *   [flax.linen.get_sharding](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.get_sharding.html)
        *   [flax.linen.LogicallyPartitioned](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.LogicallyPartitioned.html)
        *   [flax.linen.logical_axis_rules](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.logical_axis_rules.html)
        *   [flax.linen.set_logical_axis_rules](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.set_logical_axis_rules.html)
        *   [flax.linen.get_logical_axis_rules](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.get_logical_axis_rules.html)
        *   [flax.linen.logical_to_mesh_axes](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.logical_to_mesh_axes.html)
        *   [flax.linen.logical_to_mesh](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.logical_to_mesh.html)
        *   [flax.linen.logical_to_mesh_sharding](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.logical_to_mesh_sharding.html)
        *   [flax.linen.with_logical_constraint](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.with_logical_constraint.html)
        *   [flax.linen.with_logical_partitioning](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.with_logical_partitioning.html)
        *   [flax.linen.Dense](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Dense.html)
        *   [flax.linen.DenseGeneral](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.DenseGeneral.html)
        *   [flax.linen.Conv](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Conv.html)
        *   [flax.linen.ConvTranspose](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.ConvTranspose.html)
        *   [flax.linen.ConvLocal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.ConvLocal.html)
        *   [flax.linen.Embed](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Embed.html)
        *   [flax.linen.BatchNorm](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.BatchNorm.html)
        *   [flax.linen.LayerNorm](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.LayerNorm.html)
        *   [flax.linen.GroupNorm](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.GroupNorm.html)
        *   [flax.linen.max_pool](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.max_pool.html)
        *   [flax.linen.avg_pool](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.avg_pool.html)
        *   [flax.linen.pool](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.pool.html)
        *   [flax.linen.activation.PReLU](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.PReLU.html)
        *   [flax.linen.activation.celu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.celu.html)
        *   [flax.linen.activation.elu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.elu.html)
        *   [flax.linen.activation.gelu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.gelu.html)
        *   [flax.linen.activation.glu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.glu.html)
        *   [flax.linen.activation.hard_sigmoid](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.hard_sigmoid.html)
        *   [flax.linen.activation.hard_silu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.hard_silu.html)
        *   [flax.linen.activation.hard_swish](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.hard_swish.html)
        *   [flax.linen.activation.hard_tanh](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.hard_tanh.html)
        *   [flax.linen.activation.leaky_relu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.leaky_relu.html)
        *   [flax.linen.activation.log_sigmoid](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.log_sigmoid.html)
        *   [flax.linen.activation.log_softmax](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.log_softmax.html)
        *   [flax.linen.activation.logsumexp](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.logsumexp.html)
        *   [flax.linen.activation.one_hot](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.one_hot.html)
        *   [flax.linen.activation.relu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.relu.html)
        *   [flax.linen.activation.relu6](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.relu6.html)
        *   [flax.linen.activation.selu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.selu.html)
        *   [flax.linen.activation.sigmoid](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.sigmoid.html)
        *   [flax.linen.activation.silu](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.silu.html)
        *   [flax.linen.activation.soft_sign](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.soft_sign.html)
        *   [flax.linen.activation.softmax](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.softmax.html)
        *   [flax.linen.activation.softplus](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.softplus.html)
        *   [flax.linen.activation.standardize](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.standardize.html)
        *   [flax.linen.activation.swish](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.swish.html)
        *   [flax.linen.activation.tanh](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.activation.tanh.html)
        *   [flax.linen.initializers.constant](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.constant.html)
        *   [flax.linen.initializers.delta_orthogonal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.delta_orthogonal.html)
        *   [flax.linen.initializers.glorot_normal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.glorot_normal.html)
        *   [flax.linen.initializers.glorot_uniform](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.glorot_uniform.html)
        *   [flax.linen.initializers.he_normal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.he_normal.html)
        *   [flax.linen.initializers.he_uniform](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.he_uniform.html)
        *   [flax.linen.initializers.kaiming_normal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.kaiming_normal.html)
        *   [flax.linen.initializers.kaiming_uniform](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.kaiming_uniform.html)
        *   [flax.linen.initializers.lecun_normal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.lecun_normal.html)
        *   [flax.linen.initializers.lecun_uniform](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.lecun_uniform.html)
        *   [flax.linen.initializers.normal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.normal.html)
        *   [flax.linen.initializers.ones](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.ones.html)
        *   [flax.linen.initializers.ones_init](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.ones_init.html)
        *   [flax.linen.initializers.orthogonal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.orthogonal.html)
        *   [flax.linen.initializers.uniform](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.uniform.html)
        *   [flax.linen.initializers.variance_scaling](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.variance_scaling.html)
        *   [flax.linen.initializers.xavier_normal](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.xavier_normal.html)
        *   [flax.linen.initializers.xavier_uniform](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.xavier_uniform.html)
        *   [flax.linen.initializers.zeros](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.zeros.html)
        *   [flax.linen.initializers.zeros_init](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.initializers.zeros_init.html)
        *   [flax.linen.Sequential](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Sequential.html)
        *   [flax.linen.dot_product_attention_weights](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.dot_product_attention_weights.html)
        *   [flax.linen.dot_product_attention](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.dot_product_attention.html)
        *   [flax.linen.make_attention_mask](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.make_attention_mask.html)
        *   [flax.linen.make_causal_mask](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.make_causal_mask.html)
        *   [flax.linen.SelfAttention](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.SelfAttention.html)
        *   [flax.linen.MultiHeadDotProductAttention](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#)
        *   [flax.linen.Dropout](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Dropout.html)
        *   [flax.linen.LSTMCell](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.LSTMCell.html)
        *   [flax.linen.OptimizedLSTMCell](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.OptimizedLSTMCell.html)
        *   [flax.linen.GRUCell](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.GRUCell.html)
        *   [flax.linen.RNNCellBase](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.RNNCellBase.html)
        *   [flax.linen.RNN](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.RNN.html)
        *   [flax.linen.Bidirectional](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Bidirectional.html)

    *   [flax.serialization package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.serialization.html)
    *   [flax.struct package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.struct.html)
    *   [flax.traceback_util package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.traceback_util.html)
    *   [flax.training package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.training.html)
    *   [flax.traverse_util package](https://flax.readthedocs.io/en/v0.6.10/api_reference/flax.traverse_util.html)

[](https://github.com/google/flax "Source repository")

*   [.rst](https://flax.readthedocs.io/en/v0.6.10/_sources/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.rst "Download source file")
*   .pdf

# flax.linen.MultiHeadDotProductAttention

## Contents

*   [`MultiHeadDotProductAttention`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention)
    *   [`MultiHeadDotProductAttention.num_heads`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.num_heads)
    *   [`MultiHeadDotProductAttention.dtype`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.dtype)
    *   [`MultiHeadDotProductAttention.param_dtype`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.param_dtype)
    *   [`MultiHeadDotProductAttention.qkv_features`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.qkv_features)
    *   [`MultiHeadDotProductAttention.out_features`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.out_features)
    *   [`MultiHeadDotProductAttention.broadcast_dropout`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.broadcast_dropout)
    *   [`MultiHeadDotProductAttention.dropout_rate`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.dropout_rate)
    *   [`MultiHeadDotProductAttention.deterministic`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.deterministic)
    *   [`MultiHeadDotProductAttention.precision`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.precision)
    *   [`MultiHeadDotProductAttention.kernel_init`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.kernel_init)
    *   [`MultiHeadDotProductAttention.bias_init`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.bias_init)
    *   [`MultiHeadDotProductAttention.use_bias`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.use_bias)
    *   [`MultiHeadDotProductAttention.attention_fn`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.attention_fn)
    *   [`MultiHeadDotProductAttention.decode`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.decode)
    *   [`MultiHeadDotProductAttention.__call__()`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.__call__)

# flax.linen.MultiHeadDotProductAttention[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax-linen-multiheaddotproductattention "Permalink to this heading")

_class_ flax.linen.MultiHeadDotProductAttention(_num\_heads_, _dtype=None_, _param\_dtype=<class'jax.numpy.float32'>_, _qkv\_features=None_, _out\_features=None_, _broadcast\_dropout=True_, _dropout\_rate=0.0_, _deterministic=None_, _precision=None_, _kernel\_init=<function variance\_scaling.<locals>.init>_, _bias\_init=<function zeros>_, _use\_bias=True_, _attention\_fn=<function dot\_product\_attention>_, _decode=False_, _qkv\_dot\_general=<function dot\_general>_, _out\_dot\_general=<function dot\_general>_, _parent=<flax.linen.module.\_Sentinel object>_, _name=None_)[[source]](https://flax.readthedocs.io/en/v0.6.10/_modules/flax/linen/attention.html#MultiHeadDotProductAttention)[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention "Permalink to this definition")
Multi-head dot-product attention.

num_heads[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.num_heads "Permalink to this definition")
number of attention heads. Features (i.e. inputs_q.shape[-1]) should be divisible by the number of heads.

Type
int

dtype[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.dtype "Permalink to this definition")
the dtype of the computation (default: infer from inputs and params)

Type
Optional[Any]

param_dtype[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.param_dtype "Permalink to this definition")
the dtype passed to parameter initializers (default: float32)

Type
Any

qkv_features[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.qkv_features "Permalink to this definition")
dimension of the key, query, and value.

Type
Optional[int]

out_features[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.out_features "Permalink to this definition")
dimension of the last projection

Type
Optional[int]

broadcast_dropout[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.broadcast_dropout "Permalink to this definition")
bool: use a broadcasted dropout along batch dims.

Type
bool

dropout_rate[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.dropout_rate "Permalink to this definition")
dropout rate

Type
float

deterministic[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.deterministic "Permalink to this definition")
if false, the attention weight is masked randomly using dropout, whereas if true, the attention weights are deterministic.

Type
Optional[bool]

precision[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.precision "Permalink to this definition")
numerical precision of the computation see jax.lax.Precision for details.

Type
Union[None, str, jax._src.lax.lax.Precision, Tuple[str, str], Tuple[jax._src.lax.lax.Precision, jax._src.lax.lax.Precision]]

kernel_init[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.kernel_init "Permalink to this definition")
initializer for the kernel of the Dense layers.

Type
Callable[[Any, Tuple[int, …], Any], Any]

bias_init[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.bias_init "Permalink to this definition")
initializer for the bias of the Dense layers.

Type
Callable[[Any, Tuple[int, …], Any], Any]

use_bias[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.use_bias "Permalink to this definition")
bool: whether pointwise QKVO dense transforms use bias.

Type
bool

attention_fn[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.attention_fn "Permalink to this definition")
dot_product_attention or compatible function. Accepts query, key, value, and returns output of shape [bs, dim1, dim2, …, dimN,, num_heads, value_channels]`

Type
Callable[[…], Any]

decode[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.decode "Permalink to this definition")
whether to prepare and use an autoregressive cache.

Type
bool

 __call__ (_inputs\_q_, _inputs\_kv_, _mask=None_, _deterministic=None_)[[source]](https://flax.readthedocs.io/en/v0.6.10/_modules/flax/linen/attention.html#MultiHeadDotProductAttention.__call__)[#](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.__call__ "Permalink to this definition")
Applies multi-head dot product attention on the input data.

Projects the inputs into multi-headed query, key, and value vectors, applies dot-product attention and project the results to an output vector.

Parameters
*   **inputs_q** – input queries of shape [batch_sizes…, length, features].

*   **inputs_kv** – key/values of shape [batch_sizes…, length, features].

*   **mask** – attention mask of shape [batch_sizes…, num_heads, query_length, key/value_length]. Attention weights are masked out if their corresponding mask value is False.

*   **deterministic** – if false, the attention weight is masked randomly using dropout, whereas if true, the attention weights are deterministic.

Returns
output of shape [batch_sizes…, length, features].

Methods

[previous flax.linen.SelfAttention](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.SelfAttention.html "previous page")[next flax.linen.Dropout](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.Dropout.html "next page")

 Contents 

*   [`MultiHeadDotProductAttention`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention)
    *   [`MultiHeadDotProductAttention.num_heads`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.num_heads)
    *   [`MultiHeadDotProductAttention.dtype`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.dtype)
    *   [`MultiHeadDotProductAttention.param_dtype`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.param_dtype)
    *   [`MultiHeadDotProductAttention.qkv_features`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.qkv_features)
    *   [`MultiHeadDotProductAttention.out_features`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.out_features)
    *   [`MultiHeadDotProductAttention.broadcast_dropout`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.broadcast_dropout)
    *   [`MultiHeadDotProductAttention.dropout_rate`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.dropout_rate)
    *   [`MultiHeadDotProductAttention.deterministic`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.deterministic)
    *   [`MultiHeadDotProductAttention.precision`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.precision)
    *   [`MultiHeadDotProductAttention.kernel_init`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.kernel_init)
    *   [`MultiHeadDotProductAttention.bias_init`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.bias_init)
    *   [`MultiHeadDotProductAttention.use_bias`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.use_bias)
    *   [`MultiHeadDotProductAttention.attention_fn`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.attention_fn)
    *   [`MultiHeadDotProductAttention.decode`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.decode)
    *   [`MultiHeadDotProductAttention.__call__()`](https://flax.readthedocs.io/en/v0.6.10/api_reference/_autosummary/flax.linen.MultiHeadDotProductAttention.html#flax.linen.MultiHeadDotProductAttention.__call__)

By The Flax authors

© Copyright 2023, The Flax authors.