BAG_OUTPUT = "2023-05-10-T16-05-loop-2d-v2"
BAG_OUTPUT = "2023-05-10-T16-08-loop-2d-fast-v2"
BAG_OUTPUT = "2023-05-10-T16-16-loop-3d-v2"
#BAG_OUTPUT = "2023-05-10-T17-29-los-v3"

#BAG_OUTPUT = "2023-05-11-T16-15-loop-2d-1tag-v2"
#BAG_OUTPUT = "2023-05-11-T16-15-loop-2d-fast-1tag"
#BAG_OUTPUT = "2023-05-11-T16-15-loop-3d-1tag"
#BAG_OUTPUT = "2023-05-11-T16-15-zigzag-1tag"
#BAG_OUTPUT = "2023-05-11-T16-15-eight-1tag"
#BAG_OUTPUT = "2023-05-11-T16-15-eight-1tag-v2"
#BAG_OUTPUT = "2023-05-11-T16-15-eight-1tag-v2"

#BAG_OUTPUT = "2023-05-12-T11-20-loop-2d-1tag-nlos"
#BAG_OUTPUT = "2023-05-12-T11-20-uwb-test2"
#BAG_OUTPUT = "2023-05-12-T11-20-loop-2d-1tag-nlos-v3"
#BAG_OUTPUT = "2023-05-12-T11-20-ell"
#BAG_OUTPUT = "2023-05-12-T11-20-loop-3d"
#BAG_OUTPUT = "2023-05-12-T11-20-human-nlos"
#BAG_OUTPUT = "2023-05-12-T11-20-apriltag"
#BAG_OUTPUT = "2023-05-12-T16-00-decawave-v2"
BAG_OUTPUT = "2023-05-12-T16-00-dwm-loop-3d-v3"

ROS2_WS_LOCAL = "/home/asrl/research/my580-experiments/workspace"
ROS2_WS_DOCKER = "/home/asrl/research/my580-experiments/workspace"

DOCKER_VOLUMES = \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix" \

# We removed --net=host below because it seems to be incompatible 
# with this docker image
DOCKER_ENV_VARS = \
	--env="NVIDIA_DRIVER_CAPABILITIES=all" \
	--ipc=host \
	--env="DISPLAY" \
	--gpus all \
	-it --privileged 

#BAG_TOPICS = \
	zed2i/zed_node/right/image_rect_color/compressed \
	zed2i/zed_node/left/image_rect_color/compressed \
	zed2i/zed_node/imu/data 

BAG_TOPICS = \
	zed2i/zed_node/left/camera_info \
	zed2i/zed_node/left/image_rect_color/compressed \
	zed2i/zed_node/right/camera_info \
	zed2i/zed_node/right/image_rect_color/compressed \
	zed2i/zed_node/odom \
	zed2i/zed_node/pose_with_covariance \
	zed2i/zed_node/imu/data \
	zed2i/zed_node/imu/mag \
	zed2i/zed_node/atm_press \
	zed2i/zed_node/left_cam_imu_transform \
	diagnostics \
	detections/left \
	detections/right \
  uwb/range \
  tf \
  tf_static \
  vicon/robot/robot \
  vicon/environment/environment \
  vicon/uwb_markers/uwb_markers \
	vicon/obstacle/obstacle


DOCKER_ARGS = ${DOCKER_ENV_VARS} ${DOCKER_VOLUMES} 

ROS_VOLUMES = \
	--volume="${ROS2_WS_LOCAL}":"${ROS2_WS_DOCKER}":rw


kill:
	-docker container rm --force run-zed2
	-docker container rm --force run-zed2-tmp
	-docker container rm --force run-zed2-term
	-docker container rm --force run-uwb
	-docker container rm --force run-april-left
	-docker container rm --force run-april-right
	-docker container rm --force run-rviz
	-docker container rm --force run-vicon
	-docker container rm --force run-bag-play
	-docker container rm --force run-bag-record
	-tmux detach-client
	-tmux kill-session -t my580


build-zed_ros2: 
	docker build -f Dockerfile -t zed_ros2_tmp .
	-docker container rm container_tmp
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --name container_tmp \
		zed_ros2_tmp bash -c "colcon build --cmake-args=-DCMAKE_BUILD_TYPE=Release"
	docker commit container_tmp zed_ros2
	-docker container rm container_tmp

build-uwb:
	docker build -t uwb_ros ${ROS2_WS_LOCAL}/src/uwb_ros2/

run-devel:
	-docker container rm "run-zed2-term"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-zed2-term" \
		zed_ros2 bash

run-uwb:
	-docker container rm "run-uwb"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-uwb" zed_ros2 bash -c "ros2 run uwb_driver uwb_node --ros-args --params-file src/uwb_ros2/uwb_driver/config/params.yaml"

run-zed2:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-zed2" \
		zed_ros2 ros2 launch zed_wrapper zed2i.launch.py

run-april-left:
	-docker container rm "run-april-left"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-april-left" \
		zed_ros2 bash -c "scripts/run_april_left.sh"

run-april-right:
	-docker container rm "run-april-right"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-april-right" \
		zed_ros2 bash -c "scripts/run_april_right.sh"

run-rviz:
	-docker container rm "run-rviz"
	xhost + 
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-rviz" \
		--env "QT_DEBUG_PLUGINS=1" \
		zed_ros2 rviz2 -d config/aprilconfig.rviz

run-vicon:
	-docker container rm "run-vicon"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-vicon" \
		zed_ros2 ros2 launch vicon_receiver client.launch.py

vicon-term:
	-docker container rm "run-vicon"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-vicon" \
		zed_ros2 /bin/bash

# Record bag file
run-bag-record: 
	-docker container rm --force "run-bag-record"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-bag-record" \
		zed_ros2 bash -c "cd output/; ros2 bag record -o ${BAG_OUTPUT} ${BAG_TOPICS} --qos-profile-overrides-path ../params/bag-qos.yaml"

# Replay bag file
run-bag-play:
	-docker container rm "run-bag-play"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-bag-play" \
		zed_ros2 bash -c "cd output/; ros2 bag play -l ${BAG_OUTPUT} ${extra_args} --qos-profile-overrides-path ../params/bag-qos.yaml;"
