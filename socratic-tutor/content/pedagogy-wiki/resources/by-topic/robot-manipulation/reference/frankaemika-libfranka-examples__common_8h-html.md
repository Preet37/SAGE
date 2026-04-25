# Source: https://frankaemika.github.io/libfranka/examples__common_8h.html
# Title: ◆ setDefaultBehavior()
# Fetched via: search
# Date: 2026-04-09

frankaemika / **
...
#include <iostream>
#include <thread>
#include <franka/active_control.h>
#include <franka/active_torque_control.h>
#include <franka/duration.h>
#include <franka/exception.h>
#include <franka/robot.h>
#include "examples_common.h"
/**
* @example communication_test.cpp
* An example indicating the network performance.
*
* @warning Before executing this example, make sure there is enough space in front of the robot.
*/
int main(int argc, char** argv) {
if (argc != 2) {
std::cerr << "Usage: " << argv[0] << " <robot-hostname>" << std::endl;
return -1;
}
uint64_t counter = 0;
double avg_success_rate = 0.0;
double min_success_rate = 1.0;
double max_success_rate = 0.0;
uint64_t time = 0;
std::cout.precision(2);
std::cout << std::fixed;
try {
franka::Robot robot(argv[1]);
setDefaultBehavior(robot);
// First move the robot to a suitable joint configuration
std::array<double, 7> q_goal = {{0, -M_PI_4, 0, -3 * M_PI_4, 0, M_PI_2, M_PI_4}};
MotionGenerator motion_generator(0.5, q_goal);
std::cout << "WARNING: This example will move the robot!
"
<< "Please make sure to have the user stop button at hand!"
<< std::endl
<< "Press Enter to continue..."
<< std::endl;
std::cin.ignore();
robot.control(motion_generator);
std::cout << "Finished moving to initial joint configuration."
<< std::endl << std::endl;
std::cout << "Starting communication test."
<< std::endl;
robot.setCollisionBehavior(
{{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
{{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}}, {{20.0, 20.0, 18.0, 18.0, 16.0, 14.0, 12.0}},
{{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}},
{{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}}, {{20.0, 20.0, 20.0, 25.0, 25.0, 25.0}});
franka::Torques zero_torques{{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
auto rw_interface = robot.startTorqueControl();
franka::RobotState robot_state;
franka::Duration period;
while (!zero_torques.motion_finished) {
std::tie(robot_state, period) = rw_interface->readOnce();
time += period.toMSec();
if (time == 0.0) {
rw_interface->writeOnce(zero_torques);
continue;
}
counter++;
if (counter % 100 == 0) {
std::cout << "#" << counter
<< " Current success rate: " << robot_state.control_command_success_rate
<< std::endl;
}
std::this_thread::sleep_for(std::chrono::microseconds(100));
avg_success_rate += robot_state.control_command_success_rate;
if (robot_state.control_command_success_rate > max_success_rate) {
max_success_rate = robot_state.control_command_success_rate;
}
if (robot_state.control_command_success_rate < min_success_rate) {
min_success_rate = robot_state.control_command_success_rate;
}
if (time >= 10000) {
std::cout << std::endl << "Finished test, shutting down example" << std::endl;
zero_torques.motion_finished = true;
}
// Sending zero torques - if EE is configured correctly, robot should not move
rw_interface->writeOnce(zero_torques);
}
} catch (const franka::Exception& e) {
std::cout << e.what() << std::endl;
return -1;
}
avg_success_rate = avg_success_rate / counter;
std::cout << std::endl
<< std::endl
<< "#######################################################" << std::endl;
uint64_t lost_robot_states = time - counter;
if (lost_robot_states > 0) {
std::cout << "The control loop did not get executed " << lost_robot_states << " times in the"
<< std::endl
<< "last " << time << " milliseconds!
(lost " << lost_robot_states << " robot states)"
<< std::endl
<< std::endl;
}
std::cout << "Control command success rate of " << counter << " samples: " << std::endl;
std::cout << "Max: " << max_success_rate << std::endl;
std::cout << "Avg: " << avg_success_rate << std::endl;
std::cout << "Min: " << min_success_rate << std::endl;
if (avg_success_rate < 0.90) {
std::cout << std::endl
<< "WARNING: THIS SETUP IS PROBABLY NOT SUFFICIENT FOR FCI!"
<< std::endl;
std::cout << "PLEASE TRY OUT A DIFFERENT PC / NIC" << std::endl;
} else if (avg_success_rate < 0.95) {
std::cout << std::endl << "WARNING: MANY PACKETS GOT LOST!"
<< std::endl;
std::cout << "PLEASE INSPECT YOUR SETUP AND FOLLOW ADVICE ON" << std::endl
<< "https://frankaemika.github.io/docs/troubleshooting.html" << std::endl;
}
std::cout << "#######################################################" << std::endl << std::endl;
return 0;
}
```

# Usage Examples
The following examples demonstrate how to use libfranka in both C++ and Python:
**C++ Example Programs:** **Python Example Programs:**
The following examples demonstrate how to use libfranka in both C++ and Python:
**C++ Example Programs:**
**Python Example Programs:**

frankarobotics / **
docs ** Public

##

## Files

# libfranka.rst

## Latest commit

BarisYazici

chore: remove the changelog sections

Feb 20, 2025

c46d208 · Feb 20, 2025

## History
History

620 lines (468 loc) · 29.1 KB

# libfranka.rst

620 lines (468 loc) · 29.1 KB

# libfranka

Before continuing with this chapter, please install or compile libfranka for :doc:`Linux <installation_linux>`.

API documentation for the latest version of
```
libfranka
```
is available at
https://frankaemika.github.io/libfranka .

Libfranka changelog is available at CHANGELOG.md .
Schematic overview

```
libfranka
```
is the C++ implementation of the client side of the FCI. It handles the network
communication with Control and provides interfaces to easily:

- execute **non-realtime commands** to control the Hand and configure Arm parameters.
- execute **realtime commands** to run your own 1 kHz control loops.
- read the **robot state** to get sensor data at 1 kHz.
- access the **model library** to compute your desired kinematic and dynamic parameters.

…

- ```
  homing
  ```
  which calibrates the maximum grasping width of the Hand.
- ```
  move
  ```
  ,
  ```
  grasp
  ```
  and
  ```
  stop
  ```
  , to move or grasp with the Hand.
- ```
  readOnce
  ```
  , which reads the Hand state.
Concerning the Arm, some useful non-realtime commands are:
- ```
  setCollisionBehavior
  ```
  which sets the contact and collision detection thresholds.
- ```
  setCartesianImpedance
  ```
  and
  ```
  setJointImpedance
  ```
  which set the impedance parameters
  for the internal Cartesian impedance and internal joint impedance controllers.
- ```
  setEE
  ```
  sets the transformation *NE_T_EE* from nominal end effector to end effector frame. The transformation from flange to end effector frame *F_T_EE* is split into two transformations: *F_T_NE* and *NE_T_EE*. The transformation from flange to nominal end effector frame *F_T_NE* can only be set through the administrator's interface.
- ```
  setK
  ```
  sets the transformation *EE_T_K* from end effector frame to stiffness frame.
- ```
  setLoad
  ```
  sets the dynamic parameters of a payload.
- ```
  automaticErrorRecovery
  ```
  that clears any command or control exception that previously
  happened in the robot.
For a complete and fully specified list check the API documentation for the
:api:`Robot|classfranka_1_1Robot.html` or the :api:`Gripper|classfranka_1_1Gripper.html`.

All operations (non-realtime or realtime) on the Arm or the Hand are performed through the
```
franka::Robot
```
and
```
franka::Gripper
```
objects respectively. A connection to the Arm/Hand
will be established when the object is created:

```
#include <franka/robot.h>
#include <franka/gripper.h>

...

franka::Gripper gripper("<fci-ip>");
franka::Robot robot("<fci-ip>");
```
The address can be passed either as a hostname or an IP address. In case of any error, either due
to networking or conflicting library version, an exception of type
```
franka::Exception
```
will
be thrown. When using several robots at the same time, simply create several objects with
appropriate IP addresses.
To run a specific command, simply call the corresponding method, e.g.

```
gripper.homing();
robot.automaticErrorRecovery();
```

## Realtime commands

Realtime commands are UDP based and require a 1 kHz connection to Control.
There are two types of realtime interfaces:

- **Motion generators**, which define a robot motion in joint or Cartesian space.
- **Controllers**, which define the torques to be sent to the robot joints.

There are 4 different types of external motion generators and 3 different types of controllers
(one external and 2 internal) as depicted in the following figure:
Realtime interfaces: motion generators and controllers.

You can either use a single interface or combine two different types. Specifically, you can
command:

- *only a motion generator* and therefore use one of the two internal controllers to follow the commanded motion.
- *only an external controller* and ignore any motion generator signals, i.e. torque control only.
- *a motion generator and an external controller* to use the inverse kinematics of Control in your external controller.
All realtime loops (motion generator or controller) are defined by a callback function that
receives the robot state and the duration of the last cycle (1 ms unless packet losses occur)
and returns the specific type of the interface. The
```
control
```
method of the
```
franka::Robot
```
class will then run the control loop by executing the callback function at a 1 kHz frequency,
as shown in this example

…

...

try {
  franka::Robot robot("<fci-ip>");
  // only a motion generator
  robot.control(my_external_motion_generator_callback);
  // only an external controller
  robot.control(my_external_controller_callback);
  // a motion generator and an external controller
  robot.control(my_external_motion_generator_callback, my_external_controller_callback);
} catch (franka::Exception const& e) {
  std::cout << e.what() << std::endl;
  return -1;
}
  return 0;
}
```
All control loops are finished once the
```
motion_finished
```
flag of a realtime command is set
to
```
true
```
. An excerpt of the
```
generate_joint_velocity_motion
```
example included
in the :api:`libfranka examples|examples.html` is shown here
```
robot.control(
     [=, &time](const franka::RobotState&, franka::Duration period) -> franka::JointVelocities {
       time += period.toSec();

       double cycle = std::floor(std::pow(-1.0, (time - std::fmod(time, time_max)) / time_max));
       double omega = cycle * omega_max / 2.0 * (1.0 - std::cos(2.0 * M_PI / time_max * time));

       franka::JointVelocities velocities = {{0.0, 0.0, 0.0, omega, omega, omega, omega}};

       if (time >= 2 * time_max) {
         std::cout << std::endl << "Finished motion, shutting down example" << std::endl;
         return franka::MotionFinished(velocities);
       }
       return velocities;
     });
```
In this case, the callback function is defined directly in the call of the

```
robot.control( ... )
```
function. It uses the joint velocity motion generator interface,
as it returns a
```
franka::JointVelocities
```
object. It commands joint velocities to the last four
joints and move them by approx. +/-12 degrees. After
```
2 * time_max
```
seconds it will return a

```
motion_finished
```
flag by setting it to true with the
```
franka::MotionFinished
```
method and
the control loop will stop.

Note that if you use only a motion generator, the default controller is the internal joint
impedance controller. You can however use the internal Cartesian impedance controller by
setting the optional argument of the control function, e.g.

…

For writing a controller, the
```
franka::Robot::control
```
function is used as well. The following
example shows a simple controller commanding zero torque for each joint. Gravity is
compensated by the robot.

```
robot.control([&](const franka::RobotState&, franka::Duration) -> franka::Torques {
      return {{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0}};
    });
```
You can find examples for all interfaces and combinations of control loops in the
:api:`examples|examples.html`. Prior to running the examples, verify that the robot has enough free space to move without colliding. Then, for instance for the
```
generate_joint_velocity_motion
```
example execute the following command from
the

…

### Signal processing

To facilitate the control of the robot under non-ideal network connections, libfranka includes
signal processing functions that will modify the user-commanded values to make them conform
with the :ref:`limits of the interface<control_parameters_specifications>`. There are two *optional* functions included in all realtime control loops:
- A first-order **low-pass filter** to smooth the user-commanded signal.
- A **rate limiter**, that saturates the time derivatives of the user-commanded values.
- As of version
  ```
  0.5.0
  ```
  , libfranka includes a **low-pass filter** for all realtime interfaces **running by default** with a 100 Hz cutoff frequency. The filter smooths commanded signals to provide more stable robot motions but does not prevent the violation of the :ref:`limits of the interface<control_parameters_specifications>`.

…

The limits used in the rate limiter are defined in
  ```
  franka/rate_limiting.h
  ```

  and are set to the interface limits. If this produces a jerky or unstable behavior
  you can set the limits to lower values, activate the low-pass filter or reduce its cutoff
  frequency.
To control the signal processing functions, all
```
robot.control()
```
function calls
have two additional optional parameters. The first one is a flag to activate or
deactivate the rate limiter while the second one
specifies the cutoff frequency of the first-order low-pass filter. If the cutoff frequency

```
>=1000.0
```

…

// Identical to the previous line (default true, 100.0 Hz cutoff)
robot.control(my_external_motion_generator_callback, franka::ControllerMode::kCartesianImpedance, true, 100.0);
// Runs my_external_motion_generator_callback with the Cartesian impedance controller,
// rate limiters off and low-pass filter off
robot.control(my_external_motion_generator_callback, franka::ControllerMode::kCartesianImpedance, false, 1000.0);
```
Or similarly for an external controller

```
// With rate limiting and filter
robot.control(my_external_controller);
// Identical to the previous line (default true, 100.0 Hz cutoff)
robot.control(my_external_controller, true, 100.0);
// Without rate limiting but with low-pass filter (100.0 Hz)
robot.control(my_external_controller, false);
// Without rate limiting and without low-pass filter
robot.control(my_external_controller, false, 1000.0);
```

…

**Motion generators**: all motion generator commands sent by the user have the subscript c which stands for 'commanded'. When a motion generator is sent, the Robot Kinematics completion block will compute the forward/inverse kinematics of the user-commanded signal yielding the 'desired' signals, subscript d.

…

All variables on the Control side of the figure, i.e. the last received c values (after the low pass filter and the extrapolation due to packet losses, read below for an explanation), the computed d values and their time derivatives are sent back to the user in the robot state. This way you can take advantage of the inverse kinematics in your own external controller and, at the same time, it will offer you full transparency: you will always know the exact values and derivatives that the robot received and tracked in the last sample.

…

- \tau_{d} is the desired torque given as input by the libfranka user,
- \tau_{c} is the torque effectively commanded to the joint,
- \tau_{f} is the torque to compensate the motor friction,
- \tau_{g} is the torque required for compensating the gravity of the whole kinematic chain.

…

```
read
```
or
```
readOnce
```
can be used to gather it, e.g. for
logging or visualization purposes.

With a valid connection, *a single sample of the robot state* can be read using the
```
readOnce
```

function:

```
franka::RobotState state = robot.readOnce();
```
The next example shows how to continuously read the robot state using the
```
read
```
function and a
callback. Returning
```
false
```
in the callback stops the loop. In the following, an excerpt of the

```
echo_robot_state
```
example is shown:

…

## Model library

The robot model library provides

- The forward kinematics of all robot joints.
- The body and zero jacobian matrices of all robot joints.
- Dynamic parameters: inertia matrix, Coriolis and centrifugal vector and gravity vector.
Note that after you load the model library, you can compute kinematic and dynamic parameters for
an arbitrary robot state, not just the current one. You can also use the model library in a non
realtime fashion, e.g. in an optimization loop. The libfranka examples include exemplary code for
:api:`printing joint poses|print_joint_poses_8cpp-example.html` or :api:`computing jacobians|cartesian_impedance_control_8cpp-example.html`.

…

```
double time{0.0};
robot.control(
 [=, &time](const franka::RobotState& robot_state, franka::Duration period) -> franka::JointPositions {
   time += period.toSec();
   if (time == 0) {
     // Send the last commanded q_c as the initial value
     return franka::JointPositions(robot_state.q_c);
   } else {
     // The rest of your control loop
     ...
   }
 });
```

…

where \Delta t = 0.001. Note that q_{c,k-1}, \dot{q}_{c,k-1} and \ddot{q}_{c,k-1} are always sent back to the user in the robot state as q_{d}, \dot{q}_{d} and \ddot{q}_{d} so you will be able to compute the resulting derivatives in advance, even in case of packet losses. Check the :ref:`section about the details of the Control side of the interface<control-side>` for more details.

**libfranka**Public



Notifications

You must be signed in to change notification settings

- Fork 147



# robot.h

## Latest commit

## HistoryHistory724 lines (682 loc) · 31.9 KB

# robot.h

## File metadata and controls

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

…

724// Copyright (c) 2017 Franka Emika GmbH// Use of this source code is governed by the Apache-2.0 license, see LICENSE/** * @file robot.h * Contains the franka::Robot type. *//** * Maintains a network connection to the robot, provides the current robot state, gives access to * the model library and allows to control the robot. * * @note * The members of this class are threadsafe. * * @anchor o-frame * @par Base frame O * The base frame is located at the center of the robot's base.
Its z-axis is identical with the * axis of rotation of the first joint. * * @anchor f-frame * @par Flange frame F * The flange frame is located at the center of the flange surface. Its z-axis is identical with the * axis of rotation of the last joint. This frame is fixed and cannot be changed. * * @anchor ne-frame * @par Nominal end effector frame NE * The nominal end effector frame is configured outside of libfranka (in DESK) and cannot be changed * here.
It may be used to set end effector frames which are rarely changed. * * @anchor ee-frame * @par end effector frame EE * By default, the end effector frame EE is the same as the nominal end effector frame NE * (i.e. the transformation between NE and EE is the identity transformation).
It may be used to set * end effector frames which are changed more frequently (such as a tool that is grasped with the * end effector). With Robot::setEE, a custom transformation matrix can be set. * * @anchor k-frame * @par Stiffness frame K * This frame describes the transformation from the end effector frame EE to the stiffness frame K.
* The stiffness frame is used for Cartesian impedance control, and for measuring and applying * forces. The values set using Robot::setCartesianImpedance are used in the direction of the * stiffness frame. It can be set with Robot::setK. * This frame allows to modify the compliance behavior of the robot (e.g. to have a low * stiffness around a specific point which is not the end effector).
The stiffness frame does not * affect where the robot will move to. The user should always command the desired end effector * frame (and not the desired stiffness frame). */ * Version of the robot server. */ * Establishes a connection with the robot. * * @param[in] franka_address IP/hostname of the robot. * @param[in] realtime_config if set to Enforce, an exception will be thrown if realtime priority * cannot be set when required.

…

*/ * Move-constructs a new Robot instance. * * @param[in] other Other Robot instance. */ * Move-assigns this Robot from another Robot instance. * * @param[in] other Other Robot instance. * * @return Robot instance. */ * Closes the connection. */ * @name Motion generation and joint-level torque commands * * The following methods allow to perform motion generation and/or send joint-level torque * commands without gravity and friction by providing callback functions.
* * Only one of these methods can be active at the same time; a franka::ControlException is thrown * otherwise. * * @anchor callback-docs * When a robot state is received, the callback function is used to calculate the response: the * desired values for that time step. After sending back the response, the callback function will * be called again with the most recently received robot state.
Since the robot is controlled with * a 1 kHz frequency, the callback functions have to compute their result in a short time frame * in order to be accepted. Callback functions take two parameters: * * * A franka::RobotState showing the current robot state. * * A franka::Duration to indicate the time since the last callback invocation.
Thus, the * duration is zero on the first invocation of the callback function!

* * The following incomplete example shows the general structure of a callback function: * * @code{.cpp} * double time = 0.0; * auto control_callback = [&time](const franka::RobotState& robot_state, * franka::Duration time_step) -> franka::JointPositions
{ * time += time_step.toSec(); // Update time at the beginning of the callback. * * franka::JointPositions output = getJointPositions(time); * * if (time >= max_time) { * // Return MotionFinished at the end of the trajectory. * return franka::MotionFinished(output); * } * * return output; * } * @endcode * * @{ */ * Starts a control loop for sending joint-level torque commands.
* * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] control_callback Callback function providing joint-level torque commands. * See @ref callback-docs "here" for more details. * @param[in] limit_rate True if rate limiting should be activated.

…

Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to torque control or motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if joint-level torque commands are NaN or infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for sending joint-level torque commands and joint positions. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] control_callback Callback function providing joint-level torque commands. * See @ref callback-docs "here" for more details. * @param[in] motion_generator_callback Callback function for motion generation.
See @ref * callback-docs "here" for more details. * @param[in] limit_rate True if rate limiting should be activated. True by default. * This could distort your motion! * @param[in] cutoff_frequency Cutoff frequency for a first order low-pass filter applied on * the user commanded signal.
Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to torque control or motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if joint-level torque or joint position commands are NaN or * infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for sending joint-level torque commands and joint velocities. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] control_callback Callback function providing joint-level torque commands. * See @ref callback-docs "here" for more details. * @param[in] motion_generator_callback Callback function for motion generation.
See @ref * callback-docs "here" for more details. * @param[in] limit_rate True if rate limiting should be activated. True by default. * This could distort your motion! * @param[in] cutoff_frequency Cutoff frequency for a first order low-pass filter applied on * the user commanded signal.
Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to torque control or motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if joint-level torque or joint velocity commands are NaN or * infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for sending joint-level torque commands and Cartesian poses. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] control_callback Callback function providing joint-level torque commands. * See @ref callback-docs "here" for more details. * @param[in] motion_generator_callback Callback function for motion generation.
See @ref * callback-docs "here" for more details. * @param[in] limit_rate True if rate limiting should be activated. True by default. * This could distort your motion! * @param[in] cutoff_frequency Cutoff frequency for a first order low-pass filter applied on * the user commanded signal.
Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to torque control or motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if joint-level torque or Cartesian pose command elements are NaN * or infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for sending joint-level torque commands and Cartesian velocities. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] control_callback Callback function providing joint-level torque commands. * See @ref callback-docs "here" for more details. * @param[in] motion_generator_callback Callback function for motion generation.
See @ref * callback-docs "here" for more details. * @param[in] limit_rate True if rate limiting should be activated. True by default. * This could distort your motion! * @param[in] cutoff_frequency Cutoff frequency for a first order low-pass filter applied on * the user commanded signal.
Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to torque control or motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if joint-level torque or Cartesian velocity command elements are * NaN or infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for a joint position motion generator with a given controller mode. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] motion_generator_callback Callback function for motion generation. See @ref * callback-docs "here" for more details. * @param[in] controller_mode Controller to use to execute the motion. * @param[in] limit_rate True if rate limiting should be activated.

…

Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if joint position commands are NaN or infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for a joint velocity motion generator with a given controller mode. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] motion_generator_callback Callback function for motion generation. See @ref * callback-docs "here" for more details. * @param[in] controller_mode Controller to use to execute the motion. * @param[in] limit_rate True if rate limiting should be activated.

…

Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if joint velocity commands are NaN or infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for a Cartesian pose motion generator with a given controller mode. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] motion_generator_callback Callback function for motion generation. See @ref * callback-docs "here" for more details. * @param[in] controller_mode Controller to use to execute the motion. * @param[in] limit_rate True if rate limiting should be activated.

…

Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if Cartesian pose command elements are NaN or infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.
*/ * Starts a control loop for a Cartesian velocity motion generator with a given controller mode. * * Sets realtime priority for the current thread. * Cannot be executed while another control or motion generator loop is active. * * @param[in] motion_generator_callback Callback function for motion generation. See @ref * callback-docs "here" for more details. * @param[in] controller_mode Controller to use to execute the motion. * @param[in] limit_rate True if rate limiting should be activated.

…

Set to franka::kMaxCutoffFrequency to disable. * * @throw ControlException if an error related to motion generation occurred. * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * @throw RealtimeException if realtime priority cannot be set for the current thread. * @throw std::invalid_argument if Cartesian velocity command elements are NaN or infinity. * * @see Robot::Robot to change behavior if realtime priority cannot be set.

…

* * This minimal example will print the robot state 100 times: * @code{.cpp} * franka::Robot robot("robot.franka.de"); * size_t count = 0; * robot.read([&count](const franka::RobotState& robot_state) { * std::cout <<
robot_state << std::endl; * return count++ < 100; * }); * @endcode * * @param[in] read_callback Callback function for robot state reading. * * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout.
*/ * Waits for a robot state update and returns it. * * Cannot be executed while a control or motion generator loop is running. * * @return Current robot state. * * @throw InvalidOperationException if a conflicting operation is already running. * @throw NetworkException if the connection is lost, e.g. after a timeout. * * @see Robot::read for a way to repeatedly receive the robot state. */ * @name Commands * * Commands are executed by communicating with the robot over the network.

…

*/ * Changes the collision behavior. * * Set separate torque and force boundaries for acceleration/deceleration and constant velocity * movement phases. * * Forces or torques between lower and upper threshold are shown as contacts in the RobotState.

…

*/ * Changes the collision behavior. * * Set common torque and force boundaries for acceleration/deceleration and constant velocity * movement phases. * * Forces or torques between lower and upper threshold are shown as contacts in the RobotState.

…

*/ * Sets the transformation \f$^{EE}T_K\f$ from end effector frame to stiffness frame. * * The transformation matrix is represented as a vectorized 4x4 matrix in column-major format. * * @param[in] EE_T_K Vectorized EE-to-K transformation matrix \f$^{EE}T_K\f$, column-major. * * @throw CommandException if the Control reports an error. * @throw NetworkException if the connection is lost, e.g. after a timeout. * * @see Robot for an explanation of the stiffness frame.

…

Translation from flange to center of mass of load * \f$^Fx_{C_\text{load}}\f$ in \f$[m]\f$. * @param[in] load_inertia Inertia matrix \f$I_\text{load}\f$ in \f$[kg \times m^2]\f$, * column-major. * * @throw CommandException if the Control reports an error. * @throw NetworkException if the connection is lost, e.g. after a timeout.
*/ * Sets the cut off frequency for the given motion generator or controller. * * @deprecated Use franka::lowpassFilter() instead. * * Allowed input range for all the filters is between 1.0 Hz and 1000.0 Hz.

…

param[in] cartesian_position_filter_frequency Frequency at which the commanded * Cartesian position is cut off. * @param[in] cartesian_velocity_filter_frequency Frequency at which the commanded * Cartesian velocity is cut off. * @param[in] controller_filter_frequency Frequency at which the commanded torque is cut * off. * * @throw CommandException if the Control reports an error. * @throw NetworkException if the connection is lost, e.g. after a timeout.
*/ * Runs automatic error recovery on the robot. * * Automatic error recovery e.g. resets the robot after a collision occurred. * * @throw CommandException if the Control reports an error. * @throw NetworkException if the connection is lost, e.g. after a timeout. */ * Stops all currently running motions.
* * If a control or motion generator loop is running in another thread, it will be preempted * with a franka::ControlException. * * @throw CommandException if the Control reports an error. * @throw NetworkException if the connection is lost, e.g. after a timeout. */ * @} */ * Loads the model library from the robot. * * @return Model instance. * * @throw ModelException if the model library cannot be loaded. * @throw NetworkException if the connection is lost, e.g. after a timeout.

# Architecture & Design
Relevant source files - CHANGELOG.md
- CMakeLists.txt
- examples/CMakeLists.txt
- include/franka/robot.h
- src/robot.cpp
- src/robot_impl.cpp
- src/robot_impl.h
## Purpose and Scope
This document outlines the overall architecture and design of the libfranka library.
It explains the high-level components, their relationships, and the flow of control and data within the system.
The architecture is designed to provide a robust, real-time interface for controlling Franka Emika robots, supporting various control modes, motion generation, and state monitoring.
…
## High-Level Architecture Overview
The libfranka library is organized into several core components that work together to control Franka robots.
At a high level, the library provides interfaces for robot control, motion generation, robot state monitoring, and model-based calculations.
…
The architecture follows a layered design:
1. **User API Layer**: Provides high-level interfaces (`Robot`, `Gripper`, `Model` classes) for controlling the robot, accessing state information, and performing model-based calculations.
2. **Control Layer**: Handles motion generation, real-time control, and state monitoring through various control modes.
3. **Communication Layer**: Manages network communication with the physical robot, including command transmission and state reception.
…
## Core Components Architecture
The central component of libfranka is the `Robot` class, which serves as the main interface for users to interact with the robot hardware.
This class delegates most of its implementation to `Robot::Impl`, following the pimpl (pointer to implementation) pattern.
…
The `Robot` class provides multiple methods for controlling the robot, including different overloads for motion control (joint positions, joint velocities, Cartesian poses, Cartesian velocities) and combining these with torque control.
It also offers methods for configuring robot parameters such as impedance and collision behavior.
...
The control system in libfranka is built around a control loop architecture that can handle different types of motion generation and control commands.
The library supports various control modes including joint position, joint velocity, Cartesian pose, Cartesian velocity, and torque control.
…
The control loop operates with a 1 kHz frequency, requiring real-time constraints on the callback functions.
User-provided callbacks receive the current robot state and compute the appropriate control commands, which are then rate-limited, filtered, and sent to the robot.
...
The library communicates with the physical robot using a combination of TCP and UDP protocols.
TCP is used for command transmission and guaranteed responses, while UDP is used for high-frequency state updates.
…
The communication layer handles:
1. Command serialization and transmission
2. State reception and deserialization
3. Error handling and protocol negotiation
4. Real-time constraints for control loops
...
1. **Poco**: For networking and foundation classes
2. **Eigen3**: For linear algebra operations
3. **Pinocchio**: For robot dynamics calculations
4. **Threads**: For multi-threading support
5. **fmt**: For formatting