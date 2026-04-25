# Card: Nerfstudio Ray Samplers (defaults + algorithms)
**Source:** https://docs.nerf.studio/_modules/nerfstudio/model_components/ray_samplers.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** authoritative defaults and parameter meanings for ray sampling + proposal/PDF/occupancy sampling implementation in nerfstudio

## Key Content
- **SpacedSampler (core spacing → euclidean bins)**  
  - Create normalized bin edges: `bins = linspace(0,1,num_samples+1)[None,:]`.  
  - **Stratified jitter (train only):** if `train_stratified and training`: jitter within each bin using `t_rand ~ U(0,1)`; if `single_jitter=True`, one jitter per ray (`[num_rays,1]`), else per edge (`[num_rays,num_samples+1]`).  
  - Map near/far through spacing: `s_near = spacing_fn(near)`, `s_far = spacing_fn(far)`.  
  - **Eq.1 (spacing→euclidean):** `t = spacing_fn_inv(x*s_far + (1-x)*s_near)` where `x∈[0,1]` are `bins`.  
  - Output `RaySamples` with `bin_starts=t[..., :-1]`, `bin_ends=t[..., 1:]` plus stored `spacing_*` and `spacing_to_euclidean_fn`.

- **Built-in spacings (all default `train_stratified=True`)**
  - `UniformSampler`: `spacing_fn(x)=x`.  
  - `LinearDisparitySampler`: `spacing_fn(x)=1/x`.  
  - `SqrtSampler`: `spacing_fn=sqrt`, inverse `x^2`.  
  - `LogSampler`: `spacing_fn=log`, inverse `exp`.  
  - `UniformLinDispPiecewiseSampler`: `spacing_fn(x)=where(x<1, x/2, 1-1/(2x))`; inverse `where(x<0.5, 2x, 1/(2-2x))`.

- **PDFSampler (hierarchical resampling from weights)**
  - Defaults: `train_stratified=True`, `include_original=True`, `histogram_padding=0.01`, `single_jitter=False`.  
  - **Eq.2 (PDF/CDF):** `w = weights[...,0] + histogram_padding`; normalize `pdf=w/sum(w)`; `cdf=[0, cumsum(pdf)]` clamped to ≤1.  
  - Sample `u` in `[0,1)` with `num_bins=num_samples+1`: stratified (train) or centered (eval). Invert CDF via `searchsorted`, linear interpolate bins; optionally concatenate+sort with original bins; `bins` are `detach()`’d.

- **VolumetricSampler (Instant-NGP-style occupancy sampling)**
  - Uses `OccGridEstimator.sampling(..., stratified=training, alpha_thre=0.01, near_plane=0.0, far_plane=1e10 if None, cone_angle=0.0)`.  
  - Optional **sigma_fn** (train only): density at midpoint `pos = o + d*(t_start+t_end)/2`.

- **ProposalNetworkSampler (proposal → NeRF sampling loop)**
  - Defaults: `num_proposal_samples_per_ray=(64,)`, `num_nerf_samples_per_ray=32`, `num_proposal_network_iterations=2`, `update_sched=lambda step:1`.  
  - Default samplers: initial `UniformLinDispPiecewiseSampler`; later `PDFSampler(include_original=False)`.  
  - Update logic: `updated = steps_since_update > update_sched(step) or step < 10`; proposal densities computed with grad if updated else `no_grad`.  
  - Anneal: resample with `annealed_weights = weights ** _anneal`.

- **NeuSSampler defaults**
  - `num_samples=64`, `num_samples_importance=64`, `num_samples_outside=32`, `num_upsample_steps=4`, `base_variance=64`, `single_jitter=True`.  
  - Upsampling uses fixed `inv_s = base_variance * 2**iter` and PDF resampling with `histogram_padding=1e-5`, `include_original=False`.

## When to surface
Use when students ask how nerfstudio chooses ray sample locations (uniform vs disparity/log), what “stratified” and “single_jitter” mean, how PDF/proposal/hierarchical sampling is implemented, or what the default sample counts and thresholds are.