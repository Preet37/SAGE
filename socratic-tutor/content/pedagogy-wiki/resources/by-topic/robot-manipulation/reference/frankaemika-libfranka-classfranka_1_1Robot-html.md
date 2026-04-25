# Source: https://frankaemika.github.io/libfranka/classfranka_1_1Robot.html
# Title: ◆ Robot() [1/2]
# Fetched via: search
# Date: 2026-04-09

|libfranka 0.15.0 FCI C++ API|
|--|
Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot. More...

`#include <robot.h>`
|## Public Types|
|--|
|using|ServerVersion = uint16_t|
|Version of the robot server.|
|## Public Member Functions|
|--|
|Robot (const std::string &franka_address, RealtimeConfig realtime_config=RealtimeConfig::kEnforce, size_t log_size=50)|
|Establishes a connection with the robot.|
|Robot (Robot &&other) noexcept|
|Move-constructs a new Robot instance.|
|Robot &|operator= (Robot &&other) noexcept|
|Move-assigns this Robot from another Robot instance.|
|virtual|~Robot () noexcept|
|Closes the connection.|
|void|read (std::function< bool(const RobotState &)> read_callback)|
|Starts a loop for reading the current robot state.|
|virtual RobotState|readOnce ()|
|Waits for a robot state update and returns it.|
|Model|loadModel ()|
|Loads the model library from the robot.|
|Model|loadModel (std::unique_ptr< RobotModelBase > robot_model)|
|ServerVersion|serverVersion () const noexcept|
|Returns the software version reported by the connected server.|
|Motion generation and joint-level torque commands|
|The following methods allow to perform motion generation and/or send joint-level torque commands without gravity and friction by providing callback functions. Only one of these methods can be active at the same time; a franka::ControlException is thrown otherwise. When a robot state is received, the callback function is used to calculate the response: the desired values for that time step. After sending back the response, the callback function will be called again with the most recently received robot state. Since the robot is controlled with a 1 kHz frequency, the callback functions have to compute their result in a short time frame in order to be accepted. Callback functions take two parameters: The following incomplete example shows the general structure of a callback function: double time = 0.0; auto control_callback = [&time](const franka::RobotState& robot_state, franka::Duration time_step) -> franka::JointPositions { time += time_step.toSec(); // Update time at the beginning of the callback. franka::JointPositions output = getJointPositions(time); if (time >= max_time) { // Return MotionFinished at the end of the trajectory. return franka::MotionFinished(output); } return output; } Represents a duration with millisecond resolution. Definition duration.h:19 Stores values for joint position motion generation. Definition control_types.h:72 Torques MotionFinished(Torques command) noexcept Helper method to indicate that a motion should stop after processing the given command. Definition control_types.h:294 Describes the robot state. Definition robot_state.h:34|
|void|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for sending joint-level torque commands.|
|void|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< JointPositions(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for sending joint-level torque commands and joint positions.|
|void|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< JointVelocities(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for sending joint-level torque commands and joint velocities.|
|void|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< CartesianPose(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for sending joint-level torque commands and Cartesian poses.|
|void|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< CartesianVelocities(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for sending joint-level torque commands and Cartesian velocities.|
|void|control (std::function< JointPositions(const RobotState &, franka::Duration)> motion_generator_callback, ControllerMode controller_mode=ControllerMode::kJointImpedance, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for a joint position motion generator with a given controller mode.|
|void|control (std::function< JointVelocities(const RobotState &, franka::Duration)> motion_generator_callback, ControllerMode controller_mode=ControllerMode::kJointImpedance, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for a joint velocity motion generator with a given controller mode.|
|void|control (std::function< CartesianPose(const RobotState &, franka::Duration)> motion_generator_callback, ControllerMode controller_mode=ControllerMode::kJointImpedance, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for a Cartesian pose motion generator with a given controller mode.|
|void|control (std::function< CartesianVelocities(const RobotState &, franka::Duration)> motion_generator_callback, ControllerMode controller_mode=ControllerMode::kJointImpedance, bool limit_rate=false, double cutoff_frequency=kDefaultCutoffFrequency)|
|Starts a control loop for a Cartesian velocity motion generator with a given controller mode.|
|Commands|
|Commands are executed by communicating with the robot over the network. These functions should therefore not be called from within control or motion generator loops.|
|auto|getRobotModel () -> std::string|
|void|setCollisionBehavior (const std::array< double, 7 > &lower_torque_thresholds_acceleration, const std::array< double, 7 > &upper_torque_thresholds_acceleration, const std::array< double, 7 > &lower_torque_thresholds_nominal, const std::array< double, 7 > &upper_torque_thresholds_nominal, const std::array< double, 6 > &lower_force_thresholds_acceleration, const std::array< double, 6 > &upper_force_thresholds_acceleration, const std::array< double, 6 > &lower_force_thresholds_nominal, const std::array< double, 6 > &upper_force_thresholds_nominal)|
|Changes the collision behavior.|
|void|setCollisionBehavior (const std::array< double, 7 > &lower_torque_thresholds, const std::array< double, 7 > &upper_torque_thresholds, const std::array< double, 6 > &lower_force_thresholds, const std::array< double, 6 > &upper_force_thresholds)|
|Changes the collision behavior.|
|void|setJointImpedance (const std::array< double, 7 > &K_theta)|
|Sets the impedance for each joint in the internal controller.|
|void|setCartesianImpedance (const std::array< double, 6 > &K_x)|
|Sets the Cartesian stiffness/compliance (for x, y, z, roll, pitch, yaw) in the internal controller.|
|void|setGuidingMode (const std::array< bool, 6 > &guiding_mode, bool elbow)|
|Locks or unlocks guiding mode movement in (x, y, z, roll, pitch, yaw).|
|void|setK (const std::array< double, 16 > &EE_T_K)|
|Sets the transformation \(^{EE}T_K\) from end effector frame to stiffness frame.|
|void|setEE (const std::array< double, 16 > &NE_T_EE)|
|Sets the transformation \(^{NE}T_{EE}\) from nominal end effector to end effector frame.|
|void|setLoad (double load_mass, const std::array< double, 3 > &F_x_Cload, const std::array< double, 9 > &load_inertia)|
|Sets dynamic parameters of a payload.|
|void|automaticErrorRecovery ()|
|Runs automatic error recovery on the robot.|
|virtual std::unique_ptr< ActiveControlBase >|startTorqueControl ()|
|Starts a new torque controller.|
|virtual std::unique_ptr< ActiveControlBase >|startJointPositionControl (const research_interface::robot::Move::ControllerMode &control_type)|
|Starts a new joint position motion generator.|
|virtual std::unique_ptr< ActiveControlBase >|startJointVelocityControl (const research_interface::robot::Move::ControllerMode &control_type)|
|Starts a new joint velocity motion generator.|
|virtual std::unique_ptr< ActiveControlBase >|startCartesianPoseControl (const research_interface::robot::Move::ControllerMode &control_type)|
|Starts a new cartesian position motion generator.|
|virtual std::unique_ptr< ActiveControlBase >|startCartesianVelocityControl (const research_interface::robot::Move::ControllerMode &control_type)|
|Starts a new cartesian velocity motion generator.|
|void|stop ()|
|Stops all currently running motions.|
|## Protected Member Functions|
|--|
|Robot (std::shared_ptr< Impl > robot_impl)|
|Constructs a new Robot given a Robot::Impl.|
|Robot ()=default|
|Default constructor to enable mocking and testing.|
Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot.

||explicit|
|--|--|
Establishes a connection with the robot.
|[in]|franka_address|IP/hostname of the robot.|
|--|--|--|
|[in]|realtime_config|if set to Enforce, an exception will be thrown if realtime priority cannot be set when required. Setting realtime_config to Ignore disables this behavior.|
|[in]|log_size|sets how many last states should be kept for logging purposes. The log is provided when a ControlException is thrown.|

…

This enables unittests with Robot::Impl-Mocks.

|robot_impl|Robot::Impl to use|
|--|--|
|void franka::Robot::automaticErrorRecovery|(|)|
|--|--|--|
Runs automatic error recovery on the robot.

Automatic error recovery e.g. resets the robot after a collision occurred.
|CommandException|if the Control reports an error.|
|--|--|
|NetworkException|if the connection is lost, e.g. after a timeout.|
|void franka::Robot::control|(|std::function< CartesianPose(const RobotState &, franka::Duration)>|motion_generator_callback,|

…

Loads the model library from the robot.

|ModelException|if the model library cannot be loaded.|
|--|--|
|NetworkException|if the connection is lost, e.g. after a timeout.|
|void franka::Robot::read|(|std::function< bool(const RobotState &)>|read_callback|)|
|--|--|--|--|--|
Starts a loop for reading the current robot state.

…

|)|
Changes the collision behavior.

Set common torque and force boundaries for acceleration/deceleration and constant velocity movement phases.

Forces or torques between lower and upper threshold are shown as contacts in the RobotState. Forces or torques above the upper threshold are registered as collision and cause the robot to stop moving.

…

Changes the collision behavior.

Set separate torque and force boundaries for acceleration/deceleration and constant velocity movement phases.

Forces or torques between lower and upper threshold are shown as contacts in the RobotState. Forces or torques above the upper threshold are registered as collision and cause the robot to stop moving.

libfranka 0.8.0
FCI C++ API
Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot. More...
#include <robot.h>
Public Types
|using
|ServerVersion = uint16_t
|Version of the robot server.
Public Member Functions
|Robot (const std::string &franka_address, RealtimeConfig realtime_config=RealtimeConfig::kEnforce, size_t log_size=50)
|Establishes a connection with the robot. More...
|Robot (Robot &&other) noexcept
|Move-constructs a new Robot instance. More...
|Robot &
|operator= (Robot &&other) noexcept
|Move-assigns this Robot from another Robot instance. More...
|~Robot () noexcept
|Closes the connection.
|void
|read (std::function< bool(const RobotState &)> read_callback)
|Starts a loop for reading the current robot state. More...
|RobotState
|readOnce ()
|Waits for a robot state update and returns it. More...
|Model
|loadModel ()
|Loads the model library from the robot. More...
|ServerVersion
|serverVersion () const noexcept
|Returns the software version reported by the connected server. More...
Motion generation and joint-level torque commands
The following methods allow to perform motion generation and/or send joint-level torque commands without gravity and friction by providing callback functions.
Only one of these methods can be active at the same time; a franka::ControlException is thrown otherwise.
When a robot state is received, the callback function is used to calculate the response: the desired values for that time step. After sending back the response, the callback function will be called again with the most recently received robot state. Since the robot is controlled with a 1 kHz frequency, the callback functions have to compute their result in a short time frame in order to be accepted. Callback functions take two parameters:
The following incomplete example shows the general structure of a callback function:
double time = 0.0;
auto control_callback = [&time](const franka::RobotState& robot_state,
franka::Duration time_step) -> franka::JointPositions {
time += time_step.toSec(); // Update time at the beginning of the callback.
franka::JointPositions output = getJointPositions(time);
if (time >= max_time) {
// Return MotionFinished at the end of the trajectory.
return franka::MotionFinished(output);
return output;
|void
|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)
|Starts a control loop for sending joint-level torque commands. More...
|void
|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< JointPositions(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)
|Starts a control loop for sending joint-level torque commands and joint positions. More...
|void
|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< JointVelocities(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)
|Starts a control loop for sending joint-level torque commands and joint velocities. More...
|void
|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< CartesianPose(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)
|Starts a control loop for sending joint-level torque commands and Cartesian poses. More...
|void
|control (std::function< Torques(const RobotState &, franka::Duration)> control_callback, std::function< CartesianVelocities(const RobotState &, franka::Duration)> motion_generator_callback, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)
|Starts a control loop for sending joint-level torque commands and Cartesian velocities. More...
|void
|control (std::function< JointPositions(const RobotState &, franka::Duration)> motion_generator_callback, ControllerMode controller_mode=ControllerMode::kJointImpedance, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)

…

|Starts a control loop for a joint velocity motion generator with a given controller mode. More...
|void
|control (std::function< CartesianPose(const RobotState &, franka::Duration)> motion_generator_callback, ControllerMode controller_mode=ControllerMode::kJointImpedance, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)
|Starts a control loop for a Cartesian pose motion generator with a given controller mode. More...
|void
|control (std::function< CartesianVelocities(const RobotState &, franka::Duration)> motion_generator_callback, ControllerMode controller_mode=ControllerMode::kJointImpedance, bool limit_rate=true, double cutoff_frequency=kDefaultCutoffFrequency)
|Starts a control loop for a Cartesian velocity motion generator with a given controller mode. More...
Commands
Commands are executed by communicating with the robot over the network.
These functions should therefore not be called from within control or motion generator loops.
|VirtualWallCuboid
|getVirtualWall (int32_t id)
|Returns the parameters of a virtual wall. More...

…

|Sets the Cartesian impedance for (x, y, z, roll, pitch, yaw) in the internal controller. More...
|void
|setGuidingMode (const std::array< bool, 6 > &guiding_mode, bool elbow)
|Locks or unlocks guiding mode movement in (x, y, z, roll, pitch, yaw). More...
|void
|setK (const std::array< double, 16 > &EE_T_K)
|Sets the transformation \(^{EE}T_K\) from end effector frame to stiffness frame. More...
|void
|setEE (const std::array< double, 16 > &NE_T_EE)

…

|Sets dynamic parameters of a payload. More...
|void
|setFilters (double joint_position_filter_frequency, double joint_velocity_filter_frequency, double cartesian_position_filter_frequency, double cartesian_velocity_filter_frequency, double controller_filter_frequency)
|Sets the cut off frequency for the given motion generator or controller. More...
|void
|automaticErrorRecovery ()
|Runs automatic error recovery on the robot. More...
|void
|stop ()
|Stops all currently running motions. More...
Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot.

…

|noexcept
|void franka::Robot::automaticErrorRecovery
|(
|)
Runs automatic error recovery on the robot.
Automatic error recovery e.g. resets the robot after a collision occurred.
|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|void franka::Robot::control
|(
|std::function< Torques(const RobotState &, franka::Duration)>
|control_callback,
|bool
|limit_rate =
true,
|double
|cutoff_frequency =
kDefaultCutoffFrequency
|)
Starts a control loop for sending joint-level torque commands.
Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.
|[in]
|control_callback
|Callback function providing joint-level torque commands. See here for more details.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!

…

|NetworkException
|if the connection is lost, e.g. after a timeout.
|RealtimeException
|if realtime priority cannot be set for the current thread.
|std::invalid_argument
|if joint-level torque commands are NaN or infinity.
|void franka::Robot::control
|(
|std::function< Torques(const RobotState &, franka::Duration)>
|control_callback,
|std::function< JointPositions(const RobotState &, franka::Duration)>
|motion_generator_callback,
|bool
|limit_rate =
true,
|double
|cutoff_frequency =
kDefaultCutoffFrequency
|)
Starts a control loop for sending joint-level torque commands and joint positions.
Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.
|[in]
|control_callback
|Callback function providing joint-level torque commands. See here for more details.
|[in]
|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!

…

|NetworkException
|if the connection is lost, e.g. after a timeout.
|RealtimeException
|if realtime priority cannot be set for the current thread.
|std::invalid_argument
|if joint-level torque or joint position commands are NaN or infinity.
|void franka::Robot::control
|(

…

|)
Starts a control loop for sending joint-level torque commands and joint velocities.
Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.
|[in]
|control_callback
|Callback function providing joint-level torque commands. See here for more details.
|[in]
|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!
|[in]
|cutoff_frequency
|Cutoff frequency for a first order low-pass filter applied on the user commanded signal. Set to franka::kMaxCutoffFrequency to disable.
|ControlException
|if an error related to torque control or motion generation occurred.
|InvalidOperationException
|if a conflicting operation is already running.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|RealtimeException
|if realtime priority cannot be set for the current thread.

…

|motion_generator_callback,
|bool
|limit_rate =
true,
|double
|cutoff_frequency =
kDefaultCutoffFrequency
|)
Starts a control loop for sending joint-level torque commands and Cartesian poses.
Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.
|[in]
|control_callback
|Callback function providing joint-level torque commands. See here for more details.
|[in]
|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!

…

|NetworkException
|if the connection is lost, e.g. after a timeout.
|RealtimeException
|if realtime priority cannot be set for the current thread.
|std::invalid_argument
|if joint-level torque or Cartesian pose command elements are NaN or infinity.
|void franka::Robot::control

…

|)
Starts a control loop for sending joint-level torque commands and Cartesian velocities.
Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.
|[in]
|control_callback
|Callback function providing joint-level torque commands. See here for more details.
|[in]
|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!
|[in]
|cutoff_frequency
|Cutoff frequency for a first order low-pass filter applied on the user commanded signal. Set to franka::kMaxCutoffFrequency to disable.
|ControlException
|if an error related to torque control or motion generation occurred.
|InvalidOperationException
|if a conflicting operation is already running.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|RealtimeException
|if realtime priority cannot be set for the current thread.

…

|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|controller_mode
|Controller to use to execute the motion.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!
|[in]

…

|NetworkException
|if the connection is lost, e.g. after a timeout.
|RealtimeException
|if realtime priority cannot be set for the current thread.
|std::invalid_argument
|if joint position commands are NaN or infinity.
|void franka::Robot::control
|(
|std::function< JointVelocities(const RobotState &, franka::Duration)>
|motion_generator_callback,
|ControllerMode
|controller_mode =
ControllerMode::kJointImpedance,
|bool
|limit_rate =
true,
|double
|cutoff_frequency =
kDefaultCutoffFrequency
|)
Starts a control loop for a joint velocity motion generator with a given controller mode.
Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.
|[in]
|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|controller_mode
|Controller to use to execute the motion.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!

…

|[in]
|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|controller_mode
|Controller to use to execute the motion.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!

…

|NetworkException
|if the connection is lost, e.g. after a timeout.
|RealtimeException
|if realtime priority cannot be set for the current thread.
|std::invalid_argument
|if Cartesian pose command elements are NaN or infinity.
|void franka::Robot::control
|(
|std::function< CartesianVelocities(const RobotState &, franka::Duration)>

…

|[in]
|motion_generator_callback
|Callback function for motion generation. See here for more details.
|[in]
|controller_mode
|Controller to use to execute the motion.
|[in]
|limit_rate
|True if rate limiting should be activated. True by default. This could distort your motion!

…

|(
|int32_t
|id
|)
Returns the parameters of a virtual wall.
|[in]
|id
|ID of the virtual wall.
|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|Model franka::Robot::loadModel
|(
|)
Loads the model library from the robot.
|ModelException
|if the model library cannot be loaded.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|void franka::Robot::read
|(
|std::function< bool(const RobotState &)>
|read_callback
|)
Starts a loop for reading the current robot state.
Cannot be executed while a control or motion generator loop is running.
This minimal example will print the robot state 100 times:
|[in]
|read_callback
|Callback function for robot state reading.
|InvalidOperationException
|if a conflicting operation is already running.

…

|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|void franka::Robot::setCollisionBehavior
|(
|const std::array< double, 7 > &
|lower_torque_thresholds_acceleration,
|const std::array< double, 7 > &

…

Set separate torque and force boundaries for acceleration/deceleration and constant velocity movement phases.
Forces or torques between lower and upper threshold are shown as contacts in the RobotState. Forces or torques above the upper threshold are registered as collision and cause the robot to stop moving.
|[in]
|lower_torque_thresholds_acceleration

…

|NE_T_EE
|Vectorized NE-to-EE transformation matrix \(^{NE}T_{EE}\), column-major.
|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|void franka::Robot::setFilters
|(
|double
|joint_position_filter_frequency,
|double
|joint_velocity_filter_frequency,
|double
|cartesian_position_filter_frequency,
|double
|cartesian_velocity_filter_frequency,
|double
|controller_filter_frequency
|)
Sets the cut off frequency for the given motion generator or controller.
Allowed input range for all the filters is between 1.0 Hz and 1000.0 Hz. If the value is set to maximum (1000Hz) then no filtering is done.

…

|[in]
|cartesian_velocity_filter_frequency
|Frequency at which the commanded Cartesian velocity is cut off.
|[in]
|controller_filter_frequency
|Frequency at which the commanded torque is cut off.
|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.

…

|[in]
|guiding_mode
|Unlocked movement in (x, y, z, R, P, Y) in guiding mode.
|[in]
|elbow
|True if the elbow is free in guiding mode, false otherwise.
|CommandException
|if the Control reports an error.

…

|[in]
|K_theta
|Joint impedance values \(K_{\theta}\).
|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|void franka::Robot::setK
|(
|const std::array< double, 16 > &

…

|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|void franka::Robot::setLoad
|(
|double
|load_mass,
|const std::array< double, 3 > &
|F_x_Cload,
|const std::array< double, 9 > &
|load_inertia
|)
Sets dynamic parameters of a payload.
|[in]
|load_mass
|Mass of the load in \([kg]\).
|[in]
|F_x_Cload
|Translation from flange to center of mass of load \(^Fx_{C_\text{load}}\) in \([m]\).
|[in]
|load_inertia
|Inertia matrix \(I_\text{load}\) in \([kg \times m^2]\), column-major.
|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.
|void franka::Robot::stop
|(
|)
Stops all currently running motions.
If a control or motion generator loop is running in another thread, it will be preempted with a franka::ControlException.
|CommandException
|if the Control reports an error.
|NetworkException
|if the connection is lost, e.g. after a timeout.

Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot. More...

```
#include <robot.h>
```
|## Public Types|
|--|
|using|
|Version of the robot server. More...|
|## Public Member Functions|
|--|
|Model|
|Loads the model library from the robot. More...|
|Robot &|
|Move-assigns this Robot from another Robot instance. More...|
|void|
|Starts a loop for reading the current robot state. More...|
|RobotState|
|Waits for a robot state update and returns it. More...|
|Robot (const std::string &franka_address, RealtimeConfig realtime_config=RealtimeConfig::kEnforce, size_t log_size=50)|
|Establishes a connection with the robot. More...|
|Robot (Robot &&other) noexcept|
|Move-constructs a new Robot instance. More...|
|ServerVersion|
|Returns the software version reported by the connected server. More...|
|~Robot () noexcept|
|Closes the connection. More...|
|Motion generation and joint-level torque commands|
|The following methods allow to perform motion generation and/or send joint-level torque commands without gravity and friction by providing callback functions.Only one of these methods can be active at the same time; a franka::ControlException is thrown otherwise.When a robot state is received, the callback function is used to calculate the response: the desired values for that time step. After sending back the response, the callback function will be called again with the most recently received robot state. Since the robot is controlled with a 1 kHz frequency, the callback functions have to compute their result in a short time frame in order to be accepted. Callback functions take two parameters:The following incomplete example shows the general structure of a callback function:double time = 0.0;auto control_callback = [&time](const franka::RobotState& robot_state,franka::Duration time_step) -> franka::JointPositions {time += time_step.toSec(); // Update time at the beginning of the callback.franka::JointPositions output = getJointPositions(time);if (time >= max_time) {// Return MotionFinished at the end of the trajectory.return franka::MotionFinished(output);}return output;}|
|void|
|Starts a control loop for sending joint-level torque commands. More...|
|void|
|Starts a control loop for sending joint-level torque commands and joint positions. More...|
|void|
|Starts a control loop for sending joint-level torque commands and joint velocities. More...|
|void|
|Starts a control loop for sending joint-level torque commands and Cartesian poses. More...|
|void|
|Starts a control loop for sending joint-level torque commands and Cartesian velocities. More...|
|void|
|Starts a control loop for a joint position motion generator with a given controller mode. More...|
|void|
|Starts a control loop for a joint velocity motion generator with a given controller mode. More...|
|void|
|Starts a control loop for a Cartesian pose motion generator with a given controller mode. More...|
|void|
|Starts a control loop for a Cartesian velocity motion generator with a given controller mode. More...|
|Commands|
|Commands are executed by communicating with the robot over the network.These functions should therefore not be called from within control or motion generator loops.|
|VirtualWallCuboid|
|Returns the parameters of a virtual wall. More...|
|void|
|Changes the collision behavior. More...|
|void|
|Changes the collision behavior. More...|
|void|
|Sets the impedance for each joint in the internal controller. More...|
|void|
|Sets the Cartesian impedance for (x, y, z, roll, pitch, yaw) in the internal controller. More...|
|void|
|Locks or unlocks guiding mode movement in (x, y, z, roll, pitch, yaw). More...|
|void|
|Sets the transformation from end effector frame to stiffness frame. More...|
|void|
|Sets the transformation from flange to end effector frame. More...|
|void|
|Sets dynamic parameters of a payload. More...|
|void|
|Sets the cut off frequency for the given motion generator or controller. More...|
|void|
|Runs automatic error recovery on the robot. More...|
|void|
|Stops all currently running motions. More...|
|## Private Attributes|
|--|
|std::mutex|
|std::unique_ptr< Impl >|

Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot.

using franka::Robot::ServerVersion = uint16_t

|<table></table>|explicit|
|--|--|

Establishes a connection with the robot.

|[in]|franka_address|IP/hostname of the robot.|
|--|--|--|
|[in]|realtime_config|if set to Enforce, an exception will be thrown if realtime priority cannot be set when required. Setting realtime_config to Ignore disables this behavior.|
|[in]|log_size|sets how many last states should be kept for logging purposes. The log is provided when a ControlException is thrown.|
|NetworkException|if the connection is unsuccessful.|
|--|--|
|IncompatibleVersionException|if this version of
``` libfranka ``` is not supported.|
|<table></table>|noexcept|
|--|--|
|<table></table>|noexcept|
|--|--|

Closes the connection.

|void franka::Robot::automaticErrorRecovery|(|)|
|--|--|--|

Runs automatic error recovery on the robot.

Automatic error recovery e.g. resets the robot after a collision occurred.

|CommandException|if the Control reports an error.|
|--|--|
|NetworkException|if the connection is lost, e.g. after a timeout.|
|void franka::Robot::control|(|std::function< Torques(const RobotState &, franka::Duration)>|control_callback,|
|--|--|--|--|
|bool|limit_rate =
``` true ``` ,| | |
|double|cutoff_frequency =
``` kDefaultCutoffFrequency ```| | |
|)| | | |

Starts a control loop for sending joint-level torque commands.

Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.

|[in]|control_callback|Callback function providing joint-level torque commands. See here for more details.|
|--|--|--|
|[in]|limit_rate|True if rate limiting should be activated. True by default. This could distort your motion!|
|[in]|cutoff_frequency|Cutoff frequency for a first order low-pass filter applied on the user commanded signal. Set to franka::kMaxCutoffFrequency to disable.|
|ControlException|if an error related to torque control or motion generation occurred.|
|--|--|
|InvalidOperationException|if a conflicting operation is already running.|
|NetworkException|if the connection is lost, e.g. after a timeout.|
|RealtimeException|if realtime priority cannot be set for the current thread.|
|std::invalid_argument|if joint-level torque commands are NaN or infinity.|
|void franka::Robot::control|(|std::function< Torques(const RobotState &, franka::Duration)>|control_callback,|
|--|--|--|--|
|std::function< JointPositions(const RobotState &, franka::Duration)>|motion_generator_callback,| | |
|bool|limit_rate =
``` true ``` ,| | |
|double|cutoff_frequency =
``` kDefaultCutoffFrequency ```| | |
|)| | | |

Starts a control loop for sending joint-level torque commands and joint positions.

Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.

|[in]|control_callback|Callback function providing joint-level torque commands. See here for more details.|
|--|--|--|
|[in]|motion_generator_callback|Callback function for motion generation. See here for more details.|
|[in]|limit_rate|True if rate limiting should be activated. True by default. This could distort your motion!|
|[in]|cutoff_frequency|Cutoff frequency for a first order low-pass filter applied on the user commanded signal. Set to franka::kMaxCutoffFrequency to disable.|
|ControlException|if an error related to torque control or motion generation occurred.|
|--|--|
|InvalidOperationException|if a conflicting operation is already running.|
|NetworkException|if the connection is lost, e.g. after a timeout.|
|RealtimeException|if realtime priority cannot be set for the current thread.|
|std::invalid_argument|if joint-level torque or joint position commands are NaN or infinity.|
|void franka::Robot::control|(|std::function< Torques(const RobotState &, franka::Duration)>|control_callback,|
|--|--|--|--|
|std::function< JointVelocities(const RobotState &, franka::Duration)>|motion_generator_callback,| | |
|bool|limit_rate =
``` true ``` ,| | |
|double|cutoff_frequency =
``` kDefaultCutoffFrequency ```| | |
|)| | | |

Starts a control loop for sending joint-level torque commands and joint velocities.

Sets realtime priority for the current thread. Cannot be executed while another control or motion generator loop is active.
|[in]|control_callback|Callback function providing joint-level torque commands. See here for more details.|
|--|--|--|
|[in]|motion_generator_callback|Callback function for motion generation. See here for more details.|
|[in]|limit_rate|True if rate limiting should be activated. True by default. This could distort your motion!|

…

|NetworkException|if the connection is lost, e.g. after a timeout.|
|RealtimeException|if realtime priority cannot be set for the current thread.|
|std::invalid_argument|if joint-level torque or joint velocitiy commands are NaN or infinity.|
|void franka::Robot::control|(|std::function< Torques(const RobotState &, franka::Duration)>|control_callback,|

…

|[in]|control_callback|Callback function providing joint-level torque commands. See here for more details.|
|--|--|--|
|[in]|motion_generator_callback|Callback function for motion generation. See here for more details.|
|[in]|limit_rate|True if rate limiting should be activated. True by default. This could distort your motion!|

…

|NetworkException|if the connection is lost, e.g. after a timeout.|
|RealtimeException|if realtime priority cannot be set for the current thread.|
|std::invalid_argument|if joint-level torque or Cartesian pose command elements are NaN or infinity.|
|void franka::Robot::control|(|std::function< Torques(const RobotState &, franka::Duration)>|control_callback,|

…

|NetworkException|if the connection is lost, e.g. after a timeout.|
|RealtimeException|if realtime priority cannot be set for the current thread.|
|std::invalid_argument|if joint velocity commands are NaN or infinity.|
|void franka::Robot::control|(|std::function< CartesianPose(const RobotState &, franka::Duration)>|motion_generator_callback,|

…

|const std::array< double, 6 > &|upper_force_thresholds_nominal| | |
|)| | | |

Changes the collision behavior.

Set separate torque and force boundaries for acceleration/deceleration and constant velocity movement phases.

Forces or torques between lower and upper threshold are shown as contacts in the RobotState. Forces or torques above the upper threshold are registered as collision and cause the robot to stop moving.

## Expand description
Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot.
…
- A &franka::RobotState showing the current robot state.
- A &std::time::Duration to indicate the time since the last callback invocation.
Thus, the duration is zero on the first invocation of the callback function!
The following incomplete example shows the general structure of a callback function:

|libfranka 0.14.1 FCI C++ API|
|--|
|▼N franka|
|--|
|CActiveControl|Documented in ActiveControlBase|
|CActiveControlBase|Allows the user to read the state of a Robot and to send new control commands after starting a control process of a Robot|
|CActiveMotionGenerator|Allows the user to read the state of a Robot and to send new motion generator commands after starting a control process of a Robot|
|CActiveTorqueControl|Allows the user to read the state of a Robot and to send new torque control commands after starting a control process of a Robot|
|CFinishable|Helper type for control and motion generation loops|
|CTorques|Stores joint-level torque commands without gravity and friction|
|CJointPositions|Stores values for joint position motion generation|
|CJointVelocities|Stores values for joint velocity motion generation|
|CCartesianPose|Stores values for Cartesian pose motion generation|
|CCartesianVelocities|Stores values for Cartesian velocity motion generation|
|CDuration|Represents a duration with millisecond resolution|
|CErrors|Enumerates errors that can occur while controlling a franka::Robot|
|CException|Base class for all exceptions used by `libfranka`|
|CModelException|ModelException is thrown if an error occurs when loading the model library|
|CNetworkException|NetworkException is thrown if a connection to the robot cannot be established, or when a timeout occurs|
|CProtocolException|ProtocolException is thrown if the robot returns an incorrect message|
|CIncompatibleVersionException|IncompatibleVersionException is thrown if the robot does not support this version of libfranka|
|CControlException|ControlException is thrown if an error occurs during motion generation or torque control|
|CCommandException|CommandException is thrown if an error occurs during command execution|
|CRealtimeException|RealtimeException is thrown if realtime priority cannot be set|
|CInvalidOperationException|InvalidOperationException is thrown if an operation cannot be performed|
|CGripper|Maintains a network connection to the gripper, provides the current gripper state, and allows the execution of commands|
|CGripperState|Describes the gripper state|
|CRobotCommand|Command sent to the robot|
|CRecord|One row of the log contains a robot command of timestamp n and a corresponding robot state of timestamp n+1|
|CModel|Calculates poses of joints and dynamic properties of the robot|
|CRobot|Maintains a network connection to the robot, provides the current robot state, gives access to the model library and allows to control the robot|
|CRobotModel|Implements RobotModelBase using Pinocchio|
|CRobotState|Describes the robot state|
|CVacuumGripper|Maintains a network connection to the vacuum gripper, provides the current vacuum gripper state, and allows the execution of commands|
|CVacuumGripperState|Describes the vacuum gripper state|
|CMotionGenerator|An example showing how to generate a joint pose motion to a goal position|
|CRobotModelBase|Robot dynamic parameters computed from the URDF model with Pinocchio|