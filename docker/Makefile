ROS2_WS_LOCAL = "/home/asrl/research/my580ds/"
ROS2_WS_DOCKER = "/my580_ros2_ws"

DOCKER_VOLUMES = \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix"
DOCKER_ENV_VARS = \
	--env="NVIDIA_DRIVER_CAPABILITIES=all" \
	--env="DISPLAY" 
DOCKER_ARGS = ${DOCKER_VOLUMES} ${DOCKER_ENV_VARS}

# Build the core image
.PHONY: build-core
build-core:
	docker build -f dockerfile_zed_ros2 -t zed_ros2 .

# Build the base image
.PHONY: build-base
build-base: build-core
	docker build -f dockerfile_zed_ros2_base -t zed_ros2_base .

# Run colcon inside the docker and save the updated image
build-zed-compiled: build-base
	docker run -it --net=host --gpus all --privileged \
	--name "zed_ros2_compiled" \
	${DOCKER_ARGS} zed_ros2_base  \
	colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
	docker commit zed_ros2_compiled zed_ros2_built
	docker rm zed_ros2_compiled

# Build the overlay image (depends on base image build)
.PHONY: build-overlay
build-overlay:
	docker build -f dockerfile_zed_ros2_overlay -t zed_ros2_overlay .

# Build the apriltag recognition container
build-apriltag:
	docker build -f dockerfile_apriltag_overlay -t apriltag_overlay .
	docker run -it --net=host --ipc=host --gpus all --privileged \
	--name "apriltag_compile" \
	--volume="${ROS2_WS_LOCAL}/src/tag_recog/":"${ROS2_WS_DOCKER}/src/tag_recog":rw \
	${DOCKER_ARGS} apriltag_overlay bash
#colcon build --symlink-install
#docker commit apriltag_compile apriltag_overlay
	docker rm apriltag_compile
	

# RUN PARTS
# Open a terminal with ros2
run-ros-term:
	docker run -it --gpus all --privileged \
	--net=host --ipc=host \
	${DOCKER_ARGS} \
	--volume="${ROS2_WS_LOCAL}/src/my580_ros2/":"${ROS2_WS_DOCKER}/src/my580_ros2/":rw \
	--name "ros_terminal" \
	zed_ros2_overlay bash
	docker container rm ros_terminal

# Dev terminal for apriltag
run-apriltag-term:
	docker run -it --gpus all --privileged \
	--net=host --ipc=host \
	${DOCKER_ARGS} \
	--volume="${ROS2_WS_LOCAL}/src/my580_ros2/":"${ROS2_WS_DOCKER}/src/my580_ros2/":rw \
	--name "apriltag_dev_term" \
	apriltag_overlay bash
	docker container rm apriltag_dev_term

# run zed2 camera publisher container.
run-zed2:
	docker run -it --gpus all --privileged \
	--net=host --ipc=host \
	${DOCKER_ARGS} \
	--volume="${ROS2_WS_LOCAL}/src/my580_ros2/":"${ROS2_WS_DOCKER}/src/my580_ros2/":rw \
	--name "zed2_publish" \
	zed_ros2_built ros2 launch zed_wrapper zed2.launch.py
	docker container rm zed2_publish

# Run visualization
run-rviz:
	docker run -it --gpus all --privileged \
	--net=host --ipc=host \
	${DOCKER_ARGS} \
	--volume="${ROS2_WS_LOCAL}/src/my580_ros2/":"${ROS2_WS_DOCKER}/src/my580_ros2/":rw \
	--name "rviz_container" \
	zed_ros2_built rviz2 -d src/my580_ros2/rvizconfig.rviz
	docker container rm rviz_container