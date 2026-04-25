# Card: nerfstudio Cameras & Rays API (intrinsics/extrinsics, distortion, ray gen)
**Source:** https://docs.nerf.studio/reference/api/cameras.html  
**Role:** reference_doc | **Need:** API_REFERENCE  
**Anchor:** Camera model conventions + core API fields for intrinsics/extrinsics, distortion handling, ray generation, pose optimization.

## Key Content
- **Cameras dataclass (per-image camera model):**  
  `Cameras(camera_to_worlds[* 3×4], fx, fy, cx, cy, width, height, distortion_params[* 6], camera_type, times[num_cameras], metadata)`  
  - `camera_to_worlds`: per-image **c2w** matrices in **[R | t]** (3×4).  
  - Intrinsics scalars/tensors: `fx, fy` (focal lengths), `cx, cy` (principal point). Single values are **broadcast** to all cameras.  
  - `distortion_params`: **6 params** in OpenCV order **[k1, k2, k3, k4, p1, p2]** (radial + tangential; also mentions OpenCV “6 radial” / “6-2-4 … thin-prism for Fisheye624”).  
  - `camera_type`: int enum (default **CameraType.PERSPECTIVE**).  
  - `metadata`: broadcast to generated rays / RaySamples for interpolation or conditioning.
- **Intrinsics matrix (pinhole):** `get_intrinsics_matrices() -> K[* 3×3]` built from `(fx, fy, cx, cy)` (standard pinhole K).
- **Pixel coordinate grid:** `get_image_coords(pixel_offset=0.5)` returns `[H, W, 2]` coords; default offset **0.5** = pixel centers.
- **Ray generation workflow:** `generate_rays(camera_indices, coords=None, ..., disable_distortion=False, aabb_box=None, obb_box=None)`  
  - Handles 4 broadcasting cases for `(camera_indices, coords)`; if `coords=None`, renders full image.  
  - **Jagged cameras** (varying H/W): if `coords=None`, coordinate maps can’t stack → **flatten & concatenate** rays.  
  - Optional `aabb_box` computes `nears/fars` via box intersection.
- **Undistortion procedure:** `radial_and_tangential_undistort(coords, distortion_params, eps=0.001, max_iterations=10)` iterative undistort (MultiNeRF-adapted).
- **Pose optimization config:** `CameraOptimizerConfig(mode ∈ {'off','SO3xR3','SE3'} default 'off', trans_l2_penalty=0.01, rot_l2_penalty=0.001)`; recommendation: **SO3xR3**.
- **Ray structures:**  
  - `RayBundle(origins[* 3], directions[* 3] unit, pixel_area[* 1], camera_indices, nears, fars, times, metadata)`  
  - `RaySamples.get_weights(densities)` and `get_weights_and_transmittance_from_alphas(alphas)` for volumetric rendering weights.

## When to surface
Use when students ask how nerfstudio represents cameras (c2w, intrinsics), how distortion is parameterized/disabled/undistorted, how `generate_rays` shapes/broadcasts inputs (including jagged resolutions), or how pose optimization modes/penalties are configured.