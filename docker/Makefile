BAG_OUTPUT = "test"

ROS2_WS_LOCAL = "/home/asrl/research/my580-experiments/workspace"
ROS2_WS_DOCKER = "/home/ros/my580_ros2_ws/workspace"

DOCKER_VOLUMES = \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix" \
	--volume="/dev:/dev"

DOCKER_ENV_VARS = \
	--env="NVIDIA_DRIVER_CAPABILITIES=all" \
	--env="DISPLAY" \
	--net=host --ipc=host \
	-it --gpus all --privileged 

BAG_TOPICS = \
	zed2/zed_node/left/camera_info \
	zed2/zed_node/left/image_rect_color \
	zed2/zed_node/left/image_rect_gray \
	zed2/zed_node/left_raw/camera_info \
	zed2/zed_node/left_raw/image_rect_color \
	zed2/zed_node/left_raw/image_rect_gray \
	zed2/zed_node/right/camera_info \
	zed2/zed_node/right/image_rect_color \
	zed2/zed_node/right/image_rect_gray \
	zed2/zed_node/right_raw/camera_info \
	zed2/zed_node/right_raw/image_rect_color \
	zed2/zed_node/right_raw/image_rect_gray \
	zed2/zed_node/disparity/disparity_image \
	zed2/zed_node/depth/depth_registered \
	zed2/zed_node/odom \
	zed2/zed_node/pose_with_covariance \
	zed2/zed_node/imu/data \
	zed2/zed_node/imu/data_raw \
	zed2/zed_node/imu/mag \
	zed2/zed_node/atm_press \
	zed2/zed_node/left_cam_imu_transform \
	diagnostics \
	detections/left \
	detections/right \

DOCKER_ARGS = ${DOCKER_ENV_VARS} ${DOCKER_VOLUMES} 

ROS_VOLUMES = \
	--volume="${ROS2_WS_LOCAL}":"${ROS2_WS_DOCKER}":rw

build-zed_ros2: 
	docker build -f Dockerfile_zed_ros2_base -t zed_ros2_tmp .
	-docker container rm container_tmp
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --name container_tmp \
		zed_ros2_tmp bash -c "colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release"
	docker commit container_tmp zed_ros2
	-docker container rm container_tmp

build-uwb:
	docker build -t uwb_ros ${ROS2_WS_LOCAL}/src/uwb_ros2/

run-tmp:
	-docker container rm "run-zed2-tmp"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-zed2-tmp" \
		zed_ros2_tmp bash

run-devel:
	-docker container rm "run-zed2-term"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-zed2-term" \
		zed_ros2 bash

run-uwb:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-uwb" \
		uwb_ros 

run-zed2:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-zed2" \
		zed_ros2 ros2 launch zed_wrapper zed2.launch.py

run-april-left:
	-docker container rm "run-april-left"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-april-left" \
		zed_ros2 scripts/run_stereo_april.sh

run-april-right:
	-docker container rm "run-april-right"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-april-right" \
		zed_ros2 scripts/run_stereo_april.sh

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

# Record bag file
run-bag-record: 
	-docker container rm --force "run-bag-record"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-bag-record" \
		zed_ros2 bash -c "cd output/; ros2 bag record -o ${BAG_OUTPUT} ${BAG_TOPICS}"

# Replay bag file
run-bag-play:
	-docker container rm "run-bag-play"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --rm --name "run-bag-play" \
		zed_ros2 bash -c "cd output/; ros2 bag play ${BAG_OUTPUT} ${extra_args};"
