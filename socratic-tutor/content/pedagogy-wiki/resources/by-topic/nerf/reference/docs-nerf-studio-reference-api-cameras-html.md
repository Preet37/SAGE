# Source: https://docs.nerf.studio/reference/api/cameras.html
# Title: Cameras - nerfstudio
# Fetched via: trafilatura
# Date: 2026-04-09

Cameras[#](#cameras)
Cameras[#](#id2)
Camera Models
-
class nerfstudio.cameras.cameras.Cameras(camera_to_worlds: Float[Tensor, '*batch_c2ws 3 4'], fx: Union[Float[Tensor, '*batch_fxs 1'], float], fy: Union[Float[Tensor, '*batch_fys 1'], float], cx: Union[Float[Tensor, '*batch_cxs 1'], float], cy: Union[Float[Tensor, '*batch_cys 1'], float], width: Optional[Union[Shaped[Tensor, '*batch_ws 1'], int]] = None, height: Optional[Union[Shaped[Tensor, '*batch_hs 1'], int]] = None, distortion_params: Optional[Float[Tensor, '*batch_dist_params 6']] = None, camera_type: Union[Int[Tensor, '*batch_cam_types 1'], int, List[
[CameraType](#nerfstudio.cameras.cameras.CameraType)],[CameraType](#nerfstudio.cameras.cameras.CameraType)] = CameraType.PERSPECTIVE, times: Optional[Float[Tensor, 'num_cameras']] = None, metadata: Optional[Dict] = None)[[source]](../../_modules/nerfstudio/cameras/cameras.html#Cameras)[#](#nerfstudio.cameras.cameras.Cameras) Bases:
TensorDataclass
Dataparser outputs for the image dataset and the ray generator.
If a single value is provided, it is broadcasted to all cameras.
- Parameters:
camera_to_worlds – Camera to world matrices. Tensor of per-image c2w matrices, in [R | t] format
fx – Focal length x
fy – Focal length y
cx – Principal point x
cy – Principal point y
width – Image width
height – Image height
distortion_params – distortion coefficients (OpenCV 6 radial or 6-2-4 radial, tangential, thin-prism for Fisheye624)
camera_type – Type of camera model. This will be an int corresponding to the CameraType enum.
times – Timestamps for each camera
metadata – Additional metadata or data needed for interpolation, will mimic shape of the cameras and will be broadcasted to the rays generated from any derivative RaySamples we create with this
-
property device: Union[device, str]
[#](#nerfstudio.cameras.cameras.Cameras.device) Returns the device that the camera is on.
-
generate_rays(camera_indices: Union[Int[Tensor, '*num_rays num_cameras_batch_dims'], int], coords: Optional[Float[Tensor, '*num_rays 2']] = None, camera_opt_to_camera: Optional[Float[Tensor, '*num_rays 3 4']] = None, distortion_params_delta: Optional[Float[Tensor, '*num_rays 6']] = None, keep_shape: Optional[bool] = None, disable_distortion: bool = False, aabb_box: Optional[
[SceneBox](data/index.html#nerfstudio.data.scene_box.SceneBox)] = None, obb_box: Optional[[OrientedBox](data/index.html#nerfstudio.data.scene_box.OrientedBox)] = None)[RayBundle](#nerfstudio.cameras.rays.RayBundle)[[source]](../../_modules/nerfstudio/cameras/cameras.html#Cameras.generate_rays)[#](#nerfstudio.cameras.cameras.Cameras.generate_rays) Generates rays for the given camera indices.
This function will standardize the input arguments and then call the _generate_rays_from_coords function to generate the rays. Our goal is to parse the arguments and then get them into the right shape:
camera_indices: (num_rays:…, num_cameras_batch_dims)
coords: (num_rays:…, 2)
camera_opt_to_camera: (num_rays:…, 3, 4) or None
distortion_params_delta: (num_rays:…, 6) or None
Read the docstring for _generate_rays_from_coords for more information on how we generate the rays after we have standardized the arguments.
We are only concerned about different combinations of camera_indices and coords matrices, and the following are the 4 cases we have to deal with:
- isinstance(camera_indices, int) and coords == None
In this case we broadcast our camera_indices / coords shape (h, w, 1 / 2 respectively)
- isinstance(camera_indices, int) and coords != None
In this case, we broadcast camera_indices to the same batch dim as coords
- not isinstance(camera_indices, int) and coords == None
- In this case, we will need to set coords so that it is of shape (h, w, num_rays, 2), and broadcast
all our other args to match the new definition of num_rays := (h, w) + num_rays
- not isinstance(camera_indices, int) and coords != None
In this case, we have nothing to do, only check that the arguments are of the correct shape
There is one more edge case we need to be careful with: when we have “jagged cameras” (ie: different heights and widths for each camera). This isn’t problematic when we specify coords, since coords is already a tensor. When coords == None (ie: when we render out the whole image associated with this camera), we run into problems since there’s no way to stack each coordinate map as all coordinate maps are all different shapes. In this case, we will need to flatten each individual coordinate map and concatenate them, giving us only one batch dimension, regardless of the number of prepended extra batch dimensions in the camera_indices tensor.
- Parameters:
camera_indices – Camera indices of the flattened cameras object to generate rays for.
coords – Coordinates of the pixels to generate rays for. If None, the full image will be rendered.
camera_opt_to_camera – Optional transform for the camera to world matrices.
distortion_params_delta – Optional delta for the distortion parameters.
keep_shape – If None, then we default to the regular behavior of flattening if cameras is jagged, otherwise keeping dimensions. If False, we flatten at the end. If True, then we keep the shape of the camera_indices and coords tensors (if we can).
disable_distortion – If True, disables distortion.
aabb_box – if not None will calculate nears and fars of the ray according to aabb box intersection
- Returns:
Rays for the given camera indices and coords.
-
get_image_coords(pixel_offset: float = 0.5, index: Optional[Tuple] = None) Float[Tensor, 'height width 2']
[[source]](../../_modules/nerfstudio/cameras/cameras.html#Cameras.get_image_coords)[#](#nerfstudio.cameras.cameras.Cameras.get_image_coords) This gets the image coordinates of one of the cameras in this object.
If no index is specified, it will return the maximum possible sized height / width image coordinate map, by looking at the maximum height and width of all the cameras in this object.
- Parameters:
pixel_offset – Offset for each pixel. Defaults to center of pixel (0.5)
index – Tuple of indices into the batch dimensions of the camera. Defaults to None, which returns the 0th flattened camera
- Returns:
Grid of image coordinates.
-
get_intrinsics_matrices() Float[Tensor, '*num_cameras 3 3']
[[source]](../../_modules/nerfstudio/cameras/cameras.html#Cameras.get_intrinsics_matrices)[#](#nerfstudio.cameras.cameras.Cameras.get_intrinsics_matrices) Returns the intrinsic matrices for each camera.
- Returns:
Pinhole camera intrinsics matrices
-
property image_height: Shaped[Tensor, '*num_cameras 1']
[#](#nerfstudio.cameras.cameras.Cameras.image_height) Returns the height of the images.
-
property image_width: Shaped[Tensor, '*num_cameras 1']
[#](#nerfstudio.cameras.cameras.Cameras.image_width) Returns the height of the images.
-
property is_jagged: bool
[#](#nerfstudio.cameras.cameras.Cameras.is_jagged) Returns whether or not the cameras are “jagged” (i.e. the height and widths are different, meaning that you cannot concatenate the image coordinate maps together)
-
rescale_output_resolution(scaling_factor: Union[Shaped[Tensor, '*num_cameras'], Shaped[Tensor, '*num_cameras 1'], float, int], scale_rounding_mode: str = 'floor') None
[[source]](../../_modules/nerfstudio/cameras/cameras.html#Cameras.rescale_output_resolution)[#](#nerfstudio.cameras.cameras.Cameras.rescale_output_resolution) Rescale the output resolution of the cameras.
- Parameters:
scaling_factor – Scaling factor to apply to the output resolution.
scale_rounding_mode – round down or round up when calculating the scaled image height and width
-
to_json(camera_idx: int, image: Optional[Float[Tensor, 'height width 2']] = None, max_size: Optional[int] = None) Dict
[[source]](../../_modules/nerfstudio/cameras/cameras.html#Cameras.to_json)[#](#nerfstudio.cameras.cameras.Cameras.to_json) Convert a camera to a json dictionary.
- Parameters:
camera_idx – Index of the camera to convert.
image – An image in range [0, 1] that is encoded to a base64 string.
max_size – Max size to resize the image to if present.
- Returns:
A JSON representation of the camera
Camera Optimizers[#](#camera-optimizers)
Pose and Intrinsics Optimizers
-
class nerfstudio.cameras.camera_optimizers.CameraOptimizer(config:
[CameraOptimizerConfig](#nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig), num_cameras: int, device: Union[device, str], non_trainable_camera_indices: Optional[Int[Tensor, 'num_non_trainable_cameras']] = None, **kwargs)[[source]](../../_modules/nerfstudio/cameras/camera_optimizers.html#CameraOptimizer)[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizer) Bases:
Module
Layer that modifies camera poses to be optimized as well as the field during training.
-
apply_to_camera(camera:
[Cameras](#nerfstudio.cameras.cameras.Cameras)) Tensor[[source]](../../_modules/nerfstudio/cameras/camera_optimizers.html#CameraOptimizer.apply_to_camera)[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizer.apply_to_camera) Apply the pose correction to the world-to-camera matrix in a Camera object
-
apply_to_camera(camera:
-
class nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig(_target: ~typing.Type = <factory>, mode: ~typing.Literal['off', 'SO3xR3', 'SE3'] = 'off', trans_l2_penalty: float = 0.01, rot_l2_penalty: float = 0.001, optimizer: ~typing.Optional[~nerfstudio.engine.optimizers.OptimizerConfig] = None, scheduler: ~typing.Optional[~nerfstudio.engine.schedulers.SchedulerConfig] = None)
[[source]](../../_modules/nerfstudio/cameras/camera_optimizers.html#CameraOptimizerConfig)[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig) Bases:
InstantiateConfig
Configuration of optimization for camera poses.
-
mode: Literal['off', 'SO3xR3', 'SE3'] = 'off'
[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig.mode) Pose optimization strategy to use. If enabled, we recommend SO3xR3.
-
optimizer: Optional[
[OptimizerConfig](optimizers.html#nerfstudio.engine.optimizers.OptimizerConfig)] = None[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig.optimizer) Deprecated, now specified inside the optimizers dict
-
rot_l2_penalty: float = 0.001
[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig.rot_l2_penalty) L2 penalty on rotation parameters.
-
scheduler: Optional[
[SchedulerConfig](optimizers.html#nerfstudio.engine.schedulers.SchedulerConfig)] = None[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig.scheduler) Deprecated, now specified inside the optimizers dict
-
trans_l2_penalty: float = 0.01
[#](#nerfstudio.cameras.camera_optimizers.CameraOptimizerConfig.trans_l2_penalty) L2 penalty on translation parameters.
-
mode: Literal['off', 'SO3xR3', 'SE3'] = 'off'
Camera Paths[#](#camera-paths)
Code for camera paths.
-
nerfstudio.cameras.camera_paths.get_interpolated_camera_path(cameras:
[Cameras](#nerfstudio.cameras.cameras.Cameras), steps: int, order_poses: bool)[Cameras](#nerfstudio.cameras.cameras.Cameras)[[source]](../../_modules/nerfstudio/cameras/camera_paths.html#get_interpolated_camera_path)[#](#nerfstudio.cameras.camera_paths.get_interpolated_camera_path) Generate a camera path between two cameras. Uses the camera type of the first camera
- Parameters:
cameras – Cameras object containing intrinsics of all cameras.
steps – The number of steps to interpolate between the two cameras.
- Returns:
A new set of cameras along a path.
-
nerfstudio.cameras.camera_paths.get_path_from_json(camera_path: Dict[str, Any])
[Cameras](#nerfstudio.cameras.cameras.Cameras)[[source]](../../_modules/nerfstudio/cameras/camera_paths.html#get_path_from_json)[#](#nerfstudio.cameras.camera_paths.get_path_from_json) Takes a camera path dictionary and returns a trajectory as a Camera instance.
- Parameters:
camera_path – A dictionary of the camera path information coming from the viewer.
- Returns:
A Cameras instance with the camera path.
-
nerfstudio.cameras.camera_paths.get_spiral_path(camera:
[Cameras](#nerfstudio.cameras.cameras.Cameras), steps: int = 30, radius: Optional[float] = None, radiuses: Optional[Tuple[float]] = None, rots: int = 2, zrate: float = 0.5)[Cameras](#nerfstudio.cameras.cameras.Cameras)[[source]](../../_modules/nerfstudio/cameras/camera_paths.html#get_spiral_path)[#](#nerfstudio.cameras.camera_paths.get_spiral_path) Returns a list of camera in a spiral trajectory.
- Parameters:
camera – The camera to start the spiral from.
steps – The number of cameras in the generated path.
radius – The radius of the spiral for all xyz directions.
radiuses – The list of radii for the spiral in xyz directions.
rots – The number of rotations to apply to the camera.
zrate – How much to change the z position of the camera.
- Returns:
A spiral camera path.
Camera Utils[#](#camera-utils)
Camera transformation helper code.
-
nerfstudio.cameras.camera_utils.auto_orient_and_center_poses(poses: Float[Tensor, '*num_poses 4 4'], method: Literal['pca', 'up', 'vertical', 'none'] = 'up', center_method: Literal['poses', 'focus', 'none'] = 'poses') Tuple[Float[Tensor, '*num_poses 3 4'], Float[Tensor, '3 4']]
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#auto_orient_and_center_poses)[#](#nerfstudio.cameras.camera_utils.auto_orient_and_center_poses) Orients and centers the poses.
We provide three methods for orientation:
- pca: Orient the poses so that the principal directions of the camera centers are aligned
with the axes, Z corresponding to the smallest principal component. This method works well when all of the cameras are in the same plane, for example when images are taken using a mobile robot.
- up: Orient the poses so that the average up vector is aligned with the z axis.
This method works well when images are not at arbitrary angles.
- vertical: Orient the poses so that the Z 3D direction projects close to the
y axis in images. This method works better if cameras are not all looking in the same 3D direction, which may happen in camera arrays or in LLFF.
There are two centering methods:
poses: The poses are centered around the origin.
- focus: The origin is set to the focus of attention of all cameras (the
closest point to cameras optical axes). Recommended for inward-looking camera configurations.
- Parameters:
poses – The poses to orient.
method – The method to use for orientation.
center_method – The method to use to center the poses.
- Returns:
Tuple of the oriented poses and the transform matrix.
-
nerfstudio.cameras.camera_utils.focus_of_attention(poses: Float[Tensor, '*num_poses 4 4'], initial_focus: Float[Tensor, '3']) Float[Tensor, '3']
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#focus_of_attention)[#](#nerfstudio.cameras.camera_utils.focus_of_attention) Compute the focus of attention of a set of cameras. Only cameras that have the focus of attention in front of them are considered.
- Args:
poses: The poses to orient. initial_focus: The 3D point views to decide which cameras are initially activated.
- Returns:
The 3D position of the focus of attention.
-
nerfstudio.cameras.camera_utils.get_distortion_params(k1: float = 0.0, k2: float = 0.0, k3: float = 0.0, k4: float = 0.0, p1: float = 0.0, p2: float = 0.0) Float[Tensor, '*batch']
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#get_distortion_params)[#](#nerfstudio.cameras.camera_utils.get_distortion_params) Returns a distortion parameters matrix.
- Parameters:
k1 – The first radial distortion parameter.
k2 – The second radial distortion parameter.
k3 – The third radial distortion parameter.
k4 – The fourth radial distortion parameter.
p1 – The first tangential distortion parameter.
p2 – The second tangential distortion parameter.
- Returns:
A distortion parameters matrix.
- Return type:
torch.Tensor
-
nerfstudio.cameras.camera_utils.get_interpolated_k(k_a: Float[Tensor, '3 3'], k_b: Float[Tensor, '3 3'], steps: int = 10) List[Float[Tensor, '3 4']]
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#get_interpolated_k)[#](#nerfstudio.cameras.camera_utils.get_interpolated_k) Returns interpolated path between two camera poses with specified number of steps.
- Parameters:
k_a – camera matrix 1
k_b – camera matrix 2
steps – number of steps the interpolated pose path should contain
- Returns:
List of interpolated camera poses
-
nerfstudio.cameras.camera_utils.get_interpolated_poses(pose_a: ndarray[Any, dtype[_ScalarType_co]], pose_b: ndarray[Any, dtype[_ScalarType_co]], steps: int = 10) List[float]
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#get_interpolated_poses)[#](#nerfstudio.cameras.camera_utils.get_interpolated_poses) Return interpolation of poses with specified number of steps. :param pose_a: first pose :param pose_b: second pose :param steps: number of steps the interpolated pose path should contain
-
nerfstudio.cameras.camera_utils.get_interpolated_poses_many(poses: Float[Tensor, 'num_poses 3 4'], Ks: Float[Tensor, 'num_poses 3 3'], times: Optional[Float[Tensor, 'num_poses 1']] = None, steps_per_transition: int = 10, order_poses: bool = False) Tuple[Float[Tensor, 'num_poses 3 4'], Float[Tensor, 'num_poses 3 3'], Optional[Float[Tensor, 'num_poses 1']]]
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#get_interpolated_poses_many)[#](#nerfstudio.cameras.camera_utils.get_interpolated_poses_many) Return interpolated poses for many camera poses.
- Parameters:
poses – list of camera poses
Ks – list of camera intrinsics
steps_per_transition – number of steps per transition
order_poses – whether to order poses by euclidian distance
- Returns:
tuple of new poses and intrinsics
-
nerfstudio.cameras.camera_utils.get_interpolated_time(time_a: Float[Tensor, '1'], time_b: Float[Tensor, '1'], steps: int = 10) List[Float[Tensor, '1']]
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#get_interpolated_time)[#](#nerfstudio.cameras.camera_utils.get_interpolated_time) Returns interpolated time between two camera poses with specified number of steps.
- Parameters:
time_a – camera time 1
time_b – camera time 2
steps – number of steps the interpolated pose path should contain
-
nerfstudio.cameras.camera_utils.get_ordered_poses_and_k_and_time(poses: Float[Tensor, 'num_poses 3 4'], Ks: Float[Tensor, 'num_poses 3 3'], times: Optional[Float[Tensor, 'num_poses 1']] = None) Tuple[Float[Tensor, 'num_poses 3 4'], Float[Tensor, 'num_poses 3 3'], Optional[Float[Tensor, 'num_poses 1']]]
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#get_ordered_poses_and_k_and_time)[#](#nerfstudio.cameras.camera_utils.get_ordered_poses_and_k_and_time) Returns ordered poses and intrinsics by euclidian distance between poses.
- Parameters:
poses – list of camera poses
Ks – list of camera intrinsics
times – list of camera times
- Returns:
tuple of ordered poses, intrinsics and times
-
nerfstudio.cameras.camera_utils.normalize(x: Tensor) Float[Tensor, '*batch']
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#normalize)[#](#nerfstudio.cameras.camera_utils.normalize) Returns a normalized vector.
-
nerfstudio.cameras.camera_utils.normalize_with_norm(x: Tensor, dim: int) Tuple[Tensor, Tensor]
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#normalize_with_norm)[#](#nerfstudio.cameras.camera_utils.normalize_with_norm) Normalize tensor along axis and return normalized value with norms.
- Parameters:
x – tensor to normalize.
dim – axis along which to normalize.
- Returns:
Tuple of normalized tensor and corresponding norm.
-
nerfstudio.cameras.camera_utils.quaternion_from_matrix(matrix: ndarray[Any, dtype[_ScalarType_co]], isprecise: bool = False) ndarray
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#quaternion_from_matrix)[#](#nerfstudio.cameras.camera_utils.quaternion_from_matrix) Return quaternion from rotation matrix.
- Parameters:
matrix – rotation matrix to obtain quaternion
isprecise – if True, input matrix is assumed to be precise rotation matrix and a faster algorithm is used.
-
nerfstudio.cameras.camera_utils.quaternion_matrix(quaternion: ndarray[Any, dtype[_ScalarType_co]]) ndarray
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#quaternion_matrix)[#](#nerfstudio.cameras.camera_utils.quaternion_matrix) Return homogeneous rotation matrix from quaternion.
- Parameters:
quaternion – value to convert to matrix
-
nerfstudio.cameras.camera_utils.quaternion_slerp(quat0: ndarray[Any, dtype[_ScalarType_co]], quat1: ndarray[Any, dtype[_ScalarType_co]], fraction: float, spin: int = 0, shortestpath: bool = True) ndarray
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#quaternion_slerp)[#](#nerfstudio.cameras.camera_utils.quaternion_slerp) Return spherical linear interpolation between two quaternions. :param quat0: first quaternion :param quat1: second quaternion :param fraction: how much to interpolate between quat0 vs quat1 (if 0, closer to quat0; if 1, closer to quat1) :param spin: how much of an additional spin to place on the interpolation :param shortestpath: whether to return the short or long path to rotation
-
nerfstudio.cameras.camera_utils.radial_and_tangential_undistort(coords: Tensor, distortion_params: Tensor, eps: float = 0.001, max_iterations: int = 10) Tensor
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#radial_and_tangential_undistort)[#](#nerfstudio.cameras.camera_utils.radial_and_tangential_undistort) Computes undistorted coords given opencv distortion parameters. Adapted from MultiNeRF
[https://github.com/google-research/multinerf/blob/b02228160d3179300c7d499dca28cb9ca3677f32/internal/camera_utils.py#L477-L509](https://github.com/google-research/multinerf/blob/b02228160d3179300c7d499dca28cb9ca3677f32/internal/camera_utils.py#L477-L509)- Parameters:
coords – The distorted coordinates.
distortion_params – The distortion parameters [k1, k2, k3, k4, p1, p2].
eps – The epsilon for the convergence.
max_iterations – The maximum number of iterations to perform.
- Returns:
The undistorted coordinates.
-
nerfstudio.cameras.camera_utils.rotation_matrix_between(a: Float[Tensor, '3'], b: Float[Tensor, '3']) Float[Tensor, '3 3']
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#rotation_matrix_between)[#](#nerfstudio.cameras.camera_utils.rotation_matrix_between) Compute the rotation matrix that rotates vector a to vector b.
- Parameters:
a – The vector to rotate.
b – The vector to rotate to.
- Returns:
The rotation matrix.
-
nerfstudio.cameras.camera_utils.unit_vector(data: ndarray[Any, dtype[_ScalarType_co]], axis: Optional[int] = None) ndarray
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#unit_vector)[#](#nerfstudio.cameras.camera_utils.unit_vector) Return ndarray normalized by length, i.e. Euclidean norm, along axis.
- Parameters:
axis – the axis along which to normalize into unit vector
out – where to write out the data to. If None, returns a new np ndarray
-
nerfstudio.cameras.camera_utils.viewmatrix(lookat: Tensor, up: Tensor, pos: Tensor) Float[Tensor, '*batch']
[[source]](../../_modules/nerfstudio/cameras/camera_utils.html#viewmatrix)[#](#nerfstudio.cameras.camera_utils.viewmatrix) Returns a camera transformation matrix.
- Parameters:
lookat – The direction the camera is looking.
up – The upward direction of the camera.
pos – The position of the camera.
- Returns:
A camera transformation matrix.
Lie Groups[#](#lie-groups)
Helper for Lie group operations. Currently only used for pose optimization.
-
nerfstudio.cameras.lie_groups.exp_map_SE3(tangent_vector: Float[Tensor, 'b 6']) Float[Tensor, 'b 3 4']
[[source]](../../_modules/nerfstudio/cameras/lie_groups.html#exp_map_SE3)[#](#nerfstudio.cameras.lie_groups.exp_map_SE3) Compute the exponential map se(3) -> SE(3).
This can be used for learning pose deltas on SE(3).
- Parameters:
tangent_vector – A tangent vector from se(3).
- Returns:
[R|t] transformation matrices.
-
nerfstudio.cameras.lie_groups.exp_map_SO3xR3(tangent_vector: Float[Tensor, 'b 6']) Float[Tensor, 'b 3 4']
[[source]](../../_modules/nerfstudio/cameras/lie_groups.html#exp_map_SO3xR3)[#](#nerfstudio.cameras.lie_groups.exp_map_SO3xR3) Compute the exponential map of the direct product group SO(3) x R^3.
This can be used for learning pose deltas on SE(3), and is generally faster than exp_map_SE3.
- Parameters:
tangent_vector – Tangent vector; length-3 translations, followed by an so(3) tangent vector.
- Returns:
[R|t] transformation matrices.
Rays[#](#rays)
Some ray datastructures.
-
class nerfstudio.cameras.rays.Frustums(origins: Float[Tensor, '*bs 3'], directions: Float[Tensor, '*bs 3'], starts: Float[Tensor, '*bs 1'], ends: Float[Tensor, '*bs 1'], pixel_area: Float[Tensor, '*bs 1'], offsets: Optional[Float[Tensor, '*bs 3']] = None)
[[source]](../../_modules/nerfstudio/cameras/rays.html#Frustums)[#](#nerfstudio.cameras.rays.Frustums) Bases:
TensorDataclass
Describes region of space as a frustum.
-
directions: Float[Tensor, '*bs 3']
[#](#nerfstudio.cameras.rays.Frustums.directions) Direction of ray.
-
ends: Float[Tensor, '*bs 1']
[#](#nerfstudio.cameras.rays.Frustums.ends) Where the frustum ends along a ray.
-
get_gaussian_blob()
[Gaussians](utils/math.html#nerfstudio.utils.math.Gaussians)[[source]](../../_modules/nerfstudio/cameras/rays.html#Frustums.get_gaussian_blob)[#](#nerfstudio.cameras.rays.Frustums.get_gaussian_blob) Calculates guassian approximation of conical frustum.
- Returns:
Conical frustums approximated by gaussian distribution.
-
classmethod get_mock_frustum(device: Optional[Union[str, device]] = 'cpu')
[Frustums](#nerfstudio.cameras.rays.Frustums)[[source]](../../_modules/nerfstudio/cameras/rays.html#Frustums.get_mock_frustum)[#](#nerfstudio.cameras.rays.Frustums.get_mock_frustum) Helper function to generate a placeholder frustum.
- Returns:
A size 1 frustum with meaningless values.
-
get_positions() Float[Tensor, '*batch 3']
[[source]](../../_modules/nerfstudio/cameras/rays.html#Frustums.get_positions)[#](#nerfstudio.cameras.rays.Frustums.get_positions) Calculates “center” position of frustum. Not weighted by mass.
- Returns:
xyz positions.
-
get_start_positions() Float[Tensor, '*batch 3']
[[source]](../../_modules/nerfstudio/cameras/rays.html#Frustums.get_start_positions)[#](#nerfstudio.cameras.rays.Frustums.get_start_positions) Calculates “start” position of frustum.
- Returns:
xyz positions.
-
offsets: Optional[Float[Tensor, '*bs 3']] = None
[#](#nerfstudio.cameras.rays.Frustums.offsets) Offsets for each sample position
-
origins: Float[Tensor, '*bs 3']
[#](#nerfstudio.cameras.rays.Frustums.origins) xyz coordinate for ray origin.
-
pixel_area: Float[Tensor, '*bs 1']
[#](#nerfstudio.cameras.rays.Frustums.pixel_area) Projected area of pixel a distance 1 away from origin.
-
starts: Float[Tensor, '*bs 1']
[#](#nerfstudio.cameras.rays.Frustums.starts) Where the frustum starts along a ray.
-
directions: Float[Tensor, '*bs 3']
-
class nerfstudio.cameras.rays.RayBundle(origins: ~jaxtyping.Float[Tensor, '*batch 3'], directions: ~jaxtyping.Float[Tensor, '*batch 3'], pixel_area: ~jaxtyping.Float[Tensor, '*batch 1'], camera_indices: ~typing.Optional[~jaxtyping.Int[Tensor, '*batch 1']] = None, nears: ~typing.Optional[~jaxtyping.Float[Tensor, '*batch 1']] = None, fars: ~typing.Optional[~jaxtyping.Float[Tensor, '*batch 1']] = None, metadata: ~typing.Dict[str, ~jaxtyping.Shaped[Tensor, 'num_rays latent_dims']] = <factory>, times: ~typing.Optional[~jaxtyping.Float[Tensor, '*batch 1']] = None)
[[source]](../../_modules/nerfstudio/cameras/rays.html#RayBundle)[#](#nerfstudio.cameras.rays.RayBundle) Bases:
TensorDataclass
A bundle of ray parameters.
-
camera_indices: Optional[Int[Tensor, '*batch 1']] = None
[#](#nerfstudio.cameras.rays.RayBundle.camera_indices) Camera indices
-
directions: Float[Tensor, '*batch 3']
[#](#nerfstudio.cameras.rays.RayBundle.directions) Unit ray direction vector
-
fars: Optional[Float[Tensor, '*batch 1']] = None
[#](#nerfstudio.cameras.rays.RayBundle.fars) Rays Distance along ray to stop sampling
-
get_ray_samples(bin_starts: Float[Tensor, '*bs num_samples 1'], bin_ends: Float[Tensor, '*bs num_samples 1'], spacing_starts: Optional[Float[Tensor, '*bs num_samples 1']] = None, spacing_ends: Optional[Float[Tensor, '*bs num_samples 1']] = None, spacing_to_euclidean_fn: Optional[Callable] = None)
[RaySamples](#nerfstudio.cameras.rays.RaySamples)[[source]](../../_modules/nerfstudio/cameras/rays.html#RayBundle.get_ray_samples)[#](#nerfstudio.cameras.rays.RayBundle.get_ray_samples) Produces samples for each ray by projection points along the ray direction. Currently samples uniformly.
- Parameters:
bin_starts – Distance from origin to start of bin.
bin_ends – Distance from origin to end of bin.
- Returns:
Samples projected along ray.
-
get_row_major_sliced_ray_bundle(start_idx: int, end_idx: int)
[RayBundle](#nerfstudio.cameras.rays.RayBundle)[[source]](../../_modules/nerfstudio/cameras/rays.html#RayBundle.get_row_major_sliced_ray_bundle)[#](#nerfstudio.cameras.rays.RayBundle.get_row_major_sliced_ray_bundle) Flattens RayBundle and extracts chunk given start and end indices.
- Parameters:
start_idx – Start index of RayBundle chunk.
end_idx – End index of RayBundle chunk.
- Returns:
Flattened RayBundle with end_idx-start_idx rays.
-
metadata: Dict[str, Shaped[Tensor, 'num_rays latent_dims']]
[#](#nerfstudio.cameras.rays.RayBundle.metadata) Additional metadata or data needed for interpolation, will mimic shape of rays
-
nears: Optional[Float[Tensor, '*batch 1']] = None
[#](#nerfstudio.cameras.rays.RayBundle.nears) Distance along ray to start sampling
-
origins: Float[Tensor, '*batch 3']
[#](#nerfstudio.cameras.rays.RayBundle.origins) Ray origins (XYZ)
-
pixel_area: Float[Tensor, '*batch 1']
[#](#nerfstudio.cameras.rays.RayBundle.pixel_area) Projected area of pixel a distance 1 away from origin
-
sample(num_rays: int)
[RayBundle](#nerfstudio.cameras.rays.RayBundle)[[source]](../../_modules/nerfstudio/cameras/rays.html#RayBundle.sample)[#](#nerfstudio.cameras.rays.RayBundle.sample) Returns a RayBundle as a subset of rays.
- Parameters:
num_rays – Number of rays in output RayBundle
- Returns:
RayBundle with subset of rays.
-
set_camera_indices(camera_index: int) None
[[source]](../../_modules/nerfstudio/cameras/rays.html#RayBundle.set_camera_indices)[#](#nerfstudio.cameras.rays.RayBundle.set_camera_indices) Sets all the camera indices to a specific camera index.
- Parameters:
camera_index – Camera index.
-
times: Optional[Float[Tensor, '*batch 1']] = None
[#](#nerfstudio.cameras.rays.RayBundle.times) Times at which rays are sampled
-
camera_indices: Optional[Int[Tensor, '*batch 1']] = None
-
class nerfstudio.cameras.rays.RaySamples(frustums:
[Frustums](#nerfstudio.cameras.rays.Frustums), camera_indices: Optional[Int[Tensor, '*bs 1']] = None, deltas: Optional[Float[Tensor, '*bs 1']] = None, spacing_starts: Optional[Float[Tensor, '*bs num_samples 1']] = None, spacing_ends: Optional[Float[Tensor, '*bs num_samples 1']] = None, spacing_to_euclidean_fn: Optional[Callable] = None, metadata: Optional[Dict[str, Shaped[Tensor, '*bs latent_dims']]] = None, times: Optional[Float[Tensor, '*batch 1']] = None)[[source]](../../_modules/nerfstudio/cameras/rays.html#RaySamples)[#](#nerfstudio.cameras.rays.RaySamples) Bases:
TensorDataclass
Samples along a ray
-
camera_indices: Optional[Int[Tensor, '*bs 1']] = None
[#](#nerfstudio.cameras.rays.RaySamples.camera_indices) Camera index.
-
deltas: Optional[Float[Tensor, '*bs 1']] = None
[#](#nerfstudio.cameras.rays.RaySamples.deltas) “width” of each sample.
-
get_weights(densities: Float[Tensor, '*batch num_samples 1']) Float[Tensor, '*batch num_samples 1']
[[source]](../../_modules/nerfstudio/cameras/rays.html#RaySamples.get_weights)[#](#nerfstudio.cameras.rays.RaySamples.get_weights) Return weights based on predicted densities
- Parameters:
densities – Predicted densities for samples along ray
- Returns:
Weights for each sample
-
[[source]](../../_modules/nerfstudio/cameras/rays.html#RaySamples.get_weights_and_transmittance_from_alphas)[#](#nerfstudio.cameras.rays.RaySamples.get_weights_and_transmittance_from_alphas) - static get_weights_and_transmittance_from_alphas(alphas: Float[Tensor, '*batch num_samples 1'], weights_only: Literal[False] = False) Tuple[Float[Tensor, '*batch num_samples 1'], Float[Tensor, '*batch num_samples 1']]
Return weights based on predicted alphas :param alphas: Predicted alphas (maybe from sdf) for samples along ray :param weights_only: If function should return only weights
- Returns:
Tuple of weights and transmittance for each sample
-
metadata: Optional[Dict[str, Shaped[Tensor, '*bs latent_dims']]] = None
[#](#nerfstudio.cameras.rays.RaySamples.metadata) additional information relevant to generating ray samples
-
spacing_ends: Optional[Float[Tensor, '*bs num_samples 1']] = None
[#](#nerfstudio.cameras.rays.RaySamples.spacing_ends) Start of normalized bin edges along ray [0,1], before warping is applied, ie. linear in disparity sampling.
-
spacing_starts: Optional[Float[Tensor, '*bs num_samples 1']] = None
[#](#nerfstudio.cameras.rays.RaySamples.spacing_starts) Start of normalized bin edges along ray [0,1], before warping is applied, ie. linear in disparity sampling.
-
spacing_to_euclidean_fn: Optional[Callable] = None
[#](#nerfstudio.cameras.rays.RaySamples.spacing_to_euclidean_fn) Function to convert bins to euclidean distance.
-
times: Optional[Float[Tensor, '*batch 1']] = None
[#](#nerfstudio.cameras.rays.RaySamples.times) Times at which rays are sampled
-
camera_indices: Optional[Int[Tensor, '*bs 1']] = None