ROS2_WS_LOCAL = "/home/asrl/research/my580ds/"
ROS2_WS_DOCKER = "/my580_ros2_ws"

DOCKER_VOLUMES = \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix:rw"
DOCKER_ENV_VARS = \
	--env="NVIDIA_DRIVER_CAPABILITIES=all" \
	--env="DISPLAY" 
DOCKER_ARGS = ${DOCKER_VOLUMES} ${DOCKER_ENV_VARS}

# Build the core image
.PHONY: build-core
build-core:
	sudo docker build -f dockerfile_zed_ros2 -t zed_ros2 .

# Build the base image
.PHONY: build-base
build-base: build-core
	sudo docker build -f dockerfile_zed_ros2_base -t zed_ros2_base .

# Build the overlay image (depends on base image build)
.PHONY: build-overlay
build-overlay: build-base
	sudo docker build -f dockerfile_zed_ros2_overlay -t zed_ros2_overlay .

run-base:
	sudo docker run -it --net=host --gpus all --privileged \
	${DOCKER_ARGS} zed_ros2_base bash

run-built:
	sudo docker run -it --net=host --gpus all --privileged \
	${DOCKER_ARGS} zed_ros2_built bash

run-overlay:
	sudo docker run -it --net=host --gpus all --privileged \
	${DOCKER_ARGS} \
	--volume="${ROS2_WS_LOCAL}/src/my580_ros2/":"${ROS2_WS_DOCKER}/src/my580_ros2/":rw \
	zed_ros2_overlay bash
