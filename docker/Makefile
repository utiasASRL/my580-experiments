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

# Run colcon inside the docker and save the updated image
build-zed-compiled:
	sudo docker run -it --net=host --gpus all --privileged \
	--name "zed_ros2_compiled" \
	${DOCKER_ARGS} zed_ros2_base  \
	colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
	sudo docker commit zed_ros2_compiled zed_ros2_built
	sudo docker rm zed_ros2_compiled

# Build the overlay image (depends on base image build)
.PHONY: build-overlay
build-overlay:
	sudo docker build -f dockerfile_zed_ros2_overlay -t zed_ros2_overlay .
	
run-overlay:
	sudo docker run -it --gpus all --privileged \
	--net=host --ipc=host \
	${DOCKER_ARGS} \
	--volume="${ROS2_WS_LOCAL}/src/my580_ros2/":"${ROS2_WS_DOCKER}/src/my580_ros2/":rw \
	--name "$(NAME)_overlay" \
	zed_ros2_overlay bash
	sudo docker container rm $(NAME)_overlay

launch-zed2:
	sudo docker exec -it $(CONT) ros2 launch zed_wrapper zed2.launch.py

# run zed2 camera publisher container.
run-zed2:
	sudo docker run -it --gpus all --privileged \
	--net=host --ipc=host \
	${DOCKER_ARGS} \
	--volume="${ROS2_WS_LOCAL}/src/my580_ros2/":"${ROS2_WS_DOCKER}/src/my580_ros2/":rw \
	--name "zed2_publish" \
	zed_ros2_built ros2 launch zed_wrapper zed2.launch.py
	sudo docker container rm zed2_publish