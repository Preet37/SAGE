# Source: https://docs.omniverse.nvidia.com/py/replicator/1.4.4/source/extensions/omni.replicator.core/docs/API.html
# Title: API — omni_replicator 1.4.4 documentation
# Fetched via: trafilatura
# Date: 2026-04-09

API[¶](#api)
Core Functions[¶](#module-omni.replicator.core)
-
omni.replicator.core.
new_layer
(name:[str](https://docs.python.org/3/library/stdtypes.html#str)= None)[¶](#omni.replicator.core.new_layer) Create a new authoring layer context. Use new_layer to keep replicator changes into a contained layer. If a layer of the same name already exists, the layer will be cleared before new changes are applied.
- Parameters
name – Name of the layer to be created. If ommitted, the name “Replicator” is used.
Example
>>> import omni.replicator.core as rep >>> with rep.new_layer(): >>> rep.create.cone(count=100, position=rep.distribution.uniform((-100,-100,-100),(100,100,100)))
Annotators[¶](#annotators)
-
class
omni.replicator.core.
AnnotatorRegistry
Registry of annotators providing groundtruth data to writers.
-
register_annotator_from_aov
() →[None](https://docs.python.org/3/library/constants.html#None) Register annotator from an Arbitrary Output Variable (AOV).
- Parameters
aov – AOV name
-
classmethod
register_annotator_from_node
(name:[str](https://docs.python.org/3/library/stdtypes.html#str), input_rendervars: List[Union[[str](https://docs.python.org/3/library/stdtypes.html#str),[list](https://docs.python.org/3/library/stdtypes.html#list), omni.syntheticdata.SyntheticData.NodeConnectionTemplate]], node_type_id:[str](https://docs.python.org/3/library/stdtypes.html#str), init_params: Optional[[dict](https://docs.python.org/3/library/stdtypes.html#dict)] = None, render_product_idxs:[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)= (0), output_rendervars: Optional[List[Union[[str](https://docs.python.org/3/library/stdtypes.html#str),[list](https://docs.python.org/3/library/stdtypes.html#list)]]] = None, output_data_type: Optional[Any] = None, output_is_2d:[bool](https://docs.python.org/3/library/functions.html#bool)= False, output_channels:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.replicator.core.scripts.annotator_registry.AnnotatorTemplate Register annotator from an omnigraph node definition.
- Parameters
name – Annotator name. This name will be used to retrieve the annotator from the registry and will be used as the key in the data dictionary provided to the writer.
input_rendervars – List of rendervars or other nodes that supply inputs to the node.
node_type_id – Node type ID
init_params – Set node attributes to static values
render_product_idxs – Index of render prodcuts to utilize.
output_rendervars – Specifies the render vars output by the node.
output_data_type – Specifies the output data type.
output_is_2d – Set to True if output is a 2D array
output_channels – Specifies the number of output channels of the array. Ignored if
output_is_2d
is set toFalse
.
-
Writers[¶](#writers)
-
class
omni.replicator.core.
BasicWriter
(output_dir:[str](https://docs.python.org/3/library/stdtypes.html#str), semantic_types: Optional[List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, rgb:[bool](https://docs.python.org/3/library/functions.html#bool)= False, bounding_box_2d_tight:[bool](https://docs.python.org/3/library/functions.html#bool)= False, bounding_box_2d_loose:[bool](https://docs.python.org/3/library/functions.html#bool)= False, semantic_segmentation:[bool](https://docs.python.org/3/library/functions.html#bool)= False, instance_id_segmentation:[bool](https://docs.python.org/3/library/functions.html#bool)= False, instance_segmentation:[bool](https://docs.python.org/3/library/functions.html#bool)= False, distance_to_camera:[bool](https://docs.python.org/3/library/functions.html#bool)= False, distance_to_image_plane:[bool](https://docs.python.org/3/library/functions.html#bool)= False, bounding_box_3d:[bool](https://docs.python.org/3/library/functions.html#bool)= False, occlusion:[bool](https://docs.python.org/3/library/functions.html#bool)= False, normals:[bool](https://docs.python.org/3/library/functions.html#bool)= False, motion_vectors:[bool](https://docs.python.org/3/library/functions.html#bool)= False, camera_params:[bool](https://docs.python.org/3/library/functions.html#bool)= False, pointcloud:[bool](https://docs.python.org/3/library/functions.html#bool)= False, image_output_format:[str](https://docs.python.org/3/library/stdtypes.html#str)= 'png', colorize_semantic_segmentation:[bool](https://docs.python.org/3/library/functions.html#bool)= True, colorize_instance_id_segmentation:[bool](https://docs.python.org/3/library/functions.html#bool)= True, colorize_instance_segmentation:[bool](https://docs.python.org/3/library/functions.html#bool)= True, skeleton_data:[bool](https://docs.python.org/3/library/functions.html#bool)= False, frame_padding:[int](https://docs.python.org/3/library/functions.html#int)= 4) Basic writer capable of writing built-in annotator groundtruth.
-
output_dir
Output directory string that indicates the directory to save the results.
-
semantic_types
List of semantic types to consider when filtering annotator data. Default: [“class”]
-
rgb
Boolean value that indicates whether the rgb annotator will be activated and the data will be written or not. Default: False.
-
bounding_box_2d_tight
Boolean value that indicates whether the bounding_box_2d_tight annotator will be activated and the data will be written or not. Default: False.
-
bounding_box_2d_loose
Boolean value that indicates whether the bounding_box_2d_loose annotator will be activated and the data will be written or not. Default: False.
-
semantic_segmentation
Boolean value that indicates whether the semantic_segmentation annotator will be activated and the data will be written or not. Default: False.
-
instance_id_segmentation
Boolean value that indicates whether the instance_id_segmentation annotator will be activated and the data will be written or not. Default: False.
-
instance_segmentation
Boolean value that indicates whether the instance_segmentation annotator will be activated and the data will be written or not. Default: False.
-
distance_to_camera
Boolean value that indicates whether the distance_to_camera annotator will be activated and the data will be written or not. Default: False.
-
distance_to_image_plane
Boolean value that indicates whether the distance_to_image_plane annotator will be activated and the data will be written or not. Default: False.
-
bounding_box_3d
Boolean value that indicates whether the bounding_box_3d annotator will be activated and the data will be written or not. Default: False.
-
occlusion
Boolean value that indicates whether the occlusion annotator will be activated and the data will be written or not. Default: False.
-
normals
Boolean value that indicates whether the normals annotator will be activated and the data will be written or not. Default: False.
-
motion_vectors
Boolean value that indicates whether the motion_vectors annotator will be activated and the data will be written or not. Default: False.
-
camera_params
Boolean value that indicates whether the camera_params annotator will be activated and the data will be written or not. Default: False.
-
pointcloud
Boolean value that indicates whether the pointcloud annotator will be activated and the data will be written or not. Default: False.
-
image_output_format
String that indicates the format of saved RGB images. Default: “png”
-
colorize_semantic_segmentation
If
True
, semantic segmentation is converted to an image where semantic IDs are mapped to colors and saved as a uint8 4 channel PNG image. IfFalse
, the output is saved as a uint32 PNG image. Defaults toTrue
.
-
colorize_instance_id_segmentation
If True, instance id segmentation is converted to an image where instance IDs are mapped to colors. and saved as a uint8 4 channel PNG image. If
False
, the output is saved as a uint32 PNG image. Defaults toTrue
.
-
colorize_instance_segmentation
If True, instance segmentation is converted to an image where instance are mapped to colors. and saved as a uint8 4 channel PNG image. If
False
, the output is saved as a uint32 PNG image. Defaults toTrue
.
-
frame_padding
Pad the frame number with leading zeroes. Default: 4
Example
>>> import omni.replicator.core as rep >>> camera = rep.create.camera() >>> render_product = rep.create.render_product(camera, (1024, 1024)) >>> writer = rep.WriterRegistry.get("BasicWriter") >>> import carb >>> tmp_dir = carb.tokens.get_tokens_interface().resolve("${temp}/rgb") >>> writer.initialize(output_dir=tmp_dir, rgb=True) >>> writer.attach([render_product]) >>> rep.orchestrator.run()
-
write
(data:[dict](https://docs.python.org/3/library/stdtypes.html#dict)) Write function called from the OgnWriter node on every frame to process annotator output.
- Parameters
data – A dictionary containing the annotator data for the current frame.
-
-
class
omni.replicator.core.
Writer
Base Writer class.
Writers must specify a list of required annotators which will be called during data collection and which return their output in a data dict of the form <annotator_name>: <annotator_data>.
An optional on_final_frame function can be defined to run on the final data writing frame.
-
on_final_frame
() Run after final frame is written.
-
abstract
write
(data:[dict](https://docs.python.org/3/library/stdtypes.html#dict)) Write ground truth.
-
Create[¶](#module-omni.replicator.core.create)
-
omni.replicator.core.create.
register
(fn: Callable[[…], Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, omni.graph.core._omni_graph_core.Node]], override:[bool](https://docs.python.org/3/library/functions.html#bool)= True) →[None](https://docs.python.org/3/library/constants.html#None)[¶](#omni.replicator.core.create.register) Register a new function under omni.replicator.core.create. Extend the default capabilities of omni.replicator.core.create by registering new functionality. New functions must return a ReplicatorItem or an OmniGraph node.
- Parameters
fn – A function that returns a ReplicatorItem or an OmniGraph node.
override – If True, will override existing functions of the same name. If false, an error is raised.
Example
>>> import omni.replicator.core as rep >>> def light_cluster(num_lights: int = 10): ... lights = rep.create.light( ... light_type="sphere", ... count=num_lights, ... position=rep.distribution.uniform((-500, -500, -500), (500, 500, 500)), ... intensity=rep.distribution.uniform(10000, 20000), ... temperature=rep.distribution.uniform(1000, 10000), ... ) ... return lights >>> rep.create.register(light_cluster) >>> lights = rep.create.light_cluster(50)
-
omni.replicator.core.create.
sphere
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, material: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, pxr.Usd.Prim] = None, visible:[bool](https://docs.python.org/3/library/functions.html#bool)= True, as_mesh:[bool](https://docs.python.org/3/library/functions.html#bool)= True, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.sphere) Create a sphere
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value.
pivot – Pivot that sets the center point of translate and rotate operation. Pivot values are normalized between [-1, 1] for each axis based on the prim’s axis aligned extents.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
semantics – List of semantic type-label pairs.
material – Material to attach to the sphere.
visible – If false, the prim will be invisible. This is often useful when creating prims to use as bounds with other randomizers.
as_mesh – If false, create a Usd.Sphere prim. If true, create a mesh.
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> sphere = rep.create.sphere( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... scale=2, ... rotation=(45, 45, 0), ... semantics=[("class", "sphere")], ... )
-
omni.replicator.core.create.
torus
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, material: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, pxr.Usd.Prim] = None, visible:[bool](https://docs.python.org/3/library/functions.html#bool)= True, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.torus) Create a torus
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value.
pivot – Pivot that sets the center point of translate and rotate operation. Pivot values are normalized between [-1, 1] for each axis based on the prim’s axis aligned extents.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
semantics – List of semantic type-label pairs.
material – Material to attach to the torus.
visible – If false, the prim will be invisible. This is often useful when creating prims to use as bounds with other randomizers.
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> torus = rep.create.torus( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... scale=2, ... rotation=(45, 45, 0), ... semantics=[("class", "torus")], ... )
-
omni.replicator.core.create.
disk
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, material: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, pxr.Usd.Prim] = None, visible:[bool](https://docs.python.org/3/library/functions.html#bool)= True, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.disk) Create a disk
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value.
pivot – Pivot that sets the center point of translate and rotate operation. Pivot values are normalized between [-1, 1] for each axis based on the prim’s axis aligned extents.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
semantics – List of semantic type-label pairs.
material – Material to attach to the disk.
visible – If false, the prim will be invisible. This is often useful when creating prims to use as bounds with other randomizers.
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> disk = rep.create.disk( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... scale=2, ... rotation=(45, 45, 0), ... semantics=[("class", "disk")], ... )
-
omni.replicator.core.create.
plane
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, material: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, pxr.Usd.Prim] = None, visible:[bool](https://docs.python.org/3/library/functions.html#bool)= True, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.plane) Create a plane
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value.
pivot – Pivot that sets the center point of translate and rotate operation. Pivot values are normalized between [-1, 1] for each axis based on the prim’s axis aligned extents.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
semantics – List of semantic type-label pairs.
material – Material to attach to the plane.
visible – If false, the prim will be invisible. This is often useful when creating prims to use as bounds with other randomizers.
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> plane = rep.create.plane( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... scale=2, ... rotation=(45, 45, 0), ... semantics=[("class", "plane")], ... )
-
omni.replicator.core.create.
cube
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, material: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, pxr.Usd.Prim] = None, visible:[bool](https://docs.python.org/3/library/functions.html#bool)= True, as_mesh:[bool](https://docs.python.org/3/library/functions.html#bool)= True, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.cube) Create a cube
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value.
pivot – Pivot that sets the center point of translate and rotate operation. Pivot values are normalized between [-1, 1] for each axis based on the prim’s axis aligned extents.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
semantics – List of semantic type-label pairs.
material – Material to attach to the cube.
visible – If false, the prim will be invisible. This is often useful when creating prims to use as bounds with other randomizers.
as_mesh – If false, create a Usd.Cube prim. If true, create a mesh.
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> cube = rep.create.cube( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... scale=2, ... rotation=(45, 45, 0), ... semantics=[("class", "cube")], ... )
-
omni.replicator.core.create.
cylinder
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, material: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, pxr.Usd.Prim] = None, visible:[bool](https://docs.python.org/3/library/functions.html#bool)= True, as_mesh:[bool](https://docs.python.org/3/library/functions.html#bool)= True, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.cylinder) Create a cylinder
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value.
pivot – Pivot that sets the center point of translate and rotate operation. Pivot values are normalized between [-1, 1] for each axis based on the prim’s axis aligned extents.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
semantics – List of semantic type-label pairs.
material – Material to attach to the cylinder.
visible – If false, the prim will be invisible. This is often useful when creating prims to use as bounds with other randomizers.
as_mesh – If false, create a Usd.Cylinder prim. If true, create a mesh.
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> cylinder = rep.create.cylinder( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... scale=2, ... rotation=(45, 45, 0), ... semantics=[("class", "cylinder")], ... )
-
omni.replicator.core.create.
cone
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, material: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, pxr.Usd.Prim] = None, visible:[bool](https://docs.python.org/3/library/functions.html#bool)= True, as_mesh:[bool](https://docs.python.org/3/library/functions.html#bool)= True, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.cone) Create a cone
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value.
pivot – Pivot that sets the center point of translate and rotate operation. Pivot values are normalized between [-1, 1] for each axis based on the prim’s axis aligned extents.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
semantics – List of semantic type-label pairs.
material – Material to attach to the cone.
visible – If false, the prim will be invisible. This is often useful when creating prims to use as bounds with other randomizers.
as_mesh – If false, create a Usd.Cone prim. If true, create a mesh.
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> cone = rep.create.cone( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... scale=2, ... rotation=(45, 45, 0), ... semantics=[("class", "cone")], ... )
-
omni.replicator.core.create.
camera
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, focal_length: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 24.0, focus_distance: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 400.0, f_stop: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, horizontal_aperture: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 20.955, horizontal_aperture_offset: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, vertical_aperture_offset: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, clipping_range: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = (1.0, 1000000.0), projection_type: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str)] = 'pinhole', fisheye_nominal_width: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 1936.0, fisheye_nominal_height: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 1216.0, fisheye_optical_centre_x: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 970.94244, fisheye_optical_centre_y: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 600.37482, fisheye_max_fov: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 200.0, fisheye_polynomial_a: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, fisheye_polynomial_b: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.00245, fisheye_polynomial_c: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, fisheye_polynomial_d: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, fisheye_polynomial_e: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, count:[int](https://docs.python.org/3/library/functions.html#int)= 1, parent: omni.replicator.core.scripts.utils.utils.ReplicatorItem = None) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.camera) Create a camera
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
focal_length – Physical focal length of the camera in units equal to 0.1 * world units.
focus_distance – Distance from the camera to the focus plane in world units.
f_stop – Lens aperture. Default 0.0 turns off focusing.
horizontal_aperture – Horizontal aperture in units equal to 0.1 * world units. Default simulates a 35mm spherical projection aperture.
horizontal_aperture_offset – Horizontal aperture offset in units equal to 0.1 * world units.
vertical_aperture_offset – Vertical aperture offset in units equal to 0.1 * world units.
clipping_range – (Near, Far) clipping distances of the camera in world units.
projection_type – Camera projection model. Select from [pinhole, fisheye_polynomial].
fisheye_nominal_width – Nominal width of fisheye lens model.
fisheye_nominal_height – Nominal height of fisheye lens model.
fisheye_optical_centre_x – Horizontal optical centre position of fisheye lens model.
fisheye_optical_centre_y – Vertical optical centre position of fisheye lens model.
fisheye_max_fov – Maximum field of view of fisheye lens model.
fisheye_polynomial_a – First component of fisheye polynomial (only valid for fisheye_polynomial projection type).
fisheye_polynomial_b – Second component of fisheye polynomial (only valid for fisheye_polynomial projection type).
fisheye_polynomial_c – Third component of fisheye polynomial (only valid for fisheye_polynomial projection type).
fisheye_polynomial_d – Fourth component of fisheye polynomial (only valid for fisheye_polynomial projection type).
fisheye_polynomial_e – Fifth component of fisheye polynomial (only valid for fisheye_polynomial projection type).
count – Number of objects to create.
parent – Optional parent prim path. The camera will be created as a child of this prim.
Example
>>> import omni.replicator.core as rep >>> # Create camera >>> camera = rep.create.camera( ... position=rep.distribution.uniform((0,0,0), (100, 100, 100)), ... rotation=(45, 45, 0), ... focus_distance=rep.distribution.normal(400.0, 100), ... f_stop=1.8, ... ) >>> # Attach camera to render product >>> render_product = rep.create.render_product(camera, resolution=(1024, 1024))
-
omni.replicator.core.create.
light
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at_up_axis: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, light_type:[str](https://docs.python.org/3/library/stdtypes.html#str)= 'Distant', color: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = (1.0, 1.0, 1.0), intensity: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 1000.0, exposure: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = None, temperature: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 6500, texture: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str)] = None, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.light) Create a light
- Parameters
position – XYZ coordinates in world space. If a single value is provided, all axes will be set to that value. Ignored for dome and distant light types.
scale – Scaling factors for XYZ axes. If a single value is provided, all axes will be set to that value. Ignored for dome and distant light types.
rotation – Euler angles in degrees in XYZ order. If a single value is provided, all axes will be set to that value.
look_at – Look-at target, specified either as a ReplicatorItem, a prim path or as coordinates. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – Look-at up axis of the created prim.
light_type – Light type. Select from [“cylinder”, “disk”, “distant”, “dome”, “rect”, “sphere”]
color – Light color in RGB colorspace.
intensity – Light intensity. Scales the power of the light linearly.
exposure – Scales the power of the light exponentially as a power of 2. The result is multiplied with intensity.
temperature – Color temperature in degrees Kelvin indicating the white point. Lower values are warmer, higher values are cooler. Valid range [1000, 10000].
texture – Image texture to use for dome light such as an HDR (High Dynamic Range) intended for IBL (Image Based Lighting). Ignored for other light types.
count – Number of objects to create.
Examples
>>> import omni.replicator.core as rep >>> distance_light = rep.create.light( ... rotation=rep.distribution.uniform((0,-180,-180), (0,180,180)), ... intensity=rep.distribution.normal(10000, 1000), ... temperature=rep.distribution.normal(6500, 1000), ... light_type="distant") >>> dome_light = rep.create.light( ... rotation=rep.distribution.uniform((0,-180,-180), (0,180,180)), ... texture=rep.distribution.choice(rep.example.TEXTURES), ... light_type="dome")
-
omni.replicator.core.create.
from_usd
(usd:[str](https://docs.python.org/3/library/stdtypes.html#str), semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, count:[int](https://docs.python.org/3/library/functions.html#int)= 1) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.from_usd) Reference a USD into the current USD stage.
- Parameters
usd – Path to a usd file (*.usd, *.usdc, *.usda)
semantics – List of semantic type-label pairs.
Example
>>> import omni.replicator.core as rep >>> usd_path = rep.example.ASSETS[0] >>> asset = rep.create.from_usd(usd_path, semantics=[("class", "example")])
-
omni.replicator.core.create.
group
(items: List[Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path]], semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.create.group) Group assets into a common node. Grouping assets makes it easier and faster to apply randomizations to multiple assets simultaneously.
- Parameters
items – Assets to be grouped together.
semantics – List of semantic type-label pairs.
Example
>>> import omni.replicator.core as rep >>> cones = [rep.create.cone() for _ in range(100)] >>> group = rep.create.group(cones, semantics=[("class", "cone")])
-
omni.replicator.core.create.
material_omnipbr
(diffuse: Tuple[[float](https://docs.python.org/3/library/functions.html#float)] = None, diffuse_texture:[str](https://docs.python.org/3/library/stdtypes.html#str)= None, roughness:[float](https://docs.python.org/3/library/functions.html#float)= None, roughness_texture:[str](https://docs.python.org/3/library/stdtypes.html#str)= None, metallic:[float](https://docs.python.org/3/library/functions.html#float)= None, metallic_texture:[str](https://docs.python.org/3/library/stdtypes.html#str)= None, specular:[float](https://docs.python.org/3/library/functions.html#float)= None, emissive_color: Tuple[[float](https://docs.python.org/3/library/functions.html#float)] = None, emissive_texture:[str](https://docs.python.org/3/library/stdtypes.html#str)= None, emissive_intensity:[float](https://docs.python.org/3/library/functions.html#float)= 0.0, project_uvw:[bool](https://docs.python.org/3/library/functions.html#bool)= False, semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, count:[int](https://docs.python.org/3/library/functions.html#int)= 1)[¶](#omni.replicator.core.create.material_omnipbr) Create an OmniPBR Material
- Parameters
diffuse – Diffuse/albedo color in RGB colorspace
diffuse_texture – Path to diffuse texture
roughness – Material roughness in the range [0, 1]
roughness_texture – Path to roughness texture
metallic – Material metallic value in the range [0, 1]. Typically, metallic is assigned either 0.0 or 1.0
metallic_texture – Path to metallic texture
specular – Intensity of specular reflections in the range [0, 1]
emissive_color – Color of emissive light emanating from material in RGB colorspace
emissive_texture – Path to emissive texture
emissive_intensity – Emissive intensity of the material. Setting to 0.0 (default) disables emission.
project_uvw – When True, UV coordinates will be generated by projecting them from a coordinate system.
semantics – Assign semantics to material
count – Number of objects to create.
Example
>>> import omni.replicator.core as rep >>> mat1 = rep.create.material_omnipbr( ... diffuse=rep.distribution.uniform((0, 0, 0), (1, 1, 1)), ... roughness=rep.distribution.uniform(0, 1), ... metallic=rep.distribution.choice([0, 1]), ... emissive_color=rep.distribution.uniform((0, 0, 0.5), (0, 0, 1)), ... emissive_intensity=rep.distribution.uniform(0, 1000), ... ) >>> mat2 = rep.create.material_omnipbr( ... diffuse_texture=rep.distribution.choice(rep.example.TEXTURES), ... roughness_texture=rep.distribution.choice(rep.example.TEXTURES), ... metallic_texture=rep.distribution.choice(rep.example.TEXTURES), ... emissive_texture=rep.distribution.choice(rep.example.TEXTURES), ... emissive_intensity=rep.distribution.uniform(0, 1000), ... ) >>> cone = rep.create.cone(material=mat1) >>> torus = rep.create.torus(material=mat2)
Distribution[¶](#module-omni.replicator.core.distribution)
-
omni.replicator.core.distribution.
register
(fn: Callable[[…], Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, omni.graph.core._omni_graph_core.Node]], override:[bool](https://docs.python.org/3/library/functions.html#bool)= True) →[None](https://docs.python.org/3/library/constants.html#None)[¶](#omni.replicator.core.distribution.register) Register a new function under omni.replicator.core.distribution. Extend the default capabilities of omni.replicator.core.distribution by registering new functionality. New functions must return a ReplicatorItem or an OmniGraph node.
- Parameters
fn – A function that returns a ReplicatorItem or an OmniGraph node.
override – If True, will override existing functions of the same name. If false, an error is raised.
-
omni.replicator.core.distribution.
uniform
(lower: Tuple, upper: Tuple, num_samples:[int](https://docs.python.org/3/library/functions.html#int)= 1, seed: Optional[[int](https://docs.python.org/3/library/functions.html#int)] = None, name: Optional[[str](https://docs.python.org/3/library/stdtypes.html#str)] = None)[¶](#omni.replicator.core.distribution.uniform) Provides sampling with a uniform distribution
- Parameters
lower – Lower end of the distribution.
upper – Upper end of the distribution.
num_samples – The number of times to sample.
seed (optional) – A seed to use for the sampling.
name (optional) – A name for the given distribution. Named distributions will have their values available to the Writer.
-
omni.replicator.core.distribution.
normal
(mean: Tuple, std: Tuple, num_samples:[int](https://docs.python.org/3/library/functions.html#int)= 1, seed: Optional[[int](https://docs.python.org/3/library/functions.html#int)] = None, name: Optional[[str](https://docs.python.org/3/library/stdtypes.html#str)] = None)[¶](#omni.replicator.core.distribution.normal) Provides sampling with a normal distribution
- Parameters
mean – Average value for the distribution.
std – Standard deviation value for the distribution.
num_samples – The number of times to sample.
seed (optional) – A seed to use for the sampling.
name (optional) – A name for the given distribution. Named distributions will have their values available to the Writer.
-
omni.replicator.core.distribution.
choice
(choices: List[[str](https://docs.python.org/3/library/stdtypes.html#str)], weights: List[[float](https://docs.python.org/3/library/functions.html#float)] = None, num_samples: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[int](https://docs.python.org/3/library/functions.html#int)] = 1, seed: Optional[[int](https://docs.python.org/3/library/functions.html#int)] = None, with_replacements:[bool](https://docs.python.org/3/library/functions.html#bool)= True, name: Optional[[str](https://docs.python.org/3/library/stdtypes.html#str)] = None)[¶](#omni.replicator.core.distribution.choice) Provides sampling from a list of values
- Parameters
choices – Values in the distribution to choose from.
weights – Matching list of weights for each choice.
num_samples – The number of times to sample.
seed (optional) – A seed to use for the sampling.
with_replacements – If
True
, allow re-sampling the same element. IfFalse
, each element can only be sampled once. Note that in this case, the size of the elements being sampled must be larger than the sampling size. Default is True.name (optional) – A name for the given distribution. Named distributions will have their values available to the Writer.
Get[¶](#module-omni.replicator.core.get)
-
omni.replicator.core.get.
register
(fn, override=True)[¶](#omni.replicator.core.get.register) Register a new function under omni.replicator.core.get. Extend the default capabilities of omni.replicator.core.get by registering new functionality. New functions must return a ReplicatorItem or an OmniGraph node.
- Parameters
fn – A function that returns a ReplicatorItem or an OmniGraph node.
override – If True, will override existing functions of the same name. If false, an error is raised.
-
omni.replicator.core.get.
prims
(path_pattern:[str](https://docs.python.org/3/library/stdtypes.html#str)= None, path_pattern_exclusion:[str](https://docs.python.org/3/library/stdtypes.html#str)= None, prim_types: Union[[str](https://docs.python.org/3/library/stdtypes.html#str), List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, prim_types_exclusion: Union[[str](https://docs.python.org/3/library/stdtypes.html#str), List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, semantics: Union[List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]], Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, semantics_exclusion: Union[List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]], Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, cache_result:[bool](https://docs.python.org/3/library/functions.html#bool)= True)[¶](#omni.replicator.core.get.prims) Get prims based on specified constraints.
Search the stage for stage paths with matches to the specified constraints.
- Parameters
path_pattern – The RegEx (Regular Expression) path pattern to match.
path_pattern_exclusion – The RegEx (Regular Expression) path pattern to ignore.
prim_types – List of prim types to include
prim_types_exclusion – List of prim types to ignore
semantics – Semantic type-value pairs of semantics to include
semantics_exclusion – Semantic type-value pairs of semantics to ignore
cache_result – Run get prims a single time, then return the cached result
Modify[¶](#module-omni.replicator.core.modify)
-
omni.replicator.core.modify.
register
(fn, override=True)[¶](#omni.replicator.core.modify.register) Register a new function under omni.replicator.core.modify. Extend the default capabilities of omni.replicator.core.modify by registering new functionality. New functions must return a ReplicatorItem or an OmniGraph node.
- Parameters
fn – A function that returns a ReplicatorItem or an OmniGraph node.
override – If True, will override existing functions of the same name. If false, an error is raised.
-
omni.replicator.core.modify.
semantics
(semantics: List[Tuple[[str](https://docs.python.org/3/library/stdtypes.html#str),[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.modify.semantics) Modify the orientation of the prims specified in input_prims to look at the specified target.
- Parameters
target – The target to orient towards. If multiple prims are set, the target point will be the mean of their positions.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> with rep.create.sphere(): ... rep.modify.semantics([("class", "sphere")]) omni.replicator.core.modify.semantics
-
omni.replicator.core.modify.
pose
(position: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, rotation_order:[str](https://docs.python.org/3/library/stdtypes.html#str)= 'XYZ', scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, size: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float), Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, pivot: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float)]] = None, look_at: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[Union[[str](https://docs.python.org/3/library/stdtypes.html#str), pxr.Sdf.Path]]] = None, look_at_up_axis: Union[[str](https://docs.python.org/3/library/stdtypes.html#str), Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.modify.pose) Modify the position, rotation, scale, and/or look-at target of the prims specified in input_prims.
NOTE: rotation and look_at cannot both be specified.
NOTE: size and scale cannot both be specified.
NOTE: size is converted to scale based on the prim’s current axis-aligned bounding box size. If a scale is already applied, it might not be able to reflect the true size of the prim.
- Parameters
position – XYZ coordinates in world space.
rotation – Rotation in degrees for the axes specified in rotation_order
rotation_order – Order of rotation. Select from [XYZ, XZY, YXZ, YZX, ZXY, ZYX]
scale – Scale factor for each of XYZ axes.
size – Desired size of the input prims. Each input prim is scaled to match the specified size extents in each of the XYZ axes.
pivot – Pivot that sets the center point of translate and rotate operation.
look_at – The look at target to orient towards. If multiple prims are set, the target point will be the mean of their positions.
look_at_up_axis – The up axis used in look_at function
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> with rep.create.cube(): ... rep.modify.pose(position=rep.distribution.uniform((0, 0, 0), (100, 100, 100)), ... scale=rep.distribution.uniform(0.1, 10), ... look_at=(0, 0, 0)) omni.replicator.core.modify.pose
-
omni.replicator.core.modify.
attribute
(name:[str](https://docs.python.org/3/library/stdtypes.html#str), value: Union[Any, omni.replicator.core.scripts.utils.utils.ReplicatorItem], attribute_type:[str](https://docs.python.org/3/library/stdtypes.html#str)= None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.modify.attribute) Modify the attribute of the prims specified in input_prims.
- Parameters
name – The name of the attribute to modify.
value – The value to set the attribute to.
attribute_type – The data type of the attribute. This parameter is required if the attribute specified does not already exist and must be created.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> sphere = rep.create.sphere(as_mesh=False) >>> with sphere: ... rep.modify.attribute("radius", rep.distribution.uniform(1, 5)) omni.replicator.core.modify.attribute
Orchestrator[¶](#module-omni.replicator.core.orchestrator)
-
omni.replicator.core.orchestrator.
run
()[¶](#omni.replicator.core.orchestrator.run) Run the replicator scenario
-
omni.replicator.core.orchestrator.
stop
()[¶](#omni.replicator.core.orchestrator.stop) Stop the replicator scenario
-
omni.replicator.core.orchestrator.
preview
()[¶](#omni.replicator.core.orchestrator.preview) Run the replicator scenario for a single iteration. Writers are disabled during preview.
Physics[¶](#module-omni.replicator.core.physics)
-
omni.replicator.core.physics.
rigid_body
(velocity: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = (0.0, 0.0, 0.0), angular_velocity: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]] = (0.0, 0.0, 0.0), input_prims: List = None)[¶](#omni.replicator.core.physics.rigid_body) - Randomizes the velocity and angular velocity of the prims specified in input_prims. If they do not have
the RigidBody API then one will be created for the prim.
- Parameters
velocity – The velocity of the prim.
angular_velocty – The angular velocity of the prim (degrees / time).
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> with rep.create.cube(): ... rep.physics.rigid_body( ... velocity=rep.distribution.uniform((0, 0, 0), (100, 100, 100)), ... angular_velocity=rep.distribution.uniform((30, 30, 30), (300, 300, 300)) ... ) omni.replicator.core.physics.rigid_body
-
omni.replicator.core.physics.
collider
(approximation_shape:[str](https://docs.python.org/3/library/stdtypes.html#str)= 'convexHull', input_prims: Optional[Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List]] = None)[¶](#omni.replicator.core.physics.collider) Applies the Physx Collision API to the prims specified in input_prims.
- Parameters
approximation_shape – The approximation used in the collider (by default, convex hull). Other approximations include “convexDecomposition”, “boundingSphere”, “boundingCube”, “meshSimplification”, and “none”. “none” will just use default mesh geometry.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> with rep.create.cube(): ... rep.physics.collider()
-
omni.replicator.core.physics.
mass
(mass: Optional[[float](https://docs.python.org/3/library/functions.html#float)] = None, density: Optional[[float](https://docs.python.org/3/library/functions.html#float)] = None, center_of_mass: Optional[List] = None, diagonal_inertia: Optional[List] = None, principal_axes: Optional[List] = None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List] = None)[¶](#omni.replicator.core.physics.mass) - Applies the Physx Mass API to the prims specified in input_prims, if necessary. This function sets up randomization
parameters for various mass-related properties in the mass API.
- Parameters
mass – The mass of the prim. By default mass is derived from the volume of the collision geometry multiplied by a density.
density – The density of the prim.
center_of_mass – Center of the mass of the prim in local coordinates.
diagonal_inertia – Constructs a diagonalized inertia tensor along the principal axes.
principal_axes – A quaternion (wxyz) representing the orientation of the principal axes in the local coordinate frame.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> with rep.create.cube(): ... rep.physics.mass(mass=rep.distribution.uniform(1.0, 50.0)) omni.replicator.core.physics.mass
-
omni.replicator.core.physics.
drive_properties
(stiffness: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, damping: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = 0.0, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List] = None)[¶](#omni.replicator.core.physics.drive_properties) - Applies the Drive API to the prims specified in input_prims, if necessary. Prims must be either revolute or
prismatic joints. For D6 joint randomization, please refer to omni.replicator.core.modify.attribute and provide the exact attribute name of the drive parameter to be randomized.
- Parameters
stiffness – The stiffness of the drive (unitless).
damping – The damping of the drive (unitless).
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
-
omni.replicator.core.physics.
physics_material
(static_friction: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = None, dynamic_friction: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = None, restitution: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[float](https://docs.python.org/3/library/functions.html#float)] = None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List] = None)[¶](#omni.replicator.core.physics.physics_material) - If input prim is a material, the physics material API will be applied if necessary. Otherwise, if the prim has a
bound material, then randomizations will be made on this material (where once again, with the physics material API being bound if necessary). If the prim does not have a bound material, then a physics material will be created at <prim_path>/PhysicsMaterial and bound at the prim.
- Parameters
dynamic_friction – Dynamic friction coefficient (unitless).
restitution – Restitution coefficient (unitless).
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> with rep.create.cube(): ... rep.physics.physics_material( ... static_friction=rep.distribution.uniform(0.0, 1.0), ... dynamic_friction=rep.distribution.uniform(0.0, 1.0), ... restitution=rep.distribution.uniform(0.0, 1.0) ... ) omni.replicator.core.physics.physics_material
Randomizer[¶](#module-omni.replicator.core.randomizer)
-
omni.replicator.core.randomizer.
scatter_2d
(surface_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]], seed:[int](https://docs.python.org/3/library/functions.html#int)= None, offset:[int](https://docs.python.org/3/library/functions.html#int)= 0, check_for_collisions:[bool](https://docs.python.org/3/library/functions.html#bool)= False, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None)[¶](#omni.replicator.core.randomizer.scatter_2d) Scatter input prims across the surface of the specified surface prims.
- Parameters
surface_prims – The prims across which to scatter the input prims. These can be meshes or GeomSubsets which specify a subset of a mesh’s polygons on which to scatter.
seed – Seed to use as initialization for the pseudo-random number generator. If not specified, the global seed will be used.
offset – The distance the prims should be offset along the normal of the surface of the mesh.
check_for_collisions – Whether the scatter operation should ensure that objects are not intersecting.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> spheres = rep.create.sphere(count=100) >>> surface_prim = rep.create.torus(scale=20, visible=False) >>> with spheres: ... rep.randomizer.scatter_2d(surface_prim) omni.replicator.core.randomizer.scatter_2d
-
omni.replicator.core.randomizer.
scatter_3d
(volume_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]], resolution_scaling:[float](https://docs.python.org/3/library/functions.html#float)= 1.0, check_for_collisions:[bool](https://docs.python.org/3/library/functions.html#bool)= False, seed:[int](https://docs.python.org/3/library/functions.html#int)= None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None)[¶](#omni.replicator.core.randomizer.scatter_3d) Scatter input prims within the bounds of the specified volume prims.
- Parameters
volume_prims – The prims within which to scatter the input prims. Currently, only meshes are supported.
resolution_scaling – The scale factor that should be applied to the resolution of the voxelgrid. Higher values
ensure more fine-grained voxels (will) –
will come at the cost of performance. (but) –
check_for_collisions – Whether the scatter operation should ensure that objects are not intersecting.
seed – Seed to use as initialization for the pseudo-random number generator. If not specified, the global seed will be used.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> spheres = rep.create.sphere(count=100) >>> volume_prim = rep.create.torus(scale=20, visible=False) >>> with spheres: ... rep.randomizer.scatter_3d(volume_prim) omni.replicator.core.randomizer.scatter_3d
-
omni.replicator.core.randomizer.
materials
(materials: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]], seed:[int](https://docs.python.org/3/library/functions.html#int)= None, input_prims=None)[¶](#omni.replicator.core.randomizer.materials) Sample materials from provided materials and bind to the input_prims.
Note that binding materials is a relatively expensive operation. It is generally more efficient to modify materials already bound to prims.
- Parameters
materials – The list of materials to sample from and bind to the input prims. The materials can be prim paths, MDL paths or a ReplicatorItem.
seed – Seed to use as initialization for the pseudo-random number generator. If not specified, the global seed will be used.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> mats = rep.create.material_omnipbr(diffuse=rep.distribution.uniform((0,0,0), (1,1,1)), count=100) >>> spheres = rep.create.sphere( ... scale=0.2, ... position=rep.distribution.uniform((-100,-100,-100), (100,100,100)), ... count=100 ... ) >>> with spheres: ... rep.randomizer.materials(mats) omni.replicator.core.randomizer.materials
-
omni.replicator.core.randomizer.
instantiate
(paths: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]], size: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem,[int](https://docs.python.org/3/library/functions.html#int)], weights: List[[float](https://docs.python.org/3/library/functions.html#float)] = None, mode:[str](https://docs.python.org/3/library/stdtypes.html#str)= 'scene_instance', with_replacements=True, seed:[int](https://docs.python.org/3/library/functions.html#int)= None, use_cache:[bool](https://docs.python.org/3/library/functions.html#bool)= True)[¶](#omni.replicator.core.randomizer.instantiate) Sample size number of prims from the paths provided.
- Parameters
paths – The list of USD paths pointing to the assets to sample from.
size – The number of samples to sample.
weights – The weights to use for sampling. If provided, the length of weights must match the length of paths. If omitted, uniform sampling will be used.
mode – The instantiation mode. Choose from [scene_instance, point_instance, reference]. Defaults to scene_instance. Scene Instance creates a prototype in the cache, and new instances reference the prototype. Point Instances are best suited for situations requiring a very large number of samples, but only pose attributes can be modified per instance. Reference mode is used for asset references that need to be modified (WARNING: this mode has know material loading issue.).
with_replacements – When False, avoids duplicates when sampling. Default True.
seed – Seed to use as initialization for the pseudo-random number generator. If not specified, the global seed will be used.
use_cache – If True, cache the assets in paths to speed up randomization. Set to False if the size of the population is too large to be cached. Default: True.
Example
>>> import omni.replicator.core as rep >>> usds = rep.utils.get_usd_files(rep.example.ASSETS_DIR) >>> with rep.randomizer.instantiate(usds, size=100): ... rep.modify.pose(position=rep.distribution.uniform((-50,-50,-50),(50,50,50))) omni.replicator.core.modify.pose
-
omni.replicator.core.randomizer.
rotation
(min_angle: Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)] = (- 180.0, - 180.0, - 180.0), max_angle: Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)] = (180.0, 180.0, 180.0), seed:[int](https://docs.python.org/3/library/functions.html#int)= None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None)[¶](#omni.replicator.core.randomizer.rotation) Randomize the rotation of the input prims
This randomizer produces a truly uniformly distributed rotations to the input prims. In contrast, rotations are not truly uniformly distributed when simply sampling uniformly for each rotation axis.
- Parameters
min_angle – Minimum value for Euler angles in XYZ form (degrees)
max_angle – Maximum value for Euler angles in XYZ form (degrees)
seed – Seed to use as initialization for the pseudo-random number generator. If not specified, the global seed will be used.
input_prims – The prims to be modified. If using with syntax, this argument can be omitted.
Example
>>> import omni.replicator.core as rep >>> cubes = rep.create.cube(position=rep.distribution.uniform((-100,-100,-100),(100,100,100)), count=100) >>> with cubes: ... rep.randomizer.rotation() omni.replicator.core.randomizer.rotation
-
omni.replicator.core.randomizer.
texture
(textures: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]], texture_scale: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[Tuple[[float](https://docs.python.org/3/library/functions.html#float),[float](https://docs.python.org/3/library/functions.html#float)]]] = None, texture_rotate: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[int](https://docs.python.org/3/library/functions.html#int)]] = None, per_sub_mesh:[bool](https://docs.python.org/3/library/functions.html#bool)= False, project_uvw:[bool](https://docs.python.org/3/library/functions.html#bool)= False, seed:[int](https://docs.python.org/3/library/functions.html#int)= None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.randomizer.texture) Randomize texture Creates and binds an OmniPBR material to each prim in input_prims and modifies textures.
- Parameters
textures – List of texture paths, or a ReplicatorItem that outputs a list of texture paths. If a list of texture paths is provided, they will be sampled uniformly using the global seed.
texture_scale – List of texture scales in (X, Y) represented by positive floats. Larger values will make the texture appear smaller on the asset.
texture_rotate – Rotation in degrees of the texture.
per_sub_mesh – If True, bind a material to each mesh and geom_subset. If False, a material is bound only to the specified prim.
project_uvw – When True, UV coordinates will be generated by projecting them from a coordinate system.
seed – Seed to use as initialization for the pseudo-random number generator. If not specified, the global seed will be used.
input_prims – List of input_prims. If constructing using with structure, set to None to bind input_prims to the current context.
Example
>>> import omni.replicator.core as rep >>> with rep.create.cone(position=rep.distribution.uniform((-100,-100,-100),(100,100,100)), count=100): ... rep.randomizer.texture(textures=rep.example.TEXTURES, texture_scale=[(0.5, 0.5)], texture_rotate=[45]) omni.replicator.core.randomizer.texture
-
omni.replicator.core.randomizer.
color
(colors: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[Tuple[[float](https://docs.python.org/3/library/functions.html#float)]]], per_sub_mesh:[bool](https://docs.python.org/3/library/functions.html#bool)= False, seed:[int](https://docs.python.org/3/library/functions.html#int)= None, input_prims: Union[omni.replicator.core.scripts.utils.utils.ReplicatorItem, List[[str](https://docs.python.org/3/library/stdtypes.html#str)]] = None) → omni.graph.core._omni_graph_core.Node[¶](#omni.replicator.core.randomizer.color) Randomize colors Creates and binds an OmniPBR material to each prim in input_prims and modifies colors.
- Parameters
textures – List of texture paths, or a ReplicatorItem that outputs a list of texture paths. The number of textures must correspond with the number of input_prims.
per_sub_mesh – If True, bind a material to each mesh and geom_subset. If False, a material is bound only to the specified prim.
input_prims – List of input_prims. If constructing using with structure, set to None to bind input_prims to the current context.
Example
>>> import omni.replicator.core as rep >>> cones = rep.create.cone(position=rep.distribution.uniform((-100,-100,-100),(100,100,100)), count=100) >>> with cones: ... rep.randomizer.color(colors=rep.distribution.uniform((0, 0, 0), (1, 1, 1))) omni.replicator.core.randomizer.color
Settings[¶](#module-omni.replicator.core.settings)
Trigger[¶](#module-omni.replicator.core.trigger)
-
omni.replicator.core.trigger.
on_key_press
(key)[¶](#omni.replicator.core.trigger.on_key_press) Execute when a keyboard key is input.
- Parameters
key – The key to listen for.