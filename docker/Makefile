BAG_OUTPUT = "test"

ROS2_WS_LOCAL = "/home/asrl/research/my580-experiments/"
ROS2_WS_DOCKER = "/my580_ros2_ws"

DOCKER_VOLUMES = \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix" \
	--volume="/dev:/dev"

# rm means we remove the container after running it.
DOCKER_ENV_VARS = \
	--env="NVIDIA_DRIVER_CAPABILITIES=all" \
	--env="DISPLAY" \
	--net=host --ipc=host \
	-it --gpus all --privileged \

DOCKER_ARGS = ${DOCKER_ENV_VARS} ${DOCKER_VOLUMES} 

ROS_APRIL_VOLUMES = \
	--volume="${ROS2_WS_LOCAL}/src/apriltag_ros":"${ROS2_WS_DOCKER}/src/apriltag_ros":rw \
	--volume="${ROS2_WS_LOCAL}/src/apriltag_msg":"${ROS2_WS_DOCKER}/src/apriltag_msg":rw \
	--volume="${ROS2_WS_LOCAL}/apriltag":"${ROS2_WS_DOCKER}/apriltag":rw  \

ROS_VOLUMES = ${ROS_APRIL_VOLUMES} \
	--volume="${ROS2_WS_LOCAL}/ros2-vicon-receiver":"${ROS2_WS_DOCKER}/ros2-vicon-receiver":rw \
	--volume="${ROS2_WS_LOCAL}/uwb_ros2":"${ROS2_WS_DOCKER}/uwb_ros2":rw \
	--volume="${ROS2_WS_LOCAL}/output":"${ROS2_WS_DOCKER}/output":rw \
	--volume="${ROS2_WS_LOCAL}/config":"${ROS2_WS_DOCKER}/config":rw \
	--volume="${ROS2_WS_LOCAL}/params":"${ROS2_WS_DOCKER}/params":rw \
	--volume="${ROS2_WS_LOCAL}/scripts":"${ROS2_WS_DOCKER}/scripts":rw

# TODO(FD): limit below to selected topics. 
BAG_TOPICS = -a #\
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
	zed2/zed_node/right_raw/image_rect_gray
  #apriltag/image/left  \
	#apriltag/image/right

# Run colcon inside the docker and save the updated image
build-zed_ros2: 
	-docker container rm container_tmp
	docker build -f Dockerfile_zed_ros2_base -t zed_ros2_tmp .
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --name container_tmp zed_ros2_tmp bash -c "colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release --packages-select zed_wrapper"
	docker commit container_tmp zed_ros2
	-docker container rm container_tmp

# Build the apriltag recognition container
build-apriltag:
	docker build -f dockerfile_apriltag_overlay -t apriltag_overlay .
	docker run ${DOCKER_ARGS} ${ROS_APRIL_VOLUMES} \
	--name container_tmp \
	apriltag_overlay bash -c "colcon build --symlink-install"
	docker commit container_tmp apriltag_overlay

# build apriltag with vicon container
build-apriltag-vicon:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name container_tmp \
	apriltag_overlay bash -c "cd ros2-vicon-receiver; ./install_libs.sh; cd vicon_receiver; colcon build --symlink-install" 
	docker commit container_tmp apriltag_vicon_overlay

build-uwb:
	docker build -t uwb_ros ${ROS2_WS_LOCAL}/uwb_ros2/
	
# RUN PARTS
# Dev terminal for apriltag
run-apriltag-term:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \ 
	--name "run-apriltag-term" \
	apriltag_backup bash 

run-apriltag-backup:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-apriltag-backup" \
	apriltag_backup scripts/run_stereo_april.sh

# Run zed2 camera publisher
# we link the shared params/zed2-custom.yaml paramters file to where the zed node 
# loads the parameters files at runtime, so that we can easily tune parameters.
run-zed2:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --name "run-zed2" --rm zed_ros2 bash -c \
	"rm src/zed-ros2-wrapper/zed_wrapper/config/common.yaml; ln -s params/zed2-custom.yaml src/zed-ros2-wrapper/zed_wrapper/config/common.yaml" 
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --name "run-zed2" zed_ros2 ros2 launch zed_wrapper zed2.launch.py

run-zed2-term:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} --name "run-zed2-term2" zed_ros2 bash

# Run vicon publisher
run-vicon:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-vicon" \
	apriltag_vicon_overlay bash -c \
	"source ros2-vicon-receiver/vicon_receiver/install/local_setup.bash; ros2 launch vicon_receiver client.launch.py"

run-vicon-term:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-vicon-bash" \
	apriltag_vicon_overlay bash

# Run visualization
run-rviz:
	xhost + 
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-rviz" --env "QT_DEBUG_PLUGINS=1" \
	apriltag_vicon_overlay rviz2 -d config/aprilconfig.rviz

# Record bag file
run-bag-record: 
	-docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-bag-record" \
	apriltag_backup bash -c "source ros2-vicon-receiver/vicon_receiver/install/local_setup.bash; cd output/; ros2 bag record -o ${BAG_OUTPUT} ${BAG_TOPICS}"

# Replay bag file
run-bag-play:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-bag-play" \
	apriltag_backup bash -c "source ros2-vicon-receiver/vicon_receiver/install/local_setup.bash; cd output/; ros2 bag play ${BAG_OUTPUT} ${extra_args};"

# runUWB node
run-uwb:
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-uwb" uwb_ros 
