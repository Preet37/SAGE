# Card: Omniverse Replicator Core API (v1.4.0) — essentials for reproducible synthetic-data scripts
**Source:** https://docs.omniverse.nvidia.com/py/replicator/1.4.0/source/extensions/omni.replicator.core/docs/API.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Exact callable signatures + parameter defaults (incl. `new_layer` clearing behavior, writer/creator/distribution defaults)

## Key Content
- **Layer isolation (authoring context)**
  - `omni.replicator.core.new_layer(name: str = None)`  
    Creates a new authoring layer context to contain Replicator changes. **If a layer of the same name already exists, it is cleared** before applying new changes. Default name: **"Replicator"**.
- **Basic data-writing pipeline (minimal workflow)**
  1. Create camera: `rep.create.camera(...)`
  2. Create render product: `rep.create.render_product(camera, (W, H))`
  3. Writer: `writer = rep.WriterRegistry.get("BasicWriter")`
  4. `writer.initialize(output_dir=..., rgb=True, ...)`
  5. `writer.attach([render_product])`
  6. `rep.orchestrator.run()`
- **Writer API + defaults**
  - `class omni.replicator.core.BasicWriter(output_dir: str, semantic_types: Optional[List[str]] = None, rgb: bool=False, ... image_output_format: str='png', colorize_semantic_segmentation: bool=True, colorize_instance_id_segmentation: bool=True, colorize_instance_segmentation: bool=True, ...)`
  - `write(data: dict)` called every frame; `Writer.on_final_frame()` runs after final frame.
- **Sampling/distributions (named values can be written)**
  - `rep.distribution.uniform(lower, upper, num_samples: int=1, seed: Optional[int]=None, name: Optional[str]=None)`
  - `rep.distribution.normal(mean, std, num_samples: int=1, seed: Optional[int]=None, name: Optional[str]=None)`
  - `rep.distribution.choice(choices: List[str], weights: List[float]=None, num_samples=1, seed=None, with_replacements: bool=True, name=None)`
- **Camera defaults (useful for 3DGS dataset generation)**
  - `rep.create.camera(... focal_length=24.0, focus_distance=400.0, f_stop=0.0, horizontal_aperture=20.955, clipping_range=(1.0, 1000000.0), projection_type='pinhole', ... count: int=1, parent=None)`

## When to surface
Use when students ask how to **set up Omniverse Replicator scripts reproducibly** (layer isolation, default camera parameters) or how to **generate synthetic RGB/GT outputs** via `BasicWriter`, distributions, and `orchestrator.run()`.