ROS2_WS_LOCAL = "/home/asrl/research/my580ds/"
ROS2_WS_DOCKER = "/my580_ros2_ws"

DOCKER_VOLUMES = \
	--volume="/tmp/.X11-unix:/tmp/.X11-unix"
DOCKER_ENV_VARS = \
	--env="NVIDIA_DRIVER_CAPABILITIES=all" \
	--env="DISPLAY" \
	--net=host --ipc=host \
	-it --gpus all --privileged
DOCKER_ARGS = ${DOCKER_ENV_VARS} ${DOCKER_VOLUMES} 

ROS_APRIL_VOLUMES = \
	--volume="${ROS2_WS_LOCAL}/src/tag_recog":"${ROS2_WS_DOCKER}/src/tag_recog":rw

ROS_VOLUMES = ${ROS_APRIL_VOLUMES}\
	--volume="${ROS2_WS_LOCAL}/ros2-vicon-receiver":"${ROS2_WS_DOCKER}/ros2-vicon-receiver":rw \
	--volume="${ROS2_WS_LOCAL}/output":"${ROS2_WS_DOCKER}/output":rw

BAG_OUTPUT = "test"
BAG_TOPICS = \
	zed2/zed_node/left/image_rect_color \
	zed2/zed_node/right/image_rect_color  \
  apriltag/image/left  \
	apriltag/image/right

# Run colcon inside the docker and save the updated image
build-zed-compiled: 
	docker build -f dockerfile_zed_ros2_base -t zed_ros2_base .
	-docker container rm -f container_tmp 
	docker run ${DOCKER_ARGS} \
	--name container_tmp \
	zed_ros2_base \
	colcon build --symlink-install --cmake-args=-DCMAKE_BUILD_TYPE=Release
	docker commit container_tmp zed_ros2_built
	docker container rm container_tmp 

# Build the apriltag recognition container
build-apriltag:
	docker build -f dockerfile_apriltag_overlay -t apriltag_overlay .
	-docker container rm -f container_tmp 
	docker run ${DOCKER_ARGS} ${ROS_APRIL_VOLUMES} \
	--name container_tmp \
	apriltag_overlay bash -c "colcon build --symlink-install"
	docker commit container_tmp apriltag_overlay
	docker container rm container_tmp 

build-apriltag-vicon:
	-docker container rm -f container_tmp
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name container_tmp \
	apriltag_overlay bash -c "cd ros2-vicon-receiver; ./install_libs.sh; cd vicon_receiver; colcon build --symlink-install" 
	docker commit container_tmp apriltag_vicon_overlay
	docker container rm container_tmp 
	
# RUN PARTS
# Dev terminal for apriltag
run-apriltag-term:
	-docker container rm -f "run-apriltag-term"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-apriltag-term" \
	apriltag_overlay bash
	docker container rm -f "run-apriltag-term" 

# Run zed2 camera publisher
run-zed2:
	-docker container rm -f "run-zed2"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-zed2" \
	zed_ros2_built ros2 launch zed_wrapper zed2.launch.py
	docker container rm -f "run-zed2" 

# Run vicon publisher
run-vicon:
	-docker container rm -f "run-vicon"
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-vicon" \
	apriltag_vicon_overlay bash -c \
	"source ros2-vicon-receiver/vicon_receiver/install/local_setup.bash; ros2 launch vicon_receiver client.launch.py"
	docker container rm -f "run-vicon"

# Run visualization
run-rviz:
	xhost + 
	-docker container rm -f "run-rviz" 
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-rviz" --env "QT_DEBUG_PLUGINS=1" \
	apriltag_vicon_overlay rviz2 -d rvizconfig.rviz
	docker container rm -f "run-rviz"

# Record bag file
run-bag-record: 
	-docker container rm -f "run-bag-record"
	-docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-bag-record" \
	zed_ros2_built bash -c "cd output/; ros2 bag record -o ${BAG_OUTPUT} ${BAG_TOPICS}"
	docker container rm -f "run-bag-record" 

# Replay bag file
run-bag-play:
	-docker container rm -f "run-bag-play" 
	docker run ${DOCKER_ARGS} ${ROS_VOLUMES} \
	--name "run-bag-play" \
	zed_ros2_built bash -c "cd output/; ros2 bag play ${BAG_OUTPUT}"
	docker container rm -f "run-bag-play" 
