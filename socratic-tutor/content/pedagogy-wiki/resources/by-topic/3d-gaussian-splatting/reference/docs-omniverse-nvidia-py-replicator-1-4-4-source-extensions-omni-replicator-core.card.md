# Card: Omniverse Replicator Core API (1.4.4) — layers, creation, distributions, writers
**Source:** https://docs.omniverse.nvidia.com/py/replicator/1.4.4/source/extensions/omni.replicator.core/docs/API.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Documented Replicator API surface + defaults (e.g., `rep.new_layer()` defaults to layer name **"Replicator"**) and core synthetic-data workflow patterns.

## Key Content
- **Layer isolation (authoring context)**
  - `rep.new_layer(name: str=None)`: creates a new authoring layer to contain Replicator changes; if a layer with the same name exists, it is **cleared** before applying new changes.
  - **Default:** if `name` omitted → layer name **"Replicator"**.
  - Pattern: `with rep.new_layer(): ...` (e.g., create 100 cones with random positions).

- **Core synthetic-data workflow (procedure)**
  1. Create camera: `camera = rep.create.camera(...)`
     - Key defaults: `focal_length=24.0`, `focus_distance=400.0`, `f_stop=0.0`, `horizontal_aperture=20.955`, `clipping_range=(1.0, 1000000.0)`, `projection_type='pinhole'`.
  2. Create render product: `render_product = rep.create.render_product(camera, (W,H))` (example uses **(1024,1024)**).
  3. Initialize writer: `writer = rep.WriterRegistry.get("BasicWriter"); writer.initialize(output_dir=..., rgb=True, ...)`
     - `BasicWriter` defaults: `image_output_format='png'`, `frame_padding=4`, `semantic_types=["class"]`.
     - Colorization defaults: `colorize_semantic_segmentation=True`, `colorize_instance_id_segmentation=True`, `colorize_instance_segmentation=True`.
  4. Attach writer: `writer.attach([render_product])`
  5. Run: `rep.orchestrator.run()`; stop via `rep.orchestrator.stop()`.

- **Randomization distributions (parameters)**
  - `rep.distribution.uniform(lower, upper, num_samples=1, seed=None, name=None)`
  - `rep.distribution.normal(mean, std, num_samples=1, seed=None, name=None)`
  - `rep.distribution.choice(choices, weights=None, num_samples=1, seed=None, with_replacements=True, name=None)`
  - **Rationale:** `name` makes distribution values available to the **Writer**.

- **Creation & modification primitives**
  - `rep.create.*` (e.g., `sphere`, `cube`, `cone`, `light`, `from_usd`, `group`, `material_omnipbr`) commonly accept `position/rotation/scale`, `semantics=[("class","label")]`, `count=1`, `visible=True`.
  - `rep.modify.pose(...)`: cannot specify **both** `rotation` and `look_at`; cannot specify **both** `size` and `scale`. Default `rotation_order='XYZ'`.

## When to surface
Use when students ask how to script Omniverse Replicator for synthetic data (camera/render product/writer/run), what defaults apply (layer name, camera params, writer formats), or how to randomize scenes via built-in distributions and semantics.