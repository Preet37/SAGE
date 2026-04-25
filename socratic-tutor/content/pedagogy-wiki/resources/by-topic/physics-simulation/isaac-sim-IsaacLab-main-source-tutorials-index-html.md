# Source: https://isaac-sim.github.io/IsaacLab/main/source/tutorials/index.html
# Downloaded: 2026-04-06
# Words: 316
# Author: NVIDIA
# Author Slug: nvidia-isaac
Tutorials[#](#tutorials)
Welcome to the Isaac Lab tutorials! These tutorials provide a step-by-step guide to help you understand
and use various features of the framework. All the tutorials are written as Python scripts. You can
find the source code for each tutorial in the scripts/tutorials
directory of the Isaac Lab
repository.
Note
We would love to extend the tutorials to cover more topics and use cases, so please let us know if you have any suggestions.
We recommend that you go through the tutorials in the order they are listed here.
Setting up a Simple Simulation[#](#setting-up-a-simple-simulation)
These tutorials show you how to launch the simulation with different settings and spawn objects in the
simulated scene. They cover the following APIs: [ AppLauncher](../api/lab/isaaclab.app.html#isaaclab.app.AppLauncher),
[, and](../api/lab/isaaclab.sim.html#isaaclab.sim.SimulationContext)
SimulationContext
[.](../api/lab/isaaclab.sim.spawners.html#module-isaaclab.sim.spawners)
spawners
Interacting with Assets[#](#interacting-with-assets)
Having spawned objects in the scene, these tutorials show you how to create physics handles for these
objects and interact with them. These revolve around the [ AssetBase](../api/lab/isaaclab.assets.html#isaaclab.assets.AssetBase)
class and its derivatives such as
[,](../api/lab/isaaclab.assets.html#isaaclab.assets.RigidObject)
RigidObject
[and](../api/lab/isaaclab.assets.html#isaaclab.assets.Articulation)
Articulation
[.](../api/lab/isaaclab.assets.html#isaaclab.assets.DeformableObject)
DeformableObject
Creating a Scene[#](#creating-a-scene)
With the basic concepts of the framework covered, the tutorials move to a more intuitive scene
interface that uses the [ InteractiveScene](../api/lab/isaaclab.scene.html#isaaclab.scene.InteractiveScene) class. This class
provides a higher level abstraction for creating scenes easily.
Designing an Environment[#](#designing-an-environment)
The following tutorials introduce the concept of manager-based environments: [ ManagerBasedEnv](../api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedEnv)
and its derivative
[, as well as the direct workflow base class](../api/lab/isaaclab.envs.html#isaaclab.envs.ManagerBasedRLEnv)
ManagerBasedRLEnv
[. These environments bring-in together different aspects of the framework to create a simulation environment for agent interaction.](../api/lab/isaaclab.envs.html#isaaclab.envs.DirectRLEnv)
DirectRLEnv
Integrating Sensors[#](#integrating-sensors)
The following tutorial shows you how to integrate sensors into the simulation environment. The
tutorials introduce the [ SensorBase](../api/lab/isaaclab.sensors.html#isaaclab.sensors.SensorBase) class and its derivatives
such as
[and](../api/lab/isaaclab.sensors.html#isaaclab.sensors.Camera)
Camera
[.](../api/lab/isaaclab.sensors.html#isaaclab.sensors.RayCaster)
RayCaster
Using motion generators[#](#using-motion-generators)
While the robots in the simulation environment can be controlled at the joint-level, the following tutorials show you how to use motion generators to control the robots at the task-level.