# Source: https://github.com/TheGreatGalaxy/sensor-fusion
# Title: sensor-fusion (KF/EKF/UKF with Radar/LiDAR models) — GitHub
# Fetched via: trafilatura
# Date: 2026-04-09

Sensor Fusion with KF, EKF, and UKF for CV & CTRV Process Models and Lidar & Radar Measurements Models
This repository contains implementations of Kalman filter, extended Kalman filter, and unscented Kalman filter for the selected process and measurement models.
Process Models:
Measurement Models:
The project relies on the
[Eigen library](http://eigen.tuxfamily.org/index.php?title=Main_Page) for vector and matrix operations.
A great effort has been put in designing abstractions of filter, process model, and measurement model. The code heavily relies on C++ templates and avoids dynamic memory allocations, which is crucial for embedded systems, such as, self-driving car's onboard computer.
There are several files defining int main(int, char**)
function.
[udacity_sim_main.cpp](/TheGreatGalaxy/sensor-fusion/blob/master/src/mains/udacity_sim_main.cpp)- Use it in conjunction with the
[Udacity Self-Driving Car Engineer Nanodegree Term 2 Simulator](https://github.com/udacity/self-driving-car-sim/releases)for checking how the sensor fusion works on simulated measurement data.
- Use it in conjunction with the
[all_main.cpp](/TheGreatGalaxy/sensor-fusion/blob/master/src/mains/all_main.cpp)- Use it to check that all possible configurations of filters, process models, and measurement models compile.
[test.cpp](/TheGreatGalaxy/sensor-fusion/blob/master/test/test.cpp)- Use it to run unit tests.
One of the configurations works with the
[Udacity Self-Driving Car Engineer Nanodegree Term 2 Simulator](https://github.com/udacity/self-driving-car-sim/releases).
- cmake >= 3.5
- gcc/g++ >= 6.0
Additional:
- For
[udacity_sim_main.cpp](/TheGreatGalaxy/sensor-fusion/blob/master/src/mains/udacity_sim_main.cpp)[uWebSocketIO](https://github.com/uWebSockets/uWebSockets)with commit hash e94b6e1[Udacity Self-Driving Car Engineer Nanodegree Term 2 Simulator](https://github.com/udacity/self-driving-car-sim/releases)
The project can be built by doing the following from the project top directory.
$> mkdir build
$> cd build
$> cmake ..
$> make
$> cd ..
- For
[udacity_sim_main.cpp](/TheGreatGalaxy/sensor-fusion/blob/master/src/mains/udacity_sim_main.cpp)runbuild/sensor_fusion_udacity_sim
and then run[Udacity Self-Driving Car Engineer Nanodegree Term 2 Simulator](https://github.com/udacity/self-driving-car-sim/releases). - For
[all_main.cpp](/TheGreatGalaxy/sensor-fusion/blob/master/src/mains/all_main.cpp)runbuild/sensor_fusion_all
. - For unit tests run
build/sensor_fusion_test
.
While implementing different variations of Kalman filters, the notation from the book "Thrun, S., Burgard, W. and Fox, D., 2005. Probabilistic robotics. MIT press." was followed.
The equations below describe the Kalman filter and are implemented in
the [KalmanFilter](/TheGreatGalaxy/sensor-fusion/blob/master/src/filters/KalmanFilter.hpp) class.
For explanations of what each variable means, please, refer to comments in the code in corresponding files or
the book "Thrun, S., Burgard, W. and Fox, D., 2005. Probabilistic robotics. MIT press."
The equations below describe the extended Kalman filter and are implemented in
the [ExtendedKalmanFilter](/TheGreatGalaxy/sensor-fusion/blob/master/src/filters/ExtendedKalmanFilter.hpp) class.
[
For explanations of what each variable means, please, refer to comments in the code in corresponding files or
the book "Thrun, S., Burgard, W. and Fox, D., 2005. Probabilistic robotics. MIT press."](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/Algorithm_Extended_Kalman_filter.png)
The equations below describe the unscented Kalman filter and are implemented in
the [UnscentedKalmanFilter](/TheGreatGalaxy/sensor-fusion/blob/master/src/filters/UnscentedKalmanFilter.hpp) class.
[
For explanations of what each variable means, please, refer to comments in the code in corresponding files or
the book "Thrun, S., Burgard, W. and Fox, D., 2005. Probabilistic robotics. MIT press."](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/Algorithm_Unscented_Kalman_filter.png)
The following illustration helps to understand what the state vector dimensions mean.
The CV process model is a process model where the object moves linearly with constant velocity.
In this project, CV process model dials with a 2D world.
The state vector consists of 4 components---px, py, vx, vy---where p* represents the position and v* represents
the velocity. The leftmost column in the following equation represents the additive process noise;
a* represents acceleration.
[
The CV process model is implemented as a ](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/CV_process_model.png)[CVProcessModel](/TheGreatGalaxy/sensor-fusion/blob/master/src/process_models/CVProcessModel.hpp) class.
The CTRV process model is a process model where the object moves with a constant turn rate and velocity,
that is, with zero longitudinal and yaw accelerations. CTRV process model dials with a 2D world.
The state vector consists of 5 components---px, py, v, yaw, yaw_rate---where p* represents the position,
v represents the velocity module, yaw represents
the [yaw angle](https://en.wikipedia.org/wiki/Aircraft_principal_axes), and yaw_rate represents the yaw velocity.
The leftmost column in the following equation represents the non-linear process noise;
a_a represents longitudinal acceleration, and a_psi is yaw acceleration.
where
[
and
](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/CTRV_process_model_alpha.png)[
The results of solving these integrals depends on the yaw_rate,
see ](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/CTRV_process_model_beta.png)[CTRVProcessModel](/TheGreatGalaxy/sensor-fusion/blob/master/src/process_models/CTRVProcessModel.hpp).
The Lidar measurement model is a linear measurement model. This project does not deal with the lidar point cloud.
It assumes that the lidar point cloud has already been processed and a single measurement vector
has been identified for the object under consideration.
The measurement vector consists of 2 components---px, py---where p* represents the position.
The transformation from the state space to the Lidar measurement space is as follows
[
where
](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/Lidar_measurement_model.png)[
The Lidar measurement model is implemented as
a ](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/Lidar_measurement_model_H.png)[LidarMeasurementModel](/TheGreatGalaxy/sensor-fusion/blob/master/src/measurement_models/LidarMeasurementModel.hpp) class.
The Radar measurement model is a non-linear measurement model. The measurement vector consists of 3 components---range,
bearing, range_rate---where the range is a radial distance from the origin,
the bearing is an angle between range and X-axis which points into the direction of the heading of the vehicle,
where sensors are installed, and range_rate is a radial velocity.
The transformation from the state space to the Radar measurement space is as follows
[
where
](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/Radar_measurement_model.png)[
The Radar measurement model is implemented as
a ](/TheGreatGalaxy/sensor-fusion/blob/master/docs/pics/Radar_measurement_model_h.png)[RadarMeasurementModel](/TheGreatGalaxy/sensor-fusion/blob/master/src/measurement_models/RadarMeasurementModel.hpp) class.